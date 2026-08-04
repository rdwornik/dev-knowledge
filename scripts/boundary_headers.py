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
discipline.

Safety properties (each earned from a codex finding on the first cut)
--------------------------------------------------------------------
* **Stripping is marker-adjacent.** A generated header is removed only when it matches the
  full-line grammar AND the next line opens a region. Prose that merely *quotes* the header
  format -- documentation, an example, a §12 history entry -- is never eaten.
* **Fence-aware.** Markers inside a fenced code block are examples, not markers.
* **Line endings preserved.** Terminators are carried through untouched, so regenerating a
  CRLF file cannot silently rewrite every region body to LF.
* **Validate before transform.** Any parser warning (unbalanced / nested / mismatched-id)
  refuses ``--write`` and fails ``--check`` rather than emitting into a broken structure.
* **Coverage cannot be vacuous.** Required governed files are declared independently of
  marker presence, so deleting every marker FAILS instead of reporting an empty 100%.

Modes
-----
``--check``      validate + regen-and-diff every governed file; exit 1 on drift or warning.
``--write``      rewrite governed files in place (refuses on a parser warning).
``--coverage``   print ``headed/total`` governed files; exit 1 below 100% or if vacuous.

Layer-2 safe: reads and writes only ``.dev-knowledge`` paths (ADR-28/36).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatchcase
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

# Files that are governed BY DECLARATION, not by whether they currently carry markers.
# Without this, deleting every marker from CLAUDE.md would drop it out of the denominator
# and report a vacuous 0/0 = 100% -- the metric would go blind exactly when the boundary
# disappeared, which is the one failure it exists to catch.
_REQUIRED_GOVERNED = ("CLAUDE.md",)

_HUB_LABEL = "[HUB - methodology]"
_REPO_LABEL = "[REPO - local]"
_HUB_HEADER = (
    "> **" + _HUB_LABEL + "** region `{id}` - single-sourced from the hub; "
    "do not edit these lines here."
)
_REPO_HEADER = "> **" + _REPO_LABEL + "** region `{id}` - this repo owns these lines."

# Full-line grammar of a line THIS module emits. Anchored and complete -- not a prefix
# test -- so a lookalike or a hand-altered header is never silently accepted as current,
# and prose quoting the format is not matched by accident.
_GENERATED_RE = re.compile(
    r"^> \*\*\[(?:HUB - methodology|REPO - local)\]\*\* region `[a-z0-9-]+` - .*$"
)
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def is_generated_header(line: str) -> bool:
    """True if `line` matches the exact grammar this module emits.

    NOTE: matching the grammar is necessary but NOT sufficient for removal -- see
    `_strip_generated`, which additionally requires the line to be marker-adjacent.
    """
    return bool(_GENERATED_RE.match(line.rstrip("\r\n")))


def header_for(region_id: str, owner: str) -> str:
    """The reader-visible header for one marker. Pure function of the marker attributes."""
    template = _HUB_HEADER if owner == "hub" else _REPO_HEADER
    return template.format(id=region_id)


def _split_keepends(text: str) -> list[str]:
    """Lines WITH their terminators, so CRLF/LF is carried through untouched."""
    return text.splitlines(keepends=True)


def _marker_flags(lines: list[str]) -> list[bool]:
    """Per line: is this a REAL marker line (i.e. not inside a fenced code block)?

    A fenced example is documentation, not a boundary declaration. Treating it as one
    would emit a header into a code block and, worse, count it in coverage.
    """
    flags: list[bool] = []
    fence: str | None = None          # the OPENING delimiter char, or None
    for raw in lines:
        line = raw.rstrip("\r\n")
        m = _FENCE_RE.match(line)
        if m:
            tok = m.group(1)[0]
            if fence is None:         # opening
                fence = tok
                flags.append(False)
                continue
            if fence == tok:          # matching close
                fence = None
                flags.append(False)
                continue
            # a ``` line inside a ~~~ block (or vice versa) is CONTENT, not a delimiter
        s = line.strip()
        flags.append(fence is None and bool(_START_RE.match(s) or _END_RE.match(s)))
    return flags


def _start_match(raw: str):
    return _START_RE.match(raw.rstrip("\r\n").strip())


def _strip_generated(lines: list[str], is_marker: list[bool]) -> list[str]:
    """Drop generated headers that sit immediately before a real start marker.

    Marker-adjacency is the safety property: a line matching the grammar but NOT leading
    into a region opener is authored prose (an example, a history entry) and is preserved.

    A contiguous RUN of generated-grammar lines before one start marker is stripped whole.
    Stripping only the adjacent line would leave a stale duplicate that then survives every
    later regeneration -- a header disagreeing with its marker while `--check` reports no
    drift, which is precisely the failure this module exists to make impossible.
    """
    drop = [False] * len(lines)
    i = 0
    while i < len(lines):
        if is_generated_header(lines[i]):
            j = i
            while j < len(lines) and is_generated_header(lines[j]):
                j += 1
            if j < len(lines) and is_marker[j] and _start_match(lines[j]):
                for k in range(i, j):
                    drop[k] = True
            i = j
            continue
        i += 1
    return [raw for i, raw in enumerate(lines) if not drop[i]]


def apply_headers(text: str) -> str:
    """Return `text` with exactly one generated header before each real start marker.

    Idempotent: ``apply_headers(apply_headers(t)) == apply_headers(t)``.
    Line terminators are preserved exactly.
    """
    lines = _split_keepends(text)
    kept = _strip_generated(lines, _marker_flags(lines))
    kept_flags = _marker_flags(kept)

    # Terminator to use for an inserted line: match the line it precedes.
    out: list[str] = []
    for i, raw in enumerate(kept):
        if kept_flags[i]:
            ms = _start_match(raw)
            if ms:
                term = "\r\n" if raw.endswith("\r\n") else ("\n" if raw.endswith("\n") else "")
                out.append(header_for(ms.group(1), ms.group(2)) + term)
        out.append(raw)
    return "".join(out)


def has_markers(text: str) -> bool:
    """True if `text` carries at least one real (non-fenced) marker line."""
    return any(_marker_flags(_split_keepends(text)))


def is_fully_headed(text: str) -> bool:
    """True if every real start marker is immediately preceded by its exact header."""
    lines = _split_keepends(text)
    flags = _marker_flags(lines)
    for i, raw in enumerate(lines):
        if not flags[i]:
            continue
        ms = _start_match(raw)
        if not ms:
            continue
        want = header_for(ms.group(1), ms.group(2))
        if i == 0 or lines[i - 1].rstrip("\r\n") != want:
            return False
    return True


@dataclass
class FileReport:
    path: Path
    rel: str
    regions: int
    headed: bool
    drifted: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _tracked_files(repo_root: Path) -> list[str]:
    """Git-tracked paths (POSIX-separated). Tracked-only: untracked scratch is not governed."""
    proc = subprocess.run(["git", "-C", str(repo_root), "ls-files"],
                          capture_output=True, text=True, check=True)
    return [ln for ln in proc.stdout.splitlines() if ln]


def _glob_matches(rel: str, pattern: str) -> bool:
    """True-glob match of one POSIX-separated path against one pattern ([#482]).

    TRUE-GLOB, not `fnmatch` ([#482], operator ruling 2026-08-03 — REPAIR, not REMOVE).
    `fnmatch` has no `**` and its `*` CROSSES `/`, so `.claude/*.md` was already recursive
    while `.claude/**/*.md` was a strict subset of it adding nothing: each glob read
    narrower than it behaved. Here `*` never crosses a separator and `**` means zero or
    more whole segments — so a pattern means what it reads.

    `fnmatchcase`, never `fnmatch`, for the per-SEGMENT step. `fnmatch` normalizes case via
    `os.path.normcase`, a no-op on POSIX and lowercasing on Windows — so the same repository
    yielded a DIFFERENT governed set depending on which box ran the gate. Paths here come
    from `git ls-files`, which is case-sensitive on every platform, so host case rules were
    never the right authority.

    WHY HAND-COMPOSED rather than a stdlib call: `glob.translate()` and
    `PurePath.full_match()` are both 3.13+, and this repo's floor is `>=3.12`;
    3.12's `PurePath.match()` is right-anchored (`*.md` matches `a/b/c.md`) with a
    non-recursive `**`. This is those 3.13 semantics backported, and it is a one-line swap
    for `full_match` once the floor moves. `glob.glob(recursive=True)` was rejected as the
    engine: it walks the WORKING TREE rather than the git index, so a tracked file deleted
    from the worktree would silently leave the governed set — the gate going blind exactly
    when a governed file vanishes. It is still used as the ORACLE this matcher is proved
    against (`test_glob_matches_agrees_with_stdlib_glob_per_glob`), which is how a
    hand-composed matcher earns its keep: it carries its own live proof.

    `pathspec` was rejected too, though already installed: its dialect is `gitwildmatch`,
    not pure glob, so adopting it would reintroduce the very defect class this repair
    closes — a matcher whose semantics differ from what the pattern string reads.
    """
    parts, pats = rel.split("/"), pattern.split("/")

    def walk(i: int, j: int) -> bool:
        if j == len(pats):
            return i == len(parts)
        if pats[j] == "**":                       # zero or more WHOLE segments
            return any(walk(k, j + 1) for k in range(i, len(parts) + 1))
        return (i < len(parts)
                and fnmatchcase(parts[i], pats[j])   # `*` cannot cross `/`: one segment only
                and walk(i + 1, j + 1))

    return walk(0, 0)


def _matches_governed_glob(rel: str) -> bool:
    """True iff a POSIX-separated tracked path falls under `_GOVERNED_GLOBS`.

    Extracted so the match rule is one named, directly testable predicate instead of an
    expression buried in the discovery loop.
    """
    return any(_glob_matches(rel, g) for g in _GOVERNED_GLOBS)


def discover_governed(repo_root: Path = _REPO_ROOT) -> tuple[list[Path], list[str]]:
    """(governed files, errors).

    Governed = every `_REQUIRED_GOVERNED` file (unconditionally) plus any tracked file
    under `_GOVERNED_GLOBS` that carries >=1 real marker. An unreadable candidate is an
    ERROR, never a silent skip.
    """
    found: list[Path] = []
    errors: list[str] = []
    for rel in _tracked_files(repo_root):
        if not _matches_governed_glob(rel):
            continue
        path = repo_root / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{rel}: unreadable governed candidate ({exc.__class__.__name__})")
            continue
        if rel in _REQUIRED_GOVERNED or has_markers(text):
            found.append(path)
            if rel not in _REQUIRED_GOVERNED:
                # Discovery is a TRIPWIRE, not the source of the governed set. Left
                # undeclared, this file would silently leave the denominator the day its
                # markers were deleted -- coverage would read 100% with the boundary gone.
                errors.append(f"{rel}: carries markers but is not declared in "
                              f"_REQUIRED_GOVERNED -- declare it, so coverage cannot go "
                              f"blind if its markers are later deleted")

    present = {p.relative_to(repo_root).as_posix() for p in found}
    for rel in _REQUIRED_GOVERNED:
        if rel not in present:
            errors.append(f"{rel}: required governed file missing from the tracked tree")
    return sorted(found), errors


def inspect(repo_root: Path = _REPO_ROOT) -> tuple[list[FileReport], list[str]]:
    """Per governed file: region count, headed?, would-regeneration-change-it?"""
    paths, errors = discover_governed(repo_root)
    reports: list[FileReport] = []
    for path in paths:
        rel = path.relative_to(repo_root).as_posix()
        text = path.read_text(encoding="utf-8")
        regions, warnings = parse_regions(text)
        errs: list[str] = []
        kept = text.splitlines(keepends=True)
        seen_starts = sum(1 for raw, flag in zip(kept, _marker_flags(kept))
                          if flag and _start_match(raw))
        if seen_starts != len(regions):
            # The generator is fence-aware; boundary_report is not. A disagreement means a
            # marker sits inside (or after an unterminated) fence -- resolve it rather than
            # letting the two organs classify the same lines differently.
            errs.append(f"{rel}: generator sees {seen_starts} start marker(s) but "
                        f"boundary_report parses {len(regions)} region(s) -- a fenced or "
                        f"unterminated-fence disagreement; resolve before generating")
        if rel in _REQUIRED_GOVERNED and not regions:
            errs.append(f"{rel}: required governed file carries NO markers "
                        f"-- the boundary has gone invisible")
        reports.append(FileReport(
            path=path, rel=rel, regions=len(regions),
            headed=is_fully_headed(text),
            drifted=apply_headers(text) != text,
            warnings=warnings, errors=errs,
        ))
    return reports, errors


def _report_problems(reports: list[FileReport], errors: list[str]) -> bool:
    """Print every error/warning. True if anything disqualifying was found."""
    bad = False
    for err in errors:
        print(f"[ERROR] {err}")
        bad = True
    for rep in reports:
        for err in rep.errors:
            print(f"[ERROR] {err}")
            bad = True
        for w in rep.warnings:
            print(f"[ERROR] {rep.rel}: marker parse warning -- {w}")
            bad = True
    return bad


def cmd_write(repo_root: Path) -> int:
    reports, errors = inspect(repo_root)
    if _report_problems(reports, errors):
        print("[FAIL] refusing to write into a file whose markers do not parse cleanly")
        return 1
    changed = 0
    for rep in reports:
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
    reports, errors = inspect(repo_root)
    bad = _report_problems(reports, errors)
    for rep in reports:
        if rep.drifted:
            print(f"[FAIL]  {rep.rel}: headers stale vs markers "
                  f"-- run `python scripts/boundary_headers.py --write`")
            bad = True
    if bad:
        return 1
    print("boundary-headers: all generated headers match their markers")
    return 0


def cmd_coverage(repo_root: Path) -> int:
    """Coverage = governed files carrying reader-visible headers / total governed files."""
    reports, errors = inspect(repo_root)
    bad = _report_problems(reports, errors)
    total = len(reports)
    headed = sum(1 for r in reports if r.headed)
    for rep in reports:
        mark = "OK  " if rep.headed else "MISS"
        print(f"[{mark}] {rep.rel}: {rep.regions} region(s)")
    if total == 0:
        print("[FAIL] no governed files discovered -- coverage would be vacuous")
        return 1
    pct = 100.0 * headed / total
    print(f"boundary-header coverage: {headed}/{total} governed files headed ({pct:.0f}%)")
    if headed != total:
        print("[FAIL] unheaded governed file(s) -- run "
              "`python scripts/boundary_headers.py --write`")
        return 1
    return 1 if bad else 0


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
