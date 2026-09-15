"""Price and verdict the provider CLIs installed on this box on ten real outcomes,
with nobody watching -- `[#772]`.

WHAT THIS IS AND WHAT IT IS NOT. It is a one-off MEASUREMENT harness, operator-invoked,
that makes real paid network calls. It is deliberately NOT on any commit-tier path and it
is not an organ: `[#676]` owns the enforcing invocation-shape check that belongs at commit
tier, and this module supplies that row its measured shapes as data. The night plan's rule
-- "no new organ without a trigger and a named consumer" -- is honoured by naming the
consumer rather than by inventing a trigger that would bill the operator on every commit.

THE THREE PROPERTIES THAT MAKE A RESULT HERE MEAN ANYTHING.

1. STDOUT-AND-VERIFY. Every outcome states its predicate BEFORE the run. The harness runs
   the CLI, captures stdout, stderr and the exit code, and evaluates the predicate against
   the captured text. Nothing is scored by reading an answer and agreeing with it.

2. ONE NEUTRAL WORKING DIRECTORY. Every provider is invoked from the SAME empty, non-git
   directory, and every prompt is self-contained. Without this the comparison is not a
   comparison: measured on this repo, `claude -p` run from the worktree loaded the project
   hooks and the governance doctrine, spent 139,611 tokens and $0.40 answering a five-word
   probe with a JOURNAL-anchor report, and the identical probe from a neutral directory
   cost $0.085 and answered the question. A benchmark that lets one contestant carry
   90 KB of house rules into the ring measures the house, not the contestant.

3. SELF-CONTAINED PROMPTS, BECAUSE THE FIELD INCLUDES A MODEL RUNNER. `ollama` has no tool
   layer at all -- it cannot open a file. A task set that half the field is physically
   unable to attempt prices nothing, so every outcome is a closed-form text task whose
   correct answer is fixed by the prompt itself.

PROMPTS ARE SINGLE-LINE PRINTABLE ASCII, and that is a transport constraint rather than a
preference. These CLIs reach us through npm `.cmd` shims; a multi-line prompt with an em
dash and embedded double quotes is corrupted by the shim (the child reports the prompt
"looks cut off"). `tests/test_provider_bench.py` asserts the constraint so a later editor
cannot quietly reintroduce it.

UNPRICED IS NOT FREE. Money comes from `provider_registry.resolve_rate`, which raises
`RateUnavailable` BY NAME for every model with no `rates:` row -- today every non-Anthropic
id. This module NEVER substitutes a zero and never divides a subscription price by its own
token count to manufacture a rate: it records the count, names the metering unit the vendor
actually bills in, and leaves the rate row to the registry's owner.

Consumers: `docs/audits/2026-09-15-technical-lane-z-4-non-claude-execution.md` (the packet
that reads the ledger), `logs/PROVIDER-BENCH-RUNS.jsonl` (the append-only ledger it writes),
`tests/test_provider_bench.py` (the witnesses).
"""
from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

import click

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT / "scripts") not in sys.path:      # dual-import shim, as the sibling
    sys.path.insert(0, str(REPO_ROOT / "scripts"))  # validators use

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("provider-bench")

#: The append-only run ledger. One JSON object per line, never rewritten.
LEDGER_REL = "logs/PROVIDER-BENCH-RUNS.jsonl"

#: Strips the terminal control sequences `ollama run` and `copilot -p` emit even when
#: stdout is a pipe. Without this the ollama capture is ~90% spinner frames and a predicate
#: reads a correct answer as absent.
_ANSI = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\][^\x07]*\x07|\x1b[=>]|[\x00-\x08\x0b\x0c\x0e-\x1f]")
#: The braille block, which is where every one of these CLIs draws its spinner. It is NOT a
#: control sequence -- it is printable text -- so the escape-code pass leaves it behind, and
#: what survives is a line like "⠋ [#762]". Harmless to a substring predicate and NOT
#: harmless to the budgeted-summary predicate, which counts words on the longest line and
#: would charge the model for a spinner frame. Stripped deliberately and narrowly: no answer
#: this benchmark asks for can legitimately contain braille.
_SPINNER = re.compile(r"[⠀-⣿]")


def strip_ansi(text: str) -> str:
    """Captured text with terminal control sequences and spinner glyphs removed, newlines
    preserved."""
    return _SPINNER.sub("", _ANSI.sub("", text))


# --- the ten outcomes -------------------------------------------------------------------
# Each is a real shape this repo performs by hand: pull an id out of a subject line, pick a
# class from a closed enum, author a regex for the branch enum, emit a JSON row, price a
# token count, locate a defect, REFUSE to answer what the text does not say, summarise to a
# budget, write a small function, order versions. The predicate for each is mechanical.


@dataclass(frozen=True)
class Outcome:
    """One bounded task and the predicate that decides it, stated before any run."""

    key: str
    prompt: str
    #: What "correct" means, in the operator's terms. Rendered in the packet verbatim.
    predicate_text: str
    #: `(cleaned_stdout) -> bool`. Pure; no network, no clock, no filesystem.
    predicate: Callable[[str], bool]


_ID_TOKEN = re.compile(r"\[#(\d{1,4})\]")
_ENUM_WORDS = ("technical", "functional", "qa", "census", "verification")
_TAG = re.compile(r"v\d+\.\d+\.\d+")


def _p_extract_id(out: str) -> bool:
    found = set(_ID_TOKEN.findall(out))
    return found == {"762"}


def _p_classify(out: str) -> bool:
    words = set(re.findall(r"[a-z]+", out.lower()))
    return "technical" in words and not (words & set(_ENUM_WORDS[1:]))


def _p_regex(out: str) -> bool:
    """Compile whatever the model emitted and run it against four positives and four
    negatives. A model that answers with prose rather than a pattern fails here, which is
    the point -- the deliverable was a pattern."""
    positives = ("worktree-lane-z-4", "epic/docs-cut", "claude/conformance-1", "automation/fleet-audit")
    # THE LAST FOUR NEGATIVES ARE THE ONES THAT DISCRIMINATE, and they were added after the
    # witness caught the predicate accepting a wrong answer. `^(worktree|epic|claude|
    # automation)` -- the separator-less near-miss a model actually tends to write -- passes
    # every positive AND every obvious negative, because `re.match` already anchors at the
    # start. Only a name that begins with the bare word and is not one of the four prefixes
    # tells the two patterns apart. A negative set that cannot fail the wrong answer is not a
    # test of anything.
    negatives = ("feat/thing", "main", "worktre-lane", "my-worktree-lane",
                 "worktreelane", "epicenter/x", "claudeish/y", "automationy/z")
    for line in _candidate_lines(out):
        try:
            rx = re.compile(line)
        except re.error:
            continue
        if all(rx.match(p) for p in positives) and not any(rx.match(n) for n in negatives):
            return True
    return False


def _p_json_shape(out: str) -> bool:
    want = {"id": "772", "status": "open", "size": "M"}
    for line in _candidate_lines(out):
        try:
            got = json.loads(line)
        except (ValueError, TypeError):
            continue
        if got == want:
            return True
    return False


def _p_pricing(out: str) -> bool:
    """31,000 input at $5.00/M plus 1,200 output at $25.00/M is $0.1850 exactly."""
    return bool(re.search(r"0\.185\b|0\.1850\b", out))


def _p_defect(out: str) -> bool:
    return "mean_b" in out and "mean_a" not in out and "mean_c" not in out


def _p_refusal(out: str) -> bool:
    return "NOT_DETERMINABLE" in out


def _p_summary(out: str) -> bool:
    """At most twenty words, and both required terms present. The longest non-empty line is
    taken as the sentence, so a model that prefixes a label is not punished for the label."""
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if not lines:
        return False
    sentence = max(lines, key=len)
    low = sentence.lower()
    return len(sentence.split()) <= 20 and "gate" in low and "refuses" in low


def _p_dedupe(out: str) -> bool:
    """Execute the emitted function. Nothing else proves a function works."""
    for block in _candidate_blocks(out):
        if "def dedupe" not in block:
            continue
        ns: dict[str, Any] = {}
        try:
            exec(block, ns)                                    # noqa: S102 -- the measurement
            fn = ns.get("dedupe")
            if fn is None:
                continue
            if fn([3, 1, 3, 2, 1]) == [3, 1, 2] and fn([]) == [] and fn(["a", "a"]) == ["a"]:
                return True
        except Exception:                                      # noqa: BLE001 -- a bad answer
            continue
    return False


def _p_ordering(out: str) -> bool:
    tags = _TAG.findall(out)
    want = ["v1.2.0", "v1.2.10", "v1.9.3", "v1.10.0"]
    return len(tags) >= 4 and tags[-4:] == want


def _candidate_lines(out: str) -> list[str]:
    """Every line worth trying, fences and common prefixes removed. A model told to emit
    one line and emitting three is wrong about terseness, not necessarily about content, and
    the two are scored separately."""
    seen: list[str] = []
    for raw in out.splitlines():
        line = raw.strip().strip("`").strip()
        if not line or line.startswith(("```", "#")):
            continue
        seen.append(line)
        if ":" in line:
            seen.append(line.split(":", 1)[1].strip())
    return seen


def _candidate_blocks(out: str) -> list[str]:
    """The whole capture, plus each fenced block in it -- so a fenced answer and a bare one
    are both reachable."""
    blocks = [out]
    fence = re.compile(r"```(?:python|py)?\n(.*?)```", re.DOTALL)
    blocks.extend(m.group(1) for m in fence.finditer(out))
    return blocks


OUTCOMES: tuple[Outcome, ...] = (
    Outcome(
        key="extract-id",
        # THE SQUARE-BRACKET CLAUSE WAS ADDED AFTER A FOUR-PROVIDER PILOT, and the amendment
        # is disclosed rather than absorbed. Without it, codex and copilot both answered
        # `#762` -- the right number, the wrong token -- while agy answered `[#762]`. A
        # predicate that fails two providers on a detail the prompt never asked for measures
        # the prompt, not the provider. The predicate is UNCHANGED and still strict; the ask
        # is now unambiguous, so a miss is a miss.
        prompt=("From the commit subject that follows, output ONLY the backlog id token, "
                "including its square brackets, and nothing else. Subject: docs(batch-y): "
                "the close packet with its seven numbers, and [#762] from this session own "
                "teardown"),
        predicate_text="the set of [#NNN] tokens in stdout is exactly {[#762]}",
        predicate=_p_extract_id,
    ),
    Outcome(
        key="classify-enum",
        prompt=("Classify the file name 2026-09-15-technical-lane-z-4-non-claude-execution.md "
                "by its class token. Choose exactly one word from this closed list: technical "
                "functional qa census verification. Output only that one word."),
        predicate_text="stdout contains 'technical' and none of the other four enum words",
        predicate=_p_classify,
    ),
    Outcome(
        key="regex-branch-prefix",
        prompt=("Output only a Python regular expression, with no code fence and no "
                "explanation, that matches a branch name if and only if it starts with one of "
                "these four prefixes: worktree- or epic/ or claude/ or automation/"),
        predicate_text=("some emitted line compiles as a regex and re.match is truthy for all "
                        "four of worktree-lane-z-4, epic/docs-cut, claude/conformance-1, "
                        "automation/fleet-audit and falsy for all eight of feat/thing, main, "
                        "worktre-lane, my-worktree-lane, worktreelane, epicenter/x, "
                        "claudeish/y, automationy/z"),
        predicate=_p_regex,
    ),
    Outcome(
        key="json-shape",
        prompt=("Output only one line of valid JSON, with no code fence and no explanation, "
                "having exactly the three keys id, status and size, where id is the string "
                "772, status is the string open and size is the string M."),
        predicate_text="some emitted line parses as JSON equal to {'id':'772','status':'open','size':'M'}",
        predicate=_p_json_shape,
    ),
    Outcome(
        key="arithmetic-pricing",
        prompt=("A run used 31000 input tokens billed at 5.00 US dollars per million tokens "
                "and 1200 output tokens billed at 25.00 US dollars per million tokens. Output "
                "only the total cost in US dollars, rounded to four decimal places."),
        predicate_text="stdout contains 0.185 or 0.1850",
        predicate=_p_pricing,
    ),
    Outcome(
        key="locate-defect",
        prompt=("Three Python functions follow, separated by three semicolons. Exactly one of "
                "them raises ZeroDivisionError when called with an empty list. Output only "
                "that function name. def mean_a(xs): return sum(xs)/max(len(xs),1) ;;; def "
                "mean_b(xs): return sum(xs)/len(xs) ;;; def mean_c(xs): return sum(xs)/len(xs) "
                "if xs else 0"),
        predicate_text="stdout names mean_b and names neither mean_a nor mean_c",
        predicate=_p_defect,
    ),
    Outcome(
        key="honest-refusal",
        prompt=("Using ONLY the sentence that follows as evidence, state how many commits "
                "landed on main in August 2026. If the sentence does not contain the answer, "
                "output exactly NOT_DETERMINABLE and nothing else. The sentence: the batch "
                "closed with seven numbers and one defined median."),
        predicate_text="stdout contains NOT_DETERMINABLE",
        predicate=_p_refusal,
    ),
    Outcome(
        key="summary-budget",
        prompt=("Summarise the text that follows in one sentence of at most 20 words, using "
                "both the word gate and the word refuses. Output only the sentence. Text: a "
                "pre-commit hook reads the staged set and refuses any file that no open "
                "backlog row claims."),
        predicate_text=("the longest non-empty line is at most 20 words and contains both "
                        "'gate' and 'refuses' case-insensitively"),
        predicate=_p_summary,
    ),
    Outcome(
        key="write-function",
        prompt=("Output only a Python function, with no explanation, named dedupe that takes "
                "one list argument and returns a new list with duplicates removed while "
                "preserving first-occurrence order."),
        predicate_text=("the emitted source executes and the resulting dedupe returns [3,1,2] "
                        "for [3,1,3,2,1], [] for [] and ['a'] for ['a','a']"),
        predicate=_p_dedupe,
    ),
    Outcome(
        key="order-versions",
        prompt=("Sort these four release tags by semantic version, lowest first, and output "
                "only the four tags separated by single spaces: v1.10.0 v1.2.0 v1.2.10 v1.9.3"),
        predicate_text="the last four version tags in stdout are v1.2.0 v1.2.10 v1.9.3 v1.10.0 in that order",
        predicate=_p_ordering,
    ),
)

OUTCOME_KEYS: tuple[str, ...] = tuple(o.key for o in OUTCOMES)

#: A prompt must survive an npm `.cmd` shim. Printable ASCII, one line, no double quote.
PROMPT_CHARSET = re.compile(r"^[ -~]+$")


# --- the providers ----------------------------------------------------------------------
# Every invocation shape below was ESTABLISHED BY RUNNING IT, never by reading a help page.
# The traps each flag defuses are named, because a flag whose reason is unrecorded is the
# first thing a later editor removes.


@dataclass(frozen=True)
class Provider:
    """One CLI, the exact argv that reaches it unattended, and how to read its usage."""

    key: str
    #: Resolved at call time -- an npm global is a `.cmd` shim on Windows and `CreateProcess`
    #: does not consult PATHEXT, so a bare name raises WinError 2 from Python.
    executable: str
    args: Callable[[str, Path], list[str]]
    #: How the served model and the token counts are read back out of this CLI.
    parse: Callable[["ProviderRun"], None]
    #: What the vendor actually bills for. Naming it is the honest alternative to a
    #: manufactured per-token rate.
    metering_unit: str
    note: str = ""
    #: Set when a run needs a scratch file (copilot's `--usage-output-file`).
    wants_usage_file: bool = False


@dataclass
class ProviderRun:
    """One (provider, outcome) invocation and everything read back off it."""

    provider: str
    outcome: str
    argv: list[str] = field(default_factory=list)
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    wall_seconds: float = 0.0
    served_model: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cache_read_tokens: Optional[int] = None
    cache_write_tokens: Optional[int] = None
    #: The vendor's own billing counter, where it exposes one (copilot premium requests).
    vendor_units: Optional[float] = None
    usage_path: Optional[Path] = None
    #: True unless the CLI stopped on something only a human could answer.
    unattended: bool = True
    blocking_prompt: Optional[str] = None
    error: Optional[str] = None
    #: WHERE the served-model id came from, in the CLI's own words. Standing ruling Q9 makes
    #: the substitution probe a hard precondition, so "which model answered" is never allowed
    #: to be a guess: a provider that discloses nothing records `none` and is reported as
    #: UNREPRODUCIBLE rather than quietly credited with its configured default.
    model_attestation: str = "none"
    #: The vendor's own correlation handle for this call, kept so a later reader can rejoin a
    #: row to the CLI's log without re-running anything.
    vendor_call_id: Optional[str] = None


def _npm_shim(name: str) -> str:
    """The `.cmd` next to an npm global, or the bare name off PATH elsewhere."""
    if os.name == "nt":
        cmd = shutil.which(f"{name}.cmd")
        if cmd:
            return cmd
    found = shutil.which(name)
    return found or name


def _codex_args(prompt: str, _tmp: Path) -> list[str]:
    # `codex exec` reads stdin as ADDITIONAL prompt input and waits for EOF, so a
    # tool-spawned process hangs forever with a 0-byte capture. The runner closes stdin;
    # the flag set itself carries no model pin, so the box's configured default answers and
    # is READ BACK off the header rather than assumed.
    return ["exec", prompt]


def _copilot_args(prompt: str, tmp: Path) -> list[str]:
    # `--model` refuses EVERY id on this host, including the three `copilot help config`
    # documents, while a call with no `--model` answers fine -- so the served model is
    # knowable only after the fact, from `--usage-output-file`. `--allow-all-tools` is
    # required for non-interactive mode; `--no-ask-user` removes the one tool that can stop
    # an unattended run dead.
    return ["-p", prompt, "--allow-all-tools", "--no-ask-user", "--no-color",
            "--usage-output-file", str(tmp)]


def _gemini_args(prompt: str, _tmp: Path) -> list[str]:
    return ["-p", prompt]


def _ollama_args(prompt: str, _tmp: Path) -> list[str]:
    # `--verbose` is the only way this CLI discloses token counts at all, and it prints them
    # to stderr while the answer goes to stdout.
    return ["run", "--verbose", OLLAMA_MODEL, prompt]


def _agy_args(prompt: str, _tmp: Path) -> list[str]:
    # `--print` alone SOFT-DENIES every tool and returns an empty response at
    # status=CANCELED after burning real tokens; `--dangerously-skip-permissions` is what
    # makes a print-mode run answer. `--sandbox` is deliberately absent: with it the same
    # item ran 604 s and died at "timeout waiting for response". The prompt must be ATTACHED
    # to the flag or `--print` swallows the next flag as its prompt.
    return ["--output-format", "json", "--print-timeout=10m",
            "--dangerously-skip-permissions", f"--print={prompt}"]


def _claude_args(prompt: str, _tmp: Path) -> list[str]:
    # `--setting-sources local` is load-bearing and is the control that makes this leg a
    # COMPARISON: without it the child loads this repo's project hooks and answers the Stop
    # backpressure hook instead of the prompt. Run from the neutral directory it also sees
    # no CLAUDE.md, which is the same starting position every other CLI here gets.
    return ["-p", prompt, "--model", CLAUDE_MODEL, "--setting-sources", "local",
            "--output-format", "json", "--permission-mode", "bypassPermissions"]


#: The local model this harness runs. `ollama list` on this box also carries llama3.2:3b;
#: the coder model is the fair comparator for a field of coding assistants, and the small
#: one is reported separately rather than blended in.
OLLAMA_MODEL = "qwen2.5-coder:14b"
#: The comparison leg. `opus` is an alias the CLI resolves; the CANONICAL id comes back in
#: the result envelope and is what gets priced.
CLAUDE_MODEL = "opus"


_CODEX_MODEL = re.compile(r"^\s*model:\s*(\S+)\s*$", re.MULTILINE)
_CODEX_TOKENS = re.compile(r"tokens used\s*\n\s*([\d,]+)", re.MULTILINE)
_OLLAMA_PROMPT_EVAL = re.compile(r"prompt eval count:\s*(\d+)")
_OLLAMA_EVAL = re.compile(r"\beval count:\s*(\d+)")
_AGY_MODEL_LOG = re.compile(r"Resolving model (\S+)")


def _parse_codex(run: ProviderRun) -> None:
    # THE HEADER GOES TO STDERR WHEN STDOUT IS A PIPE, and stdout carries the answer alone.
    # Measured in the pilot: parsing stdout only returned `served_model: None` on a run that
    # had plainly declared its model. Both streams are searched, in that order.
    body = strip_ansi(run.stdout) + "\n" + strip_ansi(run.stderr)
    m = _CODEX_MODEL.search(body)
    run.served_model = m.group(1) if m else None
    run.model_attestation = "codex exec session header (`model:` line on stderr)" if m else "none"
    t = _CODEX_TOKENS.search(body)
    if t:
        # `codex exec` reports ONE total, not a split. Recording it as input would price a
        # number the vendor never quoted; it goes in its own field and the report says so.
        run.vendor_units = float(t.group(1).replace(",", ""))


def _parse_copilot(run: ProviderRun) -> None:
    if not run.usage_path or not run.usage_path.exists():
        return
    try:
        usage = json.loads(run.usage_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:                       # pragma: no cover -- vendor file
        run.error = f"usage file unreadable: {exc}"
        return
    metrics = usage.get("modelMetrics") or {}
    if metrics:
        run.served_model = sorted(metrics)[0]
        run.model_attestation = "copilot --usage-output-file modelMetrics key (post-hoc only)"
    details = usage.get("tokenDetails") or {}
    run.input_tokens = (details.get("input") or {}).get("tokenCount")
    run.output_tokens = (details.get("output") or {}).get("tokenCount")
    run.cache_read_tokens = (details.get("cache_read") or {}).get("tokenCount")
    run.cache_write_tokens = (details.get("cache_write") or {}).get("tokenCount")
    run.vendor_units = usage.get("totalPremiumRequestCost")


def _parse_gemini(run: ProviderRun) -> None:
    # Nothing to parse: this client is refused at authentication before a model is chosen.
    # The refusal text itself is the result and is captured in `stderr`.
    return


def _parse_ollama(run: ProviderRun) -> None:
    # The ONE provider whose served model needs no attestation machinery: the weights are on
    # this disk and the id is the argument. There is no server that could substitute one.
    run.served_model = OLLAMA_MODEL
    run.model_attestation = "the local weights named on the command line; no remote to substitute"
    both = strip_ansi(run.stdout) + "\n" + strip_ansi(run.stderr)
    pe = _OLLAMA_PROMPT_EVAL.search(both)
    ev = _OLLAMA_EVAL.search(both)
    run.input_tokens = int(pe.group(1)) if pe else None
    run.output_tokens = int(ev.group(1)) if ev else None


def _parse_agy(run: ProviderRun) -> None:
    envelope = _last_json_object(strip_ansi(run.stdout))
    if envelope is None:
        return
    usage = envelope.get("usage") or {}
    run.input_tokens = usage.get("input_tokens")
    run.output_tokens = usage.get("output_tokens")
    run.cache_read_tokens = usage.get("cache_read_tokens")
    run.vendor_call_id = envelope.get("conversation_id")
    denied = envelope.get("denied_actions") or []
    empty = not (envelope.get("response") or "").strip()
    if empty and (denied or envelope.get("status") == "CANCELED"):
        # THE SOFT-DENY CHANGED SHAPE IN 1.2.2 AND THE OLD DETECTOR WOULD HAVE MISSED IT.
        # On 1.1.x it was `status: CANCELED` with an empty response. Measured here on 1.2.2 it
        # is `status: SUCCESS`, an empty response, 1,342 output tokens spent, and a new
        # `denied_actions` array carrying the refusal. A detector keyed on CANCELED alone reads
        # that as a model that answered with nothing -- which is exactly the misdiagnosis
        # `[#676]` was filed over, in a new costume. Emptiness plus EITHER signal is the test.
        run.unattended = False
        reason = json.dumps(denied)[:160] if denied else "status=CANCELED"
        run.blocking_prompt = f"print mode soft-denied a tool confirmation ({reason})"
    run.served_model = _agy_served_model(envelope.get("conversation_id"))
    run.model_attestation = (AGY_ATTESTATION_LOG if run.served_model else AGY_ATTESTATION_NONE)
    run.stdout = str(envelope.get("response") or run.stdout)


AGY_ATTESTATION_LOG = "agy CLI log `Resolving model` line, bound by conversation_id"
#: MEASURED ON 1.2.2, not assumed. The JSON envelope carries conversation_id / status /
#: response / duration / num_turns / usage and NO model field, and the `model_resolver.go:80]
#: Resolving model <id>` line the 1.1.x builds wrote is absent from the current logs (zero
#: hits across every `cli-*.log` on this box). So on this build the served id is disclosed
#: NOWHERE, which by the registry's own `cursor` precedent makes an agy result
#: UNREPRODUCIBLE -- a verdict about the CLI, not a defect in this reader.
AGY_ATTESTATION_NONE = ("none -- agy 1.2.2 discloses no model id in its JSON envelope and its "
                        "log no longer carries the 1.1.x `Resolving model` line")


def _agy_served_model(conversation_id: Optional[str]) -> Optional[str]:
    """The Q9 served-id attestation, which the JSON envelope does not carry. The 1.1.x CLI
    log did, bound by conversation_id so parallel runs still joined log to item exactly.
    Kept because the line may return; absent log, absent line, absent id -- never a guess."""
    if not conversation_id:
        return None
    log_dir = Path.home() / ".gemini" / "antigravity-cli" / "log"
    if not log_dir.is_dir():
        return None
    for log in sorted(log_dir.glob("cli-*.log"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]:
        try:
            text = log.read_text(encoding="utf-8", errors="replace")
        except OSError:                                        # pragma: no cover -- vendor file
            continue
        if conversation_id not in text:
            continue
        found = _AGY_MODEL_LOG.findall(text)
        if found:
            return found[-1]
    return None


def _parse_claude(run: ProviderRun) -> None:
    envelope = _last_json_object(strip_ansi(run.stdout))
    if envelope is None:
        return
    usage = envelope.get("modelUsage") or {}
    # The session also bills a small Haiku side-call for its own bookkeeping. Every model
    # the envelope names is recorded; the PRIMARY is the one carrying the output tokens, and
    # the secondary spend is reported rather than dropped, because it is really billed.
    primary = max(usage, key=lambda k: usage[k].get("outputTokens", 0)) if usage else None
    run.served_model = primary
    run.vendor_call_id = envelope.get("session_id")
    if primary:
        run.model_attestation = "claude result envelope modelUsage (canonical id, per invocation)"
        row = usage[primary]
        run.input_tokens = row.get("inputTokens")
        run.output_tokens = row.get("outputTokens")
        run.cache_read_tokens = row.get("cacheReadInputTokens")
        run.cache_write_tokens = row.get("cacheCreationInputTokens")
    run.vendor_units = envelope.get("total_cost_usd")
    run.stdout = str(envelope.get("result") or run.stdout)


def _last_json_object(text: str) -> Optional[dict]:
    """The last line that parses as a JSON object. These CLIs print progress before the
    envelope, so 'the last object' is the envelope and 'the first' is noise."""
    for line in reversed([ln.strip() for ln in text.splitlines() if ln.strip()]):
        if not line.startswith("{"):
            continue
        try:
            got = json.loads(line)
        except ValueError:
            continue
        if isinstance(got, dict):
            return got
    return None


PROVIDERS: dict[str, Provider] = {
    "codex": Provider(
        key="codex", executable="codex", args=_codex_args, parse=_parse_codex,
        metering_unit="ChatGPT plan quota; the CLI reports ONE total token figure, not a split",
        note="stdin must be closed or `codex exec` blocks forever with a 0-byte capture",
    ),
    "copilot": Provider(
        key="copilot", executable="copilot", args=_copilot_args, parse=_parse_copilot,
        metering_unit="GitHub Copilot PREMIUM REQUESTS (and nano-AIU), not tokens",
        note="`--model` refuses every id on this host; the served model is post-hoc only",
        wants_usage_file=True,
    ),
    "gemini": Provider(
        key="gemini", executable="gemini", args=_gemini_args, parse=_parse_gemini,
        metering_unit="Gemini Code Assist tier quota",
        note="refused at authentication on this account",
    ),
    "ollama": Provider(
        key="ollama", executable="ollama", args=_ollama_args, parse=_parse_ollama,
        metering_unit="none -- local inference, no vendor bill; the cost is wall time and RAM",
        note="needs a running server on 127.0.0.1:11434",
    ),
    "agy": Provider(
        key="agy", executable="agy", args=_agy_args, parse=_parse_agy,
        metering_unit="Antigravity subscription quota",
        note="print mode soft-denies tools without --dangerously-skip-permissions",
    ),
    "claude": Provider(
        key="claude", executable="claude", args=_claude_args, parse=_parse_claude,
        metering_unit="Anthropic first-party per-token list price -- the ONE priced leg",
        note="the comparison baseline; --setting-sources local keeps repo doctrine out",
    ),
}

#: The contract's in-scope set. `claude` is the comparison leg and is not one of them.
IN_SCOPE: tuple[str, ...] = ("copilot", "codex", "gemini", "ollama", "agy")
#: Named in the frozen contract as ABSENT. Re-measured rather than believed.
DECLARED_ABSENT: tuple[str, ...] = ("cursor-agent", "aider", "llm", "amp")

#: Phrases that mean a CLI stopped on something only a human can answer. Matched against the
#: whole capture; a hit sets `unattended: false` and the matched text is quoted.
BLOCKING_PATTERNS: tuple[tuple[str, str], ...] = (
    ("Workspace Trust Required", "cursor-agent stops on a Workspace Trust prompt"),
    ("Please run /login", "the CLI demands an interactive login"),
    ("Press Enter to continue", "the CLI waits on a keypress"),
    ("? Do you want to", "the CLI asks a yes/no question"),
    ("ask_user", "the CLI reached its ask-the-human tool"),
)


def detect_blocking(capture: str) -> Optional[str]:
    """The exact blocking text, quoted, or None. Recording the QUOTE rather than a boolean
    is what makes `unattended: false` a result a later reader can act on."""
    for needle, _why in BLOCKING_PATTERNS:
        idx = capture.find(needle)
        if idx >= 0:
            return capture[idx:idx + 200].strip()
    return None


# --- running ----------------------------------------------------------------------------


def bench_cwd(root: Optional[Path] = None) -> Path:
    """The ONE neutral, empty, non-git directory every provider is invoked from."""
    base = root or Path(os.environ.get("CLAUDE_JOB_DIR", REPO_ROOT / ".bench")) / "tmp"
    path = base / "bench-cwd"
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_one(provider: Provider, outcome: Outcome, *, cwd: Path,
            timeout: int = 900) -> ProviderRun:
    """One invocation, captured whole. Never raises on a provider failure -- a CLI that
    dies is a RESULT and is recorded as one."""
    run = ProviderRun(provider=provider.key, outcome=outcome.key)
    tmp = cwd / f"usage-{provider.key}-{outcome.key}.json"
    if provider.wants_usage_file:
        run.usage_path = tmp
        tmp.unlink(missing_ok=True)
    exe = _npm_shim(provider.executable)
    run.argv = [exe, *provider.args(outcome.prompt, tmp)]
    started = time.monotonic()
    try:
        proc = subprocess.run(                                 # noqa: S603 -- the measurement
            run.argv, cwd=str(cwd), capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            stdin=subprocess.DEVNULL, timeout=timeout, check=False,
        )
        run.exit_code, run.stdout, run.stderr = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        run.error = f"timed out after {timeout}s"
        run.unattended = False
        run.blocking_prompt = f"no exit within {timeout}s with stdin closed"
    except OSError as exc:
        run.error = f"could not start: {exc}"
    run.wall_seconds = round(time.monotonic() - started, 3)

    if run.error is None:
        quoted = detect_blocking(strip_ansi(run.stdout) + "\n" + strip_ansi(run.stderr))
        if quoted:
            run.unattended = False
            run.blocking_prompt = quoted
        try:
            provider.parse(run)
        except Exception as exc:                               # noqa: BLE001 -- vendor output
            run.error = f"usage parse failed: {type(exc).__name__}: {exc}"
    return run


def score(run: ProviderRun, outcome: Outcome) -> dict[str, Any]:
    """The predicate verdict plus the terseness observation, kept apart on purpose. Getting
    the answer right and obeying 'output only' are two different findings, and a scorer that
    folds them reports neither."""
    cleaned = strip_ansi(run.stdout)
    body_lines = [ln for ln in cleaned.splitlines() if ln.strip()]
    passed = False
    if run.error is None and run.unattended:
        try:
            passed = bool(outcome.predicate(cleaned))
        except Exception as exc:                               # noqa: BLE001 -- a bad answer
            logger.warning("predicate raised for %s/%s: %s", run.provider, outcome.key, exc)
    return {"predicate_pass": passed, "terse": len(body_lines) <= 3,
            "answer_lines": len(body_lines)}


def price(run: ProviderRun, registry_path: Optional[Path] = None) -> dict[str, Any]:
    """USD for this run, or the named refusal. NEVER a zero for an unknown rate."""
    import provider_registry as pr                             # noqa: PLC0415 -- sibling

    model = run.served_model
    if not model:
        return {"usd": None, "unpriced_reason": "no served model was attested for this run"}
    try:
        rate = pr.resolve_rate(model, registry_path)
    except pr.RateUnavailable as exc:
        return {"usd": None, "unpriced_reason": str(exc)}
    usd = rate.usd(
        input_tokens=run.input_tokens or 0,
        output_tokens=run.output_tokens or 0,
        cache_write_tokens=run.cache_write_tokens or 0,
        cache_read_tokens=run.cache_read_tokens or 0,
    )
    return {"usd": round(usd, 6), "rate_as_of": rate.as_of, "currency": rate.currency,
            "unpriced_reason": None}


def record(run: ProviderRun, outcome: Outcome, *,
           registry_path: Optional[Path] = None) -> dict[str, Any]:
    """One ledger row: what was asked, what came back, what it cost, and how it was judged."""
    row: dict[str, Any] = {
        "row": ROW,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "provider": run.provider,
        "outcome": run.outcome,
        "served_model": run.served_model,
        "model_attestation": run.model_attestation,
        "vendor_call_id": run.vendor_call_id,
        "exit_code": run.exit_code,
        "wall_seconds": run.wall_seconds,
        "unattended": run.unattended,
        "blocking_prompt": run.blocking_prompt,
        "error": run.error,
        "input_tokens": run.input_tokens,
        "output_tokens": run.output_tokens,
        "cache_read_tokens": run.cache_read_tokens,
        "cache_write_tokens": run.cache_write_tokens,
        "vendor_units": run.vendor_units,
        "metering_unit": PROVIDERS[run.provider].metering_unit,
        "predicate_text": outcome.predicate_text,
        "stdout_head": strip_ansi(run.stdout)[:400],
        "stderr_head": strip_ansi(run.stderr)[:400],
    }
    row.update(score(run, outcome))
    row.update(price(run, registry_path))
    return row


def append_ledger(rows: list[dict[str, Any]], ledger: Path) -> None:
    """Append-only, one object per line. Never rewrites an existing byte."""
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


#: The row every artifact this module writes belongs to. Carried INSIDE each artifact, not
#: only in the row's body: `graph-task-coverage` accepts the claim from either direction, and
#: a file that names its own row stays claimed even if the row's prose is later rewritten.
ROW = "[#772]"


def _write_json(path: Path, payload: Any) -> None:
    """Pretty JSON with LF endings, ALWAYS, wrapped so the artifact names its own row.

    `Path.write_text` uses the platform newline, so on Windows it emits CRLF and git greets
    every committed artifact with a conversion warning -- and a stray CR is the thing that
    breaks a later byte-split read of the same file.
    """
    envelope = {"row": ROW, "generated_by": "scripts/provider_bench.py", "rows": payload}
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(envelope, indent=2, ensure_ascii=False) + "\n")


def read_ledger(ledger: Path) -> list[dict[str, Any]]:
    if not ledger.exists():
        return []
    out = []
    for line in ledger.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def census(*, probe_versions: bool = True) -> list[dict[str, Any]]:
    """Presence and version for every provider this contract names, in scope or declared
    absent. Presence is `shutil.which`, never a belief.

    `probe_versions=False` is the offline half. It exists because the suite needs to assert
    WHICH names get probed without spawning ten processes on a machine where one of them may
    block on a server socket -- a test whose runtime depends on a daemon being up is a test
    that reports the daemon.
    """
    rows = []
    for key in (*IN_SCOPE, "claude", *DECLARED_ABSENT):
        exe = _npm_shim(key)
        present = shutil.which(exe) is not None or Path(exe).exists()
        version = None
        if present and probe_versions:
            try:
                proc = subprocess.run(                         # noqa: S603 -- the measurement
                    [exe, "--version"], capture_output=True, text=True,
                    encoding="utf-8", errors="replace",
                    stdin=subprocess.DEVNULL, timeout=120, check=False)
                version = strip_ansi((proc.stdout or proc.stderr)).strip().splitlines()
                version = version[0] if version else None
            except (OSError, subprocess.TimeoutExpired) as exc:
                version = f"version probe failed: {exc}"
        rows.append({"provider": key, "present": present, "resolved": exe if present else None,
                     "version": version,
                     "declared": "in-scope" if key in IN_SCOPE
                     else ("baseline" if key == "claude" else "declared-absent")})
    return rows


# --- the recorded traps, VERIFIED rather than trusted ------------------------------------
# The frozen contract names three traps from earlier lanes and says to verify them rather
# than trust them. A trap carried forward on faith is indistinguishable from a trap that was
# fixed upstream three releases ago, and the second kind silently costs a capability.

#: A tiny prompt: the trap under test is the INVOCATION, so the task must not be able to fail.
TRAP_PROMPT = "Reply with exactly: TRAP_PROBE_OK"
#: Real model ids to try against copilot's `--model`. The first two are ids `copilot help
#: config` itself documents, which is what made the 2026-09-09 refusal a documentation defect
#: rather than a user error.
COPILOT_MODEL_IDS: tuple[str, ...] = ("claude-sonnet-5", "claude-fable-5.1", "gpt-5")
#: NOT A MODEL, AND THAT IS WHY IT IS HERE. `auto` is a selection MODE the CLI's own help
#: documents, and it is ACCEPTED. It is the negative control that keeps the verdict honest in
#: both directions: it proves the flag is wired and parsed, so "every id refused" is a
#: statement about model ids rather than about a dead flag. Counting it among the candidates
#: is a defect this lane made and caught -- `all(refused)` then went False on one accepted
#: non-model and reported a standing finding as RETRACTED, which would have re-opened an
#: admission verdict on the strength of a word that names no model.
COPILOT_MODEL_CONTROL = "auto"


#: Trap key -> prober. Keyed so one trap can be re-probed alone: these are PAID calls, and
#: re-running the whole set to re-check one of them bills the other two for nothing.
TRAP_PROBES: dict[str, Callable[[Path, int], dict[str, Any]]] = {
    "copilot-model": lambda cwd, t: _trap_copilot_model(cwd, t),
    "codex-stdin": lambda cwd, t: _trap_codex_stdin(cwd, t),
    "agy-soft-deny": lambda cwd, t: _trap_agy_soft_deny(cwd, t),
}


def verify_traps(cwd: Path, *, short_timeout: int = 90,
                 only: tuple[str, ...] = ()) -> list[dict[str, Any]]:
    """Run each recorded trap and report whether it still bites, with the evidence."""
    keys = [k for k in TRAP_PROBES if not only or k in only]
    return [TRAP_PROBES[k](cwd, short_timeout) for k in keys]


def _capture(argv: list[str], cwd: Path, timeout: int, *,
             stdin_open: bool = False) -> tuple[Optional[int], str, Optional[str]]:
    """`(exit_code, combined_output, error)`. `stdin_open=True` leaves stdin attached to an
    empty pipe that is never closed -- the exact condition that wedges `codex exec`."""
    try:
        proc = subprocess.run(                                 # noqa: S603 -- the measurement
            argv, cwd=str(cwd), capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            stdin=(subprocess.PIPE if stdin_open else subprocess.DEVNULL),
            timeout=timeout, check=False)
        return proc.returncode, strip_ansi(proc.stdout) + strip_ansi(proc.stderr), None
    except subprocess.TimeoutExpired as exc:
        got = (exc.stdout or b"") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        body = got.decode("utf-8", "replace") if isinstance(got, bytes) else got
        return None, strip_ansi(body), f"no exit within {timeout}s"
    except OSError as exc:
        return None, "", f"could not start: {exc}"


def _trap_copilot_model(cwd: Path, timeout: int) -> dict[str, Any]:
    """Trap 1: `copilot --model` has refused every id tried, including its own documented
    three, while a call with no flag answers."""
    exe = _npm_shim("copilot")

    def _try(mid: str) -> dict[str, Any]:
        code, body, err = _capture(
            [exe, "-p", TRAP_PROMPT, "--allow-all-tools", "--no-ask-user", "--no-color",
             "--model", mid], cwd, timeout)
        return {"exit_code": code, "refused": "is not available" in body or code not in (0, None),
                "evidence": body.strip()[:200], "error": err}

    tried = {mid: _try(mid) for mid in COPILOT_MODEL_IDS}
    control = _try(COPILOT_MODEL_CONTROL)
    every_id_refused = all(v["refused"] for v in tried.values())
    still_bites = every_id_refused and not control["refused"]
    return {"trap": "copilot --model refuses every real model id",
            "still_bites": still_bites,
            "detail": {"model_ids": tried, f"control:{COPILOT_MODEL_CONTROL}": control},
            "meaning": ("every real id is refused while the `auto` control is accepted, so the "
                        "flag is live and the caller still cannot pin a model -- a copilot "
                        "result remains unreproducible" if still_bites else
                        "a real model id was ACCEPTED, or the control was refused; read the "
                        "evidence before touching any verdict that rested on this")}


def _really_open_stdin(argv: list[str], cwd: Path, timeout: int) -> tuple[Optional[int], str, Optional[str]]:
    """Run with a stdin pipe that is genuinely HELD OPEN for the whole wait.

    `subprocess.run(stdin=PIPE)` does NOT do this: `communicate()` closes the write end
    immediately, so the child sees EOF at once. A first version of this probe used it, watched
    the "open" leg finish normally, and was one line away from publishing "the stdin trap no
    longer bites" -- a retraction of a standing finding produced entirely by the instrument.
    `Popen` with the handle left alone is what actually reproduces a background lane's stdin.
    Output goes to files rather than pipes so an unread pipe buffer cannot deadlock the child
    and be mistaken for the hang under test.
    """
    out_path = cwd / "trap-stdout.txt"
    err_path = cwd / "trap-stderr.txt"
    with out_path.open("w", encoding="utf-8") as out, err_path.open("w", encoding="utf-8") as err:
        proc = subprocess.Popen(                               # noqa: S603 -- the measurement
            argv, cwd=str(cwd), stdin=subprocess.PIPE, stdout=out, stderr=err, text=True)
        try:
            code: Optional[int] = proc.wait(timeout=timeout)
            error = None
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=30)
            code, error = None, f"no exit within {timeout}s with stdin held open"
        finally:
            if proc.stdin and not proc.stdin.closed:
                proc.stdin.close()
    body = out_path.read_text(encoding="utf-8", errors="replace") + \
        err_path.read_text(encoding="utf-8", errors="replace")
    return code, strip_ansi(body), error


def _trap_codex_stdin(cwd: Path, timeout: int) -> dict[str, Any]:
    """Trap 2: `codex exec` reads stdin as ADDITIONAL prompt and waits for EOF, so a
    tool-spawned process hangs forever with an empty capture even though the prompt was an
    argument. Verified by running it BOTH ways against the same prompt -- and the "open" way
    has to be genuinely open, which is the whole difficulty."""
    exe = _npm_shim("codex")
    open_code, open_body, open_err = _really_open_stdin([exe, "exec", TRAP_PROMPT], cwd, timeout)
    closed_code, closed_body, closed_err = _capture(
        [exe, "exec", TRAP_PROMPT], cwd, timeout, stdin_open=False)
    hung = open_err is not None and closed_err is None
    return {"trap": "codex exec blocks on a stdin that is never closed", "still_bites": hung,
            "detail": {
                "stdin_held_open": {"exit_code": open_code, "error": open_err,
                                    "evidence": open_body.strip()[:300]},
                "stdin_closed": {"exit_code": closed_code, "error": closed_err,
                                 "evidence": closed_body.strip()[:300]}},
            "meaning": ("stdin must be closed by the caller; the announcement 'Reading "
                        "additional input from stdin...' is the tell" if hung else
                        "the held-open run ALSO completed -- on this build the announcement "
                        "is printed but no longer waits")}


def _trap_agy_soft_deny(cwd: Path, timeout: int) -> dict[str, Any]:
    """Trap 3: `agy --print` soft-denies every filesystem tool and returns an empty response
    at status=CANCELED unless `--dangerously-skip-permissions` is passed. Probed with a task
    that CANNOT be answered without a tool, both with and without the flag."""
    exe = _npm_shim("agy")
    probe = ("List the file names in the current working directory. Output only the names, "
             "one per line. If you cannot read the directory, output exactly TOOL_DENIED.")
    (cwd / "trap-marker.txt").write_text("marker\n", encoding="utf-8")
    without_code, without_body, without_err = _capture(
        [exe, "--output-format", "json", "--print-timeout=5m", f"--print={probe}"],
        cwd, timeout)
    with_code, with_body, with_err = _capture(
        [exe, "--output-format", "json", "--print-timeout=5m",
         "--dangerously-skip-permissions", f"--print={probe}"], cwd, timeout)
    # `denied_actions` is the 1.2.2 signal; CANCELED was the 1.1.x one; TOOL_DENIED is the
    # model saying so itself.
    denied = ("denied_actions" in without_body or "CANCELED" in without_body
              or "TOOL_DENIED" in without_body)
    allowed = "trap-marker" in with_body
    # THE VERDICT IS THE DENY HALF ALONE, and separating the two legs was forced by a verdict
    # that FLIPPED between two runs of the same probe. The without-flag deny reproduced both
    # times; the with-flag leg answered correctly once (99.9 s) and once rambled -- "I have
    # launched the check and will wait for it to complete" -- before emitting TOOL_DENIED with
    # permissions it actually held. Conjoining them made a stable finding about permissions
    # depend on an unstable one about reliability, so the boolean tracked agy's mood. The
    # trap's own claim is "print mode denies without the flag", the remedy is "pass the flag",
    # and neither moves with the second leg. It is reported beside, never folded in.
    return {"trap": "agy print mode soft-denies tools without --dangerously-skip-permissions",
            "still_bites": bool(denied),
            "flagged_run_answered": bool(allowed),
            "detail": {
                "without_flag": {"exit_code": without_code, "error": without_err,
                                 "evidence": without_body.strip()[:300]},
                "with_flag": {"exit_code": with_code, "error": with_err,
                              "evidence": with_body.strip()[:300]}},
            "meaning": ("the flag is mandatory for any agy run that must touch a file"
                        + ("" if allowed else
                           "; SEPARATELY, the flagged run did NOT complete the task this time "
                           "-- a reliability observation, not a permissions one")
                        if denied else
                        "the unflagged run was NOT denied -- read the evidence before touching "
                        "any verdict that rested on this")}


# --- CLI --------------------------------------------------------------------------------


@click.group(help=__doc__.split("\n\n")[0])
def cli() -> None:
    """Entry point. Subcommands are census / run / report."""


@cli.command("census")
@click.option("--json-out", type=click.Path(path_type=Path), default=None,
              help="write the census rows here as JSON as well as logging them")
def cmd_census(json_out: Optional[Path]) -> None:
    """Presence and version for every provider the contract names."""
    rows = census()
    for row in rows:
        logger.info("%-13s %-15s %s", row["provider"],
                    "PRESENT" if row["present"] else "ABSENT", row["version"] or "")
    if json_out:
        _write_json(json_out, rows)
        logger.info("census written to %s", json_out)


@cli.command("traps")
@click.option("--json-out", type=click.Path(path_type=Path), default=None,
              help="write the trap verdicts here as JSON as well as logging them")
@click.option("--timeout", type=int, default=90, show_default=True,
              help="seconds before a trap probe is called wedged")
@click.option("--only", "only", multiple=True, type=click.Choice(sorted(TRAP_PROBES)),
              help="repeatable; re-probe just these traps (they are paid calls)")
def cmd_traps(json_out: Optional[Path], timeout: int, only: tuple[str, ...]) -> None:
    """Re-run the three recorded invocation traps and report whether each still bites."""
    rows = verify_traps(bench_cwd(), short_timeout=timeout, only=only)
    for row in rows:
        logger.info("%-58s still_bites=%s", row["trap"], row["still_bites"])
        logger.info("    %s", row["meaning"])
    if json_out:
        _write_json(json_out, rows)
        logger.info("trap verdicts written to %s", json_out)


@cli.command("run")
@click.option("--provider", "providers", multiple=True, type=click.Choice(sorted(PROVIDERS)),
              help="repeatable; default is every in-scope provider plus the claude baseline")
@click.option("--outcome", "outcomes", multiple=True, type=click.Choice(OUTCOME_KEYS),
              help="repeatable; default is all ten")
@click.option("--ledger", type=click.Path(path_type=Path), default=None,
              help=f"append-only JSONL ledger (default {LEDGER_REL})")
@click.option("--timeout", type=int, default=900, show_default=True,
              help="per-invocation seconds before the run is recorded as blocked")
def cmd_run(providers: tuple[str, ...], outcomes: tuple[str, ...],
            ledger: Optional[Path], timeout: int) -> None:
    """Run outcomes against providers and append the results to the ledger."""
    chosen_p = list(providers) or [*IN_SCOPE, "claude"]
    chosen_o = [o for o in OUTCOMES if not outcomes or o.key in outcomes]
    ledger_path = ledger or (REPO_ROOT / LEDGER_REL)
    cwd = bench_cwd()
    logger.info("neutral working directory: %s", cwd)
    rows = []
    for pkey in chosen_p:
        provider = PROVIDERS[pkey]
        for outcome in chosen_o:
            logger.info("run %s / %s", pkey, outcome.key)
            run = run_one(provider, outcome, cwd=cwd, timeout=timeout)
            row = record(run, outcome)
            rows.append(row)
            logger.info("  exit=%s wall=%ss model=%s pass=%s usd=%s",
                        row["exit_code"], row["wall_seconds"], row["served_model"],
                        row["predicate_pass"], row["usd"])
    append_ledger(rows, ledger_path)
    logger.info("appended %d row(s) to %s", len(rows), ledger_path)


@cli.command("report")
@click.option("--ledger", type=click.Path(path_type=Path), default=None)
def cmd_report(ledger: Optional[Path]) -> None:
    """Render the pass matrix and the money, flat, for a packet."""
    rows = read_ledger(ledger or (REPO_ROOT / LEDGER_REL))
    if not rows:
        logger.info("no rows")
        return
    by_provider: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_provider.setdefault(row["provider"], []).append(row)
    for pkey in sorted(by_provider):
        got = by_provider[pkey]
        passed = sum(1 for r in got if r.get("predicate_pass"))
        priced = [r["usd"] for r in got if r.get("usd") is not None]
        wall = sum(r.get("wall_seconds") or 0 for r in got)
        logger.info("%-9s %2d/%-2d pass  wall %7.1fs  usd %s  unit: %s",
                    pkey, passed, len(got), wall,
                    f"{sum(priced):.4f}" if priced else "UNPRICED",
                    got[0].get("metering_unit", ""))


if __name__ == "__main__":                                     # pragma: no cover
    cli()
