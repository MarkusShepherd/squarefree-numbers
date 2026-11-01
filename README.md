# sqf-sparse: a small multi-agent proof harness

A worked example of how to run "agents" on a research problem with off-the-shelf
Claude Code and Codex. The problem is the sparse variance for squarefree numbers in
arithmetic progressions to polynomial moduli (`problem.md`), but nothing in the
driver is specific to it.

## Ideas

- **An agent is one `claude -p` (or `codex exec`) process** in its own folder under `runs/`. The
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
orchestrate.py      the driver (~700 lines, standard library only)
numerics/           written by the numerics agent
plans/              one plan per hint (.json for the driver, .md for you)
plan.json           the plan you selected
props/P*/           statement, proof-vN, review-vN-i, objections, status
runs/               symlink to runs_dir (outside the repo): every agent's sandbox, kept
logs/costs.jsonl    one line per agent run: role, model, variant, seconds, cost, leak hits
logs/probe-*.md     what fresh models already know about the problem
logs/leaks.json     output of check-leaks
report/             integrator output
archive/<label>/    finished runs, copied by `archive` for committing
tests/              stub CLIs and dry_run.sh, for testing the plumbing for free
```

## Running it

### Before the first run

1. **Prerequisites.** Check, don't assume:

   ```
   python3 --version   # 3.10 or newer
   claude --version    # and logged in: `claude` starts without asking you to log in
   codex --version     # only for the default Claude+Codex mix; `codex login` once
   ```

   Without Codex, set `"backends": ["claude"]` in `config.json`. The driver
   uses only the standard library, so there is nothing to install; it carries
   PEP 723 metadata, so `uv run orchestrate.py <step>` works as well as
   `./orchestrate.py <step>` and pins the Python version.
2. **Your own instruction files.** `~/.claude/CLAUDE.md`, Claude Code's auto
   memory and `~/.codex/AGENTS.md` load into every agent. Make sure none of
   them mentions the thesis or Dehnert.
3. **Dry run, free:** `tests/dry_run.sh`. It runs every step with stub CLIs
   instead of `claude` and `codex`, checks the expected outcome, cleans up
   after itself, and ends with `dry run OK`. Rerun it after changing the driver.
4. **Papers** into `papers/` (gitignored; any file names), and nothing else:
   - Vaughan 2005, *A variance for k-free numbers in arithmetic progressions*,
     Proc. LMS 91, 573–597 (paywalled)
   - Brüdern–Wooley 2011: <https://www.math.purdue.edu/~twooley/publ/2011sparse.pdf>
   - Brüdern–Granville–Perelli–Vaughan–Wooley 1998:
     <https://www.math.purdue.edu/~twooley/publ/1998%20kfree.pdf>

   Every agent gets a copy of `papers/`, so a later paper left there would
   break the literature cutoff (see "Independence from the thesis").
5. **Choose the setup** in `config.json`: `variant` (`neutral` or
   `thesis-informed`, see `variants/README.md`), `backends`, models and effort.
   For a cheap first real run, set the Claude models to `sonnet` and every
   effort to `medium`.

### Backends

**Claude only, Codex only, or both.** `backends` in `config.json` lists the
enabled backends; `BACKENDS=claude` (or `codex`) in the environment overrides
it for one command. A model of a disabled backend is replaced by
`fallback` (`codex` -> `sonnet`, `claude` -> `codex`), so the per-role model
list stays as it is. `prove` warns if both referees end up as the same model.

```
BACKENDS=claude ./orchestrate.py plan
```

### A run, step by step

Read the output of each step before starting the next.

1. `./orchestrate.py probe`: ask fresh models, with no tools, what they already
   know about this variance. Read `logs/probe-*.md`. If a model reproduces the
   thesis's or Dehnert's result, runs with that model are contaminated by
   pretraining.
2. `./orchestrate.py numerics`: exact computation of V_f. Read
   `numerics/README.md` and sanity-check it yourself before going on; every
   later step trusts it.
3. `./orchestrate.py plan`: four planners in parallel. Read `plans/*.md`.
   Existing plans are kept, so a rerun only retries the failures. `plan --cross`
   adds every other model on every hint, as `plans/<hint>@<model>.*`, so that a
   strategy isn't lost to the model it happened to be paired with; select one
   with `select <hint>@<model>`.
4. `./orchestrate.py select vaughan` (or whichever plan you prefer).
5. `./orchestrate.py prove`: prover/referee loop for every proposition, up to
   `max_rounds` rounds each. `./orchestrate.py status` at any time.
6. For a stuck proposition: read `props/P*/objections.md`, then
   `./orchestrate.py pollinate P3` and `./orchestrate.py prove P3`. Or edit
   its statement by hand; that is often the right call.
7. `./orchestrate.py integrate`: checks the passed pieces compose and compares
   the constant with the numerics.
8. `./orchestrate.py check-leaks`: scan every transcript (it also runs after
   each agent and warns).
9. `./orchestrate.py archive [label]`: copy every sandbox and the run's
   outputs into `archive/<label>/` (default label: date, time and variant),
   without the PDFs. Review it and commit it; that is the run's permanent
   record. Agents never run inside the repo, so later runs can't read it.
   Transcripts at max effort can be several MB per agent; compress the
   archive or use Git LFS if that becomes a problem.

### Starting over

A run's state is `plans/ plan.json props/ numerics/ report/ logs/` in the repo
plus the sandboxes in `runs_dir`. To start a new run, archive the old one (step
9), then:

```
rm -rf plans plan.json props numerics report logs ~/sqf-runs/squarefree-numbers
```

To keep the numerics and only replan, keep `numerics/`.

## Independence from the thesis

An agent with web access could simply find the 2011 thesis. Full sandboxing,
a container per agent, isn't set up yet; it would work with the subscriptions
(`claude setup-token`, and a mounted `~/.codex/auth.json`). Instead:

**Enforced** for every agent, all tested against Claude Code:

- `--tools <list>` per role (`config.json`): the agent sees only these built-in
  tools. (`--allowedTools` alone only pre-approves; `Task`, `Skill` etc. stay
  visible.) Planners and provers get `WebSearch`/`WebFetch` for the literature
  search; referees get `Read` only.
- `--disallowedTools "mcp__*"` and `--strict-mcp-config`: no MCP servers or
  tools, including browser integrations such as Claude in Chrome.
- `ENABLE_CLAUDEAI_MCP_SERVERS=false`: no claude.ai connectors (GitLab etc.).
- `--settings '{"disableAllHooks": true}'`: your own hooks from
  `~/.claude/settings.json` don't run in agents (a `SessionStart` hook's output
  would otherwise go into the agent's context).
- `WebFetch(domain:...)` deny rules for the blog's domains and gitlab.com, and
  `Bash(curl *)`, `Bash(wget *)` deny rules.
- `--permission-mode dontAsk`: anything not pre-approved is denied.
- **Sandboxes outside the repository.** Agents run in `runs_dir`
  (`~/sqf-runs/squarefree-numbers` by default, `RUNS_DIR` overrides), not
  inside this git repo, so a Bash agent can't `git log` its way to the
  thesis-informed variant or to commit messages about the answer. The driver
  refuses to start if `runs_dir` is inside any git work tree. Claude agents
  also get a `Bash(git *)` deny rule.

**Instructed** (`prompts/_rules.md`, appended to every prompt): do not read
anything by Markus Schepke / Shepherd, or Dehnert's 2015 paper on the same
problem (Monatsh. Math. 177, 373–396); report it if encountered; do not use
remembered knowledge of either; do not read outside the working directory.
Dehnert's paper is paywalled, so there is no domain to block; the leak
patterns cover his name and the DOI.

**Literature cutoff.** Agents may use only literature from 2010 or earlier,
plus `papers/` (which includes Brüdern–Wooley 2011): roughly what was
available when the problem was set. This excludes Dehnert (2015) by
construction and keeps the run comparable with the original task. Deny rules
can't filter by date, so the cutoff is instructed (`_rules.md`), checked by
the referees (a proof relying on a later result fails review), and audited:
`check-leaks` reports new-style arXiv identifiers dated 2011 or later
(`arXiv:YYMM.NNNNN`, `arxiv.org/abs/...`) as `post-cutoff arxiv`, except in
probes, which have no rules. The year is `exclusion.literature_cutoff_year` in
`config.json`. Models still know later results from pretraining (the probes
name several); the referee check is what keeps them out of the proofs.

**Audited**: every run is recorded with `--output-format stream-json
--verbose` in `runs/*/_stream.jsonl`, including every search query, fetch and
tool result. `check-leaks` classifies hits of the patterns in
`config.json` as `exposure` (excluded material reached the agent, e.g. in a
search snippet: read it and decide whether the run is tainted), `attempt`,
`denied` and `mention`. It scans tool calls, tool results, the agent's text
and its reasoning (Claude `thinking` blocks, Codex `reasoning` items), and
matches on normalised text (lower case, no LaTeX/Markdown markup, hyphens or
dashes), so "Square-free" and "$k$-free" variants are caught.

**Not covered**: Bash can still reach the web by other means (e.g. Python's
`urllib`) and read files outside its folder by absolute path, including this
repository if the agent knows or guesses where it is; search snippets
can't be blocked, only detected; and pretraining can't be undone, only measured
(`probe`). Also check that your own `~/.claude/CLAUDE.md` and auto memory say
nothing about the thesis: they load into every `claude -p` session.

## Models: Claude and Codex

Any model in `config.json` can be a Claude model (`opus`, `sonnet`, ...) or
`codex` / `codex:<model>`, which runs that agent with the Codex CLI
(`codex exec`, logged in with your ChatGPT account) instead of `claude -p`.
Model IDs are pinned (`claude-opus-5-5`, `claude-sonnet-5-5`,
`codex:gpt-6.1-sol`), so they can't change mid-experiment; a bare `codex`
would run the Codex CLI's default model, since `--ignore-user-config` skips
the model set in `~/.codex/config.toml`. The default mix, sized for the $20
Claude and ChatGPT plans:

- **Opus** where judgement matters: one planner of two (`planner` may be a
  list; hints are assigned round-robin), one referee, the integrator.
- **Sonnet** for volume: the numerics and the provers. The Claude referee is
  therefore never the prover's own model.
- **Codex** (GPT-6.1-Sol) as the second model family: the other planner and
  referee, the pollinator, and one of the probes.
- Effort `high` everywhere (pollinator `medium`). `max` exhausts the plans'
  usage windows early in proving; raise effort for a single stuck crux
  proposition instead (`prove P3` after editing `config.json`).

Fable is not used: it isn't included in the standard subscription. GPT-6-Astra
is Codex's frontier model but costs several times Sol's usage; it is worth
trying as `codex:gpt-6-astra` for one referee round on a stuck crux
proposition, not as a default.

How a Codex agent differs (flags checked against codex-cli 0.166.0; run
`codex exec --help` if yours is newer):

- **Tools.** Codex has no per-tool whitelist. A role whose tool list contains
  Write, Edit or Bash runs with `--sandbox workspace-write` (writes only in its
  folder), anything else with `--sandbox read-only`. Commands have no network
  in either mode, which is stricter than the Claude side; but the read-only
  sandbox still lets the agent *read* files anywhere on disk.
- **Web access, without domain blocks.** Codex agents do literature search with
  the `codex_apps` MCP tool `search_service.web_run`, which stays available
  despite `web_search="disabled"` and `--ignore-user-config`. Codex can't deny
  individual domains: `tools.web_search.allowed_domains` did not stop a page
  from opening (codex-cli 0.166.0). So the blocks that Claude agents have are,
  for Codex, only the rules in the prompt plus the audit in `check-leaks`.
  `--disable apps` would remove web access altogether.
- **No user config.** `--ignore-user-config` keeps MCP servers and settings
  from `~/.codex/config.toml` out (login still works). `~/.codex/AGENTS.md` is
  still loaded, so check it says nothing about the thesis, as for `CLAUDE.md`.
- **Structured output.** The final message must be the JSON object;
  `--output-schema` would need strict schemas, and ours have optional fields.
- **Effort.** `codex.effort` maps the harness's effort levels onto
  `model_reasoning_effort`, one-to-one by default. GPT-6.1-Sol accepts `low`,
  `medium`, `high`, `xhigh` and `max` (checked with codex-cli 0.166.0); Ultra
  is a parallel sub-agent mode, not an effort level, and isn't used.
- **Cost.** Codex reports tokens, not dollars, and there is no equivalent of
  `--max-budget-usd`; only `timeout_s` caps a runaway Codex agent.
  `costs.jsonl` records the backend and token counts.
- **Auditing** is the same: `codex exec --json` events go to
  `runs/*/_stream.jsonl`, and `check-leaks` reads both formats.

`tests/dry_run.sh` exercises both backends.

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

## When an agent fails

Nothing retries or waits. A failed agent is logged and the batch goes on, so
after a usage limit, later agents probably fail too: rerun the step once the
window resets. An agent counts as failed if it exits non-zero, passes `timeout_s`
(it is killed), or ends without a successful result, such as an exhausted budget.
Its transcript stays in `_stream.jsonl`, which is written as the agent runs, is
scanned for leaks, and gets a line in `costs.jsonl` with the reason in `failure`.

## What it does not do

- Lean. Mathlib does not cover this kind of analytic number theory, so the
  referees and the numerics are the verifier. They are much weaker than a proof
  checker; the final read is yours.
- Automatic replanning. When a statement is wrong, its dependents are probably
  wrong too, and deciding how is the part worth doing yourself.
