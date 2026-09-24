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
_TRANSCRIPTS_ENV = "DEV_KNOWLEDGE_HOOK_TRANSCRIPTS"

_PAYLOAD = {"session_id": "sess-808-witness", "hook_event_name": "PreToolUse",
            "tool_name": "Bash", "tool_input": {"command": "echo hi"}}


def _load_wrapper():
    spec = importlib.util.spec_from_file_location("bounded_hook_under_test", _WRAPPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _env(log_path: Path, transcripts: Path | None = None) -> dict[str, str]:
    """Every surface a case touches points into `tmp_path`: the record, the declarations and
    scan cache beside it, and the transcript store -- never the operator's real session store."""
    env = {k: v for k, v in os.environ.items() if k not in (_LOG_ENV, _TRANSCRIPTS_ENV)}
    env[_LOG_ENV] = str(log_path)
    env[_TRANSCRIPTS_ENV] = str(transcripts or (log_path.parent / "no-transcripts"))
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
    # No BYPASS is written. One RUN row is: the bypass rate needs its denominator (operator
    # ruling 2026-09-17), and a run is not a skip -- `surface` never lists it as one.
    assert [r["reason"] for r in _records(log)] == ["ok"]


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


def _fleet_health():
    spec = importlib.util.spec_from_file_location(
        "fleet_health_under_808", _REPO_ROOT / "scripts" / "fleet_health.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_surface_is_printed_at_session_start_by_the_existing_digest(tmp_path, monkeypatch):
    """Operator ruling 2026-09-17 item 1: the `.claude/settings.json` wiring is HELD -- a wrapper
    or a new hook adds an interpreter to every boot, which makes the measured suspended-at-start
    failure likelier. So the surface rides INSIDE the SessionStart hook that already runs,
    `fleet_health.py`, in-process: no new registration, no new interpreter. (This replaces the
    lane's earlier witness that a separate `surface` hook was registered; the ruling removed the
    registration, and the property -- the record reaches every boot -- is what stays asserted.)"""
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    log.write_text(json.dumps({"ts": now, "hook_id": "slow-guard", "bound_s": 10,
                               "elapsed_s": 10.4, "session_id": "s", "reason": "timeout",
                               "posture": "fail-open"}) + "\n", encoding="utf-8")
    for key, value in _env(log).items():
        if key in (_LOG_ENV, _TRANSCRIPTS_ENV):
            monkeypatch.setenv(key, value)
    fh = _fleet_health()

    lines = fh.hook_bypass_lines()

    assert any("slow-guard" in line for line in lines), lines
    import ast
    tree = ast.parse((_REPO_ROOT / "scripts" / "fleet_health.py").read_text(encoding="utf-8"))
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    called = {n.func.id for n in ast.walk(main)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "hook_bypass_lines" in called, "fleet_health.main() no longer prints the bypass surface"


def test_the_bypass_surface_never_breaks_the_digest(tmp_path, monkeypatch):
    fh = _fleet_health()
    monkeypatch.setattr(fh, "_import_bounded_hook", lambda: (_ for _ in ()).throw(OSError("x")))
    assert fh.hook_bypass_lines() == []


# --- Operator ruling 2026-09-17 item 2: the BYPASS RATE is the signal ---------------------------

def _run_rows(hook_id: str, runs: int, bypasses: int, ts: str | None = None) -> str:
    ts = ts or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rows = [{"ts": ts, "hook_id": hook_id, "bound_s": 10, "elapsed_s": 10.5 if i < bypasses else 0.4,
             "session_id": f"s{i}", "reason": "timeout" if i < bypasses else "ok",
             "posture": "fail-open"} for i in range(runs)]
    return "".join(json.dumps(r) + "\n" for r in rows)


def _surface(log: Path, transcripts: Path | None = None, *extra: str):
    return subprocess.run([sys.executable, str(_WRAPPER), "surface", *extra],
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          env=_env(log, transcripts))


def _declarations(log: Path) -> dict:
    path = log.with_name("HOOK-BYPASSES-BROKEN.json")
    return json.loads(path.read_text(encoding="utf-8")).get("broken", {}) if path.exists() else {}


def test_a_hook_whose_bypass_rate_exceeds_the_threshold_is_DECLARED_BROKEN_with_its_numbers(
        tmp_path):
    module = _load_wrapper()
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    runs = module.BROKEN_MIN_RUNS + 10
    bypasses = int(runs * module.BROKEN_RATE) + 3
    log.write_text(_run_rows("changelog-sentinel", runs, bypasses), encoding="utf-8")

    res = _surface(log)

    assert res.returncode == 0, res.stderr
    declared = _declarations(log)
    assert set(declared) == {"changelog-sentinel"}, declared
    decl = declared["changelog-sentinel"]
    assert (decl["runs"], decl["bypasses"]) == (runs, bypasses)
    assert decl["threshold"] == module.BROKEN_RATE
    assert decl["window_h"] == module.RATE_WINDOW_H
    # The row carries its numbers, so whoever files it files the measurement, not a paraphrase.
    assert f"{bypasses} of {runs}" in decl["draft_row"]
    # Surfaced beside the recent skips, with the rate itself.
    assert "changelog-sentinel" in res.stdout and "DECLARED BROKEN" in res.stdout
    assert f"{bypasses}/{runs}" in res.stdout
    # X-2 (operator ruling 2026-09-17): a hook never files a row. It drafts to a known place, and
    # the integrator files at batch close -- the line must say both.
    assert "NOT filed" in res.stdout and "integrator files" in res.stdout
    # X-1: a declaration that cannot enforce says so, never implies the action.
    assert decl["scope"] == "repo" and "Disabled: NO" in res.stdout


def test_the_report_states_its_own_hosts_declared_status_and_is_not_special_cased(tmp_path):
    """X-4 (operator ruling 2026-09-17): the bar declaring `fleet_health.py` -- the hook this report
    prints from -- is correct and must NOT be exempted. The report still prints, and says in its
    own output that its host is declared broken, so a reader knows why it is sometimes absent."""
    module = _load_wrapper()
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    runs = module.BROKEN_MIN_RUNS + 10
    log.write_text(_run_rows(module.HOST_HOOK_ID, runs, runs // 2), encoding="utf-8")

    res = _surface(log)

    assert res.returncode == 0, res.stderr
    assert module.HOST_HOOK_ID in _declarations(log), "the report's own host was exempted"
    host_lines = [line for line in res.stdout.splitlines() if "this report's own host" in line]
    assert len(host_lines) == 1, res.stdout
    assert f"{runs // 2}/{runs}" in host_lines[0]


def test_a_rate_at_or_under_the_threshold_or_a_thin_sample_declares_nothing(tmp_path):
    module = _load_wrapper()
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    runs = module.BROKEN_MIN_RUNS * 2
    log.write_text(_run_rows("fine-guard", runs, int(runs * module.BROKEN_RATE))
                   + _run_rows("thin-guard", module.BROKEN_MIN_RUNS - 1,
                               module.BROKEN_MIN_RUNS - 1), encoding="utf-8")

    res = _surface(log)

    assert res.returncode == 0, res.stderr
    assert _declarations(log) == {}
    # The thin sample is SAID to be thin, not silently treated as healthy.
    assert "thin-guard" in res.stdout and "sample" in res.stdout


def test_a_declared_broken_hook_is_disabled_by_the_wrapper_and_the_skip_is_recorded(tmp_path):
    """Disabled AUTOMATICALLY: the wrapper does not start a declared-broken hook at all. The
    stand-in would leave a marker file if it ran. A `declared-broken` skip is not a run, so it
    cannot feed the rate that declared it."""
    module = _load_wrapper()
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    runs = module.BROKEN_MIN_RUNS + 5
    log.write_text(_run_rows("leaky-guard", runs, runs), encoding="utf-8")
    assert _surface(log).returncode == 0
    assert "leaky-guard" in _declarations(log)
    marker = tmp_path / "ran.txt"
    guard = _script(tmp_path, "guard.py", f"open({str(marker)!r}, 'w').write('ran')\n")

    rc, out, err, _ = _run_like_harness(
        [sys.executable, str(_WRAPPER), "run", "--id", "leaky-guard", "--bound", "20",
         "--", sys.executable, str(guard)], log)

    assert rc == 0, (rc, out, err)
    assert not marker.exists(), "a DECLARED BROKEN hook was still run"
    assert "DECLARED BROKEN" in out
    assert _records(log)[-1]["reason"] == "declared-broken"
    decl = _declarations(log)["leaky-guard"]
    _surface(log)
    assert _declarations(log)["leaky-guard"] == decl, "the skip fed back into the declaration"


def test_a_declaration_is_sticky_until_reinstated_and_old_bypasses_do_not_re_declare(tmp_path):
    """A disabled hook produces no runs, so a declaration that lapsed when the rate went quiet
    would re-arm a broken guard by itself. It stays until a person reinstates it, and the
    reinstatement starts the count again rather than re-reading the window that condemned it."""
    module = _load_wrapper()
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    old = (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 3600)))
    runs = module.BROKEN_MIN_RUNS + 5
    log.write_text(_run_rows("leaky-guard", runs, runs, ts=old), encoding="utf-8")
    assert _surface(log).returncode == 0
    assert "leaky-guard" in _declarations(log)

    res = subprocess.run([sys.executable, str(_WRAPPER), "reinstate", "--id", "leaky-guard"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace",
                         env=_env(log))
    assert res.returncode == 0, res.stdout + res.stderr
    assert _declarations(log) == {}

    _surface(log)
    assert _declarations(log) == {}, "the pre-reinstatement window re-declared the hook"


def test_reinstating_a_hook_stops_the_banner_calling_it_DECLARED_BROKEN(tmp_path):
    """lane-hooks-urgent (LANE-5A-7) done-contract item 4, proven directly against the banner
    TEXT rather than only the JSON store: a hook that keeps its `broken` entry after being fixed
    keeps printing `[hook-BROKEN] <id> DECLARED BROKEN ...` at every SessionStart even though the
    settings.json wiring already re-armed it -- the exact "the banner lies" defect this lane was
    filed to fix (DIGEST-HOOK-ARCHITECTURE-2026-09-23-APPENDIX.md A6 item 6). Once reinstated,
    the surfaced report must no longer name that hook as broken at all.
    """
    module = _load_wrapper()
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    old = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 3600))
    runs = module.BROKEN_MIN_RUNS + 5
    log.write_text(_run_rows("fleet-health-session-start", runs, runs, ts=old), encoding="utf-8")

    before = _surface(log)
    assert "fleet-health-session-start" in _declarations(log)
    assert "fleet-health-session-start" in before.stdout and "DECLARED BROKEN" in before.stdout

    res = subprocess.run(
        [sys.executable, str(_WRAPPER), "reinstate", "--id", "fleet-health-session-start"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env(log))
    assert res.returncode == 0, res.stdout + res.stderr

    after = _surface(log)
    assert after.returncode == 0, after.stderr
    assert "fleet-health-session-start" not in _declarations(log)
    broken_lines = [line for line in after.stdout.splitlines()
                   if "DECLARED BROKEN" in line and "fleet-health-session-start" in line]
    assert broken_lines == [], (
        f"the banner still calls a reinstated hook DECLARED BROKEN: {broken_lines}")


def _transcript(dir_: Path, name: str, lines: list[dict]) -> None:
    dir_.mkdir(parents=True, exist_ok=True)
    (dir_ / name).write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")


def _attachment(ts, sid, event, command, kind="hook_success", timed_out=False, tool=None,
                firing=None):
    attachment = {"type": kind, "hookEvent": event, "command": command,
                  "hookName": f"{event}:{tool}" if tool else event, "durationMs": 100,
                  "toolUseID": firing or f"{sid}-{event}"}
    if timed_out:
        attachment.update(type="hook_cancelled", timedOut=True, timeoutMs=10000)
    return {"type": "attachment", "timestamp": ts, "sessionId": sid, "attachment": attachment}


def _tool_use(ts, sid, name):
    return {"type": "assistant", "timestamp": ts, "sessionId": sid,
            "message": {"content": [{"type": "tool_use", "name": name, "id": "t"}]}}


def test_the_rate_is_read_from_the_transcripts_for_a_hook_the_wrapper_never_ran(tmp_path):
    """The guards behind the wedges were NOT wrapped, and the wiring stays held -- so the
    transcripts' `hook_cancelled` attachments are the only live counter for them.

    ATTACHMENTS ARE NOT RUNS. A hook that passes SILENTLY writes no attachment, on every event
    (measured 2026-09-17, per call: 8,046 prompts-guard-matched calls carried 1,112 attachments;
    `arm_hooks.py` attached in 109 of 263 SessionStart firings, every one with output). Counting
    attachments as runs inflates the rate by exactly the runs that went well -- the error behind
    this lane's retracted "477 of 573 (83%)". So the denominator is the FIRINGS of the hook's
    event between its first and last recorded run: distinct firings for SessionStart/Stop, calls
    of the tools it was seen matching for PreToolUse -- or the attachments, if more."""
    module = _load_wrapper()
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    store = tmp_path / "projects" / "C--Dev--dev-knowledge"
    now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    n = module.BROKEN_MIN_RUNS + 20
    start = 'uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/changelog_sentinel.py"'
    sibling = 'uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/fleet_health.py"'
    triage = 'powershell -ExecutionPolicy Bypass -File "$CLAUDE_PROJECT_DIR/scripts/surface_triage.ps1"'
    guard = 'G="$CLAUDE_PROJECT_DIR/scripts/hooks/deny_and_point.py"; python "$G"'
    wrapped = 'python "x/scripts/hooks/bounded_hook.py" run --id arm-hooks --bound 40 -- python y'
    user_level = ('powershell -ExecutionPolicy Bypass -File '
                  '"C:\\Users\\someone\\.claude\\hooks\\surface-closures-with-a-long-name.ps1"')
    lines = []
    for i in range(n):
        # One SessionStart firing per session. The sibling always prints, so it always attaches;
        # the sentinel attaches ONLY when it times out (a quarter of firings) and passes silently
        # otherwise; triage times out on a third. Wrapped attachments are not transcript runs.
        lines.append(_attachment(now, f"s{i}", "SessionStart", sibling, firing=f"f{i}"))
        if i % 4 == 0:
            lines.append(_attachment(now, f"s{i}", "SessionStart", start, timed_out=True,
                                     firing=f"f{i}"))
        if i % 3 == 0:
            lines.append(_attachment(now, f"s{i}", "SessionStart", triage, timed_out=True,
                                     firing=f"f{i}"))
        lines.append(_attachment(now, f"s{i}", "SessionStart", wrapped, timed_out=True,
                                 firing=f"f{i}"))
        lines.append(_attachment(now, f"s{i}", "SessionStart", user_level, timed_out=True,
                                 firing=f"f{i}"))
    # PreToolUse: 3 timeouts out of 100 Bash calls -- 3%, not 3/3.
    lines += [_tool_use(now, "p1", "Bash") for _ in range(100)]
    lines += [_attachment(now, "p1", "PreToolUse", guard, timed_out=True, tool="Bash",
                          firing=f"t{i}") for i in range(3)]
    _transcript(store, "sess.jsonl", lines)

    res = _surface(log, tmp_path / "projects")

    assert res.returncode == 0, res.stderr
    declared = _declarations(log)
    # A hook this repo does not register is named by its script, and declared as NOT disableable
    # from here rather than as held wiring -- only its owner's settings can stop it.
    user_id = "cmd:surface-closures-with-a-long-name.ps1"
    assert set(declared) == {"changelog-sentinel", "surface-triage", user_id}, declared
    assert "outside this repo" in declared[user_id]["draft_row"]
    # X-5 (operator ruling 2026-09-17): out-of-repo hooks are declared ADVISORY -- named, with their
    # rates, routed to the user-level disable. The repo observes what it cannot stop and must not
    # claim to stop it.
    assert declared[user_id]["scope"] == "advisory"
    assert "ADVISORY" in declared[user_id]["draft_row"]
    advisory = [line for line in res.stdout.splitlines() if line.startswith("[hook-ADVISORY]")]
    assert len(advisory) == 1 and user_id in advisory[0] and "user-level disable" in advisory[0]
    assert not any(line.startswith("[hook-BROKEN]") and user_id in line
                   for line in res.stdout.splitlines())
    sentinel = declared["changelog-sentinel"]
    assert (sentinel["bypasses"], sentinel["runs"]) == (len(range(0, n, 4)), n), \
        "a silent pass was not counted as a run"
    assert "fleet-health-session-start" not in res.stdout  # zero bypasses: not listed
    assert "3/100" in res.stdout, res.stdout


def test_a_partial_transcript_scan_never_declares(tmp_path):
    """The scan is incremental and time-boxed so SessionStart pays for new bytes only. A rate
    read off part of the window is not the rate, so nothing is declared until the scan is whole."""
    module = _load_wrapper()
    log = tmp_path / "HOOK-BYPASSES.jsonl"
    store = tmp_path / "projects" / "C--Dev--dev-knowledge"
    now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    start = 'uv run --locked python "$CLAUDE_PROJECT_DIR/scripts/changelog_sentinel.py"'
    n = module.BROKEN_MIN_RUNS + 5
    _transcript(store, "sess.jsonl",
                [_attachment(now, f"s{i}", "SessionStart", start, timed_out=True) for i in range(n)])

    partial = _surface(log, tmp_path / "projects", "--scan-budget", "0")
    assert _declarations(log) == {}
    assert "partial" in partial.stdout

    _surface(log, tmp_path / "projects")
    assert "changelog-sentinel" in _declarations(log)


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
