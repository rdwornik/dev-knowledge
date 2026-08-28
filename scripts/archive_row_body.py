#!/usr/bin/env python
"""archive_row_body.py — [#612] doc-rot row-body ARCHIVAL: relocation, not trimming.

WHY THIS EXISTS. A backlog row accretes dated-amendment narration because that narration
has nowhere else to go, so every condense pass buys a few sessions and the ceiling comes
back. `validate_doc_rot`'s two BACKLOG arms name the debt; nothing drained it without
destroying it. `protocols/STANDING_RULINGS.md` **B1** ("trim-vs-disposition") already
measured which drain works — *"dropping the dated-amendment narration ... is the drain
that works -- that narration IS the accretion the check names"* — and sentence-level
pruning is explicitly recorded there as weak. This module performs **exactly B1's drain
without B1's loss**: the narration leaves the row byte-for-byte intact into a durable
per-row record under `tasks/archive/`, and the row keeps a path-qualified pointer.

THE DOCTRINE IN ONE LINE: **the row carries a pointer, the record carries the record.**
No row is deleted, no row is closed, no byte is rewritten. Relocation only.

--- THE UNIT OF RELOCATION -------------------------------------------------------------

A task body is ONE line of ` · `-separated clauses (`gen_task_tree.extract_body`). The
unit is therefore a CLAUSE, and the eligible set is deliberately narrow — precision over
recall, because one false relocation destroys the trust the mechanism runs on:

  * a clause is ELIGIBLE only if it carries >= 1 citation-blind PAST date (it is
    dated-amendment narration in B1's sense -- `_history_dates` is reused from
    `validate_doc_rot`, not re-implemented, so "dated" means the same thing in the
    detector and in the drain);
  * a clause carrying ANY structural marker is INELIGIBLE (`_STRUCTURAL_MARKERS`).
    `Done when:` / `refs` / `kill-candidates:` / `depends-on:` / `serialize-group:` /
    `routine:` / `review_date=` / `· DEFER` / the resolved markers are read by live
    gates and by `gen_task_tree`'s frontmatter derivation. `· DEFER` is the sharpest of
    them: `derive_status` is a SUBSTRING test on the whole row, so relocating a
    `· DEFERRED ...` clause would silently flip a deferred row to open -- content
    destroyed by a mechanism whose whole claim is that it destroys nothing;
  * only a CONTIGUOUS RUN sitting immediately before the pointer (or at the very end,
    before the first relocation) is taken. Accretion appends, so the narration is a tail;
    taking a tail run means ONE splice point, ONE pointer, and a reconstruction formula
    a reader can check by eye.

The pointer clause is always LAST and always the same text for a given row, so a second
wave over the same row is idempotent in the pointer and appends an event to the record.

--- PROOF, NOT ASSERTION ---------------------------------------------------------------

`Path.write_text` launders LF->CRLF on Windows and a `read_text` round-trip cannot detect
it, so every read and write here is `read_bytes`/`write_bytes` with an explicit strict
utf-8 decode. A claim of byte-identity made through `write_text` is not a claim.

`verify` re-derives the proof from the tree rather than trusting a recorded verdict:

  LEG A  clause-integrity      -- each stored clause hashes to its recorded sha256 and
                                  matches its recorded byte length. Durable: it holds for
                                  every event of every record forever.
  LEG B  pointer-present       -- the live row body ends with the recorded pointer clause,
                                  and carries it exactly once.
  LEG C  lossless-reconstruction -- for the LATEST event, re-splice the stored clauses back
                                  into the live body and assert the result hashes to the
                                  recorded pre-relocation digest. This is the leg that says
                                  "nothing was destroyed", and it says it about live bytes.
  LEG D  strictly-shorter      -- the live row body is strictly shorter than the body the
                                  latest event acted on. Relocation that does not reduce is
                                  a no-op dressed as work.
  LEG E  completeness          -- enumerated from the ROWS, not the records: a row carrying
                                  a pointer whose record is absent is a FAILURE. Every
                                  other leg starts at a record and asks whether its row
                                  agrees, so deleting the record -- or the whole archive
                                  directory -- would remove the only thing that could
                                  complain, and the run would report a clean empty set.
                                  A verifier that enumerates only what exists cannot
                                  detect absence.

LEG C IS ATTEMPTED UNCONDITIONALLY, and the recorded post-relocation digest only CLASSIFIES
a failure. Gating the attempt on that digest -- the first shape this took -- meant one
flipped hex character in it turned the leg off while the run still exited 0: a digest whose
only power is to disable the check that would catch its own corruption. Now the
reconstruction runs first; if it reproduces the recorded pre-relocation body the record is
PROVEN whatever the post digest says, and if it does not, the post digest decides between
*the row was legitimately edited since* (a NOTE) and *this record is inconsistent* (a FAIL).

HONEST LIMIT, stated rather than left to be discovered. LEG C can only PROVE a record while
the live row is still the one the latest event left behind. Once a human edits that row
again, the pre-relocation body is no longer derivable from the working tree, and from the
tree alone *a legitimate later edit* and *a corrupt record* are indistinguishable -- so
`verify` reports the record **UNPROVEN**, says both readings, and names git at the
relocation commit as the witness that tells them apart. Loud, in the summary, never a
silent pass and never a false FAIL; the headline counts what was PROVEN, so an all-UNPROVEN
run cannot read as a clean one. Legs A, B, D and E still bind. Earlier events on
a multi-event record are in the same position by construction: each event is exact about
the body IT acted on, so unwinding a chain of events in reverse reproduces the original row
ONLY when nothing was appended between relocations. When narration WAS appended in between
— the normal case, and the reason a second event exists at all — the chain returns every
clause of the original but not their original ORDER. That is a limit about order, never
about loss, and `test_a_chained_unwind_is_only_exact_when_nothing_was_appended_between_events`
pins it so it cannot quietly become a claim of more. This is a real gap in the standing
proof and it is the price of letting rows keep being edited; the alternative (freezing a
relocated row) would be worse.

Layer-2 / ADR-28/36: this module writes ONLY inside `tasks/` — the ADR-107 source of
truth it belongs to — and drives no state in any child repo. It is not wired into any
gate: `validate_doc_rot` stays DETECT-ONLY and a human (or the integrator's filing wave)
decides what gets relocated. After any relocation run:
`uv run --locked python scripts/gen_task_tree.py --emit-source`.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

# Same dual-import shape every sibling in scripts/ uses: run as a script the siblings are
# importable bare, imported as `scripts.*` they are not.
try:
    from scripts import gen_task_tree as _gtt
    from scripts import validate_doc_rot as _rot
except ImportError:  # pragma: no cover - exercised by the scripts/-on-sys.path entrypoint
    import gen_task_tree as _gtt
    import validate_doc_rot as _rot

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

SEP = " · "
ARCHIVE_DIRNAME = "archive"
SCHEMA = 1

# A 4-backtick fence: the payload is verbatim row prose and routinely contains inline
# single backticks and occasionally a 3-backtick run, neither of which can terminate this.
FENCE = "````text"
FENCE_END = "````"

# Clause markers that make a clause STRUCTURAL and therefore never relocatable. Each is
# read by something live; the comment names what, so a future reader can check rather than
# trust. `· DEFER` is matched WITHOUT the leading separator because `derive_status` tests
# the whole row for the substring `· DEFER` and our clause text has the separator stripped.
_STRUCTURAL_MARKERS: tuple[tuple[str, str], ...] = (
    ("done when:", "validate_backlog._DONEWHEN_RE"),
    ("refs ", "the row's evidence pointers (validate_backlog, preflight_backlog_ids)"),
    ("kill-candidates:", "check_backlog_filing"),
    ("depends-on:", "gen_task_tree.derive_depends_on / validate_backlog._DEPENDS_CLAUSE_RE"),
    ("serialize-group:", "gen_task_tree.derive_serialize_group"),
    ("routine:", "routine_consumers"),
    # The routine DECLARATION's fields are their own ` · ` clauses that follow the marker,
    # so blocking the marker clause alone is not enough (terra HIGH, 2026-08-29):
    # `check_routine_consumers._ROUTINE_FIELD_RE` reads `· consumer=` / `· consumption_path=`
    # off the row and `_ROUTINE_REQUIRED` FAILs the check when either is absent. Relocating
    # a trailing `consumption_path=...` clause out of a declared-routine row would therefore
    # break a live gate while every leg here still reported the move lossless.
    ("consumer=", "check_routine_consumers._ROUTINE_FIELD_RE / _ROUTINE_REQUIRED"),
    ("consumption_path=", "check_routine_consumers._ROUTINE_FIELD_RE / _ROUTINE_REQUIRED"),
    ("trigger=", "the routine declaration's own fields (check_routine_consumers)"),
    ("verified_by=", "the routine declaration's own fields (check_routine_consumers)"),
    ("review_date=", "validate_backlog._REVIEW_DATE_RE"),
    ("status: done", "validate_backlog._DONE_MARKER_RE"),
)
# `derive_status` tests the WHOLE row for the literal substring `· DEFER`, so the clause
# that carries the deferral is the one whose text STARTS with `DEFER` (the separator is
# stripped from clause text). Matched on the prefix rather than anywhere in the clause
# because prose routinely says "the deferral below" / "UN-DEFERRED" without being the
# marker, and blocking those would refuse exactly the narration this drain exists for.
# `relocate` re-checks `derive_status` on the resulting body regardless, as the backstop.
_DEFER_CLAUSE_PREFIX = "DEFER"
_INPLACE_RESOLVED_RE = re.compile(r"~~.+?~~|\*\*\s*(?:RESOLVED|DONE)\b")

_FM_FENCE = "---\n"
_TASK_FILE_RE = re.compile(r"^(\d+)-.*\.md$")
# A record is `<id>.md` (see `record_filename`), so `README.md` and anything else that
# wanders into the archive directory is simply not a record.
_RECORD_FILE_RE = re.compile(r"^(\d+)\.md$")


# --- byte-exact IO ----------------------------------------------------------------------

def read_text(path: Path) -> str:
    """Strict utf-8 from bytes. Never `read_text` — universal newlines hides a CRLF."""
    return path.read_bytes().decode("utf-8")


def write_text(path: Path, text: str) -> None:
    """LF-only bytes. Never `write_text` — it launders LF->CRLF on Windows, and a
    `read_text` round-trip cannot detect that it did (memory: pathlib-write-text-launders)."""
    path.write_bytes(text.encode("utf-8"))


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --- clause model -----------------------------------------------------------------------

def split_clauses(body: str) -> list[str]:
    """The row body as its ` · `-separated clauses. `SEP.join(split_clauses(b)) == b`."""
    return body.split(SEP)


def is_structural(clause: str) -> Optional[str]:
    """The reason `clause` may never be relocated, or None."""
    low = clause.lower()
    for marker, why in _STRUCTURAL_MARKERS:
        if marker in low:
            return f"carries {marker!r} ({why})"
    if clause.startswith(_DEFER_CLAUSE_PREFIX):
        return ("is the row's `· DEFER` marker clause (gen_task_tree.derive_status reads it "
                "as a substring of the WHOLE row)")
    if _INPLACE_RESOLVED_RE.search(clause):
        return "carries an in-place RESOLVED/DONE marker (validate_backlog._INPLACE_RESOLVED_RE)"
    return None


def is_dated_narration(clause: str, today: date) -> bool:
    """True when `clause` carries >= 1 citation-blind PAST date — B1's accretion unit.

    Reuses `validate_doc_rot._history_dates`, so a date means the same thing to the drain
    as to the detector: an artifact identifier (`docs/audits/2026-08-15-...`) is a NAME,
    a future date is a re-check peg, and neither counts as inline history.
    """
    return bool(_rot._history_dates(clause, today))


def pointer_for(record_rel: str) -> str:
    """The pointer clause a relocated row carries. Path-qualified, and carries NO date.

    Path-qualified because a bare artifact filename inside a row is a doc-rot false strip
    (CLAUDE.md §4 "Resolve a locator before you act on it"; the same rule that makes
    `_ARTIFACT_DATE_RE` demand a path). Date-free so the pointer cannot itself become a
    history date and re-arm the arm it just drained.
    """
    return f"**Archived annotations:** `{record_rel}`"


def worth_relocating(before_chars: int, after_chars: int, pointer: str) -> bool:
    """Is this relocation worth the indirection it buys? A DECLARED rule, not a hunch.

    The row must save **at least what the pointer costs it**. Below that the row is paying
    more in indirection than it gains in length, and splitting a body across two files to
    save forty characters makes the corpus harder to read, not easier — which is the
    opposite of what the doc-rot surface is for. The threshold is the pointer's own length
    rather than a tuned constant so it scales with the row's filename and never goes stale
    (the [#532] lesson: a percentile ALWAYS has members, so no tuned number is a rule).

    Measured on the live tree at build time: this excludes five rows whose whole eligible
    run is shorter than their own pointer (`[#457]` +10, `[#298]` +42, `[#561]` +43,
    `[#555]` +95) and admits `[#533]` at +102 against a 96-char pointer.
    """
    return (before_chars - after_chars) >= len(pointer)


def eligible_run(body: str, pointer: Optional[str], today: date) -> list[str]:
    """The contiguous run of relocatable clauses ending just before `pointer` (or at EOL).

    Returns the clauses in row order, or `[]` when nothing is eligible. Clause 0 is never
    eligible — it carries `- [#id] [P][size] **Title**` and the row's scope prose, which is
    the row, not its narration.
    """
    parts = split_clauses(body)
    end = len(parts)
    if pointer is not None and parts and parts[-1] == pointer:
        end -= 1
    i = end
    while i > 1:  # `> 1` keeps clause 0 out of the run under every input
        c = parts[i - 1]
        if is_structural(c) or not is_dated_narration(c, today):
            break
        i -= 1
    return parts[i:end]


# --- the record -------------------------------------------------------------------------

@dataclass(frozen=True)
class Event:
    """One relocation act, self-proving against the body it acted on."""
    n: int
    relocated: str            # ISO date
    body_before_sha256: str
    body_before_bytes: int
    body_after_sha256: str
    body_after_bytes: int
    had_pointer_before: bool
    clauses: list[str]
    clause_sha256: list[str]


@dataclass(frozen=True)
class Record:
    path: Path
    task_id: int
    row_rel: str
    pointer: str
    events: list[Event]


def record_filename(task_id: int) -> str:
    """`<id>.md` — the record is named by ID ALONE, and that is not a shortening.

    The obvious name is the row's own `<id>-<slug>.md`, and the first build used it. It is
    WRONG, for a reason the doc-rot suite already had a test for: a slug derived from a
    title containing a date carries a date-shaped token (`[#492]`'s slug ends
    `...-2026-08-07-mea`), and putting that filename inside the row as a pointer feeds
    `validate_doc_rot._ARTIFACT_DATE_RE`'s bare-bundle-name alternative a token it strips
    as a citation while no such bundle exists. `test_citation_regex_strips_only_real_dated_
    artifact_identifiers` documents exactly that hazard for the one-line VIEW and pins it
    for the CANONICAL text — and a slug-named pointer would have imported the view's defect
    into the source the scanners read. Measured: it did, and that test caught it.

    An id is unique by construction (ADR-107 §6.3's allocation ledger), so `<id>.md` is
    unambiguous, can never carry a date, and makes the shortest pointer — which matters,
    because `worth_relocating` charges the row for its pointer's length. The pairing is not
    lost: the record's `row:` frontmatter names its row path exactly.
    """
    return f"{task_id}.md"


def _fm_get(fm: str, key: str) -> Optional[str]:
    m = re.search(rf"^{re.escape(key)}: (.*)$", fm, re.MULTILINE)
    if not m:
        return None
    v = m.group(1).strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def render_record(task_id: int, row_rel: str, record_rel: str, events: list[Event]) -> str:
    """The record file text. One `````text` fence per clause — readable AND byte-exact."""
    pointer = pointer_for(record_rel)
    latest = events[-1]
    out = [
        "---",
        f'id: "[#{task_id}]"',
        f"row: {row_rel}",
        "record: row-body-archival",
        f"schema: {SCHEMA}",
        f"events: {len(events)}",
        f'pointer: "{pointer}"',
        "---",
        "",
        f"# Archived row annotations — [#{task_id}]",
        "",
        f"Dated-amendment narration relocated **verbatim** out of `{row_rel}` by",
        "`scripts/archive_row_body.py` under `[#612]`. Nothing was trimmed, summarised or",
        "rewritten; the row keeps the path-qualified pointer",
        "",
        f"> {pointer}",
        "",
        "and this file keeps the narration. Ruling **B1** (`protocols/STANDING_RULINGS.md`,",
        "\"trim-vs-disposition\") records that dropping the dated-amendment narration is the",
        "drain that works on this class — relocation is that drain performed without the loss.",
        "",
        "**Proof, re-derived not asserted.** `uv run --locked python",
        "scripts/archive_row_body.py verify` recomputes every digest below and re-splices",
        "these clauses back into the live row, asserting the result hashes to the recorded",
        "pre-relocation digest. See that module's docstring for all five legs (A-E) and for",
        "the honest limits — a row edited after relocation reports UNPROVEN rather than a",
        "false pass, and deletion is made detectable by the declared counts, not impossible.",
        "",
        f"Latest event: **{latest.body_before_bytes} bytes → {latest.body_after_bytes} bytes** "
        f"in the row body.",
        "",
    ]
    for ev in events:
        out += [
            f"## Event {ev.n} — relocated {ev.relocated}",
            "",
            f"- pre-relocation row body: `{ev.body_before_sha256}` ({ev.body_before_bytes} bytes)",
            f"- post-relocation row body: `{ev.body_after_sha256}` ({ev.body_after_bytes} bytes)",
            f"- pointer already present before this event: {str(ev.had_pointer_before).lower()}",
            f"- clauses relocated: {len(ev.clauses)}",
            "",
        ]
        for i, (c, h) in enumerate(zip(ev.clauses, ev.clause_sha256), start=1):
            out += [
                f"### Clause {ev.n}.{i} — sha256 `{h}` ({len(c.encode('utf-8'))} bytes)",
                "",
                FENCE,
                c,
                FENCE_END,
                "",
            ]
    return "\n".join(out).rstrip("\n") + "\n"


def parse_record(path: Path) -> Record:
    """Read a record back. Raises ValueError on anything it cannot read exactly.

    EVERY RENDERED FIELD IS PARSED AND CHECKED. That is not tidiness: a field rendered as
    proof but never read is decoration, and decoration is exactly what lets a record be
    quietly *shortened*. Content tampering is caught by the clause digests, but DELETION is
    a different failure — remove a whole `## Event` section, or one `### Clause` block
    inside it, and every surviving digest still matches. The declared counts (`events:` in
    the frontmatter, `clauses relocated:` per event) and the per-clause byte length are
    what make a deletion detectable, so they are compared here rather than displayed.

    HONEST LIMIT, and it is the same one `tasks/README.md` states about its own id ledger:
    this makes deletion *detectable*, not impossible. Someone who edits the counts to match
    what they removed defeats it — the durable witness against that is git, not this file.
    """
    text = read_text(path)
    if not text.startswith(_FM_FENCE):
        raise ValueError(f"{path.name}: no opening frontmatter fence")
    end = text.find("\n---\n", 1)
    if end == -1:
        raise ValueError(f"{path.name}: no closing frontmatter fence")
    fm, body = text[4:end + 1], text[end + 5:]

    raw_id = _fm_get(fm, "id") or ""
    m = re.fullmatch(r"\[#(\d+)\]", raw_id)
    if not m:
        raise ValueError(f"{path.name}: frontmatter `id` is not `[#N]` (got {raw_id!r})")
    task_id = int(m.group(1))
    row_rel = _fm_get(fm, "row")
    pointer = _fm_get(fm, "pointer")
    if not row_rel or not pointer:
        raise ValueError(f"{path.name}: frontmatter is missing `row` or `pointer`")
    if record_filename(task_id) != path.name:
        raise ValueError(f"{path.name}: frontmatter says [#{task_id}], which belongs in "
                         f"`{record_filename(task_id)}`")
    if pointer != pointer_for(f"tasks/{ARCHIVE_DIRNAME}/{path.name}"):
        raise ValueError(f"{path.name}: the recorded pointer does not name this record")
    raw_schema = _fm_get(fm, "schema")
    if raw_schema != str(SCHEMA):
        raise ValueError(f"{path.name}: schema is {raw_schema!r}, this reader speaks "
                         f"{SCHEMA}")
    raw_events = _fm_get(fm, "events")
    if raw_events is None or not raw_events.isdigit():
        raise ValueError(f"{path.name}: frontmatter `events` is missing or not a number")
    declared_events = int(raw_events)

    lines = body.split("\n")
    events: list[Event] = []
    cur: dict | None = None
    i = 0
    while i < len(lines):
        line = lines[i]
        em = re.fullmatch(r"## Event (\d+) — relocated (\d{4}-\d{2}-\d{2})", line)
        if em:
            if cur:
                events.append(_finish_event(path, cur))
            cur = {"n": int(em.group(1)), "relocated": em.group(2),
                   "clauses": [], "clause_sha256": []}
            i += 1
            continue
        if cur is not None:
            bm = re.fullmatch(r"- (pre|post)-relocation row body: `([0-9a-f]{64})` \((\d+) bytes\)",
                              line)
            if bm:
                cur[f"{bm.group(1)}_sha"] = bm.group(2)
                cur[f"{bm.group(1)}_bytes"] = int(bm.group(3))
            pm = re.fullmatch(r"- pointer already present before this event: (true|false)", line)
            if pm:
                cur["had_pointer_before"] = pm.group(1) == "true"
            dm = re.fullmatch(r"- clauses relocated: (\d+)", line)
            if dm:
                cur["declared_clauses"] = int(dm.group(1))
            cm = re.fullmatch(
                r"### Clause (\d+)\.(\d+) — sha256 `([0-9a-f]{64})` \((\d+) bytes\)", line)
            if cm:
                if i + 4 >= len(lines) or lines[i + 2] != FENCE:
                    raise ValueError(f"{path.name}: clause heading at line {i + 1} is not "
                                     f"followed by a blank line and a {FENCE} fence")
                if lines[i + 4] != FENCE_END:
                    raise ValueError(f"{path.name}: clause payload at line {i + 4} is not "
                                     f"exactly one line inside the fence")
                if int(cm.group(1)) != cur["n"]:
                    raise ValueError(f"{path.name}: clause heading at line {i + 1} claims "
                                     f"event {cm.group(1)}, but sits inside event {cur['n']}")
                if int(cm.group(2)) != len(cur["clauses"]) + 1:
                    raise ValueError(f"{path.name}: clause numbering in event {cur['n']} is "
                                     f"not contiguous at line {i + 1} (a block was removed)")
                payload = lines[i + 3]
                if len(payload.encode("utf-8")) != int(cm.group(4)):
                    raise ValueError(f"{path.name}: clause {cm.group(1)}.{cm.group(2)} is "
                                     f"{len(payload.encode('utf-8'))} bytes, its heading "
                                     f"claims {cm.group(4)}")
                cur["clauses"].append(payload)
                cur["clause_sha256"].append(cm.group(3))
                i += 5
                continue
        i += 1
    if cur:
        events.append(_finish_event(path, cur))
    if not events:
        raise ValueError(f"{path.name}: no `## Event N` section found")
    if len(events) != declared_events:
        raise ValueError(f"{path.name}: frontmatter declares {declared_events} event(s) but "
                         f"{len(events)} are present -- an event section was added or removed")
    if [e.n for e in events] != list(range(1, len(events) + 1)):
        raise ValueError(f"{path.name}: event numbering {[e.n for e in events]} is not "
                         f"1..{len(events)} -- an event section was removed or reordered")
    return Record(path=path, task_id=task_id, row_rel=row_rel, pointer=pointer, events=events)


def _finish_event(path: Path, cur: dict) -> Event:
    for k in ("pre_sha", "pre_bytes", "post_sha", "post_bytes", "had_pointer_before",
              "declared_clauses"):
        if k not in cur:
            raise ValueError(f"{path.name}: event {cur['n']} is missing its `{k}` line")
    if not cur["clauses"]:
        raise ValueError(f"{path.name}: event {cur['n']} relocated no clauses")
    if len(cur["clauses"]) != cur["declared_clauses"]:
        raise ValueError(f"{path.name}: event {cur['n']} declares {cur['declared_clauses']} "
                         f"clause(s) but {len(cur['clauses'])} are present -- a clause block "
                         f"was added or removed")
    return Event(n=cur["n"], relocated=cur["relocated"],
                 body_before_sha256=cur["pre_sha"], body_before_bytes=cur["pre_bytes"],
                 body_after_sha256=cur["post_sha"], body_after_bytes=cur["post_bytes"],
                 had_pointer_before=cur["had_pointer_before"],
                 clauses=cur["clauses"], clause_sha256=cur["clause_sha256"])


def reconstruct_before(body_after: str, ev: Event, pointer: str) -> str:
    """The pre-relocation body, re-derived from the POST body plus the stored clauses.

    `after  = head + SEP + pointer`
    `before = head + SEP + clauses[ + SEP + pointer, when one was already there]`
    """
    tail = SEP + pointer
    if not body_after.endswith(tail):
        raise ValueError("body does not end with the recorded pointer clause")
    head = body_after[: -len(tail)]
    out = head + SEP + SEP.join(ev.clauses)
    if ev.had_pointer_before:
        out += SEP + pointer
    return out


# --- tree walking -----------------------------------------------------------------------

def tasks_dir(repo_root: Path) -> Path:
    return repo_root / "tasks"


def archive_dir(repo_root: Path) -> Path:
    return tasks_dir(repo_root) / ARCHIVE_DIRNAME


def task_files(repo_root: Path) -> dict[int, Path]:
    """`{id: path}` for every row IN THE LIVE QUEUE — i.e. referenced by `manifest.json`.

    RETIRED ROWS ARE DELIBERATELY EXCLUDED, and this is not a convenience filter. A task
    file that no manifest node references is an **allocation record** (`tasks/README.md`,
    ADR-107 §6.3): it exists to keep its id spent, it is out of `BACKLOG.md` and out of
    `canonical_text`, so it contributes nothing to the doc-rot surface this drain targets —
    and rewriting a frozen ledger record to shorten a row nobody reads would be tampering
    with the one thing `tasks/` has to be trustworthy about. Measured at build time: four
    retired records (`[#71]`, `[#122]`, `[#127]`, `[#296]`) carried bodies over the row
    ceiling and were proposed by an earlier, unfiltered walk. None of them is a finding.

    `tasks/archive/` is a directory, so it never appears in a `*.md` glob of `tasks/`.
    """
    referenced: set[int] = set()
    manifest_path = tasks_dir(repo_root) / "manifest.json"
    if manifest_path.is_file():
        import json  # noqa: PLC0415 - deferred like every other sibling's optional import
        manifest = json.loads(read_text(manifest_path))
        referenced = {n["task"] for n in manifest.get("nodes", []) if "task" in n}
    out: dict[int, Path] = {}
    for p in sorted(tasks_dir(repo_root).glob("*.md")):
        m = _TASK_FILE_RE.match(p.name)
        if m and int(m.group(1)) in referenced:
            out[int(m.group(1))] = p
    return out


def record_files(repo_root: Path) -> list[Path]:
    d = archive_dir(repo_root)
    if not d.is_dir():
        return []
    return sorted((p for p in d.glob("*.md") if _RECORD_FILE_RE.match(p.name)),
                  key=lambda p: int(p.stem))


def _row_body(path: Path) -> str:
    return _gtt.extract_body(read_text(path))


def _set_row_body(path: Path, new_body: str) -> None:
    text = read_text(path)
    old = _gtt.extract_body(text)
    marker = "\n---\n\n"
    idx = text.find(marker, 1)
    write_text(path, text[: idx + len(marker)] + new_body + "\n")
    if _row_body(path) != new_body:  # pragma: no cover - defensive round-trip assertion
        raise RuntimeError(f"{path.name}: body round-trip failed after write (was {len(old)}B)")


# --- commands ---------------------------------------------------------------------------

def propose(repo_root: Path, ids: Optional[list[int]], today: date) -> list[tuple]:
    """One tuple per row with a relocatable run: (id, before, after, n_clauses, under)."""
    out = []
    existing = {r.task_id: r for r in _safe_records(repo_root)}
    for tid, path in task_files(repo_root).items():
        if ids and tid not in ids:
            continue
        body = _row_body(path)
        rec = existing.get(tid)
        ptr = rec.pointer if rec else pointer_for(
            f"tasks/{ARCHIVE_DIRNAME}/{record_filename(tid)}")
        run = eligible_run(body, ptr, today)
        if not run:
            continue
        removed = len(SEP.join(run)) + len(SEP)
        added = 0 if (rec or body.endswith(SEP + ptr)) else len(SEP) + len(ptr)
        after = len(body) - removed + added
        # `relocate` refuses anything this predicate would list but not perform, so the
        # two must agree. Stated once, in `worth_relocating`.
        if not worth_relocating(len(body), after, ptr):
            continue
        out.append((tid, len(body), after, len(run),
                    after <= _rot._BACKLOG_ROW_CEILING))
    return out


def _safe_records(repo_root: Path) -> list[Record]:
    out = []
    for p in record_files(repo_root):
        try:
            out.append(parse_record(p))
        except ValueError:
            continue
    return out


def relocate(repo_root: Path, task_id: int, today: date) -> tuple[int, int, int]:
    """Relocate one row's eligible run. Returns (before_bytes, after_bytes, n_clauses).

    Refuses — loudly, before writing anything — on every condition under which the act
    would not be a lossless strict reduction.
    """
    files = task_files(repo_root)
    if task_id not in files:
        raise ValueError(f"[#{task_id}] has no file in tasks/")
    row = files[task_id]
    row_rel = f"tasks/{row.name}"
    record_rel = f"tasks/{ARCHIVE_DIRNAME}/{record_filename(task_id)}"
    rec_path = archive_dir(repo_root) / record_filename(task_id)
    pointer = pointer_for(record_rel)

    before = _row_body(row)
    prior = parse_record(rec_path) if rec_path.is_file() else None
    if prior is not None and prior.pointer != pointer:
        raise ValueError(f"[#{task_id}]: existing record's pointer {prior.pointer!r} does not "
                         f"match the pointer this row name derives; the row was renamed — "
                         f"resolve by hand, this tool will not guess")

    had_pointer = before.endswith(SEP + pointer)
    run = eligible_run(before, pointer, today)
    if not run:
        raise ValueError(f"[#{task_id}]: no eligible dated-amendment clause run "
                         f"(nothing to relocate; this is the normal answer for a row that is "
                         f"long-and-young rather than accreted — B1/[#532])")

    parts = split_clauses(before)
    end = len(parts) - 1 if had_pointer else len(parts)
    head = SEP.join(parts[: end - len(run)])
    after = head + SEP + pointer
    if not worth_relocating(len(before), len(after), pointer):
        raise ValueError(f"[#{task_id}]: relocation saves {len(before) - len(after)} chars "
                         f"against a {len(pointer)}-char pointer, so the row would pay more "
                         f"in indirection than it gains ({len(before)} -> {len(after)}); "
                         f"refused (see worth_relocating)")
    if _gtt.derive_title(after) != _gtt.derive_title(before):
        raise ValueError(f"[#{task_id}]: relocation would change the derived title "
                         f"({_gtt.derive_title(before)!r} -> {_gtt.derive_title(after)!r}), "
                         f"which renames the task file; refused")
    if _gtt.derive_status(after) != _gtt.derive_status(before):
        raise ValueError(f"[#{task_id}]: relocation would change the derived status "
                         f"({_gtt.derive_status(before)} -> {_gtt.derive_status(after)}); refused")
    for name, fn in (("priority", _gtt.derive_priority), ("size", _gtt.derive_size),
                     ("serialize-group", _gtt.derive_serialize_group),
                     ("depends-on", _gtt.derive_depends_on)):
        if fn(after) != fn(before):
            raise ValueError(f"[#{task_id}]: relocation would change derived {name} "
                             f"({fn(before)!r} -> {fn(after)!r}); refused")

    ev = Event(n=(prior.events[-1].n + 1) if prior else 1,
               relocated=today.isoformat(),
               body_before_sha256=sha256(before), body_before_bytes=len(before.encode("utf-8")),
               body_after_sha256=sha256(after), body_after_bytes=len(after.encode("utf-8")),
               had_pointer_before=had_pointer,
               clauses=list(run), clause_sha256=[sha256(c) for c in run])
    events = (prior.events + [ev]) if prior else [ev]

    # The pointer must be UNIQUE in the resulting row, because `verify`'s leg B keys on
    # that and `reconstruct_before` splices at the row's tail. A row whose prose already
    # quotes the pointer literal (a row ABOUT this mechanism is the realistic case) would
    # be written and only then fail verification, which is a defect found one step too
    # late. Checked here, before anything is written.
    if after.count(pointer) != 1:
        raise ValueError(f"[#{task_id}]: the pointer text would occur {after.count(pointer)} "
                         f"times in the resulting row, and leg B requires exactly 1 "
                         f"(the row's own prose quotes it); refused")

    archive_dir(repo_root).mkdir(parents=True, exist_ok=True)
    rec_backup = rec_path.read_bytes() if rec_path.is_file() else None
    row_backup = row.read_bytes()
    try:
        write_text(rec_path, render_record(task_id, row_rel, record_rel, events))
        _set_row_body(row, after)
        # Prove the act on the bytes just WRITTEN — not on the values in hand.
        check = parse_record(rec_path)
        if reconstruct_before(_row_body(row), check.events[-1], check.pointer) != before:
            raise RuntimeError(f"[#{task_id}]: post-write reconstruction did not reproduce "
                               f"the pre-relocation body — the relocation is NOT "
                               f"byte-identical")
    except Exception:
        # ROLL BACK, do not leave the half-written pair behind. The post-write proof is the
        # last line of defence, so the state it rejects is exactly the state that must not
        # survive into a commit — and a partially-relocated row plus a record that does not
        # describe it is worse than no relocation at all.
        row.write_bytes(row_backup)
        if rec_backup is None:
            rec_path.unlink(missing_ok=True)
        else:
            rec_path.write_bytes(rec_backup)
        raise
    return len(before), len(after), len(run)


def rerender(repo_root: Path) -> list[int]:
    """Re-emit every record's PROSE from its own parsed content. Payload-preserving.

    A record carries explanatory prose alongside its payload, and prose goes stale -- the
    first version said "four legs" and went on saying it after LEG E landed, which is the
    exact doc-rot this whole mechanism exists to fight. Fixing that by hand across twenty
    committed records would be twenty unverifiable edits; this makes it one reproducible
    act instead.

    SAFETY IS THE POINT, not a caveat. Each record is re-rendered from what `parse_record`
    read back out of it, and the result is re-parsed and compared against what went in --
    clauses, digests, byte counts, pointer flags, dates, the row path and the pointer. Any
    difference is rolled back and raised before the next file is touched, so a rerender can
    change wording and can never change what is archived. Returns the ids that changed.
    """
    changed: list[int] = []
    for path in record_files(repo_root):
        rec = parse_record(path)
        record_rel = f"tasks/{ARCHIVE_DIRNAME}/{path.name}"
        new_text = render_record(rec.task_id, rec.row_rel, record_rel, rec.events)
        original = path.read_bytes()
        if new_text.encode("utf-8") == original:
            continue
        write_text(path, new_text)
        # The re-parse can RAISE as well as disagree — a renderer that drops a clause makes
        # the declared counts stop matching, which `parse_record` refuses outright. Both
        # outcomes must roll back, so the rollback wraps the whole round-trip rather than
        # sitting after it (caught by
        # `test_rerender_rolls_back_if_it_would_change_content`, which left a mangled
        # record on disk until this `try` existed).
        try:
            after = parse_record(path)
            if (after.task_id, after.row_rel, after.pointer, after.events) != (
                    rec.task_id, rec.row_rel, rec.pointer, rec.events):
                raise RuntimeError(f"{path.name}: rerender changed the record's CONTENT, "
                                   f"not only its prose")
        except Exception:
            path.write_bytes(original)
            raise
        changed.append(rec.task_id)
    return changed


def verify(repo_root: Path, today: date) -> tuple[list[str], list[str], int]:
    """`(failures, notes, proven)`. A failure is a defect; a note is a stated, non-fatal limit.

    `proven` is the count of records whose LEG C actually reconstructed — returned rather
    than inferred, so a caller can never render "byte-identity proven" over a set where
    nothing was proved.
    """
    failures: list[str] = []
    notes: list[str] = []
    proven = 0
    files = task_files(repo_root)

    # LEG E — COMPLETENESS, and it runs from the ROWS, not from the records. Every other
    # leg starts at a record and asks whether its row agrees, so deleting the record (or
    # the whole `tasks/archive/` directory) removes the only thing that would have
    # complained — the rows keep pointing at nothing and the run reports a clean, empty
    # set. Graded HIGH by terra (2026-08-29) for exactly that reason: a verifier that
    # enumerates only what exists cannot detect absence. This leg enumerates the live rows
    # instead, so an ORPHAN POINTER is a failure rather than a silence.
    have = {p.stem for p in record_files(repo_root)}
    for tid, path in sorted(files.items()):
        try:
            body = _row_body(path)
        except ValueError:
            continue  # the tree's own coherence gate owns malformed task files
        if pointer_for(f"tasks/{ARCHIVE_DIRNAME}/{record_filename(tid)}") in body \
                and str(tid) not in have:
            failures.append(f"tasks/{path.name}: LEG E the row points at "
                            f"`tasks/{ARCHIVE_DIRNAME}/{record_filename(tid)}`, which does "
                            f"not exist — the archived narration is GONE, not relocated")

    for p in record_files(repo_root):
        try:
            rec = parse_record(p)
        except ValueError as exc:
            failures.append(f"{p.name}: unreadable record — {exc}")
            continue
        tag = f"tasks/{ARCHIVE_DIRNAME}/{p.name}"

        # LEG A — clause integrity, every event, always.
        for ev in rec.events:
            for i, (c, h) in enumerate(zip(ev.clauses, ev.clause_sha256), start=1):
                if sha256(c) != h:
                    failures.append(f"{tag}: LEG A clause {ev.n}.{i} does not match its "
                                    f"recorded sha256")

        # Resolved from the record's OWN `row:` path, not from the live-queue map: a row
        # that is later retired leaves that map (see `task_files`) while its file — and so
        # its archived narration — stays, and a retirement must not turn a proven record
        # into a FAIL. The live-queue map is only consulted to warn about the reverse.
        row = repo_root / rec.row_rel
        if not row.is_file():
            failures.append(f"{tag}: LEG B names row `{rec.row_rel}`, which does not exist")
            continue
        if rec.task_id in files and files[rec.task_id].name != row.name:
            failures.append(f"{tag}: LEG B names `{rec.row_rel}`, but [#{rec.task_id}] lives at "
                            f"`tasks/{files[rec.task_id].name}`")
            continue
        try:
            body = _row_body(row)
        except ValueError as exc:
            failures.append(f"{tag}: LEG B row `{rec.row_rel}` is unreadable — {exc}")
            continue

        # LEG B — the pointer is present, last, and unique.
        if not body.endswith(SEP + rec.pointer):
            failures.append(f"{tag}: LEG B the row does not end with the recorded pointer")
            continue
        if body.count(rec.pointer) != 1:
            failures.append(f"{tag}: LEG B the row carries the pointer "
                            f"{body.count(rec.pointer)} times, expected exactly 1")
            continue

        latest = rec.events[-1]
        # LEG C — lossless reconstruction of the latest event, on live bytes.
        #
        # THE RECONSTRUCTION IS ATTEMPTED FIRST, ALWAYS, and the `body_after` digest is
        # only consulted to CLASSIFY a failure. Gating the attempt on that digest was the
        # shape terra graded HIGH (2026-08-29): one flipped hex character in the recorded
        # `post-relocation row body` hash turned the leg off, and the run still exited 0.
        # A digest whose only power is to disable the check that would catch its own
        # corruption is worse than no digest. Attempting first means corruption cannot buy
        # silence — the reconstruction either reproduces the recorded pre-relocation body
        # or it does not, and only then does the `body_after` digest decide whether "does
        # not" means *the row was legitimately edited* or *this record is inconsistent*.
        try:
            got = reconstruct_before(body, latest, rec.pointer)
        except ValueError as exc:  # pragma: no cover - leg B already refuses this shape
            failures.append(f"{tag}: LEG C reconstruction failed — {exc}")
            continue
        if sha256(got) == latest.body_before_sha256:
            proven += 1
        elif sha256(body) == latest.body_after_sha256:
            # The row is EXACTLY what the record says it left behind, so a failed
            # reconstruction cannot be blamed on a later edit: the record is wrong.
            failures.append(f"{tag}: LEG C reconstruction does NOT reproduce the recorded "
                            f"pre-relocation body, and the row still matches this event's "
                            f"post-relocation digest — content was destroyed or altered")
        else:
            notes.append(f"{tag}: LEG C UNPROVEN — the row no longer matches event "
                         f"{latest.n}'s ({latest.relocated}) post-relocation digest, so the "
                         f"pre-relocation body is not derivable from the tree. Either the row "
                         f"was legitimately edited since, or this record is corrupt — the two "
                         f"are indistinguishable from the tree alone; git at the relocation "
                         f"commit tells them apart. Legs A/B/D still hold.")

        # LEG D — strictly shorter than the body the latest event acted on.
        if len(body.encode("utf-8")) >= latest.body_before_bytes:
            failures.append(f"{tag}: LEG D the row is {len(body.encode('utf-8'))} bytes, not "
                            f"strictly under the {latest.body_before_bytes} bytes event "
                            f"{latest.n} acted on")
    return failures, notes, proven


# --- CLI --------------------------------------------------------------------------------

def _ids(arg: Optional[str]) -> Optional[list[int]]:
    return [int(x) for x in arg.replace(",", " ").split()] if arg else None


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="[#612] relocate dated-amendment narration out of a backlog row into a "
                    "durable per-row record under tasks/archive/, byte-identically.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("propose", help="list rows with a relocatable clause run (read-only)")
    p.add_argument("--id", help="restrict to these task ids (comma/space separated)")

    r = sub.add_parser("relocate", help="perform the relocation for one or more rows")
    r.add_argument("--id", required=True, help="task ids (comma/space separated)")

    sub.add_parser("verify", help="re-derive the byte-identity proof for every record")
    sub.add_parser("rerender", help="re-emit every record's prose from its own parsed "
                                    "content (payload-preserving; for when the explanatory "
                                    "text goes stale)")

    args = ap.parse_args(argv)
    today = date.today()

    if args.cmd == "propose":
        rows = propose(_REPO_ROOT, _ids(args.id), today)
        if not rows:
            print("archive_row_body: no row carries a relocatable dated-amendment run")
            return 0
        print(f"archive_row_body: {len(rows)} row(s) with a relocatable run "
              f"(ceiling {_rot._BACKLOG_ROW_CEILING}):")
        for tid, before, after, n, under in sorted(rows, key=lambda t: -(t[1] - t[2])):
            print(f"  [#{tid}]  {before} -> {after} chars  ({n} clause(s))  "
                  f"{'under ceiling' if under else 'STILL OVER ceiling'}")
        return 0

    if args.cmd == "relocate":
        rc = 0
        for tid in _ids(args.id) or []:
            try:
                before, after, n = relocate(_REPO_ROOT, tid, today)
            except (ValueError, RuntimeError) as exc:
                print(f"  [#{tid}]  REFUSED - {exc}", file=sys.stderr)
                rc = 1
                continue
            print(f"  [#{tid}]  {before} -> {after} chars, {n} clause(s) relocated")
        print("archive_row_body: now run "
              "`uv run --locked python scripts/gen_task_tree.py --emit-source`")
        return rc

    if args.cmd == "rerender":
        changed = rerender(_REPO_ROOT)
        print(f"archive_row_body: rerendered {len(changed)} record(s)"
              + (f": {', '.join(f'[#{i}]' for i in changed)}" if changed
                 else " - every record's prose was already current"))
        return 0

    failures, notes, proven = verify(_REPO_ROOT, today)
    n_rec = len(record_files(_REPO_ROOT))
    for note in notes:
        print(f"  NOTE  {note}")
    for f in failures:
        print(f"  FAIL  {f}", file=sys.stderr)
    if failures:
        print(f"archive_row_body: {len(failures)} failure(s) over {n_rec} record(s)",
              file=sys.stderr)
        return 1
    if not n_rec:
        # Never report a vacuous pass as proof (CLAUDE.md §10: "running validators with no
        # args -- vacuous pass"). Zero records is a true statement about an empty set, and
        # saying "byte-identity proven" about it would be a false one. LEG E is what makes
        # this line safe: an empty set with rows still pointing at records is a FAILURE, so
        # reaching here means the tree genuinely carries no relocation.
        print("archive_row_body: no records under tasks/archive/ - nothing to verify "
              "(and no row points at one -- leg E)")
        return 0
    # The headline counts what was actually PROVEN, never the number of files present.
    print(f"archive_row_body: OK - {n_rec} record(s), {proven} byte-identity PROVEN "
          f"(legs A/B/C/D/E)"
          f"{f', {len(notes)} UNPROVEN (see NOTE above)' if notes else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
