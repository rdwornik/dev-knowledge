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


# --- repair 1 (G-1744): F1 contract-alone check 13, F2 case folding, F3 kinds and bounded walk ---

def _case_sensitive(path):
    probe = path / "CaseProbe"
    probe.mkdir()
    try:
        return not (path / "caseprobe").exists()
    finally:
        probe.rmdir()


def test_f1_contract_alone_runs_check_13_and_fails_on_scratch(tmp_path):
    repo = make_repo(tmp_path)
    to_cc = tmp_path / "to-cc"
    to_cc.mkdir()
    (to_cc / "note.md").write_text("a claim exists\n", encoding="utf-8")
    scratch = repo / ".claude" / "worktrees" / "x" / "tmp.txt"
    scratch.parent.mkdir(parents=True)
    scratch.write_text("scratch\n", encoding="utf-8")

    code, output = verify("--repo", repo, "--contract", CONTRACT, "--transport-root", tmp_path)

    assert code == 1, output
    assert fail_line(output, "13 worktrees-scratch-files-absent") is not None, output
    assert scratch.exists()


def test_f1_contract_alone_passes_check_13_on_a_clean_checkout(tmp_path):
    repo = make_repo(tmp_path)
    to_cc = tmp_path / "to-cc"
    to_cc.mkdir()
    (to_cc / "note.md").write_text("a claim exists\n", encoding="utf-8")

    code, output = verify("--repo", repo, "--contract", CONTRACT, "--transport-root", tmp_path)

    assert code == 0, output
    assert any(ln.startswith("PASS 13 worktrees-scratch-files-absent") for ln in output.splitlines()), output


def test_f2_unregistered_dir_differing_only_by_case_is_not_skipped(tmp_path):
    repo = make_repo(tmp_path)
    root = repo / ".claude" / "worktrees"
    root.mkdir(parents=True)
    if not _case_sensitive(root):
        pytest.skip("case-insensitive filesystem: two directories differing only by case cannot exist")
    registered = root / "Lane"
    git(repo, "worktree", "add", "-q", "-b", "lane-branch", str(registered))
    stray = root / "lane" / "tmp.txt"
    stray.parent.mkdir()
    stray.write_text("scratch\n", encoding="utf-8")

    code, output = verify("--repo", repo)

    assert code == 1, output
    assert fail_line(output, "tmp.txt") is not None, output


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="no FIFOs on this platform")
def test_f3_fifo_is_reported_by_its_kind(tmp_path):
    repo = make_repo(tmp_path)
    fifo = repo / ".claude" / "worktrees" / "x" / "pipe"
    fifo.parent.mkdir(parents=True)
    os.mkfifo(fifo)

    code, output = verify("--repo", repo)

    assert code == 1, output
    line = fail_line(output, "pipe")
    assert line is not None and "fifo" in line.lower(), output


def test_f3_walk_of_empty_directories_is_bounded_and_fails_closed_naming_the_cap(tmp_path):
    repo = make_repo(tmp_path)
    husk = repo / ".claude" / "worktrees" / "husk"
    husk.mkdir(parents=True)
    for i in range(1100):
        (husk / f"d{i:04d}").mkdir()

    code, output = verify("--repo", repo)

    assert code == 1, output
    line = fail_line(output, "13 worktrees-scratch-files-absent")
    assert line is not None and "cap" in line.lower(), output


def test_f3_file_truncation_names_the_cap(tmp_path):
    repo = make_repo(tmp_path)
    husk = repo / ".claude" / "worktrees" / "husk"
    husk.mkdir(parents=True)
    for i in range(250):
        (husk / f"f{i:03d}.txt").write_text("x\n", encoding="utf-8")

    code, output = verify("--repo", repo)

    assert code == 1, output
    assert any("cap" in ln.lower() for ln in output.splitlines() if ln.startswith("FAIL 13")), output


# --- review 1 round 1 findings (R1-a unprobeable fold, R1-b walk cap inside one directory) ---

def test_r1a_unprobeable_case_sensitivity_does_not_fold(tmp_path, monkeypatch):
    import no_leftovers as nl

    root = tmp_path / "worktrees"
    root.mkdir()

    def boom(*_a, **_k):
        raise OSError("probe failed")

    monkeypatch.setattr(nl.os.path, "samefile", boom)
    monkeypatch.setattr(Path, "exists", lambda self: True)
    assert nl._fold(root) is False


def test_r1b_walk_cap_bounds_a_single_large_directory(tmp_path):
    import no_leftovers as nl

    repo = make_repo(tmp_path)
    husk = repo / ".claude" / "worktrees" / "husk"
    husk.mkdir(parents=True)
    for i in range(30):
        (husk / f"f{i:02d}.txt").write_text("x\n", encoding="utf-8")

    found, truncated, err = nl.find_scratch_files(repo, cap=200, walk_cap=5)

    assert truncated and "cap" in err
    assert len(found) <= 5


def test_r1c_iteration_time_read_error_fails_closed(tmp_path, monkeypatch):
    import no_leftovers as nl

    repo = make_repo(tmp_path)
    (repo / ".claude" / "worktrees" / "husk").mkdir(parents=True)

    class Broken:
        def __enter__(self):
            return self

        def __exit__(self, *_a):
            return False

        def __iter__(self):
            return self

        def __next__(self):
            raise PermissionError("denied mid-scan")

    real = os.scandir
    root = repo / ".claude" / "worktrees"
    monkeypatch.setattr(nl.os, "scandir", lambda p: Broken() if Path(p) == root else real(p))

    ok, evidence, _ = nl._check_scratch_files(repo)

    assert ok is False
    assert "could not list" in evidence
