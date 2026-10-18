import json
import sys
from pathlib import Path

import pytest
from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.model_matrix import CASES, Stub  # noqa: E402
from run_scenarios import BPMN, ServiceEnv, load  # noqa: E402
from SpiffWorkflow.bpmn import BpmnEvent, BpmnWorkflow  # noqa: E402
from SpiffWorkflow.bpmn.script_engine import PythonScriptEngine  # noqa: E402
from SpiffWorkflow.spiff.specs.event_definitions import MessageEventDefinition  # noqa: E402

DZ = "{https://dev-knowledge.invalid/spike/dz}"


@pytest.mark.parametrize("case,overrides,event,end", CASES, ids=[c[0] for c in CASES])
def test_branch(case, overrides, event, end):
    spec, subs = load()
    wf = BpmnWorkflow(spec, subs, script_engine=PythonScriptEngine(ServiceEnv(Stub(overrides))))
    done = []
    wf.do_engine_steps(did_complete_task=lambda t: done.append(t.task_spec.bpmn_id))
    if event and not wf.is_completed():
        wf.send_event(BpmnEvent(MessageEventDefinition(event)))
        wf.do_engine_steps(did_complete_task=lambda t: done.append(t.task_spec.bpmn_id))
    assert [d for d in done if d and d.startswith("end_")] == [end]


def test_every_node_is_bound_or_a_listed_hole():
    els = [e for e in etree.parse(str(BPMN)).iter() if isinstance(e.tag, str) and e.get("id")
           and etree.QName(e).localname.endswith(("Event", "Gateway", "Task", "subProcess"))]
    holes = {e.get("id") for e in els if e.get(DZ + "bind") is None and e.get("id") not in ("w_start", "w_end")}
    assert holes == {"t_tier", "c_reaped", "c_early", "end_reaped", "end_early"}


def test_zone_and_actor_are_closed_enums():
    root = etree.parse(str(BPMN)).getroot()
    assert {e.get(DZ + "zone") for e in root.iter() if e.get(DZ + "zone")} <= {"BROWSER", "HARNESS", "BOTH"}
    assert {e.get(DZ + "actor") for e in root.iter() if e.get(DZ + "actor")} <= {"code", "seat", "browser", "operator"}
