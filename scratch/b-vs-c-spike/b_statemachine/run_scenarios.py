"""Run form B over the scenarios against the REAL verbs (dry-run) and write the traces.

    /tmp/spike/venv-python_statemachine/bin/python scratch/b-vs-c-spike/b_statemachine/run_scenarios.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from common import report  # noqa: E402
from common.report import SYNTHETIC, base  # noqa: E402
from common.services import SCENARIOS, Services  # noqa: E402
from p1_dispatch import P1Dispatch  # noqa: E402

OUT = HERE / "out"

def run(name: str) -> dict:
    svc = Services(SCENARIOS[base(name)])
    t0 = time.time()
    try:
        sm = P1Dispatch(svc)
        sm.send("go")
        if "running" in sm.configuration_values:
            sm.send(SYNTHETIC.get(name, "lane_handback"))
        end = [s for s in sm.configuration][0].id
        oracle = svc.oracle() if SCENARIOS[base(name)].expect_oracle and name not in SYNTHETIC else None
        return {"scenario": name, "end": end, "trace": sm.trace, "verbs": svc.calls, "oracle": oracle,
                "seconds": round(time.time() - t0, 1)}
    finally:
        svc.close()


def main() -> int:
    results = [run(n) for n in [*SCENARIOS, *SYNTHETIC]]
    return 0 if report.write("Form B traces (python-statemachine)", results, OUT) else 1


if __name__ == "__main__":
    raise SystemExit(main())
