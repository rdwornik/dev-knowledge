"""Tests for scripts/session_end_backpressure.py (#8 backpressure + ADR-85 gate).

Two layers:
  * Unit — deterministic git/file reads; tests stub the module's `_git` so no real repo is
    needed. Verifies each check's fire/silent branches, the override token logic, and the
    main() output modes (hard `decision:block` vs advisory `additionalContext` vs silent).
  * E2E — a real throwaway git repo (tmp_path), the hook invoked as a subprocess, exercising
    the five ADR-85 paths end-to-end (block / pass / no-op / backlog / override). This is the
    closure metric for the gate, not the unit tests.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "scripts" / "session_end_backpressure.py"

# a realistic 40-hex full SHA; first 7 chars are the short prefix the gate matches on
_SHA = "abc1234e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c"


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


# --- dirty tree (advisory, unchanged) ---------------------------------------

def test_dirty_tree_fires(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R(" M foo.py\n?? bar.txt\n")}))
    line = sb.check_dirty_tree()
    assert line and "dirty tree: 2 uncommitted" in line
    assert "foo.py" in line and "commit or stash" in line


def test_dirty_tree_silent_when_clean(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R("")}))
    assert sb.check_dirty_tree() is None


# --- journal SHA anchor (HARD, ADR-85) --------------------------------------

def _journal_log(added):
    """Build a 'log' stub: -p query on JOURNAL.md returns `added`; everything else empty."""
    def log(args):
        if "-p" in args and args[-1] == sb._JOURNAL:
            return _R(added)
        return _R("")
    return log


def test_journal_sha_fires_when_commits_without_sha(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),                       # clean tree
        "rev-parse": _R("", 1),                  # no upstream -> base = main
        "rev-list": _R(_SHA + "\n"),             # one commit shipped this arc
        "log": _journal_log("+a journal entry with no commit sha\n"),
    }))
    line = sb.check_journal_sha_anchor()
    assert line and "JOURNAL (hard)" in line and _SHA[:7] in line


def test_journal_sha_passes_when_sha_present(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),
        "rev-parse": _R("", 1),
        "rev-list": _R(_SHA + "\n"),
        "log": _journal_log(f"+Changes: commit {_SHA[:7]} landed this arc\n"),
    }))
    assert sb.check_journal_sha_anchor() is None


def test_journal_sha_silent_when_dirty(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R(" M x\n")}))
    assert sb.check_journal_sha_anchor() is None


def test_journal_sha_silent_when_nothing_shipped(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "rev-list": _R(""),
    }))
    assert sb.check_journal_sha_anchor() is None


# --- backlog marker (ADVISORY, ADR-85 R1) -----------------------------------

def _backlog_log(added):
    def log(args):
        if "-p" in args and args[-1] == sb._BACKLOG:
            return _R(added)
        return _R("")
    return log


def test_backlog_marker_fires_without_marker(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),
        "rev-parse": _R("", 1),
        "rev-list": _R(_SHA + "\n"),
        "log": _backlog_log("+some prose change, no structural marker\n"),
    }))
    line = sb.check_backlog_marker()
    assert line and "BACKLOG (advisory)" in line


def test_backlog_marker_passes_with_issue_id(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),
        "rev-parse": _R("", 1),
        "rev-list": _R(_SHA + "\n"),
        "log": _backlog_log("+- [#168] [P2][S] new follow-up task\n"),
    }))
    assert sb.check_backlog_marker() is None


def test_backlog_marker_silent_when_nothing_shipped(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "rev-list": _R(""),
    }))
    assert sb.check_backlog_marker() is None


# --- canonical freshness (advisory, unchanged) ------------------------------

def test_canonical_freshness_fires_without_bump(monkeypatch):
    def log(args):
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
            return _R("+**last_reviewed:** 2026-06-16\n+new prose\n") if args[-1] == "CLAUDE.md" else _R("")
        return _R("")
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "log": log,
    }))
    assert sb.check_canonical_freshness() is None


# --- override token (HEAD-bound, pure-read; ADR-85 §4) ----------------------

def test_override_active_true_when_head_matches(monkeypatch, tmp_path):
    tok = tmp_path / ".session-override-token"
    tok.write_text(json.dumps({"head": _SHA, "reason": "x"}), encoding="utf-8")
    monkeypatch.setattr(sb, "_TOKEN_PATH", tok)
    monkeypatch.setattr(sb, "_git", _fake_git({"rev-parse": _R(_SHA + "\n")}))
    assert sb._override_active() is True


def test_override_inactive_when_head_moved(monkeypatch, tmp_path):
    tok = tmp_path / ".session-override-token"
    tok.write_text(json.dumps({"head": _SHA, "reason": "x"}), encoding="utf-8")
    monkeypatch.setattr(sb, "_TOKEN_PATH", tok)
    monkeypatch.setattr(sb, "_git", _fake_git({"rev-parse": _R("0000000new\n")}))
    assert sb._override_active() is False


def test_override_inactive_when_no_token(monkeypatch, tmp_path):
    monkeypatch.setattr(sb, "_TOKEN_PATH", tmp_path / "nope")
    assert sb._override_active() is False


# --- main() output modes ----------------------------------------------------

def test_main_blocks_when_journal_sha_missing(monkeypatch, capsys):
    monkeypatch.setattr(sb, "_override_active", lambda: False)
    def log(args):
        # JOURNAL diff has no sha (hard fires); BACKLOG diff has no marker (advisory fires);
        # canon name-only empty (freshness skips)
        if "-p" in args and args[-1] in (sb._JOURNAL, sb._BACKLOG):
            return _R("+prose change\n")
        return _R("")
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "rev-list": _R(_SHA + "\n"), "log": log,
    }))
    assert sb.main() == 0
    payload = json.loads(capsys.readouterr().out.strip())
    assert payload["decision"] == "block"
    assert "JOURNAL (hard)" in payload["reason"]
    assert "BACKLOG (advisory)" in payload["reason"]   # advisory folded into the block reason
    assert "/override" in payload["reason"]


def test_main_allows_when_override_active(monkeypatch, capsys):
    # even with a hard failure present, an active override -> silent allow
    monkeypatch.setattr(sb, "_override_active", lambda: True)
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "rev-list": _R(_SHA + "\n"),
        "log": _journal_log("+no sha here\n"),
    }))
    assert sb.main() == 0
    assert capsys.readouterr().out.strip() == ""


def test_main_advisory_when_only_soft_fires(monkeypatch, capsys):
    # dirty tree only: hard journal check skips (not clean), dirty-tree advisory fires
    monkeypatch.setattr(sb, "_override_active", lambda: False)
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R(" M foo.py\n")}))
    assert sb.main() == 0
    payload = json.loads(capsys.readouterr().out.strip())
    hso = payload["hookSpecificOutput"]
    assert hso["hookEventName"] == "Stop"
    assert "dirty tree" in hso["additionalContext"]
    assert "decision" not in payload   # advisory must NOT block


def test_main_silent_when_all_clear(monkeypatch, capsys):
    monkeypatch.setattr(sb, "_override_active", lambda: False)
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "rev-list": _R(""), "log": _R(""),
    }))
    assert sb.main() == 0
    assert capsys.readouterr().out.strip() == ""


def test_main_fail_soft_on_exception(monkeypatch, capsys):
    # a check that raises must never wedge the stop: no block, exit 0, silent
    def boom(*a):
        raise RuntimeError("git exploded")
    monkeypatch.setattr(sb, "_override_active", lambda: False)
    monkeypatch.setattr(sb, "_git", boom)
    assert sb.main() == 0
    assert capsys.readouterr().out.strip() == ""


# --- E2E: real throwaway git repo, hook invoked as a subprocess -------------

def _git_in(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


def _commit(repo, path, content, msg):
    (repo / path).write_text(content, encoding="utf-8")
    _git_in(repo, "add", path)
    _git_in(repo, "commit", "-q", "-m", msg)
    return _git_in(repo, "rev-parse", "HEAD").stdout.strip()


def _run_hook(repo):
    """Invoke the hook with its _REPO_ROOT == repo; return stdout (the JSON, or '')."""
    return subprocess.run(
        [sys.executable, str(repo / "scripts" / "session_end_backpressure.py")],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def test_e2e_five_paths(tmp_path):
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "logs").mkdir()
    # copy the live hook into the throwaway repo so _REPO_ROOT resolves to it
    (repo / "scripts" / "session_end_backpressure.py").write_text(
        _P.read_text(encoding="utf-8"), encoding="utf-8")
    # mirror the real repo: logs/ is gitignored, so the override token never dirties the tree
    (repo / ".gitignore").write_text("logs/\n", encoding="utf-8")
    token = repo / "logs" / ".session-override-token"

    _git_in(repo, "init", "-q", "-b", "main")
    _git_in(repo, "config", "user.email", "t@t.t")
    _git_in(repo, "config", "user.name", "t")
    # base point on main: commit README + the hook + the .gitignore (clean tree)
    (repo / "README.md").write_text("# repo\n", encoding="utf-8")
    _git_in(repo, "add", "README.md", "scripts/session_end_backpressure.py", ".gitignore")
    _git_in(repo, "commit", "-q", "-m", "init")

    # PATH 3 — no-op: on main, clean, nothing ahead of base -> silent allow
    assert _run_hook(repo) == "", "no-op session must pass silently"

    # work happens on a feature branch (base = main; no upstream -> _base_ref() == 'main')
    _git_in(repo, "checkout", "-q", "-b", "feat/x")
    foo_sha = _commit(repo, "foo.txt", "change\n", "feat: change foo")

    # PATH 1 — block: commit landed, JOURNAL has no session SHA -> decision:block
    payload = json.loads(_run_hook(repo))
    assert payload["decision"] == "block", "commit w/o journal SHA must hard-block"
    assert "JOURNAL (hard)" in payload["reason"]
    assert "BACKLOG (advisory)" in payload["reason"]  # advisory rides inside the block

    # PATH 5 — override: in this genuine block state, arm a HEAD-bound token -> allow
    token.write_text(json.dumps({"head": foo_sha, "reason": "e2e override"}), encoding="utf-8")
    assert _run_hook(repo) == "", "valid HEAD-bound override token -> allow"
    # a stale token (HEAD moved on) must NOT bypass -> still blocks
    token.write_text(json.dumps({"head": "deadbeef" * 5, "reason": "stale"}), encoding="utf-8")
    assert json.loads(_run_hook(repo))["decision"] == "block", "stale override must not bypass"
    token.unlink()  # disarm before the remaining paths

    # PATH 2 — pass: add a JOURNAL entry naming the session SHA -> hard gate clears
    _commit(repo, "JOURNAL.md", f"### entry\nChanges: commit {foo_sha}\n", "docs: journal")
    payload = json.loads(_run_hook(repo))
    assert payload.get("decision") != "block", "journal SHA present must clear the hard gate"
    # journal satisfied; BACKLOG still untouched -> advisory additionalContext, NOT a block
    assert "BACKLOG (advisory)" in payload["hookSpecificOutput"]["additionalContext"]

    # PATH 4 — backlog satisfied: add a [#id] marker -> fully silent.
    # (The JOURNAL still names foo_sha, which remains in the now-larger main..HEAD arc.)
    _commit(repo, "BACKLOG.md", "- [#1] [P2][S] task · Done when: x\n", "docs: backlog")
    assert _run_hook(repo) == "", "journal SHA + backlog marker present -> silent pass"
