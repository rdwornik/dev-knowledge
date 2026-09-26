#!/usr/bin/env python
"""codespace_admission.py — the admission predicate `Dispatch-Codespace` runs, as ONE hub
script (LANE-5B2-23 / LANE-5B3-9).

WHY THIS EXISTS. `Dispatch-Codespace`'s admission self-test (the deployed
`DispatchHelpers.psm1`, `~\\.dispatch-helpers\\Modules\\DispatchHelpers\\DispatchHelpers.psm1`,
STEP 0 around lines 3075-3182) is bash embedded in a PowerShell here-string, running once, at
dispatch time, on whichever container happened to be built. Nothing else in this repo asks the
same question before that moment: the heartbeat (`substrate_heartbeat.py`) builds a devcontainer
recipe from scratch and never runs the admission test at all, so a heartbeat that reports green
tells a reader nothing about whether `Dispatch-Codespace` would actually admit a lane into that
same container. This module is the fix — the SAME predicate, extracted into ONE hub script that
both the deployed PowerShell (unedited, per this lane's "Do not") and the heartbeat can run, so a
green heartbeat means admission would pass.

EVERY GATING CONDITION CITES THE DEPLOYED MODULE, BY LINE, because the deployed copy is what
actually runs — it diverges from win-tooling's tracked source (REFUSED-lane-codespace-proof.md)
— and a predicate that quietly re-derived its own opinion of what gates would drift from it
silently. Line numbers below are the deployed copy read 2026-09-26; `ROWS-OWED` records that
DispatchHelpers should call THIS script instead of carrying its own copy, which is what makes
future drift impossible rather than merely rare.

THE CONDITIONS, gating (each flips admission to REFUSED) unless marked non-gating:

  claude on PATH          psm1:3083 (computed), psm1:3127-3137 (the three-way diagnosis; the
                          deployed test treats this as its OWN hard failure, exit 91, separate
                          from the STEP-0 `adm_ok` bundle below — collapsed here into one
                          gating condition because both are "this container cannot run a lane")
  uv on PATH              psm1:3084 (computed), psm1:3149 (gated)
  python3 on PATH         psm1:3085 (computed), psm1:3150 (gated)
  git remote reachable    psm1:3101-3102 (`timeout 30 git ls-remote origin HEAD`, computed),
                          psm1:3151 (gated)
  pre-commit on PATH      psm1:3114 (computed), psm1:3152 (gated) — MEASURED (WAVE5B-N2,
                          REFUSED-lane-codespace-proof.md): the venv's `pre-commit` resolves
                          inside `uv run` / an activated shell but not on a FRESH LOGIN shell's
                          PATH, which is the one this predicate must be run under (Done-contract
                          item 2: `bash -l`) for the check to mean anything.
  gh not broken           psm1:3094-3096 (computed), psm1:3162 (gated) — NON-GATING when gh is
                          simply ABSENT (psm1:3093, psm1:3154-3161: gh absence is a measured
                          "container fit to run the work", `lane-632-longrun-a-54r7jgp5qprh766p`);
                          gating only when gh is present and `gh auth status` fails, because that
                          is a broken tool rather than an absent one.
  contract resolved       psm1:3115-3121 (computed), psm1:3153 (gated) — NON-GATING here when no
                          `--contract` is given. The deployed test checks that a PARTICULAR lane
                          contract, copied in for THIS dispatch, landed at its path; a heartbeat
                          run dispatches no lane and has no such file to check. A caller that
                          IS dispatching a lane passes `--contract PATH` and the check gates.

  git hooks armed         ADDED, beyond what the deployed test checks — the Done-contract names
                          it explicitly ("the git hooks armed (`core.hooksPath` or the hook
                          files)"), and the deployed test's own comment (psm1:3109-3113) says why
                          it is needed: "pre-commit IS GATED, and it is the one tool whose absence
                          is INVISIBLE at the moment it matters. A container without it does not
                          fail to commit -- it commits happily, with every gate in
                          .pre-commit-config.yaml unarmed". The deployed test only checks that the
                          `pre-commit` BINARY resolves on PATH — it does not check that the git
                          hook SHIMS themselves exist and are pre-commit-managed, which is the
                          actual precondition for a gate to fire. `provision.sh::assert_hooks_armed`
                          already reuses `scripts/arm_hooks.py`'s `_armed` predicate for exactly
                          this reason ("duplicating that logic here would give the repo two
                          answers to one question"), and this module reuses the same one rather
                          than inventing a second.

NON-GATING, REPORTED-ONLY, NOT MODELLED HERE AT ALL: the deployed test also reads the Anthropic
and GitHub token env-var NAMES (never values, psm1:3105-3106) and whether the workspace-trust
dialog was recorded (psm1:3107-3108, 3144-3146) — both explicitly "recorded but not gating" in
the deployed test's own comments, so they carry no admission verdict to extract. `gh` PRESENCE
(as opposed to brokenness) is the same shape and is folded into the `gh not broken` condition
above rather than a condition of its own.

RUNS UNDER `bash -l` (Done-contract item 2). This module makes no attempt to spawn its own
login shell — it trusts that whatever invoked it (the heartbeat's workflow step, or a human at
a login prompt) already put it under one, and reads `PATH` from its own process environment,
which is the honest way to answer "what would THIS shell resolve" rather than re-deriving a
shell's own startup-file resolution order in Python.

WHY A CUSTOM PATH SEARCH AND NOT `shutil.which`. `shutil.which` on Windows consults `PATHEXT`
and treats an extension-less file as not executable unless a registered extension is appended —
behaviour this repo's own Windows development workstation exhibits and the Linux container this
predicate actually targets does not. A test fixture built to model "absent from PATH" or
"present on PATH" needs to mean the same thing on both, so `Probe.which` does a plain
basename-in-directory search instead — the same portable simplification this lane's tests need
DispatchHelpers.psm1 to have to be testable at all, since it is bash `command -v` under the hood.

Layer-2 / read-only-except-the-checks-it-runs: this module writes nothing of its own. Every
condition it names is deterministic and, where they touch the network at all (git ls-remote,
gh auth status), bounded (30s, mirroring the deployed test's own `timeout 30`).
"""
from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

logging.basicConfig(format="%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("codespace-admission")

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent

#: Where the conditions below were read. Cited by line in each condition's docstring/detail so a
#: reader can go verify the deployed copy has not drifted further out from under this module.
DEPLOYED_MODULE = r"~\.dispatch-helpers\Modules\DispatchHelpers\DispatchHelpers.psm1"

_NETWORK_TIMEOUT = 30  # seconds — mirrors the deployed test's own `timeout 30` (psm1:3102)


# --- the seam ---------------------------------------------------------------------------------

class Probe:
    """Everything this module learns about the environment it runs in, behind ONE seam — the
    same shape `substrate_provenance.LiveProbe` uses, so a test drives this module the way it
    drives that one: by constructing a `Probe` (or a subclass overriding `run`), never by
    monkeypatching a name this module never consults.
    """

    def __init__(self, env: dict[str, str] | None = None):
        self.env = dict(os.environ) if env is None else dict(env)

    def which(self, exe: str) -> str | None:
        """A basename-only search over `self.env['PATH']`. See the module docstring for why
        this is not `shutil.which`."""
        path_value = self.env.get("PATH", "")
        for entry in path_value.split(os.pathsep):
            if not entry:
                continue
            candidate = Path(entry) / exe
            if candidate.is_file():
                return str(candidate)
        return None

    def run(self, argv: list[str], *, cwd: Path | None = None,
            timeout: int = _NETWORK_TIMEOUT) -> subprocess.CompletedProcess | None:
        """`None` when the process could not even be started, or timed out — collapsed to one
        return shape so a caller (and a test double) never has to distinguish "refused" from
        "could not look" beyond checking for `None`."""
        try:
            return subprocess.run(
                argv, cwd=str(cwd) if cwd else None, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=timeout, env=self.env)
        except (OSError, subprocess.SubprocessError):
            return None


# --- one condition ------------------------------------------------------------------------------

@dataclass(frozen=True)
class Condition:
    """One admission condition's verdict. `cites` is the provenance a reader checks when the
    deployed test moves — a line number in `DEPLOYED_MODULE`, or "ADDED" for the one condition
    this predicate checks beyond what the deployed test does (see the module docstring)."""

    id: str
    ok: bool
    detail: str
    cites: str
    gates: bool = True  # False for a condition the deployed test RECORDS but does not refuse on


# --- the conditions, one function each, each citing its line(s) --------------------------------

def check_claude_on_path(probe: Probe) -> Condition:
    found = probe.which("claude")
    ok = found is not None
    detail = (f"claude resolves to {found}" if ok else
              "claude is not on this login shell's PATH — a container without a working agent "
              "is not a provisioned one (the exact three-way diagnosis the deployed test makes "
              "collapses here to: this container cannot run a lane)")
    return Condition("claude_on_path", ok, detail,
                     f"{DEPLOYED_MODULE}:3083,3127-3137")


def check_uv_on_path(probe: Probe) -> Condition:
    found = probe.which("uv")
    ok = found is not None
    detail = f"uv resolves to {found}" if ok else "uv is not on the login PATH"
    return Condition("uv_on_path", ok, detail, f"{DEPLOYED_MODULE}:3084,3149")


def check_python3_on_path(probe: Probe) -> Condition:
    found = probe.which("python3")
    ok = found is not None
    detail = f"python3 resolves to {found}" if ok else "python3 is not on the login PATH"
    return Condition("python3_on_path", ok, detail, f"{DEPLOYED_MODULE}:3085,3150")


def check_pre_commit_on_path(probe: Probe) -> Condition:
    found = probe.which("pre-commit")
    ok = found is not None
    detail = (f"pre-commit resolves to {found}" if ok else
              "pre-commit is not on the login PATH -- a lane that commits here would land work "
              "past every gate")
    return Condition("pre_commit_on_path", ok, detail, f"{DEPLOYED_MODULE}:3114,3152")


def check_git_remote_reachable(root: Path, probe: Probe) -> Condition:
    proc = probe.run(["git", "-C", str(root), "ls-remote", "origin", "HEAD"])
    ok = proc is not None and proc.returncode == 0
    detail = ("this container can reach origin (git ls-remote succeeded)" if ok else
              "this container cannot reach origin -- git ls-remote failed")
    return Condition("git_remote_reachable", ok, detail, f"{DEPLOYED_MODULE}:3101-3102,3151")


def check_gh_not_broken(probe: Probe) -> Condition:
    found = probe.which("gh")
    if found is None:
        # ABSENCE IS NOT GATED — a measured decision, not a soft one. See the module docstring.
        return Condition("gh_not_broken", True,
                         "gh is absent -- not gated (measured: a container with no gh at all "
                         "ran a lane perfectly well because GITHUB_TOKEN was set and git could "
                         "reach origin, which is every remote thing a lane actually does)",
                         f"{DEPLOYED_MODULE}:3086-3096,3154-3161", gates=False)
    proc = probe.run(["gh", "auth", "status"])
    ok = proc is not None and proc.returncode == 0
    detail = ("gh is installed and gh auth status succeeds" if ok else
              "gh is installed but gh auth status fails -- an unauthenticated gh is a broken "
              "tool, not an absent one")
    return Condition("gh_not_broken", ok, detail, f"{DEPLOYED_MODULE}:3094-3096,3162")


def check_contract(contract_path: str | None) -> Condition:
    if contract_path is None:
        return Condition("contract_resolved", True,
                         "no --contract given -- not applicable outside a real lane dispatch "
                         "(a heartbeat run dispatches no lane and has no contract file to "
                         "resolve); pass --contract PATH for a caller that has one",
                         f"{DEPLOYED_MODULE}:3115-3121,3153", gates=False)
    ok = Path(contract_path).is_file()
    detail = (f"contract resolved at {contract_path}" if ok else
              f"the contract did not resolve at {contract_path} -- the copy-in leg landed "
              "nothing")
    return Condition("contract_resolved", ok, detail, f"{DEPLOYED_MODULE}:3115-3121,3153")


def check_git_hooks_armed(root: Path) -> Condition:
    """ADDED, beyond the deployed test — see the module docstring for why. Reuses
    `scripts/arm_hooks.py`'s own predicate, the same one `provision.sh::assert_hooks_armed`
    already reuses, rather than a second answer to the same question."""
    sys.path.insert(0, str(root / "scripts"))
    try:
        import arm_hooks
    except ImportError:
        return Condition("git_hooks_armed", False,
                         "scripts/arm_hooks.py could not be imported -- cannot check hook state",
                         "ADDED (beyond the deployed test) -- reuses scripts/arm_hooks.py")
    hooks = arm_hooks._hooks_dir(root)
    if hooks is None:
        return Condition("git_hooks_armed", False,
                         "hooks directory unresolvable via `git rev-parse --git-path hooks`",
                         "ADDED (beyond the deployed test) -- reuses scripts/arm_hooks.py")
    ok = arm_hooks._armed(hooks)
    detail = (f"all three hook types (pre-commit/commit-msg/pre-push) armed at {hooks}" if ok
             else f"hook types not all present, pre-commit-managed, and current at {hooks} -- "
                  "a lane here would commit past a gate that never fires")
    return Condition("git_hooks_armed", ok, detail,
                     "ADDED (beyond the deployed test) -- reuses scripts/arm_hooks.py, the same "
                     "predicate provision.sh::assert_hooks_armed already reuses")


# --- the whole predicate ------------------------------------------------------------------------

@dataclass(frozen=True)
class AdmissionResult:
    ok: bool
    conditions: list[Condition] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1

    def failing(self) -> list[Condition]:
        return [c for c in self.conditions if c.gates and not c.ok]


def run_admission(root: Path, *, probe: Probe | None = None,
                  contract_path: str | None = None) -> AdmissionResult:
    """Would `Dispatch-Codespace` admit a lane into this container, right now? Never raises —
    every condition function above catches its own I/O failures and reports them as `ok=False`
    with a detail line, the same "refuse rather than crash the caller" posture every module in
    this family (`substrate_heartbeat.py`, `substrate_provenance.py`) already takes.
    """
    probe = probe or Probe()
    conditions = [
        check_claude_on_path(probe),
        check_uv_on_path(probe),
        check_python3_on_path(probe),
        check_pre_commit_on_path(probe),
        check_git_remote_reachable(root, probe),
        check_gh_not_broken(probe),
        check_git_hooks_armed(root),
        check_contract(contract_path),
    ]
    ok = all(c.ok for c in conditions if c.gates)
    return AdmissionResult(ok, conditions)


# --- CLI ------------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="codespace_admission.py",
        description="the Dispatch-Codespace admission predicate, extracted as one hub script "
                    "(LANE-5B2-23 / LANE-5B3-9)")
    parser.add_argument("--repo-root", default=str(_REPO_ROOT))
    parser.add_argument("--contract", default=None,
                        help="a lane contract path to check resolved -- omit outside a real "
                             "lane dispatch (a heartbeat run has none)")
    args = parser.parse_args(argv)
    root = Path(args.repo_root)

    result = run_admission(root, contract_path=args.contract)
    for c in result.conditions:
        tag = "OK    " if c.ok else ("NOTE  " if not c.gates else "REFUSED")
        logger.info("%s %-20s %s [%s]", tag, c.id, c.detail, c.cites)

    if result.ok:
        logger.info("admission: OK -- every gating condition satisfied; "
                    "Dispatch-Codespace would admit a lane here")
    else:
        names = ", ".join(c.id for c in result.failing())
        logger.error("admission: REFUSED -- %s", names)
    return result.exit_code


if __name__ == "__main__":       # pragma: no cover - exercised by the heartbeat workflow
    sys.exit(main())
