"""The [#577] byte-cap gate: the Codex instruction payload asserted IN BYTES.

`[#577]`'s done-when requires that "the combined global+root payload is asserted **in
bytes** against the 32 KiB cap by a test". Batch-1 landed `AGENTS.md` and *measured* the
payload, but reported it UNGUARDED -- the figures existed, the gate did not. This module
is that gate.

Why bytes and never lines
-------------------------
Codex truncates a project doc at `project_doc_max_bytes` -- a **byte** budget. This corpus
averages ~117 B/line, so a line ceiling does not bound what the cap measures, and ADR-115
bound (4) states the guard in bytes for exactly that reason. Nothing here asserts a line
count.

WHAT "THE PAYLOAD" IS, and the machine-dependence trade -- decided here, deliberately
--------------------------------------------------------------------------------------
Codex composes the budget from a **global** doc plus the **repo-root** doc. The global one
lives OFF-REPO at `~/.codex/AGENTS.md`, so a test that reads only it passes on the author's
machine and vacuously skips (or REDs) anywhere else, including any future CI.

This module takes option (b) of the three the lane contract offered, split into two tests
so neither half is silent:

* `test_tracked_payload_is_within_cap` is the **hermetic** gate. It reads the repo-root
  `AGENTS.md` and the **tracked in-repo** `codex/AGENTS.md` as the global stand-in. It runs
  everywhere, on any checkout, with no off-repo dependency -- this is the assertion that
  actually holds the line in CI.
* `test_live_codex_payload_is_within_cap` reads the **real** `~/.codex/AGENTS.md` when it
  is present and `skip`s (never passes vacuously) when it is not. This is the half that is
  honest about what Codex on THIS machine actually loads.
* `test_tracked_stand_in_matches_the_live_global` guards the substitution itself. The
  hermetic gate is only meaningful while the tracked stand-in still resembles the live
  global; if they diverge, this test says so rather than letting the hermetic gate keep
  measuring the wrong file. Verified at authoring (2026-08-28): the two are byte-identical
  in **content**, sha256 `991837cb...7642edbcab`, 3,891 B each -- the lane contract claimed
  only identity of *length*, and the stronger claim was confirmed by hashing, not assumed.

**The trade, stated plainly:** the hermetic half can go stale relative to the operator's
real `~/.codex` state, and the live half does not run in CI. Neither is complete alone; the
third test is what keeps the pair from drifting apart quietly. The anti-pattern this repo
keeps re-learning is a gate that looks armed and measures the wrong thing.

THE PLANTED-OVERSIZE HALF
-------------------------
A gate that has never fired is not proven. `assert_within_cap` is parametrised on its two
path arguments precisely so the failing case can be built from `tmp_path` fixtures rather
than by touching the real files: `test_planted_oversize_pair_is_refused` proves the
assertion FAILS at cap+1, and `test_planted_pair_at_exactly_the_cap_passes` pins the
boundary so an off-by-one cannot pass unnoticed.

Measured live at authoring, 2026-08-28 (re-measured by the test at every run, never
compared against a remembered constant):

    ~/.codex/AGENTS.md   3,891 B
    AGENTS.md            5,539 B (107 lines)
    combined             9,430 B = 28.78 % of 32,768
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent

#: Codex's `project_doc_max_bytes` default -- 32 KiB. Named by ADR-115 bound (4) and by
#: `[#577]`'s done-when. A literal, because Codex's own default is not readable from here.
CAP_BYTES = 32 * 1024

#: The repo-root half of the payload -- always read from the tree under test.
ROOT_DOC = _REPO_ROOT / "AGENTS.md"

#: The tracked stand-in for the global half. NOT the file Codex reads (that is
#: `~/.codex/AGENTS.md`); it is the in-repo copy that makes the gate hermetic.
TRACKED_GLOBAL_DOC = _REPO_ROOT / "codex" / "AGENTS.md"

#: The real global doc Codex loads. Off-repo and per-machine -- every use is guarded.
LIVE_GLOBAL_DOC = Path.home() / ".codex" / "AGENTS.md"


def payload_bytes(*docs: Path) -> int:
    """Total size, IN BYTES, of the instruction docs Codex would compose.

    `stat().st_size` and not `len(read_text())`: the cap is applied to bytes on disk, so a
    decode-then-count would under-report every non-ASCII byte and every CRLF.
    """
    return sum(doc.stat().st_size for doc in docs)


def assert_within_cap(*docs: Path, cap: int = CAP_BYTES) -> int:
    """Assert the combined payload of `docs` fits under `cap`. Returns the measured total.

    Parametrised on both the paths and the cap so the planted-oversize tests can exercise
    the real assertion against `tmp_path` fixtures instead of the real files.
    """
    for doc in docs:
        assert doc.is_file(), f"instruction doc missing: {doc}"
    total = payload_bytes(*docs)
    # `parent.name/name` and not `.name`: both halves are literally called `AGENTS.md`, so a
    # bare filename makes the diagnostic ambiguous about WHICH doc grew.
    breakdown = " + ".join(f"{d.parent.name}/{d.name}={d.stat().st_size:,} B" for d in docs)
    assert total <= cap, (
        f"Codex instruction payload {total:,} B EXCEEDS the "
        f"project_doc_max_bytes cap of {cap:,} B by {total - cap:,} B "
        f"({breakdown}). Codex truncates SILENTLY past the cap."
    )
    return total


# --------------------------------------------------------------------------- live payload


def test_tracked_payload_is_within_cap() -> None:
    """The hermetic gate: root doc + tracked global stand-in, in bytes, under the cap.

    The emptiness floor is not decoration. A cap assertion only ever fails UPWARDS, so a
    stand-in that was truncated or blanked would shrink the measured payload and make this
    gate greener, not redder -- the exact "looks armed, measures nothing" failure this module
    exists to refuse. `assert_within_cap` already refuses a *missing* doc; this refuses a
    *hollow* one.
    """
    for doc in (ROOT_DOC, TRACKED_GLOBAL_DOC):
        assert doc.stat().st_size > 0, (
            f"{doc} is empty -- a hollowed instruction doc makes the cap assertion pass by "
            "measuring nothing. The gate would look armed and would not be."
        )
    total = assert_within_cap(ROOT_DOC, TRACKED_GLOBAL_DOC)
    # Surfaced so a `-s` run reports the live figure rather than a remembered constant.
    print(f"\npayload {total:,} B = {total / CAP_BYTES:.2%} of {CAP_BYTES:,} B cap")


def test_live_codex_payload_is_within_cap() -> None:
    """The honest half: the payload Codex on THIS machine actually composes."""
    if not LIVE_GLOBAL_DOC.is_file():
        pytest.skip(f"no off-repo Codex global doc at {LIVE_GLOBAL_DOC} -- hermetic gate stands")
    assert_within_cap(ROOT_DOC, LIVE_GLOBAL_DOC)


def test_tracked_stand_in_matches_the_live_global() -> None:
    """Guard the substitution: the hermetic gate is only honest while the two agree."""
    if not LIVE_GLOBAL_DOC.is_file():
        pytest.skip(f"no off-repo Codex global doc at {LIVE_GLOBAL_DOC} -- nothing to compare")
    assert TRACKED_GLOBAL_DOC.read_bytes() == LIVE_GLOBAL_DOC.read_bytes(), (
        f"the tracked stand-in {TRACKED_GLOBAL_DOC} has diverged from the live global "
        f"{LIVE_GLOBAL_DOC} ({TRACKED_GLOBAL_DOC.stat().st_size:,} B vs "
        f"{LIVE_GLOBAL_DOC.stat().st_size:,} B). The hermetic gate is now measuring a file "
        "Codex does not read -- reconcile them, or the gate looks armed and is not."
    )


def test_root_doc_is_not_a_wholesale_claude_md_copy() -> None:
    """`AGENTS.md` is not byte-identical to `CLAUDE.md` -- the trap `[#577]` names.

    Scope, stated exactly: this asserts **byte-inequality only**. It does NOT assert that
    `CLAUDE.md` exceeds the cap, and it would not catch a near-copy. Asserting `CLAUDE.md`
    against the cap was considered and rejected: `CLAUDE.md` is deliberately NOT part of the
    Codex payload, so pinning its size here would RED on a legitimate `CLAUDE.md` edit and
    guard nothing Codex reads. The oversize figure below is **measured at run time**, not a
    remembered constant, so the diagnostic cannot go stale even though the assertion is
    narrow.
    """
    claude_md = _REPO_ROOT / "CLAUDE.md"
    assert claude_md.is_file(), f"missing {claude_md}"
    claude_size = claude_md.stat().st_size
    over = claude_size - CAP_BYTES
    verdict = f"{over:,} B OVER" if over > 0 else f"{-over:,} B under"
    assert ROOT_DOC.read_bytes() != claude_md.read_bytes(), (
        f"AGENTS.md is a byte-for-byte copy of CLAUDE.md, measured right now at "
        f"{claude_size:,} B -- {verdict} the {CAP_BYTES:,} B cap. Codex truncates SILENTLY."
    )


# ------------------------------------------------------------------ planted oversize (RED)


def _plant(tmp_path: Path, root_size: int, global_size: int) -> tuple[Path, Path]:
    """Write a synthetic root/global doc pair of exact byte sizes. No real file is touched."""
    root = tmp_path / "AGENTS.md"
    glob = tmp_path / "codex-AGENTS.md"
    root.write_bytes(b"r" * root_size)
    glob.write_bytes(b"g" * global_size)
    return root, glob


def test_planted_oversize_pair_is_refused() -> None:
    """cap+1 must FAIL -- proof the gate can fire, not merely that it is green today.

    Uses `tempfile` rather than the `tmp_path` fixture on purpose: the anchor-gate probe
    test has been RED on `main` since 2026-08-22 on a `tmp_path` fixture, and the one test
    that is the whole point of this module should not share that failure surface.
    """
    with tempfile.TemporaryDirectory() as td:
        root, glob = _plant(Path(td), CAP_BYTES // 2, CAP_BYTES - CAP_BYTES // 2 + 1)
        assert payload_bytes(root, glob) == CAP_BYTES + 1
        with pytest.raises(AssertionError, match=r"EXCEEDS the\s+project_doc_max_bytes cap"):
            assert_within_cap(root, glob)


def test_planted_pair_at_exactly_the_cap_passes(tmp_path: Path) -> None:
    """The boundary is inclusive -- exactly at the cap is not over it."""
    root, glob = _plant(tmp_path, CAP_BYTES // 2, CAP_BYTES - CAP_BYTES // 2)
    assert assert_within_cap(root, glob) == CAP_BYTES


def test_planted_single_oversize_doc_is_refused(tmp_path: Path) -> None:
    """One oversize doc is refused even when the other is empty -- the cap is on the sum."""
    root, glob = _plant(tmp_path, CAP_BYTES + 1, 0)
    with pytest.raises(AssertionError, match=r"EXCEEDS"):
        assert_within_cap(root, glob)


def test_missing_doc_is_refused_not_counted_as_zero(tmp_path: Path) -> None:
    """A vanished instruction doc must RED, never shrink the payload into a silent pass."""
    with pytest.raises(AssertionError, match=r"instruction doc missing"):
        assert_within_cap(tmp_path / "nope.md")
