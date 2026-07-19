#!/usr/bin/env python3
"""Generate reader-visible ownership headers FROM the #312 Form-A boundary markers.

The boundary has two representations: the machine markers
(``<!-- methodology:start id=... owner=hub|repo -->``) and the reader-visible header a
human sees when they open the file. If those two were maintained in parallel they would
drift, and the fleet would grow two vocabularies that can disagree. So:

    THE MARKERS ARE THE SINGLE SOURCE OF TRUTH. Headers are GENERATED from them.

The coupling is structural, not conventional: this module imports the marker regexes and
the parser from ``boundary_report`` (the #312 reporter) rather than restating them. There
is exactly one definition of the marker vocabulary in the repo, and both the reporter and
this generator read it.

Placement contract
------------------
A generated header is emitted on the line IMMEDIATELY BEFORE its ``methodology:start``
marker -- never inside the region. Region BODIES therefore stay byte-identical to the
``templates/claude-regions/*.md`` extracts, preserving the v2.39/v2.42 byte-match
discipline. Regeneration first strips every previously generated header, so the transform
is idempotent and ``--check`` is a true regen-and-diff.

Modes
-----
``--check``      regen-and-diff every governed file; exit 1 on drift (gate form).
``--write``      rewrite governed files in place.
``--coverage``   print ``headed/total`` governed files; exit 1 below 100%.

Layer-2 safe: reads and writes only ``.dev-knowledge`` paths (ADR-28/36).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

# The marker vocabulary is single-sourced from the #312 reporter. Importing it (rather
# than restating the regexes) is what makes "headers derived from markers" a structural
# guarantee instead of a convention someone can forget.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from boundary_report import _END_RE, _START_RE, parse_regions  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent

# Governed surfaces: the CONFIG files a reader opens to learn how the repo is governed.
# Deliberately excludes docs/ -- audits and handoffs QUOTE the marker syntax as evidence
# (inside fences, tables and PowerShell strings); they are immutable records, not governed
# config, and counting them would make coverage meaningless.
_GOVERNED_GLOBS = ("CLAUDE.md", ".claude/*.md", ".claude/**/*.md")

_HUB_HEADER = (
    "> **[HUB - methodology]** region `{id}` - single-sourced from the hub; "
    "do not edit these lines here."
)
_REPO_HEADER = (
    "> **[REPO - local]** region `{id}` - this repo owns these lines."
)

# Recognises a line this module previously emitted, so regeneration can strip it. Kept
# deliberately narrow (the exact rendered shape) so hand-written prose is never eaten.
_GENERATED_PREFIXES = ("> **[HUB - methodology]** region ", "> **[REPO - local]** region ")


def is_generated_header(line: str) -> bool:
    """True if `line` is a header this module emitted (and may therefore strip)."""
    return line.startswith(_GENERATED_PREFIXES)


def header_for(region_id: str, owner: str) -> str:
    """The reader-visible header for one marker. Pure function of the marker attributes."""
    template = _HUB_HEADER if owner == "hub" else _REPO_HEADER
    return template.format(id=region_id)


def apply_headers(text: str) -> str:
    """Return `text` with exactly one generated header before each `methodology:start`.

    Strips previously generated headers first, so the transform is idempotent:
    ``apply_headers(apply_headers(t)) == apply_headers(t)``.
    """
    kept = [ln for ln in text.splitlines() if not is_generated_header(ln)]
    out: list[str] = []
    for line in kept:
        ms = _START_RE.match(line.strip())
        if ms:
            out.append(header_for(ms.group(1), ms.group(2)))
        out.append(line)
    trailing = "\n" if text.endswith("\n") else ""
    return "\n".join(out) + trailing


def has_markers(text: str) -> bool:
    """True if `text` carries at least one well-formed marker line."""
    return any(_START_RE.match(ln.strip()) or _END_RE.match(ln.strip())
               for ln in text.splitlines())


def is_fully_headed(text: str) -> bool:
    """True if every `methodology:start` in `text` is immediately preceded by its header."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        ms = _START_RE.match(line.strip())
        if not ms:
            continue
        want = header_for(ms.group(1), ms.group(2))
        if i == 0 or lines[i - 1] != want:
            return False
    return True


@dataclass
class FileReport:
    path: Path
    rel: str
    regions: int
    headed: bool
    drifted: bool
    warnings: list[str]


def _tracked_files(repo_root: Path) -> list[str]:
    """Git-tracked paths (POSIX-separated). Tracked-only: untracked scratch is not governed."""
    proc = subprocess.run(["git", "-C", str(repo_root), "ls-files"],
                          capture_output=True, text=True, check=True)
    return [ln for ln in proc.stdout.splitlines() if ln]


def discover_governed(repo_root: Path = _REPO_ROOT) -> list[Path]:
    """Governed files = tracked files under `_GOVERNED_GLOBS` that carry >=1 marker.

    Discovery, not a hardcoded list -- a newly marked config file is picked up
    automatically, which is what lets the coverage check fail on an unheadered file.
    """
    found: list[Path] = []
    for rel in _tracked_files(repo_root):
        if not any(fnmatch(rel, g) for g in _GOVERNED_GLOBS):
            continue
        path = repo_root / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if has_markers(text):
            found.append(path)
    return sorted(found)


def inspect(repo_root: Path = _REPO_ROOT) -> list[FileReport]:
    """Report per governed file: region count, headed?, would-regeneration-change-it?"""
    reports: list[FileReport] = []
    for path in discover_governed(repo_root):
        text = path.read_text(encoding="utf-8")
        regions, warnings = parse_regions(text)
        reports.append(FileReport(
            path=path,
            rel=path.relative_to(repo_root).as_posix(),
            regions=len(regions),
            headed=is_fully_headed(text),
            drifted=apply_headers(text) != text,
            warnings=warnings,
        ))
    return reports


def cmd_write(repo_root: Path) -> int:
    changed = 0
    for rep in inspect(repo_root):
        text = rep.path.read_text(encoding="utf-8")
        new = apply_headers(text)
        if new != text:
            rep.path.write_text(new, encoding="utf-8", newline="")
            print(f"[write] {rep.rel}: {rep.regions} region header(s) regenerated")
            changed += 1
        else:
            print(f"[ok]    {rep.rel}: already current ({rep.regions} region(s))")
    print(f"boundary-headers: {changed} file(s) rewritten")
    return 0


def cmd_check(repo_root: Path) -> int:
    drifted = [r for r in inspect(repo_root) if r.drifted]
    for rep in inspect(repo_root):
        for w in rep.warnings:
            print(f"[warn]  {rep.rel}: {w}")
    if drifted:
        for rep in drifted:
            print(f"[FAIL]  {rep.rel}: headers stale vs markers "
                  f"-- run `python scripts/boundary_headers.py --write`")
        return 1
    print("boundary-headers: all generated headers match their markers")
    return 0


def cmd_coverage(repo_root: Path) -> int:
    """Coverage = governed files carrying reader-visible headers / total governed files."""
    reports = inspect(repo_root)
    total = len(reports)
    headed = sum(1 for r in reports if r.headed)
    for rep in reports:
        mark = "OK  " if rep.headed else "MISS"
        print(f"[{mark}] {rep.rel}: {rep.regions} region(s)")
    pct = 100.0 if total == 0 else 100.0 * headed / total
    print(f"boundary-header coverage: {headed}/{total} governed files headed ({pct:.0f}%)")
    if headed != total:
        print("[FAIL] unheaded governed file(s) -- run "
              "`python scripts/boundary_headers.py --write`")
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true", help="regenerate headers in place")
    g.add_argument("--check", action="store_true", help="regen-and-diff; exit 1 on drift")
    g.add_argument("--coverage", action="store_true",
                   help="headed/total governed files; exit 1 below 100%%")
    ap.add_argument("--repo-root", type=Path, default=_REPO_ROOT)
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    if args.write:
        return cmd_write(root)
    if args.check:
        return cmd_check(root)
    return cmd_coverage(root)


if __name__ == "__main__":
    raise SystemExit(main())
