"""`[#863]` -- a hook process created SUSPENDED never runs a line, so no bound living inside it
can ever fire; only a watchdog reading the OS process table from OUTSIDE that process's own
tree can see it. RED-first: this module (and `scripts/hooks/hook_watchdog.py` it drives) do not
exist on `origin/main` at all, so every test here is a fresh RED there and GREEN on this tip.

THE FIXTURE IS THE REPRODUCTION (Done-item 1), not only a test aid. `_spawn_orphaned_stuck_
grandchild` constructs the `[#863]` signature directly with the SAME two-step primitive libuv
uses on Windows (`CREATE_SUSPENDED`, meant to be followed by a separate `ResumeThread` call) --
an intermediate "shell" process creates the grandchild suspended and exits WITHOUT ever
resuming it, exactly as the real incident's parent shell died between those two calls. On POSIX
there is no `CREATE_SUSPENDED` primitive, so the equivalent kernel-level stop is used instead
(`SIGSTOP`, never `SIGCONT`'d) -- a genuine platform BRANCH with two working code paths, not a
skip (`tests/test_platform_skip_ratchet.py`'s own "honest cross-platform arm" shape; the
platform-skip baseline may only shrink, so this suite adds no `skipif`/body-skip site at all).
Both arms produce the same observable signature `hook_watchdog.py` detects: a process alive,
zero CPU movement, parent already gone.

Done-item 3's OTHER witness -- `[#808]`'s timeout catching the ran-then-blocked mode -- already
exists and is not rebuilt here: `tests/test_bounded_hook.py::
test_a_guard_that_sleeps_past_its_bound_is_bypassed_and_the_bypass_is_recorded`. This module's
`test_a_process_whose_cpu_time_is_moving_is_never_a_candidate` is the negative control that
keeps the two modes apart on this side.
"""
from __future__ import annotations

import importlib.util
import json
import os
import signal
import subprocess
import sys
import textwrap
import time
import uuid
from pathlib import Path

import psutil
import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_MODULE_PATH = _REPO_ROOT / "scripts" / "hooks" / "hook_watchdog.py"


def _load_module():
    """Same shape as `test_bounded_hook.py::_load_wrapper`: a fresh module object per test file,
    never a cached `sys.modules` entry from another test."""
    hooks_dir = str(_MODULE_PATH.parent)
    if hooks_dir not in sys.path:
        sys.path.insert(0, hooks_dir)
    spec = importlib.util.spec_from_file_location("hook_watchdog_under_test", _MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hw = _load_module()

_STUCK_BODY = "import time\nwhile True:\n    time.sleep(3600)\n"
_CREATE_SUSPENDED = 0x00000004


def _unique(basename: str) -> str:
    """A per-call-unique script name. `sweep`'s candidate match is a basename SUBSTRING over
    the WHOLE system process table (the real `.claude/settings.json` convention it mirrors is
    not scoped to one directory) -- under `pytest-xdist` two workers running two tests each
    named e.g. `stuck_hook.py` at the same moment would otherwise pick up each other's fixture
    process. A unique name per call is the fix, not a narrower match: the production matcher's
    breadth is deliberate (a hook's cmdline path is not fixed across `uv run`/`python`/an
    absolute vs. relative invocation)."""
    stem, _, ext = basename.rpartition(".")
    return f"{stem}_{uuid.uuid4().hex[:12]}.{ext}"


def _settings(tmp_path: Path, script_name: str) -> Path:
    """A minimal `.claude/settings.json` naming ONE hook script -- so `sweep`'s candidate match
    is narrow to this test's own fixture process, never the live repo's real hooks."""
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"hooks": {"PreToolUse": [{"hooks": [
        {"type": "command", "command": f"uv run python \"$CLAUDE_PROJECT_DIR/{script_name}\"",
         "timeout": 15}]}]}}), encoding="utf-8")
    return path


def _spawn_orphaned_stuck_grandchild(tmp_path: Path) -> tuple[int, str]:
    """The `[#863]` signature, constructed directly rather than assumed: an intermediate
    process creates a grandchild SUSPENDED (Windows: `CREATE_SUSPENDED`; POSIX: a normal spawn
    immediately `SIGSTOP`'d) and exits WITHOUT ever completing the resume step -- the orphaning
    act itself. Returns (the grandchild's pid, its unique script basename); it stays alive,
    zero CPU, parent already gone."""
    pid_file = tmp_path / "grandchild.pid"
    script_name = _unique("stuck_hook.py")
    stuck = tmp_path / script_name
    stuck.write_text(_STUCK_BODY, encoding="utf-8")
    shell = tmp_path / "shell.py"
    if os.name == "nt":
        shell.write_text(textwrap.dedent(f"""
            import subprocess, sys
            child = subprocess.Popen([sys.executable, {str(stuck)!r}],
                                     creationflags={_CREATE_SUSPENDED})
            open({str(pid_file)!r}, "w").write(str(child.pid))
            # Exits here WITHOUT ever calling ResumeThread -- the orphaning act itself.
        """), encoding="utf-8")
    else:
        shell.write_text(textwrap.dedent(f"""
            import os, signal, subprocess, sys
            child = subprocess.Popen([sys.executable, {str(stuck)!r}])
            os.kill(child.pid, signal.SIGSTOP)
            open({str(pid_file)!r}, "w").write(str(child.pid))
            # Exits here WITHOUT ever calling SIGCONT -- the orphaning act itself.
        """), encoding="utf-8")
    subprocess.run([sys.executable, str(shell)], check=True, timeout=30)
    return int(pid_file.read_text(encoding="utf-8").strip()), script_name


def _reap(pid: int) -> None:
    """No leftovers: the fixture process is killed whatever the test's verdict, whether or not
    the code under test already did it."""
    if not psutil.pid_exists(pid):
        return
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)
    else:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass


def _read_int_with_retry(path: Path, timeout_s: float = 10.0) -> int | None:
    """A fixture process's `open(path, "w").write(str(pid))` is two syscalls, not one: the file
    can EXIST with zero bytes for a real window between them. Polling on existence alone (as an
    earlier version of this suite did) races that window; polling on a successfully-parsed
    non-empty read does not."""
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            text = path.read_text(encoding="utf-8").strip()
            if text:
                return int(text)
        except (OSError, ValueError):
            pass
        time.sleep(0.05)
    return None


def _wait_gone(pid: int, timeout_s: float = 10.0) -> bool:
    """`taskkill`/`kill` above are fired, not awaited (same posture as `bounded_hook.py::
    _kill_tree`) -- poll rather than assume instant death."""
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if not psutil.pid_exists(pid):
            return True
        time.sleep(0.1)
    return not psutil.pid_exists(pid)


# --- Done-item 1: the reproduction ------------------------------------------------------------

def test_a_suspended_at_creation_orphan_shows_zero_cpu_and_no_live_parent(tmp_path):
    """The `[#863]` signature reproduced directly, before any watchdog code runs at all: a
    process alive, its CPU time not moving across a real sleep, and its parent already gone --
    never an inference from a description of the incident.

    Orphanhood is checked through `hw._is_orphaned`, not a bare `proc.parent() is None`: on
    POSIX a child whose parent exits is reparented to PID 1 (or a subreaper), never orphaned
    into a null parent, so `parent() is None` alone never holds there (Codex terra review,
    LANE-5B5-5-lane-hook-watchdog High finding) -- the platform-aware check is what this test
    is actually verifying against the fixture."""
    pid, _script_name = _spawn_orphaned_stuck_grandchild(tmp_path)
    try:
        proc = psutil.Process(pid)
        assert proc.is_running()
        cpu0 = proc.cpu_times()
        time.sleep(1.0)
        cpu1 = proc.cpu_times()
        assert cpu1.user + cpu1.system == pytest.approx(cpu0.user + cpu0.system, abs=1e-3)
        assert hw._is_orphaned(proc)
    finally:
        _reap(pid)


# --- Done-item 2: RED-first -- the watchdog detects and kills it, and records the kill --------

def test_sweep_kills_a_suspended_at_creation_orphan_and_records_the_kill(tmp_path, monkeypatch):
    log = tmp_path / "HOOK-WATCHDOG-KILLS.jsonl"
    monkeypatch.setenv(hw.RECORD_ENV, str(log))
    pid, script_name = _spawn_orphaned_stuck_grandchild(tmp_path)
    try:
        killed = hw.sweep(threshold_s=1.0, settings_path=_settings(tmp_path, script_name))

        assert len(killed) == 1, killed
        row = killed[0]
        assert row["pid"] == pid
        assert row["hook_id"] == f"cmd:{script_name}"
        assert row["reason"] == "zero-cpu-after-threshold"
        assert row["age_s"] is not None and row["age_s"] >= 0

        assert _wait_gone(pid), "sweep() reported a kill but the process is still alive"

        records = [json.loads(line) for line in
                  log.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert len(records) == 1
        assert records[0]["pid"] == pid
        # Best-effort only (honest limit: a suspended process never reads its own stdin, where
        # every OTHER hook surface gets a session id) -- some non-empty string, inherited
        # environment or the "unknown" fallback; never asserted to a fixed value, since the
        # test's own process environment is inherited by the fixture and is not controlled here.
        assert records[0]["session_id"]
    finally:
        _reap(pid)


class _FakeTimes:
    def __init__(self, user: float, system: float) -> None:
        self.user, self.system = user, system


class _FakeCandidateProc:
    """A test double for the ONE thing `sweep`'s decision actually reads off a process across
    the threshold window: `cmdline()`, `parent()` and successive `cpu_times()` calls. Real
    wall-clock CPU scheduling is NOT this module's concern to assert against -- this repo's own
    box runs many parallel lanes, and a real busy-loop process measured 0.03 s of accumulated
    CPU over 3 REAL seconds here once (a live scheduling artifact, not a `sweep()` defect;
    `logs/HOOK-WATCHDOG-KILLS.jsonl`'s own kind of honest limit). The arithmetic that decides
    moved-vs-not-moved is exercised deterministically instead, exactly the way `cpu_times()`
    reports it to `sweep` regardless of what the OS scheduler actually did."""

    def __init__(self, pid: int, cmdline: list[str], cpu_readings: list[tuple[float, float]]):
        self.pid = pid
        self._cmdline = cmdline
        self._readings = iter(cpu_readings)

    def cmdline(self):
        return self._cmdline

    def parent(self):
        return None  # orphaned, same as every real candidate `sweep` considers

    def cpu_times(self):
        return _FakeTimes(*next(self._readings))


def test_a_process_whose_cpu_time_is_moving_is_never_a_candidate(tmp_path, monkeypatch):
    """The negative control that keeps the two `[#863]`/`[#808]` failure modes apart: a
    candidate that STARTS near-zero (so it passes the baseline filter) but whose CPU time then
    DID move within the window is left alone -- only zero movement across the WHOLE window is
    this module's signal. The companion witness for the OTHER mode (ran, then legitimately
    blocked) is `tests/test_bounded_hook.py::
    test_a_guard_that_sleeps_past_its_bound_is_bypassed_and_the_bypass_is_recorded`, a separate
    mechanism entirely."""
    log = tmp_path / "HOOK-WATCHDOG-KILLS.jsonl"
    monkeypatch.setenv(hw.RECORD_ENV, str(log))
    running = _FakeCandidateProc(9001, ["python", "busy_hook.py"],
                                 [(0.02, 0.0), (2.1, 0.3)])  # near-zero at t0, moved by t1

    killed = hw.sweep(threshold_s=0, settings_path=_settings(tmp_path, "busy_hook.py"),
                      process_iter=lambda: [running], sleep=lambda _s: None)

    assert killed == []
    assert not log.exists() or log.read_text(encoding="utf-8").strip() == ""


def test_a_process_with_real_accumulated_cpu_is_never_a_candidate_even_if_flat_now(
        tmp_path, monkeypatch):
    """The Critical fix itself (Codex terra review, LANE-5B5-5-lane-hook-watchdog): a process
    that had ALREADY run real work before `sweep` ever samples it -- the "ran, then legitimately
    blocked" mode `[#808]`'s bound is meant to reach -- must never be killed by THIS module,
    even though its CPU total is perfectly flat for the whole window that follows (exactly the
    same observable shape a truly suspended-at-creation process has, IF only the window is
    looked at). Before this fix, `sweep` tracked and killed any orphaned candidate flat for one
    window regardless of its starting CPU total; this is the regression witness for that gap."""
    log = tmp_path / "HOOK-WATCHDOG-KILLS.jsonl"
    monkeypatch.setenv(hw.RECORD_ENV, str(log))
    ran_then_blocked = _FakeCandidateProc(9002, ["python", "busy_hook.py"],
                                          [(2.5, 0.4), (2.5, 0.4)])  # real CPU, flat afterward

    killed = hw.sweep(threshold_s=0, settings_path=_settings(tmp_path, "busy_hook.py"),
                      process_iter=lambda: [ran_then_blocked], sleep=lambda _s: None)

    assert killed == []
    assert not log.exists() or log.read_text(encoding="utf-8").strip() == ""


def test_a_real_busy_loop_process_does_accumulate_cpu_time(tmp_path):
    """The fake in the test above stands in for real OS scheduling, and that substitution is
    only honest if a real busy loop really does behave the way the fake claims SOMEWHERE in
    this suite. This is that check, on its own terms: no `sweep()`, no fixed window, just poll
    until the accumulation is unambiguous, however long the box takes to schedule it."""
    script_name = _unique("busy_hook.py")
    busy = tmp_path / script_name
    busy.write_text("x = 0\nwhile True:\n    x += 1\n", encoding="utf-8")
    proc = subprocess.Popen([sys.executable, str(busy)])
    try:
        cpu0 = hw._cpu_total(psutil.Process(proc.pid))
        deadline = time.monotonic() + 60
        moved = False
        while time.monotonic() < deadline:
            time.sleep(0.5)
            cpu1 = hw._cpu_total(psutil.Process(proc.pid))
            if cpu1 is not None and cpu0 is not None and cpu1 > cpu0:
                moved = True
                break
        assert moved, "a real busy-loop process accumulated no CPU time in 60 s"
    finally:
        _reap(proc.pid)


def test_a_process_with_a_live_parent_is_never_a_candidate(tmp_path, monkeypatch):
    """The orphan check's own reason to exist: a hook process still owned by a live session must
    never be touched, however long it has run at zero CPU (that is a legitimate wait, `[#808]`'s
    territory, not this module's)."""
    log = tmp_path / "HOOK-WATCHDOG-KILLS.jsonl"
    monkeypatch.setenv(hw.RECORD_ENV, str(log))
    script_name = _unique("owned_hook.py")
    stuck = tmp_path / script_name
    stuck.write_text(_STUCK_BODY, encoding="utf-8")
    if os.name == "nt":
        proc = subprocess.Popen([sys.executable, str(stuck)], creationflags=_CREATE_SUSPENDED)
    else:
        proc = subprocess.Popen([sys.executable, str(stuck)])
        os.kill(proc.pid, signal.SIGSTOP)
    try:
        killed = hw.sweep(threshold_s=1.0, settings_path=_settings(tmp_path, script_name))
        assert killed == []
        assert psutil.pid_exists(proc.pid)
    finally:
        _reap(proc.pid)


# --- "kills its whole process tree" ------------------------------------------------------------

def test_kill_tree_kills_the_whole_process_tree(tmp_path):
    parent_pid_file = tmp_path / "parent.pid"
    child_pid_file = tmp_path / "child.pid"
    parent_script = tmp_path / "tree_parent.py"
    parent_script.write_text(textwrap.dedent(f"""
        import subprocess, sys, time
        child = subprocess.Popen([sys.executable, "-c",
                                  "import time; time.sleep(3600)"])
        open({str(child_pid_file)!r}, "w").write(str(child.pid))
        time.sleep(3600)
    """), encoding="utf-8")
    parent = subprocess.Popen([sys.executable, str(parent_script)])
    parent_pid_file.write_text(str(parent.pid), encoding="utf-8")
    child_pid = None
    try:
        child_pid = _read_int_with_retry(child_pid_file)
        assert child_pid is not None, "the parent never wrote the child pid file"
        assert psutil.pid_exists(child_pid)

        hw.kill_tree(parent.pid)

        assert _wait_gone(parent.pid), "the parent survived kill_tree"
        assert _wait_gone(child_pid), "the child survived kill_tree -- not a whole-tree kill"
    finally:
        _reap(parent.pid)
        if child_pid is not None:
            _reap(child_pid)


# --- surfacing ---------------------------------------------------------------------------------

def test_surface_lines_reports_a_recent_kill(tmp_path, monkeypatch):
    log = tmp_path / "HOOK-WATCHDOG-KILLS.jsonl"
    monkeypatch.setenv(hw.RECORD_ENV, str(log))
    hw.append_record({"ts": hw._utc_now(), "hook_id": "cmd:stuck_hook.py", "pid": 4242,
                      "age_s": 12.3, "session_id": "unknown", "threshold_s": 30.0,
                      "reason": "zero-cpu-after-threshold"})
    lines = hw.surface_lines()
    assert any("1 suspended-at-creation kill" in line for line in lines)
    assert any("cmd:stuck_hook.py" in line and "pid 4242" in line for line in lines)


def test_surface_lines_is_silent_with_no_kills(tmp_path, monkeypatch):
    monkeypatch.setenv(hw.RECORD_ENV, str(tmp_path / "absent.jsonl"))
    assert hw.surface_lines() == []


def test_surface_lines_never_breaks_on_a_malformed_line(tmp_path, monkeypatch):
    log = tmp_path / "HOOK-WATCHDOG-KILLS.jsonl"
    log.write_text("not json\n", encoding="utf-8")
    monkeypatch.setenv(hw.RECORD_ENV, str(log))
    assert hw.surface_lines() == []


# --- _is_orphaned: platform-aware, unit-tested directly -----------------------------------------

class _FakeParentedProc:
    def __init__(self, parent, ppid: int):
        self._parent, self._ppid = parent, ppid

    def parent(self):
        return self._parent

    def ppid(self):
        return self._ppid


def test_is_orphaned_true_when_parent_is_none():
    """The Windows shape: a dead parent's pid is simply gone."""
    assert hw._is_orphaned(_FakeParentedProc(parent=None, ppid=4242))


def test_is_orphaned_true_when_reparented_to_pid_1():
    """The POSIX shape: a child whose parent exits is reparented to init, never orphaned into a
    null parent (Codex terra review, LANE-5B5-5-lane-hook-watchdog High finding) -- `parent()`
    returning a live process here must NOT by itself read as "still owned"."""
    live_init = _FakeParentedProc(parent=None, ppid=0)  # PID 1's own parent is 0
    assert hw._is_orphaned(_FakeParentedProc(parent=live_init, ppid=1))


def test_is_orphaned_false_with_a_live_non_init_parent():
    """The safety property `_is_orphaned` exists for: a hook process still owned by a live
    session (a real parent, not init) is never read as orphaned."""
    live_session_shell = _FakeParentedProc(parent=None, ppid=1)
    assert not hw._is_orphaned(_FakeParentedProc(parent=live_session_shell, ppid=9999))


# --- session id: best-effort, controlled environment -------------------------------------------

def test_session_id_for_falls_back_to_unknown_with_no_session_env_var(tmp_path):
    script = tmp_path / _unique("no_session.py")
    script.write_text("import time; time.sleep(30)\n", encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if "SESSION" not in k.upper()}
    proc = subprocess.Popen([sys.executable, str(script)], env=env)
    try:
        assert hw._session_id_for(psutil.Process(proc.pid)) == "unknown"
    finally:
        _reap(proc.pid)


def test_session_id_for_reads_a_session_env_var_when_present(tmp_path):
    script = tmp_path / _unique("with_session.py")
    script.write_text("import time; time.sleep(30)\n", encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if "SESSION" not in k.upper()}
    env["CLAUDE_SESSION_ID"] = "sess-watchdog-witness"
    proc = subprocess.Popen([sys.executable, str(script)], env=env)
    try:
        assert hw._session_id_for(psutil.Process(proc.pid)) == "sess-watchdog-witness"
    finally:
        _reap(proc.pid)


# --- candidate-name parsing ----------------------------------------------------------------------

def test_candidate_hook_names_reads_every_event_block(tmp_path):
    settings = tmp_path / "settings.json"
    settings.write_text(json.dumps({"hooks": {
        "PreToolUse": [{"hooks": [{"command": "uv run python scripts/hooks/scope_guard.py"}]}],
        "SessionStart": [{"hooks": [{"command": "uv run python scripts/fleet_health.py"}]}],
    }}), encoding="utf-8")
    names = hw._candidate_hook_names(settings)
    assert names == {"scope_guard.py", "fleet_health.py"}


def test_candidate_hook_names_is_empty_on_an_unreadable_settings_file(tmp_path):
    assert hw._candidate_hook_names(tmp_path / "does-not-exist.json") == set()


# --- CLI smoke -----------------------------------------------------------------------------------

def test_main_sweep_with_no_match_reports_nothing_found(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv(hw.RECORD_ENV, str(tmp_path / "kills.jsonl"))
    settings = _settings(tmp_path, "a-script-name-nothing-will-ever-run.py")
    rc = hw.main(["sweep", "--threshold", "0", "--settings", str(settings)])
    assert rc == 0
    assert "no suspended-at-creation candidate found" in capsys.readouterr().out
