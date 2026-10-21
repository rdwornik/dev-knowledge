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


def test_claude_implement_without_vendor_fail_is_refused_naming_the_registry_role():
    problems = _problems(_contract(SONNET))
    joined = "\n".join(problems)
    assert problems, "the implement row names Claude but the registry implement role is Copilot-first"
    assert "implement" in joined and "provider-registry" in joined
    assert SONNET in joined, "the refusal must quote the contract row"


def test_copilot_implement_is_accepted():
    assert _problems(_contract(COPILOT_CELL)) == []


def test_claude_implement_with_a_vendor_fail_line_is_accepted():
    text = _contract(SONNET, extra="VENDOR-FAIL: implement copilot auth error")
    assert [p for p in _problems(text) if "implement" in p and "phase" in p.lower()] == []
    assert _problems(text) == []


def test_lane_head_row_naming_the_seat_orchestrator_passes():
    assert _problems(_contract(COPILOT_CELL, head_row=f"| lane head | {SONNET} | local |")) == []


def test_lane_head_row_naming_opus_is_refused():
    text = _contract(COPILOT_CELL, head_row=f"| lane head | {OPUS} | local |")
    problems = _problems(text)
    assert any(OPUS in p and "REFUSED" in p for p in problems), problems


def test_a_claude_implement_contract_is_refused_before_anything_is_launched(tmp_path):
    contract = tmp_path / "contract.md"
    contract.write_text(_contract(SONNET), encoding="utf-8")
    env = {**__import__("os").environ, "HARNESS_BATCH": "E2.0", "HARNESS_MODEL": SONNET}
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "subst_gate.py"), "contract", "--lane", "x",
         "--contract", str(contract)],
        capture_output=True, text=True, env=env, cwd=str(_ROOT))
    out = proc.stdout + proc.stderr
    assert proc.returncode != 0, out
    assert "implement" in out and "provider-registry" in out, out
