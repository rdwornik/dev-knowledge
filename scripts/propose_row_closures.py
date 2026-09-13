#!/usr/bin/env python
"""propose_row_closures.py -- [#730] AX16-2/AX27-5: the WITNESS SCAN half of one-command
row closure.

WHAT THIS IS, AND WHAT IT IS NOT. [#730] (AX10-1) asks for a per-batch-close packet that
lists every row a batch's own merges WITNESSED as done -- id, Done-when verbatim, the merged
SHA, and the proving test or gate -- refusing any row it cannot cite a witness for. This
module is a single-lane, MECHANICAL instance of that vision, not the full thing: it can name
the id, the Done-when (read from the row's own file, reusing `gen_dashboard`'s [#589]
fallback) and the commit that removed the row, but it CANNOT derive which gate or test
proved the Done-when -- that is a semantic judgment this module does not attempt. The
rendered list says so explicitly, naming the cited commit for the operator to open rather
than asserting a gate it did not check.

THE WITNESS RULE. A row is witnessed when:
  1. it is still OPEN on THIS branch (tasks/manifest.json on disk, so an in-progress,
     uncommitted close_row plan is reflected too); and
  2. `compare_ref` (default: local `main`, the fleet's shared integration ref) has ALREADY
     removed it from the projected BACKLOG.md, at some commit since the merge-base.
That second leg is exactly `gen_dashboard.closed_rows_from_history`'s own detector, pointed
at an arbitrary ref instead of hardcoded HEAD -- reused rather than reimplemented (LIBRARY-
FIRST, matching gen_dashboard.py's own stated policy for this shape of parser).

AX10-1's load-bearing clause holds here too: a row `compare_ref` never touched, or whose
diff this module could not read, is never listed. No witness, no listing -- silence, not a
weaker claim.

CLOSURE STAYS PROPOSED, NEVER PERFORMED. This module writes only the rendered list; it never
calls `close_row` and never touches `tasks/` or `BACKLOG.md`. Read-only over the repo, one
write path (`--out`), matching `gen_dashboard.py`'s own "IT REPORTS, IT NEVER REPAIRS" stance.

LAYER-2 POSTURE (ADR-28/36): reads git history and the working tree; writes only its own
declared output path. Drives no state in any other repo, arms no hook.

CLI: `--out PATH` (default: the operator TRANSPORT's `to-browser/CLOSURE-LIST-<today>.md`,
`gen_handoff.transport_root()` -- the same home `gen_ledger.py`'s LEDGER already uses, not a
path inside this git tree) | `--compare-ref REF` (default: resolve `main`, the shared local
integration ref) | `--repo-root PATH`.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import importlib.util
import json
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent


def _load(name: str):
    """Load a loose top-level `scripts/` module by path (the repo's standard for this shape,
    e.g. gen_dashboard.py's own `_load` -- scripts/ is not a package, so a bare `import`
    would depend on `sys.path` accidents)."""
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(name, module)
    spec.loader.exec_module(module)
    return module


_gd = _load("gen_dashboard")
_gh = _load("gen_handoff")

DEFAULT_COMPARE_REF_CANDIDATES = ("main",)

#: The transport filename grammar (OPERATOR-INTERFACE §1): `to-browser/CLOSURE-LIST-<date>.md`,
#: on the operator's TRANSPORT (`gen_handoff.transport_root()`), not inside this git tree --
#: the same home `gen_ledger.py`'s LEDGER and `gen_handoff.py`'s own to-browser/ writes already
#: use. A file landed at `<repo_root>/to-browser/...` would be a NEW top-level directory inside
#: the repo, which ADR-101 hermetization correctly refuses; the fix is the right target, not a
#: bypass of the gate that caught it.


def default_out(generated_on: str) -> Path | None:
    """The transport home for this run's closure list, or None when no transport resolves."""
    transport = _gh.transport_root()
    return Path(transport) / "to-browser" / f"CLOSURE-LIST-{generated_on}.md" if transport \
        else None


def _resolve_ref(git: "_gd.GitReader", candidates: tuple[str, ...]) -> str | None:
    """The first candidate ref that actually resolves, or None (never crash on a fresh
    clone / detached checkout with no `main`)."""
    for ref in candidates:
        if git._run("rev-parse", "--verify", "--quiet", ref) is not None:
            return ref
    return None


def _merge_base(git: "_gd.GitReader", a: str, b: str) -> str | None:
    out = git._run("merge-base", a, b)
    return out.strip() if out else None


def open_ids_at_ref(repo_root: Path, git: "_gd.GitReader", ref: str) -> set[int]:
    """Every task id still open (manifest-referenced) at `ref`. Empty on any read failure --
    an unreadable ref witnesses nothing rather than crashing the scan.

    `ref == "HEAD"` reads the WORKING TREE off disk instead of the committed blob, so an
    in-progress (uncommitted) close_row plan is reflected in "here" immediately, not only
    after its own commit lands.
    """
    if ref == "HEAD":
        try:
            text = (repo_root / "tasks" / "manifest.json").read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            return set()
    else:
        text = git.file_at(ref, "tasks/manifest.json")
        if text is None:
            return set()
    try:
        manifest = json.loads(text)
    except ValueError:
        return set()
    nodes = manifest.get("nodes") if isinstance(manifest, dict) else None
    if not isinstance(nodes, list):
        return set()
    return {n["task"] for n in nodes if isinstance(n, dict) and "task" in n}


def _log_pairs_for_ref(
    git: "_gd.GitReader", relpath: str, since_rev: str, ref: str
) -> list[tuple[str, str, str]]:
    """Like `GitReader.log_pairs`, but walking an arbitrary `ref` instead of hardcoded HEAD --
    the one thing this module needs from git history that the reused class does not expose."""
    out = git._run("log", "--first-parent", "--format=%H|%ad|%P", "--date=short",
                    f"{since_rev}..{ref}", "--", relpath)
    if not out:
        return []
    pairs: list[tuple[str, str, str]] = []
    for line in out.splitlines():
        parts = line.split("|")
        if len(parts) != 3 or not parts[0]:
            continue
        parents = parts[2].split()
        if not parents:
            continue
        pairs.append((parts[0], parts[1], parents[0]))
    return pairs


def witnessed_closures(repo_root: Path, compare_ref: str) -> list["_gd.ClosedRow"]:
    """[#730] AX16-2/AX27-5 -- rows this branch (HEAD) still shows OPEN that `compare_ref`
    has already closed, each one witnessed by the exact commit that removed it.

    A row `compare_ref` never touched, or whose diff could not be read, is never listed --
    AX10-1's own load-bearing clause.
    """
    git = _gd.GitReader(repo_root)
    here_open = open_ids_at_ref(repo_root, git, "HEAD")
    if not here_open:
        return []
    since_ref = _merge_base(git, "HEAD", compare_ref) or compare_ref
    pairs = _log_pairs_for_ref(git, "BACKLOG.md", since_ref, compare_ref)

    rows: list[_gd.ClosedRow] = []
    seen: set[int] = set()
    for sha, when, parent in pairs:
        before = git.file_at(parent, "BACKLOG.md")
        after = git.file_at(sha, "BACKLOG.md")
        if before is None or after is None:
            continue
        try:
            gone = _gd.closed_rows_between(before, after)
        except (ValueError, AssertionError):
            continue
        for row in gone:
            if row.id in seen or row.id not in here_open:
                continue
            seen.add(row.id)
            task = _gd._rows_by_id(before)[row.id]
            gain = _gd._gain_from_task_file(git, parent, task) or row.gain
            rows.append(dataclasses.replace(row, gain=gain, closed_on=when, sha=sha[:12]))
    return rows


def render_closure_list(rows: list["_gd.ClosedRow"], compare_ref: str, generated_on: str) -> str:
    lines = [
        f"# Closure list -- {generated_on}",
        "",
        f"_Rows this branch still shows OPEN that `{compare_ref}` has already closed, each "
        f"one witnessed by the commit that removed it. A row with no witnessing commit is "
        f"never listed (AX10-1's load-bearing clause: no witness, no listing). This is a "
        f"single-lane, mechanical instance of [#730]'s larger evidenced-bulk-closure vision "
        f"-- it can name the id, the Done-when, and the closing commit, but it does NOT "
        f"verify which gate or test proved the Done-when; open the cited commit before "
        f"acting on this list. This lane does not close rows on its own authority "
        f"(`close_row`, [#730] AX16-2) -- closing the list is the operator's word._",
        "",
    ]
    if not rows:
        lines += [
            "**0 rows witnessed this run.** Nothing for the operator to close -- the "
            "mechanism ran clean against zero false positives.",
            "",
        ]
        return "\n".join(lines) + "\n"
    lines.append(f"**{len(rows)} row(s) witnessed.**")
    lines.append("")
    for row in sorted(rows, key=lambda r: r.id):
        gain = row.gain or "_(no Done-when clause on file)_"
        lines.append(
            f"- **[#{row.id}] {row.title}** -- Done when: {gain} -- merged `{row.sha}` on "
            f"{row.closed_on} (`{compare_ref}`, `git show {row.sha}`)")
    lines.append("")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="propose_row_closures",
        description="[#730] AX16-2/AX27-5 witness scan: rows this branch still shows open "
                    "that a comparison ref has already closed. Read-only over the repo; "
                    "writes only the rendered list.",
    )
    parser.add_argument("--repo-root", type=Path, default=_REPO_ROOT, dest="repo_root")
    parser.add_argument("--compare-ref", type=str, default=None, dest="compare_ref",
                        help="git ref to compare against (default: main)")
    parser.add_argument("--out", type=Path, default=None,
                        help="output path (default: the operator transport's "
                             "to-browser/CLOSURE-LIST-<today>.md)")
    args = parser.parse_args(argv)

    repo_root = args.repo_root
    git = _gd.GitReader(repo_root)
    today = _dt.date.today().isoformat()
    out_path = args.out or default_out(today)
    if out_path is None:
        print("propose_row_closures: no transport resolvable (CLAUDE_PROMPTS_DIR / "
              "~/Downloads) and no --out given; nothing written", file=sys.stderr)
        return 1

    tried = (args.compare_ref,) if args.compare_ref else DEFAULT_COMPARE_REF_CANDIDATES
    compare_ref = _resolve_ref(git, tried)
    if compare_ref is None:
        text = (
            f"# Closure list -- {today}\n\n"
            f"**Could not resolve a comparison ref** (tried: "
            f"{', '.join(tried)}). Nothing witnessed this run.\n")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8", newline="\n")
        print(f"propose_row_closures: no comparison ref resolvable; wrote {out_path}",
              file=sys.stderr)
        return 0

    rows = witnessed_closures(repo_root, compare_ref)
    text = render_closure_list(rows, compare_ref, today)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8", newline="\n")
    print(f"propose_row_closures: {len(rows)} row(s) witnessed against `{compare_ref}` "
          f"-> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
