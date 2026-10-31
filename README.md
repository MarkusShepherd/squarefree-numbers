# sqf-sparse: a small multi-agent proof harness

A worked example of how to run "agents" on a research problem with off-the-shelf
Claude Code. The problem is the sparse variance for squarefree numbers in
arithmetic progressions to polynomial moduli (`problem.md`), but nothing in the
driver is specific to it.

## Ideas

- **An agent is one `claude -p` process** in its own folder under `runs/`. The
  folder contains only what that role may see; it is kept afterwards, so you can
  read exactly what each agent saw (inputs), did (`_stdout.json`) and wrote.
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

## Layout

```
problem.md          the question (edit this for another problem)
papers/             PDFs the agents may read (you supply these)
prompts/            one file per role, plus schemas.json
hints/              one strategy hint per planner
config.json         models, effort, rounds, parallelism, budget per call
orchestrate.py      the driver (~300 lines)
numerics/           written by the numerics agent
plans/              one plan per hint (.json for the driver, .md for you)
plan.json           the plan you selected
props/P*/           statement, proof-vN, review-vN-i, objections, status
runs/               every agent's sandbox, kept for inspection
logs/costs.jsonl    one line per agent run: role, model, seconds, cost
report/             integrator output
```

## Running it

Requires Claude Code (`claude`) logged in, and Python 3.10+.

1. Put the papers in `papers/` (Vaughan 2005, Brüdern–Wooley 2011,
   BGP+ 1998).
2. `./orchestrate.py numerics`: exact computation of V_f. Read
   `numerics/README.md` and sanity-check it yourself before going on; every
   later step trusts it.
3. `./orchestrate.py plan`: four planners in parallel. Read `plans/*.md`.
4. `./orchestrate.py select vaughan` (or whichever plan you prefer).
5. `./orchestrate.py prove`: prover/referee loop for every proposition, up to
   `max_rounds` rounds each. `./orchestrate.py status` at any time.
6. For a stuck proposition: read `props/P*/objections.md`, then
   `./orchestrate.py pollinate P3` and `./orchestrate.py prove P3`. Or edit
   its statement by hand; that is often the right call.
7. `./orchestrate.py integrate`: checks the passed pieces compose and compares
   the constant with the numerics.

To test the plumbing for free:

```
CLAUDE_BIN=$PWD/tests/fake_claude.py ./orchestrate.py numerics
```

and so on through the steps. The stub makes every proposition need two rounds
and makes P3 get stuck. Delete `runs/ plans/ props/ numerics/ logs/
plan.json report/` afterwards.

## Cost control

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
