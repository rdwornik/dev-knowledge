"""End-to-end integration test for the dependency-coherence spine (#172).

THE CLOSURE GATE (the hard metric — end-state-meets-goal, NOT tests-pass): an injected
PARTIAL drift, detected by the REAL checker, must drive the REAL enumerator (wired to the
checker's `enumerate_edges` output — no stub) to surface the SPECIFIC missed sites as
candidates for verdict, by category.

R2 framing — what the deterministic chain proves, and what it does NOT:
  * deterministic guarantee = (a) the version lag is DETECTED (Finding fail) AND (b) every
    candidate reference site the drift could touch is ENUMERATED as a must-verdict line item
    (here: the stale walkthrough block + the un-updated diagram), by category.
  * the STALENESS verdict itself — judging those candidates `stale` and editing them — is the
    LLM/human advisory gate (`check-against-spec` skill), NOT proven here. This test never
    claims the spine "flags the site stale"; it claims the spine cannot let the site pass
    unseen.

If either missed site fails to enumerate, the deterministic guarantee is broken and v1 has
NOT closed.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit as aud  # noqa: E402
import coherence_enumerator as ce  # noqa: E402
import validate_reconciliation as vr  # noqa: E402

# A registered spec (handoff-process) bumped to 5.3 with a NEW required step.
_SPEC_53 = """\
# HANDOFF_PROCESS

Version: 5.3
Status: live

## Required steps

1. Original step one.
2. Original step two.
3. Original step three.
4. **New mandatory step (the drift).** A step the dependent runbook's walkthrough
   does not yet mention.
"""

# The dependent still declares @5.2 (the OLD version): its walkthrough and its diagram
# do NOT reflect the new required step — the partial-update scenario a version bump creates.
_DEPENDENT_STALE = """\
---
reconciled_with: handoff-process@5.2
last_reviewed: 2026-06-17
---

# Boot runbook

A dependent of HANDOFF_PROCESS, reconciled against an older spec version.

## Boot walkthrough

1. Read CLAUDE.md.
2. Read ESSENTIALS and PLAYBOOK.
3. Read the latest handoff bundle.
4. Read the last 5 JOURNAL entries.
5. Run git status.
6. Run pytest --collect-only.
7. Wait for the operator prompt.

## Flow diagram

```mermaid
flowchart TD
    A[session start] --> B[boot]
    B --> C[work]
    C --> D[handoff]
```
"""

# A reconciled dependent (declares @5.3) — proves the gate is not constant-fail.
_DEPENDENT_RECONCILED = _DEPENDENT_STALE.replace(
    "reconciled_with: handoff-process@5.2", "reconciled_with: handoff-process@5.3")


def _fixture(tmp_path: Path, dependent_text: str) -> Path:
    (tmp_path / "protocols").mkdir(parents=True, exist_ok=True)
    (tmp_path / "protocols" / "HANDOFF_PROCESS.md").write_text(_SPEC_53, encoding="utf-8")
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "runbook.md").write_text(dependent_text, encoding="utf-8")
    return tmp_path


def test_partial_drift_caught_and_missed_sites_enumerated(tmp_path: Path) -> None:
    """THE CLOSURE GATE: real drift -> real Finding(fail) -> enumerator names the specific
    missed walkthrough + diagram sites, by category."""
    repo = _fixture(tmp_path, _DEPENDENT_STALE)

    # 1) the REAL ship-gate detects the version lag -> exactly one Finding(fail).
    findings = aud.check_reconciled_versions(repo)
    assert [f.status for f in findings] == ["fail"], \
        f"expected a single FAIL, got {[(f.check_name, f.status) for f in findings]}"
    assert findings[0].check_name == "reconciled_versions"
    assert "docs/runbook.md" in findings[0].evidence and "5.2" in findings[0].evidence

    # 2) the enumerator consumes the checker's REAL Edge output (the wired seam, no stub).
    edges = vr.enumerate_edges(repo)
    assert len(edges) == 1
    edge = edges[0]
    assert (edge.old_version, edge.new_version) == ("5.2", "5.3")
    result = ce.enumerate_from_edge(edge, repo)
    sites = result["sites"]
    assert result["spec_version_current"] == "5.3"

    # 3) CLOSURE METRIC — the missed sites are enumerated as candidates, BY CATEGORY.
    #    (Whether they are stale is the LLM/human advisory verdict, not asserted here.)
    walk = [s for s in sites["walkthrough_steps"] if "Wait for the operator prompt" in s.text]
    assert walk, "the stale 7-step walkthrough block was not enumerated as a candidate"
    assert walk[0].line_end > walk[0].line_start, "surfaced as a discrete range, not a file flag"

    diags = sites["diagrams"]
    assert any("mermaid" in d.anchor for d in diags), "the un-updated diagram was not enumerated"
    diag = next(d for d in diags if "mermaid" in d.anchor)
    assert diag.line_end > diag.line_start

    # the rendered checklist NAMES both specific sites, under their category headers, with a
    # verdict slot per site — the deliverable the verdicting agent fills.
    checklist = ce.format_checklist(result)
    assert "Read CLAUDE.md" in checklist          # the walkthrough block's anchor (first line)
    assert "mermaid" in checklist                 # the diagram's anchor
    assert "walkthrough_steps" in checklist and "diagrams" in checklist
    assert "verdict: ___" in checklist


def test_drive_via_enumerate_repo_is_equivalent(tmp_path: Path) -> None:
    """The repo-level driver (`enumerate_repo`) walks A's edges and enumerates each — the
    same result as enumerating the single edge by hand. The full deterministic spine."""
    repo = _fixture(tmp_path, _DEPENDENT_STALE)
    results = ce.enumerate_repo(repo)
    assert len(results) == 1
    sites = results[0]["sites"]
    assert sites["walkthrough_steps"] and sites["diagrams"]


def test_gate_is_not_constant_fail_when_reconciled(tmp_path: Path) -> None:
    """Sanity: once the dependent declares the new version, the ship-gate PASSES — the FAIL
    above is meaningful drift detection, not a constant red."""
    repo = _fixture(tmp_path, _DEPENDENT_RECONCILED)
    findings = aud.check_reconciled_versions(repo)
    assert [f.status for f in findings] == ["pass"]
