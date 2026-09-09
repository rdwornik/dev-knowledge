"""The Ch8 extraction map resolves, refuses, and has no dead entries.

The load-bearing tests here are the REFUSAL ones. `seat_ch8` exists so a seat boot is never
composed by hand, and the way that guarantee dies quietly is an extractor that guesses past a
stale or ambiguous anchor and emits a plausible-looking paste quoting the wrong paragraph. Each
test below removes one way of guessing.
"""
from __future__ import annotations

import pytest

import seat_ch8


# --- the map resolves against the LIVE chapter ------------------------------------------------

def test_every_declared_anchor_resolves_in_the_live_playbook():
    """The whole point: the map is only true of the Ch8 that is actually on disk."""
    for key in seat_ch8.BLOCKS:
        body = seat_ch8.extract(key)
        assert body.strip(), f"block {key!r} extracted empty"


def test_every_block_starts_at_its_own_anchor_and_stops_before_its_terminator():
    text = seat_ch8.playbook_text()
    for key, block in seat_ch8.BLOCKS.items():
        body = seat_ch8.extract(key, text)
        head = body.splitlines()[0]
        if not block.rewritten:
            assert head.startswith(block.start), f"{key}: body does not open on its start anchor"
        assert not any(line.startswith(block.end) for line in body.splitlines()), (
            f"{key}: the terminator leaked into the body"
        )


def test_every_seat_reads_at_least_one_block_and_the_enum_is_complete():
    assert set(seat_ch8.SEATS) == set(seat_ch8.SEAT_BLOCKS)
    text = seat_ch8.playbook_text()
    for seat in seat_ch8.SEATS:
        sections = seat_ch8.seat_sections(seat, text)
        assert sections, f"seat {seat!r} reads nothing"
        for label, body in sections:
            assert label.startswith("[") and body.strip()


def test_no_block_is_declared_and_then_read_by_nobody():
    """A dead map entry is doctrine that renders nowhere -- and reads as if it reached a seat."""
    read = {key for keys in seat_ch8.SEAT_BLOCKS.values() for key in keys}
    assert set(seat_ch8.BLOCKS) - read == set()


# --- REFUSALS ---------------------------------------------------------------------------------

def test_ambiguous_start_anchor_refuses_rather_than_taking_the_first_hit():
    doubled = "\n".join([
        seat_ch8.CHAPTER_HEADING,
        "**Twice.** first",
        "",
        "**Twice.** second",
        "",
        "**End.**",
        "## Ch9. Next",
    ])
    block = seat_ch8.Block(title="t", start="**Twice.**", end="**End.**")
    with pytest.MonkeyPatch.context() as mp:
        mp.setitem(seat_ch8.BLOCKS, "_probe", block)
        with pytest.raises(seat_ch8.ExtractionError, match="matches 2 lines"):
            seat_ch8.extract("_probe", doubled)


def test_absent_start_anchor_refuses():
    chapter = f"{seat_ch8.CHAPTER_HEADING}\n\nnothing here\n\n## Ch9. Next\n"
    block = seat_ch8.Block(title="t", start="**Gone.**", end="**End.**")
    with pytest.MonkeyPatch.context() as mp:
        mp.setitem(seat_ch8.BLOCKS, "_probe", block)
        with pytest.raises(seat_ch8.ExtractionError, match="matches no line"):
            seat_ch8.extract("_probe", chapter)


def test_absent_end_anchor_refuses_rather_than_running_to_the_end_of_the_chapter():
    chapter = f"{seat_ch8.CHAPTER_HEADING}\n\n**Here.** body\n\n## Ch9. Next\n"
    block = seat_ch8.Block(title="t", start="**Here.**", end="**Never.**")
    with pytest.MonkeyPatch.context() as mp:
        mp.setitem(seat_ch8.BLOCKS, "_probe", block)
        with pytest.raises(seat_ch8.ExtractionError, match="no terminator"):
            seat_ch8.extract("_probe", chapter)


def test_end_anchor_takes_the_first_hit_after_the_start_even_when_it_recurs():
    """A terminator is not an identity -- `#### Honest limits` legitimately recurs in Ch8."""
    chapter = "\n".join([
        seat_ch8.CHAPTER_HEADING, "", "**Here.** body", "#### End", "later",
        "#### End", "## Ch9. Next",
    ])
    block = seat_ch8.Block(title="t", start="**Here.**", end="#### End")
    with pytest.MonkeyPatch.context() as mp:
        mp.setitem(seat_ch8.BLOCKS, "_probe", block)
        assert seat_ch8.extract("_probe", chapter) == "**Here.** body"


def test_unknown_block_and_unknown_seat_both_refuse():
    with pytest.raises(seat_ch8.ExtractionError, match="not a declared block"):
        seat_ch8.extract("no-such-block")
    with pytest.raises(seat_ch8.ExtractionError, match="not a declared seat"):
        seat_ch8.seat_sections("no-such-seat")


def test_chapter_heading_must_resolve_exactly_once():
    with pytest.raises(seat_ch8.ExtractionError, match="matched 0 times"):
        seat_ch8.chapter_text("# no chapter here\n")
    twice = f"{seat_ch8.CHAPTER_HEADING}\na\n## Ch9. x\n{seat_ch8.CHAPTER_HEADING}\nb\n"
    with pytest.raises(seat_ch8.ExtractionError, match="matched 2 times"):
        seat_ch8.chapter_text(twice)


def test_chapter_slice_stops_at_the_next_chapter():
    text = f"# top\n{seat_ch8.CHAPTER_HEADING}\nmine\n## Ch9. Next\nnot mine\n"
    sliced = seat_ch8.chapter_text(text)
    assert "mine" in sliced and "not mine" not in sliced


# --- the ONE declared transform ---------------------------------------------------------------

def test_the_prompts_dir_placeholder_is_rewritten_only_in_blocks_that_declare_it():
    """AMEND-BATCH-V-002 section 3(b): the generator makes transport resolution structural."""
    rendered = seat_ch8.extract("dispatch-interactive")
    assert "<PROMPTS_DIR>" not in rendered
    assert "$d" in rendered
    assert seat_ch8.BLOCKS["dispatch-interactive"].rewritten is True


def test_a_verbatim_block_is_left_byte_identical_to_the_chapter():
    text = seat_ch8.playbook_text()
    chapter = seat_ch8.chapter_text(text)
    body = seat_ch8.extract("refuse-to-finish", text)
    assert body in chapter, "a VERBATIM block must appear byte-identically inside Ch8"


def test_a_rewritten_block_says_so_in_its_label_and_a_verbatim_one_says_verbatim():
    assert "VERBATIM" in seat_ch8.BLOCKS["refuse-to-finish"].label
    assert "VERBATIM" not in seat_ch8.BLOCKS["dispatch-interactive"].label
    assert "3(b)" in seat_ch8.BLOCKS["dispatch-interactive"].label
