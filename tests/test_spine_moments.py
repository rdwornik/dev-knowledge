"""lane-l1-spine-moments: the spine survives an interruption, and the moments declare where organs fire.

RED-FIRST (ADR-108 §B, DECLARE-NIGHT N2/N4): authored and witnessed FAILING before `dodo.py` /
`harness.yaml` / `telemetry_emit.py wrap` changed; the RED output is quoted in the RED commit body.

Every test that runs the engine drives a real `doit` subprocess against a synthetic harness in
`tmp_path`, with the receipts home pointed at `tmp_path` -- a run never writes into the checkout's
own `logs/`. "Executed" is counted from a marker file each stage appends to, not from doit's log,
so the count is what the stage did rather than what the engine printed.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_DODO = _REPO / "scripts" / "dodo.py"
_HARNESS = _REPO / "ecosystem" / "harness.yaml"
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


# --- helpers ------------------------------------------------------------------------------------

def _env(tmp: Path, harness: Path | None, **extra: str) -> dict[str, str]:
    env = {**os.environ, "HARNESS_RECEIPTS_DIR": str(tmp / "receipts"), "HARNESS_KIND": "WIRE",
           "HARNESS_SUBJECT": "x", "DEV_KNOWLEDGE_TELEMETRY_DB": str(tmp / "telemetry.db")}
    env.pop("HARNESS_YAML", None)
    if harness is not None:
        env["HARNESS_YAML"] = str(harness)
    env.update(extra)
    return env


def _doit_argv(tmp: Path, *targets: str, flags: tuple[str, ...] = ()) -> list[str]:
    return [sys.executable, "-m", "doit", "-f", str(_DODO), "--dir", str(tmp),
            "--db-file", str(tmp / ".doit.db"), *flags, *targets]


def _doit(tmp: Path, harness: Path | None, *targets: str, flags: tuple[str, ...] = (),
          timeout: int = 300, **extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(_doit_argv(tmp, *targets, flags=flags), capture_output=True, text=True,
                          env=_env(tmp, harness, **extra), cwd=tmp, timeout=timeout)


def _touch(marker: Path, tag: str) -> list[str]:
    return [sys.executable, "-c", f"open(r'{marker}', 'a').write('{tag}')"]


def _write(tmp: Path, stages: list[dict], moments: list[dict] | None = None) -> Path:
    doc: dict = {"stages": stages}
    if moments is not None:
        doc["moments"] = moments
    path = tmp / "harness.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


def _three_stages(marker: Path, **overrides: dict) -> list[dict]:
    out = []
    for n in (1, 2, 3):
        row = {"stage": n, "name": f"s{n}", "field": "f", "kind": "deterministic",
               "command": _touch(marker, str(n))}
        row.update(overrides.get(str(n), {}))
        out.append(row)
    return out


def _receipt(tmp: Path, stem: str) -> dict:
    hits = sorted((tmp / "receipts").glob(f"*{stem}*.json"))
    assert hits, f"no receipt matching {stem!r} in {sorted(p.name for p in (tmp / 'receipts').glob('*'))}"
    return json.loads(hits[0].read_text(encoding="utf-8"))


# --- Done-contract 7a: a completed spine is a no-op the second time -----------------------------

def test_a_second_spine_run_after_a_completed_one_executes_zero_tasks(tmp_path):
    marker = tmp_path / "ran.txt"
    harness = _write(tmp_path, _three_stages(marker))
    first = _doit(tmp_path, harness, "spine")
    assert first.returncode == 0, first.stdout + first.stderr
    assert marker.read_text() == "123"
    second = _doit(tmp_path, harness, "spine")
    assert second.returncode == 0, second.stdout + second.stderr
    assert marker.read_text() == "123", "the second run re-executed a stage that had a valid receipt"


# --- Done-contract 7b: a KILLED run resumes at the stage where it stopped ------------------------

def _kill_tree(proc: subprocess.Popen) -> None:
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
    else:
        import signal  # noqa: PLC0415
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    proc.wait(timeout=30)


def test_a_run_killed_mid_way_resumes_at_the_stopped_stage_and_redoes_nothing(tmp_path):
    marker, started = tmp_path / "ran.txt", tmp_path / "started.flag"
    hang = textwrap.dedent(f"""\
        import os, time
        flag, marker = r'{started}', r'{marker}'
        if os.path.exists(flag):
            open(marker, 'a').write('2')
        else:
            open(flag, 'w').write('x')
            time.sleep(300)
        """)
    stages = _three_stages(marker, **{"2": {"command": [sys.executable, "-c", hang]}})
    harness = _write(tmp_path, stages)
    kwargs = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if sys.platform == "win32"
              else {"start_new_session": True})
    proc = subprocess.Popen(_doit_argv(tmp_path, "spine"), env=_env(tmp_path, harness), cwd=tmp_path,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kwargs)
    try:
        deadline = time.monotonic() + 120
        while not started.exists() and time.monotonic() < deadline:
            time.sleep(0.25)
        assert started.exists(), "stage 2 never started"
    finally:
        _kill_tree(proc)
    assert marker.read_text() == "1", "only stage 1 may have completed before the kill"
    resumed = _doit(tmp_path, harness, "spine")
    assert resumed.returncode == 0, resumed.stdout + resumed.stderr
    assert marker.read_text() == "123", "the resume must run stages 2-3 once and NOT redo stage 1"


def test_a_failed_stage_leaves_no_valid_receipt_so_the_rerun_retries_it(tmp_path):
    marker, flag = tmp_path / "ran.txt", tmp_path / "second.flag"
    flaky = textwrap.dedent(f"""\
        import os, sys
        flag = r'{flag}'
        if not os.path.exists(flag):
            open(flag, 'w').write('x'); sys.exit(3)
        open(r'{marker}', 'a').write('2')
        """)
    harness = _write(tmp_path, _three_stages(marker, **{"2": {"command": [sys.executable, "-c", flaky]}}))
    assert _doit(tmp_path, harness, "spine").returncode != 0
    assert _receipt(tmp_path, "S2")["exit_code"] == 3, "a failing run still writes its receipt"
    assert _doit(tmp_path, harness, "spine").returncode == 0
    assert marker.read_text() == "123"


# --- Done-contract 7e: an input change invalidates the receipt ----------------------------------

def test_an_input_change_invalidates_the_receipt_and_the_stage_reruns(tmp_path):
    marker = tmp_path / "ran.txt"
    harness = _write(tmp_path, _three_stages(marker))
    assert _doit(tmp_path, harness, "spine", HARNESS_SUBJECT="alpha").returncode == 0
    assert _doit(tmp_path, harness, "spine", HARNESS_SUBJECT="alpha").returncode == 0
    assert marker.read_text() == "123"
    assert _doit(tmp_path, harness, "spine", HARNESS_SUBJECT="beta").returncode == 0
    assert marker.read_text() == "123123", "a changed subject must re-run every stage that depends on it"


def test_an_upstream_input_change_invalidates_the_downstream_receipts_only(tmp_path):
    """Stage 2's argv changes; stage 1 keeps its receipt, stages 2 AND 3 re-run (3 chains on 2)."""
    marker = tmp_path / "ran.txt"
    harness = _write(tmp_path, _three_stages(marker))
    assert _doit(tmp_path, harness, "spine").returncode == 0
    changed = _three_stages(marker, **{"2": {"command": _touch(marker, "b")}})
    _write(tmp_path, changed)
    assert _doit(tmp_path, harness, "spine").returncode == 0
    assert marker.read_text() == "123b3"


def test_a_stage_declaring_always_true_runs_every_time_and_the_rest_do_not(tmp_path):
    marker = tmp_path / "ran.txt"
    harness = _write(tmp_path, _three_stages(
        marker, **{"2": {"always": True, "reason": "reads live git state"}}))
    assert _doit(tmp_path, harness, "spine").returncode == 0
    assert _doit(tmp_path, harness, "spine").returncode == 0
    assert marker.read_text() == "1232", "stage 3 chains on stage 2's INPUT hash, which did not change"


def test_a_truncated_receipt_is_not_up_to_date(tmp_path):
    marker = tmp_path / "ran.txt"
    harness = _write(tmp_path, _three_stages(marker))
    assert _doit(tmp_path, harness, "spine").returncode == 0
    target = next((tmp_path / "receipts").glob("*S1*.json"))
    target.write_text('{"organ": "s1", "exit_c', encoding="utf-8")
    assert _doit(tmp_path, harness, "spine").returncode == 0
    assert marker.read_text() == "1231", "a receipt that does not parse must not count as done"


# --- Done-contract 2: the receipt's fields ------------------------------------------------------

def test_every_stage_receipt_records_organ_exit_duration_input_hash_and_models(tmp_path):
    marker = tmp_path / "ran.txt"
    harness = _write(tmp_path, _three_stages(marker))
    assert _doit(tmp_path, harness, "spine").returncode == 0
    receipt = _receipt(tmp_path, "S2")
    assert receipt["organ"].endswith("s2")
    assert receipt["exit_code"] == 0 and receipt["status"] == "ok"
    assert isinstance(receipt["duration_ms"], int) and receipt["duration_ms"] >= 0
    assert len(receipt["input_hash"]) == 64
    assert {"model_requested", "model_reported"} <= set(receipt), "the model fields are always present"
    assert receipt["model_requested"] is None and receipt["model_reported"] is None


def test_wrap_writes_a_receipt_and_still_propagates_the_exit_code(tmp_path, monkeypatch):
    import telemetry_emit as te  # noqa: PLC0415
    monkeypatch.setenv("DEV_KNOWLEDGE_TELEMETRY_DB", str(tmp_path / "t.db"))
    receipt = tmp_path / "R.json"
    rc = te.main(["wrap", "organ-x", "--receipt", str(receipt), "--input-hash", "ab" * 32,
                  "--model-requested", "sonnet", "--model-reported", "claude-sonnet-5",
                  "--", "-c", "import sys; sys.exit(4)"])
    assert rc == 4
    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert (data["organ"], data["exit_code"], data["input_hash"]) == ("organ-x", 4, "ab" * 32)
    assert (data["model_requested"], data["model_reported"]) == ("sonnet", "claude-sonnet-5")


def test_wrap_without_receipt_options_is_unchanged(tmp_path, monkeypatch):
    import telemetry_emit as te  # noqa: PLC0415
    monkeypatch.setenv("DEV_KNOWLEDGE_TELEMETRY_DB", str(tmp_path / "t.db"))
    assert te.main(["wrap", "h", "--", "-c", "import sys; sys.exit(0)"]) == 0
    assert list(tmp_path.glob("*.json")) == []


def test_wrap_skipped_not_built_writes_the_receipt_without_running_anything(tmp_path, monkeypatch):
    import telemetry_emit as te  # noqa: PLC0415
    monkeypatch.setenv("DEV_KNOWLEDGE_TELEMETRY_DB", str(tmp_path / "t.db"))
    receipt, ran = tmp_path / "R.json", tmp_path / "ran.txt"
    rc = te.main(["wrap", "organ-y", "--receipt", str(receipt), "--skipped", "SKIPPED-NOT-BUILT",
                  "--", "-c", f"open(r'{ran}', 'w').write('x')"])
    assert rc == 0 and not ran.exists()
    assert json.loads(receipt.read_text(encoding="utf-8"))["status"] == "SKIPPED-NOT-BUILT"


# --- Done-contract 6/7d: the moments ---------------------------------------------------------------

def _moment(name: str, organs: list[dict]) -> dict:
    return {"name": name, "trigger": f"synthetic {name}", "organs": organs}


def test_moment_lane_start_writes_a_receipt_per_organ_including_skipped_not_built(tmp_path):
    marker = tmp_path / "ran.txt"
    organs = [
        {"id": "present", "command": _touch(marker, "p"), "receipt": "MOMENT-LANE-START-PRESENT.json",
         "manual_until": "2026-12-31"},
        {"id": "future", "optional": True, "manual_until": "2026-12-31",
         "command": [sys.executable, "scripts/organ_that_is_not_built_yet.py", "{lane}"],
         "receipt": "MOMENT-LANE-START-FUTURE.json"},
    ]
    harness = _write(tmp_path, _three_stages(marker), [_moment("lane-start", organs)])
    out = _doit(tmp_path, harness, "moment:lane-start")
    assert out.returncode == 0, out.stdout + out.stderr
    assert marker.read_text() == "p", "the moment runs its organs, not the spine's stages"
    assert (tmp_path / "receipts" / "MOMENT-LANE-START-PRESENT.json").is_file()
    future = json.loads((tmp_path / "receipts" / "MOMENT-LANE-START-FUTURE.json").read_text("utf-8"))
    assert future["status"] == "SKIPPED-NOT-BUILT" and future["organ"].endswith("future")
    assert future["exit_code"] is None


def test_a_required_organ_whose_command_is_absent_fails_the_moment(tmp_path):
    marker = tmp_path / "ran.txt"
    organs = [{"id": "gone", "command": [sys.executable, "scripts/never_built_zz.py"],
               "receipt": "MOMENT-LANE-START-GONE.json", "manual_until": "2026-12-31"}]
    harness = _write(tmp_path, _three_stages(marker), [_moment("lane-start", organs)])
    out = _doit(tmp_path, harness, "moment:lane-start")
    assert out.returncode != 0
    assert "never_built_zz" in out.stdout + out.stderr


def test_an_optional_organ_missing_a_required_input_is_skipped_not_failed(tmp_path):
    marker = tmp_path / "ran.txt"
    organs = [{"id": "needs-batch", "optional": True, "manual_until": "2026-12-31",
               "command": _touch(marker, "x") + ["{batch}"], "receipt": "MOMENT-MERGE-NEEDS-BATCH.json"}]
    harness = _write(tmp_path, _three_stages(marker), [_moment("merge", organs)])
    out = _doit(tmp_path, harness, "moment:merge")
    assert out.returncode == 0, out.stdout + out.stderr
    assert not marker.exists()
    assert _receipt(tmp_path, "NEEDS-BATCH")["status"] == "SKIPPED-NO-INPUT"


def test_a_moment_receipt_can_be_a_resume_target_when_the_organ_is_not_always(tmp_path):
    marker = tmp_path / "ran.txt"
    organs = [{"id": "once", "command": _touch(marker, "o"), "receipt": "MOMENT-TEARDOWN-ONCE.json",
               "manual_until": "2026-12-31"},
              {"id": "live", "command": _touch(marker, "L"), "receipt": "MOMENT-TEARDOWN-LIVE.json",
               "manual_until": "2026-12-31", "always": True, "reason": "reads live worktree state"}]
    harness = _write(tmp_path, _three_stages(marker), [_moment("teardown", organs)])
    assert _doit(tmp_path, harness, "moment:teardown").returncode == 0
    assert _doit(tmp_path, harness, "moment:teardown").returncode == 0
    assert marker.read_text() == "oLL"


# --- the real harness.yaml ----------------------------------------------------------------------

def _real() -> dict:
    return yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))


_MOMENT_ORGANS = {
    "lane-start": ["single_flight", "seat_refusals.refuse_no_live_integrator", "routing_agreement",
                   "worktree_occupancy"],
    "merge": ["merge_receipt.models", "review_packet", "gates", "test_pairing"],
    "teardown": ["no_leftovers"],
    "lane-end": ["lane_cost", "fleet_health.seat_health_line", "transport_report", "digest"],
}
_OPTIONAL = {"worktree_occupancy", "gates", "test_pairing", "no_leftovers", "transport_report",
             "digest", "review_packet"}


def test_harness_declares_the_four_moments_with_their_organs():
    moments = {m["name"]: m for m in _real()["moments"]}
    assert set(moments) == set(_MOMENT_ORGANS)
    for name, ids in _MOMENT_ORGANS.items():
        assert [o["id"] for o in moments[name]["organs"]] == ids, name


def test_every_moment_and_organ_carries_the_declared_schema():
    for moment in _real()["moments"]:
        assert isinstance(moment["trigger"], str) and moment["trigger"].strip()
        assert "\n" not in moment["trigger"].strip(), "the trigger is one line"
        for organ in moment["organs"]:
            assert {"id", "command", "receipt"} <= set(organ), organ
            stem = organ["receipt"].rsplit(".", 1)[0]
            assert organ["receipt"].endswith(".json") and stem == stem.upper(), organ["receipt"]
            assert not re.search(r"\d{4}-\d{2}-\d{2}", stem), "a dated name is moved by logs_retention"
            assert isinstance(organ.get("optional", False), bool)
            if organ["id"] in _OPTIONAL:
                assert organ.get("optional") is True, organ["id"]
            if organ.get("manual_until") is not None:
                assert str(organ["manual_until"]) >= "2026-09-20", organ["id"]


def test_every_organ_not_armed_states_a_manual_until_date():
    """Nothing calls a moment yet (the four triggers are wave 2's wiring), so every organ is manual."""
    for moment in _real()["moments"]:
        for organ in moment["organs"]:
            assert organ.get("manual_until"), f"{moment['name']}/{organ['id']} is neither armed nor dated"


def test_every_always_true_row_states_its_reason_in_one_line():
    doc = _real()
    rows = doc["stages"] + [o for m in doc["moments"] for o in m["organs"]]
    always = [r for r in rows if r.get("always")]
    assert always, "the stages that read live state must say so"
    for row in always:
        reason = row.get("reason", "")
        assert reason.strip() and "\n" not in reason.strip(), row


def test_uptodate_false_is_gone_from_the_adapter():
    assert "[False]" not in _DODO.read_text(encoding="utf-8")


# --- Done-contract 4 and 5: stages 7 and 11 -----------------------------------------------------

_CONFORMING = textwrap.dedent("""\
    # LANE lane-a-1-x -- a conforming fixture

    ## Dispatch

    **Shape:** `local`

    ## Worktree pairing

    slug `lane-a-1-x` -> branch `worktree-lane-a-1-x` -> contract `LANE-a-1-x.md`

    ## Done-contract (immutable)

    1. `<something checkable>`
    """)


def test_stage_7_passes_its_positional_argument_and_exits_zero_on_a_normal_contract(tmp_path):
    stage7 = next(s for s in _real()["stages"] if s["stage"] == 7)
    assert stage7["command"], "stage 7 must carry a command"
    contract = tmp_path / "LANE-a-1-x.md"
    contract.write_text(_CONFORMING, encoding="utf-8")
    out = _doit(tmp_path, None, "stage:07-substrate", flags=("-s",), HARNESS_CONTRACT=str(contract))
    assert out.returncode == 0, out.stdout + out.stderr
    assert _receipt(tmp_path, "SUBSTRATE")["exit_code"] == 0


def test_stage_11_fills_the_cap_field_and_never_governs_or_stops(tmp_path):
    stage11 = next(s for s in _real()["stages"] if s["stage"] == 11)
    argv = stage11["command"]
    assert argv and "dispatch.py" in " ".join(argv) and "plan" in argv
    assert "govern" not in argv, "DECLARE N3: no cap may ever stop a task"
    contract = tmp_path / "LANE-a-1-x.md"
    contract.write_text(_CONFORMING + "\n| Model | Mode | Effort |\n|---|---|---|\n| sonnet | execute | high |\n",
                        encoding="utf-8")
    out = _doit(tmp_path, None, "stage:11-token-cap", flags=("-s",), HARNESS_CONTRACT=str(contract))
    assert out.returncode == 0, out.stdout + out.stderr
    receipts = sorted((tmp_path / "receipts").glob("*TOKEN-CAP*.json"))
    assert receipts, sorted(p.name for p in (tmp_path / "receipts").glob("*"))
    receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    assert receipt["exit_code"] == 0
    plan = json.loads((tmp_path / "receipts" / receipt["output_file"]).read_text(encoding="utf-8"))
    assert plan["token_cap"] >= 10**9, "the cap field is a record, set out of any lane's reach"


@pytest.mark.parametrize("stage", range(1, 13))
def test_every_real_stage_row_is_still_present_and_ordered(stage):
    assert [s["stage"] for s in _real()["stages"]][stage - 1] == stage


# --- codex terra review (docs/audits/2026-09-20-codex-l1-spine-moments.md): the three HIGHs ------------

def test_an_in_place_edit_of_a_file_a_stage_names_invalidates_its_receipt(tmp_path):
    """HIGH 1: the hash covers the CONTENT of a file named in argv, not just its path."""
    marker, contract = tmp_path / "ran.txt", tmp_path / "c.md"
    contract.write_text("v1", encoding="utf-8")
    stages = _three_stages(marker, **{"1": {"command": [*_touch(marker, "1"), str(contract)]}})
    harness = _write(tmp_path, stages)
    assert _doit(tmp_path, harness, "spine").returncode == 0
    contract.write_text("v2", encoding="utf-8")
    assert _doit(tmp_path, harness, "spine").returncode == 0
    assert marker.read_text() == "123123"


def test_the_repo_state_fingerprint_is_part_of_the_input_hash(monkeypatch):
    import importlib.util  # noqa: PLC0415
    spec = importlib.util.spec_from_file_location("dodo_state_under_test", _DODO)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "_repo_state", lambda: "head-a")
    first = mod._input_hash(["x"], None)
    monkeypatch.setattr(mod, "_repo_state", lambda: "head-b")
    assert mod._input_hash(["x"], None) != first, "a new commit or edit must stale every receipt"


def test_a_parseable_but_incomplete_receipt_is_not_up_to_date(tmp_path):
    """HIGH 2: `{"status": "ok", "exit_code": 0}` with a matching hash is still not a completion record."""
    marker = tmp_path / "ran.txt"
    harness = _write(tmp_path, _three_stages(marker))
    assert _doit(tmp_path, harness, "spine").returncode == 0
    target = next((tmp_path / "receipts").glob("SPINE-01-*.json"))
    data = json.loads(target.read_text(encoding="utf-8"))
    target.write_text(json.dumps({k: data[k] for k in ("status", "exit_code", "input_hash")}), encoding="utf-8")
    assert _doit(tmp_path, harness, "spine").returncode == 0
    assert marker.read_text() == "1231"


def test_a_receipt_written_for_another_organ_is_not_up_to_date(tmp_path):
    marker = tmp_path / "ran.txt"
    harness = _write(tmp_path, _three_stages(marker))
    assert _doit(tmp_path, harness, "spine").returncode == 0
    target = next((tmp_path / "receipts").glob("SPINE-01-*.json"))
    data = json.loads(target.read_text(encoding="utf-8"))
    target.write_text(json.dumps({**data, "organ": "stage:99-someone-else"}), encoding="utf-8")
    assert _doit(tmp_path, harness, "spine").returncode == 0
    assert marker.read_text() == "1231"


def test_an_optional_organ_with_command_null_is_skipped_not_crashed(tmp_path):
    """HIGH 3: the freshness check must not call `_argv(None)` before the skip branch is reached."""
    marker = tmp_path / "ran.txt"
    organs = [{"id": "nullcmd", "optional": True, "command": None, "manual_until": "2026-12-31",
               "receipt": "MOMENT-TEARDOWN-NULLCMD.json"}]
    harness = _write(tmp_path, _three_stages(marker), [_moment("teardown", organs)])
    out = _doit(tmp_path, harness, "moment:teardown")
    assert out.returncode == 0, out.stdout + out.stderr
    assert _receipt(tmp_path, "NULLCMD")["status"] == "SKIPPED-NOT-BUILT"
