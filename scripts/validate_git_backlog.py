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

Two precision levers (precision-over-recall: one false positive kills adoption):
  1. `--first-parent` — scan only the MAIN-LINE history (the `--no-ff` merge spine,
     core-invariants rule 5), where real closures are declared at ship time; excludes
     branch-internal commits.
  2. strip inline-code/fenced spans before matching — a real closure is plain text
     (`feat: …, closes [#57]`, CONTRIBUTING.md); backtick-quoted `closes [#N]` is PROSE
     about the convention (constant in this methodology repo) and must not count. This
     lever is topology-independent: it holds even when the prose rides a main-line merge.
Two field-runs on this repo proved both: a full-history run flagged #5 (a test-fixture
body, FP) + #77 (a real merge `closes [#77]` never removed — genuine ADR-65 drift);
`--first-parent` dropped #5 but a later run showed an own-commit body quoting the
convention re-introduced #5 on the linear branch → code-stripping closed that. Result:
only #77 (the real, bare declaration in merge 77e5d7d) survives.

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

import re
import sys
from pathlib import Path

# Dual import: `scripts.propose_closures` for `python -m scripts.…`; `propose_closures`
# for `python scripts/validate_git_backlog.py` and the test path (scripts/ on sys.path).
try:
    from scripts.propose_closures import (
        Commit,
        find_strong,
        git_head,
        git_log_commits,
        open_tasks_from_backlog,
        _load_validate_backlog,
    )
except ImportError:
    from propose_closures import (
        Commit,
        find_strong,
        git_head,
        git_log_commits,
        open_tasks_from_backlog,
        _load_validate_backlog,
    )

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_BACKLOG = _REPO_ROOT / "BACKLOG.md"

# Inline-code / fenced spans hold `closes [#N]` as PROSE about the convention (this is
# a methodology repo — commits routinely quote the token), never a real declaration.
# A real closure is plain text per CONTRIBUTING.md (`feat: …, closes [#57]`). Stripping
# these spans before matching is the topology-independent precision lever (complements
# --first-parent): it kills prose false positives even when they ride a main-line merge.
_FENCE_RE = re.compile(r"```.*?```", re.S)
_INLINE_CODE_RE = re.compile(r"`[^`]*`")


def _strip_code(text: str) -> str:
    """Blank out fenced + inline-code spans so backtick-quoted `closes [#N]` prose
    (example/explanatory text) is not mistaken for a real closure declaration."""
    return _INLINE_CODE_RE.sub(" ", _FENCE_RE.sub(" ", text or ""))


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
    # branch-internal `closes` text. No baseline (still-present guard).
    raw = git_log_commits(Path(repo_root), "HEAD", first_parent=True)
    # strip inline-code/fenced spans so backtick-quoted `closes [#N]` prose (this repo
    # discusses the convention constantly) is not read as a declaration.
    commits = [Commit(c.sha, _strip_code(c.subject), _strip_code(c.body), c.files)
               for c in raw]
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
