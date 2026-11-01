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

COST: every model call appends one line to `<state>/calls.jsonl`; `report` sums it. A call whose
model has no registered rate carries `usd: null`, and the total sums PRICED calls only -- absent
and free are different facts (`provider_registry.RateUnavailable`'s rule), so the record never
reports an unpriced model as zero.

HEADLESS CLAUDE (`run_claude`): the prompt goes on STDIN (the Windows `.cmd` shim corrupts a
multi-line argv prompt), `--setting-sources local` plus a scratch cwd keep the repo's Stop hook
from eating the answer (`claude-p-json-result-is-only-the-last-message-a-stop-hook-eats-the-report`),
and the scratch directory is removed afterwards (no leftovers).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import logging
import math
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional, Sequence

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
_READ_LINE_RE = re.compile(
    r"^\s*\[?#?(\d+)\]?\s*\|\s*(done|open|obsolete|unclear)\s*\|\s*[\"“](.*)[\"”]\s*$"
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
            for row_id in batch_sampled:
                other = second.get(row_id, ("unclear", ""))[0]
                result.reads[row_id]["second_read"] = (
                    "agree" if other == result.reads[row_id]["verdict"] else "disagree")
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
        new_front, n = re.subn(r"(?m)^status: open(\r?\n)", r"status: closed\1", front, count=1)
    else:  # rewrite
        if re.search(r"(?m)^reconcile: rewrite\r?$", front):
            return False
        new_front, n = re.subn(r"(?m)^status: open(\r?\n)",
                               r"status: open\1reconcile: rewrite\1", front, count=1)
    if not n:
        return False
    path.write_bytes((raw[:match.start(1)] + new_front + raw[match.end(1):]).encode("utf-8"))
    return True


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
    reads = _read_json(state_dir / "reads.json", {})
    adjudications = _read_json(state_dir / "adjudications.json", {})
    rows = load_open_rows(tasks_dir)
    classification: dict[str, str] = {}
    for row in rows:
        classification[row.id] = classify(
            evid.get(row.id, {}), reads.get(row.id, {}).get("verdict"),
            adjudications.get(row.id, {}).get("class"))
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
@click.option("--ruling", type=click.Path(path_type=Path), required=True)
@_tasks_option
@_state_option
def apply(ruling: Path, tasks_dir: Path, state_dir: Path) -> None:
    """Apply an operator ruling: only the classes it names, nothing else."""
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
