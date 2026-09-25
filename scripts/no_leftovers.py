#!/usr/bin/env python
"""no_leftovers.py — teardown verified by code, not by a human reading eleven lines.

WHAT THIS IS
------------
The eleven "no leftovers" checks the integrator ran by hand on 2026-09-20
(`to-browser/SESSION-integrator-loop-eval.md` §11), as one read-only verifier for one lane slug.
It is the command `ecosystem/harness.yaml` declares for the teardown moment's `no_leftovers`
organ (`no_leftovers.py verify --lane {lane}`), and CLAUDE.md §5 critical rule 9's "removes AND
VERIFIES removal" made executable.

WHY A HUMAN READING ELEVEN LINES IS NOT ENOUGH. Two empty directories, `lane-z-4-...` (15.09) and
`lane-ab-833-...` (17.09), sat under `.claude/worktrees/` for five days: unregistered with git,
absent from `git worktree list`, no branch, nothing for `git status` to say. Only a directory
enumeration sees them (`[#762]`: a gitignored leftover reads clean on both git views).

THE ELEVEN CHECKS (numbers are the spec's order)
   1 worktree-not-registered            `git worktree list --porcelain` names neither lane path nor branch
   2 worktree-dir-absent                `.claude/worktrees/<slug>` is not on disk
   3 worktree-dir-enumeration-empty     `find <path> -mindepth 1` finds nothing (the check `git status` cannot do)
   4 worktree-admin-entry-absent        no `.git/worktrees/<name>` for the lane (by name or by `gitdir` target)
   5 no-lane-branch                     no `worktree-<slug>` in local or remote-tracking branches
   6 no-ref-names-lane                  no ref of any kind whose name carries the slug
   7 no-remote-head                     `git ls-remote --heads origin` carries no head for the lane
   8 job-record-absent                  no LIVE `~/.claude/jobs/<id>/state.json` points at the lane
   9 job-not-in-agents                  `claude agents --json` lists no LIVE session cwd'd in the lane
  10 working-tree-clean                 the primary's `git status --porcelain` is empty
  11 main-equals-origin-main            local `main` == the remote's `main` (read with ls-remote, never a stale tracking ref)

R3 (2026-09-25, LANE-5B2-5-teardown-visible): teardown STOPS a lane's session (`batch_janitor.py`)
rather than removing it, so its transcript survives -- which means its job record and its
`claude agents --json` entry are BOTH expected to keep pointing at the lane after a clean
teardown. Checks 8 and 9 therefore read each record's own `state` field and only count a
pointing record as a leftover when that state is NOT one of `batch_janitor`'s own
`_ENDED_STATES` (imported, never re-typed) -- a record with no readable `state` still fails
closed, the same posture every other unreadable-evidence case here takes.

With no slug it runs the husk scan alone: every directory under `.claude/worktrees/` that git does
not register, and every registration whose directory is gone.

POSTURE — READ-ONLY, BY CONSTRUCTION. It verifies; it never removes, unlocks, prunes or deletes.
A leftover is REPORTED, not repaired: repair is an ordered act (job first, then unlock -> remove
-> prune -> branch delete) with an owner. Three independent pins: `_git` refuses every git verb
that is not a listing; the tests assert an AST with no mutating call; and a run over a
leftover-laden tree leaves it byte-identical.

EXIT CODE. 0 = every check passed; 1 = at least one leftover; 2 = usage / repo not resolvable.
Anything that cannot be READ (no `origin`, unreadable jobs directory, `claude` absent) is a FAIL,
never a PASS — an unread check proves nothing.

HONEST LIMITS
  * A slugged run reports OTHER lanes' husks as NOTE lines and does not let them decide the exit
    code: the verdict is about this lane's teardown. The slug-less run is the one that fails on them.
  * Run it from the primary checkout (or anywhere — it resolves the primary from the git common
    dir). Run from INSIDE the lane it is verifying, checks 1-2 correctly fail: the lane is there.
  * Check 9's cwd/worktreePath matching is only as good as the fields `claude agents --json` emits.
  * It cannot see a process holding a handle on a directory (the VS Code watcher, `[#762]`); it can
    only report that the directory is still there.
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

# THE ONE HOME FOR "IS THIS JOB'S OWN STATE TERMINAL", imported rather than re-typed -- R3
# (checks 8/9 below) reads the same vocabulary `batch_janitor.py` already owns and tests against
# `dispatch.py`'s own `_ENDED`, for the same reason `batch_janitor` imports `dispatch` instead of
# guessing: a third private copy would drift from the two that already agree.
try:
    from scripts import batch_janitor as _bj
except ImportError:  # pragma: no cover -- exercised by the scripts/-on-sys.path entrypoint
    import batch_janitor as _bj

EXIT_OK = 0
EXIT_LEFTOVER = 1
EXIT_USAGE = 2

_SLUG_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_MAX_EVIDENCE = 8
_ENUM_CAP = 200
_GIT_TIMEOUT = 60


class ReadOnlyViolation(RuntimeError):
    """Raised when this module is asked to run a git verb that could change anything."""


@dataclass(frozen=True)
class Result:
    number: int
    name: str
    passed: bool
    evidence: str


# --- the read-only git wrapper --------------------------------------------------

def _is_listing(args: tuple[str, ...]) -> bool:
    if not args:
        return False
    verb = args[0]
    if verb in {"rev-parse", "status", "for-each-ref", "ls-remote"}:
        return True
    if verb == "worktree":
        return len(args) > 1 and args[1] == "list"
    if verb == "remote":
        return len(args) == 1 or args[1] == "get-url"
    return False


def _git(repo: Path, *args: str, timeout: int = _GIT_TIMEOUT) -> subprocess.CompletedProcess:
    """Run a git LISTING verb in `repo`; refuse anything else before it starts."""
    if not _is_listing(args):
        raise ReadOnlyViolation(f"no_leftovers is read-only; refusing `git {' '.join(args)}`")
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    return subprocess.run(["git", "--no-optional-locks", "-C", str(repo), *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          timeout=timeout, env=env)


def _git_out(repo: Path, *args: str) -> tuple[str | None, str]:
    """(stdout, "") on success; (None, reason) when git failed or could not run."""
    try:
        proc = _git(repo, *args)
    except (OSError, subprocess.SubprocessError) as exc:
        return None, f"git {args[0]} could not run: {exc}"
    if proc.returncode != 0:
        return None, f"git {' '.join(args[:2])} exited {proc.returncode}: {proc.stderr.strip()[:200]}"
    return proc.stdout, ""


# --- small helpers ---------------------------------------------------------------

def _norm(path: str | Path) -> str:
    return re.sub(r"[\\/]+", "/", str(path)).rstrip("/").casefold()


def _lane_re(slug: str) -> re.Pattern[str]:
    """The slug as a whole token, optionally `worktree-`-prefixed; `-2`, `x` suffixes do NOT match."""
    return re.compile(r"(?<![A-Za-z0-9._-])(?:worktree-)?" + re.escape(slug) + r"(?![A-Za-z0-9._-])")


def _shown(items: list[str]) -> str:
    head = ", ".join(items[:_MAX_EVIDENCE])
    return head + (f" (+{len(items) - _MAX_EVIDENCE} more)" if len(items) > _MAX_EVIDENCE else "")


def resolve_primary(start: Path) -> Path:
    """The primary checkout that owns `start`, whether `start` is the primary or a linked worktree."""
    out, why = _git_out(start, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if out is None or not out.strip():
        raise ValueError(f"not inside a git repository: {start} ({why})")
    common = Path(out.strip())
    if not common.is_absolute():
        common = (start / common)
    if common.name != ".git":
        raise ValueError(f"git common dir {common} is not a `.git` directory (bare repo?)")
    return common.parent


def _common_dir(repo: Path) -> Path | None:
    out, _ = _git_out(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if out is None or not out.strip():
        return None
    p = Path(out.strip())
    return p if p.is_absolute() else repo / p


def _worktrees_root(repo: Path) -> Path:
    return repo / ".claude" / "worktrees"


def _registered(repo: Path) -> tuple[list[dict[str, str]] | None, str]:
    """Registered worktrees as [{worktree, branch?, prunable?}], or (None, reason)."""
    out, why = _git_out(repo, "worktree", "list", "--porcelain")
    if out is None:
        return None, why
    entries: list[dict[str, str]] = []
    cur: dict[str, str] = {}
    for line in out.splitlines():
        if not line.strip():
            if cur:
                entries.append(cur)
                cur = {}
            continue
        key, _, val = line.partition(" ")
        cur[key] = val
    if cur:
        entries.append(cur)
    return entries, ""


def enumerate_entries(path: Path, cap: int = _ENUM_CAP) -> tuple[list[str], bool, str]:
    """`find <path> -mindepth 1`, bounded and non-following. -> (relative entries, truncated, error)."""
    found: list[str] = []
    stack = [path]
    is_junction = getattr(Path, "is_junction", lambda self: False)
    while stack:
        cur = stack.pop()
        try:
            children = sorted(cur.iterdir())
        except OSError as exc:
            return found, False, f"could not list {cur}: {exc}"
        for child in children:
            if len(found) >= cap:
                return found, True, ""
            found.append(child.relative_to(path).as_posix())
            try:
                descend = child.is_dir() and not child.is_symlink() and not is_junction(child)
            except OSError:
                descend = False
            if descend:
                stack.append(child)
    return found, False, ""


# --- the husk scan ----------------------------------------------------------------

def find_husks(repo: Path) -> list[Path]:
    """Directories under `.claude/worktrees/` that git does not register — the leak `git worktree list` cannot see."""
    root = _worktrees_root(repo)
    if not root.is_dir():
        return []
    entries, _ = _registered(repo)
    known = {_norm(e["worktree"]) for e in (entries or [])}
    return sorted((p for p in root.iterdir() if p.is_dir() and _norm(p) not in known),
                  key=lambda p: p.name)


def find_prunable(repo: Path) -> list[Path]:
    """Worktrees git still registers under `.claude/worktrees/` whose directory is gone."""
    entries, _ = _registered(repo)
    root = _norm(_worktrees_root(repo))
    return [Path(e["worktree"]) for e in (entries or [])
            if _norm(e["worktree"]).startswith(root + "/") and not Path(e["worktree"]).exists()]


# --- the eleven checks --------------------------------------------------------------

def _refs(repo: Path, *patterns: str) -> tuple[list[str] | None, str]:
    out, why = _git_out(repo, "for-each-ref", "--format=%(refname)", *patterns)
    return (None, why) if out is None else ([ln for ln in out.splitlines() if ln], "")


def _is_ended(state_value: object) -> bool:
    """True only when `state_value` is a string naming one of `batch_janitor`'s own terminal
    states. R3: a job/agent record that still points at a torn-down lane is expected to survive
    with a terminal `state` -- that is not a leftover. Anything else (missing, non-string,
    unrecognized) fails closed: unread or unknown evidence is not clean here either."""
    return isinstance(state_value, str) and state_value.lower() in _bj._ENDED_STATES


def _points_at_lane(rec: dict, lane_path: str, branch: str) -> bool:
    for key in ("cwd", "worktreePath"):
        v = rec.get(key)
        if isinstance(v, str) and v:
            n = _norm(v)
            if n == lane_path or n.startswith(lane_path + "/"):
                return True
    return rec.get("worktreeBranch") == branch


def run_checks(repo: Path, lane: str, *, jobs_dir: Path, agents: list[dict] | None,
               remote: str = "origin", main_branch: str = "main") -> list[Result]:
    """Run the eleven checks for `lane` against the primary checkout `repo`.

    `agents` is the parsed `claude agents --json` list, or None when it could not be read (check 9
    then FAILS rather than passing on no evidence).
    """
    lane_path = _worktrees_root(repo) / lane
    lane_norm = _norm(lane_path)
    branch = f"worktree-{lane}"
    lane_re = _lane_re(lane)
    res: list[Result] = []

    def add(n: int, name: str, ok: bool, evidence: str) -> None:
        res.append(Result(n, name, ok, evidence))

    # 1
    entries, why = _registered(repo)
    if entries is None:
        add(1, "worktree-not-registered", False, f"unreadable: {why}")
    else:
        hits = [e["worktree"] for e in entries
                if _norm(e["worktree"]) == lane_norm or e.get("branch") == f"refs/heads/{branch}"]
        add(1, "worktree-not-registered", not hits,
            f"registered: {_shown(hits)}" if hits else f"{len(entries)} registered worktree(s), none is {lane}")

    # 2
    on_disk = lane_path.exists() or lane_path.is_symlink()
    add(2, "worktree-dir-absent", not on_disk,
        f"{lane_path} is on disk" if on_disk else f"{lane_path} absent")

    # 3
    if not on_disk:
        add(3, "worktree-dir-enumeration-empty", True, f"{lane_path} absent; nothing to enumerate")
    else:
        found, truncated, err = enumerate_entries(lane_path)
        if err:
            add(3, "worktree-dir-enumeration-empty", False, err)
        elif found:
            add(3, "worktree-dir-enumeration-empty", False,
                f"{len(found)}{'+' if truncated else ''} entr(y/ies) under {lane_path}: {_shown(found)}")
        else:
            add(3, "worktree-dir-enumeration-empty", True, f"{lane_path} present but holds 0 entries")

    # 4
    common = _common_dir(repo)
    if common is None:
        add(4, "worktree-admin-entry-absent", False, "unreadable: git common dir not resolvable")
    else:
        admin_root = common / "worktrees"
        hits, unreadable = [], []
        if admin_root.is_dir():
            for d in sorted(admin_root.iterdir()):
                if not d.is_dir():
                    continue
                try:
                    target = (d / "gitdir").read_text(encoding="utf-8", errors="replace").strip()
                except OSError:
                    target = ""
                if not target:
                    unreadable.append(d.name)          # fail closed: unknown evidence is not clean
                elif d.name == lane or _norm(Path(target).parent) == lane_norm:
                    hits.append(d.name)                # a `<slug>1` collision suffix counts only by its gitdir target
        add(4, "worktree-admin-entry-absent", not (hits or unreadable),
            (f"admin entries for the lane: {_shown(hits)} under {admin_root}" if hits else "")
            + (f"{'; ' if hits else ''}admin entries with an unreadable gitdir (cannot rule the lane out): "
               f"{_shown(unreadable)}" if unreadable else "")
            or f"no admin entry for {lane} under {admin_root}")

    # 5
    refs, why = _refs(repo, "refs/heads", "refs/remotes")
    if refs is None:
        add(5, "no-lane-branch", False, f"unreadable: {why}")
    else:
        hits = [r for r in refs
                if re.sub(r"^refs/(heads|remotes/[^/]+)/", "", r) == branch]
        add(5, "no-lane-branch", not hits,
            f"branch ref(s): {_shown(hits)}" if hits else f"no {branch} among {len(refs)} branch ref(s), local or remote")

    # 6
    refs, why = _refs(repo)
    if refs is None:
        add(6, "no-ref-names-lane", False, f"unreadable: {why}")
    else:
        hits = [r for r in refs if lane_re.search(r)]
        add(6, "no-ref-names-lane", not hits,
            f"ref(s) naming the lane: {_shown(hits)}" if hits else f"0 of {len(refs)} ref(s) name {lane}")

    # 7
    remote_urls, why = _git_out(repo, "remote")
    if remote_urls is None or remote not in remote_urls.split():
        add(7, "no-remote-head", False, f"cannot verify: no remote named '{remote}' ({why or 'not configured'})")
    else:
        out, why = _git_out(repo, "ls-remote", "--heads", remote)
        if out is None:
            add(7, "no-remote-head", False, f"unreadable: {why}")
        else:
            heads = [ln.split("\t", 1)[1] for ln in out.splitlines() if "\t" in ln]
            hits = [h for h in heads if lane_re.search(h)]
            add(7, "no-remote-head", not hits,
                f"remote head(s): {_shown(hits)}" if hits else f"0 of {len(heads)} head(s) on {remote} name {lane}")

    # 8
    if not jobs_dir.is_dir():
        add(8, "job-record-absent", False, f"unreadable: jobs directory {jobs_dir} not found")
    else:
        hits, unparseable, seen = [], [], 0
        for state in sorted(jobs_dir.glob("*/state.json")):
            seen += 1
            try:
                rec = json.loads(state.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                unparseable.append(state.parent.name)
                continue
            if isinstance(rec, dict) and _points_at_lane(rec, lane_norm, branch) \
                    and not _is_ended(rec.get("state")):
                hits.append(state.parent.name)
        note = (f"{'; ' if hits else ''}job record(s) that could not be read or parsed "
                f"(cannot rule the lane out): {_shown(unparseable)}") if unparseable else ""
        add(8, "job-record-absent", not (hits or unparseable),
            (f"LIVE job record(s) pointing at the lane: {_shown(hits)}" if hits else "")
            + note or f"0 of {seen} job record(s) point at {lane}, live")

    # 9
    if agents is None:
        add(9, "job-not-in-agents", False, "unreadable: `claude agents --json` could not be read")
    else:
        hits = [f"{a.get('id', '?')}({a.get('status', '?')})" for a in agents
                if isinstance(a, dict) and _points_at_lane(a, lane_norm, branch)
                and not _is_ended(a.get("state"))]
        add(9, "job-not-in-agents", not hits,
            f"LIVE session(s) in the lane: {_shown(hits)}" if hits else f"0 of {len(agents)} listed session(s) are LIVE in {lane}")

    # 10
    out, why = _git_out(repo, "status", "--porcelain")
    if out is None:
        add(10, "working-tree-clean", False, f"unreadable: {why}")
    else:
        lines = [ln for ln in out.splitlines() if ln.strip()]
        add(10, "working-tree-clean", not lines,
            f"{len(lines)} path(s) dirty in {repo}: {_shown(lines)}" if lines else f"{repo} clean")

    # 11
    local, why_l = _git_out(repo, "rev-parse", "--verify", f"refs/heads/{main_branch}")
    if remote_urls is None or remote not in remote_urls.split():
        add(11, "main-equals-origin-main", False, f"cannot verify: no remote named '{remote}'")
    else:
        rem, why_r = _git_out(repo, "ls-remote", remote, f"refs/heads/{main_branch}")
        if local is None or rem is None:
            add(11, "main-equals-origin-main", False, f"unreadable: {why_l or why_r}")
        else:
            rem_sha = rem.split("\t", 1)[0].strip() if rem.strip() else ""
            ok = bool(rem_sha) and rem_sha == local.strip()
            add(11, "main-equals-origin-main", ok,
                f"{main_branch} {local.strip()[:8]} == {remote}/{main_branch} {rem_sha[:8]}" if ok
                else f"{main_branch} {local.strip()[:8]} != {remote}/{main_branch} {rem_sha[:8] or '(absent)'}")
    return res


# --- CLI ----------------------------------------------------------------------------

def _read_agents(agents_json: str | None) -> list[dict] | None:
    """The `claude agents --json` list from a file, or by running the (listing) CLI; None on any failure."""
    try:
        if agents_json:
            raw = Path(agents_json).read_text(encoding="utf-8")
        else:
            exe = shutil.which("claude")
            if not exe:
                return None
            raw = subprocess.run([exe, "agents", "--json"], capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", timeout=_GIT_TIMEOUT,
                                 check=True).stdout
        data = json.loads(raw)
    except (OSError, ValueError, subprocess.SubprocessError):
        return None
    if isinstance(data, dict):
        data = data.get("agents")
    return data if isinstance(data, list) else None


def _report_husks(repo: Path, header: str) -> int:
    husks, prunable = find_husks(repo), find_prunable(repo)
    for h in husks:
        try:
            n = sum(1 for _ in h.iterdir())
        except OSError:
            n = -1
        print(f"{header} husk directory (unregistered with git): {h}  [{n if n >= 0 else '?'} top-level entr(y/ies)]")
    for p in prunable:
        print(f"{header} registered but directory gone (prunable): {p}")
    return len(husks) + len(prunable)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="no_leftovers.py", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verify", help="run the eleven checks for --lane, or the husk scan without it")
    v.add_argument("--lane", help="lane slug, e.g. lane-l5-no-leftovers (worktree dir name)")
    v.add_argument("--repo", help="repository to check (default: the primary of the current directory)")
    v.add_argument("--jobs-dir", help="claude jobs directory (default: ~/.claude/jobs)")
    v.add_argument("--agents-json", help="read `claude agents --json` output from this file instead of running it")
    args = ap.parse_args(argv)

    if args.lane is not None and not _SLUG_RE.fullmatch(args.lane):
        print(f"no_leftovers: refusing lane slug {args.lane!r} — must match {_SLUG_RE.pattern}", file=sys.stderr)
        return EXIT_USAGE
    try:
        repo = resolve_primary(Path(args.repo) if args.repo else Path.cwd())
    except ValueError as exc:
        print(f"no_leftovers: {exc}", file=sys.stderr)
        return EXIT_USAGE

    if args.lane is None:
        n = _report_husks(repo, "FAIL")
        print(f"no-leftovers husk scan of {_worktrees_root(repo)}: "
              + ("CLEAN (no husk)" if n == 0 else f"NOT CLEAN ({n} leftover(s))"))
        return EXIT_OK if n == 0 else EXIT_LEFTOVER

    jobs_dir = Path(args.jobs_dir) if args.jobs_dir else Path.home() / ".claude" / "jobs"
    results = run_checks(repo, args.lane, jobs_dir=jobs_dir, agents=_read_agents(args.agents_json))
    for r in results:
        print(f"{'PASS' if r.passed else 'FAIL'} {r.number:02d} {r.name}  {r.evidence}")
    _report_husks(repo, "NOTE")
    failed = [r for r in results if not r.passed]
    print(f"no-leftovers {args.lane}: "
          + ("CLEAN (11/11 checks pass)" if not failed
             else f"NOT CLEAN ({len(failed)} of {len(results)} checks fail: {', '.join(r.name for r in failed)})"))
    return EXIT_OK if not failed else EXIT_LEFTOVER


if __name__ == "__main__":
    sys.exit(main())
