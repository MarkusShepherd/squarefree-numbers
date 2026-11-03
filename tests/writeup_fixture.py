"""Tiny manuscript and adversarial behaviours for both stub providers."""
import json
import os


def draft(cwd):
    manuscript = cwd / 'manuscript'
    manuscript.mkdir(exist_ok=True)
    if os.environ.get('WRITEUP_SOURCE_GAP') == 'writer':
        (manuscript / 'SOURCE_GAP.md').write_text('Fixture: archived proof gap.\n')
        return
    if os.environ.get('WRITEUP_MODIFY_INPUT') == 'writer':
        (cwd / 'source/plan.json').write_text('{}')
    (manuscript / 'main.tex').write_text(r'''\documentclass{report}
\begin{document}Fixture manuscript.\input{table.tex}
\begin{thebibliography}{9}\bibitem{stub}Fixture.\end{thebibliography}
\end{document}
''')
    (manuscript / 'changes.md').write_text('Fixture mapping to P1 and P2.\n')
    (manuscript / 'README.md').write_text('Fixture reproduction.\n')
    (manuscript / 'reproduce.py').write_text('''from pathlib import Path
import json
assert Path('source/numerics/snapshot/compute.py').is_file()
Path('manuscript/table.tex').write_text('Recomputed fixture table.\\n')
Path('manuscript/reproduction.json').write_text(json.dumps({'artifacts':['table.tex']}))
''')


def review(cwd, provider):
    if os.environ.get('WRITEUP_MODIFY_INPUT') == 'reviewer':
        (cwd / 'manuscript/main.tex').write_text('tampered')
    if os.environ.get('WRITEUP_FAIL_REVIEW') in ('1', provider):
        # The parent test removes the environment flag on its retry.
        raise SystemExit('Fixture reviewer usage limit')
    verdict = 'pass'
    if os.environ.get('WRITEUP_SOURCE_GAP') == 'reviewer':
        verdict = 'source-gap'
    elif os.environ.get('WRITEUP_REVISE') == '1' and '-r1-' in cwd.name:
        verdict = 'revise'
    return {'verdict': verdict, 'summary': 'Fixture manuscript review.',
            'issues': [] if verdict == 'pass' else ['Fixture issue at theorem 1.'],
            **{f'{kind}_checks': f'Fixture {kind} checked.' for kind in
               ('statement', 'dependency', 'numerics', 'citation', 'provenance', 'layout')}}
