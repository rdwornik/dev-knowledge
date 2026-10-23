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
`--slug` on `launch` or `plan` may restate that slug but never replace it: a `--slug` the block
disagrees with is REFUSED (`contract_slug`), never silently preferred.
Model and effort come from an explicit flag, the block, or the contract's `| Model | Mode | Effort |`
table -- never a default ([#717]); the block and the table disagreeing is a refusal.

THE CAP IS A RECORD (N3). `--token-cap` is REQUIRED on `plan` (harness stage 11 fills the cap
field with it; without it `plan` exits 2) and optional on `launch`. When given it is written into the launch
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

import hashlib
import json
import logging
import os
import re
import secrets
import shlex
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Iterable, Mapping, Optional, Sequence

import click
import psutil
import yaml
from filelock import FileLock, Timeout as FileLockTimeout

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

try:  # pragma: no cover -- the Codespace legs' classifier: one reader of the creation log and the lane's progress
    from scripts import codespace_state as cs
except ImportError:  # pragma: no cover
    import codespace_state as cs

try:  # pragma: no cover -- the regime ledger: the ONE writer of a lane's fate row (`write_fate`)
    from scripts import codespace_regime as regime
except ImportError:  # pragma: no cover
    import codespace_regime as regime

try:  # pragma: no cover -- the sign-in table and the expiry reader the launch-time mirror shares with C1
    from scripts import codespace_parity as cpar
except ImportError:  # pragma: no cover
    import codespace_parity as cpar

try:  # pragma: no cover -- the alias table below is derived from the registry, never hand-copied
    from scripts import transport as _transport
except ImportError:  # pragma: no cover
    import transport as _transport

try:
    from scripts import provider_registry as _preg
except ImportError:  # pragma: no cover
    import provider_registry as _preg

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


class AlreadyLaunched(LaunchRefused):
    """The slug's earlier launch is still holding it. Still a refusal (exit 5, nothing spawned) for
    `launch`; `queue` reads it as "already launched" -- a fact about one lane, not a reason to stop
    the pass ([#1572])."""


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
# so this table is dispatch.py's own record of what each alias currently resolves to. It is
# DERIVED from the registry's `seat-integrator`, `seat-orchestrator` and `read` roles by
# `provider_registry.claude_alias_ids`, so no id is copied here. It exists to
# make the drift VISIBLE at launch time, never to resolve it: `warn_model_alias` never changes
# `model`, because resolving the alias here would be the exact silent repoint the note exists to
# stop happening again.
MODEL_ALIASES: dict[str, str] = _preg.claude_alias_ids()


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
    got = _line_fields(tokens)
    _validate_line(got)
    return DispatchLine(head=head, **got)


def _line_fields(tokens: Sequence[tuple[str, bool]]) -> dict[str, str]:
    """The known flags' values on a tokenized Dispatch line, UNVALIDATED (`_validate_line` judges them)."""
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
    return got


def dispatch_block_slug_line(text: str) -> Optional[DispatchLine]:
    """Only the Dispatch block's `-n` / `--worktree`, read even when its head or another field is one
    `parse_dispatch_block` refuses: the slug check must never ride on the rest of the line being valid."""
    lines = _dispatch_lines(text)
    if not lines:
        return None
    got = _line_fields(_tokens(lines[0]))
    return DispatchLine(head="", name=got.get("name", ""), worktree=got.get("worktree", ""))


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


#: The section-3 LANE REPORT JSON Schema ([#1368]) -- generated from
#: `ecosystem/schema/lane_report.LaneReport`, never hand-edited.
LANE_REPORT_SCHEMA = Path(__file__).resolve().parents[1] / "ecosystem" / "schema" / "lane-report.schema.json"


#: The API refuses these at the TOP level of a `--json-schema` (nested ones are accepted) ([#1537]).
_API_REFUSED_TOP_LEVEL = frozenset({"$schema", "allOf", "anyOf", "oneOf"})


def api_safe_schema(schema: dict) -> dict:
    """A new dict: `schema` minus the top-level keys the API refuses. The input is never mutated."""
    return {k: v for k, v in schema.items() if k not in _API_REFUSED_TOP_LEVEL}


def lane_report_schema_arg() -> str:
    """The LANE REPORT schema as ONE compact argv token, for `claude -p --json-schema`."""
    schema = api_safe_schema(json.loads(LANE_REPORT_SCHEMA.read_text(encoding="utf-8")))
    return json.dumps(schema, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class SmokeResult:
    ok: bool
    exit_code: int
    detail: str


_SCHEMA_SMOKE_PROMPT = ('Reply with a minimal LANE REPORT: state FAILED, reason "schema smoke". '
                        "Do not use any tool.")
_SCHEMA_SMOKE_TIMEOUT_S = 300


def schema_smoke_argv(head_argv: Sequence[str]) -> Optional[list[str]]:
    """The argv of a one-shot live `claude` call carrying the head's own `--json-schema` token, or None
    when the head is not a claude head with a schema."""
    head = list(head_argv)
    if not head or head[0] != "claude" or "--json-schema" not in head:
        return None
    token_at = head.index("--json-schema") + 1
    if token_at >= len(head) or "--model" not in head or head.index("--model") + 1 >= len(head):
        return None
    model = head[head.index("--model") + 1]
    return ["claude", "-p", "--output-format", "json", "--model", model, "--effort", "low",
            "--json-schema", head[token_at], _SCHEMA_SMOKE_PROMPT]


def run_schema_smoke(argv: Sequence[str]) -> SmokeResult:
    """Run the smoke for real: ok iff exit 0 and the stdout JSON says `is_error` false."""
    try:
        proc = subprocess.run(list(argv), stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=_SCHEMA_SMOKE_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return SmokeResult(False, 124, f"timed out after {_SCHEMA_SMOKE_TIMEOUT_S}s")
    except OSError as exc:
        return SmokeResult(False, 127, str(exc)[:300])
    stdout = proc.stdout or ""
    payload = None
    try:
        payload = json.loads(stdout)
    except ValueError:
        pass
    is_error = payload.get("is_error") if isinstance(payload, dict) else None
    ok = proc.returncode == 0 and is_error is False
    if ok:
        return SmokeResult(True, 0, "")
    text = ""
    if isinstance(payload, dict) and isinstance(payload.get("result"), str):
        text = payload["result"]
    text = text or stdout.strip() or (proc.stderr or "").strip()
    return SmokeResult(False, proc.returncode, text[:300])


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
        #
        # R15's git/gh denial (lane-scope-guard, WAVE5B-N4): `--deny-tool shell
        # --disable-builtin-mcps`. LIBRARY-FIRST FIRST, AND IT FAILED (O-12): Copilot CLI
        # 1.0.88's own `--deny-tool` has NO command-scoped form -- verified live, `--deny-tool
        # "shell(git)"` is accepted as an argument but never denies anything (`git status` still
        # ran); only a whole TOOL NAME is enforced (`--deny-tool shell` denies every shell call,
        # git or not). A per-command scope ("deny git, allow ls") therefore does not exist in
        # this CLI version to ask for. Denying the whole `shell` tool is the only mechanism this
        # CLI exposes that is categorically unbypassable through another shell -- there is no
        # shell left to wrap anything in, which is a STRONGER property than a git-specific
        # pattern match would have been, not a narrower one. `--disable-builtin-mcps` closes the
        # other path to the same actions (the bundled `github-mcp-server`'s structured
        # create_pr/etc. tools, gh's own non-shell equivalent). Verified live 2026-09-27: a
        # direct `git status` and a `powershell -Command "git status"` wrapper are BOTH refused
        # ("Permission to run this tool was denied due to the following rules: `shell`"),
        # command + output recorded in to-browser/SESSION-lane-scope-guard.md. Copilot's role
        # here is producer only (R8) -- the harness's own git/gh calls (dispatch, integrate,
        # push) never route through this head, so shell has nothing this lane needs it for.
        argv = ["copilot", "-p", prompt, "--model", model, "--reasoning-effort", eff,
                "--allow-all-tools", "--deny-tool", "shell", "--disable-builtin-mcps",
                "-n", slug]
        return Plan(argv, "stream")
    if streamed:  # a headless claude, for a substrate that cannot hand over a transcript
        # [#1368] Done 3: the lane's final answer is its section-3 LANE REPORT, enforced by the
        # CLI's own flag rather than a tool of ours. `--json-schema` takes the schema INLINE
        # (`claude --help`, 2.1.296), so the value is the schema file's content, compacted to one
        # token -- the file stays the single source (`ecosystem/schema/lane_report.py`).
        argv = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", model,
                "--effort", eff, "--permission-mode", permission_mode,
                "--json-schema", lane_report_schema_arg(), prompt]
        return Plan(argv, "stream")
    # `-n <slug>` names the session, so the Agent View row is the lane's own name and not the
    # contract prompt's first words. --permission-mode is not optional: nobody is at a --bg lane's
    # keyboard, so a prompt is a silent stall that looks exactly like a slow lane.
    argv = ["claude", "--bg", "-n", slug, "--model", model, "--effort", eff, "--permission-mode",
            permission_mode, "--worktree", slug, "--disallowedTools=AskUserQuestion", prompt]
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


def contract_slug(path: Path, line: Optional[DispatchLine], slug: str = "") -> str:
    """The lane's one slug: the Dispatch block's `-n`/`--worktree`, else `LANE-<slug>.md`. An
    explicit `slug` may restate the block's but never replace it -- a disagreement is REFUSED."""
    if line is not None and line.name and line.worktree and line.name != line.worktree:
        raise DispatchRefused(f"the Dispatch block names the session {line.name!r} but the worktree "
                              f"{line.worktree!r}; a lane has one slug. Fix the contract.")
    from_block = (line.name or line.worktree) if line else ""
    if slug and from_block and slug != from_block:
        raise DispatchRefused(f"--slug {slug!r} disagrees with the contract's Dispatch block, which names "
                              f"the lane {from_block!r} (-n / --worktree). Refusing rather than silently "
                              "replacing it: drop --slug, or fix the contract.")
    slug = slug or from_block or slug_from_contract(path)
    if not slug:
        raise DispatchRefused(f"no lane slug: {path.name!r} is not LANE-<slug>.md, the Dispatch block "
                              "names none, and --slug was not given")
    if not _SLUG.match(slug):
        raise DispatchRefused(f"{slug!r} is not a usable lane slug (letters, digits, '.', '_', '-')")
    return slug


def request_from_contract(contract: Path, *, slug: str = "", provider: str = "", model: str = "",
                          effort: str = "", permission_mode: str = "", batch: str = "",
                          token_cap: Optional[int] = None) -> LaunchRequest:
    """Resolve a contract into a `LaunchRequest`. Explicit arguments beat the Dispatch block, which
    beats the file name (slug) and the `| Model | Mode | Effort |` table (model, effort). Two
    sources that disagree are a refusal, never a quiet pick."""
    path = Path(contract)
    text = path.read_text(encoding="utf-8", errors="replace")
    line = parse_dispatch_block(text)
    slug = contract_slug(path, line, slug)
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
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8", newline="\n")


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


def _require_contract_file(contract: Path) -> None:
    """The check click's `exists=True` made, run AFTER the batch grammar so a malformed batch is refused
    (rc 5) before a missing contract is (rc 2). Same message, same rc."""
    if not Path(contract).exists():
        raise click.BadParameter(f"Path '{contract}' does not exist.", param_hint="'CONTRACT'")


def _refuse_malformed_batch(slug: str, batch: str) -> None:
    """P1, fail closed: a NON-EMPTY batch id outside `E<n>.<n>` (`x`, `B1`, `E2.0junk`, `E2.0 `) is
    refused (rc 5, `REFUSED [batch-grammar]`) by `launch`, `codespace-exec` and `repair` alike, BEFORE
    any spawn, box create, `gh` call or spend. One grammar, `subst_gate.batch_grammar_ok`, no
    normalisation of the value as supplied. An empty batch is the callers' own case."""
    import subst_gate                                 # lazy: subst_gate imports this module lazily too
    if subst_gate.batch_malformed(batch):
        raise LaunchRefused(subst_gate.batch_grammar_refusal(slug, batch))


def run_prelaunch(request: LaunchRequest, hub: Path = HUB_ROOT, *, repair: bool = False) -> PreLaunch:
    """Run the DECLARED `pre-launch` moment (ecosystem/harness.yaml) for this lane, from the hub.

    The organs are whatever the file declares -- occupancy, a live integrator, routing agreement --
    and this function names none of them: a non-zero exit is a refusal whose reason is the organs'
    own output. Raises OSError when `uv` cannot run; the caller treats that as a refusal too.

    `HARNESS_MODEL` is the model this launch will actually use, so the `model_per_role` organ judges the
    launch and not only the contract (P1: a substitution at the CLI is a substitution). `repair=True`
    (the `repair` verb, item 2b) sets `HARNESS_REPAIR=1`: a repair expects the lane's OWN worktree,
    directory and branch, which `worktree_occupancy` must then not count as occupancy but MUST find
    (a repair into a hand-made directory is refused) -- a busy session in the tree still refuses. The flag is dropped from the child env otherwise, so a stale one in the
    caller's shell cannot weaken a fresh launch."""
    env = dict(os.environ)
    env["HARNESS_LANE"] = request.slug
    env["HARNESS_CONTRACT"] = str(request.contract)
    env["HARNESS_MODEL"] = request.model
    env.pop("HARNESS_REPAIR", None)
    if repair:
        env["HARNESS_REPAIR"] = "1"
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


# The holder started BEFORE it wrote the stamp, so a process that began much later is a recycled
# pid; the slack absorbs boot-time and clock jitter so a live holder is never judged dead.
_LOCK_PID_RECYCLE_SLACK_S = 120
_LOCK_LINE = re.compile(r"^pid (\d+) at (\S+)\s*$")
_LOCK_ATTEMPTS = 3
_LOCK_RECLAIM_TIMEOUT_S = 30


def _lock_stamp_epoch(text: str) -> Optional[float]:
    """UTC epoch of a lock stamp, or None when it will not parse. A trailing Z is UTC; a naive
    stamp is treated as UTC."""
    raw = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        stamp = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    try:
        return stamp.timestamp()
    except (OverflowError, OSError, ValueError):   # a date the platform cannot convert (Windows)
        return None


def _holder_liveness(pid: int, stamp_epoch: float) -> tuple[str, str]:
    """`(ALIVE|DEAD|UNDETERMINABLE, why)` for the process named by a parsed lock.

    `psutil.Process` rather than `os.kill(pid, 0)`: the latter is not portable to Windows."""
    try:
        holder = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return "DEAD", f"pid {pid} is not running"
    except psutil.Error as exc:
        return "UNDETERMINABLE", f"pid {pid} could not be looked up ({type(exc).__name__}: {exc})"
    try:
        started = holder.create_time()
    except psutil.AccessDenied:   # exists, but a recycled pid cannot be told from the holder
        return "UNDETERMINABLE", f"pid {pid} exists; its start time could not be read (access denied)"
    except psutil.Error as exc:
        return "UNDETERMINABLE", f"pid {pid} start time could not be read ({type(exc).__name__}: {exc})"
    except OSError as exc:
        return "UNDETERMINABLE", f"pid {pid} start time could not be read ({type(exc).__name__}: {exc})"
    if started > stamp_epoch + _LOCK_PID_RECYCLE_SLACK_S:
        return "DEAD", f"pid {pid} started after the lock was written (recycled)"
    return "ALIVE", f"pid {pid} is running"


def _judge_lock(path: Path) -> tuple[str, Optional[int], str]:
    """`(verdict, pid, why)` for the lock file at `path`.

    Verdict is ALIVE, DEAD, UNREADABLE, UNDETERMINABLE, or GONE (the holder finished and removed it
    between the caller's create and this read -- the caller just tries the create again). `pid` is
    set only when the line parsed."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "GONE", None, "the lock was removed"
    except OSError as exc:
        return "UNREADABLE", None, f"cannot read the lock ({type(exc).__name__}: {exc})"
    matched = _LOCK_LINE.fullmatch(text.strip())
    if matched is None:
        return "UNREADABLE", None, "the lock text is not 'pid <pid> at <stamp>'"
    pid = int(matched.group(1))
    if pid <= 0:
        return "UNREADABLE", None, f"pid {pid} is not a live process id"
    stamp_epoch = _lock_stamp_epoch(matched.group(2))
    if stamp_epoch is None:
        return "UNREADABLE", None, f"stamp {matched.group(2)!r} is not a time"
    verdict, why = _holder_liveness(pid, stamp_epoch)
    return verdict, pid, why


def _refuse_unjudged(slug: str, path: Path, why: str) -> LaunchRefused:
    return LaunchRefused(
        f"a launch of {slug} is in progress or left a lock that cannot be judged "
        f"(lock {path}: {why}); refusing rather than assuming it is free or held -- "
        "remove the lock by hand once you know")


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
    not. A live holder's lock is never taken. A DEAD holder's lock is reclaimed, and the reclaim is
    recorded before the file is removed. An unreadable or undeterminable lock is refused and left
    in place: the refusal names the file, and removing it is the operator's call."""

    def __init__(self, slug: str):
        self.path = receipts_dir() / f"LAUNCH-LOCK-{slug.upper()}"
        self.slug = slug

    def _raise_for(self, verdict: str, pid: Optional[int], why: str) -> None:
        if verdict == "ALIVE":
            raise AlreadyLaunched(
                f"a launch of {self.slug} is in progress (lock {self.path}, held by live pid {pid})")
        if verdict in ("UNREADABLE", "UNDETERMINABLE"):
            raise _refuse_unjudged(self.slug, self.path, why)

    def _reclaim_dead(self, pid: int) -> None:
        """Under the reclaim guard, re-judge and take a lock that is still DEAD.

        The journal line is appended BEFORE the unlink: a reclaim with no recorded line must not
        happen. The guard file `<lock>.reclaim` is a filelock (an OS-level lock, released on
        process death); it is left in place -- unlinking a lock file other processes may be waiting
        on would strand them."""
        guard = FileLock(str(self.path) + ".reclaim", timeout=_LOCK_RECLAIM_TIMEOUT_S, thread_local=False)
        try:
            with guard:
                if not self.path.exists():
                    return
                verdict, held, why = _judge_lock(self.path)
                self._raise_for(verdict, held, why)
                if verdict != "DEAD" or held is None:
                    return
                line = json.dumps({
                    "event": "lock-reclaimed", "slug": self.slug, "lock": str(self.path),
                    "dead_pid": held, "at": _stamp()}) + "\n"
                journal = receipts_dir() / f"LAUNCH-RECLAIM-{self.slug.upper()}.jsonl"
                try:
                    with journal.open("a", encoding="utf-8", newline="\n") as sink:
                        sink.write(line)
                except OSError as exc:
                    raise LaunchRefused(
                        f"a launch of {self.slug} found a dead lock ({self.path}) but could not record "
                        f"the reclaim ({type(exc).__name__}: {exc}); refusing rather than taking it "
                        "unrecorded") from exc
                self.path.unlink()
                click.echo(f"[dispatch] reclaimed the launch lock of {self.slug}: holder pid {held} "
                           f"is dead ({self.path})", err=True)
        except FileLockTimeout as exc:
            raise LaunchRefused(
                f"a launch of {self.slug} could not reclaim the lock ({self.path}): the reclaim guard "
                f"was not free within {_LOCK_RECLAIM_TIMEOUT_S}s") from exc

    def __enter__(self) -> "_SlugLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        for _attempt in range(_LOCK_ATTEMPTS):
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                verdict, pid, why = _judge_lock(self.path)
                self._raise_for(verdict, pid, why)
                if verdict == "DEAD" and pid is not None:
                    self._reclaim_dead(pid)
                continue
            with os.fdopen(fd, "w", encoding="utf-8") as sink:
                sink.write(f"pid {os.getpid()} at {_stamp()}\n")
            return self
        raise LaunchRefused(f"the launch lock of {self.slug} keeps changing")

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
            raise AlreadyLaunched(f"{request.slug} is already launched: {holder}. Not launching a second lane.")
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
                "batch": request.batch, "contract": str(request.contract),
                "substrate": "local", "end": None, "end_reason": _LOCAL_END_REASON})
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


def planned_model(argv: Sequence[str]) -> str:
    """The model a planned head argv names -- `--model X`, `--model=X`, `-m X` or `-m=X` -- else ""."""
    for i, tok in enumerate(argv):
        for flag in ("--model", "-m"):
            if tok == flag and i + 1 < len(argv):
                return argv[i + 1]
            if tok.startswith(flag + "="):
                return tok[len(flag) + 1:]
    return ""


#: Why a local launch receipt carries no `end`: the launcher exits when the lane starts.
_LOCAL_END_REASON = "UNMEASURED: the launcher exits when the lane starts; it cannot observe the lane's end"


def _write_launch_records(request: LaunchRequest, result: LaunchResult,
                          extra: Optional[Mapping[str, object]] = None) -> None:
    """The launch receipt (one per slug) and the job-to-lane record (one per job). `extra` adds fields
    to the receipt only -- the `repair` verb passes `kind` and `attempt` (item 2b)."""
    when = _stamp()
    _write_json(_receipt_path(request.slug), {
        "schema": 1, "organ": "launch", "launched_at": when, "exit_code": 0, "batch": request.batch,
        "contract": str(request.contract), "effort": request.effort, "token_cap": request.token_cap,
        "substrate": "local", "end": None, "end_reason": _LOCAL_END_REASON,
        **{k: v for k, v in asdict(result).items()}, **(extra or {})})
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

#: The integrator's own receipt grammar, exactly as `SESSION-integrator-wave5b-n2-2026-09-25.md`
#: writes it throughout, e.g. `STATE lane-launch-queue MERGED bc969abc 22:20 108` and
#: `STATE lane-teardown-visible FAILED - 20:42 -`: five whitespace-separated tokens after the
#: literal `STATE` -- slug, one of the five terminal states, a sha or `-`, a timestamp (ISO or
#: bare `HH:MM`), and a minutes figure or `-`. Any OTHER state word the integrator writes (its
#: transcript also carries `BOUND` and `HANDBACK-SEEN`) is not one `dependency_status` ever reads,
#: so this pattern deliberately matches only the five the Done-contract names.
_STATE_LINE_RE = re.compile(
    r"^STATE\s+(?P<slug>\S+)\s+(?P<state>MERGED|REFUSED|WAITING|FAILED|REPORTED)\s+"
    r"(?P<sha>\S+)\s+(?P<time>\S+)\s+(?P<min>\S+)\s*$", re.MULTILINE)


def parse_state_lines(text: str) -> dict[str, str]:
    """Every `STATE <lane> ...` line in `text`, keyed by slug. A lane's state MOVES over a batch
    (WAITING -> REFUSED -> MERGED as repairs land, `SESSION-integrator-wave5b-n2-2026-09-25.md`
    shows `lane-launch-queue` doing exactly this) and the integrator's receipt is append-only, so
    the LAST line for a slug in the text is its current state -- a plain iteration order, not a
    timestamp parse (the time column mixes ISO and bare `HH:MM` and is not reliably sortable)."""
    out: dict[str, str] = {}
    for match in _STATE_LINE_RE.finditer(text):
        out[match.group("slug")] = match.group("state")
    return out


def read_lane_states(path: Optional[Path]) -> dict[str, str]:
    """The dependency hold's live state, read from the integrator's OWN receipt
    (`to-browser/SESSION-integrator-<batch>.md` or any text carrying its `STATE <lane>
    MERGED|REFUSED|WAITING|FAILED|REPORTED <sha|-> <time> <min>` lines) -- not an invented
    fixture. (N2 lane 9's `{"lanes": {"<slug>": {"state": ...}}}` JSON had no real writer anywhere
    in the harness; ROWS-OWED from that lane's own handback, reconciled here rather than kept.)
    `path=None`, a missing file, or an unreadable read all read as `{}` -- every dependency then
    reads WAITING, never a guessed MERGED (see the section docstring)."""
    if path is None:
        return {}
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    return parse_state_lines(text)


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
ACTION_SKIP_MERGED = "SKIP-MERGED"
ACTION_ALREADY_LAUNCHED = "already-launched"


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
    if states.get(lane.slug) == "MERGED":
        return QueueDecision(lane.slug, ACTION_SKIP_MERGED,
                             "the integrator's receipt reads MERGED -- the lane is done, never refired")
    if lane.slug in set(live_slugs):
        # Before every new-launch gate: a live lane already holds a slot of the cap and the RAM it
        # would be held by, so gating it reports HOLD for a lane that is running ([#1572]).
        return QueueDecision(lane.slug, ACTION_ALREADY_LAUNCHED,
                             "a live lane of this slug is in the agent listing -- not launching a second")
    dep = dependency_status(lane, states)
    if dep == DEP_BLOCKED_FAILED:
        return QueueDecision(lane.slug, ACTION_HELD_FAILED,
                             f"dependency FAILED: {', '.join(lane.starts_after)}")
    if dep == DEP_WAITING:
        unmet = [name for name in lane.starts_after if states.get(name) != "MERGED"]
        return QueueDecision(lane.slug, ACTION_HOLD,
                             f"waiting on {', '.join(unmet)} to read MERGED")
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
    batch: str = ""

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


def _launched_batch(slug: str) -> str:
    """The batch the lane's own LAUNCH receipt recorded, else "": a repair that is not told the batch
    keeps the lane's, so the receipt it rewrites still matches the merge gate's batch check."""
    try:
        return str(json.loads(_receipt_path(slug).read_text(encoding="utf-8")).get("batch") or "")
    except (OSError, ValueError, AttributeError):
        return ""


def repair_worktree_path(repo_root: Path, slug: str) -> Path:
    return Path(repo_root) / ".claude" / "worktrees" / slug


def repair_lane(request: RepairRequest, *, repo_root: Path,
                spawn: Callable[..., "Spawned"] = None,
                environ: Optional[Mapping[str, str]] = None,
                prelaunch: Optional[Callable[..., PreLaunch]] = None) -> "Spawned":
    """Spawn the repair INTO `request.slug`'s existing worktree. Refuses (never spawns) when that
    worktree is not there: starting one is a fresh launch's job, not a repair's.

    A repair is a hub launch too (integrator OWED-ROWS 2, S4): it runs the SAME `pre-launch` moment a
    launch runs -- with `repair=True`, the one rule that the lane's own tree is expected -- and, once the
    provider has started, writes the same `LAUNCH-<SLUG>.json` receipt (with `kind: repair` and the
    attempt) so the merge gate sees it and the model-per-role organ has judged it. A request with no
    batch is refused (`--batch` is required): an unknown batch would read as "not applicable"."""
    spawn = spawn or spawn_process
    prelaunch = prelaunch or run_prelaunch
    if not (request.batch or "").strip():
        raise DispatchRefused(f"the repair of {request.slug} names no batch (--batch, $HARNESS_BATCH and "
                              "the slug's LAUNCH receipt are all absent): `--batch` is required -- a "
                              "repair whose batch is unknown would skip the model-per-role check")
    _refuse_malformed_batch(request.slug, request.batch)
    tree = repair_worktree_path(repo_root, request.slug)
    if not tree.is_dir():
        raise DispatchRefused(f"no existing worktree at {tree} -- a repair reuses the lane's own "
                              "worktree; it does not start one (that is launch_lane's job)")
    launch = LaunchRequest(slug=request.slug, provider="anthropic", model=request.model,
                           effort=request.effort, permission_mode=request.permission_mode,
                           contract=request.contract, batch=request.batch)
    try:
        outcome = prelaunch(launch, repair=True)
    except Exception as exc:  # noqa: BLE001 -- a pre-launch that could not run is a REFUSAL, never a pass
        raise LaunchRefused(f"pre-launch could not run for the repair of {request.slug}: "
                            f"{type(exc).__name__}: {exc}") from exc
    if not outcome.passed:
        raise LaunchRefused(f"pre-launch refused the repair of {request.slug}: {outcome.reason}")
    env = dict(environ if environ is not None else os.environ)
    started = spawn(request.argv, env, tree)
    if started.returncode == 0:
        match = _JOB_ID.search(_ANSI.sub("", started.stdout or ""))
        result = LaunchResult(
            slug=request.slug, provider="anthropic", model_requested=request.model,
            model_reported=MODEL_PENDING, job_id=match.group(1) if match else "unresolved",
            worktree=str(tree), session_name=request.session_name, pid=started.pid,
            argv=list(request.argv))
        try:
            _write_launch_records(launch, result, extra={"kind": "repair", "attempt": request.attempt})
        except OSError as exc:
            raise LaunchIncomplete(f"the repair of {request.slug} WAS started but its launch receipt "
                                   f"could not be written ({exc}). It is running; nothing was stopped."
                                   ) from exc
    return started


# --- a successor is a FIRST-RUN lane whose worktree is cut from a named base, not main's tip ------

def build_successor_plan(model: str, slug: str, effort: str, prompt: str,
                         permission_mode: str = "bypassPermissions") -> Plan:
    """`claude --bg -n <slug> ...` -- NO `--worktree` flag: the successor's `cwd` IS the worktree
    `successor_lane` cut at the base, and `--worktree <slug>` would provision one from main's tip."""
    eff = EFFORTS.get(effort.lower())
    if eff is None:
        raise DispatchRefused(f"unknown effort {effort!r}. Valid: low, medium, high, xhigh, max "
                              "(or l/m/h/x)")
    argv = ["claude", "--bg", "-n", slug, "--model", model, "--effort", eff, "--permission-mode",
            permission_mode, prompt]
    return Plan(argv, "transcript")


@dataclass(frozen=True)
class SuccessorRequest:
    slug: str
    contract: Path
    base: str
    batch: str
    model: str
    effort: str
    permission_mode: str = "bypassPermissions"

    @property
    def _launch(self) -> LaunchRequest:
        return LaunchRequest(slug=self.slug, provider="anthropic", model=self.model, effort=self.effort,
                             permission_mode=self.permission_mode, contract=self.contract,
                             batch=self.batch)

    @property
    def session_name(self) -> str:
        return self.slug

    @property
    def prompt(self) -> str:
        return self._launch.prompt

    @property
    def argv(self) -> list[str]:
        return build_successor_plan(self.model, self.slug, self.effort, self.prompt,
                                    self.permission_mode).argv


def _git_out(repo_root: Path, *args: str) -> "subprocess.CompletedProcess":
    return subprocess.run(["git", "-C", str(repo_root), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def successor_lane(request: SuccessorRequest, *, repo_root: Path,
                   spawn: Callable[..., "Spawned"] = None,
                   environ: Optional[Mapping[str, str]] = None,
                   prelaunch: Optional[Callable[..., PreLaunch]] = None) -> "Spawned":
    """Cut `<repo>/.claude/worktrees/<slug>` on `worktree-<slug>` at the resolved BASE and spawn a
    first-run lane into it. Pre-launch runs BEFORE the worktree exists (`repair=False`); an existing
    worktree at the same base is reused (`repair=True`, its own tree is expected), at any other commit
    it is refused. A refused or failed launch removes whatever THIS call created."""
    spawn = spawn or spawn_process
    prelaunch = prelaunch or run_prelaunch
    if not (request.batch or "").strip():
        raise DispatchRefused(f"the successor {request.slug} names no batch: `--batch` is required -- an "
                              "unknown batch would skip the model-per-role check")
    _refuse_malformed_batch(request.slug, request.batch)
    if not Path(request.contract).is_file():
        raise DispatchRefused(f"no contract file at {request.contract}")
    resolved = _git_out(repo_root, "rev-parse", "--verify", f"{request.base}^{{commit}}")
    sha = resolved.stdout.strip()
    if resolved.returncode != 0 or not sha:
        raise DispatchRefused(f"base {request.base!r} does not resolve to a commit in {repo_root}: "
                              f"{_tail(resolved.stderr, 300)}")
    argv = request.argv
    tree = repair_worktree_path(repo_root, request.slug)
    branch = f"worktree-{request.slug}"
    launch = request._launch

    with _SlugLock(request.slug):
        existed = tree.exists()
        if not existed:
            if _git_out(repo_root, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}").returncode == 0:
                raise DispatchRefused(f"the branch {branch} already exists and the worktree of "
                                      f"{request.slug} does not: refusing to reuse or delete a branch "
                                      "this call did not create")
        else:
            top = _git_out(tree, "rev-parse", "--show-toplevel")
            on_branch = _git_out(tree, "symbolic-ref", "--short", "HEAD")
            try:
                is_tree = top.returncode == 0 and Path(top.stdout.strip()).resolve() == tree.resolve()
            except OSError:
                is_tree = False
            if not is_tree or on_branch.returncode != 0 or on_branch.stdout.strip() != branch:
                raise DispatchRefused(f"{tree} is not a worktree of {repo_root} on branch {branch}: "
                                      "refusing to reuse it for the successor")
            head = _git_out(tree, "rev-parse", "HEAD").stdout.strip()
            if head != sha:
                raise DispatchRefused(f"the worktree of {request.slug} is at {head}, not the base {sha}: "
                                      "refusing to reuse it for a successor of another commit")
        try:
            outcome = prelaunch(launch, repair=existed)
        except Exception as exc:  # noqa: BLE001 -- a pre-launch that could not run is a REFUSAL, never a pass
            raise LaunchRefused(f"pre-launch could not run for the successor {request.slug}: "
                                f"{type(exc).__name__}: {exc}") from exc
        if not outcome.passed:
            raise LaunchRefused(f"pre-launch refused the successor {request.slug}: {outcome.reason}")

        created = False

        def undo() -> None:
            if created:
                _git_out(repo_root, "worktree", "remove", "--force", str(tree))
                _git_out(repo_root, "branch", "-D", branch)

        if not existed:
            added = _git_out(repo_root, "worktree", "add", "-b", branch, str(tree), sha)
            if added.returncode != 0:
                raise DispatchRefused(f"could not create the worktree of {request.slug} at {sha}: "
                                      f"{_tail(added.stderr, 300)}")
            created = True
        try:
            env = dict(environ if environ is not None else os.environ)
            started = spawn(argv, env, tree)
        except Exception:
            undo()
            raise
        if started.returncode != 0:
            undo()
            raise LaunchRefused(f"the successor {request.slug} failed to start (exit {started.returncode}): "
                                f"{_tail(started.stdout, 300)} -- no lane was started")
    match = _JOB_ID.search(_ANSI.sub("", started.stdout or ""))
    result = LaunchResult(
        slug=request.slug, provider="anthropic", model_requested=request.model,
        model_reported=MODEL_PENDING, job_id=match.group(1) if match else "unresolved",
        worktree=str(tree), session_name=request.session_name, pid=started.pid,
        argv=list(request.argv))
    try:
        _write_launch_records(launch, result, extra={"kind": "successor", "base": sha})
    except OSError as exc:
        raise LaunchIncomplete(f"the successor {request.slug} WAS started but its launch receipt "
                               f"could not be written ({exc}). It is running; nothing was stopped."
                               ) from exc
    return started


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
    skipped_merged: tuple[str, ...] = ()
    already_launched: tuple[str, ...] = ()

    @property
    def terminal(self) -> frozenset[str]:
        """Every slug this watcher is done waiting on, for any of the five reasons ([#1572] added
        `skipped_merged` and `already_launched` -- neither is a launch, so neither joins `fired`)."""
        return (frozenset(self.fired) | frozenset(self.held_failed) | frozenset(self.routed_codespace)
                | frozenset(self.skipped_merged) | frozenset(self.already_launched))


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
    """Poll `plan_pass` until every lane is `FIRE`d or terminal (`HELD-FAILED`/`ROUTE-CODESPACE`/
    `SKIP-MERGED`/already launched), OR `deadline_s` elapses -- whichever comes first, NEVER longer (each sleep is CLAMPED to what
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
    merged: set[str] = set()
    already: set[str] = set()
    polls = 0

    def _result(expired: bool) -> WatchResult:
        return WatchResult(polls, expired, tuple(fired), tuple(held_failed), tuple(routed),
                           tuple(merged), tuple(already))

    while True:
        polls += 1
        resolved = fired | held_failed | routed | merged | already
        decisions = plan_pass(lanes, order, fired=resolved, states=states_fn(),
                              live_slugs=live_slugs_fn(), local_cap=local_cap,
                              local_live_count=local_live_count_fn(), free_mb=free_mb_fn(),
                              floor_mb=floor_mb)
        for decision in decisions:
            if decision.action == ACTION_FIRE:
                try:
                    if on_fire is not None:
                        on_fire(decision.slug)
                except AlreadyLaunched:
                    already.add(decision.slug)   # launched earlier: reported, not fired, never a halt
                else:
                    fired.add(decision.slug)
            elif decision.action == ACTION_HELD_FAILED:
                held_failed.add(decision.slug)
            elif decision.action == ACTION_ROUTE_CODESPACE:
                routed.add(decision.slug)
            elif decision.action == ACTION_SKIP_MERGED:
                merged.add(decision.slug)
            elif decision.action == ACTION_ALREADY_LAUNCHED:
                already.add(decision.slug)
        resolved = fired | held_failed | routed | merged | already
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
    successor SLUG CONTRACT   a fresh lane whose worktree is cut from --base (a ref or
                       sha), not main's tip; first-run prompt, `kind: successor` receipt.

    Run `dispatch.py <verb> --help` for a verb's options. The contract's Dispatch
    block is read for its fields (head, -n, --worktree, --model, --effort), never run."""


@cli.command("launch")
@click.argument("contract")
@click.option("--slug", default="", help="Lane slug; default: the Dispatch block's -n / --worktree, "
                                         "else LANE-<slug>.md from the file name. Refused if it "
                                         "disagrees with the block.")
@click.option("--provider", default="", help="Overrides the Dispatch block's head "
                                             "(claude -> anthropic, codex -> codex).")
@click.option("--model", default="", help="Overrides the contract's model. No default.")
@click.option("--effort", default="", help="Overrides the contract's effort. No default.")
@click.option("--batch", default="", help="The batch the lane joins; pre-launch checks its integrator "
                                          "is live. The model-per-role gate applies to ids of the form "
                                          "`E<major>.<minor>` from E2.0 on. Default: $HARNESS_BATCH.")
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
    _refuse_malformed_batch(slug or Path(contract).stem, batch or os.environ.get("HARNESS_BATCH", ""))
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


def _plan_dispatch_line(path: Path) -> Optional[DispatchLine]:
    """The Dispatch block, read for its slug only. `plan` takes its head from `--provider`, never
    the block, so a block `launch` would refuse is not a `plan` error -- but its `-n`/`--worktree`
    still binds: a conflicting `--slug` is refused whatever else on the line is invalid."""
    return dispatch_block_slug_line(path.read_text(encoding="utf-8", errors="replace"))


@cli.command("plan")
@click.argument("contract")
@click.option("--slug", default="", help="Lane slug; default: the Dispatch block's -n / --worktree, "
                                         "else LANE-<slug>.md from the file name. Refused if it "
                                         "disagrees with the block.")
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
    slug = contract_slug(path, _plan_dispatch_line(path), slug)
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
                   machine: str = "standardLinux32gb", idle_timeout: str = "240m",
                   retention: str = "24h", workdir: str = "/workspaces/dispatch",
                   batch: str = "") -> list[Step]:
    """Ported from Start-DispatchCodespace. `{cs}` is the codespace NAME, printed to stdout by
    `create` itself -- measured, `[CLI-SRC]`: `gh codespace create` writes `codespace.Name` via
    `fmt.Fprintln` (`DIGEST-2026-09-15-codespaces-reference.md:182-183`) -- never reconstructed
    from `gh codespace list`, whose display-name match is not unique across a stale codespace
    from a prior run of this same slug (codex terra P1, 2026-09-27). The prompt and the command
    travel as FILES; the only thing crossing the ssh boundary is `bash <path>`.

    The trailing steps are R17 (`to-browser/PROPOSAL-ADR-REMOTE-LANE-OBSERVABILITY-2026-09-26.md`
    D2): harvest before delete, and the manifest check is shown in the PLAN -- not only enforced
    silently inside `codespace_delete` -- so a dry run names the gate before anything runs."""
    runner = f"{workdir}/run-{slug}.sh"
    out_dir = _harvest_dir(batch or "<batch>", slug)
    steps = [
        Step(["gh", "codespace", "create", "-R", repo, "-b", branch, "--machine", machine,
              "--idle-timeout", idle_timeout, "--retention-period", retention, "-d", slug],
             "create -- its own stdout is the NAME, `{cs}` below"),
        Step(["gh", "codespace", "ssh", "-c", "{cs}", "--", *_remote("cat", cs.CREATION_LOG_PATH)],
             "creation log: read over ssh and classified -- a recovery container is REFUSED "
             "before anything ships or runs (night leg 5, D3)"),
        Step(["gh", "codespace", "ssh", "-c", "{cs}", "--", *_remote("mkdir", "-p", workdir)],
             "create the workdir -- NOT the checkout's own directory"),
        Step(["gh", "codespace", "cp", "-c", "{cs}", "-e", str(contract),
              f"remote:{workdir}/{Path(contract).name}"], "ship the contract in"),
        Step(["gh", "codespace", "cp", "-c", "{cs}", "-e", "{runner}", f"remote:{runner}"],
             "ship the runner in"),
        Step(["gh", "codespace", "ssh", "-c", "{cs}", "--", *_remote("bash", "-l", runner)],
             "run (stream-metered) in a LOGIN shell -- a non-login ssh shell sees none of the "
             "Codespaces secrets (night leg 5, D1); cwd is the checkout `create` produced, "
             "not `workdir`"),
        Step(["gh", "codespace", "cp", "-c", "{cs}", "-e", f"remote:{workdir}/receipt.json",
              "{receipt}"], "pull the receipt back"),
    ]
    for rel in HARVEST_FILES:
        steps.append(Step(["gh", "codespace", "ssh", "-c", "{cs}", "--", *_remote("cat", f"{workdir}/{rel}")],
                           f"harvest: {rel} (R17/D2, ssh|cat -- measured, not `cp`)"))
    steps.append(Step(["<local>", "verify_harvest_manifest", str(out_dir)],
                       "manifest check (local, no gh call) -- GATES the delete step below"))
    steps.append(Step(["gh", "codespace", "delete", "-c", "{cs}", "--force"],
                       "delete -- REFUSED above if the manifest check failed (R17)"))
    return steps


# ===================================================== codespace exec / harvest / delete (R17)
#
# `codespace_plan` above only ever PRINTS the argv it would run (`dispatch.py plan`'s own
# contract: "Starts nothing"). Everything below actually calls `gh`, ported from the PS module's
# `Invoke-CodespaceGh` seam and the create/exec half of `Start-DispatchCodespace`, plus the two
# legs the PS module already had as separate verbs (`Save-CodespaceLaneHarvest`,
# `Stop-DispatchCodespace`) and one it deliberately never had: `codespace_delete`.
#
# WHY DELETE IS NEW HERE AND ABSENT THERE. `Stop-DispatchCodespace`'s own docstring: "This module
# composes no `gh codespace delete` anywhere... deletion is destructive and stays an operator
# act." R17 (D2) changes what "operator act" means for THIS one call: a manifest-gated delete
# that refuses without a verified private copy in hand is no longer a bare irreversible act, it is
# an act with a checked precondition -- the same shape `block-unanchored-push` already uses for a
# different irreversible act (a push). `codespace_delete` is that gated call, never the bare one.
#
# HONEST LIMIT (recorded so it is not mistaken for oversight). The PS runner's own receipt carries
# a much larger shape than what is ported here: per-tool `admission` probes taken INSIDE the
# container, a `commit` witness, `stall`/fuse diagnostics, and a `restart-once` recovery policy
# (`Start-DispatchCodespace:980-1052`). That machinery is a separate, larger surface (stall
# detection, admission-probe porting) and is out of this lane's scope; what is ported is the
# subset a delete-gate or merge-gate reads today: `exit_code`, `is_error`, `status`, `turns`,
# `transcript`, plus a stub `admission`/`recovery` so the KEYS are the same shape even where the
# VALUES are not yet as rich. A receipt this module writes is not read as a stall diagnosis.


# A generous bound, not a tuning knob: `codespace create` provisions a machine and `codespace
# ssh -- bash <runner>` runs a whole lane, both legitimately slow -- this exists only to convert
# a genuinely STUCK `gh` (an interactive auth prompt with no TTY to answer it, a hung network
# call) into the documented refusal path instead of an indefinite block (codex terra P1,
# 2026-09-27).
GH_TIMEOUT_SECONDS = 900


@dataclass(frozen=True)
class GhResult:
    """One `gh` invocation's outcome -- `Ok`/`ExitCode`/`Stdout` from `Invoke-CodespaceGh`, with
    `stderr` kept SEPARATE, never folded into `stdout` (codex terra P1, 2026-09-27: a successful
    `create` that also writes progress/warnings to stderr would otherwise corrupt the one-line
    NAME every later `-c` call keys on, and a harvested `cat` would hash diagnostics as if they
    were the file's own content)."""

    ok: bool
    exit_code: int
    stdout: str
    stderr: str = ""


def format_gh_line(argv: Sequence[str]) -> str:
    """Display-only rendering of a `gh` argv -- ported from `Format-CodespaceGhLine`. What
    executes is the argument LIST, never this string; nothing re-parses it."""
    parts = []
    for a in argv:
        parts.append('"' + a.replace('"', '""') + '"' if re.search(r'[\s"]', a) else a)
    return "gh " + " ".join(parts)


def run_gh(argv: Sequence[str], *, invoker: Optional[Callable[..., GhResult]] = None,
           timeout: float = GH_TIMEOUT_SECONDS, input_bytes: Optional[bytes] = None) -> GhResult:
    """The single seam every `gh` call in the codespace legs goes through -- ported from
    `Invoke-CodespaceGh`. Returns ok/exit_code/stdout rather than raising: a non-zero `gh` exit is
    data this domain reasons about (unauthenticated, no such codespace, quota), never an
    exception. `invoker` is the test seam -- every test below hands in a recording stand-in and
    asserts the ARGV that would have run, exactly as the PS tests do for `Invoke-CodespaceGh`.

    `input_bytes` is the one way bytes reach a remote command without being an argument: they go on
    the command's STDIN, so a credential never appears in an argv, a log line or a process listing
    (b2-codespace-subscription-auth, R13). The seam receives them only when there are some."""
    if invoker is not None:
        return invoker(argv) if input_bytes is None else invoker(argv, input_bytes)
    if input_bytes is not None:  # pragma: no cover -- real gh
        try:
            raw = subprocess.run(["gh", *argv], capture_output=True, input=input_bytes, timeout=timeout)
        except OSError as exc:
            return GhResult(ok=False, exit_code=127, stdout=f"gh could not be run: {exc}")
        except subprocess.TimeoutExpired:
            return GhResult(ok=False, exit_code=124, stdout=f"gh timed out after {timeout}s")
        return GhResult(ok=(raw.returncode == 0), exit_code=raw.returncode,
                        stdout=(raw.stdout or b"").decode("utf-8", "replace"),
                        stderr=(raw.stderr or b"").decode("utf-8", "replace"))
    # `timeout` is per call: an observer's read is bounded in seconds, a whole lane's run step in
    # hours, and neither is the 900 s default. stdin is closed so a `gh` prompt can only fail,
    # never wait on a pipe nobody writes to.
    try:  # pragma: no cover -- real gh
        proc = subprocess.run(["gh", *argv], capture_output=True, text=True,
                              timeout=timeout, stdin=subprocess.DEVNULL)
    except OSError as exc:
        # `gh` missing (or unrunnable) is DATA this domain reasons about, same as a non-zero
        # exit -- a codex terra HIGH (2026-09-27): an uncaught FileNotFoundError crashed every
        # codespace command with a traceback instead of its own documented refusal path.
        return GhResult(ok=False, exit_code=127, stdout=f"gh could not be run: {exc}")
    except subprocess.TimeoutExpired as exc:
        # Codex terra P1 (2026-09-27): a stalled `gh` (an auth prompt, a hung network request)
        # blocked every codespace command indefinitely -- no HONEST-LIMIT stall/fuse diagnostics
        # are ported here (this module's own docstring), so a bound is the only thing standing
        # between a stuck `gh` and a caller that never gets its documented refusal.
        return GhResult(ok=False, exit_code=124,
                        stdout=f"gh timed out after {timeout}s: {exc}")
    return GhResult(ok=(proc.returncode == 0), exit_code=proc.returncode,
                     stdout=proc.stdout or "", stderr=proc.stderr or "")


# ----- exec: create, ship, run, pull the receipt back -----------------------------------------

@dataclass(frozen=True)
class ExecResult:
    ok: bool
    name: str = ""
    receipt: dict = field(default_factory=dict)
    commands: tuple[str, ...] = ()
    failure: str = ""
    #: A failed lane's fate (R65): `{"fate": "FAILED", "step": ..., "reason": ...}`. Empty on success.
    fate: dict = field(default_factory=dict)
    #: The credential mirror's record, one dict per CLI: names, paths, modes and booleans -- never a
    #: value (R13). Empty when the launch ran without a mirror.
    mirror: tuple = ()
    #: The finish witnesses: one `codespace-step` row per step that ran (empty without a `batch`).
    steps: tuple = ()

#: The Codespaces secrets a lane needs, probed as BOOLEANS by the runner (R13: a value never
#: enters a file or a log). `claude -p` needs the first, `gh` and `git push` the second, the two
#: review heads the next two, and the transport read/write the last.
RUNNER_SECRETS: tuple[str, ...] = ("CLAUDE_CODE_OAUTH_TOKEN", "GITHUB_TOKEN",
                                   "XAI_API_KEY", "RCLONE_CONFIG_GDRIVE_TOKEN",
                                   # R88a: Copilot signs in through this token, not a keyring login
                                   "COPILOT_GITHUB_TOKEN",
                                   # R87 fallback: a SEPARATE ChatGPT login's auth.json, written to
                                   # ~/.codex/auth.json only when the mirror put nothing there
                                   "CODEX_AUTH_JSON")

#: The API keys NO codex invocation may see (R87.3, b2w2-codespace-finish). The runner records each one's
#: presence as a boolean (`present-before-unset`) and removes it from the environment on EVERY launch,
#: mirror configured or not: OpenAI does not document a key's precedence over a ChatGPT sign-in, so the
#: lane does not leave it to precedence. They are no lane secret, so they are not in `RUNNER_SECRETS`.
RUNNER_NEVER_SET: tuple[str, ...] = ("CODEX_API_KEY", "OPENAI_API_KEY")

#: The runner's own bounds, from the classifier's: a head whose run log is quiet for longer than
#: this is killed and its receipt says why.
RUNNER_STALL_AFTER_S = int(cs.STALE_AFTER_S)

#: The runner's own copy of the agent's structured output. `handback.json` belongs to the lane
#: itself, which writes it in the checkout's workdir; the runner must never overwrite it.
RUNNER_HANDBACK_FILE = "runner-handback.json"

#: How long, in total sleep, the creation log is re-read while INDETERMINATE (a prebuild-less
#: container build runs for minutes; the ssh read works only once the box is up and the log's last
#: line lands later still). Past the bound the box is refused.
CREATION_LOG_WAIT_BOUND_S = 900
CREATION_LOG_WAIT_S = 20
CREATION_LOG_ATTEMPTS = CREATION_LOG_WAIT_BOUND_S // CREATION_LOG_WAIT_S + 1


def _remote(*words: str) -> list[str]:
    """The argv tail after `--` for `gh codespace ssh`: the remote command as ONE element. ssh
    re-joins separate elements with spaces, so a path with a space would split on the box."""
    return [shlex.join(words)]

#: The run step's own bound, in seconds: the codespace's idle timeout (240 m) less a margin. A lane
#: is long, and the stall watchdog in the runner (not this number) is what ends a quiet one.
RUN_TIMEOUT_SECONDS = 3 * 3600

#: What bounds the life of a mirrored credential copy in the box, besides the run: the time to create
#: the box and ship the copy in. A declared bound, not a measurement -- create plus ship is minutes.
MIRROR_LEAD_S = 3600

#: How long a mirrored copy can live: the runner removes it on exit (EXIT trap), so the run's own
#: bound plus the lead is the longest it can exist.
COPY_LIFETIME_S = RUN_TIMEOUT_SECONDS + MIRROR_LEAD_S


def codex_mirror_max_age_days() -> float:
    """The oldest codex cache the launch may copy: the age at which codex refreshes on its next call
    (`CODEX_REFRESH_DAYS`) less the copy's whole lifetime, so the copy is gone before it could reach
    that refresh. Derived, never typed."""
    return cpar.CODEX_REFRESH_DAYS - COPY_LIFETIME_S / 86400.0


# ----- the credential mirror (b2-codespace-subscription-auth, R87) ----------------------------------
#
# DECIDED-BY-LANE (channel): a cache file travels as the STDIN of `gh codespace ssh -- bash -l
# credential-tools.sh install <relpath>`, not through `gh codespace cp`. `cp` needs a local file
# path the bytes would have to be staged under (a second copy of a credential on this disk) and its
# failures have been measured three ways on this transport (`codespace_plan`'s docstring); stdin
# puts the bytes in no argv, no temp file and no listing. The remote script is a constant shipped
# by `cp` (it holds no secret), takes ONLY a path from the declared allow-list, writes umask 077,
# `chmod 700` on the directory and `600` on the file, and prints the mode -- never a byte.
#
# DECIDED-BY-LANE (what is mirrored): measured on the laptop 2026-10-06, per CLI, in
# `codespace_parity.SIGN_IN` (route, files, refresh verdict, why). A CLI whose sign-in is an OS keyring
# entry and has no token route (agy) has no file to copy and ends WAITING with its renew step -- never
# a workaround. Copilot signs in through its COPILOT_GITHUB_TOKEN secret (R88a). An env API key is used
# in the Codespace only where the laptop itself uses one (grok).

#: Where the shipped helper lives in the box, and how long its calls may run.
CREDENTIAL_TOOLS_NAME = "credential-tools.sh"
CREDENTIAL_CALL_TIMEOUT_S = 300

_SEMVER_STRICT = re.compile(r"^\d+\.\d+\.\d+$")

#: What a status call says when the sign-in is dead -- classified from OUTPUT TEXT only (a refresh
#: that failed, a token already used, a login that is gone). Exit status alone is read too: a
#: mirrored credential that the CLI cannot use is expired for the lane's purposes.
_CREDENTIAL_DEAD = re.compile(
    r"expired|could not be refreshed|refresh token (?:was )?(?:already )?(?:used|reused|invalid|revoked)"
    r"|refresh_token_reused|invalid_grant|log ?in again|logged out|not logged in|please (?:run )?log ?in"
    r"|\b401\b|unauthori[sz]ed", re.IGNORECASE)


@dataclass(frozen=True)
class MirrorConfig:
    """What the launch-time mirror reads: the laptop's HOME and environment (booleans are taken from
    it, never values -- the bytes of a cache file are read only to be shipped), the provider registry
    that names the CLIs, and the clock. `local_versions` is the laptop's `claude --version`; None
    means "read it now". `verdicts` overrides a CLI's recorded refresh verdict (`SIGN_IN.refresh`)."""

    home: Path
    env: Mapping[str, str]
    registry: Mapping
    now: Optional[datetime] = None
    local_versions: Optional[Mapping[str, str]] = None
    verdicts: Mapping[str, str] = field(default_factory=dict)
    #: Refreshes the laptop's codex cache with ONE keyless call; True when the call ran. None means
    #: the default (`_refresh_codex_on_laptop`). A test seam: no real codex is ever run by a test.
    refresh_codex: Optional[Callable[[], bool]] = None


@dataclass(frozen=True)
class MirrorItem:
    """One CLI's launch decision. `action`: mirrored | not-mirrored | gap | fallback | absent |
    refused | no-cli | undeclared. `files` are paths relative to HOME that WILL be copied. `gap` is
    the stable id of a sign-in only an operator can finish (agy)."""

    cli: str
    route: str = ""
    action: str = ""
    files: tuple[str, ...] = ()
    detail: str = ""
    operator_action: str = ""
    gap: str = ""


def default_mirror_config(env: Optional[Mapping[str, str]] = None) -> MirrorConfig:
    """The launcher's own: this laptop's HOME and environment and the repository's registry."""
    return MirrorConfig(home=Path.home(), env=dict(os.environ if env is None else env),
                        registry=cpar.load_registry())


AGY_GAP_ID = "agy-interactive-sign-in"
AGY_SIGNIN_WAIT_S = 600
AGY_HEARTBEAT_S = 60
AGY_POLL_S = 2
AGY_READ_FALLBACK = "copilot"


def _refresh_codex_on_laptop() -> bool:
    """ONE laptop-side codex call, made so codex refreshes its own cache (it does so from
    `CODEX_REFRESH_DAYS`). Run with neither API key (R87.3). True when the call exited 0."""
    argv = cpar.keyless_command("codex", ["codex", "exec", "--skip-git-repo-check", "-s", "read-only", "ok"])
    res = cpar.default_run(argv, timeout=CREDENTIAL_CALL_TIMEOUT_S, env=cpar.probe_env("codex"))
    return res.returncode == 0


def _codex_last_refresh(home: Path, rel: str) -> Optional[datetime]:
    try:
        return cpar._iso(json.loads((home / rel).read_text(encoding="utf-8")).get("last_refresh"))
    except (OSError, json.JSONDecodeError, AttributeError):
        return None


def _decide_guarded_codex(cfg: MirrorConfig, cli: str, spec, present: tuple[str, ...], now: datetime,
                          refresh: str) -> MirrorItem:
    """The mirror decision for a `guarded` cache (codex): mirrored while its age leaves room for the
    copy's whole life before codex's own refresh; `due` (8 days or older) is refreshed by the launcher
    with one keyless laptop call and judged again; the band between is refused with the instant it
    reopens, because no call can refresh a cache that young."""
    ceiling = codex_mirror_max_age_days()
    state = cpar.credential_expiry(cli, cfg.home, now=now)
    note = ""
    if state["state"] == "due":
        refresher = cfg.refresh_codex or _refresh_codex_on_laptop
        refresher()
        state = cpar.credential_expiry(cli, cfg.home, now=now)
        note = "; refreshed by the launcher"
    if state["state"] == "expired":
        return MirrorItem(cli, "mirror", "refused", files=present,
                          detail=f"the laptop's {cli} sign-in has expired: {state['detail']}",
                          operator_action=f"OPERATOR-ACTION: {state['renew']}")
    if state["state"] == "due":
        return MirrorItem(cli, "mirror", "refused", files=present,
                          detail=f"the laptop's {cli} cache is {state.get('age_days', '?')} days old and the "
                                 "launcher's own refresh call did not refresh it",
                          operator_action=f"OPERATOR-ACTION: {state['renew']}, then relaunch")
    age = float(state.get("age_days", 0.0))
    if age >= ceiling:
        refreshed = _codex_last_refresh(cfg.home, present[0])
        reopens = (refreshed + timedelta(days=cpar.CODEX_REFRESH_DAYS)) if refreshed else None
        when = reopens.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%MZ") if reopens else "its 8th day"
        return MirrorItem(cli, "mirror", "refused", files=present,
                          detail=f"the laptop's {cli} cache is {age:g} days old, past the {ceiling:.2f}-day "
                                 "window: a copy could reach codex's own refresh while the laptop may "
                                 "refresh it too",
                          operator_action=f"OPERATOR-ACTION: relaunch after {when}, when the launcher "
                                          f"refreshes the laptop's {cli} cache by itself (or {state['renew']})")
    return MirrorItem(cli, "mirror", "mirrored", files=present,
                      detail=f"{state['detail']}{note}; refresh verdict {refresh!r}")


def credential_decisions(cfg: MirrorConfig) -> list[MirrorItem]:
    """Decide, per registry provider and per declared non-model tool, what the launch does with its
    sign-in -- from the laptop's own files and the recorded refresh verdicts, offline, before any box
    exists. A `refused` item carries the ONE `OPERATOR-ACTION` line that renews it (R59, R65)."""
    now = cfg.now or datetime.now(timezone.utc)
    items: list[MirrorItem] = []
    for provider in cpar.providers_without_cli(cfg.registry):
        items.append(MirrorItem(provider, "none", "no-cli",
                                detail="the registry names no CLI for this provider: nothing to mirror"))
    for cli in cpar.lane_tools(cfg.registry):
        spec = cpar.SIGN_IN.get(cli)
        if spec is None:
            items.append(MirrorItem(cli, "none", "undeclared",
                                    detail=f"no sign-in is declared for {cli} in codespace_parity.SIGN_IN"))
            continue
        refresh = str(cfg.verdicts.get(cli, spec.refresh))
        if spec.route in ("secret-token", "env-key"):
            items.append(MirrorItem(cli, spec.route, "not-mirrored", detail=spec.why))
        elif spec.route == "waiting":
            # no non-interactive subscription sign-in exists (G1): a recorded GAP, never a refusal --
            # the launch goes on and the sign-in URL is surfaced to the operator on stderr
            items.append(MirrorItem(cli, "waiting", "gap", detail=spec.why, gap=AGY_GAP_ID,
                                    operator_action=f"OPERATOR-ACTION: {spec.renew}"))
        elif spec.route == "mirror":
            present = tuple(rel for rel in spec.files if (cfg.home / rel).is_file())
            if not present or present[0] != spec.files[0]:
                items.append(MirrorItem(cli, "mirror", "absent",
                                        detail=f"the laptop has no {spec.files[0]} to copy",
                                        operator_action=f"OPERATOR-ACTION: {spec.renew}"))
            elif refresh in ("rotates", "unknown"):
                items.append(MirrorItem(
                    cli, "secret-fallback", "fallback",
                    detail=f"refresh verdict {refresh!r}: a copy could sign the other side out, so the "
                           f"cache is not copied. {spec.why}",
                    operator_action="OPERATOR-ACTION: " + (spec.fallback or f"no fallback is declared for {cli}")))
            elif cli == "codex" and refresh == "guarded":
                items.append(_decide_guarded_codex(cfg, cli, spec, present, now, refresh))
            else:
                state = cpar.credential_expiry(cli, cfg.home, now=now)
                if state["state"] == "expired":
                    items.append(MirrorItem(
                        cli, "mirror", "refused", files=present,
                        detail=f"the laptop's {cli} sign-in has expired: {state['detail']}",
                        operator_action=f"OPERATOR-ACTION: {state['renew']}"))
                elif state["state"] == "due":
                    items.append(MirrorItem(
                        cli, "mirror", "refused", files=present,
                        detail=f"the laptop's {cli} cache is {state.get('age_days', '?')} days old: a copy "
                               "would reach its refresh while the laptop may refresh it too",
                        operator_action=f"OPERATOR-ACTION: {state['renew']}, then relaunch"))
                else:
                    items.append(MirrorItem(cli, "mirror", "mirrored", files=present,
                                            detail=f"{state['detail']}; refresh verdict {refresh!r}"))
        else:
            items.append(MirrorItem(cli, spec.route, "undeclared", detail=f"unknown route {spec.route!r}"))
    return items


def leak_check(credentials: Mapping[str, bytes], artefacts: Iterable[str]) -> list[str]:
    """The NAMES of the credentials whose bytes reached any artefact (R13): the whole file's sha-256,
    any of its string values of twelve characters or more, or the file itself. Compared in memory;
    neither the credential nor the artefact is ever returned, printed or logged."""
    texts = [a for a in artefacts if a]
    hits: list[str] = []
    for name, blob in sorted(credentials.items()):
        needles = {hashlib.sha256(blob).hexdigest()}
        text = blob.decode("utf-8", "replace")
        if len(text) >= 12:
            needles.add(text)
        try:
            tree = json.loads(text)
        except json.JSONDecodeError:
            tree = None

        def leaves(node):
            if isinstance(node, str):
                yield node
            elif isinstance(node, Mapping):
                for v in node.values():
                    yield from leaves(v)
            elif isinstance(node, (list, tuple)):
                for v in node:
                    yield from leaves(v)

        needles.update(v for v in leaves(tree) if len(v) >= 12)
        if any(n in t for n in needles for t in texts):
            hits.append(name)
    return hits


def _credential_tools_script(allowed: Sequence[str]) -> str:
    """The helper shipped into the box: `install <relpath>` (stdin -> HOME/<relpath>, mode 600, the
    path from the allow-list only), `status <cli>`, `claude-version`, `claude-install <x.y.z>`. It
    prints modes, versions and each CLI's own status text -- never a credential."""
    paths = "|".join(shlex.quote(p) for p in allowed) or "__none__"
    return "\n".join([
        "#!/usr/bin/env bash",
        "# shipped by dispatch.py (b2-codespace-subscription-auth): holds no secret, prints no secret",
        "set -u",
        'sub="${1:-}"',
        'case "$sub" in',
        "  install)",
        '    rel="${2:-}"',
        '    case "$rel" in',
        f"      {paths}) ;;",
        '      *) echo "refused: not a declared sign-in cache path" >&2; exit 64 ;;',
        "    esac",
        "    umask 077",
        '    dest="$HOME/$rel"; dir="$(dirname "$dest")"',
        '    mkdir -p "$dir" && chmod 700 "$dir" || exit 65',
        '    tmp="$dest.tmp.$$"',
        '    cat > "$tmp" || { rm -f "$tmp"; exit 66; }',
        '    chmod 600 "$tmp" && mv -f "$tmp" "$dest" || exit 67',
        '    echo "mode $(stat -c %a "$dest")"',
        "    ;;",
        "  status)",
        '    case "${2:-}" in',
        "      codex) env -u CODEX_API_KEY -u OPENAI_API_KEY codex login status 2>&1 ;;",
        "      claude) claude auth status 2>&1 ;;",
        "      gh) gh auth status 2>&1 ;;",
        '      *) echo "no status command" >&2; exit 64 ;;',
        "    esac",
        "    ;;",
        "  claude-version) claude --version 2>&1 ;;",
        "  agy-signin-start)",
        # agy holds its sign-in only in an OS keyring (G1): start it in a sized pty that outlives this
        # ssh call, BROWSER unset, its stdin a FIFO; the setsid leader's pid and the FIFO holder's pid
        # are kept so `agy-signin-stop` can kill the whole tree; print ONLY the authorization URL line
        '    box="$HOME/.agy-signin"; umask 077',
        '    mkdir -p "$box" && chmod 700 "$box" || exit 65',
        '    rm -f "$box/in" "$box/out" "$box/pid" "$box/holder"; mkfifo "$box/in" || exit 65',
        # own stdin/stderr: a captured caller never sees EOF while the holder inherits its pipes
        '    sleep 900 < /dev/null > "$box/in" 2>/dev/null &',
        '    echo $! > "$box/holder"',
        '    nohup setsid script -qfec "stty cols 500 rows 50; exec env -u BROWSER timeout 900 agy" '
        '"$box/out" < "$box/in" > /dev/null 2>&1 &',
        '    echo $! > "$box/pid"',
        # live finding (agy 1.3.5): agy draws a login menu before any URL and waits for a key; option 1
        # (Google OAuth) is the highlighted default, so ONE Enter answers it -- never anything else
        "    sent=0",
        "    for _ in $(seq 1 90); do",
        '      if [ "$sent" = 0 ] && sed -e \'s/\\x1b\\[[0-9;?]*[a-zA-Z]//g\' "$box/out" 2>/dev/null '
        "| grep -aq 'Select login method'; then",
        "        printf '\\r' > \"$box/in\"; sent=1",
        "      fi",
        "      url=\"$(sed -e 's/\\x1b\\[[0-9;?]*[a-zA-Z]//g' \"$box/out\" 2>/dev/null | tr -d '\\r' "
        "| grep -aoE 'https://[^[:space:]]+' | head -n 1)\"",
        '      if [ -n "$url" ]; then printf "%s\\n" "$url"; exit 0; fi',
        "      sleep 1",
        "    done",
        "    exit 70",
        "    ;;",
        "  agy-signin-stop)",
        '    box="$HOME/.agy-signin"',
        '    pg="$(cat "$box/pid" 2>/dev/null)"; holder="$(cat "$box/holder" 2>/dev/null)"',
        '    [[ "$pg" =~ ^[0-9]+$ ]] && kill -TERM -- -"$pg" 2>/dev/null',
        '    [[ "$holder" =~ ^[0-9]+$ ]] && kill -TERM "$holder" 2>/dev/null',
        "    sleep 1",
        '    [[ "$pg" =~ ^[0-9]+$ ]] && kill -KILL -- -"$pg" 2>/dev/null',
        '    [[ "$holder" =~ ^[0-9]+$ ]] && kill -KILL "$holder" 2>/dev/null',
        '    rm -rf "$box"',
        "    exit 0",
        "    ;;",
        "  agy-signin-diag)",
        # facts only: yes/no per variable, a byte count and sanitized output -- never a URL or a code
        '    box="$HOME/.agy-signin"',
        "    for v in SSH_CONNECTION SSH_TTY BROWSER DISPLAY DBUS_SESSION_BUS_ADDRESS; do",
        '      if [ -n "${!v:-}" ]; then echo "$v=yes"; else echo "$v=no"; fi',
        "    done",
        '    pg="$(cat "$box/pid" 2>/dev/null)"',
        '    if [[ "$pg" =~ ^[0-9]+$ ]] && kill -0 "$pg" 2>/dev/null; then echo "agy_alive=yes"; '
        'else echo "agy_alive=no"; fi',
        '    echo "out_bytes=$(wc -c < "$box/out" 2>/dev/null || echo 0)"',
        "    sed -e 's/\\x1b\\[[0-9;?]*[a-zA-Z]//g' \"$box/out\" 2>/dev/null | tr -d '\\r' "
        "| tail -n 30 | sed -E 's#https?://[^[:space:]]+#<url>#g'",
        "    exit 0",
        "    ;;",
        "  agy-probe)",
        # the nonce proves a sign-in works: refused unless alphanumeric, so it is safe in the prompt
        '    nonce="${2:-}"',
        '    [[ "$nonce" =~ ^[A-Za-z0-9]{8,64}$ ]] || { echo "refused: not a probe nonce" >&2; exit 64; }',
        '    pg="$(cat "$HOME/.agy-signin/pid" 2>/dev/null)"',
        '    if [[ "$pg" =~ ^[0-9]+$ ]]; then',
        "      for _ in $(seq 1 60); do kill -0 \"$pg\" 2>/dev/null || break; sleep 1; done",
        "    fi",
        '    timeout 300 agy -p "Reply with exactly this token and nothing else: $nonce" < /dev/null 2>&1',
        '    exit "${PIPESTATUS[0]}"',
        "    ;;",
        "  agy-signin-code)",
        # the code is a credential: read from STDIN only, never an argument
        '    IFS= read -r line || exit 66',
        '    [ -p "$HOME/.agy-signin/in" ] || { echo "no agy sign-in is waiting" >&2; exit 67; }',
        '    printf "%s\\n" "$line" > "$HOME/.agy-signin/in"',
        "    ;;",
        "  claude-install)",
        '    ver="${2:-}"',
        '    [[ "$ver" =~ ^[0-9]+\\.[0-9]+\\.[0-9]+$ ]] || { echo "refused: not x.y.z" >&2; exit 64; }',
        '    curl -fsSL https://claude.ai/install.sh | bash -s "$ver" 2>&1 | tail -3',
        '    exit "${PIPESTATUS[0]}"',
        "    ;;",
        '  *) echo "unknown subcommand" >&2; exit 64 ;;',
        "esac",
        "",
    ])


def _local_claude_version(cfg: MirrorConfig) -> Optional[str]:
    if cfg.local_versions is not None:
        return cfg.local_versions.get("claude")
    res = cpar.default_run(["claude", "--version"], timeout=60)
    return cpar._semver((res.stdout or "").splitlines()[0]) if res.returncode == 0 and res.stdout else None


def _refusal(step: str, failure: str, mirror: Sequence[dict], name: str = "",
             commands: Sequence[str] = (), fate: str = "WAITING") -> "ExecResult":
    return ExecResult(False, name=name, commands=tuple(commands), failure=failure,
                      fate={"fate": fate, "step": step, "reason": failure}, mirror=tuple(mirror))


def _mirror_record(item: MirrorItem, **extra) -> dict:
    rec = {"cli": item.cli, "route": item.route, "action": item.action, "present": bool(item.files),
           "files": list(item.files), "mode": None, "detail": item.detail,
           "operator_action": item.operator_action}
    if item.gap:
        rec["gap"] = item.gap
    rec.update(extra)
    return rec


def _mirrored_rel_files(items: Sequence[MirrorItem]) -> tuple[str, ...]:
    """Every $HOME-relative cache the mirror copied in -- the runner removes them on EVERY exit."""
    return tuple(sorted({rel for i in items if i.action == "mirrored" for rel in i.files}))


def _runner_unset(items: Sequence[MirrorItem]) -> tuple[str, ...]:
    """The API-key variables the lane must NOT see because the sign-in cache is mirrored: a key the
    laptop does not use for that CLI (R87). Taken from the same table the mirror reads."""
    names: list[str] = []
    for item in items:
        if item.action == "mirrored":
            names.extend(k for k in cpar.SIGN_IN[item.cli].env_keys if k not in names)
    return tuple(names)


def _status_is_dead(cli: str, res: GhResult) -> bool:
    """Is the sign-in the Codespace's own status call reports unusable? A non-zero exit or any of the
    dead-credential phrases in what the CLI printed; claude's JSON says `loggedIn` outright."""
    text = f"{res.stdout}\n{res.stderr}"
    if cli == "claude" and re.search(r'"loggedIn"\s*:\s*false', text):
        return True
    return (not res.ok) or bool(_CREDENTIAL_DEAD.search(text))


def _mirror_into_box(cfg: MirrorConfig, items: Sequence[MirrorItem], records: list[dict], name: str,
                     workdir: str, call: Callable[..., GhResult], artefacts: list[str],
                     commands: Sequence[str], tmp: Path, surface_agy: bool = False,
                     agy_wait_s: float = 0, clock: Callable[[], float] = time.monotonic,
                     sleep: Callable[[float], None] = time.sleep,
                     agy_channel: Optional[Path] = None) -> Optional["ExecResult"]:
    """The box-side half of the mirror. Returns None when every step held, else the refusal (the box
    exists and is named for teardown). Order: ship the helper; copy each mirrorable cache over stdin;
    leak-check what came back; have the Codespace's own status calls confirm each sign-in; make the
    Codespace's claude the laptop's. Nothing here prints, logs or records a byte of a credential."""
    tools_remote = f"{workdir}/{CREDENTIAL_TOOLS_NAME}"
    allowed = sorted({rel for i in items if i.action == "mirrored" for rel in i.files})
    helper = tmp / CREDENTIAL_TOOLS_NAME
    helper.write_text(_credential_tools_script(allowed), encoding="utf-8", newline="\n")
    shipped = call(["codespace", "cp", "-c", name, "-e", str(helper), f"remote:{tools_remote}"])
    if not shipped.ok:
        return _refusal("credentials", f"shipping the credential helper in exited {shipped.exit_code}",
                        records, name, commands, fate="FAILED")

    def tool(*args: str, stdin: Optional[bytes] = None) -> GhResult:
        return call(["codespace", "ssh", "-c", name, "--", *_remote("bash", "-l", tools_remote, *args)],
                    timeout=CREDENTIAL_CALL_TIMEOUT_S, input_bytes=stdin)

    by_cli = {r["cli"]: r for r in records}
    credentials: dict[str, bytes] = {}

    def leaked(names: Sequence[str]) -> "ExecResult":
        return _refusal("credentials",
                        f"credential leak: the bytes of {', '.join(names)} reached a command line or an "
                        "output (compared by hash and value; nothing was printed) -- REFUSED before the runner",
                        records, name, commands, fate="FAILED")

    for item in items:
        if item.action != "mirrored":
            continue
        for index, rel in enumerate(item.files):
            blob = (cfg.home / rel).read_bytes()
            credentials[item.cli if index == 0 else f"{item.cli}:{rel}"] = blob
            res = tool("install", rel, stdin=blob)
            echoed = leak_check({item.cli: blob}, [res.stdout, res.stderr])
            if echoed:     # judged before anything else: the box answered with the credential
                return leaked(echoed)
            mode = (re.search(r"^mode (\d+)\s*$", res.stdout or "", re.MULTILINE) or [None, None])[1]
            if not res.ok or mode != "600":
                return _refusal("credentials",
                                f"copying the {item.cli} sign-in cache ({rel}) into the box exited "
                                f"{res.exit_code} with mode {mode or 'unread'}; owner-only is the bar",
                                records, name, commands, fate="FAILED")
            if index == 0:
                by_cli[item.cli]["mode"] = mode
    leaks = leak_check(credentials, [*artefacts, *commands])
    if leaks:
        return leaked(leaks)

    # agy (G1): there is no non-interactive sign-in, so the OPERATOR is asked once -- the URL goes to
    # stderr and the credentials row, the code comes back through a laptop file and goes to agy's STDIN
    # only. No code in the window (or a failed relay/probe) is a recorded GAP: the box's auth process
    # tree is killed and reads go through copilot. The launch always continues.
    if surface_agy:
        for item in items:
            if item.action != "gap" or item.cli != "agy":
                continue
            record = by_cli[item.cli]
            channel = agy_channel if agy_channel is not None else tmp / "agy-code.txt"
            usable = True
            try:
                if channel.exists():     # a code left by an earlier run is never the answer
                    channel.unlink()
            except OSError:
                usable = False                      # ...and one that cannot be removed cannot be told apart
            signin = "no-url"
            code: Optional[str] = None
            if not usable:
                signin = "channel-unusable"
                record["auth_url_surfaced"] = False
            else:
                try:
                    res = tool("agy-signin-start")
                    found = re.search(r"https://\S+", res.stdout or "") if res.ok else None
                    record["auth_url_surfaced"] = bool(found)
                    if found:
                        line = (f"OPERATOR-ACTION: agy sign-in: open {found.group(0)}, "
                                f"then put the browser's code in {channel}")
                        record["operator_action_line"] = line
                        print(f"[codespace {name}] agy sign-in: waiting for the operator "
                              f"(up to {agy_wait_s:g}s)", file=sys.stderr)
                        print(line, file=sys.stderr)
                        start = clock()
                        beats = 0
                        next_beat = start + AGY_HEARTBEAT_S
                        while True:     # the last read happens at the deadline, never past it
                            try:
                                text = channel.read_text(encoding="utf-8").strip() if channel.is_file() else ""
                            except OSError:
                                text = ""
                            if text:
                                code = text
                                break
                            if clock() >= start + agy_wait_s:
                                break
                            if clock() >= next_beat:
                                beats += 1
                                next_beat += AGY_HEARTBEAT_S
                                print(f"[codespace {name}] agy sign-in: waiting for the code in {channel} "
                                      f"({int(clock() - start)}s of {agy_wait_s:g}s)", file=sys.stderr)
                            sleep(AGY_POLL_S)
                        record["heartbeats"] = beats
                        signin = "timeout"
                finally:
                    try:
                        channel.unlink(missing_ok=True)
                    except OSError:
                        record["channel_removed"] = False
            if code is not None:
                credentials["agy"] = code.encode("utf-8")
                relayed = tool("agy-signin-code", stdin=(code + "\n").encode("utf-8"))
                echoed = leak_check({"agy": credentials["agy"]}, [relayed.stdout, relayed.stderr])
                if echoed:
                    return leaked(echoed)
                if relayed.ok:
                    nonce = secrets.token_hex(8)
                    probed = tool("agy-probe", nonce)
                    ok = nonce in (probed.stdout or "")
                    record.update({"probe_nonce": nonce, "probe_ok": ok})
                    signin = "signed-in" if ok else "probe-failed"
                else:
                    signin = "relay-failed"
            record["signin"] = signin
            if signin != "signed-in":
                if signin == "no-url":
                    diag = tool("agy-signin-diag")
                    record["signin_diag"] = [ln for ln in (diag.stdout or "").splitlines() if ln.strip()]
                stopped = tool("agy-signin-stop")
                record.update({"auth_tree_killed": stopped.ok, "read_route": AGY_READ_FALLBACK})
                print(f"GAP: agy sign-in {signin}: the auth process tree was killed; "
                      f"reads go through {AGY_READ_FALLBACK}", file=sys.stderr)
            else:
                # the login lives in the keyring; the sign-in TUI would otherwise run to its own timeout
                record["auth_tree_killed"] = tool("agy-signin-stop").ok
            if "agy" in credentials:
                echoed = leak_check(
                    {"agy": credentials["agy"]},
                    [*artefacts, *commands, json.dumps(records, default=str)])
                if echoed:
                    return leaked(echoed)
    # the Codespace's own status call decides whether a sign-in is usable there (R59, R65)
    dead: list[str] = []
    for item in items:
        spec = cpar.SIGN_IN.get(item.cli)
        if spec is None or item.cli not in ("codex", "claude", "gh"):
            continue
        if item.action not in ("mirrored", "not-mirrored"):
            continue
        res = tool("status", item.cli)
        by_cli[item.cli]["remote_status"] = "dead" if _status_is_dead(item.cli, res) else "ok"
        if by_cli[item.cli]["remote_status"] == "dead":
            dead.append(f"OPERATOR-ACTION: {spec.renew}")
    if dead:
        return _refusal("credentials", "\n".join(dead), records, name, commands)

    # the Codespace's claude is the laptop's, derived at every launch -- never a hand-typed pin
    local = _local_claude_version(cfg)
    if not local or not _SEMVER_STRICT.match(local):
        return _refusal("claude-version", "the laptop's claude version could not be read: the "
                        "Codespace's cannot be made equal to it", records, name, commands, fate="FAILED")

    def remote_claude() -> Optional[str]:
        first = (tool("claude-version").stdout or "").strip().splitlines()
        return cpar._semver(first[0]) if first else None

    remote = remote_claude()
    if remote != local:
        tool("claude-install", local)
        remote = remote_claude()
    claude = by_cli.get("claude")
    if claude is None:
        claude = {"cli": "claude"}
        records.append(claude)
    claude.update({"local_version": local, "codespace_version": remote})
    if remote != local:
        return _refusal("claude-version",
                        f"claude version skew: the laptop runs {local} and the Codespace {remote or 'none'} "
                        "even after installing the laptop's version -- REFUSED before the runner",
                        records, name, commands, fate="FAILED")
    return None


def _codespace_runner_script(workdir: str, checkout_dir: str, head_argv: Sequence[str],
                             stall_after_s: int = RUNNER_STALL_AFTER_S,
                             unset: Sequence[str] = (), mirrored: Sequence[str] = (),
                             lane_branch: str = "") -> str:
    """The bash script shipped in and run as `bash <path>` -- never a string crossing the ssh
    boundary (the same measured failure `codespace_plan`'s own docstring names for the contract
    prompt: a command travels as a FILE, not an argument). `head_argv` runs with `checkout_dir`
    (the repo `gh codespace create` already checked out, `/workspaces/<repo-name>`) as its CWD --
    codex terra P1 (2026-09-27): an earlier version `cd`'d into `workdir` instead (this runner's
    OWN scratch directory for the contract/runner/receipt files, always empty of the repo), so
    the dispatched agent could read its contract but never touch, test, commit, or push the
    checkout the contract asks it to work in. `run.log`/`receipt.json` still live in `workdir`,
    by absolute path, since the agent's cwd is now the checkout, not the scratch directory."""
    quoted = " ".join(shlex.quote(a) for a in head_argv)
    run_log = f"{workdir}/run.log"
    receipt_json = f"{workdir}/receipt.json"
    handback_json = f"{workdir}/{RUNNER_HANDBACK_FILE}"
    # ONE STATEMENT PER LINE, joined by "\n" -- never ";" across a block. A `try/except`/`for`
    # body de-indented with ";" instead of a real newline is a Python IndentationError, and that
    # is exactly the failure mode this script exists not to introduce (measured while writing
    # this: an earlier ";".join version put the block's last statement and the next top-level one
    # on the same physical line at the block's own indent).
    #
    # THE REVERSE SCAN CONTINUES PAST A NON-JSON OR NON-DICT LINE, never stopping at the first
    # one -- codex terra P1 (2026-09-27): `run.log` also carries stderr (folded in by `2>&1`), so
    # a trailing diagnostic line after the agent's own final JSON result used to stop the scan
    # dead on the FIRST (i.e. last) line, leaving `d={}` and a zero exit code read as success even
    # when the real last JSON result reported an error.
    #
    # A STALLED RUN (item 5, R65): the runner's watchdog kills a head whose run log has not grown
    # for `stall_after_s` and passes `stalled` as the second argument; the receipt then says so --
    # `is_error`, status `hung`, and a FAILED fate with its reason and the step that failed -- so
    # a stalled lane is never an empty result with no fate.
    py = "\n".join([
        "import json,sys,os",
        f"RUN_LOG={run_log!r}",
        f"RECEIPT={receipt_json!r}",
        f"RUNNER_HB={handback_json!r}",
        f"STALL={int(stall_after_s)!r}",
        "t=open(RUN_LOG,encoding='utf-8',errors='replace').read()",
        "r=None",
        "for ln in reversed(t.splitlines()):",
        "    ln=ln.strip()",
        "    if not ln:",
        "        continue",
        "    try:",
        "        parsed=json.loads(ln)",
        "    except Exception:",
        "        continue",
        "    if isinstance(parsed,dict):",
        "        r=parsed",
        "        break",
        "d=r if isinstance(r,dict) else {}",
        "receipt={'admission':{'ok':True},"
        "'is_error':d.get('is_error'),'status':d.get('subtype'),'turns':d.get('num_turns'),"
        "'exit_code':int(sys.argv[1]),"
        "'transcript':{'session_id':d.get('session_id'),'path':''},"
        "'recovery':{'policy':'restart-once','attempt':0,'next':'none'}}",
        "if len(sys.argv)>2 and sys.argv[2]=='stalled':",
        "    receipt['is_error']=True",
        "    receipt['status']='hung'",
        "    receipt['fate']={'fate':'FAILED','step':'run',"
        "'reason':'hung: no progress for more than %ds (bound %ds); the runner killed the head' % (STALL,STALL)}",
        "hb_present=False",
        "last=None",
        "for ln in reversed(t.splitlines()):",
        "    try:",
        "        p=json.loads(ln.strip())",
        "    except Exception:",
        "        continue",
        "    if isinstance(p,dict) and p.get('type')=='result':",
        "        last=p",
        "        break",
        "if last is not None and isinstance(last.get('structured_output'),dict):",
        "    json.dump(last['structured_output'],open(RUNNER_HB,'w'))",
        "    hb_present=True",
        f"receipt['handback']={{'present':hb_present}}  # {RUNNER_HANDBACK_FILE}",
        "E=os.environ.get",
        "bs,hs,br,ps,pe=E('CS_BASE_SHA') or None,E('CS_HEAD_SHA') or None,E('CS_BRANCH') or None,"
        "E('CS_PUSHED_SHA') or None,E('CS_PUSH_EXIT') or None",
        "receipt['commit']={'branch':br,'base_sha':bs,'head_sha':hs,'pushed_sha':ps,"
        "'committed':bool(hs and bs and hs!=bs),'pushed':bool(ps and ps==hs),"
        "'push_exit':int(pe) if pe is not None else None}",
        "json.dump(receipt,open(RECEIPT,'w'))",
    ])
    heartbeat = shlex.quote(f"{workdir}/heartbeat")
    stalled = shlex.quote(f"{workdir}/stalled")
    names = " ".join(RUNNER_SECRETS)
    never = " ".join(RUNNER_NEVER_SET)
    removed = " ".join([*RUNNER_NEVER_SET, *(n for n in unset if n not in RUNNER_NEVER_SET)])
    rm_list = " ".join(f'"$HOME/{m}"' for m in mirrored)
    return "\n".join([
        "#!/usr/bin/env bash",
        "set -uo pipefail",
        # a dropped ssh connection sends SIGHUP: the lane outlives it and the receipt is still written
        "trap '' HUP",
        # the one EXIT trap, present even when nothing was mirrored: it also removes the fallback's auth.json
        "cs_codex_fallback=0",
        f"""trap 'rm -f {rm_list}; [ "$cs_codex_fallback" = 1 ] && rm -f "$HOME/.codex/auth.json"' EXIT""",
        f"cd {shlex.quote(checkout_dir)} || exit 90",
        "base_sha=$(git rev-parse HEAD 2>/dev/null || true)",
        f"rm -f {stalled}",
        # BOOLEANS ONLY (R13): a name and yes/no. `${!n}` is read for emptiness and never printed.
        f"for n in {names}; do",
        '  if [ -n "${!n:-}" ]; then v=yes; else v=no; fi',
        '  echo "[runner] secret $n set=$v"',
        f"done > {shlex.quote(run_log)} 2>&1",
        # the keys no codex call may see (R87.3): a boolean per name, then removed on EVERY launch
        f"for n in {never}; do",
        '  if [ -n "${!n:-}" ]; then v=yes; else v=no; fi',
        '  echo "[runner] api-key $n present-before-unset=$v"',
        f"done >> {shlex.quote(run_log)} 2>&1",
        # the fallback sign-in (R87): a separate login's auth.json from a secret, only where the
        # mirror put nothing -- written owner-only, its value never echoed
        'if [ -n "${CODEX_AUTH_JSON:-}" ] && [ ! -f "$HOME/.codex/auth.json" ]; then '
        'umask 077; mkdir -p "$HOME/.codex"; printf "%s" "$CODEX_AUTH_JSON" > "$HOME/.codex/auth.json"; '
        'chmod 600 "$HOME/.codex/auth.json"; cs_codex_fallback=1; fi',
        # no codex invocation sees an API key, and a key the laptop does not use for a mirrored CLI is
        # not in the lane's environment either (R87, R87.3)
        f"unset {removed}",
        # the heartbeat says the runner PROCESS lives (the run log's age says the lane works)
        f"( while :; do date +%s > {heartbeat}; sleep {cs.HEARTBEAT_S}; done ) &",
        "hb=$!",
        # stdin is closed: `claude -p` waits 3 s on an open one and a codex head would hang (D8)
        f"{quoted} < /dev/null >> {shlex.quote(run_log)} 2>&1 &",
        "head=$!",
        # the watchdog: a run log quiet for longer than the bound is a stalled head
        "( while kill -0 $head 2>/dev/null; do",
        "    sleep 15",
        "    now=$(date +%s)",
        f"    mt=$(stat -c %Y {shlex.quote(run_log)} 2>/dev/null || echo $now)",
        f"    if [ $((now - mt)) -gt {int(stall_after_s)} ]; then",
        f"      echo stalled > {stalled}",
        "      kill -TERM $head 2>/dev/null; sleep 5; kill -KILL $head 2>/dev/null",
        "      break",
        "    fi",
        "  done ) &",
        "wd=$!",
        "wait $head",
        "code=$?",
        "kill $hb $wd 2>/dev/null",
        'stalled=""',
        f'if [ -f {stalled} ]; then stalled=stalled; code=124; fi',
        'head_sha=$(git rev-parse HEAD 2>/dev/null || true)',
        'branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)',
        'push_exit=""; pushed_sha=""',
        # A lane that followed the repo rule "parallel work needs a worktree" commits on its own
        # branch in a LINKED worktree; the checkout's HEAD never moves. When the checkout is
        # unchanged, the lane's declared branch is witnessed and pushed instead (live 2026-10-16:
        # finished work read "the lane committed nothing").
        f"lane_branch={shlex.quote(lane_branch)}",
        'lane_sha=""',
        'if [ -n "$lane_branch" ] && [ "$head_sha" = "$base_sha" ] '
        '&& [ "$lane_branch" != main ]; then',
        '  lane_sha=$(git rev-parse --verify --quiet "refs/heads/$lane_branch" 2>/dev/null || true)',
        "fi",
        'if [ -n "$lane_sha" ] && [ "$lane_sha" != "$base_sha" ]; then',
        '  head_sha="$lane_sha"; branch="$lane_branch"',
        '  git push origin "refs/heads/$lane_branch:refs/heads/$lane_branch" >> '
        + shlex.quote(run_log) + ' 2>&1; push_exit=$?',
        '  pushed_sha=$(git ls-remote origin "refs/heads/$lane_branch" 2>/dev/null | cut -f1 | head -n1)',
        'elif [ -n "$base_sha" ] && [ "$head_sha" != "$base_sha" ] && [ -n "$branch" ] '
        '&& [ "$branch" != main ] && [ "$branch" != HEAD ]; then',
        '  git push origin "HEAD:refs/heads/$branch" >> ' + shlex.quote(run_log) + ' 2>&1; push_exit=$?',
        '  pushed_sha=$(git ls-remote origin "refs/heads/$branch" 2>/dev/null | cut -f1 | head -n1)',
        "fi",
        'CS_BASE_SHA="$base_sha" CS_HEAD_SHA="$head_sha" CS_BRANCH="$branch" '
        'CS_PUSHED_SHA="$pushed_sha" CS_PUSH_EXIT="$push_exit" '
        f'python3 -c {shlex.quote(py)} "$code" "$stalled"',
        "exit $code",
        "",
    ])


def codespace_exec(repo: str, branch: str, slug: str, contract: Path, head_argv: Sequence[str],
                    *, machine: str = "standardLinux32gb", idle_timeout: str = "240m",
                    retention: str = "24h", workdir: str = "/workspaces/dispatch",
                    invoker: Optional[Callable[..., GhResult]] = None,
                    sleep: Callable[[float], None] = time.sleep,
                    run_timeout_s: float = RUN_TIMEOUT_SECONDS,
                    mirror: Optional[MirrorConfig] = None, batch: str,
                    receipts_root: Optional[Path] = None,
                    ledger_path: Optional[Path] = None,
                    schema_smoke: Optional[Callable[[list[str]], "SmokeResult"]] = None,
                    pins: Optional[Callable[[str], tuple[int, list[str]]]] = None,
                    agy_wait_s: float = 0,
                    clock: Callable[[], float] = time.monotonic) -> ExecResult:
    """`_codespace_exec_core` plus the FINISH witnesses. `batch` is a required keyword: every step of
    the line -- create, credentials, run, commit, handback -- writes one row of `<receipts_root>/
    <batch>/<slug>/steps.jsonl` (`ExecResult.steps` carries the same rows), the regime ledger gets its
    open row once the box exists, and a run whose lane committed and pushed nothing, or returned no
    valid handback, is FAILED at that step. An empty `batch` is refused before any `gh` call."""
    if not batch:
        raise DispatchRefused("codespace_exec needs a non-empty batch: the FINISH receipts and gates "
                              "are not optional")
    for flag in ("--json-schema", "--model"):
        if list(head_argv).count(flag) > 1:
            raise DispatchRefused(f"head_argv carries {flag} more than once: the schema smoke and the "
                                  "run would not judge the same token")
    rows: list[dict] = []
    steps_path = _harvest_dir(batch, slug, root=receipts_root) / "steps.jsonl"

    def rec(step: str, ok: bool, codespace: str = "", evidence: Optional[dict] = None,
            failure: str = "", fate: Optional[dict] = None) -> None:
        rows.append(write_step(steps_path, batch, slug, codespace, step, ok, evidence, failure, fate))

    result = _codespace_exec_core(repo, branch, slug, contract, head_argv, machine=machine,
                                  idle_timeout=idle_timeout, retention=retention, workdir=workdir,
                                  invoker=invoker, sleep=sleep, run_timeout_s=run_timeout_s,
                                  mirror=mirror, batch=batch, rec=rec, ledger_path=ledger_path,
                                  schema_smoke=schema_smoke, pins=pins, agy_wait_s=agy_wait_s,
                                  clock=clock, agy_channel=steps_path.parent / "agy-code.txt")
    return replace(result, steps=tuple(rows))


def branch_pin_check(branch: str, *, run: Callable[..., "cpar.CmdResult"] = cpar.default_run,
                     laptop: Optional[Mapping[str, Optional[str]]] = None) -> tuple[int, list[str]]:
    """`(exit code, finding lines)` for the pin record the BRANCH carries -- read at FETCH_HEAD, never
    the checked-out copy: the box is created from the branch, so the branch's record is what binds.
    A fetch or read that fails is `(2, [reason])`: could not look, never silently clean."""
    fetched = run(["git", "fetch", "origin", branch], cwd=HUB_ROOT, timeout=120)
    if fetched.returncode != 0:
        return 2, [f"could not fetch origin {branch} (exit {fetched.returncode})"]
    shown = run(["git", "show", "FETCH_HEAD:.devcontainer/provisioning.yaml"], cwd=HUB_ROOT, timeout=60)
    if shown.returncode != 0:
        return 2, [f"could not read .devcontainer/provisioning.yaml on {branch} (exit {shown.returncode})"]
    with tempfile.TemporaryDirectory() as tmp:
        record = Path(tmp) / "provisioning.yaml"
        record.write_text(shown.stdout, encoding="utf-8", newline="\n")
        try:
            if laptop is None:
                laptop = cpar.read_laptop_versions(tuple(cpar.typed_pins(record)))
            return cpar.pin_check(record, laptop)
        except cpar.PinError as exc:
            return 2, [str(exc)]


def write_step(path: Path, batch: str, lane: str, codespace: str, step: str, ok: bool,
               evidence: Optional[dict] = None, failure: str = "",
               fate: Optional[dict] = None) -> dict:
    """Append one `codespace-step` row (booleans, ids, counts and paths -- never a value, R13)."""
    row = {"schema": 1, "kind": "codespace-step", "batch": batch, "lane": lane,
           "codespace": codespace, "step": step, "ok": bool(ok),
           "recorded": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "evidence": evidence or {}, "failure": failure, "fate": fate or {}}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    return row


def _handback_evidence(raw: str) -> dict:
    """{present, valid, errors} for a pulled `handback.json` -- judged by the LaneReport schema."""
    if not raw.strip():
        return {"present": False, "valid": False, "errors": []}
    try:
        from ecosystem.schema.lane_report import LaneReport
        LaneReport.model_validate(json.loads(raw))
    except json.JSONDecodeError as exc:
        return {"present": True, "valid": False, "errors": [f"not JSON: {exc.msg}"]}
    except Exception as exc:
        errors = getattr(exc, "errors", None)
        found = ([f"{'.'.join(str(p) for p in e.get('loc', ()))}: {e.get('msg', '')}" for e in errors()]
                 if callable(errors) else [str(exc)])
        return {"present": True, "valid": False, "errors": found}
    return {"present": True, "valid": True, "errors": []}


def _codespace_exec_core(repo: str, branch: str, slug: str, contract: Path, head_argv: Sequence[str],
                    *, machine: str = "standardLinux32gb", idle_timeout: str = "240m",
                    retention: str = "24h", workdir: str = "/workspaces/dispatch",
                    invoker: Optional[Callable[..., GhResult]] = None,
                    sleep: Callable[[float], None] = time.sleep,
                    run_timeout_s: float = RUN_TIMEOUT_SECONDS,
                    mirror: Optional[MirrorConfig] = None, batch: str,
                    rec: Optional[Callable[..., None]] = None,
                    ledger_path: Optional[Path] = None,
                    schema_smoke: Optional[Callable[[list[str]], "SmokeResult"]] = None,
                    pins: Optional[Callable[[str], tuple[int, list[str]]]] = None,
                    agy_wait_s: float = 0,
                    clock: Callable[[], float] = time.monotonic,
                    agy_channel: Optional[Path] = None) -> ExecResult:
    """Actually RUN `codespace_plan`'s create/exec steps end to end -- ported from the first half
    of `Start-DispatchCodespace` (create, read the NAME back, read the creation log and refuse a
    recovery container, ship the contract and a generated runner script in, run it, pull
    `receipt.json` back). Harvest, stop and delete are the separate legs below, matching the PS
    module's own split.

    DECIDED-BY-LANE (b2-codespace-green, item 1, D1): the run step is `bash -l <runner>`, a LOGIN
    shell. A non-login ssh shell sees none of the five Codespaces secrets (night probe x3:
    `set=no`; a login shell `yes`), so `claude -p` answered 'Not logged in'. `bash -l` is what the
    PS verb did, what `codespace_admission` and `codespace_parity` already assume ("PATH is only
    complete there"), and what the night's workaround proved; an equivalent (sourcing a profile
    by hand) would be a second spelling of the same fact. The runner closes the head's stdin (D8)
    and records the five secrets as booleans (R13).

    THE CREDENTIAL MIRROR (b2-codespace-subscription-auth, R87). With a `mirror` config the launch
    decides every CLI's sign-in from the laptop's own files BEFORE a box exists (a dead credential
    refuses here, WAITING, with its one renew line and no `gh` call), copies each mirrorable cache in
    over stdin once the box is up, has the Codespace's own status call confirm it, makes the
    Codespace's claude the laptop's version, and proves by hash that no credential reached any
    artefact -- all before the runner starts. The CLI verb always passes one; `None` (a library
    caller's seam) skips it and says so in the result's empty `mirror`."""
    if not head_argv:
        # Codex terra P1 (2026-09-27): an empty argv made `_codespace_runner_script` emit a
        # redirection-only shell command -- `> run.log 2>&1` with no left-hand side -- that exits
        # 0 and writes a success receipt having run no agent at all.
        return ExecResult(False, failure="head_argv is empty -- nothing to run in the codespace")
    rec = rec or (lambda *a, **k: None)
    items: list[MirrorItem] = []
    records: list[dict] = []

    def creds_evidence() -> dict:
        return {"clis": [dict(r) for r in records],
                "gaps": [i.cli for i in items if i.action == "gap"]}

    if mirror is not None:
        items = credential_decisions(mirror)
        records = [_mirror_record(i) for i in items]
        refused = [i for i in items if i.action == "refused"]
        if refused:
            failure = "\n".join(i.operator_action for i in refused)
            result = _refusal("credentials", failure, records)
            rec("credentials", False, "", creds_evidence(), failure, result.fate)
            return result
    # RESOLVE TO ABSOLUTE, matching `plan` cmd's own `path.resolve()` before it builds the prompt
    # embedded in `head_argv` (line ~1792). Codex terra P1 (2026-09-27): a caller following the
    # documented `plan` -> `codespace-exec --argv-json` flow with a RELATIVE contract argument
    # left `str(contract)` unable to match the absolute path already baked into `head_argv`'s
    # prompt -- the rewrite below silently did nothing, and the local path leaked into the runner.
    contract = Path(contract).resolve()
    commands: list[str] = []

    artefacts: list[str] = []   # every string a `gh` call returned, for the leak check

    smoke_argv = schema_smoke_argv(head_argv) if schema_smoke is not None else None
    if smoke_argv is not None:
        smoked = schema_smoke(smoke_argv)
        if not smoked.ok:
            failure = f"schema smoke: claude refused the --json-schema token (exit {smoked.exit_code}): {smoked.detail}"
            result = ExecResult(False, mirror=tuple(records), failure=failure,
                                fate={"fate": "FAILED", "step": "schema-smoke", "reason": failure})
            rec("schema-smoke", False, "", {"exit_code": smoked.exit_code}, failure, result.fate)
            return result
        rec("schema-smoke", True, "", {"exit_code": smoked.exit_code})
    if pins is not None:
        pin_code, pin_lines = pins(branch)
        if pin_code != 0:
            action = (f"OPERATOR-ACTION: run `uv run --locked python scripts/codespace_parity.py pin write`, "
                      f"commit it to {branch} and push, then launch again")
            failure = "\n".join([*pin_lines, action])
            result = _refusal("pins", failure, records)
            rec("pins", False, "", {"exit_code": pin_code, "findings": len(pin_lines)}, failure, result.fate)
            return result
        rec("pins", True, "", {"exit_code": pin_code})

    def call(argv: Sequence[str], timeout: float = GH_TIMEOUT_SECONDS,
             input_bytes: Optional[bytes] = None) -> GhResult:
        commands.append(format_gh_line(argv))
        res = run_gh(argv, invoker=invoker, timeout=timeout, input_bytes=input_bytes)
        artefacts.extend((res.stdout, res.stderr))
        return res

    created = call(["codespace", "create", "-R", repo, "-b", branch, "--machine", machine,
                    "--idle-timeout", idle_timeout, "--retention-period", retention, "-d", slug])
    if not created.ok:
        failure = f"create exited {created.exit_code}"
        fate = {"fate": "FAILED", "step": "create", "reason": failure} if batch else {}
        rec("create", False, "", {"repo": repo, "branch": branch, "machine": machine,
                                  "exit_code": created.exit_code}, failure, fate)
        return ExecResult(False, commands=tuple(commands), mirror=tuple(records),
                           failure=failure, fate=fate)
    # THE NAME IS RETURNED BY CREATE -- IT IS NEVER RECONSTRUCTED (measured, `[CLI-SRC]`:
    # `gh codespace create` writes `codespace.Name` via `fmt.Fprintln`,
    # `DIGEST-2026-09-15-codespaces-reference.md:182-183`). Codex terra P1 (2026-09-27): an
    # earlier version re-derived the name from `gh codespace list --json` matched by display
    # name, which is not unique across a stale stopped codespace from a prior run of this same
    # slug -- ambiguous, and a codespace this call just created (and is now billing) would be
    # orphaned untracked on a list failure or a match miss.
    name = created.stdout.strip()
    if not name:
        return ExecResult(False, commands=tuple(commands), mirror=tuple(records),
                           failure="`gh codespace create` returned no name on stdout")
    rec("create", True, name, {"repo": repo, "branch": branch, "machine": machine,
                               "exit_code": created.exit_code})
    if batch:
        regime.write_receipt(slug, batch, name, created=datetime.now(timezone.utc), deleted=None,
                             machine=machine, prebuild=False, tokens={}, ledger_path=ledger_path)
    # THE CREATION LOG IS READ BEFORE ANYTHING SHIPS (item 3, D3). A recovery container is
    # reachable and reports `Available` throughout, so nothing else says it is not ours; the log is
    # the one discriminator GitHub documents. A log that is not finished yet is read again a
    # bounded number of times; one that never finishes, or that names a recovery container or a
    # failed creation, REFUSES the run -- the box exists and is named for teardown.
    refusal = _creation_log_refusal(name, call, sleep)
    if refusal:
        return ExecResult(False, name=name, commands=tuple(commands), mirror=tuple(records), failure=refusal)

    # REWRITE THE CONTRACT PATH. `head_argv` (built by `plan` from `build_plan`) carries the
    # prompt "Read and execute the frozen contract at <LOCAL path>" -- a path on the machine that
    # RAN `plan`, which does not exist inside the codespace. Only the remote copy this function
    # itself ships in (`{workdir}/{contract.name}`, below) does. Codex terra P1 (2026-09-27): the
    # unrewritten argv asked the agent to read a file that was never there, so no planned
    # dispatch could ever execute its own contract.
    remote_contract = f"{workdir}/{Path(contract).name}"
    runner_argv = [a.replace(str(contract), remote_contract) for a in head_argv]
    # `gh codespace create -R owner/name` checks the repo out to `/workspaces/<name>` -- the
    # directory the dispatched agent must run in, never `workdir` itself (that is this runner's
    # OWN scratch space; see `_codespace_runner_script`'s docstring, codex terra P1, 2026-09-27).
    checkout_dir = f"/workspaces/{repo.rsplit('/', 1)[-1]}"

    with tempfile.TemporaryDirectory() as tmp:
        runner_local = Path(tmp) / f"run-{slug}.sh"
        runner_local.write_text(_codespace_runner_script(workdir, checkout_dir, runner_argv,
                                                         unset=_runner_unset(items),
                                                         mirrored=_mirrored_rel_files(items),
                                                         lane_branch=(slug if slug.startswith("worktree-")
                                                                      else "worktree-" + (
                                                                          slug if slug.startswith("lane-")
                                                                          else "lane-" + slug))),
                                 encoding="utf-8", newline="\n")
        receipt_local = Path(tmp) / "receipt.json"
        runner_remote = f"{workdir}/run-{slug}.sh"

        # `workdir` is NOT the checkout `gh codespace create` produces (that lands under
        # `/workspaces/<repo-name>`) -- it is only where THIS runner's own files live, and
        # nothing creates it. Codex terra P1 (2026-09-27): the first `cp` into it failed on
        # every fresh codespace because the directory had never existed.
        mkdir = call(["codespace", "ssh", "-c", name, "--", *_remote("mkdir", "-p", workdir)])
        if not mkdir.ok:
            return ExecResult(False, name=name, commands=tuple(commands), mirror=tuple(records),
                               failure=f"creating {workdir} exited {mkdir.exit_code}")
        if batch:
            regime.mark_ready(name, ledger_path=ledger_path)

        cp1 = call(["codespace", "cp", "-c", name, "-e", str(contract),
                    f"remote:{workdir}/{Path(contract).name}"])
        if not cp1.ok:
            return ExecResult(False, name=name, commands=tuple(commands), mirror=tuple(records),
                               failure=f"shipping the contract in exited {cp1.exit_code}")

        if mirror is not None:
            stop = _mirror_into_box(mirror, items, records, name, workdir, call, artefacts, commands,
                                    Path(tmp), surface_agy=bool(batch), agy_wait_s=agy_wait_s,
                                    clock=clock, sleep=sleep, agy_channel=agy_channel)
            if stop is not None:
                rec("credentials", False, name, creds_evidence(), stop.failure, stop.fate)
                return stop
            rec("credentials", True, name, creds_evidence())

        cp2 = call(["codespace", "cp", "-c", name, "-e", str(runner_local),
                    f"remote:{runner_remote}"])
        if not cp2.ok:
            return ExecResult(False, name=name, commands=tuple(commands), mirror=tuple(records),
                               failure=f"shipping the runner in exited {cp2.exit_code}")

        # THE RECEIPT IS PULLED REGARDLESS OF `ran.ok` (codex terra P1, 2026-09-27): the runner
        # writes `receipt.json` in its own `exit $code` tail, so a non-zero ssh exit still has a
        # receipt worth reading -- returning early on `ran.ok` alone threw away exactly the
        # evidence a failed lane most needs kept.
        ran = call(["codespace", "ssh", "-c", name, "--", *_remote("bash", "-l", runner_remote)],
                   timeout=run_timeout_s)

        # THE FATE OF A RUN WHOSE TRANSPORT DIED (item 5, R65): ssh's own exit 255 is a dropped
        # connection and gh's 124 a timeout (`run_gh`). The lane may still be running on the box --
        # the runner outlives a hangup -- so this is FAILED at the `run` step with the reason, and
        # the box is named for the observer / harvest, never an empty result with no fate.
        transport_fate: dict = {}
        if not ran.ok and ran.exit_code in (255, 124):
            what = ("disconnected: the ssh session to the codespace dropped"
                    if ran.exit_code == 255 else
                    f"timed out: the run step exceeded {run_timeout_s:.0f}s")
            transport_fate = {"fate": "FAILED", "step": "run",
                              "reason": f"{what} (exit {ran.exit_code}); the lane may still be "
                                        "running on the box -- observe it, then harvest"}

        cp3 = call(["codespace", "cp", "-c", name, "-e", f"remote:{workdir}/receipt.json",
                    str(receipt_local)])
        if not cp3.ok or not receipt_local.exists():
            failure = ("no receipt came back -- NOT reporting success (same doctrine as the "
                      "PS verb's own receipt gate)")
            if not ran.ok:
                failure = f"the runner exited {ran.exit_code}; {failure}"
            fate = transport_fate or {"fate": "FAILED", "step": "receipt", "reason": failure}
            rec("run", False, name, {"exit_code": ran.exit_code, "status": None, "is_error": None,
                                     "turns": None, "session_id": None}, failure, fate)
            return ExecResult(False, name=name, commands=tuple(commands), mirror=tuple(records), failure=failure,
                              fate=fate)
        try:
            receipt = json.loads(receipt_local.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failure = f"receipt.json did not parse: {exc}"
            fate = {"fate": "FAILED", "step": "receipt", "reason": failure}
            rec("run", False, name, {"exit_code": ran.exit_code, "status": None, "is_error": None,
                                     "turns": None, "session_id": None}, failure, fate)
            return ExecResult(False, name=name, commands=tuple(commands), mirror=tuple(records), failure=failure,
                              fate=fate)

        # a stalled head's receipt carries the runner's own fate (reason + step), written there
        # by the runner that killed it
        receipt_fate = receipt.get("fate") if isinstance(receipt.get("fate"), dict) else {}
        run_failure, run_fate = "", {}
        if not ran.ok:
            run_failure = f"the runner exited {ran.exit_code}"
            run_fate = transport_fate or receipt_fate or {
                "fate": "FAILED", "step": "run",
                "reason": f"{run_failure}; the receipt reports status={receipt.get('status')!r}"}
        # THE RECEIPT'S OWN VERDICT GATES SUCCESS TOO (codex terra P1, 2026-09-27): the ssh call
        # can exit 0 while the agent it ran reports `is_error: true` or a non-success status --
        # `bash runner_remote` only ever fails on a TRANSPORT problem, not a lane one.
        elif receipt.get("is_error") or receipt.get("status") not in (None, "success"):
            run_failure = (f"the lane's own receipt reports failure: "
                           f"is_error={receipt.get('is_error')!r} status={receipt.get('status')!r}")
            run_fate = receipt_fate or {"fate": "FAILED", "step": "run", "reason": run_failure}
        transcript = receipt.get("transcript") if isinstance(receipt.get("transcript"), dict) else {}
        rec("run", not run_failure, name,
            {"exit_code": receipt.get("exit_code"), "status": receipt.get("status"),
             "is_error": receipt.get("is_error"), "turns": receipt.get("turns"),
             "session_id": transcript.get("session_id")}, run_failure, run_fate)

        failure, fate = run_failure, run_fate
        if batch:
            commit = receipt.get("commit") if isinstance(receipt.get("commit"), dict) else {}
            commit_ok = bool(commit.get("committed") and commit.get("pushed"))
            commit_failure = "" if commit_ok else (
                "the lane committed nothing" if not commit.get("committed")
                else "the lane's commit was not pushed to origin")
            commit_fate = {} if commit_ok else {"fate": "FAILED", "step": "commit",
                                                "reason": commit_failure}
            rec("commit", commit_ok, name,
                {k: commit.get(k) for k in ("branch", "base_sha", "head_sha", "pushed_sha",
                                            "committed", "pushed", "push_exit")},
                commit_failure, commit_fate)
            pulled = call(["codespace", "ssh", "-c", name, "--", *_remote("cat", f"{workdir}/{RUNNER_HANDBACK_FILE}")])
            evidence = _handback_evidence(pulled.stdout if pulled.ok else "")
            hb_ok = evidence["present"] and evidence["valid"]
            hb_failure = "" if hb_ok else (
                "the lane returned no handback" if not evidence["present"]
                else "the lane's handback does not validate against the lane-report schema")
            hb_fate = {} if hb_ok else {"fate": "FAILED", "step": "handback", "reason": hb_failure}
            rec("handback", hb_ok, name, evidence, hb_failure, hb_fate)
            if not failure:
                failure, fate = commit_failure or hb_failure, commit_fate or hb_fate
        if failure:
            return ExecResult(False, name=name, receipt=receipt, commands=tuple(commands), mirror=tuple(records),
                               failure=failure, fate=fate)

    return ExecResult(True, name=name, receipt=receipt, commands=tuple(commands), mirror=tuple(records))


def _creation_log_refusal(name: str, call: Callable[..., GhResult],
                          sleep: Callable[[float], None]) -> str:
    """'' when the creation log says the container is ours; else the reason to refuse the run.

    READS THE LOG OVER SSH with a timeout, until `CREATION_LOG_WAIT_BOUND_S` of sleep is spent
    while it is INDETERMINATE (empty, unreadable, or not yet finished). A recovery container
    or a failed creation refuses at once: another read cannot make it ours."""
    verdict = None
    for attempt in range(CREATION_LOG_ATTEMPTS):
        res = call(["codespace", "ssh", "-c", name, "--", *_remote("cat", cs.CREATION_LOG_PATH)],
                   timeout=cs.SSH_TIMEOUT_S)
        verdict = cs.classify_creation_log(res.stdout if res.ok else "")
        if verdict.verdict is cs.ContainerVerdict.OURS:
            return ""
        if verdict.verdict is not cs.ContainerVerdict.INDETERMINATE:
            break
        if attempt + 1 < CREATION_LOG_ATTEMPTS:
            sleep(CREATION_LOG_WAIT_S)
    assert verdict is not None
    why = f"the codespace is a {verdict.verdict.value}: {verdict.reason}"
    if verdict.verdict is cs.ContainerVerdict.INDETERMINATE:
        why += f" (read {CREATION_LOG_ATTEMPTS} times)"
    return why + " -- the run was REFUSED; the box exists and must be deleted"


# ----- observe: what is the lane doing, and what is its fate (items 3 and 5) ------------------------

def codespace_observe(name: str, *, workdir: str = "/workspaces/dispatch",
                      expected_gone: bool = False, unreachable_for_s: float = 0.0,
                      slug: Optional[str] = None, ledger_path: Optional[Path] = None,
                      now: Optional[datetime] = None,
                      invoker: Optional[Callable[[Sequence[str]], GhResult]] = None) -> dict:
    """One reading of a Codespace lane: the platform state from a LISTING, the progress signal over
    ssh (both bounded), crossed by `codespace_state.assess_lane` into a state AND a fate.

    A live lane reads `working` (not `unknown`); a deleted codespace reads `absent` -- `torn-down`
    when `expected_gone` says this line deleted it; a stalled one reads `hung` and a disconnected
    one `disconnected`, each FAILED with its reason and step; what cannot be read is WAITING with
    its gate named. The box is probed over ssh only while the platform says it is `Available`: a
    probe of a deleted or stopped box says nothing.

    THE FATE HAS ITS OWN CLOCK AND THE LINE RECORDS IT (review P1-2). With a `slug` the regime
    ledger is the observer's memory: the first reading of an unreachable box stamps
    `unreachable_since` on its fate row, every later reading derives the duration from that stamp
    (no caller has to count), and a reachable reading ends the streak. Every fate TRANSITION --
    (fate, state) changed, or an unreachable streak began or ended -- is appended through
    `codespace_regime.write_fate`; a repeat of the same reading appends nothing. `unreachable_for_s`
    stays an override for a caller with a longer clock of its own (the larger of the two wins); with
    no `slug` the read records nothing and the clock is the caller's alone. DECIDED-BY-LANE: a stored
    stamp, not an observer loop -- the line stays one-shot per invocation (no process outlives its
    handback) and the bound is measured across invocations, whoever makes them."""
    stamp = now or datetime.now(timezone.utc)
    listing = run_gh(["codespace", "list", "--json", "name,state"], invoker=invoker,
                     timeout=cs.SSH_TIMEOUT_S)
    container: Optional[str] = None
    if listing.ok:
        try:
            rows = json.loads(listing.stdout or "[]")
        except json.JSONDecodeError:
            rows = None
        if isinstance(rows, list):
            container = cs.state_from_listing(rows, name)
    reading: Optional[cs.ProgressReading] = None
    if container == "Available":
        probe = run_gh(cs.progress_args(name, workdir), invoker=invoker, timeout=cs.SSH_TIMEOUT_S)
        reading = (cs.parse_progress(probe.stdout) if probe.ok else
                   cs.ProgressReading(reachable=False,
                                      error=f"ssh exited {probe.exit_code}"))
    streak = container == "Available" and reading is not None and not reading.reachable
    prev = regime.last_fate(name, ledger_path, slug=slug) if slug is not None else None
    prior_since: Optional[datetime] = None
    if (prev or {}).get("unreachable_since"):
        try:
            prior_since = datetime.fromisoformat(prev["unreachable_since"])
        except (TypeError, ValueError):
            prior_since = None
    since: Optional[datetime] = None
    if streak:
        since = min(stamp, prior_since) if prior_since else stamp
        if slug is not None:
            unreachable_for_s = max(unreachable_for_s, (stamp - since).total_seconds())
    elif container is None and prior_since is not None:
        # an INDETERMINATE reading (the listing could not be read) says nothing about the box:
        # the stamp survives it, and ends only on an affirmative recovery or a terminal state
        since = prior_since
    assessed = cs.assess_lane(container, reading, unreachable_for_s=unreachable_for_s,
                              expected_gone=expected_gone)
    recorded = False
    if slug is not None:
        changed = (prev is None
                   or (prev.get("fate"), prev.get("state")) != (assessed.fate, assessed.state.value)
                   or bool(prev.get("unreachable_since")) != (since is not None))
        if changed:
            regime.write_fate(name, slug, assessed.fate, assessed.state.value, assessed.reason,
                              assessed.step, ledger_path=ledger_path, now=stamp,
                              unreachable_since=since)
            recorded = True
    return {
        "codespace": name,
        "container_state": container,
        "state": assessed.state.value,
        "fate": assessed.fate,
        "reason": assessed.reason,
        "step": assessed.step,
        "progress_age_s": reading.age_s if reading else None,
        "runner_alive": reading.runner_alive if reading else None,
        "receipt_present": reading.receipt_present if reading else False,
        "reachable": reading.reachable if reading else None,
        "unreachable_for_s": unreachable_for_s,
        "unreachable_since": since.isoformat(timespec="seconds") if since else None,
        "recorded": recorded,
        "observed": stamp.isoformat(timespec="seconds"),
    }


# ----- harvest: pull evidence out, before any delete (R17 / D2) -------------------------------

#: The evidence set D2 names: the raw run log, the receipt, and the transcript. Subagent logs and
#: Stop-hook receipts are NOT ported here (HONEST LIMIT, module docstring): the in-container
#: epilogue that would write them next to these files is a separate, unbuilt surface. A file
#: absent on the remote is SKIPPED at harvest, not refused -- a stalled lane's partial evidence is
#: still worth capturing -- but only the files actually captured enter the manifest, and
#: `codespace_delete` gates on exactly that manifest, never on this constant.
HARVEST_FILES: tuple[str, ...] = ("run.log", "receipt.json", "handback.json", RUNNER_HANDBACK_FILE)

#: The platform's creation log, read from its FIXED remote path rather than from `workdir`, and kept
#: as `creation.log`. A run refused before it started (a recovery container, a failed creation --
#: b2-codespace-green run 1) has no run.log and no receipt, so without this the manifest lists
#: nothing and `codespace_delete` refuses: a billing box with no way out. The log is also the one
#: evidence of WHY the box was refused.
HARVEST_CREATION_LOG = "creation.log"

HARVEST_MANIFEST_NAME = "manifest.json"

#: D2's own default ("a durable PRIVATE location", proposed `~/.claude/remote-runs/<batch>/<lane>/`).
#: `lane-runtime-data-home` (the lane meant to ratify the telemetry home) FAILED this batch
#: (`to-browser/SESSION-integrator-wave5b-n4-2026-09-26.md`), so this is a DECIDED-BY-LANE choice
#: of "a gitignored path it names" (the contract's own fallback clause) rather than the ratified
#: home: outside `HUB_ROOT` entirely, so it is outside the public tree by construction, not merely
#: by a `.gitignore` line that a future `git add -f` could defeat.
DEFAULT_HARVEST_ROOT = Path.home() / ".claude" / "remote-runs"


def _harvest_dir(batch: str, lane: str, *, root: Optional[Path] = None) -> Path:
    return (root or DEFAULT_HARVEST_ROOT) / batch / lane


@dataclass(frozen=True)
class HarvestResult:
    ok: bool
    name: str = ""
    out_dir: Optional[Path] = None
    manifest_path: Optional[Path] = None
    files: dict = field(default_factory=dict)  # relative path -> sha256 hex
    commands: tuple[str, ...] = ()
    failure: str = ""


def codespace_harvest(name: str, *, batch: str, lane: str, workdir: str = "/workspaces/dispatch",
                       files: Sequence[str] = HARVEST_FILES, out_root: Optional[Path] = None,
                       force: bool = False, dry_run: bool = False,
                       invoker: Optional[Callable[[Sequence[str]], GhResult]] = None,
                       checkout_dir: str = "", transport_dir: Optional[Path] = None
                       ) -> HarvestResult:
    """R17 / D2's harvest leg: pull evidence out of a codespace via `ssh ... cat` -- ported from
    `Save-CodespaceLaneHarvest`, whose own docstring calls this "measured rather than preferred":
    `gh codespace cp` has failed this exact transport three distinct ways, where `ssh <name> cat
    <path>` fails visibly (an empty answer is visibly empty) instead of exiting 0 having written
    nothing. Writes each file plus a `manifest.json` of what was captured and its sha256 into a
    durable PRIVATE directory OUTSIDE the public tree; `codespace_delete` refuses without a
    verified copy of exactly that manifest.

    A file absent on the remote is skipped, not refused (see `HARVEST_FILES`'s docstring); an
    existing manifest is a REFUSAL without `force=True` -- the same doctrine as the PS verb's own
    `-Force` guard: a second harvest that silently replaced the first would destroy the only copy
    of a lane that may no longer exist to re-harvest from.
    """
    out_dir = _harvest_dir(batch, lane, root=out_root)
    manifest_path = out_dir / HARVEST_MANIFEST_NAME
    commands: list[str] = []

    def call(argv: Sequence[str]) -> GhResult:
        commands.append(format_gh_line(argv))
        return run_gh(argv, invoker=invoker)

    if manifest_path.exists() and not force:
        failure = f"{manifest_path} already exists -- pass force=True to replace it"
        if not dry_run:
            write_step(out_dir / "steps.jsonl", batch, lane, name, "harvest", False,
                       {"manifest_path": str(manifest_path), "files": {}}, failure)
        return HarvestResult(False, name=name, out_dir=out_dir, manifest_path=manifest_path,
                              failure=failure)

    if dry_run:
        for rel in files:
            commands.append(format_gh_line(["codespace", "ssh", "-c", name, "--",
                                             *_remote("cat", f"{workdir}/{rel}")]))
        commands.append(format_gh_line(["codespace", "ssh", "-c", name, "--",
                                         *_remote("cat", cs.CREATION_LOG_PATH)]))
        return HarvestResult(True, name=name, out_dir=out_dir, manifest_path=manifest_path,
                              commands=tuple(commands))

    out_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict = {}
    for rel in files:
        res = call(["codespace", "ssh", "-c", name, "--", *_remote("cat", f"{workdir}/{rel}")])
        if not res.ok:
            continue  # absent on the remote -- skipped, not refused (module docstring above)
        local = out_dir / rel
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_text(res.stdout, encoding="utf-8", newline="\n")
        manifest[rel] = hashlib.sha256(local.read_bytes()).hexdigest()

    session_rel = f"SESSION-{lane}.md"
    if checkout_dir and transport_dir is not None:
        src = f"{checkout_dir}/to-browser/{session_rel}"
        got = call(["codespace", "ssh", "-c", name, "--", *_remote("cat", src)])
        if not got.ok:
            # asked for, so a missing SESSION file is a refusal, never a skipped file (review 2, P1)
            failure = f"{session_rel}: the box could not be read at {src} (exit {got.exit_code})"
            write_step(out_dir / "steps.jsonl", batch, lane, name, "harvest", False,
                       {"manifest_path": str(manifest_path), "files": manifest}, failure)
            return HarvestResult(False, name=name, out_dir=out_dir, manifest_path=manifest_path,
                                 files=manifest, commands=tuple(commands), failure=failure)
        if got.ok:
            data = got.stdout.encode("utf-8")
            box, why = _box_size_and_hash(name, src, call)
            digest = hashlib.sha256(data).hexdigest()
            problem = ""
            if box is None:
                problem = why
            elif len(data) != box[0]:
                problem = f"{session_rel}: size mismatch -- box {box[0]} bytes, harvested {len(data)}"
            elif digest != box[1]:
                problem = f"{session_rel}: sha256 mismatch -- box {box[1]}, harvested {digest}"
            if not problem:
                local = out_dir / session_rel
                local.write_bytes(data)
                try:
                    # the operator named the directory, so its folder name is not policed here --
                    # the writer and the content lint still are
                    registry = [replace(k, folders=(*k.folders, "root")) if k.matches(session_rel) else k
                                for k in _transport.load_registry()]
                    landed = _transport.write("lane", Path(transport_dir) / session_rel, got.stdout,
                                              registry=registry)
                except (OSError, _transport.TransportWriteRefused) as exc:
                    problem = f"{session_rel}: the transport refused the session file ({exc})"
                else:
                    manifest[session_rel] = hashlib.sha256(landed.read_bytes()).hexdigest()
            if problem:
                (out_dir / session_rel).unlink(missing_ok=True)
                write_step(out_dir / "steps.jsonl", batch, lane, name, "harvest", False,
                           {"manifest_path": str(manifest_path), "files": manifest}, problem)
                return HarvestResult(False, name=name, out_dir=out_dir, manifest_path=manifest_path,
                                     files=manifest, commands=tuple(commands), failure=problem)

    log = call(["codespace", "ssh", "-c", name, "--", *_remote("cat", cs.CREATION_LOG_PATH)])
    if log.ok and log.stdout.strip():
        local = out_dir / HARVEST_CREATION_LOG
        local.write_text(log.stdout, encoding="utf-8", newline="\n")
        manifest[HARVEST_CREATION_LOG] = hashlib.sha256(local.read_bytes()).hexdigest()

    manifest_path.write_text(
        json.dumps({"name": name, "batch": batch, "lane": lane, "files": manifest},
                   indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
    if not manifest:
        # an empty manifest is still written (codespace_delete refuses on it) but is a FAILED
        # harvest: a caller that proceeds as if evidence were captured would lose the box's only copy
        commands.append("# nothing captured -- every named file was absent on the remote")
        failure = "nothing was captured -- every named file was absent on the remote"
        write_step(out_dir / "steps.jsonl", batch, lane, name, "harvest", False,
                   {"manifest_path": str(manifest_path), "files": manifest}, failure)
        return HarvestResult(False, name=name, out_dir=out_dir, manifest_path=manifest_path,
                             commands=tuple(commands), failure=failure)
    write_step(out_dir / "steps.jsonl", batch, lane, name, "harvest", True,
               {"manifest_path": str(manifest_path), "files": manifest})
    return HarvestResult(True, name=name, out_dir=out_dir, manifest_path=manifest_path,
                         files=manifest, commands=tuple(commands))


@dataclass(frozen=True)
class HarvestVerdict:
    ok: bool
    reason: str
    checked: tuple[str, ...] = ()


def verify_harvest_manifest(out_dir: Path, *, expected_name: Optional[str] = None) -> HarvestVerdict:
    """Re-check a harvest by RECOMPUTING every file's sha256 against `manifest.json` -- never
    trust a cached flag from the harvest call itself. Missing manifest, an empty one, a missing
    file, or a hash mismatch all refuse. `codespace_delete` calls this immediately before every
    delete and makes NO `gh` call at all when it refuses (R17).

    `expected_name`, when given, must match the manifest's own recorded `name` -- codex terra P1
    (2026-09-27): checking hashes alone verifies the EVIDENCE is intact but not that it is
    evidence OF the codespace about to be deleted; a valid manifest for A would otherwise
    authorize deleting any B passed as `--name`."""
    manifest_path = Path(out_dir) / HARVEST_MANIFEST_NAME
    if not manifest_path.exists():
        return HarvestVerdict(False, f"no harvest manifest at {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return HarvestVerdict(False, f"harvest manifest is not valid JSON: {exc}")
    if not isinstance(manifest, dict):
        return HarvestVerdict(False, f"{manifest_path} is not a JSON object")
    if expected_name is not None and manifest.get("name") != expected_name:
        return HarvestVerdict(False,
                              f"manifest is for {manifest.get('name')!r}, not {expected_name!r} "
                              "-- refusing to authorize deleting a different codespace")
    entries = manifest.get("files")
    if not entries:
        return HarvestVerdict(False, f"{manifest_path} lists no files -- nothing was captured")
    checked = []
    for rel, expected in entries.items():
        local = Path(out_dir) / rel
        if not local.exists():
            return HarvestVerdict(False, f"{rel} is in the manifest but missing on disk")
        actual = hashlib.sha256(local.read_bytes()).hexdigest()
        if actual != expected:
            return HarvestVerdict(False,
                                   f"{rel} hash mismatch -- manifest has {expected}, disk has {actual}")
        checked.append(rel)
    return HarvestVerdict(True, f"{len(checked)} file(s) verified against {manifest_path}",
                          tuple(checked))


# ----- stop: NOT delete ------------------------------------------------------------------------

@dataclass(frozen=True)
class StopResult:
    ok: bool
    name: str
    exit_code: int


def codespace_stop(name: str, *, invoker: Optional[Callable[[Sequence[str]], GhResult]] = None
                    ) -> StopResult:
    """`gh codespace stop` -- ported from `Stop-DispatchCodespace`. Stopping is NOT deleting: a
    stopped codespace ends compute billing and keeps billing storage until deleted."""
    res = run_gh(["codespace", "stop", "-c", name], invoker=invoker)
    return StopResult(ok=res.ok, name=name, exit_code=res.exit_code)


# ----- delete: refused until the harvest verifies (R17) ---------------------------------------

@dataclass(frozen=True)
class DeleteResult:
    ok: bool
    name: str
    refused: bool = False
    reason: str = ""
    exit_code: Optional[int] = None


def codespace_delete(name: str, *, out_dir: Path,
                      invoker: Optional[Callable[[Sequence[str]], GhResult]] = None,
                      batch: str = "", lane: str = "", receipts_root: Optional[Path] = None,
                      ledger_path: Optional[Path] = None) -> DeleteResult:
    """R17: delete a codespace only once `verify_harvest_manifest(out_dir)` passes.

    The PS module deliberately composes no `gh codespace delete` anywhere -- `deletion is
    destructive and stays an operator act` (`Stop-DispatchCodespace`'s own docstring). This
    function IS that act, now with a checked precondition: a missing manifest, an empty one, or a
    hash mismatch refuses WITHOUT calling `gh` at all, so a failed harvest can never be compounded
    by a destroyed codespace -- the retention period (D2's stop-then-delete belt) is what a
    refusal here leaves the operator to fall back on.

    With a `batch` and `lane` the outcome is also one `delete` step row, and a successful delete
    closes the regime ledger's open row for the box (uptime minutes included)."""
    steps_path = (_harvest_dir(batch, lane, root=receipts_root) / "steps.jsonl") if batch and lane else None
    verdict = verify_harvest_manifest(out_dir, expected_name=name)
    if not verdict.ok:
        if steps_path:
            write_step(steps_path, batch, lane, name, "delete", False,
                       {"refused": True, "exit_code": None, "reason": verdict.reason,
                        "uptime_minutes": None}, verdict.reason)
        return DeleteResult(False, name=name, refused=True, reason=verdict.reason)
    res = run_gh(["codespace", "delete", "-c", name, "--force"], invoker=invoker)
    if steps_path:
        minutes = None
        if res.ok:
            opened = next((r for r in regime.open_receipts(ledger_path) if r.get("codespace") == name), None)
            if opened and opened.get("created"):
                closed = regime.write_receipt(
                    lane, batch, name, created=datetime.fromisoformat(opened["created"]),
                    deleted=datetime.now(timezone.utc), machine=opened.get("machine", ""),
                    prebuild=bool(opened.get("prebuild")), tokens={}, ledger_path=ledger_path,
                    ready=opened.get("ready"), ready_reason=opened.get("ready_reason") or "",
                    end_reason="deleted via dispatch.py codespace-delete after a manifest-gated "
                               "harvest (hash-verified)")
                minutes = closed["uptime_minutes"]
        write_step(steps_path, batch, lane, name, "delete", res.ok,
                   {"refused": False, "exit_code": res.exit_code, "reason": verdict.reason,
                    "uptime_minutes": minutes},
                   "" if res.ok else f"delete exited {res.exit_code}")
    return DeleteResult(res.ok, name=name, refused=False, reason=verdict.reason,
                        exit_code=res.exit_code)


# ----- deliver + handback: the box is deleted only after the browser's bytes have landed ------------

@dataclass(frozen=True)
class DeliveryResult:
    ok: bool
    reason: str = ""
    delivered: dict = field(default_factory=dict)  # transport file name -> sha256 hex
    commands: tuple[str, ...] = ()


@dataclass(frozen=True)
class LifecycleResult:
    ok: bool
    deleted: bool = False
    reason: str = ""
    steps: tuple[str, ...] = ()


def _box_size_and_hash(name: str, src: str, call: Callable[[Sequence[str]], GhResult]
                       ) -> tuple[Optional[tuple[int, str]], str]:
    """`((bytes, sha256), "")` as the BOX reports them for `src`, or `(None, why)`."""
    quoted = shlex.quote(src)
    res = call(["codespace", "ssh", "-c", name, "--",
                *_remote("sh", "-c", f"wc -c < {quoted}; sha256sum {quoted}")])
    lines = res.stdout.split("\n") if res.ok else []
    try:
        return (int(lines[0].strip()), lines[1].split()[0]), ""
    except (ValueError, IndexError):
        return None, f"the box could not report the size and sha256 of {src} (exit {res.exit_code})"


def deliver_to_transport(name: str, *, lane: str, workdir: str, checkout_dir: str, transport_dir: Path,
                         stage_dir: Path, invoker: Optional[Callable[..., GhResult]] = None
                         ) -> DeliveryResult:
    """Copy the lane's SESSION file and run log out of the box into `transport_dir`, byte-identical.

    Transfer is `gh codespace cp` alone: no credential is placed in the box and nothing goes on a
    command's stdin. Each file is staged, then compared with what the BOX says it holds (byte length
    and sha256), then copied into the transport and re-hashed there. An empty, short or altered file,
    or a transport that cannot be written, is a refusal naming the file -- and a refusal is what keeps
    `codespace_handback` from deleting the box."""
    commands: list[str] = []
    transport_dir, stage_dir = Path(transport_dir), Path(stage_dir)
    if not lane or any(c in lane for c in "/\\") or ".." in lane:
        return DeliveryResult(False, f"lane {lane!r} is not a plain slug -- refusing to build a transport path from it",
                              {}, ())

    def call(argv: Sequence[str]) -> GhResult:
        commands.append(format_gh_line(argv))
        return run_gh(argv, invoker=invoker)

    def refuse(reason: str, delivered: Optional[dict] = None) -> DeliveryResult:
        return DeliveryResult(False, reason, delivered or {}, tuple(commands))

    if not transport_dir.is_dir():
        return refuse(f"transport directory {transport_dir} is missing or not a directory")
    plan = ((f"{checkout_dir}/to-browser/SESSION-{lane}.md", f"SESSION-{lane}.md"),
            (f"{workdir}/run.log", f"{lane}-run.log"))
    delivered: dict[str, str] = {}
    for src, target in plan:
        staged = stage_dir / target
        copied = call(["codespace", "cp", "-c", name, "-e", f"remote:{src}", str(staged)])
        if not copied.ok:
            return refuse(f"{target}: `gh codespace cp` of {src} exited {copied.exit_code}", delivered)
        box, why = _box_size_and_hash(name, src, call)
        if box is None:
            return refuse(f"{target}: {why}", delivered)
        try:
            data = staged.read_bytes()
        except OSError as exc:
            return refuse(f"{target}: the staged copy cannot be read ({exc})", delivered)
        if not data:
            return refuse(f"{target}: delivered file is empty", delivered)
        if len(data) != box[0]:
            return refuse(f"{target}: size mismatch -- box {box[0]} bytes, delivered {len(data)}", delivered)
        digest = hashlib.sha256(data).hexdigest()
        if digest != box[1]:
            return refuse(f"{target}: sha256 mismatch -- box {box[1]}, delivered {digest}", delivered)
        try:
            partial = transport_dir / (target + ".partial")
            partial.write_bytes(data)
            os.replace(partial, transport_dir / target)     # a reader never sees a half-written handback
            landed = hashlib.sha256((transport_dir / target).read_bytes()).hexdigest()
        except OSError as exc:
            return refuse(f"{target}: transport {transport_dir} is not writable ({exc})", delivered)
        if landed != digest:
            return refuse(f"{target}: sha256 mismatch in transport {transport_dir}", delivered)
        delivered[target] = digest
    return DeliveryResult(True, "", delivered, tuple(commands))


def codespace_handback(name: str, *, batch: str, lane: str, repo: str,
                       workdir: str = "/workspaces/dispatch", transport_dir: Path, out_root: Path,
                       receipts_root: Path, ledger_path: Optional[Path] = None,
                       invoker: Optional[Callable[..., GhResult]] = None,
                       sleep: Callable[[float], None] = lambda s: None) -> LifecycleResult:
    """Harvest, deliver, delete, verify teardown -- in that order, stopping at the first refusal.

    The delete is gated on the delivery: a box whose SESSION file or run log did not land in the
    transport byte-identical is NOT deleted (no `gh codespace delete` argv is ever issued), and the
    reason is returned. Teardown is verified by `gh codespace list --json name`, never assumed."""
    steps: list[str] = []

    def done(ok: bool, deleted: bool, reason: str) -> LifecycleResult:
        return LifecycleResult(ok, deleted, reason, tuple(steps))

    steps.append("harvest")
    prior = _harvest_dir(batch, lane, root=out_root)
    if (prior / HARVEST_MANIFEST_NAME).exists():
        # a retry after a failed delivery: the earlier harvest may be the only copy, so it is moved
        # aside (never overwritten) and this harvest lands in a fresh directory
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        try:
            prior.rename(prior.with_name(f"{prior.name}.prev-{stamp}"))
        except OSError as exc:
            return done(False, False, f"harvest failed: cannot set the earlier harvest aside ({exc})")
    harvested = codespace_harvest(name, batch=batch, lane=lane, workdir=workdir, out_root=out_root,
                                  invoker=invoker)
    if not harvested.ok:
        return done(False, False, f"harvest failed: {harvested.failure}")
    steps.append("deliver")
    with tempfile.TemporaryDirectory() as stage:
        delivery = deliver_to_transport(name, lane=lane, workdir=workdir,
                                        checkout_dir=f"/workspaces/{repo.rsplit('/', 1)[-1]}",
                                        transport_dir=Path(transport_dir), stage_dir=Path(stage),
                                        invoker=invoker)
    if not delivery.ok:
        return done(False, False, f"delivery failed, box NOT deleted: {delivery.reason}")
    steps.append("delete")
    removed = codespace_delete(name, out_dir=harvested.out_dir, invoker=invoker, batch=batch, lane=lane,
                               receipts_root=receipts_root, ledger_path=ledger_path)
    if not removed.ok:
        return done(False, False, f"delete failed: {removed.reason or removed.exit_code}")
    steps.append("verify-teardown")
    listed = run_gh(["codespace", "list", "--json", "name"], invoker=invoker)
    if not listed.ok:
        return done(False, True, f"teardown not verified: `gh codespace list` exited {listed.exit_code}")
    try:
        names = {str(row.get("name")) for row in json.loads(listed.stdout or "[]")}
    except (json.JSONDecodeError, AttributeError):
        return done(False, True, "teardown not verified: `gh codespace list` did not return JSON")
    if name in names:
        return done(False, True, f"{name} is still listed after delete")
    return done(True, True, "")


def codespace_lifecycle(repo: str, branch: str, slug: str, contract: Path, head_argv: Sequence[str], *,
                        batch: str, transport_dir: Path, out_root: Path, receipts_root: Path,
                        ledger_path: Optional[Path] = None,
                        invoker: Optional[Callable[..., GhResult]] = None,
                        workdir: str = "/workspaces/dispatch",
                        sleep: Callable[[float], None] = time.sleep, **exec_kwargs) -> LifecycleResult:
    """`codespace_exec`, then `codespace_handback` for whatever box exec named -- even a failed run
    leaves a box that is billing, so a name is always handed back. No name, no handback."""
    ran = codespace_exec(repo, branch, slug, contract, head_argv, batch=batch, workdir=workdir,
                         invoker=invoker, sleep=sleep, receipts_root=receipts_root,
                         ledger_path=ledger_path, **exec_kwargs)
    if not ran.name:
        return LifecycleResult(False, False, f"exec produced no box: {ran.failure}", ("exec",))
    back = codespace_handback(ran.name, batch=batch, lane=slug, repo=repo, workdir=workdir,
                              transport_dir=transport_dir, out_root=out_root,
                              receipts_root=receipts_root, ledger_path=ledger_path, invoker=invoker)
    reason = back.reason or ("" if ran.ok else f"exec failed: {ran.failure}")
    return LifecycleResult(ran.ok and back.ok, back.deleted, reason, ("exec", *back.steps))


@cli.command("codespace-exec")
@click.argument("contract", type=click.Path(path_type=Path))
@click.option("--repo", required=True, help="owner/name.")
@click.option("--branch", default="main", show_default=True)
@click.option("--slug", required=True, help="Lane slug; also the codespace's -d display name.")
@click.option("--argv-json", required=True,
              help="JSON list -- the head argv, e.g. `plan --substrate codespace`'s own `argv` field.")
@click.option("--machine", default="standardLinux32gb", show_default=True)
@click.option("--idle-timeout", default="240m", show_default=True)
@click.option("--retention", default="24h", show_default=True)
@click.option("--batch", required=True, help="The batch id: step rows and the regime receipt are keyed by it.")
@click.option("--workdir", default="/workspaces/dispatch", show_default=True)
@click.option("--agy-signin-wait-s", type=float, default=AGY_SIGNIN_WAIT_S, show_default=True,
              help=f"How long to wait for the operator's agy sign-in code (0..{AGY_SIGNIN_WAIT_S}).")
def codespace_exec_cmd(contract: Path, repo: str, branch: str, slug: str, argv_json: str,
                       machine: str, idle_timeout: str, retention: str, batch: str, workdir: str,
                       agy_signin_wait_s: float) -> None:
    """Actually dispatch a Codespace lane end to end: create, ship, run, pull the receipt back.

    `--argv-json` is deliberately not re-derived from the contract here -- `dispatch.py plan
    --substrate codespace` already computes it (model/effort table, provider) and this command
    executes what that one planned, matching the file's own "plan starts nothing, exec does"
    split."""
    _refuse_malformed_batch(slug, batch)
    _require_contract_file(contract)
    try:
        head_argv = json.loads(argv_json)
    except json.JSONDecodeError as exc:
        raise DispatchRefused(f"--argv-json did not parse: {exc}") from exc
    if not isinstance(head_argv, list) or not all(isinstance(a, str) for a in head_argv):
        raise DispatchRefused("--argv-json must be a JSON list of strings")
    if not head_argv:
        raise DispatchRefused("--argv-json is empty -- nothing to run in the codespace")
    if not 0 <= agy_signin_wait_s <= AGY_SIGNIN_WAIT_S:
        raise DispatchRefused(f"--agy-signin-wait-s must be between 0 and {AGY_SIGNIN_WAIT_S} seconds")
    # P1-B04: the Codespace path runs the SAME `moment:pre-launch` the local `launch` runs, BEFORE
    # `gh codespace create` -- a refusal here means no gh call was made and nothing is running. The
    # model the lane will actually run is the `--model` of the planned head argv, when it names one.
    # The request is built here, not by `request_from_contract`: that REFUSES a contract it cannot
    # parse, whereas the contract is the organ's to judge (and its refusal names the role and models).
    planned = planned_model(head_argv)
    request = LaunchRequest(slug=slug, provider="anthropic", model=planned, effort="",
                            permission_mode="bypassPermissions", contract=Path(contract).resolve(),
                            batch=batch)
    try:
        outcome = run_prelaunch(request)
    except Exception as exc:  # noqa: BLE001 -- a pre-launch that could not run is a REFUSAL, never a pass
        raise LaunchRefused(f"pre-launch could not run for {slug}: {type(exc).__name__}: {exc}") from exc
    if not outcome.passed:
        raise LaunchRefused(f"pre-launch refused {slug}: {outcome.reason}")
    # the launcher always mirrors the laptop's own sign-ins (R87): this verb is the launcher
    result = codespace_exec(repo, branch, slug, Path(contract), head_argv, machine=machine,
                            idle_timeout=idle_timeout, retention=retention, workdir=workdir,
                            mirror=default_mirror_config(), batch=batch,
                            schema_smoke=run_schema_smoke, pins=branch_pin_check,
                            agy_wait_s=agy_signin_wait_s)
    click.echo(json.dumps(asdict(result)))
    if not result.ok:
        sys.exit(EXIT_NO_COMMIT if result.fate.get("step") == "commit" else EXIT_REFUSED)


@cli.command("codespace-observe")
@click.option("--name", required=True, help="Codespace NAME (gh codespace list -> name).")
@click.option("--workdir", default="/workspaces/dispatch", show_default=True)
@click.option("--expected-gone", is_flag=True,
              help="This line deleted the codespace: absence is the clean end (TORN-DOWN).")
@click.option("--unreachable-for-s", type=float, default=0.0, show_default=True,
              help="An override for a caller with a longer unreachable clock of its own; with "
                   "--slug the line derives the duration itself, from the stamp it stored.")
@click.option("--slug", required=True,
              help="The lane's slug: every fate TRANSITION is recorded in the regime ledger "
                   "(`write_fate`) and the unreachable clock runs from its stored stamp -- the "
                   "line never reads a lane unrecorded.")
@click.option("--ledger", "ledger", type=click.Path(path_type=Path), default=None,
              help=f"Default: {regime.RECEIPT_LEDGER_RELPATH}.")
def codespace_observe_cmd(name: str, workdir: str, expected_gone: bool,
                          unreachable_for_s: float, slug: str,
                          ledger: Optional[Path]) -> None:
    """Read a Codespace lane once: state, progress, fate. Starts nothing; appends the fate row
    when the fate changed (the only write)."""
    click.echo(json.dumps(codespace_observe(name, workdir=workdir, expected_gone=expected_gone,
                                            unreachable_for_s=unreachable_for_s, slug=slug,
                                            ledger_path=ledger)))


@cli.command("codespace-harvest")
@click.option("--name", required=True, help="Codespace NAME (gh codespace list -> name).")
@click.option("--batch", required=True)
@click.option("--lane", required=True)
@click.option("--workdir", default="/workspaces/dispatch", show_default=True)
@click.option("--out-root", type=click.Path(path_type=Path), default=None,
              help="Default: ~/.claude/remote-runs -- outside the public tree (R17).")
@click.option("--force", is_flag=True, help="Replace an existing manifest for this batch/lane.")
@click.option("--dry-run", is_flag=True)
@click.option("--deliver/--no-deliver", default=False, show_default=True,
              help="Run the full handback: harvest, deliver to the transport, delete, verify teardown.")
@click.option("--transport-dir", type=click.Path(path_type=Path), default=None,
              help="Where --deliver lands the SESSION file and run log. Default: "
                   "$CLAUDE_PROMPTS_DIR/to-browser.")
@click.option("--repo", default="rdwornik/.dev-knowledge", show_default=True,
              help="owner/name -- names the box's checkout (/workspaces/<name>) for --deliver.")
@click.option("--checkout-dir", default="", show_default=True,
              help="The box's checkout; with --transport-dir (no --deliver) the harvest also copies "
                   "and hash-verifies to-browser/SESSION-<lane>.md into the transport.")
def codespace_harvest_cmd(name: str, batch: str, lane: str, workdir: str,
                          out_root: Optional[Path], force: bool, dry_run: bool, deliver: bool,
                          transport_dir: Optional[Path], repo: str, checkout_dir: str) -> None:
    """Pull evidence out of a codespace and write the manifest `codespace-delete` gates on.

    With `--deliver` the whole handback runs: the box is deleted only once its SESSION file and run
    log have landed in the transport byte-identical, and a refusal is printed to stderr."""
    if deliver and dry_run:
        raise DispatchRefused("--deliver cannot be combined with --dry-run: the handback deletes the box")
    if deliver:
        if transport_dir is None:
            prompts = os.environ.get("CLAUDE_PROMPTS_DIR")
            if not prompts:
                raise DispatchRefused("--deliver needs --transport-dir or CLAUDE_PROMPTS_DIR set: "
                                      "there is no default transport to invent")
            transport_dir = Path(prompts) / "to-browser"
        back = codespace_handback(name, batch=batch, lane=lane, repo=repo, workdir=workdir,
                                  transport_dir=transport_dir,
                                  out_root=out_root or DEFAULT_HARVEST_ROOT,
                                  receipts_root=out_root or DEFAULT_HARVEST_ROOT)
        click.echo(json.dumps(asdict(back)))
        if not back.ok:
            click.echo(f"[codespace] NOT COMPLETE -- {back.reason}", err=True)
            sys.exit(EXIT_REFUSED)
        return
    result = codespace_harvest(name, batch=batch, lane=lane, workdir=workdir, out_root=out_root,
                               force=force, dry_run=dry_run, checkout_dir=checkout_dir,
                               transport_dir=transport_dir)
    click.echo(json.dumps({
        "ok": result.ok, "name": result.name, "out_dir": str(result.out_dir),
        "manifest_path": str(result.manifest_path), "files": result.files,
        "commands": list(result.commands), "failure": result.failure}))
    if not result.ok:
        sys.exit(EXIT_REFUSED)


@cli.command("codespace-stop")
@click.option("--name", required=True)
def codespace_stop_cmd(name: str) -> None:
    """`gh codespace stop` -- NOT delete. See `codespace-delete` for the gated delete leg."""
    result = codespace_stop(name)
    click.echo(json.dumps(asdict(result)))
    if not result.ok:
        sys.exit(EXIT_REFUSED)


@cli.command("codespace-delete")
@click.option("--name", required=True)
@click.option("--batch", required=True)
@click.option("--lane", required=True)
@click.option("--out-root", type=click.Path(path_type=Path), default=None)
def codespace_delete_cmd(name: str, batch: str, lane: str, out_root: Optional[Path]) -> None:
    """Delete a codespace -- refused unless `codespace-harvest`'s manifest verifies (R17)."""
    out_dir = _harvest_dir(batch, lane, root=out_root)
    result = codespace_delete(name, out_dir=out_dir, batch=batch, lane=lane, receipts_root=out_root)
    click.echo(json.dumps(asdict(result)))
    if result.refused:
        click.echo(f"[codespace] REFUSED -- {result.reason}", err=True)
        sys.exit(EXIT_REFUSED)
    if not result.ok:
        sys.exit(EXIT_REFUSED)


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
              help="The integrator's own session receipt (to-browser/SESSION-integrator-<batch>.md), "
                   "or any text carrying its `STATE <lane> MERGED|REFUSED|WAITING|FAILED|REPORTED "
                   "<sha|-> <time> <min>` lines. Default: none -- every dependency reads WAITING.")
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
    -- `dispatch.py launch` refuses that head by design; use the codespace verb for it. A re-run
    is idempotent ([#1572]): a lane already launched is reported `already-launched` (exit stays 0,
    the pass goes on) and a lane the --state-file reads MERGED is `SKIP-MERGED`, never refired."""
    _refuse_malformed_batch("queue", batch or os.environ.get("HARNESS_BATCH", ""))
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

    already_reasons: dict[str, str] = {}

    def launch_or_report(slug: str) -> None:
        """`do_launch`, but an already-launched lane (found by `launch_lane`'s own collision check,
        which sees what the listing alone does not) is RECORDED and re-raised for the caller to step
        over -- a fact about one lane, not a reason to stop the pass ([#1572]). Any other refusal
        still propagates (exit 5)."""
        try:
            do_launch(slug)
        except AlreadyLaunched as exc:
            already_reasons[slug] = exc.message
            raise

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
                             on_fire=launch_or_report, states_fn=states_fn, live_slugs_fn=live_slugs,
                             local_live_count_fn=local_live_count, free_mb_fn=mag.free_memory_mb,
                             local_cap=cap, floor_mb=floor_mb)
        for slug in result.already_launched:
            click.echo(f"[queue] already-launched {slug}: "
                       f"{already_reasons.get(slug) or 'a live lane of this slug is in the agent listing'}")
        pending = [s for s in order if s not in result.terminal]
        click.echo(f"[queue] watch ended after {result.polls} poll(s): fired {len(result.fired)}, "
                   f"held-failed {len(result.held_failed)}, routed-codespace "
                   f"{len(result.routed_codespace)}, skipped-merged {len(result.skipped_merged)}, "
                   f"already-launched {len(result.already_launched)}, of {len(order)}; "
                   f"{'DEADLINE -- still pending: ' + ', '.join(pending) if result.expired else 'all clear'}")
        return

    decisions = plan_pass(lanes, order, fired=(), states=states_fn(), live_slugs=live_slugs(),
                          local_cap=cap, local_live_count=local_live_count(),
                          free_mb=mag.free_memory_mb(), floor_mb=floor_mb)
    for decision in decisions:
        if decision.action == ACTION_FIRE:
            try:
                launch_or_report(decision.slug)
            except AlreadyLaunched:
                click.echo(f"[queue] already-launched {decision.slug}: {already_reasons[decision.slug]}")
        else:
            click.echo(f"[queue] {decision.action} {decision.slug}: {decision.reason}")


@cli.command("repair")
@click.argument("slug")
@click.argument("contract", type=click.Path(path_type=Path))
@click.option("--attempt", type=int, default=1, show_default=True)
@click.option("--model", required=True)
@click.option("--effort", required=True)
@click.option("--permission-mode", default="bypassPermissions", show_default=True)
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path), default=HUB_ROOT,
              show_default=True)
@click.option("--batch", default="", help="The batch the lane belongs to, `E<major>.<minor>` (e.g. E2.0); "
                                          "pre-launch judges it and the launch receipt records it. Default: "
                                          "$HARNESS_BATCH, then the lane's LAUNCH receipt; none of the three, "
                                          "or an id outside that grammar, is a refusal.")
def repair_cmd(slug: str, contract: Path, attempt: int, model: str, effort: str,
              permission_mode: str, repo_root: Path, batch: str) -> None:
    """Relaunch a REPAIR of SLUG into its EXISTING worktree -- never a fresh `--worktree`.
    Refuses when that worktree is not there (starting one is a fresh launch's job). Runs the same
    `pre-launch` moment a launch runs and writes the same LAUNCH receipt (`kind: repair`)."""
    batch = batch or os.environ.get("HARNESS_BATCH", "") or _launched_batch(slug)
    _refuse_malformed_batch(slug, batch)
    _require_contract_file(contract)
    request = RepairRequest(slug=slug, attempt=attempt, model=model, effort=effort,
                            contract=Path(contract).resolve(), permission_mode=permission_mode,
                            batch=batch)
    spawned = repair_lane(request, repo_root=Path(repo_root))
    click.echo(f"[dispatch] repair {request.session_name} spawned: {_tail(spawned.stdout, 300)}")


@cli.command("successor")
@click.argument("slug")
@click.argument("contract", type=click.Path(path_type=Path))
@click.option("--base", required=True, help="The ref or sha the lane's worktree is cut from.")
@click.option("--batch", default="", help="The batch the lane belongs to, `E<major>.<minor>`. Default: "
                                          "$HARNESS_BATCH; absent or outside that grammar is a refusal.")
@click.option("--model", required=True)
@click.option("--effort", required=True)
@click.option("--permission-mode", default="bypassPermissions", show_default=True)
@click.option("--repo-root", type=click.Path(file_okay=False, path_type=Path), default=HUB_ROOT,
              show_default=True)
def successor_cmd(slug: str, contract: Path, base: str, batch: str, model: str, effort: str,
                  permission_mode: str, repo_root: Path) -> None:
    """Start SLUG as a FIRST-RUN lane in a fresh worktree cut from --base, not main's tip. Runs the
    same `pre-launch` moment a launch runs (before the worktree exists) and writes the LAUNCH receipt
    (`kind: successor`, with the resolved base sha)."""
    batch = batch or os.environ.get("HARNESS_BATCH", "")
    _refuse_malformed_batch(slug, batch)
    _require_contract_file(contract)
    request = SuccessorRequest(slug=slug, contract=Path(contract).resolve(), base=base, batch=batch,
                               model=model, effort=effort, permission_mode=permission_mode)
    spawned = successor_lane(request, repo_root=Path(repo_root))
    click.echo(f"[dispatch] successor {request.session_name} spawned: {_tail(spawned.stdout, 300)}")


if __name__ == "__main__":  # pragma: no cover
    cli()
