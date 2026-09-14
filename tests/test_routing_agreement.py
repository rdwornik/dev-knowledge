"""[#613] — the L0 routing-agreement organ.

The property under test is register ruling **Z-G3 amendment A2**: the authoritative routing
table is in-repo and an agreement check asserts the L0 derived copy matches it. The tests that
matter most here are the NEGATIVE ones, because this organ's whole reason to exist is that
silence must not read as agreement (**Z-G4**).
"""
from __future__ import annotations

import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import routing_agreement as ra  # noqa: E402
from audit_checks.check_routing_agreement import check_routing_agreement  # noqa: E402

_TABLE = """
version: 1
roles:
  producer:
    cli: claude-code
  reviewer:
    cli: codex
  fan_out:
    cli: [luna, haiku]
l0_derived_copy: "{l0}"
"""


def _repo(tmp_path, l0: pathlib.Path):
    (tmp_path / "ecosystem").mkdir(parents=True, exist_ok=True)
    (tmp_path / "ecosystem" / "routing-table.yaml").write_text(
        _TABLE.format(l0=l0.as_posix()), encoding="utf-8", newline="\n")
    return tmp_path


def test_agreement_passes_when_l0_corroborates_every_role(tmp_path):
    l0 = tmp_path / "ROUTING.md"
    l0.write_text("producer: claude-code\nreviewer: codex\nfan-out: luna, haiku\n",
                  encoding="utf-8", newline="\n")
    state, diverged, _ = ra.scan(_repo(tmp_path, l0))
    assert (state, diverged) == ("agree", [])
    assert check_routing_agreement(_repo(tmp_path, l0))[0].status == "pass"


def test_a_role_l0_omits_entirely_is_a_DIVERGENCE_not_a_pass(tmp_path):
    """Silence is the failure mode, not the absence of one.

    An L0 copy that simply never mentions `fan_out` would, under a naive "check what both
    mention" comparison, agree vacuously. That is the shape of every green-by-omission bug.
    """
    l0 = tmp_path / "ROUTING.md"
    l0.write_text("producer: claude-code\nreviewer: codex\n", encoding="utf-8", newline="\n")
    state, diverged, _ = ra.scan(_repo(tmp_path, l0))
    assert state == "diverge"
    assert [d.role for d in diverged] == ["fan_out"]
    assert check_routing_agreement(_repo(tmp_path, l0))[0].status == "fail"


def test_a_role_bound_to_a_cli_l0_does_not_name_diverges(tmp_path):
    l0 = tmp_path / "ROUTING.md"
    l0.write_text("producer: claude-code\nreviewer: codex\nfan-out: luna\n",
                  encoding="utf-8", newline="\n")
    state, diverged, detail = ra.scan(_repo(tmp_path, l0))
    assert state == "diverge"
    assert "haiku" in detail


def test_absent_l0_is_a_REPORTED_GAP_never_a_pass(tmp_path):
    """Z-G4: a check that cannot compute its ground truth FAILs, it does not skip.

    L0 lives on the operator's disk, so it is missing on exactly the hosts where routing drift
    is least visible -- CI, a container, a cloud lane. A skip here would make the organ absent
    precisely where it is needed, and `unavailable` would be worse: audit.py projects that onto
    `pass`, so the arc would SHIP GREEN having measured nothing.
    """
    l0 = tmp_path / "does-not-exist.md"
    state, diverged, _ = ra.scan(_repo(tmp_path, l0))
    assert state == "l0-absent"
    assert diverged is None
    finding = check_routing_agreement(_repo(tmp_path, l0))[0]
    assert finding.status == "warn", "an absent L0 is a reported gap, never a pass"
    assert finding.status != "unavailable"


def test_a_repo_with_no_table_is_subject_absent_not_a_failure(tmp_path):
    findings = check_routing_agreement(tmp_path)
    assert findings[0].status not in {"fail", "pass"}


def test_an_unreadable_table_FAILS_rather_than_reporting_zero_divergence(tmp_path):
    (tmp_path / "ecosystem").mkdir(parents=True)
    (tmp_path / "ecosystem" / "routing-table.yaml").write_text(
        "roles: [this, is, not, a, mapping]\n", encoding="utf-8", newline="\n")
    with pytest.raises(ra.RoutingAgreementError):
        ra.load_table(tmp_path)
    assert check_routing_agreement(tmp_path)[0].status == "fail"


def test_the_live_table_is_well_formed():
    """The shipped table parses and binds every role the ruling names."""
    root = pathlib.Path(__file__).resolve().parents[1]
    roles, l0 = ra.load_table(root)
    assert {"producer", "reviewer", "adversarial", "fan_out"} <= set(roles)
    assert roles["reviewer"] == ["codex"]
    assert roles["adversarial"] == ["sol"]
    assert l0.endswith("ROUTING.md")


def test_a_cli_named_elsewhere_does_not_corroborate_a_role(tmp_path):
    """FALSE AGREEMENT is the one outcome this organ may not produce -- terra HIGH 2026-08-28.

    L0 binds `reviewer` to the WRONG cli, but names the right one under an unrelated role.
    A whole-document search agrees; a region-scoped one does not. If this test ever passes
    vacuously the organ is certifying agreement about the binding it got wrong.
    """
    l0 = tmp_path / "ROUTING.md"
    l0.write_text(
        "producer: codex\n"
        "reviewer: claude-code\n"
        "fan-out: luna, haiku\n",
        encoding="utf-8", newline="\n")
    state, diverged, detail = ra.scan(_repo(tmp_path, l0))
    assert state == "diverge"
    roles = {d.role for d in diverged}
    assert "reviewer" in roles, f"reviewer must diverge; got {detail}"


def test_a_crlf_l0_copy_agrees_exactly_as_the_lf_one_does(tmp_path):
    """A line-ending flip on the derived copy is not a routing divergence.

    WHY THIS IS A REAL PATH AND NOT A HYPOTHETICAL. `~/.claude` is a git repo with autocrlf on:
    committing `ROUTING.md` warns that LF will be replaced by CRLF the next time git touches the
    file, so the L0 copy this organ reads flips endings on an ordinary checkout. Were the
    comparison CR-sensitive, that checkout would report divergence on every role and read as a
    routing defect -- the check certifying a break that never happened.
    """
    body = "producer: claude-code@CRLF@reviewer: codex@CRLF@fan-out: luna, haiku@CRLF@"
    crlf = tmp_path / "ROUTING.md"
    crlf.write_text(body.replace("@CRLF@", "@CR@" + chr(10)).replace("@CR@", chr(13)),
                    encoding="utf-8", newline="")

    assert chr(13) in crlf.read_bytes().decode("utf-8")   # the fixture really is CRLF
    state, diverged, _ = ra.scan(_repo(tmp_path, crlf))
    assert (state, diverged) == ("agree", [])


def test_render_puts_every_cli_on_the_SAME_LINE_as_its_role(tmp_path):
    """The one-line-per-role property `compare`'s region bound depends on.

    A renderer that wrapped a role's CLIs onto a following line would still LOOK right and would
    still pass a naive round-trip, because `_role_regions` extends up to `_REGION_LINES`. It
    would break the moment a role gained a fourth CLI. Asserting adjacency on the LINE is the
    only form of this test that keeps failing when it should.
    """
    roles = {"producer": ["claude-code"], "fan_out": ["luna", "haiku", "gemini"]}
    rendered = ra.render_table(roles)
    lines = rendered.splitlines()

    assert lines[0] == ra.REGION_BEGIN and lines[-1] == ra.REGION_END
    for role, clis in roles.items():
        row = [ln for ln in lines if ln.startswith(f"| {role} ")]
        assert len(row) == 1, f"{role} renders on {len(row)} rows, expected exactly 1"
        assert all(c in row[0] for c in clis)


def test_a_rendered_region_makes_a_previously_diverging_l0_agree(tmp_path):
    """The closure property: rendering into an L0 copy that named no role closes the gate."""
    l0 = tmp_path / "ROUTING.md"
    l0.write_text("# Task Routing Rules@NL@@NL@Prose that binds no role to a CLI.@NL@"
                  .replace("@NL@", chr(10)), encoding="utf-8", newline="\n")
    repo = _repo(tmp_path, l0)
    assert ra.scan(repo)[0] == "diverge"

    roles, _ = ra.load_table(repo)
    l0.write_text(l0.read_text(encoding="utf-8") + chr(10) + ra.render_table(roles),
                  encoding="utf-8", newline="\n")
    assert ra.scan(repo)[0] == "agree"


# ===============================================================================================
# RED-FIRST WITNESSES (ADR-108 §B) -- `[#752]`, the ORDERED-vs-RAN reading.
#
# THE DISPATCH LINE RECORDS WHAT WAS ASKED; ONLY THE TRANSCRIPT RECORDS WHAT RAN. Batch X3 slot 1
# ordered `opusplan`, the resolved line printed `--model opusplan`, `claude --print --model
# opusplan` resolved fine, and the lane's own transcript recorded 84 of 84 assistant messages on
# `claude-sonnet-5`. Every surface that could be READ agreed with the order; the only surface that
# disagreed was the one nobody was reading. That is what this section reads.
#
# WHY IT LIVES IN THE AGREEMENT ORGAN. This module already answers one agreement question -- does
# the derived L0 copy still say what the in-repo table says -- under one standing rule: a check
# that cannot compute its ground truth FAILs and never skips (**Z-G4**), because the host where
# the copy is missing is exactly the host where drift is least visible. "Did the tier the contract
# ordered actually run" is the same question about a different pair of copies, and it inherits the
# same rule: an absent session store is a reported GAP, never an agreement.
# ===============================================================================================

import json  # noqa: E402


def _seed(store, worktree, models, *, extra_lines=()):
    """Write a transcript for `worktree` into `store`, one assistant message per entry in
    `models`. Seeded in the store's own shape rather than through a stub, so what is under test is
    the reading of a real file layout."""
    d = store / ra.session_slug(worktree)
    d.mkdir(parents=True, exist_ok=True)
    rows = [json.dumps({"type": "assistant", "message": {"model": m}}) for m in models]
    (d / "session.jsonl").write_text("\n".join([*rows, *extra_lines]) + "\n",
                                     encoding="utf-8", newline="\n")
    return d


def test_the_session_slug_replaces_every_character_outside_the_stores_alphabet():
    """The store names a project directory by flattening its absolute path: every character
    outside `[A-Za-z0-9_-]` becomes ONE dash, which is what produces the doubled dash after a
    drive letter and before a dotted directory. Same encoder `gen_handoff._session_slug` uses."""
    slug = ra.session_slug("/tmp/x.y/.claude/worktrees/lane-a")
    assert set(slug) <= set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
    assert "--claude-worktrees-lane-a" in slug


def test_the_ran_model_is_read_off_the_transcript(tmp_path):
    store, tree = tmp_path / "store", tmp_path / "tree"
    _seed(store, tree, ["claude-opus-5"] * 3)
    assert ra.ran_models(tree, sessions_root=store) == {"claude-opus-5": 3}
    assert ra.ran_model(tree, sessions_root=store) == "claude-opus-5"


def test_only_assistant_messages_are_counted(tmp_path):
    """A `model` key elsewhere in the stream is not a statement about what generated a turn."""
    store, tree = tmp_path / "store", tmp_path / "tree"
    _seed(store, tree, ["claude-opus-5"],
          extra_lines=[json.dumps({"type": "user", "message": {"model": "claude-haiku-4-5"}})])
    assert ra.ran_models(tree, sessions_root=store) == {"claude-opus-5": 1}


def test_a_partial_trailing_line_does_not_empty_the_tally(tmp_path):
    """A LIVE transcript is being appended to while it is read, so its last line is routinely a
    half-written object. Refusing the whole file on it would make every reading of a running lane
    report nothing -- an absence manufactured by the instrument."""
    store, tree = tmp_path / "store", tmp_path / "tree"
    _seed(store, tree, ["claude-opus-5"] * 2, extra_lines=['{"type": "assist'])
    assert ra.ran_models(tree, sessions_root=store) == {"claude-opus-5": 2}


def test_the_whole_tally_is_reported_not_only_the_winner(tmp_path):
    """A lane that ran mostly Opus with Haiku subagents is a different fact from a pure-Opus lane,
    and the dominant model alone cannot tell them apart. The reading carries both."""
    store, tree = tmp_path / "store", tmp_path / "tree"
    _seed(store, tree, ["claude-opus-5"] * 9 + ["claude-haiku-4-5-20251001"])
    reading = ra.model_reading("opus", tree, sessions_root=store)
    assert reading.state == "agree"
    assert reading.tally == {"claude-opus-5": 9, "claude-haiku-4-5-20251001": 1}
    assert "claude-haiku-4-5-20251001" in reading.detail


def test_an_ordered_tier_the_lane_did_not_run_diverges(tmp_path):
    store, tree = tmp_path / "store", tmp_path / "tree"
    _seed(store, tree, ["claude-sonnet-5"] * 84)
    reading = ra.model_reading("opus", tree, sessions_root=store)
    assert reading.state == "diverge"
    assert reading.ran == "claude-sonnet-5" and "opus" in reading.detail


def test_the_x689_reading_is_a_REPORTED_GAP_rather_than_an_agreement(tmp_path):
    """THE WITNESS, reconstructed at its measured proportions: ordered `opusplan`, ran 84 of 84 on
    `claude-sonnet-5`.

    `opusplan` is a SPLIT tier -- Opus while the session plans, Sonnet after -- so BOTH families
    are a legal reading of it and no transcript can confirm or refute the order. Calling that
    "agree" because Sonnet is one of its halves would certify exactly the collapse that made every
    routing decision in that window advisory. Z-G4's rule is the one that applies: a check that
    cannot compute its ground truth reports a GAP, and no aggregate surface may count it as a
    pass."""
    store, tree = tmp_path / "store", tmp_path / "tree"
    _seed(store, tree, ["claude-sonnet-5"] * 84)
    reading = ra.model_reading("opusplan", tree, sessions_root=store)
    assert reading.state == ra.STATE_UNVERIFIABLE
    assert reading.state != "agree"
    assert reading.ran == "claude-sonnet-5"
    assert "split" in reading.detail.lower()


def test_an_absent_session_store_is_a_reported_gap_never_an_agreement(tmp_path):
    """Z-G4, and the trap it names is live here: the session store sits on the machine that ran
    the lane, so it is missing on exactly the hosts where a routing claim is least checkable --
    CI, a container, another operator's clone."""
    reading = ra.model_reading("opus", tmp_path / "tree", sessions_root=tmp_path / "nothing")
    assert reading.state == ra.STATE_NO_TRANSCRIPT
    assert reading.state != "agree"
    assert reading.ran is None


def test_a_transcript_with_no_assistant_message_is_a_gap_not_an_agreement(tmp_path):
    """An empty tally is an absence, not a match. Zero assistant messages agrees with every order
    ever placed, which is the shape of answer this organ exists to refuse."""
    store, tree = tmp_path / "store", tmp_path / "tree"
    _seed(store, tree, [])
    assert ra.model_reading("opus", tree, sessions_root=store).state == ra.STATE_NO_TRANSCRIPT


def test_an_ordered_tier_outside_the_enum_is_reported_not_guessed(tmp_path):
    store, tree = tmp_path / "store", tmp_path / "tree"
    _seed(store, tree, ["claude-opus-5"])
    reading = ra.model_reading("gpt", tree, sessions_root=store)
    assert reading.state != "agree"
    assert "gpt" in reading.detail
