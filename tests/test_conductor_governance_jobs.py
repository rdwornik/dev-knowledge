"""LANE-5B4-8 (row L5, D4): the `spine` and `anchor` CI jobs in `.github/workflows/conductor.yml`
-- server-side equivalents of the local pre-push PREVENT/HARD gates
(`scripts/block_ff_push.py`, `scripts/block_unanchored_push.py`), so a `git push --no-verify`
no longer erases them without a trace (proposal row L5; `to-browser/PROPOSAL-ADR-CI-
VERIFICATION-2026-09-26-seat-71020de7.md`).

RED-FIRST (ADR-108 sec:B). Row L5's Done-when, verbatim: "seeded unanchored range and seeded
FF onto the spine each turn the job red." The structural tests below pin that the two new jobs
call the EXISTING organs (never a copy) and carry no `continue-on-error`; the E2E tests prove
the organs themselves turn red on exactly the two seeded cases the Done-when names, invoked
with the identical stdin shape the workflow's own steps construct (`<ref> <sha> <ref>
<before>`, ref repeated on both sides the way `${{ github.ref }} ${{ github.sha }} ${{
github.ref }} ${{ github.event.before }}` renders).

WHY THE SHELL-MECHANICS TEST EXISTS. `report-only-wall.yml`'s own (advisory) `anchor` step
pipes the stdin line through the organ and into `tee`, then reads `PIPESTATUS[0]` for the
verdict -- but in a 3-stage pipe (`echo | uv run | tee`), `PIPESTATUS[0]` is `echo`'s exit
status, which is always 0. That step's job carries `continue-on-error: true`, so the mistake
never gates anything there -- but copying the SAME shape into a job whose entire purpose is to
gate would silently defeat it: every push would report "clean" regardless of what the organ
actually decided. The two new steps here use a direct redirect (`> file 2>&1; rc=$?`) instead,
specifically to avoid that trap; `test_the_redirect_then_rc_pattern_reads_the_organs_own_exit_
code` pins the mechanism, not just the intent.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import block_ff_push as bfp        # noqa: E402 -- reuse-integrity: same organ as the CI step
import block_unanchored_push as bup  # noqa: E402

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
requires_bash = pytest.mark.skipif(shutil.which("bash") is None, reason="bash not available")

_REPO = Path(__file__).resolve().parents[1]
_WORKFLOW = _REPO / ".github" / "workflows" / "conductor.yml"
_BFP = _REPO / "scripts" / "block_ff_push.py"
_BUP = _REPO / "scripts" / "block_unanchored_push.py"
_ZERO = "0" * 40

# Structural over enumerated: derived from the organ, never a "refs/heads/main" literal.
PROTECTED = bfp.PROTECTED_REF
PROTECTED_BRANCH = PROTECTED.rsplit("/", 1)[-1]

# After BASELINE_DATE (2026-06-15) so a seeded violation is never grandfathered.
_AFTER_BASELINE = "2026-06-16T10:00:00"


@pytest.fixture(scope="module")
def workflow():
    return yaml.safe_load(_WORKFLOW.read_text(encoding="utf-8"))


def _run_text(job: dict) -> str:
    return "\n".join(str(s.get("run", "")) for s in job["steps"])


# --- structural: the jobs exist, name the real organs, and are not advisory --------------

def test_spine_and_anchor_jobs_exist_and_name_the_real_organs(workflow):
    assert "spine" in workflow["jobs"], "row L5's first governance job is missing"
    assert "anchor" in workflow["jobs"], "row L5's second governance job is missing"
    spine_text = _run_text(workflow["jobs"]["spine"])
    anchor_text = _run_text(workflow["jobs"]["anchor"])
    # Contract item 2: "the jobs call the existing gate scripts ... not a copy; a test
    # asserts the job steps name them."
    assert "scripts/block_ff_push.py" in spine_text
    assert "scripts/block_unanchored_push.py" in anchor_text
    # And not the wrong organ in the wrong job.
    assert "block_unanchored_push.py" not in spine_text
    assert "block_ff_push.py" not in anchor_text


def test_spine_and_anchor_carry_no_continue_on_error(workflow):
    # Unlike every report-only leg elsewhere in this file, a violation here MUST turn the
    # job red -- `continue-on-error` anywhere in the job (job level or any step) would
    # silence exactly the signal row L5 exists to produce.
    for job_name in ("spine", "anchor"):
        job = workflow["jobs"][job_name]
        assert "continue-on-error" not in job, f"{job_name} job must not be advisory"
        for step in job["steps"]:
            assert "continue-on-error" not in step, \
                f"{job_name} step {step.get('name')!r} must not be advisory"


def test_the_final_step_fails_the_job_on_the_organs_own_exit_code(workflow):
    for job_name in ("spine", "anchor"):
        steps = workflow["jobs"][job_name]["steps"]
        last = steps[-1]
        assert last.get("name", "").startswith("Fail the job on")
        assert "steps.run.outputs.exit" in str(last.get("run", ""))
        run_step = next(s for s in steps if s.get("id") == "run")
        assert run_step is not None


def test_the_redirect_then_rc_pattern_never_pipes_the_organ_into_tee(workflow):
    # The exact shape report-only-wall.yml's advisory anchor step uses (`| tee x.out` then
    # `PIPESTATUS[0]`) reads the WRONG command's exit status in a 3-stage pipe. These jobs
    # gate on the result, so they must use the direct-redirect form instead.
    for job_name, script in (("spine", "block_ff_push.py"), ("anchor", "block_unanchored_push.py")):
        run_step = next(s for s in workflow["jobs"][job_name]["steps"] if s.get("id") == "run")
        text = str(run_step["run"])
        assert f"{script} > " in text or f"{script} >" in text, \
            f"{job_name} must redirect the organ's own output with '>', not pipe it into tee"
        assert "rc=$?" in text
        # A literal PIPESTATUS *variable reference* (`$PIPESTATUS`/`${PIPESTATUS`), not the
        # bare word -- the step's own explanatory comment names PIPESTATUS in prose without
        # ever reading it, and that prose is not the defect this test guards against.
        assert "$PIPESTATUS" not in text, \
            f"{job_name} must not read PIPESTATUS -- it names the wrong command in a 3-stage pipe"


def test_spine_and_anchor_skip_cleanly_on_a_non_push_event(workflow):
    for job_name in ("spine", "anchor"):
        text = _run_text(workflow["jobs"][job_name])
        assert "github.event_name" in text and '!= "push"' in text


# --- the shell mechanics themselves, isolated from the real organ ------------------------

@requires_bash
def test_the_redirect_then_rc_pattern_reads_the_organs_own_exit_code(tmp_path):
    """Proves the fix, not just the intent: a `stdin | prog > file 2>&1; rc=$?` pipeline
    reports PROG's exit code, even though it is the second stage of a two-stage pipe --
    unlike `PIPESTATUS[0]` in a 3-stage `| prog | tee` pipe, which reports the FIRST
    stage's (always 0). Uses a throwaway script standing in for the real organ so this test
    is about the shell idiom, not about block_ff_push/block_unanchored_push."""
    fake = tmp_path / "fake_organ.py"
    fake.write_text("import sys; sys.exit(1)\n", encoding="utf-8")
    out = tmp_path / "out.txt"
    script = (
        f"printf 'line\\n' | python3 '{fake}' > '{out}' 2>&1\n"
        "rc=$?\n"
        "echo \"rc=$rc\"\n"
    )
    r = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
    assert "rc=1" in r.stdout, r.stdout + r.stderr


@requires_bash
def test_the_buggy_pipestatus_zero_shape_is_the_defect_this_avoids(tmp_path):
    """The negative control: the shape this lane deliberately did NOT copy. Pins that the
    defect is real (not a misreading of report-only-wall.yml) -- a 3-stage pipe's
    PIPESTATUS[0] names the leftmost command, which here is always-zero `printf`, so a
    refusing organ would still report a clean 0."""
    fake = tmp_path / "fake_organ.py"
    fake.write_text("import sys; sys.exit(1)\n", encoding="utf-8")
    out = tmp_path / "out.txt"
    script = (
        f"printf 'line\\n' | python3 '{fake}' 2>&1 | tee '{out}' >/dev/null\n"
        "echo \"rc=${PIPESTATUS[0]}\"\n"
    )
    r = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
    assert "rc=0" in r.stdout, ("the negative control itself must show the masking; "
                                "if this fails the defect class may already be gone: "
                                + r.stdout + r.stderr)


# --- git helpers (mirror tests/test_block_ff_push.py and test_adr85_integration_enforcement.py) --

def _git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _rev(repo, ref="HEAD"):
    return _git(repo, "rev-parse", ref).stdout.strip()


def _commit(repo, msg, adate=_AFTER_BASELINE, fname="f.txt", content=None):
    (repo / fname).write_text(content if content is not None else msg, encoding="utf-8")
    _git(repo, "add", "-A")
    env = dict(os.environ)
    if adate:
        env["GIT_AUTHOR_DATE"] = adate
        env["GIT_COMMITTER_DATE"] = adate
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", msg],
                   check=True, capture_output=True, text=True, encoding="utf-8", env=env)


def _journal(repo, text):
    (repo / "JOURNAL.md").write_text(text, encoding="utf-8")


def _repo_with_remote(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")
    _journal(repo, "# Journal\n\n")
    # Root seed dated before the FF-organ's baseline -> always grandfathered there.
    _commit(repo, "seed", adate="2026-06-01T00:00:00", fname="seed.txt")
    _git(repo, "branch", "-M", PROTECTED_BRANCH)
    bare = tmp_path / "remote.git"
    bare.mkdir()
    _git(bare, "init", "--bare", "-q")
    _git(repo, "remote", "add", "origin", str(bare))
    _git(repo, "push", "-q", "origin", PROTECTED_BRANCH)
    return repo, _rev(repo, PROTECTED_BRANCH)


def _merge_branch(repo, branch, msg, ff_only=False, journal_text=None):
    """Off the protected branch: commit work (+ optional journal), then merge back either
    --no-ff (the sanctioned path) or --ff-only (the seeded violation)."""
    _git(repo, "checkout", "-q", "-b", branch)
    _commit(repo, f"work on {branch}", fname=f"{branch.replace('/', '_')}.txt")
    work = _rev(repo)
    if journal_text is not None:
        text = journal_text(work) if callable(journal_text) else journal_text
        _journal(repo, text)
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", f"journal for {branch}")
    _git(repo, "checkout", "-q", PROTECTED_BRANCH)
    if ff_only:
        _git(repo, "merge", "--ff-only", "-q", branch)
    else:
        _git(repo, "merge", "-q", "--no-ff", branch, "-m", msg)
    return work, _rev(repo, PROTECTED_BRANCH)


def _workflow_line(ref, sha, before):
    """The exact stdin shape the `spine`/`anchor` steps construct: `${{ github.ref }} ${{
    github.sha }} ${{ github.ref }} ${{ github.event.before }}` -- the SAME ref on both
    sides, unlike the native git pre-push shape where local_ref/remote_ref can differ. The
    organs only key on `remote_ref`, so this still exercises the real scoping."""
    return f"{ref} {sha} {ref} {before}\n"


def _invoke(script, repo, stdin_text):
    env = {k: v for k, v in os.environ.items() if not k.startswith("PRE_COMMIT_")}
    return subprocess.run([sys.executable, str(script)], input=stdin_text,
                          capture_output=True, text=True, env=env, cwd=str(repo))


# --- E2E: the Done-when's two seeded cases, invoked exactly as the CI step would ----------

@requires_git
def test_seeded_direct_to_main_commit_turns_spine_red(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    _commit(repo, "feat: oops direct on main", fname="a.txt")
    line = _workflow_line(PROTECTED, _rev(repo, PROTECTED_BRANCH), remote)
    r = _invoke(_BFP, repo, line)
    assert r.returncode == 1, r.stderr
    assert "oops direct on main" in r.stderr


@requires_git
def test_seeded_ff_merge_onto_the_spine_turns_spine_red(tmp_path):
    # Row L5's Done-when, verbatim: "seeded ... FF onto the spine ... turn the job red."
    repo, remote = _repo_with_remote(tmp_path)
    _merge_branch(repo, "feat/y", "unused", ff_only=True)
    line = _workflow_line(PROTECTED, _rev(repo, PROTECTED_BRANCH), remote)
    r = _invoke(_BFP, repo, line)
    assert r.returncode == 1, r.stderr


@requires_git
def test_a_sanctioned_no_ff_merge_leaves_spine_green(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    _merge_branch(repo, "feat/z", "Merge branch 'feat/z' --no-ff")
    line = _workflow_line(PROTECTED, _rev(repo, PROTECTED_BRANCH), remote)
    r = _invoke(_BFP, repo, line)
    assert r.returncode == 0, r.stderr


@requires_git
def test_a_lane_branch_push_is_a_clean_no_op_for_spine(tmp_path):
    # A `worktree-**` / `epic/**` push renders `github.ref` as the LANE ref, not
    # `refs/heads/main` -- the organ's own PROTECTED_REF check makes this a no-op, the
    # identical behaviour the local pre-push hook already has on those pushes.
    repo, _remote = _repo_with_remote(tmp_path)
    _git(repo, "checkout", "-q", "-b", "worktree-lane-x")
    _commit(repo, "feat: on a lane branch", fname="x.txt")
    lane_ref = "refs/heads/worktree-lane-x"
    line = _workflow_line(lane_ref, _rev(repo, "worktree-lane-x"), _ZERO)
    r = _invoke(_BFP, repo, line)
    assert r.returncode == 0, r.stderr


@requires_git
def test_seeded_unanchored_range_turns_anchor_red(tmp_path):
    # Row L5's Done-when, verbatim: "seeded unanchored range ... turn the job red."
    repo, remote = _repo_with_remote(tmp_path)
    _work, merge = _merge_branch(repo, "feat/unanchored", "Merge branch 'feat/unanchored'")
    line = _workflow_line(PROTECTED, merge, remote)
    r = _invoke(_BUP, repo, line)
    assert r.returncode == 1, r.stderr
    assert "REFUSED" in r.stderr


@requires_git
def test_an_anchored_range_leaves_anchor_green(tmp_path):
    repo, remote = _repo_with_remote(tmp_path)
    _work, merge = _merge_branch(
        repo, "feat/anchored", "Merge branch 'feat/anchored'",
        journal_text=lambda w: f"# Journal\n\n### entry -- work {w[:7]}\n")
    line = _workflow_line(PROTECTED, merge, remote)
    r = _invoke(_BUP, repo, line)
    assert r.returncode == 0, r.stderr


@requires_git
def test_a_lane_branch_push_is_a_clean_no_op_for_anchor(tmp_path):
    repo, _remote = _repo_with_remote(tmp_path)
    _git(repo, "checkout", "-q", "-b", "epic/wave-int")
    _commit(repo, "feat: unanchored, but not going to main", fname="x.txt")
    lane_ref = "refs/heads/epic/wave-int"
    line = _workflow_line(lane_ref, _rev(repo, "epic/wave-int"), _ZERO)
    r = _invoke(_BUP, repo, line)
    assert r.returncode == 0, r.stderr
