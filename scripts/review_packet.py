#!/usr/bin/env python
"""review_packet.py -- hand review and triage PRE-ASSEMBLED inputs (`[#675]` target 3.5).

THE TARGET, verbatim, and the second half binds hardest:

    (5) review and triage are handed pre-assembled inputs and are NOT cut -- the saving comes
    from removing assembly, never from removing the judgement step, and a median reached by
    cutting either is a false pass on this row

THE DANGEROUS FAILURE HERE IS A GOOD-LOOKING ONE. Summarising the diff, ranking files by
"importance", or truncating a long list all LOOK like pre-assembly and are in fact cuts: the
reviewer's judgement ends up exercised over less than the change, the merge gets faster, and
the row goes unmet while the number says it was met. So this module assembles and refuses to
abbreviate -- every changed file is listed, in the input's own order, with no score attached,
and there is no `--brief`, `--summary` or `--max-files` flag to add one. `tests/
test_review_packet.py` asserts each of those absences, so adding one is a visible act.

WHAT ASSEMBLY ACTUALLY IS, measured off the live reviewer rather than assumed. `/codex-review`
runs `codex-review.ps1`, which derives the diff itself from `-DiffRange`. The DIFF was never the
hand-assembled part. What is hand-assembled is the CONTEXT without which the diff means
nothing:

    * which clauses this lane was contracted to satisfy  (verbatim, never paraphrased)
    * what it DECLARED it would touch
    * what it ACTUALLY touched
    * where those two disagree, in both directions

THE FOURTH ITEM CLOSES A GAP THIS LANE OPENED, which is why it is here and not merely nice.
Target 3.4's dispatch refusal reads DECLARED footprints and states that as an honest limit: a
lane writing outside its declaration is invisible to it. Review time is the first moment both
sets exist, so it is where the comparison belongs. A lane's stated weakness answered by the
lane's own next target is better than the same weakness restated in a docstring.

WHY IT REFUSES RATHER THAN RENDERING AN EMPTY SECTION. An absent section and an empty one look
identical once rendered, and a reviewer handed a packet with no contract reviews against
nothing and reports clean -- a false pass produced by the tool that was supposed to help. Every
input is required; a missing one raises `PacketIncomplete` naming which.

HONEST LIMITS:

  * IT ASSEMBLES CONTEXT, IT DOES NOT REVIEW. Nothing here judges the change, and nothing here
    should: the whole point of target 3.5 is that the judgement step survives intact.
  * THE DECLARED FOOTPRINT IS ONLY AS GOOD AS THE CONTRACT. A contract that declares nothing
    produces an empty declared set, so every write reads as undeclared. That is the true
    answer, and `seat_refusals.undeclared_lanes` names the same absence at dispatch time.
  * `changed_files` IS SUPPLIED, NOT DISCOVERED. The caller owns the range, exactly as it owns
    the baseline in `actions_verdict` -- `/lane-integrate` states which it passes.
"""
from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import click

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

try:
    import seat_refusals as _sr
except ImportError:                                  # imported as `scripts.review_packet`
    from scripts import seat_refusals as _sr

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("review-packet")

#: LIBRARY-FIRST, AND SPECIFICALLY NOT A SECOND EXTRACTOR. The dispatch refusal and this packet
#: must describe the SAME lane; two organs privately deciding what a contract declares is the
#: defect class this repo keeps filing. Bound by identity so a test can assert it.
declared_footprint_of = _sr.declared_footprint


class PacketIncomplete(RuntimeError):
    """An input the reviewer needs is missing. Raised, never rendered as an empty section."""


@dataclass(frozen=True)
class ReviewPacket:
    """Everything a reviewer needs before the diff means anything. No judgement, no ranking."""
    lane: str
    diff_range: str
    handback: str
    done_contract: str
    declared_footprint: tuple[str, ...]
    changed_files: tuple[str, ...]
    undeclared_writes: tuple[str, ...]
    undelivered_declarations: tuple[str, ...]

    def render(self) -> str:
        lines = [
            f"# Review input -- {self.lane}",
            "",
            "PRE-ASSEMBLED CONTEXT, not a review. Nothing here judges the change; the judgement",
            "is yours and is not abbreviated by this file. Every changed file is listed, in the",
            "order it was supplied, with no ranking -- `[#675]` target 3.5 forbids trading",
            "review coverage for merge speed.",
            "",
            f"- diff range: `{self.diff_range}`  (read the code from here; this file does not",
            "  summarise it, because a summary of a diff is a claim about a diff)",
            f"- handback: `{self.handback}`",
            "",
            "## The clauses this lane was contracted to satisfy (VERBATIM)",
            "",
            self.done_contract.strip(),
            "",
            "## Declared footprint",
            "",
        ]
        lines += [f"- `{path}`" for path in self.declared_footprint] or ["- (none declared)"]
        lines += ["", f"## Files actually changed ({len(self.changed_files)})", ""]
        lines += [f"- `{path}`" for path in self.changed_files]
        lines += ["", "## Declared vs actual", ""]
        if self.undeclared_writes:
            lines += [
                "**WRITTEN BUT NOT DECLARED** -- the contract forbids edits outside the declared",
                "footprint, and the dispatch-time collision refusal (`[#675]` 3.4) cannot see",
                "these by construction: it reads declarations, and this is the first moment both",
                "sets exist. Each is either an undeclared write or a stale declaration.",
                "",
            ]
            lines += [f"- `{path}`" for path in self.undeclared_writes]
            lines.append("")
        if self.undelivered_declarations:
            lines += [
                "**DECLARED BUT NOT WRITTEN** -- an unfinished clause or a stale declaration;",
                "both are the reviewer's business.",
                "",
            ]
            lines += [f"- `{path}`" for path in self.undelivered_declarations]
            lines.append("")
        if not self.undeclared_writes and not self.undelivered_declarations:
            lines += ["This lane's diff **matches its declaration** exactly, in both directions.",
                      "Stated rather than left silent: silence reads as 'not checked'.", ""]
        return "\n".join(lines)

    def write(self, path: "Path | str") -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.render(), encoding="utf-8", newline="\n")
        return out


def _done_contract_section(contract_text: str) -> str:
    match = _sr._DONE_CONTRACT_RE.search(contract_text)
    if match is None:
        raise PacketIncomplete(
            "the contract carries no `## Done-contract` section, so there is no clause to "
            "review against -- a reviewer handed this would review against nothing and report "
            "clean")
    return match.group("body")


def assemble(*, lane: str, contract_text: str, changed_files: Sequence[str] | Iterable[str],
             diff_range: str, handback: str) -> ReviewPacket:
    """Build the packet. Every input is required; a missing one is named, never omitted."""
    if not contract_text.strip():
        raise PacketIncomplete("no contract text was supplied -- the clauses are the standard "
                               "the change is judged against")
    changed = tuple(changed_files)
    if not changed:
        raise PacketIncomplete("no changed files were supplied -- an empty file list and a "
                               "change that touched nothing render identically, and only one "
                               "of them is a reviewable state")
    if not diff_range.strip():
        raise PacketIncomplete("no diff range was supplied -- the reviewer needs somewhere to "
                               "read the code from")
    if not handback.strip():
        raise PacketIncomplete("no handback line was supplied -- it carries the review tally "
                               "the lane claimed")

    done_contract = _done_contract_section(contract_text)
    declared = tuple(sorted(declared_footprint_of(contract_text)))
    # NO SORTING of `changed`: the input's own order is preserved, so the packet adds no
    # opinion the reviewer might mistake for evidence.
    undeclared = tuple(path for path in changed if path not in set(declared))
    undelivered = tuple(path for path in declared if path not in set(changed))

    return ReviewPacket(lane=lane, diff_range=diff_range, handback=handback,
                        done_contract=done_contract, declared_footprint=declared,
                        changed_files=changed, undeclared_writes=undeclared,
                        undelivered_declarations=undelivered)


@click.command()
@click.option("--lane", required=True, help="the lane this review is of")
@click.option("--contract", required=True, type=click.Path(exists=True, dir_okay=False),
              help="the lane's FROZEN contract file")
@click.option("--range", "diff_range", required=True,
              help="the diff range the reviewer reads, e.g. main..worktree-lane-x")
@click.option("--handback", required=True, help="the lane's HANDBACK line, verbatim")
@click.option("--changed", "changed", multiple=True, required=True,
              help="a changed path; repeatable. Pass EVERY one -- this tool will not "
                   "abbreviate the list and must not be handed an abbreviated one")
@click.option("--out", required=True, type=click.Path(dir_okay=False),
              help="where to write the packet the reviewer is handed")
def cli(lane: str, contract: str, diff_range: str, handback: str,
        changed: tuple[str, ...], out: str) -> None:
    """Assemble the reviewer's inputs into ONE file, handed over before the review starts."""
    try:
        packet = assemble(lane=lane, contract_text=Path(contract).read_text(encoding="utf-8"),
                          changed_files=changed, diff_range=diff_range, handback=handback)
    except PacketIncomplete as exc:
        raise click.ClickException(str(exc)) from exc
    written = packet.write(out)
    logger.info("wrote %s -- %d changed file(s), %d declared, %d undeclared write(s)",
                written, len(packet.changed_files), len(packet.declared_footprint),
                len(packet.undeclared_writes))


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
