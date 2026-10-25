"""RED-first witnesses: `subst_gate` judges an `orchestrator-<batch>-cycle-<n>` lane against
`seat-dispatcher` (Opus) and every other lane head against `seat-orchestrator` (Sonnet)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import subst_gate as sg  # noqa: E402

SONNET = "claude-sonnet-5-5"
OPUS = "claude-opus-5-5"
ORCH = "orchestrator-e2-1-cycle-4"


def _contract(*, head, dispatch, lane, rows=""):
    text = (
        f"# LANE {lane} -- a test contract\n\n"
        "| Model | Mode | Effort |\n|---|---|---|\n"
        f"| {head} | execute | high |\n\n"
        "## Dispatch\n\n```\n"
        f"claude --bg -n {lane} --model {dispatch} --effort high --permission-mode bypassPermissions "
        f"--worktree {lane} \"Read and execute the frozen contract\"\n```\n\n"
    )
    if rows:
        text += "| Phase | Model | Where |\n|---|---|---|\n" + rows + "\n"
    return text


def _problems(model, lane, launch_model="", rows=""):
    text = _contract(head=model, dispatch=model, lane=lane, rows=rows)
    return sg.contract_problems(text, lane=lane, batch="E2.1", launch_model=launch_model)[0]


def test_an_orchestrator_lane_on_opus_is_accepted():
    assert _problems(OPUS, ORCH, launch_model=OPUS) == []


def test_an_orchestrator_lane_on_sonnet_is_refused_naming_the_dispatcher_model():
    problems = _problems(SONNET, ORCH, launch_model=SONNET)
    assert problems
    assert all(OPUS in p and "seat-dispatcher" in p for p in problems)


def test_an_ordinary_lane_on_opus_is_still_refused_against_seat_orchestrator():
    problems = _problems(OPUS, "lane-x", launch_model=OPUS)
    assert problems and all("seat-orchestrator" in p and SONNET in p for p in problems)


def test_an_ordinary_lane_on_sonnet_is_accepted():
    assert _problems(SONNET, "lane-x", launch_model=SONNET) == []


@pytest.mark.parametrize("lane", [
    "orchestrator-e2-1-cycle-", "orchestrator-e2-1-cycle-4x", "xorchestrator-e2-1-cycle-4",
    "orchestrator-e2-1-cycle-4 ", "orchestrator-e2-1-cycle-4\n", "Orchestrator-e2-1-cycle-4",
])
def test_near_miss_names_are_ordinary_lanes(lane):
    assert sg.head_role_for_lane(lane) == sg.HEAD_ROLE
    assert _problems(OPUS, lane, launch_model=OPUS)
    assert _problems(SONNET, lane, launch_model=SONNET) == []


@pytest.mark.parametrize("lane", ["orchestrator-e2-1-cycle-4", "orchestrator-e10-12-cycle-103"])
def test_the_grammar_selects_seat_dispatcher(lane):
    assert sg.head_role_for_lane(lane) == "seat-dispatcher"


def test_the_lane_head_where_row_follows_the_chosen_role():
    row = f"| lane head | {OPUS} | local |"
    assert _problems(OPUS, ORCH, launch_model=OPUS, rows=row) == []
    assert _problems(OPUS, "lane-x", launch_model=OPUS, rows=row)
    sonnet_row = f"| lane head | {SONNET} | local |"
    assert _problems(OPUS, ORCH, launch_model=OPUS, rows=sonnet_row)


def _substrate_problems(rows, lane, head):
    """The Substrate table is the FIRST (and only) table, so `_phase_rows` judges its rows."""
    text = _contract(head=head, dispatch=head, lane=lane)
    text += "| Phase | Model | Substrate |" + chr(10) + "|---|---|---|" + chr(10) + rows + chr(10)
    return sg.contract_problems(text, lane=lane, batch="E2.1", launch_model=head)[0]


@pytest.mark.parametrize("phase", ["orchestrate the batch", "lane head"])
def test_a_substrate_head_row_follows_the_chosen_role(phase):
    opus_row = f"| {phase} | {OPUS} | local |"
    sonnet_row = f"| {phase} | {SONNET} | local |"
    assert _substrate_problems(opus_row, ORCH, OPUS) == []
    assert _substrate_problems(sonnet_row, ORCH, OPUS)
    assert _substrate_problems(sonnet_row, "lane-x", SONNET) == []
    assert _substrate_problems(opus_row, "lane-x", SONNET)


def test_a_lane_head_substrate_row_is_not_an_unmapped_phase():
    problems = _substrate_problems(f"| lane head | {OPUS} | local |", ORCH, OPUS)
    assert not any("maps to no registry role" in p for p in problems)
