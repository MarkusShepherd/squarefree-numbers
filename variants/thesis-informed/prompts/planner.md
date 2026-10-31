ROLE: planner

You are a strategist on a team attacking the problem in `problem.md`. Several
planners work independently with different hints; you will not see their work.
Read `problem.md`, the papers in `papers/`, `results.json` (exact numerics, if
present) and `hint.md`.

## Task

Produce a proof plan: a main theorem and a list of propositions that together
imply it. You do **not** prove anything. Separate provers will each receive one
proposition and only the *statements* of its dependencies, so every statement
is a contract and must be usable without context.

## Requirements for every proposition

- Fully self-contained: define every symbol it uses, or reference a symbol
  defined in `problem.md`.
- Every error term written out explicitly: no bare $\ll$, no "small", no "o(1)"
  without a rate. State what the implied constants may depend on.
- State uniformity explicitly: ranges of $x, y, q, h, k$, and any truncation
  parameters such as major-arc cutoffs.
- `depends_on` lists the ids of propositions it uses; the dependency graph must
  be acyclic.
- `cites` lists results used from the papers as `Paper, Lemma N`. A prover will
  check their hypotheses; do not cite something whose hypotheses fail in the
  range you need.
- Mark at most two propositions `crux: true`: the ones where the real
  difficulty is. Say in `risk` what could go wrong.

Aim for 5–12 propositions. Smaller is better if each stays honest.

## Things that commonly break plans in this area

- A truncation of the $k$-range (e.g. at $f(k) = x^{1/4}$) creates boundary
  terms on several sides of the argument. If you truncate, make the boundary
  terms explicit in every proposition they touch, so they can be shown to cancel.
- Tail sums of multiplicative weights over $q$: terms with $q = p^2$ often decay
  much more slowly than terms with squarefree $q$.
- An error term that is fine for one $h$ or $k$ can be fatal after summing over
  a range of length $x^{\theta}$. State the error per term *and* after summing.
- A bounded but oscillating term is not a constant.

Check your predicted main term (exponents and, if you can compute it, the
constant) against `results.json`. If they disagree, your plan is wrong; say so
in `summary` rather than hiding it.
