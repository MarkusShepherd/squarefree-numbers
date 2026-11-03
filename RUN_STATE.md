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
- The worktree requirement applied to harness development. After merging,
  the write-up stage runs from the main checkout with a fresh external RUNS_DIR;
  the development worktree has been removed.
- The write-up belongs in this repository. Previous write-ups are excluded
  from later independent runs; this is now explicit in AGENTS.md and
  prompts/_rules.md. A write-up task may access its designated archive and
  manuscript only, not manuscripts from other runs.
- Scope: present the proof work recorded in the archive; no new literature
  search. Existing wishlist entries and references cited by available works
  are allowed, subject to the 2010 cutoff plus Brüdern–Wooley 2011.
  papers/ records available PDFs, not an exhaustive permitted bibliography.
- Include provenance for open science and reproducibility: the models used,
  their recorded versions, and a repository link identifying the source commit.
  This is a provenance account, not a separate AI authorship disclosure.
  Do not claim human authorship. Do not invent model version details absent
  from the records.
- These are write-up policy changes, not a new agent stage or a modification
  of the accepted mathematical artifacts.
- Validation: tests/dry_run.sh passed all 37 tests (37 seconds);
  git diff --check passed.

## Write-up implementation (3 Nov 2026)

- Review correction: Markus approved `writeups/` as the output directory.
  The document is an accessible, self-contained write-up of the archived proof
  work for readers beyond the specialist audience; no degree-submission
  framing or fixed page target. Internal revision folders use `manuscript/`.
  Removed the added Git ignore overrides during review.

- Implemented `writeup <archive-label>` in the dedicated worktree, including
  archive-only proof inputs, original approval/input-integrity verification,
  an offline writer and two independent offline reviewers, resumable revision
  rounds, numerical reproduction, LaTeX compilation and source-gap stops.
- Review correction: removed the per-run brief and its mandatory pipeline
  requirement. Optional per-write-up briefings remain supported via `--brief`;
  no default briefing is generated. The writer chooses structure, ordering and
  exposition unless explicitly directed in a supplied briefing; shared prompts
  set the scope and standards.
- Archive packaging gap: the general `*.log` ignore rule kept 14 `.log` files
  of archive/zt-neutral out of Git, four of them in the accepted numerical
  snapshot and bound by its acceptance hashes. They were copied into this
  worktree from the main checkout and match the recorded hashes, but remain
  untracked; the ignore exception was removed during review. No mathematical
  artifact was edited.
- With those local copies, the real zt-neutral archive, original approval
  hashes, integration inputs, numerical snapshot and original supplied corpus
  pass `writeup --check`. A clean checkout of dc3dfe5 fails it ("archived
  accepted numerical snapshot changed") until the logs are committed on main.
- Validation: tests/dry_run.sh passed 42 tests in 76.623 seconds; real host
  latexmk compilation of a tiny fixture passed. All 7 write-up tests also
  passed in 31.687 seconds, including the two added retry/corpus tests.
- No real writer/reviewer invocation has started; additional provider usage
  and cost for this implementation stage are zero. Next operational step is
  the first write-up invocation using a fresh external RUNS_DIR, after this
  implementation is reported and reviewed.
- Review (3 Nov 2026): tests/dry_run.sh passed all 48 tests in 81 seconds.
  Added per-role time and USD limits (`role_limits`): writer 6 h / $60,
  write-up reviewers 3 h / $25; other roles unchanged.
- Cleanup review fixes (3 Nov 2026, uncommitted): preserve explicitly declared
  numerical artifacts even when their extensions match TeX auxiliaries; mirror
  build-time deletions into the saved manuscript before hashing and review.
  Added regressions for a numerical `.out` file and writer-generated top-level
  and chapter auxiliary files, including reuse of the completed review.
  tests/dry_run.sh passed all 51 tests in 101.461 seconds; git diff --check
  passed. No real agent invocation or additional provider usage/cost.
- Main-checkout execution fix (3 Nov 2026, uncommitted): removed the erroneous
  runtime worktree guard and corrected the operator/readme instructions.
  Added a full main-checkout regression with stub providers.
  tests/dry_run.sh passed all 52 tests in 100.813 seconds; git diff --check
  passed. No real write-up agents started; no commit or push.

## Thesis-plan preparation (3 Nov 2026)

These notes apply to the `thesis-plan-setup` worktree. Earlier run and write-up
notes above are historical; no proof run is active in this worktree.

- Markus authorised this operator to read the thesis and write a light hint
  encouraging the agents to combine Vaughan (2005) and Brüdern–Wooley (2011).
  The hint is in `hints/thesis.md`; it does not supply the methodology, range,
  constant or known error. `thesis-plan` is registered as a single-hint variant,
  separate from `thesis-informed`. The active config remains `neutral` until
  the new experiment is set up; no planner has been invoked.
- Markus approved publication of the hint alongside the other hints, host
  mode, reuse of the existing accepted numerics and literature search, and
  subjective comparison. He will judge/select after seeing both plans.
- Numerical acceptance is bound to the problem and full snapshot, not the
  hint or variant, so reuse requires no harness change or fresh acceptance.
  Reuse only the existing accepted snapshot and literature/corpus, not the
  neutral run's proof-attempt outputs.
- Shared agent rules now explicitly exclude other runs' plans, statements,
  proofs, reviews, integration reports and transcripts, as well as all GitLab
  content. `gitlab.com` was already blocked in config. Host mode continues
  to use prompt rules and transcript auditing rather than filesystem isolation.
- This operator has deliberately read the thesis with Markus's permission;
  do not use this session to operate a later neutral run. The downloaded PDF,
  extraction and inspection image are outside the repository in `/private/tmp`.
- All repository changes are in `.worktrees/thesis-plan-setup` on branch
  `thesis-plan-setup`. No real agents, commit, push or MR have been started.
- Markus requires worktrees inside the repository. Moved this worktree from
  `/private/tmp` into the repository's `.worktrees/` directory and repaired
  Git's worktree registration; changes and local intervention log preserved.
- Validation: `tests/dry_run.sh` passed all 52 tests in 95.240 seconds;
  `git diff --check` passed. The existing numerical acceptance verified all
  24 artifacts against the unchanged problem. Read-only planning preflight
  resolved the shared hint for Opus and Sol without creating a run directory.
  Additional harness-agent usage/cost: zero.
