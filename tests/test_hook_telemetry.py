"""Tests for the [#529] `hook_run` + `blocker_fired` wiring in the three gate organs — lane L2,
contract STEP 4.

THE ORGANS ARE GATES FIRST AND INSTRUMENTS SECOND, and every case here is written from that
side. `block_ff_push` and `block_unanchored_push` are the two pre-push organs that fail CLOSED;
`block_commit_on_main` is the commit-time sibling. What telemetry may cost them is exactly
nothing:

  * **exit codes must not move** — 0 allow, 1 refuse, 2 internal error. A telemetry write that
    turned a refusal into an allow would be worse than no telemetry at all;
  * **stderr must stay byte-identical** — the existing suites assert stderr SUBSTRINGS, which
    survive extra output, so "no new line appeared" needs its own byte-equality assertion rather
    than trusting theirs. Expected to hold on the measured `logging.lastResort` behaviour (a
    hook configures no handler, so an `.info()` is silent); this test is what keeps it true if a
    host ever configures logging;
  * **a dead store must not change a verdict** — `safe_emit` swallows `sqlite3.Error`/`OSError`
    so a locked database on a shared machine cannot brick a push.

Driven as real subprocesses against real throwaway git repos, mirroring
`tests/test_block_ff_push.py` and `tests/test_adr85_integration_enforcement.py`, because the
question is what the ORGAN does when git runs it — not what a function returns when pytest calls
it. The store is pointed at `tmp_path` with `DEV_KNOWLEDGE_TELEMETRY_DB`, which is also the
sandbox seam being exercised: a hook that derived its path from `telemetry_emit._REPO_ROOT` would
write into the real repo from inside this suite.

`blocker_fired` fires at the REFUSAL return only. An internal error (exit 2) emits
`hook_run(outcome="error")` and NO `blocker_fired`: the push is refused, but by a crash rather
than by a policy, and conflating the two would inflate every "what did this gate refuse" count
with the gate's own bugs.
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

import block_commit_on_main as bcm
import block_ff_push as bfp

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
pytestmark = pytest.mark.slow  # real-git + subprocess spawns, per the #317 marker tier

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
_FF = _SCRIPTS / "block_ff_push.py"
_UNANCHORED = _SCRIPTS / "block_unanchored_push.py"
_ON_MAIN = _SCRIPTS / "block_commit_on_main.py"

_TELEMETRY_ENV = "DEV_KNOWLEDGE_TELEMETRY"
_DB_ENV = "DEV_KNOWLEDGE_TELEMETRY_DB"


# --- git tmp-repo helpers (mirror test_block_ff_push / test_adr85_integration_enforcement) ---

def _git(repo, *args):
    # errors="replace": a refusal's text carries an em-dash and comes back in the console
    # codepage on Windows; a strict utf-8 decode raises inside subprocess's reader thread.
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _rev(repo, ref="HEAD"):
    return _git(repo, "rev-parse", ref).stdout.strip()


def _commit(repo, msg, fname="f.txt", adate="2026-06-16T10:00:00"):
    (repo / fname).write_text(msg, encoding="utf-8")
    _git(repo, "add", "-A")
    env = {**os.environ, "GIT_AUTHOR_DATE": adate, "GIT_COMMITTER_DATE": adate}
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", msg], check=True,
                   capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)


def _repo_with_remote(tmp_path, name="r"):
    """A repo on `main`, already pushed to a fresh bare origin. Returns (repo, remote_sha)."""
    repo = tmp_path / name
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")
    (repo / "JOURNAL.md").write_text("# Journal\n\n", encoding="utf-8")
    # Root seed dated before the FF baseline -> always grandfathered.
    _commit(repo, "seed", fname="seed.txt", adate="2026-06-01T00:00:00")
    _git(repo, "branch", "-M", "main")
    bare = tmp_path / f"{name}-remote.git"
    bare.mkdir()
    _git(bare, "init", "--bare", "-q")
    _git(repo, "remote", "add", "origin", str(bare))
    _git(repo, "push", "-q", "origin", "main")
    return repo, _rev(repo, "main")


def _push_line(local_sha, remote_sha, ref="refs/heads/main"):
    return f"{ref} {local_sha} {ref} {remote_sha}\n"


def _invoke(script, repo, stdin_text="", db=None, telemetry=None):
    """Run an organ exactly as git would: a subprocess in `repo`, ref lines on stdin.

    PRE_COMMIT_* is scrubbed so a caller's stray env cannot leak into the stdin path, and both
    telemetry switches are scrubbed then set explicitly, so no case inherits the host's.
    """
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("PRE_COMMIT_") and k not in (_TELEMETRY_ENV, _DB_ENV)}
    if telemetry is not None:
        env[_TELEMETRY_ENV] = telemetry
    if db is not None:
        env[_DB_ENV] = str(db)
    return subprocess.run([sys.executable, str(script)], input=stdin_text, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", env=env, cwd=str(repo))


def _rows(db_path):
    if not Path(db_path).exists():
        return []
    with sqlite3.connect(str(db_path)) as conn:
        cur = conn.execute(
            "SELECT event_type, name, outcome, duration_ms, context_json FROM events ORDER BY id")
        return [dict(zip(("event_type", "name", "outcome", "duration_ms", "context_json"), r))
                for r in cur.fetchall()]


# --- the six scenarios: each organ, allowing and refusing ----------------------------------

def _ff_allow(tmp_path):
    """A --no-ff merge push: the sanctioned shape, so the FF gate allows it."""
    repo, remote_sha = _repo_with_remote(tmp_path)
    _git(repo, "checkout", "-q", "-b", "feat/z")
    _commit(repo, "feat: do z", fname="z.txt")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "--no-ff", "-q", "-m", "Merge feat/z --no-ff", "feat/z")
    return _FF, repo, _push_line(_rev(repo, "main"), remote_sha), 0


def _ff_refuse(tmp_path):
    """A direct commit on main: core-invariant #5's violation, so the FF gate refuses."""
    repo, remote_sha = _repo_with_remote(tmp_path)
    _commit(repo, "feat: oops direct on main", fname="a.txt")
    return _FF, repo, _push_line(_rev(repo, "main"), remote_sha), 1


def _unanchored_allow(tmp_path):
    """A feature-branch push: not this organ's business, so it allows."""
    repo, _ = _repo_with_remote(tmp_path)
    _git(repo, "checkout", "-q", "-b", "feat/x")
    _commit(repo, "feat: on a branch", fname="x.txt")
    line = _push_line(_rev(repo, "feat/x"), "0" * 40, ref="refs/heads/feat/x")
    return _UNANCHORED, repo, line, 0


def _unanchored_refuse(tmp_path):
    """A --no-ff merge onto main with no JOURNAL entry naming what it brings in."""
    repo, remote_sha = _repo_with_remote(tmp_path)
    _git(repo, "checkout", "-q", "-b", "feat/y")
    _commit(repo, "feat: unanchored work", fname="y.txt")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "--no-ff", "-q", "-m", "Merge feat/y --no-ff", "feat/y")
    return _UNANCHORED, repo, _push_line(_rev(repo, "main"), remote_sha), 1


def _on_main_allow(tmp_path):
    """HEAD on a feature branch: the commit-time gate allows."""
    repo, _ = _repo_with_remote(tmp_path)
    _git(repo, "checkout", "-q", "-b", "feat/w")
    return _ON_MAIN, repo, "", 0


def _on_main_refuse(tmp_path):
    """HEAD on main with no merge in progress: the commit-time gate refuses."""
    repo, _ = _repo_with_remote(tmp_path)
    return _ON_MAIN, repo, "", 1


_ALLOW = {"block-ff-push": _ff_allow,
          "block-unanchored-push": _unanchored_allow,
          "block-commit-on-main": _on_main_allow}
_REFUSE = {"block-ff-push": _ff_refuse,
           "block-unanchored-push": _unanchored_refuse,
           "block-commit-on-main": _on_main_refuse}
_ORGANS = sorted(_ALLOW)


# --- case 12: hook_run on every exit path -------------------------------------------------

@requires_git
@pytest.mark.parametrize("organ", _ORGANS)
@pytest.mark.parametrize("verdict", ["allow", "refuse"])
def test_hook_run_lands_on_every_exit_path(tmp_path, organ, verdict):
    """Six cells: three organs x {allow, refuse}. A gate that only records its refusals cannot
    answer the memo's actual question ("is this hook pure ceremony?") — that needs the FIRES
    count as much as the BLOCKS count."""
    db = tmp_path / "T.db"
    script, repo, stdin_text, expected = (_ALLOW if verdict == "allow" else _REFUSE)[organ](tmp_path)

    res = _invoke(script, repo, stdin_text, db=db, telemetry="1")

    assert res.returncode == expected, res.stderr
    hook_rows = [r for r in _rows(db) if r["event_type"] == "hook_run"]
    assert len(hook_rows) == 1, _rows(db)
    assert hook_rows[0]["name"] == organ
    assert hook_rows[0]["outcome"] == ("pass" if verdict == "allow" else "block")
    assert hook_rows[0]["duration_ms"] is not None


# --- case 13: blocker_fired on refusal ONLY -----------------------------------------------

@requires_git
@pytest.mark.parametrize("organ", _ORGANS)
def test_blocker_fired_lands_only_on_a_refusal_and_carries_a_reason(tmp_path, organ):
    db = tmp_path / "T.db"
    script, repo, stdin_text, expected = _REFUSE[organ](tmp_path)

    res = _invoke(script, repo, stdin_text, db=db, telemetry="1")

    assert res.returncode == 1, res.stderr
    blocked = [r for r in _rows(db) if r["event_type"] == "blocker_fired"]
    assert len(blocked) == 1
    assert blocked[0]["name"] == organ
    assert blocked[0]["outcome"] == "block"
    reason = json.loads(blocked[0]["context_json"])["reason"]
    assert reason and isinstance(reason, str)


@requires_git
@pytest.mark.parametrize("organ", _ORGANS)
def test_an_allow_fires_no_blocker(tmp_path, organ):
    db = tmp_path / "T.db"
    script, repo, stdin_text, expected = _ALLOW[organ](tmp_path)

    res = _invoke(script, repo, stdin_text, db=db, telemetry="1")

    assert res.returncode == 0, res.stderr
    assert [r for r in _rows(db) if r["event_type"] == "blocker_fired"] == []


# --- case 14: exit codes are unchanged ----------------------------------------------------

@requires_git
@pytest.mark.parametrize("organ", _ORGANS)
def test_exit_codes_do_not_move_with_telemetry_on(tmp_path, organ):
    """The same assertions the existing organ suites make, re-made with telemetry on. This is
    the property that makes the wiring safe to land on a gate that fails CLOSED."""
    for builder, expected in ((_ALLOW[organ], 0), (_REFUSE[organ], 1)):
        sub = tmp_path / f"{organ}-{expected}"
        sub.mkdir()
        script, repo, stdin_text, want = builder(sub)
        assert want == expected
        assert _invoke(script, repo, stdin_text, db=sub / "T.db",
                       telemetry="1").returncode == expected


def test_an_internal_error_is_recorded_as_error_and_still_refuses(tmp_path, monkeypatch):
    """Exit 2 is the fail-CLOSED path (ADR-85 amendment §A6). It emits `hook_run(error)` and NO
    `blocker_fired`: the push IS refused, but by a crash rather than by a policy, and conflating
    the two would inflate every "what did this gate refuse" count with the gate's own bugs.

    Driven in-process (as `test_adr85_integration_enforcement::test_t4` drives its error case)
    because forcing a genuine internal error through a subprocess would mean corrupting a repo,
    which tests the corruption rather than the organ."""
    db = tmp_path / "T.db"
    monkeypatch.setenv(_TELEMETRY_ENV, "1")
    monkeypatch.setenv(_DB_ENV, str(db))
    monkeypatch.setattr(bfp, "_read_stdin", lambda: (_ for _ in ()).throw(OSError("stdin gone")))

    assert bfp.main([]) == 2

    rows = _rows(db)
    assert [(r["event_type"], r["outcome"]) for r in rows] == [("hook_run", "error")]
    assert rows[0]["name"] == "block-ff-push"


# --- case 15: stderr is byte-identical with telemetry on vs off ---------------------------

@requires_git
@pytest.mark.parametrize("organ", _ORGANS)
def test_stderr_is_byte_identical_with_telemetry_on_and_off(tmp_path, organ):
    """ONE repo, invoked twice, so the two runs differ only in the switch — two repos would
    differ in their SHAs and the comparison would be vacuous. The organs are read-only, so a
    second invocation sees the same state as the first."""
    script, repo, stdin_text, expected = _REFUSE[organ](tmp_path)

    off = _invoke(script, repo, stdin_text)
    on = _invoke(script, repo, stdin_text, db=tmp_path / "T.db", telemetry="1")

    assert off.returncode == on.returncode == expected
    assert on.stderr == off.stderr
    assert on.stdout == off.stdout
    assert "telemetry: " not in on.stderr


# --- case 16: a dead store never changes a verdict ----------------------------------------

@requires_git
@pytest.mark.parametrize("organ", _ORGANS)
def test_an_unwritable_store_never_changes_the_verdict(tmp_path, organ):
    """`safe_emit` swallows `sqlite3.Error`/`OSError`. A locked database on a shared machine, or
    a read-only disk, must not turn a refusal into an allow — or an allow into a failed push."""
    blocker = tmp_path / "not-a-dir"
    blocker.write_text("x\n", encoding="utf-8")
    dead = blocker / "nested" / "T.db"

    for builder, expected in ((_ALLOW[organ], 0), (_REFUSE[organ], 1)):
        sub = tmp_path / f"{organ}-dead-{expected}"
        sub.mkdir()
        script, repo, stdin_text, want = builder(sub)
        res = _invoke(script, repo, stdin_text, db=dead, telemetry="1")
        assert res.returncode == expected, res.stderr


# --- case 17: off by default ---------------------------------------------------------------

@requires_git
@pytest.mark.parametrize("organ", _ORGANS)
def test_telemetry_is_off_by_default_for_the_hooks(tmp_path, organ):
    """No env var, no rows, and no store file at all. The hooks have no click layer, so the env
    switch is the ONLY way emission is ever on for them — and it defaults off, exactly as the
    click flag does for `audit.py health`. Flipping either default is a separate ruling."""
    db = tmp_path / "T.db"
    script, repo, stdin_text, expected = _REFUSE[organ](tmp_path)

    res = _invoke(script, repo, stdin_text, db=db)  # db pointed at, switch NOT set

    assert res.returncode == expected, res.stderr
    assert not db.exists()
    assert _rows(db) == []


# --- the switch predicate itself ------------------------------------------------------------

@pytest.mark.parametrize("value,expected", [
    ("1", True), ("true", True), ("TRUE", True), ("yes", True), ("on", True),
    ("0", False), ("false", False), ("", False), ("no", False), ("  ", False),
])
def test_the_env_switch_predicate_is_explicit_about_what_counts_as_on(monkeypatch, value, expected):
    """An operator who writes `DEV_KNOWLEDGE_TELEMETRY=0` means OFF. A naive truthiness test on
    the string would read "0" as on, which is the sort of switch that looks wired and is not."""
    monkeypatch.setenv(_TELEMETRY_ENV, value)
    assert bfp.telemetry_enabled() is expected
    assert bcm.telemetry_enabled() is expected


def test_the_switch_is_absent_by_default(monkeypatch):
    monkeypatch.delenv(_TELEMETRY_ENV, raising=False)
    assert bfp.telemetry_enabled() is False
    assert bcm.telemetry_enabled() is False


def test_the_unanchored_organ_reuses_the_ff_organs_switch_not_its_own_copy():
    """Reuse-integrity, the shape `test_block_ff_push::test_shares_validate_no_ff_signature`
    already pins for the FF signature: `block_unanchored_push` imports the sibling's predicate as
    the SAME object, so the two pre-push organs cannot drift into two ideas of what "telemetry is
    on" means."""
    import block_unanchored_push as bup
    assert bup.telemetry_enabled is bfp.telemetry_enabled
