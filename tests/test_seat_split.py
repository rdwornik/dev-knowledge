"""The integrator seat's PLAN/EXECUTE split, RED-first (lane `aa-2`). Implements `[#737]`.

`[#737]`'s last open done-when clause asks for *"the dispatcher and integrator seats observed
booting at `sonnet` and `opusplan` respectively, which is the only evidence that the ruling took
effect rather than merely being recorded."* This file is what makes that observable, and it
records that the observation came back NEGATIVE. The row is not closed here.


WHAT WAS ALREADY TRUE, AND WHY IT BOUGHT NOTHING. Operator ruling AX22-3 (2026-09-11) routed the
integrator seat to `opusplan` — "judges merge verdicts on Opus while running suites and teardowns
on Sonnet, which is what `opusplan` is" — and `gen_seat_boot.SEAT_MODELS` has carried that value
since. Batch Z then ran, and its close packet measured the integrator seat at **USD 82.53, 100%
`claude-opus-5`, 30.5% of a USD 270.72 night**. The declared split did not happen.

TWO INDEPENDENT REASONS IT COULD NOT HAVE, and a test here for each:

  1. **The value reached no flag.** `SEAT_MODELS` is rendered into a `<!-- GENERATED … -->`
     COMMENT. The launch command the integrator's boot actually carries is Ch8 dispatch row 3,
     which is the bare word `claude` — no `--model`, no `--effort`, no `--permission-mode`. That
     is `[#717]`'s defect ("the launch line omits the model, so a contract declaring sonnet
     dispatches at opus") one surface over: `[#717]` fixed the LANE CONTRACT generator's line,
     and the SEAT boot's line was never in its scope. A declared tier that reaches no argument is
     a decision the tree records and does not make.

  2. **`opusplan` keys on the wrong thing, and at this seat's context size it LOSES money.**
     `opusplan` is Opus while the session is in plan MODE and Sonnet after. The integrator's
     halves are not plan-mode and not-plan-mode; they are *judgment* and *mechanics*, which
     interleave many times per merge. And the prompt cache is per-model — MEASURED on six mixed-
     model transcripts on this host, where the turn following a model switch carries a
     cache-write of 29,751–379,585 tokens against a same-session median of 614–1,759, a 48x to
     391x jump, while its cache-read collapses to the small shared prefix. At the integrator's
     own measured mean context (232,875 tokens/call) one switch into Opus costs USD 1.46 and one
     into Sonnet USD 0.58, against a saving of USD 0.0812 per turn moved. **A per-turn split
     needs 25 consecutive cheap turns to repay one round trip**, and a merge walk does not have
     them between judgments.

SO THE BOUNDARY IS COARSE AND IT IS A FILE. Two SESSIONS, not two modes: each holds its own
context on its own model, permanently cached, and an escalation is a message between two live
sessions rather than a model switch that re-caches 232,875 tokens. Ch8 point 6 already rules
STATE IS FILES; this applies it to the seam inside one seat.

WHAT THESE TESTS REFUSE:
  1. A split that lives in a comment and reaches no flag.
  2. A launch line that drops a dispatch constant — `[#717]`'s defect, rebuilt at the seat.
  3. A boundary with no escalation path, or one the cheap half cannot take.
  4. A split whose two halves are not separately routed.
"""
from __future__ import annotations

import re

import pytest

import dispatch_surface as ds
import gen_lane_contract as glc
import gen_seat_boot as gsb
import seat_ch8
import seat_refusals as sr

BATCH, DATE = "AA", "2026-09-15"


@pytest.fixture()
def integrator(tmp_path):
    gsb.write_bundle(tmp_path, batch=BATCH, date=DATE)
    return (tmp_path / gsb.out_name("integrator")).read_text(encoding="utf-8")


# --- REFUSAL 4: the two halves are separately routed --------------------------------------

def test_the_integrator_declares_TWO_phases_and_they_run_on_DIFFERENT_models():
    """The split, at its declaration. Two phases on one model is a split in name only."""
    phases = gsb.SEAT_PHASES["integrator"]
    assert len(phases) == 2
    assert [p.name for p in phases] == ["plan", "execute"]
    assert phases[0].model != phases[1].model
    assert (phases[0].model, phases[1].model) == ("opus", "sonnet")


def test_every_seat_declares_at_least_one_phase_so_a_new_seat_cannot_default_one():
    """`SEAT_MODELS`'s own posture, carried to the phase map: a seat added to the enum without a
    declared tier must FAIL a test rather than render an unresolved one."""
    assert set(gsb.SEAT_PHASES) == set(seat_ch8.SEATS)
    for seat in seat_ch8.SEATS:
        assert gsb.SEAT_PHASES[seat], f"{seat} declares no phase"


def test_SEAT_MODELS_is_DERIVED_from_the_phases_and_is_not_a_second_declaration():
    """ONE declaration, not two. A seat's tier stated in two places is two things to keep true,
    and the drift is invisible: a header saying `opusplan` over a boot that launches `opus` reads
    exactly like one that agrees."""
    for seat, phases in gsb.SEAT_PHASES.items():
        assert gsb.SEAT_MODELS[seat] == phases[0].model


def test_every_declared_phase_uses_only_the_ruled_vocabulary():
    """READ, never restated. The four enums live in `gen_lane_contract`, which owns them because
    it bakes them into a contract; a fifth copy here is the defect register section V was ruled
    on. A phase naming a model outside the enum would render a launch line the CLI refuses."""
    for seat, phases in gsb.SEAT_PHASES.items():
        for phase in phases:
            assert phase.model in glc.MODEL_ENUM, f"{seat}/{phase.name}: model"
            assert phase.mode in glc.MODE_ENUM, f"{seat}/{phase.name}: mode"
            assert phase.effort in glc.EFFORT_ENUM, f"{seat}/{phase.name}: effort"


def test_opusplan_is_NOT_the_carrier_of_this_split_and_the_reason_is_recorded():
    """AX22-3's INTENT is kept and its named MECHANISM is replaced, on measured evidence.

    The ruling's substance — judgment on Opus, mechanics on Sonnet — is exactly what
    `SEAT_PHASES` now encodes. `opusplan` was the ruling's stated *means*, and it keys on plan
    MODE rather than on the work, so it cannot express this boundary; at this seat's context it
    also costs more than it saves. A ruling binds its merits, not its quoted token.
    """
    assert gsb.SEAT_MODELS["integrator"] != "opusplan"
    assert {p.model for p in gsb.SEAT_PHASES["integrator"]} == {"opus", "sonnet"}
    assert "opusplan" in gsb.SPLIT_RATIONALE
    assert "AX22-3" in gsb.SPLIT_RATIONALE


# --- REFUSAL 1 + 2: the split reaches a FLAG, and no constant is dropped -------------------

def test_the_boot_carries_a_RESOLVED_launch_line_per_phase(integrator):
    """`[#717]` at the seat. A boot whose launch line is the bare word `claude` dispatches the
    seat at whatever the operator's default happens to be — which on batch Z was Opus for 100% of
    a USD 82.53 sitting whose own header said `opusplan`."""
    for phase in gsb.SEAT_PHASES["integrator"]:
        launch = ds.resolve_launch(model=phase.model, mode=phase.mode, effort=phase.effort,
                                   shape="interactive", slug="integrator")
        assert launch.ok, launch.refusals
        assert launch.render() in integrator, f"{phase.name}: {launch.render()!r} absent"


def test_no_phase_launch_line_DROPS_A_DISPATCH_CONSTANT(integrator):
    """Section V's measured defect — roughly thirty consecutive seats launched at a tier nobody
    chose because a line silently omitted `--model`. Every constant is emitted by name."""
    for phase in gsb.SEAT_PHASES["integrator"]:
        launch = ds.resolve_launch(model=phase.model, mode=phase.mode, effort=phase.effort,
                                   shape="interactive", slug="integrator")
        for flag in ("--model", "--effort", "--permission-mode"):
            assert flag in launch.flags, f"{phase.name} drops {flag}"
        assert launch.render() in integrator


def test_the_PLAN_half_cannot_merge_and_that_is_the_permission_mode_not_a_promise(integrator):
    """A safety property the split buys for free, and it is worth asserting because it is the
    half of `plan` mode nobody asked for: the judging half runs under `--permission-mode plan`,
    so the seat that RULES on a merge is mechanically incapable of performing one. The split is
    therefore not only cheaper, it is harder to get wrong in the expensive direction."""
    plan = gsb.SEAT_PHASES["integrator"][0]
    assert plan.mode == "plan"
    assert ds.MODE_PERMISSION_MODE[plan.mode] == "plan"
    assert "--permission-mode plan" in integrator


def test_every_SELF_LAUNCHING_seat_carries_its_own_resolved_line(tmp_path):
    """No attended seat is left on a bare `claude`. The bare-launch defect is identical for all
    four, and fixing one while leaving three armed would leave the cost defect live everywhere
    but the seat this lane happens to name."""
    gsb.write_bundle(tmp_path, batch=BATCH, date=DATE)
    checked = 0
    for seat in seat_ch8.SEATS:
        text = (tmp_path / gsb.out_name(seat)).read_text(encoding="utf-8")
        for phase in gsb.SEAT_PHASES[seat]:
            if not phase.self_launched:
                continue
            launch = ds.resolve_launch(model=phase.model, mode=phase.mode, effort=phase.effort,
                                       shape="interactive", slug=seat)
            assert launch.ok, launch.refusals
            assert launch.render() in text, f"{seat}/{phase.name}"
            checked += 1
    assert checked == 5, "four attended seats, and the integrator counts twice"


def test_the_LANE_seat_carries_NO_launch_line_because_it_does_not_launch_itself(tmp_path):
    """The one seat another seat starts, and the reason this is not an oversight.

    A lane is dispatched `--bg` BY THE DISPATCHER. A launch line in a lane's own boot would be a
    command that seat can never run, and the `--bg --worktree` form it would have to carry is
    exactly the rival literal launch form register section V was ruled on
    (`dispatch_surface._RIVAL_FORMS`) -- the defect where four rival commands existed for one act.
    The tier is still DECLARED, so the header records it and `SEAT_MODELS` derives from it; the
    boot points at the contract's own routing row instead of restating a command.
    """
    gsb.write_bundle(tmp_path, batch=BATCH, date=DATE)
    text = (tmp_path / gsb.out_name("lane")).read_text(encoding="utf-8")
    assert [p.self_launched for p in gsb.SEAT_PHASES["lane"]] == [False]
    assert "does NOT launch itself" in text
    assert "model: opus |" in text, "the tier is still recorded"
    for fenced in re.findall(r"^```[^\n]*\n(.*?)^```", text, re.DOTALL | re.MULTILINE):
        for line in fenced.splitlines():
            for rx, why in ds._RIVAL_FORMS:
                assert not rx.search(line.strip()), f"rival launch form in the lane boot: {why}"


def test_a_phase_whose_launch_REFUSES_refuses_the_whole_render(monkeypatch, tmp_path):
    """A boot carrying a partial command is worse than one that was never written: a seat copies
    what is in front of it. `resolve_launch` already refuses to emit survivors; this asserts the
    generator does not paper over that with a placeholder."""
    monkeypatch.setitem(
        gsb.SEAT_PHASES, "integrator",
        (gsb.Phase(name="plan", model="not-a-model", mode="plan", effort="high",
                   does="x", escalates="y"),))
    with pytest.raises(gsb.RenderRefusal) as excinfo:
        gsb.render("integrator", batch=BATCH, date=DATE)
    assert "not-a-model" in str(excinfo.value)


# --- REFUSAL 3: the escalation path -------------------------------------------------------

def test_the_boot_names_the_ESCALATION_PATH_and_what_crosses_the_boundary(integrator):
    """THE hard question this lane's contract refuses to let anyone route around:

        *"a split seat has a HANDOFF between its two halves. State where the boundary is, what
        crosses it, and what happens when the Sonnet half hits something that needs judgment. A
        split that silently lets the cheap half make expensive decisions is worse than no split."*

    The answer has to be IN THE BOOT, because the boot is the only thing the seat reads.
    """
    assert gsb.HANDOFF_ARTIFACT in integrator
    assert gsb.ESCALATION_ARTIFACT in integrator
    for phase in gsb.SEAT_PHASES["integrator"]:
        assert phase.escalates
        assert phase.escalates in integrator


def test_the_EXECUTE_half_is_told_to_STOP_rather_than_to_decide(integrator):
    """The failure this lane was warned about by name. The cheap half must have exactly one
    response to a judgment call, and it must not be 'use your judgment'."""
    execute = gsb.SEAT_PHASES["integrator"][1]
    assert execute.name == "execute"
    assert "STOP" in execute.escalates
    assert "STOP" in integrator


def test_the_escalation_is_PRICED_in_the_boot_so_a_seat_knows_what_it_costs(integrator):
    """Cheap is a claim, and an unpriced one trains a seat either to escalate on everything or to
    avoid it entirely. Both defeat the split. The boot carries the two measured numbers the seat
    needs: what one escalation costs and what one cheap turn saves."""
    assert "0.0812" in integrator          # saving per turn moved opus -> sonnet
    assert "232,875" in integrator         # the measured mean context this is computed at


def test_the_boot_carries_the_SEAT_COST_VERB_so_the_measurement_is_not_a_habit(integrator):
    """DONE-WHEN 4's boot-side leg. The SessionStart digest reports the gap; this line is how the
    seat closes it, and it is in the paste rather than in somebody's memory."""
    assert "lane_cost.py seat-close" in integrator
    assert "--session" in integrator


# --- the escalation path, as a MECHANISM rather than an instruction -----------------------
#
# "Escalate when the plan does not rule it" is, as written, a JUDGMENT CALL -- and the half being
# addressed is the one that cannot make one. That is the contract's own warning taken seriously:
# *"a split that silently lets the cheap half make expensive decisions is worse than no split."*
# An instruction the cheap half must interpret has moved judgment, not removed it.
#
# So the boundary is decidable by a predicate the execute half RUNS rather than applies. The plan
# file carries one entry per queued branch; `refuse_unruled_merge` answers "am I authorised to
# merge this" with a yes, or a refusal naming what to escalate. Nothing about the answer depends
# on the model reading it, which is the property that makes the cheap half safe to be cheap.

def test_a_branch_the_plan_does_not_name_is_REFUSED_and_the_refusal_says_to_escalate():
    plan = "- `worktree-lane-aa-1` -> MERGE · INDEPENDENT\n"
    with pytest.raises(sr.SeatRefusal) as excinfo:
        sr.refuse_unruled_merge(plan, branch="worktree-lane-aa-9")
    message = str(excinfo.value)
    assert "worktree-lane-aa-9" in message
    assert "ESCALATE" in message.upper()


def test_a_branch_the_plan_RULED_is_permitted_and_its_ruling_comes_back():
    plan = ("- `worktree-lane-aa-1` -> MERGE · INDEPENDENT\n"
            "- `worktree-lane-aa-2` -> MERGE · SERIAL, after aa-1\n")
    entry = sr.refuse_unruled_merge(plan, branch="worktree-lane-aa-2")
    assert entry.verdict == "MERGE"
    assert entry.independent is False
    assert sr.refuse_unruled_merge(plan, branch="worktree-lane-aa-1").independent is True


@pytest.mark.parametrize("verdict", ["HOLD", "REFUSE"])
def test_a_branch_the_plan_ruled_AGAINST_is_refused_just_as_hard_as_an_unruled_one(verdict):
    """A plan that says HOLD is a ruling, and the execute half obeying it is the same act as
    escalating an unruled one: in neither case does it decide. What it must never do is read
    'the plan mentions this branch' as 'the plan authorises this merge'."""
    plan = f"- `worktree-lane-aa-1` -> {verdict} · waiting on the operator\n"
    with pytest.raises(sr.SeatRefusal) as excinfo:
        sr.refuse_unruled_merge(plan, branch="worktree-lane-aa-1")
    assert verdict in str(excinfo.value)


def test_a_plan_that_rules_NOTHING_is_refused_rather_than_read_as_ruling_nothing_out():
    """An empty plan and a plan that authorises everything are the same document to a reader that
    only asks 'is this branch forbidden'. The question is the other way round: authority is
    granted per entry, so no entries means no authority."""
    with pytest.raises(sr.SeatRefusal) as excinfo:
        sr.refuse_unruled_merge("# MERGE-PLAN-AA\n\nnothing decided yet\n", branch="anything")
    assert "no plan entr" in str(excinfo.value).lower()


def test_a_branch_ruled_TWICE_with_different_verdicts_is_refused_not_resolved():
    """Taking the first hit would let a superseded ruling authorise a merge, and taking the last
    would let a stale append do it. Neither is the execute half's call -- an ambiguous plan is an
    escalation, which is the same posture `seat_ch8.extract` takes on an ambiguous anchor."""
    plan = ("- `worktree-lane-aa-1` -> MERGE · INDEPENDENT\n"
            "- `worktree-lane-aa-1` -> HOLD · superseded by the operator\n")
    with pytest.raises(sr.SeatRefusal) as excinfo:
        sr.refuse_unruled_merge(plan, branch="worktree-lane-aa-1")
    assert "twice" in str(excinfo.value).lower() or "ambiguous" in str(excinfo.value).lower()


def test_the_queue_the_execute_half_walks_is_READ_from_the_plan_in_the_plans_own_order():
    """The plan's ORDER is a ruling too -- it is most of what the plan half was paid to produce.
    A queue the execute half re-derived would be the cheap half re-deciding the one thing the
    expensive half was there for."""
    plan = ("- `b-third` -> MERGE\n"
            "- `b-first` -> MERGE · INDEPENDENT\n"
            "- `b-held` -> HOLD · blocked\n")
    assert [e.branch for e in sr.ruled_merges(plan)] == ["b-third", "b-first"]
    assert [e.branch for e in sr.ruled_merges(plan, include_unmergeable=True)] == [
        "b-third", "b-first", "b-held"]


def test_the_refusal_is_on_the_INTEGRATOR_roster_so_the_boot_renders_it(integrator):
    """A refusal nobody runs is a function with a test. It reaches the seat by being on the
    roster, which is what puts a runnable line in the rendered boot."""
    assert "unruled-merge" in sr.REFUSALS
    assert "unruled-merge" in sr.SEAT_REFUSALS["integrator"]
    assert "unruled-merge" in integrator
    assert "seat_refusals.py unruled-merge" in integrator


def test_only_the_integrator_carries_it_because_no_other_seat_merges():
    """A seat's absence from a refusal's audience is a claim that the seat cannot commit that
    failure -- the roster's own stated rule. Only the integrator merges."""
    carriers = [s for s, names in sr.SEAT_REFUSALS.items() if "unruled-merge" in names]
    assert carriers == ["integrator"]


# --- the render stays honest --------------------------------------------------------------

def test_the_render_header_names_BOTH_halves_for_a_split_seat(integrator):
    """`model:` on a split seat's header must not report one of two tiers. A header saying `opus`
    over a boot whose second half runs Sonnet is the same class of lie as `opusplan` over a boot
    that ran neither."""
    assert "model: opus (plan) + sonnet (execute)" in integrator


def test_a_split_boot_still_passes_every_guard_the_generator_already_had(tmp_path):
    """The new blocks are rendered text like any other: no live token, no typed path, no
    placeholder, and no wait stated as an intention."""
    gsb.write_bundle(tmp_path, batch=BATCH, date=DATE)
    assert gsb.verify(tmp_path) == []
    text = (tmp_path / gsb.out_name("integrator")).read_text(encoding="utf-8")
    assert not gsb._LEFTOVER_TOKEN_RE.search(text)
    for pattern, _what in gsb._FORBIDDEN_IN_RENDER:
        assert re.search(pattern, text) is None
