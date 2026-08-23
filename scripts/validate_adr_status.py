#!/usr/bin/env python
"""validate_adr_status.py -- the ADR `Status:` grammar + enum validator (`[#242]`).

WHY THIS EXISTS. `docs/decisions/README.md` declares the permitted `Status:` domain
(2026-08-12, register `protocols/STANDING_RULINGS.md` M-6 / `N2-D2-i`) and says in terms:
*"Nothing checks this enum -- it is a declared domain, not a gate; a validator is available
work and is not claimed here."* This is that validator. ADR-94 filed the need as `[#242]`,
naming two legs: header<->README-index coherence, and Pattern-B go-forward enforcement.

POSTURE. Read-only (Layer-2, ADR-28/36): it parses and reports; it writes nothing and it
normalizes nothing. Deciding an ADR's status, editing a status line, and archiving are all
OUT of scope by construction -- see the honest limits below.

THE ENUM IS ADOPTED, NOT MINTED. `STATUS_ENUM` is `docs/decisions/README.md` §"Status enum"
verbatim, plus `PARKED`. `PARKED` is live (ADR-114, operator ruling 2026-08-22) and is
acknowledged in that section's own 2026-08-22 update paragraph, but was never added to its
table. Enforcing the table literally would RED a correctly-ruled operator selection, so it is
accepted here and the table/prose divergence is filed rather than silently absorbed.

EXIT CONTRACT (never-silently-green -- the `validate_onboarding_rulings.py` pattern):
  * 0 -- no defects.
  * 1 -- defects found; each is printed.
  * 2 -- the corpus is unreadable / structurally unusable. A broken subject must never
         look green, so this is louder than a defect, not quieter.

THE FIVE GRAMMARS ARE MEASURED, NOT GUESSED. Every one below was found in the live corpus at
merge base `aeec0fd1` and is enumerated with counts in
`docs/audits/2026-08-23-technical-lane-status-grammar.md` Step 1.

HONEST ENFORCEMENT LIMITS (state-honest-enforcement-limits):
  1. **It checks SHAPE and DOMAIN, never correctness.** Nothing here says an ADR's status is
     the *right* status. `R_COHERENCE` compares two surfaces and reports disagreement; which
     side is wrong is a human call, and the check deliberately does not guess.
  2. **The README-index side is prose, not a field.** `index_effective_status` reads a status
     out of the index's free-text Title column via three marker forms measured in the live
     file, and falls back to `Accepted` on no marker (the file's own convention: a prefix
     appears only for non-Accepted). That fallback is a *convention*, not a declaration, so a
     genuinely status-less row is indistinguishable from an Accepted one. A structured status
     column would retire this limit; `[#553]` already touches that file.
  3. **An unindexed ADR is `R_UNINDEXED`, never a silent pass.** Reporting an ADR the index
     does not mention as "coherent" would be the vacuous pass this gate exists to prevent.
     At merge base `aeec0fd1` this leg fires zero times on the live corpus -- not because
     every ADR is indexed, but because the only two unindexed files are the duplicate-numbered
     ones, and limit 4 catches those instead. Both legs are needed; neither is redundant.
  4. **Duplicate ADR numbers are ambiguous, and the ambiguity is REPORTED not resolved.**
     `adr_number` keys on the number, and two numbers (51, 70) are each claimed by two files
     (`ADR-51-architecture-doc-convention.md` + `ADR-51-amendment-*`, and likewise for 70).
     A first-wins dict would hide the second file's status entirely and silently disarm
     `R_UNINDEXED` for it, so `duplicate_id_defects` raises the collision separately. Which
     file "is" ADR-51 is not this validator's call.
  5. **Only the first `HEADER_WINDOW` lines are scanned.** A status field buried below that is
     invisible. 30 lines covers every member of the live corpus with margin (deepest live
     field: line 5).
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import click

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
LIVE_DIR = _REPO_ROOT / "docs" / "decisions"
ARCHIVE_DIR = LIVE_DIR / "archive"

# How far into a file a status field may legitimately live. See honest limit 5.
HEADER_WINDOW = 30

# --- the grammars -------------------------------------------------------------
#
# Most-specific first; the first match on a line wins, so one physical line can never be
# counted as two fields.
#
# `Status` MUST be immediately followed by ':'. That single constraint is the only thing
# separating a real status FIELD from an amendment marker headed `**Status update (...)`,
# which `ADR-82:11` carries. An optional-colon regex swallows that marker as a bogus SECOND
# status field -- a false positive that was live in this lane's own first measurement pass
# and is pinned by `test_status_update_marker_is_NOT_a_status_field`.
GRAMMARS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("G5", re.compile(r"^>\s*\*\*Status:\s*(?P<v>.*?)\*\*\s*(?P<tail>.*)$")),
    ("G1", re.compile(r"^-\s+\*\*Status:\*\*\s*(?P<v>.*)$")),
    ("G2", re.compile(r"^\*\*Status:\*\*\s*(?P<v>.*)$")),
    ("G3", re.compile(r"^Status:\s*(?P<v>.*)$")),
    ("G4", re.compile(r"^status:\s*(?P<v>.*)$")),
)

GRAMMAR_LABELS = {
    "G1": "`- **Status:** V` (list item, bold, colon outside)",
    "G2": "`**Status:** V` (bare bold paragraph)",
    "G3": "`Status: V` (plain text, no markup)",
    "G4": "`status: V` (YAML frontmatter, lowercase key)",
    "G5": "`> **Status: V**` (blockquote banner, colon inside the bold)",
}

#: The single canonical grammar. G1 is chosen because it is the plurality of the live corpus
#: (40 of 87) and is the form ADR-94 itself names when it writes `**Status:**`.
CANONICAL_GRAMMAR = "G1"

#: `docs/decisions/README.md` §"Status enum", verbatim, plus PARKED (see module docstring).
#: Longest-first so `Partially superseded` is never read as `Superseded` with junk in front.
STATUS_ENUM: tuple[str, ...] = (
    "Explored, not adopted",
    "Partially superseded",
    "Superseded",
    "Deprecated",
    "Proposed",
    "Accepted",
    "PARKED",
)

#: Terminal statuses -- archival-eligible at H3's zero-inbound bar. Carried by ZERO live
#: ADRs at merge base `aeec0fd1`, which is `[#552]`'s "structurally unreachable" observation
#: and is independently re-measured in this lane's Step 1.
TERMINAL_STATUSES = frozenset({"Superseded", "Deprecated"})

# --- rule ids -----------------------------------------------------------------
R_GRAMMAR = "grammar"          # not the canonical grammar
R_ENUM = "enum"                # value not in the declared domain
R_SINGLE = "single-field"      # a file must carry exactly one status field
R_WRAP = "wrapped-value"       # value continues onto the next physical line
R_COHERENCE = "coherence"      # header status != README-index effective status
R_UNINDEXED = "unindexed"      # ADR carries no README-index row at all
R_DUPLICATE = "duplicate-id"   # two files claim one ADR number

#: Legs armed at FAIL vs WARN. See `docs/audits/2026-08-23-technical-lane-status-grammar.md`
#: Step 4: the corpus carries 47 `R_GRAMMAR`, 1 `R_WRAP` and 3 `R_COHERENCE` defects today, so
#: those legs are armed WARN against a measured baseline; `R_ENUM` and `R_SINGLE` are at zero
#: and are armed FAIL. Arming the grammar leg FAIL would RED-block every commit on day one,
#: which the lane contract forbids.
FAIL_RULES = frozenset({R_ENUM, R_SINGLE})
WARN_RULES = frozenset({R_GRAMMAR, R_WRAP, R_COHERENCE, R_UNINDEXED, R_DUPLICATE})


class CorpusUnusable(Exception):
    """The corpus is unreadable/shapeless -- exit-2 class (never silent-green)."""


@dataclass(frozen=True)
class StatusField:
    """One parsed `Status:` field."""
    path: Path
    grammar: str
    lineno: int
    raw: str          # the value as written, markup intact
    value: str        # the enum member it starts with, or "" if none
    wrapped: bool     # the value continues onto the next physical line


@dataclass(frozen=True)
class Defect:
    rule: str
    subject: str      # ADR id or filename -- whatever names the offender
    detail: str


# --- parsing ------------------------------------------------------------------

_ADR_NUM_RE = re.compile(r"^(ADR-\d+)")
_MARKUP_RE = re.compile(r"[*~_`]+")
#: A line that opens a new field/heading/list item, i.e. NOT a value continuation.
_NEW_BLOCK_RE = re.compile(r"^\s*(?:[-*>#|]|\w[\w ]*:)")


def adr_number(path: Path) -> str:
    """`ADR-94` from `ADR-94-adr-status-line-....md`. Empty string if unparseable."""
    m = _ADR_NUM_RE.match(path.name)
    return m.group(1) if m else ""


def normalize_value(raw: str) -> str:
    """The enum member `raw` starts with, or `""`.

    Markup is stripped first so `**PARKED**` (ADR-114) and `~~Accepted~~` (ADR-52) match the
    same members their unmarked spellings do -- bold/strikethrough changes the rendering, not
    the decision. Matching is longest-first and CASE-SENSITIVE: `accepted` is not `Accepted`,
    because a status is a declared token rather than a free word.
    """
    cleaned = _MARKUP_RE.sub("", raw).strip()
    for member in STATUS_ENUM:
        if cleaned.startswith(member):
            return member
    return ""


def parse_status_fields(text: str, path: Path) -> list[StatusField]:
    """Every status field in `text`'s header window, in document order."""
    lines = text.splitlines()
    out: list[StatusField] = []
    for idx, line in enumerate(lines[:HEADER_WINDOW]):
        for grammar, rx in GRAMMARS:
            m = rx.match(line)
            if not m:
                continue
            raw = m.group("v").strip()
            # G5's value sits inside the bold; anything after the close is prose, not value.
            nxt = lines[idx + 1] if idx + 1 < len(lines) else ""
            wrapped = bool(
                raw
                and not raw.endswith((".", ")", "]", "*"))
                and nxt.strip()
                and not _NEW_BLOCK_RE.match(nxt)
            )
            out.append(StatusField(
                path=path, grammar=grammar, lineno=idx + 1, raw=raw,
                value=normalize_value(raw), wrapped=wrapped))
            break
    return out


def scan_zone(directory: Path) -> tuple[list[StatusField], list[str], list[str]]:
    """Parse every `ADR-*.md` directly in `directory`.

    Returns `(fields, missing, extra)` -- one field per conforming file, plus the names of
    files carrying zero and more-than-one status field. `missing`/`extra` are returned rather
    than folded into `fields` so a caller cannot mistake an absent field for a clean one.
    """
    if not directory.is_dir():
        raise CorpusUnusable(f"not a directory: {directory}")
    fields: list[StatusField] = []
    missing: list[str] = []
    extra: list[str] = []
    paths = sorted(directory.glob("ADR-*.md"))
    if not paths:
        raise CorpusUnusable(f"no ADR-*.md files under {directory}")
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise CorpusUnusable(f"unreadable: {path} ({exc})") from exc
        found = parse_status_fields(text, path)
        if not found:
            missing.append(path.name)
        elif len(found) > 1:
            extra.append(path.name)
            fields.extend(found)
        else:
            fields.extend(found)
    return fields, missing, extra


# --- the rules ----------------------------------------------------------------

def field_defects(fields: list[StatusField]) -> list[Defect]:
    """Grammar / enum / single-field / wrap defects for one file's parsed fields.

    Takes the fields of a SINGLE file: `R_SINGLE` is a per-file property, so passing a
    whole corpus here would compare the corpus's total against 1 and always fire. `scan_zone`
    callers use `corpus_defects` instead.
    """
    defects: list[Defect] = []
    if len(fields) != 1:
        subject = fields[0].path.name if fields else "(file)"
        defects.append(Defect(
            R_SINGLE, subject,
            f"expected exactly 1 status field, found {len(fields)}"
            + (f" at lines {[f.lineno for f in fields]}" if fields else "")))
    for f in fields:
        if f.grammar != CANONICAL_GRAMMAR:
            defects.append(Defect(
                R_GRAMMAR, f"{f.path.name}:{f.lineno}",
                f"{f.grammar} {GRAMMAR_LABELS[f.grammar]} -- canonical is "
                f"{CANONICAL_GRAMMAR} {GRAMMAR_LABELS[CANONICAL_GRAMMAR]}"))
        if not f.value:
            defects.append(Defect(
                R_ENUM, f"{f.path.name}:{f.lineno}",
                f"value {f.raw[:60]!r} starts with no declared enum member "
                f"({', '.join(STATUS_ENUM)})"))
        if f.wrapped:
            defects.append(Defect(
                R_WRAP, f"{f.path.name}:{f.lineno}",
                "value continues onto the next physical line -- a line-oriented reader "
                "truncates it silently"))
    return defects


def corpus_defects(fields: list[StatusField], missing: list[str],
                   extra: list[str]) -> list[Defect]:
    """Field defects across a whole zone, with `R_SINGLE` applied per file."""
    defects: list[Defect] = []
    for name in missing:
        defects.append(Defect(R_SINGLE, name, "no status field found in the header window"))
    by_file: dict[str, list[StatusField]] = {}
    for f in fields:
        by_file.setdefault(f.path.name, []).append(f)
    for name in extra:
        defects.append(Defect(
            R_SINGLE, name,
            f"{len(by_file.get(name, []))} status fields at lines "
            f"{[f.lineno for f in by_file.get(name, [])]}"))
    for f in fields:
        for d in field_defects([f]):
            if d.rule != R_SINGLE:
                defects.append(d)
    return defects


# --- the README-index side ----------------------------------------------------

_INDEX_ROW_RE = re.compile(r"^\|\s*(ADR-\d+)\s*\|\s*([^|]*?)\s*\|\s*(.*?)\s*\|\s*$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")

#: Status markers in MARKER POSITION only. An incidental mention -- ADR-98's row reads
#: "superseded-in-part by intake brief #1" -- must NOT be read as a status, which is why
#: none of these matches a bare mid-sentence word.
_INDEX_MARKERS: tuple[tuple[str, re.Pattern[str]], ...] = (
    # leading bold:     **PARKED (operator ruling 2026-08-22) - ...**
    ("lead-bold", re.compile(r"^\*\*(?P<s>[A-Z][A-Za-z, ]*?)[\s(*]")),
    # strikethrough:    ~~Old title~~ Superseded by ADR-53
    ("strike", re.compile(r"^~~.*?~~\s*(?P<s>[A-Z][a-z]+)\b")),
    # trailing dash:    ... - Deprecated 2026-05-23; relocated byte-identical
    ("dash", re.compile(
        r"[—-]\s*(?P<s>Deprecated|Superseded|Partially superseded|"
        r"Explored, not adopted|PARKED|Proposed)\b")),
)

#: The index's own convention: a status prefix appears only for a NON-Accepted ADR, so a row
#: with no marker means Accepted. A convention, not a declaration -- see honest limit 2.
INDEX_DEFAULT_STATUS = "Accepted"


def index_effective_status(readme_text: str) -> dict[str, str]:
    """`{ADR-NN: effective status}` read out of the ADR index's Title column.

    Only rows whose second cell is a `YYYY-MM-DD` date are index rows; that filter is what
    keeps the file's other pipe tables (e.g. the Council-transcript table, which repeats ADR
    ids) from being read as status. First row per id wins.
    """
    out: dict[str, str] = {}
    for line in readme_text.splitlines():
        m = _INDEX_ROW_RE.match(line)
        if not m:
            continue
        adr, date, title = m.group(1), m.group(2), m.group(3)
        if not _DATE_RE.match(date) or adr in out:
            continue
        status = INDEX_DEFAULT_STATUS
        for _kind, rx in _INDEX_MARKERS:
            mm = rx.search(title)
            if not mm:
                continue
            token = _MARKUP_RE.sub("", mm.group("s")).strip()
            member = next(
                (e for e in STATUS_ENUM
                 if token.lower().startswith(e.split(",")[0].lower())), "")
            if member:
                status = member
                break
        out[adr] = status
    return out


def duplicate_id_defects(fields: list[StatusField]) -> list[Defect]:
    """One defect per ADR number claimed by more than one file.

    This exists because collapsing a collision into a single key is exactly the silent pass
    the coherence leg must not make: with two files at `ADR-51`, a first-wins dict hides the
    second file's status entirely, and `R_UNINDEXED` can then never fire for it. Reported,
    never resolved -- picking which file "is" ADR-51 is not this validator's call.
    """
    by_num: dict[str, list[str]] = {}
    for f in fields:
        num = adr_number(f.path)
        if num:
            by_num.setdefault(num, []).append(f.path.name)
    return [
        Defect(R_DUPLICATE, num,
               f"{len(names)} files claim this number: {', '.join(sorted(names))} -- "
               "index coherence is ambiguous for all of them")
        for num, names in sorted(by_num.items()) if len(names) > 1
    ]


def coherence_defects(header_status: dict[str, str],
                      index_status: dict[str, str]) -> list[Defect]:
    """`[#242]`'s Done-when leg: flag an ADR whose header status differs from the index's.

    An ADR absent from the index yields `R_UNINDEXED`, never silence (honest limit 3).
    """
    defects: list[Defect] = []
    for adr in sorted(header_status, key=lambda a: (len(a), a)):
        head = header_status[adr]
        if adr not in index_status:
            defects.append(Defect(
                R_UNINDEXED, adr,
                f"header says {head!r} but the ADR carries no README index row -- "
                "coherence is indeterminate, not confirmed"))
            continue
        idx = index_status[adr]
        if head != idx:
            defects.append(Defect(
                R_COHERENCE, adr,
                f"header {head!r} != README index {idx!r}"))
    return defects


# --- reporting ----------------------------------------------------------------

def surface_line(fields: list[StatusField], defects: list[Defect]) -> str:
    counts: dict[str, int] = {}
    for d in defects:
        counts[d.rule] = counts.get(d.rule, 0) + 1
    breakdown = ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "none"
    return (f"[adr-status] {len(fields)} status field(s); defects: {breakdown} "
            f"-- canonical grammar {CANONICAL_GRAMMAR}")


@click.command()
@click.option("--root", "root", default=str(_REPO_ROOT), show_default=False,
              help="Repo root (tests override).")
@click.option("--include-archive", is_flag=True, default=False,
              help="Also scan docs/decisions/archive/ (terminal statuses live there).")
def main(root: str, include_archive: bool) -> None:
    """Validate the ADR `Status:` grammar and enum. Read-only."""
    live_dir = Path(root) / "docs" / "decisions"
    try:
        fields, missing, extra = scan_zone(live_dir)
    except CorpusUnusable as exc:
        click.echo(f"adr-status: UNUSABLE -- {exc}", err=True)
        sys.exit(2)

    defects = corpus_defects(fields, missing, extra)

    if include_archive:
        try:
            a_fields, a_missing, a_extra = scan_zone(live_dir / "archive")
        except CorpusUnusable as exc:
            click.echo(f"adr-status: archive UNUSABLE -- {exc}", err=True)
            sys.exit(2)
        fields += a_fields
        defects += corpus_defects(a_fields, a_missing, a_extra)

    defects += duplicate_id_defects(fields)

    readme = live_dir / "README.md"
    if readme.is_file():
        headers: dict[str, str] = {}
        for f in fields:
            num = adr_number(f.path)
            if num:
                headers.setdefault(num, f.value or f.raw[:40])
        defects += coherence_defects(
            headers, index_effective_status(readme.read_text(encoding="utf-8")))

    if defects:
        click.echo("adr-status: DEFECT(S)")
        for d in sorted(defects, key=lambda x: (x.rule, x.subject)):
            level = "FAIL" if d.rule in FAIL_RULES else "WARN"
            click.echo(f"  [{level}] {d.rule}: {d.subject} -- {d.detail}")
        click.echo(surface_line(fields, defects))
        sys.exit(1)

    click.echo(surface_line(fields, defects))
    sys.exit(0)


if __name__ == "__main__":
    main()
