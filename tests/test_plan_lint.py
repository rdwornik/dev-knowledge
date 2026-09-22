"""RED-first witnesses for `scripts/plan_lint.py` -- FR6, plan lint (`[#961]`).

Written before the module's behaviour was trusted, per ADR-108 section B: this file is the
frozen pass/fail criterion. SYNTHETIC CONTRACTS ONLY (Done-contract item 4) -- the real-data
proof (Done-contract item 3, "it must flag the W4-2/W4-4 conflict of wave 4a") is a one-time,
read-only run over the transport's `LANE-*.md` files, pasted into this lane's handback rather
than wired into the suite: the transport lives outside this repository (a Google Drive path),
so a test that read it would not run on any other machine or in CI, which is exactly the
hermeticity `tests/fixtures/README.md`'s sibling fixtures exist to preserve.

Each finding class gets a positive test (the class fires) and, where the class is easy to get
vacuously right, a negative test (it does not fire on a clean pair) -- the same discipline
`test_impacted_tests.py` applies to its own mapping.
"""
from __future__ import annotations

from pathlib import Path

import pytest

import plan_lint


# --- fixtures ----------------------------------------------------------------------------------

def _contract(tmp_path: Path, filename: str, slug: str, files_body: str,
             extra_body: str = "", title: str = "a synthetic lane") -> Path:
    """The minimal `LANE-*.md` shape plan-lint's grammar reads: a slug pairing line and a
    `**Files you own:**` paragraph. Not a real contract's full shape (no `## Dispatch` fence,
    no `## Done-contract`) -- plan-lint does not read those, and `gen_lane_contract.parse_contract`
    already owns the test that a real contract carries them."""
    text = (
        f"# LANE {slug} — {title}\n\n"
        f"slug `{slug}` -> branch `worktree-{slug}` -> contract `{filename}`\n\n"
        f"**Files you own:** {files_body}\n\n"
        f"{extra_body}\n\n"
        f"## Value\n\nsynthetic fixture, not a real lane.\n"
    )
    path = tmp_path / filename
    path.write_text(text, encoding="utf-8")
    return path


def _harness(repo_root: Path, moment: str, organ_ids: list[str]) -> None:
    ecosystem = repo_root / "ecosystem"
    ecosystem.mkdir(parents=True, exist_ok=True)
    organs = "\n".join(f"      - {{id: {oid}, receipt: R-{oid}.json, command: []}}"
                       for oid in organ_ids)
    (ecosystem / "harness.yaml").write_text(
        f"stages: []\nmoments:\n  - name: {moment}\n    trigger: test\n    organs:\n{organs}\n",
        encoding="utf-8")


# --- parsing -------------------------------------------------------------------------------

def test_parse_lane_contract_reads_slug_owned_paths_and_moment(tmp_path):
    path = _contract(tmp_path, "LANE-a.md", "lane-a",
                     "`scripts/foo.py`, the `merge` moment of `ecosystem/harness.yaml`.")
    lane = plan_lint.parse_lane_contract(path)
    assert lane.slug == "lane-a"
    assert "scripts/foo.py" in lane.owned_paths
    assert "ecosystem/harness.yaml" in lane.owned_paths
    assert lane.moments_touched == ("merge",)


def test_parse_lane_contract_reads_serial_and_starts_after(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.",
                  extra_body="**Serial: you run first; every other lane waits for your merge.**")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.",
                  extra_body="**Starts after `lane-a` are merged**")
    la, lb = plan_lint.parse_lane_contract(a), plan_lint.parse_lane_contract(b)
    assert la.serial is True
    assert lb.starts_after == ("lane-a",)


def test_parse_lane_contract_reads_starts_after_with_a_trailing_period(tmp_path):
    """`LANE-W4B-1-merge-path.md`'s real spelling closes the bold span with `.**`, not `**` --
    a period the first version of this regex did not allow, found while proving this module on
    real transport data."""
    path = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.",
                     extra_body="**Starts after `lane-a` and `lane-c` are merged.** more prose.")
    lane = plan_lint.parse_lane_contract(path)
    assert lane.starts_after == ("lane-a", "lane-c")


def test_parse_lane_contract_reads_wait_for_none_and_produces_consumes(tmp_path):
    path = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.",
                     extra_body=("You depend on no other lane and wait for none.\n\n"
                                 "**Produces:** `widget-schema`\n\n**Consumes:** `other-thing`"))
    lane = plan_lint.parse_lane_contract(path)
    assert lane.wait_for_none is True
    assert lane.produces == ("widget-schema",)
    assert lane.consumes == ("other-thing",)


def test_parse_lane_contract_refuses_a_contract_with_no_slug_pairing_line(tmp_path):
    path = tmp_path / "LANE-broken.md"
    path.write_text("# not a real contract\n\n**Files you own:** nothing.\n", encoding="utf-8")
    with pytest.raises(plan_lint.PlanLintError):
        plan_lint.parse_lane_contract(path)


def test_load_contracts_refuses_a_duplicate_slug(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-dup", "`scripts/a.py`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-dup", "`scripts/b.py`.")
    with pytest.raises(plan_lint.PlanLintError):
        plan_lint.load_contracts([a, b])


# --- class 1: file collision ----------------------------------------------------------------

def test_file_collision_flagged_between_a_synthetic_pair_that_shares_a_file(tmp_path):
    """The plan's own acceptance text: "flags a synthetic pair of contracts that share a file"."""
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/shared.py`, its tests.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/shared.py`, a different test.")
    lanes = plan_lint.load_contracts([a, b])
    findings = plan_lint.find_file_collisions(lanes, plan_lint.build_edges(lanes))
    assert len(findings) == 1
    f = findings[0]
    assert f.category == "file-collision"
    assert f.severity == plan_lint.BLOCKING
    assert {f.lane_a, f.lane_b} == {"lane-a", "lane-b"}


def test_file_collision_detects_a_directory_ancestor_overlap(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "fixtures under `tests/`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`tests/test_foo.py`, its fixtures.")
    lanes = plan_lint.load_contracts([a, b])
    findings = plan_lint.find_file_collisions(lanes, plan_lint.build_edges(lanes))
    assert len(findings) == 1


def test_file_collision_is_silent_on_a_clean_pair(tmp_path):
    """Negative control -- a check that always fires is not a check."""
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`, its tests.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`, its tests.")
    lanes = plan_lint.load_contracts([a, b])
    assert plan_lint.find_file_collisions(lanes, plan_lint.build_edges(lanes)) == []


def test_file_collision_is_ordered_not_blocking_when_a_dependency_orders_the_lanes(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`tests/test_shared.py`, its tests.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`tests/test_shared.py`, more.",
                  extra_body="**Starts after `lane-a` are merged**")
    lanes = plan_lint.load_contracts([a, b])
    findings = plan_lint.find_file_collisions(lanes, plan_lint.build_edges(lanes))
    assert len(findings) == 1
    assert findings[0].severity == plan_lint.ORDERED


# --- class 2: missing producer ----------------------------------------------------------------

def test_missing_producer_flagged_for_a_synthetic_pair(tmp_path):
    """The plan's own acceptance text: "one that consumes an artifact no lane produces"."""
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.",
                  extra_body="**Consumes:** `widget-schema`")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.")
    lanes = plan_lint.load_contracts([a, b])
    findings = plan_lint.find_missing_producers(lanes)
    assert len(findings) == 1
    assert findings[0].category == "missing-producer"
    assert "widget-schema" in findings[0].detail


def test_missing_producer_is_silent_when_a_lane_produces_the_artifact(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.",
                  extra_body="**Consumes:** `widget-schema`")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.",
                  extra_body="**Produces:** `widget-schema`")
    lanes = plan_lint.load_contracts([a, b])
    assert plan_lint.find_missing_producers(lanes) == []


# --- class 3: moment/test coupling (the W4-2/W4-4 class) ------------------------------------

def test_moment_test_conflict_flagged_the_w4_2_w4_4_shape(tmp_path):
    _harness(tmp_path, "merge", ["organ_one", "organ_two", "organ_three"])
    a = _contract(tmp_path, "LANE-a.md", "lane-a",
                  "the `merge` moment of `ecosystem/harness.yaml`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b",
                  "the connection-test module under `tests/`.")
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_connection_module.py").write_text(
        'EXPECTED = ["organ_one", "organ_two"]\n', encoding="utf-8")
    lanes = plan_lint.load_contracts([a, b])
    findings = plan_lint.find_moment_test_conflicts(lanes, tmp_path, plan_lint.build_edges(lanes))
    assert len(findings) == 1
    f = findings[0]
    assert f.category == "moment-test-coupling"
    assert f.severity == plan_lint.BLOCKING
    assert f.lane_a == "lane-a" and f.lane_b == "lane-b"


def test_moment_test_conflict_requires_at_least_two_literal_organ_hits(tmp_path):
    """One incidental mention is not a hard-coded list -- see the module's honest limits."""
    _harness(tmp_path, "merge", ["organ_one", "organ_two"])
    a = _contract(tmp_path, "LANE-a.md", "lane-a",
                  "the `merge` moment of `ecosystem/harness.yaml`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b",
                  "the connection-test module under `tests/`.")
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_connection_module.py").write_text(
        'EXPECTED = ["organ_one"]\n', encoding="utf-8")
    lanes = plan_lint.load_contracts([a, b])
    assert plan_lint.find_moment_test_conflicts(lanes, tmp_path, plan_lint.build_edges(lanes)) == []


def test_moment_test_conflict_is_ordered_not_blocking_when_declared_dependency_orders_them(tmp_path):
    _harness(tmp_path, "merge", ["organ_one", "organ_two"])
    a = _contract(tmp_path, "LANE-a.md", "lane-a",
                  "the `merge` moment of `ecosystem/harness.yaml`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b",
                  "the connection-test module under `tests/`.",
                  extra_body="**Starts after `lane-a` are merged**")
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_connection_module.py").write_text(
        'EXPECTED = ["organ_one", "organ_two"]\n', encoding="utf-8")
    lanes = plan_lint.load_contracts([a, b])
    findings = plan_lint.find_moment_test_conflicts(lanes, tmp_path, plan_lint.build_edges(lanes))
    assert len(findings) == 1
    assert findings[0].severity == plan_lint.ORDERED


def test_moment_test_conflict_is_silent_when_no_lane_touches_the_moment(tmp_path):
    _harness(tmp_path, "merge", ["organ_one", "organ_two"])
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b",
                  "the connection-test module under `tests/`.")
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_connection_module.py").write_text(
        'EXPECTED = ["organ_one", "organ_two"]\n', encoding="utf-8")
    lanes = plan_lint.load_contracts([a, b])
    assert plan_lint.find_moment_test_conflicts(lanes, tmp_path, plan_lint.build_edges(lanes)) == []


# --- class 4: serial mismatch -----------------------------------------------------------------

def test_serial_mismatch_flagged_when_another_lane_declares_it_waits_for_none(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.",
                  extra_body="**Serial: you run first; every other lane waits for your merge.**")
    b = _contract(tmp_path, "LANE-b.md", "lane-b",
                  "`scripts/b.py`. You depend on no other lane and wait for none.")
    lanes = plan_lint.load_contracts([a, b])
    findings = plan_lint.find_serial_mismatches(lanes)
    assert len(findings) == 1
    assert findings[0].category == "serial-mismatch"
    assert findings[0].lane_a == "lane-a" and findings[0].lane_b == "lane-b"


def test_serial_mismatch_flagged_for_a_named_wait_on_a_lane_that_is_not_serial(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.",
                  extra_body="This lane waits for `lane-a`'s merge before starting.")
    lanes = plan_lint.load_contracts([a, b])
    findings = plan_lint.find_serial_mismatches(lanes)
    assert len(findings) == 1
    assert findings[0].lane_a == "lane-b" and findings[0].lane_b == "lane-a"


def test_serial_mismatch_is_silent_on_a_consistent_pair(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.",
                  extra_body="**Serial: you run first; every other lane waits for your merge.**")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.")
    lanes = plan_lint.load_contracts([a, b])
    assert plan_lint.find_serial_mismatches(lanes) == []


# --- the dependency graph -----------------------------------------------------------------------

def test_build_edges_from_serial_and_starts_after(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`x`.",
                  extra_body="**Serial: you run first; every other lane waits for your merge.**")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`y`.",
                  extra_body="**Starts after `lane-c` are merged**")
    c = _contract(tmp_path, "LANE-c.md", "lane-c", "`z`.")
    lanes = plan_lint.load_contracts([a, b, c])
    edges = plan_lint.build_edges(lanes)
    assert ("lane-a", "lane-b") in edges
    assert ("lane-a", "lane-c") in edges
    assert ("lane-c", "lane-b") in edges


def test_is_ordered_is_transitive(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`x`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`y`.",
                  extra_body="**Starts after `lane-a` are merged**")
    c = _contract(tmp_path, "LANE-c.md", "lane-c", "`z`.",
                  extra_body="**Starts after `lane-b` are merged**")
    lanes = plan_lint.load_contracts([a, b, c])
    edges = plan_lint.build_edges(lanes)
    assert plan_lint.is_ordered(edges, "lane-a", "lane-c")
    assert not plan_lint.is_ordered(edges, "lane-a", "lane-a-does-not-exist")


def test_longest_chain_counts_lanes_not_edges(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`x`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`y`.",
                  extra_body="**Starts after `lane-a` are merged**")
    c = _contract(tmp_path, "LANE-c.md", "lane-c", "`z`.",
                  extra_body="**Starts after `lane-b` are merged**")
    d = _contract(tmp_path, "LANE-d.md", "lane-d", "`w`.")  # unordered, off the chain
    lanes = plan_lint.load_contracts([a, b, c, d])
    edges = plan_lint.build_edges(lanes)
    assert plan_lint._longest_chain(lanes, edges) == 3


# --- the real conflict, reproduced synthetically to pin its shape -----------------------------

def test_w4_2_w4_4_conflict_reproduced_from_the_wave_4a_shape(tmp_path):
    """Pins the real finding this lane exists to catch, without reading the transport (see the
    module docstring). Same shape as the real pair: an owner lane touching the `merge` moment,
    a bare-`tests/`-directory owner whose connection-test module hard-codes that moment's fired
    organs, and NO declared dependency between the two (both merely follow a third, serial,
    lane -- which orders each of them against it and NOT against each other)."""
    _harness(tmp_path, "merge",
            ["merge_receipt.open", "merge_receipt.models", "go_reader", "review_packet", "gates"])
    serial = _contract(tmp_path, "LANE-serial.md", "lane-known-reds", "`scripts/test_pairing.py`.",
                       extra_body="**Serial: you run first; four lanes wait for your merge.**")
    owner = _contract(tmp_path, "LANE-owner.md", "lane-merge-gates-truth",
                      "`.claude/commands/lane-integrate.md`, the `merge` moment of "
                      "`ecosystem/harness.yaml`.")
    tester = _contract(tmp_path, "LANE-tester.md", "lane-connection-hygiene",
                       "the connection-test module and its fixtures under `tests/`, "
                       "`scripts/impacted_tests.py`.")
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_connection_loop.py").write_text(
        'EXPECTED_STOPS = (("merge", "gates"),)\n'
        'FIRED = ["merge_receipt.open", "merge_receipt.models", "go_reader", "review_packet"]\n',
        encoding="utf-8")
    lanes = plan_lint.load_contracts([serial, owner, tester])
    findings = plan_lint.lint(lanes, tmp_path)
    conflicts = [f for f in findings if f.category == "moment-test-coupling"]
    assert len(conflicts) == 1
    assert conflicts[0].severity == plan_lint.BLOCKING
    assert {conflicts[0].lane_a, conflicts[0].lane_b} == {
        "lane-merge-gates-truth", "lane-connection-hygiene"}


# --- estimates -----------------------------------------------------------------------------

def test_estimate_wave_computes_the_stated_formula(tmp_path, monkeypatch):
    """The formula in isolation from `merge_receipt`'s own completeness machinery (which has its
    own test suite): stub the two library calls this module reuses read-only, and check only
    that THIS module's arithmetic combines their answers as documented."""
    import merge_receipt as mr_module

    lane_report = mr_module.MedianReport(n=2, median_minutes=15.0, minimum=10.0, maximum=20.0,
                                         quartiles=None, per_merge=(10.0, 20.0), kind=mr_module.KIND_ARC)
    merge_report = mr_module.MedianReport(n=1, median_minutes=30.0, minimum=30.0, maximum=30.0,
                                          quartiles=None, per_merge=(30.0,), kind=mr_module.KIND_MERGE)

    def _fake_median_report(receipts, kind=mr_module.KIND_MERGE):
        return lane_report if kind == mr_module.KIND_ARC else merge_report

    monkeypatch.setattr(plan_lint.mr, "read_ledger", lambda repo_root: [])
    monkeypatch.setattr(plan_lint.mr, "median_report", _fake_median_report)

    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`x`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`y`.",
                  extra_body="**Starts after `lane-a` are merged**")
    lanes = plan_lint.load_contracts([a, b])
    est = plan_lint.estimate_wave(lanes, tmp_path)
    assert est.serial_chain_len == 2
    assert est.lane_count == 2
    assert est.lane_median.n == 2
    assert est.merge_median.n == 1
    assert est.minutes == pytest.approx(2 * 15.0 + 2 * 30.0)


def test_estimate_wave_is_undefined_over_an_empty_ledger(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`x`.")
    lanes = plan_lint.load_contracts([a])
    est = plan_lint.estimate_wave(lanes, tmp_path)
    assert est.minutes is None
    assert "UNDEFINED" in est.render()


# --- the orchestrator ------------------------------------------------------------------------

def test_lint_combines_every_class(tmp_path):
    _harness(tmp_path, "merge", ["organ_one", "organ_two"])
    a = _contract(tmp_path, "LANE-a.md", "lane-a",
                  "`scripts/shared.py`, the `merge` moment of `ecosystem/harness.yaml`.",
                  extra_body="**Serial: you run first; every other lane waits for your merge.**")
    b = _contract(tmp_path, "LANE-b.md", "lane-b",
                  "`scripts/shared.py`, the connection-test module under `tests/`. "
                  "You depend on no other lane and wait for none.",
                  extra_body="**Consumes:** `nothing-anyone-makes`")
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_connection_module.py").write_text(
        'EXPECTED = ["organ_one", "organ_two"]\n', encoding="utf-8")
    lanes = plan_lint.load_contracts([a, b])
    findings = plan_lint.lint(lanes, tmp_path)
    categories = {f.category for f in findings}
    assert categories == {"file-collision", "missing-producer", "moment-test-coupling",
                          "serial-mismatch"}


def test_render_findings_reports_no_findings_over_a_clean_wave(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.")
    lanes = plan_lint.load_contracts([a, b])
    assert plan_lint.render_findings(plan_lint.lint(lanes, tmp_path)) == "plan-lint: no findings"
