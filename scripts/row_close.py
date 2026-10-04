#!/usr/bin/env python
"""row_close.py -- the integrator's row-close step (batch B2-W1, lane W1-1; R55, seat ruling 3).

WHAT THIS CLOSES. FOUNDATION merged 10 lanes and closed 0 of 11 rows with evidence: ruling (h)
rightly bars a lane from closing its own row, and nothing else closed it. This step is the
"something else". After `merge_receipt.py close` for a lane, the INTEGRATOR runs

    row_close.py close --contract <lane contract> --slug <receipt slug> --ci-run <id> --test <node id> ...

and every row the contract's `**Rows:** closes -- [#id] ...` clause names flips to CLOSED with
the merge sha, the CI run id and the tests named in the evidence clause. A `related` id is never
touched.

EVIDENCE IS VERIFIED, NOT TYPED (R59). The merge sha is READ from the closed merge receipt
(`logs/MERGE-RECEIPTS.jsonl`) -- there is no flag that accepts one. Then, each unreadable or
failing check is a refusal (exit 1) that leaves every row file and the manifest byte-identical:
  * the sha resolves to a commit and is reachable from the main ref (default `origin/main`);
  * the CI run is a `push` run whose `headSha` equals the merge sha, `status` is completed and
    `conclusion` is `success` or `failure`. A `failure` is recorded in the clause, not refused:
    a red present on both sides of a merge is FLAGGED by the receipt's verdict, never refused
    (common rules section 3) -- this step records which run it read. `cancelled`, `timed_out`,
    `skipped`, in-progress, a `schedule` run, another sha, an unreadable `gh`: all refused;
  * every named test is a node id whose file exists at the merge sha and whose class and
    function names are defined in it.

A LANE CANNOT CLOSE ITS OWN ROW. The step refuses when run from inside the lane's own worktree
(`.claude/worktrees/<slug>` or branch `worktree-<slug>`), when the caller's session (the first 8
characters of `$CLAUDE_CODE_SESSION_ID`, the convention `claim.py` writes) equals the implementing
session (the suffix of `to-cc/<contract stem>.CLAIMED-*`, the only source -- there is no flag that
names it), and when either is unknown, no marker included: a caller that cannot prove it is not the
lane is refused. Limit, stated: the caller's session is `$CLAUDE_CODE_SESSION_ID`, which a process
that controls its own environment can set; the claim marker is the trusted half.

ALL ROWS OR NONE. Every named row is planned against the untouched tree first; one that is not
open refuses the whole batch. The writes then go through `gen_task_tree._cmd_close_row` -- the
ONE row writer -- and a failure part-way restores every file touched.

Prior-art check (library-first): the row writer, its evidence clause and its refusal grammar are
`gen_task_tree.close_row_plan` / `_cmd_close_row` ([#730]) -- reused, not duplicated. The receipt
reader is `merge_receipt.read_ledger`. Everything else is stdlib (`subprocess` for `git` and
`gh`, `re`, `json`). No new dependency.

HONEST LIMITS. `gen_task_tree._cmd_close_row` leaves `BACKLOG.md` alone; the integrator regenerates
it (`gen_task_tree.py --emit-source`) on the merged tree. The step reads the CI run's workflow
conclusion, not each test's own result -- the per-leg verdict stays the merge receipt's. Folding
this call inside `merge_receipt.py close` is not this wave's (that file is lane W1-2's).

EXIT CODES: 0 closed (or the contract closes no row) | 1 refusal, nothing written | 2 internal
error.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Sequence

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

# The dual package/script import shim (see `lane_cost.py`): both entry points are supported.
try:  # pragma: no cover -- exercised by whichever path the caller uses
    from scripts import gen_task_tree as gtt
    from scripts import merge_receipt as mr
except ImportError:  # pragma: no cover
    import gen_task_tree as gtt
    import merge_receipt as mr

CLOSED = 0
REFUSED = 1
INTERNAL_ERROR = 2

#: CI conclusions that are evidence of a completed run. `failure` is admitted and recorded (see
#: the module docstring); every other conclusion -- cancelled, timed_out, skipped, none -- is not.
_ACCEPTED_CONCLUSIONS = ("success", "failure")
_ROWS_LINE_RE = re.compile(r"^\*\*Rows:\*\*(?P<rest>.*)$", re.MULTILINE)
_ROW_ID_RE = re.compile(r"\[#(\d+)\]")
_RELATED_OPEN_RE = re.compile(r"^\s*related\b", re.IGNORECASE)
#: The clause must open with `closes` and a dash or colon; ids anywhere else are not closable.
_CLOSES_OPEN_RE = re.compile(r"^\s*closes\s*(?:—|--|-|:)")
_SESSION_PREFIX = 8


class RowCloseRefusal(Exception):
    """A refusal: the evidence or the caller does not support a close. Nothing was written."""


GhRunner = Callable[[str], dict]


@dataclass(frozen=True)
class ParsedRows:
    closes: tuple[int, ...]
    related: tuple[int, ...]
    refusal: Optional[str] = None


def parse_rows_line(contract_text: str) -> ParsedRows:
    """Read a lane contract's `**Rows:**` line. Only the `closes` clause yields closable ids; a
    contract with no such line yields no ids and an explicit refusal."""
    match = _ROWS_LINE_RE.search(contract_text)
    if match is None:
        return ParsedRows((), (), "the contract has no **Rows:** line -- nothing names a row")
    rest = match.group("rest")
    if _CLOSES_OPEN_RE.match(rest) is None:
        return ParsedRows((), (), "the **Rows:** line does not open with `closes —` -- no id "
                                  "is closable from it")
    head, semicolon, tail = rest.partition(";")
    if semicolon and tail.strip() and not _RELATED_OPEN_RE.match(tail):
        return ParsedRows((), (), "the **Rows:** line has text after the closes clause that is "
                                  "not a `related` clause -- no id is closable from it")
    closes = tuple(int(i) for i in _ROW_ID_RE.findall(head))
    related = tuple(int(i) for i in _ROW_ID_RE.findall(tail))
    return ParsedRows(closes, related)


def _session_key(session: Optional[str]) -> Optional[str]:
    session = (session or "").strip()
    return session[:_SESSION_PREFIX] if session else None


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo_root), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=60)


def check_caller_is_not_the_lane(slug: str, cwd: Path, caller_session: Optional[str],
                                 lane_session: Optional[str]) -> None:
    """Item 5: only the integrator path closes. Raises RowCloseRefusal."""
    parts = [p.lower() for p in Path(cwd).resolve().parts]
    for i in range(len(parts) - 2):
        if parts[i:i + 3] == [".claude", "worktrees", slug.lower()]:
            raise RowCloseRefusal(
                f"refused: running from inside the lane's own worktree ({cwd}) -- a lane "
                f"cannot close its own row; the integrator runs this from the primary checkout")
    try:
        branch = _git(Path(cwd), "branch", "--show-current").stdout.strip()
    except (OSError, subprocess.SubprocessError):
        branch = ""
    if branch == f"worktree-{slug}":
        raise RowCloseRefusal(
            f"refused: the checkout is on the lane's own branch {branch} -- a lane cannot "
            f"close its own row")
    caller, lane = _session_key(caller_session), _session_key(lane_session)
    if caller is None:
        raise RowCloseRefusal(
            "refused: the caller's session is unknown ($CLAUDE_CODE_SESSION_ID is empty) -- a "
            "caller that cannot prove it is not the implementing lane does not close")
    if lane is None:
        raise RowCloseRefusal(
            "refused: the implementing session is unknown (pass --lane-session, or keep the "
            "contract's claim marker) -- cannot prove the caller is not the lane")
    if caller == lane:
        raise RowCloseRefusal(
            f"refused: the caller's session {caller} is the implementing session -- a lane "
            f"cannot close its own row")


def merge_sha_from_receipt(repo_root: Path, slug: str) -> str:
    """The merge sha of the newest CLOSED merge receipt for `slug`. Raises RowCloseRefusal."""
    rows = [r for r in mr.read_ledger(repo_root)
            if r.slug == slug and r.kind == mr.KIND_MERGE]
    if not rows:
        raise RowCloseRefusal(f"refused: no merge receipt for {slug!r} in {mr.LEDGER_RELPATH}")
    receipt = rows[-1]
    if not receipt.closed:
        raise RowCloseRefusal(f"refused: the receipt for {slug!r} is not closed")
    if not receipt.merge_sha:
        raise RowCloseRefusal(f"refused: the receipt for {slug!r} names no merge sha")
    return receipt.merge_sha


def verify_merge_sha(repo_root: Path, merge_sha: str, main_ref: str) -> str:
    """Resolve to the full sha and prove it is reachable from `main_ref`."""
    try:
        resolved = _git(repo_root, "rev-parse", "--verify", f"{merge_sha}^{{commit}}")
    except (OSError, subprocess.SubprocessError) as exc:
        raise RowCloseRefusal(f"refused: git is unreadable ({exc})") from exc
    if resolved.returncode != 0:
        raise RowCloseRefusal(f"refused: merge sha {merge_sha} does not resolve to a commit")
    full = resolved.stdout.strip()
    reach = _git(repo_root, "merge-base", "--is-ancestor", full, main_ref)
    if reach.returncode == 1:
        raise RowCloseRefusal(f"refused: merge sha {full} is not reachable from {main_ref}")
    if reach.returncode != 0:
        raise RowCloseRefusal(f"refused: cannot test {full} against {main_ref}: "
                              f"{reach.stderr.strip()}")
    return full


def _default_gh(repo_root: Path) -> GhRunner:
    def run(run_id: str) -> dict:
        done = subprocess.run(
            ["gh", "run", "view", run_id, "--json", "headSha,event,status,conclusion"],
            cwd=str(repo_root), capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=60)
        if done.returncode != 0:
            raise RuntimeError(f"gh run view exited {done.returncode}: {done.stderr.strip()}")
        return json.loads(done.stdout)
    return run


def verify_ci_run(ci_run: Optional[str], merge_sha: str, gh: GhRunner) -> str:
    """The run is a completed `push` run of the merge sha. Returns its conclusion."""
    if not ci_run or not re.fullmatch(r"[0-9]+", ci_run):
        raise RowCloseRefusal(f"refused: --ci-run {ci_run!r} is not a numeric run id")
    try:
        info = gh(ci_run)
        head, event = info["headSha"], info["event"]
        status, conclusion = info["status"], info.get("conclusion")
    except Exception as exc:  # unreadable gh / network / shape -- a refusal, never a close
        raise RowCloseRefusal(f"refused: CI run {ci_run} is unreadable ({exc!r})") from exc
    if head != merge_sha:
        raise RowCloseRefusal(
            f"refused: CI run {ci_run} ran {head}, not the merge sha {merge_sha}")
    if event != "push":
        raise RowCloseRefusal(f"refused: CI run {ci_run} is a {event!r} run, not a push run")
    if status != "completed":
        raise RowCloseRefusal(f"refused: CI run {ci_run} is {status!r}, not completed")
    if conclusion not in _ACCEPTED_CONCLUSIONS:
        raise RowCloseRefusal(f"refused: CI run {ci_run} concluded {conclusion!r}")
    return conclusion


def verify_tests(repo_root: Path, merge_sha: str, tests: Sequence[str]) -> None:
    """Every named node id exists at the merge sha: the file, the exact class nesting and the
    function, parsed with `ast` rather than searched for as text. A `[param]` selector is admitted
    only on a parametrized function -- the parameter value itself is not collected here."""
    if not tests:
        raise RowCloseRefusal("refused: no test named (--test) -- a close needs the tests")
    for node_id in tests:
        path, *names = node_id.split("::")
        if not path.endswith(".py") or ".." in path.split("/") or not names:
            raise RowCloseRefusal(f"refused: {node_id!r} is not a test node id (file.py::name)")
        shown = _git(repo_root, "show", f"{merge_sha}:{path}")
        if shown.returncode != 0:
            raise RowCloseRefusal(f"refused: {path} does not exist at {merge_sha}")
        try:
            tree = ast.parse(shown.stdout)
        except SyntaxError as exc:
            raise RowCloseRefusal(f"refused: {path} at {merge_sha} does not parse ({exc})") from exc
        if "[" in names[-1]:
            raise RowCloseRefusal(
                f"refused: {node_id!r}: a parameter selector cannot be proven without collecting "
                f"the test -- name the function, not a case")
        if _defined_at(tree.body, names) is None:
            raise RowCloseRefusal(f"refused: {node_id!r}: {'::'.join(names)} is not defined in "
                                  f"{path} at {merge_sha} (exact class nesting)")


def _defined_at(body: list, names: list[str]) -> Optional[ast.AST]:
    """The def reached by walking `names` through DIRECT class nesting, else None."""
    node = None
    for index, name in enumerate(names):
        kinds = ((ast.FunctionDef, ast.AsyncFunctionDef) if index == len(names) - 1
                 else (ast.ClassDef,))
        node = next((n for n in body if isinstance(n, kinds) and n.name == name), None)
        if node is None:
            return None
        body = node.body
    return node


def close_for_merge(repo_root: Path, *, contract_text: str, slug: str, ci_run: Optional[str],
                    tests: Sequence[str], caller_session: Optional[str],
                    lane_session: Optional[str], cwd: Path, gh: Optional[GhRunner] = None,
                    main_ref: str = "origin/main", tasks_dir: Optional[Path] = None
                    ) -> list[int]:
    """Verify the evidence, then close every row the contract names. Returns the closed ids.

    Raises RowCloseRefusal with nothing written."""
    repo_root = Path(repo_root)
    parsed = parse_rows_line(contract_text)
    if parsed.refusal:
        raise RowCloseRefusal(f"refused: {parsed.refusal}")
    check_caller_is_not_the_lane(slug, Path(cwd), caller_session, lane_session)
    if not parsed.closes:
        return []
    out_dir = Path(tasks_dir) if tasks_dir else repo_root / "tasks"

    merge_sha = verify_merge_sha(repo_root, merge_sha_from_receipt(repo_root, slug), main_ref)
    conclusion = verify_ci_run(ci_run, merge_sha, gh or _default_gh(repo_root))
    verify_tests(repo_root, merge_sha, tests)

    # Every row against the untouched tree first: one not open refuses the whole batch.
    for task_id in parsed.closes:
        try:
            gtt.close_row_plan(out_dir, task_id, merge_sha, "1970-01-01", ci_run, conclusion,
                               tuple(tests))
        except (OSError, ValueError, KeyError, UnicodeDecodeError) as exc:
            raise RowCloseRefusal(f"refused: [#{task_id}]: {exc}") from exc

    touched = [out_dir / "manifest.json"]
    manifest = json.loads(touched[0].read_bytes().decode("utf-8"))
    touched += [out_dir / n["file"] for n in manifest["nodes"]
                if n.get("task") in parsed.closes]
    snapshot = {p: p.read_bytes() for p in touched if p.exists()}
    closed: list[int] = []
    try:
        for task_id in parsed.closes:
            code = gtt._cmd_close_row(out_dir, task_id, merge_sha, ci_run, conclusion,
                                      tuple(tests))
            if code != 0:
                raise RowCloseRefusal(f"refused: [#{task_id}] could not be written")
            closed.append(task_id)
    except BaseException:
        for path, original in snapshot.items():
            path.write_bytes(original)
        raise
    return closed


def _lane_session_from_marker(contract: Path) -> Optional[str]:
    """The suffix of `to-cc/<contract stem>.CLAIMED-*` -- the implementing session."""
    root = os.environ.get("CLAUDE_PROMPTS_DIR", "").strip()
    if not root:
        return None
    found = sorted((Path(root) / "to-cc").glob(f"{contract.stem}.CLAIMED-*"))
    return found[0].name.split(".CLAIMED-", 1)[1] if len(found) == 1 else None


def main(argv: Optional[Sequence[str]] = None, *, gh: Optional[GhRunner] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    close = sub.add_parser("close", help="close the rows a merged lane's contract names")
    close.add_argument("--repo-root", type=Path, default=Path.cwd())
    close.add_argument("--contract", type=Path, required=True, help="the lane contract file")
    close.add_argument("--slug", required=True, help="the lane slug = its merge receipt's slug")
    close.add_argument("--ci-run", default=None, help="the CI push run id of the merge sha")
    close.add_argument("--test", action="append", default=[], dest="tests",
                       help="a test node id, repeatable")
    close.add_argument("--main-ref", default="origin/main")
    args = parser.parse_args(argv)

    try:
        text = args.contract.read_text(encoding="utf-8")
        # The implementing session comes from the contract's claim marker ALONE: no flag can
        # name it, so a lane cannot pass a session that is not its own.
        lane_session = _lane_session_from_marker(args.contract)
        closed = close_for_merge(
            args.repo_root, contract_text=text, slug=args.slug, ci_run=args.ci_run,
            tests=args.tests, caller_session=os.environ.get("CLAUDE_CODE_SESSION_ID"),
            lane_session=lane_session, cwd=Path.cwd(), gh=gh, main_ref=args.main_ref)
    except RowCloseRefusal as exc:
        print(f"row_close: {exc}", file=sys.stderr)
        return REFUSED
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"row_close: internal error: {exc!r}", file=sys.stderr)
        return INTERNAL_ERROR
    print(f"row_close: closed {', '.join(f'[#{i}]' for i in closed) or 'no row'} for {args.slug}. "
          f"Run gen_task_tree.py --emit-source to drop them from BACKLOG.md.")
    return CLOSED


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
