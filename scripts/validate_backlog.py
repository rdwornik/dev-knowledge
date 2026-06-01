#!/usr/bin/env python
"""Read-only narrow schema validator for BACKLOG.md (ADR-64 / ADR-65).

Layer-2 invariant: reads BACKLOG.md only; never writes, never orchestrates.

Hard-fail (exit 1) — objective schema violations only:
  - a ``status:`` word outside ``open | in-progress | blocked | done``
  - any ``done`` entry present (done items must leave the file — ADR-65)
  - an entry missing its ``id:`` field, or a duplicate ``id:``
  - section<->status disagreement for the status sections
    (``## Now``->in-progress, ``## Blocked``->blocked, ``## Open``->open)

(Monotonic / never-reused ``id`` is an *assignment* discipline — removals leave
gaps and ids are not in file order — so only uniqueness is enforced statically.)

Warn-only (never blocks) — subjective signals:
  - ``## Now`` has more than 5 items
  - a ``## Now`` item older than 30 days (stale)
  - ``## Coordination`` has more than 10 items

``## Coordination`` is the documented status-agnostic carveout: its entries are
checked for a valid, non-``done`` status but are exempt from section<->status.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

VALID_STATUS = {"open", "in-progress", "blocked", "done"}
SECTION_STATUS = {"Now": "in-progress", "Blocked": "blocked", "Open": "open"}
STALE_DAYS = 30

BACKLOG = Path(__file__).resolve().parent.parent / "BACKLOG.md"

_SECTION_RE = re.compile(r"^## (Now|Open|Blocked|Coordination)\b")
_ENTRY_RE = re.compile(r"^### \[P\d\]")
_FIELD_RE = re.compile(r"^- \*\*(id|repo|status):\*\*\s*(.+?)\s*$")
_ADDED_RE = re.compile(r"^- \*\*Added:\*\*\s*(\d{4}-\d{2}-\d{2})")


def parse(text):
    """Return a list of entry dicts: section, title, line, id, repo, status, added."""
    entries = []
    section = None
    cur = None
    for lineno, raw in enumerate(text.splitlines(), 1):
        sec = _SECTION_RE.match(raw)
        if sec:
            section = sec.group(1)
            continue
        if _ENTRY_RE.match(raw):
            cur = {
                "section": section,
                "title": raw.strip(),
                "line": lineno,
                "id": None,
                "repo": None,
                "status": None,
                "added": None,
            }
            entries.append(cur)
            continue
        if cur is not None:
            field = _FIELD_RE.match(raw)
            if field:
                cur[field.group(1)] = field.group(2).strip()
                continue
            added = _ADDED_RE.match(raw)
            if added:
                cur["added"] = added.group(1)
    return entries


def validate(entries):
    """Return (hard_fails, warnings)."""
    hard, warn = [], []
    now = [e for e in entries if e["section"] == "Now"]
    coord = [e for e in entries if e["section"] == "Coordination"]

    for e in entries:
        tag = f'id={e["id"]} "{e["title"][:48]}" (line {e["line"]})'
        status = (e["status"] or "").strip()
        if not (e["id"] and e["id"].isdigit()):
            hard.append(f'missing/invalid id: "{e["title"][:48]}" (line {e["line"]})')
        if status not in VALID_STATUS:
            hard.append(f'invalid status {status!r} — {tag}')
        elif status == "done":
            hard.append(f'done item present (done items leave the file, ADR-65) — {tag}')
        want = SECTION_STATUS.get(e["section"])
        if want and status in VALID_STATUS and status != "done" and status != want:
            hard.append(f'section/status mismatch: ## {e["section"]} requires status:{want}, got {status!r} — {tag}')

    # id uniqueness (hard-fail). NOT enforced: file-order / contiguous monotonicity —
    # ids are assigned monotonically and never reused, so removals leave gaps and a new
    # id can sit above earlier ones in a different section; a contiguous/order check would
    # be wrong by design. Monotonic *assignment* is a discipline, not a static file invariant
    # (would need a last-issued watermark to verify). Uniqueness is the checkable invariant.
    seen = {}
    for e in entries:
        eid = e["id"]
        if eid and eid.isdigit():
            if eid in seen:
                hard.append(f'duplicate id {eid}: lines {seen[eid]} and {e["line"]}')
            else:
                seen[eid] = e["line"]

    if len(now) > 5:
        warn.append(f'## Now has {len(now)} items (>5)')
    if len(coord) > 10:
        warn.append(f'## Coordination has {len(coord)} items (>10 — pending child-repo relocations?)')
    today = date.today()
    for e in now:
        if e["added"]:
            try:
                age = (today - date.fromisoformat(e["added"])).days
            except ValueError:
                continue
            if age > STALE_DAYS:
                warn.append(f'## Now item stale ({age}d): "{e["title"][:48]}"')
    return hard, warn


def main():
    if not BACKLOG.exists():
        print(f"validate_backlog: {BACKLOG} not found", file=sys.stderr)
        return 1
    entries = parse(BACKLOG.read_text(encoding="utf-8"))
    hard, warn = validate(entries)
    for w in warn:
        print(f"WARN  {w}")
    for h in hard:
        print(f"FAIL  {h}")
    if hard:
        print(f"validate_backlog: {len(hard)} hard-fail(s), {len(warn)} warning(s)")
        return 1
    print(f"validate_backlog: OK ({len(entries)} entries, {len(warn)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
