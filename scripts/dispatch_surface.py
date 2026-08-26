#!/usr/bin/env python
"""dispatch_surface.py — R5: ONE reader for the ruled dispatch form, and the gate §V owes.

WHY THIS EXISTS. `protocols/STANDING_RULINGS.md` §V (2026-08-25) records that the hub carried
FOUR rival literal launch commands for one act, that `.claude/commands/lane-boot.md` emitted the
form Ch8 itself labels a fallback while silently dropping `--model` and `--effort`, and that
"roughly thirty consecutive browser seats failed to launch a lane. They were not uninformed;
they were informed by four sources that disagreed." Its own closing line names the remedy as
outstanding: "the drift organ that would assert every literal command in Ch8 resolves ... and
that `/lane-boot` names the ruled verb, is owed and unbuilt; until it exists these rulings bind
the seat and not the tree."

This module builds the tree-side half of that organ, and it does it by READING rather than
restating. Ch8's dispatch table is "the only place in the repository that carries a literal
launch command" — so a handoff bundle that wants to put the ruled verb in front of a seat
renders `ruled_form()` at generation time instead of carrying a fifth copy. A copy is what the
ruling was about.

HONEST LIMIT, and it is half the organ §V describes. The other half — asserting every literal
command in Ch8 actually RESOLVES via `Get-Command` on the operator's machine — is a live probe
of an L0 surface (`win-tooling`'s DispatchHelpers module) and is not buildable here: Layer 2
never executes (Critical Rule #4; ADR-28/36), and the module is not in this repo. What is built
is the half that lives in the tree: the ruled verb reaches the two point-of-use surfaces, and no
rival literal form sits beside it. A verb that agrees everywhere and resolves nowhere would pass
this gate — that is a stated gap, not a covered one.
"""
from __future__ import annotations

import re
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

# The SOLE literal-command site, by its own heading (PLAYBOOK Ch8). Anchored on the heading text
# rather than a line number: an anchor rots inside its own branch, a heading survives an edit.
PLAYBOOK_PATH = "protocols/PLAYBOOK.md"
_TABLE_HEADING = "#### The dispatch table — the SOLE literal-command site"
# The row inside it that carries the LOCAL background-lane form — the shape a batch lane uses.
_LOCAL_ROW = "**1 — LOCAL background lane**"

# The two point-of-use surfaces §V names. Both are POINTERS to Ch8 by construction; this gate
# asserts the pointer still points at the same verb the table rules.
AGREEMENT_SITES = (".claude/commands/lane-boot.md", "templates/prompt-template.md")

# Rival literal launch forms, refused inside a FENCED BLOCK only. The distinction is deliberate
# and load-bearing: §V's correction is RECORDED in the prose of both files ("this line used to
# emit a raw `claude --worktree … --bg …` form"), and a gate that refused the mention would
# force the two surfaces to delete the very history that explains why they changed. What V4
# actually rules is narrower and checkable: the raw form "does not appear in a command file or a
# template" — as a command a seat would type, which in a markdown file means inside a fence.
#
# `Dispatch-Local` is NOT a rival: V2 makes it the documented manual fallback. The version-named
# aliases are (V3 — deprecated, fully working, and not what an operator types).
_RIVAL_FORMS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"^claude\b.*--bg\b"), "raw `claude … --bg` form (§V V4 — FALLBACK-ONLY, "
                                       "documented once in Ch8 and never in a command file "
                                       "or a template)"),
    (re.compile(r"^claude\b.*--worktree\b"), "raw `claude --worktree` form (§V V4 — "
                                             "FALLBACK-ONLY)"),
    (re.compile(r"\bDispatch-CloudBrief\b"), "`Dispatch-CloudBrief` (superseded; it prints its "
                                             "own supersession notice)"),
    (re.compile(r"\bDispatch-Lane\b"), "`Dispatch-Lane` (§V V3 — a version-named alias, "
                                       "deprecated in favour of `Dispatch-Local`)"),
    (re.compile(r"\bDispatch-CloudV2\b"), "`Dispatch-CloudV2` (§V V3 — a version-named alias)"),
)


def fenced_lines(text: str) -> list[str]:
    """Every line inside a triple-backtick fence, stripped. Fences toggle on any ``` line.

    A markdown fence is where a literal command a seat TYPES lives; prose backticks are where a
    seat READS about one. The whole rival test rests on that split, so it is one function."""
    out: list[str] = []
    inside = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            inside = not inside
            continue
        if inside and line.strip():
            out.append(line.strip())
    return out


def ruled_form(repo_root: Path | None = None) -> list[str] | None:
    """The literal LOCAL-lane dispatch line(s), read LIVE from Ch8's dispatch table.

    Returns the fenced block's lines, or None when the table, the row, or its fence cannot be
    found — the caller then emits a POINTER. It never falls back to a remembered command: a
    second copy of the line is precisely the defect §V ruled on, and a stale copy that renders
    confidently is worse than a pointer that makes the seat open the table."""
    root = _REPO_ROOT if repo_root is None else Path(repo_root)
    try:
        text = (root / PLAYBOOK_PATH).read_text(encoding="utf-8")
    except OSError:
        return None
    head = text.find(_TABLE_HEADING)
    if head == -1:
        return None
    # BOUND the search to the table's own section. The LOCAL row's marker could plausibly appear
    # again later in the chapter as explanatory prose, and an unbounded `find` would then select
    # that occurrence and render whatever fence followed it as if it were the ruled command —
    # so the very drift this reader exists to detect (the row leaving the table) would render a
    # confident wrong answer instead of degrading. The section ends at the next heading of the
    # table's own level or shallower; `#####` sub-rows inside it are deliberately included.
    body = text[head + len(_TABLE_HEADING):]
    end = re.search(r"^#{1,4} ", body, re.MULTILINE)
    section = body[:end.start()] if end else body
    row = section.find(_LOCAL_ROW)
    if row == -1:
        return None
    m = re.search(r"^```[^\n]*\n(.*?)^```", section[row:], re.DOTALL | re.MULTILINE)
    if m is None:
        return None
    lines = [ln.rstrip() for ln in m.group(1).splitlines() if ln.strip()]
    return lines or None


def ruled_verb(repo_root: Path | None = None) -> str | None:
    """The lead token of the ruled LOCAL-lane form — the verb an operator types (`dispatch`)."""
    lines = ruled_form(repo_root)
    if not lines:
        return None
    first = lines[0].split()
    return first[0] if first else None


def agreement_findings(repo_root: Path | None = None) -> list[str]:
    """Every disagreement between the two point-of-use sites and Ch8's ruled verb.

    Returns a list of human-readable violation strings; [] when the surfaces agree. Two classes,
    both from §V: a site that does not NAME the ruled verb in a fence (the pointer stopped
    pointing), and a site carrying a RIVAL literal form in a fence (a fifth source to disagree
    with). Read-only."""
    root = _REPO_ROOT if repo_root is None else Path(repo_root)
    verb = ruled_verb(root)
    if verb is None:
        return [f"the ruled dispatch form is unreadable at {PLAYBOOK_PATH} "
                f"'{_TABLE_HEADING}' / '{_LOCAL_ROW}' — the SOLE literal-command site moved "
                "or was reworded; re-anchor this gate rather than removing it"]
    out: list[str] = []
    for rel in AGREEMENT_SITES:
        path = root / rel
        try:
            fenced = fenced_lines(path.read_text(encoding="utf-8"))
        except OSError:
            out.append(f"{rel}: unreadable — cannot verify it names the ruled verb `{verb}`")
            continue
        if not any(ln.split()[:1] == [verb] for ln in fenced):
            out.append(f"{rel}: no fenced line names the ruled verb `{verb}` "
                       f"({PLAYBOOK_PATH} '{_TABLE_HEADING}')")
        for line in fenced:
            for rx, why in _RIVAL_FORMS:
                if rx.search(line):
                    out.append(f"{rel}: rival literal launch form in a fenced block — {why}")
    return out
