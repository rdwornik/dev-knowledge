#!/usr/bin/env python
"""governance_health.py — FM-5, the value half of the funnel machine, scoped honest.

WHAT THIS IS. The library behind `audit.py governance-health`: a read-only command that
renders FM-4's FUNNEL HEALTH numbers ON DEMAND (a bundle carries them at cut time; this
answers between cuts), attaches a per-closed-row **"what it bought"** line sourced from the
repo's close packets, and appends one record of the run to the EXISTING telemetry store so
the numbers become a time series rather than a moment.

THE ONE RULE THIS MODULE IS BUILT AROUND. The lane's Ex-ante is *"the command runs on merged
main and its numbers equal FM-4's block byte-for-byte for the shared fields."* Byte-for-byte
equality between two renderers is achievable exactly one way: **both render from the same
function.** So this module computes **none** of FM-4's four fields. It resolves FM-4's emitter
and renders what that emitter returns; when the emitter is absent, the four fields render
`unavailable` with the resolution report attached. An `unavailable` is a true answer. A
locally-computed number that happens to look right is the failure this whole batch exists to
remove, and `tests/test_governance_health.py::test_no_fm4_owned_field_is_derivable_from_this_module`
enforces the absence structurally rather than by reading output.

ONE TRUTH RUNS BOTH WAYS, and this is the part a reader will not guess. FM-4's block carries
five fields, and the fifth — `value evidence attached` — is *this* lane's derivation: it can
only be computed by parsing close packets, which is FM-5's write-scope. So the ownership split
is:

    FM4_OWNED_FIELDS  intakes consumed-unarchived · ADRs unexecuted · orphans forward ·
                      orphans backward        -> imported, NEVER computed here
    FM5_OWNED_FIELDS  rows closed this window · value evidence attached
                      -> computed here, EXPORTED for FM-4 to import

`rows closed this window` sits on the FM-5 side by elimination and it is worth saying so
plainly: FM-2's four FAIL classes do not produce it and FM-4's contract does not derive it, so
somebody had to own it or the field would be computed twice. If a later ruling moves it, moving
it is a one-line change to the two tuples below and the equality test measures the result
unchanged.

VALUE EVIDENCE IS QUOTED, NEVER SYNTHESISED. A row's "what it bought" is a close packet's own
LINE, reproduced verbatim with a `docs/audits/<file>:<line>` locator. A row whose packets say
nothing renders `no value evidence` — a true and useful answer. Writing a plausible benefit
sentence for such a row is the named failure mode, so this module has no sentence-writing path
at all: it can only quote or say nothing.

  THE PREDICATE, AND ITS HONEST LIMITS. Every `[#id]` in a packet is a *mention*; only some
  mentions are *evidence*. A mention becomes evidence when its line also carries a value token
  — a verdict from `_VERDICT_RE` (MET / NOT-MET / PARTIAL / discharged / landed / shipped /
  delivered / closed / retired / superseded) or a measured quantity from `_DELTA_RE`
  (`77 -> 60`, `77 → 60`, `5 of 5`, `8/8`). That is a heuristic over prose and it fails both
  ways: a packet that records value in a sentence carrying none of those tokens is scored
  `no value evidence` (under-count), and a line that happens to pair an id with an unrelated
  ratio is scored as evidence (over-count). It is stated rather than hidden because the output
  is auditable by construction — every evidence line ships its locator, so a reader disputes a
  claim by opening the file, which is the property a summarised benefit could never offer.

A1 — NO SECOND STORE. `[#529]`'s `logs/TELEMETRY.db` (`scripts/telemetry_emit.py`) is this
repo's telemetry store: one append-only SQLite table in WAL mode, three event types. That
module's docstring records that wiring its CALL SURFACE is an owed phase-3 step and that a grep
for `telemetry_emit` outside it and its test "is expected to return nothing today"; `audit.py`
became its first call site at `[#529]` leg 1, and this command is a second one on the same
surface. It appends ONE `check_run` row named `governance_health` whose context carries every
shared field, so the trend is queryable with SQL and no new file, format or writer is born.
Emission follows `audit.telemetry_enabled()` — the existing switch, default OFF.

WHAT THIS IS NOT — the scope fence the contract states itself. Intake `#50`
(`docs/intake/2026-08-26-tech-cost-and-delivery-telemetry.md`) stays its own arc. That arc is a
weekly **cost-and-delivery** pipeline: it joins provider billing APIs, `ccusage` local token
usage, Codespaces core-hours and git delivery data, renders a Markdown report, **commits it**,
runs on a cron, and is explicitly *"the first CONSUMER arc (O4 parity), not a hub arc"*. This
command builds none of that: no provider API, no cost, no cron, no committed report, no consumer
repo — a hub CLI that renders numbers another lane derives and appends one local, gitignored
row. The boundary is the pipeline, and this module does not approach it.

LAYER-2 POSTURE (ADR-28/36, CLAUDE.md §5 rule 4). Read-only over the repo; the single write is
the local ephemeral `logs/TELEMETRY.db` row, which is the established in-repo pattern
`telemetry_emit.py` documents. Nothing here drives state in a child repo.
"""
from __future__ import annotations

import importlib
import re
import sys
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

# DUAL package/script import, and it is a regression fix rather than a style: `audit.py` imports
# this module, and `from scripts import audit` (package mode — repo ROOT on sys.path, not
# `scripts/`) is a supported entry point pinned by
# `tests/test_audit.py::test_check_fleet_parity_package_mode_import`. A bare `from gen_task_tree
# import ...` here raises ImportError under package mode, which `audit.py`'s own shim then
# mis-reads as "governance_health is absent" and the whole module fails to import. Same shape as
# the `_te`/`_vgb`/`_vdc` shims in `audit.py`.
try:
    from scripts.gen_task_tree import _TERMINAL_STATUSES, frontmatter_status
except ImportError:
    from gen_task_tree import _TERMINAL_STATUSES, frontmatter_status

#: The close-packet shapes, WITNESSED on disk (2026-08-29) rather than trusted from a list:
#: `docs/audits/2026-08-26-verification-batch-1-close-packet.md`,
#: `docs/audits/2026-08-27-verification-batch-w2-close-packet.md`,
#: `docs/audits/2026-08-29-verification-night-mission-close-packet.md` and
#: `docs/audits/2026-08-28-technical-batch1-end-of-batch-packet.md`. A per-lane
#: `*-nb2-<letter>-packet.md` is deliberately NOT a close packet: it is one lane's hand-back,
#: not the batch's account of what the batch bought.
CLOSE_PACKET_PATTERNS: tuple[str, ...] = ("*close-packet*.md", "*end-of-batch-packet*.md")

#: Rendered for any field this module refuses to compute. Never `0` — an unresolved number and
#: a measured zero are different facts, the same distinction `telemetry_emit.UNKNOWN` exists for.
UNAVAILABLE = "unavailable"

#: What a row with no quotable packet line renders as.
NO_VALUE_EVIDENCE = "no value evidence"

#: The block's first line. Matches FM-4's block header so the two surfaces read alike.
HEALTH_HEADER = "FUNNEL HEALTH"

#: The event `name` this command appends under. One name, so a trend query is one `WHERE`.
TELEMETRY_NAME = "governance_health"

#: FM-4's five contract fields, with "orphans, both directions" rendered as the two numbers it
#: names. Order IS the contract — a golden test pins it on FM-4's side and on this one.
FM4_OWNED_FIELDS: tuple[str, ...] = (
    "intakes consumed-unarchived",
    "ADRs unexecuted",
    "orphans forward",
    "orphans backward",
)
FM5_OWNED_FIELDS: tuple[str, ...] = (
    "rows closed this window",
    "value evidence attached",
)
SHARED_FIELDS: tuple[str, ...] = FM4_OWNED_FIELDS + FM5_OWNED_FIELDS

#: The module FM-4's emitter lands in. `scripts/gen_handoff.py` is the handoff assembler —
#: `generate()` at :906 assembles a bundle and `_window()` at :641 resolves the window this
#: module reuses — and FM-4's write-scope is "the handoff assembler module + tests".
FM4_MODULE = "gen_handoff"

#: FM-4's contract does not name its emitting function, so this resolves by CAPABILITY rather
#: than by a guessed name: a public callable whose name carries both "funnel" and "health".
#: Two matches is an AMBIGUITY and is refused — picking one would be a guess wearing a
#: resolution's clothes, and an `unavailable` naming both candidates is the honest answer.
FM4_CALLABLE_RE = re.compile(r"(?=.*funnel)(?=.*health)", re.IGNORECASE)

#: Anti-bluff, asserted rather than promised: no commit sha may appear in the health block.
SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")

_ROW_RE = re.compile(r"\[#(\d+)\]")

#: A verdict token. `\bclosed\b` and NOT `close`, so the extremely common word "closure"
#: ("two closure candidates, reported not filed") does not silently become value evidence.
_VERDICT_RE = re.compile(
    r"\b(?:MET|NOT-MET|PARTIAL|discharged|landed|lands|shipped|delivered|"
    r"closed|retired|superseded)\b",
    re.IGNORECASE,
)

#: A measured quantity: a before->after delta or an n-of-m tally. Deliberately NOT `\d+ to \d+`
#: — English uses "to" for far more than deltas, and a predicate that scores "in 2 to 3 days" as
#: value evidence is worse than one that misses a delta written in words.
_DELTA_RE = re.compile(r"\d+\s*(?:->|→|-->)\s*\d+|\b\d+\s*/\s*\d+\b|\b\d+\s+of\s+\d+\b")


@dataclass(frozen=True)
class ValueEvidence:
    """One quoted close-packet line, with the locator that makes it disputable."""

    row_id: int
    text: str
    locator: str


@dataclass
class Fm4Source:
    """Where the four FM-4-owned numbers came from, or why they did not come."""

    available: bool
    dotted: str | None
    reason: str
    render: Callable[[Path], str] | None = None


@dataclass
class Report:
    shared: dict[str, str]
    rows: dict[int, list[ValueEvidence]]
    fm4: Fm4Source
    window_base: str | None
    packets: list[Path] = field(default_factory=list)
    duration_ms: int = 0


# ---------------------------------------------------------------------------------------
# Close packets and the value they record
# ---------------------------------------------------------------------------------------

def close_packets(repo_root: Path) -> list[Path]:
    """Every close packet under `docs/audits/`, sorted by name (== chronological here)."""
    audits = Path(repo_root) / "docs" / "audits"
    if not audits.is_dir():
        return []
    found: set[Path] = set()
    for pattern in CLOSE_PACKET_PATTERNS:
        found.update(p for p in audits.glob(pattern) if p.is_file())
    return sorted(found)


def is_value_line(line: str) -> bool:
    """Does this line carry a value token — a verdict or a measured quantity?

    Separate from `value_evidence` so the predicate is testable on its own; the case that
    matters is the NEGATIVE one, because a predicate that matches every mention reports 100%
    coverage forever and measures nothing.
    """
    return bool(_VERDICT_RE.search(line) or _DELTA_RE.search(line))


def value_evidence(repo_root: Path, row_ids: Iterable[int],
                   packets: Sequence[Path] | None = None) -> dict[int, list[ValueEvidence]]:
    """For each row id, the close-packet lines that say what it bought — verbatim.

    Every requested id appears in the result, mapped to `[]` when nothing quotable was found:
    the absence is a reportable fact, so it is represented rather than omitted.
    """
    root = Path(repo_root)
    wanted = {int(r) for r in row_ids}
    out: dict[int, list[ValueEvidence]] = {r: [] for r in sorted(wanted)}
    for packet in (close_packets(root) if packets is None else packets):
        rel = packet.relative_to(root).as_posix()
        text = packet.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            cited = {int(m) for m in _ROW_RE.findall(line)} & wanted
            if not cited or not is_value_line(line):
                continue
            for row_id in sorted(cited):
                out[row_id].append(ValueEvidence(row_id, line.rstrip(), f"{rel}:{lineno}"))
    return out


def coverage(found: Mapping[int, list[ValueEvidence]]) -> tuple[int, int]:
    """`(rows carrying value evidence, rows considered)` — the fraction the contract asks for."""
    return sum(1 for evs in found.values() if evs), len(found)


# ---------------------------------------------------------------------------------------
# The window, and the rows that closed inside it
# ---------------------------------------------------------------------------------------

def _handoff():
    """`gen_handoff`, or `None` if it will not import. Lazy and non-fatal on purpose: this
    module must be able to REPORT that FM-4's home is unreachable, not die because it is.

    Both import shapes are tried for the same reason the top-of-module shim exists: under
    package mode only `scripts.gen_handoff` resolves, and a resolver that silently returned
    `None` there would report "FM-4 has not landed" about a tree where it had.
    """
    for name in (f"scripts.{FM4_MODULE}", FM4_MODULE):
        try:
            return importlib.import_module(name)
        except Exception:  # noqa: BLE001 - any import failure is the same fact to a reporter
            continue
    return None


def window_base_sha(repo_root: Path) -> str | None:
    """The commit the current window opens at, or `None` when it cannot be resolved.

    THE WINDOW IS NOT REDEFINED HERE. `gen_handoff._window` states this repo's definition — the
    diff since the PREVIOUS bundle was added, "resolved from git rather than from the seat's
    memory" — and that function returns the previous bundle's SLUG and the changed paths, not
    the boundary sha. This re-runs its one documented git command to get the sha, which is a
    duplicated CALL and not a second definition; when FM-4 exposes a sha-returning window
    resolver, this delegates to it. Filed as a consolidation candidate rather than left silent.
    """
    mod = _handoff()
    if mod is None:
        return None
    ok, sha = mod._git_status(Path(repo_root), "log", "-1", "--format=%H", "--diff-filter=A",
                              "--", "docs/handoffs/*/HANDOFF_BOOT.md")
    return sha.strip() if ok and sha.strip() else None


def rows_closed_in_window(repo_root: Path, base: str | None = None) -> list[int] | None:
    """Backlog rows that became terminal inside the window, or `None` if it cannot be computed.

    TERMINAL means `gen_task_tree._TERMINAL_STATUSES` — imported, so this cannot drift from the
    generator that owns the vocabulary. A row counts only when it was NOT terminal at the
    window's base and IS terminal now, so a closed row merely re-edited inside the window does
    not inflate the number.
    """
    root = Path(repo_root)
    mod = _handoff()
    base = base if base is not None else window_base_sha(root)
    if mod is None or base is None:
        return None
    ok, changed = mod._git_status(root, "diff", "--name-only", f"{base}..HEAD", "--", "tasks")
    if not ok:
        return None

    closed: list[int] = []
    for rel in (ln.strip() for ln in changed.splitlines()):
        if not rel.endswith(".md") or not rel.startswith("tasks/"):
            continue
        path = root / rel
        if not path.is_file():
            continue
        if frontmatter_status(path.read_text(encoding="utf-8", errors="replace")) \
                not in _TERMINAL_STATUSES:
            continue
        was_ok, before = mod._git_status(root, "show", f"{base}:{rel}")
        if was_ok and frontmatter_status(before) in _TERMINAL_STATUSES:
            continue  # already terminal when the window opened
        try:
            closed.append(int(Path(rel).name.split("-", 1)[0]))
        except ValueError:
            continue
    return sorted(set(closed))


# ---------------------------------------------------------------------------------------
# FM-4's emitter — resolved, never re-implemented
# ---------------------------------------------------------------------------------------

def resolve_fm4_emitter() -> Fm4Source:
    """Find FM-4's FUNNEL HEALTH emitter, or report precisely why it was not found."""
    mod = _handoff()
    if mod is None:
        return Fm4Source(False, None, f"{FM4_MODULE} did not import")
    names = sorted(n for n in dir(mod)
                   if not n.startswith("__")
                   and callable(getattr(mod, n, None))
                   and FM4_CALLABLE_RE.match(n))
    if not names:
        # Two different facts produce this branch and the message must not collapse them into
        # the flattering one: FM-4 may not have landed, OR it landed under a name this rule
        # does not match. Both are resolution failures; neither is a measured equality. The
        # public roster is printed so the reader settles which one it is by looking.
        public = sorted(n for n in dir(mod)
                        if not n.startswith("_") and callable(getattr(mod, n, None)))
        return Fm4Source(
            False, None,
            f"no callable in {FM4_MODULE} matches /funnel.*health|health.*funnel/ — either "
            f"FM-4 (lane K) has not landed its emitter in this tree, or it landed under a name "
            f"this resolver's rule does not match. {FM4_MODULE}'s public callables: "
            f"{', '.join(public) or '(none)'}")
    if len(names) > 1:
        return Fm4Source(
            False, None,
            f"ambiguous: {FM4_MODULE} exposes {len(names)} candidates ({', '.join(names)}) — "
            f"refusing to pick one; a resolution rule, not a guess, decides this")
    fn = getattr(mod, names[0])
    return Fm4Source(True, f"{FM4_MODULE}:{names[0]}", "resolved", render=fn)


# ---------------------------------------------------------------------------------------
# The report
# ---------------------------------------------------------------------------------------

def parse_shared_fields(block: str) -> dict[str, str]:
    """`field -> value` for every `  <field>: <value>` line in a rendered block.

    The comparison surface for the Ex-ante: it parses THIS module's block and FM-4's with one
    function, so an equality failure is a real disagreement about a number and never two
    parsers disagreeing about a format.
    """
    out: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line or line.startswith(HEALTH_HEADER):
            continue
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
    return out


def build_report(repo_root: Path, *, source: Fm4Source | None = None) -> Report:
    """Assemble the report. Computes the FM-5-owned half; IMPORTS the FM-4-owned half."""
    started = time.perf_counter()
    root = Path(repo_root)
    src = source if source is not None else resolve_fm4_emitter()

    shared: dict[str, str] = dict.fromkeys(SHARED_FIELDS, UNAVAILABLE)
    if src.available and src.render is not None:
        theirs = parse_shared_fields(src.render(root))
        for name in FM4_OWNED_FIELDS:
            if name in theirs:
                shared[name] = theirs[name]

    base = window_base_sha(root)
    closed = rows_closed_in_window(root, base)
    packets = close_packets(root)
    rows: dict[int, list[ValueEvidence]] = {}
    if closed is not None:
        rows = value_evidence(root, closed, packets)
        attached, considered = coverage(rows)
        shared["rows closed this window"] = str(considered)
        shared["value evidence attached"] = str(attached)

    return Report(shared=shared, rows=rows, fm4=src, window_base=base, packets=packets,
                  duration_ms=int((time.perf_counter() - started) * 1000))


def render_health_block(report: Report) -> str:
    """FM-4's block, rendered here. NUMBERS ONLY — no verdicts, no shas, no adjectives."""
    lines = [HEALTH_HEADER]
    lines += [f"  {name}: {report.shared[name]}" for name in SHARED_FIELDS]
    return "\n".join(lines)


def render_value_section(found: Mapping[int, list[ValueEvidence]]) -> str:
    """What each closed row bought — quoted from close packets, with locators."""
    attached, considered = coverage(found)
    lines = ["VALUE — what each closed row bought "
             "(verbatim from close packets; never invented)"]
    if not found:
        lines.append(f"  (no closed rows in this window, or the window is {UNAVAILABLE})")
    for row_id in sorted(found):
        evidence = found[row_id]
        if not evidence:
            lines.append(f"  [#{row_id}] — {NO_VALUE_EVIDENCE}")
            continue
        for ev in evidence:
            lines.append(f"  [#{row_id}] — {ev.locator} — {ev.text}")
    lines.append(f"  coverage: {attached}/{considered} rows carry value evidence, "
                 f"{considered - attached} do not")
    return "\n".join(lines)


def console_safe(text: str, encoding: str | None = None) -> str:
    """`text`, made writable on THIS console without losing what it said.

    NOT a nicety. This command quotes arbitrary close-packet prose, and `audit.py`'s output
    goes through `click.echo`, which raises `UnicodeEncodeError` on a Windows cp1252 console
    for any character outside cp1252 — the same trap `check_doc_code_edge` carries an
    "ASCII arrow" comment about (`audit.py`, the `doc->code edge(s) resolved` finding). It is
    live, not hypothetical: `docs/audits/2026-08-26-verification-batch-1-close-packet.md`
    contains U+2192, and `_DELTA_RE` matches `77 → 60` — so the very lines this command exists
    to quote are the ones most likely to carry it.

    `backslashreplace` and not `?` or `ignore`: an escape a reader can decode (`\\u2192`)
    preserves the evidence, and silently deleting a character out of a line advertised as
    verbatim would be the worst available outcome.
    """
    enc = encoding or getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        text.encode(enc)
    except (UnicodeEncodeError, LookupError):
        return text.encode(enc, errors="backslashreplace").decode(enc)
    return text


def render(report: Report) -> str:
    """The whole command output.

    The health block is byte-comparable with FM-4's and carries the anti-bluff contract. The
    provenance and value sections sit OUTSIDE it — they quote packet prose, which legitimately
    contains verdicts and shas, and this is a CLI report, never a browser-visible bundle.
    """
    provenance = (f"FM-4 emitter: {report.fm4.dotted}" if report.fm4.available
                  else f"FM-4 emitter: {UNAVAILABLE} — {report.fm4.reason}")
    window = report.window_base or UNAVAILABLE
    return "\n\n".join((
        f"governance-health\n  {provenance}\n  window base: {window}\n"
        f"  close packets read: {len(report.packets)}",
        render_health_block(report),
        render_value_section(report.rows),
    ))


# ---------------------------------------------------------------------------------------
# A1 — one appended record in the EXISTING store
# ---------------------------------------------------------------------------------------

def telemetry_context(report: Report) -> dict:
    """What the appended record carries. The NUMBERS ride along, not just an outcome — a trend
    that has to re-derive its own values from a timestamp is not a trend."""
    attached, considered = coverage(report.rows)
    return {
        "shared": dict(report.shared),
        "fm4_source": report.fm4.dotted if report.fm4.available else UNAVAILABLE,
        "window_base": report.window_base or UNAVAILABLE,
        "close_packets": len(report.packets),
        "value_coverage": {"attached": attached, "considered": considered},
    }


def emit(report: Report, db_path=None, repo_path=None) -> int | None:
    """Append ONE `check_run` row to `[#529]`'s store. No second store, no new format.

    `git_derived=True` because the window is resolved from git history, which makes the
    constraint-1 refusal on a shallow clone the right behaviour: a window computed over
    truncated history yields a number that looks measured and is wrong.
    """
    try:
        from scripts import telemetry_emit as _te
    except ImportError:
        import telemetry_emit as _te
    return _te.emit_check_run(
        TELEMETRY_NAME, "pass",
        duration_ms=report.duration_ms,
        context=telemetry_context(report),
        db_path=db_path,
        repo_path=repo_path,
        git_derived=True,
    )
