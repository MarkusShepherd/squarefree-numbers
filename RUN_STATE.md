# Where the run stands (2 Nov 2026)

Operator notes on the run's state; rules and procedure are in AGENTS.md.
Update this file after each step. `config.json`, `git log`, `logs/` and
`./orchestrate.py status` win over anything here.

- **Earlier run, before the literature cutoff:** archived as
  `archive/pre-cutoff` (commit 27adfd0 on main) and cleared from the repo and
  `runs_dir`. Don't import its numerical or mathematical outputs into the new
  run. `archive/pre-cutoff/logs.bk/` (its first probes) is gitignored and not
  in that commit.
- **Harness:** MR !16 (provider-parity). Both providers fill every role (see
  `config.json`); effort `high`; `parallel` 2. Both subscriptions are the $20
  plans: usage windows are the binding constraint.
- **Smoke tests passed** with real CLIs, in host and Docker mode: a Claude and
  a Codex referee on a toy proof, and a Codex librarian whose search showed up
  as native `web_search`.
- **Corpus (`papers/`):** Vaughan 2005, Brüdern–Wooley 2011, BGP+ 1998
  (gitignored). Further works only through the literature step.
- **Literature cutoff:** agents may use only literature from 2010 or earlier,
  plus `papers/`.
- **Not decided yet:** `isolation.mode` (host or docker) for the run. Choose
  before the first agent and keep it for the whole run.
- **Next:** merge MR !16, then from the main checkout (the first real command
  ties `runs_dir` to that checkout) start a new `logs/interventions.md` and run
  step 1 of the procedure: `probe`, `numerics`, `literature`.
