"""Branch-context fixtures: a repository whose HEAD and `main` THIS module sets (B2-W1 W1-8).

WHY THIS EXISTS. A test that reads the live checkout answers for whichever branch CI happens to
be on. On `main` HEAD, local `main` and `origin/main` are one commit; on a lane branch they are
not (the lane is ahead, or `main` moved after the lane branched, or the lane adds a file the
index has not caught up with). Measured over 222 CI job logs (`DIGEST-B2-PREP-2026-10-03` Part 4)
a handful of tests failed on 67 of 67 lane runs and on 0 of 21 `main` runs, so every lane's CI
was red by construction and a real red hid among them.

THE TWO USES.
  * AS THE FIXTURE: `contexts(tmp_path_factory).main()` is a clone whose HEAD == local `main` ==
    `origin/main`. A test that is about MECHANICS (a handoff cut, a bundle) runs against it
    instead of the live checkout, so its verdict does not depend on how far the live branch has
    drifted from `main`.
  * AS THE WITNESS: `contexts(...).lane(...)` is the same clone shaped like a CI lane run, and
    `run_node(...)` runs a listed test in it. A test is branch-independent when it passes in both.
    The witness is RED when the test reads the live branch, because the lane shape is exactly what
    differs from `main`.

THE SHAPES a lane run can have (each a keyword of `lane`):
  * `lane_files` -- the lane's own commit adds files (an audit, a test) and nothing regenerated an
    index of them;
  * `peer_files` -- another lane merged to `main` after this one branched, so `main` (and the
    remote-tracking ref CI seeds it from) is AHEAD of the lane's tree;
  * `local_main_follows_origin=False` -- `origin/main` moved after the job seeded local `main`.

LIBRARY-FIRST CHECK: stdlib `subprocess` and `git clone`; pytest's `tmp_path_factory` for the
location. A clone (not `git worktree add`) because a worktree shares the source's refs, and the
whole point is to set `main` and `HEAD` without touching them. No new dependency.

HONEST LIMIT: the clone is of `HEAD`'s COMMITTED tree. An uncommitted edit in the live checkout is
not in it. A witness therefore measures what is committed -- which is what CI measures.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

#: The files a lane commit carries when the caller names none: enough that HEAD != main.
_DEFAULT_LANE_FILES = {"LANE-PROBE.txt": "a lane commit\n"}


def _git(cwd: Path, *args: str, check: bool = True) -> str:
    done = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=300)
    if check and done.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: {done.stderr.strip()}")
    return done.stdout.strip()


def _write(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)


class BranchContexts:
    """One clone of the live repo's HEAD plus a bare `origin`, re-shaped on request."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.base = _git(REPO, "rev-parse", "HEAD")
        self.origin = root / "origin.git"
        self.work = root / "work"
        hooks = root / "no-hooks"
        hooks.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "-q", "--bare", str(REPO), str(self.origin)],
                       check=True, capture_output=True, timeout=600)
        _git(self.origin, "update-ref", "refs/heads/main", self.base)
        _git(self.origin, "symbolic-ref", "HEAD", "refs/heads/main")
        subprocess.run(["git", "clone", "-q", "-c", "core.autocrlf=false", "-c", "core.longpaths=true",
                        str(self.origin), str(self.work)],
                       check=True, capture_output=True, timeout=900)
        for key, value in (("user.name", "branch-context"), ("user.email", "bc@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.hooksPath", str(hooks)),
                           ("core.autocrlf", "false"), ("core.longpaths", "true")):
            _git(self.work, "config", key, value)

    # -- shapes -----------------------------------------------------------------------------------

    def _reset(self) -> None:
        """Back to the base: `main` == `origin/main` == the live HEAD, checked out, tree clean."""
        _git(self.work, "checkout", "-q", "-f", "-B", "main", self.base)
        _git(self.work, "clean", "-fdxq")
        for line in _git(self.work, "branch", "--format=%(refname:short)").splitlines():
            if line.strip() and line.strip() != "main":
                _git(self.work, "branch", "-q", "-D", line.strip())
        _git(self.work, "push", "-q", "-f", "origin", f"{self.base}:refs/heads/main")
        _git(self.work, "update-ref", "refs/remotes/origin/main", self.base)

    def main(self) -> Path:
        """HEAD == local `main` == `origin/main`: the shape a push to `main` has."""
        self._reset()
        return self.work

    def lane(self, *, branch: str = "worktree-branch-context-probe",
             lane_files: "dict[str, str] | None" = None,
             peer_files: "dict[str, str] | None" = None,
             local_main_follows_origin: bool = True) -> Path:
        """A lane-shaped checkout: HEAD is a commit on `branch`, never on `main`."""
        self._reset()
        if peer_files:
            _write(self.work, peer_files)
            _git(self.work, "add", "-A")
            _git(self.work, "commit", "-q", "-m", "peer: a sibling lane merged to main")
            _git(self.work, "push", "-q", "origin", "main")
        _git(self.work, "checkout", "-q", "-b", branch, self.base)
        _write(self.work, lane_files or _DEFAULT_LANE_FILES)
        _git(self.work, "add", "-A")
        _git(self.work, "commit", "-q", "-m", "lane: the lane's own work")
        if peer_files and not local_main_follows_origin:
            _git(self.work, "branch", "-q", "-f", "main", self.base)
        return self.work

    # -- running ----------------------------------------------------------------------------------

    def run_node(self, work: Path, *nodeids: str, timeout: int = 1500) -> subprocess.CompletedProcess:
        """Run pytest node ids from `work`'s own tests, as a CI step would, and return the result."""
        env = {k: v for k, v in os.environ.items()
               if not k.startswith(("GITHUB_", "PYTEST_")) and k != "VIRTUAL_ENV"}
        env.update(UV_PROJECT_ENVIRONMENT=sys.prefix, PYTHONUTF8="1")
        return subprocess.run(
            [sys.executable, "-m", "pytest", "-o", "addopts=", "-p", "no:cacheprovider",
             "-q", "--no-header", "--tb=short", "--color=no", *nodeids],
            cwd=str(work), env=env, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=timeout)


def names_at_merge_base(repo: Path, subtree: str, against: str = "origin/main") -> "frozenset[str] | None":
    """Repo-relative paths under `subtree` as of `git merge-base HEAD <against>`.

    The branch-independent half of a live-corpus test: what THIS branch inherited. On `main` the
    merge base is HEAD itself, so the answer is the whole current corpus and a test using it is as
    strict as it ever was; on a lane it excludes only what the lane added after branching, which
    the integrator's merge is what reconciles. None when it cannot be told (no `against` ref, no
    common ancestor, git absent) -- a caller falls back to the strict whole-corpus verdict.
    """
    try:
        base = subprocess.run(["git", "-C", str(repo), "merge-base", "HEAD", against],
                              capture_output=True, text=True, encoding="utf-8", timeout=60)
        if base.returncode != 0 or not base.stdout.strip():
            return None
        listing = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "-z", "--name-only",
                                  base.stdout.strip(), "--", subtree],
                                 capture_output=True, text=True, encoding="utf-8", timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if listing.returncode != 0:
        return None
    return frozenset(p for p in listing.stdout.split("\0") if p)


_CACHE: dict[str, BranchContexts] = {}


def contexts(tmp_path_factory) -> BranchContexts:
    """One `BranchContexts` per pytest basetemp (each xdist worker has its own), built on first use."""
    key = str(tmp_path_factory.getbasetemp())
    if key not in _CACHE:
        _CACHE[key] = BranchContexts(tmp_path_factory.mktemp("branch-context"))
    return _CACHE[key]


def tail(done: subprocess.CompletedProcess, lines: int = 40) -> str:
    """The end of a run's output -- where pytest prints the failure summary."""
    text = (done.stdout or "") + (done.stderr or "")
    return "\n".join(text.splitlines()[-lines:])


def witness(tmp_path_factory, nodeid: str, **lane_shape) -> None:
    """Assert `nodeid` passes on `main` AND on a lane shaped as `lane_shape` says.

    The `main` run is the CONTROL: if the harness itself (a missing file in the clone, a changed
    interpreter) broke the test, the control fails too and the failure names the harness, not the
    branch. Only a test that passes on `main` and fails on the lane is branch-dependent.
    """
    ctx = contexts(tmp_path_factory)
    control = ctx.run_node(ctx.main(), nodeid)
    assert control.returncode == 0, f"CONTROL (main-shaped) failed -- the harness, not the branch:\n{tail(control)}"
    lane = ctx.run_node(ctx.lane(**lane_shape), nodeid)
    assert lane.returncode == 0, f"{nodeid} passes on main and FAILS on a lane-shaped checkout:\n{tail(lane)}"
