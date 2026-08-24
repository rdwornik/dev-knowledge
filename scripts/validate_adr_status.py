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

#: One alternation of the declared enum in STATUS_ENUM order, i.e. LONGEST-FIRST. Regex
#: alternation is leftmost-first, so this ordering is what stops `Partially superseded` being
#: read as `Superseded`; reordering STATUS_ENUM silently breaks that.
_ENUM_ALT = "|".join(re.escape(m) for m in STATUS_ENUM)

#: An enum token at the start of a value, optionally wrapped in BALANCED, SAME-KIND emphasis,
#: and followed by a real boundary.
#:
#: The wrapper is MATCHED, never stripped, so inline markup inside a word (`Acce*pted`) cannot
#: be laundered into a valid token. `(?(w)(?P=w))` is a conditional backreference: a wrapper
#: that opened must close with the identical marker, so `**Accepted` and `*Accepted\`` are
#: rejected rather than leniently accepted. The trailing class forbids `*` and a backtick as
#: well as word characters, because with NO wrapper an emphasis run immediately after the
#: token means the token was never the whole value — `Accepted**ness` (terra R3-HIGH-1).
#: `\*+` rather than `\*{1,3}`: nested emphasis (`****Accepted****`) is valid markdown, and
#: rejecting it produced a FALSE `enum` FAIL — the worst failure mode available to a
#: FAIL-armed leg (terra R4-HIGH-2). The backreference still forces the identical run to
#: close, so arbitrary length costs no strictness.
_ENUM_AT_START_RE = re.compile(
    rf"^(?P<w>\*+|`+)?(?P<s>{_ENUM_ALT})(?(w)(?P=w))(?![\w\-*`])")

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
#: A struck-through span is REMOVED, content and all — never unwrapped. `~~Accepted~~
#: Superseded by ADR-53` (ADR-52) means "no longer Accepted, now Superseded"; stripping the
#: tildes and keeping the word yields `Accepted`, which INVERTS the status of the one genuinely
#: superseded ADR in the corpus. Pinned by `test_strikethrough_is_removed_not_unwrapped`.
_STRIKE_SPAN_RE = re.compile(r"~~.*?~~")
#: Fence opener — ``` or ~~~ (3+), up to 3 spaces of indent, with an optional info string.
#: An info string may contain spaces (` ```md example `); a BACKTICK fence's info string may
#: not contain a backtick (CommonMark), a tilde fence's may.
_FENCE_OPEN_RE = re.compile(r"^ {0,3}(?P<f>`{3,}|~{3,})(?P<info>[^`]*)$")
#: Fence closer — same character, AT LEAST the opener's length, nothing but whitespace after.
#: Length matters: a 4-char opener is NOT closed by 3 (terra R2-HIGH-2).
_FENCE_CLOSE_RE = re.compile(r"^ {0,3}(?P<f>`{3,}|~{3,})\s*$")
#: A line that opens a new block — i.e. NOT a lazy continuation of the value above it.
#: List and heading markers require their FOLLOWING WHITESPACE, per CommonMark: without it,
#: `*continued rationale*` (emphasis) was misread as a bullet and a genuine wrapped value went
#: undetected (terra R2-MEDIUM-1). The `**Key:**` alternative is listed explicitly because the
#: bare `\w[\w ]*:` form cannot match a bolded field name, and 34 live ADRs use exactly that.
_NEW_BLOCK_RE = re.compile(
    r"""^\s*(?:
          [-*+]\s              # bullet list item
        | \d+[.)]\s            # ordered list item
        | \#{1,6}\s            # ATX heading
        | >                    # blockquote
        | \|                   # table row
        | `{3,} | ~{3,}        # code fence
        | <!--                 # HTML comment
        | \*\*[^*]+:\*\*       # **Key:** field — the key may contain punctuation, e.g.
                               # ADR-72's `**Amends (does not edit):**`. A `[\w ]+` key
                               # class misses that and misreads the line as a continuation,
                               # inventing a second wrapped-value defect out of a
                               # perfectly well-formed file. The required `:` before the
                               # closing `**` is what keeps a bare `**Accepted**` emphasis
                               # line classified as a continuation (terra R2-MEDIUM-1).
        | \w[\w ]*:            # Key: field
    )""", re.VERBOSE)


def adr_number(path: Path) -> str:
    """`ADR-94` from `ADR-94-adr-status-line-....md`. Empty string if unparseable."""
    m = _ADR_NUM_RE.match(path.name)
    return m.group(1) if m else ""


def normalize_value(raw: str) -> str:
    """The enum member `raw` starts with, or `""`.

    Two markup passes, in this order and NOT interchangeable:

      1. **Struck-through spans are DELETED, content included.** `~~X~~ Y` asserts "not X, now
         Y", so the struck word is the OLD status and must not be matched. Unwrapping it
         instead — the obvious `[*~_`]+` strip — turns ADR-52's `~~Accepted~~ Superseded by
         ADR-53` into `Accepted`, inverting the status of the only genuinely superseded ADR in
         the corpus and hiding it from the archival bar that exists to find it.
      2. **Remaining emphasis markers are stripped**, so `**PARKED**` (ADR-114) matches the
         same member its unmarked spelling does — bold changes rendering, not meaning.

    Matching is longest-first (the alternation is built in `STATUS_ENUM` order, so
    `Partially superseded` can never be read as `Superseded`), CASE-SENSITIVE (`accepted` is
    not `Accepted` — a status is a declared token, not a free word), and BOUNDARY-CHECKED
    (`Acceptedness` and `Accepted-ish` are not `Accepted`).

    Emphasis is matched as a BALANCED WRAPPER around the token, never stripped in place.
    A blanket `[*`]+` strip let `Acce*pted` and ``Acce`pted`` normalize to `Accepted` and
    bypass the FAIL-armed enum rule (terra R2-HIGH-1).
    """
    m = _ENUM_AT_START_RE.match(_STRIKE_SPAN_RE.sub("", raw).strip())
    return m.group("s") if m else ""


def parse_status_fields(text: str, path: Path) -> list[StatusField]:
    """Every status field in `text`'s header window, in document order.

    Lines inside a fenced code block are SKIPPED. An ADR quoting a status form in an example
    block — e.g. showing the pre-enum spelling it no longer uses — would otherwise parse as a
    real second field and fire BOTH FAIL-armed legs (`single-field` on the count, `enum` on the
    quoted value), REDDING the pre-commit gate on a legitimate file. A false positive on a
    FAIL-armed leg is the worst failure this validator can have, so the fence state is tracked
    rather than assumed absent.
    """
    # A UTF-8 BOM makes line 1 start with ﻿, so `^-\s+\*\*Status:` never matches and the
    # field goes INVISIBLE — a silent miss, not a loud one (terra HIGH-1).
    lines = text.lstrip("﻿").splitlines()
    out: list[StatusField] = []
    fence: tuple[str, int] | None = None   # (fence char, opener length)
    for idx, line in enumerate(lines[:HEADER_WINDOW]):
        if fence is None:
            fo = _FENCE_OPEN_RE.match(line)
            if fo and (fo.group("f")[0] == "~" or "`" not in fo.group("info")):
                fence = (fo.group("f")[0], len(fo.group("f")))
                continue
        else:
            fc = _FENCE_CLOSE_RE.match(line)
            if (fc and fc.group("f")[0] == fence[0]
                    and len(fc.group("f")) >= fence[1]):
                fence = None
            continue
        for grammar, rx in GRAMMARS:
            m = rx.match(line)
            if not m:
                continue
            raw = m.group("v").strip()
            # A value continues onto the next line exactly when that line is a markdown LAZY
            # CONTINUATION: non-blank, and not the start of a new block. The terminal-
            # punctuation test this replaced was wrong in both directions (terra HIGH-3) —
            # it missed `**Accepted**\ncontinued rationale` because the value ends in `*`,
            # and it depended on punctuation that carries no block-structure meaning.
            nxt = lines[idx + 1] if idx + 1 < len(lines) else ""
            wrapped = bool(raw and nxt.strip() and not _NEW_BLOCK_RE.match(nxt))
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

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")


def _split_cells(row: str) -> list[str]:
    """Split a markdown table row on UNESCAPED pipes.

    A pipe is escaped only after an ODD-length backslash run: in `a \\\\| b` the two
    backslashes are themselves escaped, so the pipe IS a delimiter. A `(?<!\\\\)\\|` lookbehind
    gets this wrong and folds a four-cell row into three, which lets a malformed row invent an
    index status (terra R3-HIGH-2). Scanned rather than regexed because a lookbehind cannot
    count a variable-length run.
    """
    cells: list[str] = []
    buf: list[str] = []
    backslashes = 0
    for ch in row:
        if ch == "|" and backslashes % 2 == 0:
            cells.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
        backslashes = backslashes + 1 if ch == "\\" else 0
    cells.append("".join(buf))
    return cells

#: Status markers in MARKER POSITION only, each matching a COMPLETE enum token with a trailing
#: boundary. An incidental mention must NOT be read as a status — ADR-98's row reads
#: "superseded-in-part by intake brief #1", and `Pre-Deprecated API migration` must not resolve
#: to Deprecated (terra HIGH-4).
_INDEX_MARKERS: tuple[tuple[str, re.Pattern[str]], ...] = (
    # leading bold:  **PARKED (operator ruling 2026-08-22) — ...**
    # Anchored, complete token, and the next char must not continue a word — so
    # `**Explored option**` does NOT resolve to `Explored, not adopted`.
    ("lead-bold", re.compile(rf"^\*\*(?P<s>{_ENUM_ALT})(?![\w-])")),
    # strikethrough:  ~~Old title~~ Superseded by ADR-53
    ("strike", re.compile(rf"^~~.*?~~\s*(?P<s>{_ENUM_ALT})(?![\w-])")),
    # trailing dash:  ... — Deprecated 2026-05-23; relocated byte-identical
    # The dash must be preceded by whitespace or start-of-cell, so the hyphen inside
    # `Pre-Deprecated` cannot serve as the marker's separator.
    ("dash", re.compile(rf"(?:^|(?<=\s))[—–-]\s*(?P<s>{_ENUM_ALT})(?![\w-])")),
)

#: The index's own convention: a status prefix appears only for a NON-Accepted ADR, so a row
#: with no marker means Accepted. A convention, not a declaration -- see honest limit 2.
INDEX_DEFAULT_STATUS = "Accepted"


def index_effective_status(readme_text: str) -> dict[str, str]:
    """`{ADR-NN: effective status}` read out of the ADR index's Title column.

    Cells are split on UNESCAPED pipes, and the row must have exactly three content cells —
    a four-cell row previously folded its fourth cell into the Title and could take its status
    from there (terra HIGH-4). Only rows whose second cell is a `YYYY-MM-DD` date are index
    rows; that filter keeps the file's other pipe tables (e.g. the Council-transcript table,
    which repeats ADR ids) from being read as status. First row per id wins.

    A marker must match a COMPLETE enum token in marker position; the value is taken verbatim
    from that match, never inferred from a prefix of it.
    """
    out: dict[str, str] = {}
    for line in readme_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        parts = _split_cells(stripped)
        # The outer parts must be EMPTY, i.e. the row really did open and close on UNESCAPED
        # delimiters. `endswith("|")` alone is satisfied by a trailing ESCAPED pipe, and the
        # `[1:-1]` slice would then discard a real content cell and admit a malformed
        # four-cell row as a valid three-cell one (terra R4-HIGH-1).
        if len(parts) < 2 or parts[0].strip() or parts[-1].strip():
            continue
        cells = [c.strip() for c in parts[1:-1]]
        if len(cells) != 3:
            continue
        adr, date, title = cells
        if not _ADR_NUM_RE.fullmatch(adr) or not _DATE_RE.match(date) or adr in out:
            continue
        status = INDEX_DEFAULT_STATUS
        for _kind, rx in _INDEX_MARKERS:
            mm = rx.search(title)
            if mm:
                status = mm.group("s")
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
    # Keyed on FILENAME, not on field: a file carrying two status fields (ADR-40 in the
    # archive does) would otherwise be reported as colliding with ITSELF -- "2 files claim
    # this number: ADR-40-....md, ADR-40-....md". That is a false collision, and it appears
    # only on the --include-archive path, which is why a field-keyed count survived the live
    # corpus unnoticed.
    by_num: dict[str, set[str]] = {}
    for f in fields:
        num = adr_number(f.path)
        if num:
            by_num.setdefault(num, set()).add(f.path.name)
    return [
        Defect(R_DUPLICATE, num,
               f"{len(names)} files claim this number: {', '.join(sorted(names))} -- "
               "index coherence is ambiguous for all of them")
        for num, names in sorted(by_num.items()) if len(names) > 1
    ]


def header_status_map(fields: list[StatusField]) -> dict[str, str]:
    """`{ADR-NN: header status}`, with duplicate-numbered ADRs EXCLUDED.

    A first-wins dict over a collision picks a winner by filename order and then reports a
    coherence verdict derived from it — so with `ADR-11-a.md: Proposed` and
    `ADR-11-b.md: Accepted`, whichever sorts first decides, and reversing the two hides the
    other disagreement (terra R2-MEDIUM-2). A collision contributes NO coherence verdict,
    because no honest one exists; it is reported by `duplicate_id_defects` instead.

    The exclusion is keyed on the FIELD count, not the filename count, so it also covers ONE
    file carrying two status fields — `archive/ADR-40` does, at two casings. Keying on
    filenames alone left that case picking the first field arbitrarily (terra R3-MEDIUM-1);
    its `single-field` defect is still raised either way.
    """
    by_num: dict[str, list[StatusField]] = {}
    for f in fields:
        num = adr_number(f.path)
        if num:
            by_num.setdefault(num, []).append(f)
    return {
        num: fs[0].value or fs[0].raw[:40]
        for num, fs in by_num.items()
        if len(fs) == 1
    }


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

    # The index is HALF the subject. Exiting 0 with the coherence leg silently skipped is the
    # same vacuous pass the adapter was fixed for; the CLI must not disagree with it
    # (terra R2-HIGH-3).
    readme = live_dir / "README.md"
    try:
        defects += coherence_defects(
            header_status_map(fields),
            index_effective_status(readme.read_text(encoding="utf-8", errors="replace")))
    except OSError as exc:
        click.echo(f"adr-status: ADR index unreadable ({exc}) -- the header-vs-index "
                   f"coherence leg DID NOT RUN", err=True)
        defects.append(Defect(R_UNINDEXED, str(readme),
                              f"index unreadable ({exc}); coherence leg did not run"))

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
