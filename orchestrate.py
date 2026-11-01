#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Multi-agent proof attempt using Claude Code and/or Codex CLI.

Every agent is a fresh process in its own working folder under runs/.
Use container isolation to prevent access to files outside that folder. Agents never
talk to each other; all state lives in this directory tree.

Steps (run in order; you read the output between steps):
    ./orchestrate.py probe             contamination check -> logs/probe-*.md
    ./orchestrate.py numerics          exact computations -> numerics/
    ./orchestrate.py literature        literature search -> literature/review.md
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
import re
import shutil
import signal
import threading
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from harness_support import strict_schema, validate, validate_verdict, digest, hash_json, input_hashes, artifact_files

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "config.json").read_text())
SCHEMAS = {k: strict_schema(v) for k, v in json.loads((ROOT / "prompts" / "schemas.json").read_text()).items()}
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
CODEX = os.environ.get("CODEX_BIN", "codex")
CODEX_CFG = CFG.get("codex", {})
RUNS = Path(os.environ.get("RUNS_DIR") or CFG["runs_dir"]).expanduser().resolve()
AGENT_SLOTS = threading.BoundedSemaphore(CFG["parallel"])
VERSION_LOCK = threading.Lock()
VERSIONS = {}


def log(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


# --------------------------------------------------------------------------
# One agent = one working folder + one provider CLI process
# --------------------------------------------------------------------------

def sandbox(name, files):
    """Create runs/<name>-<timestamp>/ containing only `files` ({dest: src}).
    Kept after the run so you can see exactly what each agent saw and wrote."""
    d = RUNS / f"{name}-{datetime.now():%Y%m%d-%H%M%S-%f}"
    d.mkdir(parents=True)
    for dest, src in files.items():
        src, target = Path(src), d / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        if src.is_symlink() or src.is_dir() and any(p.is_symlink() for p in src.rglob("*")):
            raise ValueError(f"symlink input is not supported: {src}")
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


def role_capabilities(role):
    return CFG["capabilities"][role]


def claude_tools(caps):
    tools = []
    if caps["read"]:
        tools += ["Read"]
    if caps["write"]:
        tools += ["Write", "Edit"]
    if caps["compute"]:
        tools += ["Bash"]
    if caps["research"]:
        tools += ["WebSearch", "WebFetch"]
    return tools


def capability_violations(stream, kind, caps):
    violations = []
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if kind == "codex":
            item = event.get("item") or {}
            t = item.get("type")
            if event.get("type") not in ("item.started", "item.completed"):
                continue
            if t == "mcp_tool_call":
                violations.append("unexpected MCP tool")
            if t == "web_search" and not caps["research"]:
                violations.append("web search in an offline role")
            if not any(caps.values()) and t not in ("agent_message", "reasoning", None):
                violations.append(f"tool {t} in memory-only probe")
        else:
            for block in _blocks(event):
                if block.get("type") == "tool_use" and block.get("name") not in claude_tools(caps):
                    violations.append(f"unexpected tool {block.get('name')}")
    return sorted(set(violations))


def cli_version(binary):
    with VERSION_LOCK:
        if binary not in VERSIONS:
            try:
                p = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=10)
                VERSIONS[binary] = p.stdout.strip() if p.returncode == 0 else "unavailable"
            except (OSError, subprocess.TimeoutExpired):
                VERSIONS[binary] = "unavailable"
        return VERSIONS[binary]


def source_snapshot():
    # Include exact harness sources, not just HEAD (which may have local changes).
    names = ["orchestrate.py", "harness_support.py", "config.json", "problem.md", "prompts/schemas.json"]
    names += [f"prompts/{r}.md" for r in CFG["capabilities"]] + ["prompts/_rules.md"]
    names += ["isolation/docker_runner.py", "isolation/Dockerfile",
              "agent-env/pyproject.toml", "agent-env/uv.lock"]
    names += [str(p.relative_to(ROOT)) for p in sorted((ROOT / "hints").glob("*.md"))]
    names += [str(p.relative_to(ROOT)) for p in sorted((ROOT / "variants" / VARIANT).rglob("*.md"))]
    return {n: (ROOT / n).read_text() for n in names if (ROOT / n).is_file()}


def run_agent(role, workdir, model, effort, task="", schema=None, rules=True):
    # A single global limit includes nested referee workers.
    with AGENT_SLOTS:
        return _run_agent(role, workdir, model, effort, task, schema, rules)


def _run_agent(role, workdir, model, effort, task, schema, rules):
    caps = role_capabilities(role)
    prompt = build_prompt(role, task, rules)
    kind, name = backend(model)
    mode = CFG.get("isolation", {}).get("mode", "host")
    if mode == "host":
        check_agent_venv()
    if mode not in ("host", "docker"):
        raise ValueError(f"unknown isolation mode {mode!r}")
    agent_dir = Path("/workspace") if mode == "docker" else workdir
    if schema:
        (workdir / "_schema.json").write_text(json.dumps(SCHEMAS[schema], indent=2))
    if kind == "codex":
        cmd = build_codex_cmd(prompt, caps, name, effort, agent_dir, schema)
        env = dict(os.environ)
    else:
        cmd = build_cmd(prompt, claude_tools(caps), name, schema)
        env = dict(os.environ, CLAUDE_CODE_EFFORT_LEVEL=effort,
                   ENABLE_CLAUDEAI_MCP_SERVERS="false")
    if mode == "host":
        venv = agent_venv()
        if venv:
            env |= {"VIRTUAL_ENV": str(venv),
                    "PATH": f"{venv / 'bin'}{os.pathsep}{env.get('PATH', '')}",
                    "ZDOTDIR": str(venv), "BASH_ENV": ""}
    invocation = list(cmd)
    if mode == "docker":
        invocation[0] = kind
        cmd = [sys.executable, str(ROOT / "isolation" / "docker_runner.py"),
               "--image", CFG["isolation"]["image"], "--workdir", str(workdir),
               "--backend", kind, "--outputs", str(RUNS / "_records" / workdir.name / "outputs"),
               *(["--readonly-workspace"] if not caps["write"] else []), "--", *cmd]
    try:
        revision = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                           text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = None
    manifest = {"role": role, "model": model, "effort": effort, "capabilities": caps,
                "isolation": mode, "command": invocation, "launch_command": cmd, "prompt": prompt,
                "schema": SCHEMAS.get(schema), "inputs": input_hashes(workdir),
                "revision": revision, "sources": source_snapshot(),
                "agent_environment": {"venv": str(agent_venv()) if mode == "host" and agent_venv() else "/opt/agent-venv" if mode == "docker" else None,
                                      "lock_hash": digest(ROOT / "agent-env/uv.lock")},
                "cli_version": cli_version(CODEX if kind == "codex" else CLAUDE) if mode == "host" else "see outputs/_container-version.txt"}
    # Records live outside the agent's directory so operator metadata cannot leak in.
    record = RUNS / "_records" / workdir.name
    record.mkdir(parents=True, exist_ok=True)
    (record / "invocation.json").write_text(json.dumps(manifest, indent=2))
    t0, failure, out = time.time(), None, None
    try:
        with open(record / "_stream.jsonl", "w") as stdout, open(record / "_stderr.txt", "w") as stderr:
            p = subprocess.Popen(cmd, cwd=workdir, env=env, stdin=subprocess.DEVNULL,
                                 stdout=stdout, stderr=stderr, text=True, start_new_session=True)
            try:
                p.wait(timeout=CFG["timeout_s"])
                if p.returncode != 0:
                    failure = f"exited {p.returncode}"
            except subprocess.TimeoutExpired:
                # TERM lets the container runner remove its container, then kill leftovers.
                os.killpg(p.pid, signal.SIGTERM)
                try:
                    p.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                p.wait()
                failure = f"timed out after {CFG['timeout_s']}s"
        stream = (record / "_stream.jsonl").read_text()
        if any(p.is_symlink() for p in workdir.rglob("*")):
            raise ValueError("agent outputs contain symlinks; refusing to read or promote them")
        out = parse_codex(stream, workdir, schema) if kind == "codex" else parse_stream(stream)
        if not failure and (out is None or out.get("is_error") or out.get("subtype", "success") != "success"):
            failure = "gave no usable successful result"
        if not failure:
            violations = capability_violations(stream, kind, caps)
            if violations:
                raise ValueError("capability violation: " + "; ".join(violations))
        if not failure and schema:
            value = out.get("structured_output")
            validate(value, SCHEMAS[schema])
            if schema == "verdict":
                validate_verdict(value)
            elif schema == "plan":
                check_acyclic(value["propositions"])
    except (OSError, ValueError, TypeError, KeyError) as e:
        failure = str(e)
    # Compatibility copies are written only after the process exits; the authoritative
    # transcript is outside the Docker mount and cannot be rewritten by an agent.
    for name in ("_stream.jsonl", "_stderr.txt"):
        src, target = record / name, workdir / name
        if src.exists():
            if target.is_symlink():
                target.unlink()
            if not target.is_dir():
                shutil.copyfile(src, target)
    hits = scan_leaks(workdir)
    if hits:
        log(f"  WARNING: {len(hits)} possible leak(s) in runs/{workdir.name}; run check-leaks")
    (record / "outcome.json").write_text(json.dumps({
        "failure": failure, "outputs": input_hashes(workdir),
        "provider_outputs": input_hashes(record / "outputs") if (record / "outputs").exists() else {}}, indent=2))
    with open(ROOT / "logs" / "costs.jsonl", "a") as fh:
        fh.write(json.dumps({
            "time": datetime.now().isoformat(timespec="seconds"), "role": role,
            "model": model, "effort": effort, "variant": VARIANT, "run": workdir.name,
            "seconds": round(time.time() - t0), "cost_usd": (out or {}).get("total_cost_usd"),
            "leak_hits": len(hits), "backend": kind, "tokens": (out or {}).get("tokens"),
            "failure": failure,
        }) + "\n")
    if failure:
        stderr = record / "_stderr.txt"
        tail = stderr.read_text()[-500:] if stderr.exists() else ""
        raise RuntimeError(f"{role} in {workdir.name} {failure}: {tail}")
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


def build_codex_cmd(prompt, caps, model, effort, workdir, schema=None):
    """Use native search by role; apps/plugins never supply an alternate web route."""
    cmd = [CODEX, "exec", "--json", "--skip-git-repo-check",
           "--sandbox", "workspace-write" if caps["write"] else "read-only",
           "--cd", str(workdir), "--output-last-message", str(Path("/outputs/_last.txt") if CFG.get("isolation", {}).get("mode") == "docker" else workdir / "_last.txt"),
           *CODEX_CFG.get("extra_args", []),
           "-c", f'model_reasoning_effort="{CODEX_CFG["effort"][effort]}"',
           "-c", 'approval_policy="never"',
           "-c", "allow_login_shell=false",
           "-c", 'sandbox_workspace_write.network_access=false',
           "--disable", "apps", "--disable", "plugins", "--disable", "hooks",
           "--disable", "multi_agent", "--disable", "multi_agent_v2",
           "-c", f'features.shell_tool={str(caps["read"] or caps["compute"]).lower()}',
           "-c", 'web_search="live"' if caps["research"] else 'web_search="disabled"']
    if schema:
        cmd += ["--output-schema", str(workdir / "_schema.json")]
    if not any(caps.values()):
        for feature in ("image_generation", "view_image", "browser_use", "in_app_browser", "sleep_tool", "goals"):
            cmd += ["--disable", feature]
    if CFG.get("isolation", {}).get("mode") == "docker":
        cmd[cmd.index("--sandbox") + 1] = "danger-full-access"
    if model:
        cmd += ["--model", model]
    return cmd + [prompt]


def parse_codex(text, workdir, schema):
    """A `codex exec --json` transcript in the shape of Claude's `result`
    message: result, structured_output, and token counts instead of a cost."""
    msgs, tokens, completed, failed = [], {"input": 0, "output": 0, "cached_input": 0}, False, False
    for line in text.splitlines():
        try:
            m = json.loads(line)
        except json.JSONDecodeError:
            continue
        if m.get("type") in ("turn.failed", "error"):
            failed = True
        item = m.get("item") or {}
        if m.get("type") == "item.completed" and item.get("type") == "agent_message":
            msgs.append(item.get("text", ""))
        elif m.get("type") == "turn.completed":
            completed = True
            u = m.get("usage") or {}
            tokens["input"] += u.get("input_tokens") or 0
            tokens["output"] += u.get("output_tokens") or 0
            tokens["cached_input"] += u.get("cached_input_tokens") or 0
    last = workdir / "_last.txt"
    if not last.exists():
        last = RUNS / "_records" / workdir.name / "outputs" / "_last.txt"
    result = last.read_text() if last.exists() else (msgs[-1] if msgs else None)
    if result is None or failed or not completed:
        return None
    out = {"result": result, "total_cost_usd": None, "tokens": tokens}
    if schema:
        s = result.strip()
        try:
            obj = json.loads(s)
        except json.JSONDecodeError:
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


_ARXIV = re.compile(r"arxiv(?:\.org/(?:abs|pdf)/|\s*:\s*|\s+)(\d{2})(\d{2})\.\d{4,5}")


def _post_cutoff(text):
    """New-style arXiv identifiers (arXiv:YYMM.NNNNN) dated after the literature
    cutoff. Only identifiers next to 'arxiv' count, so numbers in tables don't."""
    cut = EXCL.get("literature_cutoff_year")
    if not cut:
        return []
    return [m for m in _ARXIV.finditer(text.lower())
            if 1 <= int(m.group(2)) <= 12 and 2000 + int(m.group(1)) > cut]


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
    f = RUNS / "_records" / workdir.name / "_stream.jsonl"
    if not f.exists():
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
            if not workdir.name.startswith("probe-"):        # probes have no cutoff rule
                for mt in _post_cutoff(text):
                    hits.append({"run": workdir.name, "kind": kind, "pattern": "post-cutoff arxiv",
                                 "context": text[max(0, mt.start() - 120): mt.end() + 120]})
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
    owner = RUNS / "_owner.json"
    if owner.exists():
        if json.loads(owner.read_text())["checkout"] != str(ROOT):
            raise ValueError(f"runs_dir {RUNS} belongs to another checkout; set a fresh RUNS_DIR")
    elif any(RUNS.iterdir()):
        raise ValueError(f"runs_dir {RUNS} contains unclaimed legacy runs; archive with the old harness and choose a fresh RUNS_DIR")
    else:
        owner.write_text(json.dumps({"checkout": str(ROOT)}, indent=2))
    link = ROOT / "runs"
    if link.is_symlink():
        if link.resolve() != RUNS:              # e.g. left over from a dry run
            link.unlink()
            link.symlink_to(RUNS, target_is_directory=True)
    elif link.exists():
        log(f"note: runs/ is a directory from an older version; new runs go to {RUNS}")
    else:
        link.symlink_to(RUNS, target_is_directory=True)


def agent_venv():
    """The agents' Python environment (agent-env/), or None if disabled."""
    v = os.environ.get("AGENT_VENV") or CFG.get("agent_venv")
    return Path(v).expanduser().resolve() if v else None


def check_agent_venv():
    """Refuse to start agents without their Python environment, so that no run
    silently has fewer packages than another; and keep it outside any git work
    tree, since every agent sees its path."""
    v = agent_venv()
    if not v:
        return
    if not (v / "bin" / "python3").exists():
        raise ValueError(f"agent_venv {v} does not exist; build it with\n"
                 f"  UV_PROJECT_ENVIRONMENT={v} uv sync --project agent-env\n"
                 "or set \"agent_venv\": null in config.json to run agents without it")
    try:
        p = subprocess.run(["git", "-C", str(v), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
        if p.returncode == 0:
            raise ValueError(f"agent_venv {v} is inside the git work tree {p.stdout.strip()}; move it out")
    except FileNotFoundError:
        pass


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
        if any(v is None for v in results.values()):
            raise RuntimeError("one or more agents failed; successful artifacts were retained")
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


def model_list(role):
    models = role_models(role)
    return list(dict.fromkeys(models if isinstance(models, list) else [models]))


def model_tag(model):
    return model.replace(":", "-")


def cmd_numerics(args):
    out = ROOT / "numerics"
    out.mkdir(exist_ok=True)
    if args.accept:
        candidate = out / "candidates" / args.accept
        if not (candidate / "results.json").is_file():
            raise ValueError("unknown numerical candidate; use its directory name")
        for name in ("results.json", "compute.py", "README.md"):
            if not (candidate / name).is_file():
                raise ValueError(f"candidate is missing {name}")
        provenance = candidate / "_candidate.json"
        if not provenance.is_file() or json.loads(provenance.read_text())["spec"]["problem"] != digest(ROOT / "problem.md"):
            raise ValueError("numerical candidate was computed for a different problem or lacks provenance")
        # Copy all supporting code, including C sources used by compute.py.
        for name, source in artifact_files(candidate).items():
            destination = out / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(source, destination)
        (out / "accepted.json").write_text(json.dumps({
            "candidate": args.accept, "problem_hash": digest(ROOT / "problem.md"),
            "results_hash": digest(out / "results.json"),
            "artifacts": {name: digest(out / name) for name in artifact_files(candidate)},
            "time": datetime.now().isoformat(), "acceptance": "operator selected; not a proof of numerical correctness"}, indent=2))
        mark_report_stale("Accepted numerical evidence changed; rerun integration.")
        log(f"accepted numerics candidate {args.accept}; record the independent validation in interventions.md")
        return

    def one(model):
        target = out / "candidates" / model_tag(model)
        spec = {"model": model, "problem": digest(ROOT / "problem.md"),
                "prompt": build_prompt("numerics"), "effort": CFG["effort"]["numerics"],
                "capabilities": role_capabilities("numerics")}
        record = target / "_candidate.json"
        if target.exists():
            if record.exists():
                saved = json.loads(record.read_text())
                artifacts = {name: digest(path) for name, path in artifact_files(target).items()}
                if saved == {"spec": spec, "artifacts": artifacts}:
                    return str(target.relative_to(ROOT))
            raise ValueError(f"candidate {target.name} changed or lacks provenance; archive/move it aside before rerunning")
        wd = sandbox(f"numerics-{model_tag(model)}", {"problem.md": ROOT / "problem.md"})
        run_agent("numerics", wd, model, CFG["effort"]["numerics"])
        for name in ("results.json", "compute.py", "README.md"):
            if not (wd / name).is_file():
                raise ValueError(f"numerics agent did not write {name}")
        data = json.loads((wd / "results.json").read_text())
        if not isinstance(data.get("polynomials"), dict) or not isinstance(data.get("validation"), list):
            raise ValueError("malformed numerical results")
        target.mkdir(parents=True)
        for name, source in artifact_files(wd).items():
            destination = target / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(source, destination)
        artifacts = {name: digest(path) for name, path in artifact_files(target).items()}
        record.write_text(json.dumps({"spec": spec, "artifacts": artifacts}, indent=2))
        return str(target.relative_to(ROOT))

    for model, candidate in parallel(one, model_list("numerics")).items():
        log(f"numerics {model}: {candidate}")
    log("compare independent candidates and validate their code, then numerics --accept <candidate-directory-name>")


# Literature search: the librarian lists, the driver vets and downloads.

SHADOW_LIBRARIES = ("sci-hub", "scihub", "libgen", "library.lol", "annas-archive",
                    "z-lib", "zlibrary", "booksc")


def _host(url):
    return (urlparse(url).hostname or "").lower()


def _blocked_host(host):
    for d in (d.lower() for d in EXCL["blocked_domains"]):
        if host == d or (d.startswith("*.") and host.endswith(d[1:])):
            return True
    return any(s in host for s in SHADOW_LIBRARIES)


def vet_item(it):
    """Why a librarian's item must not reach papers/, or None if it may. The
    driver checks this itself instead of trusting the agent's own vetting."""
    cut = EXCL.get("literature_cutoff_year")
    try:
        year = int(it.get("year"))
    except (TypeError, ValueError):
        return "no publication year"
    if cut and year > cut:
        return f"published {year}, after the {cut} cutoff"
    text = " ".join(str(it.get(k) or "") for k in ("authors", "title", "venue", "url", "pdf_url"))
    low = _norm(text)
    for p in EXCL["leak_patterns"]:
        if _norm(p) in low:
            return f"matches excluded pattern '{p}'"
    if _post_cutoff(text):
        return "arXiv identifier after the cutoff"
    for u in (it.get("url"), it.get("pdf_url")):
        if u and _blocked_host(_host(u)):
            return f"blocked host {_host(u)}"
    return None


def fetch_pdf(url, dest, limit=50 * 2**20):
    """Download url to dest if it really is a PDF; None on success, else why not."""
    scheme = urlparse(url).scheme
    if scheme not in ("http", "https") and not (scheme == "file" and os.environ.get("LIT_ALLOW_FILE")):
        return f"unsupported URL scheme {scheme!r}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (literature download)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            if _blocked_host(_host(r.geturl())):
                return f"redirected to blocked host {_host(r.geturl())}"
            data = r.read(limit + 1)
    except Exception as e:                  # network errors, HTTP errors, timeouts
        return f"download failed: {e}"
    if len(data) > limit:
        return "larger than 50 MB"
    if not data.startswith(b"%PDF-"):
        return "not a PDF (probably a landing page or a paywall)"
    dest.write_bytes(data)
    return None


def render_literature(rows, notes):
    sections = {
        "downloaded": "Downloaded: check each, then copy what you want into papers/ and list it in papers/INDEX.md",
        "wishlist": "Wishlist: no open PDF; get the full text if worthwhile, then as above",
        "rejected": "Rejected by the driver (a leak pattern can also hit an unrelated work: check the reason)",
    }
    lines = ["# Literature search", ""] + ([notes, ""] if notes else [])
    for status, title in sections.items():
        lines += [f"## {title}", ""]
        for r in sorted((r for r in rows if r["status"] == status),
                        key=lambda r: -(r.get("relevance") or 0)):
            ref = r.get("url") or r.get("pdf_url") or ""
            lines += [f"- **{r.get('authors', '?')} ({r.get('year', '?')})**, *{r.get('title', '?')}*, "
                      f"{r.get('venue') or ''} [{r.get('kind', '?')}, relevance {r.get('relevance', '?')}]  ",
                      f"  {r.get('why', '')}  ",
                      f"  {ref} ({r['note']})"]
        lines.append("")
    return "\n".join(lines)


def cmd_literature(_):
    """Literature search, after numerics and before planning. A librarian agent
    lists relevant literature up to the cutoff; the driver vets every item,
    downloads open-access PDFs to literature/pdf/ and writes
    literature/review.md. Nothing reaches the other agents until you copy a
    file into papers/ and list it in papers/INDEX.md."""
    lit = ROOT / "literature"
    if (lit / "candidates.json").exists():
        sys.exit("literature/candidates.json exists; move literature/ aside to search again")
    model = role_models("librarian")
    if backend(model)[0] == "codex":
        log("Codex librarian uses native search without domain deny rules; review its transcript and driver-rejected candidates")
    wd = sandbox("literature", {"problem.md": ROOT / "problem.md", "papers": ROOT / "papers"})
    log(f"librarian in runs/{wd.name}")
    out = run_agent("librarian", wd, model, CFG["effort"]["librarian"],
                    schema="literature")
    (lit / "pdf").mkdir(parents=True, exist_ok=True)
    rows = []
    for i, it in enumerate(out["structured_output"].get("items", [])):
        why = vet_item(it)
        if why:
            status = "rejected"
        elif it.get("pdf_url"):
            name = f"{i:02d}-" + re.sub(r"[^A-Za-z0-9._-]+", "_", str(it.get("id") or "item"))[:60] + ".pdf"
            why = fetch_pdf(it["pdf_url"], lit / "pdf" / name)
            status, why = ("downloaded", f"literature/pdf/{name}") if why is None else ("wishlist", why)
        else:
            status, why = "wishlist", f"no open-access PDF ({it.get('access', 'unknown')})"
        rows.append(it | {"status": status, "note": why})
    (lit / "candidates.json").write_text(json.dumps(rows, indent=2))
    (lit / "review.md").write_text(render_literature(rows, out["structured_output"].get("notes", "")))
    counts = {s: sum(r["status"] == s for r in rows) for s in ("downloaded", "wishlist", "rejected")}
    log(f"{len(rows)} items {counts}; read literature/review.md")


def common_inputs(include_numerics=False):
    files = {"problem.md": ROOT / "problem.md", "papers": ROOT / "papers"}
    if include_numerics:
        result, accepted = ROOT / "numerics/results.json", ROOT / "numerics/accepted.json"
        if not accepted.is_file():
            raise ValueError("accept independently validated numerics with numerics --accept <candidate> first")
        acceptance = json.loads(accepted.read_text())
        if acceptance["problem_hash"] != digest(ROOT / "problem.md") or acceptance["results_hash"] != digest(result) or any(
                digest(ROOT / "numerics" / name) != expected for name, expected in acceptance["artifacts"].items()):
            raise ValueError("accepted numerical artifacts changed; validate and accept again")
        files["results.json"] = result
    return files


def cmd_plan(args):
    """Cross models and hints by default; reuse only plans with matching provenance."""
    if not (ROOT / "literature" / "review.md").exists():
        log("note: no literature search yet (./orchestrate.py literature); the planners get only what is in papers/")
    hints = CFG["variants"][VARIANT]["hints"]
    models = role_models("planner")
    models = list(dict.fromkeys(models if isinstance(models, list) else [models]))
    model_of = {h: models[i % len(models)] for i, h in enumerate(hints)}   # alternate

    pairs = {h: (h, model_of[h]) for h in hints}
    if args.cross or CFG.get("planning_cross", False) and not args.single:
        pairs |= {f"{h}@{m.removeprefix('codex:')}": (h, m)
                  for h in hints for m in models if m != model_of[h]}
    records = ROOT / "plans" / "_records"
    records.mkdir(exist_ok=True)
    expected = {}
    for name, (hint, model) in pairs.items():
        files = common_inputs(include_numerics=True) | {"hint.md": variant_file(f"hints/{hint}.md")}
        expected[name] = {"model": model, "effort": CFG["effort"]["planner"],
                          "inputs": {dest: digest(src) for dest, src in files.items()},
                          "prompt": build_prompt("planner"), "schema": SCHEMAS["plan"],
                          "capabilities": role_capabilities("planner"), "exclusion": EXCL,
                          "provider_config": CODEX_CFG if backend(model)[0] == "codex" else {}}
        existing = ROOT / "plans" / f"{name}.json"
        record = records / f"{name}.json"
        if existing.exists() and not args.refresh:
            if not record.exists() or json.loads(record.read_text()) != expected[name]:
                raise ValueError(f"cached plan {name!r} has different inputs/model or lacks provenance; use plan --refresh or a fresh experiment")
    names = [n for n in pairs if args.refresh or not (ROOT / "plans" / f"{n}.json").exists()]
    log(f"planners to run: {names or 'none'}; {len(pairs) - len(names)} plan(s) already exist")

    def one(name):
        hint, model = pairs[name]
        wd = sandbox(f"plan-{name}", common_inputs(include_numerics=True) | {"hint.md": variant_file(f"hints/{hint}.md")})
        log(f"planner '{name}' ({model}) in runs/{wd.name}")
        out = run_agent("planner", wd, model, CFG["effort"]["planner"], schema="plan")
        plan = out["structured_output"] | {"model": model}
        if expected[name]["inputs"] != {dest: digest(src) for dest, src in (common_inputs(include_numerics=True) | {"hint.md": variant_file(f"hints/{hint}.md")}).items()}:
            raise ValueError("planner inputs changed during invocation")
        (ROOT / "plans" / f"{name}.json").write_text(json.dumps(plan, indent=2))
        (ROOT / "plans" / f"{name}.md").write_text(render_plan(name, plan))
        (records / f"{name}.json").write_text(json.dumps(expected[name], indent=2))
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
    if not props or len(ids) != len(props):
        raise ValueError("plan must contain propositions with unique IDs")
    deps = {p["id"]: set(p["depends_on"]) for p in props}
    for pid, ds in deps.items():
        if ds - ids:
            raise ValueError(f"{pid} depends on unknown {ds - ids}")
    seen, done = set(), set()

    def visit(n):
        if n in done:
            return
        if n in seen:
            raise ValueError(f"dependency cycle through {n}")
        seen.add(n)
        for m in deps[n]:
            visit(m)
        done.add(n)
    for n in deps:
        visit(n)


def cmd_select(args):
    plan = json.loads((ROOT / "plans" / f"{args.hint}.json").read_text())
    validate({k: v for k, v in plan.items() if k != "model"}, SCHEMAS["plan"])
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
    mark_report_stale("Proposition state changed; rerun integration after approvals are current.")


def latest_proof(pid):
    proofs = sorted((ROOT / "props" / pid).glob("proof-v*.md"),
                    key=lambda p: int(p.stem.split("-v")[1]))
    return proofs[-1] if proofs else None


def dep_statements(pid):
    meta = json.loads((ROOT / "props" / pid / "meta.json").read_text())
    return {f"deps/{d}.md": ROOT / "props" / d / "statement.md" for d in meta["depends_on"]}


def mark_report_stale(reason):
    if (ROOT / "report" / "integration.json").exists():
        (ROOT / "report" / "STALE").write_text(reason + "\n")


def contract_hash(pid, seen=None):
    """Include all ancestor contracts, so even transitive edits invalidate approval."""
    seen = set() if seen is None else seen
    if pid in seen:
        raise ValueError(f"dependency cycle through {pid}")
    pdir = ROOT / "props" / pid
    meta = json.loads((pdir / "meta.json").read_text())
    deps = {d: contract_hash(d, seen | {pid}) for d in meta["depends_on"]}
    return hash_json({"statement": digest(pdir / "statement.md"), "meta": digest(pdir / "meta.json"),
                      "dependencies": deps, "problem": digest(ROOT / "problem.md"),
                      "papers": digest(ROOT / "papers")})


def approval_hash(pid):
    return hash_json({"contract": contract_hash(pid), "proof": digest(latest_proof(pid)) if latest_proof(pid) else None,
                      "review_policy": {"prompt": build_prompt("referee"), "schema": SCHEMAS["verdict"],
                                        "models": referee_models(), "effort": CFG["effort"]["referee"],
                                        "capabilities": role_capabilities("referee"), "exclusion": EXCL},
                      "reviews": {p.name: digest(p) for p in sorted((ROOT / "props" / pid).glob(
                          f"review-v{status(pid)['round']}-*.json"))}})


def invalidate_stale():
    props = ROOT / "props"
    if not props.exists():
        return
    for p in sorted(props.iterdir()):
        st = status(p.name)
        if st["state"] in ("passed", "defect") and st.get("approval_hash") != approval_hash(p.name):
            set_status(p.name, state="open", approval_hash=None, invalidated="statement, dependency, proof, review or corpus changed")
            log(f"{p.name}: previous approval invalidated; review again")
    # Reports are retained for audit but explicitly marked stale when any source changes.
    manifest = ROOT / "report" / "inputs.json"
    if manifest.exists() and json.loads(manifest.read_text()) != integration_hashes():
        (ROOT / "report" / "STALE").write_text("Inputs changed. Rerun integrate after approvals are current.\n")


def numerical_artifact_hashes():
    accepted = ROOT / "numerics/accepted.json"
    if not accepted.exists():
        return {}
    return {name: digest(ROOT / "numerics" / name)
            for name in json.loads(accepted.read_text()).get("artifacts", {})}


def integration_hashes():
    return {"props": digest(ROOT / "props"), "plan": digest(ROOT / "plan.json"),
            "problem": digest(ROOT / "problem.md"), "numerics": digest(ROOT / "numerics/results.json"),
            "accepted": digest(ROOT / "numerics/accepted.json"),
            "numerical_artifacts": numerical_artifact_hashes()}


def prove_one(pid, override=None):
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
        set_status(pid, state="open", round=rnd)
        contract = contract_hash(pid)
        # ---- prover ----
        files = common_inputs() | dep_statements(pid) | {"statement.md": pdir / "statement.md"}
        if objections_file.exists():
            files |= {"objections.md": objections_file,
                      "previous-proof.md": latest_proof(pid)}
        if (pdir / "hint.md").exists():
            files["hint.md"] = pdir / "hint.md"
        wd = sandbox(f"prove-{pid}-r{rnd}", files)
        log(f"{pid} round {rnd}: prover")
        models = [resolve(override)] if override else model_list("prover")
        model = models[(rnd - 1) % len(models)]
        log(f"{pid} round {rnd}: model {model}")
        run_agent("prover", wd, model, CFG["effort"]["prover"])
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
            v = out["structured_output"] | {"model": model, "contract_hash": contract, "proof_hash": digest(proof)}
            (pdir / f"review-v{rnd}-{i}.json").write_text(json.dumps(v, indent=2))
            return v

        with cf.ThreadPoolExecutor(2) as ex:
            verdicts = list(ex.map(referee, enumerate(referee_models())))
        log(f"{pid} round {rnd}: " + ", ".join(f"{v['model']}={v['verdict']}/{v['severity']}"
                                                for v in verdicts))

        if contract_hash(pid) != contract or digest(proof) != digest(wd / "proof.md"):
            raise ValueError(f"{pid}: inputs changed during proof/review; no approval recorded")
        defect = (wd / "proof.md").read_text().startswith("STATEMENT DEFECT:")
        if any(v["severity"] == "defect-confirmed" for v in verdicts) and not defect:
            raise ValueError("referee confirmed a defect without a STATEMENT DEFECT report")
        if all(v["verdict"] == "pass" for v in verdicts):
            if defect and not all(v["severity"] == "defect-confirmed" for v in verdicts):
                raise ValueError("a statement-defect report cannot be approved as a proof")
            set_status(pid, state="defect" if defect else "passed", round=rnd)
            set_status(pid, approval_hash=approval_hash(pid))
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


def referee_models():
    # Preserve two independent sessions even if fallback collapses model diversity.
    refs = role_models("referees")
    if not isinstance(refs, list) or len(refs) != 2:
        raise ValueError("configure exactly two referee entries")
    return refs


def cmd_prove(args):
    invalidate_stale()
    refs = referee_models()
    if len(set(refs)) < 2:
        log(f"WARNING: both referees use {refs[0]}; configure models.referees for model diversity")
    pids = args.props or sorted(p.name for p in (ROOT / "props").iterdir())
    pids = [p for p in pids if status(p)["state"] != "passed"]
    for pid, res in parallel(lambda pid: prove_one(pid, args.model), pids).items():
        log(f"{pid}: {res}")
    stuck = [p for p in pids if status(p)["state"] in ("stuck", "defect")]
    if stuck:
        log(f"needs you: {stuck}. Read reviews/objections; consider pollinate.")


def cmd_pollinate(args):
    pdir = ROOT / "props" / args.prop
    wd = sandbox(f"pollinate-{args.prop}", {
        "statement.md": pdir / "statement.md",
        "history.md": pdir / "objections.md",
        "plans": ROOT / "plans",
    })
    model = resolve(args.model) if args.model else model_list("pollinator")[status(args.prop)["round"] % len(model_list("pollinator"))]
    out = run_agent("pollinator", wd, model,
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


def cmd_integrate(args):
    invalidate_stale()
    pids = sorted(p.name for p in (ROOT / "props").iterdir())
    open_ = [p for p in pids if status(p)["state"] != "passed"]
    if open_ or not pids:
        raise ValueError(f"not all propositions passed: {open_}")
    selected = json.loads((ROOT / "plan.json").read_text())
    check_acyclic(selected["propositions"])
    if {p["id"] for p in selected["propositions"]} != set(pids):
        raise ValueError("selected plan and proposition directories disagree")
    for p in selected["propositions"]:
        meta = json.loads((ROOT / "props" / p["id"] / "meta.json").read_text())
        if p["depends_on"] != meta["depends_on"]:
            raise ValueError("selected plan and proposition dependency graph disagree")
    before = integration_hashes()
    files = common_inputs(include_numerics=True) | {"plan.json": ROOT / "plan.json"}
    for p in pids:
        files[f"props/{p}/statement.md"] = ROOT / "props" / p / "statement.md"
        files[f"props/{p}/proof.md"] = latest_proof(p)
    rep = ROOT / "report"
    rep.mkdir(exist_ok=True)

    def one(model):
        wd = sandbox(f"integrate-{model_tag(model)}", files)
        out = run_agent("integrator", wd, model, CFG["effort"]["integrator"], schema="integration")
        if not (wd / "assembly.md").is_file():
            raise ValueError("integrator did not write assembly.md")
        value = out["structured_output"]
        tag = model_tag(model)
        (rep / f"integration-{tag}.json").write_text(json.dumps(value, indent=2))
        shutil.copy(wd / "assembly.md", rep / f"assembly-{tag}.md")
        return value

    # A failed or interrupted rerun must not leave an apparently current old report.
    (rep / "STALE").write_text("Integration in progress or incomplete.\n")
    models = [resolve(args.model)] if args.model else model_list("integrator")
    reports = parallel(one, models)
    if before != integration_hashes():
        raise ValueError("inputs changed during integration; report is stale")
    summary = {"composes": all(v["composes"] for v in reports.values()),
               "reviews": reports, "requires_human_comparison": True}
    (rep / "integration.json").write_text(json.dumps(summary, indent=2))
    (rep / "inputs.json").write_text(json.dumps(before, indent=2))
    (rep / "STALE").unlink()
    log(f"all integrators compose: {summary['composes']}; compare independent theorems and constants in report/")


def cmd_archive(args):
    """Copy every sandbox in runs_dir and the run's outputs into the repo under
    archive/<label>/, for review and committing. Run it once no agent is running.
    Host folders do not prevent agents from reading an archive; Docker does.
    PDFs from papers/, literature/ and working folders are omitted."""
    label = args.label or f"{datetime.now():%Y%m%d-%H%M}-{VARIANT}"
    dest = ROOT / "archive" / label
    if dest.exists():
        sys.exit(f"archive/{label} exists; pass another label")
    def skip(directory, names):
        return [name for name in names if name == "papers" or name.lower().endswith(".pdf")]
    n = 0
    for d in sorted(RUNS.iterdir()):
        if d.is_dir():
            shutil.copytree(d, dest / "runs" / d.name, ignore=skip)
            n += 1
    (dest / "runs").mkdir(parents=True, exist_ok=True)
    shutil.copy(RUNS / "_owner.json", dest / "runs" / "_owner.json")
    for name in ("config.json", "plan.json", "numerics", "literature", "plans", "props", "report", "logs"):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, dest / name, ignore=skip)
        elif src.exists():
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest / name)
    log(f"archived {n} sandboxes and the run's outputs to archive/{label}/; "
        "review, then git add it")


def cmd_status(_):
    invalidate_stale()
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
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe").set_defaults(fn=cmd_probe)
    sub.add_parser("check-leaks").set_defaults(fn=cmd_check_leaks)
    sub.add_parser("literature").set_defaults(fn=cmd_literature)
    s = sub.add_parser("numerics"); s.add_argument("--accept", metavar="CANDIDATE"); s.set_defaults(fn=cmd_numerics)
    s = sub.add_parser("plan"); s.add_argument("--cross", action="store_true"); s.add_argument("--single", action="store_true"); s.add_argument("--refresh", action="store_true"); s.set_defaults(fn=cmd_plan)
    s = sub.add_parser("select"); s.add_argument("hint"); s.set_defaults(fn=cmd_select)
    s = sub.add_parser("prove"); s.add_argument("props", nargs="*"); s.add_argument("--model"); s.set_defaults(fn=cmd_prove)
    s = sub.add_parser("pollinate"); s.add_argument("prop"); s.add_argument("--model"); s.set_defaults(fn=cmd_pollinate)
    s = sub.add_parser("integrate"); s.add_argument("--model"); s.set_defaults(fn=cmd_integrate)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    s = sub.add_parser("archive"); s.add_argument("label", nargs="?"); s.set_defaults(fn=cmd_archive)
    args = ap.parse_args()
    try:
        for d in ("logs", "plans", "papers"):
            (ROOT / d).mkdir(exist_ok=True)
        if args.cmd in ("probe", "literature", "plan", "prove", "pollinate", "integrate") or args.cmd == "numerics" and not args.accept:
            if CFG.get("isolation", {}).get("mode", "host") == "host":
                check_agent_venv()
        check_runs_dir()
        args.fn(args)
    except (OSError, RuntimeError, ValueError) as e:
        ap.exit(1, f"error: {e}\n")


if __name__ == "__main__":
    main()
