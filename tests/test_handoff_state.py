"""Tests for scripts/handoff_state.py — the handoff boot's live state rows
(LANE-5B4-17-handoff-min, Part A Done-when items 1, 2 and 6).

RED-FIRST (Part A Done-contract item 2): every test here failed before `handoff_state.py`,
its `gen_handoff.boot_data_rows` wiring and its `verify_handoff_probes.BOOT_DATA_RULES`
entries existed — there was no module to import and no `BD-ci` / `BD-batches` / ... probe id
to find. The parametrized wrong-value tests below are the load-bearing ones: each FAILS the
one row it tampers and none other, which is the property "rows equal rules both ways" exists
to buy.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import handoff_state as hs
import gen_handoff as gh
import verify_handoff_probes as vhp

from test_gen_handoff import _stub_repo  # noqa: E402 -- shared fixture, precedent: test_test_pairing.py


# --- fixture plumbing: a stub repo carrying the two registries + a transport --------------

def _repo_with_registries(tmp_path: Path) -> Path:
    repo = _stub_repo(tmp_path)
    (repo / "ecosystem" / "substrate-registry.yaml").write_text(
        "substrates:\n  local:\n    live: true\n  cloud:\n    live: false\n", encoding="utf-8")
    (repo / "ecosystem" / "transport-registry.yaml").write_text(
        "kinds:\n  - kind: GO\n  - kind: BATCH\n", encoding="utf-8")
    return repo


def _transport(tmp_path: Path, *, ratification: bool = True, capability_map: bool = True) -> Path:
    t = tmp_path / "transport"
    (t / "to-browser").mkdir(parents=True)
    # A refused Plan row fails BD-plan (W1-9 repair 1), so the shared transport declares a master.
    (t / "to-cc").mkdir(parents=True)
    (t / "to-cc" / "PLAN-FIXTURE-2026-09-20.md").write_text(
        "carried-by: OPEN\nkind: PLAN v1 -- the fixture master\n\n# PLAN\n", encoding="utf-8")
    if ratification:
        (t / "to-browser" / "RATIFICATION-2026-09-25.md").write_text(
            "- **R1** one.\n- **R2** two.\n## R3 — three\n", encoding="utf-8")
        # A superseded sibling must never win "newest".
        (t / "to-browser" / "RATIFICATION-2026-09-25-v1-superseded.md").write_text(
            "- **R1** one only (stale).\n", encoding="utf-8")
    if capability_map:
        (t / "to-browser" / "DIGEST-CAPABILITY-MAP-2026-09-26.md").write_text(
            "## Table (at deadbeef)\n\n"
            "| # | capability | status |\n|---|---|---|\n"
            "| 1 | a | WORKS |\n| 2 | b | MISSING |\n| 3 | c | WORKS (partial) |\n",
            encoding="utf-8")
        # An OLDER dated sibling must lose to the newer one above.
        (t / "to-browser" / "DIGEST-CAPABILITY-MAP-2026-09-20.md").write_text(
            "## Table (at old)\n\n| # | capability | status |\n|---|---|---|\n"
            "| 1 | a | MISSING |\n", encoding="utf-8")
    return t


# --- StateRow itself ---------------------------------------------------------------------

def test_state_row_rejects_an_unknown_freshness_class():
    with pytest.raises(ValueError, match="freshness"):
        hs.StateRow("X", "v", "SOMETIMES", "nowhere")


def test_state_row_rendered_flattens_newlines_and_pipes():
    row = hs.StateRow("X", "a\nb | c", "SLOW", "loc | ator")
    out = row.rendered()
    assert "\n" not in out
    assert "|" not in out


# --- individual row readers: normal + degraded paths --------------------------------------

def test_row_ci_degrades_cleanly_when_repo_has_no_git(tmp_path):
    row = hs.row_ci(tmp_path)
    assert row.key == "CI" and row.freshness == "LIVE-DRIFTS"
    assert "not a git repository" in row.value


# --- [#1330]: row_ci(at_sha=...) anchors to a specific commit, not origin/main ------------

def test_row_ci_defaults_to_origin_main_when_at_sha_is_none(tmp_path, monkeypatch):
    (tmp_path / ".git").mkdir()
    seen = {}

    def _fake_verdict_for(ref, **kwargs):
        seen["ref"] = ref
        return hs._civ.CiVerdict(ref=ref, sha="deadbeef", verdict=hs._civ.STATE_GREEN, run_id=1)
    monkeypatch.setattr(hs._civ, "verdict_for", _fake_verdict_for)
    hs.row_ci(tmp_path)
    assert seen["ref"] == "origin/main"


def test_row_ci_with_at_sha_queries_that_sha_not_origin_main(tmp_path, monkeypatch):
    (tmp_path / ".git").mkdir()
    seen = {}

    def _fake_verdict_for(ref, **kwargs):
        seen["ref"] = ref
        return hs._civ.CiVerdict(ref=ref, sha=ref, verdict=hs._civ.STATE_GREEN, run_id=1)
    monkeypatch.setattr(hs._civ, "verdict_for", _fake_verdict_for)
    row = hs.row_ci(tmp_path, at_sha="c758fe2f847238c7f9bc88797ab13ac106453795")
    assert seen["ref"] == "c758fe2f847238c7f9bc88797ab13ac106453795"
    assert "c758fe2" in row.value  # the resolved sha7 shows up in the VALUE, not evidence
    assert row.evidence == "ci_verdict.verdict_for(ref, timeout_s=0)"  # evidence stays fixed


def test_row_ci_evidence_string_is_identical_regardless_of_at_sha(tmp_path, monkeypatch):
    """[#1330] load-bearing: the generator always calls with `at_sha=None`, so a bundle's
    RECORDED evidence string is this fixed literal. If the verifier's anchored re-derivation
    rendered a DIFFERENT evidence string, `.rendered()` could never match again even when
    the verdict content agrees -- this pins evidence as invariant across at_sha."""
    (tmp_path / ".git").mkdir()
    monkeypatch.setattr(hs._civ, "verdict_for",
                        lambda ref, **kw: hs._civ.CiVerdict(ref=ref, sha=ref, verdict=hs._civ.STATE_GREEN, run_id=1))
    live = hs.row_ci(tmp_path)
    anchored = hs.row_ci(tmp_path, at_sha="c758fe2f847238c7f9bc88797ab13ac106453795")
    assert live.evidence == anchored.evidence


def test_row_batches_reports_none_open_when_no_manifest_declares_one(tmp_path):
    repo = _repo_with_registries(tmp_path)
    row = hs.row_batches(repo)
    assert row.value == "no batch open"


def test_row_batches_names_an_open_batch(tmp_path, monkeypatch):
    repo = _repo_with_registries(tmp_path)

    class _Open:
        batch, path, closed_by = "Z", "docs/audits/x-batch-z-manifest.md", "docs/audits/close.md"
    monkeypatch.setattr(hs._bm, "open_batches", lambda _p: [_Open()])
    row = hs.row_batches(repo)
    assert "Z" in row.value and "docs/audits/x-batch-z-manifest.md" in row.value


def test_row_seats_degrades_to_a_named_default_on_an_empty_registry(tmp_path):
    empty = tmp_path / "seat-registry.jsonl"
    row = hs.row_seats(path=empty)
    assert row.value  # a real registry file with nothing valid in it -> the "no seats" default


def test_row_seats_is_stable_across_a_clock_advance_with_no_seat_change(tmp_path, monkeypatch):
    """LANE-5B4-17 repair 1 (`to-browser/REFUSED-lane-handoff-min.md`): a bundle cut at T and
    re-verified at T+2 min must PASS BD-seats when no seat's state changed -- only the clock
    moved. Before the fix, `row_seats` rendered `seat_registry._label`'s "NN min since last
    event" figure, which ages every minute on its own with no seat-state change, so the same
    wedged seat rendered a DIFFERENT string at cut and at verify and BD-seats failed on timing
    alone, not on a real drift. This is RED against the pre-repair `row_seats` (no
    `elapsed=False`) and GREEN after."""
    path = tmp_path / "seats.jsonl"
    t0 = datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc)
    hs._sr.bind("integrator", "AB", session_id="wedged-1", path=path, now=t0)
    cut_at = t0 + timedelta(minutes=hs._sr.WEDGED_AFTER_MIN + 1)  # already wedged at cut
    verify_at = cut_at + timedelta(minutes=2)                     # no new event in between

    monkeypatch.setattr(hs._sr, "_now", lambda: cut_at)
    cut_row = hs.row_seats(path=path)

    monkeypatch.setattr(hs._sr, "_now", lambda: verify_at)
    verify_row = hs.row_seats(path=path)

    assert "WEDGED" in cut_row.value  # sanity: the fixture actually names a stalled seat
    assert cut_row.rendered() == verify_row.rendered()


# --- [#1124] handoff part B: BD-seats compares identity + liveness, not a whole-string diff --

def _seats_ctx() -> vhp._BootCtx:
    return vhp._BootCtx(Path("nonexistent-bundle"), Path("nonexistent-repo"), {})


def test_bd_seats_fails_on_a_cut_value_that_is_not_a_seat_health_line(tmp_path, monkeypatch):
    """The identity/liveness comparator reads WEDGED/STARVED segments out of the cut value --
    a value carrying NEITHER (a tampered/garbage cell, e.g. `TAMPERED-VALUE`) would otherwise
    silently PASS (no named bad seat to lose, no new one to gain). Shape sanity keeps this row
    falsifiable against a value that is not even `row_seats`' own output."""
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(hs._sr, "REGISTRY_PATH", path)
    status, detail = vhp._rule_bd_seats("TAMPERED-VALUE", _seats_ctx())
    assert status == "fail"
    assert "shape" in detail.lower()


def test_bd_seats_passes_when_an_unrelated_seat_changes_state(tmp_path, monkeypatch):
    """[#1124] RED-FIRST: before this fix, BD-seats (the generic `_rule_state(row_seats)`)
    whole-string-compared the cut value to a live re-derivation, so ANY session's state moving
    between cut and verify failed it -- even a session the cut never named (R26's waiver,
    2026-09-28). Bind one healthy seat at cut, then let an UNRELATED second seat arrive before
    verify (the '[seats] N live' counts line now differs, purely from an unrelated session):
    BD-seats must still PASS, because no seat named at cut lost resolvability and no new
    wedge/starve appeared that the cut did not name."""
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(hs._sr, "REGISTRY_PATH", path)
    t0 = datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc)
    hs._sr.bind("integrator", "AB", session_id="deadbeef-cut", path=path, now=t0)
    monkeypatch.setattr(hs._sr, "_now", lambda: t0)
    cut_row = hs.row_seats()

    t1 = t0 + timedelta(minutes=5)
    hs._sr.bind("integrator", "AB", session_id="cafebabe-new", path=path, now=t1)
    monkeypatch.setattr(hs._sr, "_now", lambda: t1)
    live_row = hs.row_seats()
    assert live_row.rendered() != cut_row.rendered()  # sanity: the whole string DID drift

    status, detail = vhp._rule_bd_seats(cut_row.rendered(), _seats_ctx())
    assert status == "pass", detail


def test_bd_seats_fails_when_a_named_seat_is_no_longer_resolvable(tmp_path, monkeypatch):
    """[#1124]: a seat this bundle NAMED wedged at cut must still be a resolvable identity at
    verify. Simulate a lost identity by pointing the LIVE read at a different (empty)
    registry -- the named seat's session id appears nowhere in it."""
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(hs._sr, "REGISTRY_PATH", path)
    t0 = datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc)
    hs._sr.bind("integrator", "AB", session_id="deadbeef-wedge", path=path, now=t0)
    cut_at = t0 + timedelta(minutes=hs._sr.WEDGED_AFTER_MIN + 1)
    monkeypatch.setattr(hs._sr, "_now", lambda: cut_at)
    cut_row = hs.row_seats()
    assert "WEDGED" in cut_row.value  # sanity: the fixture actually names a stalled seat

    monkeypatch.setattr(hs._sr, "REGISTRY_PATH", tmp_path / "other-seats.jsonl")
    status, detail = vhp._rule_bd_seats(cut_row.rendered(), _seats_ctx())
    assert status == "fail"
    assert "deadbeef" in detail


def test_bd_seats_fails_when_a_new_unnamed_wedge_appears(tmp_path, monkeypatch):
    """[#1124]: no seat may be wedged/starved at verify that the cut did not name. Bind a
    healthy seat at cut (no wedge named), then let it go silent past WEDGED_AFTER_MIN with no
    new event before verify -- a genuinely new problem the cut could not have known about."""
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(hs._sr, "REGISTRY_PATH", path)
    t0 = datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc)
    hs._sr.bind("integrator", "AB", session_id="deadbeef-quiet", path=path, now=t0)
    monkeypatch.setattr(hs._sr, "_now", lambda: t0)
    cut_row = hs.row_seats()
    assert "WEDGED" not in cut_row.value  # sanity: nothing named wedged at cut

    t1 = t0 + timedelta(minutes=hs._sr.WEDGED_AFTER_MIN + 5)   # still no new event
    monkeypatch.setattr(hs._sr, "_now", lambda: t1)
    status, detail = vhp._rule_bd_seats(cut_row.rendered(), _seats_ctx())
    assert status == "fail"
    assert "deadbeef" in detail


def test_bd_seats_passes_a_genuine_empty_registry_cut_against_a_still_empty_live_registry(
    tmp_path, monkeypatch,
):
    """terra HIGH (2026-09-29): `value` here is always `StateRow.rendered()` in production --
    the fact PLUS the ' — evidence: ... [FRESHNESS]' suffix `gen_handoff.py` writes into the
    DATA row and `parse_boot_blocks` reads back verbatim (see the live 2026-09-28 bundle's own
    Seats row). A genuine cut with nothing in the lookback window renders `NO_SEATS_OBSERVED`
    plus that suffix, which never equals the bare literal -- so before the tail was stripped
    back out, a real empty-registry cut always FAILed shape sanity even with the live registry
    still empty too."""
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(hs._sr, "REGISTRY_PATH", path)
    cut_row = hs.row_seats()
    assert cut_row.value == hs.NO_SEATS_OBSERVED  # sanity: the fixture is genuinely empty

    status, detail = vhp._rule_bd_seats(cut_row.rendered(), _seats_ctx())
    assert status == "pass", detail


def test_bd_seats_fails_a_forged_seats_prefixed_value_with_no_real_counts_line(
    tmp_path, monkeypatch,
):
    """terra HIGH (2026-09-29): the prior shape-sanity rung accepted ANY value starting with
    the two words '[seats] ', not the real counts-line structure `seat_health_line()` always
    writes -- so a forged cell like '[seats] forged' read empty cut/live named-bad-seat sets
    and PASSED against a healthy (nothing wedged/starved) live registry: the exact near-no-op
    [#1124]'s shape rung exists to bar, reachable through a value that merely started with the
    right two words rather than one carrying no seats-shape at all."""
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(hs._sr, "REGISTRY_PATH", path)
    status, detail = vhp._rule_bd_seats("[seats] forged", _seats_ctx())
    assert status == "fail"
    assert "shape" in detail.lower()


def test_bd_seats_fails_a_genuine_counts_prefix_with_unrecognized_trailing_text(
    tmp_path, monkeypatch,
):
    """terra HIGH (2026-09-29, second round): `_SEAT_COUNTS_LINE_RE.match()` alone only
    anchors the PREFIX (`re.match` never requires reaching the end of the string) -- a forged
    value that starts with a genuine counts line and ends in arbitrary trailing text (no
    recognized WEDGED:/STARVED:/NO LIVE INTEGRATOR marker at all) satisfied the prefix-only
    check and still read empty named-bad-seat sets, passing against a healthy live registry:
    the SAME near-no-op the counts-line anchor was meant to bar, reached through the
    unvalidated remainder instead of the prefix."""
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(hs._sr, "REGISTRY_PATH", path)
    forged = ("[seats] 0 live / 0 wedged / 0 absent / 0 starved "
              "(last 24 h; 0 unbound) garbage")
    status, detail = vhp._rule_bd_seats(forged, _seats_ctx())
    assert status == "fail"
    assert "shape" in detail.lower()


def test_bd_seats_fails_when_a_named_prefix_is_ambiguous_among_live_sessions(tmp_path, monkeypatch):
    """terra HIGH (`verify_handoff_probes.py:1436`, repair 1, 2026-09-29): `_label` and
    `named_bad_seats` both truncate a session id to its first 8 characters, and the LIVE side
    truncates the same way (`{s.session_id[:8] for s in seats()}`) -- so a bare-prefix
    membership test cannot distinguish the cut-named session from a DIFFERENT live session that
    happens to share the same first 8 characters. Two live sessions sharing one prefix must
    fail as ambiguous, never silently read as 'still resolvable'."""
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(hs._sr, "REGISTRY_PATH", path)
    t0 = datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc)
    hs._sr.bind("integrator", "AB", session_id="deadbeef-1111", path=path, now=t0)
    cut_at = t0 + timedelta(minutes=hs._sr.WEDGED_AFTER_MIN + 1)
    monkeypatch.setattr(hs._sr, "_now", lambda: cut_at)
    cut_row = hs.row_seats()
    assert "WEDGED" in cut_row.value  # sanity: the fixture actually names a stalled seat

    # A second live session arrives sharing the SAME first-8-characters prefix as the named one.
    hs._sr.bind("integrator", "AB", session_id="deadbeef-2222", path=path, now=cut_at)
    status, detail = vhp._rule_bd_seats(cut_row.rendered(), _seats_ctx())
    assert status == "fail"
    assert "ambiguous" in detail.lower() or "more than one live session" in detail.lower()
    assert "deadbeef" in detail


def test_bd_seats_uses_the_tail_stripped_value_not_the_rendered_string_for_named_seats(
    tmp_path, monkeypatch,
):
    """Gemini/agy Medium finding (repair 1, 2026-09-29): `named_bad_seats` parses a
    `seat_health_line`'s own segments, not a rendered `StateRow` string -- passing the raw
    rendered `value` (its ' — evidence: ... [FRESHNESS]' tail included) worked only by
    coincidence, because the LAST named segment's lazy match extends all the way into that
    tail when no later ' / UPPERCASE:' marker follows it. If the evidence text itself happens
    to contain '; ' followed by something shaped like '<label> (<detail>)', the coincidental
    parse reads a PHANTOM extra 'named bad seat' out of the evidence text -- a false FAIL
    against an id nothing in the real registry ever named. Passing the already tail-stripped
    `underlying` (computed by shape sanity a few lines above) is immune."""
    path = tmp_path / "seats.jsonl"
    monkeypatch.setattr(hs._sr, "REGISTRY_PATH", path)
    t0 = datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc)
    hs._sr.bind("integrator", "AB", session_id="deadbeef-real", path=path, now=t0)
    cut_at = t0 + timedelta(minutes=hs._sr.WEDGED_AFTER_MIN + 1)
    monkeypatch.setattr(hs._sr, "_now", lambda: cut_at)
    cut_row = hs.row_seats()
    assert "WEDGED" in cut_row.value  # sanity: the fixture actually names a stalled seat

    # A forged evidence tail whose OWN text contains '; ' followed by a label-shaped fragment
    # -- exactly the shape the coincidental old parse mis-reads as a second named bad seat.
    forged = f"{cut_row.value} — evidence: forged; ghostbeef (0 min) [LIVE]"

    status, detail = vhp._rule_bd_seats(forged, _seats_ctx())
    assert status == "pass", detail
    assert "ghostbeef" not in detail


def test_row_substrates_counts_only_live_true(tmp_path):
    repo = _repo_with_registries(tmp_path)
    row = hs.row_substrates(repo)
    assert row.value == "1/2 live: local"


def test_row_substrates_degrades_when_the_file_is_absent(tmp_path):
    repo = _stub_repo(tmp_path)  # no ecosystem/substrate-registry.yaml
    row = hs.row_substrates(repo)
    assert row.value.startswith("unavailable")


def test_row_transport_counts_registered_kinds(tmp_path):
    repo = _repo_with_registries(tmp_path)
    row = hs.row_transport(repo)
    assert row.value == "2 kind(s) registered"


def test_row_rulings_picks_the_newest_non_superseded_file(tmp_path):
    t = _transport(tmp_path)
    row = hs.row_rulings(t)
    assert "R1" in row.value and "R3" in row.value and "3 ruling id(s) in force" in row.value
    assert "RATIFICATION-2026-09-25.md" in row.value
    assert "superseded" not in row.value


def test_row_rulings_degrades_when_transport_is_unresolved():
    row = hs.row_rulings(None)
    assert "no RATIFICATION file" in row.value


# --- [#1330]: as_of reconstructs "newest as of the bundle's own cut date" -----------------

def test_row_rulings_as_of_excludes_a_file_dated_after_it(tmp_path):
    t = tmp_path / "transport"
    (t / "to-browser").mkdir(parents=True)
    (t / "to-browser" / "RATIFICATION-2026-09-20.md").write_text(
        "- **R1** one.\n", encoding="utf-8")
    (t / "to-browser" / "RATIFICATION-2026-09-25.md").write_text(
        "- **R1** one.\n- **R2** two.\n", encoding="utf-8")
    live = hs.row_rulings(t)
    assert "RATIFICATION-2026-09-25.md" in live.value

    anchored = hs.row_rulings(t, as_of="2026-09-20")
    assert "RATIFICATION-2026-09-20.md" in anchored.value
    assert "1 ruling(s)" in anchored.value             # cut before ROWS_V2_ERA: the legacy shape


def test_row_capabilities_picks_the_newest_dated_file_and_counts_works(tmp_path):
    t = _transport(tmp_path)
    row = hs.row_capabilities(t)
    assert row.value == "2/3 WORKS (1 qualified) — `DIGEST-CAPABILITY-MAP-2026-09-26.md`"


def test_row_capabilities_as_of_excludes_a_file_dated_after_it(tmp_path):
    """The live `_transport` fixture carries an OLDER 2026-09-20 map alongside the newest
    2026-09-26 one — `as_of` anchored to the older date must select the older file, the same
    value a bundle cut on 2026-09-20 would have recorded."""
    t = _transport(tmp_path)
    anchored = hs.row_capabilities(t, as_of="2026-09-20")
    assert "DIGEST-CAPABILITY-MAP-2026-09-20.md" in anchored.value


def test_row_capabilities_degrades_when_transport_is_unresolved():
    row = hs.row_capabilities(None)
    assert "no DIGEST-CAPABILITY-MAP file" in row.value


# --- [#1124] item 2: the capability counter reads the STATUS column, not the last one -------

def test_row_capabilities_uses_the_status_column_not_the_last_column(tmp_path):
    """The prior reader used `row[-1]` (the LAST cell), which was 'status' only by coincidence
    in a 3-column fixture. The real digest carries a trailing 'delta vs …' column AFTER
    status -- reproduced here -- and the prior code counted 0 WORKS against it
    (`to-browser/SESSION-handoff-cut-2026-09-28.md`'s HANDOFF_BOOT.md: literally
    '0/20 WORKS' against a map whose own status column names 10 WORKS rows). RED against the
    pre-fix `_capability_table_rows`/`r[-1]` reader; green against the header-mapped one."""
    t = tmp_path / "transport"
    (t / "to-browser").mkdir(parents=True)
    (t / "to-browser" / "DIGEST-CAPABILITY-MAP-2026-09-29.md").write_text(
        "## Table (at deadbeef)\n\n"
        "| # | capability | status | delta vs 09-27 |\n|---|---|---|---|\n"
        "| 1 | a | WORKS | unrelated trailing text, never WORKS |\n"
        "| 2 | b | MISSING | also never WORKS |\n",
        encoding="utf-8")
    row = hs.row_capabilities(t)
    assert row.value == "1/2 WORKS — `DIGEST-CAPABILITY-MAP-2026-09-29.md`"


def test_row_capabilities_handles_a_backslash_escaped_pipe_before_the_status_column(tmp_path):
    """The real 2026-09-28 map's row 1 mechanism cell contains a literal backslash-escaped
    pipe (`O_CREAT\\|O_EXCL`) to keep it out of the table grammar. A naive `line.split("|")`
    still splits there, shifting every LATER column's index for that one row and misreading
    its status cell -- the harder direction (an escape AFTER status merely shifts a column
    nothing here reads)."""
    t = tmp_path / "transport"
    (t / "to-browser").mkdir(parents=True)
    (t / "to-browser" / "DIGEST-CAPABILITY-MAP-2026-09-29.md").write_text(
        "## Table (at deadbeef)\n\n"
        "| # | capability | mechanism | status |\n|---|---|---|---|\n"
        "| 1 | a | uses O_CREAT\\|O_EXCL sentinel | WORKS |\n"
        "| 2 | b | plain | MISSING |\n",
        encoding="utf-8")
    row = hs.row_capabilities(t)
    assert row.value == "1/2 WORKS — `DIGEST-CAPABILITY-MAP-2026-09-29.md`"


def test_split_table_row_splits_on_an_even_backslash_run_before_the_delimiter(tmp_path):
    """terra HIGH (2026-09-29): the prior `(?<!\\\\)\\|` regex is a single-char lookbehind, so
    it cannot distinguish a genuinely escaped pipe (ONE backslash) from a cell ending in a
    literal backslash immediately followed by a REAL delimiter pipe (TWO backslashes) -- both
    read as "preceded by a backslash" and neither split, silently swallowing a real delimiter
    and shifting every later column. Splitting is by backslash-RUN PARITY: an EVEN run
    (0, 2, 4, ...) is a real delimiter; an ODD run (the documented single-backslash escaping
    convention, still exercised above) is not."""
    assert hs._split_table_row("| cellA\\\\|statusB |") == ["cellA\\\\", "statusB"]
    # the sanctioned single-backslash convention keeps working identically (odd run: no split)
    assert hs._split_table_row("| cellA\\|statusB |") == ["cellA\\|statusB"]
    # a THREE-backslash run (odd) still doesn't split -- one full escape, one bare backslash
    assert hs._split_table_row("| cellA\\\\\\|statusB |") == ["cellA\\\\\\|statusB"]
    # a FOUR-backslash run (even) splits, same as the two-backslash case
    assert hs._split_table_row("| cellA\\\\\\\\|statusB |") == ["cellA\\\\\\\\", "statusB"]


#: A condensed copy of the REAL DIGEST-CAPABILITY-MAP-2026-09-28.md's 20-row status column,
#: verbatim (`H:\My Drive\CLAUDE PROMPT DIR\to-browser\DIGEST-CAPABILITY-MAP-2026-09-28.md`,
#: read 2026-09-29). Other columns are placeholders -- this module never reads them -- but the
#: STATUS text and its position (second-to-last, before a trailing delta column, exactly as
#: the live digest shapes it) are unchanged, so the count this fixture gives IS the map's own
#: count: 10/20 WORKS on rows 8, 10, 11, 12, 14, 16-20 -- the batch contract's own row list.
_MAP_2026_09_28_STATUSES = (
    "WIRED-UNPROVEN (partial)",
    "EXISTS-UNWIRED",
    "WIRED-UNPROVEN (red, not enforced)",
    "EXISTS-UNWIRED",
    "MISSING",
    "EXISTS-UNWIRED",
    "PROSE-ONLY",
    "WORKS (still red — verdict job's own conclusion; green only by manual known-reds "
    "attribution, now OS-normalized)",
    "EXISTS-UNWIRED (manual merge); governance-gate sub-part now WORKS",
    "WORKS (local, direct launch); queue observed firing for real but interrupted "
    "(was WIRED-UNPROVEN, never fired)",
    "WORKS grammar / attributes MISSING",
    "WORKS / trailers MISSING",
    "WIRED-UNPROVEN (unchanged)",
    "WORKS agreement / currency MISSING",
    "EXISTS-UNWIRED (partial)",
    "WORKS (Codespace, strengthened); Anthropic cloud EXISTS-UNWIRED",
    "WORKS (narrow); strays alarm unwired",
    "WORKS token (subagent-inclusive); quota WORKS via close trigger; daily hook WIRED-UNPROVEN",
    "WORKS; gen_ledger EXISTS-UNWIRED",
    "WORKS (bundle probes); seat resume WIRED-UNPROVEN (strengthened)",
)


def test_row_capabilities_matches_the_2026_09_28_maps_own_count(tmp_path):
    t = tmp_path / "transport"
    (t / "to-browser").mkdir(parents=True)
    rows = "\n".join(
        f"| {i} | cap{i} | mechanism | trigger | last fired | tests | {status} | delta |"
        for i, status in enumerate(_MAP_2026_09_28_STATUSES, start=1))
    (t / "to-browser" / "DIGEST-CAPABILITY-MAP-2026-09-28.md").write_text(
        "## Table (at db79ec4e)\n\n"
        "| # | capability | mechanism | trigger | last fired | fails when violated | status "
        "| delta vs 09-27 |\n|---|---|---|---|---|---|---|---|\n" + rows + "\n",
        encoding="utf-8")
    row = hs.row_capabilities(t)
    assert row.value == ("10/20 WORKS (10 qualified) — "
                          "`DIGEST-CAPABILITY-MAP-2026-09-28.md`")


def test_state_rows_returns_all_keys_in_declared_order(tmp_path):
    repo = _repo_with_registries(tmp_path)
    t = _transport(tmp_path)
    rows = hs.state_rows(repo, t)
    assert tuple(r.key for r in rows) == hs.STATE_ROW_KEYS == (
        "CI", "Batches", "Plan", "Seats", "Substrates", "Transport", "Rulings", "Capabilities",
        "Landed", "Decisions", "Dates", "Models")


# --- the four rows foundation-3-handoff-boot adds (onboarding items 6, 7, 12) -------------------
# RED-first: none of these readers existed on 2e7fa5f2 (`AttributeError: module 'handoff_state'
# has no attribute 'row_landed'` ...), so every test below failed before the rows were built.

def test_row_landed_reads_the_register_bullets_not_the_transport(tmp_path):
    repo = _repo_with_registries(tmp_path)
    (repo / "protocols").mkdir(exist_ok=True)
    (repo / "protocols" / "STANDING_RULINGS.md").write_text(
        "- **R3** three\n- **R12 — twelve** x\n- **R2** two\n- **R3** again\nprose R99 is not a bullet\n",
        encoding="utf-8")
    row = hs.row_landed(repo)
    assert row.key == "Landed" and row.freshness == "SLOW"
    assert "through R12" in row.value and "3 ruling id(s)" in row.value, row.value
    assert "protocols/STANDING_RULINGS.md" in row.evidence


def test_row_landed_degrades_visibly_when_the_register_is_absent(tmp_path):
    row = hs.row_landed(tmp_path)
    assert row.value.startswith("unavailable"), row.value


def test_row_decisions_counts_the_transport_decision_files_by_carriage(tmp_path, monkeypatch):
    repo = _repo_with_registries(tmp_path)
    t = tmp_path / "transport"
    (t / "to-cc").mkdir(parents=True)
    (t / "to-browser").mkdir(parents=True)
    (t / "to-cc" / "BATCH-A.md").write_text("carried-by: OPEN\n\n# a\n", encoding="utf-8")
    (t / "to-cc" / "AMEND-B.md").write_text("carried-by: protocols/X.md\n\n# b\n", encoding="utf-8")
    (t / "to-browser" / "DECLARE-C.md").write_text("# no key here\n", encoding="utf-8")
    (t / "to-browser" / "STATUS-D.md").write_text("carried-by: OPEN\n", encoding="utf-8")  # not a decision file
    monkeypatch.setattr(gh, "_resolves_on_main", lambda repo_root, token: token == "protocols/X.md")
    row = hs.row_decisions(t, repo)
    assert row.key == "Decisions" and row.freshness == "LIVE-DRIFTS"
    assert "3 decision file(s)" in row.value, row.value
    assert "1 OPEN" in row.value and "1 resolve on main" in row.value
    assert "1 without a carried-by key" in row.value, row.value
    assert "gen_handoff.carriage_verdicts" in row.evidence


def test_row_decisions_with_no_transport_says_so(tmp_path):
    row = hs.row_decisions(None, _repo_with_registries(tmp_path))
    assert "no transport" in row.value


def test_row_dates_groups_the_harness_fates_and_counts_the_overdue(tmp_path):
    repo = _repo_with_registries(tmp_path)
    (repo / "ecosystem" / "harness.yaml").write_text(
        "a:\n  manual_until: 2026-10-04\nb:\n  manual_until: 2026-10-04\nc:\n  manual_until: 2026-10-19\n"
        "d:\n  manual_until: 2026-10-05\ne:\n  manual_until: 2026-09-01\nf:\n  manual_until:\n",
        encoding="utf-8")
    row = hs.row_dates(repo, today="2026-10-03")
    assert row.key == "Dates" and row.freshness == "LIVE-DRIFTS"
    assert "2026-10-04 ×2" in row.value and "2026-10-05 ×1" in row.value and "2026-10-19 ×1" in row.value
    assert "1 overdue" in row.value, row.value
    assert row.value.index("2026-10-04") < row.value.index("2026-10-05") < row.value.index("2026-10-19")
    assert "manual_until" in row.evidence
    # moving "today" past a date moves that date to overdue -- the row is a function of the date
    later = hs.row_dates(repo, today="2026-10-06")
    assert "2026-10-04 ×2" not in later.value and "4 overdue" in later.value, later.value


def test_row_dates_degrades_visibly_without_a_harness(tmp_path):
    assert hs.row_dates(tmp_path, today="2026-10-03").value.startswith("unavailable")


_REGISTRY_FIXTURE = """\
roles:
  implement:
    order:
      - {provider: anthropic, model: claude-sonnet-5}
      - {provider: copilot-enterprise}
  review:
    order:
      - {provider: openai, model: gpt-5.6-terra}
      - {provider: anthropic, model: claude-sonnet-5}
dispatcher: {provider: anthropic, model: claude-sonnet-5}
"""


def test_row_models_states_routing_order_and_says_it_is_not_live_availability(tmp_path):
    repo = _repo_with_registries(tmp_path)
    (repo / "ecosystem" / "provider-registry.yaml").write_text(_REGISTRY_FIXTURE, encoding="utf-8")
    row = hs.row_models(repo)
    assert row.key == "Models" and row.freshness == "SLOW"
    assert "not live availability" in row.value, row.value
    assert "implement claude-sonnet-5 → copilot-enterprise" in row.value, row.value
    assert "review gpt-5.6-terra → claude-sonnet-5" in row.value
    assert "dispatcher claude-sonnet-5" in row.value
    assert "provider-registry.yaml" in row.evidence


def test_row_models_degrades_visibly_without_a_registry(tmp_path):
    assert hs.row_models(tmp_path).value.startswith("unavailable")


# --- Done-when 6: the coverage line ---------------------------------------------------------

def test_coverage_line_meets_the_part_a_bar(tmp_path):
    repo = _repo_with_registries(tmp_path)
    line = hs.coverage_line(repo, _transport(tmp_path))
    m = re.match(r"COVERAGE: (\d+)/(\d+)", line)
    assert m, line
    covered, total = int(m.group(1)), int(m.group(2))
    assert total == 9
    assert covered >= 6, f"Part A requires >= 6 of 9; got {covered}: {line}"
    assert "1.5/9" in line  # the 2026-09-24 baseline, restated honestly


# --- coupling: the generator's rows and the verifier's rules are the SAME set, both ways ----

def test_state_row_keys_are_a_subset_of_boot_data_rules():
    missing = [k for k in hs.STATE_ROW_KEYS if k not in vhp.BOOT_DATA_RULES]
    assert missing == [], f"a handoff_state row with no BD- rule: {missing}"


# --- Done-when 1 + 2: a real generated bundle carries the rows, and each one is falsifiable -

def _build_bundle(tmp_path, transport, monkeypatch):
    """Build a bundle with `CLAUDE_PROMPTS_DIR` pinned to `transport` for the CALLER's whole
    test, not just this call -- `gen_handoff.transport_root()` re-reads the env var live, and
    `verify_boot()` (via `_rule_state`) calls it AGAIN at check time. A narrower monkeypatch
    (set here, restored before returning) would let verify-time re-derivation fall through to
    whatever the real machine's `CLAUDE_PROMPTS_DIR` happens to be -- a false BD-rulings /
    BD-capabilities FAIL against live Drive content, not a defect in either row's logic."""
    repo = _repo_with_registries(tmp_path)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(transport))
    res = gh.generate(repo, mode="architect", slug="0000-00-00-t", repo=".dev-knowledge",
                      date="2026-07-04", bundle_root=repo / "docs" / "handoffs",
                      assemble=True)
    return repo, res.bundle_dir


def test_generated_bundle_carries_all_seven_state_rows_and_they_pass(tmp_path, monkeypatch):
    t = _transport(tmp_path)
    repo, bundle_dir = _build_bundle(tmp_path, t, monkeypatch)
    boot = (bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    rows, _prose = vhp.parse_boot_blocks(boot)
    keys = {k for k, _v in rows}
    assert set(hs.STATE_ROW_KEYS) <= keys
    results = vhp.verify_boot(bundle_dir, repo)
    for key in hs.STATE_ROW_KEYS:
        rid = f"BD-{vhp.boot_data_id(key)}"
        found = [r for r in results if r.probe_id == rid]
        assert found, f"{rid} did not fire"
        assert found[0].status == "pass", (rid, found[0].detail)


@pytest.mark.parametrize("key", hs.STATE_ROW_KEYS)
def test_a_tampered_state_row_fails_only_its_own_probe(tmp_path, key, monkeypatch):
    t = _transport(tmp_path)
    repo, bundle_dir = _build_bundle(tmp_path, t, monkeypatch)
    boot_path = bundle_dir / "HANDOFF_BOOT.md"
    text = boot_path.read_text(encoding="utf-8")
    tampered = re.sub(rf"(\|\s*\*\*{re.escape(key)}\*\*\s*\|).*", r"\1 TAMPERED-VALUE |",
                      text, count=1)
    assert tampered != text, f"the {key} row was not found to tamper"
    boot_path.write_text(tampered, encoding="utf-8")
    results = vhp.verify_boot(bundle_dir, repo)
    rid = f"BD-{vhp.boot_data_id(key)}"
    mine = next(r for r in results if r.probe_id == rid)
    assert mine.status == "fail", f"{rid} should fail on a tampered value: {mine.detail}"
    others = [r for r in results if r.probe_id != rid and r.probe_id.startswith("BD-")
             and r.probe_id not in (f"BD-{vhp.boot_data_id(k)}" for k in hs.STATE_ROW_KEYS
                                    if k != key)
             # BD-manifest is a WHOLE-BUNDLE integrity check, not a per-row state check --
             # tampering ANY bundle file (including this one) legitimately fails it too; that
             # is BD-manifest's entire job (Done-when 2), not a leak from this row's tamper.
             and r.probe_id != "BD-manifest"]
    # every OTHER original (non-state) row is untouched by this single-row tamper
    assert all(r.status != "fail" for r in others), \
        [(r.probe_id, r.detail) for r in others if r.status == "fail"]


# --- Done-when 2: BD-manifest FAILs on one byte changed anywhere in the bundle -------------

def test_bd_manifest_passes_on_a_fresh_bundle_then_fails_on_one_byte_change(tmp_path, monkeypatch):
    t = _transport(tmp_path)
    repo, bundle_dir = _build_bundle(tmp_path, t, monkeypatch)
    results = vhp.verify_boot(bundle_dir, repo)
    manifest_result = next(r for r in results if r.probe_id == "BD-manifest")
    assert manifest_result.status == "pass", manifest_result.detail

    residual = bundle_dir / "RESIDUAL.md"
    text = residual.read_text(encoding="utf-8")
    residual.write_text(text + "x", encoding="utf-8")  # one byte, appended

    results2 = vhp.verify_boot(bundle_dir, repo)
    manifest_result2 = next(r for r in results2 if r.probe_id == "BD-manifest")
    assert manifest_result2.status == "fail", "a one-byte change anywhere must fail BD-manifest"


def test_bd_manifest_fails_on_a_file_added_after_the_cut(tmp_path, monkeypatch):
    # Codex review, lane-handoff-min: a per-listed-file hash check alone never notices a file
    # ADDED after the cut (every listed hash is still intact) -- BD-manifest must cross-check
    # the bundle's actual file set against the manifest's listed set too.
    t = _transport(tmp_path)
    repo, bundle_dir = _build_bundle(tmp_path, t, monkeypatch)
    (bundle_dir / "UNLISTED.md").write_text("not in the manifest\n", encoding="utf-8")
    results = vhp.verify_boot(bundle_dir, repo)
    manifest_result = next(r for r in results if r.probe_id == "BD-manifest")
    assert manifest_result.status == "fail", manifest_result.detail
    assert "UNLISTED.md" in manifest_result.detail


# --- Done-when 3: publish_bundle / verify_published -----------------------------------------

def test_publish_bundle_then_verify_published_is_clean_on_a_faithful_copy(tmp_path, monkeypatch):
    t = _transport(tmp_path)
    repo, bundle_dir = _build_bundle(tmp_path, t, monkeypatch)
    dest = tmp_path / "scratch-transport"
    published = gh.publish_bundle(bundle_dir, dest)
    assert published["files"], "publish_bundle published nothing"
    for rel in published["files"]:
        assert (dest / rel).is_file()
    assert gh.verify_published(bundle_dir, dest) == []


def test_verify_published_flags_a_tampered_copy_only(tmp_path, monkeypatch):
    t = _transport(tmp_path)
    repo, bundle_dir = _build_bundle(tmp_path, t, monkeypatch)
    dest = tmp_path / "scratch-transport"
    published = gh.publish_bundle(bundle_dir, dest)
    victim = next(rel for rel in published["files"] if rel.endswith("RESIDUAL.md"))
    (dest / victim).write_text("tampered\n", encoding="utf-8")
    mismatches = gh.verify_published(bundle_dir, dest)
    assert mismatches == [victim]


def test_verify_published_fails_closed_when_the_receipt_has_no_manifest(tmp_path):
    # Codex review, lane-handoff-min: an EMPTY/absent manifest must not read as "nothing to
    # mismatch" -- that is indistinguishable from a genuinely clean publish to a caller.
    bundle_dir = tmp_path / "bundle"
    bundle_dir.mkdir()
    (bundle_dir / vhp.RECEIPT_FILE).write_text(json.dumps({}), encoding="utf-8")
    with pytest.raises(ValueError, match="no manifest"):
        gh.verify_published(bundle_dir, tmp_path / "dest")


def test_publish_bundle_refuses_a_manifest_key_that_escapes_the_bundle(tmp_path, monkeypatch):
    # Codex review, lane-handoff-min CRITICAL: a manifest key travels inside a JSON receipt --
    # a tampered receipt naming `../../evil.txt` must never let publish_bundle write outside
    # bundle_dir/dest_dir.
    t = _transport(tmp_path)
    repo, bundle_dir = _build_bundle(tmp_path, t, monkeypatch)
    receipt_path = bundle_dir / vhp.RECEIPT_FILE
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["manifest"]["files"] = {"../../evil.txt": "0" * 64}
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    with pytest.raises(gh.ManifestPathError, match="evil.txt"):
        gh.publish_bundle(bundle_dir, tmp_path / "scratch-transport")
    assert not (tmp_path.parent / "evil.txt").exists()


def test_verify_published_refuses_a_manifest_key_that_escapes_the_dest(tmp_path, monkeypatch):
    t = _transport(tmp_path)
    repo, bundle_dir = _build_bundle(tmp_path, t, monkeypatch)
    receipt_path = bundle_dir / vhp.RECEIPT_FILE
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["manifest"]["files"] = {"../../evil.txt": "0" * 64}
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    with pytest.raises(gh.ManifestPathError, match="evil.txt"):
        gh.verify_published(bundle_dir, tmp_path / "scratch-transport")


def test_a_bundle_cut_before_a_rows_era_is_not_asked_for_it():
    # A committed bundle is immutable: the four rows added 2026-10-03 cannot be owed by the
    # 2026-10-02 bundle, so its absence of them is not a "the DATA block omits this ruled row" FAIL.
    repo = Path(__file__).resolve().parents[1]
    bundle = repo / "docs" / "handoffs" / "2026-10-02-dev-knowledge-architect"
    assert bundle.is_dir(), bundle
    omitted = [r for r in vhp.verify_boot(bundle, repo) if "omits this ruled row" in r.detail]
    assert not omitted, [r.probe_id for r in omitted]
    assert not vhp.bundle_at_or_after(bundle.name, vhp._ROW_ERA["Landed"])
    assert vhp.bundle_at_or_after("2026-10-03-dev-knowledge-architect", vhp._ROW_ERA["Models"])


def test_a_bundle_cut_in_or_after_a_rows_era_is_failed_for_omitting_it(tmp_path):
    # The other half of the era rule: a 2026-10-03+ bundle whose DATA block lacks the four new
    # rows FAILs by name, so the era gate narrows the demand and does not switch it off.
    repo = Path(__file__).resolve().parents[1]
    old = repo / "docs" / "handoffs" / "2026-10-02-dev-knowledge-architect" / "HANDOFF_BOOT.md"
    bundle = tmp_path / "2026-10-03-dev-knowledge-architect"
    bundle.mkdir()
    (bundle / "HANDOFF_BOOT.md").write_text(old.read_text(encoding="utf-8"), encoding="utf-8")
    omitted = {r.probe_id for r in vhp.verify_boot(bundle, repo) if "omits this ruled row" in r.detail}
    assert omitted == {"BD-landed", "BD-decisions", "BD-dates", "BD-models"}, omitted


# --- B2-W1 lane W1-9 (b2-handoff-hardening) items 1 and 4 -------------------------------------
# RED-first at e67f27ac: `handoff_state.row_plan` did not exist and `row_rulings` printed a range
# plus a count (`R1–R73 (6 ruling(s))`), which hid WHICH six it parsed.

_MASTER_HEAD = ("carried-by: OPEN\nlands-via: B2 waves\ndate: 2026-10-04\nfrom: a seat\n"
                "kind: PLAN v12 — supersedes `-v11-superseded`. **The one place to read.**\n\n"
                "# PLAN-HARNESS-2026-10-04 (v12)\n")
_COMPANION_HEAD = ("carried-by: OPEN\nlands-via: the real handoff\ndate: 2026-10-04\nfrom: a seat\n"
                   "kind: PLAN — this seat's close-out. It complements `to-cc/PLAN-HARNESS-2026-10-04.md` "
                   "v12, which holds the harness plan.\n\n# PLAN-HANDOFF-2026-10-04\n")


def _plan_transport(tmp_path: Path) -> Path:
    """The live transport's shape: a v12 master written FIRST, a companion plan of the SAME date
    written LATER (so a newest-by-date-then-mtime pick lands on the companion), a superseded v11
    and an older master."""
    t = tmp_path / "transport"
    (t / "to-cc").mkdir(parents=True)
    (t / "to-browser").mkdir(parents=True)
    (t / "to-cc" / "PLAN-HARNESS-2026-10-04-v11-superseded.md").write_text(
        _MASTER_HEAD.replace("v12", "v11"), encoding="utf-8")
    (t / "to-cc" / "PLAN-WAVE5-2026-09-23.md").write_text(
        "carried-by: OPEN\ndate: 2026-09-23\nstatus: MASTER PLAN — the single source for waves\n\n# PLAN\n",
        encoding="utf-8")
    (t / "to-cc" / "PLAN-HARNESS-2026-10-04.md").write_text(_MASTER_HEAD, encoding="utf-8")
    (t / "to-cc" / "PLAN-HANDOFF-2026-10-04.md").write_text(_COMPANION_HEAD, encoding="utf-8")
    return t


def test_row_plan_names_the_master_not_the_newer_companion_plan(tmp_path):
    t = _plan_transport(tmp_path)
    row = hs.row_plan(t)
    assert row.key == "Plan" and row.freshness == "SLOW"
    assert "`to-cc/PLAN-HARNESS-2026-10-04.md`" in row.value, row.value
    assert "PLAN-HANDOFF" not in row.value and "superseded" not in row.value, row.value
    assert "evidence: to-cc/PLAN-*.md" in row.rendered(), row.rendered()


def test_row_plan_as_of_names_the_master_that_existed_at_the_cut(tmp_path):
    t = _plan_transport(tmp_path)
    assert "PLAN-WAVE5-2026-09-23.md" in hs.row_plan(t, as_of="2026-09-30").value


def test_row_plan_degrades_visibly_without_a_transport_or_a_master(tmp_path):
    assert "no master plan" in hs.row_plan(None).value
    (tmp_path / "t" / "to-cc").mkdir(parents=True)
    (tmp_path / "t" / "to-cc" / "PLAN-HANDOFF-2026-10-04.md").write_text(_COMPANION_HEAD, encoding="utf-8")
    assert "no master plan" in hs.row_plan(tmp_path / "t").value


def _rulings_fixture(tmp_path: Path):
    """Two live RATIFICATION files carrying disjoint ids (as the transport does: each file holds
    the rulings of its own window), a superseded and a withdrawn one whose ids are NOT in force, and
    a register that bullets only some of the live ids."""
    repo = _repo_with_registries(tmp_path)
    (repo / "protocols").mkdir(exist_ok=True)
    (repo / "protocols" / "STANDING_RULINGS.md").write_text(
        "- **R1** a\n- **R2** b\n- **R3** c\n- **R7** d\nprose R9 is not a bullet\n", encoding="utf-8")
    t = tmp_path / "transport"
    (t / "to-browser").mkdir(parents=True)
    (t / "to-browser" / "RATIFICATION-2026-09-25.md").write_text(
        "- **R1** one.\n- **R2** two.\n## R3 — three\n", encoding="utf-8")
    (t / "to-browser" / "RATIFICATION-2026-10-03.md").write_text(
        "## R5 — five\n## R6 — six\n- **R7** seven.\n", encoding="utf-8")
    (t / "to-browser" / "RATIFICATION-2026-10-03-v1-superseded.md").write_text(
        "## R4 — only in a superseded file\n", encoding="utf-8")
    (t / "to-browser" / "RATIFICATION-2026-09-28-v6-withdrawn.md").write_text(
        "## R8 — withdrawn\n", encoding="utf-8")
    return repo, t


def test_row_rulings_prints_the_ids_in_force_and_the_exact_not_landed_set(tmp_path):
    repo, t = _rulings_fixture(tmp_path)
    row = hs.row_rulings(t, repo_root=repo)
    # the exact ids, as runs that hide none: R1-R3 (09-25) + R5-R7 (10-03); R4 and R8 are not in force
    assert row.value.startswith("R1–R3, R5–R7 (6 ruling id(s) in force"), row.value
    assert "R4" not in row.value.split("not landed:")[0] and "R8" not in row.value, row.value
    # in force minus Landed (R1, R2, R3, R7 are bulleted) = R5, R6
    assert row.value.endswith("not landed: R5, R6") or "not landed: R5, R6" in row.value, row.value
    assert "`RATIFICATION-2026-10-03.md`" in row.value, row.value      # the newest file is named


def test_row_rulings_not_landed_is_none_when_every_id_is_bulleted(tmp_path):
    repo, t = _rulings_fixture(tmp_path)
    reg = repo / "protocols" / "STANDING_RULINGS.md"
    reg.write_text(reg.read_text(encoding="utf-8") + "- **R5** e\n- **R6** f\n", encoding="utf-8")
    assert "not landed: none" in hs.row_rulings(t, repo_root=repo).value


def test_row_rulings_not_landed_agrees_with_the_landed_row(tmp_path):
    repo, t = _rulings_fixture(tmp_path)
    landed = hs.row_landed(repo)
    assert "through R7 (4 ruling id(s) bulleted)" in landed.value, landed.value
    assert "not landed: R5, R6" in hs.row_rulings(t, repo_root=repo).value


def test_row_rulings_without_a_register_says_it_could_not_compute_not_landed(tmp_path):
    repo, t = _rulings_fixture(tmp_path)
    assert "not landed: not computed" in hs.row_rulings(t).value


def test_the_plan_row_is_owed_only_by_a_bundle_cut_on_or_after_its_era(tmp_path):
    """B2-W1 W1-9 item 1: `Plan` has a BOOT_DATA rule (rows == rules, both ways) and an era, so the
    committed 2026-10-02 bundle is not asked for it while a 2026-10-04+ bundle without it FAILs."""
    assert "Plan" in vhp.BOOT_DATA_RULES and "Plan" in hs.STATE_ROW_KEYS
    assert vhp._ROW_ERA["Plan"] == hs.ROWS_V2_ERA == "2026-10-04"
    repo = Path(__file__).resolve().parents[1]
    old = repo / "docs" / "handoffs" / "2026-10-02-dev-knowledge-architect" / "HANDOFF_BOOT.md"
    new = tmp_path / "2026-10-04-dev-knowledge-architect"
    new.mkdir()
    (new / "HANDOFF_BOOT.md").write_text(old.read_text(encoding="utf-8"), encoding="utf-8")
    omitted = {r.probe_id for r in vhp.verify_boot(new, repo) if "omits this ruled row" in r.detail}
    assert "BD-plan" in omitted, omitted
    assert not [r for r in vhp.verify_boot(old.parent, repo) if r.probe_id == "BD-plan"]


def test_bd_plan_passes_on_the_master_and_fails_when_the_companion_is_named(tmp_path, monkeypatch):
    t = _plan_transport(tmp_path)
    repo, bundle_dir = _build_bundle(tmp_path, t, monkeypatch)
    boot = (bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    assert "`to-cc/PLAN-HARNESS-2026-10-04.md`" in boot
    assert [r.status for r in vhp.verify_boot(bundle_dir, repo) if r.probe_id == "BD-plan"] == ["pass"]
    (bundle_dir / "HANDOFF_BOOT.md").write_text(
        boot.replace("PLAN-HARNESS-2026-10-04.md", "PLAN-HANDOFF-2026-10-04.md"), encoding="utf-8")
    assert [r.status for r in vhp.verify_boot(bundle_dir, repo) if r.probe_id == "BD-plan"] == ["fail"]


def test_row_rulings_keeps_the_legacy_shape_for_a_bundle_cut_before_the_era(tmp_path):
    """A committed bundle is immutable: one cut before 2026-10-04 recorded `R1–Rn (k ruling(s))`
    and must still re-derive to that string (else BD-rulings turns WARN on every old bundle)."""
    repo, t = _rulings_fixture(tmp_path)
    old = hs.row_rulings(t, as_of="2026-10-02", repo_root=repo)
    assert old.value == "R1–R3 (3 ruling(s)) — `RATIFICATION-2026-09-25.md`", old.value


# --- B2-W1 lane W1-9 repair 1: the Plan row never falls back silently to an older master --------
# RED-first at 88c77d6f: on 2026-10-04 17:19Z the live master was rewritten to a bare `kind: PLAN`
# head (v13 shape, the version moved into `summary:`), the companion has the same bare head, and
# `row_plan` -- which matched only `kind: PLAN v<n>` / `status: MASTER PLAN` -- passed over both and
# named `PLAN-WAVE5-2026-09-23.md`, eleven days old, with `evidence:` making it look checked.

_V13_HEAD = ("carried-by: OPEN\nkind: PLAN\ndate: 2026-10-04\n"
             "supersedes: PLAN-HARNESS-2026-10-04-v12-superseded.md\n"
             "summary: The harness plan, v13 and handoff-ready.\nlands-via: B2-W1\n\n"
             "# PLAN-HARNESS (v13) — start here\n")
_BARE_COMPANION_HEAD = ("carried-by: OPEN\nkind: PLAN\ndate: 2026-10-04\n"
                        "supersedes: PLAN-HANDOFF-2026-10-04-v1-superseded.md\n"
                        "summary: This seat's close-out and handoff.\n\n# PLAN-HANDOFF (v2)\n")
_V12_SUPERSEDED = _MASTER_HEAD
_V1_SUPERSEDED = _COMPANION_HEAD
_WAVE5 = ("carried-by: OPEN\ndate: 2026-09-23\n"
          "status: MASTER PLAN — the single source for waves\n\n# PLAN\n")


def _v13_transport(tmp_path: Path, *, with_lineage: bool = True) -> Path:
    """Today's three shapes: a superseded versioned master, a newer bare-`kind: PLAN` master beside a
    bare-`kind: PLAN` companion (written LAST, so newest by mtime), and an older MASTER PLAN file.
    `with_lineage=False` drops the two superseded predecessors the bare heads' `supersedes:` lines
    point at -- the head then declares nothing a reader can resolve."""
    t = tmp_path / "transport"
    (t / "to-cc").mkdir(parents=True)
    (t / "to-browser").mkdir(parents=True)
    (t / "to-cc" / "PLAN-WAVE5-2026-09-23.md").write_text(_WAVE5, encoding="utf-8")
    if with_lineage:
        (t / "to-cc" / "PLAN-HARNESS-2026-10-04-v12-superseded.md").write_text(
            _V12_SUPERSEDED, encoding="utf-8")
        (t / "to-cc" / "PLAN-HANDOFF-2026-10-04-v1-superseded.md").write_text(
            _V1_SUPERSEDED, encoding="utf-8")
    (t / "to-cc" / "PLAN-HARNESS-2026-10-04.md").write_text(_V13_HEAD, encoding="utf-8")
    (t / "to-cc" / "PLAN-HANDOFF-2026-10-04.md").write_text(_BARE_COMPANION_HEAD, encoding="utf-8")
    return t


def test_row_plan_names_the_v13_master_by_its_supersedes_lineage_not_an_older_master(tmp_path):
    row = hs.row_plan(_v13_transport(tmp_path))
    assert "`to-cc/PLAN-HARNESS-2026-10-04.md`" in row.value, row.value
    assert "WAVE5" not in row.value and "PLAN-HANDOFF" not in row.value, row.value


def test_row_plan_refuses_visibly_when_a_newer_plan_declares_nothing(tmp_path):
    """No resolvable lineage: the two bare-head plans are undeclared and NEWER than the older
    master. The row must name them and refuse -- never hand the seat the older master."""
    row = hs.row_plan(_v13_transport(tmp_path, with_lineage=False))
    assert row.value.startswith("no master plan declared among the newest"), row.value
    assert "PLAN-HARNESS-2026-10-04.md" in row.value and "PLAN-HANDOFF-2026-10-04.md" in row.value
    assert "WAVE5" not in row.value.split("(")[0], row.value


def test_row_plan_an_older_undeclared_plan_does_not_block_a_newer_declared_master(tmp_path):
    t = _v13_transport(tmp_path)
    (t / "to-cc" / "PLAN-OLD-2026-09-16.md").write_text("# PLAN — no head at all\n", encoding="utf-8")
    assert "`to-cc/PLAN-HARNESS-2026-10-04.md`" in hs.row_plan(t).value


def test_bd_plan_fails_on_a_refused_plan_row_even_though_cut_and_live_agree(tmp_path, monkeypatch):
    t = _v13_transport(tmp_path, with_lineage=False)
    repo, bundle_dir = _build_bundle(tmp_path, t, monkeypatch)
    boot = (bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    assert "no master plan declared among the newest" in boot
    res = [r for r in vhp.verify_boot(bundle_dir, repo) if r.probe_id == "BD-plan"]
    assert [r.status for r in res] == ["fail"], res


# Review of the repair (gpt-5.6-terra): `supersedes:` is a basename in the plan's own directory, and
# an `as_of` cutoff binds the lineage too.

def test_a_supersedes_line_cannot_leave_the_to_cc_directory(tmp_path):
    t = _v13_transport(tmp_path, with_lineage=False)
    (t / "to-browser" / "OUTSIDE-2026-10-04.md").write_text(_V12_SUPERSEDED, encoding="utf-8")
    abs_target = (t / "to-browser" / "OUTSIDE-2026-10-04.md").as_posix()
    for ref in ("../to-browser/OUTSIDE-2026-10-04.md", abs_target):
        (t / "to-cc" / "PLAN-HARNESS-2026-10-04.md").write_text(
            _V13_HEAD.replace("PLAN-HARNESS-2026-10-04-v12-superseded.md", ref), encoding="utf-8")
        row = hs.row_plan(t)
        assert row.value.startswith("no master plan declared among the newest"), (ref, row.value)


def test_as_of_binds_the_supersedes_lineage_not_only_the_candidates(tmp_path):
    """A bundle cut on 2026-10-03 must not call a bare plan a master because of a predecessor that
    only existed from 2026-10-04."""
    t = _v13_transport(tmp_path)
    (t / "to-cc" / "PLAN-HARNESS-2026-10-03.md").write_text(
        _V13_HEAD.replace("date: 2026-10-04", "date: 2026-10-03")
        .replace("PLAN-HARNESS-2026-10-04-v12-superseded.md", "PLAN-HARNESS-2026-10-04-v12-superseded.md"),
        encoding="utf-8")
    row = hs.row_plan(t, as_of="2026-10-03")
    assert row.value.startswith("no master plan declared among the newest"), row.value
    assert "PLAN-HARNESS-2026-10-03.md" in row.value, row.value


def test_a_committed_bundle_still_fails_bd_plan_on_a_refused_row(tmp_path):
    ctx = vhp._BootCtx(tmp_path, tmp_path, {}, "0" * 40, "2026-10-04")
    refused = ("no master plan declared among the newest: PLAN-A-2026-10-04.md (add `status: MASTER "
               "PLAN` to the head of the master) — evidence: to-cc/PLAN-*.md (x) [SLOW]")
    status, detail = vhp.BOOT_DATA_RULES["Plan"](refused, ctx)
    assert status == "fail", (status, detail)


def test_as_of_rejects_an_undated_lineage_predecessor(tmp_path):
    """Candidates with no date token stay eligible (the existing reader's rule); a LINEAGE target
    with none cannot be placed before the cut, so under an `as_of` it vouches for nothing."""
    t = _v13_transport(tmp_path)
    (t / "to-cc" / "PLAN-LINEAGE-ROOT-v1-superseded.md").write_text(_V12_SUPERSEDED, encoding="utf-8")
    (t / "to-cc" / "PLAN-HARNESS-2026-10-03.md").write_text(
        _V13_HEAD.replace("date: 2026-10-04", "date: 2026-10-03")
        .replace("PLAN-HARNESS-2026-10-04-v12-superseded.md", "PLAN-LINEAGE-ROOT-v1-superseded.md"), encoding="utf-8")
    row = hs.row_plan(t, as_of="2026-10-03")
    assert row.value.startswith("no master plan declared among the newest"), row.value


def test_a_symlinked_supersedes_target_cannot_escape_the_plan_directory(tmp_path):
    t = _v13_transport(tmp_path, with_lineage=False)
    (t / "to-cc" / "PLAN-HANDOFF-2026-10-04.md").unlink()   # the bare companion would refuse on its own
    outside = t / "to-browser" / "PLAN-OUTSIDE-2026-10-04.md"
    outside.write_text(_V12_SUPERSEDED, encoding="utf-8")
    link = t / "to-cc" / "PLAN-HARNESS-2026-10-04-v12-superseded.md"
    try:
        os.symlink(outside, link)      # a lineage name that resolves outside `to-cc`
    except OSError:
        pytest.skip("this account cannot create symlinks")
    row = hs.row_plan(t)
    assert row.value.startswith("no master plan declared among the newest"), row.value


def test_an_undated_newer_undeclared_plan_refuses_and_an_undated_older_one_does_not(tmp_path):
    """`_live_transport_docs` ranks an undated filename (date "") before every dated one; the Plan
    row ranks it by its file's own mtime date instead, so a newer undeclared `PLAN-NEW.md` cannot
    hide behind an older dated master (review P1) and an old undated plan cannot block a new one."""
    t = tmp_path / "transport"
    (t / "to-cc").mkdir(parents=True)
    master = t / "to-cc" / "PLAN-MASTER-2026-10-04.md"
    master.write_text(_WAVE5.replace("2026-09-23", "2026-10-04"), encoding="utf-8")
    old = t / "to-cc" / "PLAN-OLD.md"
    old.write_text("# PLAN — no head\n", encoding="utf-8")
    new = t / "to-cc" / "PLAN-NEW.md"
    new.write_text("kind: PLAN\n\n# PLAN — newer, declares nothing\n", encoding="utf-8")
    day = 24 * 3600
    base = datetime(2026, 10, 4, 12, 0).timestamp()
    os.utime(old, (base - 30 * day, base - 30 * day))
    os.utime(new, (base - 40 * day, base - 40 * day))
    os.utime(master, (base, base))
    assert "`to-cc/PLAN-MASTER-2026-10-04.md`" in hs.row_plan(t).value       # old undated: no block
    os.utime(new, (base + 3600 * 30, base + 3600 * 30))
    row = hs.row_plan(t)
    assert row.value.startswith("no master plan declared among the newest"), row.value
    assert "PLAN-NEW.md" in row.value, row.value
