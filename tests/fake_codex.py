#!/usr/bin/env python3
"""Stand-in for `codex exec --json` that exercises the driver's plumbing for free.

Same role behaviour as tests/fake_claude.py, in Codex's event format: provers
need two rounds, referees always fail P3, and the 'none' planner's transcript
contains a search and a fetch attempt on an excluded domain. Structured answers
come back as the final message, as orchestrate.py asks Codex agents to do."""
import json
import os
import sys
from pathlib import Path

if '--version' in sys.argv:
    print('sqf-test-cli 1.0')
    sys.exit(0)

from fixture_schema import fill
args = sys.argv[1:]
prompt = args[-1]
role = prompt.split("\n", 1)[0].removeprefix("ROLE: ").strip()
cwd = Path(args[args.index("--cd") + 1])
last = Path(args[args.index("--output-last-message") + 1])
writable = args[args.index("--sandbox") + 1] == "workspace-write"
n = 0
venv = os.environ.get("AGENT_VENV")         # the dry run's stub agent environment
if venv and (os.environ.get("VIRTUAL_ENV") != venv or os.environ.get("ZDOTDIR") != venv
             or os.environ.get("BASH_ENV") != ""
             or not os.environ["PATH"].startswith(os.path.join(venv, "bin"))):
    sys.exit("agent environment not passed to the agent")
if "allow_login_shell=false" not in args:   # a login shell's profile files rewrite PATH
    sys.exit("codex called without -c allow_login_shell=false")


def emit(m):
    print(json.dumps(m))


def item(**it):
    global n
    n += 1
    emit({"type": "item.completed", "item": {"id": f"item_{n}", **it}})


def write(name, text):
    if not writable:
        sys.exit(f"{role}: write to {name} in a read-only sandbox")
    (cwd / name).parent.mkdir(parents=True, exist_ok=True)
    (cwd / name).write_text(text)
    item(type="file_change", changes=[{"path": name, "kind": "add"}], status="completed")


def finish(answer):
    if not isinstance(answer, str) and '--output-schema' in args:
        answer = fill(answer, json.loads(Path(args[args.index('--output-schema') + 1]).read_text()))
    text = answer if isinstance(answer, str) else json.dumps(answer)
    item(type="agent_message", text=text)
    emit({"type": "turn.completed", "usage": {"input_tokens": 1000, "output_tokens": 100}})
    last.write_text(text)


emit({"type": "thread.started", "thread_id": "fake"})
emit({"type": "turn.started"})

if role == "probe":
    finish("I know of no result for V_f itself.")
elif role == "numerics":
    write("results.json", json.dumps({"polynomials": {}, "validation": [], "notes": "stub"}))
    write("compute.py", "# stub\n")
    write("src/helper.py", "# nested source fixture\n")
    write("README.md", "Stub numerics; not real mathematical evidence.\n")
    finish("done")
elif role == "planner":
    hint = (cwd / "hint.md").read_text()
    if hint.startswith("Strategy hint: follow Vaughan"):
        item(type="web_search", query="squarefree variance", result="Fixed modulus: https://arxiv.org/abs/1912.04683")
        item(type="web_search", query="squarefree numbers 2010", result="Before cutoff: arXiv:1012.5674")
    if hint.startswith("No strategy hint"):
        item(type="web_search", query="sparse variance squarefree polynomial moduli")
        item(type="command_execution", command="curl -s https://riemannhypothesis.blog/thesis.pdf",
             aggregated_output="Distribution of squarefree numbers ... riemannhypothesis.blog",
             exit_code=0, status="completed")
        item(type="web_search", query="example.org",
             result={"content": [{"type": "text", "text": "Dehnert, Monatsh. Math."}]},
             status="completed")
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
    write("proof.md", text)
    finish("done")
elif role == "referee":
    proof = (cwd / "proof.md").read_text()
    if "P3" in proof or "Response to objections" not in proof:
        finish({"verdict": "fail", "severity": "gap", "location": "line 1",
                "objection": "stub objection"})
    else:
        finish({"verdict": "pass", "severity": "none"})
elif role == "pollinator":
    write("hint.md", "stub hint\n")
    finish({"diagnosis": "route", "needs_replan": False, "summary": "try plan B's step 4"})
elif role == "librarian":
    # the open PDF is a file:// URL, which the driver accepts only with LIT_ALLOW_FILE=1
    (cwd / "fake.pdf").write_bytes(b"%PDF-1.4\n% stub\n")
    candidate = {"kind": "article", "relevance": 2, "why": "stub"}
    finish({"items": [
        candidate | {"id": "open2005", "authors": "A. Author", "title": "An open paper", "year": 2005,
                "access": "open", "pdf_url": (cwd / "fake.pdf").as_uri()},
        candidate | {"id": "croft1975", "authors": "M. J. Croft", "title": "Square-free numbers in "
                "arithmetic progressions", "year": 1975, "access": "paywalled"},
        candidate | {"id": "excluded2015", "authors": "F. Dehnert", "title": "Sparse variance for "
                "k-free numbers in arithmetic progressions", "year": 2015, "access": "paywalled"},
        candidate | {"id": "blog", "authors": "B. Logger", "title": "A post", "year": 2009,
                "kind": "blog post", "access": "open", "url": "https://gitlab.com/someone/notes"},
    ], "notes": "stub"})
elif role == "integrator":
    write("assembly.md", "stub assembly\n")
    finish({"composes": True, "final_theorem": "T"})
else:
    sys.exit(f"unknown role {role!r}")
