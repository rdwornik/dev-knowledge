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
  session    a live (`busy`, read off `status` or -- a session still STARTING -- `state`) session
             from `claude agents --json` whose `cwd` ends in `.claude/worktrees/<slug>`. The leg
             that was missing on the day.

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
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Iterable

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


def _run(argv: list, cwd: Path | None = None, timeout: int = 30) -> str:
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                              cwd=str(cwd) if cwd else None, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        raise OccupancyError(f"could not run {argv[0]}: {exc!r}") from exc
    if proc.returncode != 0:
        raise OccupancyError(f"{' '.join(argv[:3])} failed: {proc.stderr.strip()!r}")
    return proc.stdout


def primary_root(start: Path = Path()) -> Path:
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


def _status_of(row: dict) -> str | None:
    """A session record's liveness field, for the READABILITY check only (is there SOME string
    naming a status at all). Most records carry `status`; a record for a session still
    STARTING carries `state` instead (D23: `worktree_occupancy` exited 2 -- "could not look" --
    on a starting record, because it read `status` alone and a payload naming only `state` is a
    different external shape, not an unreadable one). A record naming neither is genuinely
    unreadable, not a quiet "not busy". Liveness ITSELF is `_is_live`, not this function -- see
    its docstring for why the two fields are not simply preferred one over the other."""
    for key in ("status", "state"):
        value = row.get(key)
        if isinstance(value, str):
            return value
    return None


def _is_live(row: dict) -> bool:
    """RECON s5.3 leg 4 is a `busy` session. EITHER `status` or `state` claiming `busy` is
    enough -- a record naming both fields with CONFLICTING values (one busy, one not) is read
    as busy. Codex terra review, HIGH (`docs/audits/2026-09-24-codex-lane-handback-fixes.md`):
    preferring `status` alone let `{"status": "idle", "state": "busy", "cwd": <tree>}` read as
    non-live, missing a session mid-transition between the two external shapes. Fail-closed
    toward OCCUPIED on a record this reader was not told to expect, never toward FREE."""
    return any(row.get(key) == _LIVE_STATUS for key in ("status", "state"))


def _validated_sessions(sessions: object) -> list:
    """The session list, or `OccupancyError`. A record this cannot judge is never read as "not
    holding the tree": a non-mapping row, a row with no `status`/`state`, or a `busy` row with
    no `cwd` means the payload has changed shape and the session leg cannot be trusted."""
    if not isinstance(sessions, list):
        raise OccupancyError("the session payload is not a list")
    for i, row in enumerate(sessions):
        if not isinstance(row, dict):
            raise OccupancyError(f"session record {i} is not a mapping: {row!r}")
        if _status_of(row) is None:
            raise OccupancyError(f"session record {i} has no string `status`/`state`: {row!r}")
        if _is_live(row) and not isinstance(row.get("cwd"), str):
            raise OccupancyError(f"busy session record {i} has no string `cwd`: {row!r}")
    return sessions


def _dir_exists(path: Path) -> bool:
    """True/False for present/absent; anything else (permissions, I/O) is `OccupancyError`.
    `Path.exists()` cannot be used: it answers False on an error, so a husk this process cannot
    stat would read FREE."""
    try:
        os.stat(path)
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise OccupancyError(f"could not stat {path}: {exc!r}") from exc
    return True


def _session_holds(session: dict, tree: str) -> bool:
    return _is_live(session) and _norm(session["cwd"]) == tree


def check(slug: str, root: Path, sessions: list | None = None,
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
    sessions = _validated_sessions(live_sessions() if sessions is None else sessions)
    ignored = set(ignore_sessions)
    legs = {
        "worktree": tree in _registered_worktrees(root),
        "directory": _dir_exists(tree_dir),
        "branch": _has_branch(root, f"worktree-{slug}"),
        "session": any(_session_holds(s, tree) for s in sessions
                       if s.get("id") not in ignored and s.get("sessionId") not in ignored),
    }
    return Occupancy(slug, legs)


def main(argv: list | None = None) -> int:
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
