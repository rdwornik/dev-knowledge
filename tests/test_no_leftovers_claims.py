"""Black-box checks for no_leftovers.py's claim and scratch-file scans."""

import os
import subprocess
import sys
from pathlib import Path

import pytest


CONTRACT = "example-contract"
SCRIPT = os.environ.get("NL_SCRIPT") or str(Path(__file__).resolve().parents[1] / "scripts" / "no_leftovers.py")


def verify(*args, cwd=None):
    result = subprocess.run(
        [sys.executable, SCRIPT, "verify", *map(str, args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=cwd,
    )
    return result.returncode, result.stdout + result.stderr


def fail_line(output, needle):
    return next(
        (line for line in output.splitlines() if line.startswith("FAIL ") and needle in line),
        None,
    )


def git(repo, *args):
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def make_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Test User")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "commit", "-q", "--allow-empty", "-m", "initial")
    return repo


def test_claim_check_fails_vacuously_without_markdown(tmp_path):
    repo = make_repo(tmp_path)
    to_cc = tmp_path / "to-cc"
    to_cc.mkdir()
    decoy = to_cc / "note.txt"
    contents = b"not a markdown file\n"
    decoy.write_bytes(contents)

    code, output = verify("--contract", CONTRACT, "--transport-root", tmp_path, cwd=repo)

    line = fail_line(output, "12 no-claim-marker")
    assert code == 1, output
    assert line is not None, output
    assert "vacuous" in line.lower(), output
    assert decoy.read_bytes() == contents


def test_claim_check_passes_with_markdown_and_no_marker(tmp_path):
    repo = make_repo(tmp_path)
    to_cc = tmp_path / "to-cc"
    to_cc.mkdir()
    (to_cc / "note.md").write_text("a claim exists\n", encoding="utf-8")

    code, output = verify("--contract", CONTRACT, "--transport-root", tmp_path, cwd=repo)

    assert code == 0, output
    assert any(
        line.startswith("PASS 12 no-claim-marker") for line in output.splitlines()
    ), output


def test_claim_check_names_marker_and_preserves_it(tmp_path):
    repo = make_repo(tmp_path)
    to_cc = tmp_path / "to-cc"
    to_cc.mkdir()
    (to_cc / "note.md").write_text("claim\n", encoding="utf-8")
    marker = to_cc / f"{CONTRACT}.CLAIMED-abc12345"
    contents = b"marker contents\x00\n"
    marker.write_bytes(contents)

    code, output = verify("--contract", CONTRACT, "--transport-root", tmp_path, cwd=repo)

    assert code == 1, output
    line = fail_line(output, "12 no-claim-marker")
    assert line is not None and marker.name in line, output
    assert marker.read_bytes() == contents


def test_claim_check_reports_missing_to_cc_as_unreadable(tmp_path):
    repo = make_repo(tmp_path)
    code, output = verify("--contract", CONTRACT, "--transport-root", tmp_path, cwd=repo)

    assert code == 1, output
    line = fail_line(output, "12 no-claim-marker")
    assert line is not None and "unreadable" in line.lower(), output


@pytest.mark.parametrize("create_empty", [False, True])
def test_repo_without_scratch_files_is_clean(tmp_path, create_empty):
    repo = make_repo(tmp_path)
    if create_empty:
        (repo / ".claude" / "worktrees").mkdir(parents=True)

    code, output = verify("--repo", repo)

    assert code == 0, output


@pytest.mark.parametrize("relative", ["loose.txt", "x/tmp.txt"])
def test_unregistered_scratch_file_fails_and_is_preserved(tmp_path, relative):
    repo = make_repo(tmp_path)
    scratch = repo / ".claude" / "worktrees" / relative
    scratch.parent.mkdir(parents=True, exist_ok=True)
    contents = b"scratch\x00contents\n"
    scratch.write_bytes(contents)

    code, output = verify("--repo", repo)

    assert code == 1, output
    assert fail_line(output, scratch.name) is not None, output
    assert scratch.read_bytes() == contents


def test_files_in_registered_worktree_are_not_scratch(tmp_path):
    repo = make_repo(tmp_path)
    worktree = repo / ".claude" / "worktrees" / "registered"
    worktree.parent.mkdir(parents=True)
    git(repo, "worktree", "add", "-q", "-b", "registered-branch", str(worktree))
    inside = worktree / "inside.txt"
    inside.write_text("belongs to registered worktree\n", encoding="utf-8")

    _, output = verify("--repo", repo)

    assert fail_line(output, inside.name) is None, output
