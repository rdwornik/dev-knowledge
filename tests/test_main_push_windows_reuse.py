"""Reuse on a push to main must not skip a Windows leg the plan requires (review-2 P1).

The reused run may have been Linux-only while this main push's plan (`os`) includes windows-latest:
reuse is then allowed only if the reused run's `pytest (windows-latest)` job succeeded.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

import test_landing_suite_runs as base

BASH = shutil.which("bash")
LINUX = '["ubuntu-latest"]'
BOTH = '["ubuntu-latest","windows-latest"]'


def _step():
    return base.reuse_parts(base.load_workflow())[0]


def test_reuse_step_binds_plan_os_and_names_the_windows_job():
    step = _step()
    assert base.expression((step.get("env") or {}).get("PLAN_OS")) == "steps.plan.outputs.os"
    assert "gh run view" in step["run"]
    assert "pytest (windows-latest)" in step["run"]


def _run(tmp_path, plan_os: str, view: str):
    script = _step()["run"].replace("${{ github.sha }}", "landing-sha").replace("${{ github.run_id }}", "99999")
    bindir = tmp_path / "bin"
    bindir.mkdir()
    gh = bindir / "gh"
    gh.write_text(
        '#!/bin/sh\n'
        'echo "$1 $2" >> "$FAKE_LOG"\n'
        'if [ "$1 $2" = "run view" ]; then printf \'%s\n\' "$FAKE_VIEW"; else echo 12345; fi\n',
        encoding="utf-8")
    gh.chmod(0o755)
    out, log = tmp_path / "out", tmp_path / "log"
    out.write_text("", encoding="utf-8")
    log.write_text("", encoding="utf-8")
    env = os.environ.copy()
    env.update(PATH=f"{bindir}{os.pathsep}{env['PATH']}", GITHUB_OUTPUT=str(out), FAKE_LOG=str(log),
               FAKE_VIEW=view, PLAN_OS=plan_os)
    r = subprocess.run([BASH, "-e", "-c", script], cwd=Path(__file__).resolve().parent.parent, env=env,
                       text=True, capture_output=True, check=False)
    assert r.returncode == 0, r.stderr
    value = [ln.removeprefix("reuse=") for ln in out.read_text(encoding="utf-8").splitlines() if ln.startswith("reuse=")]
    return value[-1], log.read_text(encoding="utf-8")


@pytest.mark.skipif(BASH is None, reason="bash required")
def test_linux_only_plan_reuses_without_asking_about_windows(tmp_path):
    value, log = _run(tmp_path, LINUX, "")
    assert value == "true"
    assert "run view" not in log


@pytest.mark.skipif(BASH is None, reason="bash required")
def test_windows_plan_reuses_when_the_reused_run_judged_windows_green(tmp_path):
    assert _run(tmp_path, BOTH, "success")[0] == "true"


@pytest.mark.skipif(BASH is None, reason="bash required")
@pytest.mark.parametrize("view", ["", "failure", "skipped"])
def test_windows_plan_does_not_reuse_a_run_that_did_not_judge_windows(tmp_path, view):
    assert _run(tmp_path, BOTH, view)[0] == "false"
