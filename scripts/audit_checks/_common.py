"""Primitives shared by the extracted `audit_checks/` modules AND the `audit.py` facade.

[#533]. This module holds ONLY symbols that satisfy both of the following, because those
are the two properties that make a relocation a *pure* move:

  1. **Never monkeypatched.** No test anywhere in `tests/` calls
     `monkeypatch.setattr(aud, "<name>", ...)` for anything defined here. A symbol that IS
     patched on the `audit` module namespace cannot move: the check would then read this
     module's binding while the test rewrites `audit`'s, and the seam silently detaches. That
     criterion — measured, not judged — is what kept 25 of the 43 checks in the facade.
  2. **Needed on both sides.** The facade still uses every name here (`RepoState`,
     `classify_inert_checks`, the 26 resident checks), so it cannot simply travel with one
     check module.

`audit.py` re-exports all of these, so `audit.Finding`, `audit._na`, … keep working and keep
their ORIGINAL OBJECT IDENTITY — `isinstance(x, aud.Finding)` and dataclass equality across
the two import spellings are unaffected.

The code below is moved BYTE-IDENTICAL from `scripts/audit.py` (its own comments included).
Nothing here was rewritten, renamed, reformatted or "improved" in transit.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Finding:
    """One audit/check result — the LOCKED coherence-spine output contract.

    Stable shape: exactly three string fields — `check_name`, `status`, `evidence`.
    `status` is one of the five-value enum: "pass" | "fail" | "warn" | "unavailable" | "n/a".
    `evidence` is markdown-table-safe (no literal `|` — emitters replace it with `/`).

    This is the surface the #171 conformance dashboard consumes (ADR-86): the coherence
    checker emits `check_name == "reconciled_versions"` here (check_reconciled_versions),
    a `fail` per drifting edge. The shape is LOCKED — do not add/rename fields without
    updating that consumer. Pinned by tests/test_coherence_integration.py
    (test_finding_format_is_locked). No dashboard is built yet (#171, v2); this only
    fixes the format it will read.
    """
    check_name: str
    status: str          # "pass" | "fail" | "warn" | "unavailable" | "n/a"
    evidence: str


# --- [#465] leg 4, FR-1: why an n/a is an n/a -------------------------------
# A dead check and a correctly-skipped one both rendered as the bare token "n/a", so they were
# indistinguishable in every daily -- which is how `handoff_tag_canonicity` emitted a verdict
# for two spec generations after its subject stopped existing, unnoticed.
#
# The reason rides a parsable PREFIX inside the existing `evidence` string. That is deliberate
# and it is what keeps tripwire T1 from firing: `Finding` keeps exactly three fields and the
# five-value status enum, so the LOCKED coherence-spine contract and the daily's column grammar
# are untouched, and `test_finding_format_is_locked` still passes.
#
#   SUBJECT-ABSENT  the governed thing does not exist ANYWHERE -- the check can never fire
#   NOT-APPLICABLE  this repo legitimately lacks the surface; another repo has it
_NA_SUBJECT_ABSENT = "SUBJECT-ABSENT"
_NA_NOT_APPLICABLE = "NOT-APPLICABLE"
_NA_REASONS = (_NA_SUBJECT_ABSENT, _NA_NOT_APPLICABLE)
_NA_REASON_RE = re.compile(rf"^\[n/a-reason:({'|'.join(_NA_REASONS)})\] (.+)$", re.DOTALL)


def _na(check_name: str, reason: str, evidence: str) -> Finding:
    """An n/a Finding carrying a machine-readable reason. Raises on an unknown reason --
    a mis-typed reason must not silently become an unclassifiable n/a."""
    if reason not in _NA_REASONS:
        raise ValueError(f"unknown n/a reason: {reason!r}")
    return Finding(check_name, "n/a", f"[n/a-reason:{reason}] {evidence}".replace("|", "/"))


def _na_reason(finding: Finding) -> str | None:
    """The encoded reason, or None for a non-n/a finding OR an unclassified one.

    None is meaningful, not an error value: the detector treats an unclassified n/a as a loud
    WARN rather than assuming either reason (FR-3 -- never pass silently)."""
    if finding.status != "n/a":
        return None
    m = _NA_REASON_RE.match(finding.evidence)
    return m.group(1) if m else None


# Sibling dirs under docs/handoffs/ that are not bundles to validate.
#
# Lives here rather than with either user because it is the one constant read by BOTH an
# extracted check (`check_handoff_bundle_structure`) and a facade-resident one
# (`check_handoff_probes`, held back by the `_gitenv` path-load — see registry.py).
_BUNDLE_EXCLUDE_DIRS = {"aborted", "in-progress", "archive"}
