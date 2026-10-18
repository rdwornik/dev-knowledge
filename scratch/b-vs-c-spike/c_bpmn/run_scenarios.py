"""Run form C (SpiffWorkflow executing p1_dispatch.bpmn) over the scenarios against the REAL verbs (dry-run).

    /tmp/spike/venv-spiffworkflow/bin/python scratch/b-vs-c-spike/c_bpmn/run_scenarios.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from SpiffWorkflow.bpmn import BpmnEvent, BpmnWorkflow  # noqa: E402
from SpiffWorkflow.bpmn.script_engine import PythonScriptEngine, TaskDataEnvironment  # noqa: E402
from SpiffWorkflow.spiff.specs.event_definitions import MessageEventDefinition  # noqa: E402
from SpiffWorkflow.spiff.parser import SpiffBpmnParser  # noqa: E402

from common import report  # noqa: E402
from common.report import SYNTHETIC, base  # noqa: E402
from common.services import SCENARIOS, Services  # noqa: E402

BPMN = HERE / "p1_dispatch.bpmn"
OUT = HERE / "out"
KEEP = ("ok", "exit", "status", "clear", "substrate", "action", "held", "passed", "job_id", "returncode",
        "hole", "unreadable", "steps")


class ServiceEnv(TaskDataEnvironment):
    """SpiffWorkflow calls a service task through the script engine's environment: route it to Services."""

    def __init__(self, svc):
        super().__init__()
        self.svc = svc

    def call_service(self, context, operation_name, operation_params, **kw):
        args = {k: v["value"] for k, v in operation_params.items()}
        return json.dumps(getattr(self.svc, operation_name)(**args))


def load():
    parser = SpiffBpmnParser()
    parser.add_bpmn_file(str(BPMN))
    return parser.get_spec("p1_dispatch"), parser.get_subprocess_specs("p1_dispatch")


def run(name: str) -> dict:
    svc = Services(SCENARIOS[base(name)])
    t0, trace = time.time(), []
    spec, subs = load()
    wf = BpmnWorkflow(spec, subs, script_engine=PythonScriptEngine(ServiceEnv(svc)))

    def did(task):
        bid = task.task_spec.bpmn_id
        if bid and bid in NODES:
            result = {k: v for k, v in (task.data.get(task.task_spec.result_variable, {}) if hasattr(
                task.task_spec, "result_variable") else {}).items() if k in KEEP}
            trace.append({"n": len(trace) + 1, "node": bid, "kind": NODES[bid], "actor": ATTR[bid][0],
                          "zone": ATTR[bid][1], "result": result})

    wf.do_engine_steps(did_complete_task=did)
    if not wf.is_completed():
        wf.send_event(BpmnEvent(MessageEventDefinition(SYNTHETIC.get(name, "lane_handback"))))
        wf.do_engine_steps(did_complete_task=did)
    end = next(t["node"] for t in reversed(trace) if t["node"].startswith("end_"))
    oracle = svc.oracle() if SCENARIOS[base(name)].expect_oracle and name not in SYNTHETIC else None
    out = {"scenario": name, "end": end, "trace": trace, "verbs": svc.calls, "oracle": oracle,
           "seconds": round(time.time() - t0, 1)}
    svc.close()
    return out


def _nodes():
    """bpmn_id -> kind, and (actor, zone): read from the .bpmn file's own attributes (never retyped here)."""
    from lxml import etree
    ns = {"b": "http://www.omg.org/spec/BPMN/20100524/MODEL"}
    dz = "{https://dev-knowledge.invalid/spike/dz}"
    kinds, attrs = {}, {}
    for el in etree.parse(str(BPMN)).iter():
        tag = etree.QName(el).localname
        if "id" in el.attrib and not tag.startswith(("sequenceFlow", "message", "error", "definitions", "process")):
            if tag.endswith(("Event", "Gateway", "Task", "subProcess")) or tag == "subProcess":
                kinds[el.get("id")] = ("event" if tag == "startEvent" else "end" if tag == "endEvent"
                                       else "gateway" if tag.endswith("Gateway") else "task")
                attrs[el.get("id")] = (el.get(dz + "actor", "code"), el.get(dz + "zone", "HARNESS"))
    return kinds, attrs


NODES, ATTR = _nodes()


def main() -> int:
    results = [run(n) for n in [*SCENARIOS, *SYNTHETIC]]
    return 0 if report.write("Form C traces (SpiffWorkflow, BPMN 2.0)", results, OUT) else 1


if __name__ == "__main__":
    raise SystemExit(main())
