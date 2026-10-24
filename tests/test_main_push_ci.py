"""RED-first contract tests for one push-time verdict on main."""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
ALLOWED_SKIPS = (
    "${{ (startsWith(github.event_name, 'PUSH') && "
    "startsWith(github.ref, 'refs/heads/worktree-') && "
    "!startsWith(github.ref, 'refs/heads/worktree-integrate-')) && "
    "'pytest, windows-nightly-triage' || 'tier1, windows-nightly-triage' }}"
)


def load(name: str) -> dict:
    doc = yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))
    if True in doc and "on" not in doc:
        doc["on"] = doc.pop(True)
    return doc


def triggers(doc: dict) -> dict:
    on = doc.get("on")
    if on is None:
        return {}
    if isinstance(on, str):
        return {on: None}
    if isinstance(on, list):
        return {item: None for item in on}
    return on


def expression(value) -> str:
    text = str(value or "").strip()
    if text.startswith("${{") and text.endswith("}}"):
        text = text[3:-2].strip()
    return text


def _matches(patterns, branch: str) -> bool:
    return any(fnmatch.fnmatchcase(branch, pattern.replace("**", "*")) for pattern in patterns)


def _push_workflows(branch: str) -> dict[str, list[str]]:
    runs = {"unconditional": [], "path_filtered": []}
    for path in sorted(WORKFLOWS.glob("*.yml")):
        push = triggers(load(path.name)).get("push")
        if push is None:
            continue
        push = push or {}
        if "branches" in push and not _matches(push["branches"], branch):
            continue
        if "branches-ignore" in push and _matches(push["branches-ignore"], branch):
            continue
        kind = "path_filtered" if "paths" in push or "paths-ignore" in push else "unconditional"
        runs[kind].append(path.name)
    return runs


def _reuse_step(doc: dict) -> dict:
    steps = doc["jobs"]["plan"]["steps"]
    found = [step for step in steps if step.get("id") == "reuse"]
    assert len(found) == 1
    return found[0]


def _jq_filter(script: str) -> str:
    match = re.search(r"--jq\s+'([^']*)'", script, flags=re.DOTALL)
    if not match:
        match = re.search(r'--jq\s+"([^"]*)"', script, flags=re.DOTALL)
    assert match, "the reuse lookup must use gh run list --jq"
    return match.group(1)


def test_main_push_starts_only_the_conductor_verdict():
    conductor = triggers(load("conductor.yml"))["push"]
    assert {"main", "worktree-**", "epic/**"} <= set(conductor["branches"])
    assert _push_workflows("main") == {
        "unconditional": ["conductor.yml"],
        "path_filtered": ["substrate-heartbeat.yml"],
    }
    wall_triggers = triggers(load("report-only-wall.yml"))
    assert "push" not in wall_triggers or "main" not in str(wall_triggers["push"])


def test_plan_reuses_only_a_prior_green_run_for_the_same_sha():
    doc = load("conductor.yml")
    plan = doc["jobs"]["plan"]
    permissions = plan["permissions"]
    assert permissions.get("actions") == "read"
    assert permissions.get("contents") == "read"

    step = _reuse_step(doc)
    condition = expression(step.get("if"))
    assert "github.event_name == 'push'" in condition
    assert "github.ref == 'refs/heads/main'" in condition
    script = step["run"]
    assert "gh run list" in script
    assert "--workflow conductor.yml" in script
    assert "--commit" in script and "${{ github.sha }}" in script
    assert "--jq" in script
    jq = _jq_filter(script)
    assert re.search(r"\.status\s*==\s*['\"]completed['\"]", jq)
    assert re.search(r"\.conclusion\s*==\s*['\"]success['\"]", jq)
    assert "github.run_id" in script or "github.run_id" in jq
    assert re.search(r"\.databaseId\s*!=\s*[^ ]+", jq)
    assert re.search(r"headBranch\s*!=\s*['\"]main['\"]", jq)
    assert "reuse=true" in script and "reuse=false" in script
    assert "$GITHUB_OUTPUT" in script

    outputs = plan["outputs"]
    assert expression(outputs["reuse"]) == "steps.reuse.outputs.reuse"


def test_pytest_steps_keep_the_context_but_skip_work_on_reuse():
    job = load("conductor.yml")["jobs"]["pytest"]
    assert "if" not in job
    reuse_steps = [
        step for step in job["steps"] if "reuse" in str(step.get("name", "")).lower()
    ]
    assert len(reuse_steps) == 1
    info = reuse_steps[0]
    assert expression(info.get("if")).replace(" ", "") == (
        "needs.plan.outputs.reuse=='true'"
    )

    for step in job["steps"]:
        if step is info:
            continue
        condition = expression(step.get("if"))
        assert "needs.plan.outputs.reuse" in condition
        assert re.search(
            r"needs\.plan\.outputs\.reuse\s*!=\s*['\"]true['\"]", condition
        ), f"step {step.get('name', step.get('uses'))!r} must be disabled on reuse"


def test_gate_allowed_skips_expression_is_unchanged():
    step = load("conductor.yml")["jobs"]["gate"]["steps"][0]
    assert step["with"]["allowed-skips"] == ALLOWED_SKIPS


def test_windows_gate_does_not_repeat_a_reused_windows_verdict():
    job = load("conductor.yml")["jobs"]["windows-gate"]
    assert expression(job["env"]["PLAN_REUSE"]) == "needs.plan.outputs.reuse"
    step = next(
        step
        for step in job["steps"]
        if step.get("name") == "Does the plan require the Windows leg?"
    )
    script = step["run"]
    assert re.search(r'PLAN_REUSE.*["\']true["\']', script)
    assert re.search(r'windows=no', script)
