"""Review and triage are handed PRE-ASSEMBLED inputs, RED-first (`[#675]` target 3.5).

THE TARGET, verbatim from `[#675]`'s Done-when, and the half that binds hardest is the second:

    (5) review and triage are handed pre-assembled inputs and are NOT cut -- the saving comes
    from removing assembly, never from removing the judgement step, and a median reached by
    cutting either is a false pass on this row

SO THE DANGEROUS FAILURE HERE IS A GOOD-LOOKING ONE. A packet that summarised the diff, ranked
the files by "importance", or truncated a long list would look like pre-assembly and would in
fact be a cut: the reviewer's judgement would be exercised over less than the change. Every
test below that looks paranoid is guarding that specific substitution, because it is the one
that makes the median number go down while the row it is filed under goes unmet.

WHAT ASSEMBLY ACTUALLY IS HERE, measured off the live reviewer. `/codex-review` runs
`codex-review.ps1`, which derives the diff itself from `-DiffRange`. So the diff was never the
hand-assembled part. What IS hand-assembled is the CONTEXT a reviewer needs before the diff
means anything: which clauses the lane was contracted to satisfy, what it declared it would
touch, what it actually touched, and where those two disagree.

THAT LAST ONE CLOSES A GAP THIS LANE OPENED. `[#675]` target 3.4's refusal reads DECLARED
footprints and says so as an honest limit -- a lane that writes outside its declaration is
invisible to it at dispatch. Review time is exactly when that becomes visible, and the packet
is where the comparison belongs. The lane's own stated weakness is answered by the lane's own
next target rather than left in a docstring.
"""
from __future__ import annotations

import pytest

import review_packet as rp


_CONTRACT = """# LANE lane-probe

## Dispatch

claude --bg ...

## Done-contract (immutable)

1. The lane edits `scripts/audit.py` so the thing holds.
2. A RED-first witness lands in `tests/test_audit.py`.

## Steps

1. do it **COMMIT**
"""


def _packet(changed, *, contract=_CONTRACT, handback="HANDBACK worktree-x @ abc review=codex"):
    return rp.assemble(lane="lane-probe", contract_text=contract, changed_files=changed,
                       diff_range="main..HEAD", handback=handback)


# --- the target: assembly, and only assembly --------------------------------

def test_the_packet_carries_the_DONE_CONTRACT_VERBATIM_not_a_paraphrase():
    """A reviewer judges the change against the CLAUSE. A summarised clause is a different
    standard wearing the clause's name, and the reviewer cannot tell which they were given."""
    packet = _packet(["scripts/audit.py"])

    rendered = packet.render()
    assert "The lane edits `scripts/audit.py` so the thing holds." in rendered
    assert "A RED-first witness lands in `tests/test_audit.py`." in rendered


def test_a_file_the_lane_WROTE_but_never_DECLARED_is_named_for_the_reviewer():
    """The gap `[#675]` 3.4 leaves open by construction, closed at the one moment it is
    visible. The dispatch-time refusal reads DECLARED footprints; only at review time do the
    declared and the actual sets both exist."""
    packet = _packet(["scripts/audit.py", "scripts/sneaky.py"])

    assert packet.undeclared_writes == ("scripts/sneaky.py",)
    assert "scripts/sneaky.py" in packet.render()
    assert "declared" in packet.render().lower()


def test_a_file_DECLARED_but_never_written_is_named_too():
    """The other direction, and it is not symmetric noise: a declared file left untouched is
    either an unfinished clause or a stale declaration, and both are the reviewer's business."""
    packet = _packet(["scripts/audit.py"])

    assert packet.undelivered_declarations == ("tests/test_audit.py",)
    assert "tests/test_audit.py" in packet.render()


def test_a_lane_that_did_EXACTLY_what_it_declared_says_so_rather_than_printing_nothing():
    """Silence reads as "not checked". The agreement is stated so the reviewer knows it was."""
    packet = _packet(["scripts/audit.py", "tests/test_audit.py"])

    assert packet.undeclared_writes == ()
    assert packet.undelivered_declarations == ()
    assert "matches its declaration" in packet.render()


# --- what makes this assembly rather than a cut -----------------------------

def _section(rendered: str, heading_starts: str) -> str:
    """The body under one `##` heading. The whole-document `in` check this replaces was
    VACUOUS and a truncation mutation proved it: with 400 undeclared files, every path also
    appeared in the declared-vs-actual section, so truncating the changed-file list changed
    nothing the assertion could see. A test that cannot fail is worse than no test, because it
    is counted."""
    body = rendered.split(f"## {heading_starts}", 1)[1]
    return body.split("\n## ", 1)[0]


def test_EVERY_changed_file_is_listed_and_the_list_is_NEVER_truncated():
    """The substitution target 3.5 forbids, in its most tempting form. A 400-file packet is
    unwieldy; a packet that shows 50 of them and says "and 350 more" has quietly narrowed what
    the reviewer's judgement was exercised over.

    PROVEN TO BITE: slicing `changed_files[:50]` in `render()` fails this and only this.
    """
    changed = [f"scripts/mod_{i:03d}.py" for i in range(400)]

    listed = _section(_packet(changed).render(), "Files actually changed")

    for path in changed:
        assert path in listed, f"{path} was dropped from the changed-file list"
    assert "more" not in listed, "no elision marker -- the list is whole or it is not the list"


def test_the_changed_file_list_is_whole_even_when_every_file_WAS_declared():
    """The complement of the test above, and the reason it exists: with everything declared,
    the declared-vs-actual section is empty, so the changed-file list is the ONLY place those
    paths appear. This is the case the vacuous version could never have distinguished.
    """
    changed = [f"scripts/mod_{i:03d}.py" for i in range(120)]
    contract = ("# LANE\n\n## Done-contract (immutable)\n\n"
                + "".join(f"- edits `{p}`\n" for p in changed)
                + "\n## Steps\n\n1. go\n")

    packet = _packet(changed, contract=contract)
    listed = _section(packet.render(), "Files actually changed")

    assert packet.undeclared_writes == ()
    for path in changed:
        assert path in listed, f"{path} was dropped"


def test_the_packet_does_NOT_rank_or_score_the_changed_files():
    """Ranking is a judgement, and judgement is the step this may not perform. Order is the
    input's own order, so the packet adds no opinion the reviewer might mistake for evidence."""
    changed = ["scripts/z.py", "scripts/a.py", "scripts/m.py"]

    assert _packet(changed).changed_files == tuple(changed)


def test_the_packet_does_not_SUMMARISE_the_diff_it_points_at_the_range():
    """A summary of a diff is a claim about a diff. The reviewer reads the code; the packet
    hands them the exact range to read it from."""
    packet = _packet(["scripts/audit.py"])

    assert packet.diff_range == "main..HEAD"
    assert "main..HEAD" in packet.render()


def test_a_MISSING_input_is_REFUSED_rather_than_quietly_omitted():
    """An absent section and a section with nothing in it look identical in a rendered packet.
    A reviewer handed a packet with no contract would review against nothing and report clean.
    """
    with pytest.raises(rp.PacketIncomplete, match="contract"):
        rp.assemble(lane="l", contract_text="", changed_files=["a.py"],
                    diff_range="main..HEAD", handback="HANDBACK x")

    with pytest.raises(rp.PacketIncomplete, match="changed"):
        rp.assemble(lane="l", contract_text=_CONTRACT, changed_files=[],
                    diff_range="main..HEAD", handback="HANDBACK x")


def test_a_contract_with_NO_DONE_CONTRACT_section_is_refused_not_rendered_empty():
    with pytest.raises(rp.PacketIncomplete, match="Done-contract"):
        rp.assemble(lane="l", contract_text="# LANE\n\n## Steps\n\n1. go\n",
                    changed_files=["a.py"], diff_range="main..HEAD", handback="HANDBACK x")


def test_the_HANDBACK_line_rides_the_packet_so_the_reviewer_sees_what_was_claimed():
    packet = _packet(["scripts/audit.py"], handback="HANDBACK worktree-x @ abc review=codex")

    assert "review=codex" in packet.render()


def test_the_packet_offers_NO_way_to_omit_a_section():
    """Target 3.5 enforced by absence, the same way `merge_receipt` has no `--skip`. A
    `--brief` or `--summary` flag is one flag away from a median reached by cutting review."""
    from click.testing import CliRunner

    help_text = CliRunner().invoke(rp.cli, ["--help"]).output.lower()

    for forbidden in ("--brief", "--summary", "--short", "--max-files", "--truncate"):
        assert forbidden not in help_text


# --- the thing being removed from the critical path -------------------------

def test_the_packet_records_the_footprint_it_read_so_the_comparison_is_checkable():
    packet = _packet(["scripts/audit.py"])

    assert packet.declared_footprint == ("scripts/audit.py", "tests/test_audit.py")


def test_the_footprint_is_read_by_the_SAME_organ_the_dispatch_refusal_uses():
    """Library-first, and specifically NOT a second extractor. Two organs disagreeing about
    what a contract declares would make the dispatch refusal and the review packet describe
    different lanes -- the exact class of defect this repo keeps filing."""
    import seat_refusals

    assert rp.declared_footprint_of is seat_refusals.declared_footprint


def test_the_packet_is_a_FILE_the_reviewer_is_handed_not_a_terminal_dump(tmp_path):
    """Pre-assembled means it exists before the reviewer is invoked, as an artifact they are
    given -- not something a seat pastes together at the moment of asking."""
    out = tmp_path / "REVIEW-INPUT.md"
    packet = _packet(["scripts/audit.py"])

    packet.write(out)

    assert out.read_text(encoding="utf-8") == packet.render()
