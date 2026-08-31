#!/usr/bin/env python
"""gen_trend_dashboard.py -- DB-1: the analyst-grade TREND surface, successor to the
conformance HTML dashboard.

    ONE COMMAND:  uv run --locked python scripts/gen_trend_dashboard.py --write
    OUTPUT:       ecosystem/trends.html   (regenerated on demand; NOT committed)

WHAT THIS REPLACES, AND WHY IT IS NOT THE SAME SHAPE. `ecosystem/conformance.md` and its
`.html` twin render the CURRENT value of every audit check as a colour-coded table. Three
properties of that shape are the defect:

  * a table shows VALUES, and a value cannot tell you whether the repo is getting better;
  * it is a committed generated artifact, so it goes stale between regenerations -- the
    live audit store said so while this module was being written
    (`generated_artifact_freshness`: "conformance-dashboard: 5d stale");
  * colour encodes pass/warn/fail, which is a status, not a trend.

This surface answers the other question: for each series, WHICH WAY IS IT GOING. Every
panel carries a direction verdict computed over the whole window, drawn as a glyph and
written as a word. That is the operator's first acceptance test, so it is the first thing
the layout spends space on.

INPUT IS THE STORE -- and the store is git. Nothing here computes a metric from scratch,
scrapes a doc, or accepts a hand-entered number. Every point is read back out of something
the repo already records:

  series                store                                              reach
  ------                -----                                              -----
  open rows             `status:` frontmatter in `tasks/*.md`, per rev      2026-07-27 ->
  banked ledger         same, `status: closed`                             2026-07-27 ->
  backlog velocity      banked delta vs `--diff-filter=A` births           2026-07-27 ->
  paste / boot bytes    `protocols/HANDOFF_BOOT.md` blob size, per rev     32 revisions
  doc-rot findings      `ecosystem/<repo>/history/*.md` dated snapshots     SPARSE
  funnel orphans        `ecosystem/audit-funnel-baseline.json` `uncovered`  2 revisions
  commit-gate ms        `logs/TELEMETRY.db` events.duration_ms              ABSENT
  suite wall-time       -- no store exists --                               ABSENT
  per-model quality     -- no store exists --                               ABSENT

The three ABSENT rows are rendered as absences with their reason, named in the legend.
That is deliberate and it is the point: a chart of invented history is worse than no chart,
and the two "no store exists" rows are findings this surface exists to make visible rather
than gaps it should quietly paper over.

NO SECOND STORE (batch clause A1). This module WRITES NOTHING but its own HTML. It is a
derived view over append-only records -- git history, and `logs/TELEMETRY.db` when that
store has rows. It does not emit telemetry, does not cache, and does not maintain a series
file of its own.

LIBRARY-FIRST, MEASURED (see the lane packet for the full comparison). Inline SVG on the
stdlib wins on measured fit: it is the only candidate that costs no ADR-106 dependency act,
emits a diffable text artifact, renders an ABSENT panel as a first-class state, and stays
inside the ASCII output the next paragraph requires. matplotlib and plotly were rejected on
the dependency gate plus a binary output; mermaid `xychart-beta` was rejected because it
cannot express an absent series or a per-panel predicate label.

ASCII-ONLY OUTPUT, structurally. `gen_dashboard`-class generators in this repo emit silent
mojibake and exit 0 when `PYTHONUTF8` is unset. Rather than document that hazard, this
module removes its own exposure: direction glyphs are DRAWN as SVG polygons instead of
typed as arrow characters, so the page contains no non-ASCII byte to launder.
`tests/test_trend_dashboard.py::test_output_is_pure_ascii` holds that closed, and `--write`
verifies the bytes it just wrote rather than trusting its own exit code.

READ-ONLY (ADR-28/36 Layer 2). Reads git and the working tree; the only disk write is the
declared `--write` output.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sqlite3
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_RELPATH = "ecosystem/trends.html"

#: The five-value `tasks/` status enum, measured by C6 (2026-08-19) and re-measured here.
#: `deferred` / `retired` / `superseded` are NONE OF open and NONE OF closed. Folding
#: `retired` into `closed` would let the ledger go net-negative by relabelling, which is
#: the gaming the ledger row was filed against -- so all five are counted separately and
#: only `closed` is ever called "banked".
STATUS_ENUM: tuple[str, ...] = ("open", "closed", "deferred", "retired", "superseded")

_STATUS_RE = re.compile(r"^status:\s*(\S+)\s*$", re.M)
_DOC_ROT_ROW_RE = re.compile(r"^\|\s*doc_rot\s*\|", re.M)
_DOC_ROT_FINDING_RE = re.compile(r"^\|\s*doc_rot\s*\|\s*(warn|fail)\s*\|", re.M)

# Loaded BY PATH for the shallow-clone probe. `telemetry_emit` already owns that predicate
# (`is_shallow_repository`, returning bool | None -- the third state being "could not
# tell"); C6 section 2.6 made refusing a truncated git-derived series a page-wide rule and
# named reuse, not reimplementation, as the way to get it.
_te_spec = importlib.util.spec_from_file_location(
    "dev_knowledge_telemetry_emit", Path(__file__).resolve().with_name("telemetry_emit.py"))
_telemetry = importlib.util.module_from_spec(_te_spec)
_te_spec.loader.exec_module(_telemetry)

# The [#355] git-env scrub, also loaded BY PATH for the reason gitenv.py's own docstring
# gives: `import gitenv` and `from scripts import gitenv` each have a shadow hole that
# silently empties the scrub. Without it an inherited GIT_DIR would answer every question
# on this page about a DIFFERENT repository while the page labelled it as this one.
_ge_spec = importlib.util.spec_from_file_location(
    "dev_knowledge_gitenv_trend", Path(__file__).resolve().with_name("gitenv.py"))
_gitenv = importlib.util.module_from_spec(_ge_spec)
_ge_spec.loader.exec_module(_gitenv)

# HY-4: the north-star ARC declarations, loaded BY PATH for the same reason as the two
# modules above -- and so the burn-down panel READS the arc set rather than restating it
# (done-contract item 1). `gen_north_star.py` is a sibling script, never a package import.
_ns_spec = importlib.util.spec_from_file_location(
    "dev_knowledge_north_star_trend", Path(__file__).resolve().with_name("gen_north_star.py"))
_north_star = importlib.util.module_from_spec(_ns_spec)
_ns_spec.loader.exec_module(_north_star)


# ---------------------------------------------------------------------------
# The series record
# ---------------------------------------------------------------------------

@dataclass
class Series:
    """One panel.

    `state` is the load-bearing field and has three values, because "no data" is three
    different facts and collapsing them is how a gap becomes invisible:

      ok            -- 3+ points; a direction may be claimed
      insufficient  -- 1-2 points; the store exists but cannot support a trend
      absent        -- 0 points; named in the legend with `basis` carrying the reason

    `better` says which way is improvement, and every direction verdict is relative to it.
    Without it a falling line is ambiguous: falling open-rows is good, falling banked
    closures is bad, and the same polyline would otherwise get the same headline.
    """
    key: str
    label: str
    predicate: str
    points: list[tuple[date, float]]
    basis: str
    better: str  # "up" | "down"
    state: str = "ok"
    unit: str = ""
    note: str = ""
    extra: dict = field(default_factory=dict)


@dataclass
class ArcBurndown:
    """HY-4: one north-star arc's done-vs-remaining panel, over time.

    Two lines sharing one x-axis and one scale: `done` (status: closed among the arc's
    theme-selected rows) and `remaining` (status: open). `themes` and `name` are carried
    from `gen_north_star.ARCS` rather than retyped, so a new arc appears here without
    editing this module (done-contract item 1). `state` follows the same three-value
    discipline as `Series` -- see its docstring.
    """
    key: str
    name: str
    themes: tuple[str, ...]
    done: list[tuple[date, float]]
    remaining: list[tuple[date, float]]
    basis: str
    state: str = "ok"


@dataclass
class QuotaRow:
    """HY-4 / CUT-5: one provider's quota-visibility row.

    `provider` and `display_name` are DERIVED from `ecosystem/provider-registry.yaml` at
    call time (done-contract item 4) -- a provider added or removed there appears or
    vanishes here without editing this module. `credits_state` is "absent" for every row
    today: no store anywhere in this repo can compute a numeric credit balance for any
    provider (verified against the registry's own schema, which forbids an undeclared key,
    and against `docs/audits/2026-08-31-technical-agy-admission-and-quota-visibility.md`,
    which found no programmatic quota surface for any configured provider). Rendering a
    plausible number here would be exactly the "partial series that looks complete" `[#615]`
    warns against, applied to this panel itself (done-contract item 3).
    """
    provider: str
    display_name: str
    cli: str | None
    credits_state: str
    credits_basis: str


# ---------------------------------------------------------------------------
# Pure derivations
# ---------------------------------------------------------------------------

def classify_state(points: list) -> str:
    """0 points is absent, 1-2 is insufficient, 3+ can carry a trend.

    The 3-point floor is a judgment and it is deliberately conservative: two samples are a
    line through two dots, and a line through two dots always has a slope, so a 2-point
    "trend" is guaranteed to produce a confident-looking arrow from no evidence.
    """
    if not points:
        return "absent"
    return "insufficient" if len(points) < 3 else "ok"


def direction(points: list[tuple[date, float]], better: str) -> tuple[str, float]:
    """(verdict, delta) over the WHOLE window -- first sample to last.

    Reading the window rather than the final step is the whole design. Keying off the last
    step lets one noisy sample flip the headline, and a headline that flips on noise is
    exactly how a trend surface starts lying to the person who trusts it at a glance.
    """
    if len(points) < 2:
        return ("unknown", 0.0)
    delta = points[-1][1] - points[0][1]
    if delta == 0:
        return ("flat", 0.0)
    rising = delta > 0
    improving = rising if better == "up" else not rising
    return ("improving" if improving else "worsening", delta)


def parse_band_counts(git_grep_output: str) -> dict[str, int]:
    """Count each of the five `status:` values in one `git grep -h '^status:'` payload.

    An unrecognised value is dropped rather than counted into a catch-all: a new status
    would otherwise silently inflate whichever band it landed in, and a wrong band is
    worse than a missing one on a surface whose only job is direction.
    """
    counts = dict.fromkeys(STATUS_ENUM, 0)
    for value in _STATUS_RE.findall(git_grep_output):
        if value in counts:
            counts[value] += 1
    return counts


def arc_counts(frontmatter: dict[str, dict], themes: tuple[str, ...]) -> tuple[int, int]:
    """(done, remaining) among rows whose `theme` is one of `themes`.

    done == status: closed; remaining == status: open. A row that is `deferred`,
    `retired` or `superseded` belongs to NEITHER band, mirroring `banked_ledger`'s own
    rule (C6, 2026-08-19): folding a not-yet-finished row into either count would misstate
    progress toward the arc the same way folding `retired` into `closed` misstates the
    ledger.
    """
    done = remaining = 0
    for row in frontmatter.values():
        if row.get("theme") not in themes:
            continue
        status = row.get("status")
        if status == "closed":
            done += 1
        elif status == "open":
            remaining += 1
    return done, remaining


def parse_doc_rot_count(snapshot_md: str) -> int | None:
    """doc_rot findings in one dated `ecosystem/<repo>/history/*.md` snapshot.

    Returns `None` when the snapshot does not mention `doc_rot` AT ALL, which means the
    check did not exist when that snapshot was taken -- these snapshots record passing
    checks as well as findings, so a check that ran clean still appears as a `pass` row.

    THIS DISTINCTION IS THE WHOLE FUNCTION, and it was found by reading the generator's own
    first real output rather than by reasoning: `doc_rot` is registered check #24 and does
    not appear in any snapshot before 2026-07-31. Counting those as clean zeros produced a
    fifteen-sample flat line and a confident "WORSENING +2" headline describing nothing but
    the check coming into existence. That is exactly the invented history the surface is
    supposed to refuse, so absence of the check is `None` (not a point) and only a snapshot
    that actually ran it can contribute a value -- including a genuine 0.
    """
    if not _DOC_ROT_ROW_RE.search(snapshot_md):
        return None
    return len(_DOC_ROT_FINDING_RE.findall(snapshot_md))


def velocity(banked: list[tuple[date, float]],
             births_by_date: dict[date, int]) -> list[dict]:
    """Per-window NET banked change vs births -- the "closures fund births" pair.

    MATCHED BY DATE, NEVER BY INDEX. `collect_bands` drops sample dates from before
    `tasks/` existed, so its list is SHORTER than the sample vector; pairing the two
    positionally shifted every birth count by the number of dropped samples and silently
    overstated net velocity. (Terra pre-merge, H1 -- the witness was a "42 closed against
    0 filed" window that had no business reading zero.) A window whose birth count cannot
    be resolved is skipped rather than defaulted to 0.

    HONEST LIMIT ON "CLOSURES" (terra H2). The first value is the DELTA OF THE BANKED
    BAND, which is a NET change, not a count of closure transitions. No task file has ever
    been deleted (C6 measured `git log --diff-filter=D -- tasks/*.md` = 0), so the band
    moves only on real frontmatter transitions -- but a row moving BACK out of `closed`
    inside the same window offsets one that moved in, and the delta cannot see that. It is
    therefore labelled "net banked" everywhere it is rendered, and a true transition count
    would need a per-revision frontmatter walk this surface deliberately does not run.
    """
    out = []
    for i in range(1, len(banked)):
        window_end = banked[i][0]
        if window_end not in births_by_date:
            continue
        net_banked = banked[i][1] - banked[i - 1][1]
        births = births_by_date[window_end]
        out.append({"date": window_end, "closures": net_banked, "births": births,
                    "net": net_banked - births})
    return out


#: A backlog row lives at the TOP LEVEL of `tasks/`. `tasks/archive/` holds relocated
#: records of rows that already existed.
_TASK_ROW_RE = re.compile(r"^tasks/[^/]+\.md$")


def is_task_row_path(path: str) -> bool:
    """True only for a top-level `tasks/<name>.md` -- never an archived record.

    A birth is a row coming into EXISTENCE. `tasks/archive/` holds relocated records of
    rows that were already born, so counting an archival as a birth double-counts it and
    understates velocity by the size of the archival (terra third pass, N2). Measured on
    the live tree: the 2026-08-22..29 window counted 57 additions, of which 21 were
    archive files -- on the one metric whose headline this lane had already seen flip.
    """
    return bool(_TASK_ROW_RE.match(path))


def latest_snapshot(snapshot_md: str) -> str:
    """The LAST `### ...` snapshot in a dated history file, or the whole text if unmarked.

    A dated history file can hold SEVERAL audit runs -- `2026-05-16.md` holds twelve.
    Counting findings across all of them produces an aggregate no single audit run ever
    recorded (terra pre-merge, H6). The day's final run is chosen as the day's value, and
    that choice is stated rather than left implicit.
    """
    parts = re.split(r"(?m)^### ", snapshot_md)
    return parts[-1] if len(parts) > 1 else snapshot_md


def shallow_basis(is_shallow: bool | None) -> str | None:
    """The C6 refusal string, or None when the history is trustworthy.

    `None` from the probe means "could not tell", and that is NOT a pass: a series
    rendered from a history we could not confirm is the same risk as one rendered from a
    history we know is truncated.
    """
    if is_shallow is False:
        return None
    if is_shallow is None:
        return ("unavailable -- could not determine whether this clone is shallow; a "
                "git-derived series is not rendered from unverified history")
    return ("unavailable -- shallow clone; a truncated series would read as the whole "
            "history and is refused rather than drawn short")


def scale_bounds(points: list[tuple[date, float]], ceiling: float | None = None):
    """(lo, hi) for the vertical axis, widened to include a budget ceiling if there is one.

    A budget line must sit on the SAME scale as the polyline it is judging, so the ceiling
    joins the range rather than being positioned separately. Without this the dashed line
    lands at an arbitrary height and the panel silently misreports headroom -- which is
    the one thing a budget panel exists to show.
    """
    values = [v for _, v in points]
    lo, hi = min(values), max(values)
    if ceiling is not None:
        lo, hi = min(lo, ceiling), max(hi, ceiling)
    return lo, hi


def scale_y(value: float, lo: float, hi: float, h: float) -> float:
    """Map a value onto the box, y inverted so HIGHER renders UPWARD."""
    frac = 0.5 if hi == lo else (value - lo) / (hi - lo)
    return h - (frac * h)


def sparkline_points(points: list[tuple[date, float]], w: float, h: float,
                     ceiling: float | None = None) -> str:
    """SVG `points` for a polyline, y inverted so a RISING series renders UPWARD.

    A flat series maps to the vertical middle rather than dividing by a zero range.
    """
    if not points:
        return ""
    lo, hi = scale_bounds(points, ceiling)
    n = len(points)
    coords = []
    for i, (_, v) in enumerate(points):
        x = 0.0 if n == 1 else (w * i / (n - 1))
        coords.append(f"{x:.2f},{scale_y(v, lo, hi, h):.2f}")
    return " ".join(coords)


# ---------------------------------------------------------------------------
# Git-backed collectors
# ---------------------------------------------------------------------------

def _git_checked(*args: str, root: Path | None = None) -> str | None:
    """stdout on success, None on ANY non-zero exit.

    The distinction matters more here than in most places (terra second pass, N1). A
    collector that treats a FAILED git call as "" cannot tell "nothing was filed" from
    "the command did not run", and both then render as a confident zero -- the missing-
    versus-zero contract this whole surface is built on, broken at its own root. Callers
    that genuinely do not care (a display SHA) use `_git`; callers that turn output into a
    DATA POINT must use this one and skip the sample when it returns None.

    THE ENVIRONMENT IS SCRUBBED (terra fourth pass). An inherited `GIT_DIR` overrides both
    `cwd` and `-C`, so a shell carrying one would have made every collector read ANOTHER
    repository and label the result as this one's -- plausible numbers, wrong repo, and
    the shallow probe would not catch it because `telemetry_emit` scrubs its own
    environment and would answer about the right tree while these calls answered about the
    wrong one. `scripts/gitenv.py` already owns that scrub and is reused, not
    reimplemented, exactly as the shallow probe is.
    """
    p = subprocess.run(["git", "-C", str(root or _REPO_ROOT), *args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=_gitenv.scrubbed_git_env())
    return p.stdout if p.returncode == 0 else None


def _git(*args: str, root: Path | None = None) -> str:
    """stdout, or "" on failure. Display-only -- never use this to build a data point."""
    return _git_checked(*args, root=root) or ""


def sample_dates(end: date, weeks: int) -> list[date]:
    """Weekly sample dates, oldest first, ending at `end`, spanning `weeks` FULL weeks.

    N SAMPLES ARE N-1 INTERVALS, so a `weeks`-week window needs `weeks + 1` samples (terra
    fourth pass). The earlier form returned exactly `weeks` dates, which made `--weeks 12`
    advertise twelve weeks while reading 77 days, and made `--weeks 1` produce a single
    sample spanning no interval at all -- a window label that did not describe the data
    under it, on a page whose entire claim is that its numbers come from a named store.

    `weeks` must be >= 1: a zero or negative window yields a degenerate date list that
    every caller then indexes for its window bound, so the CLI accepted an input that
    crashed with an IndexError instead of refusing (terra third pass).
    """
    if weeks < 1:
        raise ValueError(f"weeks must be >= 1, got {weeks}")
    return [end - timedelta(days=7 * i) for i in range(weeks, -1, -1)]


def _rev_at(d: date, root: Path | None = None) -> str:
    """The MAINLINE state at end of day `d`, or "" when history does not reach that far.

    `--first-parent`, and the reason is this repo's own core invariant: every change lands
    by `--no-ff` merge, so the first-parent spine IS the history of `main` and anything off
    it is work-in-progress inside a lane. Without the flag, `rev-list -1 --before` can
    return an unmerged lane commit that happens to carry the newest timestamp, and the
    page would then report a lane's private state as the repo's (terra fifth pass).

    MEASURED, not assumed: at the four sample dates in the current 12-week window where
    the two predicates disagree, every series is identical (closed 52/52, open 161/161 at
    2026-08-08; closed 90/90, open 185/185 at 2026-08-22; boot bytes 16493/16493). So this
    fixes nothing visible today -- it makes the sampler correct by construction rather
    than correct by luck, which is the difference that matters the first time a lane is
    open across a sample boundary.
    """
    out = _git("rev-list", "--first-parent", "-1",
               f"--before={d.isoformat()} 23:59:59", "HEAD", root=root)
    return out.strip()


def collect_bands(dates: list[date], root: Path | None = None) -> list[tuple[date, dict]]:
    """The five-band composition at each sample date -- ONE `git grep` per sample."""
    out = []
    for d in dates:
        rev = _rev_at(d, root)
        if not rev:
            continue
        payload = _git("grep", "-h", "^status:", rev, "--", "tasks/*.md", root=root)
        if not payload.strip():
            continue  # pre-flip: tasks/ did not exist yet. Not a zero.
        out.append((d, parse_band_counts(payload)))
    return out


_FRONTMATTER_FIELD_RE = re.compile(r"^(status|theme):\s*(.+?)\s*$")


def collect_task_frontmatter(rev: str, root: Path | None = None) -> dict[str, dict] | None:
    """{path: {"status": ..., "theme": ...}} for every top-level `tasks/*.md` at REV.

    ONE `git grep` call, not one per file -- the same shape discipline `collect_bands`
    already holds. The `tasks/*.md` pathspec does not recurse (git wildmatch: `*` never
    crosses `/`), so `tasks/archive/*.md` is excluded structurally, exactly as it already
    is for the status-only collector -- measured: `git grep -- tasks/*.md` returns zero
    `tasks/archive/` hits on the live tree.

    Returns `None` on a FAILED git call (an unresolvable revision), never `{}` -- the same
    missing-versus-empty contract every collector in this module holds (terra second pass,
    N1). An empty-but-successful result (payload "") means `tasks/` did not exist yet at
    this revision, and the caller treats that as a pre-flip sample to skip, not a zero.

    Theme values are double-quoted YAML strings on disk (`theme: "[E7] ..."`); the quoting
    is stripped so a returned value compares equal to an `ARCS[i]["themes"]` entry without
    the caller having to know the on-disk quoting convention.
    """
    payload = _git_checked("grep", "-n", "-e", "^status:", "-e", "^theme:", rev,
                           "--", "tasks/*.md", root=root)
    if payload is None:
        return None
    out: dict[str, dict] = {}
    for line in payload.splitlines():
        parts = line.split(":", 3)
        if len(parts) != 4:
            continue
        _rev, path, _lineno, content = parts
        m = _FRONTMATTER_FIELD_RE.match(content)
        if not m:
            continue
        key, value = m.groups()
        out.setdefault(path, {})[key] = value.strip("\"'")
    return out


def collect_births(dates: list[date], root: Path | None = None) -> dict[date, int]:
    """New `tasks/*.md` files added in each window, KEYED BY THE WINDOW'S END DATE.

    A dict, not a list, so `velocity` can match by date. A window whose endpoints do not
    both resolve is OMITTED rather than recorded as 0 -- "could not measure" and "nothing
    was filed" are different facts, and only the second is a zero.
    """
    births: dict[date, int] = {}
    for prev, cur in zip(dates, dates[1:]):
        a, b = _rev_at(prev, root), _rev_at(cur, root)
        if not a or not b:
            continue
        added = _git_checked("diff", "--diff-filter=A", "--name-only", a, b,
                             "--", "tasks/", root=root)
        if added is None:
            continue  # the diff FAILED -- not a window in which nothing was filed
        births[cur] = len([ln for ln in added.splitlines() if is_task_row_path(ln.strip())])
    return births


def collect_blob_bytes(dates: list[date], path: str, root: Path | None = None):
    """Byte size of one tracked file at each sample rev -- the paste/boot-budget series."""
    out = []
    for d in dates:
        rev = _rev_at(d, root)
        if not rev:
            continue
        size = _git("cat-file", "-s", f"{rev}:{path}", root=root).strip()
        if size.isdigit():
            out.append((d, float(size)))
    return out


_FUNNEL_PATH = "ecosystem/audit-funnel-baseline.json"


def collect_funnel(since: date | None = None, root: Path | None = None):
    """`uncovered` at every REVISION of the committed funnel baseline, oldest first.

    REVISIONS, NOT WEEKLY SAMPLES (terra second pass, N4). The baseline is regenerated
    rarely and irregularly -- two of its revisions land inside a single week -- so a
    weekly sampler silently dropped one and then rendered "1 sample" beside a panel whose
    predicate says "per rev". Walking `git log` on the file itself is both cheaper and
    the thing the label actually claims.
    """
    log = _git_checked("log", "--format=%H %cs", "--follow", "--", _FUNNEL_PATH, root=root)
    if log is None:
        return []
    out: list[tuple[date, float]] = []
    for line in reversed(log.splitlines()):  # git log is newest-first
        parts = line.split()
        if len(parts) != 2:
            continue
        sha, stamp = parts
        try:
            d = date.fromisoformat(stamp)
        except ValueError:
            continue
        if since and d < since:
            continue
        blob = _git_checked("cat-file", "-p", f"{sha}:{_FUNNEL_PATH}", root=root)
        if not blob:
            continue
        try:
            value = float(json.loads(blob)["uncovered"])
        except (ValueError, KeyError, TypeError):
            continue
        # Collapse a revision that did not move the number: the file is regenerated for
        # other reasons too, and an unchanged value is not a fresh observation.
        if out and out[-1][1] == value:
            continue
        out.append((d, value))
    return out


def collect_doc_rot(root: Path | None = None, since: date | None = None):
    """doc_rot findings per dated snapshot under `ecosystem/*/history/`, hub repo only.

    `since` bounds the series to the page's declared window. Without it the page could
    advertise "12w" and plot a point from outside it, making panel directions
    incomparable (terra pre-merge, H5).
    """
    base = (root or _REPO_ROOT) / "ecosystem" / ".dev-knowledge" / "history"
    if not base.is_dir():
        return []
    out = []
    for f in sorted(base.glob("????-??-??.md")):
        try:
            d = date.fromisoformat(f.stem)
        except ValueError:
            continue
        if since and d < since:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if "| Check |" not in text:
            continue
        count = parse_doc_rot_count(latest_snapshot(text))
        if count is None:
            continue  # the check did not exist at this snapshot -- not a zero
        out.append((d, float(count)))
    return out


def collect_commit_gate(db_path: Path | None = None, since: date | None = None):
    """(points, reason) -- mean gate wall-time per day from the telemetry store.

    THE QUANTITY IS PER-RUN, NOT PER-HOOK (terra pre-merge, H3). Gate wall-time is what
    one invocation of the gate mesh COSTS, so events are summed within a `run_id` -- the
    `[#565]` correlation id that ties a gate invocation's process tree together -- and
    only then averaged across the runs of a day. Averaging individual hook durations
    instead answers "how long is the average hook", which moves whenever the NUMBER of
    hooks changes and is not the labelled quantity.

    `hook_run` ONLY, AND THIS IS THE LOAD-BEARING PART (terra second pass, N2). An earlier
    revision summed `check_run` alongside it, which DOUBLE-COUNTS: `check_run` is emitted
    per audit check from inside `scripts/audit.py`, and `audit.py` runs as the
    `audit-health` hook, which emits its own enclosing `hook_run`. The two populations are
    nested, so adding them charges the same milliseconds twice.

    WHAT A run_id GROUP ACTUALLY IS, and why the label had to change (terra third pass).
    `telemetry_emit.current_run_id` states its own honest limit: the id is exported to a
    process's DESCENDANTS, not its SIBLINGS, and `pre-commit` spawns each hook as its own
    child -- so "one `git commit` yields one run_id per emitting hook, not one for the
    commit", and "a reader grouping by run_id is grouping RUNNER INVOCATIONS". Calling
    that "commit-gate wall-time" would have been this page asserting a number its own
    store cannot support, which is the single failure it exists to refuse. The panel is
    therefore labelled **gate time per runner invocation**. It becomes a true per-commit
    figure only when something sets `DEV_KNOWLEDGE_TELEMETRY_RUN_ID` before `pre-commit`
    starts -- the seam step 1 of that resolution order deliberately leaves open, and which
    nothing in this repo currently uses. That gap is reported as a candidate filing, not
    closed here.

    FOUR OUTCOMES, NOT ONE (terra pre-merge, H4). "no file", "file with no matching rows"
    and "unreadable store" are different operational facts, and collapsing them made a
    corrupt store render as the reassuring sentence "telemetry was never enabled". The
    reason string is returned so the panel can say which one actually happened.
    """
    path = Path(db_path or _telemetry.default_db_path())
    if not path.exists():
        # Observable fact only (terra second pass, N5): file absence proves that no store
        # is available HERE AND NOW. It does not prove telemetry was never enabled -- a
        # store can be deleted, relocated by DEV_KNOWLEDGE_TELEMETRY_DB, or simply live in
        # a different checkout. Claiming the stronger fact would be this page committing
        # the exact sin it refuses elsewhere.
        return [], ("NO STORE AVAILABLE -- logs/TELEMETRY.db is not present in this"
                    " checkout, so there is nothing to read. The store is wired"
                    " (scripts/telemetry_emit.py), emission is opt-in"
                    " (DEV_KNOWLEDGE_TELEMETRY=1), and the path is relocatable"
                    " (DEV_KNOWLEDGE_TELEMETRY_DB). That is the whole observable fact:"
                    " it says nothing about what the gates cost, and nothing about"
                    " whether telemetry has ever run.")
    try:
        con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        try:
            rows = con.execute(
                "SELECT day, AVG(run_ms) FROM ("
                "  SELECT substr(ts,1,10) AS day, run_id, SUM(duration_ms) AS run_ms"
                "  FROM events"
                "  WHERE event_type = 'hook_run'"
                "    AND duration_ms IS NOT NULL AND run_id <> ''"
                "  GROUP BY day, run_id"
                ") GROUP BY day ORDER BY day").fetchall()
        finally:
            con.close()
    except sqlite3.Error as exc:
        return [], (f"STORE UNREADABLE -- logs/TELEMETRY.db exists but could not be"
                    f" queried ({type(exc).__name__}). This is an operational failure,"
                    f" NOT an absence of telemetry, and it is reported as such rather"
                    f" than rendered as an empty series.")
    out = []
    for day, avg in rows:
        try:
            d = date.fromisoformat(day)
        except (ValueError, TypeError):
            continue
        if since and d < since:
            continue
        out.append((d, float(avg)))
    if not out:
        return [], ("NO CORRELATED RUNS -- logs/TELEMETRY.db exists but carries no"
                    " run_id-correlated hook_run/check_run rows in this window. Rows"
                    " emitted before the [#565] correlation column carry an empty run_id"
                    " and are deliberately not averaged together as if they were one run.")
    return out, None


# ---------------------------------------------------------------------------
# Series assembly
# ---------------------------------------------------------------------------

_ABSENT_MODEL_QUALITY = (
    "NO STORE -- nothing in the tree records which model authored a commit, so change "
    "quality cannot be grouped by model. Enabling row reported as a candidate filing "
    "(MODEL ATTRIBUTION: a hook-enforced model+version trailer the store consumes). "
    "Deliberately NOT proxied by token share or any other stand-in.")

_ABSENT_SUITE_TIME = (
    "NO STORE -- suite wall-time appears only in prose audit artifacts; no script, log or "
    "committed surface records it as a value, so there is nothing to read back.")


def build_series(weeks: int = 12, today: date | None = None, root: Path | None = None,
                 db_path: Path | None = None) -> list[Series]:
    """Every panel, assembled from the stores. No metric is computed that a store does not
    already carry, and no absence is filled in."""
    today = today or date.today()
    dates = sample_dates(today, weeks)
    refusal = shallow_basis(_telemetry.is_shallow_repository(str(root or _REPO_ROOT)))

    if refusal:
        # C6 section 2.6: every git-derived panel refuses together rather than each one
        # drawing its own plausible short line.
        git_series = [
            ("open_rows", "open backlog rows", "down"),
            ("banked_ledger", "banked ledger (status: closed)", "up"),
            ("velocity", "backlog velocity (closures - births)", "up"),
            ("paste_bytes", "paste / boot bytes", "down"),
            ("funnel_orphans", "funnel orphans (undispositioned)", "down"),
        ]
        out = [Series(key=k, label=lab, predicate="git-derived", points=[], basis=refusal,
                      better=b, state="absent") for k, lab, b in git_series]
    else:
        bands = collect_bands(dates, root)
        births = collect_births(dates, root)
        open_pts = [(d, float(b["open"])) for d, b in bands]
        banked_pts = [(d, float(b["closed"])) for d, b in bands]
        windows = velocity(banked_pts, births)
        net_pts = [(w["date"], float(w["net"])) for w in windows]

        composition = ""
        if bands:
            last = bands[-1][1]
            composition = (" latest composition: "
                           + ", ".join(f"{k} {last[k]}" for k in STATUS_ENUM) + ".")

        boot_pts = collect_blob_bytes(dates, "protocols/HANDOFF_BOOT.md", root)
        funnel_pts = collect_funnel(since=dates[0], root=root)

        out = [
            Series(
                key="open_rows", label="open backlog rows", better="down", unit="rows",
                predicate="count of `status: open` in tasks/*.md at each weekly rev",
                points=open_pts,
                basis=("tasks/*.md frontmatter, read at one rev per sample."
                       + composition
                       + " Read from tasks/, never from BACKLOG.md, which is a generated"
                         " one-line VIEW since [#589] and cannot answer a status question."),
                state=classify_state(open_pts)),
            Series(
                key="banked_ledger", label="banked ledger (status: closed)", better="up",
                unit="rows",
                predicate="count of `status: closed` in tasks/*.md at each weekly rev",
                points=banked_pts,
                basis=("Banked means `closed` ONLY. `retired` and `superseded` are counted"
                       " but never folded in: folding them would let the ledger rise by"
                       " relabelling rather than by finishing work." + composition),
                state=classify_state(banked_pts)),
            Series(
                key="velocity", label="backlog velocity (net banked - births)",
                better="up", unit="rows/week",
                predicate=("delta of the `status: closed` band minus tasks/*.md files"
                           " added, per window, matched by window end date"),
                points=net_pts,
                basis=("Closures fund births. The first term is the NET change in the"
                       " banked band, not a count of closure transitions: no task file"
                       " has ever been deleted, so the band moves only on real"
                       " frontmatter transitions, but a row moving back OUT of `closed`"
                       " inside a window offsets one that moved in and the delta cannot"
                       " see it. Births are `--diff-filter=A` on tasks/ over the same"
                       " window, matched by end date."
                       f" Latest window: net banked {windows[-1]['closures']:+.0f}"
                       f" against {windows[-1]['births']:.0f} filed." if windows else
                       "Closures fund births; no complete window yet."),
                state=classify_state(net_pts)),
            Series(
                key="paste_bytes", label="paste / boot bytes", better="down", unit="bytes",
                predicate="blob size of protocols/HANDOFF_BOOT.md at each weekly rev",
                points=boot_pts,
                basis=("Against the 18000-byte boot budget the `boot_byte_budget` audit"
                       " check enforces. Rising means the boot paste is eating its"
                       " headroom."),
                state=classify_state(boot_pts), extra={"budget": 18000.0}),
            Series(
                key="funnel_orphans", label="funnel orphans (undispositioned)",
                better="down", unit="artifacts",
                predicate="`uncovered` in ecosystem/audit-funnel-baseline.json, per rev",
                points=funnel_pts,
                basis=("The committed funnel baseline is the store, walked at every"
                       " REVISION of the file rather than sampled weekly -- it is"
                       " regenerated irregularly, and two revisions can land inside one"
                       " week, so a weekly sampler drops real measurements. A revision"
                       " that did not move the number is collapsed: the file is"
                       " regenerated for other reasons too, and an unchanged value is"
                       " not a fresh observation."),
                state=classify_state(funnel_pts)),
        ]

    # Every panel is bounded by the SAME declared window, or the page advertises "12w"
    # while plotting points from outside it (terra pre-merge, H5).
    window_start = dates[0]
    doc_rot_pts = collect_doc_rot(root, since=window_start)
    out.append(Series(
        key="doc_rot", label="doc-rot findings", better="down", unit="findings",
        predicate="rows matching `| doc_rot |` in ecosystem/.dev-knowledge/history/*.md",
        points=doc_rot_pts,
        basis=("Dated audit snapshots are the only TRACKED doc-rot store. The live value"
               " sits in ecosystem/*/state.yaml, which is gitignored and therefore carries"
               " no history. The snapshot writer has been dormant since 2026-07-31, which"
               " is why this series is short -- reported, not back-filled."),
        state=classify_state(doc_rot_pts)))

    gate_pts, gate_reason = collect_commit_gate(db_path, since=window_start)
    out.append(Series(
        key="commit_gate", label="gate time per runner invocation", better="down",
        unit="ms",
        predicate=("mean per-run SUM(duration_ms) per day, grouped by run_id, over"
                   " events WHERE event_type = 'hook_run'"),
        points=gate_pts,
        basis=(gate_reason or
               ("Store: logs/TELEMETRY.db via scripts/telemetry_emit.py, schema"
                " events(ts, event_type, name, outcome, duration_ms, context_json,"
                " run_id). `check_run` is excluded because it NESTS inside the"
                " audit-health hook_run and would be charged twice. Named a RUNNER"
                " INVOCATION, not a commit: telemetry_emit.current_run_id exports the id"
                " to descendants but not to siblings, and pre-commit spawns each hook as"
                " its own child, so one commit yields one run_id per emitting hook. A"
                " true per-commit figure needs DEV_KNOWLEDGE_TELEMETRY_RUN_ID set before"
                " pre-commit starts; nothing does that today.")),
        state=classify_state(gate_pts)))

    out.append(Series(
        key="suite_time", label="suite wall-time", better="down", unit="s",
        predicate="n/a -- no store", points=[], basis=_ABSENT_SUITE_TIME, state="absent"))
    out.append(Series(
        key="model_quality", label="per-model change quality", better="up", unit="",
        predicate="n/a -- no store", points=[], basis=_ABSENT_MODEL_QUALITY,
        state="absent"))
    return out


def demo_series() -> list[Series]:
    """A fixed, git-free series set. Used by the tests so the acceptance assertions pin the
    RENDERER rather than whatever the repo's history happens to look like today."""
    def pts(*vals):
        start = date(2026, 6, 1)
        return [(start + timedelta(days=7 * i), float(v)) for i, v in enumerate(vals)]

    return [
        Series(key="open_rows", label="open backlog rows", predicate="count of open rows",
               points=pts(190, 175, 160, 151), basis="tasks/ frontmatter", better="down",
               state="ok", unit="rows"),
        Series(key="banked_ledger", label="banked ledger", predicate="count of closed rows",
               points=pts(33, 80, 110, 132), basis="tasks/ frontmatter", better="up",
               state="ok", unit="rows"),
        Series(key="paste_bytes", label="paste / boot bytes", predicate="blob size",
               points=pts(15000, 16200, 17196), basis="boot budget 18000", better="down",
               state="ok", unit="bytes", extra={"budget": 18000.0}),
        Series(key="funnel_orphans", label="funnel orphans", predicate="uncovered",
               points=pts(720, 707), basis="2 samples", better="down",
               state="insufficient", unit="artifacts"),
        Series(key="suite_time", label="suite wall-time", predicate="n/a -- no store",
               points=[], basis=_ABSENT_SUITE_TIME, better="down", state="absent"),
        Series(key="model_quality", label="per-model change quality",
               predicate="n/a -- no store", points=[], basis=_ABSENT_MODEL_QUALITY,
               better="up", state="absent"),
    ]


# ---------------------------------------------------------------------------
# HY-4: the burn-down panel -- done vs remaining, per north-star arc, over time
# ---------------------------------------------------------------------------

def build_arc_burndowns(weeks: int = 12, today: date | None = None,
                        root: Path | None = None) -> list[ArcBurndown]:
    """One `ArcBurndown` per arc DECLARED in `scripts/gen_north_star.py::ARCS` -- read at
    call time, never restated, so the panel cannot drift from the arc set (done-contract
    item 1). Every point is `arc_counts` over `collect_task_frontmatter` at each weekly
    rev; no number is typed in.
    """
    today = today or date.today()
    dates = sample_dates(today, weeks)
    refusal = shallow_basis(_telemetry.is_shallow_repository(str(root or _REPO_ROOT)))
    arcs = _north_star.ARCS

    if refusal:
        # C6 section 2.6, applied here too: every git-derived panel refuses together.
        return [ArcBurndown(key=a["key"], name=a["name"], themes=a["themes"],
                            done=[], remaining=[], basis=refusal, state="absent")
                for a in arcs]

    per_arc_done: dict[str, list] = {a["key"]: [] for a in arcs}
    per_arc_remaining: dict[str, list] = {a["key"]: [] for a in arcs}
    for d in dates:
        rev = _rev_at(d, root)
        if not rev:
            continue
        fm = collect_task_frontmatter(rev, root)
        if not fm:
            continue  # pre-flip (tasks/ did not exist) or the git call failed -- not a zero
        for a in arcs:
            done, remaining = arc_counts(fm, a["themes"])
            per_arc_done[a["key"]].append((d, float(done)))
            per_arc_remaining[a["key"]].append((d, float(remaining)))

    out = []
    for a in arcs:
        done_pts = per_arc_done[a["key"]]
        out.append(ArcBurndown(
            key=a["key"], name=a["name"], themes=a["themes"],
            done=done_pts, remaining=per_arc_remaining[a["key"]],
            basis=("status: closed (done) vs status: open (remaining) in tasks/*.md,"
                   " filtered to theme(s) " + ", ".join(a["themes"]) + " -- the selector"
                   " declared for this arc in scripts/gen_north_star.py, read at each"
                   " weekly rev. deferred/retired/superseded rows belong to neither band,"
                   " the same rule banked_ledger applies to the whole-repo ledger."),
            state=classify_state(done_pts)))
    return out


# ---------------------------------------------------------------------------
# HY-4 / CUT-5: the quota panel -- provider and credits, folded into this lane
# ---------------------------------------------------------------------------

_PROVIDER_REGISTRY_RELPATH = "ecosystem/provider-registry.yaml"

_QUOTA_ABSENT_BASIS = (
    "NO STORE -- no machine-readable credit or quota field exists on any provider row in"
    " ecosystem/provider-registry.yaml: its schema (ecosystem/schema/provider_registry.py)"
    " sets extra=\"forbid\" and declares no such key today. A `quota_source` field was"
    " drafted and deliberately NOT filed"
    " (docs/audits/2026-08-31-technical-agy-admission-and-quota-visibility.md section 5):"
    " birthing a schema field is a functional decision for the operator, not this panel's"
    " to make. This row's PROVIDER identity is read live from the registry; its CREDITS"
    " value is named absent rather than fabricated.")

_MODEL_ATTRIBUTION_LIMIT = (
    "This panel CANNOT attribute a lane to a MODEL: [#615] (MODEL ATTRIBUTION -- the"
    " model+version commit trailer) is open and deliberately UNFUNDED in this batch. A"
    " partial series that looks complete is worse than an absent one -- [#615]'s own"
    " reasoning, applied to its own absence (architect ruling CUT-5).")


def collect_quota_rows(root: Path | None = None) -> list[QuotaRow]:
    """Every provider in `ecosystem/provider-registry.yaml`, credits named absent.

    PROVIDER IDENTITY IS DERIVED: a provider added to or removed from the registry
    appears or vanishes here without editing this module. CREDITS IS NOT: no store in this
    repo can compute a number, so every row states that absence rather than inventing one
    (see `QuotaRow`'s docstring and CUT-5).
    """
    import yaml

    path = (root or _REPO_ROOT) / _PROVIDER_REGISTRY_RELPATH
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")) or {}
    providers = data.get("providers") or {}
    out = []
    for key in sorted(providers):
        row = providers[key]
        if not isinstance(row, dict):
            continue
        out.append(QuotaRow(
            provider=key, display_name=str(row.get("display_name", key)),
            cli=row.get("cli"), credits_state="absent",
            credits_basis=_QUOTA_ABSENT_BASIS))
    return out


# ---------------------------------------------------------------------------
# Rendering -- inline SVG, ASCII only
# ---------------------------------------------------------------------------

_W, _H = 320.0, 78.0

_GLYPH = {
    # Drawn, never typed. An arrow character would be the only non-ASCII byte on the page
    # and the exact input the mojibake hazard needs.
    "improving": "0,10 12,10 6,0",   # up triangle
    "worsening": "0,0 12,0 6,10",    # down triangle
    "flat": "0,3 12,3 12,7 0,7",     # bar
    "unknown": "0,0 12,0 12,10 0,10",
}


def _esc(text: str) -> str:
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _fmt(v: float, unit: str) -> str:
    if unit == "bytes":
        return f"{v:,.0f}"
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.1f}"


def render_panel(series: Series) -> str:
    """One panel. An absent or insufficient panel draws NO line and claims NO direction."""
    head = (f'<article class="panel {_esc(series.state)}">'
            f'<h2>{_esc(series.label)}</h2>')

    if series.state == "absent":
        return (head
                + '<p class="verdict absent"><span class="tag">absent</span> no series</p>'
                + f'<p class="basis">{_esc(series.basis)}</p></article>')

    first, last = series.points[0], series.points[-1]
    span = (f'{_esc(first[0].isoformat())} to {_esc(last[0].isoformat())}'
            f' &middot; {len(series.points)} samples')

    if series.state == "insufficient":
        verdict = ('<p class="verdict insufficient"><span class="tag">insufficient'
                   '</span> history too short to state a direction</p>')
        chart = ""
    else:
        word, delta = direction(series.points, series.better)
        sign = "+" if delta > 0 else ""
        verdict = (f'<p class="verdict {word}">'
                   f'<svg class="glyph" viewBox="0 0 12 10" aria-hidden="true">'
                   f'<polygon points="{_GLYPH[word]}"/></svg>'
                   f'<span class="word">{word}</span>'
                   f'<span class="delta">{sign}{_fmt(delta, series.unit)}'
                   f' {_esc(series.unit)}</span></p>')
        budget = series.extra.get("budget")
        budget_line = ""
        if budget:
            lo, hi = scale_bounds(series.points, budget)
            by = scale_y(budget, lo, hi, _H)
            budget_line = (f'<line class="budget" x1="0" y1="{by:.2f}"'
                           f' x2="{_W:.0f}" y2="{by:.2f}"/>')
        chart = (f'<svg class="spark" viewBox="0 0 {_W:.0f} {_H:.0f}"'
                 f' preserveAspectRatio="none" role="img"'
                 f' aria-label="{_esc(series.label)} trend">'
                 f'{budget_line}'
                 f'<polyline points="{sparkline_points(series.points, _W, _H, budget)}"/>'
                 f'</svg>')

    values = (f'<p class="values"><span class="from">{_fmt(first[1], series.unit)}</span>'
              f'<span class="arrowless">to</span>'
              f'<span class="to">{_fmt(last[1], series.unit)}</span>'
              f'<span class="unit">{_esc(series.unit)}</span></p>')

    return (head + verdict + chart + values
            + f'<p class="span">{span}</p>'
            + f'<p class="predicate">{_esc(series.predicate)}</p>'
            + f'<p class="basis">{_esc(series.basis)}</p></article>')


def _scaled_points(points: list[tuple[date, float]], lo: float, hi: float,
                   w: float = _W, h: float = _H) -> str:
    """SVG `points` for one line, scaled against a CALLER-SUPPLIED (lo, hi).

    Unlike `sparkline_points` (which derives its own bounds from one series), a burn-down
    panel draws two lines that must share a single scale -- computing bounds separately
    per line would put `done` and `remaining` on two different y-axes inside the same box
    and misreport how close they are to converging.
    """
    if not points:
        return ""
    n = len(points)
    coords = []
    for i, (_, v) in enumerate(points):
        x = 0.0 if n == 1 else (w * i / (n - 1))
        coords.append(f"{x:.2f},{scale_y(v, lo, hi, h):.2f}")
    return " ".join(coords)


def render_burndown_panel(ab: ArcBurndown) -> str:
    """HY-4: one arc's done-vs-remaining panel. An absent or insufficient arc draws no
    line and claims no direction, mirroring `render_panel`.

    The direction verdict tracks REMAINING, not done: an arc's `done_when` is reached
    when remaining hits zero, so a flat `done` line (nothing newly closed this window)
    must not mask real burn-down if remaining is still falling for another reason (a row
    leaving the theme, or being retired).
    """
    head = (f'<article class="panel burndown {_esc(ab.state)}">'
            f'<h2>{_esc(ab.name)}</h2>')

    if ab.state == "absent":
        return (head
                + '<p class="verdict absent"><span class="tag">absent</span> no series</p>'
                + f'<p class="basis">{_esc(ab.basis)}</p></article>')

    d_last, r_last = ab.done[-1], ab.remaining[-1]
    span = (f'{_esc(ab.done[0][0].isoformat())} to {_esc(d_last[0].isoformat())}'
            f' &middot; {len(ab.done)} samples')

    if ab.state == "insufficient":
        verdict = ('<p class="verdict insufficient"><span class="tag">insufficient'
                   '</span> history too short to state a direction</p>')
        chart = ""
    else:
        word, delta = direction(ab.remaining, better="down")
        sign = "+" if delta > 0 else ""
        verdict = (f'<p class="verdict {word}">'
                   f'<svg class="glyph" viewBox="0 0 12 10" aria-hidden="true">'
                   f'<polygon points="{_GLYPH[word]}"/></svg>'
                   f'<span class="word">{word}</span>'
                   f'<span class="delta">remaining {sign}{_fmt(delta, "rows")} rows</span>'
                   f'</p>')
        lo, hi = scale_bounds(ab.done + ab.remaining)
        chart = (f'<svg class="spark" viewBox="0 0 {_W:.0f} {_H:.0f}"'
                 f' preserveAspectRatio="none" role="img"'
                 f' aria-label="{_esc(ab.name)} done vs remaining">'
                 f'<polyline class="done" points="{_scaled_points(ab.done, lo, hi)}"/>'
                 f'<polyline class="remaining"'
                 f' points="{_scaled_points(ab.remaining, lo, hi)}"/>'
                 f'</svg>')

    values = (f'<p class="values"><span class="from">done {_fmt(d_last[1], "rows")}</span>'
              f'<span class="arrowless">/</span>'
              f'<span class="to">remaining {_fmt(r_last[1], "rows")}</span>'
              f'<span class="unit">rows</span></p>')

    return (head + verdict + chart + values
            + f'<p class="span">{span}</p>'
            + f'<p class="predicate">done vs remaining, theme(s) '
              f'{_esc(", ".join(ab.themes))}</p>'
            + f'<p class="basis">{_esc(ab.basis)}</p></article>')


def render_quota_panel(rows: list[QuotaRow]) -> str:
    """HY-4 / CUT-5: provider identity, credits named absent -- no table, ever.

    A provider/credits grid rendered as an HTML `<table>` would be exactly the tabular
    shape this page's own ACCEPTANCE 2 refuses, even dressed in this page's own markup, so
    each provider is one paragraph rather than one row of a table.
    """
    if not rows:
        return ('<article class="panel quota absent"><h2>provider credits</h2>'
                '<p class="verdict absent"><span class="tag">absent</span> no provider'
                ' registry found</p></article>')

    items = "".join(
        f'<p class="quota-row"><span class="provider">{_esc(r.display_name)}</span>'
        f'<span class="tag">absent</span></p>'
        for r in rows)

    return (
        '<article class="panel quota absent"><h2>provider credits</h2>'
        '<p class="verdict absent"><span class="tag">absent</span> no numeric credits'
        ' store exists for any provider</p>'
        f'{items}'
        f'<p class="basis">{_esc(rows[0].credits_basis)}</p>'
        f'<p class="basis">{_esc(_MODEL_ATTRIBUTION_LIMIT)}</p></article>')


_CSS = """
:root{--bg:#fbfbfa;--fg:#1d1d1b;--dim:#6b6b66;--line:#d8d8d2;--card:#fff;
--good:#1a7f4b;--bad:#b3261e;--flat:#6b6b66;--absent:#8a8a84;--budget:#c98a00;}
@media (prefers-color-scheme:dark){:root{--bg:#16171a;--fg:#e8e8e4;--dim:#9a9a94;
--line:#2e3034;--card:#1d1f23;--good:#4ec27f;--bad:#f2736a;--flat:#9a9a94;
--absent:#77776f;--budget:#e0a52a;}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:14px/1.5 ui-sans-serif,-apple-system,Segoe UI,Roboto,sans-serif;padding:28px}
header{max-width:1180px;margin:0 auto 22px}
h1{font-size:20px;margin:0 0 4px;letter-spacing:-.01em}
.sub{color:var(--dim);margin:0;font-size:12.5px}
.grid{max-width:1180px;margin:0 auto;display:grid;
grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:15px 16px}
.panel h2{font-size:13px;margin:0 0 9px;font-weight:600;letter-spacing:.01em}
.verdict{display:flex;align-items:center;gap:7px;margin:0 0 10px;font-size:13px}
.glyph{width:12px;height:10px;flex:none}
.word{font-weight:650;text-transform:uppercase;letter-spacing:.04em;font-size:11.5px}
.delta{color:var(--dim);font-size:12px;margin-left:auto;
font-variant-numeric:tabular-nums}
.improving .glyph polygon{fill:var(--good)} .improving .word{color:var(--good)}
.worsening .glyph polygon{fill:var(--bad)} .worsening .word{color:var(--bad)}
.flat .glyph polygon{fill:var(--flat)} .flat .word{color:var(--flat)}
.unknown .glyph polygon{fill:var(--flat)} .unknown .word{color:var(--flat)}
.tag{font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;font-weight:650;
border:1px solid var(--line);border-radius:4px;padding:1px 6px;color:var(--absent)}
.verdict.absent,.verdict.insufficient{color:var(--dim);font-size:12px}
.spark{width:100%;height:78px;display:block;margin:0 0 8px}
.spark polyline{fill:none;stroke:currentColor;stroke-width:1.75;
vector-effect:non-scaling-stroke;stroke-linejoin:round;stroke-linecap:round}
.improving+.spark polyline{stroke:var(--good)}
.worsening+.spark polyline{stroke:var(--bad)}
.flat+.spark polyline,.unknown+.spark polyline{stroke:var(--flat)}
.budget{stroke:var(--budget);stroke-width:1;stroke-dasharray:4 3;
vector-effect:non-scaling-stroke}
.values{margin:0 0 6px;display:flex;align-items:baseline;gap:7px;
font-variant-numeric:tabular-nums}
.from{color:var(--dim);font-size:14px}
.arrowless{color:var(--dim);font-size:11px}
.to{font-size:20px;font-weight:640;letter-spacing:-.02em}
.unit{color:var(--dim);font-size:11.5px}
.span,.predicate,.basis{margin:0;color:var(--dim);font-size:11.5px}
.predicate{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;
margin-top:7px;padding-top:7px;border-top:1px solid var(--line);word-break:break-word}
.basis{margin-top:5px;line-height:1.45}
.panel.absent{opacity:.72}
.section-title{max-width:1180px;margin:26px auto 12px;font-size:14px;font-weight:650;
letter-spacing:.01em}
.spark .done{stroke:var(--good)}
.spark .remaining{stroke:var(--bad);stroke-dasharray:4 3}
.quota-row{display:flex;align-items:center;gap:8px;margin:0 0 6px;font-size:13px}
.quota-row .provider{font-weight:600}
footer{max-width:1180px;margin:22px auto 0;color:var(--dim);font-size:11.5px;
border-top:1px solid var(--line);padding-top:12px}
footer p{margin:0 0 5px}
"""


def render_page(series_list: list[Series], meta: dict,
                arc_burndowns: list[ArcBurndown] = (),
                quota_rows: list[QuotaRow] = ()) -> str:
    """The whole surface. Deterministic: same series + same meta -> byte-identical output.

    `arc_burndowns` and `quota_rows` are HY-4 additions, both OPTIONAL and both defaulting
    to empty: a caller that omits them gets exactly the pre-HY-4 page, byte for byte --
    the two existing call sites in `tests/test_trend_dashboard.py` (a file this lane may
    not edit) never pass them and must keep seeing the old shape.
    """
    panels = "".join(render_panel(s) for s in series_list)

    absent = [s for s in series_list if s.state == "absent"]
    short = [s for s in series_list if s.state == "insufficient"]
    legend = []
    if absent:
        legend.append("<p><strong>Absent series</strong> (named, never drawn as zero): "
                      + "; ".join(f"{_esc(s.label)} &mdash; {_esc(s.basis)}"
                                  for s in absent) + "</p>")
    if short:
        legend.append("<p><strong>Insufficient history</strong> (store exists, fewer than "
                      "3 samples; no direction claimed): "
                      + "; ".join(_esc(s.label) for s in short) + "</p>")
    legend.append(
        "<p><strong>Regenerate:</strong> "
        "<code>uv run --locked python scripts/gen_trend_dashboard.py --write</code> "
        "&mdash; reads git and the telemetry store, writes only this file, and is "
        "idempotent for a fixed history. Nothing on this page is hand-entered.</p>")

    extra_sections = ""
    if arc_burndowns:
        extra_sections += (
            '<h2 class="section-title">north-star arcs &mdash; done vs remaining</h2>'
            f'<section class="grid">'
            f'{"".join(render_burndown_panel(a) for a in arc_burndowns)}</section>')
    if quota_rows:
        extra_sections += (
            '<h2 class="section-title">provider quota (CUT-5)</h2>'
            f'<section class="grid">{render_quota_panel(quota_rows)}</section>')

    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>.dev-knowledge trends</title>'
        f"<style>{_CSS}</style></head><body>"
        '<header><h1>.dev-knowledge &mdash; direction of travel</h1>'
        f'<p class="sub">window {_esc(meta.get("window", ""))} &middot; '
        f'state of {_esc(meta.get("generated_at", ""))} &middot; '
        f'at {_esc(meta.get("sha", ""))} &middot; '
        'every point is read back out of a store; none is computed for this page</p>'
        '</header>'
        f'<main class="grid">{panels}</main>'
        f'{extra_sections}'
        f'<footer>{"".join(legend)}</footer>'
        "</body></html>\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _positive_weeks(raw: str) -> int:
    """argparse type: a window of at least one week, refused at the CLI boundary."""
    try:
        value = int(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(f"weeks must be an integer, got {raw!r}") from None
    if value < 1:
        raise argparse.ArgumentTypeError(f"weeks must be >= 1, got {value}")
    return value


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true",
                    help=f"write {OUT_RELPATH} (default: print the summary only)")
    ap.add_argument("--weeks", type=_positive_weeks, default=12,
                    help="window length in weeks (>= 1)")
    ap.add_argument("--out", default=None, help="override the output path")
    args = ap.parse_args(argv)

    series_list = build_series(weeks=args.weeks)
    arc_burndowns = build_arc_burndowns(weeks=args.weeks)
    quota_rows = collect_quota_rows()
    head = _git("rev-parse", "--short", "HEAD").strip() or "unknown"
    # THE STAMP IS DERIVED FROM THE INPUT, NOT FROM THE CLOCK (terra pre-merge, H7).
    # A wall-clock stamp made every regeneration differ by a few bytes, so the page could
    # never actually satisfy the acceptance test it claims -- "regenerable, and a
    # regeneration must be idempotent". Stamping HEAD's own commit date makes the artifact
    # byte-identical for a fixed history, and it is the more honest field anyway: it says
    # WHICH STATE this page describes, where the clock only said when someone ran it.
    meta = {"generated_at": _git("log", "-1", "--format=%cI", "HEAD").strip() or "unknown",
            "sha": head, "window": f"{args.weeks}w"}
    page = render_page(series_list, meta, arc_burndowns=arc_burndowns,
                       quota_rows=quota_rows)

    # ASCII-only console summary (cp1252 console; a non-encodable glyph would crash
    # exactly the run that produces the artifact).
    for s in series_list:
        if s.state == "absent":
            verdict = "ABSENT"
        elif s.state == "insufficient":
            verdict = f"INSUFFICIENT ({len(s.points)} pts)"
        else:
            word, delta = direction(s.points, s.better)
            verdict = f"{word.upper():<10} {delta:+.0f} {s.unit}"
        print(f"  {s.label:<38} {verdict}")
    for ab in arc_burndowns:
        if ab.state == "absent":
            verdict = "ABSENT"
        elif ab.state == "insufficient":
            verdict = f"INSUFFICIENT ({len(ab.done)} pts)"
        else:
            word, delta = direction(ab.remaining, better="down")
            verdict = f"{word.upper():<10} remaining {delta:+.0f}"
        print(f"  arc: {ab.name:<38} {verdict}")
    if quota_rows:
        print(f"  provider credits: ABSENT for {len(quota_rows)} provider(s)"
              " -- no numeric store exists; see the panel")

    if args.write:
        out = Path(args.out) if args.out else (_REPO_ROOT / OUT_RELPATH)
        out.parent.mkdir(parents=True, exist_ok=True)
        # write_bytes, not write_text: write_text launders LF to CRLF on this platform and
        # a round-trip read cannot detect it, which would make "idempotent" untestable.
        out.write_bytes(page.encode("ascii"))
        # Verify the bytes just written rather than trusting exit 0 -- the recorded
        # `gen_dashboard` failure mode is silent mojibake WITH a clean exit.
        written = out.read_bytes()
        written.decode("ascii")
        if written != page.encode("ascii"):
            print("FAIL: written bytes differ from the rendered page", file=sys.stderr)
            return 1
        # `--out` may legitimately point outside the repo (a scratch dir, a diff harness),
        # and relative_to() RAISES rather than falling back when it does.
        try:
            shown = out.resolve().relative_to(_REPO_ROOT)
        except ValueError:
            shown = out
        print(f"\nwrote {shown} ({len(written):,} bytes, ascii-verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
