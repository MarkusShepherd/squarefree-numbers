# Manuscript: sparse variance of squarefree numbers to polynomial moduli

Files:

* `main.tex`: main file; `sections/*.tex`: the sections and appendices;
  `references.bib`: bibliography.
* `generated/`: every table fragment (`tab_*.tex`), plot data file (`fig_*.dat`),
  the macros for numbers quoted in the text (`macros.tex`), and the re-run
  snapshot output (`snapshot_rerun_results.json`). All of these are written by
  `reproduce.py`.
* `reproduce.py`: regenerates everything in `generated/` and writes
  `reproduction.json` (list of artifacts, their sources, parameters, fits,
  constants and checks).
* `changes.md`: map from the manuscript to the archived run, with notation
  changes, merged arguments, corrections and additions.

## Reproduction

Requirements (no installation or network access is needed or performed):
Python 3 with numpy, scipy, mpmath and sympy; `clang++` with C++17 support;
about 5 GB of free memory. No fixed running time is quoted here: the run
that produced the shipped artifacts records its own timings in
`reproduction.json` (`snapshot_rerun.seconds` for the snapshot re-run,
`snapshot_rerun.total_seconds_of_reproduce_py` for the whole script); the
snapshot re-run dominates.

From the workspace root (the directory containing `source/` and `manuscript/`):

```sh
python3 manuscript/reproduce.py
```

This

1. checks the SHA-256 of `source/numerics/snapshot/compute.py` and
   `counts.cpp` against `source/numerics/accepted.json`, copies both into the
   scratch directory `scratch/reproduce-work/`, and runs `compute.py` there
   unchanged. That script compiles `counts.cpp` with
   `clang++ -O3 -std=c++17`, re-runs its validations, recomputes all
   11 sizes x = 2.5e5 … 2.56e8 for the three polynomials, and redoes the
   fits. The archived executable `counts` is not used;
2. compares the regenerated `results.json` with the archived one (recorded in
   `reproduction.json` under `snapshot_rerun`);
3. computes C_f (Euler products over p ≤ 1e7 with a rigorous tail bound;
   interval endpoints rounded outwards; a 40-digit recomputation for
   p ≤ 1e5 as a check of floating-point rounding), Vaughan's c_2, the
   exact-shape sums `Σ f'(k) MT(x; f(k))` and `Σ F(k) h(f(k))`, symbolic
   checks, a self-test of the exact identity (Proposition 4.1), and, for each
   row at the largest x, the range of δ for which it lies in the range of
   Theorem 1.1(iii);
4. checks the qualitative statements made in Section 10 against the data,
   and checks that every number quoted there as a bound or range (rounded
   outwards: upper bounds up, lower bounds down) holds for the computed
   value. The script stops with an error if a check fails. It then writes
   `manuscript/generated/*` (including `macros.tex`, which holds every number
   quoted in the prose of Section 10) and `manuscript/reproduction.json`.

Options: `--work DIR` selects another scratch directory. The script refuses to
delete a non-empty directory that it did not create. `--reuse-work` reuses a
`results.json` already present in the scratch directory instead of re-running
the snapshot (for quick iterations only).

## Compilation

```sh
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error -no-shell-escape main.tex
```

The build uses only standard TeX Live packages (amsmath/amsthm, thmtools,
mathtools, pgfplots, booktabs, enumitem, hyperref, cleveref, microtype) and
BibTeX with the `plainurl` style. No shell escape is needed. `reproduce.py`
must have been run first, because the text inputs `generated/macros.tex` and
the generated tables.

## Bibliography limitations

* All works cited are in the supplied corpus (`papers/`). No historical
  attribution is made for the pair-count estimate of Proposition 5.1, whose
  proof is self-contained; the only related remark (Section 5) quotes what
  BGPVW (1998, §1, p. 3) report about Evelyn and Linfoot, whose papers were
  not consulted and are not cited separately.
* Goldston–Vaughan (1997) and Vaughan (1998, I) are cited only for the
  attribution made by Brüdern–Wooley (2011, §1); their content was not used.
* The supplied Brüdern–Wooley PDF is a preprint without journal header
  (PDF creation date 2009). The venue (Quart. J. Math. 62 (2011), 289–305) is
  taken from `papers/INDEX.md`. For it and for
  Brüdern–Granville–Perelli–Vaughan–Wooley (1998), whose venue is also taken
  from `papers/INDEX.md`, no URL, DOI or arXiv identifier is given in the
  supplied material, and none could be verified without network access. The
  bibliography entries say so; no locator was invented.
* Montgomery–Vaughan (2007): Theorem 1.8/1.9, Theorem 1.12, (2.20) and
  Corollary 10.4 were checked in the supplied chapters. Appendix B (Euler–Maclaurin
  summation) is not in the supplied corpus; the manuscript proves the needed
  Euler–Maclaurin lemma directly.
* Earlier work on the squarefree variance (Orr, Warlimont, Croft) is mentioned
  only as quoted in Vaughan (2005) and is not cited separately.

## Manual requirements

None beyond running the two commands above in this order.
