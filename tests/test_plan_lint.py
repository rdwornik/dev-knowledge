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
from click.testing import CliRunner

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


def _contract_with_model(tmp_path: Path, filename: str, slug: str, model: str,
                         files_body: str = "`scripts/a.py`.") -> Path:
    """A contract carrying the real `| Model | Mode | Effort |` table and `## Dispatch` fence
    (class 6's own grammar) on top of `_contract`'s minimal shape."""
    text = (
        f"# LANE {slug} — a synthetic lane\n\n"
        f"| Model | Mode | Effort |\n|---|---|---|\n| {model} | execute | high |\n\n"
        f"## Dispatch\n\n```\nclaude --bg -n {slug} --model {model} --effort high "
        f"--permission-mode bypassPermissions --worktree {slug} \"...\"\n```\n\n"
        f"slug `{slug}` -> branch `worktree-{slug}` -> contract `{filename}`\n\n"
        f"**Files you own:** {files_body}\n\n"
        f"## Value\n\nsynthetic fixture, not a real lane.\n"
    )
    path = tmp_path / filename
    path.write_text(text, encoding="utf-8")
    return path


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


def test_parse_lane_contract_reads_starts_after_singular_is_merged(tmp_path):
    """The template's own spelling (`templates/lane-contract-template.md`, one dependency):
    `**Starts after `<lane>` is merged.**` -- singular, correct subject-verb agreement for one
    named lane. Before this lane the regex matched only the plural `…are merged**`, so the
    template's own written grammar was invisible to the reader meant to check it
    (`LANE-5B-6-plan-lint-grammar.md`'s Value line names exactly this mismatch)."""
    path = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.",
                     extra_body="**Starts after `lane-a` is merged.**")
    lane = plan_lint.parse_lane_contract(path)
    assert lane.starts_after == ("lane-a",)


def test_parse_lane_contract_reads_starts_after_the_real_corpus_em_dash_plural(tmp_path):
    """The real WAVE5B-N1 corpus's own spelling (`LANE-5B-11-handback-stop-hook.md` and
    siblings): `**Starts after `<lane>` — every lane named here — are merged.**` -- plural,
    with an em-dash appositive between the lane list and `are merged`. Already matched before
    this lane (the non-greedy `body` group swallows the appositive); pinned here so a future
    edit to the regex cannot silently break the spelling the batch actually shipped."""
    path = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.",
                     extra_body=("**Starts after `lane-hooks-port` — every lane named here — "
                                 "are merged.**"))
    lane = plan_lint.parse_lane_contract(path)
    assert lane.starts_after == ("lane-hooks-port",)


def test_parse_lane_contract_reads_serialize_group(tmp_path):
    path = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.",
                     extra_body="serialize-group: harness-yaml")
    lane = plan_lint.parse_lane_contract(path)
    assert lane.serialize_group == "harness-yaml"


def test_parse_lane_contract_serialize_group_is_none_when_absent(tmp_path):
    path = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.")
    lane = plan_lint.parse_lane_contract(path)
    assert lane.serialize_group is None


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


# --- serialize-group: ordering, not just membership --------------------------------------------

def test_serialize_group_orders_two_lanes_sharing_it(tmp_path):
    """The plan's own acceptance text (`LANE-5B-6-plan-lint-grammar.md` Done-contract item 2):
    "it reads `serialize-group:` and orders lanes sharing a group" -- a shared file that would
    otherwise BLOCK downgrades to ORDERED once both declare the same label."""
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/shared.py`.",
                  extra_body="serialize-group: harness-yaml")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/shared.py`.",
                  extra_body="serialize-group: harness-yaml")
    lanes = plan_lint.load_contracts([a, b])
    edges = plan_lint.build_edges(lanes)
    assert plan_lint.is_ordered(edges, "lane-a", "lane-b")
    findings = plan_lint.find_file_collisions(lanes, edges)
    assert len(findings) == 1
    assert findings[0].severity == plan_lint.ORDERED


def test_serialize_group_orders_every_pair_in_a_group_of_three(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`x`.", extra_body="serialize-group: g")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`y`.", extra_body="serialize-group: g")
    c = _contract(tmp_path, "LANE-c.md", "lane-c", "`z`.", extra_body="serialize-group: g")
    lanes = plan_lint.load_contracts([a, b, c])
    edges = plan_lint.build_edges(lanes)
    assert plan_lint.is_ordered(edges, "lane-a", "lane-b")
    assert plan_lint.is_ordered(edges, "lane-a", "lane-c")
    assert plan_lint.is_ordered(edges, "lane-b", "lane-c")


def test_serialize_group_does_not_order_lanes_in_different_groups(tmp_path):
    """Negative control -- membership in DIFFERENT groups is not a shared-resource claim."""
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/shared.py`.",
                  extra_body="serialize-group: harness-yaml")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/shared.py`.",
                  extra_body="serialize-group: settings-json")
    lanes = plan_lint.load_contracts([a, b])
    edges = plan_lint.build_edges(lanes)
    assert not plan_lint.is_ordered(edges, "lane-a", "lane-b")
    findings = plan_lint.find_file_collisions(lanes, edges)
    assert len(findings) == 1
    assert findings[0].severity == plan_lint.BLOCKING


def test_serialize_group_never_overrides_a_declared_edge_the_other_way(tmp_path):
    """Codex terra review, HIGH: a first cut let `serialize-group`'s input-order guess add an
    edge OPPOSITE a real declared `Starts after` dependency, manufacturing a cycle out of a
    legitimate plan and refusing it. Here `lane-b` is passed BEFORE `lane-a` (so the naive
    input-order guess would read `lane-b` before `lane-a`), but `lane-b` itself declares
    `Starts after `lane-a``  -- the declared edge must win: no cycle, and `is_ordered` still
    reads `lane-a` before `lane-b`, never the reverse."""
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`x`.",
                  extra_body=("**Starts after `lane-a` are merged**\n\n"
                              "serialize-group: g"))
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`y`.", extra_body="serialize-group: g")
    lanes = plan_lint.load_contracts([b, a])  # b passed FIRST -- opposite the declared order
    edges = plan_lint.build_edges(lanes)  # must not raise / must not encode a cycle
    cycle = plan_lint.find_cycle(lanes, edges)
    assert cycle is None
    assert plan_lint.is_ordered(edges, "lane-a", "lane-b")
    assert ("lane-b", "lane-a") not in edges


# --- class 5: a new organ with no declared fate or moment (D14) -------------------------------

def test_new_script_no_fate_flagged_for_an_undeclared_new_script(tmp_path):
    """The plan's own acceptance text: "a contract that adds a new script without a declared
    fate or moment is a finding" -- the LANE-W4B-2 instance, `scripts/handback.py`."""
    _harness(tmp_path, "merge", ["organ_one"])
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/handback.py`, its tests.")
    lanes = plan_lint.load_contracts([a])
    findings = plan_lint.find_new_organs_without_fate(lanes, tmp_path)
    assert len(findings) == 1
    f = findings[0]
    assert f.category == "new-script-no-fate"
    assert f.severity == plan_lint.BLOCKING
    assert f.lane_a == "lane-a" and f.lane_b == "lane-a"
    assert "scripts/handback.py" in f.detail


def test_new_script_no_fate_is_silent_when_the_script_already_exists(tmp_path):
    _harness(tmp_path, "merge", ["organ_one"])
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "existing.py").write_text("pass\n", encoding="utf-8")
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/existing.py`, its tests.")
    lanes = plan_lint.load_contracts([a])
    assert plan_lint.find_new_organs_without_fate(lanes, tmp_path) == []


def test_new_script_no_fate_is_silent_when_the_contract_declares_a_fate(tmp_path):
    _harness(tmp_path, "merge", ["organ_one"])
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/new_thing.py`, its tests.",
                  extra_body=("Add one dated `fates:` line for `scripts/new_thing.py` "
                              "(`manual_until: 2026-10-05`)."))
    lanes = plan_lint.load_contracts([a])
    assert plan_lint.find_new_organs_without_fate(lanes, tmp_path) == []


def test_new_script_no_fate_is_silent_when_the_lane_touches_a_moment(tmp_path):
    _harness(tmp_path, "merge", ["organ_one"])
    a = _contract(tmp_path, "LANE-a.md", "lane-a",
                  "`scripts/new_thing.py`, the `merge` moment of `ecosystem/harness.yaml`.")
    lanes = plan_lint.load_contracts([a])
    assert plan_lint.find_new_organs_without_fate(lanes, tmp_path) == []


def test_new_script_no_fate_is_silent_without_a_harness_declaration(tmp_path):
    """No `ecosystem/harness.yaml` at all -- nothing for a fate to be declared IN, the same
    posture `check_organ_truth` itself takes (subject-absent, not a finding)."""
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/new_thing.py`, its tests.")
    lanes = plan_lint.load_contracts([a])
    assert plan_lint.find_new_organs_without_fate(lanes, tmp_path) == []


def test_new_script_no_fate_is_silent_on_a_non_scripts_path(tmp_path):
    _harness(tmp_path, "merge", ["organ_one"])
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`tests/test_new_thing.py`, its fixtures.")
    lanes = plan_lint.load_contracts([a])
    assert plan_lint.find_new_organs_without_fate(lanes, tmp_path) == []


def test_new_script_no_fate_still_fires_on_ordinary_prose_using_fate_or_moment(tmp_path):
    """Codex terra review, HIGH (`docs/audits/2026-09-24-codex-lane-handback-fixes.md`): a
    first cut matched the bare words "fate" and "moment" anywhere in the contract, so ordinary
    prose ("this has no fate yet", "at this moment we are focusing on X") silently suppressed
    the finding for every new script the lane owned. Only the literal `fates:` key or a dated
    shape keyword counts as a declared commitment."""
    _harness(tmp_path, "merge", ["organ_one"])
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/new_thing.py`, its tests.",
                  extra_body=("This organ has no fate yet -- at this moment we are focusing "
                              "on the happy path."))
    lanes = plan_lint.load_contracts([a])
    findings = plan_lint.find_new_organs_without_fate(lanes, tmp_path)
    assert len(findings) == 1
    assert findings[0].category == "new-script-no-fate"


# --- class 6: model alias where an explicit id belongs -----------------------------------------

def test_parse_lane_contract_reads_model_tokens_from_table_and_dispatch_line(tmp_path):
    path = _contract_with_model(tmp_path, "LANE-a.md", "lane-a", "claude-sonnet-5")
    lane = plan_lint.parse_lane_contract(path)
    assert "claude-sonnet-5" in lane.model_tokens


def test_model_alias_flagged_in_model_table_and_dispatch_line(tmp_path):
    """The plan's own acceptance text (`LANE-5B-6-plan-lint-grammar.md` Done-contract item 3):
    "a model alias … in a contract's Model table or Dispatch line is a finding naming the
    explicit id"."""
    path = _contract_with_model(tmp_path, "LANE-a.md", "lane-a", "opus")
    lanes = plan_lint.load_contracts([path])
    findings = plan_lint.find_model_aliases(lanes)
    assert len(findings) == 1
    f = findings[0]
    assert f.category == "model-alias"
    assert f.severity == plan_lint.BLOCKING
    assert f.lane_a == "lane-a" and f.lane_b == "lane-a"
    assert "opus" in f.detail
    assert "claude-opus-5-5" in f.detail


def test_model_alias_covers_opusplan_sonnet_and_haiku(tmp_path):
    for i, (alias, explicit) in enumerate((
            ("opusplan", "claude-opus-5-5"),
            ("sonnet", "claude-sonnet-5"),
            ("haiku", "claude-haiku-4-5-20251001"))):
        path = _contract_with_model(tmp_path, f"LANE-{i}.md", f"lane-{alias}", alias)
        lanes = plan_lint.load_contracts([path])
        findings = plan_lint.find_model_aliases(lanes)
        assert len(findings) == 1, alias
        assert explicit in findings[0].detail, alias


def test_model_alias_is_silent_on_an_explicit_id(tmp_path):
    """Negative control -- an explicit id CONTAINING one of the alias words (`claude-opus-5-5`
    contains `opus`) must not false-positive; only an EXACT alias value counts."""
    path = _contract_with_model(tmp_path, "LANE-a.md", "lane-a", "claude-opus-5-5")
    lanes = plan_lint.load_contracts([path])
    assert plan_lint.find_model_aliases(lanes) == []


def test_model_alias_ignores_a_dash_dash_model_mention_outside_the_dispatch_fence(tmp_path):
    """Codex terra review, HIGH: a first cut scanned `--model` anywhere in the contract, so a
    `Do not` line or a `Read first` bullet that merely MENTIONS the flag (documentation, not a
    real launch command) could trip a BLOCKING finding. Only the `## Dispatch` fence counts."""
    path = _contract_with_model(tmp_path, "LANE-a.md", "lane-a", "claude-sonnet-5")
    extra = path.read_text(encoding="utf-8") + (
        "\n## Do not\n\n- Never launch with `--model opus`; use the pinned id instead.\n")
    path.write_text(extra, encoding="utf-8")
    lanes = plan_lint.load_contracts([path])
    assert plan_lint.find_model_aliases(lanes) == []


def test_model_alias_reported_once_per_lane_when_table_and_dispatch_agree(tmp_path):
    """The Model table and the Dispatch line name the same alias in a real contract (they must
    agree, per the template's own comment) -- one finding, not two."""
    path = _contract_with_model(tmp_path, "LANE-a.md", "lane-a", "sonnet")
    lanes = plan_lint.load_contracts([path])
    assert len(plan_lint.find_model_aliases(lanes)) == 1


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


def test_find_cycle_detects_a_circular_starts_after(tmp_path):
    """Codex terra review (`[#961]` diff, HIGH): a cyclic `Starts after` made `is_ordered`
    read the two lanes as ordered, silently downgrading a real collision to ORDERED."""
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`x`.",
                  extra_body="**Starts after `lane-b` are merged**")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`y`.",
                  extra_body="**Starts after `lane-a` are merged**")
    lanes = plan_lint.load_contracts([a, b])
    edges = plan_lint.build_edges(lanes)
    cycle = plan_lint.find_cycle(lanes, edges)
    assert cycle is not None
    assert set(cycle) == {"lane-a", "lane-b"}


def test_lint_refuses_a_cyclic_dependency_instead_of_reading_it_as_ordered(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`tests/shared.py`.",
                  extra_body="**Starts after `lane-b` are merged**")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`tests/shared.py`.",
                  extra_body="**Starts after `lane-a` are merged**")
    lanes = plan_lint.load_contracts([a, b])
    with pytest.raises(plan_lint.PlanLintError):
        plan_lint.lint(lanes, tmp_path)


def test_estimate_wave_also_refuses_a_cyclic_dependency(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`x`.",
                  extra_body="**Starts after `lane-b` are merged**")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`y`.",
                  extra_body="**Starts after `lane-a` are merged**")
    lanes = plan_lint.load_contracts([a, b])
    with pytest.raises(plan_lint.PlanLintError):
        plan_lint.estimate_wave(lanes, tmp_path)


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


# --- the real WAVE5B-N1 batch, copied in as fixtures (Done-contract item 1) --------------------

#: Trimmed COPIES of the 13 real `LANE-5B-*.md` contracts this lane's own batch froze
#: (`to-cc/BATCH-WAVE5B-N1-2026-09-24.md` §2), transport root, base `2ae86d07` / `04868005`.
#: HERMETICITY (see the module docstring): the transport lives outside this repository (a
#: Google Drive path), so these are COPIES pasted in rather than a read of the live transport --
#: the same posture `tests/fixtures/README.md`'s sibling fixtures already take. TRIMMED, not
#: paraphrased: every span this module's grammar actually reads is verbatim (the title, the
#: Model table, the `## Dispatch` fence, the `slug` pairing line, `Starts after`/F2 clauses, the
#: `Ruling (a) edit -- not ownership` paragraphs, and `**Files you own:**` in full); the `Read
#: first` bullet lists and the `Done-contract`/`Do not` sections -- prose this module does not
#: parse -- are dropped to keep this file a manageable size.
_REAL_WAVE5B_N1_CONTRACTS: dict[str, str] = {
    "LANE-5B-1-adr122-step0.md": '''\
# LANE lane-adr122-step0 — the backlog view has one budget; truth is unlimited (ADR-122 step 0)

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-adr122-step0 --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-adr122-step0 "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-1-adr122-step0.md"
```

## Worktree pairing

slug `lane-adr122-step0` -> branch `worktree-lane-adr122-step0` -> contract `LANE-5B-1-adr122-step0.md`

**Owns:**

**Files you own:** `scripts/gen_task_tree.py`, the view generator's config, `tests/test_gen_task_tree.py` (its size test), and one new row under `tasks/` (the filed ROWS-OWED row).

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-2-registry-models.md": '''\
# LANE lane-registry-models — orchestrate and plan admit Opus 5.5 by explicit id; cache writes priced at 2x

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-registry-models --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-registry-models "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-2-registry-models.md"
```

## Worktree pairing

slug `lane-registry-models` -> branch `worktree-lane-registry-models` -> contract `LANE-5B-2-registry-models.md`

**Owns:**

**Files you own:** `ecosystem/provider-registry.yaml`, `tests/test_provider_router.py` and the router's other tests.

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-3-launcher-fixes.md": '''\
# LANE lane-launcher-fixes — the launcher names the bind command, launches Copilot detached, and warns on an alias

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-launcher-fixes --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-launcher-fixes "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-3-launcher-fixes.md"
```

## Worktree pairing

slug `lane-launcher-fixes` -> branch `worktree-lane-launcher-fixes` -> contract `LANE-5B-3-launcher-fixes.md`

**Owns:**

**Files you own:** `scripts/dispatch.py`, `tests/test_dispatch.py` and its other tests.

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-4-merge-hygiene.md": '''\
# LANE lane-merge-hygiene — timed merge receipts, a post-merge check, and a batch janitor

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-merge-hygiene --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-merge-hygiene "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-4-merge-hygiene.md"
```

## Worktree pairing

slug `lane-merge-hygiene` -> branch `worktree-lane-merge-hygiene` -> contract `LANE-5B-4-merge-hygiene.md`

**Owns:**

**Files you own:** `scripts/merge_receipt.py`, a new post-merge-check module and a new batch-janitor module under scripts/, and their tests under tests/ — module paths chosen by a cited convention of scripts/ (record which).

**Ruling (a) edit — not ownership:** one additive dated `fates:` line (`manual_until`) per new module in `ecosystem/harness.yaml`, and nothing else in that file; `lane-organ-wirings` owns it, and an additive conflict at merge keeps both entries (ruling (f)).

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-5-hooks-port.md": '''\
# LANE lane-hooks-port — the start hooks run through uv, and start time is measured before and after

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-hooks-port --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-hooks-port "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-5-hooks-port.md"
```

## Worktree pairing

slug `lane-hooks-port` -> branch `worktree-lane-hooks-port` -> contract `LANE-5B-5-hooks-port.md`

**Owns:**

**Files you own:** `scripts/surface_triage.ps1`, `scripts/billing_leak_sentinel.ps1` (ported to Python modules under scripts/), the `lane_end_guard` invocation, the hooks section of `.claude/settings.json`, and their tests.

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-6-plan-lint-grammar.md": '''\
# LANE lane-plan-lint-grammar — one contract grammar: plan lint parses every contract of this batch

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-plan-lint-grammar --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-plan-lint-grammar "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-6-plan-lint-grammar.md"
```

## Worktree pairing

slug `lane-plan-lint-grammar` -> branch `worktree-lane-plan-lint-grammar` -> contract `LANE-5B-6-plan-lint-grammar.md`

**Owns:**

**Files you own:** `scripts/plan_lint.py`, `templates/lane-contract-template.md`, `tests/test_plan_lint.py`.

## Value

the contract that produced this fixture set.
''',
    "LANE-5B-7-ci-commit-gate.md": '''\
# LANE lane-ci-commit-gate — the CI commit-gate judges only the pushed diff

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-ci-commit-gate --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-ci-commit-gate "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-7-ci-commit-gate.md"
```

## Worktree pairing

slug `lane-ci-commit-gate` -> branch `worktree-lane-ci-commit-gate` -> contract `LANE-5B-7-ci-commit-gate.md`

**Owns:**

**Files you own:** `.github/workflows/` and any test that reads the workflow.

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-8-trial-gh-issues.md": '''\
# LANE lane-trial-gh-issues — the live GitHub Issues trial ADR-122 never ran, symmetric to the YAML trial

| Model | Mode | Effort |
|---|---|---|
| claude-opus-5-5 | execute | high |

## Dispatch

```
claude --bg -n lane-trial-gh-issues --model claude-opus-5-5 --effort high --permission-mode bypassPermissions --worktree lane-trial-gh-issues "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-8-trial-gh-issues.md"
```

## Worktree pairing

slug `lane-trial-gh-issues` -> branch `worktree-lane-trial-gh-issues` -> contract `LANE-5B-8-trial-gh-issues.md`

**Owns:**

**Files you own:** one record under `docs/audits/` (dated, class-named per `validate_hermetization`), the ADR-122 amendment section in `docs/decisions/`; off-repo: one scratch repository on the hub's own account `rdwornik`, created by `gh` for this trial; its local clone and one worktree of it, both under `$env:TEMP\\lane-trial-gh-issues\\` (outside the hub tree; removed and the removal verified at close-out), plus the item-4 branch and PR on the scratch repository.

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-9-transport-registry.md": '''\
# LANE lane-transport-registry — the transport as data, first cut: registered kinds, registered writers

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-transport-registry --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-transport-registry "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-9-transport-registry.md"
```

## Worktree pairing

slug `lane-transport-registry` -> branch `worktree-lane-transport-registry` -> contract `LANE-5B-9-transport-registry.md`

**Owns:**

**Files you own:** `ecosystem/transport-registry.yaml`, `scripts/transport.py` (new), `scripts/handback.py` (the writer switch only), and their tests.

**Ruling (a) edit — not ownership:** one additive dated `fates:` line (`manual_until`) for `scripts/transport.py` in `ecosystem/harness.yaml`, and nothing else in that file; `lane-organ-wirings` owns it, and an additive conflict at merge keeps both entries (ruling (f)).

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-10-census-instrument.md": '''\
# LANE lane-census-instrument — a trustworthy census of what runs

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-census-instrument --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-census-instrument "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-10-census-instrument.md"
```

## Worktree pairing

slug `lane-census-instrument` -> branch `worktree-lane-census-instrument` -> contract `LANE-5B-10-census-instrument.md`

**Owns:**

**Files you own:** `scripts/organ_usage_metric.py`, `tests/test_organ_usage_metric.py`.

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-11-handback-stop-hook.md": '''\
# LANE lane-handback-stop-hook — a lane session cannot end without a machine HANDBACK line

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-handback-stop-hook --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-handback-stop-hook "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-11-handback-stop-hook.md"
```

**Starts after `lane-hooks-port` — every lane named here — are merged.**

**First step (F2), before any build:** `git fetch origin`; `git merge origin/main`; then for each
dependency `git merge-base --is-ancestor <its merge sha> HEAD`, the sha read from the integrator's
`STATE <lane> MERGED <sha>` line in `to-browser/SESSION-integrator-wave5b-n1-2026-09-24.md`;
record the commands and exit codes in your session file.

## Worktree pairing

slug `lane-handback-stop-hook` -> branch `worktree-lane-handback-stop-hook` -> contract `LANE-5B-11-handback-stop-hook.md`

**Owns:**

**Files you own:** the Stop hook module (`scripts/lane_end_guard.py`, or a new module under scripts/ — record which), the Stop entry of `.claude/settings.json`, and their tests.

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-12-agents-import.md": '''\
# LANE lane-agents-import — CLAUDE.md imports AGENTS.md and the shared block exists once

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-agents-import --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-agents-import "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-12-agents-import.md"
```

**Starts after `lane-hooks-port` — every lane named here — are merged.**

**First step (F2), before any build:** `git fetch origin`; `git merge origin/main`; then for each
dependency `git merge-base --is-ancestor <its merge sha> HEAD`, the sha read from the integrator's
`STATE <lane> MERGED <sha>` line in `to-browser/SESSION-integrator-wave5b-n1-2026-09-24.md`;
record the commands and exit codes in your session file.

## Worktree pairing

slug `lane-agents-import` -> branch `worktree-lane-agents-import` -> contract `LANE-5B-12-agents-import.md`

**Owns:**

**Files you own:** `CLAUDE.md`, `AGENTS.md`, `tests/test_claude_md_byte_cap.py`, `tests/test_agents_md_byte_cap.py` and the parity test.

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
    "LANE-5B-13-organ-wirings.md": '''\
# LANE lane-organ-wirings — the census's WIRE items and the inert invariant — merges LAST

| Model | Mode | Effort |
|---|---|---|
| claude-sonnet-5 | execute | high |

## Dispatch

```
claude --bg -n lane-organ-wirings --model claude-sonnet-5 --effort high --permission-mode bypassPermissions --worktree lane-organ-wirings "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\\LANE-5B-13-organ-wirings.md"
```

**Starts after `lane-launcher-fixes` and `lane-plan-lint-grammar` — every lane named here — are merged.**

**First step (F2), before any build:** `git fetch origin`; `git merge origin/main`; then for each
dependency `git merge-base --is-ancestor <its merge sha> HEAD`, the sha read from the integrator's
`STATE <lane> MERGED <sha>` line in `to-browser/SESSION-integrator-wave5b-n1-2026-09-24.md`;
record the commands and exit codes in your session file.

## Worktree pairing

slug `lane-organ-wirings` -> branch `worktree-lane-organ-wirings` -> contract `LANE-5B-13-organ-wirings.md`

**Owns:**

**Files you own:** `ecosystem/harness.yaml` and its tests; `.pre-commit-config.yaml` (the `block-commit-on-main` stage only).

## Value

synthetic-in-test copy, trimmed for the plan-lint fixture suite.
''',
}


def test_lint_parses_the_real_wave5b_n1_batch_and_finds_the_known_settings_json_collision(tmp_path):
    """Done-contract item 1: "The lint parses every `LANE-5B-*.md` contract of this batch (a
    test over copies of them as fixtures)". Every one of the 13 real contracts parses without a
    `PlanLintError`, and `lint()` reproduces exactly the result the batch's own generation step
    measured (`to-browser/SESSION-gen-wave5b-n1-2026-09-24.md` Part 2, final render): one
    ORDERED file-collision (lane-hooks-port <-> lane-handback-stop-hook, both own
    `.claude/settings.json`, downgraded from BLOCKING because lane 11 declares `Starts after
    `lane-hooks-port` … are merged`), zero BLOCKING."""
    paths = []
    for filename, text in _REAL_WAVE5B_N1_CONTRACTS.items():
        path = tmp_path / filename
        path.write_text(text, encoding="utf-8")
        paths.append(path)
    lanes = plan_lint.load_contracts(paths)  # raises PlanLintError on any parse failure
    assert len(lanes) == 13
    findings = plan_lint.lint(lanes, tmp_path)  # no ecosystem/harness.yaml here -- see fixture note
    assert [f.category for f in findings] == ["file-collision"]
    f = findings[0]
    assert f.severity == plan_lint.ORDERED
    assert {f.lane_a, f.lane_b} == {"lane-hooks-port", "lane-handback-stop-hook"}
    assert ".claude/settings.json" in f.detail
    blocking = [f for f in findings if f.severity == plan_lint.BLOCKING]
    assert blocking == []


def test_lint_over_the_real_batch_finds_no_model_aliases(tmp_path):
    """Every one of the 13 real contracts already names an explicit id (the batch's own night
    rule, §5) -- class 6 fires on none of them. Pinned separately from the combined test above
    so a future alias regression in the fixture set is attributed to the right class."""
    paths = []
    for filename, text in _REAL_WAVE5B_N1_CONTRACTS.items():
        path = tmp_path / filename
        path.write_text(text, encoding="utf-8")
        paths.append(path)
    lanes = plan_lint.load_contracts(paths)
    assert plan_lint.find_model_aliases(lanes) == []


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
                          "serial-mismatch", "new-script-no-fate"}


def test_render_findings_reports_no_findings_over_a_clean_wave(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.")
    lanes = plan_lint.load_contracts([a, b])
    assert plan_lint.render_findings(plan_lint.lint(lanes, tmp_path)) == "plan-lint: no findings"


# --- CLI exit codes --------------------------------------------------------------------------

def test_cmd_report_exits_nonzero_on_a_blocking_finding(tmp_path):
    """Codex terra review (`[#961]` diff, HIGH): `report` calls itself the freeze-time command
    but always exited 0, so an automated gate using it would accept an invalid plan."""
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/shared.py`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/shared.py`.")
    result = CliRunner().invoke(plan_lint.cli, [
        "report", str(a), str(b), "--repo-root", str(tmp_path)])
    assert result.exit_code != 0
    assert "BLOCKING" in result.output


def test_cmd_report_exits_zero_on_a_clean_wave(tmp_path):
    a = _contract(tmp_path, "LANE-a.md", "lane-a", "`scripts/a.py`.")
    b = _contract(tmp_path, "LANE-b.md", "lane-b", "`scripts/b.py`.")
    result = CliRunner().invoke(plan_lint.cli, [
        "report", str(a), str(b), "--repo-root", str(tmp_path)])
    assert result.exit_code == 0
