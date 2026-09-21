#!/usr/bin/env python
"""dispatch.py -- LAUNCH one lane, refuse a collision, and MONITOR its spend. It never ends a run.

THREE VERBS
  launch   contract -> run `doit moment:pre-launch` for the lane, and ONLY on a pass spawn the
           provider (`claude --bg` by default, `codex exec` when the contract's Dispatch block names
           it), then write a launch receipt and a job-to-lane record. A refusal spawns nothing and
           exits non-zero with the reason.
  govern   a MONITOR. Records the lane's spend against the cap FIELD, poll by poll. It never stops,
           pauses or kills a lane -- under any condition, including unreadable usage.
  plan     contract -> a JSON plan (argv, env delta, model/effort). Harness stage 11 runs it; it
           starts nothing.

WHY (wave 3, R-W3-2). Yesterday two agents entered one worktree because the launcher checked
nothing; every browser seat relearned the launch syntax because the launcher could not describe
itself; the one cap-aware launcher we built would have killed a lane mid-task; and every lane sat in
the operator's Agent View under one title, so he could not tell which was which. So: one command,
`--help` on it and on every verb, the occupancy check is the declared `pre-launch` moment (R-W3-1:
occupancy is caller-side), nothing here can end a task (N3), and every Claude launch carries
`-n <slug>` so the row is the lane's own name.

THE DISPATCH BLOCK IS READ, NEVER RUN. `parse_dispatch_block` takes the head program (claude|codex)
and the flags `-n`, `--worktree`, `--model`, `--effort`, `--permission-mode` from the contract's
`## Dispatch` fence; the argv is then BUILT here from those fields (`build_plan`). Anything else on
the line -- a pipe, a second command, an unknown flag -- is ignored, so the block is not an
arbitrary-execution surface (the fence `Assert-ClaudeCommand` existed to hold). A head other than
claude or codex is refused. The slug comes from the block (`--worktree`, `-n`; they must agree),
because a contract's file name need not carry it (`LANE-W3-B-launch-adapter.md` -> `lane-launch-adapter`).
Model and effort come from an explicit flag, the block, or the contract's `| Model | Mode | Effort |`
table -- never a default ([#717]); the block and the table disagreeing is a refusal.

THE CAP IS A RECORD (N3). `--token-cap` is optional. When given it is written into the launch
receipt; `govern` reads it back and records each poll's spend against it (`over_cap` in the row) and
exits `EXIT_OVER_CAP` after the fact. That exit code is a receipt for a check to surface, not a stop:
nothing in this module starts a process against a running lane. `claude agents --json` and `git`
are read-only control-plane calls.

MODEL REPORTED. Codex cannot attest which model served a turn: its `model_reported` is
`not attestable`. A Claude launch has served nothing yet, so its `model_reported` is `pending`; the
served model lands in `govern`'s spend rows and in `merge_receipt.py models`, from the transcript.

HONEST LIMITS
  * `launch` runs `doit moment:pre-launch` from the HUB root (dodo.py's own root) and spawns from the
    CALLER's cwd: a lane's worktree is created in the repo the operator stands in.
  * The second-launch refusal reads the launch receipt and the live job listing. A `claude --bg` job
    that has not been listed yet is not seen; the occupancy organ's session leg has the same window.
  * Codex `--worktree` is a managed worktree whose path this launcher does not choose: its receipt
    records `(codex-managed)`, and its job id is `codex-<pid>`.
  * `govern` is a POLL. A lane that finishes between two polls is recorded at its last reading.
"""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Mapping, Optional, Sequence

import click
import yaml

try:  # pragma: no cover -- exercised by whichever path the caller uses
    from scripts import lane_cost as lc
except ImportError:  # pragma: no cover
    import lane_cost as lc

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("dispatch")

HUB_ROOT = Path(__file__).resolve().parent.parent

EXIT_OVER_CAP = 3         # govern: spend passed the cap FIELD. Recorded; the lane was not touched.
EXIT_UNOBSERVED = 4       # govern: spend (or the lane's liveness) could not be read. Recorded.
EXIT_REFUSED = 5          # launch: refused, or the provider did not start. Nothing is running.
EXIT_NO_COMMIT = 6        # finished but committed nothing -- FAILED, not DONE
EXIT_UNWITNESSED = 7      # finished; whether it committed could not be established

NOT_ATTESTABLE = "not attestable"
MODEL_PENDING = "pending"

EFFORTS = {"l": "low", "low": "low", "m": "medium", "med": "medium", "medium": "medium",
           "h": "high", "high": "high", "x": "xhigh", "xhigh": "xhigh", "max": "max"}
SUBSTRATES = ("local", "codespace")
_ANTHROPIC_CREDS = ("ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN")
_SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
#: `claude --permission-mode` choices (claude 2.1.278 `--help`). A Dispatch block may pick one of these and nothing else.
PERMISSION_MODES = frozenset({"acceptEdits", "auto", "bypassPermissions", "manual", "dontAsk", "plan"})
_ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


class DispatchRefused(click.ClickException):
    """A launch this module will not perform. Carries the fix in its message."""


class LaunchRefused(DispatchRefused):
    """A launch that was refused at the door (or whose provider did not start): nothing is running."""
    exit_code = EXIT_REFUSED


class ListingUnreadable(RuntimeError):
    """`claude agents --json` could not be read. NOT evidence that a lane finished or is absent."""


# --- the cap: a field, never a stop -----------------------------------------------------------

def validate_cap(cap: int) -> int:
    if not isinstance(cap, int) or isinstance(cap, bool) or cap <= 0:
        raise DispatchRefused(f"token cap must be a positive integer, got {cap!r}")
    return cap


def capped_tokens(usage: "lc.TokenUsage", count_cache_reads: bool = False) -> int:
    used = usage.input_tokens + usage.output_tokens + usage.cache_write_tokens
    return used + (usage.cache_read_tokens if count_cache_reads else 0)


# --- providers: ported from Get-CloudModelProvider (values as recorded there, 2026-08-26) -----

@dataclass(frozen=True)
class Provider:
    head: str
    key: str = ""
    base_url: str = ""
    env: Mapping[str, str] = field(default_factory=dict)
    metering: str = "transcript"


PROVIDERS: dict[str, Provider] = {
    "anthropic": Provider("claude"),
    "deepseek": Provider("claude", "DEEPSEEK_API_KEY", "https://api.deepseek.com/anthropic", {
        "ANTHROPIC_MODEL": "deepseek-v4-pro", "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
        "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash", "CLAUDE_CODE_EFFORT_LEVEL": "max",
        "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "786432"}),
    "zai": Provider("claude", "ZAI_API_KEY", "https://api.z.ai/api/anthropic",
                    {"API_TIMEOUT_MS": "3000000"}),
    "moonshot": Provider("claude", "MOONSHOT_API_KEY", "https://api.moonshot.ai/anthropic", {
        "ANTHROPIC_MODEL": "kimi-k3[1m]", "ANTHROPIC_DEFAULT_OPUS_MODEL": "kimi-k3[1m]",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "kimi-k3[1m]",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "kimi-k3[1m]",
        "ANTHROPIC_DEFAULT_FABLE_MODEL": "kimi-k3[1m]",
        "CLAUDE_CODE_SUBAGENT_MODEL": "kimi-k3[1m]",
        "CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1048576"}),
    "codex": Provider("codex", metering="stream"),
}
_HEAD_PROVIDER = {"claude": "anthropic", "codex": "codex"}


def _provider(name: str) -> Provider:
    if name not in PROVIDERS:
        raise DispatchRefused(f"unknown provider {name!r}. Known: {', '.join(PROVIDERS)}")
    return PROVIDERS[name]


def read_secrets(path: Optional[Path]) -> dict[str, str]:
    """KEY=VALUE lines of the operator's key store; {} when absent. Values are never logged."""
    out: dict[str, str] = {}
    if path is None or not Path(path).is_file():
        return out
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        key, sep, value = line.strip().partition("=")
        if sep and key and not key.startswith("#"):
            out[key.strip()] = value.strip().strip("\"'")
    return out


def child_env(provider: str, parent: Mapping[str, str],
              secrets: Optional[Mapping[str, str]] = None) -> dict[str, str]:
    """The environment for the child. `parent` is copied, never mutated."""
    p = _provider(provider)
    env = dict(parent)
    if not p.base_url:
        return env
    token = env.get(p.key) or (secrets or {}).get(p.key)
    if not token:
        raise DispatchRefused(f"no {p.key} in the environment or the key store -- {provider} needs "
                              "it. Refusing rather than falling back: a fallback would answer from "
                              "a DIFFERENT model on a DIFFERENT bill.")
    # never send the operator's own key, or ANOTHER provider's key, to this third party
    for name in _ANTHROPIC_CREDS + tuple(q.key for q in PROVIDERS.values() if q.key and q is not p):
        env.pop(name, None)
    env["ANTHROPIC_BASE_URL"] = p.base_url
    env["ANTHROPIC_AUTH_TOKEN"] = token
    env.update(p.env)
    return env


# --- contract + branch guards: ported from Start-DispatchLane ---------------------------------

def windows_user_env(name: str) -> Optional[str]:
    """The USER-scope value of an environment variable (HKCU\\Environment), or None.

    The process copy goes stale: a session started before the value was set, or before the
    authority drive changed, carries the old one for its whole life. Get-DispatchPromptsDir reads
    the User scope first for that reason. None off Windows or when the value is absent."""
    if os.name != "nt":
        return None
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _kind = winreg.QueryValueEx(key, name)
    except (ImportError, OSError):
        return None
    return os.path.expandvars(str(value))


def prompts_dir(environ: Mapping[str, str] = os.environ, home: Optional[str] = None,
                root_exists: Callable[[str], bool] = os.path.exists,
                user_scope: Callable[[str], Optional[str]] = windows_user_env) -> Path:
    """Precedence, as Get-DispatchPromptsDir has it: the USER-scope value, then the process copy,
    then ~/Downloads. A whitespace-only value is unset."""
    raw = ((user_scope("CLAUDE_PROMPTS_DIR") or "").strip()
           or (environ.get("CLAUDE_PROMPTS_DIR") or "").strip())
    if raw:
        root = Path(raw).anchor
        if root and not root_exists(root):
            raise DispatchRefused(
                f"authority drive {root} absent -- CLAUDE_PROMPTS_DIR is {raw!r} but that root is "
                "not mounted. Mount it or clear the value; falling back would resolve against a "
                "stale directory without saying so.")
        return Path(raw)
    return Path(home or Path.home()) / "Downloads"


def resolve_contract(name: str, prompts_dir: Path) -> Path:
    given = Path(name)
    if given.is_file():
        return given.resolve()
    for candidate in (prompts_dir / name, prompts_dir / f"{name}.md"):
        if candidate.is_file():
            return candidate
    raise DispatchRefused(f"contract not found: {name!r}; looked in {prompts_dir}")


def branch_guard(slug: str, branch_exists: Callable[[str], bool]) -> Optional[str]:
    """A refusal string when `worktree-<slug>` already exists (a second dispatch would collide)."""
    if branch_exists(f"worktree-{slug}"):
        return f"SKIP -- branch 'worktree-{slug}' already exists; not dispatching a second lane."
    return None


def _git(*args: str) -> Optional["subprocess.CompletedProcess"]:
    """A bounded, UTF-8 git call in the CALLER's repo; None when it could not run at all."""
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=30)
    except (subprocess.TimeoutExpired, OSError):
        return None


def _git_branch_exists(branch: str) -> bool:
    done = _git("show-ref", "--verify", "--quiet", f"refs/heads/{branch}")
    return done is not None and done.returncode == 0


def commit_witness(slug: str) -> tuple[str, str]:
    """DONE MEANS A COMMIT: (`DONE`|`FAILED`|`UNWITNESSED`, reason) for lane `worktree-<slug>`.

    A lane that ran cleanly and committed nothing used to report DONE (PLAYBOOK Ch8 "DONE means a
    commit on origin"): a clean exit says the SESSION ended well, not that it did any work. The
    witness is the branch's own start point -- the oldest reflog entry, which is where the lane's
    worktree was cut -- against its tip, so it needs no baseline captured before launch.

    Three outcomes, not two. An ESTABLISHED absence (no branch, or a tip equal to its start) is
    FAILED; a question git could not answer is UNWITNESSED, because reporting a transient failure as
    "the lane did nothing" claims a failure nothing established."""
    ref = f"refs/heads/worktree-{slug}"
    tip = _git("rev-parse", "--verify", "--quiet", ref)
    if tip is None:
        return "UNWITNESSED", "git could not be run"
    if tip.returncode == 1:
        return "FAILED", f"no commit: branch worktree-{slug} does not exist"
    if tip.returncode != 0:
        return "UNWITNESSED", f"git could not read {ref}: {tip.stderr.strip()[:120]}"
    log = _git("reflog", "show", "--format=%H", ref)
    starts = log.stdout.split() if log is not None and log.returncode == 0 else []
    if not starts:
        return "UNWITNESSED", f"{ref} has no reflog to take its start point from"
    counted = _git("rev-list", "--count", f"{starts[-1]}..{tip.stdout.strip()}")
    if counted is None or counted.returncode != 0 or not counted.stdout.strip().isdigit():
        return "UNWITNESSED", "git could not count the branch's commits"
    n = int(counted.stdout.strip())
    if n == 0:
        return "FAILED", f"no commit on worktree-{slug} since its worktree was cut"
    return "DONE", f"{n} commit(s) on worktree-{slug}"


# --- the contract's own model and effort ([#717]: never a default) --------------------------------

_TABLE_HEAD = re.compile(r"^\|\s*Model\s*\|\s*Mode\s*\|\s*Effort\s*\|\s*$", re.IGNORECASE)
_MODEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._\[\]-]*$")


def parse_contract_model_effort(text: str) -> tuple[str, str]:
    """`(model, effort)` from the contract's `| Model | Mode | Effort |` table.

    A contract with no parseable table, an empty model, or an effort outside the enum is REFUSED --
    the alternative is a default, and a default silently re-decides the most expensive constant on
    the line."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not _TABLE_HEAD.match(line.strip()):
            continue
        rows = [ln.strip() for ln in lines[i + 1:i + 4] if ln.strip().startswith("|")]
        values = [r for r in rows if not set(r) <= set("|-: ")]
        cells = [c.strip().strip("`") for c in values[0].strip("|").split("|")] if values else []
        if len(cells) != 3:
            break
        model, _mode, effort = cells
        if not _MODEL.match(model):
            raise DispatchRefused(f"the contract's Model cell is {model!r} -- not a model name. "
                                  "Refusing rather than defaulting to one.")
        if EFFORTS.get(effort.lower()) is None:
            raise DispatchRefused(f"the contract's Effort cell is {effort!r}. Valid: low, medium, "
                                  "high, xhigh, max. Refusing rather than defaulting.")
        return model, effort.lower()
    raise DispatchRefused("no parseable `| Model | Mode | Effort |` table in the contract, and no "
                          "--model/--effort given. Refusing rather than defaulting to a model "
                          "([#717]).")


def slug_from_contract(path: Path) -> str:
    """`LANE-<slug>.md` -> `<slug>`; '' when the file name does not carry one."""
    found = re.match(r"^LANE-(.+)\.md$", Path(path).name, re.IGNORECASE)
    return found.group(1) if found else ""


# --- the Dispatch block: read for its fields, never executed --------------------------------------

@dataclass(frozen=True)
class DispatchLine:
    """The fields of a contract's `## Dispatch` line. '' means the line did not carry it."""
    head: str
    name: str = ""
    worktree: str = ""
    model: str = ""
    effort: str = ""
    permission_mode: str = ""


_VALUE_FLAGS = {"-n": "name", "--name": "name", "-m": "model", "--model": "model",
                "--effort": "effort", "--permission-mode": "permission_mode"}
_WORKTREE_FLAGS = ("-w", "--worktree")   # the value is optional: `--worktree "prompt"` names none


def _tokens(line: str) -> list[tuple[str, bool]]:
    """`(text, was_quoted)` pairs: whitespace-split, double quotes group. NOT a shell lexer -- a
    Windows path's backslashes must survive, and nothing here is ever expanded or run."""
    out: list[tuple[str, bool]] = []
    for found in re.finditer(r'"([^"]*)"|(\S+)', line):
        quoted = found.group(1) is not None
        out.append((found.group(1) if quoted else found.group(2), quoted))
    return out


def _dispatch_lines(text: str) -> list[str]:
    """The non-blank lines of the fenced block under the `## Dispatch` heading."""
    found = re.search(r"^##\s+Dispatch\b[^\n]*\n(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    if not found:
        return []
    fence = re.search(r"^```[^\n]*\n(.*?)^```", found.group(1), re.M | re.S)
    return [ln.strip() for ln in fence.group(1).splitlines() if ln.strip()] if fence else []


def parse_dispatch_block(text: str) -> Optional[DispatchLine]:
    """The first line of the contract's Dispatch fence as a `DispatchLine`, or None when there is no
    block. A head other than `claude` or `codex` is REFUSED. Only the known flags are read."""
    lines = _dispatch_lines(text)
    if not lines:
        return None
    tokens = _tokens(lines[0])
    head = Path(tokens[0][0]).stem.lower() if tokens else ""
    if head not in _HEAD_PROVIDER:
        raise DispatchRefused(f"the Dispatch block starts with {tokens[0][0] if tokens else ''!r}; "
                              "only `claude` and `codex` are launched. Refusing.")
    got: dict[str, str] = {}
    i = 1
    while i < len(tokens):
        word, quoted = tokens[i]
        if not quoted and word in _VALUE_FLAGS and i + 1 < len(tokens):
            got[_VALUE_FLAGS[word]] = tokens[i + 1][0]
            i += 1
        elif not quoted and word in _WORKTREE_FLAGS:
            if i + 1 < len(tokens) and not tokens[i + 1][1] and not tokens[i + 1][0].startswith("-"):
                got["worktree"] = tokens[i + 1][0]
                i += 1
        i += 1
    _validate_line(got)
    return DispatchLine(head=head, **got)


def _validate_line(got: Mapping[str, str]) -> None:
    """A value the parser took after a flag must be a value, not another flag or a free string:
    `--permission-mode --dangerously-skip-permissions` must not become argv."""
    for key, value in got.items():
        if value.startswith("-"):
            raise DispatchRefused(f"the Dispatch block's {key.replace('_', '-')} value is {value!r}, which "
                                  "looks like a flag, not a value. Refusing.")
    if "model" in got and not _MODEL.match(got["model"]):
        raise DispatchRefused(f"the Dispatch block's model {got['model']!r} is not a model name. Refusing.")
    if "effort" in got and EFFORTS.get(got["effort"].lower()) is None:
        raise DispatchRefused(f"the Dispatch block's effort {got['effort']!r} is not one of low, medium, "
                              "high, xhigh, max. Refusing.")
    if "permission_mode" in got and got["permission_mode"] not in PERMISSION_MODES:
        raise DispatchRefused(f"the Dispatch block's permission mode {got['permission_mode']!r} is not one "
                              f"of {', '.join(sorted(PERMISSION_MODES))}. Refusing.")


def _same_effort(a: str, b: str) -> bool:
    return EFFORTS.get(a.lower(), a.lower()) == EFFORTS.get(b.lower(), b.lower())


# --- the request and the plan ----------------------------------------------------------------------

@dataclass(frozen=True)
class Plan:
    argv: list[str]
    metering: str


def build_plan(provider: str, model: str, slug: str, effort: str, prompt: str,
               permission_mode: str = "bypassPermissions", streamed: bool = False) -> Plan:
    p = _provider(provider)
    eff = EFFORTS.get(effort.lower())
    if eff is None:
        raise DispatchRefused(f"unknown effort {effort!r}. Valid: low, medium, high, xhigh, max "
                              "(or l/m/h/x)")
    if p.head == "codex":
        argv = ["codex", "exec", "--json", "--skip-git-repo-check", "--worktree", "-m", model,
                "-c", f"model_reasoning_effort={eff}", "-s", "workspace-write", prompt]
        return Plan(argv, "stream")
    if streamed:  # a headless claude, for a substrate that cannot hand over a transcript
        argv = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", model,
                "--effort", eff, "--permission-mode", permission_mode, prompt]
        return Plan(argv, "stream")
    # `-n <slug>` names the session, so the Agent View row is the lane's own name and not the
    # contract prompt's first words. --permission-mode is not optional: nobody is at a --bg lane's
    # keyboard, so a prompt is a silent stall that looks exactly like a slow lane.
    argv = ["claude", "--bg", "-n", slug, "--model", model, "--effort", eff, "--permission-mode",
            permission_mode, "--worktree", slug, prompt]
    return Plan(argv, "transcript")


@dataclass(frozen=True)
class LaunchRequest:
    """Everything a launch needs, resolved: what to run, for which lane, from which contract."""
    slug: str
    provider: str
    model: str
    effort: str
    permission_mode: str
    contract: Path
    batch: str = ""
    token_cap: Optional[int] = None

    @property
    def session_name(self) -> str:
        return self.slug

    @property
    def prompt(self) -> str:
        return f"Read and execute the frozen contract at {self.contract}"

    @property
    def argv(self) -> list[str]:
        return build_plan(self.provider, self.model, self.slug, self.effort, self.prompt,
                          self.permission_mode).argv


@dataclass(frozen=True)
class LaunchResult:
    """What a launch produced. `model_reported` is `not attestable` for Codex and `pending` for a
    Claude lane that has served nothing yet; `session_name_reported` is what the job record says."""
    slug: str
    provider: str
    model_requested: str
    model_reported: str
    job_id: str
    worktree: str
    session_name: str
    session_name_reported: str = ""
    session_id: str = ""
    pid: Optional[int] = None
    log_path: str = ""
    argv: list = field(default_factory=list)


@dataclass(frozen=True)
class PreLaunch:
    passed: bool
    reason: str = ""


@dataclass(frozen=True)
class Spawned:
    returncode: int
    stdout: str = ""
    pid: Optional[int] = None


def request_from_contract(contract: Path, *, slug: str = "", provider: str = "", model: str = "",
                          effort: str = "", permission_mode: str = "", batch: str = "",
                          token_cap: Optional[int] = None) -> LaunchRequest:
    """Resolve a contract into a `LaunchRequest`. Explicit arguments beat the Dispatch block, which
    beats the file name (slug) and the `| Model | Mode | Effort |` table (model, effort). Two
    sources that disagree are a refusal, never a quiet pick."""
    path = Path(contract)
    text = path.read_text(encoding="utf-8", errors="replace")
    line = parse_dispatch_block(text)
    if line is not None and line.name and line.worktree and line.name != line.worktree:
        raise DispatchRefused(f"the Dispatch block names the session {line.name!r} but the worktree "
                              f"{line.worktree!r}; a lane has one slug. Fix the contract.")
    slug = slug or (line.name or line.worktree if line else "") or slug_from_contract(path)
    if not slug:
        raise DispatchRefused(f"no lane slug: {path.name!r} is not LANE-<slug>.md, the Dispatch block "
                              "names none, and --slug was not given")
    if not _SLUG.match(slug):
        raise DispatchRefused(f"{slug!r} is not a usable lane slug (letters, digits, '.', '_', '-')")
    provider = provider or (_HEAD_PROVIDER[line.head] if line else "anthropic")
    table: Optional[tuple[str, str]] = None
    if not (model and effort) and not (line and line.model and line.effort):
        table = parse_contract_model_effort(text)     # nothing else names them: it must parse
    else:
        try:
            table = parse_contract_model_effort(text)
        except DispatchRefused:
            table = None                              # the block names both; a table is optional
    for label, from_block, from_table, same in (
            ("model", line.model if line else "", table[0] if table else "",
             lambda a, b: a.lower() == b.lower()),
            ("effort", line.effort if line else "", table[1] if table else "", _same_effort)):
        if from_block and from_table and not same(from_block, from_table):
            raise DispatchRefused(
                f"the Dispatch block's {label} is {from_block!r} but the contract's table says "
                f"{from_table!r}. Refusing rather than picking one: pass --{label} to say which.")
    model = model or (line.model if line else "") or (table[0] if table else "")
    effort = effort or (line.effort if line else "") or (table[1] if table else "")
    if EFFORTS.get(effort.lower()) is None:
        raise DispatchRefused(f"unknown effort {effort!r}. Valid: low, medium, high, xhigh, max")
    if permission_mode and permission_mode not in PERMISSION_MODES:
        raise DispatchRefused(f"unknown permission mode {permission_mode!r}. Valid: "
                              f"{', '.join(sorted(PERMISSION_MODES))}")
    if token_cap is not None:
        validate_cap(token_cap)
    return LaunchRequest(
        slug=slug, provider=provider, model=model, effort=EFFORTS[effort.lower()],
        permission_mode=permission_mode or (line.permission_mode if line else "") or "bypassPermissions",
        contract=path.resolve(), batch=batch or os.environ.get("HARNESS_BATCH", ""),
        token_cap=token_cap)


# --- receipts: the launch receipt, the job-to-lane record, the spend rows -------------------------

def receipts_dir() -> Path:
    """`HARNESS_RECEIPTS_DIR`, else the hub's `logs/receipts/` (gitignored, per checkout) -- where
    the moments' own receipts go (DECLARE-NIGHT N2)."""
    return Path(os.environ.get("HARNESS_RECEIPTS_DIR") or HUB_ROOT / "logs" / "receipts")


def _stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _receipt_path(slug: str) -> Path:
    return receipts_dir() / f"LAUNCH-{slug.upper()}.json"


def _job_path(job_id: str) -> Path:
    return receipts_dir() / f"LAUNCH-JOB-{re.sub(r'[^A-Za-z0-9._-]', '_', job_id)}.json"


def _spend_path(slug: str) -> Path:
    return receipts_dir() / f"LAUNCH-SPEND-{slug.upper()}.jsonl"


def _write_json(path: Path, body: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")


def read_launch_receipt(slug: str) -> Optional[dict]:
    try:
        body = json.loads(_receipt_path(slug).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return body if isinstance(body, dict) else None


# --- the job listing and process liveness (read-only) ---------------------------------------------

_ENDED = frozenset({"done", "stopped", "failed", "error", "exited", "cancelled", "canceled"})


def _control(argv: list[str]) -> Optional["subprocess.CompletedProcess"]:
    """A bounded, read-only control-plane call; None when it hung or could not run."""
    try:
        return subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=30)
    except (subprocess.TimeoutExpired, OSError):
        return None


def list_agents() -> list[dict]:
    """`claude agents --json` as a list of records; ListingUnreadable when it cannot be read."""
    listing = _control(["claude", "agents", "--json"])
    if listing is None or listing.returncode != 0 or not listing.stdout.strip():
        raise ListingUnreadable("`claude agents --json` failed, hung or was empty")
    try:
        data = json.loads(listing.stdout)
    except ValueError as exc:
        raise ListingUnreadable(f"`claude agents --json` was not JSON ({exc})") from exc
    if not isinstance(data, list):
        raise ListingUnreadable("`claude agents --json` was not a list")
    return [entry for entry in data if isinstance(entry, dict)]


def _find_agent(agents: Sequence[dict], lane_id: str) -> Optional[dict]:
    """The record for `lane_id` -- its short id, or a prefix of its session id."""
    for entry in agents:
        if str(entry.get("id") or "") == lane_id or (
                lane_id and str(entry.get("sessionId") or "").startswith(lane_id)):
            return entry
    return None


def _is_live(entry: Mapping) -> bool:
    return str(entry.get("state") or "").lower() not in _ENDED


def process_alive(pid: int) -> bool:
    """Is process `pid` running? Read-only (`tasklist` / `ps`); never a signal, so it cannot end it."""
    if os.name == "nt":
        done = _control(["tasklist", "/FI", f"PID eq {pid}", "/NH", "/FO", "CSV"])
        return done is not None and f'"{pid}"' in done.stdout
    done = _control(["ps", "-p", str(pid)])
    return done is not None and done.returncode == 0


@dataclass(frozen=True)
class LaneBinding:
    """A `--bg` lane's own identity: the session id its transcript is filed under ('' when the
    listing carries none), and its cwd."""
    session_id: str
    cwd: str
    live: bool = True   # False for an ENDED record (state done/stopped/...)


def bind_lane(lane_id: str) -> Optional[LaneBinding]:
    """Bind a launched lane to ITS OWN session id, from the listing -- no `--slug-dir`, no slug.
    None when the lane is not listed (or the listing cannot be read)."""
    try:
        entry = _find_agent(list_agents(), lane_id)
    except ListingUnreadable:
        return None
    if entry is None:
        return None
    return LaneBinding(str(entry.get("sessionId") or ""), str(entry.get("cwd") or ""),
                       live=_is_live(entry))


def find_lane_by_slug_in(agents: Sequence[dict], slug: str) -> Optional[str]:
    """The id of the ONE live lane in an already-read listing whose cwd is `.../worktrees/<slug>`,
    else None. Ambiguity (two live lanes for one slug) is None, never a guess."""
    suffix = f"/worktrees/{slug}".lower()
    live = [e for e in agents
            if str(e.get("cwd") or "").replace("\\", "/").rstrip("/").lower().endswith(suffix)
            and _is_live(e) and e.get("id")]
    return str(live[0]["id"]) if len(live) == 1 else None


def find_launched_lane_in(agents: Sequence[dict], slug: str, since: float) -> Optional[str]:
    """The id of the ONE record in `.../worktrees/<slug>` that STARTED at or after `since` (epoch
    seconds), whatever its state: a one-line lane can be `done` before the listing is first read. An
    older record for the same worktree is an earlier launch, never this one."""
    suffix = f"/worktrees/{slug}".lower()
    found = [e for e in agents
             if str(e.get("cwd") or "").replace("\\", "/").rstrip("/").lower().endswith(suffix)
             and e.get("id") and isinstance(e.get("startedAt"), (int, float))
             and e["startedAt"] / 1000.0 >= since - 5]
    return str(found[0]["id"]) if len(found) == 1 else None


def find_lane_by_slug(slug: str) -> Optional[str]:
    """`find_lane_by_slug_in` over the live listing; None when it cannot be read."""
    try:
        return find_lane_by_slug_in(list_agents(), slug)
    except ListingUnreadable:
        return None


def lane_alive(lane_id: str) -> bool:
    """False once the lane has ENDED. A finished `--bg` lane stays LISTED with state `done`, so
    "is it in the listing" is not liveness. Absent from the listing is ended too. Raises
    ListingUnreadable when the listing cannot be read: that is not "ended"."""
    entry = _find_agent(list_agents(), lane_id)
    return entry is not None and _is_live(entry)


# --- launch ----------------------------------------------------------------------------------------

def _tail(text: str, limit: int = 600) -> str:
    text = " | ".join(part.strip() for part in text.splitlines() if part.strip())
    return text if len(text) <= limit else text[:limit] + " ..."


_DOIT_CHATTER = re.compile(r"^(\.\s+organ:|TaskFailed|Python Task failed|warning:|\s*$)")


def run_prelaunch(request: LaunchRequest, hub: Path = HUB_ROOT) -> PreLaunch:
    """Run the DECLARED `pre-launch` moment (ecosystem/harness.yaml) for this lane, from the hub.

    The organs are whatever the file declares -- occupancy, a live integrator, routing agreement --
    and this function names none of them: a non-zero exit is a refusal whose reason is the organs'
    own output. Raises OSError when `uv` cannot run; the caller treats that as a refusal too."""
    env = dict(os.environ)
    env["HARNESS_LANE"] = request.slug
    env["HARNESS_CONTRACT"] = str(request.contract)
    if request.batch:
        env["HARNESS_BATCH"] = request.batch
    argv = ["uv", "run", "--locked", "doit", "-f", "scripts/dodo.py", "moment:pre-launch"]
    done = subprocess.run(argv, cwd=str(hub), env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    if done.returncode == 0:
        gaps = _pre_launch_gaps(hub)
        return PreLaunch(False, "an organ of the declared pre-launch moment did not clear it: " + "; ".join(gaps)
                         ) if gaps else PreLaunch(True)
    said = [ln for ln in (done.stdout + "\n" + done.stderr).splitlines() if not _DOIT_CHATTER.match(ln)]
    return PreLaunch(False, _tail("\n".join(said)) or f"pre-launch exited {done.returncode}")


def _pre_launch_gaps(hub: Path) -> list[str]:
    """Organs of the DECLARED `pre-launch` moment whose receipt is missing, SKIPPED or non-zero.

    The moment exits 0 when an `optional` organ is not built (`SKIPPED-NOT-BUILT`), which is right for
    a spine and wrong for a launch: a launch is not cleared by a check that did not run."""
    path = Path(os.environ.get("HARNESS_YAML") or hub / "ecosystem" / "harness.yaml")
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return [f"{path} could not be read ({type(exc).__name__})"]
    moment = next((m for m in doc.get("moments") or [] if m.get("name") == "pre-launch"), None)
    if moment is None:
        return ["harness.yaml declares no `pre-launch` moment"]
    gaps = []
    for organ in moment.get("organs") or []:
        try:
            body = json.loads((receipts_dir() / organ["receipt"]).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            gaps.append(f"{organ['id']} left no receipt ({organ['receipt']})")
            continue
        status = str(body.get("status") or "")
        if status.upper().startswith("SKIPPED"):
            gaps.append(f"{organ['id']} was {status}")
        elif body.get("exit_code") != 0:
            gaps.append(f"{organ['id']} exited {body.get('exit_code')}")
    return gaps


def spawn_process(argv: Sequence[str], env: Mapping[str, str], cwd: Path,
                  log_path: Optional[Path] = None) -> Spawned:
    """THE process boundary -- the one place a provider is started, and the one thing tests replace.

    Without `log_path` the command is run to completion and its output returned (`claude --bg`
    prints its job id and exits). With one, the child is DETACHED with its stdout in that file and
    this returns at once with its pid (`codex exec` runs for the length of the lane). Nothing here
    keeps a handle that could later end the child."""
    if log_path is None:
        done = subprocess.run(list(argv), env=dict(env), cwd=str(cwd), capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
        return Spawned(done.returncode, done.stdout + done.stderr, None)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    flags = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP) if os.name == "nt" else 0
    with open(log_path, "ab") as sink:
        child = subprocess.Popen(list(argv), env=dict(env), cwd=str(cwd), stdin=subprocess.DEVNULL,
                                 stdout=sink, stderr=subprocess.STDOUT, creationflags=flags,
                                 start_new_session=(os.name != "nt"))
    return Spawned(0, "", child.pid)


_JOB_ID = re.compile(r"(?im)^\s*backgrounded\b[^0-9a-f\r\n]*([0-9a-f]{8})\b")   # after `_ANSI` is stripped


#: How long a launch whose job the listing has not shown yet still holds its slug: `claude --bg` can
#: return before `claude agents --json` lists the job, and that window is where a second launch gets in.
LISTING_LAG_SECONDS = 180


class LaunchIncomplete(DispatchRefused):
    """The lane WAS started but a record of it could not be written. Not a refusal: it is running."""
    exit_code = 8


def _age_seconds(stamp: object) -> Optional[float]:
    try:
        then = datetime.fromisoformat(str(stamp))
    except ValueError:
        return None
    return (datetime.now(timezone.utc) - then.astimezone(timezone.utc)).total_seconds()


def _held_by(slug: str, receipt: Optional[dict], agents: Callable[[], list[dict]]) -> str:
    """'' when nothing holds the slug; else what does. ListingUnreadable when a Claude lane's state
    cannot be read -- the caller refuses, it never assumes free.

    Three ways a slug is held: its earlier launch's job is LIVE; a live lane sits in
    `.../worktrees/<slug>` whatever its id (a receipt that says `unresolved`, or no receipt); or the
    earlier launch is younger than `LISTING_LAG_SECONDS` and the listing has not shown its job yet."""
    receipt = receipt or {}
    job = str(receipt.get("job_id") or "")
    if receipt.get("provider") == "codex":
        pid = receipt.get("pid")
        if isinstance(pid, int):
            return f"codex job {job} (pid {pid}) is still running" if process_alive(pid) else ""
        age = _age_seconds(receipt.get("launched_at"))   # an INTENT receipt: Popen may already have run
        if job and age is not None and age < LISTING_LAG_SECONDS:
            return f"a codex launch ({job}) began {int(age)}s ago and has not recorded its process yet"
        return ""
    listing = agents()
    entry = _find_agent(listing, job) if job and job not in ("unresolved", "pending") else None
    if entry is not None and _is_live(entry):
        return f"job {job} is {entry.get('state') or 'listed'}"
    by_worktree = find_lane_by_slug_in(listing, slug)
    if by_worktree:
        return f"job {by_worktree} is live in .claude/worktrees/{slug}"
    age = _age_seconds(receipt.get("launched_at"))
    if job and entry is None and age is not None and age < LISTING_LAG_SECONDS:
        return f"job {job} was launched {int(age)}s ago and is not in the listing yet"
    return ""


class _SlugLock:
    """One launch of a slug at a time: an exclusive-create lock file beside the receipts.

    A launch that finds it refuses (`in progress`); it is removed when the launch ends, refused or
    not. It is never stolen: a launch killed outright leaves it, and the refusal names the file --
    removing it is the operator's call, like any other husk."""

    def __init__(self, slug: str):
        self.path = receipts_dir() / f"LAUNCH-LOCK-{slug.upper()}"
        self.slug = slug

    def __enter__(self) -> "_SlugLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise LaunchRefused(f"a launch of {self.slug} is in progress (lock {self.path}); if that launch "
                                "died, remove the lock file by hand") from exc
        with os.fdopen(fd, "w", encoding="utf-8") as sink:
            sink.write(f"pid {os.getpid()} at {_stamp()}\n")
        return self

    def __exit__(self, *exc: object) -> None:
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def launch_lane(request: LaunchRequest, *,
                prelaunch: Callable[[LaunchRequest], PreLaunch] = None,
                spawn: Callable[..., Spawned] = None,
                agents: Callable[[], list[dict]] = None,
                cwd: Optional[Path] = None, environ: Optional[Mapping[str, str]] = None,
                secrets_file: Optional[Path] = None, sleep: Callable[[float], None] = time.sleep,
                ) -> LaunchResult:
    """Refuse a collision, run `pre-launch`, and only then spawn -- exactly once.

    Raises `LaunchRefused` (exit 5) BEFORE anything is spawned when another launch of the slug is in
    progress, when the slug's earlier launch (or any lane in its worktree) is still running or its
    state cannot be read, when `pre-launch` refuses or cannot run, or when the provider needs a key
    it lacks; and after a spawn that did not start (nothing is running). `LaunchIncomplete` (exit 8)
    when the lane started but its receipt could not be written."""
    prelaunch = prelaunch or run_prelaunch
    spawn = spawn or spawn_process
    agents = agents or list_agents
    cwd = Path(cwd or Path.cwd())
    provider = _provider(request.provider)
    with _SlugLock(request.slug):
        try:
            holder = _held_by(request.slug, read_launch_receipt(request.slug), agents)
        except ListingUnreadable as exc:
            raise LaunchRefused(f"cannot tell whether {request.slug} is already launched ({exc}); "
                                "refusing rather than assuming it is free") from exc
        if holder:
            raise LaunchRefused(f"{request.slug} is already launched: {holder}. Not launching a second lane.")
        env = child_env(request.provider, environ if environ is not None else os.environ,
                        read_secrets(secrets_file) if provider.key else None)
        try:
            outcome = prelaunch(request)
        except Exception as exc:  # noqa: BLE001 -- a pre-launch that could not run is a REFUSAL, never a pass
            raise LaunchRefused(f"pre-launch could not run for {request.slug}: {type(exc).__name__}: {exc}") from exc
        if not outcome.passed:
            raise LaunchRefused(f"pre-launch refused {request.slug}: {outcome.reason}")

        codex = provider.head == "codex"
        log_path = receipts_dir() / f"LAUNCH-LOG-{request.slug.upper()}.jsonl" if codex else None
        # The INTENT receipt goes down before the spawn: a launch interrupted after the provider
        # started still leaves a fresh receipt, which holds the slug while the listing catches up.
        try:
            _write_json(_receipt_path(request.slug), {
                "schema": 1, "organ": "launch", "launched_at": _stamp(), "exit_code": None,
                "job_id": "pending", "slug": request.slug, "provider": request.provider,
                "batch": request.batch, "contract": str(request.contract)})
        except OSError as exc:
            raise LaunchRefused(f"cannot write the launch receipt for {request.slug} ({exc}); refusing "
                                "to start a lane nothing can record") from exc
        began = time.time()
        try:
            started = spawn(request.argv, env, cwd, log_path) if codex else spawn(request.argv, env, cwd)
        except OSError as exc:
            _receipt_path(request.slug).unlink(missing_ok=True)
            raise LaunchRefused(f"{request.argv[0]} could not be started ({type(exc).__name__}: {exc}) -- "
                                "no lane was started") from exc
        if started.returncode != 0:
            _receipt_path(request.slug).unlink(missing_ok=True)
            raise LaunchRefused(f"{request.argv[0]} exited {started.returncode} -- no lane was started: "
                                f"{_tail(started.stdout, 300)}")
        # From here a lane IS running: whatever fails below, the receipt is still written.
        job_id, session_id, reported_name = _identify(request, started, codex, agents, sleep, began)
        result = LaunchResult(
            slug=request.slug, provider=request.provider, model_requested=request.model,
            model_reported=NOT_ATTESTABLE if codex else MODEL_PENDING,
            job_id=job_id or "unresolved",
            worktree="(codex-managed)" if codex else str(cwd / ".claude" / "worktrees" / request.slug),
            session_name=request.session_name, session_name_reported=reported_name,
            session_id=session_id, pid=started.pid, log_path=str(log_path or ""), argv=list(request.argv))
        try:
            _write_launch_records(request, result)
        except OSError as exc:
            raise LaunchIncomplete(f"{request.slug} WAS started (job {result.job_id}) but its launch receipt "
                                   f"could not be written ({exc}). It is running; nothing was stopped.") from exc
        if result.job_id == "unresolved":
            raise LaunchIncomplete(
                f"{request.slug} was started ({request.argv[0]} exited 0) but no job could be identified: its "
                "output carried no id and no record in .claude/worktrees/"
                f"{request.slug} appeared. Run `claude agents` to find it. The launch receipt says "
                f"`unresolved` and holds the slug for {LISTING_LAG_SECONDS}s; nothing was stopped.")
        return result


def _identify(request: LaunchRequest, started: Spawned, codex: bool, agents: Callable[[], list[dict]],
              sleep: Callable[[float], None], since: float) -> tuple[str, str, str]:
    """`(job id, session id, the name the job record reports)` for a lane that has just started.
    Blank parts are unknown, never guessed: the id comes from the provider's own output, else the one
    live lane in the slug's worktree."""
    if codex:
        return f"codex-{started.pid}", "", ""
    found = _JOB_ID.search(_ANSI.sub("", started.stdout or ""))
    job_id = found.group(1) if found else ""
    for attempt in range(4):        # the listing can lag the start by a moment
        try:
            jobs = agents()
        except Exception:  # noqa: BLE001 -- an unreadable listing leaves the fields blank; the lane is running
            jobs = []
        entry = _find_agent(jobs, job_id) if job_id else None
        if entry is None and not job_id:
            recovered = find_launched_lane_in(jobs, request.slug, since)
            entry = _find_agent(jobs, recovered) if recovered else None
            job_id = str(entry.get("id")) if entry else ""
        if entry is not None:
            return job_id, str(entry.get("sessionId") or ""), str(entry.get("name") or "")
        if attempt < 3:
            sleep(1.0)
    return job_id, "", ""


def _write_launch_records(request: LaunchRequest, result: LaunchResult) -> None:
    """The launch receipt (one per slug) and the job-to-lane record (one per job)."""
    when = _stamp()
    _write_json(_receipt_path(request.slug), {
        "schema": 1, "organ": "launch", "launched_at": when, "exit_code": 0, "batch": request.batch,
        "contract": str(request.contract), "effort": request.effort, "token_cap": request.token_cap,
        **{k: v for k, v in asdict(result).items()}})
    if result.job_id == "unresolved":
        return          # one file per job id, and there is none to name
    _write_json(_job_path(result.job_id), {
        "schema": 1, "job_id": result.job_id, "session_id": result.session_id, "slug": request.slug,
        "batch": request.batch, "provider": request.provider, "worktree": result.worktree,
        "contract": str(request.contract), "launched_at": when})


# --- govern: a MONITOR ------------------------------------------------------------------------------

@dataclass(frozen=True)
class MonitorVerdict:
    polls: int
    used: Optional[int]
    cap: Optional[int]
    over_cap: bool = False
    unobserved: str = ""     # why spend or liveness could not be read at some poll; "" when it always could
    ended: bool = False      # the lane was seen to end (nothing else about it is claimed)

    @property
    def exit_code(self) -> int:
        if self.over_cap:
            return EXIT_OVER_CAP
        return EXIT_UNOBSERVED if self.unobserved else 0


def monitor(*, cap: Optional[int], read_usage: Callable[[], Optional["lc.TokenUsage"]],
            alive: Callable[[], bool], record: Callable[[dict], None],
            sleep: Callable[[float], None] = time.sleep, interval: float = 15.0,
            max_polls: Optional[int] = None, blind_polls: int = 8, count_cache_reads: bool = False,
            models: Optional[list] = None) -> MonitorVerdict:
    """Poll a running lane and RECORD each reading; touch nothing.

    One row per poll goes to `record`: `used`, `cap`, `over_cap`, `readable`. An unreadable usage is
    a row with `readable: false` -- not zero, and not a reason to do anything to the lane. When the
    lane's liveness cannot be read `blind_polls` times running, THIS MONITOR ends (the verdict says
    why); the lane is not consulted, stopped or disturbed. `max_polls` bounds the monitor, not the
    lane."""
    polls, used, over, why, blind = 0, None, False, "", 0
    while True:
        usage = read_usage()
        polls += 1
        readable = usage is not None
        if readable:
            used = capped_tokens(usage, count_cache_reads)
        else:
            why = why or "spend was unreadable at one or more polls"
        over = over or (readable and cap is not None and used > cap)
        record({"ts": _stamp(), "poll": polls, "used": used if readable else None, "cap": cap,
                "over_cap": bool(readable and cap is not None and used > cap), "readable": readable,
                "models": list(models or [])})
        try:
            done = not alive()
            blind = 0
        except ListingUnreadable as exc:
            blind += 1
            why = why or f"the lane's liveness could not be read ({exc})"
            done = False
            if blind >= blind_polls:
                return MonitorVerdict(polls, used, cap, over, why, ended=False)
        if done:
            return MonitorVerdict(polls, used, cap, over, why, ended=True)
        if max_polls is not None and polls >= max_polls:
            return MonitorVerdict(polls, used, cap, over, why, ended=False)
        sleep(interval)


# --- stream metering (codex): read the log a detached lane writes ------------------------------------

def usage_from_stream_line(line: str, seen: set[str]) -> Optional["lc.TokenUsage"]:
    """One event's usage, or None. Anthropic `assistant` events repeat per message id; codex
    reports `turn.completed`."""
    try:
        ev = json.loads(line)
    except ValueError:
        return None
    if not isinstance(ev, dict):
        return None
    if ev.get("type") == "turn.completed" and isinstance(ev.get("usage"), dict):
        u = ev["usage"]
        cached = int(u.get("cached_input_tokens") or 0)
        return lc.TokenUsage(input_tokens=max(int(u.get("input_tokens") or 0) - cached, 0),
                             output_tokens=int(u.get("output_tokens") or 0),
                             cache_write_tokens=int(u.get("cache_write_input_tokens") or 0),
                             cache_read_tokens=cached, calls=1)
    if ev.get("type") == "assistant":
        msg = ev.get("message") or {}
        mid = msg.get("id")
        if mid in seen or not isinstance(msg.get("usage"), dict):
            return None
        seen.add(mid)
        return lc._usage_from_turn(msg["usage"])
    return None


def _log_reader(log_path: Path) -> Callable[[], Optional["lc.TokenUsage"]]:
    """Usage summed from a detached lane's stdout log; None when it is absent or carries none."""
    def read() -> Optional["lc.TokenUsage"]:
        try:
            lines = Path(log_path).read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return None
        total, seen, observed = lc.TokenUsage(), set(), False
        for line in lines:
            try:
                usage = usage_from_stream_line(line, seen)
            except (ValueError, TypeError, OverflowError):
                continue
            if usage is not None:
                observed, total = True, total + usage
        return total if observed else None
    return read


def _session_reader(session_id: str, sessions_root: Optional[Path] = None,
                    models_out: Optional[list] = None) -> Callable[[], Optional["lc.TokenUsage"]]:
    def read() -> Optional["lc.TokenUsage"]:
        try:
            models = lc.seat_usage(session_id, sessions_root)
        except Exception as exc:  # noqa: BLE001 -- ANY read failure is unreadable spend: a row, never an escape
            logger.warning("transcript for session %s unreadable: %s: %s", session_id,
                           type(exc).__name__, exc)
            return None
        if not models:  # no transcript found: unobservable, NOT zero
            return None
        if models_out is not None:
            models_out[:] = sorted(models)
        return _sum(models)
    return read


def _sum(models: Mapping[str, "lc.TokenUsage"]) -> "lc.TokenUsage":
    total = lc.TokenUsage()
    for u in models.values():
        total = total + u
    return total


# --- CLI ---------------------------------------------------------------------------------

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli() -> None:
    """Launch one lane, refuse a collision, and monitor its spend. It never ends a run.

    \b
    launch  CONTRACT   run `doit moment:pre-launch`, then spawn the provider once and
                       write a launch receipt + a job-to-lane record. A refusal spawns
                       nothing and exits 5. Every Claude launch carries `-n <slug>`.
    govern  SLUG       a monitor: records spend against the cap field, poll by poll.
                       It never stops, pauses or kills a lane -- not on an over-cap
                       reading, not on unreadable usage.
    plan    CONTRACT   print the launch plan as JSON; starts nothing.

    Run `dispatch.py <verb> --help` for a verb's options. The contract's Dispatch
    block is read for its fields (head, -n, --worktree, --model, --effort), never run."""


@cli.command("launch")
@click.argument("contract")
@click.option("--slug", default="", help="Lane slug; default: the Dispatch block's -n / --worktree, "
                                         "else LANE-<slug>.md from the file name.")
@click.option("--provider", default="", help="Overrides the Dispatch block's head "
                                             "(claude -> anthropic, codex -> codex).")
@click.option("--model", default="", help="Overrides the contract's model. No default.")
@click.option("--effort", default="", help="Overrides the contract's effort. No default.")
@click.option("--batch", default="", help="The batch the lane joins; pre-launch checks its integrator "
                                          "is live. Default: $HARNESS_BATCH.")
@click.option("--token-cap", "token_cap", type=int, default=None,
              help="Optional. Written into the launch receipt as the cap FIELD `govern` records "
                   "spend against. It stops nothing.")
@click.option("--secrets-file", type=click.Path(path_type=Path),
              default=Path.home() / "Documents" / ".secrets" / ".env", show_default=True)
@click.option("--dry-run", is_flag=True, help="Print the resolved request as JSON and start nothing "
                                              "(pre-launch is NOT run).")
def launch_cmd(contract: str, slug: str, provider: str, model: str, effort: str, batch: str,
               token_cap: Optional[int], secrets_file: Path, dry_run: bool) -> None:
    """Run `pre-launch`, then spawn the lane exactly once.

    Reads the contract's Dispatch block for the head program (claude|codex), the slug (-n /
    --worktree), the model and the effort; runs `doit moment:pre-launch` for the slug (occupancy, a
    live integrator, routing agreement); on a pass spawns `claude --bg -n <slug> ...` (or
    `codex exec ...`) and writes the launch receipt and a job-to-lane record under
    logs/receipts/. On a refusal it spawns nothing, prints the reason and exits 5. Nothing here can
    stop a lane that is already running."""
    path = (Path(contract).resolve() if Path(contract).is_file()
            else resolve_contract(contract, prompts_dir()))
    request = request_from_contract(path, slug=slug, provider=provider, model=model, effort=effort,
                                    batch=batch, token_cap=token_cap)
    if dry_run:
        click.echo(json.dumps({"schema": 1, "slug": request.slug, "provider": request.provider,
                               "model": request.model, "effort": request.effort, "batch": request.batch,
                               "token_cap": request.token_cap, "session_name": request.session_name,
                               "contract": str(request.contract), "prompt": request.prompt,
                               "argv": request.argv}))
        return
    result = launch_lane(request, prelaunch=run_prelaunch, spawn=spawn_process, agents=list_agents,
                         secrets_file=secrets_file)
    click.echo(f"[dispatch] launched {result.slug}: job {result.job_id}, session name "
               f"{result.session_name_reported or result.session_name!r}, model {result.model_requested} "
               f"(reported: {result.model_reported})", err=True)
    click.echo(json.dumps(asdict(result)))


@cli.command("plan")
@click.argument("contract")
@click.option("--slug", default="", help="Lane slug; default: LANE-<slug>.md from the file name.")
@click.option("--provider", default="anthropic", show_default=True)
@click.option("--model", default="", help="Overrides the contract's Model cell. No default.")
@click.option("--effort", default="", help="Overrides the contract's Effort cell. No default.")
@click.option("--substrate", type=click.Choice(SUBSTRATES), default="local", show_default=True)
@click.option("--token-cap", "token_cap", type=int, required=True,
              help="REQUIRED here (harness stage 11 fills the cap field with it). A record; stops nothing.")
@click.option("--repo", default="", help="owner/name; the codespace substrate only.")
@click.option("--branch", default="main", show_default=True)
@click.option("--secrets-file", type=click.Path(path_type=Path),
              default=Path.home() / "Documents" / ".secrets" / ".env", show_default=True)
@click.option("--emit-env", is_flag=True, help="Include the env delta's VALUES (a human should not).")
def plan_cmd(contract: str, slug: str, provider: str, model: str, effort: str, substrate: str,
             token_cap: int, repo: str, branch: str, secrets_file: Path, emit_env: bool) -> None:
    """Print the launch plan as JSON. Starts nothing; every pre-launch input error fires here."""
    validate_cap(token_cap)
    # the prompts dir is resolved LAZILY: an absolute contract must not be refused because an
    # unrelated authority drive is unmounted (the PS comment in Invoke-Dispatch.ps1 says why)
    path = (Path(contract).resolve() if Path(contract).is_file()
            else resolve_contract(contract, prompts_dir()))
    if not (model and effort):
        from_contract = parse_contract_model_effort(path.read_text(encoding="utf-8", errors="replace"))
        model, effort = model or from_contract[0], effort or from_contract[1]
    slug = slug or slug_from_contract(path)
    if not slug:
        raise DispatchRefused(f"no lane slug: {path.name!r} is not LANE-<slug>.md and --slug was "
                              "not given")
    prompt = f"Read and execute the frozen contract at {path}"
    lane = build_plan(provider, model, slug, effort, prompt,
                      streamed=(substrate == "codespace" and _provider(provider).head == "claude"))
    steps: list[dict] = []
    if substrate == "codespace":
        if not repo:
            raise DispatchRefused("--repo owner/name is required for the codespace substrate")
        steps = [{"argv": s.argv, "note": s.note} for s in codespace_plan(repo, branch, slug, path, lane.argv)]
    if (skip := branch_guard(slug, _git_branch_exists)) is not None:
        raise DispatchRefused(skip)
    env = child_env(provider, os.environ, read_secrets(secrets_file))
    env_set = {k: v for k, v in env.items() if os.environ.get(k) != v}
    click.echo(json.dumps({
        "schema": 1, "slug": slug, "provider": provider, "model": model,
        "effort": EFFORTS[effort.lower()], "token_cap": token_cap, "substrate": substrate,
        "metering": lane.metering, "argv": lane.argv, "prompt": prompt, "contract": str(path),
        "env_set": env_set if emit_env else {k: "<withheld>" for k in env_set},
        "env_unset": [k for k in os.environ if k not in env], "steps": steps}))


@dataclass(frozen=True)
class Step:
    argv: list[str]
    note: str = ""


def codespace_plan(repo: str, branch: str, slug: str, contract: Path, head_argv: Sequence[str],
                   machine: str = "basicLinux32gb", idle_timeout: str = "30m",
                   retention: str = "1d", workdir: str = "/workspaces/dispatch") -> list[Step]:
    """Ported from Start-DispatchCodespace. `{cs}` is the codespace NAME, read back from
    `gh codespace list` because the display name is not what later commands need. The prompt and
    the command travel as FILES; the only thing crossing the ssh boundary is `bash <path>`."""
    runner = f"{workdir}/run-{slug}.sh"
    return [
        Step(["gh", "codespace", "create", "-R", repo, "-b", branch, "--machine", machine,
              "--idle-timeout", idle_timeout, "--retention-period", retention, "-d", slug],
             "create"),
        Step(["gh", "codespace", "list", "--json", "name,displayName"], "read the NAME back"),
        Step(["gh", "codespace", "cp", "-c", "{cs}", "-e", str(contract),
              f"remote:{workdir}/{Path(contract).name}"], "ship the contract in"),
        Step(["gh", "codespace", "cp", "-c", "{cs}", "-e", "{runner}", f"remote:{runner}"],
             "ship the runner in"),
        Step(["gh", "codespace", "ssh", "-c", "{cs}", "--", "bash", runner], "run (stream-metered)"),
        Step(["gh", "codespace", "cp", "-c", "{cs}", "-e", f"remote:{workdir}/receipt.json",
              "{receipt}"], "pull the receipt back"),
    ]


@cli.command("govern")
@click.argument("lane_id", required=False, default="")
@click.option("--slug", required=True, help="Lane slug; its branch is worktree-<slug>.")
@click.option("--token-cap", "token_cap", type=int, default=None,
              help="The cap FIELD to record against. Default: the one in the slug's launch receipt; "
                   "none -> spend is recorded with no cap.")
@click.option("--count-cache-reads", is_flag=True, help="Also count cache reads.")
@click.option("--interval", type=float, default=15.0, show_default=True)
@click.option("--bind-polls", type=int, default=8, show_default=True,
              help="Attempts to find the lane's session id before the monitor gives up.")
@click.option("--max-polls", type=int, default=None,
              help="End THE MONITOR after this many polls (the lane is untouched). Default: watch "
                   "until the lane ends.")
@click.option("--blind-polls", type=int, default=8, show_default=True,
              help="End the monitor after this many polls in a row whose liveness cannot be read.")
@click.option("--sessions-root", type=click.Path(path_type=Path), default=None, hidden=True)
def govern_cmd(lane_id: str, slug: str, token_cap: Optional[int], count_cache_reads: bool,
               interval: float, bind_polls: int, max_polls: Optional[int], blind_polls: int,
               sessions_root: Optional[Path]) -> None:
    """Monitor a launched lane: record its spend against the cap field, poll by poll.

    A MONITOR, not a governor: it never stops, pauses or kills a lane -- not when the spend passes
    the cap, not when the usage is unreadable. Each poll appends a row (`used`, `cap`, `over_cap`,
    `readable`) to logs/receipts/LAUNCH-SPEND-<SLUG>.jsonl. Exit 0 finished; 3 the spend passed the
    cap (recorded after the fact -- the lane was NOT stopped); 4 spend or liveness was unreadable
    (recorded); 6/7 a finished lane committed nothing / could not be checked.

    LANE_ID may be omitted: it is read from the launch receipt, else the lane is FOUND by its
    worktree (`.../worktrees/<slug>`) in `claude agents --json`. Run from the CALLER's repo root
    (the commit witness reads its branches)."""
    receipt = read_launch_receipt(slug) or {}
    cap = token_cap if token_cap is not None else receipt.get("token_cap")
    if cap is not None:
        validate_cap(cap)
    path = _spend_path(slug)

    def record(row: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8", newline="\n") as sink:
            sink.write(json.dumps({"slug": slug, "job_id": lane_id or receipt.get("job_id", ""), **row}) + "\n")

    models: list = []
    try:
        verdict = _watch(receipt, lane_id, slug, cap, record, models, interval, bind_polls,
                         max_polls, blind_polls, count_cache_reads, sessions_root)
    except KeyboardInterrupt:
        # ending THE MONITOR is all Ctrl-C does: nothing here holds a handle on the lane
        verdict = MonitorVerdict(0, None, cap, unobserved="the monitor was interrupted")
    except Exception as exc:  # noqa: BLE001 -- a monitor that crashes says so and exits; the lane is untouched
        verdict = MonitorVerdict(0, None, cap, unobserved=f"the monitor failed ({type(exc).__name__}: {exc})")
    _finish(verdict, slug)


def _watch(receipt: dict, lane_id: str, slug: str, cap: Optional[int], record: Callable[[dict], None],
           models: list, interval: float, bind_polls: int, max_polls: Optional[int], blind_polls: int,
           count_cache_reads: bool, sessions_root: Optional[Path]) -> MonitorVerdict:
    """Bind the lane (or its log) and run the monitor. Reads and records; touches nothing."""
    if receipt.get("provider") == "codex" and receipt.get("log_path") and isinstance(receipt.get("pid"), int):
        pid = receipt["pid"]
        read_usage, alive = _log_reader(Path(receipt["log_path"])), (lambda: process_alive(pid))
        shown = receipt.get("job_id", "?")
    else:
        given = lane_id or (receipt.get("job_id") if receipt.get("job_id") not in (None, "unresolved") else "")
        lane_id, binding = _bind(str(given), slug, bind_polls, interval)
        if binding is None or not binding.session_id:
            why = (f"no lane for worktree-{slug} could be identified in `claude agents --json`"
                   if binding is None else f"lane {lane_id} carries no session id to read usage from")
            record({"poll": 0, "used": None, "cap": cap, "over_cap": False, "readable": False, "models": []})
            return MonitorVerdict(0, None, cap, unobserved=why)
        read_usage = _session_reader(binding.session_id, sessions_root, models)
        alive = lambda: lane_alive(lane_id)  # noqa: E731
        shown = lane_id
    click.echo(f"[dispatch] monitoring {slug} (job {shown}) -- cap {cap if cap is not None else 'none'}; "
               "this never stops the lane", err=True)
    return monitor(cap=cap, read_usage=read_usage, alive=alive, record=record, interval=interval,
                   max_polls=max_polls, blind_polls=blind_polls, count_cache_reads=count_cache_reads,
                   models=models)


def _cwd_is_lane(cwd: str, slug: str) -> bool:
    """Is `cwd` the worktree `.../worktrees/<slug>` the launched lane runs in?"""
    return cwd.replace("\\", "/").rstrip("/").lower().endswith(f"/worktrees/{slug}".lower())


def _bind(lane_id: str, slug: str, polls: int, interval: float) -> tuple[str, Optional[LaneBinding]]:
    """`(lane id, binding)`, or `("", None)` when no lane could be tied to the slug.

    A PROVISIONAL id (from the launch receipt or the command line) is trusted only once its listed
    worktree is the slug's AND its record is LIVE (an old `done` record for the same worktree is not
    the lane just launched). One that is not listed, is ended, or belongs to another lane is
    dropped, and the lane is FOUND by worktree instead (`find_lane_by_slug`)."""
    for attempt in range(max(polls, 1)):
        binding = bind_lane(lane_id) if lane_id else None
        if binding is None or not binding.live or not _cwd_is_lane(binding.cwd, slug):
            lane_id = find_lane_by_slug(slug) or ""
            binding = bind_lane(lane_id) if lane_id else None
        if binding is not None and lane_id:
            return lane_id, binding
        if attempt + 1 < polls:
            time.sleep(min(interval, 3.0))
    return "", None


def _finish(verdict: MonitorVerdict, slug: str) -> None:
    """Report the verdict and exit. A lane SEEN to end under a clean verdict must also have
    committed something. Never returns."""
    _report(verdict)
    code = verdict.exit_code
    if code == 0 and verdict.ended:
        outcome, reason = commit_witness(slug)
        click.echo(f"[dispatch] {outcome}: {reason}")
        code = {"DONE": 0, "FAILED": EXIT_NO_COMMIT}.get(outcome, EXIT_UNWITNESSED)
    sys.exit(code)


def _report(verdict: MonitorVerdict) -> None:
    if verdict.over_cap:
        state = "CAP EXCEEDED -- recorded; the lane was NOT stopped (this monitor never stops a lane)"
    elif verdict.unobserved:
        state = f"UNOBSERVED ({verdict.unobserved}) -- recorded; the lane was not touched"
    elif verdict.ended:
        state = "lane finished"
    else:
        state = f"monitor ended after {verdict.polls} poll(s); the lane was not touched"
    used = "unread" if verdict.used is None else verdict.used
    click.echo(f"[dispatch] {state}: used {used} of {verdict.cap if verdict.cap is not None else 'no cap'}")


if __name__ == "__main__":  # pragma: no cover
    cli()
