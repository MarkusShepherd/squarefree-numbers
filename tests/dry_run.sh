#!/usr/bin/env bash
# Free end-to-end test of orchestrate.py: every step runs against
# tests/fake_claude.py and tests/fake_codex.py instead of the real CLIs, with a
# throwaway runs_dir. Refuses to touch an existing run; cleans up after itself.
set -euo pipefail
cd "$(dirname "$0")/.."

for p in plans props numerics literature report logs; do
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
export LIT_ALLOW_FILE=1                 # the stub librarian's open PDF is a file:// URL

cleanup() {
    rm -rf plans props numerics literature report logs plan.json archive/dry-run "$STUB_RUNS"
    rmdir archive 2>/dev/null || true
    if [ -L runs ]; then rm runs; fi        # the next real command re-creates it
}
trap cleanup EXIT

fail() { echo "dry run FAILED: $*" >&2; exit 1; }

./orchestrate.py probe
./orchestrate.py numerics
./orchestrate.py literature             # one download, one wishlist, two rejected
lit=$(python3 -c 'import json; print(" ".join(r["status"] for r in json.load(open("literature/candidates.json"))))')
[ "$lit" = "downloaded wishlist rejected rejected" ] || fail "literature statuses: $lit"
[ "$(ls literature/pdf/*.pdf | wc -l)" -eq 1 ] || fail "literature: expected one downloaded PDF"
grep -q "after the 2010 cutoff" literature/review.md || fail "literature: 2015 paper not rejected"
grep -q "blocked host primes.recommend.games" literature/review.md || fail "literature: blocked host not rejected"
./orchestrate.py plan
[ "$(ls plans/*.json | wc -l)" -eq 4 ] || fail "expected 4 plans"
./orchestrate.py plan                   # keeps the existing plans
[ "$(ls -d "$STUB_RUNS"/plan-* | wc -l)" -eq 4 ] || fail "plan reran an existing plan"
./orchestrate.py plan --cross           # adds the other model on each hint
[ "$(ls plans/*.json | wc -l)" -eq 8 ] || fail "expected 8 plans after --cross"
[ "$(ls -d "$STUB_RUNS"/plan-* | wc -l)" -eq 8 ] || fail "--cross reran an existing plan"
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
grep -q "sparse variance for kfree" <<<"$leaks" || fail "check-leaks missed the planted title in a thinking block"
grep -Eq '^exposure +dehnert' <<<"$leaks" || fail "check-leaks did not class an MCP result as exposure"
[ "$(grep -c 'post-cutoff arxiv' <<<"$leaks")" -eq 1 ] \
    || fail "check-leaks: expected exactly one post-cutoff arXiv hit (1912.04683, not 1012.5674)"

# A killed agent keeps its transcript and is logged, with the failure.
slow="$STUB_RUNS/slow_agent.sh"
printf '#!/bin/sh\necho "{\\"type\\": \\"system\\"}"\nexec sleep 30\n' > "$slow"
chmod +x "$slow"
CLAUDE_BIN="$slow" python3 - <<'PY' || fail "timeout handling"
import json
import orchestrate as o
o.CFG["timeout_s"] = 1
wd = o.sandbox("timeout-test", {})
try:
    o.run_agent("probe", wd, "sonnet", "high")
    raise SystemExit("no exception on timeout")
except RuntimeError as e:
    assert "timed out" in str(e), e
assert "system" in (wd / "_stream.jsonl").read_text()
row = json.loads((o.ROOT / "logs" / "costs.jsonl").read_text().splitlines()[-1])
assert "timed out" in row["failure"], row
PY

./orchestrate.py archive dry-run
[ -d archive/dry-run/runs ] || fail "archive has no sandboxes"
[ -f archive/dry-run/literature/review.md ] || fail "archive has no literature review"
[ -z "$(find archive/dry-run -name '*.pdf')" ] || fail "archive contains PDFs"

echo "dry run OK"
