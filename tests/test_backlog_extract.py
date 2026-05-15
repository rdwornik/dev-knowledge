"""Tests for scripts/backlog_extract.py — extraction logic."""
from __future__ import annotations

import sys
import os
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import backlog_extract as be

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

GOOD_BACKLOG = """\
# BACKLOG

<!-- scope: meta -->

## Stream A: work

### [P1] [open] Open item
- **What:** Still open.
- **Why:** Reason.
- **Added:** 2026-05-15 by rob
- **Status:** open

### [P1] [done] Done item
- **What:** Completed.
- **Why:** Was needed.
- **Added:** 2026-05-01 by rob
- **Status:** done (2026-05-15 - closed)

### [P2] [open] Second open item
- **What:** Also open.
- **Why:** Another reason.
- **Added:** 2026-05-10 by rob
- **Status:** open
"""

NO_DONE_BACKLOG = """\
# BACKLOG

## Stream A: work

### [P1] [open] Open item
- **What:** Open.
- **Why:** Reason.
- **Added:** 2026-05-15 by rob
- **Status:** open
"""

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_extract_no_done_items_is_noop(tmp_path: Path) -> None:
    backlog = tmp_path / "BACKLOG.md"
    archive = tmp_path / "BACKLOG_ARCHIVE.md"
    backlog.write_text(NO_DONE_BACKLOG, encoding="utf-8")
    archive.write_text("# Archive\n", encoding="utf-8")
    original_backlog = backlog.read_text(encoding="utf-8")

    moved = be.extract(tmp_path, date(2026, 5, 15))

    assert moved == 0
    assert backlog.read_text(encoding="utf-8") == original_backlog
    assert archive.read_text(encoding="utf-8") == "# Archive\n"


def test_extract_done_item_moved_to_archive(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(GOOD_BACKLOG, encoding="utf-8")
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text("# Archive\n", encoding="utf-8")

    moved = be.extract(tmp_path, date(2026, 5, 15))

    assert moved == 1
    archive_text = (tmp_path / "BACKLOG_ARCHIVE.md").read_text(encoding="utf-8")
    assert "Done item" in archive_text
    assert "[done]" in archive_text


def test_extract_preserves_ordering_of_remaining_open_items(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(GOOD_BACKLOG, encoding="utf-8")
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text("", encoding="utf-8")

    be.extract(tmp_path, date(2026, 5, 15))

    remaining = (tmp_path / "BACKLOG.md").read_text(encoding="utf-8")
    assert "Open item" in remaining
    assert "Second open item" in remaining
    assert "Done item" not in remaining
    assert remaining.index("Open item") < remaining.index("Second open item")


def test_extract_appends_archived_line(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(GOOD_BACKLOG, encoding="utf-8")
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text("", encoding="utf-8")

    be.extract(tmp_path, date(2026, 5, 15))

    archive_text = (tmp_path / "BACKLOG_ARCHIVE.md").read_text(encoding="utf-8")
    assert "**Archived:** 2026-05-15" in archive_text


def test_extract_idempotent_second_run_does_nothing(tmp_path: Path) -> None:
    (tmp_path / "BACKLOG.md").write_text(GOOD_BACKLOG, encoding="utf-8")
    (tmp_path / "BACKLOG_ARCHIVE.md").write_text("", encoding="utf-8")

    first = be.extract(tmp_path, date(2026, 5, 15))
    backlog_after_first = (tmp_path / "BACKLOG.md").read_text(encoding="utf-8")
    second = be.extract(tmp_path, date(2026, 5, 15))

    assert first == 1
    assert second == 0
    assert (tmp_path / "BACKLOG.md").read_text(encoding="utf-8") == backlog_after_first


def test_extract_script_loc_under_50(tmp_path: Path) -> None:
    """backlog_extract.py must stay under 50 non-blank non-comment code lines per ADR-47."""
    script = Path(__file__).parent.parent / "scripts" / "backlog_extract.py"
    lines = script.read_text(encoding="utf-8").splitlines()
    stripped = [ln.strip() for ln in lines]
    # Exclude blank lines, # comments, and module docstring lines
    in_docstring = False
    code_lines = []
    for ln in stripped:
        if ln.startswith('"""'):
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue
        if not ln or ln.startswith("#"):
            continue
        code_lines.append(ln)
    assert len(code_lines) < 50, f"backlog_extract.py has {len(code_lines)} code lines (limit: 49)"
