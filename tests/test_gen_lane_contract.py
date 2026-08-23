"""Tests for `scripts/gen_lane_contract.py` — the [#539] lane-contract generator.

Four obligations, one class of test each. The first three are [#539]'s Done-contract; the
fourth is M10's, added by lane L7 (2026-08-23):
  1. the emitted file PARSES — `parse_contract` recovers the contract from the bytes the
     generator wrote, with no problems reported;
  2. every MANDATORY FIELD is present — the dispatch block, the worktree<->file pairing,
     the decision budget's three ask-classes, and the receipt-gate fields for a cloud lane;
  3. an INVALID EFFORT NAME is REFUSED — at the pure-function layer and at the CLI;
  4. every generated contract carries a COMMAND LINE, and it is the RIGHT one for the
     contract's declared shape — asserted for all three shapes, not just the local one.

The round-trip tests are the load-bearing ones: they assert emitter and parser agree, so a
future edit to either surface reddens rather than silently drifting. A test that only read
the emitter's own constants back out of its own output would pass on a generator that emits
nothing a dispatch can use.

Obligation 4 needs the same care one level up, and section 4 is written to it: a test that
only asserted a command line is PRESENT would have passed against the generator as it stood
on 2026-08-22, which emitted `Dispatch-Lane` for a cloud lane. Presence is necessary and
not sufficient; the selection is what is under test.
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
    return glc.render_contract(_spec(shape="cloud"))


@pytest.fixture()
def interactive_contract() -> str:
    return glc.render_contract(_spec(shape="interactive"))


# --- 1. the emitted file parses -----------------------------------------------------------

def test_an_emitted_local_contract_parses_with_no_problems(local_contract):
    parsed = glc.parse_contract(local_contract, expect_shape="local")
    assert parsed.problems == (), parsed.problems
    assert parsed.ok


def test_an_emitted_cloud_contract_parses_with_no_problems(cloud_contract):
    parsed = glc.parse_contract(cloud_contract, expect_shape="cloud")
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
    problems = glc.parse_contract(mangled, expect_shape="cloud").problems
    assert any(glc.RECEIPT_FIELDS[1] in p for p in problems), problems


def test_a_doubled_prefix_in_the_pairing_line_is_reported(local_contract):
    # Anchored on the PAIRING LINE (slug -> branch), not on the bare `branch `worktree-…``
    # substring: the dispatch prose also names the branch, so an unanchored replace could
    # mangle the prose instead and the test would pass while checking nothing. That silent
    # miss actually happened while this file was being extended (L7, 2026-08-23).
    target = ("slug `lane-a-539-ch8-codification` -> "
              "branch `worktree-lane-a-539-ch8-codification`")
    assert target in local_contract, "the pairing line moved; re-anchor this test"
    mangled = local_contract.replace(
        target, target.replace("branch `worktree-", "branch `worktree-worktree-"), 1)
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


# --- 4. the command line, and the SHAPE it is selected from (M10 / L7) ----------------------
#
# The class these close, stated once so a later reader knows what they are for. Before this
# lane the generator emitted `Dispatch-Lane` UNCONDITIONALLY: `spec.cloud` added a receipt
# section and changed nothing else, so `emit --cloud` produced a cloud contract carrying the
# LOCAL command. A lane handed the wrong command is worse than a lane handed none, because
# a wrong command looks authoritative — so presence alone is not the property under test.
# Every test below asserts the SELECTION.

def test_every_shape_emits_a_command_line():
    """The closure property: no shape emits a contract with no command."""
    for shape in glc.SHAPE_ENUM:
        text = glc.render_contract(_spec(shape=shape))
        assert glc.find_command_line(text) is not None, \
            f"{shape}: emitted a contract with no dispatch command line"
        assert glc.parse_contract(text, expect_shape=shape).problems == ()


def test_a_generated_contract_without_its_command_line_fails(local_contract):
    """The contract's Done-item 2, as a mutation: delete the command, the check REFUSES.

    Written as a deletion rather than a corruption on purpose — the failure M10 exists to
    close is a session handed over with NO command, so the absence is the case that has to
    redden. Deleting the emitted line is the smallest mutation that reproduces it.
    """
    mangled = local_contract.replace(
        "Dispatch-Lane lane-a-539-ch8-codification LANE-a-539-ch8-codification.md "
        "-Effort high\n", "", 1)
    assert "Dispatch-Lane lane-a-539" not in mangled, "the mutation did not bite"
    problems = glc.parse_contract(mangled).problems
    assert any("no dispatch command line" in p for p in problems), problems


@pytest.mark.parametrize("shape, present, absent", [
    ("local", "Dispatch-Lane ", ("Dispatch-CloudV2", "and execute it exactly")),
    ("cloud", "Dispatch-CloudV2 ", ("Dispatch-Lane ", "and execute it exactly")),
    ("interactive", "and execute it exactly", ("Dispatch-Lane ", "Dispatch-CloudV2")),
])
def test_the_command_shape_is_selected_from_the_declared_shape(shape, present, absent):
    """All three shapes, not just the local one (Done-item 3).

    The `absent` half is the load-bearing one: it is what would have caught the pre-lane
    defect, where a cloud contract carried `Dispatch-Lane`.
    """
    text = glc.render_contract(_spec(shape=shape))
    assert present in text
    for wrong in absent:
        assert wrong not in text, f"{shape} contract carries the {wrong!r} form"


def test_a_cloud_contract_carries_the_cloud_command_and_never_the_local_one(cloud_contract):
    """The exact pre-lane defect, pinned as its own regression."""
    match = glc._CLOUD_DISPATCH_LINE_RE.search(cloud_contract)
    assert match is not None
    assert match.group("file") == "LANE-a-539-ch8-codification.md"
    assert match.group("slug") == "lane-a-539-ch8-codification"
    assert glc._DISPATCH_LINE_RE.search(cloud_contract) is None


def test_an_interactive_contract_carries_the_read_and_execute_first_message(
        interactive_contract):
    match = glc._INTERACTIVE_LINE_RE.search(interactive_contract)
    assert match is not None
    assert match.group("file") == "LANE-a-539-ch8-codification.md"
    # The session is STARTED by `claude`; the line above is its first message, not a shell
    # command. Both halves are emitted, because either alone is unusable.
    assert "\nclaude\n" in interactive_contract
    assert glc.PROMPTS_DIR_TOKEN in interactive_contract


@pytest.mark.parametrize("shape", glc.SHAPE_ENUM)
def test_the_declared_shape_line_is_emitted_and_recovered(shape):
    text = glc.render_contract(_spec(shape=shape))
    assert f"**Shape:** `{shape}`" in text
    assert glc.parse_contract(text).shape == shape


@pytest.mark.parametrize("declared, wrong_command", [
    ("cloud", "Dispatch-Lane lane-a-539-ch8-codification "
              "LANE-a-539-ch8-codification.md -Effort high"),
    ("interactive", "Dispatch-CloudV2 LANE-a-539-ch8-codification.md "
                    "-Title 'lane-a-539-ch8-codification'"),
])
def test_a_command_that_disagrees_with_the_declared_shape_is_refused(declared, wrong_command):
    """A hand-edited contract cannot keep a shape label while carrying another's command."""
    text = glc.render_contract(_spec(shape=declared))
    original = glc.find_command_line(text)
    assert original is not None
    mangled = text.replace(original, wrong_command, 1)
    problems = glc.parse_contract(mangled).problems
    assert any("declared shape" in p for p in problems), problems


def test_an_expect_shape_mismatch_is_reported(local_contract):
    problems = glc.parse_contract(local_contract, expect_shape="cloud").problems
    assert any("cloud" in p for p in problems), problems


@pytest.mark.parametrize("bad", ["", "  ", "Local", "worktree", "remote", "batch"])
def test_an_off_enum_shape_is_refused(bad):
    with pytest.raises(glc.LaneContractError) as exc:
        glc.validate_shape(bad)
    assert "outside the enum" in str(exc.value)


@pytest.mark.parametrize("good", glc.SHAPE_ENUM)
def test_every_shape_enum_member_is_accepted(good):
    assert glc.validate_shape(good) == good


def test_the_shape_enum_is_exactly_the_three_ch8_names():
    assert glc.SHAPE_ENUM == ("local", "cloud", "interactive")
    assert glc.DEFAULT_SHAPE == "local"


def test_the_branch_derivation_follows_the_shape():
    """Ch8 puts a cloud lane on `claude/<slug>`, not on `worktree-<slug>`.

    The pre-lane generator emitted the worktree branch for every shape, so a cloud contract
    declared a branch its own transport would never create.
    """
    assert glc.branch_name("lane-a-539-x", "local") == "worktree-lane-a-539-x"
    assert glc.branch_name("lane-a-539-x", "cloud") == "claude/lane-a-539-x"
    assert glc.branch_name("lane-a-539-x", "interactive") is None
    # The one-argument form is unchanged — the local default, so every existing caller and
    # the batch-6 doubled-prefix regression keep their meaning.
    assert glc.branch_name("lane-a-539-x") == "worktree-lane-a-539-x"


def test_a_cloud_contract_pairs_its_slug_with_the_claude_branch(cloud_contract):
    match = glc._PAIRING_RE.search(cloud_contract)
    assert match is not None
    assert match.group("branch") == "claude/lane-a-539-ch8-codification"
    assert "worktree-" not in match.group("branch")


def test_an_interactive_contract_pairs_slug_to_contract_with_no_branch(interactive_contract):
    assert glc._PAIRING_RE.search(interactive_contract) is None, \
        "an interactive session has no lane branch to declare"
    match = glc._PAIRING_NO_BRANCH_RE.search(interactive_contract)
    assert match is not None
    assert match.group("slug") == "lane-a-539-ch8-codification"
    assert match.group("file") == "LANE-a-539-ch8-codification.md"
    assert glc.parse_contract(interactive_contract).branch is None


def test_only_a_local_contract_states_an_effort_on_its_command_line():
    """`Dispatch-CloudV2` has no `-Effort` parameter, so demanding one would be wrong.

    The tier is still on the record for every shape — the routing row carries it — which is
    why this asserts the SOURCE moves rather than that the requirement disappears.
    """
    assert glc.parse_contract(glc.render_contract(_spec())).effort == "high"
    for shape in ("cloud", "interactive"):
        parsed = glc.parse_contract(glc.render_contract(_spec(shape=shape)))
        assert parsed.effort is None
        assert parsed.problems == ()
        assert "| opus | execute | high |" in glc.render_contract(_spec(shape=shape))


def test_the_receipt_gate_rides_the_cloud_shape_and_nothing_else(interactive_contract):
    assert f"## {glc.CLOUD_SECTION}" not in interactive_contract
    for field_name in glc.RECEIPT_FIELDS:
        assert field_name not in interactive_contract


@pytest.mark.parametrize("shape", glc.SHAPE_ENUM)
def test_the_cli_emits_every_shape_and_the_written_file_checks_clean(tmp_path, shape):
    runner = CliRunner()
    out = tmp_path / shape
    result = runner.invoke(glc.cli, [
        "emit", "--slug", "lane-b-101-widget", "--purpose", "build the widget",
        "--id", "101", "--shape", shape, "--out-dir", str(out)])
    assert result.exit_code == 0, result.output
    written = out / "LANE-b-101-widget.md"
    assert glc.parse_contract(written.read_text(encoding="utf-8"),
                              expect_shape=shape).problems == ()


def test_the_cli_refuses_an_off_enum_shape(tmp_path):
    result = CliRunner().invoke(glc.cli, [
        "emit", "--slug", "lane-b-101-widget", "--purpose", "x", "--shape", "remote",
        "--out-dir", str(tmp_path)])
    assert result.exit_code != 0
    assert not list(tmp_path.iterdir()), "a refused emit leaves no file behind"


def test_the_emit_log_line_names_the_command_for_the_shape_it_wrote(tmp_path, caplog):
    """The operator reads this line off the terminal — it is a dispatch surface too."""
    with caplog.at_level("INFO", logger="gen-lane-contract"):
        result = CliRunner().invoke(glc.cli, [
            "emit", "--slug", "lane-b-101-widget", "--purpose", "x", "--shape", "cloud",
            "--out-dir", str(tmp_path)])
    assert result.exit_code == 0, result.output
    logged = " ".join(r.getMessage() for r in caplog.records)
    assert "Dispatch-CloudV2" in logged
    assert "Dispatch-Lane" not in logged


def test_the_emit_log_line_for_an_interactive_contract_says_to_start_claude_first(
        tmp_path, caplog):
    """The interactive line is a MESSAGE, so the log has to say what to do with it.

    Added after a mutation survived: flipping the interactive branch of the emit log to the
    generic form left every test green, because the only log assertion covered the cloud
    shape. Logging `Read <PROMPTS_DIR>\\… ` with no instruction reads like a shell command,
    which is exactly the confusion this shape invites.
    """
    with caplog.at_level("INFO", logger="gen-lane-contract"):
        result = CliRunner().invoke(glc.cli, [
            "emit", "--slug", "lane-b-101-widget", "--purpose", "x", "--shape",
            "interactive", "--out-dir", str(tmp_path)])
    assert result.exit_code == 0, result.output
    logged = " ".join(r.getMessage() for r in caplog.records)
    assert "start `claude`" in logged
    assert "and execute it exactly." in logged


def test_the_enums_command_prints_the_shape_surface():
    result = CliRunner().invoke(glc.cli, ["enums"])
    assert result.exit_code == 0
    for shape in glc.SHAPE_ENUM:
        assert shape in result.output
