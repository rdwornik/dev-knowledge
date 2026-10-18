"""The completeness test, both ways (shared half; each form supplies only its node loader).

  (1) every node binds to ONE file:line that exists, with a test that exists   (a node with neither is a HOLE)
  (2) every dispatch entry point in code (@cli.command in scripts/dispatch.py) maps to a node, by static
      call graph: the entry's function transitively calls the function that holds some node's bind line.
      An unmapped entry point is a LEFTOVER.
"""
from __future__ import annotations

import ast
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DISPATCH = REPO / "scripts" / "dispatch.py"


def check_nodes(nodes: list[dict]) -> dict:
    """nodes: dicts with id, kind, bind ('path:line' or None), test ('path::name' or None)."""
    bound, holes, bad = [], [], []
    for n in nodes:
        if not n["bind"]:
            holes.append(n["id"])
            continue
        path, line = n["bind"].rsplit(":", 1)
        lines = (REPO / path).read_text(encoding="utf-8").splitlines()
        if not (1 <= int(line) <= len(lines) and lines[int(line) - 1].strip()):
            bad.append((n["id"], "bind line missing/blank"))
        tpath, _, tname = (n["test"] or "").partition("::")
        if not n["test"] or f"def {tname}(" not in (REPO / tpath).read_text(encoding="utf-8"):
            bad.append((n["id"], "test missing"))
        bound.append(n["id"])
    return {"nodes": len(nodes), "bound": len(bound), "holes": holes, "bad": bad,
            "gateways": [n["id"] for n in nodes if n["kind"] == "gateway"]}


def entry_points() -> dict[str, set[str]]:
    """entry command function -> every module-level function it transitively calls (plus itself)."""
    tree = ast.parse(DISPATCH.read_text(encoding="utf-8"))
    funcs = {f.name: f for f in tree.body if isinstance(f, ast.FunctionDef)}
    calls = {name: {c.func.id for c in ast.walk(f) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                    and c.func.id in funcs} for name, f in funcs.items()}
    entries = [f.name for f in funcs.values() if any(
        isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr == "command" for d in f.decorator_list)]
    out = {}
    for e in entries:
        seen, todo = {e}, [e]
        while todo:
            for c in calls[todo.pop()]:
                if c not in seen:
                    seen.add(c)
                    todo.append(c)
        out[e] = seen
    return out


def owner(line: int) -> str | None:
    tree = ast.parse(DISPATCH.read_text(encoding="utf-8"))
    for f in tree.body:
        if isinstance(f, ast.FunctionDef) and f.lineno <= line <= f.end_lineno:
            return f.name
    return None


def check_entries(nodes: list[dict]) -> dict:
    held = {owner(int(n["bind"].rsplit(":", 1)[1])) for n in nodes if n["bind"] and n["bind"].startswith("scripts/dispatch.py")}
    eps = entry_points()
    return {"entry_points": sorted(eps), "mapped": sorted(e for e, reach in eps.items() if reach & held),
            "leftovers": sorted(e for e, reach in eps.items() if not reach & held)}


def report(form: str, nodes: list[dict]) -> int:
    a, b = check_nodes(nodes), check_entries(nodes)
    print(f"[{form}] nodes={a['nodes']} bound={a['bound']} gateways={len(a['gateways'])} bad={a['bad']} HOLES={a['holes']}")
    print(f"[{form}] entry points={len(b['entry_points'])} mapped={b['mapped']} LEFTOVERS={b['leftovers']}")
    return 1 if a["bad"] else 0
