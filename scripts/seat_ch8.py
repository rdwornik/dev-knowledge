"""seat_ch8.py -- the EXTRACTION MAP: which slice of PLAYBOOK Ch8 each seat boot is rendered from.

WHY THIS EXISTS. `SEAT-BOOT-<role>.md` is a paste an operator hands to a booting seat. Two
consecutive browser seats composed one by hand on 2026-09-08 and both were withdrawn (operator
ruling INBOX-dev-knowledge-2026-09-08-038): a composed boot is a second copy of Ch8, free to
drift from it, and thirty consecutive seats had already failed to launch a lane off sources that
disagreed. The fix is not a better hand-written paste. It is that **Ch8 is the only source** and
the boot is RENDERED from it -- so this module owns the map from seat to Ch8 slice, and nothing
downstream is allowed to type doctrine of its own.

WHAT IS DECLARED vs WHAT IS DERIVED, because the split is the whole design:
  * DECLARED here: which blocks exist, where each one starts and stops, and which seats read
    which. Those are editorial judgments about Ch8 and cannot be computed from it.
  * DERIVED at render time: every byte of the block bodies, read out of `protocols/PLAYBOOK.md`
    at the moment of the cut. No block body is stored here, in a template, or in a bundle.

ANCHORS, NOT LINE NUMBERS. A block is bounded by two literal strings that appear in Ch8, never by
a line range: Ch8 grows, and a line range silently starts quoting the wrong paragraph while
continuing to look correct. The repo's own convention says the same thing ("cite by anchor text,
not line number"). The cost of an anchor is that it must stay unique -- so `extract()` REFUSES an
anchor that matches zero times or more than once, rather than taking the first hit. An ambiguous
anchor is a defect in this map, and a render that guessed past it would be a boot paste quoting a
paragraph nobody chose.

THE ONE TRANSFORM, and why it is not hand-writing. Ch8's INTERACTIVE dispatch row carries the
literal token `<PROMPTS_DIR>` -- a placeholder written for a human at a keyboard. AMEND-BATCH-V-002
section 3(b) rules that a RENDERED boot resolves its own transport from User scope and carries
neither a placeholder nor a typed path, and says in terms that "the generator makes it
structural". So exactly one rewrite is declared here, `PLACEHOLDER_REWRITES`, applied at render
time and tested in both directions. A block that is rewritten is labelled as rewritten rather
than as VERBATIM, because a label that overstates its own fidelity is the failure this whole
module exists to end.

HONEST LIMIT. This module reads Ch8 and nothing else. It cannot tell whether a block still SAYS
what the map assumed when the block was chosen -- only that the anchors still resolve, uniquely,
in that order. A Ch8 edit that rewrites a block's meaning while leaving its first and last lines
intact renders cleanly and says something new. What catches that is a human reading the diff the
render produces, which is the point of rendering into a reviewable artifact rather than into a
chat message.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

_REPO_ROOT = _SCRIPTS.parent

#: The chapter this module is the map of. Matched as a whole line.
CHAPTER_HEADING = "## Ch8. Session boundaries"
#: Ch8 ends where the next chapter begins. Any `## ChNN.` heading terminates the slice.
_CHAPTER_PREFIX = "## Ch"

PLAYBOOK_RELPATH = "protocols/PLAYBOOK.md"

#: The ONE declared render rewrite (AMEND-BATCH-V-002 section 3(b)). `$d` is the variable every
#: rendered boot binds in its own section 0, from `[Environment]::GetEnvironmentVariable(...,
#: "User")` -- so the rendered command resolves the transport instead of asking the operator to
#: expand a placeholder by eye, which is the act 3(b) forbids.
PLACEHOLDER_REWRITES: tuple[tuple[str, str], ...] = (
    ("<PROMPTS_DIR>", "$d"),
)


class ExtractionError(RuntimeError):
    """An anchor did not resolve uniquely, in order, inside Ch8.

    A REFUSAL, not a warning: the caller gets no text at all. A render that fell back to a
    best-effort slice would emit a boot paste quoting a paragraph nobody selected, and it would
    look exactly like one that worked.
    """


@dataclass(frozen=True)
class Block:
    """One declared slice of Ch8.

    `start` is the first literal line of the block (matched as a line PREFIX, so a long
    paragraph's opening sentence is enough). `end` is the first line AFTER it, exclusive and
    matched the same way. `label` is what the rendered artifact calls the block; `rewritten`
    records whether `PLACEHOLDER_REWRITES` applies, so the label can stop saying VERBATIM the
    moment the bytes stop being verbatim.
    """

    title: str
    start: str
    end: str
    rewritten: bool = False

    @property
    def label(self) -> str:
        kind = ("FROM Ch8 -- transport-resolved per AMEND-BATCH-V-002 section 3(b)"
                if self.rewritten else "VERBATIM -- Ch8")
        return f"[{kind}: {self.title}]"


#: THE MAP. Key -> the Ch8 slice it names. Keys are stable; seats select by key below.
BLOCKS: dict[str, Block] = {
    "boundary": Block(
        title='The boundary -- LOCAL or CLOUD',
        start="- **LOCAL** if the work needs the operator's **disk**",
        end="This is the routing test the",
    ),
    "integration-is-local": Block(
        title='Integration is always LOCAL and INTERACTIVE',
        start="- **Integration is always LOCAL *and* INTERACTIVE.**",
        end="This is the routing test the",
    ),
    "layer1-routing": Block(
        title='Layer 1 -- which substrate, first match wins',
        start="##### Layer 1 ",
        end="**THE FOUR AXES, VERBATIM",
    ),
    "four-axes": Block(
        title='The four axes, verbatim',
        start="**THE FOUR AXES, VERBATIM",
        end="**Deliberately NOT a fenced block.**",
    ),
    "concurrency-ceilings": Block(
        title='Concurrency ceilings and cost, per route',
        start="**Concurrency ceilings and cost, per route.**",
        end="**The ceiling is checked at STEP 0",
    ),
    "lane-ceiling": Block(
        title='The ceiling is checked at STEP 0, and it is a REFUSAL',
        start="**The ceiling is checked at STEP 0",
        end="##### Layer 2 ",
    ),
    "dispatch-local": Block(
        title='Row 1 -- LOCAL background lane',
        start="**1 — LOCAL background lane**",
        end="**2 — CLOUD lane**",
    ),
    "dispatch-interactive": Block(
        title='Row 3 -- INTERACTIVE',
        start="**3 — INTERACTIVE** (integration, seat acts",
        end="**4 — CODESPACE**",
        rewritten=True,
    ),
    "routing-matrix": Block(
        title='Model + effort -- the routing matrix, as ruled',
        start="**The matrix, as ruled**",
        end="**AMENDMENT 2026-08-07",
    ),
    "dispatch-constants": Block(
        title='Dispatch constants',
        start="**Dispatch constants.**",
        end="**Ceremony cut, ruled in the same act",
    ),
    "reviewer-model-tally": Block(
        title="The reviewer's MODEL ID rides the tally line",
        start="**The reviewer's MODEL ID rides the tally line",
        end='**Declared collision with "Model is CC\'s pick"',
    ),
    "per-lane-requirements": Block(
        title='Per-lane requirements -- the five a lane contract carries',
        start="**Per-lane requirements — the five a lane contract carries.**",
        end="**Artifact paths in a contract are DERIVED",
    ),
    "artifact-paths-derived": Block(
        title='Artifact paths in a contract are DERIVED from the ADR-101 enum',
        start="**Artifact paths in a contract are DERIVED",
        end="**The integrator's refuse-to-finish checklist.**",
    ),
    "refuse-to-finish": Block(
        title="The integrator's refuse-to-finish checklist",
        start="**The integrator's refuse-to-finish checklist.**",
        end="`/lane-integrate` walks this list mechanically",
    ),
    "journal-anchoring": Block(
        title='JOURNAL-rides-the-branch is the anchoring law',
        start="**JOURNAL-rides-the-branch is the anchoring law.**",
        end="**The integrator's branch carries ",
    ),
    "integrator-two-commits": Block(
        title="The integrator's branch carries at least 2 commits",
        start="**The integrator's branch carries ",
        end="**The integrator's branch is `docs/…`-class",
    ),
    "integrator-branch-class": Block(
        title="The integrator's branch is docs/-class",
        start="**The integrator's branch is `docs/…`-class",
        end="**WINDOW = BATCH.**",
    ),
    "window-equals-batch": Block(
        title='WINDOW = BATCH',
        start="**WINDOW = BATCH.**",
        end="**2-touch transport, on both seams.**",
    ),
    "two-touch": Block(
        title='2-touch transport, on both seams',
        start="**2-touch transport, on both seams.**",
        end="**The two numbers, counted separately",
    ),
    "message-shapes": Block(
        title='Message shapes -- verbatim, machine-greppable',
        start="2. **MESSAGE SHAPES**",
        end="3. **AUTHORIZATION.**",
    ),
    "authorization": Block(
        title='Authorization -- a peer message carries no authority',
        start="3. **AUTHORIZATION.**",
        end="4. **WAITS.**",
    ),
    "waits": Block(
        title='Waits -- every wait has a timeout and a fallback',
        start="4. **WAITS.**",
        end="5. **IDLE SUBSCRIPTIONS**",
    ),
    "state-is-files": Block(
        title='State is files',
        start="6. **STATE IS FILES.**",
        end="7. **CARRIER.**",
    ),
    "poll-as-code": Block(
        title='Poll-as-code -- NO SEAT ENDS A TURN ON A WAIT',
        start="**Poll-as-code — NO SEAT ENDS A TURN ON A WAIT.**",
        end="#### Honest limits",
    ),
    "wave-close": Block(
        title='The wave close -- every dispatched wave ends D0-D5',
        start="**Every dispatched wave ends with the same six steps, in this order.**",
        end="**The five classifications, and the clause each answers to**",
    ),
    "handoff-prep": Block(
        title='Handoff prep for the next architect -- an index, not a restatement',
        start="A seat inheriting the architect role needs four things",
        end="**Rulings an incoming seat applies without asking:**",
    ),
}

#: WHICH SEAT READS WHICH, in render order. Five roles, per INBOX 038 and AMEND-BATCH-V-001 s1.
#: A seat's list is its whole doctrine: whatever is not here does not reach that seat's boot.
SEAT_BLOCKS: dict[str, tuple[str, ...]] = {
    "dispatcher": (
        "boundary",
        "layer1-routing",
        "four-axes",
        "concurrency-ceilings",
        "lane-ceiling",
        "dispatch-local",
        "routing-matrix",
        "dispatch-constants",
        "per-lane-requirements",
        "artifact-paths-derived",
        "two-touch",
    ),
    "integrator": (
        "integration-is-local",
        "dispatch-interactive",
        "refuse-to-finish",
        "journal-anchoring",
        "integrator-two-commits",
        "integrator-branch-class",
        "message-shapes",
    ),
    "lane": (
        "per-lane-requirements",
        "artifact-paths-derived",
        "poll-as-code",
        "waits",
        "message-shapes",
        "reviewer-model-tally",
    ),
    "filings": (
        "message-shapes",
        "authorization",
        "state-is-files",
        "poll-as-code",
        "wave-close",
    ),
    "handoff": (
        "window-equals-batch",
        "two-touch",
        "handoff-prep",
        "state-is-files",
    ),
}

#: The role enum, in a stable render order. A sixth role is a ruling, not an edit here.
SEATS: tuple[str, ...] = ("dispatcher", "integrator", "filings", "handoff", "lane")


def playbook_text(repo_root: Path | None = None) -> str:
    """The whole PLAYBOOK, read as UTF-8. One read per render; callers pass it around."""
    root = Path(repo_root) if repo_root is not None else _REPO_ROOT
    return (root / PLAYBOOK_RELPATH).read_text(encoding="utf-8")


def chapter_text(text: str) -> str:
    """The Ch8 slice of `text`, from its heading to the next `## Ch` heading.

    REFUSES when Ch8's heading is absent or appears twice -- a chapter this module cannot locate
    unambiguously is one it must not guess at, since every anchor below is scoped to the slice.
    """
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == CHAPTER_HEADING]
    if len(starts) != 1:
        raise ExtractionError(
            f"REFUSED: {CHAPTER_HEADING!r} matched {len(starts)} times in {PLAYBOOK_RELPATH}; "
            "the chapter heading must resolve exactly once"
        )
    start = starts[0]
    for i in range(start + 1, len(lines)):
        if lines[i].startswith(_CHAPTER_PREFIX):
            return "\n".join(lines[start:i])
    return "\n".join(lines[start:])


def _start_index(lines: list[str], anchor: str, *, key: str) -> int:
    """The index of the ONE line in Ch8 starting with `anchor`. Refuses on zero or many.

    The START anchor is the block's IDENTITY, so it must be unique: two paragraphs opening the
    same way means the map names a block ambiguously, and taking the first hit would quote a
    paragraph nobody chose while looking exactly like a render that worked.
    """
    hits = [i for i, line in enumerate(lines) if line.startswith(anchor)]
    if not hits:
        raise ExtractionError(
            f"REFUSED: block {key!r} start anchor {anchor!r} matches no line in Ch8 -- "
            "the chapter moved out from under this map; re-anchor it against the current text"
        )
    if len(hits) > 1:
        raise ExtractionError(
            f"REFUSED: block {key!r} start anchor {anchor!r} matches {len(hits)} lines in Ch8 "
            f"(lines {[h + 1 for h in hits]} of the chapter slice) -- an ambiguous anchor is a "
            "defect in this map, and picking the first hit would quote a paragraph nobody chose"
        )
    return hits[0]


def _end_index(lines: list[str], anchor: str, *, key: str, after: int) -> int:
    """The FIRST line strictly after `after` that starts with `anchor`. Refuses on zero.

    The END anchor is a TERMINATOR rather than an identity, so first-hit is the correct reading
    and not a shortcut: a block runs until the next thing that ends it, and a heading like
    `#### Honest limits` legitimately recurs later in the chapter under a different subsection.
    Requiring global uniqueness here would refuse well-formed maps for no gain.
    """
    for i in range(after, len(lines)):
        if lines[i].startswith(anchor):
            return i
    raise ExtractionError(
        f"REFUSED: block {key!r} end anchor {anchor!r} matches no line after its start in Ch8 -- "
        "the block has no terminator, so its extent is unknown"
    )


def extract(key: str, text: str | None = None, *, repo_root: Path | None = None) -> str:
    """The body of block `key`, read out of Ch8 and stripped of trailing blank lines.

    `PLACEHOLDER_REWRITES` is applied when the block declares `rewritten`. Every failure mode is
    a refusal carrying the anchor that failed -- see `ExtractionError`.
    """
    if key not in BLOCKS:
        raise ExtractionError(
            f"REFUSED: {key!r} is not a declared block; known blocks are "
            f"{', '.join(sorted(BLOCKS))}"
        )
    block = BLOCKS[key]
    chapter = chapter_text(text if text is not None else playbook_text(repo_root))
    lines = chapter.splitlines()
    start = _start_index(lines, block.start, key=key)
    end = _end_index(lines, block.end, key=key, after=start + 1)
    body = "\n".join(lines[start:end]).rstrip()
    if block.rewritten:
        for token, replacement in PLACEHOLDER_REWRITES:
            body = body.replace(token, replacement)
    return body


def seat_sections(seat: str, text: str | None = None,
                  *, repo_root: Path | None = None) -> list[tuple[str, str]]:
    """`(label, body)` for every block a seat reads, in declared order. Refuses an unknown seat."""
    if seat not in SEAT_BLOCKS:
        raise ExtractionError(
            f"REFUSED: {seat!r} is not a declared seat; the enum is {', '.join(SEATS)}"
        )
    source = text if text is not None else playbook_text(repo_root)
    return [(BLOCKS[key].label, extract(key, source)) for key in SEAT_BLOCKS[seat]]


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="The PLAYBOOK Ch8 extraction map -- read-only; renders nothing on its own."
    )
    ap.add_argument("--list", action="store_true",
                    help="list every declared block and the seats that read it")
    ap.add_argument("--show", metavar="KEY", help="print one block's extracted body")
    ap.add_argument("--seat", metavar="ROLE", help="print every block a seat reads")
    ap.add_argument("--check", action="store_true",
                    help="resolve every anchor against the live PLAYBOOK; non-zero on a refusal")
    args = ap.parse_args(argv)

    try:
        if args.list:
            for key, block in BLOCKS.items():
                readers = [s for s in SEATS if key in SEAT_BLOCKS[s]]
                print(f"{key}: {block.title} -- read by {', '.join(readers) or 'nobody'}")
            return 0
        if args.show:
            print(extract(args.show))
            return 0
        if args.seat:
            for label, body in seat_sections(args.seat):
                print(f"{label}\n\n{body}\n")
            return 0
        if args.check:
            for key in BLOCKS:
                extract(key)
            print(f"seat_ch8: {len(BLOCKS)} blocks resolve in Ch8; "
                  f"{len(SEATS)} seats mapped")
            return 0
    except ExtractionError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    ap.print_help()
    return 0


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    raise SystemExit(_main())
