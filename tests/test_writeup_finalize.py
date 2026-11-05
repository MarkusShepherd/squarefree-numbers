"""Offline write-up regressions; Git mutations use isolated temporary repos."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from harness_support import digest, input_hashes
from writeup_finalize import accept_round, finalize, verify_acceptance, verify_finalization


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


class FinalizationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='sqf-finalize-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        self.source = self.root / 'archive/test'
        save(self.source / 'plan.json', {'main_theorem': 'Fixture theorem'})
        save(self.source / 'numerics/snapshot/results.json', {'counts': [1, 2, 3]})
        self.base = self.root / 'writeups/test'
        self.round = self.base / 'round-4'
        self.manuscript = self.round / 'manuscript'
        self.manuscript.mkdir(parents=True)
        (self.manuscript / 'main.pdf').write_bytes(b'%PDF-1.4\naccepted fixture\n')
        (self.manuscript / 'main.tex').write_text('Fixture source.\n')
        (self.manuscript / 'numbers.out').write_text('Recomputed fixture numbers.\n')
        save(self.manuscript / 'reproduction.json', {'artifacts': ['numbers.out']})
        save(self.manuscript / 'build-inputs.json', {
            'accepted_snapshot': digest(self.source / 'numerics/snapshot'),
            'pdf': digest(self.manuscript / 'main.pdf'),
            'artifacts': {'numbers.out': digest(self.manuscript / 'numbers.out')}})
        self.writer = 'writeup-writer-test-r5-20260101-000000-000000'
        self.refs = [f'writeup-referee-test-r4-{i}-20260101-000000-000000' for i in range(2)]
        self.models = ['claude-opus-5-5', 'codex:gpt-6.1-sol']
        referees = []
        for index, model in enumerate(self.models):
            path = self.round / 'reviews' / f'{index}.json'
            save(path, {'run': self.refs[index], 'model': model,
                        'manuscript_hash': digest(self.manuscript),
                        'review': {'verdict': 'revise', 'issues': ['Fixture owner override.']}})
            referees.append({'file': f'round-4/reviews/{index}.json', 'sha256': digest(path),
                             'model': model, 'verdict': 'revise'})
        save(self.base / 'state.json', {'round': 5, 'stage': 'writing', 'writer_run': self.writer})
        (self.base / 'STALE').write_text('Historical incomplete machine checkpoint.\n')
        save(self.base / 'inputs.json', {'sources': {'archive': digest(self.source)}})
        self.bundle = self.base / 'accepted'
        shutil.copytree(self.round, self.bundle)
        shutil.copy2(self.base / 'inputs.json', self.bundle / 'inputs.json')
        shutil.copytree(self.source, self.bundle / 'source')
        save(self.bundle / 'provenance.json', {'archive_label': 'test'})
        save(self.bundle / 'bibliography-candidates.json', [])
        save(self.bundle / 'usage.json', [
            {'run': self.writer, 'role': 'writer'},
            *[{'run': name, 'role': 'writeup_referee'} for name in self.refs]])
        save(self.bundle / 'manifest.json', {'algorithm': 'sha256', 'files': input_hashes(self.bundle)})
        save(self.base / 'acceptance.json', {
            'decision': 'accepted_by_human', 'accepted_by': 'Markus', 'archive_label': 'test',
            'accepted_round': 4, 'source_revision': 'round-4', 'source_revision_hash': digest(self.round),
            'accepted_bundle': 'accepted', 'accepted_bundle_hash': digest(self.bundle),
            'manifest': 'accepted/manifest.json', 'manifest_sha256': digest(self.bundle / 'manifest.json'),
            'manuscript_hash': digest(self.manuscript), 'pdf': 'accepted/manuscript/main.pdf',
            'pdf_sha256': digest(self.manuscript / 'main.pdf'),
            'input_bindings_sha256': digest(self.base / 'inputs.json'), 'referee_records': referees})
        self.runs = Path(self.temp.name) / 'external-runs'
        for name in [self.writer] + self.refs:
            record = self.runs / '_records' / name
            record.mkdir(parents=True)
            (record / '_stream.jsonl').write_text('{"type":"fixture"}\n')
            (record / '_stderr.txt').write_text('')
            inputs = {'source/plan.json': digest(self.bundle / 'source/plan.json')}
            if name in self.refs:
                context = self.runs / name
                shutil.copytree(self.source, context / 'source')
                for item in ('provenance.json', 'bibliography-candidates.json'):
                    shutil.copy2(self.bundle / item, context / item)
                inputs.update(input_hashes(context))
                inputs.update({f'manuscript/{p}': h for p, h in input_hashes(self.manuscript).items()})
            save(record / 'invocation.json', {
                'role': 'writer' if name == self.writer else 'writeup_referee',
                'model': self.models[self.refs.index(name)] if name in self.refs else 'fixture-model',
                'inputs': inputs})
            save(record / 'outcome.json', {
                'failure': 'exited 1' if name == self.writer else None,
                'outputs': {p: digest(record / p) for p in ('_stream.jsonl', '_stderr.txt')},
                'provider_outputs': {}})
        log = self.root / 'logs/interventions.md'
        log.parent.mkdir()
        log.write_text('Recorded owner decision.\n')
        (log.parent / 'costs.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in load_usage(self.bundle)))
        self.messages = []
        self.driver = SimpleNamespace(ROOT=self.root, RUNS=self.runs, log=self.messages.append)
        env = patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop('RUNS_DIR', None)

    def remove_fixture_acceptance(self):
        (self.base / 'acceptance.json').unlink()
        shutil.rmtree(self.bundle)

    def test_explicit_acceptance_creates_package_without_changing_revision_or_verdicts(self):
        self.remove_fixture_acceptance()
        before = {name: digest(self.base / name) for name in ('round-4', 'state.json', 'STALE')}
        accept_round(self.driver, 'test', 4, 'Markus', 'Accept as presented; overrule remaining comments.')
        _, decision, bundle = verify_acceptance(self.root, 'test')
        self.assertEqual(decision['accepted_round'], 4)
        self.assertEqual(decision['accepted_by'], 'Markus')
        self.assertEqual(decision['reason'], 'Accept as presented; overrule remaining comments.')
        for name, value in before.items():
            self.assertEqual(digest(self.base / name), value)
        for index in (0, 1):
            original = self.round / 'reviews' / f'{index}.json'
            copied = bundle / 'reviews' / f'{index}.json'
            self.assertEqual(original.read_bytes(), copied.read_bytes())
            self.assertEqual(json.loads(copied.read_text())['review']['verdict'], 'revise')
        self.assertEqual(digest(bundle / 'source'), digest(self.source))
        self.assertIn('Markus | write-up acceptance', (self.root / 'logs/interventions.md').read_text())
        finalize(self.driver, 'test')
        verify_finalization(self.root, 'test')

    def test_acceptance_retry_preserves_existing_decision(self):
        before = input_hashes(self.base)
        accept_round(self.driver, 'test', 4, 'Markus', 'Additional explanation must not rewrite history.')
        self.assertEqual(input_hashes(self.base), before)
        with self.assertRaisesRegex(ValueError, 'different round or owner'):
            accept_round(self.driver, 'test', 3, 'Markus')
        with self.assertRaisesRegex(ValueError, 'different round or owner'):
            accept_round(self.driver, 'test', 4, 'Someone else')

    def test_acceptance_requires_complete_unchanged_round(self):
        self.remove_fixture_acceptance()
        (self.manuscript / 'main.pdf').write_bytes(b'%PDF-tampered')
        with self.assertRaisesRegex(ValueError, 'integrity check failed'):
            accept_round(self.driver, 'test', 4, 'Markus')
        self.assertFalse((self.base / 'acceptance.json').exists())
        self.assertFalse(self.bundle.exists())

    def test_acceptance_requires_both_reports(self):
        self.remove_fixture_acceptance()
        (self.round / 'reviews/1.json').unlink()
        with self.assertRaisesRegex(ValueError, 'both independent reviewer reports'):
            accept_round(self.driver, 'test', 4, 'Markus')
        self.assertFalse((self.base / 'acceptance.json').exists())

    def test_acceptance_rejects_changed_context_and_incomplete_invocation(self):
        self.remove_fixture_acceptance()
        source = self.runs / self.refs[0] / 'source/plan.json'
        source.write_text('changed source')
        with self.assertRaisesRegex(ValueError, 'integrity check failed'):
            accept_round(self.driver, 'test', 4, 'Markus')
        shutil.copy2(self.source / 'plan.json', source)
        record = self.runs / '_records' / self.refs[0] / 'outcome.json'
        value = json.loads(record.read_text())
        value['failure'] = 'exited 1'
        save(record, value)
        with self.assertRaisesRegex(ValueError, 'completed, attributable'):
            accept_round(self.driver, 'test', 4, 'Markus')
        self.assertFalse((self.base / 'acceptance.json').exists())

    def test_acceptance_rejects_conflicting_existing_bundle(self):
        (self.base / 'acceptance.json').unlink()
        (self.bundle / 'keep.txt').write_text('Do not overwrite.')
        with self.assertRaisesRegex(ValueError, 'refusing to overwrite'):
            accept_round(self.driver, 'test', 4, 'Markus')
        self.assertEqual((self.bundle / 'keep.txt').read_text(), 'Do not overwrite.')
        self.assertFalse((self.base / 'acceptance.json').exists())

    def test_acceptance_copies_supplied_inputs_and_excludes_referee_scratch(self):
        self.remove_fixture_acceptance()
        (self.runs / self.refs[0] / 'source/scratch.txt').write_text('Referee scratch work.\n')
        accept_round(self.driver, 'test', 4, 'Markus')
        _, _, bundle = verify_acceptance(self.root, 'test')
        self.assertFalse((bundle / 'source/scratch.txt').exists())
        self.assertEqual(digest(bundle / 'source'), digest(self.source))

    def test_acceptance_does_not_count_one_review_session_twice(self):
        self.remove_fixture_acceptance()
        path = self.round / 'reviews/1.json'
        review = json.loads(path.read_text())
        review.update(run=self.refs[0], model=self.models[0])
        save(path, review)
        with self.assertRaisesRegex(ValueError, 'two independent review invocations'):
            accept_round(self.driver, 'test', 4, 'Markus')
        self.assertFalse((self.base / 'acceptance.json').exists())

    def test_finalize_preserves_failed_attempts_and_owner_override(self):
        before = {name: digest(self.base / name) for name in ('accepted', 'round-4', 'state.json', 'STALE', 'acceptance.json')}
        finalize(self.driver, 'test')
        _, record, audit = verify_finalization(self.root, 'test')
        self.assertEqual(len(audit['runs']), 3)
        self.assertEqual(audit['runs'][self.writer]['failure'], 'exited 1')
        self.assertEqual(digest(self.base / 'run-records'), digest(self.runs / '_records'))
        self.assertEqual((self.base / 'operator-interventions.md').read_text(), 'Recorded owner decision.\n')
        self.assertEqual(record['accepted_round'], 4)
        for name, value in before.items():
            self.assertEqual(digest(self.base / name), value)
        self.assertFalse((self.runs / '_owner.json').exists())
        self.assertFalse((self.root / 'runs').exists())

    def test_rerun_is_idempotent_and_verification_needs_no_external_runs(self):
        finalize(self.driver, 'test')
        before = input_hashes(self.base)
        shutil.rmtree(self.runs)
        (self.root / 'logs/interventions.md').write_text('Later operator activity.\n')
        finalize(self.driver, 'test')
        verify_finalization(self.root, 'test')
        self.assertEqual(input_hashes(self.base), before)

    def test_tampered_accepted_output_is_rejected_before_copying(self):
        (self.bundle / 'manuscript/numbers.out').write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'integrity check failed'):
            finalize(self.driver, 'test')
        self.assertFalse((self.base / 'run-records').exists())

    def test_changed_source_revision_or_review_is_rejected(self):
        (self.round / 'reviews/0.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'integrity check failed'):
            verify_acceptance(self.root, 'test')

    def test_missing_or_running_invocation_is_rejected(self):
        (self.runs / '_records' / self.writer / 'outcome.json').unlink()
        with self.assertRaisesRegex(ValueError, 'incomplete or still running'):
            finalize(self.driver, 'test')
        self.assertFalse((self.base / 'finalization.json').exists())
        self.assertFalse((self.base / 'run-records').exists())

    def test_tampered_transcript_is_rejected(self):
        (self.runs / '_records' / self.writer / '_stream.jsonl').write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'integrity check failed'):
            finalize(self.driver, 'test')

    def test_unrelated_invocations_are_not_copied(self):
        (self.runs / '_records/writeup-writer-other-r1-123').mkdir()
        finalize(self.driver, 'test')
        self.assertEqual(len(list((self.base / 'run-records').iterdir())), 3)

    def test_existing_conflicting_audit_is_not_overwritten(self):
        target = self.base / 'run-records/keep.txt'
        target.parent.mkdir()
        target.write_text('existing audit')
        with self.assertRaisesRegex(ValueError, 'without overwriting'):
            finalize(self.driver, 'test')
        self.assertEqual(target.read_text(), 'existing audit')
        self.assertFalse((self.base / 'finalization.json').exists())

    def test_matching_manual_copy_can_be_finalized(self):
        shutil.copytree(self.runs / '_records', self.base / 'run-records')
        finalize(self.driver, 'test')
        verify_finalization(self.root, 'test')

    def test_archived_transcript_corruption_is_detected(self):
        finalize(self.driver, 'test')
        (self.base / 'run-records' / self.writer / '_stream.jsonl').write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'audit files changed'):
            verify_finalization(self.root, 'test')

    def test_traversal_and_symlinks_are_rejected(self):
        path = self.base / 'acceptance.json'
        record = json.loads(path.read_text())
        record['accepted_bundle'] = '../outside'
        save(path, record)
        with self.assertRaisesRegex(ValueError, 'unsafe artifact path'):
            verify_acceptance(self.root, 'test')
        record['accepted_bundle'] = 'accepted'
        save(path, record)
        link = self.runs / '_records' / self.writer / 'outside'
        link.symlink_to(self.root)
        with self.assertRaisesRegex(ValueError, 'symlinks or special files'):
            finalize(self.driver, 'test')

    def test_run_directory_is_discovered_from_existing_runs_link(self):
        self.driver.RUNS = Path(self.temp.name) / 'wrong-default'
        (self.root / 'runs').symlink_to(self.runs, target_is_directory=True)
        finalize(self.driver, 'test')
        self.assertEqual((self.root / 'runs').resolve(), self.runs.resolve())

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, stderr=subprocess.PIPE)

    def test_static_ignore_and_plain_git_add_make_a_self_contained_package(self):
        finalize(self.driver, 'test')
        shutil.copy2(SOURCE / '.gitignore', self.root / '.gitignore')
        shutil.copy2(SOURCE / 'writeups/.gitignore', self.root / 'writeups/.gitignore')
        (self.base / 'round-1').mkdir()
        (self.base / 'round-1/scratch.txt').write_text('Unaccepted draft\n')
        (self.base / 'scratch.txt').write_text('Working output\n')
        self.git('init', '-q')
        self.git('add', 'writeups/')
        names = set(self.git('ls-files', '-z').decode().split('\0')) - {''}
        expected = {'writeups/.gitignore', 'writeups/test/acceptance.json',
                    'writeups/test/finalization.json', 'writeups/test/operator-interventions.md'}
        for directory in ('accepted', 'run-records'):
            expected.update(f'writeups/test/{directory}/{name}'
                            for name in input_hashes(self.base / directory))
        self.assertEqual(names, expected)
        clean = Path(self.temp.name) / 'clean'
        clean.mkdir()
        self.git('checkout-index', '--all', f'--prefix={clean}/')
        shutil.rmtree(self.runs)
        verify_finalization(clean, 'test')
        # Repeated finalization also works without round directories, root
        # inputs/state, archive, paper PDFs or external provider workspaces.
        finalize(SimpleNamespace(ROOT=clean, log=lambda _: None), 'test')

    def test_finalized_verification_still_rejects_corrupt_packaged_inputs(self):
        finalize(self.driver, 'test')
        shutil.rmtree(self.round)
        (self.base / 'inputs.json').unlink()
        verify_finalization(self.root, 'test')
        (self.bundle / 'inputs.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'integrity check failed'):
            verify_finalization(self.root, 'test')

    def prepare_cli(self):
        for name in ('orchestrate.py', 'harness_support.py', 'writeup_support.py', 'writeup_finalize.py', 'config.json'):
            shutil.copy2(SOURCE / name, self.root / name)
        shutil.copytree(SOURCE / 'prompts', self.root / 'prompts')
        return dict(os.environ, RUNS_DIR=str(self.runs), AGENT_VENV=str(self.root / 'missing-venv'),
                    CLAUDE_BIN='/nonexistent/claude', CODEX_BIN='/nonexistent/codex')

    def cli(self, env, *args):
        return subprocess.run([sys.executable, str(self.root / 'orchestrate.py'), 'writeup', 'test', *args],
                              cwd=self.root, env=env, text=True, capture_output=True, timeout=10)

    def test_cli_offline_finalize_and_verify_and_acceptance_closes_loop(self):
        env = self.prepare_cli()
        result = self.cli(env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('revision loop closed', result.stdout)
        self.assertFalse((self.base / 'finalization.json').exists())
        result = self.cli(env, '--finalize')
        self.assertEqual(result.returncode, 0, result.stderr)
        shutil.rmtree(self.runs)
        result = self.cli(env, '--verify')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('3 preserved invocation records verified', result.stdout)
        shutil.rmtree(self.round)
        (self.base / 'inputs.json').unlink()
        result = self.cli(env, '--accept-round', '4', '--accepted-by', 'Markus')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('verified; unchanged', result.stdout)
        result = self.cli(env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('revision loop closed', result.stdout)
        for name in ('runs', 'plans', 'papers'):
            self.assertFalse((self.root / name).exists())

    def test_cli_modes_are_exclusive_and_unfinalized_verification_is_clear(self):
        env = self.prepare_cli()
        result = self.cli(env, '--finalize', '--verify')
        self.assertNotEqual(result.returncode, 0)
        result = self.cli(env, '--verify')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('use --finalize', result.stderr)

    def test_cli_accepts_explicit_owner_decision_without_provider_prerequisites(self):
        self.remove_fixture_acceptance()
        env = self.prepare_cli()
        result = self.cli(env, '--accept-round', '4')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--accepted-by', result.stderr)
        result = self.cli(env, '--accepted-by', 'Markus')
        self.assertNotEqual(result.returncode, 0)
        result = self.cli(env, '--accept-round', '4', '--accepted-by', 'Markus', '--reason', 'Owner accepts round 4.')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('round 4 accepted by Markus', result.stdout)
        _, record, _ = verify_acceptance(self.root, 'test')
        self.assertEqual(record['reason'], 'Owner accepts round 4.')
        result = self.cli(env, '--finalize')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.cli(env, '--verify')
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ('runs', 'plans', 'papers'):
            self.assertFalse((self.root / name).exists())


def load_usage(bundle):
    return json.loads((bundle / 'usage.json').read_text())
