#!/usr/bin/env python
"""validate_landing_predicate.py — [#513] propagation-completeness landing-predicate scanner.

A ruling that names an adoption or a mechanism class can land at some call sites and not
others — the standing example this row was born from: the `markdown_it` fence ADOPT reached
2 of 4 fence sites, the `yaml.safe_load` ADOPT reached 1 of 2 frontmatter readers. Fixing the
found sites repairs the INSTANCE; nothing previously owned noticing the CLASS. This module is
the detector, not the fixes.

**The `landed:` predicate shape** (row clause (a)/(d); designed reusing the register's own
`- **Expiry:**` bullet position rather than adding a second convention). A `protocols/
STANDING_RULINGS.md` register entry declares where a ruling should hold with a fenced
```landed``` block anywhere in its body, one `site:` line per location:

    ```landed
    site: scripts/audit.py | pattern: from markdown_it import MarkdownIt
    site: scripts/validate_doc_structure.py | pattern: _code_line_indices
    ```

Each `site:` line names a repo-relative path and a regex `pattern:`. A site's predicate
RESOLVES TRUE when `pattern` is found (`re.search`, `re.MULTILINE` — a leading `^` anchors to
any line, not just the file's first) in the live text of `path`; an entry whose
declared sites do not all resolve the same way is MIXED — the ruling landed somewhere and not
everywhere, which is exactly the defect class this row exists to surface. An entry with zero or
one site, or whose sites all agree, is not mixed (a single-site or fully-landed / not-yet-begun
ruling is not a propagation gap by this row's own definition). A missing or unreadable site file
is an ERROR result for that site, reported rather than silently skipped or silently counted as
either boolean.

**Fence parsing uses `markdown_it`** (the very mechanism this row is about propagating,
rather than a bespoke regex over the register file — see [#513] instance N5-03 in
`scripts/audit.py::_blank_fenced_code_blocks`, which this module's sibling fix ships).

Layer-2 / read-only (ADR-28/36): reads `protocols/STANDING_RULINGS.md` plus whatever site
files it names; writes NOTHING; never orchestrates. The audit adapter (`scripts/audit.py::
check_landing_predicate`) converts a `LandedEntry` into a Finding and is the only place that
consults `ecosystem/disposition-register.yaml` — this module has no disposition awareness by
design, so its output is the undispositioned ground truth a gate can layer exemptions on top of.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from markdown_it import MarkdownIt

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_DEFAULT_REGISTER = _REPO_ROOT / "protocols" / "STANDING_RULINGS.md"

_MD = MarkdownIt("commonmark")
_HEADING_RE = re.compile(r"^###\s+(?P<id>\S+)\s*(?:·|-)?\s*(?P<title>.*)$")
_SITE_LINE_RE = re.compile(
    r"^\s*site:\s*(?P<path>\S+)\s*\|\s*pattern:\s*(?P<pattern>.+?)\s*$"
)


@dataclass(frozen=True)
class SiteResult:
    path: str
    pattern: str
    landed: bool | None   # None = site file missing / unreadable / bad pattern


@dataclass(frozen=True)
class LandedEntry:
    ruling_id: str
    title: str
    sites: tuple[SiteResult, ...]

    @property
    def mixed(self) -> bool:
        """True iff declared sites disagree — the propagation-gap condition (clause (a))."""
        vals = {s.landed for s in self.sites if s.landed is not None}
        return len(vals) > 1

    @property
    def errors(self) -> tuple[SiteResult, ...]:
        return tuple(s for s in self.sites if s.landed is None)


def _landed_fence_blocks(text: str) -> list[tuple[int, str]]:
    """[(0-indexed start line, block content), ...] for every ```landed fenced code block,
    located via markdown_it (CommonMark-correct fence detection, not a regex over the file)."""
    out: list[tuple[int, str]] = []
    for token in _MD.parse(text):
        if token.type == "fence" and (token.info or "").strip() == "landed" and token.map:
            out.append((token.map[0], token.content))
    return out


def parse_landed_entries(text: str) -> list[tuple[str, str, list[tuple[str, str]]]]:
    """[(ruling_id, title, [(path, pattern), ...]), ...] — one tuple per ```landed block,
    associated with the nearest `### <id> ...` heading at or before the block's start line."""
    lines = text.splitlines()
    headings: list[tuple[int, str, str]] = []  # (line_no, id, title)
    for i, line in enumerate(lines):
        m = _HEADING_RE.match(line)
        if m:
            headings.append((i, m.group("id"), m.group("title").strip()))

    out: list[tuple[str, str, list[tuple[str, str]]]] = []
    for start_line, block in _landed_fence_blocks(text):
        owner = None
        for h_line, h_id, h_title in headings:
            if h_line <= start_line:
                owner = (h_id, h_title)
            else:
                break
        if owner is None:
            continue  # a ```landed block with no owning entry heading declares nothing
        sites: list[tuple[str, str]] = []
        for raw in block.splitlines():
            m = _SITE_LINE_RE.match(raw)
            if m:
                sites.append((m.group("path"), m.group("pattern")))
        if sites:
            out.append((owner[0], owner[1], sites))
    return out


def _resolve_site(repo_root: Path, path: str, pattern: str) -> bool | None:
    fp = repo_root / path
    if not fp.exists() or not fp.is_file():
        return None
    try:
        content = fp.read_text(encoding="utf-8")
        return bool(re.search(pattern, content, re.MULTILINE))
    except (OSError, re.error):
        return None


def scan(repo_root: Path, register: Path | None = None) -> list[LandedEntry]:
    """Evaluate every declared `landed:` predicate in `register` (default
    `protocols/STANDING_RULINGS.md`) against the live tree at `repo_root`. Returns one
    `LandedEntry` per declaration, in file order; [] if the register is absent (hub-only
    surface — a no-op on any other repo)."""
    reg_path = register if register is not None else (Path(repo_root) / "protocols" / "STANDING_RULINGS.md")
    if not reg_path.exists():
        return []
    text = reg_path.read_text(encoding="utf-8")
    out: list[LandedEntry] = []
    for ruling_id, title, sites in parse_landed_entries(text):
        results = tuple(
            SiteResult(path, pattern, _resolve_site(Path(repo_root), path, pattern))
            for path, pattern in sites
        )
        out.append(LandedEntry(ruling_id, title, results))
    return out


def format_entry(entry: LandedEntry) -> str:
    site_desc = "; ".join(
        f"{s.path} -> {'ERROR' if s.landed is None else s.landed}" for s in entry.sites
    )
    return f"{entry.ruling_id} ({entry.title}): {site_desc}"


def main(argv: list[str] | None = None) -> int:
    entries = scan(_REPO_ROOT)
    mixed = [e for e in entries if e.mixed]
    errored = [e for e in entries if e.errors and not e.mixed]
    for e in entries:
        tag = "MIXED" if e.mixed else ("ERROR" if e.errors else "ok")
        print(f"[{tag}] {format_entry(e)}")
    if mixed or errored:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
