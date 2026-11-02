import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from harness_support import strict_schema, validate, validate_verdict


class HarnessTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='sqf-test-')
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        for name in ('orchestrate.py', 'harness_support.py', 'config.json', 'problem.md', 'prompts', 'hints', 'tests', 'isolation', 'agent-env'):
            src, target = SOURCE / name, self.root / name
            if src.is_dir():
                shutil.copytree(src, target, ignore=shutil.ignore_patterns('__pycache__'))
            else:
                shutil.copy2(src, target)
        venv = (Path(self.temp.name) / 'agent-venv').resolve()
        (venv / 'bin').mkdir(parents=True)
        (venv / 'bin/python3').symlink_to(sys.executable)
        self.env = dict(os.environ, AGENT_VENV=str(venv), LIT_ALLOW_FILE='1', RUNS_DIR=str(Path(self.temp.name) / 'runs'),
                        CLAUDE_BIN=str(self.root / 'tests/fake_claude.py'),
                        CODEX_BIN=str(self.root / 'tests/fake_codex.py'), BACKENDS='claude,codex')
        environment = patch.dict(os.environ, {'AGENT_VENV': str(venv)})
        environment.start()
        self.addCleanup(environment.stop)

    def tearDown(self):
        self.temp.cleanup()

    def run_step(self, *args, success=True):
        p = subprocess.run([sys.executable, str(self.root / 'orchestrate.py'), *args],
                           cwd=self.root, env=self.env, capture_output=True, text=True, timeout=30)
        if success:
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        else:
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
        return p

    def load_driver(self):
        with patch.dict(os.environ, self.env):
            spec = importlib.util.spec_from_file_location('sqf_test_driver', self.root / 'orchestrate.py')
            driver = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(driver)
        for name in ('logs', 'papers', 'plans'):
            (self.root / name).mkdir(exist_ok=True)
        driver.check_runs_dir()
        return driver

    def ready(self):
        self.run_step('numerics')
        candidates = sorted((self.root / 'numerics/candidates').iterdir())
        self.run_step('numerics', '--accept', candidates[0].name)
        self.run_step('plan', '--single')
        self.run_step('select', 'vaughan')

    def selected_numerics(self):
        acceptance = json.loads((self.root / 'numerics/accepted.json').read_text())
        return self.root / 'numerics' / acceptance['snapshot']

    def finish_two_props(self):
        # P3 is deliberately unprovable in fixtures; the integration fixture needs only P1/P2.
        shutil.rmtree(self.root / 'props/P3')
        plan = json.loads((self.root / 'plan.json').read_text())
        plan['propositions'] = plan['propositions'][:2]
        (self.root / 'plan.json').write_text(json.dumps(plan))
        self.run_step('prove')

    def test_end_to_end_all_backend_modes(self):
        for backend in ('claude,codex', 'codex', 'claude'):
            with self.subTest(backends=backend):
                self.env['BACKENDS'] = backend
                if backend == 'codex':
                    self.env['CLAUDE_BIN'] = '/nonexistent/claude'
                if backend == 'claude':
                    self.env['CODEX_BIN'] = '/nonexistent/codex'
                self.run_step('probe')
                self.run_step('literature')
                candidates = json.loads((self.root / 'literature/candidates.json').read_text())
                expected_models = ({'claude-opus-5-5', 'codex:gpt-6.1-sol'} if backend == 'claude,codex'
                                   else {'codex:gpt-6.1-sol'} if backend == 'codex'
                                   else {'claude-opus-5-5', 'claude-sonnet-5-5'})
                self.assertEqual({r['model'] for r in candidates}, expected_models)
                self.assertEqual(len(list((self.root / 'literature/searches').glob('*.json'))), len(expected_models))
                for model in expected_models:
                    items = [r for r in candidates if r['model'] == model]
                    self.assertEqual([r['status'] for r in items], ['downloaded', 'wishlist', 'rejected', 'rejected'])
                    self.assertIn('after the 2010 cutoff', items[2]['note'])
                    self.assertIn('blocked host gitlab.com', items[3]['note'])
                    self.assertIn(model, (self.root / 'literature/review.md').read_text())
                self.assertEqual(len(list((self.root / 'literature/pdf').glob('*.pdf'))), len(expected_models))
                self.assertFalse(any((self.root / 'papers').glob('*.pdf')), 'download must not auto-promote')
                self.ready()
                self.run_step('plan', '--single')
                self.assertEqual(len(list((self.root / 'plans').glob('*.json'))), 4)
                self.run_step('plan', '--cross')
                expected = 4 if backend == 'codex' else 8
                self.assertEqual(len(list((self.root / 'plans').glob('*.json'))), expected)
                self.run_step('prove')
                status = self.run_step('status').stdout
                self.assertRegex(status, r'P1\s+passed')
                self.assertRegex(status, r'P3\s+stuck')
                self.run_step('pollinate', 'P3')
                self.run_step('prove', 'P3')
                self.run_step('integrate', success=False)
                self.finish_two_props()
                self.run_step('integrate')
                summary = json.loads((self.root / 'report/integration.json').read_text())
                self.assertTrue(summary['composes'])
                self.assertEqual(len(summary['reviews']), 1 if backend == 'codex' else 2)
                leaks = self.run_step('check-leaks').stdout
                self.assertIn('exposure', leaks)
                self.assertIn('post-cutoff arxiv', leaks)
                self.assertIn('dehnert' if backend != 'claude' else 'riemannhypothesis', leaks)
                (self.root / 'literature/pdf/UPPER.PDF').write_bytes(b'%PDF-1.4\nfixture')
                self.run_step('archive', 'test')
                self.assertTrue((self.root / 'archive/test/literature/review.md').exists())
                self.assertFalse([p for p in (self.root / 'archive/test').rglob('*') if p.suffix.lower() == '.pdf'])
                records = self.root / 'archive/test/runs/_records'
                invocation = json.loads(next(records.glob('*/invocation.json')).read_text())
                self.assertIn('sources', invocation)
                self.assertIn('prompt', invocation)
                self.assertIn('inputs', invocation)
                rows = [json.loads(s) for s in (self.root / 'logs/costs.jsonl').read_text().splitlines()]
                if backend != 'claude,codex':
                    self.assertTrue(all(r['backend'] == backend for r in rows))
                for name in ('logs', 'plans', 'numerics', 'literature', 'props', 'report', 'archive'):
                    shutil.rmtree(self.root / name)
                (self.root / 'plan.json').unlink()
                shutil.rmtree(Path(self.env['RUNS_DIR']))
                self.env['CLAUDE_BIN'] = str(self.root / 'tests/fake_claude.py')
                self.env['CODEX_BIN'] = str(self.root / 'tests/fake_codex.py')

    def test_statement_and_ancestor_edits_invalidate(self):
        self.ready()
        self.finish_two_props()
        self.run_step('integrate')
        p = self.root / 'props/P1/statement.md'
        p.write_text(p.read_text() + '\nChanged contract\n')
        output = self.run_step('status').stdout
        self.assertRegex(output, r'P1\s+open')
        self.assertRegex(output, r'P2\s+open')
        self.assertTrue((self.root / 'report/STALE').exists())
        self.run_step('integrate', success=False)

    def test_proof_and_review_tampering_invalidates(self):
        self.ready()
        self.finish_two_props()
        p = self.root / 'props/P1/proof-v2.md'
        p.write_text(p.read_text() + '\nChanged proof\n')
        self.assertRegex(self.run_step('status').stdout, r'P1\s+open')
        review = self.root / 'props/P2/review-v2-0.json'
        review.write_text('{}')
        self.assertRegex(self.run_step('status').stdout, r'P2\s+open')

    def test_schemas_and_failed_turn(self):
        o = self.load_driver()
        v = {'verdict': 'pass', 'severity': 'banana', 'location': '', 'objection': '', 'other_issues': []}
        with self.assertRaises(ValueError):
            validate(v, o.SCHEMAS['verdict'])
        v['severity'] = 'gap'
        with self.assertRaises(ValueError):
            validate_verdict(v)
        plan = {'propositions': [{'id': 'P1', 'depends_on': []}, {'id': 'P1', 'depends_on': []}]}
        with self.assertRaises(ValueError):
            o.check_acyclic(plan['propositions'])
        wd = o.sandbox('bad-result', {})
        (wd / '_last.txt').write_text(json.dumps(v))
        self.assertIsNone(o.parse_codex('{"type":"turn.failed"}', wd, 'verdict'))
        (wd / '_last.txt').write_text('prefix ' + json.dumps(v))
        self.assertIsNone(o.parse_codex('{"type":"turn.completed"}', wd, 'verdict'))

    def test_capability_profiles(self):
        o = self.load_driver()
        for role in ('probe', 'referee', 'planner'):
            cmd = o.build_codex_cmd('prompt', o.role_capabilities(role), 'gpt-6.1-sol', 'high', Path('/tmp'))
            joined = ' '.join(cmd)
            self.assertIn('allow_login_shell=false', joined)
            self.assertIn('--disable apps', joined)
            self.assertIn('--disable plugins', joined)
            self.assertIn('--disable hooks', joined)
            self.assertIn('features.shell_tool=' + ('false' if role == 'probe' else 'true'), joined)
            self.assertIn('web_search="' + ('live' if role == 'planner' else 'disabled') + '"', joined)
        event = json.dumps({'type': 'item.completed', 'item': {'type': 'command_execution'}})
        self.assertTrue(o.capability_violations(event, 'codex', o.role_capabilities('probe')))
        event = json.dumps({'type': 'item.completed', 'item': {'type': 'mcp_tool_call'}})
        self.assertTrue(o.capability_violations(event, 'codex', o.role_capabilities('planner')))

    def test_timeout_kills_descendants_and_logs_failure(self):
        o = self.load_driver()
        slow = self.root / 'slow.py'
        child = self.root / 'child.py'
        child.write_text('import pathlib, signal, sys, time\n'
                         'def stop(*args):\n pathlib.Path("child-terminated").write_text("yes"); sys.exit(0)\n'
                         'signal.signal(signal.SIGTERM, stop)\n'
                         'pathlib.Path("child-started").write_text("yes")\ntime.sleep(60)\n')
        slow.write_text('import subprocess, time, sys\n'
                        f'p=subprocess.Popen([sys.executable,{str(child)!r}])\n'
                        'print("{\\"type\\":\\"system\\"}",flush=True)\ntime.sleep(60)\n')
        o.CLAUDE = sys.executable
        # Replace only the CLI construction; exercise the real process/group timeout path.
        o.build_cmd = lambda *args: [sys.executable, str(slow)]
        o.CFG['timeout_s'] = 1
        wd = o.sandbox('timeout', {})
        with self.assertRaisesRegex(RuntimeError, 'timed out'):
            o.run_agent('probe', wd, 'sonnet', 'high')
        row = json.loads((self.root / 'logs/costs.jsonl').read_text().splitlines()[-1])
        self.assertIn('timed out', row['failure'])
        self.assertTrue((wd / 'child-started').exists())
        self.assertTrue((wd / 'child-terminated').exists(), 'descendant did not receive group termination')

    def test_structured_output_tool_needs_a_schema(self):
        o = self.load_driver()
        event = json.dumps({'type': 'assistant', 'message': {'content': [
            {'type': 'tool_use', 'name': 'StructuredOutput', 'input': {}}]}})
        caps = o.role_capabilities('referee')
        self.assertEqual(o.capability_violations(event, 'claude', caps, 'verdict'), [])
        self.assertTrue(o.capability_violations(event, 'claude', caps))

    def test_interrupt_stops_agents_and_queued_work(self):
        pids = self.root / 'agent-pids'
        stub = self.root / 'slow.sh'
        stub.write_text('#!/bin/sh\n[ "$1" = --version ] && { echo stub; exit 0; }\n'
                        f'echo $$ >> {pids}\nexec sleep 60\n')
        stub.chmod(0o755)
        env = dict(self.env, CLAUDE_BIN=str(stub), CODEX_BIN=str(stub))
        driver = subprocess.Popen([sys.executable, str(self.root / 'orchestrate.py'), 'probe'], cwd=self.root,
                                  env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.addCleanup(driver.kill)
        deadline = time.time() + 15
        while time.time() < deadline and not (pids.exists() and len(pids.read_text().split()) == 2):
            time.sleep(0.05)
        started = [int(pid) for pid in pids.read_text().split()]
        self.assertEqual(len(started), 2, 'expected the two parallel agents, with the third queued')
        driver.send_signal(signal.SIGINT)
        self.assertEqual(driver.wait(timeout=15), 130)
        for pid in started:
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)
        self.assertEqual(len(pids.read_text().split()), 2, 'queued agent started after the interrupt')
        rows = [json.loads(line) for line in (self.root / 'logs/costs.jsonl').read_text().splitlines()]
        self.assertEqual([row['failure'] for row in rows], ['interrupted', 'interrupted'])

    def test_failed_round_restarts_with_same_number_and_model(self):
        self.ready()
        real = self.env['CLAUDE_BIN']
        broken = self.root / 'broken.sh'
        broken.write_text('#!/bin/sh\n[ "$1" = --version ] && { echo stub; exit 0; }\nexit 1\n')
        broken.chmod(0o755)
        self.env['CLAUDE_BIN'] = str(broken)
        self.run_step('prove', 'P1', success=False)
        self.assertEqual(json.loads((self.root / 'props/P1/status.json').read_text())['round'], 0)
        self.env['CLAUDE_BIN'] = real
        self.run_step('prove', 'P1')
        self.assertEqual(json.loads((self.root / 'props/P1/status.json').read_text())['round'], 2)
        self.assertEqual(sorted(p.name for p in (self.root / 'props/P1').glob('proof-v*.md')),
                         ['proof-v1.md', 'proof-v2.md'])

    def test_incomplete_objections_are_removed_with_their_proof(self):
        self.ready()
        pdir = self.root / 'props/P1'
        (pdir / 'proof-v1.md').write_text('Interrupted proof')
        (pdir / 'review-v1-0.json').write_text('{"incomplete": true}')
        (pdir / 'objections.md').write_text(
            '\n## Round 1 (against proof-v1)\n\nObjection to interrupted proof\n')
        self.assertEqual(json.loads((pdir / 'status.json').read_text())['round'], 0)

        self.run_step('prove', 'P1')

        objections = (pdir / 'objections.md').read_text()
        self.assertNotIn('Objection to interrupted proof', objections)
        self.assertEqual(objections.count('## Round 1 (against proof-v1)'), 1)
        self.assertNotIn('incomplete', (pdir / 'review-v1-0.json').read_text())
        self.assertEqual(json.loads((pdir / 'status.json').read_text())['round'], 2)

    def test_os_metadata_does_not_invalidate_approvals(self):
        self.ready()
        self.finish_two_props()
        (self.root / 'papers/.DS_Store').write_bytes(b'finder')
        self.assertRegex(self.run_step('status').stdout, r'P1\s+passed')
        o = self.load_driver()
        self.assertFalse((o.sandbox('metadata', {'papers': self.root / 'papers'}) / 'papers/.DS_Store').exists())
        (self.root / 'papers/note.txt').write_text('real corpus change')
        self.assertRegex(self.run_step('status').stdout, r'P1\s+open')

    def test_codex_search_results_are_exposure_not_attempt(self):
        o = self.load_driver()
        event = {'type': 'item.completed', 'item': {
            'id': 'ws', 'type': 'web_search', 'query': 'Croft 1975 squarefree',
            'action': {'type': 'search', 'queries': ['Croft 1975 squarefree']},
            'results': [{'type': 'text_result', 'title': 'Thesis',
                         'url': 'https://primes.recommend.games/thesis.pdf'}]}}
        kinds = {kind: text for kind, text in o._events(event)}
        self.assertNotIn('primes.recommend.games', kinds['attempt'])
        self.assertIn('Croft 1975', kinds['attempt'])
        self.assertIn('primes.recommend.games', kinds['exposure'])
        event['item'] |= {'query': 'https://primes.recommend.games/thesis.pdf',
                          'action': {'type': 'open_page', 'url': 'https://primes.recommend.games/thesis.pdf'}}
        self.assertIn('primes.recommend.games', dict(o._events(event))['attempt'])

    def test_stray_files_in_props_are_not_propositions(self):
        self.ready()
        (self.root / 'props/.DS_Store').write_bytes(b'finder')
        self.assertNotIn('.DS_Store', self.run_step('status').stdout)
        self.run_step('prove', 'P1')
        self.assertRegex(self.run_step('status').stdout, r'P1\s+passed')

    def test_global_concurrency(self):
        o = self.load_driver()
        active = 0
        peak = 0
        lock = threading.Lock()
        def fake(*args):
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
            time.sleep(.03)
            with lock:
                active -= 1
        o._run_agent = fake
        workers = [threading.Thread(target=o.run_agent, args=('probe', None, 'codex', 'high')) for _ in range(8)]
        for w in workers: w.start()
        for w in workers: w.join()
        self.assertEqual(peak, o.CFG['parallel'])

    def test_numerics_requires_acceptance(self):
        self.run_step('numerics')
        self.run_step('plan', success=False)
        candidate = sorted((self.root / 'numerics/candidates').iterdir())[0]
        self.run_step('numerics', '--accept', candidate.name)
        (self.selected_numerics() / 'results.json').write_text('{}')
        self.run_step('plan', success=False)

    def test_stale_plan_cache_and_refresh(self):
        self.ready()
        hint = self.root / 'hints/vaughan.md'
        hint.write_text(hint.read_text() + '\nAdditional strategy constraint.\n')
        self.assertIn('different inputs', self.run_step('plan', '--single', success=False).stderr)
        self.run_step('plan', '--single', '--refresh')
        self.run_step('plan', '--single')

    def test_legacy_approvals_and_review_policy_changes(self):
        self.ready()
        self.finish_two_props()
        path = self.root / 'props/P1/status.json'
        status = json.loads(path.read_text())
        status.pop('approval_hash')
        path.write_text(json.dumps(status))
        self.assertRegex(self.run_step('status').stdout, r'P1\s+open')
        prompt = self.root / 'prompts/referee.md'
        prompt.write_text(prompt.read_text() + '\nCheck an additional invariant.\n')
        self.assertRegex(self.run_step('status').stdout, r'P2\s+open')

    def test_failed_invocation_does_not_count_as_success(self):
        o = self.load_driver()
        binary = self.root / 'bad_cli.py'
        binary.write_text('import json\nprint(json.dumps({"type":"result","subtype":"success",'
                          '"structured_output":{"verdict":"pass","severity":"banana","location":"","objection":"","other_issues":[]}}))\n')
        o.CLAUDE = sys.executable
        o.build_cmd = lambda *args: [sys.executable, str(binary)]
        wd = o.sandbox('invalid-verdict', {})
        with self.assertRaisesRegex(RuntimeError, 'invalid enum'):
            o.run_agent('referee', wd, 'sonnet', 'high', schema='verdict')
        row = json.loads((self.root / 'logs/costs.jsonl').read_text().splitlines()[-1])
        self.assertIsNotNone(row['failure'])

    def test_run_directory_ownership(self):
        o = self.load_driver()
        owner = Path(self.env['RUNS_DIR']) / '_owner.json'
        owner.write_text(json.dumps({'checkout': '/another/checkout'}))
        with self.assertRaisesRegex(ValueError, 'another checkout'):
            o.check_runs_dir()
        owner.unlink()
        (owner.parent / 'legacy-run').mkdir()
        with self.assertRaisesRegex(ValueError, 'legacy runs'):
            o.check_runs_dir()

    def test_numerical_resume_and_supporting_code_hash(self):
        self.run_step('numerics')
        count = len(list(Path(self.env['RUNS_DIR']).glob('numerics-*')))
        self.run_step('numerics')
        self.assertEqual(len(list(Path(self.env['RUNS_DIR']).glob('numerics-*'))), count)
        candidate = sorted((self.root / 'numerics/candidates').iterdir())[0]
        self.run_step('numerics', '--accept', candidate.name)
        self.assertTrue((self.selected_numerics() / 'src/helper.py').is_file())
        (self.selected_numerics() / 'compute.py').write_text('# modified implementation\n')
        self.run_step('plan', success=False)

    def test_docker_mounts_and_prompt_preservation(self):
        spec = importlib.util.spec_from_file_location('sqf_docker_runner', self.root / 'isolation/docker_runner.py')
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        auth = Path(self.temp.name) / 'auth.json'
        auth.write_text('{}')
        prompt = 'Literal $(do-not-execute) `backticks` "quotes"\nsecond line'
        _, cmd = runner.command('test-image', '/agent/input', '/agent/output', 'codex',
                                ['codex', 'exec', prompt], {'CODEX_AUTH_FILE': str(auth)}, readonly=True)
        mounts = [cmd[i + 1] for i, arg in enumerate(cmd) if arg == '--mount']
        self.assertEqual(len(mounts), 3)
        self.assertIn('type=bind,src=/agent/input,dst=/workspace,readonly', mounts)
        self.assertIn('type=bind,src=/agent/output,dst=/outputs', mounts)
        self.assertEqual(cmd[-1], prompt)
        self.assertNotIn(prompt, cmd[cmd.index('-c') + 1])
        self.assertNotIn('/var/run/docker.sock', ' '.join(cmd))
        self.assertNotIn(str(self.root), ' '.join(cmd))
        with self.assertRaisesRegex(ValueError, 'CLAUDE_CODE_OAUTH_TOKEN'):
            runner.command('image', '/input', '/output', 'claude', ['claude'], {})

    def test_transitive_contract_and_defect_cannot_pass_as_proof(self):
        self.ready()
        o = self.load_driver()
        before = o.contract_hash('P3')
        statement = self.root / 'props/P1/statement.md'
        statement.write_text(statement.read_text() + '\nChanged ancestor\n')
        self.assertNotEqual(before, o.contract_hash('P3'))
        def fake_agent(role, workdir, *args, **kwargs):
            if role == 'prover':
                (workdir / 'proof.md').write_text('STATEMENT DEFECT: counterexample\n')
                return {'result': 'done'}
            return {'structured_output': {'verdict': 'pass', 'severity': 'none',
                                         'location': '', 'objection': '', 'other_issues': []}}
        o.run_agent = fake_agent
        with self.assertRaisesRegex(ValueError, 'cannot be approved as a proof'):
            o.prove_one('P1')
        self.assertNotEqual(o.status('P1')['state'], 'passed')

    def test_symlink_outputs_cannot_read_host_files(self):
        o = self.load_driver()
        secret = Path(self.temp.name) / 'outside.txt'
        secret.write_text('outside host file')
        binary = self.root / 'symlink_cli.py'
        binary.write_text('import pathlib, json\n'
                          f'pathlib.Path("proof.md").symlink_to({str(secret)!r})\n'
                          'print(json.dumps({"type":"result","subtype":"success","result":"done"}))\n')
        o.CLAUDE = sys.executable
        o.build_cmd = lambda *args: [sys.executable, str(binary)]
        wd = o.sandbox('symlink-test', {})
        with self.assertRaisesRegex(RuntimeError, 'symlinks'):
            o.run_agent('prover', wd, 'sonnet', 'high')
        record = Path(self.env['RUNS_DIR']) / '_records' / wd.name
        self.assertNotIn('outside host file', (record / 'outcome.json').read_text())
        self.assertTrue((record / '_stream.jsonl').exists())

    def test_numerical_evidence_bound_to_problem(self):
        self.run_step('numerics')
        candidate = sorted((self.root / 'numerics/candidates').iterdir())[0]
        self.run_step('numerics', '--accept', candidate.name)
        problem = self.root / 'problem.md'
        problem.write_text(problem.read_text() + '\nChanged definition\n')
        self.run_step('plan', success=False)
        self.run_step('numerics', '--accept', candidate.name, success=False)

    def test_agent_environment_preflight_and_opt_out(self):
        self.env['AGENT_VENV'] += '/missing'
        result = self.run_step('probe', success=False)
        self.assertIn('does not exist', result.stderr)
        self.assertFalse(Path(self.env['RUNS_DIR']).exists(), 'fail before creating/starting runs')
        self.run_step('status')
        self.env.pop('AGENT_VENV')
        config = json.loads((self.root / 'config.json').read_text())
        config['agent_venv'] = None
        (self.root / 'config.json').write_text(json.dumps(config))
        self.run_step('probe')

    def test_environment_inside_git_worktree_is_rejected(self):
        # A real temporary Git tree verifies the check, independent of this repo's parent.
        venv = self.root / 'agent-venv'
        (venv / 'bin').mkdir(parents=True)
        (venv / 'bin/python3').symlink_to(sys.executable)
        subprocess.run(['git', 'init', '--quiet', str(self.root)], check=True)
        self.env['AGENT_VENV'] = str(venv)
        result = self.run_step('probe', success=False)
        self.assertIn('inside the git work tree', result.stderr)

    def test_cutoff_scan_and_literature_vetting(self):
        o = self.load_driver()
        for identifier in ('2006.04060', '1912.04683v2', '1101.0001'):
            self.assertEqual(len(o._post_cutoff('arxiv.org/pdf/' + identifier)), 1)
        for text in ('arXiv:1012.5674', 'arXiv:0905.1234', 'arXiv:math/0501123',
                     'arXiv:1715.76478', '2026.1234 in a table', 'Journal 2015'):
            self.assertFalse(o._post_cutoff(text), text)
        event = json.dumps({'type': 'assistant', 'message': {'content': [
            {'type': 'text', 'text': 'arXiv:1912.04683 and arXiv:1012.5674'}]}})
        probe = o.sandbox('probe-memory', {})
        (probe / '_stream.jsonl').write_text(event)
        self.assertFalse(o.scan_leaks(probe))
        planner = o.sandbox('plan-check', {})
        (planner / '_stream.jsonl').write_text(event)
        self.assertEqual(sum(h['pattern'] == 'post-cutoff arxiv' for h in o.scan_leaks(planner)), 1)
        item = {'year': 2005, 'authors': 'A. Author', 'title': 'Useful estimate',
                'url': 'https://example.org/paper', 'pdf_url': ''}
        self.assertIsNone(o.vet_item(item))
        for changes, reason in (
                ({'year': 2015}, 'cutoff'),
                ({'authors': 'F. Dehnert'}, 'excluded pattern'),
                ({'url': 'https://sub.riemannhypothesis.blog/paper'}, 'excluded pattern'),
                ({'url': 'https://gitlab.com/notes'}, 'blocked host'),
                ({'pdf_url': 'https://sci-hub.example/paper'}, 'blocked host'),
                ({'url': 'https://arxiv.org/abs/1912.04683'}, 'arXiv'),
                ({'year': None}, 'no publication year')):
            self.assertIn(reason, o.vet_item(item | changes))
        for relevance in (0, 4):
            from fixture_schema import fill
            value = fill({'items': [item | {'id': 'test', 'kind': 'article',
                                          'access': 'unknown', 'why': 'test', 'relevance': relevance}]},
                         o.SCHEMAS['literature'])
            with self.assertRaises(ValueError):
                validate(value, o.SCHEMAS['literature'])
        pdf = Path(self.temp.name) / 'test.pdf'
        pdf.write_bytes(b'%PDF-1.4\nfixture')
        dest = self.root / 'download.pdf'
        with patch.dict(os.environ, {'LIT_ALLOW_FILE': '1'}):
            self.assertIsNone(o.fetch_pdf(pdf.as_uri(), dest))
        self.assertEqual(dest.read_bytes(), pdf.read_bytes())
        with patch.dict(os.environ, {}, clear=True):
            self.assertIn('unsupported URL scheme', o.fetch_pdf(pdf.as_uri(), dest))
        html = Path(self.temp.name) / 'paywall.html'
        html.write_text('<html>paywall</html>')
        with patch.dict(os.environ, {'LIT_ALLOW_FILE': '1'}):
            self.assertIn('not a PDF', o.fetch_pdf(html.as_uri(), dest))

    def test_docker_has_locked_environment_without_host_venv_mount(self):
        dockerfile = (self.root / 'isolation/Dockerfile').read_text()
        self.assertIn('uv sync --locked --project /opt/agent-env --python 3.12', dockerfile)
        self.assertIn('VIRTUAL_ENV=/opt/agent-venv', dockerfile)
        o = self.load_driver()
        o.CFG['isolation']['mode'] = 'docker'
        # Docker mode must not fail because a macOS host environment is absent.
        with patch.object(o, 'check_agent_venv', side_effect=AssertionError('host environment used')):
            # Stop at process launch, before running Docker or touching credentials.
            class Captured(Exception):
                pass
            with patch.object(o.subprocess, 'Popen', side_effect=Captured):
                with self.assertRaises(Captured):
                    o.run_agent('probe', o.sandbox('docker-env', {}), 'codex:gpt-6.1-sol', 'high')

    def test_literature_retries_only_failed_search(self):
        self.env['CODEX_BIN'] = '/nonexistent/codex'
        self.run_step('literature', success=False)
        searches = self.root / 'literature/searches'
        self.assertEqual([p.name for p in searches.glob('*.json')], ['claude-opus-5-5.json'])
        self.assertFalse((self.root / 'literature/candidates.json').exists())
        self.env['CODEX_BIN'] = str(self.root / 'tests/fake_codex.py')
        self.run_step('literature')
        rows = [json.loads(line) for line in (self.root / 'logs/costs.jsonl').read_text().splitlines()]
        successful = [r for r in rows if r['role'] == 'librarian' and r['failure'] is None]
        self.assertEqual([r['model'] for r in successful].count('claude-opus-5-5'), 1)
        self.assertEqual([r['model'] for r in successful].count('codex:gpt-6.1-sol'), 1)
        for record in (Path(self.env['RUNS_DIR']) / '_records').glob('*/invocation.json'):
            invocation = json.loads(record.read_text())
            self.assertFalse(any(name.startswith('literature/') for name in invocation['inputs']))

    def test_referees_reject_modified_inputs_for_both_backends(self):
        o = self.load_driver()
        actor = self.root / 'mutating_referee.py'
        verdict = {'verdict': 'pass', 'severity': 'none', 'location': '', 'objection': '', 'other_issues': []}
        actor.write_text('import json, pathlib, sys\n'
                         'pathlib.Path(sys.argv[1]).write_text("Changed input\\n")\n'
                         f'verdict = {verdict!r}\n'
                         'if sys.argv[2] == "claude":\n'
                         ' print(json.dumps({"type":"result","subtype":"success","structured_output":verdict}))\n'
                         'else:\n'
                         ' print(json.dumps({"type":"item.completed","item":{"type":"agent_message","text":json.dumps(verdict)}}))\n'
                         ' print(json.dumps({"type":"turn.completed","usage":{}}))\n')
        sources = {}
        for name in ('proof.md', 'statement.md', 'deps/P1.md', 'papers/source.txt'):
            source = self.root / ('original-' + name.replace('/', '-'))
            source.write_text('Original input\n')
            sources[name] = source
        for kind, model in (('claude', 'sonnet'), ('codex', 'codex:gpt-6.1-sol')):
            for filename in sources:
                with self.subTest(backend=kind, input=filename):
                    o.CLAUDE = o.CODEX = sys.executable
                    cmd = lambda *args, **kw: [sys.executable, str(actor), filename, kind]
                    o.build_cmd = o.build_codex_cmd = cmd
                    wd = o.sandbox('mutating-referee', sources)
                    with self.assertRaisesRegex(RuntimeError, 'referee modified review inputs'):
                        o.run_agent('referee', wd, model, 'high', schema='verdict')
                    row = json.loads((self.root / 'logs/costs.jsonl').read_text().splitlines()[-1])
                    self.assertIn(filename, row['failure'])

    def test_changed_referee_copy_never_approves_original_proof(self):
        self.ready()
        o = self.load_driver()
        def fake_agent(role, workdir, *args, **kwargs):
            if role == 'prover':
                (workdir / 'proof.md').write_text('GAP: original unrepaired proof\n')
                return {'result': 'done'}
            (workdir / 'proof.md').write_text('A repaired proof\n')
            return {'structured_output': {'verdict': 'pass', 'severity': 'none',
                                         'location': '', 'objection': '', 'other_issues': []}}
        o.run_agent = fake_agent
        with self.assertRaisesRegex(ValueError, 'referee modified review inputs'):
            o.prove_one('P1')
        self.assertNotEqual(o.status('P1')['state'], 'passed')
        self.assertEqual((self.root / 'props/P1/proof-v1.md').read_text(), 'GAP: original unrepaired proof\n')
        self.assertFalse(list((self.root / 'props/P1').glob('review-v*.json')))

    def test_docker_output_mount_links_fail_before_response_read(self):
        o = self.load_driver()
        o.CFG['isolation']['mode'] = 'docker'
        external = Path(self.temp.name) / 'outside-host-file.json'
        external.write_text(json.dumps({'items': [], 'notes': 'OUTSIDE_HOST_CONTENT'}))
        for location in ('final-file', 'output-directory', 'nested-directory'):
            with self.subTest(link=location):
                wd = o.sandbox('docker-output-link', {})
                record = o.RUNS / '_records' / wd.name
                outputs = record / 'outputs'
                actor = self.root / 'output_link_cli.py'
                actor.write_text('import json\nfrom pathlib import Path\n'
                                 f'p=Path({str(outputs)!r})\n'
                                 f'target=Path({str(external)!r})\n'
                                 + ('p.symlink_to(target.parent, target_is_directory=True)\n' if location == 'output-directory'
                                    else 'p.mkdir(parents=True)\n' + (
                                        '(p/"_last.txt").symlink_to(target)\n' if location == 'final-file'
                                        else '(p/"nested").symlink_to(target.parent, target_is_directory=True)\n'))
                                 + 'print(json.dumps({"type":"item.completed","item":{"type":"agent_message","text":"{\\"items\\":[],\\"notes\\":\\"real output\\"}"}}))\n'
                                 + 'print(json.dumps({"type":"turn.completed","usage":{}}))\n')
                original_popen = o.subprocess.Popen
                def fake_container(cmd, **kwargs):
                    if len(cmd) > 1 and str(cmd[1]).endswith('docker_runner.py'):
                        return original_popen([sys.executable, str(actor)], **kwargs)
                    return original_popen(cmd, **kwargs)
                with patch.object(o.subprocess, 'Popen', side_effect=fake_container), \
                     patch.object(o, 'read_text_nofollow', side_effect=AssertionError('unsafe output read')):
                    with self.assertRaisesRegex(RuntimeError, 'symlinks'):
                        o.run_agent('librarian', wd, 'codex:gpt-6.1-sol', 'high', schema='literature')
                outcome = json.loads((record / 'outcome.json').read_text())
                self.assertIsNotNone(outcome['failure'])
                self.assertNotIn('OUTSIDE_HOST_CONTENT', json.dumps(outcome))

    def test_final_response_reader_rejects_links_and_special_files(self):
        o = self.load_driver()
        stream = json.dumps({'type': 'turn.completed', 'usage': {}})
        external = Path(self.temp.name) / 'outside.json'
        external.write_text('{"items":[],"notes":"outside"}')
        for target in (external, external.with_name('missing.json')):
            wd = o.sandbox('linked-final', {})
            (wd / '_last.txt').symlink_to(target)
            with self.assertRaisesRegex(ValueError, 'unsafe final response'):
                o.parse_codex(stream, wd, 'literature')
        wd = o.sandbox('linked-output-parent', {})
        record = o.RUNS / '_records' / wd.name
        record.mkdir(parents=True)
        (record / 'outputs').symlink_to(external.parent, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'unsafe final response'):
            o.parse_codex(stream, wd, 'literature')
        wd = o.sandbox('fifo-final', {})
        os.mkfifo(wd / '_last.txt')
        with self.assertRaisesRegex(ValueError, 'regular file'):
            o.parse_codex(stream, wd, 'literature')
        wd = o.sandbox('regular-docker-final', {})
        outputs = o.RUNS / '_records' / wd.name / 'outputs'
        outputs.mkdir(parents=True)
        (outputs / '_last.txt').write_text('{"items":[],"notes":"regular output"}')
        self.assertEqual(o.parse_codex(stream, wd, 'literature')['structured_output']['notes'], 'regular output')

    def test_accepting_numerics_publishes_clean_complete_snapshots(self):
        self.run_step('numerics')
        first, second = sorted((self.root / 'numerics/candidates').iterdir())
        (first / 'old_helper.py').write_text('VALUE = 1\n')
        (second / 'compute.py').write_text('import importlib.util\nprint(importlib.util.find_spec("old_helper") is not None)\n')
        self.run_step('numerics', '--accept', first.name)
        old_selection = self.selected_numerics()
        self.assertTrue((old_selection / 'old_helper.py').exists())
        self.run_step('numerics', '--accept', second.name)
        selection = self.selected_numerics()
        self.assertNotEqual(selection, old_selection)
        self.assertFalse((selection / 'old_helper.py').exists())
        self.assertTrue((old_selection / 'old_helper.py').exists(), 'previous snapshot retained for audit')
        p = subprocess.run([sys.executable, str(selection / 'compute.py')], cwd=selection,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True, check=True)
        self.assertEqual(p.stdout.strip(), 'False')
        self.run_step('plan', '--single')
        # An extra importable file must invalidate acceptance even if all recorded files match.
        (selection / 'unrecorded_helper.py').write_text('VALUE = 2\n')
        self.assertIn('artifacts changed', self.run_step('plan', '--single', success=False).stderr)

    def test_failed_acceptance_keeps_previous_numerical_selection(self):
        self.run_step('numerics')
        first, second = sorted((self.root / 'numerics/candidates').iterdir())
        self.run_step('numerics', '--accept', first.name)
        original = (self.root / 'numerics/accepted.json').read_bytes()
        selection = self.selected_numerics()
        o = self.load_driver()
        real_copy = o.shutil.copy
        def broken_copy(src, dest):
            if Path(src).name == 'compute.py':
                raise OSError('simulated copy failure')
            return real_copy(src, dest)
        for operation in ('copy', 'publish'):
            with self.subTest(failure=operation):
                target, name, failure = ((o.shutil, 'copy', broken_copy) if operation == 'copy'
                                         else (o.os, 'replace', OSError('simulated publish failure')))
                with patch.object(target, name, side_effect=failure):
                    with self.assertRaises(OSError):
                        o.cmd_numerics(argparse.Namespace(accept=second.name))
                self.assertEqual((self.root / 'numerics/accepted.json').read_bytes(), original)
                self.assertEqual(self.selected_numerics(), selection)
                self.assertEqual(list((self.root / 'numerics/accepted').iterdir()), [selection])
                self.assertFalse(list((self.root / 'numerics').glob('.acceptance-*')))
        self.run_step('plan', '--single')

    def test_legacy_numerical_acceptance_requires_migration_without_breaking_status(self):
        self.ready()
        self.finish_two_props()
        self.run_step('integrate')
        selected = self.selected_numerics()
        manifest = self.root / 'numerics/accepted.json'
        acceptance = json.loads(manifest.read_text())
        acceptance.pop('snapshot')
        shutil.copy(selected / 'results.json', self.root / 'numerics/results.json')
        manifest.write_text(json.dumps(acceptance))
        self.run_step('status')
        self.assertTrue((self.root / 'report/STALE').exists())
        self.assertIn('clean snapshot', self.run_step('plan', '--single', success=False).stderr)
        self.run_step('numerics', '--accept', acceptance['candidate'])
        self.assertNotEqual(self.selected_numerics(), selected)
        self.run_step('integrate')

    def test_response_path_swap_cannot_escape_no_follow_reader(self):
        o = self.load_driver()
        external = Path(self.temp.name) / 'host-response.json'
        external.write_text('{"items":[],"notes":"outside"}')
        wd = o.sandbox('swapped-final', {})
        final = wd / '_last.txt'
        final.write_text('{"items":[],"notes":"model output"}')
        original_open = os.open
        swapped = False
        def replace_before_open(path, flags, *args, **kwargs):
            nonlocal swapped
            if path == '_last.txt' and not swapped:
                final.unlink()
                final.symlink_to(external)
                swapped = True
            return original_open(path, flags, *args, **kwargs)
        with patch.object(os, 'open', side_effect=replace_before_open):
            with self.assertRaisesRegex(ValueError, 'unsafe final response'):
                o.parse_codex('{"type":"turn.completed","usage":{}}', wd, 'literature')
        self.assertTrue(swapped)


if __name__ == '__main__':
    unittest.main()
