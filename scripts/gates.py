#!/usr/bin/env python
"""gates.py -- the per-merge gate list, run as ONE organ with ONE verdict artifact.

WHY IT EXISTS. The gates a merge is judged by -- the self-audit, the ship gate, ruff, the tests the
change impacts -- existed as four separate invocations a human strings together, which is why they
ran once per window instead of once per merge. L1 declared this organ at the `merge` moment
(`ecosystem/harness.yaml`, `gates.py run --lane {lane}`); this file is the path it named.

WHAT IT IS NOT. It implements no check and weakens none: each gate below is an existing verb,
invoked as its own argv, and the verdict is the conjunction of their exit codes. The gate list is a
declaration in this file, not a knob -- there is no flag that removes a gate, and `--gate-list`
(test plumbing) is stamped onto the verdict as `list: override:<path>` so an overridden run cannot
pass for the declared one.

  * EVERY GATE RUNS EXACTLY ONCE, IN THE DECLARED ORDER, AND A RED ONE DOES NOT HIDE THE REST. The
    artifact is the complete picture of the merge, not the first thing that failed.
  * A GATE THAT CANNOT START IS RED (exit 127), never skipped: an absent program and a failing one
    are the same refusal to call the merge good.
  * NO TIMEOUT. Nothing built tonight may stop, truncate or kill a task (DECLARE-NIGHT N3); a slow
    gate is a slow gate, and its duration is in the verdict.
  * THE FULL SUITE IS NOT IN THE LIST. The per-merge leg is the IMPACTED tests; CI owns the full
    run. Where the selector declines to narrow it says so, and the gate is RED with that reason
    rather than quietly running everything -- a gate that sometimes secretly becomes the full suite
    is the once-per-window cost this organ exists to remove.

THE VERDICT ARTIFACT is `MOMENT-MERGE-GATES-VERDICT.json` in the receipts home (`logs/receipts/`,
gitignored, `HARNESS_RECEIPTS_DIR` overrides -- L1's convention). The organ RECEIPT beside it is
written by `telemetry_emit.py wrap`; this file is what the receipt's exit code summarises.

PER-ORGAN FINDINGS (FR4, W4B-3). `audit.py health` and `audit.py ship-gate` each run many
self-audit checks (organs) and print one line per Finding in the LOCKED shape `[MARKER] check_name:
evidence` (`audit.py`'s own `_marker` table: `[OK]`/`[~~]`/`[!!]`/`[??]`/`[--]`). Grepping a
truncated TAIL of that text for a hard-fail name is exactly the failure this organ existed to
remove one layer down: the fail/warn lines sit wherever they sit in run order, not necessarily near
the end, so a tail can miss them entirely (WAVE4-FINAL digest, finding 4). Every gate's FULL
captured text (not the truncated `output_tail`) is parsed for that same locked line shape, and
every fail/warn line becomes one entry in the row's new `findings` list: `{"check_name", "status",
"evidence"}` -- the organ's own identity and verdict, structured, independent of where in the
output it printed. A gate whose output carries no such lines (ruff, impacted-tests) simply yields
`findings: []`; nothing about the existing `output_tail` or any other field changes -- this is new
data alongside old (common rule 8).

Run:  uv run --locked python scripts/gates.py run --lane <lane> [--base <ref>]
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional, Sequence

import click

_ROOT = Path(__file__).resolve().parent.parent
_VERDICT_NAME = "MOMENT-MERGE-GATES-VERDICT.json"
_TAIL_CHARS = 2000
_NOT_STARTED = 127

#: The locked `audit.py` Finding-line shape (`_marker` there: OK/~~/!!/??/--) -> our status name.
#: Read from FULL gate text, never a truncated tail (FR4): a hard-fail's line does not move just
#: because it happens to print early in a long ship-gate run.
_FINDING_MARKER_STATUS = {"OK": "pass", "~~": "warn", "!!": "fail", "??": "unavailable", "--": "n/a"}
_FINDING_LINE_RE = re.compile(
    r"^[ \t]*\[(OK|~~|!!|\?\?|--)\][ \t]+([A-Za-z_]\w*): (.*)$", re.MULTILINE)


def _findings_in(text: str) -> list[dict]:
    """Every hard-fail/warning Finding printed in `text`, as `{check_name, status, evidence}` --
    parsed from the same locked `[MARKER] check_name: evidence` line `audit.py` already prints, so
    this reads real CLI output rather than re-running the checks in-process (no doubled cost). A
    gate with no such lines (ruff, impacted-tests) yields `[]`, not an error."""
    found = []
    for marker, name, evidence in _FINDING_LINE_RE.findall(text or ""):
        status = _FINDING_MARKER_STATUS[marker]
        if status in ("fail", "warn"):
            found.append({"check_name": name, "status": status, "evidence": evidence})
    return found


@dataclass(frozen=True)
class Gate:
    """One gate: an argv to run, or a `runner(cwd, base) -> (exit_code, text)` for a gate that is
    two steps (select, then run). Exactly one of the two is meaningful."""
    name: str
    argv: tuple[str, ...] = ()
    runner: Optional[Callable[..., tuple[int, str]]] = None


def _run_argv(argv: Sequence[str], cwd: Path) -> tuple[int, str]:
    try:
        proc = subprocess.run(list(argv), cwd=str(cwd), capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
    except (OSError, ValueError) as exc:
        return _NOT_STARTED, f"could not start {argv[0] if argv else '<empty>'}: {exc!r}"
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


# --- the impacted-tests gate: select, then run ONLY what was selected -----------------------------

_UV = ("uv", "run", "--locked")


def _select_impacted(cwd: Path, base: str) -> tuple[int, str]:
    """`impacted_tests.py select --ref <base>` -> (exit code, its stdout).

    A ref that does not resolve is refused here: `git diff --name-only <bad>` prints nothing, and the
    selector reads nothing as 'no changed paths; nothing to select' -- a clean-looking answer from
    a call that never worked."""
    code, out = _run_argv(("git", "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}"), cwd)
    if code != 0:
        return 1, f"base ref {base!r} does not resolve -- refusing to read that as 'nothing changed'"
    return _run_argv((*_UV, "python", "scripts/impacted_tests.py", "select", "--ref", base), cwd)


def _run_pytest(cwd: Path, args: list[str]) -> tuple[int, str]:
    return _run_argv((*_UV, "pytest", "-x", "--tb=short", *args), cwd)


def impacted_tests_gate(cwd: Path, base: str = "HEAD^1") -> tuple[int, str]:
    code, out = _select_impacted(cwd, base)
    if code != 0:
        return code, out
    lines = [line for line in out.splitlines() if line.strip()]
    if any(line.startswith("# FULL SUITE") for line in lines):
        return 1, ("the impacted-test selector declined to narrow ('# FULL SUITE') -- refusing to "
                   "run the full suite as a per-merge gate; CI owns that run. Selector said: "
                   + " | ".join(lines))
    args = " ".join(line for line in lines if not line.startswith("#")).split()
    if not args:
        return 0, "no impacted tests selected (" + " | ".join(lines) + ")"
    return _run_pytest(cwd, args)


#: THE DECLARED LIST. Order is the order they run; add a gate by adding a row, never by a flag.
GATES: tuple[Gate, ...] = (
    Gate("audit-health", (*_UV, "python", "scripts/audit.py", "health")),
    Gate("ship-gate", (*_UV, "python", "scripts/audit.py", "ship-gate")),
    Gate("ruff", (*_UV, "ruff", "check")),
    Gate("impacted-tests", runner=lambda cwd, base: impacted_tests_gate(cwd, base)),
)


# --- running the list ------------------------------------------------------------------------------

def default_base(cwd: Path) -> str:
    """The merge's first parent when HEAD is a merge (the moment fires after the local merge),
    else `main`."""
    code, out = _run_argv(("git", "rev-list", "--parents", "-n", "1", "HEAD"), cwd)
    if code == 0 and len(out.split()) >= 3:
        return "HEAD^1"
    return "main"


def run_gates(gates: Sequence[Gate], *, lane: str, cwd: Path, base: Optional[str] = None,
              source: str = "declared") -> dict:
    """Run each gate once, in order; return the verdict. Nothing is swallowed and nothing stops early."""
    base = base or default_base(cwd)
    rows = []
    for gate in gates:
        started = time.monotonic()
        if gate.runner is not None:
            try:
                code, text = gate.runner(cwd, base)
            except Exception as exc:  # a gate that raises is a red gate, with the reason on it
                code, text = 1, f"gate raised {exc!r}"
            except SystemExit as exc:  # a runner must not end the PROCESS green under the verdict
                code, text = 1, f"gate runner called sys.exit({exc.code!r}) -- recorded as a failure"
        else:
            code, text = _run_argv(gate.argv, cwd)
        rows.append({"name": gate.name, "argv": list(gate.argv), "exit_code": int(code),
                     "duration_ms": int((time.monotonic() - started) * 1000),
                     "output_tail": (text or "")[-_TAIL_CHARS:],
                     "findings": _findings_in(text or "")})
    red = [row["name"] for row in rows if row["exit_code"] != 0]
    return {"schema": 1, "lane": lane, "base": base, "list": source,
            "verdict": "RED" if red else "GREEN", "red": red, "gates": rows,
            "finished_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def exit_code_for(verdict: dict) -> int:
    return 0 if verdict["verdict"] == "GREEN" else 1


def write_verdict(verdict: dict, out: Path) -> Path:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".tmp")
    tmp.write_text(json.dumps(verdict, indent=2), encoding="utf-8", newline="\n")
    os.replace(tmp, out)
    return out


def _default_out() -> Path:
    return Path(os.environ.get("HARNESS_RECEIPTS_DIR") or _ROOT / "logs" / "receipts") / _VERDICT_NAME


def _load_override(path: str) -> tuple[Gate, ...]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return tuple(Gate(name=row["name"], argv=tuple(row["argv"])) for row in rows)


@click.group()
def cli() -> None:
    """The per-merge gate list."""


@cli.command("run")
@click.option("--lane", required=True, help="the lane whose merge is being judged")
@click.option("--base", default=None,
              help="ref the impacted tests are selected against [default: HEAD^1 on a merge, else main]")
@click.option("--out", default=None, type=click.Path(dir_okay=False),
              help=f"verdict artifact [default: <receipts home>/{_VERDICT_NAME}]")
@click.option("--gate-list", "gate_list", default=None, type=click.Path(exists=True, dir_okay=False),
              help="TEST PLUMBING: a JSON list of {name, argv} replacing the declared list; the "
                   "verdict is stamped `override` so it cannot pass for the declared run")
def run_cmd(lane: str, base: Optional[str], out: Optional[str], gate_list: Optional[str]) -> None:
    """Run every declared gate once; write the verdict; exit non-zero if any gate is red."""
    if gate_list:
        gates, source = _load_override(gate_list), f"override:{gate_list}"
        click.echo(f"gates: OVERRIDDEN gate list {gate_list} -- this is not the declared run")
    else:
        gates, source = GATES, "declared"
    verdict = run_gates(gates, lane=lane, cwd=_ROOT, base=base, source=source)
    path = write_verdict(verdict, Path(out) if out else _default_out())
    for row in verdict["gates"]:
        state = "ok " if row["exit_code"] == 0 else "RED"
        click.echo(f"gates: {state} {row['name']} exit={row['exit_code']} {row['duration_ms']}ms")
    click.echo(f"gates: {verdict['verdict']} ({len(verdict['gates'])} gates) -> {path}")
    if verdict["red"]:
        click.echo("gates: RED: " + ", ".join(verdict["red"]))
    sys.exit(exit_code_for(verdict))


if __name__ == "__main__":  # pragma: no cover -- CLI entry
    cli()
