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
