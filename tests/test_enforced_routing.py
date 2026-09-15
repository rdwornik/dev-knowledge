"""`[#793]` — the model a contract DECLARES is the model that RUNS, and the default is in the
generator rather than in a paste.

WHAT WAS ALREADY THERE AND IS NOT RE-TESTED HERE. `[#752]` landed the VERIFY and REFUSE legs:
`routing_agreement.model_reading` reads the ran model off the lane's own transcript, and
`merge_receipt`'s fourth incompleteness leg refuses a receipt whose `ran_model` does not match
its `ordered_model`. Those have their own witnesses
(`tests/test_routing_agreement.py`, `tests/test_merge_receipt.py::
test_a_receipt_whose_ran_model_differs_from_its_ordered_model_is_REFUSED`) and are cited, not
restated. This file covers the two legs that were missing and the one hole the landed pair left:

  1. RESOLVE — a tier the BACKGROUND LAUNCHER cannot honour is refused AT FREEZE, not passed
     through to evaporate at dispatch. The whole defect the lane was cut for is a contract that
     ordered `opusplan` and ran `claude-sonnet-5` with every surface agreeing.
  2. CLAUSE 2 — the routing default lives in the generator, keyed on a DECLARED lane kind from
     a closed enum, and an Opus declaration on a text-only lane is refused at freeze.
  3. THE ORDERED SIDE WAS STILL CIRCULAR. `merge_receipt model --ordered <tier>` takes the
     ordered tier as a TYPED STRING. A seat that mis-typed it, or that typed what it wished had
     been ordered, produced a receipt agreeing with itself — the same collapse one column over.
     `--contract` reads it off the FROZEN CONTRACT instead, which is a surface the launcher did
     not write.

RED-FIRST, AND THE WITNESS IS A RECORDED RUN RATHER THAN A LANDED RED COMMIT. `graph-orphan-census`
and `graph-task-coverage` both refuse a staged `scripts/*.py` with no wiring surface and no
claiming open row, so a standalone RED commit cannot land in this repository at all. The RED run
is captured in `docs/audits/2026-09-15-technical-lane-aa-12-enforced-routing.md` before the
implementation existed; this file and the implementation land together.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))

import gen_lane_contract as glc            # noqa: E402
import merge_receipt as mr                 # noqa: E402
import provider_bench as pb                # noqa: E402
import routing_agreement as ra             # noqa: E402


def _spec(**over) -> glc.LaneSpec:
    base = dict(slug="lane-a-787-enforced-routing",
                purpose="the model a contract declares is the model that runs",
                task_id="787", kind="code")
    base.update(over)
    return glc.LaneSpec(**base)


# --- 1. the lane KIND is a declared, closed enum -----------------------------------------

def test_the_kind_enum_is_closed_and_a_miss_is_refused_with_the_enum_named():
    assert glc.KIND_ENUM == ("text", "code", "review")
    with pytest.raises(glc.LaneContractError) as exc:
        glc.validate_kind("digest")
    assert "text" in str(exc.value) and "code" in str(exc.value)


def test_an_ABSENT_kind_is_refused_rather_than_inferred():
    """DECLARED, never guessed — the contract's own instruction, and the reason is in it.

    An inferred kind that is wrong produces a refusal the author cannot act on: they declared
    nothing, so there is nothing for them to correct. A missing declaration is the one failure
    whose remedy is unambiguous.
    """
    with pytest.raises(glc.LaneContractError) as exc:
        glc.validate_kind(None)
    assert "declare" in str(exc.value).lower()


def test_an_emitted_contract_declares_its_kind_and_the_parser_recovers_it():
    text = glc.render_contract(_spec(kind="text", model="sonnet"))
    assert "**Kind:** `text`" in text
    assert glc.parse_contract(text).kind == "text"


def test_a_contract_carrying_no_kind_line_is_reported_by_the_freeze_gate():
    text = glc.render_contract(_spec(kind="text", model="sonnet"))
    stripped = "\n".join(ln for ln in text.splitlines() if not ln.startswith("**Kind:**"))
    problems = glc.parse_contract(stripped).problems
    assert any("kind" in p.lower() for p in problems), problems


# --- 2. clause 1, leg RESOLVE: an inert tier is refused AT FREEZE -------------------------

@pytest.mark.parametrize("shape", ["local", "cloud", "codespace"])
def test_opusplan_is_REFUSED_at_freeze_on_every_unattended_shape(shape):
    refusals = glc.routing_refusals(model="opusplan", kind="code", shape=shape)
    assert refusals, shape
    assert any("opusplan" in r for r in refusals)
    assert any("bypassPermissions" in r or "plan mode" in r for r in refusals)


def test_opusplan_is_ADMITTED_on_the_attended_shape_because_that_seat_can_plan():
    """The scope is narrower than it looks — AX22-3 routes the INTEGRATOR seat to `opusplan`,
    and that seat is attended. Refusing it everywhere would refuse a live, ruled configuration.
    """
    assert glc.routing_refusals(model="opusplan", kind="code", shape="interactive") == []


def test_the_freeze_REFUSES_the_spec_rather_than_emitting_a_token_that_evaporates():
    with pytest.raises(glc.LaneContractError) as exc:
        _spec(model="opusplan", shape="local").validated()
    assert "opusplan" in str(exc.value)


def test_the_inert_tier_table_is_READ_from_the_dispatch_surface_not_restated():
    """One vocabulary, one home. A second copy of the inert-tier table is the four-rival-
    dispatch-commands disease in a new costume, which is the thing this lane exists to end."""
    import dispatch_surface as ds

    assert set(glc.background_inert_models()) == set(ds.BACKGROUND_INERT_MODELS)


# --- 3. clause 2: the default by lane kind, IN THE GENERATOR ------------------------------

def test_a_TEXT_lane_declaring_OPUS_is_refused_at_freeze_with_the_reason():
    refusals = glc.routing_refusals(model="opus", kind="text", shape="local")
    assert refusals
    joined = " ".join(refusals)
    assert "text" in joined and "opus" in joined


def test_the_text_lane_refusal_NAMES_the_rule_vs_ruling_conflict_it_sits_on():
    """Clause 2 NARROWS the ruled Ch8 matrix, which makes `opus` the default for any arc
    touching `.dev-knowledge`. The two disagree on a hub text-only lane, and that disagreement
    is escalation class (b) — so the refusal reports it at the point it fires rather than
    picking a winner silently."""
    joined = " ".join(glc.routing_refusals(model="opus", kind="text", shape="local"))
    assert "PLAYBOOK" in joined and "Ch8" in joined


def test_a_TEXT_lane_on_sonnet_or_haiku_is_clean():
    assert glc.routing_refusals(model="sonnet", kind="text", shape="local") == []
    assert glc.routing_refusals(model="haiku", kind="text", shape="local") == []


def test_a_CODE_lane_on_either_half_of_the_split_is_clean_and_the_contract_SAYS_it_is_two():
    assert glc.routing_refusals(model="opus", kind="code", shape="local") == []
    assert glc.routing_refusals(model="sonnet", kind="code", shape="local") == []
    text = glc.render_contract(_spec(kind="code", model="opus"))
    assert "two sessions" in text


def test_a_REVIEW_lane_is_refused_because_the_reviewer_role_routes_to_another_CLI():
    """`ecosystem/routing-table.yaml` is the AUTHORITY for role -> CLI (Z-G3 A2). Every shape
    this generator emits launches a `claude` session, so a review lane frozen here names a CLI
    the authority does not route the role to."""
    for model in ("opus", "sonnet", "haiku"):
        refusals = glc.routing_refusals(model=model, kind="review", shape="local")
        assert refusals, model
        assert any("routing-table.yaml" in r for r in refusals)


def test_the_reviewer_cli_is_read_from_the_authority_rather_than_restated():
    assert glc.reviewer_cli() == "codex"


def test_a_mis_declared_contract_is_refused_by_the_FREEZE_GATE_end_to_end(tmp_path):
    """Not a unit test of a predicate: the CLI is invoked, and it refuses."""
    from click.testing import CliRunner

    result = CliRunner().invoke(glc.cli, [
        "emit", "--slug", "lane-b-000-digest", "--purpose", "read-only digest of the corpus",
        "--kind", "text", "--model", "opus", "--out-dir", str(tmp_path)])
    assert result.exit_code != 0, result.output
    # NOT A VACUOUS PASS. Before `--kind` existed this invocation also exited non-zero -- with
    # click's "no such option", which is a different refusal about a different thing. Asserting
    # the REASON is what makes this test able to fail for the right cause.
    assert "text" in result.output and "clause 2" in result.output, result.output
    assert not list(tmp_path.glob("LANE-*.md")), "a refused contract must not be written"


def test_the_check_verb_refuses_a_hand_edited_contract_that_flips_the_model(tmp_path):
    text = glc.render_contract(_spec(kind="text", model="sonnet"))
    mangled = (text.replace("| sonnet | execute | high |", "| opus | execute | high |")
                   .replace("--model sonnet", "--model opus"))
    path = tmp_path / glc.contract_filename("lane-a-787-enforced-routing")
    path.write_text(mangled, encoding="utf-8", newline="\n")

    from click.testing import CliRunner

    result = CliRunner().invoke(glc.cli, ["check", str(path)])
    assert result.exit_code != 0, result.output


# --- 4. clause 1, the ordered side stops being circular ------------------------------------

def _seed_transcript(tmp_path: Path, model: str, n: int = 3) -> tuple[Path, Path]:
    tree = tmp_path / "tree"
    tree.mkdir(parents=True, exist_ok=True)
    store = tmp_path / "sessions"
    (store / ra.session_slug(tree)).mkdir(parents=True, exist_ok=True)
    lines = [json.dumps({"type": "assistant", "message": {"model": model}}) for _ in range(n)]
    (store / ra.session_slug(tree) / "s.jsonl").write_text("\n".join(lines), encoding="utf-8")
    return tree, store


def test_the_ordered_tier_can_be_read_off_the_FROZEN_CONTRACT(tmp_path):
    path = tmp_path / glc.contract_filename("lane-a-787-enforced-routing")
    path.write_text(glc.render_contract(_spec(kind="code", model="sonnet")),
                    encoding="utf-8", newline="\n")
    assert mr.ordered_model_from_contract(path) == "sonnet"


def test_a_contract_declaring_no_routing_row_RAISES_rather_than_defaulting(tmp_path):
    path = tmp_path / "LANE-x.md"
    path.write_text("# LANE x\n\nno routing row here\n", encoding="utf-8", newline="\n")
    with pytest.raises(mr.MergeReceiptError):
        mr.ordered_model_from_contract(path)


def test_the_two_readings_come_from_surfaces_that_cannot_collapse(tmp_path):
    """The contract is written by the ARCHITECT at freeze; the transcript is written by the
    CLI at run time. Neither can be produced from the other, which is what makes a divergence
    detectable at all — a verifier reading both sides off the launcher could not see one."""
    contract = tmp_path / glc.contract_filename("lane-a-787-enforced-routing")
    contract.write_text(glc.render_contract(_spec(kind="code", model="opus")),
                        encoding="utf-8", newline="\n")
    tree, store = _seed_transcript(tmp_path, "claude-sonnet-5")

    ordered = mr.ordered_model_from_contract(contract)
    reading = ra.model_reading(ordered, tree, sessions_root=store)
    assert reading.state == ra.STATE_DIVERGE
    assert "opus" in reading.detail and "claude-sonnet-5" in reading.detail


def test_recording_from_a_contract_lands_BOTH_values_on_the_receipt(tmp_path):
    """END TO END: a receipt is opened, the reading is recorded from the contract plus the
    transcript, and the completeness gate then REFUSES it naming both values."""
    repo = tmp_path / "repo"
    repo.mkdir()
    contract = tmp_path / glc.contract_filename("lane-a-787-enforced-routing")
    contract.write_text(glc.render_contract(_spec(kind="code", model="opus")),
                        encoding="utf-8", newline="\n")
    tree, store = _seed_transcript(tmp_path, "claude-sonnet-5")

    receipt = mr.open_receipt(repo, slug="lane-a-787-enforced-routing", batch="aa",
                              kind=mr.KIND_ARC)
    receipt.steps.append(mr.StepTiming(step="work", step_class=mr.CLASS_TESTS, seconds=1.0,
                                       ok=True, returncode=0, command="pytest",
                                       started=receipt.opened))
    receipt.closed = receipt.opened
    mr.save_receipt(repo, receipt)

    _r, reading = mr.record_model_reading(
        repo, slug="lane-a-787-enforced-routing", contract=contract, worktree=tree,
        read=lambda ordered, wt: ra.model_reading(ordered, wt, sessions_root=store))
    assert reading.state == ra.STATE_DIVERGE

    back = mr.load_receipt(repo, "lane-a-787-enforced-routing")
    assert (back.ordered_model, back.ran_model) == ("opus", "claude-sonnet-5")
    why = back.incompleteness_reason()
    assert why and "opus" in why and "claude-sonnet-5" in why


# --- 5. clause 3: a rate edit MOVES the derived figures -------------------------------------

def test_a_stored_row_carrying_the_per_model_split_is_repriced_at_todays_card():
    row = {"provider": "claude", "outcome": "x", "usd": None, "usd_is_partial": True,
           "unpriced_reason": "stale",
           "model_usage": {"claude-haiku-4-5-20251001":
                           {"input": 1000, "output": 100, "cache_write": 0, "cache_read": 0}}}
    out = pb.reprice_row(row)
    # 1000 input at USD 1.00/MTok + 100 output at USD 5.00/MTok.
    assert out["usd"] == pytest.approx(0.0015)
    assert out["usd_is_partial"] is False
    assert out["unpriced_reason"] is None
    assert row["usd"] is None, "the stored ledger row is never mutated"


def test_a_row_naming_a_model_with_no_rate_is_STILL_refused_by_name_not_costed_at_zero():
    row = {"model_usage": {"qwen2.5-coder:14b": {"input": 10, "output": 10}}}
    out = pb.reprice_row(row)
    assert out["usd_is_partial"] is True
    assert "qwen2.5-coder:14b" in out["unpriced_reason"]


def test_a_LEGACY_row_without_the_split_is_returned_UNCHANGED():
    """The ten claude rows of the 2026-09-15 sweep are this case. Haiku is priced now, and
    their partial flag still cannot be cleared: the side-call's input/output split was never
    written down, so the money is unrecoverable rather than merely unpriced. Returning them
    untouched is the honest answer; re-pricing from the answering model's counts alone would
    drop the remainder and clear a flag that is still true."""
    row = {"provider": "claude", "usd": 0.01148, "usd_is_partial": True,
           "input_tokens": 2, "output_tokens": 6, "unpriced_reason": "haiku (959 tokens): ..."}
    assert pb.reprice_row(row) == row


def test_the_haiku_id_the_CLI_ACTUALLY_EMITS_resolves_in_the_registry():
    """Keyed on the CLI-emitted string, dated suffix and all: `resolve_rate` looks the attested
    id up RAW and the registry has no alias field, so a row keyed on the marketing id would
    resolve nothing and leave the baseline partial exactly where it was."""
    import provider_registry as pr

    rate = pr.resolve_rate("claude-haiku-4-5-20251001")
    assert (rate.input, rate.output) == (1.0, 5.0)
