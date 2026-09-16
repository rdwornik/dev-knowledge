"""`[#808]` -- every hook carries a bounded execution time and fails OPEN past it, loudly.

THE PREMISE THESE TESTS STAND ON WAS MEASURED, NOT ASSUMED (lane ab-808 step 1, recorded in
`docs/audits/2026-09-16-technical-lane-ab-808-guard-timeout.md`). Claude Code's own hook
`timeout` DOES fire while the hook's top process is alive: it kills that process tree, the tool
call proceeds, and the transcript gains a `hook_cancelled` attachment. It does NOT fire once the
top process has EXITED while a descendant still holds the inherited stdout/stderr pipe: the
harness then waits for the pipe to close, past the bound, with no attachment at all -- the
signature of both real wedges found in the transcripts (20 h and 5.7 h, no hook record).

So the wrapper under test is not a rival timer. It closes the one gap the harness timer
structurally cannot: a wrapped command's descendants inherit the WRAPPER's pipes, never the
harness's, and the wrapper stops waiting at its bound whatever they do.

The harness is stood in for by `_run_like_harness`: payload on stdin, both streams piped, and a
wait for EOF on both -- which is the behaviour the measurement pinned. Exit 0 means the tool
call proceeds; exit 2 means a PreToolUse hook refused it.

Every test drives the module as a subprocess, the way a hook runs it, and points the record at
`tmp_path` through `DEV_KNOWLEDGE_HOOK_BYPASS_LOG` so no case writes into the real `logs/`.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_WRAPPER = _REPO_ROOT / "scripts" / "hooks" / "bounded_hook.py"
_SETTINGS = _REPO_ROOT / ".claude" / "settings.json"
_LOG_ENV = "DEV_KNOWLEDGE_HOOK_BYPASS_LOG"

_PAYLOAD = {"session_id": "sess-808-witness", "hook_event_name": "PreToolUse",
            "tool_name": "Bash", "tool_input": {"command": "echo hi"}}


def _load_wrapper():
    spec = importlib.util.spec_from_file_location("bounded_hook_under_test", _WRAPPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _env(log_path: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k != _LOG_ENV}
    env[_LOG_ENV] = str(log_path)
    return env


def _run_like_harness(argv, log_path, payload=None, wait_s=60):
    """Payload on stdin, both streams piped, wait for EOF on both -- the harness's shape."""
    started = time.monotonic()
    proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, env=_env(log_path), cwd=str(_REPO_ROOT))
    out, err = proc.communicate(json.dumps(payload or _PAYLOAD).encode("utf-8"), timeout=wait_s)
    return proc.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace"), \
        time.monotonic() - started


def _records(log_path: Path) -> list[dict]:
    if not log_path.exists():
        return []
    return [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def _script(tmp_path: Path, name: str, body: str) -> Path:
    path = tmp_path / name
    path.write_text(textwrap.dedent(body), encoding="utf-8")
    return path


def _kill_pid_file(pid_file: Path) -> None:
    """No leftovers: a stand-in descendant is killed whatever the test's verdict."""
    if not pid_file.exists():
        return
    pid = int(pid_file.read_text(encoding="utf-8").strip())
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)
    else:
        try:
            os.kill(pid, 9)
        except OSError:
            pass


# --- Done-contract 1: a guard that sleeps past its bound is BYPASSED and RECORDED ------------

def test_a_guard_that_sleeps_past_its_bound_is_bypassed_and_the_bypass_is_recorded(tmp_path):
    """The refusal-shaped witness: this stand-in would REFUSE (exit 2) if it were ever allowed
    to finish. Past its bound it must not be -- the tool call proceeds (exit 0), and the bypass
    lands on the named surface carrying hook id, bound, elapsed time and session id. A silent
    pass fails this test as surely as a wedge does."""
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    guard = _script(tmp_path, "sleeper.py", """
        import time, sys
        time.sleep(30)
        print("refused", file=sys.stderr)
        sys.exit(2)
    """)

    rc, out, err, elapsed = _run_like_harness(
        [sys.executable, str(_WRAPPER), "run", "--id", "test-sleeper", "--bound", "2",
         "--", sys.executable, str(guard)], log)

    assert rc == 0, (rc, out, err)
    assert elapsed < 20, f"the wrapper outlived its bound: {elapsed:.1f}s"
    records = _records(log)
    assert len(records) == 1, records
    record = records[0]
    assert record["hook_id"] == "test-sleeper"
    assert record["bound_s"] == 2
    assert record["elapsed_s"] >= 2
    assert record["session_id"] == "sess-808-witness"
    assert record["reason"] == "timeout"
    assert record["posture"] == "fail-open"
    # LOUD, in-band: the seat is told which guard was skipped, not left to infer it.
    assert "test-sleeper" in out + err


def test_a_descendant_holding_the_pipe_cannot_hold_the_seat_past_the_bound(tmp_path):
    """The measured wedge mechanism. The guard exits at once, leaving a child that inherited its
    stdout and sleeps. Unwrapped, a harness waiting for EOF waits for that child (the control
    leg proves the stand-in reproduces it); wrapped, the wait ends at the bound and is recorded."""
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    pid_file = tmp_path / "descendant.pid"
    guard = _script(tmp_path, "spawner.py", f"""
        import subprocess, sys
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(12)"])
        open({str(pid_file)!r}, "w").write(str(child.pid))
        sys.exit(0)
    """)
    try:
        rc, _, _, unwrapped = _run_like_harness([sys.executable, str(guard)], log)
        assert rc == 0
        assert unwrapped >= 8, f"control leg did not reproduce the held pipe: {unwrapped:.1f}s"
    finally:
        _kill_pid_file(pid_file)
        pid_file.unlink(missing_ok=True)

    try:
        rc, out, err, wrapped = _run_like_harness(
            [sys.executable, str(_WRAPPER), "run", "--id", "test-spawner", "--bound", "3",
             "--", sys.executable, str(guard)], log)
    finally:
        _kill_pid_file(pid_file)

    assert rc == 0, (rc, out, err)
    assert wrapped < 8, f"the held pipe still held the seat: {wrapped:.1f}s"
    records = _records(log)
    assert [r["hook_id"] for r in records] == ["test-spawner"]
    assert records[0]["reason"] == "pipe-held-after-exit"
    assert records[0]["session_id"] == "sess-808-witness"


def test_a_guard_within_its_bound_is_relayed_verbatim_and_records_nothing(tmp_path):
    """The wrapper must cost a working guard nothing: its exit code and both streams pass
    through byte-for-byte -- a refusal stays a refusal -- and no bypass is written."""
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    guard = _script(tmp_path, "refuser.py", """
        import sys
        payload = sys.stdin.read()
        sys.stdout.write("OUT:" + str(len(payload)))
        sys.stderr.write("refused by policy")
        sys.exit(2)
    """)

    rc, out, err, _ = _run_like_harness(
        [sys.executable, str(_WRAPPER), "run", "--id", "test-refuser", "--bound", "20",
         "--", sys.executable, str(guard)], log)

    assert rc == 2
    assert out == "OUT:" + str(len(json.dumps(_PAYLOAD)))
    assert err == "refused by policy"
    assert _records(log) == []


# --- Done-contract 2: every registered hook carries an explicit bound, and a check refuses ----

def test_the_check_refuses_a_hook_registration_without_an_explicit_bound(tmp_path):
    settings = tmp_path / "settings.json"
    settings.write_text(json.dumps({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
        {"type": "command", "command": "python unbounded_guard.py"}]}]}}), encoding="utf-8")

    res = subprocess.run([sys.executable, str(_WRAPPER), "check", "--settings", str(settings)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")

    assert res.returncode == 1, res.stdout + res.stderr
    assert "unbounded_guard.py" in res.stdout + res.stderr
    assert "timeout" in res.stdout + res.stderr


def test_the_check_refuses_a_wrapper_bound_the_harness_timeout_does_not_cover(tmp_path):
    """The wrapper's bound is measured from the wrapper's own start, and interpreter startup on a
    loaded box was measured at up to ~20 s. A harness timeout with no headroom over the bound
    cancels the wrapper before it can write the record -- a silent bypass again."""
    settings = tmp_path / "settings.json"
    command = 'python "scripts/hooks/bounded_hook.py" run --id tight --bound 10 -- python x.py'
    settings.write_text(json.dumps({"hooks": {"SessionStart": [{"matcher": "", "hooks": [
        {"type": "command", "command": command, "timeout": 12}]}]}}), encoding="utf-8")

    res = subprocess.run([sys.executable, str(_WRAPPER), "check", "--settings", str(settings)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")

    assert res.returncode == 1, res.stdout + res.stderr
    assert "tight" in res.stdout + res.stderr


def test_the_live_settings_pass_the_check():
    res = subprocess.run([sys.executable, str(_WRAPPER), "check", "--settings", str(_SETTINGS)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert res.returncode == 0, res.stdout + res.stderr


# --- Done-contract 3: the record is surfaced at SessionStart ---------------------------------

def test_the_surface_names_each_guard_that_timed_out(tmp_path):
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rows = [{"ts": now, "hook_id": "slow-guard", "bound_s": 10, "elapsed_s": 10.4,
             "session_id": f"s{i}", "reason": "timeout", "posture": "fail-open"} for i in range(3)]
    log.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")

    res = subprocess.run([sys.executable, str(_WRAPPER), "surface"], capture_output=True,
                         text=True, encoding="utf-8", errors="replace", env=_env(log))

    assert res.returncode == 0
    assert "slow-guard" in res.stdout
    assert "3" in res.stdout


def test_the_surface_is_silent_and_green_with_no_record(tmp_path):
    res = subprocess.run([sys.executable, str(_WRAPPER), "surface"], capture_output=True,
                         text=True, encoding="utf-8", errors="replace",
                         env=_env(tmp_path / "absent.jsonl"))
    assert res.returncode == 0
    assert res.stdout.strip() == ""


def test_the_surface_is_wired_at_session_start():
    settings = json.loads(_SETTINGS.read_text(encoding="utf-8"))
    commands = [h["command"] for block in settings["hooks"]["SessionStart"]
                for h in block["hooks"]]
    assert any("bounded_hook.py" in c and " surface" in c for c in commands), commands


# --- Done-contract 4: the posture is stated per hook, with its reason --------------------------

def test_every_registered_hook_has_a_stated_posture_with_a_reason():
    module = _load_wrapper()
    settings = json.loads(_SETTINGS.read_text(encoding="utf-8"))
    for event, blocks in settings["hooks"].items():
        for block in blocks:
            for hook in block["hooks"]:
                posture = module.posture_for(hook["command"])
                assert posture is not None, f"{event}: no stated posture for {hook['command'][:80]}"
                assert posture.reason.strip(), posture.hook_id


def test_a_hook_that_must_fail_closed_is_named_as_escalated_never_wrapped_open():
    """`[#808]` Done 4: a guard whose ruling says fail CLOSED is NAMED and escalated, never
    decided by default. Wrapping it fail-open would decide it; so an escalated hook must not
    route through the wrapper at all until a ruling says which way it goes."""
    module = _load_wrapper()
    escalated = [p for p in module.POSTURES if p.posture == "escalated"]
    assert escalated, "no hook is named as escalated -- the fail-CLOSED guards were decided silently"
    settings = json.loads(_SETTINGS.read_text(encoding="utf-8"))
    for blocks in settings["hooks"].values():
        for block in blocks:
            for hook in block["hooks"]:
                posture = module.posture_for(hook["command"])
                if posture.posture == "escalated":
                    assert "bounded_hook.py" not in hook["command"], posture.hook_id


def test_the_record_resolves_to_the_primary_checkout_from_a_lane_worktree(tmp_path):
    """A lane's worktree is torn down at integration; a bypass recorded inside it would be
    destroyed with it. The record therefore lives under the PRIMARY checkout's `logs/`."""
    module = _load_wrapper()
    primary = tmp_path / "primary"
    lane = primary / ".claude" / "worktrees" / "lane-x"
    (primary / ".git" / "worktrees" / "lane-x").mkdir(parents=True)
    lane.mkdir(parents=True)
    (lane / ".git").write_text(f"gitdir: {primary / '.git' / 'worktrees' / 'lane-x'}\n",
                               encoding="utf-8")

    assert module.primary_root(lane) == primary
    assert module.primary_root(primary) == primary


@pytest.mark.parametrize("posture", ["closed"])
def test_a_closed_posture_refuses_past_the_bound_and_still_records(tmp_path, posture):
    """The switch a ruling needs, built so that either answer is one flag: `--posture closed`
    refuses (exit 2) with a teaching message and the same record. Nothing is wired closed."""
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    guard = _script(tmp_path, "sleeper.py", "import time; time.sleep(30)\n")

    rc, out, err, elapsed = _run_like_harness(
        [sys.executable, str(_WRAPPER), "run", "--id", "test-closed", "--bound", "2",
         "--posture", posture, "--", sys.executable, str(guard)], log)

    assert rc == 2
    assert elapsed < 20
    assert "test-closed" in err
    assert [r["posture"] for r in _records(log)] == ["fail-closed"]
