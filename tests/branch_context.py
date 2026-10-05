# B2-W1 W1-8 -- related rows: [#1101], [#912], [#590] (the lane contract names them; none is closed here).
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

    def __init__(self, root: Path, base: "str | None" = None) -> None:
        self.root = root
        #: The commit that is `main` in every shape: the live HEAD, or a commit the caller names
        #: (an ancestor of it) when the question is about what `main` carried earlier.
        self.base = base or _git(REPO, "rev-parse", "HEAD")
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
        if base is None:
            self._leave_out_what_the_integrator_indexes()

    def _leave_out_what_the_integrator_indexes(self) -> None:
        """Make the base a tree `main` could be: without the audits THIS branch added.

        A lane adds an audit record (its own Codex review, at least) and is barred from indexing it
        -- the integrator does at merge. A clone of that tree called `main` would carry an audit
        `main`'s README does not list, and every strict corpus check would fail on it for a reason
        that is the lane's own file, not the shape under test. So the base is HEAD's tree minus the
        `docs/audits/` files added since the merge base; nothing else is touched, and on `main`
        (nothing added) the base stays HEAD.
        """
        inherited = names_at_merge_base(REPO, "docs/audits")
        listing = _git(REPO, "ls-tree", "-r", "--name-only", self.base, "--", "docs/audits", check=False)
        added = [p for p in listing.splitlines()
                 if p and inherited is not None and p not in inherited and p != "docs/audits/README.md"]
        if not added:
            return
        _git(self.work, "checkout", "-q", "-f", "-B", "main", self.base)
        _git(self.work, "rm", "-q", "--", *added)
        _git(self.work, "commit", "-q", "-m", "base: the audits this branch added are the integrator's to index")
        self.base = _git(self.work, "rev-parse", "HEAD")
        _git(self.work, "push", "-q", "-f", "origin", f"{self.base}:refs/heads/main")

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


def _git_out(repo: Path, *args: str) -> "str | None":
    """`git -C repo <args>` stdout, stripped; None when git fails, is absent or times out."""
    try:
        done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                              encoding="utf-8", timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    out = done.stdout.strip()
    return out if done.returncode == 0 and out else None


def _is_ancestor(repo: Path, older: str, newer: str) -> bool:
    try:
        return subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", older, newer],
                              capture_output=True, timeout=60).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def merge_base_with_main(repo: Path) -> "str | None":
    """The commit this branch inherited from `main`: the LATER of its merge bases with local
    `main` and with `origin/main`.

    Later, so the scope can only be as loose as the evidence forces. A checkout ON `main` that is
    ahead of a stale `origin/main` has merge base HEAD with the local ref, and a lane whose local
    `main` has not been fetched forward has the newer base with the remote ref; either way no
    commit is treated as "the lane's" that the branch actually inherited. The two bases are both
    ancestors of HEAD; when neither is an ancestor of the other the answer is None (cannot tell),
    which every caller reads as "judge strictly". On `main` itself the answer is HEAD, so a check
    scoped by it is exactly as strict as the unscoped one.
    """
    local = _git_out(repo, "merge-base", "HEAD", "refs/heads/main")
    remote = _git_out(repo, "merge-base", "HEAD", "refs/remotes/origin/main")
    if local is None or remote is None or local == remote:
        return local or remote
    if _is_ancestor(repo, local, remote):
        return remote
    if _is_ancestor(repo, remote, local):
        return local
    return None


def names_at_merge_base(repo: Path, subtree: str) -> "frozenset[str] | None":
    """Repo-relative paths under `subtree` as of `merge_base_with_main(repo)`.

    The branch-independent half of a live-corpus test: what THIS branch inherited. On `main` the
    base is HEAD itself, so the answer is the whole current corpus and a test using it is as
    strict as it ever was; on a lane it excludes only what the lane added after branching, which
    the integrator's merge is what reconciles. None when it cannot be told (no `main` ref, no
    common ancestor, git absent) -- a caller falls back to the strict whole-corpus verdict.
    """
    base = merge_base_with_main(repo)
    if base is None:
        return None
    try:
        listing = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "-z", "--name-only",
                                  base, "--", subtree],
                                 capture_output=True, text=True, encoding="utf-8", timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if listing.returncode != 0:
        return None
    return frozenset(p for p in listing.stdout.split("\0") if p)


def pin_journal_spine(mp) -> None:
    """Pin the live JOURNAL spine's UNANCHORED LIST, the one input of a handoff cut that depends
    on the branch, to empty -- on `mp` (a MonkeyPatch).

    A cut is run to test its MECHANICS (bundle files, organ set, refusal shape). Two of the
    organs it evaluates -- `gen_handoff._journal_spine_gaps` (preflight row `journal_anchored`) and
    `audit.check_journal_spine_anchor` (the `ship_gate` row's organ set) -- both ask
    `journal_anchor.unanchored_on_spine` which entries on `main`'s first-parent spine the JOURNAL
    has not anchored. That list is non-empty whenever `main` carries an entry the JOURNAL has not
    anchored YET: on a lane whose tree lags `main`, and on `main` itself between an integrator's
    merge and its JOURNAL entry (measured at 469f0d85: two unanchored spine entries on a
    main-shaped clone). Neither state is the cut's.

    Only that list is replaced. Both organs still run for real -- the floor read from the ADR, the
    JOURNAL text, the batch-manifest exemption, the pass/fail verdict -- and the predicate itself
    has its own tests (`tests/test_journal_anchor.py`, `tests/test_gen_handoff_preflight.py`).
    """
    import journal_anchor as ja  # noqa: PLC0415

    mp.setattr(ja, "unanchored_on_spine", lambda *_args, **_kwargs: [])

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


def witness(tmp_path_factory, *nodeids: str, **lane_shape) -> None:
    """Assert every node id passes on `main` AND on a lane shaped as `lane_shape` says.

    Several node ids go through ONE pytest run per shape: a clone's collection and a module-level
    fixture (a dry cut) are paid once, not once per test.

    The `main` run is the CONTROL: a test that fails there too has a verdict that depends on live
    state (or on the harness) rather than on the branch, and the failure says so. Only a test that
    passes on `main` and fails on the lane is branch-dependent in the narrow sense.
    """
    ctx = contexts(tmp_path_factory)
    control = ctx.run_node(ctx.main(), *nodeids)
    assert control.returncode == 0, (
        f"{nodeids} FAIL on a main-shaped clone (HEAD == main == origin/main) -- the verdict "
        f"depends on live state, not on the branch:\n{tail(control)}")
    lane = ctx.run_node(ctx.lane(**lane_shape), *nodeids)
    assert lane.returncode == 0, (
        f"{nodeids} pass on main and FAIL on a lane-shaped checkout:\n{tail(lane)}")
