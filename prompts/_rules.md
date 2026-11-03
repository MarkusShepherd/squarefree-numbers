## Rules for every agent on this project

1. **Excluded author.** Markus Schepke (who also publishes as Markus Shepherd)
   wrote a master's thesis on exactly this problem. The point of this project is
   to solve it independently of that work. Do not search for, open, fetch or
   read anything written by him: his thesis, his blog (riemannhypothesis.blog,
   primes.recommend.games, mshepherd.gitlab.io), his GitLab projects, or any
   other source by him. If a search result or a source turns out to be his,
   stop, use nothing from it, and say so explicitly in your output. The same
   applies to anything you may remember about his work: do not use it.
   **Excluded paper.** The same rules apply to Fabian Dehnert, *Sparse variance
   for k-free numbers in arithmetic progressions*, Monatsh. Math. 177 (2015),
   373–396 (doi:10.1007/s00605-014-0691-6), which solves this problem too: do
   not search for, open or use it, or anything you remember of it.
2. Work only with the files in your current directory and with the published
   literature. Do not read or list files outside your current directory.
   **Previous write-ups are excluded.** Do not search for, open, fetch, read
   or use manuscripts produced from other runs of this project, including
   their LaTeX sources, compiled PDFs, extracts and drafts, whether in this
   repository (such as `thesis/`), published online or remembered. Do not use
   them indirectly as hints. If encountered, stop reading, use nothing from
   them and report the exposure. A write-up task may use only the archived
   run and manuscript explicitly supplied for that task; this does not permit
   access to write-ups of other runs.
3. Cite every external source you use: authors, title, year, and URL or arXiv
   id.
4. **Literature up to 2010.** Use only literature published, or posted as a
   preprint, in 2010 or earlier, plus the papers in `papers/` (Brüdern–Wooley
   2011 among them). This applies to searching, reading and citing, and to
   results you remember: do not use a result first published in 2011 or
   later, even if you know it. If a source turns out to be from 2011 or later,
   stop reading it, use nothing from it, and say so in your output.
5. **Python.** If you can run commands, `python3` has numpy, scipy, mpmath
   and sympy installed, besides the standard library; use them as you like.
   Installing anything else is not possible in your sandbox, so don't try.
6. **Reading PDFs.** Poppler's `pdfinfo`, `pdftotext` and `pdftoppm` should
   be available to you. Use `pdftotext -layout` to extract text and, when
   supported, render relevant pages with `pdftoppm` to check equations,
   tables or unclear extraction visually. You are free to use a different
   tool if it works better for you. If Poppler is unavailable, flag this to
   the user for installation; do not try to install it in your sandbox.
   Keep any extracted text or rendered pages within your current directory.
