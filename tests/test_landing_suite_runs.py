"""Landing suite-run model and the existing M2 metric contract."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "conductor.yml"
SINCE = "2026-01-01T00:00:00Z"
UNTIL = "2026-01-10T00:00:00Z"
BASH = shutil.which("bash")


def load_workflow() -> dict:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    if True in doc and "on" not in doc:
        doc["on"] = doc.pop(True)
    return doc


def expression(value) -> str:
    text = str(value or "").strip()
    if text.startswith("${{") and text.endswith("}}"):
        text = text[3:-2].strip()
    return text


def reuse_parts(doc: dict) -> tuple[dict, list[dict], dict]:
    jobs = doc["jobs"]
    reuse_steps = [
        step for step in jobs["plan"]["steps"] if step.get("id") == "reuse"
    ]
    assert len(reuse_steps) == 1
    pytest_job = jobs["pytest"]
    named_reuse = [
        step
        for step in pytest_job["steps"]
        if "reuse" in str(step.get("name", "")).lower()
    ]
    assert len(named_reuse) == 1
    return reuse_steps[0], pytest_job["steps"], named_reuse[0]


def _main_reuse_is_wired(doc: dict) -> bool:
    reuse, steps, info = reuse_parts(doc)
    reuse_if = expression(reuse.get("if"))
    if "github.event_name == 'push'" not in reuse_if:
        return False
    if "github.ref == 'refs/heads/main'" not in reuse_if:
        return False
    if expression(info.get("if")).replace(" ", "") != (
        "needs.plan.outputs.reuse=='true'"
    ):
        return False
    guarded = [step for step in steps if step is not info]
    return bool(guarded) and all(
        "needs.plan.outputs.reuse" in expression(step.get("if"))
        and re.search(
            r"needs\.plan\.outputs\.reuse\s*!=\s*['\"]true['\"]",
            expression(step.get("if")),
        )
        for step in guarded
    )


def _jq_filter(script: str) -> str:
    match = re.search(r"--jq\s+'([^']*)'", script, flags=re.DOTALL)
    if not match:
        match = re.search(r'--jq\s+"([^"]*)"', script, flags=re.DOTALL)
    assert match, "the reuse lookup must use its --jq filter"
    return match.group(1)


def _filtered_gh_output(jq: str, result: str) -> str:
    """Return the jq-shaped output for a canned filtered candidate set."""
    has_candidate = result == "green"
    if re.search(r"\|\s*length\b", jq):
        return "1" if has_candidate else "0"
    if re.search(r"\bany\s*\(", jq):
        return "true" if has_candidate else "false"
    if re.search(r"\|\s*\.?(databaseId|headBranch|headSha)\b", jq):
        return "12345" if has_candidate else ""
    return json.dumps(
        {
            "databaseId": 12345,
            "headBranch": "worktree-integrate-x",
            "headSha": "landing-sha",
            "status": "completed",
            "conclusion": "success",
        }
    ) if has_candidate else ""


@pytest.mark.skipif(BASH is None, reason="bash is required to execute the workflow script")
@pytest.mark.parametrize(
    ("candidate", "expected"),
    [("green", "true"), ("none", "false"), ("red", "false")],
)
def test_reuse_script_emits_the_result_of_its_green_run_filter(
    tmp_path, candidate, expected
):
    assert _run_reuse_script(load_workflow(), tmp_path, candidate) == expected


def _run_reuse_script(doc: dict, tmp_path, candidate: str) -> str:
    reuse, _, _ = reuse_parts(doc)
    script = reuse["run"]
    jq = _jq_filter(script)
    assert re.search(r"\.conclusion\s*==\s*['\"]success['\"]", jq)
    assert re.search(r"\.status\s*==\s*['\"]completed['\"]", jq)
    assert "github.run_id" in script or "github.run_id" in jq
    assert re.search(r"\.databaseId\s*!=\s*[^ ]+", jq)
    assert re.search(r"headBranch\s*!=\s*['\"]main['\"]", jq)

    fake_bin = tmp_path / candidate / "bin"
    fake_bin.mkdir(parents=True)
    fake_gh = fake_bin / "gh"
    fake_gh.write_text(
        "#!/bin/sh\nprintf '%s\\n' \"$FAKE_GH_FILTERED_OUTPUT\"\n",
        encoding="utf-8",
    )
    fake_gh.chmod(0o755)
    output = tmp_path / candidate / "github-output"
    output.write_text("", encoding="utf-8")
    script = script.replace("${{ github.sha }}", "landing-sha")
    script = script.replace("${{ github.run_id }}", "99999")
    env = os.environ.copy()
    env["PATH"] = str(fake_bin) + os.pathsep + env.get("PATH", "")
    env["GITHUB_OUTPUT"] = str(output)
    env["FAKE_GH_FILTERED_OUTPUT"] = _filtered_gh_output(jq, candidate)
    result = subprocess.run(
        [BASH, "-e", "-c", script],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    values = [
        line.removeprefix("reuse=")
        for line in output.read_text(encoding="utf-8").splitlines()
        if line.startswith("reuse=")
    ]
    assert len(values) == 1
    return values[0]


def _suite_runs_on_push(doc: dict, branch: str, reuse_value: str) -> bool:
    job = doc["jobs"]["pytest"]
    if "if" in job:
        return False
    reuse, steps, info = reuse_parts(doc)
    if branch == "main" and reuse_value == "true" and _main_reuse_is_wired(doc):
        return False
    if expression(info.get("if")).replace(" ", "") != (
        "needs.plan.outputs.reuse=='true'"
    ):
        return False
    return all(
        step is info
        or (
            "needs.plan.outputs.reuse" in expression(step.get("if"))
            and re.search(
                r"needs\.plan\.outputs\.reuse\s*!=\s*['\"]true['\"]",
                expression(step.get("if")),
            )
            and reuse_value != "true"
        )
        for step in steps
    )


@pytest.mark.skipif(BASH is None, reason="bash is required to execute the workflow script")
def test_landing_runs_at_most_two_suites_when_integration_sha_is_green(tmp_path):
    doc = load_workflow()
    assert _main_reuse_is_wired(doc)
    main_reuse = _run_reuse_script(doc, tmp_path, "green")
    events = [
        ("worktree-lane", "lane-sha", ""),
        ("worktree-integrate-x", "landing-sha", ""),
        ("main", "landing-sha", main_reuse),
    ]
    suite_runs = sum(
        _suite_runs_on_push(doc, branch, reuse_value)
        for branch, _sha, reuse_value in events
    )
    assert suite_runs <= 2


@pytest.mark.skipif(BASH is None, reason="bash is required to execute the workflow script")
def test_main_push_runs_without_a_prior_green_and_does_not_reuse_a_red_sha(tmp_path):
    doc = load_workflow()
    assert _main_reuse_is_wired(doc)
    no_prior_green = _run_reuse_script(doc, tmp_path, "none")
    red_sha = _run_reuse_script(doc, tmp_path, "red")
    assert no_prior_green == "false"
    assert red_sha == "false"
    assert _suite_runs_on_push(doc, "main", no_prior_green)
    assert _suite_runs_on_push(doc, "main", red_sha)


# Minimal helpers copied from tests/test_test_flow_metrics.py for the M2 contract.
def receipt(slug, ended, sha="landing-sha"):
    return {
        "kind": "merge",
        "slug": slug,
        "merge_sha": sha,
        "steps": [
            {"step": "push-main", "ended": ended},
        ],
    }


def run(rid, branch, sha):
    return {
        "databaseId": rid,
        "headBranch": branch,
        "headSha": sha,
        "workflowName": "conductor",
    }


def timed(seconds):
    start = datetime(2026, 1, 2, 10, 0, tzinfo=timezone.utc)
    end = start + timedelta(seconds=seconds)
    return {
        "name": "pytest (ubuntu-latest)",
        "conclusion": "success",
        "startedAt": start.isoformat().replace("+00:00", "Z"),
        "completedAt": end.isoformat().replace("+00:00", "Z"),
    }


def test_m2_metric_still_counts_suite_jobs_over_the_landing():
    import test_flow_metrics as tfm

    landed = [receipt("lane", "2026-01-03T00:00:00Z")]
    runs = [
        run(1, "worktree-lane", "lane-sha"),
        run(2, "worktree-integrate-x", "landing-sha"),
        run(3, "main", "landing-sha"),
    ]
    all_full = {rid: [timed(300)] for rid in (1, 2, 3)}
    reused_main = {1: [timed(300)], 2: [timed(300)], 3: [timed(20)]}

    def count(jobs):
        return tfm.m2_runs_per_landing(
            landed, runs, jobs, since=SINCE, until=UNTIL
        )["per_landing"][0]["suite_runs"]

    assert count(all_full) == 3
    assert count(reused_main) == 2
