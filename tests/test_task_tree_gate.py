"""Coverage for the [#433] C1 gate-arm — `task_tree_coherence` in scripts/audit.py.

The gap this closes, quoted from ARCHITECTURE Ch5: "`--check` is a *mode*, not a wired
gate -- no pre-commit hook and no `audit.py` check invokes it." The headline case here is
the WITNESSED one: a BACKLOG edit without a regen must FAIL the leg.
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit as aud
import gen_task_tree as gtt

REPO_ROOT = Path(__file__).resolve().parent.parent


def _git_repo(root: Path) -> Path:
    """A committed git repo carrying the two required hub artifacts.

    Needed because the check now consults index/worktree agreement BEFORE reading, so a
    bare tmp dir short-circuits on "git could not compare" long before the path under test.
    """
    import subprocess

    def git(*a):
        subprocess.run(["git", *a], cwd=root, check=True, capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "t")
    (root / "BACKLOG.md").write_text("# BACKLOG\n", encoding="utf-8")
    (root / "tasks").mkdir()
    (root / "tasks" / ".keep").write_text("", encoding="utf-8")
    git("add", "-A")
    git("commit", "-qm", "fixture")
    return root


def _status(findings) -> str:
    assert len(findings) == 1, f"expected exactly one Finding, got {findings!r}"
    return findings[0].status


def _edit_first_task_line(text: str, suffix: str) -> str:
    """Append `suffix` to the END of the first task line found in the CURRENT BACKLOG.md.

    Located from the fixture rather than hardcoded, deliberately. These tests used to pin
    the literal `- [#436]`; when that row closed and left the file the mutation became a
    silent no-op, so the gate stayed (correctly) green and three tests failed for a reason
    that had nothing to do with the gate they exercise. A fixture naming a specific id
    rots the day that id closes -- and two of the three call sites had no `assert marker
    in text` guard, so it rotted quietly.

    Appended to the line TAIL, also deliberately: inserting after the `[#id]` marker lands
    ahead of the `**title**`, which changes the DERIVED SLUG and therefore the filename.
    The import path would then emit a new filename and leave the old one holding the same
    id — a rename remnant that (correctly) REDs the duplicate-id ledger leg, failing the
    test for a reason it is not about. Editing the tail keeps title and filename stable.
    """
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if gtt._TASK_RE.match(line):
            lines[i] = line + suffix
            return "\n".join(lines)
    raise AssertionError("fixture BACKLOG.md carries no task row to mutate")


def _seed_tree(tmp_path: Path) -> tuple[Path, Path]:
    """A minimal repo-shaped fixture: real BACKLOG.md + a freshly generated tasks/ tree."""
    source = tmp_path / "BACKLOG.md"
    shutil.copyfile(REPO_ROOT / "BACKLOG.md", source)
    out_dir = tmp_path / "tasks"
    out_dir.mkdir()
    text = source.read_bytes().decode("utf-8")
    gtt.write_tree(gtt.parse_backlog(text), out_dir)
    return source, out_dir


def test_backlog_edit_without_regen_fails_the_leg(tmp_path):
    """THE WITNESSED CLASS — edit BACKLOG.md, skip the regen, and the gate must FAIL.

    Before this leg existed, exactly this sequence left the committed tree stale at commit
    time (at b4dd3e48: two task files stale, [#435]/[#436] missing, manifest and full
    reassembly both mismatched) with nothing blocking it.
    """
    source, out_dir = _seed_tree(tmp_path)
    assert gtt.find_incoherences(source, out_dir) == [], "fixture should start coherent"

    text = source.read_bytes().decode("utf-8")
    source.write_bytes(_edit_first_task_line(text, " EDITED-WITHOUT-REGEN").encode("utf-8"))

    problems = gtt.find_incoherences(source, out_dir)
    assert problems, "a BACKLOG edit without regen must be detected"
    assert _status(aud._task_tree_findings(problems)) == "fail"


def test_regen_after_the_edit_restores_green(tmp_path):
    """The failure is actionable, not sticky: regenerating clears it."""
    source, out_dir = _seed_tree(tmp_path)
    text = source.read_bytes().decode("utf-8")
    source.write_bytes(_edit_first_task_line(text, " EDITED").encode("utf-8"))
    assert gtt.find_incoherences(source, out_dir)

    gtt.write_tree(gtt.parse_backlog(source.read_bytes().decode("utf-8")), out_dir)
    assert gtt.find_incoherences(source, out_dir) == []
    assert _status(aud._task_tree_findings([])) == "pass"


def test_missing_task_file_is_detected(tmp_path):
    """The specific drift shape witnessed at b4dd3e48 — a row with no emitted file."""
    source, out_dir = _seed_tree(tmp_path)
    victim = next(p for p in sorted(out_dir.glob("*.md")) if p.name[0].isdigit())
    victim.unlink()
    problems = gtt.find_incoherences(source, out_dir)
    assert any("missing task file" in p for p in problems), problems


def test_unreferenced_foreign_task_file_is_detected(tmp_path):
    """Post-flip ([#439]) an unreferenced task-shaped file is only legitimate when it is
    OUR retired allocation record. This one carries no provenance marker, so it is foreign
    and must still be surfaced — otherwise 'retired' becomes a hiding place."""
    source, out_dir = _seed_tree(tmp_path)
    (out_dir / "999-a-task-that-no-longer-exists.md").write_bytes(b"---\nid: \"[#999]\"\n---\n")
    problems = gtt.find_incoherences(source, out_dir)
    assert any("foreign" in p.lower() for p in problems), problems


def test_missing_source_tree_is_a_problem_not_a_crash(tmp_path):
    """Post-flip the absent directory is the SOURCE, not a regenerable derivative."""
    source = tmp_path / "BACKLOG.md"
    shutil.copyfile(REPO_ROOT / "BACKLOG.md", source)
    problems = gtt.find_incoherences(source, tmp_path / "tasks")
    assert problems and "source tree missing" in problems[0]


def test_cli_check_still_exits_nonzero_on_drift(tmp_path, capsys):
    """The extraction must not have changed CLI behaviour — `--check` still exits 1 and
    prints each problem to stderr."""
    source, out_dir = _seed_tree(tmp_path)
    next(p for p in sorted(out_dir.glob("*.md")) if p.name[0].isdigit()).unlink()
    assert gtt._cmd_check(source, out_dir) == 1
    assert "check FAIL" in capsys.readouterr().err


def test_cli_check_exits_zero_when_coherent(tmp_path, capsys):
    source, out_dir = _seed_tree(tmp_path)
    assert gtt._cmd_check(source, out_dir) == 0
    assert "check ok" in capsys.readouterr().out


def test_registered_and_green_on_live_repo():
    """Registered in ALL_CHECKS (so it is a ship-gate leg) and GREEN on the live hub —
    i.e. the committed tree is coherent as shipped, which it was not before this arc."""
    assert aud.check_task_tree_coherence in aud.ALL_CHECKS
    assert _status(aud.check_task_tree_coherence(REPO_ROOT)) == "pass"


def test_check_is_read_only(tmp_path):
    """A gate that silently regenerates what it measures cannot fail. Pin that it doesn't:
    running the check over a drifted tree must leave the tree drifted."""
    source, out_dir = _seed_tree(tmp_path)
    victim = next(p for p in sorted(out_dir.glob("*.md")) if p.name[0].isdigit())
    victim.unlink()
    before = sorted(p.name for p in out_dir.iterdir())
    aud._task_tree_findings(gtt.find_incoherences(source, out_dir))
    assert sorted(p.name for p in out_dir.iterdir()) == before
    assert not victim.exists()


def test_missing_hub_artifacts_fail_rather_than_na(tmp_path, monkeypatch):
    """terra HIGH (2026-07-27) — a missing BACKLOG.md or tasks/ returned `n/a` on the hub,
    which ship-gate does not block on. Deleting the derived tree would therefore have
    DISARMED the very gate that exists to notice the tree drifting. `n/a` is reserved for
    the off-hub guard; on the hub an absent artifact is a FAIL."""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    findings = aud.check_task_tree_coherence(tmp_path)
    assert _status(findings) == "fail", findings
    ev = findings[0].evidence
    assert "BACKLOG.md" in ev and "tasks/" in ev


def test_off_hub_is_na_not_fail(tmp_path):
    """The off-hub guard still short-circuits: a consumer repo has no tasks/ tree and must
    not be failed for it."""
    findings = aud.check_task_tree_coherence(tmp_path)
    assert _status(findings) == "n/a"


def test_every_problem_path_is_present():
    """terra asked whether the _cmd_check -> find_incoherences extraction dropped a path.
    Pin the full set of problem shapes the core can emit.

    Rewritten at the [#439] flip: the shapes changed with the direction. The pre-flip set
    described a tree checked against a file ("task file content differs",
    "manifest.json differs", "orphan task-shaped file"); the post-flip set describes a
    FILE checked against a tree, plus the frontmatter-honesty leg the flip made necessary.
    This test is a coverage ratchet, so it is updated deliberately, never relaxed.
    """
    import inspect

    # The shapes live across find_incoherences + _scan_source since the [#439] 7th-pass
    # split (identity problems, which a regen must REFUSE on, vs stale-frontmatter ones,
    # which it repairs). Grep both, or the ratchet silently stops covering the larger half.
    src = inspect.getsource(gtt.find_incoherences) + inspect.getsource(gtt._scan_source)
    for shape in ("source tree missing", "missing manifest.json", "manifest.json unreadable",
                  "no 'nodes' list", "missing task file", "unreadable or malformed",
                  "frontmatter disagrees with its own body", "placement:",
                  "foreign task-shaped file", "reassemble_from_tree",
                  "does not match what tasks/ generates", "generated_sha256"):
        assert shape in src, f"problem path lost: {shape}"


def test_artifact_read_error_fails_rather_than_warns(monkeypatch, tmp_path):
    """terra HIGH RE-REVIEW — a blanket `except Exception -> warn` let malformed artifacts
    slip past a gate documented as FAIL-class (the commit-time audit-health gate blocks
    only on `fail`). Artifact read/parse errors must FAIL."""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    _git_repo(tmp_path)

    def boom(_source, _out):
        raise ValueError("simulated malformed derived tree")

    monkeypatch.setattr(aud._gtt, "find_incoherences", boom)
    findings = aud.check_task_tree_coherence(tmp_path)
    assert _status(findings) == "fail", findings
    assert "could not complete" in findings[0].evidence


def test_programming_defect_is_not_laundered_into_a_status(monkeypatch, tmp_path):
    """Anything outside the artifact-error set is a defect and must propagate, not be
    converted into a passing or merely-warning Finding."""
    import pytest

    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    _git_repo(tmp_path)

    def boom(_source, _out):
        raise ZeroDivisionError("programming defect")

    monkeypatch.setattr(aud._gtt, "find_incoherences", boom)
    with pytest.raises(ZeroDivisionError):
        aud.check_task_tree_coherence(tmp_path)


def test_index_worktree_divergence_refuses_to_answer(tmp_path, monkeypatch):
    """terra HIGH (5th pass) — the coherence read is a WORKING-TREE read, so a staged
    BACKLOG change hidden by restoring the working copy would let the gate bless a coherent
    OLD tree while the commit records an incoherent source/tree pair. When index and
    working tree disagree on these paths the check refuses to answer rather than answering
    about the wrong bytes."""
    import subprocess

    def git(*a):
        subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True)

    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "t")
    source = tmp_path / "BACKLOG.md"
    shutil.copyfile(REPO_ROOT / "BACKLOG.md", source)
    out_dir = tmp_path / "tasks"
    out_dir.mkdir()
    gtt.write_tree(gtt.parse_backlog(source.read_bytes().decode("utf-8")), out_dir)
    git("add", "-A")
    git("commit", "-qm", "coherent")
    assert _status(aud.check_task_tree_coherence(tmp_path)) == "pass"

    original = source.read_bytes()
    source.write_bytes(_edit_first_task_line(original.decode("utf-8"), " STAGED-ONLY").encode("utf-8"))
    git("add", "BACKLOG.md")
    source.write_bytes(original)          # restore the working copy -- the hiding move
    findings = aud.check_task_tree_coherence(tmp_path)
    assert _status(findings) == "fail", findings
    assert "index and working tree disagree" in findings[0].evidence


def test_git_probe_failure_blocks_rather_than_skipping(tmp_path, monkeypatch):
    """terra HIGH (6th pass) — skipping the divergence guard when the git probe could not
    complete reopened the exact staged-content hiding path the guard exists to close. An
    unknown answer is not agreement."""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    (tmp_path / "BACKLOG.md").write_text("# BACKLOG\n", encoding="utf-8")
    (tmp_path / "tasks").mkdir()
    monkeypatch.setattr(aud, "_git", lambda *a, **k: None)
    findings = aud.check_task_tree_coherence(tmp_path)
    assert _status(findings) == "fail", findings
    assert "could not compare" in findings[0].evidence


def test_staged_backlog_with_unstaged_tasks_is_divergence(tmp_path, monkeypatch):
    """terra HIGH (7th pass) — the helper INTERSECTED staged and unstaged path lists, so
    DIFFERENT monitored paths diverging returned "ok": a staged BACKLOG.md alongside a
    regenerated-but-unstaged tasks/ blessed a coherent working tree while the commit
    recorded only half of it, leaving a stale derived tree."""
    import subprocess

    def git(*a):
        subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True)

    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    _git_repo(tmp_path)
    (tmp_path / "BACKLOG.md").write_text("# BACKLOG edited\n", encoding="utf-8")
    git("add", "BACKLOG.md")
    (tmp_path / "tasks" / ".keep").write_text("regenerated but unstaged\n", encoding="utf-8")

    state, divergent = aud._index_worktree_divergence(tmp_path, "BACKLOG.md", "tasks")
    assert state == "diverged", (state, divergent)
    assert any("tasks/" in d for d in divergent), divergent
    assert _status(aud.check_task_tree_coherence(tmp_path)) == "fail"


def test_unstaged_backlog_with_staged_tasks_is_divergence(tmp_path, monkeypatch):
    """The inverse arrangement must also be caught."""
    import subprocess

    def git(*a):
        subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True)

    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    _git_repo(tmp_path)
    (tmp_path / "tasks" / ".keep").write_text("regenerated\n", encoding="utf-8")
    git("add", "tasks")
    (tmp_path / "BACKLOG.md").write_text("# BACKLOG edited but unstaged\n", encoding="utf-8")

    state, divergent = aud._index_worktree_divergence(tmp_path, "BACKLOG.md", "tasks")
    assert state == "diverged", (state, divergent)
    assert "BACKLOG.md" in divergent, divergent


def test_untracked_generated_task_file_counts_as_divergence(tmp_path, monkeypatch):
    """A newly generated task file is invisible to `git diff`, so omitting untracked files
    would leave the same hole for the ADD case."""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    _git_repo(tmp_path)
    (tmp_path / "tasks" / "999-brand-new.md").write_text("new\n", encoding="utf-8")
    state, divergent = aud._index_worktree_divergence(tmp_path, "BACKLOG.md", "tasks")
    assert state == "diverged", (state, divergent)
    assert any("999-brand-new" in d for d in divergent), divergent


def test_clean_tree_is_ok(tmp_path, monkeypatch):
    """The negative case: a committed, clean tree reports agreement, so the guard does not
    fire on every ordinary run."""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    _git_repo(tmp_path)
    assert aud._index_worktree_divergence(tmp_path, "BACKLOG.md", "tasks") == ("ok", [])
