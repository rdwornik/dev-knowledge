#!/usr/bin/env python
"""harness_probes.py -- ADR-123 §Migration step 0: the three probe receipts ([#670] nearest).

WHAT THE THREE PROBES ARE (ADR-123, verbatim intent)
=================================================================================================
P-1  a Claude Code plugin materialised from PACKAGE DATA loads in a fresh codespace, witnessed by
     one hook firing.
P-2  `uv add "dk-harness @ git+https://...#subdirectory=..."` resolves under the pinned uv 0.11.19
     in a fresh codespace.
P-3  a lane runs with the hub unreachable after the codespace's setup.

Exit: three receipts; any FAIL routes to ADR-123 §Flip-condition. `FLIP_ROUTES` carries that
routing as data, so a FAIL receipt that names the wrong fallback is refused by `validate`.

LAYER 2 NEVER EXECUTES IN A CHILD REPO
=================================================================================================
`remote` runs INSIDE a throwaway codespace of the consumer and writes nothing into the consumer's
checkout: P-2 resolves against a COPY of it under /tmp, P-1/P-3 use a scratch project under /tmp.
It records `git status --porcelain` + HEAD of the checkout before and after, so "read-only in the
consumer" is a measured fact in the receipt, not a claim. The package it installs is the stand-in
under `tests/fixtures/harness-probe-pkg/` (the real `packages/harness/` is ADR-123 step 1).

CALL SURFACE
=================================================================================================

    # inside the codespace (needs uv 0.11.19 on PATH; click comes from --with):
    uv run --no-project --with click python /tmp/harness_probes.py remote \\
        --ref <hub sha> --codespace <name> --out /tmp/harness-probe-receipts.json
    # in the hub, over the committed receipts audit:
    uv run --locked python scripts/harness_probes.py check docs/audits/<receipts>.md
"""
from __future__ import annotations

import json
import logging
import os
import re
import shlex
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

import click

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("harness-probes")

PROBES: tuple[str, ...] = ("P-1", "P-2", "P-3")
VERDICTS: frozenset[str] = frozenset({"PASS", "FAIL", "NOT_RUN"})

#: ADR-123 §Flip-condition, one route per probe. P-3 has no named fallback in the ADR; the route
#: says so instead of inventing one.
FLIP_ROUTES: dict[str, str] = {
    "P-1": "ADR-123 Flip-condition: fall back to O8 (three coordinates) -- a plugin cannot be "
           "materialised from package data and still load",
    "P-2": "ADR-123 Flip-condition: fall back to O6 (git subtree) -- git-URL subdirectory installs "
           "are not usable on the pinned uv without a uv bump",
    "P-3": "ADR-123 Flip-condition names no fallback for P-3 -- Exit says any failure routes to "
           "Flip-condition before step 1: the operator rules (revisit before step 1)",
}

HUB_URL = "https://github.com/rdwornik/dev-knowledge"
PACKAGE = "dk-harness-probe"
FIXTURE_SUBDIR = "tests/fixtures/harness-probe-pkg"
CONSUMER_DIR = "/workspaces/corp-monorepo"
ORGAN_MARKER = "dk-harness-probe check ok"
_EXCERPT_CHARS = 1500


# ------------------------------------------------------------------ receipt shape

def _is_iso(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate(receipts: list[dict]) -> list[str]:
    """Return every reason the receipt set is not three complete receipts; [] when it is."""
    errors: list[str] = []
    seen: dict[str, int] = {}
    for row in receipts:
        probe = row.get("probe")
        seen[probe] = seen.get(probe, 0) + 1
        if probe not in PROBES:
            errors.append(f"unknown probe {probe!r}")
            continue
        verdict = row.get("verdict")
        if verdict not in VERDICTS:
            errors.append(f"{probe}: verdict {verdict!r} not in {sorted(VERDICTS)}")
            continue
        if verdict == "NOT_RUN":
            if not (isinstance(row.get("blocker"), str) and row["blocker"].strip()):
                errors.append(f"{probe}: NOT_RUN needs the exact blocker")
            continue
        if not (isinstance(row.get("command"), str) and row["command"].strip()):
            errors.append(f"{probe}: command is blank")
        if not isinstance(row.get("exit_code"), int) or isinstance(row.get("exit_code"), bool):
            errors.append(f"{probe}: exit_code must be an integer")
        evidence = row.get("evidence") or {}
        for field in ("log_excerpt", "codespace"):
            if not (isinstance(evidence.get(field), str) and evidence[field].strip()):
                errors.append(f"{probe}: evidence.{field} is blank")
        if not _is_iso(evidence.get("timestamp")):
            errors.append(f"{probe}: evidence.timestamp is not an ISO-8601 timestamp")
        if verdict == "FAIL" and row.get("flip_route") != FLIP_ROUTES[probe]:
            errors.append(f"{probe}: a FAIL must carry flip_route == FLIP_ROUTES[{probe!r}]")
    for probe in PROBES:
        if seen.get(probe, 0) == 0:
            errors.append(f"{probe}: no receipt")
        elif seen[probe] > 1:
            errors.append(f"{probe}: receipt appears {seen[probe]} times, expected once")
    return errors


def routes(receipts: Iterable[dict]) -> list[tuple[str, str]]:
    """The ADR-123 Flip-condition route of every FAILed probe, in probe order."""
    failed = {r.get("probe") for r in receipts if r.get("verdict") == "FAIL"}
    return [(p, FLIP_ROUTES[p]) for p in PROBES if p in failed]


_JSON_BLOCK = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def extract_receipts(markdown: str) -> list[dict]:
    """The receipts are the FIRST fenced ```json block of the audit file (a list of dicts)."""
    match = _JSON_BLOCK.search(markdown)
    if not match:
        raise ValueError("no fenced json block holding the receipts")
    data = json.loads(match.group(1))
    if not isinstance(data, list):
        raise ValueError("the receipts block must be a JSON list")
    return data


# ------------------------------------------------------------------ verdicts (conjunctions)

def p1_verdict(*, plugin_loaded: bool, fired_events: list[str]) -> str:
    return "PASS" if plugin_loaded and fired_events else "FAIL"


def p2_verdict(exit_code: int, lock_text: str, package: str) -> str:
    named = re.search(rf'^name = "{re.escape(package)}"$', lock_text or "", re.MULTILINE)
    return "PASS" if exit_code == 0 and named else "FAIL"


def p3_verdict(*, hub_reachable: bool, lane_exit: int, organ_seen: bool,
               fired_events: list[str]) -> str:
    ok = (not hub_reachable) and lane_exit == 0 and organ_seen and bool(fired_events)
    return "PASS" if ok else "FAIL"


# ------------------------------------------------------------------ the remote run

def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sh(command: str, *, cwd: Optional[str] = None, timeout: int = 900) -> tuple[int, str]:
    """Run one command in a LOGIN bash (codespace secrets and ~/.local/bin live there)."""
    # The driver itself runs under `uv run --with click`, whose VIRTUAL_ENV must not leak into
    # the consumer's uv commands (uv warns and ignores it, which pollutes the evidence).
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    try:
        proc = subprocess.run(["bash", "-lc", command], cwd=cwd, capture_output=True, env=env,
                              text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        return 124, f"TIMEOUT after {timeout}s: {exc}"
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def _excerpt(text: str) -> str:
    """Keep the HEAD: callers put the facts a verdict rests on first, the bulk after."""
    text = text.strip()
    return text if len(text) <= _EXCERPT_CHARS else text[:_EXCERPT_CHARS] + "..."


def stream_summary(stream: str) -> str:
    """The facts of a `claude -p --output-format stream-json` run: init plugins and the result."""
    lines = []
    for raw in stream.splitlines():
        try:
            event = json.loads(raw)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            lines.append(f"init.plugins={_init_plugins(raw)}")
        elif event.get("type") == "result":
            lines.append(f"result={event.get('result')!r} is_error={event.get('is_error')} "
                         f"num_turns={event.get('num_turns')}")
    return "\n".join(lines) or "(no stream-json events)"


def _receipt(probe: str, command: str, exit_code: int, log: str, codespace: str,
             verdict: str, extra: Optional[dict] = None) -> dict:
    row = {
        "probe": probe, "command": command, "exit_code": exit_code,
        "evidence": {"log_excerpt": _excerpt(log) or "(no output)", "codespace": codespace,
                     "timestamp": _now()},
        "verdict": verdict, "blocker": None,
        "flip_route": FLIP_ROUTES[probe] if verdict == "FAIL" else None,
    }
    if extra:
        row["evidence"].update(extra)
    return row


def _consumer_state() -> dict:
    _, porcelain = _sh(f"git -C {CONSUMER_DIR} status --porcelain")
    _, head = _sh(f"git -C {CONSUMER_DIR} rev-parse HEAD")
    return {"porcelain": porcelain.strip(), "head": head.strip()}


def _witness_events(path: Path) -> list[str]:
    if not path.is_file():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            events.append(json.loads(line).get("event", "unknown"))
        except ValueError:
            continue
    return events


def _init_plugins(stream: str) -> list[str]:
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            return [p.get("name", str(p)) if isinstance(p, dict) else str(p)
                    for p in event.get("plugins", [])]
    return []


def _claude(prompt: str, cwd: str, witness: Path, extra: str = "") -> tuple[str, int, str]:
    witness.unlink(missing_ok=True)
    cmd = (f"HARNESS_PROBE_WITNESS={shlex.quote(str(witness))} claude -p {shlex.quote(prompt)} "
           f"--output-format stream-json --verbose {extra}").strip()
    code, out = _sh(cmd, cwd=cwd, timeout=600)
    return cmd, code, out


def run_remote(ref: str, codespace: str) -> dict:
    spec = f"{PACKAGE} @ git+{HUB_URL}@{ref}#subdirectory={FIXTURE_SUBDIR}"
    context: dict = {"ref": ref, "spec": spec, "consumer_before": _consumer_state()}
    context["uv_version"] = _sh("uv --version")[1].strip()
    context["claude_version"] = _sh("claude --version")[1].strip()
    receipts: list[dict] = []

    # P-2 -- resolve the git-URL subdirectory dependency in a COPY of the consumer project.
    copy = Path("/tmp/p2-corp")
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(CONSUMER_DIR, copy, ignore=shutil.ignore_patterns(".git", ".venv", ".worktrees"))
    p2_cmd = f"uv add --no-sync {shlex.quote(spec)}"
    p2_code, p2_out = _sh(p2_cmd, cwd=str(copy))
    lock = (copy / "uv.lock").read_text(encoding="utf-8") if (copy / "uv.lock").is_file() else ""
    lock_lines = [ln for ln in lock.splitlines() if PACKAGE in ln or "subdirectory=" in ln]
    receipts.append(_receipt("P-2", f"cd /tmp/p2-corp (copy of {CONSUMER_DIR}) && {p2_cmd}",
                             p2_code, p2_out, codespace, p2_verdict(p2_code, lock, PACKAGE),
                             {"uv_lock_lines": lock_lines[:6], "uv_version": context["uv_version"]}))

    # P-1 -- install the stand-in into a scratch project, materialise its plugin from package
    # data, install that plugin from the materialised marketplace at PROJECT scope (the ADR's
    # "project .claude/" route: it writes enabledPlugins into <project>/.claude/settings.json),
    # and watch one hook fire.
    scratch = Path("/tmp/harness-consumer")
    shutil.rmtree(scratch, ignore_errors=True)
    scratch.mkdir(parents=True)
    market = scratch / ".harness" / "marketplace"
    setup = (f"uv init --bare --name harness-consumer-probe && uv add {shlex.quote(spec)} && "
             f"uv run --locked {PACKAGE} install {market} && "
             f"claude plugin marketplace add {market} && "
             f"claude plugin install {PACKAGE}@dk-harness-probe-local --scope project")
    setup_code, setup_out = _sh(setup, cwd=str(scratch))
    witness = Path("/tmp/harness-probe-witness.jsonl")
    p1_cmd, p1_code, p1_out = _claude("Reply with the single word OK.", str(scratch), witness,
                                      "--max-turns 1")
    plugins = _init_plugins(p1_out)
    fired = _witness_events(witness)
    loaded = any(PACKAGE in p for p in plugins)
    settings = scratch / ".claude" / "settings.json"
    p1_log = "\n".join([
        stream_summary(p1_out),
        "witness=" + (witness.read_text(encoding="utf-8").strip() if witness.is_file() else ""),
        "project .claude/settings.json=" + (settings.read_text(encoding="utf-8").strip()
                                             if settings.is_file() else "(absent)"),
        "setup tail: " + setup_out.strip()[-400:],
    ])
    receipts.append(_receipt(
        "P-1", f"{setup} && {p1_cmd}", p1_code if setup_code == 0 else setup_code,
        p1_log, codespace,
        p1_verdict(plugin_loaded=loaded and setup_code == 0, fired_events=fired),
        {"init_plugins": plugins, "witness_events": fired}))

    # P-3 -- make the hub unreachable at the git transport, prove it, then run a lane that uses
    # the harness organ and the plugin.
    block = (f"git config --global url.https://hub-unreachable.invalid/rdwornik/dev-knowledge"
             f".insteadOf {HUB_URL}")
    _sh(block)
    probe_code, probe_out = _sh(f"GIT_TERMINAL_PROMPT=0 timeout 60 git ls-remote {HUB_URL} HEAD")
    lane_prompt = (f"Run the shell command `uv run --locked {PACKAGE} check` in the current "
                   "directory and reply with its output verbatim.")
    p3_cmd, p3_code, p3_out = _claude(lane_prompt, str(scratch), witness,
                                      "--max-turns 4 --allowedTools Bash")
    p3_fired = _witness_events(witness)
    _sh("git config --global --unset url.https://hub-unreachable.invalid/rdwornik/dev-knowledge"
        ".insteadOf")
    receipts.append(_receipt(
        "P-3", f"{block} && git ls-remote {HUB_URL} HEAD && {p3_cmd}", p3_code,
        f"[hub probe exit {probe_code}] {probe_out.strip()}\n{stream_summary(p3_out)}\n"
        f"witness={p3_fired}", codespace,
        p3_verdict(hub_reachable=probe_code == 0, lane_exit=p3_code,
                   organ_seen=ORGAN_MARKER in p3_out, fired_events=p3_fired),
        {"hub_probe_exit": probe_code, "witness_events": p3_fired}))

    context["consumer_after"] = _consumer_state()
    return {"context": context, "receipts": receipts}


# ------------------------------------------------------------------ CLI

@click.group()
def cli() -> None:
    """ADR-123 step-0 probe receipts."""


@cli.command("check")
@click.argument("path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def check_cmd(path: Path) -> None:
    """Validate the receipts in PATH and print the Flip-condition route of every FAIL."""
    try:
        receipts = extract_receipts(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        click.echo(f"REFUSED {path}: {exc}", err=True)
        raise SystemExit(1) from exc
    errors = validate(receipts)
    for err in errors:
        click.echo(f"REFUSED {err}", err=True)
    if errors:
        raise SystemExit(1)
    for row in receipts:
        click.echo(f"{row['probe']} {row['verdict']}")
    for probe, route in routes(receipts):
        click.echo(f"{probe} FAIL -> {route}")


@cli.command("remote")
@click.option("--ref", required=True, help="hub commit carrying the stand-in package")
@click.option("--codespace", required=True, help="the codespace's name, for the receipts")
@click.option("--out", required=True, type=click.Path(dir_okay=False, path_type=Path))
def remote_cmd(ref: str, codespace: str, out: Path) -> None:
    """Run P-2, P-1 and P-3 inside a codespace of the consumer; write the receipts to OUT."""
    result = run_remote(ref, codespace)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for row in result["receipts"]:
        logger.info("%s %s (exit %s)", row["probe"], row["verdict"], row["exit_code"])


if __name__ == "__main__":
    cli()
