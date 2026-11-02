# Operating the squarefree-numbers harness

You are the **operator** of a multi-agent proof attempt, not one of its agents.
The agents are separate `claude -p` / `codex exec` processes that
`orchestrate.py` starts in working directories under `runs_dir`
(`~/sqf-runs/squarefree-numbers`, outside this repository), so this operator
guide is not copied to agents. Read `README.md` for how the harness works.

The experiment: can off-the-shelf models, in this harness, solve a problem from
Markus's 2011 master's thesis (sparse variance of squarefree numbers in
arithmetic progressions to polynomial moduli; see `problem.md`) *independently
of that thesis*? The run's process, cost and human interventions are the
material for a blog post, as much as its result.

## Roles

**You do mechanics:** run steps, read their output and transcripts, run the
checks below, debug and fix the harness (driver, stubs, config), archive runs,
and report what happened. Fix harness bugs on a branch with an MR, and run
`tests/dry_run.sh` before proposing it. Shared operator instructions belong here
in AGENTS.md; CLAUDE.md is a pointer, not a separate policy.

**Markus makes the mathematical decisions:** which plan to select, whether to
edit a proposition's statement, whether to pollinate or replan, when a proof
is good enough, and any change to prompts or hints during a run. You may
summarise plans, objections and verdicts to help him decide, neutrally and from
the run's own files only. Do not recommend a plan on the basis of what you know
about the answer.

## What you must not bring into the run

Your choices, summaries and edits reach the agents. Keep them independent of
the thesis:

- Do **not** open or read, unless Markus explicitly asks: the thesis PDF
  (`schepke_distribution_of_squarefree_numbers_in_arithmetic_progressions.pdf`,
  wherever it is), `variants/thesis-informed/`, issue
  mshepherd/riemannhypothesis.blog#4 and its comments, Dehnert (2015), or
  anything on riemannhypothesis.blog / primes.recommend.games.
- Do not put known results into prompts, hints, statements or `problem.md`:
  the thesis's range or constant, the factor-2 error in it, or the baselines'
  results. Markus knows these; if a change to an agent-visible file seems
  needed, propose it and let him decide.
- Use only literature from 2010 or earlier, except papers explicitly supplied
  in `papers/`. This also covers remembered results. Do not add anything to
  `papers/` beyond Markus's choices from `literature/review.md` and the initial
  approved corpus. Every agent reads `papers/INDEX.md`; it contains bibliographic
  entries only.
- `archive/` holds earlier runs. Don't copy anything from there into a new
  run's agent-visible files.

## Current state

`RUN_STATE.md` records where the run stands; read it first and update it after
each step. The current configuration and `./orchestrate.py status` are
authoritative where they disagree with it. A worktree has separate state;
never copy an earlier run's outputs into a fresh experiment unintentionally.

## Procedure

One step at a time. After each step, run its checks and report to Markus
before starting the next.

1. Run `probe`, `numerics` and the optional `literature` search. These are
   independent, but settle the approved papers before planning. Literature
   searches run on both providers by default; compare the attributed combined
   review and per-model responses in `literature/searches/`. Report probe
   answers; numerical constants and uncertainties; and the downloaded, wishlist
   and rejected literature lists with reasons. Markus picks additions to the
   corpus. Verify title pages and dates, copy only approved pre-2011 PDFs to
   `papers/`, and add their bibliographic entries to `papers/INDEX.md`. Markus
   validates and selects a candidate with `numerics --accept <candidate>`.
   The active numerical snapshot is named in `numerics/accepted.json`; never
   use leftover root-level numerical files from an earlier harness version.
   `plan` crosses every configured planner with every hint by default.
   - Check: expected `plans/*.md`; `check-leaks`; in one Claude planner's
     `_stream.jsonl`, `grep -c hook_started` is 0 (user hooks disabled).
   - Report per plan: model, main theorem, range, number of propositions, crux
     propositions and their risks, and whether it claims agreement with the
     numerics. Then Markus selects.
2. `./orchestrate.py select <hint>`, with the hint Markus chose.
3. `./orchestrate.py prove`: prover/referee loop, up to `max_rounds` additional
   rounds per proposition per invocation. Prover models rotate across rounds.
   This is the expensive step; watch for usage-limit failures
   (agents exit non-zero; rerunning `prove` resumes from the last round).
   - Report: `status`, and for each stuck proposition the referees'
     objections in short.
4. Stuck propositions: Markus decides between `./orchestrate.py pollinate P<n>`
   then `prove P<n>`, editing the statement, or replanning.
5. `./orchestrate.py integrate`; compare every independent integration report,
   including constant checks against the accepted numerics. Summarize differences
   in the final theorems; a machine boolean does not establish equivalence.
6. `./orchestrate.py check-leaks` over everything, then
   `./orchestrate.py archive [label]` and commit `archive/<label>/` on a
   branch.

## Intervention log

Append every human or operator decision that affects the run to
`logs/interventions.md` (gitignored; `archive` copies it):

```
- 2026-11-01 10:15 | Markus | select | chose plan 'vaughan' over 'dirichlet': <reason in his words>
- 2026-11-01 14:02 | operator | harness fix | prove crashed on X; fixed in MR !n, reran P3 round 2
```

Record: plan choice, statement edits (with the diff), pollinate calls, config
changes mid-run, reruns after failures, and harness fixes. Also note the
wall-clock time of each step and `status` cost totals. These numbers go into
the post.

## Checks and quirks

- **Leaks:** `./orchestrate.py check-leaks`. `exposure` (excluded material
  reached an agent) is serious: stop and show Markus the context. `mention` of
  Dehnert's title by an Opus agent is a known half-memory; report it, don't
  stop. Hits are printed in normalised form (lower case, no hyphens or
  markup). `shepherd` also matches unrelated authors called Shepherd; check
  the context.
- **Literature:** `post-cutoff arxiv` exposures can be expected in search results.
  Report uses/citations by planners and provers, and verify referee enforcement.
  A librarian may encounter later sources, but the driver must reject those
  items. Downloads never become agent inputs without Markus's decision.
- **Python:** build `agent-env/` into external `agent_venv` with `uv sync --locked`.
  Both backends must receive its PATH, VIRTUAL_ENV, ZDOTDIR and empty BASH_ENV;
  Codex must have `allow_login_shell=false`. Docker builds the same lockfile
  inside the image instead of mounting the host environment. A missing host
  environment must fail before agents start. See README for setup and opt-out.
- **Codex agents:** native `web_search` is available only to research roles.
  Apps, plugins, hooks and internal subagents are disabled. Any MCP event is
  unexpected and makes an invocation fail. A probe using tools also fails.
  Inspect native search queries and URLs for excluded material.
- **Dry run:** `tests/dry_run.sh` uses temporary checkouts and stub CLIs for
  both providers and single-provider modes. It is safe beside a real run.
- **Approvals:** statement/dependency/corpus edits and proof/review changes
  invalidate old approvals. A referee that changes supplied inputs fails its
  invocation. Legacy approvals, including those made before input-integrity
  verification, require review.
  `status`, `prove` and `integrate` perform this check; `report/STALE` marks
  outdated integration. Do not bypass it by manually changing status files.
- **Isolation:** host mode does not prevent outside reads or guarantee offline
  shell commands. Use the Docker runner for filesystem separation. Neither
  runner guarantees that web-search snippets exclude prohibited material.
- **macOS:** `grep` repetition counts are capped at 255 (`.\{0,500\}` fails);
  use Python for long context windows.
- **Numerics:** preserve supporting code as well as compute.py. The Docker
  image includes Python, a C compiler, Poppler and ripgrep.
- **Usage:** the operator shares its provider subscription with agent runs;
  don't read whole transcripts when a grep will do
  (they reach several MB).
