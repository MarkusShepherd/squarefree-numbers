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

## Thesis-plan planning review (4 Nov 2026)

- Current config is now `thesis-plan`, host mode, with external runs directory
  `~/sqf-runs/squarefree-numbers-thesis`. The accepted numerics and corpus have
  been supplied. Markus ran planning; both expected plans exist. No plan is
  selected and no proving has started.
- Opus (`plans/thesis.md`): 9 propositions; added hypothesis that f has no
  repeated irreducible factor; cruxes P7 (sparse arithmetic averaging) and P8
  (Mellin evaluation). Proposed asymptotic range has lower exponent
  max(13/15, d/(d+1)), with f(y)/x tending to zero.
- Sol (`plans/thesis@gpt-6.1-sol.md`): 7 propositions; original polynomial class;
  cruxes P4 (polynomial averaging) and P5 (Dirichlet series/residues). Supplies
  a fixed-ratio profile and a constant asymptotic with lower exponent
  1 - 2 min(1/5,1/(4d-1))/3. P3 also requires a uniform correlation adaptation.
  Both plans claim agreement with the existing numerical evidence; these are
  unproved contracts, not accepted results.
- Checks: status reports 3 invocations, Claude $4.56 and Codex 26,956 output
  tokens. First Claude invocation failed at the session limit after 3 seconds;
  successful retry took 2016 seconds (33m36s), Sol took 649 seconds (10m49s).
  No new agent invocation was made during this operator review.
- check-leaks: 3 hits, all from Claude's own persisted/background tool-output
  paths containing the project name; no excluded source content found in
  those contexts. Both Claude planner streams have 0 hook_started events.
  Sol's one native search queried the supplied 1998 and 2011 paper titles;
  it reports an unrelated 2015 metadata result, unopened and unused. Opus
  made no web search/fetch calls. Await Markus's plan choice.

## Thesis-plan proof status (4 Nov 2026)

- Markus selected the Sol plan and reports completion of proving. Operator
  status check confirms P1–P7 all passed in round 1 with current approvals.
- Status totals: 42 agent invocations; Claude $7.64; 23 Codex invocations,
  173,458 output tokens. This includes failed attempts and retries.
- Full leak scan: 10 hits. Contexts are Claude persisted/background tool
  paths and a referee compliance note naming excluded sources; no excluded
  source content is shown in these contexts.
- Next stage is integration by both configured integrators, followed by
  comparing their reports and numerical-constant checks. Integration has not
  been launched by the operator; no archive/commit/push action is authorised.

## Thesis-plan integration complete (5 Nov 2026)

- Markus reports integration, leak scan and status all good. Operator read
  both independent integration reports: Opus and Sol agree on the theorem,
  profile, constant, errors and asymptotic range, with no loss versus Sol's
  plan. Opus's minor interface notes are resolved within the supplied proofs.
  Both constants agree with the numerical uncertainty bands; Opus additionally
  diagnoses extrapolation-fit bias using the predicted profile.
- Current status: P1–P7 passed in round 1; integration is not marked stale.
  Totals: 44 agent invocations; Claude $9.46; 24 Codex invocations with
  185,060 output tokens. The final leak scan has 11 hits, consisting of
  tool-output paths and a referee compliance note naming excluded sources.
- Integration codex:gpt-6.1-sol: 260 seconds; failure: none.
- Integration claude-opus-5-5: 384 seconds; failure: none.
- Markus authorised committing the current worktree state before archiving.
  Archive label proposed: `zt-thesis-plan`. No archive or push performed.

## Write-up finalization development (4 Nov 2026)

- Fresh worktree `.worktrees/writeup-finalize`, branch `writeup/finalize`,
  based on main at 33aadc6. Main's staged write-up outputs and acceptance
  remain untouched; no real experiment was started in this worktree.
- Added `writeup <label> --finalize` to verify recorded human acceptance and
  preserve the associated invocation manifests, outcomes, full transcripts,
  provider outputs and available operator intervention log. Audit hashes bind
  the preserved files to acceptance without modifying the accepted bundle,
  referee verdicts or historical machine checkpoint.
- Added offline `--verify`; verification and repeated finalization work after
  external runs are removed. Normal execution stops at verified human
  acceptance instead of continuing revision rounds. No provider credentials,
  scientific environment, TeX, original PDFs or runs-directory claiming are
  required for these offline paths.
- Validation: all 66 tests passed in 92.290 seconds; 14 new regressions cover
  preservation, idempotency, missing/running records, changed artifacts and
  transcripts, conflicting destinations, symlinks/path traversal, offline CLI
  operation and run-directory discovery. The real accepted round 4 and all
  15 external invocation records also passed read-only verification with the
  new code. `git diff --check` passed.
- Implementation remains uncommitted. No push, MR, live finalization, agent
  invocation, mathematical edit or additional provider usage/cost.
- Added explicit human acceptance through `--accept-round N --accepted-by NAME`
  with optional `--reason`. It validates the completed revision and original
  supplied inputs, preserves the accepted package and both unchanged reports,
  records the decision, and closes the revision loop at stage boundaries.
- Final validation: all 76 tests passed in 100.417 seconds, including acceptance,
  finalization, offline verification and acceptance during a later revision.
  No live acceptance/finalization was performed; main's results are untouched.

## Main merge into thesis-plan worktree (5 Nov 2026)

- Resolved the RUN_STATE.md append conflict by preserving both the thesis-plan
  run history and main's separate write-up-finalization development notes above.
  The active experiment remains thesis-plan in host mode with its own external
  runs directory. No mathematical artifacts or experiment settings changed.
- Main's harness changes merged automatically. Merge commit and push have not
  been performed by the operator.
- Initial dry run exposed test fixtures inheriting the active thesis-plan
  variant while selecting neutral plan names. Pinned the temporary fixture
  config to neutral; the real experiment config is unchanged.
- Validation: all 76 dry-run tests passed in 84.081 seconds; both
  complete state histories preserved in order; no unresolved conflict paths;
  staged and unstaged diff whitespace checks passed.

## Thesis-plan archive verification (5 Nov 2026)

- Markus created and staged archive/zt-thesis-plan and authorised committing
  after operator verification. All 629 archived files exactly match the live
  run under the documented paper/PDF exclusions. All 628 substantive files
  are staged with matching Git blob hashes; the sole omitted file is Finder
  metadata (.DS_Store). All hash-bound numerical log files are included.
- writeup --check verifies all seven archived approvals, original referee
  input integrity, both successful integrations, numerical acceptance and the
  exact supplied corpus. A separate export of the Git index passed the same
  verification, so the check does not rely on unstaged archive files.
- Preserved all 44 invocation records. Original archive whitespace was kept
  unchanged rather than editing historical artifacts to satisfy formatting
  checks. No new agents or additional provider usage/cost.
- The write-up implementation works in this worktree with a fresh external
  RUNS_DIR; merging into main is an operator-guide workflow instruction,
  not a runtime prerequisite. No write-up has been started and no push was
  authorised for this archive commit.
