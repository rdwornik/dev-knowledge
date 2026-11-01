"""RED witnesses: the pre-launch `model_per_role` organ judges the contract's `implement` row
against the registry `implement` role's FIRST entry (Copilot) and the lane head against the
`seat-orchestrator` role, and accepts the `| Phase | Model | Where |` Roles table.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = _ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import subst_gate as sg  # noqa: E402

SONNET = "claude-sonnet-5-5"
OPUS = "claude-opus-5-5"
COPILOT_CELL = "**Copilot CLI** (Enterprise account, served claude-sonnet-5.5)"


def _contract(implement: str, *, head: str = SONNET, extra: str = "", head_row: str | None = None,
              lane: str = "lane-x") -> str:
    head_row = head_row if head_row is not None else f"| lane head | {head} | local |"
    return (
        f"# LANE {lane} -- a test contract\n\n"
        "| Model | Mode | Effort |\n|---|---|---|\n"
        f"| {head} | execute | high |\n\n"
        "## Dispatch\n\n```\n"
        f"claude --bg -n {lane} --model {head} --effort high --permission-mode bypassPermissions "
        f"--worktree {lane} \"Read and execute the frozen contract\"\n```\n\n"
        "## Roles\n\n"
        "| Phase | Model | Where |\n|---|---|---|\n"
        f"| implement | {implement} | codespace |\n"
        f"{head_row}\n"
        "| coffee notes | free prose, not judged | anywhere |\n"
        f"\n{extra}\n"
    )


def _problems(text: str, *, launch_model: str = SONNET) -> list[str]:
    problems, _notes = sg.contract_problems(text, lane="lane-x", batch="E2.0", launch_model=launch_model)
    return problems


def test_admitted_claude_implement_is_accepted_without_vendor_fail():
    problems = _problems(_contract(SONNET))
    # GO-E3.0 R11: admitted Sonnet is the first implement entry and needs no VENDOR-FAIL.
    assert problems == []


def test_copilot_implement_requires_vendor_fail_after_sonnet():
    problems = _problems(_contract(COPILOT_CELL))
    # GO-E3.0 R11: Copilot is a later implement entry and requires VENDOR-FAIL evidence.
    assert any("implement" in p and "VENDOR-FAIL" in p for p in problems), problems


# GO-E3.0 R11: Sonnet leads implement; Copilot is the VENDOR-FAIL fallback.
FROZEN_CELL = (
    "claude-sonnet-5-5 (R11: Sonnet writes the code; fallback Copilot CLI only after a recorded "
    "`VENDOR-FAIL: implement copilot <error verbatim>`)"
)


def test_sonnet_primary_cell_naming_the_copilot_fallback_is_accepted():
    # GO-E3.0 R11: the cell names admitted Sonnet first and Copilot as its fallback.
    assert _problems(_contract(FROZEN_CELL)) == []


def test_copilot_led_cell_mentioning_the_sonnet_fallback_is_refused():
    # GO-E3.0 R11: the later implement entry (Copilot) leading a cell needs a genuine VENDOR-FAIL line, even when the cell names the first entry as a fallback; mirrors the base test that refused a cell led by the later entry.
    assert _problems(_contract(f"copilot (fallback {SONNET})"))


def test_claude_via_copilot_cell_is_refused():
    assert _problems(_contract("Claude via Copilot"))


def test_claude_implement_with_a_vendor_fail_line_is_accepted():
    text = _contract(SONNET, extra="VENDOR-FAIL: implement copilot auth error")
    assert [p for p in _problems(text) if "implement" in p and "phase" in p.lower()] == []
    assert _problems(text) == []


def test_lane_head_row_naming_the_seat_orchestrator_passes():
    # GO-E3.0 R11: use first-entry Sonnet while checking the lane-head role independently.
    assert _problems(_contract(SONNET, head_row=f"| lane head | {SONNET} | local |")) == []


def test_lane_head_row_naming_opus_is_refused():
    text = _contract(COPILOT_CELL, head_row=f"| lane head | {OPUS} | local |")
    problems = _problems(text)
    assert any(OPUS in p and "REFUSED" in p for p in problems), problems


def test_admitted_claude_implement_contract_passes_before_launch(tmp_path):
    contract = tmp_path / "contract.md"
    contract.write_text(_contract(SONNET), encoding="utf-8")
    env = {**__import__("os").environ, "HARNESS_BATCH": "E2.0", "HARNESS_MODEL": SONNET}
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "subst_gate.py"), "contract", "--lane", "x",
         "--contract", str(contract)],
        capture_output=True, text=True, env=env, cwd=str(_ROOT))
    out = proc.stdout + proc.stderr
    # GO-E3.0 R11: the admitted first implementer passes the pre-launch gate.
    assert proc.returncode == 0, out
    # GO-E3.0 R11: accepting Sonnet must not be reported as a refusal.
    assert "REFUSED" not in out, out


def test_where_table_alone_does_not_make_an_out_of_batch_contract_applicable():
    text = _contract(COPILOT_CELL, head="opus", head_row="| lane head | opus | local |")
    problems, notes = sg.contract_problems(text, lane="lane-x", batch="", launch_model="opus")
    assert problems == []
    assert any("not applicable" in n for n in notes), notes


def test_where_table_with_opus_head_is_refused_in_batch_e2_0():
    text = _contract(COPILOT_CELL, head="opus", head_row="| lane head | opus | local |")
    problems, _notes = sg.contract_problems(text, lane="lane-x", batch="E2.0", launch_model="opus")
    assert any("REFUSED" in p and "opus" in p for p in problems), problems


PROSE = "only after a recorded `VENDOR-FAIL: implement copilot <error verbatim>`, announced"


def test_vendor_fail_prose_mention_in_paragraph_and_table_cell_does_not_exempt():
    # GO-E3.0 R11: the later Copilot entry still needs actual VENDOR-FAIL evidence.
    extra = f"Claude implements {PROSE} in the chat.\n\n| note | {PROSE} |\n|---|---|\n"
    assert _problems(_contract(COPILOT_CELL, extra=extra)), "prose mention must not count as evidence"


def test_flush_start_vendor_fail_evidence_line_is_accepted():
    text = _contract(SONNET, extra="VENDOR-FAIL: implement copilot exit 1: not signed in")
    assert _problems(text) == []


def test_bulleted_vendor_fail_evidence_line_is_accepted():
    text = _contract(SONNET, extra="- VENDOR-FAIL: implement copilot exit 1: not signed in")
    assert _problems(text) == []
