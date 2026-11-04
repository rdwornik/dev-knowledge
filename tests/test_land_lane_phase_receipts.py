"""RED-first tests for receipt-gated merge_path and land_lane behavior."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace

import pytest
from click.testing import CliRunner

_REPO = Path(__file__).resolve().parents[1]
for _path in (str(_REPO), str(_REPO / "scripts")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from ecosystem.schema import phase_receipt  # noqa: E402
import land_lane as ll  # noqa: E402
import merge_path  # noqa: E402
import round_receipts as rr  # noqa: E402

SLUG = "e30-landing-stage-receipts"
BATCH = "E1.0"
ROW = "1858"
PHASES = ("P2", "P3", "P4", "P5", "P6a", "P6b", "P6c", "P7")
_GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "phase-landing-test",
    "GIT_AUTHOR_EMAIL": "phase-landing-test@example.invalid",
    "GIT_COMMITTER_NAME": "phase-landing-test",
    "GIT_COMMITTER_EMAIL": "phase-landing-test@example.invalid",
}


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        encoding="utf-8", env=_GIT_ENV, check=True,
    )
    return result.stdout.strip()


def _commit(repo: Path, name: str, message: str) -> str:
    (repo / name).write_text(message + "\n", encoding="utf-8", newline="\n")
    _git(repo, "add", name)
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _real_repo(tmp_path: Path) -> dict[str, object]:
    repo = tmp_path / "git-repo"
    repo.mkdir()
    _git(repo, "init", "--initial-branch=main")
    base = _commit(repo, "base.txt", "base")
    p2 = _commit(repo, "p2.txt", "p2")
    p3 = _commit(repo, "p3.txt", "p3")
    tip = _commit(repo, "tip.txt", "tip")
    return {"repo": repo, "base": base, "p2": p2, "p3": p3, "tip": tip}


@dataclass
class Rig:
    """The substitution-gate test Rig, with optional real merge-base delegation."""

    first_parent: str = "b" * 40
    second_parent: str = "a" * 40
    real_repo: Path | None = None
    calls: list[list[str]] = field(default_factory=list)
    events: list[str] = field(default_factory=list)

    def git(self, args: list[str]) -> tuple[int, str]:
        self.calls.append(list(args))
        if args[0] == "rev-list":
            return 0, f"{'c' * 40} {self.first_parent} {self.second_parent}"
        if args[0] == "ls-remote":
            return 0, f"{self.first_parent}\trefs/heads/main"
        if args[0] == "push":
            self.events.append("push")
            return 0, ""
        if args[0] == "merge-base" and self.real_repo is not None:
            result = subprocess.run(
                ["git", "-C", str(self.real_repo), *args], capture_output=True, text=True,
                encoding="utf-8", env=_GIT_ENV, check=False,
            )
            return result.returncode, result.stdout.strip() or result.stderr.strip()
        return 1, "unexpected"

    def pushes(self) -> list[list[str]]:
        return [call for call in self.calls if call[0] == "push"]


def _receipt(round_dir: Path, phase: str, *, head_sha: str, outcome: str = "PASS") -> None:
    nonce = "nonce-phase-landing"
    input_hash = "d" * 64
    payload = phase_receipt.PhasePayload(nonce=nonce, input_hash=input_hash, outcome=outcome)
    command = ["claude"]
    data = {
        "schema": "phase-receipt/1",
        "organ": f"phase:{phase}",
        "status": "COMPLETE",
        "exit_code": 0,
        "duration_ms": 1,
        "input_hash": input_hash,
        "model_requested": None,
        "model_reported": None,
        "command": command,
        "finished_at": "2026-11-03T00:00:00Z",
        "row": ROW,
        "lane": SLUG,
        "phase": phase,
        "round": 1,
        "vendor": phase_receipt.vendor_for_argv(command),
        "cli_version": None,
        "served_model": None,
        "started_at": "2026-11-03T00:00:00Z",
        "inputs": [],
        "nonce": nonce,
        "usage": None,
        "payload_sha256": phase_receipt.payload_sha256(payload),
        "payload": payload.model_dump(mode="json"),
        "substituted_from": None,
        "head_sha": head_sha,
    }
    phase_receipt.PhaseReceipt.model_validate(data)
    (round_dir / f"{phase}.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n",
    )


def _receipts(home: Path, world: dict[str, object], *, tip_sha: str | None = None,
              review_sha: str | None = None) -> Path:
    tip = tip_sha or str(world["tip"])
    round_dir = home / f"LANE-{SLUG}" / "r1"
    round_dir.mkdir(parents=True, exist_ok=True)
    phases = [
        {"id": phase, "gate": "exit" if phase in ("P4", "P6c") else "payload"}
        for phase in ("P1", *PHASES)
    ]
    (round_dir / rr.ROUND_HARNESS_NAME).write_text(
        "phases:\n" + "".join(f"  - id: {row['id']}\n    gate: {row['gate']}\n"
                               for row in phases),
        encoding="utf-8", newline="\n",
    )
    for phase in PHASES:
        if phase == "P2":
            head = str(world["base"])
        elif phase == "P3":
            head = str(world["p2"])
        else:
            head = review_sha or tip
        _receipt(round_dir, phase, head_sha=head, outcome="ACCEPT" if phase == "P7" else "PASS")
        if phase == "P4":
            (round_dir / "P4-OUTPUT.txt").write_text("passed\n", encoding="utf-8", newline="\n")
        if phase == "P6c":
            (round_dir / "P6c-OUTPUT.txt").write_text(
                json.dumps({
                    "ref": "refs/heads/main",
                    "sha": tip,
                    "verdict": "green",
                    "run_id": 1,
                    "state": "PASS",
                    "missing_contexts": [],
                }, indent=2) + "\n",
                encoding="utf-8", newline="\n",
            )
    (round_dir / rr.ROUND_VERDICT_NAME).write_text(
        json.dumps({"lane": SLUG, "round": 1, "verdict": "ACCEPT", "head_sha": tip}) + "\n",
        encoding="utf-8", newline="\n",
    )
    return round_dir


def _land(
    tmp_path: Path,
    rig: Rig,
    *,
    receipts_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    require_phase_receipts: bool = False,
    no_push: bool = False,
    operator_act_line: str | None = None,
    verdict_state: str = "PASS",
):
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(receipts_dir))
    monkeypatch.setattr(merge_path, "windows_required_for", lambda *_args: False)
    verdict = SimpleNamespace(
        state=verdict_state,
        missing_contexts=(),
        reason="test verdict",
    )
    return merge_path.land(
        rig.real_repo or tmp_path,
        slug=SLUG,
        batch=BATCH,
        sha="c" * 40,
        base=rig.first_parent,
        git=rig.git,
        verdict_fn=lambda _sha, **_kwargs: verdict,
        record_push_fn=lambda *_args, **_kwargs: None,
        record_suite_fn=lambda *_args, **_kwargs: None,
        no_push=no_push,
        operator_act_line=operator_act_line,
        require_phase_receipts=require_phase_receipts,
    )


def _simple_git(base: str = "b" * 40, merge_sha: str = "c" * 40):
    calls: list[list[str]] = []

    def run(args: list[str]) -> tuple[int, str]:
        calls.append(list(args))
        if args[0] == "fetch":
            return 0, ""
        if args[:2] == ["rev-parse", "origin/main"]:
            return 0, base
        if args[0] == "rev-parse":
            return 0, merge_sha
        if args[0] == "status":
            return 0, ""
        if args[0] in ("checkout", "merge", "add", "commit", "reset"):
            return 0, ""
        if args[0] == "diff" or args[0] == "log":
            return 0, ""
        if args[0] == "rev-list":
            return 0, f"{merge_sha} {base} {'a' * 40}"
        if args[0] == "ls-remote":
            return 0, f"{merge_sha}\trefs/heads/main"
        return 1, "unexpected"

    return run, calls


def _fake_result(*, landed: bool = False, state: str = "PHASE-RECEIPTS-REFUSED"):
    return SimpleNamespace(
        landed=landed,
        state=state,
        reason="phase receipt chain incomplete",
        sha="c" * 40,
        branch=merge_path.integration_branch(BATCH),
        commands=[],
        verdict=None,
        main_sha="",
    )


def _run_lane_with_land_fn(
    tmp_path: Path,
    land_fn,
    *,
    require_phase_receipts: bool = False,
):
    worktree = tmp_path / "integration"
    worktree.mkdir()
    git, _calls = _simple_git()
    return ll.land_lane(
        worktree,
        slug=SLUG,
        batch=BATCH,
        carry_file=tmp_path / "carry.jsonl",
        git=git,
        land_fn=land_fn,
        require_phase_receipts=require_phase_receipts,
        regenerate_fn=lambda _root: [],
        teardown_fn=lambda _root: None,
    )


def test_inactive_land_path_keeps_original_rig_commands_and_writes_no_cost(
    tmp_path, monkeypatch,
):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    rig = Rig(first_parent=world["base"], second_parent=world["tip"])

    result = _land(tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch)

    assert result.landed
    assert {call[0] for call in rig.calls} <= {"rev-list", "ls-remote", "push"}
    assert rr.COST_NAME not in {path.name for path in home.rglob("*") if path.is_file()}


def test_flagged_complete_chain_checks_the_second_parent_and_pushes(
    tmp_path, monkeypatch,
):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _receipts(home, world)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True,
    )

    assert result.landed
    assert rig.pushes()
    assert (round_dir.parent / rr.COST_NAME).is_file()
    assert any(call[0] == "merge-base" for call in rig.calls)


def test_flagged_incomplete_chain_refuses_before_push(tmp_path, monkeypatch):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    lane_dir = home / f"LANE-{SLUG}"
    lane_dir.mkdir(parents=True)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True,
    )

    assert result.state == "PHASE-RECEIPTS-REFUSED"
    assert result.landed is False
    assert rig.pushes() == []


def test_receipt_gate_binds_reviews_to_merge_second_parent_not_first(
    tmp_path, monkeypatch,
):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _receipts(home, world, tip_sha=world["base"], review_sha=world["base"])
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True,
    )

    assert result.state == "PHASE-RECEIPTS-REFUSED"
    assert world["base"] in result.reason and world["tip"] in result.reason
    assert rig.pushes() == []
    assert round_dir.is_dir()


def test_operator_act_is_refused_when_phase_receipts_are_required(tmp_path, monkeypatch):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    _receipts(home, world)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True, operator_act_line="| ACT-1 | ratified |",
    )

    assert result.state == "PHASE-RECEIPTS-REFUSED"
    assert rig.pushes() == []


def test_round_directory_activates_gate_without_flag(tmp_path, monkeypatch):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    (home / f"LANE-{SLUG}").mkdir(parents=True)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    result = _land(tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch)

    assert result.state == "PHASE-RECEIPTS-REFUSED"
    assert rig.pushes() == []


def test_cost_write_failure_refuses_before_any_push(tmp_path, monkeypatch):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    _receipts(home, world)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    def fail_write(*_args, **_kwargs):
        raise OSError("injected write failure")

    monkeypatch.setattr(rr, "write_cost_record", fail_write)
    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True,
    )

    assert result.state == "PHASE-RECEIPTS-REFUSED"
    assert "injected write failure" in result.reason
    assert rig.pushes() == []


def test_cost_record_is_written_before_a_later_integration_push_refusal(tmp_path, monkeypatch):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _receipts(home, world)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])
    write_cost_record = rr.write_cost_record
    write_calls: list[Path] = []

    def observed_write(lane, receipts_dir, root=None):
        path = write_cost_record(lane, receipts_dir, root=root)
        write_calls.append(path)
        rig.events.append("cost")
        return path

    monkeypatch.setattr(rr, "write_cost_record", observed_write)

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True, verdict_state="RED",
    )

    assert result.landed is False
    assert result.state == "RED"
    assert len(rig.pushes()) == 1
    assert (round_dir.parent / rr.COST_NAME).is_file()
    assert write_calls == [round_dir.parent / rr.COST_NAME]
    assert rig.events.index("cost") < rig.events.index("push")


def test_no_push_mode_never_writes_cost_record(tmp_path, monkeypatch):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _receipts(home, world)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True, no_push=True,
    )

    assert result.landed is False and result.would_land is True
    assert rig.pushes() == []
    assert not (round_dir.parent / rr.COST_NAME).exists()


@pytest.mark.parametrize("home_kind", ("ignored-subdir", "outside-repo"))
def test_cost_write_accepts_ignored_or_external_receipts_home(
    tmp_path, monkeypatch, home_kind,
):
    world = _real_repo(tmp_path)
    root = Path(world["repo"])
    home = root / "logs" / "receipts" / "nested" if home_kind == "ignored-subdir" else (
        tmp_path / "external-receipts"
    )
    round_dir = _receipts(home, world)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=root)

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True,
    )

    assert result.landed
    assert (round_dir.parent / rr.COST_NAME).is_file()


def test_in_repo_receipts_home_outside_logs_receipts_refuses_before_push(
    tmp_path, monkeypatch,
):
    world = _real_repo(tmp_path)
    root = Path(world["repo"])
    home = root / "custom-receipts"
    _receipts(home, world)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=root)

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True,
    )

    assert result.state == "PHASE-RECEIPTS-REFUSED"
    assert str(home) in result.reason
    assert rig.pushes() == []


def test_existing_gitignore_covers_run_cost_record():
    result = subprocess.run(
        ["git", "check-ignore", "-q", "logs/receipts/LANE-x/RUN-COST.json"],
        cwd=_REPO, check=False,
    )

    assert result.returncode == 0


def test_land_lane_without_flag_does_not_pass_new_keyword_to_legacy_land_fn(tmp_path):
    seen: dict[str, object] = {}

    def legacy_land_fn(_root, *, slug, batch, sha, base, timeout_s, interval_s, git,
                       finalize_fn):
        seen.update(locals())
        return _fake_result()

    report = _run_lane_with_land_fn(tmp_path, legacy_land_fn)

    assert report.state == "REFUSED"
    assert "require_phase_receipts" not in seen


def test_land_lane_passes_receipt_keyword_only_when_flag_is_true(tmp_path):
    seen: dict[str, object] = {}

    def modern_land_fn(_root, *, slug, batch, sha, base, timeout_s, interval_s, git,
                       finalize_fn, require_phase_receipts=False):
        seen["require_phase_receipts"] = require_phase_receipts
        return _fake_result()

    report = _run_lane_with_land_fn(
        tmp_path, modern_land_fn, require_phase_receipts=True,
    )

    assert report.state == "REFUSED"
    assert seen["require_phase_receipts"] is True


def test_land_lane_refusal_report_and_cli_use_existing_exit_code_five(tmp_path, monkeypatch):
    captured: dict[str, object] = {}
    worktree = tmp_path / "integration"
    worktree.mkdir()
    fake_git, _calls = _simple_git()

    def cli_git(args: list[str]) -> tuple[int, str]:
        if args[:2] == ["remote", "get-url"]:
            return 0, str(tmp_path)
        return fake_git(args)

    def fake_land(_root, **kwargs):
        captured.update(kwargs)
        return _fake_result()

    monkeypatch.setattr(merge_path, "_run_git", lambda _root: cli_git)
    monkeypatch.setattr(merge_path, "land", fake_land)
    result = CliRunner().invoke(
        ll.cli,
        ["--worktree", str(worktree), "--slug", SLUG, "--batch", BATCH,
         "--carry-file", str(tmp_path / "carry.jsonl"), "--require-phase-receipts"],
    )

    assert result.exit_code == 5
    assert "PHASE-RECEIPTS-REFUSED" in result.output
    assert captured["require_phase_receipts"] is True


def test_dry_run_and_help_expose_receipt_flag_and_plan_line():
    runner = CliRunner()
    planned = runner.invoke(
        ll.cli, ["--slug", SLUG, "--batch", BATCH, "--dry-run", "--require-phase-receipts"],
    )
    help_result = runner.invoke(ll.cli, ["--help"])

    assert planned.exit_code == 0
    lines = planned.output.splitlines()
    assert sum(line.startswith("phase-receipts:") for line in lines) == 1
    assert sum(line.split(":", 1)[0] in ll.STEPS for line in lines) == len(ll.STEPS)
    assert help_result.exit_code == 0
    assert "--require-phase-receipts" in help_result.output


def test_cli_plan_without_flag_remains_unchanged():
    planned = CliRunner().invoke(
        ll.cli, ["--slug", SLUG, "--batch", BATCH, "--dry-run"],
    )

    assert planned.exit_code == 0
    assert not any(line.startswith("phase-receipts:") for line in planned.output.splitlines())
    assert sum(line.split(":", 1)[0] in ll.STEPS for line in planned.output.splitlines()) == len(
        ll.STEPS
    )


def test_operator_act_is_refused_when_receipts_directory_alone_activates_gate(
    tmp_path, monkeypatch,
):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    (home / f"LANE-{SLUG}" / "r1").mkdir(parents=True)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        operator_act_line="| ACT-1 | ratified |",
    )

    assert result.state == "PHASE-RECEIPTS-REFUSED"
    assert rig.pushes() == []


def test_operator_act_without_receipts_directory_still_lands(tmp_path, monkeypatch):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        operator_act_line="| ACT-1 | ratified |",
    )

    assert result.landed
    assert rig.pushes()


@pytest.mark.parametrize(
    ("complete_name", "incomplete_name"),
    [("r2", "r02"), ("r02", "r2")],
)
def test_equal_maximum_round_numbers_refuse_landing_before_push(
    tmp_path, monkeypatch, complete_name, incomplete_name,
):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    complete = _receipts(home, world)
    for path in complete.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["round"] = 2
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    lane_dir = complete.parent
    complete_path = lane_dir / complete_name
    complete.rename(complete_path)
    incomplete_path = lane_dir / incomplete_name
    incomplete_path.mkdir()
    for artifact in complete_path.iterdir():
        (incomplete_path / artifact.name).write_bytes(artifact.read_bytes())
    (incomplete_path / "P7.json").unlink()
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True,
    )

    assert result.state == "PHASE-RECEIPTS-REFUSED"
    assert str(complete_path) in result.reason
    assert str(incomplete_path) in result.reason
    assert rig.pushes() == []


def test_preexisting_tmp_link_refuses_landing_before_push(tmp_path, monkeypatch):
    world = _real_repo(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _receipts(home, world)
    sentinel = tmp_path / "outside-sentinel.txt"
    sentinel.write_text("unchanged\n", encoding="utf-8", newline="\n")
    scratch = round_dir.parent / f"{rr.COST_NAME}.tmp"
    if sys.platform == "win32":
        os.link(sentinel, scratch)
    else:
        os.symlink(sentinel, scratch)
    rig = Rig(first_parent=world["base"], second_parent=world["tip"], real_repo=world["repo"])

    result = _land(
        tmp_path, rig, receipts_dir=home, monkeypatch=monkeypatch,
        require_phase_receipts=True,
    )

    assert result.state == "PHASE-RECEIPTS-REFUSED"
    assert rig.pushes() == []
    assert sentinel.read_text(encoding="utf-8") == "unchanged\n"
    assert not (round_dir.parent / rr.COST_NAME).exists()
