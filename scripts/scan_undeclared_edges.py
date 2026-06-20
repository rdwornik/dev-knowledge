#!/usr/bin/env python
"""scan_undeclared_edges.py — #179 undeclared-edge referential-currency scan (FC2).

The DISCOVERY half of dependency coherence. The coherence spine (#172) only catches
staleness on edges a dependent has already DECLARED via `reconciled_with: <spec-id>@<ver>`.
This scan finds the edges that were never declared: a doc Y that references a registered
spec X in PROSE but carries no `reconciled_with: X@...` line. Such an edge is invisible to
`validate_reconciliation.py`, so a change to X never flags Y as stale (ADR-88 failure class
FC2). The scan surfaces (Y -> X) as a CANDIDATE for a human to confirm; on confirmation the
human adds the `reconciled_with` line and the existing checker takes over. It is discovery
of MISSING edges, the complement to #172's checking of DECLARED ones.

NO AUTO-DECLARE (the load-bearing rule). The scan only surfaces; the human confirms each
candidate and writes the edge. Read-only (Layer-2, ADR-28/36): reads docs + spec files;
writes NOTHING; never gates by exit code (CLI exits 0 always — an awareness layer, like
validate_reconciliation / validate_no_ff).

Candidate rule — a doc Y is a candidate undeclared edge to spec X iff ALL of:
  1. Y is a repo .md (pruning vr._EXCLUDE_DIRS + archive*, the discover_dependents walk);
  2. Y is not X itself (self-reference exclusion);
  3. Y does NOT already declare `reconciled_with: X@...` (the GAP-ONLY rule — an already-
     declared edge, even to an older version, is left to the version checker, never re-flagged);
  4. Y prose-references X above the surfacing threshold.

Reference tiers (derived per spec, never hardcoded to one edge):
  * Tier 1 — the spec's repo-relative path or basename (`protocols/HANDOFF_PROCESS.md`).
  * Tier 2 — the registry spec-id token (`handoff-process`), the declaration token itself.
  * Tier 3 — the SCREAMING_SNAKE family + title/space variants (reuses
    coherence_enumerator._spec_key_terms — #172 "one regex, N consumers" dedup).
Tier 1+2 are surfaced as CANDIDATES; Tier-3-only docs are RETAINED in a separate weak-signal
section (fully enumerated with evidence, human-promotable) — never a bare count, never
silently dropped. The split is precision: the enumerator over-extracts per KNOWN edge
(cheap); this scan runs repo-wide x every spec, where undifferentiated over-extraction is
noise, so candidates stay high-precision (ADR-88 Principle 4, narrow-first) while the weak
tier stays visible for human judgment.

Fenced code regions are excluded from MATCHING (not only from snippet rendering): a fenced
operational path ref — a command example naming the spec file — is not a `reconciled_with`
content-dependency. Mirrors coherence_enumerator's `fenced_line_idx` skip for its prose
`sections` category. Inline code spans (single backtick, on a prose line) are kept — they are
genuine in-prose references.

Specs scanned = the curated vr._SPEC_REGISTRY (narrow-first). No broadening to "all ADRs".
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:  # package-first / direct-fallback, mirroring audit.py + coherence_enumerator.py
    from scripts import coherence_enumerator as ce
    from scripts import validate_reconciliation as vr
except ImportError:
    import coherence_enumerator as ce
    import validate_reconciliation as vr

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# Tiers: lower number == stronger signal. 1/2 surface as candidates; 3 is weak (retained).
_CANDIDATE_TIER_MAX = 2


@dataclass(frozen=True)
class RefSite:
    """One prose reference to the spec in a dependent doc, with its strongest tier."""
    line: int                       # 1-based line number in the dependent
    tier: int                       # 1 (path/basename) | 2 (spec-id) | 3 (family/prose)
    snippet: str                    # fence-safe, one-line anchor


@dataclass(frozen=True)
class Candidate:
    """A surfaced undeclared-edge candidate: doc Y -> spec X, with its evidence sites."""
    dependent_path: str             # repo-relative posix
    spec_id: str
    spec_path: str                  # repo-relative posix
    best_tier: int                  # strongest (min) tier across sites
    sites: tuple[RefSite, ...]


# --- detection (pure) -------------------------------------------------------

def _tier_patterns(spec: vr.SpecSource) -> tuple[list[re.Pattern], list[re.Pattern], tuple[re.Pattern, ...]]:
    """The (tier1, tier2, tier3) match patterns derived from a spec, strongest first.

    Tier 1: the spec's repo-relative path and its basename, matched verbatim (the `.md`
    and SCREAMING_SNAKE stem make these distinctive — case-sensitive, no false prose hits).
    Tier 2: the registry spec-id token, word-bounded, case-insensitive.
    Tier 3: coherence_enumerator._spec_key_terms over the filename stem (the shared
    prose-pattern derivation — not re-implemented here).
    """
    posix_path = Path(spec.path).as_posix()
    basename = Path(spec.path).name
    tier1 = [re.compile(re.escape(posix_path)), re.compile(re.escape(basename))]
    tier2 = [re.compile(rf"\b{re.escape(spec.spec_id)}\b", re.IGNORECASE)]
    tier3 = ce._spec_key_terms(Path(spec.path).stem)
    return tier1, tier2, tier3


def reference_sites(doc_text: str, spec: vr.SpecSource) -> list[RefSite]:
    """Every prose reference to `spec` in `doc_text`, one RefSite per matching line.

    Each line is classified by its STRONGEST matching tier (1 > 2 > 3). Lines inside
    fenced code blocks are skipped in matching (a fenced operational path ref is not a
    content-dependency) — fence detection reuses coherence_enumerator._find_fenced_blocks.
    Pure; reads nothing. Over-extraction within a tier is fine; the tier split is what
    keeps the candidate set precise.
    """
    lines = doc_text.splitlines()
    fenced_idx = {idx for (s, e, _info) in ce._find_fenced_blocks(lines)
                  for idx in range(s, e + 1)}
    tier1, tier2, tier3 = _tier_patterns(spec)
    sites: list[RefSite] = []
    for idx, line in enumerate(lines):
        if idx in fenced_idx:
            continue
        if any(p.search(line) for p in tier1):
            tier = 1
        elif any(p.search(line) for p in tier2):
            tier = 2
        elif any(p.search(line) for p in tier3):
            tier = 3
        else:
            continue
        sites.append(RefSite(idx + 1, tier, ce._sanitize_anchor(line)))
    return sites


def _declared_spec_ids(doc_text: str) -> set[str]:
    """The spec-ids this doc already declares via `reconciled_with` (the GAP-ONLY filter).

    A well-formed `<spec-id>@<ver>` yields its spec-id; a malformed value (e.g. a bare
    `handoff-process` with no @version) still yields the named token — a doc that already
    NAMES the spec in its edge is not an undeclared edge, even if the declaration is
    malformed (that is the version checker's WARN, not ours to re-flag)."""
    raw = vr.parse_reconciled_with(doc_text)
    if raw is None:
        return set()
    parsed = vr.split_edge(raw)
    if parsed is not None:
        return {parsed[0]}
    token = raw.split("@", 1)[0].strip()
    return {token} if token else set()


def _walk_md(repo_root: Path):
    """Yield (repo-relative posix path, text) for every repo .md, pruning excluded dirs.

    The discover_dependents walk, but over ALL .md (not only those declaring an edge).
    Deterministic (sorted filenames). Read-only; OSErrors skipped."""
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames
                       if d not in vr._EXCLUDE_DIRS and not d.startswith("archive")]
        for fn in sorted(filenames):
            if not fn.endswith(".md"):
                continue
            fp = Path(dirpath) / fn
            try:
                text = fp.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            yield fp.relative_to(repo_root).as_posix(), text


def scan(repo_root: Path, registry: dict | None = None) -> list[Candidate]:
    """Every undeclared prose edge in the repo, candidates AND weak signals together.

    Returns one Candidate per (doc, spec) pair with >=1 reference site, carrying its
    strongest tier; the caller (format_report) splits tier<=2 candidates from tier-3 weak
    signals. No tier-3 row is discarded here. Read-only."""
    reg = vr._SPEC_REGISTRY if registry is None else registry
    out: list[Candidate] = []
    for rel, text in _walk_md(repo_root):
        declared = _declared_spec_ids(text)
        for spec_id, spec in reg.items():
            if rel == Path(spec.path).as_posix():       # self-reference exclusion
                continue
            if spec_id in declared:                     # gap-only: already declared
                continue
            sites = reference_sites(text, spec)
            if not sites:
                continue
            best = min(s.tier for s in sites)
            out.append(Candidate(rel, spec_id, Path(spec.path).as_posix(), best, tuple(sites)))
    return sorted(out, key=lambda c: (c.best_tier, c.dependent_path, c.spec_id))


# --- rendering (read-only; flat + fence-safe per CLAUDE.md S4) ---------------

def _confirm_hint(repo_root: Path, cand: Candidate, registry: dict) -> str:
    """The surface-only confirmation hint — NEVER written by this tool."""
    spec = registry[cand.spec_id]
    current = vr.spec_current_version(repo_root, spec) or "<spec-version>"
    return (f"confirm: add `reconciled_with: {cand.spec_id}@{current}` "
            f"to {cand.dependent_path} frontmatter")


def _render_block(repo_root: Path, cands: list[Candidate], registry: dict) -> list[str]:
    out: list[str] = []
    for c in cands:
        out.append(f"  {c.dependent_path}  ->  {c.spec_id}  (tier {c.best_tier})")
        for s in c.sites:
            out.append(f"      L{s.line} (tier {s.tier}): {s.snippet}")
        if c.best_tier <= _CANDIDATE_TIER_MAX:
            out.append(f"      {_confirm_hint(repo_root, c, registry)}")
    return out


def format_report(repo_root: Path, results: list[Candidate], registry: dict | None = None) -> str:
    """Flat two-section report: CANDIDATES (tier<=2) then RETAINED weak signals (tier 3).

    Flat / no padded pipe-tables and fence-safe snippets (CLAUDE.md S4 render-layer rule).
    The weak section is always rendered and fully enumerated — human-promotable, never a
    bare count."""
    reg = vr._SPEC_REGISTRY if registry is None else registry
    candidates = [c for c in results if c.best_tier <= _CANDIDATE_TIER_MAX]
    weak = [c for c in results if c.best_tier > _CANDIDATE_TIER_MAX]

    lines = [f"scan_undeclared_edges: {len(candidates)} candidate(s), "
             f"{len(weak)} weak signal(s)"]
    lines.append("")
    lines.append("CANDIDATES (undeclared prose edges — confirm each; NO auto-declare):")
    lines.extend(_render_block(repo_root, candidates, reg) if candidates
                 else ["  (none)"])
    lines.append("")
    lines.append("WEAK SIGNALS (tier-3 bare-name mentions — RETAINED, human-promotable; "
                 "not auto-candidates):")
    lines.extend(_render_block(repo_root, weak, reg) if weak else ["  (none)"])
    return "\n".join(lines)


def main() -> int:
    """Standalone CLI: print candidates + retained weak signals; exit 0 always (awareness)."""
    try:  # scanned snippets may carry non-cp1252 glyphs (e.g. U+2192) on a Windows console
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    results = scan(_REPO_ROOT)
    print(format_report(_REPO_ROOT, results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
