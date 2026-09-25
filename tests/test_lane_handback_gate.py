"""lane_handback_gate.py -- the Stop hook that REFUSES to let a LANE session end without a
clean, machine-parseable closing `HANDBACK <branch> @ <sha> <kind>` line ([#1010], WAVE5B-N1
lane-handback-stop-hook).

RED-first (ADR-108 s.B): authored and witnessed FAILING before `scripts/lane_handback_gate.py`
existed. Test names carry the Done-contract's own words.

Distinct from `lane_end_guard.py` on purpose: that guard's own invariant (DECLARE-NIGHT N3,
"NEVER BLOCKS THE SESSION") is load-bearing for its own tests and must not be touched. This is
a SEPARATE Stop entry, scoped to lane sessions only, that DOES block -- via the
`{"decision":"block","reason":...}` JSON contract `session_end_backpressure.py` already
established as the live Stop-hook protocol in this Claude Code runtime (plain stdout / a bare
non-zero exit do not reach the model). Scoping the block to lanes only (never the operator's
own interactive sessions) is what keeps this safe from the ADR-85 block-cap exhaustion that
retired session_end_backpressure's own HARD leg (`scripts/session_end_backpressure.py`
module docstring) -- a lane stops rarely (completion + at most two dispatcher nudges), not on
every reply the way an interactive session does.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
_GATE = _SCRIPTS / "lane_handback_gate.py"
_SETTINGS = _REPO / ".claude" / "settings.json"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

CLEAN = "HANDBACK worktree-lane-handback-stop-hook @ abc1234 code"


def _gate():
    import importlib
    return importlib.import_module("lane_handback_gate")


# --- classify(): the pure grammar/backtick check --------------------------------------------

def test_classify_ok_on_a_clean_unwrapped_line():
    g = _gate()
    status, line = g.classify(f"# SESSION\n\nwork\n\n{CLEAN}\n")
    assert status == g.STATUS_OK and line == CLEAN


def test_classify_missing_with_no_handback_word_at_all():
    g = _gate()
    status, line = g.classify("# SESSION\n\nstill working\n")
    assert status == g.STATUS_MISSING and line is None


def test_classify_missing_with_an_empty_file():
    g = _gate()
    assert g.classify("") == (g.STATUS_MISSING, None)


def test_classify_backtick_wrapped_inline():
    g = _gate()
    status, line = g.classify(f"# SESSION\n\nthe closing line is `{CLEAN}`\n")
    assert status == g.STATUS_WRAPPED
    assert "HANDBACK" in (line or "")


def test_classify_backtick_wrapped_in_a_fenced_block():
    g = _gate()
    text = f"# SESSION\n\n```\n{CLEAN}\n```\n"
    status, _line = g.classify(text)
    assert status == g.STATUS_WRAPPED


def test_classify_wrapped_in_a_tilde_fence():
    """The library-first upgrade over a hand-rolled ``` -only toggle: CommonMark also treats
    `~~~` fences as code -- the exact class of miss `normalize_headers.py::_heading_lines`'s own
    docstring records for a naive toggle."""
    g = _gate()
    text = f"# SESSION\n\n~~~\n{CLEAN}\n~~~\n"
    status, _line = g.classify(text)
    assert status == g.STATUS_WRAPPED


def test_classify_wrapped_in_an_indented_code_block():
    g = _gate()
    text = f"# SESSION\n\n    {CLEAN}\n"
    status, _line = g.classify(text)
    assert status == g.STATUS_WRAPPED


def test_classify_malformed_missing_the_kind_field():
    g = _gate()
    status, line = g.classify("HANDBACK worktree-lane-handback-stop-hook @ abc1234\n")
    assert status == g.STATUS_MALFORMED
    assert line == "HANDBACK worktree-lane-handback-stop-hook @ abc1234"


def test_classify_malformed_the_word_appears_but_no_shape_matches():
    g = _gate()
    status, line = g.classify("the HANDBACK line goes at the very end\n")
    assert status == g.STATUS_MALFORMED and line is None


def test_classify_takes_the_last_line_the_closing_semantics():
    """An earlier bad candidate does not poison a later clean one -- `last_handback`'s own rule
    (lane_end_guard.py), applied here too."""
    g = _gate()
    text = f"`HANDBACK worktree-x @ deadbee1 code`\n\n{CLEAN}\n"
    assert g.classify(text) == (g.STATUS_OK, CLEAN)


def test_classify_a_later_wrapped_line_does_not_downgrade_an_earlier_clean_one_missing_case():
    """The scan still reports the clean line as ok even when a wrapped mention follows it --
    ok always wins once found, regardless of position."""
    g = _gate()
    text = f"{CLEAN}\n\nsee also `{CLEAN}`\n"
    status, line = g.classify(text)
    assert status == g.STATUS_OK and line == CLEAN


# --- reason(): named, directive messages -----------------------------------------------------

@pytest.mark.parametrize("status", ["missing", "backtick-wrapped", "malformed"])
def test_reason_names_the_status_and_the_session_path(status):
    g = _gate()
    msg = g.reason(status, "some line" if status != "missing" else None, "SESSION-x.md")
    assert status in msg or status.split("-")[0].upper() in msg.upper()
    assert "SESSION-x.md" in msg


def test_reason_is_empty_for_ok():
    g = _gate()
    assert g.reason(g.STATUS_OK, CLEAN, "SESSION-x.md") == ""


# --- main(): the Done-contract itself ---------------------------------------------------------

@pytest.fixture()
def lane(tmp_path: Path) -> dict:
    session = tmp_path / "SESSION-lane-handback-stop-hook.md"
    env = {"HARNESS_LANE": "lane-handback-stop-hook", "HARNESS_SESSION_FILE": str(session)}
    return {"session": session, "env": env, "root": tmp_path}


def test_a_clean_handback_line_does_not_block(lane, capsys):
    lane["session"].write_text(f"# SESSION\n\nwork\n\n{CLEAN}\n", encoding="utf-8")
    assert _gate().main([], environ=lane["env"], root=lane["root"]) == 0
    assert capsys.readouterr().out == ""


def test_a_missing_handback_line_blocks_with_a_named_reason(lane, capsys):
    lane["session"].write_text("# SESSION\n\nstill working\n", encoding="utf-8")
    assert _gate().main([], environ=lane["env"], root=lane["root"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["decision"] == "block"
    assert "missing" in out["reason"].lower()


def test_a_backtick_wrapped_handback_line_blocks_with_a_named_reason(lane, capsys):
    lane["session"].write_text(f"# SESSION\n\n`{CLEAN}`\n", encoding="utf-8")
    assert _gate().main([], environ=lane["env"], root=lane["root"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["decision"] == "block"
    assert "backtick" in out["reason"].lower()


def test_a_malformed_handback_line_blocks_with_a_named_reason(lane, capsys):
    lane["session"].write_text("HANDBACK worktree-x @ abc1234\n", encoding="utf-8")
    assert _gate().main([], environ=lane["env"], root=lane["root"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["decision"] == "block"
    assert "malformed" in out["reason"].lower()


def test_a_missing_session_file_does_not_block_never_bricks_on_infra(lane, capsys):
    """The session file cannot even be found: an environment problem, not the agent's fault --
    matches lane_end_guard.py's own posture of never blocking on infra it cannot control."""
    assert not lane["session"].exists()
    assert _gate().main([], environ=lane["env"], root=lane["root"]) == 0
    assert capsys.readouterr().out == ""


def test_a_non_lane_session_is_unaffected_even_with_no_handback_at_all(tmp_path, capsys):
    """Done-contract 2: non-lane sessions are unaffected. The primary checkout (not under
    .claude/worktrees) with no HARNESS_LANE set must never block, regardless of content."""
    session = tmp_path / "SESSION-not-a-lane.md"
    session.write_text("no handback here\n", encoding="utf-8")
    env = {"HARNESS_SESSION_FILE": str(session)}
    assert _gate().main([], environ=env, root=tmp_path) == 0
    assert capsys.readouterr().out == ""


def test_an_internal_error_never_blocks(lane, monkeypatch, capsys):
    """A broken gate must never brick a session -- fail-open on its own errors, fail-closed
    only on a genuine, positively-detected bad line (repo-wide convention, e.g.
    session_end_backpressure.py's own fail-soft posture)."""
    lane["session"].write_text("still working\n", encoding="utf-8")
    g = _gate()
    monkeypatch.setattr(g, "classify", lambda text: (_ for _ in ()).throw(RuntimeError("boom")))
    assert g.main([], environ=lane["env"], root=lane["root"]) == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "DEGRADED" in captured.err


# --- the declared rows, run as declared -------------------------------------------------------

def _stop_commands() -> list[dict]:
    data = json.loads(_SETTINGS.read_text(encoding="utf-8"))
    return [h for entry in data["hooks"]["Stop"] for h in entry["hooks"]]


def test_exactly_one_new_stop_entry_for_the_gate():
    cmds = [c for c in _stop_commands() if "lane_handback_gate.py" in c["command"]]
    assert len(cmds) == 1, cmds
    command = cmds[0]["command"]
    assert command.startswith('uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/lane_handback_gate.py"'), command
    assert command.endswith("|| true"), command
    assert cmds[0]["timeout"] <= 15


def test_three_stop_entries_total_the_two_existing_plus_this_one():
    cmds = _stop_commands()
    assert len(cmds) == 3, cmds


def test_no_powershell_in_the_new_entry():
    cmds = [c for c in _stop_commands() if "lane_handback_gate.py" in c["command"]]
    assert "powershell" not in cmds[0]["command"].lower()


# --- witness run: the real script, through a real subprocess, malformed then clean ------------

def test_witness_the_declared_stop_command_refuses_a_malformed_handback_and_passes_a_clean_one(tmp_path):
    """The Done-contract's own words: 'a witness run demonstrates the refusal on a synthetic
    malformed handback and passes on a clean one.' Runs the real script as a subprocess, exactly
    as the Stop hook invokes it (module entry point, not the test's own main() call)."""
    import os as _os

    session = tmp_path / "SESSION-lane-handback-stop-hook.md"
    env = {**_os.environ, "HARNESS_LANE": "lane-handback-stop-hook",
           "HARNESS_SESSION_FILE": str(session)}

    session.write_text("HANDBACK worktree-lane-handback-stop-hook @ abc1234\n", encoding="utf-8")
    bad = subprocess.run([sys.executable, str(_GATE)], env=env, input="", capture_output=True,
                         text=True, timeout=30)
    assert bad.returncode == 0
    out = json.loads(bad.stdout)
    assert out["decision"] == "block" and "malformed" in out["reason"].lower()

    session.write_text(f"{CLEAN}\n", encoding="utf-8")
    clean = subprocess.run([sys.executable, str(_GATE)], env=env, input="", capture_output=True,
                           text=True, timeout=30)
    assert clean.returncode == 0
    assert clean.stdout.strip() == ""
