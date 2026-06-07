"""Unit tests for scripts/changelog_sentinel.py (#113 version sentinel).

Targets the pure core: version parsing, the strict-newer compare, and the
evaluate() decision (fires when installed > reviewed, silent otherwise).
"""

import importlib.util
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "scripts" / "changelog_sentinel.py"


def _load():
    spec = importlib.util.spec_from_file_location("changelog_sentinel", _P)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cs = _load()


# --- parse_version ----------------------------------------------------------

def test_parse_version_claude_format():
    assert cs.parse_version("2.1.168 (Claude Code)") == (2, 1, 168)


def test_parse_version_codex_format():
    assert cs.parse_version("codex-cli 0.136.0") == (0, 136, 0)


def test_parse_version_none_on_garbage():
    assert cs.parse_version("no version here") is None
    assert cs.parse_version("") is None


# --- is_newer ---------------------------------------------------------------

def test_is_newer_true_when_patch_ahead():
    assert cs.is_newer((2, 1, 168), (2, 1, 167)) is True


def test_is_newer_false_when_equal():
    assert cs.is_newer((0, 136, 0), (0, 136, 0)) is False


def test_is_newer_false_when_older():
    assert cs.is_newer((0, 135, 9), (0, 136, 0)) is False


def test_is_newer_handles_length_mismatch():
    assert cs.is_newer((2, 1), (2, 1, 0)) is False        # 2.1 == 2.1.0
    assert cs.is_newer((2, 1, 1), (2, 1)) is True         # 2.1.1 > 2.1
    assert cs.is_newer(None, (2, 1, 0)) is False
    assert cs.is_newer((2, 1, 0), None) is False


# --- evaluate (the witnessed both-branches scenario) ------------------------

_STATE = {
    "claude-code": {"last_reviewed_version": "2.1.167"},
    "codex": {"last_reviewed_version": "0.136.0"},
}


def test_evaluate_fires_for_claude_silent_for_codex():
    # the live seed scenario: claude 2.1.168 installed (gap), codex 0.136.0 (current)
    installed = {"claude-code": "2.1.168 (Claude Code)", "codex": "codex-cli 0.136.0"}
    lines = cs.evaluate(_STATE, installed)
    assert len(lines) == 1
    assert lines[0].startswith("[changelog] claude-code 2.1.168 > last reviewed 2.1.167")
    assert "/changelog-review" in lines[0]


def test_evaluate_silent_when_all_current():
    installed = {"claude-code": "2.1.167 (Claude Code)", "codex": "codex-cli 0.136.0"}
    assert cs.evaluate(_STATE, installed) == []


def test_evaluate_fires_for_both_when_both_behind():
    installed = {"claude-code": "2.2.0 (Claude Code)", "codex": "codex-cli 0.137.0"}
    lines = cs.evaluate(_STATE, installed)
    assert len(lines) == 2


def test_evaluate_silent_when_version_unreadable():
    # a tool whose --version failed (empty) must not fire (fail-soft, no false nudge)
    installed = {"claude-code": "", "codex": "codex-cli 0.136.0"}
    assert cs.evaluate(_STATE, installed) == []


def test_evaluate_silent_when_reviewed_ahead_of_installed():
    # operator reviewed 0.137.0 but only 0.136.0 installed -> no nudge
    state = {"codex": {"last_reviewed_version": "0.137.0"}, "claude-code": {"last_reviewed_version": "2.1.168"}}
    installed = {"claude-code": "2.1.168 (Claude Code)", "codex": "codex-cli 0.136.0"}
    assert cs.evaluate(state, installed) == []
