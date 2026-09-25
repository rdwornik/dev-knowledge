"""`scripts/no_leftovers.py` — teardown verified by code, not by a human reading eleven lines.

THE SPECIFICATION is `to-browser/SESSION-integrator-loop-eval.md` §11 "No leftovers — 11 checks,
filesystem enumeration included": the eleven checks a human ran by hand on 2026-09-20. The
proof that reading them is not enough is two empty husk directories (`lane-z-4-...` 15.09,
`lane-ab-833-...` 17.09) that sat unregistered under `.claude/worktrees/` for five days.

WHAT THESE PIN. For each of the eleven checks, ONE fixture where it FAILS and ONE where it
PASSES — the passing fixture is the torn-down-clean round-trip, so a check cannot satisfy its
trip-test by failing everything. Plus the properties the contract makes immutable:

  * READ-ONLY. It verifies; it never removes, unlocks, prunes or deletes. Pinned three ways: the
    git wrapper refuses every non-listing verb, the AST carries no mutating call, and a run
    against a leftover-laden fixture leaves the tree byte-identical.
  * THE HUSK. An unregistered directory under `.claude/worktrees/` is reported, with or without
    a slug, and a slug-less run names every one.
  * NON-ZERO ON ANY LEFTOVER, so the teardown moment can refuse to call the teardown clean.
  * NEVER THE LIVE HUB. Every fixture is a temporary repository with its own bare `origin`.
"""
from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

import pytest

import no_leftovers as nl  # noqa: E402

SLUG = "lane-t-1-demo"

_NAMES = {
    1: "worktree-not-registered",
    2: "worktree-dir-absent",
    3: "worktree-dir-enumeration-empty",
    4: "worktree-admin-entry-absent",
    5: "no-lane-branch",
    6: "no-ref-names-lane",
    7: "no-remote-head",
    8: "job-record-absent",
    9: "job-not-in-agents",
    10: "working-tree-clean",
    11: "main-equals-origin-main",
}


# --- fixtures -----------------------------------------------------------------

def _git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                          check=check)


@pytest.fixture
def hub(tmp_path: Path) -> Path:
    """A throwaway primary checkout with its own bare `origin` — never the live hub."""
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


def _tear_down_lane(hub: Path, slug: str = SLUG) -> None:
    _git(hub, "worktree", "remove", "--force", str(_lane_dir(hub, slug)))
    _git(hub, "worktree", "prune")
    _git(hub, "branch", "-D", f"worktree-{slug}")


def _run(hub: Path, jobs_dir: Path, agents=(), slug: str = SLUG):
    return {r.number: r for r in nl.run_checks(hub, slug, jobs_dir=jobs_dir, agents=list(agents))}


def _job(jobs_dir: Path, job_id: str, **state) -> None:
    (jobs_dir / job_id).mkdir()
    (jobs_dir / job_id / "state.json").write_text(json.dumps(state), encoding="utf-8")


# --- the spec: eleven named checks ---------------------------------------------

def test_the_eleven_checks_are_named_and_numbered_as_the_spec_lists_them(hub, jobs):
    results = nl.run_checks(hub, SLUG, jobs_dir=jobs, agents=[])
    assert {r.number: r.name for r in results} == _NAMES


def test_every_result_carries_the_evidence_it_read(hub, jobs):
    for r in nl.run_checks(hub, SLUG, jobs_dir=jobs, agents=[]):
        assert isinstance(r.evidence, str) and r.evidence.strip(), r.name


# --- PASS fixture: the provision -> teardown round trip leaves the tree identical ---

@pytest.mark.parametrize("n", sorted(_NAMES))
def test_check_passes_after_a_clean_round_trip(hub, jobs, n):
    _add_lane(hub)
    _tear_down_lane(hub)
    # neighbours that must NOT be mistaken for the lane: a prefix-sibling worktree, its
    # branch, a job and a live agent belonging to it
    sibling = SLUG + "-2"
    _add_lane(hub, sibling)
    _job(jobs, "aaaa1111", worktreePath=str(_lane_dir(hub, sibling)),
         worktreeBranch=f"worktree-{sibling}")
    agents = [{"id": "aaaa1111", "cwd": str(_lane_dir(hub, sibling)), "status": "busy"},
              {"id": "bbbb2222", "cwd": str(hub), "status": "busy"}]
    res = _run(hub, jobs, agents)[n]
    assert res.passed, f"{res.name}: {res.evidence}"


# --- FAIL fixtures: one per check ------------------------------------------------

def test_1_fails_while_the_worktree_is_still_registered(hub, jobs):
    _add_lane(hub)
    assert not _run(hub, jobs)[1].passed


def test_1_fails_for_a_registered_worktree_whose_directory_is_gone(hub, jobs):
    import shutil
    path = _add_lane(hub)
    shutil.rmtree(path)                      # fixture only: a half-done teardown
    assert not _run(hub, jobs)[1].passed


def test_2_fails_for_an_empty_husk_directory_git_has_forgotten(hub, jobs):
    _lane_dir(hub).mkdir(parents=True)
    res = _run(hub, jobs)
    assert not res[2].passed
    assert res[1].passed                     # `git worktree list` cannot see it — that is the point
    assert res[5].passed


def test_3_fails_for_a_gitignored_leftover_that_a_clean_git_status_hides(hub, jobs):
    leftover = _lane_dir(hub) / "logs" / "2026-09" / "DETECTOR-ERROR-2026-09-14.md"
    leftover.parent.mkdir(parents=True)
    leftover.write_text("re-created by the departing Stop hook\n", encoding="utf-8")
    res = _run(hub, jobs)
    assert not res[3].passed
    assert "DETECTOR-ERROR-2026-09-14.md" in res[3].evidence
    assert _git(hub, "status", "--porcelain").stdout.strip() == ""   # the blind spot, witnessed
    assert res[10].passed


def test_3_passes_for_an_empty_husk_so_the_two_checks_answer_different_questions(hub, jobs):
    _lane_dir(hub).mkdir(parents=True)
    assert _run(hub, jobs)[3].passed


def test_4_fails_while_git_keeps_an_administrative_entry(hub, jobs):
    admin = hub / ".git" / "worktrees" / SLUG
    admin.mkdir(parents=True)
    (admin / "gitdir").write_text(str(_lane_dir(hub) / ".git") + "\n", encoding="utf-8")
    assert not _run(hub, jobs)[4].passed


def test_4_fails_for_an_admin_entry_under_a_renamed_directory_pointing_at_the_lane(hub, jobs):
    admin = hub / ".git" / "worktrees" / (SLUG + "1")   # git suffixes on a name collision
    admin.mkdir(parents=True)
    (admin / "gitdir").write_text(str(_lane_dir(hub) / ".git") + "\n", encoding="utf-8")
    assert not _run(hub, jobs)[4].passed


def test_4_passes_for_a_digit_suffixed_admin_entry_that_belongs_to_a_live_sibling(hub, jobs):
    # Codex HIGH: `<slug>1` is git's collision suffix, but it is THIS lane's only if its gitdir says so.
    _add_lane(hub, SLUG + "1")
    assert _run(hub, jobs)[4].passed


def test_4_fails_closed_on_an_admin_entry_whose_gitdir_cannot_be_read(hub, jobs):
    # Codex HIGH: unreadable administrative evidence must not be accepted as clean.
    (hub / ".git" / "worktrees" / "unrelated-name").mkdir(parents=True)
    res = _run(hub, jobs)[4]
    assert not res.passed and "unrelated-name" in res.evidence


def test_4_fails_closed_on_an_ambiguous_suffixed_entry_with_no_readable_target(hub, jobs):
    (hub / ".git" / "worktrees" / (SLUG + "2")).mkdir(parents=True)
    assert not _run(hub, jobs)[4].passed


def test_5_fails_for_a_surviving_local_lane_branch(hub, jobs):
    _git(hub, "branch", f"worktree-{SLUG}")
    assert not _run(hub, jobs)[5].passed


def test_5_fails_for_a_surviving_remote_tracking_branch(hub, jobs):
    _git(hub, "update-ref", f"refs/remotes/origin/worktree-{SLUG}", "HEAD")
    assert not _run(hub, jobs)[5].passed


def test_5_does_not_mistake_a_prefix_sibling_for_the_lane(hub, jobs):
    _git(hub, "branch", f"worktree-{SLUG}-2")
    assert _run(hub, jobs)[5].passed


def test_6_fails_for_any_ref_that_names_the_lane_not_only_worktree_branches(hub, jobs):
    _git(hub, "tag", f"archive/{SLUG}")
    res = _run(hub, jobs)
    assert not res[6].passed
    assert res[5].passed


def test_6_does_not_mistake_a_prefix_sibling_for_the_lane(hub, jobs):
    _git(hub, "tag", f"archive/{SLUG}-2")
    assert _run(hub, jobs)[6].passed


def test_7_fails_for_a_head_that_survives_only_on_origin(hub, jobs):
    _git(hub, "push", "origin", f"HEAD:refs/heads/worktree-{SLUG}")
    _git(hub, "update-ref", "-d", f"refs/remotes/origin/worktree-{SLUG}", check=False)
    res = _run(hub, jobs)
    assert not res[7].passed
    assert res[5].passed                     # invisible locally — `git branch -a` reads clean


def test_8_fails_while_a_job_record_still_points_at_the_lane(hub, jobs):
    _job(jobs, "bc6e739e", worktreePath=str(_lane_dir(hub)), worktreeBranch=f"worktree-{SLUG}",
         state="blocked", respawnFlags=["--effort", "high"])
    res = _run(hub, jobs)
    assert not res[8].passed
    assert "bc6e739e" in res[8].evidence


def test_8_matches_a_record_by_branch_when_the_path_is_missing(hub, jobs):
    _job(jobs, "cafe0001", worktreeBranch=f"worktree-{SLUG}")
    assert not _run(hub, jobs)[8].passed


def test_8_fails_closed_on_a_job_record_it_cannot_parse(hub, jobs):
    # Codex HIGH: a record that cannot be inspected may still point at the lane.
    (jobs / "deadbeef").mkdir()
    (jobs / "deadbeef" / "state.json").write_text("{not json", encoding="utf-8")
    res = _run(hub, jobs)[8]
    assert not res.passed and "deadbeef" in res.evidence


def test_8_fails_when_the_jobs_directory_cannot_be_read(hub, tmp_path):
    res = {r.number: r for r in nl.run_checks(hub, SLUG, jobs_dir=tmp_path / "no-such-jobs",
                                              agents=[])}[8]
    assert not res.passed
    assert "no-such-jobs" in res.evidence


def test_8_passes_when_the_pointing_job_record_is_TERMINAL(hub, jobs):
    """R3: teardown STOPS a lane's session rather than removing it (`batch_janitor.py`), and
    `claude stop` "leaves ... the job record in place" -- so a record that still points at the
    (now torn-down) lane is not itself a leftover once its own `state` says the job ended."""
    _job(jobs, "deadbeef", worktreePath=str(_lane_dir(hub)), worktreeBranch=f"worktree-{SLUG}",
         state="stopped")
    assert _run(hub, jobs)[8].passed


def test_9_fails_while_a_live_session_is_cwd_d_in_the_lane(hub, jobs):
    agents = [{"id": "9c53bd44", "cwd": str(_lane_dir(hub)), "status": "busy"}]
    res = _run(hub, jobs, agents)[9]
    assert not res.passed
    assert "9c53bd44" in res.evidence


def test_9_matches_a_worktree_path_and_forward_slashes(hub, jobs):
    agents = [{"id": "77770000", "cwd": str(hub),
               "worktreePath": str(_lane_dir(hub)).replace("\\", "/").upper()}]
    assert not _run(hub, jobs, agents)[9].passed


def test_9_fails_when_the_agent_list_could_not_be_read(hub, jobs):
    res = {r.number: r for r in nl.run_checks(hub, SLUG, jobs_dir=jobs, agents=None)}[9]
    assert not res.passed
    assert "claude agents" in res.evidence


def test_9_passes_when_the_pointing_agents_entry_is_TERMINAL(hub, jobs):
    """R3: a session survives its own teardown, so `claude agents --json` keeps listing it,
    cwd and all -- only a still-LIVE entry counts as a leftover here."""
    agents = [{"id": "9c53bd44", "cwd": str(_lane_dir(hub)), "status": "done",
               "state": "stopped"}]
    assert _run(hub, jobs, agents)[9].passed


def test_10_fails_for_a_dirty_primary_working_tree(hub, jobs):
    (hub / "stray.txt").write_text("x", encoding="utf-8")
    res = _run(hub, jobs)[10]
    assert not res.passed
    assert "stray.txt" in res.evidence


def test_11_fails_when_local_main_is_ahead_of_origin(hub, jobs):
    _git(hub, "commit", "--allow-empty", "-m", "unpushed")
    assert not _run(hub, jobs)[11].passed


def test_11_fails_when_origin_is_ahead_of_local_main(hub, jobs, tmp_path):
    other = tmp_path / "other"
    subprocess.run(["git", "clone", str(tmp_path / "origin.git"), str(other)], check=True,
                   capture_output=True)
    _git(other, "config", "user.name", "t")
    _git(other, "config", "user.email", "t@example.invalid")
    _git(other, "commit", "--allow-empty", "-m", "elsewhere")
    _git(other, "push", "origin", "main")
    assert not _run(hub, jobs)[11].passed    # read from the remote, not a stale tracking ref


def test_7_and_11_fail_rather_than_pass_when_there_is_no_origin(hub, jobs):
    _git(hub, "remote", "remove", "origin")
    res = _run(hub, jobs)
    assert not res[7].passed and not res[11].passed
    assert "origin" in res[7].evidence


# --- the husk: the leak that is live -----------------------------------------------

def test_find_husks_names_every_unregistered_directory_and_no_registered_one(hub):
    (hub / ".claude" / "worktrees" / "lane-z-4-husk").mkdir(parents=True)
    (hub / ".claude" / "worktrees" / "lane-ab-833-husk").mkdir(parents=True)
    _add_lane(hub, "lane-live")
    assert sorted(p.name for p in nl.find_husks(hub)) == ["lane-ab-833-husk", "lane-z-4-husk"]


def test_a_non_empty_unregistered_directory_is_a_husk_too(hub):
    d = _lane_dir(hub, "lane-full")
    (d / "sub").mkdir(parents=True)
    (d / "sub" / "f.txt").write_text("x", encoding="utf-8")
    assert [p.name for p in nl.find_husks(hub)] == ["lane-full"]


def test_no_husks_in_a_hub_with_only_registered_lanes(hub):
    _add_lane(hub, "lane-live")
    assert nl.find_husks(hub) == []


def test_slugless_run_names_both_husks_and_exits_non_zero(hub, capsys):
    for name in ("lane-z-4-non-claude-execution", "lane-ab-833-seat-registry"):
        (hub / ".claude" / "worktrees" / name).mkdir(parents=True)
    rc = nl.main(["verify", "--repo", str(hub)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "lane-z-4-non-claude-execution" in out
    assert "lane-ab-833-seat-registry" in out


def test_slugless_run_is_clean_when_there_is_no_husk(hub, capsys):
    _add_lane(hub, "lane-live")
    assert nl.main(["verify", "--repo", str(hub)]) == 0


def test_a_slugged_run_names_other_lanes_husks_but_does_not_let_them_decide_its_verdict(
        hub, jobs, tmp_path, capsys):
    (hub / ".claude" / "worktrees" / "lane-old-husk").mkdir(parents=True)
    rc = nl.main(_cli(hub, jobs, tmp_path))
    out = capsys.readouterr().out
    assert "lane-old-husk" in out            # visible ...
    assert rc == 0                           # ... but this lane's teardown is judged on this lane


# --- the CLI: exit code and report -------------------------------------------------

def _cli(hub, jobs, tmp_path, slug=SLUG, agents="[]"):
    f = tmp_path / "agents.json"
    f.write_text(agents, encoding="utf-8")
    return ["verify", "--lane", slug, "--repo", str(hub), "--jobs-dir", str(jobs),
            "--agents-json", str(f)]


def test_exit_zero_and_every_check_reported_by_name_on_a_clean_teardown(hub, jobs, tmp_path,
                                                                       capsys):
    _add_lane(hub)
    _tear_down_lane(hub)
    rc = nl.main(_cli(hub, jobs, tmp_path))
    out = capsys.readouterr().out
    assert rc == 0
    for name in _NAMES.values():
        assert name in out
    assert "FAIL" not in out
    assert out.count("PASS") >= 11


def test_exit_non_zero_and_the_failing_check_named_when_anything_is_left(hub, jobs, tmp_path,
                                                                        capsys):
    _lane_dir(hub).mkdir(parents=True)
    rc = nl.main(_cli(hub, jobs, tmp_path))
    out = capsys.readouterr().out
    assert rc == 1
    assert any(line.startswith("FAIL") and "worktree-dir-absent" in line
               for line in out.splitlines())


def test_unreadable_agents_file_is_a_failed_check_not_a_crash(hub, jobs, tmp_path, capsys):
    argv = _cli(hub, jobs, tmp_path, agents="{not json")
    assert nl.main(argv) == 1
    assert "job-not-in-agents" in capsys.readouterr().out


@pytest.mark.parametrize("bad", ["../escape", "a/b", "a\\b", "..", ".", "", "lane x"])
def test_a_slug_that_could_leave_the_worktrees_directory_is_refused(hub, jobs, tmp_path, bad):
    argv = _cli(hub, jobs, tmp_path, slug=bad)
    assert nl.main(argv) == 2


def test_resolve_primary_from_inside_a_linked_worktree_is_the_primary(hub):
    lane = _add_lane(hub)
    assert nl.resolve_primary(lane).resolve() == hub.resolve()


# --- read-only ------------------------------------------------------------------------

@pytest.mark.parametrize("args", [
    ("worktree", "remove", "x"), ("worktree", "prune"), ("worktree", "unlock", "x"),
    ("worktree", "add", "x"), ("branch", "-D", "x"), ("branch", "-d", "x"),
    ("push", "origin", "--delete", "x"), ("update-ref", "-d", "x"), ("gc",),
    ("clean", "-fdx"), ("checkout", "x"), ("stash", "drop"), ("fetch",), ("tag", "-d", "x"),
])
def test_the_git_wrapper_refuses_every_verb_that_mutates(hub, args):
    with pytest.raises(nl.ReadOnlyViolation):
        nl._git(hub, *args)


def test_the_git_wrapper_admits_the_listing_verbs(hub):
    assert nl._git(hub, "worktree", "list", "--porcelain").returncode == 0
    assert nl._git(hub, "status", "--porcelain").returncode == 0


_FORBIDDEN_CALLS = {"rmtree", "unlink", "rmdir", "remove", "removedirs", "rename", "replace",
                    "write_text", "write_bytes", "mkdir", "makedirs", "touch", "chmod", "move",
                    "copy", "copytree", "copyfile", "symlink_to", "kill", "terminate"}


def test_the_source_contains_no_mutating_call():
    tree = ast.parse((Path(nl.__file__)).read_text(encoding="utf-8"))
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            if name in _FORBIDDEN_CALLS:
                hits.append((name, node.lineno))
            if name == "open" and len(node.args) > 1 and isinstance(node.args[1], ast.Constant) \
                    and any(c in str(node.args[1].value) for c in "wax+"):
                hits.append(("open-for-write", node.lineno))
    assert hits == []


def _snapshot(root: Path) -> dict:
    return {str(p.relative_to(root)): (p.stat().st_size if p.is_file() else -1)
            for p in sorted(root.rglob("*"))}


def test_a_run_against_a_leftover_laden_tree_changes_nothing(hub, jobs, tmp_path, capsys):
    (_lane_dir(hub) / "logs").mkdir(parents=True)
    (_lane_dir(hub) / "logs" / "DETECTOR-ERROR-x.md").write_text("x", encoding="utf-8")
    (hub / ".claude" / "worktrees" / "lane-old-husk").mkdir(parents=True)
    _git(hub, "branch", f"worktree-{SLUG}")
    _git(hub, "tag", f"archive/{SLUG}")
    admin = hub / ".git" / "worktrees" / SLUG
    admin.mkdir(parents=True)
    (admin / "gitdir").write_text("x\n", encoding="utf-8")
    _job(jobs, "bc6e739e", worktreePath=str(_lane_dir(hub)))
    argv = _cli(hub, jobs, tmp_path)
    before = (_snapshot(tmp_path), _git(hub, "for-each-ref").stdout,
              _git(hub, "worktree", "list", "--porcelain").stdout)
    rc = nl.main(argv)
    after = (_snapshot(tmp_path), _git(hub, "for-each-ref").stdout,
             _git(hub, "worktree", "list", "--porcelain").stdout)
    assert rc == 1
    assert before == after
