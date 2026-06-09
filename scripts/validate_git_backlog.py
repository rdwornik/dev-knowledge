#!/usr/bin/env python
"""validate_git_backlog.py — #90 read-only git↔backlog reconciliation verifier.

Direction (a) STRONG (ADR-65): a `closes [#id]` commit ANYWHERE in history whose
`[#id]` is STILL PRESENT (open) in BACKLOG.md is DRIFT — the closing commit fired
but the done item never left the file ("done items leave", ADR-65). This automates
the manual git-resync toil (the reference spec: commit `021532c`, 2026-06-09, which
intersected the full-history git-closed-id set against BACKLOG's active list).

Full history is safe and needs NO baseline: the still-present guard means an old
`closes [#N]` for an `[#N]` long gone from BACKLOG simply does not fire; ids are
monotonic / never-reused (CONTRIBUTING.md, PLAYBOOK §10), so there is no aliasing.

Precision lever — `--first-parent`: detection scans only the MAIN-LINE history (the
`--no-ff` merge spine, core-invariants rule 5), where real closures are declared at
ship time. This excludes branch-internal commits whose bodies carry `closes [#N]` as
FIXTURE / EXAMPLE text (e.g. a test commit describing "a real `closes [#5]` commit").
A first field-run on this repo proved the lever: full-history flagged #5 (a test-
fixture body, false positive) + #77 (a real merge `closes [#77]` whose item was never
removed — genuine ADR-65 drift); `--first-parent` kept #77 and dropped #5.

Scope — direction (a) only. The #90 spec also named direction (b) (every merged arc
maps to an item/closure/no-item-class) and a literal "advanced→present" clause; both
are DEFERRED to **#90b**:
  - "advanced→present" is a no-op — `advances [#id]` items are *supposed* to stay
    open and are invisible to the closure detector by design (CONTRIBUTING.md), so
    there is nothing to reconcile.
  - direction (b) needs arc-CONTENT inspection (`<merge>^1..<merge>^2` work commits),
    not the merge subject: `/ship` merge subjects here are never Conventional-Commits
    prefixed (`Merge <branch> — …`), so a `^(feat|fix)` subject predicate would match
    nothing in production = a vacuous pass. Deferred until redesigned.

Layer-2 / read-only contract (ADR-28/36): reads git + BACKLOG.md; writes NOTHING;
never orchestrates; never gates (awareness layer — prints, exits 0). REUSES
`propose_closures.find_strong` (the identical closes∩still-open core) and
`validate_backlog.parse` (the single backlog reader) — no parallel parser, no
re-derived detection.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Dual import: `scripts.propose_closures` for `python -m scripts.…`; `propose_closures`
# for `python scripts/validate_git_backlog.py` and the test path (scripts/ on sys.path).
try:
    from scripts.propose_closures import (
        find_strong,
        git_head,
        git_log_commits,
        open_tasks_from_backlog,
        _load_validate_backlog,
    )
except ImportError:
    from propose_closures import (
        find_strong,
        git_head,
        git_log_commits,
        open_tasks_from_backlog,
        _load_validate_backlog,
    )

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_BACKLOG = _REPO_ROOT / "BACKLOG.md"


def reconcile(repo_root: Path, backlog_path: Path) -> dict:
    """Direction (a) drift: {id: [(sha, subject), ...]} for every `closes [#id]`
    commit in full history whose `[#id]` is still open in BACKLOG.md (ADR-65).

    Pure orchestration over reused parts: parse open ids (validate_backlog.parse),
    read full history (git_log_commits over HEAD), intersect (find_strong).
    """
    vb = _load_validate_backlog()
    open_tasks = open_tasks_from_backlog(
        Path(backlog_path).read_text(encoding="utf-8", errors="replace"), vb.parse
    )
    # full history, MAIN-LINE only (--first-parent): real ship-time closures, not
    # branch-internal fixture/example `closes` text. No baseline (still-present guard).
    commits = git_log_commits(Path(repo_root), "HEAD", first_parent=True)
    return find_strong(set(open_tasks), commits)


def format_findings(drift: dict) -> str:
    """One flat line per drifted id (cheap to scan; safe in a markdown table cell)."""
    if not drift:
        return ""
    parts = []
    for cid in sorted(drift, key=int):
        shas = ", ".join(sha[:9] for sha, _ in drift[cid])
        parts.append(f"#{cid} (closes in {shas}) still in BACKLOG")
    return "; ".join(parts)


def main() -> int:
    """CLI: print direction-(a) drift, exit 0 always (awareness layer, never a gate)."""
    head = git_head(_REPO_ROOT)
    if head is None:
        print("validate_git_backlog: git unavailable or not a repo — skipped",
              file=sys.stderr)
        return 0
    drift = reconcile(_REPO_ROOT, _BACKLOG)
    if not drift:
        print("validate_git_backlog: OK — no closed-but-present drift "
              "(direction (a) STRONG, full history)")
        return 0
    print(f"validate_git_backlog: {len(drift)} closed-but-present backlog item(s) "
          "(ADR-65 done-items-leave — remove from BACKLOG, reference the id):")
    for cid in sorted(drift, key=int):
        for sha, subject in drift[cid]:
            print(f"  DRIFT  #{cid}  closed by {sha[:9]}  {subject}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
