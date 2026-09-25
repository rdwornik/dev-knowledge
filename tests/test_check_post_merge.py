"""Tests for scripts/check_post_merge.py -- [#1014], RED-first.

THE INCIDENT THIS REPLAYS, verbatim from DIGEST-WAVE5A-2026-09-24.md blind spot 4: "A --no-ff
merge commit runs almost no pre-commit hooks: my first test-selection build (d908b6eb)
committed a conflict marker in JOURNAL.md and a manifest missing 45 nodes, and no hook refused
it. I caught it from the generator's refusal and discarded it before push." No pre-commit hook
fires on a merge commit's own tree, so the only way to catch this is a check that reads the
MERGE COMMIT ITSELF, after it lands and before it is pushed -- which is what this module is.

Two scratch-repo scenarios, both real git: a `--no-ff` merge landed WITH an unresolved conflict
marker (git leaves one on disk the instant a merge conflicts; the incident was committing that
without resolving it), and the same merge landed clean.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

import check_post_merge as cpm  # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")


def _run(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check,
                          capture_output=True, text=True, encoding="utf-8")


def _commit(repo, msg, *, fname="f.txt", content=None):
    (repo / fname).write_text(content if content is not None else msg, encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", msg)


def _init_repo(tmp_path) -> Path:
    repo = tmp_path / "r"
    repo.mkdir()
    _run(repo, "init", "-q")
    _run(repo, "config", "user.email", "t@t.t")
    _run(repo, "config", "user.name", "t")
    _run(repo, "branch", "-M", "main")
    _commit(repo, "seed", fname="JOURNAL.md", content="base\n")
    return repo


def _diverge(repo) -> None:
    """`main` and `feature` each edit JOURNAL.md, so merging them conflicts on that file."""
    _run(repo, "checkout", "-q", "-b", "feature")
    (repo / "JOURNAL.md").write_text("feature change\n", encoding="utf-8")
    _run(repo, "commit", "-q", "-am", "feature: edit JOURNAL.md")
    _run(repo, "checkout", "-q", "main")
    (repo / "JOURNAL.md").write_text("main change\n", encoding="utf-8")
    _run(repo, "commit", "-q", "-am", "main: edit JOURNAL.md")


def _attempt_conflicting_merge(repo) -> None:
    """`git merge --no-ff feature`, expected to CONFLICT and leave marker text on disk."""
    proc = _run(repo, "merge", "--no-ff", "--no-edit", "feature", check=False)
    assert proc.returncode != 0, "the fixture is only meaningful if the merge actually conflicts"
    assert "<<<<<<<" in (repo / "JOURNAL.md").read_text(encoding="utf-8")


@requires_git
def test_check_merge_FAILS_on_a_conflict_marker_landed_by_a_no_ff_merge(tmp_path):
    """THE INCIDENT: a merge commit whose tree still carries `<<<<<<<`/`=======`/`>>>>>>>`,
    because the conflict was never resolved -- only committed as-is (`git add -A; git commit`
    over the conflicted working tree, exactly what happened at d908b6eb)."""
    repo = _init_repo(tmp_path)
    _diverge(repo)
    _attempt_conflicting_merge(repo)
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "merge feature (unresolved)")
    sha = _run(repo, "rev-parse", "HEAD").stdout.strip()

    verdict = cpm.check_merge(repo, sha)

    assert not verdict.ok
    assert "JOURNAL.md" in {hit.path for hit in verdict.hits}
    assert any("<<<<<<<" in hit.line for hit in verdict.hits)


@requires_git
def test_check_merge_CATCHES_a_marker_baked_in_unchanged_from_one_parent(tmp_path):
    """CODEX HIGH FINDING, reproduced and fixed: a file identical to the merge's SECOND parent
    (never itself in conflict -- carried in wholesale) but different from the first still
    counts as 'touched by this merge', and a marker sitting in it must not slip through. A
    combined-diff (`git diff-tree -c`) narrowing MISSES this path entirely; measured on this
    exact fixture before the fix (`-c` named one of two genuinely-differing paths)."""
    repo = _init_repo(tmp_path)
    _run(repo, "checkout", "-q", "-b", "feature")
    (repo / "OTHER.md").write_text("<<<<<<< baked in on feature, never conflicts\n",
                                   encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "feature: bake a marker into OTHER.md")
    (repo / "JOURNAL.md").write_text("feature change\n", encoding="utf-8")
    _run(repo, "commit", "-q", "-am", "feature: edit JOURNAL.md")
    _run(repo, "checkout", "-q", "main")
    (repo / "JOURNAL.md").write_text("main change\n", encoding="utf-8")
    _run(repo, "commit", "-q", "-am", "main: edit JOURNAL.md")
    _attempt_conflicting_merge(repo)
    (repo / "JOURNAL.md").write_text("resolved\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "merge feature (JOURNAL.md resolved, OTHER.md untouched)")
    sha = _run(repo, "rev-parse", "HEAD").stdout.strip()

    verdict = cpm.check_merge(repo, sha)

    assert "OTHER.md" in verdict.touched, "a file taken wholesale from one parent is still TOUCHED"
    assert not verdict.ok
    assert "OTHER.md" in {hit.path for hit in verdict.hits}


@requires_git
def test_check_merge_PASSES_a_clean_no_ff_merge(tmp_path):
    """The same divergence, resolved properly before commit -- no marker anywhere."""
    repo = _init_repo(tmp_path)
    _diverge(repo)
    _attempt_conflicting_merge(repo)
    (repo / "JOURNAL.md").write_text("main change\nfeature change\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "merge feature (resolved)")
    sha = _run(repo, "rev-parse", "HEAD").stdout.strip()

    verdict = cpm.check_merge(repo, sha)

    assert verdict.ok
    assert verdict.hits == ()
    assert "JOURNAL.md" in verdict.touched


@requires_git
def test_check_merge_reports_touched_files_even_when_clean(tmp_path):
    """`touched` names what the merge's tree actually differs on from every parent -- the
    completeness signal `render()` uses to distinguish 'checked and clean' from 'checked
    nothing', the same failure class `render_require` refuses to let a vacuous walk hide."""
    repo = _init_repo(tmp_path)
    _diverge(repo)
    _attempt_conflicting_merge(repo)
    (repo / "JOURNAL.md").write_text("resolved\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "merge feature (resolved)")
    sha = _run(repo, "rev-parse", "HEAD").stdout.strip()

    verdict = cpm.check_merge(repo, sha)

    assert verdict.touched == ("JOURNAL.md",)


def test_marker_regex_matches_the_three_git_conflict_lines_and_the_diff3_base():
    assert cpm.MARKER_RE.match("<<<<<<< HEAD")
    assert cpm.MARKER_RE.match("=======")
    assert cpm.MARKER_RE.match(">>>>>>> feature")
    assert cpm.MARKER_RE.match("||||||| base")
    assert not cpm.MARKER_RE.match("this is normal prose")
    assert not cpm.MARKER_RE.match("==== a markdown rule of four ====")


def test_render_names_a_clean_merge_as_clean():
    verdict = cpm.PostMergeVerdict(merge_sha="a" * 40, touched=("f.txt",), hits=())
    rendered = verdict.render()
    assert "clean" in rendered.lower()


def test_render_names_every_hit_with_its_path_and_line():
    hit = cpm.MarkerHit(path="JOURNAL.md", line_number=42, line="<<<<<<< HEAD")
    verdict = cpm.PostMergeVerdict(merge_sha="a" * 40, touched=("JOURNAL.md",), hits=(hit,))
    rendered = verdict.render()
    assert "JOURNAL.md:42" in rendered
    assert "<<<<<<< HEAD" in rendered


@requires_git
def test_check_merge_raises_on_an_unresolvable_sha(tmp_path):
    """FAILS CLOSED, the posture every git-orchestrating reader in this repo takes
    (`merge_receipt.first_parent_of`, `first_parent_merges`): an unreadable SHA is an error,
    never a quiet 'no files touched' that would print CLEAN over nothing checked."""
    repo = _init_repo(tmp_path)
    with pytest.raises(cpm.PostMergeCheckError):
        cpm.check_merge(repo, "not-a-real-sha")


@requires_git
def test_cli_check_exits_nonzero_on_a_dirty_merge(tmp_path):
    repo = _init_repo(tmp_path)
    _diverge(repo)
    _attempt_conflicting_merge(repo)
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "merge feature (unresolved)")
    sha = _run(repo, "rev-parse", "HEAD").stdout.strip()

    from click.testing import CliRunner
    result = CliRunner().invoke(cpm.cli, ["check", "--repo-root", str(repo), "--sha", sha])

    assert result.exit_code == 1
    assert "JOURNAL.md" in result.output


@requires_git
def test_cli_check_exits_zero_on_a_clean_merge(tmp_path):
    repo = _init_repo(tmp_path)
    _diverge(repo)
    _attempt_conflicting_merge(repo)
    (repo / "JOURNAL.md").write_text("resolved\n", encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", "merge feature (resolved)")
    sha = _run(repo, "rev-parse", "HEAD").stdout.strip()

    from click.testing import CliRunner
    result = CliRunner().invoke(cpm.cli, ["check", "--repo-root", str(repo), "--sha", sha])

    assert result.exit_code == 0
