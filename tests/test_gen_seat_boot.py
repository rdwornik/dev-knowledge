"""The five SEAT-BOOT pastes render from Ch8, and probe P12 catches every way one goes stale.

P12 is the load-bearing test in this file: `test_p12_fails_when_ch8_moves_under_a_rendered_boot`
is the one INBOX-dev-knowledge-2026-09-08-038 asks for by name ("every SEAT-BOOT file in the
bundle equals a fresh render from Ch8, drift = FAIL, so a Ch8 change re-issues the pastes
automatically"). The rest close the ways a drifted bundle can look correct: a missing file, a
hand-edited file, a hand-written file with no render header.
"""
from __future__ import annotations

import pytest

import gen_seat_boot as gsb
import seat_ch8
import seat_refusals as sr

BATCH, DATE = "V", "2026-09-09"


@pytest.fixture()
def bundle(tmp_path):
    """A freshly rendered bundle -- five files, P12 clean."""
    gsb.write_bundle(tmp_path, batch=BATCH, date=DATE)
    return tmp_path


# --- the render itself --------------------------------------------------------------------------

def test_all_five_seats_render_and_the_closure_is_five_of_five(bundle):
    """INBOX 038's closure: SEAT-BOOT files in the cut bundle 0/5 -> 5/5."""
    present = sorted(p.name for p in bundle.glob("SEAT-BOOT-*.md"))
    assert present == sorted(gsb.out_name(s) for s in seat_ch8.SEATS)
    assert len(present) == 5


def test_a_rendered_boot_carries_the_ch8_regions_its_seat_declares(bundle):
    for seat in seat_ch8.SEATS:
        text = (bundle / gsb.out_name(seat)).read_text(encoding="utf-8")
        for key in seat_ch8.SEAT_BLOCKS[seat]:
            assert f"<!-- ch8:begin {key} -->" in text
            assert f"<!-- ch8:end {key} -->" in text


def test_no_rendered_boot_ships_an_unresolved_token(bundle):
    for seat in seat_ch8.SEATS:
        text = (bundle / gsb.out_name(seat)).read_text(encoding="utf-8")
        assert not gsb._LEFTOVER_TOKEN_RE.search(text)


def test_the_authoring_note_does_not_ship(bundle):
    """The `.tmpl` header explains the template, not the bundle -- same rule as gen_handoff."""
    text = (bundle / gsb.out_name("lane")).read_text(encoding="utf-8")
    assert "STRUCTURE ONLY" not in text
    assert text.startswith("# SEAT-BOOT-lane")


# --- AMEND-BATCH-V-002 §3(b): transport resolved, N -> 0 ---------------------------------------

def test_no_rendered_boot_carries_a_placeholder_or_a_typed_path(bundle):
    """The closure is N -> 0 with a render test that fails on EITHER. This is that test."""
    for seat in seat_ch8.SEATS:
        text = (bundle / gsb.out_name(seat)).read_text(encoding="utf-8")
        assert "<PROMPTS_DIR>" not in text
        for pattern, _what in gsb._FORBIDDEN_IN_RENDER:
            assert not __import__("re").search(pattern, text), f"{seat} carries {pattern}"


def test_every_rendered_boot_resolves_its_transport_from_User_scope(bundle):
    for seat in seat_ch8.SEATS:
        text = (bundle / gsb.out_name(seat)).read_text(encoding="utf-8")
        assert 'GetEnvironmentVariable("CLAUDE_PROMPTS_DIR","User")' in text


def test_the_render_REFUSES_a_boot_that_would_ship_a_placeholder(monkeypatch):
    """Disable the declared rewrite and the guard must catch what it was rewriting."""
    monkeypatch.setattr(seat_ch8, "PLACEHOLDER_REWRITES", ())
    with pytest.raises(gsb.RenderRefusal, match="PROMPTS_DIR"):
        gsb.render("integrator", batch=BATCH, date=DATE)


# --- the boots pass the refusals they teach ----------------------------------------------------

def test_every_rendered_boot_passes_the_sleeping_poll_refusal_it_carries(bundle):
    for seat in seat_ch8.SEATS:
        text = (bundle / gsb.out_name(seat)).read_text(encoding="utf-8")
        sr.refuse_sleeping_poll(text, site=gsb.out_name(seat))


def test_each_boot_carries_a_runnable_line_for_each_refusal_its_seat_runs(bundle):
    for seat in seat_ch8.SEATS:
        text = (bundle / gsb.out_name(seat)).read_text(encoding="utf-8")
        for name in sr.SEAT_REFUSALS[seat]:
            assert f"seat_refusals.py {name.replace('reviewer-mismatch', 'reviewer')}" in text, (
                f"{seat} names refusal {name} but carries no command for it"
            )


def _section(text: str, number: int) -> str:
    """One `## <n> · ...` section of a rendered boot, up to the next `## `."""
    lines = text.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith(f"## {number} "))
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end])


def test_the_dispatchers_step0_passes_the_dryrun_refusal_against_its_own_text(bundle):
    """AMEND-BATCH-V-002 §1 run against the artifact: present, LAST, covering every contract."""
    text = (bundle / gsb.out_name("dispatcher")).read_text(encoding="utf-8")
    step0 = _section(text, 2)
    assert sr.refuse_dispatcher_step0_without_dryrun(step0, contracts=["<LANE-*.md>"]) == 1


def test_the_ceiling_check_precedes_every_launch_verb_in_the_dispatcher_boot(bundle):
    """"Where the check sits is the whole mechanism" -- so the placement is asserted, not hoped."""
    text = (bundle / gsb.out_name("dispatcher")).read_text(encoding="utf-8")
    ceiling = text.index("seat_refusals.py lane-ceiling")
    launch = text.index("**1 — LOCAL background lane**")
    assert ceiling < launch


def test_the_dryrun_closes_step0_and_the_ceiling_opens_it(bundle):
    text = (bundle / gsb.out_name("dispatcher")).read_text(encoding="utf-8")
    step0 = _section(text, 2)
    assert step0.index("lane-ceiling") < step0.index("dryrun-step0")


# --- PROBE P12 ----------------------------------------------------------------------------------

def test_p12_passes_on_a_freshly_rendered_bundle(bundle):
    assert gsb.verify(bundle) == []


def test_p12_fails_when_ch8_moves_under_a_rendered_boot(tmp_path, monkeypatch):
    """The probe INBOX 038 asks for by name: a Ch8 edit re-issues the pastes, or the bundle FAILs.

    Renders against a doctored chapter, then verifies against the real one -- exactly the shape
    of "someone edited Ch8 after the bundle was cut".

    ALL FIVE drift, not only the seat whose block changed, and that is the intended granularity:
    every boot's render header carries a sha256 of the WHOLE chapter, so any Ch8 edit invalidates
    the whole set. INBOX 038 asks for "a Ch8 change re-issues the pastes automatically" -- a
    per-block digest would re-issue only the boots that happened to quote the edited paragraph
    and leave the rest asserting a chapter state that no longer exists.
    """
    real = seat_ch8.playbook_text()
    doctored = real.replace(
        "**The integrator's refuse-to-finish checklist.**",
        "**The integrator's refuse-to-finish checklist.** (an edit landed after the cut)",
        1,
    )
    assert doctored != real
    monkeypatch.setattr(seat_ch8, "playbook_text", lambda *_a, **_k: doctored)
    gsb.write_bundle(tmp_path, batch=BATCH, date=DATE)
    monkeypatch.undo()

    drift = gsb.verify(tmp_path)
    assert len(drift) == len(seat_ch8.SEATS)
    assert all("DRIFT from Ch8" in line for line in drift)
    # and the seat that quotes the edited paragraph drifts in its BODY, not only its header
    stale = (tmp_path / gsb.out_name("integrator")).read_text(encoding="utf-8")
    assert "(an edit landed after the cut)" in stale
    assert "(an edit landed after the cut)" not in gsb.render(
        "integrator", batch=BATCH, date=DATE)


def test_p12_fails_on_a_hand_edited_boot(bundle):
    victim = bundle / gsb.out_name("filings")
    victim.write_text(victim.read_text(encoding="utf-8") + "\nand one more thing\n",
                      encoding="utf-8")
    drift = gsb.verify(bundle)
    assert len(drift) == 1 and "DRIFT" in drift[0]


def test_p12_fails_on_an_absent_boot_rather_than_checking_only_what_is_there(bundle):
    (bundle / gsb.out_name("handoff")).unlink()
    drift = gsb.verify(bundle)
    assert len(drift) == 1 and "ABSENT" in drift[0]


def test_p12_fails_on_a_hand_written_boot_with_no_render_header(bundle):
    (bundle / gsb.out_name("lane")).write_text("# SEAT-BOOT-lane\n\nYou are the lane.\n",
                                               encoding="utf-8")
    drift = gsb.verify(bundle)
    assert len(drift) == 1 and "no render header" in drift[0]


def test_p12_is_not_confused_by_a_bundle_cut_on_a_different_date(tmp_path):
    """The header carries batch and date, so a re-render uses the inputs the file was made with."""
    gsb.write_bundle(tmp_path, batch="T", date="2026-01-01")
    assert gsb.verify(tmp_path) == []


# --- render refusals ------------------------------------------------------------------------------

def test_a_template_that_disagrees_with_the_map_is_REFUSED(monkeypatch):
    monkeypatch.setitem(seat_ch8.SEAT_BLOCKS, "lane",
                        seat_ch8.SEAT_BLOCKS["lane"] + ("window-equals-batch",))
    with pytest.raises(gsb.RenderRefusal, match="declared-but-unplaced"):
        gsb.render("lane", batch=BATCH, date=DATE)


def test_a_refused_render_leaves_NO_partial_set_behind(tmp_path, monkeypatch):
    """terra HIGH 2026-09-09: writing each boot as it renders leaves earlier ones on disk when a
    later seat refuses -- and the caller then reports "no boots written" about a directory that
    has three. Five files is a set: the bundle carries it, or it carries none of it."""
    real = gsb.render
    seats_seen: list[str] = []

    def explode_on_the_last_seat(seat, **kw):
        seats_seen.append(seat)
        if seat == seat_ch8.SEATS[-1]:
            raise gsb.RenderRefusal("REFUSED: contrived")
        return real(seat, **kw)

    monkeypatch.setattr(gsb, "render", explode_on_the_last_seat)
    with pytest.raises(gsb.RenderRefusal):
        gsb.write_bundle(tmp_path, batch=BATCH, date=DATE)
    assert len(seats_seen) == len(seat_ch8.SEATS), "it should render all before writing any"
    assert list(tmp_path.glob("SEAT-BOOT-*.md")) == []


def test_an_unknown_seat_and_a_missing_template_both_REFUSE(tmp_path):
    with pytest.raises(gsb.RenderRefusal, match="not a declared seat"):
        gsb.render("archivist", batch=BATCH, date=DATE)
    with pytest.raises(gsb.RenderRefusal, match="no seat template"):
        gsb.render("lane", batch=BATCH, date=DATE, repo_root=tmp_path)


def test_every_seat_has_a_template_and_a_stop_block(tmp_path):
    for seat in seat_ch8.SEATS:
        assert gsb._template_path(seat, gsb._REPO_ROOT).exists()
        assert gsb.SEAT_STOP_BLOCK[seat] in seat_ch8.BLOCKS


# --- the cut-time hook in the bundle engine ------------------------------------------------------

def test_the_cut_time_hook_writes_all_five_into_a_bundle_and_p12_passes(tmp_path):
    """`gen_handoff` gains a HOOK, not a second copy of Ch8 -- so the hook is tested as a hook."""
    import gen_handoff

    written = gen_handoff._write_seat_boots(tmp_path, gsb._REPO_ROOT, "some-slug", DATE)
    assert len(written) == len(seat_ch8.SEATS)
    assert gsb.verify(tmp_path) == []


def test_the_hook_degrades_to_no_files_rather_than_taking_down_a_cut(tmp_path, monkeypatch):
    """A refused render leaves the other bundle artifacts intact; P12 then reports the absence."""
    import gen_handoff

    monkeypatch.setattr(seat_ch8, "playbook_text",
                        lambda *_a, **_k: "# no Ch8 in this document\n")
    assert gen_handoff._write_seat_boots(tmp_path, gsb._REPO_ROOT, "some-slug", DATE) == []
    assert list(tmp_path.glob("SEAT-BOOT-*.md")) == []
    monkeypatch.undo()
    assert len(gsb.verify(tmp_path)) == len(seat_ch8.SEATS)


def test_the_batch_label_falls_back_to_the_cut_slug_when_the_manifest_is_ambiguous(monkeypatch):
    import gen_handoff

    monkeypatch.setattr(gen_handoff, "_open_batches", lambda _root: [])
    assert gen_handoff._seat_boot_batch(gsb._REPO_ROOT, "2026-09-09-cut") == "2026-09-09-cut"

    one = [type("B", (), {"batch": "V"})()]
    monkeypatch.setattr(gen_handoff, "_open_batches", lambda _root: one)
    assert gen_handoff._seat_boot_batch(gsb._REPO_ROOT, "2026-09-09-cut") == "V"

    monkeypatch.setattr(gen_handoff, "_open_batches", lambda _root: one * 2)
    assert gen_handoff._seat_boot_batch(gsb._REPO_ROOT, "2026-09-09-cut") == "2026-09-09-cut"


# --- [#737] AX22-3: the seat's model is recorded in its own render ----------------------
#
# The operator ruled the two largest Opus sinks down a tier: the dispatcher seat is mechanical
# (freeze, DryRun, fire, receipts) and runs on Sonnet; the integrator judges merge verdicts on
# Opus but runs suites and teardowns on Sonnet, which is `opusplan`. Before this, a SEAT-BOOT
# render carried no model at all, so the ruling had nowhere to live except prose that the next
# seat would have to be told about -- which is the failure the boot renders exist to end.
#
# AMENDED 2026-09-15 (lane `aa-2`). Recording the tier in the render was necessary and was not
# sufficient: the value landed in a `<!-- GENERATED -->` COMMENT, while the launch command the
# boot carried stayed Ch8 row 3's bare `claude`. A tier that reaches no flag is a decision the
# tree records and does not make, and batch Z measured the consequence -- the integrator seat ran
# 100% `claude-opus-5`, USD 82.53, 30.5% of a USD 270.72 night, under a header saying `opusplan`.
# The split now lives in `gen_seat_boot.SEAT_PHASES` and reaches a RESOLVED launch line per
# phase; `tests/test_seat_split.py` is where that is asserted. These tests keep the narrower
# claim they were written for: the render RECORDS the tier.


def test_every_rendered_boot_records_its_seat_model(bundle):
    """ASSERTED AGAINST `model_clause`, NOT `SEAT_MODELS`, and the difference is load-bearing.

    `SEAT_MODELS[seat]` is the seat's ENTRY tier. For a split seat the header names every phase,
    so asserting the entry value alone would pass on a substring -- `model: opus` is a prefix of
    `model: opus (plan) + sonnet (execute)` -- and a header that reported one of two tiers would
    sail through the check that exists to catch exactly that.
    """
    for seat in seat_ch8.SEATS:
        text = (bundle / gsb.out_name(seat)).read_text(encoding="utf-8")
        assert f"model: {gsb.model_clause(seat)} |" in text, seat


def test_the_two_seats_the_operator_retiered_carry_the_ruled_TIERS(bundle):
    """AX22-3 names these two explicitly; the others stay Opus.

    AMENDED 2026-09-15 by lane `aa-2`, and the amendment is to the ruling's MEANS, never its
    substance. AX22-3 ruled the integrator seat split -- "judges merge verdicts on Opus while
    running suites and teardowns on Sonnet" -- and named `opusplan` as how. That clause is what
    this test now asserts, in the form `SEAT_PHASES` gives it: Opus for the judging half, Sonnet
    for the mechanical one. The ruling is stated MORE precisely than before, not relaxed.

    `opusplan` is gone as the carrier because it was measured not to be one. It keys on plan
    MODE, which is not where this seat's halves divide; it is INERT on a background shape
    (`dispatch_surface.BACKGROUND_INERT_MODELS`, measured 84/84 turns on Sonnet); and at the
    integrator's own context size a per-turn split pays more in per-model cache re-writes than
    the cheaper tier saves. Batch Z is the outcome under the old carrier: the integrator seat ran
    **100% `claude-opus-5`, USD 82.53, 30.5% of the night**, under a header reading `opusplan`.
    Full rationale, kept where the map is: `gen_seat_boot.SPLIT_RATIONALE`.
    """
    assert gsb.SEAT_MODELS["dispatcher"] == "sonnet"
    judge, mechanics = gsb.SEAT_PHASES["integrator"]
    assert (judge.model, mechanics.model) == ("opus", "sonnet"), "AX22-3's substance"
    dispatcher = (bundle / gsb.out_name("dispatcher")).read_text(encoding="utf-8")
    integrator = (bundle / gsb.out_name("integrator")).read_text(encoding="utf-8")
    assert "model: sonnet" in dispatcher
    assert "model: opus (plan) + sonnet (execute)" in integrator
    assert "model: opusplan" not in integrator


def test_the_seat_model_map_covers_every_declared_seat(bundle):
    """A seat added to the enum without a model would render an unresolved one."""
    assert set(gsb.SEAT_MODELS) == set(seat_ch8.SEATS)
