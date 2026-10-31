#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Multi-agent proof attempt driven by non-interactive Claude Code (`claude -p`),
optionally mixed with Codex CLI agents (`codex exec`) for model diversity.

Every agent is one `claude -p` process run in its own sandbox folder under
runs/, which contains only the files that role is allowed to see. Agents never
talk to each other; all state lives in this directory tree.

Steps (run in order; you read the output between steps):
    ./orchestrate.py probe             contamination check -> logs/probe-*.md
    ./orchestrate.py numerics          exact computations -> numerics/
    ./orchestrate.py plan [--cross]    parallel planners  -> plans/<hint>.json
    ./orchestrate.py select <hint>     split chosen plan  -> props/P*/statement.md
    ./orchestrate.py prove [P3 ...]    prover/referee loop per proposition
    ./orchestrate.py pollinate P3      hint for a stuck proposition, then `prove P3`
    ./orchestrate.py integrate         composition check  -> report/
    ./orchestrate.py status            table of where everything stands
    ./orchestrate.py check-leaks       scan all transcripts for excluded sources
    ./orchestrate.py archive [label]   copy the finished run into archive/<label>/
"""
import argparse
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "config.json").read_text())
SCHEMAS = json.loads((ROOT / "prompts" / "schemas.json").read_text())
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
CODEX = os.environ.get("CODEX_BIN", "codex")
CODEX_CFG = CFG.get("codex", {})
RUNS = Path(os.environ.get("RUNS_DIR") or CFG["runs_dir"]).expanduser().resolve()


def log(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


# --------------------------------------------------------------------------
# One agent = one sandbox folder + one `claude -p` process
# --------------------------------------------------------------------------

def sandbox(name, files):
    """Create runs/<name>-<timestamp>/ containing only `files` ({dest: src}).
    Kept after the run so you can see exactly what each agent saw and wrote."""
    d = RUNS / f"{name}-{datetime.now():%Y%m%d-%H%M%S-%f}"
    d.mkdir(parents=True)
    for dest, src in files.items():
        src, target = Path(src), d / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, target)
        elif src.exists():
            shutil.copy(src, target)
    return d


VARIANT = CFG["variant"]
EXCL = CFG["exclusion"]


def variant_file(rel):
    """`variants/<variant>/<rel>` if it exists, else `<rel>` (see variants/README.md)."""
    v = ROOT / "variants" / VARIANT / rel
    return v if v.exists() else ROOT / rel


def build_prompt(role, task="", rules=True):
    prompt = variant_file(f"prompts/{role}.md").read_text()
    if rules:
        prompt += "\n\n" + (ROOT / "prompts" / "_rules.md").read_text()
    if task:
        prompt += f"\n\n## This run\n\n{task}\n"
    return prompt


def build_cmd(prompt, tools, model, schema=None):
    """The `claude -p` invocation. Restrictions, all tested on Claude Code:

    --tools               the agent sees only these built-in tools (--allowedTools
                          alone merely pre-approves; Task, Skill etc. stay visible)
    --strict-mcp-config   no MCP servers from settings or .mcp.json
    mcp__* deny           no MCP tools at all, incl. browser integrations
    WebFetch(domain:...)  deny rules for every blocked domain
    Bash(curl *) etc.     deny rules against fetching around WebFetch
    dontAsk               anything not pre-approved is denied, never prompted
    """
    deny = ["mcp__*"]
    if "WebFetch" in tools:
        deny += [f"WebFetch(domain:{d})" for d in EXCL["blocked_domains"]]
    if "Bash" in tools:
        deny += [f"Bash({b})" for b in EXCL["blocked_bash"]]
    cmd = [
        CLAUDE, "-p", prompt,
        "--model", model,
        "--tools", ",".join(tools),
        "--allowedTools", ",".join(tools),
        "--disallowedTools", *deny,
        "--strict-mcp-config",
        "--settings", json.dumps({"disableAllHooks": True}),   # no user hooks in agents
        "--permission-mode", "dontAsk",
        "--output-format", "stream-json", "--verbose",   # full transcript, for auditing
        "--max-budget-usd", str(CFG["max_budget_usd"]),
    ]
    if schema:
        cmd += ["--json-schema", json.dumps(SCHEMAS[schema])]
    return cmd


def run_agent(role, workdir, model, effort, task="", schema=None, tools=None, rules=True):
    """Run one agent to completion. Returns the final `result` message.

    The full stream (every tool call and tool result) is written to
    <workdir>/_stream.jsonl as it arrives, so a killed or failed agent keeps its
    transcript, and is scanned for leaks of excluded sources. Failed runs are
    logged in costs.jsonl too, with the reason in `failure`."""
    tools = CFG["tools"][role] if tools is None else tools
    prompt = build_prompt(role, task, rules)
    kind, name = backend(model)
    if kind == "codex":
        if schema:
            prompt += codex_schema_note(schema)
        cmd = build_codex_cmd(prompt, tools, name, effort, workdir)
        env = dict(os.environ)
    else:
        cmd = build_cmd(prompt, tools, name, schema)
        env = dict(os.environ, CLAUDE_CODE_EFFORT_LEVEL=effort,
                   ENABLE_CLAUDEAI_MCP_SERVERS="false")   # no claude.ai connectors

    t0 = time.time()
    with open(workdir / "_stream.jsonl", "w") as stdout, open(workdir / "_stderr.txt", "w") as stderr:
        p = subprocess.Popen(cmd, cwd=workdir, env=env, stdin=subprocess.DEVNULL,
                             stdout=stdout, stderr=stderr, text=True)
        try:
            p.wait(timeout=CFG["timeout_s"])
            failure = f"exited {p.returncode}" if p.returncode != 0 else None
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            failure = f"timed out after {CFG['timeout_s']}s"
    stream = (workdir / "_stream.jsonl").read_text()
    out = parse_codex(stream, workdir, schema) if kind == "codex" else parse_stream(stream)
    if not failure and (out is None or out.get("is_error")
                        or out.get("subtype", "success") != "success"):   # e.g. budget exhausted
        failure = f"gave no usable result ({(out or {}).get('subtype', 'no result message')})"
    hits = scan_leaks(workdir)
    if hits:
        log(f"  WARNING: {len(hits)} possible leak(s) in runs/{workdir.name}; "
            "run `./orchestrate.py check-leaks`")

    with open(ROOT / "logs" / "costs.jsonl", "a") as fh:
        fh.write(json.dumps({
            "time": datetime.now().isoformat(timespec="seconds"),
            "role": role, "model": model, "effort": effort, "variant": VARIANT,
            "run": workdir.name, "seconds": round(time.time() - t0),
            "cost_usd": (out or {}).get("total_cost_usd"), "leak_hits": len(hits),
            "backend": kind, "tokens": (out or {}).get("tokens"), "failure": failure,
        }) + "\n")
    if failure:
        stderr_tail = (workdir / "_stderr.txt").read_text()[-500:]
        raise RuntimeError(f"{role} in {workdir.name} {failure}: {stderr_tail}")
    return out


def parse_stream(text):
    """The last `result` message of a stream-json transcript, or None."""
    result = None
    for line in text.splitlines():
        try:
            m = json.loads(line)
        except json.JSONDecodeError:
            continue
        if m.get("type") == "result":
            result = m
    return result


# --------------------------------------------------------------------------
# Codex backend: model "codex" or "codex:<model>" in config.json
# --------------------------------------------------------------------------

def backend(model):
    """'codex' / 'codex:<model>' -> ('codex', <model> or None); else ('claude', model)."""
    if model == "codex" or model.startswith("codex:"):
        return "codex", model.partition(":")[2] or None
    return "claude", model


def enabled_backends():
    """BACKENDS=claude,codex in the environment overrides `backends` in config.json."""
    env = os.environ.get("BACKENDS")
    return [b.strip() for b in env.split(",")] if env else CFG.get("backends", ["claude", "codex"])


def resolve(model):
    """A model of a disabled backend is replaced by that backend's `fallback`."""
    kind = backend(model)[0]
    if kind in enabled_backends():
        return model
    alt = CFG.get("fallback", {}).get(kind)
    if not alt or backend(alt)[0] not in enabled_backends():
        sys.exit(f"model {model!r}: backend '{kind}' is disabled and has no enabled fallback")
    return alt


def role_models(role):
    """The configured model(s) for a role, after the backend switch."""
    m = CFG["models"][role]
    return [resolve(x) for x in m] if isinstance(m, list) else resolve(m)


def build_codex_cmd(prompt, tools, model, effort, workdir):
    """The `codex exec` invocation (flags checked against codex-cli 0.166.0).

    Codex has no per-tool whitelist, so a role's tool list maps onto a sandbox
    mode: any of Write/Edit/Bash -> workspace-write (writes only inside the
    sandbox folder), otherwise read-only. Both modes block network access from
    commands. Codex has no per-domain deny rules either, so web search is off
    for every Codex agent (`codex.extra_args`), and --ignore-user-config keeps
    MCP servers and settings from ~/.codex/config.toml out."""
    writes = any(t in tools for t in ("Write", "Edit", "Bash"))
    cmd = [CODEX, "exec", "--json", "--skip-git-repo-check",
           "--sandbox", "workspace-write" if writes else "read-only",
           "--cd", str(workdir),
           "--output-last-message", str(workdir / "_last.txt"),
           "-c", f'model_reasoning_effort="{CODEX_CFG["effort"][effort]}"',
           *CODEX_CFG.get("extra_args", [])]
    if model:
        cmd += ["--model", model]
    return cmd + [prompt]


def codex_schema_note(schema):
    """Codex's --output-schema needs strict schemas (every property required);
    ours have optional fields, so the final message carries the JSON instead."""
    return ("\n\n## Structured output\n\nEnd with a final message that is exactly one JSON "
            "object matching this JSON schema: no prose before or after it, no code "
            f"fence.\n\n```json\n{json.dumps(SCHEMAS[schema], indent=2)}\n```\n")


def parse_codex(text, workdir, schema):
    """A `codex exec --json` transcript in the shape of Claude's `result`
    message: result, structured_output, and token counts instead of a cost."""
    msgs, tokens = [], {"input": 0, "output": 0}
    for line in text.splitlines():
        try:
            m = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = m.get("item") or {}
        if m.get("type") == "item.completed" and item.get("type") == "agent_message":
            msgs.append(item.get("text", ""))
        elif m.get("type") == "turn.completed":
            u = m.get("usage") or {}
            tokens["input"] += u.get("input_tokens") or 0
            tokens["output"] += u.get("output_tokens") or 0
    last = workdir / "_last.txt"
    result = last.read_text() if last.exists() else (msgs[-1] if msgs else None)
    if result is None:
        return None
    out = {"result": result, "total_cost_usd": None, "tokens": tokens}
    if schema:
        s = result.strip()
        try:
            obj = json.loads(s[s.find("{"): s.rfind("}") + 1])
        except json.JSONDecodeError:
            return None
        if not isinstance(obj, dict) or any(k not in obj for k in SCHEMAS[schema]["required"]):
            return None
        out["structured_output"] = obj
    return out


# --------------------------------------------------------------------------
# Leak detection: did any agent see or seek an excluded source?
# --------------------------------------------------------------------------

# Paths of runs_dir as they appear in transcripts, longest first; masked in scans.
RUNS_PATHS = sorted({str(RUNS), str(RUNS).replace(str(Path.home()), "~"),
                     os.environ.get("RUNS_DIR") or CFG["runs_dir"]}, key=len, reverse=True)

_STRIP = str.maketrans("", "", "$\\{}*_`-‐‑‒–—")


def _norm(s):
    """Lower-case, drop LaTeX/Markdown markup, hyphens and dashes, collapse
    whitespace: 'Square-free', '$k$-free' and 'k‐free' all match."""
    return " ".join(s.lower().translate(_STRIP).split())


def _flat(obj):
    """Every string in a JSON value, joined; unlike json.dumps, no escaping
    of non-ASCII characters or newlines."""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return " ".join(_flat(v) for v in obj.values())
    if isinstance(obj, list):
        return " ".join(_flat(v) for v in obj)
    return "" if obj is None else str(obj)


def _blocks(m):
    msg = m.get("message")
    content = msg.get("content") if isinstance(msg, dict) else None
    return content if isinstance(content, list) else []


def _events(m):
    """(kind, text) pairs from one transcript line, Claude or Codex format."""
    item = m.get("item")
    if isinstance(item, dict):                          # `codex exec --json`
        if m.get("type") != "item.completed":
            return
        t = item.get("type")
        if t in ("agent_message", "reasoning"):
            yield "mention", item.get("text", "")
        elif t != "user_message":                       # commands, searches, file changes
            out = _flat(item.get("aggregated_output") or item.get("output") or item.get("result") or "")
            call = {k: v for k, v in item.items()
                    if k not in ("id", "aggregated_output", "output", "result")}
            yield "attempt", _flat(call)
            if out:
                yield ("denied" if "denied" in out.lower()[:200] else "exposure"), out
        return
    for b in _blocks(m):
        if b.get("type") == "tool_use":
            yield "attempt", f"{b.get('name')}: {_flat(b.get('input'))}"
        elif b.get("type") == "tool_result":
            text = _flat(b.get("content"))
            yield ("denied" if "denied" in text.lower()[:200] else "exposure"), text
        elif b.get("type") == "text" and m.get("type") == "assistant":
            yield "mention", b.get("text", "")
        elif b.get("type") == "thinking" and m.get("type") == "assistant":
            yield "mention", b.get("thinking", "")      # recall may show only here


def scan_leaks(workdir):
    """Find leak patterns in what the agent *did* (tool calls, its own text)
    and what it *saw* (tool results). The prompt itself names the excluded
    author, so the initial prompt is not scanned. Denied fetches show up as
    'attempt' hits with a denial result; those were blocked, but still worth
    knowing about."""
    f = workdir / "_stream.jsonl"
    if not f.exists():
        return []
    pats = [_norm(p) for p in EXCL["leak_patterns"]]
    hits = []
    for line in f.read_text().splitlines():
        try:
            m = json.loads(line)
        except json.JSONDecodeError:
            continue
        for kind, text in _events(m):
            for own in RUNS_PATHS:                      # the sandbox's own path is not a leak
                text = text.replace(own, "<runs>")
            low = _norm(text)
            for pat in pats:
                i = low.find(pat)
                if i >= 0:
                    hits.append({"run": workdir.name, "kind": kind, "pattern": pat,
                                 "context": low[max(0, i - 120): i + 120]})
    return hits


def check_runs_dir():
    """Sandboxes must not sit inside a git work tree: an agent with Bash could
    otherwise read the repository's history (thesis-informed prompts, commit
    messages about the answer). runs/ in the repo is a symlink to RUNS."""
    RUNS.mkdir(parents=True, exist_ok=True)
    try:
        p = subprocess.run(["git", "-C", str(RUNS), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
        if p.returncode == 0:
            sys.exit(f"runs_dir {RUNS} is inside the git work tree {p.stdout.strip()}; "
                     "set runs_dir in config.json, or RUNS_DIR, to a path outside any repository")
    except FileNotFoundError:       # no git installed, so no git history to read either
        pass
    link = ROOT / "runs"
    if link.is_symlink():
        if link.resolve() != RUNS:              # e.g. left over from a dry run
            link.unlink()
            link.symlink_to(RUNS, target_is_directory=True)
    elif link.exists():
        log(f"note: runs/ is a directory from an older version; new runs go to {RUNS}")
    else:
        link.symlink_to(RUNS, target_is_directory=True)


def cmd_check_leaks(_):
    """Scan every run. 'exposure' is the serious kind: excluded material reached
    an agent. Read the context and decide whether that run's output is tainted."""
    all_hits = []
    for d in sorted(RUNS.iterdir()):
        all_hits += scan_leaks(d)
    (ROOT / "logs" / "leaks.json").write_text(json.dumps(all_hits, indent=2))
    if not all_hits:
        log("no leak patterns found in any run")
        return
    for h in all_hits:
        print(f"{h['kind']:9} {h['pattern']:22} {h['run']}\n          ...{h['context']!r}...")
    kinds = {k: sum(h["kind"] == k for h in all_hits) for k in ("exposure", "attempt", "denied", "mention")}
    log(f"{len(all_hits)} hits {kinds}; details in logs/leaks.json")


def parallel(fn, items):
    with cf.ThreadPoolExecutor(max_workers=CFG["parallel"]) as ex:
        futures = {ex.submit(fn, it): it for it in items}
        results = {}
        for fut in cf.as_completed(futures):
            it = futures[fut]
            try:
                results[it] = fut.result()
            except Exception as e:      # one failed agent must not kill the batch
                log(f"  {it}: ERROR {e}")
                results[it] = None
        return results


# --------------------------------------------------------------------------
# Steps
# --------------------------------------------------------------------------

def cmd_probe(_):
    """Contamination check, run before anything else: does a fresh model, with
    no tools, no files and no exclusion rules, already know a result for V_f
    (e.g. from pretraining)? Read logs/probe-<model>.md before trusting a run."""
    def one(model):
        tag = model.replace(":", "-")
        wd = sandbox(f"probe-{tag}", {})
        out = run_agent("probe", wd, model, CFG["effort"]["probe"], rules=False)
        (ROOT / "logs" / f"probe-{tag}.md").write_text(out.get("result", ""))
        return "ok"
    for model, res in parallel(one, list(dict.fromkeys(role_models("probe")))).items():
        log(f"probe {model}: {res}; read logs/probe-{model.replace(':', '-')}.md")


def cmd_numerics(_):
    wd = sandbox("numerics", {"problem.md": ROOT / "problem.md"})
    log(f"numerics agent in runs/{wd.name}")
    run_agent("numerics", wd, role_models("numerics"), CFG["effort"]["numerics"])
    if not (wd / "results.json").exists():
        sys.exit("numerics agent did not write results.json")
    out = ROOT / "numerics"
    out.mkdir(exist_ok=True)
    for f in ("results.json", "compute.py", "README.md"):
        if (wd / f).exists():
            shutil.copy(wd / f, out / f)
    log("wrote numerics/results.json")


def common_inputs():
    files = {"problem.md": ROOT / "problem.md", "papers": ROOT / "papers"}
    if (ROOT / "numerics" / "results.json").exists():
        files["results.json"] = ROOT / "numerics" / "results.json"
    return files


def cmd_plan(args):
    """One planner per hint, models alternating; a plan that already exists is
    kept, so a rerun only retries the failures. --cross adds every other
    model on every hint, as plans/<hint>@<model>.json."""
    hints = CFG["variants"][VARIANT]["hints"]
    models = role_models("planner")
    models = models if isinstance(models, list) else [models]
    model_of = {h: models[i % len(models)] for i, h in enumerate(hints)}   # alternate

    pairs = {h: (h, model_of[h]) for h in hints}
    if args.cross:
        pairs |= {f"{h}@{m.removeprefix('codex:')}": (h, m)
                  for h in hints for m in models if m != model_of[h]}
    names = [n for n in pairs if not (ROOT / "plans" / f"{n}.json").exists()]
    log(f"planners to run: {names or 'none'}; {len(pairs) - len(names)} plan(s) already exist")

    def one(name):
        hint, model = pairs[name]
        wd = sandbox(f"plan-{name}", common_inputs() | {"hint.md": variant_file(f"hints/{hint}.md")})
        log(f"planner '{name}' ({model}) in runs/{wd.name}")
        out = run_agent("planner", wd, model, CFG["effort"]["planner"], schema="plan")
        plan = out["structured_output"] | {"model": model}
        (ROOT / "plans" / f"{name}.json").write_text(json.dumps(plan, indent=2))
        (ROOT / "plans" / f"{name}.md").write_text(render_plan(name, plan))
        return len(plan["propositions"])

    for name, n in parallel(one, names).items():
        log(f"plan '{name}': {n} propositions" if n else f"plan '{name}': failed")
    log("read plans/*.md, then run: ./orchestrate.py select <hint>")


def render_plan(hint, plan):
    lines = [f"# Plan: {hint}", "", f"Model: {plan.get('model', '?')}", "", plan["summary"], "",
             "## Main theorem", "", plan["main_theorem"], ""]
    if plan.get("agrees_with_numerics"):
        lines += ["## Numerics check", "", plan["agrees_with_numerics"], ""]
    for p in plan["propositions"]:
        flag = " (CRUX)" if p.get("crux") else ""
        lines += [f"## {p['id']}: {p['title']}{flag}", "",
                  f"Depends on: {', '.join(p['depends_on']) or 'none'}  ",
                  f"Cites: {', '.join(p.get('cites', [])) or 'none'}", "",
                  p["statement"], ""]
        if p.get("risk"):
            lines += [f"*Risk:* {p['risk']}", ""]
    return "\n".join(lines)


def check_acyclic(props):
    ids = {p["id"] for p in props}
    deps = {p["id"]: set(p["depends_on"]) for p in props}
    for pid, ds in deps.items():
        if ds - ids:
            sys.exit(f"{pid} depends on unknown {ds - ids}")
    seen, done = set(), set()

    def visit(n):
        if n in done:
            return
        if n in seen:
            sys.exit(f"dependency cycle through {n}")
        seen.add(n)
        for m in deps[n]:
            visit(m)
        done.add(n)
    for n in deps:
        visit(n)


def cmd_select(args):
    plan = json.loads((ROOT / "plans" / f"{args.hint}.json").read_text())
    check_acyclic(plan["propositions"])
    if (ROOT / "props").exists() and any((ROOT / "props").iterdir()):
        sys.exit("props/ is not empty; move it aside before selecting a new plan")
    shutil.copy(ROOT / "plans" / f"{args.hint}.json", ROOT / "plan.json")
    for p in plan["propositions"]:
        d = ROOT / "props" / p["id"]
        d.mkdir(parents=True)
        (d / "statement.md").write_text(f"# {p['id']}: {p['title']}\n\n{p['statement']}\n")
        (d / "meta.json").write_text(json.dumps(p, indent=2))
        (d / "status.json").write_text(json.dumps({"state": "open", "round": 0}))
    log(f"selected plan '{args.hint}': {len(plan['propositions'])} propositions in props/")


def status(pid):
    return json.loads((ROOT / "props" / pid / "status.json").read_text())


def set_status(pid, **kw):
    s = status(pid) | kw
    (ROOT / "props" / pid / "status.json").write_text(json.dumps(s))


def latest_proof(pid):
    proofs = sorted((ROOT / "props" / pid).glob("proof-v*.md"),
                    key=lambda p: int(p.stem.split("-v")[1]))
    return proofs[-1] if proofs else None


def dep_statements(pid):
    meta = json.loads((ROOT / "props" / pid / "meta.json").read_text())
    return {f"deps/{d}.md": ROOT / "props" / d / "statement.md" for d in meta["depends_on"]}


def prove_one(pid):
    """Prover/referee loop for one proposition.

    Provers see only the *statements* of dependencies (the contracts), so all
    propositions can be attacked in parallel; they do not wait for their
    dependencies to be proved."""
    pdir = ROOT / "props" / pid
    st = status(pid)
    if st["state"] == "passed":
        return "passed"
    objections_file = pdir / "objections.md"

    for rnd in range(st["round"] + 1, st["round"] + 1 + CFG["max_rounds"]):
        # ---- prover ----
        files = common_inputs() | dep_statements(pid) | {"statement.md": pdir / "statement.md"}
        if objections_file.exists():
            files |= {"objections.md": objections_file,
                      "previous-proof.md": latest_proof(pid)}
        if (pdir / "hint.md").exists():
            files["hint.md"] = pdir / "hint.md"
        wd = sandbox(f"prove-{pid}-r{rnd}", files)
        log(f"{pid} round {rnd}: prover")
        run_agent("prover", wd, role_models("prover"), CFG["effort"]["prover"])
        if not (wd / "proof.md").exists():
            log(f"{pid} round {rnd}: prover wrote no proof.md")
            continue
        proof = pdir / f"proof-v{rnd}.md"
        shutil.copy(wd / "proof.md", proof)

        # ---- two referees, independent sandboxes, read-only, in parallel ----
        ref_files = common_inputs() | dep_statements(pid) | {
            "statement.md": pdir / "statement.md", "proof.md": proof}

        def referee(i_model):
            i, model = i_model
            rwd = sandbox(f"referee-{pid}-r{rnd}-{i}", ref_files)
            out = run_agent("referee", rwd, model, CFG["effort"]["referee"],
                            schema="verdict")
            v = out["structured_output"] | {"model": model}
            (pdir / f"review-v{rnd}-{i}.json").write_text(json.dumps(v, indent=2))
            return v

        with cf.ThreadPoolExecutor(2) as ex:
            verdicts = list(ex.map(referee, enumerate(role_models("referees"))))
        log(f"{pid} round {rnd}: " + ", ".join(f"{v['model']}={v['verdict']}/{v['severity']}"
                                                for v in verdicts))

        if all(v["verdict"] == "pass" for v in verdicts):
            defect = any(v["severity"] == "defect-confirmed" for v in verdicts)
            set_status(pid, state="defect" if defect else "passed", round=rnd)
            return "defect" if defect else "passed"

        # ---- objections feed the next round ----
        with open(objections_file, "a") as fh:
            fh.write(f"\n## Round {rnd} (against proof-v{rnd})\n\n")
            for v in verdicts:
                if v["verdict"] == "fail":
                    fh.write(f"**Referee ({v['model']}), {v['severity']}** at: "
                             f"{v.get('location', '?')}\n\n{v.get('objection', '')}\n\n")
                    for o in v.get("other_issues", []):
                        fh.write(f"- {o}\n")
                    fh.write("\n")
        set_status(pid, state="open", round=rnd)

    set_status(pid, state="stuck")
    return "stuck"


def cmd_prove(args):
    refs = role_models("referees")
    if len(set(refs)) < 2:
        log(f"WARNING: both referees are {refs[0]}; set `fallback` to keep them different models")
    pids = args.props or sorted(p.name for p in (ROOT / "props").iterdir())
    pids = [p for p in pids if status(p)["state"] != "passed"]
    for pid, res in parallel(prove_one, pids).items():
        log(f"{pid}: {res}")
    stuck = [p for p in pids if status(p)["state"] in ("stuck", "defect")]
    if stuck:
        log(f"needs you: {stuck}. Read their objections.md; try `pollinate`.")


def cmd_pollinate(args):
    pdir = ROOT / "props" / args.prop
    wd = sandbox(f"pollinate-{args.prop}", {
        "statement.md": pdir / "statement.md",
        "history.md": pdir / "objections.md",
        "plans": ROOT / "plans",
    })
    out = run_agent("pollinator", wd, role_models("pollinator"),
                    CFG["effort"]["pollinator"], schema="pollination")
    v = out["structured_output"]
    if (wd / "hint.md").exists():
        shutil.copy(wd / "hint.md", pdir / "hint.md")
    log(f"{args.prop}: {v['diagnosis']}: {v['summary']}")
    if v["needs_replan"]:
        log("statement needs changing: edit props/{0}/statement.md and its dependents by hand"
            .format(args.prop))
    else:
        set_status(args.prop, state="open")
        log(f"wrote props/{args.prop}/hint.md; now run: ./orchestrate.py prove {args.prop}")


def cmd_integrate(_):
    pids = sorted(p.name for p in (ROOT / "props").iterdir())
    open_ = [p for p in pids if status(p)["state"] != "passed"]
    if open_:
        sys.exit(f"not all propositions passed: {open_}")
    files = common_inputs() | {"plan.json": ROOT / "plan.json"}
    for p in pids:
        files[f"props/{p}/statement.md"] = ROOT / "props" / p / "statement.md"
        files[f"props/{p}/proof.md"] = latest_proof(p)
    wd = sandbox("integrate", files)
    out = run_agent("integrator", wd, role_models("integrator"), CFG["effort"]["integrator"],
                    schema="integration")
    v = out["structured_output"]
    rep = ROOT / "report"
    rep.mkdir(exist_ok=True)
    (rep / "integration.json").write_text(json.dumps(v, indent=2))
    if (wd / "assembly.md").exists():
        shutil.copy(wd / "assembly.md", rep / "assembly.md")
    log(f"composes: {v['composes']}")
    log(f"final theorem: {v['final_theorem']}")


def cmd_archive(args):
    """Copy every sandbox in runs_dir and the run's outputs into the repo under
    archive/<label>/, for review and committing. Run it once no agent is running.
    Agents of later runs can't reach the archive, since they can't read git.
    PDFs from papers/ are left out: they are not ours to redistribute."""
    label = args.label or f"{datetime.now():%Y%m%d-%H%M}-{VARIANT}"
    dest = ROOT / "archive" / label
    if dest.exists():
        sys.exit(f"archive/{label} exists; pass another label")
    skip = shutil.ignore_patterns("papers")
    n = 0
    for d in sorted(RUNS.iterdir()):
        if d.is_dir():
            shutil.copytree(d, dest / "runs" / d.name, ignore=skip)
            n += 1
    for name in ("config.json", "plan.json", "numerics", "plans", "props", "report", "logs"):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, dest / name, ignore=skip)
        elif src.exists():
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest / name)
    log(f"archived {n} sandboxes and the run's outputs to archive/{label}/; "
        "review, then git add it")


def cmd_status(_):
    if not (ROOT / "props").exists():
        print("no plan selected yet")
    else:
        print(f"{'prop':6} {'state':8} {'round':>5}  title")
        for d in sorted((ROOT / "props").iterdir()):
            s, m = status(d.name), json.loads((d / "meta.json").read_text())
            crux = " [crux]" if m.get("crux") else ""
            print(f"{d.name:6} {s['state']:8} {s['round']:>5}  {m['title']}{crux}")
    cost_file = ROOT / "logs" / "costs.jsonl"
    if cost_file.exists():
        rows = [json.loads(l) for l in cost_file.read_text().splitlines()]
        total = sum(r["cost_usd"] or 0 for r in rows)
        print(f"\n{len(rows)} agent runs, ${total:.2f} total (Claude)")
        cx = [r for r in rows if r.get("backend") == "codex"]
        if cx:
            tok = sum((r.get("tokens") or {}).get("output", 0) for r in cx)
            print(f"{len(cx)} of them Codex: {tok:,} output tokens (Codex reports no USD cost)")


def main():
    for d in ("logs", "plans", "papers"):
        (ROOT / d).mkdir(exist_ok=True)
    check_runs_dir()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe").set_defaults(fn=cmd_probe)
    sub.add_parser("check-leaks").set_defaults(fn=cmd_check_leaks)
    sub.add_parser("numerics").set_defaults(fn=cmd_numerics)
    s = sub.add_parser("plan"); s.add_argument("--cross", action="store_true"); s.set_defaults(fn=cmd_plan)
    s = sub.add_parser("select"); s.add_argument("hint"); s.set_defaults(fn=cmd_select)
    s = sub.add_parser("prove"); s.add_argument("props", nargs="*"); s.set_defaults(fn=cmd_prove)
    s = sub.add_parser("pollinate"); s.add_argument("prop"); s.set_defaults(fn=cmd_pollinate)
    sub.add_parser("integrate").set_defaults(fn=cmd_integrate)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    s = sub.add_parser("archive"); s.add_argument("label", nargs="?"); s.set_defaults(fn=cmd_archive)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
