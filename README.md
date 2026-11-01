# sqf-sparse: a proof harness for Claude Code and Codex

A file-based research workflow for the sparse variance of squarefree numbers
in arithmetic progressions to polynomial moduli (`problem.md`). Either provider
can do every role. Use both, Claude only, or Codex only; the Python driver uses
only the standard library.

An agent is a fresh `claude -p` or `codex exec` process. Planners propose
propositions with explicit dependency contracts. Provers see dependency
statements, not their proofs. Two fresh referee sessions inspect each proof.
Independent integrators check the complete argument. Markus chooses plans,
accepts numerical evidence, decides statement changes and judges the result.
Model agreement is evidence, not a proof checker.

## Layout

```
AGENTS.md            shared instructions for the interactive operator
CLAUDE.md            points Claude Code to AGENTS.md
RUN_STATE.md         historical snapshot, not current run authority
problem.md           mathematical question
papers/              supplied PDFs (gitignored)
prompts/             role prompts, exclusion rules and JSON schemas
hints/               strategy hints
variants/            optional prompt/hint overrides
config.json          models, capabilities, effort, isolation and limits
orchestrate.py       orchestration and state transitions
harness_support.py   JSON validation and hashing helpers
isolation/           optional Docker image and per-invocation runner
numerics/            independent candidates and operator-selected evidence
plans/               plans and cache provenance
plan.json            selected plan
props/P*/            statements, proof versions, reviews, objections, approval hashes
runs/                symlink to external working directories and _records/
logs/                costs/tokens, probes, exclusions and interventions
report/              independent integration reports; STALE if outdated
archive/<label>/     permanent run record, excluding paper PDFs
tests/               stub CLIs and temporary-checkout regression tests
```

## Setup

Check Python 3.10+, and the installed versions of the providers you enable:

```sh
python3 --version
claude --version
codex --version
```

Log in with `claude` and/or `codex login`. No Claude installation is necessary
for Codex-only runs. Subscription usage and model availability depend on your
account. Claude's USD budget flag does not meter Codex; Codex tokens are logged
separately. Effort labels across providers are not equal compute budgets.

Put the approved papers into `papers/`:

- Brüdern–Wooley 2011: <https://www.math.purdue.edu/~twooley/publ/2011sparse.pdf>
- BGP+ 1998: <https://www.math.purdue.edu/~twooley/publ/1998%20kfree.pdf>
- arXiv:1912.04683: <https://arxiv.org/pdf/1912.04683>

Vaughan 2005 is paywalled; if supplied, update the availability paragraph in
`problem.md`. Supply text extractions alongside PDFs when useful; the Docker
image includes `pdftotext` so both providers can inspect the same corpus.

Before spending subscription usage, run:

```sh
tests/dry_run.sh
```

Tests use temporary copies, never the current experiment. They cover mixed,
Claude-only and Codex-only workflows, including integration, schema failures,
stale approvals, process cleanup and the global concurrency limit. Stub success
does not verify live provider tool discovery or mathematical quality.

## Running one experiment

Read each step's outputs before proceeding.

1. `./orchestrate.py probe`: memory-only contamination probes for enabled models.
   Read `logs/probe-*.md`. Recall of excluded work can taint a run; a negative
   probe cannot establish absence of pretraining contamination.
2. `./orchestrate.py numerics`: configured models independently compute numerical
   candidates under `numerics/candidates/<model>/`. Compare implementations,
   brute-force small cases and rerun the code. Counts and fits have different
   reliability; investigate disagreement rather than deciding by model vote.
3. `./orchestrate.py numerics --accept <candidate>`: explicitly promote a reviewed
   candidate, e.g. `codex-gpt-6.1-sol`. Record why in `logs/interventions.md`.
   Acceptance is a human choice, not automated certification. Supporting source
   files are retained. Existing accepted evidence is unchanged until acceptance.
4. `./orchestrate.py plan`: cross every unique configured planner with every hint.
   Base names retain the alternating assignment (`vaughan`, etc.); the additional
   plans use `<hint>@<model>`. `plan --single` runs only the base assignment;
   `plan --cross` explicitly requests the full crossing. Existing matching plans
   are reused. Changed inputs require `plan --refresh` or a fresh experiment.
5. `./orchestrate.py select <plan-name>`: Markus selects a plan. Existing
   propositions must be moved aside before selecting another.
6. `./orchestrate.py prove`: each proposition gets up to `max_rounds` **additional**
   rounds per invocation. Prover models rotate across rounds, so both providers
   can try the hard work. Two independent referee sessions inspect each attempt.
   A defect report can never become an approved proof.
7. For a stuck proposition, read its reviews and objections. Markus may request
   `pollinate P3`, then `prove P3`; change a statement; or replan. Use
   `prove P3 --model codex:gpt-6.1-sol` (or a Claude model) for a targeted attempt.
   `pollinate` also accepts `--model`.
8. `./orchestrate.py integrate`: every unique configured integrator independently
   checks composition and compares constants with accepted numerical evidence.
   Read every `integration-<model>.json` and `assembly-<model>.md`. The summary's
   `composes` is true only if all integrators agree to composition; differing
   theorem statements still need human comparison. `integrate --model <model>`
   requests a single model explicitly.
9. `./orchestrate.py check-leaks`: inspect exposure, attempt, denied and mention
   hits. Exclusion scanning also runs after every invocation. Stop to review an
   exposure before feeding affected outputs into another stage.
10. `./orchestrate.py archive <label>`: after all agents finish, preserve working
    directories, provenance, outputs and logs. Review and commit the archive.

`./orchestrate.py status` shows approvals and usage. Numerical target results
are withheld from provers and referees; planners and integrators can see the
accepted evidence. Independent integration sessions do not see each other.

## Codex only, Claude only, or both

```sh
export BACKENDS=codex
./orchestrate.py probe
./orchestrate.py numerics
# Review candidates, accept one, and follow the remaining steps above.
```

Set `BACKENDS=claude` or `BACKENDS=claude,codex` similarly, or change `backends`
in config.json. Disabled-provider assignments resolve through `fallback`.
The default Claude-to-Codex fallback is `codex:gpt-6.1-sol`. Codex-only thus
uses Sol for every role and two fresh Sol referee sessions. The harness warns
about duplicate referee models: separate sessions do not supply model-family
diversity. To use multiple available Codex models, set explicit `codex:<id>`
entries under `models`; no Claude model is required.

To use Codex as the interactive operator, start `codex` in this repository;
it loads AGENTS.md. Claude Code follows CLAUDE.md's pointer to the same guide.
The operator's provider does not constrain the agent backends.

**Switching backends does not make existing outputs single-provider outputs.**
Archive the current experiment, then start with empty `logs/`, `plans/`,
`plan.json`, `props/`, `numerics/`, `report/` and a fresh external RUNS_DIR.
A separate Git worktree is convenient for this. Always give worktrees distinct
RUNS_DIR values: the driver refuses a directory already owned by another
checkout or containing unclaimed old runs. A legacy run must be archived with
the old harness before migration. Do not copy earlier mathematical results into
a supposedly independent run.

## Capabilities and provider adapters

`capabilities` expresses read, write, compute and research access per role.
Claude receives an explicit built-in tool list and no MCP tools. Codex receives
native search only for research roles, read-only or workspace-write commands,
and no apps, plugins, hooks or internal subagents. Probes have shell execution
and research disabled. The transcript audit rejects tool use in probes, MCP
calls, and online search in offline roles. One role invocation is the accounting
unit; the driver provides the explicit multi-agent structure for both providers.

Read access on Codex uses shell commands; both providers therefore receive
local computation for roles that need files. A read-only command sandbox cannot
write scratch code. Native provider policies and filesystem isolation remain
different mechanisms; inspect live transcripts to verify actual capabilities.

Both providers use strict JSON schemas for plans, verdicts and integration.
Optional fields in the source schemas become required in the emitted schemas;
use empty strings/lists or false when those fields do not apply.
The host validates nested fields, types, enums, dependency IDs and cycles, and
verdict consistency. Codex uses `--output-schema`, `--json` and
`--output-last-message`, and must emit a successful completed turn.
`--ignore-user-config` keeps user config out while preserving login. It does
not imply that global instructions and every other user customization disappear.
See [Codex noninteractive mode](https://learn.chatgpt.com/docs/non-interactive-mode),
[CLI flags](https://learn.chatgpt.com/docs/developer-commands?surface=cli) and
[configuration](https://learn.chatgpt.com/docs/config-file/config-reference).

## Isolation and excluded sources

The excluded thesis, its author's sites, and Dehnert (2015) must not be used.
`prompts/_rules.md` spells out the policy. The leak scanner checks normalized
transcript text, tool calls, results and exposed reasoning summaries. It cannot
inspect hidden reasoning, undo pretraining, guarantee complete tool telemetry,
or prove a source was not used.

**Host mode** (default) is convenient, but working directories are not security
boundaries. Agents can potentially read outside their folders, including other
runs and the repository. Check your global Claude/Codex instructions, skills,
auto memory and rules for contamination. Command sandboxes limit writes and
Codex command networking; Claude's shell deny patterns do not block every
possible network client. Native Codex search has no equivalent of the Claude
fetch deny rules here. Prompts and after-the-fact audits are not domain filters.

**Docker mode** gives each invocation its own filesystem, only its own work
folder, a clean home and the minimum provider login. It never mounts the
repository, siblings, archives, the Docker socket or your full home/config.

```sh
docker build -t sqf-agents:local -f isolation/Dockerfile isolation
# For Claude container sessions only:
claude setup-token
# Set CLAUDE_CODE_OAUTH_TOKEN to that token in your environment (do not commit it).
# Codex uses ~/.codex/auth.json, or set CODEX_AUTH_FILE to a login JSON file.
```

Set `isolation.mode` to `docker` in config.json. The image pins CLI versions
with build arguments and includes Python, GCC, Poppler, git and ripgrep.
Codex's inner command sandbox uses `danger-full-access` **only in Docker** to
avoid requiring nested Linux namespace privileges; the container supplies the
filesystem boundary. Read-only roles also receive a read-only work-folder mount and a separate
output folder. The container still has network access for inference and
research, and model commands can reach that network. Docker mode does **not**
provide a network allowlist, source exclusion proxy or tool-free inference
service. Those require a separate controlled network deployment. For a tightly
controlled corpus experiment, disable research capabilities, keep the filesystem
isolation, and account for this network limitation in the experiment's claims.
Credentials available to a provider process are also accessible to code running
inside its container. Docker removes the container after success or termination;
refreshes to its copied Codex auth are not written back to your host login.

## Approval validity and reproducibility

Approvals bind the current proposition and all transitive dependency contracts,
problem, supplied corpus, proof, referee artifacts and current referee policy. `status`, `prove` and
`integrate` invalidate approvals when these change. Legacy approvals without
hashes require new review. Updating an upstream statement invalidates dependent
approvals. Dependency proofs are not assumptions: changing only an upstream
proof invalidates its own approval, while unchanged contracts remain usable.
Integration cannot proceed until every proposition has a current approval.
Old reports are retained but marked `report/STALE` when their inputs change.

Every invocation has an external `runs/_records/<run>/invocation.json` with its
exact prompt, schema, command, capabilities, config/harness sources, input
hashes, revision and CLI version; `outcome.json` records output hashes and
failure. Authoritative transcripts are also recorded there, outside the agent
mount; per-folder transcript copies remain available for convenience. Symlink
inputs and agent outputs are rejected to prevent host-side promotion from
following links outside the mounted directory. The agent cannot read these
records in Docker mode. Container versions
are captured in each record's `outputs/_container-version.txt`. Archives retain records but omit
paper PDFs; preserve the supplied corpus separately using the recorded hashes.

`parallel` limits **all live agent invocations**, including nested referees.
Timeouts terminate process groups; Docker cleanup also removes the container.
Failed agents retain streams, stderr, provenance and usage records. A failed
batch exits nonzero after keeping successful artifacts; rerun after addressing
the failure or the usage window resets. No automatic mathematical replanning,
usage-limit retries, formal proof checking or automatic publication is provided.
