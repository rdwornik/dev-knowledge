"""codespace_admission.py — the extracted Dispatch-Codespace admission predicate (LANE-5B2-23 /
LANE-5B3-9), one fixture environment per condition.

RED-FIRST. Written and first run against a tree with no `scripts/codespace_admission.py` at all
(import error) -- see the lane's session file for the RED transcript. Every test below drives the
module through its own `Probe` seam (or a real tmp-path git repo for the two conditions that need
one), never the operator's real PATH or a real `gh`/network call -- the deployed
`DispatchHelpers.psm1` this predicate extracts is itself just `command -v` and `timeout 30 git
ls-remote`, so a portable stand-in for both is enough to prove the Python logic without needing a
real container.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

import codespace_admission as ca


# --- Probe fixtures --------------------------------------------------------------------------

def _path_with(tmp_path: Path, *names: str) -> ca.Probe:
    """A Probe whose PATH resolves exactly the given basenames (each an empty stub file)."""
    bindir = tmp_path / "bin"
    bindir.mkdir(exist_ok=True)
    for name in names:
        (bindir / name).write_text("", encoding="utf-8")
    return ca.Probe(env={"PATH": str(bindir)})


def _empty_path(tmp_path: Path) -> ca.Probe:
    empty = tmp_path / "empty-bin"
    empty.mkdir(exist_ok=True)
    return ca.Probe(env={"PATH": str(empty)})


class _StubRunProbe(ca.Probe):
    """A Probe whose `which` is PATH-backed (real fixture files) and whose `run` returns a
    canned CompletedProcess for one argv shape -- so 'gh is present but broken' and 'origin
    unreachable' are testable without a real `gh` binary or a real network call."""

    def __init__(self, env, *, returncode: int):
        super().__init__(env=env)
        self._returncode = returncode

    def run(self, argv, *, cwd=None, timeout=30):
        return subprocess.CompletedProcess(argv, self._returncode, stdout="", stderr="")


# --- claude on PATH ----------------------------------------------------------------------------

def test_claude_absent_refuses(tmp_path):
    cond = ca.check_claude_on_path(_empty_path(tmp_path))
    assert not cond.ok
    assert cond.gates
    assert "claude" in cond.detail
    assert "3083" in cond.cites


def test_claude_present_admits(tmp_path):
    cond = ca.check_claude_on_path(_path_with(tmp_path, "claude"))
    assert cond.ok


# --- uv on PATH ----------------------------------------------------------------------------------

def test_uv_absent_refuses(tmp_path):
    cond = ca.check_uv_on_path(_empty_path(tmp_path))
    assert not cond.ok
    assert cond.gates


def test_uv_present_admits(tmp_path):
    assert ca.check_uv_on_path(_path_with(tmp_path, "uv")).ok


# --- python3 on PATH -------------------------------------------------------------------------

def test_python3_absent_refuses(tmp_path):
    cond = ca.check_python3_on_path(_empty_path(tmp_path))
    assert not cond.ok
    assert cond.gates


def test_python3_present_admits(tmp_path):
    assert ca.check_python3_on_path(_path_with(tmp_path, "python3")).ok


# --- pre-commit on PATH ------------------------------------------------------------------------

def test_pre_commit_absent_refuses(tmp_path):
    cond = ca.check_pre_commit_on_path(_empty_path(tmp_path))
    assert not cond.ok
    assert cond.gates
    assert "past every gate" in cond.detail


def test_pre_commit_present_admits(tmp_path):
    assert ca.check_pre_commit_on_path(_path_with(tmp_path, "pre-commit")).ok


# --- git remote reachable ----------------------------------------------------------------------

def test_git_remote_unreachable_refuses(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    # no 'origin' remote configured at all -- ls-remote origin fails deterministically, offline.
    cond = ca.check_git_remote_reachable(repo, ca.Probe())
    assert not cond.ok
    assert cond.gates
    assert "cannot reach origin" in cond.detail


def test_git_remote_reachable_admits(tmp_path):
    bare = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "remote", "add", "origin", str(bare)], cwd=repo, check=True)
    # A push is unnecessary: ls-remote succeeds against a reachable (if empty) remote.
    cond = ca.check_git_remote_reachable(repo, ca.Probe())
    assert cond.ok, cond.detail


# --- gh: absent is not gated, present-and-broken is ---------------------------------------------

def test_gh_absent_is_not_gated(tmp_path):
    cond = ca.check_gh_not_broken(_empty_path(tmp_path))
    assert cond.ok
    assert not cond.gates
    assert "not gated" in cond.detail


def test_gh_present_and_broken_refuses(tmp_path):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    (bindir / "gh").write_text("", encoding="utf-8")
    probe = _StubRunProbe({"PATH": str(bindir)}, returncode=1)
    cond = ca.check_gh_not_broken(probe)
    assert not cond.ok
    assert cond.gates
    assert "broken tool" in cond.detail


def test_gh_present_and_authenticated_admits(tmp_path):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    (bindir / "gh").write_text("", encoding="utf-8")
    probe = _StubRunProbe({"PATH": str(bindir)}, returncode=0)
    cond = ca.check_gh_not_broken(probe)
    assert cond.ok
    assert cond.gates


# --- the contract leg: non-gating when omitted, gating when given -------------------------------

def test_contract_omitted_is_not_gated():
    cond = ca.check_contract(None)
    assert cond.ok
    assert not cond.gates


def test_contract_missing_refuses(tmp_path):
    cond = ca.check_contract(str(tmp_path / "does-not-exist.md"))
    assert not cond.ok
    assert cond.gates


def test_contract_present_admits(tmp_path):
    p = tmp_path / "CONTRACT.md"
    p.write_text("# a contract\n", encoding="utf-8")
    cond = ca.check_contract(str(p))
    assert cond.ok


# --- git hooks armed (ADDED, beyond the deployed test) -------------------------------------------

def _git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    return repo


def test_hooks_unarmed_refuses(tmp_path):
    repo = _git_repo(tmp_path)
    cond = ca.check_git_hooks_armed(repo)
    assert not cond.ok
    assert cond.gates
    assert cond.cites.startswith("ADDED")


def test_hooks_armed_admits(tmp_path):
    import sys
    repo = _git_repo(tmp_path)
    hooks_dir = repo / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    body = (
        "#!/usr/bin/env python\n"
        f"INSTALL_PYTHON='{sys.executable}'\n"
        "# File generated by pre-commit: https://pre-commit.com\n"
    )
    for name in ("pre-commit", "commit-msg", "pre-push"):
        (hooks_dir / name).write_text(body, encoding="utf-8")
    cond = ca.check_git_hooks_armed(repo)
    assert cond.ok, cond.detail


# --- the whole predicate: run_admission / AdmissionResult ---------------------------------------

def _fully_admitted_probe(tmp_path: Path) -> ca.Probe:
    return _path_with(tmp_path, "claude", "uv", "python3", "pre-commit")


def test_run_admission_refuses_when_any_gating_condition_fails(tmp_path):
    repo = _git_repo(tmp_path)
    probe = _empty_path(tmp_path)  # every PATH-based leg absent
    result = ca.run_admission(repo, probe=probe)
    assert not result.ok
    assert result.exit_code == 1
    failing_ids = {c.id for c in result.failing()}
    assert {"claude_on_path", "uv_on_path", "python3_on_path", "pre_commit_on_path",
            "git_remote_reachable", "git_hooks_armed"} <= failing_ids


def test_run_admission_admits_when_every_gating_condition_passes(tmp_path):
    repo = _git_repo(tmp_path)
    bare = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
    subprocess.run(["git", "remote", "add", "origin", str(bare)], cwd=repo, check=True)
    hooks_dir = repo / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    body = (
        "#!/usr/bin/env python\n"
        f"INSTALL_PYTHON='{__import__('sys').executable}'\n"
        "# File generated by pre-commit: https://pre-commit.com\n"
    )
    for name in ("pre-commit", "commit-msg", "pre-push"):
        (hooks_dir / name).write_text(body, encoding="utf-8")

    probe = _fully_admitted_probe(tmp_path)
    result = ca.run_admission(repo, probe=probe)
    assert result.ok, [c for c in result.failing()]
    assert result.exit_code == 0


def test_non_gating_conditions_never_block_admission(tmp_path):
    """gh absent and no --contract given must never, by themselves, refuse admission."""
    repo = _git_repo(tmp_path)
    bare = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
    subprocess.run(["git", "remote", "add", "origin", str(bare)], cwd=repo, check=True)
    hooks_dir = repo / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    body = (
        "#!/usr/bin/env python\n"
        f"INSTALL_PYTHON='{__import__('sys').executable}'\n"
        "# File generated by pre-commit: https://pre-commit.com\n"
    )
    for name in ("pre-commit", "commit-msg", "pre-push"):
        (hooks_dir / name).write_text(body, encoding="utf-8")

    probe = _fully_admitted_probe(tmp_path)  # deliberately no 'gh' stub
    result = ca.run_admission(repo, probe=probe, contract_path=None)
    assert result.ok, [c for c in result.failing()]
    gh_cond = next(c for c in result.conditions if c.id == "gh_not_broken")
    assert gh_cond.ok and not gh_cond.gates


# --- the CLI ---------------------------------------------------------------------------------

def _real_git_path_entries() -> list[str]:
    """The PATH entries a REAL `git.exe` needs to run `ls-remote` without crashing, on this
    workstation's Git-for-Windows install. Measured: `mingw64\\bin\\git.exe` alone returns
    0xC0000005 (access violation) on `ls-remote` against a local bare repo unless its sibling
    `usr\\bin` and `cmd` directories are ALSO reachable -- `rev-parse` (what
    `check_git_hooks_armed` runs) needs none of this, which is why only `ls-remote` failed the
    first time this was tried with just git's own bin directory on PATH."""
    import shutil

    git_bin = Path(shutil.which("git")).parent           # .../Git/mingw64/bin
    git_root = git_bin.parent.parent                     # .../Git
    return [str(git_bin), str(git_root / "usr" / "bin"), str(git_root / "cmd"),
           os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32")]


def test_cli_exit_codes(tmp_path, monkeypatch, capsys):
    # `check_git_hooks_armed` and `check_git_remote_reachable` both shell out to a REAL git
    # (not a stub), so the PATH `ca.main` runs under must still resolve a working one even once
    # it is stubbed down for the other tools.
    real_git_dirs = _real_git_path_entries()

    # Every fixture git operation runs BEFORE the PATH is monkeypatched.
    repo = _git_repo(tmp_path)
    bare = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
    subprocess.run(["git", "remote", "add", "origin", str(bare)], cwd=repo, check=True)
    hooks_dir = repo / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    body = (
        "#!/usr/bin/env python\n"
        f"INSTALL_PYTHON='{__import__('sys').executable}'\n"
        "# File generated by pre-commit: https://pre-commit.com\n"
    )
    for name in ("pre-commit", "commit-msg", "pre-push"):
        (hooks_dir / name).write_text(body, encoding="utf-8")

    empty_bin = tmp_path / "empty-bin"
    empty_bin.mkdir(exist_ok=True)
    monkeypatch.setenv("PATH", os.pathsep.join([str(empty_bin), *real_git_dirs]))
    assert ca.main(["--repo-root", str(repo)]) == 1

    bindir = tmp_path / "full-bin"
    bindir.mkdir()
    for exe in ("claude", "uv", "python3", "pre-commit"):
        (bindir / exe).write_text("", encoding="utf-8")
    monkeypatch.setenv("PATH", os.pathsep.join([str(bindir), *real_git_dirs]))
    assert ca.main(["--repo-root", str(repo)]) == 0


@pytest.mark.live_repo
def test_the_live_repo_admits_or_names_why():
    """Against the real tree (not the deployed test's container, so `claude` etc. resolve
    however this workstation's own PATH resolves them) -- proves the module runs end to end
    against real git, not only fixtures."""
    root = Path(__file__).resolve().parent.parent
    result = ca.run_admission(root)
    # Not asserting ok=True: this workstation is not the container `Dispatch-Codespace` targets,
    # so e.g. `pre-commit`/`uv` may resolve only inside an activated venv here. The property this
    # asserts is narrower and always true: the predicate runs to completion and names conditions.
    assert result.conditions
    assert all(c.cites for c in result.conditions)
