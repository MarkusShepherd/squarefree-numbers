# Operating the squarefree-numbers harness

You are the **operator** of a multi-agent proof attempt, not one of its agents.
The agents are separate `claude -p` / `codex exec` processes that
`orchestrate.py` starts in sandboxes under `runs_dir`
(`~/sqf-runs/squarefree-numbers`, outside this repository), so this file never
reaches them. Read `README.md` for how the harness works.

The experiment: can off-the-shelf models, in this harness, solve a problem from
Markus's 2011 master's thesis (sparse variance of squarefree numbers in
arithmetic progressions to polynomial moduli; see `problem.md`) *independently
of that thesis*? The run's process, cost and human interventions are the
material for a blog post, as much as its result.

## Roles

**You do mechanics:** run steps, read their output and transcripts, run the
checks below, debug and fix the harness (driver, stubs, config), archive runs,
and report what happened. Fix harness bugs on a branch with an MR, and run
`tests/dry_run.sh` before proposing it.

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
- `archive/` holds earlier runs. Don't copy anything from there into a new
  run's agent-visible files.
- Don't add papers to `papers/` or point agents to literature from 2011 or
  later: the run has a literature cutoff (README, "Independence from the
  thesis").

## Where the run stands (31 Oct 2026)

- Configured as in `config.json`: variant `neutral`; Opus
  (`claude-opus-5-5`) plans, referees and integrates; Sonnet
  (`claude-sonnet-5-5`) does numerics and proofs; Codex `gpt-6.1-sol` plans,
  referees and pollinates; effort `high`; `parallel` 2. Both subscriptions are
  the $20 plans: usage windows are the binding constraint.
- `papers/`: Vaughan 2005, Brüdern–Wooley 2011, BGP+ 1998 (gitignored), and
  nothing else: every agent gets a copy.
- **Literature cutoff:** agents may use only literature from 2010 or earlier,
  plus `papers/`. It was added after a first probe and numerics run, so **the
  whole run restarts from scratch** under the cutoff.
- **Earlier run, before the cutoff:** probe (no model knows a result for V_f;
  Opus half-recalls the title of Dehnert's paper) and numerics (constants
  extrapolated to f(y)/x → 0, about 0.135–0.142 ± 0.01 for the three
  polynomials). Archive it as `archive/pre-cutoff` and clear the run state
  (README, "Starting over") before starting again.
- **Next:** archive and clear the earlier run, `tests/dry_run.sh`, then step 0
  below.

Check `git log`, `./orchestrate.py status` and `logs/` before assuming any of
this is still current.

## Procedure

One step at a time. After each step, run its checks and report to Markus
before starting the next.

0. `./orchestrate.py probe`, then `./orchestrate.py numerics`.
   - Check: `logs/probe-*.md`; `check-leaks`; `numerics/results.json` has a
     `constant_extrapolated` for each polynomial.
   - Report: each probe's answer in short, and the extrapolated constants with
     their uncertainties.
1. `./orchestrate.py plan`: four planners (hints `vaughan`, `simplest`,
   `dirichlet`, `none`; models alternate Opus / Codex).
   - Check: four `plans/*.md`; `check-leaks`; in one Claude planner's
     `_stream.jsonl`, `grep -c hook_started` is 0 (user hooks disabled).
   - Report per plan: model, main theorem, range, number of propositions, crux
     propositions and their risks, and whether it claims agreement with the
     numerics. Then Markus selects.
2. `./orchestrate.py select <hint>`, with the hint Markus chose.
3. `./orchestrate.py prove`: prover/referee loop, up to `max_rounds` per
   proposition. This is the expensive step; watch for usage-limit failures
   (agents exit non-zero; rerunning `prove` resumes from the last round).
   - Report: `status`, and for each stuck proposition the referees'
     objections in short.
4. Stuck propositions: Markus decides between `./orchestrate.py pollinate P<n>`
   then `prove P<n>`, editing the statement, or replanning.
5. `./orchestrate.py integrate`; report `report/integration.json`, including
   the constant check against `numerics/results.json`.
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
- **Post-cutoff literature:** `post-cutoff arxiv` hits in `check-leaks`. An
  `exposure` (a search result from 2011 or later) is normal in a literature
  search; check whether the agent then used it. A `mention` or `attempt`
  (citing or fetching it) by a planner or prover: report it to Markus. The
  referees should fail any proof that relies on it; check that they did.
- **Codex agents:** list event types with
  `grep -o '"type":"[a-z_.]*"' runs/<agent>/_stream.jsonl | sort | uniq -c`.
  `mcp_tool_call` to `codex_apps` `search_service.web_run` is Codex's literature
  search and has no domain blocks, so read its queries and URLs. Any other MCP
  tool means the Codex restrictions aren't doing what the config says.
  `command_execution` is normal in a role without Bash (it is how Codex reads
  files); check that commands stay in the sandbox.
  `failed to connect to Responses WebSocket` is transient: delete that
  sandbox and rerun.
- **Dry run:** `tests/dry_run.sh` refuses to run while `logs/`, `plans/` etc.
  hold a real run. Move them aside (`mv logs logs.keep && tests/dry_run.sh;
  mv logs.keep logs`), or archive first.
- **macOS:** `grep` repetition counts are capped at 255 (`.\{0,500\}` fails);
  use Python for long context windows.
- **Sandboxes** can't install packages (network is denied); the numerics agent
  wrote C and stdlib Python.
- **Usage:** you run on the same Claude subscription as the agents. Keep your
  own effort moderate; don't read whole transcripts when a grep will do
  (they reach several MB).
