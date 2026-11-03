# Prompt variants

Files in `variants/<name>/` override the files of the same path in `prompts/`
and `hints/` when `"variant": "<name>"` is set in `config.json`. The variant's
hint list is `variants.<name>.hints` in `config.json`.

## neutral (default)

The prompts in `prompts/` and `hints/`: generic guidance for careful analytic
number theory, written without knowledge of earlier work on this problem.

## thesis-informed

The planner's "things that commonly break plans", two items of the referee
checklist and the `no-trunc` hint were written by Claude **after reading the
2011 thesis on this problem** and encode the specific gaps it found there:
boundary terms from truncating the $k$-range, slowly decaying $q = p^2$
terms in tail sums, and a bounded oscillating term treated as a constant.

Runs with this variant are therefore *not* independent of the thesis. They are
kept to measure how much such targeted guidance helps: compare a neutral run
and a thesis-informed run on whether the referees catch these issues.

## thesis-plan

**Not independent of the thesis.** This variant uses the single shared hint
`hints/thesis.md`, written by the operator after Markus explicitly authorised
reading the thesis. It encourages a close reading and combination of Vaughan
(2005) and Brüdern–Wooley (2011), leaving the strategy and adaptations to the
agents. It supplies no decomposition, proof recipe, range, constant or known
error. It is separate from the targeted referee guidance in `thesis-informed`;
the role prompts remain the shared prompts.

Markus approved keeping and publishing the hint alongside the other hints.
Set `"variant": "thesis-plan"` in the experiment's worktree to produce two
plans, one from each configured planner. Markus selects after reading them.

For this comparison, use host mode, a separate worktree and a fresh external
runs directory (for example `~/sqf-runs/squarefree-numbers-thesis`). Keep
`problem.md`, the approved corpus, model/effort settings and `max_rounds`
unchanged from `zt-neutral`. Skip probe and new numerical/literature runs:
reuse its accepted numerical snapshot and existing literature search, as
explicitly authorised by Markus. Copy `numerics/accepted.json` and its named
snapshot intact; the driver verifies the problem and every snapshot artifact
hash. Numerical acceptance is not bound to the hint or variant. Do not import
the earlier run's plans, proofs or other proof-attempt outputs.

The comparison is subjective: Markus judges the plans and eventual results.
An operator session that has read the thesis must not subsequently operate a
neutral run.
