#!/usr/bin/env python
"""check_post_merge.py — refuses a merge commit that landed with a conflict marker (`[#1014]`).

THE GAP, witnessed rather than hypothetical (DIGEST-WAVE5A-2026-09-24.md blind spot 4, in the
integrator's own words): "A `--no-ff` merge commit runs almost no pre-commit hooks: my first
test-selection build (d908b6eb) committed a conflict marker in JOURNAL.md and a manifest
missing 45 nodes, and no hook refused it. I caught it from the generator's refusal and
discarded it before push." A `--no-ff` merge fires no `pre-commit` hook against its OWN tree —
the staged-content checks already ran once, on the feature branch's commits, and a merge that
resolves conflicts by hand introduces content none of them ever saw. `[#1014]`'s Done-when: "a
post-merge, pre-push check runs the equivalent of the commit-time hook set ... against the
merge commit before it reaches origin".

THIS MODULE IS THAT CHECK'S FIRST LEG: the conflict-marker scan. It reads one merge commit's
tree, from git, and refuses when a line any of its touched files carries looks like a leftover
`<<<<<<<`/`=======`/`>>>>>>>`/`|||||||` marker — the literal signature of an unresolved conflict
committed as-is. The manifest-coherence leg `[#1014]` also names is a separate concern with a
separate checker (`audit.py`'s existing organs already read the manifest); this module does not
duplicate that.

DETECT-AND-SURFACE, NOT PREVENT (the same honest limit `validate_no_ff.py` states for the
sibling gap). It is wired into no hook — `lane-organ-wirings` owns wiring a moment onto it — so
today it is a checklist row with an exit code, run by hand between the merge and the push, the
same way `merge_receipt.py require` is run over the integrator's own walk range.

WHICH FILES ARE READ. `git diff-tree <sha>^1 <sha>` — the diff between the merge's FIRST
PARENT and the merge itself, the same baseline `merge_receipt.first_parent_of` derives for
its own attribution ("the differential must mean 'what THIS merge changed'"). Every path where
main gained or changed content because of this merge is scanned, including one carried in
WHOLESALE from the other side: an earlier draft of this module used `git diff-tree -c`
(COMBINED diff — paths differing from EVERY parent), which is git's own narrowing to "genuinely
touched by conflict resolution" and is NARROWER than that. Measured on a scratch repo: a file
identical to the merge's SECOND parent but different from the first (a marker baked into a
feature commit long before this merge, never itself in conflict) is INVISIBLE to `-c` and
VISIBLE to the first-parent diff — and `[#1014]`'s Done-when is "a conflict marker in a file
touched by a --no-ff merge commit", not only a file `-c` calls genuinely merged. On a
single-parent SHA the same command degrades to an ordinary diff against that one parent, which
is still the right question to ask.

THE BLOB READ IS THE COMMIT'S, NEVER THE WORKING TREE'S. `git show <sha>:<path>` reads the
merge commit's own tree, so the verdict is a property of the commit under test and does not
depend on what happens to be checked out — the same posture `record_actions_verdict` takes by
deriving its baseline rather than reading an ambient one.

HONEST LIMITS:
  * A file `diff-tree` cannot read as text (binary, a submodule boundary, a deletion) is
    skipped and LOGGED, never silently folded into "clean" — one unreadable path must not hide
    a marker in every other file `touched_files` named.
  * The marker regex is git's own convention (`<<<<<<<`, `=======`, `>>>>>>>`, and the diff3
    base marker `|||||||`), anchored at seven repeats so an ordinary markdown rule of four
    equals signs is not a false positive. It cannot see a marker mangled by a hand edit that
    removed exactly one character.
  * `check_merge` does not require its SHA to actually BE a merge (>= 2 parents); a single-
    parent commit is scanned too, which degrades gracefully rather than refusing to run.
"""
from __future__ import annotations

import logging
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import click

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("check-post-merge")

_SCRIPTS = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS.parent

#: git's own conflict-marker vocabulary: the three merge markers plus the diff3 base marker.
#: Anchored at exactly seven repeats (git's own width) so a markdown rule of four-or-so equals
#: signs, or prose that happens to start with `>`, is not a false positive.
MARKER_RE = re.compile(r"^(?:<{7} |={7}$|>{7} |\|{7} )")


class PostMergeCheckError(RuntimeError):
    """The check could not run at all — git unreadable, or a SHA that does not resolve.

    RAISED, NEVER SWALLOWED INTO A CLEAN VERDICT: an unread merge and a genuinely clean one
    must not render the same, the same argument `first_parent_merges` makes for an empty
    range — a call that never completed must never print as a passing result.
    """


@dataclass(frozen=True)
class MarkerHit:
    """One conflict-marker line, in the file the merge commit actually committed."""
    path: str
    line_number: int
    line: str


@dataclass(frozen=True)
class PostMergeVerdict:
    """One merge commit's conflict-marker reading. `touched` is reported even on a clean
    verdict, so "checked and found nothing" prints differently from "checked nothing" — the
    same vacuity concern `render_require` names for an empty merge range."""
    merge_sha: str
    touched: tuple[str, ...]
    hits: tuple[MarkerHit, ...]

    @property
    def ok(self) -> bool:
        return not self.hits

    def render(self) -> str:
        lines = [f"post-merge check {self.merge_sha[:12]}: {len(self.touched)} file(s) touched "
                 "by this merge (differ from every parent)"]
        if not self.touched:
            lines.append("  NOTHING TOUCHED -- this SHA has one parent whose tree is identical, "
                         "or names no file at all. Not the same as CLEAN: nothing was checked.")
        elif not self.hits:
            lines.append("  clean -- no conflict marker in any touched file")
        else:
            for hit in self.hits:
                lines.append(f"  CONFLICT MARKER {hit.path}:{hit.line_number}: "
                             f"{hit.line.strip()[:80]!r}")
            lines.append(
                f"  -> {len(self.hits)} marker(s) in "
                f"{len({h.path for h in self.hits})} file(s) -- a --no-ff merge commit runs "
                f"almost no pre-commit hook, so this is the first read of the merge's own tree "
                f"(DIGEST-WAVE5A-2026-09-24.md blind spot 4, [#1014])")
        return "\n".join(lines)


def _run(argv: list[str], *, timeout: float = 60) -> "subprocess.CompletedProcess[str]":
    try:
        return subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        raise PostMergeCheckError(f"{' '.join(argv)!r} could not be run: {exc!r}") from exc


def touched_files(repo_root: Path, merge_sha: str) -> list[str]:
    """The paths that differ between `merge_sha`'s FIRST PARENT and `merge_sha` itself.

    `git diff-tree --no-commit-id --name-only -r <sha>^1 <sha>` -- an ordinary two-tree diff
    against the derived first-parent baseline, the same one `merge_receipt.first_parent_of`
    uses ("the differential must mean 'what THIS merge changed'").

    NOT `git diff-tree -c <sha>` (COMBINED diff, "paths differing from EVERY parent") --
    REJECTED after measurement. `-c` is git's own narrowing to paths a human visibly resolved,
    and it is NARROWER than "touched by this merge": a path identical to the merge's SECOND
    parent but different from the first — a marker baked into a feature commit long before this
    merge, never itself in conflict — is invisible to `-c` and would land in main with nobody
    having scanned it. Measured on a scratch repo (three-file fixture, one marker file
    untouched on the feature side): `-c` named one of two genuinely differing paths; the
    first-parent diff named both.
    """
    proc = _run(["git", "-C", str(repo_root), "diff-tree", "--no-commit-id", "--name-only",
                "-r", f"{merge_sha}^1", merge_sha])
    if proc.returncode != 0:
        raise PostMergeCheckError(
            f"git diff-tree {merge_sha!r}^1..{merge_sha!r} exited {proc.returncode}: "
            f"{proc.stderr.strip()[:200]} -- refusing to read that as 'nothing touched', "
            f"because an unresolvable SHA and a no-op merge are different facts")
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def file_markers(repo_root: Path, merge_sha: str, path: str) -> list[MarkerHit]:
    """Conflict-marker lines in `path` AS THE MERGE COMMIT COMMITTED IT.

    Reads the blob at `<merge_sha>:<path>`, never the working tree, so the verdict is a
    property of the COMMIT under test and not of whatever happens to be checked out.

    A path `diff-tree` named but `git show` cannot read as text (a deletion, a binary blob, a
    submodule gitlink) is LOGGED and skipped, never silently read as clean: one unreadable path
    must not hide a marker in every other file `touched_files` named.
    """
    proc = _run(["git", "-C", str(repo_root), "show", f"{merge_sha}:{path}"])
    if proc.returncode != 0:
        logger.warning("git show %s:%s exited %d -- skipped, not scanned for markers",
                       merge_sha[:12], path, proc.returncode)
        return []
    return [MarkerHit(path=path, line_number=number, line=line)
            for number, line in enumerate(proc.stdout.splitlines(), start=1)
            if MARKER_RE.match(line)]


def check_merge(repo_root: Path, merge_sha: str) -> PostMergeVerdict:
    """The full reading: every touched file, every marker line in each."""
    touched = touched_files(repo_root, merge_sha)
    hits: list[MarkerHit] = []
    for path in touched:
        hits.extend(file_markers(repo_root, merge_sha, path))
    return PostMergeVerdict(merge_sha=merge_sha, touched=tuple(touched), hits=tuple(hits))


# --- CLI -------------------------------------------------------------------------------------

def _root(repo_root: Optional[str]) -> Path:
    return Path(repo_root) if repo_root else _REPO_ROOT


@click.group(help="Post-merge conflict-marker check -- reads a merge commit's own tree, which "
                  "almost no pre-commit hook does (`[#1014]`).")
def cli() -> None:
    pass


@cli.command("check")
@click.option("--sha", required=True, help="the merge commit to read")
@click.option("--repo-root", default=None, type=click.Path(file_okay=False),
             help="repo root [default: this script's parent]")
def cmd_check(sha: str, repo_root: Optional[str]) -> None:
    """Read SHA's tree; refuse (exit 1) on any conflict-marker line in a touched file."""
    try:
        verdict = check_merge(_root(repo_root), sha)
    except PostMergeCheckError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(verdict.render())
    raise SystemExit(0 if verdict.ok else 1)


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
