#!/usr/bin/env python
"""validate_doc_code_edge.py -- #194 Phase-A spike: move-safe doc<->code edge resolver.

Proves the ADR-89 OQ1 corrected mechanism (rule-ID identity + path/AST resolution) is
MOVE-SAFE before any production build -- i.e. it does NOT reintroduce the path-rot the
codemap mechanism was rejected for.

Design under test:
  * Identity = rule-ID on BOTH sides: doc `<!-- rule: ID -->`, code `# rule: ID`. The edge
    tracks ID <-> ID.
  * Resolution = content lookup, and ONLY resolution. The resolver LOCATES the `# rule: ID`
    annotation by scanning comment tokens over the code tree; the path is a resolution-time
    lookup, NEVER the identity. A file move therefore must NOT break the edge -- the
    annotation travels with the code and the resolver re-finds it at its new path.

Two validation outcomes (ADR-89): `broken_edge` (a side resolves to nothing = deterministic
hard-FAIL) vs a resolved edge. `ambiguous` flags a duplicated rule-ID.

Phase-2 wired this as the `doc_code_edge` ADVISORY check in `audit.py` ALL_CHECKS (WARN-only,
never a gate; #194) via `iter_doc_rule_ids` + `scan_structural_integrity` below. The rule-ID
NAMING scheme is adopted (ADR-89 OQ1) and the #194 "Done when" landed: `build_edge_index` (the
derived rebuildable index) + `scan_structural_integrity` (L1 integrity -- dangling / code-orphan
/ duplicate). Still deferred: hard-gate promotion (data-gated, ADR-89 OQ3), `staleness_signal`,
the `::symbol` target leg (via `reverse_dep_oracle.resolve_symbol`), and the deferred-tail
annotation rollout (two-organ #201 / Tier-3 #202 / drift-guard #203). The file-level edge + the
move-safety proofs remain the proven core.

Layer-2 / read-only (ADR-28/36): reads `*.md` + `*.py` under the given roots; writes
NOTHING; never orchestrates; never gates (the spike CLI exits 0 -- awareness only).

Output is ASCII only (a Windows cp1252 console crashes on `<->`/arrow glyphs); Unicode
edge markers live in the markdown docs, never in this script's printed strings.

Usage:  python scripts/validate_doc_code_edge.py <rule-id>
                 [--doc-root .] [--code-root scripts]
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# Rule-ID charset: alnum plus `_`, `.`, `-` (room for ids like `PLAYBOOK.S5-1`).
_ID = r"[A-Za-z0-9_.-]+"
DOC_RE = re.compile(r"<!--\s*rule:\s*(" + _ID + r")\s*-->")
CODE_RE = re.compile(r"#\s*rule:\s*(" + _ID + r")")


@dataclass(frozen=True)
class Site:
    """One annotation hit. `file` is root-relative (forward slashes); `line` is 1-based.

    (Phase-2 seed: a `symbol` field can be added here when the `::symbol` target leg lands;
    the spike proves the file leg, which is where move-safety is decided.)
    """

    file: str
    line: int


@dataclass(frozen=True)
class EdgeResult:
    rule_id: str
    status: str  # "resolved" | "broken_edge" | "ambiguous"
    doc_sites: tuple[Site, ...]
    code_sites: tuple[Site, ...]


@dataclass(frozen=True)
class StructuralFinding:
    """One L1 structural-integrity defect (#194). `kind` is one of:
    `dangling_doc` (declared, no code impl) | `code_orphan` (code annotation, no declaration =
    code->nonexistent-rule) | `duplicate_doc` (>1 doc site) | `duplicate_code` (>1 code site)."""

    rule_id: str
    kind: str
    doc_sites: tuple[Site, ...]
    code_sites: tuple[Site, ...]


def find_doc_sites(rule_id: str, doc_root: Path,
                   include: tuple[str, ...] | None = None) -> list[Site]:
    """Locate `<!-- rule: <rule_id> -->` by content, scoped to the declaration registry.

    `include` is the registry-scoped declaration-doc list (`declaration_docs:` in
    `ecosystem/doc-code-edge.yaml`) -- the SAME scope `iter_doc_rule_ids` enumerates over. When
    given, ONLY those repo-relative docs are scanned, so a real rule-ID quoted in PROSE in a
    NON-declaration doc (an immutable audit, ARCHITECTURE, a record) is NOT counted as a doc-site.
    This closes the scan/resolve ASYMMETRY that made a rule `ambiguous` when an audit file merely
    discussed its `<!-- rule: ... -->` token (the #194 doc-site-scoping fix): enumeration was
    registry-scoped while resolution scanned every `*.md`. `include=None` is the unscoped
    spike/mechanism mode (scan every `*.md` under `doc_root`) used by the move-safety fixtures;
    the LIVE check (`audit.check_doc_code_edge`) and the coverage gate ALWAYS pass the registry.
    A listed path that does not exist is skipped (fail-soft, same as `iter_doc_rule_ids`).
    """
    out: list[Site] = []
    if include is None:
        items = [(md, md.relative_to(doc_root).as_posix())
                 for md in sorted(doc_root.rglob("*.md"))]
    else:
        items = [(doc_root / rel, rel) for rel in include]
    for md, rel in items:
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            for m in DOC_RE.finditer(line):
                if m.group(1) == rule_id:
                    out.append(Site(rel, i))
    return out


def iter_doc_rule_ids(doc_root: Path, include: tuple[str, ...] = ()) -> set[str]:
    """Enumerate every `<!-- rule: ID -->` rule-ID across the declaration docs in `include`.

    `include` is the registry-scoped include-list of repo-relative doc paths (the
    `declaration_docs:` list in `ecosystem/doc-code-edge.yaml`); the scan reads ONLY those
    files, each resolved against `doc_root`. Returns the set of unique IDs (location-free; pair
    with `resolve_edge` to locate sites). Same content-scan contract as `find_doc_sites` -- the
    ID is read from annotation CONTENT, never a stored path. A listed path that does not exist
    is skipped (fail-soft).

    Registry-scoped (replaces the earlier hardcoded record-tree exclude-list): the live scan
    universe is exactly the docs that AUTHORITATIVELY declare an enforced rule, so illustrative
    `<!-- rule: ID -->` tokens elsewhere (immutable design records, teaching sections, the test
    fixtures) never register as live edges. Two complementary guards keep examples out:
    (1) this include-list bounds WHICH files are scanned; (2) teaching tokens use the
    angle-bracket placeholder form `<!-- rule: <domain>-<slug> -->`, whose `<`/`>` fall outside
    the ID charset, so even inside a listed doc a placeholder is never matched as a live edge.
    """
    ids: set[str] = set()
    for rel in include:
        md = doc_root / rel
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in DOC_RE.finditer(text):
            ids.add(m.group(1))
    return ids


def find_code_sites(rule_id: str, code_root: Path) -> list[Site]:
    """Locate `# rule: <rule_id>` across `*.py` under `code_root`, by content.

    Matches only real COMMENT tokens (via `tokenize`), so a `# rule: ID` embedded in a
    string literal is NOT a false hit. The annotation is found by CONTENT -- never by a
    stored path -- which is the whole point of the move-safety proof. (A line-regex scan is
    the documented fallback if a file is untokenizable; such files are skipped here.)
    """
    out: list[Site] = []
    for py in sorted(code_root.rglob("*.py")):
        try:
            src = py.read_text(encoding="utf-8")
        except OSError:
            continue
        rel = py.relative_to(code_root).as_posix()
        try:
            tokens = list(tokenize.generate_tokens(io.StringIO(src).readline))
        except (tokenize.TokenError, SyntaxError, IndentationError):
            continue
        for tok in tokens:
            if tok.type != tokenize.COMMENT:
                continue
            m = CODE_RE.search(tok.string)
            if m and m.group(1) == rule_id:
                out.append(Site(rel, tok.start[0]))
    return out


def iter_code_rule_ids(code_root: Path) -> set[str]:
    """Enumerate every `# rule: ID` across `*.py` under `code_root` (real COMMENT tokens only).

    The code-side half of the derived edge index, symmetric to `iter_doc_rule_ids`. Same
    tokenize-based, content-only contract as `find_code_sites` -- a `# rule: ID` inside a string
    literal is never collected, an untokenizable file is skipped (fail-soft). Returns the set of
    unique code-side IDs (location-free; pair with `find_code_sites` to locate each).
    """
    ids: set[str] = set()
    for py in sorted(code_root.rglob("*.py")):
        try:
            src = py.read_text(encoding="utf-8")
        except OSError:
            continue
        try:
            tokens = list(tokenize.generate_tokens(io.StringIO(src).readline))
        except (tokenize.TokenError, SyntaxError, IndentationError):
            continue
        for tok in tokens:
            if tok.type != tokenize.COMMENT:
                continue
            m = CODE_RE.search(tok.string)
            if m:
                ids.add(m.group(1))
    return ids


def resolve_edge(rule_id: str, doc_root: Path, code_root: Path,
                 include: tuple[str, ...] | None = None,
                 multi_site: dict[str, int] | None = None) -> EdgeResult:
    """Resolve the doc<->code edge for `rule_id`.

    A side that resolves to nothing -> `broken_edge` (the deterministic hard-FAIL the ADR
    requires). A duplicated rule-ID on either side -> `ambiguous`. Exactly one each ->
    `resolved`. `broken_edge` is checked first: an unresolved target is the hard failure.

    `include` scopes the DOC-side resolution to the declaration registry (see `find_doc_sites`);
    the live check + coverage gate pass it so a prose mention in a non-declaration doc cannot make
    a real edge `ambiguous`. `include=None` keeps the unscoped spike behaviour (scan all `*.md`).

    `multi_site` (ADR-90 resolver-allows-N) is the declared expected code-site count per rule-ID:
    a rule legitimately enforced in N `# rule:`-able code organs maps `rule_id -> N`. Such a rule
    `resolves` iff it has EXACTLY one doc site AND EXACTLY `N` code sites; any other code count
    (incl. N+/-1) stays `ambiguous`, so the duplicate-guard keeps its teeth for the declared
    organs too. The doc side is ALWAYS 1:1 (multiplicity is a code-side property). A rule absent
    from `multi_site` keeps the strict `>1 -> ambiguous` 1:1 duplicate-guard, unchanged.
    """
    doc_sites = tuple(find_doc_sites(rule_id, doc_root, include))
    code_sites = tuple(find_code_sites(rule_id, code_root))
    expected = (multi_site or {}).get(rule_id)
    if not doc_sites or not code_sites:
        status = "broken_edge"
    elif expected is not None:
        # Declared multi-site rule: resolve at EXACTLY the declared code-site count + one doc site.
        status = ("resolved" if (len(doc_sites) == 1 and len(code_sites) == expected)
                  else "ambiguous")
    elif len(doc_sites) > 1 or len(code_sites) > 1:
        status = "ambiguous"
    else:
        status = "resolved"
    return EdgeResult(rule_id, status, doc_sites, code_sites)


def build_edge_index(doc_root: Path, code_root: Path,
                     include: tuple[str, ...],
                     multi_site: dict[str, int] | None = None) -> dict[str, EdgeResult]:
    """The derived, rebuildable edge index: every rule-ID on EITHER side -> its `EdgeResult`.

    REBUILT from source on every call -- there is no hand-maintained manifest (ADR-88 principle
    3: the model reads the graph, never holds it; the fit-check's "no central manifest ->
    nothing to drift"). Reuses `resolve_edge` per ID, so it adds no new scan logic. `include`
    scopes the DOC side to the declaration registry (same contract as `resolve_edge`); the code
    side is the full `# rule:` enumeration under `code_root`, so a code-only orphan
    (code->nonexistent-rule) is present in the index as a `broken_edge` (doc side empty).
    `multi_site` (ADR-90) threads through to `resolve_edge` so a declared multi-site rule
    resolves at its expected count rather than as `ambiguous`.
    """
    ids = iter_doc_rule_ids(doc_root, include) | iter_code_rule_ids(code_root)
    return {rid: resolve_edge(rid, doc_root, code_root, include, multi_site)
            for rid in sorted(ids)}


def scan_structural_integrity(doc_root: Path, code_root: Path,
                              include: tuple[str, ...],
                              multi_site: dict[str, int] | None = None) -> list[StructuralFinding]:
    """L1 structural-integrity scan over the rebuildable index (the #194 "Done when"). DETECT-first.

    One `StructuralFinding` per defect in the declared doc<->code edge:
      * `dangling_doc`   -- a declared rule-ID with NO `# rule:` code site (declared-unimplemented).
      * `code_orphan`    -- a `# rule:` annotation whose ID is declared in NO declaration doc
                            (code->nonexistent-rule) -- the direction `check_doc_code_edge`'s
                            doc-side resolution structurally cannot see.
      * `duplicate_doc`  -- the same rule-ID on >1 doc site.
      * `duplicate_code` -- the same rule-ID on >1 code site.
    A clean resolved edge (exactly one doc + one code site) yields NO finding. Read-only; never
    raises, never gates (advisory-first; hard-gate promotion is data-gated, ADR-89 OQ3).
    """
    index = build_edge_index(doc_root, code_root, include, multi_site)
    findings: list[StructuralFinding] = []
    for rid in sorted(index):
        r = index[rid]
        # A declared multi-site rule (ADR-90) tolerates exactly its expected code count; an
        # undeclared rule tolerates 1. Code sites ABOVE that threshold are real over-duplication.
        code_threshold = (multi_site or {}).get(rid, 1)
        if r.doc_sites and not r.code_sites:
            findings.append(StructuralFinding(rid, "dangling_doc", r.doc_sites, r.code_sites))
        elif r.code_sites and not r.doc_sites:
            findings.append(StructuralFinding(rid, "code_orphan", r.doc_sites, r.code_sites))
        if len(r.doc_sites) > 1:
            findings.append(StructuralFinding(rid, "duplicate_doc", r.doc_sites, r.code_sites))
        if len(r.code_sites) > code_threshold:
            findings.append(StructuralFinding(rid, "duplicate_code", r.doc_sites, r.code_sites))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate_doc_code_edge",
        description="Resolve a doc<->code rule-ID edge (read-only spike; exits 0).",
    )
    parser.add_argument("rule_id")
    parser.add_argument("--doc-root", default=str(_REPO_ROOT))
    parser.add_argument("--code-root", default=str(_SCRIPTS_DIR))
    args = parser.parse_args(argv)

    result = resolve_edge(args.rule_id, Path(args.doc_root), Path(args.code_root))
    print(f"{result.rule_id}: {result.status}")
    for site in result.doc_sites:
        print(f"  doc:  {site.file}:{site.line}")
    for site in result.code_sites:
        print(f"  code: {site.file}:{site.line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
