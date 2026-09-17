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


# --- [#833]: the seat refusals, at the same STEP 0 ------------------------------------------------
#
# A lane is the seat that pays for an absent integrator (its handback has nowhere to land) and the
# seat that DOUBLES an owned lane (two committing sessions on one index -- the 2026-09-17 near-miss
# on lane ab-833 itself). Both refusals therefore run here, after the manifest refusals: a lane
# with no open batch has no batch whose integrator could be asked about.
#
# These drive `seat_preflight` on a registry built in `tmp_path` and need no git, so they carry no
# skip guard.

from datetime import datetime, timedelta, timezone  # noqa: E402

_T0 = datetime(2026, 9, 17, 10, 47, tzinfo=timezone.utc)
_OWNED = "lane-ab-833-seat-registry"
_OWNED_CWD = f"C:/Dev/.dev-knowledge/.claude/worktrees/{_OWNED}"


def _seat_registry():
    return importlib.import_module("seat_registry")


def _seats(tmp_path, *, integrator_batch=None, owner=None, minutes=1):
    reg = _seat_registry()
    path = tmp_path / "seats.jsonl"
    if integrator_batch:
        reg.record_event({"hook_event_name": "SessionStart", "session_id": "int-1",
                          "cwd": "C:/Dev/hub"}, path=path, now=_T0, env={"CLAUDE_PID": "1"})
        reg.bind("integrator", integrator_batch, session_id="int-1", path=path, now=_T0)
    if owner:
        reg.record_event({"hook_event_name": "SessionStart", "session_id": owner,
                          "cwd": _OWNED_CWD}, path=path, now=_T0, env={"CLAUDE_PID": "2"})
    return reg.seats(path, now=_T0 + timedelta(minutes=minutes), pid_alive=lambda _p: True,
                     path_exists=lambda _p: True, transcript_mtime=lambda _p: None)


def test_lane_boot_refuses_a_lane_whose_batch_has_no_live_integrator(tmp_path, capsys):
    with pytest.raises(SystemExit) as exc:
        _lane_boot().seat_preflight(_OWNED, _seats(tmp_path), own_session="me")
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "no-live-integrator" in err and "integrator" in err


def test_lane_boot_refuses_a_second_session_onto_an_owned_lane(tmp_path, capsys):
    seats = _seats(tmp_path, integrator_batch="AB", owner="52a3764d")
    with pytest.raises(SystemExit) as exc:
        _lane_boot().seat_preflight(_OWNED, seats, own_session="506ef5c0")
    assert exc.value.code == 1
    assert "lane-owned" in capsys.readouterr().err


def test_lane_boot_admits_a_lane_with_a_live_integrator_and_no_other_owner(tmp_path):
    seats = _seats(tmp_path, integrator_batch="AB")
    line = _lane_boot().seat_preflight(_OWNED, seats, own_session="me")
    assert "int-1" in line
