"""lane-connection-test (wave-3 W3-F, goal G1): is the harness connected? One toy task, the whole loop, a receipt per moment.

WHAT IT DOES. It builds a THROWAWAY repository (a copy of this hub's tracked tree, its own bare `origin`, its own
seat registry, its own transport folder) and walks ONE toy task through the loop:

    spine stages 1-12 -> `dispatch.py launch` -> pre-launch -> lane-start -> a fixture lane that commits and writes its
    HANDBACK line -> lane-end (through the REAL Stop-hook guard) -> merge (with a fixture GO file) -> push -> teardown
    -> batch-close

Every moment is the real `doit -f scripts/dodo.py moment:<name>` reading the real `ecosystem/harness.yaml`; every
organ is the real script. Only two things are faked: the provider PROCESS (`dispatch.spawn_process`, the one process
boundary the launcher documents) and the git REMOTE (a local bare repository standing in for origin).

THE ASSERTION IS THE RECEIPTS: one per organ of every moment, in order, each exit 0, and the batch digest naming the
task. Where a moment does not fire, the walk records a `Stop` (moment, organ, receipt, detail) and CONTINUES the later
moments -- each given its best legitimate chance, as if an operator had overridden the stop -- so the queue of stops
is complete rather than first-only. `test_the_loop_stops_where_the_walk_recorded` pins that queue; the strict-xfail
`test_one_toy_task_leaves_a_receipt_at_every_moment_in_order` is what goes green (XPASS-strict -> red -> delete the
marker) when the loop is actually connected. A stop is the deliverable, not a failure to hide (Done-contract 6).

FIXTURE-ONLY SUBSTITUTIONS, each named so it is not mistaken for a mock of a moment or an organ:
  * HOME (USERPROFILE) is redirected so the seat registry, the session store (transcripts), the L0 routing copy and
    `~/.claude/jobs` are the test's own. The L0 copy is rendered by the repo's own `routing_agreement.py --render`.
  * On Windows the User-scope `CLAUDE_PROMPTS_DIR` wins over the environment, so `tests/fixtures/connection_loop/
    sitecustomize.py` redirects that ONE registry read to the test's transport. Without it `go_reader` and the lane-end
    report would touch the operator's live transport; `live_transport_touched` proves they did not.
  * The integrator "command" is a markdown chain (`.claude/commands/lane-integrate.md`), not a script, so `integrate()`
    runs its steps: open, handback verdict, `merge --no-ff`, `moment:merge`, push, teardown, `moment:teardown`. NOT run:
    `race` (it launches the full suite plus a reviewer) and `actions` (it reads GitHub Actions).
"""
from __future__ import annotations

import contextlib
import functools
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

import pytest
import yaml
from click.testing import CliRunner

logger = logging.getLogger("connection-loop")

_HUB = Path(__file__).resolve().parents[1]
_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "connection_loop"
_HARNESS = _HUB / "ecosystem" / "harness.yaml"
_LIGHT_TREE = ("scripts", "ecosystem", "pyproject.toml", "uv.lock", ".python-version", ".gitignore")

BATCH = "TOYBATCH"
SUBJECT = "toy-connection"
FEATURE_COMMIT = f"feat: {SUBJECT} -- the toy change"
INTEGRATOR_SESSION = "toy-integrator"
NEGATIVE_SLUG = "lane-20260921-wire-toy-negative"
STOP_TIMEOUT_S = 1800

#: Done-contract 4/5: this module's tests are NOT independently parallelizable -- exactly one heavy
#: operation (the shared walk, or a negative-path test) may hold the host's uv/git/doit subprocess
#: tree at a time (`_exclusive` below already serializes them against EACH OTHER), so a second xdist
#: WORKER PROCESS sitting alongside it adds pure overhead: another Python interpreter with the full
#: `dispatch`/`audit`/`click`/`pyyaml` import graph loaded, live at the exact moment the walk's own
#: subprocess tree peaks. On a host already thin on headroom (this box: ~3.7 GB free of 27.7 GB,
#: shared with sibling batch lanes) that fixed second-worker cost was enough to occasionally tip a
#: post-spawn step of `dispatch.py launch` (inside the ONE real walk, read identically by every
#: consumer -- `_exclusive`'s lock already rules out a second, divergent walk ever being computed)
#: into a bare uncaught exception, which Click's CliRunner reports as exit 1 with no organ to blame
#: -- the "launch-step trio" (`launched_once...`, `human_writes...`, `loop_stops...`) all read that
#: SAME single walk and fail together. `xdist_group` pins every test in this module to ONE worker:
#: under `-n 2` the second worker simply never loads this module's import graph, which is the
#: shared-state cost actually inside this module's control (the box's own headroom is not).
pytestmark = [pytest.mark.slow, pytest.mark.xdist_group(name="connection_loop")]

#: The stops the walk recorded when W3-F ran (2026-09-21). Pinned so a change in EITHER direction is loud: a stop that
#: disappears means wave 4 fixed it (delete its row); a new one means the loop moved. Each row is (moment, organ).
EXPECTED_STOPS = (("merge", "gates"), ("batch-close", "digest-names-the-task"))


# --- domain: Receipt, Step, Stop ---------------------------------------------------------------------------------------

@dataclass(frozen=True)
class OrganReceipt:
    """One organ's receipt as its moment wrote it."""
    moment: str
    organ: str
    receipt: str
    status: str
    exit_code: Optional[int]
    mtime_ns: int

    @property
    def fired(self) -> bool:
        return self.status == "ok" and self.exit_code == 0


@dataclass(frozen=True)
class Stop:
    """Where the loop did not fire: the moment, the organ, the receipt that says so, and why.

    `fixture_artifacts` names known TOY-COPY-ONLY causes bundled into this same red (Done-contract
    2) -- e.g. a commit-date check that fails because the throwaway repo has one "seed" commit, not
    real history. Empty for a stop that is (as far as this walk can tell) entirely the loop's own."""
    moment: str
    organ: str
    receipt: str
    detail: str
    fixture_artifacts: tuple[str, ...] = ()


@dataclass
class Step:
    """One moment as walked: its exit code and the receipts of every organ it declares (missing ones named)."""
    moment: str
    exit_code: int
    organs: list[OrganReceipt] = field(default_factory=list)
    unreached: list[str] = field(default_factory=list)

    @property
    def stop(self) -> Optional[Stop]:
        for organ in self.organs:
            if not organ.fired:
                return Stop(self.moment, organ.organ, organ.receipt,
                            f"receipt status {organ.status!r}, exit_code {organ.exit_code} (moment exit {self.exit_code})")
        if self.unreached:
            return Stop(self.moment, self.unreached[0], "(no receipt)",
                        f"organ never ran (moment exit {self.exit_code}); not reached: {', '.join(self.unreached)}")
        if self.exit_code != 0:
            return Stop(self.moment, "(moment)", "(none)", f"every organ receipt is ok but the moment exited {self.exit_code}")
        return None


@dataclass
class Walk:
    """The whole loop as walked once: steps in order, the stops, and what a human had to write."""
    slug: str = ""
    steps: list[Step] = field(default_factory=list)
    stops: list[Stop] = field(default_factory=list)
    human_writes: list[dict] = field(default_factory=list)
    standing: list[str] = field(default_factory=list)
    digest: str = ""
    live_transport_touched: Optional[bool] = None
    integrator: dict = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, text: str) -> "Walk":
        raw = json.loads(text)
        raw["steps"] = [Step(s["moment"], s["exit_code"], [OrganReceipt(**o) for o in s["organs"]], s["unreached"])
                        for s in raw["steps"]]
        raw["stops"] = [Stop(**{**s, "fixture_artifacts": tuple(s.get("fixture_artifacts", ()))})
                       for s in raw["stops"]]
        return cls(**raw)


def _declared() -> dict:
    return yaml.safe_load(_HARNESS.read_text(encoding="utf-8"))


def _declared_moment(name: str) -> dict:
    return next(m for m in _declared()["moments"] if m["name"] == name)


def _read_receipt(path: Path) -> Optional[dict]:
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return body if isinstance(body, dict) else None


def _slug_of(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").upper()


# --- the fake provider: the ONE process boundary ---------------------------------------------------------------------

class FakeProvider:
    """Stands in for `claude --bg`: records the argv, creates the lane worktree the real CLI would, lists the job."""

    def __init__(self) -> None:
        self.calls: list[list[str]] = []
        self.agents: list[dict] = []

    def spawn(self, argv, env, cwd, log_path=None):
        import dispatch as d  # noqa: PLC0415
        self.calls.append(list(argv))
        slug = argv[argv.index("--worktree") + 1]
        worktree = Path(cwd) / ".claude" / "worktrees" / slug
        subprocess.run(["git", "worktree", "add", "-q", "-b", f"worktree-{slug}", str(worktree)], cwd=str(cwd),
                       check=True, capture_output=True)
        self.agents.append({"id": "c0ffee01", "name": slug, "sessionId": "c0ffee01-toy-session", "state": "running",
                            "status": "busy", "cwd": str(worktree)})
        return d.Spawned(0, "Backgrounded \u2014 c0ffee01\n", None)

    def listing(self) -> list[dict]:
        return list(self.agents)


# --- the world ------------------------------------------------------------------------------------------------------

class World:
    """A throwaway repository, its bare origin, a home, a transport and a fake `claude` -- nothing of the operator's."""

    def __init__(self, root: Path, *, full: bool) -> None:
        self.root = root
        self.full = full
        self.repo = root / "repo"
        self.origin = root / "origin.git"
        self.home = root / "home"
        self.transport = root / "transport"
        self.bin = root / "bin"
        self.human_writes: list[dict] = []
        self.standing: list[str] = []

    # environment ----------------------------------------------------------------------------------------------------
    def env(self, **extra: str) -> dict[str, str]:
        base = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV" and not k.startswith("HARNESS_")}
        base.update(
            UV_PROJECT_ENVIRONMENT=sys.prefix, PYTHONUTF8="1", USERPROFILE=str(self.home), HOME=str(self.home),
            CT_TRANSPORT=str(self.transport), CLAUDE_PROMPTS_DIR=str(self.transport),
            DEV_KNOWLEDGE_TELEMETRY_DB=str(self.root / "telemetry.db"),
            PATH=os.pathsep.join([str(self.bin), str(Path(sys.executable).parent), base.get("PATH", "")]),
            PYTHONPATH=os.pathsep.join([str(_FIXTURES), base.get("PYTHONPATH", "")]))
        base.update(extra)
        return base

    def run(self, argv, cwd: Optional[Path] = None, **extra: str) -> subprocess.CompletedProcess:
        started = time.monotonic()
        done = subprocess.run([str(a) for a in argv], cwd=str(cwd or self.repo), env=self.env(**extra), text=True,
                              capture_output=True, encoding="utf-8", errors="replace", timeout=STOP_TIMEOUT_S)
        logger.info("$ %s [%s] -> %s in %.1fs", " ".join(map(str, argv))[:120], (cwd or self.repo).name,
                    done.returncode, time.monotonic() - started)
        return done

    def git(self, *args: str, cwd: Optional[Path] = None) -> str:
        done = self.run(["git", *args], cwd=cwd)
        assert done.returncode == 0, f"git {' '.join(args)} failed in {cwd or self.repo}: {done.stderr}"
        return done.stdout.strip()

    def uv(self, *args: str, cwd: Optional[Path] = None, **extra: str) -> subprocess.CompletedProcess:
        return self.run(["uv", "run", "--locked", *args], cwd=cwd, **extra)

    # construction ---------------------------------------------------------------------------------------------------
    def build(self) -> "World":
        self._copy_tree()
        self.git("init", "-q", "-b", "main")
        for key, value in (("user.email", "toy@example.invalid"), ("user.name", "toy"), ("core.autocrlf", "false")):
            self.git("config", key, value)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "seed")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(self.origin)], check=True, capture_output=True)
        self.git("remote", "add", "origin", str(self.origin))
        self.git("push", "-q", "origin", "main")
        for folder in (self.home / ".claude" / "jobs", self.transport / "to-cc", self.transport / "to-browser", self.bin):
            folder.mkdir(parents=True, exist_ok=True)
        self.standing.append("`~/.claude/jobs` exists (no_leftovers reads it; an absent directory is 'unreadable')")
        self._fake_claude()
        # NOT armed here, and that absence is deliberate, not an oversight (Done-contract 2):
        # `scripts/arm_hooks.py` was tried and reverted -- it installs REAL pre-push hooks
        # (block-ff-push, block-unanchored-push), and this fixture's own bootstrap choreography
        # (write_task's direct push to its own origin/main, the post-merge "chore: merge
        # receipts" push) is exactly the direct-to-main shape those hooks exist to refuse. Arming
        # them breaks the fixture that is supposed to be exercising the loop, not gating itself.
        # `hooks_armed` is therefore recorded as FIXTURE-ARTIFACT (`_FIXTURE_ARTIFACT_MARKERS`)
        # rather than armed -- the Done-contract's other sanctioned path.
        self._render_l0_routing_copy()
        self._bind_integrator()
        return self

    def _copy_tree(self) -> None:
        self.repo.mkdir(parents=True)
        if self.full:
            listing = subprocess.run(["git", "ls-files", "-z"], cwd=str(_HUB), capture_output=True, check=True)
            names = [n.decode() for n in listing.stdout.split(b"\0") if n]
        else:
            names = [str(p.relative_to(_HUB)) for entry in _LIGHT_TREE for p in
                     ([_HUB / entry] if (_HUB / entry).is_file() else (_HUB / entry).rglob("*"))
                     if p.is_file() and "__pycache__" not in p.parts]
        for name in names:
            source = _HUB / name
            if source.is_file():
                (self.repo / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, self.repo / name)

    def _fake_claude(self) -> None:
        """`claude agents --json` -> `[]`. The launcher's own listing is replaced in-process (FakeProvider)."""
        if os.name == "nt":
            (self.bin / "claude.cmd").write_text("@echo off\r\necho []\r\n", encoding="utf-8")
        else:
            exe = self.bin / "claude"
            exe.write_text("#!/bin/sh\necho '[]'\n", encoding="utf-8")
            exe.chmod(0o755)

    def _render_l0_routing_copy(self) -> None:
        rendered = self.uv("python", "scripts/routing_agreement.py", "--render")
        assert rendered.returncode == 0, rendered.stderr
        (self.home / ".claude" / "ROUTING.md").write_text(rendered.stdout, encoding="utf-8")
        self.standing.append("L0 routing copy `~/.claude/ROUTING.md` (rendered by routing_agreement.py --render); "
                             "absent on a fresh host, where pre-launch and spine stage 8 refuse")

    def _bind_integrator(self) -> None:
        """A real `bind` and a real SessionStart hook event through the registry's own writers."""
        import seat_registry as registry  # noqa: PLC0415
        path = self.home / ".claude" / "seat-registry.jsonl"
        registry.bind("integrator", BATCH, session_id=INTEGRATOR_SESSION, path=path)
        registry.record_event({"hook_event_name": "SessionStart", "session_id": INTEGRATOR_SESSION,
                               "cwd": str(self.repo)}, path=path)
        self.standing.append(f"integrator seat bound and live for batch {BATCH} (seat_registry bind + a SessionStart event)")

    # what a human writes --------------------------------------------------------------------------------------------
    def operator_writes(self, kind: str, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="")
        self.human_writes.append({"kind": kind, "path": str(path)})

    def write_task(self) -> None:
        """The task: one BUILD-LIST row (spine stage 1 reads it; stage 4 distills the contract from it)."""
        build_list = self.repo / "protocols" / "BUILD-LIST.md"
        lines = build_list.read_text(encoding="utf-8").splitlines(keepends=True)
        header = next(i for i, ln in enumerate(lines) if ln.startswith("| subject | context-cost"))
        row = f"| {SUBJECT} | 1 KB · reduces: no | `scripts/dodo.py` (code) | WIRE | nothing | S | no |\n"
        lines.insert(header + 2, row)
        self.operator_writes("task", build_list, "".join(lines))
        self.git("add", "-A")
        self.git("commit", "-q", "-m", f"docs: task row {SUBJECT}")
        self.git("push", "-q", "origin", "main")

    def write_go(self) -> Path:
        go = self.transport / "to-cc" / f"GO-{BATCH}.md"
        self.operator_writes("go", go, "GO\n")
        return go

    # moments --------------------------------------------------------------------------------------------------------
    def moment(self, name: str, cwd: Optional[Path] = None, **extra: str) -> Step:
        cwd = cwd or self.repo
        done = self.uv("doit", "-f", "scripts/dodo.py", f"moment:{name}", cwd=cwd, **extra)
        return self._step(name, done.returncode, cwd / "logs" / "receipts",
                          [(o["id"], o["receipt"]) for o in self._declared_organs(name)])

    def spine(self) -> Step:
        done = self.uv("doit", "-f", "scripts/dodo.py", "spine", HARNESS_KIND="WIRE", HARNESS_SUBJECT=SUBJECT)
        expected = [(s["name"], f"SPINE-{s['stage']:02d}-{_slug_of(s['name'])}.json") for s in _declared()["stages"]]
        return self._step("spine", done.returncode, self.repo / "logs" / "receipts", expected)

    @staticmethod
    def _declared_organs(moment: str) -> list[dict]:
        declared = _declared_moment(moment)
        pre = declared.get("precondition")
        return ([{"id": "precondition", "receipt": pre["receipt"]}] if pre else []) + list(declared["organs"])

    @staticmethod
    def _step(name: str, exit_code: int, receipts: Path, expected: list[tuple[str, str]]) -> Step:
        step = Step(name, exit_code)
        for organ, receipt in expected:
            path = receipts / receipt
            body = _read_receipt(path)
            if body is None:
                step.unreached.append(organ)
                continue
            step.organs.append(OrganReceipt(name, organ, receipt, str(body.get("status")), body.get("exit_code"),
                                            path.stat().st_mtime_ns))
        return step

    # launch ---------------------------------------------------------------------------------------------------------
    def launch(self, contract: Path, provider: FakeProvider, mp: pytest.MonkeyPatch):
        """`dispatch.py launch` through its own click command, with the provider process and listing replaced."""
        import dispatch as d  # noqa: PLC0415
        real_prelaunch = d.run_prelaunch
        for key, value in self.env().items():
            mp.setenv(key, value)
        mp.setenv("HARNESS_RECEIPTS_DIR", str(self.repo / "logs" / "receipts"))
        mp.chdir(self.repo)
        mp.setattr(d, "spawn_process", provider.spawn)
        mp.setattr(d, "list_agents", provider.listing)
        mp.setattr(d, "run_prelaunch", functools.partial(real_prelaunch, hub=self.repo))
        return CliRunner().invoke(d.cli, ["launch", str(contract), "--batch", BATCH])

    # the fixture lane -----------------------------------------------------------------------------------------------
    def lane_commit(self, worktree: Path) -> str:
        (worktree / "toy_feature.txt").write_text("the toy change\n", encoding="utf-8")
        self.git("add", "-A", cwd=worktree)
        self.git("commit", "-q", "-m", FEATURE_COMMIT, cwd=worktree)
        return self.git("rev-parse", "--short", "HEAD", cwd=worktree)

    def lane_transcript(self, worktree: Path, model: str = "claude-opus-5") -> None:
        """The session store files a lane's transcript under its working directory; `merge_receipt models` reads it."""
        import routing_agreement as ra  # noqa: PLC0415
        folder = self.home / ".claude" / "projects" / ra.session_slug(worktree)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "toy-lane-session.jsonl").write_text(
            json.dumps({"type": "assistant", "message": {"model": model, "usage": {"input_tokens": 10,
                                                                                    "output_tokens": 5}}}) + "\n",
            encoding="utf-8")

    def session_file(self, slug: str) -> Path:
        return self.transport / "to-browser" / f"SESSION-{slug}.md"

    def write_session(self, slug: str, sha: Optional[str]) -> str:
        """The lane's session file. With `sha` it closes with the HANDBACK line a conforming lane writes."""
        line = f"HANDBACK worktree-{slug} @ {sha} code review=codex HIGH:0 MED:0 LOW:0" if sha else ""
        self.session_file(slug).write_text(f"# SESSION {slug}\n\nthe toy lane's report\n\n{line}\n", encoding="utf-8")
        return line

    def stop_hook(self, worktree: Path) -> None:
        """Run the Stop entry `.claude/settings.json` declares for the lane-end guard, as the harness does: through a
        POSIX shell with CLAUDE_PROJECT_DIR set to the lane's directory. Then wait for the detached worker to finish."""
        settings = json.loads((_HUB / ".claude" / "settings.json").read_text(encoding="utf-8"))
        commands = [h["command"] for group in settings["hooks"]["Stop"] for h in group["hooks"]
                    if "lane_end_guard.py" in h.get("command", "")]
        assert len(commands) == 1, "settings.json must declare exactly one lane_end_guard Stop entry"
        shell = next((c for c in (r"C:\Program Files\Git\bin\bash.exe", shutil.which("bash"), shutil.which("sh"))
                      if c and Path(c).exists()), None)
        assert shell, "no POSIX shell to run the declared Stop command"
        self.run([shell, "-c", commands[0]], cwd=worktree, CLAUDE_PROJECT_DIR=worktree.as_posix())
        receipt = worktree / "logs" / "receipts" / "MOMENT-LANE-END-HOOK.json"
        deadline = time.monotonic() + 300
        while time.monotonic() < deadline:
            body = _read_receipt(receipt)
            if body and body.get("status") != "running":
                return
            time.sleep(1)

    # the integrator's chain -----------------------------------------------------------------------------------------
    def integrate_merge(self, slug: str, contract: Path, handback: str) -> tuple[Optional[str], dict]:
        """open -> handback verdict -> `merge --no-ff` (the HARNESS_* for `moment:merge` are `merge_env`).

        A refused handback verdict is a REFUSAL, as lane-integrate.md has it: nothing is merged and `(None, info)` comes
        back, so no later step is simulated on top of a merge the integrator would not have made."""
        opened = self.uv("python", "scripts/merge_receipt.py", "open", "--slug", slug, "--batch", BATCH)
        assert opened.returncode == 0, opened.stderr
        verdict = self.uv("python", "scripts/audit.py", "handback", handback)
        info = {"handback_verdict_exit": verdict.returncode,
                "handback_verdict_out": (verdict.stdout + verdict.stderr).strip()[-300:]}
        if verdict.returncode != 0:
            return None, info
        merged = self.run(["git", "merge", "--no-ff", "-m", f"Merge branch 'worktree-{slug}'\n\nkill-candidates: none",
                           f"worktree-{slug}"])
        assert merged.returncode == 0, merged.stderr
        return self.git("rev-parse", "HEAD"), info

    def merge_env(self, slug: str, contract: Path, handback: str, merge: str) -> dict[str, str]:
        return {"HARNESS_LANE": slug, "HARNESS_BATCH": BATCH, "HARNESS_CONTRACT": str(contract),
                "HARNESS_HANDBACK": handback, "HARNESS_CHANGED": merge, "HARNESS_MERGE": merge}


def _fresh_world(tmp_path_factory: pytest.TempPathFactory, name: str, *, full: bool) -> World:
    return World(tmp_path_factory.mktemp(name), full=full).build()


def _transport_fingerprint() -> Optional[dict[str, tuple[int, int]]]:
    """name -> (size, mtime_ns) of toy-looking files on the operator's REAL transport (None when unresolvable)."""
    try:
        import dispatch as d  # noqa: PLC0415
        base = d.prompts_dir()
    except Exception:  # noqa: BLE001 -- an unresolvable live transport is simply not observable here
        return None
    if not base.is_dir():
        return None
    return {f"{folder}/{p.name}": (p.stat().st_size, p.stat().st_mtime_ns)
            for folder in ("to-cc", "to-browser") if (base / folder).is_dir()
            for p in (base / folder).glob("*") if "toy" in p.name.lower() or BATCH in p.name}


def _registry_redirect(world: World) -> str:
    """Ask a CHILD process (the way every organ runs) where the User-scope transport is: the shim must answer with the
    test's own folder. `not-applicable` off Windows, where there is no registry read to redirect."""
    if os.name != "nt":
        return "not-applicable"
    probe = world.run([sys.executable, "-c", "import sys; sys.path.insert(0, 'scripts'); import transport_report as t; "
                       "print(t.windows_user_env('CLAUDE_PROMPTS_DIR'))"])
    got = probe.stdout.strip()
    return "verified" if got == str(world.transport) else f"BROKEN: child sees {got!r}, not {world.transport}"


# --- the walk -------------------------------------------------------------------------------------------------------

def walk_the_loop(tmp_path_factory: pytest.TempPathFactory) -> Walk:
    """Walk ONE toy task through the loop, recording every moment's receipts and every stop."""
    live_before = _transport_fingerprint()
    world = _fresh_world(tmp_path_factory, "connection_world", full=True)
    walk = Walk()
    walk.integrator["registry_redirect"] = _registry_redirect(world)
    with pytest.MonkeyPatch.context() as mp:
        _walk(world, walk, mp)
    walk.human_writes, walk.standing = world.human_writes, world.standing
    live_after = _transport_fingerprint()
    walk.live_transport_touched = None if live_before is None or live_after is None else live_before != live_after
    return walk


def _record(walk: Walk, step: Step) -> Step:
    """Add a moment to the walk in order, and its stop (if it did not fire) to the queue."""
    walk.steps.append(step)
    if step.stop:
        walk.stops.append(step.stop)
    return step


#: Known TOY-COPY-ONLY causes, keyed by the gates.py row (audit-health = commit tier,
#: ship-gate = ship tier) they surface in -- Done-contract 2. Each name is a `check_name` gates.py
#: parses out of that gate's FULL output as a structured `findings` entry (FR4) -- not a text
#: marker searched for as a substring. `canonical_freshness` and `journal_spine_anchor` are tied to
#: the throwaway repo having ONE "seed" commit rather than real history (commit-date-driven);
#: `funnel_lifecycle` is the same class per SESSION-lane-connection-test.md's own account.
#: `hooks_armed` was TRIED as arm-instead-of-record (installing real pre-commit/pre-push hooks via
#: scripts/arm_hooks.py) and reverted: those hooks then refuse this fixture's own direct-to-main
#: bootstrap pushes (write_task, the post-merge "chore: merge receipts" push), breaking the harness
#: that is supposed to be exercising the loop. Recording is the sanctioned alternative Done-contract
#: 2 names, and it is the one used here. NEVER list `organ_truth`: it is the real, same cause the
#: live integrator records -- Done-contract 2's "the loop's real stops stay visible" is exactly the
#: invariant this exclusion protects.
_FIXTURE_ARTIFACT_MARKERS: dict[str, tuple[str, ...]] = {
    "audit-health": ("canonical_freshness", "journal_spine_anchor", "hooks_armed"),
    "ship-gate": ("funnel_lifecycle",),
}


def _fixture_artifacts_in(verdict: Optional[dict]) -> tuple[str, ...]:
    """`f"{gate}:{check_name}"` for each known toy-copy-only cause found in a RED gate's
    STRUCTURED findings (Done-contract 3, FR4) -- `gates.py`'s own `findings` list on the verdict
    it already wrote (`MOMENT-MERGE-GATES-VERDICT.json`), one `{check_name, status, evidence}`
    entry per hard-fail/warning `gates.py` parsed from that gate's FULL output. Never a second
    probe run (that would double the subprocess cost `_exclusive` exists to bound), and never a
    substring search over a truncated `output_tail` -- that missed markers that printed before the
    tail's window (WAVE4-FINAL digest, finding 4): a name is either IN the structured list or it
    is not, independent of where in the gate's output it happened to print."""
    if not verdict:
        return ()
    found: list[str] = []
    for row in verdict.get("gates", []):
        if row.get("exit_code") == 0:
            continue
        names = {f.get("check_name") for f in row.get("findings", []) if isinstance(f, dict)}
        for marker in _FIXTURE_ARTIFACT_MARKERS.get(row.get("name", ""), ()):
            if marker in names:
                found.append(f"{row['name']}:{marker}")
    return tuple(found)


def _assert_transport_untouched(live_before: Optional[dict]) -> None:
    """Done-contract 5: transport isolation proven before AND after every heavy run, not just
    the walk. `live_before` is `None`-safe (an unresolvable live transport is simply not
    observable, per `_transport_fingerprint`'s own contract) so this degrades the same way."""
    live_after = _transport_fingerprint()
    assert live_before is None or live_after is None or live_before == live_after, \
        "this run wrote toy files onto the operator's live transport"


def _label_fixture_artifacts(walk: Walk, world: World) -> None:
    """If the walk just stopped at merge/gates, split any known toy-copy-only causes out of that
    same red into `Stop.fixture_artifacts`, so a reader is not left to guess which part is the
    loop and which part is the copy (Done-contract 2)."""
    if not (walk.stops and walk.stops[-1].moment == "merge" and walk.stops[-1].organ == "gates"):
        return
    verdict = _read_receipt(world.repo / "logs" / "receipts" / "MOMENT-MERGE-GATES-VERDICT.json")
    artifacts = _fixture_artifacts_in(verdict)
    if not artifacts:
        return
    last = walk.stops[-1]
    walk.stops[-1] = Stop(last.moment, last.organ, last.receipt,
                          last.detail + f" -- FIXTURE-ARTIFACT (toy-copy-only, not a loop stop): "
                                        f"{', '.join(artifacts)}",
                          fixture_artifacts=artifacts)


def _label_launch_failure(walk: Walk, launched) -> None:
    """If the walk just stopped at pre-launch, attach `dispatch.py launch`'s own CliRunner output
    (and exception, if the CLI raised something Click did not turn into a typed exit code) to the
    Stop's detail. `Step.stop`'s generic "every organ receipt is ok but the moment exited N" names
    no organ to blame BY DESIGN when every declared pre-launch organ's receipt is green (Done-
    contract 4) -- that shape is exactly what a bare, uncaught exception in `launch_cmd` AFTER a
    successful spawn produces (Click's `CliRunner` reports exit 1 for anything that is not a typed
    `DispatchRefused` subclass), and without the CLI's own text a reader has nothing to go on."""
    if not (walk.stops and walk.stops[-1].moment == "pre-launch"):
        return
    detail = (launched.output or "").strip()
    if launched.exception is not None:
        detail = (detail + f"\nexception: {launched.exception!r}").strip()
    if not detail:
        return
    last = walk.stops[-1]
    walk.stops[-1] = Stop(last.moment, last.organ, last.receipt,
                          last.detail + " -- dispatch.py launch's own output: " + detail[-2000:],
                          fixture_artifacts=last.fixture_artifacts)


def _walk(world: World, walk: Walk, mp: pytest.MonkeyPatch) -> None:
    world.write_task()
    _record(walk, world.spine())
    contract_text = (world.repo / "logs" / "receipts" / "SPINE-12-CONTRACT-OUTPUT.txt").read_text(encoding="utf-8")
    slug = re.search(r"^# LANE (\S+)", contract_text, re.M).group(1)
    walk.slug = slug
    contract = world.transport / f"LANE-{slug.removeprefix('lane-')}.md"
    contract.write_text(contract_text.lstrip(), encoding="utf-8")   # the spine's stage-12 contract, delivered to the transport

    provider = FakeProvider()
    launched = world.launch(contract, provider, mp)
    pre = world._step("pre-launch", launched.exit_code, world.repo / "logs" / "receipts",
                      [(o["id"], o["receipt"]) for o in world._declared_organs("pre-launch")])
    _record(walk, pre)
    _label_launch_failure(walk, launched)
    walk.integrator["launch_exit"] = launched.exit_code
    walk.integrator["spawns"] = len(provider.calls)
    if launched.exit_code != 0 or not provider.calls:
        return          # nothing was launched, so there is no lane to walk (a stop, recorded above)
    worktree = world.repo / ".claude" / "worktrees" / slug

    _record(walk, world.moment("lane-start", cwd=worktree))
    sha = world.lane_commit(worktree)
    world.lane_transcript(worktree)
    handback = world.write_session(slug, sha)
    world.stop_hook(worktree)
    _record(walk, world._step("lane-end", 0, worktree / "logs" / "receipts",
                              [(o["id"], o["receipt"]) for o in world._declared_organs("lane-end")]))

    world.write_go()
    merge_sha, verdict = world.integrate_merge(slug, contract, handback)
    walk.integrator.update(verdict, merge=merge_sha)
    if merge_sha is None:      # the integrator refuses a handback it cannot verdict: no merge, nothing after it
        walk.stops.append(Stop("integrate", "handback-verdict", "(audit.py handback)", verdict["handback_verdict_out"]))
        return
    _record(walk, world.moment("merge", **world.merge_env(slug, contract, handback, merge_sha)))
    _label_fixture_artifacts(walk, world)

    # From here the walk CONTINUES past a stop: each later moment gets its best legitimate chance.
    world.uv("python", "scripts/merge_receipt.py", "close", "--slug", slug)
    world.git("add", "-A")
    world.git("commit", "-q", "-m", "chore: merge receipts\n\nkill-candidates: none")
    world.git("push", "-q", "origin", "main")
    world.git("worktree", "remove", f".claude/worktrees/{slug}")
    world.git("worktree", "prune")
    world.git("branch", "-d", f"worktree-{slug}")
    _record(walk, world.moment("teardown", HARNESS_LANE=slug, HARNESS_BATCH=BATCH))
    _record(walk, world.moment("batch-close", HARNESS_LANE=slug, HARNESS_BATCH=BATCH))
    output = world.repo / "logs" / "receipts" / "MOMENT-BATCH-CLOSE-DIGEST-OUTPUT.txt"
    walk.digest = output.read_text(encoding="utf-8", errors="replace") if output.is_file() else ""
    if slug not in walk.digest and SUBJECT not in walk.digest:     # a requirement of the loop, kept apart from the receipt
        walk.stops.append(Stop("batch-close", "digest-names-the-task", "MOMENT-BATCH-CLOSE-DIGEST-OUTPUT.txt",
                               "the declared digest organ exited 0 and named the batch, never the task or its commits"))


def _run_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """This test RUN's shared folder -- one per invocation of pytest, common to every
    xdist worker, never a stale one from an earlier run (a worker's own basetemp is
    `.../popen-gwN`; its PARENT is what every worker of THIS run shares)."""
    base = tmp_path_factory.getbasetemp()
    return base.parent if os.environ.get("PYTEST_XDIST_WORKER") else base


@contextlib.contextmanager
def _exclusive(tmp_path_factory: pytest.TempPathFactory, label: str):
    """One machine-wide mutex for every HEAVY operation this module runs: the walk and
    each negative-path test spawn several minutes of real `uv`/`git`/`doit` subprocess
    work against a throwaway repo, sharing this machine's CPU, memory and
    `UV_PROJECT_ENVIRONMENT` with whatever else this run is doing. Under `-n 4` the walk
    and all three negative-path tests were free to run fully concurrently -- and that
    shared load, not a defect in any one test, is what turned three of them red while
    every one was correct alone (DIGEST-WAVE3-2026-09-21.md queue item 4). Serializing
    the walk against ITSELF (the original single-purpose lock this generalises) was not
    enough, because nothing serialized it against its siblings.

    Same technique as the original walk-only lock: an exclusive-create lock file in this
    RUN's shared folder, held for the CALLER's whole body, not just a result-file check.
    """
    lock = _run_dir(tmp_path_factory) / "connection-loop.lock"
    deadline = time.monotonic() + 2 * STOP_TIMEOUT_S
    while time.monotonic() < deadline:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            time.sleep(2)
            continue
        os.write(fd, label.encode("utf-8"))
        os.close(fd)
        try:
            yield
        finally:
            lock.unlink(missing_ok=True)
        return
    raise TimeoutError(f"{label} could not acquire the connection-loop module lock")


# One walk per test RUN, shared across xdist workers: the RESULT is shared through a file (read
# lock-free once present); COMPUTING it holds the module-wide `_exclusive` mutex, so it never runs
# alongside a negative-path test either (not just alongside another worker's own walk attempt).
def _shared_walk(tmp_path_factory: pytest.TempPathFactory) -> Walk:
    result = _run_dir(tmp_path_factory) / "connection-loop-walk.json"
    if result.is_file():
        return Walk.from_json(result.read_text(encoding="utf-8"))
    with _exclusive(tmp_path_factory, "walk"):
        if result.is_file():          # someone else finished while we waited for the lock
            return Walk.from_json(result.read_text(encoding="utf-8"))
        walk = walk_the_loop(tmp_path_factory)
        partial = result.with_name(result.name + f".{os.getpid()}.tmp")
        partial.write_text(walk.to_json(), encoding="utf-8")
        os.replace(partial, result)   # readers see the whole file or none of it
        return walk


@pytest.fixture(scope="module")
def walk(tmp_path_factory: pytest.TempPathFactory) -> Walk:
    return _shared_walk(tmp_path_factory)


def _stops(w: Walk) -> str:
    return "; ".join(f"{s.moment}/{s.organ} [{s.receipt}] {s.detail}" for s in w.stops) or "none"


# --- Done-contract 1 + 2: the loop, the receipts, the digest ---------------------------------------------------------

@pytest.mark.xfail(strict=True, reason="W3-F walk (2026-09-21): stops at merge/gates (RED) and at batch-close (the "
                                       "digest never names the task) -- wave 4's queue. Delete this marker and "
                                       "EXPECTED_STOPS when the loop is connected.")
def test_one_toy_task_leaves_a_receipt_at_every_moment_in_order(walk):
    assert not walk.stops, f"the loop stopped: {_stops(walk)}"
    declared = ["spine", "pre-launch", "lane-start", "lane-end", "merge", "teardown", "batch-close"]
    assert [s.moment for s in walk.steps] == declared
    stamps = [max(o.mtime_ns for o in s.organs) for s in walk.steps]
    assert stamps == sorted(stamps), "the moments' receipts are not in loop order"
    assert all(o.fired for s in walk.steps for o in s.organs)
    assert walk.slug in walk.digest or SUBJECT in walk.digest, "the digest does not name the task"


def test_the_loop_stops_where_the_walk_recorded(walk):
    """Everything before the first stop fired, in order, each exit 0; the stops are exactly the recorded queue."""
    assert tuple((s.moment, s.organ) for s in walk.stops) == EXPECTED_STOPS, _stops(walk)
    first = walk.stops[0].moment
    before = walk.steps[:[s.moment for s in walk.steps].index(first)]
    assert [s.moment for s in before] == ["spine", "pre-launch", "lane-start", "lane-end"]
    assert all(o.fired for s in before for o in s.organs)
    stamps = [max(o.mtime_ns for o in s.organs) for s in before]
    assert stamps == sorted(stamps)
    merge = next(s for s in walk.steps if s.moment == "merge")
    assert [o.organ for o in merge.organs if o.fired] == ["merge_receipt.open", "merge_receipt.models", "go_reader", "review_packet"]


def test_the_toy_task_was_launched_once_by_the_launcher_and_nothing_real_spawned(walk):
    assert walk.integrator["launch_exit"] == 0 and walk.integrator["spawns"] == 1


# --- Done-contract 2: toy-copy artifacts are distinguished from the loop's own stops ------------

def _finding(check_name: str, status: str = "fail", evidence: str = "...") -> dict:
    return {"check_name": check_name, "status": status, "evidence": evidence}


def test_fixture_artifacts_in_finds_a_known_toy_copy_cause_in_a_red_gate():
    verdict = {"gates": [
        {"name": "audit-health", "exit_code": 1, "findings": [_finding("canonical_freshness")]},
        {"name": "ship-gate", "exit_code": 1, "findings": [_finding("organ_truth", "warn",
                                                                    "36 organs ...")]},
    ]}
    assert _fixture_artifacts_in(verdict) == ("audit-health:canonical_freshness",)


def test_fixture_artifacts_in_reads_the_structured_list_not_a_tail_substring():
    """Done-contract 3: a marker present in `findings` but ABSENT from `output_tail` (as it would
    be if the finding printed before a truncated tail's window, WAVE4-FINAL finding 4) must still
    be found -- proves the reader no longer greps text."""
    verdict = {"gates": [{"name": "ship-gate", "exit_code": 1,
                          "output_tail": "nothing resembling that check name is in this tail",
                          "findings": [_finding("funnel_lifecycle", "warn", "toy seed commit")]}]}
    assert _fixture_artifacts_in(verdict) == ("ship-gate:funnel_lifecycle",)


def test_fixture_artifacts_in_never_lists_organ_truth():
    """`organ_truth` must never enter the catalogue -- Done-contract 2's "the loop's real stops
    stay visible" is exactly the invariant this asserts, independent of any one probe's output."""
    assert all("organ_truth" not in markers for markers in _FIXTURE_ARTIFACT_MARKERS.values())


def test_fixture_artifacts_in_ignores_a_green_gate():
    verdict = {"gates": [{"name": "audit-health", "exit_code": 0,
                          "findings": [_finding("canonical_freshness")]}]}
    assert _fixture_artifacts_in(verdict) == ()


def test_fixture_artifacts_in_is_empty_with_no_verdict():
    assert _fixture_artifacts_in(None) == ()


def test_fixture_artifacts_in_is_empty_with_no_findings_key():
    """A gate row from before FR4 (no `findings` key at all) must degrade to no match, not raise."""
    verdict = {"gates": [{"name": "audit-health", "exit_code": 1,
                          "output_tail": "... canonical_freshness: FAIL ..."}]}
    assert _fixture_artifacts_in(verdict) == ()


# --- FR4: gates.py's structured per-organ findings, read straight (not through the walk) --------

def test_gates_findings_in_parses_the_locked_finding_line_shape():
    """`gates._findings_in` reads the exact `[MARKER] check_name: evidence` line `audit.py`
    already prints per Finding -- `pass`/`n/a`/`unavailable` lines are not findings (only fail and
    warn are "every hard-fail and warning name", FR4's own words)."""
    import gates  # noqa: PLC0415

    text = ("operational:\n  [OK] repos registered  (['x'])\n"
            "self-audit (.dev-knowledge) - 40/44 pass:\n"
            "  [OK] doc_structure: fine\n"
            "  [!!] organ_truth: 3 organ(s) have no caller anywhere: a, b, c\n"
            "  [~~] canonical_freshness: 2 file(s) stale: x.md, y.md\n"
            "  [??] handoff_probes: n/a\n"
            "ship-gate: RED -- not shipped-ready (1 hard-fail organ(s))\n")
    assert gates._findings_in(text) == [
        {"check_name": "organ_truth", "status": "fail",
         "evidence": "3 organ(s) have no caller anywhere: a, b, c"},
        {"check_name": "canonical_freshness", "status": "warn",
         "evidence": "2 file(s) stale: x.md, y.md"},
    ]


def test_gates_findings_in_is_empty_for_output_with_no_finding_lines():
    import gates  # noqa: PLC0415

    assert gates._findings_in("ruff check: all good\n") == []
    assert gates._findings_in("") == []


def test_gates_run_gates_attaches_findings_regardless_of_tail_truncation(tmp_path):
    """The regression this lane exists to fix: a Finding line that prints BEFORE a large amount of
    trailing output falls out of the truncated `output_tail` but must still land in `findings` --
    proves gates.py itself parses FULL text, not the tail it also keeps for humans."""
    import gates  # noqa: PLC0415

    filler = "x" * (gates._TAIL_CHARS + 500)
    src = ("import sys; "
           "sys.stdout.write('  [!!] organ_truth: 36 organ(s) carry a fate\\n'); "
           f"sys.stdout.write({filler!r} + '\\n'); "
           "sys.exit(1)")
    gate = gates.Gate(name="fake-ship-gate", argv=(sys.executable, "-c", src))
    verdict = gates.run_gates((gate,), lane="toy", cwd=tmp_path)
    row = verdict["gates"][0]
    assert "organ_truth" not in row["output_tail"], \
        "the tail must have pushed the finding line out for this test to be meaningful"
    assert row["findings"] == [{"check_name": "organ_truth", "status": "fail",
                                "evidence": "36 organ(s) carry a fate"}]


def test_gates_findings_in_preserves_every_dated_organ_the_census_names():
    """Done-contract 2: the census (`check_organ_truth.check_organ_truth`) names EVERY dated
    organ in ONE Finding's evidence, never a rolled-up preview -- its own docstring: "These four
    ALL-NAME, never `_rolled()`'s truncated preview". `gates.py` parsing FULL text (not a tail)
    must therefore carry all of them into the JSON, whatever the count. Built from the exact
    format `check_organ_truth._fail`/`_warn` produce (`{N} organ(s) carry a \\`manual_until\\`
    fate not yet due: {joined labels}`), pinned at the WAVE4-FINAL digest's own count (36) so a
    future truncation regression is caught by an exact count, not by eyeballing a long string."""
    import gates  # noqa: PLC0415

    organs = [f"scripts/organ_{i:02d}.py (manual_until 2026-10-05)" for i in range(36)]
    evidence = f"36 organ(s) carry a `manual_until` fate not yet due: {', '.join(organs)}"
    text = f"  [~~] organ_truth: {evidence}\nship-gate: RED -- not shipped-ready (...)\n"
    findings = gates._findings_in(text)
    assert len(findings) == 1
    assert findings[0]["check_name"] == "organ_truth" and findings[0]["status"] == "warn"
    for organ in organs:
        assert organ in findings[0]["evidence"], f"{organ} dropped from the JSON"


# --- Done-contract 5: transport isolation proven before and after every run --------------------

def test_assert_transport_untouched_passes_when_fingerprints_match(monkeypatch):
    monkeypatch.setattr(sys.modules[__name__], "_transport_fingerprint", lambda: {"a": (1, 1)})
    _assert_transport_untouched({"a": (1, 1)})   # no raise


def test_assert_transport_untouched_fails_when_fingerprints_differ(monkeypatch):
    monkeypatch.setattr(sys.modules[__name__], "_transport_fingerprint", lambda: {"a": (2, 2)})
    with pytest.raises(AssertionError):
        _assert_transport_untouched({"a": (1, 1)})


def test_assert_transport_untouched_is_none_safe():
    _assert_transport_untouched(None)   # an unresolvable transport is not observable -- never a false alarm


def test_the_merge_gates_stop_separates_toy_copy_artifacts_from_the_real_cause(walk):
    """Integration leg: canonical_freshness's A2 check compares every canonical file's
    `last_reviewed` stamp against its git commit date, and the toy repo's one "seed" commit makes
    every file's commit date read "today" -- so if the walk stopped at merge/gates at all, this
    toy-copy artifact is virtually certain to be among the causes, and must be labelled apart from
    whatever real cause (organ_truth) is also in that same red."""
    gates_stop = next((s for s in walk.stops if s.moment == "merge" and s.organ == "gates"), None)
    if gates_stop is None:
        pytest.skip("the loop no longer stops at merge/gates")
    assert not any(a.split(":", 1)[-1] == "organ_truth" for a in gates_stop.fixture_artifacts)
    assert gates_stop.fixture_artifacts, "expected at least one known toy-copy artifact to be labelled"
    assert "FIXTURE-ARTIFACT" in gates_stop.detail


# --- Done-contract 4: operator touches --------------------------------------------------------------------------------

def test_a_human_writes_at_most_three_files_task_go_and_nothing_else(walk):
    kinds = [w["kind"] for w in walk.human_writes]
    assert kinds == ["task", "go"], f"a human would have had to write: {walk.human_writes}"
    assert len(kinds) <= 3


def test_the_operators_live_transport_was_not_touched(walk):
    assert walk.integrator["registry_redirect"] in ("verified", "not-applicable"), walk.integrator["registry_redirect"]
    assert walk.live_transport_touched is not True, "the walk wrote toy files onto the operator's live transport"


# --- Done-contract 3: negative paths, each its own test ----------------------------------------------------------------

def _negative_contract(world: World) -> Path:
    path = world.transport / "LANE-20260921-wire-toy-negative.md"
    path.write_text((_FIXTURES / "negative-contract.md").read_text(encoding="utf-8"), encoding="utf-8")
    return path


# Each negative-path test holds the SAME module-wide `_exclusive` mutex the walk holds while
# computing (see `_exclusive`'s docstring): it is a heavy operation too, and nothing about being a
# short test exempts it from the shared load that turned three of this module's tests red under
# `-n 4` while every one was correct alone. Each also proves transport isolation before and after
# itself (Done-contract 5), not just the walk -- `_assert_transport_untouched`.

def test_an_occupied_slug_stops_at_pre_launch(tmp_path_factory):
    with _exclusive(tmp_path_factory, "negative-occupied"):
        live_before = _transport_fingerprint()
        world = _fresh_world(tmp_path_factory, "negative_occupied", full=False)
        world.git("worktree", "add", "-q", "-b", f"worktree-{NEGATIVE_SLUG}", f".claude/worktrees/{NEGATIVE_SLUG}")
        provider = FakeProvider()
        with pytest.MonkeyPatch.context() as mp:
            launched = world.launch(_negative_contract(world), provider, mp)
        assert launched.exit_code == 5, launched.output
        assert "occupied" in launched.output.lower() or "OCCUPIED" in launched.output
        assert provider.calls == [], "a refused launch must not reach the process boundary"
        receipts = world.repo / "logs" / "receipts"
        occupancy = _read_receipt(receipts / "MOMENT-PRE-LAUNCH-WORKTREE-OCCUPANCY.json")
        assert occupancy and occupancy["exit_code"] == 1
        assert not (receipts / "MOMENT-PRE-LAUNCH-NO-LIVE-INTEGRATOR.json").exists(), "later organs ran past the refusal"
        assert not list(receipts.glob("LAUNCH-LANE-*.json")), "a refused launch wrote a launch receipt"
        _assert_transport_untouched(live_before)


def test_a_missing_go_file_stops_at_merge(tmp_path_factory):
    with _exclusive(tmp_path_factory, "negative-no-go"):
        live_before = _transport_fingerprint()
        world = _fresh_world(tmp_path_factory, "negative_no_go", full=False)
        contract = _negative_contract(world)
        world.git("worktree", "add", "-q", "-b", f"worktree-{NEGATIVE_SLUG}", f".claude/worktrees/{NEGATIVE_SLUG}")
        worktree = world.repo / ".claude" / "worktrees" / NEGATIVE_SLUG
        sha = world.lane_commit(worktree)
        world.lane_transcript(worktree)
        handback = world.write_session(NEGATIVE_SLUG, sha)
        merge_sha, _ = world.integrate_merge(NEGATIVE_SLUG, contract, handback)
        assert merge_sha, "the handback verdict must pass so the refusal under test is the missing GO"
        assert not (world.transport / "to-cc" / f"GO-{BATCH}.md").exists(), "this test must not write a GO"
        step = world.moment("merge", **world.merge_env(NEGATIVE_SLUG, contract, handback, merge_sha))
        assert step.exit_code != 0
        fired = [o.organ for o in step.organs if o.fired]
        assert fired == ["merge_receipt.open", "merge_receipt.models"], f"models must pass and nothing after go_reader may run: {step}"
        assert step.stop and step.stop.organ == "go_reader"
        refusal = (world.repo / "logs" / "receipts" / "MOMENT-MERGE-GO-READER-OUTPUT.txt").read_text(encoding="utf-8")
        assert "REFUSED" in refusal and f"GO-{BATCH}.md" in refusal
        assert step.unreached == ["review_packet", "gates", "test_pairing"]
        _assert_transport_untouched(live_before)


def test_no_handback_line_means_lane_end_does_not_run(tmp_path_factory):
    with _exclusive(tmp_path_factory, "negative-no-handback"):
        live_before = _transport_fingerprint()
        world = _fresh_world(tmp_path_factory, "negative_no_handback", full=False)
        world.git("worktree", "add", "-q", "-b", f"worktree-{NEGATIVE_SLUG}", f".claude/worktrees/{NEGATIVE_SLUG}")
        worktree = world.repo / ".claude" / "worktrees" / NEGATIVE_SLUG
        world.lane_commit(worktree)
        world.write_session(NEGATIVE_SLUG, None)          # a session file, a finished-looking commit, NO closing line
        world.stop_hook(worktree)                          # the real Stop guard
        receipts = worktree / "logs" / "receipts"
        assert not (receipts / "MOMENT-LANE-END-HOOK.json").exists(), "the guard claimed a lane that has not finished"
        moment = world.moment("lane-end", cwd=worktree)    # and the moment itself refuses on its declared precondition
        assert moment.exit_code == 0
        assert [o.status for o in moment.organs] == ["SKIPPED-PRECONDITION"]
        assert sorted(p.name for p in receipts.glob("MOMENT-LANE-END-*.json")) == ["MOMENT-LANE-END-PRECONDITION.json"]
        assert not (world.transport / "to-browser" / f"LANE-END-{NEGATIVE_SLUG}.md").exists(), "a report was delivered"
        _assert_transport_untouched(live_before)
