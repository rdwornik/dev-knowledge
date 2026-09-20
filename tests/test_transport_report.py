"""lane-l8-lane-end: transport_report -- every finished lane reports to the transport by itself.

RED-first (ADR-108 s.B, DECLARE-NIGHT N2/N3): authored and witnessed FAILING before
`scripts/transport_report.py` and `scripts/lane_digest.py` existed.

The report runs at EVERY turn end of a background lane, inside a 15-second budget shared with another
hook. The tests pin the two facts that follow from that: it is idempotent (one artifact, replaced) and
it can never stop the session (an unmounted drive is a recorded refusal, never a fallback, never a
claim of delivery, never exit code 2 -- a Stop hook's blocking code).

Every test drives a synthetic transport root in `tmp_path`; nothing touches the real drive.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
_REPORT = _SCRIPTS / "transport_report.py"
_DIGEST = _SCRIPTS / "lane_digest.py"
_TELEMETRY = _SCRIPTS / "telemetry_emit.py"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

LANE = "lane-l8-lane-end"


def _mod(name: str):
    return importlib.import_module(name)


# --- fixtures -----------------------------------------------------------------------------------

def _receipt(organ: str, status: str = "ok", exit_code: int = 0, duration_ms: int = 12) -> dict:
    return {"schema": 1, "organ": organ, "status": status, "exit_code": exit_code,
            "duration_ms": duration_ms, "input_hash": "abc123", "model_requested": None,
            "model_reported": None, "command": ["x"], "output_file": None,
            "finished_at": "2026-09-20T10:00:00+00:00"}


def _write_receipts(receipts: Path, rows: list[dict]) -> None:
    receipts.mkdir(parents=True, exist_ok=True)
    for row in rows:
        (receipts / f"MOMENT-{row['organ'].upper().replace('_', '-')}.json").write_text(
            json.dumps(row), encoding="utf-8")


@pytest.fixture()
def world(tmp_path: Path) -> dict:
    root = tmp_path / "drive"
    (root / "to-browser").mkdir(parents=True)
    (root / "to-cc").mkdir()
    receipts = tmp_path / "receipts"
    _write_receipts(receipts, [_receipt("lane_cost"), _receipt("digest", "SKIPPED-NOT-BUILT", 0)])
    downloads = tmp_path / "home" / "Downloads"
    downloads.mkdir(parents=True)
    return {"root": root, "browser": root / "to-browser", "agent": root / "to-cc",
            "receipts": receipts, "downloads": downloads, "home": tmp_path / "home", "tmp": tmp_path}


def _run(world: dict, *extra: str, root: Path | None = None, lane: str = LANE,
         **env: str) -> subprocess.CompletedProcess:
    argv = [sys.executable, str(_REPORT), "--lane", lane,
            "--transport-root", str(root if root is not None else world["root"]),
            "--receipts-dir", str(world["receipts"]), "--repo", str(world["tmp"]), *extra]
    full_env = {**os.environ, "USERPROFILE": str(world["home"]), "HOME": str(world["home"]), **env}
    return subprocess.run(argv, capture_output=True, text=True, env=full_env, timeout=60)


def _result(proc: subprocess.CompletedProcess) -> dict:
    """The report prints exactly one JSON object on stdout -- the wrapper captures it as the
    receipt's output file."""
    assert proc.stdout.strip(), f"no stdout; stderr={proc.stderr!r}"
    return json.loads(proc.stdout.strip().splitlines()[-1])


def _files(folder: Path) -> list[str]:
    return sorted(p.name for p in folder.iterdir())


# --- 1. a report lands and is verified by read-back ---------------------------------------------

def test_report_lands_in_browser_folder_and_is_verified(world):
    proc = _run(world)
    assert proc.returncode == 0, proc.stderr
    res = _result(proc)
    assert res["delivered"] is True and res["verified"] is True
    landed = world["browser"] / res["artifact"]
    assert landed.is_file()
    body = landed.read_text(encoding="utf-8")
    assert LANE in body
    # the lane's receipts are carried, verbatim
    assert '"organ": "lane_cost"' in body and '"organ": "digest"' in body
    # the verification is a real read-back: the recorded hash is the hash of the bytes on disk
    assert res["sha256"] == hashlib.sha256(landed.read_bytes()).hexdigest()


def test_report_never_touches_the_agent_bound_folder(world):
    assert _run(world).returncode == 0
    assert _files(world["agent"]) == []


def test_a_readback_mismatch_is_a_failed_delivery_not_a_claimed_one(world):
    tr = _mod("transport_report")
    dest = world["browser"] / "LANE-END-x.md"
    with pytest.raises(tr.DeliveryFailed):
        tr.deliver(dest, b"what we wrote", read=lambda _p: b"what the drive kept")
    assert not [n for n in _files(world["browser"]) if n.endswith(".tmp")]


def test_a_delivery_that_lands_is_read_back_by_deliver(world):
    tr = _mod("transport_report")
    dest = world["browser"] / "LANE-END-x.md"
    digest = tr.deliver(dest, b"payload")
    assert digest == hashlib.sha256(b"payload").hexdigest()
    assert dest.read_bytes() == b"payload"


# --- 2. idempotent, cheap, runtime recorded -----------------------------------------------------

def test_two_consecutive_runs_leave_one_artifact_not_two(world):
    assert _run(world).returncode == 0
    first = _files(world["browser"])
    assert _run(world).returncode == 0
    second = _files(world["browser"])
    assert len(first) == 1 and second == first
    assert not [n for n in second if n.endswith(".tmp")]


def test_a_rerun_replaces_the_artifact_content(world):
    assert _run(world).returncode == 0
    _write_receipts(world["receipts"], [_receipt("gates", "failed", 1)])
    assert _run(world).returncode == 0
    (only,) = [p for p in world["browser"].iterdir()]
    text = only.read_text(encoding="utf-8")
    assert '"organ": "gates"' in text
    assert text.count(f"# {LANE}") == 1   # replaced, not appended


def test_the_report_records_its_own_runtime(world):
    res = _result(_run(world))
    assert isinstance(res["runtime_ms"], int) and res["runtime_ms"] >= 0


def test_the_runtime_is_measured_not_defaulted(world, monkeypatch, capsys):
    """A controlled clock: the recorded runtime is the elapsed time, so removing the measurement
    (which would leave the default 0) fails here."""
    tr = _mod("transport_report")
    ticks = iter([100.0, 100.25, 100.5, 100.75])
    monkeypatch.setattr(tr.time, "perf_counter", lambda: next(ticks))
    code = tr.main(["--lane", LANE, "--transport-root", str(world["root"]),
                    "--receipts-dir", str(world["receipts"]), "--repo", str(world["tmp"])])
    assert code == 0
    res = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert res["runtime_ms"] == 250


def test_an_oversized_receipt_is_bounded_and_marked(world):
    tr = _mod("transport_report")
    big = world["receipts"] / "MOMENT-BIG.json"
    big.write_text('{"organ": "big", "pad": "' + "x" * (tr.MAX_RECEIPT_BYTES * 4) + '"}', encoding="utf-8")
    ((name, text),) = [r for r in tr.collect_receipts(world["receipts"]) if r[0] == "MOMENT-BIG.json"]
    assert len(text) < tr.MAX_RECEIPT_BYTES + 100 and "truncated" in text


def test_runtime_lands_in_the_wrapper_receipt_and_a_refusal_is_a_nonzero_receipt(world):
    """Through the real wrapper -- the receipt the audit check reads."""
    receipt = world["tmp"] / "MOMENT-LANE-END-TRANSPORT-REPORT.json"
    out = world["tmp"] / "MOMENT-LANE-END-TRANSPORT-REPORT-OUTPUT.txt"
    gone = world["tmp"] / "drive-not-mounted"
    argv = [sys.executable, str(_TELEMETRY), "wrap", "transport_report", "--receipt", str(receipt),
            "--stdout-file", str(out), "--input-hash", "h", "--",
            str(_REPORT), "--lane", LANE, "--transport-root", str(gone),
            "--receipts-dir", str(world["receipts"]), "--repo", str(world["tmp"])]
    env = {**os.environ, "DEV_KNOWLEDGE_TELEMETRY_DB": str(world["tmp"] / "t.db")}
    proc = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=60)
    assert proc.returncode != 0
    rec = json.loads(receipt.read_text(encoding="utf-8"))
    assert rec["exit_code"] != 0 and rec["status"] != "ok"
    assert isinstance(rec["duration_ms"], int)
    assert json.loads(out.read_text(encoding="utf-8").strip().splitlines()[-1])["delivered"] is False


def test_the_git_summary_cannot_eat_the_shared_budget():
    tr = _mod("transport_report")
    assert tr.GIT_TIMEOUT_S <= 3      # the hook budget is 15 s and is shared with another hook


def test_the_two_git_calls_of_one_summary_get_the_same_deadline(world, monkeypatch):
    tr = _mod("transport_report")
    seen: list[float] = []

    def fake_git(_repo, args, deadline):
        seen.append(deadline)
        return "## worktree-x\n" if args[0] == "status" else "abc one\n"

    monkeypatch.setattr(tr, "_git", fake_git)
    tr.session_summary(world["tmp"])
    assert len(seen) >= 2 and len(set(seen)) == 1


# --- the destination is judged by where it RESOLVES ---------------------------------------------

def _link(link: Path, target: Path) -> bool:
    try:
        os.symlink(target, link, target_is_directory=True)
        return True
    except (OSError, NotImplementedError):
        pass
    if os.name == "nt":   # a junction needs no privilege
        done = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                              capture_output=True, text=True)
        return done.returncode == 0
    return False


def test_a_to_browser_link_into_the_agent_bound_folder_is_refused(world):
    root = world["tmp"] / "linked-root"
    root.mkdir()
    if not _link(root / "to-browser", world["agent"]):
        pytest.skip("cannot create a symlink or junction here")
    proc = _run(world, root=root)
    assert proc.returncode not in (0, 2)
    assert _files(world["agent"]) == []


def test_a_to_browser_link_into_downloads_is_refused(world, monkeypatch):
    root = world["tmp"] / "linked-root"
    root.mkdir()
    if not _link(root / "to-browser", world["downloads"]):
        pytest.skip("cannot create a symlink or junction here")
    tr = _mod("transport_report")
    monkeypatch.setattr(Path, "home", staticmethod(lambda: world["home"]))  # Downloads is judged vs home
    with pytest.raises(tr.TransportRefused):
        tr.resolve_transport(str(root))
    assert _files(world["downloads"]) == []


# --- 3. an unmounted destination is loud and harmless -------------------------------------------

def test_unmounted_destination_is_a_nonzero_receipt_with_no_claim_of_delivery(world):
    gone = world["tmp"] / "drive-not-mounted"
    proc = _run(world, root=gone)
    assert proc.returncode != 0
    res = _result(proc)
    assert res["delivered"] is False and res["verified"] is False
    assert res["exit_code"] == proc.returncode
    assert res["reason"]
    assert not gone.exists()                       # nothing was created to "make it work"


def test_unmounted_destination_never_falls_back_to_downloads(world):
    gone = world["tmp"] / "drive-not-mounted"
    proc = _run(world, root=gone)
    assert proc.returncode != 0
    assert _files(world["downloads"]) == []
    stray = [p for p in world["tmp"].rglob("LANE-END-*") if p.is_file()]
    assert stray == []


def test_a_root_that_exists_but_has_no_browser_folder_is_refused_not_created(world):
    bare = world["tmp"] / "bare-root"
    bare.mkdir()
    proc = _run(world, root=bare)
    assert proc.returncode != 0
    assert not (bare / "to-browser").exists()


def test_resolving_the_transport_never_returns_downloads():
    tr = _mod("transport_report")
    with pytest.raises(tr.TransportRefused):
        tr.resolve_transport(environ={}, user_scope=lambda _n: None)
    with pytest.raises(tr.TransportRefused):
        tr.resolve_transport(environ={"CLAUDE_PROMPTS_DIR": str(Path.home() / "Downloads")},
                             user_scope=lambda _n: None)


def test_user_scope_wins_over_a_stale_process_value(tmp_path):
    tr = _mod("transport_report")
    real = tmp_path / "real"
    (real / "to-browser").mkdir(parents=True)
    got = tr.resolve_transport(environ={"CLAUDE_PROMPTS_DIR": str(tmp_path / "stale")},
                               user_scope=lambda _n: str(real))
    assert got == real / "to-browser"


def test_the_refusal_never_exits_with_the_stop_hooks_blocking_code(world):
    """Exit 2 from a Stop hook forces the session to continue. A refusal must be non-zero (so the
    receipt shows it) and must not be 2 (so it can never steer the lane)."""
    proc = _run(world, root=world["tmp"] / "drive-not-mounted")
    assert proc.returncode not in (0, 2)


def test_a_bad_lane_name_is_refused_without_writing_outside_the_folder(world):
    proc = _run(world, lane="..\\..\\evil")
    assert proc.returncode not in (0, 2)
    assert _files(world["browser"]) == []
    assert not (world["root"].parent / "evil").exists()


def test_bad_arguments_do_not_exit_2(world):
    proc = subprocess.run([sys.executable, str(_REPORT), "--no-such-flag"], capture_output=True,
                          text=True, timeout=60)
    assert proc.returncode not in (0, 2)


def test_an_unexpected_error_is_a_recorded_failure_not_a_traceback_or_a_block(world, monkeypatch, capsys):
    tr = _mod("transport_report")

    def boom(*_a, **_k):
        raise RuntimeError("synthetic")

    monkeypatch.setattr(tr, "build_report", boom)
    code = tr.main(["--lane", LANE, "--transport-root", str(world["root"]),
                    "--receipts-dir", str(world["receipts"]), "--repo", str(world["tmp"])])
    assert code not in (0, 2)
    res = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert res["delivered"] is False and "synthetic" in res["reason"]
