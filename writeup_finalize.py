"""Verify human acceptance and preserve write-up audit records without agents."""
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from datetime import datetime, timezone

from harness_support import digest, input_hashes, validate_artifact_tree, OS_METADATA


def load(path):
    return json.loads(path.read_text())


def within(root, name):
    if not isinstance(name, str):
        raise ValueError('artifact path must be a string')
    path = Path(name)
    if path.is_absolute() or not path.parts or '..' in path.parts:
        raise ValueError(f'unsafe artifact path: {name}')
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f'symlink artifact is not supported: {name}')
    return current


def match(path, expected):
    if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise ValueError(f'missing or invalid recorded hash for {path}')
    if digest(path) != expected:
        raise ValueError(f'write-up integrity check failed: {path}')


def writeup_root(root, label):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', label):
        raise ValueError('archive label must be a single safe directory name')
    return within(root, f'writeups/{label}')


def verify_acceptance(root, label):
    """Check the existing acceptance format, including unchanged revise verdicts."""
    try:
        return _verify_acceptance(root, label)
    except (KeyError, TypeError, IndexError) as exc:
        raise ValueError(f'invalid acceptance record for {label}: {exc}') from exc


def _verify_acceptance(root, label):
    base = writeup_root(root, label)
    validate_artifact_tree(base)
    record = load(base / 'acceptance.json')
    if record['decision'] != 'accepted_by_human' or not record['accepted_by'].strip():
        raise ValueError('finalization requires a recorded human acceptance')
    if record['archive_label'] != label:
        raise ValueError('acceptance names a different archive')
    rnd = record['accepted_round']
    if type(rnd) is not int or rnd < 1 or record['source_revision'] != f'round-{rnd}':
        raise ValueError('acceptance names an invalid revision')
    revision = within(base, record['source_revision'])
    bundle = within(base, record['accepted_bundle'])
    manifest_path = within(base, record['manifest'])
    if manifest_path != bundle / 'manifest.json':
        raise ValueError('acceptance manifest must belong to the accepted bundle')
    match(revision, record['source_revision_hash'])
    match(bundle, record['accepted_bundle_hash'])
    match(manifest_path, record['manifest_sha256'])
    manifest = load(manifest_path)
    if manifest['algorithm'] != 'sha256':
        raise ValueError('unsupported accepted-manifest hash algorithm')
    for name in manifest['files']:
        within(bundle, name)
    expected = dict(manifest['files'])
    if 'manifest.json' in expected:
        raise ValueError('accepted manifest cannot hash itself')
    expected['manifest.json'] = record['manifest_sha256']
    if input_hashes(bundle) != expected:
        raise ValueError('accepted bundle file inventory differs from its manifest')
    match(bundle / 'manuscript', record['manuscript_hash'])
    match(revision / 'manuscript', record['manuscript_hash'])
    pdf = within(base, record['pdf'])
    if pdf != bundle / 'manuscript/main.pdf':
        raise ValueError('accepted PDF must belong to the accepted manuscript')
    match(pdf, record['pdf_sha256'])
    match(base / 'inputs.json', record['input_bindings_sha256'])
    match(bundle / 'inputs.json', record['input_bindings_sha256'])
    build = load(bundle / 'manuscript/build-inputs.json')
    match(pdf, build['pdf'])
    reproduction = load(bundle / 'manuscript/reproduction.json')
    if not build['artifacts'] or set(build['artifacts']) != set(reproduction['artifacts']):
        raise ValueError('numerical artifact inventories disagree')
    for name, expected_hash in build['artifacts'].items():
        match(within(bundle / 'manuscript', name), expected_hash)
    if len(record['referee_records']) != 2:
        raise ValueError('acceptance must preserve two independent referee records')
    names, review_runs = set(), set()
    for referee in record['referee_records']:
        path = within(base, referee['file'])
        if path.parent != revision / 'reviews' or path.name in names:
            raise ValueError('acceptance names invalid referee records')
        names.add(path.name)
        match(path, referee['sha256'])
        match(bundle / 'reviews' / path.name, referee['sha256'])
        review = load(path)
        if review['run'] in review_runs:
            raise ValueError('acceptance must preserve two independent review invocations')
        review_runs.add(review['run'])
        if (review['model'] != referee['model'] or review['review']['verdict'] != referee['verdict']
                or review['manuscript_hash'] != record['manuscript_hash']):
            raise ValueError('referee attribution, verdict or reviewed manuscript changed')
    return base, record, bundle


def verify_finalization(root, label, require_audit=True):
    base, record, bundle = verify_acceptance(root, label)
    path = base / 'finalization.json'
    if not path.exists():
        if require_audit:
            raise ValueError(f'{label}: accepted bundle verified, but audit is not finalized; use --finalize')
        return base, record, None
    try:
        final = load(path)
        match(base / 'acceptance.json', final['acceptance_sha256'])
        if final['accepted_bundle_hash'] != record['accepted_bundle_hash']:
            raise ValueError('finalization binds a different accepted bundle')
        records = within(base, 'run-records')
        validate_artifact_tree(records)
        actual = {f'run-records/{name}': value for name, value in input_hashes(records).items()}
        if final['operator_interventions'] is not None:
            log_path = within(base, final['operator_interventions'])
            actual[str(log_path.relative_to(base))] = digest(log_path)
        for name in final['files']:
            within(base, name)
        if actual != final['files']:
            raise ValueError('preserved audit files changed or are incomplete')
        if sorted(p.name for p in records.iterdir()) != sorted(final['runs']):
            raise ValueError('preserved invocation inventory changed')
        for name in final['runs']:
            if verify_record(records / name, label, bundle) != final['runs'][name]:
                raise ValueError('preserved invocation summary differs from its records')
        return base, record, final
    except (KeyError, TypeError, IndexError) as exc:
        raise ValueError(f'invalid finalization record for {label}: {exc}') from exc


def run_name(name, label):
    return (isinstance(name, str) and '/' not in name and '\\' not in name
            and any(name.startswith(f'writeup-{role}-{label}-r') for role in ('writer', 'referee')))


def verify_record(path, label, bundle):
    validate_artifact_tree(path)
    if not run_name(path.name, label):
        raise ValueError(f'unrelated write-up invocation: {path.name}')
    for name in ('invocation.json', 'outcome.json', '_stream.jsonl', '_stderr.txt'):
        if not (path / name).is_file():
            raise ValueError(f'invocation is incomplete or still running: {path.name}/{name}')
    try:
        invocation, outcome = load(path / 'invocation.json'), load(path / 'outcome.json')
        role = 'writer' if path.name.startswith('writeup-writer-') else 'writeup_referee'
        if invocation['role'] != role:
            raise ValueError(f'unexpected invocation role: {path.name}')
        match(bundle / 'source/plan.json', invocation['inputs']['source/plan.json'])
        for name in ('_stream.jsonl', '_stderr.txt'):
            match(path / name, outcome['outputs'][name])
        outputs = path / 'outputs'
        if outputs.exists():
            validate_artifact_tree(outputs)
        actual = input_hashes(outputs) if outputs.exists() else {}
        if actual != outcome['provider_outputs']:
            raise ValueError(f'provider output inventory changed: {path.name}')
        return {'role': role, 'model': invocation['model'], 'failure': outcome['failure']}
    except (KeyError, TypeError) as exc:
        raise ValueError(f'invalid invocation record {path.name}: {exc}') from exc


def expected_runs(base, bundle, label):
    names = set()
    usage = bundle / 'usage.json'
    if usage.exists():
        for row in load(usage):
            if row.get('role') in ('writer', 'writeup_referee'):
                names.add(row['run'])
    for path in base.glob('round-*/reviews/*.json'):
        names.add(load(path)['run'])
    state = base / 'state.json'
    if state.exists() and load(state).get('writer_run'):
        names.add(load(state)['writer_run'])
    if any(not run_name(name, label) for name in names):
        raise ValueError('write-up history references an unrelated invocation')
    return names


def runs_directory(driver):
    if os.environ.get('RUNS_DIR'):
        return Path(os.environ['RUNS_DIR']).expanduser().resolve()
    if (driver.ROOT / 'runs').exists():
        return (driver.ROOT / 'runs').resolve()
    return driver.RUNS


def accept_round(driver, label, rnd, owner, reason=None):
    """Record a deliberate owner decision, never inferred from model verdicts."""
    if type(rnd) is not int or rnd < 1 or not isinstance(owner, str) or not owner.strip():
        raise ValueError('acceptance requires a positive round number and the owner name')
    owner = owner.strip()
    base = writeup_root(driver.ROOT, label)
    validate_artifact_tree(base)
    if (base / 'acceptance.json').exists():
        _, record, _ = verify_acceptance(driver.ROOT, label)
        if record['accepted_round'] != rnd or record['accepted_by'] != owner:
            raise ValueError('an existing acceptance names a different round or owner; refusing to replace it')
        driver.log(f'{label}: existing acceptance of round {rnd} by {owner} verified; unchanged')
        return
    try:
        _accept_round(driver, label, rnd, owner, reason, base)
    except (KeyError, TypeError, IndexError) as exc:
        raise ValueError(f'incomplete round or review inputs for acceptance: {exc}') from exc


def _accept_round(driver, label, rnd, owner, reason, base):
    revision = within(base, f'round-{rnd}')
    validate_artifact_tree(revision)
    manuscript = revision / 'manuscript'
    manuscript_hash = digest(manuscript)
    build = load(manuscript / 'build-inputs.json')
    match(manuscript / 'main.pdf', build['pdf'])
    reproduction = load(manuscript / 'reproduction.json')
    if not build['artifacts'] or set(build['artifacts']) != set(reproduction['artifacts']):
        raise ValueError('numerical artifact inventories disagree')
    for name, expected in build['artifacts'].items():
        match(within(manuscript, name), expected)
    binding_hash = digest(base / 'inputs.json')
    binding = load(base / 'inputs.json')
    match(within(driver.ROOT, f'archive/{label}'), binding['sources']['archive'])
    records = runs_directory(driver) / '_records'
    validate_artifact_tree(records)
    paths = sorted((revision / 'reviews').glob('*.json'))
    if [p.name for p in paths] != ['0.json', '1.json']:
        raise ValueError('select a completed round with both independent reviewer reports')
    referees, context, context_hashes, review_runs = [], None, None, set()
    for path in paths:
        review = load(path)
        if review['manuscript_hash'] != manuscript_hash:
            raise ValueError('selected manuscript differs from the reviewed revision')
        if not run_name(review['run'], label) or not review['run'].startswith('writeup-referee-'):
            raise ValueError('review references an unrelated invocation')
        if review['run'] in review_runs:
            raise ValueError('acceptance requires two independent review invocations')
        review_runs.add(review['run'])
        record_path = within(records, review['run'])
        invocation = load(record_path / 'invocation.json')
        outcome = load(record_path / 'outcome.json')
        if (outcome['failure'] is not None or invocation['role'] != 'writeup_referee'
                or invocation['model'] != review['model']):
            raise ValueError('acceptance requires completed, attributable reviewer reports')
        workspace = within(runs_directory(driver), review['run'])
        # Preserve only supplied context, not referee scratch work or paper PDFs.
        validate_artifact_tree(workspace / 'source')
        for name, expected in invocation['inputs'].items():
            if name.startswith('source/') or name in ('provenance.json', 'bibliography-candidates.json'):
                match(within(workspace, name), expected)
            elif name.startswith('manuscript/'):
                match(within(revision, name), expected)
        for name in ('provenance.json', 'bibliography-candidates.json'):
            match(workspace / name, invocation['inputs'][name])
        supplied = {name: value for name, value in invocation['inputs'].items()
                    if name.startswith('source/') or name in ('provenance.json', 'bibliography-candidates.json')}
        if context_hashes is not None and supplied != context_hashes:
            raise ValueError('reviewers received different write-up source inputs')
        context, context_hashes = workspace, supplied
        referees.append({'file': str(path.relative_to(base)), 'sha256': digest(path),
                         'model': review['model'], 'verdict': review['review']['verdict'],
                         'issues': review['review'].get('issues', []),
                         'owner_disposition': f'Accepted as presented by {owner}, overriding remaining reviewer objections.'})
    original_hash = digest(revision)
    usage_path = driver.ROOT / 'logs/costs.jsonl'
    usage = [json.loads(line) for line in usage_path.read_text().splitlines() if line.strip()] if usage_path.exists() else []
    usage = [row for row in usage if run_name(row.get('run'), label)
             and row.get('role') in ('writer', 'writeup_referee')]
    with tempfile.TemporaryDirectory(prefix='.accepting-', dir=base) as temporary:
        temp = Path(temporary)
        bundle = temp / 'accepted'
        ignore = shutil.ignore_patterns(*OS_METADATA)
        shutil.copytree(revision, bundle, ignore=ignore)
        for name, expected in context_hashes.items():
            target = within(bundle, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(context / name, target)
            match(target, expected)
        shutil.copy2(base / 'inputs.json', bundle / 'inputs.json')
        (bundle / 'usage.json').write_text(json.dumps(usage, indent=2) + '\n')
        notes = bundle / 'ACCEPTANCE.md'
        if notes.exists():
            raise ValueError('selected revision already has ACCEPTANCE.md; refusing to overwrite it')
        notes.write_text(
            f'# Accepted write-up: {label}, round {rnd}\n\n'
            f'Accepted as presented by {owner}. The manuscript and referee verdicts are unchanged.\n'
            'The decision, optional reason and exact hashes are in ../acceptance.json.\n\n'
            'manuscript/ contains the PDF, LaTeX, numerical code, results and logs;\n'
            'reviews/ contains the original reports; source/ contains the supplied\n'
            'archived proof and numerical inputs. Original paper PDFs are not duplicated.\n'
            'provenance.json and inputs.json preserve the recorded provenance and bindings.\n'
            'usage.json contains the available invocation cost/token rows.\n'
            'manifest.json hashes all bundled files except itself.\n\n'
            'The original state.json and STALE outside this bundle remain historical\n'
            'automated checkpoints. Human acceptance is recorded separately.\n')
        validate_artifact_tree(bundle)
        match(bundle / 'manuscript', manuscript_hash)
        match(bundle / 'source/plan.json', digest(driver.ROOT / 'archive' / label / 'plan.json'))
        match(bundle / 'source/numerics/snapshot', build['accepted_snapshot'])
        for path in paths:
            verify_record(records / load(path)['run'], label, bundle)
        manifest = {'algorithm': 'sha256', 'files': input_hashes(bundle)}
        (bundle / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        match(revision, original_hash)
        match(base / 'inputs.json', binding_hash)
        target = base / 'accepted'
        if target.exists():
            if digest(target) != digest(bundle):
                raise ValueError('an existing accepted directory differs; refusing to overwrite it')
        else:
            bundle.rename(target)
        record = {'decision': 'accepted_by_human', 'accepted_by': owner,
                  'recorded_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                  'reason': reason, 'archive_label': label, 'accepted_round': rnd,
                  'source_revision': f'round-{rnd}', 'source_revision_hash': original_hash,
                  'accepted_bundle': 'accepted', 'accepted_bundle_hash': digest(target),
                  'manifest': 'accepted/manifest.json', 'manifest_sha256': digest(target / 'manifest.json'),
                  'manuscript_hash': manuscript_hash, 'pdf': 'accepted/manuscript/main.pdf',
                  'pdf_sha256': build['pdf'], 'input_bindings_sha256': binding_hash,
                  'referee_records': referees, 'revision_loop': 'closed_by_owner_acceptance',
                  'scope': 'Exact selected revision accepted as presented, including documented corrections and remaining referee objections. No model pass verdict is asserted.'}
        pending = temp / 'acceptance.json'
        pending.write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
        pending.rename(base / 'acceptance.json')
    verify_acceptance(driver.ROOT, label)
    log = driver.ROOT / 'logs/interventions.md'
    log.parent.mkdir(exist_ok=True)
    with log.open('a') as stream:
        stream.write(f'- {record["recorded_at_utc"]} | {owner} | write-up acceptance | '
                     f'Accepted {label} round {rnd} as presented; PDF SHA-256 {build["pdf"]}; '
                     f'referee verdicts unchanged. Reason: {json.dumps(reason, ensure_ascii=False)}\n')
    driver.log(f'{label}: round {rnd} accepted by {owner}; package and exact hashes recorded at {base / "acceptance.json"}')
    driver.log('revision loop closed; use --finalize to preserve the invocation audit')


def finalize(driver, label):
    base, record, bundle = verify_acceptance(driver.ROOT, label)
    if (base / 'finalization.json').exists():
        _, _, final = verify_finalization(driver.ROOT, label)
        driver.log(f'{label}: finalization verified; {len(final["runs"])} invocation records already preserved')
        return
    runs = runs_directory(driver)
    records = runs / '_records'
    if not records.is_dir():
        raise ValueError(f'write-up records not found at {records}; set RUNS_DIR to the write-up run directory')
    validate_artifact_tree(records)
    names = expected_runs(base, bundle, label)
    names.update(p.name for p in records.iterdir() if run_name(p.name, label))
    if not names:
        raise ValueError('no write-up invocation records found')
    driver.log(f'{label}: acceptance and numerical artifacts verified; preserving {len(names)} invocation records from {records}')
    summaries = {}
    for name in sorted(names):
        summaries[name] = verify_record(within(records, name), label, bundle)
    acceptance_hash = digest(base / 'acceptance.json')
    operator_log = driver.ROOT / 'logs/interventions.md'
    with tempfile.TemporaryDirectory(prefix='.finalizing-', dir=base) as temporary:
        temp = Path(temporary)
        staged = temp / 'run-records'
        staged.mkdir()
        for name in sorted(names):
            source = records / name
            before = input_hashes(source)
            shutil.copytree(source, staged / name)
            if input_hashes(source) != before or input_hashes(staged / name) != before:
                raise ValueError(f'invocation changed while being preserved: {name}')
        log_name = None
        if operator_log.is_file():
            if operator_log.is_symlink():
                raise ValueError('operator intervention log must not be a symlink')
            log_name = 'operator-interventions.md'
            before = digest(operator_log)
            shutil.copy2(operator_log, temp / log_name)
            if digest(operator_log) != before or digest(temp / log_name) != before:
                raise ValueError('operator log changed while being preserved')
        # Check all destinations before publishing; never overwrite existing audit data.
        for name in ('run-records', log_name):
            if name is not None and (base / name).exists() and digest(base / name) != digest(temp / name):
                raise ValueError(f'existing audit differs; preserved without overwriting: {base / name}')
        verify_acceptance(driver.ROOT, label)
        match(base / 'acceptance.json', acceptance_hash)
        hashes = {f'run-records/{name}': value for name, value in input_hashes(staged).items()}
        if log_name:
            hashes[log_name] = digest(temp / log_name)
        for name in ('run-records', log_name):
            if name is not None and not (base / name).exists():
                (temp / name).rename(base / name)
        final = {'finalized_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                 'acceptance_sha256': acceptance_hash, 'accepted_bundle_hash': record['accepted_bundle_hash'],
                 'source_runs_dir': str(runs), 'runs': summaries,
                 'operator_interventions': log_name, 'files': hashes}
        pending = temp / 'finalization.json'
        pending.write_text(json.dumps(final, indent=2) + '\n')
        pending.rename(base / 'finalization.json')
    verify_finalization(driver.ROOT, label)
    driver.log(f'{label}: finalized accepted round {record["accepted_round"]}; {len(names)} invocation records and transcripts verified')
    driver.log(f'preserved audit: {base / "run-records"}; verification record: {base / "finalization.json"}')
