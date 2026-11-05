# Changes: from the archived run to the manuscript

This file maps every result in `main.tex` to its source in the archived run
(`source/`), records the two referee reports for each proposition, and lists
every notation change, merged argument, correction and addition.

Archive: `source/` (archive label `zt-neutral`, archive commit
`ed0aebaf461b602601856bf1b693fd76893d9aba`); selected plan
`simplest@claude-opus-5-5` (`source/plan.md`, `source/plan.json`).
For every proposition PN, `source/props/PN/review-v1-0.json` is the review by
`claude-opus-5-5` and `source/props/PN/review-v1-1.json` the review by
`codex:gpt-6.1-sol`. Both reviewers passed all nine propositions in round 1
(severities: none or cosmetic). The assembly/integration reports are
`source/report/assembly-claude-opus-5-5.md`,
`source/report/assembly-codex-gpt-6.1-sol.md`,
`source/report/integration-*.json` and `source/report/integration.json`.

The theorem is stated with exactly the strength, ranges, hypotheses and
error terms of the plan's main theorem and of P9. The weight `f'(k)` and the
class of `f` are unchanged. No proposition is used outside its stated range.
No mathematical change was made beyond the local corrections listed in §4.
Each is tagged in §4 by its origin:

* **(a)** recorded in the operator audit (`source/interventions.md`,
  2026-11-03 10:21, and Markus's 2026-11-03 "result" entry: P1(iii)
  normalisation/convergence wording, P8 endpoint explanation, unused P6/P8
  numerical notes);
* **(b)** raised by the run's own referees (`source/props/PN/review-v1-*.json`),
  all cosmetic;
* **(c)** raised at the write-up stage, by the writer or by the write-up
  referees (`claude-opus-5-5`, `codex:gpt-6.1-sol`). These are not covered by
  the recorded audit.

None of them weakens a statement or changes the main theorem. A few auxiliary
statements are stated slightly more strongly or more explicitly than in the
archived statement files; each such case is taken from the archived proof or
proved in full in the manuscript, and is listed in §4a. One archived
auxiliary statement, the infinite-interval clause of the Euler–Maclaurin
lemma in the P5 proof (Lemma 2.6), is stated more precisely: its hypotheses
are kept exactly, and its conclusion is stated in the form that is true under
them (§4, item 19). No decision by Markus on this point is recorded in the
supplied material; it is listed for his attention in §10.

**Feedback files.** The write-up was refereed in three rounds by
`claude-opus-5-5` and `codex:gpt-6.1-sol`. Only the round-3 review files are
in this workspace: `feedback/0.json` (`claude-opus-5-5`, verdict pass) and
`feedback/1.json` (`codex:gpt-6.1-sol`, verdict revise), both reviewing the
previous version (manuscript hash `79e72fca…`). They are answered in §9. The
round-1 and round-2 review files are historical and are **not** in this
package. §7 and §8, and every mention of a round-1 or round-2 objection
elsewhere in this file, are the writer's own summaries, written when those
reviews were answered. They cannot be checked against the original files
here. Wherever the content of such an objection matters, it is stated inline.

## 1. Map of results

| Manuscript | Archived statement / proof | Reviews |
|---|---|---|
| Theorem 1.1 (i), (ii), (iii) | `plan.md` "Main theorem"; `props/P9/statement.md`, `props/P9/proof.md`; composition audited in both assembly reports | P9: `review-v1-0.json` (Opus, pass, none), `review-v1-1.json` (Sol, pass, none) |
| Theorem 1.1, positivity of C_f | `props/P8/statement.md` claim (0) | see P8 |
| Remark 1.2 (range) | `plan.md` "Range" paragraph; assembly reports §5 (Opus) and §4 (Sol) | — |
| Remark 1.3 (C_t = Vaughan's c_2) | `plan.md` consistency check 1; Opus assembly report §3 | — (numerical in the run; see §5 below) |
| Lemma 2.1 (tail bound) | P3 proof Step 0 `(*)`; also P1 proof (i), P4 proof (0), P5 proof (c) | P1, P3, P4, P5 |
| Lemma 2.2 (residue-class count) | P1 proof (i) (`source/props/P1/proof.md` line 14); P3 proof Step 2 (line 33) | P1, P3 |
| Lemma 2.3 (divisor bounds) | standard facts used in P3, P5(c), P8 §3.2–3.3; MV (2.20) as cited by the Sol referee of P3 | P3, P5, P8 |
| Euler products (2.1) | used throughout P1, P3, P5, P8; cited as MV Theorem 1.9 | — |
| Lemma 2.4 (η, κ, A_0) | P1(v) and its proof; P2 notation (absolute convergence of MT); P6 proof Step 0 | P1, P2, P6 |
| Lemma 2.5 (coprime pairs) | P1 proof (iv) (the product I(t)) and P3 proof Step 4 | P1, P3 |
| Lemma 2.6 (Euler–Maclaurin) | P5 proof §0, Lemma EM (`source/props/P5/proof.md` lines 9–11); conclusion of the b = ∞ clause stated precisely, archived hypotheses unchanged, see §4 item 19 | P5 |
| Proposition 3.1 | P1 (i)–(v) | P1: Opus pass/none; Sol pass/cosmetic |
| Lemma 3.2 | P4 proof (ii) Step 3, estimate (3) for all y > 0 (`source/props/P4/proof.md` lines 33–48); P4 proof (i) (line 13) is its case r = 1 | P4 |
| Proposition 3.3 | P4 (i), (ii); explicit c_0 from P4 proof "Conclusion" (line 68) | P4: Opus pass/none; Sol pass/none |
| Proposition 4.1 | P2 | P2: Opus pass/none; Sol pass/none |
| Proposition 5.1 | P3 | P3: Opus pass/cosmetic; Sol pass/none |
| Proposition 6.1 (a)–(c) | P5 (a)–(c); explicit c_1 = 60 from P5 proof (b) (line 37) | P5: Opus pass/none; Sol pass/none |
| Proposition 6.2 | P6; range x > 0, q ≥ 1 from P6 proof Step 2 (line 50) and "Conclusion" (line 71) | P6: Opus pass/none; Sol pass/cosmetic |
| Proposition 7.1 | P7 | P7: Opus pass/none; Sol pass/none |
| Proposition 8.1 (0), (a)–(c) | P8 | P8: Opus pass/cosmetic; Sol pass/cosmetic |
| Lemma 8.2 (local factors) | P8 proof §0 "Elementary identities" | P8 |
| Lemma 8.3 (root counts) | P8 proof §0 "The function ρ" | P8 |
| Lemma 8.4 (shape of F) | P8 proof §0 "Shape of F" | P8 |
| Lemma 8.5 (monotone weights) | P8 proof §3.4 "Lemma" | P8 |
| Section 9 | P9 proof §0–§3 | P9 |
| Section 10 | `source/numerics/` (accepted snapshot `snapshot-nu6pbkr4`, candidate `codex-gpt-6.1-sol`), assembly reports §3–§4 (Opus) and §6 (Sol); recomputed by `manuscript/reproduce.py` | — |
| Appendix B | `provenance.json`, `source/interventions.md` | — |

## 2. Notation changes

| Archived | Manuscript | Reason |
|---|---|---|
| `tau_p` (local factor of C_f; plan, P8, P9, reports) | `σ_p` | `τ(n)` is the divisor function (P3, P8) |
| `c_0 = -4ζ(-1/2)` (P8 proof) | `I` (as in P5) | one name for one constant; `c_0` is now the absolute constant `3e^{2ζ(3/2)}` of P4 |
| `A_p, B_p, D_p` (P8 proof) | `a_p, b_p, c_p` (as in the Sol assembly report) | `B` is the sawtooth function |
| `A = ∏ A_p`, `b(q)`, `u = b*μ` (P8 proof) | `A_h`, `h^♮(q)`, `w = μ*h^♮` | avoid clashes with `A(m)`, `b_p` and P5's `b` |
| `c_1, c_2, c_3, c_5` (P8 shape constants), `C_1 = ∏_{p∈P_0} p^2`, truncation parameter `E` | `γ_1, …, γ_4`, `C_P`, `W` | avoid clashes with `c_1 = 60` (P5), `C_1` (Vaughan) and `E(x;q,l)` |
| `δ_q` (P5) | `Δ_q` | `δ` is the range parameter of the theorem |
| `f(t) = κ(t)1[(t,q)=1]`, `b = μ*f` (P5(c) proof) | `κ_q(t)`, `β = μ*κ_q` (the plan's name) | `f` is the polynomial |
| `A(u)`, `E_1, …, E_5` (P5(b) proof) | `Φ(u)`, `R_1, …, R_5` | `A(m)`, `E(x;q,l)` |
| `t = t_1 t_2 t_3`, `Z(t_2)` (P6 proof) | `t = t_0 t_1 t_2` (subscript = min(v_p(q), 2)), `Z_1` | mnemonic indexing |
| local `h(p)` (P1 proof (iii)) | `u(p)` | `h(q)` is the main-term function |
| `κ_r` (P4 proof) | `ν_r` | `κ(t)` |
| `E_1, E_2, E_3` (P3 proof) | `𝓔_1, 𝓔_2, 𝓔_3` | `E(x;q,l)` |
| generic `c(ε)` in P3, P5, P6, P7, P8 | `c_3(ε)`, `c_5(ε)`, `c_6(ε)`, `c_7(ε)`, `c_8(f), c_8(f,ε)` | to compose constants explicitly in §7 and §9 |
| Vaughan's modulus bound `Q` in `V(x,Q)` (Vaughan 2005, quoted in §1.2) | `Y`, so `V(x,Y)` | `Q(x)` and `Q(x;q,l)` are the counting functions (write-up referee, round 1) |
| actual ratio `ratio_actual` (snapshot) | `ϱ = f(y)/x` (§10.5) | distinguish from the target ratio `r` |

## 3. Merged arguments

* **Tail bound** `Σ_{a>w} a^{-2} ≤ 2/w`: proved four times in the archive (P1 (i),
  P3 `(*)`, P4 (0), P5 (c)); stated once as Lemma 2.1 (P3's version, valid for all w > 0).
* **Counting integers in a residue class** (`N/L + θ`): P1 (i) and P3 Step 2 →
  Lemma 2.2.
* **Coprime pairs of squarefree numbers**: the Euler product
  `Σ μ(a)μ(b)/(ab)^2 = ∏_{p∤e}(1-2/p^2)` was derived twice by "local choices"
  (P1 proof (iv), P3 proof Step 4). Lemma 2.5 states it once. Its proof groups
  the pairs by n = ab, which turns the sum into the multiplicative series
  `Σ μ(n)2^{ω(n)} n^{-2} 1[(n,e)=1]`. This is the same computation in a
  shorter form.
* **Squarefree numbers coprime to r**: P4 (i) (count of Q(x)) and P4 (ii) Step 3
  (count of T_r) are the same estimate; Lemma 3.2 proves the general case, and
  Proposition 3.3(i) is its case r = 1. The constant `3√x` of P4 (i) is unchanged.
* **Facts on η, κ, A_0** scattered over P1, P2, P6 → Lemma 2.4.

## 4. Corrections (all local; no weakening of any statement)

1. [a] **P1(iii), normalisation** (Sol review of P1, "other issues"; operator audit).
   The proof states `q·μ(d) g_d/d²·1[g_d | n] = ∏_{p|d} h(p)`, with an
   extraneous factor q. Corrected in Proposition 3.1(iii): `μ(d) g_d/d² 1[g_d|n]
   = ∏_{p|d} u(p)` and `q g(q,n) = Σ_d μ²(d) ∏_{p|d} u(p)`.
2. [a] **P1(iii), convergence** (Sol review of P1, main objection, cosmetic;
   operator audit). The claim `Σ_p |h(p)| ≤ Σ_p p^{-2}` is false for p | q
   (e.g. q = n = 2). Corrected: `|u(p)| = p^{-2}` for p ∤ q, and `|u(p)| ≤ 1` for
   the finitely many p | q, so the series converges absolutely.
3. [b] **P3 Step 3, constant** (Opus review of P3). The proof writes
   `2·(π²/6)·Σ e^{-2}(2e/z) ≤ (4π²/(3z)) Σ 1/e`; the left side equals
   `(2π²/(3z)) Σ 1/e`. The original inequality was true but overestimated by a factor 2. The manuscript uses
   the correct value and the bound `7τ(m)/z` instead of `14τ(m)/z`. The final
   constant `(3 + 9C(ε))` replaces `2(1+τ*) + 1 + 14τ*`. Statement unchanged.
4. [a] **P8 §3.4, endpoint k = 1** (Opus review of P8, cosmetic; operator audit;
   flagged as "P8 endpoint clarification" in `interventions.md`). The proof
   treats the closed first interval `[1, β]` as `(1-δ, β]`. That needs F to be defined and
   monotone left of 1, which fails e.g. for f = 3t − 1. Corrected by stating
   the counting lemma (Lemma 8.5) for arbitrary intervals (open, closed or
   half-open). Its proof only uses that `k_1 − e` and `k_n + e` lie outside the
   interval. The closed interval `[1, β]` is then covered directly, and the constant
   `3(2d−1) ≤ 6d` in eq. (8.10) (source eq. (3.9)) is unchanged.
5. [b] **P8 §3.5, implicit error term** (Opus review of P8). The source writes
   `O(Y^{3/2} y^{-1/2})` for the term `(2/3)(Y^{3/2} − f(1)^{3/2})·O(y^{-1/2})`
   without saying where it comes from. The assembly display in §8.3 now shows
   it. The short-sum bound keeps the factor `(1 + log W)` (P8 (3.6)) explicitly,
   and it is absorbed by the choice `ε ≤ 1/8` (the source absorbs it into
   `E^{2ε}`). The final bound is unchanged.
6. [b] **P8 §3.2(ii), constant dependence** (Opus review of P8). The bound
   `(2d)^{ω(n)} ≤ C n^ε` has a constant depending on d; this is now stated
   (`C(f, ε)`).
7. [b] **P2, wording** (Opus review of P2). The parenthetical after (3) ("finitely
   many nonzero terms after the bracket is rewritten") is replaced by: the
   bracket vanishes for `q m_t(q) > x` (twice an empty sum), and each of the
   three series obtained by splitting it converges absolutely.
8. [b] **P4 (i), wording** (Opus review of P4). "Every squarefree-indicator
   identity gives" → derived from `μ²(n) = Σ_{d²|n} μ(d)` (Lemma 3.2).
9. [b] **P5(b), small s** (Opus review of P5). The two quantities both lie in
   `[0, Λ/4]`, so their difference is at most `Λ/4` (source: `Λ/2`). The constant
   `c_1 = 60` is kept.
10. [b] **P9, real-variable hypothesis** (Opus review of P9). The step
    `f(k) ≤ f(y)` for real y uses `f'(t) ≥ 1` for all real `t ≥ 1`. This is
    now explicit in (1.1) and in §9. The convention `1 ≤ k ≤ y` (integers) is
    explicit in (1.2). The constants `c(ε/3)`, `c(f, ε/3)` and their
    combination are written out in §9.
11. [b] **P9 remark on δ < 1/9** (Opus review of P9). Non-emptiness of the range
    holds for x > 1; stated so.
12. [b] **P7, role of x ≥ 2** (Opus review of P7). Noted in the proof of
    Proposition 7.1 that x ≥ 2 is needed only for P3.
13. [b] **P3, n ≥ 1** (Opus review of P3). C_x(m) counts positive n; explicit in
    eq. (4.1).
14. [b] **P1(iii), sign of n** (Opus review of P1). Stated for squarefree `n ∈ ℕ`,
    the only case used.
15. [b] **P5, citation "MV Thm B.5"** (Opus review of P5: not found in the
    supplied PDF). Appendix B of Montgomery–Vaughan is not in the supplied
    corpus. Its §1.3 refers to "Theorem B.5" for Euler–Maclaurin summation.
    The manuscript proves Lemma 2.6 directly and cites only MV §1.3 and
    Theorem 1.12 for comparison.
16. [a/b] **Unused numerical notes in the proofs** (not reproduced):
    * P2: the proof's check agreed only to ~1e-3 because of truncation (Opus
      review); replaced by the exact self-test in `reproduce.py`
      (`identity_selftest`, agreement 4.8e-10).
    * P6: the tail estimate `A_0 x/(q·3000)` wrongly contains 1/q (Sol review),
      and the difference 92 at (10^6, 1) is a truncation artefact (Opus review).
    * P8: "ρ(p²) ≈ ρ(p)/p, exact for these squarefree f" is false for root
      counts (should be ρ(p²) = ρ(p) for unramified p); Sol review and Sol
      assembly report §5. Also flagged in the operator audit.
    * P1, P5: numerical sanity checks are not reproduced; P5's constants were
      checked by the referees.

    (The P6 and P8 notes are group (a); the P2 note is group (b).)
17. [c] **Remark 1.2 (range of part (ii))**. The plan says statement (a)/(ii)
    "remains meaningful up to f(y) ~ x". The manuscript states only what is
    proved: the error term of (ii) is of smaller order than `x^{1/2}Y^{3/2}`
    for `x^{7/9+δ} ≤ Y ≤ x`. No lower bound for `Σ f'(k) MT(x; f(k))` is
    claimed.
18. [c] **References.** P8's "Hooley 1964 (background on rho only; not needed)" is
    dropped because no statement from it is used. The plan named a 1949 paper
    of Mirsky on pairs of squarefree numbers from memory. Earlier versions of
    this write-up cited Mirsky, Bull. AMS 55 (1949), from
    `bibliography-candidates.json`, without having consulted it. The round-1
    write-up referee `claude-opus-5-5` objected that this citation could not be
    checked against the supplied material, so the unverifiable historical
    attribution is dropped. Section 5 now quotes only what the
    supplied BGPVW (1998, §1) says about the related additive problem (see §5).
19. [c] **Lemma 2.6 / P5 Lemma EM, the case b = ∞.** *Archived text* (P5
    proof line 11): "If b = ∞ and F, F' → 0, F'' ∈ L^1, the same holds with the
    terms at b dropped." *Problem:* read as an identity between a convergent
    series `Σ_{n>a} F(n)` and a convergent integral `∫_a^∞ F`, this is false in
    that generality: `G(u) = cos(log u)/u` on `[1, ∞)` has `G, G' → 0` and
    `G'' = O(u^{-3}) ∈ L^1`, but `∫_1^X G = sin(log X)` has no limit as X → ∞
    (raised by the write-up referee `codex:gpt-6.1-sol` in round 1; confirmed
    by both round-3 referees, `feedback/0.json` and `feedback/1.json`).
    *History in this write-up:* rounds 2–3 added the hypothesis "`∫_a^∞ G`
    converges" to Lemma 2.6 and flagged it for Markus's acknowledgement. The
    round-3 referee `codex:gpt-6.1-sol` asked for Markus's decision before
    that change could be treated as accepted (`feedback/1.json`, issue 1). The
    supplied material records no such decision: there is no `brief.md`, and
    `source/interventions.md` has no entry on it. *Present version (round 4):*
    the added hypothesis has been removed. Lemma 2.6 now has exactly the
    archived hypotheses (`G ∈ C²[a, ∞)`, `G, G' → 0`, `G'' ∈ L^1`). Its
    conclusion is the statement that letting b → ∞ in the finite formula
    actually gives: `lim_{b→∞}(Σ_{a<n≤b} G(n) − ∫_a^b G)` exists and equals
    `ψ(a)G(a) − ψ_2(a)G'(a) − ∫_a^∞ ψ_2 G''`. In particular, the series
    converges if and only if the integral does, and then the formula holds with
    b = ∞. This is one reading of "the same holds", and under it the archived
    clause is true as stated. The cos(log u)/u example is kept in the proof to
    show why the precise form is needed. The lemma also says explicitly that G
    may be complex-valued, as in the archived application to `u^{-s}`; the
    proof applies to the real and imaginary parts. *Applications:* both
    archived applications have absolutely convergent series and integrals:
    `G(u) = u^{-s}`, `Re s > 1`, in Proposition 6.1(a) (P5 line 23–24, where
    the archive itself evaluates `∫_N^∞ u^{-s} = N^{1-s}/(s−1)`), and
    `Φ(u) = Z/u² − Z²/u⁴` on `(T, ∞)` in Proposition 6.1(b) (P5 line 62: "all
    integrals converge absolutely"). Section 6 now says this at both places.
    No proposition, no step of the P5 argument and no constant changes, so this
    is not a source gap and no `SOURCE_GAP.md` is written. Because it is still
    a write-up-stage choice of how to state an archived lemma, it is listed for
    Markus's attention in §10.
20. [c] **Proposition 6.1(b), arithmetic of the final sum** (write-up referee
    `codex:gpt-6.1-sol`, round 1; objection, stated inline: the sum of the
    bounds for `R_1, …, R_5` is `449Λ/8`, not `< 56.1Λ`). The round-1 manuscript wrote the
    sum of the bounds for `R_1, …, R_5` as `< 56.1Λ`. It equals
    `449/8 Λ = 56.125Λ`. This was an error introduced in the write-up: the
    archived P5 proof (line 65) has the correct bound `< 57Λ`, with the
    decimal approximation "56.1" written as a rounding. Corrected to
    `= 449/8 Λ < 57Λ`. The constant `c_1 = 60` is unchanged.
21. [c] **Remark 6.3, range of the relative-error formula** (write-up referee
    `codex:gpt-6.1-sol`, round 2; that review file is not in this workspace). The remark (write-up
    material, §5) replaced `q^{2ε}` by `x^{2ε}` without stating `q ≤ x`, while
    Proposition 6.2 just above it holds for all `x > 0`. The formula is now
    stated for `x ≥ 1`, `1 ≤ q ≤ x`, with the reason (`q^{2ε} ≤ x^{2ε}`).
    The remark also notes why the restriction is needed: `0 ≤ MT(x;q) ≪ x` by
    (1.7) and Lemma 2.4, so `MT(x;1)/(h(1)√x) → 0` as `x → 0`, while the error
    term tends to 0 for `ε > 1/12`. Proposition 6.2 and the main theorem are
    untouched.

## 4a. Statements stated more explicitly or more strongly than the archived statement files

Each item is either proved in the archived proof (with line reference) or
proved in full in the manuscript. None is used to strengthen the main theorem.
(Identified as unrecorded by the round-1 write-up referee `claude-opus-5-5`,
whose objection was that the manuscript stated some auxiliary results more
strongly than the archived statement files without saying so.)

* **Proposition 6.2 (P6), range.** `source/props/P6/statement.md` states the
  bound for real `x ≥ 1` and integers `1 ≤ q ≤ x`. The manuscript states it
  for all real `x > 0` and all `q ∈ ℕ`, adding "in particular for `x ≥ 1`,
  `1 ≤ q ≤ x`". Source: P6 proof Step 2, line 50 ("No use was made of q ≤ x or
  x ≥ 1 in this step; the error bound holds for all x > 0, q ≥ 1"), and the
  Conclusion, line 71.
* **Proposition 6.1(b) (P5(b)), explicit constant.** The statement file has
  "an absolute constant c_1"; the manuscript states `c_1 = 60`. Source: P5
  proof line 37 ("I show this with c_1 = 60").
* **Proposition 3.3 (P4), explicit constant.** The statement file has "an
  absolute constant c_0"; the manuscript states `c_0 = 3e^{2ζ(3/2)}`. Source: P4
  proof line 68. The manuscript also notes, as in P4 proof line 17, that `q ≤ x`
  is not used in (ii).
* **Lemma 3.2 (P4 Step 3).** `|T_r(y) − ν_r y| ≤ 3·2^{ω(r)} √y` for all `y > 0` is
  P4 proof estimate (3), lines 45–48. Its case `r = 1`, `|Q(y) − 6y/π²| ≤ 3√y`
  for all `y > 0`, extends P4(i) (stated for `x ≥ 1`, line 13) to `0 < y < 1`.
  That case is trivial: `Q(y) = 0` and `6y/π² < 3√y`. It is not used.
* **Lemma 2.2, strict inequality.** P1 proof line 14 and P3 proof line 33 use
  `N/L + θ` with `|θ| ≤ 1`. Lemma 2.2 states and proves `|θ| < 1`. Every use
  needs only `|θ| ≤ 1`.
* **Proposition 5.1 (P3), constant.** `(3 + 9C(ε))` instead of
  `2(1+τ*) + 1 + 14τ*`; see §4 item 3.

## 5. Material added after the run

None of the following is used in a proof.

* **Section 1 background**: Vaughan's theorem for the full variance (2005,
  (1.12)–(1.16)), the earlier `x²𝓕(x/Y)` results it quotes, and the
  Brüdern–Wooley theorem (2011, Theorem in §1), all read from the supplied PDFs.
* **Section 5, first paragraph**: the remark that BGPVW (1998, §1) report an
  elementary argument of Evelyn and Linfoot giving
  `r_k(n) = S_k(n) n + O(n^{2/(k+1)+ε})` for sums of two k-free numbers (read
  from the supplied PDF, p. 3). It is background only.
* **Remark 1.3**: the identity `σ_p|_{ρ≡1} = C_{1,p}(1 − p^{-2})²` of local
  factors. The run checked `C_t = c_2` numerically to 7–8 digits (plan;
  Opus assembly report §3). The write-up verifies the identity symbolically
  with sympy (`reproduce.py`, `symbolic_local_identity`).
* **Section 10** is recomputed from scratch by `manuscript/reproduce.py`:
  * re-run of the accepted snapshot code (unchanged; recompiled), with
    an exact comparison against the archived `results.json` (identical);
  * C_f for k²+1, k³+2, 2k+1 and the formal f = t, with a rigorous bound for
    the omitted primes. This uses the tail argument of the Sol assembly report §6, eq. (21),
    which rests on eq. (8.2), `|σ_p − 1| ≤ (3+2d)/p²`, from P8 §1. The value for 2k+1
    (not compared by either integrator) is new here; the plan quotes 0.14261;
  * new code for `Σ f'(k) MT(x; f(k))` and `Σ F(k) h(f(k))`. The Opus integrator
    did a similar computation with its own code, which is not in the archive.
    The write-up's code evaluates the infinite t-series without truncation (closed-form tails)
    and is checked against the exact identity of Proposition 4.1;
  * the sensitivity table of the snapshot's extrapolation (values from the
    snapshot's own `results.json` fields);
  * (round 2) outward rounding of the printed C_f interval endpoints, the
    digits of C_f fixed by the intervals, and a 40-digit recomputation of the
    partial products for p ≤ 1e5 as a check of floating-point rounding;
  * (round 2) for every row at the largest x, the largest δ for which the row
    lies in the range of Theorem 1.1(iii), computed from the actual ratio
    f(y)/x (`reproduction.json`, `eligibility_at_largest_x`);
  * (round 2) every number quoted in the prose of Section 10 is generated as a
    macro by `reproduce.py`, and the qualitative claims made there are checked
    by the script (`reproduction.json`, `text_claim_checks`);
  * (round 4) every number that the prose of Section 10 states as a bound or
    range is rounded outwards (upper bounds up, lower bounds down), and the
    script checks that each printed bound holds for the computed value
    (`text_claim_checks`, the entries added in round 4).
* **Remark 6.3**: the lower bound `h(q) ≥ I A_h φ(q)/q`, from `b_p/a_p ≥ 1 − 1/p`
  and `c_p/a_p = (p+1)/(p+2)`. It justifies stating the relative error of
  Proposition 6.2, for `x ≥ 1` and `1 ≤ q ≤ x` (range made explicit in round 3,
  §4 item 21). This is a remark only; P6 states the absolute error.
* **Appendix B** (provenance), from `provenance.json` and `interventions.md`.

## 6. Exposure and compliance notes

No source outside the workspace was read. No work by the excluded author and
not the excluded paper was searched for, opened or used. The repository URL in
`provenance.json` is stated for reproducibility only and was not browsed. No
literature published after 2010 was used except the supplied
Brüdern–Wooley (2011) paper.

## 7. Revision log: round 2 (response to the round-1 write-up reviews)

The round-1 review files are not in this workspace (see the note at the top);
the objections are summarised as recorded when they were answered.

Referee 0 (`claude-opus-5-5`):

1. Duplicate hyperref destinations: anchors for equations and theorem-like
   environments are now section-qualified (`\theHequation`, `\theHtheorem` in
   `main.tex`); bookmark levels for the theorem-like environments are defined.
2. Unrecorded strengthenings: listed in §4a with source lines.
3. README runtime figures: the README no longer quotes fixed timings; it
   points to `snapshot_rerun.seconds` and
   `snapshot_rerun.total_seconds_of_reproduce_py` in `reproduction.json`,
   which are written by the run that produced the shipped artifacts.
4. Stale numbering in `reproduce.py` comments: corrected (Proposition 4.1,
   Section 10.2, proof of Proposition 6.2).
5. `Q` versus `Y` in §1.2: Vaughan's result is written with `Y`, and the
   change of letter is stated.
6. §10.4 tautology and the "0.140" wording: rewritten; the values at
   r = 0.005 and r = 1 are now generated ranges over the three polynomials.
7. Mirsky: the unverifiable citation is dropped (§4 item 18).
   Cosmetic layout points: a `\FloatBarrier` keeps the Section 10 floats out
   of the Limitations list; floats in Section 10 may now use float pages.

Referee 1 (`codex:gpt-6.1-sol`):

1. Lemma 2.6 convergence hypothesis: §4 item 19.
2. `56.1Λ`: §4 item 20.
3. Interval endpoints: rounded outwards (lower down, upper up) in
   `reproduce.py`; §10.2 distinguishes digits fixed by the intervals from
   approximate values, and states that floating-point rounding is not
   certified.
4. Target ratio versus actual ratio: §10.5 now uses the actual ratio
   `ϱ = f(y)/x` and the exact eligibility condition; the incorrect claim
   about rows with r = 1 "for every δ > 0" is replaced.
5. Locators for BGPVW (1998) and Brüdern–Wooley (2011): no verified URL, DOI
   or arXiv identifier is available in the supplied material, and none was
   searched for (no network access). This is now recorded in the
   bibliography entries and in the README.
6. Compliance sentences in §1.1: moved to Appendix B ("Workflow").

## 8. Revision log: round 3 (response to the round-2 write-up reviews)

The round-2 review files are not in this workspace (see the note at the top);
the objections are summarised as recorded when they were answered.

Both round-2 referees found no error in the mathematics and no source gap.

Referee 0 (`claude-opus-5-5`):

1. Write-up workflow incomplete in Appendix B: a paragraph "Write-up stage"
   now names the writer (`claude-opus-5-5`, Claude Code 2.1.311), the write-up
   referees `claude-opus-5-5` and `codex:gpt-6.1-sol` (`reviewer_models` in
   `provenance.json`), the CLI versions recorded for the write-up stage
   (Claude Code 2.1.311, codex-cli 0.166.0), and the two review rounds with
   revisions.
2. Corrections not separated by origin: Appendix B ("Workflow") now sorts the
   corrections into groups (a) operator audit, (b) run referees and (c)
   write-up stage. It says in one line that Lemma 2.6 narrows an
   over-general auxiliary lemma of the archived P5 proof, introduced at the
   write-up stage. Every §4 item here carries its group tag, and item 19 is
   flagged for Markus's acknowledgement. (Superseded in round 4: Lemma 2.6
   no longer adds a hypothesis; see §4 item 19 and §9.)
3. Round-1 feedback files not supplied: noted at the top of this file and in
   §7; the round-1 objections behind items 18–20 and §4a are stated inline.
4. Inconsistent runtimes: §10.1 and the README no longer quote fixed
   timings; both point to the fields of `reproduction.json` written by the
   run that produced the shipped artifacts.
5. Acceptance wording: Appendix B now quotes the recorded decision ("Let's
   just assume the proof is correct and complete") and states that the audit
   left final mathematical acceptance to the project owner.

Referee 1 (`codex:gpt-6.1-sol`):

1. Remark 6.3 range: §4 item 21.

The numerical artifacts were regenerated by a fresh full run of
`reproduce.py` for this revision (no change to the script).

## 9. Revision log: round 4 (response to `feedback/0.json` and `feedback/1.json`)

Both round-3 referees found no error in the mathematics and no source gap.
`claude-opus-5-5` passed the manuscript with optional cosmetic remarks;
`codex:gpt-6.1-sol` asked for a revision on three points.

Referee 1 (`codex:gpt-6.1-sol`):

1. *Lemma 2.6 adds a hypothesis that Markus has not authorised; obtain and
   record his decision.* The writer cannot obtain a decision, and none is
   recorded in the supplied material. The added hypothesis has therefore been
   removed. Lemma 2.6 keeps exactly the archived hypotheses and states the
   b = ∞ conclusion in the form that is true under them (convergence of
   `Σ_{a<n≤b} G(n) − ∫_a^b G`; the series converges iff the integral does).
   Both applications in §6 now say explicitly that their series and integrals
   converge absolutely. Details: §4 item 19. Appendix B ("Workflow") is
   updated accordingly. The point stays listed for Markus in §10, because the
   precise reading of the archived "the same holds" is a write-up-stage
   choice.
2. *Nearest rounding makes stated bounds false* (δ_row at r = 1: 2.3455e-4 >
   2.3e-4; max V/Σ_MT = 1.0010036 > 1.0010; float check 2.212e-16 > 2.2e-16;
   β up to 1.55117 > 1.551; N(x,1) down to 0.16671 < 0.167). `reproduce.py`
   now rounds every quoted bound or range outwards (helpers `up`, `down`,
   `tex_sci_up`). It checks each printed bound against the computed value and
   stops if one fails (`bound_checks`, recorded in `text_claim_checks`). The
   new values are δ_row ≤ 2.4e-4, V/Σ_MT ∈ [0.9938, 1.0011], float
   discrepancy ≤ 2.3e-16, β ∈ [1.538, 1.552] and N(x,1) ∈ [0.166, 0.184].
   The self-test and re-run comparisons now read "at most" and are also
   rounded up. Values stated as approximate (relative differences of the
   extrapolations, `x^{-2/9}`, `x^{-1/3}r^{-3/2}`, the largest δ_row) keep
   nearest rounding, and the text now says "approximately" or "about". The
   first paragraph of Section 10 states this convention. The value of I in (1.3), which is followed
   by "…", is now truncated rather than rounded; the digits are unchanged.
3. *"Now in feedback/" is inaccurate.* The note at the top of this file now
   says which review files are in this workspace (round 3 only). It says that
   the round-1 and round-2 files are historical and not in the package, and
   that §7, §8 and inline mentions of earlier objections are the writer's
   summaries. The stale `feedback/…` references in §4 items 19 and 21 and in
   the heading of §8 are corrected.

Referee 0 (`claude-opus-5-5`), optional cosmetic remarks:

1. Abstract: it now states that δ ∈ (0, 1/9) is fixed and that the implied
   constant depends only on f and δ.
2. Lemma 8.5: a sentence after the proof notes that the lemma has content
   only when `sup_J G < ∞`, which holds in its application (`G = F`
   continuous on `[1, y]`). The hypotheses of the lemma are unchanged.
3. Table 3: the last column header is now `(C_extr − C_f)/envelope`, and the
   caption explains how to read it. Table 4: the header of the third model is
   written out as `C + a√r + br + cr^{3/2}`. Figure 3: the caption explains
   that both panels use the legend of the left panel.
4. The referee could not check §7–§8 against the earlier feedback files; see
   item 3 above.

The numerical artifacts were regenerated by a fresh full run of
`reproduce.py` for this revision.

## 10. Points for Markus's attention

* **Lemma 2.6 (§4 item 19).** The archived P5 proof (line 11) states the
  infinite-interval Euler–Maclaurin formula under `F, F' → 0`, `F'' ∈ L^1`,
  with "the same holds". The manuscript keeps these hypotheses and reads the
  conclusion as convergence of `Σ_{a<n≤b} F(n) − ∫_a^b F`. Under that reading
  the clause is true, and the series converges iff the integral does. A
  literal reading as an identity between two separately convergent
  quantities would be false (`cos(log u)/u`). Both archived applications
  involve absolutely convergent series and integrals, so the P5 argument and
  every statement stand. No decision on this point is recorded; please
  confirm the reading or say if you prefer another presentation.
