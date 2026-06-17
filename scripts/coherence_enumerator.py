#!/usr/bin/env python
"""coherence_enumerator.py — the reconciliation enumerator (coherence spine v1).

The load-bearing half of the dependency-coherence spine. Given a flagged stale
edge (a dependent doc whose spec advanced a version), this DETERMINISTICALLY
extracts every candidate reference site in the dependent, so a downstream LLM can
verdict EACH one. The split is the whole point:

  * completeness is DETERMINISTIC — this extractor over-extracts but never misses
    a real site (a missed walkthrough step or an un-updated diagram cannot pass
    silently);
  * judgment is SEMANTIC — an LLM (the `check-against-spec` skill) verdicts the
    list this produces; it can never omit a site that exists here.

Over-extraction is fine; MISSING a real site is the failure mode. The categories
deliberately overlap (a line can surface under more than one lens).

Flag contract consumed (Prompt A's checker produces it; build against a stub):
  {dependent_path, spec_path, old_version, new_version}

Layer-2 / read-only contract (ADR-28/36): reads the two in-repo docs named by the
flag; writes NOTHING; never orchestrates; never gates. The CLI prints a flat
by-category checklist skeleton to stdout (the agent fills verdicts inline and puts
the result in the re-stamp COMMIT MESSAGE — never a JSON file) and exits 0.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import validate_reconciliation as vr

# --- categories -------------------------------------------------------------
# Order is the checklist's display order. Every category is always rendered,
# empties stated explicitly ("none found").
CATEGORIES = ("sections", "walkthrough_steps", "diagrams", "commands", "summaries")

# Fenced-block info-strings that read as a diagram vs a command. An UNKNOWN /
# empty info-string falls back to `diagrams` (over-extract — a diagram drawn in a
# bare fence must not be missed).
_DIAGRAM_LANGS = {
    "mermaid", "flowchart", "graph", "sequencediagram", "gantt", "classdiagram",
    "statediagram", "statediagram-v2", "erdiagram", "journey", "mindmap",
    "timeline", "gitgraph", "dot", "plantuml",
}
_SHELL_LANGS = {
    "powershell", "pwsh", "ps1", "ps", "bash", "sh", "shell", "shell-session",
    "console", "zsh", "bat", "cmd", "dos",
}

# `\d+.` then a space OR end-of-line — an EMPTY item ("2." on its own line) is
# still a list marker, so it does not fragment the surrounding step block. The
# `(?:\s|$)` (not bare `\.`) keeps decimals like "3.14" from matching.
_ORDERED_ITEM = re.compile(r"^(\s*)\d+\.(?:\s|$)")
_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([\w-]*)\s*$")
_VERSION_TOKEN = re.compile(r"\bv\d+(?:\.\d+)*\b")

# Inline command / invocation patterns (single-line sites).
_COMMAND_PATTERNS = (
    re.compile(r"\brun\s+`?[\w./-]"),          # `run <command>`
    re.compile(r"\b(?:python|py)\s+[\w./-]"),  # python / py invocations
    re.compile(r"\bGet-[A-Z]\w+"),             # PowerShell cmdlets
    re.compile(r"\bscripts/[\w/]+\.py\b"),     # repo script references
    re.compile(r"(?:^|[\s(`])/[a-z][\w-]{2,}\b"),  # /slash-commands
)

_MAX_ANCHOR = 78


@dataclass(frozen=True)
class Site:
    """One candidate reference site the LLM must verdict.

    line_start/line_end are 1-based and inclusive. `anchor` is a sanitized,
    single-line snippet safe to embed inside a triple-backtick fence (no literal
    backticks or newlines), so the rendered checklist can itself be fenced for the
    operator to copy into browser chat (CLAUDE.md §4 render-layer rule).
    """

    category: str
    line_start: int
    line_end: int
    anchor: str
    text: str = field(repr=False, default="")


def _sanitize_anchor(s: str) -> str:
    """One-line, fence-safe, truncated snippet for the checklist."""
    s = s.replace("`", "").replace("\n", " ").strip()
    s = re.sub(r"\s+", " ", s)
    if len(s) > _MAX_ANCHOR:
        s = s[: _MAX_ANCHOR - 3].rstrip() + "..."
    return s


def read_spec_version(spec_text: str) -> str:
    """Parse the spec's CURRENT version from its frontmatter, LIVE — never hardcoded.

    Delegates to the single coherence-spine parser (`validate_reconciliation.parse_spec_version`)
    so the checker, the enumerator, and the nudge never drift to three regexes (#172 dedup).
    The enumerator surfaces the RAW token verbatim (full-text, e.g. "5.2" / "v5.4.1") for the
    display checklist — the checker's numeric normalization is its own consumer-layer concern,
    not duplicated here. Returns the raw value, or "" if no Version line is present.
    """
    return vr.parse_spec_version(spec_text)


def _spec_key_terms(spec_name: str) -> tuple[re.Pattern, ...]:
    """Detection patterns for mentions of the spec, derived from its filename stem.

    General (not hardcoded to one edge): the SCREAMING_SNAKE family prefix
    (`HANDOFF_*` from `HANDOFF_PROCESS`) matched case-sensitively, plus the full
    stem's punctuation variants matched case-insensitively. The distinctive forms
    are the structurally-meaningful mentions; lowercase prose words (e.g. a bare
    "handoff") are intentionally left to the LLM's additive escape, not dragged in
    here as noise.
    """
    pats: list[re.Pattern] = []
    prefix = spec_name.split("_")[0]
    if prefix.isupper() and len(prefix) >= 3:
        # the post-underscore char may be a digit too (e.g. a FOO_2025 family member)
        pats.append(re.compile(rf"\b{re.escape(prefix)}_[A-Z0-9][A-Z0-9_]*\b"))
    stem_variants = {
        spec_name,
        spec_name.replace("_", "-"),
        spec_name.replace("_", " "),
    }
    for v in stem_variants:
        pats.append(re.compile(rf"\b{re.escape(v)}\b", re.IGNORECASE))
    return tuple(pats)


def _find_fenced_blocks(lines: list[str]) -> list[tuple[int, int, str]]:
    """Return (start, end, info) for each fenced block — 0-based, inclusive."""
    blocks: list[tuple[int, int, str]] = []
    i = 0
    n = len(lines)
    while i < n:
        m = _FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        ticks, info = m.group(2), m.group(3)
        start = i
        j = i + 1
        while j < n:
            cm = _FENCE.match(lines[j])
            # A closing fence: same-or-more ticks of the same char, no info string.
            if cm and cm.group(2)[0] == ticks[0] and len(cm.group(2)) >= len(ticks) and not cm.group(3):
                break
            j += 1
        end = j if j < n else n - 1
        blocks.append((start, end, info.lower()))
        i = end + 1
    return blocks


def _find_ordered_blocks(lines: list[str], skip: set[int]) -> list[tuple[int, int]]:
    """Group consecutive ordered-list items (with continuations) into step blocks.

    A block runs from the first `N. ` marker through its indented continuation /
    interleaving blank lines, closing at the first non-indented, non-blank line
    that is not itself an ordered item. Returns (start, end) 0-based, inclusive.
    Lines in `skip` (inside fenced blocks) are never list markers.
    """
    blocks: list[tuple[int, int]] = []
    n = len(lines)
    i = 0
    while i < n:
        if i in skip or not _ORDERED_ITEM.match(lines[i]):
            i += 1
            continue
        start = i
        last_content = i
        j = i + 1
        while j < n:
            line = lines[j]
            if not line.strip():            # blank — tentatively inside; don't move last_content
                j += 1
                continue
            if j in skip:
                break
            if _ORDERED_ITEM.match(line):   # next item — same block
                last_content = j
                j += 1
                continue
            if line[:1].isspace():          # indented continuation
                last_content = j
                j += 1
                continue
            break                           # non-indented prose — block ends
        blocks.append((start, last_content))
        i = max(j, last_content + 1)
    return blocks


def extract_sites(dependent_text: str, spec_name: str) -> dict[str, list[Site]]:
    """THE HEART. Deterministically extract every candidate reference site.

    Returns a category -> [Site] map for every category in CATEGORIES (empty lists
    for categories with no hits). Over-extracts by design; the only contract that
    matters is that no real site is missed.
    """
    lines = dependent_text.splitlines()
    out: dict[str, list[Site]] = {c: [] for c in CATEGORIES}

    fenced = _find_fenced_blocks(lines)
    fenced_line_idx = {idx for (s, e, _info) in fenced for idx in range(s, e + 1)}

    # diagrams + fenced commands
    for (s, e, info) in fenced:
        body = lines[s + 1] if e > s else lines[s]
        anchor = _sanitize_anchor(f"{info or 'fence'}: {body}")
        # shell-ish fences are command sites; diagram langs AND unknown/empty info
        # both fall to diagrams (over-extract — never miss a bare-fence diagram).
        cat = "commands" if info in _SHELL_LANGS else "diagrams"
        out[cat].append(Site(cat, s + 1, e + 1, anchor, "\n".join(lines[s:e + 1])))

    # walkthrough steps
    for (s, e) in _find_ordered_blocks(lines, fenced_line_idx):
        out["walkthrough_steps"].append(
            Site("walkthrough_steps", s + 1, e + 1, _sanitize_anchor(lines[s]), "\n".join(lines[s:e + 1]))
        )

    # sections (spec-name / key-term mentions) + inline commands + summaries
    key_terms = _spec_key_terms(spec_name)
    for idx, line in enumerate(lines):
        if idx in fenced_line_idx:
            continue
        lineno = idx + 1
        if any(p.search(line) for p in key_terms):
            out["sections"].append(Site("sections", lineno, lineno, _sanitize_anchor(line), line))
        if any(p.search(line) for p in _COMMAND_PATTERNS):
            out["commands"].append(Site("commands", lineno, lineno, _sanitize_anchor(line), line))
        if _VERSION_TOKEN.search(line):
            out["summaries"].append(Site("summaries", lineno, lineno, _sanitize_anchor(line), line))

    # dedup within each category by (start, end), preserving order
    for cat, sites in out.items():
        seen: set[tuple[int, int]] = set()
        deduped = []
        for st in sites:
            key = (st.line_start, st.line_end)
            if key not in seen:
                seen.add(key)
                deduped.append(st)
        out[cat] = deduped
    return out


def enumerate_from_flag(flag: dict) -> dict:
    """Entry point. Reads the flagged files, extracts sites. Stub-flag compatible.

    `flag` is the {dependent_path, spec_path, old_version, new_version} contract
    Prompt A produces. Returns a structured result; rendering is `format_checklist`.
    """
    dependent_path = Path(flag["dependent_path"])
    spec_path = Path(flag["spec_path"])
    dependent_text = dependent_path.read_text(encoding="utf-8")
    spec_text = spec_path.read_text(encoding="utf-8")
    spec_name = spec_path.stem
    return {
        "flag": dict(flag),
        "spec_name": spec_name,
        "spec_version_current": read_spec_version(spec_text),
        "sites": extract_sites(dependent_text, spec_name),
    }


def enumerate_from_edge(edge: vr.Edge, repo_root: Path | str = ".") -> dict:
    """Enumerate sites for one REAL reconciliation Edge — Prompt A's `enumerate_edges` output.

    This is the A->B seam: the enumerator consumes the checker's real `Edge` contract
    ({dependent_path, spec_path, old_version, new_version}) instead of a hand-built stub
    flag. The Edge carries repo-relative paths; they are resolved against `repo_root` and
    handed to `enumerate_from_flag`. Read-only.
    """
    root = Path(repo_root)
    flag = {
        "dependent_path": str(root / edge.dependent_path),
        "spec_path": str(root / edge.spec_path),
        "old_version": edge.old_version,
        "new_version": edge.new_version,
    }
    return enumerate_from_flag(flag)


def enumerate_repo(repo_root: Path | str = ".") -> list[dict]:
    """Drive the whole deterministic spine over a repo: every checker-resolved edge enumerated.

    A's `enumerate_edges(repo_root)` yields one Edge per well-formed, known-spec edge (the real
    output that replaces B's stub flag); each is enumerated into a by-category site map. Returns
    one result dict per edge (empty list when no reconciliation edges are declared). Read-only.
    """
    root = Path(repo_root)
    return [enumerate_from_edge(edge, root) for edge in vr.enumerate_edges(root)]


_CATEGORY_LABELS = {
    "sections": "sections (spec-name / key-term mentions)",
    "walkthrough_steps": "walkthrough_steps (numbered / sequential procedures)",
    "diagrams": "diagrams (fenced blocks)",
    "commands": "commands (slash-commands / CLI invocations)",
    "summaries": "summaries (anchored version-references)",
}


def format_checklist(result: dict) -> str:
    """Render the FLAT by-category checklist SKELETON (the deliverable's shape).

    Flat text only — no markdown tables, no box-drawing, no triple-backticks inside
    (so the agent can wrap the whole thing in a code fence per CLAUDE.md §4 when
    surfacing it). Categories are ALWAYS rendered; empties stated explicitly. Each
    site carries an empty `verdict:` slot where `fine` (no change needed) is a
    first-class verdict. A final additive-only section lets the LLM net anchor-less
    sites the deterministic pass cannot see — it may ADD, never drop, sites.
    """
    flag = result["flag"]
    sites = result["sites"]
    total = sum(len(v) for v in sites.values())
    lines = [
        "COHERENCE RECONCILIATION CHECKLIST",
        f"edge: {flag.get('dependent_path')}  <-reconciled_with->  {flag.get('spec_path')}",
        f"spec version: {flag.get('old_version')} -> {flag.get('new_version')}  "
        f"(spec file currently reads: {result.get('spec_version_current') or 'n/a'})",
        f"deterministically extracted sites: {total}",
        "",
        "Verdict EACH site below: stale | fine | not-relevant   "
        "(+ transclusion-candidate if verbatim-duplicated from the spec).",
        "'fine' (no change needed) is a first-class verdict. Every extracted site MUST get a "
        "verdict; none may be dropped.",
        "",
    ]
    for cat in CATEGORIES:
        cat_sites = sites.get(cat, [])
        label = _CATEGORY_LABELS.get(cat, cat)
        if not cat_sites:
            lines.append(f"== {label} ==  [none found]")
            lines.append("")
            continue
        lines.append(f"== {label} ==  [{len(cat_sites)} found]")
        for st in cat_sites:
            loc = f"L{st.line_start}" if st.line_start == st.line_end else f"L{st.line_start}-{st.line_end}"
            lines.append(f"- {loc}  <<{st.anchor}>>")
            lines.append("    verdict: ___    (stale | fine | not-relevant; + transclusion-candidate)")
        lines.append("")
    lines.append("== additional (LLM-noticed; ADDITIVE ONLY) ==")
    lines.append(
        "The extractor cannot see anchor-less spec restatements / semantic paraphrases that carry "
        "no detectable key-term. Add any you notice here. You may ADD sites; you may NEVER drop a "
        "site extracted above."
    )
    lines.append("- (none / list here)    verdict: ___")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Deterministically enumerate candidate reconciliation sites in a "
        "dependent doc (read-only; prints a checklist skeleton to stdout)."
    )
    ap.add_argument("--dependent", required=True, help="path to the dependent doc")
    ap.add_argument("--spec", required=True, help="path to the spec doc")
    ap.add_argument("--old-version", default="", help="spec version before the bump")
    ap.add_argument("--new-version", default="", help="spec version after the bump")
    args = ap.parse_args(argv)

    # Anchors echo the source markdown's Unicode (arrows, mid-dots); a Windows
    # console defaults to cp1252 and would crash on print. Force UTF-8 stdout.
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

    flag = {
        "dependent_path": args.dependent,
        "spec_path": args.spec,
        "old_version": args.old_version,
        "new_version": args.new_version,
    }
    try:
        result = enumerate_from_flag(flag)
    except OSError as e:  # unreadable path — fail soft, never wedge a caller
        print(f"coherence_enumerator: could not read flagged files: {e}", file=sys.stderr)
        return 0
    print(format_checklist(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
