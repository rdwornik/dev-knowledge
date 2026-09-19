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


# --- codex-review HIGH findings (2026-09-18, b2-lane2-organ-invocations), RED-first ------

def test_python_dash_m_dotted_module_invocation_counts_as_a_call(tmp_path):
    """HIGH: substring matching never recognised `python -m scripts.codemap.cli` -- no `.py`
    substring exists on that line, so a module-form organ (the codemap/toc entry points'
    OWN documented call shape, per `.pre-commit-config.yaml`) always read UNCALLED."""
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    procs = {"scripts/codemap/cli.py": "script"}
    _transcript(session_dir, "session-a", [
        _tool_use("Bash",
                  {"command": "uv run --locked python -m scripts.codemap.cli check ."},
                  ts="2026-09-16T10:00:00.000Z", uuid="1"),
    ])
    report = oum.process_census(
        repo_root=repo_root, sessions_root=session_dir.parent, processes=procs,
        now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))
    assert report["counts"]["scripts/codemap/cli.py"] == 1
    assert "scripts/codemap/cli.py" not in report["uncalled"]


def test_a_path_passed_as_an_argument_to_a_different_tool_does_not_count(tmp_path):
    """HIGH: `uv run ruff check scripts/graph_queries.py` only names the path as RUFF's
    argument -- it does not run `scripts/graph_queries.py`. Whole-line substring matching
    counted this as an invocation; the census must identify the actual operand."""
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    procs = {"scripts/graph_queries.py": "script"}
    _transcript(session_dir, "session-a", [
        _tool_use("Bash", {"command": "uv run ruff check scripts/graph_queries.py"},
                  ts="2026-09-16T10:00:00.000Z", uuid="1"),
    ])
    report = oum.process_census(
        repo_root=repo_root, sessions_root=session_dir.parent, processes=procs,
        now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))
    assert report["counts"]["scripts/graph_queries.py"] == 0
    assert "scripts/graph_queries.py" in report["uncalled"]


def test_not_observable_processes_never_appear_in_counts_json(tmp_path):
    """HIGH: `counts` used to hold an explicit `0` for command/skill processes even though
    they are labelled NOT OBSERVABLE -- a JSON consumer reading `counts["<skill>"] == 0`
    cannot tell that from a real zero. They must be absent from `counts` entirely."""
    repo_root, session_dir = _repo_and_sessions(tmp_path)
    report = oum.process_census(
        repo_root=repo_root, sessions_root=session_dir.parent / "nonexistent",
        processes=_PROCS, now=datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc))
    assert ".claude/commands/preflight.md" not in report["counts"]
    assert ".claude/skills/verify/SKILL.md" not in report["counts"]


# --- the census that lied twice (NIGHT WAVE 2, L4): reachable is CALLED, RED-first ---------
#
# A transcript records local Claude Code tool calls. A git hook, a CI workflow and an `import`
# never appear in one, so a count over transcripts alone reported 90 of 159 observable
# processes "uncalled" -- 77 of them are reached by a wiring surface or by an import chain
# (measured live, 2026-09-19). One of those errors was a regex that missed `from .check_x
# import`: `audit_checks/registry.py` has 23 relative imports. FPG-1 already holds the
# `triggers` + `imports` relation (relative imports included), so the census READS it rather
# than computing a second opinion.

import pytest  # noqa: E402

import graph_store as gs  # noqa: E402


@pytest.fixture(scope="module")
def wired_repo(tmp_path_factory):
    """A tree with four processes: one reachable ONLY from a git hook, one ONLY from CI, one
    ONLY through a RELATIVE import, and one that nothing reaches (must stay uncalled)."""
    root = tmp_path_factory.mktemp("wired")
    files = {
        ".pre-commit-config.yaml": (
            "repos:\n"
            "  - repo: local\n"
            "    hooks:\n"
            "      - id: hook-only\n"
            "        name: hook only\n"
            "        entry: python scripts/hook_only.py\n"
            "        language: system\n"
            "      - id: registry\n"
            "        name: registry\n"
            "        entry: python scripts/checks/registry.py\n"
            "        language: system\n"),
        ".github/workflows/ci.yml": (
            "name: ci\non: push\njobs:\n  x:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - run: python scripts/ci_only.py\n"),
        "scripts/hook_only.py": "print('hook')\n",
        "scripts/ci_only.py": "print('ci')\n",
        "scripts/checks/__init__.py": "",
        "scripts/checks/registry.py": "from .check_x import run\n",
        "scripts/checks/check_x.py": "def run():\n    return 1\n",
        "scripts/orphan.py": "print('nobody calls me')\n",
    }
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    gs.rebuild(root)
    return root


def _census_of(root, tmp_path):
    return oum.process_census(
        repo_root=root, sessions_root=tmp_path / "no-transcripts",
        now=datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc))


def test_organ_reachable_only_from_a_git_hook_is_not_reported_uncalled(wired_repo, tmp_path):
    report = _census_of(wired_repo, tmp_path)
    assert "scripts/hook_only.py" not in report["uncalled"]


def test_organ_reachable_only_from_ci_is_not_reported_uncalled(wired_repo, tmp_path):
    report = _census_of(wired_repo, tmp_path)
    assert "scripts/ci_only.py" not in report["uncalled"]


def test_organ_reachable_only_by_a_relative_import_is_not_reported_uncalled(
        wired_repo, tmp_path):
    """`registry.py` does `from .check_x import run` -- `check_x.py` has no other caller."""
    report = _census_of(wired_repo, tmp_path)
    assert "scripts/checks/check_x.py" not in report["uncalled"]


def test_a_process_nothing_reaches_is_still_reported_uncalled(wired_repo, tmp_path):
    """The fix must not over-report: an unwired, never-invoked script stays UNCALLED."""
    report = _census_of(wired_repo, tmp_path)
    assert "scripts/orphan.py" in report["uncalled"]


def test_reachable_processes_are_named_separately_from_transcript_invoked(wired_repo, tmp_path):
    """Called-by-wiring is a DIFFERENT fact from called-in-a-transcript; the report keeps both
    so a reader can tell 'runs invisibly' from 'seen running'."""
    report = _census_of(wired_repo, tmp_path)
    for path in ("scripts/hook_only.py", "scripts/ci_only.py", "scripts/checks/check_x.py"):
        assert path in report["wiring_reachable"]
        assert report["counts"][path] == 0        # no transcript saw it
    assert "scripts/orphan.py" not in report["wiring_reachable"]
    text = oum.render_census(report)
    assert "wiring-reachable" in text.lower()
    assert "\t" not in text


def test_reachable_can_be_injected_without_a_store(tmp_path):
    """The seam a unit test uses -- same split `organs=` gives `organ_usage_report`."""
    report = oum.process_census(
        repo_root=tmp_path, sessions_root=tmp_path / "nope", processes=_PROCS,
        reachable=frozenset({"scripts/graph_queries.py"}),
        now=datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc))
    assert "scripts/graph_queries.py" not in report["uncalled"]
    assert "scripts/impacted_tests.py" in report["uncalled"]


def test_census_never_writes_a_store_it_only_reads(tmp_path):
    """Codex terra P1 (pass 3): a report over `--repo-root <sibling>` must not rebuild and write
    that repo's git-admin graph. The census READS the persisted store; the graph-rebuild
    pre-commit hook is the freshness contract."""
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "a.py").write_text("print(1)\n", encoding="utf-8")
    oum.process_census(repo_root=root, sessions_root=tmp_path / "none",
                       now=datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc))
    assert not gs.store_path(root).exists()


def test_census_says_when_the_graph_it_read_is_stale(tmp_path):
    """Read-only means stale is possible, so it is SAID, not hidden: `graph_stale` is True when
    a source file is newer than the store. One-directional -- `is_stale` scans a coarse set of
    trees, so False is 'not proven stale', never 'proven fresh'."""
    import os
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "a.py").write_text("print(1)\n", encoding="utf-8")
    gs.rebuild(root)
    fresh = oum.process_census(repo_root=root, sessions_root=tmp_path / "none",
                               now=datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc))
    assert fresh["graph_stale"] is False
    later = os.stat(gs.store_path(root)).st_mtime + 10
    os.utime(root / "scripts" / "a.py", (later, later))
    stale = oum.process_census(repo_root=root, sessions_root=tmp_path / "none",
                               now=datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc))
    assert stale["graph_stale"] is True
    assert "STALE" in oum.render_census(stale)



@pytest.mark.parametrize("surface", [".github/workflows/ci.yml", ".pre-commit-config.yaml",
                                     ".pre-commit-hooks.yaml"])
def test_a_wiring_surface_edit_after_the_build_makes_the_graph_stale(tmp_path, surface):
    """Codex terra P1 (pass 4): `graph_store.is_stale` scans source trees but NOT the wiring
    surfaces, so a workflow/hook-config edit left `graph_stale` False while reachability read
    obsolete edges. The census adds the wiring surfaces to its own staleness check (the
    `graph_store` gap itself is outside this lane, handed back)."""
    import os
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "a.py").write_text("print(1)" + chr(92) + "n", encoding="utf-8")
    target = root / surface
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("name: x" + chr(92) + "n", encoding="utf-8")
    gs.rebuild(root)
    kwargs = dict(repo_root=root, sessions_root=tmp_path / "none",
                  now=datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc))
    assert oum.process_census(**kwargs)["graph_stale"] is False
    later = os.stat(gs.store_path(root)).st_mtime + 10
    os.utime(target, (later, later))
    assert oum.process_census(**kwargs)["graph_stale"] is True


def test_a_deleted_wiring_surface_makes_the_graph_stale(tmp_path):
    """Codex terra P1 (pass 5): the mtime check sees added/edited surfaces only. A deleted
    workflow leaves its trigger edges in the store; the stored root set no longer matches the
    surfaces on disk, and that is stale."""
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "a.py").write_text("print(1)" + chr(92) + "n", encoding="utf-8")
    workflow = root / ".github" / "workflows" / "ci.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("name: x" + chr(92) + "n", encoding="utf-8")
    gs.rebuild(root)
    kwargs = dict(repo_root=root, sessions_root=tmp_path / "none",
                  now=datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc))
    assert oum.process_census(**kwargs)["graph_stale"] is False
    workflow.unlink()
    assert oum.process_census(**kwargs)["graph_stale"] is True


def test_an_unreadable_store_degrades_to_stale_not_a_crash(tmp_path):
    """Codex terra P1 (pass 6): `wiring_reachable` degrades on a corrupt store; the staleness
    check must too, or the census aborts instead of reporting an unreadable graph."""
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "a.py").write_text("print(1)" + chr(92) + "n", encoding="utf-8")
    db = gs.store_path(root)
    db.parent.mkdir(parents=True, exist_ok=True)
    db.write_bytes(b"this is not a sqlite database" * 50)
    report = oum.process_census(
        repo_root=root, sessions_root=tmp_path / "none", processes={"scripts/a.py": "script"},
        now=datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc))
    assert report["graph_stale"] is True
    assert report["wiring_reachable"] == []


def test_a_deleted_or_added_process_file_makes_the_graph_stale(tmp_path):
    """Codex terra P1 (pass 7): `is_stale` compares mtimes of files that still exist, so a
    deleted process file kept its edges in `wiring_reachable` while `graph_stale` read False.
    The census's own subject is the process set, so that comparison is exact: the store's
    process paths vs the process files on disk."""
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    for name in ("a.py", "b.py"):
        (root / "scripts" / name).write_text("print(1)" + chr(92) + "n", encoding="utf-8")
    gs.rebuild(root)
    kwargs = dict(repo_root=root, sessions_root=tmp_path / "none",
                  now=datetime(2026, 9, 19, 12, 0, tzinfo=timezone.utc))
    assert oum.process_census(**kwargs)["graph_stale"] is False
    (root / "scripts" / "b.py").unlink()
    assert oum.process_census(**kwargs)["graph_stale"] is True
