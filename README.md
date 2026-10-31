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

Requires Claude Code (`claude`) logged in, and Python 3.10+. For the default
model mix also the Codex CLI (`npm i -g @openai/codex`, then `codex login`).

The driver uses only the standard library, so there is nothing to install. It
carries PEP 723 metadata, so `uv run orchestrate.py <step>` works as well as
`./orchestrate.py <step>` and pins the Python version.

**Claude only, Codex only, or both.** `backends` in `config.json` lists the
enabled backends; `BACKENDS=claude` (or `codex`) in the environment overrides
it for one command. A model of a disabled backend is replaced by
`fallback` (`codex` -> `sonnet`, `claude` -> `codex`), so the per-role model
list stays as it is. `prove` warns if both referees end up as the same model.

```
BACKENDS=claude ./orchestrate.py plan
```

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
CLAUDE_BIN=$PWD/tests/fake_claude.py CODEX_BIN=$PWD/tests/fake_codex.py ./orchestrate.py numerics
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
anything by Markus Schepke / Shepherd, or Dehnert's 2015 paper on the same
problem (Monatsh. Math. 177, 373–396); report it if encountered; do not use
remembered knowledge of either; do not read outside the working directory.
Dehnert's paper is paywalled, so there is no domain to block; the leak
patterns cover his name and the DOI.

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

## Models: Claude and Codex

Any model in `config.json` can be a Claude model (`opus`, `sonnet`, ...) or
`codex` / `codex:<model>`, which runs that agent with the Codex CLI
(`codex exec`, logged in with your ChatGPT account) instead of `claude -p`.
The default mix uses Opus for the numerics, the provers and the integrator,
and Codex as the second model family: one of the two referees, every other
planner (`planner` may be a list; hints are assigned round-robin), the
pollinator, and one of the probes. Fable is not used: it isn't included in
the standard subscription.

How a Codex agent differs (flags checked against codex-cli 0.166.0; run
`codex exec --help` if yours is newer):

- **Tools.** Codex has no per-tool whitelist. A role whose tool list contains
  Write, Edit or Bash runs with `--sandbox workspace-write` (writes only in its
  folder), anything else with `--sandbox read-only`. Commands have no network
  in either mode, which is stricter than the Claude side; but the read-only
  sandbox still lets the agent *read* files anywhere on disk.
- **No web search.** Codex can't deny individual domains, so `web_search` is
  disabled for all Codex agents (`codex.extra_args`). A Codex planner therefore
  works from `papers/` and memory only, unlike the Claude planners.
- **No user config.** `--ignore-user-config` keeps MCP servers and settings
  from `~/.codex/config.toml` out (login still works). `~/.codex/AGENTS.md` is
  still loaded, so check it says nothing about the thesis, as for `CLAUDE.md`.
- **Structured output.** The final message must be the JSON object;
  `--output-schema` would need strict schemas, and ours have optional fields.
- **Effort.** `codex.effort` maps the harness's effort levels onto
  `model_reasoning_effort`; `max` maps to `high` by default.
- **Cost.** Codex reports tokens, not dollars, and there is no equivalent of
  `--max-budget-usd`; only `timeout_s` caps a runaway Codex agent.
  `costs.jsonl` records the backend and token counts.
- **Auditing** is the same: `codex exec --json` events go to
  `runs/*/_stream.jsonl`, and `check-leaks` reads both formats.

To test the plumbing for free, add `CODEX_BIN=$PWD/tests/fake_codex.py` to the
command below.

## Cost control

Runs use your Claude Code login, so they count against your subscription's
usage limits rather than API billing.

- `max_budget_usd` in `config.json` is passed as `--max-budget-usd` to every
  call, so one runaway agent is capped.
- `logs/costs.jsonl` records each run; `status` prints the total.
- The expensive steps are the provers and referees at `max` effort. For a dry
  run, set every Claude model to `sonnet` and every effort to `medium`.
- Codex agents count against your ChatGPT plan's limits instead, and `status`
  shows their token totals separately.

## What it does not do

- Lean. Mathlib does not cover this kind of analytic number theory, so the
  referees and the numerics are the verifier. They are much weaker than a proof
  checker; the final read is yours.
- Automatic replanning. When a statement is wrong, its dependents are probably
  wrong too, and deciding how is the part worth doing yourself.
