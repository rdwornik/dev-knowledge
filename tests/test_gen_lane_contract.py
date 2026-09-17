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

import contextlib as _contextlib
import logging as _logging
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import gen_handoff as gh  # noqa: E402
import gen_lane_contract as glc  # noqa: E402


@_contextlib.contextmanager
def caplog_at_info():
    """Collect this module's own log records as plain strings.

    `caplog` is the obvious tool and it is not the right one here: `gen_lane_contract`
    configures logging at import (`logging.basicConfig`), so the records a CliRunner run emits
    reach the module's own handler rather than pytest's capture in every invocation order. A
    local handler is deterministic and does not depend on which test ran first.
    """
    records: list[str] = []

    class _Collect(_logging.Handler):
        def emit(self, record):  # noqa: D102
            records.append(record.getMessage() % () if not record.args
                           else record.getMessage())

    handler = _Collect()
    logger = _logging.getLogger("gen-lane-contract")
    logger.addHandler(handler)
    previous = logger.level
    logger.setLevel(_logging.INFO)
    try:
        yield records
    finally:
        logger.setLevel(previous)
        logger.removeHandler(handler)


# --- fixtures ---------------------------------------------------------------------------

def _spec(**over) -> glc.LaneSpec:
    base = dict(slug="lane-a-539-ch8-codification",
                purpose="codify the dispatch system into PLAYBOOK Ch8",
                # `[#787]`: the lane KIND is declared, never inferred, and has no default -- so
                # every fixture states one. `code` is this fixture's honest value and it is the
                # kind clause 2 leaves free on either half of the plan/implement split, which
                # keeps the existing cases testing what they were written to test.
                kind="code",
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
        "emit", "--kind", "code", "--slug", "lane-b-101-widget", "--purpose", "build the widget",
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



def test_check_takes_MANY_paths_because_the_pre_commit_hook_passes_many(tmp_path):
    """The gate died with `Got unexpected extra arguments` the first time a batch staged
    more than one contract in one commit -- it did not refuse a bad contract, it failed to
    RUN. Found 2026-08-29 freezing six contracts at once; earlier batches staged them
    singly, so a single-`PATH` signature survived unnoticed.
    """
    runner = CliRunner()
    made = []
    for i, slug in enumerate(("lane-a-201-one", "lane-b-202-two", "lane-c-203-three")):
        f = tmp_path / f"LANE-{slug}.md"
        f.write_text(glc.render_contract(_spec(slug=slug, task_id=str(201 + i))),
                     encoding="utf-8", newline="\n")
        made.append(str(f))
    assert runner.invoke(glc.cli, ["check", *made]).exit_code == 0


def test_check_reports_EVERY_bad_path_rather_than_stopping_at_the_first(tmp_path, caplog):
    """One broken contract must not mask the rest: a gate that exits on the first failure
    turns a batch freeze into a one-at-a-time bisect."""
    runner = CliRunner()
    good = tmp_path / "LANE-a-204-good.md"
    good.write_text(glc.render_contract(_spec(slug="lane-a-204-good", task_id="204")),
                    encoding="utf-8", newline="\n")
    bad1 = tmp_path / "LANE-b-205-bad.md"
    bad1.write_text("# LANE lane-b-205-bad", encoding="utf-8")
    bad2 = tmp_path / "LANE-c-206-bad.md"
    bad2.write_text("# LANE lane-c-206-bad", encoding="utf-8")

    import logging
    with caplog.at_level(logging.ERROR):
        res = runner.invoke(glc.cli, ["check", str(good), str(bad1), str(bad2)])
    assert res.exit_code == 1
    reported = caplog.text
    assert "205" in reported and "206" in reported, reported


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
    mangled = local_contract.replace(" --effort high", "", 1)
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
        "emit", "--kind", "code", "--slug", "lane-b-101-widget", "--purpose", "x", "--effort", "ultra",
        "--out-dir", str(tmp_path)])
    assert result.exit_code != 0
    assert "ultra" in result.output
    assert not list(tmp_path.iterdir()), "a refused emit leaves no file behind"


def test_a_contract_whose_dispatch_line_carries_an_off_enum_effort_is_reported(local_contract):
    mangled = local_contract.replace("--effort high", "--effort ultra", 1)
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


def test_809_a_multi_letter_batch_slug_is_emitted_without_loose_slug(tmp_path):
    """`[#809]` Done-when (2). Batch AB had to emit its contracts with `--loose-slug`, because
    the strict grammar refused `lane-ab-...`. With the token widened, the strict default
    accepts it."""
    assert glc.validate_slug("lane-ab-808-guard-timeout", strict=True) ==         "lane-ab-808-guard-timeout"
    result = CliRunner().invoke(glc.cli, [
        "emit", "--kind", "code", "--slug", "lane-ab-808-guard-timeout", "--purpose", "a guard timeout",
        "--id", "808", "--out-dir", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert (tmp_path / "LANE-ab-808-guard-timeout.md").is_file()


def test_the_contract_filename_drops_a_leading_lane_token():
    assert glc.contract_filename("lane-a-539-ch8") == "LANE-a-539-ch8.md"
    assert glc.contract_filename("changelog-sync") == "LANE-changelog-sync.md"


def test_emit_refuses_to_overwrite_a_frozen_contract_without_force(tmp_path):
    runner = CliRunner()
    args = ["emit", "--kind", "code", "--slug", "lane-b-101-widget", "--purpose", "x", "--out-dir", str(tmp_path)]
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

    THE MUTATION IS BUILT FROM `dispatch_command`, NOT TYPED. It was a literal until
    2026-09-11, when `[#717]` put `-Model` on the line and the literal stopped matching: the
    deletion silently deleted nothing and the test would have gone vacuous. It did not, because
    the "did the mutation bite" guard below caught it — that guard is why this test reported a
    changed premise instead of a false pass. Deriving the line from the emitter closes the
    class rather than re-typing today's spelling, which would rot at the next flag.
    """
    doomed = glc.dispatch_command(
        "lane-a-539-ch8-codification", "LANE-a-539-ch8-codification.md", "high", "local",
        glc.DEFAULT_MODEL)
    assert doomed in local_contract, doomed
    mangled = local_contract.replace(doomed + "\n", "", 1)
    assert "Dispatch-Lane lane-a-539" not in mangled, "the mutation did not bite"
    problems = glc.parse_contract(mangled).problems
    assert any("no dispatch command line" in p for p in problems), problems


@pytest.mark.parametrize("shape, present, absent", [
    ("local", "claude --bg --model ", ("Dispatch-CloudV2", "and execute it exactly")),
    ("cloud", "Dispatch-CloudV2 ", ("claude --bg --model ", "and execute it exactly")),
    ("interactive", "and execute it exactly", ("claude --bg --model ", "Dispatch-CloudV2")),
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


def test_the_shape_enum_is_exactly_the_four_ch8_names():
    """The enum is CLOSED and this test is the closing.

    It was three names until 2026-08-31, when `codespace` entered by ruling (R-ENUM). Widened
    here rather than deleted, because the property under test is not the arity: it is that a
    shape enters this enum only by a recorded ruling and never by a lane, a generator or an
    integrator. This assertion is what makes a silent fourth member impossible, and the same
    assertion is what makes the fourth one traceable to the act that admitted it.
    """
    assert glc.SHAPE_ENUM == ("local", "cloud", "interactive", "codespace")
    assert glc.DEFAULT_SHAPE == "local"


def test_the_branch_derivation_follows_the_shape():
    """Ch8 puts a cloud lane on `claude/<slug>`, not on `worktree-<slug>`.

    The pre-lane generator emitted the worktree branch for every shape, so a cloud contract
    declared a branch its own transport would never create.
    """
    assert glc.branch_name("lane-a-539-x", "local") == "worktree-lane-a-539-x"
    assert glc.branch_name("lane-a-539-x", "cloud") == "claude/lane-a-539-x"
    assert glc.branch_name("lane-a-539-x", "interactive") is None
    # R-ENUM leg 3: OFF-MACHINE is not the same axis as CLOUD. A codespace lane commits and
    # pushes like a local one, so it keeps `worktree-`; reading "off-machine" as "claude/"
    # here would have emitted a branch nothing creates, which is the cloud defect in mirror.
    assert glc.branch_name("lane-a-539-x", "codespace") == "worktree-lane-a-539-x"
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
        "emit", "--kind", "code", "--slug", "lane-b-101-widget", "--purpose", "build the widget",
        "--id", "101", "--shape", shape, "--out-dir", str(out)])
    assert result.exit_code == 0, result.output
    written = out / "LANE-b-101-widget.md"
    assert glc.parse_contract(written.read_text(encoding="utf-8"),
                              expect_shape=shape).problems == ()


def test_the_cli_refuses_an_off_enum_shape(tmp_path):
    result = CliRunner().invoke(glc.cli, [
        "emit", "--kind", "code", "--slug", "lane-b-101-widget", "--purpose", "x", "--shape", "remote",
        "--out-dir", str(tmp_path)])
    assert result.exit_code != 0
    assert not list(tmp_path.iterdir()), "a refused emit leaves no file behind"


def test_the_emit_log_line_names_the_command_for_the_shape_it_wrote(tmp_path, caplog):
    """The operator reads this line off the terminal — it is a dispatch surface too."""
    with caplog.at_level("INFO", logger="gen-lane-contract"):
        result = CliRunner().invoke(glc.cli, [
            "emit", "--kind", "code", "--slug", "lane-b-101-widget", "--purpose", "x", "--shape", "cloud",
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
            "emit", "--kind", "code", "--slug", "lane-b-101-widget", "--purpose", "x", "--shape",
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


# --- 6. R-ENUM — `codespace` in the contract grammar (ruling 2026-08-31, class [#514]) ------
#
# The substrate was ADMITTED for running on 2026-08-31 (3-of-3 legs green on a fresh create)
# and remained UNADMITTED in the vocabulary this module enforces, which is a different
# admission. Three closed enums refused it and the tier-(D) proof-of-work lane could not be
# frozen: the SHAPE enum here, the dispatch-verb table `_COMMAND_RES`, and the pairing rule.
# The failure class is [#514]'s — `validate_substrate` read `codespace` off
# `ecosystem/substrate-registry.yaml` and ACCEPTED the same contract this gate REFUSED, so one
# vocabulary carried two verdicts and a contract could pass the freeze gate and fail the shape
# gate. These witnesses are written to the RULING, not to the implementation.

@pytest.fixture()
def codespace_contract() -> str:
    return glc.render_contract(_spec(shape="codespace"))


def test_codespace_is_in_the_shape_enum(codespace_contract):
    """Leg 1 of R-ENUM. Without this the other two legs have nothing to attach to."""
    assert "codespace" in glc.SHAPE_ENUM
    assert glc.validate_shape("codespace") == "codespace"
    assert "codespace" in glc.SHAPE_GLOSS


def test_an_emitted_codespace_contract_parses_with_no_problems(codespace_contract):
    parsed = glc.parse_contract(codespace_contract, expect_shape="codespace")
    assert parsed.problems == (), parsed.problems
    assert parsed.ok


def test_a_codespace_contract_carries_the_dispatch_codespace_verb(codespace_contract):
    """Leg 2 — the dispatch-verb enum. The emitted form is the Ch8 table's row 4 verb, and
    it is NOT either on-machine form: a lane handed another shape's command is worse than
    one handed none, because a wrong command looks authoritative."""
    assert "Dispatch-Codespace -Contract " in codespace_contract
    assert glc._DISPATCH_LINE_RE.search(codespace_contract) is None
    assert glc._CLOUD_DISPATCH_LINE_RE.search(codespace_contract) is None
    assert glc.find_command_line(codespace_contract).startswith("Dispatch-Codespace")


def test_a_codespace_contract_carries_its_declared_model_on_the_dispatch_line(codespace_contract):
    """[#810] Done-contract clause 2: `Dispatch-Codespace` carries `-Model <m>` from the
    contract's own routing row -- the same failure class `[#717]` closed for the local
    transport. Before this, the docstring on `dispatch_command` said in as many words that
    `Dispatch-Codespace` carries no such parameter; a codespace lane dispatched at whatever
    the runner defaulted to, unstated and unchecked against the routing row."""
    assert "-Model opus" in codespace_contract, codespace_contract
    parsed = glc.parse_contract(codespace_contract, expect_shape="codespace")
    assert parsed.problems == (), parsed.problems


def test_the_codespace_dispatch_line_regex_ADMITS_a_model_flag():
    """A generator rendering what its own parser rejects is worse than one omitting it --
    the same lesson `[#717]` applied to the local form's regex."""
    line = "Dispatch-Codespace -Contract LANE-a-1-example.md -Slug lane-a-1-example -Model sonnet"
    match = glc._CODESPACE_DISPATCH_LINE_RE.search(line)
    assert match is not None, f"the checker refuses its own generator's line: {line!r}"
    assert match.group("model") == "sonnet"


def test_a_codespace_dispatch_line_carrying_a_model_the_routing_row_contradicts_is_REPORTED(
        codespace_contract):
    """Two sources free to disagree is the class this generator removes, and this pair is
    the one that costs money -- exactly `[#717]`'s reasoning, applied to the third shape."""
    contract = codespace_contract.replace("-Model opus", "-Model sonnet")
    problems = glc.parse_contract(contract, expect_shape="codespace").problems
    assert any("model" in p.lower() for p in problems), problems


def test_a_codespace_dispatch_line_carrying_a_model_outside_the_enum_is_REPORTED(
        codespace_contract):
    """The admitted value is held to `MODEL_ENUM`, exactly as the local form's already is."""
    contract = codespace_contract.replace("-Model opus", "-Model gpt")
    problems = glc.parse_contract(contract, expect_shape="codespace").problems
    assert any("gpt" in p for p in problems), problems


def test_a_codespace_lane_pairs_a_worktree_branch_not_a_claude_one(codespace_contract):
    """Leg 3 — the pairing rule. A codespace lane COMMITS like a local lane, merely
    elsewhere, so it runs on `worktree-<slug>`; `claude/` is the cloud transport's prefix and
    nothing in a codespace creates it."""
    assert glc.branch_name("lane-a-539-ch8-codification", "codespace") == (
        "worktree-lane-a-539-ch8-codification")
    parsed = glc.parse_contract(codespace_contract, expect_shape="codespace")
    assert parsed.branch == "worktree-lane-a-539-ch8-codification"


def test_a_codespace_contract_with_a_claude_prefixed_pairing_is_reported(codespace_contract):
    mangled = codespace_contract.replace(
        "branch `worktree-lane-a-539-ch8-codification`",
        "branch `claude/lane-a-539-ch8-codification`", 1)
    problems = glc.parse_contract(mangled, expect_shape="codespace").problems
    assert any("worktree-lane-a-539-ch8-codification" in p for p in problems), problems


def test_a_codespace_lane_carries_a_receipt_gate_with_its_own_fields(codespace_contract):
    """The receipt gate is an OFF-MACHINE rule, not a cloud-only one — Ch8's row 4 states it
    for this substrate in its own words (`receipt.json` is pulled back out, and `Ok` and
    `RemoteExitCode` are read separately). Its FIELDS differ from cloud's, because the traps
    differ: a codespace receipt can carry `subtype: "success"` with `is_error: true`."""
    assert f"## {glc.CLOUD_SECTION}" in codespace_contract
    for field_name in glc.RECEIPT_FIELDS_BY_SHAPE["codespace"]:
        assert field_name in codespace_contract
    for cloud_field in glc.RECEIPT_FIELDS:
        assert cloud_field not in codespace_contract


def test_a_codespace_lane_missing_a_receipt_field_is_reported(codespace_contract):
    field_name = glc.RECEIPT_FIELDS_BY_SHAPE["codespace"][0]
    mangled = codespace_contract.replace(field_name, "something-else", 1)
    problems = glc.parse_contract(mangled, expect_shape="codespace").problems
    assert any(field_name in p for p in problems), problems


def test_a_codespace_contract_that_dropped_its_receipt_gate_is_reported(codespace_contract):
    mangled = codespace_contract.replace(f"## {glc.CLOUD_SECTION}", "## Notes", 1)
    problems = glc.parse_contract(mangled, expect_shape="codespace").problems
    assert any(glc.CLOUD_SECTION in p for p in problems), problems


def test_the_receipt_shapes_are_exactly_the_off_machine_ones():
    """Stated as a set so a fourth shape cannot be added without deciding this question."""
    assert set(glc.RECEIPT_SHAPES) == {"cloud", "codespace"}
    assert set(glc.RECEIPT_FIELDS_BY_SHAPE) == set(glc.RECEIPT_SHAPES)


def test_the_playbook_dispatch_table_carries_the_codespace_pairing_rule():
    """SOLE-site discipline: the Ch8 dispatch table is the only place in the repository that
    carries a literal launch command, so the verb this module emits has to be the verb that
    table publishes — and the table has to state the pairing rule the gate enforces. A
    generator free to invent a rival form is the drift this ruling closes."""
    playbook = (_REPO_ROOT / "protocols" / "PLAYBOOK.md").read_text(encoding="utf-8")
    table = playbook.split("#### The dispatch table — the SOLE literal-command site", 1)[1]
    table = table.split("#### Standing operator-interface rules", 1)[0]
    assert glc.dispatch_command(
        "lane-a-539-ch8-codification", "LANE-a-539-ch8-codification.md", "high",
        "codespace").split()[0] in table
    # Scoped to ROW 4, not to the whole table: `worktree-` appears in row 1 (the LOCAL row),
    # so an unscoped `in table` assertion passes on a table that never states the codespace
    # pairing at all. That vacuous form was written first and caught here.
    row4 = table.split("**4 — CODESPACE**", 1)[1]
    row4 = row4.split("##### Where the contract file lives", 1)[0]
    assert "worktree-" in row4, "Ch8 row 4 does not state the codespace branch pairing"
    assert "claude/" in row4, "Ch8 row 4 does not say which prefix a codespace lane is NOT on"


# --- 5. [#630] — the hook runs on an empty set, and never passes vacuously -----------------
#
# `lane-contract-check` gains `always_run: true` and KEEPS filename passing. `paths` must
# therefore stop being a REQUIRED argument, or the hook errors out (`Missing argument 'PATHS'`)
# on the first commit that does not touch a `LANE-*.md` — the opposite of "runs on an empty set".
#
# WHY NOT `pass_filenames: false`, which this lane originally shipped (terra P1, 2026-09-02).
# The `provider-registry` / `audit-health` hooks set it because they take NO input: they scan the
# tree themselves. `lane-contract-check` is the opposite — its CONTRACT-MANIFEST predicate
# compares the manifest against *the contracts it was handed*, and with `pass_filenames: false`
# it is handed none, on EVERY invocation including the freeze commit that stages them. MEASURED
# with a real contract staged: `contract-manifest predicate ([#630]): 0 contract(s) given —
# 0 checked`, i.e. `open_batches` was never reached and a slug mismatch still passed. The lane
# satisfied "runs on an empty set" by severing the input the predicate needs, which is the
# vacuous pass this row exists to end, in a new costume.

import yaml  # noqa: E402


def test_the_precommit_hook_runs_on_every_commit_AND_still_receives_its_contracts():
    """Both halves, because this lane shipped the first without the second.

    `always_run: true` makes the gate fire on a commit that stages no `LANE-*.md` — a
    `files:`-globbed gate disappears exactly when nothing looks suspicious. But filename
    passing must SURVIVE, or the CONTRACT-MANIFEST predicate is handed nothing on every
    invocation and reports `0 checked` forever while a slug mismatch sails through.
    """
    config = yaml.safe_load(
        (_REPO_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    hooks = {h["id"]: h for repo in config["repos"] for h in repo.get("hooks", ())}
    hook = hooks["lane-contract-check"]
    assert hook.get("always_run") is True, hook
    assert hook.get("pass_filenames") is not False, (
        "pass_filenames must not be False: the predicate compares the manifest against the "
        "contracts it is HANDED, so suppressing filenames makes it unreachable", hook)


def test_check_runs_with_zero_paths_instead_of_erroring():
    """Before this lane, `paths` was `required=True` — pre-commit's now-unconditional
    invocation would have died with `Missing argument 'PATHS'` on every ordinary commit."""
    result = CliRunner().invoke(glc.cli, ["check"])
    assert result.exit_code == 0, result.output


# --- 6. [#630] — the CONTRACT-MANIFEST predicate --------------------------------------------
#
# An OPEN batch's manifest and the contract set `check` is handed must declare the SAME set
# of lane slugs. Seeded from task-630's own measured defect (batch E, integrator defect (b),
# ruled 2026-09-01): the manifest named `lane-b-2-essentials-and-claude-md`; what was actually
# dispatched, and what carries the commit, pairs to `lane-b-3-claude-md-genre`. The slug was
# renumbered between draft and dispatch and nothing anywhere compared the two. The pure
# comparison (`batch_manifest.freeze_manifest_contract_agreement`) is already unit-tested in
# `tests/test_batch_manifest.py`; these tests are the WIRING — `open_batches` imported by
# name into this module, so a `monkeypatch.setattr(glc, "open_batches", ...)` reaches it.

import batch_manifest as bm  # noqa: E402


def _write_open_manifest(tmp_path, table: str, *,
                         name="2026-09-02-technical-batch-z-manifest.md") -> "bm.OpenBatch":
    rel = f"docs/audits/{name}"
    target = tmp_path / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"---\nbatch: z\nstatus: open\nclosed_by: docs/audits/2026-09-02-x-packet.md\n---\n\n"
        f"{table}", encoding="utf-8", newline="\n")
    return bm.OpenBatch(batch="z", path=rel, closed_by="docs/audits/2026-09-02-x-packet.md")


def test_check_reports_zero_checked_when_given_no_contracts(caplog):
    """The empty-set case pre-commit now hits on every commit: it must be VISIBLE in the
    log that the predicate ran and found nothing to compare, not merely silent."""
    import logging
    with caplog.at_level(logging.INFO):
        result = CliRunner().invoke(glc.cli, ["check"])
    assert result.exit_code == 0, result.output
    assert "0 checked" in caplog.text, caplog.text


def test_check_reports_zero_checked_when_no_batch_is_open(tmp_path, monkeypatch, caplog):
    import logging
    monkeypatch.setattr(glc, "open_batches", lambda repo_root: [])
    contract = tmp_path / "LANE-a-1-x.md"
    contract.write_text(glc.render_contract(_spec(slug="lane-a-1-x", task_id="1")),
                        encoding="utf-8", newline="\n")
    with caplog.at_level(logging.INFO):
        result = CliRunner().invoke(glc.cli, ["check", str(contract)])
    assert result.exit_code == 0, result.output
    assert "0 checked" in caplog.text, caplog.text


def test_check_refuses_the_measured_batch_e_slug_renumbering(tmp_path, monkeypatch):
    """Seeded from the real defect (task-630): fails if the predicate is removed."""
    open_batch = _write_open_manifest(tmp_path, (
        "## THE LANES\n\n```\n"
        "DC-1   lane-a-1-vision-to-readme          worktree-lane-a-1-...   local   --\n"
        "DC-23  lane-b-2-essentials-and-claude-md  worktree-lane-b-2-...   local   DC-1\n"
        "```\n"))
    monkeypatch.setattr(glc, "_SCRIPTS", tmp_path / "scripts")
    monkeypatch.setattr(glc, "open_batches", lambda repo_root: [open_batch])

    a1 = tmp_path / "LANE-a-1-vision-to-readme.md"
    a1.write_text(glc.render_contract(_spec(slug="lane-a-1-vision-to-readme", task_id="1")),
                 encoding="utf-8", newline="\n")
    # Renumbered -- the manifest above still says `lane-b-2-...`, matching the measured defect.
    b3 = tmp_path / "LANE-b-3-claude-md-genre.md"
    b3.write_text(glc.render_contract(_spec(slug="lane-b-3-claude-md-genre", task_id="3")),
                 encoding="utf-8", newline="\n")

    result = CliRunner().invoke(glc.cli, ["check", str(a1), str(b3)])
    assert result.exit_code == 1, result.output


def test_check_admits_a_manifest_and_contract_set_that_agree(tmp_path, monkeypatch, caplog):
    import logging
    open_batch = _write_open_manifest(tmp_path, (
        "## THE LANES\n\n```\n"
        "L1  lane-a-1-vision-to-readme  worktree-lane-a-1-...  local  --\n"
        "```\n"))
    monkeypatch.setattr(glc, "_SCRIPTS", tmp_path / "scripts")
    monkeypatch.setattr(glc, "open_batches", lambda repo_root: [open_batch])

    a1 = tmp_path / "LANE-a-1-vision-to-readme.md"
    a1.write_text(glc.render_contract(_spec(slug="lane-a-1-vision-to-readme", task_id="1")),
                 encoding="utf-8", newline="\n")

    with caplog.at_level(logging.INFO):
        result = CliRunner().invoke(glc.cli, ["check", str(a1)])
    assert result.exit_code == 0, result.output
    assert "0 checked" not in caplog.text, caplog.text


def test_check_refuses_a_manifest_naming_a_contract_no_manifest_row_declares(tmp_path,
                                                                             monkeypatch):
    """The OTHER direction: a committed contract absent from the open manifest's lane table
    fails just as loudly as a phantom manifest row."""
    open_batch = _write_open_manifest(tmp_path, (
        "## THE LANES\n\n```\nL1  lane-a-1-vision-to-readme  worktree-lane-a-1-...  local  --\n"
        "```\n"))
    monkeypatch.setattr(glc, "_SCRIPTS", tmp_path / "scripts")
    monkeypatch.setattr(glc, "open_batches", lambda repo_root: [open_batch])

    a1 = tmp_path / "LANE-a-1-vision-to-readme.md"
    a1.write_text(glc.render_contract(_spec(slug="lane-a-1-vision-to-readme", task_id="1")),
                 encoding="utf-8", newline="\n")
    stray = tmp_path / "LANE-c-3-stray.md"
    stray.write_text(glc.render_contract(_spec(slug="lane-c-3-stray", task_id="3")),
                     encoding="utf-8", newline="\n")

    result = CliRunner().invoke(glc.cli, ["check", str(a1), str(stray)])
    assert result.exit_code == 1, result.output


def test_a_contract_OUTSIDE_the_repo_is_not_compared_against_an_open_batch(tmp_path,
                                                                           monkeypatch, caplog):
    """SCOPE: only contracts living in the tree are the batch's (integrator, 2026-09-02).

    Measured after `pass_filenames` was restored: with batch G genuinely open, `check` on three
    `tmp_path` fixtures exited 1, because their slugs are absent from G's manifest. That is a
    refusal about the FIXTURE, not about the repo — and it broke two tests that had nothing to
    do with the predicate. A contract outside the tree belongs to no open batch.

    The seeded batch-E tests are unaffected and that is the point of this pair: they monkeypatch
    `_SCRIPTS` so `tmp_path` IS their repo root, so their contracts are in-tree and still
    compared. If this guard over-filtered, those refusal tests would go vacuously green.
    """
    import logging
    open_batch = _write_open_manifest(tmp_path, (
        "## THE LANES\n\n```\n"
        "L1  lane-a-1-in-the-manifest  worktree-lane-a-1-...  local  --\n"
        "```\n"))
    # NOTE: _SCRIPTS deliberately NOT patched -- repo_root stays the real tree, so the
    # contract below is genuinely outside it, which is the condition under test.
    monkeypatch.setattr(glc, "open_batches", lambda repo_root: [open_batch])

    stray = tmp_path / "LANE-z-999-not-in-any-batch.md"
    stray.write_text(glc.render_contract(_spec(slug="lane-z-999-not-in-any-batch",
                                               task_id="999")),
                     encoding="utf-8", newline="\n")

    with caplog.at_level(logging.INFO):
        result = CliRunner().invoke(glc.cli, ["check", str(stray)])
    assert result.exit_code == 0, result.output
    assert "none in this repo" in caplog.text, caplog.text
# --- 5. [#718]: the generator writes where the dispatch verb READS -------------------------
#
# RED-first witness, ADR-108 section B. Measured at full batch scale before it was written:
# batch W emitted SIX lane contracts into `to-cc/` while `Dispatch-Lane` resolves against the
# prompts root, and all six were REFUSED. Two literals where there should be one key -- and
# both were individually CORRECT about the root they named, which is why review never caught
# it: there is no wrong line to find, only two right lines that disagree.
#
# The assertion is the row's Done-when verbatim: the written path EQUALS the path the verb
# resolves, both from ONE key. Against the code these tests were written for,
# `_default_out_dir()` returned `Path.cwd()` and this section is RED.


def test_the_generators_default_out_dir_IS_the_root_the_verb_reads(tmp_path, monkeypatch):
    """ONE KEY, asserted as an identity rather than as two agreeing literals.

    `gen_handoff.transport_root()` is the reader's own resolution rule, already in the tree and
    already tested: `CLAUDE_PROMPTS_DIR`, with the documented `~/Downloads` fallback and None on
    unresolved. This test says the writer's default is not a second implementation that happens
    to agree -- it is that function. A test comparing two string literals would stay green
    through exactly the drift `[#718]` records.
    """
    prompts = tmp_path / "prompts-root"
    prompts.mkdir()
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(prompts))
    monkeypatch.chdir(tmp_path)  # cwd is deliberately NOT the prompts root -- the `to-cc/` half

    assert glc._default_out_dir() == gh.transport_root()
    assert glc._default_out_dir() == prompts


def test_emit_writes_the_contract_where_the_dispatch_line_it_prints_will_be_read(tmp_path,
                                                                                 monkeypatch):
    """The end-to-end property: `emit` puts the file where `Dispatch-Lane <file>` resolves it.

    The dispatch line carries a BARE FILENAME -- the verb resolves it against the prompts root
    itself -- so writer and reader agreeing is the whole contract between them. This is the
    batch-W failure reproduced at one lane's scale: emit from a cwd that is not the prompts
    root, then look for the file where the verb would.
    """
    prompts = tmp_path / "prompts-root"
    prompts.mkdir()
    elsewhere = tmp_path / "to-cc"
    elsewhere.mkdir()
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(prompts))
    monkeypatch.chdir(elsewhere)

    result = CliRunner().invoke(glc.cli, [
        "emit", "--kind", "code", "--slug", "lane-x-718-one-key", "--purpose", "one key for writer and reader",
        "--id", "718"])
    assert result.exit_code == 0, result.output

    fname = glc.contract_filename("lane-x-718-one-key")
    resolved_by_the_verb = gh.transport_root() / fname
    assert resolved_by_the_verb.exists(), (
        f"emit wrote nothing at {resolved_by_the_verb} -- the verb reads the prompts root and "
        f"the writer used {Path.cwd()}; that split is [#718]")
    assert not (elsewhere / fname).exists(), (
        "emit wrote into the cwd as well as the prompts root -- two locations is the defect "
        "wearing the fix's clothes")


def test_an_UNRESOLVED_prompts_directory_is_a_REFUSAL_and_not_a_silent_fall_back_to_cwd(
        tmp_path, monkeypatch):
    """`[#718]`'s own words: "the refusal is the good outcome here, and it should survive the fix".

    Six refusals cost six dispatches; six contracts silently read from a stale location would
    have cost six lanes running against the wrong text. So when the ONE key resolves to nothing,
    `emit` refuses -- it does not quietly write to `Path.cwd()`, which is precisely how the
    split would come back invisibly. `transport_root` already returns None for this case
    (DEFECT E-29's reading); this asserts the generator honours it.
    """
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(tmp_path / "does-not-exist"))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(gh.Path, "home", staticmethod(lambda: tmp_path / "no-home"))

    result = CliRunner().invoke(glc.cli, [
        "emit", "--kind", "code", "--slug", "lane-x-718-unresolved", "--purpose", "refuse rather than guess",
        "--id", "718"])
    assert result.exit_code != 0, result.output
    assert "CLAUDE_PROMPTS_DIR" in result.output, result.output
    assert not list(tmp_path.glob("LANE-*.md")), (
        "emit fell back to the cwd on an unresolved prompts root -- that restores the "
        "writer/reader split silently, which is worse than the refusal that surfaced it")


def test_an_explicit_out_dir_still_wins_over_the_resolved_root(tmp_path, monkeypatch):
    """`--out-dir` is an operator override and stays one: the one key is the DEFAULT, not a jail.

    Named because the fix narrows a default, and a fix that also removed the escape hatch would
    break every test fixture and every ad-hoc draft in the tree.
    """
    prompts = tmp_path / "prompts-root"
    prompts.mkdir()
    chosen = tmp_path / "chosen"
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(prompts))
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(glc.cli, [
        "emit", "--kind", "code", "--slug", "lane-x-718-explicit", "--purpose", "the override survives",
        "--id", "718", "--out-dir", str(chosen)])
    assert result.exit_code == 0, result.output

    fname = glc.contract_filename("lane-x-718-explicit")
    assert (chosen / fname).exists()
    assert not (prompts / fname).exists()
# --- 6. [#717]: the launch line is RENDERED FROM the contract's Model row -------------------
#
# RED-first witness, ADR-108 section B. The mechanism, and both halves are individually
# reasonable: `dispatch_command` emitted slug, file and `-Effort` and not `-Model`, while
# `Start-DispatchLane`'s `-Model` parameter defaults to `opus`. Together they mean a contract
# whose own routing row says `sonnet`, dispatched by the line that contract carries, runs at
# `opus` -- silently, and in the expensive direction. Nothing refuses and nothing warns; the
# lane produces work that is entirely plausible and simply cost several times what the
# contract declared.
#
# The checker widens IN THE SAME CHANGE, and that is a Done-contract clause rather than a
# nicety: `_DISPATCH_LINE_RE` was anchored with no `-Model` alternative, so rendering the
# model without widening the regex turns every emitted contract RED at `lane-contract-check`.
# `-Model` is admitted OPTIONAL -- the six frozen batch-X contracts carry none and must keep
# passing -- and where present it is held to AGREE with the routing row, the same conjunction
# `-Effort` already gets.


def test_the_local_dispatch_line_is_rendered_from_the_contracts_own_model_row():
    """`[#717]`'s Done-when: rendered model == the `Model` row. The SONNET case is the witness.

    An opus contract cannot witness this defect at all -- the surface's default is `opus`, so
    the omitted flag and the declared model coincide and the bug is invisible. The fixture is
    therefore deliberately `sonnet`: the one contract shape where "omits the model" and "states
    the model" produce different dispatches.
    """
    contract = glc.render_contract(_spec(model="sonnet"))
    parsed = glc.parse_contract(contract, expect_shape="local")
    assert parsed.problems == (), parsed.problems
    assert parsed.model == "sonnet"
    assert "--model sonnet" in parsed.command, (
        f"the carried line is {parsed.command!r} -- a contract declaring sonnet whose own "
        f"launch line omits the model dispatches at the surface default, opus ([#717])")


def test_the_dispatch_line_regex_ADMITS_a_model_flag():
    """Done-contract clause 2: the CHECKER widens, not only the generator.

    Measured by the dispatcher while freezing batch X: `_DISPATCH_LINE_RE` was
    `^Dispatch-Lane <slug> <file>( -Effort <v>)?\\s*$`, anchored, admitting no `-Model`, so a
    line carrying the model was refused as "no dispatch command line found". A generator
    rendering what its own parser rejects is worse than one omitting it.
    """
    line = "Dispatch-Lane lane-a-1-example LANE-a-1-example.md -Effort high -Model sonnet"
    match = glc._DISPATCH_LINE_RE.search(line)
    assert match is not None, f"the checker refuses its own generator's line: {line!r}"
    assert match.group("model") == "sonnet"
    assert match.group("effort") == "high"


def test_a_dispatch_line_carrying_a_model_the_routing_row_contradicts_is_REPORTED():
    """Two sources free to disagree is the class this generator removes -- `-Effort` already
    gets this conjunction, and after `[#717]` the model gets it too.

    Without this, widening the regex would merely make a contradicting line PARSE.
    """
    contract = glc.render_contract(_spec(model="sonnet")).replace("--model sonnet", "--model opus")
    problems = glc.parse_contract(contract).problems
    assert any("model" in p.lower() for p in problems), problems


def test_a_dispatch_line_carrying_a_model_outside_the_enum_is_REPORTED():
    """The admitted value is held to `MODEL_ENUM`, exactly as the routing row's already is."""
    contract = glc.render_contract(_spec(model="sonnet")).replace("--model sonnet", "--model gpt")
    problems = glc.parse_contract(contract).problems
    assert any("gpt" in p for p in problems), problems


def test_a_LEGACY_contract_carrying_NO_model_flag_still_parses_clean():
    """`-Model` is OPTIONAL on the LEGACY spelling, and this is why the widening is safe.

    Every contract frozen before `[#717]` carries a `Dispatch-Lane` line without it. Making
    the flag mandatory for that spelling would turn the whole existing corpus RED at
    `lane-contract-check` -- the failure mode Done-contract clause 2 names in as many words.

    RE-POINTED AT THE LEGACY FORM by `[#675]` clause 1, and the re-point is the point. The
    amnesty was always about what was ALREADY WRITTEN; this test used to demonstrate it on the
    generator's own output, which conflated "the checker tolerates the frozen corpus" with "the
    generator may emit a model-less line". The emitted `claude` form now REPORTS an absent
    `--model` by name (see the test directly below), so the two halves are separated: amnesty
    for the corpus, structure for what is written next.
    """
    # Built by swapping ONLY the dispatch line of a real emitted contract, never hand-rolled:
    # a synthetic contract would have to restate every other mandatory section, and would then
    # be testing this test's idea of a contract rather than the checker's.
    emitted = glc.render_contract(_spec(model="opus"))
    new_line = glc.find_command_line(emitted)
    assert new_line is not None and new_line.startswith("claude "), new_line
    legacy = emitted.replace(
        new_line,
        "Dispatch-Lane lane-a-539-ch8-codification "
        "LANE-a-539-ch8-codification.md -Effort high", 1)
    parsed = glc.parse_contract(legacy, expect_shape="local")
    assert parsed.problems == (), parsed.problems
    assert parsed.command.endswith("-Effort high")


def test_the_EMITTED_form_omitting_its_model_flag_IS_reported():
    """The other half of the split above -- `[#717]` made structural for the form emitted now.

    The legacy amnesty exists because a corpus was already frozen without the flag. The
    `claude` form has no such history, so on it an absent `--model` is a REFUSAL rather than a
    tolerated omission: a launch line that drops the model dispatches at whatever the surface
    defaults to, and that failure is silent in the expensive direction.
    """
    contract = glc.render_contract(_spec(model="sonnet")).replace(" --model sonnet", "", 1)
    problems = glc.parse_contract(contract).problems

    assert any("--model" in p for p in problems), problems


def test_the_FROZEN_BATCH_X_CONTRACTS_still_pass_after_the_widening():
    """The contract's own step 3 asks for exactly this re-check, against the real files.

    These are immutable frozen contracts carrying pre-`[#717]` launch lines. A regex widening
    that broke them would have broken a live batch mid-flight, and no synthetic fixture proves
    it did not -- so the fixture is the corpus.

    THE HARD-CODED `== 6` IS GONE, and its removal is a repair rather than a loosening. It was
    RED on `main` before `[#675]`'s lane touched anything: `4057be83` and `88f8d4a9` each added
    a contract to this directory after the count was written, so the test failed on its own
    arithmetic BEFORE reaching the property it exists to check -- which is the worse failure,
    because a fixture that cannot run proves nothing about a widening that landed under it. A
    restated roster count is stale at the next commit; the lower bound keeps the only thing the
    number was doing (the fixture is not empty and was not deleted) and the loop below covers
    whatever is actually there.
    """
    frozen = sorted(
        (_REPO_ROOT / "docs" / "audits"
         / "2026-09-11-technical-batch-x-launch-contracts").glob("LANE-*.md"))
    assert len(frozen) >= 6, [p.name for p in frozen]
    for path in frozen:
        parsed = glc.parse_contract(path.read_text(encoding="utf-8"))
        # AMENDED 2026-09-15 BY `[#787]`, AND THE AMENDMENT IS THE HONEST HALF OF ADDING A
        # REQUIRED FIELD. `**Kind:**` is a field none of these contracts could have carried --
        # it did not exist when they were frozen -- so the absent-kind report is the ONE problem
        # a pre-`[#787]` contract is allowed to raise here. Everything else still has to be
        # clean, which is the property this test was written for and which it still checks.
        #
        # THE ALTERNATIVE WAS TO GRANDFATHER INSIDE THE GATE, and it was rejected. An era bound
        # in `parse_contract` would have to key on something -- a date this corpus does not
        # carry in its filenames, or the emitted dispatch form, which splits this very directory
        # 7/1 and would have exempted the wrong file. A gate bent to preserve a test's premise
        # is weaker everywhere; a test amended to record that its premise changed is weaker
        # nowhere. The premise that changed is stated above, in the test, where a reader meets
        # it.
        residual = tuple(pr for pr in parsed.problems if "`**Kind:**" not in pr)
        assert residual == (), f"{path.name}: {residual}"
        assert "-Model" not in parsed.command, (
            f"{path.name} was frozen before [#717]; this test's premise is that it carries no "
            f"model flag, and it now does -- re-point the fixture rather than deleting it")


def test_the_emit_log_line_carries_the_model_it_wrote_into_the_file(tmp_path, monkeypatch):
    """The terminal line the operator reads is a dispatch surface too, and is built from the
    SAME `dispatch_command` the file carries. A model on one and not the other would be
    `[#717]` reproduced between the file and the log."""
    import logging
    prompts = tmp_path / "prompts-root"
    prompts.mkdir()
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(prompts))
    monkeypatch.chdir(tmp_path)

    with caplog_at_info() as records:
        result = CliRunner().invoke(glc.cli, [
            "emit", "--kind", "code", "--slug", "lane-x-717-model-row", "--purpose", "render the model",
            "--id", "717", "--model", "sonnet"])
    assert result.exit_code == 0, result.output
    logged = "\n".join(records)
    assert "--model sonnet" in logged, logged

    written = (prompts / glc.contract_filename("lane-x-717-model-row")).read_text(
        encoding="utf-8")
    assert "--model sonnet" in written
    assert logging  # the import is the fixture's, kept explicit for the reader
# --- 7. [#716]: the step-0 sync region retires ITSELF ---------------------------------------
#
# `[#716]`'s Done-when: "the mandatory step-0 sync is retired from the lane-contract template
# only in the same change that makes that test green". Measured while executing it, the
# retirement surface turned out to be narrower than the clause assumes: the sync region is
# HAND-AUTHORED into each frozen contract and appears in none of `templates/prompt-template.md`
# v1.15, `.claude/commands/lane-boot.md`, `protocols/PLAYBOOK.md` or `render_contract` -- so
# there was no template line to delete, and deleting nothing would have discharged the clause
# vacuously.
#
# So the retirement is made MECHANICAL instead of editorial. The generator gains the region,
# conditioned on the very predicate the row's test asserts: emitted while the base property is
# unheld, absent once it holds, and BACK if the setting is ever unset again. That is a stronger
# reading of "retired in the same change" than a deletion -- a deletion retires it once, this
# retires it exactly when it should be retired, forever.


def test_a_contract_emits_the_step_0_sync_region_while_the_base_property_is_unheld():
    contract = glc.render_contract(_spec(needs_base_sync=True))
    assert "## Step 0 — sync before anything else" in contract
    assert "git merge origin/main" in contract
    assert "[#716]" in contract


def test_a_contract_OMITS_the_step_0_sync_region_once_the_property_holds():
    """The retirement, asserted as an absence. This is the half that has to bite: a region that
    is emitted unconditionally is a region nobody ever removes."""
    contract = glc.render_contract(_spec(needs_base_sync=False))
    assert "Step 0" not in contract
    assert "git merge origin/main" not in contract


def test_the_default_spec_does_not_carry_the_sync_region():
    """`cmd_emit` sets the flag from the live predicate; a hand-built spec defaults to OFF, so
    nothing emits the region by accident once the defect is fixed."""
    assert glc.LaneSpec(slug="lane-a-1-x", purpose="p").needs_base_sync is False
    assert "Step 0" not in glc.render_contract(_spec())


def test_the_sync_region_does_not_disturb_the_mandatory_section_check():
    """Both shapes parse clean. A conditional section that reddened the checker would trade one
    defect for another, and `MANDATORY_SECTIONS` is a subset check for exactly this reason."""
    for flag in (True, False):
        parsed = glc.parse_contract(glc.render_contract(_spec(needs_base_sync=flag)),
                                    expect_shape="local")
        assert parsed.problems == (), (flag, parsed.problems)


def test_rendering_stays_PURE_with_the_flag():
    """`render_contract` must not read the machine: a generator whose output depends on the
    state of whoever ran it cannot be diffed. The live read lives in `cmd_emit`, which is why
    the flag is a spec field rather than a call inside the renderer."""
    assert (glc.render_contract(_spec(needs_base_sync=True))
            == glc.render_contract(_spec(needs_base_sync=True)))
    assert (glc.render_contract(_spec(needs_base_sync=True))
            != glc.render_contract(_spec(needs_base_sync=False)))


def test_emit_sets_the_flag_from_the_LIVE_base_ref_predicate(tmp_path, monkeypatch):
    """End to end: the region tracks `worktree_seed.base_ref_verdict`, not a constant.

    Both directions are exercised, because a wiring that always returned one answer would pass
    a one-directional test while being no predicate at all.
    """
    import worktree_seed as ws

    prompts = tmp_path / "prompts-root"
    prompts.mkdir()
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(prompts))
    monkeypatch.chdir(tmp_path)

    def _verdict(holds):
        return ws.BaseRefVerdict(setting="head", effective="head", base_label="x",
                                 base_sha="a" * 40, main_sha="a" * 40, holds=holds,
                                 why="stubbed for the wiring test")

    for holds, slug in ((False, "lane-x-716-unheld"), (True, "lane-x-716-held")):
        monkeypatch.setattr(glc, "base_ref_verdict", lambda repo, h=holds: _verdict(h))
        result = CliRunner().invoke(glc.cli, [
            "emit", "--kind", "code", "--slug", slug, "--purpose", "wiring", "--id", "716"])
        assert result.exit_code == 0, result.output
        written = (prompts / glc.contract_filename(slug)).read_text(encoding="utf-8")
        assert ("Step 0" in written) is not holds, (
            f"holds={holds} produced the wrong region for {slug}")


def test_opusplan_is_an_admitted_model_tier_end_to_end():
    """`opusplan` is a ROUTED tier, not a typo -- AX22-3 ruled it, and the CLI accepts it.

    RED-first for the wave-3 freeze (2026-09-13). The operator routed two wave-3 lanes to
    `opusplan` ("Opus plans, Sonnet implements"); AX22-3 had already routed the integrator
    SEAT to it, and `to-browser/SEAT-BOOT-integrator.md` renders `model: opusplan` today. The
    generator's enum was the one surface that had not been widened, so a contract stating the
    ruled tier was refused by its own freeze gate while the live verb -- `Dispatch-Lane`, whose
    `-Model` is an unconstrained `[string]` passed to `claude --model` -- ran it happily. That
    asymmetry is AX25-1's root cause in miniature: generator narrower than verb, no test
    between them.

    Measured before widening: `claude --print --model opusplan` returns a normal completion,
    while a bogus id returns `[claude-code:unrecognized_model]`. The enum admits a value the
    CLI resolves, not a hopeful string.

    RE-POINTED 2026-09-15 BY `[#787]` CLAUSE 1, ON A MEASUREMENT TAKEN AFTER THIS TEST WAS
    WRITTEN. The enum-admission property above still holds and is still checked -- `opusplan` is
    a routed tier and the CLI resolves it. What the 2026-09-13 reading of `lane-x-689`'s own
    transcript established is that RESOLVING is not HONOURING: that lane ran 84 of 84 assistant
    messages on `claude-sonnet-5`, because a split tier needs plan mode and every unattended
    dispatch carries `--permission-mode bypassPermissions`, which never enters one. So the tier
    is admitted where a seat can plan (`interactive` -- AX22-3's integrator seat, untouched) and
    REFUSED AT FREEZE where nobody can (`local`, `cloud`, `codespace`).

    The test is amended rather than deleted, and the distinction is the point: the ruling that
    put `opusplan` in the enum is not overturned, it is SCOPED by a measurement of the same
    tier's behaviour on a different substrate. Same word, two populations.
    """
    contract = glc.render_contract(_spec(model="opusplan", shape="interactive"))
    parsed = glc.parse_contract(contract, expect_shape="interactive")
    assert parsed.problems == (), parsed.problems
    assert parsed.model == "opusplan"

    with pytest.raises(glc.LaneContractError, match="opusplan"):
        glc.render_contract(_spec(model="opusplan", shape="local"))


def test_a_model_outside_the_widened_enum_is_STILL_refused():
    """The widening admits one ruled tier; it does not open the field.

    Paired with the test above deliberately. A widening asserted only by its happy path is
    indistinguishable from deleting the check, which is the failure mode `[#717]`'s own
    divergence test was written against.
    """
    contract = glc.render_contract(_spec(model="sonnet")).replace("--model sonnet", "--model gpt")
    problems = glc.parse_contract(contract).problems
    assert any("gpt" in p for p in problems), problems
