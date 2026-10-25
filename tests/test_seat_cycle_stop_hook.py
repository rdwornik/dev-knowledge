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


def test_a_missing_state_file_is_not_fabricated(tmp_path):
    assert _run(tmp_path, "integrator", 5000) == "CROSSED"
    assert not (tmp_path / "to-browser" / "STATE-b9.json").exists()
    assert "CROSSED " in (tmp_path / "to-browser" / "SESSION-integrator-b9.md").read_text(encoding="utf-8")


def test_hook_never_blocks_or_continues(tmp_path):
    """Black box: the Stop hook prints nothing on stdout (no decision/additionalContext), exit 0."""
    reg_home = tmp_path / "home"
    (reg_home / ".claude").mkdir(parents=True)
    _state(tmp_path)
    transcript = _transcript(tmp_path / "t.jsonl", 999999)   # over the real 300000 threshold
    reg = reg_home / ".claude" / "seat-registry.jsonl"
    _bind(reg, "integrator")
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
    state = json.loads((tmp_path / "to-browser" / "STATE-b9.json").read_text(encoding="utf-8"))
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
