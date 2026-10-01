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
    assert "R1" in row.value and "R3" in row.value and "3 ruling(s)" in row.value
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
    assert "1 ruling(s)" in anchored.value


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


def test_state_rows_returns_all_seven_keys_in_declared_order(tmp_path):
    repo = _repo_with_registries(tmp_path)
    t = _transport(tmp_path)
    rows = hs.state_rows(repo, t)
    assert tuple(r.key for r in rows) == hs.STATE_ROW_KEYS == (
        "CI", "Batches", "Seats", "Substrates", "Transport", "Rulings", "Capabilities")


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
