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

# distinct fake commits for the per-session anchor arc (each [:7] is its matched short prefix)
_S1W = "1111111aaaa"    # prior session: work
_S1J = "2222222bbbb"    # prior session: journal-wrap (cites _S1W)
_S2A = "3333333cccc"    # this session: work
_S2B = "4444444dddd"    # this session: work (HEAD)
_S2J = "5555555eeee"    # this session: journal-wrap (cites this session's work)
_S2FIX = "6666666ffff"  # this session: a trailing commit after the wrap


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


def _journal_show(added):
    """Build a 'show' stub: any `git show … -- JOURNAL.md` returns `added` as that commit's
    journal additions; everything else empty. (The per-commit `--first-parent` show the
    session-anchor check now uses; mirrors _journal_log for single-commit arcs.)"""
    def show(args):
        if args[-1] == sb._JOURNAL:
            return _R(added)
        return _R("")
    return show


def _arc_show(citations):
    """A 'show' stub keyed by the commit SHA: returns citations.get(sha, '') as that commit's
    JOURNAL additions. `citations` maps a full SHA -> the '+…' line it added. The object is the
    token right before the '--' path separator in `git show … <sha> -- JOURNAL.md`."""
    def show(args):
        if args[-1] != sb._JOURNAL:
            return _R("")
        sha = args[args.index("--") - 1]
        return _R(citations.get(sha, ""))
    return show


def test_journal_sha_fires_when_commits_without_sha(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),                       # clean tree
        "rev-parse": _R("", 1),                  # no upstream/origin -> base = main
        "rev-list": _R(_SHA + "\n"),             # one commit shipped this arc
        "show": _journal_show("+a journal entry with no commit sha\n"),
    }))
    line = sb.check_journal_sha_anchor()
    assert line and "JOURNAL (hard)" in line and _SHA[:7] in line


def test_journal_sha_passes_when_sha_present(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),
        "rev-parse": _R("", 1),
        "rev-list": _R(_SHA + "\n"),
        "show": _journal_show(f"+Changes: commit {_SHA[:7]} landed this session\n"),
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


# --- per-session anchor: the C1 arc-granularity regression + guards ---------

def test_anchor_regression_two_session_arc(monkeypatch):
    # C1, THE witnessed miss: a deferred-serial-push arc spanning two sessions. S1 journaled
    # (S1J cites S1W); S2 shipped S2A,S2B but did NOT journal; no push between. The OLD any()-
    # over-the-push-arc saw S1W cited and PASSED (the silent miss). The per-session anchor must
    # FIRE on S2's work and must NOT drag in the prior session's S1W/S1J.
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),
        "rev-parse": _R("", 1),
        "rev-list": _R("\n".join([_S2B, _S2A, _S1J, _S1W]) + "\n"),   # newest-first
        "show": _arc_show({_S1J: f"+wrapped S1: commit {_S1W[:7]}\n"}),  # only S1J cites
    }))
    line = sb.check_journal_sha_anchor()
    assert line and "JOURNAL (hard)" in line and "2 commit(s)" in line
    assert _S2A[:7] in line and _S2B[:7] in line          # this session's uncited work, named
    assert _S1W[:7] not in line and _S1J[:7] not in line  # prior session not dragged in


def test_anchor_happy_path_passes(monkeypatch):
    # this session journaled: the newest commit is the wrap, citing this session's work.
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),
        "rev-parse": _R("", 1),
        "rev-list": _R("\n".join([_S2J, _S2A, _S1J, _S1W]) + "\n"),
        "show": _arc_show({
            _S2J: f"+Changes: commit {_S2A[:7]} this session\n",
            _S1J: f"+wrapped S1: commit {_S1W[:7]}\n",
        }),
    }))
    assert sb.check_journal_sha_anchor() is None


def test_anchor_trailing_work_fires(monkeypatch):
    # journaled, then committed more without re-journaling -> the trailing commit fires
    # (intended "latest work not journaled"); the wrapped work behind the boundary is not named.
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),
        "rev-parse": _R("", 1),
        "rev-list": _R("\n".join([_S2FIX, _S2J, _S2A]) + "\n"),
        "show": _arc_show({_S2J: f"+Changes: commit {_S2A[:7]}\n"}),
    }))
    line = sb.check_journal_sha_anchor()
    assert line and "1 commit(s)" in line and _S2FIX[:7] in line and _S2A[:7] not in line


def test_anchor_no_journal_fires_all(monkeypatch):
    # no journal-wrap anywhere in the arc -> the whole session is unanchored -> FIRE all.
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""),
        "rev-parse": _R("", 1),
        "rev-list": _R("\n".join([_S2B, _S2A]) + "\n"),
        "show": _arc_show({}),
    }))
    line = sb.check_journal_sha_anchor()
    assert line and "2 commit(s)" in line and _S2A[:7] in line and _S2B[:7] in line


def test_session_shas_bad_base_anchors_head(monkeypatch):
    # secondary C1: a degenerate base makes `git rev-list base..HEAD` ERROR -> do NOT vacuous-
    # PASS; anchor on HEAD so the gate still demands a citation. (RED pre-fix: returned [].)
    head = _S2B

    def run(*args):
        if args[0] == "rev-list":
            return _R("", 128)                       # bad/missing base -> error
        if args[0] == "rev-parse" and "HEAD" in args:
            return _R(head + "\n")                    # _head_sha
        if args[0] == "rev-parse":
            return _R("", 1)                         # no upstream; origin/main verify fails
        if args[0] == "status":
            return _R("")
        return _R("")                                # show -> empty (HEAD can't self-cite)
    monkeypatch.setattr(sb, "_git", run)
    assert sb._session_shas() == [head]
    line = sb.check_journal_sha_anchor()
    assert line and head[:7] in line


def test_session_shas_clean_empty_passes(monkeypatch):
    # the legitimate empty: a real base with nothing ahead (rev-list ZERO exit, empty) -> [].
    monkeypatch.setattr(sb, "_git", _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "rev-list": _R("", 0),
    }))
    assert sb._session_shas() == []
    assert sb.check_journal_sha_anchor() is None


def test_base_ref_prefers_upstream(monkeypatch):
    monkeypatch.setattr(sb, "_git", _fake_git({"rev-parse": _R("origin/feat-x\n", 0)}))
    assert sb._base_ref() == "origin/feat-x"


def test_base_ref_verified_origin_main(monkeypatch):
    # no upstream, but origin/main verifies -> prefer it over the bare 'main' string.
    def run(*args):
        if args[0] == "rev-parse" and "@{upstream}" in args:
            return _R("", 1)
        if args[0] == "rev-parse" and "--verify" in args and "origin/main" in args:
            return _R("abc1234\n", 0)
        return _R("", 0)
    monkeypatch.setattr(sb, "_git", run)
    assert sb._base_ref() == "origin/main"


def test_base_ref_falls_back_to_main(monkeypatch):
    # no upstream AND origin/main does not resolve -> bare 'main' (last resort).
    def run(*args):
        if "@{upstream}" in args:
            return _R("", 1)
        if "--verify" in args:
            return _R("", 1)
        return _R("", 0)
    monkeypatch.setattr(sb, "_git", run)
    assert sb._base_ref() == "main"


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
    # leg CLEARS via the per-commit show), BACKLOG has no structural marker (advisory fires),
    # canon name-only empty.
    def log(args):
        if "-p" in args and args[-1] == sb._BACKLOG:
            return _R("+prose-only change, no structural marker\n")
        return _R("")
    return _fake_git({
        "status": _R(""), "rev-parse": _R("", 1), "rev-list": _R(_SHA + "\n"),
        "show": _journal_show(f"+Changes: commit {_SHA[:7]} landed this session\n"),
        "log": log,
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
    """Invoke the hook FROM WITHIN repo (cwd=repo) so its git-toplevel-first `_REPO_ROOT`
    (#237 port) resolves to repo; return stdout (the JSON, or '').

    cwd=repo mirrors the real invocation on both sides of the mesh: Claude Code runs a Stop hook
    with cwd = the project root, and the Informant's fire_test runs the hook with cwd = the clone.
    (Before the #237 port the organ resolved its root from `__file__`; the copy-into-repo above
    made that land on repo. The port resolves from cwd instead, so the test must set it.)

    stdin_obj None -> empty stdin (the CC-2.1.178 reality: no stop_hook_active -> structural
    floor). A dict is fed as JSON on stdin (e.g. {"stop_hook_active": True}).
    """
    return subprocess.run(
        [sys.executable, str(repo / "scripts" / "session_end_backpressure.py")],
        input=("" if stdin_obj is None else json.dumps(stdin_obj)),
        cwd=str(repo),
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

    # PATH 4 — backlog satisfied: add a [#id] marker, THEN journal it so the newest commit is
    # the wrap. Under the per-session anchor (ADR-85 amendment) the wrap must cover the latest
    # work, so the trailing backlog commit must itself be journaled — the old whole-arc any()
    # would have silently passed it (the exact C1 laxness this fix removes).
    bk = _commit(repo, "BACKLOG.md", "- [#1] [P2][S] task · Done when: x\n", "docs: backlog")
    _commit(repo, "JOURNAL.md",
            f"### backlog\nChanges: commit {bk}\n### entry\nChanges: commit {foo_sha}\n",
            "docs: journal backlog")
    assert _run_hook(repo) == "", "journal SHA + backlog marker present + journaled -> silent pass"
    assert _run_hook(repo, {"stop_hook_active": False}) == "", "nothing to surface -> silent"


# --- E2E: the C1 per-session anchor (cross-session miss + merge-delivered journal) ----------

def _make_repo(tmp_path, name="repo", with_origin=False):
    """Throwaway repo with the hook installed + an initial commit on main; optionally a bare
    origin so @{upstream}=origin/main is the pre-divergence base (the real push boundary)."""
    repo = tmp_path / name
    (repo / "scripts").mkdir(parents=True)
    (repo / "logs").mkdir()
    (repo / "scripts" / "session_end_backpressure.py").write_text(
        _P.read_text(encoding="utf-8"), encoding="utf-8")
    (repo / ".gitignore").write_text("logs/\n", encoding="utf-8")
    _git_in(repo, "init", "-q", "-b", "main")
    _git_in(repo, "config", "user.email", "t@t.t")
    _git_in(repo, "config", "user.name", "t")
    (repo / "README.md").write_text("# repo\n", encoding="utf-8")
    _git_in(repo, "add", "README.md", "scripts/session_end_backpressure.py", ".gitignore")
    _git_in(repo, "commit", "-q", "-m", "init")
    if with_origin:
        bare = tmp_path / (name + "-origin.git")
        subprocess.run(["git", "init", "--bare", "-q", str(bare)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
        _git_in(repo, "remote", "add", "origin", str(bare))
        _git_in(repo, "push", "-q", "-u", "origin", "main")
    return repo


def test_e2e_cross_session_miss_blocks(tmp_path):
    # THE C1 closure metric, real git: session-1 journals (cites its work); session-2 ships work
    # but does NOT journal; no push between -> the 2nd-session arc is uncited. OLD code: any()
    # over origin/main..HEAD saw S1's citation and PASSED (the silent miss). NEW: decision:block.
    repo = _make_repo(tmp_path)
    _git_in(repo, "checkout", "-q", "-b", "feat/x")           # base = main (no upstream/origin)
    s1w = _commit(repo, "a.txt", "a\n", "feat: s1 work")
    _commit(repo, "JOURNAL.md", f"### s1\nChanges: commit {s1w}\n", "docs: s1 journal")
    s2w = _commit(repo, "b.txt", "b\n", "feat: s2 work")      # shipped, NOT journaled
    payload = json.loads(_run_hook(repo))
    assert payload["decision"] == "block", "2nd-session-before-push uncited work must hard-block"
    assert s2w[:7] in payload["reason"] and s1w[:7] not in payload["reason"]


def test_e2e_cross_session_journaled_passes(tmp_path):
    # the companion (no false block): session-2 DOES journal its work -> the gate clears.
    repo = _make_repo(tmp_path)
    _git_in(repo, "checkout", "-q", "-b", "feat/x")
    s1w = _commit(repo, "a.txt", "a\n", "feat: s1 work")
    _commit(repo, "JOURNAL.md", f"### s1\nChanges: commit {s1w}\n", "docs: s1 journal")
    s2w = _commit(repo, "b.txt", "b\n", "feat: s2 work")
    _commit(repo, "JOURNAL.md",
            f"### s2\nChanges: commit {s2w}\n### s1\nChanges: commit {s1w}\n", "docs: s2 journal")
    assert _run_hook(repo) == "", "session-2 journaled its own work -> clear"


def test_e2e_merge_delivered_journal_passes(tmp_path):
    # the --no-ff happy path: work + journal on a branch, --no-ff merged to main; HEAD = merge.
    # git's default combined (--cc) merge diff HIDES the branch's JOURNAL add, so without
    # --first-parent the hook mis-reads the merge as unjournaled and BLOCKS; with it the merge
    # anchors -> PASS. origin makes @{upstream}=origin/main the pre-merge base (non-empty arc).
    repo = _make_repo(tmp_path, with_origin=True)
    _git_in(repo, "checkout", "-q", "-b", "feat/y")
    w = _commit(repo, "c.txt", "c\n", "feat: work")
    _commit(repo, "JOURNAL.md", f"### y\nChanges: commit {w}\n", "docs: journal y")
    _git_in(repo, "checkout", "-q", "main")
    _git_in(repo, "merge", "--no-ff", "-q", "-m", "merge feat/y", "feat/y")
    assert _run_hook(repo) == "", "merge-delivered journal must clear via --first-parent"


def test_e2e_merge_trailing_work_fires(tmp_path):
    # the mirror (direction preserved): work merged via --no-ff but NOT journaled -> still fires.
    repo = _make_repo(tmp_path, with_origin=True)
    _git_in(repo, "checkout", "-q", "-b", "feat/z")
    _commit(repo, "d.txt", "d\n", "feat: unjournaled work")
    _git_in(repo, "checkout", "-q", "main")
    _git_in(repo, "merge", "--no-ff", "-q", "-m", "merge feat/z", "feat/z")
    assert json.loads(_run_hook(repo))["decision"] == "block", "merged unjournaled work must block"


# --- lane-owned fleet-audit dailies ([#476]) --------------------------------
#
# The dirty-tree leg fired 4x in one session on two files that are untracked on `main` BY
# DESIGN: ADR-80/ADR-84 put the durable fleet-audit record on the `automation/fleet-audit`
# lane, and `.gitignore`'s own comment names `ecosystem/*/history/*.md` as durable records.
# Every repair the hook implied was wrong. A guard that fires on correct state trains the
# operator to ignore it.
#
# The exclusion is VERIFIED, never a pattern: a path is excused only when that exact file is
# already present on the lane tip (`ls-tree`). So the two ways this could go wrong are both
# pinned below — a stray file under history/ must still flag, and a daily NOT yet replicated
# must still flag, because that one really is at risk of being lost.

_LANE_DAILY = "ecosystem/.dev-knowledge/history/2026-08-02.md"
_LANE_DAILY_2 = "ecosystem/ai-council/history/2026-08-02.md"


def _lane_git(on_lane, status):
    """git stub: `status` porcelain output; `ls-tree` answers from the `on_lane` set."""
    def run(*args):
        if args[0] == "status":
            return _R(status)
        if args[0] == "ls-tree":
            path = args[-1]
            return _R(path + "\n" if path in on_lane else "")
        return _R("")
    return run


def test_lane_owned_daily_present_on_the_lane_does_not_flag(monkeypatch):
    """(a) The live false positive. Both dailies are on the lane tip -> nothing to repair."""
    monkeypatch.setattr(sb, "_git", _lane_git(
        {_LANE_DAILY, _LANE_DAILY_2},
        f"?? {_LANE_DAILY}\n?? {_LANE_DAILY_2}\n"))
    assert sb.check_dirty_tree() is None


def test_stray_untracked_file_under_history_still_flags(monkeypatch):
    """(b) NOT a blind pattern exclude. A file living under `history/` that the lane has
    never seen is ordinary untracked work and must still be surfaced."""
    stray = "ecosystem/.dev-knowledge/history/scratch-notes.md"
    monkeypatch.setattr(sb, "_git", _lane_git({_LANE_DAILY}, f"?? {stray}\n"))
    line = sb.check_dirty_tree()
    assert line and "1 uncommitted" in line
    assert stray in line


def test_daily_not_yet_on_the_lane_still_flags(monkeypatch):
    """(c) The at-risk case, and the reason the check is `ls-tree` rather than a regex: a
    daily that has NOT been replicated is exactly the one that can still be lost."""
    monkeypatch.setattr(sb, "_git", _lane_git(set(), f"?? {_LANE_DAILY}\n"))
    line = sb.check_dirty_tree()
    assert line and "1 uncommitted" in line
    assert _LANE_DAILY in line


def test_lane_exclusion_applies_only_to_untracked_entries(monkeypatch):
    """A TRACKED modification under `history/` is a real edit to a real file and must flag
    even when the lane also carries that path — the exclusion covers `??` only."""
    monkeypatch.setattr(sb, "_git", _lane_git({_LANE_DAILY}, f" M {_LANE_DAILY}\n"))
    line = sb.check_dirty_tree()
    assert line and _LANE_DAILY in line


def test_lane_owned_daily_does_not_mask_other_dirt(monkeypatch):
    """The excused daily is removed from the count, not the whole finding: real dirt beside
    it must still be reported, and reported with an honest count."""
    monkeypatch.setattr(sb, "_git", _lane_git(
        {_LANE_DAILY}, f"?? {_LANE_DAILY}\n M scripts/audit.py\n"))
    line = sb.check_dirty_tree()
    assert line and "1 uncommitted" in line, line
    assert "scripts/audit.py" in line
    assert _LANE_DAILY not in line


def test_lane_exclusion_is_scoped_to_history_dirs(monkeypatch):
    """`ecosystem/` is not blanket-excused — only `<repo>/history/<file>`. A sibling path is
    ordinary untracked work even if the lane happens to carry it."""
    other = "ecosystem/doc-counts.md"
    monkeypatch.setattr(sb, "_git", _lane_git({other}, f"?? {other}\n"))
    line = sb.check_dirty_tree()
    assert line and other in line


def test_lane_probe_failure_keeps_the_finding(monkeypatch):
    """Fail-CLOSED on the probe: if `ls-tree` errors (no lane branch, git trouble), the file
    is NOT excused. An unknown replication status is not a confirmed one — the same rule the
    RM-8 refusal follows. Silence here would hide a genuinely unreplicated daily."""
    def run(*args):
        if args[0] == "status":
            return _R(f"?? {_LANE_DAILY}\n")
        return _R("", 1)          # ls-tree errors
    monkeypatch.setattr(sb, "_git", run)
    line = sb.check_dirty_tree()
    assert line and _LANE_DAILY in line


def test_dirty_tree_output_is_ascii(monkeypatch):
    """ASCII output: this string is rendered into a Stop-hook JSON payload and read in a
    terminal that has already mangled non-ASCII glyphs this session."""
    monkeypatch.setattr(sb, "_git", _lane_git(set(), f"?? {_LANE_DAILY}\n"))
    line = sb.check_dirty_tree()
    assert line
    line.encode("ascii")          # raises UnicodeEncodeError if a non-ASCII glyph crept in
