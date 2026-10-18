"""Form B diagram: python-statemachine's own DOT export, then a post-pass that colours by NODE ATTRIBUTES.

No node is drawn by hand: zone -> fill, TODAY-GLUE -> red dashed border, kind -> shape,
bind=None -> "NO CODE" in the label. Needs `pydot` (python-statemachine[diagrams]) and the `dot` binary.

    /tmp/spike/venv-python_statemachine/bin/python scratch/b-vs-c-spike/b_statemachine/export_diagram.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from p1_dispatch import P1Dispatch  # noqa: E402
from statemachine.contrib.diagram import DotGraphMachine, MermaidGraphMachine, run_graphviz  # noqa: E402

ZONE_FILL = {"HARNESS": "#c8e6c9", "BROWSER": "#bbdefb", "BOTH": "#fff59d"}


class _Null:                       # constructing the machine enters `start`; give it a service that does nothing
    def __getattr__(self, name):
        return lambda *a, **k: {}


def _walk(graph):
    for node in graph.get_nodes():
        yield node
    for sub in graph.get_subgraphs():
        yield from _walk(sub)


def build() -> str:
    sm = P1Dispatch(_Null())
    DotGraphMachine.graph_rankdir = "TB"
    graph = DotGraphMachine(sm).get_graph()
    meta = {s.id: s for s in sm.states}
    for node in _walk(graph):
        state = meta.get(node.get_name().strip('"'))
        if state is None:
            continue
        short = (state.bind or "NO CODE").replace("scripts/", "").replace("dispatch.py", "dispatch.py")
        label = f"{state.label}\\n{short}" + ("  [HOLE]" if state.bind is None else "")
        style = "filled" + (",dashed" if state.glue else "")
        node.set("label", f'"{label}"')
        node.set("fillcolor", ZONE_FILL[state.zone])
        node.set("color", "red" if state.glue else "black")
        node.set("penwidth", "3" if state.glue else "1")
        node.set("style", f'"{style}"')
        node.set("shape", {"gateway": "diamond", "end": "ellipse", "event": "ellipse"}.get(state.kind, "box"))
        node.set("peripheries", "2" if state.kind == "end" else "1")
        node.set("fontcolor", "red" if state.bind is None else "black")
    return graph.to_string()


def main() -> None:
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    dot = build()
    (out / "p1_dispatch_b.dot").write_text(dot, encoding="utf-8")
    for fmt in ("svg", "png"):
        (out / f"p1_dispatch_b.{fmt}").write_bytes(run_graphviz(dot, fmt))
    (out / "p1_dispatch_b.mmd").write_text(MermaidGraphMachine(P1Dispatch(_Null()))(), encoding="utf-8")
    print("wrote", sorted(p.name for p in out.glob("p1_dispatch_b.*")))


if __name__ == "__main__":
    main()
