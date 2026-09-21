"""lane-end-hook (W3-D): the Stop hook that runs `moment:lane-end` once, when the lane has written HANDBACK.

RED-first (ADR-108 s.B, WAVE3-COMMON rules 1-4): authored and witnessed FAILING before
`scripts/lane_end_guard.py` existed. Test names carry the Done-contract's words.

The guard is a Stop-hook entry, so two facts bound it: it fires at EVERY turn end of a lane (so the
skip path must be cheap and the run path must happen once), and it can never stop the session
(DECLARE-NIGHT N3: a failure is a receipt with a non-zero exit, never exit code 2, never a `decision`
on stdout, never a killed child).

Every test drives a synthetic session file and receipts dir in `tmp_path`; nothing touches the real
transport. The declared rows are read from the real files and run as written (rule 4).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
_GUARD = _SCRIPTS / "lane_end_guard.py"
_SETTINGS = _REPO / ".claude" / "settings.json"
_HARNESS = _REPO / "ecosystem" / "harness.yaml"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

LANE = "lane-end-hook"
HANDBACK = "HANDBACK worktree-lane-end-hook @ abc1234 code"


def _guard():
    import importlib
    return importlib.import_module("lane_end_guard")


class _Runner:
    """A stand-in for the moment: records each call, returns a canned result."""

    def __init__(self, exit_code: int = 0, raises: BaseException | None = None):
        self.calls: list[list[str]] = []
        self.exit_code, self.raises = exit_code, raises

    def __call__(self, argv, cwd, log, budget_s):
        self.calls.append(list(argv))
        if self.raises:
            raise self.raises
        return _guard().MomentResult(exit_code=self.exit_code, over_budget=False, duration_ms=7)


@pytest.fixture()
def lane(tmp_path: Path) -> dict:
    session = tmp_path / "SESSION-lane-end-hook.md"
    receipts = tmp_path / "receipts"
    env = {"HARNESS_LANE": LANE, "HARNESS_SESSION_FILE": str(session), "HARNESS_RECEIPTS_DIR": str(receipts)}
    return {"session": session, "receipts": receipts, "env": env, "root": tmp_path}


def _receipt(lane: dict) -> dict | None:
    path = lane["receipts"] / "MOMENT-LANE-END-HOOK.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def _run(lane: dict, runner, **kw) -> int:
    return _guard().main([], environ=lane["env"], runner=runner, **kw)


# --- Done-contract 1: skip with no HANDBACK, run once with it ---------------------------------------

def test_guard_skips_with_no_handback_line(lane, capsys):
    lane["session"].write_text("# SESSION\n\nstill working\nHANDBACK is described here mid-line\n", encoding="utf-8")
    runner = _Runner()
    assert _run(lane, runner) == 0
    assert runner.calls == [], "no HANDBACK line: the moment must not run"
    assert _receipt(lane) is None, "a skip leaves no receipt (cheap path)"
    assert capsys.readouterr().out == ""


def test_guard_skips_when_the_session_file_is_absent(lane):
    runner = _Runner()
    assert _run(lane, runner) == 0
    assert runner.calls == [] and _receipt(lane) is None


def test_guard_skips_outside_a_lane(lane):
    lane["session"].write_text(HANDBACK + "\n", encoding="utf-8")
    env = {k: v for k, v in lane["env"].items() if k != "HARNESS_LANE"}
    runner = _Runner()
    # the primary checkout is not under .claude/worktrees, so no lane can be named from the root
    assert _guard().main([], environ=env, runner=runner, root=lane["root"]) == 0
    assert runner.calls == []


def test_guard_runs_once_with_the_handback_line(lane):
    lane["session"].write_text(f"# SESSION\n\nwork\n\n{HANDBACK}\n", encoding="utf-8")
    runner = _Runner()
    assert _run(lane, runner) == 0
    assert len(runner.calls) == 1
    assert runner.calls[0][-1] == "moment:lane-end"
    rec = _receipt(lane)
    assert rec["status"] == "ok" and rec["exit_code"] == 0
    assert rec["lane"] == LANE and rec["handback"] == HANDBACK
    assert {"guard_ms", "moment_ms", "budget_s", "finished_at"} <= set(rec)


def test_a_second_turn_end_after_completion_does_nothing(lane):
    lane["session"].write_text(HANDBACK + "\n", encoding="utf-8")
    runner = _Runner()
    assert _run(lane, runner) == 0
    first = _receipt(lane)
    assert _run(lane, runner) == 0
    assert _run(lane, runner) == 0
    assert len(runner.calls) == 1, "the receipt marks the moment done; later turn ends skip it"
    assert _receipt(lane) == first, "a skipped turn end does not rewrite the receipt"


def test_a_failed_moment_is_also_done_once(lane):
    lane["session"].write_text(HANDBACK + "\n", encoding="utf-8")
    runner = _Runner(exit_code=3)
    assert _run(lane, runner) == 0
    assert _run(lane, runner) == 0
    assert len(runner.calls) == 1, "a failure is a receipt, not a retry on every later turn end"


# --- Done-contract 2: it can never block the session ------------------------------------------------

def test_an_unmounted_transport_records_a_refusal_and_does_not_block(lane, capsys):
    """transport_report exits 3 (refused) inside the moment: the guard's receipt carries it, exit 0."""
    lane["session"].write_text(HANDBACK + "\n", encoding="utf-8")
    assert _run(lane, _Runner(exit_code=3)) == 0
    rec = _receipt(lane)
    assert rec["status"] == "FAILED" and rec["exit_code"] == 3
    assert capsys.readouterr().out == ""


def test_an_unresolvable_transport_records_a_refusal_and_does_not_block(lane, capsys):
    """No HARNESS_SESSION_FILE and no mounted transport: the HANDBACK line cannot be looked for at all."""
    from transport_report import TransportRefused

    def unmounted():
        raise TransportRefused("transport root H:\\ is not mounted or does not exist")

    env = {k: v for k, v in lane["env"].items() if k != "HARNESS_SESSION_FILE"}
    runner = _Runner()
    assert _guard().main([], environ=env, runner=runner, resolve_transport=unmounted) == 0
    assert runner.calls == []
    rec = _receipt(lane)
    assert rec["status"] == "REFUSED" and rec["exit_code"] == 3 and "not mounted" in rec["reason"]
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("boom", [RuntimeError("doit exploded"), OSError("no uv"), KeyboardInterrupt()])
def test_a_crashing_moment_is_a_receipt_never_a_blocking_exit(lane, capsys, boom):
    lane["session"].write_text(HANDBACK + "\n", encoding="utf-8")
    code = _run(lane, _Runner(raises=boom))
    assert code == 0 and code != 2, "exit 2 is a Stop hook's block-and-continue; never returned"
    rec = _receipt(lane)
    assert rec["status"] == "FAILED" and rec["exit_code"] != 0
    assert capsys.readouterr().out == "", "no `decision` JSON on stdout"


def test_a_moment_over_budget_is_left_running_not_killed(lane, tmp_path):
    """N3: nothing this builds may kill a task. The moment outlives the budget and finishes on its own."""
    lane["session"].write_text(HANDBACK + "\n", encoding="utf-8")
    marker = tmp_path / "finished.txt"
    slow = [sys.executable, "-c",
            f"import time, pathlib; time.sleep(2.5); pathlib.Path(r'{marker}').write_text('done')"]
    started = time.perf_counter()
    assert _guard().main([], environ=lane["env"], moment_argv=slow, budget_s=0.4, root=lane["root"]) == 0
    assert time.perf_counter() - started < 2.0, "the guard returned at the budget, not at the moment's end"
    rec = _receipt(lane)
    assert rec["status"] == "OVER-BUDGET" and rec["exit_code"] != 0
    deadline = time.time() + 15
    while not marker.exists() and time.time() < deadline:
        time.sleep(0.2)
    assert marker.read_text() == "done", "the moment was not killed"


def test_the_real_runner_records_a_nonzero_moment_exit(lane):
    lane["session"].write_text(HANDBACK + "\n", encoding="utf-8")
    argv = [sys.executable, "-c", "raise SystemExit(3)"]
    assert _guard().main([], environ=lane["env"], moment_argv=argv, root=lane["root"]) == 0
    rec = _receipt(lane)
    assert rec["status"] == "FAILED" and rec["exit_code"] == 3


# --- the declared rows, run as declared (rule 4) ----------------------------------------------------

def _stop_entries() -> list[dict]:
    return json.loads(_SETTINGS.read_text(encoding="utf-8"))["hooks"]["Stop"]


def _stop_commands() -> list[dict]:
    return [h for entry in _stop_entries() for h in entry["hooks"]]


def test_one_new_stop_entry_and_the_existing_one_untouched():
    cmds = _stop_commands()
    guard = [c for c in cmds if "lane_end_guard.py" in c["command"]]
    assert len(guard) == 1, "exactly one lane-end guard entry"
    backpressure = [c for c in cmds if "session_end_backpressure.py" in c["command"]]
    assert backpressure == [{"type": "command", "timeout": 15,
                             "command": 'uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/session_end_backpressure.py"'}]
    assert len(cmds) == 2, "one new entry beside the existing one; nothing else added or removed"
    assert guard[0]["timeout"] <= 15, "shares the declared 15-second limit"


def test_the_bounded_hook_wrapper_stays_unwired():
    text = _SETTINGS.read_text(encoding="utf-8")
    live = json.loads(text)["hooks"]
    assert "bounded_hook" not in json.dumps(live), "operator ruling 2026-09-17 item 1"


def test_the_guard_regex_is_the_declared_lane_end_precondition():
    doc = yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))
    moment = next(m for m in doc["moments"] if m["name"] == "lane-end")
    assert _guard().HANDBACK_PATTERN.pattern == moment["precondition"]["matches"]


def test_the_default_moment_argv_is_the_doit_lane_end_moment():
    argv = _guard().moment_argv()
    assert argv[:2] == ["uv", "run"] and "doit" in argv
    assert argv[-1] == "moment:lane-end" and "scripts/dodo.py" in argv


def test_the_declared_stop_command_skips_fast_with_no_handback(tmp_path):
    """The command exactly as settings.json declares it, run as a shell would run it."""
    cmd = next(c for c in _stop_commands() if "lane_end_guard.py" in c["command"])["command"]
    session = tmp_path / "SESSION-x.md"
    session.write_text("no closing line yet\n", encoding="utf-8")
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(_REPO), "HARNESS_LANE": "x",
           "HARNESS_SESSION_FILE": str(session), "HARNESS_RECEIPTS_DIR": str(tmp_path / "r")}
    started = time.perf_counter()
    proc = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True, timeout=30)
    elapsed = time.perf_counter() - started
    assert proc.returncode == 0 and proc.stdout == ""
    assert elapsed < 1.0, f"the skip path must be well under a second, took {elapsed:.2f}s"
    assert not (tmp_path / "r").exists(), "a skip writes nothing"


def test_the_handback_pattern_matches_only_a_closing_line():
    pat = _guard().HANDBACK_PATTERN
    assert pat.search(HANDBACK) and pat.search("x\n" + HANDBACK + "\n")
    assert not pat.search("the HANDBACK line comes last") and not pat.search("HANDBACK")
