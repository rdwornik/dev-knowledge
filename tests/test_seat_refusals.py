"""The five seat refusals REFUSE.

RED-FIRST, and every test here is a removal test. `pytest.raises(SeatRefusal)` fails the moment
the refusal it names stops raising -- which is the property the contract asks for ("each with a
test that FAILS when the refusal is removed"). The passing-path tests exist so that a refusal
cannot be made to pass its own trip-test by refusing everything.

WHY REFUSALS AND NOT WARNINGS. Each of the five is a rule that ALREADY EXISTED in prose and was
broken anyway, in batches T and U, by seats that had read the prose. A warning printed after the
fact is the state being replaced: by then the lane has ended its turn on an intention, the
seventh worktree exists, the substituted reviewer's finding count is in the tally, and the
decision file is on the transport with no carrier. So these raise.
"""
from __future__ import annotations

import pytest
from click.testing import CliRunner

import boot_frontier
import seat_ch8
import seat_refusals as sr


# --- R1 -- the sleeping poll ------------------------------------------------------------------

_GOOD_WAIT = (
    "## 4 - wait for the integrator's PACKET-MERGED\n"
    "<!-- WAIT: interval=120s bound=30 "
    "predicate=to-browser/STATUS-INTEGRATOR.md names this branch as merged -->\n"
)


def test_a_wait_written_as_an_intention_is_refused():
    text = "## 4\n\nWait for the integrator to hand back, then continue.\n"
    with pytest.raises(sr.SeatRefusal, match="sleeping-poll"):
        sr.refuse_sleeping_poll(text, site="SEAT-BOOT-lane.md")


def test_a_wait_declared_as_code_passes():
    assert sr.refuse_sleeping_poll(_GOOD_WAIT, site="t") == 1


def test_a_wait_missing_its_interval_is_refused():
    text = "Wait for the packet.\n<!-- WAIT: bound=30 predicate=STATUS names it -->\n"
    with pytest.raises(sr.SeatRefusal, match="interval"):
        sr.refuse_sleeping_poll(text, site="t")


def test_a_wait_missing_its_bound_is_refused_because_unbounded_is_the_same_stall():
    text = "Wait for the packet.\n<!-- WAIT: interval=60s predicate=STATUS names it -->\n"
    with pytest.raises(sr.SeatRefusal, match="bound"):
        sr.refuse_sleeping_poll(text, site="t")


def test_a_wait_missing_its_predicate_is_refused():
    text = "Wait for the packet.\n<!-- WAIT: interval=60s bound=30 -->\n"
    with pytest.raises(sr.SeatRefusal, match="predicate"):
        sr.refuse_sleeping_poll(text, site="t")


def test_a_zero_interval_or_zero_bound_is_refused():
    for bad in ("interval=0s bound=30 predicate=x", "interval=60s bound=0 predicate=x"):
        with pytest.raises(sr.SeatRefusal):
            sr.refuse_sleeping_poll(f"Wait for x.\n<!-- WAIT: {bad} -->\n", site="t")


def test_quoted_ch8_doctrine_is_exempt_because_it_is_the_rule_not_an_instance():
    """Ch8's own text says "wait for message" -- a rendered boot quotes it and must still pass."""
    text = (
        "<!-- ch8:begin waits -->\n"
        '4. **WAITS.** Every "wait for message" has a 10-minute timeout.\n'
        "<!-- ch8:end waits -->\n"
    )
    assert sr.refuse_sleeping_poll(text, site="t") == 0


def test_one_unrelated_declaration_does_not_vouch_for_every_intention():
    """terra HIGH 2026-09-09: a per-DOCUMENT check lets one valid wait elsewhere in the file
    cover an intention-only one, and the refusal reports PASS while the seat can still stall."""
    text = (
        "Wait for the integrator, then continue.\n"
        + "\n" * 20
        + "## a different section\n"
        + _GOOD_WAIT
    )
    with pytest.raises(sr.SeatRefusal, match="no declaration within"):
        sr.refuse_sleeping_poll(text, site="t")


def test_a_declaration_beside_its_own_intention_passes():
    assert sr.refuse_sleeping_poll("Wait for the packet.\n" + _GOOD_WAIT, site="t") == 1


def test_two_intentions_and_one_declaration_refuses_the_uncovered_one():
    text = "Wait for A.\n" + _GOOD_WAIT + "\n" * 15 + "Wait for B, then continue.\n"
    with pytest.raises(sr.SeatRefusal, match=r"1 wait\(s\)"):
        sr.refuse_sleeping_poll(text, site="t")


def test_a_fenced_poll_loop_is_not_read_as_an_intention():
    text = "```powershell\nwhile ($i -lt 30) { # wait for the file\n  Start-Sleep 60\n}\n```\n"
    assert sr.refuse_sleeping_poll(text, site="t") == 0


# --- R2 -- the lane ceiling, at dispatcher step 0 ---------------------------------------------

def test_a_plan_naming_seven_lanes_is_refused_and_the_excess_is_named():
    lanes = [f"lane-{i}" for i in range(7)]
    with pytest.raises(sr.SeatRefusal, match="lane-ceiling") as exc:
        sr.refuse_lane_ceiling(lanes)
    assert "lane-6" in str(exc.value)
    assert "back to the plan" in str(exc.value)


def test_a_plan_at_the_ceiling_passes():
    lanes = [f"lane-{i}" for i in range(6)]
    assert sr.refuse_lane_ceiling(lanes) == lanes


def test_the_ceiling_is_read_from_the_existing_organ_not_retyped():
    """Library-first: ADR-110's number already lives in `boot_frontier.BATCH_WIDTH_MAX`."""
    assert sr.LANE_CEILING is boot_frontier.BATCH_WIDTH_MAX


def test_a_duplicate_lane_name_is_refused_because_the_plan_miscounts_its_own_width():
    with pytest.raises(sr.SeatRefusal, match="duplicate"):
        sr.refuse_lane_ceiling(["a", "b", "a"])


def test_checking_the_ceiling_after_provisioning_is_itself_refused():
    """"Run later the number is decorative" -- the placement IS the mechanism (Ch8)."""
    with pytest.raises(sr.SeatRefusal, match="checked LATE"):
        sr.refuse_lane_ceiling(["a", "b"], already_provisioned=["worktree-a"])


def test_a_step0_check_with_nothing_provisioned_is_the_sanctioned_call():
    assert sr.refuse_lane_ceiling(["a"], already_provisioned=[]) == ["a"]


# --- R6 -- the same-file collision, at dispatcher step 0 ([#675] target 3.4) -------------------
#
# THE TARGET, verbatim from `[#675]`'s Done-when:
#
#     (4) the dispatcher REFUSES to fire two lanes whose contracts touch the same file,
#     RED-first, as a refusal AT DISPATCH in the `scripts/seat_refusals.py` STEP-0 family
#     alongside `lane-ceiling` -- evaluated on the frozen contract set before the first worktree
#     exists, never as a warning afterwards, because run later the collision it exists to
#     prevent has already been paid for and every remaining option is a teardown
#
# WHY THIS IS A REFUSAL AND NOT A REPORT is the same argument `lane-ceiling` makes one rule over,
# and the row makes it explicitly: after provisioning, the collision has been PAID FOR. Two lanes
# editing one file produce a merge conflict the integrator resolves serially, or -- worse -- two
# lanes that each regenerate the same derived surface and hand back mutually-stale trees. Neither
# is recoverable by anything cheaper than a teardown, so the check that runs late is decorative.

_DONE = "## Done-contract (immutable)\n"


def _contract(*paths: str, extra: str = "") -> str:
    """A contract whose Done-contract section declares writes to `paths`."""
    body = "".join(f"- the lane edits `{p}` and lands it\n" for p in paths)
    return (f"# LANE lane-probe\n\n## Dispatch\n\nsomething\n\n{_DONE}\n{body}{extra}\n"
            f"## Steps\n\n1. do it **COMMIT**\n")


def test_two_lanes_declaring_the_same_file_are_REFUSED_and_both_are_named():
    """The clause itself. The refusal names the FILE and BOTH lanes, because a refusal that
    says only "there is a collision" cannot be acted on -- the dispatcher has to know which two
    contracts to re-cut."""
    contracts = {
        "lane-a": _contract("scripts/audit.py"),
        "lane-b": _contract("scripts/audit.py", "tests/test_audit.py"),
    }

    with pytest.raises(sr.SeatRefusal, match="file-collision") as exc:
        sr.refuse_file_collision(contracts)

    message = str(exc.value)
    assert "scripts/audit.py" in message
    assert "lane-a" in message and "lane-b" in message


def test_lanes_touching_DIFFERENT_files_pass_and_the_footprints_come_back():
    contracts = {
        "lane-a": _contract("scripts/audit.py"),
        "lane-b": _contract("tests/test_audit.py"),
    }

    footprints = sr.refuse_file_collision(contracts)

    assert footprints["lane-a"] == {"scripts/audit.py"}
    assert footprints["lane-b"] == {"tests/test_audit.py"}


def test_checking_collisions_AFTER_provisioning_is_itself_refused():
    """The row's own words: run later, "the collision it exists to prevent has already been paid
    for and every remaining option is a teardown". Same placement argument as `lane-ceiling`,
    and the same reason it is a separate leg rather than a note."""
    contracts = {"lane-a": _contract("scripts/audit.py"),
                 "lane-b": _contract("scripts/audit.py")}

    with pytest.raises(sr.SeatRefusal, match="checked LATE"):
        sr.refuse_file_collision(contracts, already_provisioned=["worktree-lane-a"])


def test_a_step0_call_with_nothing_provisioned_is_the_sanctioned_call():
    contracts = {"lane-a": _contract("scripts/audit.py")}

    assert sr.refuse_file_collision(contracts, already_provisioned=[]) == {
        "lane-a": {"scripts/audit.py"}}


def test_THREE_lanes_on_one_file_report_ALL_THREE_not_just_the_first_pair():
    """A refusal that stops at the first colliding pair sends the dispatcher back for a second
    round trip, and the second round is exactly the cost step 0 exists to avoid paying twice."""
    contracts = {name: _contract("deploy/manifest-v1.5.0.yaml")
                 for name in ("lane-a", "lane-b", "lane-c")}

    with pytest.raises(sr.SeatRefusal) as exc:
        sr.refuse_file_collision(contracts)

    message = str(exc.value)
    assert all(name in message for name in ("lane-a", "lane-b", "lane-c"))


def test_the_footprint_is_read_from_the_DONE_CONTRACT_not_the_whole_file():
    """MEASURED, not assumed, and this is the choice that makes the refusal usable.

    On the live batch-X set the Done-contract extraction found ONE colliding pair in 78 and NO
    path cited by three or more contracts -- that section is write-shaped. The whole file is not:
    it quotes carried rows, cites ADRs and names the organs it reasons about, so extracting from
    it would collide every lane against every other on shared references and the refusal would be
    turned off inside a window. A refusal that overstates its reach is worse than none, which is
    this module's own contract.
    """
    contract = _contract("scripts/audit.py") + (
        "\n## Carried rows and clauses (verbatim)\n\n"
        "the row cites `protocols/PLAYBOOK.md` and `scripts/gen_task_tree.py` as CONTEXT\n")

    assert sr.declared_footprint(contract) == {"scripts/audit.py"}


def test_a_path_cited_only_OUTSIDE_a_write_root_is_not_a_footprint_entry():
    """`H:/My Drive/...` and bare prose nouns are not repo paths, and a checker that counted
    them would refuse on the transport's own filename."""
    contract = _contract("scripts/audit.py",
                         extra="- see `LANE-x-000-other.md` on the transport\n")

    assert sr.declared_footprint(contract) == {"scripts/audit.py"}


# --- `[#743]`: A ROOT-LEVEL FILE IS A FILE -----------------------------------
#
# RED-FIRST WITNESS (ADR-108 SB). At `dbac84b8` a Done-contract declaring `ARCHITECTURE.md`,
# `.pre-commit-config.yaml` or `pyproject.toml` was invisible to this extractor, so two lanes
# could both declare the same root-level file and the step-0 refusal would report PASS.
#
# THE BLINDNESS HAD TWO INDEPENDENT LEGS, and either alone was enough:
#
#   * `_CONTRACT_PATH_RE` required `(?:...)+` -- ONE OR MORE segments ending in `/`. A bare
#     `ARCHITECTURE.md` produced no match at all.
#   * `_WRITE_ROOTS` was a tuple of DIRECTORY prefixes tested with `str.startswith`, so even a
#     matched root-level name had no admitting prefix.
#
# AND IT WAS LIVE IN THE BATCH THAT FIXED IT, which is why the row exists. The step-0 refusal
# this lane's own dispatcher ran reported "4 contract(s), 21 declared path(s), no file claimed
# twice" while `lane-x-628-docs-cut` declared `ARCHITECTURE.md` and
# `lane-x-664-delete-list-execution` declared `.pre-commit-config.yaml`. The two happened not
# to collide with each other, so the PASS was correct BY LUCK rather than by check.


def test_two_lanes_declaring_the_same_ROOT_LEVEL_file_are_REFUSED():
    """`[#743]`'s first leg, and the whole row in one assertion. RED at `dbac84b8`: the
    extractor saw neither declaration, found no collision, and passed."""
    contracts = {"lane-a": _contract("ARCHITECTURE.md"),
                 "lane-b": _contract("ARCHITECTURE.md", "scripts/audit.py")}

    with pytest.raises(sr.SeatRefusal) as exc:
        sr.refuse_file_collision(contracts)

    assert "ARCHITECTURE.md" in str(exc.value)
    assert "lane-a" in str(exc.value) and "lane-b" in str(exc.value)


@pytest.mark.parametrize("name", ["ARCHITECTURE.md", ".pre-commit-config.yaml",
                                  "pyproject.toml", "CLAUDE.md", "uv.lock", "package.json"])
def test_a_root_level_TRACKED_file_is_extracted_like_any_other_declared_path(name):
    """Every shape the root actually holds: an UPPERCASE living doc, a dotfile with an
    extension, and lowercase build config. A fix that admitted only `*.md` would leave the
    `.pre-commit-config.yaml` half of the measured live instance still blind."""
    assert sr.declared_footprint(_contract(name)) == {name}


@pytest.mark.parametrize("not_a_repo_path", [
    "LANE-x-000-other.md",          # the transport's own filename -- the false positive
    "LANE-x-675-instrument-fixes.md",
    "MATRIX.md",                    # a prose noun that happens to look like a file
    "REVIEW.md",
    "NIGHT-LOG.md",
])
def test_admitting_the_ROOT_does_not_admit_the_transport_or_a_prose_noun(not_a_repo_path):
    """`[#743]`'s explicit anti-regression clause: "a bare `*.md` admission that lets
    `LANE-x-000-other.md` through is a regression, not a fix, and a test asserts that too".

    The admission is a CLOSED SET -- the repo's own sanctioned top-level file roster -- not a
    glob, so the transport filenames and prose nouns this module's comment exists to exclude
    stay excluded BY CONSTRUCTION rather than by a second filter that could be dropped.
    """
    contract = _contract("scripts/audit.py", extra=f"- see `{not_a_repo_path}` on the transport\n")

    assert sr.declared_footprint(contract) == {"scripts/audit.py"}


def test_an_ABSOLUTE_operator_path_is_still_not_a_declared_footprint():
    """The other class `_WRITE_ROOTS`'s comment names. Widening to the root must not widen to
    the operator's disk: the basename of an absolute path is not a repo file."""
    contract = _contract("scripts/audit.py",
                         extra="- the contract lives at `H:/My Drive/CLAUDE PROMPT DIR/"
                               "LANE-x-000-other.md` and is read from there\n")

    assert sr.declared_footprint(contract) == {"scripts/audit.py"}


def test_the_root_admission_is_the_repo_s_OWN_roster_not_a_second_copy_of_it():
    """LIBRARY-FIRST, and it is the reason this fix adds no roster. `validate_hermetization`
    already computes the sanctioned top-level file set from the shape spec, and that set is
    what ADR-101 refuses new root files against. Retyping it here would create exactly the
    defect `_CONTRACT_PATH_RE`'s own comment names -- two organs disagreeing about what counts
    as a path -- and a root file added by a future ruling would be invisible to this check
    until someone remembered to copy it across.
    """
    import validate_hermetization as vh

    assert frozenset(vh.SANCTIONED_TIER1_FILES) == sr.ROOT_LEVEL_FILES


def test_a_row_body_QUOTED_INSIDE_the_done_contract_reads_as_a_declaration():
    """THE ONE FALSE POSITIVE THE WIDENING PRODUCES, measured and pinned rather than left to be
    rediscovered as flakiness.

    Run over all 57 contracts on the transport, the root admission produced FIVE multi-claimed
    root files and every single over-claim traced to ONE contract --
    `LANE-x-675-instrument-fixes`, the one that carries `[#743]`'s row body verbatim INSIDE its
    Done-contract, where the row text enumerates `ARCHITECTURE.md`, `.pre-commit-config.yaml`
    and `pyproject.toml` as EXAMPLES of what the checker should learn to see. Excluding that
    contract, the widening produces ZERO in-batch false collisions across the whole transport.

    THE CHECKER IS RIGHT AND THE CONTRACT IS MIS-SHAPED, which is why this is pinned as
    behaviour rather than patched. `declared_footprint` reads the Done-contract because that
    section is write-shaped; the sanctioned home for a carried row body is a SEPARATE section,
    which is exactly what the fixture in
    `test_the_footprint_is_read_from_the_DONE_CONTRACT_not_the_whole_file` uses. A contract that
    quotes filenames into its Done-contract has declared them, and the refusal's own remedy --
    re-cut the contract -- is the right answer to that.
    """
    quoting = _contract("scripts/audit.py",
                        extra="- carried verbatim: *\"a contract declaring a root-level file "
                              "(`ARCHITECTURE.md`, `pyproject.toml`) is extracted\"*\n")

    assert sr.declared_footprint(quoting) == {"scripts/audit.py", "ARCHITECTURE.md",
                                              "pyproject.toml"}

    # The same words in the sanctioned place declare nothing.
    carried_properly = _contract("scripts/audit.py") + (
        "\n## Carried rows and clauses (verbatim)\n\n"
        "*\"a contract declaring a root-level file (`ARCHITECTURE.md`, `pyproject.toml`) is "
        "extracted\"*\n")

    assert sr.declared_footprint(carried_properly) == {"scripts/audit.py"}


def test_a_root_file_declared_in_PROSE_outside_the_done_contract_is_still_not_a_footprint():
    """The Done-contract-only rule is unchanged by this widening. It is the measured choice
    that makes the refusal usable at all, and the root admission must not quietly undo it --
    every contract in this repo cites `pyproject.toml` and `CLAUDE.md` somewhere."""
    contract = _contract("scripts/audit.py") + (
        "\n## Carried rows and clauses (verbatim)\n\n"
        "the row cites `ARCHITECTURE.md` and `pyproject.toml` as CONTEXT, not as writes\n")

    assert sr.declared_footprint(contract) == {"scripts/audit.py"}


def test_a_contract_declaring_NO_footprint_is_REPORTED_not_silently_passed():
    """NEVER GREEN-BY-SKIP -- the 2026-08-25 sweep's rule, applied to a different absence.

    A contract whose Done-contract names no repo path cannot collide with anything, and a
    checker that returned a clean pass would report the same word for "no collision" and for "I
    could not see this lane at all". The dispatcher is told which lanes were invisible to it.
    """
    contracts = {"lane-a": _contract("scripts/audit.py"),
                 "lane-silent": "# LANE\n\n## Done-contract (immutable)\n\nprose only\n"}

    footprints = sr.refuse_file_collision(contracts)

    assert footprints["lane-silent"] == set()
    assert "lane-silent" in sr.undeclared_lanes(footprints)


def test_the_refusal_is_wired_into_the_DISPATCHER_seat_at_STEP_0():
    """Roster membership, and the ORDER inside it. `lane-ceiling` opens step 0 and
    `dryrun-step0` closes it (AMEND-BATCH-V-002 §1 makes the DryRun the last line), so the
    collision check sits between them: after the width is known, before anything is launched."""
    assert "file-collision" in sr.REFUSALS

    dispatcher = sr.SEAT_REFUSALS["dispatcher"]
    assert "file-collision" in dispatcher
    assert dispatcher.index("lane-ceiling") < dispatcher.index("file-collision")
    assert dispatcher.index("file-collision") < dispatcher.index("dryrun-step0")


def test_the_refusal_is_DISPATCHER_ONLY_because_only_the_dispatcher_fires_lanes():
    """A lane cannot commit this failure: by the time a lane boots, it has been fired."""
    for seat, refusals in sr.SEAT_REFUSALS.items():
        if seat != "dispatcher":
            assert "file-collision" not in refusals, seat


def test_the_LIVE_batch_x_contract_set_is_carried_as_a_regression_fixture():
    """The measurement that justified the design, frozen as a test.

    Two lanes for row `[#734]` -- `retire-stage` and `retire-stage-2` -- both declare writes to
    `deploy/manifest-v1.5.0.yaml`. That is a REAL collision in a REAL batch, found by running
    this extraction over the frozen set, and it is the evidence that the refusal catches
    something rather than merely being satisfiable.
    """
    contracts = {
        "lane-x-734-retire-stage": _contract("deploy/manifest-v1.5.0.yaml",
                                             "scripts/validate_hermetization.py"),
        "lane-x-734-retire-stage-2": _contract("deploy/manifest-v1.5.0.yaml"),
        "lane-x-675-merge-cost": _contract("scripts/merge_receipt.py"),
    }

    with pytest.raises(sr.SeatRefusal) as exc:
        sr.refuse_file_collision(contracts)

    assert "deploy/manifest-v1.5.0.yaml" in str(exc.value)
    assert "lane-x-675-merge-cost" not in str(exc.value), "an uninvolved lane is not named"


def test_a_SUPERSEDED_contract_left_on_the_transport_collides_with_its_own_replacement():
    """The usage trap, frozen as a test because it is a FALSE positive and those are what turn a
    refusal off.

    MEASURED 2026-09-12 on the live transport: globbing `LANE-x-*.md` returns 13 contracts, of
    which `LANE-x-734-retire-stage` and `LANE-x-734-retire-stage-2` both declare
    `deploy/manifest-v1.5.0.yaml` -- and `git worktree list` shows only the SECOND provisioned.
    The first is a superseded re-cut nobody deleted. So the collision is real in the DIRECTORY
    and absent from the BATCH, and a dispatcher that fed this refusal a glob would be refused
    for a lane it was never going to fire.

    The remedy is upstream and already exists: `[#630]`'s
    `batch_manifest.freeze_manifest_contract_agreement` refuses when the manifest's lane slugs
    and the contract set disagree. This test asserts the SHAPE of the trap so that the composed
    order stays deliberate -- it is not a claim that this refusal can detect supersession, which
    it cannot and should not try to.
    """
    superseded = _contract("deploy/manifest-v1.5.0.yaml")
    replacement = _contract("deploy/manifest-v1.5.0.yaml")

    with pytest.raises(sr.SeatRefusal):
        sr.refuse_file_collision({"lane-734-retire-stage": superseded,
                                  "lane-734-retire-stage-2": replacement})

    # Fed the set the manifest actually declares, the same pair passes.
    assert sr.refuse_file_collision({"lane-734-retire-stage-2": replacement}) == {
        "lane-734-retire-stage-2": {"deploy/manifest-v1.5.0.yaml"}}


def test_the_remedy_names_a_way_forward_rather_than_only_the_problem():
    """`SeatRefusal`'s own contract: "a refusal that names no way forward gets worked around
    rather than fixed"."""
    contracts = {"a": _contract("scripts/audit.py"), "b": _contract("scripts/audit.py")}

    with pytest.raises(sr.SeatRefusal) as exc:
        sr.refuse_file_collision(contracts)

    remedy = exc.value.remedy
    assert "sequence" in remedy.lower() or "re-cut" in remedy.lower()


# --- R3 -- the reviewer's model id in the tally ------------------------------------------------

_TALLY = "Tally: review=lane-v-000 reviewer=gpt-5.6-terra findings=3 fixed=3"


def test_a_matching_reviewer_passes_and_the_exact_id_is_returned():
    parsed = sr.refuse_tally_reviewer(_TALLY, contracted_reviewer="gpt-5.6-terra")
    assert parsed.reviewer == "gpt-5.6-terra"
    assert parsed.findings == 3 and parsed.fixed == 3


def test_a_substituted_reviewer_that_does_not_report_NONE_is_refused():
    line = "Tally: review=lane-v-000 reviewer=gpt-5.6-sol findings=3 fixed=3"
    with pytest.raises(sr.SeatRefusal, match="reviewer-mismatch"):
        sr.refuse_tally_reviewer(line, contracted_reviewer="gpt-5.6-terra")


def test_a_bare_family_id_is_a_mismatch_not_a_near_miss():
    line = "Tally: review=lane-v-000 reviewer=gpt-5.6 findings=3 fixed=3"
    with pytest.raises(sr.SeatRefusal, match="reviewer-mismatch"):
        sr.refuse_tally_reviewer(line, contracted_reviewer="gpt-5.6-terra")


def test_a_substituted_reviewer_reporting_review_NONE_is_the_honest_form_and_passes():
    line = "Tally: review=NONE reviewer=gpt-5.6-sol findings=0 fixed=0"
    assert sr.refuse_tally_reviewer(line, contracted_reviewer="gpt-5.6-terra").review == "NONE"


def test_a_tally_with_no_reviewer_field_is_refused():
    line = "Tally: review=lane-v-000 findings=3 fixed=3"
    with pytest.raises(sr.SeatRefusal, match="reviewer-absent"):
        sr.refuse_tally_reviewer(line, contracted_reviewer="gpt-5.6-terra")


def test_a_malformed_tally_line_is_refused_rather_than_partially_parsed():
    with pytest.raises(sr.SeatRefusal, match="tally-malformed"):
        sr.refuse_tally_reviewer("reviewed by terra, 3 findings",
                                 contracted_reviewer="gpt-5.6-terra")


def test_review_SELF_still_carries_the_seats_own_model_id():
    line = "Tally: review=SELF reviewer=claude-opus-5 findings=1 fixed=1"
    assert sr.refuse_tally_reviewer(line, contracted_reviewer="claude-opus-5").review == "SELF"
    with pytest.raises(sr.SeatRefusal, match="reviewer-absent"):
        sr.refuse_tally_reviewer("Tally: review=SELF findings=1 fixed=1",
                                 contracted_reviewer="claude-opus-5")


# --- R4 -- carried-by: on DECLARE- / AMEND- / BATCH- WRITES ------------------------------------

_CARRIED = "# DECLARE-X\ncarried-by: docs/audits/2026-09-08-technical-batch-v-manifest.md\n\nbody\n"


def test_a_decision_file_with_no_carrier_is_refused_at_write_time():
    with pytest.raises(sr.SeatRefusal, match="carried-by-absent"):
        sr.refuse_uncarried_decision_write("DECLARE-X.md", "# DECLARE-X\n\nbody\n")


def test_a_carried_decision_file_passes():
    assert sr.refuse_uncarried_decision_write("DECLARE-X.md", _CARRIED) is True


def test_an_indented_carried_by_is_refused_because_the_probe_anchors_flush_left():
    text = "# DECLARE-X\n  carried-by: docs/x.md\n\nbody\n"
    with pytest.raises(sr.SeatRefusal, match="carried-by-absent"):
        sr.refuse_uncarried_decision_write("DECLARE-X.md", text)


def test_a_carried_by_below_the_head_window_is_refused():
    text = "# DECLARE-X\n" + "\n" * 10 + "carried-by: docs/x.md\n"
    with pytest.raises(sr.SeatRefusal, match="carried-by-absent"):
        sr.refuse_uncarried_decision_write("DECLARE-X.md", text)


def test_an_empty_carrier_value_is_refused():
    with pytest.raises(sr.SeatRefusal, match="carried-by-empty"):
        sr.refuse_uncarried_decision_write("AMEND-BATCH-V-003.md", "carried-by:   \n\nbody\n")


def test_the_literal_OPEN_is_a_lawful_value():
    text = "carried-by: OPEN -- no home written yet; named in the bundle residual\n\nbody\n"
    assert sr.refuse_uncarried_decision_write("BATCH-2026-09-09-W-CONTRACTS.md", text) is True


@pytest.mark.parametrize("value", ["OPENING soon", "OPEN-not-a-carrier", "OPENED by filings"])
def test_a_value_that_merely_STARTS_with_OPEN_is_refused(value):
    """terra HIGH 2026-09-09: `startswith("OPEN")` admits three things the probe does not."""
    with pytest.raises(sr.SeatRefusal, match="carried-by-unresolvable"):
        sr.refuse_uncarried_decision_write("DECLARE-X.md", f"carried-by: {value}\n\nbody\n")


@pytest.mark.parametrize("value", ["OPEN", "OPEN -- named in the residual"])
def test_the_literal_OPEN_alone_or_with_a_reason_is_lawful(value):
    assert sr.refuse_uncarried_decision_write(
        "DECLARE-X.md", f"carried-by: {value}\n\nbody\n") is True


def test_a_value_that_is_neither_OPEN_nor_a_path_is_refused():
    text = "carried-by: the manifest, probably\n\nbody\n"
    with pytest.raises(sr.SeatRefusal, match="carried-by-unresolvable"):
        sr.refuse_uncarried_decision_write("DECLARE-X.md", text)


def test_a_file_outside_the_three_prefixes_is_not_governed():
    assert sr.refuse_uncarried_decision_write("STATUS-integrator.md", "no carrier\n") is False


def test_write_decision_file_refuses_BEFORE_it_writes(tmp_path):
    """A write-time refusal that writes first and complains after has refused nothing."""
    target = tmp_path / "DECLARE-Y.md"
    with pytest.raises(sr.SeatRefusal, match="carried-by-absent"):
        sr.write_decision_file(target, "# DECLARE-Y\n\nbody\n")
    assert not target.exists()
    sr.write_decision_file(target, _CARRIED)
    assert target.read_text(encoding="utf-8") == _CARRIED


# --- R5 -- the -DryRun line is the LAST line of dispatcher step 0 (AMEND-BATCH-V-002 s1) -------

_STEP0 = (
    "## Step 0\n\n"
    "Freeze the plan, then DryRun every generated contract -- LAST LINE of step 0:\n\n"
    "```\n"
    "dispatch LANE-a.md -DryRun\n"
    "dispatch LANE-b.md -DryRun\n"
    "```\n"
)


def test_a_step0_that_dryruns_every_contract_last_passes():
    assert sr.refuse_dispatcher_step0_without_dryrun(
        _STEP0, contracts=["LANE-a.md", "LANE-b.md"]) == 2


def test_a_step0_with_no_dryrun_at_all_is_refused():
    with pytest.raises(sr.SeatRefusal, match="dryrun-absent"):
        sr.refuse_dispatcher_step0_without_dryrun(
            "## Step 0\n\nFreeze the plan.\n", contracts=["LANE-a.md"])


def test_a_dryrun_that_is_not_the_last_line_of_step0_is_refused():
    text = _STEP0 + "\nThen provision the worktrees.\n"
    with pytest.raises(sr.SeatRefusal, match="dryrun-not-last"):
        sr.refuse_dispatcher_step0_without_dryrun(text, contracts=["LANE-a.md", "LANE-b.md"])


def test_a_contract_left_out_of_the_dryrun_is_refused_and_named():
    with pytest.raises(sr.SeatRefusal, match="dryrun-incomplete") as exc:
        sr.refuse_dispatcher_step0_without_dryrun(
            _STEP0, contracts=["LANE-a.md", "LANE-b.md", "LANE-c.md"])
    assert "LANE-c.md" in str(exc.value)


def test_zero_contracts_is_refused_because_a_batch_with_no_contract_dryruns_nothing():
    with pytest.raises(sr.SeatRefusal, match="dryrun-no-contracts"):
        sr.refuse_dispatcher_step0_without_dryrun(_STEP0, contracts=[])


# --- step-0 ISOLATION (terra HIGH 2026-09-09) ---------------------------------------------------

_LATER = "\n## Step 1\n\nThen provision the worktrees.\n"


def test_a_correct_step0_passes_even_when_the_file_continues_past_it():
    """The rendered boot says `--step0 <this file>`, and that file has six more sections."""
    assert sr.refuse_dispatcher_step0_without_dryrun(
        _STEP0 + _LATER, contracts=["LANE-a.md", "LANE-b.md"]) == 2


def test_a_dryrun_in_a_LATER_section_does_not_mask_a_step0_that_has_none():
    """The dangerous direction: a checker reading the whole file passes a bare step 0."""
    text = "## Step 0\n\nFreeze the plan.\n\n## Step 1\n\n```\ndispatch LANE-a.md -DryRun\n```\n"
    with pytest.raises(sr.SeatRefusal, match="dryrun-absent"):
        sr.refuse_dispatcher_step0_without_dryrun(text, contracts=["LANE-a.md"])


def test_text_with_no_step0_heading_is_treated_whole():
    assert sr.isolate_step0("no headings here\n") == "no headings here\n"
    assert sr.isolate_step0(_STEP0 + _LATER).strip().endswith("```")


def test_the_step0_heading_is_matched_at_any_depth_and_with_decoration():
    decorated = _STEP0.replace("## Step 0", "### 2 - STEP 0 - the refusals")
    assert sr.refuse_dispatcher_step0_without_dryrun(
        decorated + _LATER, contracts=["LANE-a.md", "LANE-b.md"]) == 2


# --- the refusal type itself -------------------------------------------------------------------

def test_every_refusal_names_itself_and_carries_a_remedy():
    with pytest.raises(sr.SeatRefusal) as exc:
        sr.refuse_lane_ceiling([f"l{i}" for i in range(9)])
    message = str(exc.value)
    assert message.startswith("REFUSED [lane-ceiling]")
    assert "->" in message or "--" in message


def test_the_refusal_registry_lists_every_refusal_in_declaration_order():
    """Five from batches T/U, `file-collision` from `[#675]` target 3.4, and `unruled-merge`
    from lane `aa-2`'s integrator plan/execute split.

    The roster is asserted WHOLE and in order rather than by membership: a seat template cites
    these ids, so a silent addition or reorder changes what a rendered boot runs. Widening it is
    therefore an edit a reviewer sees, which is the point -- a membership assertion, or a
    `len(...) <= N` bound, would both be satisfied by swapping one id for another.
    """
    assert sr.REFUSALS == (
        "sleeping-poll", "lane-ceiling", "reviewer-mismatch", "carried-by", "dryrun-step0",
        "file-collision", "unruled-merge",
        # [#833]: the two STEP-0 refusals over the seat registry.
        "no-live-integrator", "lane-owned",
    )


def test_every_seat_runs_at_least_one_refusal_and_names_only_real_ones():
    assert set(sr.SEAT_REFUSALS) == set(seat_ch8.SEATS)
    for seat, names in sr.SEAT_REFUSALS.items():
        assert names, f"seat {seat!r} runs no refusal"
        assert set(names) <= set(sr.REFUSALS), f"seat {seat!r} names an unknown refusal"


def test_every_refusal_has_at_least_one_seat_that_runs_it():
    """A refusal nobody runs is a module nobody imports wearing an enforcement label."""
    run = {name for names in sr.SEAT_REFUSALS.values() for name in names}
    assert set(sr.REFUSALS) - run == set()


# --- the CLI: the refusals are RUNNABLE, which is what a seat template can carry ---------------

def _run(*args: str):
    return CliRunner().invoke(sr.cli, list(args))


def test_cli_lists_the_roster():
    result = _run("list")
    assert result.exit_code == 0
    assert result.output.split() == list(sr.REFUSALS)


def test_cli_exits_1_on_a_refusal_and_0_on_a_pass():
    over = [arg for lane in range(9) for arg in ("--lane", f"l{lane}")]
    refused = _run("lane-ceiling", *over)
    assert refused.exit_code == 1
    assert "REFUSED [lane-ceiling]" in refused.output

    ok = _run("lane-ceiling", "--lane", "a", "--lane", "b")
    assert ok.exit_code == 0 and "PASS" in ok.output


def test_cli_late_check_is_refused_through_the_provisioned_flag():
    result = _run("lane-ceiling", "--lane", "a", "--provisioned", ".claude/worktrees/a")
    assert result.exit_code == 1 and "checked LATE" in result.output


def test_cli_carried_by_reads_files(tmp_path):
    good = tmp_path / "DECLARE-Ok.md"
    good.write_text(_CARRIED, encoding="utf-8")
    bad = tmp_path / "AMEND-Bad.md"
    bad.write_text("# AMEND-Bad\n\nbody\n", encoding="utf-8")
    assert _run("carried-by", str(good)).exit_code == 0
    assert _run("carried-by", str(bad)).exit_code == 1


def test_cli_reviewer_reads_the_tally_out_of_an_artifact(tmp_path):
    art = tmp_path / "REVIEW.md"
    art.write_text(f"# review\n\n{_TALLY}\n", encoding="utf-8")
    assert _run("reviewer", "--contracted", "gpt-5.6-terra", str(art)).exit_code == 0
    assert _run("reviewer", "--contracted", "gpt-5.6-sol", str(art)).exit_code == 1


def test_cli_sleeping_poll_and_dryrun_read_files(tmp_path):
    waiting = tmp_path / "boot.md"
    waiting.write_text("Wait for the integrator, then continue.\n", encoding="utf-8")
    assert _run("sleeping-poll", str(waiting)).exit_code == 1

    step0 = tmp_path / "step0.md"
    step0.write_text(_STEP0, encoding="utf-8")
    assert _run("dryrun-step0", "--step0", str(step0),
                "--contract", "LANE-a.md", "--contract", "LANE-b.md").exit_code == 0
    assert _run("dryrun-step0", "--step0", str(step0), "--contract", "LANE-z.md").exit_code == 1


# --- 8/9 -- a batch with no live integrator, and a lane that already has a live owner ([#833]) ----
#
# Both are STEP-0 refusals over the seat registry, and both exist because the absence cost hours
# this week: a half-day with no integrator because nobody booted one, and -- on lane ab-833 itself,
# 2026-09-17 -- a second session dispatched onto a lane whose owner was live, found only by reading
# staged files and a process scan. Each has a trip-test AND a passing path, so neither can satisfy
# its trip-test by refusing everything.

import importlib  # noqa: E402
from datetime import datetime, timedelta, UTC  # noqa: E402

_T0 = datetime(2026, 9, 17, 10, 47, tzinfo=UTC)
_LANE_CWD = "C:/Dev/.dev-knowledge/.claude/worktrees/lane-ab-833-seat-registry"


def _registry(tmp_path, *events, binds=()):
    seat_registry = importlib.import_module("seat_registry")
    path = tmp_path / "seats.jsonl"
    for event, session, minutes, cwd in events:
        seat_registry.record_event({"hook_event_name": event, "session_id": session, "cwd": cwd},
                                   path=path, now=_T0 + timedelta(minutes=minutes),
                                   env={"CLAUDE_PID": "4242"})
    for role, batch, session in binds:
        seat_registry.bind(role, batch, session_id=session, path=path, now=_T0)
    return path


def _read(path, *, minutes=1):
    seat_registry = importlib.import_module("seat_registry")
    return seat_registry.seats(path, now=_T0 + timedelta(minutes=minutes),
                               pid_alive=lambda _p: True, path_exists=lambda _p: True,
                               transcript_mtime=lambda _p: None)


def test_a_lane_into_a_batch_with_no_integrator_seat_is_refused_naming_the_role(tmp_path):
    path = _registry(tmp_path)
    with pytest.raises(sr.SeatRefusal, match="no-live-integrator") as exc:
        sr.refuse_no_live_integrator("AB", _read(path))
    assert "integrator" in exc.value.detail and "AB" in exc.value.detail


def test_a_wedged_integrator_does_not_count_as_a_receiving_seat(tmp_path):
    path = _registry(tmp_path, ("SessionStart", "int-1", 0, "C:/Dev/hub"),
                     binds=[("integrator", "AB", "int-1")])
    stale = _read(path, minutes=importlib.import_module("seat_registry").WEDGED_AFTER_MIN + 5)
    with pytest.raises(sr.SeatRefusal, match="no-live-integrator") as exc:
        sr.refuse_no_live_integrator("AB", stale)
    assert "wedged" in exc.value.detail


def test_an_integrator_of_another_batch_does_not_count(tmp_path):
    path = _registry(tmp_path, ("SessionStart", "int-1", 0, "C:/Dev/hub"),
                     binds=[("integrator", "AA", "int-1")])
    with pytest.raises(sr.SeatRefusal, match="no-live-integrator"):
        sr.refuse_no_live_integrator("AB", _read(path))


def test_a_live_integrator_for_the_batch_admits_the_lane(tmp_path):
    path = _registry(tmp_path, ("SessionStart", "int-1", 0, "C:/Dev/hub"),
                     binds=[("integrator", "ab", "int-1")])
    assert sr.refuse_no_live_integrator("AB", _read(path)).session_id == "int-1"


def test_a_second_session_onto_a_lane_with_a_live_owner_is_refused(tmp_path):
    """The 2026-09-17 witness: owner 52a3764d live, duplicate 506ef5c0 dispatched at 11:12."""
    path = _registry(tmp_path, ("SessionStart", "52a3764d", 0, _LANE_CWD))
    with pytest.raises(sr.SeatRefusal, match="lane-owned") as exc:
        sr.refuse_lane_owned("lane-ab-833-seat-registry", _read(path, minutes=25),
                             own_session="506ef5c0")
    assert "52a3764d" in exc.value.detail


def test_the_owner_itself_is_not_refused_by_its_own_seat(tmp_path):
    path = _registry(tmp_path, ("SessionStart", "52a3764d", 0, _LANE_CWD))
    assert sr.refuse_lane_owned("lane-ab-833-seat-registry", _read(path),
                                own_session="52a3764d") is None


def test_a_relaunch_over_a_wedged_owner_is_admitted(tmp_path):
    """The 12 h 43 min SessionStart wedge: relaunching over a dead-in-place seat is the remedy."""
    path = _registry(tmp_path, ("SessionStart", "old-seat", 0, _LANE_CWD))
    stale = _read(path, minutes=importlib.import_module("seat_registry").WEDGED_AFTER_MIN + 5)
    assert sr.refuse_lane_owned("lane-ab-833-seat-registry", stale, own_session="new") is None


def test_an_owner_of_a_different_lane_does_not_refuse(tmp_path):
    path = _registry(tmp_path, ("SessionStart", "52a3764d", 0, _LANE_CWD))
    assert sr.refuse_lane_owned("lane-ab-834-protocols-heading-gate", _read(path),
                                own_session="new") is None
