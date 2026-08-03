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
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import block_ff_push as _bfp        # noqa: E402  -- shared range resolver
import journal_anchor as _ja        # noqa: E402  -- shared anchoring predicate

PROTECTED_REF = _bfp.PROTECTED_REF  # single source: refs/heads/main


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
    try:
        repo = _bfp._repo_root()
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
        return 2
    if anchored:
        return 0
    print(f"block_unanchored_push: REFUSED — {len(entries)} first-parent spine entry(ies) "
          "would land on main with no JOURNAL anchor (ADR-85 amendment 2026-08-03 §A5):",
          file=sys.stderr)
    for sha in entries:
        print(f"  UNANCHORED  {_ja.describe(repo, sha)}", file=sys.stderr)
    print("  fix: add a JOURNAL entry naming >=1 SHA this push introduces, commit it, "
          "and push again (a merge cannot name its own hash — name a commit it brings in).",
          file=sys.stderr)
    print("  bypass: `git push --no-verify` — explicit and logged by its absence; the "
          "audit backstop FAILs until an anchor lands.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
