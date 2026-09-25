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
`not attestable`. Copilot is the same -- there is no live transcript this module reads a served
model back from -- so it carries the same value. A Claude launch has served nothing yet, so its
`model_reported` is `pending`; the served model lands in `govern`'s spend rows and in
`merge_receipt.py models`, from the transcript.

COPILOT RUNS DETACHED, NEVER AS A SHELL OF THE DISPATCHER (wave 5b blind spot 8: a Copilot
producer ran as a dispatcher shell and died with it). Like Codex, a Copilot launch is spawned
through `spawn_process`'s `log_path` branch -- `Popen` with the platform's detach flags, stdout to
a log file, no handle this module keeps -- rather than `subprocess.run` to completion. Its job id
is `copilot-<pid>`; it has no `--worktree` flag of its own, so (HONEST LIMIT) it runs in the
launch's own `cwd`, never a managed worktree the way Codex's does.

A MODEL ALIAS (`opus`, `sonnet`, `haiku`, `opusplan`) IS WARNED, NEVER REFUSED, NEVER REWRITTEN.
`warn_model_alias` names the explicit id `ecosystem/provider-registry.yaml` records that alias as
currently resolving to; the launch still runs with the alias exactly as the contract wrote it,
because resolving it here would be the same silent repoint the registry's own ALIAS DRIFT note
exists to make visible instead of committing again.

HONEST LIMITS
  * `launch` runs `doit moment:pre-launch` from the HUB root (dodo.py's own root) and spawns from the
    CALLER's cwd: a lane's worktree is created in the repo the operator stands in.
  * The second-launch refusal reads the launch receipt and the live job listing. A `claude --bg` job
    that has not been listed yet is not seen; the occupancy organ's session leg has the same window.
  * Codex `--worktree` is a managed worktree whose path this launcher does not choose: its receipt
    records `(codex-managed)`, and its job id is `codex-<pid>`.
  * Copilot has no such flag: unlike Codex, its worktree is whatever `cwd` this launcher was given.
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
from typing import Callable, Iterable, Mapping, Optional, Sequence

import click
import yaml

try:  # pragma: no cover -- exercised by whichever path the caller uses
    from scripts import lane_cost as lc
except ImportError:  # pragma: no cover
    import lane_cost as lc

try:  # pragma: no cover -- `queue`'s own ordering: no second contract-grammar reader here
    from scripts import plan_lint as pl
except ImportError:  # pragma: no cover
    import plan_lint as pl

try:  # pragma: no cover -- `queue`'s own RAM read: no second memory reader here
    from scripts import memory_admission_gate as mag
except ImportError:  # pragma: no cover
    import memory_admission_gate as mag

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
    # No key/base_url: the `copilot` CLI holds its own auth (`copilot login`), the way `codex`
    # does. Detached like codex -- see `launch_lane`'s `detached` set -- because it has no live
    # transcript this module reads a served model back from either.
    "copilot": Provider("copilot", metering="stream"),
}
_HEAD_PROVIDER = {"claude": "anthropic", "codex": "codex", "copilot": "copilot"}
#: Heads whose lane is spawned DETACHED (Popen + the platform's detach flags, stdout to a log
#: file) rather than run to completion in the caller's own process. Both report their own pid as
#: the job id (`_identify`) rather than being looked up in `claude agents --json`, and neither can
#: be attested for the model actually served (`NOT_ATTESTABLE`).
_DETACHED_HEADS = frozenset({"codex", "copilot"})


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


# --- a bare model ALIAS is warned, never refused, never rewritten ---------------------------------
#
# `ecosystem/provider-registry.yaml`'s own ALIAS DRIFT note records that Claude Code 2.1.280 made
# the bare `opus` alias resolve to `claude-opus-5-5` rather than the id lane contracts have
# pinned -- "a silent repoint: nothing in this registry moved and nothing in a lane contract that
# says `--model opus` changed, yet the model actually served underneath it did". That registry
# deliberately carries no alias FIELD (every `order[].model` there is a versioned id, by design),
# so this table is dispatch.py's own record of what each alias currently resolves to, cited
# against the same registry rows the note and the `models:` section already carry. It exists to
# make the drift VISIBLE at launch time, never to resolve it: `warn_model_alias` never changes
# `model`, because resolving the alias here would be the exact silent repoint the note exists to
# stop happening again.
MODEL_ALIASES: dict[str, str] = {
    # provider-registry.yaml's ALIAS DRIFT note (Claude Code 2.1.280+ default Opus).
    "opus": "claude-opus-5-5",
    # provider-registry.yaml `models.claude-sonnet-5` (roles.implement's pinned id).
    "sonnet": "claude-sonnet-5",
    # provider-registry.yaml `models.claude-haiku-4-5-20251001` (the id the CLI actually emits).
    "haiku": "claude-haiku-4-5-20251001",
    # a COMBO alias (Opus while planning, Sonnet while building) -- no single id, so both are named.
    "opusplan": "claude-opus-5-5 (plan mode) / claude-sonnet-5 (build mode)",
}


def warn_model_alias(model: str) -> Optional[str]:
    """A one-line warning when `model` is a bare Claude Code alias, naming the explicit id
    `MODEL_ALIASES` records the registry as currently resolving it to. `None` for a versioned id
    (or anything else `MODEL_ALIASES` does not name) -- never raised, and never changes what gets
    launched: the caller logs this and launches with `model` exactly as given."""
    target = MODEL_ALIASES.get(model.strip().lower())
    if target is None:
        return None
    return (f"the model {model!r} is a bare alias, not a versioned id -- the registry currently "
            f"resolves it to {target}. Launching with the alias exactly as the contract wrote "
            "it; pin the versioned id there to stop this from silently repointing again.")


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
                              "only `claude`, `codex` and `copilot` are launched. Refusing.")
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
    if p.head == "copilot":
        # `-p` (non-interactive; exits after completion) + `--allow-all-tools` (required for
        # non-interactive mode, per `copilot --help`) + `-n <slug>` (the same session-naming
        # discipline as Claude's `-n`, so a listing can name the lane back). `--reasoning-effort`
        # is copilot's own flag name for the same enum `--effort` names elsewhere.
        argv = ["copilot", "-p", prompt, "--model", model, "--reasoning-effort", eff,
                "--allow-all-tools", "-n", slug]
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
    # WARNED, NEVER REFUSED: an alias in the Model table or the Dispatch line is visible now
    # rather than silently re-deciding which id actually served the lane later. See the warning's
    # own docstring for why this never rewrites `model`.
    if (alias_warning := warn_model_alias(model)) is not None:
        logger.warning("%s: %s", slug, alias_warning)
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

#: A `seat_refusals.SeatRefusal`'s own rendering (`REFUSED [<id>]: <detail> -- <remedy>`; e.g.
#: `no-live-integrator`'s remedy names the exact `seat_registry.py bind` command a missing
#: integrator needs). WAVE5A blind spot 1: the refusal fired, but its fix scrolled off `_tail`'s
#: 600-char budget underneath doit's own per-task chatter and telemetry prints -- the launch was
#: refused without saying how to fix it. `run_prelaunch` below surfaces every line matching this
#: pattern WHOLE and UNTRUNCATED (never through `_tail`'s cap), rather than letting it compete for
#: shared budget with everything else doit printed, or with a SECOND refusal, or with its own
#: `--batch` value repeated inside the remedy (terra HIGH, 2026-09-25: a fixed cap on the joined
#: refusals can still cut the command out from under a long batch name or multiple refusals).
_REFUSED_LINE_RE = re.compile(r"^REFUSED \[[^\]]+\]:")


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
    refused = [ln.strip() for ln in said if _REFUSED_LINE_RE.match(ln.strip())]
    if refused:
        # NEVER through `_tail`: a fixed cap shared across every refused line -- or spent inside
        # one line's own repeated `--batch` value -- can still cut the exact remedy command out.
        return PreLaunch(False, " | ".join(refused))
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
    provider = str(receipt.get("provider") or "")
    if provider in _DETACHED_HEADS:  # codex, copilot: self-identified by pid, never claude-listed
        pid = receipt.get("pid")
        if isinstance(pid, int):
            return f"{provider} job {job} (pid {pid}) is still running" if process_alive(pid) else ""
        age = _age_seconds(receipt.get("launched_at"))   # an INTENT receipt: Popen may already have run
        if job and age is not None and age < LISTING_LAG_SECONDS:
            return f"a {provider} launch ({job}) began {int(age)}s ago and has not recorded its process yet"
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
        # DETACHED (codex, copilot): `Popen` + the platform's detach flags, stdout to a log file,
        # no handle kept here -- never `subprocess.run` to completion in the caller's own process
        # (wave 5b blind spot 8: a Copilot producer ran as a dispatcher shell and died with it).
        detached = provider.head in _DETACHED_HEADS
        log_path = receipts_dir() / f"LAUNCH-LOG-{request.slug.upper()}.jsonl" if detached else None
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
            started = spawn(request.argv, env, cwd, log_path) if detached else spawn(request.argv, env, cwd)
        except OSError as exc:
            _receipt_path(request.slug).unlink(missing_ok=True)
            raise LaunchRefused(f"{request.argv[0]} could not be started ({type(exc).__name__}: {exc}) -- "
                                "no lane was started") from exc
        if started.returncode != 0:
            _receipt_path(request.slug).unlink(missing_ok=True)
            raise LaunchRefused(f"{request.argv[0]} exited {started.returncode} -- no lane was started: "
                                f"{_tail(started.stdout, 300)}")
        # From here a lane IS running: whatever fails below, the receipt is still written.
        self_identified = provider.head if detached else ""
        job_id, session_id, reported_name = _identify(request, started, self_identified, agents, sleep, began)
        result = LaunchResult(
            slug=request.slug, provider=request.provider, model_requested=request.model,
            model_reported=NOT_ATTESTABLE if detached else MODEL_PENDING,
            job_id=job_id or "unresolved",
            worktree=("(codex-managed)" if codex
                      else str(cwd) if provider.head == "copilot"  # no --worktree flag of its own
                      else str(cwd / ".claude" / "worktrees" / request.slug)),
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


def _identify(request: LaunchRequest, started: Spawned, self_identified: str,
              agents: Callable[[], list[dict]], sleep: Callable[[float], None],
              since: float) -> tuple[str, str, str]:
    """`(job id, session id, the name the job record reports)` for a lane that has just started.
    Blank parts are unknown, never guessed: the id comes from the provider's own output, else the one
    live lane in the slug's worktree.

    `self_identified` is the provider HEAD when it reports its own pid rather than being looked up
    in `claude agents --json` (codex, copilot -- neither is a claude subagent); '' for claude."""
    if self_identified:
        return f"{self_identified}-{started.pid}", "", ""
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


# --- queue: the dispatcher's hand procedure becomes code (LANE-5B2-9) --------------------------
#
# WHY. WAVE5B-N1's dispatcher ran the queue BY HAND: a RAM gate read by eye off a screenshot, a
# dependency hold worked out by re-reading the integrator's prose receipts every tick, and 13
# orphan watcher loops that outlived their own usefulness (`to-browser/SESSION-dispatcher-wave5b-
# n1-2026-09-24.md`, "an-expired-monitor-leaves-its-bash-loop-running"). This section is that
# procedure as code: `launch_order` computes a static schedule from the contracts alone (priority
# = input order, `Starts after`, `serialize-group`, substrate); `decide_lane` turns that schedule
# plus LIVE state (an integrator receipt fixture, a local-lane count, free memory) into one
# decision per lane; `watch_queue` polls `decide_lane` in a loop that is BOUNDED BY CONSTRUCTION
# -- it returns at `deadline_s` whatever is still pending, so nothing started here can become an
# orphan loop the way N1's watchers did.
#
# NO SECOND CONTRACT-GRAMMAR READER. `launch_order` reuses `plan_lint.parse_lane_contract` /
# `build_edges` / `find_cycle` for the `Starts after` and `serialize-group` edges -- the exact
# grammar `lane-plan-lint-grammar` already wrote and reads, not a second regex set here that could
# drift from it. This module's only new reading is the substrate column (`dispatch_head` /
# `lane_substrate`), which plan_lint has no reason to know about.
#
# THE INTEGRATOR RECEIPT FIXTURE. No machine-readable "STATE <lane> MERGED <sha>" format existed
# before this lane -- the dispatcher's own session files carry that as PROSE, written by hand into
# a transcript. `read_lane_states` defines the smallest JSON shape a dependency hold can act on:
# `{"lanes": {"<slug>": {"state": "MERGED"|"FAILED", "sha": "..."}}}`. A slug this file does not
# mention reads WAITING, never a guessed MERGED -- an unreadable or absent fixture holds every
# dependent lane rather than assuming its dependency is done.
#
# SUBSTRATE IS READ, NEVER LAUNCHED. A `Dispatch-Codespace` head (`lane_substrate` via
# `dispatch_head`) routes a lane to `ROUTE-CODESPACE` and this module never spawns it -- exactly
# the refusal `dispatch.py launch` already gives a non-claude/codex/copilot head, surfaced here as
# a decision instead of an exception so a mixed-substrate queue does not stop on its first
# codespace lane. The codespace verb itself (`Dispatch-Codespace` / `Start-DispatchCodespace`) is
# PowerShell, outside this module's reach by design (the dispatcher order's own words: "NOT
# `scripts/dispatch.py launch`, which launches `claude`/`codex` heads only and refuses any other").
#
# A REPAIR IS NOT A LAUNCH. `launch_lane`'s `--worktree <slug>` provisions a FRESH tree; a repair
# must run inside the lane's EXISTING (locked) worktree or it abandons the branch the repair exists
# to fix -- the WAVE5A precedent `DECIDED-BY-LANE` in `SESSION-dispatcher-wave5b-n1-2026-09-24.md`
# ("Repairs"). `build_repair_plan` never emits `--worktree`; `repair_lane` spawns with `cwd` set to
# the pre-existing tree and REFUSES when it is not there (starting one is a fresh launch's job).
#
# HONEST LIMITS
#   * `local_live_count`/`live_slugs` read `claude agents --json` (via the caller's injected
#     functions, same as `govern`) -- a codespace lane's liveness is NOT observable this way (it is
#     a `gh codespace`, not a claude agent), so this module never claims to know one is live; it
#     only ever ROUTES a codespace lane away, never gates it on codespace-substrate occupancy.
#   * `launch_order` is a STATIC schedule from the contracts as given, not a live re-plan: it does
#     not know which lane is already running or already MERGED. `decide_lane`/`watch_queue` are
#     what reads live state; a caller wanting an order that reflects today's progress re-runs
#     `launch_order` after removing already-fired/terminal slugs from its input, the same way
#     `plan_pass` already skips them.
#   * `watch_queue`'s RAM and local-cap reads are single per-poll SNAPSHOTS, the same limits
#     `memory_admission_gate`'s own gate already carries -- two lanes clearing the same headroom
#     in the same poll is a real race this module does not arbitrate (the box-wide reserve is
#     `memory_admission_gate`'s job for a HEAVY COMMAND; this queue's floor is a coarser, launch-
#     time-only check, not a second admission-control system).


@dataclass(frozen=True)
class QueuedLane:
    """One contract, read for exactly what `queue` needs to place it in the schedule."""
    slug: str
    contract: Path
    priority: int                        # index in the order the caller passed the contracts
    starts_after: tuple[str, ...]
    serialize_group: Optional[str]
    substrate: str                        # "local" | "codespace"


#: "substrate: local" / "substrate: **codespace**" -- the contract header's own note (both real
#: spellings: LANE-5B2-1's is bolded, LANE-5B2-5's is not). Read only as a FALLBACK -- the Dispatch
#: block's own head is authoritative when it names `Dispatch-Codespace` (see `lane_substrate`).
_SUBSTRATE_LABEL_RE = re.compile(r"substrate:\s*\*{0,2}(?P<sub>[a-z]+)\*{0,2}", re.IGNORECASE)


def dispatch_head(text: str) -> str:
    """The `## Dispatch` fence's first token, lowercased -- read, never validated: unlike
    `parse_dispatch_block`, this must not raise on a `Dispatch-Codespace` head (queue reads EVERY
    lane's substrate, including the codespace ones `parse_dispatch_block` exists to refuse).
    '' when the contract carries no Dispatch fence at all."""
    lines = _dispatch_lines(text)
    if not lines:
        return ""
    tokens = _tokens(lines[0])
    return Path(tokens[0][0]).stem.lower() if tokens else ""


def lane_substrate(text: str) -> str:
    """`"codespace"` or `"local"` for one contract's full text.

    The Dispatch block's own head decides first: a `Dispatch-Codespace` head can ONLY be the
    codespace verb (`dispatch.py launch` refuses that head outright), so queue must route it away
    from a local spawn before `launch_lane` would ever get the chance to raise. A `claude`/`codex`/
    `copilot` head falls through to the contract's own `substrate: <label>` note, because
    `dispatch.py` CAN spawn those heads locally -- the label is what still says whether this lane
    sits outside the local RAM cap (a cloud/codespace lane dispatched some other way) or inside it.
    No note at all defaults to `"local"`, the common case."""
    if dispatch_head(text) == "dispatch-codespace":
        return "codespace"
    match = _SUBSTRATE_LABEL_RE.search(text)
    if match:
        label = match.group("sub").lower()
        if label in SUBSTRATES:
            return label
    return "local"


def load_queue(contracts: Sequence[Path]) -> tuple[QueuedLane, ...]:
    """Every contract in `contracts`, in the order given -- that order IS the priority ("merge
    priority = table order", `BATCH-WAVE5B-N2-2026-09-25.md` §2). Reuses `plan_lint.load_contracts`
    for the slug/`Starts after`/`serialize-group` grammar (a duplicate slug refuses, same as
    plan-lint itself); adds only the substrate read plan-lint has no reason to make."""
    parsed = pl.load_contracts(contracts)
    return tuple(
        QueuedLane(slug=lane.slug, contract=lane.path, priority=i, starts_after=lane.starts_after,
                  serialize_group=lane.serialize_group, substrate=lane_substrate(lane.full_text))
        for i, lane in enumerate(parsed))


#: Codespace before local when a round's ties are broken: a codespace lane never touches the local
#: RAM cap, so trying it first costs a static schedule nothing and mirrors the real batch's own
#: wave α (its one codespace lane sits first even though it is also lowest-priority by number).
_SUBSTRATE_RANK = {"codespace": 0, "local": 1}


def launch_order(lanes: Sequence[QueuedLane]) -> list[str]:
    """The static launch order: a BFS-layered topological sort over plan_lint's OWN dependency
    graph (`Starts after` + `serialize-group`, built exactly as `plan_lint.build_edges` builds it
    -- no second edge-builder here). Every lane whose dependencies are ALL already placed forms one
    ROUND, sorted by `(substrate, priority)`; the next round is computed only after the whole
    round is placed. LAYERED, not a flat priority queue: a lane a single edge frees late (wave
    gamma's 2/3/4/6/7/10) must never preempt a lane still waiting from an EARLIER round just
    because it happens to rank higher on substrate or priority -- a flat pop-lowest queue lets a
    freshly-freed codespace lane jump the entire local wave still sitting in the ready set, which
    is not the batch's own wave α/β/γ shape (`DISPATCHER-WAVE5B-N2-2026-09-25.md` §Sequence).

    Raises `DispatchRefused` on a cycle (reusing `plan_lint.find_cycle`'s own check) or when the
    graph leaves lanes unplaced -- the latter should be unreachable once the cycle check has
    passed, and is refused rather than silently dropping a lane from the printed order."""
    contracts = pl.load_contracts([lane.contract for lane in lanes])
    edges = pl.build_edges(contracts)
    cycle = pl.find_cycle(contracts, edges)
    if cycle is not None:
        raise DispatchRefused(
            f"queue: declared dependency edges form a cycle: {' -> '.join(cycle)} -- no launch "
            "order exists for this set of contracts")
    by_slug = {lane.slug: lane for lane in lanes}
    indeg: dict[str, int] = {lane.slug: 0 for lane in lanes}
    children: dict[str, list[str]] = {lane.slug: [] for lane in lanes}
    for a, b in edges:
        if a in by_slug and b in by_slug:
            indeg[b] += 1
            children[a].append(b)

    def _round_sort(slugs: list[str]) -> list[str]:
        return sorted(slugs, key=lambda s: (_SUBSTRATE_RANK.get(by_slug[s].substrate, 1),
                                            by_slug[s].priority))

    order: list[str] = []
    placed: set[str] = set()
    round_ = _round_sort([slug for slug, d in indeg.items() if d == 0])
    while round_:
        order.extend(round_)
        placed.update(round_)
        for slug in round_:
            for child in children[slug]:
                indeg[child] -= 1
        round_ = _round_sort([slug for slug, d in indeg.items() if d == 0 and slug not in placed])
    missing = set(by_slug) - placed
    if missing:
        raise DispatchRefused(f"queue: {len(missing)} lane(s) never became ready: {sorted(missing)} "
                              "-- a dependency this graph could not resolve")
    return order


# --- live decisions: dependency, serialize-group, local cap, RAM --------------------------------

def read_lane_states(path: Optional[Path]) -> dict[str, str]:
    """The integrator's lane-state fixture: `{"lanes": {"<slug>": {"state": "MERGED"|"FAILED",
    "sha": "..."}}}`. `path=None`, a missing file, or unreadable JSON all read as `{}` -- every
    dependency then reads WAITING, never a guessed MERGED (see the section docstring)."""
    if path is None:
        return {}
    try:
        body = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    lanes = body.get("lanes") if isinstance(body, dict) else None
    if not isinstance(lanes, dict):
        return {}
    out: dict[str, str] = {}
    for slug, row in lanes.items():
        if isinstance(row, dict) and isinstance(row.get("state"), str):
            out[str(slug)] = row["state"].strip().upper()
    return out


DEP_READY = "READY"
DEP_WAITING = "WAITING"
DEP_BLOCKED_FAILED = "BLOCKED-FAILED"


def dependency_status(lane: QueuedLane, states: Mapping[str, str]) -> str:
    """`READY` (no dependency, or every named one reads MERGED); `BLOCKED-FAILED` (any named one
    reads FAILED -- the Sequence's own rule: "A lane whose dependency is FAILED is not launched");
    else `WAITING` (a dependency is absent from the fixture, or present but not yet terminal)."""
    if not lane.starts_after:
        return DEP_READY
    seen = [states.get(dep, "") for dep in lane.starts_after]
    if any(s == "FAILED" for s in seen):
        return DEP_BLOCKED_FAILED
    if all(s == "MERGED" for s in seen):
        return DEP_READY
    return DEP_WAITING


def serialize_group_clear(lane: QueuedLane, all_lanes: Sequence[QueuedLane],
                          live_slugs: Iterable[str]) -> bool:
    """True when no OTHER member of `lane`'s `serialize-group` is currently live -- "never two
    members live" (Done-contract item 2). A lane with no group is trivially clear."""
    if not lane.serialize_group:
        return True
    live = set(live_slugs)
    members = {other.slug for other in all_lanes
              if other.serialize_group == lane.serialize_group and other.slug != lane.slug}
    return not (members & live)


ACTION_FIRE = "FIRE"
ACTION_HOLD = "HOLD"
ACTION_HELD_FAILED = "HELD-FAILED"
ACTION_ROUTE_CODESPACE = "ROUTE-CODESPACE"


@dataclass(frozen=True)
class QueueDecision:
    slug: str
    action: str
    reason: str


def decide_lane(lane: QueuedLane, *, states: Mapping[str, str], live_slugs: Iterable[str],
                all_lanes: Sequence[QueuedLane], local_cap: int, local_live_count: int,
                free_mb: float, floor_mb: float) -> QueueDecision:
    """One lane's decision, gate by gate, in the order a real launch must clear them: dependency,
    then `serialize-group`, then substrate (a codespace lane is ROUTED, never gated on cap/RAM --
    it does not use either), then the local cap, then the RAM floor."""
    dep = dependency_status(lane, states)
    if dep == DEP_BLOCKED_FAILED:
        return QueueDecision(lane.slug, ACTION_HELD_FAILED,
                             f"dependency FAILED: {', '.join(lane.starts_after)}")
    if dep == DEP_WAITING:
        return QueueDecision(lane.slug, ACTION_HOLD,
                             f"waiting on {', '.join(lane.starts_after)} to read MERGED")
    if not serialize_group_clear(lane, all_lanes, live_slugs):
        return QueueDecision(lane.slug, ACTION_HOLD,
                             f"serialize-group {lane.serialize_group!r} has a live member")
    if lane.substrate == "codespace":
        return QueueDecision(lane.slug, ACTION_ROUTE_CODESPACE,
                             "Dispatch-Codespace head -- the codespace verb launches this, never "
                             "a local spawn (dispatch.py launch refuses that head by design)")
    if local_live_count >= local_cap:
        return QueueDecision(lane.slug, ACTION_HOLD,
                             f"local cap {local_cap} full ({local_live_count} live)")
    if free_mb < floor_mb:
        return QueueDecision(lane.slug, ACTION_HOLD,
                             f"free {free_mb:.0f} MB is below the {floor_mb:.0f} MB floor")
    return QueueDecision(lane.slug, ACTION_FIRE, "clear")


def plan_pass(lanes: Sequence[QueuedLane], order: Sequence[str], *, fired: Iterable[str],
             states: Mapping[str, str], live_slugs: Iterable[str], local_cap: int,
             local_live_count: int, free_mb: float, floor_mb: float) -> list[QueueDecision]:
    """One decision per not-yet-RESOLVED slug in `order` (`fired` names every slug this pass
    should skip -- fired, held-failed or routed in an earlier pass; the name is kept for the
    common case, a fired lane, but callers pass every terminal slug here).

    RESERVES within THIS pass: a `FIRE` decision immediately counts toward `local_live_count` and
    joins `live_slugs` for every LATER decision in the same call -- Codex terra review, HIGH
    (`docs/audits/2026-09-25-codex-lane-launch-queue.md`): a single shared snapshot let several
    ready local lanes all pass a cap of four at once, and let two ready members of one
    `serialize-group` both read `FIRE` in the same pass, in direct violation of "never two members
    live". A `HELD-FAILED`/`ROUTE-CODESPACE` decision reserves NOTHING further -- neither one is a
    real local occupant, so it must not block a later `serialize-group` sibling in the same pass."""
    by_slug = {lane.slug: lane for lane in lanes}
    already = set(fired)
    live = set(live_slugs)
    count = local_live_count
    decisions: list[QueueDecision] = []
    for slug in order:
        if slug in already:
            continue
        decision = decide_lane(by_slug[slug], states=states, live_slugs=live, all_lanes=lanes,
                               local_cap=local_cap, local_live_count=count, free_mb=free_mb,
                               floor_mb=floor_mb)
        decisions.append(decision)
        if decision.action == ACTION_FIRE:
            count += 1
            live.add(slug)
    return decisions


# --- a repair relaunches into the lane's EXISTING worktree, never a fresh one --------------------

def build_repair_plan(model: str, slug: str, attempt: int, effort: str, prompt: str,
                      permission_mode: str = "bypassPermissions") -> Plan:
    """`claude --bg -n <slug>-repair-<attempt> ...` -- deliberately NO `--worktree` flag (unlike
    `build_plan`'s local-claude branch): a repair's `cwd` IS the lane's existing worktree, and
    `--worktree <slug>` would provision a fresh one, abandoning the branch under repair."""
    eff = EFFORTS.get(effort.lower())
    if eff is None:
        raise DispatchRefused(f"unknown effort {effort!r}. Valid: low, medium, high, xhigh, max "
                              "(or l/m/h/x)")
    name = f"{slug}-repair-{attempt}"
    argv = ["claude", "--bg", "-n", name, "--model", model, "--effort", eff, "--permission-mode",
            permission_mode, prompt]
    return Plan(argv, "transcript")


@dataclass(frozen=True)
class RepairRequest:
    slug: str
    attempt: int
    model: str
    effort: str
    contract: Path
    permission_mode: str = "bypassPermissions"

    @property
    def session_name(self) -> str:
        return f"{self.slug}-repair-{self.attempt}"

    @property
    def prompt(self) -> str:
        return (f"Repair for {self.slug} (attempt {self.attempt}): read the refusal and the "
                f"frozen contract at {self.contract}; fix only what the refusal names; hand back "
                "per the common rules.")

    @property
    def argv(self) -> list[str]:
        return build_repair_plan(self.model, self.slug, self.attempt, self.effort, self.prompt,
                                 self.permission_mode).argv


def repair_worktree_path(repo_root: Path, slug: str) -> Path:
    return Path(repo_root) / ".claude" / "worktrees" / slug


def repair_lane(request: RepairRequest, *, repo_root: Path,
                spawn: Callable[..., "Spawned"] = None,
                environ: Optional[Mapping[str, str]] = None) -> "Spawned":
    """Spawn the repair INTO `request.slug`'s existing worktree. Refuses (never spawns) when that
    worktree is not there: starting one is a fresh launch's job, not a repair's."""
    spawn = spawn or spawn_process
    tree = repair_worktree_path(repo_root, request.slug)
    if not tree.is_dir():
        raise DispatchRefused(f"no existing worktree at {tree} -- a repair reuses the lane's own "
                              "worktree; it does not start one (that is launch_lane's job)")
    env = dict(environ if environ is not None else os.environ)
    return spawn(request.argv, env, tree)


# --- watch: one bounded loop, never an orphan --------------------------------------------------

@dataclass(frozen=True)
class WatchResult:
    """`fired` is ONLY `ACTION_FIRE` -- lanes this watcher actually asked `on_fire` to launch.
    `held_failed` and `routed_codespace` are the other two ways a lane stops being pending, kept
    SEPARATE from `fired` (Codex terra review, HIGH,
    `docs/audits/2026-09-25-codex-lane-launch-queue.md`: folding all three into one `fired` set let
    `queue --watch` report "fired N/N; all clear" for a run where a dependency-failed lane was
    only HELD, or a codespace lane was never spawned at all -- neither is a launch, and a caller
    reading `fired` as "launched" would believe one happened that did not)."""
    polls: int
    expired: bool
    fired: tuple[str, ...]
    held_failed: tuple[str, ...] = ()
    routed_codespace: tuple[str, ...] = ()

    @property
    def terminal(self) -> frozenset[str]:
        """Every slug this watcher is done waiting on, for any of the three reasons."""
        return frozenset(self.fired) | frozenset(self.held_failed) | frozenset(self.routed_codespace)


def watch_queue(lanes: Sequence[QueuedLane], order: Sequence[str], *, deadline_s: float,
                poll_interval_s: float = 60.0, sleep: Callable[[float], None] = time.sleep,
                clock: Callable[[], float] = time.monotonic,
                on_fire: Optional[Callable[[str], None]] = None,
                states_fn: Optional[Callable[[], Mapping[str, str]]] = None,
                live_slugs_fn: Optional[Callable[[], Iterable[str]]] = None,
                local_live_count_fn: Optional[Callable[[], int]] = None,
                free_mb_fn: Optional[Callable[[], float]] = None,
                local_cap: int = 4, floor_mb: float = 3072.0,
                max_polls: Optional[int] = None) -> WatchResult:
    """Poll `plan_pass` until every lane is `FIRE`d or terminal (`HELD-FAILED`/`ROUTE-CODESPACE`),
    OR `deadline_s` elapses -- whichever comes first, NEVER longer (each sleep is CLAMPED to what
    is left before the deadline, Codex terra review HIGH: a full, un-clamped `poll_interval_s`
    sleep with little time left overshoots past `deadline_s` before the next check catches it).

    This is the fix for N1's 13 orphan watcher loops: every watcher this queue starts carries its
    own deadline and self-terminates at it, still-pending lanes and all (the caller reads
    `WatchResult.expired` and `order` minus `.terminal` to see what is left). `on_fire`, when
    given, is called once per lane the instant it clears every gate -- the caller's own launch
    (local) side effect; this function itself never spawns anything, and never calls `on_fire` for
    a `HELD-FAILED`/`ROUTE-CODESPACE` decision (neither one is a launch)."""
    states_fn = states_fn or (lambda: {})
    live_slugs_fn = live_slugs_fn or (lambda: ())
    local_live_count_fn = local_live_count_fn or (lambda: 0)
    free_mb_fn = free_mb_fn or (lambda: float("inf"))
    start = clock()
    fired: set[str] = set()
    held_failed: set[str] = set()
    routed: set[str] = set()
    polls = 0

    def _result(expired: bool) -> WatchResult:
        return WatchResult(polls, expired, tuple(fired), tuple(held_failed), tuple(routed))

    while True:
        polls += 1
        resolved = fired | held_failed | routed
        decisions = plan_pass(lanes, order, fired=resolved, states=states_fn(),
                              live_slugs=live_slugs_fn(), local_cap=local_cap,
                              local_live_count=local_live_count_fn(), free_mb=free_mb_fn(),
                              floor_mb=floor_mb)
        for decision in decisions:
            if decision.action == ACTION_FIRE:
                if on_fire is not None:
                    on_fire(decision.slug)
                fired.add(decision.slug)
            elif decision.action == ACTION_HELD_FAILED:
                held_failed.add(decision.slug)
            elif decision.action == ACTION_ROUTE_CODESPACE:
                routed.add(decision.slug)
        resolved = fired | held_failed | routed
        if all(slug in resolved for slug in order):
            return _result(expired=False)
        elapsed = clock() - start
        if elapsed >= deadline_s or (max_polls is not None and polls >= max_polls):
            return _result(expired=True)
        remaining = deadline_s - elapsed
        sleep(min(poll_interval_s, remaining) if remaining > 0 else 0.0)


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
    queue   CONTRACTS  the launch order (priority, Starts after, serialize-group,
                       substrate), and, unless --dry-run, one pass or a bounded
                       --watch loop firing whatever clears the dependency/cap/RAM
                       gates. A codespace lane is routed, never spawned here.
    repair  SLUG CONTRACT   relaunch a repair into SLUG's EXISTING worktree -- never
                       a fresh `--worktree`.

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
    provider = receipt.get("provider")
    if provider == "codex" and receipt.get("log_path") and isinstance(receipt.get("pid"), int):
        pid = receipt["pid"]
        read_usage, alive = _log_reader(Path(receipt["log_path"])), (lambda: process_alive(pid))
        shown = receipt.get("job_id", "?")
    elif provider == "copilot":
        # Copilot is not a claude agent (`claude agents --json` never lists it), so falling
        # through to the claude-agent bind below would search a listing that can never carry it
        # and report a MISLEADING reason (terra HIGH, 2026-09-25). Copilot's CLI does carry a
        # supported usage surface (`--usage-output-file`, `--output-format json`), but this
        # module does not read either one yet: honest, explicit UNOBSERVED -- never a false zero,
        # never a stop -- until that reader exists.
        record({"poll": 0, "used": None, "cap": cap, "over_cap": False, "readable": False, "models": []})
        return MonitorVerdict(0, None, cap, unobserved=(
            "copilot governance is not implemented yet: no claude-agent identity to bind to, and "
            "no reader for the CLI's own usage surface (--usage-output-file / --output-format "
            "json)"))
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


@cli.command("queue")
@click.argument("contracts", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--batch", default="", help="Passed through as --batch to every local launch fired.")
@click.option("--cap", type=int, default=4, show_default=True,
              help="Max live LOCAL lanes at once (codespace lanes never count against it).")
@click.option("--floor-mb", type=float, default=3072.0, show_default=True,
              help="Minimum free memory to fire a local lane.")
@click.option("--state-file", type=click.Path(path_type=Path), default=None,
              help="The integrator's lane-state fixture (JSON): {\"lanes\": {\"<slug>\": "
                   "{\"state\": \"MERGED\"|\"FAILED\"}}}. Default: none -- every dependency "
                   "reads WAITING.")
@click.option("--dry-run", is_flag=True, help="Print the static order only. Reads and spawns "
                                              "nothing.")
@click.option("--watch", is_flag=True, help="Loop, firing lanes as they clear, until every lane "
                                            "is fired/terminal or --deadline-s passes.")
@click.option("--deadline-s", type=float, default=3600.0, show_default=True)
@click.option("--poll-interval", type=float, default=60.0, show_default=True)
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path), default=HUB_ROOT,
              show_default=True)
@click.option("--secrets-file", type=click.Path(path_type=Path),
              default=Path.home() / "Documents" / ".secrets" / ".env", show_default=True)
def queue_cmd(contracts: tuple[Path, ...], batch: str, cap: int, floor_mb: float,
             state_file: Optional[Path], dry_run: bool, watch: bool, deadline_s: float,
             poll_interval: float, repo_root: Path, secrets_file: Path) -> None:
    """The launch order for CONTRACTS, computed from the contracts alone (priority = the order
    given, `Starts after`, `serialize-group`, substrate) -- reusing plan_lint's own dependency
    grammar, never a second reader of it.

    --dry-run prints that static order and exits; touches nothing live. Otherwise this runs ONE
    pass over it (or, with --watch, a bounded loop -- see `watch_queue`) firing whatever clears
    its dependency (the --state-file fixture), `serialize-group`, local-cap and RAM gates. A
    codespace lane (`Dispatch-Codespace` head) is reported ROUTE-CODESPACE and never spawned here
    -- `dispatch.py launch` refuses that head by design; use the codespace verb for it."""
    lanes = load_queue(list(contracts))
    order = launch_order(lanes)
    by_slug = {lane.slug: lane for lane in lanes}
    if dry_run:
        click.echo(f"[queue] {len(order)} lane(s), static order:")
        for i, slug in enumerate(order, 1):
            click.echo(f"  {i:2d}. {slug} ({by_slug[slug].substrate})")
        return

    def do_launch(slug: str) -> None:
        request = request_from_contract(by_slug[slug].contract, batch=batch)
        # `cwd=repo_root`: Codex terra review, HIGH -- without it, `launch_lane` defaulted to
        # `Path.cwd()`, so `--repo-root` was accepted but silently had no effect on where a
        # queued local lane's worktree was created.
        result = launch_lane(request, secrets_file=secrets_file, cwd=repo_root)
        click.echo(f"[queue] FIRE {slug}: job {result.job_id}", err=True)

    def live_slugs() -> set:
        try:
            agents = list_agents()
        except ListingUnreadable:
            return set()
        return {lane.slug for lane in lanes if find_lane_by_slug_in(agents, lane.slug)}

    def local_live_count() -> int:
        return len({s for s in live_slugs() if by_slug[s].substrate == "local"})

    states_fn = lambda: read_lane_states(state_file)  # noqa: E731

    if watch:
        result = watch_queue(lanes, order, deadline_s=deadline_s, poll_interval_s=poll_interval,
                             on_fire=do_launch, states_fn=states_fn, live_slugs_fn=live_slugs,
                             local_live_count_fn=local_live_count, free_mb_fn=mag.free_memory_mb,
                             local_cap=cap, floor_mb=floor_mb)
        pending = [s for s in order if s not in result.terminal]
        click.echo(f"[queue] watch ended after {result.polls} poll(s): fired {len(result.fired)}, "
                   f"held-failed {len(result.held_failed)}, routed-codespace "
                   f"{len(result.routed_codespace)}, of {len(order)}; "
                   f"{'DEADLINE -- still pending: ' + ', '.join(pending) if result.expired else 'all clear'}")
        return

    decisions = plan_pass(lanes, order, fired=(), states=states_fn(), live_slugs=live_slugs(),
                          local_cap=cap, local_live_count=local_live_count(),
                          free_mb=mag.free_memory_mb(), floor_mb=floor_mb)
    for decision in decisions:
        if decision.action == ACTION_FIRE:
            do_launch(decision.slug)
        else:
            click.echo(f"[queue] {decision.action} {decision.slug}: {decision.reason}")


@cli.command("repair")
@click.argument("slug")
@click.argument("contract", type=click.Path(exists=True, path_type=Path))
@click.option("--attempt", type=int, default=1, show_default=True)
@click.option("--model", required=True)
@click.option("--effort", required=True)
@click.option("--permission-mode", default="bypassPermissions", show_default=True)
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path), default=HUB_ROOT,
              show_default=True)
def repair_cmd(slug: str, contract: Path, attempt: int, model: str, effort: str,
              permission_mode: str, repo_root: Path) -> None:
    """Relaunch a REPAIR of SLUG into its EXISTING worktree -- never a fresh `--worktree`.
    Refuses when that worktree is not there (starting one is a fresh launch's job)."""
    request = RepairRequest(slug=slug, attempt=attempt, model=model, effort=effort,
                            contract=Path(contract).resolve(), permission_mode=permission_mode)
    spawned = repair_lane(request, repo_root=Path(repo_root))
    click.echo(f"[dispatch] repair {request.session_name} spawned: {_tail(spawned.stdout, 300)}")


if __name__ == "__main__":  # pragma: no cover
    cli()
