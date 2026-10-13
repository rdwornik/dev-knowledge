"""The ONE SessionStart entry (`scripts/hooks/session_start.py`) -- batch BW lane
`lane-bw-1001-sessionstart-one`, row `[#1001]`.

Done-contract, as this file checks it:
  2. `.claude/settings.json` registers exactly ONE SessionStart command, launched through the
     shared launcher (`scripts/hooks/hook_launcher.py`), and its injected output is bounded by a
     named byte cap;
  3. the one entry runs the former readers in ONE interpreter (import, not a subprocess per
     reader), is stdlib-only itself, keeps every refusal or advisory line, and lists a dropped
     reader with why -- nothing is dropped silently.

The composition tests drive `session_start.run` with throwaway readers, so they measure the
entry's own mechanics (capture, cap, order, failure surfacing) and never depend on a real
reader's verdict. Each real reader's own lines stay pinned in that reader's own test file.
"""
from __future__ import annotations

import ast
import json
import os
import sys
import threading
import time
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SETTINGS = _REPO / ".claude" / "settings.json"
_TARGET = "scripts/hooks/session_start.py"
_MODULE = _REPO / _TARGET

sys.path.insert(0, str(_REPO / "scripts" / "hooks"))
import session_start as ss  # noqa: E402

from test_hook_launcher import launch_command  # noqa: E402

#: The nine SessionStart entries `.claude/settings.json` carried before this lane (measured in
#: `docs/audits/2026-10-13-technical-lane-bw-1001-sessionstart-measurement.md`).
_FORMER = (
    "scripts/arm_hooks.py",
    "scripts/surface_triage.py",
    "scripts/changelog_sentinel.py",
    "scripts/conductor.py",
    "scripts/resource_lifecycle.py",
    "scripts/codespace_regime.py",
    "scripts/billing_leak_sentinel.py",
    "scripts/fleet_health.py",
    "scripts/hooks/quota_daily.py",
)


def _session_start_entries() -> list[dict]:
    hooks = json.loads(_SETTINGS.read_text(encoding="utf-8"))["hooks"]
    return [h for g in hooks["SessionStart"] for h in g["hooks"]]


# --- 2. one registered command, through the launcher, bounded ---------------------------------

def test_settings_registers_exactly_one_session_start_command_through_the_launcher():
    entries = _session_start_entries()
    assert [e["command"] for e in entries] == [launch_command(_TARGET)]
    assert isinstance(entries[0].get("timeout"), int) and entries[0]["timeout"] > 0


def test_the_output_cap_is_a_named_positive_constant():
    assert isinstance(ss.OUTPUT_CAP_BYTES, int) and ss.OUTPUT_CAP_BYTES > 0
    assert isinstance(ss.LINE_CAP_BYTES, int) and 0 < ss.LINE_CAP_BYTES < ss.OUTPUT_CAP_BYTES


def _reader(rid: str, fn, script: str = "scripts/x.py") -> ss.Reader:
    return ss.Reader(rid, script, fn)


def test_injected_output_never_exceeds_the_cap():
    def bulky():
        for i in range(2000):
            print(f"[bulk] line {i} " + "x" * 120)
    out, _err = ss.run([_reader("bulky", bulky)])
    assert len(out.encode("utf-8")) <= ss.OUTPUT_CAP_BYTES
    assert "[session-start] cut" in out


def test_a_long_line_is_shortened_to_the_line_cap():
    def long_line():
        print("[long] " + "y" * (ss.LINE_CAP_BYTES * 3))
    out, _err = ss.run([_reader("long", long_line)])
    line = out.splitlines()[0]
    assert len(line.encode("utf-8")) <= ss.LINE_CAP_BYTES
    assert line.startswith("[long] ")


def test_refusal_and_advisory_lines_survive_an_overflow():
    def banner():
        print("[prompts] REFUSED -- the two CLAUDE_PROMPTS_DIR scopes disagree")
        print("[prompts-guard] preflight FAILED -- guard script missing")

    def bulky():
        for i in range(2000):
            print(f"[bulk] line {i} " + "x" * 120)

    def late_warning():
        print("[billing] WARN: ANTHROPIC_API_KEY is visible in this Claude Code session")
        print("[gh] auth invalid -- run: gh auth refresh -h github.com")

    out, _err = ss.run([_reader("banner", banner), _reader("bulky", bulky),
                        _reader("late", late_warning)])
    assert len(out.encode("utf-8")) <= ss.OUTPUT_CAP_BYTES
    for pinned in ("[prompts] REFUSED", "[prompts-guard] preflight FAILED",
                   "[billing] WARN", "[gh] auth invalid"):
        assert pinned in out, pinned


def test_output_order_is_reader_order_not_finish_order():
    def slow():
        time.sleep(0.3)
        print("[a] first reader")

    def fast():
        print("[b] second reader")

    out, _err = ss.run([_reader("a", slow), _reader("b", fast)])
    assert out.index("[a] first reader") < out.index("[b] second reader")


# --- 3. one interpreter, stdlib only, nothing dropped silently --------------------------------

def test_readers_run_in_this_interpreter_not_a_subprocess():
    seen = []
    out, _err = ss.run([_reader("pid", lambda: seen.append(os.getpid()))])
    assert seen == [os.getpid()]


def test_the_module_imports_only_the_stdlib_and_spawns_no_process():
    tree = ast.parse(_MODULE.read_text(encoding="utf-8"))
    reader_modules = {Path(r.script).stem for r in ss.READERS}
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    third_party = sorted(n for n in names - reader_modules
                         if n not in sys.stdlib_module_names and n != "__future__")
    assert not third_party, third_party
    assert "subprocess" not in names


def test_every_former_reader_is_run_or_listed_as_dropped_with_a_reason():
    run_scripts = {r.script for r in ss.READERS}
    dropped = dict(ss.DROPPED)
    assert run_scripts | set(dropped) == set(_FORMER)
    assert not run_scripts & set(dropped)
    for script, why in dropped.items():
        assert isinstance(why, str) and why.strip(), script
    for script in run_scripts:
        assert (_REPO / script).is_file(), script


def test_a_failing_reader_is_named_and_the_entry_still_exits_zero():
    def raises():
        raise RuntimeError("boom")

    def exits():
        raise SystemExit(2)

    def fine():
        print("[ok] still here")

    out, _err = ss.run([_reader("raises", raises), _reader("exits", exits),
                        _reader("fine", fine)])
    assert "[session-start] raises raised RuntimeError: boom" in out
    assert "[session-start] exits exited 2" in out
    assert "[ok] still here" in out


def test_a_reader_past_the_deadline_is_named_not_waited_for():
    gate = threading.Event()

    def hangs():
        gate.wait(5)

    t0 = time.perf_counter()
    out, _err = ss.run([_reader("hangs", hangs)], deadline_s=0.3)
    gate.set()
    assert time.perf_counter() - t0 < 3
    assert "[session-start] hangs still running after 0.3 s" in out


def test_the_hook_payload_reaches_a_reader_that_reads_stdin_from_its_own_thread():
    got = []

    def reads_from_a_helper_thread():
        t = threading.Thread(target=lambda: got.append(sys.stdin.read()), daemon=True)
        t.start()
        t.join(2)

    ss.run([_reader("stdin", reads_from_a_helper_thread)], payload='{"session_id": "s1"}')
    assert got == ['{"session_id": "s1"}']


def test_stderr_is_kept_apart_from_the_injected_stdout():
    def both():
        print("[x] to context")
        print("loud operator line", file=sys.stderr)

    out, err = ss.run([_reader("both", both)])
    assert "[x] to context" in out and "loud operator line" not in out
    assert "loud operator line" in err


@pytest.mark.parametrize("reader", ss.READERS, ids=lambda r: r.reader_id)
def test_each_real_reader_names_a_script_on_disk(reader):
    assert (_REPO / reader.script).is_file()


def test_the_parity_arm_probe_follows_the_one_entry_and_arm_hooks_stays_its_reader():
    """`ecosystem/parity-surfaces.yaml` settings-precommit-arm names the hub's arm hook by its
    local name. It now names this entry, which is honest only while arm_hooks.py is one of its
    readers -- the coupling this test holds."""
    import yaml

    rows = yaml.safe_load((_REPO / "ecosystem" / "parity-surfaces.yaml").read_text(
        encoding="utf-8"))["surfaces"]
    arm = next(r for r in rows if r["id"] == "settings-precommit-arm")
    assert arm["local_names"][".dev-knowledge"] == Path(_TARGET).name
    assert "scripts/arm_hooks.py" in {r.script for r in ss.READERS}


def test_a_reader_that_reads_stdin_until_eof_gets_the_payload_once():
    chunks = []

    def drains():
        while True:
            chunk = sys.stdin.read(4096)
            if not chunk:
                break
            chunks.append(chunk)

    ss.run([_reader("drain", drains)], payload='{"a": 1}', deadline_s=2)
    assert chunks == ['{"a": 1}']


def test_a_straggler_cannot_print_past_the_cap_once_the_output_is_composed():
    gate = threading.Event()
    saved = sys.stdout, sys.stderr

    def late():
        gate.wait(5)
        print("[late] after the deadline")

    try:
        out, _err = ss.run([_reader("late", late)], deadline_s=0.2, silence_stragglers=True)
        silenced = sys.stdout
        gate.set()
        time.sleep(0.3)
        assert silenced is not saved[0]
        assert silenced.write("x") == 1  # a sink: it accepts and discards
        assert "[late] after the deadline" not in out
    finally:
        sys.stdout, sys.stderr = saved


def test_the_cap_holds_even_when_protected_lines_alone_exceed_it():
    def floods():
        for i in range(500):
            print(f"[hook-BROKEN] guard-{i} DECLARED BROKEN " + "z" * 200)

    out, _err = ss.run([_reader("floods", floods)])
    assert len(out.encode("utf-8")) <= ss.OUTPUT_CAP_BYTES
    assert out.splitlines()[0].startswith("[hook-BROKEN] guard-0 ")
    assert "[session-start] cut" in out.splitlines()[-1]


def test_a_helper_thread_a_finished_reader_left_behind_cannot_write_past_the_digest():
    saved = sys.stdout, sys.stderr
    written = threading.Event()
    late_target = []

    def leaves_a_writer():
        def later():
            time.sleep(0.3)
            late_target.append(sys.stdout)
            print("[late] from a helper thread")
            written.set()
        threading.Thread(target=later, daemon=True).start()

    try:
        out, _err = ss.run([_reader("leaves", leaves_a_writer)], silence_stragglers=True)
        assert written.wait(3)
        assert late_target and late_target[0] is not saved[0]
        assert isinstance(late_target[0], ss._Sink)
        assert "[late] from a helper thread" not in out
    finally:
        sys.stdout, sys.stderr = saved


def test_a_writer_running_through_the_whole_call_never_sees_the_real_streams():
    """Codex r2: no restore-then-sink window. A helper thread polls `sys.stdout` in a tight loop
    from before the readers finish until after `run` returns; it must never see the real one."""
    saved = sys.stdout, sys.stderr
    stop = threading.Event()
    seen_real = []

    def spawns_a_poller():
        def poll():
            while not stop.is_set():
                if sys.stdout is saved[0] or sys.stderr is saved[1]:
                    seen_real.append(True)
        threading.Thread(target=poll, daemon=True).start()

    try:
        for _ in range(20):
            ss.run([_reader("poller", spawns_a_poller)], silence_stragglers=True)
            time.sleep(0.01)
            sys.stdout, sys.stderr = ss._Sink(), ss._Sink()  # stay silenced between calls
    finally:
        stop.set()
        time.sleep(0.05)
        sys.stdout, sys.stderr = saved
    assert not seen_real
