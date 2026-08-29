#!/usr/bin/env python
"""funnel_lifecycle.py -- the detector behind the FM-2 funnel-lifecycle leg.

THE GAP, in the repo's own words. `docs/intake/README.md` section 5 rules the exit step of the
intake funnel and then states, verbatim, that nothing enforces it:

    Terminal docs (CONSUMED | SUPERSEDED | REJECTED) relocate byte-identical to
    `docs/intake/archive/` ... The move is MANUAL for now -- **the status-coupled validator
    that would gate/automate it is wave work, not built.**

This module is that validator. It asks four questions about governed objects that have reached
the END of their lifecycle and did not leave it.

EXTENDS THREE EXISTING ORGANS, RIVALS NONE. Stated explicitly because two answers to "is this
intake consumed?" is the failure mode, not the fix:

  * `funnel_coverage` (M3) asks whether an audit artifact was DISPOSITIONED. Corpus
    `docs/audits/`, unit = artifact, question = triage. It never reads `docs/intake/`,
    `docs/decisions/` or `tasks/`.
  * `consumer_at_landing` ([#595]) asks whether a landed audit artifact is CITED by a
    governance surface. Same corpus as above, opposite direction, and its POOL includes
    `docs/intake/` and `tasks/` as CITERS -- never as subjects.
  * `intake_tree_coherence` ([#383]) asks whether the `docs/intake/` residue CARRIER
    (`manifest.json` + the generated index) regenerates byte-identically. It is a
    regen-and-diff gate over the derived artifact and is blind to what the frontmatter SAYS:
    the 2026-08-29 census (`docs/audits/2026-08-29-census-nb2-funnel.md` D1) measured it
    reproducing a WRONG index byte-for-byte and staying green through six broken docs.

  WHAT THIS ADDS: nothing above reads an object's STATUS and asks whether its LOCATION and its
  provenance still agree with that status. That is the whole question here, and it is why the
  resolvers are BORROWED rather than rewritten -- `gen_intake_index._parse_frontmatter` for
  intake frontmatter, `validate_adr_status.scan_zone` + `TERMINAL_STATUSES` for ADR status,
  `gen_task_tree.frontmatter_id/frontmatter_status/extract_body` for rows, and
  `consumer_at_landing.ARM_DATE` for the cutoff.

THE FOUR LEGS.

  a1  FAIL  an intake doc at a TERMINAL status (CONSUMED | SUPERSEDED | REJECTED) still sitting
            at `docs/intake/` depth 1 -- ruled by `docs/intake/README.md` section 5.
  a2  FAIL  an intake doc at ACCEPTED whose `consumed-by:` names at least one `[#id]` row and
            EVERY named row is terminal -- consumed in substance, status never flipped. The
            ">= 1 named row" bar is load-bearing: "all rows terminal" over an EMPTY set is
            vacuously true and would flag every ACCEPTED doc that names no row, which is the
            standing-authority class ADR-98 deliberately keeps live (intake #28 / ADR-112).
  b   FAIL  a live ADR at a status in `validate_adr_status.TERMINAL_STATUSES` still sitting in
            `docs/decisions/` rather than `docs/decisions/archive/`.
  c   FAIL  a `tasks/` row born on/after `consumer_at_landing.ARM_DATE` whose provenance clause
            is absent or resolves to nothing.
  d   WARN  an intake doc at READY older than the ruled threshold with no recorded review date.

WHY LEG (c) READS `refs` AND NOT `source:`. The FM-2 contract defines leg (c) against a
`source:` frontmatter key. That key DOES NOT EXIST: the live `tasks/` schema is
`id | title | status | priority | size | theme | story | generates`, measured at 0 of 343 rows
carrying `source:` (census P1, re-derived here 2026-08-29). The de-facto provenance clause is
the row body's `* refs ...`, carried by 151 of 151 OPEN rows on the merged tree. This module
takes that substitute and says so rather than inventing the missing field; growing `tasks/` a
`source:` key is a schema change to the backlog source of truth and is a ruling, not a check.

WHY LEG (d) CAN BE INERT, AND WHY THAT IS NOT A Z-G4 SKIP. The READY-age threshold is a
DOCTRINE CONSTANT that FM-1 rules and lands in `protocols/`. `docs/intake/README.md` section 7
carries only the prose figure "~1 month", which is not a number a gate may act on. When no
ruled threshold is found this leg emits a WARN naming the absence -- a REPORTED GAP, which is
exactly what Z-G4 requires ("a `skipped` status is a reported gap, never a pass"). It does NOT
FAIL, because Z-G4 governs a check that cannot compute the ground truth OF A RULE THAT EXISTS;
arming a hard refusal against a threshold nobody ruled would be the invented-constant drift
this organ exists to stop. Every OTHER cannot-compute condition here DOES raise, and the
adapter renders it `fail`.

Z-G4 CONDITIONS, ENUMERATED. Each raises `LifecycleUnreadable`:
  * an intake/ADR/row file that cannot be read;
  * an intake `.md` whose frontmatter parses to `{}` -- the exact D1 case, where
    `gen_intake_index._parse_frontmatter` swallows a YAML error and the doc silently loses its
    id AND its status. A doc with no computable status is not a doc with no status;
  * `validate_adr_status.CorpusUnusable`;
  * a `git log` that cannot produce row birth dates, so leg (c)'s cutoff is uncomputable.

HONEST LIMITS -- they bound what a green verdict means:
  * Leg a2 reads `consumed-by:`, which today NO live ACCEPTED intake carries with a row token
    (measured 0 of 18, 2026-08-29). The leg is correct and armed, and it is near-inert until
    the field is used that way. That is a schema-adoption gap, reported rather than papered.
  * Leg (d) measures DOCUMENT AGE from the filename date, not TIME-AT-READY. The intake schema
    records no dated transitions, so a doc that reached READY yesterday after two months at
    DRAFT is aged from its birth. Under A1 ("every governed object carries explicit state +
    dated transitions") that is a real gap in the SCHEMA, not something a check can fix.
  * Leg (c) asks whether a provenance token RESOLVES, never whether it is the RIGHT one. A row
    citing an unrelated but existing ADR passes.
  * A bare `#N` is deliberately NOT resolved against the intake id namespace. Both namespaces
    start at 1 (census section 4.2 measured 8 open rows on that ambiguity), and a FAIL-armed
    leg must not resolve a token two ways to find one that works.
  * Nothing here MOVES a file. A gate that silently fixes what it measures cannot fail.

READ-ONLY and Layer-2 (ADR-28/36): it writes nothing, drives no state, and its only subprocess
is a read-only `git log`.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

try:
    from scripts import consumer_at_landing as _cal
    from scripts import gen_intake_index as _gii
    from scripts import gen_task_tree as _gtt
    from scripts import validate_adr_status as _vas
except ImportError:  # running with scripts/ itself on the path
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import consumer_at_landing as _cal
    import gen_intake_index as _gii
    import gen_task_tree as _gtt
    import validate_adr_status as _vas


CHECK_NAME = "funnel_lifecycle"
DETECTOR_ID = "funnel-lifecycle/v1"

INTAKE_RELPATH = "docs/intake"
INTAKE_ARCHIVE_RELPATH = "docs/intake/archive"
DECISIONS_RELPATH = "docs/decisions"
DECISIONS_ARCHIVE_RELPATH = "docs/decisions/archive"
TASKS_RELPATH = "tasks"

#: `docs/intake/README.md` section 5, verbatim: "Terminal docs (CONSUMED | SUPERSEDED |
#: REJECTED) relocate byte-identical to `docs/intake/archive/`". ACCEPTED is deliberately NOT
#: in this set -- "a standing authority must stay visible live" -- which is why leg a2 exists
#: as a separate, differently-shaped question.
TERMINAL_INTAKE_STATUSES = frozenset({"CONSUMED", "SUPERSEDED", "REJECTED"})
ACCEPTED_STATUS = "ACCEPTED"
READY_STATUS = "READY"

#: Row statuses that count as done, copied from `gen_task_tree._TERMINAL_STATUSES` rather than
#: re-declared, so the two cannot drift.
TERMINAL_ROW_STATUSES = frozenset(_gtt._TERMINAL_STATUSES)

#: The cutoff for leg (c). REUSED from `consumer_at_landing`, never a second constant: the two
#: legs grandfather the same corpus for the same reason and a divergence would be silent.
ARM_DATE = _cal.ARM_DATE

#: FM-1's ruled READY threshold binds HERE, in this shape, anywhere under `protocols/`:
#:     READY threshold: 30 days
#: (case-insensitive; an optional leading list marker and optional `**` emphasis are allowed,
#: as is `intake READY threshold` / `READY-age threshold` / `=` for `:`). The shape is declared
#: rather than guessed at read time so that "FM-1 landed a different shape" is a REPORTED
#: mismatch and never a silently-invented number.
_READY_THRESHOLD_RE = re.compile(
    # HORIZONTAL whitespace only. `\s` after `^` matches a NEWLINE, so `^\s{0,4}` anchors on
    # the PRECEDING blank line and reports a locator one line early -- a caught-in-test
    # off-by-one, and a locator a reader cannot resolve is the failure this repo files most.
    r"^[ \t]{0,4}(?:[-*+][ \t]+)?\*{0,2}(?:intake[ \t]+)?READY(?:[- ]age)?[ \t]+threshold\*{0,2}"
    r"[ \t]*[:=][ \t]*\*{0,2}(?P<days>\d{1,4})[ \t]*days?\b",
    re.IGNORECASE | re.MULTILINE)

#: The provenance clause: a `refs` run introduced by the row-body separator and ending at the
#: next separator or end of body. `extract_body` hands back the row's own text, so the search
#: is scoped to one row.
_REFS_RE = re.compile(r"[·]\s*refs\s+(?P<body>.+?)(?=\s+[·]\s|\s*$)", re.S)

_INTAKE_TOKEN_RE = re.compile(r"intake[ -]#\s*(\d+)", re.IGNORECASE)
_ADR_TOKEN_RE = re.compile(r"\bADR-0*(\d+)\b")
_ROW_TOKEN_RE = re.compile(r"\[?#(\d+)\]?")
_PATH_TOKEN_RE = re.compile(
    r"[A-Za-z0-9_./-]+\.(?:md|py|yaml|yml|json|jsonl|ps1|toml|html|log|txt)\b")
_STEM_TOKEN_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2}-[A-Za-z0-9._-]+)\b")
_DATED_NAME_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-")

#: Directories whose dated stems a `refs` clause may name. Scanned one level deep only; that is
#: enough for every genre a row cites and keeps the walk to five `scandir` calls.
_STEM_DIRS = ("docs/audits", "docs/handoffs", "docs/intake", "docs/decisions", "docs/archive")

LEG_A1 = "terminal-not-archived"
LEG_A2 = "accepted-rows-terminal"
LEG_B = "adr-terminal-not-archived"
LEG_C = "row-provenance-unresolved"
LEG_D = "ready-past-threshold"


class LifecycleUnreadable(Exception):
    """Ground truth could not be computed -- the Z-G4 class. The adapter renders it `fail`."""


@dataclass(frozen=True)
class Violation:
    leg: str
    subject: str
    detail: str


@dataclass(frozen=True)
class IntakeDoc:
    path: Path
    relpath: str
    intake_id: str
    status: str
    fields: dict


@dataclass
class Measurement:
    detector: str = DETECTOR_ID
    live_intakes: int = 0
    archived_intakes: int = 0
    live_adrs: int = 0
    rows: int = 0
    post_cutoff_rows: int = 0
    ready_intakes: int = 0
    threshold_days: int | None = None
    threshold_locator: str | None = None
    violations: list[Violation] = field(default_factory=list)

    def by_leg(self, leg: str) -> list[Violation]:
        return [v for v in self.violations if v.leg == leg]


# --- readers ------------------------------------------------------------------------------

def _read(path: Path) -> str:
    """Strict-enough read. An unreadable governed file is a failed computation, never a skip."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise LifecycleUnreadable(f"unreadable: {path} ({exc})") from exc


def read_intake_dir(directory: Path, repo_root: Path) -> list[IntakeDoc]:
    """Every `*.md` under `directory` except `README.md`, parsed with the GENERATOR's parser.

    A `{}` parse RAISES rather than yielding a status-less doc. That is the D1 defect made
    loud: `_parse_frontmatter` returns `{}` on malformed YAML by design so the generated index
    can carry on, and the six docs it hit lost their id and their status while
    `intake-index-freshness` stayed green because regen-and-diff reproduces a wrong index
    exactly. A status this module cannot read is a ground truth it cannot compute (Z-G4).
    """
    if not directory.is_dir():
        return []
    out: list[IntakeDoc] = []
    for p in sorted(directory.glob("*.md")):
        if p.name == "README.md":
            continue
        fm = _gii._parse_frontmatter(_read(p))
        rel = p.relative_to(repo_root).as_posix()
        if not fm:
            raise LifecycleUnreadable(
                f"{rel}: frontmatter parsed to {{}} -- id and status are both unreadable, so "
                f"its lifecycle position cannot be computed (Z-G4)")
        out.append(IntakeDoc(
            path=p, relpath=rel,
            intake_id=(fm.get("intake-id", "") or "").strip(),
            status=(fm.get("status", "") or "").strip().upper(),
            fields=fm))
    return out


def ready_threshold(repo_root: Path) -> tuple[int | None, str | None]:
    """FM-1's ruled READY threshold as `(days, "path:line")`, or `(None, None)` when absent.

    Scans `protocols/*.md` only -- the contract names `protocols/` as where FM-1 lands it, and
    widening the scan would let an arbitrary audit or draft arm a gate.
    """
    protocols = repo_root / "protocols"
    if not protocols.is_dir():
        return (None, None)
    for p in sorted(protocols.glob("*.md")):
        text = _read(p)
        m = _READY_THRESHOLD_RE.search(text)
        if m:
            line = text.count("\n", 0, m.start()) + 1
            return (int(m.group("days")),
                    f"{p.relative_to(repo_root).as_posix()}:{line}")
    return (None, None)


def _row_files(repo_root: Path) -> list[Path]:
    """The ACTIVE queue only: `tasks/*.md` matching the engine's own orphan pattern.

    `tasks/archive/` is deliberately excluded -- those are archived row BODIES landed by
    [#612], not rows in the queue, and `gen_task_tree` does not enumerate them either.
    """
    tasks = repo_root / TASKS_RELPATH
    if not tasks.is_dir():
        return []
    return [p for p in sorted(tasks.glob("*.md")) if _gtt._ORPHAN_RE.match(p.name)]


def _row_birth_dates(repo_root: Path) -> dict[str, str]:
    """`{repo-relative path: ISO date of the commit that ADDED it}` for `tasks/`.

    ONE git call for the whole directory. A row git cannot date is NOT returned, and the caller
    treats an undated row as IN SCOPE rather than grandfathered: absence of evidence does not
    buy an exemption from a rule, which is the same direction Z-G4 points.
    """
    try:
        proc = subprocess.run(
            ["git", "log", "--diff-filter=A", "--name-only", "--format=%x00%ad",
             "--date=short", "--", f"{TASKS_RELPATH}/"],
            cwd=str(repo_root), capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=False)
    except OSError as exc:
        raise LifecycleUnreadable(
            f"git could not be run, so row birth dates -- leg (c)'s cutoff -- are "
            f"uncomputable: {exc}") from exc
    if proc.returncode != 0:
        raise LifecycleUnreadable(
            f"git log over {TASKS_RELPATH}/ exited {proc.returncode}, so row birth dates -- "
            f"leg (c)'s cutoff -- are uncomputable: {proc.stderr.strip()[:200]}")
    births: dict[str, str] = {}
    current = ""
    for line in proc.stdout.splitlines():
        if line.startswith("\x00"):
            current = line[1:].strip()
            continue
        name = line.strip()
        if name and current:
            births[name] = current   # newest-first walk, so the last write is the OLDEST add
    return births


# --- the provenance resolver ---------------------------------------------------------------

@dataclass(frozen=True)
class RefUniverse:
    row_ids: frozenset
    adr_numbers: frozenset
    intake_ids: frozenset
    stems: frozenset
    repo_root: Path

    def resolving(self, clause: str) -> list[str]:
        """Every token in `clause` that names an object this repo actually carries."""
        hits: list[str] = []
        intake_spans: list[tuple[int, int]] = []
        for m in _INTAKE_TOKEN_RE.finditer(clause):
            intake_spans.append(m.span())
            if m.group(1).lstrip("0") in self.intake_ids or m.group(1) in self.intake_ids:
                hits.append(f"intake #{m.group(1)}")
        for m in _ADR_TOKEN_RE.finditer(clause):
            if int(m.group(1)) in self.adr_numbers:
                hits.append(f"ADR-{m.group(1)}")
        for m in _PATH_TOKEN_RE.finditer(clause):
            token = m.group(0)
            if (self.repo_root / token).exists():
                hits.append(token)
        for m in _STEM_TOKEN_RE.finditer(clause):
            if m.group(1) in self.stems:
                hits.append(m.group(1))
        for m in _ROW_TOKEN_RE.finditer(clause):
            # A bare `#N` inside `intake #N` is NOT also read as a row id -- see the module
            # docstring's ambiguity limit.
            if any(lo <= m.start() < hi for lo, hi in intake_spans):
                continue
            if int(m.group(1)) in self.row_ids:
                hits.append(f"#{m.group(1)}")
        return hits


def build_ref_universe(repo_root: Path, row_ids: set, intake_docs: list[IntakeDoc]) -> RefUniverse:
    adr_numbers = set()
    for rel in (DECISIONS_RELPATH, DECISIONS_ARCHIVE_RELPATH):
        d = repo_root / rel
        if d.is_dir():
            for p in d.glob("ADR-*.md"):
                m = re.match(r"ADR-0*(\d+)", p.name)
                if m:
                    adr_numbers.add(int(m.group(1)))
    intake_ids = {d.intake_id.lstrip("0") or d.intake_id
                  for d in intake_docs if d.intake_id.isdigit()}
    intake_ids |= {d.intake_id for d in intake_docs if d.intake_id.isdigit()}
    stems = set()
    for rel in _STEM_DIRS:
        d = repo_root / rel
        if not d.is_dir():
            continue
        for child in d.iterdir():
            name = child.name[:-3] if child.name.endswith(".md") else child.name
            if _DATED_NAME_RE.match(name):
                stems.add(name)
    return RefUniverse(frozenset(row_ids), frozenset(adr_numbers), frozenset(intake_ids),
                       frozenset(stems), repo_root)


def refs_clause(body: str) -> str | None:
    """The row body's `* refs ...` provenance clause, or None when it carries none."""
    m = _REFS_RE.search(body)
    return m.group("body").strip() if m else None


# --- the measurement ------------------------------------------------------------------------

def measure(repo_root: Path, today: _dt.date | None = None) -> Measurement:
    """Run all four legs. Raises `LifecycleUnreadable` on any Z-G4 condition."""
    root = Path(repo_root)
    today = today or _dt.date.today()
    m = Measurement()

    live = read_intake_dir(root / INTAKE_RELPATH, root)
    archived = read_intake_dir(root / INTAKE_ARCHIVE_RELPATH, root)
    m.live_intakes, m.archived_intakes = len(live), len(archived)

    # --- rows (needed by a2 and c) ---------------------------------------------------------
    rows: dict[int, tuple[str, str, str]] = {}   # id -> (relpath, status, body)
    for p in _row_files(root):
        text = _read(p)
        rid = _gtt.frontmatter_id(text)
        if rid is None:
            continue
        try:
            body = _gtt.extract_body(text)
        except ValueError as exc:
            # A row whose body cannot be recovered has no readable provenance clause, and
            # "no clause found" would render as a leg-(c) verdict about a row that was never
            # parsed. Z-G4: report the failed computation, never a verdict drawn from it.
            raise LifecycleUnreadable(
                f"{p.relative_to(root).as_posix()}: row body unreadable ({exc}), so its "
                f"provenance clause cannot be computed") from exc
        rows[rid] = (p.relative_to(root).as_posix(),
                     (_gtt.frontmatter_status(text) or "").strip(), body)
    m.rows = len(rows)

    # --- leg a1 ----------------------------------------------------------------------------
    for doc in live:
        if doc.status in TERMINAL_INTAKE_STATUSES:
            m.violations.append(Violation(
                LEG_A1, doc.relpath,
                f"status {doc.status} is terminal but the doc sits at {INTAKE_RELPATH}/ depth 1 "
                f"-- docs/intake/README.md section 5 relocates it byte-identical to "
                f"{INTAKE_ARCHIVE_RELPATH}/"))

    # --- leg a2 ----------------------------------------------------------------------------
    for doc in live:
        if doc.status != ACCEPTED_STATUS:
            continue
        named = [int(x) for x in _ROW_TOKEN_RE.findall(doc.fields.get("consumed-by", ""))]
        if not named:
            continue
        unknown = [n for n in named if n not in rows]
        if unknown:
            continue   # a row this tree does not carry says nothing about terminality
        states = {n: rows[n][1] for n in named}
        if all(s in TERMINAL_ROW_STATUSES for s in states.values()):
            m.violations.append(Violation(
                LEG_A2, doc.relpath,
                "status ACCEPTED but every row its consumed-by names is terminal ("
                + ", ".join(f"#{n}={s}" for n, s in sorted(states.items()))
                + ") -- consumed in substance, status never flipped"))

    # --- leg b -----------------------------------------------------------------------------
    decisions = root / DECISIONS_RELPATH
    if decisions.is_dir():
        try:
            fields, _missing, _extra = _vas.scan_zone(decisions)
        except _vas.CorpusUnusable as exc:
            raise LifecycleUnreadable(f"ADR corpus unusable, leg (b) uncomputable: {exc}") from exc
        m.live_adrs = len({f.path for f in fields})
        for f in fields:
            if f.value in _vas.TERMINAL_STATUSES:
                m.violations.append(Violation(
                    LEG_B, f.path.relative_to(root).as_posix(),
                    f"Status {f.value} is terminal but the ADR sits in {DECISIONS_RELPATH}/ "
                    f"rather than {DECISIONS_ARCHIVE_RELPATH}/"))

    # --- leg c -----------------------------------------------------------------------------
    births = _row_birth_dates(root)
    universe = build_ref_universe(root, set(rows), live + archived)
    cutoff = ARM_DATE.isoformat()
    for rid, (relpath, _status, body) in sorted(rows.items()):
        born = births.get(relpath)
        if born is not None and born < cutoff:
            continue                      # grandfathered, and DATED -- never assumed
        m.post_cutoff_rows += 1
        clause = refs_clause(body)
        if clause is None:
            m.violations.append(Violation(
                LEG_C, f"[#{rid}] {relpath}",
                f"landed {born or 'undated'} (on/after {cutoff}) with no `* refs ...` "
                f"provenance clause"))
            continue
        if not universe.resolving(clause):
            m.violations.append(Violation(
                LEG_C, f"[#{rid}] {relpath}",
                f"landed {born or 'undated'} (on/after {cutoff}) and no token in its "
                f"provenance clause resolves: {clause[:120]!r}"))

    # --- leg d -----------------------------------------------------------------------------
    m.threshold_days, m.threshold_locator = ready_threshold(root)
    ready = [d for d in live if d.status == READY_STATUS]
    m.ready_intakes = len(ready)
    if m.threshold_days is not None:
        for doc in ready:
            dm = _DATED_NAME_RE.match(doc.path.name)
            if not dm:
                continue
            try:
                born = _dt.date.fromisoformat(dm.group("date"))
            except ValueError:
                continue
            age = (today - born).days
            if age > m.threshold_days and not doc.fields.get("review-date", "").strip():
                m.violations.append(Violation(
                    LEG_D, doc.relpath,
                    f"READY for {age} days (document age), past the ruled {m.threshold_days}-day "
                    f"threshold at {m.threshold_locator}, and carries no review-date:"))
    return m


# --- verdict ---------------------------------------------------------------------------------

def findings(m: Measurement) -> list[tuple[str, str]]:
    """`[(status, evidence), ...]`. ONE finding per violation, never a bundle.

    The `#147` register suppresses an ENTIRE Finding on a substring match, so a bundled Finding
    would let one archived intake wave through every other violation beside it -- the reason
    `funnel_coverage` and `consumer_at_landing` both emit one per subject.
    """
    out: list[tuple[str, str]] = []
    for v in m.violations:
        status = "warn" if v.leg == LEG_D else "fail"
        out.append((status, f"{v.leg}: {v.subject} -- {v.detail}"))
    if m.threshold_days is None:
        out.append((
            "warn",
            f"{LEG_D}: NOT ARMED -- no ruled READY threshold found under protocols/ "
            f"(FM-1's constant, expected as `READY threshold: <N> days`). "
            f"{m.ready_intakes} READY intake(s) went unexamined. Reported, not skipped: "
            f"a threshold nobody ruled is not one this gate may invent."))
    if not out:
        out.append((
            "pass",
            f"{m.live_intakes} live + {m.archived_intakes} archived intake(s), {m.live_adrs} "
            f"live ADR(s), {m.rows} row(s): no terminal object left in a live home, every "
            f"ACCEPTED doc still owns an open row, and all {m.post_cutoff_rows} row(s) landed "
            f"on/after {ARM_DATE.isoformat()} carry resolving provenance"))
    return out


def render_report(m: Measurement) -> str:
    lines = [
        "```",
        f"detector           {m.detector}",
        f"intakes            {m.live_intakes} live / {m.archived_intakes} archived",
        f"live ADRs          {m.live_adrs}",
        f"rows               {m.rows} ({m.post_cutoff_rows} on/after {ARM_DATE.isoformat()})",
        f"READY threshold    {m.threshold_days if m.threshold_days is not None else 'NOT RULED'}"
        + (f"  ({m.threshold_locator})" if m.threshold_locator else ""),
        "",
    ]
    for leg, label in ((LEG_A1, "a1 terminal intake not archived"),
                       (LEG_A2, "a2 ACCEPTED, all named rows terminal"),
                       (LEG_B, "b  terminal ADR not archived"),
                       (LEG_C, "c  post-cutoff row provenance"),
                       (LEG_D, "d  READY past threshold")):
        vs = m.by_leg(leg)
        lines.append(f"{label:<38} {len(vs)}")
        for v in vs:
            lines.append(f"    {v.subject} -- {v.detail}")
    lines.append("```")
    return "\n".join(lines)


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FM-2 funnel-lifecycle detector (read-only).")
    ap.add_argument("--repo", default=str(_REPO_ROOT), help="repo root (default: this hub)")
    ap.add_argument("--report", action="store_true", help="print the full measurement")
    args = ap.parse_args(argv)
    try:
        m = measure(Path(args.repo))
    except LifecycleUnreadable as exc:
        print(f"{CHECK_NAME}: ground truth uncomputable (Z-G4): {exc}", file=sys.stderr)
        return 2
    if args.report:
        print(render_report(m))
    else:
        for status, evidence in findings(m):
            print(f"{status.upper():<5} {evidence}")
    return 1 if any(s == "fail" for s, _ in findings(m)) else 0


if __name__ == "__main__":
    raise SystemExit(_main())
