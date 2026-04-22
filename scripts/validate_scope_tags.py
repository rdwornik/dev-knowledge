"""
validate_scope_tags.py — Pre-commit hook for ADR-27 scope tag enforcement.

Validates that all Markdown section headers in in-scope files are annotated
with a <!-- scope: X --> HTML comment within 3 lines of the header. Governed
by ADR-27 (docs/decisions/ADR-27_council-27-scope-tagging.md).

Vocabulary: dev | llm | hybrid | runtime | meta
LESSONS.md exception: file-level tag under H1 satisfies the requirement (ADR-29).

Usage (pre-commit invokes automatically):
    python scripts/validate_scope_tags.py [files...]

Exit codes:
    0 — all in-scope staged files pass validation
    1 — one or more violations found
"""

from __future__ import annotations

import logging
import os
import re
import sys
from dataclasses import dataclass

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("validate_scope_tags")

VOCABULARY = {"dev", "llm", "hybrid", "runtime", "meta"}
HYBRID_CEILING = 0.25

IN_SCOPE_FILES = {
    "CLAUDE.md",
    "README.md",
    "PLAYBOOK.md",
    "ESSENTIALS.md",
    "SESSION_SETUP.md",
    "HANDOFF_PROCESS.md",
    "LESSONS.md",
    "ENVIRONMENT.md",
}

SKIP_PATTERNS = [
    "CHANGELOG.md",
    "TOKEN-LOG.md",
    "docs/decisions/",
    "docs/audits/",
    "docs/handoffs/",
    "templates/",
    ".claude/",
]

TAG_RE = re.compile(r"^<!--\s*scope:\s*(\w+)\s*-->$")
H1_RE = re.compile(r"^#\s+")
H2_RE = re.compile(r"^#{2,3}\s+")


@dataclass
class Violation:
    file: str
    line: int
    kind: str
    detail: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: {self.detail}"


def is_in_scope(path: str) -> bool:
    basename = os.path.basename(path)
    if basename not in IN_SCOPE_FILES:
        return False
    norm = path.replace("\\", "/")
    for pattern in SKIP_PATTERNS:
        if pattern in norm:
            return False
    return True


def _find_tag_in_window(lines: list[str], start: int) -> tuple[str | None, int | None]:
    """Search up to 3 non-blank lines after `start` for a scope tag."""
    checked = 0
    i = start
    while i < len(lines) and checked < 3:
        line = lines[i].strip()
        if line:
            m = TAG_RE.match(line)
            if m:
                return m.group(1), i + 1  # 1-indexed line number
            checked += 1
        i += 1
    return None, None


def parse_file(path: str) -> tuple[list[Violation], dict[str, int]]:
    violations: list[Violation] = []
    tag_counts: dict[str, int] = {v: 0 for v in VOCABULARY}

    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    # Strip newlines for easier processing but keep 1-indexed for reporting
    stripped = [l.rstrip("\n") for l in lines]

    # Detect file-level tag: scope comment within 3 lines of the first H1
    file_level_tag: str | None = None
    for i, line in enumerate(stripped):
        if H1_RE.match(line):
            tag_val, _ = _find_tag_in_window(stripped, i + 1)
            if tag_val:
                if tag_val in VOCABULARY:
                    file_level_tag = tag_val
                else:
                    violations.append(Violation(
                        file=path,
                        line=i + 2,
                        kind="invalid_tag",
                        detail=f"invalid file-level tag '{tag_val}' (allowed: {', '.join(sorted(VOCABULARY))})",
                    ))
            break  # only check first H1

    if file_level_tag is not None:
        # File-level tag satisfies all sections — count it and return
        tag_counts[file_level_tag] += 1
        return violations, tag_counts

    # Per-section tag validation; skip headers inside fenced code blocks
    in_fence = False
    for i, line in enumerate(stripped):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if H2_RE.match(line):
            tag_val, tag_lineno = _find_tag_in_window(stripped, i + 1)
            if tag_val is None:
                violations.append(Violation(
                    file=path,
                    line=i + 1,
                    kind="missing_tag",
                    detail=f"missing scope tag after '{line.strip()}'",
                ))
            elif tag_val not in VOCABULARY:
                violations.append(Violation(
                    file=path,
                    line=tag_lineno or (i + 2),
                    kind="invalid_tag",
                    detail=f"invalid tag '{tag_val}' (allowed: {', '.join(sorted(VOCABULARY))})",
                ))
            else:
                tag_counts[tag_val] += 1

    return violations, tag_counts


def main(paths: list[str]) -> int:
    all_violations: list[Violation] = []
    total_tags: dict[str, int] = {v: 0 for v in VOCABULARY}

    for path in paths:
        if not is_in_scope(path):
            continue
        if not os.path.isfile(path):
            continue
        violations, tag_counts = parse_file(path)
        all_violations.extend(violations)
        for k, v in tag_counts.items():
            total_tags[k] += v

    for v in all_violations:
        logger.error(str(v))

    total_sections = sum(total_tags.values())
    hybrid_count = total_tags.get("hybrid", 0)
    hybrid_ratio = hybrid_count / total_sections if total_sections > 0 else 0.0
    hybrid_pct = f"{hybrid_ratio:.0%}"

    ceiling_note = ""
    if hybrid_ratio > HYBRID_CEILING:
        ceiling_note = f" *** EXCEEDS {HYBRID_CEILING:.0%} ceiling — hygiene pass needed ***"

    violation_count = len(all_violations)
    file_count = len({v.file for v in all_violations})
    if violation_count:
        summary = f"Summary: {violation_count} violation(s) across {file_count} file(s). Hybrid ratio: {hybrid_pct} (info only, threshold {HYBRID_CEILING:.0%}).{ceiling_note}"
    else:
        summary = f"Summary: all files pass. Hybrid ratio: {hybrid_pct} (info only, threshold {HYBRID_CEILING:.0%}).{ceiling_note}"

    print(summary)
    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
