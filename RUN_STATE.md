# Where the run stands (2 Nov 2026)

Operator notes on the run's state; rules and procedure are in AGENTS.md.
Update this file after each step. `config.json`, `git log`, `logs/` and
`./orchestrate.py status` win over anything here.

- **Earlier run, before the literature cutoff:** archived as
  `archive/pre-cutoff` (commit 27adfd0 on main) and cleared from the repo and
  `runs_dir`. Don't import its numerical or mathematical outputs into the new
  run. `archive/pre-cutoff/logs.bk/` (its first probes) is gitignored and not
  in that commit.
- **Harness:** MR !16 (provider-parity). Both providers fill every role (see
  `config.json`); effort `high`; `parallel` 2. Both subscriptions are the $20
  plans: usage windows are the binding constraint.
- **Smoke tests passed** with real CLIs, in host and Docker mode: a Claude and
  a Codex referee on a toy proof, and a Codex librarian whose search showed up
  as native `web_search`.
- **Corpus (`papers/`):** Vaughan 2005, Brüdern–Wooley 2011, BGP+ 1998
  (gitignored). Further works only through the literature step.
- **Literature cutoff:** agents may use only literature from 2010 or earlier,
  plus `papers/`.
- **Not decided yet:** `isolation.mode` (host or docker) for the run. Choose
  before the first agent and keep it for the whole run.
- **Next:** merge MR !16, then from the main checkout (the first real command
  ties `runs_dir` to that checkout) start a new `logs/interventions.md` and run
  step 1 of the procedure: `probe`, `numerics`, `literature`.

## Current checkout audit (3 Nov 2026)

The preceding 2 Nov notes are historical and superseded by the current files.
`status` on 3 Nov reports P1–P9 passed in round 1; both integration reports
compose the selected plan without loss. Accepted numerics are in
`numerics/accepted/snapshot-nu6pbkr4/`. Usage: 42 agent invocations,
Claude $23.04; 16 Codex invocations with 160,543 output tokens.

At Markus's request the operator read the reports, all proposition statements,
proofs and reviews, and their relevant supporting material. Assessment: no
substantive mathematical gap found in the stated weaker-range theorem; local
corrections are needed in P1(iii), the P8 endpoint explanation, and unused
numerical notes in P6/P8. This is an operator assessment, not Markus's final
acceptance. No agent-visible mathematical files were changed and no new agent
stage was invoked. The leak scan remains at 21 hits with the previously logged
tool-path/compliance-note contexts. Await Markus's judgment; do not archive or
change mathematical statements on the basis of this audit alone.

## Write-up decisions (3 Nov 2026)

- Markus chose a harness writer agent for the archived-run write-up.
- All write-up work belongs in a dedicated worktree inside this repository,
  never the main checkout. Current worktree: `.worktrees/writeup`, branch
  `writeup/policy`. The main checkout's tracked files have been restored.
- The write-up belongs in this repository. Previous write-ups are excluded
  from later independent runs; this is now explicit in AGENTS.md and
  prompts/_rules.md. A write-up task may access its designated archive and
  manuscript only, not manuscripts from other runs.
- Scope: present the proof work recorded in the archive; no new literature
  search. Existing wishlist entries and references cited by available works
  are allowed, subject to the 2010 cutoff plus Brüdern–Wooley 2011.
  papers/ records available PDFs, not an exhaustive permitted bibliography.
- These are write-up policy changes, not a new agent stage or a modification
  of the accepted mathematical artifacts.
- Validation: tests/dry_run.sh passed all 37 tests (37 seconds);
  git diff --check passed.
