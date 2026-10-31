#!/usr/bin/env python3
"""Stand-in for `claude -p` that exercises the driver's plumbing for free.

Behaviour: provers write a dummy proof; referees fail any proof without a
"Response to objections" section (so every proposition needs two rounds), and
always fail P3 (so it gets stuck and `pollinate` can be tested)."""
import json
import sys
from pathlib import Path

args = sys.argv[1:]
prompt = args[args.index("-p") + 1]
role = prompt.split("\n", 1)[0].removeprefix("ROLE: ").strip()
cwd = Path.cwd()


def emit(structured=None):
    out = {"type": "result", "result": "ok", "total_cost_usd": 0.0}
    if structured is not None:
        out["structured_output"] = structured
    print(json.dumps(out))


if role == "numerics":
    (cwd / "results.json").write_text(json.dumps({"polynomials": {}, "validation": [], "notes": "stub"}))
    (cwd / "compute.py").write_text("# stub\n")
    emit()
elif role == "planner":
    hint = (cwd / "hint.md").read_text()[:20]
    props = [
        {"id": "P1", "title": "Rearrangement", "statement": "S1", "depends_on": []},
        {"id": "P2", "title": "Major arcs", "statement": "S2", "depends_on": ["P1"]},
        {"id": "P3", "title": "Dirichlet series", "statement": "S3", "depends_on": ["P2"], "crux": True},
    ]
    emit({"summary": f"stub plan ({hint})", "main_theorem": "T", "propositions": props})
elif role == "prover":
    stmt = (cwd / "statement.md").read_text()
    text = f"Proof of {stmt.splitlines()[0]}\n"
    if (cwd / "objections.md").exists():
        text += "\n## Response to objections\n"
    (cwd / "proof.md").write_text(text)
    emit()
elif role == "referee":
    proof = (cwd / "proof.md").read_text()
    if "P3" in proof or "Response to objections" not in proof:
        emit({"verdict": "fail", "severity": "gap", "location": "line 1",
              "objection": "stub objection"})
    else:
        emit({"verdict": "pass", "severity": "none"})
elif role == "pollinator":
    (cwd / "hint.md").write_text("stub hint\n")
    emit({"diagnosis": "route", "needs_replan": False, "summary": "try plan B's step 4"})
elif role == "integrator":
    (cwd / "assembly.md").write_text("stub assembly\n")
    emit({"composes": True, "final_theorem": "T"})
else:
    sys.exit(f"unknown role {role!r}")
