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


def _status(findings) -> str:
    assert len(findings) == 1, f"expected exactly one Finding, got {findings!r}"
    return findings[0].status


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
    marker = "- [#436]"
    assert marker in text, "fixture BACKLOG.md must carry the [#436] row"
    source.write_bytes(text.replace(marker, "- [#436] EDITED-WITHOUT-REGEN", 1).encode("utf-8"))

    problems = gtt.find_incoherences(source, out_dir)
    assert problems, "a BACKLOG edit without regen must be detected"
    assert _status(aud._task_tree_findings(problems)) == "fail"


def test_regen_after_the_edit_restores_green(tmp_path):
    """The failure is actionable, not sticky: regenerating clears it."""
    source, out_dir = _seed_tree(tmp_path)
    text = source.read_bytes().decode("utf-8")
    source.write_bytes(text.replace("- [#436]", "- [#436] EDITED", 1).encode("utf-8"))
    assert gtt.find_incoherences(source, out_dir)

    gtt.write_tree(gtt.parse_backlog(source.read_bytes().decode("utf-8")), out_dir, prune=True)
    assert gtt.find_incoherences(source, out_dir) == []
    assert _status(aud._task_tree_findings([])) == "pass"


def test_missing_task_file_is_detected(tmp_path):
    """The specific drift shape witnessed at b4dd3e48 — a row with no emitted file."""
    source, out_dir = _seed_tree(tmp_path)
    victim = next(p for p in sorted(out_dir.glob("*.md")) if p.name[0].isdigit())
    victim.unlink()
    problems = gtt.find_incoherences(source, out_dir)
    assert any("missing task file" in p for p in problems), problems


def test_orphan_task_file_is_detected(tmp_path):
    """A retired row leaving its derived file behind — the `--write --prune` lifecycle."""
    source, out_dir = _seed_tree(tmp_path)
    (out_dir / "999-a-task-that-no-longer-exists.md").write_bytes(b"---\nid: \"[#999]\"\n---\n")
    problems = gtt.find_incoherences(source, out_dir)
    assert any("orphan" in p for p in problems), problems


def test_missing_output_dir_is_a_problem_not_a_crash(tmp_path):
    source = tmp_path / "BACKLOG.md"
    shutil.copyfile(REPO_ROOT / "BACKLOG.md", source)
    problems = gtt.find_incoherences(source, tmp_path / "tasks")
    assert problems and "output dir missing" in problems[0]


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


def test_extraction_preserved_every_problem_path():
    """terra asked whether the _cmd_check -> find_incoherences extraction dropped a path.
    Pin the full set of problem shapes the core can still emit."""
    import inspect

    src = inspect.getsource(gtt.find_incoherences)
    for shape in ("cannot read source", "parse error", "output dir missing",
                  "missing task file", "task file content differs",
                  "missing manifest.json", "manifest.json differs",
                  "orphan task-shaped file", "reassemble_from_tree"):
        assert shape in src, f"problem path lost in extraction: {shape}"
