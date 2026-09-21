"""lane-loop-declaration (wave-3 W3-A): the one file declares every moment the loop needs.

RED-FIRST (WAVE3-COMMON rules 1-4; ADR-108 §B): every test is named in the Done-contract's words and was
committed FAILING before `ecosystem/harness.yaml` / `scripts/dodo.py` changed; the RED output is quoted
in the RED commit body. Each test reads its row from the REAL `ecosystem/harness.yaml` and runs it as
written -- through the real `doit -f scripts/dodo.py moment:<name>` engine. Where the real organ would touch
the operator's live transport drive (`transport_report`), the moment is DERIVED from the real declaration
(same ids, order, flags, precondition; only the `command` is swapped for a marker) and a separate test
pins the real command's text. Nothing here writes to the transport, a GO file or a remote.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import re
import stat
import subprocess
import sys
import uuid
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_DODO = _REPO / "scripts" / "dodo.py"
_HARNESS = _REPO / "ecosystem" / "harness.yaml"
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

_HANDBACK = "HANDBACK worktree-lane-fixture @ 0123abc code"
_CONTRACT = """\
# LANE lane-fixture -- a conforming fixture

## Done-contract (immutable)

1. `a thing a reviewer can check`
"""


# --- helpers ------------------------------------------------------------------------------------

def _real() -> dict:
    return yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))


def _moment(name: str) -> dict:
    return next(m for m in _real()["moments"] if m["name"] == name)


def _organ(moment: str, organ_id: str) -> dict:
    return next(o for o in _moment(moment)["organs"] if o["id"] == organ_id)


def _env(tmp: Path, harness: Path | None = None, **extra: str) -> dict[str, str]:
    env = {**os.environ, "HARNESS_RECEIPTS_DIR": str(tmp / "receipts"), "HARNESS_KIND": "WIRE",
           "HARNESS_SUBJECT": "x", "DEV_KNOWLEDGE_TELEMETRY_DB": str(tmp / "telemetry.db"),
           "PYTHONUTF8": "1"}
    for name in ("HARNESS_YAML", "HARNESS_LANE", "HARNESS_BATCH", "HARNESS_MERGE", "HARNESS_SESSION_FILE",
                 "HARNESS_CONTRACT", "HARNESS_HANDBACK", "HARNESS_CHANGED"):
        env.pop(name, None)
    if harness is not None:
        env["HARNESS_YAML"] = str(harness)
    env.update(extra)
    return env


def _doit(tmp: Path, harness: Path | None, target: str, timeout: int = 300, **extra: str):
    return subprocess.run(
        [sys.executable, "-m", "doit", "-f", str(_DODO), "--dir", str(tmp), "--db-file",
         str(tmp / ".doit.db"), target],
        capture_output=True, text=True, env=_env(tmp, harness, **extra), cwd=tmp, timeout=timeout)


def _receipt(tmp: Path, name: str) -> dict:
    return json.loads((tmp / "receipts" / name).read_text(encoding="utf-8"))


def _touch(marker: Path, tag: str, code: int = 0) -> list[str]:
    return [sys.executable, "-c", f"open(r'{marker}', 'a').write('{tag},'); raise SystemExit({code})"]


def _derive(tmp: Path, marker: Path, names: list[str], fail: tuple[str, ...] = (),
            extra_after: dict[str, str] | None = None) -> Path:
    """The REAL moments (ids, order, flags, precondition, receipts) with every command swapped for a marker."""
    moments = []
    for src in _real()["moments"]:
        if src["name"] not in names:
            continue
        moment = copy.deepcopy(src)
        for organ in moment["organs"]:
            organ["command"] = _touch(marker, organ["id"], 3 if organ["id"] in fail else 0)
            organ.pop("optional", None)
        for after, new_id in (extra_after or {}).items():
            if moment["name"] != "lane-end":
                continue
            at = next(i for i, o in enumerate(moment["organs"]) if o["id"] == after)
            moment["organs"].insert(at + 1, {"id": new_id, "receipt": "MOMENT-LANE-END-TAIL.json",
                                             "manual_until": "2026-12-31", "command": _touch(marker, new_id)})
        moments.append(moment)
    stages = [{"stage": 1, "name": "s1", "field": "f", "kind": "deterministic",
               "command": [sys.executable, "-c", "pass"]}]
    path = tmp / "derived-harness.yaml"
    path.write_text(yaml.safe_dump({"stages": stages, "moments": moments}, sort_keys=False), encoding="utf-8")
    return path


def _dodo_module(monkeypatch, **env: str):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    spec = importlib.util.spec_from_file_location(f"dodo_under_test_{uuid.uuid4().hex[:6]}", _DODO)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _fake_claude(tmp: Path) -> Path:
    """`claude agents --json` -> `[]`: the live-session leg of worktree_occupancy without a real CLI."""
    bin_dir = tmp / "bin"
    bin_dir.mkdir()
    if os.name == "nt":
        (bin_dir / "claude.cmd").write_text("@echo off\r\necho []\r\n", encoding="utf-8")
    else:
        exe = bin_dir / "claude"
        exe.write_text("#!/bin/sh\necho '[]'\n", encoding="utf-8")
        exe.chmod(exe.stat().st_mode | stat.S_IEXEC)
    return bin_dir


def _primary_root() -> Path:
    out = subprocess.run(["git", "-C", str(_REPO), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return Path(out).parent


# --- Done-contract 2: `pre-launch` -----------------------------------------------------------------

_PRE_LAUNCH = ["worktree_occupancy", "seat_refusals.refuse_no_live_integrator", "routing_agreement"]


def test_pre_launch_moment_declares_occupancy_live_integrator_and_routing():
    moment = _moment("pre-launch")
    assert [o["id"] for o in moment["organs"]] == _PRE_LAUNCH, "occupancy first: the cheapest refusal spends nothing"
    for organ in moment["organs"]:
        assert organ["receipt"].startswith("MOMENT-PRE-LAUNCH-"), organ["receipt"]
        assert organ.get("manual_until"), organ["id"]
    assert "scripts/worktree_occupancy.py" in _organ("pre-launch", "worktree_occupancy")["command"]
    assert "scripts/seat_refusals.py" in _organ("pre-launch", "seat_refusals.refuse_no_live_integrator")["command"]
    assert "scripts/routing_agreement.py" in _organ("pre-launch", "routing_agreement")["command"]
    assert "launcher" in moment["trigger"], "pre-launch is run by the launcher (R-W3-1: occupancy is caller-side)"


def test_lane_start_keeps_only_in_lane_organs():
    ids = [o["id"] for o in _moment("lane-start")["organs"]]
    assert ids == ["single_flight"]
    assert not set(_PRE_LAUNCH) & set(ids), "an organ that asks 'is this slug taken' cannot run inside the lane"


def test_pre_launch_refuses_an_occupied_fixture_slug(tmp_path):
    slug = f"zz-w3a-occupied-{uuid.uuid4().hex[:8]}"
    tree = _primary_root() / ".claude" / "worktrees" / slug
    made_parent = not tree.parent.exists()
    tree.mkdir(parents=True)
    try:
        path = f"{_fake_claude(tmp_path)}{os.pathsep}{os.environ['PATH']}"
        out = _doit(tmp_path, None, "moment:pre-launch", HARNESS_LANE=slug, HARNESS_BATCH="fixture", PATH=path)
    finally:
        tree.rmdir()
        if made_parent:
            tree.parent.rmdir()
    assert not tree.exists(), "the fixture directory must not outlive the test"
    assert out.returncode != 0, "an occupied slug must refuse the launch\n" + out.stdout + out.stderr
    occupancy = _receipt(tmp_path, "MOMENT-PRE-LAUNCH-WORKTREE-OCCUPANCY.json")
    assert occupancy["exit_code"] == 1 and occupancy["status"] == "failed"
    text = (tmp_path / "receipts" / "MOMENT-PRE-LAUNCH-WORKTREE-OCCUPANCY-OUTPUT.txt").read_text(encoding="utf-8")
    assert "OCCUPIED" in text and "directory" in text, text
    assert not (tmp_path / "receipts" / "MOMENT-PRE-LAUNCH-NO-LIVE-INTEGRATOR.json").exists(), \
        "the launch was refused, so nothing after the occupancy check may have run"
    assert not (tmp_path / "receipts" / "MOMENT-PRE-LAUNCH-ROUTING-AGREEMENT.json").exists()


def test_pre_launch_lets_a_free_slug_through_the_occupancy_organ(tmp_path):
    slug = f"zz-w3a-free-{uuid.uuid4().hex[:8]}"
    path = f"{_fake_claude(tmp_path)}{os.pathsep}{os.environ['PATH']}"
    _doit(tmp_path, None, "moment:pre-launch", HARNESS_LANE=slug, HARNESS_BATCH="fixture", PATH=path)
    occupancy = _receipt(tmp_path, "MOMENT-PRE-LAUNCH-WORKTREE-OCCUPANCY.json")
    assert occupancy["exit_code"] == 0 and occupancy["status"] == "ok", occupancy


# --- Done-contract 3: `lane-end` fires once ---------------------------------------------------------

def test_lane_end_declares_a_handback_precondition_and_the_report_continues_on_failure():
    moment = _moment("lane-end")
    pre = moment["precondition"]
    assert pre["file"] == "{session_file}" and pre["receipt"] == "MOMENT-LANE-END-PRECONDITION.json"
    assert re.search(pre["matches"], _HANDBACK, re.M), "the declared pattern must match a real HANDBACK line"
    assert not re.search(pre["matches"], "no closing line here", re.M)
    ids = [o["id"] for o in moment["organs"]]
    assert "digest" not in ids, "the digest moved to batch-close (R-W3-3)"
    report = _organ("lane-end", "transport_report")
    assert report.get("continue_on_failure") is True
    assert ids.index("transport_report") > ids.index("lane_cost"), \
        "the report copies the lane's receipts, so the receipts it copies must exist first"
    assert "scripts/transport_report.py" in report["command"]


def test_lane_end_with_no_handback_line_writes_a_skipped_receipt_and_runs_no_organ(tmp_path):
    # The precondition, ids and order are the REAL declaration's; the commands are markers, because a
    # regression here must not be able to write the operator's live transport from a test.
    marker = tmp_path / "ran.txt"
    harness = _derive(tmp_path, marker, ["lane-end"])
    session = tmp_path / "SESSION-lane-fixture.md"
    session.write_text("# session\n\nstill working, no closing line yet\n", encoding="utf-8")
    for fixture in (tmp_path / "does-not-exist.md", session):
        for stale in (tmp_path / "receipts").glob("*") if (tmp_path / "receipts").exists() else []:
            stale.unlink()
        out = _doit(tmp_path, harness, "moment:lane-end", HARNESS_LANE="lane-fixture",
                    HARNESS_SESSION_FILE=str(fixture))
        assert out.returncode == 0, out.stdout + out.stderr
        skipped = _receipt(tmp_path, "MOMENT-LANE-END-PRECONDITION.json")
        assert skipped["status"] == "SKIPPED-PRECONDITION" and skipped["exit_code"] is None
        names = sorted(p.name for p in (tmp_path / "receipts").glob("MOMENT-LANE-END-*.json"))
        assert names == ["MOMENT-LANE-END-PRECONDITION.json"], f"an organ ran: {names}"
        assert not marker.exists(), f"an organ command ran: {marker.read_text()}"


def test_lane_end_runs_its_organs_in_order_once_the_handback_line_is_present(tmp_path):
    marker = tmp_path / "ran.txt"
    session = tmp_path / "SESSION-lane-fixture.md"
    session.write_text(f"# session\n\nwork\n\n{_HANDBACK}\n", encoding="utf-8")
    harness = _derive(tmp_path, marker, ["lane-end"])
    out = _doit(tmp_path, harness, "moment:lane-end", HARNESS_LANE="lane-fixture",
                HARNESS_SESSION_FILE=str(session))
    assert out.returncode == 0, out.stdout + out.stderr
    assert marker.read_text() == "lane_cost,fleet_health.seat_health_line,transport_report,"
    assert _receipt(tmp_path, "MOMENT-LANE-END-PRECONDITION.json")["status"] == "ok"


def test_a_failing_report_is_recorded_and_does_not_stop_the_moments_remaining_organs(tmp_path):
    marker = tmp_path / "ran.txt"
    session = tmp_path / "SESSION-lane-fixture.md"
    session.write_text(_HANDBACK + "\n", encoding="utf-8")
    harness = _derive(tmp_path, marker, ["lane-end"], fail=("transport_report",),
                      extra_after={"transport_report": "after_report"})
    out = _doit(tmp_path, harness, "moment:lane-end", HARNESS_LANE="lane-fixture",
                HARNESS_SESSION_FILE=str(session))
    assert marker.read_text().endswith("transport_report,after_report,"), \
        f"an organ after the failing report did not run: {marker.read_text()}\n{out.stdout}{out.stderr}"
    report = _receipt(tmp_path, "MOMENT-LANE-END-TRANSPORT-REPORT.json")
    assert report["exit_code"] == 3 and report["status"] == "failed", "the failure is RECORDED"
    assert out.returncode != 0, "and the moment does not report success over it"
    assert "transport_report" in out.stdout + out.stderr


def test_a_failing_report_does_not_stop_the_digest(tmp_path):
    marker = tmp_path / "ran.txt"
    session = tmp_path / "SESSION-lane-fixture.md"
    session.write_text(_HANDBACK + "\n", encoding="utf-8")
    lane_end = _derive(tmp_path, marker, ["lane-end"], fail=("transport_report",))
    _doit(tmp_path, lane_end, "moment:lane-end", HARNESS_LANE="lane-fixture", HARNESS_SESSION_FILE=str(session))
    digest = _doit(tmp_path, None, "moment:batch-close", HARNESS_BATCH="toy-batch")   # the REAL declared row
    assert digest.returncode == 0, digest.stdout + digest.stderr
    assert _receipt(tmp_path, "MOMENT-BATCH-CLOSE-DIGEST.json")["status"] == "ok"
    assert "toy-batch" in digest.stdout, "the digest names the batch it closed"
    assert "transport report" in digest.stdout, "and it reads the failed report as an open item, not a stop"


def test_an_organ_that_does_not_continue_on_failure_still_stops_the_moment(tmp_path):
    marker = tmp_path / "ran.txt"
    session = tmp_path / "SESSION-lane-fixture.md"
    session.write_text(_HANDBACK + "\n", encoding="utf-8")
    harness = _derive(tmp_path, marker, ["lane-end"], fail=("lane_cost",))
    out = _doit(tmp_path, harness, "moment:lane-end", HARNESS_LANE="lane-fixture",
                HARNESS_SESSION_FILE=str(session))
    assert out.returncode != 0
    assert marker.read_text() == "lane_cost,", "continue_on_failure is per organ, never a moment-wide amnesty"


# --- Done-contract 4: `batch-close` ------------------------------------------------------------------

def test_batch_close_moment_declares_the_digest_run_by_the_integrator():
    moment = _moment("batch-close")
    assert [o["id"] for o in moment["organs"]] == ["digest"]
    digest = moment["organs"][0]
    assert digest["receipt"] == "MOMENT-BATCH-CLOSE-DIGEST.json" and digest.get("manual_until")
    assert "scripts/lane_digest.py" in digest["command"]
    assert "integrator" in moment["trigger"] and "last merge" in moment["trigger"]


def test_batch_close_digest_row_runs_as_declared_and_exits_zero_on_an_empty_receipts_dir(tmp_path):
    out = _doit(tmp_path, None, "moment:batch-close", HARNESS_BATCH="toy-batch")
    assert out.returncode == 0, out.stdout + out.stderr
    assert "toy-batch" in out.stdout


# --- Done-contract 5: `merge` -- `{merge}` and `go_reader` -------------------------------------------

def test_the_merge_review_row_uses_the_merge_placeholder_not_a_range():
    command = [str(t) for t in _organ("merge", "review_packet")["command"]]
    assert "--merge" in command and command[command.index("--merge") + 1] == "{merge}"
    assert "--range" not in command, "a merge sha and a range are exclusive to review_packet"
    assert "--changed" not in command, "the packet reads the file list off the merge itself"


def test_the_merge_placeholder_resolves(monkeypatch):
    mod = _dodo_module(monkeypatch, HARNESS_MERGE="deadbeef1234")
    assert mod._argv(["--merge", "{merge}"]) == ["--merge", "deadbeef1234"]
    monkeypatch.delenv("HARNESS_MERGE")
    assert mod._argv(["--merge", "{merge}"]) == ["--merge", "HEAD"], \
        "the integrator merges then runs the moment, so HEAD is the merge commit"


def test_the_declared_review_row_runs_as_written_against_a_real_merge(tmp_path, monkeypatch):
    merges = subprocess.run(["git", "-C", str(_REPO), "rev-list", "--merges", "--first-parent", "-n", "1", "HEAD"],
                            capture_output=True, text=True).stdout.split()
    if not merges:
        pytest.skip("this checkout carries no merge commit to review")
    contract = tmp_path / "LANE-fixture.md"
    contract.write_text(_CONTRACT, encoding="utf-8")
    mod = _dodo_module(monkeypatch, HARNESS_LANE="lane-fixture", HARNESS_MERGE=merges[0],
                       HARNESS_CONTRACT=str(contract), HARNESS_HANDBACK=_HANDBACK,
                       HARNESS_RECEIPTS_DIR=str(tmp_path / "receipts"))
    argv = mod._argv(_organ("merge", "review_packet")["command"])
    proc = subprocess.run(argv, capture_output=True, text=True, cwd=_REPO, timeout=300)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    packet = tmp_path / "receipts" / "MOMENT-MERGE-REVIEW-PACKET.md"
    assert packet.is_file() and merges[0][:7] in packet.read_text(encoding="utf-8")


def test_a_go_reader_organ_is_declared_optional_at_the_merge_moment_until_it_is_built():
    organ = _organ("merge", "go_reader")
    assert organ["optional"] is True and organ["receipt"] == "MOMENT-MERGE-GO-READER.json"
    assert organ["owner"] == "lane-merge-truth", "the census names the lane that owes an unbuilt organ"
    command = [str(t) for t in organ["command"]]
    assert "scripts/go_reader.py" in command and "{batch}" in command
    ids = [o["id"] for o in _moment("merge")["organs"]]
    assert ids.index("merge_receipt.models") < ids.index("go_reader") < ids.index("review_packet")


def test_the_declared_go_reader_row_runs_as_written(tmp_path, monkeypatch):
    """Unbuilt -> SKIPPED-NOT-BUILT (N4). Once W3-C builds it, an absent GO file must refuse."""
    mod = _dodo_module(monkeypatch, HARNESS_BATCH=f"zz-no-such-batch-{uuid.uuid4().hex[:6]}",
                       HARNESS_RECEIPTS_DIR=str(tmp_path / "receipts"))
    row = _organ("merge", "go_reader")
    argv = mod._argv(row["command"])
    if mod._absent(argv):
        assert row["optional"] is True
        return
    proc = subprocess.run(argv, capture_output=True, text=True, cwd=_REPO, timeout=120)
    assert proc.returncode != 0, "a batch with no GO file must be refused\n" + proc.stdout + proc.stderr


# --- Done-contract 6: the 36 organs with no caller ---------------------------------------------------

_FATE_KEYS = ("moment", "manual_until", "retire_candidate")
_PRE_LANE_ORGANS = [
    "single_flight", "seat_refusals.refuse_no_live_integrator", "routing_agreement", "worktree_occupancy",
    "merge_receipt.models", "review_packet", "gates", "test_pairing", "no_leftovers", "lane_cost",
    "fleet_health.seat_health_line", "transport_report", "digest"]


def _fates() -> list[dict]:
    return _real()["fates"]


def test_the_36_fates_list_parses_and_records_exactly_one_fate_per_organ():
    fates = _fates()
    assert len(fates) >= 36
    paths = [f["path"] for f in fates]
    assert len(paths) == len(set(paths)), "one recorded fate per organ, never two"
    declared_moments = {m["name"] for m in _real()["moments"]}
    for fate in fates:
        held = [k for k in _FATE_KEYS if fate.get(k)]
        assert len(held) == 1, f"{fate['path']} holds {held or 'no fate'}"
        assert (_REPO / fate["path"]).is_file(), f"{fate['path']} names a file that is not there"
        if "moment" in held:
            assert fate["moment"] in declared_moments
        else:
            reason = str(fate.get("reason", ""))
            assert reason.strip() and "\n" not in reason.strip(), f"{fate['path']}: a fate carries a one-line reason"
        if "manual_until" in held:
            assert str(fate["manual_until"]) >= "2026-09-21", fate["path"]
        if "retire_candidate" in held:
            assert fate["retire_candidate"] is True


def test_the_fates_cover_every_organ_the_census_names():
    import graph_queries as gq  # noqa: PLC0415
    rows = gq.organ_moments(_REPO)
    census = {r.path for r in rows if r.status == gq.MOMENT_NOWHERE and not r.wired_elsewhere}
    recorded = {f["path"] for f in _fates()}
    assert census, "the census names no uncalled organ -- the fixture is vacuous"
    assert census <= recorded, f"organs with no caller and no recorded fate: {sorted(census - recorded)}"


def test_no_organ_is_dropped_from_the_roster():
    declared = {o["id"] for m in _real()["moments"] for o in m["organs"]}
    assert set(_PRE_LANE_ORGANS) <= declared, sorted(set(_PRE_LANE_ORGANS) - declared)


def test_a_fate_never_narrows_what_counts_as_an_organ():
    """Retirement is a later GO: nothing in the declaration may disarm, delete or hide a script."""
    for fate in _fates():
        assert (_REPO / fate["path"]).is_file()
    stages = _real()["stages"]
    assert [s["stage"] for s in stages] == list(range(1, 13)), "the twelve stages are untouched"


# --- Done-contract 7: dodo.py ------------------------------------------------------------------------

def test_dodo_evaluates_the_lane_end_precondition_from_the_declared_row(tmp_path, monkeypatch):
    session = tmp_path / "SESSION-lane-fixture.md"
    mod = _dodo_module(monkeypatch, HARNESS_LANE="lane-fixture", HARNESS_SESSION_FILE=str(session))
    pre = _moment("lane-end")["precondition"]
    met, why = mod._precondition_met(pre)
    assert met is False and "session" in why.lower(), why
    session.write_text("work\n" + _HANDBACK + "\n", encoding="utf-8")
    assert mod._precondition_met(pre)[0] is True
    session.write_text("mentions HANDBACK in the middle of a sentence only\n", encoding="utf-8")
    assert mod._precondition_met(pre)[0] is False, "the line must BEGIN with HANDBACK, not merely contain it"
