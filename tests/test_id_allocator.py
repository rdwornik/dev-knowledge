"""RED-first witnesses for `scripts/id_allocator.py` -- `[#804]` / `[#788]`, lane ab-804.

THE DEFECT, measured three times. Every lane allocated `max(local ids) + 1`. From a worktree,
that maximum cannot see a sibling's unpushed branch. Every id surface in the tree agreed on an
answer that was wrong (`[#788]`), and the renumbers followed (`279caaff`, `e17c6200`).

WHAT THESE TESTS PIN. An id is RESERVED by PUSHING a ref to the shared remote before a lane
writes anything. The remote is the one substrate two worktrees, or two machines, share. So:

  1. Two lanes in SEPARATE worktrees, started CONCURRENTLY, are never granted the same id. The
     loser is refused, and the refusal names the holder.
  2. A sibling's pushed reservation defeats a higher local maximum. The allocator's answer does
     not move when the local tree carries higher ids, and it skips an id a sibling holds even
     though nothing in the local tree mentions that id.

Every test uses a LOCAL BARE REPOSITORY as `origin`. None of them touches the real remote.
"""
from __future__ import annotations

import importlib
import shutil
import subprocess
import sys
import threading
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")


def _allocator():
    """Imported per test, so a missing module fails each witness on its own rather than
    erroring the whole file at collection."""
    return importlib.import_module("id_allocator")


def _git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    assert proc.returncode == 0, f"git {' '.join(args)} failed: {proc.stderr}"
    return proc.stdout.strip()


def _origin_and_worktrees(tmp_path: Path, names=("lane-a", "lane-b")) -> tuple[Path, list[Path]]:
    """A bare `origin`, one clone of it, and one git WORKTREE per lane off that clone.

    That is the shape the defect was measured in: lanes are worktrees of one clone, so they share
    the common git dir. An id that one worktree holds on an unpushed branch is still invisible to
    the others.
    """
    origin = tmp_path / "origin.git"
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(origin))
    primary = tmp_path / "primary"
    _git(tmp_path, "clone", "-q", str(origin), str(primary))
    _git(primary, "config", "user.email", "t@t.t")
    _git(primary, "config", "user.name", "t")
    (primary / "tasks").mkdir()
    (primary / "tasks" / "807-last-filed-row.md").write_text("---\nid: \"[#807]\"\n---\n",
                                                             encoding="utf-8")
    _git(primary, "add", "-A")
    _git(primary, "commit", "-q", "-m", "seed")
    _git(primary, "push", "-q", "origin", "HEAD:main")
    trees = []
    for name in names:
        wt = tmp_path / name
        _git(primary, "worktree", "add", "-q", "-b", f"worktree-{name}", str(wt))
        trees.append(wt)
    return origin, trees


def _cli(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    """Run the allocator as a SEPARATE PROCESS. A lane is a separate process, and an in-process
    call would share interpreter state that two real lanes do not share."""
    return subprocess.run(
        [sys.executable, str(_SCRIPTS / "id_allocator.py"), *args], cwd=str(cwd),
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)


def _race(calls: list[tuple[Path, list[str]]]) -> list[subprocess.CompletedProcess]:
    """Start every call behind one barrier, so they reach the remote together."""
    barrier = threading.Barrier(len(calls))
    results: list = [None] * len(calls)

    def run(i: int, cwd: Path, args: list[str]) -> None:
        barrier.wait()
        results[i] = _cli(cwd, *args)

    threads = [threading.Thread(target=run, args=(i, cwd, args))
               for i, (cwd, args) in enumerate(calls)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


# --- Done-contract 1: concurrent lanes are refused the same id ------------------------------

@requires_git
@pytest.mark.parametrize("round_", range(3))
def test_two_concurrent_lanes_in_separate_worktrees_are_refused_the_same_id(tmp_path, round_):
    """Both lanes ask for `815` at once. Exactly one gets it. The other exits 3, and its
    refusal names the lane that holds the id."""
    _allocator()  # RED on a tree with no allocator
    _, (lane_a, lane_b) = _origin_and_worktrees(tmp_path)
    a, b = _race([(lane_a, ["reserve", "task-id", "815", "--holder", "lane-a"]),
                  (lane_b, ["reserve", "task-id", "815", "--holder", "lane-b"])])

    codes = sorted([a.returncode, b.returncode])
    assert codes == [0, 3], f"expected one win and one refusal: {a.stderr!r} / {b.stderr!r}"
    winner, loser = (a, b) if a.returncode == 0 else (b, a)
    winner_name = "lane-a" if winner is a else "lane-b"
    assert winner_name in loser.stderr, f"the refusal must name the holder: {loser.stderr!r}"


@requires_git
@pytest.mark.parametrize("round_", range(3))
def test_two_concurrent_allocations_from_one_block_are_disjoint(tmp_path, round_):
    """Batch AA's shape, reproduced: two lanes from one base allocate from the same block at
    the same moment. The two ids must differ."""
    _allocator()
    _, (lane_a, lane_b) = _origin_and_worktrees(tmp_path)
    a, b = _race([(lane_a, ["allocate", "--block", "815-818", "--holder", "lane-a"]),
                  (lane_b, ["allocate", "--block", "815-818", "--holder", "lane-b"])])

    assert a.returncode == 0 and b.returncode == 0, (a.stderr, b.stderr)
    got = {a.stdout.strip(), b.stdout.strip()}
    assert got == {"815", "816"}, f"allocations collided or skipped: {got}"


@requires_git
def test_a_reservation_is_visible_from_a_second_clone_that_never_fetched(tmp_path):
    """Worktrees of one clone share refs, so a same-clone test alone could pass on a LOCAL ref.
    A second CLONE shares nothing but the remote. It is refused as well."""
    origin, (lane_a,) = _origin_and_worktrees(tmp_path, names=("lane-a",))
    other = tmp_path / "other-clone"
    _git(tmp_path, "clone", "-q", str(origin), str(other))

    assert _cli(lane_a, "reserve", "task-id", "815", "--holder", "lane-a").returncode == 0
    refused = _cli(other, "reserve", "task-id", "815", "--holder", "lane-z")
    assert refused.returncode == 3, refused.stderr
    assert "lane-a" in refused.stderr


@requires_git
def test_the_holder_verb_names_who_holds_an_id(tmp_path):
    _, (lane_a, lane_b) = _origin_and_worktrees(tmp_path)
    assert _cli(lane_a, "reserve", "task-id", "815", "--holder", "lane-a").returncode == 0
    shown = _cli(lane_b, "holder", "task-id", "815")
    assert shown.returncode == 0, shown.stderr
    assert "lane-a" in shown.stdout
    free = _cli(lane_b, "holder", "task-id", "816")
    assert free.returncode == 0 and "FREE" in free.stdout


@requires_git
def test_an_exhausted_block_is_refused_not_widened(tmp_path):
    """When every id in the block is held, the allocator refuses. It never reaches past the
    block, because the block is the lane's grant."""
    _, (lane_a, lane_b) = _origin_and_worktrees(tmp_path)
    for n in ("815", "816"):
        assert _cli(lane_a, "reserve", "task-id", n, "--holder", "lane-a").returncode == 0
    refused = _cli(lane_b, "allocate", "--block", "815-816", "--holder", "lane-b")
    assert refused.returncode == 3, refused.stderr
    assert refused.stdout.strip() == ""


# --- Done-contract 4: the local maximum is never consulted -----------------------------------

@requires_git
def test_a_siblings_pushed_reservation_defeats_a_higher_local_max(tmp_path):
    """The `[#788]` shape. Lane B's tree carries ids far ABOVE the block (`tasks/900-*`). It
    carries nothing about 815. Lane A has already pushed its reservation of 815.

    If the allocator used the local maximum, lane B would get 901 (`max + 1`). If it used local
    membership alone, lane B would get 815, which collides with A. The right answer is 816: the
    lowest id in the block that the REMOTE shows as free.
    """
    _, (lane_a, lane_b) = _origin_and_worktrees(tmp_path)
    (lane_b / "tasks" / "900-a-much-higher-local-row.md").write_text(
        "---\nid: \"[#900]\"\n---\n", encoding="utf-8")
    _git(lane_b, "add", "-A")
    _git(lane_b, "commit", "-q", "-m", "local row above the block")

    assert _cli(lane_a, "reserve", "task-id", "815", "--holder", "lane-a").returncode == 0
    got = _cli(lane_b, "allocate", "--block", "815-818", "--holder", "lane-b")
    assert got.returncode == 0, got.stderr
    assert got.stdout.strip() == "816"


@requires_git
def test_the_answer_does_not_move_when_the_local_tree_moves(tmp_path):
    """Two identical remotes, two very different local trees: one tree has no rows, the other
    has rows up to 999. Both get the same id. That is the property; the grep below only
    backs it up."""
    alloc = _allocator()
    answers = []
    for i, local_rows in enumerate(((), ("999-top.md", "500-mid.md"))):
        case = tmp_path / f"case-{i}"
        case.mkdir()
        _, (lane,) = _origin_and_worktrees(case, names=("lane-x",))
        for row in local_rows:
            (lane / "tasks" / row).write_text("---\n---\n", encoding="utf-8")
        answers.append(alloc.allocate(lane, range(815, 819), holder="lane-x").value)
    assert answers == [815, 815]


def test_the_allocator_source_reads_no_task_tree():
    """Backs up the behavioural tests above; it is not enough on its own. The module names no
    `tasks/` surface, no `manifest.json` and no `BACKLOG.md`."""
    alloc = _allocator()
    source = Path(alloc.__file__).read_text(encoding="utf-8")
    code = "\n".join(ln for ln in source.splitlines() if not ln.lstrip().startswith("#"))
    for forbidden in ("glob(", "manifest.json", "BACKLOG.md", "gen_task_tree"):
        assert forbidden not in code, f"allocator reads a local id surface: {forbidden}"


# --- `[#809]` Done-when (4): a batch token is allocated by the same mechanism --------------

@requires_git
def test_809_a_batch_token_is_reserved_like_a_task_id(tmp_path):
    """Two dispatchers cannot both take batch token `ac`. A token outside the enum's shape is an
    internal error (exit 2): it was never a candidate."""
    _, (lane_a, lane_b) = _origin_and_worktrees(tmp_path)
    assert _cli(lane_a, "reserve", "batch-token", "ac", "--holder", "dispatcher-ac").returncode == 0
    refused = _cli(lane_b, "reserve", "batch-token", "ac", "--holder", "dispatcher-other")
    assert refused.returncode == 3 and "dispatcher-ac" in refused.stderr
    assert _cli(lane_b, "reserve", "batch-token", "abcd", "--holder", "x").returncode == 2
