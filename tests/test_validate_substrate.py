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
    """Legs 5 and 6 entered this tuple at batch E's freeze (0a and CUT-6), deliberately —
    which is exactly what this pin exists to force: a new leg cannot arrive silently."""
    assert vs.RULE_IDS == (
        vs.RULE_NO_LIVE_VERB,
        vs.RULE_CLOUD_GATE,
        vs.RULE_OFFMACHINE_PATH,
        vs.RULE_SECOND_LOCAL_WRITER,
        vs.RULE_TEARDOWN_ENUM,
        vs.RULE_WRITE_SCOPE_DISJOINT,
        vs.RULE_UNKNOWN_OVERRIDE,
    )


# --- C-F: `**Shape:**` PROSE is not a substrate declaration -----------------
#
# The defect, recorded as batch-1 finding C-F and as architect premise error 3 of 3
# (LESSONS.md 2026-08-28): `_SHAPE_RE` accepted a bare unquoted token, so the batch-1
# contract's ordinary English heading `**Shape:** ONE plan -> 5 file-disjoint lanes`
# bound the substrate to `'one'` -- an off-enum value RETURNED rather than reported,
# which then suppressed the genuine `Substrate:` line, because `_SHAPE_RE` wins the
# precedence race and `declared_substrate` returns on its first match.
#
# The fix is a TIGHTER declaration grammar, never a looser substrate check: a
# declaration is a BACKTICKED token, prose is not a declaration. And it is not a NEW
# grammar either -- it is layer 1's existing one. `gen_lane_contract._SHAPE_LINE_RE`
# has always required the backticks (``^\*\*Shape:\*\*\s+`(?P<shape>[a-z]+)` ``), so
# after this the two organs read the generator's field identically instead of
# disagreeing about what counts as a declaration at all.

_BATCH1_PROSE_SHAPE = (
    "# BATCH-1 LANE CONTRACTS - 2026-08-28 - SEQ 2 - ADR-110 shape\n"
    "\n"
    "**Shape:** ONE plan -> 5 file-disjoint lanes -> ONE integration. Operator gates at\n"
    "exactly two points: GO at batch start - end-of-batch packet.\n"
)


def test_prose_shape_line_is_not_a_substrate_declaration():
    """RED before the fix: this returned `'one'`."""
    assert vs.declared_substrate(_BATCH1_PROSE_SHAPE) is None


def test_backticked_shape_line_is_still_read_first():
    """The generator's own spelling keeps working -- the fix tightens, it does not remove."""
    assert vs.declared_substrate("**Shape:** `local` - one worktree per lane.\n") == "local"


def test_prose_shape_no_longer_masks_the_real_substrate_line():
    """RED before the fix: `'one'` won the race and the real line was never read.

    The masking is the expensive half. An off-enum value at least LOOKS wrong; a
    correct declaration silently never being consulted does not.
    """
    text = _BATCH1_PROSE_SHAPE + "\n**Real substrate: LOCAL**, for all five lanes.\n"
    assert vs.declared_substrate(text) == "local"


def test_prose_shape_does_not_fabricate_an_off_enum_refusal(registry):
    """The whole cost of C-F: a false `substrate-no-live-verb` on a correct contract."""
    text = _BATCH1_PROSE_SHAPE + "\n**Substrate:** local\n"
    assert vs.validate_contract(text, source="B1.md", registry=registry) == []


def test_shape_declaration_is_anchored_to_line_start():
    """Terra HIGH, this arc. Unanchored, an EXAMPLE of the field wins the precedence race.

    A contract that explains the convention mid-sentence -- and this corpus does exactly
    that -- would bind to the example and mask the real declaration further down, which is
    the same masking failure the prose heading caused, arriving by a different door.
    """
    text = ("The generator emits **Shape:** `cloud` as its field.\n"
            "\n"
            "**Shape:** `local`\n")
    assert vs.declared_substrate(text) == "local"


def test_shape_declaration_requires_BOTH_backticks():
    """A half-quoted token is not a declaration -- it is a typo, and it falls through.

    Guards the direction the fix must not drift back toward: `` `?`` on either side is
    what made prose parseable in the first place.
    """
    assert vs.declared_substrate("**Shape:** `local\n") is None
    assert vs.declared_substrate("**Shape:** local`\n") is None


# --- LEG 5: teardown-enum coverage (batch E, 0a / CUT-6) --------------------
#
# ADR-116 sat stranded on `claude/lane-f` until a window close, because the batch teardown
# iterates an enum that cannot see a cloud lane: `LANE_BRANCH_RE` matches `worktree-lane-*`
# only, so `claude/<slug>` and codespace lanes are invisible to it AND to the ADR-110
# exemption. This leg makes that a FREEZE-TIME refusal instead of an integration surprise.


def _cloud_shape() -> str:
    return "**Shape:** `cloud`"


def test_leg5_refuses_a_lane_whose_branch_shape_the_teardown_enum_cannot_see(registry):
    """A cloud lane on `claude/<slug>` is outside `LANE_BRANCH_RE` — REFUSE at freeze."""
    text = _contract(
        shape_line=_cloud_shape(),
        pairing="slug `lane-f-0-x` -> branch `claude/lane-f-0-x` -> contract `LANE-f-0-x.md`",
    )
    refusals = vs.validate_contract(text, source="F.md", registry=registry)
    assert vs.RULE_TEARDOWN_ENUM in [r.rule for r in refusals]
    fired = [r for r in refusals if r.rule == vs.RULE_TEARDOWN_ENUM][0]
    assert fired.severity == vs.SEVERITY_REFUSE
    assert "claude/lane-f-0-x" in fired.detail


def test_leg5_passes_a_lane_the_enum_does_cover(registry):
    """`worktree-lane-a-1-x` matches the enum, so teardown can iterate it. No refusal."""
    text = _contract(shape_line="**Shape:** `local`")
    assert vs.RULE_TEARDOWN_ENUM not in [
        r.rule for r in vs.validate_contract(text, source="F.md", registry=registry)]


def test_leg5_is_dischargeable_by_a_recorded_deviation_never_a_silent_pass(registry):
    """`[#591]`'s done-when: an override is an explicit RECORDED deviation, never a silent
    pass. The refusal is downgraded to WARN and KEPT, carrying its reason."""
    text = _contract(
        shape_line=_cloud_shape(),
        pairing="slug `lane-f-0-x` -> branch `claude/lane-f-0-x` -> contract `LANE-f-0-x.md`",
        body=("**Substrate deviation:** `substrate-teardown-enum-coverage` — the batch "
              "manifest enumerates this cloud lane by name and the teardown iterates the "
              "manifest rather than the branch regex.\n"),
    )
    fired = [r for r in vs.validate_contract(text, source="F.md", registry=registry)
             if r.rule == vs.RULE_TEARDOWN_ENUM]
    assert len(fired) == 1, "the refusal is downgraded, never removed"
    assert fired[0].severity == vs.SEVERITY_WARN
    assert fired[0].overridden is True


# --- LEG 6: write-scope disjointness (batch E, CUT-3(c) / CUT-6) ------------
#
# CUT-3 collapsed DC-2+DC-3 into one lane and stripped CLAUDE.md from DC-1's scope so the
# doctrine lanes are genuinely file-disjoint. CUT-3(c) requires that be RE-VERIFIED through
# `[#591]` at freeze rather than asserted, which is what this leg does.


def _scoped(paths: str, *, pairing: str, shape: str = "**Shape:** `local`") -> str:
    return _contract(
        shape_line=shape, pairing=pairing,
        body=f"## Write-scope (frozen)\n\n{paths}\n")


def test_leg6_refuses_two_lanes_in_one_batch_whose_write_scopes_intersect(registry):
    batch = {
        "DC-1.md": _scoped(
            "- `README.md`\n- `scripts/canonical_docs.py`",
            pairing="slug `lane-dc-1-x` -> branch `worktree-lane-dc-1-x` -> "
                    "contract `LANE-dc-1-x.md`"),
        "DC-23.md": _scoped(
            "- `CLAUDE.md`\n- `scripts/canonical_docs.py`",
            pairing="slug `lane-dc-23-x` -> branch `worktree-lane-dc-23-x` -> "
                    "contract `LANE-dc-23-x.md`"),
    }
    fired = [r for r in vs.validate_batch(batch, registry=registry)
             if r.rule == vs.RULE_WRITE_SCOPE_DISJOINT]
    assert len(fired) == 1
    assert fired[0].severity == vs.SEVERITY_REFUSE
    assert "scripts/canonical_docs.py" in fired[0].detail
    assert "DC-1.md" in fired[0].source and "DC-23.md" in fired[0].source


def test_leg6_admits_the_post_cut_shape_where_DC1_dropped_claude_md(registry):
    """The cut's own arrangement must PASS, or the leg is testing nothing about it."""
    batch = {
        "DC-1.md": _scoped(
            "- `README.md`\n- `VISION.md`",
            pairing="slug `lane-dc-1-x` -> branch `worktree-lane-dc-1-x` -> "
                    "contract `LANE-dc-1-x.md`"),
        "DC-23.md": _scoped(
            "- `CLAUDE.md`\n- `protocols/PLAYBOOK.md`",
            pairing="slug `lane-dc-23-x` -> branch `worktree-lane-dc-23-x` -> "
                    "contract `LANE-dc-23-x.md`"),
    }
    assert [r for r in vs.validate_batch(batch, registry=registry)
            if r.rule == vs.RULE_WRITE_SCOPE_DISJOINT] == []


def test_leg6_reads_list_items_only_so_prose_cannot_declare_a_scope(registry):
    """Batch E's own DC-1 says, INSIDE its write-scope section, that `CLAUDE.md` is deliberately
    ABSENT from that scope. Read as a declaration, the disclaimer produced a phantom collision
    with DC-23 on the one file the cut had just separated. A declaration is a bullet."""
    batch = {
        "DC-1.md": _scoped(
            "- `README.md`\n\n**`CLAUDE.md` IS DELIBERATELY ABSENT FROM THIS SCOPE** — the "
            "VISION-line removals are DC-23's last act.",
            pairing="slug `lane-a-1-x` -> branch `worktree-lane-a-1-x` -> "
                    "contract `LANE-a-1-x.md`"),
        "DC-23.md": _scoped(
            "- `CLAUDE.md`",
            pairing="slug `lane-b-2-x` -> branch `worktree-lane-b-2-x` -> "
                    "contract `LANE-b-2-x.md`"),
    }
    assert [r for r in vs.validate_batch(batch, registry=registry)
            if r.rule == vs.RULE_WRITE_SCOPE_DISJOINT] == []


def test_leg6_ignores_a_write_scope_of_NONE(registry):
    """Read-only census lanes declare NONE. Two of them intersect on nothing."""
    batch = {
        "A1.md": _scoped("**NONE — this lane writes no tree file.**",
                         pairing="slug `lane-a1-x` -> branch `worktree-lane-a1-x` -> "
                                 "contract `LANE-a1-x.md`"),
        "A2.md": _scoped("**NONE — this lane writes no tree file.**",
                         pairing="slug `lane-a2-x` -> branch `worktree-lane-a2-x` -> "
                                 "contract `LANE-a2-x.md`"),
    }
    assert [r for r in vs.validate_batch(batch, registry=registry)
            if r.rule == vs.RULE_WRITE_SCOPE_DISJOINT] == []


def test_both_new_legs_are_in_the_closed_rule_surface():
    """RULE_IDS is the checkable surface — a new leg enters it deliberately."""
    assert vs.RULE_TEARDOWN_ENUM in vs.RULE_IDS
    assert vs.RULE_WRITE_SCOPE_DISJOINT in vs.RULE_IDS
    assert len(vs.RULE_IDS) == len(set(vs.RULE_IDS))


# --- the ADAPTER's scoping of the two later-armed legs ----------------------
#
# The logic module is armed unconditionally (above). The commit-time ADAPTER scopes the two
# legs that arrived after it did, because a leg written today cannot honestly gate a contract
# dispatched before it existed. Both properties are asserted here so neither can drift.


def test_adapter_grandfathers_the_two_later_armed_legs_by_their_own_date():
    """Legs 5 and 6 carry their own arm date, LATER than the check's, and both are in the map.

    Without this the commit gate REDs on the whole already-executed corpus — measured: 14
    findings across batch D's and batch E's committed contracts, none of them dischargeable
    without editing a record of a dispatch that already happened.
    """
    from audit_checks import check_substrate_declaration as adapter

    assert set(adapter.LEG_ARM_DATES) == {vs.RULE_TEARDOWN_ENUM, vs.RULE_WRITE_SCOPE_DISJOINT}
    for rule, armed in adapter.LEG_ARM_DATES.items():
        assert armed > adapter.ARM_DATE, (
            f"{rule} must arm AFTER the check itself, or it retro-gates the corpus")


def test_adapter_corpus_is_lane_contracts_only_not_every_md_in_the_directory():
    """A launch-contracts directory holds rulings and plans too; only `LANE-*.md` is a contract.

    Batch E is the witness in BOTH directions: `CUT.md` (a ruling) was REFUSED for declaring no
    substrate, and `PLAN.md` PASSED because its lane list quotes `substrate: LOCAL` inside a
    fenced block. Neither file is a lane.
    """
    from audit_checks import check_substrate_declaration as adapter

    audits = vs.repo_root() / adapter.AUDITS_RELPATH
    if not audits.is_dir():                      # child-repo-safe, same as the check itself
        pytest.skip("no docs/audits/ in this repo")
    names = {p.name for p in adapter._corpus(audits)}
    assert names, "the corpus must not be empty on the hub"
    assert all(n.startswith("LANE-") for n in names), sorted(n for n in names
                                                            if not n.startswith("LANE-"))
    assert "CUT.md" not in names and "PLAN.md" not in names
