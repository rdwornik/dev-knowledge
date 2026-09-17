"""Unit tests for scripts/check_commit_message_type.py (commit-msg type-prefix hook, [#834]).

RED-first: this test module imports the hook by file path with no fallback, so it fails
LOUD (a collection error, not a silent skip) while `scripts/check_commit_message_type.py`
does not yet exist. Once the hook lands the import succeeds and every case below exercises
`check()` directly, the same shape as `tests/test_check_backlog_commit_msg.py`.
"""

import importlib.util
from pathlib import Path

_H = Path(__file__).resolve().parent.parent / "scripts" / "check_commit_message_type.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_commit_message_type", _H)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hook = _load()


def test_trip_no_type_prefix_is_flagged():
    """The refusal itself: a bare, type-less subject is a violation."""
    assert hook.check("standardize ADR-32 placeholder wording") is False


def test_passing_conventional_commit_passes():
    assert hook.check("docs(playbook): add a line") is True


def test_passing_with_scope_and_bang_passes():
    assert hook.check("feat(446)!: breaking change") is True


def test_extended_type_not_in_playbooks_closed_six_still_passes():
    """perf/build/lessons are live, sanctioned extensions -- not this gate's business."""
    assert hook.check("perf(audit): batch the commit/blob reads") is True
    assert hook.check("lessons: append entries from this window") is True


def test_merge_commit_exempt():
    assert hook.check("Merge branch 'worktree-x' @ deadbeef -- did a thing") is True


def test_revert_commit_exempt():
    assert hook.check('Revert "docs(audit): synthetic nightly digest"') is True


def test_empty_message_not_this_gates_problem():
    assert hook.check("") is True


def test_historical_breach_sha_2b337bf6_replayed_as_fixture():
    """Real historical breach: 2b337bf67a583803d01bddbe9be58961b8b63bcb ([ADR-30] era,
    pre-formalization) -- subject carries no Conventional Commits type prefix at all.
    Proves the gate would have caught it, had it existed then."""
    assert hook.check("[ADR-30] Add ADR-30 -- default branch = main for all Rob's repos") is False


def test_multiline_message_checks_only_the_subject():
    msg = "docs(playbook): add a line\n\nBody explaining why, at length.\n"
    assert hook.check(msg) is True
