#!/usr/bin/env bash
# Every test uses a temporary checkout and stub CLIs. Safe beside an active run.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPYCACHEPREFIX="${TMPDIR:-/tmp}/sqf-test-pycache"
python3 -m unittest discover -s tests -p 'test_*.py' -v
echo "dry run OK"
