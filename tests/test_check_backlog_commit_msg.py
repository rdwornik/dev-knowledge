"""Unit tests for scripts/check_backlog_commit_msg.py (commit-msg [#id] hook core)."""

import importlib.util
from pathlib import Path

_H = Path(__file__).resolve().parent.parent / "scripts" / "check_backlog_commit_msg.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_backlog_commit_msg", _H)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hook = _load()

# unified diff fragments (git diff -U0 style: removed lines prefixed '-', added '+')
D_REMOVE = "@@ -10 +9 @@\n-- [#5] [P1][M] foo · Done when: x\n"
D_REWORD = "@@ -10 +10 @@\n-- [#5] [P1][M] old · Done when: x\n+- [#5] [P1][M] new · Done when: x\n"
D_MULTI = "@@ -10 +8 @@\n-- [#5] [P1][M] a · Done when: x\n-- [#6] [P3][S] b · Done when: y\n"
D_ADD_ONLY = "@@ -0 +1 @@\n+- [#7] [P2][M] new task · Done when: z\n"


def test_remove_without_ref_is_flagged():
    assert hook.check("refactor: drop a task", D_REMOVE) == ["5"]


def test_remove_with_closes_passes():
    assert hook.check("chore: relocate, closes [#5]", D_REMOVE) == []


def test_remove_with_bare_id_passes():
    assert hook.check("refactor: rework [#5]", D_REMOVE) == []


def test_reword_does_not_trigger():
    assert hook.check("docs: reword task", D_REWORD) == []


def test_multi_id_partial_reference():
    assert hook.check("chore: closes [#5]", D_MULTI) == ["6"]


def test_multi_id_both_referenced_passes():
    assert hook.check("chore: closes [#5] and [#6]", D_MULTI) == []


def test_add_only_does_not_trigger():
    assert hook.check("feat: add a task", D_ADD_ONLY) == []


def test_no_backlog_change_passes():
    assert hook.check("docs: unrelated change", "") == []
