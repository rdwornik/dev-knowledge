"""RED-first witnesses for `scripts/lane_boot.py` -- `[#804]` Done-when (1), lane ab-804.

THE FALSE CLAIM THESE TESTS RETIRE. `protocols/PLAYBOOK.md` (the "RULED 2026-08-29" block) says
`/lane-boot` REFUSES to dispatch the first lane while `open_batches()` returns `[]`, and names
`preflight_contract.check_open_batch` as the predicate. `/lane-boot` never called it. Batch AA
dispatched six lanes with no manifest, and nothing noticed until merge.

The witnesses drive the REAL entry point: the `preflight` command that
`.claude/commands/lane-boot.md` runs. They do not test the predicate on its own. Two refusals are
pinned:

  * no committed manifest declares an open batch -> refused;
  * a manifest that is committed on the lane branch but NOT on `main` -> refused, naming the
    file. A manifest held only in a worktree is the same visibility defect as `[#788]`.
"""
from __future__ import annotations

import importlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_LANE = "lane-ab-804-id-allocator"
_MANIFEST = "docs/audits/2026-09-16-technical-batch-ab-manifest.md"
_CLOSER = "docs/audits/2026-09-16-technical-batch-ab-close-packet.md"


def _lane_boot():
    return importlib.import_module("lane_boot")


def _git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    assert proc.returncode == 0, f"git {' '.join(args)} failed: {proc.stderr}"
    return proc.stdout.strip()


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "hub"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")
    (repo / "JOURNAL.md").write_text("# Journal\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    return repo


def _commit_manifest(repo: Path) -> None:
    path = repo / _MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\nbatch: AB\nstatus: open\nclosed_by: {_CLOSER}\n---\n\n# Batch AB\n",
                    encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "batch AB manifest")


def _boot(repo: Path, lane: str = _LANE):
    return CliRunner().invoke(_lane_boot().cli,
                              ["preflight", "--lane", lane, "--repo", str(repo)])


@requires_git
def test_lane_boot_refuses_a_batch_with_no_committed_manifest(tmp_path):
    repo = _repo(tmp_path)
    result = _boot(repo)
    assert result.exit_code == 1, result.output
    assert "manifest" in result.output.lower()


@requires_git
def test_lane_boot_admits_a_batch_whose_manifest_is_committed_on_main(tmp_path):
    repo = _repo(tmp_path)
    _commit_manifest(repo)
    result = _boot(repo)
    assert result.exit_code == 0, result.output
    assert _MANIFEST.rsplit("/", 1)[-1] in result.output


@requires_git
def test_a_manifest_committed_only_on_a_lane_branch_is_refused_and_named(tmp_path):
    """The manifest exists and is committed, but only on a side branch that `main` does not
    contain. Every other worktree reads `main`, so for them the batch is not open."""
    repo = _repo(tmp_path)
    _git(repo, "checkout", "-q", "-b", "worktree-batch-ab-manifest")
    _commit_manifest(repo)
    result = _boot(repo)
    assert result.exit_code == 1, result.output
    assert _MANIFEST in result.output
    assert "main" in result.output


@requires_git
def test_an_uncommitted_manifest_opens_nothing(tmp_path):
    repo = _repo(tmp_path)
    path = repo / _MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\nbatch: AB\nstatus: open\nclosed_by: {_CLOSER}\n---\n", encoding="utf-8")
    assert _boot(repo).exit_code == 1


@requires_git
def test_a_closed_batch_is_refused(tmp_path):
    repo = _repo(tmp_path)
    _commit_manifest(repo)
    closer = repo / _CLOSER
    closer.write_text("# packet\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "close packet")
    assert _boot(repo).exit_code == 1


@requires_git
def test_a_malformed_lane_name_is_refused_before_the_manifest_is_read(tmp_path):
    repo = _repo(tmp_path)
    _commit_manifest(repo)
    result = _boot(repo, lane="worktree-lane-ab-804-id-allocator")
    assert result.exit_code == 1
    assert "BRANCH form" in result.output


def test_the_lane_boot_command_file_runs_the_entry_point():
    """The wiring half. A refusal that no boot step calls does not refuse anything. That is the
    state this lane found. `/lane-boot`'s pre-flight must RUN `lane_boot.py preflight` inside a
    fenced block, which is the part a seat actually types."""
    text = (_REPO_ROOT / ".claude" / "commands" / "lane-boot.md").read_text(encoding="utf-8")
    fences = re.findall(r"```[a-z]*\n(.*?)```", text, flags=re.S)
    assert any("scripts/lane_boot.py preflight" in f for f in fences), \
        "/lane-boot does not run the manifest refusal"
