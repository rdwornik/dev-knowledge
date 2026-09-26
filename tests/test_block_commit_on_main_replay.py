"""tests/test_block_commit_on_main_replay.py -- lane-organ-wirings Done-contract item 3.

`block-commit-on-main` moved from `stages: [manual]` to the default `pre-commit` stage
(`.pre-commit-config.yaml`); `tests/test_block_commit_on_main.py` already pins the hook's
own predicate (E1-E5, W1). This file is the OTHER half the contract asks for: a REPLAY of
`templates/integrator-order-template.md`'s own steps 2, 3 and 5 -- the integration-branch
`--no-ff` merge, the regenerated-files commit, the receipt/ledger-line commit, and the
fast-forward push to `main` -- proving each one passes the newly-armed hook. The claim this
guards is the contract's own Value line: the hook "refuses by default -- without refusing
the integrator's own path", which is why this lane merges last.

Why this is a SEPARATE rig from the acceptance matrix's E2/E3/W1, rather than a restatement
of them: those prove the PREDICATE in isolation (a generic feature branch, a generic clean
merge). This proves the SEQUENCE an integrator actually runs, in the actual branch shapes
the template names (`worktree-integrate-<lane>`, not `feat/x`), ending in a real
`git push origin HEAD:main` against a bare remote -- so a regression in how those specific
steps compose (not just in the predicate itself) would show up here even if the matrix
stayed green.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "block_commit_on_main.py"


def _run(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True, encoding="utf-8", errors="replace")


def _try(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def _rev(repo, ref="HEAD"):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", ref],
                          check=True, capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def _commit(repo, msg, fname, content):
    (Path(repo) / fname).write_text(content, encoding="utf-8")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-q", "-m", msg)


def _arm(repo):
    """Install the REAL script as this repo's pre-commit hook (mirrors
    test_block_commit_on_main.py's `_arm`; shared config, so every worktree of `repo`
    inherits it -- see that file's W1 for the proof this holds across worktrees)."""
    out = subprocess.run(["git", "-C", str(repo), "rev-parse", "--git-path", "hooks"],
                         check=True, capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stdout.strip()
    hooks = Path(out) if Path(out).is_absolute() else Path(repo) / out
    hooks.mkdir(parents=True, exist_ok=True)
    hook = hooks / "pre-commit"
    hook.write_text("#!/bin/sh\n" + f'exec "{Path(sys.executable).as_posix()}" '
                    f'"{_SCRIPT.as_posix()}"\n', encoding="utf-8", newline="\n")
    hook.chmod(0o755)


def _stage_and_assert_allowed(repo, fname, content, msg):
    path = Path(repo) / fname
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    _run(repo, "add", "-A")
    r = _try(repo, "commit", "-q", "-m", msg)
    assert r.returncode == 0, (
        f"the hook refused a commit on {fname!r} on the integration branch: {r.stderr}")


def _init_bare_origin_and_primary(tmp_path):
    """A bare `origin` plus a `primary` clone on `main` -- the shape the integrator's own
    push (`git push origin HEAD:main`) actually targets, not a single local repo."""
    origin = tmp_path / "origin.git"
    _run(tmp_path, "init", "-q", "--bare", str(origin))
    primary = tmp_path / "primary"
    _run(tmp_path, "clone", "-q", str(origin), str(primary))
    _run(primary, "config", "user.email", "t@t.t")
    _run(primary, "config", "user.name", "t")
    # ABSOLUTE hooksPath (test_block_commit_on_main.py::_init_repo explains why relative
    # breaks a linked worktree); shared config, so it is set exactly once, on `primary`.
    _run(primary, "config", "core.hooksPath", str((primary / ".git" / "hooks").resolve()))
    _commit(primary, "seed", "seed.txt", "seed\n")
    _run(primary, "branch", "-M", "main")
    _run(primary, "push", "-q", "-u", "origin", "main")
    return origin, primary


@requires_git
def test_the_integrator_replay_never_refuses_its_own_path(tmp_path):
    """Steps 2, 3 and 5 of templates/integrator-order-template.md, replayed end to end
    against the real, now-armed hook -- none of them land on a branch literally `main`."""
    _origin, primary = _init_bare_origin_and_primary(tmp_path)
    base_main = _rev(primary)

    # The lane's own worktree, on its own branch off main -- what it hands back.
    lane_wt = tmp_path / "lane"
    _run(primary, "worktree", "add", "-q", "-b", "worktree-lane-organ-wirings-test",
        str(lane_wt), "main")
    _commit(lane_wt, "lane work", "lane.txt", "lane work\n")
    lane_branch_tip = _rev(lane_wt)

    # Step 2: "a temporary worktree on a NEW branch from origin/main ... merge the lane
    # there --no-ff". Armed only now (ARM LAST -- see test_block_commit_on_main.py::_arm):
    # every fixture commit above must land regardless of the gate under test.
    integ_wt = tmp_path / "int"
    _run(primary, "worktree", "add", "-q", "-b", "worktree-integrate-lane-organ-wirings-test",
        str(integ_wt), "main")
    _arm(primary)

    merged = _try(integ_wt, "merge", "--no-ff", "--no-edit",
                 "worktree-lane-organ-wirings-test")
    assert merged.returncode == 0, (
        f"the integration-branch --no-ff merge did not land: {merged.stderr}")
    assert len(subprocess.run(
        ["git", "-C", str(integ_wt), "rev-list", "--parents", "-n", "1", "HEAD"],
        check=True, capture_output=True, text=True, encoding="utf-8", errors="replace"
    ).stdout.split()) == 3, "the merge did not land as a two-parent commit"

    # Step 2's "regenerate generated files on the merged tree" and step 5's "the ledger row
    # written" -- plain commits ON THE INTEGRATION BRANCH, never on `main`.
    _stage_and_assert_allowed(integ_wt, "BACKLOG.md", "regenerated\n", "regen: BACKLOG.md")
    _stage_and_assert_allowed(integ_wt, "logs/MERGE-RECEIPTS.jsonl", '{"slug": "x"}\n',
                              "receipt/ledger line")
    integ_tip = _rev(integ_wt)
    assert integ_tip not in (lane_branch_tip, base_main), (
        "the merge + regen + ledger commits produced no new integration tip")

    # Step 5: "git push origin HEAD:main -- a push that only advances origin's main". A
    # fast-forward ref update creates no commit, so pre-commit is never in the loop for it
    # either -- asserted end to end via a real push to the bare remote, not inferred.
    pushed = _try(integ_wt, "push", "origin", "HEAD:main")
    assert pushed.returncode == 0, f"the fast-forward push to main was refused: {pushed.stderr}"
    _run(primary, "fetch", "-q", "origin")
    assert _rev(primary, "origin/main") == integ_tip
    assert _rev(primary, "origin/main") != base_main
