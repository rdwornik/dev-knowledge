"""funnel_coverage.py -- the detector behind the audit funnel-coverage leg (M3).

THE GAP. `protocols/PLAYBOOK.md` Ch8 makes the wave-close funnel table mandatory and ADR-111
governs what a finding may become, but ADR-111's own Consequences paragraph states the honest
limit verbatim: *"No organ checks that an audit's findings are triaged, and none is built
here."* So "no audit is wasted" was an instruction, and an instruction is a request. This
module is the half that makes it a claim a machine can refute.

WHAT IT MEASURES, precisely. For every artifact in `docs/audits/`, whether some **disposition
ledger** in that same directory carries a row naming it with a term from the ruled closed set
AND a non-empty evidence locator. It does NOT measure whether the disposition is correct, and
it cannot -- see HONEST LIMITS at the bottom.

THE VOCABULARY IS RULED, NOT INVENTED. Architect standing ruling of 2026-08-17
(`docs/audits/2026-08-17-technical-batch-7a-lane-a-contract.md:22-27`, committed `875509bd`;
quoted again at the head of `docs/audits/2026-08-17-technical-audit-disposition-ledger.md`):

    Every audit artifact carries exactly one disposition: ACTIONED (conclusion already live --
    cite the commit), FILED (a row owns it -- cite the id), REJECTED (a ruling declined it --
    cite it), SUPERSEDED (a later artifact replaced it -- cite it). An undisposed audit is a
    defect, not a document.

That ruling is ARTIFACT-level, which is this check's unit. ADR-111 §1's four outcomes and
PLAYBOOK Ch8's five classifications are FINDING-level -- a different unit, deliberately not
used here. No fifth vocabulary is introduced.

PENDING IS NOT COVERAGE, AND IT IS NOT ABSENCE EITHER. The same ruling admits PENDING for the
undecidable case (*"a wrong ACTIONED is worse than an honest PENDING"*). A PENDING artifact has
been looked at and its open question recorded; an absent one has not. Collapsing the two would
throw away the only distinction that says whether work was done, so they are counted and
reported separately and only the ABSENT set drives the ratchet.

THE LEDGER SHAPE IS THE ONE ALREADY ON DISK, not a schema this module asks for. A ledger is a
markdown table whose header carries a file-ish column, a `disposition` column and an
`evidence locator` column -- the exact columns the lane-a contract specified at `:87-92`. Any
artifact may carry one, including an artifact dispositioning itself, so a new audit has an
authoring-time discharge path that never requires editing an immutable file (§5 rule 3).

A DISPOSITION LEDGER SELF-DISCHARGES BY CONSTRUCTION -- it carries a row naming itself, so
using the mechanism can never mint the debt it exists to clear (architect ruling, R5 window
bundle B3, 2026-09-05). Stated here because this is the point of enforcement: without that row
every new ledger lands as one more undispositioned artifact, making the mechanism net-neutral
at best -- the recursion the R5 disposition sheet flagged and the ruling closed. Live example:
`docs/audits/2026-09-05-technical-r5-funnel-disposition-ledger.md`, whose last row is itself.

MEASURED DISCRIMINATION, because a predicate nobody measured is a guess. On the 693-artifact
corpus the header predicate admits exactly ONE table. `docs/audits/2026-05-24-dev-knowledge-self-audit.md`
carries a table literally headed "## Disposition ledger" with `File` and `Disposition` columns
and is correctly DECLINED: it predates the ruling, carries no evidence-locator column, and its
vocabulary is `WILL FIX`. One same-named, same-shaped, pre-ruling near-miss admitted 0 rows --
that is the false-admit number, and it is why the locator column is required rather than
optional.

EVERY TABLE, EVERY ROW -- the [#560] lesson, adopted rather than repeated. That row exists
because `review_artifact_coverage` reads only the FIRST Branch/HEAD triple per file, so a real
review in a second triple is invisible to it. This scanner walks every table in a file and
every row in a table; `tests/test_funnel_coverage.py` pins it with a fixture whose SECOND table
carries the only disposition. `[#560]`'s own defect is NOT fixed here -- it is that row's, and
it lives in the collision file this lane may not edit.

ESCAPED PIPES ARE REAL DATA HERE. The live ledger quotes each artifact's final metric line
verbatim, and those quotes contain `\\|`. A naive `split("|")` shredded two ACTIONED rows into
the tokens `SHALL\\` and `\\` during the measurement pass -- a silent two-row undercount that
looked exactly like a clean parse. The cell splitter therefore honours the escape.

A LEADING PIPE IS REQUIRED; a trailing one is not. That asymmetry is deliberate and it is
stated precisely because an earlier draft of this paragraph overclaimed "outer pipes are
required" while the code only ever enforced the leading one (terra MEDIUM, round 3 -- caught
against the DOCUMENTATION, which was the half that was wrong). The leading pipe is what
discriminates a table row from prose; a trailing pipe is optional in GFM, so requiring it would
false-WARN a well-formed ledger.

A FULLY PIPELESS ROW is a DECLINED review finding rather than an oversight. GFM admits
`File | Disposition | Evidence locator` with no outer pipes at all, and `split_cells` returns
None for that shape, so such a ledger would be invisible and every artifact it dispositions
would read as uncovered. Declined deliberately (terra HIGH, round 2):
the ledger shape is RULED -- the 2026-08-17 lane-a contract specifies the table and the live
ledger uses outer pipes -- and admitting pipeless rows widens the surface on which ordinary
prose containing pipes becomes a candidate row. The two failure modes are not symmetric. A
pipeless ledger produces a LOUD wave of false WARNs, noticed immediately and fixed in one edit;
a prose line read as a ledger produces SILENT false coverage, which is the failure this leg
exists to prevent. Precision over recall, the same trade `review_artifact_coverage`'s title
predicate makes.

READ-ONLY and Layer-2: this module never writes. The baseline file is regenerated by an
explicit `--write-baseline` invocation, never as a side effect of measuring.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# The ruled closed set (2026-08-17). Order is the ruling's own.
DISPOSITION_TERMS: tuple[str, ...] = ("ACTIONED", "FILED", "REJECTED", "SUPERSEDED")
PENDING_TERM = "PENDING"

# Bumped when the predicate changes. A baseline stamped with a DIFFERENT id is not
# commensurable with a live measurement and the ratchet refuses to compare them rather than
# letting a predicate revision silently rebase the debt -- the `silent_rule_ratchet` discipline
# ([#436]), which exists because a re-measurement that nobody reviewed is indistinguishable
# from a drain.
DETECTOR_ID = "funnel-coverage/v1"

#: NOT BUMPED BY THE 2026-09-05 MANIFEST-LINK RULING, and the reason is the ratchet's own
#: safety property rather than convenience. The id exists so a predicate revision cannot
#: silently REBASE the debt: `ratchet_findings` refuses to compare a baseline stamped with a
#: different id, which is right when a revision can move an artifact in EITHER direction.
#: This revision is strictly MONOTONE -- it only ever adds a coverage route, so an artifact
#: covered under the old predicate is covered under the new one and `uncovered` can only
#: shrink. A shrinking predicate cannot hide debt: it adds no name to the baseline, and every
#: name it removes shows up as ratchet-down headroom. Bumping here would replace 32 by-name
#: regressions with one "not commensurable" WARN -- switching the leg OFF while appearing to
#: satisfy it, which is the exact failure the id was introduced to prevent.
#: `tests/test_funnel_coverage.py::test_manifest_link_route_is_monotone` pins the property.

# JSON, not YAML, and the reason is a MEASURED false positive in a sibling organ rather than
# a preference. `silent_rule_detector`'s governed corpus is `protocols/*.md`,
# `templates/**/*.{md,tmpl}` and `ecosystem/*.yaml`; this baseline enumerates 613 audit
# FILENAMES, one of which is `2026-07-06-arc5-must-verification.md`. Its slug contains the
# literal token `must`, so as an `ecosystem/*.yaml` file this baseline raises the silent-rule
# pool by +1 and FAILs the `[#436]` ratchet -- a data enumeration scoring as rule accretion,
# which is that detector's own stated residual limit ("occurrences in examples, quotations and
# already-enforced rules still count. This is a proxy").
#
# The lawful alternative is a fourth `EXCLUDED_RELPATHS` member -- the exact class already
# applied to `ecosystem/silent-rule-baseline.yaml` ("would otherwise count its own provenance
# prose, making the metric self-referential") and to `ecosystem/parity-surfaces.yaml`. That
# change is NOT taken here: `silent_rule_detector`'s docstring requires a `DETECTOR_ID` bump on
# ANY contract clause change, which forces a re-measure and re-stamp of another ratchet's
# CURATED baseline while sibling lanes are in flight. That is an operator act, not a lane's.
#
# So the format is the reversible half of the fork, and it is reported rather than quietly
# taken -- see the lane artifact's decisions section. JSON is also the honest shape for this
# file: it is machine-generated and machine-read, carries no doctrine, and needs no comments.
# It keeps the whole detector stdlib, `pyyaml` included.
BASELINE_RELPATH = "ecosystem/audit-funnel-baseline.json"
AUDITS_RELPATH = "docs/audits"

# `docs/audits/README.md` is GENERATED and cites every artifact by construction, so including
# it would make the index disposition itself. Excluded on the 2026-08-17 ledger's own stated
# precedent ("excluding the generated docs/audits/README.md, which cites everything by
# construction"), not by a fresh judgement call.
CORPUS_EXCLUDE: frozenset[str] = frozenset({"README.md"})

# A dated audit filename, with or without a `docs/audits/` prefix and with or without backticks.
# The trailing negative lookahead is load-bearing (terra HIGH, round 1): without it the
# non-greedy body matches a PREFIX, so a File cell reading `2026-08-01-technical-a.md.bak`
# binds to `2026-08-01-technical-a.md` and a backup reference or a typo silently becomes
# coverage. `.md` must be the end of the token, not a substring of a longer one.
# The BOTH-SIDED boundary is load-bearing. Round 1 added only the right one, and terra found
# on round 2 that `typo2026-08-01-technical-a.md` still bound to the real artifact -- a fix
# that closes one end of a boundary and not the other is the more dangerous kind, because it
# reads as solved. The left lookbehind still admits every decoration the live ledger uses:
# a `docs/audits/` path prefix, a backtick, a bold marker, or the start of a cell.
_AUDIT_NAME_RE = re.compile(
    r"(?<![A-Za-z0-9._-])(\d{4}-\d{2}-\d{2}-[A-Za-z0-9._-]+?\.md)(?![A-Za-z0-9._-])")

# A fenced code region opener/closer. Fence tracking is not decoration (sol route 8; terra
# HIGH, round 1): a document that DOCUMENTS the ledger shape would otherwise have its worked
# examples read as evidence, so an artifact showing an example could disposition itself -- or
# another artifact -- by accident. Fence-awareness is established practice here; the
# `markdown_it` fence-region ADOPT is a `landing_predicate`-tracked ruling with four sites.
_FENCE_RE = re.compile(r"^\s{0,3}(?P<mark>`{3,}|~{3,})(?P<rest>.*)$")

# Per-term locator SHAPES. The ruling makes the citation part of the disposition -- ACTIONED
# "cite the commit", FILED "cite the id", SUPERSEDED "cite it" -- so a term whose locator
# carries no reference of the right kind is a claim, not a disposition (sol route 7: "any
# one-character locator passes"). MEASURED ACROSS ALL 78 LIVE ROWS BEFORE ARMING: 0 mismatches
# for all three, and both SUPERSEDED targets resolve to artifacts that exist.
#
# REJECTED is deliberately absent, and that is measured rather than lazy: a ruling has no
# uniform locator form, and both live REJECTED locators are prose sentences (144 and 253
# characters). Any shape rule strong enough to matter would have false-positived 2 of 2, and a
# false WARN corrupts the very evidence a later hard-flip would rest on. Consequence accepted
# and named: REJECTED-with-prose is the cheapest fabricated route this leg admits.
# The REJECTED substance floor, and the PENDING question mark. Both are the weakest rules
# here and both are stated as such. PENDING's is PRINCIPLED -- the ruling's own words are
# "PENDING with the exact question it needs", and a question is punctuated; both live PENDING
# locators open with `Q:` and contain `?`. REJECTED's is a measured FLOOR rather than a rule
# about form, because no form exists to require.
_REJECTED_MIN_LOCATOR = 24

_LOCATOR_SHAPES: dict[str, re.Pattern[str]] = {
    # Case-insensitive: a git object name is hexadecimal and case-insensitive, so rejecting
    # `DEADBEEF` would have been a FALSE WARN on a valid commit locator (terra MEDIUM, round 3).
    # The ruling asks for a commit, not for lowercase formatting.
    "ACTIONED": re.compile(r"\b[0-9a-fA-F]{7,40}\b"),
    "FILED": re.compile(r"\[#\d+\]"),
    "SUPERSEDED": _AUDIT_NAME_RE,
}

# Header cells that identify the artifact column. `file` is the ruled spelling; the other two
# are admitted so a future ledger that says `artifact` is not silently unread.
_FILE_HEADERS: frozenset[str] = frozenset({"file", "artifact", "audit"})
_DISPOSITION_HEADER = "disposition"
_LOCATOR_HEADER = "evidence locator"


class FunnelCoverageError(RuntimeError):
    """Raised when the corpus itself cannot be read. Never raised for a coverage gap."""


@dataclass(frozen=True)
class LedgerRow:
    """One parsed ledger row. `term` is upper-cased and stripped of bold markers."""
    audit: str
    term: str
    locator: str
    ledger: str


@dataclass
class Measurement:
    """The whole live picture. Pure data -- no filesystem handles, so it pickles and prints."""
    corpus: list[str] = field(default_factory=list)
    ledgers: list[str] = field(default_factory=list)
    dispositioned: dict[str, LedgerRow] = field(default_factory=dict)
    pending: dict[str, LedgerRow] = field(default_factory=dict)
    malformed: list[LedgerRow] = field(default_factory=list)
    dangling: list[LedgerRow] = field(default_factory=list)
    #: artifact -> link kind ('explicit' | 'lane-slug'). The 2026-09-05 operator ruling: an
    #: audit linked from a batch manifest is DISPOSITIONED by that link. Kept as its own
    #: field rather than folded into `dispositioned` because a manifest link is not a ledger
    #: row -- it carries no ruled term and no evidence locator, so reporting it as one would
    #: overstate what was recorded.
    manifest_linked: dict[str, str] = field(default_factory=dict)
    detector_id: str = DETECTOR_ID

    @property
    def uncovered(self) -> list[str]:
        """Artifacts with NO ledger record at all. PENDING is deliberately excluded --
        see the module docstring; a recorded open question is not an unlooked-at file."""
        known = set(self.dispositioned) | set(self.pending) | set(self.manifest_linked)
        return sorted(n for n in self.corpus if n not in known)


def split_cells(line: str) -> list[str] | None:
    """Split one markdown table row into cells, honouring `\\|` escapes.

    Returns None for a line that is not a table row. The escape handling is not decoration:
    the live ledger's verbatim-quote column contains escaped pipes, and ignoring them
    silently truncates real rows (module docstring).
    """
    # A line indented 4+ columns is an INDENTED CODE BLOCK in CommonMark, i.e. an example
    # rather than a table (terra HIGH, round 4 -- the same "documentation becomes evidence"
    # class the fence tracker handles, reached without a fence). The ruled ledger is never
    # indented; the live one starts at column 0.
    if len(line) - len(line.lstrip(" ")) >= 4:
        return None
    s = line.strip()
    if not s.startswith("|"):
        return None
    s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells: list[str] = []
    buf: list[str] = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            buf.append("|")
            i += 2
            continue
        if ch == "|":
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    cells.append("".join(buf).strip())
    return cells


_SEPARATOR_CELL_RE = re.compile(r"^:?-+:?$")


def _is_separator(cells: list[str], width: int) -> bool:
    """A markdown header-separator row (`|---|:--:|`) of exactly `width` columns.

    THE WIDTH MATCH IS THE DISCRIMINATING HALF (terra HIGH, round 2). A real table's separator
    always carries the same column count as its header, so requiring the match refuses a
    fabricated pseudo-table without refusing any well-formed one.

    A minimum HYPHEN count was proposed and deliberately NOT adopted: a single hyphen is valid
    markdown, so a three-hyphen floor would false-WARN a genuinely well-formed ledger -- and a
    false WARN is the one failure this leg cannot afford, because it corrupts the very evidence
    a later hard flip would rest on.
    """
    return (len(cells) == width and bool(cells)
            and all(_SEPARATOR_CELL_RE.match(c.strip()) for c in cells))


def _normalise_header(cell: str) -> str:
    """A header cell, stripped of presentation. `**File**` / `` `file` `` -> `file`.

    Disposition cells were normalised from the start and header cells were matched RAW, so a
    perfectly valid table headed `| **File** | ... |` was invisible (terra HIGH, round 2). That
    is a FALSE-WARN bug rather than an evasion: every artifact such a ledger dispositioned
    would have been reported uncovered.
    """
    return cell.strip().strip(_PRESENTATION_CHARS).strip().lower()


_PRESENTATION_CHARS = "*`_ "


def _normalise_term(cell: str) -> str:
    """`**ACTIONED**` / `` `actioned` `` / `__FILED__` -> the bare upper-cased term.

    Strips the SAME presentation set `_normalise_header` does. Stripping only `*` was an
    inconsistency between the two, and a FALSE-WARN one (terra HIGH, round 5): a valid cell
    written `` `ACTIONED` `` read as malformed, leaving a genuinely dispositioned artifact
    uncovered while the header beside it normalised fine.
    """
    return cell.strip().strip(_PRESENTATION_CHARS).strip().upper()


def scan_ledger(text: str, source: str) -> list[LedgerRow]:
    """Every ledger row in one document. Walks EVERY table and EVERY row ([#560] lesson).

    A table is a ledger only if its header carries a file-ish column, a `disposition` column
    AND an `evidence locator` column. The locator column is REQUIRED because the ruling makes
    the citation part of the disposition -- a term with nothing to resolve is not one.
    """
    rows: list[LedgerRow] = []
    lines = _blank_fenced_regions(text.splitlines())
    i = 0
    while i < len(lines):
        header = split_cells(lines[i])
        if header is None or len(header) < 3:
            i += 1
            continue
        lowered = [_normalise_header(c) for c in header]
        if (_DISPOSITION_HEADER not in lowered
                or _LOCATOR_HEADER not in lowered
                or not any(c in _FILE_HEADERS for c in lowered)):
            i += 1
            continue
        file_idx = next(k for k, c in enumerate(lowered) if c in _FILE_HEADERS)
        disp_idx = lowered.index(_DISPOSITION_HEADER)
        loc_idx = lowered.index(_LOCATOR_HEADER)
        widest = max(file_idx, disp_idx, loc_idx)

        # The separator row is REQUIRED (sol route 6; terra HIGH, round 1). While it was
        # optional, any two consecutive pipe-prefixed prose lines were a ledger -- so the
        # entry price for a fabricated disposition was two lines that are not even a table.
        # A real markdown table always carries it; the live ledger does.
        j = i + 1
        sep = split_cells(lines[j]) if j < len(lines) else None
        if sep is None or not _is_separator(sep, len(header)):
            i += 1
            continue
        j += 1
        while j < len(lines):
            body = split_cells(lines[j])
            if body is None:
                break                     # the table itself ended
            # A SHORT row is a malformed row, NOT the end of the table (terra HIGH, round 1).
            # Breaking here meant one `| note |` line between two ledger rows silently
            # discarded every row after it -- the same stop-early class as [#560], reached by
            # a different route, and it would have reported dispositioned artifacts as newly
            # uncovered.
            if len(body) > widest:
                match = _AUDIT_NAME_RE.search(body[file_idx])
                if match:
                    rows.append(LedgerRow(audit=match.group(1),
                                          term=_normalise_term(body[disp_idx]),
                                          locator=body[loc_idx].strip(),
                                          ledger=source))
            j += 1
        i = j
    return rows


def locator_resolves(row: LedgerRow, corpus: set[str]) -> bool:
    """Does this row's locator carry a reference of the kind its term promises?

    NOT a resolution of the reference -- except for SUPERSEDED, where the successor must
    actually be in the corpus, because that one costs nothing to check and a successor that
    does not exist is not evidence of anything. For ACTIONED and FILED this is SHAPE only: a
    sha-shaped token, an id-shaped token. See `_LOCATOR_SHAPES` for the measurement behind
    each pattern and for why REJECTED is deliberately unshaped.

    HONEST LIMIT, and it is the residual sol named: a well-shaped FABRICATION passes.
    `ACTIONED | deadbeef1` is admitted without `deadbeef1` being a real commit. Closing that
    needs a batched `git cat-file` for shas and a `tasks/` liveness join for ids -- the second
    of which is the P-2 orphan work this lane is scoped out of.
    """
    if not row.locator:
        return False
    shape = _LOCATOR_SHAPES.get(row.term)
    if shape is None:
        # REJECTED. No SHAPE rule is possible -- see `_LOCATOR_SHAPES` -- but `REJECTED | x`
        # is plainly not "a ruling declined it, cite it" either (terra HIGH, round 4). A
        # SUBSTANCE floor is the only rule the corpus supports, and it is the weakest in this
        # module: it distinguishes a recorded reason from a token, and nothing more. Measured:
        # the two live REJECTED locators are 144 and 253 characters, so the floor clears them
        # by ~6x and rejects every one-word dodge.
        return len(row.locator) >= _REJECTED_MIN_LOCATOR
    found = shape.search(row.locator)
    if found is None:
        return False
    if row.term == "SUPERSEDED":
        return found.group(1) in corpus
    return True


def _blank_fenced_regions(lines: list[str]) -> list[str]:
    """Blank out fenced code regions, PRESERVING line indices so the scanner is unaffected.

    See `_FENCE_RE` for why this exists. Honest limit: this tracks ``` / ~~~ fences opened at
    up to three columns of indentation, which is CommonMark's rule; it does not model
    indented code blocks or fences nested inside list items at deeper indentation. Those
    would read as ordinary text, which is the same failure the un-fenced scanner had -- so
    this narrows the hole rather than closing it, and says so.
    """
    out: list[str] = []
    opener: str | None = None
    in_comment = False
    for line in lines:
        # HTML comments are the other way a document carries an example it does not mean
        # (terra HIGH, round 4). Handled before fences: a comment may contain a fence marker.
        if in_comment:
            out.append("")
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line and "-->" not in line.split("<!--", 1)[1]:
            in_comment = True
            out.append("")
            continue
        fence = _FENCE_RE.match(line)
        if fence:
            mark = fence.group("mark")
            if opener is None:
                opener = mark
            elif (mark[0] == opener[0] and len(mark) >= len(opener)
                    and not fence.group("rest").strip()):
                # A CLOSING fence carries only whitespace after its marker (CommonMark), so
                # ```` ```python ```` INSIDE a block is an opener-shaped line, not a closer
                # (terra HIGH, round 3). Treating it as a closer let a ledger further down the
                # same code block become live evidence -- the third variant of the one hole,
                # after "any fence closes" and "a shorter fence closes".
                # Close ONLY on the same character, at least as long (terra HIGH, round 2).
                # Toggling on any fence meant a ``` example nested inside a ```` block closed
                # the OUTER fence, so a ledger later in that same code example was scanned as
                # real evidence -- reopening the exact hole this tracker was added to close,
                # one level down.
                opener = None
            out.append("")
            continue
        out.append("" if opener is not None else line)
    return out


def measure(repo_root: Path) -> Measurement:
    """Walk `docs/audits/`, parse every ledger, and classify the corpus.

    Raises FunnelCoverageError only when the directory itself is unreadable. A corpus with
    zero dispositions is a MEASUREMENT, not an error -- the whole point is to report it.
    """
    audits_dir = Path(repo_root) / AUDITS_RELPATH
    if not audits_dir.is_dir():
        raise FunnelCoverageError(f"{AUDITS_RELPATH} is not a directory under {repo_root}")

    try:
        paths = sorted(audits_dir.glob("*.md"))
    except OSError as exc:
        raise FunnelCoverageError(f"could not list {AUDITS_RELPATH}: {exc!r}") from exc

    m = Measurement()
    m.corpus = sorted(p.name for p in paths if p.name not in CORPUS_EXCLUDE)
    corpus_set = set(m.corpus)

    # THE MANIFEST-LINK ROUTE (operator ruling, 2026-09-05). An artifact a batch manifest
    # links -- via `closed_by:`, as a lane packet, or as a close packet -- is dispositioned by
    # that link. Library-first: `batch_manifest` already owns manifest discovery, frontmatter
    # parsing and the lane-slug grammar, so none of it is re-derived here. Import is LOCAL to
    # keep module import order free of a cycle (`consumer_at_landing` imports this module).
    try:
        import batch_manifest as _bm
    except ImportError:  # pragma: no cover - both import shims are installed in-tree
        from scripts import batch_manifest as _bm
    links = _bm.manifest_links(Path(repo_root))
    for name in m.corpus:
        kind = _bm.links_artifact(links, name)
        if kind is not None:
            m.manifest_linked[name] = kind

    for p in paths:
        try:
            # STRICT decoding, and a decode failure RAISES (terra HIGH, round 5). This repo has
            # the lesson already recorded, in `silent_rule_detector`: its arm-time probe used a
            # platform default and "SILENTLY ZEROED several files before erroring -- a silent
            # decode failure is the exact measurement-error class this metric must not
            # reproduce". `errors="replace"` reproduced it here: an unreadable byte anywhere in
            # the corpus left the ratchet passing on a read that had partly failed.
            text = p.read_text(encoding="utf-8")
        except OSError as exc:
            raise FunnelCoverageError(f"could not read {p.name}: {exc!r}") from exc
        except UnicodeDecodeError as exc:
            raise FunnelCoverageError(
                f"{p.name} is not valid UTF-8 ({exc}); the corpus was not fully read, so no "
                f"coverage number from this run is trustworthy") from exc
        rows = scan_ledger(text, p.name)
        if rows:
            m.ledgers.append(p.name)
        for row in rows:
            if row.audit not in corpus_set:
                # A ledger row naming an artifact that is not on disk. Reported, never
                # silently dropped: it is either a relocation or a typo, and both are the
                # ledger rotting rather than the corpus being covered.
                m.dangling.append(row)
                continue
            if row.term in DISPOSITION_TERMS and locator_resolves(row, corpus_set):
                m.dispositioned.setdefault(row.audit, row)
            elif row.term == PENDING_TERM and "?" in row.locator:
                # PENDING REQUIRES ITS QUESTION, punctuated. The ruling admits the undecidable
                # case as "PENDING with the exact question it needs", so neither a blank
                # locator (sol route 6) nor arbitrary text (terra HIGH, round 4) is the
                # ruling's PENDING. Both live PENDING rows open with `Q:` and contain `?`, so
                # requiring the mark cost 0 false positives.
                m.pending.setdefault(row.audit, row)
            else:
                # An off-vocabulary term, a ruled term whose locator is empty or the wrong
                # shape, or a blank PENDING. None is coverage -- and all are surfaced,
                # because a malformed row is a LEDGER DEFECT and looks nothing like an
                # unledgered file. Collapsing the two would hide a rotting ledger inside a
                # backlog number.
                m.malformed.append(row)

    m.ledgers.sort()
    return m


def render_baseline(m: Measurement, measured_at: str, measured_at_sha: str,
                    provenance: str) -> str:
    """Render the committed ratchet baseline as JSON.

    THE BASELINE NAMES FILES, NOT A COUNT, and that is the one place this ratchet is
    deliberately stronger than `[#436]`'s. A bare integer baseline is satisfied by
    dispositioning one old artifact while adding one new undispositioned one -- net zero,
    debt unchanged, gate silent. An identity set cannot be gamed that way: the check reports
    `live - baseline`, so a NEW uncovered artifact surfaces BY NAME even while the total
    falls. The silent-rule ratchet could not do this because its metric is an occurrence
    count with no attribution; here the unit is a filename, so the stronger form is free.

    `artifacts` may SHRINK (drain a name by ledgering that artifact) or hold. Adding a name
    is a RAISE -- it excuses an artifact that was skipped -- and it is a curated-baseline
    touch, i.e. an operator decision. HONEST LIMIT, stated rather than left to be found:
    nothing REFUSES a raise. The teeth are the named WARN, the attributable one-line diff,
    and the decision-budget rule -- not a code path. See the lane artifact's sol section.
    """
    payload = {
        "_": ("Committed baseline for the audit funnel-coverage ratchet (M3). Regenerate: "
              "python scripts/funnel_coverage.py --write-baseline. Contract, semantics and "
              "honest limits: scripts/funnel_coverage.py (module docstring + render_baseline)."),
        "detector_id": m.detector_id,
        "measured_at": measured_at,
        "measured_at_sha": measured_at_sha,
        "corpus": len(m.corpus),
        "dispositioned": len(m.dispositioned),
        "pending": len(m.pending),
        "uncovered": len(m.uncovered),
        "provenance": provenance.strip(),
        # The uncovered set enumerated by name -- closure-contract item 1. This IS the
        # enumeration; the lane artifact points here rather than restating 613 filenames in
        # prose (CLAUDE.md Sec.4: cite the surface that computes a roster, do not retype it).
        "artifacts": list(m.uncovered),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def load_baseline(repo_root: Path) -> dict | None:
    """Read the committed baseline, or None when it is absent/unreadable/malformed.

    None is a MEASUREMENT-refusing state, not a default: the caller reports an inert ratchet
    rather than treating a missing baseline as an empty one. An empty baseline would make
    every one of the 613 pre-existing artifacts read as a fresh regression, which is how a
    ratchet turns into noise on its first bad read.
    """
    path = Path(repo_root) / BASELINE_RELPATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get("artifacts"), list):
        return None
    if not all(isinstance(a, str) for a in data["artifacts"]):
        return None
    # The declared count must agree with the list it counts. This refuses sol's laziest raise
    # -- append one filename, leave the numbers alone -- so excusing an artifact by hand takes
    # a deliberate edit to the very number it contradicts rather than a single appended line.
    # `uncovered` is REQUIRED, not merely checked-when-present (terra MEDIUM, round 2): an
    # absent field silently disabled the very integrity guard a hand-edit was supposed to trip.
    # DUPLICATES are refused (terra MEDIUM, round 5). The ratchet compares SETS, so
    # `{"uncovered": 2, "artifacts": ["a.md", "a.md"]}` satisfied the count check and then
    # collapsed to one identity -- the declared count agreed with the LIST while disagreeing
    # with the identity set the ratchet actually uses, which is the only number that matters.
    if len(set(data["artifacts"])) != len(data["artifacts"]):
        return None
    declared = data.get("uncovered")
    if not isinstance(declared, int) or isinstance(declared, bool):
        return None
    if declared != len(data["artifacts"]):
        return None
    return data


CHECK_NAME = "funnel_coverage"


def ratchet_findings(m: Measurement, baseline: dict | None) -> list[tuple[str, str]]:
    """The ratchet verdict as `(status, evidence)` pairs. PURE -- no filesystem, no git.

    Returns tuples rather than `Finding` objects so this module imports nothing from
    `audit`; the facade wrapper maps them. That keeps the four contract cases
    (pass-at-baseline, warn-on-regression, ratchet-down accepted, identity-swap refused)
    pinned without standing up a repo, and keeps the detector standalone.

    WARN-TIER BY RULING, and there is deliberately NO code path to a hard verdict here.
    The architect's ruling on this lane is explicit: arm as WARN against a zero-baseline
    ratchet, because arming RED against an unmeasured corpus turns the gate off on day one
    -- everyone routes around a gate that blocks work for a debt they did not create. The
    flip to RED is a later act with its own ruling. `tests/test_funnel_coverage.py`
    asserts the absence of a hard-verdict literal AT SOURCE LEVEL, because an
    observational test only proves such a path was not REACHED, which is exactly what a
    latent one looks like.

    ONE FINDING PER CONCERN, never a bundle. The #147 register suppresses an ENTIRE
    Finding on a substring match, so a bundled Finding lets one dispositioned artifact
    wave through every other regression sharing the line. `git_backlog_drift` emits one
    per drifted id for this reason, and `[#560]` records "bundled Finding" as a live
    structural rider in `review_artifact_coverage`. Not repeated here.
    """
    if baseline is None:
        return [("warn",
                 f"no readable {BASELINE_RELPATH} -- ratchet INERT (live uncovered "
                 f"{len(m.uncovered)} of {len(m.corpus)}); the gate is not measuring "
                 f"anything")]

    stamped = baseline.get("detector_id")
    if stamped != m.detector_id:
        return [("warn",
                 f"detector mismatch: baseline stamped {stamped!r} but live measurement "
                 f"produced by {m.detector_id!r} -- the two are not commensurable; "
                 f"re-measure and re-stamp rather than comparing them")]

    baseline_set = set(baseline["artifacts"])
    live_set = set(m.uncovered)
    corpus_set = set(m.corpus)

    # THE IDENTITY LEG, and the reason this ratchet is not a counter. `live - baseline`
    # names artifacts that are uncovered NOW and were not part of the arm-time debt. A
    # count-based ratchet is satisfied by draining one old artifact while adding one new
    # undispositioned one: total unchanged, debt unchanged, gate silent. Here that swap
    # still surfaces, by name.
    regressions = sorted(live_set - baseline_set)
    drained = sorted(baseline_set - live_set)
    stale = sorted(baseline_set - corpus_set)

    out: list[tuple[str, str]] = []
    for name in regressions:
        out.append(("warn",
                    f"{name} carries no disposition and is not in the arm-time baseline -- "
                    f"record one of {'/'.join(DISPOSITION_TERMS)} with an evidence locator "
                    f"in a ledger row (architect ruling 2026-08-17), or {PENDING_TERM} with "
                    f"the exact question it needs"))
    for row in m.malformed:
        out.append(("warn",
                    f"{row.ledger} carries a ledger row for {row.audit} whose disposition "
                    f"{row.term!r} is outside the ruled set or whose evidence locator is "
                    f"empty -- a term with nothing to resolve is not a disposition"))
    for row in m.dangling:
        out.append(("warn",
                    f"{row.ledger} carries a ledger row naming {row.audit}, which is not "
                    f"present in {AUDITS_RELPATH}/ -- a relocated or mistyped locator, not "
                    f"coverage"))
    for name in stale:
        out.append(("warn",
                    f"the baseline names {name}, which is no longer present in "
                    f"{AUDITS_RELPATH}/ -- drain the entry rather than carrying a debt for "
                    f"an artifact that does not exist"))
    if out:
        return out

    headroom = len(baseline_set) - len(live_set)
    drain_note = (f"; {headroom} drained since arm time "
                  f"({', '.join(drained[:3])}{'...' if len(drained) > 3 else ''}) -- "
                  f"ratchet-down available" if drained else "")
    return [("pass",
             f"{len(m.dispositioned)} of {len(m.corpus)} artifact(s) in {AUDITS_RELPATH}/ "
             f"carry a ruled disposition with a locator, {len(m.pending)} are "
             f"{PENDING_TERM}, and no undispositioned artifact is outside the arm-time "
             f"baseline of {len(baseline_set)}{drain_note}")]


def render_report(m: Measurement) -> str:
    """Human-readable census. Used by `--report` and quoted into the lane artifact."""
    lines = [
        f"detector      {m.detector_id}",
        f"corpus N      {len(m.corpus)}   ({AUDITS_RELPATH}/*.md, excluding "
        f"{', '.join(sorted(CORPUS_EXCLUDE))})",
        f"ledgers       {len(m.ledgers)}   {', '.join(m.ledgers) or '(none)'}",
        f"dispositioned {len(m.dispositioned)}",
        f"pending       {len(m.pending)}",
        f"uncovered     {len(m.uncovered)}",
        f"malformed     {len(m.malformed)}",
        f"dangling      {len(m.dangling)}",
        "",
        "by term:",
    ]
    for term in DISPOSITION_TERMS:
        n = sum(1 for r in m.dispositioned.values() if r.term == term)
        lines.append(f"  {term:<11} {n}")
    return "\n".join(lines)


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo-root", default=".", help="repository root (default: cwd)")
    ap.add_argument("--report", action="store_true", help="print the census")
    ap.add_argument("--list-uncovered", action="store_true",
                    help="print every uncovered artifact, one per line")
    ap.add_argument("--write-baseline", action="store_true",
                    help=f"regenerate {BASELINE_RELPATH} from the live measurement")
    ap.add_argument("--measured-at", default="", help="date stamp for --write-baseline")
    ap.add_argument("--measured-at-sha", default="", help="sha stamp for --write-baseline")
    ap.add_argument("--provenance-file", default="",
                    help="path to a text file whose contents become the provenance block")
    ap.add_argument("--allow-raise", action="store_true",
                    help="permit --write-baseline to ADD names (a curated-baseline touch)")
    ap.add_argument("--recover-corrupt-baseline", action="store_true",
                    help="permit --write-baseline to REPLACE an unreadable baseline "
                         "(a distinct act from --allow-raise; destroys the damaged evidence)")
    args = ap.parse_args(argv)
    try:
        m = measure(Path(args.repo_root))
    except FunnelCoverageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.list_uncovered:
        for name in m.uncovered:
            print(name)
        return 0
    if args.write_baseline:
        # THE TOOL WILL NOT SILENTLY BLESS NEW DEBT (sol route 5). Re-running --write-baseline
        # was a one-command way to excuse every currently-uncovered artifact, which made the
        # cheapest evasion cheaper than the honest act. A DRAIN still needs no flag -- making
        # the right thing harder than doing nothing would be worse than no tool at all -- but
        # a RAISE is refused, names every artifact it would have excused, and requires an
        # explicit --allow-raise, which is a curated-baseline touch and therefore operator work.
        # BOOTSTRAP AND CORRUPTION ARE NOT THE SAME STATE (terra HIGH, round 3). `load_baseline`
        # returns None for both, so keying the guard on it alone meant DELETING or corrupting
        # the committed baseline silently blessed every regression -- an attacker-free,
        # one-command defeat of the identity ratchet. A genuinely absent file is a first arm;
        # a present-but-unreadable one is indeterminate, and an indeterminate baseline must not
        # be replaced without the operator saying so.
        baseline_path = Path(args.repo_root) / BASELINE_RELPATH
        existing = load_baseline(Path(args.repo_root))
        # CORRUPTION RECOVERY IS ITS OWN ACT, not a raise (terra HIGH, round 5). `--allow-raise`
        # says "I accept adding these named artifacts to the debt"; overwriting an unreadable
        # baseline says "I accept destroying the only evidence that the baseline was damaged".
        # Folding the second into the first let one flag do both, so the recovery needs its own
        # word and leaves its own trace in a shell history and a commit message.
        if existing is None and baseline_path.exists() and not args.recover_corrupt_baseline:
            print(f"funnel_coverage: REFUSING to overwrite {BASELINE_RELPATH} -- it exists but "
                  f"could not be read as a valid baseline, so a raise cannot be ruled out. "
                  f"Repair it, or pass --recover-corrupt-baseline deliberately (NOT "
                  f"--allow-raise, which is a different act).", file=sys.stderr)
            return 2
        if (existing is not None and not args.allow_raise
                and existing.get("detector_id") != m.detector_id):
            # A DETECTOR CHANGE makes the two sets incommensurable (terra HIGH, round 4).
            # Without this, a predicate revision that happens to LOWER the count reads as a
            # drain, quietly writes the new detector id, and the mismatch WARN never fires
            # again -- silently rebasing a measurement nobody reviewed, which is the exact
            # failure `[#436]`'s detector-id discipline exists to prevent.
            print(f"funnel_coverage: REFUSING to rebaseline across a detector change "
                  f"({existing.get('detector_id')!r} -> {m.detector_id!r}) -- the two "
                  f"measurements are not commensurable. Re-arm deliberately with "
                  f"--allow-raise after reviewing the re-measurement.", file=sys.stderr)
            return 2
        if existing is not None and not args.allow_raise:
            added = sorted(set(m.uncovered) - set(existing["artifacts"]))
            if added:
                print(f"funnel_coverage: REFUSING to raise the baseline -- {len(added)} "
                      f"artifact(s) would be ADDED, i.e. excused without a disposition:",
                      file=sys.stderr)
                for name in added:
                    print(f"  + {name}", file=sys.stderr)
                print("Disposition them in a ledger, or pass --allow-raise deliberately.",
                      file=sys.stderr)
                return 2
        provenance = (Path(args.provenance_file).read_text(encoding="utf-8")
                      if args.provenance_file else "")
        target = Path(args.repo_root) / BASELINE_RELPATH
        target.write_text(
            render_baseline(m, args.measured_at, args.measured_at_sha, provenance),
            encoding="utf-8", newline="\n")
        print(f"funnel_coverage: wrote {BASELINE_RELPATH} "
              f"({len(m.uncovered)} uncovered of {len(m.corpus)})")
        return 0
    print(render_report(m))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
