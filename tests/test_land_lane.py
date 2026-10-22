"""RED-first witnesses for `scripts/land_lane.py`: the harness map's "land" transition as code.

ONE script runs the lane-integrate sequence for ONE lane with no model call. It CALLS
`merge_path.land()` (no second landing push) and writes receipts through `merge_receipt`.
No network: origin is a bare repo in `tmp_path`; CI's verdict, the suite read and `sleep` are injected.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from click.testing import CliRunner

import merge_path
import merge_receipt
import land_lane as ll

SLUG = "lane-a"
BATCH = "E1.0"          # well-formed and older than E2.0: subst_gate does not require a handback
INTEGRATION = "worktree-integrate-e1.0"


def _git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                          encoding="utf-8", check=True)
    return proc.stdout.strip()


def _config(clone: Path) -> None:
    _git(clone, "config", "user.name", "Test")
    _git(clone, "config", "user.email", "test@example.com")
    _git(clone, "config", "core.autocrlf", "false")


def _commit_file(clone: Path, name: str, text: str, message: str) -> str:
    path = clone / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    _git(clone, "add", name)
    _git(clone, "commit", "-m", message)
    return _git(clone, "rev-parse", "HEAD")


class Env:
    def __init__(self, root: Path):
        self.root = root
        self.origin = root / "origin.git"
        self.seed = root / "seed"
        self.lane = root / "lane"
        self.worktree = root / "worktree"
        self.carry = root / "carry.jsonl"
        root.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "--bare", "-b", "main", str(self.origin)], check=True,
                       capture_output=True)
        subprocess.run(["git", "clone", str(self.origin), str(self.seed)], check=True,
                       capture_output=True)
        _config(self.seed)
        _git(self.seed, "checkout", "-B", "main")
        (self.seed / "logs").mkdir()
        (self.seed / "README.md").write_text("readme\n", encoding="utf-8", newline="\n")
        (self.seed / "logs" / "MERGE-RECEIPTS.jsonl").write_text("", encoding="utf-8")
        (self.seed / "shared.txt").write_text("base\n", encoding="utf-8", newline="\n")
        _git(self.seed, "add", "-A")
        _git(self.seed, "commit", "-m", "seed")
        _git(self.seed, "push", "origin", "main")
        subprocess.run(["git", "clone", str(self.origin), str(self.lane)], check=True,
                       capture_output=True)
        _config(self.lane)
        self.make_lane("lane-a", "lane_a.txt")
        subprocess.run(["git", "clone", str(self.origin), str(self.worktree)], check=True,
                       capture_output=True)
        _config(self.worktree)
        _git(self.worktree, "checkout", "main")

    def make_lane(self, slug: str, filename: str, *, text: str = "lane\n") -> str:
        _git(self.lane, "fetch", "origin")
        _git(self.lane, "checkout", "-B", f"worktree-{slug}", "origin/main")
        _commit_file(self.lane, filename, text, f"lane {slug}")
        _git(self.lane, "push", "-f", "origin", f"worktree-{slug}")
        return _git(self.lane, "rev-parse", "HEAD")

    def make_conflicting_lane(self, slug: str) -> None:
        self.make_lane(slug, "shared.txt", text="lane side\n")
        self.advance_main(name="shared.txt", text="main side\n")

    def advance_main(self, name: str = "moved.txt", text: str = "moved\n") -> str:
        _git(self.seed, "pull", "--ff-only", "origin", "main")
        sha = _commit_file(self.seed, name, text, "main moves")
        _git(self.seed, "push", "origin", "main")
        return sha

    def origin_ref(self, ref: str) -> str:
        proc = subprocess.run(["git", "-C", str(self.origin), "rev-parse", "--verify", "-q", ref],
                              capture_output=True, text=True)
        return proc.stdout.strip()

    def refs(self) -> str:
        return _git(self.origin, "for-each-ref", "--format=%(refname) %(objectname)")

    def ledger_on_main(self) -> list[str]:
        out = _git(self.origin, "show", "main:logs/MERGE-RECEIPTS.jsonl")
        return [line for line in out.splitlines() if line.strip()]

    def status(self) -> str:
        return _git(self.worktree, "status", "--porcelain")

    def head(self) -> str:
        return _git(self.worktree, "rev-parse", "HEAD")


@pytest.fixture(autouse=True)
def _events(tmp_path, monkeypatch):
    monkeypatch.setenv(merge_path.EVENTS_PATH_ENV, str(tmp_path / "events" / "events.jsonl"))
    # Machine-independent git: a bare repo is usable and no autocrlf dirties the clones.
    for i, (k, v) in enumerate((("safe.bareRepository", "all"), ("core.autocrlf", "false"))):
        monkeypatch.setenv(f"GIT_CONFIG_KEY_{i}", k)
        monkeypatch.setenv(f"GIT_CONFIG_VALUE_{i}", v)
    monkeypatch.setenv("GIT_CONFIG_COUNT", "2")


@pytest.fixture
def env(tmp_path, monkeypatch):
    e = Env(tmp_path / "env")
    monkeypatch.chdir(e.worktree)
    return e


def pass_verdict(sha, **kwargs):
    return SimpleNamespace(state="PASS", missing_contexts=(), reason="", newly_failing=(),
                           new_tests=(), jobs=())


def stub_suite(root, *, slug, sha, required_contexts=None):
    """Record a landable suite read on the open receipt, as `record_actions_verdict` would."""
    receipt = merge_receipt.load_receipt(root, slug)
    receipt.steps.append(merge_receipt.StepTiming(
        step="suite", step_class=merge_receipt.CLASS_CEREMONY, seconds=0.0, ok=True, returncode=0,
        command="stub", started="", verdict_state="PASS"))
    merge_receipt.save_receipt(root, receipt)


def recording_git(root: Path, log: list, rewrite=None):
    run = merge_path._run_git(root)

    def git(args):
        args = list(args)
        if rewrite is not None:
            args = rewrite(args)
        log.append(args)
        return run(args)
    return git


def do_land(env: Env, **overrides):
    kwargs = dict(slug=SLUG, batch=BATCH, carry_file=env.carry, verdict_fn=pass_verdict,
                  record_suite_fn=stub_suite, sleep=lambda s: None, teardown_fn=lambda wt: None)
    kwargs.update(overrides)
    return ll.land_lane(env.worktree, **kwargs)


def model_cli_sandbox(tmp_path: Path, monkeypatch) -> Path:
    bin_dir = tmp_path / "model-bin"
    bin_dir.mkdir()
    marker = tmp_path / "model-called.txt"
    for name in ("claude", "codex", "copilot"):
        if sys.platform == "win32":
            (bin_dir / f"{name}.cmd").write_text(f'@echo {name}>>"{marker}"\r\n', encoding="utf-8")
        shim = bin_dir / name
        shim.write_text(f'#!/bin/sh\necho {name} >> "{marker}"\n', encoding="utf-8", newline="\n")
        shim.chmod(0o755)
    monkeypatch.setenv("PATH", str(bin_dir) + os.pathsep + os.environ.get("PATH", ""))
    return marker


# --- a ----------------------------------------------------------------------------------------

def test_clean_lane_lands_with_zero_model_calls(env, tmp_path, monkeypatch):
    marker = model_cli_sandbox(tmp_path, monkeypatch)
    old_main = env.origin_ref("main")
    log: list = []
    report = do_land(env, git=recording_git(env.worktree, log))

    assert not marker.exists() or marker.read_text(encoding="utf-8").strip() == ""
    assert report.ok, report.message
    assert report.exit_code == ll.EXIT_OK == 0
    assert report.state == "LANDED"
    assert [name for name, _ in report.steps] == list(ll.STEPS)
    assert report.sha
    assert env.origin_ref("main") == report.sha
    assert env.origin_ref(f"refs/heads/{INTEGRATION}") == report.sha
    parents = _git(env.worktree, "rev-list", "--parents", "-n1", report.sha).split()
    assert len(parents) == 3 and parents[0] == report.sha and parents[1] == old_main

    carried = [ln for ln in env.carry.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(carried) == 1
    assert json.loads(carried[0])["slug"] == SLUG
    assert env.ledger_on_main() == []
    assert env.status() == ""

    verbs = [a[0] for a in log if a and a[0] in ("fetch", "merge", "push")]
    assert verbs[0] == "fetch"
    assert verbs.index("merge") < verbs.index("push")
    assert verbs[-2:] == ["push", "push"]
    pushes = [a for a in log if a and a[0] == "push"]
    assert len(pushes) == 2
    assert pushes[0][-1] == f"{report.sha}:refs/heads/{INTEGRATION}"
    assert pushes[1][-1] == f"{report.sha}:refs/heads/main"


# --- b ----------------------------------------------------------------------------------------

def test_conflicting_lane_stops_with_file_list(env):
    env.make_conflicting_lane("lane-a")
    refs_before = env.refs()
    report = do_land(env)

    assert not report.ok
    assert report.state == "CONFLICT"
    assert report.exit_code == ll.EXIT_CONFLICT
    assert "shared.txt" in report.conflicts
    assert env.status() == ""
    assert env.head() == env.origin_ref("main")
    assert env.refs() == refs_before
    assert env.origin_ref(f"refs/heads/{INTEGRATION}") == ""


# --- c ----------------------------------------------------------------------------------------

def test_red_ci_stops_with_failing_check_names(env):
    old_main = env.origin_ref("main")
    name = "pytest (ubuntu-latest)"

    def red(sha, **kwargs):
        return SimpleNamespace(state="REGRESSED", missing_contexts=(), reason="a check regressed",
                               newly_failing=(name,), new_tests=(), jobs=())

    report = do_land(env, verdict_fn=red)

    assert not report.ok
    assert report.state == "RED"
    assert report.exit_code == ll.EXIT_RED
    assert name in report.failing
    assert name in report.message
    assert env.origin_ref("main") == old_main
    assert env.origin_ref(f"refs/heads/{INTEGRATION}")
    assert env.origin_ref(f"refs/heads/{INTEGRATION}") == report.sha


# --- d ----------------------------------------------------------------------------------------

def test_base_moved_before_push_stops(env):
    moved = {}

    def land_fn(*args, **kwargs):
        moved["sha"] = env.advance_main()
        return merge_path.land(*args, **kwargs)

    report = do_land(env, land_fn=land_fn)

    assert not report.ok
    assert report.state == "BASE-MOVED"
    assert report.exit_code == ll.EXIT_BASE_MOVED
    assert "BASE-MOVED" in report.message
    assert "before" in report.message.lower()
    assert env.origin_ref("main") == moved["sha"]
    assert env.origin_ref(f"refs/heads/{INTEGRATION}") == ""


def test_base_moved_after_push_stops(env):
    moved = {}

    def verdict(sha, **kwargs):
        moved["sha"] = env.advance_main()
        return pass_verdict(sha)

    report = do_land(env, verdict_fn=verdict)

    assert not report.ok
    assert report.state == "BASE-MOVED"
    assert report.exit_code == ll.EXIT_BASE_MOVED
    assert "BASE-MOVED" in report.message
    assert "already holds" in report.message
    assert env.origin_ref("main") == moved["sha"] != report.sha
    assert env.origin_ref(f"refs/heads/{INTEGRATION}") == report.sha


# --- e ----------------------------------------------------------------------------------------

def test_poll_window_defaults_above_25_minutes_and_is_a_parameter(env, tmp_path):
    assert ll.DEFAULT_TIMEOUT_S > 25 * 60
    assert ll.DEFAULT_INTERVAL_S == 20

    seen: list = []

    def verdict(sha, **kwargs):
        seen.append(kwargs["timeout_s"])
        return pass_verdict(sha)

    assert do_land(env, verdict_fn=verdict, timeout_s=77).ok
    assert seen == [77]

    second = Env(tmp_path / "second")
    seen.clear()
    assert do_land(second, verdict_fn=verdict).ok
    assert seen == [ll.DEFAULT_TIMEOUT_S]

    option = next(p for p in ll.cli.params if p.name == "timeout_s")
    assert option.default == ll.DEFAULT_TIMEOUT_S


# --- f ----------------------------------------------------------------------------------------

def test_main_only_receives_the_sha_ci_judged(env):
    _git(env.seed, "pull", "--ff-only", "origin", "main")
    rogue = _commit_file(env.seed, "rogue.txt", "rogue\n", "unjudged commit")
    _git(env.seed, "push", "origin", f"{rogue}:refs/heads/rogue")
    _git(env.worktree, "fetch", "origin")

    def rewrite(args):
        if args and args[0] == "push" and args[-1].endswith(":refs/heads/main"):
            return [*args[:-1], f"{rogue}:refs/heads/main"]
        return args

    report = do_land(env, git=recording_git(env.worktree, [], rewrite=rewrite))

    assert not report.ok
    assert report.exit_code != 0
    assert report.state == "REFUSED"
    assert "unjudged" in report.message

    lane_sha = _git(env.worktree, "rev-parse", "origin/worktree-lane-a")
    assert merge_path.land(env.worktree, slug=SLUG, batch=BATCH, sha=lane_sha,
                           base=env.origin_ref("main") or rogue, verdict_fn=pass_verdict,
                           record_suite_fn=stub_suite,
                           record_push_fn=lambda *a, **k: None).state == "NOT-A-MERGE-ON-BASE"


# --- g ----------------------------------------------------------------------------------------

def _tree_files(root: Path) -> list[str]:
    return sorted(str(p.relative_to(root)) for p in root.rglob("*")
                  if ".git" not in p.relative_to(root).parts)


def test_dry_run_prints_every_step_and_touches_nothing(env):
    lines = ll.plan(SLUG, BATCH)
    assert len(lines) == len(ll.STEPS)
    for line, step in zip(lines, ll.STEPS):
        assert step in line

    refs_before = env.refs()
    files_before = _tree_files(env.worktree)
    result = CliRunner().invoke(ll.cli, ["--worktree", str(env.worktree), "--slug", SLUG,
                                         "--batch", BATCH, "--dry-run"])

    assert result.exit_code == 0, result.output
    for line in lines:
        assert line in result.output
    assert env.refs() == refs_before
    assert _tree_files(env.worktree) == files_before
    assert env.status() == ""


# --- h ----------------------------------------------------------------------------------------

def test_real_landing_needs_the_integrator_flag(env):
    _git(env.worktree, "remote", "set-url", "origin", "https://github.com/example/example.git")
    result = CliRunner().invoke(ll.cli, ["--worktree", str(env.worktree), "--slug", SLUG,
                                         "--batch", BATCH])

    assert result.exit_code == ll.EXIT_REFUSED != 0
    assert "--i-am-the-integrator" in result.output

    helped = CliRunner().invoke(ll.cli, ["--help"])
    assert helped.exit_code == 0
    assert "--i-am-the-integrator" in helped.output


# --- i ----------------------------------------------------------------------------------------

def test_carry_file_round_trips_between_two_landings(env):
    first = do_land(env)
    assert first.ok, first.message
    first_line = env.carry.read_text(encoding="utf-8").splitlines()[0]
    assert env.ledger_on_main() == []

    env.make_lane("lane-b", "lane_b.txt")
    second = do_land(env, slug="lane-b", lane_ref="origin/worktree-lane-b")
    assert second.ok, second.message

    # The first landing's receipt rode the second merge commit; the second's waits in the carry.
    on_main = env.ledger_on_main()
    assert on_main == [first_line]
    assert on_main[0].encode("utf-8") == first_line.encode("utf-8")
    carried = [ln for ln in env.carry.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(carried) == 1 and carried[0] != first_line
    assert json.loads(carried[0])["slug"] == "lane-b"
    assert len(on_main) + len(carried) == 2
    assert merge_receipt.ledger_path(env.worktree).read_text(encoding="utf-8").strip() == first_line


# --- regenerate ---------------------------------------------------------------------------------

def test_regenerated_files_are_folded_into_the_two_parent_merge(env):
    old_main = env.origin_ref("main")
    cmd = [sys.executable, "-c", "open('generated.txt', 'w').write('regenerated')"]
    report = do_land(env, regen_cmds=[cmd])

    assert report.ok, report.message
    parents = _git(env.worktree, "rev-list", "--parents", "-n1", report.sha).split()
    assert len(parents) == 3 and parents[1] == old_main
    assert _git(env.origin, "show", "main:generated.txt") == "regenerated"
