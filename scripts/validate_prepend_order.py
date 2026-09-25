#!/usr/bin/env python
"""validate_prepend_order.py — pre-commit GATE giving teeth to ONE heading:
`protocols/PLAYBOOK.md` Ch6 "### Order conventions" (PLAYBOOK.md:1399). Row `[#786]`.

THE HEADING declares four file classes. Two of them name specific files and are
decidable from the tree alone; those two are this gate's whole scope:

    "**Newest-first (prepend):** TOKEN-LOG, JOURNAL"
    "**Append-only, newest-first (prepend):** LESSONS -- new entries at the top of the
     Entries section, per the file's own header and ADR-29."

The other two classes ("Living (in-place updates)" and "Immutable (dated)") are NOT
enforced here -- see HONEST LIMITS below.

THE PREDICATE, in one line. With `tail(x)` = the text of `x` from its FIRST dated entry
heading onward:

        tail(staged)  must END WITH  tail(HEAD)

That single byte-exact test refuses both halves of the heading at once:
  * the APPEND-ONLY half -- any pre-existing entry that is edited, reordered or deleted
    stops being part of a contiguous suffix, so the suffix test fails; and
  * the NEWEST-FIRST half -- an entry added at the BOTTOM, or inserted between two
    existing entries, also breaks the suffix even though nothing was deleted. A naive
    "no deleted lines" gate would wave both of those through.

WHY THE TAIL AND NOT THE WHOLE FILE. Everything ABOVE the first dated heading -- the
title, the format blockquote, `> Last updated: YYYY-MM-DD`, the `---` rule -- is header,
not record. Bumping that stamp is the single most common legitimate edit to these files
(`c099e783` is one such commit), and a gate that refused it would teach `--no-verify`,
which costs more than the invariant it guards.

WHY THIS HEADING (breach history, measured, not asserted). `git log --numstat --
LESSONS.md` on this repo names three commits that rewrote a file this heading declares
append-only, each by a seat that had read the prose:
    eb08075c 2026-05-16  155+/157-  "remove non-ISO ## Entries H2 + reorder pre-convention tail"
    99a104ed 2026-05-14   20+/20-   "rewrite 9 same-day LESSONS to canonical schema + relocate to file top"
    febafcac 2026-04-28    7+/25-   "docs(lessons): standardize entry format per ESSENTIALS spec"
Before this gate the rule was carried by CLAUDE.md prose, ADR-29, this PLAYBOOK heading
and the file's own header line "Never edit old entries. Never delete." -- four prose
carriers and zero organs.

THE ADR-29 ARCHIVAL CARVE-OUT is honoured, and only in its sanctioned shape. ADR-29
amend. 2026-07-17 permits a contiguous OLDER block of `LESSONS.md` to be relocated
**byte-identically** into a dated `LESSONS-legacy-<span>.md`. So a trimmed tail is
allowed when the removed block splits at an entry boundary AND appears byte-identically
in a `LESSONS-legacy-*.md` blob in the index. A relocation that EDITS while it moves is
refused -- byte-identical is the amendment's own word, and it is what makes the
exception cheap. `logs/TOKEN-LOG.md` gets no such escape: CLAUDE.md §5 rule 1 says it
"stays strict".

BLOBS, NOT DISK. Both sides are read with `git show` (HEAD blob vs index blob), never
from the working tree. Two reasons, both load-bearing on this repo's Windows clone:
  * line endings -- a disk read under `core.autocrlf=true` returns CRLF against an LF
    HEAD blob, so every file would read as 100% rewritten and the gate would refuse
    everything; and
  * the index is what is actually being committed. A partially-staged file (`git add -p`)
    differs from disk, and the commit records the index.

SELF-MATCH HAZARD, CHECKED. A gate predicate that is satisfied merely by reading the
document that specifies it is decoration. This one cannot be: the guarded set is three
LOG files at the repo root and under `logs/`; the declaring document is
`protocols/PLAYBOOK.md`, which is not in GUARDED and is never opened. Pinned as a
property by `tests/test_validate_prepend_order.py::test_s1_*` and as behaviour by
`::test_s2_*`, so a later widening of GUARDED into `protocols/` REDs rather than
quietly making the gate tautological.

FAILURE POSTURE -- BLOCKS (exit 1 on a violation), and fails CLOSED (exit 2) on an
internal error or a vacuous invocation. Justified by PLAYBOOK Ch10: deterministic
automation is "fail-closed on any executing path". The cost of a false block here is one
`--no-verify`; the cost of a false pass is a silently rewritten institutional record,
which is the failure the three commits above already produced and which no later organ
can detect, because after the commit there is nothing left to compare against. The zone
is three files and the predicate is a suffix test, so the false-block surface is small
-- unlike a heuristic gate, this one has no approximation in it.

Run cost: three `git show` pairs and three string comparisons. Measured well under the
pre-commit budget; it does not parse markdown and builds no index.

HONEST LIMITS -- what this gate does NOT catch:
  * ONLY THE THREE REGISTERED FILES. `GUARDED` is an explicit roster, not shape
    detection. A fourth prepend-class log added later is unguarded until someone adds
    it. Deliberate: auto-discovering "files that look like dated logs" would guess, and
    a gate that guesses about which files are records is worse than one with a roster.
  * NOT THE OTHER TWO CLASSES AT THE SAME HEADING. "Immutable (dated)" -- ADRs,
    transcripts, handoffs, audits -- is out of scope here; its partial organs are the
    ADR-77 `PreToolUse` guard (`scripts/hooks/block_immutable_edits.py`, transcripts
    only, Edit/Write tools only) and `validate_hermetization` (staged ADDs). "Living"
    has no decidable content.
  * POSITION, NOT CHRONOLOGY. The gate proves a new entry sits at the TOP. It does not
    read the date in the heading, so a BACKDATED entry prepended above a newer one
    passes. Enforcing chronology would misfire on the repo's real same-day `(a)`/`(b)`
    sub-lettered JOURNAL entries.
  * NOT THE ENTRY SCHEMA. LESSONS' `### YYYY-MM-DD | source | lesson | category |
    [scope: X] | action taken` pipe-field shape is unchecked. A correctly-positioned
    entry with a malformed body passes. That is a different heading's rule
    (`protocols/SESSION_SETUP.md:196`) and would be a different gate.
  * NOTHING ABOVE THE FIRST DATED HEADING. The header block is unprotected by
    construction -- so is deleting the whole header, not just bumping its stamp.
  * SAME-BRANCH REFINEMENT IS REFUSED, and this is the limit most likely to bite.
    The comparison is index-vs-HEAD per commit, so an entry you added in commit 1 is
    "pre-existing" by commit 2: fixing your own wording in a FOLLOW-UP commit on the
    same unmerged branch is refused exactly like editing a year-old entry. The escape
    is `git commit --amend`, which is the better hygiene anyway. Measured, not
    theorised: replaying this predicate over all 136 commits touching `LESSONS.md`
    (non-merge, 134 evaluable) refuses 41, and in the MODERN era -- after the
    2026-05-16 `eb08075c` reorder that established the current newest-first shape --
    the refusals are exactly six, of which four are this pattern, all on 2026-07-16
    (`99d40d2f`, `0082ac02`, `b6e999d9`, `b3dbe25a`, the "doc-lane pass-N" chain).
    From 2026-06-02 to 2026-09-08 the gate refuses NOTHING, so the false-block rate on
    current practice is zero. The 35 older refusals are era-correct rather than wrong:
    before `eb08075c` the file appended at the BOTTOM, which the present convention
    forbids. Whether the same-branch case SHOULD be refused is an operator question,
    not a code one -- it is carried as `[#786]`'s fourth residual.
  * MERGE COMMITS ARE CARVED OUT ENTIRELY. With `MERGE_HEAD` present the gate exits 0:
    a merge's file is a combination of two tails and neither parent's tail need be a
    suffix of it. This is a real hole, and it is the same one the repo already carries
    ("a clean --no-ff merge runs zero pre-commit hooks"), so a mangling merge is not
    refused here. The merge-time half belongs to the integrator seat's review.
  * HISTORY REWRITES ARE INVISIBLE. The comparison is index-vs-HEAD at one commit. A
    rebase, `commit --amend` of an older commit, or a force-push that changes what an
    earlier commit said the file contained is not seen.
  * CLIENT-SIDE, THEREFORE BYPASSABLE. `git commit --no-verify`, an unset
    `core.hooksPath`, or a clone that never ran `pre-commit install` all disarm it.
  * THE ARCHIVAL ESCAPE CHECKS CONTAINMENT, NOT SANITY. It verifies the removed block
    appears byte-identically inside SOME `LESSONS-legacy-*.md` blob in the index. It
    does not check that the archive filename's `<span>` matches the dates moved, that
    the archive is otherwise well-formed, or that the archive file is itself append-only.
    It also requires the archive to be in the index at the same commit: a two-commit
    relocation (archive first, trim second) is refused at the trim.

Read-only / Layer-2: reads git blobs, mutates nothing. The pure decision core
(`check_prepend`) is unit-tested directly; `main` is the CLI/exit wire adapter.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass

ADR_NN = "ADR-29"
HEADING_SOURCE = "protocols/PLAYBOOK.md:1399 '### Order conventions'"

# The roster. An explicit map path -> entry-heading regex, NOT shape detection.
#
# Each file gets its OWN pattern because they genuinely differ: TOKEN-LOG's entries are
# `## YYYY-MM-DD`, the other two are `### YYYY-MM-DD`. Sharing one pattern would leave
# TOKEN-LOG with an EMPTY tail -- and an empty tail is a suffix of everything, so the
# gate would report OK on that file forever while inspecting nothing. Pinned by
# tests/test_validate_prepend_order.py::test_each_guarded_file_uses_its_own_real_heading_pattern.
GUARDED: dict[str, str] = {
    "LESSONS.md": r"^### \d{4}-\d{2}-\d{2}",
    "JOURNAL.md": r"^### \d{4}-\d{2}-\d{2}",
    "logs/TOKEN-LOG.md": r"^## \d{4}-\d{2}-\d{2}",
}

# Only LESSONS.md has the ADR-29 archival escape; TOKEN-LOG "stays strict" (CLAUDE.md
# §5 rule 1) and JOURNAL has no archival convention.
ARCHIVE_GLOBS: dict[str, str] = {"LESSONS.md": r"^LESSONS-legacy-.*\.md$"}


@dataclass(frozen=True)
class Violation:
    """A refusal. `kind` is the machine-stable class; `detail` is for the operator."""

    path: str
    kind: str
    detail: str


# --- the pure decision core ------------------------------------------------

def _tail(text: str, heading_re: str) -> str | None:
    """Text from the first dated entry heading onward, or None if there is none."""
    m = re.compile(heading_re, re.M).search(text)
    return text[m.start():] if m else None


def _entry_blocks(tail: str, heading_re: str) -> list[tuple[int, str]]:
    """[(offset, block)] for each entry in `tail`, in file order (newest first)."""
    starts = [m.start() for m in re.compile(heading_re, re.M).finditer(tail)]
    bounds = starts + [len(tail)]
    return [(starts[i], tail[starts[i]:bounds[i + 1]]) for i in range(len(starts))]


def check_prepend(
    old_text: str,
    new_text: str,
    heading_re: str,
    archive_texts: tuple[str, ...] = (),
    path: str = "",
) -> Violation | None:
    """Return a Violation, or None when the change conforms to the heading.

    `old_text` is the HEAD blob, `new_text` the staged blob, both already decoded.
    `archive_texts` are the index blobs of this file's sanctioned archive targets
    (empty for files with no archival carve-out).
    """
    old_tail = _tail(old_text, heading_re)
    if old_tail is None:
        # No pre-existing dated entries: a new file, or a log that has never had one.
        # There is no record to protect, so there is nothing to refuse.
        return None

    new_tail = _tail(new_text, heading_re)
    if new_tail is None:
        return Violation(path, "entries-erased",
                         "every dated entry was removed; the file has no entry heading left")

    if new_tail.endswith(old_tail):
        return None

    # ADR-29 escape: old_tail == kept + archived, where the split is at an entry
    # boundary, `kept` survives as a suffix of the new tail, and `archived` appears
    # BYTE-IDENTICALLY in one of this file's sanctioned archive blobs.
    if archive_texts:
        for offset, _block in _entry_blocks(old_tail, heading_re):
            archived = old_tail[offset:]
            if not archived:
                continue
            if new_tail.endswith(old_tail[:offset]) and any(archived in a for a in archive_texts):
                return None

    # Name the topmost pre-existing entry that no longer survives verbatim. When every
    # old block IS still present, the breach is ORDER rather than content.
    for _offset, block in _entry_blocks(old_tail, heading_re):
        if block not in new_tail:
            head = block.splitlines()[0][:110]
            return Violation(path, "entry-not-preserved",
                             f"a pre-existing entry was edited or deleted: {head!r}")
    return Violation(path, "not-prepended",
                     "no entry was edited, but the pre-existing entries are no longer a "
                     "contiguous block at the BOTTOM -- a new entry was appended at the "
                     "wrong end or inserted between two existing ones. This file is "
                     "newest-first prepend.")


# --- git plumbing ----------------------------------------------------------

def _git_bytes(*args: str) -> bytes | None:
    """`git <args>` stdout as raw bytes, or None when git exits non-zero."""
    r = subprocess.run(["git", *args], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def _blob(rev_path: str) -> str | None:
    """Decoded blob at `HEAD:path` / `:path` (index), or None when absent."""
    raw = _git_bytes("show", rev_path)
    return None if raw is None else raw.decode("utf-8", errors="replace")


def _index_paths() -> list[str]:
    raw = _git_bytes("ls-files", "-z")
    if raw is None:
        return []
    return [p for p in raw.decode("utf-8", errors="replace").split("\0") if p]


def _in_merge() -> bool:
    raw = _git_bytes("rev-parse", "--git-path", "MERGE_HEAD")
    if raw is None:
        return False
    from pathlib import Path
    return Path(raw.decode().strip()).exists()


def _normalize(p: str) -> str:
    return p.replace("\\", "/").removeprefix("./")


def check_path(path: str) -> Violation | None:
    heading_re = GUARDED[path]
    old = _blob(f"HEAD:{path}")
    if old is None:
        return None  # not in HEAD: a brand-new log has no record to protect
    new = _blob(f":{path}")
    if new is None:
        return Violation(path, "log-removed",
                         "the file exists in HEAD but not in the index -- an append-only "
                         "record cannot be deleted; supersede it instead")
    archives: tuple[str, ...] = ()
    pat = ARCHIVE_GLOBS.get(path)
    if pat:
        rx = re.compile(pat)
        blobs = [_blob(f":{p}") for p in _index_paths() if rx.match(p)]
        archives = tuple(b for b in blobs if b is not None)
    return check_prepend(old, new, heading_re, archives, path=path)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="validate_prepend_order.py",
        description=f"Enforce {HEADING_SOURCE} on the newest-first prepend logs.")
    ap.add_argument("paths", nargs="*", help="repo-relative paths to check")
    ap.add_argument("--all", action="store_true", help="check every registered log")
    ns = ap.parse_args(argv)

    if not ns.all and not ns.paths:
        # A validator run with no args is a vacuous pass. Refuse to be one.
        print("validate_prepend_order: refusing a vacuous run -- pass explicit paths "
              "or --all. A validator invoked with no arguments inspects nothing and "
              "reports success, which is worse than not running it.", file=sys.stderr)
        return 2

    targets = list(GUARDED) if ns.all else [
        p for p in (_normalize(x) for x in ns.paths) if p in GUARDED]
    if not targets:
        return 0  # paths were given, none of them are registered logs

    if _in_merge():
        print("validate_prepend_order: MERGE_HEAD present -- skipped (a merge's tail is "
              "a combination of two parents' tails; see the module's honest limits).")
        return 0

    try:
        violations = [v for v in (check_path(p) for p in sorted(targets)) if v is not None]
    except Exception as exc:  # fail CLOSED: a records gate that cannot evaluate refuses
        print(f"validate_prepend_order: INTERNAL ERROR ({exc!r}) -- failing closed.",
              file=sys.stderr)
        return 2

    if not violations:
        return 0

    print(f"validate_prepend_order: REFUSED -- {HEADING_SOURCE}", file=sys.stderr)
    for v in violations:
        print(f"  {v.path}: [{v.kind}] {v.detail}", file=sys.stderr)
    # Deliberately ASCII-only: this text is read off a cp1252 Windows console, where a
    # section sign or em-dash renders as a replacement char and makes a real refusal
    # look like an encoding bug.
    print("\n  These files are append-only / newest-first prepend (ADR-29; CLAUDE.md "
          "sec. 5 rule 1).\n  New entries go at the TOP of the entries region; pre-existing "
          "entries are never\n  edited, reordered or deleted. The header block above the "
          "first dated heading is\n  exempt, so a `Last updated:` bump is fine.\n"
          "  LESSONS.md only: a contiguous OLDER block may be relocated BYTE-IDENTICALLY "
          "into a\n  dated LESSONS-legacy-<span>.md staged in the same commit (ADR-29 "
          "amend. 2026-07-17).", file=sys.stderr)
    return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
