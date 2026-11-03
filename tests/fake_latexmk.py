#!/usr/bin/env python3
"""Build stub, so TeX need not be installed on a dry-run machine."""
import os
from pathlib import Path
import sys

if os.environ.get('WRITEUP_BAD_BUILD') == '1':
    sys.exit('Fixture TeX error')
if os.environ.get('WRITEUP_UNDEFINED') == '1':
    log = 'LaTeX Warning: There were undefined references.'
elif os.environ.get('WRITEUP_OVERFULL'):
    log = f"Overfull \\hbox ({os.environ['WRITEUP_OVERFULL']}pt too wide) in paragraph at lines 1--2"
else:
    log = 'Fixture clean build.'
manuscript = Path('manuscript')
(manuscript / 'main.pdf').write_bytes(b'%PDF-1.4\nfixture\n')
(manuscript / 'main.log').write_text(log)
(manuscript / 'main.aux').write_text('fixture aux\n')
(manuscript / 'chapters').mkdir(exist_ok=True)
(manuscript / 'chapters/intro.aux').write_text('fixture aux\n')
