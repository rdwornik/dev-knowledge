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
import io
import json
import subprocess
import sys
from datetime import date
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


def _main_out(monkeypatch, capsys, stdin_obj):
    """Drive main() with a chosen Stop-hook stdin payload; return (rc, stdout-stripped).

    stdin_obj is None -> empty stdin (the CC-2.1.178 reality: no stop_hook_active -> the
    structural floor applies). A dict -> JSON on stdin (e.g. {"stop_hook_active": True}).
    """
    payload = "" if stdin_obj is None else json.dumps(stdin_obj)
    monkeypatch.setattr(sb.sys, "stdin", io.StringIO(payload))
    rc = sb.main()
    return rc, capsys.readouterr().out.strip()


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
    # Isolate from the live CLAUDE.md stamp: the #142 same-day exemption (line 287) would
    # otherwise silence this whenever the real file's last_reviewed == today, making the
    # test pass/fail on repo state. Force a non-today stamp so the unbumped-diff leg runs.
    monkeypatch.setattr(sb, "_current_last_reviewed", lambda doc: None)
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


def _freshness_git_for(doc):
    """name-only shows `doc` changed in the arc; its -p diff has no last_reviewed line."""
    def log(args):
        if "--name-only" in args:
            return _R(doc + "\n") if args[-1] == doc else _R("")
        if "-p" in args:
            return _R("+new prose line\n-old prose line\n") if args[-1] == doc else _R("")
        return _R("")
    return _fake_git({"status": _R(""), "rev-parse": _R("", 1), "log": log})


def test_freshness_same_day_exempt(monkeypatch, tmp_path):
    # #142: the doc changed in the arc with no last_reviewed bump, BUT its current
    # last_reviewed already == today -> re-stamping is a no-op diff, so the leg could never
    # be cleared. Same-day exemption: not a finding. (RED pre-fix: the old check ignores the
    # current value and fires; GREEN post-fix.)
    doc = "CLAUDE.md"
    today = date.today().isoformat()
    (tmp_path / doc).write_text(
        f"---\nlast_reviewed: {today}\nstatus: active\n---\n# x\n", encoding="utf-8")
    monkeypatch.setattr(sb, "_REPO_ROOT", tmp_path)
    monkeypatch.setattr(sb, "_git", _freshness_git_for(doc))
    assert sb.check_canonical_freshness() is None


def test_freshness_still_fires_when_stale(monkeypatch, tmp_path):
    # guard against over-exemption: a genuinely stale last_reviewed (< today) edited without
    # a bump still fires (the exemption is same-day ONLY).
    doc = "CLAUDE.md"
    (tmp_path / doc).write_text(
        "---\nlast_reviewed: 2000-01-01\nstatus: active\n---\n# x\n", encoding="utf-8")
    monkeypatch.setattr(sb, "_REPO_ROOT", tmp_path)
    monkeypatch.setattr(sb, "_git", _freshness_git_for(doc))
    line = sb.check_canonical_freshness()
    assert line and doc in line and "last_reviewed" in line


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


def test_main_floor_suppresses_advisory_without_retry_signal(monkeypatch, capsys):
    # dirty tree only (hard journal check skips: not clean). No stop_hook_active in stdin
    # (the CC-2.1.178 reality) -> STRUCTURAL FLOOR: advisory-only must NOT keep the turn
    # going. additionalContext "continues the conversation" (CC v2.1.163) and a persistent
    # advisory condition would loop to the block-cap, so advisory-only output is silent.
    monkeypatch.setattr(sb, "_override_active", lambda: False)
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R(" M foo.py\n")}))
    rc, out = _main_out(monkeypatch, capsys, None)
    assert rc == 0 and out == ""


def test_main_fire_once_surfaces_advisory_on_first_attempt(monkeypatch, capsys):
    # stop_hook_active present and False = the FIRST stop attempt -> surface the advisory
    # once (the nudge still reaches the agent when a runtime provides the retry signal).
    monkeypatch.setattr(sb, "_override_active", lambda: False)
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R(" M foo.py\n")}))
    rc, out = _main_out(monkeypatch, capsys, {"stop_hook_active": False})
    payload = json.loads(out)
    assert payload["hookSpecificOutput"]["hookEventName"] == "Stop"
    assert "dirty tree" in payload["hookSpecificOutput"]["additionalContext"]
    assert "decision" not in payload   # advisory must NOT block


def test_main_fire_once_suppresses_advisory_on_retry(monkeypatch, capsys):
    # stop_hook_active True = a retry after the nudge already surfaced -> suppress
    # (fire-once). This is what prevents reaching the block-cap when the field is present.
    monkeypatch.setattr(sb, "_override_active", lambda: False)
    monkeypatch.setattr(sb, "_git", _fake_git({"status": _R(" M foo.py\n")}))
    rc, out = _main_out(monkeypatch, capsys, {"stop_hook_active": True})
    assert rc == 0 and out == ""


def test_main_silent_when_all_clear(monkeypatch, capsys):
    monkeypatch.setattr(sb, "_override_active", lambda: False)
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "rev-list": _R(""), "log": _R(""),
    }))
    assert sb.main() == 0
    assert capsys.readouterr().out.strip() == ""


def _notask_git():
    # the witnessed loop's shape: clean tree, one commit ahead, JOURNAL names the SHA (hard
    # leg CLEARS), BACKLOG has no structural marker (advisory fires), canon name-only empty.
    def log(args):
        if "-p" in args and args[-1] == sb._JOURNAL:
            return _R(f"+Changes: commit {_SHA[:7]} landed this arc\n")
        if "-p" in args and args[-1] == sb._BACKLOG:
            return _R("+prose-only change, no structural marker\n")
        return _R("")
    return _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "rev-list": _R(_SHA + "\n"), "log": log,
    })


def test_loop_advisory_does_not_keep_going_on_retry(monkeypatch, capsys):
    # THE witnessed loop, reproduced: a no-task session (hard leg satisfied, BACKLOG advisory
    # fires) on a RETRY (stop_hook_active True). Pre-fix the hook ignores stdin and emits
    # additionalContext on every consecutive attempt -> "continues the conversation" each
    # time -> 9 consecutive -> block-cap -> auto-override. Post-fix: SILENT (the loop is gone).
    monkeypatch.setattr(sb, "_override_active", lambda: False)
    monkeypatch.setattr(sb, "_git", _notask_git())
    rc, out = _main_out(monkeypatch, capsys, {"stop_hook_active": True})
    assert rc == 0
    assert out == "", "advisory must not keep the turn going on a retry (would loop to the cap)"


def test_loop_advisory_floored_without_retry_signal(monkeypatch, capsys):
    # CC 2.1.178 sends NO stop_hook_active -> the structural floor is the active guarantee:
    # advisory-only is silent even on the very first attempt. Pre-fix: emits (loops). GREEN: silent.
    monkeypatch.setattr(sb, "_override_active", lambda: False)
    monkeypatch.setattr(sb, "_git", _notask_git())
    rc, out = _main_out(monkeypatch, capsys, None)
    assert rc == 0
    assert out == "", "floor: advisory-only must not keep the turn going absent a retry signal"


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


def _run_hook(repo, stdin_obj=None):
    """Invoke the hook with its _REPO_ROOT == repo; return stdout (the JSON, or '').

    stdin_obj None -> empty stdin (the CC-2.1.178 reality: no stop_hook_active -> structural
    floor). A dict is fed as JSON on stdin (e.g. {"stop_hook_active": True}).
    """
    return subprocess.run(
        [sys.executable, str(repo / "scripts" / "session_end_backpressure.py")],
        input=("" if stdin_obj is None else json.dumps(stdin_obj)),
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
    # TEETH: the hard gate must NOT honor stop_hook_active -> still blocks on a retry
    assert json.loads(_run_hook(repo, {"stop_hook_active": True}))["decision"] == "block", \
        "hard JOURNAL gate ignores stop_hook_active (teeth survive; only advisory fires once)"

    # PATH 5 — override: in this genuine block state, arm a HEAD-bound token -> allow
    token.write_text(json.dumps({"head": foo_sha, "reason": "e2e override"}), encoding="utf-8")
    assert _run_hook(repo) == "", "valid HEAD-bound override token -> allow"
    # a stale token (HEAD moved on) must NOT bypass -> still blocks
    token.write_text(json.dumps({"head": "deadbeef" * 5, "reason": "stale"}), encoding="utf-8")
    assert json.loads(_run_hook(repo))["decision"] == "block", "stale override must not bypass"
    token.unlink()  # disarm before the remaining paths

    # PATH 2 — pass + FLOOR: add a JOURNAL entry naming the session SHA -> hard gate clears.
    _commit(repo, "JOURNAL.md", f"### entry\nChanges: commit {foo_sha}\n", "docs: journal")
    # No stop_hook_active in stdin (CC 2.1.178) -> structural floor: with the hard gate clear
    # and only the BACKLOG advisory left, advisory-only output is SILENT (additionalContext
    # keeps the turn going and would loop to the block-cap).
    assert _run_hook(repo) == "", "hard cleared + no retry signal -> floor suppresses advisory"
    # fire-once first attempt (a runtime that DOES send stop_hook_active=False): surface once.
    payload = json.loads(_run_hook(repo, {"stop_hook_active": False}))
    assert payload.get("decision") != "block", "journal SHA present must clear the hard gate"
    assert "BACKLOG (advisory)" in payload["hookSpecificOutput"]["additionalContext"]
    # retry (stop_hook_active True) -> suppressed; never reaches a second consecutive keep-going.
    assert _run_hook(repo, {"stop_hook_active": True}) == "", "retry -> fire-once suppress"

    # PATH 4 — backlog satisfied: add a [#id] marker -> fully silent on every path.
    # (The JOURNAL still names foo_sha, which remains in the now-larger main..HEAD arc.)
    _commit(repo, "BACKLOG.md", "- [#1] [P2][S] task · Done when: x\n", "docs: backlog")
    assert _run_hook(repo) == "", "journal SHA + backlog marker present -> silent pass"
    assert _run_hook(repo, {"stop_hook_active": False}) == "", "nothing to surface -> silent"
