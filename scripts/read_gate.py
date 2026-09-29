"""A read counts only when its output exists, its log is clean and every quotation is
literally in the source (WAVE5B-N5 AX21-1, "CC verifies" -- LANE-5B5-11). The defect this
closes: `agy` reported SUCCESS on a 20-minute print timeout with no output file, and put
paraphrase in quotation marks on 4 of 6 pages checked
(`to-browser/SESSION-seat-trackb-aj-m06-wave5b-n5-r.md`).

LIBRARY-FIRST, cited per this repo's convention:
- extraction: `pdfplumber` (MIT) for PDF -- this lane's one added dependency, `uv add`, AMEND
  v3 authorization quoted in `pyproject.toml`; the standard library (`zipfile` +
  `html.parser`) for EPUB; plain text as-is. `PyMuPDF` (AGPL) is not added -- the operator's
  word was not given for it.
- the route runner's injectable-invoker shape and its `RuntimeError` subclass mirror
  `scripts/aj_scan.py::delegate_describe` / `ScanError`; the real `agy`/`copilot` argv and the
  JSONL ledger-append convention (`json.dumps(row, ensure_ascii=False, sort_keys=True)`) mirror
  `scripts/provider_bench.py::_agy_args` / `_copilot_args` / `append_ledger`. Neither module is
  imported -- both are benchmark/scan-specific -- their SHAPES are reused, not their code.

WHAT COUNTS AS A QUOTATION (DONE-ITEM 1 requires this stated here): any run of text enclosed
in a matching pair of ASCII `"` or Unicode curly `“ ... ”` quotation marks in a
route's output file. Whitespace inside a quotation is normalized
(`re.sub(r"\\s+", " ", s).strip()`) before the literal-substring check against the source
text, which is normalized the same way -- "and nothing else" (AMEND v3): no fuzzy matching,
no case folding, no punctuation stripping.

THE LEDGER: `logs/READ-OUTCOMES.jsonl`. The render's own placeholder name already matches
this repo's `logs/<NAME>.jsonl` append-only convention exactly (`PROVIDER-BENCH-RUNS.jsonl`,
`LANE-COSTS.jsonl`, `QUOTA-READS.jsonl`), so it is kept rather than renamed -- no
DECIDED-BY-LANE line is needed for the ledger's home.
"""
from __future__ import annotations

import hashlib
import html.parser
import json
import os
import re
import shutil
import subprocess
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_REL = "ecosystem/provider-registry.yaml"
LEDGER_REL = "logs/READ-OUTCOMES.jsonl"

PRINT_TIMEOUT_MARKER = "print timeout"
_QUOTE_RE = re.compile(r'"([^"]+)"|“([^”]+)”')
_WS_RE = re.compile(r"\s+")


class ReadGateError(RuntimeError):
    """The registry or a route's declared shape could not be read -- raised rather than
    degraded, the same posture as `aj_scan.ScanError`: a silently-skipped route would be a
    false negative on the fall-through, not a missing feature."""


def normalize_whitespace(text: str) -> str:
    return _WS_RE.sub(" ", text).strip()


def extract_quotations(output_text: str) -> list[str]:
    """Every run of text between a matching pair of quotation marks (straight `"..."` or
    curly `“...”`), whitespace-normalized. See the module docstring for why this,
    and only this, counts as a quotation."""
    found = []
    for straight, curly in _QUOTE_RE.findall(output_text):
        normalized = normalize_whitespace(straight or curly)
        if normalized:
            found.append(normalized)
    return found


# --- source extraction (DONE-ITEM 1) ---------------------------------------------------------


def extract_source_text(source_path: Path) -> str:
    suffix = source_path.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf_text(source_path)
    if suffix == ".epub":
        return _extract_epub_text(source_path)
    return source_path.read_text(encoding="utf-8")


def _extract_pdf_text(source_path: Path) -> str:
    import pdfplumber  # local import: only a PDF read pays this cost

    with pdfplumber.open(source_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


class _EpubTextExtractor(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []

    def handle_data(self, data: str) -> None:
        self._chunks.append(data)

    def text(self) -> str:
        return "".join(self._chunks)


def _extract_epub_text(source_path: Path) -> str:
    chunks = []
    with zipfile.ZipFile(source_path) as zf:
        for name in zf.namelist():
            if name.lower().endswith((".xhtml", ".html", ".htm")):
                parser = _EpubTextExtractor()
                parser.feed(zf.read(name).decode("utf-8", errors="replace"))
                chunks.append(parser.text())
    return "\n".join(chunks)


# --- the verifier (DONE-ITEM 1) ---------------------------------------------------------------


@dataclass(frozen=True)
class ReadVerdict:
    accepted: bool
    failed_check: Optional[str] = None


def verify_read(output_path: Optional[Path], log_text: str, source_text: str) -> ReadVerdict:
    """Accepts a read only if all three (AMEND v3 done-when item 1) hold, PLUS one more this
    lane strengthens rather than weakens (ADR-108 SS B): an output with zero quotations is a
    paraphrase wearing no quotation marks, not a verified read -- "every quotation ... is
    found literally in the source" is vacuously true of an empty set, so the three-check
    reading on its own accepts free-form paraphrase (Codex terra CRITICAL,
    `docs/audits/2026-09-29-codex-lane-read-gate.md`). Checked in this order so
    `failed_check` always names the FIRST thing wrong."""
    if output_path is None or not output_path.exists() or output_path.stat().st_size == 0:
        return ReadVerdict(False, "output-file-missing-or-empty")
    if PRINT_TIMEOUT_MARKER in log_text.lower():
        return ReadVerdict(False, "print-timeout-in-log")
    output_text = output_path.read_text(encoding="utf-8")
    quotations = extract_quotations(output_text)
    if not quotations:
        return ReadVerdict(False, "no-quotation-in-output")
    normalized_source = normalize_whitespace(source_text)
    for quotation in quotations:
        if quotation not in normalized_source:
            return ReadVerdict(False, f"quotation-not-in-source:{quotation[:80]!r}")
    return ReadVerdict(True, None)


# --- the route runner (DONE-ITEM 2) ------------------------------------------------------------


@dataclass(frozen=True)
class RouteSpec:
    provider: str
    model: Optional[str] = None
    note: Optional[str] = None


def load_read_routes(registry_path: Path) -> list[RouteSpec]:
    """`roles.read.order`, read fresh every call -- DONE-ITEM 5: this lane never changes the
    registry, and the runner never hard-codes a route."""
    data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    try:
        order = data["roles"]["read"]["order"]
    except (KeyError, TypeError) as exc:
        raise ReadGateError(f"{registry_path}: no roles.read.order") from exc
    return [
        RouteSpec(provider=item["provider"], model=item.get("model"), note=item.get("note"))
        for item in order
    ]


@dataclass(frozen=True)
class InvokeAttempt:
    """What an invoker hands back: the output file it expects the reader to have written (or
    `None` if the route produced nothing), and the log text the verifier checks for a print
    timeout."""

    output_path: Optional[Path]
    log_text: str = ""
    status: str = ""


Invoker = Callable[[RouteSpec, Path, Path], InvokeAttempt]


@dataclass(frozen=True)
class RouteOutcome:
    route: str
    verdict: str  # "accepted" | "rejected"
    failed_check: Optional[str] = None


@dataclass(frozen=True)
class ReadGateResult:
    accepted: bool
    served_route: Optional[str]
    output_path: Optional[Path]
    attempts: list[RouteOutcome] = field(default_factory=list)

    def failure_summary(self) -> str:
        """Every route and its failed check -- DONE-ITEM 2's failure-naming half."""
        return "; ".join(f"{a.route}: {a.failed_check}" for a in self.attempts)


def run_read_gate(
    source_path: Path,
    *,
    registry_path: Path,
    invoke: Invoker,
    workdir: Path,
    ledger_path: Path,
) -> ReadGateResult:
    """Walk `roles.read` in the registry's declared order; verify each read; fall through on
    a failed check; return the first verified result, or a failure naming every route and its
    failed check (all attempts are always in `.attempts`, verified or not)."""
    source_text = extract_source_text(source_path)
    source_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
    attempts: list[RouteOutcome] = []
    for route in load_read_routes(registry_path):
        # The RUNNER owns each attempt's output path and clears it before the call -- an
        # invoker's return value is never trusted to name it, so a stale file, the source
        # file, or a path outside `workdir` cannot be read back as this attempt's output
        # (Codex terra HIGH, `docs/audits/2026-09-29-codex-lane-read-gate.md`).
        expected_output = workdir / f"{route.provider}.output.txt"
        expected_output.unlink(missing_ok=True)
        try:
            attempt = invoke(route, source_path, workdir)
        # An unavailable or misbehaving route falls through to the next one; it does not
        # abort the run -- that is the whole point of a fall-through gate.
        except Exception as exc:
            outcome = RouteOutcome(route.provider, "rejected", f"invoke-error:{exc}")
            attempts.append(outcome)
            _append_ledger(ledger_path, outcome, source_sha256)
            continue
        output_path = expected_output if expected_output.exists() else None
        try:
            verdict = verify_read(output_path, attempt.log_text, source_text)
        # A malformed or partially written output (deleted mid-race, a permission error,
        # invalid UTF-8 bytes) rejects this route rather than aborting every later one.
        except (OSError, UnicodeDecodeError) as exc:
            verdict = ReadVerdict(False, f"verify-error:{exc}")
        outcome = RouteOutcome(
            route.provider,
            "accepted" if verdict.accepted else "rejected",
            verdict.failed_check,
        )
        attempts.append(outcome)
        _append_ledger(ledger_path, outcome, source_sha256)
        if verdict.accepted:
            return ReadGateResult(True, route.provider, output_path, attempts)
    return ReadGateResult(False, None, None, attempts)


def _append_ledger(ledger_path: Path, outcome: RouteOutcome, source_sha256: str) -> None:
    """One line per read -- DONE-ITEM 4. Same convention as
    `provider_bench.append_ledger`: append-only, `sort_keys=True`, never rewrites a byte."""
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "route": outcome.route,
        "source_sha256": source_sha256,
        "verdict": outcome.verdict,
        "failed_check": outcome.failed_check,
    }
    with ledger_path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


# --- real invokers (DONE-ITEM 7's live leg; no test calls any of these) -----------------------


def _npm_shim(name: str) -> str:
    """Mirrors `provider_bench._npm_shim`: an npm global is a `.cmd` shim on Windows and
    `CreateProcess` does not consult PATHEXT."""
    if os.name == "nt":
        cmd = shutil.which(f"{name}.cmd")
        if cmd:
            return cmd
    return shutil.which(name) or name


def _cli_invoker(
    cli: str,
    argv_builder: Callable[[str, Path], list[str]],
    timeout_s: int,
    *,
    runner: Callable[..., "subprocess.CompletedProcess[str]"] = subprocess.run,
) -> Invoker:
    def invoke(route: RouteSpec, source_path: Path, workdir: Path) -> InvokeAttempt:
        output_path = workdir / f"{route.provider}.output.txt"
        output_path.unlink(missing_ok=True)
        prompt = (
            f"Read exactly this file and nothing else: {source_path}. "
            "Quote, verbatim and in double quotes, the sentence(s) that answer what it says. "
            f"Write your answer to exactly this path and no other: {output_path}. "
            "Do not modify, move, or write to any other file."
        )
        argv = [_npm_shim(cli), *argv_builder(prompt, output_path)]
        try:
            # `stdin=DEVNULL`: a CLI that waits on stdin for EOF or an interactive prompt
            # must not stall this route for the full timeout (Codex terra HIGH,
            # `docs/audits/2026-09-29-codex-lane-read-gate.md`) -- mirrors
            # `provider_bench.run_one`.
            proc = runner(
                argv, capture_output=True, text=True, timeout=timeout_s, check=False,
                stdin=subprocess.DEVNULL,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            return InvokeAttempt(None, log_text=str(exc), status="unavailable")
        log_text = (proc.stdout or "") + "\n" + (proc.stderr or "")
        return InvokeAttempt(
            output_path if output_path.exists() else None,
            log_text=log_text,
            status=f"exit={proc.returncode}",
        )

    return invoke


def _agy_argv(prompt: str, _output_path: Path) -> list[str]:
    """Mirrors `provider_bench._agy_args`: print mode soft-denies every tool without
    `--dangerously-skip-permissions`, and the prompt must be attached to `--print=` or the
    flag swallows the next argv entry."""
    return [
        "--output-format", "json", "--print-timeout=10m",
        "--dangerously-skip-permissions", f"--print={prompt}",
    ]


def _copilot_argv(prompt: str, _output_path: Path) -> list[str]:
    """Mirrors `provider_bench._copilot_args` (minus `--usage-output-file`, which this lane
    does not consume)."""
    return ["-p", prompt, "--allow-all-tools", "--no-ask-user", "--no-color"]


def agy_invoker(timeout_s: int = 600, *, runner: Callable[..., Any] = subprocess.run) -> Invoker:
    return _cli_invoker("agy", _agy_argv, timeout_s, runner=runner)


def copilot_invoker(
    timeout_s: int = 600, *, runner: Callable[..., Any] = subprocess.run
) -> Invoker:
    return _cli_invoker("copilot", _copilot_argv, timeout_s, runner=runner)


def real_invoker(
    route: RouteSpec, source_path: Path, workdir: Path, *, timeout_s: int = 600
) -> InvokeAttempt:
    """Dispatches on `route.provider` to the real, automatable invoker for a `roles.read`
    entry. Never used by a test -- DONE-ITEM 3's "no test calls a real reader".

    The `anthropic`/`claude-sonnet-5` entry is the registry's own "live terminal fallback":
    there is no CLI to shell out to for it, because it names the live Claude Code session
    itself. This function does NOT fabricate a read for it (a prior version did -- Codex
    terra CRITICAL, `docs/audits/2026-09-29-codex-lane-read-gate.md`: an automatic,
    always-succeeding stand-in for a route that is supposed to require a real reader defeats
    the whole gate for any future caller that reaches for `real_invoker` by default). A
    caller that is itself the live session and wants this route answered supplies its own
    `invoke` to `run_read_gate` for that one entry, same as any other injectable invoker."""
    if route.provider == "antigravity":
        return agy_invoker(timeout_s)(route, source_path, workdir)
    if route.provider == "copilot-enterprise":
        return copilot_invoker(timeout_s)(route, source_path, workdir)
    raise ReadGateError(
        f"no automated invoker for route {route.provider!r} -- "
        "the live terminal fallback is not automatable; supply your own invoker for it"
    )
