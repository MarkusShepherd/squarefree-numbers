# Historical run snapshot

This snapshot predates the provider-parity changes. It is not a source of current
configuration or approval status. Check config.json, git log, logs/ and status.

## Cutoff restart (merged MRs !13–!15)

The snapshot below describes the earlier, pre-cutoff experiment, not an eligible
run under the new rules. Archive it as `pre-cutoff` before clearing its state.
The new run uses only literature from 2010 or earlier plus the approved corpus
(Vaughan 2005, Brüdern–Wooley 2011, BGP+ 1998). The 2019 background paper is
excluded. Rebuild the shared agent environment, then restart probe and numerics;
review optional literature search results before planning. Do not import the
old run's numerical or mathematical outputs into the new experiment.

## Where the run stands (31 Oct 2026)

- Configured as in `config.json`: variant `neutral`; Opus
  (`claude-opus-5-5`) plans, referees and integrates; Sonnet
  (`claude-sonnet-5-5`) does numerics and proofs; Codex `gpt-6.1-sol` plans,
  referees and pollinates; effort `high`; `parallel` 2. Both subscriptions are
  the $20 plans: usage windows are the binding constraint.
- `papers/`: Brüdern–Wooley 2011, BGP+ 1998, arXiv:1912.04683 (gitignored).
- **Done:** `probe` (no model knows a result for V_f; Opus half-recalls the
  title of Dehnert's paper, see `check-leaks`), `numerics` (constants
  extrapolated to f(y)/x → 0, about 0.135–0.142 ± 0.01 for the three
  polynomials).
- **Next:** MR !10 (mask runs_dir in the leak scan, disable user hooks in
  agents) should be merged first. Then `./orchestrate.py plan`.

Check `git log`, `./orchestrate.py status` and `logs/` before assuming any of
this is still current.

