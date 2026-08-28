"""`check_routing_agreement` — the `[#613]` L0 routing-agreement organ as a registered gate.

Thin ADAPTER half; the logic lives in `scripts/routing_agreement.py`. Same module-import +
thin-adapter shape as `check_dispatch_drift` (`[#592]`), reused rather than reinvented — which
is what register ruling **Z-G3 amendment A2** asks for when it says the agreement check is
"the same shape `[#592]` already built".

WHY IT IS SHIP-TIER AND NOT COMMIT-TIER, stated because it is a deliberate choice and not an
omission. The L0 derived copy lives on the OPERATOR's disk and the hub writes it at no time —
deriving it is the operator's act, and this lane's contract names writing to `~/.claude/` as an
anti-pattern. At arm time the live L0 (`~/.claude/ROUTING.md`) exists but does **not** yet
carry the derived rows, so the organ measures **4 divergences on a clean tree**. Arming a FAIL
leg at COMMIT tier against a state only the operator can clear would wedge every commit in the
repository on a file the repository may not touch.

`[#592]` set the evidence bar this follows — *"MEASURED BEFORE ARMING … the check measures 0
findings, so arming its FAIL leg cannot RED a clean tree"* — and this check does not clear that
bar today. The honest response is to declare the tier, not to soften the verdict: `_tier(TIER_SHIP, ...)`
per `[#597]`, so the FAIL is real and surfaces at `audit run` / `ship-gate` where a human is
reading, while `audit.py health` (the pre-commit gate) does not run it.

WHAT IS **NOT** DONE HERE, so the tier is not mistaken for a softening: the verdict is still
`fail` on divergence and `warn` on an absent L0. Neither is `unavailable` — `_check_outcome`
projects that onto `pass` and `cmd_ship_gate` blocks only on `fail` plus undispositioned
`warn`, so `unavailable` would SHIP GREEN having measured nothing. That is the green-by-skip
class register ruling **Z-G4** closes, and this organ is one of its named consumers.

Child-repo-safe: a repo with no `ecosystem/routing-table.yaml` yields `n/a` (subject-absent),
not a FAIL. Read-only (Layer 2): two file reads, no writes, no git.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding, _na, _NA_SUBJECT_ABSENT

try:
    from scripts import routing_agreement as _ra
except ImportError:
    import routing_agreement as _ra

CHECK_NAME = "routing_agreement"


def check_routing_agreement(repo_path: Path) -> list[Finding]:
    """`[#613]`: the L0 routing copy agrees with the authoritative in-repo table."""
    root = Path(repo_path)
    if not (root / _ra.TABLE_RELPATH).is_file():
        return [_na(CHECK_NAME, _NA_SUBJECT_ABSENT,
                    f"no {_ra.TABLE_RELPATH} — this repo carries no routing table")]

    try:
        state, _diverged, detail = _ra.scan(root)
    except _ra.RoutingAgreementError as exc:
        # FAIL, not "unavailable": an unreadable corpus reports zero divergence, which is
        # exactly what a broken scan looks like from the outside.
        return [Finding(CHECK_NAME, "fail",
                        f"the routing corpus could not be scanned, so no role was "
                        f"checked: {exc}".replace("|", "/"))]

    if state == "l0-absent":
        return [Finding(CHECK_NAME, "warn", detail.replace("|", "/"))]
    if state == "diverge":
        return [Finding(CHECK_NAME, "fail",
                        f"the L0 derived copy diverges from {_ra.TABLE_RELPATH}: "
                        f"{detail}".replace("|", "/"))]
    return [Finding(CHECK_NAME, "pass", detail.replace("|", "/"))]
