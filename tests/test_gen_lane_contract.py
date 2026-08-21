"""Tests for `scripts/gen_lane_contract.py` — the [#539] lane-contract generator.

Three obligations from the lane's Done-contract, one class of test each:
  1. the emitted file PARSES — `parse_contract` recovers the contract from the bytes the
     generator wrote, with no problems reported;
  2. every MANDATORY FIELD is present — the dispatch block in its `Dispatch-Lane` form,
     the worktree<->file pairing, the decision budget's three ask-classes, and the
     receipt-gate fields for a cloud lane;
  3. an INVALID EFFORT NAME is REFUSED — at the pure-function layer and at the CLI.

The round-trip tests are the load-bearing ones: they assert emitter and parser agree, so a
future edit to either surface reddens rather than silently drifting. A test that only read
the emitter's own constants back out of its own output would pass on a generator that emits
nothing a dispatch can use.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import gen_lane_contract as glc  # noqa: E402


# --- fixtures ---------------------------------------------------------------------------

def _spec(**over) -> glc.LaneSpec:
    base = dict(slug="lane-a-539-ch8-codification",
                purpose="codify the dispatch system into PLAYBOOK Ch8",
                task_id="539")
    base.update(over)
    return glc.LaneSpec(**base)


@pytest.fixture()
def local_contract() -> str:
    return glc.render_contract(_spec())


@pytest.fixture()
def cloud_contract() -> str:
    return glc.render_contract(_spec(cloud=True))


# --- 1. the emitted file parses -----------------------------------------------------------

def test_an_emitted_local_contract_parses_with_no_problems(local_contract):
    parsed = glc.parse_contract(local_contract, expect_cloud=False)
    assert parsed.problems == (), parsed.problems
    assert parsed.ok


def test_an_emitted_cloud_contract_parses_with_no_problems(cloud_contract):
    parsed = glc.parse_contract(cloud_contract, expect_cloud=True)
    assert parsed.problems == (), parsed.problems


def test_the_parser_recovers_the_slug_branch_and_file_the_emitter_wrote(local_contract):
    parsed = glc.parse_contract(local_contract)
    assert parsed.slug == "lane-a-539-ch8-codification"
    assert parsed.branch == "worktree-lane-a-539-ch8-codification"
    assert parsed.contract_file == "LANE-a-539-ch8-codification.md"
    assert parsed.effort == "high"


def test_rendering_is_deterministic(local_contract):
    assert glc.render_contract(_spec()) == local_contract


def test_the_file_written_to_disk_is_the_file_that_parses(tmp_path):
    runner = CliRunner()
    result = runner.invoke(glc.cli, [
        "emit", "--slug", "lane-b-101-widget", "--purpose", "build the widget",
        "--id", "101", "--out-dir", str(tmp_path)])
    assert result.exit_code == 0, result.output
    written = tmp_path / "LANE-b-101-widget.md"
    assert written.exists()
    assert glc.parse_contract(written.read_text(encoding="utf-8")).problems == ()


def test_check_accepts_an_emitted_contract_and_rejects_a_truncated_one(tmp_path):
    runner = CliRunner()
    good = tmp_path / "LANE-b-101-widget.md"
    good.write_text(glc.render_contract(_spec(slug="lane-b-101-widget", task_id="101")),
                    encoding="utf-8", newline="\n")
    assert runner.invoke(glc.cli, ["check", str(good)]).exit_code == 0

    bad = tmp_path / "LANE-c-102-broken.md"
    bad.write_text("# LANE lane-c-102-broken — no sections at all\n",
                   encoding="utf-8", newline="\n")
    assert runner.invoke(glc.cli, ["check", str(bad)]).exit_code == 1


# --- 2. all mandatory fields present ------------------------------------------------------

@pytest.mark.parametrize("section", glc.MANDATORY_SECTIONS)
def test_every_mandatory_section_is_emitted(local_contract, section):
    assert f"## {section}" in local_contract


def test_the_dispatch_block_carries_the_dispatch_lane_form(local_contract):
    match = glc._DISPATCH_LINE_RE.search(local_contract)
    assert match is not None
    assert match.group("slug") == "lane-a-539-ch8-codification"
    assert match.group("file") == "LANE-a-539-ch8-codification.md"
    assert match.group("effort") == "high"


def test_the_dispatch_constants_and_the_model_default_are_stated(local_contract):
    assert "--permission-mode bypassPermissions" in local_contract
    assert "--bg" in local_contract
    assert "opus" in local_contract


def test_the_worktree_prefix_is_applied_exactly_once():
    # The batch-6 doubled-prefix class: `worktree-worktree-<name>`.
    assert glc.branch_name("lane-a-539-x") == "worktree-lane-a-539-x"
    text = glc.render_contract(_spec())
    assert "worktree-worktree-" not in text


def test_the_pairing_line_is_present_and_self_consistent(local_contract):
    match = glc._PAIRING_RE.search(local_contract)
    assert match is not None
    assert match.group("branch") == glc.branch_name(match.group("slug"))
    assert match.group("file") == glc.contract_filename(match.group("slug"))


def test_the_decision_budget_carries_all_three_ask_classes(local_contract):
    for ask_class in ("(a)", "(b)", "(c)"):
        assert ask_class in local_contract


def test_a_cloud_lane_carries_both_receipt_fields_and_a_local_lane_carries_neither(
        cloud_contract, local_contract):
    for field_name in glc.RECEIPT_FIELDS:
        assert field_name in cloud_contract
        assert field_name not in local_contract
    assert f"## {glc.CLOUD_SECTION}" in cloud_contract
    assert f"## {glc.CLOUD_SECTION}" not in local_contract


def test_a_missing_mandatory_section_is_reported_by_name(local_contract):
    mangled = local_contract.replace("## Decision budget", "## Budget of decisions", 1)
    problems = glc.parse_contract(mangled).problems
    assert any("Decision budget" in p for p in problems), problems


def test_a_cloud_lane_missing_a_receipt_field_is_reported(cloud_contract):
    mangled = cloud_contract.replace(glc.RECEIPT_FIELDS[1], "something-else", 1)
    problems = glc.parse_contract(mangled, expect_cloud=True).problems
    assert any(glc.RECEIPT_FIELDS[1] in p for p in problems), problems


def test_a_doubled_prefix_in_the_pairing_line_is_reported(local_contract):
    mangled = local_contract.replace("branch `worktree-lane-a-539-ch8-codification`",
                                     "branch `worktree-worktree-lane-a-539-ch8-codification`", 1)
    problems = glc.parse_contract(mangled).problems
    assert any("exactly once" in p for p in problems), problems


# --- the four terra findings of 2026-08-21, each with its own regression test ---------------

def test_a_contract_whose_whole_body_is_inside_a_code_fence_is_refused(local_contract):
    """terra finding 1: every heading and ask-class 'present' as example text."""
    quoted = "# LANE lane-a-539-x — quoted\n\n```\n" + local_contract + "\n```\n"
    problems = glc.parse_contract(quoted).problems
    assert problems, "a file whose entire body is an example block is not a contract"
    assert any("missing mandatory section" in p for p in problems), problems


def test_a_fenced_dispatch_line_is_still_found(local_contract):
    # The complement of the test above: the dispatch line legitimately lives in a fence, so
    # de-fencing is applied to the STRUCTURE scan only.
    assert "```" in local_contract
    assert glc.parse_contract(local_contract).slug == "lane-a-539-ch8-codification"


def test_a_self_consistent_contract_on_an_off_grammar_slug_is_refused(local_contract):
    """terra finding 2: `bad_slug` + `LANE-bad_slug.md` + `worktree-bad_slug` all agreed."""
    mangled = (local_contract
               .replace("lane-a-539-ch8-codification", "bad_slug")
               .replace("LANE-a-539-ch8-codification.md", "LANE-bad_slug.md"))
    problems = glc.parse_contract(mangled).problems
    assert any("invalid lane slug" in p for p in problems), problems


def test_a_dispatch_line_with_no_effort_tier_is_refused(local_contract):
    """terra finding 3: `-Effort` is optional in the grammar, so its absence read as OK."""
    mangled = local_contract.replace(" -Effort high", "", 1)
    problems = glc.parse_contract(mangled).problems
    assert any("states no `-Effort" in p for p in problems), problems


@pytest.mark.parametrize("row, needle", [
    ("| gpt | execute | high |", "model 'gpt'"),
    ("| opus | arbitrary | high |", "mode 'arbitrary'"),
    ("| opus | execute | ultra |", "effort 'ultra'"),
    ("| opus | execute | low |", "dispatch line states"),
])
def test_an_edited_routing_row_is_refused(local_contract, row, needle):
    """terra finding 4: the Model/Mode/Effort table was emitted and never read back."""
    mangled = local_contract.replace("| opus | execute | high |", row, 1)
    problems = glc.parse_contract(mangled).problems
    assert any(needle in p for p in problems), (needle, problems)


def test_a_contract_with_no_routing_row_is_refused(local_contract):
    mangled = local_contract.replace("| opus | execute | high |", "", 1)
    problems = glc.parse_contract(mangled).problems
    assert any("routing row" in p for p in problems), problems


def test_the_parser_recovers_the_model_and_mode(local_contract):
    parsed = glc.parse_contract(local_contract)
    assert (parsed.model, parsed.mode) == ("opus", "execute")


def test_strip_fenced_blocks_preserves_line_count():
    text = "a\n```\nb\nc\n```\nd\n"
    assert glc.strip_fenced_blocks(text).count("\n") == text.count("\n")
    assert "b" not in glc.strip_fenced_blocks(text)


# --- 3. invalid effort names are refused ---------------------------------------------------

@pytest.mark.parametrize("bad", ["", "  ", "HIGH", "ultra", "maximum", "xxhigh",
                                 "high-effort", "1", "None", "high,low"])
def test_an_effort_outside_the_enum_is_refused(bad):
    with pytest.raises(glc.LaneContractError) as exc:
        glc.validate_effort(bad)
    assert "outside the enum" in str(exc.value)


@pytest.mark.parametrize("good", glc.EFFORT_ENUM)
def test_every_enum_member_is_accepted(good):
    assert glc.validate_effort(good) == good


def test_surrounding_whitespace_is_stripped_rather_than_refused():
    # Documented deliberately: a padded value is an artifact of how the string reached the
    # validator, not a different tier — the same posture validate_model/validate_slug take.
    assert glc.validate_effort("  medium ") == "medium"


def test_the_enum_is_exactly_the_five_the_lane_contract_names():
    assert glc.EFFORT_ENUM == ("low", "medium", "high", "xhigh", "max")


def test_max_is_accepted_but_warns_that_the_dispatch_surface_refuses_it(caplog):
    # The declared divergence: [#539]'s contract admits `max`; the dispatch surface's own
    # enum is the closed four. The generator surfaces the conflict rather than resolving it.
    assert "max" not in glc.DISPATCH_ROUTED_EFFORT
    with caplog.at_level("WARNING", logger="gen-lane-contract"):
        assert glc.validate_effort("max") == "max"
    assert any("OUTSIDE the dispatch" in r.getMessage() for r in caplog.records), \
        [r.getMessage() for r in caplog.records]


def test_a_routed_effort_does_not_warn(caplog):
    with caplog.at_level("WARNING", logger="gen-lane-contract"):
        glc.validate_effort("high")
    assert caplog.records == []


def test_the_cli_refuses_an_off_enum_effort(tmp_path):
    result = CliRunner().invoke(glc.cli, [
        "emit", "--slug", "lane-b-101-widget", "--purpose", "x", "--effort", "ultra",
        "--out-dir", str(tmp_path)])
    assert result.exit_code != 0
    assert "ultra" in result.output
    assert not list(tmp_path.iterdir()), "a refused emit leaves no file behind"


def test_a_contract_whose_dispatch_line_carries_an_off_enum_effort_is_reported(local_contract):
    mangled = local_contract.replace("-Effort high", "-Effort ultra", 1)
    problems = glc.parse_contract(mangled).problems
    assert any("ultra" in p for p in problems), problems


# --- the other enums, and the slug grammar -------------------------------------------------

@pytest.mark.parametrize("bad", ["gpt", "Opus", "opus-4", ""])
def test_an_off_enum_model_is_refused(bad):
    with pytest.raises(glc.LaneContractError):
        glc.validate_model(bad)


@pytest.mark.parametrize("bad", ["auto-accept", "Execute", ""])
def test_an_off_enum_mode_is_refused(bad):
    with pytest.raises(glc.LaneContractError):
        glc.validate_mode(bad)


@pytest.mark.parametrize("bad", ["lane_a_539_x", "Lane-A-539-x", "lane--a-539-x",
                                 "-lane-a-539-x", "lane-a-539-x-", ""])
def test_a_non_hyphen_only_slug_is_refused(bad):
    with pytest.raises(glc.LaneContractError):
        glc.validate_slug(bad, strict=False)


def test_the_batch_lane_grammar_is_delegated_not_reimplemented():
    # `lane-539-...` omits the lane LETTER, so the repo's own checker refuses it. The point
    # of the assertion is that this generator asks that checker rather than carrying a
    # second copy of the grammar, which could then disagree with `/lane-boot`.
    from validate_branch_naming import validate_lane_worktree_name
    assert validate_lane_worktree_name("lane-539-ch8-codification") is not None
    with pytest.raises(glc.LaneContractError) as exc:
        glc.validate_slug("lane-539-ch8-codification", strict=True)
    assert "batch-lane grammar" in str(exc.value)
    # …and the same name passes under the relaxed, non-batch worktree reading.
    assert glc.validate_slug("lane-539-ch8-codification", strict=False) == \
        "lane-539-ch8-codification"


def test_the_contract_filename_drops_a_leading_lane_token():
    assert glc.contract_filename("lane-a-539-ch8") == "LANE-a-539-ch8.md"
    assert glc.contract_filename("changelog-sync") == "LANE-changelog-sync.md"


def test_emit_refuses_to_overwrite_a_frozen_contract_without_force(tmp_path):
    runner = CliRunner()
    args = ["emit", "--slug", "lane-b-101-widget", "--purpose", "x", "--out-dir", str(tmp_path)]
    assert runner.invoke(glc.cli, args).exit_code == 0
    second = runner.invoke(glc.cli, args)
    assert second.exit_code != 0
    assert "already exists" in second.output
    assert runner.invoke(glc.cli, args + ["--force"]).exit_code == 0


def test_the_enums_command_prints_the_checkable_surface():
    result = CliRunner().invoke(glc.cli, ["enums"])
    assert result.exit_code == 0
    for member in glc.EFFORT_ENUM:
        assert member in result.output
    assert glc.CLOUD_SECTION in result.output
