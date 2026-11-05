# Accepted write-up: zt-neutral, round 4

Markus accepted round 4 on 4 November 2026, overriding the two recorded
`revise` verdicts. The manuscript and reviews are preserved unchanged.
The separate ../acceptance.json records the decision, exact hashes and
remaining referee issues, including authorization of the round-4 formulation
of the auxiliary Euler–Maclaurin lemma (Lemma 2.6).

- manuscript/main.pdf: accepted PDF.
- manuscript/: unchanged LaTeX, bibliography, numerical code, generated results,
  reproduction manifest and build logs.
- reviews/: unchanged independent reviewer reports.
- source/: the exact supplied archived proof and numerical inputs.
- provenance.json, bibliography-candidates.json and inputs.json: supplied
  provenance, existing bibliography candidates and harness input bindings.
- usage.json: recorded invocation costs/tokens, including failed attempts.
- manifest.json: SHA-256 hashes of every bundled file except the manifest itself.

For reproduction, use the commands in manuscript/README.md from this directory,
with the recorded scientific Python environment and a C++/TeX installation.
Original paper PDFs are not duplicated here; their hashes remain recorded in
inputs.json and they remain in the project's supplied corpus.

Human acceptance closes this revision loop. The original state.json and STALE
outside this bundle remain the historical automated checkpoint (failed round 5);
they have not been changed into model approval. The accepted PDF still contains
its pre-acceptance wording; the later owner decision is recorded separately.
