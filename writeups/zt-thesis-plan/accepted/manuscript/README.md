# Sparse variance for squarefree numbers — write-up of archived run `zt-thesis-plan`

This directory contains a LaTeX account of the proof archived in `../source/`
(selected plan `thesis@gpt-6.1-sol`, archive commit
`867fc9baf25edf4995748d91dd950e98cfd9debf`), together with the script that
recomputes every number in its tables and figures.

## Files

- `main.tex`, `chapters/*.tex`: the manuscript (report class, 10 chapters + 2 appendices).
- `references.bib`: bibliography (BibTeX, style `plainurl` from urlbst, which
  prints the DOI of each entry as a link).
- `reproduce.py`: standalone numerical entry point.
- `generated/`: tables (`tab_*.tex`), pgfplots figures (`fig_*.tex`), plot data
  (`*.dat`) and constant macros (`constants.tex`), all written by `reproduce.py`.
- `reproduction.json`: machine-readable summary written by `reproduce.py`
  (`artifacts` lists every generated file relative to this directory; also
  parameters, fits, uncertainties, the decomposition of the extrapolation
  offset, the deviation trends quoted in Chapter 10, the consistency check
  against the archived snapshot, and the environment).
- `changes.md`: map from every statement to its archived proposition, proof
  and reviews; notation changes, merged arguments, corrections, added material
  and the revision history.

`reproduce.py` writes nothing else inside `manuscript/`: the snapshot code runs
in a separate build directory (see below).

## Reproduction

From the **workspace root** (the directory containing `source/` and `manuscript/`):

```sh
python3 manuscript/reproduce.py
```

Requirements: Python 3 with `numpy`, `scipy` and `mpmath`; `clang++` with C++17
support (the snapshot code calls `clang++ -O3 -std=c++17`). No network access
and no installation are needed. The full run recomputes the archived snapshot
grid (x up to 2.56·10^8). The full run that preceded revision 5 of this
document took 914 s (about 15 minutes), of which 910 s were the snapshot
pipeline, on a macOS arm64 machine. Every run records its own total time in
`reproduction.json → total_runtime_seconds` and its software versions in
`reproduction.json → environment`. Peak memory was not
recorded; at x = 2.56·10^8 the transform array alone has 2^29 32-bit entries
(2 GiB), so several gigabytes of free memory are needed. What it does:

1. Copies `source/numerics/snapshot/compute.py` and `counts.cpp` unchanged into
   a fresh temporary directory created by Python's `tempfile` (normally under
   `$TMPDIR`; the script refuses to build inside `manuscript/`), checks their SHA-256 against
   `source/numerics/accepted.json`, compiles the C++ worker locally there and
   runs the snapshot pipeline (`compute.main()`), including its validations
   and fits. The snapshot code writes its worker binary, per-x caches,
   `results.json` and `report.md` into that directory, which is deleted when
   the script ends. Nothing under `source/` is written.
2. Compares the recomputed rows with the archived `results.json` (exact integer
   counts and 70-digit values); the result is stored in `reproduction.json`
   under `snapshot.consistency_with_archived_results`.
3. Evaluates R_f, B_f, H_f(-1/2), K_f, W_f(h), Θ_f(H), F_f(H) from their
   Euler products (primes ≤ 10^7) and definitions, compares the data with the
   predicted profile, and applies the snapshot's own extrapolation routine to
   the exact profile.
4. Writes `generated/*` and `reproduction.json`.

Options: `--quick` (x ≤ 4·10^6 only; a pipeline test, whose tables differ from
the manuscript and overwrite `generated/`), `--build-dir DIR` (keep the
snapshot build in `DIR`, which must lie outside `manuscript/`, instead of a
temporary directory), `--reuse` (with `--build-dir`: reuse the per-x caches
there), `--pmax N` (prime cutoff for the Euler products).

## Compilation

```sh
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error -no-shell-escape main.tex
```

Packages used: amsmath/amssymb/amsthm/mathtools, thmtools, booktabs, enumitem,
microtype, geometry, xcolor, pgfplots (with the `groupplots` library),
hyperref, cleveref; BibTeX style `plainurl`. No shell escape is needed. `main.tex` inputs the files in
`generated/`, so `reproduce.py` must have been run first (the generated files
from the run used to prepare this document are included).

## Limitations and manual notes

- **Bibliography.** Only the supplied papers were read: Vaughan (2005),
  Brüdern–Granville–Perelli–Vaughan–Wooley (1998), Brüdern–Wooley (2011),
  Montgomery–Vaughan (2007), Goldston–Vaughan (1997) and Vaughan (1998, I).
  The two results quoted in proofs (BGPVW Lemma 2.2, Montgomery–Vaughan
  Corollary 10.5) were checked against these PDFs. Data for Warlimont (1980),
  Croft (1975), Mikawa–Peneva (2005), Montgomery (1970) and Hooley (1975) come
  from the reference lists of the supplied papers and the project's
  bibliography candidate list. Data for Mirsky (1949) come from the candidate
  list only. These references are cited only as background and were not
  checked against the originals; their DOIs are unverified. The DOI of
  Brüdern–Wooley (2011) is taken from the archived plan and was not verified.
  The supplied BGPVW PDF does not print its DOI; the DOI used was given in
  the archived proof of P2.
- **Numerics.** All fitted constants and uncertainty envelopes are heuristic.
  The snapshot's regression standard errors are formal OLS values for the
  fixed-x and joint fits. The fixed-ratio value is the standard error of the
  mean of eight slopes. None of them is a rigorous error bound.
  The truncation bound for K_f is rigorous for the omitted primes, but the
  floating-point evaluation is not certified. The precision used in each part
  (70-digit decimals for V in the snapshot, mpmath at the 85 digits set by the
  snapshot's `compute.py`, double precision for the constants) is recorded in
  `reproduction.json → parameters.precision`. See Chapter 10.
- **Status.** The mathematics is the archived, model-generated proof, approved
  by two model referees per proposition and by two integration reports. This
  agreement is evidence, not certification. No source gap was found while
  preparing this write-up (no `SOURCE_GAP.md`).
- **Sources consulted.** Only the files in this workspace were used: `source/`,
  `papers/`, `provenance.json`, `bibliography-candidates.json`, the previous
  rounds' reviews in `feedback/` (revisions 3, 4 and 5), a `build-feedback.txt`
  (revision 2 only) and the previous draft of this manuscript. No online
  resource, excluded author, excluded paper, other run or other write-up was
  accessed.
