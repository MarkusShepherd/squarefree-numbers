"""Archived-run manuscript pipeline. Never mutate or reapprove the source run."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

from harness_support import (digest, hash_json, input_hashes, validate_artifact_tree,
                             validate_verdict, verify_inputs, OS_METADATA)


OVERFULL_PT = 1.0
BUILD_FILES = ('.aux', '.toc', '.lof', '.lot', '.out', '.fls', '.fdb_latexmk', '.bbl', '.blg',
               '.bcf', '.run.xml', '.synctex.gz', '.nav', '.snm', '.xdv', '.dvi')


def read_json(path):
    return json.loads(path.read_text())


def save(path, value):
    """Atomically publish a checkpoint, retaining failures for a resumable retry."""
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(path)


def validate_review(value):
    if value['verdict'] == 'pass' and value['issues']:
        raise ValueError('passing write-up review has unresolved issues')
    if value['verdict'] != 'pass' and not value['issues']:
        raise ValueError('write-up rejection requires actionable issues')
    for name in ('summary', 'statement_checks', 'dependency_checks', 'numerics_checks',
                 'citation_checks', 'provenance_checks', 'layout_checks'):
        if not value.get(name, '').strip():
            raise ValueError(f'write-up review needs substantive {name}')


def safe_label(label):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', label):
        raise ValueError('archive label must be a single safe directory name')
    return label


def briefing_input(path):
    if path is None:
        return {}
    path = path.expanduser()
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'briefing must be a regular file: {path}')
    return {'brief.md': path}


def archive_sources(root, label, papers_dir=None):
    """Verify archived approvals using their original policy and corpus hashes.

    Archives omit PDFs and the root problem.md. Recover hashes/text from the
    external invocation records, never from the current experiment's state.
    """
    archive = root / 'archive' / safe_label(label)
    validate_artifact_tree(archive)
    cfg = read_json(archive / 'config.json')
    plan = read_json(archive / 'plan.json')
    props = plan['propositions']
    ids = [p['id'] for p in props]
    if not ids or len(set(ids)) != len(ids) or any(not re.fullmatch(r'P[0-9]+', p) for p in ids):
        raise ValueError('invalid archived proposition IDs')
    if set(ids) != {p.name for p in (archive / 'props').iterdir() if p.is_dir()}:
        raise ValueError('archived plan and propositions disagree')
    if (archive / 'report/STALE').exists():
        raise ValueError('archived integration is stale')
    integration = read_json(archive / 'report/integration.json')
    if not integration.get('composes') or not integration.get('reviews'):
        raise ValueError('archive has no successful independent integration')
    integrated = read_json(archive / 'report/inputs.json')
    for name, rel in [('props', 'props'), ('plan', 'plan.json'), ('accepted', 'numerics/accepted.json')]:
        if integrated[name] != digest(archive / rel):
            raise ValueError(f'archived integration inputs changed: {name}')
    acceptance = read_json(archive / 'numerics/accepted.json')
    rel = Path(acceptance.get('snapshot', ''))
    if len(rel.parts) != 2 or rel.parts[0] != 'accepted' or '..' in rel.parts:
        raise ValueError('archive needs an accepted numerical snapshot')
    snapshot = archive / 'numerics' / rel
    actual = input_hashes(snapshot)
    if not actual or actual != acceptance['artifacts'] or actual != integrated['numerical_artifacts']:
        raise ValueError('archived accepted numerical snapshot changed')
    if actual.get('results.json') != acceptance['results_hash'] or acceptance['problem_hash'] != integrated['problem']:
        raise ValueError('archived numerical acceptance disagrees with integration')

    files = {'source/plan.json': archive / 'plan.json',
             'source/numerics/accepted.json': archive / 'numerics/accepted.json',
             'source/numerics/snapshot': snapshot,
             'source/report': archive / 'report'}
    if (archive / 'logs/interventions.md').exists():
        files['source/interventions.md'] = archive / 'logs/interventions.md'
    selected = [p for p in (archive / 'plans').glob('*.json') if read_json(p) == plan]
    if len(selected) != 1 or not selected[0].with_suffix('.md').is_file():
        raise ValueError('cannot identify the selected archived plan')
    files['source/plan.md'] = selected[0].with_suffix('.md')

    records = []
    for path in sorted((archive / 'runs/_records').glob('*/invocation.json')):
        record = read_json(path)
        records.append((path, record))
    if not records:
        raise ValueError('archive has no invocation provenance')
    models = []
    for path, record in records:
        version = record.get('cli_version', 'unavailable')
        container = path.parent / 'outputs/_container-version.txt'
        if container.is_file():
            version = container.read_text().strip()
        row = {'role': record['role'], 'model': record['model'], 'cli_version': version,
               'revision': record.get('revision')}
        if row not in models:
            models.append(row)

    corpus, problem = None, None
    approved = {}
    contracts = {}
    refs_for = {}
    for prop in props:
        pid = prop['id']
        pdir = archive / 'props' / pid
        st, meta = read_json(pdir / 'status.json'), read_json(pdir / 'meta.json')
        rnd = st['round']
        if st['state'] != 'passed' or not st.get('approval_hash'):
            raise ValueError(f'{pid}: no current archived approval')
        if prop['depends_on'] != meta['depends_on']:
            raise ValueError(f'{pid}: dependency contracts disagree')
        proofs = sorted(pdir.glob('proof-v*.md'), key=lambda p: int(p.stem.split('-v')[1]))
        if not proofs or proofs[-1].name != f'proof-v{rnd}.md':
            raise ValueError(f'{pid}: approved proof is not the latest proof')
        proof = proofs[-1]
        if proof.read_text().startswith('STATEMENT DEFECT:'):
            raise ValueError(f'{pid}: a defect report is not a proof')
        review_paths = sorted(pdir.glob(f'review-v{rnd}-*.json'))
        if [p.name for p in review_paths] != [f'review-v{rnd}-0.json', f'review-v{rnd}-1.json']:
            raise ValueError(f'{pid}: need two archived passing referee reviews')
        reviews = [read_json(p) for p in review_paths]
        local_policy = None
        for i, review in enumerate(reviews):
            validate_verdict(review)
            if review['verdict'] != 'pass' or review['severity'] == 'defect-confirmed':
                raise ValueError(f'{pid}: nonpassing archived proof review')
            matches = []
            for path, record in records:
                if not path.parent.name.startswith(f'referee-{pid}-r{rnd}-{i}-'):
                    continue
                inputs = record['inputs']
                outcome_path = path.parent / 'outcome.json'
                if (record['role'] == 'referee' and record['model'] == review['model']
                        and inputs.get('proof.md') == digest(proof)
                        and inputs.get('statement.md') == digest(pdir / 'statement.md')
                        and outcome_path.is_file() and read_json(outcome_path)['failure'] is None):
                    matches.append((path, record))
            if not matches:
                raise ValueError(f'{pid}: missing successful input-integrity referee provenance')
            path, record = matches[-1]
            outcome = read_json(path.parent / 'outcome.json')
            if any(outcome['outputs'].get(k) != v for k, v in record['inputs'].items()):
                raise ValueError(f'{pid}: archived referee changed supplied inputs')
            inputs = record['inputs']
            papers = {k.removeprefix('papers/'): v for k, v in inputs.items() if k.startswith('papers/')}
            text = record['sources']['problem.md']
            if hashlib.sha256(text.encode()).hexdigest() != integrated['problem'] or inputs.get('problem.md') != integrated['problem']:
                raise ValueError(f'{pid}: archived problem provenance disagrees')
            if corpus is not None and (papers != corpus or text != problem):
                raise ValueError('archived referees used different corpus/problem inputs')
            corpus, problem = papers, text
            for dep in prop['depends_on']:
                if inputs.get(f'deps/{dep}.md') != digest(archive / 'props' / dep / 'statement.md'):
                    raise ValueError(f'{pid}: referee dependency input changed: {dep}')
            rp = {'input_integrity_version': 1, 'prompt': record['prompt'],
                  'schema': record['schema'], 'models': [r['model'] for r in reviews],
                  'effort': record['effort'], 'capabilities': record['capabilities'],
                  'exclusion': cfg['exclusion']}
            if local_policy is not None and rp != local_policy:
                raise ValueError(f'{pid}: archived referee policies disagree')
            local_policy = rp
        refs_for[pid] = (st, reviews, review_paths, local_policy, proof)
        files[f'source/props/{pid}/statement.md'] = pdir / 'statement.md'
        files[f'source/props/{pid}/proof.md'] = proof
        for path in review_paths:
            files[f'source/props/{pid}/{path.name}'] = path

    def contract(pid, seen=()):
        if pid in seen or pid not in refs_for:
            raise ValueError('invalid archived dependency graph')
        if pid not in contracts:
            pdir = archive / 'props' / pid
            meta = read_json(pdir / 'meta.json')
            contracts[pid] = hash_json({'statement': digest(pdir / 'statement.md'),
                'meta': digest(pdir / 'meta.json'),
                'dependencies': {d: contract(d, seen + (pid,)) for d in meta['depends_on']},
                'problem': integrated['problem'], 'papers': hash_json(corpus)})
        return contracts[pid]

    for pid, (st, reviews, paths, policy, proof) in refs_for.items():
        bound = contract(pid)
        for review in reviews:
            if review.get('contract_hash') != bound or review.get('proof_hash') != digest(proof):
                raise ValueError(f'{pid}: review no longer binds archived proof/contract')
        approval = hash_json({'contract': bound, 'proof': digest(proof), 'review_policy': policy,
                             'reviews': {p.name: digest(p) for p in paths}})
        if approval != st['approval_hash']:
            raise ValueError(f'{pid}: archived approval hash mismatch')
        approved[pid] = {'approval_hash': approval, 'contract_hash': bound, 'proof_hash': digest(proof)}

    for model, report in integration['reviews'].items():
        tag = model.replace(':', '-').replace('/', '-')
        if not report['composes'] or read_json(archive / 'report' / f'integration-{tag}.json') != report:
            raise ValueError('independent archived integration report disagrees with summary')
        if not (archive / 'report' / f'assembly-{tag}.md').is_file():
            raise ValueError('missing independent archived assembly')
        matches = []
        for path, record in records:
            if record['role'] != 'integrator' or record['model'] != model:
                continue
            inputs = record['inputs']
            outcome_path = path.parent / 'outcome.json'
            if not outcome_path.is_file():
                continue
            outcome = read_json(outcome_path)
            if outcome['failure'] is not None or inputs.get('plan.json') != integrated['plan']:
                continue
            if any(inputs.get(f'props/{pid}/proof.md') != approved[pid]['proof_hash']
                   or inputs.get(f'props/{pid}/statement.md') != digest(archive / 'props' / pid / 'statement.md')
                   for pid in ids):
                continue
            if outcome['outputs'].get('assembly.md') == digest(archive / 'report' / f'assembly-{tag}.md'):
                matches.append(path)
        if not matches:
            raise ValueError('archived assembly lacks matching successful integration provenance')

    # PDFs are omitted by archive. Only exact matches to recorded inputs are allowed.
    if corpus:
        papers_dir = papers_dir or root / 'papers'
        for name, expected in corpus.items():
            rel = Path(name)
            if rel.is_absolute() or '..' in rel.parts:
                raise ValueError('unsafe archived corpus path')
            path = papers_dir / name
            if not path.is_file() or path.is_symlink() or digest(path) != expected:
                raise ValueError(f'archived corpus file unavailable or changed: {name}; supply --papers-dir with the original corpus')
            files[f'papers/{name}'] = path

    candidates = []
    if (archive / 'literature/candidates.json').exists():
        candidates = [r for r in read_json(archive / 'literature/candidates.json')
                      if r.get('status') in ('downloaded', 'wishlist') and isinstance(r.get('year'), int)
                      and r['year'] <= 2010]
    return archive, files, {'problem': problem, 'models': models, 'approvals': approved,
                            'bibliography_candidates': candidates, 'selected_plan': selected[0].stem}


def tool_command(driver, workspace, command):
    if driver.CFG.get('isolation', {}).get('mode', 'host') == 'docker':
        return ['docker', 'run', '--rm', '--name', 'sqf-writeup-' + uuid.uuid4().hex,
                '--network', 'none', '--read-only',
                '--cap-drop=ALL', '--security-opt=no-new-privileges', '--pids-limit=256',
                '--user', f'{os.getuid()}:{os.getgid()}', '--tmpfs', '/tmp:rw,nosuid,nodev,mode=1777',
                '--env', 'HOME=/tmp', '--env', 'PYTHONDONTWRITEBYTECODE=1',
                '--mount', f'type=bind,src={workspace},dst=/workspace', '--workdir', '/workspace',
                driver.CFG['isolation']['image'], *command]
    return command


def preflight(driver):
    if driver.CFG.get('isolation', {}).get('mode', 'host') == 'docker':
        cmd = tool_command(driver, driver.ROOT, ['sh', '-c', 'command -v latexmk && command -v pdflatex'])
        # Preflight needs no workspace mount, avoiding exposure of the repository.
        i = cmd.index('--mount')
        del cmd[i:i+2]
        i = cmd.index('--workdir')
        del cmd[i:i+2]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        finally:
            cleanup_container(cmd)
        if p.returncode:
            raise ValueError('Docker image lacks LaTeX; rebuild isolation/Dockerfile with the TeX packages')
    elif not shutil.which('latexmk') or not shutil.which('pdflatex'):
        raise ValueError('writeup requires latexmk and pdflatex; install TeX before starting agents')


def cleanup_container(command):
    if command[:2] == ['docker', 'run']:
        name = command[command.index('--name') + 1]
        subprocess.run(['docker', 'rm', '--force', name], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=5)


def run_tool(driver, wd, command, logfile):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    venv = driver.agent_venv()
    if venv:
        env.update(VIRTUAL_ENV=str(venv), PATH=f"{venv / 'bin'}{os.pathsep}{env.get('PATH', '')}",
                   ZDOTDIR=str(venv), BASH_ENV='')
    cmd = tool_command(driver, wd, command)
    # Use the same termination discipline as agents, including child compilers.
    with logfile.open('w') as stream:
        stream.write(json.dumps({'command': command}) + '\n')
        stream.flush()
        process = subprocess.Popen(cmd, cwd=wd, env=env, stdin=subprocess.DEVNULL,
                                   stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            deadline = time.monotonic() + driver.CFG['timeout_s']
            while process.poll() is None and not driver.STOPPING.is_set() and time.monotonic() < deadline:
                try:
                    process.wait(timeout=.2)
                except subprocess.TimeoutExpired:
                    pass
            if process.poll() is None:
                driver.stop_process_group(process)
                raise RuntimeError('write-up build interrupted or timed out')
            if process.returncode:
                raise ValueError(f'{logfile.name} failed; see {logfile}')
        finally:
            if process.poll() is None:
                driver.stop_process_group(process)
            cleanup_container(cmd)


def build_manuscript(driver, wd):
    manuscript = wd / 'manuscript'
    validate_artifact_tree(manuscript)
    for name in ('main.tex', 'changes.md', 'README.md', 'reproduce.py'):
        if not (manuscript / name).is_file():
            raise ValueError(f'writer did not produce manuscript/{name}')
    if not any(manuscript.rglob('*.bib')) and not any('thebibliography' in p.read_text() for p in manuscript.rglob('*.tex')):
        raise ValueError('writer did not produce a bibliography')
    old_manifest = manuscript / 'reproduction.json'
    if old_manifest.is_file():
        for name in read_json(old_manifest).get('artifacts', []):
            path = Path(name)
            if path.is_absolute() or '..' in path.parts or path.suffix in ('.py', '.bib') or name in ('main.tex', 'changes.md', 'README.md'):
                raise ValueError('unsafe previous numerical artifact path')
            (manuscript / path).unlink(missing_ok=True)
    # Delete old build products so a successful return cannot validate a stale PDF.
    for name in ('main.pdf', 'main.log', 'reproduction.json'):
        (manuscript / name).unlink(missing_ok=True)
    manuscript_sources = {str(p.relative_to(wd)): digest(p) for p in manuscript.rglob('*')
                          if p.is_file() and p.suffix in ('.tex', '.bib', '.py', '.md')}
    python = 'python3' if driver.CFG.get('isolation', {}).get('mode') == 'docker' else str(driver.agent_venv() / 'bin/python3') if driver.agent_venv() else sys.executable
    run_tool(driver, wd, [python, 'manuscript/reproduce.py'], manuscript / 'reproduce.log')
    validate_artifact_tree(wd)
    verify_inputs(wd, manuscript_sources)
    manifest = read_json(manuscript / 'reproduction.json')
    artifacts = manifest.get('artifacts')
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError('reproduction.json needs nonempty artifacts')
    for name in artifacts:
        if not isinstance(name, str) or Path(name).is_absolute() or '..' in Path(name).parts or not (manuscript / name).is_file():
            raise ValueError('invalid or missing numerical reproduction artifact')
    run_tool(driver, wd, ['latexmk', '-cd', '-pdf', '-interaction=nonstopmode',
                          '-halt-on-error', '-no-shell-escape', 'manuscript/main.tex'], manuscript / 'build.log')
    validate_artifact_tree(wd)
    if not (manuscript / 'main.pdf').is_file() or not (manuscript / 'main.pdf').read_bytes().startswith(b'%PDF-'):
        raise ValueError('latexmk did not create a PDF')
    log = (manuscript / 'main.log').read_text(errors='replace')
    if re.search(r'(?:LaTeX Warning: (?:There were undefined references|Reference .* undefined|Citation .* undefined)|(?:Package .* Warning:.*(?:[Uu]ndefined|[Cc]itation.*not found)))', log):
        raise ValueError('LaTeX has unresolved references/citations; see main.log')
    # Sub-point overflows are invisible; only a visible overflow needs a revision.
    overfull = [float(x) for x in re.findall(r'Overfull \\[hv]box \(([0-9.]+)pt too (?:wide|high)\)', log)]
    if any(x > OVERFULL_PT for x in overfull):
        raise ValueError(f'LaTeX has boxes overfull by more than {OVERFULL_PT}pt; see main.log')
    # Numerical outputs can share extensions with TeX auxiliaries (e.g. .out).
    artifact_paths = {manuscript / name for name in artifacts}
    # Remove regenerable build files; keep declared numerical outputs too.
    for path in manuscript.rglob('*'):
        if path.is_file() and path.name.endswith(BUILD_FILES) and path not in artifact_paths:
            path.unlink()
    save(manuscript / 'build-inputs.json', {'accepted_snapshot': digest(wd / 'source/numerics/snapshot'),
                                     'artifacts': {n: digest(manuscript / n) for n in artifacts},
                                     'pdf': digest(manuscript / 'main.pdf')})


def writeup(driver, args):
    label = safe_label(args.label)
    from writeup_finalize import accept_round, finalize, verify_acceptance, verify_finalization, writeup_root
    if getattr(args, 'accept_round', None) is not None:
        accept_round(driver, label, args.accept_round, args.accepted_by, args.reason)
        return
    if getattr(args, 'finalize', False):
        finalize(driver, label)
        return
    if getattr(args, 'verify', False):
        _, record, final = verify_finalization(driver.ROOT, label)
        driver.log(f'{label}: accepted round {record["accepted_round"]} and {len(final["runs"])} preserved invocation records verified')
        return
    def accepted():
        if not (writeup_root(driver.ROOT, label) / 'acceptance.json').exists():
            return False
        if (writeup_root(driver.ROOT, label) / 'finalization.json').exists():
            _, record, _ = verify_finalization(driver.ROOT, label)
        else:
            _, record, _ = verify_acceptance(driver.ROOT, label)
        driver.log(f'{label}: round {record["accepted_round"]} is accepted by {record["accepted_by"]}; revision loop closed; use --finalize to preserve the audit')
        return True

    if not args.check and accepted():
        return
    archive, files, provenance = archive_sources(driver.ROOT, label, args.papers_dir)
    files.update(briefing_input(args.brief))
    if args.check:
        driver.log(f'{label}: archived approvals, integration, numerical snapshot and corpus verified; no agents started')
        return
    preflight(driver)
    writers = driver.model_list('writer')
    reviewers = driver.role_models('writeup_referees')
    if not writers or len(reviewers) != 2:
        raise ValueError('configure a writer and exactly two write-up referees')
    if len(set(reviewers)) < 2:
        driver.log('WARNING: write-up reviewers resolve to the same model')
    destination = driver.ROOT / 'writeups' / label
    destination.mkdir(parents=True, exist_ok=True)
    validate_artifact_tree(destination)
    source_hashes = {'archive': digest(archive),
                     'brief': digest(files['brief.md']) if 'brief.md' in files else None,
                     'papers': {name: digest(path) for name, path in files.items() if name.startswith('papers/')}}
    policy = {'writers': writers, 'reviewers': reviewers,
              'prompts': {r: driver.build_prompt(r) for r in ('writer', 'writeup_referee')},
              'schema': driver.SCHEMAS['writeup_review'],
              'effort': {r: driver.CFG['effort'][r] for r in ('writer', 'writeup_referee')},
              'capabilities': {r: driver.role_capabilities(r) for r in ('writer', 'writeup_referee')},
              'isolation': driver.CFG.get('isolation'), 'repository_url': driver.CFG['writeup']['repository_url'],
              'pipeline': digest(driver.ROOT / 'writeup_support.py')}
    binding = {'sources': source_hashes, 'policy': policy}
    binding_path = destination / 'inputs.json'
    if binding_path.exists() and read_json(binding_path) != binding:
        (destination / 'STALE').write_text('Inputs or policy changed; preserve this attempt and choose a fresh output directory.\n')
        raise ValueError('write-up inputs/policy changed; move the existing manuscript attempt aside before rerunning')
    save(binding_path, binding)
    (destination / 'STALE').write_text('Write-up in progress or incomplete.\n')
    state_path = destination / 'state.json'
    state = read_json(state_path) if state_path.exists() else {'round': 0, 'stage': 'new'}
    if state['stage'] == 'source-gap':
        raise ValueError('archived proof gap awaits Markus; see source-gap report before any further writer invocation')
    if state['stage'] == 'passed':
        current = destination / f"round-{state['round']}"
        if digest(current / 'manuscript') != state['manuscript_hash'] or digest(current / 'reviews') != state['reviews_hash']:
            raise ValueError('approved write-up changed; preserve it and start a fresh attempt')
        (destination / 'STALE').unlink()
        driver.log(f'{label}: existing write-up has two passing reviews; human acceptance still required')
        return
    try:
        archive_commit = subprocess.check_output(['git', '-C', str(driver.ROOT), 'log', '-1', '--format=%H', '--', f'archive/{label}'], text=True).strip()
        harness_commit = subprocess.check_output(['git', '-C', str(driver.ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    except subprocess.CalledProcessError as e:
        raise ValueError('cannot determine repository provenance') from e
    if not archive_commit:
        raise ValueError('source archive must be committed before writing')
    dirty = subprocess.check_output(['git', '-C', str(driver.ROOT), 'status', '--porcelain',
                                     '--untracked-files=all', '--', f'archive/{label}'], text=True)
    if dirty.strip():
        raise ValueError('commit the exact source archive before writing; archived files are uncommitted')
    provenance.update(repository_url=driver.CFG['writeup']['repository_url'], archive_commit=archive_commit,
                      archive_label=label, harness_commit=harness_commit,
                      writer_models=writers, reviewer_models=reviewers,
                      writer_cli_versions={m: driver.cli_version(driver.CODEX if driver.backend(m)[0] == 'codex' else driver.CLAUDE) for m in set(writers + reviewers)} if driver.CFG.get('isolation', {}).get('mode') != 'docker' else {},
                      version_note='Model IDs are recorded model identifiers; CLI versions are not model weight versions. Unavailable model versions remain unknown.')
    candidates = provenance.pop('bibliography_candidates')
    problem = provenance.pop('problem')
    start_round = state['round'] if state['stage'] in ('writing', 'draft', 'built', 'reviewing') else state['round'] + 1
    for rnd in range(start_round, start_round + driver.CFG['max_rounds']):
        if accepted():
            return
        folder = destination / f'round-{rnd}'
        folder.mkdir(exist_ok=True)
        if state['round'] != rnd:
            state = {'round': rnd, 'stage': 'writing'}
            save(state_path, state)
        manuscript = folder / 'manuscript'
        if state['stage'] == 'writing':
            incoming = dict(files)
            if rnd > 1:
                previous = destination / f'round-{rnd-1}'
                if (previous / 'manuscript').exists():
                    incoming['manuscript'] = previous / 'manuscript'
                feedback = previous / 'reviews'
                if feedback.exists():
                    incoming['feedback'] = feedback
                if (previous / 'build-feedback.txt').exists():
                    incoming['build-feedback.txt'] = previous / 'build-feedback.txt'
            wd = driver.sandbox(f'writeup-writer-{label}-r{rnd}', incoming)
            (wd / 'source/problem.md').write_text(problem)
            save(wd / 'provenance.json', provenance)
            save(wd / 'bibliography-candidates.json', candidates)
            expected = {k: v for k, v in input_hashes(wd).items() if not k.startswith('manuscript/')}
            state['writer_run'] = wd.name
            save(state_path, state)
            driver.run_agent('writer', wd, writers[(rnd-1) % len(writers)], driver.CFG['effort']['writer'])
            verify_inputs(wd, expected)
            if accepted():
                return
            if (wd / 'manuscript/SOURCE_GAP.md').is_file():
                shutil.copy(wd / 'manuscript/SOURCE_GAP.md', folder / 'SOURCE_GAP.md')
                state['stage'] = 'source-gap'
                save(state_path, state)
                raise ValueError(f'writer found a source-proof gap; Markus must decide: {folder / "SOURCE_GAP.md"}')
            if not (wd / 'manuscript').is_dir():
                raise ValueError('writer produced no manuscript directory')
            shutil.copytree(wd / 'manuscript', manuscript)
            state['stage'] = 'draft'
            save(state_path, state)
        if state['stage'] == 'draft':
            wd = driver.sandbox(f'writeup-build-{label}-r{rnd}', files | {'manuscript': manuscript})
            expected = {k: v for k, v in input_hashes(wd).items() if not k.startswith('manuscript/')}
            try:
                build_manuscript(driver, wd)
                verify_inputs(wd, expected)
            except ValueError as e:
                verify_inputs(wd, expected)
                (folder / 'build-feedback.txt').write_text(str(e) + '\n' + '\n'.join(
                    p.read_text(errors='replace')[-16000:] for p in sorted((wd / 'manuscript').glob('*.log'))))
                state['stage'] = 'revise'
                save(state_path, state)
                driver.log(f'{label} round {rnd}: build needs revision; retained logs in {folder}')
                continue
            shutil.copytree(wd / 'manuscript', manuscript, dirs_exist_ok=True)
            # Mirror build-time deletions, including auxiliaries left by the writer,
            # before binding reviews to the saved revision. Copy first so a failed
            # copy leaves the original draft available for a retry.
            for path in sorted(manuscript.rglob('*'), key=lambda p: len(p.parts), reverse=True):
                if not (wd / 'manuscript' / path.relative_to(manuscript)).exists():
                    if path.is_dir():
                        path.rmdir()
                    else:
                        path.unlink()
            state.update(stage='built', manuscript_hash=digest(manuscript))
            save(state_path, state)
        if state['stage'] in ('built', 'reviewing'):
            if accepted():
                return
            if digest(manuscript) != state['manuscript_hash']:
                raise ValueError('manuscript changed during review; preserve attempt before retrying')
            reviews_dir = folder / 'reviews'
            reviews_dir.mkdir(exist_ok=True)
            state['stage'] = 'reviewing'
            save(state_path, state)

            def review(index_model):
                index, model = index_model
                result_path = reviews_dir / f'{index}.json'
                if result_path.exists():
                    result = read_json(result_path)
                    driver.validate(result['review'], driver.SCHEMAS['writeup_review'])
                    validate_review(result['review'])
                    if result['model'] != model or result['manuscript_hash'] != state['manuscript_hash']:
                        raise ValueError('cached write-up review has different inputs')
                    return result['review']
                wd = driver.sandbox(f'writeup-referee-{label}-r{rnd}-{index}', files | {'manuscript': manuscript})
                (wd / 'source/problem.md').write_text(problem)
                save(wd / 'provenance.json', provenance)
                save(wd / 'bibliography-candidates.json', candidates)
                expected = input_hashes(wd)
                out = driver.run_agent('writeup_referee', wd, model, driver.CFG['effort']['writeup_referee'], schema='writeup_review')
                verify_inputs(wd, expected)
                value = out['structured_output']
                save(result_path, {'model': model, 'manuscript_hash': state['manuscript_hash'],
                                   'run': wd.name, 'review': value})
                return value

            # Cache completed independent reviews if the other provider fails.
            # A completed gap report remains decisive even if the other provider
            # failed. Do not start another reviewer on a usage-limit retry.
            def saved_gap():
                return any(read_json(p)['review']['verdict'] == 'source-gap'
                           for p in reviews_dir.glob('*.json'))
            if saved_gap():
                state['stage'] = 'source-gap'
                save(state_path, state)
                raise ValueError(f'archived proof gap requires Markus: {reviews_dir}')
            try:
                results = driver.parallel(review, list(enumerate(reviewers)))
            except RuntimeError:
                if saved_gap():
                    state['stage'] = 'source-gap'
                    save(state_path, state)
                raise
            if digest(archive) != source_hashes['archive'] or digest(manuscript) != state['manuscript_hash']:
                raise ValueError('source archive or manuscript changed during write-up')
            if accepted():
                return
            values = list(results.values())
            if any(r['verdict'] == 'source-gap' for r in values):
                state['stage'] = 'source-gap'
                save(state_path, state)
                raise ValueError(f'archived proof gap requires Markus: {reviews_dir}')
            if all(r['verdict'] == 'pass' for r in values):
                state.update(stage='passed', reviews_hash=digest(reviews_dir))
                save(state_path, state)
                (destination / 'STALE').unlink()
                driver.log(f'{label}: write-up has two passing reviews: {manuscript / "main.pdf"}; human acceptance still required')
                return
            state['stage'] = 'revise'
            save(state_path, state)
            driver.log(f'{label} round {rnd}: revision requested; see {reviews_dir}')
    raise ValueError(f'{label}: write-up needs attention after {driver.CFG["max_rounds"]} rounds; see {destination}; rerun to resume')
