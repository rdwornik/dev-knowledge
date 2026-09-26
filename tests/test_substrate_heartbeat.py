"""L2: a heartbeat — the substrate is proven live on a SCHEDULE, and dispatch reads it ([#554]).

RED-FIRST. Written and run against a tree with no `scripts/substrate_heartbeat.py`, no
`.github/workflows/substrate-heartbeat.yml`, and no heartbeat leg in `validate_substrate`.

WHY A SCHEDULE IS THE WHOLE POINT. The substrate died at one commit and nobody noticed for
weeks BECAUSE NOTHING RAN THERE. A health signal that only fires when someone happens to use
the thing is not a health signal — it is a usage log. The scheduled leg removes the dependency
on usage; the pre-dispatch leg turns what it learns into a REFUSAL AT DISPATCH rather than a
discovery mid-batch.

THE MEASURED CONSTRAINT THIS IS DESIGNED AROUND, not discovered: this repo has NO ACTIONS
SECRETS AT ALL (`gh secret list` -> `[]`, `actions/secrets` -> `total_count: 0`), and
`conductor.yml:178` already guards for the absence of both `CODEX_API_KEY` and
`ANTHROPIC_API_KEY`. So the scheduled leg is built credential-free: a probe that checks
toolchain and declaration identity needs no model. The credentialed extension is DECLARED and
is explicitly not this lane's to resolve (DECLARE section 2 debt 4, operator's word).

WHAT THE CREDENTIAL-FREE PROBE ACTUALLY CATCHES, and it is the real outage rather than a proxy
for it: on 2026-09-14 `provision.sh` reached a call site for a module retired twelve days
earlier, exited non-zero, and Codespaces substituted a recovery container. Checking that every
repo file provisioning NAMES still exists is exactly that defect, and it needs no container, no
credential and no network — `test_a_call_site_pointing_at_a_retired_module_is_DEAD` is it.
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path

import pytest
import yaml

import substrate_heartbeat as hb
import validate_substrate as vs

REPO_ROOT = Path(__file__).resolve().parent.parent
NOW = dt.datetime(2026, 9, 15, 12, 0, tzinfo=dt.timezone.utc)


@pytest.fixture()
def state(tmp_path):
    """The machine-local state dir, pointed at a private tree. The receipt lives OUTSIDE the
    repo now, so a test that wrote it into `tmp_path/repo` would be testing a path nothing uses.
    """
    store = tmp_path / "state"
    store.mkdir()
    return {"DEV_KNOWLEDGE_PROVENANCE_DIR": str(store), "HOME": str(tmp_path)}


def _mini_repo(tmp_path: Path, *, call: str = "scripts/widget.py") -> Path:
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / ".devcontainer").mkdir()
    (root / "logs").mkdir()
    (root / "scripts" / "widget.py").write_text("V = 1\n", encoding="utf-8")
    (root / "scripts" / "substrate_provenance.py").write_text("V = 1\n", encoding="utf-8")
    (root / "pyproject.toml").write_text(
        '[tool.uv]\nrequired-version = "==0.11.19"\n', encoding="utf-8")
    (root / ".python-version").write_text("3.12.10\n", encoding="utf-8")
    (root / ".devcontainer" / "provision.sh").write_text(
        "#!/usr/bin/env bash\n"
        f"uv run python {call}\n"
        "uv run python scripts/substrate_provenance.py write --writer provision.sh\n"
        "uv run python scripts/substrate_provenance.py verify --require-marker\n",
        encoding="utf-8")
    (root / ".devcontainer" / "devcontainer.json").write_text(
        '{\n  // a comment, because devcontainer.json is JSONC\n'
        '  "name": "t",\n'
        '  "onCreateCommand": "bash .devcontainer/provision.sh",\n'
        '  "postCreateCommand": "bash .devcontainer/provision.sh",\n'
        '  "postStartCommand": "bash .devcontainer/provision.sh --gate"\n}\n',
        encoding="utf-8")
    return root


# --- the credential-free declaration probe ------------------------------------------------

def test_a_coherent_declaration_probes_LIVE(tmp_path):
    reading = hb.probe(_mini_repo(tmp_path), "codespace", now=NOW)
    assert reading.status == "live", reading.findings


def test_a_call_site_pointing_at_a_retired_module_is_DEAD(tmp_path):
    """THE 2026-09-14 OUTAGE, as a check that costs no container and no credential.

    `provision.sh` named `scripts/cloud_provisioning.py` after the module was retired; the call
    exited 2, `provision.sh` died, and Codespaces substituted a recovery container while
    reporting Available. Nothing ran on that substrate for two weeks, so nothing found out.
    """
    root = _mini_repo(tmp_path, call="scripts/cloud_provisioning.py")
    reading = hb.probe(root, "codespace", now=NOW)

    assert reading.status == "dead"
    assert any("cloud_provisioning" in f for f in reading.findings), reading.findings


def test_an_unreadable_uv_pin_is_DEAD(tmp_path):
    root = _mini_repo(tmp_path)
    (root / "pyproject.toml").write_text('[tool.uv]\nrequired-version = ">=0.11"\n',
                                         encoding="utf-8")
    assert hb.probe(root, "codespace", now=NOW).status == "dead"


def test_provisioning_losing_its_L1_wiring_is_DEAD(tmp_path):
    """L1 and L2 guard each other. A provision.sh that stopped writing the marker would leave
    every later verify refusing a container that is in fact fine — so the heartbeat treats the
    unwiring as the substrate defect it is, rather than waiting for the first lane to hit it."""
    root = _mini_repo(tmp_path)
    (root / ".devcontainer" / "provision.sh").write_text(
        "#!/usr/bin/env bash\nuv run python scripts/widget.py\n", encoding="utf-8")

    reading = hb.probe(root, "codespace", now=NOW)

    assert reading.status == "dead"
    assert any("substrate_provenance" in f for f in reading.findings), reading.findings


@pytest.mark.live_repo
def test_the_LIVE_repo_declaration_probes_green():
    """The probe against the real tree. If this REDs, the substrate is genuinely broken."""
    reading = hb.probe(REPO_ROOT, "codespace", now=NOW)
    assert reading.status == "live", reading.findings


# --- the receipt --------------------------------------------------------------------------

def test_a_receipt_round_trips(tmp_path, state):
    root = _mini_repo(tmp_path)
    path = hb.write_receipt(root, hb.probe(root, "codespace", now=NOW), env=state)

    assert path == hb.receipt_path(root, state)
    assert root not in path.parents, "the receipt must not live inside the working tree"
    receipt = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["schema"] == hb.SCHEMA
    assert receipt["readings"]["codespace"]["status"] == "live"


def test_a_second_substrate_does_not_clobber_the_first(tmp_path, state):
    """Per-substrate readings, for the same reason L1's marker is per-substrate: one shared
    slot means the last writer's answer is read as everyone's."""
    root = _mini_repo(tmp_path)
    hb.write_receipt(root, hb.probe(root, "codespace", now=NOW), env=state)
    hb.write_receipt(root, hb.probe(root, "cloud", now=NOW), env=state)

    receipt = json.loads(hb.receipt_path(root, state).read_text(encoding="utf-8"))
    assert {"codespace", "cloud"} <= set(receipt["readings"])


# --- the pre-dispatch leg -------------------------------------------------------------------

def test_predispatch_refuses_a_substrate_never_proven_live(tmp_path, state):
    """No receipt is not "unknown, proceed". A substrate nothing has ever proven live is the
    exact state the codespace was in for two weeks while the platform said Available."""
    refusals = hb.predispatch(_mini_repo(tmp_path), "codespace", now=NOW, env=state)
    assert refusals
    assert any("never" in r or "no heartbeat" in r for r in refusals), refusals


def test_predispatch_refuses_a_stale_receipt(tmp_path, state):
    root = _mini_repo(tmp_path)
    old = NOW - dt.timedelta(hours=hb.MAX_AGE_HOURS + 1)
    hb.write_receipt(root, hb.probe(root, "codespace", now=old), env=state)

    refusals = hb.predispatch(root, "codespace", now=NOW, env=state)

    assert refusals
    assert any("stale" in r or "old" in r for r in refusals), refusals


def test_predispatch_refuses_a_dead_receipt_and_names_the_finding(tmp_path, state):
    root = _mini_repo(tmp_path, call="scripts/cloud_provisioning.py")
    hb.write_receipt(root, hb.probe(root, "codespace", now=NOW), env=state)

    refusals = hb.predispatch(root, "codespace", now=NOW, env=state)

    assert refusals
    assert any("cloud_provisioning" in r for r in refusals), refusals


def test_predispatch_accepts_a_fresh_live_receipt(tmp_path, state):
    root = _mini_repo(tmp_path)
    hb.write_receipt(root, hb.probe(root, "codespace", now=NOW), env=state)
    assert hb.predispatch(root, "codespace", now=NOW + dt.timedelta(hours=1), env=state) == []


def test_cli_exit_codes(tmp_path, state, monkeypatch):
    """0 clean · 1 a real violation · 2 could not look — the repo's declared split."""
    monkeypatch.setenv("DEV_KNOWLEDGE_PROVENANCE_DIR", state["DEV_KNOWLEDGE_PROVENANCE_DIR"])
    root = _mini_repo(tmp_path)
    assert hb.main(["probe", "--repo-root", str(root), "--substrate", "codespace",
                    "--write-receipt"]) == 0
    assert hb.main(["predispatch", "--repo-root", str(root), "--substrate", "codespace"]) == 0
    assert hb.main(["predispatch", "--repo-root", str(root), "--substrate", "cloud"]) == 1


# --- the prebuild-freshness leg (LANE-5B2-23 / LANE-5B3-9 Done-contract item 3) --------------

def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                          check=True).stdout.strip()


def _repo_with_devcontainer_history(tmp_path: Path, *, repo="acme/widget") -> tuple[Path, str, str]:
    """A real repo with two commits: an initial one, then one adding `.devcontainer/`.
    Returns (root, sha_before_devcontainer, sha_with_devcontainer)."""
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)
    (root / "README.md").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)
    old_sha = _git(root, "rev-parse", "HEAD")

    (root / ".devcontainer").mkdir()
    (root / ".devcontainer" / "devcontainer.json").write_text("{}\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "add devcontainer"], cwd=root, check=True)
    dc_sha = _git(root, "rev-parse", "HEAD")

    (root / ".devcontainer" / "provisioning.yaml").write_text(
        f"prebuild:\n  repository: {repo}\n  ref: main\n  regions: [EuropeWest]\n",
        encoding="utf-8")
    return root, old_sha, dc_sha


def _bare_origin_with_main(tmp_path: Path) -> Path:
    """A bare `origin` remote carrying one commit on `main`, with no `.devcontainer/` history."""
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(origin)], check=True)
    seed = tmp_path / "seed"
    seed.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=seed, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=seed, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=seed, check=True)
    (seed / "README.md").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=seed, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=seed, check=True)
    subprocess.run(["git", "branch", "-q", "-M", "main"], cwd=seed, check=True)
    subprocess.run(["git", "remote", "add", "origin", str(origin)], cwd=seed, check=True)
    subprocess.run(["git", "push", "-q", "origin", "main"], cwd=seed, check=True)
    return origin


def test_devcontainer_freshness_reads_origin_main_not_the_checked_out_branch(tmp_path):
    """Codex terra review, 2026-09-26 [HIGH]
    (docs/audits/2026-09-26-codex-lane-heartbeat-admission.md): a `workflow_dispatch` run checks
    out the DISPATCHING branch, not main. A lane branch that adds its own `.devcontainer/` commit
    -- never pushed to origin's `main` -- must not make this leg answer against itself; it answers
    against `origin/main`, which here has no `.devcontainer/` history at all."""
    origin = _bare_origin_with_main(tmp_path)
    work = tmp_path / "work"
    subprocess.run(["git", "clone", "-q", str(origin), str(work)], check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=work, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=work, check=True)
    subprocess.run(["git", "checkout", "-q", "-b", "lane"], cwd=work, check=True)
    (work / ".devcontainer").mkdir()
    (work / ".devcontainer" / "devcontainer.json").write_text("{}\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=work, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "add devcontainer on lane only"], cwd=work,
                   check=True)

    assert hb._resolve_main_ref(work) == "origin/main"
    assert hb._newest_devcontainer_commit(work) is None


_WORKFLOWS_WITH_PREBUILD = {"workflows": [
    {"id": 1, "path": ".github/workflows/conductor.yml"},
    {"id": 42, "path": "dynamic/codespaces/create_codespaces_prebuilds"},
]}
_WORKFLOWS_WITHOUT_PREBUILD = {"workflows": [
    {"id": 1, "path": ".github/workflows/conductor.yml"}]}


def test_no_declared_repository_is_undetermined(tmp_path):
    root, _old, _dc = _repo_with_devcontainer_history(tmp_path)
    (root / ".devcontainer" / "provisioning.yaml").write_text("prebuild:\n  ref: main\n",
                                                              encoding="utf-8")
    verdict = hb.prebuild_freshness(root)
    assert verdict.status == "undetermined"
    assert verdict.exit_code == 2


def test_unreadable_workflow_list_falls_back_to_machines(monkeypatch, tmp_path):
    root, _old, _dc = _repo_with_devcontainer_history(tmp_path)
    calls = []

    def fake_gh_json(argv, *, env=None, timeout=30):
        calls.append(argv)
        if "actions/workflows" in argv[1]:
            return None
        if "codespaces/machines" in argv[1]:
            return {"machines": [{"name": "basicLinux32gb", "prebuild_availability": "ready"}]}
        raise AssertionError(f"unexpected gh call: {argv}")

    monkeypatch.setattr(hb, "_gh_json", fake_gh_json)
    verdict = hb.prebuild_freshness(root)

    assert verdict.status == "undetermined"
    assert verdict.exit_code == 2
    assert any("prebuild_availability" in f for f in verdict.findings), verdict.findings
    assert len(calls) == 2


def test_both_read_paths_failing_is_undetermined_and_names_both(monkeypatch, tmp_path):
    root, _old, _dc = _repo_with_devcontainer_history(tmp_path)
    monkeypatch.setattr(hb, "_gh_json", lambda argv, env=None, timeout=30: None)
    verdict = hb.prebuild_freshness(root)
    assert verdict.status == "undetermined"
    assert any("also failed" in f for f in verdict.findings), verdict.findings


def test_no_prebuild_workflow_configured_is_undetermined(monkeypatch, tmp_path):
    root, _old, _dc = _repo_with_devcontainer_history(tmp_path)
    monkeypatch.setattr(hb, "_gh_json",
                        lambda argv, env=None, timeout=30: _WORKFLOWS_WITHOUT_PREBUILD)
    verdict = hb.prebuild_freshness(root)
    assert verdict.status == "undetermined"
    assert any("no auto-generated" in f for f in verdict.findings), verdict.findings


def test_prebuild_workflow_never_succeeded_is_undetermined(monkeypatch, tmp_path):
    root, _old, _dc = _repo_with_devcontainer_history(tmp_path)

    def fake(argv, *, env=None, timeout=30):
        if "actions/workflows" in argv[1] and "runs" not in argv[1]:
            return _WORKFLOWS_WITH_PREBUILD
        return {"workflow_runs": []}

    monkeypatch.setattr(hb, "_gh_json", fake)
    verdict = hb.prebuild_freshness(root)
    assert verdict.status == "undetermined"
    assert any("never completed" in f for f in verdict.findings), verdict.findings


def test_prebuild_containing_the_newest_devcontainer_commit_is_fresh(monkeypatch, tmp_path):
    root, _old, dc_sha = _repo_with_devcontainer_history(tmp_path)
    head = _git(root, "rev-parse", "HEAD")  # == dc_sha here; the prebuild is fully current

    def fake(argv, *, env=None, timeout=30):
        if "runs" in argv[1]:
            return {"workflow_runs": [{"id": 999, "head_sha": head,
                                       "created_at": "2026-09-26T00:00:00Z"}]}
        return _WORKFLOWS_WITH_PREBUILD

    monkeypatch.setattr(hb, "_gh_json", fake)
    verdict = hb.prebuild_freshness(root)

    assert verdict.status == "ok", verdict.findings
    assert verdict.exit_code == 0
    assert verdict.prebuild_run_id == 999
    assert verdict.prebuild_sha == head


def test_prebuild_missing_the_newest_devcontainer_commit_is_refused(monkeypatch, tmp_path):
    """THE 2026-08-26 DEFECT SHAPE: the prebuild's sha is OLDER than the newest commit that
    touches .devcontainer/**, so a codespace built from it would run stale provisioning."""
    root, old_sha, dc_sha = _repo_with_devcontainer_history(tmp_path)

    def fake(argv, *, env=None, timeout=30):
        if "runs" in argv[1]:
            return {"workflow_runs": [{"id": 7, "head_sha": old_sha,
                                       "created_at": "2026-08-22T00:00:00Z"}]}
        return _WORKFLOWS_WITH_PREBUILD

    monkeypatch.setattr(hb, "_gh_json", fake)
    verdict = hb.prebuild_freshness(root)

    assert verdict.status == "refused"
    assert verdict.exit_code == 1
    assert verdict.prebuild_run_id == 7
    assert verdict.prebuild_sha == old_sha
    assert any(dc_sha[:12] in f and "does NOT contain" in f for f in verdict.findings), \
        verdict.findings


def test_prebuild_cli_exit_codes(monkeypatch, tmp_path):
    root, _old, dc_sha = _repo_with_devcontainer_history(tmp_path)
    head = _git(root, "rev-parse", "HEAD")

    def fake(argv, *, env=None, timeout=30):
        if "runs" in argv[1]:
            return {"workflow_runs": [{"id": 1, "head_sha": head}]}
        return _WORKFLOWS_WITH_PREBUILD

    monkeypatch.setattr(hb, "_gh_json", fake)
    assert hb.main(["prebuild", "--repo-root", str(root)]) == 0


# --- the scheduled leg ----------------------------------------------------------------------

@pytest.mark.live_repo
def test_the_heartbeat_workflow_runs_on_a_schedule():
    """A workflow that only fires on push cannot remove the dependency on usage — which is the
    whole reason this layer exists."""
    spec = yaml.safe_load(
        (REPO_ROOT / ".github/workflows/substrate-heartbeat.yml").read_text(encoding="utf-8"))
    # PyYAML parses a bare `on:` key as the boolean True; both spellings are accepted here so
    # the test asserts the workflow's content rather than PyYAML's opinion about its key.
    triggers = spec.get("on", spec.get(True))
    assert "schedule" in triggers, triggers
    assert triggers["schedule"], "a schedule block with no cron is not a schedule"
    assert "workflow_dispatch" in triggers, "the operator must be able to fire it by hand"


@pytest.mark.live_repo
def test_the_container_job_runs_on_a_schedule_not_dispatch_only():
    """LANE-5B2-8 (AMEND-BATCH-WAVE5B-N2-LANE8, R2): the devcontainer-build job re-arms on the
    daily cron, not only on a human's workflow_dispatch. A build leg that only fires when
    someone asks for it by name is the same usage-dependency this whole heartbeat exists to
    remove, one layer up."""
    spec = yaml.safe_load(
        (REPO_ROOT / ".github/workflows/substrate-heartbeat.yml").read_text(encoding="utf-8"))
    container_if = spec["jobs"]["container"]["if"]
    assert "schedule" in container_if, (
        f"container job's `if:` is {container_if!r} — it still gates on workflow_dispatch alone")
    assert "workflow_dispatch" in container_if, (
        "the operator must still be able to fire the build leg by hand")


@pytest.mark.live_repo
def test_the_container_job_asserts_uv_claude_node_and_update_content_command():
    """Done-contract item 1 (LANE-5B2-8): the container job asserts, INSIDE the built container
    and with its own evidence lines, that `uv --version` equals the pyproject.toml pin, that
    `claude` and `node` are on PATH, and that `updateContentCommand` is the command that runs —
    not merely inferred from provision.sh's internal asserts, which a reader of the CI log
    cannot see without already knowing where to look."""
    spec = yaml.safe_load(
        (REPO_ROOT / ".github/workflows/substrate-heartbeat.yml").read_text(encoding="utf-8"))
    steps = spec["jobs"]["container"]["steps"]
    build_step = next(s for s in steps if "runCmd" in s.get("with", {}))
    run_cmd = build_step["with"]["runCmd"]

    assert "uv --version" in run_cmd, "no evidence line for the live uv version"
    assert "pyproject.toml" in run_cmd, "the uv pin must be read from its single source"
    assert "command -v claude" in run_cmd, "no assertion that claude is on PATH"
    assert "command -v node" in run_cmd, "no assertion that node is on PATH"
    assert "updateContentCommand" in run_cmd, "no evidence line naming updateContentCommand"
    assert "scripts/substrate_provenance.py verify --require-marker" in run_cmd, (
        "the L1 marker verify must still run")


@pytest.mark.live_repo
def test_the_container_job_needs_no_model_credential():
    """The build leg is credential-free by the same measurement as the scheduled leg above — a
    repo with no Actions secrets at all cannot arm a leg that expands `secrets.*` on a schedule
    without going permanently red."""
    spec = yaml.safe_load(
        (REPO_ROOT / ".github/workflows/substrate-heartbeat.yml").read_text(encoding="utf-8"))
    steps = spec["jobs"]["container"]["steps"]
    build_step = next(s for s in steps if "runCmd" in s.get("with", {}))
    run_cmd = build_step["with"]["runCmd"]
    used = set(__import__("re").findall(r"\$\{\{\s*secrets\.([A-Za-z0-9_]+)", run_cmd))
    assert not used, f"the container job's runCmd expands {sorted(used)} — no secret is read"


@pytest.mark.live_repo
def test_the_heartbeat_workflow_needs_no_model_credential():
    """MEASURED BLOCKER, designed around rather than discovered: this repo has no Actions
    secrets at all. A scheduled leg that referenced one would never run."""
    REFERENCE = __import__("re").compile(r"\$\{\{\s*secrets\.([A-Za-z0-9_]+)")
    text = (REPO_ROOT / ".github/workflows/substrate-heartbeat.yml").read_text(encoding="utf-8")

    # THE MECHANISM, NOT A SUBSTRING. An earlier spelling of this test asserted the key NAMES
    # were absent from the file and went red on the comment explaining why they are absent —
    # a probe matching its own specification. What makes a workflow depend on a credential is
    # a `${{ secrets.X }}` expansion, so that is what is checked. `GITHUB_TOKEN` is not one of
    # the absent secrets: Actions issues it to every run.
    used = set(REFERENCE.findall(text))
    assert used <= {"GITHUB_TOKEN"}, (
        f"the workflow expands {sorted(used - {'GITHUB_TOKEN'})}, and this repo has no Actions "
        f"secrets at all — the scheduled leg would be permanently red")
    assert "scripts/substrate_heartbeat.py" in text, "the workflow must run the probe"


# --- the pre-dispatch leg, WIRED into the organ that refuses a contract ----------------------

def _cloud_contract(body: str = "") -> str:
    return ("# LANE test\n\n**Substrate:** `codespace`\n\n"
            "**Branch:** `claude/lane-test`\n\n" + body + "\n## Done when\n\n- a thing\n")


def test_validate_substrate_refuses_an_offmachine_lane_with_no_heartbeat(registry_or_none=None):
    """THE WIRING. A dead substrate must be a refusal at DISPATCH, not a discovery mid-batch,
    and this is the organ that refuses a contract before it is dispatched."""
    registry = vs.load_registry(REPO_ROOT)
    refusals = vs.validate_contract(_cloud_contract(), source="t.md", registry=registry,
                                    heartbeat=hb.Receipt.empty())

    assert vs.RULE_HEARTBEAT_DEAD in {r.rule for r in refusals}, [r.rule for r in refusals]


def test_a_local_lane_is_not_gated_on_the_offmachine_heartbeat():
    """A LOCAL lane runs on the operator's machine, whose liveness is not in question — the
    operator is sitting at it. Gating it on a cloud probe would refuse the only substrate that
    is definitely alive."""
    registry = vs.load_registry(REPO_ROOT)
    text = ("# LANE test\n\n**Substrate:** `local`\n\n"
            "**Branch:** `worktree-lane-a-1-thing`\n\n## Done when\n\n- a thing\n")
    refusals = vs.validate_contract(text, source="t.md", registry=registry,
                                    heartbeat=hb.Receipt.empty())

    assert vs.RULE_HEARTBEAT_DEAD not in {r.rule for r in refusals}


def test_a_live_heartbeat_admits_the_offmachine_lane(tmp_path, state):
    registry = vs.load_registry(REPO_ROOT)
    root = _mini_repo(tmp_path)
    hb.write_receipt(root, hb.probe(root, "codespace", now=NOW), env=state)
    receipt = hb.read_receipt(root, env=state)

    refusals = vs.validate_contract(_cloud_contract(), source="t.md", registry=registry,
                                    heartbeat=receipt, now=NOW)

    assert vs.RULE_HEARTBEAT_DEAD not in {r.rule for r in refusals}


def test_the_heartbeat_refusal_is_overridable_by_a_recorded_deviation():
    """The repo's designed escape, and it applies here like every other leg: an override is an
    explicit recorded deviation, never a silent pass."""
    registry = vs.load_registry(REPO_ROOT)
    body = ("**Substrate deviation:** substrate-heartbeat-dead — the operator has just "
            "rebuilt the container by hand and watched provisioning finish; the scheduled "
            "probe has not run since.\n")
    refusals = vs.validate_contract(_cloud_contract(body), source="t.md", registry=registry,
                                    heartbeat=hb.Receipt.empty())

    fired = [r for r in refusals if r.rule == vs.RULE_HEARTBEAT_DEAD]
    assert fired and fired[0].severity == vs.SEVERITY_WARN, fired


def test_the_new_rule_is_in_the_closed_rule_surface():
    assert vs.RULE_HEARTBEAT_DEAD in vs.RULE_IDS


# --- library-first: the recorded check, with a reader so it cannot rot -------------------------

@pytest.mark.live_repo
def test_every_provisioning_leg_carries_a_library_first_verdict():
    """THE RECORD IS ENFORCED, not written. "State your library-first check in the plan, or give
    a one-line reason for its absence" is a requirement, and a requirement discharged in prose
    beside the code is discharged for exactly one lane. This makes it a standing obligation: a
    NEW bespoke provisioning leg cannot be added without either naming the feature that does it
    or writing down why no feature does."""
    import re

    declared = yaml.safe_load(
        (REPO_ROOT / ".devcontainer/provisioning.yaml").read_text(encoding="utf-8"))["features"]
    legs = set(re.findall(
        r"^(leg[a-z0-9_]*)\(\)",
        (REPO_ROOT / ".devcontainer/provision.sh").read_text(encoding="utf-8"), re.M))

    missing = sorted(legs - set(declared))
    assert not missing, (
        f"provisioning legs with no library-first verdict in provisioning.yaml: {missing}. "
        f"Name the devcontainer feature that does it, or record why none does.")
    for name, row in sorted(declared.items()):
        assert row["verdict"] in ("feature", "no-feature", "rejected"), name
        assert len(row.get("reason", "")) >= 40, f"{name}: a token, not a recorded reason"
        if row["verdict"] in ("feature", "rejected"):
            assert row.get("feature"), f"{name}: names no feature but claims to have judged one"


@pytest.mark.live_repo
def test_the_claude_leg_installs_nothing_and_asserts_everything():
    """The deletion is the deliverable, so the deletion is what is pinned.

    A leg that both declares a feature AND keeps its own installer would be library-first in the
    manifest and bespoke in fact — and worse, it would silently repair a broken feature, which
    is precisely how a substrate reports healthy while one of its legs is dead.
    """
    text = (REPO_ROOT / ".devcontainer/provision.sh").read_text(encoding="utf-8")
    body = text.split("leg_f1_claude() {", 1)[1].split("\n}", 1)[0]

    assert "curl" not in body, "the bespoke Claude installer is still here"
    assert "claude" in body and "die " in body, "the assert is the leg; it must still refuse"
    assert "node" in body, "node's absence — not auth — is what blocked copilot and codex"

    spec = json.loads("\n".join(
        "" if line.lstrip().startswith("//") else line
        for line in (REPO_ROOT / ".devcontainer/devcontainer.json")
        .read_text(encoding="utf-8").splitlines()))
    assert "ghcr.io/anthropics/devcontainer-features/claude-code:1.0" in spec["features"]
    assert "ghcr.io/devcontainers/features/node:1" in spec["features"]
