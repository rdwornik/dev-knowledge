#!/usr/bin/env python
"""validate_reconciliation.py — coherence-spine reconciliation checker (v1).

The deterministic half of the coherence spine: a dependent doc declares which spec
version it was last reconciled against via a `reconciled_with: <spec-id>@<version>`
frontmatter edge; this checker resolves the spec's CURRENT version from a registry and
FAILs when the declared version lags. It is the trigger that turns "the spec moved and a
dependent still claims the old version" from invisible drift into a gating Finding.

Generic by construction (reads the frontmatter graph, compares each declared edge) but in
v1 exactly ONE edge is declared in the repo:
  docs/handoffs/README.md  reconciled_with  handoff-process@<HANDOFF_PROCESS.md Version>.

Status model (the audit adapter, scripts/audit.py check_reconciled_versions, maps these):
  - declared != current                         -> 'mismatch'    -> Finding FAIL (fail-closed)
  - frontmatter `reconciled_with` malformed     -> 'malformed'   -> Finding WARN (fail-open)
  - spec-id not in the registry / spec absent / -> 'unknown-spec'-> Finding WARN  (its own
    spec version unparseable                                                       error)
  - declared == current                         -> 'match'       -> contributes to PASS
A mismatch is the only FAIL: a checker that cannot read its own inputs WARNs (fail-open on
its own error), never blocks. The spec version is read LIVE (never hardcoded).

Prompt-B contract (the reconciliation enumerator consumes this): `enumerate_edges(root)`
returns one `Edge(dependent_path, spec_path, old_version, new_version)` per well-formed,
known-spec edge — old = declared in the dependent, new = the spec's current version.

Read-only (Layer-2, ADR-28/36): reads docs + the spec file; writes NOTHING; never gates by
exit code (the audit adapter owns the Finding; this module's CLI exits 0 always).
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# Dirs pruned from the dependent scan: VCS internals, nested CC worktree checkouts
# (full duplicate trees), vendored deps, and immutable/aborted/in-progress handoff
# bundles. `archive` is matched by prefix. Mirrors the exclude sets in audit.py /
# verify_handoff_probes.py so a duplicate copy of a dependent cannot double-report.
_EXCLUDE_DIRS = {".git", ".claude", "node_modules", "aborted", "in-progress"}


@dataclass(frozen=True)
class SpecSource:
    """A spec whose live version is the authority for any edge that names it.

    The version is read LIVE from the spec file via the single coherence-spine parser
    `parse_spec_version` (never a hardcoded token); a SpecSource carries no parser of its
    own — there is exactly ONE spec-version reader for the whole spine (#172 dedup)."""
    spec_id: str
    path: str                       # repo-relative


# The live spec registry. Add a row when a new spec becomes a reconciliation authority.
_SPEC_REGISTRY: dict[str, SpecSource] = {
    "handoff-process": SpecSource(
        "handoff-process",
        "protocols/HANDOFF_PROCESS.md",
    ),
}


@dataclass(frozen=True)
class Edge:
    """The Prompt-B contract: one resolved reconciliation edge (well-formed, known spec)."""
    dependent_path: str             # repo-relative dependent doc
    spec_path: str                  # repo-relative spec file
    old_version: str                # version the dependent declares it reconciled against
    new_version: str                # the spec's current (live) version


@dataclass(frozen=True)
class ReconResult:
    dependent_path: str             # repo-relative
    spec_id: str                    # parsed spec id (or the raw value when malformed)
    status: str                     # 'match' | 'mismatch' | 'malformed' | 'unknown-spec'
    declared: str                   # version declared in the dependent (or "" )
    current: str                    # spec's current version (or "" / reason)


# --- frontmatter + version parsing (pure) -----------------------------------

def _frontmatter(text: str) -> Optional[dict]:
    """The YAML frontmatter mapping, or None when absent/unclosed/not-a-mapping."""
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def parse_reconciled_with(text: str) -> Optional[str]:
    """The raw `reconciled_with` frontmatter value, or None when the key is absent."""
    fm = _frontmatter(text)
    if fm is None:
        return None
    val = fm.get("reconciled_with")
    return str(val) if val is not None else None


_EDGE_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+)@(\d+(?:\.\d+)*)\s*$")


def split_edge(raw: str) -> Optional[tuple[str, str]]:
    """Parse a `<spec-id>@<version>` value into (spec_id, version), or None if malformed."""
    m = _EDGE_RE.match(raw)
    return (m.group(1), m.group(2)) if m else None


def norm_version(raw: str) -> tuple[int, ...]:
    """Dotted version to an int tuple, trailing zeros stripped so 5.2 == 5.2.0."""
    parts = [int(p) for p in raw.split(".") if p.isdigit()]
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


_VERSION_LINE_RE = re.compile(r"^\s*Version:\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)
_NUMERIC_VERSION_RE = re.compile(r"v?(\d+(?:\.\d+)*)")


def parse_spec_version(text: str) -> str:
    """The spec's declared version token, read LIVE from its `Version:` line — TOLERANT.

    The SINGLE spec-version reader for the whole coherence spine (#172 dedup): one regex,
    three consumers. Returns the raw token verbatim (e.g. "5.2", "v5.4.1"), or "" if no
    Version line. Consumers normalize as they need — this checker numeric-normalizes for
    version comparison (`spec_current_version`); the enumerator surfaces the raw token for
    its display checklist (`coherence_enumerator.read_spec_version`); the nudge compares two
    raw tokens for equality. The capture scope is deliberately TOLERANT (full text after the
    colon, not numeric-only) so the full-text consumer is not forced through a numeric regex.
    """
    m = _VERSION_LINE_RE.search(text)
    return m.group(1).strip() if m else ""


def _numeric_version(raw: str) -> str:
    """Strip a leading `v` and keep the dotted-numeric core ("v5.4.1" -> "5.4.1"); "" if none."""
    m = _NUMERIC_VERSION_RE.match(raw.strip())
    return m.group(1) if m else ""


def spec_version_numeric(text: str) -> str:
    """The spec version in COMPARISON form, from spec TEXT: numeric, leading `v` stripped.

    The single normalized form both version-EQUALITY consumers share — this checker (does the
    declared version match the spec's current?) and the forgotten-bump nudge (did a content
    edit leave the numeric version unchanged?). Comparing the numeric core, not raw text, is
    what makes a cosmetic `v5.2`->`5.2` edit NOT masquerade as a real version change. The
    enumerator, by contrast, DISPLAYS the raw `parse_spec_version` token. Returns "" if no
    parseable numeric version is present."""
    return _numeric_version(parse_spec_version(text))


def spec_current_version(repo_root: Path, spec: SpecSource) -> Optional[str]:
    """The spec's current version, numeric-normalized, read live; None if absent/unparseable.

    Reads the live spec file and returns its `spec_version_numeric` comparison form — A's
    consumer-layer normalization over the shared `parse_spec_version`, NOT a second parser
    (#172 dedup)."""
    p = repo_root / spec.path
    if not p.exists():
        return None
    return spec_version_numeric(p.read_text(encoding="utf-8", errors="replace")) or None


# --- discovery + reconcile (pure) -------------------------------------------

def discover_dependents(repo_root: Path) -> list[tuple[str, str]]:
    """Every repo .md that declares `reconciled_with`, as (repo-relative path, raw value).

    Walks the tree pruning _EXCLUDE_DIRS (VCS/worktree/vendor/immutable bundles) so a
    duplicate copy of a dependent cannot double-report. Deterministic (sorted)."""
    out: list[tuple[str, str]] = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames
                       if d not in _EXCLUDE_DIRS and not d.startswith("archive")]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            fp = Path(dirpath) / fn
            try:
                text = fp.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            raw = parse_reconciled_with(text)
            if raw is not None:
                out.append((fp.relative_to(repo_root).as_posix(), raw))
    return sorted(out)


# rule: coherence-spec-reconciled
def reconcile(repo_root: Path) -> list[ReconResult]:
    """Classify every declared reconciliation edge against live spec state. Read-only."""
    results: list[ReconResult] = []
    for rel, raw in discover_dependents(repo_root):
        parsed = split_edge(raw)
        if parsed is None:
            results.append(ReconResult(rel, raw, "malformed", "",
                                       "reconciled_with not '<spec-id>@<version>'"))
            continue
        spec_id, declared = parsed
        spec = _SPEC_REGISTRY.get(spec_id)
        if spec is None:
            results.append(ReconResult(rel, spec_id, "unknown-spec", declared,
                                       "spec-id not in registry"))
            continue
        current = spec_current_version(repo_root, spec)
        if current is None:
            results.append(ReconResult(rel, spec_id, "unknown-spec", declared,
                                       f"{spec.path} absent or version unparseable"))
            continue
        status = "match" if norm_version(declared) == norm_version(current) else "mismatch"
        results.append(ReconResult(rel, spec_id, status, declared, current))
    return results


def enumerate_edges(repo_root: Path) -> list[Edge]:
    """The Prompt-B contract: one Edge per well-formed, known-spec edge (match OR mismatch).

    Malformed / unknown-spec rows are excluded (no resolvable spec_path/new_version)."""
    edges: list[Edge] = []
    for r in reconcile(repo_root):
        if r.status in ("match", "mismatch"):
            spec = _SPEC_REGISTRY[r.spec_id]
            edges.append(Edge(r.dependent_path, spec.path, r.declared, r.current))
    return edges


def format_findings(results: list[ReconResult]) -> str:
    """One flat line per MISMATCHED edge (markdown-table-safe — no `|`)."""
    parts = [f"{r.dependent_path} declares {r.spec_id}@{r.declared} but spec is {r.current}"
             for r in results if r.status == "mismatch"]
    return "; ".join(parts).replace("|", "/")


def main() -> int:
    """Standalone CLI: print every edge's status; exit 0 always (awareness layer)."""
    results = reconcile(_REPO_ROOT)
    if not results:
        print("validate_reconciliation: no reconciled_with edges declared")
        return 0
    mismatches = [r for r in results if r.status == "mismatch"]
    for r in results:
        print(f"  {r.status:>12}  {r.dependent_path} -> {r.spec_id} "
              f"(declared {r.declared or '-'} / current {r.current or '-'})")
    print(f"validate_reconciliation: {len(results)} edge(s), {len(mismatches)} mismatch(es)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
