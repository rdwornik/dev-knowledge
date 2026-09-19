#!/usr/bin/env python
"""dispatch.py -- PLAN one lane and GOVERN it under a TOKEN CAP that is enforced, not requested.

WHY. Four sessions were ordered 180k tokens and used ~845k. A budget written into a prompt caps
nothing: the session has no instrument for its own spend. The cap therefore lives HERE, in the
governor, which is the one place that can see the spend from outside and can stop the lane.

THE SPLIT (wave 3, operator ruling 2026-09-19, protocols/BUILD-LIST.md "Dispatch / Layer 2"):
THE HUB SHIPS THE CODE, THE CALLER RUNS IT. CLAUDE.md section 5 rule 4 says Layer 2 never
executes -- no script drives state in a child repo -- and a launcher that starts a
workspace-writing lane in whatever repo invokes it is exactly that. So this module NEVER spawns a
lane. It has two verbs, and a thin caller-side shim (`templates/dispatch-shim.ps1`) does the
spawning between them, from the CALLER's repo root:

  plan     contract -> a JSON plan (argv, env delta, model/effort FROM THE CONTRACT); every
           pre-launch refusal fires here, before anything exists to clean up
  govern   lane id  -> bind the lane's own usage by SESSION ID, poll it, STOP the lane past the
           cap, and witness that a finished lane committed something

`claude stop`, `claude agents` and `git` are control-plane calls this module still makes; none of
them starts a lane.

THE CAP CANNOT BE LEFT OFF. A launch whose usage cannot be bound, or that runs over its cap, is
REFUSED and its lane STOPPED -- never left running and reported as ungoverned. (Before this split
a default `--bg` launch read no usage without `--slug-dir` and went UNGOVERNED after 8 polls: it
failed loud but did not cap.)

THIS STARTED AS A MOVE PLUS A LANGUAGE REWRITE, not a new design. Prior art, read before writing:

  win-tooling/scripts/dev-terminals/bin/dispatch.ps1        `dispatch <file>` entry (77 lines)
  win-tooling/scripts/dispatch/Invoke-Dispatch.ps1          contract flow, Assert-ClaudeCommand (565)
  win-tooling/config/dispatch-helpers/DispatchHelpers.psm1  Start-DispatchLane, Start-DispatchCodespace,
                                                            Get-CloudModelProvider, Start-CloudModelSession (3964)

WHAT MOVED (each is a port, with the PS function it came from):
  resolve_contract / prompts_dir  <- Resolve-DispatchPromptFile / Get-DispatchPromptsDir
  build_plan (claude, --bg)       <- Start-DispatchLane (the ruled lane line; effort map; bypass)
  branch_guard                    <- Start-DispatchLane guard 1 (skip if worktree-<slug> exists)
  PROVIDERS / child_env           <- Get-CloudModelProvider / Start-CloudModelSession (scrub + route)
  codespace_plan                  <- Start-DispatchCodespace steps 2-5 (create, ship in, run, receipt)

WHAT CHANGED ON PURPOSE, and why it is not a new design:
  * The head program is chosen by `--provider`, never by a contract. `Assert-ClaudeCommand` refused
    every head but `claude` because a `## Dispatch` block could name the program; here the block is
    not read at all, so the refusal is structural and `codex` is admitted as a provider.
  * MODEL AND EFFORT COME FROM THE CONTRACT's `| Model | Mode | Effort |` table, or an explicit
    flag -- never a default (`[#717]`). A contract with neither is REFUSED.
  * The child environment is a dict delta in the plan, so the PS `finally` that restored
    ANTHROPIC_BASE_URL has nothing to restore: the operator's shell is never touched.
  * No `Invoke-Expression`, no shell string: every command is an argv list.

WHAT DID NOT MOVE (left in win-tooling; see the audit for the list and the shim content):
  the cloud (Anthropic-hosted) substrate, harvest, Start-DispatchAfter, the deep-code wrapper,
  and Invoke-Dispatch's derived-line fallback. None of those is on the cap's path.

THE CAP, and its honest limits:
  * REQUIRED, no default. Counts input + output + cache-write; cache READS are excluded unless
    `--count-cache-reads` (they run to millions on a 100k context and would make any cap void).
  * `claude --bg` lanes: `govern` reads the lane's session id and cwd from `claude agents --json`
    and reads that ONE session's transcript by id (`lane_cost.seat_usage`) -- no slug matching, no
    `--slug-dir`. It runs `claude stop <id>` past the cap. It is a POLL: a lane can overshoot by
    one interval of work, and by the message in flight (a cap of 5 stopped a lane at 22,471).
  * Unobservable spend is not "under cap": a lane that cannot be bound, or whose transcript stays
    unreadable, is STOPPED and the exit code is a refusal. Ctrl-C stops the lane too.
  * Stream-metered lanes (codex, `claude -p`) have the metering primitive here (`meter_lines`) but
    NO caller-side spawner yet -- the shim refuses them. codex reports usage only in
    `turn.completed`, so it is POST-HOC PER TURN; Anthropic stream-json reports thinking tokens
    only in the final `result` event.
"""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Mapping, Optional, Sequence

import click

try:  # pragma: no cover -- exercised by whichever path the caller uses
    from scripts import lane_cost as lc
except ImportError:  # pragma: no cover
    import lane_cost as lc

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("dispatch")

EXIT_CAP_EXCEEDED = 3
EXIT_UNGOVERNED = 4       # the cap was NOT enforced and the lane may still be running
EXIT_REFUSED = 5          # usage could not be bound: the lane was STOPPED (or had already ended)
EXIT_NO_COMMIT = 6        # finished under cap but committed nothing -- FAILED, not DONE
EXIT_UNWITNESSED = 7      # finished under cap; whether it committed could not be established

EFFORTS = {"l": "low", "low": "low", "m": "medium", "med": "medium", "medium": "medium",
           "h": "high", "high": "high", "x": "xhigh", "xhigh": "xhigh", "max": "max"}
SUBSTRATES = ("local", "codespace")
_ANTHROPIC_CREDS = ("ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN")


class DispatchRefused(click.ClickException):
    """A launch this module will not perform. Carries the fix in its message."""


# --- the cap -----------------------------------------------------------------------------

def validate_cap(cap: int) -> int:
    if not isinstance(cap, int) or cap <= 0:
        raise DispatchRefused(f"token cap must be a positive integer, got {cap!r} -- a lane with "
                              "no cap is the failure this launcher exists to end")
    return cap


def capped_tokens(usage: "lc.TokenUsage", count_cache_reads: bool = False) -> int:
    used = usage.input_tokens + usage.output_tokens + usage.cache_write_tokens
    return used + (usage.cache_read_tokens if count_cache_reads else 0)


class GovernorBlind(RuntimeError):
    """The governor cannot observe the lane (status probe failed). NOT evidence it finished."""


@dataclass(frozen=True)
class Verdict:
    exceeded: bool
    used: int
    cap: int
    polls: int = 0
    ungoverned: str = ""      # why the cap could not be enforced; "" when it could
    stop_failed: bool = False
    child_exit: int = 0       # a streamed child's own non-zero exit, never masked as success
    refused: bool = False     # the lane was unobservable and was STOPPED for it

    @property
    def exit_code(self) -> int:
        if self.stop_failed:
            return EXIT_UNGOVERNED
        if self.refused:
            return EXIT_REFUSED
        if self.ungoverned:
            return EXIT_UNGOVERNED
        if self.exceeded:
            return EXIT_CAP_EXCEEDED
        return self.child_exit


def _refuse(why: str, used: int, cap: int, polls: int, stop: Callable[[], Optional[bool]]) -> Verdict:
    """An unobservable lane is STOPPED. Leaving it running and saying so is the failure this
    launcher exists to end: a report is not a cap. If the stop itself fails the lane may still be
    running, and that is the one case reported as UNGOVERNED."""
    failed = stop() is False
    return Verdict(False, used, cap, polls, ungoverned=why, stop_failed=failed, refused=not failed)


def govern(*, cap: int, read_usage: Callable[[], Optional["lc.TokenUsage"]],
           stop: Callable[[], Optional[bool]],
           sleep: Callable[[float], None] = time.sleep, interval: float = 15.0,
           max_polls: Optional[int] = None, alive: Callable[[], bool] = lambda: True,
           count_cache_reads: bool = False, blind_polls: int = 8) -> Verdict:
    """Poll a running lane; STOP it the first time it is past `cap`.

    `read_usage` returns None when the spend cannot be observed (no transcript yet / at all):
    after `blind_polls` in a row the lane is STOPPED and REFUSED, never assumed to be at zero
    spend and never left running. `stop` returning False is a stop that did not happen.
    `alive` raising GovernorBlind is an unreadable status probe, not a finished lane: the lane
    is stopped for that too. A lane that ENDS while its usage was unreadable has nothing left to
    stop, so it is reported UNGOVERNED (its final spend was never observed)."""
    validate_cap(cap)
    polls, used, blind = 0, 0, 0
    while True:
        usage = read_usage()
        if usage is None:
            blind += 1
            if blind >= blind_polls:
                return _refuse(f"no readable usage for {blind} polls", used, cap, polls + 1, stop)
        else:
            blind = 0
            used = capped_tokens(usage, count_cache_reads)
            if used > cap:
                return Verdict(True, used, cap, polls + 1, stop_failed=(stop() is False))
        polls += 1
        try:
            done = not alive()
        except GovernorBlind as exc:
            return _refuse(str(exc), used, cap, polls, stop)
        if (max_polls is not None and polls >= max_polls) or done:
            # the last read was blind: the final spend was never observed -- not "under cap".
            # The lane has ENDED, so nothing is left to stop: it is REFUSED (exit 5), which keeps
            # exit 4 meaning exactly one thing -- the lane may still be running.
            return Verdict(False, used, cap, polls,
                           ungoverned=(f"lane ended after {blind} unreadable usage poll(s); "
                                       "final spend never observed") if blind else "",
                           refused=bool(blind))
        sleep(interval)


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

    The `## Dispatch` block is deliberately NOT read: it is the arbitrary-execution surface
    `Assert-ClaudeCommand` existed to fence. A contract with no parseable table, an empty model,
    or an effort outside the enum is REFUSED -- the alternative is a default, and a default
    silently re-decides the most expensive constant on the line."""
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


# --- the plan ------------------------------------------------------------------------------

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
    # --permission-mode is not optional: nobody is at a --bg lane's keyboard, so a prompt is a
    # silent stall that looks exactly like a slow lane.
    argv = ["claude", "--bg", "--model", model, "--effort", eff, "--permission-mode",
            permission_mode, "--worktree", slug, prompt]
    return Plan(argv, "transcript")


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


# --- stream metering (codex, codespace) ----------------------------------------------------

def usage_from_stream_line(line: str, seen: set[str]) -> Optional["lc.TokenUsage"]:
    """One event's usage, or None. Anthropic `assistant` events repeat per message id; codex
    reports `turn.completed`. The cumulative `result` event is handled by the caller."""
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


def meter_lines(lines: Iterable[str], cap: int, terminate: Callable[[], bool],
                count_cache_reads: bool = False) -> Verdict:
    """Meter a lane's stdout as it arrives; TERMINATE it the moment it is past `cap`.

    THE HUB METERS, THE CALLER OWNS THE PROCESS: `terminate` is the caller's callback (it returns
    True when the child is verified gone), because this module starts no lane and so cannot stop
    one it does not own. There is no caller-side spawner for stream lanes yet (the shim refuses
    them) -- this is the metering half, kept tested so it does not have to be re-derived."""
    total, seen, polls, observed = lc.TokenUsage(), set(), 0, False
    for line in lines:
        polls += 1
        try:
            usage = usage_from_stream_line(line, seen)
        except (ValueError, TypeError, OverflowError) as exc:  # not a (finite) number: stop, never abandon
            stopped = terminate()
            return Verdict(False, capped_tokens(total, count_cache_reads), cap, polls,
                           ungoverned=f"malformed usage in the stream ({exc}); child stopped",
                           stop_failed=not stopped)
        if usage is not None:
            observed = True
            total = total + usage
        used = capped_tokens(total, count_cache_reads)
        if used > cap:
            return Verdict(True, used, cap, polls, stop_failed=not terminate())
    blind = "" if observed else "the stream carried no parseable usage event"
    return Verdict(False, capped_tokens(total, count_cache_reads), cap, polls, ungoverned=blind)


# --- the control plane: binding, stopping, liveness (none of it starts a lane) ---------------

_ENDED = frozenset({"done", "stopped", "failed", "error", "exited", "cancelled", "canceled"})


@dataclass(frozen=True)
class LaneBinding:
    """A `--bg` lane's own identity: the session id its transcript is filed under, and its cwd."""
    session_id: str
    cwd: str


def _control(argv: list[str]) -> Optional["subprocess.CompletedProcess"]:
    """A bounded control-plane call; None when it hung or could not run."""
    try:
        return subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=30)
    except (subprocess.TimeoutExpired, OSError):
        return None


def stop_lane(lane_id: str) -> bool:
    done = _control(["claude", "stop", lane_id])
    return done is not None and done.returncode == 0


def _agents() -> list[dict]:
    """`claude agents --json` as a list of records; GovernorBlind when it cannot be read."""
    listing = _control(["claude", "agents", "--json"])
    if listing is None or listing.returncode != 0 or not listing.stdout.strip():
        raise GovernorBlind("`claude agents --json` failed, hung or was empty")
    try:
        data = json.loads(listing.stdout)
    except ValueError as exc:
        raise GovernorBlind(f"`claude agents --json` was not JSON ({exc})") from exc
    if not isinstance(data, list):
        raise GovernorBlind("`claude agents --json` was not a list")
    return [entry for entry in data if isinstance(entry, dict)]


def _find_agent(agents: Sequence[dict], lane_id: str) -> Optional[dict]:
    """The record for `lane_id` -- its short id, or a prefix of its session id."""
    for entry in agents:
        if str(entry.get("id") or "") == lane_id or (
                lane_id and str(entry.get("sessionId") or "").startswith(lane_id)):
            return entry
    return None


def bind_lane(lane_id: str) -> Optional[LaneBinding]:
    """Bind a launched lane to ITS OWN session id, from the listing -- no `--slug-dir`, no slug.

    A `--bg` lane files its transcript under a directory named for its cwd, and the launching
    session's directory is a different one; slug matching had to guess between them (the move
    audit's one finding only partly closed). The listing states the session id outright, and a
    transcript is `<session-id>.jsonl` in whichever directory it landed. None when the lane is not
    listed or carries no session id -- unbound, which the caller must treat as REFUSED."""
    try:
        entry = _find_agent(_agents(), lane_id)
    except GovernorBlind:
        return None
    session_id = str((entry or {}).get("sessionId") or "")
    if not session_id:
        return None
    return LaneBinding(session_id, str((entry or {}).get("cwd") or ""))


def find_lane_by_slug(slug: str) -> Optional[str]:
    """The id of the ONE live lane whose cwd is `.../worktrees/<slug>`, else None.

    For a launch whose output carried no readable id: the listing names each lane's cwd, and a
    `--bg --worktree` lane's cwd is its worktree. Ambiguity (two live lanes for one slug) is None,
    never a guess -- stopping the wrong lane is worse than reporting that this one was not found."""
    try:
        agents = _agents()
    except GovernorBlind:
        return None
    suffix = f"/worktrees/{slug}".lower()
    live = [e for e in agents
            if str(e.get("cwd") or "").replace("\\", "/").rstrip("/").lower().endswith(suffix)
            and str(e.get("state") or "").lower() not in _ENDED and e.get("id")]
    return str(live[0]["id"]) if len(live) == 1 else None


def lane_alive(lane_id: str) -> bool:
    """False once the lane has ENDED. A finished `--bg` lane stays LISTED with state `done`, so
    "is it in the listing" is not liveness. Absent from the listing is ended too."""
    entry = _find_agent(_agents(), lane_id)
    return entry is not None and str(entry.get("state") or "").lower() not in _ENDED


def _session_reader(session_id: str,
                    sessions_root: Optional[Path] = None) -> Callable[[], Optional["lc.TokenUsage"]]:
    def read() -> Optional["lc.TokenUsage"]:
        try:
            models = lc.seat_usage(session_id, sessions_root)
        except Exception as exc:  # noqa: BLE001 -- ANY read failure is unobservable spend, and the
            # governor turns that into a stop; an exception here would end the governor while the
            # lane it is capping kept running
            logger.warning("transcript for session %s unreadable: %s: %s", session_id,
                           type(exc).__name__, exc)
            return None
        if not models:  # no transcript found: unobservable, NOT zero
            return None
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
    """Plan a lane and govern it under an enforced token cap. Never spawns one."""


@cli.command("plan")
@click.argument("contract")
@click.option("--slug", default="", help="Lane slug; default: LANE-<slug>.md from the file name.")
@click.option("--provider", default="anthropic", show_default=True)
@click.option("--model", default="", help="Overrides the contract's Model cell. No default.")
@click.option("--effort", default="", help="Overrides the contract's Effort cell. No default.")
@click.option("--substrate", type=click.Choice(SUBSTRATES), default="local", show_default=True)
@click.option("--token-cap", "token_cap", type=int, required=True,
              help="REQUIRED. Tokens (input+output+cache-write) after which the lane is stopped.")
@click.option("--repo", default="", help="owner/name; the codespace substrate only.")
@click.option("--branch", default="main", show_default=True)
@click.option("--secrets-file", type=click.Path(path_type=Path),
              default=Path.home() / "Documents" / ".secrets" / ".env", show_default=True)
@click.option("--emit-env", is_flag=True,
              help="Include the env delta's VALUES (the shim passes this; a human should not).")
def plan_cmd(contract: str, slug: str, provider: str, model: str, effort: str, substrate: str,
             token_cap: int, repo: str, branch: str, secrets_file: Path, emit_env: bool) -> None:
    """Print the launch plan as JSON. Every pre-launch refusal fires here."""
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


@cli.command("govern")
@click.argument("lane_id", required=False, default="")
@click.option("--slug", required=True, help="Lane slug; its branch is worktree-<slug>.")
@click.option("--token-cap", "token_cap", type=int, required=True,
              help="REQUIRED. Tokens (input+output+cache-write) after which the lane is stopped.")
@click.option("--count-cache-reads", is_flag=True, help="Also count cache reads against the cap.")
@click.option("--interval", type=float, default=15.0, show_default=True)
@click.option("--bind-polls", type=int, default=8, show_default=True,
              help="Attempts to find the lane's session id before it is REFUSED and stopped.")
@click.option("--sessions-root", type=click.Path(path_type=Path), default=None, hidden=True)
def govern_cmd(lane_id: str, slug: str, token_cap: int, count_cache_reads: bool, interval: float,
               bind_polls: int, sessions_root: Optional[Path]) -> None:
    """Govern a launched `--bg` lane: bind, poll, stop past the cap, witness a commit.

    LANE_ID may be omitted when the launcher could not read it from `claude --bg`'s output: the
    lane is then FOUND by its worktree (`.../worktrees/<slug>`) in `claude agents --json`.
    Run from the CALLER's repo root (the commit witness reads its branches)."""
    validate_cap(token_cap)
    try:
        lane_id, binding = _bind(lane_id, slug, bind_polls, interval)
        if not lane_id:
            # nothing names the lane, so there is nothing to stop: the one honest UNGOVERNED
            _finish(Verdict(False, 0, token_cap, 0, ungoverned=(
                f"no lane for worktree-{slug} could be identified in `claude agents --json`; if "
                "one was started it MAY BE RUNNING, uncapped -- stop it by hand")), slug)
        if binding is None:
            _finish(_refuse(f"lane {lane_id} could not be bound to a session id after "
                            f"{bind_polls} attempt(s)", 0, token_cap, 0, lambda: stop_lane(lane_id)),
                    slug)
        click.echo(f"[dispatch] governing lane {lane_id} (session {binding.session_id}) -- cap "
                   f"{token_cap}", err=True)
        verdict = govern(cap=token_cap, read_usage=_session_reader(binding.session_id, sessions_root),
                         stop=lambda: stop_lane(lane_id), sleep=time.sleep, interval=interval,
                         alive=lambda: lane_alive(lane_id), count_cache_reads=count_cache_reads)
    except KeyboardInterrupt:
        # a governor that quits leaves the lane uncapped: stop it, do not just say so
        stopped = stop_lane(lane_id)
        click.echo(f"[dispatch] governor interrupted -- lane {lane_id} "
                   f"{'STOPPED' if stopped else 'may STILL BE RUNNING, uncapped'}", err=True)
        sys.exit(EXIT_REFUSED if stopped else EXIT_UNGOVERNED)
    except Exception as exc:  # noqa: BLE001 -- whatever raised, a governor that dies must not
        # leave the lane it was capping running with nothing watching it
        stopped = bool(lane_id) and stop_lane(lane_id)
        click.echo(f"[dispatch] governor failed ({type(exc).__name__}: {exc}) -- lane {lane_id or '?'} "
                   f"{'STOPPED' if stopped else 'may STILL BE RUNNING, uncapped'}", err=True)
        sys.exit(EXIT_REFUSED if stopped else EXIT_UNGOVERNED)
    _finish(verdict, slug)


def _cwd_is_lane(cwd: str, slug: str) -> bool:
    """Is `cwd` the worktree `.../worktrees/<slug>` the planned lane runs in?"""
    return cwd.replace("\\", "/").rstrip("/").lower().endswith(f"/worktrees/{slug}".lower())


def _bind(lane_id: str, slug: str, polls: int, interval: float) -> tuple[str, Optional[LaneBinding]]:
    """`(lane id, binding)`; the id is '' when nothing identifies the lane.

    A PROVISIONAL id (the launcher read it out of `claude --bg`'s output) whose worktree is not the
    planned slug's belongs to ANOTHER lane: it is dropped and never governed -- stopping someone
    else's lane while ours runs uncapped is the worse failure. The lane is then FOUND by worktree."""
    binding: Optional[LaneBinding] = None
    for attempt in range(max(polls, 1)):
        if lane_id:
            binding = bind_lane(lane_id)
            if binding is not None and not _cwd_is_lane(binding.cwd, slug):
                binding, lane_id = None, ""
        if not lane_id:
            lane_id = find_lane_by_slug(slug) or ""
            binding = bind_lane(lane_id) if lane_id else None
        if binding is not None:
            return lane_id, binding
        if attempt + 1 < polls:
            time.sleep(min(interval, 3.0))
    return lane_id, None


def _finish(verdict: Verdict, slug: str) -> None:
    """Report the verdict; a lane that finished under cap must also have committed. Never returns."""
    _report(verdict)
    code = verdict.exit_code
    if code == 0:
        outcome, reason = commit_witness(slug)
        click.echo(f"[dispatch] {outcome}: {reason}")
        code = {"DONE": 0, "FAILED": EXIT_NO_COMMIT}.get(outcome, EXIT_UNWITNESSED)
    sys.exit(code)


def _report(verdict: Verdict) -> None:
    if verdict.stop_failed:
        state = "CAP NOT ENFORCED -- `claude stop` FAILED; the lane may still be running"
    elif verdict.refused:
        state = f"REFUSED ({verdict.ungoverned}) -- the lane is not running"
    elif verdict.ungoverned:
        state = f"UNGOVERNED ({verdict.ungoverned}) -- the cap was NOT enforced"
    elif verdict.exceeded:
        state = "CAP EXCEEDED -- lane stopped"
    else:
        state = "finished under cap" + (f" (child exited {verdict.child_exit})"
                                        if verdict.child_exit else "")
    click.echo(f"[dispatch] {state}: used {verdict.used} of {verdict.cap} tokens")


if __name__ == "__main__":  # pragma: no cover
    cli()
