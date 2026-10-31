ROLE: integrator

Your folder contains `problem.md`, `plan.json` (the chosen plan),
`props/<id>/statement.md` and `props/<id>/proof.md` for every proposition (each
proof has passed two independent referees), and `results.json` (exact
numerics).

## Task

1. Check that the propositions compose: the main theorem follows from them with
   the error terms exactly as stated. Do the composition explicitly, with every
   error term, and write it to `assembly.md`.
2. Check for interface mismatches: a proposition used with a range, a
   uniformity or an error term other than what it states.
3. Compute the predicted main term, with the constant numerically for
   $f(k)=k^2+1$ and $f(k)=k^3+2$, and compare it with `results.json`. State the
   relative discrepancy at the largest $x$ available.
4. State the final theorem that the passed propositions actually prove. If it is
   weaker than the plan's main theorem, say exactly where the loss happens.

Return the structured verdict.
