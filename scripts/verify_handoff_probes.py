#!/usr/bin/env python
"""verify_handoff_probes.py — #163 read-only handoff-probe TEETH validator.

STUB (steps 1–2 / #163): the parser (this step) is live; the §10 classifier
(`verify`) lands in step 3. The §10 ladder this validator mechanizes is documented
on `verify` once implemented.

Parser contract (step 2):
  - `split_row` splits a markdown table row on `|` but NOT on a `|` inside a backtick
    code span (the named failure mode: `git log | grep` is ONE cell, not two).
  - columns are mapped by HEADER NAME, never fixed position — live PROBES.md tables
    carry a leading `#` id column that §5's 4-col spec example omits, so a positional
    parser mis-reads every field.
  - a table is a probe table iff its header has all four load-bearing columns
    (question / binds-to / why / verifies-via); other tables are skipped.

Read-only (Layer-2, ADR-28/36): reads PROBES.md + resolves repo paths; writes nothing.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# A repo-relative file path token: optional dir segments + a name with a known ext.
_FILE_RE = re.compile(r"(?:[\w.-]+/)*[\w-]+\.(?:py|md|ya?ml|toml|json|sh|ps1)")


@dataclass(frozen=True)
class ProbeResult:
    probe_id: str   # the table's `#` column, e.g. "P2" (or "" when absent)
    status: str     # 'pass' | 'fail' | 'anchor-missing' | 'skipped'
    detail: str     # evidence (pipe-free)
    bundle: str     # bundle dir name


# --- extractors (pure) ------------------------------------------------------

def split_row(line: str) -> list[str]:
    """Split a markdown table row into cell strings, treating `|` inside a backtick
    code span as a literal (NOT a delimiter). Leading/trailing border pipes dropped."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells: list[str] = []
    buf: list[str] = []
    in_tick = False
    for ch in s:
        if ch == "`":
            in_tick = not in_tick
            buf.append(ch)
        elif ch == "|" and not in_tick:
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def backtick_spans(text: str) -> list[str]:
    """Contents of every `...` inline code span, in order (backticks stripped)."""
    return [m.strip() for m in re.findall(r"`([^`]+)`", text)]


def first_span(text: str) -> str:
    """Contents of the FIRST backtick span (the canonical command), or "" if none.

    Command targets come from this span ALONE: a probe's verification cell may carry a
    secondary span (e.g. `audit.py health`, a root-relative shorthand that does not
    exist as a path) — resolving those would false-FAIL. Source-locators, by contrast,
    use ALL spans (the file often sits in the 2nd span: `ALL_CHECKS` in `scripts/audit.py`).
    """
    m = re.search(r"`([^`]+)`", text)
    return m.group(1).strip() if m else ""


def file_tokens(text: str) -> list[str]:
    """Repo-relative file-path tokens in `text` (precision-over-recall: only tokens
    ending in a known source/doc extension — never bare symbols or command args)."""
    return _FILE_RE.findall(text)


def header_tokens(text: str) -> list[str]:
    """Backtick spans that are markdown headers (`## …`) — the anchors to resolve."""
    return [s for s in backtick_spans(text) if s.startswith("#")]


def lead_exe(command: str) -> str:
    """The lead executable of a command string (first whitespace token), or ""."""
    command = command.strip()
    return command.split()[0] if command else ""


# --- probe-manifest table parser --------------------------------------------

def _is_table_row(line: str) -> bool:
    return line.strip().startswith("|")


def _is_separator(line: str) -> bool:
    s = line.strip()
    return bool(s) and set(s) <= set("|-: ")


def _map_columns(header: list[str]) -> dict | None:
    """Map a header row to column indices by NAME. Returns None unless all four
    load-bearing columns (question / source / why / command) are present."""
    cols: dict[str, int] = {}
    for idx, cell in enumerate(header):
        c = cell.lower()
        if "binds" in c and "source" not in cols:
            cols["source"] = idx
        elif "verif" in c and "command" not in cols:
            cols["command"] = idx
        elif "why" in c and "why" not in cols:
            cols["why"] = idx
        elif ("probe" in c or "question" in c) and "question" not in cols:
            cols["question"] = idx
        elif c.strip() == "#" and "id" not in cols:
            cols["id"] = idx
    if {"source", "command", "why", "question"} <= cols.keys():
        return cols
    return None


def _row_to_probe(cells: list[str], cols: dict) -> dict:
    def get(key: str) -> str:
        idx = cols.get(key)
        return cells[idx] if idx is not None and idx < len(cells) else ""
    return {k: get(k) for k in ("id", "question", "source", "why", "command")}


def parse_probes(md_text: str) -> list[dict]:
    """Parse every probe-table row in a PROBES.md into mapped-field dicts.

    Handles multiple tables per file (P1 orientation + P2–P7 teeth) and skips any
    non-probe table (one whose header lacks the four load-bearing columns)."""
    rows: list[dict] = []
    lines = md_text.splitlines()
    i, n = 0, len(md_text.splitlines())
    while i < n:
        if _is_table_row(lines[i]) and i + 1 < n and _is_separator(lines[i + 1]):
            cols = _map_columns(split_row(lines[i]))
            i += 2  # past header + separator
            while i < n and _is_table_row(lines[i]):
                if cols is not None:
                    rows.append(_row_to_probe(split_row(lines[i]), cols))
                i += 1
            continue
        i += 1
    return rows


# --- classifier (step 3) ----------------------------------------------------

def _exe_available(name: str) -> bool:
    raise NotImplementedError


def verify(bundle_path, repo_root=None) -> list[ProbeResult]:
    raise NotImplementedError


def format_findings(results: list[ProbeResult]) -> str:
    raise NotImplementedError


def main(argv=None) -> int:
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
