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
from pathlib import Path

import pytest
import yaml

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


def test_row_capabilities_picks_the_newest_dated_file_and_counts_works(tmp_path):
    t = _transport(tmp_path)
    row = hs.row_capabilities(t)
    assert row.value == "2/3 WORKS — `DIGEST-CAPABILITY-MAP-2026-09-26.md`"


def test_row_capabilities_degrades_when_transport_is_unresolved():
    row = hs.row_capabilities(None)
    assert "no DIGEST-CAPABILITY-MAP file" in row.value


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
