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

HONEST LIMIT, stated rather than left to be discovered. LEG C can only be computed while
the live row still matches the `body_after_sha256` the latest event recorded. Once a human
edits the row again, the pre-relocation body is no longer derivable from the working tree
and `verify` reports that event **UNPROVEN (row edited since relocation)** -- loudly, in
the summary, never as a silent pass and never as a false FAIL. Legs A, B and D still bind,
and the superseded proof stays checkable in git at the relocation commit. Earlier events on
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
        "pre-relocation digest. See that module's docstring for the four legs and for the",
        "one honest limit (a row edited after relocation reports UNPROVEN, never a false pass).",
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
    """Read a record back. Raises ValueError on anything it cannot read exactly."""
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
            cm = re.fullmatch(r"### Clause \d+\.\d+ — sha256 `([0-9a-f]{64})` \(\d+ bytes\)", line)
            if cm:
                if i + 3 >= len(lines) or lines[i + 2] != FENCE:
                    raise ValueError(f"{path.name}: clause heading at line {i + 1} is not "
                                     f"followed by a blank line and a {FENCE} fence")
                if lines[i + 4] != FENCE_END:
                    raise ValueError(f"{path.name}: clause payload at line {i + 4} is not "
                                     f"exactly one line inside the fence")
                cur["clauses"].append(lines[i + 3])
                cur["clause_sha256"].append(cm.group(1))
                i += 5
                continue
        i += 1
    if cur:
        events.append(_finish_event(path, cur))
    if not events:
        raise ValueError(f"{path.name}: no `## Event N` section found")
    return Record(path=path, task_id=task_id, row_rel=row_rel, pointer=pointer, events=events)


def _finish_event(path: Path, cur: dict) -> Event:
    for k in ("pre_sha", "pre_bytes", "post_sha", "post_bytes", "had_pointer_before"):
        if k not in cur:
            raise ValueError(f"{path.name}: event {cur['n']} is missing its `{k}` line")
    if not cur["clauses"]:
        raise ValueError(f"{path.name}: event {cur['n']} relocated no clauses")
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

    archive_dir(repo_root).mkdir(parents=True, exist_ok=True)
    write_text(rec_path, render_record(task_id, row_rel, record_rel, events))
    _set_row_body(row, after)

    # Prove the act before returning, on the bytes just written — not on the values in hand.
    check = parse_record(rec_path)
    if reconstruct_before(_row_body(row), check.events[-1], check.pointer) != before:
        raise RuntimeError(f"[#{task_id}]: post-write reconstruction did not reproduce the "
                           f"pre-relocation body — the relocation is NOT byte-identical")
    return len(before), len(after), len(run)


def verify(repo_root: Path, today: date) -> tuple[list[str], list[str]]:
    """(failures, notes). A failure is a defect; a note is a stated, non-fatal limit."""
    failures: list[str] = []
    notes: list[str] = []
    files = task_files(repo_root)
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
        if sha256(body) != latest.body_after_sha256:
            notes.append(f"{tag}: LEG C UNPROVEN — the row has been edited since event "
                         f"{latest.n} ({latest.relocated}), so the pre-relocation body is no "
                         f"longer derivable from the tree. Legs A/B/D still hold; the proof "
                         f"stays checkable in git at the relocation commit.")
        else:
            try:
                got = reconstruct_before(body, latest, rec.pointer)
            except ValueError as exc:
                failures.append(f"{tag}: LEG C reconstruction failed — {exc}")
                continue
            if sha256(got) != latest.body_before_sha256:
                failures.append(f"{tag}: LEG C reconstruction does NOT reproduce the recorded "
                                f"pre-relocation body — content was destroyed or altered")

        # LEG D — strictly shorter than the body the latest event acted on.
        if len(body.encode("utf-8")) >= latest.body_before_bytes:
            failures.append(f"{tag}: LEG D the row is {len(body.encode('utf-8'))} bytes, not "
                            f"strictly under the {latest.body_before_bytes} bytes event "
                            f"{latest.n} acted on")
    return failures, notes


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

    failures, notes = verify(_REPO_ROOT, today)
    n_rec = len(record_files(_REPO_ROOT))
    for note in notes:
        print(f"  NOTE  {note}")
    for f in failures:
        print(f"  FAIL  {f}", file=sys.stderr)
    if failures:
        print(f"archive_row_body: {len(failures)} failure(s) over {n_rec} record(s)",
              file=sys.stderr)
        return 1
    print(f"archive_row_body: OK - {n_rec} record(s), byte-identity proven "
          f"(legs A/B/C/D){f', {len(notes)} UNPROVEN note(s)' if notes else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
