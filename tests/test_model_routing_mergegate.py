"""RED witnesses: the merge gate refuses an `implement` MODELS line not served by Copilot
unless the same line carries `VENDOR-FAIL: implement ...`.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import provider_registry as pr  # noqa: E402
import subst_gate as sg  # noqa: E402

_SERVED = "claude-sonnet-5.5"


def _block(line: str) -> str:
    return f"MODELS:\n- {line}\n"


def test_the_gateway_served_id_comes_from_the_registry():
    assert _SERVED in pr.copilot_gateway_served()


def test_copilot_served_implement_is_accepted():
    assert _SERVED in pr.copilot_gateway_served()
    problems, subs = sg.check_models_block(
        _block(f"implement (R177): requested=copilot-cli/default served={_SERVED}"))
    assert problems == [] and subs == []


def test_claude_implement_without_vendor_fail_is_refused():
    problems, _ = sg.check_models_block(
        _block("implement: requested=claude-sonnet-5-5/medium served=claude-sonnet-5-5"))
    assert any("implement" in p and "REFUSED" in p for p in problems), problems


def test_claude_implement_with_vendor_fail_is_accepted_and_listed():
    line = ("implement: requested=claude-sonnet-5-5/medium served=claude-sonnet-5-5 "
            "VENDOR-FAIL: implement copilot auth error")
    problems, subs = sg.check_models_block(_block(line))
    assert problems == []
    assert any("VENDOR-FAIL: implement" in s for s in subs), subs
