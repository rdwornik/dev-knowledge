"""wave2-spine (L1): `harness.yaml` + `dodo.py` over doit -- a stage with NO command STOPS the run.

RED-FIRST (ADR-108 §B): authored and witnessed FAILING before `dodo.py` / `harness.yaml`
existed; the RED output is quoted in the landing commit body.

SCOPE BOUNDARY (binding, payload §3 L1): the spine PREPARES A CONTRACT. It moves no row through
a phase -- that is [#669] / [#689] ground -- so `test_spine_moves_no_row_through_a_phase` pins it.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

_REPO = Path(__file__).resolve().parents[1]
_DODO = _REPO / "scripts" / "dodo.py"
_HARNESS = _REPO / "ecosystem" / "harness.yaml"
_KEYS = {"stage", "name", "field", "kind", "command"}


def _run_spine(harness: Path, cwd: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "HARNESS_YAML": str(harness), "HARNESS_KIND": "WIRE",
           "HARNESS_SUBJECT": "x"}
    return subprocess.run([sys.executable, "-m", "doit", "-f", str(_DODO), "--dir", str(cwd),
                           "--db-file", str(cwd / ".doit.db"), "spine"],
                          capture_output=True, text=True, env=env, cwd=cwd, timeout=120)


def _write_harness(tmp: Path, marker: Path, missing: int | None) -> Path:
    """Three stages; stage `missing` (if any) has no command; the others touch a marker file."""
    stages = []
    for n in (1, 2, 3):
        touch = [sys.executable, "-c", f"open(r'{marker}', 'a').write('{n}')"]
        stages.append({"stage": n, "name": f"s{n}", "field": "f", "kind": "deterministic",
                       "command": None if n == missing else touch})
    path = tmp / "harness.yaml"
    path.write_text(yaml.safe_dump({"stages": stages}), encoding="utf-8")
    return path


def test_stage_without_command_stops_run_and_names_stage(tmp_path):
    marker = tmp_path / "ran.txt"
    result = _run_spine(_write_harness(tmp_path, marker, missing=2), tmp_path)
    assert result.returncode != 0, "a stage with no command must fail the run"
    assert "stage 2 does not exist" in result.stdout + result.stderr
    assert marker.read_text() == "1", "the run must STOP at stage 2 -- stage 3 must not execute"


def test_run_with_every_stage_commanded_completes(tmp_path):
    marker = tmp_path / "ran.txt"
    result = _run_spine(_write_harness(tmp_path, marker, missing=None), tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert marker.read_text() == "123"


def test_harness_yaml_declares_stages_1_to_12_within_caps():
    lines = _HARNESS.read_text(encoding="utf-8").splitlines()
    assert len(lines) < 60, f"harness.yaml is {len(lines)} lines; the cap is under 60"
    stages = yaml.safe_load("\n".join(lines))["stages"]
    assert [s["stage"] for s in stages] == list(range(1, 13))
    for s in stages:
        assert set(s) == _KEYS, s
        assert s["kind"] in {"deterministic", "judgement"}, s


def test_dodo_adapter_is_under_100_lines():
    assert len(_DODO.read_text(encoding="utf-8").splitlines()) < 100


def test_spine_moves_no_row_through_a_phase():
    """[#669]/[#689] own phase transitions; a `perform` verb here would close [#669] by accident."""
    code = _DODO.read_text(encoding="utf-8")
    assert not re.search(r"(def|task_)\s*\w*perform|transition", code), "no perform/transition verb"
    for s in yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))["stages"]:
        assert "phase" not in s["name"]
        assert "phase" not in " ".join(s["command"] or [])


def test_prior_art_stage_completes_on_a_subject_with_zero_hits():
    """Codex terra P1: an empty prior-art search is a RESULT, not a failure -- stage 2 must exit 0
    on zero hits so the run reaches the real STOP instead of dying at the search."""
    stage2 = next(s for s in yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))["stages"]
                  if s["stage"] == 2)
    argv = [t.replace("{subject}", "zzqq-no-such-subject-9f3a") for t in stage2["command"]]
    result = subprocess.run(argv, capture_output=True, text=True, cwd=_REPO, timeout=60)
    assert result.returncode == 0, (argv, result.returncode, result.stderr)
