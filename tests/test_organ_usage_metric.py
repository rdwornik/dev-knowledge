"""Tests for `scripts/organ_usage_metric.py` -- AX9-5's metric, RED-first (`[#694]`).

THE TARGET, verbatim from the roster (intake 93 Part 9) and the row's own clause: "raw-search
calls versus organ calls per session, and organs never called in 30 days" -- "the operator sees
in one number whether the model uses the harness or rebuilds it."

WHAT THESE TESTS REFUSE:
  1. A `Grep` call, or a `Bash`/`PowerShell` command headed by a search tool, going untallied as
     `raw_search` -- the metric's whole numerator would read zero on a session that spent it
     entirely re-deriving what an organ already answers.
  2. A `Bash` call naming a known organ path going untallied as `organ_call` -- the denominator
     the ratio needs to mean anything.
  3. An organ NEVER called (or last called outside the window) not appearing in
     `organs_uncalled` -- the half of AX9-5 that answers "which tool did the model never pick up".
  4. A tool call the classifier does not recognise (`Read`, `Write`, ...) landing in EITHER
     bucket -- the ratio is over two named classes, not a partition of every call.

WHAT THEY DO NOT TEST. That any REAL session's transcripts classify a particular way -- that
would put a second, drifting copy of live session content in the suite. Every fixture here is a
synthetic transcript this test writes and reads back, the same posture `test_lane_cost.py`
established for the same class of problem.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import organ_usage_metric as oum


# --- helpers ----------------------------------------------------------------------------

def _tool_use(name: str, tool_input: dict, *, ts: str, uuid: str) -> str:
    """One `tool_use` turn in the Claude Code transcript shape (confirmed against a live
    transcript this session's own JSONL -- see the lane's design notes)."""
    return json.dumps({
        "timestamp": ts,
        "message": {
            "id": f"msg_{uuid}",
            "content": [{"type": "tool_use", "id": f"call_{uuid}", "name": name,
                        "input": tool_input}],
        },
    })


def _read_only(*, ts: str, uuid: str) -> str:
    return json.dumps({
        "timestamp": ts,
        "message": {
            "id": f"msg_{uuid}",
            "content": [{"type": "tool_use", "id": f"call_{uuid}", "name": "Read",
                        "input": {"file_path": "scripts/graph_queries.py"}}],
        },
    })


def _transcript(dir_path, name: str, lines: list[str]):
    dir_path.mkdir(parents=True, exist_ok=True)
    path = dir_path / f"{name}.jsonl"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


_ORGANS = frozenset({"scripts/graph_queries.py", "scripts/impacted_tests.py"})


# --- LIE 1: a search call goes untallied -----------------------------------------------

def test_grep_tool_call_classifies_as_raw_search():
    assert oum.classify_tool_call("Grep", {"pattern": "foo"}, _ORGANS) == "raw_search"


def test_bash_call_headed_by_a_search_tool_classifies_as_raw_search():
    assert oum.classify_tool_call(
        "Bash", {"command": "grep -rn TODO scripts/"}, _ORGANS) == "raw_search"


def test_powershell_select_string_classifies_as_raw_search():
    assert oum.classify_tool_call(
        "PowerShell", {"command": "Select-String -Pattern TODO -Path scripts/*.py"},
        _ORGANS) == "raw_search"


# --- LIE 2: an organ call goes untallied -------------------------------------------------

def test_bash_call_naming_a_known_organ_classifies_as_organ_call():
    assert oum.classify_tool_call(
        "Bash", {"command": "uv run --locked python scripts/graph_queries.py list"},
        _ORGANS) == "organ_call"


def test_a_search_headed_command_wins_over_an_organ_mention_in_the_same_line():
    """A command that both greps AND names an organ path (e.g. grepping the organ's own
    source) is a search, not a call -- the head verb is what ran, not what the args mention."""
    assert oum.classify_tool_call(
        "Bash", {"command": "grep -n def scripts/graph_queries.py"}, _ORGANS) == "raw_search"


# --- LIE 4: an unclassifiable call must land in neither bucket --------------------------

def test_read_tool_call_classifies_as_neither():
    assert oum.classify_tool_call("Read", {"file_path": "scripts/graph_queries.py"},
                                  _ORGANS) is None


def test_bash_call_naming_no_search_tool_and_no_organ_classifies_as_neither():
    assert oum.classify_tool_call("Bash", {"command": "uv run --locked pytest -x"},
                                  _ORGANS) is None


# --- report(): per-session tallies and the uncalled-in-window half -----------------------

def _repo_and_sessions(tmp_path):
    """A `repo_root` and a matching session-store directory, named so
    `organ_usage_metric._session_dirs`'s segment matcher finds it -- the repo's own
    directory name must appear as a dash-bounded segment of the session dir's name, the
    same predicate `lane_cost.transcript_dirs` applies to a lane slug."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    sessions_root = tmp_path / "projects"
    return repo_root, sessions_root / repo_root.name


def test_report_tallies_raw_search_and_organ_call_per_session(tmp_path):
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    sessions_root = session_dir.parent
    _transcript(session_dir, "session-a", [
        _tool_use("Grep", {"pattern": "foo"}, ts="2026-09-16T10:00:00.000Z", uuid="1"),
        _tool_use("Bash", {"command": "uv run --locked python scripts/graph_queries.py list"},
                  ts="2026-09-16T10:00:01.000Z", uuid="2"),
        _tool_use("Bash", {"command": "uv run --locked python scripts/graph_queries.py list"},
                  ts="2026-09-16T10:00:02.000Z", uuid="3"),
        _read_only(ts="2026-09-16T10:00:03.000Z", uuid="4"),
    ])

    report = oum.organ_usage_report(
        repo_root=repo_root, sessions_root=sessions_root, organs=_ORGANS,
        now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))

    assert report["totals"] == {"raw_search": 1, "organ_call": 2}
    assert report["sessions"]["session-a"] == {"raw_search": 1, "organ_call": 2}


def test_organ_never_called_in_any_transcript_is_reported_uncalled(tmp_path):
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    sessions_root = session_dir.parent
    _transcript(session_dir, "session-a", [
        _tool_use("Bash", {"command": "uv run --locked python scripts/graph_queries.py list"},
                  ts="2026-09-16T10:00:00.000Z", uuid="1"),
    ])

    report = oum.organ_usage_report(
        repo_root=repo_root, sessions_root=sessions_root, organs=_ORGANS,
        now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))

    assert report["organs_uncalled"] == ["scripts/impacted_tests.py"]


def test_organ_called_outside_the_window_is_reported_uncalled(tmp_path):
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    sessions_root = session_dir.parent
    _transcript(session_dir, "session-a", [
        _tool_use("Bash", {"command": "uv run --locked python scripts/impacted_tests.py check"},
                  ts="2026-08-01T10:00:00.000Z", uuid="1"),  # 46 days before `now` below
    ])

    report = oum.organ_usage_report(
        repo_root=repo_root, sessions_root=sessions_root, organs=_ORGANS, since_days=30,
        now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))

    assert "scripts/impacted_tests.py" in report["organs_uncalled"]


def test_organ_called_inside_the_window_is_not_reported_uncalled(tmp_path):
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    sessions_root = session_dir.parent
    _transcript(session_dir, "session-a", [
        _tool_use("Bash", {"command": "uv run --locked python scripts/impacted_tests.py check"},
                  ts="2026-09-15T10:00:00.000Z", uuid="1"),
    ])

    report = oum.organ_usage_report(
        repo_root=repo_root, sessions_root=sessions_root, organs=_ORGANS, since_days=30,
        now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))

    assert "scripts/impacted_tests.py" not in report["organs_uncalled"]


def test_no_matching_session_directory_reports_zero_totals_not_a_raise(tmp_path):
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    report = oum.organ_usage_report(
        repo_root=repo_root, sessions_root=session_dir.parent / "nonexistent", organs=_ORGANS)
    assert report["totals"] == {"raw_search": 0, "organ_call": 0}
    assert report["sessions"] == {}


def test_render_report_is_flat_text_naming_totals_and_uncalled_organs(tmp_path):
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    report = oum.organ_usage_report(
        repo_root=repo_root, sessions_root=session_dir.parent / "nonexistent", organs=_ORGANS)
    text = oum.render_report(report)
    assert "\t" not in text
    assert "raw_search=0" in text and "organ_call=0" in text
    for organ in _ORGANS:
        assert organ in text


# --- process_census(): B2 lane 2 -- the ratchet's real number, replacing the process-list
# "no trigger" PROXY in `protocols/BUILD-LIST.md`. RED-first ([#900]-adjacent; the F3/F4/F5
# defects the 2026-09-18 AX9-5 re-run audit found and left as proposed rows, wired here). ------

_PROCS = {
    "scripts/graph_queries.py": "script",
    "scripts/impacted_tests.py": "script",
    ".claude/commands/preflight.md": "command",
    ".claude/skills/verify/SKILL.md": "skill",
}


def test_command_class_process_is_not_observable_never_reported_uncalled(tmp_path):
    """LIE: a command/skill process with zero classified calls silently reads as UNCALLED,
    indistinguishable from a script that really was never called (F5's honesty gap, applied
    to observability rather than to mention-vs-call)."""
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    report = oum.process_census(
        repo_root=repo_root, sessions_root=session_dir.parent / "nonexistent",
        processes=_PROCS, now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))
    assert ".claude/commands/preflight.md" in report["not_observable"]
    assert ".claude/skills/verify/SKILL.md" in report["not_observable"]
    assert ".claude/commands/preflight.md" not in report["uncalled"]
    assert ".claude/skills/verify/SKILL.md" not in report["uncalled"]


def test_a_path_mention_with_no_interpreter_head_does_not_count_as_a_call(tmp_path):
    """LIE (F5): `git add scripts/graph_queries.py` is a mention, not an invocation -- the
    lenient `organ_call` classifier used by `organ_usage_report` would count this; the strict
    census must not."""
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    _transcript(session_dir, "session-a", [
        _tool_use("Bash", {"command": "git add scripts/graph_queries.py"},
                  ts="2026-09-16T10:00:00.000Z", uuid="1"),
    ])
    report = oum.process_census(
        repo_root=repo_root, sessions_root=session_dir.parent, processes=_PROCS,
        now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))
    assert report["counts"]["scripts/graph_queries.py"] == 0
    assert "scripts/graph_queries.py" in report["uncalled"]


def test_an_interpreter_headed_command_naming_the_path_counts_as_a_call(tmp_path):
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    _transcript(session_dir, "session-a", [
        _tool_use("Bash", {"command": "uv run --locked python scripts/graph_queries.py list"},
                  ts="2026-09-16T10:00:00.000Z", uuid="1"),
    ])
    report = oum.process_census(
        repo_root=repo_root, sessions_root=session_dir.parent, processes=_PROCS,
        now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))
    assert report["counts"]["scripts/graph_queries.py"] == 1
    assert "scripts/graph_queries.py" not in report["uncalled"]


def test_a_call_outside_the_window_does_not_count_towards_the_total(tmp_path):
    """LIE (F4): `organ_usage_report`'s `totals` are all-time; the census's per-process counts
    must be windowed, so an invocation 46 days ago does not hide an organ's real 30-day
    neglect."""
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    _transcript(session_dir, "session-a", [
        _tool_use("Bash", {"command": "uv run --locked python scripts/graph_queries.py list"},
                  ts="2026-08-01T10:00:00.000Z", uuid="1"),
    ])
    report = oum.process_census(
        repo_root=repo_root, sessions_root=session_dir.parent, processes=_PROCS,
        since_days=30, now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))
    assert report["counts"]["scripts/graph_queries.py"] == 0
    assert "scripts/graph_queries.py" in report["uncalled"]


def test_headline_counts_uncalled_against_observable_total_only(tmp_path):
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    report = oum.process_census(
        repo_root=repo_root, sessions_root=session_dir.parent / "nonexistent",
        processes=_PROCS, now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))
    assert report["processes_total"] == 4
    assert report["observable_total"] == 2
    assert report["not_observable_total"] == 2
    assert len(report["uncalled"]) == 2


def test_render_census_is_flat_text_with_the_headline_and_no_zero_claim_on_not_observable(
        tmp_path):
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    report = oum.process_census(
        repo_root=repo_root, sessions_root=session_dir.parent / "nonexistent",
        processes=_PROCS, since_days=30, now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))
    text = oum.render_census(report)
    assert "\t" not in text
    assert "uncalled over 30 days: 2 of 2 observable" in text
    assert "not observable" in text.lower()
    for path in report["not_observable"]:
        assert path in text


def test_canonical_repo_root_uses_git_common_dir_parent(tmp_path, monkeypatch):
    """F3: the worktree's own `.git` (a file pointing elsewhere) must not silently scope the
    census to the worktree's own single session directory -- the metric resolves the PRIMARY
    checkout root via `git rev-parse --git-common-dir` instead of using wherever it runs."""
    primary = tmp_path / "primary"
    (primary / ".git").mkdir(parents=True)
    worktree = tmp_path / "primary" / ".claude" / "worktrees" / "lane-x"
    worktree.mkdir(parents=True)

    def _fake_run(cmd, **kwargs):
        class _Result:
            returncode = 0
            stdout = str(primary / ".git") + "\n"
        assert cmd[:2] == ["git", "-C"]
        return _Result()

    monkeypatch.setattr(oum.subprocess, "run", _fake_run)
    assert oum.canonical_repo_root(worktree) == primary


def test_canonical_repo_root_falls_back_when_git_is_unavailable(tmp_path, monkeypatch):
    def _raise(cmd, **kwargs):
        raise OSError("git not found")

    monkeypatch.setattr(oum.subprocess, "run", _raise)
    fallback = tmp_path / "wherever"
    assert oum.canonical_repo_root(fallback) == fallback
