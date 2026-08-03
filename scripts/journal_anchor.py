#!/usr/bin/env python
"""journal_anchor.py — the ADR-85 anchoring predicate, defined ONCE.

ADR-85 amendment 2026-08-03. Two organs enforce that amendment:

  * `block_unanchored_push.py` — the HARD leg at pre-push (§A5 / FR1-FR2), over the
    range git hands the hook.
  * `audit.check_journal_spine_anchor` — the audit backstop (§A8 / FR4), over
    `git log --first-parent main` above the dated disposition floor.

They MUST agree about what "anchored" means, so the predicate lives here and both import
it — the same reuse-integrity shape `block_ff_push` already uses for its FF-signature
(`validate_no_ff.find_violations`). A second definition is a drift edge, not a convenience.

THE PREDICATE (ADR-85 §A7, ratified 2026-08-03):

    A first-parent spine entry is ANCHORED when JOURNAL.md names >= 1 SHA that the entry
    INTRODUCED -- not the entry's own SHA.

A merge commit cannot name its own hash: the JOURNAL entry it carries is authored before
the merge exists. Measured at 4f3f8531, the naive "spine SHA is named" predicate reports
686 of 1292 spine entries unanchored INCLUDING HEAD ITSELF; the correct predicate gives a
contiguous anchored run of 11 from HEAD. An implementation on the naive predicate fails on
its own merge — which is why this docstring states it rather than leaving it to a reader.

Matching is on the 7-char short prefix, so any reference length (7..40) is caught — the
same convention `session_end_backpressure._commit_anchors_journal` has always used.

Layer-2 contract (ADR-28/36): read-only. This module runs git plumbing reads and string
matches; it writes nothing, anywhere.

FAIL-LOUD: every helper raises `AnchorError` on a git failure. Callers decide the posture
-- the hard organs fail CLOSED (ADR-85 §A6 / FR6), never swallowing an error into a pass.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

_JOURNAL = "JOURNAL.md"
_SHORT = 7

# ADR-85's dated disposition floor is read FROM THE ADR, never hardcoded here and never
# re-derived. FR4: "Floor read from the ADR, never re-derived and never widened in code."
# Keeping the constant out of code is the point: a floor that lives in a Python literal can
# be widened in a commit that reads like a refactor, whereas widening it here requires
# editing the ratified ADR, which is a visible governance act.
_ADR_PATH = "docs/decisions/ADR-85-session-lifecycle-enforcement.md"
_FLOOR_RE = re.compile(r"Dated disposition floor:\s*`([0-9a-f]{7,40})`")


class AnchorError(RuntimeError):
    """A git read failed, or a required governance input is missing/unparseable."""


def _git(repo: Path, *args: str) -> str:
    """Run a read-only git command in `repo`; raise AnchorError on failure.

    Deliberately NOT fail-soft. An unreadable history is an unknown anchoring state, and
    an unknown state must never render as "anchored" -- that is the exact defect class the
    ADR-85 amendment exists to remove.
    """
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=60)
    except Exception as exc:  # noqa: BLE001 -- surfaced, never swallowed
        raise AnchorError(f"git {' '.join(args)} failed to run: {exc!r}") from exc
    if r.returncode != 0:
        raise AnchorError(f"git {' '.join(args)} exited {r.returncode}: {r.stderr.strip()}")
    return r.stdout


def floor_sha(repo: Path) -> str:
    """The dated disposition floor SHA, parsed from the ratified ADR-85 amendment.

    Raises AnchorError when the ADR is missing or the floor line is unparseable. That is
    deliberate: a backstop that silently defaults to "no floor" would either flood on
    inherited history or, worse, quietly widen its own exemption.
    """
    path = repo / _ADR_PATH
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise AnchorError(f"cannot read {_ADR_PATH}: {exc!r}") from exc
    # EXACTLY ONE declaration, never "the first match" (terra HIGH, 2026-08-03). With
    # `search()` a second floor line -- an amendment that adds one without removing the old,
    # or a malformed line beside a valid one -- silently selects whichever appears first,
    # quietly changing which history is exempted. An ambiguous exemption boundary is not a
    # boundary; it fails closed like a missing one.
    found = _FLOOR_RE.findall(text)
    if not found:
        raise AnchorError(
            f"no 'Dated disposition floor: `<sha>`' line found in {_ADR_PATH} -- the "
            "ADR-85 backstop cannot run without its ratified floor")
    if len(set(found)) > 1:
        raise AnchorError(
            f"{len(found)} DIFFERENT disposition floors declared in {_ADR_PATH} "
            f"({', '.join(sorted(set(found)))}) -- an ambiguous exemption boundary is not a "
            "boundary; resolve the ADR to exactly one")
    return found[0]


def journal_text(repo: Path, rev: str | None = None) -> str:
    """JOURNAL.md content -- at `rev` when given, else the working tree.

    The pre-push organ reads it at the LOCAL TIP being pushed (the anchor commit is inside
    the range, so the working tree and the tip can differ); the audit backstop reads the
    working tree, which is what a ship-gate run is judging.
    """
    if rev is None:
        try:
            return (repo / _JOURNAL).read_text(encoding="utf-8")
        except OSError as exc:
            raise AnchorError(f"cannot read {_JOURNAL}: {exc!r}") from exc
    return _git(repo, "show", f"{rev}:{_JOURNAL}")


def spine_entries(repo: Path, rev_range: str) -> list[str]:
    """First-parent spine entries in `rev_range`, newest-first.

    `rev_range` is any git log positional -- `A..B` for a push range, or a bare ref like
    `main` for the backstop. `--first-parent` is what makes this the SPINE (ADR-85 §A7:
    the anchored object is the spine entry, not every reachable commit).
    """
    out = _git(repo, "log", "--first-parent", "--format=%H", rev_range)
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def introduced(repo: Path, sha: str) -> list[str]:
    """The commits a spine entry INTRODUCED: `firstparent..sha`, plus the entry itself.

    For a `--no-ff` merge this is the merge plus every commit the merged branch brought
    in -- which is where the branch's JOURNAL anchor lives. For a non-merge spine entry
    (§A9) it is just the entry: structurally unanchorable at push time, since no JOURNAL
    can name a SHA that does not yet exist. A root commit has no first parent and likewise
    introduces only itself.
    """
    parents = _git(repo, "rev-list", "--parents", "-n", "1", sha).split()
    if len(parents) < 2:          # root commit: no first parent
        return [sha]
    first_parent = parents[1]
    out = _git(repo, "rev-list", f"{first_parent}..{sha}")
    brought = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return brought or [sha]


def is_anchored(repo: Path, sha: str, journal: str) -> bool:
    """True iff `journal` names >= 1 SHA the spine entry `sha` introduced (§A7)."""
    return any(c[:_SHORT] in journal for c in introduced(repo, sha))


def unanchored_in_range(repo: Path, rev_range: str, journal: str) -> list[str]:
    """Spine entries in `rev_range` that no JOURNAL text anchors -- newest-first.

    NOTE the asymmetry with `unanchored_on_spine`, and it is intentional per FR2: the
    pre-push organ's discharge is RANGE-level ("a JOURNAL entry naming >= 1 SHA in that
    range"), so callers treat a non-empty return as a refusal only when NO entry in the
    range is anchored. This function reports per-entry facts; the range verdict is
    `range_is_anchored` below, so the two rules cannot drift apart in a caller.
    """
    return [s for s in spine_entries(repo, rev_range) if not is_anchored(repo, s, journal)]


def range_is_anchored(repo: Path, rev_range: str, journal: str) -> bool:
    """FR2's range-level discharge: >= 1 spine entry in the range is anchored.

    An empty range is vacuously anchored -- there is nothing being integrated, so there is
    no obligation (§A1: the obligation is created by integration, not by authorship).
    """
    entries = spine_entries(repo, rev_range)
    if not entries:
        return True
    return any(is_anchored(repo, s, journal) for s in entries)


def unanchored_on_spine(repo: Path, ref: str, floor: str, journal: str) -> list[str]:
    """Backstop scan (FR4): unanchored spine entries on `ref` at/above the dated `floor`.

    Per-entry, not range-level: the backstop's job is to make a `--no-verify` bypass
    visible after the fact, so it asks the stricter question of every entry above the
    floor. Entries strictly older than `floor` are dispositioned once by the ADR-85
    amendment §A8 and are not scanned.

    Raises AnchorError when `floor` is not an ancestor of `ref` -- an unverifiable floor is
    an error, never an empty (clean-looking) result.
    """
    try:
        _git(repo, "merge-base", "--is-ancestor", floor, ref)
    except AnchorError as exc:
        raise AnchorError(
            f"disposition floor {floor[:9]} is not an ancestor of {ref}: {exc}") from exc
    entries = spine_entries(repo, f"{floor}..{ref}")
    floor_full = _git(repo, "rev-parse", floor).strip()
    entries = [s for s in entries if s != floor_full]
    return [s for s in entries if not is_anchored(repo, s, journal)]


def describe(repo: Path, sha: str) -> str:
    """`<short> (<date>) <subject>` for an operator-facing refusal line."""
    try:
        return _git(repo, "log", "-1", "--format=%h (%ad) %s", "--date=short", sha).strip()
    except AnchorError:
        return sha[:9]
