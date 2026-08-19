#!/usr/bin/env python
"""gen_dashboard.py -- [#171] stage 1: the operator conformance dashboard (ADR-86 / ADR-80).

WHAT THIS ANSWERS. The operator's four standing questions, in their own words: *which tasks are
finished*, *where is our telemetry*, *did the intakes pass the gate*, *are the implemented ADRs
archived*. Stage 1 is ONE regenerable document that answers all four at a glance, plus a release-
notes header saying what the last seven days actually bought.

LOCATION + ZONE CLASS are ruled, not chosen here: ADR-86 puts the dashboard at
`ecosystem/conformance.md` as an ADR-80 **committed-generated** zone -- a read-only validator
generates it and commits its own output. A self-contained HTML sibling
(`ecosystem/conformance.html`) is emitted alongside it by operator addendum (2026-08-19), for the
same reason ADR-86 rejected generate-on-demand: the artifact must be openable without running
anything.

LAYER-2 POSTURE (ADR-28/36). Read-only over the repo; the ONLY files written are the two output
paths above, and only under `--write`. It drives no state in any other repo, imports no gate, and
arms no hook.

IT REPORTS, IT NEVER REPAIRS. A VIOLATION in section 2, an archivable ADR in section 3, an
off-enum status anywhere -- each is rendered and left exactly where it is. Repair is somebody
else's commit.

LIBRARY-FIRST -- the reading code paths are the repo's existing parsers, not new regex:
  * `gen_task_tree.parse_backlog` / `derive_*` / `frontmatter_status` -- the BACKLOG line model
    and the `tasks/` tree. Nothing here re-parses a task row by hand.
  * `gen_intake_index._parse_frontmatter` -- intake frontmatter (the `yaml.safe_load` path whose
    hand-rolled predecessor silently dropped every underscore-bearing key).
  * `gen_claude_rosters.collect_recent_adrs` -- ADR headers, both `Status:` dialects, with the
    same `(unparsed)` honesty rather than silent omission.
Loaded BY PATH (`_load`), the way the repo's tests load these loose top-level modules: `scripts/`
is not a package, and an `import` would depend on `sys.path` accidents.

DETERMINISM, AND WHY THE CLOCK IS NOT AN INPUT. Output is a function of the TREE, never of wall
time: the "as of" instant is HEAD's commit date, so two runs on one tree are byte-identical and
`--check` is meaningful. The consequence, stated rather than hidden: after HEAD moves, `--check`
reports drift -- that is a "regenerate me" signal, and it gates nothing (no hook is armed).

TELEMETRY IS READ AS A FILE, NEVER AS AN IMPORT. `[#529]`'s emit store is lane L2's to build;
this module records only whether the store exists at its expected path and says so. It does not
import `telemetry_emit`, `single_flight`, or `audit`, and a test pins that.

CLI: `--write` (emit both files) | `--check` (regen-and-diff; 1 on drift) | `--print` (stdout).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import importlib.util
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent


# --------------------------------------------------------------------------- configuration
# Paths, thresholds and vocabularies are constants, never literals buried in a renderer.

#: The ADR-86 ruled home. Repo-relative so the module works against a fixture tree.
MD_RELPATH = "ecosystem/conformance.md"
#: The self-contained HTML sibling (operator addendum, 2026-08-19).
HTML_RELPATH = "ecosystem/conformance.html"

BACKLOG_RELPATH = "BACKLOG.md"
TASKS_RELDIR = "tasks"
INTAKE_RELDIR = "docs/intake"
INTAKE_ARCHIVE_RELDIR = "docs/intake/archive"
DECISIONS_RELDIR = "docs/decisions"
AUDITS_RELDIR = "docs/audits"

#: Release-notes / trend window. The operator asked for "the last 7 days".
WINDOW_DAYS = 7

#: `[#529]`'s expected emit store. Mirrors `telemetry_emit.DEFAULT_DB_RELPATH` by VALUE, on
#: purpose: importing that module to read one constant would pull lane L2's code into this
#: process, which the lane contract forbids. If L2 moves the store, this constant is the
#: single site to follow it.
TELEMETRY_STORE_RELPATH = "logs/TELEMETRY.db"
TELEMETRY_PENDING_NOTE = "EMIT wiring in flight (lane L2) — no data yet"

#: `tasks/` frontmatter statuses that mean the row has left the queue (gen_task_tree §6.3).
TERMINAL_TASK_STATUSES = ("closed", "retired", "superseded")

#: docs/intake/README.md §5 lifecycle. A status outside it lands in the loud bucket.
INTAKE_STATUS_ORDER = ("SEED", "DRAFT", "READY", "ACCEPTED", "CONSUMED", "SUPERSEDED", "REJECTED")
INTAKE_TERMINAL_STATUSES = ("CONSUMED", "SUPERSEDED", "REJECTED")
STATUS_UNKNOWN = "UNKNOWN"

#: The anti-orphan verdicts an ACCEPTED intake can carry.
VERDICT_CARRIED = "carried"
VERDICT_DEFERRED = "deferred(dated)"
VERDICT_VIOLATION = "VIOLATION (no carrier)"

#: docs/decisions/README.md "Status enum", declared 2026-08-12 (STANDING_RULINGS M-6).
ADR_STATUS_ENUM = (
    "Proposed", "Accepted", "Explored, not adopted",
    "Partially superseded", "Superseded", "Deprecated",
)
#: The two terminal values whose files are eligible for `docs/decisions/archive/` (H3's bar).
ADR_TERMINAL_STATUSES = ("Superseded", "Deprecated")
ADR_ARCHIVE_DIRNAME = "archive"

FLAG_ARCHIVABLE = "ARCHIVABLE"
FLAG_OFF_ENUM = "OFF-ENUM"
FLAG_UNPARSED = "UNPARSED"
#: A file whose NAME is off the `ADR-<n>-<slug>.md` grammar the shared filename regex requires.
FLAG_OFF_GRAMMAR = "OFF-GRAMMAR-FILENAME"

#: The shared parser's own "field absent" sentinel; matched, never re-spelled.
UNPARSED = "(unparsed)"

#: Which header dialect a ledger row was actually read with.
DIALECT_SHARED = "shared"
DIALECT_LEGACY = "legacy"
DIALECT_OFF_GRAMMAR = "off-grammar"

SECTION_TITLES = (
    "Section 0 — Release notes",
    "Section 1 — Backlog at a glance",
    "Section 2 — Intake lifecycle gate",
    "Section 3 — ADR ledger",
    "Section 4 — Telemetry",
    "Section 5 — Gate health",
)

_GENERATED_NOTE = (
    "<!-- generated by scripts/gen_dashboard.py; do not edit by hand. "
    "Regenerate: python scripts/gen_dashboard.py --write -->"
)


# --------------------------------------------------------------------------- borrowed parsers

def _load(name: str):
    """Load a loose top-level `scripts/` module by path (the repo's standard for this shape)."""
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(name, module)
    spec.loader.exec_module(module)
    return module


_gtt = _load("gen_task_tree")
_gii = _load("gen_intake_index")
_gcr = _load("gen_claude_rosters")


# --------------------------------------------------------------------------- row model

@dataclass(frozen=True)
class ClosedRow:
    id: int
    title: str
    gain: str  # the row's own `Done when:` clause -- what the operator gained
    theme: str | None
    closed_on: str = ""  # YYYY-MM-DD of the commit that removed the row, "" if unknown
    sha: str = ""


@dataclass(frozen=True)
class ThemeStats:
    theme: str
    open: int
    deferred: int
    closed: int
    sizes: dict[str, int]


@dataclass(frozen=True)
class IntakeRow:
    intake_id: str
    filename: str
    title: str
    status: str
    verdict: str  # "" for any non-ACCEPTED doc -- the anti-orphan check is ACCEPTED-only
    detail: str
    archived: bool


@dataclass(frozen=True)
class AdrRow:
    number: int
    status: str
    date: str
    title: str
    archived: bool
    flag: str
    dialect: str = DIALECT_SHARED
    filename: str = ""


@dataclass(frozen=True)
class TelemetryState:
    exists: bool
    relpath: str
    size_bytes: int = 0


@dataclass(frozen=True)
class GateHealth:
    source: str = ""
    columns: tuple[str, ...] = ()
    rows: tuple[tuple[str, tuple[int, ...]], ...] = ()
    current_index: int = -1
    current_total: int = 0
    commit_tax: str = ""
    commit_tax_date: str = ""
    commit_tax_source: str = ""


@dataclass(frozen=True)
class Dashboard:
    head_sha: str
    as_of: str
    since: str
    themes: list[ThemeStats] = field(default_factory=list)
    total_open: int = 0
    total_open_prior: int | None = None
    closed_in_window: list[ClosedRow] = field(default_factory=list)
    intake: list[IntakeRow] = field(default_factory=list)
    adrs: list[AdrRow] = field(default_factory=list)
    telemetry: TelemetryState = TelemetryState(False, TELEMETRY_STORE_RELPATH)
    gate: GateHealth = GateHealth()


# --------------------------------------------------------------------------- git access

class GitReader:
    """The only place a subprocess is spawned. Injectable so every renderer stays pure."""

    def __init__(self, repo_root: Path):
        self._root = repo_root

    def _run(self, *args: str) -> str | None:
        # GIT_DIR/GIT_WORK_TREE in the ambient environment override `-C`, so the local
        # env vars are scrubbed rather than blanket-stripped (git names them itself).
        env = dict(os.environ)
        probe = subprocess.run(["git", "rev-parse", "--local-env-vars"],
                               capture_output=True, text=True)
        if probe.returncode == 0:
            for var in probe.stdout.split():
                env.pop(var, None)
        proc = subprocess.run(["git", "-C", str(self._root), *args],
                              capture_output=True, text=True, env=env, errors="replace")
        return proc.stdout if proc.returncode == 0 else None

    def head_sha(self) -> str:
        out = self._run("rev-parse", "HEAD")
        return out.strip()[:12] if out else ""

    def head_date(self) -> str:
        out = self._run("log", "-1", "--format=%ad", "--date=short")
        return out.strip() if out else ""

    def rev_before(self, iso_date: str) -> str | None:
        out = self._run("rev-list", "-1", "--first-parent", f"--before={iso_date}", "HEAD")
        return out.strip() or None if out else None

    def file_at(self, rev: str, relpath: str) -> str | None:
        return self._run("show", f"{rev}:{relpath}")

    def log_pairs(self, relpath: str, since_rev: str) -> list[tuple[str, str, str]]:
        """[(sha, YYYY-MM-DD, first-parent sha), ...] newest-first for commits touching relpath."""
        out = self._run("log", "--first-parent", "--format=%H|%ad|%P", "--date=short",
                        f"{since_rev}..HEAD", "--", relpath)
        if not out:
            return []
        pairs: list[tuple[str, str, str]] = []
        for line in out.splitlines():
            parts = line.split("|")
            if len(parts) != 3 or not parts[0]:
                continue
            parents = parts[2].split()
            if not parents:
                continue
            pairs.append((parts[0], parts[1], parents[0]))
        return pairs


def _reader(repo_root: Path) -> GitReader:
    return GitReader(repo_root)


# --------------------------------------------------------------------------- section 0

_DONE_WHEN_RE = re.compile(r"·\s*Done when:\s*(.+?)(?=\s+·\s|$)")


def parse_done_when(raw: str) -> str:
    """A task row's own `Done when:` clause -- the operator-facing statement of the gain."""
    m = _DONE_WHEN_RE.search(raw)
    return m.group(1).strip() if m else ""


def _rows_by_id(backlog_text: str) -> dict[int, "object"]:
    model = _gtt.parse_backlog(backlog_text.replace("\r\n", "\n"))
    return {payload.id: payload for kind, payload in model.nodes if kind == "task"}


def _closed_row(task) -> ClosedRow:
    return ClosedRow(id=task.id, title=_gtt.derive_title(task.raw),
                     gain=parse_done_when(task.raw), theme=task.theme)


def closed_rows_between(old_text: str, new_text: str) -> list[ClosedRow]:
    """Task rows present in `old_text` and absent from `new_text` -- "done items leave" (ADR-65)."""
    old = _rows_by_id(old_text)
    new = _rows_by_id(new_text)
    return [_closed_row(old[i]) for i in sorted(set(old) - set(new))]


def closed_rows_from_history(git, relpath: str, since_rev: str) -> list[ClosedRow]:
    """Per-commit closures across the window, so each row carries its real closing DATE.

    The two-snapshot diff cannot date a closure (ids are monotonic by FILING, not by closing),
    and the release notes are ordered newest-first, so the date has to come from the commit that
    removed the line.
    """
    rows: list[ClosedRow] = []
    seen: set[int] = set()
    for sha, when, parent in git.log_pairs(relpath, since_rev):
        before = git.file_at(parent, relpath)
        after = git.file_at(sha, relpath)
        if before is None or after is None:
            continue
        try:
            gone = closed_rows_between(before, after)
        except (ValueError, AssertionError):
            continue  # a malformed historical BACKLOG is skipped, never fatal
        for row in gone:
            if row.id in seen:
                continue
            seen.add(row.id)
            rows.append(ClosedRow(id=row.id, title=row.title, gain=row.gain, theme=row.theme,
                                  closed_on=when, sha=sha[:12]))
    return rows


def _release_order(rows: list[ClosedRow]) -> list[ClosedRow]:
    return sorted(rows, key=lambda r: (r.closed_on, r.id), reverse=True)


def render_release_notes(rows: list[ClosedRow], window_days: int, since: str, until: str) -> str:
    out = [f"## {SECTION_TITLES[0]} (last {window_days} days)", "",
           f"_Rows that left `BACKLOG.md` between {since} and {until}, newest first. "
           "The gain line is the row's own `Done when:` clause — what the operator can now do "
           "that they could not before._", ""]
    if not rows:
        out += [f"**No rows closed in the last {window_days} days.**", ""]
        return "\n".join(out)
    for row in _release_order(rows):
        gain = row.gain or "_(row carried no `Done when:` clause — see the closing commit)_"
        when = f" · closed {row.closed_on}" if row.closed_on else ""
        sha = f" · `{row.sha}`" if row.sha else ""
        out.append(f"- **{row.title}** [#{row.id}] → {gain}{when}{sha}")
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------- section 1

def theme_stats(backlog_text: str, tasks_dir: Path) -> list[ThemeStats]:
    """Per-theme open / deferred / closed counts and size mix.

    Live rows come from BACKLOG.md via the line model; closed rows come from the `tasks/` tree,
    which is the only surface that still remembers a retired row's theme.
    """
    live: dict[str, dict] = {}
    order: list[str] = []
    for kind, payload in _gtt.parse_backlog(backlog_text.replace("\r\n", "\n")).nodes:
        if kind != "task":
            continue
        theme = payload.theme or "(no theme)"
        if theme not in live:
            live[theme] = {"open": 0, "deferred": 0, "sizes": {}}
            order.append(theme)
        bucket = live[theme]
        bucket["deferred" if _gtt.derive_status(payload.raw) == "deferred" else "open"] += 1
        size = _gtt.derive_size(payload.raw)
        if size:
            bucket["sizes"][size] = bucket["sizes"].get(size, 0) + 1

    closed: dict[str, int] = {}
    for path in sorted(tasks_dir.glob("*.md")) if tasks_dir.is_dir() else []:
        text = path.read_text(encoding="utf-8", errors="replace")
        if _gtt.frontmatter_status(text) not in TERMINAL_TASK_STATUSES:
            continue
        m = re.search(r"^theme:\s*\"?(.+?)\"?\s*$", text, re.MULTILINE)
        theme = m.group(1) if m else "(no theme)"
        closed[theme] = closed.get(theme, 0) + 1
        if theme not in live:
            live[theme] = {"open": 0, "deferred": 0, "sizes": {}}
            order.append(theme)

    return [ThemeStats(theme=t, open=live[t]["open"], deferred=live[t]["deferred"],
                       closed=closed.get(t, 0), sizes=dict(sorted(live[t]["sizes"].items())))
            for t in sorted(order)]


def _cell(value) -> str:
    r"""One markdown TABLE cell, pipe-escaped.

    A raw `|` inside a value silently splits the row into extra columns, and derived content is
    exactly where an unescaped pipe arrives from: ADR-41's live status line reads
    `open | in-progress | blocked | done`, which shredded this table before it was escaped.
    Newlines collapse for the same reason.
    """
    return str(value).replace("|", r"\|").replace("\n", " ")


def _size_mix(sizes: dict[str, int]) -> str:
    return " · ".join(f"{k} {v}" for k, v in sizes.items()) or "—"


def render_backlog(themes: list[ThemeStats], total_open: int, total_open_prior: int | None,
                   window_days: int, closed_in_window: list[ClosedRow]) -> str:
    out = [f"## {SECTION_TITLES[1]}", "",
           "| Theme | Open | Deferred | Closed | Size mix (live rows) |",
           "|---|---:|---:|---:|---|"]
    for t in themes:
        out.append(f"| {_cell(t.theme)} | {t.open} | {t.deferred} | {t.closed} | "
                   f"{_cell(_size_mix(t.sizes))} |")
    out.append("")
    if total_open_prior is None:
        out.append(f"**Total live rows: {total_open}.** {window_days}-day trend **unavailable** — "
                   "no committed BACKLOG.md at the window start to compare against.")
    else:
        delta = total_open - total_open_prior
        arrow = "+" if delta > 0 else ""
        out.append(f"**Total live rows: {total_open}** ({arrow}{delta} over {window_days} days; "
                   f"{total_open_prior} at the window start).")
    out.append("")
    if closed_in_window:
        ids = " · ".join(f"[#{r.id}]" for r in _release_order(closed_in_window))
        out += [f"Closed this window ({len(closed_in_window)}): {ids}", ""]
    else:
        out += ["Closed this window: none.", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- section 2

def carrier_ids_for(intake_id: str, backlog_text: str) -> list[int]:
    """Live BACKLOG rows that cite this intake, in either landed dialect.

    Both `intake #12` and `intake-id 12` appear in the tree; the trailing boundary is anchored
    so `intake #7` never matches a row that cites `intake #70`.
    """
    if not intake_id:
        return []
    pattern = re.compile(rf"intake(?:-id\s+|\s+#)\s*{re.escape(intake_id)}(?!\d)", re.IGNORECASE)
    hits: list[int] = []
    for kind, payload in _gtt.parse_backlog(backlog_text.replace("\r\n", "\n")).nodes:
        if kind == "task" and pattern.search(payload.raw):
            hits.append(payload.id)
    return hits


def _intake_verdict(fm: dict, intake_id: str, backlog_text: str) -> tuple[str, str]:
    carriers = carrier_ids_for(intake_id, backlog_text)
    if carriers:
        return VERDICT_CARRIED, " · ".join(f"[#{i}]" for i in carriers)
    disposition = (fm.get("disposition", "") or "").strip().lower()
    trigger = (fm.get("trigger", "") or "").strip()
    review_date = (fm.get("review-date", "") or "").strip()
    if disposition == "deferred" and (trigger or review_date):
        return VERDICT_DEFERRED, trigger or review_date
    return VERDICT_VIOLATION, ""


def _collect_intake_dir(directory: Path, archived: bool, backlog_text: str) -> list[IntakeRow]:
    rows: list[IntakeRow] = []
    if not directory.is_dir():
        return rows
    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = _gii._parse_frontmatter(text)
        status = (fm.get("status", "") or "").strip().upper() or STATUS_UNKNOWN
        intake_id = (fm.get("intake-id", "") or "").strip()
        verdict, detail = ("", "")
        if status == "ACCEPTED":
            verdict, detail = _intake_verdict(fm, intake_id, backlog_text)
        rows.append(IntakeRow(intake_id=intake_id, filename=path.name, title=_gii._title_of(text),
                              status=status, verdict=verdict, detail=detail, archived=archived))
    return rows


def intake_rows(intake_dir: Path, archive_dir: Path, backlog_text: str) -> list[IntakeRow]:
    rows = _collect_intake_dir(intake_dir, False, backlog_text)
    rows += _collect_intake_dir(archive_dir, True, backlog_text)
    return sorted(rows, key=lambda r: (int(r.intake_id) if r.intake_id.isdigit() else 10**9,
                                       r.filename))


def _status_bucket(status: str) -> str:
    return status if status in INTAKE_STATUS_ORDER else STATUS_UNKNOWN


def render_intake(rows: list[IntakeRow]) -> str:
    out = [f"## {SECTION_TITLES[2]}", "",
           "_Anti-orphan check, ACCEPTED docs only: an accepted intake must be carried by a live "
           "BACKLOG row, or be explicitly parked with a trigger / review date. Neither is a "
           "**VIOLATION** — reported here, repaired elsewhere._", ""]
    violations = [r for r in rows if r.verdict == VERDICT_VIOLATION]
    if violations:
        out += [f"> **{len(violations)} VIOLATION(s)**: "
                + " · ".join(f"#{r.intake_id or '?'} `{r.filename}`" for r in violations), ""]
    else:
        out += ["> No anti-orphan violations.", ""]
    out += ["| Intake | Status | Doc | Anti-orphan | Detail | Archived |",
            "|---|---|---|---|---|---|"]
    order = {s: i for i, s in enumerate(INTAKE_STATUS_ORDER)}
    for r in sorted(rows, key=lambda r: (order.get(_status_bucket(r.status), 99),
                                         int(r.intake_id) if r.intake_id.isdigit() else 10**9)):
        label = f"#{r.intake_id}" if r.intake_id else "MISSING-ID"
        status = r.status if r.status in INTAKE_STATUS_ORDER else f"{r.status} → {STATUS_UNKNOWN}"
        archived = "yes" if r.archived else ("**no**" if r.status in INTAKE_TERMINAL_STATUSES
                                             else "—")
        out.append(f"| {_cell(label)} | {_cell(status)} | `{_cell(r.filename)}` | "
                   f"{_cell(r.verdict) or '—'} | {_cell(r.detail) or '—'} | {archived} |")
    out += ["", "_Terminal docs (CONSUMED / SUPERSEDED / REJECTED) belong in "
            "`docs/intake/archive/` per docs/intake/README.md §5; a bold **no** is one that has "
            "not been relocated._", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- section 3

_STRIKETHROUGH_RE = re.compile(r"~~[^~]*~~")
_ENUM_BY_LENGTH = tuple(sorted(ADR_STATUS_ENUM, key=len, reverse=True))

#: The filename grammar the shared parser requires. Mirrored (not imported) so a file the
#: shared regex SKIPS can be enumerated here rather than silently vanishing from the ledger.
_ADR_FILENAME_RE = re.compile(r"^ADR-(\d+)-[\w.-]+\.md$")

#: The third, pre-2026-05 header dialect: `# ADR-NN — Title` + a BARE `Status:` / `Date:` line.
_LEGACY_STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$", re.MULTILINE)
_LEGACY_DATE_RE = re.compile(r"^Date:\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)
_LEGACY_TITLE_RE = re.compile(r"^#\s+ADR-\d+\s*[—:\-]\s*(.+?)\s*$", re.MULTILINE)


def normalize_adr_status(status: str) -> str:
    """The enum value a raw `Status:` line resolves to, or "" when it resolves to none.

    Live status lines are not bare enum members. Two landed forms have to survive:
      * a named successor  -- `Superseded by ADR-53`
      * the strikethrough  -- `~~Accepted~~ Superseded by ADR-53` (ADR-52's actual text), where
        the struck-out half is the OLD value and reading it would invert the answer.
    Struck-out text is dropped first, then the longest enum member that PREFIXES what remains
    wins -- longest-first is what keeps `Partially superseded` from being read as `Superseded`.
    """
    text = _STRIKETHROUGH_RE.sub(" ", status).strip()
    if not text:
        text = status.replace("~", "").strip()
    lowered = text.lower()
    for value in _ENUM_BY_LENGTH:
        if lowered.startswith(value.lower()):
            return value
    for value in _ENUM_BY_LENGTH:
        if re.search(rf"\b{re.escape(value.lower())}\b", lowered):
            return value
    return ""


def _adr_flag(status: str, archived: bool) -> str:
    if status == UNPARSED:
        return FLAG_UNPARSED
    normalized = normalize_adr_status(status)
    if not normalized:
        return FLAG_OFF_ENUM
    if normalized in ADR_TERMINAL_STATUSES and not archived:
        return FLAG_ARCHIVABLE
    return ""


def _legacy_header(text: str) -> tuple[str, str, str]:
    """The pre-2026-05 ADR header dialect: `# ADR-NN — Title` with a BARE `Status:` line.

    A third dialect exists in this corpus and the shared parser does not cover it. That is not
    a defect in `gen_claude_rosters` -- it reads the LAST FIVE ADRs, which are all modern, so
    the dialect has never been in its field of view. Reading a whole ledger puts it there. This
    fallback fires ONLY on a row the shared parser already returned `(unparsed)` for, so the
    shared parser stays primary and its behaviour is not altered; the dialect a row was read
    with is carried on the row and reported.
    """
    status_m = _LEGACY_STATUS_RE.search(text)
    title_m = _LEGACY_TITLE_RE.search(text)
    date_m = _LEGACY_DATE_RE.search(text)
    status = status_m.group(1).strip() if status_m else UNPARSED
    if status != UNPARSED:
        # Same qualifier trim the shared parser applies to the bold dialect, so both dialects
        # land on comparable values: `Accepted (amended four times: ...)` -> `Accepted`.
        status = re.split(r"\s*[(—]", status, maxsplit=1)[0].strip() or UNPARSED
    return (status,
            date_m.group(1) if date_m else UNPARSED,
            title_m.group(1).strip() if title_m else UNPARSED)


def _adr_dir_rows(directory: Path, archived: bool) -> list[AdrRow]:
    if not directory.is_dir():
        return []
    files = sorted(directory.glob("ADR-*.md"))
    if not files:
        return []
    by_number: dict[int, Path] = {}
    off_grammar: list[Path] = []
    for path in files:
        m = _ADR_FILENAME_RE.match(path.name)
        if m:
            by_number[int(m.group(1))] = path
        else:
            off_grammar.append(path)

    rows: list[AdrRow] = []
    # collect_recent_adrs is the repo's ADR header parser (both bold `Status:` dialects, and
    # the `(unparsed)` honesty). Asking it for `len(files)` ADRs asks it for all of them.
    for number, status, date, title in _gcr.collect_recent_adrs(directory, count=len(files)):
        dialect = DIALECT_SHARED
        if UNPARSED in (status, title, date) and number in by_number:
            text = by_number[number].read_text(encoding="utf-8", errors="replace")
            alt_status, alt_date, alt_title = _legacy_header(text)
            if alt_status != UNPARSED or alt_title != UNPARSED:
                dialect = DIALECT_LEGACY
                status = alt_status if status == UNPARSED else status
                date = alt_date if date == UNPARSED else date
                title = alt_title if title == UNPARSED else title
        rows.append(AdrRow(number=number, status=status, date=date, title=title,
                           archived=archived, flag=_adr_flag(status, archived), dialect=dialect))

    # A file whose NAME is off the `ADR-<n>-<slug>.md` grammar is invisible to the shared
    # parser's filename regex -- it is not "(unparsed)", it is absent. Reported as its own row
    # so a whole decision cannot go missing from a ledger that claims to be complete.
    for path in off_grammar:
        m = re.match(r"^ADR-(\d+)", path.name)
        text = path.read_text(encoding="utf-8", errors="replace")
        alt_status, alt_date, alt_title = _legacy_header(text)
        rows.append(AdrRow(number=int(m.group(1)) if m else -1, status=alt_status, date=alt_date,
                           title=alt_title, archived=archived, flag=FLAG_OFF_GRAMMAR,
                           dialect=DIALECT_OFF_GRAMMAR, filename=path.name))
    return rows


def adr_rows(decisions_dir: Path) -> list[AdrRow]:
    rows = _adr_dir_rows(decisions_dir, False)
    rows += _adr_dir_rows(decisions_dir / ADR_ARCHIVE_DIRNAME, True)
    return sorted(rows, key=lambda r: (r.number, r.filename))


def _status_mix(rows: list[AdrRow]) -> dict[str, int]:
    """Counts by NORMALIZED status, so `Superseded by ADR-53` lands in the `Superseded` bucket."""
    counts: dict[str, int] = {}
    for r in rows:
        key = normalize_adr_status(r.status) or r.status
        counts[key] = counts.get(key, 0) + 1
    return counts


def render_adrs(rows: list[AdrRow]) -> str:
    out = [f"## {SECTION_TITLES[3]}", ""]
    counts = _status_mix(rows)
    out += ["_Status per ADR, plus the archival candidates. In this repo **Accepted is not an "
            "archive trigger** — `docs/decisions/README.md` keys the bar on `Superseded` / "
            "`Deprecated` only, so an implemented-and-still-binding ADR correctly stays put. "
            "The flag below is a report; no file is moved._", "",
            "**Status mix:** " + " · ".join(f"{k} {v}" for k, v in sorted(counts.items())), "",
            _dialect_note(rows), ""]
    flagged = [r for r in rows if r.flag]
    if flagged:
        out += ["| ADR | Status | Date | Flag | Title |", "|---|---|---|---|---|"]
        for r in flagged:
            out.append(f"| ADR-{r.number} | {_cell(r.status)} | {_cell(r.date)} | "
                       f"**{r.flag}** | {_cell(r.title)} |")
        out.append("")
    else:
        out += ["No archival candidates and no off-enum or unparsed status.", ""]
    out += ["<details><summary>Full ledger (" + str(len(rows)) + " ADRs)</summary>", "",
            "| ADR | Status | Date | Home | Read as | Title |", "|---|---|---|---|---|---|"]
    for r in rows:
        home = "archive/" if r.archived else "decisions/"
        out.append(f"| ADR-{r.number} | {_cell(r.status)} | {_cell(r.date)} | {home} | "
                   f"{r.dialect} | {_cell(r.title)} |")
    out += ["", "</details>", ""]
    return "\n".join(out)


def _dialect_counts(rows: list[AdrRow]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r.dialect] = counts.get(r.dialect, 0) + 1
    return counts


def _dialect_note(rows: list[AdrRow]) -> str:
    """How each row was READ. A ledger that hides its own coverage gap is worse than none."""
    counts = _dialect_counts(rows)
    legacy = counts.get(DIALECT_LEGACY, 0)
    off = counts.get(DIALECT_OFF_GRAMMAR, 0)
    if not legacy and not off:
        return ("**Header coverage:** every row read with the shared parser "
                "(`gen_claude_rosters.collect_recent_adrs`).")
    parts = [f"**Header coverage:** {counts.get(DIALECT_SHARED, 0)} rows read with the shared "
             "parser (`gen_claude_rosters.collect_recent_adrs`)"]
    if legacy:
        parts.append(f"{legacy} needed the pre-2026-05 dialect fallback for at least one header "
                     "field (bare `Status:` / `Date:` + `# ADR-NN — Title`), which the shared "
                     "parser does not cover — it reads only the last five ADRs, so the dialect "
                     "has never been in its field of view")
    if off:
        names = " · ".join(f"`{r.filename}`" for r in rows if r.dialect == DIALECT_OFF_GRAMMAR)
        parts.append(f"{off} sit outside its filename grammar entirely and are INVISIBLE to it "
                     f"({names}) — not `(unparsed)`, absent")
    return "; ".join(parts) + ". Reported, not repaired."


# --------------------------------------------------------------------------- section 4

def telemetry_state(repo_root: Path) -> TelemetryState:
    """Whether `[#529]`'s emit store exists. A stat call — never an import, never a query."""
    path = repo_root / TELEMETRY_STORE_RELPATH
    if path.is_file():
        return TelemetryState(True, TELEMETRY_STORE_RELPATH, path.stat().st_size)
    return TelemetryState(False, TELEMETRY_STORE_RELPATH)


def render_telemetry(state: TelemetryState) -> str:
    out = [f"## {SECTION_TITLES[4]}", ""]
    if not state.exists:
        out += [f"**{TELEMETRY_PENDING_NOTE}.**", "",
                f"Expected store path: `{state.relpath}` — absent on this tree.", "",
                "_This dashboard reads the store as a FILE and never imports or calls the emit "
                "code: `scripts/telemetry_emit.py` and `scripts/single_flight.py` belong to lane "
                "L2 ([#529]/[#530]), and a read-only surface must not become a caller of the "
                "thing it reports on._", ""]
    else:
        out += [f"Emit store present at `{state.relpath}` ({state.size_bytes} bytes).", "",
                "_Presence only. Reading the store's CONTENT is stage 2 — it needs the schema "
                "lane L2 owns, and this generator deliberately does not import it._", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- section 5

_AUDIT_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
_AUDIT_HEADER_DATE_RE = re.compile(r"\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})")
_FENCE_RE = re.compile(r"^```")
_BLOCK_HEADER_RE = re.compile(r"^(?:class|check)\s{2,}(.+?)\s*$")
_BLOCK_ROW_RE = re.compile(r"^([a-z][a-z0-9_]*)((?:\s+[-+]?\d+)+)\s*(.*)$")
_COMMIT_TAX_RE = re.compile(r"\*\*median:\s*([\d.]+)\s*s\*\*")
_COMMIT_TAX_TOPIC_RE = re.compile(r"commit[- ]tax", re.IGNORECASE)


def _audit_files_newest_first(audits_dir: Path) -> list[Path]:
    if not audits_dir.is_dir():
        return []
    files = [p for p in audits_dir.glob("*.md") if p.name != "README.md"]
    return sorted(files, key=lambda p: ((_AUDIT_DATE_RE.match(p.name) or [None, ""])[1], p.name),
                  reverse=True)


def _fenced_blocks(text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if _FENCE_RE.match(line):
            if current is None:
                current = []
            else:
                blocks.append(current)
                current = None
            continue
        if current is not None:
            current.append(line)
    return blocks


def _parse_warn_block(block: list[str]) -> tuple[tuple[str, ...], list[tuple[str, tuple[int, ...]]]]:
    columns: tuple[str, ...] = ()
    rows: list[tuple[str, tuple[int, ...]]] = []
    for line in block:
        header = _BLOCK_HEADER_RE.match(line)
        if header and not rows:
            columns = tuple(c.strip() for c in re.split(r"\s{2,}", header.group(1)) if c.strip())
            continue
        if not columns:
            continue
        m = _BLOCK_ROW_RE.match(line)
        if m:
            rows.append((m.group(1), tuple(int(v) for v in m.group(2).split())))
    if rows:
        width = min(len(v) for _, v in rows)
        rows = [(name, values[:width]) for name, values in rows]
        columns = columns[:width]
    return columns, rows


def _current_column(columns: tuple[str, ...]) -> int:
    for idx, label in enumerate(columns):
        if "after" in label.lower() or "post" in label.lower():
            return idx
    for idx in range(len(columns) - 1, -1, -1):
        if "delta" not in columns[idx].lower():
            return idx
    return len(columns) - 1 if columns else -1


def _commit_tax(files: list[Path], audits_dir: Path) -> tuple[str, str, str]:
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        if not _COMMIT_TAX_TOPIC_RE.search(text):
            continue
        m = _COMMIT_TAX_RE.search(text)
        if not m:
            continue
        header = _AUDIT_HEADER_DATE_RE.search(text)
        name_date = _AUDIT_DATE_RE.match(path.name)
        date = header.group(1) if header else (name_date.group(1) if name_date else "")
        return f"{m.group(1)} s", date, str(path.relative_to(audits_dir.parent.parent))
    return "", "", ""


def gate_health(audits_dir: Path) -> GateHealth:
    """The newest audit that records a ship-gate WARN composition, plus the commit-tax reading.

    Parsed off the evidence spine rather than measured here: running the gate would make this a
    2-minute generator AND a caller of `audit.py`, which the lane contract forbids.
    """
    files = _audit_files_newest_first(audits_dir)
    tax, tax_date, tax_source = _commit_tax(files, audits_dir)
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for block in _fenced_blocks(text):
            columns, rows = _parse_warn_block(block)
            if len(rows) < 2:
                continue
            idx = _current_column(columns)
            total = sum(v[idx] for _, v in rows) if 0 <= idx else 0
            return GateHealth(source=str(path.relative_to(audits_dir.parent.parent)).replace("\\", "/"),
                              columns=columns, rows=tuple(rows), current_index=idx,
                              current_total=total, commit_tax=tax, commit_tax_date=tax_date,
                              commit_tax_source=tax_source.replace("\\", "/"))
    return GateHealth(commit_tax=tax, commit_tax_date=tax_date,
                      commit_tax_source=tax_source.replace("\\", "/"))


def render_gate_health(gate: GateHealth) -> str:
    out = [f"## {SECTION_TITLES[5]}", ""]
    if not gate.rows:
        out += ["**Ship-gate WARN composition not found** on the audit surface — no audit under "
                "`docs/audits/` carries a parsable class/count block.", ""]
    else:
        label = gate.columns[gate.current_index] if 0 <= gate.current_index < len(gate.columns) \
            else "current"
        out += [f"Last recorded ship-gate composition — source `{gate.source}`; "
                f"the `{label}` column is the standing count.", "",
                "| WARN class | " + " | ".join(_cell(c) for c in gate.columns) + " |",
                "|---" * (len(gate.columns) + 1) + "|"]
        for name, values in gate.rows:
            out.append(f"| `{_cell(name)}` | " + " | ".join(str(v) for v in values) + " |")
        out += ["", f"**Standing WARN total: {gate.current_total}** across "
                f"{len(gate.rows)} classes.", ""]
    if gate.commit_tax:
        out += [f"**Commit tax: {gate.commit_tax}** (median), measured {gate.commit_tax_date} — "
                f"source `{gate.commit_tax_source}`.", ""]
    else:
        out += ["**Commit tax: not found** on the audit surface.", ""]
    out += ["_Both figures are read off `docs/audits/` rather than measured here: this generator "
            "must not call the gate it reports on._", ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- assembly

def _window_start(as_of: str, window_days: int) -> str:
    day = _dt.date.fromisoformat(as_of) - _dt.timedelta(days=window_days)
    return day.isoformat()


def build(repo_root: Path, git) -> Dashboard:
    """Collect every section. Pure with respect to the clock: `as_of` is HEAD's commit date."""
    backlog_text = (repo_root / BACKLOG_RELPATH).read_text(encoding="utf-8")
    as_of = git.head_date() or ""
    since = _window_start(as_of, WINDOW_DAYS) if as_of else ""

    since_rev = git.rev_before(since) if since else None
    prior_text = git.file_at(since_rev, BACKLOG_RELPATH) if since_rev else None

    closed: list[ClosedRow] = []
    if since_rev:
        closed = closed_rows_from_history(git, BACKLOG_RELPATH, since_rev)
        if not closed and prior_text is not None:
            closed = closed_rows_between(prior_text, backlog_text)

    themes = theme_stats(backlog_text, repo_root / TASKS_RELDIR)
    total_open = sum(t.open + t.deferred for t in themes)
    total_prior = None
    if prior_text is not None:
        try:
            total_prior = len(_rows_by_id(prior_text))
        except (ValueError, AssertionError):
            total_prior = None

    return Dashboard(
        head_sha=git.head_sha(), as_of=as_of, since=since,
        themes=themes, total_open=total_open, total_open_prior=total_prior,
        closed_in_window=closed,
        intake=intake_rows(repo_root / INTAKE_RELDIR, repo_root / INTAKE_ARCHIVE_RELDIR,
                           backlog_text),
        adrs=adr_rows(repo_root / DECISIONS_RELDIR),
        telemetry=telemetry_state(repo_root),
        gate=gate_health(repo_root / AUDITS_RELDIR),
    )


def _preamble(d: Dashboard) -> str:
    return "\n".join([
        "# Conformance dashboard — `.dev-knowledge`",
        "",
        "<!-- scope: meta -->",
        "",
        _GENERATED_NOTE,
        "",
        "> **Generated, committed, read-only** (ADR-86 location + ADR-80 zone class). It answers "
        "four standing operator questions — what finished, where the telemetry is, whether the "
        "intakes passed their gate, and whether implemented ADRs are archived — and it **reports "
        "rather than repairs**: every VIOLATION and flag below is left exactly where it was found.",
        "",
        f"- **As of:** {d.as_of or '(unknown)'} · **HEAD:** `{d.head_sha or '(unknown)'}` · "
        f"**window:** {d.since or '(unknown)'} → {d.as_of or '(unknown)'} ({WINDOW_DAYS} days)",
        "- **Regenerate:** `python scripts/gen_dashboard.py --write` · "
        "**verify:** `python scripts/gen_dashboard.py --check`",
        "- **Determinism:** derived from the tree, not the clock — the \"as of\" instant is "
        "HEAD's commit date, so two runs on one tree are byte-identical. After HEAD moves, "
        "`--check` reports drift; that is a regenerate-me signal and gates nothing.",
        "",
        "---",
        "",
    ])


def render_markdown(d: Dashboard) -> str:
    parts = [
        _preamble(d),
        render_release_notes(d.closed_in_window, WINDOW_DAYS, d.since, d.as_of),
        render_backlog(d.themes, d.total_open, d.total_open_prior, WINDOW_DAYS,
                       d.closed_in_window),
        render_intake(d.intake),
        render_adrs(d.adrs),
        render_telemetry(d.telemetry),
        render_gate_health(d.gate),
    ]
    return "\n".join(parts).rstrip("\n") + "\n"


# --------------------------------------------------------------------------- HTML sibling

_CSS = """
:root{--bg:#fbfbfa;--fg:#1f2328;--muted:#5b6470;--line:#e2e4e8;--card:#ffffff;
--red:#b3261e;--redbg:#fdecea;--amber:#8a6100;--amberbg:#fdf3d8;--green:#1a7f37;--accent:#2f5fd0}
@media (prefers-color-scheme:dark){:root{--bg:#14171a;--fg:#e6e9ee;--muted:#9aa4b2;
--line:#2a2f36;--card:#1b1f24;--red:#ff8a80;--redbg:#3a1c1a;--amber:#f0c14b;--amberbg:#3a3018;
--green:#7ee787;--accent:#8ab4ff}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:1100px;margin:0 auto;padding:2rem 1.25rem 4rem}
h1{font-size:1.7rem;margin:0 0 .35rem}
h2{font-size:1.15rem;margin:2.5rem 0 .5rem;padding-bottom:.35rem;border-bottom:2px solid var(--line)}
p,li{color:var(--fg)}
.meta{color:var(--muted);font-size:.86rem;margin:.2rem 0}
.note{color:var(--muted);font-size:.88rem;margin:.4rem 0 1rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:.85rem 1rem;margin:.75rem 0}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.88rem;min-width:520px}
th,td{text-align:left;padding:.4rem .55rem;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600;white-space:nowrap}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.86em}
.badge{display:inline-block;padding:.06rem .45rem;border-radius:999px;font-size:.78rem;
font-weight:600;white-space:nowrap}
.violation{background:var(--redbg);color:var(--red)}
.flag{background:var(--amberbg);color:var(--amber)}
.ok{color:var(--green);font-weight:600}
.rel{margin:0;padding-left:1.1rem}
.rel li{margin:.3rem 0}
.gain{color:var(--muted)}
""".strip()


def _esc(value) -> str:
    return html.escape(str(value), quote=True)


_MD_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_MD_CODE_RE = re.compile(r"`([^`]+)`")


def _md_to_text(markdown: str) -> str:
    """Render one line of prose shared with the markdown output: escape first, then re-mark.

    Escaping BEFORE the markers are converted is what keeps a `<` in the source text from
    reaching the page as markup.
    """
    escaped = _esc(markdown)
    escaped = _MD_BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    return _MD_CODE_RE.sub(r"<code>\1</code>", escaped)


def html_table(headers, rows, numeric: tuple[int, ...] = ()) -> str:
    head = "".join(f'<th class="num">{_esc(h)}</th>' if i in numeric else f"<th>{_esc(h)}</th>"
                   for i, h in enumerate(headers))
    body = []
    for row in rows:
        cells = "".join(f'<td class="num">{_esc(c)}</td>' if i in numeric else f"<td>{_esc(c)}</td>"
                        for i, c in enumerate(row))
        body.append(f"<tr>{cells}</tr>")
    return ('<div class="scroll"><table><thead><tr>' + head + "</tr></thead><tbody>"
            + "".join(body) + "</tbody></table></div>")


def _html_release(d: Dashboard) -> str:
    out = [f"<h2>{_esc(SECTION_TITLES[0])} (last {WINDOW_DAYS} days)</h2>",
           '<p class="note">Rows that left <code>BACKLOG.md</code> between '
           f"{_esc(d.since)} and {_esc(d.as_of)}, newest first. The gain line is the row's own "
           "<code>Done when:</code> clause.</p>"]
    if not d.closed_in_window:
        return "\n".join(out + ['<p class="card"><strong>No rows closed in the last '
                                f"{WINDOW_DAYS} days.</strong></p>"])
    items = []
    for r in _release_order(d.closed_in_window):
        gain = r.gain or "(row carried no Done-when clause — see the closing commit)"
        tail = f" · closed {r.closed_on}" if r.closed_on else ""
        tail += f" · <code>{_esc(r.sha)}</code>" if r.sha else ""
        items.append(f"<li><strong>{_esc(r.title)}</strong> [#{r.id}] → "
                     f'<span class="gain">{_esc(gain)}</span>{tail}</li>')
    return "\n".join(out + ['<ul class="rel">'] + items + ["</ul>"])


def _html_backlog(d: Dashboard) -> str:
    rows = [(t.theme, t.open, t.deferred, t.closed, _size_mix(t.sizes)) for t in d.themes]
    out = [f"<h2>{_esc(SECTION_TITLES[1])}</h2>",
           html_table(("Theme", "Open", "Deferred", "Closed", "Size mix (live rows)"), rows,
                      numeric=(1, 2, 3))]
    if d.total_open_prior is None:
        trend = (f"<strong>Total live rows: {d.total_open}.</strong> {WINDOW_DAYS}-day trend "
                 "<em>unavailable</em> — no committed BACKLOG.md at the window start.")
    else:
        delta = d.total_open - d.total_open_prior
        trend = (f"<strong>Total live rows: {d.total_open}</strong> "
                 f"({'+' if delta > 0 else ''}{delta} over {WINDOW_DAYS} days; "
                 f"{d.total_open_prior} at the window start).")
    closed = (" · ".join(f"[#{r.id}]" for r in _release_order(d.closed_in_window))
              or "none")
    out.append(f'<p class="card">{trend}<br>Closed this window: {_esc(closed)}</p>')
    return "\n".join(out)


def _html_intake(d: Dashboard) -> str:
    violations = [r for r in d.intake if r.verdict == VERDICT_VIOLATION]
    out = [f"<h2>{_esc(SECTION_TITLES[2])}</h2>",
           '<p class="note">Anti-orphan check, ACCEPTED docs only: an accepted intake must be '
           "carried by a live BACKLOG row, or be explicitly parked with a trigger / review date. "
           "Neither is a VIOLATION — reported here, repaired elsewhere.</p>"]
    if violations:
        names = " · ".join(f"#{r.intake_id or '?'} {r.filename}" for r in violations)
        out.append(f'<p class="card"><span class="badge violation">'
                   f"{len(violations)} VIOLATION</span> {_esc(names)}</p>")
    else:
        out.append('<p class="card"><span class="ok">No anti-orphan violations.</span></p>')
    order = {s: i for i, s in enumerate(INTAKE_STATUS_ORDER)}
    rows = []
    for r in sorted(d.intake, key=lambda r: (order.get(_status_bucket(r.status), 99),
                                             int(r.intake_id) if r.intake_id.isdigit() else 10**9)):
        status = r.status if r.status in INTAKE_STATUS_ORDER else f"{r.status} → {STATUS_UNKNOWN}"
        archived = "yes" if r.archived else ("no" if r.status in INTAKE_TERMINAL_STATUSES else "—")
        rows.append((f"#{r.intake_id}" if r.intake_id else "MISSING-ID", status, r.filename,
                     r.verdict or "—", r.detail or "—", archived))
    table = html_table(("Intake", "Status", "Doc", "Anti-orphan", "Detail", "Archived"), rows)
    for verdict in (VERDICT_VIOLATION,):
        table = table.replace(f"<td>{_esc(verdict)}</td>",
                              f'<td><span class="badge violation">{_esc(verdict)}</span></td>')
    return "\n".join(out + [table])


def _html_adrs(d: Dashboard) -> str:
    counts = _status_mix(d.adrs)
    flagged = [r for r in d.adrs if r.flag]
    out = [f"<h2>{_esc(SECTION_TITLES[3])}</h2>",
           '<p class="note">In this repo <strong>Accepted is not an archive trigger</strong> — '
           "docs/decisions/README.md keys the bar on Superseded / Deprecated only. The flag is a "
           "report; no file is moved.</p>",
           '<p class="card"><strong>Status mix:</strong> '
           + _esc(" · ".join(f"{k} {v}" for k, v in sorted(counts.items()))) + "</p>",
           '<p class="note">' + _md_to_text(_dialect_note(d.adrs)) + "</p>"]
    if flagged:
        rows = [(f"ADR-{r.number}", r.status, r.date, r.flag, r.title) for r in flagged]
        table = html_table(("ADR", "Status", "Date", "Flag", "Title"), rows)
        for flag in (FLAG_ARCHIVABLE, FLAG_OFF_ENUM, FLAG_UNPARSED, FLAG_OFF_GRAMMAR):
            table = table.replace(f"<td>{_esc(flag)}</td>",
                                  f'<td><span class="badge flag">{_esc(flag)}</span></td>')
        out.append(table)
    else:
        out.append('<p class="card"><span class="ok">No archival candidates and no off-enum or '
                   "unparsed status.</span></p>")
    rows = [(f"ADR-{r.number}", r.status, r.date, "archive/" if r.archived else "decisions/",
             r.dialect, r.title) for r in d.adrs]
    out.append(f"<details><summary>Full ledger ({len(d.adrs)} ADRs)</summary>"
               + html_table(("ADR", "Status", "Date", "Home", "Read as", "Title"), rows)
               + "</details>")
    return "\n".join(out)


def _html_telemetry(d: Dashboard) -> str:
    out = [f"<h2>{_esc(SECTION_TITLES[4])}</h2>"]
    if not d.telemetry.exists:
        out.append(f'<p class="card"><strong>{_esc(TELEMETRY_PENDING_NOTE)}.</strong><br>'
                   f"Expected store path: <code>{_esc(d.telemetry.relpath)}</code> — absent on "
                   "this tree.</p>")
        out.append('<p class="note">Read as a FILE, never as an import: '
                   "<code>scripts/telemetry_emit.py</code> and "
                   "<code>scripts/single_flight.py</code> belong to lane L2 ([#529]/[#530]).</p>")
    else:
        out.append(f'<p class="card">Emit store present at <code>{_esc(d.telemetry.relpath)}'
                   f"</code> ({d.telemetry.size_bytes} bytes).</p>")
        out.append('<p class="note">Presence only — reading the store\'s content is stage 2.</p>')
    return "\n".join(out)


def _html_gate(d: Dashboard) -> str:
    g = d.gate
    out = [f"<h2>{_esc(SECTION_TITLES[5])}</h2>"]
    if not g.rows:
        out.append('<p class="card"><strong>Ship-gate WARN composition not found</strong> on the '
                   "audit surface.</p>")
    else:
        label = g.columns[g.current_index] if 0 <= g.current_index < len(g.columns) else "current"
        out.append(f'<p class="note">Source <code>{_esc(g.source)}</code>; the '
                   f"<code>{_esc(label)}</code> column is the standing count.</p>")
        rows = [(name, *values) for name, values in g.rows]
        numeric = tuple(range(1, len(g.columns) + 1))
        out.append(html_table(("WARN class", *g.columns), rows, numeric=numeric))
        out.append(f'<p class="card"><strong>Standing WARN total: {g.current_total}</strong> '
                   f"across {len(g.rows)} classes.</p>")
    if g.commit_tax:
        out.append(f'<p class="card"><strong>Commit tax: {_esc(g.commit_tax)}</strong> (median), '
                   f"measured {_esc(g.commit_tax_date)} — source "
                   f"<code>{_esc(g.commit_tax_source)}</code>.</p>")
    else:
        out.append('<p class="card"><strong>Commit tax: not found</strong> on the audit '
                   "surface.</p>")
    out.append('<p class="note">Both figures are read off docs/audits/ rather than measured '
               "here: this generator must not call the gate it reports on.</p>")
    return "\n".join(out)


def render_html(d: Dashboard) -> str:
    """A self-contained page: inline CSS, no scripts, no network references of any kind."""
    body = "\n".join([
        "<main>",
        "<h1>Conformance dashboard — <code>.dev-knowledge</code></h1>",
        f'<p class="meta">As of {_esc(d.as_of or "(unknown)")} · HEAD '
        f'<code>{_esc(d.head_sha or "(unknown)")}</code> · window {_esc(d.since or "?")} → '
        f'{_esc(d.as_of or "?")} ({WINDOW_DAYS} days)</p>',
        '<p class="meta">Generated by <code>scripts/gen_dashboard.py</code> — do not edit by '
        "hand. Regenerate: <code>python scripts/gen_dashboard.py --write</code></p>",
        '<p class="note">Generated, committed, read-only (ADR-86 location + ADR-80 zone class). '
        "It reports rather than repairs: every VIOLATION and flag below is left exactly where it "
        "was found.</p>",
        _html_release(d), _html_backlog(d), _html_intake(d), _html_adrs(d),
        _html_telemetry(d), _html_gate(d),
        "</main>",
    ])
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>Conformance dashboard — .dev-knowledge</title>\n"
            f"<style>\n{_CSS}\n</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n")


# --------------------------------------------------------------------------- write / check

_TARGETS = ((MD_RELPATH, render_markdown), (HTML_RELPATH, render_html))


def write_outputs(repo_root: Path, git) -> int:
    dashboard = build(repo_root, git)
    for relpath, renderer in _TARGETS:
        path = repo_root / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(renderer(dashboard), encoding="utf-8", newline="\n")
        print(f"gen_dashboard: wrote {relpath}")
    return 0


def check_outputs(repo_root: Path, git) -> int:
    dashboard = build(repo_root, git)
    rc = 0
    for relpath, renderer in _TARGETS:
        path = repo_root / relpath
        expected = renderer(dashboard)
        if not path.is_file():
            print(f"gen_dashboard: MISSING {relpath} — run --write")
            rc = 1
            continue
        if path.read_text(encoding="utf-8") != expected:
            print(f"gen_dashboard: STALE {relpath} — regenerate with --write")
            rc = 1
    if rc == 0:
        print("gen_dashboard: up to date")
    return rc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the ecosystem conformance dashboard.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="emit the markdown + HTML outputs")
    group.add_argument("--check", action="store_true", help="regen-and-diff; 1 on drift")
    group.add_argument("--print", dest="to_stdout", action="store_true",
                       help="render the markdown to stdout without writing")
    args = parser.parse_args(argv)
    git = _reader(_REPO_ROOT)
    if args.write:
        return write_outputs(_REPO_ROOT, git)
    if args.check:
        return check_outputs(_REPO_ROOT, git)
    print(render_markdown(build(_REPO_ROOT, git)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
