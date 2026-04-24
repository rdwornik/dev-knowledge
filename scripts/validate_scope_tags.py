"""
validate_scope_tags.py — Pre-commit hook for ADR-27 scope tag enforcement.

Validates that all Markdown section headers in in-scope files are annotated
with a <!-- scope: X --> HTML comment within 3 lines of the header. Governed
by ADR-27 (docs/decisions/ADR-27_scope-tagging.md).

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
import subprocess
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
    "handoff-prompts/",
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
    stripped = [ln.rstrip("\n") for ln in lines]

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


def _count_tags_in_content(content: str) -> dict[str, int]:
    """Count scope tags in a text string using the same rules as parse_file (no violations)."""
    lines = [line.rstrip("\n") for line in content.splitlines()]
    counts: dict[str, int] = {v: 0 for v in VOCABULARY}
    for i, line in enumerate(lines):
        if H1_RE.match(line):
            tag_val, _ = _find_tag_in_window(lines, i + 1)
            if tag_val and tag_val in VOCABULARY:
                counts[tag_val] += 1
                return counts
            break
    in_fence = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if H2_RE.match(line):
            tag_val, _ = _find_tag_in_window(lines, i + 1)
            if tag_val and tag_val in VOCABULARY:
                counts[tag_val] += 1
    return counts


def _head_content(fname: str) -> str | None:
    """Return file content at HEAD for a bare filename, or None if not present."""
    result = subprocess.run(
        ["git", "show", f"HEAD:{fname}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout if result.returncode == 0 else None


def _ratio(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    return counts.get("hybrid", 0) / total if total > 0 else 0.0


def _enforce_ratio(staged_paths: list[str]) -> tuple[int, str, str]:
    """
    Compute repo-wide hybrid ratio at HEAD vs working tree and apply delta enforcement.

    Returns (exit_code, info_line, error_msg).
    exit_code 0 = pass, 1 = block. error_msg is empty when passing.
    """
    staged_basenames = {os.path.basename(p) for p in staged_paths}
    head_counts: dict[str, int] = {v: 0 for v in VOCABULARY}
    wt_counts: dict[str, int] = {v: 0 for v in VOCABULARY}
    any_head = False

    for fname in IN_SCOPE_FILES:
        head_text = _head_content(fname)

        if head_text is not None:
            any_head = True
            for k, v in _count_tags_in_content(head_text).items():
                head_counts[k] += v

        if fname in staged_basenames:
            path = next((p for p in staged_paths if os.path.basename(p) == fname), fname)
            if os.path.isfile(path) and is_in_scope(path):
                _, fc = parse_file(path)
                for k, v in fc.items():
                    wt_counts[k] += v
            elif head_text is not None:
                # Staged file with matching basename is out-of-scope (e.g. skipped dir);
                # treat the governed file as unchanged.
                for k, v in _count_tags_in_content(head_text).items():
                    wt_counts[k] += v
        elif head_text is not None:
            # Non-staged IN_SCOPE file: working tree == HEAD (unchanged by this commit)
            for k, v in _count_tags_in_content(head_text).items():
                wt_counts[k] += v

    wt_ratio = _ratio(wt_counts)

    if not any_head:
        # Genesis: no baseline exists — apply flat ceiling
        head_str, delta_str = "n/a", "n/a"
        should_block = wt_ratio > HYBRID_CEILING
        err = (
            f"Hybrid ratio {wt_ratio:.0%} exceeds {HYBRID_CEILING:.0%} ceiling "
            f"(genesis commit). Decompose hybrid sections to remediate."
        ) if should_block else ""
    else:
        head_ratio = _ratio(head_counts)
        delta = wt_ratio - head_ratio
        head_str = f"{head_ratio:.0%}"
        delta_str = f"{delta:+.0%}"
        should_block = wt_ratio > head_ratio and wt_ratio > HYBRID_CEILING
        err = (
            f"Hybrid ratio regression: {head_ratio:.1%} -> {wt_ratio:.1%} "
            f"(exceeds {HYBRID_CEILING:.0%} ceiling). "
            f"Decompose hybrid sections into dev/llm to remediate."
        ) if should_block else ""

    info = f"Hybrid ratio: {wt_ratio:.0%} (HEAD: {head_str}, delta: {delta_str})"
    return (1 if should_block else 0), info, err


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

    ratio_exit, ratio_info, ratio_err = _enforce_ratio(paths)
    if ratio_err:
        logger.error(ratio_err)

    violation_count = len(all_violations)
    file_count = len({v.file for v in all_violations})
    if violation_count:
        summary = f"Summary: {violation_count} violation(s) across {file_count} file(s). {ratio_info}."
    else:
        summary = f"Summary: all files pass. {ratio_info}."

    print(summary)
    return 1 if (all_violations or ratio_exit) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
