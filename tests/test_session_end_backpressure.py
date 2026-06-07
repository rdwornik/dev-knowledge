"""Unit tests for scripts/session_end_backpressure.py (#8 Stop backpressure).

The checks are deterministic git/file reads; tests stub the module's `_git` so no
real repo is needed. Verifies each check's fire/silent branches, the JSON output
shape (additionalContext on a Stop hook), and silence when all clear.
"""

import importlib.util
import json
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "scripts" / "session_end_backpressure.py"


def _load():
    spec = importlib.util.spec_from_file_location("session_end_backpressure", _P)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sb = _load()


class _R:
    def __init__(self, stdout="", returncode=0):
        self.stdout = stdout
        self.returncode = returncode


def _fake_git(responses):
    """responses: dict keyed by the first git subcommand -> _R (or callable(args)->_R)."""
    def run(*args):
        key = args[0]
        val = responses.get(key)
        if callable(val):
            return val(args)
        return val if val is not None else _R("", 0)
    return run


# --- dirty tree -------------------------------------------------------------

def test_dirty_tree_fires(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R(" M foo.py\n?? bar.txt\n")}))
    line = sb.check_dirty_tree()
    assert line and "dirty tree: 2 uncommitted" in line
    assert "foo.py" in line and "commit or stash" in line


def test_dirty_tree_silent_when_clean(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R("")}))
    assert sb.check_dirty_tree() is None


# --- journal-for-shipped ----------------------------------------------------

def test_journal_fires_when_commits_without_journal(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),                                   # clean
        "rev-parse": _R("", 1),                             # no upstream -> base=main
        "log": _R("scripts/foo.py\nBACKLOG.md\n"),          # arc touched, no JOURNAL.md
        "rev-list": _R("3\n"),
    }))
    line = sb.check_journal_for_shipped_session()
    assert line and "3 commit(s) ahead of main" in line and "JOURNAL.md" in line


def test_journal_silent_when_journal_touched(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),
        "rev-parse": _R("", 1),
        "log": _R("JOURNAL.md\nscripts/foo.py\n"),
    }))
    assert sb.check_journal_for_shipped_session() is None


def test_journal_silent_when_dirty(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R(" M x\n")}))
    assert sb.check_journal_for_shipped_session() is None


def test_journal_silent_when_nothing_shipped(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "log": _R(""),
    }))
    assert sb.check_journal_for_shipped_session() is None


# --- canonical freshness ----------------------------------------------------

def test_canonical_freshness_fires_without_bump(monkeypatch):
    def log(args):
        # names query lists the doc; -p query shows a diff with no last_reviewed line
        if "--name-only" in args:
            return _R("CLAUDE.md\n") if args[-1] == "CLAUDE.md" else _R("")
        if "-p" in args:
            return _R("+some new prose line\n-old prose line\n") if args[-1] == "CLAUDE.md" else _R("")
        return _R("")
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "log": log,
    }))
    line = sb.check_canonical_freshness()
    assert line and "CLAUDE.md" in line and "last_reviewed" in line


def test_canonical_freshness_silent_when_bumped(monkeypatch):
    def log(args):
        if "--name-only" in args:
            return _R("CLAUDE.md\n") if args[-1] == "CLAUDE.md" else _R("")
        if "-p" in args:
            return _R("+**last_reviewed:** 2026-06-07\n+new prose\n") if args[-1] == "CLAUDE.md" else _R("")
        return _R("")
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "log": log,
    }))
    assert sb.check_canonical_freshness() is None


# --- main JSON shape --------------------------------------------------------

def test_main_emits_stop_additionalcontext_when_dirty(monkeypatch, capsys):
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R(" M foo.py\n")}))
    assert sb.main() == 0
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)                               # must be valid JSON
    hso = payload["hookSpecificOutput"]
    assert hso["hookEventName"] == "Stop"
    assert "dirty tree" in hso["additionalContext"]


def test_main_silent_when_all_clear(monkeypatch, capsys):
    # clean tree, nothing shipped -> every check None -> NO stdout (silent)
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "log": _R(""),
    }))
    assert sb.main() == 0
    assert capsys.readouterr().out.strip() == ""
