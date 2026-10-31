"""RED-first acceptance tests for the GO-E3.0 bootstrap contract."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import dispatch as d  # noqa: E402
import provider_registry as pr  # noqa: E402
import subst_gate as sg  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
SONNET = "claude-sonnet-5-5"
DISALLOWED_TOOLS = "--disallowedTools=AskUserQuestion,advisor"


# --- R11 role order -----------------------------------------------------------------------------

def test_implement_role_prefers_sonnet_then_admitted_copilot():
    order = pr.role_order("implement")
    assert order[0]["provider"] == "anthropic"
    assert order[0]["model"] == SONNET
    assert not order[0].get("vendor_fail_only")
    assert order[1]["provider"] == "copilot-enterprise"
    assert order[1]["model"] == "claude-sonnet-5.5"
    assert order[1]["admission"]["verdict"] == "admitted"


def test_judge_role_starts_with_gpt_6_sol():
    order = pr.role_order("judge")
    assert order[0]["provider"] == "openai"
    assert order[0]["model"] == "gpt-6-sol"


def test_review_role_starts_with_terra_then_grok():
    order = pr.role_order("review")
    assert order[0]["model"] == "gpt-5.6-terra"
    assert order[1]["model"] == "grok-4.7"


def test_read_role_starts_with_admitted_antigravity_then_haiku():
    order = pr.role_order("read")
    assert order[0]["provider"] == "antigravity"
    assert order[0]["admission"]["verdict"] == "admitted"
    assert order[1]["model"] == "claude-haiku-5-5"


@pytest.mark.parametrize("role", ["red", "qa"])
def test_red_and_qa_roles_start_with_copilot_gpt_6_luna(role):
    order = pr.role_order(role)
    assert order[0]["provider"] == "copilot-enterprise"
    assert order[0].get("model") == "gpt-6-luna"


# --- E3.0 contract ------------------------------------------------------------------------------

def _e30_contract():
    return f"""# LANE e30-fixture -- a test contract

| Model | Mode | Effort |
|---|---|---|
| {SONNET} | execute | high |

## Dispatch

```
claude --bg -n e30-fixture --model {SONNET} --effort high --permission-mode bypassPermissions
```

| Phase | Model | Where |
|---|---|---|
| lane head | {SONNET} | local |
| implement | {SONNET} | local |
"""


def test_inline_e30_sonnet_implement_contract_is_accepted():
    problems, _notes = sg.contract_problems(
        _e30_contract(), lane="e30-fixture", batch="E3.0", launch_model=SONNET
    )
    assert problems == []


def test_committed_e30_sonnet_implement_contract_fixture_is_accepted():
    fixture = REPO / "tests" / "fixtures" / "e30-sonnet-implement-contract.md"
    assert fixture.is_file()
    text = fixture.read_text(encoding="utf-8")
    problems, _notes = sg.contract_problems(
        text, lane="e30-fixture", batch="E3.0", launch_model=SONNET
    )
    assert problems == []


# --- MODELS handback ----------------------------------------------------------------------------

def test_matching_sonnet_implement_models_line_is_accepted():
    text = f"MODELS:\n  implement: requested={SONNET} served={SONNET}\n"
    problems, _subs = sg.check_models_block(text)
    assert problems == []


def test_matching_copilot_sonnet_implement_models_line_is_accepted():
    text = ("MODELS:\n"
            "  implement: requested=copilot/claude-sonnet-5.5 served=claude-sonnet-5.5\n")
    problems, _subs = sg.check_models_block(text)
    assert problems == []


def test_grok_implement_substitution_without_vendor_fail_is_refused():
    text = "MODELS:\n  implement: requested=grok-4.7 served=grok-4.7\n"
    problems, _subs = sg.check_models_block(text)
    assert problems


def test_different_served_model_without_vendor_fail_is_refused():
    text = f"MODELS:\n  implement: requested={SONNET} served=claude-haiku-5-5\n"
    problems, _subs = sg.check_models_block(text)
    assert problems


def test_different_served_model_with_vendor_fail_is_accepted():
    text = (f"MODELS:\n  implement: requested={SONNET} served=claude-haiku-5-5 "
            "VENDOR-FAIL: implement quota exhausted today\n")
    problems, _subs = sg.check_models_block(text)
    assert problems == []


# --- Claude argv restrictions -------------------------------------------------------------------

@pytest.mark.parametrize("argv", [
    d.schema_smoke_argv(["claude", "--json-schema", "{}", "--model", SONNET]),
    d.build_plan("anthropic", SONNET, "s", "medium", "p", streamed=True).argv,
    d.build_plan("anthropic", SONNET, "s", "medium", "p").argv,
    d.build_repair_plan(SONNET, "s", 1, "medium", "p").argv,
    d.build_successor_plan(SONNET, "s", "medium", "p").argv,
], ids=["schema-smoke", "headless", "background", "repair", "successor"])
def test_every_claude_dispatch_argv_has_the_disallowed_tools_token(argv):
    assert argv is not None
    assert argv.count(DISALLOWED_TOOLS) == 1


def test_background_claude_argv_has_no_old_partial_disallowed_tools_token():
    argv = d.build_plan("anthropic", SONNET, "s", "medium", "p").argv
    assert "--disallowedTools=AskUserQuestion" not in argv


# --- E3.0 task-file contract ---------------------------------------------------------------------

_TASKS = {
    1747: (
        "`ci_verdict.py` reads the retired suite-gate block on its no-baseline path and reports registry members as new reds",
        "RED first: a test built from c6618dbb7's case (6 known-reds members) asserts 0 new reds; real-use witness: `ci_verdict.py --ref c6618dbb7` prints an empty new-red list.",
    ),
    1748: (
        "the view: /decide first, then build",
        "(1) an ADR at status Proposed from /decide over DIGEST-E3-0-PROPOSALS-EVALUATION-2026-10-31.md section C with every decide_checks.py check passing; (2) after the operator ratifies it, the view is built (expected: scripts/system_map.py extended into the generated AS-IS view, JSON + static HTML, live on localhost, snapshot for the artifact) and wired at batch close.",
    ),
    1749: (
        "the backlog per-row reconciliation organ (GO-E3.0 R10), after L2",
        "RED first: `apply` refuses without an operator ruling and applies only the ruled classes; real-use witness: one `report` run over the open rows lands as an audit with its cost record.",
    ),
}


@pytest.mark.parametrize(("number", "title", "done_when"), [
    (number, title, done_when)
    for number, (title, done_when) in _TASKS.items()
], ids=["1747", "1748", "1749"])
def test_e30_task_file_has_required_open_p2_metadata_and_done_when(number, title, done_when):
    matches = list((REPO / "tasks").glob(f"{number}-*.md"))
    assert len(matches) == 1
    text = matches[0].read_text(encoding="utf-8")
    assert title in text
    assert "status: open" in text
    assert "priority: P2" in text
    assert done_when in text
