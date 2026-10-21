"""RED witnesses for the e2-model-routing review findings (merge gate, VENDOR-FAIL evidence, phase tables)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = _ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import provider_registry as pr  # noqa: E402
import subst_gate as sg  # noqa: E402

SONNET = "claude-sonnet-5-5"
SERVED = "claude-sonnet-5.5"
OPUS = "claude-opus-5-5"
COPILOT_CELL = "**Copilot CLI** (Enterprise account, served claude-sonnet-5.5)"


def _block(line: str) -> str:
    return f"MODELS:\n  {line}\n"


# --- 1. merge gate: the Copilot arm checks the served id ---------------------------------------------

def test_copilot_implement_served_opus_without_vendor_fail_is_a_problem():
    assert SERVED in pr.copilot_gateway_served()
    problems, subs = sg.check_models_block(
        _block(f"implement: requested=copilot/default served={OPUS}"))
    assert any("implement" in p and "REFUSED" in p for p in problems), problems
    assert subs == []


def test_copilot_implement_served_sonnet_is_ok():
    problems, subs = sg.check_models_block(
        _block(f"implement: requested=copilot/default served={SERVED}"))
    assert problems == [] and subs == []


def test_copilot_implement_served_opus_with_genuine_vendor_fail_is_listed():
    line = f"implement: requested=copilot/default served={OPUS} VENDOR-FAIL: implement INC-7"
    problems, subs = sg.check_models_block(_block(line))
    assert problems == []
    assert len(subs) == 1 and "VENDOR-FAIL: implement INC-7" in subs[0]


# --- 2. VENDOR-FAIL evidence: whole word `implement` + real text, one shared helper ------------------

@pytest.mark.parametrize("text,expected", [
    ("VENDOR-FAIL: implementation x", False),
    ("VENDOR-FAIL: implement none", False),
    ("VENDOR-FAIL: implement N/A", False),
    ("VENDOR-FAIL: implement na", False),
    ("VENDOR-FAIL: implement -", False),
    ("VENDOR-FAIL: implement TBD", False),
    ("VENDOR-FAIL: implement todo", False),
    ("VENDOR-FAIL: implement", False),
    ("VENDOR-FAIL: implement copilot exit 1: not signed in", True),
])
def test_vendor_fail_evidence_in_a_contract(text, expected):
    assert sg._has_vendor_fail_evidence(text + "\n") is expected


@pytest.mark.parametrize("text,expected", [
    ("VENDOR-FAIL: implementation x", False),
    ("VENDOR-FAIL: implement none", False),
    ("VENDOR-FAIL: implement copilot exit 1: not signed in", True),
])
def test_vendor_fail_evidence_on_a_models_line(text, expected):
    line = f"implement: requested={SONNET}/high served={SONNET} {text}"
    problems, subs = sg.check_models_block(_block(line))
    assert (problems == [] and len(subs) == 1) is expected, (problems, subs)
    if not expected:
        assert any("implement" in p for p in problems)


# --- 6. legacy Substrate table: implement is the `implement` role ------------------------------------

def _substrate_contract(implement_cell: str, extra: str = "") -> str:
    return (
        "# LANE lane-x -- a test contract\n\n"
        "| Model | Mode | Effort |\n|---|---|---|\n"
        f"| {SONNET} | execute | high |\n\n"
        "## Dispatch\n\n```\n"
        f"claude --bg -n lane-x --model {SONNET} --effort high --permission-mode bypassPermissions "
        "--worktree lane-x \"Read and execute the frozen contract\"\n```\n\n"
        "| Phase | Model | Substrate |\n|---|---|---|\n"
        f"| implement code | {implement_cell} | local |\n"
        f"| orchestrate the batch | {SONNET} | local |\n"
        f"\n{extra}\n"
    )


def _problems(text: str) -> list[str]:
    return sg.contract_problems(text, lane="lane-x", batch="E2.0", launch_model=SONNET)[0]


def test_substrate_table_claude_implement_without_evidence_is_refused():
    problems = _problems(_substrate_contract(SONNET))
    assert any("implement" in p and SONNET in p and "REFUSED" in p for p in problems), problems


def test_substrate_table_claude_implement_with_evidence_is_accepted():
    text = _substrate_contract(SONNET, extra="VENDOR-FAIL: implement copilot exit 1: not signed in")
    assert _problems(text) == []


def test_substrate_table_copilot_implement_is_accepted():
    assert _problems(_substrate_contract(COPILOT_CELL)) == []


def test_substrate_table_orchestrate_row_still_judged_against_the_head_role():
    text = _substrate_contract(COPILOT_CELL).replace(f"| orchestrate the batch | {SONNET} |",
                                                     f"| orchestrate the batch | {OPUS} |")
    problems = _problems(text)
    assert any("seat-orchestrator" in p and OPUS in p for p in problems), problems


# --- 7. extra trailing columns; decorated `implement` labels ------------------------------------------

def _where_contract(header: str, row: str) -> str:
    return (
        "# LANE lane-x -- a test contract\n\n"
        "| Model | Mode | Effort |\n|---|---|---|\n"
        f"| {SONNET} | execute | high |\n\n"
        "## Dispatch\n\n```\n"
        f"claude --bg -n lane-x --model {SONNET} --effort high --permission-mode bypassPermissions "
        "--worktree lane-x \"Read and execute the frozen contract\"\n```\n\n"
        f"{header}\n|---|---|---|---|\n{row}\n"
    )


def test_a_phase_table_with_a_trailing_notes_column_is_still_parsed():
    text = _where_contract("| Phase | Model | Where | Notes |", f"| implement | {SONNET} | codespace | n |")
    assert any("implement" in p and "REFUSED" in p for p in _problems(text))
    ok = _where_contract("| Phase | Model | Where | Notes |", f"| implement | {COPILOT_CELL} | codespace | n |")
    assert _problems(ok) == []


@pytest.mark.parametrize("label", ["**implement**", "`implement`", "Implement", "_implement_", "** Implement **"])
def test_a_decorated_implement_label_in_a_where_table_is_judged_as_implement(label):
    bad = _where_contract("| Phase | Model | Where | Notes |", f"| {label} | {SONNET} | codespace | n |")
    assert any("implement" in p and "REFUSED" in p for p in _problems(bad)), label
    good = _where_contract("| Phase | Model | Where | Notes |", f"| {label} | {COPILOT_CELL} | codespace | n |")
    assert _problems(good) == [], label


def test_phase_rows_returns_rows_for_a_four_column_header():
    rows, where = sg._phase_rows(json.dumps("") + "\n| Phase | Model | Where | Notes |\n|---|---|---|---|\n"
                                 "| implement | x | y | z |\n")
    assert rows == [("implement", "x")] and where is True
