"""`CLAUDE.md`'s boot cost, asserted IN BYTES — the gate the line budget never was.

`CLAUDE.md` is auto-read at the start of every Claude Code session in this repo, so its
size is a cost paid per session, not per edit. Until this module the only budget on it was
ADR-53's **≤200 lines**, enforced WARN-only by `validate_doc_rot._FILE_SIZE_BUDGETS`. That
budget was satisfied and the file still grew: at the 2026-08-29 freeze it measured **240
physical lines / 39,588 B**, i.e. **165 B per line** against the ~117 B/line this corpus
averages (the figure `tests/test_agents_md_byte_cap.py` records for the same estate).

A line count is gameable by density. Bytes are not. This module is the byte gate.

WHY 24,576 B, and why that number is not chosen after the fact
--------------------------------------------------------------
The ceiling is ADR-53's own ≤200-line claim **re-denominated** in the metric the claim was
trying to bound, rounded up to the next binary KiB. Three independent derivations land on
the same place:

* 200 lines x ~117 B/line (this corpus's measured density) = 23,400 B
* 200 lines x ~124 B/line (this file's density once re-genred to ordinary prose) = 24,800 B
* the eight frozen `owner=hub` regions cost 7,607 B that this repo cannot edit at all
  (they are byte-matched to `templates/claude-regions/*.md`); a 16 KiB budget for the
  repo-owned remainder puts the total at 23,991 B

So the ceiling encodes the intent ADR-53 always had, and is not reverse-engineered from
whatever the re-genre happened to produce. It is deliberately TIGHT: at the v2.69 landing
the file sits at 23,931 B, leaving ~645 B. That is the design, and it matches how this repo
already runs its line budget (`CLAUDE.md` v2.68: "Closes 196/200, headroom 4 — bought, not
shaved"). Room for a new rule is **bought by condensing**, not by raising the ceiling.

THE LINE BOUND IS KEPT, NOT REPLACED
------------------------------------
ADR-53's ≤200 lines is ratified doctrine, restated in ADR-115 and in several
`protocols/PLAYBOOK.md` sites. This module adds a second, binding budget; it does not
retire the first, and `validate_doc_rot._FILE_SIZE_BUDGETS` is untouched. Promoting the
byte bound into ADR-53 / ADR-115 / PLAYBOOK is a separate, owed act.

NOT THE CODEX CAP -- stated because the sibling module rules the other way, deliberately
--------------------------------------------------------------------------------------
`tests/test_agents_md_byte_cap.py` considered and REJECTED asserting `CLAUDE.md` against
Codex's 32 KiB `project_doc_max_bytes`, on the correct ground that `CLAUDE.md` is not part
of the Codex payload. Nothing here disturbs that. This is a *different* budget with a
*different* rationale: the cost of the Claude Code session boot, not of a Codex project
doc. The two caps are unrelated numbers that must not be conflated.

WHAT IS REUSED, AND WHERE REUSE STOPS
-------------------------------------
The lane contract names the **pattern** as the reusable artifact, and the split is drawn
where reuse stays honest:

* `payload_bytes` is IMPORTED from the sibling module. It is a pure size helper, and the
  rule it encodes -- `stat().st_size`, never `len(read_text())`, because the budget is on
  bytes on disk and a decode-then-count under-reports every non-ASCII byte and every CRLF
  -- must hold identically for both gates. One site, no drift.
* `assert_within_cap` is NOT imported. Its failure message is Codex-specific by design
  ("Codex instruction payload ... EXCEEDS the project_doc_max_bytes cap"), and emitting
  that text for a `CLAUDE.md` overrun would name the wrong consumer and the wrong cap. A
  gate whose diagnostic lies about what it measured is the failure this repo keeps
  refusing. The shape below is the sibling's; the wording is this budget's.

HONEST LIMITS
-------------
* This gate measures SIZE, never QUALITY. A file that stays under the ceiling by deleting
  a load-bearing rule passes. The no-deletion discipline (every removal is a relocation to
  a named destination) is a review obligation this module cannot enforce.
* `CLAUDE.md`'s `@`-imports (`@AGENTS.md`, `@.claude/generated/*.md`,
  `@.claude/methodology-roster.md`) are expanded by the Claude Code runtime at read time.
  This gate measures the file on disk, so the real session payload is LARGER than the
  figure asserted here. Bounding the expanded payload is a different, unbuilt gate.
"""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

import pytest
from test_agents_md_byte_cap import payload_bytes

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: `CLAUDE.md`'s own boot budget. See the module docstring for the derivation. NOT Codex's
#: `project_doc_max_bytes` -- a different cap, for a different consumer, at a different size.
CLAUDE_MD_CAP_BYTES = 24 * 1024

CLAUDE_MD = _REPO_ROOT / "CLAUDE.md"

#: The header's declared ceiling, e.g. `≤24,576 B`. The `B` is required so ADR-53's
#: `≤200 lines` cannot match. Kept in agreement with the constant above by
#: `test_declared_ceiling_agrees_with_the_gate`.
_DECLARED_CEILING_RE = re.compile(r"≤\s*([\d,]+)\s*B\b")


def assert_within_cap(doc: Path, cap: int = CLAUDE_MD_CAP_BYTES) -> int:
    """Assert `doc` fits under `cap`. Returns the measured size in bytes.

    Same shape as `test_agents_md_byte_cap.assert_within_cap` -- refuse a missing file
    rather than counting it as zero, measure, then assert -- with wording that names THIS
    budget. Parametrised on both the path and the cap so the planted-oversize tests below
    exercise the real assertion against synthetic files instead of the real one.
    """
    assert doc.is_file(), f"session boot contract missing: {doc}"
    total = payload_bytes(doc)
    assert total <= cap, (
        f"{doc.name} is {total:,} B and EXCEEDS its session boot budget of {cap:,} B by "
        f"{total - cap:,} B. This file is auto-read at every session start, so the overrun "
        "is paid per session. Buy the room by condensing and relocating to a named "
        "destination -- do not raise the ceiling (see this module's docstring)."
    )
    return total


def test_claude_md_is_within_its_byte_budget() -> None:
    """The live gate: `CLAUDE.md` on disk, in bytes, under its own ceiling."""
    total = assert_within_cap(CLAUDE_MD)
    # Surfaced so a `-s` run reports the live figure rather than a remembered constant.
    print(
        f"\nCLAUDE.md {total:,} B = {total / CLAUDE_MD_CAP_BYTES:.1%} of "
        f"{CLAUDE_MD_CAP_BYTES:,} B  (headroom {CLAUDE_MD_CAP_BYTES - total:,} B)"
    )


def test_claude_md_is_not_hollow() -> None:
    """The emptiness floor, for the reason the sibling module states.

    A cap assertion only ever fails UPWARDS, so a truncated or blanked `CLAUDE.md` would
    make this gate GREENER, not redder -- the "looks armed, measures nothing" failure.
    `assert_within_cap` already refuses a *missing* file; this refuses a *hollow* one. The
    floor is deliberately far below any plausible real value: it catches truncation, and
    makes no claim about what the file ought to contain.
    """
    size = CLAUDE_MD.stat().st_size
    assert size > 4096, (
        f"{CLAUDE_MD} is {size:,} B -- implausibly small for a session boot contract. A "
        "hollowed file makes the cap assertion pass by measuring nothing."
    )


def test_declared_ceiling_agrees_with_the_gate() -> None:
    """`CLAUDE.md`'s prose may not name a ceiling the gate does not enforce.

    The file's own §4 forbids restating a number in prose without the surface that computes
    it. The header declares the budget for a human reader, so that declaration is checked
    against this module's constant rather than trusted -- otherwise the doc could advertise
    one ceiling while the gate held another, which is the exact drift class this repo keeps
    re-learning.
    """
    declared = _DECLARED_CEILING_RE.findall(CLAUDE_MD.read_text(encoding="utf-8"))
    assert declared, (
        f"{CLAUDE_MD} declares no byte ceiling matching {_DECLARED_CEILING_RE.pattern!r}. "
        "The gate is armed but the file no longer tells a reader what it is bound by."
    )
    for raw in declared:
        assert int(raw.replace(",", "")) == CLAUDE_MD_CAP_BYTES, (
            f"CLAUDE.md declares a ceiling of {raw} B while this gate enforces "
            f"{CLAUDE_MD_CAP_BYTES:,} B. Reconcile them -- a doc that advertises a budget "
            "nothing holds is worse than one that advertises none."
        )


# ------------------------------------------------------------------ planted oversize (RED)


def _plant(directory: Path, size: int) -> Path:
    """Write a synthetic doc of an exact byte size. No real file is touched."""
    doc = directory / "CLAUDE.md"
    doc.write_bytes(b"c" * size)
    return doc


def test_planted_oversize_is_refused() -> None:
    """cap+1 must FAIL -- proof this gate can fire, not merely that it is green today.

    Uses `tempfile` rather than the `tmp_path` fixture for the reason the sibling module
    gives: the one test that is the whole point of the module should not share a fixture
    surface that has been RED on `main`.
    """
    with tempfile.TemporaryDirectory() as td:
        doc = _plant(Path(td), CLAUDE_MD_CAP_BYTES + 1)
        assert payload_bytes(doc) == CLAUDE_MD_CAP_BYTES + 1
        with pytest.raises(AssertionError, match=r"EXCEEDS its session boot budget"):
            assert_within_cap(doc)


def test_planted_doc_at_exactly_the_cap_passes(tmp_path: Path) -> None:
    """The boundary is inclusive -- exactly at the ceiling is not over it."""
    doc = _plant(tmp_path, CLAUDE_MD_CAP_BYTES)
    assert assert_within_cap(doc) == CLAUDE_MD_CAP_BYTES


def test_missing_doc_is_refused_not_counted_as_zero(tmp_path: Path) -> None:
    """A vanished boot contract must RED, never shrink the measurement into a silent pass."""
    with pytest.raises(AssertionError, match=r"session boot contract missing"):
        assert_within_cap(tmp_path / "nope.md")
