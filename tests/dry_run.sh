#!/usr/bin/env bash
# Free end-to-end test of orchestrate.py: every step runs against
# tests/fake_claude.py and tests/fake_codex.py instead of the real CLIs, with a
# throwaway runs_dir. Refuses to touch an existing run; cleans up after itself.
set -euo pipefail
cd "$(dirname "$0")/.."

for p in plans props numerics report logs; do
    if [ -n "$(ls -A "$p" 2>/dev/null)" ]; then
        echo "dry_run: $p/ is not empty; archive or move the current run aside first" >&2
        exit 1
    fi
done
for p in plan.json archive/dry-run; do
    if [ -e "$p" ]; then
        echo "dry_run: $p exists; move it aside first" >&2
        exit 1
    fi
done

STUB_RUNS=$(mktemp -d)
export CLAUDE_BIN="$PWD/tests/fake_claude.py" CODEX_BIN="$PWD/tests/fake_codex.py"
export RUNS_DIR="$STUB_RUNS" BACKENDS=claude,codex   # both backends, whatever config.json says

cleanup() {
    rm -rf plans props numerics report logs plan.json archive/dry-run "$STUB_RUNS"
    rmdir archive 2>/dev/null || true
    if [ -L runs ]; then rm runs; fi        # the next real command re-creates it
}
trap cleanup EXIT

fail() { echo "dry run FAILED: $*" >&2; exit 1; }

./orchestrate.py probe
./orchestrate.py numerics
./orchestrate.py plan
[ "$(ls plans/*.json | wc -l)" -eq 4 ] || fail "expected 4 plans"
./orchestrate.py select vaughan
./orchestrate.py prove                  # P1, P2 pass in round 2; P3 gets stuck
./orchestrate.py pollinate P3
./orchestrate.py prove P3               # the stub referees always fail P3

status=$(./orchestrate.py status)
echo "$status"
grep -Eq '^P1 +passed' <<<"$status" || fail "P1 should have passed"
grep -Eq '^P2 +passed' <<<"$status" || fail "P2 should have passed"
grep -Eq '^P3 +stuck' <<<"$status" || fail "P3 should be stuck"

leaks=$(./orchestrate.py check-leaks)
echo "$leaks"
grep -q riemannhypothesis <<<"$leaks" || fail "check-leaks missed the planted leak"

./orchestrate.py archive dry-run
[ -d archive/dry-run/runs ] || fail "archive has no sandboxes"

echo "dry run OK"
