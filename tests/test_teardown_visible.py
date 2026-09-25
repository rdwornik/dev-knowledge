"""tests/test_teardown_visible.py -- R3 (LANE-5B2-5-teardown-visible): teardown stops
a lane's session and removes its worktree and branches; it never removes the session, so the
session and its transcript SURVIVE, and the digest is the only thing that still points at them.

HONEST LIMIT, taken up on the contract's own escape clause ("the janitor's own seam if a live
job is impossible headless -- say which"): this file does NOT spawn a real `claude --bg` job in
a scratch worktree. This test session is itself a headless `--bg` job, and this run's own
SessionStart line already read the fleet at zero admission headroom (4 live seats, 0.36 GB free
against a 2.0 GB reserve) -- launching a fifth job to prove the fifth job's own teardown would
risk getting IT killed by the same pressure, not prove anything. Instead this composes the three
injection seams each owning module already exercises, none invented here:
  * `batch_janitor`'s injected `agents`/`run` seam (`tests/test_batch_janitor.py`) for
    "stop, never `claude rm`";
  * `no_leftovers`'s throwaway-hub-with-its-own-bare-origin fixture
    (`tests/test_no_leftovers.py`) for "worktree and branch gone, verified CLEAN";
  * `routing_agreement.transcript_paths` with an injected `sessions_root`
    (`scripts/routing_agreement.py`) for "the transcript survives, at the path the test
    resolves".
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import batch_janitor as bj
import no_leftovers as nl
import routing_agreement as ra

REPO_ROOT = Path(__file__).resolve().parent.parent

SLUG = "lane-scratch-teardown-demo"
JOB_ID = "deadbeef01"
BATCH = "SCRATCH-TEARDOWN-VISIBLE"


# --- fixtures -- the same throwaway-hub shape `test_no_leftovers.py` owns -------------------

def _git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                          check=check)


@pytest.fixture
def hub(tmp_path: Path) -> Path:
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(origin)], check=True,
                   capture_output=True)
    repo = tmp_path / "hub"
    subprocess.run(["git", "init", "-b", "main", str(repo)], check=True, capture_output=True)
    _git(repo, "config", "user.name", "t")
    _git(repo, "config", "user.email", "t@example.invalid")
    _git(repo, "config", "commit.gpgsign", "false")
    (repo / ".gitignore").write_text(".claude/worktrees/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "init")
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "push", "-u", "origin", "main")
    return repo


@pytest.fixture
def jobs(tmp_path: Path) -> Path:
    d = tmp_path / "jobs"
    d.mkdir()
    return d


def _lane_dir(hub: Path, slug: str = SLUG) -> Path:
    return hub / ".claude" / "worktrees" / slug


def _add_lane(hub: Path, slug: str = SLUG) -> Path:
    path = _lane_dir(hub, slug)
    _git(hub, "worktree", "add", "-b", f"worktree-{slug}", str(path))
    return path


def _remove_worktree_and_branch_only(hub: Path, slug: str = SLUG) -> None:
    """R3's teardown, exactly: the worktree and the branch, local and (in a live repo) on
    origin. NEVER a `claude stop`/`claude rm` call -- that half is the janitor's, exercised
    separately below, so this helper cannot be mistaken for proving both halves at once."""
    _git(hub, "worktree", "remove", "--force", str(_lane_dir(hub, slug)))
    _git(hub, "worktree", "prune")
    _git(hub, "branch", "-D", f"worktree-{slug}")


# --- the end-to-end property ----------------------------------------------------------------

def test_teardown_stops_the_session_removes_worktree_and_branch_transcript_survives(
        hub, jobs, tmp_path, monkeypatch):
    receipts = tmp_path / "receipts"
    receipts.mkdir()
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(receipts))
    worktree_path = _add_lane(hub)

    # dispatch's own launch record -- the one home tying a job id to this lane
    (receipts / f"LAUNCH-JOB-{JOB_ID}.json").write_text(json.dumps({
        "schema": 1, "job_id": JOB_ID, "session_id": f"sess-{JOB_ID}", "slug": SLUG,
        "batch": BATCH, "provider": "anthropic", "worktree": str(worktree_path),
        "contract": f"LANE-{SLUG}.md", "launched_at": "2026-09-25T00:00:00+00:00",
    }), encoding="utf-8")

    # the transcript this session is filed under, in a scratch sessions_root -- the janitor's
    # stop verb must never touch this file, and nothing here ever will either
    sessions_root = tmp_path / "projects"
    transcript_dir = sessions_root / ra.session_slug(worktree_path)
    transcript_dir.mkdir(parents=True)
    transcript = transcript_dir / f"sess-{JOB_ID}.jsonl"
    transcript.write_text('{"type": "assistant"}\n', encoding="utf-8")

    # ONE shared listing stands for "what `claude agents --json` reads after the stop" --
    # CODEX HIGH, fixed: the first draft asserted nothing about the janitor's own post-stop
    # read and fed no_leftovers a second, disconnected record instead. Now the exact same
    # object is what the janitor's second read returns AND what no_leftovers reads below, so
    # `report.after` is the proof, not a fabrication alongside it. It still carries `cwd` and
    # `worktreeBranch` -- `claude stop` "leaves ... the job record in place" (batch_janitor's
    # own docstring), and nothing erases the launch cwd from the live listing either, so this
    # is the hard case: without the R3 fix, no_leftovers would read this surviving pointer as
    # a leftover forever.
    branch = f"worktree-{SLUG}"
    after_listing = [{"id": JOB_ID, "state": "stopped", "sessionId": f"sess-{JOB_ID}",
                      "cwd": str(worktree_path), "worktreeBranch": branch}]
    reads = [[{"id": JOB_ID, "state": "done"}], after_listing]
    stop_calls: list[list[str]] = []

    def fake_run(argv: list[str]) -> subprocess.CompletedProcess:
        stop_calls.append(argv)
        return subprocess.CompletedProcess(argv, 0, "", "")

    report = bj.run_janitor(BATCH, dry_run=False, agents=lambda: reads.pop(0), run=fake_run)

    assert stop_calls == [["claude", "stop", JOB_ID]], \
        "the janitor's own stop verb -- never `claude rm` -- is what teardown calls"
    assert report.stopped[0].ok

    # the janitor's OWN post-stop observation: the session is still LISTED, stopped not gone
    after_session = next(s for s in report.after if s.job_id == JOB_ID)
    assert after_session.state == "stopped", \
        "the session survives teardown -- the janitor's own re-read must still list it"
    assert after_session.live is False

    # R3's other half: worktree and branch removed. The job/session is untouched by this.
    _remove_worktree_and_branch_only(hub, SLUG)

    (jobs / JOB_ID).mkdir()
    (jobs / JOB_ID / "state.json").write_text(json.dumps({
        "worktreePath": str(worktree_path), "worktreeBranch": branch, "state": "stopped",
    }), encoding="utf-8")

    # its transcript exists at the path the test resolves, byte-identical to what was written
    resolved = ra.transcript_paths(worktree_path, sessions_root=sessions_root)
    assert resolved == [transcript]
    assert transcript.read_text(encoding="utf-8") == '{"type": "assistant"}\n'

    # the worktree and branch are gone -- no_leftovers CLEAN, fed the SAME listing the janitor
    # itself just observed as stopped, not a second record invented for this assertion alone
    results = nl.run_checks(hub, SLUG, jobs_dir=jobs, agents=after_listing)
    failed = [r for r in results if not r.passed]
    assert not failed, f"no_leftovers not CLEAN: {[(r.name, r.evidence) for r in failed]}"


# --- item 2: templates never instruct the destructive verb ---------------------------------

def test_templates_never_instruct_claude_rm():
    """R3: teardown stops a lane's session; it must never be told to `claude rm` it, which
    would delete the transcript the digest is now required to point at."""
    result = subprocess.run(
        ["git", "grep", "-nE", r"claude\s+rm", "--", "templates/"],
        cwd=REPO_ROOT, capture_output=True, text=True)
    assert result.stdout == ""
    assert result.returncode != 0, f"templates/ instructs `claude rm`:\n{result.stdout}"


# --- item 3: the digest records where each lane's session and transcript are -----------------

def test_integrator_close_step_writes_session_id_and_transcript_path():
    text = (REPO_ROOT / "templates" / "integrator-order-template.md").read_text(encoding="utf-8")
    close_section = text.split("## Close", 1)[1]
    assert "session id" in close_section
    assert "transcript path" in close_section
