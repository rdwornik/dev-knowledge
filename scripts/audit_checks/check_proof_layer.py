"""`check_proof_layer` — the `[#596]` family-3 proof layer as a registered gate.

The thin ADAPTER half; the class, its predicate and its honest limits live in
`scripts/proof_layer.py`, which is the durable home the row asks for.

WHAT IT REPORTS. Every environment-conditional guard under `tests/` — a proof whose firing is
gated, by `skipif` or a tool-presence probe, on the presence of the environment it polices —
against a committed identity baseline, so the class cannot silently re-form.

WHY A REGISTERED CHECK RATHER THAN A TEST. A test asserting "no new guards" would itself be a
test, and this class is precisely about proofs that stop running without saying so. A
registered check reports into the audit table on every run, where a reader sees the cell. That
is the sweep's own §9.6 remedy applied to itself: *"propagate the skip predicate into the
reporting surface, so a skipped proof is rendered as NOT PROVEN rather than absorbed into a
green run."*

WARN-TIER, on the `funnel_coverage` ruling and for the reason that module records: the live
population is pre-existing debt this row did not create, and arming RED against an unmeasured
corpus turns the gate off on day one. The teeth are the identity keying and the named
regression — a NEW guard surfaces by name even while an old one drains, which a counter cannot
do.

MEASURED BEFORE ARMING: 38 environment-conditional guards across 13 test modules, 38 distinct
identities, 5 of them gated on an enforcement RUNNER — including both of the sweep's named
exemplars (`tests/test_enforcement_coverage.py` §9.3 and `tests/test_floor_conformance.py`
§9.4). Enumerated by name in `ecosystem/proof-layer-baseline.json`.

FAIL-CLOSED ON ITS OWN INPUTS. A `tests/` module that cannot be parsed is reported by name,
never counted clean — counting an unreadable input as clean is this very class reached through
the scanner. An absent `tests/` directory is `n/a` (subject-absent), and `unavailable` is not
used anywhere here: `_STATUS_LABEL` renders it as "N/A" and `_check_outcome` projects it onto
`pass`, which is the green-by-skip shape the whole family is about.

HONEST LIMITS — the logic module's own, restated because they bound a clean run:
  * it reads `skipif` marks and module-level `pytestmark`; a bare `pytest.skip()` in a test
    body, or a skip reached through a fixture, is NOT detected;
  * `self_policing` is a declared roster (`ENFORCEMENT_RUNNERS`), not an inference about
    intent — a guard on `git` or `pwsh` may still be self-policing in a module whose subject
    IS that tool;
  * a guard on the list is a QUESTION, not a verdict. The sweep's §9.2 exemplar is
    load-bearing and correct where it lives; what it praises is that win-tooling paid to route
    the unskippable property out from behind the guard.

Child-repo-safe: a repo with no `tests/` yields `n/a`. Read-only (Layer 2): no git, no writes.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding, _na, _NA_SUBJECT_ABSENT

try:
    from scripts import proof_layer as _pl
except ImportError:
    import proof_layer as _pl

CHECK_NAME = _pl.CHECK_NAME


def check_proof_layer(repo_path: Path) -> list[Finding]:
    """`[#596]`: a proof that can be skipped on the machine that breaks the property.

    One Finding PER guard, never a bundle. The `#147` register suppresses an ENTIRE Finding on
    a substring match, so a bundled Finding would let one dispositioned guard wave through
    every other one sharing the line.
    """
    root = Path(repo_path)
    tests_dir = root / "tests"
    if not tests_dir.is_dir():
        return [_na(CHECK_NAME, _NA_SUBJECT_ABSENT,
                    "no tests/ — this repo carries no proof layer to measure")]

    try:
        guards, unreadable = _pl.scan_guards(tests_dir, report_unreadable=True)
    except OSError as exc:
        return [Finding(CHECK_NAME, "fail",
                        f"could not scan tests/ for environment-conditional guards, so none "
                        f"was measured: {exc!r}".replace("|", "/"))]

    baseline = _pl.load_baseline(root)
    out = [Finding(CHECK_NAME, status, evidence.replace("|", "/"))
           for status, evidence in _pl.ratchet_findings(guards, baseline, unreadable)]
    if not out:
        self_policing = sum(1 for g in guards if g.self_policing)
        out.append(Finding(
            CHECK_NAME, "pass",
            f"{len(guards)} environment-conditional guard(s) across "
            f"{len({g.module for g in guards})} test module(s), all at the committed "
            f"baseline; {self_policing} gated on an enforcement runner (the sharpest form). "
            f"A guard here is a question, not a verdict — see scripts/proof_layer.py"))
    return out
