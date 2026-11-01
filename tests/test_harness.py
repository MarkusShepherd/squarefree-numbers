import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
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
                self.assertEqual([r['status'] for r in candidates], ['downloaded', 'wishlist', 'rejected', 'rejected'])
                self.assertIn('after the 2010 cutoff', candidates[2]['note'])
                self.assertIn('blocked host gitlab.com', candidates[3]['note'])
                self.assertEqual(len(list((self.root / 'literature/pdf').glob('*.pdf'))), 1)
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
        (self.root / 'numerics/results.json').write_text('{}')
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
        self.assertTrue((self.root / 'numerics/src/helper.py').is_file())
        (self.root / 'numerics/compute.py').write_text('# modified implementation\n')
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


if __name__ == '__main__':
    unittest.main()
