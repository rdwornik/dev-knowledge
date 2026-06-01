#!/usr/bin/env python
"""Read-only narrow schema validator for BACKLOG.md (ADR-64 / ADR-65).

Layer-2 invariant: reads BACKLOG.md only; never writes, never orchestrates.

Terse entry shape (3 lines):

    ### [P1][M] Title
    `id:1 · repo:.dev-knowledge · status:open`
    One-line What.

Hard-fail (exit 1) — objective schema only:
  - a ``### [P\\d]`` entry header missing its ``[S|M|L]`` size band
  - an entry under an H2 not in {Now, Open, Blocked, Coordination} (or before any
    section) — a mistyped/retired heading must not let an entry dodge the rules
  - a status word outside ``open | in-progress | blocked | done``
  - any ``done`` entry present (done items leave the file — ADR-65)
  - a missing or duplicate ``id``
  - a missing ``repo``, or a non-``.dev-knowledge`` ``repo`` outside ``## Coordination``
  - section<->status disagreement: ``## Now`` in {open, in-progress};
    ``## Open`` = open; ``## Blocked`` = blocked. ``## Coordination`` is the
    status-agnostic carveout (valid non-``done`` status only; section<->status exempt).

Warn-only: ``## Now`` > 5 items; ``## Coordination`` > 10 items.

(Monotonic / never-reused ``id`` is an assignment discipline — removals leave gaps
and ids are not in file order — so only uniqueness is enforced statically.)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

VALID_STATUS = {"open", "in-progress", "blocked", "done"}
SECTION_STATUS = {"Now": {"open", "in-progress"}, "Open": {"open"}, "Blocked": {"blocked"}}
KNOWN_SECTIONS = {"Now", "Open", "Blocked", "Coordination"}
SIZES = {"S", "M", "L"}

BACKLOG = Path(__file__).resolve().parent.parent / "BACKLOG.md"

_SECTION_RE = re.compile(r"^## (.+?)\s*$")
_ENTRY_RE = re.compile(r"^### \[P(\d)\]\[([A-Za-z]+)\]\s*(.+?)\s*$")
_ENTRY_LOOSE_RE = re.compile(r"^### \[P\d\]")
_ID_RE = re.compile(r"\bid:\s*([^\s·`]+)")
_REPO_RE = re.compile(r"\brepo:\s*([^\s·`]+)")
_STATUS_RE = re.compile(r"\bstatus:\s*([A-Za-z-]+)")


def parse(text):
    """Return a list of entry dicts: section, line, priority, size, title, id, repo, status, malformed."""
    entries = []
    section = None
    cur = None
    for lineno, raw in enumerate(text.splitlines(), 1):
        sec = _SECTION_RE.match(raw)
        if sec:
            section = sec.group(1).strip()
            cur = None
            continue
        m = _ENTRY_RE.match(raw)
        if m:
            cur = {
                "section": section, "line": lineno,
                "priority": m.group(1), "size": m.group(2), "title": m.group(3).strip(),
                "id": None, "repo": None, "status": None, "malformed": False,
            }
            entries.append(cur)
            continue
        if _ENTRY_LOOSE_RE.match(raw):
            cur = {
                "section": section, "line": lineno,
                "priority": None, "size": None, "title": raw.strip(),
                "id": None, "repo": None, "status": None, "malformed": True,
            }
            entries.append(cur)
            continue
        if cur is not None and cur["id"] is None:
            idm = _ID_RE.search(raw)
            if idm:
                cur["id"] = idm.group(1)
                rm = _REPO_RE.search(raw)
                cur["repo"] = rm.group(1) if rm else None
                sm = _STATUS_RE.search(raw)
                cur["status"] = sm.group(1) if sm else None
    return entries


def validate(entries):
    """Return (hard_fails, warnings)."""
    hard, warn = [], []
    now = [e for e in entries if e["section"] == "Now"]
    coord = [e for e in entries if e["section"] == "Coordination"]
    seen = {}
    for e in entries:
        loc = f'line {e["line"]} "{e["title"][:48]}"'
        if e["malformed"]:
            hard.append(f'malformed header — missing [S|M|L] size band — {loc}')
        if e["section"] not in KNOWN_SECTIONS:
            hard.append(f'entry under unknown/no section {e["section"]!r} — {loc}')
        if e["size"] is not None and e["size"].upper() not in SIZES:
            hard.append(f'invalid size band [{e["size"]}] (want S|M|L) — {loc}')
        if not (e["id"] and e["id"].isdigit()):
            hard.append(f'missing/invalid id — {loc}')
        elif e["id"] in seen:
            hard.append(f'duplicate id {e["id"]}: lines {seen[e["id"]]} and {e["line"]}')
        else:
            seen[e["id"]] = e["line"]
        status = (e["status"] or "").strip()
        if status not in VALID_STATUS:
            hard.append(f'invalid/missing status {status!r} — {loc}')
        elif status == "done":
            hard.append(f'done entry present (done items leave the file, ADR-65) — {loc}')
        if not e["repo"]:
            hard.append(f'missing repo — {loc}')
        elif e["section"] != "Coordination" and e["repo"] != ".dev-knowledge":
            hard.append(f'repo:{e["repo"]} outside ## Coordination (only .dev-knowledge allowed there) — {loc}')
        allowed = SECTION_STATUS.get(e["section"])
        if allowed and status in VALID_STATUS and status != "done" and status not in allowed:
            hard.append(f'section/status: ## {e["section"]} allows {sorted(allowed)}, got {status!r} — {loc}')

    if len(now) > 5:
        warn.append(f'## Now has {len(now)} items (>5)')
    if len(coord) > 10:
        warn.append(f'## Coordination has {len(coord)} items (>10 — pending child-repo relocations?)')
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
