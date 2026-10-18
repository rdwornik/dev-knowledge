import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.model_matrix import CASES, Stub  # noqa: E402
from p1_dispatch import P1Dispatch  # noqa: E402


@pytest.mark.parametrize("case,overrides,event,end", CASES, ids=[c[0] for c in CASES])
def test_branch(case, overrides, event, end):
    sm = P1Dispatch(Stub(overrides))
    sm.send("go")
    if event and "running" in sm.configuration_values:
        sm.send(event)
    assert [s.id for s in sm.configuration] == [end]


def test_every_state_is_bound_or_a_listed_hole():
    holes = {s.id for s in P1Dispatch.states if s.bind is None}
    assert holes == {"tier", "end_reaped", "end_early"}


def test_zone_and_actor_are_closed_enums():
    assert {s.zone for s in P1Dispatch.states} <= {"BROWSER", "HARNESS", "BOTH"}
    assert {s.actor for s in P1Dispatch.states} <= {"code", "seat", "browser", "operator"}
