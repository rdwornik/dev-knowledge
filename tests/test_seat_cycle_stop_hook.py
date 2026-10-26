"""RED-first witnesses for the seat-cycle Stop leg ([#1636]): the Stop hook runs the threshold
check for orchestrator/integrator seats only, records CROSSED in the seat state file and the
receipt, never blocks or asks the model to continue, and the state/digest carry
cycles / max_context / compactions."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
for p in (REPO_ROOT, SCRIPTS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import lane_digest as ld  # noqa: E402
import seat_cycle as sc  # noqa: E402
import seat_registry as sr  # noqa: E402
import seat_state as ss  # noqa: E402

@pytest.fixture(autouse=True)
def _no_real_transport(tmp_path, monkeypatch):
    """The state lookup also tries $CLAUDE_PROMPTS_DIR/to-browser: never the operator's real one."""
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(tmp_path / "no-such-transport"))
    monkeypatch.setattr(ss, "_user_env", lambda name: None, raising=False)   # the User-scope registry copy
    import importlib
    monkeypatch.setattr(importlib.import_module("scripts.seat_state"), "_user_env",    # lane_digest's copy
                        lambda name: None, raising=False)


NOW = datetime(2026, 10, 25, 12, 0, tzinfo=timezone.utc)
CONFIG = {"threshold": {"orchestrator": {"context_tokens": 1000, "max_age_hours": 3.0},
                        "integrator": {"context_tokens": 1000, "max_age_hours": 3.0}}}


def _transcript(path: Path, tokens: int, compactions: int = 0) -> Path:
    rows = [{"type": "user", "isCompactSummary": True} for _ in range(compactions)]
    rows.append({"type": "assistant", "message": {"usage": {"input_tokens": tokens}}})
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


def _bind(reg: Path, role: str, session: str = "sess-1", age_h: float = 0.1) -> None:
    sr.bind(role, "B9", session_id=session, path=reg, now=NOW - timedelta(hours=age_h))


def _state(root: Path, role: str = "integrator") -> Path:
    path = root / "to-browser" / ("STATE-b9.json" if role == "integrator" else "STATE-b9-dispatcher.json")
    ss.write_state(path, role=role, batch="B9", base_sha="abc123",
                   lanes={"l1": {"state": "QUEUED", "evidence": {"session_file": "to-browser/S.md"}}},
                   now=NOW.isoformat(timespec="seconds"))
    return path


def _run(tmp_path, role, tokens, *, bind_role=None, session="sess-1", age_h=0.1, compactions=0):
    reg = tmp_path / "registry.jsonl"
    if bind_role != "none":
        _bind(reg, bind_role or role, session, age_h)
    transcript = _transcript(tmp_path / "t.jsonl", tokens, compactions)
    payload = {"hook_event_name": "Stop", "session_id": session, "transcript_path": str(transcript)}
    return sc.stop_check(payload, registry_path=reg, repo_root=tmp_path, config=CONFIG, now=NOW)


def test_unbound_or_other_role_is_a_noop(tmp_path):
    state = _state(tmp_path)
    before = state.read_text(encoding="utf-8")
    assert _run(tmp_path, "integrator", 99999, bind_role="none") is None
    assert _run(tmp_path, "lane", 99999, bind_role="lane") is None
    assert _run(tmp_path, "browser", 99999, bind_role="browser") is None
    assert state.read_text(encoding="utf-8") == before
    assert not (tmp_path / "to-browser" / "SESSION-integrator-b9.md").exists()


def test_below_threshold_writes_no_crossed(tmp_path):
    state = _state(tmp_path)
    assert _run(tmp_path, "integrator", 500) == "OK"
    data = json.loads(state.read_text(encoding="utf-8"))
    assert data["max_context"] == 500 and data["cycles"] == 0 and not data.get("crossed")
    assert not (tmp_path / "to-browser" / "SESSION-integrator-b9.md").exists()


@pytest.mark.parametrize("role,state_name,receipt", [
    ("integrator", "STATE-b9.json", "SESSION-integrator-b9.md"),
    ("dispatcher", "STATE-b9-dispatcher.json", "SESSION-dispatcher-b9.md"),
])
def test_crossed_is_recorded_in_state_and_receipt(tmp_path, role, state_name, receipt):
    _state(tmp_path, role)
    assert _run(tmp_path, role, 5000, compactions=2) == "CROSSED"
    data = json.loads((tmp_path / "to-browser" / state_name).read_text(encoding="utf-8"))
    assert data["cycles"] == 1 and data["max_context"] == 5000 and data["compactions"] == 2
    assert data["crossed"][0].startswith("CROSSED ") and "sess-1" in data["crossed"][0]
    line = [ln for ln in (tmp_path / "to-browser" / receipt).read_text(encoding="utf-8").splitlines()
            if ln.startswith("CROSSED ")]
    assert len(line) == 1 and "tokens=5000" in line[0]


def test_age_alone_crosses(tmp_path):
    _state(tmp_path)
    assert _run(tmp_path, "integrator", 10, age_h=4.0) == "CROSSED"


def test_repeated_stops_record_one_crossed_per_session(tmp_path):
    _state(tmp_path)
    _run(tmp_path, "integrator", 5000)
    _run(tmp_path, "integrator", 6000)
    data = json.loads((tmp_path / "to-browser" / "STATE-b9.json").read_text(encoding="utf-8"))
    assert data["cycles"] == 1 and len(data["crossed"]) == 1 and data["max_context"] == 6000
    receipt = (tmp_path / "to-browser" / "SESSION-integrator-b9.md").read_text(encoding="utf-8")
    assert receipt.count("CROSSED ") == 1


def test_a_missing_state_file_is_not_fabricated_and_writes_no_receipt(tmp_path):
    """Repair 2 (c): no state file -> no CROSSED line anywhere, no receipt write."""
    assert _run(tmp_path, "integrator", 5000) == "CROSSED"
    assert not (tmp_path / "to-browser" / "STATE-b9.json").exists()
    assert not (tmp_path / "to-browser" / "SESSION-integrator-b9.md").exists()


def test_hook_never_blocks_or_continues(tmp_path):
    """Black box: the Stop hook prints nothing on stdout (no decision/additionalContext), exit 0."""
    reg_home = tmp_path / "home"
    (reg_home / ".claude").mkdir(parents=True)
    # a batch name no real transport holds: the child reads the User-scope $CLAUDE_PROMPTS_DIR first
    state_path = tmp_path / "to-browser" / "STATE-zzhook.json"
    ss.write_state(state_path, role="integrator", batch="ZZHOOK", base_sha="abc123",
                   lanes={"l1": {"state": "QUEUED", "evidence": {"session_file": "to-browser/S.md"}}})
    transcript = _transcript(tmp_path / "t.jsonl", 999999)   # over the real 300000 threshold
    reg = reg_home / ".claude" / "seat-registry.jsonl"
    sr.bind("integrator", "ZZHOOK", session_id="sess-1", path=reg, now=NOW - timedelta(hours=0.1))
    env = {**os.environ, "HOME": str(reg_home), "USERPROFILE": str(reg_home),
           "SEAT_CYCLE_REPO_ROOT": str(tmp_path)}
    env.pop("CLAUDE_CODE_SESSION_ATTENDED", None)   # the unrelated hygiene nudge stays silent
    payload = {"hook_event_name": "Stop", "session_id": "sess-1", "stop_hook_active": False,
               "transcript_path": str(transcript), "cwd": str(tmp_path)}
    done = subprocess.run([sys.executable, str(SCRIPTS / "session_end_backpressure.py")],
                          input=json.dumps(payload), capture_output=True, text=True, env=env,
                          cwd=str(tmp_path), timeout=15)
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == ""
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["cycles"] == 1, done.stderr          # ... and yet the CROSSED was recorded


# --- state fields -----------------------------------------------------------------------------

def test_new_fields_round_trip(tmp_path):
    path = tmp_path / "S.json"
    ss.write_state(path, role="integrator", batch="B9", base_sha="abc", lanes={},
                   cycles=2, max_context=250000, compactions=1)
    state = ss.read_state(path, now=datetime.now(timezone.utc))
    assert (state.cycles, state.max_context, state.compactions) == (2, 250000, 1)


def test_old_state_file_without_the_fields_still_reads(tmp_path):
    path = tmp_path / "S.json"
    ss.write_state(path, role="integrator", batch="B9", base_sha="abc", lanes={})
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("cycles", "max_context", "compactions", "crossed"):
        data.pop(key, None)
    path.write_text(json.dumps(data), encoding="utf-8")
    state = ss.read_state(path)
    assert (state.cycles, state.max_context, state.compactions) == (0, 0, 0)


def test_rewriting_state_by_hand_keeps_the_hook_counters(tmp_path):
    path = _state(tmp_path)
    _run(tmp_path, "integrator", 5000, compactions=1)
    ss.write_state(path, role="integrator", batch="B9", base_sha="abc", lanes={})
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["cycles"] == 1 and data["max_context"] == 5000 and data["compactions"] == 1


# --- digest -------------------------------------------------------------------------------------

def test_digest_prints_cycles_max_context_compactions(tmp_path):
    path = tmp_path / "S.json"
    ss.write_state(path, role="integrator", batch="B9", base_sha="abc", lanes={},
                   cycles=3, max_context=412000, compactions=0)
    text = ld.render_digest([], seat_states=[ss.load_counters(path)])
    assert "cycles 3" in text and "max context 412000" in text and "compactions 0" in text
    assert "target 0" in text


def test_digest_without_seat_states_is_unchanged():
    assert "cycles" not in ld.render_digest([])


# --- repair 2: the five HIGH findings -------------------------------------------------------------

def test_hook_from_a_subdirectory_writes_to_the_repo_root(tmp_path):
    """(b) state and receipt follow the repo root, not the hook's cwd."""
    (tmp_path / ".git").mkdir()
    sub = tmp_path / "scripts" / "deep"
    sub.mkdir(parents=True)
    path = _state(tmp_path)
    reg = tmp_path / "registry.jsonl"
    _bind(reg, "integrator")
    payload = {"hook_event_name": "Stop", "session_id": "sess-1", "cwd": str(sub),
               "transcript_path": str(_transcript(tmp_path / "t.jsonl", 5000))}
    assert sc.stop_check(payload, registry_path=reg, config=CONFIG, now=NOW) == "CROSSED"
    assert json.loads(path.read_text(encoding="utf-8"))["cycles"] == 1
    assert (tmp_path / "to-browser" / "SESSION-integrator-b9.md").exists()
    assert not (sub / "to-browser").exists()


def test_hook_without_seat_registry_is_a_silent_noop(tmp_path):
    """(a) a consumer repo has no hub-only `seat_registry`: the standalone hook still exits 0, silently."""
    import shutil
    lone = tmp_path / "lone"
    lone.mkdir()
    shutil.copy(SCRIPTS / "session_end_backpressure.py", lone / "session_end_backpressure.py")
    env = {**os.environ, "HOME": str(tmp_path), "USERPROFILE": str(tmp_path)}
    env.pop("CLAUDE_CODE_SESSION_ATTENDED", None)
    env.pop("PYTHONPATH", None)
    payload = {"hook_event_name": "Stop", "session_id": "sess-1", "cwd": str(lone),
               "transcript_path": str(tmp_path / "t.jsonl")}
    done = subprocess.run([sys.executable, str(lone / "session_end_backpressure.py")],
                          input=json.dumps(payload), capture_output=True, text=True, env=env,
                          cwd=str(lone), timeout=15)
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == ""
    assert "DEGRADED" not in done.stderr, done.stderr


def test_concurrent_write_state_and_hook_update_lose_nothing(tmp_path, monkeypatch):
    """(d) read-merge-write is atomic: a hook update that lands while a by-hand rewrite is between
    its read and its write survives, and so does the rewrite."""
    import threading
    import time
    path = _state(tmp_path)
    real = ss._read_counters

    def slow(p):
        out = real(p)
        time.sleep(0.3)           # widen the read -> write window of whichever writer is in it
        return out

    monkeypatch.setattr(ss, "_read_counters", slow)
    errors = []

    def rewrite():
        try:
            ss.write_state(path, role="integrator", batch="B9", base_sha="abc",
                           lanes={"l2": {"state": "QUEUED", "evidence": {"session_file": "S.md"}}},
                           written_by="by-hand")
        except Exception as exc:                      # noqa: BLE001
            errors.append(exc)

    def hook():
        try:
            time.sleep(0.1)
            ss.update_counters(path, max_context=9, compactions=4)
        except Exception as exc:                      # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=rewrite), threading.Thread(target=hook)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert not errors, errors
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["written_by"] == "by-hand" and "l2" in data["lanes"]      # the rewrite survived
    assert data["compactions"] == 4 and data["max_context"] == 9          # ... and so did the hook


def test_batch_close_digest_prints_seat_cycles_without_a_flag(tmp_path, capsys):
    """(e) the batch-close row passes no --seat-state; the digest finds the batch's STATE files itself."""
    path = tmp_path / "to-browser" / "STATE-b9.json"
    ss.write_state(path, role="integrator", batch="B9", base_sha="abc", lanes={},
                   cycles=2, max_context=412000, compactions=0)
    other = tmp_path / "to-browser" / "STATE-b8.json"
    ss.write_state(other, role="integrator", batch="B8", base_sha="abc", lanes={}, cycles=7)
    rc = ld.main(["--lane", "B9", "--repo", str(tmp_path), "--receipts-dir", str(tmp_path / "r"),
                  "--costs-file", str(tmp_path / "none.jsonl")])
    out = capsys.readouterr().out
    assert rc == 0
    assert "cycles 2" in out and "max context 412000" in out and "(target 0)" in out
    assert "cycles 7" not in out


# --- repair 2, second round: findings from the re-review of the fix tip ------------------------------

def test_concurrent_hooks_append_one_crossed_per_session(tmp_path, monkeypatch):
    """Receipt dedupe is read-then-append: two Stop processes for one session must not both append."""
    import threading
    import time
    _state(tmp_path)
    reg = tmp_path / "registry.jsonl"
    _bind(reg, "integrator")
    payload = {"hook_event_name": "Stop", "session_id": "sess-1",
               "transcript_path": str(_transcript(tmp_path / "t.jsonl", 5000))}
    real = Path.exists

    def slow(self):
        out = real(self)
        if self.name.startswith("SESSION-"):
            time.sleep(0.3)          # widen the check -> append window of the receipt dedupe
        return out

    monkeypatch.setattr(Path, "exists", slow)
    threads = [threading.Thread(target=sc.stop_check, args=(payload,),
                                kwargs=dict(registry_path=reg, repo_root=tmp_path, config=CONFIG, now=NOW))
               for _ in range(2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    monkeypatch.undo()
    receipt = (tmp_path / "to-browser" / "SESSION-integrator-b9.md").read_text(encoding="utf-8")
    assert receipt.count("CROSSED seat=sess-1 ") == 1


def test_state_file_on_the_transport_is_found_and_recorded(tmp_path, monkeypatch):
    """The seat templates' `to-browser/` is the transport; a state file there (none in the checkout) counts."""
    prompts = tmp_path / "prompts"
    (prompts / "to-browser").mkdir(parents=True)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(prompts))
    path = _state(prompts, "integrator")
    checkout = tmp_path / "checkout"
    (checkout / ".git").mkdir(parents=True)
    reg = tmp_path / "registry.jsonl"
    _bind(reg, "integrator")
    payload = {"hook_event_name": "Stop", "session_id": "sess-1",
               "transcript_path": str(_transcript(tmp_path / "t.jsonl", 5000))}
    assert sc.stop_check(payload, registry_path=reg, repo_root=checkout, config=CONFIG, now=NOW) == "CROSSED"
    assert json.loads(path.read_text(encoding="utf-8"))["cycles"] == 1
    assert "CROSSED seat=sess-1" in (prompts / "to-browser" / "SESSION-integrator-b9.md").read_text(encoding="utf-8")
    assert not (checkout / "to-browser").exists()


def test_batch_close_digest_reads_state_files_on_the_transport(tmp_path, monkeypatch, capsys):
    prompts = tmp_path / "prompts"
    (prompts / "to-browser").mkdir(parents=True)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(prompts))
    ss.write_state(prompts / "to-browser" / "STATE-b9.json", role="integrator", batch="B9",
                   base_sha="abc", lanes={}, cycles=3, max_context=300001, compactions=0)
    rc = ld.main(["--lane", "B9", "--repo", str(tmp_path), "--receipts-dir", str(tmp_path / "r"),
                  "--costs-file", str(tmp_path / "none.jsonl")])
    out = capsys.readouterr().out
    assert rc == 0 and "cycles 3" in out and "max context 300001" in out


# --- repair 2, third round --------------------------------------------------------------------------

def test_transport_state_file_wins_over_a_stale_checkout_copy(tmp_path, monkeypatch):
    prompts = tmp_path / "prompts"
    (prompts / "to-browser").mkdir(parents=True)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(prompts))
    live = _state(prompts, "integrator")
    stale = _state(tmp_path / "checkout", "integrator")
    reg = tmp_path / "registry.jsonl"
    _bind(reg, "integrator")
    payload = {"hook_event_name": "Stop", "session_id": "sess-1",
               "transcript_path": str(_transcript(tmp_path / "t.jsonl", 5000))}
    sc.stop_check(payload, registry_path=reg, repo_root=tmp_path / "checkout", config=CONFIG, now=NOW)
    assert json.loads(live.read_text(encoding="utf-8"))["cycles"] == 1
    assert json.loads(stale.read_text(encoding="utf-8"))["cycles"] == 0


def test_a_linked_worktree_finds_the_primary_checkouts_state(tmp_path):
    primary = tmp_path / "primary"
    (primary / ".git" / "worktrees" / "wt").mkdir(parents=True)
    wt = tmp_path / "wt"
    wt.mkdir()
    (wt / ".git").write_text(f"gitdir: {(primary / '.git' / 'worktrees' / 'wt').as_posix()}\n", encoding="utf-8")
    path = _state(primary, "integrator")
    reg = tmp_path / "registry.jsonl"
    _bind(reg, "integrator")
    payload = {"hook_event_name": "Stop", "session_id": "sess-1", "cwd": str(wt),
               "transcript_path": str(_transcript(tmp_path / "t.jsonl", 5000))}
    assert sc.stop_check(payload, registry_path=reg, config=CONFIG, now=NOW) == "CROSSED"
    assert json.loads(path.read_text(encoding="utf-8"))["cycles"] == 1


def test_compactions_add_up_across_successor_sessions(tmp_path):
    path = _state(tmp_path)
    assert ss.update_counters(path, compactions=1, session="s-1")
    assert ss.update_counters(path, compactions=1, session="s-2")
    assert ss.update_counters(path, compactions=1, session="s-2") is False      # same session: a max, not a sum
    assert json.loads(path.read_text(encoding="utf-8"))["compactions"] == 2
    ss.write_state(path, role="integrator", batch="B9", base_sha="abc", lanes={})   # a by-hand rewrite keeps it
    assert json.loads(path.read_text(encoding="utf-8"))["compactions"] == 2
    assert ss.update_counters(path, compactions=2, session="s-2")
    assert json.loads(path.read_text(encoding="utf-8"))["compactions"] == 3


def test_digest_lists_one_row_per_seat_batch(tmp_path, monkeypatch, capsys):
    prompts = tmp_path / "prompts"
    (prompts / "to-browser").mkdir(parents=True)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(prompts))
    for root, n in ((prompts, 5), (tmp_path, 1)):
        ss.write_state(root / "to-browser" / "STATE-b9.json", role="integrator", batch="B9",
                       base_sha="abc", lanes={}, cycles=n)
    ld.main(["--lane", "B9", "--repo", str(tmp_path), "--receipts-dir", str(tmp_path / "r"),
             "--costs-file", str(tmp_path / "none.jsonl")])
    out = capsys.readouterr().out
    assert out.count("integrator B9: cycles") == 1 and "cycles 5" in out


def test_receipt_is_not_written_when_the_state_update_cannot_apply(tmp_path):
    path = _state(tmp_path)
    path.write_text("{ not json", encoding="utf-8")          # torn after the existence check would pass
    assert _run(tmp_path, "integrator", 5000) == "CROSSED"
    assert not (tmp_path / "to-browser" / "SESSION-integrator-b9.md").exists()


def test_transcript_is_streamed_not_read_whole(tmp_path, monkeypatch):
    t = _transcript(tmp_path / "t.jsonl", 4321, compactions=2)

    def boom(self, *a, **k):
        raise AssertionError("read_text on the transcript")

    monkeypatch.setattr(Path, "read_text", boom)
    assert sc.transcript_stats(t) == (4321, 2)


# --- repair 2, fourth round -----------------------------------------------------------------------------

def test_digest_precedence_survives_path_sort_order(tmp_path, monkeypatch, capsys):
    """A checkout path that sorts BEFORE the transport's must still lose to it."""
    checkout = tmp_path / "a-checkout"
    prompts = tmp_path / "z-prompts"
    (prompts / "to-browser").mkdir(parents=True)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(prompts))
    for root, n in ((prompts, 5), (checkout, 1)):
        ss.write_state(root / "to-browser" / "STATE-b9.json", role="integrator", batch="B9",
                       base_sha="abc", lanes={}, cycles=n)
    ld.main(["--lane", "B9", "--repo", str(checkout), "--receipts-dir", str(tmp_path / "r"),
             "--costs-file", str(tmp_path / "none.jsonl")])
    out = capsys.readouterr().out
    assert out.count("integrator B9: cycles") == 1 and "cycles 5" in out


def test_a_legacy_compaction_total_survives_the_first_session_update(tmp_path):
    path = _state(tmp_path)
    ss.write_state(path, role="integrator", batch="B9", base_sha="abc", lanes={}, compactions=2)
    assert json.loads(path.read_text(encoding="utf-8")).get("compaction_sessions", {}) == {}
    ss.update_counters(path, compactions=0, session="s-1", max_context=1)
    assert json.loads(path.read_text(encoding="utf-8"))["compactions"] == 2
    ss.update_counters(path, compactions=1, session="s-1")
    assert json.loads(path.read_text(encoding="utf-8"))["compactions"] == 3


def test_user_scope_transport_beats_a_stale_process_copy(tmp_path, monkeypatch):
    stale, live = tmp_path / "stale", tmp_path / "live"
    for d in (stale, live):
        (d / "to-browser").mkdir(parents=True)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(stale))
    monkeypatch.setattr(ss, "_user_env", lambda name: str(live), raising=False)
    assert ss.state_folders(tmp_path / "checkout")[0] == live / "to-browser"
