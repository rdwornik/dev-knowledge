"""Form C diagram: SpiffWorkflow ships NO renderer, and a hand-written .bpmn has no <bpmndi> layout, so
bpmn.io cannot draw it as-is. This ~60-line BPMN -> DOT pass is the measured cost of 'a rendered diagram'
without hand-drawing: zone -> fill, TODAY-GLUE -> red dashed border, kind -> shape, no dz:bind -> HOLE.

    /tmp/spike/venv-spiffworkflow/bin/python scratch/b-vs-c-spike/c_bpmn/render.py
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from lxml import etree

HERE = Path(__file__).resolve().parent
DZ = "{https://dev-knowledge.invalid/spike/dz}"
ZONE_FILL = {"HARNESS": "#c8e6c9", "BROWSER": "#bbdefb", "BOTH": "#fff59d"}
FLOW = ("startEvent", "endEvent", "serviceTask", "exclusiveGateway", "eventBasedGateway",
        "intermediateCatchEvent", "boundaryEvent")


def node_dot(el, tag) -> str:
    bind = el.get(DZ + "bind")
    short = (bind or "NO CODE").replace("scripts/", "")
    label = f"{el.get('name', el.get('id'))}\\n{short}" + ("  [HOLE]" if bind is None and tag not in
                                                         ("boundaryEvent",) else "")
    glue = el.get(DZ + "glue") == "true"
    shape = {"exclusiveGateway": "diamond", "eventBasedGateway": "diamond", "startEvent": "ellipse",
             "endEvent": "ellipse", "intermediateCatchEvent": "ellipse", "boundaryEvent": "ellipse"}.get(tag, "box")
    zone = el.get(DZ + "zone", "HARNESS")
    peri = 2 if tag in ("endEvent", "intermediateCatchEvent", "boundaryEvent") else 1
    style = "filled" + (",dashed" if glue else "")
    return (f'"{el.get("id")}" [label="{label}", shape={shape}, style="{style}", fillcolor="{ZONE_FILL[zone]}", '
            f'color={"red" if glue else "black"}, penwidth={3 if glue else 1}, peripheries={peri}, '
            f'fontcolor={"red" if bind is None and tag != "boundaryEvent" else "black"}, fontsize=10]')


def build(path: Path) -> str:
    root = etree.parse(str(path)).getroot()
    q = lambda t: "{http://www.omg.org/spec/BPMN/20100524/MODEL}" + t  # noqa: E731
    lines = ["digraph P1 {", "rankdir=TB; fontname=Helvetica; node [fontname=Helvetica]; edge [fontname=Helvetica, fontsize=9];"]
    for sub in root.iter(q("subProcess")):
        lines.append(f'subgraph "cluster_{sub.get("id")}" {{ label="{sub.get("name")}"; style=rounded; color=grey;')
        for el in sub:
            tag = etree.QName(el).localname
            if tag in FLOW and el.get("id") not in ("w_start", "w_end"):
                lines.append(node_dot(el, tag))
        lines.append("}")
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        tag = etree.QName(el).localname
        if tag in FLOW and el.getparent().tag != q("subProcess"):
            lines.append(node_dot(el, tag))
    inner = {"w_start", "w_end"}
    for el in root.iter(q("subProcess")):
        lines.append(f'"{el.get("id")}" [shape=point, width=0.01, label=""];')
    for f in root.iter(q("sequenceFlow")):
        src, dst = f.get("sourceRef"), f.get("targetRef")
        if src in inner:
            src = dst
            continue
        if dst in inner:
            continue
        src_t = "launch_window" if src == "launch_window" else src
        cond = f.find(q("conditionExpression"))
        label = f.get("name", "") + (f"\\n[{cond.text}]".replace(chr(34), "\x27") if cond is not None else "")
        attrs = f'label="{label}"'
        if src_t == "launch_window":
            attrs += ", ltail=cluster_launch_window"
        if dst == "launch_window":
            attrs += ", lhead=cluster_launch_window"
            dst = "t_spawn"
        if src_t == "launch_window":
            src_t = "t_receipt"
        if f.get("sourceRef") in {b.get("id") for b in root.iter(q("boundaryEvent"))}:
            attrs += ", style=dashed"
        lines.append(f'"{src_t}" -> "{dst}" [{attrs}];')
    for b in root.iter(q("boundaryEvent")):   # a boundary event hangs off its subprocess
        lines.append(f'"t_spawn" -> "{b.get("id")}" [style=dotted, arrowhead=none, constraint=false];'
                     if b.get("id") == "b_spawn_failed" else
                     f'"t_identify" -> "{b.get("id")}" [style=dotted, arrowhead=none, constraint=false];')
    lines.append("compound=true; }")
    return "\n".join(lines)


def main() -> None:
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    dot = build(HERE / "p1_dispatch.bpmn")
    (out / "p1_dispatch_c.dot").write_text(dot, encoding="utf-8")
    for fmt in ("svg", "png"):
        (out / f"p1_dispatch_c.{fmt}").write_bytes(subprocess.run(["dot", f"-T{fmt}"], input=dot.encode(),
                                                                  capture_output=True, check=True).stdout)
    print("wrote", sorted(p.name for p in out.glob("p1_dispatch_c.*")))


if __name__ == "__main__":
    main()
