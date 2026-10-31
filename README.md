# sqf-sparse: a small multi-agent proof harness

A worked example of how to run "agents" on a research problem with off-the-shelf
Claude Code. The problem is the sparse variance for squarefree numbers in
arithmetic progressions to polynomial moduli (`problem.md`), but nothing in the
driver is specific to it.

## Ideas

- **An agent is one `claude -p` process** in its own folder under `runs/`. The
  folder contains only what that role may see; it is kept afterwards, so you can
  read exactly what each agent saw (inputs), did (`_stream.jsonl`) and wrote.
- **State lives in files, not conversations.** Agents never talk to each other.
  The driver copies files between folders, and that copying *is* the
  information flow.
- **Propositions are contracts.** A prover sees only the *statements* of its
  dependencies, so all propositions can be attacked in parallel, and a broken
  proof of P2 cannot leak into P5.
- **Referees are independent by construction**: separate process, separate
  folder, read-only tools, no access to the prover's reasoning, the other
  referee, or earlier objections. Two different models referee each proof.
- **Structured output** (`--json-schema`) for anything the driver must parse:
  plans, verdicts. Free text for anything a human reads: proofs.
- **Humans steer at the seams**: you read the plans and pick one, and you decide
  what to do with stuck propositions.
- **Independence from the 2011 thesis** on this problem is enforced where it is
  cheap and *audited* everywhere else; see below.

## Layout

```
problem.md          the question (edit this for another problem)
papers/             PDFs the agents may read (you supply these)
prompts/            one file per role, plus schemas.json; _rules.md is appended to all
hints/              one strategy hint per planner
variants/           prompt variants that override prompts/ and hints/ (see variants/README.md)
config.json         models, effort, tools, exclusions, rounds, parallelism, budget
orchestrate.py      the driver (~500 lines)
numerics/           written by the numerics agent
plans/              one plan per hint (.json for the driver, .md for you)
plan.json           the plan you selected
props/P*/           statement, proof-vN, review-vN-i, objections, status
runs/               every agent's sandbox, kept for inspection
logs/costs.jsonl    one line per agent run: role, model, variant, seconds, cost, leak hits
logs/probe-*.md     what fresh models already know about the problem
logs/leaks.json     output of check-leaks
report/             integrator output
```

## Running it

Requires Claude Code (`claude`) logged in, and Python 3.10+.

1. Put the papers in `papers/`: Brüdern–Wooley 2011, BGP+ 1998 and
   arXiv:1912.04683 (see `problem.md`; Vaughan 2005 is paywalled and not
   included). `papers/` is gitignored: the PDFs are not ours to redistribute.
2. `./orchestrate.py probe`: ask fresh models, with no tools, what they already
   know about this variance. Read `logs/probe-*.md`. If a model reproduces the
   thesis result, runs with that model are contaminated by pretraining.
3. `./orchestrate.py numerics`: exact computation of V_f. Read
   `numerics/README.md` and sanity-check it yourself before going on; every
   later step trusts it.
4. `./orchestrate.py plan`: four planners in parallel. Read `plans/*.md`.
5. `./orchestrate.py select vaughan` (or whichever plan you prefer).
6. `./orchestrate.py prove`: prover/referee loop for every proposition, up to
   `max_rounds` rounds each. `./orchestrate.py status` at any time.
7. For a stuck proposition: read `props/P*/objections.md`, then
   `./orchestrate.py pollinate P3` and `./orchestrate.py prove P3`. Or edit
   its statement by hand; that is often the right call.
8. `./orchestrate.py integrate`: checks the passed pieces compose and compares
   the constant with the numerics.
9. `./orchestrate.py check-leaks`: scan every transcript (it also runs after
   each agent and warns).

To test the plumbing for free:

```
CLAUDE_BIN=$PWD/tests/fake_claude.py ./orchestrate.py numerics
```

and so on through the steps. The stub makes every proposition need two rounds
and makes P3 get stuck; the unhinted planner's transcript contains a planted
search result from an excluded domain, which `check-leaks` should report.
Delete `runs/ plans/ props/ numerics/ logs/ plan.json report/` afterwards.

## Independence from the thesis

An agent with web access could simply find the 2011 thesis. Full sandboxing
(containers, `--bare`) would need API billing, so instead:

**Enforced** for every agent, all tested against Claude Code:

- `--tools <list>` per role (`config.json`): the agent sees only these built-in
  tools. (`--allowedTools` alone only pre-approves; `Task`, `Skill` etc. stay
  visible.) Planners and provers get `WebSearch`/`WebFetch` for the literature
  search; referees get `Read` only.
- `--disallowedTools "mcp__*"` and `--strict-mcp-config`: no MCP servers or
  tools, including browser integrations such as Claude in Chrome.
- `ENABLE_CLAUDEAI_MCP_SERVERS=false`: no claude.ai connectors (GitLab etc.).
- `WebFetch(domain:...)` deny rules for the blog's domains and gitlab.com, and
  `Bash(curl *)`, `Bash(wget *)` deny rules.
- `--permission-mode dontAsk`: anything not pre-approved is denied.

**Instructed** (`prompts/_rules.md`, appended to every prompt): do not read
anything by Markus Schepke / Shepherd; report it if encountered; do not use
remembered knowledge of it; do not read outside the working directory.

**Audited**: every run is recorded with `--output-format stream-json
--verbose` in `runs/*/_stream.jsonl`, including every search query, fetch and
tool result. `check-leaks` classifies hits of the patterns in
`config.json` as `exposure` (excluded material reached the agent, e.g. in a
search snippet: read it and decide whether the run is tainted), `attempt`,
`denied` and `mention`.

**Not covered**: Bash can still reach the web by other means (e.g. Python's
`urllib`) and read files outside its folder by absolute path; search snippets
can't be blocked, only detected; and pretraining can't be undone, only measured
(`probe`). Also check that your own `~/.claude/CLAUDE.md` and auto memory say
nothing about the thesis: they load into every `claude -p` session.

## Cost control

Runs use your Claude Code login, so they count against your subscription's
usage limits rather than API billing.

- `max_budget_usd` in `config.json` is passed as `--max-budget-usd` to every
  call, so one runaway agent is capped.
- `logs/costs.jsonl` records each run; `status` prints the total.
- The expensive steps are the provers and referees at `max` effort. For a dry
  run, set everything to `sonnet` and `medium`.

## What it does not do

- Lean. Mathlib does not cover this kind of analytic number theory, so the
  referees and the numerics are the verifier. They are much weaker than a proof
  checker; the final read is yours.
- Automatic replanning. When a statement is wrong, its dependents are probably
  wrong too, and deciding how is the part worth doing yourself.
