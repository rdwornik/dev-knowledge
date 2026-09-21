"""wave2-spine (L1): `harness.yaml` + `dodo.py` over doit -- a stage with NO command STOPS the run.

RED-FIRST (ADR-108 §B): authored and witnessed FAILING before `dodo.py` / `harness.yaml`
existed; the RED output is quoted in the landing commit body.

SCOPE BOUNDARY (binding, payload §3 L1): the spine PREPARES A CONTRACT. It moves no row through
a phase -- that is [#669] / [#689] ground -- so `test_spine_moves_no_row_through_a_phase` pins it.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_DODO = _REPO / "scripts" / "dodo.py"
_HARNESS = _REPO / "ecosystem" / "harness.yaml"
_KEYS = {"stage", "name", "field", "kind", "command"}
_OPTIONAL_KEYS = {"always", "reason"}  # L1: a row that reads live state says so, in one line


def _run_spine(harness: Path, cwd: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "HARNESS_YAML": str(harness), "HARNESS_KIND": "WIRE",
           "HARNESS_SUBJECT": "x", "HARNESS_RECEIPTS_DIR": str(cwd / "receipts")}
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
    assert len(lines) < 100, f"harness.yaml is {len(lines)} lines; the cap is under 100 (L1: moments added)"
    stages = yaml.safe_load("\n".join(lines))["stages"]
    assert [s["stage"] for s in stages] == list(range(1, 13))
    for s in stages:
        assert _KEYS <= set(s) <= _KEYS | _OPTIONAL_KEYS, s
        assert s["kind"] in {"deterministic", "judgement"}, s


def test_dodo_adapter_stays_small():
    assert len(_DODO.read_text(encoding="utf-8").splitlines()) < 300  # L1: receipts + moments (was 100)


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


def test_stage_argv_is_delivered_verbatim_with_no_shell(tmp_path):
    """Codex terra P1: CmdAction defaulted to shell=True, so an argv token holding shell
    metacharacters (`|`, `&`, `%`) was re-parsed by cmd.exe / sh -c instead of delivered."""
    marker = tmp_path / "arg.txt"
    nasty = "a & b | c %PATH% > d"
    code = f"import sys; open(r'{marker}', 'w', encoding='utf-8').write(sys.argv[1])"
    path = tmp_path / "harness.yaml"
    path.write_text(yaml.safe_dump({"stages": [{
        "stage": 1, "name": "s1", "field": "f", "kind": "deterministic",
        "command": [sys.executable, "-c", code, nasty]}]}), encoding="utf-8")
    result = _run_spine(path, tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert marker.read_text(encoding="utf-8") == nasty


# --- wave3-spine-fixups: stage 6 is wired; the spine leaves no state in the checkout ---------------

def _run_real_spine(db_file: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "HARNESS_KIND": "WIRE", "HARNESS_SUBJECT": "dispatch",
           "HARNESS_RECEIPTS_DIR": str(db_file.parent / "receipts")}
    env.pop("HARNESS_YAML", None)
    return subprocess.run([sys.executable, "-m", "doit", "-f", str(_DODO), "--db-file", str(db_file), "spine"],
                          capture_output=True, text=True, env=env, cwd=_REPO, timeout=900)


def test_real_spine_gets_past_stage_6_on_the_dispatch_subject(tmp_path):
    """L5 built stage 6's CHECK and never wired its FILL: the spine halted at 6 on every real subject."""
    out = _run_real_spine(tmp_path / "doit.db")
    text = out.stdout + out.stderr
    # Anchored to the engine's own STOP line: stage 2 now echoes archive prose (candidate: lines), and
    # the audits about THIS very bug quote the phrase mid-line.
    assert not re.search(r"^STOP: stage 6 does not exist", text, re.MULTILINE), text[-800:]
    # ...and the spine really REACHED stage 6 (a stage-2 failure would otherwise stop it earlier and
    # leave the absence above vacuously true): its receipt is there and records exit 0.
    receipt = next((tmp_path / "receipts").glob("SPINE-06-*.json"), None)
    assert receipt is not None, sorted(p.name for p in (tmp_path / "receipts").glob("*"))
    assert json.loads(receipt.read_text(encoding="utf-8"))["exit_code"] == 0


def test_stage_6_fill_round_trips_through_the_check_and_prose_is_still_refused():
    import stage_library_first as slf  # noqa: PLC0415 -- scripts/ is a sys.path root under pytest
    stage6 = next(s for s in yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))["stages"] if s["stage"] == 6)
    assert stage6["command"], "stage 6 must carry a command"
    out = subprocess.run(stage6["command"], capture_output=True, text=True, encoding="utf-8", cwd=_REPO, timeout=300)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "deptry" in out.stdout
    assert slf.check_contract("library-first:\n" + out.stdout, site="fill") >= 1
    with pytest.raises(slf.StageRefusal):
        slf.check_contract("library-first: we looked and found nothing better", site="prose")


def _doit_state_files() -> set[Path]:
    """doit puts its db beside the dodo file (scripts/), not at the root -- look in both."""
    return set(_REPO.glob(".doit.db*")) | set(_DODO.parent.glob(".doit.db*"))


def _load_dodo():
    import importlib.util  # noqa: PLC0415
    spec = importlib.util.spec_from_file_location("dodo_under_test", _DODO)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_dodo_config_points_state_outside_the_repo():
    dep = Path(_load_dodo().DOIT_CONFIG["dep_file"]).resolve()
    assert _REPO not in dep.parents, f"doit state {dep} lives inside the checkout"
    assert dep.parent.is_dir(), "the parent dir must exist"


def test_dodo_state_is_unique_per_checkout(monkeypatch):
    """Two checkouts (primary + a worktree) must never share a doit lock/db."""
    mod = _load_dodo()
    other = mod._state_file(Path("Z:/another/checkout"))
    assert other != Path(mod.DOIT_CONFIG["dep_file"])
    assert other == mod._state_file(Path("Z:/another/checkout")), "stable for one checkout"


def test_running_the_spine_creates_no_doit_state_in_the_repo(tmp_path):
    before = _doit_state_files()
    harness = _write_harness(tmp_path, tmp_path / "ran.txt", missing=None)
    env = {**os.environ, "HARNESS_YAML": str(harness), "HARNESS_KIND": "WIRE", "HARNESS_SUBJECT": "x",
           "HARNESS_RECEIPTS_DIR": str(tmp_path / "receipts")}
    try:
        subprocess.run([sys.executable, "-m", "doit", "-f", str(_DODO), "spine"],
                       capture_output=True, text=True, env=env, cwd=_REPO, timeout=120)
        created = _doit_state_files() - before
        assert not created, f"the spine left {sorted(p.name for p in created)} in the repo root"
    finally:
        for p in _doit_state_files() - before:
            p.unlink()
