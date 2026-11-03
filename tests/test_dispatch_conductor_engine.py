"""RED-first acceptance tests for dispatching conductor-engine lane contracts."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from click.testing import CliRunner

import dispatch as d
import gen_process_diagrams as gpd
import subst_gate
import worktree_occupancy as wo

REPO = Path(__file__).resolve().parents[1]
FIXTURES = REPO / "tests" / "fixtures" / "round_loop_dispatch"
CONDUCTOR_CONTRACT = FIXTURES / "LANE-round-loop-dispatch-fixture.md"
MODEL_CONTRACT = FIXTURES / "LANE-model-engine-fixture.md"
SLUG = "round-loop-dispatch-fixture"
BATCH = "E3.0"


@pytest.fixture(autouse=True)
def isolated_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(tmp_path / "receipts"))
    monkeypatch.delenv("HARNESS_BASE", raising=False)
    monkeypatch.delenv("HARNESS_BATCH", raising=False)
    monkeypatch.delenv("HARNESS_REPAIR", raising=False)


def _require(*names: str) -> None:
    missing = [name for name in names if not hasattr(d, name)]
    assert not missing, f"missing conductor dispatch behavior: {', '.join(missing)}"


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()


def _new_repo(path: Path, monkeypatch) -> tuple[Path, Path, str]:
    """Create a real checkout named `.dev-knowledge` with its local origin/main ref and seed file."""
    root = path
    root.mkdir(parents=True)
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.name", "dispatch-test")
    _git(root, "config", "user.email", "dispatch-test@example.invalid")
    (root / ".gitignore").write_text(
        "ecosystem/x/state.yaml\nlogs/receipts/\n",
        encoding="utf-8",
    )
    (root / "tracked.txt").write_text("base\n", encoding="utf-8")
    _git(root, "add", ".gitignore", "tracked.txt")
    _git(root, "commit", "-q", "-m", "fixture base")
    base = _git(root, "rev-parse", "HEAD")
    _git(root, "update-ref", "refs/remotes/origin/main", base)

    state = root / "ecosystem" / "x" / "state.yaml"
    state.parent.mkdir(parents=True)
    state.write_text("fixture: seeded\n", encoding="utf-8")
    receipts = root / "logs" / "receipts"
    receipts.mkdir(parents=True)
    assert _git(root, "check-ignore", "ecosystem/x/state.yaml", "logs/receipts/probe.json")
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(receipts))
    return root, receipts, base


def _commit(repo: Path, filename: str, content: str) -> str:
    (repo / filename).write_text(content, encoding="utf-8")
    _git(repo, "add", filename)
    _git(repo, "-c", "user.name=dispatch-test", "-c", "user.email=dispatch-test@example.invalid",
         "commit", "-q", "-m", filename)
    return _git(repo, "rev-parse", "HEAD")


def _tree(repo: Path, slug: str = SLUG) -> Path:
    return repo / ".claude" / "worktrees" / slug


def _receipt_path(receipts: Path, slug: str = SLUG) -> Path:
    return receipts / f"LAUNCH-{slug.upper()}.json"


def _pid_path(receipts: Path, slug: str = SLUG) -> Path:
    return receipts / f"LAUNCH-PID-{slug.upper()}.json"


def _worktree_receipt(repo: Path, slug: str = SLUG) -> Path:
    return _tree(repo, slug) / "logs" / "receipts" / f"LAUNCH-{slug.upper()}.json"


def _contract_text(
    slug: str,
    *,
    head: str = "claude",
    engine: str | None = None,
    phases: bool = True,
    row: bool = True,
    model: str | None = None,
) -> str:
    model = model or {
        "claude": "claude-sonnet-5-5",
        "codex": "gpt-5.3-codex",
        "copilot": "gpt-5.6-luna",
    }[head]
    if head == "claude":
        dispatch = (
            f"claude --bg -n {slug} --model {model} --effort high "
            f"--permission-mode bypassPermissions --worktree {slug} "
            f'"Read and execute the frozen contract at LANE-{slug}.md"'
        )
    elif head == "codex":
        dispatch = f"codex exec -m {model} --worktree {slug}"
    else:
        dispatch = (
            f"copilot --model {model} --effort high -n {slug} --worktree {slug}"
        )
    lines = [
        f"# LANE {slug}",
        "",
        "| Model | Mode | Effort |",
        "|---|---|---|",
        f"| {model} | execute | high |",
        "",
    ]
    if row:
        lines.extend(["- **Row:** [#4243]", ""])
    lines.extend(["## Dispatch", ""])
    if engine is not None:
        lines.extend([f"**Engine:** {engine}", ""])
    lines.extend(["```", dispatch, "```", ""])
    if phases:
        lines.extend([
            "## Phases",
            "",
            "```yaml",
            "phases:",
            "  - id: implement",
            "    name: implement",
            "    row_phase: build",
            "    role: implement",
            "    cli: uv",
            "    model: null",
            "    payload_model: PhasePayload",
            "    gate: payload",
            "    timeout_s: 120",
            "    budget_usd: 0",
            "    max_rounds: 1",
            "    inputs: []",
            "    command: [echo, fixture]",
            "```",
            "",
        ])
    lines.extend([f"slug `{slug}` -> branch `worktree-{slug}`", ""])
    return "\n".join(lines)


def _write_contract(
    directory: Path,
    slug: str,
    *,
    head: str = "claude",
    engine: str | None = None,
    phases: bool = True,
    row: bool = True,
    model: str | None = None,
) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"LANE-{slug}.md"
    path.write_text(
        _contract_text(slug, head=head, engine=engine, phases=phases, row=row, model=model),
        encoding="utf-8",
    )
    return path


def _request(contract: Path = CONDUCTOR_CONTRACT, *, batch: str = BATCH):
    return d.request_from_contract(contract, batch=batch)


def _write_receipt(path: Path, body: dict) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(body, separators=(",", ":")) + "\n").encode("utf-8")
    path.write_bytes(data)
    return data


def _prior_receipt(contract: Path, tree: Path, base: str, pid: int = 6101) -> dict:
    return {
        "schema": 1,
        "organ": "launch",
        "launched_at": "2026-01-01T00:00:00+00:00",
        "exit_code": 0,
        "job_id": f"conductor-{pid}",
        "slug": SLUG,
        "provider": "anthropic",
        "batch": BATCH,
        "contract": str(contract.resolve()),
        "engine": "conductor",
        "base": base,
        "pid": pid,
        "worktree": str(tree),
        "argv": [],
    }


class FakeSpawn:
    def __init__(self, *pids: int):
        self.pids = list(pids)
        self.calls: list[dict] = []

    def __call__(self, argv, env, cwd, log_path=None):
        self.calls.append({
            "argv": list(argv),
            "env": dict(env),
            "cwd": Path(cwd),
            "log_path": Path(log_path) if log_path is not None else None,
        })
        pid = self.pids.pop(0) if self.pids else 7001
        return d.Spawned(returncode=0, stdout="", pid=pid)


class FakeClock:
    def __init__(self):
        self.elapsed = 0.0

    def age_seconds(self, _stamp):
        return self.elapsed

    def advance(self, seconds: float) -> None:
        self.elapsed += seconds


def _launch(
    request,
    root: Path,
    spawn,
    *,
    prelaunch=None,
    agents=None,
):
    return d.launch_lane(
        request,
        prelaunch=prelaunch or (lambda _request, repair=False: d.PreLaunch(True)),
        spawn=spawn,
        agents=agents or (lambda: []),
        cwd=root,
        environ={"HARNESS_BATCH": request.batch},
        sleep=lambda _seconds: None,
    )


def test_a_conductor_request_has_the_literal_conductor_argv_and_resolves_base_and_row(
    tmp_path, monkeypatch
):
    _require("parse_engine")
    request = _request()
    expected = [
        "uv", "run", "--locked", "python", "scripts/conductor.py", "lane", "--run",
        "--contract", str(CONDUCTOR_CONTRACT.resolve()), "--lane", SLUG,
        "--base", "origin/main", "--receipts", str(d.receipts_dir().resolve()),
        "--row", "4243",
    ]

    assert request.engine == "conductor"
    assert request.base == "origin/main"
    assert request.row == "4243"
    assert request.argv == expected
    assert not {"--bg", "-p", "--worktree"} & set(request.argv)
    assert "Read and execute" not in "\0".join(request.argv)

    monkeypatch.setenv("HARNESS_BASE", "refs/heads/base-override")
    override = _request()
    assert override.base == "refs/heads/base-override"
    assert override.argv[override.argv.index("--base") + 1] == "refs/heads/base-override"

    no_row = _write_contract(tmp_path, "conductor-without-row", engine="conductor", row=False)
    rowless = _request(no_row)
    assert rowless.row == ""
    assert "--row" not in rowless.argv


def test_b_parse_engine_and_model_engine_argv_remain_unchanged(tmp_path):
    _require("parse_engine")

    assert d.parse_engine(MODEL_CONTRACT.read_text(encoding="utf-8")) == "model"
    assert d.parse_engine("## Dispatch\n**Engine:** conductor\n") == "conductor"
    assert d.parse_engine("## Dispatch\n**Engine:** `conductor`\n") == "conductor"
    with pytest.raises(d.DispatchRefused) as bogus:
        d.parse_engine("## Dispatch\n**Engine:** bogus\n")
    assert "bogus" in str(bogus.value)
    with pytest.raises(d.DispatchRefused) as duplicate:
        d.parse_engine("## Dispatch\n**Engine:** conductor\n**Engine:** model\n")
    assert "conductor" in str(duplicate.value)

    default_model = d.LaunchRequest(
        slug="model-defaults",
        provider="anthropic",
        model="claude-sonnet-5-5",
        effort="high",
        permission_mode="bypassPermissions",
        contract=MODEL_CONTRACT,
    )
    assert default_model.engine == "model"
    assert default_model.base == "" and default_model.row == ""

    claude = d.request_from_contract(MODEL_CONTRACT, batch=BATCH)
    assert claude.engine == "model"
    assert claude.argv == [
        "claude", "--bg", "-n", "model-engine-fixture", "--model", "claude-sonnet-5-5",
        "--effort", "high", "--permission-mode", "bypassPermissions", "--worktree",
        "model-engine-fixture", "--disallowedTools=AskUserQuestion,advisor",
        f"Read and execute the frozen contract at {MODEL_CONTRACT.resolve()}",
    ]

    codex_path = _write_contract(tmp_path, "model-codex", head="codex")
    codex = d.request_from_contract(codex_path, batch=BATCH)
    assert codex.engine == "model"
    assert codex.argv == [
        "codex", "exec", "--json", "--skip-git-repo-check", "--worktree", "-m",
        "gpt-5.3-codex", "-c", "model_reasoning_effort=high", "-s", "workspace-write",
        f"Read and execute the frozen contract at {codex_path.resolve()}",
    ]

    copilot_path = _write_contract(tmp_path, "model-copilot", head="copilot")
    copilot = d.request_from_contract(copilot_path, batch=BATCH)
    assert copilot.engine == "model"
    assert copilot.argv == [
        "copilot", "-p", f"Read and execute the frozen contract at {copilot_path.resolve()}",
        "--model", "gpt-5.6-luna", "--reasoning-effort", "high", "--allow-all-tools",
        "--deny-tool", "shell", "--disable-builtin-mcps", "-n", "model-copilot",
    ]


@pytest.mark.parametrize(
    ("case", "cause"),
    [
        ("no-phases", "Phases"),
        ("codex-head", "codex"),
        ("explicit-provider", "copilot"),
    ],
)
def test_c_conductor_contract_refusals_name_the_cause_and_create_nothing(
    case, cause, tmp_path, monkeypatch
):
    _require("parse_engine")
    root, receipts, _base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    if case == "no-phases":
        contract = _write_contract(tmp_path, "no-phases", engine="conductor", phases=False)
        provider = ""
    elif case == "codex-head":
        contract = _write_contract(tmp_path, "codex-conductor", head="codex", engine="conductor")
        provider = ""
    else:
        contract = CONDUCTOR_CONTRACT
        provider = "copilot"

    with pytest.raises(d.DispatchRefused) as refused:
        d.request_from_contract(contract, provider=provider, batch=BATCH)

    assert cause.lower() in str(refused.value).lower()
    assert not _tree(root).exists()
    assert _git(root, "branch", "--list", f"worktree-{SLUG}") == ""
    assert list(receipts.iterdir()) == []


def test_c_process_binding_anchors_rebind_without_missing_or_duplicate_dispatch_sites(tmp_path):
    _require("parse_engine")
    binding_path = Path(gpd.REPO) / "ecosystem" / "process-binding.yaml"
    copied = tmp_path / "process-binding.yaml"
    shutil.copyfile(binding_path, copied)
    gpd.rebind(copied, gpd.REPO)
    binding = yaml.safe_load(copied.read_text(encoding="utf-8"))
    assert gpd.anchor_problems(binding, gpd.REPO) == []
    for anchor in (
        "def launch_lane(",
        "outcome = prelaunch(request)",
        'raise LaunchRefused(f"pre-launch refused',
        "_identify(request, started, self_identified, agents, sleep, began)",
        'if result.job_id == "unresolved":',
        "def run_prelaunch",
    ):
        assert len(gpd.find_anchor("scripts/dispatch.py", anchor, gpd.REPO)) == 1


def test_d_conductor_launch_seeds_worktree_and_writes_valid_atomic_receipts(
    tmp_path, monkeypatch
):
    _require("parse_engine", "_write_json_atomic")
    root, receipts, base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    request = _request()
    tree = _tree(root)
    prelaunch_calls = []
    spawn = FakeSpawn(7201)

    def prelaunch(launch_request, repair=False):
        prelaunch_calls.append((launch_request, repair, tree.exists()))
        return d.PreLaunch(True)

    result = _launch(request, root, spawn, prelaunch=prelaunch, agents=lambda: [])
    (argv, env, cwd, log_path), = [
        (call["argv"], call["env"], call["cwd"], call["log_path"]) for call in spawn.calls
    ]
    assert prelaunch_calls == [(request, False, False)]
    assert tree.is_dir()
    assert _git(tree, "rev-parse", "--show-toplevel") == str(tree)
    assert _git(tree, "rev-parse", "--abbrev-ref", "HEAD") == f"worktree-{SLUG}"
    assert _git(tree, "rev-parse", "HEAD") == base
    assert (tree / "ecosystem" / "x" / "state.yaml").read_text(encoding="utf-8") == "fixture: seeded\n"
    assert argv[argv.index("--base") + 1] == base
    assert cwd == tree and log_path is not None
    assert env["HARNESS_BATCH"] == BATCH
    assert result.job_id == "conductor-7201"
    assert result.pid == 7201 and result.model_reported == "not attestable"
    assert result.worktree == str(tree)

    primary = json.loads(_receipt_path(receipts).read_text(encoding="utf-8"))
    worktree_copy = json.loads(_worktree_receipt(root).read_text(encoding="utf-8"))
    assert primary == worktree_copy
    assert primary["organ"] == "launch" and primary["batch"] == BATCH
    assert primary["engine"] == "conductor" and primary["base"] == base
    assert primary["job_id"] == "conductor-7201" and primary["pid"] == 7201
    assert primary["worktree"] == str(tree) and primary["argv"] == argv
    assert primary["model_reported"] == "not attestable"
    assert primary["caller"]
    assert subst_gate.launch_receipt_problems(tree, SLUG, BATCH) == []
    assert subst_gate.launch_receipt_problems(tree, SLUG, BATCH, receipts_dir=receipts) == []
    assert not _pid_path(receipts).exists()

    model_root, model_receipts, _model_base = _new_repo(tmp_path / "model-repo", monkeypatch)
    model_request = d.request_from_contract(MODEL_CONTRACT, batch=BATCH)
    model_spawn = FakeSpawn(7202)
    _launch(model_request, model_root, model_spawn, agents=lambda: [])
    model_body = json.loads(
        _receipt_path(model_receipts, "model-engine-fixture").read_text(encoding="utf-8")
    )
    assert set(primary) >= set(model_body)
    assert set(primary) - set(model_body) == {"engine", "base"}


def test_e_prelaunch_refusal_happens_before_worktree_or_receipt_creation(
    tmp_path, monkeypatch
):
    _require("parse_engine")
    root, receipts, _base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    tree = _tree(root)
    spawn = FakeSpawn()
    seen = []

    def refuse(_request, repair=False):
        seen.append((repair, tree.exists()))
        return d.PreLaunch(False, "OCCUPIED")

    with pytest.raises(d.LaunchRefused, match="OCCUPIED"):
        _launch(_request(), root, spawn, prelaunch=refuse, agents=lambda: [])

    assert seen == [(False, False)]
    assert spawn.calls == []
    assert not tree.exists()
    assert _git(root, "branch", "--list", f"worktree-{SLUG}") == ""
    assert list(receipts.iterdir()) == []


@pytest.mark.parametrize("failed_intent", ["primary", "worktree"])
def test_e_failed_intent_write_spawns_nothing_and_undoes_new_worktree(
    failed_intent, tmp_path, monkeypatch
):
    _require("parse_engine", "_write_json_atomic")
    root, receipts, _base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    tree = _tree(root)
    target = _receipt_path(receipts) if failed_intent == "primary" else _worktree_receipt(root)
    real_replace = os.replace
    spawn = FakeSpawn()

    def fail_receipt_replace(source, destination):
        if Path(destination) == target:
            assert Path(source).is_file()
            raise OSError(f"injected {failed_intent} intent failure")
        return real_replace(source, destination)

    monkeypatch.setattr(d.os, "replace", fail_receipt_replace)
    with pytest.raises(d.LaunchRefused, match="intent failure"):
        _launch(_request(), root, spawn, agents=lambda: [])

    assert spawn.calls == []
    assert not tree.exists()
    assert _git(root, "branch", "--list", f"worktree-{SLUG}") == ""
    assert list(receipts.iterdir()) == []
    assert not list(root.rglob("*.tmp"))


@pytest.mark.parametrize("spawn_failure", ["oserror", "launch-refused", "nonzero"])
@pytest.mark.parametrize("reuse", [False, True])
def test_f_confirmed_spawn_failure_undoes_only_this_call_and_restores_old_receipts(
    spawn_failure, reuse, tmp_path, monkeypatch
):
    _require("parse_engine", "_write_json_atomic")
    root, receipts, base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    tree = _tree(root)
    prior_primary = None
    prior_worktree = None
    if reuse:
        _git(root, "worktree", "add", "-q", "-b", f"worktree-{SLUG}", str(tree), base)
        body = _prior_receipt(CONDUCTOR_CONTRACT, tree, base)
        prior_primary = _write_receipt(_receipt_path(receipts), body)
        if spawn_failure != "nonzero":
            prior_worktree = _write_receipt(_worktree_receipt(root), body)
    monkeypatch.setattr(d, "process_alive", lambda _pid: False)
    prelaunch_calls = []

    def prelaunch(_request, repair=False):
        prelaunch_calls.append(repair)
        return d.PreLaunch(True)

    if spawn_failure == "oserror":
        def spawn(*_args, **_kwargs):
            raise OSError("injected spawn failure")
    elif spawn_failure == "launch-refused":
        def spawn(*_args, **_kwargs):
            raise d.LaunchRefused("injected spawn refusal")
    else:
        def spawn(*_args, **_kwargs):
            return d.Spawned(returncode=9, stdout="no process", pid=None)

    with pytest.raises(d.LaunchRefused):
        _launch(_request(), root, spawn, prelaunch=prelaunch, agents=lambda: [])

    assert prelaunch_calls == [reuse]
    assert tree.exists() is reuse
    branch = _git(root, "branch", "--list", f"worktree-{SLUG}")
    assert bool(branch) is reuse
    listing = _git(root, "worktree", "list", "--porcelain")
    assert (str(tree) in listing) is reuse
    if reuse:
        assert _receipt_path(receipts).read_bytes() == prior_primary
        if prior_worktree is None:
            assert not _worktree_receipt(root).exists()
        else:
            assert _worktree_receipt(root).read_bytes() == prior_worktree
    else:
        assert not _receipt_path(receipts).exists()
        assert not _worktree_receipt(root).exists()
    assert not _pid_path(receipts).exists()


@pytest.mark.parametrize("failed_final", ["primary", "worktree"])
def test_g_final_receipt_failure_keeps_pid_worktree_and_relaunch_hold(
    failed_final, tmp_path, monkeypatch
):
    _require("parse_engine", "_write_json_atomic")
    root, receipts, _base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    tree = _tree(root)
    primary = _receipt_path(receipts)
    worktree_copy = _worktree_receipt(root)
    target = primary if failed_final == "primary" else worktree_copy
    real_replace = os.replace
    matching_replaces = 0

    def fail_final_replace(source, destination):
        nonlocal matching_replaces
        if Path(destination) == target:
            matching_replaces += 1
            if matching_replaces == 2:
                raise OSError(f"injected {failed_final} final failure")
        return real_replace(source, destination)

    monkeypatch.setattr(d.os, "replace", fail_final_replace)
    monkeypatch.setattr(d, "process_alive", lambda pid: pid == 7301)
    clock = FakeClock()
    monkeypatch.setattr(d, "_age_seconds", clock.age_seconds)
    spawn = FakeSpawn(7301)

    with pytest.raises(d.LaunchIncomplete) as incomplete:
        _launch(_request(), root, spawn, agents=lambda: [])

    message = str(incomplete.value)
    assert "7301" in message
    assert tree.is_dir()
    assert _git(root, "branch", "--list", f"worktree-{SLUG}")
    assert json.loads(_pid_path(receipts).read_text(encoding="utf-8"))["pid"] == 7301
    primary_body = json.loads(primary.read_text(encoding="utf-8"))
    worktree_body = json.loads(worktree_copy.read_text(encoding="utf-8"))
    if failed_final == "primary":
        assert primary_body["job_id"] == worktree_body["job_id"] == "pending"
        assert "pid" not in primary_body and "pid" not in worktree_body
    else:
        assert primary_body["job_id"] == "conductor-7301" and primary_body["pid"] == 7301
        assert worktree_body["job_id"] == "pending" and "pid" not in worktree_body
        assert str(worktree_copy) in message
    assert subst_gate.launch_receipt_problems(root, SLUG, BATCH, receipts_dir=receipts) == []
    assert subst_gate.launch_receipt_problems(tree, SLUG, BATCH) == []

    clock.advance(d.LISTING_LAG_SECONDS + 100)
    with pytest.raises(d.AlreadyLaunched):
        _launch(
            _request(),
            root,
            FakeSpawn(7302),
            agents=lambda: pytest.fail("conductor liveness must come from its recorded pid"),
        )


def test_h_pid_record_failure_is_fail_closed_even_after_listing_lag_until_receipts_are_cleared(
    tmp_path, monkeypatch
):
    _require("parse_engine", "_write_json_atomic")
    root, receipts, _base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    tree = _tree(root)
    primary = _receipt_path(receipts)
    worktree_copy = _worktree_receipt(root)
    pid_record = _pid_path(receipts)
    real_replace = os.replace

    def fail_pid_replace(source, destination):
        destination = Path(destination)
        if destination in (primary, worktree_copy):
            replaced = real_replace(source, destination)
            intent_snapshots[destination] = destination.read_bytes()
            return replaced
        if destination == pid_record:
            raise OSError("injected pid-record failure")
        return real_replace(source, destination)

    intent_snapshots = {}
    monkeypatch.setattr(d.os, "replace", fail_pid_replace)
    alive_checks = []
    monkeypatch.setattr(d, "process_alive", lambda pid: alive_checks.append(pid) or True)
    spawn = FakeSpawn(7401)
    with pytest.raises(d.LaunchIncomplete) as incomplete:
        _launch(_request(), root, spawn, agents=lambda: [])

    message = str(incomplete.value)
    assert "7401" in message and str(primary) in message and str(worktree_copy) in message
    assert primary.exists() and worktree_copy.exists() and not pid_record.exists()
    assert primary.read_bytes() == intent_snapshots[primary]
    assert worktree_copy.read_bytes() == intent_snapshots[worktree_copy]
    assert not [path for path in receipts.rglob("*") if path.is_file() and ".tmp" in path.name]
    primary_body = json.loads(primary.read_text(encoding="utf-8"))
    worktree_body = json.loads(worktree_copy.read_text(encoding="utf-8"))
    for body in (primary_body, worktree_body):
        assert body["job_id"] == "pending"
        assert body["engine"] == "conductor" and "pid" not in body
    assert subst_gate.launch_receipt_problems(root, SLUG, BATCH, receipts_dir=receipts) == []
    assert subst_gate.launch_receipt_problems(tree, SLUG, BATCH) == []

    clock = FakeClock()
    monkeypatch.setattr(d, "_age_seconds", clock.age_seconds)
    clock.advance(d.LISTING_LAG_SECONDS + 100)
    with pytest.raises(d.AlreadyLaunched) as held:
        _launch(_request(), root, FakeSpawn(7402), agents=lambda: pytest.fail("must not list agents"))
    refusal = str(held.value).lower()
    assert str(primary).lower() in refusal and str(worktree_copy).lower() in refusal
    assert (
        "held: no recorded pid; the dispatcher resolves this by the recorded-pid check "
        "(never a command-line match) and clears the receipt copies only when no recorded process exists"
        in refusal
    )
    assert "operator" not in refusal and "you " not in refusal
    assert "delete" not in refusal and "remove" not in refusal
    assert alive_checks == []

    primary.unlink()
    worktree_copy.unlink()
    monkeypatch.setattr(d.os, "replace", real_replace)
    result = _launch(_request(), root, FakeSpawn(7403), agents=lambda: [])
    assert result.job_id == "conductor-7403"


def test_w2_pidless_refusal_names_both_receipts_and_dispatcher_without_operator_instructions(
    tmp_path, monkeypatch
):
    _require("parse_engine")
    root, receipts, _base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    tree = _tree(root)
    body = {
        "organ": "launch",
        "engine": "conductor",
        "job_id": "pending",
        "slug": SLUG,
        "batch": BATCH,
        "worktree": str(tree),
        "launched_at": "2026-01-01T00:00:00+00:00",
    }
    _write_receipt(_receipt_path(receipts), body)
    _write_receipt(_worktree_receipt(root), body)

    held = d._held_by(SLUG, body, agents=lambda: [])

    assert str(_receipt_path(receipts)) in held
    assert str(_worktree_receipt(root)) in held
    assert (
        "held: no recorded pid; the dispatcher resolves this by the recorded-pid check "
        "(never a command-line match) and clears the receipt copies only when no recorded process exists"
        in held
    )
    assert "operator" not in held.lower()
    assert "you " not in held.lower()
    assert "delete" not in held.lower() and "remove" not in held.lower()


def test_i_recorded_pid_liveness_holds_the_slug_and_a_dead_pid_allows_relaunch(
    tmp_path, monkeypatch
):
    _require("parse_engine")
    root, receipts, base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    body = _prior_receipt(CONDUCTOR_CONTRACT, _tree(root), base, pid=7501)
    _write_receipt(_receipt_path(receipts), body)
    alive = {7501: True, 7502: False}
    monkeypatch.setattr(d, "process_alive", lambda pid: alive.get(pid, False))
    spawn = FakeSpawn(7502)
    prelaunch_calls = []

    def prelaunch(_request, repair=False):
        prelaunch_calls.append(repair)
        return d.PreLaunch(True)

    with pytest.raises(d.AlreadyLaunched):
        _launch(
            _request(),
            root,
            spawn,
            prelaunch=prelaunch,
            agents=lambda: pytest.fail("a conductor receipt is identified by its recorded pid"),
        )
    assert spawn.calls == [] and prelaunch_calls == []

    alive[7501] = False
    result = _launch(_request(), root, spawn, prelaunch=prelaunch, agents=lambda: [])
    assert result.job_id == "conductor-7502"
    assert prelaunch_calls == [False]


def test_j_real_occupancy_gate_allows_only_the_registered_repair_worktree_and_preserves_history(
    tmp_path, monkeypatch
):
    _require("parse_engine")
    root, receipts, base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    tree = _tree(root)
    monkeypatch.setattr(d, "process_alive", lambda _pid: False)
    prelaunch_calls = []

    def real_occupancy_prelaunch(request, repair=False):
        prelaunch_calls.append((repair, tree.exists()))
        with monkeypatch.context() as scoped:
            scoped.delenv("HARNESS_REPAIR", raising=False)
            if repair:
                scoped.setenv("HARNESS_REPAIR", "1")
            try:
                result = wo.check(request.slug, root, sessions=[])
            except wo.OccupancyError as exc:
                return d.PreLaunch(False, str(exc))
        return d.PreLaunch(not result.occupied, ", ".join(result.fired))

    first = _launch(_request(), root, FakeSpawn(7601), prelaunch=real_occupancy_prelaunch)
    assert first.job_id == "conductor-7601"
    assert prelaunch_calls == [(False, False)]

    with monkeypatch.context() as scoped:
        scoped.delenv("HARNESS_REPAIR", raising=False)
        ordinary = wo.check(SLUG, root, sessions=[])
        assert ordinary.occupied and set(ordinary.fired) == {"worktree", "directory", "branch"}
    with monkeypatch.context() as scoped:
        scoped.setenv("HARNESS_REPAIR", "1")
        repaired = wo.check(SLUG, root, sessions=[])
        assert repaired.occupied is False

    second = _launch(_request(), root, FakeSpawn(7602), prelaunch=real_occupancy_prelaunch)
    assert second.job_id == "conductor-7602"
    assert prelaunch_calls[-1] == (True, True)
    assert _git(tree, "rev-parse", "HEAD") == base
    updated = json.loads(_receipt_path(receipts).read_text(encoding="utf-8"))
    assert updated["base"] == base
    assert updated["launches"][0]["job_id"] == "conductor-7601"
    assert updated["launches"][0]["kind"] == "launch"


@pytest.mark.parametrize("base_choice", ["recorded", "fresh", "neither"])
def test_j_reuse_selects_only_an_ancestor_base_and_names_both_failed_candidates(
    base_choice, tmp_path, monkeypatch
):
    _require("parse_engine")
    root, receipts, ancestor = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    fresh = _commit(root, "main-next.txt", "main next\n")
    _git(root, "update-ref", "refs/remotes/origin/main", fresh)
    _git(root, "checkout", "-q", "-b", "candidate-recorded", ancestor)
    recorded_fork = _commit(root, "recorded-fork.txt", "recorded fork\n")
    _git(root, "checkout", "-q", "main")
    _git(root, "checkout", "-q", "-b", "candidate-fresh", ancestor)
    fresh_fork = _commit(root, "fresh-fork.txt", "fresh fork\n")
    _git(root, "checkout", "-q", "main")

    tree = _tree(root)
    _git(root, "worktree", "add", "-q", "-b", f"worktree-{SLUG}", str(tree), fresh)
    if base_choice == "recorded":
        prior_base, selected = ancestor, ancestor
    elif base_choice == "fresh":
        prior_base, selected = recorded_fork, fresh
    else:
        prior_base, selected = recorded_fork, None
        monkeypatch.setenv("HARNESS_BASE", "candidate-fresh")
    _write_receipt(
        _receipt_path(receipts),
        _prior_receipt(CONDUCTOR_CONTRACT, tree, prior_base, pid=7651),
    )
    _write_receipt(
        _worktree_receipt(root),
        _prior_receipt(CONDUCTOR_CONTRACT, tree, prior_base, pid=7651),
    )
    monkeypatch.setattr(d, "process_alive", lambda _pid: False)
    spawn = FakeSpawn(7652)
    prelaunch_calls = []

    def prelaunch(_request, repair=False):
        prelaunch_calls.append(repair)
        return d.PreLaunch(True)

    if selected is None:
        with pytest.raises(d.DispatchRefused) as refused:
            _launch(_request(), root, spawn, prelaunch=prelaunch, agents=lambda: [])
        message = str(refused.value)
        assert _git(tree, "rev-parse", "HEAD") in message
        assert recorded_fork in message and fresh_fork in message
        assert spawn.calls == [] and prelaunch_calls == []
    else:
        _launch(_request(), root, spawn, prelaunch=prelaunch, agents=lambda: [])
        assert prelaunch_calls == [True]
        assert spawn.calls[0]["argv"][spawn.calls[0]["argv"].index("--base") + 1] == selected


@pytest.mark.parametrize("collision", ["different-branch", "plain-directory", "branch-only"])
def test_j_malformed_existing_worktree_or_branch_is_refused_and_left_untouched(
    collision, tmp_path, monkeypatch
):
    _require("parse_engine")
    root, receipts, base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    tree = _tree(root)
    if collision == "different-branch":
        _git(root, "worktree", "add", "-q", "-b", "wrong-lane-branch", str(tree), base)
        with monkeypatch.context() as scoped:
            scoped.setenv("HARNESS_REPAIR", "1")
            with pytest.raises(wo.OccupancyError):
                wo.check(SLUG, root, sessions=[])
    elif collision == "plain-directory":
        tree.mkdir(parents=True)
    else:
        _git(root, "branch", f"worktree-{SLUG}", base)

    before_worktrees = _git(root, "worktree", "list", "--porcelain")
    before_branches = _git(root, "branch", "--list")
    spawn = FakeSpawn()
    prelaunch_calls = []

    def prelaunch(_request, repair=False):
        prelaunch_calls.append(repair)
        return d.PreLaunch(True)

    with pytest.raises(d.DispatchRefused):
        _launch(_request(), root, spawn, prelaunch=prelaunch, agents=lambda: [])

    assert spawn.calls == [] and prelaunch_calls == []
    assert _git(root, "worktree", "list", "--porcelain") == before_worktrees
    assert _git(root, "branch", "--list") == before_branches
    assert tree.exists() is (collision != "branch-only")
    assert list(receipts.iterdir()) == []


def test_k_launch_dry_run_emits_engine_only_for_conductor_and_never_spawns(monkeypatch):
    _require("parse_engine")

    def no_spawn(*_args, **_kwargs):
        pytest.fail("dry-run must not spawn")

    monkeypatch.setattr(d, "spawn_process", no_spawn)
    conductor = CliRunner().invoke(d.cli, ["launch", str(CONDUCTOR_CONTRACT), "--dry-run"])
    assert conductor.exit_code == 0, conductor.output
    conductor_json = json.loads(conductor.output)
    assert conductor_json["engine"] == "conductor"
    assert conductor_json["argv"] == _request().argv

    model = CliRunner().invoke(d.cli, ["launch", str(MODEL_CONTRACT), "--dry-run"])
    assert model.exit_code == 0, model.output
    assert "engine" not in json.loads(model.output)


@pytest.mark.parametrize("guard_case", ["pytest", "fixture"])
def test_l_real_spawn_process_refuses_conductor_argv_before_popen(
    guard_case, tmp_path, monkeypatch
):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    started = []

    def forbidden_popen(argv, **_kwargs):
        started.append(list(argv))
        pytest.fail("the conductor process boundary must not be reached")

    monkeypatch.setattr(d.subprocess, "Popen", forbidden_popen)
    argv = [
        "uv", "run", "--locked", "python", "scripts/conductor.py", "lane", "--run",
        "--contract", str(CONDUCTOR_CONTRACT.resolve()), "--lane", SLUG, "--base", "abc",
        "--receipts", str(d.receipts_dir()), "--row", "4243",
    ]
    env = {}
    if guard_case == "pytest":
        env["PYTEST_CURRENT_TEST"] = "test_l_real_spawn_process_refuses_conductor_argv"
    else:
        argv[argv.index("--contract") + 1] = str(CONDUCTOR_CONTRACT.resolve())

    with pytest.raises(d.LaunchRefused):
        d.spawn_process(argv, env, tmp_path, log_path=tmp_path / "conductor.log")
    assert started == []


def test_l_real_spawn_process_leaves_a_non_provider_interpreter_argv_alone(
    tmp_path, monkeypatch
):
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    calls = []

    def harmless_run(argv, **_kwargs):
        calls.append(list(argv))
        return subprocess.CompletedProcess(argv, 0, stdout="safe\n", stderr="")

    monkeypatch.setattr(d.subprocess, "run", harmless_run)
    result = d.spawn_process([sys.executable, "-c", "print('safe')"], {}, tmp_path)
    assert result.returncode == 0 and result.stdout == "safe\n"
    assert calls == [[sys.executable, "-c", "print('safe')"]]


def _write_conductor_receipt(receipts: Path, slug: str, *, pid: int | None, batch: str = BATCH) -> None:
    body = {
        "organ": "launch",
        "slug": slug,
        "batch": batch,
        "engine": "conductor",
        "job_id": f"conductor-{pid}" if pid is not None else "pending",
    }
    if pid is not None:
        body["pid"] = pid
    _write_receipt(_receipt_path(receipts, slug), body)


def _queue_contracts(directory: Path, slugs: list[str]) -> list[Path]:
    return [_write_contract(directory, slug) for slug in slugs]


def _run_queue(contracts: list[Path], repo: Path, tmp_path: Path, monkeypatch):
    fired = []
    monkeypatch.setattr(d, "list_agents", lambda: [])
    monkeypatch.setattr(d.mag, "free_memory_mb", lambda: 100_000.0)
    monkeypatch.setattr(
        d,
        "launch_lane",
        lambda request, **_kwargs: fired.append(request.slug) or SimpleNamespace(
            job_id=f"job-{request.slug}"
        ),
    )
    state_file = tmp_path / "empty-state.md"
    state_file.write_text("", encoding="utf-8")
    output = CliRunner().invoke(
        d.cli,
        [
            "queue", *map(str, contracts), "--repo-root", str(repo), "--floor-mb", "0",
            "--cap", "4", "--state-file", str(state_file),
        ],
    )
    return output, fired


def test_m_conductor_live_slugs_and_queue_cap_include_unqueued_receipts_without_keyerror(
    tmp_path, monkeypatch
):
    _require("conductor_live_slugs")
    root, receipts, _base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    _write_conductor_receipt(receipts, "live-receipt", pid=8101)
    _write_conductor_receipt(receipts, "live-pid-record", pid=None)
    _write_receipt(_pid_path(receipts, "live-pid-record"), {"pid": 8102})
    _write_conductor_receipt(receipts, "pidless", pid=None)
    _write_conductor_receipt(receipts, "dead", pid=8103)
    _write_receipt(
        _receipt_path(receipts, "model-receipt"),
        {"organ": "launch", "slug": "model-receipt", "provider": "anthropic", "pid": 8104},
    )
    alive = {8101: True, 8102: True, 8103: False, 8104: True}
    live = d.conductor_live_slugs(process_alive=lambda pid: alive.get(pid, False))
    assert live == {"live-receipt", "live-pid-record", "pidless"}
    for slug in ("live-receipt", "live-pid-record", "pidless", "dead", "model-receipt"):
        _receipt_path(receipts, slug).unlink(missing_ok=True)
        _pid_path(receipts, slug).unlink(missing_ok=True)

    queued = ["queue-a", "queue-b", "queue-c", "queue-d", "queue-e"]
    contracts = _queue_contracts(tmp_path / "queued", queued)
    _write_conductor_receipt(receipts, "queue-a", pid=None)
    output, fired = _run_queue(contracts, root, tmp_path, monkeypatch)
    assert output.exit_code == 0, output.output
    assert fired == ["queue-b", "queue-c", "queue-d"]
    assert "queue-e" not in fired

    for slug in ("queue-a", "queue-b", "queue-c", "unlisted-live"):
        _write_conductor_receipt(receipts, slug, pid=None)
    unqueued_output, unqueued_fired = _run_queue(contracts, root, tmp_path, monkeypatch)
    assert unqueued_output.exit_code == 0, unqueued_output.output
    assert unqueued_fired == []


def test_n_job_record_atomic_replace_failure_cleans_tmp_and_names_running_pid(
    tmp_path, monkeypatch
):
    _require("parse_engine", "_write_json_atomic")
    root, receipts, _base = _new_repo(tmp_path / ".dev-knowledge", monkeypatch)
    real_replace = os.replace

    def fail_job_record(source, destination):
        if Path(destination).name.startswith("LAUNCH-JOB-"):
            raise OSError("injected job-record replace failure")
        return real_replace(source, destination)

    monkeypatch.setattr(d.os, "replace", fail_job_record)
    with pytest.raises(d.LaunchIncomplete) as incomplete:
        _launch(_request(), root, FakeSpawn(8201), agents=lambda: [])

    assert "8201" in str(incomplete.value)
    assert not [path for path in receipts.rglob("*") if path.is_file() and ".tmp" in path.name]
