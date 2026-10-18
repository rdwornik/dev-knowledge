"""Form B's completeness loader: the nodes ARE the class attributes (no parsing)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.completeness import report  # noqa: E402
from p1_dispatch import P1Dispatch  # noqa: E402

nodes = [{"id": s.id, "kind": s.kind, "bind": s.bind, "test": s.test} for s in P1Dispatch.states]
raise SystemExit(report("B", nodes))
