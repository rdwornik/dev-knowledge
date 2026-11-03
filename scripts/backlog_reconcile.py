"""The per-row backlog reconciliation organ (GO-E3.0 R10, row [#1749]).

THE RULE THE ORGAN EXISTS FOR: the operator rules on the backlog by EVIDENCE CLASS, never row by
row, and code applies only what was ruled. Everything before `apply` is evidence gathering and
classification; `apply` refuses without a ruling file and touches only the classes it names.

PIPELINE (each step a subcommand, each step's product a file in the state directory)::

    evidence    code only   open tasks/ rows -> evidence.json   (paths present/missing, work commits)
    fanout      reads       batches of 20 rows -> reads.json    (agy first, Haiku 5.5 backup,
                            a 10% Sonnet second read; EVERY read passes `read_gate.verify_read`)
    verify      code only   reads.json vs evidence.json and the batch sources it quotes
    adjudicate  Opus 5.5    only the rows still `unclear` or read-disputed -> adjudications.json
    report      code only   classification.json + the grouped markdown + the cost record
    apply       code only   `--ruling` file -> `status:` edits for the named classes only

LIBRARY-FIRST (cited per this repo's convention): the read gate is `scripts/read_gate.py`
(`run_read_gate` / `verify_read`, not re-implemented -- a read counts only when its output exists,
its log is clean and every quotation is literally in the source); rates come from
`scripts/provider_registry.py`; the CLI is Click (already a declared dependency); frontmatter is
edited as BYTES with a regex because a YAML round-trip would reflow every file it touches.

COST: every model call appends one line to `<state>/calls.jsonl`; `report` sums it. The log is
append-only for the whole run, so a re-run of a stage in the same state directory counts its
calls again: use a fresh `--state-dir` for a new run. A call whose
model has no registered rate carries `usd: null`, and the total sums PRICED calls only -- absent
and free are different facts (`provider_registry.RateUnavailable`'s rule), so the record never
reports an unpriced model as zero.

HEADLESS CLAUDE (`run_claude`): the prompt goes on STDIN (the Windows `.cmd` shim corrupts a
multi-line argv prompt), `--setting-sources local` plus a scratch cwd keep the repo's Stop hook
from eating the answer (`claude-p-json-result-is-only-the-last-message-a-stop-hook-eats-the-report`),
and the scratch directory is removed afterwards (no leftovers).
"""
from __future__ import annotations

import base64
import collections
import datetime as dt
import functools
import hashlib
import json
import logging
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence

import click
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import read_gate  # noqa: E402 -- must follow the sys.path insert above

LOG = logging.getLogger("backlog_reconcile")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TASKS_DIR = REPO_ROOT / "tasks"
DEFAULT_STATE_DIR = REPO_ROOT / "logs" / "receipts" / "backlog-reconcile"
DEFAULT_REGISTRY = REPO_ROOT / read_gate.REGISTRY_REL

EVIDENCE_CLASSES: tuple[str, ...] = ("shipped", "obsolete", "stale-refs", "live", "unclear")
ACTIONS: tuple[str, ...] = ("close", "keep", "rewrite")
VERDICTS: tuple[str, ...] = ("done", "open", "obsolete", "unclear")



def _alias_model(alias: str) -> str:
    """The registry id behind a Claude CLI alias (`opus` / `sonnet` / `haiku`), resolved at call
    time from `ecosystem/provider-registry.yaml` -- this organ carries no model-id literal
    (`tests/test_model_id_single_source.py`)."""
    import provider_registry  # noqa: PLC0415 -- sibling module, loaded only when a model is named
    return provider_registry.claude_alias_ids()[alias]

#: Paths a commit may touch without counting as WORK on a row: the bookkeeping surfaces.
BOOKKEEPING_PREFIXES = ("tasks/", "BACKLOG.md", "JOURNAL.md", "docs/audits/")

_PATH_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:py|md|yaml|yml|json|toml|ps1|sh))(?::\d+(?:-\d+)?)?`")
_PLAN_WORD_RE = re.compile(r"\b(new|create|creates|add|adds|write|writes)\b", re.IGNORECASE)
_FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?\r?\n)---[ \t]*\r?\n", re.DOTALL)
#: `status: open` as `load_open_rows` selects it (optionally quoted), so `apply` edits what it selected.
_STATUS_OPEN_RE = re.compile(r"(?m)^status:[ \t]*[\"']?open[\"']?[ \t]*(\r?\n)")
_READ_LINE_RE = re.compile(
    r"^\s*\[?#?(\d+)\]?\s*\|\s*(done|open|obsolete|unclear)\s*\|\s*[\"“](.+)[\"”]\s*$"
)
_ADJ_LINE_RE = re.compile(r"^\s*\[?#?(\d+)\]?\s*\|\s*([a-z-]+)\s*\|\s*(.*?)\s*$")


class UngatedReadError(RuntimeError):
    """A read the gate did not accept. Raised, never degraded: an ungated read must not become
    a verdict in `reads.json` (GO-E3.0 R10 -- "fanout refuses an ungated read")."""


# --- rows ----------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Row:
    id: str
    path: Path
    title: str
    body: str


def _frontmatter_value(front: str, key: str) -> Optional[str]:
    match = re.search(rf"^{re.escape(key)}:[ \t]*(.*?)[ \t]*\r?$", front, re.MULTILINE)
    if not match:
        return None
    value = match.group(1)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def load_open_rows(tasks_dir: Path) -> list[Row]:
    """Every `*.md` under `tasks_dir` whose frontmatter reads `status: open`, by integer id."""
    rows: list[Row] = []
    for path in Path(tasks_dir).glob("*.md"):
        text = path.read_text(encoding="utf-8")
        match = _FRONTMATTER_RE.match(text)
        if not match:
            continue
        front = match.group(1)
        if _frontmatter_value(front, "status") != "open":
            continue
        raw_id = _frontmatter_value(front, "id") or path.name.split("-", 1)[0]
        digits = re.sub(r"\D", "", raw_id)
        if not digits:
            LOG.warning("task file %s has no numeric id; skipped", path.name)
            continue
        title = _frontmatter_value(front, "title") or path.stem
        rows.append(Row(digits, path, title, text[match.end():].strip()))
    return sorted(rows, key=lambda r: int(r.id))


# --- evidence ------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Commit:
    sha: str
    paths: tuple[str, ...]
    message: str


def read_commit_log(path: Path) -> list[Commit]:
    """`<sha><TAB><comma-separated-changed-paths><TAB><message>` per line (the test seam)."""
    commits = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        parts = line.split("\t", 2)
        if len(parts) < 3:
            continue
        paths = tuple(p for p in parts[1].split(",") if p)
        commits.append(Commit(parts[0], paths, parts[2]))
    return commits


def git_commit_index(repo_root: Path) -> list[Commit]:
    """Every non-merge commit with its changed paths, from one `git log` pass."""
    proc = subprocess.run(
        ["git", "log", "--no-merges", "--name-only",
         "--format=%x1e%H%x1f%s%x1f%b%x1f"],
        cwd=str(repo_root), capture_output=True, text=True, encoding="utf-8",
        errors="replace", check=True,
    )
    commits = []
    for chunk in proc.stdout.split("\x1e"):
        if not chunk.strip():
            continue
        sha, subject, body, files = (chunk.split("\x1f") + ["", "", "", ""])[:4]
        paths = tuple(p.strip() for p in files.splitlines() if p.strip())
        commits.append(Commit(sha.strip(), paths, f"{subject}\n{body}"))
    return commits


def work_commit_counts(commits: Sequence[Commit]) -> dict[str, int]:
    """id -> commits whose message names `[#id]` and that changed a path outside the
    bookkeeping surfaces. A commit that only files, edits or journals a row is not work."""
    counts: dict[str, int] = {}
    for commit in commits:
        if not any(not p.startswith(BOOKKEEPING_PREFIXES) for p in commit.paths):
            continue
        for found in set(re.findall(r"\[#(\d+)\]", commit.message)):
            counts[found] = counts.get(found, 0) + 1
    return counts


def referenced_paths(body: str) -> list[tuple[str, bool]]:
    """(path, planned) for each backticked repo path in a row body, first appearance order.
    `planned` is True for a path in a `touches:` clause or one introduced by "new/add/create":
    the row asks for it to be CREATED, so its absence is the open work, not a stale reference."""
    found: list[tuple[str, bool]] = []
    seen: set[str] = set()
    for segment in re.split(r"\s·\s", body):
        in_touches = segment.lstrip().lower().startswith("touches:")
        for match in _PATH_RE.finditer(segment):
            path = match.group(1)
            if path.startswith("/") or ".." in path or path in seen:
                continue
            seen.add(path)
            lead = segment[max(0, match.start() - 40):match.start()]
            found.append((path, in_touches or bool(_PLAN_WORD_RE.search(lead))))
    return found


def collect_evidence(row: Row, *, repo_root: Path, work_commits: int) -> dict[str, Any]:
    present: list[str] = []
    missing: list[str] = []
    for path, planned in referenced_paths(row.body):
        exists = (Path(repo_root) / path).exists()
        if exists:
            present.append(path)
        elif "/" in path and not planned:
            missing.append(path)  # a bare name that is absent at the root is ambiguous: skipped
    return {"paths_present": present, "paths_missing": missing, "work_commits": work_commits}


def classify(evidence: dict[str, Any], read_verdict: Optional[str],
             adjudicated: Optional[str]) -> str:
    """The evidence class of one row; the rule order is the contract (see module tests)."""
    if adjudicated is not None:
        if adjudicated not in EVIDENCE_CLASSES:
            raise ValueError(f"adjudicated class {adjudicated!r} is not one of {EVIDENCE_CLASSES}")
        return adjudicated
    present = evidence.get("paths_present") or []
    missing = evidence.get("paths_missing") or []
    commits = evidence.get("work_commits") or 0
    if read_verdict == "done" and (commits > 0 or (present and not missing)):
        return "shipped"
    if read_verdict == "obsolete" and missing:
        return "obsolete"
    if read_verdict == "open":
        return "stale-refs" if missing else "live"
    if read_verdict is None and missing and not present:
        return "stale-refs"
    return "unclear"


# --- state files and the cost log ----------------------------------------------------------------

#: Where `record_call` appends; set by the commands that call a model.
_CALLS_PATH: Optional[Path] = None


def _read_json(path: Path, default: Any = None) -> Any:
    if not Path(path).exists():
        return default
    return json.loads(Path(path).read_text(encoding="utf-8"))


SNAPSHOT_NAME = "classification-sha.json"


def _file_sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _write_json(path: Path, data: Any) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                          encoding="utf-8", newline="\n")


def record_call(model: str, stage: str, input_tokens: int, output_tokens: int,
                usd: Optional[float]) -> None:
    if _CALLS_PATH is None:
        return
    _CALLS_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = {"model": model, "stage": stage, "input_tokens": int(input_tokens),
            "output_tokens": int(output_tokens), "usd": usd}
    with _CALLS_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(line, ensure_ascii=False, sort_keys=True) + "\n")


def cost_record(calls_path: Path) -> dict[str, Any]:
    """{calls, input_tokens, output_tokens, usd, by_model} from `calls.jsonl`. `usd` sums the
    priced calls; a model with no priced call reports `usd: null` in `by_model`."""
    total = {"calls": 0, "input_tokens": 0, "output_tokens": 0, "usd": 0.0, "by_model": {}}
    if not Path(calls_path).exists():
        return total
    for raw in Path(calls_path).read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        call = json.loads(raw)
        entry = total["by_model"].setdefault(
            call["model"], {"calls": 0, "input_tokens": 0, "output_tokens": 0, "usd": None})
        for target in (total, entry):
            target["calls"] += 1
            target["input_tokens"] += call["input_tokens"]
            target["output_tokens"] += call["output_tokens"]
        if call.get("usd") is not None:
            total["usd"] += call["usd"]
            entry["usd"] = (entry["usd"] or 0.0) + call["usd"]
    return total


# --- the reads: gated fan-out --------------------------------------------------------------------


def _plain(text: str, limit: int = 900) -> str:
    """One quote-safe line: markdown marks and double quotes would break the gate's quotation
    pairing, so the batch SOURCE is plain text and the reader quotes from it literally."""
    text = re.sub(r"[`*]", "", text).replace('"', "'").replace("“", "'").replace("”", "'")
    return re.sub(r"\s+", " ", text).strip()[:limit]


def _batch_line(row: Row, evidence: Optional[dict[str, Any]]) -> str:
    line = f"[#{row.id}] {_plain(row.title, 200)} :: {_plain(row.body)}"
    if evidence:
        line += (f" || evidence: commits={evidence.get('work_commits', 0)} "
                 f"paths-present={len(evidence.get('paths_present', []))} "
                 f"paths-missing={len(evidence.get('paths_missing', []))}")
    return line


def parse_read_output(text: str) -> dict[str, tuple[str, str]]:
    """`<id> | <verdict> | "<quote>"` lines -> {id: (verdict, quote)}; other lines ignored."""
    parsed: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        match = _READ_LINE_RE.match(line)
        if match:
            parsed[match.group(1)] = (match.group(2), match.group(3))
    return parsed


@dataclass
class FanoutResult:
    reads: dict[str, dict[str, Any]] = field(default_factory=dict)
    batches: int = 0
    second_read_ids: list[str] = field(default_factory=list)


def _sample_ids(ids: Sequence[str], fraction: float) -> list[str]:
    if not ids or fraction <= 0:
        return []
    step = max(1, math.ceil(1 / fraction))
    return [i for n, i in enumerate(sorted(ids, key=int)) if n % step == 0]


def run_fanout(rows: Sequence[Row], *, invoke: read_gate.Invoker, state_dir: Path,
               registry_path: Path, batch_size: int = 20, sample_fraction: float = 0.10,
               second_invoke: Optional[Callable[[Path, Path], read_gate.InvokeAttempt]] = None
               ) -> FanoutResult:
    """Read `rows` in batches through the read gate. Any batch the gate does not accept raises
    `UngatedReadError` and NOTHING is written to `reads.json`."""
    state_dir = Path(state_dir)
    evidence = _read_json(state_dir / "evidence.json", {})
    batch_dir = state_dir / "batches"
    batch_dir.mkdir(parents=True, exist_ok=True)
    sampled = set(_sample_ids([r.id for r in rows], sample_fraction)) if second_invoke else set()
    ledger = state_dir / "read-outcomes.jsonl"
    result = FanoutResult()
    for number, start in enumerate(range(0, len(rows), batch_size), start=1):
        batch = list(rows[start:start + batch_size])
        source = batch_dir / f"batch-{number:03d}.md"
        source.write_text("\n".join(_batch_line(r, evidence.get(r.id)) for r in batch) + "\n",
                          encoding="utf-8", newline="\n")
        workdir = state_dir / "work" / f"batch-{number:03d}"
        workdir.mkdir(parents=True, exist_ok=True)
        gated = read_gate.run_read_gate(source, registry_path=Path(registry_path), invoke=invoke,
                                        workdir=workdir, ledger_path=ledger)
        if not gated.accepted or gated.output_path is None:
            raise UngatedReadError(f"batch {number:03d} refused: {gated.failure_summary()}")
        parsed = parse_read_output(gated.output_path.read_text(encoding="utf-8"))
        omitted = [r.id for r in batch if r.id not in parsed]
        if omitted:
            # A gated read that answers 1 of 20 lines is not a read of the batch: refuse it
            # rather than record the omitted rows as a verdict nobody gave.
            raise UngatedReadError(
                f"batch {number:03d} read omitted {len(omitted)} of {len(batch)} rows "
                f"(first: {', '.join(omitted[:5])})")
        for row in batch:
            verdict, quote = parsed[row.id]
            result.reads[row.id] = {"verdict": verdict, "quote": quote,
                                    "route": gated.served_route}
        result.batches += 1
        batch_sampled = [r.id for r in batch if r.id in sampled]
        if second_invoke and batch_sampled:
            second_source = batch_dir / f"sample-{number:03d}.md"
            second_source.write_text(
                "\n".join(_batch_line(r, evidence.get(r.id)) for r in batch
                          if r.id in sampled) + "\n", encoding="utf-8", newline="\n")
            attempt = second_invoke(second_source, workdir)
            verdict = read_gate.verify_read(attempt.output_path, attempt.log_text,
                                            second_source.read_text(encoding="utf-8"))
            if not verdict.accepted:
                raise UngatedReadError(
                    f"second read of batch {number:03d} refused: {verdict.failed_check}")
            second = parse_read_output(attempt.output_path.read_text(encoding="utf-8"))
            omitted_second = [i for i in batch_sampled if i not in second]
            if omitted_second:
                raise UngatedReadError(
                    f"second read of batch {number:03d} omitted sampled rows: "
                    f"{', '.join(omitted_second)}")
            for row_id in batch_sampled:
                result.reads[row_id]["second_read"] = (
                    "agree" if second[row_id][0] == result.reads[row_id]["verdict"]
                    else "disagree")
                result.second_read_ids.append(row_id)
    _write_json(state_dir / "reads.json", result.reads)
    return result


# --- the real model hooks (never reached by a test) -----------------------------------------------


def claude_argv(model: str, prompt: str) -> list[str]:
    """argv of the headless session; GO-E3.0 R2 puts the disallowed-tools token on every one."""
    return ["claude", "-p", "--model", model, "--output-format", "json",
            "--setting-sources", "local", "--disallowedTools=AskUserQuestion,advisor", prompt]


def run_claude(model: str, prompt: str, *, timeout_s: int = 900) -> dict[str, Any]:
    """One headless `claude -p` call. Prompt on stdin; returns text, token counts (cache reads
    and writes counted as input), the CLI's own USD figure and the SERVED model id."""
    argv = claude_argv(model, "")[:-1]
    argv[0] = shutil.which("claude") or "claude"
    scratch = Path(tempfile.mkdtemp(prefix="backlog-reconcile-"))
    try:
        proc = subprocess.run(argv, input=prompt, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout_s,
                              cwd=str(scratch), check=False)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"claude -p returned non-JSON (exit {proc.returncode}): "
                           f"{proc.stdout[:200]!r} {proc.stderr[:200]!r}") from exc
    if data.get("is_error"):
        raise RuntimeError(f"claude -p reported an error: {str(data.get('result'))[:300]}")
    usage = data.get("usage") or {}
    served = next(iter(data.get("modelUsage") or {}), model)
    return {
        "text": data.get("result") or "",
        "input_tokens": int(usage.get("input_tokens", 0))
        + int(usage.get("cache_creation_input_tokens", 0))
        + int(usage.get("cache_read_input_tokens", 0)),
        "output_tokens": int(usage.get("output_tokens", 0)),
        "usd": data.get("total_cost_usd"),
        "model": served,
    }


_READ_PROMPT = (
    "You are the read stage of a backlog reconciliation. Each line below is one OPEN backlog "
    "row: `[#id] title :: text`, sometimes followed by `|| evidence:` counts computed by code "
    "(commits that touched code naming the row, referenced paths that exist / are missing).\n"
    "For EVERY line output exactly one line `<id> | <verdict> | \"<quote>\"` and nothing else, "
    "where <id> is the digits only, <verdict> is one of: done (the row's Done-when looks "
    "delivered), open (still to do and its targets still exist), obsolete (superseded or its "
    "targets are gone), unclear (cannot tell); and <quote> is a phrase copied VERBATIM, "
    "character for character, from that line. Never paraphrase inside the quotation marks.\n\n"
)


def _read_prompt(source_text: str) -> str:
    return _READ_PROMPT + source_text


def _write_claude_read(model: str, stage: str, source: Path, output: Path) -> read_gate.InvokeAttempt:
    reply = run_claude(model, _read_prompt(source.read_text(encoding="utf-8")))
    record_call(reply["model"], stage, reply["input_tokens"], reply["output_tokens"],
                reply["usd"])
    output.write_text(reply["text"], encoding="utf-8", newline="\n")
    return read_gate.InvokeAttempt(output, status="success")


def _agy_read(source: Path, output: Path) -> read_gate.InvokeAttempt:
    source_abs = source.resolve()
    prompt = (_READ_PROMPT + f"Read exactly this file and nothing else: {source_abs}. "
              f"Write your answer to exactly this path and no other: {output.resolve()}. "
              "Do not modify, move, or write to any other file.")
    built = read_gate._agy_argv(prompt, output.resolve(), source_abs)
    refusal = read_gate.agy_argv_refusal(built)
    if refusal:
        return read_gate.InvokeAttempt(None, log_text=refusal, status="refused")
    try:
        proc = subprocess.run([read_gate._npm_shim("agy"), *built], capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=900,
                              stdin=subprocess.DEVNULL, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        return read_gate.InvokeAttempt(None, log_text=str(exc), status="unavailable")
    usage = _agy_usage(proc.stdout or "")
    record_call(usage["model"], "read", usage["input_tokens"], usage["output_tokens"], None)
    return read_gate.InvokeAttempt(output if output.exists() else None,
                                   log_text=(proc.stdout or "") + "\n" + (proc.stderr or ""),
                                   status=f"exit={proc.returncode}")


def _agy_usage(stdout: str) -> dict[str, Any]:
    """Best-effort token counts from `agy --output-format json`; 0 when the shape lacks them."""
    # agy reports no served-model id in its JSON (probed 2026-11-01, agy 1.4.12), so the label
    # says so rather than naming a Gemini version nobody verified.
    out = {"model": "antigravity-agy (served model not reported)", "input_tokens": 0,
           "output_tokens": 0}
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return out

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                lowered = key.lower()
                if isinstance(value, (int, float)) and "token" in lowered:
                    if "input" in lowered or "prompt" in lowered or "cache" in lowered:
                        out["input_tokens"] += int(value)
                    elif any(w in lowered for w in ("output", "candidate", "completion", "thinking")):
                        out["output_tokens"] += int(value)
                elif lowered in ("model", "modelname", "model_name") and isinstance(value, str):
                    out["model"] = value
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return out


def default_invoke(route: read_gate.RouteSpec, source_path: Path,
                   workdir: Path) -> read_gate.InvokeAttempt:
    """The real first-read hook: agy (Gemini) first, Haiku 5.5 as the registry's second route."""
    output = (workdir / f"{route.provider}.output.txt").resolve()
    output.unlink(missing_ok=True)
    if route.provider == "antigravity":
        return _agy_read(source_path, output)
    if route.provider == "anthropic":
        return _write_claude_read(route.model or _alias_model("haiku"), "read-backup",
                                  source_path, output)
    raise read_gate.ReadGateError(f"no backlog-reconcile invoker for route {route.provider!r}")


def default_second_invoke(source_path: Path, workdir: Path) -> read_gate.InvokeAttempt:
    """The 10% second read, Sonnet 5.5."""
    output = (workdir / "second.output.txt").resolve()
    output.unlink(missing_ok=True)
    return _write_claude_read(_alias_model("sonnet"), "second-read", source_path, output)


# --- adjudication --------------------------------------------------------------------------------


def _adjudication_targets(evidence: dict, reads: dict) -> list[str]:
    targets = []
    for row_id in sorted(evidence, key=int):
        read = reads.get(row_id, {})
        verdict = read.get("verdict")
        if classify(evidence[row_id], verdict, None) == "unclear" \
                or read.get("second_read") == "disagree":
            targets.append(row_id)
    return targets


def _adjudication_prompt(targets: Sequence[str], evidence: dict, reads: dict,
                         bodies: dict[str, str]) -> str:
    lines = [
        "You adjudicate backlog rows the cheap readers could not settle. For each row below "
        "answer with exactly one line `<id> | <class> | <one-sentence reason>` and nothing "
        f"else, where <class> is one of: {', '.join(EVIDENCE_CLASSES)}. shipped = delivered; "
        "obsolete = superseded or its targets are gone; stale-refs = still wanted but its "
        "references are dead and the row needs rewriting; live = still open as written; "
        "unclear = you genuinely cannot tell.\n"
    ]
    for row_id in targets:
        ev, read = evidence[row_id], reads.get(row_id, {})
        lines.append(
            f"{row_id} | read={read.get('verdict', 'none')} second-read="
            f"{read.get('second_read', 'none')} commits={ev.get('work_commits', 0)} "
            f"present={ev.get('paths_present', [])} missing={ev.get('paths_missing', [])} "
            f"quote={read.get('quote', '')!r} text={bodies.get(row_id, '')!r}")
    return "\n".join(lines)


def parse_adjudication(text: str, allowed: Sequence[str]) -> tuple[dict[str, dict], list[str]]:
    accepted: dict[str, dict] = {}
    dropped: list[str] = []
    for line in text.splitlines():
        match = _ADJ_LINE_RE.match(line)
        if not match:
            continue
        row_id, klass, reason = match.groups()
        if row_id in allowed and klass in EVIDENCE_CLASSES:
            accepted[row_id] = {"class": klass, "reason": reason}
        else:
            dropped.append(f"{row_id} | {klass}")
    return accepted, dropped


# --- apply ---------------------------------------------------------------------------------------


class RulingError(click.ClickException):
    """A ruling the organ refuses; `apply` has changed nothing when this is raised."""


def load_ruling(path: Path) -> dict[str, str]:
    """Validate the ruling file and return `{class: action}`. Raises `RulingError`."""
    if not Path(path).is_file():
        raise RulingError(f"ruling file not found: {path}")
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise RulingError(f"ruling is not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise RulingError("ruling must be a mapping {ruled_by, ruled_on, classes}")
    if data.get("ruled_by") != "operator":
        raise RulingError("ruling.ruled_by must be exactly 'operator'")
    ruled_on = data.get("ruled_on")
    if isinstance(ruled_on, dt.datetime) or not (
            isinstance(ruled_on, dt.date) or _is_iso_date(ruled_on)):
        raise RulingError("ruling.ruled_on must be an ISO date (YYYY-MM-DD)")
    classes = data.get("classes")
    if not isinstance(classes, dict) or not classes:
        raise RulingError("ruling.classes must be a non-empty mapping {class: action}")
    for klass, action in classes.items():
        if klass not in EVIDENCE_CLASSES:
            raise RulingError(
                f"ruling names unknown evidence class {klass!r}; known: {', '.join(EVIDENCE_CLASSES)}")
        if action not in ACTIONS:
            raise RulingError(f"ruling action {action!r} for class {klass!r} is not one of "
                              f"{', '.join(ACTIONS)}")
    return dict(classes)


def _is_iso_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def apply_action(path: Path, action: str) -> bool:
    """Edit one task file's frontmatter as bytes; True when the file changed."""
    raw = path.read_bytes().decode("utf-8")
    match = _FRONTMATTER_RE.match(raw)
    if not match or action == "keep":
        return False
    front = match.group(1)
    if action == "close":
        new_front, n = _STATUS_OPEN_RE.subn(r"status: closed\1", front, count=1)
    else:  # rewrite
        if re.search(r"(?m)^reconcile: rewrite\r?$", front):
            return False
        new_front, n = _STATUS_OPEN_RE.subn(r"status: open\1reconcile: rewrite\1", front, count=1)
    if not n:
        return False
    path.write_bytes((raw[:match.start(1)] + new_front + raw[match.end(1):]).encode("utf-8"))
    return True


# --- the legacy sweep (GO-E3.0 night sweep, row [#1854]) -----------------------------------------
#
# SEPARATE from the five-evidence-class `apply --ruling` above (`EVIDENCE_CLASSES` is unchanged).
# `apply --sweep` closes OLD rows (git add-date before the cutoff) unless a KEEP witness holds, and
# takes the step-2 R-1..R-3 rule for newer rows; `apply --revert` reopens any class from the sweep's
# own ledger, byte for byte. Library-first: the close itself is `gen_task_tree.close_row_plan`
# (called, never re-implemented); git is the only source of ages and recency.

SWEEP_CUTOFF = dt.date(2026, 10, 1)
K2_WINDOW_DAYS = 30
LEGACY_CLASS = "legacy-sweep"
SWEEP_DECISION_CLASSES: tuple[str, ...] = (
    "close-shipped", "close-obsolete", "close-duplicate", "close-no-fit", "close-parked",
    "keep-P1", "keep-P2", "keep-P3", "merge-rewrite",
)
#: Rows a live lane files, builds or closes (contract Outcome (7)); the sweep never closes them.
FIXED_LIVE_IDS: frozenset[str] = frozenset(
    str(n) for n in (1572, 1633, 1748, 1800, 1811, 1833, 1837, 1838, *range(1844, 1864)))
SWEEP_LEDGER = "ledger.json"
# A dated name: consumer_at_landing counts a docs/audits file as consumed only when a governance
# surface cites a DATED name, so a file called index.md could never be consumed (Q-SW-2 (e)).
SWEEP_INDEX = "2026-11-02-technical-backlog-night-sweep-index.md"
R2_REFUSED_LINE = "R-2 refused: no adjudicated unique-content flag"
KEPT_CATEGORIES: tuple[str, ...] = (
    "protected", "k2-alive", "k3-agreed", "live-excluded", "r2-refused", "absent-from-table",
    "ungated", "unknown-decision-class", "merge-rewrite", "keep-class", "no-add-date",
    "archived-body", "duplicate-of-kept")
DEFAULT_SWEEP_HOME = REPO_ROOT / "docs" / "audits" / "2026-11-02-technical-backlog-night-sweep"
DEFAULT_TRANSPORT_ROOT = Path(os.environ.get("CLAUDE_PROMPTS_DIR") or "H:/My Drive/CLAUDE PROMPT DIR")

_CITE_RE = re.compile(r"(?<![\w/&])#(\d+)\b")
_ADR_ACCEPTED_RE = re.compile(r"(?mi)^[-*\s]*\*{0,2}status:?\*{0,2}:?\s*\*{0,2}\s*accepted")


class SweepError(click.ClickException):
    """A sweep or revert the organ refuses; nothing was written when this is raised."""


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(repo_root), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=False)


def _dates_of(proc: subprocess.CompletedProcess) -> list[dt.date]:
    return [dt.date.fromisoformat(line.strip()[:10])
            for line in proc.stdout.splitlines() if line.strip()]


def task_add_date(repo_root: Path, rel_path: str, ref: str = "HEAD") -> dt.date:
    """The OLDEST author date among the commits that ADD `rel_path` along its rename history
    (`git log --follow --diff-filter=A`): a renamed file keeps the age of its first name.

    A file that entered the tree inside a merge commit has no `A` entry under `--follow`; its age
    is then the oldest commit touching any `<dir>/<id>-*` path (the id prefix survives a rename),
    which is the contract's "oldest commit touching any of its paths"."""
    proc = _git(repo_root, "log", "--follow", "--diff-filter=A", "--format=%aI", ref, "--",
                rel_path)
    dates = _dates_of(proc)
    if not dates:
        rel = rel_path.replace("\\", "/")
        head, _, name = rel.rpartition("/")
        found = re.match(r"(\d+)-", name)
        if found:
            pattern = f"{head}/{found.group(1)}-*" if head else f"{found.group(1)}-*"
            dates = _dates_of(_git(repo_root, "log", "--format=%aI", ref, "--", pattern))
    if not dates:
        raise SweepError(f"no add-date for {rel_path} on {ref}: {proc.stderr.strip()[:200]}")
    return min(dates)


@functools.lru_cache(maxsize=512)
def _cited_ids_cached(text: str) -> frozenset[str]:
    return frozenset(_CITE_RE.findall(text))


def cited_ids(text: str) -> set[str]:
    """Ids cited as `[#123]` or `#123` (digits, as str)."""
    return set(_cited_ids_cached(text))


def k1_protected(row_id: str, *, source_texts: Mapping[str, str],
                 cited_by_open: Sequence) -> list[str]:
    """K1 / R-1: the witnesses that protect the row -- each source naming it, plus
    `cited_by_open` when an open row cites it. Empty = not protected."""
    held = [name for name, text in source_texts.items() if str(row_id) in _cited_ids_cached(text)]
    if cited_by_open:
        held.append("cited_by_open")
    return held


def k2_alive(body: str, *, repo_root: Path, ref: str, today: dt.date,
             window_days: int = K2_WINDOW_DAYS) -> list[str]:
    """K2: repo paths the row names that exist on `ref` AND were committed to within the window."""
    floor = today - dt.timedelta(days=window_days)
    alive: list[str] = []
    for path, _planned in referenced_paths(body):
        if path.startswith(BOOKKEEPING_PREFIXES):
            continue
        for cand in ([path] if "/" in path else [path, f"scripts/{path}"]):
            if _git(repo_root, "cat-file", "-e", f"{ref}:{cand}").returncode != 0:
                continue
            stamp = _git(repo_root, "log", "-1", "--format=%cI", ref, "--", cand).stdout.strip()
            if stamp and dt.date.fromisoformat(stamp[:10]) >= floor:
                alive.append(cand)
            break
    return alive


def k3_agreed(table_row: Mapping) -> bool:
    """K3: both step-1 families say LINE with P1/P2, agreed (never adjudicated)."""
    if table_row.get("label_basis") != "agreed" or table_row.get("adjudicator_followed"):
        return False
    for family in ("sonnet", "gemini"):
        label = table_row.get(family) or {}
        if label.get("fit") != "LINE" or label.get("priority") not in ("P1", "P2"):
            return False
    return True


def live_lane_ids(repo_root: Path, *, transport_root: Path,
                  main_ref: str = "origin/main") -> dict[str, str]:
    """id -> reason for every row a live lane files, builds or closes (contract Outcome (7))."""
    live: dict[str, str] = {i: "fixed live-lane set" for i in FIXED_LIVE_IDS}
    slugs: set[str] = set()
    worktrees = _git(repo_root, "worktree", "list", "--porcelain").stdout
    for match in re.finditer(r"(?m)^worktree (.+)$", worktrees):
        norm = match.group(1).replace("\\", "/")
        if "/.claude/worktrees/" in norm:
            slugs.add(norm.rsplit("/.claude/worktrees/", 1)[1].strip("/"))
    for prefix in ("refs/remotes/origin/worktree-", "refs/remotes/origin/integrate-"):
        refs = _git(repo_root, "for-each-ref", "--format=%(refname)", prefix + "*").stdout.split()
        for ref in refs:
            diff = _git(repo_root, "diff", "--name-only", f"{main_ref}...{ref}", "--", "tasks/")
            for name in diff.stdout.splitlines():
                found = re.match(r"tasks/(\d+)-", name.strip())
                if found:
                    live.setdefault(found.group(1), f"task file differs on {ref}")
            if prefix.endswith("worktree-"):
                merged = _git(repo_root, "merge-base", "--is-ancestor", ref, main_ref).returncode
                if merged != 0:
                    slugs.add(ref[len(prefix):])
    for slug in sorted(slugs):
        lane = Path(transport_root) / f"LANE-{slug}.md"
        if lane.is_file():
            for found in cited_ids(lane.read_text(encoding="utf-8", errors="replace")):
                live.setdefault(found, f"cited in the contract of live lane {slug}")
    return live


# --- the sweep ruling and the step-1 table --------------------------------------------------------


def load_sweep_ruling(path: Path) -> dict[str, Any]:
    """The sweep half of a ruling file. `load_ruling` still validates the shared schema; this adds
    the `sweep:` block and proves `text` is the file `source_sha256` names."""
    load_ruling(path)
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    text, digest = data.get("text"), data.get("source_sha256")
    if not isinstance(text, str) or not isinstance(digest, str):
        raise RulingError("sweep ruling needs `text` and `source_sha256`")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != digest:
        raise RulingError("ruling.text does not hash to ruling.source_sha256")
    sweep = data.get("sweep")
    if not isinstance(sweep, dict):
        raise RulingError("ruling.sweep must be a mapping")
    cutoff = sweep.get("cutoff")
    if not isinstance(cutoff, dt.date) and not _is_iso_date(cutoff):
        raise RulingError("ruling.sweep.cutoff must be an ISO date")
    if isinstance(cutoff, str):
        cutoff = dt.date.fromisoformat(cutoff)
    window = sweep.get("k2_window_days", K2_WINDOW_DAYS)
    if not isinstance(window, int) or window < 0:
        raise RulingError("ruling.sweep.k2_window_days must be a non-negative integer")
    sources = sweep.get("k1_sources")
    if not isinstance(sources, list):
        raise RulingError("ruling.sweep.k1_sources must be a list")
    for source in sources:
        if not isinstance(source, dict) or source.get("root") not in ("repo", "transport") \
                or not (isinstance(source.get("path"), str) or isinstance(source.get("glob"), str)):
            raise RulingError(f"bad k1_sources entry: {source!r}")
    classes = sweep.get("decision_classes")
    if not isinstance(classes, dict) or not classes:
        raise RulingError("ruling.sweep.decision_classes must be a non-empty mapping")
    for key, label in classes.items():
        if key not in SWEEP_DECISION_CLASSES:
            raise RulingError(f"ruling names unknown decision class {key!r}")
        if not isinstance(label, str) or not label:
            raise RulingError(f"decision class {key!r} needs a class label or 'keep'")
    return {"cutoff": cutoff, "k2_window_days": window,
            "legacy_class": sweep.get("legacy_class", LEGACY_CLASS),
            "k1_sources": [dict(s) for s in sources], "decision_classes": dict(classes),
            "text": text, "source_sha256": digest}


def load_step1_table(path: Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = data.get("rows") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        raise SweepError(f"step-1 table {path} has no `rows` list")
    return rows


def _read_k1_sources(ruling: dict[str, Any], repo_root: Path, transport_root: Path) -> dict[str, str]:
    texts: dict[str, str] = {}
    for source in ruling["k1_sources"]:
        root = Path(repo_root if source["root"] == "repo" else transport_root)
        if "glob" in source:
            paths = sorted(root.glob(source["glob"]))
            if not paths:
                raise SweepError(f"k1 source glob matched nothing: {source['glob']}")
        else:
            paths = [root / source["path"]]
        for path in paths:
            if not path.is_file():
                raise SweepError(f"k1 source not found (fail closed): {path}")
            text = path.read_text(encoding="utf-8", errors="replace")
            if source.get("requires_status") == "Accepted" and not _ADR_ACCEPTED_RE.search(text):
                continue  # an ADR that is not Accepted protects nothing
            texts[f"{source['root']}:{path.relative_to(root).as_posix()}"] = text
    return texts


# --- the atomic pair write ------------------------------------------------------------------------


def _atomic_write_all(writes: Sequence[tuple[Path, bytes]]) -> None:
    """Write every (path, bytes) or none: temp files first, then `os.replace` each; a failed
    replace restores the files already replaced and removes every temp file."""
    temps: list[Path] = []
    originals: list[tuple[Path, Optional[bytes]]] = []
    try:
        for path, data in writes:
            tmp = path.with_name(path.name + ".sweep-tmp")
            tmp.write_bytes(data)
            temps.append(tmp)
        for (path, _data), tmp in zip(writes, temps):
            originals.append((path, path.read_bytes() if path.exists() else None))
            os.replace(tmp, path)
    except BaseException:
        for path, original in reversed(originals):
            try:
                if original is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(original)
            except OSError:
                LOG.error("ROLLBACK FAILED for %s -- inspect the tree before retrying", path)
        raise
    finally:
        for tmp in temps:
            tmp.unlink(missing_ok=True)


def close_with_sweep_line(tasks_dir: Path, task_id: int, evidence_sha: str, closed_on: str,
                          sweep_line: str) -> None:
    """Close one row through `close_row_plan`, append the one `sweep-close:` line to the planned
    task bytes, and write the task file and tasks/manifest.json together (both or neither)."""
    import gen_task_tree as gtt  # noqa: PLC0415 -- sibling module, loaded only by the sweep
    try:
        plan = gtt.close_row_plan(Path(tasks_dir), int(task_id), evidence_sha, closed_on)
    except ValueError as exc:
        raise SweepError(str(exc)) from exc
    writes: list[tuple[Path, bytes]] = []
    for path, text in plan:
        if path.name != "manifest.json":
            text = text + sweep_line.rstrip("\n") + "\n"
        writes.append((path, text.encode("utf-8")))
    _atomic_write_all(writes)


# --- planning ---------------------------------------------------------------------------------------


@dataclass
class Decision:
    row: Row
    action: str                      # "close" | "keep"
    category: str                    # kept category, or "closed"
    cls: Optional[str] = None
    checked: list[str] = field(default_factory=list)
    absent: list[str] = field(default_factory=list)
    reason: str = ""
    would_close_as: Optional[str] = None   # a protected row's class had R-1/K1 not held


@dataclass
class SweepResult:
    closed: list[dict[str, Any]] = field(default_factory=list)
    kept: dict[str, list[str]] = field(default_factory=lambda: collections.defaultdict(list))
    label_differences: list[dict[str, Any]] = field(default_factory=list)
    protected_moves: list[dict[str, Any]] = field(default_factory=list)
    age_histogram: dict[str, int] = field(default_factory=dict)
    old_count: int = 0
    new_count: int = 0
    receipt: str = ""
    scan: str = ""


def _short_witnesses(held: Sequence[str], limit: int = 3) -> str:
    shown = ", ".join(held[:limit])
    return shown + (f" (+{len(held) - limit} more)" if len(held) > limit else "")


def open_dependency_ids(rows: Sequence[Row]) -> set[str]:
    """Ids named by the `depends-on:` frontmatter of an open row: closing one of them leaves a
    dangling dependency, which `validate_backlog` refuses (K1 witness `depends-on of open row`)."""
    named: set[str] = set()
    for row in rows:
        match = _FRONTMATTER_RE.match(row.path.read_text(encoding="utf-8"))
        value = _frontmatter_value(match.group(1), "depends-on") if match else None
        if value:
            named |= set(re.findall(r"\d+", value))
    return named


def _one_line(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _week_bucket(date: dt.date) -> str:
    monday = date - dt.timedelta(days=date.weekday())
    return monday.isoformat()


def plan_sweep(*, ruling: dict[str, Any], table: Sequence[dict[str, Any]], rows: Sequence[Row],
               repo_root: Path, transport_root: Path, today: dt.date,
               main_ref: str) -> tuple[list[Decision], dict[str, Any]]:
    """Decide every open row (pure but for git reads): returns the decisions in id order and the
    side facts (histogram, old/new counts)."""
    table_by_id = {str(t.get("id")): t for t in table}
    live = live_lane_ids(repo_root, transport_root=transport_root, main_ref=main_ref)
    sources = _read_k1_sources(ruling, repo_root, transport_root)
    mapping = ruling["decision_classes"]
    cutoff = ruling["cutoff"]
    depended_on = open_dependency_ids(rows)
    decisions: dict[str, Decision] = {}
    histogram: dict[str, int] = {}
    old = new = 0
    add_dates: dict[str, dt.date] = {}
    for row in rows:
        rel = f"tasks/{row.path.name}"
        try:
            add_dates[row.id] = task_add_date(repo_root, rel)
            histogram[_week_bucket(add_dates[row.id])] = \
                histogram.get(_week_bucket(add_dates[row.id]), 0) + 1
        except SweepError:
            pass
    for row in rows:
        entry = table_by_id.get(row.id)
        rel = f"tasks/{row.path.name}"

        def keep(category: str, reason: str = "") -> Decision:
            return Decision(row, "keep", category, reason=reason)

        if row.id in live:
            decisions[row.id] = keep("live-excluded", live[row.id])
            continue
        if entry is None or entry.get("file") != rel:
            decisions[row.id] = keep("absent-from-table")
            continue
        if entry.get("quote_verified") is not True:
            decisions[row.id] = keep("ungated")
            continue
        dclass = entry.get("decision_class")
        if dclass not in SWEEP_DECISION_CLASSES or dclass not in mapping:
            decisions[row.id] = keep("unknown-decision-class")
            continue
        added = add_dates.get(row.id)
        if added is None:
            decisions[row.id] = keep("no-add-date")
            continue
        k1 = k1_protected(row.id, source_texts=sources, cited_by_open=entry.get("cited_by_open") or [])
        if row.id in depended_on:
            k1.append("depends-on of an open row")
        k1_note = _short_witnesses(k1)
        mapped = mapping[dclass]
        if added < cutoff:
            old += 1
            would = ruling["legacy_class"]
            if k1:
                d = keep("protected", "K1: " + k1_note)
                d.would_close_as = would
                decisions[row.id] = d
                continue
            alive = k2_alive(row.body, repo_root=repo_root, ref=main_ref, today=today,
                             window_days=ruling["k2_window_days"])
            if alive:
                decisions[row.id] = keep("k2-alive", "K2: " + ", ".join(alive))
                continue
            if k3_agreed(entry):
                decisions[row.id] = keep("k3-agreed", "K3: both families LINE P1/P2, agreed")
                continue
            decisions[row.id] = Decision(
                row, "close", "closed", cls=would, checked=["K1", "K2", "K3"],
                absent=["K1", "K2", "K3"],
                reason=f"filed {added.isoformat()} before {cutoff.isoformat()}; no KEEP witness "
                       f"(K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds")
            continue
        new += 1
        if k1:
            d = keep("protected", "K1: " + k1_note)
            d.would_close_as = mapped if mapped != "keep" else None
            decisions[row.id] = d
            continue
        if dclass == "merge-rewrite":
            decisions[row.id] = keep("merge-rewrite")
        elif mapped == "keep" or dclass.startswith("keep-"):
            decisions[row.id] = keep("keep-class")
        else:
            decisions[row.id] = Decision(row, "close", "closed", cls=mapped, checked=["K1"],
                                         absent=["K1"], reason=_one_line(entry.get("reason")))

    _apply_r2(decisions, table_by_id, add_dates, cutoff)
    for row_id, dec in list(decisions.items()):
        # A row whose body ends in an archive pointer cannot take the close marker without
        # breaking the row-archive-proof gate (leg B: the row must END with the pointer), so the
        # sweep keeps it open and lists it rather than commit a refused state.
        if dec.action == "close" and (dec.row.path.parent / "archive" / f"{row_id}.md").exists():
            decisions[row_id] = Decision(dec.row, "keep", "archived-body",
                                         reason="body ends in an archive pointer (row-archive-proof)")
    _keep_duplicates_of_kept_canonicals(decisions, table_by_id)
    ordered =[decisions[r.id] for r in rows]
    return ordered, {"histogram": dict(sorted(histogram.items())), "old": old, "new": new}


def _apply_r2(decisions: dict[str, Decision], table_by_id: dict[str, dict], add_dates: dict,
              cutoff: dt.date) -> None:
    """R-2: a NEW canonical that closes takes its duplicates with it, with its class and reason;
    a cluster with a `live` duplicate is refused whole (no adjudicated unique-content flag)."""
    for canon_id, dec in list(decisions.items()):
        entry = table_by_id.get(canon_id) or {}
        if dec.action != "close" or entry.get("cluster_role") != "canonical":
            continue
        if add_dates.get(canon_id, cutoff) < cutoff or dec.cls == LEGACY_CLASS:
            continue
        dup_ids = [i for i, t in table_by_id.items() if str(t.get("duplicate_of")) == canon_id]
        if any(table_by_id[i].get("evidence_class") == "live" for i in dup_ids):
            for member in [canon_id, *dup_ids]:
                if member in decisions:
                    decisions[member] = Decision(
                        decisions[member].row, "keep", "r2-refused", reason=R2_REFUSED_LINE)
            continue
        for dup_id in dup_ids:
            dup = decisions.get(dup_id)
            if dup is None:
                continue
            overridable = (dup.action == "close" and dup.cls != LEGACY_CLASS) \
                or dup.category == "keep-class"
            if overridable:
                decisions[dup_id] = Decision(
                    dup.row, "close", "closed", cls=dec.cls, checked=["K1"], absent=["K1"],
                    reason=dec.reason)


def _keep_duplicates_of_kept_canonicals(decisions: dict[str, Decision],
                                        table_by_id: dict[str, dict]) -> None:
    """A step-2 `close-duplicate` row closes only when its canonical is closed by the SAME run:
    a canonical that is kept (merge-rewrite, keep-P*, protected, refused, archived, live) has not
    absorbed the duplicate's content, so closing the duplicate would drop it (Outcome (2) R-2,
    judge 2026-11-03). Legacy-sweep closes are decided by the cutoff rule and are not touched.
    Repeated until stable, so a duplicate of a duplicate that was just kept is kept as well."""
    changed = True
    while changed:
        changed = False
        for row_id, dec in list(decisions.items()):
            entry = table_by_id.get(row_id) or {}
            if dec.action != "close" or dec.cls == LEGACY_CLASS \
                    or entry.get("decision_class") != "close-duplicate":
                continue
            canon_id = str(entry.get("duplicate_of"))
            canon = decisions.get(canon_id)
            if canon is None or canon.action != "close":
                decisions[row_id] = Decision(
                    dec.row, "keep", "duplicate-of-kept",
                    reason=f"canonical [#{canon_id}] is not closed by this run")
                changed = True


def _sweep_line(dec: Decision) -> str:
    return (f"sweep-close: {dec.cls} · witnesses checked={','.join(dec.checked)} "
            f"absent={','.join(dec.absent)} · {_one_line(dec.reason)}")


def _label_differences(decisions: Sequence[Decision],
                       table_by_id: dict[str, dict]) -> list[dict[str, Any]]:
    diffs = []
    for dec in decisions:
        if dec.action != "keep":
            continue
        entry = table_by_id.get(dec.row.id)
        if not entry:
            continue
        match = _FRONTMATTER_RE.match(dec.row.path.read_text(encoding="utf-8"))
        filed = _frontmatter_value(match.group(1), "priority") if match else None
        sonnet = (entry.get("sonnet") or {}).get("priority")
        gemini = (entry.get("gemini") or {}).get("priority")
        if sonnet != filed or gemini != filed:
            diffs.append({"id": dec.row.id, "filed_priority": filed or "none",
                          "sonnet": sonnet, "gemini": gemini})
    return diffs


def _build_result(decisions: Sequence[Decision], facts: dict[str, Any],
                  table_by_id: dict[str, dict], revert_check: str) -> SweepResult:
    result = SweepResult()
    result.old_count, result.new_count = facts["old"], facts["new"]
    result.age_histogram = facts["histogram"]
    for dec in decisions:
        if dec.action == "close":
            result.closed.append({
                "id": dec.row.id, "title": dec.row.title, "class": dec.cls,
                "witnesses_checked": list(dec.checked), "witnesses_absent": list(dec.absent),
                "reason": dec.reason})
        else:
            result.kept[dec.category].append(dec.row.id)
            if dec.category == "protected" and dec.would_close_as:
                result.protected_moves.append({"id": dec.row.id, "would_close_as": dec.would_close_as,
                                               "witnesses": dec.reason})
    result.label_differences = _label_differences(decisions, table_by_id)
    per_class: dict[str, int] = {}
    for item in result.closed:
        per_class[item["class"]] = per_class.get(item["class"], 0) + 1
    result.receipt = (
        f"SWEEP closed={len(result.closed)} "
        f"per-class={','.join(f'{k}:{v}' for k, v in sorted(per_class.items())) or 'none'} "
        f"protected-kept={len(result.kept.get('protected', []))} protected-closed=0 "
        f"live-excluded={len(result.kept.get('live-excluded', []))} "
        f"r2-refused={len(result.kept.get('r2-refused', []))} revert-check={revert_check}")
    result.scan = _render_scan(result, per_class)
    return result


def _render_scan(result: SweepResult, per_class: dict[str, int]) -> str:
    lines = ["# Backlog sweep scan", "", result.receipt, "",
             f"Open rows: old (filed before the cutoff) {result.old_count}, "
             f"new {result.new_count}.", "", "## closed per class", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(per_class.items())] or ["- none"]
    lines += ["", "## age histogram (weekly buckets of add-date, Monday)", ""]
    lines += [f"- {k}: {v}" for k, v in result.age_histogram.items()]
    lines += ["", "## protected moves (kept by R-1/K1, a class would have closed)", ""]
    lines += [f"- [#{m['id']}] would close as {m['would_close_as']} ({m['witnesses']})"
              for m in result.protected_moves] or ["- none"]
    lines += ["", "## kept lists", ""]
    for category in KEPT_CATEGORIES:
        ids = result.kept.get(category, [])
        if category == "r2-refused" and ids:
            lines.append(f"{R2_REFUSED_LINE}: " + " ".join(f"[#{i}]" for i in ids))
        else:
            lines.append(f"- {category} ({len(ids)}): " + (" ".join(f"[#{i}]" for i in ids) or "none"))
    lines += ["", "## label differences"]
    lines += [f"- [#{d['id']}] filed={d['filed_priority']} sonnet={d['sonnet']} gemini={d['gemini']}"
              for d in result.label_differences] or ["- none"]
    return "\n".join(lines) + "\n"


# --- execution --------------------------------------------------------------------------------------


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _execute(decisions: Sequence[Decision], *, tasks_dir: Path, home: Path, ruling_name: str,
             evidence_sha: str, today: dt.date) -> None:
    """Write the ledger and index first (so a crash stays revertible), then close each row."""
    manifest_path = Path(tasks_dir) / "manifest.json"
    pre_manifest = manifest_path.read_bytes()
    nodes = json.loads(pre_manifest.decode("utf-8"))["nodes"]
    closing = [d for d in decisions if d.action == "close"]
    entries = []
    for dec in closing:
        raw = dec.row.path.read_bytes()
        index = next((i for i, n in enumerate(nodes) if n.get("task") == int(dec.row.id)), None)
        if index is None:
            raise SweepError(f"[#{dec.row.id}] has no node in tasks/manifest.json")
        entries.append({
            "id": dec.row.id, "title": dec.row.title, "class": dec.cls,
            "witnesses_checked": dec.checked, "witnesses_absent": dec.absent,
            "reason": _one_line(dec.reason), "file": dec.row.path.name,
            "pre_b64": _b64(raw), "pre_sha256": _sha(raw), "node_index": index,
            "node": nodes[index]})
    ledger = {"version": 1, "swept_on": today.isoformat(), "evidence_sha": evidence_sha,
              "ruling": ruling_name, "manifest_pre_b64": _b64(pre_manifest),
              "manifest_pre_sha256": _sha(pre_manifest), "closed": entries}
    index_lines = [f"- [#{e['id']}] {e['title']} | {e['class']} | "
                    f"checked={','.join(e['witnesses_checked'])} "
                    f"absent={','.join(e['witnesses_absent'])}" for e in entries]
    home.mkdir(parents=True, exist_ok=True)
    (home / SWEEP_LEDGER).write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + "\n",
                                     encoding="utf-8", newline="\n")
    (home / SWEEP_INDEX).write_text("\n".join(index_lines) + "\n", encoding="utf-8", newline="\n")
    done = 0
    try:
        for dec in closing:
            close_with_sweep_line(tasks_dir, int(dec.row.id), evidence_sha, today.isoformat(),
                                  _sweep_line(dec))
            done += 1
        # The post-sweep bytes of each swept file: `--revert` restores a file only while it still
        # has these bytes, so a later edit to a closed row is never overwritten (judge, 2026-11-03).
        for entry in entries:
            entry["post_sha256"] = _sha((Path(tasks_dir) / entry["file"]).read_bytes())
        (home / SWEEP_LEDGER).write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + "\n",
                                         encoding="utf-8", newline="\n")
    except BaseException:
        run_revert(tasks_dir=tasks_dir, home=home, spec=",".join(d.row.id for d in closing[:done]) or "0")
        (home / SWEEP_LEDGER).unlink(missing_ok=True)
        (home / SWEEP_INDEX).unlink(missing_ok=True)
        raise


def _tree_digest(tasks_dir: Path) -> dict[str, str]:
    return {p.name: _sha(p.read_bytes()) for p in sorted(Path(tasks_dir).iterdir()) if p.is_file()}


def run_sweep(*, ruling_path: Path, table_path: Path, tasks_dir: Path, repo_root: Path, home: Path,
              transport_root: Path, today: dt.date, evidence_sha: str,
              main_ref: str = "origin/main", dry_run: bool = False) -> SweepResult:
    """Plan the sweep, prove on a scratch copy that a full revert is byte-identical, then write."""
    tasks_dir, home, repo_root = Path(tasks_dir), Path(home), Path(repo_root)
    if (home / SWEEP_LEDGER).exists() and not dry_run:
        raise SweepError(f"{home / SWEEP_LEDGER} already exists: one sweep per home")
    ruling = load_sweep_ruling(ruling_path)
    table = load_step1_table(table_path)
    table_by_id = {str(t.get("id")): t for t in table}
    rows = load_open_rows(tasks_dir)
    decisions, facts = plan_sweep(ruling=ruling, table=table, rows=rows, repo_root=repo_root,
                                  transport_root=Path(transport_root), today=today,
                                  main_ref=main_ref)
    if dry_run:
        return _build_result(decisions, facts, table_by_id, "not-run")
    before = _tree_digest(tasks_dir)
    with tempfile.TemporaryDirectory(prefix="sweep-scratch-") as scratch_name:
        scratch = Path(scratch_name)
        shutil.copytree(tasks_dir, scratch / "tasks")
        scratch_rows = {r.id: r for r in load_open_rows(scratch / "tasks")}
        scratch_decisions = [
            Decision(scratch_rows[d.row.id], d.action, d.category, d.cls, d.checked, d.absent,
                     d.reason) if d.row.id in scratch_rows else d for d in decisions]
        _execute(scratch_decisions, tasks_dir=scratch / "tasks", home=scratch / "home",
                 ruling_name=Path(ruling_path).name, evidence_sha=evidence_sha, today=today)
        run_revert(tasks_dir=scratch / "tasks", home=scratch / "home", spec="all")
        identical = _tree_digest(scratch / "tasks") == before
    if not identical:
        raise SweepError("scratch revert is not byte-identical to the pre-sweep tree: "
                         "nothing was written")
    _execute(decisions, tasks_dir=tasks_dir, home=home, ruling_name=Path(ruling_path).name,
             evidence_sha=evidence_sha, today=today)
    return _build_result(decisions, facts, table_by_id, "byte-identical")


# --- revert -----------------------------------------------------------------------------------------


def _insert_position(pre_nodes: list, current: list, pre_index: int) -> int:
    """Where a reverted node goes: right after the nearest preceding PRE-sweep node that is still
    present in `current` (0 if none); nodes added since the sweep are never moved."""
    aligned: dict[int, int] = {}
    pointer = 0
    for cur_index, node in enumerate(current):
        for pre_j in range(pointer, len(pre_nodes)):
            if pre_nodes[pre_j] == node:
                aligned[pre_j] = cur_index
                pointer = pre_j + 1
                break
    anchors = [j for j in aligned if j < pre_index]
    return aligned[max(anchors)] + 1 if anchors else 0


def run_revert(*, tasks_dir: Path, home: Path, spec: str) -> list[str]:
    """Restore the ledgered rows named by `spec` (a class, `all`, or comma-separated ids): the
    task file byte for byte, its node at its original position. Returns the ids restored."""
    tasks_dir, home = Path(tasks_dir), Path(home)
    ledger_path = home / SWEEP_LEDGER
    if not ledger_path.is_file():
        raise SweepError(f"no sweep ledger at {ledger_path}")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    entries = ledger["closed"]
    parts = [p.strip() for p in spec.split(",") if p.strip()]
    classes = {e["class"] for e in entries}
    if parts == ["all"]:
        selected = list(entries)
    elif len(parts) == 1 and parts[0] in classes:
        selected = [e for e in entries if e["class"] == parts[0]]
    elif parts and all(p.isdigit() for p in parts):
        selected = [e for e in entries if e["id"] in set(parts)]
    else:
        raise SweepError(f"revert spec {spec!r} is neither a ledger class ({sorted(classes)}), "
                         "'all' nor a comma-separated id list")
    pre_nodes = json.loads(base64.b64decode(ledger["manifest_pre_b64"]).decode("utf-8"))["nodes"]
    manifest_path = tasks_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
    writes: list[tuple[Path, bytes]] = []
    restored: list[str] = []
    for entry in sorted(selected, key=lambda e: e["node_index"]):
        if any(n.get("task") == int(entry["id"]) for n in manifest["nodes"]):
            continue  # already open: a no-op
        pre = base64.b64decode(entry["pre_b64"])
        if _sha(pre) != entry["pre_sha256"]:
            raise SweepError(f"ledger bytes for [#{entry['id']}] fail their own sha256")
        current = tasks_dir / entry["file"]
        post = entry.get("post_sha256")
        if post and current.is_file() and _sha(current.read_bytes()) != post:
            # The closed file was edited after the sweep: restoring would overwrite that edit.
            logging.getLogger(__name__).warning(
                "revert skipped [#%s]: %s no longer has its post-sweep bytes", entry["id"], entry["file"])
            continue
        position = _insert_position(pre_nodes, manifest["nodes"], entry["node_index"])
        manifest["nodes"].insert(position, entry["node"])
        writes.append((tasks_dir / entry["file"], pre))
        restored.append(entry["id"])
    if writes:
        writes.append((manifest_path,
                       (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")))
        _atomic_write_all(writes)
    return restored


# --- the CLI -------------------------------------------------------------------------------------


def _tasks_option(fn):
    return click.option("--tasks-dir", type=click.Path(file_okay=False, path_type=Path),
                        default=DEFAULT_TASKS_DIR, show_default=True)(fn)


def _state_option(fn):
    return click.option("--state-dir", type=click.Path(file_okay=False, path_type=Path),
                        default=DEFAULT_STATE_DIR, show_default=True)(fn)


@click.group()
def cli() -> None:
    """Per-row backlog reconciliation: evidence, reads, adjudication, report, ruled apply."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")


@cli.command()
@_tasks_option
@_state_option
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path), default=REPO_ROOT)
@click.option("--commit-log", type=click.Path(dir_okay=False, path_type=Path), default=None,
              help="Test seam: a prepared commit log instead of `git log`.")
def evidence(tasks_dir: Path, state_dir: Path, repo_root: Path, commit_log: Optional[Path]) -> None:
    """Gather code-computed evidence for every open row -> evidence.json."""
    commits = read_commit_log(commit_log) if commit_log else git_commit_index(repo_root)
    counts = work_commit_counts(commits)
    rows = load_open_rows(tasks_dir)
    data = {r.id: collect_evidence(r, repo_root=repo_root, work_commits=counts.get(r.id, 0))
            for r in rows}
    _write_json(state_dir / "evidence.json", data)
    click.echo(f"evidence: {len(data)} open rows -> {state_dir / 'evidence.json'}")


@cli.command()
@_state_option
def verify(state_dir: Path) -> None:
    """Check reads.json against evidence.json and the batch sources it quotes."""
    reads = _read_json(state_dir / "reads.json")
    evid = _read_json(state_dir / "evidence.json")
    if reads is None or evid is None:
        raise click.ClickException("verify needs both evidence.json and reads.json")
    source = " ".join(read_gate.normalize_whitespace(p.read_text(encoding="utf-8"))
                      for p in sorted((state_dir / "batches").glob("*.md")))
    for row_id, read in sorted(reads.items(), key=lambda kv: int(kv[0])):
        if row_id not in evid:
            raise click.ClickException(f"[#{row_id}] is in reads.json but not in evidence.json")
        if read.get("verdict") not in VERDICTS:
            raise click.ClickException(f"[#{row_id}] verdict {read.get('verdict')!r} is invalid")
        quote = read.get("quote", "")
        if quote and not read_gate.quotation_in_source(quote, source):
            raise click.ClickException(f"[#{row_id}] quote is not in any batch source: {quote[:80]!r}")
        if not quote and read.get("verdict") != "unclear":
            raise click.ClickException(f"[#{row_id}] has a verdict but no quote")
    click.echo(f"verify: {len(reads)} reads consistent")


@cli.command()
@_tasks_option
@_state_option
@click.option("--registry", type=click.Path(dir_okay=False, path_type=Path),
              default=DEFAULT_REGISTRY, show_default=True)
@click.option("--limit", type=int, default=None, help="Read only the first N open rows.")
def fanout(tasks_dir: Path, state_dir: Path, registry: Path, limit: Optional[int]) -> None:
    """Read the open rows in gated batches of 20 -> reads.json (exit 1 on an ungated read)."""
    global _CALLS_PATH
    _CALLS_PATH = state_dir / "calls.jsonl"
    rows = load_open_rows(tasks_dir)[:limit]
    try:
        result = run_fanout(rows, invoke=default_invoke, state_dir=state_dir,
                            registry_path=registry, second_invoke=default_second_invoke)
    except UngatedReadError as exc:
        click.echo(f"fanout refused: {exc}", err=True)
        sys.exit(1)
    click.echo(f"fanout: {len(result.reads)} rows in {result.batches} batches, "
               f"{len(result.second_read_ids)} second-read")


@cli.command()
@_state_option
@click.option("--model", default=None,
              help="Defaults to the registry's Opus (alias `opus`).")
@click.option("--tasks-dir", type=click.Path(file_okay=False, path_type=Path), default=None,
              help="Optional: include each target row's text in the prompt.")
def adjudicate(state_dir: Path, model: Optional[str], tasks_dir: Optional[Path]) -> None:
    """Settle the unclear or read-disputed rows with one headless Opus session."""
    global _CALLS_PATH
    _CALLS_PATH = state_dir / "calls.jsonl"
    model = model or _alias_model("opus")
    evid = _read_json(state_dir / "evidence.json", {})
    reads = _read_json(state_dir / "reads.json", {})
    targets = _adjudication_targets(evid, reads)
    if not targets:
        _write_json(state_dir / "adjudications.json", {})
        click.echo("adjudicate: nothing unsettled")
        return
    bodies = {}
    if tasks_dir:
        bodies = {r.id: _plain(r.body, 700) for r in load_open_rows(tasks_dir) if r.id in targets}
    reply = run_claude(model, _adjudication_prompt(targets, evid, reads, bodies))
    record_call(reply["model"], "adjudicate", reply["input_tokens"], reply["output_tokens"],
                reply["usd"])
    accepted, dropped = parse_adjudication(reply["text"], targets)
    _write_json(state_dir / "adjudications.json", accepted)
    for item in dropped:
        click.echo(f"adjudicate: dropped unknown reply line: {item}", err=True)
    click.echo(f"adjudicate: {len(accepted)} of {len(targets)} rows settled by {reply['model']}")


@cli.command()
@_tasks_option
@_state_option
@click.option("--out", type=click.Path(dir_okay=False, path_type=Path), required=True)
@click.option("--cost-out", type=click.Path(dir_okay=False, path_type=Path), required=True)
def report(tasks_dir: Path, state_dir: Path, out: Path, cost_out: Path) -> None:
    """Group the open rows by evidence class; write classification.json, the report, the cost."""
    evid = _read_json(state_dir / "evidence.json")
    if evid is None:
        raise click.ClickException("report needs evidence.json (run `evidence` first)")
    reads = _read_json(state_dir / "reads.json")
    if reads is None:
        # A classification written without the gated reads is code-only evidence dressed as a
        # reconciliation; the operator would rule classes nobody read (review 1, terra).
        raise click.ClickException("report needs reads.json (run `fanout` first)")
    adjudications = _read_json(state_dir / "adjudications.json", {})
    rows = load_open_rows(tasks_dir)
    unread = [r.id for r in rows if reads.get(r.id, {}).get("verdict") not in VERDICTS]
    if unread:
        # A partial `fanout --limit N` (or a row filed after the run) must not be classified from
        # code-only evidence and offered to `apply` as if it had been read (review 1, terra).
        raise click.ClickException(
            f"report needs a gated read for every open row; {len(unread)} have none "
            f"(first: {', '.join('[#' + i + ']' for i in unread[:5])}) -- run `fanout` over all rows")
    classification: dict[str, str] = {}
    for row in rows:
        read = reads.get(row.id, {})
        adjudicated = adjudications.get(row.id, {}).get("class")
        verdict = read.get("verdict")
        if adjudicated is None and read.get("second_read") == "disagree":
            verdict = "unclear"  # two readers disagree and Opus has not settled it
        classification[row.id] = classify(evid.get(row.id, {}), verdict, adjudicated)
    _write_json(state_dir / "classification.json", classification)
    _write_json(state_dir / SNAPSHOT_NAME, {r.id: _file_sha(r.path) for r in rows})
    cost = cost_record(state_dir / "calls.jsonl")
    _write_json(cost_out, cost)
    lines = ["# Backlog reconcile report", "",
             f"Run date: {dt.date.today().isoformat()}. Open rows: {len(rows)}. Evidence classes "
             "below; the operator rules per class and `apply --ruling` acts on nothing else.", "",
             "| Class | Rows |", "|---|---|"]
    lines += [f"| {k} | {sum(1 for v in classification.values() if v == k)} |"
              for k in EVIDENCE_CLASSES]
    lines += ["", f"Cost: {cost['calls']} calls, {cost['input_tokens']} input tokens, "
              f"{cost['output_tokens']} output tokens, USD {cost['usd']:.2f} (priced calls only; "
              "models without a registered rate carry `usd: null` in the cost record).", ""]
    for klass in EVIDENCE_CLASSES:
        members = [r for r in rows if classification[r.id] == klass]
        if not members:
            continue
        lines += [f"## {klass}", ""]
        for row in members:
            ev, read = evid.get(row.id, {}), reads.get(row.id, {})
            lines.append(
                f"- [#{row.id}] {row.title} — read: {read.get('verdict', 'none')}; "
                f"work commits: {ev.get('work_commits', 0)}; "
                f"paths missing: {len(ev.get('paths_missing', []))}")
        lines.append("")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(lines), encoding="utf-8", newline="\n")
    click.echo(f"report: {len(rows)} rows -> {out}; cost USD {cost['usd']:.2f} -> {cost_out}")


@cli.command()
@click.option("--ruling", type=click.Path(path_type=Path), default=None,
              help="Mode 1: the five-evidence-class ruling (needs report's classification).")
@click.option("--sweep", "sweep_ruling", type=click.Path(path_type=Path), default=None,
              help="Mode 2: the legacy-sweep ruling file (needs --step1-table).")
@click.option("--revert", "revert_spec", default=None,
              help="Mode 3: reopen a swept class (or `all`, or ids `112,113`) from the ledger.")
@click.option("--step1-table", type=click.Path(dir_okay=False, path_type=Path), default=None)
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path), default=REPO_ROOT)
@click.option("--home", type=click.Path(file_okay=False, path_type=Path),
              default=DEFAULT_SWEEP_HOME, show_default=True)
@click.option("--transport-root", type=click.Path(file_okay=False, path_type=Path),
              default=DEFAULT_TRANSPORT_ROOT, show_default=True)
@click.option("--today", default=None, help="ISO date; default today.")
@click.option("--evidence-sha", default=None, help="Default: HEAD of --repo-root.")
@click.option("--main-ref", default="origin/main", show_default=True)
@click.option("--scan-out", type=click.Path(dir_okay=False, path_type=Path), default=None)
@click.option("--dry-run", is_flag=True, help="Sweep: plan and print, write nothing.")
@_tasks_option
@_state_option
def apply(ruling: Optional[Path], sweep_ruling: Optional[Path], revert_spec: Optional[str],
          step1_table: Optional[Path], repo_root: Path, home: Path, transport_root: Path,
          today: Optional[str], evidence_sha: Optional[str], main_ref: str,
          scan_out: Optional[Path], dry_run: bool, tasks_dir: Path, state_dir: Path) -> None:
    """Apply an operator ruling (only the classes it names), run the legacy sweep, or revert it."""
    modes = [m for m in (ruling, sweep_ruling, revert_spec) if m is not None]
    if len(modes) != 1:
        raise click.UsageError("choose exactly one of --ruling, --sweep, --revert")
    if revert_spec is not None:
        restored = run_revert(tasks_dir=tasks_dir, home=home, spec=revert_spec)
        click.echo(f"revert: restored {len(restored)} row(s): {','.join(restored)}")
        return
    if sweep_ruling is not None:
        if step1_table is None:
            raise click.UsageError("--sweep needs --step1-table")
        sha = evidence_sha or _git(repo_root, "rev-parse", "HEAD").stdout.strip()
        result = run_sweep(
            ruling_path=sweep_ruling, table_path=step1_table, tasks_dir=tasks_dir,
            repo_root=repo_root, home=home, transport_root=transport_root,
            today=dt.date.fromisoformat(today) if today else dt.date.today(),
            evidence_sha=sha, main_ref=main_ref, dry_run=dry_run)
        if scan_out is not None:
            Path(scan_out).parent.mkdir(parents=True, exist_ok=True)
            Path(scan_out).write_text(result.scan, encoding="utf-8", newline="\n")
        click.echo(result.receipt)
        return
    actions = load_ruling(ruling)
    classification = _read_json(state_dir / "classification.json")
    if classification is None:
        raise RulingError("classification.json is missing; run `report` before `apply`")
    snapshot = _read_json(state_dir / SNAPSHOT_NAME)
    if snapshot is None:
        raise RulingError(f"{SNAPSHOT_NAME} is missing; run `report` before `apply`")
    targets = []
    for row in load_open_rows(tasks_dir):
        action = actions.get(classification.get(row.id, ""))
        if action and action != "keep":
            targets.append((row, action))
    # The classification describes the task files AS THEY WERE at `report`. A row edited or
    # replaced since then would receive the old row's class, so refuse before any write.
    stale = [r.id for r, _ in targets if snapshot.get(r.id) != _file_sha(r.path)]
    if stale:
        raise RulingError(
            f"task file(s) changed since `report`: {', '.join('[#' + i + ']' for i in stale)}; "
            "re-run `report` before `apply`")
    changed = 0
    for row, action in targets:
        if apply_action(row.path, action):
            changed += 1
            snapshot[row.id] = _file_sha(row.path)
    _write_json(state_dir / SNAPSHOT_NAME, snapshot)
    click.echo(f"apply: {changed} task file(s) changed")


if __name__ == "__main__":
    cli()
