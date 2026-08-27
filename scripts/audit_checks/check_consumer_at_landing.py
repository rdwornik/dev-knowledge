"""`check_consumer_at_landing` — the `[#595]` subtraction mechanism as a registered gate.

The thin ADAPTER half; the logic lives in `scripts/consumer_at_landing.py`. Same shape as
`check_funnel_coverage` (its closest sibling — same corpus, different question: that one asks
whether an artifact was DISPOSITIONED, this one whether anything CONSUMES it).

WHY IT IS A GATE. The diagnostic's own diagnosis of why the class is invisible: *"The fleet
instruments LANDING and never CONSUMPTION, so accumulation is invisible by construction."*
Landing is the one moment a commit-time gate can reach, so that is where the declaration is
asked for.

TWO ARM LEVELS, and each is measured rather than chosen.

  * **Leg 1 — declaration at landing: FAIL.** An artifact landing on/after 2026-08-27 carries
    at least one governance citation or an explicit `no-consumer: <reason>`. Measured before
    arming: **99 of the 109 artifacts landed since 2026-08-20 already pass**, and the
    post-cutoff corpus measures **0**, so arming cannot RED a clean tree — the
    `check_adr_status_grammar` evidence bar. The ten that would not pass are probe reports and
    research memos, i.e. exactly the accumulating class the row names.
  * **Leg 2 — the consumption ratchet: WARN.** `funnel_coverage`'s ruling applies unchanged:
    arming RED against an unmeasured corpus turns the gate off on day one, because everyone
    routes around a gate that blocks work for a debt they did not create. Arm-time debt is 516
    unconsumed of 737, enumerated BY NAME in `ecosystem/audit-consumer-baseline.json`.

`info` RATHER THAN A PASS WHEN CITATIONS CANNOT BE RESOLVED — the row's third leg, and it
short-circuits both others. An unreadable governance pool produces the same "nothing
unconsumed" number as a fully-cited one, and those are not the same fact.

Note what `info` is spelled as: **`warn`**, deliberately not `unavailable`. `_STATUS_LABEL`
renders `unavailable` as "N/A", `_check_outcome` projects it onto `pass`, and `cmd_ship_gate`
blocks only on `fail` plus undispositioned `warn` — so an `unavailable` verdict SHIPS GREEN
having measured nothing. That is the green-by-skip class the 2026-08-25 sweep closed.

HONEST LIMITS — the logic module's own, restated because they bound a green verdict:
  * the landing leg checks that an artifact NAMES a governance surface, not that the surface
    exists or agrees. `[#99999]` passes;
  * consumption is a substring match over the pool, as the diagnostic's was: a row naming an
    artifact only to call it obsolete counts as a citer;
  * `no-consumer:` is honoured on its reason's LENGTH, which separates a recorded reason from
    a token and nothing more.

Child-repo-safe: a repo with no `docs/audits/` yields `n/a` (subject-absent), not a FAIL.
Read-only (Layer 2): no git, no writes.
"""

from __future__ import annotations

from pathlib import Path

from ._common import Finding, _na, _NA_SUBJECT_ABSENT

try:
    from scripts import consumer_at_landing as _cal
except ImportError:
    import consumer_at_landing as _cal

CHECK_NAME = _cal.CHECK_NAME


def check_consumer_at_landing(repo_path: Path) -> list[Finding]:
    """`[#595]`: a landed `docs/audits/` artifact declares its consumer, and the unconsumed
    set does not grow.

    One Finding PER concern, never a bundle. The `#147` register suppresses an ENTIRE Finding
    on a substring match, so a bundled Finding would let one dispositioned artifact wave
    through every other regression sharing the line — the reason `funnel_coverage` emits one
    per artifact and `git_backlog_drift` one per drifted id.
    """
    root = Path(repo_path)
    if not (root / _cal.AUDITS_RELPATH).is_dir():
        return [_na(CHECK_NAME, _NA_SUBJECT_ABSENT,
                    f"no {_cal.AUDITS_RELPATH}/ — this repo carries no audit corpus")]

    try:
        m = _cal.measure(root)
    except _cal.ConsumerScanError as exc:
        # FAIL, not "unavailable": a corpus that was not fully read yields no trustworthy
        # number, and a low number reads as good news.
        return [Finding(CHECK_NAME, "fail",
                        f"the audit corpus could not be scanned, so no consumption number "
                        f"from this run is trustworthy: {exc}".replace("|", "/"))]

    baseline = _cal.load_baseline(root)
    out = [Finding(CHECK_NAME, status, evidence.replace("|", "/"))
           for status, evidence in _cal.ratchet_findings(m, baseline)]
    if not out:
        out.append(Finding(
            CHECK_NAME, "pass",
            f"{len(m.corpus)} artifact(s): every landing on/after "
            f"{_cal.ARM_DATE.isoformat()} declares a consumer, and the unconsumed set "
            f"({len(m.unconsumed)}) has not grown past the committed baseline "
            f"({m.grandfathered} earlier artifact(s) grandfathered; governance pool "
            f"{m.pool_files} files)"))
    return out
