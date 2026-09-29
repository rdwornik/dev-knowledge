#!/usr/bin/env python
"""handoff_state.py -- the handoff boot's STATE ROWS, read live and evidence-bearing
(LANE-5B4-17-handoff-min, Part A of `to-browser/PROPOSAL-ADR-HANDOFF-SYSTEM-2026-09-26.md`).

THE ABSENCE THIS FILLS. The Context measured it directly: of the operator's nine boot-time
items (state, rulings, pending decisions, plan, capability map, substrates, transport,
working rules, CI), the 2026-09-24 bundle carried ONE with a live check (P13) and one partly
(P8b). Everything else was either absent from the boot or a fact the incoming seat had to go
re-derive by hand. This module is the reader half of the fix: SEVEN state rows, each a THIN
CALL into an organ that already exists (`ci_verdict`, `batch_manifest`, `seat_registry`, the
two ecosystem registries, and the newest transport RATIFICATION / DIGEST-CAPABILITY-MAP), so
the boot states a fact and the fact is never a second copy of one already computed elsewhere.
THIS MODULE DEFINES NO NEW REGISTRY -- it composes readers that already have one.

THE NINE-ITEM ROSTER, and an honest gap. The Context's own nine-item list is measured against
`SESSION-decision-handoff-system-2026-09-26.md` §1.2, a document outside this lane's read
scope (Part A's "Read first" list does not name it). Rather than claim a byte-identical
mapping to a source this lane never opened, `OPERATOR_ROSTER` below is this lane's OWN
nine-item roster, built from the Context paragraph's own words, with an explicit per-item
mapping to the row (if any) that now covers it live. Two items stay uncovered on purpose:
"pending decisions" (an ADR/intake triage question this lane's Owns list gives it no reader
for) and "working rules" (STANDING_RULINGS is read as a PPOINTER row already, in
`gen_handoff.boot_data_rows`, not re-derived here) -- naming the gap is the discipline; a
roster with no gap would be a roster inflated to hit the number.

EVERY ROW IS A `StateRow`: a value, a freshness class, and the evidence locator that produced
it, following `seat_state.py`'s own discipline one level up -- a fact with no evidence is not
one this module hands out. `StateRow.rendered()` is the EXACT string both the generator
(`gen_handoff.boot_data_rows`) and the verifier (`verify_handoff_probes.BOOT_DATA_RULES`) use:
the generator writes it once at cut time, the verifier calls the SAME function again at
check time and compares the two strings. Equal -> PASS. A generator and a verifier that called
two different readers could drift forever without either side noticing; calling the one
function from both ends is what makes the row's own claim -- "checked live" -- true rather
than decorative.

THE THREE FRESHNESS CLASSES (the seat_state.py precedent, one layer up: a fact with no
evidence is not a fact this module hands out):
  * CUT-FIXED  -- true at cut time and not expected to differ at boot (none of today's seven
                  rows are CUT-FIXED; the class exists for a future row whose value is an
                  identity rather than a live read, and is named here so Part B's rows have
                  a home to declare it in).
  * LIVE-DRIFTS -- may have changed between cut and boot; Part A's rule (unlike Part B's
                  planned "drift as data") still FAILS a mismatch, because this lane does not
                  build the seat-boot moment that would report drift instead of refusing it
                  (Not in A: moments). CI, Batches and Seats are LIVE-DRIFTS.
  * SLOW       -- changes on a batch or a config-edit cadence, not turn to turn. Substrates,
                  Transport, Rulings and Capabilities are SLOW.

HONEST LIMITS
  * `row_ci` reads `origin/main`'s Actions verdict through `ci_verdict.verdict_for` with
    `timeout_s=0` -- ONE non-blocking poll, never the 900 s default wait. A cut is a
    once-per-window act and this reader runs on every dry-cut and every verify pass; a
    blocking wait on either end would make the boot's own generation slower than the CI run
    it reports on. `timeout_s=0` means a run still queued reads `not-run`, correctly -- this
    row states what CI said BY THE TIME OF THE CALL, never what it will say.
  * `row_ci` skips `gh` ENTIRELY when `repo_root` carries no `.git` -- not merely lets
    `ci_verdict` fail into it. A stub/fixture repo (no git identity) would otherwise still
    spawn a real `gh run list` against whatever directory happens to be `cwd`, which is slow
    (measured ~1.2 s) and a needless external dependency for a row whose honest answer, with
    no git identity to resolve a sha from, is simply "not a git repository".
  * `row_seats` reads the MACHINE-WIDE `~/.claude/seat-registry.jsonl` (`seat_registry.
    REGISTRY_PATH`) -- real, live, cross-repo state. Its value is whatever the machine's
    actual seat traffic is at call time; the equality check this buys is "the generator and
    the verifier read the same file at their own respective moments", never "the value is
    stable across a whole test run". `path=` lets a caller (a test) point it at a fixture.
    It calls `seat_health_line(..., elapsed=False)` (LANE-5B4-17 repair 1) so a named
    wedged/starved seat's detail is its last event's FIXED timestamp, never a "NN min since
    last event" figure that ages every minute on its own with no seat-state change --
    otherwise a bundle cut at T and re-verified at T+1 min would fail BD-seats on the clock
    alone. A real seat-state change (a seat crossing into/out of wedged or starved, or its
    counts changing) still correctly mismatches; only the cosmetic elapsed-time figure is
    now held fixed.
  * `row_rulings` / `row_capabilities` resolve "newest" by the dated token in the FILENAME
    (`YYYY-MM-DD`), falling back to mtime only when two candidates share a date -- never by
    directory-listing order, which the OS does not guarantee. A `-vN-superseded.md` sibling
    (the OPERATOR-INTERFACE revision convention) is excluded by name, never by content.
  * `row_capabilities` parses ONE markdown table (the first `## ...Table...` heading's body)
    with a plain `|`-split reader, the same shape `batch_manifest.manifest_lane_slugs` already
    uses for its own bounded section -- not a general markdown-table parser. A cell containing
    a literal `|` would mis-split; none does in a DIGEST-CAPABILITY-MAP table today.
  * Every row function DEGRADES on any exception (missing file, bad YAML, an unreadable
    transport) to a `StateRow` reporting `unavailable -- <exception>`, never a raise. A boot
    row that could crash the cut it appears in would be worse than the fact it is trying to
    surface; and because both the generator and the verifier hit the SAME failure the SAME
    way, a degraded row is still an equal-both-ways pass, not a silent hole (it is visibly
    "unavailable", not invisibly absent).

Library-first (O-12): stdlib (`re`, `dataclasses`, `pathlib`) + PyYAML (already a declared
dependency, `pyproject.toml` -- "scripts/ validators"), reusing `ci_verdict`, `batch_manifest`
and `seat_registry` rather than re-deriving any of their reads.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:                    # dual-import shim, as every sibling uses
    sys.path.insert(0, str(_SCRIPTS))

try:
    import ci_verdict as _civ
    import batch_manifest as _bm
    import seat_registry as _sr
except ImportError:                                  # imported as `scripts.handoff_state`
    from scripts import ci_verdict as _civ            # type: ignore[no-redef]
    from scripts import batch_manifest as _bm         # type: ignore[no-redef]
    from scripts import seat_registry as _sr          # type: ignore[no-redef]

#: The closed enum a row's freshness must be one of -- see the module docstring.
FRESHNESS_CLASSES: tuple[str, ...] = ("CUT-FIXED", "LIVE-DRIFTS", "SLOW")


@dataclass(frozen=True)
class StateRow:
    """One boot-data state row: a value, its freshness class, and the evidence locator that
    produced it. `rendered()` is the ONE string both the generator and the verifier use -- see
    the module docstring for why a shared function, not a shared constant, is what keeps them
    from drifting apart."""
    key: str
    value: str
    freshness: str
    evidence: str

    def __post_init__(self) -> None:
        if self.freshness not in FRESHNESS_CLASSES:
            raise ValueError(f"{self.key!r}: freshness {self.freshness!r} is outside "
                             f"{{{', '.join(FRESHNESS_CLASSES)}}}")

    def rendered(self) -> str:
        """The exact DATA-row value cell: the fact, its freshness class, and the evidence
        locator that a reader could re-run to confirm it. `|` is replaced (a table cell) and
        embedded newlines are flattened (a DATA row is one line), mirroring the sanitizing
        `.replace("|", "/")` this codebase already applies at its other probe-detail sites."""
        flat = " ".join(self.value.split())
        return f"{flat} — evidence: {self.evidence} [{self.freshness}]".replace("|", "/")


def _degraded(key: str, evidence: str, freshness: str, exc: BaseException) -> StateRow:
    return StateRow(key, f"unavailable — {type(exc).__name__}: {exc}", freshness, evidence)


# --- CI: origin/main's sha and Actions verdict, ONE non-blocking poll ------------------------

def row_ci(repo_root: "Path | str") -> StateRow:
    evidence = 'ci_verdict.verdict_for("origin/main", timeout_s=0)'
    repo_root = Path(repo_root)
    if not (repo_root / ".git").exists():
        return StateRow("CI", "not a git repository — CI cannot be read", "LIVE-DRIFTS", evidence)
    try:
        v = _civ.verdict_for("origin/main", repo_root=repo_root, timeout_s=0, interval_s=1)
    except Exception as exc:                          # noqa: BLE001 -- degrade, never crash a cut
        return _degraded("CI", evidence, "LIVE-DRIFTS", exc)
    sha7 = (v.sha or "?")[:7]
    if v.verdict == _civ.STATE_GREEN:
        value = f"`{sha7}` GREEN (run {v.run_id})"
    elif v.verdict == _civ.STATE_RED:
        value = f"`{sha7}` RED ({len(v.new_reds)} new red(s), run {v.run_id})"
    else:
        value = f"`{sha7}` NOT-RUN ({v.reason[:80]})"
    return StateRow("CI", value, "LIVE-DRIFTS", evidence)


# --- Batches: committed manifests declaring an open batch right now --------------------------

def row_batches(repo_root: "Path | str") -> StateRow:
    evidence = "batch_manifest.open_batches"
    try:
        open_now = list(_bm.open_batches(Path(repo_root)))
    except Exception as exc:                          # noqa: BLE001
        return _degraded("Batches", evidence, "LIVE-DRIFTS", exc)
    value = ("no batch open" if not open_now else
             "; ".join(f"{b.batch} (`{b.path}`, closes on `{b.closed_by}`)" for b in open_now))
    return StateRow("Batches", value, "LIVE-DRIFTS", evidence)


# --- Seats: the seat registry's own health line -----------------------------------------------

#: The value `row_seats` renders when the lookback window holds nothing -- named so
#: `verify_handoff_probes._rule_bd_seats` ([#1124]) can recognize this ONE other well-formed
#: shape a cut value may carry (besides a `[seats] …` line) without duplicating the literal.
NO_SEATS_OBSERVED = "no seats observed in the lookback window"


def row_seats(*, path: "Path | None" = None) -> StateRow:
    evidence = "seat_registry.seat_health_line(elapsed=False)"
    try:
        line = _sr.seat_health_line(path, elapsed=False)
    except Exception as exc:                          # noqa: BLE001
        return _degraded("Seats", evidence, "LIVE-DRIFTS", exc)
    value = line if line else NO_SEATS_OBSERVED
    return StateRow("Seats", value, "LIVE-DRIFTS", evidence)


# --- Substrates: which dispatch substrates are live, per the registry ------------------------

def row_substrates(repo_root: "Path | str") -> StateRow:
    evidence = "ecosystem/substrate-registry.yaml"
    path = Path(repo_root) / "ecosystem" / "substrate-registry.yaml"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        subs = data.get("substrates") or {}
        live = sorted(name for name, cfg in subs.items()
                      if isinstance(cfg, dict) and cfg.get("live"))
        total = len(subs)
    except Exception as exc:                          # noqa: BLE001
        return _degraded("Substrates", evidence, "SLOW", exc)
    value = f"{len(live)}/{total} live: {', '.join(live) if live else 'none'}"
    return StateRow("Substrates", value, "SLOW", evidence)


# --- Transport: the registered transport-file kinds -------------------------------------------

def row_transport(repo_root: "Path | str") -> StateRow:
    evidence = "ecosystem/transport-registry.yaml"
    path = Path(repo_root) / "ecosystem" / "transport-registry.yaml"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        kinds = data.get("kinds") or []
    except Exception as exc:                          # noqa: BLE001
        return _degraded("Transport", evidence, "SLOW", exc)
    value = f"{len(kinds)} kind(s) registered"
    return StateRow("Transport", value, "SLOW", evidence)


# --- Rulings / Capabilities: the newest transport RATIFICATION / DIGEST-CAPABILITY-MAP -------

#: A dated transport filename's own date token, read from the NAME (never mtime alone) so a
#: file copied or re-synced by Drive still resolves to the date it was WRITTEN for.
_DATED_STEM_RE = re.compile(r"-(\d{4}-\d{2}-\d{2})(?:-v\d+(?:-superseded)?)?\.md$")
_SUPERSEDED_RE = re.compile(r"-v\d+-superseded\.md$")


def _newest_transport_doc(transport: "Path | None", prefix: str) -> "Path | None":
    """The newest non-superseded `<prefix>-*.md` under `transport/to-browser/`, by the date
    token in its own filename (ties broken by mtime) -- or None when `transport` is
    unresolved or nothing matches. See the module docstring's honest limit on this resolution."""
    if transport is None:
        return None
    candidates: list[tuple[str, float, Path]] = []
    for p in Path(transport).glob(f"to-browser/{prefix}-*.md"):
        if not p.is_file() or _SUPERSEDED_RE.search(p.name):
            continue
        m = _DATED_STEM_RE.search(p.name)
        date = m.group(1) if m else ""
        try:
            mtime = p.stat().st_mtime
        except OSError:
            mtime = 0.0
        candidates.append((date, mtime, p))
    if not candidates:
        return None
    candidates.sort()
    return candidates[-1][2]


#: A ruling id, either as a bulleted restatement (`- **R1** ...`) or a new ruling's own heading
#: (`## R22 — ...`) -- the two shapes `RATIFICATION-2026-09-25.md` itself carries.
_RULING_ID_RE = re.compile(r"(?m)^(?:-\s+\*\*R(\d+)\*\*|#{1,6}\s+R(\d+)\b)")


def row_rulings(transport: "Path | None") -> StateRow:
    locator = "to-browser/RATIFICATION-*.md (newest, non-superseded)"
    doc = _newest_transport_doc(transport, "RATIFICATION")
    if doc is None:
        return StateRow("Rulings", "no RATIFICATION file found on the transport", "SLOW", locator)
    try:
        text = doc.read_text(encoding="utf-8", errors="replace")
        nums = sorted({int(a or b) for a, b in _RULING_ID_RE.findall(text)})
    except Exception as exc:                          # noqa: BLE001
        return _degraded("Rulings", f"{locator} (`{doc.name}`)", "SLOW", exc)
    value = (f"0 rulings parsed from `{doc.name}`" if not nums else
             f"R1–R{nums[-1]} ({len(nums)} ruling(s)) — `{doc.name}`")
    return StateRow("Rulings", value, "SLOW", locator)


#: The digest's own table heading, e.g. "## Table (at 1f3f318c)" -- any heading level, any
#: trailing words, so a future digest's parenthetical does not need this regex to change.
_TABLE_HEADING_RE = re.compile(r"(?m)^#{1,6}\s*Table\b.*$")
_ANY_HEADING_RE = re.compile(r"(?m)^#{1,6}\s+\S")


def _split_table_row(line: str) -> list[str]:
    """Split one markdown table row into cells, honoring a backslash-escaped pipe (`\\|`) as
    LITERAL rather than a column delimiter -- the escaping convention the capability digest
    itself uses for a pipe inside a cell's own prose (e.g. `` `O_CREAT\\|O_EXCL` ``, row 1's
    mechanism cell in the live 2026-09-28 map). A naive `line.split("|")` over-splits such a
    cell and shifts every LATER column's index for that one row -- exactly the misalignment
    the header-mapped status column below exists to prevent.

    Escaping is by BACKSLASH-RUN PARITY, not "any backslash immediately before a pipe": a
    fixed-width regex lookbehind (`(?<!\\)\\|`, the prior implementation) cannot tell an
    escaped pipe (one backslash) from a literal trailing backslash immediately followed by a
    REAL delimiter pipe (two backslashes) -- it treated both as escaped, silently swallowing
    a genuine delimiter and shifting every later column (terra HIGH, 2026-09-29). Counting the
    run of consecutive backslashes ending at each `|` and splitting only on an EVEN run
    (0, 2, 4, ... -- including zero) keeps the single-backslash convention above working
    identically while fixing the even-run case."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells: list[str] = []
    start = 0
    for i, ch in enumerate(s):
        if ch != "|":
            continue
        run = 0
        j = i - 1
        while j >= 0 and s[j] == "\\":
            run += 1
            j -= 1
        if run % 2 == 0:
            cells.append(s[start:i])
            start = i + 1
    cells.append(s[start:])
    return [c.strip() for c in cells]


def _capability_table(text: str) -> tuple[list[str], list[list[str]]]:
    """(header_cells, data_rows) of the digest's own `## ... Table ...` section -- `([], [])`
    when the heading is absent, not a parse failure (see the module docstring's honest limit:
    a bounded reader, not a general markdown-table parser). The section's FIRST `|`-line is
    the header, its SECOND the `---` separator (skipped), and every later `|`-line whose first
    cell is a digit is a data row."""
    heading = _TABLE_HEADING_RE.search(text)
    if heading is None:
        return [], []
    start = heading.end()
    nxt = _ANY_HEADING_RE.search(text, start)
    body = text[start:nxt.start()] if nxt else text[start:]
    lines = [ln.strip() for ln in body.splitlines() if ln.strip().startswith("|")]
    if not lines:
        return [], []
    header = _split_table_row(lines[0])
    rows: list[list[str]] = []
    for line in lines[2:]:                      # [0] header, [1] `---` separator, skipped
        cells = _split_table_row(line)
        if cells and cells[0].isdigit():
            rows.append(cells)
    return header, rows


def _status_col(header: list[str]) -> "int | None":
    """The index of the header cell literally reading 'status' (case-insensitive, trimmed) --
    or None. Matched by EXACT cell text, never substring/`in`: 'fails when violated' is also a
    cell of this same header and must never be mistaken for the status column ([#1124] batch
    L6 fix: the prior reader used the row's LAST cell, which is 'status' only by coincidence in
    a 3-column test fixture -- the live digest's status column sits second-to-last, before a
    trailing 'delta vs …' column, so the old reader silently counted the WRONG cell and always
    read 0 WORKS)."""
    for idx, cell in enumerate(header):
        if cell.strip().lower() == "status":
            return idx
    return None


def row_capabilities(transport: "Path | None") -> StateRow:
    locator = "to-browser/DIGEST-CAPABILITY-MAP-*.md (newest)"
    doc = _newest_transport_doc(transport, "DIGEST-CAPABILITY-MAP")
    if doc is None:
        return StateRow("Capabilities", "no DIGEST-CAPABILITY-MAP file found on the transport",
                        "SLOW", locator)
    try:
        text = doc.read_text(encoding="utf-8", errors="replace")
        header, rows = _capability_table(text)
        col = _status_col(header)
        total = len(rows)
        statuses = [r[col].strip() for r in rows if col is not None and col < len(r)]
        # DECIDED-BY-LANE (batch WAVE5B-N5-R, lane-handoff-probes, [#1124] item 2): a status
        # cell COUNTS toward WORKS whenever it starts with the literal word "WORKS" -- bare
        # "WORKS" and a qualified cell ("WORKS (partial)", "WORKS grammar / attributes
        # MISSING") alike, since the map's own status column carries no separate enum value
        # for "partially works" and the leading word is the signal a reader acts on. A cell
        # that starts with WORKS but carries more text after it is QUALIFIED -- counted toward
        # the same total, but ALSO reported as a separate count, never folded silently into a
        # bare "N/M WORKS" that would read as N unqualified passes.
        works = [s for s in statuses if s.startswith("WORKS")]
        qualified = sum(1 for s in works if s != "WORKS")
    except Exception as exc:                          # noqa: BLE001
        return _degraded("Capabilities", f"{locator} (`{doc.name}`)", "SLOW", exc)
    if not total:
        value = f"0 rows parsed — `{doc.name}`"
    elif col is None:
        value = f"0/{total} WORKS (no 'status' column found) — `{doc.name}`"
    else:
        qual_note = f" ({qualified} qualified)" if qualified else ""
        value = f"{len(works)}/{total} WORKS{qual_note} — `{doc.name}`"
    return StateRow("Capabilities", value, "SLOW", locator)


# --- the aggregate, in paste order --------------------------------------------------------

#: The seven rows, in the order they render. A test pins this against
#: `verify_handoff_probes.BOOT_DATA_RULES` (equal both ways, the `seat_state.py`-style
#: coupling test).
STATE_ROW_KEYS: tuple[str, ...] = (
    "CI", "Batches", "Seats", "Substrates", "Transport", "Rulings", "Capabilities",
)


def state_rows(repo_root: "Path | str", transport: "Path | None") -> list[StateRow]:
    """All seven rows, in `STATE_ROW_KEYS` order. Called ONCE per cut
    (`gen_handoff.generate`) so a live poll (CI) is not repeated; the verifier instead calls
    each `row_*` function individually, once per probe, at check time."""
    repo_root = Path(repo_root)
    return [
        row_ci(repo_root),
        row_batches(repo_root),
        row_seats(),
        row_substrates(repo_root),
        row_transport(repo_root),
        row_rulings(transport),
        row_capabilities(transport),
    ]


# --- Done-when 6: the operator's nine-item roster, and how much of it is now live -------------
#
# See the module docstring's "THE NINE-ITEM ROSTER" section for why this is THIS lane's own
# roster (built from the ADR Context paragraph) rather than a claimed reproduction of
# SESSION-decision-handoff-system-2026-09-26.md §1.2, which this lane never read.

#: `(item, covering row key or None, why)`. A `None` row is a NAMED gap, not an omission.
OPERATOR_ROSTER: tuple[tuple[str, "str | None", str], ...] = (
    ("state (main sha)", "CI", "the CI row states origin/main's sha alongside its verdict"),
    ("rulings", "Rulings", "the newest RATIFICATION file, parsed for rulings in force"),
    ("pending decisions", None,
     "no reader in this lane's Owns list resolves ADR/intake triage state"),
    ("plan (active batch)", "Batches", "committed manifests declaring an open batch, live"),
    ("capability map", "Capabilities", "the newest DIGEST-CAPABILITY-MAP, WORKS-count parsed"),
    ("substrates", "Substrates", "ecosystem/substrate-registry.yaml, live: true entries"),
    ("transport", "Transport", "ecosystem/transport-registry.yaml, kinds registered"),
    ("working rules", None,
     "STANDING_RULINGS.md is a pointer row already (gen_handoff.boot_data_rows); not re-derived"),
    ("CI", "CI", "ci_verdict.verdict_for(\"origin/main\"), one non-blocking poll"),
)

#: The 2026-09-24 bundle's own measured baseline (ADR Context: "1 item fully (P13) and 1
#: partly (P8b) of 9"). A float, not two ints, because "partly" has no finer accounting here
#: than the ADR itself gives it.
BASELINE_2026_09_24 = 1.5


def coverage_line(repo_root: "Path | str", transport: "Path | None") -> str:
    """Done-when 6: how many of `OPERATOR_ROSTER`'s nine items now carry a live
    re-derivation, against the 2026-09-24 baseline. Does not itself re-run every row's live
    read beyond what building `state_rows` already does -- an item counts as covered when its
    mapped row is not `None`, independent of whether that row's OWN call degraded (a
    degraded-but-present row is still "carried with a live check": the check ran, and its
    answer is that the source could not be reached right now, which is what the row states)."""
    covered = [item for item, row_key, _why in OPERATOR_ROSTER if row_key is not None]
    total = len(OPERATOR_ROSTER)
    gaps = [item for item, row_key, _why in OPERATOR_ROSTER if row_key is None]
    return (f"COVERAGE: {len(covered)}/{total} operator items carry a live re-derivation "
            f"(baseline {BASELINE_2026_09_24:g}/9 in the 2026-09-24 bundle); gaps: "
            f"{', '.join(gaps) if gaps else 'none'}")


# ============================================================================================ CLI

def _main(argv: "list[str] | None" = None) -> int:
    """Print every state row plus the Done-when-6 coverage line. Evidence-printing only; this
    module owns no CLI subcommands and is never wired as a gate."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--transport", default=None,
                        help="the operator's transport dir; default $CLAUDE_PROMPTS_DIR")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    transport = Path(args.transport) if args.transport else None
    if transport is None:
        import os
        declared = (os.environ.get("CLAUDE_PROMPTS_DIR") or "").strip().strip('"')
        if declared and Path(declared).is_dir():
            transport = Path(declared)
    for row in state_rows(repo_root, transport):
        print(f"{row.key}: {row.rendered()}")
    print(coverage_line(repo_root, transport))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
