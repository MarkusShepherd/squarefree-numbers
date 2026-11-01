#!/usr/bin/env python3
"""Stand-in for `claude -p` that exercises the driver's plumbing for free.

Emits stream-json like the real CLI. Behaviour: provers write a dummy proof;
referees fail any proof without a "Response to objections" section (so every
proposition needs two rounds), and always fail P3 (so it gets stuck and
`pollinate` can be tested). The 'none' planner's transcript contains a search
result from an excluded domain and a denied fetch, so `check-leaks` has
something to find. The librarian lists one open PDF, one paywalled work and
two works the driver must reject."""
import json
import sys
from pathlib import Path

args = sys.argv[1:]
prompt = args[args.index("-p") + 1]
role = prompt.split("\n", 1)[0].removeprefix("ROLE: ").strip()
tools = args[args.index("--tools") + 1].split(",") if "--tools" in args else []
cwd = Path.cwd()


def emit(m):
    print(json.dumps(m))


def tool_call(name, inp, result):
    emit({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "id": "t1", "name": name, "input": inp}]}})
    emit({"type": "user", "message": {"content": [
        {"type": "tool_result", "tool_use_id": "t1", "content": result}]}})


def finish(structured=None):
    out = {"type": "result", "subtype": "success", "result": "ok", "total_cost_usd": 0.0}
    if structured is not None:
        out["structured_output"] = structured
    emit(out)


emit({"type": "system", "subtype": "init", "tools": [t for t in tools if t]})

if role == "probe":
    # planted for check-leaks: recall that shows up only in the reasoning
    emit({"type": "assistant", "message": {"content": [
        {"type": "thinking", "thinking": "I vaguely recall 'Sparse variance for $k$-free numbers'."}]}})
    emit({"type": "result", "subtype": "success", "total_cost_usd": 0.0,
          "result": "I know of no result for V_f itself."})
elif role == "numerics":
    (cwd / "results.json").write_text(json.dumps({"polynomials": {}, "validation": [], "notes": "stub"}))
    (cwd / "compute.py").write_text("# stub\n")
    finish()
elif role == "planner":
    hint = (cwd / "hint.md").read_text()
    if hint.startswith("Strategy hint: follow Vaughan"):   # planted: one post-cutoff id, one not
        tool_call("WebSearch", {"query": "squarefree variance single modulus"},
                  "Fixed modulus: https://arxiv.org/abs/1912.04683")
        tool_call("WebSearch", {"query": "squarefree numbers 2010"},
                  "Before the cutoff: arXiv:1012.5674")
    if hint.startswith("No strategy hint"):
        tool_call("WebSearch", {"query": "sparse variance squarefree polynomial moduli"},
                  "1. Distribution of squarefree numbers ... https://riemannhypothesis.blog/thesis.pdf")
        tool_call("WebFetch", {"url": "https://riemannhypothesis.blog/thesis.pdf"},
                  "Error: WebFetch denied access to domain:riemannhypothesis.blog.")
    props = [
        {"id": "P1", "title": "Rearrangement", "statement": "S1", "depends_on": []},
        {"id": "P2", "title": "Major arcs", "statement": "S2", "depends_on": ["P1"]},
        {"id": "P3", "title": "Dirichlet series", "statement": "S3", "depends_on": ["P2"], "crux": True},
    ]
    finish({"summary": f"stub plan ({hint[:20]})", "main_theorem": "T", "propositions": props})
elif role == "prover":
    stmt = (cwd / "statement.md").read_text()
    text = f"Proof of {stmt.splitlines()[0]}\n"
    if (cwd / "objections.md").exists():
        text += "\n## Response to objections\n"
    (cwd / "proof.md").write_text(text)
    finish()
elif role == "referee":
    proof = (cwd / "proof.md").read_text()
    if "P3" in proof or "Response to objections" not in proof:
        finish({"verdict": "fail", "severity": "gap", "location": "line 1",
                "objection": "stub objection"})
    else:
        finish({"verdict": "pass", "severity": "none"})
elif role == "pollinator":
    (cwd / "hint.md").write_text("stub hint\n")
    finish({"diagnosis": "route", "needs_replan": False, "summary": "try plan B's step 4"})
elif role == "librarian":
    # the open PDF is a file:// URL, which the driver accepts only with LIT_ALLOW_FILE=1
    (cwd / "fake.pdf").write_bytes(b"%PDF-1.4\n% stub\n")
    item = {"kind": "article", "relevance": 2, "why": "stub"}
    finish({"items": [
        item | {"id": "open2005", "authors": "A. Author", "title": "An open paper", "year": 2005,
                "access": "open", "pdf_url": (cwd / "fake.pdf").as_uri()},
        item | {"id": "croft1975", "authors": "M. J. Croft", "title": "Square-free numbers in "
                "arithmetic progressions", "year": 1975, "access": "paywalled"},
        item | {"id": "excluded2015", "authors": "F. Dehnert", "title": "Sparse variance for "
                "k-free numbers in arithmetic progressions", "year": 2015, "access": "paywalled"},
        item | {"id": "blog", "authors": "B. Logger", "title": "A post", "year": 2009,
                "kind": "blog post", "access": "open", "url": "https://primes.recommend.games/x"},
    ], "notes": "stub"})
elif role == "integrator":
    (cwd / "assembly.md").write_text("stub assembly\n")
    finish({"composes": True, "final_theorem": "T"})
else:
    sys.exit(f"unknown role {role!r}")
