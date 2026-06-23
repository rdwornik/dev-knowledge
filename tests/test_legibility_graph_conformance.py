"""Graph-level conformance test for the dependency-legibility graph (ADR-88/ADR-89).

ARCHITECTURE.md claims the graph's FOUR edge-type oracles are "live and integrated" over the
.dev-knowledge artifacts. The per-oracle suites prove each oracle's OWN logic; nothing proved
the graph as an INTEGRATED WHOLE. Under "a claim without a test is not implemented", this file
owns that graph-level claim. It adds graph-level proof and closes nothing (#194 stays OPEN).

SCOPE -- this test owns EXACTLY two things:
  (a) the graph-INTEGRATING property: all 4 oracles registered + operational, and each fires on
      ONE representative break through its REAL integrated entry point (the audit runner for the
      two enforcers; the public CLI/API for the two awareness tools) -- NOT the oracle function
      in isolation;
  (b) the honest tally of those integration cells (proven / skipped / gap).

It does NOT re-run or couple to per-oracle suite internals, and does NOT own per-oracle DEEP
modes (#193 transitive closure, #179 false-flag precision, the #194 coverage tail). Those are
REFERENCED in the ARCHITECTURE.md conformance map and tracked by their own backlog items.

The 4 edge-types and their real integrated entry points:
  * spec->dependent (#172)  -> audit.check_reconciled_versions   (in ALL_CHECKS, a gate)
  * doc->code        (#194) -> audit.check_doc_code_edge         (in ALL_CHECKS, hub-only gate)
  * undeclared (#179/#199)  -> scan_undeclared_edges.scan/main   (awareness CLI, exit 0 by design)
  * code<->code      (#193) -> reverse_dep_oracle.run_oracle     (query tool; Pyright-backed)

GREEN NEVER LIES: the code<->code FIRES cell needs a vendored Pyright langserver (an
`npm install` artifact; node_modules is gitignored). Its fires-cell is a THREE-state cell --
proven / skipped / gap -- whose status is derived AT RUNTIME from the SAME langserver check the
skipif uses (`_langserver_available()`), never hardcoded. When Pyright is provisioned (this env)
the cell RUNS and is "proven"; when it is not, the cell SKIPS and the tally reads "N proven,
K skipped" and must NOT make the affirmative "FULLY PROVEN" claim. A SKIP is
not-proven-in-this-env, never silently "proven".
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest  # noqa: E402

import audit as aud  # noqa: E402
import reverse_dep_oracle as rdo  # noqa: E402
import scan_undeclared_edges as sue  # noqa: E402
import validate_doc_code_edge as vdce  # noqa: E402  (in ALL_CHECKS via aud; referenced here)
import validate_reconciliation as vr  # noqa: E402  (in ALL_CHECKS via aud; referenced here)

_REPO_ROOT = Path(__file__).resolve().parents[1]

# The SAME langserver resolution the oracle (and test_reverse_dep_oracle.py) uses, computed once
# so the skipif guard and the ledger's code<->code status can NEVER diverge.
_LS_ARGV = rdo.find_langserver(_REPO_ROOT)


def _langserver_available() -> bool:
    """Reuse the oracle's OWN resolver (find_langserver) so the skipif guard and the ledger's
    code<->code status derive from ONE check (operator contract: derive the cell status at
    runtime from the same check the skipif uses -- never hardcode "proven"). Pyright is
    "provisioned" iff node is on PATH AND find_langserver resolves a langserver."""
    return shutil.which("node") is not None and _LS_ARGV is not None


# Override for an ISOLATED COPY (which has no node_modules of its own): the vendored
# langserver.index.js path when resolution is the node form; None when it is a
# `pyright-langserver` on PATH (which find_langserver re-resolves against the copy via PATH).
_LS_OVERRIDE = _LS_ARGV[1] if (_LS_ARGV and _LS_ARGV[0] == "node") else None

requires_pyright = pytest.mark.skipif(
    not _langserver_available(),
    reason="reverse_dep_oracle needs a Pyright langserver; absent in this env -- "
    "code<->code integration-fire skip-guarded, tracked by #195 + #193",
)


# ---------------------------------------------------------------------------------------------
# (a) HARD ASSERTION -- all 4 oracles registered + operational in the integrated system
# ---------------------------------------------------------------------------------------------

def test_graph_oracles_registered_and_operational(tmp_path):
    """The 2 enforcers ARE wired into the audit runner (ALL_CHECKS); the 2 awareness tools are
    callable public entry points (NOT in ALL_CHECKS, by design -- recorded in the map).
    code<->code is operational = callable + a fail-soft, provenance-bearing envelope on every
    path (never a crash -- the gate-safety contract), proven WITHOUT a langserver so it always
    runs (no Pyright needed for *operational*)."""
    # enforcers: wired into the integrated audit runner (the gate)
    assert {aud.check_reconciled_versions, aud.check_doc_code_edge} <= set(aud.ALL_CHECKS)
    # the enforcers' logic lives in these modules (referenced; their suites prove the deep modes)
    assert callable(vr.reconcile) and callable(vdce.resolve_edge)
    # awareness tools: callable public entry points, deliberately NOT in ALL_CHECKS
    assert callable(sue.scan) and callable(sue.main)
    assert aud.check_reconciled_versions not in (None,)  # (explicit: the enforcer is a real fn)
    assert callable(rdo.run_oracle)

    # code<->code operational: a fail-soft, provenance-bearing envelope (no langserver for the
    # copy -> oracle-unavailable; or resolved if a langserver is on PATH -- either is well-formed)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "mod.py").write_text(
        "def widget():\n    return 1\n", encoding="utf-8")
    env = rdo.run_oracle("widget", None, tmp_path)  # no override -> fail-soft path is exercised
    assert isinstance(env, dict)
    for key in ("query", "resolution", "reverse_dependents",
                "reverse_dependent_count", "provenance"):
        assert key in env, f"oracle envelope missing {key!r}"
    assert env["resolution"]["status"] in {
        "resolved", "oracle-unavailable", "symbol-not-found", "ambiguous"}
    assert "git_rev" in env["provenance"]  # provenance present on EVERY status (gate-safety)


# ---------------------------------------------------------------------------------------------
# (b) INTEGRATION e2e -- each oracle fires on ONE representative break, through its REAL entry
#     point, on an ISOLATED COPY. Deep modes are NOT re-tested here (referenced in the map).
# ---------------------------------------------------------------------------------------------

def test_cell_spec_dependent_fires(tmp_path):
    """spec->dependent (#172) fires through the AUDIT RUNNER adapter: a dependent declaring a
    stale `reconciled_with` version -> check_reconciled_versions emits a FAIL Finding.
    (Deep modes -- partial-drift enumeration -- are proven in test_coherence_integration.py.)"""
    (tmp_path / "protocols").mkdir()
    (tmp_path / "protocols" / "HANDOFF_PROCESS.md").write_text(
        "# HANDOFF_PROCESS\n\nVersion: 9.9\n", encoding="utf-8")
    (tmp_path / "dependent.md").write_text(
        "---\nreconciled_with: handoff-process@1.0\n---\n\n# A stale dependent\n",
        encoding="utf-8")

    findings = aud.check_reconciled_versions(tmp_path)
    assert [f.status for f in findings] == ["fail"], \
        f"expected one FAIL through the adapter, got {[(f.check_name, f.status) for f in findings]}"
    assert findings[0].check_name == "reconciled_versions"
    assert "dependent.md" in findings[0].evidence


def test_cell_doc_code_fires(tmp_path, monkeypatch):
    """doc->code (#194) fires through the AUDIT RUNNER adapter: a declared `<!-- rule: ID -->`
    in a REGISTERED declaration doc with no matching `# rule: ID` -> check_doc_code_edge emits a
    WARN (broken_edge, advisory). Two integrated-entry conditions are satisfied: (1) the hub-only
    guard, via pointing audit._REPO_ROOT at the isolated copy (the established _as_hub idiom);
    (2) the post-#194 registry scope, via a real `ecosystem/doc-code-edge.yaml` declaration
    registry so resolution is include-scoped (the broken edge is found through the REAL scoped
    entry, not the unscoped spike path). (Deep modes -- move-safety, dup-guard, coverage gate,
    the registry-scoping asymmetry guard -- are proven in test_doc_code_edge.py.)"""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / "ecosystem" / "doc-code-edge.yaml").write_text(
        "declaration_docs:\n  - GUIDE.md\n", encoding="utf-8")
    (tmp_path / "GUIDE.md").write_text(
        "a governed rule <!-- rule: CONF-1 -->\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "impl.py").write_text(
        "def f():\n    return 1\n", encoding="utf-8")  # NO `# rule: CONF-1` -> broken edge

    findings = aud.check_doc_code_edge(tmp_path)
    assert all(f.status != "fail" for f in findings)  # advisory-first: WARN, never FAIL
    assert any(f.status == "warn" and "CONF-1" in f.evidence and "broken_edge" in f.evidence
               for f in findings), \
        f"expected a broken_edge WARN, got {[(f.status, f.evidence) for f in findings]}"


def test_cell_undeclared_fires(tmp_path, monkeypatch, capsys):
    """undeclared (#179/#199) fires through its REAL public entry: a doc prose-referencing a
    REGISTERED spec with NO `reconciled_with` edge -> scan() surfaces it as a Candidate, and the
    CLI main() (driven on the isolated copy via _REPO_ROOT) reports it. The awareness tool is
    exit-0 by design and NOT in ALL_CHECKS (recorded in the map). (Deep modes -- tier patterns,
    fenced-exclusion, false-flag precision -- are proven in test_scan_undeclared_edges.py.)"""
    (tmp_path / "protocols").mkdir()
    (tmp_path / "protocols" / "HANDOFF_PROCESS.md").write_text(
        "# HANDOFF_PROCESS\n\nVersion: 9.9\n", encoding="utf-8")
    (tmp_path / "guide.md").write_text(
        "# Guide\n\nThis guide follows protocols/HANDOFF_PROCESS.md but declares no "
        "reconciled_with edge.\n", encoding="utf-8")

    # public discovery API on the isolated copy
    cands = sue.scan(tmp_path)
    assert any(c.dependent_path == "guide.md" and c.spec_id == "handoff-process" for c in cands), \
        f"expected an undeclared-edge candidate (guide.md -> handoff-process), got {cands}"

    # the REAL CLI entry (main) on the isolated copy -- faithful integrated entry point
    monkeypatch.setattr(sue, "_REPO_ROOT", tmp_path)
    rc = sue.main()
    assert rc == 0  # awareness layer: exit 0 always
    out = capsys.readouterr().out
    assert "guide.md" in out and "handoff-process" in out


@requires_pyright
def test_cell_code_code_fires(tmp_path):
    """code<->code (#193) fires through run_oracle (Pyright references) on an isolated copy: a
    representative reverse-dependency -> the oracle resolves it with provenance. Skip-guarded by
    the SAME langserver check the ledger derives from (`_langserver_available()`), so this never
    silently passes when Pyright is unprovisioned. A SAME-FILE referencer is used because the
    live repo has no pyrightconfig/__init__ -- cross-module namespace-package resolution would be
    fragile to replicate in a copy; a same-file use is a genuine, config-independent code->code
    dependency. The langserver binary is supplied via the absolute vendored override (the copy
    has no node_modules), while Pyright indexes the COPY (rootUri = tmp_path). (Deep modes --
    transitive closure -- are tracked by #193/#195.)"""
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "mod.py").write_text(
        "def widget():\n"
        "    return 1\n"
        "\n"
        "\n"
        "def use_widget():\n"
        "    return widget() + widget()\n",
        encoding="utf-8")

    env = rdo.run_oracle("widget", None, tmp_path, langserver=_LS_OVERRIDE)
    assert env["resolution"]["status"] == "resolved", \
        f"expected resolved through the oracle, got {env['resolution']}"
    assert env["reverse_dependent_count"] >= 1, "the same-file referencer was not surfaced"
    assert env["provenance"]["completeness"] in {"complete", "partial"}


# ---------------------------------------------------------------------------------------------
# The integration-cell ledger -- single source for the tally AND the ARCHITECTURE map.
# status: "proven" (ran + passed here) | "skipped" (provable, not run in THIS env) |
#         "gap" (genuinely unprovable here -> would be xfail). code<->code FIRES is the only
# env-derived cell; its status comes from _langserver_available(), the SAME check the skipif
# uses, so the tally can never claim "proven" for a cell that actually skipped.
# ---------------------------------------------------------------------------------------------

_CODE_CODE_FIRES = "proven" if _langserver_available() else "skipped"

INTEGRATION_CELLS = [
    {"edge": "spec->dependent", "prop": "registered+operational", "status": "proven",
     "tracks": "in ALL_CHECKS (#172)"},
    {"edge": "spec->dependent", "prop": "fires-on-break", "status": "proven",
     "tracks": "deep: test_coherence_integration.py + test_validate_reconciliation.py"},
    {"edge": "doc->code", "prop": "registered+operational", "status": "proven",
     "tracks": "in ALL_CHECKS, hub-only (#194)"},
    {"edge": "doc->code", "prop": "fires-on-break", "status": "proven",
     "tracks": "deep: test_doc_code_edge.py; coverage tail #201/#202/#203"},
    {"edge": "undeclared", "prop": "registered+operational", "status": "proven",
     "tracks": "awareness CLI, NOT in gate by design (#179/#199)"},
    {"edge": "undeclared", "prop": "fires-on-break", "status": "proven",
     "tracks": "deep: test_scan_undeclared_edges.py"},
    {"edge": "code<->code", "prop": "registered+operational", "status": "proven",
     "tracks": "query tool, NOT in gate; consumed by #195 (#193)"},
    {"edge": "code<->code", "prop": "fires-on-break", "status": _CODE_CODE_FIRES,
     "tracks": "skip-guarded; Pyright vendored here; portability via #195 + #193"},
]


def _tally():
    proven = [c for c in INTEGRATION_CELLS if c["status"] == "proven"]
    skipped = [c for c in INTEGRATION_CELLS if c["status"] == "skipped"]
    gaps = [c for c in INTEGRATION_CELLS if c["status"] == "gap"]
    return proven, skipped, gaps


def _headline():
    proven, skipped, gaps = _tally()
    total = len(INTEGRATION_CELLS)
    fires = [c for c in INTEGRATION_CELLS if c["prop"] == "fires-on-break"]
    fires_proven = [c for c in fires if c["status"] == "proven"]
    fully = (len(skipped) == 0 and len(gaps) == 0)
    if fully:
        return (f"graph integration: FULLY PROVEN this env "
                f"({len(fires_proven)}/{len(fires)} fires ran+passed, "
                f"{len(proven)}/{total} cells proven; 0 skipped, 0 gap); deep-mode coverage "
                f"partial (tracked: doc->code #201/#202/#203, code<->code transitive "
                f"#193/#195)"), fully
    return (f"graph integration: NOT fully proven here -- "
            f"{len(fires_proven)}/{len(fires)} fires proven, {len(skipped)} skipped"
            + (f", {len(gaps)} gap(s)" if gaps else "")
            + " (fully PROVABLE; code<->code skipped where Pyright not provisioned); "
            "deep-mode coverage partial (tracked)"), fully


def test_graph_integration_tally():
    """Surface the honest 'N of M cells proven; K skipped/gap' tally and ENFORCE that green never
    lies: the affirmative 'FULLY PROVEN' claim may appear ONLY when no integration cell skipped
    or gapped. The code<->code fires status is derived from `_langserver_available()` (the same
    check the skipif uses), so a skipped cell can never be tallied as proven."""
    proven, skipped, gaps = _tally()
    total = len(INTEGRATION_CELLS)
    assert len(proven) + len(skipped) + len(gaps) == total  # states are exhaustive

    # the ledger's env-derived cell MUST track the runtime langserver check (operator contract)
    assert _CODE_CODE_FIRES == ("proven" if _langserver_available() else "skipped")

    headline, fully = _headline()
    print("\n" + headline)
    for c in INTEGRATION_CELLS:
        print(f"  [{c['status']:>7}] {c['edge']} :: {c['prop']}  ({c['tracks']})")

    # GREEN NEVER LIES: the affirmative claim appears IFF nothing skipped/gapped.
    assert ("FULLY PROVEN" in headline) == fully
    if skipped:
        assert "skipped" in headline and "FULLY PROVEN" not in headline
    if gaps:
        assert "gap" in headline
