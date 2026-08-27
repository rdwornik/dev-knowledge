"""`[#591]` — the substrate validator, layer 2. RED-first against seeded fixtures.

Layer 1 is `gen_lane_contract.parse_contract`: it checks that a contract's declared *shape*
and its command line agree, and that its mechanical regions are present. It explicitly does
NOT check the declaration against what the contract then ASKS FOR — its own docstring's
honest limit is *"it checks SHAPE, never whether a contract's footprint claims are true"*.

Layer 2 is this module's subject: a contract that declares a substrate its own content
contradicts. Four legs, each one a REFUSAL that names the rule it fired on, per intake #52's
functional requirement and `tasks/591-*.md`'s done-when:

  1. a substrate with **no live verb** (or none declared at all) — REFUSE
  2. **cloud** + a **gate** in its Done-when — REFUSE (PLAYBOOK Ch8 Layer-1 Q1)
  3. **cloud/codespace** + an **operator-disk path** — REFUSE (Ch8 Q2)
  4. a **second local writer** in one checkout — WARN (Ch8 concurrency ceilings)

Every test here seeds its own fixture text. Nothing reads a live contract off the tree: the
committed launch-contract corpus predates this validator and grandfathering it is a ruling,
not a test's decision.
"""
from __future__ import annotations

import textwrap

import pytest

import validate_substrate as vs


# --- fixture builders -------------------------------------------------------

def _contract(*, shape_line: str, done: str = "1. `<something checkable>`",
              body: str = "", pairing: str = "slug `lane-a-1-x` -> branch "
                           "`worktree-lane-a-1-x` -> contract `LANE-a-1-x.md`") -> str:
    """A minimal contract carrying only what layer 2 reads.

    Deliberately NOT a full `gen_lane_contract` emission: layer 2 reads the substrate
    declaration, the Done-when section, the pairing line and the whole body, and a fixture
    that carried the other mechanical regions would be asserting layer 1's contract inside
    layer 2's tests.
    """
    template = textwrap.dedent("""\
        # LANE lane-a-1-x — a seeded fixture

        ## Dispatch

        {shape_line}

        ## Worktree pairing

        {pairing}

        ## Done-contract (immutable)

        {done}

        ## Steps

        1. `<imperative>` **COMMIT**

        {body}
        """)
    # Substituted AFTER the dedent, not inside an f-string: a multi-line `body` whose second
    # line carries no indentation makes `dedent` compute an empty common prefix, so the whole
    # fixture keeps its 8-space source indent and every heading moves off column 0. That is a
    # fixture bug that reads exactly like a validator bug — the Done-when section comes back
    # empty and leg 2 silently stops firing.
    return template.format(shape_line=shape_line, pairing=pairing, done=done, body=body)


@pytest.fixture()
def registry():
    """The live committed registry — the one source the validator and the router read."""
    return vs.load_registry(vs.repo_root())


# --- the registry itself ----------------------------------------------------

def test_registry_declares_the_three_ruled_substrates_plus_interactive(registry):
    """STANDING_RULINGS V3 names three substrate verbs; Ch8 row 3 adds the interactive shape."""
    assert {"local", "cloud", "codespace", "interactive"} <= set(registry)
    assert registry["local"].family == "local"
    assert registry["interactive"].family == "local"


def test_every_registry_entry_declares_its_verb_and_its_liveness(registry):
    for name, sub in registry.items():
        assert sub.verbs, f"{name} declares no verb"
        assert isinstance(sub.live, bool)


def test_registry_matches_the_generator_shape_enum(registry):
    """The registry may not drift from `gen_lane_contract.SHAPE_ENUM`.

    Layer 1 refuses a shape outside its enum; layer 2 would then be checking a vocabulary
    layer 1 can never emit. Every generator shape is a registry key.
    """
    import gen_lane_contract as glc
    assert set(glc.SHAPE_ENUM) <= set(registry)


# --- leg 1: no live verb ----------------------------------------------------

def test_refuses_a_substrate_with_no_live_verb(registry):
    text = _contract(shape_line="**Substrate:** `mainframe`")
    refusals = vs.validate_contract(text, source="F.md", registry=registry)
    assert [r.rule for r in refusals] == [vs.RULE_NO_LIVE_VERB]
    assert "mainframe" in refusals[0].detail


def test_refuses_a_contract_declaring_no_substrate_at_all(registry):
    """V7's other half: *"refusing when the field is missing"*."""
    text = _contract(shape_line="(no declaration here)")
    refusals = vs.validate_contract(text, source="F.md", registry=registry)
    assert [r.rule for r in refusals] == [vs.RULE_NO_LIVE_VERB]


def test_refuses_a_registered_substrate_whose_verb_is_not_live(registry):
    """A substrate may be DECLARED and still have no live verb — the V7 router case."""
    seeded = dict(registry)
    seeded["planned"] = vs.Substrate(
        name="planned", family="local", verbs=("Dispatch-Planned",), aliases=(),
        live=False, admits_gate_dependent_work=True, operator_disk=True)
    text = _contract(shape_line="**Substrate:** `planned`")
    refusals = vs.validate_contract(text, source="F.md", registry=seeded)
    assert [r.rule for r in refusals] == [vs.RULE_NO_LIVE_VERB]
    assert "no live verb" in refusals[0].detail


def test_accepts_the_generator_shape_spelling(registry):
    """`gen_lane_contract` writes ``**Shape:** `local` `` — the same declaration."""
    text = _contract(shape_line="**Shape:** `local` — a background lane.")
    assert vs.validate_contract(text, source="F.md", registry=registry) == []


def test_accepts_the_ch8_bolded_prose_spelling(registry):
    """Live contracts write `**Substrate: LOCAL worktree**` — read, not refused on form."""
    text = _contract(shape_line="**Substrate: LOCAL worktree**, gates armed")
    assert vs.validate_contract(text, source="F.md", registry=registry) == []


# --- leg 2: cloud + a gate in the Done-when ---------------------------------

def test_refuses_cloud_plus_a_gate_in_the_done_when(registry):
    text = _contract(shape_line="**Substrate:** `cloud`",
                     done="1. `pytest` green and `audit.py health` green")
    refusals = vs.validate_contract(text, source="F.md", registry=registry)
    assert vs.RULE_CLOUD_GATE in [r.rule for r in refusals]
    fired = next(r for r in refusals if r.rule == vs.RULE_CLOUD_GATE)
    assert "pytest" in fired.detail


def test_codespace_plus_a_gate_is_admitted(registry):
    """Ch8 Q1 routes gate-dependent work to *"Codespace or local"* — only cloud is refused."""
    text = _contract(shape_line="**Substrate:** `codespace`",
                     done="1. `pytest` green")
    assert [r.rule for r in vs.validate_contract(text, source="F.md", registry=registry)] == []


def test_a_gate_word_outside_the_done_when_does_not_fire(registry):
    """Scoped to the Done-when, per the requirement's own words."""
    text = _contract(shape_line="**Substrate:** `cloud`",
                     done="1. `<a read-only census>`",
                     body="The integrator runs `pytest` locally after the merge.")
    assert [r.rule for r in vs.validate_contract(text, source="F.md", registry=registry)] == []


# --- leg 3: off-machine substrate + an operator-disk path -------------------

@pytest.mark.parametrize("path", [
    r"C:\Users\1028120\Downloads\LANE-x.md",
    r"~\Downloads\LANE-x.md",
    "~/Downloads/LANE-x.md",
    "$env:CLAUDE_PROMPTS_DIR",
    "%USERPROFILE%",
])
def test_refuses_cloud_or_codespace_plus_an_operator_disk_path(registry, path):
    for substrate in ("cloud", "codespace"):
        text = _contract(shape_line=f"**Substrate:** `{substrate}`",
                         body=f"Read the contract at {path} first.")
        refusals = vs.validate_contract(text, source="F.md", registry=registry)
        assert vs.RULE_OFFMACHINE_PATH in [r.rule for r in refusals], (substrate, path)


def test_a_local_lane_may_name_an_operator_disk_path(registry):
    text = _contract(shape_line="**Substrate:** `local`",
                     body=r"Read `~\Downloads\LANE-x.md`.")
    assert [r.rule for r in vs.validate_contract(text, source="F.md", registry=registry)] == []


# --- leg 4: a second local writer in one checkout ---------------------------

def test_warns_on_two_local_contracts_sharing_one_checkout(registry):
    shared = ("slug `lane-a-1-x` -> branch `worktree-shared` -> contract `LANE-a-1-x.md`")
    batch = {
        "A.md": _contract(shape_line="**Substrate:** `local`", pairing=shared),
        "B.md": _contract(shape_line="**Substrate:** `local`", pairing=shared),
    }
    refusals = vs.validate_batch(batch, registry=registry)
    writer = [r for r in refusals if r.rule == vs.RULE_SECOND_LOCAL_WRITER]
    assert writer, refusals
    assert writer[0].severity == "warn"
    assert "worktree-shared" in writer[0].detail


def test_two_interactive_contracts_share_the_primary_checkout(registry):
    """An interactive session has no lane branch — it runs in the primary checkout."""
    batch = {
        "A.md": _contract(shape_line="**Substrate:** `interactive`",
                          pairing="slug `lane-a-1-x` -> contract `LANE-a-1-x.md`"),
        "B.md": _contract(shape_line="**Substrate:** `interactive`",
                          pairing="slug `lane-b-2-y` -> contract `LANE-b-2-y.md`"),
    }
    writer = [r for r in vs.validate_batch(batch, registry=registry)
              if r.rule == vs.RULE_SECOND_LOCAL_WRITER]
    assert writer
    assert writer[0].severity == "warn"


def test_distinct_worktrees_are_not_a_second_writer(registry):
    batch = {
        "A.md": _contract(shape_line="**Substrate:** `local`"),
        "B.md": _contract(shape_line="**Substrate:** `local`",
                          pairing="slug `lane-b-2-y` -> branch `worktree-lane-b-2-y` "
                                  "-> contract `LANE-b-2-y.md`"),
    }
    assert [r for r in vs.validate_batch(batch, registry=registry)
            if r.rule == vs.RULE_SECOND_LOCAL_WRITER] == []


def test_cloud_lanes_never_contend_for_a_checkout(registry):
    """A cloud lane owns its own clone — Ch8's ceilings call it effectively unlimited."""
    batch = {
        "A.md": _contract(shape_line="**Substrate:** `cloud`",
                          pairing="slug `lane-a-1-x` -> branch `claude/lane-a-1-x` "
                                  "-> contract `LANE-a-1-x.md`"),
        "B.md": _contract(shape_line="**Substrate:** `cloud`",
                          pairing="slug `lane-a-1-x` -> branch `claude/lane-a-1-x` "
                                  "-> contract `LANE-a-1-x.md`"),
    }
    assert [r for r in vs.validate_batch(batch, registry=registry)
            if r.rule == vs.RULE_SECOND_LOCAL_WRITER] == []


# --- the override: an explicit RECORDED deviation, never a silent pass ------

def test_an_override_downgrades_but_never_silences(registry):
    text = _contract(
        shape_line="**Substrate:** `cloud`",
        done="1. `pytest` green",
        body="**Substrate deviation:** substrate-cloud-gate-dependent — the lane hand-runs "
             "the suite as `python3` and declares that it did (Ch8 cloud guards).")
    refusals = vs.validate_contract(text, source="F.md", registry=registry)
    fired = next(r for r in refusals if r.rule == vs.RULE_CLOUD_GATE)
    assert fired.overridden is True
    assert fired.severity == "warn"
    assert "hand-runs" in fired.detail


def test_an_override_with_no_reason_is_not_an_override(registry):
    text = _contract(shape_line="**Substrate:** `cloud`",
                     done="1. `pytest` green",
                     body="**Substrate deviation:** substrate-cloud-gate-dependent — ok")
    fired = next(r for r in vs.validate_contract(text, source="F.md", registry=registry)
                 if r.rule == vs.RULE_CLOUD_GATE)
    assert fired.overridden is False
    assert fired.severity == "refuse"


def test_an_override_binds_only_the_rule_it_names(registry):
    text = _contract(
        shape_line="**Substrate:** `cloud`",
        done="1. `pytest` green",
        body="**Substrate deviation:** substrate-offmachine-operator-path — a different "
             "rule entirely, recorded here so the mismatch is visible.\n"
             r"Read `~\Downloads\LANE-x.md`.")
    by_rule = {r.rule: r for r in vs.validate_contract(text, source="F.md", registry=registry)}
    assert by_rule[vs.RULE_CLOUD_GATE].overridden is False
    assert by_rule[vs.RULE_OFFMACHINE_PATH].overridden is True


def test_an_override_naming_an_unknown_rule_is_reported(registry):
    text = _contract(shape_line="**Substrate:** `local`",
                     body="**Substrate deviation:** substrate-invented-rule — a reason long "
                          "enough to clear the substance floor by a wide margin.")
    refusals = vs.validate_contract(text, source="F.md", registry=registry)
    assert [r.rule for r in refusals] == [vs.RULE_UNKNOWN_OVERRIDE]


# --- every refusal names its rule -------------------------------------------

def test_every_refusal_names_the_rule_it_fired_on(registry):
    text = _contract(shape_line="**Substrate:** `cloud`",
                     done="1. `pytest` green",
                     body=r"Read `C:\Users\x\Downloads\LANE-x.md`.")
    refusals = vs.validate_contract(text, source="F.md", registry=registry)
    assert len(refusals) == 2
    for r in refusals:
        assert r.rule in vs.RULE_IDS
        assert r.rule in r.render()
        assert "F.md" in r.render()


def test_rule_ids_are_the_closed_checkable_surface():
    assert vs.RULE_IDS == (
        vs.RULE_NO_LIVE_VERB,
        vs.RULE_CLOUD_GATE,
        vs.RULE_OFFMACHINE_PATH,
        vs.RULE_SECOND_LOCAL_WRITER,
        vs.RULE_UNKNOWN_OVERRIDE,
    )
