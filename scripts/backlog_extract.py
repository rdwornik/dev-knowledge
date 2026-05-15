"""
backlog_extract.py — Extract [done]/[abandoned] entries from BACKLOG.md to BACKLOG_ARCHIVE.md.

Per ADR-47: deterministic, stdlib-only, no LLM, target < 50 LOC.

Usage:
    python scripts/backlog_extract.py --repo <path>
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

_DONE_HEADING = re.compile(r"^### \[P\d+\] \[(done|abandoned)\] ")
_SECTION_BREAK = re.compile(r"^(## |### )")


def extract(repo_path: Path, today: date | None = None) -> int:
    backlog = repo_path / "BACKLOG.md"
    archive = repo_path / "BACKLOG_ARCHIVE.md"
    if not backlog.exists():
        return 0
    today = today or date.today()
    lines = backlog.read_text(encoding="utf-8").splitlines(keepends=True)

    keep: list[str] = []
    done_blocks: list[str] = []
    current_done: list[str] | None = None

    for line in lines:
        if _DONE_HEADING.match(line):
            if current_done is not None:
                done_blocks.append("".join(current_done) + f"- **Archived:** {today.isoformat()}\n\n")
            current_done = [line]
        elif current_done is not None and _SECTION_BREAK.match(line):
            done_blocks.append("".join(current_done) + f"- **Archived:** {today.isoformat()}\n\n")
            current_done = None
            keep.append(line)
        elif current_done is not None:
            current_done.append(line)
        else:
            keep.append(line)

    if current_done is not None:
        done_blocks.append("".join(current_done) + f"- **Archived:** {today.isoformat()}\n\n")

    if not done_blocks:
        return 0

    with open(archive, "a", encoding="utf-8") as fh:
        fh.writelines(done_blocks)
    backlog.write_text("".join(keep), encoding="utf-8")
    return len(done_blocks)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()
    moved = extract(Path(args.repo))
    print(f"Extracted {moved} done/abandoned entries to BACKLOG_ARCHIVE.md")
    sys.exit(0)
