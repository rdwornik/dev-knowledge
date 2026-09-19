#!/usr/bin/env python
"""dispatch.py -- launch ONE lane with a TOKEN CAP that is enforced, not requested.

WHY. Four sessions were ordered 180k tokens and used ~845k. A budget written into a prompt caps
nothing: the session has no instrument for its own spend. The cap therefore lives HERE, at the
launcher, which is the one place that can see the spend from outside and can stop the lane.

THIS IS A MOVE PLUS A LANGUAGE REWRITE, not a new design. Prior art, read before writing:

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
  * The child environment is built as a dict and handed to the child, so the PS `finally` that
    restored ANTHROPIC_BASE_URL has nothing to restore: the operator's shell is never touched.
  * No `Invoke-Expression`, no shell string: every command is an argv list.

WHAT DID NOT MOVE (left in win-tooling; see the audit for the list and the shim content):
  the cloud (Anthropic-hosted) substrate, harvest, Start-DispatchAfter, the deep-code wrapper,
  the Windows User-scope registry read of CLAUDE_PROMPTS_DIR, and Invoke-Dispatch's derived-line
  fallback (a Model/Effort table + filename). None of those is on the cap's path.

THE CAP, and its honest limits:
  * REQUIRED, no default. Counts input + output + cache-write; cache READS are excluded unless
    `--count-cache-reads` (they run to millions on a 100k context and would make any cap void).
  * `claude --bg` lanes: after launch a governor polls the lane's own transcript (via
    `lane_cost.lane_usage`, minus the baseline read before launch) and runs `claude stop <id>` past
    the cap. It is a POLL: a lane can overshoot by one interval of work. Killing this process
    (Ctrl-C) leaves the lane running UNCAPPED -- said aloud when it happens.
  * codex and codespace lanes are STREAM-metered: stdout is parsed line by line and the process
    terminated past the cap. codex reports usage only in `turn.completed`, so it is POST-HOC PER
    TURN: one over-cap turn completes before the meter can act (no bound on a single turn). Anthropic stream-json reports thinking tokens only in the final
    `result` event, so a thinking-heavy turn can overshoot until it lands.
  * A lane whose id or transcript cannot be found is reported UNGOVERNED (exit 4), never "under cap".
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
from typing import Callable, Mapping, Optional, Sequence

import click

try:  # pragma: no cover -- exercised by whichever path the caller uses
    from scripts import lane_cost as lc
except ImportError:  # pragma: no cover
    import lane_cost as lc

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("dispatch")

EXIT_CAP_EXCEEDED = 3
EXIT_UNGOVERNED = 4

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

    @property
    def exit_code(self) -> int:
        if self.stop_failed or self.ungoverned:
            return EXIT_UNGOVERNED
        if self.exceeded:
            return EXIT_CAP_EXCEEDED
        return self.child_exit


def govern(*, cap: int, read_usage: Callable[[], Optional["lc.TokenUsage"]],
           stop: Callable[[], Optional[bool]],
           sleep: Callable[[float], None] = time.sleep, interval: float = 15.0,
           max_polls: Optional[int] = None, alive: Callable[[], bool] = lambda: True,
           count_cache_reads: bool = False, blind_polls: int = 8) -> Verdict:
    """Poll a running lane; STOP it the first time it is past `cap`.

    `read_usage` returns None when the spend cannot be observed (no transcript yet / at all):
    that is UNGOVERNED after `blind_polls` in a row, never zero spend. `stop` returning False
    is a stop that did not happen. `alive` raising GovernorBlind is an unreadable status probe,
    not a finished lane. The lane is not killed for being unobservable -- that would destroy work
    to report a measurement gap -- it is reported, exit 4."""
    validate_cap(cap)
    polls, used, blind = 0, 0, 0
    while True:
        usage = read_usage()
        if usage is None:
            blind += 1
            if blind >= blind_polls:
                return Verdict(False, used, cap, polls + 1,
                               ungoverned=f"no readable usage for {blind} polls")
        else:
            blind = 0
            used = capped_tokens(usage, count_cache_reads)
            if used > cap:
                return Verdict(True, used, cap, polls + 1, stop_failed=(stop() is False))
        polls += 1
        try:
            done = not alive()
        except GovernorBlind as exc:
            return Verdict(False, used, cap, polls, ungoverned=str(exc))
        if (max_polls is not None and polls >= max_polls) or done:
            # the last read was blind: the final spend was never observed -- not "under cap"
            return Verdict(False, used, cap, polls,
                           ungoverned=(f"lane ended after {blind} unreadable usage poll(s); "
                                       "final spend never observed") if blind else "")
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

def prompts_dir(environ: Mapping[str, str] = os.environ, home: Optional[str] = None,
                root_exists: Callable[[str], bool] = os.path.exists) -> Path:
    raw = (environ.get("CLAUDE_PROMPTS_DIR") or "").strip()
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


def _git_branch_exists(branch: str) -> bool:
    return subprocess.run(["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
                          capture_output=True).returncode == 0


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


def _terminate(proc: "subprocess.Popen", grace: float = 10.0) -> bool:
    """terminate, then kill, and VERIFY the child is gone; False when it survived both."""
    proc.terminate()
    try:
        proc.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        proc.kill()
        try:
            proc.wait(timeout=grace)
        except subprocess.TimeoutExpired:
            pass
    return proc.poll() is not None


def run_streamed(argv: Sequence[str], env: Mapping[str, str], cap: int,
                 count_cache_reads: bool = False, cwd: Optional[str] = None) -> Verdict:
    """Run `argv`, parse its stdout as it arrives, terminate it the moment it is past `cap`."""
    try:
        proc = subprocess.Popen(list(argv), env=dict(env), cwd=cwd, stdout=subprocess.PIPE,
                                stdin=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
    except OSError as exc:  # absent/unrunnable launcher: a refusal, not a traceback
        raise DispatchRefused(f"cannot start {argv[0]!r}: {exc}") from exc
    total, seen, polls, observed = lc.TokenUsage(), set(), 0, False
    assert proc.stdout is not None
    for line in proc.stdout:
        polls += 1
        try:
            usage = usage_from_stream_line(line, seen)
        except (ValueError, TypeError, OverflowError) as exc:  # not a (finite) number: stop, never abandon
            stopped = _terminate(proc)
            return Verdict(False, capped_tokens(total, count_cache_reads), cap, polls,
                           ungoverned=f"malformed usage in the stream ({exc}); child stopped",
                           stop_failed=not stopped)
        if usage is not None:
            observed = True
            total = total + usage
        used = capped_tokens(total, count_cache_reads)
        if used > cap:
            return Verdict(True, used, cap, polls, stop_failed=not _terminate(proc))
    code = proc.wait()
    blind = "" if observed or code != 0 else "the stream carried no parseable usage event"
    return Verdict(False, capped_tokens(total, count_cache_reads), cap, polls,
                   ungoverned=blind, child_exit=code)


# --- CLI ---------------------------------------------------------------------------------

_ID = re.compile(r"\b([0-9a-f]{8})\b")


def _control(argv: list[str]) -> Optional["subprocess.CompletedProcess"]:
    """A bounded control-plane call; None when it hung or could not run."""
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=30)
    except (subprocess.TimeoutExpired, OSError):
        return None


def stop_lane(lane_id: str) -> bool:
    done = _control(["claude", "stop", lane_id])
    return done is not None and done.returncode == 0


def lane_alive(lane_id: str) -> bool:
    listing = _control(["claude", "agents", "--json"])
    if listing is None or listing.returncode != 0 or not listing.stdout.strip():
        raise GovernorBlind("`claude agents --json` failed, hung or was empty")
    return lane_id in listing.stdout


def _lane_reader(slug: str, baseline: "lc.TokenUsage",
                 slug_dirs: Sequence[str] = ()) -> Callable[[], Optional["lc.TokenUsage"]]:
    def read() -> Optional["lc.TokenUsage"]:
        models = lc.lane_usage(slug, slug_dirs=tuple(slug_dirs) or None)
        if not models:  # no transcript found: unobservable, NOT zero
            return None
        total = _sum(models)
        return lc.TokenUsage(
            input_tokens=max(total.input_tokens - baseline.input_tokens, 0),
            output_tokens=max(total.output_tokens - baseline.output_tokens, 0),
            cache_write_tokens=max(total.cache_write_tokens - baseline.cache_write_tokens, 0),
            cache_read_tokens=max(total.cache_read_tokens - baseline.cache_read_tokens, 0))
    return read


def _sum(models: Mapping[str, "lc.TokenUsage"]) -> "lc.TokenUsage":
    total = lc.TokenUsage()
    for u in models.values():
        total = total + u
    return total


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli() -> None:
    """Launch a lane under an enforced token cap."""


@cli.command("launch")
@click.argument("contract")
@click.option("--slug", required=True, help="Lane slug; the worktree is worktree-<slug>.")
@click.option("--provider", default="anthropic", show_default=True)
@click.option("--model", default="opus", show_default=True)
@click.option("--effort", default="medium", show_default=True)
@click.option("--substrate", type=click.Choice(SUBSTRATES), default="local", show_default=True)
@click.option("--token-cap", "token_cap", type=int, required=True,
              help="REQUIRED. Tokens (input+output+cache-write) after which the lane is stopped.")
@click.option("--count-cache-reads", is_flag=True, help="Also count cache reads against the cap.")
@click.option("--repo", default="", help="owner/name; the codespace substrate only.")
@click.option("--branch", default="main", show_default=True)
@click.option("--slug-dir", "slug_dirs", multiple=True,
              help="Session-store directory holding the lane's transcript when it is not filed "
                   "under the slug (a --bg lane can be filed under its launcher's directory).")
@click.option("--interval", type=float, default=15.0, show_default=True)
@click.option("--secrets-file", type=click.Path(path_type=Path),
              default=Path.home() / "Documents" / ".secrets" / ".env", show_default=True)
@click.option("--dry-run", is_flag=True, help="Print the plan and stop.")
def launch(contract: str, slug: str, provider: str, model: str, effort: str, substrate: str,
           token_cap: int, count_cache_reads: bool, repo: str, branch: str, slug_dirs: tuple[str, ...],
           interval: float,
           secrets_file: Path, dry_run: bool) -> None:
    validate_cap(token_cap)
    # the prompts dir is resolved LAZILY: an absolute contract must not be refused because an
    # unrelated authority drive is unmounted (the PS comment in Invoke-Dispatch.ps1 says why)
    path = (Path(contract).resolve() if Path(contract).is_file()
            else resolve_contract(contract, prompts_dir()))
    prompt = f"Read and execute the frozen contract at {path}"
    plan = build_plan(provider, model, slug, effort, prompt,
                      streamed=(substrate == "codespace" and _provider(provider).head == "claude"))
    if substrate == "codespace":
        if not repo:
            raise DispatchRefused("--repo owner/name is required for the codespace substrate")
        head = [plan.argv[0]] + plan.argv[1:]
        steps = codespace_plan(repo, branch, slug, path, head)
        click.echo("[dispatch] substrate=codespace machine=basicLinux32gb idle-timeout=30m "
                   "retention=1d (a STOPPED codespace still bills storage; this never deletes)")
        for s in steps:
            click.echo(f"[dispatch]   {s.note}: {' '.join(s.argv)}")
    label = " (post-hoc per completed turn)" if plan.argv[0] == "codex" else ""
    click.echo(f"[dispatch] provider={provider} model={model} effort={EFFORTS.get(effort.lower())} "
               f"token-cap={token_cap} metering={plan.metering}{label}")
    click.echo(f"[dispatch] {' '.join(plan.argv[:-1])}")
    click.echo(f"[dispatch] prompt: {prompt}")
    if dry_run:
        return
    if substrate == "codespace":
        raise DispatchRefused("live codespace execution is not verified in this build (it needs "
                              "gh auth and bills per minute); run with --dry-run and see the audit")
    env = child_env(provider, os.environ, read_secrets(secrets_file))
    if (skip := branch_guard(slug, _git_branch_exists)) is not None:
        raise DispatchRefused(skip)
    if plan.metering == "stream":
        verdict = run_streamed(plan.argv, env, token_cap, count_cache_reads)
        _report(verdict)
        sys.exit(verdict.exit_code)
    baseline = _sum(lc.lane_usage(slug, slug_dirs=slug_dirs or None))
    started = subprocess.run(plan.argv, env=env, capture_output=True, text=True)
    click.echo(started.stdout.strip())
    if started.returncode != 0:
        raise DispatchRefused(f"claude exited {started.returncode}: {started.stderr.strip()[:300]}")
    found = _ID.search(started.stdout)
    if not found:
        click.echo("[dispatch] UNGOVERNED -- could not read the lane id from `claude --bg`; the cap "
                   "is NOT enforced. Stop the lane by hand if it runs long.", err=True)
        sys.exit(EXIT_UNGOVERNED)
    lane_id = found.group(1)

    click.echo(f"[dispatch] governing lane {lane_id} -- cap {token_cap}; Ctrl-C leaves it UNCAPPED")
    try:
        verdict = govern(cap=token_cap, read_usage=_lane_reader(slug, baseline, slug_dirs),
                         stop=lambda: stop_lane(lane_id), interval=interval,
                         alive=lambda: lane_alive(lane_id), count_cache_reads=count_cache_reads)
    except KeyboardInterrupt:
        click.echo(f"[dispatch] governor interrupted -- lane {lane_id} is now UNCAPPED", err=True)
        sys.exit(EXIT_UNGOVERNED)
    _report(verdict)
    sys.exit(verdict.exit_code)


def _report(verdict: Verdict) -> None:
    if verdict.stop_failed:
        state = "CAP EXCEEDED but `claude stop` FAILED -- the lane may still be running"
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
