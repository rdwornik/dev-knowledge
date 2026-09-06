#!/usr/bin/env python
"""block_unanchored_push.py — the ADR-85 HARD leg, at pre-push, scoped to `main`.

ADR-85 amendment 2026-08-03 (§A5 / FR1-FR2). This is the organ that replaces the Stop
hook's hard JOURNAL gate. It exists because of one structural fact:

    A Stop hook cannot host a hard gate. Its unit is a model-turn boundary, and the host
    force-ends a turn after N consecutive blocks. On 2026-08-03 nine identical firings
    added zero enforcement pressure and terminated in exactly the silent auto-bypass
    ADR-85 Decision 4 forbids by name. An organ that can be EXHAUSTED cannot carry teeth.

A pre-push hook cannot be exhausted: it passes, or the push fails. There is no retry
surface. And the range it judges is the one **git itself hands the hook**
(`remote_sha..local_sha`) -- exact, bounded by construction, with no invented base, no
floor and no cap. That is what dissolved the two derivations' disagreement about what
should replace the old `@{upstream}` base: nothing needed to, once the organ moved.

WHAT IT ENFORCES (FR1/FR2)
  Obligation : the first-parent spine entries inside the push range to `main`.
               A push that does not target `main` is not this organ's business.
  Discharge  : a JOURNAL entry naming >= 1 SHA that a spine entry in the range
               INTRODUCED (the §A7 predicate -- a merge cannot name its own hash).
               RANGE-level per FR2: one anchor in the range discharges the range.
  Escape     : `git push --no-verify`, explicit and human-typed, pretending to be
               nothing else. It is made non-silent by the audit backstop
               (audit.check_journal_spine_anchor, §A8/FR4), which keeps reporting the
               gap until a JOURNAL anchor lands.

WHAT IT IS NOT
  Not an authorship check. Commits parked on a feature branch awaiting operator GO create
  NO obligation (§A1/§A4) -- no integration has occurred, so a feature-branch push is
  outside this organ's hard path entirely. No agent-asserted state is an input anywhere
  (FR7): the inputs are git history and JOURNAL.md content, both recorded facts.

EXIT CODES -- fail CLOSED (§A6/FR6; model `check_seal_identity.py:73-77`)
  0  clean scan: not a push to main, empty range, or the range is anchored -> allow
  1  detected non-compliance: no spine entry in the range is anchored -> refuse
  2  internal error / indeterminate -> REFUSE. An error is never a silent allow.

Layer-2 contract (ADR-28/36): read-only. Reads git and JOURNAL.md; writes nothing.

Reuse-integrity: the push-range resolver is imported from `block_ff_push` (the sibling
pre-push organ) and the anchoring predicate from `journal_anchor`, so the two pre-push
gates cannot disagree about what "a push to main" is, and this organ cannot disagree with
the audit backstop about what "anchored" means.

  The MESSAGE is now imported from there too (batch U, lane-u-000-branch-enum-parity).
  Sharing the predicate as code while restating it as prose left this organ printing "add
  a JOURNAL entry naming >=1 SHA this push introduces" -- true, and silent about both
  exclusions a seat actually trips over. `journal_anchor.SPINE_PREDICATE` and
  `SPINE_DIAGNOSTIC` are the one wording, quoted; see AF-1 for the eight false alarms in
  one day that made restating this rule a recorded defect class rather than a style note.

THE LANE ENUM IS NOT READ HERE, AND THAT IS THE POINT (ADR-110 amendment 2026-08-07 R-1
containment). Three organs iterate the lane-branch enum: `validate_substrate` leg 5, the
ADR-110 declared-integration-arc exemption in `audit.check_journal_spine_anchor`, and the
batch teardown. This organ is deliberately not a fourth. The exemption forgives a
`worktree-lane-*` merge at COMMIT time while a batch manifest is open, because a batch's
JOURNAL entry names the lane merge SHAs and so cannot exist until after them; nothing
makes the same argument at PUSH time, where the range is what actually ships. Both halves
are pinned by test:
  * `tests/test_batch_manifest.py::test_the_pre_push_organ_does_not_consult_the_manifest_at_all`
    -- structural: neither this module nor `journal_anchor` may import `batch_manifest`.
  * `tests/test_adr85_integration_enforcement.py::test_t5d_the_r1_exemption_does_not_reach_the_pre_push_refusal`
    -- behavioural: the exact pair `audit-health` forgives is still refused here.

  THE COST OF THAT ASYMMETRY IS A SURPRISE, and the refusal now spends two lines removing
  it. A seat reads `audit.py health` -> `[OK] journal_spine_anchor`, concludes its push
  will pass, and is refused by this organ for the very merges health had just declared
  exempt -- with nothing on either surface saying the two organs answer different
  questions. Green health is not a prediction about this gate. It says so out loud below.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import block_ff_push as _bfp        # noqa: E402  -- shared range resolver
import journal_anchor as _ja        # noqa: E402  -- shared anchoring predicate

PROTECTED_REF = _bfp.PROTECTED_REF  # single source: refs/heads/main

#: The organ's name in the [#529] store -- the pre-commit hook id, as in the sibling.
HOOK_NAME = "block-unanchored-push"

# [#529] telemetry: the SAME objects the sibling defines, never a second copy. This organ
# already single-sources its range resolver and its anchoring predicate for exactly this
# reason -- two pre-push organs that disagreed about whether telemetry is on would be two
# organs, not one mesh. Reuse-integrity is asserted by tests/test_hook_telemetry.py.
telemetry_enabled = _bfp.telemetry_enabled
telemetry_db = _bfp.telemetry_db
_emit_verdict = _bfp._emit_verdict


def _local_tip(stdin_lines, env, protected: str = PROTECTED_REF) -> str | None:
    """The local SHA being pushed to `protected` -- the tip whose JOURNAL.md is judged.

    The anchor commit lives INSIDE the range, so the JOURNAL that discharges the push is
    the one at the local tip, not necessarily the one in the working tree (they differ
    whenever the push is issued from a different branch, or the tree has moved on).
    Mirrors `block_ff_push.resolve_push_range`'s two wirings: native stdin first, then
    pre-commit's PRE_COMMIT_* env.
    """
    for _local_ref, local_sha, remote_ref, _remote_sha in stdin_lines:
        if remote_ref == protected:
            return local_sha
    if env.get("PRE_COMMIT_REMOTE_BRANCH", "") == protected:
        return env.get("PRE_COMMIT_TO_REF", "") or None
    return None


# rule: seal-journal-spine-anchor
def main(argv=None) -> int:
    """Refuse (1) a push putting unanchored spine entries on main; allow (0); refuse (2) on error.

    A THIN wrapper over `_verdict`, added by the [#529] wiring: the decision stays in one place
    and the telemetry sits strictly after it, unable to change the code it is handed. With the
    switch off `_emit_verdict` returns immediately, so this is `_verdict` and nothing else."""
    started = time.perf_counter()
    verdict: dict = {}
    code = _verdict(argv, verdict)
    _emit_verdict(HOOK_NAME, verdict.get("repo"), code, started, verdict.get("reason"))
    return code


def _verdict(argv, verdict: dict) -> int:
    try:
        repo = _bfp._repo_root()
        verdict["repo"] = repo
        lines = _bfp.parse_stdin_lines(_bfp._read_stdin())
        rng = _bfp.resolve_push_range(lines, os.environ)
        reconstructed = False
        # pre-commit consumes stdin and re-exposes only ONE ref pair, so it can hide main on a
        # multi-ref push or an empty-remote initial push. Without this, such a push carrying
        # unanchored main work returns 0 and bypasses the hard leg (terra HIGH, 2026-08-03).
        # block_ff_push already reconstructs main's range from local refs for exactly this
        # case; the anchor gate has to do the same or it is weaker than its sibling on the
        # wiring the fleet actually runs under.
        if rng is None and not lines and _bfp._under_precommit(os.environ):
            rng = _bfp._reconstruct_main_range(repo, os.environ)
            reconstructed = rng is not None
        if rng is None:
            return 0  # not a push to main (or a main deletion) -- not this organ's business
        # On the reconstructed path the tip IS local main: the forwarded ref named something
        # else, so `_local_tip` would return None or a foreign tip and the JOURNAL would be
        # read at the wrong revision.
        tip = _bfp._rev_parse(repo, PROTECTED_REF) if reconstructed else _local_tip(lines, os.environ)
        journal = _ja.journal_text(repo, tip)
        entries = _ja.spine_entries(repo, rng)
        if not entries:
            return 0  # nothing being integrated -> no obligation (§A1)
        anchored = _ja.range_is_anchored(repo, rng, journal)
    except Exception as exc:  # noqa: BLE001 -- §A6/FR6: fail CLOSED, never a silent allow
        print(f"block_unanchored_push: INTERNAL ERROR ({exc!r}) — refusing the push. "
              "An unknown anchoring state is not a clean one (ADR-85 §A6). Fix the hook, "
              "or bypass explicitly with `git push --no-verify` — the audit backstop will "
              "keep reporting the gap until a JOURNAL anchor lands.", file=sys.stderr)
        verdict["reason"] = f"internal error: {type(exc).__name__}"
        return 2
    if anchored:
        return 0
    verdict["reason"] = (f"{len(entries)} first-parent spine entry(ies) with no JOURNAL anchor "
                         "(ADR-85 amendment 2026-08-03 §A5)")
    print(f"block_unanchored_push: REFUSED — {len(entries)} first-parent spine entry(ies) "
          "would land on main with no JOURNAL anchor (ADR-85 amendment 2026-08-03 §A5):",
          file=sys.stderr)
    for sha in entries:
        print(f"  UNANCHORED  {_ja.describe(repo, sha)}", file=sys.stderr)
    print("  fix: add a JOURNAL entry naming >=1 SHA this push introduces, commit it, "
          "and push again.", file=sys.stderr)
    # The predicate and the diagnostic are QUOTED from the single source, never restated --
    # the leading "; " each carries is for the backstop's one-line evidence string, so they
    # are stripped here where the message is already line-oriented.
    for _part in (_ja.SPINE_PREDICATE, _ja.SPINE_DIAGNOSTIC):
        print("  " + _part.lstrip("; "), file=sys.stderr)
    # CONTAINMENT, said at the moment it bites (batch U). Without this a seat holding a green
    # `audit.py health` reads this refusal as a bug in one of the two organs and reaches for
    # --no-verify, which is the one outcome ADR-85 Decision 4 forbids by name.
    print("  NOTE — a green `audit.py health` does NOT predict this gate. The ADR-110 "
          "declared-integration-arc exemption (amendment 2026-08-07 R-1) lets the audit "
          "backstop SKIP a `worktree-lane-*` merge while a committed manifest declares an "
          "open batch; it deliberately does not reach this organ, so the range-level refusal "
          "stays unconditional and nothing ships unanchored. The two organs are not in "
          "conflict — they answer different questions, and this one is the shipping one.",
          file=sys.stderr)
    print("  bypass: `git push --no-verify` — explicit and logged by its absence; the "
          "audit backstop FAILs until an anchor lands.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
