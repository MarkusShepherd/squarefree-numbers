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
        for name in ('orchestrate.py', 'harness_support.py', 'config.json', 'problem.md', 'prompts', 'hints', 'tests', 'isolation'):
            src, target = SOURCE / name, self.root / name
            if src.is_dir():
                shutil.copytree(src, target, ignore=shutil.ignore_patterns('__pycache__'))
            else:
                shutil.copy2(src, target)
        self.env = dict(os.environ, RUNS_DIR=str(Path(self.temp.name) / 'runs'),
                        CLAUDE_BIN=str(self.root / 'tests/fake_claude.py'),
                        CODEX_BIN=str(self.root / 'tests/fake_codex.py'), BACKENDS='claude,codex')

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
                self.assertIn('dehnert' if backend != 'claude' else 'riemannhypothesis', leaks)
                self.run_step('archive', 'test')
                records = self.root / 'archive/test/runs/_records'
                invocation = json.loads(next(records.glob('*/invocation.json')).read_text())
                self.assertIn('sources', invocation)
                self.assertIn('prompt', invocation)
                self.assertIn('inputs', invocation)
                rows = [json.loads(s) for s in (self.root / 'logs/costs.jsonl').read_text().splitlines()]
                if backend != 'claude,codex':
                    self.assertTrue(all(r['backend'] == backend for r in rows))
                for name in ('logs', 'plans', 'numerics', 'props', 'report', 'archive'):
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


if __name__ == '__main__':
    unittest.main()
