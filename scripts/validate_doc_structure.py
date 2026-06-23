#!/usr/bin/env python
"""validate_doc_structure.py — read-only prose **structural** linter (supplement organ #2).

The deterministic-trigger layer for **ADR-88's prose-shape coherence** — the graph *shape*
of the methodology docs: section-numbering integrity, header-scheme consistency, and ToC
accuracy. These are exactly the properties the architect **provably cannot eyeball** (proven
2/2 false this session: the PLAYBOOK §18 numbering gap and the embedded-template H2s inside
fenced blocks were both misread as rot when both are intentional). A grep over a text
snapshot can't see fenced code, documented-intentional gaps, or generator behaviour — which
is precisely why hand-auditing fails here, and why this is a live organ, not a snapshot grep.

DETECT-ONLY — it never edits, renumbers, or auto-fixes (a human ratifies any change;
renumbering the §18 gap would itself *create* dangling cross-references). Five deterministic
sub-detectors, each precision-over-recall (one false positive kills adoption):

  1. NUMBERING integrity (`scan_numbering`): within a doc's `## N.` section spine, a gap or a
     duplicate number — UNLESS the gap is covered by a co-located documented-intent marker
     (the §18 case). Decreasing numbers start a fresh run (a second numbered list is not rot).
  2. HEADER-SCHEME consistency (`scan_headers_scheme`): a malformed header (`##NoSpace`, an
     empty `## ` title) or a duplicate sibling header — two identical headers under the SAME
     immediate parent (a true anchor collision). Duplicates under DIFFERENT parents are benign
     parallel structure (the live PLAYBOOK "Process"/"Rules"/… repeats) and are not flagged.
  3. ToC accuracy (`scan_toc`): for a doc carrying a `<!-- TOC:START/END -->` block, ToC
     entries with no matching header (dangling) and headers absent from the ToC (orphan),
     compared bidirectionally. The header set comes from the **fence-aware** parser, so an
     embedded-template `## H2` inside a fence is never mistaken for a missing-from-ToC header.
  4. DANGLING-ALLOW self-policing (`scan_dangling_allow`): a `structure-allow` numbering-gap
     marker whose number is no longer a gap (the feature was resolved but the marker lingers).
     The organ polices its own exception-markers so a stale allow can't silently mask new rot.
  5. HEADING-SCHEME integrity (`scan_heading_scheme`): the `Ch`/`§` two-part convention — in a
     doc with a `## Part I … / ## Part II …` spine, every Part-I chapter is `## ChN.` sequential
     from Ch1 (gaps honour a `chapter-gap` allow marker). Stops an unnumbered `## Chapter` from
     silently re-drifting the standardization; Part-II `## N.` numbering is detector 1's job.

Documented-intent ledger — unit-of-truth is **live state ∪ the markers the doc itself carries**,
never a hand-kept dead-list. An intentional feature that would otherwise read as rot carries an
inline marker AT the site:  ``<!-- structure-allow: <kind> <locus> — <reason> -->``  (e.g.
``<!-- structure-allow: numbering-gap 18 — deleted, git has it -->``). Co-located so it travels
with the doc and is removed in the same edit that resolves the feature.

Scope boundary (do NOT duplicate): this is *structural shape*, a different failure class from
`validate_doc_rot.py` (#140, history-accretion bloat) — follow its pattern, don't overlap its
checks. ToC *regeneration* is gated separately by the `toc-freshness` pre-commit hook; this is
the WARN-level awareness complement, and its fence-awareness is the property the oracle tests.

Layer-2 / read-only contract (ADR-28/36): reads the living docs; writes NOTHING; never
orchestrates; never gates (awareness layer — the audit adapter emits WARN/pass only, one
Finding PER locus so the #147 ship-gate dispositions each independently; CLI exits 0).
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Reuse the fence-aware header parser + slugifier — the SAME machinery the ToC generator
# uses, so the linter and the ToC always agree (this is what makes the embedded-template
# H2 oracle pass: a fence-blind parser would treat `## What this project does` inside a
# fenced template as a real header -> false positive).
try:
    from scripts.toc.generator import _slugify, parse_headers
except ImportError:  # invoked from inside scripts/ (mirrors validate_doc_rot's import shape)
    from toc.generator import _slugify, parse_headers

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# Living docs scanned for structural shape (hub-relative; mirrors validate_doc_rot's set).
_STRUCTURE_DOCS = [
    "CLAUDE.md", "ARCHITECTURE.md", "VISION.md", "CONTRIBUTING.md",
    "protocols/PLAYBOOK.md", "protocols/ESSENTIALS.md",
    "protocols/HANDOFF_PROCESS.md", "protocols/AI_COUNCIL_PROCESS.md",
]

# A numbered section header text, e.g. "12. BACKLOG Grooming Workflow" -> 12.
_NUMBERED_RE = re.compile(r"^(\d+)\.\s+\S")
# A Part-I reference-chapter header text, e.g. "Ch3. Repo conventions" -> 3.
_CHAPTER_RE = re.compile(r"^Ch(\d+)\.\s+\S")
# The two-part spine markers: "Part I — Reference" / "Part II — Workflows" -> roman numeral.
_PART_RE = re.compile(r"^Part\s+(I+)\b")
# An inline documented-intent marker: `<!-- structure-allow: <kind> <locus> — <reason> -->`.
_ALLOW_RE = re.compile(r"<!--\s*structure-allow:\s*([\w-]+)\s+(\S+).*?-->")
# A malformed header that would be invisible to / break the ToC.
_MALFORMED_NOSPACE = re.compile(r"^#{2,3}[^#\s]")   # `##Foo` — no space after the hashes
_MALFORMED_EMPTY = re.compile(r"^#{2,3}[ \t]*$")    # `## ` — header marker, empty title
# Auto-TOC block markers + the anchor target of a `- [text](#anchor)` ToC link.
_TOC_START = "<!-- TOC:START -->"
_TOC_END = "<!-- TOC:END -->"
_TOC_LINK_RE = re.compile(r"\]\(#([^)]+)\)")


@dataclass(frozen=True)
class StructureFinding:
    category: str   # 'numbering-gap'|'numbering-dup'|'malformed-header'|'dup-header'|'toc-dangling'|'toc-orphan'|'dangling-allow'|'heading-scheme'
    locus: str      # stable token a #147 disposition can match (e.g. 'protocols/PLAYBOOK.md#numbering-18')
    detail: str     # human evidence


# --- shared helpers ---------------------------------------------------------

def parse_allow_markers(text: str) -> set[tuple[str, str]]:
    """Every `structure-allow` marker in `text` as a (kind, locus) set."""
    return {(m.group(1), m.group(2)) for m in _ALLOW_RE.finditer(text)}


def _nonfence_lines(text: str) -> list[str]:
    """Lines outside ``` fenced code blocks (mirrors parse_headers' fence toggle exactly)."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        out.append(line)
    return out


def _numbered_h2(text: str) -> list[int]:
    """The `## N.` section numbers in document order (fence-aware; level-2 only)."""
    nums: list[int] = []
    for level, raw in parse_headers(text):
        if level != 2:
            continue
        m = _NUMBERED_RE.match(raw)
        if m:
            nums.append(int(m.group(1)))
    return nums


def numbering_gaps(text: str) -> set[int]:
    """Every missing integer inside an ascending `## N.` run (ignores allow markers).

    A decrease starts a fresh run, so a second independent numbered list is never a 'gap'.
    """
    gaps: set[int] = set()
    prev: int | None = None
    for num in _numbered_h2(text):
        if prev is not None and num > prev + 1:
            gaps.update(range(prev + 1, num))
        prev = num
    return gaps


# --- sub-detectors (pure; unit-tested in isolation) -------------------------

def scan_numbering(rel: str, text: str, allow: set[tuple[str, str]]) -> list[StructureFinding]:
    """Gaps + duplicates in a doc's `## N.` spine; a gap with a matching allow is suppressed."""
    out: list[StructureFinding] = []
    prev: int | None = None
    for num in _numbered_h2(text):
        if prev is not None:
            if num == prev:
                out.append(StructureFinding(
                    "numbering-dup", f"{rel}#numbering-{num}",
                    f"section {num} appears twice in the numbered spine"))
            elif num > prev + 1:
                for missing in range(prev + 1, num):
                    if ("numbering-gap", str(missing)) in allow:
                        continue
                    out.append(StructureFinding(
                        "numbering-gap", f"{rel}#numbering-{missing}",
                        f"section {missing} missing between {prev} and {num} "
                        f"(no structure-allow marker — intentional? add one; else renumber)"))
        prev = num
    return out


def scan_headers_scheme(rel: str, text: str) -> list[StructureFinding]:
    """Malformed headers + duplicate sibling headers (identical slug under one parent)."""
    out: list[StructureFinding] = []

    # Duplicate siblings: same slug + same immediate parent header (a true anchor collision).
    stack: list[tuple[int, str]] = []
    seen: set[tuple[str, int, str]] = set()
    for level, raw in parse_headers(text):
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent = stack[-1][1] if stack else "<root>"
        slug = _slugify(raw)
        key = (parent, level, slug)
        if key in seen:
            out.append(StructureFinding(
                "dup-header", f"{rel}#{slug}",
                f"duplicate header '{raw}' under the same parent '{parent}' (anchor collision)"))
        else:
            seen.add(key)
        stack.append((level, raw))

    # Malformed headers: invisible to / breaking the ToC generator.
    for line in _nonfence_lines(text):
        if _MALFORMED_NOSPACE.match(line):
            out.append(StructureFinding(
                "malformed-header", f"{rel}#malformed",
                f"missing space after #: {line.strip()[:60]!r}"))
        elif _MALFORMED_EMPTY.match(line):
            out.append(StructureFinding(
                "malformed-header", f"{rel}#malformed-empty",
                f"empty header title: {line.strip()!r}"))
    return out


def scan_toc(rel: str, text: str) -> list[StructureFinding]:
    """Bidirectional ToC↔header check for a doc carrying a `<!-- TOC:START/END -->` block."""
    if _TOC_START not in text or _TOC_END not in text:
        return []
    block = text.split(_TOC_START, 1)[1].split(_TOC_END, 1)[0]
    toc_anchors = set(_TOC_LINK_RE.findall(block))

    # Header anchors with GitHub duplicate disambiguation (mirrors generator.generate_toc).
    seen: dict[str, int] = {}
    header_anchors: set[str] = set()
    for _level, raw in parse_headers(text):
        anchor = _slugify(raw)
        count = seen.get(anchor, 0)
        seen[anchor] = count + 1
        if count:
            anchor = f"{anchor}-{count}"
        header_anchors.add(anchor)

    out: list[StructureFinding] = []
    for anchor in sorted(toc_anchors - header_anchors):
        out.append(StructureFinding(
            "toc-dangling", f"{rel}#toc:{anchor}",
            f"ToC entry '#{anchor}' has no matching header"))
    for anchor in sorted(header_anchors - toc_anchors):
        out.append(StructureFinding(
            "toc-orphan", f"{rel}#hdr:{anchor}",
            f"header '#{anchor}' is missing from the ToC"))
    return out


def scan_dangling_allow(rel: str, gaps: set[int], allow: set[tuple[str, str]]) -> list[StructureFinding]:
    """A `structure-allow numbering-gap N` marker whose N is no longer a gap (stale marker)."""
    out: list[StructureFinding] = []
    for kind, locus in allow:
        if kind != "numbering-gap":
            continue
        if not locus.isdigit() or int(locus) not in gaps:
            out.append(StructureFinding(
                "dangling-allow", f"{rel}#allow-{locus}",
                f"structure-allow numbering-gap {locus} but {locus} is not a live gap "
                f"(stale marker — remove it)"))
    return out


def scan_heading_scheme(rel: str, text: str, allow: set[tuple[str, str]]) -> list[StructureFinding]:
    """Two-part heading-scheme integrity — the `Ch`/`§` convention (Council heading decision).

    For a doc carrying the `## Part I … / ## Part II …` spine (only the PLAYBOOK does today):
    every Part-I reference chapter must be `## ChN. <Title>`, sequential from Ch1 — a chapter
    missing its `ChN.` prefix, starting other than at Ch1, decreasing, duplicated, or gapped
    (gaps honour a co-located `chapter-gap` allow marker, mirroring the §18 numbering case) all
    fire. Part-II recipe numbering (`## N.`, §18 gap) is covered by scan_numbering, so Part II
    is NOT subject to the Ch-prefix rule here (its appendices/recipes are intentionally varied).
    A doc with no Part spine is skipped (region stays None). Precision-over-recall: detect-only.
    """
    out: list[StructureFinding] = []
    region: str | None = None
    chapters: list[int] = []
    for level, raw in parse_headers(text):
        if level == 2:
            m_part = _PART_RE.match(raw)
            if m_part:
                region = m_part.group(1)   # 'I' (Reference) or 'II' (Workflows)
                continue
            if region == "I":
                m = _CHAPTER_RE.match(raw)
                if m:
                    chapters.append(int(m.group(1)))
                else:
                    out.append(StructureFinding(
                        "heading-scheme", f"{rel}#chapter-noprefix",
                        f"Part I heading '{raw}' is not in `ChN.` form "
                        f"(a reference chapter must be `## ChN. <Title>`)"))
    # Sequence integrity over the chapter numbers (gap/dup logic mirrors scan_numbering).
    if chapters and chapters[0] != 1:
        out.append(StructureFinding(
            "heading-scheme", f"{rel}#chapter-{chapters[0]}",
            f"Part I chapters start at Ch{chapters[0]}, not Ch1"))
    prev: int | None = None
    for num in chapters:
        if prev is not None:
            if num == prev:
                out.append(StructureFinding(
                    "heading-scheme", f"{rel}#chapter-{num}",
                    f"chapter Ch{num} appears twice in the Part I spine"))
            elif num < prev:
                out.append(StructureFinding(
                    "heading-scheme", f"{rel}#chapter-{num}",
                    f"chapter Ch{num} out of sequence (follows Ch{prev})"))
            elif num > prev + 1:
                for missing in range(prev + 1, num):
                    if ("chapter-gap", str(missing)) in allow:
                        continue
                    out.append(StructureFinding(
                        "heading-scheme", f"{rel}#chapter-{missing}",
                        f"chapter Ch{missing} missing between Ch{prev} and Ch{num} "
                        f"(no structure-allow marker — intentional? add one; else renumber)"))
        prev = num
    return out


# --- scan (pure orchestration) ----------------------------------------------

def scan(repo_root: Path) -> list[StructureFinding]:
    """Run every sub-detector against the repo's living docs; one StructureFinding per locus.

    Read-only. An empty list = clean (the audit adapter synthesizes the `pass` Finding).
    A missing doc is skipped (presence is enforced elsewhere).
    """
    results: list[StructureFinding] = []
    for rel in _STRUCTURE_DOCS:
        p = repo_root / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        allow = parse_allow_markers(text)
        gaps = numbering_gaps(text)
        results.extend(scan_numbering(rel, text, allow))
        results.extend(scan_headers_scheme(rel, text))
        results.extend(scan_heading_scheme(rel, text, allow))
        results.extend(scan_toc(rel, text))
        results.extend(scan_dangling_allow(rel, gaps, allow))
    return results


def format_findings(results: list[StructureFinding]) -> str:
    """One flat clause per locus (markdown-table-safe — no `|`)."""
    return "; ".join(f"{r.category} {r.locus} ({r.detail})" for r in results).replace("|", "/")


def main() -> int:
    """Standalone CLI: scan the hub; print; exit 0 always (awareness layer, never a gate)."""
    results = scan(_REPO_ROOT)
    if not results:
        print("validate_doc_structure: OK — no structural rot (numbering / headers / ToC)")
        return 0
    print(f"validate_doc_structure: {len(results)} structural locus(es):")
    for r in results:
        print(f"  {r.category:>16}  {r.locus}  ->  {r.detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
