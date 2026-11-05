# Literature search

### claude-opus-5-5

I found no source by the excluded author (Markus Schepke / Markus Shepherd), and none of his sites (riemannhypothesis.blog, primes.recommend.games, mshepherd.gitlab.io) came up. Nothing by or about the excluded Dehnert paper was searched for or opened.

Post-2010 works seen only as search-result titles or snippets, not opened and not used: Nunes (arXiv 1402.0684, 2014), Le Boudec (2015–16), Gorodetsky–Matomäki–Radziwiłł–Rodgers (arXiv 2006.04060, 2020), R. C. Baker "Primes in arithmetic progressions to spaced moduli" I–III (2012–2017), Brüdern–Wooley "Sparser variance for primes in arithmetic progression" (arXiv 1706.07319, 2017), Vaughan's arXiv survey "The generalized Montgomery–Hooley formula" (arXiv 2605.18996, 2026), Harper (2024), and Baier–Pujahari (2023). Snippet details from these (e.g. Hooley 1975's range x^{2/3−ε}, Croft's main result) are used in the 'why' fields above; check them against the originals.

Key points for planners:
(1) Vaughan 2005 relies on Vaughan 1998 Part II (pp. 793–809, general sequences in all residue classes), not Part I. Brüdern–Wooley rely on Part I (pp. 781–791) and Goldston–Vaughan 1997. Both parts are needed.
(2) Vaughan 2005 (p. 574) says Croft 1975 is faulty at (6.6) and its constant is wrong. Warlimont 1980 gives the correct classical squarefree result.
(3) The main-term evaluation will need averages over k ≤ y of f'(k) times multiplicative functions of f(k) (or of gcds with f(k)). This means counting k with d | f(k), i.e. ρ(d), uniformly in d. I found no pre-2010 paper doing exactly this for the squarefree variance with polynomial moduli. Brüdern–Wooley §§5–6 (primes) is the closest model, and the literature on ρ (Hooley 1964, Huxley 1981, Stewart 1991, Nagell's classical bound for p ∤ disc) supplies the inputs.
(4) Mirsky 1949 (shifted squarefree pairs) is the natural input for an elementary route that expands the square and counts n1 − n2 = h f(k).

Access caveats:
- A scan of Vaughan 1998 Part I sits on a Williams College course-handout page. Its authorisation is unclear, so I did not list it.
- Royal Society, Project Euclid, AMS and zbMATH pages returned 403 or empty to my fetcher, so several likely-free items (Montgomery 1970, Mirsky 1949, Stewart 1991, Nair–Tenenbaum 1998, Hooley BDH I via GDZ) are marked 'unknown' rather than 'open'.
- An unofficial Springer mirror (elogim.com) appeared for Heath-Brown 1984; I did not use it.

Items not fully identified:
- Baier, 'The large sieve with sparse sets of moduli': the journal reference (J. Ramanujan Math. Soc. 21, 2006) is from memory. arXiv lists no journal reference.
- Several DOIs are from memory or pattern and were not opened: Goldston–Vaughan, Warlimont 1969, Orr, Mirsky 1947, Hooley 1964, Erdős 1952. Each is noted in its 'why' field; check them.

### codex:gpt-6.1-sol

The list excludes the three supplied papers. Eight full-text PDF links were opened and verified; empty pdf_url fields indicate that no reliable direct PDF was verified. Unknown access includes blocked retrievals and does not imply a paywall. Elsevier labels Orr’s article “Open archive”, but its PDF could not be verified. Blomer’s author-hosted abstract18.pdf is only an abstract and is deliberately omitted.

Critical reading warning: R. C. Vaughan, A variance for k-free numbers in arithmetic progressions (2005), p. 574, https://doi.org/10.1112/S0024611505015352, identifies the flaw in Croft’s argument and points to Warlimont (1980). Goldston–Vaughan’s chapter is sometimes cited as 1996; Cambridge confirms the print publication year as 1997.

For inaccessible works, relevance assessments rely on publisher abstracts and citations in the supplied corpus. Planners should check modular periodicity before using rho(m) for a rational integer-valued polynomial; Cahen–Chabert addresses the relevant distinction.

An unsolicited search result from primes.recommend.games was identified as belonging to the excluded author; it was not opened or used. Post-2010 works also appeared in search results and were discarded without opening or using their mathematical content. The excluded paper was not opened or used.

## Downloaded: check each, then copy what you want into papers/ and list it in papers/INDEX.md

- **D. A. Goldston and R. C. Vaughan (1997)**, *On the Montgomery-Hooley asymptotic formula*, Sieve Methods, Exponential Sums, and their Applications in Number Theory, London Mathematical Society Lecture Note Series 237, Cambridge University Press, 117–142 [article, relevance 3; codex:gpt-6.1-sol]  
  Treats the off-diagonal part of variance directly as an additive problem through the circle method. Its singular-series summation and contour arguments are explicitly used in the supplied sparse-prime paper; distinguish unconditional arguments from those assuming GRH.  
  https://doi.org/10.1017/CBO9780511526091.010 (literature/pdf/codex-gpt-6.1-sol-04-goldstonvaughan1997.pdf)
- **R. C. Vaughan (1998)**, *On a variance associated with the distribution of general sequences in arithmetic progressions. I*, Philosophical Transactions of the Royal Society of London A 356 (1738), 781–791 [article, relevance 3; codex:gpt-6.1-sol]  
  Develops the general-sequence Montgomery–Hooley method when small-modulus equidistribution concerns reduced residue classes. Its concluding singular-series calculation is specifically cited by the supplied Brüdern–Wooley paper.  
  https://doi.org/10.1098/rsta.1998.0185 (literature/pdf/codex-gpt-6.1-sol-05-vaughan1998i.pdf)
- **J. Brüdern and A. Perelli (1998)**, *Goldbach numbers in sparse sequences*, Ann. Inst. Fourier (Grenoble) 48 (1998), no. 2, 353–378 [article, relevance 2; claude-opus-5-5]  
  Ref. [1] of Brüdern–Wooley: a circle-method treatment of additive problems along sparse sequences, including polynomial-value-type sets. Brüdern–Wooley borrow from it for handling sums over f(k) on major and minor arcs. The open Numdam/Centre Mersenne PDF was confirmed as a 1.6 MB AIF 48(2) p. 353 file.  
  https://doi.org/10.5802/aif.1621 (literature/pdf/claude-opus-5-5-16-bruedernperelli1998.pdf)
- **S. Baier and L. Zhao (2006)**, *Bombieri–Vinogradov type theorems for sparse sets of moduli*, Acta Arith. 125 (2006), 187–201 [article, relevance 2; claude-opus-5-5]  
  BV and BDH-type theorems for sparse sets of moduli, e.g. squares and polynomial values, via large sieve inequalities for sparse moduli. An alternative (large-sieve) route to the upper bound for V_f, and a source of the admissible range of f(y) relative to x.  
  https://arxiv.org/abs/math/0602116 (literature/pdf/claude-opus-5-5-21-baierzhao2006.pdf)
- **C. L. Stewart (1991)**, *On the number of solutions of polynomial congruences and Thue equations*, Journal of the American Mathematical Society 4 (4), 793–835 [article, relevance 2; codex:gpt-6.1-sol]  
  Contains bounds for the number of solutions of polynomial congruences, useful when estimating local root counts and Euler factors. Check the degree, discriminant and nondegeneracy hypotheses before applying these bounds to the chosen polynomial.  
  https://doi.org/10.1090/S0894-0347-1991-1119199-X (literature/pdf/codex-gpt-6.1-sol-08-stewart1991.pdf)
- **Stephan Baier and Liangyi Zhao (2006)**, *Bombieri-Vinogradov type theorems for sparse sets of moduli*, Acta Arithmetica 125 (2), 187–201 [article, relevance 2; codex:gpt-6.1-sol]  
  Establishes Barban–Davenport–Halberstam and Bombieri–Vinogradov type bounds for well-distributed sparse sets, including square moduli. Its precise distribution hypotheses provide a useful checklist for any alternative large-sieve treatment of polynomial moduli.  
  https://arxiv.org/abs/math/0602116 (literature/pdf/codex-gpt-6.1-sol-10-baierzhao2006.pdf)
- **Stephan Baier (2006)**, *On the large sieve with sparse sets of moduli*, Journal of the Ramanujan Mathematical Society 21 (3), 279–295 [article, relevance 2; codex:gpt-6.1-sol]  
  Gives a large-sieve inequality for arbitrary coefficient sequences when the moduli satisfy suitable progression-counting conditions. This makes it a potential tool for squarefree exponential sums without requiring prime-specific coefficients.  
  https://arxiv.org/abs/math/0512228 (literature/pdf/codex-gpt-6.1-sol-11-baier2006.pdf)
- **Stephan Baier and Liangyi Zhao (2008)**, *An improvement for the large sieve for square moduli*, Journal of Number Theory 128 (1), 154–174 [article, relevance 2; codex:gpt-6.1-sol]  
  Improves large-sieve bounds for arbitrary sequences sampled at fractions with square denominators. Particularly useful if the team first restricts the problem to square moduli; the proof combines Weyl sums, quadratic Gauss sums and exponential-integral estimates.  
  https://arxiv.org/abs/math/0512271 (literature/pdf/codex-gpt-6.1-sol-17-baierzhao2008.pdf)
- **Heini Halberstam (1972)**, *The distribution of sequences in arithmetic progressions*, Séminaire Delange-Pisot-Poitou 13 (1971–1972), no. 2, exposé 25, 1–5 [lecture notes, relevance 2; codex:gpt-6.1-sol]  
  A short contemporary overview connecting prime-distribution mean values with general arithmetic sequences and squarefree numbers. Its references independently connect Orr, Warlimont and Croft’s then-developing work.  
  https://www.numdam.org/item/SDPP_1971-1972__13_2_A10_0/ (literature/pdf/codex-gpt-6.1-sol-18-halberstam1972.pdf)
- **Jörg Brüdern and Alberto Perelli (1998)**, *Goldbach numbers in sparse sequences*, Annales de l’Institut Fourier 48 (2), 353–378 [article, relevance 2; codex:gpt-6.1-sol]  
  Develops exponential-sum methods for sequences thinner than polynomial-value sequences. The supplied Brüdern–Wooley paper points to this work when discussing extensions beyond polynomial moduli.  
  https://doi.org/10.5802/aif.1621 (literature/pdf/codex-gpt-6.1-sol-19-bruedernperelli1998.pdf)
- **S. Baier and L. Zhao (2008)**, *An improvement for the large sieve for square moduli*, J. Number Theory 128 (2008), no. 1, 154–174 [article, relevance 1; claude-opus-5-5]  
  A large sieve inequality Σ_{q≤Q} Σ_{a mod q²} |Σ a_n e(an/q²)|² with improved bounds. Relevant if the team bounds V_f(x,y) from above by a large sieve with polynomial moduli (squarefree indicator as the sequence).  
  https://arxiv.org/abs/math/0512271 (literature/pdf/claude-opus-5-5-22-baierzhao2008.pdf)
- **S. Baier (2006)**, *The large sieve with sparse sets of moduli*, J. Ramanujan Math. Soc. 21 (2006) (venue from memory, unverified); preprint arXiv:math/0508417 (2005) [article, relevance 1; claude-opus-5-5]  
  A general large sieve for sparse moduli that are well distributed in progressions (extending Wolke), applied to squares. Gives a general framework for moduli f(k).  
  https://arxiv.org/abs/math/0508417 (literature/pdf/claude-opus-5-5-23-baier2005.pdf)

## Wishlist: no open PDF; get the full text if worthwhile, then as above

- **R. C. Vaughan (1998)**, *On a variance associated with the distribution of general sequences in arithmetic progressions. II*, Phil. Trans. R. Soc. Lond. A 356 (1998), no. 1738, 793–809 [article, relevance 3; claude-opus-5-5]  
  This is ref. [7] of Vaughan 2005. It gives Montgomery–Hooley-type asymptotics for general sequences that are approximately distributed in every residue class, not only the reduced ones, which is the situation for squarefree numbers. Its Theorem 1.2 and hypothesis (1.12) are what Vaughan 2005 sharpens. It is the template for the 'classical' route, with error at least x^{1+1/k} log x, and for the structure of the main term x^2 F(x/Q).  
  https://doi.org/10.1098/rsta.1998.0186 (no open-access PDF (paywalled))
- **R. C. Vaughan (1998)**, *On a variance associated with the distribution of general sequences in arithmetic progressions. I*, Phil. Trans. R. Soc. Lond. A 356 (1998), no. 1738, 781–791 [article, relevance 3; claude-opus-5-5]  
  This is ref. [10] of Brüdern–Wooley. It is the circle-method treatment of the Montgomery–Hooley variance for general sequences equidistributed in reduced classes. Brüdern–Wooley say their major-arc treatment, with auxiliary averages of multiplicative functions, mirrors this paper.  
  https://doi.org/10.1098/rsta.1998.0185 (no open-access PDF (paywalled))
- **D. A. Goldston and R. C. Vaughan (1997)**, *On the Montgomery–Hooley asymptotic formula*, Sieve Methods, Exponential Sums, and their Applications in Number Theory (Cardiff, 1995), LMS Lecture Note Ser. 237, Cambridge Univ. Press (1997), 117–142 [article, relevance 3; claude-opus-5-5]  
  Origin of the method: the variance is reduced to counting n1 − n2 = hq with q ≤ Q and evaluated by the circle method, the minor arcs being handled through the product hq. Brüdern–Wooley adapt exactly this to n1 − n2 = h f(k). Page 118 has historical comments on the method. The DOI in the URL was not verified; check the landing page.  
  https://doi.org/10.1017/CBO9780511526091.010 (no open-access PDF (paywalled))
- **R. C. Vaughan (1998)**, *On a variance associated with the distribution of general sequences in arithmetic progressions. II*, Philosophical Transactions of the Royal Society of London A 356 (1738), 793–809 [article, relevance 3; codex:gpt-6.1-sol]  
  Develops variance asymptotics for sequences with residue-dependent local densities, including non-coprime residue classes. Vaughan’s supplied 2005 paper explicitly identifies its Theorem 1.2 as an earlier framework applicable to k-free numbers.  
  https://doi.org/10.1098/rsta.1998.0186 (no open-access PDF (unknown))
- **Richard Warlimont (1980)**, *Squarefree numbers in arithmetic progressions*, Journal of the London Mathematical Society (2) 22 (1), 21–24 [article, relevance 3; codex:gpt-6.1-sol]  
  Gives an earlier asymptotic for the squarefree variance averaged over moduli. The supplied Vaughan paper specifically recommends its treatment as avoiding a flaw in Croft’s argument.  
  https://doi.org/10.1112/jlms/s2-22.1.21 (no open-access PDF (paywalled))
- **M. J. Croft (1975)**, *Square-Free Numbers in Arithmetic Progressions*, Proceedings of the London Mathematical Society (3) 30 (2), 143–159 [article, relevance 3; codex:gpt-6.1-sol]  
  A central early reference for mean-square distribution of squarefree numbers in progressions. Read with Vaughan’s correction: the contour argument leading to Croft’s equation (6.6), and consequently a stated constant, is faulty.  
  https://doi.org/10.1112/plms/s3-30.2.143 (no open-access PDF (paywalled))
- **Richard C. Orr (1971)**, *Remainder estimates for squarefree integers in arithmetic progression*, Journal of Number Theory 3 (4), 474–497 [article, relevance 3; codex:gpt-6.1-sol]  
  Establishes squarefree analogues of average remainder estimates associated with Barban, Bombieri, Davenport, Halberstam and Gallagher. A useful source for preliminary mean-square bounds before extracting a sparse-modulus asymptotic.  
  https://doi.org/10.1016/0022-314X(71)90015-1 (no open-access PDF (unknown))
- **R. C. Vaughan (1997)**, *The Hardy-Littlewood Method*, Second edition, Cambridge Tracts in Mathematics 125, Cambridge University Press [book, relevance 3; codex:gpt-6.1-sol]  
  Provides polynomial exponential-sum estimates and the circle-method machinery needed for sparse polynomial moduli. The supplied Brüdern–Wooley paper explicitly uses Theorems 5.2 and 7.4 and the transference exercise in Chapter 2.  
  https://doi.org/10.1017/CBO9780511470929 (no open-access PDF (unknown))
- **R. C. Vaughan (2001)**, *On a variance associated with the distribution of primes in arithmetic progressions*, Proc. London Math. Soc. (3) 82 (2001), 533–553 [article, relevance 2; claude-opus-5-5]  
  Ref. [11] of Brüdern–Wooley. A refined circle-method analysis of the prime variance with an explicit secondary main term. It is useful for how to extract the lower-order main terms from major arcs and singular-series-type averages.  
  https://doi.org/10.1112/plms/82.3.533 (no open-access PDF (paywalled))
- **H. Mikawa and T. P. Peneva (2005)**, *Primes in arithmetic progressions to spaced moduli*, Arch. Math. (Basel) 84 (2005), 239–248 [article, relevance 2; claude-opus-5-5]  
  The Barban–Davenport–Halberstam upper bound for primes with moduli f(k), weighted by f'(k) or k^{-1}φ(f(k)). This is the sparse-moduli predecessor that Brüdern–Wooley sharpen to an asymptotic, and a model for the upper-bound (BDH) part of the squarefree problem.  
  https://link.springer.com/article/10.1007/s00013-004-1131-y (no open-access PDF (paywalled))
- **M. J. Croft (1975)**, *Square-free numbers in arithmetic progressions*, Proc. London Math. Soc. (3) 30 (1975), 143–159 [article, relevance 2; claude-opus-5-5]  
  First BDH/Montgomery–Hooley-type result for squarefree numbers, summing over all residue classes mod q (not only coprime ones), as in the present problem. Caution: Vaughan 2005 (p. 574) says the argument leading to Croft's (6.6) is faulty and the constant B in his (7.2) is wrong. Use it for structure only, not for constants.  
  https://doi.org/10.1112/plms/s3-30.2.143 (no open-access PDF (paywalled))
- **R. Warlimont (1980)**, *Squarefree numbers in arithmetic progressions*, J. London Math. Soc. (2) 22 (1980), 21–24 [article, relevance 2; claude-opus-5-5]  
  Gives V(x,Q) = x^2 F(x/Q) + O(x^{3/2}(log x)^{7/2}) for squarefree numbers with F(y) = c y^{-3/2} + O(...), avoiding Croft's error. This is the classical benchmark main term c x^{1/2} Q^{3/2} for all moduli, against which the sparse main term should be checked.  
  https://doi.org/10.1112/jlms/s2-22.1.21 (no open-access PDF (paywalled))
- **R. C. Orr (1971)**, *Remainder estimates for squarefree integers in arithmetic progression*, J. Number Theory 3 (1971), 474–497 [article, relevance 2; claude-opus-5-5]  
  Mean-square and individual remainder estimates for Q(x;q,l) (from Orr's 1969 Syracuse thesis under Richert). Halberstam remarked that it is hard to improve upon. A source of elementary bounds for E(x;q,l) uniform in q and l. The DOI was not verified; older JNT volumes are in Elsevier's open archive.  
  https://doi.org/10.1016/0022-314X(71)90031-3 (no open-access PDF (unknown))
- **C. Hooley (1975)**, *A note on square-free numbers in arithmetic progressions*, Bull. London Math. Soc. 7 (1975), 133–138 [article, relevance 2; claude-opus-5-5]  
  An individual bound for E(x;q,l), improving Prachar, which gives an asymptotic for Q(x;q,l) for q up to about x^{2/3−ε}. Useful for disposing of moduli f(k) in ranges where pointwise bounds suffice, and for the trivial estimate of the variance.  
  https://doi.org/10.1112/blms/7.2.133 (no open-access PDF (paywalled))
- **J. Brüdern, A. Perelli and T. D. Wooley (2000)**, *Twins of k-free numbers and their exponential sum*, Michigan Math. J. 47 (2000), 173–190 [article, relevance 2; claude-opus-5-5]  
  L1 and L2 bounds for exponential sums over k-free twins, extending BGPVW's estimates for Σ μ_k(n)e(nα). Useful for minor-arc and mean-value bounds involving μ². Wooley's site lists a copy (math.purdue.edu/~twooley/publ/2000ktwin.pdf), but the fetch failed, so it is not verified. The page range is from memory: the search snippet showed 173–177, which looks truncated, so verify it.  
  https://doi.org/10.1307/mmj/1030374676 (no open-access PDF (unknown))
- **C. Hooley (1975)**, *On the Barban–Davenport–Halberstam theorem. I*, J. Reine Angew. Math. 274/275 (1975), 206–223 [article, relevance 2; claude-opus-5-5]  
  Hooley's refinement of Montgomery's asymptotic, V(x,Q) = Qx log Q + cQx + O(...), via an elementary divisor-switching method. It is the classical alternative to the circle method and the source of the second main term. EuDML links the full text at GDZ (free), but it was not downloaded.  
  https://eudml.org/doc/151577 (no open-access PDF (unknown))
- **C. Hooley (1964)**, *On the distribution of the roots of polynomial congruences*, Mathematika 11 (1964), 39–49 [article, relevance 2; claude-opus-5-5]  
  Equidistribution of ν/n for roots ν of f(ν) ≡ 0 mod n, via exponential sums over roots. Needed when counting k ≤ y with f(k) ≡ 0 mod d (or f(k) in a class) with error terms uniform in d, as in the main-term evaluation Σ_k f'(k)·(arithmetic function of f(k)). The DOI was not verified.  
  https://doi.org/10.1112/S0025579300003466 (no open-access PDF (paywalled))
- **C. L. Stewart (1991)**, *On the number of solutions of polynomial congruences and Thue equations*, J. Amer. Math. Soc. 4 (1991), 793–835 [article, relevance 2; claude-opus-5-5]  
  Sharp uniform upper bounds for ρ(p^k), the number of roots of f mod p^k, in terms of degree and discriminant. These are needed to control ρ(m) and the multiplicative functions built from it on all prime powers, including primes dividing the discriminant. AMS JAMS back content is usually free, and a scan is hosted at uwaterloo.ca/pure-mathematics (s0894-0347-1991-1119199-x_0.pdf), but its content could not be confirmed by text extraction.  
  https://doi.org/10.1090/S0894-0347-1991-1119199-X (no open-access PDF (unknown))
- **R. C. Vaughan (1997)**, *The Hardy–Littlewood Method, 2nd edition*, Cambridge Tracts in Mathematics 125, Cambridge University Press (1997) [book, relevance 2; claude-opus-5-5]  
  Standard reference cited by all three corpus papers: Weyl's inequality, major-arc approximations, and the complete exponential sums S(q,a) = Σ e(a f(x)/q) bounds (Hua) needed for sums over k of e(α h f(k)) on the minor arcs.  
  https://doi.org/10.1017/CBO9780511470929 (no open-access PDF (paywalled))
- **Valentin Blomer (2008)**, *The average value of divisor sums in arithmetic progressions*, The Quarterly Journal of Mathematics 59 (3), 275–286 [article, relevance 2; codex:gpt-6.1-sol]  
  Studies mean-square errors over residue classes for a fixed modulus, with extensions explicitly including k-free numbers. Investigate its estimates as possible inputs for controlling portions of the sparse variance.  
  https://doi.org/10.1093/qmath/ham044 (no open-access PDF (paywalled))
- **H. Mikawa and T. P. Peneva (2005)**, *Primes in arithmetic progressions to spaced moduli*, Archiv der Mathematik 84 (3), 239–248 [article, relevance 2; codex:gpt-6.1-sol]  
  Proves average distribution results for widely separated moduli. The supplied Brüdern–Wooley paper invokes this work to remove small polynomial moduli and specifically identifies Section 2.2 as containing an important ingredient.  
  https://doi.org/10.1007/s00013-004-1131-y (no open-access PDF (paywalled))
- **L. Mirsky (1949)**, *On the frequency of pairs of square-free numbers with a given difference*, Bulletin of the American Mathematical Society 55 (10), 936–939 [article, relevance 2; codex:gpt-6.1-sol]  
  Studies squarefree pair correlations at a prescribed shift, the basic objects arising after expanding the variance. Useful for understanding the local correlation factors, while uniformity in varying shifts must be checked separately.  
  https://doi.org/10.1090/S0002-9904-1949-09313-8 (no open-access PDF (unknown))
- **C. Hooley (1975)**, *On the Barban-Davenport-Halberstam theorem. I*, Journal für die reine und angewandte Mathematik 274/275, 206–223 [article, relevance 2; codex:gpt-6.1-sol]  
  A foundational refinement of the Montgomery variance asymptotic and an important source for the divisor-switching approach. Read to understand the method that the general-sequence and sparse-modulus papers subsequently adapt.  
  https://doi.org/10.1515/crll.1975.274-275.206 (no open-access PDF (unknown))
- **H. L. Montgomery (1970)**, *Primes in arithmetic progressions*, Michigan Mathematical Journal 17 (1), 33–39 [article, relevance 2; codex:gpt-6.1-sol]  
  The original asymptotic treatment of the prime variance underlying the Montgomery–Hooley framework. Provides the classical benchmark for separating diagonal and off-diagonal contributions.  
  https://doi.org/10.1307/mmj/1029000373 (no open-access PDF (unknown))
- **Richard Warlimont (1969)**, *On squarefree numbers in arithmetic progressions*, Monatshefte für Mathematik 73, 433–448 [article, relevance 2; codex:gpt-6.1-sol]  
  An early source for average distribution estimates for squarefree numbers, cited by both supplied squarefree papers. Useful for tracing the preliminary mean-square estimates and their large-sieve origins.  
  https://doi.org/10.1007/BF01316664 (no open-access PDF (paywalled))
- **Paul-Jean Cahen and Jean-Luc Chabert (1997)**, *Integer-Valued Polynomials*, Mathematical Surveys and Monographs 48, American Mathematical Society [book, relevance 2; codex:gpt-6.1-sol]  
  A reference for the distinction between polynomials with integer coefficients and rational polynomials taking integer values. Relevant to checking modular periodicity and the interpretation of local root counts in the problem’s full stated generality.  
  https://doi.org/10.1090/surv/048 (no open-access PDF (unknown))
- **J. B. Friedlander and D. A. Goldston (1996)**, *Variance of distribution of primes in residue classes*, The Quarterly Journal of Mathematics (2) 47 (3), 313–336 [article, relevance 2; codex:gpt-6.1-sol]  
  Studies refined prime-variance estimates and their connection with additive correlations and singular series. Useful methodological background for the supplied sparse-prime paper, with conditional estimates kept separate from unconditional inputs.  
  https://doi.org/10.1093/qmath/47.3.313 (no open-access PDF (paywalled))
- **R. Warlimont (1969)**, *On squarefree numbers in arithmetic progressions*, Monatsh. Math. 73 (1969), 433–448 [article, relevance 1; claude-opus-5-5]  
  Early variance and BDH-type bounds for squarefree numbers in progressions; cited by both Vaughan 2005 and BGPVW. The DOI was not verified; check via EuDML/GDZ, where Monatshefte scans of this era are often freely available.  
  https://doi.org/10.1007/BF01300302 (no open-access PDF (paywalled))
- **R. Warlimont (1972)**, *Über quadratfreie Zahlen in arithmetischen Progressionen*, Monatsh. Math. 76 (1972), 272–275 [article, relevance 1; claude-opus-5-5]  
  A short follow-up improving the squarefree variance bounds; ref. [9] of Vaughan 2005.  
  https://eudml.org/search/page?q=Warlimont+quadratfreie+Zahlen+arithmetischen+Progressionen (no open-access PDF (unknown))
- **K. Prachar (1958)**, *Über die kleinste quadratfreie Zahl einer arithmetischen Reihe*, Monatsh. Math. 62 (1958), 173–176 [article, relevance 1; claude-opus-5-5]  
  The classical elementary asymptotic Q(x;q,l) = g(q,l)x + O(x^{1/2}q^{-1/4}+q^{1/2+ε}) type for squarefree numbers in a progression. It is the simplest pointwise input. EuDML lists the full text via the Göttingen digitisation centre (GDZ).  
  https://eudml.org/doc/177039 (no open-access PDF (unknown))
- **L. Mirsky (1947)**, *Note on an asymptotic formula connected with r-free integers*, Quart. J. Math. Oxford Ser. 18 (1947), 178–182 [article, relevance 1; claude-opus-5-5]  
  Asymptotics for Σ μ_r(n+k_1)…μ_r(n+k_s) (r-free tuples) with error x^{2/(r+1)+ε}; cited by BGPVW. A k-free analogue of the shifted-correlation input. The DOI was not verified.  
  https://doi.org/10.1093/qmath/os-18.1.178 (no open-access PDF (paywalled))
- **D. R. Heath-Brown (1984)**, *The square sieve and consecutive square-free numbers*, Math. Ann. 266 (1984), 251–259 [article, relevance 1; claude-opus-5-5]  
  Improves the error term for Σ μ²(n)μ²(n+1) to x^{7/11+ε} via the square sieve. Relevant if the team uses correlations of μ² with shifts; it shows the limits of the elementary error term. EuDML (doc 163852) lists it, likely with GDZ full text.  
  https://doi.org/10.1007/BF01475576 (no open-access PDF (unknown))
- **C. Hooley (1975)**, *On the Barban–Davenport–Halberstam theorem. II*, J. London Math. Soc. (2) 9 (1975), 625–636 [article, relevance 1; claude-opus-5-5]  
  Ref. [6] of Brüdern–Wooley: further refinement of the Montgomery–Hooley formula, including what happens when the residue-class sum is over all classes. Background only.  
  https://doi.org/10.1112/jlms/s2-9.4.625 (no open-access PDF (paywalled))
- **H. L. Montgomery (1970)**, *Primes in arithmetic progressions*, Michigan Math. J. 17 (1970), 33–39 [article, relevance 1; claude-opus-5-5]  
  The original asymptotic for the BDH variance of primes, by expanding the square and counting n1 ≡ n2 mod q. Gives the basic expansion that all later works follow. Michigan Math. J. is free on Project Euclid, but the PDF could not be fetched to confirm.  
  https://doi.org/10.1307/mmj/1029000373 (no open-access PDF (unknown))
- **J. B. Friedlander and D. A. Goldston (1996)**, *Variance of distribution of primes in residue classes*, Quart. J. Math. Oxford Ser. (2) 47 (1996), 313–336 [article, relevance 1; claude-opus-5-5]  
  Variance for a single modulus q near x, with the explicit correction term; cited by Brüdern–Wooley. Background on behaviour when moduli are large relative to x (the range f(y) close to x).  
  https://doi.org/10.1093/qmath/47.3.313 (no open-access PDF (paywalled))
- **M. N. Huxley (1981)**, *A note on polynomial congruences*, Recent Progress in Analytic Number Theory, Vol. 1 (Durham, 1979), H. Halberstam and C. Hooley (eds.), Academic Press, London (1981), 193–196 [article, relevance 1; claude-opus-5-5]  
  Bound ρ(p^k) ≤ d·p^{k/2}-type, more precisely in terms of the discriminant, for the number of roots of f mod p^k. A simpler alternative to Stewart for showing ρ is O(m^ε) and multiplicative sums over ρ converge.  
  https://zbmath.org/?q=an:0463.10002 (no open-access PDF (paywalled))
- **M. Nair and G. Tenenbaum (1998)**, *Short sums of certain arithmetic functions*, Acta Math. 180 (1998), 119–144 [article, relevance 1; claude-opus-5-5]  
  Upper bounds of the expected order for Σ_{k≤y} F(|f(k)|) with F submultiplicative, e.g. divisor functions of polynomial values. Handy for bounding error terms like Σ_k τ(f(k)) that arise when E(x;f(k),l) is estimated pointwise. Acta Math. is now open on Project Euclid (euclid.acta/1485891131), but the PDF could not be fetched to confirm.  
  https://doi.org/10.1007/BF02392880 (no open-access PDF (unknown))
- **P. Erdős (1952)**, *On the sum Σ_{k=1}^x d(f(k))*, J. London Math. Soc. 27 (1952), 7–15 [article, relevance 1; claude-opus-5-5]  
  Σ_{k≤x} d(f(k)) ≍ x log x for irreducible f. The elementary prototype for the divisor-of-polynomial-value bounds needed in error terms. The DOI was not verified.  
  https://doi.org/10.1112/jlms/s1-27.1.7 (no open-access PDF (unknown))
- **E. C. Titchmarsh (revised by D. R. Heath-Brown) (1986)**, *The Theory of the Riemann Zeta-Function, 2nd edition*, Oxford University Press (1986) [book, relevance 1; claude-opus-5-5]  
  Vaughan 2005 uses §6.19 (Vinogradov–Korobov zero-free region and bound for 1/ζ) and §§3.12–3.13 for Lemma 2.1 (Σ_{n≤y,(n,q)=1} μ(n)) and for the exp(−c(log x)^{3/5}(log log x)^{−1/5}) error terms.  
  https://global.oup.com/academic/product/the-theory-of-the-riemann-zeta-function-9780198533696 (no open-access PDF (paywalled))
- **H. L. Montgomery and R. C. Vaughan (2007)**, *Multiplicative Number Theory I. Classical Theory*, Cambridge Studies in Advanced Mathematics 97, Cambridge University Press (2007) [book, relevance 1; claude-opus-5-5]  
  Background on Dirichlet series of multiplicative functions, Perron's formula and contour shifting. This is the technique for evaluating the auxiliary sums Σ_q h(q)·(stuff) whose generating function involves ζ(2s+…) as in Vaughan 2005 §6.  
  https://doi.org/10.1017/CBO9780511618314 (no open-access PDF (paywalled))

## Rejected by the driver (a leak pattern can also hit an unrelated work: check the reason)

- **L. Mirsky (1949)**, *On the frequency of pairs of square-free numbers with a given difference*, Bull. Amer. Math. Soc. 55 (1949), 936–939 [article, relevance 2; claude-opus-5-5]  
  An asymptotic for Σ_{n≤x} μ²(n)μ²(n+h) with explicit dependence on h. Expanding V_f gives correlations Σ μ²(n)μ²(n+h f(k)), and the elementary (non-circle-method) route needs exactly such shifted-pair sums with error uniform in the shift. The AMS PDF is at ams.org/bull/1949-55-10/S0002-9904-1949-09313-8; AMS back issues are normally free, but the fetch was blocked so access was not verified.  
  https://projecteuclid.org/journals/bulletin-of-the-american-mathematical-society/volume-55/issue-10/On-the-frequency-of-pairs-of-square-free-numbers-with/bams/1183514158.full (matches excluded pattern 'squarefree-numbers')
