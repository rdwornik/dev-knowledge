"""[#465] leg 1 — a SKIP must never be recorded as PASS.

The fleet-audit dailies inflated their pass counts by emitting `pass` from checks that had
not run at all: the row's own evidence found "9 hub-only checks skipped-as-PASS, 6 of the last
8 runs" when the hub intermittently resolved as not-the-hub. A green that means "did not run"
is worse than a red — it is a verification organ reporting success for work it never did, and
it corrupts every consumer of check results (state.yaml, index.yaml, the daily digests, the
report tallies).

The five-value enum already carries the honest tokens, documented at the report-generation
seam in audit.py: "unavailable" = path-absent / couldn't run; "n/a" = ran but not applicable
here. Neither blocks health or the ship-gate, so reporting a skip honestly costs no gate
verdict -- it only stops the pass count from lying.

The planted skip is a bare tmp_path: not the hub, so every hub-only check skips, and no
optional artifact exists so every presence-guarded check skips too.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest

import audit as aud

# Evidence phrasings that mean "this check did not actually verify anything".
_SKIP_EVIDENCE_RE = re.compile(
    r"\bskipped\b|nothing to validate|no probe bundle|advisory inactive"
    r"|no reconciled_with edges declared|unreadable|git unavailable",
    re.I,
)


def _findings_on(path: Path):
    for check in aud.ALL_CHECKS:
        try:
            yield from check(path)
        except Exception as exc:  # noqa: BLE001 — a raising check is a different defect
            pytest.fail(f"{check.__name__} raised on a bare repo: {exc!r}")


def test_no_check_reports_pass_for_a_skip(tmp_path):
    """The invariant, structurally: `pass` may never carry skip-shaped evidence.

    Structural rather than a fixed list of call sites, so a NEW check that emits
    pass-with-skip is caught the day it lands instead of the next time someone reads a digest.
    """
    offenders = [
        (f.check_name, f.status, f.evidence)
        for f in _findings_on(tmp_path)
        if f.status == "pass" and _SKIP_EVIDENCE_RE.search(f.evidence)
    ]
    rendered = "\n".join(f"  {n}: {s} -- {e}" for n, s, e in offenders)
    assert not offenders, (
        f"{len(offenders)} check(s) report `pass` for work they did not do -- a skip must be "
        f'"n/a" (ran, not applicable) or "unavailable" (could not run):\n{rendered}'
    )


def test_hub_only_checks_report_na_off_hub(tmp_path):
    """The 9 hub-only checks named in [#465]'s evidence, pinned by name.

    They are the ones that silently inflated the dailies when hub-detection flapped, so the
    regression names them rather than relying on the structural sweep alone.
    """
    hub_only = {
        "hooks_armed", "git_backlog_drift", "doc_claims", "doc_rot", "undeclared_edges",
        "doc_structure", "no_ff_merges", "doc_code_edge", "doc_code_coverage_drift",
    }
    seen = {f.check_name: f.status for f in _findings_on(tmp_path)
            if f.check_name in hub_only}
    wrong = {n: s for n, s in seen.items() if s == "pass"}
    assert not wrong, f"hub-only check(s) still green off-hub: {wrong}"


def test_skip_statuses_do_not_block_the_gate(tmp_path):
    """The fix must not turn a silent inflation into a noisy gate.

    `n/a`/`unavailable` are non-blocking by design (audit.py's own status semantics), so
    telling the truth about a skip changes the TALLY, never the verdict. Pinned so a later
    change cannot "fix" honesty by promoting skips to warn and REDding every consumer.
    """
    blocking = [(f.check_name, f.status) for f in _findings_on(tmp_path)
                if f.status in ("fail", "warn") and _SKIP_EVIDENCE_RE.search(f.evidence)]
    assert not blocking, f"a skip was promoted to a blocking status: {blocking}"
