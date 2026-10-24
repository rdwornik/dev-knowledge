"""Main-push reuse must retain a successful Windows verdict when the plan needs it."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "conductor.yml"
BASH = shutil.which("bash")


def load_workflow() -> dict:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    if True in doc and "on" not in doc:
        doc["on"] = doc.pop(True)
    return doc


def reuse_step(doc: dict) -> dict:
    steps = [
        step for step in doc["jobs"]["plan"]["steps"] if step.get("id") == "reuse"
    ]
    assert len(steps) == 1
    return steps[0]


def test_reuse_step_is_bound_to_plan_os_and_checks_windows_job():
    step = reuse_step(load_workflow())

    assert step.get("env", {}).get("PLAN_OS") == "${{ steps.plan.outputs.os }}"
    assert "pytest (windows-latest)" in step["run"]
    assert "gh run view" in step["run"]


@pytest.mark.skipif(BASH is None, reason="bash is required to execute the workflow script")
@pytest.mark.parametrize(
    ("plan_os", "fake_view", "expected_reuse", "expect_view"),
    [
        ('["ubuntu-latest"]', "", "true", False),
        ('["ubuntu-latest","windows-latest"]', "success", "true", True),
        ('["ubuntu-latest","windows-latest"]', "", "false", True),
        ('["ubuntu-latest","windows-latest"]', "failure", "false", True),
        ('["ubuntu-latest","windows-latest"]', "skipped", "false", True),
    ],
)
def test_reuse_requires_a_successful_windows_job_only_when_planned(
    tmp_path, plan_os, fake_view, expected_reuse, expect_view
):
    step = reuse_step(load_workflow())
    script = step["run"]
    script = script.replace("${{ github.sha }}", "landing-sha")
    script = script.replace("${{ github.run_id }}", "99999")

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_gh = fake_bin / "gh"
    fake_gh.write_text(
        "#!/bin/sh\n"
        'case "$1 $2" in\n'
        '  "run list") printf "12345\\n" ;;\n'
        '  "run view") printf "%s\\n" "$FAKE_VIEW"; '
        'printf "view\\n" >> "$FAKE_CALLS" ;;\n'
        '  *) exit 93 ;;\n'
        "esac\n",
        encoding="utf-8",
    )
    fake_gh.chmod(0o755)

    output = tmp_path / "github-output"
    output.write_text("", encoding="utf-8")
    calls = tmp_path / "calls"
    env = os.environ.copy()
    env["PATH"] = str(fake_bin) + os.pathsep + env.get("PATH", "")
    env["GITHUB_OUTPUT"] = str(output)
    env["PLAN_OS"] = plan_os
    env["FAKE_VIEW"] = fake_view
    env["FAKE_CALLS"] = str(calls)

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
    assert values == [expected_reuse]
    assert calls.exists() is expect_view
