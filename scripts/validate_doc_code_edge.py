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

Phase-2 sub-arc 1 wired this as the `doc_code_edge` ADVISORY check in `audit.py` ALL_CHECKS
(WARN-only, never a gate; #194) via the `iter_doc_rule_ids` enumerator below. Still deferred:
pre-commit promotion (data-gated, ADR-89 OQ3), `staleness_signal`, the `::symbol` target leg
(via `reverse_dep_oracle.resolve_symbol`), the rebuildable index, and the real-annotation
rollout -- gated on the still-undesigned rule-ID NAMING scheme (ADR-89 OQ1 #1 / the #194
"declared rule-ID scheme" deliverable; an ADR-89 amendment / Council ruling, not a build-time
pick). The file-level edge + the four move-safety proofs remain the proven core.

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


def find_doc_sites(rule_id: str, doc_root: Path) -> list[Site]:
    """Locate `<!-- rule: <rule_id> -->` across `*.md` under `doc_root`, by content."""
    out: list[Site] = []
    for md in sorted(doc_root.rglob("*.md")):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        rel = md.relative_to(doc_root).as_posix()
        for i, line in enumerate(text.splitlines(), start=1):
            for m in DOC_RE.finditer(line):
                if m.group(1) == rule_id:
                    out.append(Site(rel, i))
    return out


def iter_doc_rule_ids(doc_root: Path, exclude_top: tuple[str, ...] = ()) -> set[str]:
    """Enumerate every `<!-- rule: ID -->` rule-ID across `*.md` under `doc_root`.

    Returns the set of unique IDs (location-free; pair with `resolve_edge` to locate sites).
    Same content-scan contract as `find_doc_sites` -- the ID is read from annotation CONTENT,
    never a stored path. `exclude_top` skips any `*.md` whose FIRST root-relative path
    component (a directory name, or a root-level filename like `JOURNAL.md`) is listed: the
    advisory check passes the test-fixture tree plus the immutable design-record trees
    (`docs/`, `JOURNAL.md`) that only DISCUSS the token syntax, so their illustrative
    `<!-- rule: ID -->` / `<!-- rule: PB-07 -->` examples never register as live edges.

    Asymmetry seed (Phase 2): `find_code_sites` uses `tokenize` to skip a `# rule: ID` buried
    in a string literal, but the doc side has NO equivalent guard against an illustrative token
    inside a markdown code fence or inline span (the regex does not respect fencing), so the
    live scan universe is bounded by `exclude_top` instead. A real doc-side guard (skip
    fenced/inline-code spans, or honor only tokens on/adjacent to a governed heading) is later
    work.
    """
    ids: set[str] = set()
    for md in sorted(doc_root.rglob("*.md")):
        rel = md.relative_to(doc_root)
        if exclude_top and rel.parts and rel.parts[0] in exclude_top:
            continue
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


def resolve_edge(rule_id: str, doc_root: Path, code_root: Path) -> EdgeResult:
    """Resolve the doc<->code edge for `rule_id`.

    A side that resolves to nothing -> `broken_edge` (the deterministic hard-FAIL the ADR
    requires). A duplicated rule-ID on either side -> `ambiguous`. Exactly one each ->
    `resolved`. `broken_edge` is checked first: an unresolved target is the hard failure.
    """
    doc_sites = tuple(find_doc_sites(rule_id, doc_root))
    code_sites = tuple(find_code_sites(rule_id, code_root))
    if not doc_sites or not code_sites:
        status = "broken_edge"
    elif len(doc_sites) > 1 or len(code_sites) > 1:
        status = "ambiguous"
    else:
        status = "resolved"
    return EdgeResult(rule_id, status, doc_sites, code_sites)


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
