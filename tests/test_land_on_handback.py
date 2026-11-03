"""RED-first witnesses for the HANDBACK-triggered lander and its merge clock."""
from __future__ import annotations

import ast
import inspect
import json
import os
import re
import subprocess
import sys
import time
from functools import partial
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from click.testing import CliRunner

import graph_queries as gq
import lane_end_guard as leg
import land_lane as ll
import merge_path
import land_on_handback


SLUG = "lane-a"
BATCH = "E1.0"
INTEGRATION = "worktree-integrate-e1.0"
_MISSING = object()
_REPO = Path(__file__).resolve().parents[1]


def _git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return proc.stdout.strip()


def _config(clone: Path) -> None:
    _git(clone, "config", "user.name", "Test")
    _git(clone, "config", "user.email", "test@example.com")
    _git(clone, "config", "core.autocrlf", "false")


def _commit_file(clone: Path, name: str, text: str, message: str) -> str:
    path = clone / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    _git(clone, "add", name)
    _git(clone, "commit", "-m", message)
    return _git(clone, "rev-parse", "HEAD")


class Env:
    def __init__(self, root: Path):
        self.root = root
        self.origin = root / "origin.git"
        self.seed = root / "seed"
        self.lane = root / "lane"
        self.worktree = root / "worktree"
        self.carry = root / "carry.jsonl"
        root.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "init", "--bare", "-b", "main", str(self.origin)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "clone", str(self.origin), str(self.seed)],
            check=True,
            capture_output=True,
        )
        _config(self.seed)
        _git(self.seed, "checkout", "-B", "main")
        (self.seed / "logs").mkdir()
        (self.seed / "README.md").write_text("readme\n", encoding="utf-8", newline="\n")
        (self.seed / "logs" / "MERGE-RECEIPTS.jsonl").write_text("", encoding="utf-8")
        (self.seed / "shared.txt").write_text("base\n", encoding="utf-8", newline="\n")
        _git(self.seed, "add", "-A")
        _git(self.seed, "commit", "-m", "seed")
        _git(self.seed, "push", "origin", "main")
        subprocess.run(
            ["git", "clone", str(self.origin), str(self.lane)],
            check=True,
            capture_output=True,
        )
        _config(self.lane)
        self.make_lane("lane-a", "lane_a.txt")
        subprocess.run(
            ["git", "clone", str(self.origin), str(self.worktree)],
            check=True,
            capture_output=True,
        )
        _config(self.worktree)
        _git(self.worktree, "checkout", "main")

    def make_lane(self, slug: str, filename: str, *, text: str = "lane\n") -> str:
        _git(self.lane, "fetch", "origin")
        _git(self.lane, "checkout", "-B", f"worktree-{slug}", "origin/main")
        _commit_file(self.lane, filename, text, f"lane {slug}")
        _git(self.lane, "push", "-f", "origin", f"worktree-{slug}")
        return _git(self.lane, "rev-parse", "HEAD")

    def make_conflicting_lane(self, slug: str) -> str:
        sha = self.make_lane(slug, "shared.txt", text="lane side\n")
        self.advance_main(name="shared.txt", text="main side\n")
        return sha

    def advance_main(self, name: str = "moved.txt", text: str = "moved\n") -> str:
        _git(self.seed, "pull", "--ff-only", "origin", "main")
        sha = _commit_file(self.seed, name, text, "main moves")
        _git(self.seed, "push", "origin", "main")
        return sha

    def origin_ref(self, ref: str) -> str:
        proc = subprocess.run(
            ["git", "-C", str(self.origin), "rev-parse", "--verify", "-q", ref],
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()

    def refs(self) -> str:
        return _git(self.origin, "for-each-ref", "--format=%(refname) %(objectname)")

    def ledger_on_main(self) -> list[str]:
        out = _git(self.origin, "show", "main:logs/MERGE-RECEIPTS.jsonl")
        return [line for line in out.splitlines() if line.strip()]

    def status(self) -> str:
        return _git(self.worktree, "status", "--porcelain")

    def head(self) -> str:
        return _git(self.worktree, "rev-parse", "HEAD")


@pytest.fixture(autouse=True)
def _events(tmp_path, monkeypatch):
    monkeypatch.setenv(merge_path.EVENTS_PATH_ENV, str(tmp_path / "events" / "events.jsonl"))
    for i, (key, value) in enumerate(
        (("safe.bareRepository", "all"), ("core.autocrlf", "false"))
    ):
        monkeypatch.setenv(f"GIT_CONFIG_KEY_{i}", key)
        monkeypatch.setenv(f"GIT_CONFIG_VALUE_{i}", value)
    monkeypatch.setenv("GIT_CONFIG_COUNT", "2")


@pytest.fixture
def env(tmp_path, monkeypatch):
    result = Env(tmp_path / "env")
    monkeypatch.chdir(result.worktree)
    monkeypatch.delenv("HARNESS_LANE", raising=False)
    monkeypatch.delenv("HARNESS_RECEIPTS_DIR", raising=False)
    return result


@pytest.fixture
def case(env, tmp_path):
    transport = tmp_path / "transport"
    (transport / "to-browser").mkdir(parents=True)
    return SimpleNamespace(
        env=env,
        transport=transport,
        receipts=tmp_path / "receipts",
        wake_home=tmp_path / "integrator-wake",
        clock=tmp_path / "MERGE-CLOCK.jsonl",
        state=tmp_path / "state",
        tmp_path=tmp_path,
    )


def pass_verdict(sha, **kwargs):
    return SimpleNamespace(
        state="PASS",
        missing_contexts=(),
        reason="",
        newly_failing=(),
        new_tests=(),
        jobs=(),
    )


def stub_suite(root, *, slug, sha, required_contexts=None):
    """Record a landable suite read on the open receipt, as `record_actions_verdict` would."""
    import merge_receipt

    receipt = merge_receipt.load_receipt(root, slug)
    receipt.steps.append(
        merge_receipt.StepTiming(
            step="suite",
            step_class=merge_receipt.CLASS_CEREMONY,
            seconds=0.0,
            ok=True,
            returncode=0,
            command="stub",
            started="",
            verdict_state="PASS",
        )
    )
    merge_receipt.save_receipt(root, receipt)


def model_cli_sandbox(tmp_path: Path, monkeypatch) -> Path:
    bin_dir = tmp_path / "model-bin"
    bin_dir.mkdir()
    marker = tmp_path / "model-called.txt"
    for name in ("claude", "codex", "copilot"):
        if sys.platform == "win32":
            (bin_dir / f"{name}.cmd").write_text(
                f'@echo {name}>>"{marker}"\r\n', encoding="utf-8"
            )
        shim = bin_dir / name
        shim.write_text(
            f'#!/bin/sh\necho {name} >> "{marker}"\n',
            encoding="utf-8",
            newline="\n",
        )
        shim.chmod(0o755)
    monkeypatch.setenv("PATH", str(bin_dir) + os.pathsep + os.environ.get("PATH", ""))
    return marker


def _line(slug: str, sha: str, branch: str | None = None) -> str:
    return f"HANDBACK {branch or f'worktree-{slug}'} @ {sha} code"


def _launch(case, slug: str, batch: str = BATCH, engine=_MISSING) -> Path:
    case.receipts.mkdir(parents=True, exist_ok=True)
    body = {"organ": "launch", "batch": batch}
    if engine is not _MISSING:
        body["engine"] = engine
    path = case.receipts / f"LAUNCH-{slug.upper()}.json"
    path.write_text(json.dumps(body), encoding="utf-8", newline="\n")
    return path


def _session(
    case,
    slug: str,
    line: str,
    models: str = (
        "MODELS:\n"
        "  implement: requested=claude-sonnet-5-5/high served=claude-sonnet-5-5\n"
    ),
) -> Path:
    path = case.transport / "to-browser" / f"SESSION-{slug}.md"
    path.write_text(f"{models}{line}\n", encoding="utf-8", newline="\n")
    return path


def _prepare(case, slug: str = SLUG, *, batch: str = BATCH, engine=_MISSING, models=None):
    sha = case.env.origin_ref(f"refs/heads/worktree-{slug}")
    if not sha:
        sha = case.env.make_lane(slug, f"{slug}.txt")
    assert re.fullmatch(r"[0-9a-f]{40}", sha)
    line = _line(slug, sha)
    _session(case, slug, line, models=models or _session_models())
    _launch(case, slug, batch, engine)
    return line, sha


def _session_models() -> str:
    return (
        "MODELS:\n"
        "  implement: requested=claude-sonnet-5-5/high served=claude-sonnet-5-5\n"
    )


def _wake(case, slug: str, line: str) -> Path:
    return leg.write_wake(case.wake_home, slug, line)


def _real_land_lane(**overrides):
    args = {
        "verdict_fn": pass_verdict,
        "record_suite_fn": stub_suite,
        "teardown_fn": lambda worktree: None,
    }
    args.update(overrides)
    return partial(ll.land_lane, **args)


def _stub(report, calls, *, phase_parameter=False, kwargs_only=False):
    if kwargs_only:
        def land(worktree, *, slug, batch, carry_file, timeout_s, interval_s, handback,
                 regen_cmds, **kwargs):
            calls.append(
                {
                    "worktree": worktree,
                    "slug": slug,
                    "batch": batch,
                    "carry_file": carry_file,
                    "timeout_s": timeout_s,
                    "interval_s": interval_s,
                    "handback": handback,
                    "regen_cmds": regen_cmds,
                    **kwargs,
                }
            )
            return report

        return land
    if phase_parameter:
        def explicit_phase(worktree, require_phase_receipts=False, **kwargs):
            return report

        def land(worktree, **kwargs):
            calls.append({"worktree": worktree, **kwargs})
            return explicit_phase(worktree, **kwargs)

        land.__signature__ = inspect.signature(explicit_phase)
        return land

    def land(worktree, **kwargs):
        calls.append({"worktree": worktree, **kwargs})
        return report

    return land


def _report(
    state="LANDED",
    exit_code=0,
    message="LANDED",
    *,
    sha="",
    main_sha="",
    conflicts=(),
    failing=(),
    steps=None,
):
    if steps is None:
        steps = [
            ("fetch", 0.1),
            ("merge", 0.2),
            ("regenerate", 0.3),
            ("carry", 0.4),
            ("push-integration", 0.5),
            ("poll", 0.6),
            ("land", 0.7),
            ("receipt", 0.8),
            ("teardown", 0.9),
        ]
    return ll.LandReport(
        state=state,
        exit_code=exit_code,
        message=message,
        sha=sha,
        steps=steps,
        conflicts=conflicts,
        failing=failing,
        main_sha=main_sha,
    )


def _one(case, slug, line, *, land_lane_fn, **overrides):
    kwargs = {
        "batch": BATCH,
        "worktree": case.env.worktree,
        "transport": case.transport,
        "receipts": case.receipts,
        "carry_file": case.env.carry,
        "handback_at": "2026-11-02T10:00:00Z",
        "state_dir": case.state,
        "clock_path": case.clock,
        "land_lane_fn": land_lane_fn,
    }
    kwargs.update(overrides)
    return land_on_handback.land_one(slug, line, **kwargs)


def _stop_path(case, slug=SLUG):
    return case.receipts / f"LAND-STOP-{slug.upper()}.json"


def _clock_rows(path: Path) -> list[dict]:
    return [json.loads(row) for row in path.read_text(encoding="utf-8").splitlines()]


def _hold_lock(path: Path, marker: Path, seconds: float = 2.0):
    path.parent.mkdir(parents=True, exist_ok=True)
    code = (
        "from filelock import FileLock; import pathlib, time; "
        f"p=pathlib.Path({str(path)!r}); "
        "lock=FileLock(str(p)); lock.acquire(); "
        f"pathlib.Path({str(marker)!r}).write_text('held'); "
        f"time.sleep({seconds!r}); lock.release()"
    )
    process = subprocess.Popen([sys.executable, "-c", code])
    deadline = time.monotonic() + 2
    while not marker.exists() and time.monotonic() < deadline:
        time.sleep(0.01)
    assert marker.exists(), "lock-holder subprocess did not acquire the file lock"
    return process


# --- a ----------------------------------------------------------------------------------------

def test_a_watch_lands_a_clean_lane_without_model_calls(case, tmp_path, monkeypatch):
    line, sha = _prepare(case)
    marker = model_cli_sandbox(tmp_path, monkeypatch)
    _wake(case, SLUG, line)

    result = land_on_handback.watch(
        batch=BATCH,
        worktree=case.env.worktree,
        transport=case.transport,
        wake_home=case.wake_home,
        receipts=case.receipts,
        carry_file=case.env.carry,
        state_dir=case.state,
        clock_path=case.clock,
        poll_s=0.05,
        max_wait_s=1,
        land_lane_fn=_real_land_lane(),
    )

    assert result == 0
    assert case.env.origin_ref("main") == case.env.origin_ref(f"refs/heads/{INTEGRATION}")
    assert sha in _git(case.env.origin, "rev-list", "main").splitlines()
    assert any(SLUG in row for row in case.env.ledger_on_main())
    assert not _stop_path(case).exists()
    assert len(_clock_rows(case.clock)) == 1
    assert not marker.exists() or marker.read_text(encoding="utf-8").strip() == ""


def test_a2_an_old_wake_with_no_cursor_is_still_landed(case, monkeypatch):
    line, _ = _prepare(case)
    wake = _wake(case, SLUG, line)
    old = time.time() - 4 * 60 * 60
    os.utime(wake, (old, old))
    cursor = land_on_handback.cursor_path(case.wake_home, BATCH)
    assert not cursor.exists()
    watch_wakes = leg.watch_wakes

    def checking_watch_wakes(home, **kwargs):
        assert kwargs["ledger"] == cursor
        assert cursor.is_file() and cursor.read_text(encoding="utf-8") == ""
        return watch_wakes(home, **kwargs)

    monkeypatch.setattr(leg, "watch_wakes", checking_watch_wakes)

    result = land_on_handback.watch(
        batch=BATCH,
        worktree=case.env.worktree,
        transport=case.transport,
        wake_home=case.wake_home,
        receipts=case.receipts,
        carry_file=case.env.carry,
        state_dir=case.state,
        clock_path=case.clock,
        poll_s=0.05,
        max_wait_s=1,
        land_lane_fn=_real_land_lane(),
    )

    assert result == 0
    assert cursor.is_file()
    assert len(_clock_rows(case.clock)) == 1


# --- b ----------------------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("state", "code", "message", "conflicts", "failing"),
    [
        ("CONFLICT", 2, "CONFLICT merging lane-a", ("shared.txt",), ()),
        ("RED", 3, "RED CI is not landable", (), ("test_bad",)),
        ("BASE-MOVED", 4, "BASE-MOVED while CI ran", (), ()),
        (
            "REFUSED",
            5,
            "REFUSED [phase-receipts]: missing LANE-lane-a round directory",
            (),
            (),
        ),
    ],
)
def test_b_a_stop_writes_evidence_once_and_emits_one_question(
    case, capsys, monkeypatch, state, code, message, conflicts, failing
):
    line, sha = _prepare(case, "lane-a")
    later, _ = _prepare(case, "lane-z")
    _wake(case, "lane-a", line)
    _wake(case, "lane-z", later)
    marker = model_cli_sandbox(case.tmp_path, monkeypatch)
    report = _report(
        state,
        code,
        message,
        sha=sha,
        conflicts=conflicts,
        failing=failing,
    )
    calls = []

    result = land_on_handback.watch(
        batch=BATCH,
        worktree=case.env.worktree,
        transport=case.transport,
        wake_home=case.wake_home,
        receipts=case.receipts,
        carry_file=case.env.carry,
        state_dir=case.state,
        clock_path=case.clock,
        poll_s=0.05,
        max_wait_s=1,
        land_lane_fn=_stub(report, calls),
    )

    assert result == code
    assert len(calls) == 1
    stop = json.loads(_stop_path(case).read_text(encoding="utf-8"))
    assert set(stop) == {
        "slug",
        "batch",
        "sha",
        "state",
        "exit_code",
        "message",
        "conflicts",
        "failing",
        "main_sha",
        "at",
    }
    assert stop["sha"] == sha and stop["state"] == state
    assert stop["exit_code"] == code
    assert stop["conflicts"] == list(conflicts)
    assert stop["failing"] == list(failing)
    cursor = land_on_handback.cursor_path(case.wake_home, BATCH)
    assert cursor.is_file() and cursor.read_text(encoding="utf-8") == ""
    question = capsys.readouterr().out.splitlines()
    assert len(question) == 1
    assert re.match(
        rf"^QUESTION land-on-handback {SLUG} \d\d:\d\d: {re.escape(state)} exit {code} - ",
        question[0],
    )
    assert not marker.exists() or marker.read_text(encoding="utf-8").strip() == ""


def test_b_watch_leaves_stopped_wake_unrecorded_and_does_not_process_later_wakes(
    case, capsys
):
    line, sha = _prepare(case, "lane-a")
    later, _ = _prepare(case, "lane-z")
    _wake(case, "lane-a", line)
    _wake(case, "lane-z", later)
    calls = []
    report = _report("REFUSED", 5, "REFUSED stage-receipt refusal", sha=sha)

    result = land_on_handback.watch(
        batch=BATCH,
        worktree=case.env.worktree,
        transport=case.transport,
        wake_home=case.wake_home,
        receipts=case.receipts,
        carry_file=case.env.carry,
        state_dir=case.state,
        clock_path=case.clock,
        poll_s=0.05,
        max_wait_s=1,
        land_lane_fn=_stub(report, calls),
    )

    cursor = land_on_handback.cursor_path(case.wake_home, BATCH)
    assert result == 5
    assert cursor.is_file() and cursor.read_text(encoding="utf-8") == ""
    assert len(calls) == 1
    assert _stop_path(case).is_file()
    assert capsys.readouterr().out.count("QUESTION land-on-handback") == 1


@pytest.mark.parametrize("kind, expected", [("conflict", "CONFLICT"), ("red", "RED"),
                                             ("base-moved", "BASE-MOVED"), ("refusal", "REFUSED")])
def test_b_real_land_lane_refusals_are_passed_through(case, kind, expected):
    batch = BATCH
    if kind == "conflict":
        sha = case.env.make_conflicting_lane(SLUG)
        line = _line(SLUG, sha)
        _session(case, SLUG, line)
        _launch(case, SLUG)
        land_fn = _real_land_lane()
    else:
        if kind == "refusal":
            batch = "E3.0"
        line, sha = _prepare(case, batch=batch)
        if kind == "red":
            def red_verdict(_sha, **kwargs):
                return SimpleNamespace(
                    state="FAIL",
                    missing_contexts=(),
                    reason="red CI",
                    newly_failing=("test_bad",),
                    new_tests=(),
                    jobs=(),
                )

            land_fn = _real_land_lane(verdict_fn=red_verdict)
        elif kind == "base-moved":
            def moving_verdict(_sha, **kwargs):
                case.env.advance_main(name="race.txt", text="raced\n")
                return pass_verdict(_sha, **kwargs)

            land_fn = _real_land_lane(verdict_fn=moving_verdict)
        else:
            _session(case, SLUG, line, models="MODELS:\n")
            land_fn = _real_land_lane()

    outcome = _one(case, SLUG, line, batch=batch, land_lane_fn=land_fn)

    assert outcome.state == expected
    assert outcome.exit_code in (2, 3, 4, 5)
    assert outcome.report is not None
    assert _stop_path(case).is_file()
    if kind == "conflict":
        assert case.env.status() == ""
        assert case.env.head() == case.env.origin_ref("main")
    elif kind == "red":
        assert outcome.report.failing == ("test_bad",)


# --- c ----------------------------------------------------------------------------------------

def test_c_remote_origin_requires_an_explicit_integrator_statement(case):
    line, _ = _prepare(case)
    _git(case.env.worktree, "remote", "set-url", "origin", "file:///not-a-local-directory")
    calls = []

    outcome = _one(case, SLUG, line, land_lane_fn=_stub(_report(), calls))

    assert outcome.state == "NEEDS-INTEGRATOR-STATEMENT"
    assert outcome.exit_code == 5 and not outcome.recorded
    assert calls == [] and not _stop_path(case).exists()


@pytest.mark.parametrize("context", ["branch", "harness-lane", "worktree"])
def test_c_context_mismatches_refuse_before_landing(case, monkeypatch, context):
    line, _ = _prepare(case)
    options = {}
    if context == "branch":
        _git(case.env.worktree, "checkout", "-b", "worktree-some-lane")
    elif context == "harness-lane":
        monkeypatch.setenv("HARNESS_LANE", "some-other-lane")
    else:
        other = case.tmp_path / ".claude" / "worktrees" / SLUG
        other.parent.mkdir(parents=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(case.env.worktree),
                "worktree",
                "add",
                "--detach",
                str(other),
                "origin/main",
            ],
            check=True,
            capture_output=True,
        )
        options["worktree"] = other
    calls = []
    outcome = _one(case, SLUG, line, land_lane_fn=_stub(_report(), calls), **options)

    assert outcome.state == "LANE-CONTEXT" and outcome.exit_code == 5
    assert calls == [] and not _stop_path(case).exists()


def test_c_integrator_flag_does_not_assert_itself_by_default(case):
    line, _ = _prepare(case)
    # a file:// URL of the REAL origin: land_lane._origin_is_remote calls it remote, yet the
    # tip check (iv) can still fetch from it
    _git(case.env.worktree, "remote", "set-url", "origin", case.env.origin.as_uri())
    calls = []

    outcome = _one(
        case,
        SLUG,
        line,
        land_lane_fn=_stub(_report(), calls),
        integrator=True,
    )

    assert outcome.state == "LANDED" and outcome.exit_code == 0
    assert len(calls) == 1
    assert inspect.signature(land_on_handback.land_one).parameters["integrator"].default is False


def test_c_live_lock_returns_busy_without_calling_the_landing_function(case):
    line, _ = _prepare(case)
    lock = case.state / land_on_handback.LOCK_NAME
    holder = _hold_lock(lock, case.tmp_path / "lock-held", seconds=2)
    calls = []
    try:
        outcome = _one(
            case,
            SLUG,
            line,
            land_lane_fn=_stub(_report(), calls),
            lock_wait_s=0,
        )
    finally:
        holder.terminate()
        holder.wait(timeout=3)

    assert outcome.state == "LANDER-BUSY" and outcome.exit_code == 5
    assert calls == []
    landed = _one(case, SLUG, line, land_lane_fn=_stub(_report(), calls))
    assert landed.state == "LANDED" and landed.exit_code == 0
    assert len(calls) == 1


def test_c2_once_waits_for_a_live_lock_then_lands(case):
    line, _ = _prepare(case, "lane-b")
    holder = _hold_lock(
        case.state / land_on_handback.LOCK_NAME,
        case.tmp_path / "lock-held",
        seconds=2,
    )
    calls = []
    stub = _stub(_report(), calls)
    try:
        outcome = land_on_handback.once(
            "lane-b",
            batch=BATCH,
            worktree=case.env.worktree,
            transport=case.transport,
            receipts=case.receipts,
            carry_file=case.env.carry,
            handback_line=line,
            handback_at="2026-11-02T10:00:00Z",
            wake_home=case.wake_home,
            state_dir=case.state,
            clock_path=case.clock,
            lock_wait_s=30,
            land_lane_fn=stub,
        )
    finally:
        holder.terminate()
        holder.wait(timeout=3)

    assert outcome == 0
    assert len(calls) == 1


# --- d ----------------------------------------------------------------------------------------

def test_d_call_uses_only_the_landing_allowlist_and_default_regeneration(case):
    line, _ = _prepare(case)
    calls = []
    outcome = _one(case, SLUG, line, land_lane_fn=_stub(_report(), calls))

    assert outcome.exit_code == 0
    call = calls[0]
    allowed = {
        "slug",
        "batch",
        "carry_file",
        "timeout_s",
        "interval_s",
        "handback",
        "regen_cmds",
        "require_phase_receipts",
    }
    assert set(call) - {"worktree"} <= allowed
    assert call["handback"] == case.transport / "to-browser" / f"SESSION-{SLUG}.md"
    assert call["regen_cmds"] == ll.default_regen_cmds(case.env.worktree)
    assert call["timeout_s"] == ll.DEFAULT_TIMEOUT_S
    assert call["interval_s"] == ll.DEFAULT_INTERVAL_S
    assert not {
        "operator_act",
        "ratification",
        "message",
        "lane_ref",
        "verdict_fn",
        "record_suite_fn",
        "regenerate_fn",
        "teardown_fn",
        "git",
        "land_fn",
    } & set(call)


def test_d_signature_defaults_match_land_lane_and_have_no_gate_overrides():
    parameters = inspect.signature(land_on_handback.land_one).parameters
    assert parameters["land_lane_fn"].default is land_on_handback.DEFAULT_LAND_FN
    assert parameters["timeout_s"].default == ll.DEFAULT_TIMEOUT_S
    assert parameters["interval_s"].default == ll.DEFAULT_INTERVAL_S
    for name in ("operator_act", "ratification", "message", "lane_ref"):
        assert name not in parameters
    for name in ("receipts", "carry_file", "handback_at", "clock_path"):
        assert parameters[name].default is None
    landing_parameters = inspect.signature(ll.land_lane).parameters
    for name in (
        "lane_ref",
        "message",
        "operator_act",
        "ratification",
        "verdict_fn",
        "record_suite_fn",
        "regenerate_fn",
        "teardown_fn",
        "git",
        "land_fn",
    ):
        assert landing_parameters[name].default is None


def test_d_ast_has_no_second_landing_path_or_model_or_wake_writer():
    source_path = _REPO / "scripts" / "land_on_handback.py"
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    attrs = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)}
    strings = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }

    assert "write_wake" not in names | attrs | strings
    assert "hand_back_on_accept" not in names | attrs | strings
    assert "merge_path" not in names | attrs
    assert "--no-verify" not in strings
    assert not any(name in strings for name in ("claude", "codex", "copilot"))
    assert not any(
        isinstance(node, ast.Call)
        and any(
            isinstance(arg, ast.Constant)
            and isinstance(arg.value, str)
            and arg.value in {"push", "git push"}
            for arg in ast.walk(node)
        )
        for node in ast.walk(tree)
    )
    assert "refs/heads/main" not in strings


def test_d_cli_help_and_verbs_have_no_gate_override_options():
    runner = CliRunner()
    cli = land_on_handback.cli
    assert runner.invoke(cli, ["--help"]).exit_code == 0
    forbidden = (
        "--operator-act",
        "--ratification",
        "--message",
        "--lane-ref",
        "--regen-cmd",
        "--verdict",
    )
    for verb in ("once", "watch", "clock"):
        help_result = runner.invoke(cli, [verb, "--help"])
        assert help_result.exit_code == 0
        assert not any(option in help_result.output for option in forbidden)


def test_d_default_land_function_is_land_lane():
    assert land_on_handback.DEFAULT_LAND_FN is ll.land_lane


@pytest.mark.parametrize(
    "option",
    ["--operator-act", "--ratification", "--message", "--lane-ref", "--regen-cmd", "--verdict"],
)
def test_d_cli_rejects_each_gate_override_option(option):
    result = CliRunner().invoke(land_on_handback.cli, ["once", option, "value"])
    assert result.exit_code == 2
    assert "No such option" in result.output


# --- e ----------------------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("row", "expected", "exit_code", "recorded"),
    [
        ("unparsed", "HANDBACK-UNPARSED", 5, False),
        ("branch", "HANDBACK-BRANCH", 5, False),
        ("slug", "HANDBACK-SLUG", 5, False),
        ("file", "HANDBACK-FILE", 5, False),
        ("stale", "STALE-HANDBACK", 5, False),
        ("missing-receipt", "NO-LAUNCH-RECEIPT", 5, False),
        ("receipts-conflict", "RECEIPTS-CONFLICT", 5, False),
        ("other-batch", "NOT-THIS-BATCH", 0, True),
        ("already-landed", "ALREADY-LANDED", 0, True),
    ],
)
def test_e_handback_and_receipt_rows_refuse_or_skip_before_land(
    case, monkeypatch, row, expected, exit_code, recorded
):
    line, sha = _prepare(case)
    calls = []
    stub = _stub(_report(), calls)
    call_slug = SLUG
    if row == "unparsed":
        line = "not a handback"
    elif row == "branch":
        line = _line(SLUG, sha, branch="worktree-another")
    elif row == "slug":
        call_slug = "bad/slug"
        line = _line(call_slug, sha)
    elif row == "file":
        (case.transport / "to-browser" / f"SESSION-{SLUG}.md").unlink()
    elif row == "stale":
        old_sha = sha
        new_sha = case.env.make_lane(SLUG, "lane_a.txt", text="newer lane\n")
        assert new_sha != old_sha
    elif row == "missing-receipt":
        (case.receipts / f"LAUNCH-{SLUG.upper()}.json").unlink()
    elif row == "receipts-conflict":
        monkeypatch.setenv(
            "HARNESS_RECEIPTS_DIR", str(case.tmp_path / "different-receipts")
        )
    elif row == "other-batch":
        _launch(case, SLUG, "E2.0")
    elif row == "already-landed":
        _git(case.env.seed, "fetch", "origin")
        _git(case.env.seed, "merge", "--no-ff", f"origin/worktree-{SLUG}", "-m", "land lane")
        _git(case.env.seed, "push", "origin", "main")

    outcome = _one(case, call_slug, line, land_lane_fn=stub)

    assert outcome.state == expected and outcome.exit_code == exit_code
    assert outcome.recorded is recorded
    assert calls == []


def test_e_session_handback_is_passed_and_receipts_env_is_scoped(case, monkeypatch):
    line, _ = _prepare(case)
    monkeypatch.delenv("HARNESS_RECEIPTS_DIR", raising=False)
    calls = []

    def stub(worktree, **kwargs):
        assert os.environ["HARNESS_RECEIPTS_DIR"] == str(case.receipts)
        calls.append(kwargs)
        return _report()

    outcome = _one(case, SLUG, line, land_lane_fn=stub)

    assert outcome.exit_code == 0
    assert calls[0]["handback"] == case.transport / "to-browser" / f"SESSION-{SLUG}.md"
    assert "HARNESS_RECEIPTS_DIR" not in os.environ


def test_e_receipts_conflict_refuses_before_landing(case, monkeypatch):
    line, _ = _prepare(case)
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(case.tmp_path / "different-receipts"))
    calls = []

    outcome = _one(case, SLUG, line, land_lane_fn=_stub(_report(), calls))

    assert outcome.state == "RECEIPTS-CONFLICT" and outcome.exit_code == 5
    assert calls == [] and not _stop_path(case).exists()


def test_e2_e3_call_uses_session_handback_and_restores_receipts_env(case, monkeypatch):
    line, _ = _prepare(case, batch="E3.0")
    monkeypatch.delenv("HARNESS_RECEIPTS_DIR", raising=False)
    calls = []

    def stub(worktree, **kwargs):
        assert os.environ["HARNESS_RECEIPTS_DIR"] == str(case.receipts)
        calls.append(kwargs)
        return _report()

    outcome = _one(case, SLUG, line, batch="E3.0", land_lane_fn=stub)

    assert outcome.exit_code == 0
    assert calls[0]["handback"] == case.transport / "to-browser" / f"SESSION-{SLUG}.md"
    assert "HARNESS_RECEIPTS_DIR" not in os.environ


# --- f ----------------------------------------------------------------------------------------

def test_f_land_seen_cursor_is_independent_of_two_seat_monitors(case):
    line, _ = _prepare(case)
    _wake(case, SLUG, line)
    seen_by_lander = []

    def landed(worktree, **kwargs):
        seen_by_lander.append(kwargs["slug"])
        return _report()

    result = land_on_handback.watch(
        batch=BATCH,
        worktree=case.env.worktree,
        transport=case.transport,
        wake_home=case.wake_home,
        receipts=case.receipts,
        carry_file=case.env.carry,
        state_dir=case.state,
        clock_path=case.clock,
        poll_s=0.05,
        max_wait_s=0.2,
        land_lane_fn=landed,
    )
    first, second = [], []
    seat_ledger_a = case.wake_home.with_name(case.wake_home.name + ".seat-a.watch-seen")
    seat_ledger_b = case.wake_home.with_name(case.wake_home.name + ".seat-b.watch-seen")
    leg.watch_wakes(case.wake_home, ledger=seat_ledger_a, poll_s=0, max_wait_s=0, emit=first.append)
    leg.watch_wakes(case.wake_home, ledger=seat_ledger_b, poll_s=0, max_wait_s=0, emit=second.append)

    assert result == 0
    assert seen_by_lander == [SLUG]
    assert len(first) == len(second) == 1
    assert first == second


def test_f_restart_does_not_land_a_recorded_wake_twice(case):
    line, _ = _prepare(case)
    _wake(case, SLUG, line)
    calls = []
    stub = _stub(_report(), calls)
    args = dict(
        batch=BATCH,
        worktree=case.env.worktree,
        transport=case.transport,
        wake_home=case.wake_home,
        receipts=case.receipts,
        carry_file=case.env.carry,
        state_dir=case.state,
        clock_path=case.clock,
        poll_s=0.05,
        max_wait_s=0.1,
        land_lane_fn=stub,
    )

    assert land_on_handback.watch(**args) == 0
    assert land_on_handback.watch(**args) == 0
    assert len(calls) == 1
    assert len(_clock_rows(case.clock)) == 1


def test_f_dry_run_prints_checks_without_lock_clock_receipt_or_ref_changes(case, capsys):
    line, _ = _prepare(case)
    before_origin = case.env.refs()
    before_worktree = _git(
        case.env.worktree, "for-each-ref", "--format=%(refname) %(objectname)"
    )

    outcome = _one(case, SLUG, line, land_lane_fn=_stub(_report(), []), dry_run=True)

    printed = capsys.readouterr().out.splitlines()
    assert outcome.exit_code == 0 and outcome.lines
    assert printed[: len(ll.plan(SLUG, BATCH))] == ll.plan(SLUG, BATCH)
    for check in ("(ii)", "(iii)", "(iv)", "(v)", "(vi)", "(vii)"):
        assert any(line.startswith(f"check {check} ") for line in printed)
    assert any("check (vi)" in line and "not evaluated in dry-run" in line for line in printed)
    assert any(line == "engine: model" for line in printed)
    assert not case.state.exists() or not list(case.state.iterdir())
    assert not case.clock.exists()
    assert {path.name for path in case.receipts.iterdir()} == {f"LAUNCH-{SLUG.upper()}.json"}
    assert case.env.refs() == before_origin
    assert _git(case.env.worktree, "for-each-ref", "--format=%(refname) %(objectname)") == before_worktree


def test_f_once_reads_the_last_handback_from_the_session_file(case):
    line, _ = _prepare(case)
    calls = []

    result = land_on_handback.once(
        SLUG,
        batch=BATCH,
        worktree=case.env.worktree,
        transport=case.transport,
        receipts=case.receipts,
        carry_file=case.env.carry,
        wake_home=case.wake_home,
        state_dir=case.state,
        clock_path=case.clock,
        land_lane_fn=_stub(_report(), calls),
    )

    assert result == 0
    assert len(calls) == 1
    assert calls[0]["handback"] == case.transport / "to-browser" / f"SESSION-{SLUG}.md"
    assert line in calls[0]["handback"].read_text(encoding="utf-8")


def test_f_cli_dry_run_clock_and_preflight_refusal(case):
    line, _ = _prepare(case)
    runner = CliRunner()
    common = [
        "--lane",
        SLUG,
        "--batch",
        BATCH,
        "--worktree",
        str(case.env.worktree),
        "--transport",
        str(case.transport),
        "--receipts",
        str(case.receipts),
        "--carry-file",
        str(case.env.carry),
        "--wake-home",
        str(case.wake_home),
        "--clock",
        str(case.clock),
        "--state-dir",
        str(case.state),
    ]

    dry = runner.invoke(land_on_handback.cli, ["once", *common, "--dry-run"])
    assert dry.exit_code == 0, dry.output
    assert "check (vi)" in dry.output and "not evaluated in dry-run" in dry.output
    assert not case.clock.exists() and not case.state.exists()

    clock = runner.invoke(
        land_on_handback.cli,
        ["clock", "--clock", str(case.clock), "--last", "10"],
    )
    assert clock.exit_code == 0
    assert "merge-clock: n=0 landed of 0 lines (last 10)" in clock.output

    (case.transport / "to-browser" / f"SESSION-{SLUG}.md").unlink()
    refused = runner.invoke(land_on_handback.cli, ["once", *common])
    assert refused.exit_code == 5
    assert "HANDBACK-FILE" in refused.output
    assert line


def test_f_two_batch_watchers_do_not_consume_each_others_wake(case):
    line, _ = _prepare(case, "lane-b", batch="E3.1")
    _wake(case, "lane-b", line)
    calls_a, calls_b = [], []

    def stub_a(worktree, **kwargs):
        calls_a.append(kwargs)
        return _report()

    def stub_b(worktree, **kwargs):
        calls_b.append(kwargs)
        return _report()

    common = dict(
        worktree=case.env.worktree,
        transport=case.transport,
        wake_home=case.wake_home,
        receipts=case.receipts,
        carry_file=case.env.carry,
        state_dir=case.state,
        clock_path=case.clock,
        poll_s=0.05,
        max_wait_s=0.1,
    )
    result_a = land_on_handback.watch(batch=BATCH, land_lane_fn=stub_a, **common)
    result_b = land_on_handback.watch(batch="E3.1", land_lane_fn=stub_b, **common)

    assert result_a == 0 and result_b == 0
    assert calls_a == [] and len(calls_b) == 1


def test_f_unresolved_stop_blocks_replay_until_operator_removes_stop_receipt(case):
    line, sha = _prepare(case)
    _git(case.env.seed, "fetch", "origin")
    _git(case.env.seed, "merge", "--no-ff", f"origin/worktree-{SLUG}", "-m", "land lane")
    _git(case.env.seed, "push", "origin", "main")
    _wake(case, SLUG, line)
    _stop_path(case).write_text(
        json.dumps({"slug": SLUG, "batch": BATCH, "sha": sha, "state": "REFUSED"}),
        encoding="utf-8",
    )
    calls = []

    result = land_on_handback.watch(
        batch=BATCH,
        worktree=case.env.worktree,
        transport=case.transport,
        wake_home=case.wake_home,
        receipts=case.receipts,
        carry_file=case.env.carry,
        state_dir=case.state,
        clock_path=case.clock,
        poll_s=0.05,
        max_wait_s=1,
        land_lane_fn=_stub(_report(), calls),
    )

    assert result == 5
    assert not calls
    assert land_on_handback.cursor_path(case.wake_home, BATCH).read_text(encoding="utf-8") == ""
    _stop_path(case).unlink()
    outcome = _one(case, SLUG, line, land_lane_fn=_stub(_report(), calls))
    assert outcome.state == "ALREADY-LANDED" and outcome.exit_code == 0
    assert outcome.recorded and calls == []


# --- g ----------------------------------------------------------------------------------------

@pytest.mark.parametrize("engine", [_MISSING, "model", "unexpected"])
def test_g1_model_engine_omits_phase_receipt_keyword(case, engine):
    line, _ = _prepare(case, engine=engine)
    calls = []
    stub = _stub(_report(), calls, phase_parameter=True)

    outcome = _one(case, SLUG, line, land_lane_fn=stub)

    assert outcome.exit_code == 0
    assert len(calls) == 1
    assert "require_phase_receipts" not in calls[0]


@pytest.mark.parametrize("engine", [_MISSING, "model"])
def test_g2_model_engine_lands_with_stub_without_phase_parameter(case, engine):
    line, _ = _prepare(case, engine=engine)
    calls = []

    outcome = _one(case, SLUG, line, land_lane_fn=_stub(_report(), calls))

    assert outcome.state == "LANDED" and outcome.exit_code == 0
    assert len(calls) == 1 and "require_phase_receipts" not in calls[0]
    assert not (case.receipts / f"LANE-{SLUG}").exists()


def test_g3_conductor_passes_gate_and_enriches_refusal_with_round_path(case, capsys):
    line, _ = _prepare(case, engine="conductor")
    calls = []
    report = _report("REFUSED", 5, "REFUSED [phase-receipts]: no receipt", sha="a" * 40)

    outcome = _one(
        case,
        SLUG,
        line,
        land_lane_fn=_stub(report, calls, phase_parameter=True),
    )

    round_dir = str(case.receipts / f"LANE-{SLUG}")
    assert outcome.state == "REFUSED" and outcome.exit_code == 5
    assert calls[0]["require_phase_receipts"] is True
    assert round_dir in outcome.message
    assert round_dir in json.loads(_stop_path(case).read_text(encoding="utf-8"))["message"]
    assert capsys.readouterr().out.count("QUESTION land-on-handback") == 1


@pytest.mark.parametrize("stub_kind", ["without-parameter", "kwargs-only"])
def test_g4_conductor_fails_closed_when_named_gate_parameter_is_missing(
    case, capsys, monkeypatch, stub_kind
):
    line, sha = _prepare(case, engine="conductor")
    _wake(case, SLUG, line)
    marker = model_cli_sandbox(case.tmp_path, monkeypatch)
    calls = []
    stub = _stub(
        _report(sha=sha),
        calls,
        kwargs_only=stub_kind == "kwargs-only",
    )

    result = land_on_handback.watch(
        batch=BATCH,
        worktree=case.env.worktree,
        transport=case.transport,
        wake_home=case.wake_home,
        receipts=case.receipts,
        carry_file=case.env.carry,
        state_dir=case.state,
        clock_path=case.clock,
        poll_s=0.05,
        max_wait_s=1,
        land_lane_fn=stub,
    )

    round_dir = str(case.receipts / f"LANE-{SLUG}")
    stop = json.loads(_stop_path(case).read_text(encoding="utf-8"))
    assert result == 5
    assert stop["state"] == "ENGINE-GATE-MISSING" and stop["exit_code"] == 5
    assert "land_lane lacks require_phase_receipts (lane G not landed)" in stop["message"]
    assert round_dir in stop["message"]
    assert calls == []
    cursor = land_on_handback.cursor_path(case.wake_home, BATCH)
    assert cursor.is_file() and cursor.read_text(encoding="utf-8") == ""
    assert not case.clock.exists()
    assert capsys.readouterr().out.count("QUESTION land-on-handback") == 1
    assert not marker.exists() or marker.read_text(encoding="utf-8").strip() == ""


def test_g5_real_land_lane_conductor_gate_is_checked_against_its_signature(case):
    line, _ = _prepare(case, engine="conductor")
    phase_parameter = "require_phase_receipts" in inspect.signature(ll.land_lane).parameters

    outcome = _one(
        case,
        SLUG,
        line,
        land_lane_fn=_real_land_lane(),
    )

    assert outcome.exit_code == 5
    if not phase_parameter:
        assert outcome.state == "ENGINE-GATE-MISSING"
    else:
        assert outcome.state == "REFUSED"
        assert str(case.receipts / f"LANE-{SLUG}") in outcome.message


# --- m ----------------------------------------------------------------------------------------

def test_m_clock_line_has_exact_schema_and_main_timing_invariant(case):
    line, sha = _prepare(case)
    calls = []
    values = iter([1793613600.0, 1793613610.0])

    def now():
        nonlocal now_calls
        now_calls += 1
        return next(values)

    now_calls = 0
    report = _report(sha=sha, main_sha="b" * 40)
    outcome = _one(case, SLUG, line, land_lane_fn=_stub(report, calls), now=now)
    clock = _clock_rows(case.clock)[0]
    expected_keys = {
        "schema",
        "slug",
        "batch",
        "lane_sha",
        "main_sha",
        "state",
        "exit_code",
        "handback_at",
        "pickup_at",
        "main_at",
        "handback_to_main_s",
        "stages",
        "after_main",
        "unmeasured",
        "land_is_proxy",
    }

    assert outcome.state == "LANDED"
    assert now_calls == 2
    assert set(clock) == expected_keys
    assert clock["schema"] == land_on_handback.CLOCK_SCHEMA == "merge-clock/1"
    assert clock["lane_sha"] == sha
    assert clock["land_is_proxy"] is True
    assert set(clock["stages"]) == {
        "wait",
        "fetch",
        "merge",
        "regenerate",
        "carry",
        "push-integration",
        "poll",
        "land",
        "unattributed",
    }
    assert set(clock["after_main"]) == {"receipt", "teardown"}
    assert clock["main_sha"] == "b" * 40
    assert clock["handback_at"].endswith("Z")
    assert clock["pickup_at"].endswith("Z")
    assert clock["main_at"].endswith("Z")
    measured = (
        clock["stages"]["wait"]
        + sum(
            clock["stages"][name]
            for name in (
                "fetch",
                "merge",
                "regenerate",
                "carry",
                "push-integration",
                "poll",
                "land",
            )
        )
        + clock["stages"]["unattributed"]
    )
    assert abs(measured - clock["handback_to_main_s"]) <= 1


@pytest.mark.parametrize(("state", "code"), [("CONFLICT", 2), ("RED", 3), ("BASE-MOVED", 4)])
def test_m_pre_main_stop_has_null_main_fields_and_names_unmeasured(case, state, code):
    line, sha = _prepare(case)
    report = _report(state, code, state, sha=sha, steps=[("fetch", 0.2), ("merge", 0.3)])
    outcome = _one(case, SLUG, line, land_lane_fn=_stub(report, []))
    clock = _clock_rows(case.clock)[0]

    assert outcome.state == state
    assert clock["main_at"] is None
    assert clock["main_sha"] is None
    assert clock["handback_to_main_s"] is None
    assert clock["after_main"] is None
    assert {"main_at", "main_sha", "handback_to_main_s", "after_main"} <= set(
        clock["unmeasured"]
    )
    assert clock["stages"]["unattributed"] is None
    assert "stages.unattributed" in clock["unmeasured"]


def test_m_carry_file_refusal_records_main_and_after_main_measurements(case):
    line, sha = _prepare(case)
    report = _report(
        "REFUSED",
        5,
        f"LANDED {sha[:12]} on main but carry file could not be emptied",
        sha=sha,
        main_sha="c" * 40,
        steps=[
            ("fetch", 0.1),
            ("merge", 0.2),
            ("regenerate", 0.3),
            ("carry", 0.4),
            ("push-integration", 0.5),
            ("poll", 0.6),
            ("land", 0.7),
            ("receipt", 0.8),
        ],
    )
    _one(case, SLUG, line, land_lane_fn=_stub(report, []))
    clock = _clock_rows(case.clock)[0]

    assert clock["state"] == "REFUSED"
    assert clock["main_at"] is not None
    assert clock["main_sha"] == "c" * 40
    assert clock["handback_to_main_s"] is not None
    assert clock["after_main"]["teardown"] is None
    assert "after_main.teardown" in clock["unmeasured"]


def test_m2_unjudged_sha_refusal_keeps_main_measurements_null(case):
    line, sha = _prepare(case)
    report = _report(
        "REFUSED",
        5,
        "unjudged sha on main: remote differs from the judged sha",
        sha=sha,
        main_sha="d" * 40,
    )
    _one(case, SLUG, line, land_lane_fn=_stub(report, []))
    clock = _clock_rows(case.clock)[0]

    assert clock["main_at"] is None
    assert clock["main_sha"] is None
    assert clock["handback_to_main_s"] is None
    assert {"main_at", "main_sha", "handback_to_main_s"} <= set(clock["unmeasured"])


def test_n_missing_handback_time_is_unmeasured_not_zero(case, monkeypatch):
    line, sha = _prepare(case)
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    report = _report(sha=sha, main_sha="b" * 40)

    _one(case, SLUG, line, land_lane_fn=_stub(report, []), handback_at=None)
    clock = _clock_rows(case.clock)[0]

    assert clock["handback_at"] is None
    assert clock["stages"]["wait"] is None
    assert clock["handback_to_main_s"] is None
    assert {"stages.wait", "handback_to_main_s"} <= set(clock["unmeasured"])


def test_n_unwritable_clock_emits_one_stderr_line_without_changing_landing(
    case, capsys
):
    line, sha = _prepare(case)
    bad_clock = case.tmp_path / "clock-is-directory"
    bad_clock.mkdir()
    calls = []
    report = _report(sha=sha, main_sha="b" * 40)

    outcome = _one(
        case,
        SLUG,
        line,
        land_lane_fn=_stub(report, calls),
        clock_path=bad_clock,
    )

    stderr = capsys.readouterr().err.splitlines()
    assert outcome.state == "LANDED" and outcome.exit_code == 0
    assert len(calls) == 1
    assert len(stderr) == 1
    assert "LANDED" in stderr[0] and "0" in stderr[0]


def test_n_pytest_without_explicit_clock_writes_nothing(case, monkeypatch):
    line, _ = _prepare(case)
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "test_land_on_handback::test_n")
    default_clock = _REPO / "logs" / "MERGE-CLOCK.jsonl"
    existed = default_clock.exists()
    outcome = _one(
        case,
        SLUG,
        line,
        land_lane_fn=_stub(_report(), []),
        clock_path=None,
    )

    assert outcome.exit_code == 0
    assert default_clock.exists() is existed


def test_n_only_literal_clock_path_is_gitignored():
    clock = subprocess.run(
        ["git", "check-ignore", "-q", "logs/MERGE-CLOCK.jsonl"],
        cwd=_REPO,
        check=False,
    )
    other = subprocess.run(
        ["git", "check-ignore", "-q", "logs/OTHER-FILE.jsonl"],
        cwd=_REPO,
        check=False,
    )
    detail = subprocess.run(
        ["git", "check-ignore", "-v", "logs/MERGE-CLOCK.jsonl"],
        cwd=_REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert clock.returncode == 0
    assert other.returncode == 1
    assert "logs/MERGE-CLOCK.jsonl" in detail.stdout
    assert not any(char in detail.stdout.split(":")[-1] for char in "*?[")
    ignore_lines = (_REPO / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ignore_lines.count("logs/MERGE-CLOCK.jsonl") == 1
    assert not any(char in "logs/MERGE-CLOCK.jsonl" for char in "*?[")


# --- o ----------------------------------------------------------------------------------------

def test_o_clock_report_uses_median_nearest_rank_p90_and_proxy_label(case):
    stages = {
        "wait": [1.0, 3.0],
        "fetch": [2.0, 4.0],
        "merge": [3.0, 5.0],
        "regenerate": [4.0, 6.0],
        "carry": [5.0, 7.0],
        "push-integration": [6.0, 8.0],
        "poll": [7.0, 9.0],
        "land": [8.0, 10.0],
        "unattributed": [9.0, 11.0],
    }
    records = []
    records.append(
        json.dumps(
            {
                "schema": "merge-clock/1",
                "state": "LANDED",
                "handback_to_main_s": 1000.0,
                "stages": {name: 100.0 for name in stages},
            }
        )
    )
    for index, value in enumerate((10.0, 30.0)):
        record = {
            "schema": "merge-clock/1",
            "state": "LANDED",
            "handback_to_main_s": value,
            "stages": {name: values[index] for name, values in stages.items()},
        }
        records.append(json.dumps(record))
    records.append(json.dumps({"schema": "merge-clock/1", "state": "RED"}))
    case.clock.write_text("\n".join(records) + "\n", encoding="utf-8", newline="\n")

    text = land_on_handback.clock_report(case.clock, 3)
    expected = [
        "merge-clock: n=2 landed of 3 lines (last 3)",
        "handback->main: median=20.0s p90=30.0s",
        "stage wait: median=2.0s p90=3.0s",
        "stage fetch: median=3.0s p90=4.0s",
        "stage merge: median=4.0s p90=5.0s",
        "stage regenerate: median=5.0s p90=6.0s",
        "stage carry: median=6.0s p90=7.0s",
        "stage push-integration: median=7.0s p90=8.0s",
        "stage poll: median=8.0s p90=9.0s",
        "stage land (proxy): median=9.0s p90=10.0s",
        "stage unattributed: median=10.0s p90=11.0s",
    ]

    assert text.splitlines() == expected


def test_o_clock_report_marks_unmeasured_and_empty_output(case):
    record = {
        "schema": "merge-clock/1",
        "state": "LANDED",
        "handback_to_main_s": None,
        "stages": {"wait": None, "fetch": 0.1},
    }
    case.clock.write_text(json.dumps(record) + "\n", encoding="utf-8")

    text = land_on_handback.clock_report(case.clock, 10)
    assert "merge-clock: n=1 landed of 1 lines (last 10)" in text.splitlines()
    assert "handback->main: UNMEASURED" in text.splitlines()
    assert "stage wait: UNMEASURED" in text.splitlines()
    assert "stage fetch: median=0.1s p90=0.1s" in text.splitlines()

    missing = case.tmp_path / "missing-clock.jsonl"
    assert land_on_handback.clock_report(missing, 10).splitlines() == [
        "merge-clock: n=0 landed of 0 lines (last 10)",
        "handback->main: UNMEASURED",
    ]
    empty = case.tmp_path / "empty-clock.jsonl"
    empty.write_text("", encoding="utf-8")
    assert land_on_handback.clock_report(empty, 10).splitlines() == [
        "merge-clock: n=0 landed of 0 lines (last 10)",
        "handback->main: UNMEASURED",
    ]


# --- w ----------------------------------------------------------------------------------------

def test_w_orphan_disposition_fate_and_non_edge_shape_are_pinned():
    disposition = gq.ORPHAN_DISPOSITIONS["scripts/land_on_handback.py"]
    assert len(disposition.reason) >= 20
    assert disposition.owner == "[#1859]"

    harness = yaml.safe_load((_REPO / "ecosystem" / "harness.yaml").read_text(encoding="utf-8"))
    fate = next(
        row for row in harness["fates"] if row["path"] == "scripts/land_on_handback.py"
    )
    assert str(fate["manual_until"]) == "2026-11-23"
    assert "C11" in fate["reason"] and "C13" in fate["reason"]
    assert not gq.is_edge_computation_shape(
        (_REPO / "scripts" / "land_on_handback.py").read_text(encoding="utf-8")
    )
