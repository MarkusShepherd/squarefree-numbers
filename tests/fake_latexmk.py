#!/usr/bin/env python3
"""Build stub, so TeX need not be installed on a dry-run machine."""
import os
from pathlib import Path
import sys

if os.environ.get('WRITEUP_BAD_BUILD') == '1':
    sys.exit('Fixture TeX error')
if os.environ.get('WRITEUP_UNDEFINED') == '1':
    log = 'LaTeX Warning: There were undefined references.'
else:
    log = 'Fixture clean build.'
manuscript = Path('manuscript')
(manuscript / 'main.pdf').write_bytes(b'%PDF-1.4\nfixture\n')
(manuscript / 'main.log').write_text(log)
