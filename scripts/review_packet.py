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
    the baseline in `actions_verdict` -- `/lane-integrate` states which it passes. The one
    exception is a range that is EMPTY, or `--merge`: there the merge commit is the ground truth
    and the range and the file list are read off it (below).

THE RANGE IS THE MERGE'S OWN (lane-l4-integrator-surface). The old formulation, `main..worktree-
<lane>`, is EMPTY BY CONSTRUCTION once the packet is assembled after the merge: main already
contains the branch, so no commit is reachable from the branch and not from main. The merge commit
against its first parent -- `<merge>^1..<merge>` -- is non-empty for exactly the same reason, since
it is what the merge brought in. `merge_range` states it, `resolve_range` swaps an empty range for
it (finding the merge as the first-parent commit whose second parent is the lane tip), and an
empty range with no merge to find is REFUSED rather than rendered.
"""
from __future__ import annotations

import logging
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Iterable, Sequence

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


def _git(repo: Path | str, *args: str) -> str:
    """One git call in `repo`; a failure raises PacketIncomplete rather than returning ''."""
    try:
        proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
    except OSError as exc:
        raise PacketIncomplete(f"git could not be run: {exc!r}") from exc
    if proc.returncode != 0:
        raise PacketIncomplete(f"git {' '.join(args)} exited {proc.returncode}: "
                               f"{proc.stderr.strip()[:200]}")
    return proc.stdout.strip()


def merge_range(repo: Path | str, merge_sha: str) -> str:
    """`<merge>^1..<merge>` -- the merge commit against its first parent.

    REFUSES a commit with fewer than two parents: a plain commit has a first parent too, and its
    `^1..` range would read as a merge's without being one."""
    full = _git(repo, "rev-parse", "--verify", f"{merge_sha}^{{commit}}")
    parents = _git(repo, "rev-list", "--parents", "-n", "1", full).split()[1:]
    if len(parents) != 2:
        raise PacketIncomplete(
            f"{merge_sha} has {len(parents)} parent(s) -- a lane merge has exactly two. A plain "
            "commit's `^1..` reads as a merge's without being one, and an octopus's `^1..` folds "
            "in every non-first-parent branch, so neither is a lane's change")
    return f"{full}^1..{full}"


def changed_in_merge(repo: Path | str, merge_sha: str) -> tuple[str, ...]:
    """Every path the merge changed relative to its first parent, in git's own order."""
    full = merge_range(repo, merge_sha).split("..")[1]
    out = _git(repo, "diff", "--name-only", f"{full}^1", full)
    return tuple(line for line in out.splitlines() if line.strip())


def _merge_of_tip(repo: Path | str, base: str, tip: str) -> str | None:
    """The first-parent merge on `base` whose second parent is `tip` (a `--no-ff` lane merge)."""
    want = _git(repo, "rev-parse", "--verify", f"{tip}^{{commit}}")
    found = []
    for line in _git(repo, "log", "--first-parent", "--merges", "--format=%H %P", base).splitlines():
        sha, *parents = line.split()
        if len(parents) >= 2 and parents[1] == want:
            found.append(sha)
    if len(found) > 1:
        raise PacketIncomplete(
            f"ambiguous: {len(found)} first-parent merges on {base!r} have {tip!r} as their second "
            f"parent ({', '.join(s[:10] for s in found)}) -- more than one merge could be the one "
            "under review; pass --merge <sha> to name it")
    return found[0] if found else None


def resolve_range(repo: Path | str, diff_range: str) -> str:
    """The range as given when it selects commits; the merge's own range when it is EMPTY.

    An empty `A..B` whose B is a merged lane tip is the old post-merge formulation -- swap it for
    the merge that brought B in. An empty range with no such merge is refused: rendering a packet
    against nothing is the false pass this module exists to prevent."""
    if ".." not in diff_range:
        return diff_range
    if _git(repo, "rev-list", diff_range):
        return diff_range
    if "..." in diff_range:  # a symmetric range has no merge to resolve to: empty is refused outright
        raise PacketIncomplete(f"the range {diff_range!r} is empty -- refusing to render a packet "
                               "against nothing")
    base, tip = diff_range.split("..", 1)
    merge = _merge_of_tip(repo, base, tip)
    if merge is None:
        raise PacketIncomplete(
            f"the range {diff_range!r} is empty and no merge commit on {base!r} has {tip!r} as "
            "its second parent -- an empty range is main already containing the branch, and there "
            "is no merge to read the change off; refusing to render a packet against nothing")
    return merge_range(repo, merge)


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

    def write(self, path: Path | str) -> Path:
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
@click.option("--range", "diff_range", default=None,
              help="the diff range the reviewer reads, e.g. main..worktree-lane-x; an EMPTY range "
                   "(the branch is already merged) is replaced by the merge's own range")
@click.option("--merge", "merge_sha", default=None,
              help="the lane's merge commit: the range is `<merge>^1..<merge>` and, unless "
                   "--changed is given, the file list is read off it. Exclusive with --range")
@click.option("--repo", default=".", type=click.Path(file_okay=False),
              help="the repository the range is read in [default: the cwd]")
@click.option("--handback", required=True, help="the lane's HANDBACK line, verbatim")
@click.option("--changed", "changed", multiple=True,
              help="a changed path; repeatable. Pass EVERY one -- this tool will not "
                   "abbreviate the list and must not be handed an abbreviated one")
@click.option("--out", required=True, type=click.Path(dir_okay=False),
              help="where to write the packet the reviewer is handed")
def cli(lane: str, contract: str, diff_range: str | None, merge_sha: str | None, repo: str,
        handback: str, changed: tuple[str, ...], out: str) -> None:
    """Assemble the reviewer's inputs into ONE file, handed over before the review starts."""
    try:
        if (diff_range is None) == (merge_sha is None):
            raise PacketIncomplete("pass exactly one of --range and --merge")
        if merge_sha is not None:
            diff_range = merge_range(repo, merge_sha)
            merge_of = merge_sha
        else:
            resolved = resolve_range(repo, diff_range)
            merge_of = resolved.split("..")[1] if resolved != diff_range else None
            if merge_of:
                logger.info("range %s is empty (the branch is merged); using the merge's own %s",
                            diff_range, resolved)
            diff_range = resolved
        if merge_of:
            # After a merge the change IS the merge commit: git's list replaces the caller's, which
            # can only be an abbreviation of it (the declared organ passes ONE placeholder).
            derived = changed_in_merge(repo, merge_of)
            if changed and tuple(changed) != derived:
                logger.info("ignoring %d caller-supplied --changed; the merge changed %d file(s)",
                            len(changed), len(derived))
            changed = derived
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
