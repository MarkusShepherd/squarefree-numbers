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

## Finalized write-up tracking development (5 Nov 2026)

- Worktree `.worktrees/writeup-stage`, branch `writeup/stage`, based on merged
  MR !22 at 60b6c9b. Main's write-up files and index remain untouched.
- Static `writeups/.gitignore` keeps accepted packages and their audit trails;
  intermediate rounds, scratch files and working checkpoints remain local.
  Ordinary `git add writeups/<label>/` selects the preserved package. Removed
  the proposed custom staging command and all temporary-index handling.
- Initial finalization still checks original round/input hashes. Verification
  of finalized packages and repeat finalization use only preserved evidence;
  they no longer require working round directories or root input files.
- Regressions use ordinary Git to stage a fixture package and export a clean
  checkout; offline verification and repeat finalization pass after deleting
  external runs. Also verifies packaged input corruption is rejected and a
  normal invocation still stops at accepted status without working inputs.
- Validation: all 78 dry-run tests passed in 84.955 seconds. All 25 focused
  tests passed in 3.983 seconds after the final retry/path checks.
  `git diff --check` passed.
- Implementation remains uncommitted. No live staging, model calls, commits,
  pushes or MR; main remains untouched.

## First write-up invocation (3 Nov 2026)

- Markus started `writeup zt-neutral` from main, using the original papers and
  fresh external RUNS_DIR `~/sqf-runs/writeup-zt-neutral`, without a briefing.
- Round 1 produced a 31-page PDF, sources and numerical reproduction artifacts
  under `writeups/zt-neutral/round-1/manuscript/`. The build succeeded. Opus and
  Sol both returned `revise`; both report that the main theorem and dependency
  chain match the archive and find no substantive source-proof gap.
- Requested revisions include a convergence qualification in an auxiliary
  lemma, a displayed arithmetic bound, outward rounding of numerical intervals,
  the finite-row range description, duplicate PDF destinations, unrecorded
  local statement changes, citation locators and minor wording/code references.
  These are reviewer findings, not operator-approved mathematical edits.
- Round 2's writer exited 1 on Claude's five-hour usage limit. The CLI reports
  reset at 2026-11-04 03:30 Europe/Helsinki. State remains round 2 / writing;
  STALE remains, and no accepted final manuscript has been produced.
- Wall clock approximately 22:30:57–23:42:10 (71m13s). Four provider invocations:
  Claude recorded $19.91 total; Codex reported 13,655 output tokens. Writer 1
  took 2,907 s; the full numerical reproduction about 718 s; reviews 487 s and
  385 s in parallel; writer 2 failed after 158 s.
- Inspected all 44 leak-scan hits: authorized repository provenance URLs,
  archived run paths and an archived compliance note naming the excluded paper.
  No excluded-source content identified in those contexts. No rerun, source
  correction, acceptance, commit or push performed by the operator.

## Resumed write-up (4 Nov 2026)

- The resumed round-2 writer and build completed; a 32-page draft and both
  reviews are in `writeups/zt-neutral/round-2/`. Both reviewers returned revise,
  while reporting that the main theorem, dependencies and numerical
  reproduction check out, with no substantive archived source-proof gap.
- Sol's sole remaining issue is an explicit `1 <= q <= x` restriction on the
  added Remark 6.3's relative-error formula. Opus requests clearer provenance
  for the write-up reviewer roles and review-originated corrections, and a
  checkable explanation of references to prior feedback files not supplied to
  reviewers. It asks Markus to acknowledge the convergence qualification
  narrowing an over-general auxiliary lemma from P5; all actual applications
  satisfy that qualification. Other Opus comments concern runtime wording and
  precise quotation of the owner's recorded acceptance wording.
- The harness advanced to round 3, but that writer exited 1 on Claude's usage
  limit. The CLI reports reset at 12:20 Europe/Helsinki on 4 Nov. State remains
  round 3 / writing, STALE remains, and no final write-up has passed review.
- Resumed invocation approximately 07:22:45–08:46:47 (84m02s). Cumulative
  write-up usage: eight invocations, Claude $34.66, Codex 26,260 output tokens.
  Inspected the 39 new leak hits: supplied provenance URLs, archived paths and
  archived compliance notes, with no excluded-source content identified in
  those contexts. No operator rerun, mathematical edit or acceptance performed.

## Round-4 review inspection (4 Nov 2026)

- Both reviewers returned revise. Sol's sole issue remains the absence of
  Markus's authorization for the changed presentation of the archived P5
  auxiliary Euler–Maclaurin lemma. The writer reformulated it using the
  original hypotheses and a sum-minus-integral limit; both reviewers find
  this correct and applicable, but Sol notes that the conclusion still differs
  from the archived statement. No main-theorem/source-proof gap is reported.
- Opus requests `y >= 1` in the standalone abstract, precise epsilon wording
  in Remark 1.2, and correction of the repeated claim that prior feedback
  files are present in the reviewers' package. It treats the lemma item as
  requiring Markus's attention but not as a mathematical blocker.
- The harness advanced to round 5; the writer exited 1 on Claude's usage
  limit. The CLI reports reset at 19:10 Helsinki. State remains round 5 /
  writing. No operator rerun, approval or manuscript/harness edit performed.

## Human acceptance: round 4 (4 Nov 2026)

- Markus: "Yes, do that. Round 4 is now accepted." This accepts the exact
  round-4 manuscript, including the revised presentation of Lemma 2.6, and
  overrides the remaining referee objections. No manuscript changes were made.
- The final human decision is recorded in `writeups/zt-neutral/acceptance.json`,
  bound to the original round hash, manuscript hash and exact PDF SHA-256.
  The accepted copy is `writeups/zt-neutral/accepted/manuscript/main.pdf`.
- `accepted/` preserves the unchanged manuscript, sources, numerical outputs,
  build/reproduction logs, both reviews, exact supplied archived source inputs,
  provenance, bibliography candidates, harness input bindings and recorded usage.
  Its manifest hashes all 128 bundled files; the acceptance record binds that
  manifest and the entire bundle.
- Verified the PDF and all 27 numerical artifact hashes against the build
  record, both reviewers' manuscript hashes, archived approval/integration
  bindings, numerical snapshot and original corpus hashes. The preserved
  manuscript and reviews are byte-identical to round 4.
- PDF SHA-256:
  `0d555b50b3adc0128399c2c08041d6d8a544a98978cf38bbfdaf8bbf2f3fcb55`.
- Both model verdicts remain `revise`. The original `state.json` and `STALE`
  retain the historical failed round-5 machine checkpoint; human acceptance is
  separate and closes the revision loop. No further agent round was launched.
- Inspected all 149 write-up leak-scan hits: authorized provenance URLs,
  archived paths and compliance statements. No excluded-source content found
  in those contexts. Cumulative recorded usage remains 15 invocations,
  Claude $51.80 and Codex 50,647 output tokens. No commit or push performed.

## Accepted write-up finalized (5 Nov 2026)

- Updated local main to merged MR !22 (60b6c9b), preserving staged write-up
  files and both staged and unstaged local run notes. Backup of the original
  run-note versions: `/private/tmp/sqf-main-update-4gsuqfbd/`.
- Finalization initially found the configured proof-run directory, which has
  no write-up records. Repeated with the original write-up RUNS_DIR explicitly:
  `RUNS_DIR=~/sqf-runs/writeup-zt-neutral ./orchestrate.py writeup zt-neutral --finalize`.
- Accepted round 4 and its numerical artifacts verified; all 15 invocation
  records and transcripts preserved in `writeups/zt-neutral/run-records/`,
  with audit bindings in `finalization.json`. Offline `--verify` passed.
- Steps completed at 09:43 Helsinki; total wall time under two seconds for
  finalization and verification. No new agents or provider usage/cost, no
  manuscript or referee edits, and no new commit or push.

- 5 Nov 2026, 11:15 Helsinki: local main updated to merged MR !23 at cda24df.
  Preserved staged and unstaged run notes; original note versions backed up at
  `/private/tmp/sqf-main-ignore-update-2fzqzrmi/`. Accepted round 4 and all
  15 preserved invocation records passed offline verification. Write-up data
  untouched; no write-up staging, commit, push or agent invocation.
