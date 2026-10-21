"""RED tests: Stop hook is silent in unattended (headless/bg) sessions and fires once per
session_id in attended ones. Black-box: the hook is copied into a tmp git repo and run as a
subprocess with cwd=repo."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_HOOK = Path(__file__).resolve().parent.parent / "scripts" / "session_end_backpressure.py"
_SID_A = "5f0c1e5e-7a53-4a3e-9a51-0c1d2b3a4f60"
_SID_B = "9b2d7c44-1e0f-4c7a-8d35-6a7b8c9d0e1f"


def _git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    (r / "scripts").mkdir(parents=True)
    shutil.copy(_HOOK, r / "scripts" / "session_end_backpressure.py")
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@example.com")
    _git(r, "config", "user.name", "t")
    (r / "README.md").write_text("init\n", encoding="utf-8")
    _git(r, "add", "-A")
    _git(r, "commit", "-q", "-m", "init")
    (r / "untracked.txt").write_text("dirty\n", encoding="utf-8")
    return r


@pytest.fixture
def markers(tmp_path):
    return tmp_path / "markers"


def _env(markers, **extra):
    env = dict(os.environ)
    for k in ("CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_JOB_DIR"):
        env.pop(k, None)
    env["SESSION_END_BACKPRESSURE_MARKER_DIR"] = str(markers)
    env.update(extra)
    return env


def _run(repo, env, stdin):
    if not isinstance(stdin, str):
        stdin = json.dumps(stdin)
    return subprocess.run(
        [sys.executable, str(repo / "scripts" / "session_end_backpressure.py")],
        input=stdin, capture_output=True, text=True, encoding="utf-8",
        errors="replace", cwd=str(repo), env=env, timeout=60,
    )


def _stop(sid=_SID_A, active=False):
    d = {"hook_event_name": "Stop", "stop_hook_active": active}
    if sid is not None:
        d["session_id"] = sid
    return d


def _status(repo):
    return _git(repo, "status", "--porcelain").stdout


def _ctx(proc):
    return json.loads(proc.stdout)["hookSpecificOutput"]["additionalContext"]


HEADLESS = {"CLAUDE_CODE_ENTRYPOINT": "sdk-cli", "CLAUDE_CODE_SESSION_ATTENDED": "0"}


def test_headless_p_is_silent(repo, markers):
    p = _run(repo, _env(markers, **HEADLESS), _stop())
    assert p.returncode == 0
    assert p.stdout == ""
    assert "additionalContext" not in p.stdout + p.stderr


def test_bg_is_silent(repo, markers, tmp_path):
    env = _env(markers, CLAUDE_CODE_ENTRYPOINT="cli", CLAUDE_CODE_SESSION_ATTENDED="0",
               CLAUDE_JOB_DIR=str(tmp_path / "job"))
    p = _run(repo, env, _stop())
    assert p.returncode == 0
    assert p.stdout == ""
    assert "additionalContext" not in p.stdout + p.stderr


def test_headless_writes_no_marker_and_no_repo_file(repo, markers):
    before = _status(repo)
    p = _run(repo, _env(markers, **HEADLESS), _stop())
    assert p.returncode == 0
    assert not markers.exists() or list(markers.iterdir()) == []
    assert _status(repo) == before


def test_interactive_once_per_session_id(repo, markers):
    env = _env(markers, CLAUDE_CODE_SESSION_ATTENDED="1")
    before = _status(repo)

    first = _run(repo, env, _stop("s-A"))
    assert first.returncode == 0
    assert "dirty tree" in _ctx(first)
    assert _run(repo, env, _stop("s-A")).stdout == ""

    other = _run(repo, env, _stop("s-B"))
    assert other.returncode == 0
    assert "dirty tree" in _ctx(other)
    assert _run(repo, env, _stop("s-B")).stdout == ""

    assert not Path(markers).resolve().is_relative_to(repo.resolve())
    assert _status(repo) == before


def test_attended_var_absent_behaves_like_interactive(repo, markers):
    env = _env(markers)
    assert "CLAUDE_CODE_SESSION_ATTENDED" not in env
    first = _run(repo, env, _stop("s-A"))
    assert first.returncode == 0
    assert "dirty tree" in _ctx(first)
    assert _run(repo, env, _stop("s-A")).stdout == ""


def test_no_session_id_prints_every_time(repo, markers):
    env = _env(markers, CLAUDE_CODE_SESSION_ATTENDED="1")
    for _ in range(3):
        p = _run(repo, env, _stop(None))
        assert p.returncode == 0
        assert "dirty tree" in _ctx(p)


@pytest.mark.parametrize("attended", ["0", "1"])
@pytest.mark.parametrize("stdin", ["", "not json", "[1, 2, 3]"])
def test_fail_soft_on_bad_stdin(repo, markers, attended, stdin):
    p = _run(repo, _env(markers, CLAUDE_CODE_SESSION_ATTENDED=attended), stdin)
    assert p.returncode == 0
    assert "Traceback" not in p.stderr


def test_unwritable_marker_dir_still_prints(repo, tmp_path):
    bad = tmp_path / "markers-is-a-file"
    bad.write_text("x", encoding="utf-8")
    env = _env(bad, CLAUDE_CODE_SESSION_ATTENDED="1")
    p = _run(repo, env, _stop("s-A"))
    assert p.returncode == 0
    assert "Traceback" not in p.stderr
    assert "dirty tree" in _ctx(p)


def test_retry_suppressed_and_records_no_marker(repo, markers):
    env = _env(markers, CLAUDE_CODE_SESSION_ATTENDED="1")
    retry = _run(repo, env, _stop("s-A", active=True))
    assert retry.returncode == 0
    assert retry.stdout == ""
    assert not markers.exists() or list(markers.iterdir()) == []

    later = _run(repo, env, _stop("s-A", active=False))
    assert "dirty tree" in _ctx(later)
    assert _run(repo, env, _stop("s-A", active=False)).stdout == ""
