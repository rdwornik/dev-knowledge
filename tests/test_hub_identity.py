"""[#465] legs 2+3 -- the hub must recognise itself from any checkout.

The night batch (docs/audits/2026-08-02-technical-night-batch-lb-fleet-audit-commits.md
S4) proved the two remaining legs are ONE bug. On 2026-07-21 the hub daily carried 16 WARN
lines at 00:51 (`a5efca9e`) and 2 at 10:51 (`2f6f3c71`); the delta is exactly 14 and the 14
are precisely the three hub-only checks that had gone quiet -- no_ff_merges 4, doc_rot 4,
undeclared_edges 6 -- with 10 lines reading "not the hub repo" in their place. The same
collapse repeats on 8 of 10 multi-commit days.

Root cause, at the seam rather than in the checks: `audit_repo` is handed the absolute path
stored in `ecosystem/<name>/state.yaml`, and that value is COMMITTED to git
(`path: C:\\Users\\...\\.dev-knowledge`). Every hub-only check then gates on
`Path(repo_path).resolve() != Path(_REPO_ROOT).resolve()`, where `_REPO_ROOT` is derived
live from `__file__`. On the machine and checkout that registered the repo the two agree and
every check runs; from ANY other tree -- a worktree, a cloud clone, a relocated repo -- they
disagree, the hub silently resolves as not-the-hub, and all of its hub-only checks skip.
That is the "intermittent" in the row: it tracks which tree the run happened in, not chance.

Leg 2 (a day's digest losing 14 WARNs) is the same event seen at the writer: `append_history`
opens the daily "a", so two runs in ONE tree concatenate -- the duplication symptom the
report notes on 07-24/07-30/08-01. A run in a DIFFERENT tree instead commits a file holding
only its own table, which is why the high-fidelity run survives only via `git show <sha>`.
One cause, two visible directions.

These tests pin the fix at the resolution seam and, structurally, keep the identity
predicate single-sourced -- the enumerated-list lesson: 16 hand-copied comparisons (15
skip-gates plus one inverted site) are 16 chances for the next check to gate differently.
15 of the 38 ALL_CHECKS members are hub-gated, so this is a third of the audit going quiet.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit as aud

# The marker every hub-gated skip shares. Keying on the "not the hub repo" phrasing instead
# would silently miss five of the fifteen gated checks -- silent_rule_ratchet,
# task_tree_coherence, intake_tree_coherence, fleet_audit_replication, membership_agreement
# -- which say "hub-only" and then explain themselves differently. A detector that is itself
# a hand-list is the very defect these tests exist to prevent.
_HUB_ONLY = "hub-only"


def _hub_gated_checks():
    """ALL_CHECKS members that gate on hub identity, discovered not hand-listed.

    A bare tmp dir is never the hub, so every hub-gated check announces itself. Keeping
    this self-enumerating is the point: a check added tomorrow is covered on the day it
    lands, without editing a list here.
    """
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        bare = Path(td)
        gated = []
        for check in aud.ALL_CHECKS:
            try:
                findings = list(check(bare))
            except Exception:  # noqa: BLE001 - a raising check is a different defect
                continue
            if any(_HUB_ONLY in f.evidence for f in findings):
                gated.append(check)
    return gated


def test_hub_gated_checks_exist():
    """Guard the guard: if this set ever empties, the tests below go vacuous."""
    gated = _hub_gated_checks()
    assert gated, "no hub-gated checks discovered -- the probes below would pass vacuously"


def test_hub_resolves_to_the_live_tree_not_the_committed_path(tmp_path):
    """The hub audits the tree audit.py lives in, whatever state.yaml has stored.

    tmp_path stands in for a stale committed path -- another machine, another checkout.
    """
    stale = tmp_path / "some-other-checkout" / ".dev-knowledge"
    stale.mkdir(parents=True)

    resolved = aud.resolve_repo_path(aud.HUB_REPO_NAME, str(stale))

    assert Path(resolved).resolve() == Path(aud._REPO_ROOT).resolve(), (
        "the hub resolved to its stored path instead of the live tree -- every hub-only "
        "check would skip and the day's WARNs would vanish ([#465] legs 2+3)"
    )


def test_a_consumer_still_resolves_to_its_stored_path(tmp_path):
    """The fix must not capture consumers: only the hub is special-cased."""
    stored = tmp_path / "ai-council"
    stored.mkdir()

    resolved = aud.resolve_repo_path("ai-council", str(stored))

    assert Path(resolved).resolve() == stored.resolve()


def test_no_hub_only_check_skips_when_the_stored_path_is_stale(tmp_path):
    """The 14 missing WARNs, structurally: no hub-gated check may skip as not-the-hub.

    Self-enumerating over ALL_CHECKS rather than pinning the three checks the 07-21 repro
    happened to name, so the invariant covers checks that do not exist yet.
    """
    stale = tmp_path / "some-other-checkout" / ".dev-knowledge"
    stale.mkdir(parents=True)

    resolved = Path(aud.resolve_repo_path(aud.HUB_REPO_NAME, str(stale)))

    offenders = []
    for check in _hub_gated_checks():
        for f in check(resolved):
            if _HUB_ONLY in f.evidence:
                offenders.append(f"  {f.check_name}: {f.status} -- {f.evidence}")

    rendered = "\n".join(offenders)
    assert not offenders, (
        f"{len(offenders)} hub-only check(s) skipped while auditing the hub itself.\n"
        f"This is the 16 -> 2 WARN collapse of 2026-07-21, reproduced:\n{rendered}"
    )


def test_hub_identity_predicate_is_single_sourced():
    """The enumerated-list lesson: one predicate, not one comparison per call site.

    16 hand-copied `Path(repo_path).resolve() != Path(_REPO_ROOT).resolve()` lines are 16
    places for the next check to gate slightly differently. The comparison belongs in
    `_is_hub` and nowhere else.
    """
    src = Path(aud.__file__).with_suffix(".py").read_text(encoding="utf-8")
    inline = src.count("Path(_REPO_ROOT).resolve()")

    assert inline <= 1, (
        f"{inline} inline hub-identity comparisons remain; the predicate belongs in "
        "_is_hub() so every check gates identically"
    )
