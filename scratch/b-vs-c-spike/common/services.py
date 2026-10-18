"""The service layer both prototypes call -- stdlib only, so it runs in either throwaway venv.

Every method calls a REAL verb in DRY-RUN and returns a plain dict. The two forms differ only in
what decides the next step from that dict; they share this file so the comparison is of the
FORM, not of the calls. Verbs touched (all read-only / dry-run / in-process with the spawn seam
faked): `dispatch.py queue --dry-run`, `dispatch.py launch --dry-run`, `dispatch.py plan`,
`claim.py claim|release` against a THROWAWAY transport, and `common/probe.py` for the pure
decision functions that have no CLI dry-run surface.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SPIKE = REPO / "scratch" / "b-vs-c-spike"
CONTRACTS = SPIKE / "contracts"
PROBE = SPIKE / "common" / "probe.py"


def _env() -> dict:
    env = dict(os.environ)
    env.pop("VIRTUAL_ENV", None)          # the hub's own locked env, not this throwaway venv
    env.pop("CLAUDE_PROMPTS_DIR", None)
    return env


def run(argv: list[str]) -> dict:
    p = subprocess.run(argv, cwd=REPO, env=_env(), capture_output=True, text=True, encoding="utf-8")
    return {"argv": " ".join(argv[:8]) + (" ..." if len(argv) > 8 else ""), "exit": p.returncode,
            "out": p.stdout.strip(), "err": p.stderr.strip()}


def uv(*args: str) -> dict:
    return run(["uv", "run", "--locked", "python", *args])


def cli(*args: str) -> dict:
    return uv("scripts/dispatch.py", *args)


def probe(cmd: str, **payload) -> dict:
    r = uv(str(PROBE.relative_to(REPO)), cmd, json.dumps(payload))
    if r["exit"] != 0:
        raise RuntimeError(f"probe {cmd} failed: {r['err'][-300:]}")
    return json.loads(r["out"].splitlines()[-1])


@dataclass
class Scenario:
    name: str
    contract: str                      # file name under contracts/
    all_contracts: tuple[str, ...] = ()
    states: dict = field(default_factory=dict)       # the integrator's STATE lines, as slug -> state
    live: tuple[str, ...] = ()
    cap: int = 4
    live_count: int = 0
    floor_mb: float = 3072.0
    free_mb: float | None = None       # None = a real read of this box's free memory
    claim_held_by_other: bool = False
    prelaunch: dict = field(default_factory=lambda: {"passed": True, "reason": ""})
    receipt: dict | None = None        # a planted earlier-launch receipt
    agents: tuple[dict, ...] = ()      # the literal `claude agents --json` listing
    spawn_returncode: int = 0
    expect_end: str = ""               # the terminal node id the code's behaviour implies
    expect_oracle: str = ""            # what the real launch_lane does ('' = not comparable)

    @property
    def slug(self) -> str:
        return Path(self.contract).stem[len("LANE-"):]

    @property
    def path(self) -> str:
        return str((CONTRACTS / self.contract).relative_to(REPO))

    @property
    def paths(self) -> list[str]:
        names = self.all_contracts or (self.contract,)
        return [str((CONTRACTS / n).relative_to(REPO)) for n in names]


_AGENT = {"id": "abc12345", "state": "running", "cwd": "/box/.claude/worktrees/spike-clean",
          "sessionId": "abc12345-0000-4000-8000-000000000000", "name": "spike-clean"}

SCENARIOS = {
    "S1-clean": Scenario("S1-clean", "LANE-spike-clean.md", expect_end="end_launched",
                         expect_oracle="launched"),
    "S2-refused": Scenario("S2-refused", "LANE-spike-refused.md", expect_end="end_refused"),
    "S3-already-launched": Scenario(
        "S3-already-launched", "LANE-spike-clean.md", expect_end="end_already_launched",
        expect_oracle="already-launched", agents=(_AGENT,),
        receipt={"job_id": "abc12345", "provider": "anthropic", "launched_at": "2026-10-18T10:00:00+00:00"}),
    "S4-prelaunch-refused": Scenario(
        "S4-prelaunch-refused", "LANE-spike-clean.md", expect_end="end_refused", expect_oracle="refused",
        prelaunch={"passed": False, "reason": "REFUSED [worktree_occupancy]: husk in .claude/worktrees/spike-clean"}),
    "S5-dependency-hold": Scenario(
        "S5-dependency-hold", "LANE-spike-dep.md", all_contracts=("LANE-spike-clean.md", "LANE-spike-dep.md"),
        expect_end="end_hold"),
    "S6-codespace-route": Scenario("S6-codespace-route", "LANE-spike-codespace.md",
                                   expect_end="end_routed_codespace"),
}


class Services:
    """One instance per scenario run. `calls` is the evidence that real verbs ran."""

    def __init__(self, sc: Scenario):
        self.sc = sc
        self.calls: list[dict] = []
        self._transport = Path(tempfile.mkdtemp(prefix="b-vs-c-transport-"))
        (self._transport / "to-cc").mkdir()
        self._claimed = False

    def _note(self, r: dict) -> dict:
        self.calls.append({"verb": r["argv"], "exit": r["exit"]})
        return r

    # --- E_start: the entry the code has for "what order, and does a cycle exist" -------------
    def schedule(self) -> dict:
        r = self._note(cli("queue", "--dry-run", *self.sc.paths))
        return {"ok": r["exit"] == 0, "detail": r["out"].splitlines()[1:] or r["err"]}

    # --- T_parse: contract table + Dispatch block must agree --------------------------------
    def parse_contract(self) -> dict:
        r = self._note(cli("launch", "--dry-run", self.sc.path))
        return {"ok": r["exit"] == 0, "exit": r["exit"], "detail": (r["err"] or r["out"])[:140]}

    # --- T_valid: provider / model / effort / branch guard / env, via `plan` ------------------
    def validate(self, substrate: str = "local") -> dict:
        args = ["plan", self.sc.path, "--token-cap", "1000000", "--substrate", substrate]
        if substrate == "codespace":
            args += ["--repo", "spike/spike"]
        r = self._note(cli(*args))
        return {"ok": r["exit"] == 0, "exit": r["exit"], "detail": (r["err"] or r["out"])[:140]}

    # --- T_tier: R101(a) is OWED; there is no code to call -------------------------------------
    def tier(self) -> dict:
        return {"ok": True, "hole": "R101(a) tier refusal is not built (lane_boot owes it); passes by default"}

    # --- T_claim: claim.py, against a throwaway transport -------------------------------------
    def claim(self) -> dict:
        name = f"LANE-{self.sc.slug}"
        if self.sc.claim_held_by_other:
            self._note(uv("scripts/claim.py", "--session", "other", "--transport-root", str(self._transport),
                          "claim", name))
        r = self._note(uv("scripts/claim.py", "--session", "spike0001", "--transport-root",
                          str(self._transport), "claim", name))
        self._claimed = r["exit"] == 0
        return {"ok": r["exit"] == 0, "exit": r["exit"], "detail": r["out"][:100] or r["err"][:100]}

    # --- the queue's gates ---------------------------------------------------------------------
    def dependency(self) -> dict:
        return probe("dep", contracts=self.sc.paths, slug=self.sc.slug, states=self.sc.states)

    def serialize(self) -> dict:
        return probe("serial", contracts=self.sc.paths, slug=self.sc.slug, live=list(self.sc.live))

    def substrate(self) -> dict:
        return probe("substrate", contract=self.sc.path)

    def cap_ram(self) -> dict:
        return probe("capram", contracts=self.sc.paths, slug=self.sc.slug, cap=self.sc.cap,
                     live_count=self.sc.live_count, floor_mb=self.sc.floor_mb, free_mb=self.sc.free_mb)

    def route_codespace(self) -> dict:
        r = self._note(cli("plan", self.sc.path, "--token-cap", "1000000", "--substrate", "codespace",
                           "--repo", "spike/spike"))
        steps = json.loads(r["out"])["steps"] if r["exit"] == 0 else []
        return {"ok": r["exit"] == 0, "steps": len(steps), "detail": (r["err"] or "")[:140]}

    # --- launch_lane's own pieces ---------------------------------------------------------------
    def prelaunch(self) -> dict:
        # INJECTED, not run: `doit moment:pre-launch` reads live worktrees and sessions; this lane
        # runs no live organ. The verdict is the scenario's, and the trace says so.
        return {"passed": self.sc.prelaunch["passed"], "reason": self.sc.prelaunch["reason"], "injected": True}

    def held(self) -> dict:
        return probe("held", slug=self.sc.slug, receipt=self.sc.receipt, agents=list(self.sc.agents))

    def spawn(self) -> dict:
        return probe("spawn", contract=self.sc.path, returncode=self.sc.spawn_returncode)

    def identify(self, stdout: str) -> dict:
        return probe("identify", contract=self.sc.path, stdout=stdout)

    def receipt(self, job_id: str, session_id: str, name: str) -> dict:
        return probe("receipt", contract=self.sc.path, job_id=job_id, session_id=session_id, name=name)

    # --- the oracle: the real launch_lane, spawn faked ------------------------------------------
    def oracle(self) -> dict:
        return probe("oracle", contract=self.sc.path, prelaunch=self.sc.prelaunch, receipt=self.sc.receipt,
                     agents=list(self.sc.agents))

    def close(self) -> None:
        if self._claimed:
            uv("scripts/claim.py", "--session", "spike0001", "--transport-root", str(self._transport),
               "release", f"LANE-{self.sc.slug}")
        shutil.rmtree(self._transport, ignore_errors=True)   # no leftovers
