#!/usr/bin/env python
"""test_flow_metrics.py -- four numbers that say whether test flow got better (lane L1, e2-test-flow-metrics).

THE GAP THIS CLOSES. Thirty earlier test efforts left no lasting result because nothing computed
an end number (`to-browser/DIGEST-TEST-EXECUTION-EVAL-2026-10-20.md` §2 Q0); `conductor.py
metrics` still prints "minutes NOT COMPUTED". This organ computes them by code, with no seat, and
`ecosystem/test-flow-ceilings.yaml` + `tests/test_test_flow_ceilings.py` turn a regression red.
It is the future answer to "how long did landing take" -- read its record, do not re-derive it.

THE FOUR NUMBERS (every one states its window, n and source in the record):
  M1  push->main wall      first conductor run on `worktree-<slug>` -> the MERGE-RECEIPTS `push-main`
                           step's `ended`; also the merge-receipt wall (closed - opened) median.
  M2  suite runs/landing   Actions jobs named `pytest*` longer than 2 min (cancelled ones included)
                           on the lane branch's runs and on the landing sha, plus the wall's `record`.
  M3  laptop reaps         Claude Code transcripts under ~/.claude/projects carrying "was stopped
                           because the system is running low on memory". LAPTOP ONLY: on Actions the
                           record says `{"available": false, ...}`, never 0.
  M4  red on main          conductor conclusions on main (push + nightly schedule), always-red job
                           names, known-reds count.

SHAPE. Pure functions take already-fetched data (unit-tested in tests/test_test_flow_metrics.py);
every `gh` call lives in the thin layer under "the gh layer". Library-first: stdlib + `gh` + `click`
and `yaml`, both already declared in pyproject.toml -- the reader posture of `ci_red_age.py` and
`organ_usage_metric.py`. Read-only against GitHub; the only write is `logs/TEST-FLOW-METRICS.jsonl`
(append-only) and an optional `--out` file.

PERSISTENCE. No scheduled job in this repo persists a record into the tree (`report-only-wall.yml`,
`substrate-heartbeat.yml` and `conductor.yml` all upload an artifact only), and CI never pushes to
`main`. So the nightly record is an ARTIFACT; the laptop ingests it with
`test_flow_metrics.py record --from-run <id>`, which is also how M3 joins the same line.
"""
from __future__ import annotations

import json
import math
import os
import re
import statistics
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Iterable, Optional

import click
import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent

SCHEMA = "test-flow-metrics/1"
REAP_PHRASE = "was stopped because the system is running low on memory"
#: M2: a job shorter than this is setup noise, not a suite run (the digest's "> 2 min").
PYTEST_MIN_SECONDS = 120
RECORDS_PATH = Path("logs") / "TEST-FLOW-METRICS.jsonl"
CEILINGS_PATH = Path("ecosystem") / "test-flow-ceilings.yaml"
RECORD_ARTIFACT = "test-flow-metrics-record"
DEFAULT_WINDOW_H = 72
CONDUCTOR = "conductor.yml"
WALL = "report-only-wall.yml"
GH_TIMEOUT_S = 180
_RUN_FIELDS = "databaseId,headSha,headBranch,conclusion,status,createdAt,updatedAt,event,url,workflowName"
_TEST_RELATED = re.compile(r"pytest|\btests?\b|suite|census", re.IGNORECASE)

CEILING_KEYS = (
    "m1_push_to_main_median_hours",
    "m2_runs_per_landing_median",
    "m3_test_related_reaps_per_3_days",
    "m4_always_red_jobs",
    "m4_main_red_rate",
    "m4_known_reds",
)


# ------------------------------------------------------------------ pure helpers

def parse_ts(value: str) -> datetime:
    """ISO 8601 (`Z` or an offset) -> tz-aware UTC."""
    dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def median(values) -> Optional[float]:
    values = list(values)
    return float(statistics.median(values)) if values else None


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _in_window(ts: str, since: str, until: str) -> bool:
    return parse_ts(since) <= parse_ts(ts) <= parse_ts(until)


def _push_main_ended(receipt: dict) -> Optional[str]:
    for step in receipt.get("steps") or []:
        if step.get("step") == "push-main" and step.get("ended"):
            return step["ended"]
    return None


def _landings(receipts: Iterable[dict], since: str, until: str) -> list[dict]:
    """In-window `merge` receipts, each with its push-main `ended` (an `arc` row is not a landing)."""
    out = []
    for r in receipts:
        if r.get("kind") != "merge":
            continue
        ended = _push_main_ended(r)
        if ended and _in_window(ended, since, until):
            out.append({"receipt": r, "ended": ended})
    return out


# ------------------------------------------------------------------ M1

def m1_push_to_main(receipts, first_run_at_by_slug, *, since, until) -> dict:
    landings, walls = [], []
    for item in _landings(receipts, since, until):
        r = item["receipt"]
        if r.get("opened") and r.get("closed"):
            walls.append((parse_ts(r["closed"]) - parse_ts(r["opened"])).total_seconds() / 60.0)
        first = first_run_at_by_slug.get(r.get("slug"))
        if first:
            hours = (parse_ts(item["ended"]) - parse_ts(first)).total_seconds() / 3600.0
            landings.append({"slug": r.get("slug"), "hours": hours})
    hours = [x["hours"] for x in landings]
    return {
        "n": len(landings),
        "median_hours": median(hours),
        "min_hours": min(hours) if hours else None,
        "max_hours": max(hours) if hours else None,
        "landings": landings,
        "merge_wall_n": len(walls),
        "merge_wall_median_minutes": median(walls),
        "window": {"since": since, "until": until},
        "source": "logs/MERGE-RECEIPTS.jsonl (kind=merge, push-main ended) + gh run list "
                  f"{CONDUCTOR} (first run on worktree-<slug>)",
    }


# ------------------------------------------------------------------ M2

def _job_seconds(job: dict) -> float:
    start, end = job.get("startedAt"), job.get("completedAt")
    if not start or not end:
        return 0.0
    return max(0.0, (parse_ts(end) - parse_ts(start)).total_seconds())


def _is_suite_job(run: dict, job: dict) -> bool:
    if _job_seconds(job) <= PYTEST_MIN_SECONDS:
        return False
    name, wf = str(job.get("name", "")), run.get("workflowName")
    return (wf == "conductor" and name.startswith("pytest")) or (wf == "report-only-wall" and name == "record")


def m2_runs_per_landing(receipts, runs, jobs_by_run, *, since, until) -> dict:
    per_landing = []
    for item in _landings(receipts, since, until):
        r = item["receipt"]
        branch, sha = f"worktree-{r.get('slug')}", r.get("merge_sha")
        seen, count = set(), 0
        for run in runs:
            rid = run.get("databaseId")
            if rid in seen or not (run.get("headBranch") == branch or (sha and run.get("headSha") == sha)):
                continue
            seen.add(rid)
            count += sum(1 for job in jobs_by_run.get(rid, []) if _is_suite_job(run, job))
        per_landing.append({"slug": r.get("slug"), "suite_runs": count})
    counts = [p["suite_runs"] for p in per_landing]
    return {
        "n": len(per_landing),
        "median": median(counts),
        "min": min(counts) if counts else None,
        "max": max(counts) if counts else None,
        "per_landing": per_landing,
        "window": {"since": since, "until": until},
        "source": f"gh run view --json jobs over {CONDUCTOR} runs on worktree-<slug> or the landing "
                  f"sha, plus {WALL} 'record' jobs; jobs named pytest* / record longer than "
                  f"{PYTEST_MIN_SECONDS} s, cancelled included",
    }


# ------------------------------------------------------------------ M3

def extract_reap_events(lines: Iterable[str], source_name: str) -> list[dict]:
    """The reaper's notice from transcript JSONL lines. `key` dedupes the same notification that a
    transcript records twice (queue entry + user message)."""
    events = []
    for number, raw in enumerate(lines, 1):
        if REAP_PHRASE not in raw:
            continue
        try:
            obj = json.loads(raw)
        except ValueError:
            continue
        if not isinstance(obj, dict) or not obj.get("timestamp"):
            continue
        # only the harness's own notice: a seat that merely quotes or greps the phrase is not a reap
        blob = next((s for s in _strings(obj) if REAP_PHRASE in s and "<task-notification>" in s), None)
        if blob is None:
            continue
        summary = re.search(r"<summary>(.*?)</summary>", blob, re.DOTALL)
        task = re.search(r"<task-id>(.*?)</task-id>", blob, re.DOTALL)
        tail = task.group(1).strip() if task else str(obj.get("uuid") or number)
        events.append({"ts": obj["timestamp"], "key": f"{source_name}:{tail}",
                       "text": summary.group(1).strip() if summary else blob})
    return events


def _strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v)


def m3_laptop_reaps(events, *, since, until) -> dict:
    seen, kept = set(), []
    for ev in events:
        if ev["key"] in seen or not _in_window(ev["ts"], since, until):
            continue
        seen.add(ev["key"])
        kept.append(ev)
    per_day: dict[str, int] = {}
    for ev in kept:
        day = parse_ts(ev["ts"]).strftime("%Y-%m-%d")
        per_day[day] = per_day.get(day, 0) + 1
    days = (parse_ts(until) - parse_ts(since)).total_seconds() / 86400.0
    return {
        "available": True,
        "total": len(kept),
        "test_related": sum(1 for ev in kept if _TEST_RELATED.search(ev["text"])),
        "per_day": dict(sorted(per_day.items())),
        "window": {"since": since, "until": until},
        "window_days": days,
        "source": "~/.claude/projects/**/*.jsonl, deduped by session + task id; test_related = "
                  "the notice's command text mentions pytest/test/suite/census",
    }


def m3_unavailable() -> dict:
    return {"available": False, "reason": "laptop transcripts"}


# ------------------------------------------------------------------ M4

def m4_red_on_main(main_runs, jobs_by_run, all_runs, *, known_reds, registry_members,
                   since, until, min_n: int = 5) -> dict:
    judged = [r for r in main_runs if r.get("conclusion") and _in_window(r["createdAt"], since, until)]
    red = [r for r in judged if r["conclusion"] != "success"]
    outcomes: dict[str, list[str]] = {}
    for run in all_runs:
        if not _in_window(run["createdAt"], since, until):
            continue
        for job in jobs_by_run.get(run.get("databaseId"), []):
            if job.get("conclusion") in ("success", "failure"):
                outcomes.setdefault(job["name"], []).append(job["conclusion"])
    always = sorted(n for n, o in outcomes.items() if len(o) >= min_n and all(c == "failure" for c in o))
    return {
        "main_judged": len(judged),
        "main_red": len(red),
        "main_red_rate": (len(red) / len(judged)) if judged else None,
        "always_red_jobs": always,
        "always_red_count": len(always),
        "known_reds": known_reds,
        "registry_members": registry_members,
        "window": {"since": since, "until": until},
        "source": f"gh run list {CONDUCTOR}, headBranch main (push + nightly schedule); jobs of every {CONDUCTOR} run in "
                  f"the window (always red = >= {min_n} judged instances, all failure); known_reds = "
                  "failed tests in the newest judged main ubuntu pytest.out; registry_members = "
                  "logs/KNOWN-REDS-REGISTRY.json",
    }


# ------------------------------------------------------------------ record

def build_record(*, now, since, until, m1, m2, m3, m4) -> dict:
    return {"schema": SCHEMA, "recorded_at": now if isinstance(now, str) else _iso(now),
            "window": {"since": since, "until": until}, "m1": m1, "m2": m2, "m3": m3, "m4": m4}


def record_line(record: dict) -> str:
    return json.dumps(record, separators=(",", ":"), sort_keys=False)


def append_record(path, record: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(record_line(record) + "\n")


# ------------------------------------------------------------------ ceilings (the ratchet)

def load_ceilings(path) -> dict:
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(doc, dict) or not isinstance(doc.get("armed"), bool):
        raise ValueError("ceilings file: `armed` must be a bool")
    ceilings = doc.get("ceilings")
    if not isinstance(ceilings, dict) or not all(
            isinstance(k, str) and isinstance(v, (int, float)) and not isinstance(v, bool)
            and math.isfinite(v) for k, v in ceilings.items()):
        raise ValueError("ceilings file: `ceilings` must map str -> number")
    return doc


def metric_value(record: dict, key: str) -> Optional[float]:
    def get(*path):
        cur = record
        for p in path:
            if not isinstance(cur, dict) or cur.get(p) is None:
                return None
            cur = cur[p]
        return cur

    if key == "m1_push_to_main_median_hours":
        return get("m1", "median_hours")
    if key == "m2_runs_per_landing_median":
        return get("m2", "median")
    if key == "m3_test_related_reaps_per_3_days":
        m3 = record.get("m3") or {}
        if not m3.get("available") or not m3.get("window_days"):
            return None
        return m3["test_related"] * 3 / m3["window_days"]
    if key == "m4_always_red_jobs":
        return get("m4", "always_red_count")
    if key == "m4_main_red_rate":
        return get("m4", "main_red_rate")
    if key == "m4_known_reds":
        return get("m4", "known_reds")
    raise KeyError(key)


def check_record(record: dict, ceilings: dict) -> list[dict]:
    findings = []
    for key, ceiling in ceilings.items():
        value = metric_value(record, key)
        state = "UNAVAILABLE" if value is None else ("RED" if value > ceiling else "OK")
        findings.append({"metric": key, "ceiling": ceiling, "value": value, "state": state})
    return findings


def raised_ceilings(current: dict, previous: dict) -> list[str]:
    return sorted(k for k, v in current.items() if k in previous and v > previous[k])


def newest_record(path) -> Optional[dict]:
    path = Path(path)
    if not path.is_file():
        return None
    lines = [ln for ln in path.read_text(encoding="utf-8").split("\n") if ln.strip()]
    if not lines:
        return None
    records = [json.loads(ln) for ln in lines]
    # latest by `recorded_at`, not by position: `record --from-run <old id>` appends an older record
    try:
        return max(records, key=lambda r: parse_ts(r["recorded_at"]))
    except (KeyError, ValueError, TypeError):
        return records[-1]


def record_is_stale(record: dict, now: datetime, max_age_days: float = 3) -> bool:
    return (now - parse_ts(record["recorded_at"])) > timedelta(days=max_age_days)


def live_check(ceilings_doc: dict, records_path, now: datetime) -> dict:
    record = newest_record(records_path)
    armed = ceilings_doc["armed"]
    if record is None:
        if armed:
            return {"ok": False, "state": "RED", "findings": [],
                    "message": "armed: true but there is no record in logs/TEST-FLOW-METRICS.jsonl"}
        return {"ok": True, "state": "UNARMED", "findings": [],
                "message": "armed: false and no record yet -- the first scheduled record is owed; "
                           "nothing to check"}
    if armed and record_is_stale(record, now):
        return {"ok": False, "state": "RED", "findings": [],
                "message": f"armed: true and the newest record ({record['recorded_at']}) is stale "
                           "(older than 3 days)"}
    findings = check_record(record, ceilings_doc["ceilings"])
    red = [f for f in findings if f["state"] == "RED"]
    if red:
        return {"ok": False, "state": "RED", "findings": findings,
                "message": "ceiling broken: " + ", ".join(
                    f"{f['metric']}={f['value']} > {f['ceiling']}" for f in red)}
    return {"ok": True, "state": "OK", "findings": findings,
            "message": f"newest record {record['recorded_at']} is within every available ceiling"}


# ------------------------------------------------------------------ the gh layer

class GhUnavailable(RuntimeError):
    """`gh` could not be run, or returned something unreadable."""


def _gh(args: list[str], *, cwd: Path = _REPO_ROOT) -> str:
    try:
        proc = subprocess.run(["gh", *args], cwd=str(cwd), capture_output=True, text=True,
                              encoding="utf-8", timeout=GH_TIMEOUT_S, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise GhUnavailable(f"gh could not be run: {exc}") from exc
    if proc.returncode != 0:
        raise GhUnavailable(f"gh {' '.join(args[:3])} exited {proc.returncode}: {proc.stderr.strip()[:200]}")
    return proc.stdout


def fetch_runs(workflow: str, *, limit: int = 500, branch: Optional[str] = None,
               event: Optional[str] = None) -> list[dict]:
    args = ["run", "list", "--workflow", workflow, "--limit", str(limit), "--json", _RUN_FIELDS]
    if branch:
        args += ["--branch", branch]
    if event:
        args += ["--event", event]
    try:
        return json.loads(_gh(args) or "[]") or []
    except ValueError as exc:
        raise GhUnavailable(f"gh returned unreadable JSON: {exc}") from exc


def fetch_jobs(run_id: int) -> list[dict]:
    try:
        return json.loads(_gh(["run", "view", str(run_id), "--json", "jobs"]) or "{}").get("jobs", [])
    except ValueError as exc:
        raise GhUnavailable(f"gh returned unreadable JSON: {exc}") from exc


def fetch_jobs_many(run_ids: Iterable[int], *, fetch: Callable = fetch_jobs) -> dict:
    """A run whose jobs cannot be read is left OUT (unknown), never recorded as having none."""
    def one(rid):
        try:
            return rid, fetch(rid)
        except GhUnavailable:
            return rid, None
    with ThreadPoolExecutor(max_workers=8) as pool:
        return {rid: jobs for rid, jobs in pool.map(one, sorted(set(run_ids))) if jobs is not None}


def failed_count_from_pytest_out(text: str) -> Optional[int]:
    # the summary line only ("38 failed, 10807 passed ... in 1029.37s"), not a stray "N failed" in a log
    hits = re.findall(r"^=*\s*(\d+) failed.* in [\d.]+s", text, re.MULTILINE)
    return int(hits[-1]) if hits else None


def latest_main_failed_count(main_runs: list[dict]) -> Optional[int]:
    """Failed tests in the newest judged main push run's ubuntu `pytest.out` artifact (the digest's
    '38 known reds'). None when no artifact can be read -- never a guess."""
    newest = sorted((r for r in main_runs if r.get("conclusion")), key=lambda r: r["createdAt"], reverse=True)
    for run in newest[:3]:                      # a bounded look: each miss is a full gh round trip
        with tempfile.TemporaryDirectory() as tmp:
            try:
                _gh(["run", "download", str(run["databaseId"]), "-n", f"pytest-ubuntu-latest-{run['headSha']}",
                     "-D", tmp])
            except GhUnavailable:
                continue
            out = Path(tmp) / "pytest.out"
            if out.is_file():
                text = out.read_text(encoding="utf-8", errors="replace")
                count = failed_count_from_pytest_out(text)
                if count is None and re.search(r"\d+ passed", text):
                    count = 0                   # a green run has no "N failed": that is 0, not unknown
                if count is not None:
                    return count
    return None


def registry_member_count(repo_root: Path) -> Optional[int]:
    path = repo_root / "logs" / "KNOWN-REDS-REGISTRY.json"
    try:
        return len(json.loads(path.read_text(encoding="utf-8")).get("members", {}))
    except (OSError, ValueError):
        return None


def load_receipts(repo_root: Path) -> list[dict]:
    path = repo_root / "logs" / "MERGE-RECEIPTS.jsonl"
    if not path.is_file():
        return []
    rows = []
    for ln in path.read_text(encoding="utf-8").split("\n"):
        if ln.strip():
            try:
                rows.append(json.loads(ln))
            except ValueError:
                continue
    return rows


def scan_transcripts(root: Path, since: str) -> list[dict]:
    """Reap notices from every transcript touched since the window opened (older files cannot hold
    an in-window notice)."""
    floor = parse_ts(since).timestamp()
    events: list[dict] = []
    if not root.is_dir():
        return events
    for path in root.rglob("*.jsonl"):
        try:
            if path.stat().st_mtime < floor:
                continue
            with path.open(encoding="utf-8", errors="replace") as fh:
                events.extend(extract_reap_events(fh, path.stem))
        except OSError:
            continue
    return events


def compute(*, repo_root: Path, since: str, until: str, laptop: Optional[bool] = None,
            now: Optional[datetime] = None) -> dict:
    """The one impure assembly: fetch, then hand everything to the pure functions."""
    now = now or datetime.now(timezone.utc)
    receipts = load_receipts(repo_root)
    conductor = fetch_runs(CONDUCTOR)
    wall = fetch_runs(WALL)
    landings = _landings(receipts, since, until)

    first_run: dict[str, str] = {}
    for run in conductor:
        branch = run.get("headBranch", "")
        if branch.startswith("worktree-"):
            slug = branch[len("worktree-"):]
            if slug not in first_run or parse_ts(run["createdAt"]) < parse_ts(first_run[slug]):
                first_run[slug] = run["createdAt"]

    wanted = set()
    for item in landings:
        r = item["receipt"]
        for run in conductor + wall:
            if run.get("headBranch") == f"worktree-{r.get('slug')}" or (
                    r.get("merge_sha") and run.get("headSha") == r["merge_sha"]):
                wanted.add(run["databaseId"])
    window_conductor = [r for r in conductor if _in_window(r["createdAt"], since, until)]
    wanted |= {r["databaseId"] for r in window_conductor}
    jobs_by_run = fetch_jobs_many(wanted)

    runs = [{**r, "workflowName": "conductor"} for r in conductor] + \
           [{**r, "workflowName": "report-only-wall"} for r in wall]
    # every conductor run on main (push AND the nightly schedule): the digest's 7-of-15 counts both
    main_runs = [r for r in window_conductor if r.get("headBranch") == "main"]

    m1 = m1_push_to_main(receipts, first_run, since=since, until=until)
    m2 = m2_runs_per_landing(receipts, runs, jobs_by_run, since=since, until=until)
    on_laptop = (os.environ.get("GITHUB_ACTIONS") != "true") if laptop is None else laptop
    m2["jobs_unread_runs"] = len(wanted) - len(jobs_by_run)   # runs whose jobs gh would not give: not "0 suite runs"
    m3 = (m3_laptop_reaps(scan_transcripts(Path.home() / ".claude" / "projects", since),
                          since=since, until=until) if on_laptop else m3_unavailable())
    m4 = m4_red_on_main(main_runs, jobs_by_run, window_conductor,
                        known_reds=latest_main_failed_count(main_runs),
                        registry_members=registry_member_count(repo_root), since=since, until=until)
    return build_record(now=now, since=since, until=until, m1=m1, m2=m2, m3=m3, m4=m4)


def ingest_run(run_id: int) -> dict:
    """The nightly record a CI run uploaded as an artifact (`record --from-run`)."""
    with tempfile.TemporaryDirectory() as tmp:
        _gh(["run", "download", str(run_id), "-n", RECORD_ARTIFACT, "-D", tmp])
        files = sorted(Path(tmp).rglob("*.json")) + sorted(Path(tmp).rglob("*.jsonl"))
        if not files:
            raise GhUnavailable(f"run {run_id} artifact {RECORD_ARTIFACT} holds no record file")
        text = files[0].read_text(encoding="utf-8")
        return json.loads([ln for ln in text.splitlines() if ln.strip()][-1])


# ------------------------------------------------------------------ CLI

def _window(since: Optional[str], until: Optional[str], now: datetime) -> tuple[str, str]:
    return (since or _iso(now - timedelta(hours=DEFAULT_WINDOW_H)), until or _iso(now))


def _options(fn):
    for opt in (click.option("--out", type=click.Path(dir_okay=False), default=None,
                             help="also write the single record JSON here (the CI artifact)"),
                click.option("--repo-root", type=click.Path(file_okay=False), default=None),
                click.option("--from-run", "from_run", type=int, default=None,
                             help="ingest the record that this Actions run uploaded, then add M3 here"),
                click.option("--until", default=None, help="window end, ISO 8601 (default: now)"),
                click.option("--since", default=None, help="window start, ISO 8601 (default: now - 72 h)")):
        fn = opt(fn)
    return fn


def _run(command: str, since, until, from_run, repo_root, out) -> None:
    root = Path(repo_root) if repo_root else _REPO_ROOT
    now = datetime.now(timezone.utc)
    try:
        if from_run is not None:
            record = ingest_run(from_run)
            if record.get("m3", {}).get("available") is False and os.environ.get("GITHUB_ACTIONS") != "true":
                w = record["window"]
                record["m3"] = m3_laptop_reaps(scan_transcripts(Path.home() / ".claude" / "projects", w["since"]),
                                               since=w["since"], until=w["until"])
        else:
            record = compute(repo_root=root, since=_window(since, until, now)[0],
                             until=_window(since, until, now)[1], now=now)
    except GhUnavailable as exc:
        click.echo(f"test_flow_metrics: {exc}", err=True)
        raise SystemExit(2)
    if command == "record":
        target = root / RECORDS_PATH
        # re-ingesting the same run must not duplicate its line
        already = from_run is not None and target.is_file() and record_line(record) in target.read_text(
            encoding="utf-8").split("\n")
        if not already:
            append_record(target, record)
    if out:
        Path(out).write_text(record_line(record) + "\n", encoding="utf-8", newline="\n")
    click.echo(record_line(record))


@click.group()
def cli() -> None:
    """Compute M1-M4 (push->main wall, suite runs per landing, laptop reaps, red on main)."""


@cli.command("compute")
@_options
def compute_cmd(since, until, from_run, repo_root, out) -> None:
    """Print one JSON line; write nothing to the tree."""
    _run("compute", since, until, from_run, repo_root, out)


@cli.command("record")
@_options
def record_cmd(since, until, from_run, repo_root, out) -> None:
    """Print one JSON line and append it to logs/TEST-FLOW-METRICS.jsonl."""
    _run("record", since, until, from_run, repo_root, out)


if __name__ == "__main__":                                   # pragma: no cover -- CLI entry
    cli()
