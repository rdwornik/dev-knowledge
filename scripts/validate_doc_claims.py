#!/usr/bin/env python
"""validate_doc_claims.py — #89 read-only prose-vs-state checker.

Assert a living doc's own self-contained, deterministically-checkable CLAIMS match
repo ground truth, catching edited-but-not-reconciled prose the freshness gate
(audit check #10) cannot see — #10 checks whether `last_reviewed` post-dates the
last edit (stamp staleness), NOT whether the prose is accurate.

Precision-over-recall (one false positive kills adoption): only a bounded claim-set
that is mechanically checkable with ZERO false positives, NOT all prose. Three claims
across two loci:
  1. audit check-count   — ARCHITECTURE.md "**N registered checks**" vs len(ALL_CHECKS),
     INJECTED by the caller (the single source of truth lives in audit.py; never
     re-derived here by counting `def check_`).
  2a. pre-commit gate count — ARCHITECTURE.md "pre-commit gates (N)" vs the count of ALL
      hook `id:` in .pre-commit-config.yaml. Counts EVERY id including the commit-msg
      `backlog-id-on-close`: the doc's "(8)" includes it, so stage-scoping to the 7
      pre-commit-stage hooks would be a false positive (pre-flight-confirmed).
  2b. pre-commit roster  — CLAUDE.md §9's named hook list vs the same id set (order-indep).
  3. pytest collected    — ARCHITECTURE.md "**N collected**" vs `pytest --collect-only`.
     EXPENSIVE (subprocess) → evaluated only when run_expensive=True (the full-audit
     path: `audit.py run`/`repo`/standalone CLI/SessionStart), SKIPPED on the per-commit
     `health` gate so commits stay fast (operator ruling).

Anchor-not-found policy (the precision lever): a claim whose anchor no longer matches
(doc reworded) → status 'anchor-missing', a low-key WARN, NEVER a synthesized mismatch.
A reworded doc nudges a re-anchor; it does not raise a false alarm.

Scope boundary (do NOT duplicate): check #10 owns last_reviewed staleness; check #13
(`handoff_version_stamp`) owns HANDOFF_PROCESS version stamps; #140 owns cross-file
summary-fidelity drift, intra-file duplication, file bloat, and changelog accumulation.
#89 is one doc's count/list accuracy vs a machine-readable source — nothing else.

Layer-2 / read-only contract (ADR-28/36): reads docs + .pre-commit-config.yaml (+ shells
pytest --collect-only for claim 3); writes NOTHING; never orchestrates; never gates
(awareness layer — the audit adapter emits WARN/pass only, CLI prints and exits 0).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent


@dataclass(frozen=True)
class ClaimResult:
    name: str       # registry key, e.g. "audit_check_count"
    status: str     # 'match' | 'mismatch' | 'anchor-missing' | 'skipped'
    claimed: str    # value parsed from prose, or "" when anchor/claim not locatable
    actual: str     # ground truth (stringified)
    doc: str        # the doc the claim lives in (repo-relative)


@dataclass(frozen=True)
class Claim:
    name: str
    doc: str
    anchor: Optional[re.Pattern]                 # count kind: group(1) = claimed int
    kind: str                                    # "count" | "set"
    deriver: Callable[[Path, int], object]       # ground truth; 2nd arg = injected check count
    expensive: bool = False                      # True -> only when run_expensive


# --- extractors (pure, unit-tested in isolation) ----------------------------

def extract_hook_ids(precommit_yaml_text: str) -> list[str]:
    """Every hook `id:` in .pre-commit-config.yaml, in file order. Counts ALL stages
    (incl. the commit-msg `backlog-id-on-close`) — see module docstring 2a."""
    cfg = yaml.safe_load(precommit_yaml_text) or {}
    return [h["id"] for repo in cfg.get("repos", []) for h in repo.get("hooks", [])]


_SECTION9_RE = re.compile(r"^##\s+9\.\s+Hooks active\b", re.MULTILINE)
_NEXT_SECTION_RE = re.compile(r"^##\s+", re.MULTILINE)
_PRECOMMIT_LINE_RE = re.compile(r"Pre-commit", re.IGNORECASE)
_BULLET_ID_RE = re.compile(r"^-\s+`([a-z0-9-]+)`")


def extract_claimed_hooks(claude_md_text: str) -> Optional[set[str]]:
    """The pre-commit hook ids NAMED in CLAUDE.md §9, as a set.

    Window-bounded to the `## 9. Hooks active` block (heading → next `## `) so the
    §12 Section-history prose that names hooks (`ruff`, `audit-health`, …) cannot leak
    in. Within the window, collects the LEADING backtick token of each bullet under the
    `Pre-commit (.pre-commit-config.yaml):` sub-line (ignoring trailing description
    backticks and later sub-blocks like Rules/Session hooks). Returns None when the
    section or the pre-commit sub-list is not locatable → 'anchor-missing', never a
    spurious set.
    """
    ms = _SECTION9_RE.search(claude_md_text)
    if ms is None:
        return None
    rest = claude_md_text[ms.end():]
    mnext = _NEXT_SECTION_RE.search(rest)
    window = rest[: mnext.start()] if mnext else rest

    ids: set[str] = set()
    in_precommit = False
    for line in window.splitlines():
        if not in_precommit:
            if _PRECOMMIT_LINE_RE.search(line) and "pre-commit-config.yaml" in line:
                in_precommit = True
            continue
        mb = _BULLET_ID_RE.match(line)
        if mb:
            ids.add(mb.group(1))
        elif line.strip() and not line.lstrip().startswith("-"):
            # first non-bullet, non-blank line ends the pre-commit sub-list
            break
    return ids or None


def _derive_pytest_collected(repo_root: Path, _check_count: int) -> Optional[int]:
    """Collected test count via `pytest --collect-only -q` (claim 3, expensive).

    Returns the parsed count, 0 when collection ran but found nothing, or None when
    the launcher/subprocess fails (→ 'skipped', fail-soft; an infra hiccup must not
    flap a WARN). Genuine drift (a real count != the claim) still surfaces as mismatch.

    Read-only (Layer-2, ADR-28/36): `-p no:cacheprovider` suppresses `.pytest_cache/` and
    `PYTHONDONTWRITEBYTECODE=1` suppresses `__pycache__/`, so collection writes NOTHING.
    """
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"],
            cwd=str(repo_root), capture_output=True, text=True, encoding="utf-8",
            timeout=180, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except (OSError, subprocess.SubprocessError):
        return None
    out = f"{proc.stdout}\n{proc.stderr}"
    m = re.search(r"(\d+)\s+tests?\s+collected", out)
    if m:
        return int(m.group(1))
    if re.search(r"no tests (?:ran|collected)|collected 0 items", out):
        return 0
    return None


# --- reconcile (pure orchestration) -----------------------------------------

def _fmt_set(s) -> str:
    return "{" + ", ".join(sorted(s)) + "}"


def reconcile(repo_root: Path, audit_check_count: Optional[int],
              run_expensive: bool = False) -> list[ClaimResult]:
    """Evaluate every claim against ground truth. Pure; reads only. Claim 3 is skipped
    unless run_expensive. `audit_check_count` is the injected len(ALL_CHECKS) (claim 1) —
    supplied by the caller that drives reconcile (audit.check_doc_claims / tests); pass
    None when no caller owns it (standalone CLI), making claim 1 report `skipped` instead
    of importing audit (GAP-1 cycle-break, audit 2026-06-25)."""
    results: list[ClaimResult] = []
    for c in _CLAIMS:
        if c.expensive and not run_expensive:
            results.append(ClaimResult(c.name, "skipped", "",
                                       "off-gate (run via audit.py run / CLI)", c.doc))
            continue
        doc_path = repo_root / c.doc
        if not doc_path.exists():
            results.append(ClaimResult(c.name, "anchor-missing", "", "<doc absent>", c.doc))
            continue
        text = doc_path.read_text(encoding="utf-8")
        actual = c.deriver(repo_root, audit_check_count)
        if actual is None:                       # ground truth unavailable (e.g. pytest failed)
            results.append(ClaimResult(c.name, "skipped", "",
                                       "<ground truth unavailable>", c.doc))
            continue
        if c.kind == "count":
            m = c.anchor.search(text)
            if m is None:
                results.append(ClaimResult(c.name, "anchor-missing", "", str(actual), c.doc))
                continue
            claimed = m.group(1)
            status = "match" if int(claimed) == int(actual) else "mismatch"
            results.append(ClaimResult(c.name, status, claimed, str(actual), c.doc))
        else:  # kind == "set" — the §9 roster (only set claim)
            claimed_set = extract_claimed_hooks(text)
            if claimed_set is None:
                results.append(ClaimResult(c.name, "anchor-missing", "",
                                           _fmt_set(actual), c.doc))
                continue
            status = "match" if claimed_set == actual else "mismatch"
            results.append(ClaimResult(c.name, status, _fmt_set(claimed_set),
                                       _fmt_set(actual), c.doc))
    return results


def format_findings(results: list[ClaimResult]) -> str:
    """One flat line per MISMATCHED claim (markdown-table-safe — no `|`)."""
    parts = [
        f"{r.name}@{r.doc} (doc {r.claimed} != actual {r.actual})"
        for r in results if r.status == "mismatch"
    ]
    return "; ".join(parts).replace("|", "/")


# --- claim registry (a future claim is one appended row) --------------------

_CLAIMS = [
    Claim("audit_check_count", "ARCHITECTURE.md",
          re.compile(r"\*\*(\d+)\s+registered checks\*\*"), "count",
          lambda root, n: n),                                  # injected len(ALL_CHECKS)
    Claim("precommit_hook_count", "ARCHITECTURE.md",
          re.compile(r"pre-commit gates \((\d+)\)"), "count",
          lambda root, n: len(extract_hook_ids(
              (root / ".pre-commit-config.yaml").read_text(encoding="utf-8")))),
    Claim("precommit_hook_roster", "CLAUDE.md",
          None, "set",
          lambda root, n: set(extract_hook_ids(
              (root / ".pre-commit-config.yaml").read_text(encoding="utf-8")))),
    Claim("pytest_collected", "ARCHITECTURE.md",
          re.compile(r"\*\*(\d+)\s+collected\*\*"), "count",
          _derive_pytest_collected, expensive=True),
]


def main() -> int:
    """Standalone CLI: evaluate every self-derivable claim (incl. expensive claim 3);
    print; exit 0 always (awareness layer, never a gate).

    The `audit_check_count` claim is NOT evaluated here: its ground truth is
    len(ALL_CHECKS), owned by audit.py (the aggregator that imports THIS leaf). A leaf
    reaching back up to audit was the sole import cycle in scripts/ (GAP-1, audit
    2026-06-25); the dependency is inverted — whoever drives reconcile() supplies the
    count (audit.check_doc_claims injects len(ALL_CHECKS); tests inject directly), and
    standalone we pass None so that one claim reports `skipped` rather than recreate the
    edge. Run `audit health` / `audit run` for the check-count reconciliation."""
    results = reconcile(_REPO_ROOT, None, run_expensive=True)
    mismatches = [r for r in results if r.status == "mismatch"]
    if not mismatches:
        print(f"validate_doc_claims: OK — {len(results)} claim(s) checked, no prose drift")
        for r in results:
            print(f"  {r.status:>14}  {r.name} (doc {r.claimed or '-'} / actual {r.actual})")
        return 0
    print(f"validate_doc_claims: {len(mismatches)} prose claim(s) drifted from repo state:")
    for r in results:
        flag = "DRIFT " if r.status == "mismatch" else "      "
        print(f"  {flag}{r.status:>14}  {r.name}@{r.doc}  doc={r.claimed or '-'}  actual={r.actual}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
