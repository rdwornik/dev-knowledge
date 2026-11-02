#!/usr/bin/env python
"""system_view.py -- the ADR-133 system view: `view.json` and `view.html`, a pure rendering of organ outputs.

WHAT THIS ANSWERS. "What does the system look like as its organs compute it -- the graph, the process,
the runs and the state -- with every figure traced to its source?" ADR-133 (ratified 2026-11-01, see
to-browser/RATIFICATION-2026-11-01-ADR-133.md) is the contract; this module is built AS RATIFIED.
Row `[#1748]`. Called by `scripts/system_map.py view`; stdlib only at module level (the two organs
whose output is read through a function -- the ledger and the conductor metrics, and the quota
ledger's path -- are imported lazily inside their seam functions).

THE SHAPE.
  * A READER reads ONE organ output and returns TILES. Every tile carries its source, its checkout,
    a STATE (OK / STALE / ABSENT / UNREADABLE / NOT COMPUTED) and a STALENESS (OK / STALE / NOT COMPUTED).
  * Every value is a CELL `{"v": value, "r": reader id}`; `check_provenance` refuses a cell with no
    reader id, so no value reaches the page that no reader produced (D2).
  * Hand-written text lives ONLY in `LABELS` (bounded, hash-pinned by a test), `PAGE_CSS` and
    `PAGE_SCRIPT` (both hash-pinned). The renderer is a deterministic function of the view dict (D3).
  * Exactly ONE free-text pair is allowed: a task's `title`, cut to `TITLE_MAX`, marked `"src": true`
    (the operator's ruling, 2026-11-01).
  * STALE means `now - the source's own timestamp > THRESHOLDS[reader]`. A source with no timestamp
    field of its own is never STALE: its staleness is NOT COMPUTED (D2).

THREE LEGS (D4). `fast` never calls the whole-tree map build; `full` is run after it by the CLI;
`scheduled` reads ONLY the tracked map record and `logs/MERGE-RECEIPTS.jsonl`. None is a gate.

THE PAGE (D5, D6). One file, two modes: the static rendering plus an embedded snapshot of the view
(every `<` escaped); served over http it re-reads `view.json` on an interval and keeps the snapshot
when the parse fails; the Mermaid library is added by the page script ONLY over http, with an SRI hash.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Sequence

SCHEMA = "system-view/1"
VIEW_JSON_NAME = "view.json"
VIEW_HTML_NAME = "view.html"
LEGS = ("fast", "full", "scheduled")
TITLE_MAX = 100
#: The ONE (reader, field) pair whose free text may be shown (ratification, 2026-11-01).
FREE_TEXT_ALLOWLIST = (("tasks", "title"),)
#: Rows listed per tile before the list is cut; the COUNT is never cut.
ROW_CAP = 12
TASK_ROW_CAP = 30

STATE_OK, STATE_STALE, STATE_ABSENT = "OK", "STALE", "ABSENT"
STATE_UNREADABLE, STATE_NOT_COMPUTED = "UNREADABLE", "NOT COMPUTED"

#: Mermaid: the library, version, URL and SRI hash, as data in ONE place (D6). sha384 of
#: https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js, computed 2026-11-02.
MERMAID = {
    "library": "mermaid",
    "version": "11.4.1",
    "url": "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js",
    "integrity": "sha384-rbtjAdnIQE/aQJGEgXrVUlMibdfTSa4PQju4HDhN3sR2PmaKFzhEafuePsl9H/9I",
}

#: Per-reader maximum ages, seconds: ONE bounded table (part of the label and threshold table, D2).
THRESHOLDS = {
    "launch-receipts": 259200,  # 3 days: a lane lives about one batch window
    "merge-receipts": 604800,   # 7 days: a row is written per merge, merges come in batches
    "phase-receipts": 259200,   # 3 days: same lane lifetime
    "quota": 172800,            # 2 days: quota_daily reads it daily
}

#: reader id -> the measured shape of its source (see the receipt's SOURCE lines).
SOURCES = {
    "map-json": {"path": "ecosystem/system-map.json", "required": ("schema", "meta"),
                 "optional": ("leaf_count", "organ_count", "dead_count", "unexplained_count"),
                 "timestamp_field": None, "max_age": None},
    "map-record": {"path": "ecosystem/system-map-record.json", "required": ("map_sha", "node_count"),
                   "optional": ("previous_sha", "diff"), "timestamp_field": None, "max_age": None},
    "p1-mermaid": {"path": "ecosystem/process-binding.yaml", "required": ("diagram_mermaid",),
                   "optional": (), "timestamp_field": None, "max_age": None},
    "launch-receipts": {"path": "logs/receipts/LAUNCH-*.json", "required": ("slug", "launched_at"),
                        "optional": ("batch", "kind", "attempt", "model_requested", "job_id"),
                        "timestamp_field": "launched_at", "max_age": THRESHOLDS["launch-receipts"]},
    "phase-receipts": {"path": "logs/receipts/LANE-*/r*/*.json",
                       "required": ("lane", "phase", "status", "finished_at"),
                       "optional": ("round", "served_model", "vendor"),
                       "timestamp_field": "finished_at", "max_age": THRESHOLDS["phase-receipts"]},
    "merge-receipts": {"path": "logs/MERGE-RECEIPTS.jsonl", "required": ("slug", "closed"),
                       "optional": ("batch", "kind", "merge_sha", "recorded_seconds"),
                       "timestamp_field": "closed", "max_age": THRESHOLDS["merge-receipts"]},
    "ledger": {"path": "scripts/gen_ledger.py", "required": ("head", "main", "open_rows", "blocked", "worktrees"),
               "optional": ("open_batches", "proposal"), "timestamp_field": None, "max_age": None},
    "conductor-metrics": {"path": "scripts/conductor.py",
                          "required": ("n1_automated_transitions", "n3_operator_pastes", "n4_organs_deleted"),
                          "optional": ("n2_operator_hours", "n5_actions_minutes"),
                          "timestamp_field": None, "max_age": None},
    "quota": {"path": "QUOTA-READS.jsonl (per-user state directory)",
              "required": ("group", "cycle", "used", "quota", "pct"), "optional": ("billed", "measured"),
              "timestamp_field": "measured", "max_age": THRESHOLDS["quota"]},
    "health": {"path": "scripts/audit.py health", "required": (), "optional": (),
               "timestamp_field": None, "max_age": None},
    "verdicts": {"path": "logs/PROVIDER-VERDICTS.json", "required": ("rows",),
                 "optional": ("row", "generated_by"), "timestamp_field": None, "max_age": None},
    "tasks": {"path": "tasks/*.md", "required": ("id", "title", "status"), "optional": ("priority",),
              "timestamp_field": None, "max_age": None},
}
READER_IDS = tuple(SOURCES)
#: The id under which assembly itself produced a top-level value (`assembled_at`, `leg`); not a reader.
ASSEMBLY_ID = "assembly"
#: In the scheduled leg ONLY these two readers run (D4).
SCHEDULED_READERS = ("map-record", "merge-receipts")

#: The label table: the ONE place hand-written text may live (D3). Bounded in size and entry length and
#: pinned by hash in tests/test_system_view.py -- a change here is a deliberate, diff-visible change.
LABELS = {
    "title": "System view",
    "lang": "en",
    "charset": "utf-8",
    "json_type": "application/json",
    "data_id": "view-data",
    "assembled": "Assembled",
    "leg": "Leg",
    "mermaid": "Mermaid renderer",
    "library": "Library",
    "version": "Version",
    "url": "URL",
    "integrity": "Integrity",
    "source": "Source",
    "checkout": "Checkout",
    "state": "State",
    "staleness": "Staleness",
    "reason": "Reason",
    "source_text": "source text",
    "diagram": "Diagram source",
    "lines": "Lines",
    "count": "Count",
    "shown": "Shown",
    "reader.map-json": "Map JSON",
    "reader.map-record": "Map record",
    "reader.p1-mermaid": "P1 process diagram",
    "reader.launch-receipts": "Launch receipts",
    "reader.phase-receipts": "Phase receipts",
    "reader.merge-receipts": "Merge receipts",
    "reader.ledger": "Ledger",
    "reader.conductor-metrics": "Conductor metrics",
    "reader.quota": "Quota reads",
    "reader.health": "Health",
    "reader.verdicts": "Provider verdicts",
    "reader.tasks": "Open tasks",
    "schema": "Schema",
    "leaf_count": "Files",
    "organ_count": "Organs",
    "dead_count": "Dead organs",
    "unexplained_count": "Unexplained files",
    "map_sha": "Map sha",
    "node_count": "Nodes",
    "previous_sha": "Previous sha",
    "added_count": "Nodes added",
    "removed_count": "Nodes removed",
    "slug": "Slug",
    "batch": "Batch",
    "kind": "Kind",
    "attempt": "Attempt",
    "launched_at": "Launched at",
    "model_requested": "Model requested",
    "job_id": "Job",
    "lane": "Lane",
    "phase": "Phase",
    "status": "Status",
    "finished_at": "Finished at",
    "round": "Round",
    "served_model": "Served model",
    "vendor": "Vendor",
    "merge_sha": "Merge sha",
    "closed": "Closed",
    "recorded_seconds": "Seconds",
    "head": "Head",
    "main": "Main",
    "open_rows": "Open rows",
    "blocked": "Blocked rows",
    "worktrees": "Worktrees",
    "open_batches": "Open batches",
    "automated_transitions": "Automated transitions",
    "operator_hours": "Operator hours",
    "operator_pastes": "Operator pastes",
    "organs_deleted": "Organs deleted",
    "organs_present": "Organs present",
    "actions_minutes": "Actions minutes",
    "group": "Group",
    "cycle": "Cycle",
    "used": "Used",
    "quota": "Quota",
    "pct": "Percent",
    "billed": "Billed",
    "measured": "Measured at",
    "provider": "Provider",
    "verdict": "Verdict",
    "passed": "Passed",
    "runs": "Runs",
    "id": "Id",
    "task_title": "Title",
    "priority": "Priority",
    "open_total": "Open",
    "all_total": "All",
    "no-timestamp": "the source has no timestamp field",
    "no-stored-output": "the organ stores no output",
    "leg-scheduled": "not read in the scheduled leg",
    "missing-source": "no source file",
    "missing-required-field": "a required field is missing",
    "unparseable": "the source cannot be parsed",
    "reader-failed": "the reader raised an error",
    "metric-not-computed": "the organ did not compute it",
}

#: String literals the page script may hold: data keys and a fixed list of selectors (D3).
SCRIPT_LITERALS = (
    "view-data", ".", "[data-p]", "data-p", "view.json", "no-store", "http:", "https:",
    "script", "anonymous", "pre", "div", "mermaid",
)

PAGE_SCRIPT = (
    "(function(){var D=JSON.parse(document.getElementById('view-data').textContent);\n"
    "function at(o,p){var k=p.split('.');for(var i=0;i<k.length;i++){if(o==null){return o;}o=o[k[i]];}return o;}\n"
    "function paint(){var L=D.labels;document.querySelectorAll('[data-p]').forEach(function(e){"
    "var v=at(D,e.getAttribute('data-p'));if(v==null){return;}"
    "e.textContent=Object.prototype.hasOwnProperty.call(L,v)?L[v]:String(v);});}\n"
    "function draw(){var m=window.mermaid;if(!m){return;}m.initialize({startOnLoad:false});"
    "document.querySelectorAll('pre').forEach(function(p){var d=document.createElement('div');"
    "d.className='mermaid';d.textContent=p.textContent;p.after(d);m.run({nodes:[d]});});}\n"
    "function poll(){fetch('view.json',{cache:'no-store'}).then(function(r){return r.text();})"
    ".then(function(t){try{var n=JSON.parse(t);D=n;paint();}catch(e){}}).catch(function(){});}\n"
    "if(location.protocol=='http:'||location.protocol=='https:'){var s=document.createElement('script');"
    "Object.assign(s,{src:D.mermaid.url.v,integrity:D.mermaid.integrity.v,crossOrigin:'anonymous',onload:draw});"
    "document.head.appendChild(s);setInterval(poll,30000);}\n"
    "})();\n"
)

PAGE_CSS = (
    ":root{color-scheme:light dark}\n"
    "body{font:14px/1.45 system-ui,sans-serif;margin:16px;max-width:1100px}\n"
    "h1{font-size:20px;margin:0 0 8px}h2{font-size:15px;margin:20px 0 6px}\n"
    "section{border:1px solid #8884;border-radius:6px;padding:4px 10px;margin:8px 0}\n"
    "table{border-collapse:collapse;display:block;overflow-x:auto}\n"
    "td,th{border-bottom:1px solid #8884;padding:2px 8px;text-align:left;vertical-align:top;"
    "font-family:ui-monospace,Consolas,monospace;font-size:12.5px}\n"
    "th{font-weight:600}pre{overflow-x:auto;font-size:12px}q{font-style:italic}small{opacity:.7}\n"
)


class ProvenanceError(ValueError):
    """A value reached assembly that no reader produced."""


# ------------------------------------------------------------------------------------ cells and tiles


def _cell(value, reader: str, **extra) -> dict:
    return {"v": value, "r": reader, **extra}


def _tile(reader: str, root: Path, *, state: str, staleness: str, reason: str | None = None,
          fields=(), columns=(), rows=(), checkout: str | None = None, suffix: str = "") -> dict:
    spec = SOURCES[reader]
    return {
        "id": reader + suffix,
        "reader": reader,
        "source": _cell(spec["path"], reader),
        "checkout": _cell(checkout if checkout is not None else root.name, reader),
        "state": _cell(state, reader),
        "staleness": _cell(staleness, reader),
        "reason": _cell(reason, reader) if reason else None,
        "fields": [{"label": label, "cell": cell} for label, cell in fields],
        "columns": list(columns),
        "rows": [list(r) for r in rows],
    }


def _absent(reader: str, root: Path, **kw) -> dict:
    return _tile(reader, root, state=STATE_ABSENT, staleness="NOT COMPUTED", reason="missing-source", **kw)


def _unreadable(reader: str, root: Path, reason: str = "missing-required-field", **kw) -> dict:
    return _tile(reader, root, state=STATE_UNREADABLE, staleness="NOT COMPUTED", reason=reason, **kw)


def _parse_time(text) -> datetime | None:
    if not isinstance(text, str):
        return None
    try:
        when = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return when if when.tzinfo else when.replace(tzinfo=timezone.utc)


def _freshness(reader: str, newest: datetime | None, now: datetime) -> tuple[str, str]:
    """(state, staleness) for a READABLE source."""
    spec = SOURCES[reader]
    if spec["timestamp_field"] is None or newest is None:
        return STATE_OK, STATE_NOT_COMPUTED
    if (now - newest).total_seconds() > spec["max_age"]:
        return STATE_STALE, STATE_STALE
    return STATE_OK, STATE_OK


def _scalar(value):
    """A cell value: ints, strings and bools stay; floats become fixed strings (JS prints them differently)."""
    if isinstance(value, bool) or isinstance(value, int) or isinstance(value, str):
        return value
    if isinstance(value, float):
        return f"{value:.2f}"
    return json.dumps(value, sort_keys=True, ensure_ascii=True)


def _present(record: dict, key: str) -> bool:
    return key in record and record[key] is not None


def _missing_required(record, required: Sequence[str]) -> bool:
    return not isinstance(record, dict) or any(not _present(record, key) for key in required)


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------------- the file readers


def read_map_json(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    reader = "map-json"
    path = Path(map_json) if map_json else root / "ecosystem" / "system-map.json"
    if not path.is_file():
        return [_absent(reader, root)]
    try:
        data = _read_json(path)
    except (OSError, ValueError):
        return [_unreadable(reader, root, "unparseable")]
    if _missing_required(data, SOURCES[reader]["required"]) or not isinstance(data["meta"], dict):
        return [_unreadable(reader, root)]
    fields = [("schema", _cell(_scalar(data["schema"]), reader))]
    for key in SOURCES[reader]["optional"]:
        if _present(data["meta"], key):
            fields.append((key, _cell(_scalar(data["meta"][key]), reader)))
    state, staleness = _freshness(reader, None, now)
    return [_tile(reader, root, state=state, staleness=staleness, reason="no-timestamp", fields=fields)]


def read_map_record(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    reader = "map-record"
    path = root / "ecosystem" / "system-map-record.json"
    if not path.is_file():
        return [_absent(reader, root)]
    try:
        data = _read_json(path)
    except (OSError, ValueError):
        return [_unreadable(reader, root, "unparseable")]
    if _missing_required(data, SOURCES[reader]["required"]):
        return [_unreadable(reader, root)]
    fields = [("map_sha", _cell(_scalar(data["map_sha"]), reader)),
              ("node_count", _cell(_scalar(data["node_count"]), reader))]
    if _present(data, "previous_sha"):
        fields.append(("previous_sha", _cell(_scalar(data["previous_sha"]), reader)))
    diff = data.get("diff")
    if isinstance(diff, dict):
        for key in ("added_count", "removed_count"):
            if _present(diff, key):
                fields.append((key, _cell(_scalar(diff[key]), reader)))
    state, staleness = _freshness(reader, None, now)
    return [_tile(reader, root, state=state, staleness=staleness, reason="no-timestamp", fields=fields)]


_MERMAID_BLOCK = re.compile(r"^diagram_mermaid:[ \t]*\|[-+]?[ \t]*\r?\n((?:[ \t]+[^\n]*\n?|[ \t]*\r?\n)+)", re.M)


def read_p1_mermaid(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    reader = "p1-mermaid"
    path = root / "ecosystem" / "process-binding.yaml"
    if not path.is_file():
        return [_absent(reader, root)]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return [_unreadable(reader, root, "unparseable")]
    match = _MERMAID_BLOCK.search(text if text.endswith("\n") else text + "\n")
    if not match:
        return [_unreadable(reader, root)]
    lines = match.group(1).rstrip().splitlines()
    indent = min((len(ln) - len(ln.lstrip()) for ln in lines if ln.strip()), default=0)
    source = "\n".join(ln[indent:] for ln in lines).strip("\n")
    if not source:
        return [_unreadable(reader, root)]
    fields = [("lines", _cell(len(source.splitlines()), reader)), ("diagram", _cell(source, reader))]
    state, staleness = _freshness(reader, None, now)
    return [_tile(reader, root, state=state, staleness=staleness, reason="no-timestamp", fields=fields)]


def _checkouts(root: Path, siblings: Sequence[Path]) -> list[Path]:
    seen, out = set(), []
    for path in (root, *siblings):
        path = Path(path)
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            out.append(path)
    return out


def _receipt_tiles(reader: str, root: Path, siblings: Sequence[Path], now: datetime, files_of, columns,
                   row_of) -> list[dict]:
    """One tile per checkout (the current one and each sibling, READ-ONLY): rows from `files_of`."""
    spec = SOURCES[reader]
    tiles = []
    for checkout in _checkouts(root, siblings):
        files = files_of(checkout)
        if not files:
            tiles.append(_absent(reader, checkout, suffix=":" + checkout.name))
            continue
        records, bad = [], False
        for file in files:
            try:
                data = _read_json(file)
            except (OSError, ValueError):
                bad = True
                continue
            if _missing_required(data, spec["required"]) or _parse_time(data[spec["timestamp_field"]]) is None:
                bad = True
                continue
            records.append(data)
        records.sort(key=lambda r: (_parse_time(r[spec["timestamp_field"]]), json.dumps(r, sort_keys=True,
                                                                                         default=str)),
                     reverse=True)
        rows = [row_of(r, reader) for r in records[:ROW_CAP]]
        fields = [("count", _cell(len(records), reader)), ("shown", _cell(len(rows), reader))]
        if bad:
            tiles.append(_tile(reader, checkout, state=STATE_UNREADABLE, staleness=STATE_NOT_COMPUTED,
                               reason="missing-required-field", fields=fields, columns=columns, rows=rows,
                               suffix=":" + checkout.name))
            continue
        newest = _parse_time(records[0][spec["timestamp_field"]]) if records else None
        state, staleness = _freshness(reader, newest, now)
        tiles.append(_tile(reader, checkout, state=state, staleness=staleness, fields=fields, columns=columns,
                           rows=rows, suffix=":" + checkout.name))
    return tiles


def _row(record: dict, reader: str, keys: Sequence[str]) -> list[dict]:
    return [_cell(_scalar(record[k]) if _present(record, k) else "", reader) for k in keys]


_LAUNCH_COLUMNS = ("slug", "batch", "kind", "attempt", "launched_at", "model_requested")
_PHASE_COLUMNS = ("lane", "phase", "status", "round", "finished_at", "served_model")
_MERGE_COLUMNS = ("slug", "batch", "kind", "merge_sha", "closed", "recorded_seconds")


def read_launch_receipts(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    def files_of(checkout: Path) -> list[Path]:
        folder = checkout / "logs" / "receipts"
        return sorted(p for p in folder.glob("LAUNCH-*.json") if not p.name.startswith("LAUNCH-JOB-")) \
            if folder.is_dir() else []
    return _receipt_tiles("launch-receipts", root, siblings, now, files_of, _LAUNCH_COLUMNS,
                          lambda r, rd: _row(r, rd, _LAUNCH_COLUMNS))


def read_phase_receipts(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    def files_of(checkout: Path) -> list[Path]:
        folder = checkout / "logs" / "receipts"
        return sorted(folder.glob("LANE-*/r*/*.json")) if folder.is_dir() else []
    return _receipt_tiles("phase-receipts", root, siblings, now, files_of, _PHASE_COLUMNS,
                          lambda r, rd: _row(r, rd, _PHASE_COLUMNS))


def read_merge_receipts(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    reader = "merge-receipts"
    spec = SOURCES[reader]
    path = root / "logs" / "MERGE-RECEIPTS.jsonl"
    if not path.is_file():
        return [_absent(reader, root)]
    records = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            data = json.loads(line)
            if _missing_required(data, spec["required"]) or _parse_time(data["closed"]) is None:
                return [_unreadable(reader, root)]
            records.append(data)
    except (OSError, ValueError):
        return [_unreadable(reader, root, "unparseable")]
    records.sort(key=lambda r: _parse_time(r["closed"]), reverse=True)
    rows = [_row(r, reader, _MERGE_COLUMNS) for r in records[:ROW_CAP]]
    state, staleness = _freshness(reader, _parse_time(records[0]["closed"]) if records else None, now)
    return [_tile(reader, root, state=state, staleness=staleness,
                  fields=[("count", _cell(len(records), reader)), ("shown", _cell(len(rows), reader))],
                  columns=_MERGE_COLUMNS, rows=rows)]


def _quota_path(root: Path) -> Path:
    override = os.environ.get("DEV_KNOWLEDGE_QUOTA_READS_LEDGER")
    if override:
        return Path(override)
    import quota_watch  # lazy: the quota ledger's own path rule (per-user state directory)
    return quota_watch.reads_ledger_path(root)


_QUOTA_COLUMNS = ("group", "cycle", "used", "quota", "pct", "billed", "measured")


def read_quota(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    reader = "quota"
    spec = SOURCES[reader]
    try:
        path = _quota_path(root)
    except Exception:  # noqa: BLE001 -- an unresolvable path is a missing source, not a crash
        return [_absent(reader, root)]
    if not path.is_file():
        return [_absent(reader, root)]
    records = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            data = json.loads(line)
            if _missing_required(data, spec["required"]):
                return [_unreadable(reader, root)]
            if _present(data, "measured") and _parse_time(data["measured"]) is None:
                return [_unreadable(reader, root, "unparseable")]  # a stamp that is there but not a time
            records.append(data)
    except (OSError, ValueError):
        return [_unreadable(reader, root, "unparseable")]
    stamps = [t for t in (_parse_time(r.get("measured")) for r in records) if t is not None]
    state, staleness = _freshness(reader, max(stamps) if stamps else None, now)
    total = len(records)
    rows = [_row(r, reader, _QUOTA_COLUMNS) for r in records[-ROW_CAP:]]
    return [_tile(reader, root, state=state, staleness=staleness,
                  reason=None if stamps else "no-timestamp",
                  fields=[("count", _cell(total, reader)), ("shown", _cell(len(rows), reader))],
                  columns=_QUOTA_COLUMNS, rows=rows)]


_VERDICT_COLUMNS = ("provider", "verdict", "passed", "runs")


def read_verdicts(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    reader = "verdicts"
    path = root / "logs" / "PROVIDER-VERDICTS.json"
    if not path.is_file():
        return [_absent(reader, root)]
    try:
        data = _read_json(path)
    except (OSError, ValueError):
        return [_unreadable(reader, root, "unparseable")]
    if _missing_required(data, SOURCES[reader]["required"]) or not isinstance(data["rows"], list) \
            or any(_missing_required(r, ("provider", "verdict")) for r in data["rows"]):
        return [_unreadable(reader, root)]
    rows = [_row(r, reader, _VERDICT_COLUMNS) for r in data["rows"][:ROW_CAP]]
    state, staleness = _freshness(reader, None, now)
    return [_tile(reader, root, state=state, staleness=staleness, reason="no-timestamp",
                  fields=[("count", _cell(len(data["rows"]), reader))], columns=_VERDICT_COLUMNS, rows=rows)]


_FRONT = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.S)


def _frontmatter(path: Path) -> dict:
    match = _FRONT.match(path.read_text(encoding="utf-8"))
    if not match:
        return {}
    out = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() and not key.startswith((" ", "\t")):
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def _task_sort(record: dict):
    num = re.search(r"\d+", record["id"])
    return (record.get("priority", "P9"), int(num.group()) if num else 0)


def read_tasks(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    reader = "tasks"
    folder = root / "tasks"
    files = sorted(p for p in folder.glob("*.md") if p.name.lower() != "readme.md") if folder.is_dir() else []
    if not files:
        return [_absent(reader, root)]
    records = []
    for file in files:
        try:
            data = _frontmatter(file)
        except (OSError, ValueError):
            return [_unreadable(reader, root, "unparseable")]
        if _missing_required(data, SOURCES[reader]["required"]):
            return [_unreadable(reader, root)]
        records.append(data)
    open_rows = sorted((r for r in records if r["status"] == "open"), key=_task_sort)
    rows = [[_cell(r["id"], reader), _cell(r.get("priority", ""), reader),
             _cell(r["title"][:TITLE_MAX], reader, src=True)] for r in open_rows[:TASK_ROW_CAP]]
    state, staleness = _freshness(reader, None, now)
    return [_tile(reader, root, state=state, staleness=staleness, reason="no-timestamp",
                  fields=[("open_total", _cell(len(open_rows), reader)), ("all_total", _cell(len(records), reader))],
                  columns=("id", "priority", "task_title"), rows=rows)]


# ------------------------------------------------------------------------ the function-backed readers


def _ledger_collect(root: Path) -> dict:
    """Seam: `gen_ledger.collect`, the local leg only (offline: no fetch)."""
    import gen_ledger  # lazy: an organ read through its own collect function
    return gen_ledger.collect(root, offline=True)


def _conductor_metrics(root: Path) -> dict:
    """Seam: `conductor.metrics` without the gh leg."""
    import conductor  # lazy
    return conductor.metrics(root, use_gh=False)


def _count(value) -> int:
    if isinstance(value, (list, tuple, dict, set)):
        return len(value)
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    raise ValueError("not a count")


def read_ledger(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    reader = "ledger"
    try:
        data = _ledger_collect(root)
    except Exception:  # noqa: BLE001 -- an organ that cannot run is UNREADABLE, not a crash
        return [_unreadable(reader, root, "reader-failed")]
    if _missing_required(data, SOURCES[reader]["required"]):
        return [_unreadable(reader, root)]
    try:
        fields = [("head", _cell(_scalar(data["head"]), reader)), ("main", _cell(_scalar(data["main"]), reader)),
                  ("open_rows", _cell(_count(data["open_rows"]), reader)),
                  ("blocked", _cell(_count(data["blocked"]), reader)),
                  ("worktrees", _cell(_count(data["worktrees"]), reader))]
        if _present(data, "open_batches"):
            fields.append(("open_batches", _cell(_count(data["open_batches"]), reader)))
    except ValueError:
        return [_unreadable(reader, root)]
    state, staleness = _freshness(reader, None, now)
    return [_tile(reader, root, state=state, staleness=staleness, reason="no-timestamp", fields=fields)]


def _metric(entry, keys: Sequence[str]):
    """The number an organ computed, or None; the organ's own prose reason is NOT carried (D3)."""
    if not isinstance(entry, dict):
        return None
    for key in keys:
        value = entry.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value
    return None


def read_conductor_metrics(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    reader = "conductor-metrics"
    try:
        data = _conductor_metrics(root)
    except Exception:  # noqa: BLE001
        return [_unreadable(reader, root, "reader-failed")]
    if _missing_required(data, SOURCES[reader]["required"]):
        return [_unreadable(reader, root)]

    def shown(value):
        return _cell(_scalar(value) if value is not None else STATE_NOT_COMPUTED, reader)

    fields = [("automated_transitions", shown(_metric(data["n1_automated_transitions"], ("runs", "value")))),
              ("operator_pastes", shown(_metric(data["n3_operator_pastes"], ("value",))))]
    n4 = data["n4_organs_deleted"]
    for label, key in (("organs_deleted", "deleted"), ("organs_present", "present")):
        fields.append((label, shown(len(n4[key]) if isinstance(n4, dict) and isinstance(n4.get(key), list)
                                    else None)))
    if _present(data, "n2_operator_hours"):
        fields.append(("operator_hours", shown(_metric(data["n2_operator_hours"], ("hours", "value")))))
    if _present(data, "n5_actions_minutes"):
        fields.append(("actions_minutes", shown(_metric(data["n5_actions_minutes"], ("minutes", "value")))))
    state, staleness = _freshness(reader, None, now)
    return [_tile(reader, root, state=state, staleness=staleness, reason="no-timestamp", fields=fields)]


def read_health(root: Path, *, now: datetime, siblings=(), map_json=None) -> list[dict]:
    """`audit.py health` is "No file writes": it stores no output, so there is nothing to read."""
    return [_tile("health", root, state=STATE_NOT_COMPUTED, staleness=STATE_NOT_COMPUTED, reason="no-stored-output")]


READERS: dict[str, Callable[..., list[dict]]] = {
    "map-json": read_map_json,
    "map-record": read_map_record,
    "p1-mermaid": read_p1_mermaid,
    "launch-receipts": read_launch_receipts,
    "phase-receipts": read_phase_receipts,
    "merge-receipts": read_merge_receipts,
    "ledger": read_ledger,
    "conductor-metrics": read_conductor_metrics,
    "quota": read_quota,
    "health": read_health,
    "verdicts": read_verdicts,
    "tasks": read_tasks,
}


def read_source(reader_id: str, root: Path, *, now: datetime, siblings: Sequence[Path] = (),
                map_json=None) -> list[dict]:
    """The tiles of ONE reader."""
    return READERS[reader_id](Path(root), now=now, siblings=tuple(siblings), map_json=map_json)


# ---------------------------------------------------------------------------------------- assembly


#: The only top-level keys of a view. Anything else is refused (a value no reader produced).
VIEW_KEYS = ("schema", "assembled_at", "leg", "labels", "thresholds", "readers", "mermaid", "tiles")
_TILE_CELLS = ("source", "checkout", "state", "staleness")
_TILE_KEYS = ("id", "reader", "columns", "fields", "rows", "reason", *_TILE_CELLS)


def check_provenance(view: dict) -> None:
    """Refuse a value no reader produced (ADR-133 D2, EXHAUSTIVE).

    Every value in the view that is not a label is a CELL `{"v", "r"}` whose `r` is a known reader id
    (`assembly` for the values assembly itself produced). The only bare things are the structural
    identifiers: the keys of the view, the label table, the reader roster, and in a tile its `id`,
    `reader`, `columns` and each field's `label` (label keys). Anything else bare is refused."""
    known = set(view.get("readers") or ())

    def cell(node, where: str) -> None:
        if not (isinstance(node, dict) and "v" in node):
            raise ProvenanceError(f"{where}: a bare value carries no reader id")
        if node.get("r") not in known:
            raise ProvenanceError(f"{where}: value {node.get('v')!r} carries reader id "
                                  f"{node.get('r')!r}, which is not a reader")

    for key in view:
        if key not in VIEW_KEYS:
            raise ProvenanceError(f"view.{key}: not a key of a view; the value has no reader")
    for key in ("schema", "assembled_at", "leg"):
        if key in view:
            cell(view[key], f"view.{key}")
    for key, value in (view.get("thresholds") or {}).items():
        cell(value, f"view.thresholds.{key}")
    for key, value in (view.get("mermaid") or {}).items():
        cell(value, f"view.mermaid.{key}")
    for i, tile in enumerate(view.get("tiles") or ()):
        where = f"view.tiles[{i}]"
        if not isinstance(tile, dict):
            raise ProvenanceError(f"{where}: a bare value carries no reader id")
        for key, value in tile.items():
            if key not in _TILE_KEYS:
                raise ProvenanceError(f"{where}.{key}: not a key of a tile; the value has no reader")
            if key in _TILE_CELLS:
                cell(value, f"{where}.{key}")
            elif key == "reason" and value is not None:
                cell(value, f"{where}.reason")
            elif key == "fields":
                for j, field in enumerate(value):
                    cell(field.get("cell") if isinstance(field, dict) else None, f"{where}.fields[{j}].cell")
            elif key == "rows":
                for r, row in enumerate(value):
                    for c, item in enumerate(row):
                        cell(item, f"{where}.rows[{r}][{c}]")


def _skipped_tile(reader: str, root: Path) -> dict:
    return _tile(reader, root, state=STATE_NOT_COMPUTED, staleness=STATE_NOT_COMPUTED, reason="leg-scheduled")


def assemble(root, *, now: datetime, leg: str = "fast", siblings: Sequence[Path] = (), map_json=None) -> dict:
    """The view dict, from organ outputs alone."""
    if leg not in LEGS:
        raise ValueError(f"leg must be one of {LEGS}, not {leg!r}")
    root = Path(root)
    tiles: list[dict] = []
    for reader in READER_IDS:
        if leg == "scheduled" and reader not in SCHEDULED_READERS:
            tiles.append(_skipped_tile(reader, root))
            continue
        try:
            tiles.extend(READERS[reader](root, now=now, siblings=tuple(siblings), map_json=map_json))
        except Exception:  # noqa: BLE001 -- a reader that raises is shown UNREADABLE, never a blank page
            tiles.append(_unreadable(reader, root, "reader-failed"))
    view = {
        "schema": _cell(SCHEMA, ASSEMBLY_ID),
        "assembled_at": _cell(now.isoformat(timespec="seconds"), ASSEMBLY_ID),
        "leg": _cell(leg, ASSEMBLY_ID),
        "labels": dict(LABELS),
        "thresholds": {key: _cell(value, ASSEMBLY_ID) for key, value in THRESHOLDS.items()},
        "readers": [*READER_IDS, ASSEMBLY_ID],
        "mermaid": {key: _cell(value, "p1-mermaid") for key, value in MERMAID.items()},
        "tiles": tiles,
    }
    check_provenance(view)
    return view


def discover_siblings(root: Path) -> list[Path]:
    """The other checkouts of this repository (`git worktree list`), whose receipts are read READ-ONLY."""
    try:
        out = subprocess.run(["git", "-C", str(root), "worktree", "list", "--porcelain"], capture_output=True,
                             text=True, encoding="utf-8", timeout=30)
    except (OSError, subprocess.SubprocessError):
        return []
    if out.returncode != 0:
        return []
    here = Path(root).resolve()
    found = []
    for line in out.stdout.splitlines():
        if line.startswith("worktree "):
            path = Path(line[len("worktree "):].strip())
            if path.is_dir() and path.resolve() != here:
                found.append(path)
    return sorted(found, key=lambda p: p.name)


# ----------------------------------------------------------------------------------------- output


def render_json(view: dict) -> bytes:
    """Canonical bytes: sorted keys, ASCII escapes, LF, trailing newline."""
    return (json.dumps(view, sort_keys=True, indent=1, ensure_ascii=True) + "\n").encode("ascii")


def _text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _shown(labels: dict, value) -> str:
    """The text a cell shows: a label-table entry when the value is a label key, else the value."""
    return labels[value] if isinstance(value, str) and value in labels else _text(value)


def _e(text: str) -> str:
    return html.escape(text, quote=True)


def _td(labels: dict, path: str, cell: dict) -> str:
    text = _e(_shown(labels, cell["v"]))
    if cell.get("src"):
        return (f'<td><q data-p="{path}.v">{text}</q> <small>{_e(labels["source_text"])}</small></td>')
    return f'<td data-p="{path}.v">{text}</td>'


def _th(labels: dict, key: str) -> str:
    return f"<th>{_e(labels[key])}</th>"


def _tile_html(labels: dict, index: int, tile: dict) -> list[str]:
    base = f"tiles.{index}"
    out = [f"<section><h2>{_e(labels['reader.' + tile['reader']])}</h2>", "<table><tbody>"]
    for key in ("source", "checkout", "state", "staleness"):
        out.append(f"<tr>{_th(labels, key)}{_td(labels, f'{base}.{key}', tile[key])}</tr>")
    if tile["reason"]:
        out.append(f"<tr>{_th(labels, 'reason')}{_td(labels, f'{base}.reason', tile['reason'])}</tr>")
    for j, field in enumerate(tile["fields"]):
        cell_path = f"{base}.fields.{j}.cell"
        if field["label"] == "diagram":
            out.append(f"<tr>{_th(labels, 'diagram')}</tr></tbody></table>")
            out.append(f'<pre data-p="{cell_path}.v">{_e(_text(field["cell"]["v"]))}</pre><table><tbody>')
            continue
        out.append(f"<tr>{_th(labels, field['label'])}{_td(labels, cell_path, field['cell'])}</tr>")
    out.append("</tbody></table>")
    if tile["rows"]:
        out.append("<table><thead><tr>" + "".join(_th(labels, c) for c in tile["columns"]) + "</tr></thead><tbody>")
        for r, row in enumerate(tile["rows"]):
            out.append("<tr>" + "".join(_td(labels, f"{base}.rows.{r}.{c}", cell)
                                        for c, cell in enumerate(row)) + "</tr>")
        out.append("</tbody></table>")
    out.append("</section>")
    return out


def render_html(view: dict) -> str:
    """ONE page from the view dict: the static rendering + the embedded snapshot + the pinned script."""
    labels = view["labels"]
    snapshot = json.dumps(view, sort_keys=True, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")
    out = [
        "<!doctype html>",
        f'<html lang="{_e(labels["lang"])}"><head><meta charset="{_e(labels["charset"])}">',
        f"<title>{_e(labels['title'])}</title>",
        f"<style>{PAGE_CSS}</style></head><body>",
        f"<h1>{_e(labels['title'])}</h1>",
        f"<table><tbody><tr>{_th(labels, 'assembled')}<td data-p=\"assembled_at.v\">"
        f"{_e(_shown(labels, view['assembled_at']['v']))}</td>{_th(labels, 'leg')}"
        f"<td data-p=\"leg.v\">{_e(_shown(labels, view['leg']['v']))}"
        "</td></tr></tbody></table>",
        f"<section><h2>{_e(labels['mermaid'])}</h2><table><tbody>",
    ]
    for key in ("library", "version", "url", "integrity"):
        out.append(f"<tr>{_th(labels, key)}{_td(labels, f'mermaid.{key}', view['mermaid'][key])}</tr>")
    out.append("</tbody></table></section>")
    for index, tile in enumerate(view["tiles"]):
        out.extend(_tile_html(labels, index, tile))
    out.append(f'<script type="{_e(labels["json_type"])}" id="{_e(labels["data_id"])}">{snapshot}</script>')
    out.append(f"<script>{PAGE_SCRIPT}</script></body></html>")
    return "\n".join(out) + "\n"


def _atomic_write(path: Path, blob: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".view-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(blob)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def write_outputs(view: dict, out_dir) -> dict:
    """Write `view.json` (atomically) and `view.html`; return both paths."""
    out = Path(out_dir)
    json_path, html_path = out / VIEW_JSON_NAME, out / VIEW_HTML_NAME
    _atomic_write(json_path, render_json(view))
    _atomic_write(html_path, render_html(view).encode("utf-8"))
    return {"json_path": json_path.as_posix(), "html_path": html_path.as_posix()}


# ------------------------------------------------------------------------------------------ pins


def _canonical(data) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=True, separators=(",", ":"))


def pin_values() -> dict:
    """The four hashes tests/fixtures/system_view/pins.json holds (labels, thresholds, script, css)."""
    def sha(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    return {"labels_sha256": sha(_canonical(LABELS)), "thresholds_sha256": sha(_canonical(THRESHOLDS)),
            "script_sha256": sha(PAGE_SCRIPT), "css_sha256": sha(PAGE_CSS)}
