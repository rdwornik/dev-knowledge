#!/usr/bin/env python
"""worktree_occupancy.py -- is this lane slug already taken? The four-leg predicate of RECON s5.3.

WHY IT EXISTS. `dispatch` checks nothing before it spawns. On 2026-09-20 two `--bg` jobs entered
`.claude/worktrees/lane-loop-eval` 70 seconds apart and only one lane's voluntary yield saved the
branch (`to-browser/SESSION-launch-loop-eval.md` s0). RECON s5 measured why no single instrument
is enough -- the four DISAGREED that night:

  worktree   `git worktree list` registers `.claude/worktrees/<slug>` -- what `git worktree add`
             collides with. (A prunable registration whose directory is gone still fires.)
  directory  `.claude/worktrees/<slug>` exists on disk. The leg that catches the two HUSKS git
             had forgotten (empty directories left by a teardown that removed the registration
             and the contents but not the directory); no git command sees them.
  branch     a local `worktree-<slug>` branch exists. `Start-DispatchLane` refuses when it does,
             so a surviving branch is its own refusal.
  session    a live (`status: busy`) session from `claude agents --json` whose `cwd` ends in
             `.claude/worktrees/<slug>`. The leg that was missing on the day.

Exit 0 = free, 1 = occupied (the legs that fired are named), 2 = could not look or bad slug. A
tool that cannot look never prints FREE.

READ-ONLY. It never removes, unlocks, repairs or prunes anything and never touches a session:
the husks are the operator's call, and this organ only NAMES what is in the way (N3: an organ
records a refusal with a non-zero exit code; it never ends someone's work).

HONEST LIMITS
  * A conforming slug is not a conforming lane; this reads occupancy, not naming
    (`validate_branch_naming` reads naming).
  * `busy` is the RECON s5.3 definition of live. An `idle` session in the tree holds a checkout
    but is not executing, so it does not fire; a caller that wants it counted has the JSON.
  * Run from INSIDE the lane it asks about (the `moment:lane-start` shape), its own worktree,
    branch and session all fire -- it answers "is this taken", and by then it is. Pass
    `--ignore-session <id>` to exclude the caller's own job; legs 1-3 are then the caller's own
    checkout. The intended use is BEFORE the launch.
  * `claude agents --json` is the only session source; when it cannot be run the session leg is
    unknown and the run exits 2 rather than reporting a tree free on three of four legs.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

LEGS = ("worktree", "directory", "branch", "session")

#: The lane slug alone (`lane-l2-dispatch-guards`), never the branch form and never a path.
_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

#: RECON s5.3 leg 4: only a `busy` session is executing.
_LIVE_STATUS = "busy"


class OccupancyError(Exception):
    """The tool could not look (or was handed a slug it will not look up) -- distinct from
    looking and finding the slug occupied."""


@dataclass(frozen=True)
class Occupancy:
    slug: str
    legs: dict

    @property
    def fired(self) -> tuple:
        return tuple(leg for leg in LEGS if self.legs.get(leg))

    @property
    def occupied(self) -> bool:
        return bool(self.fired)


def _run(argv: list, cwd: Optional[Path] = None, timeout: int = 30) -> str:
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                              cwd=str(cwd) if cwd else None, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        raise OccupancyError(f"could not run {argv[0]}: {exc!r}") from exc
    if proc.returncode != 0:
        raise OccupancyError(f"{' '.join(argv[:3])} failed: {proc.stderr.strip()!r}")
    return proc.stdout


def primary_root(start: Path = Path(".")) -> Path:
    """The primary checkout, resolved through `--git-common-dir` so a lane worktree finds the
    hub whose `.claude/worktrees/` holds its siblings."""
    out = _run(["git", "-C", str(start), "rev-parse", "--path-format=absolute",
                "--git-common-dir"]).strip()
    return Path(out).parent


def _norm(path: str) -> str:
    return path.replace("\\", "/").rstrip("/").casefold()


def _registered_worktrees(root: Path) -> set:
    out = _run(["git", "-C", str(root), "worktree", "list", "--porcelain"])
    return {_norm(line[len("worktree "):]) for line in out.splitlines()
            if line.startswith("worktree ")}


def _has_branch(root: Path, branch: str) -> bool:
    out = _run(["git", "-C", str(root), "branch", "--list", "--format=%(refname:short)", branch])
    return branch in {ln.strip() for ln in out.splitlines()}


def live_sessions() -> list:
    """`claude agents --json`, parsed. Raises `OccupancyError` when it cannot be run."""
    exe = shutil.which("claude")
    if exe is None:
        raise OccupancyError("`claude` is not on PATH -- the live-session leg cannot be read")
    out = _run([exe, "agents", "--json"], timeout=60)
    try:
        data = json.loads(out)
    except ValueError as exc:
        raise OccupancyError(f"`claude agents --json` did not return JSON: {exc}") from exc
    if not isinstance(data, list):
        raise OccupancyError("`claude agents --json` did not return a list")
    return data


def _session_holds(session: dict, tree: str) -> bool:
    cwd = _norm(str(session.get("cwd") or ""))
    return session.get("status") == _LIVE_STATUS and cwd == tree


def check(slug: str, root: Path, sessions: Optional[list] = None,
          ignore_sessions: Iterable[str] = ()) -> Occupancy:
    """Run the four legs for `slug` against the primary checkout `root`.

    `sessions` is the parsed `claude agents --json` list; `None` reads it live. Raises
    `OccupancyError` when a leg cannot be read, so an unreadable leg is never a quiet "free".
    """
    if not _SLUG_RE.match(slug or "") or slug.startswith("worktree-"):
        raise OccupancyError(f"{slug!r} is not a bare lane slug (lowercase kebab-case, no "
                             f"`worktree-` prefix, no path)")
    root = Path(root)
    if not root.is_dir():
        raise OccupancyError(f"{root} is not a directory")
    tree_dir = root / ".claude" / "worktrees" / slug
    tree = _norm(str(tree_dir))
    if sessions is None:
        sessions = live_sessions()
    ignored = set(ignore_sessions)
    legs = {
        "worktree": tree in _registered_worktrees(root),
        "directory": tree_dir.exists(),
        "branch": _has_branch(root, f"worktree-{slug}"),
        "session": any(_session_holds(s, tree) for s in sessions
                       if s.get("id") not in ignored and s.get("sessionId") not in ignored),
    }
    return Occupancy(slug, legs)


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", help="the lane slug, e.g. lane-l2-dispatch-guards")
    ap.add_argument("--repo-root", help="the primary checkout (default: resolved from cwd)")
    ap.add_argument("--sessions-file", help="read `claude agents --json` output from this file "
                                            "instead of running it")
    ap.add_argument("--ignore-session", action="append", default=[], metavar="ID",
                    help="a session id (or sessionId) not to count -- the caller's own job")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    try:
        root = Path(args.repo_root) if args.repo_root else primary_root()
        sessions = None
        if args.sessions_file:
            try:
                sessions = json.loads(Path(args.sessions_file).read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise OccupancyError(f"could not read --sessions-file: {exc}") from exc
        res = check(args.slug, root, sessions=sessions, ignore_sessions=args.ignore_session)
    except OccupancyError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"slug": res.slug, "occupied": res.occupied,
                          "fired": list(res.fired), "legs": res.legs}))
    elif res.occupied:
        print(f"OCCUPIED {res.slug}: {', '.join(res.fired)}")
        for leg in LEGS:
            print(f"  {'FIRED' if res.legs[leg] else 'clear'}  {leg}")
    else:
        print(f"FREE {res.slug}: all four legs clear")
    return 1 if res.occupied else 0


if __name__ == "__main__":
    sys.exit(main())
