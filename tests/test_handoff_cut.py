"""ADR-132 (D1-D5, C2, C3): the handoff cut regenerates and byte-checks what it ships.

RED-first tests for `gen_handoff.run_cut` (the `--cut` verb), the preflight roster as data, the
`ledger_refreshed` regenerate-and-diff redesign, the C2 definition of `landed_vs_ratified`, the
receipt's `stops:` / `waits:` / `surfaces:` fields, C3 `time_to_boot`, the separate land verb and
the declared process row. `run_cut` takes a `generate_fn` seam so a unit test does not pay for the
ship gate; the real path has its witness in the lane SESSION file.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

import gen_handoff as gh
import transport as tr

_REPO = Path(__file__).resolve().parents[1]
_TODAY = "2026-10-28"
_D4_STEPS = {1, 5, 12, 13}


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@pytest.fixture()
def world(tmp_path, monkeypatch):
    transport = tmp_path / "transport"
    (transport / "to-browser").mkdir(parents=True)
    (transport / "to-cc").mkdir()
    repo = tmp_path / "repo"
    (repo / "ecosystem").mkdir(parents=True)
    state = {"ledger": f"# LEDGER\n<!-- refreshed {_TODAY} -->\nopen rows: 3\n", "map": "# MAP\nstate: DECLARED\n"}
    monkeypatch.setattr(gh, "_fresh_ledger_text", lambda root, name, date: state["ledger"])
    monkeypatch.setattr(gh, "dispatch_map_text", lambda root=None, **kw: state["map"])
    (transport / "to-cc" / "AMEND-seat-2026-10-28.md").write_text(
        "by: Tech-Architect-47 (2026-10-22-dev-knowledge-architect)\n\n# a\n", encoding="utf-8")
    return {"transport": transport, "repo": repo, "state": state, "tmp": tmp_path}


def _fake_generate(calls=None):
    def fake(repo_root, **kw):
        bundle = Path(kw["bundle_root"]) / kw["slug"]
        bundle.mkdir(parents=True, exist_ok=True)
        (bundle / "HANDOFF_BOOT.md").write_text("# boot\n", encoding="utf-8")
        receipt = {"schema": "handoff-receipt/1", "slug": kw["slug"], "manifest": {"files": {}}}
        extra = kw.get("receipt_extra") or {}
        receipt.update(extra)
        (bundle / "HANDOFF_RECEIPT.json").write_text(json.dumps(receipt), encoding="utf-8")
        if calls is not None:
            calls.append(kw)
        return gh.GenResult(bundle_dir=bundle, journal_draft="JOURNAL DRAFT BODY\n", filled=False)
    return fake


def _cut(world, **kw):
    kw.setdefault("generate_fn", _fake_generate())
    kw.setdefault("now", "2026-10-28T10:00:00Z")
    return gh.run_cut(world["repo"], transport=world["transport"], bundle_root=world["tmp"] / "bundles",
                      slug="cut-a", repo=".dev-knowledge", date=_TODAY, **kw)


def _receipt(res) -> dict:
    return json.loads((res.bundle_dir / "HANDOFF_RECEIPT.json").read_text(encoding="utf-8"))


# --- D2: regenerate, then byte-check ---------------------------------------------------------

def test_the_cut_regenerates_every_surface_and_records_a_sha256_per_surface(world):
    res = _cut(world)
    surfaces = _receipt(res)["surfaces"]
    assert set(surfaces) == {"ledger", "seat_ids", "dispatch_map", "reading_path"}
    ledger = world["transport"] / "to-browser" / "LEDGER-dev-knowledge.md"
    assert ledger.read_text(encoding="utf-8") == world["state"]["ledger"]
    assert surfaces["ledger"]["sha256"] == _sha(world["state"]["ledger"])
    assert (world["transport"] / "to-browser" / "MAP-DISPATCH.md").read_text(encoding="utf-8") == world["state"]["map"]
    seats = tr.load_seat_ids(world["repo"] / "ecosystem" / "seat-ids.yaml")[0]
    assert [s["seat"] for s in seats] == ["Tech-Architect-47"]
    for name, rec in surfaces.items():
        assert rec["sha256"], name


def test_the_cut_is_idempotent_it_rewrites_nothing_on_a_second_run(world):
    first = _cut(world)
    ledger = world["transport"] / "to-browser" / "LEDGER-dev-knowledge.md"
    before = ledger.stat().st_mtime_ns
    second = _cut(world)
    assert ledger.stat().st_mtime_ns == before
    assert {k: v["sha256"] for k, v in _receipt(first)["surfaces"].items()} == \
           {k: v["sha256"] for k, v in _receipt(second)["surfaces"].items()}
    assert not any(v["changed"] for v in _receipt(second)["surfaces"].values())


def test_a_surface_that_changes_between_regeneration_and_the_seal_refuses_the_cut(world, monkeypatch):
    texts = iter(["# LEDGER one\n", "# LEDGER two\n", "# LEDGER two\n", "# LEDGER two\n"])
    monkeypatch.setattr(gh, "_fresh_ledger_text", lambda root, name, date: next(texts))
    with pytest.raises(gh.CutStaleError) as err:
        _cut(world)
    assert "ledger" in str(err.value)


def test_the_cuts_own_writes_do_not_make_the_ledger_stale(world, monkeypatch):
    """Witness-found (clone cut): the cut writes seat-ids.yaml and the bundle AFTER the ledger is
    regenerated, so the ledger's `working tree:` line flips clean -> DIRTY under it. That line is a
    side effect of the cut, not a content claim: the row and the final byte-check mask it."""
    clean = "# LEDGER\n<!-- refreshed 2026-10-28 -->\n- working tree: clean\nopen rows: 3\n"
    dirty = clean.replace("- working tree: clean", "- working tree: DIRTY - 1 path(s)")
    texts = iter([clean, dirty, dirty, dirty, dirty])
    monkeypatch.setattr(gh, "_fresh_ledger_text", lambda root, name, date: next(texts))
    assert gh._mask_refreshed(clean) == gh._mask_refreshed(dirty)
    _cut(world)


def test_the_cut_never_touches_the_repo_outside_the_declared_surfaces(world):
    _cut(world)
    written = {p.relative_to(world["repo"]).as_posix() for p in world["repo"].rglob("*") if p.is_file()}
    assert written == {"ecosystem/seat-ids.yaml"}


# --- the reading-path file ---------------------------------------------------------------------

def test_the_reading_path_file_lists_registry_ratification_finding_and_names_references(world):
    tb = world["transport"] / "to-browser"
    (tb / "INDEX.md").write_text("# INDEX\n" + "x" * 100, encoding="utf-8")
    (tb / "RATIFICATION-2026-10-27.md").write_text("# old\n", encoding="utf-8")
    (tb / "RATIFICATION-2026-10-28.md").write_text("# new\n", encoding="utf-8")
    (tb / "FINDING-handoff-2026-10-26.md").write_text("# f\n", encoding="utf-8")
    (tb / "PROPOSAL-ADR-HANDOFF-2026-10-27.md").write_text("# p\n", encoding="utf-8")
    (tb / "DELTA-2026-10-27.md").write_text("# d\n", encoding="utf-8")
    text = gh.reading_path_text(world["transport"])
    read_first = text.split("## Reference")[0]
    assert "INDEX.md" in read_first and "RATIFICATION-2026-10-28.md" in read_first
    assert "RATIFICATION-2026-10-27.md" not in text
    assert "FINDING-handoff-2026-10-26.md" in read_first
    reference = text.split("## Reference")[1]
    assert "PROPOSAL-ADR-HANDOFF-2026-10-27.md" in reference and "DELTA-2026-10-27.md" in reference
    assert len(text.encode("utf-8")) <= gh.READING_PATH_BROWSER_BUDGET_BYTES


def test_the_reading_path_file_states_when_the_browser_read_set_is_over_budget(world):
    tb = world["transport"] / "to-browser"
    (tb / "INDEX.md").write_text("x" * (gh.READING_PATH_BROWSER_BUDGET_BYTES + 1), encoding="utf-8")
    text = gh.reading_path_text(world["transport"])
    assert "OVER BUDGET" in text


# --- D4 / D5: stops, waits, surfaces -----------------------------------------------------------

def test_stops_name_only_d4_steps_and_each_carries_its_census_number_and_actor(world):
    res = _cut(world)
    stops = _receipt(res)["stops"]
    assert {s["step"] for s in stops} == _D4_STEPS
    assert {s["step"]: s["actor"] for s in stops} == {1: "operator", 5: "browser", 12: "operator", 13: "operator"}


def test_a_satisfied_ratification_and_supplement_leave_only_the_attestation_steps(world):
    (world["transport"] / "to-browser" / f"RATIFICATION-{_TODAY}.md").write_text("# r\n", encoding="utf-8")
    res = _cut(world)
    assert {s["step"] for s in _receipt(res)["stops"]} >= {12, 13}
    assert 1 not in {s["step"] for s in _receipt(res)["stops"]}


def test_waits_open_at_the_first_cut_and_close_when_the_stop_is_satisfied(world):
    first = _cut(world, now="2026-10-28T10:00:00Z")
    opened = {w["step"]: w for w in _receipt(first)["waits"]}
    assert set(opened) == _D4_STEPS
    assert all(w["start"] == "2026-10-28T10:00:00Z" and w["end"] is None for w in opened.values())
    (world["transport"] / "to-browser" / f"RATIFICATION-{_TODAY}.md").write_text("# r\n", encoding="utf-8")
    second = _cut(world, now="2026-10-28T11:30:00Z")
    waits = {w["step"]: w for w in _receipt(second)["waits"]}
    assert waits[1]["start"] == "2026-10-28T10:00:00Z" and waits[1]["end"] == "2026-10-28T11:30:00Z"
    assert waits[12]["end"] is None


def test_the_manifest_is_restamped_after_the_extra_files_are_written(world):
    res = _cut(world)
    manifest = _receipt(res)["manifest"]["files"]
    assert manifest == gh._bundle_file_shas(res.bundle_dir)
    assert "CUT_DRAFTS.md" in manifest and "READING_PATH.md" in manifest


def test_the_drafts_file_carries_the_journal_entry_and_an_operator_decisions_heading(world):
    (world["transport"] / "to-browser" / f"RATIFICATION-{_TODAY}.md").write_text(
        "# r\n\n## R200 - a ruling\n", encoding="utf-8")
    res = _cut(world)
    text = (res.bundle_dir / "CUT_DRAFTS.md").read_text(encoding="utf-8")
    assert "JOURNAL DRAFT BODY" in text
    assert gh._OPERATOR_DECISIONS_RE.search(text)
    assert "R200" in text


# --- C3: time to boot from files ---------------------------------------------------------------

def test_time_to_boot_runs_from_the_merge_commit_to_the_first_file_naming_the_successor(world):
    import os
    tb = world["transport"] / "to-cc"
    early = tb / "AMEND-before.md"
    early.write_text("by: Tech-Architect-47 (x)\n", encoding="utf-8")
    first = tb / "PLAN-first-2026-10-29.md"
    first.write_text("by: Tech-Architect-48 (2026-10-29-dev-knowledge-architect)\n", encoding="utf-8")
    later = tb / "PLAN-later-2026-10-30.md"
    later.write_text("by: Tech-Architect-48 (2026-10-29-dev-knowledge-architect)\n", encoding="utf-8")
    base = 1_793_000_000
    for path, off in ((early, 0), (first, 7200), (later, 9999)):
        os.utime(path, (base + off, base + off))
    rec = gh.time_to_boot(world["transport"], "Tech-Architect-48", merge_epoch=base + 600)
    assert rec["status"] == "measured"
    assert rec["seconds"] == 7200 - 600
    assert rec["file"].endswith("PLAN-first-2026-10-29.md")


def test_time_to_boot_is_unmeasured_with_its_reason_when_no_file_names_the_successor(world):
    rec = gh.time_to_boot(world["transport"], "Tech-Architect-99", merge_epoch=1_793_000_000)
    assert rec["status"].startswith("unmeasured")
    assert rec["seconds"] is None


# --- D3: rows as data ---------------------------------------------------------------------------

def test_the_roster_and_the_blocking_split_are_read_from_one_declared_data_file():
    data = yaml.safe_load(gh.PREFLIGHT_ROWS_FILE.read_text(encoding="utf-8"))
    declared = [r["name"] for r in data["rows"]]
    cut = tuple(r["name"] for r in data["rows"] if r["scope"] == "cut")
    assert gh.PREFLIGHT_ROW_NAMES == cut
    assert gh.PREFLIGHT_NON_BLOCKING_ROWS == tuple(r["name"] for r in data["rows"] if not r["blocking"] and r["scope"] == "cut")
    assert gh.SESSION_START_ROWS == tuple(r["name"] for r in data["rows"] if r["scope"] == "session-start")
    assert len(declared) == 19


def test_the_non_blocking_set_is_landed_vs_ratified_and_operator_decisions_only():
    assert set(gh.PREFLIGHT_NON_BLOCKING_ROWS) == {"landed_vs_ratified", "operator_decisions_list"}
    assert "worktree_owners" not in gh.PREFLIGHT_NON_BLOCKING_ROWS


def test_memory_within_cap_leaves_the_cut_and_stays_a_session_start_row():
    assert "memory_within_cap" not in gh.PREFLIGHT_ROW_NAMES
    assert gh.SESSION_START_ROWS == ("memory_within_cap",)
    assert callable(gh._row_memory_within_cap)


# --- ledger_refreshed: regenerate-and-diff -------------------------------------------------------

def _ledger_row(world, text, date=_TODAY, fresh=None):
    path = world["transport"] / "to-browser" / "LEDGER-dev-knowledge.md"
    if text is not None:
        path.write_text(text, encoding="utf-8")
    world["state"]["ledger"] = fresh if fresh is not None else world["state"]["ledger"]
    return gh._row_ledger_refreshed(world["transport"], ".dev-knowledge", date, repo_root=world["repo"])


def test_ledger_refreshed_passes_on_the_regenerated_bytes_whatever_the_day(world):
    ledger = f"# LEDGER\n<!-- refreshed 2026-10-20 -->\nopen rows: 3\n"
    fresh = f"# LEDGER\n<!-- refreshed {_TODAY} -->\nopen rows: 3\n"
    row = _ledger_row(world, ledger, fresh=fresh)
    assert row.status == gh.PREFLIGHT_PASS, row.render()


def test_ledger_refreshed_fails_when_the_content_differs_from_a_fresh_regeneration(world):
    row = _ledger_row(world, f"# LEDGER\n<!-- refreshed {_TODAY} -->\nopen rows: 99\n")
    assert row.status == gh.PREFLIGHT_FAIL
    assert "differs" in row.detail


def test_ledger_refreshed_fails_when_the_ledger_is_absent(world):
    row = gh._row_ledger_refreshed(world["transport"], ".dev-knowledge", _TODAY, repo_root=world["repo"])
    assert row.status == gh.PREFLIGHT_FAIL and "absent" in row.detail


# --- C2: landed_vs_ratified ---------------------------------------------------------------------

def test_landed_vs_ratified_counts_a_ruling_carried_by_an_adr_as_landed(tmp_path):
    transport = tmp_path / "t"
    (transport / "to-browser").mkdir(parents=True)
    (transport / "to-browser" / "RATIFICATION-2026-10-28.md").write_text("# r\n\n## R301 - x\n\n## R302 - y\n", encoding="utf-8")
    repo = tmp_path / "repo"
    (repo / "protocols").mkdir(parents=True)
    (repo / "protocols" / "STANDING_RULINGS.md").write_text("- **R301** landed in the register\n", encoding="utf-8")
    (repo / "docs" / "decisions").mkdir(parents=True)
    (repo / "docs" / "decisions" / "ADR-900-x.md").write_text("# ADR\n\nCarries R302 as D1.\n", encoding="utf-8")
    row = gh._row_landed_vs_ratified(transport, repo)
    assert row.status == gh.PREFLIGHT_PASS, row.render()


# --- removed verbs and the land verb --------------------------------------------------------------

def test_the_hand_verbs_the_cut_replaces_are_gone_from_the_cli():
    help_text = CliRunner().invoke(gh.main, ["--help"]).output
    for gone in ("--boot-turns", "--boot-dispatch", "--restamp-manifest"):
        assert gone not in help_text, gone
    assert "--cut" in help_text and "--land" in help_text
    assert "nine pre-handoff" not in help_text


def test_dispatch_map_write_is_gone_the_cut_owns_the_write():
    out = CliRunner().invoke(gh.main, ["--dispatch-map", "--write"])
    assert out.exit_code != 0


def test_the_land_verb_refuses_a_bundle_branch_that_is_already_merged(tmp_path):
    ran = []
    with pytest.raises(gh.LandRefusedError):
        gh.land_cut(tmp_path, "worktree-cut-x", is_merged=lambda repo, b: True, runner=lambda argv: ran.append(argv) or 0)
    assert ran == []


def test_the_land_verb_runs_land_lane_for_an_unmerged_branch(tmp_path):
    ran = []
    code = gh.land_cut(tmp_path, "worktree-cut-x", is_merged=lambda repo, b: False,
                       runner=lambda argv: ran.append(argv) or 0)
    assert code == 0
    assert any("land_lane.py" in a for a in ran[0])


# --- D1: the declared process ---------------------------------------------------------------------

def test_the_handoff_is_a_declared_process_in_the_harness_registry():
    data = yaml.safe_load((_REPO / "ecosystem" / "harness.yaml").read_text(encoding="utf-8"))
    rows = {r["id"]: r for r in data["process_registry"]}
    row = rows["handoff"]
    assert row["trigger"] == "/handoff"
    assert row["module"] == "scripts/gen_handoff.py"
    assert row["gate"] == "preflight"
    assert row["receipt"] == "HANDOFF_RECEIPT.json"
    assert (_REPO / row["module"]).is_file()
