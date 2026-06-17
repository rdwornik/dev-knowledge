"""Tests for scripts/coherence_nudge.py — the forgotten-version-bump pre-commit nudge.

Exercises the pure should_nudge core, the git-backed process() (real tmp git repo), and
the firing-rate log instrumentation. Asserts the prompt's contract: spec body edited
without a version bump -> nudge fires + logs; version bumped -> silent.
"""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import coherence_nudge as cn
import validate_reconciliation as vr

SPEC = vr._SPEC_REGISTRY["handoff-process"]
REL = SPEC.path
_NOW = datetime(2026, 6, 17, 9, 0, 0)


def _v(version: str, body: str = "body") -> str:
    return f"# HANDOFF_PROCESS\n\nVersion: {version}\nStatus: stable\n\n{body}\n"


# --- pure core --------------------------------------------------------------

def test_should_nudge_changed_without_bump() -> None:
    assert cn.should_nudge(_v("5.2", "old"), _v("5.2", "new"), SPEC) is True


def test_should_nudge_silent_when_unchanged() -> None:
    assert cn.should_nudge(_v("5.2", "x"), _v("5.2", "x"), SPEC) is False


def test_should_nudge_silent_when_version_bumped() -> None:
    assert cn.should_nudge(_v("5.2", "old"), _v("5.3", "new"), SPEC) is False


def test_should_nudge_silent_when_version_unparseable() -> None:
    assert cn.should_nudge("no version old", "no version new", SPEC) is False


# --- process() against a real tmp git repo ----------------------------------

def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True)


def _init_repo(tmp_path: Path, spec_text: str) -> Path:
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    p = tmp_path / REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(spec_text, encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "init")
    return tmp_path


def test_process_fires_and_logs_on_changed_without_bump(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, _v("5.2", "old body"))
    (repo / REL).write_text(_v("5.2", "substantively new body"), encoding="utf-8")
    log = repo / "logs" / "coherence-nudge.log"
    msg = cn.process(repo, REL, now=_NOW, log_path=log)
    assert msg is not None and "Version stayed 5.2" in msg
    assert log.exists()
    line = log.read_text(encoding="utf-8").strip()
    assert REL in line and "version=5.2" in line and line.startswith("2026-06-17T09:00:00")


def test_process_silent_when_version_bumped(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, _v("5.2", "old body"))
    (repo / REL).write_text(_v("5.3", "new body"), encoding="utf-8")
    log = repo / "logs" / "coherence-nudge.log"
    assert cn.process(repo, REL, now=_NOW, log_path=log) is None
    assert not log.exists()


def test_process_silent_when_unchanged(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, _v("5.2", "same"))
    log = repo / "logs" / "coherence-nudge.log"
    assert cn.process(repo, REL, now=_NOW, log_path=log) is None


def test_process_ignores_non_spec_file(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, _v("5.2"))
    assert cn.process(repo, "README.md", now=_NOW) is None


def test_process_ignores_new_file_no_head(tmp_path: Path) -> None:
    # spec exists in working tree but never committed -> no HEAD text -> silent.
    _git(tmp_path, "init", "-q")
    p = tmp_path / REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(_v("5.2"), encoding="utf-8")
    assert cn.process(tmp_path, REL, now=_NOW) is None


def test_main_exits_zero_even_on_fire(tmp_path: Path, monkeypatch) -> None:
    repo = _init_repo(tmp_path, _v("5.2", "old"))
    (repo / REL).write_text(_v("5.2", "new"), encoding="utf-8")
    monkeypatch.setattr(cn, "_REPO_ROOT", repo)
    monkeypatch.setattr(cn, "_LOG_PATH", repo / "logs" / "coherence-nudge.log")
    assert cn.main([REL]) == 0
