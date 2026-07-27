#!/usr/bin/env python
"""validate_hermetization.py -- ADR-101 section 3 refusal gate (#306).

A `language: system` local pre-commit hook, HUB-ONLY, **prospective-only**: it inspects
only ADDED paths (`git diff --cached --diff-filter=A`), so every existing file is
grandfathered and never checked (ADR-101 section 6 -- no retroactive rename over the
~130 subject-before-class + 4 class-less legacy files the date-index already
disambiguates). Two rules, both BLOCK (exit 1) on violation:

  Rule A (top-level seal, ADR-101 section 1/3): an added path that introduces
    (1) an unsanctioned Tier-1 top-level directory,
    (2) an unsanctioned Tier-1 top-level FILE (outside the sanctioned classes), or
    (3) a new Tier-2 `docs/<genre>/` folder
  -> BLOCK. The tree is hermetic: growing its top level is a deliberate, surfaced act
  (an ADR-101 amendment), never a drive-by folder -- directly fixing the #131 root cause.

  Rule B (audit grammar, ADR-101 section 2 + ratification R3/R4): an added
  `docs/audits/*.md` whose name fails `<YYYY-MM-DD>-<class>[-<slug>]` with
    * <class> whole-token LONGEST-MATCH against the CLOSED 11-class enum (never
      split-on-first-hyphen -- the multi-word tokens require it, S3-3), and
    * the R4 casing rule (all-lowercase kebab-case everywhere; no UPPERCASE, no
      _underscore_, no CamelCase; sole carve-out: a literal `.` in the slug for a
      meaningful repo/version token like `.dev-knowledge` / `v3.4`, S3-1)
  -> BLOCK. This is the rule that fixes the corp-monorepo UPPERCASE `_AUDIT_`/`_BRIEF_`
  divergence the census found (R4).

**Name-SHAPE only, never date-accuracy** (ADR-101 section 3 / S3-4): the filename date is
validated as a SHAPE (\\d{4}-\\d{2}-\\d{2}) only -- `2026-13-99` passes the shape gate;
a misdated-content detector is a different tool that must diff the content-header date,
never `git log`.

Consumer carrier (floor/plugin) is the P6 rollout -- this gate is HUB-ONLY until then,
mirroring `roster-freshness`/`claude-rosters-freshness`/`audit-index-freshness`.

Read-only (Layer-2, ADR-28/36): reads the staged name-status; writes NOTHING. Fail-OPEN
but LOUD on any git error -- a convention/hygiene gate must not brick every commit on a
near-impossible git failure. Bypass parity with peer hooks: `--no-verify`.
"""

from __future__ import annotations

import re
import subprocess
import sys
from typing import Optional

# --- ADR-101 section 1 sanctioned sets (CLOSED; grow only by ADR-101 amendment) -------

# Tier-1 -- sanctioned top-level directories.
SANCTIONED_TIER1_DIRS: frozenset[str] = frozenset({
    ".claude", ".claude-plugin", ".vscode", "codex", "config", "deploy", "docs",
    "ecosystem", "logs", "plugins", "protocols", "scripts", "templates", "tests",
})

# Tier-1 -- sanctioned top-level FILES (the closed class members, ADR-101 section 1).
SANCTIONED_TIER1_FILES: frozenset[str] = frozenset({
    # living docs (UPPERCASE.md, the closed set)
    "VISION.md", "ARCHITECTURE.md", "CLAUDE.md", "CONTRIBUTING.md",
    "JOURNAL.md", "LESSONS.md", "BACKLOG.md",
    # dotfile / tool config
    ".gitignore", ".gitattributes", ".pre-commit-config.yaml",
    ".pre-commit-hooks.yaml", ".ruff.toml", ".worktreeinclude",
    ".dev-knowledge.code-workspace",
    # intake #12 section-9a ruling (SETTLED 2026-07-12): the hub carries its OWN
    # .methodology.yaml as a fleet member -- ADR-101 amendment 2026-07-13, [#328].
    ".methodology.yaml",
    # build / package manifests
    "package.json", "package-lock.json", "pyproject.toml",
    # uv toolchain (ADR-101 amendment 2026-07-27, [#432]/ADR-106): the committed
    # dependency lockfile + interpreter pin -- same class as package-lock.json.
    "uv.lock", ".python-version",
})

# Tier-2 -- sanctioned docs/<genre>/ folders. `runbooks` LEFT the set 2026-07-22
# (ADR-101 amendment: d.i REVERSED -- the one-member genre collapsed into protocols/).
SANCTIONED_GENRES: frozenset[str] = frozenset({
    "archive", "audits", "decisions", "handoffs", "intake",
})

# --- ADR-101 section 2 + R3: the CLOSED 11-class audit-class enum ----------------------
# Whole-token LONGEST-MATCH (never split-on-first-hyphen). On-disk forms per R2 (the enum
# adopts what three repos already write: `codex` not `codex-review`;
# `conformance-nightly-digest` not `conformance-digest`).
AUDIT_CLASS_ENUM: frozenset[str] = frozenset({
    # semantic
    "technical", "functional", "qa", "census", "verification",
    # recurring / automated (on-disk forms, R2)
    "ecosystem-audit", "conformance-nightly-digest", "changelog-review",
    # reviewer-origin (on-disk forms, R1/R2)
    "codex", "fresh-eyes",
    # incident
    "incident-evidence",
})

# Longest-match order: try the longest tokens first so `ecosystem-audit` wins over a
# hypothetical `ecosystem` split, and `conformance-nightly-digest` is matched whole.
_ENUM_BY_LEN = tuple(sorted(AUDIT_CLASS_ENUM, key=len, reverse=True))

_DATE_SHAPE = re.compile(r"^\d{4}-\d{2}-\d{2}-")           # SHAPE only (S3-4)
_DATE_PREFIX_LEN = len("YYYY-MM-DD-")                       # 11 chars incl. trailing hyphen
# R4 casing: all-lowercase kebab-case + digits; `.` carve-out (repo/version tokens). No
# uppercase, no underscore, no other charset. Applied to the FULL filename (incl. the `.md`
# extension) so an uppercase `.MD` extension is caught too (codex-review 2026-07-11).
_LOWER_KEBAB_DOT = re.compile(r"^[a-z0-9.-]+$")
# A well-formed slug after the class: 1+ kebab segments of [a-z0-9.] joined by SINGLE
# hyphens — rejects empty / leading- / trailing- / double-hyphen slugs (codex-review
# 2026-07-11). The `.` repo/version carve-out rides inside a segment.
_SLUG_RE = re.compile(r"^[a-z0-9.]+(-[a-z0-9.]+)*$")


# --- pure classifiers (unit-tested directly; no git) ----------------------------------

def _posix_parts(path: str) -> list[str]:
    """Repo-relative path -> its components, normalized to forward slashes."""
    return path.replace("\\", "/").strip("/").split("/")


def rule_a_violation(path: str) -> Optional[str]:
    """Rule A (top-level seal). Return a BLOCK reason, or None if the added path is
    sanctioned by the top-level rules."""
    parts = _posix_parts(path)
    if len(parts) == 1:
        # A top-level file: must be a sanctioned class member.
        if parts[0] not in SANCTIONED_TIER1_FILES:
            return (f"unsanctioned new top-level file '{parts[0]}' -- Tier-1 files are a "
                    f"closed class (ADR-101 section 1); a genuinely new class is an "
                    f"ADR-101 amendment, not a drive-by add")
        return None
    top = parts[0]
    if top not in SANCTIONED_TIER1_DIRS:
        return (f"unsanctioned new top-level directory '{top}/' -- Tier-1 dirs are a "
                f"closed set (ADR-101 section 1); surface a new top-level dir via an "
                f"ADR-101 amendment before creating it")
    if top == "docs" and len(parts) >= 3:
        genre = parts[1]
        if genre not in SANCTIONED_GENRES:
            return (f"unsanctioned new docs genre folder 'docs/{genre}/' -- Tier-2 genres "
                    f"are a closed set (ADR-101 section 1); a new artifact class nests "
                    f"under an existing genre or is surfaced via an ADR-101 amendment")
    return None


def rule_b_violation(path: str) -> Optional[str]:
    """Rule B (audit grammar + R4 casing). Applies ONLY to an added docs/audits/*.md.
    Return a BLOCK reason, or None."""
    parts = _posix_parts(path)
    # Applicability is EXTENSION-CASE-INSENSITIVE so an uppercase `.MD` cannot dodge Rule B
    # by escaping the `.md` match (codex-review 2026-07-11); the casing rule below then
    # rejects the uppercase extension itself.
    if not (len(parts) == 3 and parts[0] == "docs" and parts[1] == "audits"
            and parts[2].lower().endswith(".md")):
        return None  # not an audit file -> Rule B is silent
    fname = parts[2]
    if fname.lower() == "readme.md":
        return None  # the generated index, not an audit artifact

    # R4 casing FIRST, on the FULL filename incl. extension (the corp UPPERCASE/underscore
    # divergence class + the .MD extension loophole).
    if not _LOWER_KEBAB_DOT.match(fname):
        return (f"casing: '{fname}' must be all-lowercase kebab-case everywhere incl. the "
                f".md extension (no UPPERCASE, no _underscore_, no CamelCase; only a `.` "
                f"inside the slug for a repo/version token) -- ADR-101 R4")
    stem = fname[: -len(".md")]  # fname is now guaranteed lowercase '.md'

    # Grammar: leading YYYY-MM-DD- (SHAPE only, never date-accuracy).
    if not _DATE_SHAPE.match(stem):
        return (f"grammar: '{fname}' must start with a <YYYY-MM-DD>- date shape "
                f"(ADR-101 section 2); name-shape only, date-accuracy is never checked")

    # Class: whole-token LONGEST-MATCH against the CLOSED enum. A degenerate <date>-<class>
    # passes; a class-then-slug requires a WELL-FORMED slug (no empty/leading-/double-hyphen).
    remainder = stem[_DATE_PREFIX_LEN:]
    for cls in _ENUM_BY_LEN:
        if remainder == cls:
            return None  # degenerate <date>-<class>.md (recurring report, no slug)
        if remainder.startswith(cls + "-"):
            slug = remainder[len(cls) + 1:]
            if _SLUG_RE.match(slug):
                return None  # class-then-well-formed-slug
            return (f"slug: '{fname}' has a malformed slug after <class> '{cls}' "
                    f"(empty / leading- / trailing- / double-hyphen) -- ADR-101 section 2 "
                    f"kebab-case")
    return (f"class: '{fname}' has no CLOSED-enum <class> token after the date "
            f"(ADR-101 R3: technical/functional/qa/census/verification/ecosystem-audit/"
            f"conformance-nightly-digest/changelog-review/codex/fresh-eyes/"
            f"incident-evidence; whole-token longest-match)")


def classify(path: str) -> Optional[str]:
    """One added path -> the first BLOCK reason (Rule A then Rule B), or None if clean."""
    return rule_a_violation(path) or rule_b_violation(path)


def check(added_paths: list[str]) -> list[str]:
    """Every added path -> the list of `path: reason` BLOCK strings (empty == clean)."""
    reasons: list[str] = []
    for p in added_paths:
        r = classify(p)
        if r is not None:
            reasons.append(f"{p}: {r}")
    return reasons


# --- git glue (fail-open-loud) --------------------------------------------------------

def staged_added_paths() -> list[str]:
    """Paths staged with status A (added). Prospective-only: MODIFIED existing files are
    grandfathered. `--no-renames` forces a rename to surface as delete+ADD so a rename that
    introduces a NEW unsanctioned pathname is policed too (codex-review 2026-07-11) -- a
    rename introduces a new pathname just as much as a plain add. Fail-open on git error."""
    out = subprocess.run(
        ["git", "diff", "--cached", "--diff-filter=A", "--no-renames", "--name-only"],
        capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or f"git exited {out.returncode}")
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


def main() -> int:
    try:
        added = staged_added_paths()
    except (OSError, RuntimeError) as exc:
        # Fail OPEN but LOUD: a hermetization convention gate, not a safety control.
        print(f"validate_hermetization: WARNING -- could not read staged adds ({exc}); "
              f"hermetization check skipped", file=sys.stderr)
        return 0
    reasons = check(added)
    if reasons:
        print("validate_hermetization: refused -- ADR-101 hermetization violation(s):",
              file=sys.stderr)
        for r in reasons:
            print(f"  {r}", file=sys.stderr)
        print("  The tree is hermetic (ADR-101): a new top-level entry / docs genre, or "
              "an off-grammar audit filename, is a deliberate ADR-101 amendment -- not a "
              "drive-by add. Bypass (peer-hook parity): git commit --no-verify.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
