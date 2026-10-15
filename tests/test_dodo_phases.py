"""lane-bu-1535-outer-loop: dodo.py runs the `phases:` table, and the harness declares it.

RED-FIRST ([#1535] Done-when (2), (4), (7), (8), ADR-108 section B): authored and witnessed FAILING
before `scripts/run_phase.py`, `ecosystem/schema/phase_receipt.py`, the `phases:` / `constraints:` /
`fates:` rows of `ecosystem/harness.yaml`, dodo's `task_phase` / `task_round`, ADR-130 and the [#689]
note exist. New modules are imported INSIDE helpers and tests, so each test fails on its own rather
than the file failing at collection.

Every test that runs the engine drives a real `doit` subprocess against a toy harness in `tmp_path`
(`stages: []`, `moments: []`, a `phases:` table whose commands are `sys.executable toy.py <id>
<markers>`), receipts home pointed at `tmp_path`, and a UNIQUE `HARNESS_LANE` so the lane+round
keyed doit db never collides. "Executed" is counted from `count.txt`, a file each toy appends its
id to, so the count is what the phase did rather than what doit printed. A toy's behaviour is chosen
by files in the marker dir: `exit-<id>` (exit code), `sleep-<id>` (hang 60 s), `outcome-<id>`
(payload outcome), `badnonce-<id>` (payload carries a wrong nonce).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import textwrap
import time
import uuid
from collections import Counter
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_DODO = _REPO / "scripts" / "dodo.py"
_HARNESS = _REPO / "ecosystem" / "harness.yaml"
for _p in (str(_REPO), str(_REPO / "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_TOY = textwrap.dedent("""\
    import json, os, sys, time
    from pathlib import Path
    pid, mdir = sys.argv[1], Path(sys.argv[2])
    with open(mdir / "count.txt", "a") as fh:
        fh.write(pid + "\\n")
    (mdir / f"started-{pid}").write_text("x")
    if (mdir / f"sleep-{pid}").exists():
        time.sleep(60)
    target = os.environ.get("PHASE_PAYLOAD")
    if target:
        out = mdir / f"outcome-{pid}"
        nonce = os.environ["PHASE_NONCE"]
        if (mdir / f"badnonce-{pid}").exists():
            nonce = "wrong-nonce-0000"
        Path(target).write_text(json.dumps({
            "nonce": nonce, "input_hash": os.environ["PHASE_INPUT_HASH"],
            "outcome": out.read_text().strip() if out.exists() else "ACCEPT"}))
    code = mdir / f"exit-{pid}"
    sys.exit(int(code.read_text()) if code.exists() else 0)
    """)

_EXPECTED_TIMEOUTS = {"P1": 1200, "P2": 1200, "P3": 2700, "P4": 600, "P5": 1800, "P6a": 1200,
                      "P6b": 1200, "P7": 1200}
_BASELINE = ("C-TASK", "C-SCOPE", "C-RED", "C-VENDOR", "C-CLEAN")


# --- helpers ------------------------------------------------------------------------------------

def _lane() -> str:
    return "toy" + uuid.uuid4().hex[:10]


def _markers(tmp: Path) -> Path:
    path = tmp / "markers"
    path.mkdir(exist_ok=True)
    return path


def _write_toy_harness(tmp: Path, *, ids=("P1", "P2", "P3"), judge: str | None = None,
                       inputs: dict[str, list[str]] | None = None, timeouts: dict[str, int] | None = None,
                       fallbacks: dict[str, str] | None = None) -> Path:
    toy = tmp / "toy.py"
    toy.write_text(_TOY, encoding="utf-8")
    markers = _markers(tmp)
    rows = []
    for pid in (*ids, *([judge] if judge else [])):
        row = {"id": pid, "name": pid.lower(), "row_phase": "build", "role": "toy", "cli": "python",
               "model": None, "payload_model": "PhasePayload",
               "gate": "payload" if pid == judge else "exit",
               "timeout_s": (timeouts or {}).get(pid, 60), "budget_usd": 0, "max_rounds": 2,
               "inputs": (inputs or {}).get(pid, []),
               "command": [sys.executable, str(toy), pid, str(markers)]}
        if pid in (fallbacks or {}):
            row["fallback"] = [sys.executable, str(toy), fallbacks[pid], str(markers)]
        rows.append(row)
    path = tmp / "harness.yaml"
    path.write_text(yaml.safe_dump({"stages": [], "moments": [], "phases": rows}, sort_keys=False),
                    encoding="utf-8")
    return path


def _env(tmp: Path, harness: Path, lane: str, round_no: int = 1) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("HARNESS_")}
    env.update({"HARNESS_YAML": str(harness), "HARNESS_RECEIPTS_DIR": str(tmp / "receipts"),
                "HARNESS_LANE": lane, "HARNESS_ROUND": str(round_no), "HARNESS_ROW": "toy-row",
                "DEV_KNOWLEDGE_TELEMETRY_DB": str(tmp / "telemetry.db")})
    return env


def _round_argv() -> list[str]:
    return [sys.executable, "-m", "doit", "-f", str(_DODO), "round"]


def _run_round(tmp: Path, harness: Path, lane: str, round_no: int = 1,
               timeout: int = 240) -> subprocess.CompletedProcess:
    return subprocess.run(_round_argv(), capture_output=True, text=True, cwd=_REPO,
                          env=_env(tmp, harness, lane, round_no), timeout=timeout)


def _counts(tmp: Path) -> Counter:
    path = tmp / "markers" / "count.txt"
    return Counter(path.read_text(encoding="utf-8").split()) if path.is_file() else Counter()


def _receipt_path(tmp: Path, lane: str, pid: str, round_no: int = 1) -> Path:
    return tmp / "receipts" / f"LANE-{lane}" / f"r{round_no}" / f"{pid}.json"


def _receipt(tmp: Path, lane: str, pid: str, round_no: int = 1) -> dict:
    path = _receipt_path(tmp, lane, pid, round_no)
    assert path.is_file(), f"no receipt {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def _kill_tree(proc: subprocess.Popen) -> None:
    import psutil  # noqa: PLC0415 -- never `taskkill /T` (stale parent pids on Windows)

    try:
        root = psutil.Process(proc.pid)
        members = [*root.children(recursive=True), root]
    except psutil.Error:
        members = []
    for member in members:
        try:
            member.kill()
        except psutil.Error:
            pass
    proc.wait(timeout=30)


def _real() -> dict:
    return yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))


def _load_dodo(name: str = "dodo_phases_under_test"):
    import importlib.util  # noqa: PLC0415

    spec = importlib.util.spec_from_file_location(name, _DODO)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- Done-when (2): the phase table runs in order, halts, resumes, and stales on an input ------

def test_a_failing_phase_halts_the_round_and_the_next_phase_never_starts(tmp_path):
    harness = _write_toy_harness(tmp_path)
    (_markers(tmp_path) / "exit-P2").write_text("1")
    lane = _lane()
    out = _run_round(tmp_path, harness, lane)
    assert out.returncode != 0, out.stdout + out.stderr
    assert (tmp_path / "markers" / "started-P2").exists(), "P2 must have run"
    assert not (tmp_path / "markers" / "started-P3").exists(), "P3 started after P2 failed"
    assert _receipt(tmp_path, lane, "P2")["exit_code"] == 1, "a failing phase still writes its receipt"
    assert not _receipt_path(tmp_path, lane, "P3").exists()


def test_an_all_pass_round_writes_a_valid_phase_receipt_per_phase(tmp_path):
    from ecosystem.schema.phase_receipt import PhaseReceipt  # noqa: PLC0415

    harness = _write_toy_harness(tmp_path)
    lane = _lane()
    out = _run_round(tmp_path, harness, lane)
    assert out.returncode == 0, out.stdout + out.stderr
    for pid in ("P1", "P2", "P3"):
        receipt = PhaseReceipt.model_validate(_receipt(tmp_path, lane, pid))
        assert receipt.status == "ok" and receipt.exit_code == 0, pid
        assert receipt.round == 1 and re.fullmatch(r"[0-9a-f]{64}", receipt.input_hash), pid
    assert _counts(tmp_path) == Counter({"P1": 1, "P2": 1, "P3": 1})


def test_a_second_round_after_a_completed_one_executes_nothing(tmp_path):
    harness = _write_toy_harness(tmp_path)
    lane = _lane()
    assert _run_round(tmp_path, harness, lane).returncode == 0
    assert _run_round(tmp_path, harness, lane).returncode == 0
    assert _counts(tmp_path) == Counter({"P1": 1, "P2": 1, "P3": 1}), "fresh receipts must resume as a no-op"


def test_a_phase_killed_mid_way_resumes_there_and_redoes_no_earlier_phase(tmp_path):
    harness = _write_toy_harness(tmp_path, timeouts={"P3": 120})
    markers = _markers(tmp_path)
    (markers / "sleep-P3").write_text("x")
    lane = _lane()
    kwargs = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if sys.platform == "win32"
              else {"start_new_session": True})
    proc = subprocess.Popen(_round_argv(), env=_env(tmp_path, harness, lane), cwd=_REPO,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kwargs)
    try:
        deadline = time.monotonic() + 120
        while (not (markers / "started-P3").exists() and proc.poll() is None
               and time.monotonic() < deadline):
            time.sleep(0.25)
        assert (markers / "started-P3").exists(), "P3 never started"
    finally:
        _kill_tree(proc)
    assert _counts(tmp_path) == Counter({"P1": 1, "P2": 1, "P3": 1})
    (markers / "sleep-P3").unlink()
    resumed = _run_round(tmp_path, harness, lane)
    assert resumed.returncode == 0, resumed.stdout + resumed.stderr
    assert _counts(tmp_path) == Counter({"P1": 1, "P2": 1, "P3": 2}), \
        "the resume must re-run only the killed phase"
    assert _receipt(tmp_path, lane, "P3")["status"] == "ok"


def test_editing_a_declared_input_reruns_that_phase_and_everything_after_it(tmp_path):
    declared = tmp_path / "p2-input.txt"
    declared.write_text("v1", encoding="utf-8")
    harness = _write_toy_harness(tmp_path, inputs={"P2": [str(declared)]})
    lane = _lane()
    assert _run_round(tmp_path, harness, lane).returncode == 0
    declared.write_text("v2", encoding="utf-8")
    assert _run_round(tmp_path, harness, lane).returncode == 0
    assert _counts(tmp_path) == Counter({"P1": 1, "P2": 2, "P3": 2}), \
        "P1 keeps its receipt; P2 re-runs; P3 chains on P2's input hash"


def test_the_judge_gate_reads_a_fresh_payload_and_a_refuse_is_a_successful_task(tmp_path):
    from ecosystem.schema.phase_receipt import PhaseReceipt  # noqa: PLC0415

    harness = _write_toy_harness(tmp_path, ids=("P1",), judge="P7")
    (_markers(tmp_path) / "outcome-P7").write_text("REFUSE")
    lane = _lane()
    out = _run_round(tmp_path, harness, lane)
    assert out.returncode == 0, "a REFUSE is read by the conductor; the task itself succeeds\n" + out.stdout + out.stderr
    receipt = PhaseReceipt.model_validate(_receipt(tmp_path, lane, "P7"))
    assert receipt.status in ("ok", "COMPLETE")
    assert receipt.payload is not None and receipt.payload.outcome == "REFUSE"
    assert receipt.payload_sha256 and receipt.nonce


def test_a_judge_payload_asking_for_input_fails_the_task(tmp_path):
    harness = _write_toy_harness(tmp_path, ids=("P1",), judge="P7")
    (_markers(tmp_path) / "outcome-P7").write_text("INPUT_REQUIRED")
    lane = _lane()
    out = _run_round(tmp_path, harness, lane)
    assert out.returncode != 0, out.stdout + out.stderr
    assert _receipt(tmp_path, lane, "P7")["payload"]["outcome"] == "INPUT_REQUIRED", "the receipt records the ask"


def test_a_payload_carrying_the_wrong_nonce_is_not_harvested(tmp_path):
    harness = _write_toy_harness(tmp_path, ids=("P1",), judge="P7")
    (_markers(tmp_path) / "badnonce-P7").write_text("x")
    lane = _lane()
    out = _run_round(tmp_path, harness, lane)
    assert out.returncode != 0, out.stdout + out.stderr
    assert _receipt(tmp_path, lane, "P7")["status"] == "FAILED"


def test_a_failed_phase_runs_its_declared_fallback_once_and_records_the_substitution(tmp_path):
    harness = _write_toy_harness(tmp_path, ids=("P1", "P2"), fallbacks={"P1": "P1fb"})
    (_markers(tmp_path) / "exit-P1").write_text("1")
    lane = _lane()
    out = _run_round(tmp_path, harness, lane)
    assert out.returncode == 0, out.stdout + out.stderr
    assert _counts(tmp_path) == Counter({"P1": 1, "P1fb": 1, "P2": 1})
    receipt = _receipt(tmp_path, lane, "P1")
    assert receipt["status"] == "ok" and receipt["substituted_from"] == "local"


def test_the_doit_state_file_is_keyed_by_checkout_and_by_lane_and_round(tmp_path):
    dodo = _load_dodo()
    root_a, root_b = tmp_path / "wt-a", tmp_path / "wt-b"
    assert dodo._state_file(root_a) != dodo._state_file(root_b), "two worktrees must not share a db"
    assert dodo._state_file(root_a, "lane", "r1") != dodo._state_file(root_a), "a scope must change the file"
    assert dodo._state_file(root_a, "lane", "r1") != dodo._state_file(root_a, "lane", "r2")
    assert dodo._state_file(root_a, "lane", "r1") == dodo._state_file(root_a, "lane", "r1")


# --- Done-when (7) and (2): the real harness.yaml ----------------------------------------------

def test_the_real_harness_declares_the_eight_phases_with_timeouts_and_two_rounds():
    phases = _real().get("phases") or []
    assert [p["id"] for p in phases] == list(_EXPECTED_TIMEOUTS)
    for row in phases:
        assert row["timeout_s"] == _EXPECTED_TIMEOUTS[row["id"]], row["id"]
        assert row["max_rounds"] == 2, row["id"]
        assert row["gate"] in ("payload", "exit") and row["command"], row["id"]


def test_the_real_harness_constraints_carry_the_five_baseline_ids_always_on():
    rows = {c["id"]: c for c in _real().get("constraints") or []}
    assert set(_BASELINE) <= set(rows)
    for cid in _BASELINE:
        assert rows[cid]["applies_when"].get("always") is True, cid
        assert rows[cid]["kind"] == "deterministic", cid
        assert "--constraint" in rows[cid]["checker"] and cid in rows[cid]["checker"], cid


def test_the_fates_line_records_run_phase_as_manual_until_the_review_date():
    fates = {f["path"]: f for f in _real().get("fates") or []}
    assert "scripts/run_phase.py" in fates
    assert str(fates["scripts/run_phase.py"]["manual_until"]) == "2026-11-15"


def _stage_1(tmp: Path, subject: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("HARNESS_")}
    env.update({"HARNESS_SUBJECT": subject, "HARNESS_KIND": "WIRE",
                "HARNESS_RECEIPTS_DIR": str(tmp / "receipts"),
                "DEV_KNOWLEDGE_TELEMETRY_DB": str(tmp / "telemetry.db")})
    return subprocess.run([sys.executable, "-m", "doit", "-f", "scripts/dodo.py", "--db-file",
                           str(tmp / ".doit.db"), "stage:01-kind-subject"],
                          capture_output=True, text=True, env=env, cwd=_REPO, timeout=180)


def test_stage_1_resolves_a_task_row_subject_and_still_refuses_an_unknown_one(tmp_path):
    found = _stage_1(tmp_path, "1535")
    assert found.returncode == 0, found.stdout + found.stderr
    receipt = json.loads((tmp_path / "receipts" / "SPINE-01-KIND-SUBJECT.json").read_text(encoding="utf-8"))
    assert receipt["exit_code"] == 0
    (tmp_path / "unknown").mkdir()
    missing = _stage_1(tmp_path / "unknown", "99999999")
    assert missing.returncode != 0, "an id in neither tasks/ nor BUILD-LIST must not resolve"


# --- Done-when (8): ADR-130 and the [#689] note ---------------------------------------------------

def test_adr_130_exists_proposed_and_carries_the_required_sections():
    adr = _REPO / "docs" / "decisions" / "ADR-130-the-outer-loop-runs-in-code.md"
    assert adr.is_file()
    assert "**Status:** Proposed" in adr.read_text(encoding="utf-8")
    out = subprocess.run([sys.executable, "scripts/decide_checks.py", "adr-sections", str(adr)],
                         capture_output=True, text=True, cwd=_REPO, timeout=120)
    assert out.returncode == 0, out.stdout + out.stderr


def test_row_689_carries_the_r105_d2_note():
    files = sorted((_REPO / "tasks").glob("689-*.md"))
    assert files, "tasks/689-*.md is missing"
    assert "R105 D2" in files[0].read_text(encoding="utf-8")


@pytest.mark.parametrize("pid", list(_EXPECTED_TIMEOUTS))
def test_every_real_phase_declares_an_inputs_list(pid):
    row = next((p for p in _real().get("phases") or [] if p["id"] == pid), None)
    assert row is not None, f"phase {pid} is not declared"
    assert isinstance(row.get("inputs"), list), pid
