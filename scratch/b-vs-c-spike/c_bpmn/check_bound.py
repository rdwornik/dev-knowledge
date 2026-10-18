"""Form C's completeness loader: parse the .bpmn and read the dz: attributes."""
import sys
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.completeness import report  # noqa: E402

DZ = "{https://dev-knowledge.invalid/spike/dz}"
nodes = [{"id": e.get("id"), "kind": ("gateway" if etree.QName(e).localname.endswith("Gateway") else "other"),
          "bind": e.get(DZ + "bind"), "test": e.get(DZ + "test")}
         for e in etree.parse(str(Path(__file__).parent / "p1_dispatch.bpmn")).iter()
         if isinstance(e.tag, str) and etree.QName(e).localname.endswith(("Event", "Gateway", "Task", "subProcess"))
         and e.get("id") not in ("w_start", "w_end", "start") or (isinstance(e.tag, str) and e.get("id") == "start")]
raise SystemExit(report("C", nodes))
