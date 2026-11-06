# Changes and source map

Archive: `source/` (run `zt-thesis-plan`, plan `thesis@gpt-6.1-sol`, archive
commit `867fc9baf25edf4995748d91dd950e98cfd9debf`). Every proposition P1–P7 is
archived as `source/props/Pn/statement.md` and `source/props/Pn/proof.md`, with
two reviews: `review-v1-0.json` by `claude-opus-5-5` and `review-v1-1.json` by
`codex:gpt-6.1-sol`. All fourteen reviews give the verdict **pass**. Their
severities are "none", except "cosmetic" for the Opus reviews of P2, P5 and P7.
The integration reports are `source/report/assembly-claude-opus-5-5.md`,
`assembly-codex-gpt-6.1-sol.md`, `integration*.json`; both conclude that the
propositions compose with no loss.

No mathematical correction was made, and no gap was found. No `brief.md` was
supplied. A `build-feedback.txt` was supplied for revision 2; it concerned only
the reproduction script (§7, revision 2). Revision 3 responds to the previous
round's reviews `feedback/0.json` (`claude-opus-5-5`) and `feedback/1.json`
(`codex:gpt-6.1-sol`), both with verdict "revise" and both reporting no source
gap (§7, revision 3). Revision 4 responds to the next round's reviews, again
`feedback/0.json` (`claude-opus-5-5`) and `feedback/1.json`
(`codex:gpt-6.1-sol`), both "revise", both reporting no source gap (§7,
revision 4). Revision 5 responds to the following round: `feedback/0.json`
(`claude-opus-5-5`, "revise", minor notation and README issues only) and
`feedback/1.json` (`codex:gpt-6.1-sol`, "pass", no issues); neither reports a
source gap (§7, revision 5). The intervention record
(`source/interventions.md`) authorises no change to the mathematics.

## 1. Map of results

Numbers refer to the compiled `main.pdf`. "Pn (k)" means equation (k) of the archived proof of Pn.

| Manuscript | Archived source | Reviews |
|---|---|---|
| Theorem 1.1 (main theorem), (1.8)–(1.11) | P7 statement; plan main theorem (`source/plan.md`); constants from P5 statement, (29), (34) | P7 v1-0, v1-1; P5 v1-0, v1-1 |
| Corollary 1.2 | plan main theorem ("In particular…"); derived in both integration reports (Opus with ε=δ, Sol with ε=δ/2); **not** an approved proposition (stated in Appendix B, "Status of the evidence") | — (integration reports) |
| Remark 1.3 (two regimes) | integration report (Sol), last paragraph of numerics section; plan "Numerics check" | — |
| Remark 1.4 (K_{t+1}=c_2) | **added in write-up** (see §5) | — |
| Remark 1.5 (limitations), §9.4 | integration reports, "loss_vs_plan"; plan risks of P3, P7 | — |
| §1.5 strategy | plan summary and statements P1–P7 | — |
| Lemma 2.1 (elementary sums) | P1 (19), (21); P2 (17) and the bound for log(2x); P3 (3), (15)–(16); P4 (34); P5 (2) | P1–P5 reviews |
| Lemma 2.2 (divisor bound) | P2 (5); P3 (2) (special case η=1/10) | P2, P3 |
| Lemma 2.3 (infinite products) | P5 (3) and the positivity argument after (27); P1 convergence of ∏(1−2/p²) after (28); the Cauchy argument comes from the cosmetic remark of P5 review v1-0 | P5 v1-0 (cosmetic) |
| Lemma 2.4 (Euler products) | P1 justification of (7), (18), (26); P3 (14); P4 Euler product of (10); P5 (14)–(16), (36) | P1 v1-0 (cosmetic) |
| (2.1) c = ∏(1−p^{-2}) | P1 (6); P4 before (18) | P1, P4 |
| Lemma 2.5 (Ramanujan sums) | P4 (12)–(15); P1 (24)–(25) | P1 v1-0 (cosmetic), P4 |
| Lemma 2.6 (the polynomial) | P2 §1 (1)–(4), (17), (21); P4 (1)–(5); P7 (1)–(2) and the existence of z | P2, P4, P7 |
| Lemma 2.7 (root counts) | P5 (1); P6 (6); P5 multiplicativity of ρ before (35) | P5, P6 |
| Proposition 3.1 (density) | P1 (1)–(9); also P2 (6), which is the case l=0 | P1, P2 |
| Proposition 3.2 (second moment) | P1 (10)–(22) | P1 |
| (3.6), Proposition 3.3 (singular series) | P1 (23)–(28); P4 (18) for absolute convergence | P1, P4 |
| §4.1, Lemma 4.1 | P2 statement definitions; P2 (11) | P2 |
| Lemma 4.2 (mixed term) | P2 (6)–(9) | P2 |
| Proposition 4.3 | P2 first assertion, (12)–(19) | P2 |
| Quoted result 4.4, (4.6) | P2 §4 (BGPVW 1998, Lemma 2.2, (2.6), (2.7); normalisation check) | P2 v1-0 (checked against PDF), v1-1 |
| Proposition 4.5 | P2 second assertion, (20)–(23) | P2 |
| Proposition 5.1 | P3 (whole proof) | P3 |
| (6.2), Lemma 6.1 | P4 (17), (19); P5 (6) | P4, P5 |
| Lemma 6.2 (W = averaged 𝔖) | P4 (8)–(11), (13)–(18) | P4 |
| Lemma 6.3, (6.4) | P4 (6), (7) | P4 |
| Proposition 6.4 | P4 statement; (20)–(26) for (6.6), (36)–(41) for (6.7) | P4 |
| Lemma 6.5 | P4 (27)–(32) | P4 |
| Lemma 7.1 (zeta) | P5 (19)–(23); P6 (3) (identical to P5 (22)) | P5, P6 |
| (7.3)–(7.6) | P5 (4), (5), (10) | P5 |
| Proposition 7.2 | P5 statement and proof; (d) also P7 "identification of the density" | P5, P7 |
| Quoted result 8.1 | P6 §1 (Montgomery–Vaughan Cor. 10.5; Cor. 10.4 mentioned) | P6 |
| Lemma 8.2 | P6 (4), (5) and the T^{11/8} bound | P6 |
| Lemma 8.3 | P6 (6)–(10) | P6 (Opus review notes that P6 supplies the strip bound itself; assembly report "minor") |
| Lemma 8.4 (Mellin kernel) | P6 (11) | P6 |
| Proposition 8.5 | P6 statement; (12)–(18) | P6 |
| Lemma 8.6 (integral identity) | P6 §5, (19)–(20) | P6 |
| Lemma 9.1 | P7 (5)–(12) | P7 |
| §9.2, proof of (1.8), (1.9) | P7 (13)–(24); error table from P7 (19) and the assembly reports | P7 |
| Remark 9.2 (ε<η/2 unused) | P7 review v1-0 (claude-opus-5-5), third cosmetic remark; not the assembly reports, which restate the hypothesis without this remark (attribution corrected in revision 3 and moved out of the text) | P7 v1-0 |
| §9.3 (proof of Corollary 1.2) | integration reports (Opus: "Corollary in the plan"; Sol: "Final theorem…") | — |
| Chapter 10 | numerical snapshot `source/numerics/snapshot/` (README, report, compute.py, counts.cpp); plan "Numerics check"; integration reports' numerics sections | — |
| Appendix A | snapshot `results.json` (recomputed) | — |
| Appendix B | `provenance.json`, `source/interventions.md`, `source/numerics/accepted.json` | — |

## 2. Notation changes

- Polynomial growth constants: P2's `A, B`, P4's `a, B` and P7's `b_f, B_f^*` became κ₁, κ₂ (Lemma 2.6). This avoids a clash with the constant B_f. U = κ₂/κ₁ and V = U+U² come from P4 (3).
- P2's mixed term `M(x;q)` → Δ(x;q). P2's `N_a(x), D_a` → Q(x;a,0), g(a,0).
- P4's tail and moment `T_R, M_R` → 𝒯(R), 𝒩(R). P4's `D = U+V` → D_w. P4's `K, K_2` → K₂, K₃. P4's `S_1, S_2, I_2` → T_f, M_f, I_f, which are also P7's `M, I`. P4's `H = ⌊x/Z⌋` → H₀.
- P4's coefficient `R_f = Σ λ(r)ρ(r)/r` is written R̃_f in Chapter 6 until Proposition 7.2(d) identifies it with the residue R_f. The archive uses one symbol, and P5 proves the equality.
- P3: divisor variables `d, e` → e₁, e₂ (d is the degree); `A(m), A_H(m)` → 𝒜(m), 𝒜_H(m); constant `67+2D` → K_c = 67+2D_{1/10}.
- P5: the local coefficients α_p, β_p, δ_p of P5 (4) are used throughout. The local factor of P_f is L_p(s) and that of H_f is M_p(s) (P5 notation). P6's local factor of H_f, written `L_p` there, is M_p here. The archived a_p, b_p, c_p and B_p(s) are recorded in §7.2 of the manuscript.
- P6: the constant of MV Cor. 10.5, called `Q` there, → c_MV.
- P7: δ = ε/2 → ε₁ (δ is reserved for Corollary 1.2).
- Root-count constant (revision 5): P5's `C_0 = max{d,|A_d|,1}` → C_ρ = max{d,|A_d|} (Lemma 2.7, Chapter 7; the 1 is redundant since d ≥ 1). The letter C₀ is kept only for the absolute constant 10/3 of Proposition 3.2(d) (P1's `C = 10/3`), used in Proposition 6.4.
- P4's averaged local density `δ_p(h)` (P4 (16)–(17)) → ϑ_p(h) (Chapter 6, (6.2)), so that δ_p denotes only P5's local coefficient in Chapter 7 (revision 5).
- P5's real abscissa `η` in the holomorphy argument after P5 (21), which gives (7.2), → σ₀ (proof of Lemma 7.1(b); revision 5), since η is used for η_d and in Lemmas 2.1(d), 2.2.
- P1: the auxiliary `L(r) = φ(r)G(r)²` is not used. The text works with λ/c² directly, as P4 does.
- W_f(h) is displayed in the introduction by its three local cases (1.5). These cases are those of P5 after (5). K_f is displayed in the expanded form (1.10), which is algebraically identical to P5 (29): (1−2/p²)[a_p+(b_p−a_p)√p+(c_p−b_p)p] = α_p+β_p√p+δ_p p, and the expansion was checked with sympy.

## 3. Merged arguments

- **Counting squarefree numbers in a class**: P2 (6) is P1 (5) with l = 0, because N_a(x) = Q(x;a,0) and D_a = g(a,0). Both now cite Proposition 3.1.
- **Polynomial bounds**: P2 §1, P4 (1)–(5) and P7 (1)–(2) are merged into Lemma 2.6. P2's bound Σ f'(k)/f(k) ≤ (3D_ηB/A)L log(2x) is replaced by P4's 2U log(2x) (Lemma 2.6(c)). This changes only the constant in Proposition 4.3.
- **Divisor bound**: P2 (5) and P3 (2) are merged into Lemma 2.2.
- **Ramanujan sums**: P1 (24)–(25) and P4 (12)–(15) are merged into Lemma 2.5. Multiplicativity is proved via (a) as a Dirichlet convolution (the P4 route), which replaces P1's CRT sketch (P1 review v1-0, cosmetic).
- **Zeta formula**: P5 (22) and P6 (3) are the same identity and are merged into (7.1).
- **Infinite products and Euler products**: the convergence arguments repeated in P1, P3, P4 and P5 are merged into Lemmas 2.3 and 2.4.
- **Root-count bounds**: P5 (1) and P6 (6) are merged into Lemma 2.7.

## 4. Editorial completions and choices (no change to statements)

1. Lemma 2.3(a): the convergence of the partial products is proved by a Cauchy argument. P5 only bounded the tails; P5 review v1-0 flagged this as cosmetic and trivially fillable.
2. Propositions 3.2(b), 3.3 and Lemma 6.2: the text states explicitly that λ, γ², λβ are c² times multiplicative functions (λ(1) = c²) before taking Euler products. The archive's "absolutely convergent multiplicative series" is the same argument.
3. Lemma 6.3: the bound |w(y)| ≤ U/y ≤ U/z is made explicit (P4 review v1-0, cosmetic).
4. Proposition 5.1: the unused remark about √x terms is dropped (P3 review v1-0, cosmetic). The proposition is stated in P3's stronger proved form (absolute constant, x^{4/5}). The archived contract form C(ε)x^{4/5+ε} is recorded as a consequence. The circle-method cutoff mentioned in the P3 contract is "permitted" and is not used by the proof; the text says so.
5. P3 lists P1 as a dependency, but the proof does not use it (assembly report Opus, cosmetic). The manuscript notes only that P3 is self-contained.
6. Lemma 9.1 uses P3's proved bound x^{4/5} (no ε) and obtains x^{9/5} log(2x) in place of P7's x^{9/5+δ} log(2x). The final error terms are unchanged.
7. Proposition 6.4 keeps the archived error 𝒜 with (log 2R)² factors, although Proposition 3.2(d) (P1) proves the bounds for 𝒯, 𝒩 without logarithms, as P1's proof notes.
8. Proposition 7.2(b): for fixed σ the bound is exp(E_H(σ)) with E_H(σ) = Σ_p sup|M_p−1|. This is P5 (12)–(13) without the explicit term list. In (b) the bound |α_p − 1| ≤ 2p^{-2} is used, which follows from (7.4); P5 used 2p^{-2}+C₀p^{-3} (P5's C₀, written C_ρ here).
9. Lemma 8.3 (uniform bound for H_f on −5/8 ≤ Re s ≤ 2): this is the argument of P6 (6)–(9), written with α_p, β_p, δ_p. The term-by-term bookkeeping gives |M_p − 1| ≤ (4+4d)p^{-3/2} and M_H = e^{8(1+d)}∏_{p∈𝓑}(1+p^{-3/4})(1+p^{5/8}+p^{5/4}), in place of P6's (6+17d)p^{-3/2} and its U_p. Each inequality was re-verified; the structure and conclusion are those of P6.
10. Chapter 8: the holomorphy of ζ in the strip is taken from Lemma 7.1(b) (P5's continuation) instead of being deduced from MV Cor. 10.4 as in P6 §1. Cor. 10.5 is still quoted, and Cor. 10.4 is mentioned as its origin. The introduction says that two results are quoted (BGPVW Lemma 2.2, MV Cor. 10.5).
11. Lemma 8.4: the bound on the horizontal segments is stated as O_v(T^{-3}). P6 review v1-0 noted, as cosmetic, that the bound for |v^z| was not written out.
12. Chapter 9 keeps the hypothesis 0<ε<η_d/2 of the statement and adds a remark that the argument does not use it (P7 review v1-0, cosmetic).
13. Prose: background (Chapter 1) on Vaughan's theorem (k=2 case of Vaughan 2005, (1.13)–(1.15)), on Brüdern–Wooley and on the Goldston–Vaughan method is taken from the introductions of the supplied papers. Mirsky (1949) is cited from the bibliography candidate list as background for correlations of squarefree numbers; its content was not checked.

## 5. Material added while preparing the write-up

- **Remark 1.4 (consistency with Vaughan's constant).** For ρ ≡ 1 (f(t)=t+1) each local factor of (1.10) equals (1−p^{-2})² times the local factor of Vaughan's C₁ (Vaughan 2005, (1.15), k=2). This was verified symbolically with sympy, treating √p as a variable. Hence K_{t+1} = c₂. The numerical values are computed by `reproduce.py` (Table 10.1, `reproduction.json` → `vaughan_c2`). The remark is only a consistency check, not part of the proof.
- **Truncation bound for K_f (Chapter 10).** K_f is evaluated as ζ(2)^{-3}∏M_p(−½)(1−p^{-2})^{-3}. The bound |M_p(−½) − 1| ≤ 10p^{-2} (p ≥ 5, ρ ≤ 3) uses the explicit expansion displayed in §10.2, which was checked with sympy. The resulting relative bound is e^{15/N} − 1. The Opus integration report used a similar bound (15/p², for the unnormalised factors).
- **Numerical checks in Chapter 10**: D_f(3) vs ζ(3)P_f(3); the normalised remainder of Θ_f (Table 10.3); the comparison of data with the profile x²F_f(x/Y) (Table 10.4, Figures 10.1–10.2); and the snapshot extrapolation applied to the exact profile (Table 10.5). The last two analyses appear in the Opus integration report, where they were done with scripts that are not archived. They were re-implemented in `reproduce.py`, and all values in the manuscript come from that script. Most reproduced values agree with those quoted in the Opus integration report: the fitted profile intercepts 0.134364, 0.135793, 0.141685, and the deviation ranges at x = 2.56·10^8 (+0.007 % to +0.10 % for t²+1, −0.02 % to +2.2 % for t³+2). **Three statements of that report, and one figure of the plan, disagree with the recomputation** (`reproduction.json` → `profile_comparison`, `deviation_trends`):
  - The report says the cubic deviation is "decreasing at 7 of 9 ratios" from x = 1.28·10^8 to 2.56·10^8. The recomputation gives 8 of 9 in absolute value. The exception is the diagnostic ratio r = 0.005 (1.8175 % → 2.2083 %). At r = 0.02 the deviation changes sign (0.5075 % → −0.0203 %). The manuscript (§10.3) follows the recomputation and says "decreased in absolute value".
  - The report gives y = 86–635 for the cubic. At x = 2.56·10^8 the recomputed range is 108–634: y(r=1) = 634, because 635³ + 2 > 2.56·10^8. The value 86 is y at x = 1.28·10^8, r = 0.005. The manuscript uses 108–634.
  - The report gives "≤ 0.0005 %" for 2t+1. The recomputed maximum of |N_data/N_pred − 1| at x = 2.56·10^8 is 0.000534 % (at r = 0.02), so that bound is slightly too small. The manuscript states "within 0.00054 %" (revision 4).
  - The plan's "Numerics check" (`source/plan.md`, line 13) quotes maximum relative profile differences over the eight target ratios of approximately 0.071 %, 0.90 % and 0.00075 % for t²+1, t³+2 and 2t+1. The recomputation gives 0.0701 % and 0.893 % for the first two, which agree to the stated precision, but 0.000534 % for 2t+1, not 0.00075 %. The manuscript does not quote the plan's figures.
  The report's and plan's scripts are not archived, so the cause of these discrepancies cannot be determined. They do not affect the proof.
- **Decomposition of the extrapolation offset (revision 3).** Table 10.5 and §10.4 split C_data − K_f into (C_data − C_prof) + (C_prof − K_f), computed by `reproduce.py` (`reproduction.json` → `extrapolation.*.decomposition`). The split was requested by the codex:gpt-6.1-sol review of revision 2. It replaces the earlier claim that the whole gap is a model bias. That claim was wrong for t³+2, where C_data − C_prof ≈ 0.00053 exceeds C_prof − K_f ≈ 0.00019.
- **Reproduction of the snapshot**: `reproduce.py` reruns the archived snapshot code. In the run used for this document, all 270 rows (3 polynomials × 90 rows, including the diagnostic ratio) agreed exactly with the archived `results.json`.

## 6. Items checked and left unchanged

- The quotations of BGPVW Lemma 2.2, (2.6), (2.7) (P2) and of MV Corollaries 10.4–10.5 (P6) were compared with the supplied PDFs and match.
- Every proof was re-read step by step while writing. The writer found no gap, sign error, range error or missing uniformity, so no `SOURCE_GAP.md` was written.
- Remark 1.4 and (1.1)–(1.2): Vaughan's (1.13)–(1.15) were re-checked against a rendered page of the supplied `papers/vaughan-2005.pdf` (pp. 574–575) in revision 2.

## 7. Revision history

### Revision 2 (response to `build-feedback.txt`)

The build feedback reported: *"referee modified review inputs:
`manuscript/build/snapshot/report.md`"*. Cause: revision 1 of `reproduce.py`
copied the snapshot code into `manuscript/build/snapshot/` and ran it there, so
the snapshot's own outputs (`report.md`, `results.json`, `run_*.json`, the
compiled `counts` binary) were rewritten inside `manuscript/` on every run,
overwriting files that were part of the submitted manuscript directory.

Changes:

- `reproduce.py` now runs the unchanged snapshot code in a fresh temporary
  directory created with Python's `tempfile` and deletes it afterwards. An
  optional `--build-dir DIR` keeps the build for `--reuse`; the script refuses
  any build directory inside `manuscript/`. Inside `manuscript/` the script
  writes only `generated/*` and `reproduction.json`, the files listed in
  `reproduction.json → artifacts` plus that file itself. The computation is
  unchanged.
- The stale scratch directory `manuscript/build/` from revision 1 was deleted.
- `README.md` and the `reproduction.json` field `snapshot.how` describe the new
  build location; the description of the `build/` directory was removed.
- Editorial: in (1.2) the numerator term `p³+2p³` of Vaughan's C₁ at k = 2 is
  written `3p³`, with a note that it is `p^{2k−1}+2p^{k+1}` at k = 2. The value
  is unchanged.
- No mathematical statement, proof, hypothesis, range or error term was
  changed.

### Revision 3 (response to `feedback/0.json` and `feedback/1.json`)

Both reviews found no source gap and no problem with the statements or
proofs. Every objection was addressed; no mathematical statement, hypothesis,
range, error term or proof step was changed.

`feedback/0.json` (claude-opus-5-5):

1. *Harness commit misstated.* Appendix B now lists the archive commit
   `867fc9b…`, the harness commit `552a8f01…` and the revision `fc217220…`
   recorded in every model record of `provenance.json` separately. The false
   remark "the harness commit is the same" is removed.
2. *Hint provenance.* Appendix B now records the fact from
   `source/interventions.md` (2026-11-03 23:27) that the owner authorised the
   operator to read the owner's (otherwise excluded) master's thesis in order
   to write the hint, and that the label `thesis-plan` reflects this. Nothing
   about the thesis's content is stated.
3. *Appendix cross-references printed as "Chapter A/B".* `main.tex` adds
   `\crefalias{chapter}{appendix}` after `\appendix`. References now print
   "Appendix A/B".
4. *Attribution of Remark 9.2.* The remark now states only the mathematical
   fact. The correct source (P7 review v1-0, cosmetic) is recorded in §1
   above.
5. *Discrepancy with the Opus integration report (7 vs 8 of 9 ratios; y
   range).* Recorded in §5. §10.3 says "decreased in absolute value" and
   mentions the sign change at r = 0.02 and the exception r = 0.005. The
   counts, ratio lists and y range are generated macros (`\NdecThree`,
   `\NcmpThree`, `\NondecThree`, `\SignchThree`, `\YminThree`,
   `\YmaxThree`).
6. *"At every ratio" for t²+1.* Changed to "at every target ratio", with the
   generated minimum decrease factor `\DecfacTwo` (at least 18). A note says
   that r = 0.005 is computed only at the two largest x.
7. *"Visibly approaches −K_f" (Table 10.3).* Replaced by "close to −K_f,
   consistent with this error term", with a note that the distance to −K_f
   grows slightly from H = 10⁴ to 10⁵ for t²+1 and 2t+1.
8. *Notation clash in §1.1.* Warlimont's profile is now written
   𝓕(u) ~ c₂u^{−3/2}, with c₂ the constant of (1.2) (Vaughan 2005, (1.10)–(1.11),
   where the constant is c_k at k = 2). The range 1 ≤ Y ≤ x of (1.10) is stated.
9. *Typography.* The bound for 2t+1 is the unsigned `\DevabsLin` ("to within
   0.0005 % in absolute value"; corrected to 0.00054 % in revision 4). The
   integers y in the text macros use digit grouping (`grouped()` in
   `reproduce.py`); the y column of Table 10.4 did not until revision 4. The proved relative error sizes x^{−1/11}, x^{−1/7} are
   generated macros (`\ErrrelThree`, `\ErrrelTwo`).
   Appendix A captions now state the quantity, the polynomial and the table
   layout (also requested under "layout_checks").

`feedback/1.json` (codex:gpt-6.1-sol):

1. *Remark 1.3 overstated the asymptotic range.* The remark now requires, in
   addition to Y/x → 0, that the additive error x^{2−η_d+ε} be o(x^{1/2}Y^{3/2}),
   for instance in the range of Corollary 1.2. It says that the theorem gives no
   asymptotic formula for smaller Y. The fixed-ratio factor is written as
   F_f(1/r)r^{−3/2}/K_f = 1 + O(r^{1/8}), independent of x and not shown to
   equal one. §1.4 is adjusted accordingly.
2. *O(r^{1/8}) is a bound, not the order of the correction.* §10.4 now says
   this explicitly. The failure of the fit model to reproduce the limit is
   described as an empirical observation about the computed profile.
3. *Data-intercept gap is not all fitting bias.* §10.4 and Table 10.5 report
   the two contributions separately (macros `\Cdiff*`, `\Cbias*`). For t³+2
   the data–profile term dominates. See also §5.
4. *Fixed-ratio standard error mislabelled as OLS.* The caption of Table 10.6,
   the artifact description of `generated/tab_fits.tex` and
   `reproduction.json → uncertainty_note` now state that this is the standard
   error of the mean of the eight ratio-specific slopes (sample standard
   deviation / √8), as computed in the snapshot's `compute.py` (line 191).
   Only the fixed-x and joint fits carry formal OLS standard errors.
5. *Bibliography suppressed DOIs.* The style is now `plainurl` (urlbst, in the
   supplied TeX Live), which prints the DOI fields as links. The `url` fields,
   which only repeated `https://doi.org/<doi>`, were removed to avoid printing
   each link twice. Entries and DOIs are otherwise unchanged; the README's
   caveats about unverified DOIs still apply.
6. *Workflow notes inside the proof.* The sentence in §9.3 about the
   integration reports and the status of Corollary 1.2 moved to Appendix B
   ("Status of the evidence"). The attribution in Remark 9.2 moved to this
   file (item 4 above).

Other changes in this revision: §10.4 is labelled `sec:extrapolation`, and
`reproduction.json` gains `deviation_trends` and
`extrapolation.*.decomposition`. `reproduce.py` was rerun on the full grid;
see `reproduce.log`.

### Revision 4 (response to `feedback/0.json` and `feedback/1.json`)

Both reviews found no source gap and confirmed the statements, dependencies,
numerics, citations and provenance. Every objection was addressed; no
mathematical statement, hypothesis, range, error term or proof step was
changed.

`feedback/0.json` (claude-opus-5-5):

1. *2t+1 bound understated by rounding.* §10.3 said "within 0.0005 %", but the
   maximum is 0.000534 %. `reproduce.py` now rounds the bound `\DevabsLin` up
   to two significant digits (`ceil_sig()`), giving "within 0.00054 %". For the
   same reason the "between" bounds `\DevminTwo`, `\DevmaxTwo`,
   `\DevminThree`, `\DevmaxThree` are now rounded outwards (`round_out()`),
   e.g. +0.1018 % instead of +0.1017 % for the largest t²+1 deviation
   (0.101726 %). A sentence in §10.3 says that these bounds are rounded
   outwards and may differ from Table 10.4 in the last digit. §5 above and
   revision 3, item 9 were corrected.
2. *Table 10.4 y column ungrouped.* The y column now uses `grouped()`
   (e.g. 127,999,999). Revision 3, item 9 above now says what was actually done
   then.
3. *PDF bookmark of §9.3.* The heading uses
   `\texorpdfstring{Proof of \cref{cor:range}}{Proof of Corollary 1.2}`.
4. *Table 10.5 header.* The "decomposition" rule now spans only the two
   decomposition columns (C_data − C_prof, C_prof − K_f). The last column
   K_f/C_data − 1 has its own heading "relative gap".
5. *Misleading `mpmath_dps` in `reproduction.json`.* The field
   `parameters.mpmath_dps` is replaced by `parameters.precision`. It records
   the decimal precision of the snapshot's V computation (70 digits), the
   mpmath precision actually in force (85 digits, set globally by the
   snapshot's `compute.py` on import) and what it is used for, and that the
   theoretical constants are computed in double precision. The ineffective
   `mp.mp.dps = 40` in `reproduce.py` was removed; since it was always
   overridden before any mpmath call, no value changes.
6. *Snapshot attribution in Appendix B.* Appendix B now says that
   `codex-gpt-6.1-sol` is the candidate label in the snapshot's acceptance
   record, not one of the model records of `provenance.json`, and that no tool
   version is recorded for the numerics stage.
7. *Plan's 0.00075 % for 2t+1.* Recorded in §5 above, together with the Opus
   report's "≤ 0.0005 %".

`feedback/1.json` (codex:gpt-6.1-sol):

1. *Remark 6.6 (after the proof of Proposition 6.4).* The remark said that the sampling error
   x²Z^{−1/d}R^{1/2}(log 2R)² is small only when Z^{1/d} is large compared with
   R. The correct comparison is with R^{1/2}(log 2R)². The remark now says
   this, states the complementary requirement of the tail term, and says that
   R = Z^{1/d} makes both terms Z^{−1/(2d)} up to logarithms. Proposition 6.4
   and Chapter 9 are unchanged.

`reproduce.py` was rerun on the full grid for this revision; see
`reproduce.log`.


### Revision 5 (response to `feedback/0.json` and `feedback/1.json`)

`feedback/1.json` (codex:gpt-6.1-sol) gave the verdict "pass" with no issues.
`feedback/0.json` (claude-opus-5-5) gave "revise" with four minor items and
found no mathematical error and no source gap. All four items were addressed.
No mathematical statement, hypothesis, range, error term, constant value or
proof step was changed; only symbols were renamed.

1. *C₀ clash.* Lemma 2.7 and Chapter 7 ((7.4), proof of Proposition 7.2(b),
   (d)) now write C_ρ = max{d,|A_d|}. C₀ denotes only the absolute constant
   10/3 of Proposition 3.2(d), which is the one used in the proof of
   Proposition 6.4 and in C(f) = C₀·max{…}. See §2.
2. *δ_p clash.* The averaged local density of Chapter 6 ((6.2), Lemmas 6.1,
   6.2) is now ϑ_p(h). δ_p is used only for the local coefficient (7.3) of
   Chapters 7–8. See §2.
3. *η in Lemma 7.1(b).* The real abscissa in the holomorphy argument is now
   σ₀ (Re w ≥ σ₀ > −1). See §2.
4. *README runtime.* The README no longer says "11–14 minutes" (nor the
   unverified "roughly 5 GB … on an Apple M2 Pro"). It quotes the recorded
   914 s (910 s for the snapshot pipeline) of the full run preceding this
   revision, points to `reproduction.json → total_runtime_seconds` for each
   run's own time, and says that peak memory was not recorded, giving only the
   size of the largest transform array (2^29 32-bit entries, 2 GiB, from
   `counts.cpp`).

`reproduce.py` and the generated files were not changed in this revision.
