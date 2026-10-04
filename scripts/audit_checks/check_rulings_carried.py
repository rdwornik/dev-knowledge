"""`check_rulings_carried` -- R79.3 as a registered audit finding: no ratified decision is forgotten.

Thin ADAPTER half; the logic is `scripts/decision_coverage.py::rulings_report`, which is also the
CLI (`decision_coverage.py rulings`, exit 1 on a refusal). Same module-import + thin-adapter shape
as `check_model_currency` and `check_routing_agreement`, reused rather than reinvented.

Prior-art check (library-first, AMEND-B2-W1-2 item 3): `decision_coverage` already joins a
document-read population with a relation, carries `Disposition`, era-bounds its refusals and
returns `Finding`; `p11_carriage` proves a decision file has a HOME, not that its ruling is in it
(`gen_handoff.py` states that limit itself); `question_disposition` governs QUESTION files. None
asks "is this ruling landed, and does a row or a written 'no implementation required' carry it",
so the leg lives in `decision_coverage` and this module only registers it.

WHERE IT RUNS, and why that is the whole design of the registration:
  * `HANDOFF_ORGAN_NAMES` names it, so it runs in the real handoff cut and in
    `gen_handoff.py --trial-cut`, which is what `ecosystem/harness.yaml`'s `batch-close` moment
    runs. One registered check therefore reaches both homes the AMEND names, with no edit to
    `gen_handoff.py` or `harness.yaml`.
  * It is `TIER_SHIP`: it runs in `audit.py ship-gate`, not in the per-commit `audit.py health`.
    The reason is the carried-leg's sibling: leg (a) reads the operator's TRANSPORT, which changes
    without any commit (the seat writes a ruling), so a COMMIT tier would wedge every lane's
    commit on a state the committing lane did not cause. Leg (b) reads only the repository.

TWO LEGS, ONE FINDING EACH PER DEFECT (a ship-gate disposition then matches one concern):
  (b) CARRIED -- a landed ruling from R55 on with no row and no 'no implementation required'.
  (a) LANDED  -- a ruling in a non-superseded RATIFICATION file that has outlived more than one
      closed batch without being landed. With no readable transport (CI, an unmounted drive) this
      leg is reported `n/a` with the registered SUBJECT-ABSENT reason -- NEVER a pass.

Child-repo-safe: a repo with no `protocols/STANDING_RULINGS.md` yields `n/a` (subject absent).
Read-only (Layer 2): file reads only, no writes.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding, _na, _NA_SUBJECT_ABSENT

try:
    from scripts import decision_coverage as _dc
except ImportError:  # pragma: no cover - the scripts/-on-sys.path entrypoint
    import decision_coverage as _dc

CHECK_NAME = "rulings_carried"


def _fail(subject: str, evidence: str) -> Finding:
    return Finding(CHECK_NAME, "fail", f"{subject}: {evidence}".replace("|", "/"))


def check_rulings_carried(repo_path: Path) -> list[Finding]:
    """R79.3: every ratified ruling is landed, and every landed one is carried or dispositioned."""
    root = Path(repo_path)
    if not (root / _dc.RULINGS_REL).is_file():
        return [_na(CHECK_NAME, _NA_SUBJECT_ABSENT,
                    f"no {_dc.RULINGS_REL} -- this repo carries no ruling register")]
    try:
        report = _dc.rulings_report(root)
    except _dc.PopulationUnreadable as exc:
        return [Finding(CHECK_NAME, "fail",
                        f"the ruling register could not be read: {exc}".replace("|", "/"))]
    findings = [_fail(f.subject, f.evidence) for f in report.uncarried]
    counts = report.counts
    if not report.uncarried:
        findings.append(Finding(
            CHECK_NAME, "pass",
            f"{counts.carried} of {counts.gated} gated ruling(s) (R{_dc.FIRST_GATED_RULING} on) "
            f"carried by a row or a written 'no implementation required'; {counts.grandfathered} "
            f"older entries counted, not refused (decision_coverage.py rulings)"))
    if report.unlanded is _dc.UNMEASURED:
        findings.append(_na(
            CHECK_NAME, _NA_SUBJECT_ABSENT,
            f"leg (a) not measured, so not a pass: {report.unmeasured_reason}"))
    elif report.unlanded:
        findings.extend(_fail(f.subject, f.evidence) for f in report.unlanded)
    else:
        findings.append(Finding(
            CHECK_NAME, "pass",
            f"every ruling in {report.files_read} non-superseded RATIFICATION file(s) "
            f"({report.rulings_read} read) is landed or inside the {_dc.GRACE_BATCHES}-batch "
            f"grace period"))
    return findings
