"""RED-first tests for phase-receipt landing checks and run-cost records."""
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

_REPO = Path(__file__).resolve().parents[1]
for _path in (str(_REPO), str(_REPO / "scripts")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from ecosystem.schema import phase_receipt  # noqa: E402
import merge_path  # noqa: E402
import round_receipts as rr  # noqa: E402
from click.testing import CliRunner  # noqa: E402

SLUG = "e30-landing-stage-receipts"
ROW = "1858"
PHASES = ("P2", "P3", "P4", "P5", "P6a", "P6b", "P6c", "P7")
FIXTURES = Path(__file__).parent / "fixtures" / "round_receipts"
_GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "receipt-test",
    "GIT_AUTHOR_EMAIL": "receipt-test@example.invalid",
    "GIT_COMMITTER_NAME": "receipt-test",
    "GIT_COMMITTER_EMAIL": "receipt-test@example.invalid",
}


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        encoding="utf-8", env=_GIT_ENV, check=True,
    )
    return result.stdout.strip()


def _git_runner(repo: Path):
    def run(args: list[str]) -> tuple[int, str]:
        result = subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, text=True,
            encoding="utf-8", env=_GIT_ENV, check=False,
        )
        return result.returncode, result.stdout.strip() or result.stderr.strip()

    return run


def _commit(repo: Path, name: str, message: str) -> str:
    (repo / name).write_text(message + "\n", encoding="utf-8", newline="\n")
    _git(repo, "add", name)
    _git(repo, "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


def _git_world(tmp_path: Path) -> dict[str, object]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "--initial-branch=main")
    base = _commit(repo, "base.txt", "base")
    p2 = _commit(repo, "p2.txt", "p2")
    p3 = _commit(repo, "p3.txt", "p3")
    tip = _commit(repo, "tip.txt", "tip")
    _git(repo, "checkout", "-b", "unrelated", base)
    unrelated = _commit(repo, "unrelated.txt", "unrelated")
    _git(repo, "checkout", "main")
    return {
        "repo": repo,
        "base": base,
        "p2": p2,
        "p3": p3,
        "tip": tip,
        "unrelated": unrelated,
        "git": _git_runner(repo),
    }


def _receipt_data(
    phase: str,
    *,
    lane: str = SLUG,
    round_no: int = 1,
    head_sha: str | None = "a" * 40,
    row: str = ROW,
    command: list[str] | None = None,
    outcome: str = "PASS",
    status: str | None = None,
    payload: bool = True,
    substituted_from: str | None = None,
) -> dict:
    argv = command or ["claude"]
    vendor = phase_receipt.vendor_for_argv(argv)
    nonce = "nonce-round-receipt"
    input_hash = "b" * 64
    phase_payload = phase_receipt.PhasePayload(
        nonce=nonce, input_hash=input_hash, outcome=outcome,
    ) if payload else None
    data = {
        "schema": "phase-receipt/1",
        "organ": f"phase:{phase}",
        "status": status or ("COMPLETE" if payload else "ok"),
        "exit_code": 0,
        "duration_ms": 1,
        "input_hash": input_hash,
        "model_requested": None,
        "model_reported": None,
        "command": argv,
        "finished_at": "2026-11-03T00:00:00Z",
        "row": row,
        "lane": lane,
        "phase": phase,
        "round": round_no,
        "vendor": vendor,
        "cli_version": None,
        "served_model": None,
        "started_at": "2026-11-03T00:00:00Z",
        "inputs": [],
        "nonce": nonce,
        "usage": None,
        "payload_sha256": (
            phase_receipt.payload_sha256(phase_payload) if phase_payload is not None else None
        ),
        "payload": phase_payload.model_dump(mode="json") if phase_payload is not None else None,
        "substituted_from": substituted_from,
        "head_sha": head_sha,
    }
    return data


def _write_receipt(round_dir: Path, phase: str, **kwargs) -> Path:
    round_dir.mkdir(parents=True, exist_ok=True)
    data = _receipt_data(phase, **kwargs)
    phase_receipt.PhaseReceipt.model_validate(data)
    path = round_dir / f"{phase}.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def _write_harness(
    round_dir: Path,
    *,
    phase_ids: tuple[str, ...] | None = None,
    gates: dict[str, str] | None = None,
) -> Path:
    ids = phase_ids or ("P1", "P2", "P3", "P4", "P5", "P6a", "P6b", "P6c", "P7")
    gates = gates or {}
    rows = [
        {"id": phase, "gate": gates.get(phase, "exit" if phase in ("P4", "P6c") else "payload")}
        for phase in ids
    ]
    path = round_dir / rr.ROUND_HARNESS_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({"phases": rows}, sort_keys=False), encoding="utf-8",
                    newline="\n")
    return path


def _write_p6c(round_dir: Path, tip: str, *, state: str = "PASS",
               verdict: str = "green", missing_contexts: list[str] | None = None,
               include_state: bool = True, invalid_json: bool = False,
               sha: str | None = None) -> Path:
    path = round_dir / "P6c-OUTPUT.txt"
    if invalid_json:
        path.write_text("{not-json}\n", encoding="utf-8", newline="\n")
        return path
    data = json.loads((FIXTURES / "p6c-output.json").read_text(encoding="utf-8"))
    data["sha"] = sha or tip
    data["verdict"] = verdict
    data["missing_contexts"] = missing_contexts or []
    if include_state:
        data["state"] = state
    else:
        data.pop("state", None)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def _write_round_verdict(round_dir: Path, tip: str, *, verdict: str = "ACCEPT",
                         head_sha: str | None = None, refused_by: str | None = None) -> Path:
    path = round_dir / rr.ROUND_VERDICT_NAME
    path.write_text(json.dumps({
        "lane": SLUG,
        "round": int(round_dir.name[1:]),
        "verdict": verdict,
        "exit_code": 0,
        "halted_at": None,
        "refused_by": refused_by,
        "head_sha": head_sha or tip,
        "at": "2026-11-03T00:00:00Z",
    }, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def _build_round(
    home: Path,
    world: dict[str, object],
    *,
    lane: str = SLUG,
    round_no: int = 1,
    bound_tip: str | None = None,
    p2_sha: str | None = None,
    p3_sha: str | None = None,
    phase_ids: tuple[str, ...] | None = None,
    gates: dict[str, str] | None = None,
) -> Path:
    tip = bound_tip or str(world["tip"])
    round_dir = home / f"LANE-{lane}" / f"r{round_no}"
    ids = phase_ids or ("P1", "P2", "P3", "P4", "P5", "P6a", "P6b", "P6c", "P7")
    _write_harness(round_dir, phase_ids=ids, gates=gates)
    for phase in PHASES:
        if phase not in ids and phase not in ("P2", "P3", "P4", "P5", "P6a", "P6b", "P7"):
            continue
        head = tip
        if phase == "P2":
            head = p2_sha or str(world["base"])
        elif phase == "P3":
            head = p3_sha or str(world["p2"])
        _write_receipt(round_dir, phase, lane=lane, round_no=round_no, head_sha=head,
                       outcome="ACCEPT" if phase == "P7" else "PASS")
        gate = (gates or {}).get(phase, "exit" if phase in ("P4", "P6c") else "payload")
        if gate == "exit":
            output = round_dir / f"{phase}-OUTPUT.txt"
            if phase == "P6c":
                _write_p6c(round_dir, tip)
            else:
                output.write_text("phase completed\n", encoding="utf-8", newline="\n")
    _write_round_verdict(round_dir, tip)
    return round_dir


def _problems(world: dict[str, object], home: Path, tip: str | None = None,
              lane: str = SLUG) -> list[str]:
    return rr.landing_problems(
        Path(world["repo"]), lane, tip or str(world["tip"]), git=world["git"],
        receipts_dir=home,
    )


def _change_receipt(path: Path, **changes) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(changes)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    return data


def test_complete_round_receipt_chain_passes(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)

    output = (round_dir / "P6c-OUTPUT.txt").read_text(encoding="utf-8")
    assert len(output.splitlines()) > 1
    assert rr.landing_problems(
        world["repo"], SLUG, world["tip"], git=world["git"], receipts_dir=home,
    ) == []


@pytest.mark.parametrize("phase", PHASES)
def test_each_required_phase_receipt_is_required_and_names_its_path(tmp_path, phase):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    path = round_dir / f"{phase}.json"
    path.unlink()

    problems = _problems(world, home)

    assert any(phase in problem and str(path) in problem for problem in problems)


def test_stale_tip_bound_receipt_names_both_shas(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    stale = str(world["p3"])
    _change_receipt(round_dir / "P5.json", head_sha=stale)

    problems = _problems(world, home)

    assert any("P5" in problem and stale in problem and world["tip"] in problem
               for problem in problems)


def test_p2_head_must_be_an_ancestor_of_the_tip(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    path = round_dir / "P2.json"
    _change_receipt(path, head_sha=world["unrelated"])

    problems = _problems(world, home)

    assert any("P2" in problem and str(path) in problem and world["unrelated"] in problem
               and world["tip"] in problem for problem in problems)


def test_p2_head_must_be_an_ancestor_of_p3_head(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world, p2_sha=world["p3"], p3_sha=world["p2"])
    path = round_dir / "P2.json"

    problems = _problems(world, home)

    assert any("P2" in problem and str(path) in problem
               and world["p3"] in problem and world["p2"] in problem
               for problem in problems)


@pytest.mark.parametrize("head_value", ("absent", None))
def test_missing_or_null_head_sha_is_refused(tmp_path, head_value):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    receipt = round_dir / "P5.json"
    data = json.loads(receipt.read_text(encoding="utf-8"))
    if head_value == "absent":
        data.pop("head_sha")
    else:
        data["head_sha"] = None
    receipt.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")

    problems = _problems(world, home)

    assert any("P5" in problem and "head_sha" in problem and str(receipt) in problem
               for problem in problems)


def test_head_sha_prefix_is_not_a_match(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    _change_receipt(round_dir / "P5.json", head_sha=str(world["tip"])[:12])

    problems = _problems(world, home)

    assert any("P5" in problem and str(world["tip"]) in problem for problem in problems)


@pytest.mark.parametrize(
    ("phase", "outcome", "status"),
    [
        ("P7", "REFUSE", "COMPLETE"),
        ("P7", "ACCEPT", "FAILED"),
        ("P7", "INPUT_REQUIRED", "COMPLETE"),
    ],
)
def test_p7_must_succeed_and_accept(tmp_path, phase, outcome, status):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    data = _receipt_data(
        phase, head_sha=world["tip"], outcome=outcome, status=status,
        payload=True,
    )
    if status == "FAILED":
        data["exit_code"] = 1
    path = round_dir / f"{phase}.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")

    problems = _problems(world, home)

    assert any(phase in problem and str(path) in problem for problem in problems)


def test_payload_gate_requires_payload_and_payload_digest(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    data = _receipt_data("P2", head_sha=world["base"], payload=False)
    path = round_dir / "P2.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")

    problems = _problems(world, home)

    assert any("P2" in problem and str(path) in problem for problem in problems)


def test_exit_gate_requires_output_file(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    path = round_dir / "P4-OUTPUT.txt"
    path.unlink()

    problems = _problems(world, home)

    assert any("P4" in problem and str(path) in problem for problem in problems)


@pytest.mark.parametrize(
    ("state", "missing_contexts", "include_state", "invalid_json", "sha"),
    [
        ("PASS", [], True, False, "f" * 40),
        ("REGRESSED", [], True, False, None),
        ("RED", [], True, False, None),
        ("NO-RUN", [], True, False, None),
        ("IN-PROGRESS", [], True, False, None),
        ("UNATTRIBUTED", [], True, False, None),
        ("PASS", ["required-context"], True, False, None),
        ("", [], False, False, None),
        ("", [], True, True, None),
    ],
)
def test_p6c_output_must_be_tip_current_and_landable(
    tmp_path, state, missing_contexts, include_state, invalid_json, sha,
):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    path = _write_p6c(
        round_dir, world["tip"], state=state, missing_contexts=missing_contexts,
        include_state=include_state, invalid_json=invalid_json, sha=sha,
    )

    problems = _problems(world, home)

    assert any("P6c" in problem and str(path) in problem for problem in problems)


@pytest.mark.parametrize(
    ("state", "verdict"),
    [("PRE-EXISTING", "red"), ("PASS", "green")],
)
def test_p6c_uses_merge_path_landable_predicate(tmp_path, state, verdict):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    _write_p6c(round_dir, world["tip"], state=state, verdict=verdict)
    verdict_obj = SimpleNamespace(state=state, missing_contexts=[])

    assert merge_path.is_landable(verdict_obj)
    assert _problems(world, home) == []


@pytest.mark.parametrize(
    ("verdict", "head_sha", "write_file", "raw"),
    [
        ("REFUSED", None, True, None),
        ("ACCEPT", None, False, None),
        ("ACCEPT", "f" * 40, True, None),
        ("", None, True, "{broken"),
    ],
)
def test_round_verdict_must_be_parseable_accepted_and_tip_current(
    tmp_path, verdict, head_sha, write_file, raw,
):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    path = round_dir / rr.ROUND_VERDICT_NAME
    if write_file:
        if raw is not None:
            path.write_text(raw, encoding="utf-8", newline="\n")
        else:
            _write_round_verdict(round_dir, world["tip"], verdict=verdict, head_sha=head_sha)
    else:
        path.unlink()

    problems = _problems(world, home)

    assert any("P7" in problem and str(path) in problem for problem in problems)


def test_refused_round_verdict_names_refusing_phase(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    _write_round_verdict(round_dir, world["tip"], verdict="REFUSED",
                         refused_by="C-VENDOR:P6b")

    problems = _problems(world, home)

    assert any("P6b" in problem and str(round_dir / rr.ROUND_VERDICT_NAME) in problem
               for problem in problems)


@pytest.mark.parametrize(
    ("phase", "changes"),
    [
        ("P5", {"phase": "P4"}),
        ("P5", {"lane": "some-other-lane"}),
        ("P5", {"round": 2}),
    ],
)
def test_receipt_identity_must_match_its_file_lane_and_round(tmp_path, phase, changes):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    path = round_dir / f"{phase}.json"
    _change_receipt(path, **changes)

    problems = _problems(world, home)

    assert any(phase in problem and str(path) in problem for problem in problems)


def test_invalid_phase_receipt_is_refused(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    path = round_dir / "P5.json"
    path.write_text('{"phase":"P5","head_sha":"bad"}\n', encoding="utf-8", newline="\n")

    problems = _problems(world, home)

    assert any("P5" in problem and str(path) in problem for problem in problems)


def test_receipt_row_must_be_nonempty_and_equal_across_chain(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    path = round_dir / "P5.json"
    _change_receipt(path, row="")

    problems = _problems(world, home)

    assert any("P5" in problem and str(path) in problem for problem in problems)
    _change_receipt(path, row="different-row")
    problems = _problems(world, home)
    assert any("P5" in problem and str(path) in problem for problem in problems)


def test_latest_round_is_checked_when_tip_moves_forward(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    _build_round(home, world, round_no=1)
    repo = Path(world["repo"])
    new_tip = _commit(repo, "new-tip.txt", "new-tip")
    world["tip"] = new_tip
    _build_round(home, world, round_no=2)

    assert _problems(world, home) == []


def test_only_old_round_refuses_after_tip_moves_forward(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    _build_round(home, world)
    new_tip = _commit(Path(world["repo"]), "new-tip.txt", "new-tip")

    problems = _problems(world, home, tip=new_tip)

    assert any("P4" in problem and world["tip"] in problem and new_tip in problem
               for problem in problems)


def test_incomplete_newest_round_does_not_fall_back_to_accepted_old_round(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    _build_round(home, world, round_no=1)
    round2 = _build_round(home, world, round_no=2)
    (round2 / "P7.json").unlink()

    problems = _problems(world, home)

    assert any("P7" in problem and str(round2 / "P7.json") in problem for problem in problems)


def test_no_round_names_the_lane_receipts_directory(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    lane_dir = home / f"LANE-{SLUG}"
    lane_dir.mkdir(parents=True)

    problems = _problems(world, home)

    assert any(str(lane_dir) in problem for problem in problems)


def test_p6c_is_required_only_when_rendered_harness_lists_it(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    ids_without_p6c = ("P1", "P2", "P3", "P4", "P5", "P6a", "P6b", "P7")
    round_dir = _build_round(home, world, phase_ids=ids_without_p6c)
    assert not (round_dir / "P6c.json").exists()
    assert _problems(world, home) == []

    (round_dir / rr.ROUND_HARNESS_NAME).write_text(
        yaml.safe_dump({"phases": [{"id": phase, "gate": "payload"}
                                   for phase in (*ids_without_p6c, "P6c")]}),
        encoding="utf-8", newline="\n",
    )
    problems = _problems(world, home)
    assert any("P6c" in problem and str(round_dir / "P6c.json") in problem
               for problem in problems)


def test_required_floor_applies_even_when_harness_lists_fewer_phases(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world, phase_ids=("P1", "P3"))
    (round_dir / "P7.json").unlink()

    problems = _problems(world, home)

    assert any("P7" in problem and str(round_dir / "P7.json") in problem for problem in problems)


def test_round_uses_its_rendered_harness_not_the_root_harness(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    no_p6c = ("P1", "P2", "P3", "P4", "P5", "P6a", "P6b", "P7")
    round_dir = _build_round(home, world, phase_ids=no_p6c)
    (Path(world["repo"]) / "ecosystem").mkdir()
    (Path(world["repo"]) / "ecosystem" / "harness.yaml").write_text(
        "phases:\n  - {id: P6c, gate: exit}\n", encoding="utf-8", newline="\n",
    )

    assert _problems(world, home) == []
    assert round_dir.is_dir()


def test_p5_exit_gate_owes_output_instead_of_payload(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    gates = {"P5": "exit"}
    round_dir = _build_round(home, world, gates=gates)
    path = round_dir / "P5.json"
    data = _receipt_data("P5", head_sha=world["tip"], payload=False)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    output = round_dir / "P5-OUTPUT.txt"
    output.write_text("exit gate passed\n", encoding="utf-8", newline="\n")

    assert _problems(world, home) == []
    output.unlink()
    problems = _problems(world, home)
    assert any("P5" in problem and str(output) in problem for problem in problems)


def test_missing_rendered_harness_fails_closed_even_when_root_has_one(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    (Path(world["repo"]) / "ecosystem").mkdir()
    (Path(world["repo"]) / "ecosystem" / "harness.yaml").write_text(
        yaml.safe_dump({"phases": [{"id": phase, "gate": "payload"} for phase in PHASES]}),
        encoding="utf-8", newline="\n",
    )
    path = round_dir / rr.ROUND_HARNESS_NAME
    path.unlink()

    problems = _problems(world, home)

    assert any(rr.ROUND_HARNESS_NAME in problem and str(path) in problem for problem in problems)


def test_extra_phase_receipt_not_listed_in_harness_is_refused(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    path = _write_receipt(round_dir, "P8")

    problems = _problems(world, home)

    assert any("P8" in problem and str(path) in problem for problem in problems)


def test_non_receipt_round_artifacts_do_not_enter_the_receipt_set(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    for name in ("P8.payload.json", "P8.usage.json", "P8.heartbeat.json",
                 "P8-OUTPUT.txt", ".payload.json"):
        (round_dir / name).write_text("{}\n", encoding="utf-8", newline="\n")

    assert _problems(world, home) == []


def test_unreadable_harness_and_invalid_slug_are_refused(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    round_dir = _build_round(home, world)
    harness = round_dir / rr.ROUND_HARNESS_NAME
    harness.write_text("phases: [\n", encoding="utf-8", newline="\n")

    problems = _problems(world, home)

    assert any(rr.ROUND_HARNESS_NAME in problem and str(harness) in problem for problem in problems)
    invalid = rr.landing_problems(
        Path(world["repo"]), "../x", str(world["tip"]), git=world["git"], receipts_dir=home,
    )
    assert invalid and any("LANE-../x" in problem or "../x" in problem for problem in invalid)


def test_p1_is_outside_the_required_set_by_the_ratified_d1_step_6(tmp_path):
    """G8 Q-G-1b keeps ratified P2..P7: PROPOSAL-ADR-MINIMUM-LINE-2026-11-02.md D1 step 6
    and DIGEST-STRATEGY-SCORES-2026-11-02.md row C12 exclude P1."""
    for p1_variant in ("absent", "invalid-json", "unrelated-head"):
        case_dir = tmp_path / p1_variant
        case_dir.mkdir()
        world = _git_world(case_dir)
        home = case_dir / "receipts"
        round_dir = _build_round(home, world)
        p1 = round_dir / "P1.json"
        if p1_variant == "invalid-json":
            p1.write_text("{not-json}\n", encoding="utf-8", newline="\n")
        elif p1_variant == "unrelated-head":
            _write_receipt(round_dir, "P1", head_sha=world["unrelated"])

        assert _problems(world, home) == []


def test_cost_record_reads_claude_copilot_and_codex_fixture_artifacts(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    lane_dir = tmp_path / f"receipts/LANE-{SLUG}"
    round_dir = lane_dir / "r1"
    round_dir.mkdir(parents=True)
    phases = (
        ("P2", ["claude"], "claude-result.txt"),
        ("P3", ["copilot", "-p", "review", "--usage-output-file",
                str(round_dir / "P3-usage.json")], "copilot-usage.json"),
        ("P4", ["codex"], "codex.stderr"),
    )
    for phase, command, fixture in phases:
        _write_receipt(round_dir, phase, command=command, head_sha="c" * 40)
        if phase == "P3":
            shutil.copyfile(FIXTURES / fixture, round_dir / "P3-usage.json")
        elif phase == "P4":
            shutil.copyfile(FIXTURES / fixture, round_dir / "P4-OUTPUT.txt.stderr")
        else:
            shutil.copyfile(FIXTURES / fixture, round_dir / f"{phase}-OUTPUT.txt")
    for path in round_dir.glob("P[0-9].json"):
        phase_receipt.PhaseReceipt.model_validate(json.loads(path.read_text(encoding="utf-8")))

    record = rr.cost_record(SLUG, tmp_path / "receipts", root=repo)
    by_phase = {row["phase"]: row for row in record["rows"]}

    assert set(record) == {
        "schema", "lane", "rows", "totals_by_provider", "complete", "complete_means",
    }
    assert record["schema"] == rr.COST_SCHEMA
    assert record["lane"] == SLUG
    assert all(set(row) == {
        "round", "phase", "attempt", "vendor", "served_model", "measurements", "source",
        "measured", "lower_bound", "reason",
    } for row in record["rows"])
    assert by_phase["P2"]["vendor"] == "anthropic"
    assert by_phase["P2"]["measurements"] == [{"unit": "usd", "amount": 0.42}]
    assert by_phase["P3"]["vendor"] == "copilot-enterprise"
    assert by_phase["P3"]["measurements"] == [
        {"unit": "premium_requests", "amount": 1},
        {"unit": "aiu", "amount": 0.813256},
    ]
    assert by_phase["P4"]["vendor"] == "openai"
    assert by_phase["P4"]["measurements"] == [{"unit": "tokens", "amount": 7099}]
    decoded = json.loads(json.dumps(record))
    assert decoded["totals_by_provider"]["copilot-enterprise"]["premium_requests"] == 1
    assert decoded["totals_by_provider"]["copilot-enterprise"]["aiu"] == pytest.approx(0.813256)
    assert set(record["totals_by_provider"]["anthropic"]) == {"usd", "unmeasured_attempts"}
    assert set(record["totals_by_provider"]["openai"]) == {"tokens", "unmeasured_attempts"}


def test_copilot_usage_must_be_the_exact_file_inside_its_round(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    receipts = tmp_path / "receipts"
    round_dir = receipts / f"LANE-{SLUG}" / "r1"
    round_dir.mkdir(parents=True)
    outside = tmp_path / "elsewhere" / "same-usage.json"
    outside.parent.mkdir()
    shutil.copyfile(FIXTURES / "copilot-usage.json", outside)
    colliding = round_dir / outside.name
    colliding.write_text(
        '{"totalPremiumRequestCost":99,"totalNanoAiu":999000000000}\n',
        encoding="utf-8", newline="\n",
    )
    _write_receipt(
        round_dir, "P2",
        command=["copilot", "--usage-output-file", str(outside)],
        head_sha="d" * 40,
    )

    row = rr.cost_record(SLUG, receipts, root=repo)["rows"][0]

    assert row["measured"] is False
    assert row["measurements"] == []
    assert row["reason"] == "usage file outside the round directory"
    record_totals = rr.cost_record(SLUG, receipts, root=repo)["totals_by_provider"]
    assert record_totals["copilot-enterprise"]["unmeasured_attempts"] == 1
    assert "premium_requests" not in record_totals["copilot-enterprise"]


def test_relative_copilot_usage_path_resolves_from_repository_root(tmp_path):
    root = tmp_path
    receipts = root / "receipts"
    round_dir = receipts / f"LANE-{SLUG}" / "r1"
    round_dir.mkdir(parents=True)
    usage = round_dir / "P2-usage.json"
    shutil.copyfile(FIXTURES / "copilot-usage.json", usage)
    relative_usage = usage.relative_to(root)
    _write_receipt(
        round_dir, "P2",
        command=["copilot", "--usage-output-file", str(relative_usage)],
        head_sha="d" * 40,
    )

    row = rr.cost_record(SLUG, receipts, root=root)["rows"][0]

    assert row["measured"] is True
    assert row["measurements"] == [
        {"unit": "premium_requests", "amount": 1},
        {"unit": "aiu", "amount": 0.813256},
    ]


@pytest.mark.parametrize(
    ("phase", "command", "artifact", "content", "vendor"),
    [
        ("P2", ["claude"], "P2-OUTPUT.txt", "", "anthropic"),
        ("P3", ["codex"], None, None, "openai"),
        ("P4", ["copilot", "--usage-output-file", "missing.json"], None, None,
         "copilot-enterprise"),
        ("P5", ["python"], None, None, "local"),
    ],
)
def test_unmeasured_costs_are_named_and_never_summed_as_zero(
    tmp_path, phase, command, artifact, content, vendor,
):
    repo = tmp_path / "repo"
    repo.mkdir()
    receipts = tmp_path / "receipts"
    round_dir = receipts / f"LANE-{SLUG}" / "r1"
    round_dir.mkdir(parents=True)
    if command[0] == "copilot":
        command = ["copilot", "--usage-output-file", str(round_dir / "missing.json")]
    _write_receipt(round_dir, phase, command=command, head_sha="e" * 40)
    if artifact is not None:
        (round_dir / artifact).write_text(content, encoding="utf-8", newline="\n")

    record = rr.cost_record(SLUG, receipts, root=repo)
    row = record["rows"][0]
    totals = record["totals_by_provider"][vendor]

    assert record["complete"] is False
    assert row["measured"] is False and row["measurements"] == [] and row["reason"]
    assert "unmeasured_attempts" in totals and totals["unmeasured_attempts"] == 1
    assert not set(totals).intersection({"usd", "premium_requests", "aiu", "tokens"})


def test_substitution_creates_fallback_and_unmeasured_primary_rows(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    receipts = tmp_path / "receipts"
    round_dir = receipts / f"LANE-{SLUG}" / "r1"
    round_dir.mkdir(parents=True)
    usage = round_dir / "P2-usage.json"
    shutil.copyfile(FIXTURES / "copilot-usage.json", usage)
    _write_receipt(
        round_dir, "P2",
        command=["copilot", "--usage-output-file", str(usage)],
        head_sha="a" * 40,
        substituted_from="anthropic",
    )

    record = rr.cost_record(SLUG, receipts, root=repo)

    assert len(record["rows"]) == 2
    fallback, primary = record["rows"]
    assert fallback["attempt"] == "fallback" and fallback["measured"] is True
    assert primary["attempt"] == "primary" and primary["vendor"] == "anthropic"
    assert primary["measured"] is False
    assert primary["reason"] == "overwritten by the fallback's spawn"
    assert record["complete"] is False
    assert record["totals_by_provider"]["anthropic"]["unmeasured_attempts"] == 1


def test_cost_sums_multiple_rounds_and_reports_only_surviving_attempts(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    receipts = tmp_path / "receipts"
    first = receipts / f"LANE-{SLUG}" / "r1"
    second = receipts / f"LANE-{SLUG}" / "r2"
    for round_no, directory, amount in ((1, first, 0.42), (2, second, 0.9)):
        directory.mkdir(parents=True)
        _write_receipt(directory, "P2", round_no=round_no, head_sha="f" * 40,
                       command=["claude"])
        shutil.copyfile(FIXTURES / "claude-result.txt", directory / "P2-OUTPUT.txt")
        result_path = directory / "P2-OUTPUT.txt"
        result_path.write_text(
            f'{{"type":"result","total_cost_usd":{amount}}}\n',
            encoding="utf-8", newline="\n",
        )
    record = rr.cost_record(SLUG, receipts, root=repo)

    assert [(row["round"], row["phase"]) for row in record["rows"]] == [(1, "P2"), (2, "P2")]
    assert record["totals_by_provider"]["anthropic"]["usd"] == pytest.approx(1.32)
    assert record["complete"] is True
    assert "surviving" in record["complete_means"].lower()
    assert len(record["rows"]) == 2


def test_rerun_cost_uses_only_the_surviving_artifact(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    receipts = tmp_path / "receipts"
    round_dir = receipts / f"LANE-{SLUG}" / "r1"
    round_dir.mkdir(parents=True)
    _write_receipt(round_dir, "P2", command=["claude"], head_sha="f" * 40)
    output = round_dir / "P2-OUTPUT.txt"
    output.write_text('{"total_cost_usd":0.42}\n', encoding="utf-8", newline="\n")
    output.write_text('{"total_cost_usd":0.9}\n', encoding="utf-8", newline="\n")

    record = rr.cost_record(SLUG, receipts, root=repo)

    assert len(record["rows"]) == 1
    assert record["rows"][0]["measurements"] == [{"unit": "usd", "amount": 0.9}]
    assert record["complete"] is True
    assert "surviving" in record["complete_means"].lower()


def test_render_and_cost_cli_are_deterministic_and_write_lf_file(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    receipts = tmp_path / "receipts"
    round_dir = receipts / f"LANE-{SLUG}" / "r1"
    round_dir.mkdir(parents=True)
    _write_receipt(round_dir, "P2", command=["claude"], head_sha="a" * 40)
    shutil.copyfile(FIXTURES / "claude-result.txt", round_dir / "P2-OUTPUT.txt")

    first = CliRunner().invoke(rr.cli, ["cost", "--lane", SLUG, "--receipts", str(receipts),
                                        "--root", str(repo)])
    second = CliRunner().invoke(rr.cli, ["cost", "--lane", SLUG, "--receipts", str(receipts),
                                         "--root", str(repo)])
    assert first.exit_code == second.exit_code == 0
    assert first.output.encode() == second.output.encode()
    record = rr.cost_record(SLUG, receipts, root=repo)
    assert rr.render_cost(record) == json.dumps(record, sort_keys=True, indent=2) + "\n"

    written = CliRunner().invoke(
        rr.cli, ["cost", "--lane", SLUG, "--receipts", str(receipts), "--root", str(repo), "--write"],
    )
    target = receipts / f"LANE-{SLUG}" / rr.COST_NAME
    assert written.exit_code == 0
    assert target.read_bytes().endswith(b"\n")
    assert b"\r\n" not in target.read_bytes()
    assert json.loads(target.read_text(encoding="utf-8"))["schema"] == rr.COST_SCHEMA
    assert rr.write_cost_record(SLUG, receipts, root=repo) == target


def test_cost_record_has_units_without_enforcing_caps(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    receipts = tmp_path / "receipts"
    round_dir = receipts / f"LANE-{SLUG}" / "r1"
    round_dir.mkdir(parents=True)
    for phase, command, filename in (
        ("P2", ["claude"], "claude-result.txt"),
        ("P3", ["copilot", "--usage-output-file", str(round_dir / "P3-usage.json")],
         "copilot-usage.json"),
        ("P4", ["codex"], "codex.stderr"),
    ):
        _write_receipt(round_dir, phase, command=command, head_sha="1" * 40)
        target = round_dir / ("P3-usage.json" if phase == "P3" else
                              "P4-OUTPUT.txt.stderr" if phase == "P4" else "P2-OUTPUT.txt")
        shutil.copyfile(FIXTURES / filename, target)

    record = rr.cost_record(SLUG, receipts, root=repo)
    units = {
        unit for provider in record["totals_by_provider"].values()
        for unit in provider if unit != "unmeasured_attempts"
    }

    assert units == {"usd", "premium_requests", "aiu", "tokens"}
    source = Path(rr.__file__).read_text(encoding="utf-8").lower()
    assert "premium requests per run" not in source
    assert "$20" not in source and "15 premium requests" not in source and "$5" not in source


def test_cost_cli_missing_lane_directory_names_it(tmp_path):
    receipts = tmp_path / "receipts"
    lane_dir = receipts / f"LANE-{SLUG}"
    result = CliRunner().invoke(
        rr.cli, ["cost", "--lane", SLUG, "--receipts", str(receipts), "--root", str(tmp_path)],
    )

    assert result.exit_code != 0
    assert str(lane_dir) in result.output


def test_cost_record_missing_lane_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError, match="LANE-e30-landing-stage-receipts"):
        rr.cost_record(SLUG, tmp_path / "receipts", root=tmp_path)


def test_round_receipts_public_names_are_stable():
    assert rr.RECEIPT_HEAD_FIELD == "head_sha"
    assert rr.ROUND_HARNESS_NAME == "harness.contract.yaml"
    assert rr.ROUND_VERDICT_NAME == "ROUND-VERDICT.json"
    assert rr.COST_NAME == "RUN-COST.json"
    assert rr.COST_SCHEMA == "run-cost/1"


def test_check_cli_reports_each_problem_or_ok(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    _build_round(home, world)
    good = CliRunner().invoke(
        rr.cli, ["check", "--lane", SLUG, "--tip", str(world["tip"]),
                 "--receipts", str(home), "--root", str(world["repo"])],
    )
    assert good.exit_code == 0 and good.output.strip() == "OK"
    main_help = CliRunner().invoke(rr.cli, ["check", "--help"])
    assert main_help.exit_code == 0

    path = home / f"LANE-{SLUG}" / "r1" / "P7.json"
    path.unlink()
    bad = CliRunner().invoke(
        rr.cli, ["check", "--lane", SLUG, "--tip", str(world["tip"]),
                 "--receipts", str(home), "--root", str(world["repo"])],
    )
    assert bad.exit_code == 1
    lines = bad.output.splitlines()
    assert len(lines) == 1 and "P7" in lines[0] and str(path) in lines[0]


@pytest.mark.parametrize("receipts_from_env", (True, False))
def test_landing_problems_uses_the_declared_default_receipts_home(
    tmp_path, monkeypatch, receipts_from_env,
):
    world = _git_world(tmp_path)
    if receipts_from_env:
        home = tmp_path / "env-receipts"
        monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(home))
    else:
        home = Path(world["repo"]) / "logs" / "receipts"
        monkeypatch.delenv("HARNESS_RECEIPTS_DIR", raising=False)
    _build_round(home, world)

    problems = rr.landing_problems(
        Path(world["repo"]), SLUG, str(world["tip"]), git=world["git"],
    )

    assert problems == []


def test_round_receipts_cli_verbs_show_help():
    runner = CliRunner()
    for verb in ("check", "cost"):
        result = runner.invoke(rr.cli, [verb, "--help"])
        assert result.exit_code == 0


@pytest.mark.parametrize("verb", ("check", "cost"))
def test_round_receipts_main_runs_the_group(verb):
    result = subprocess.run(
        [sys.executable, str(_REPO / "scripts" / "round_receipts.py"), verb, "--help"],
        cwd=_REPO, capture_output=True, text=True, encoding="utf-8", check=False,
    )

    assert result.returncode == 0, result.stderr


def test_write_cost_record_refuses_lane_directory_symlink_outside_receipts(tmp_path):
    receipts = tmp_path / "receipts"
    receipts.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    lane_dir = receipts / f"LANE-{SLUG}"
    link_kind = "symlink"
    if sys.platform == "win32":     # a junction needs no privilege, a symlink may
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(lane_dir), str(outside)],
            capture_output=True, text=True, check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        link_kind = "junction"
    else:
        os.symlink(outside, lane_dir, target_is_directory=True)

    target = outside / rr.COST_NAME
    scratch = outside / f"{rr.COST_NAME}.tmp"
    try:
        with pytest.raises(Exception):
            rr.write_cost_record(SLUG, receipts, root=tmp_path)

        assert not target.exists()
        assert not scratch.exists()
    finally:
        if link_kind == "symlink":
            lane_dir.unlink()
        else:
            subprocess.run(
                ["cmd", "/c", "rmdir", str(lane_dir)],
                capture_output=True, text=True, check=True,
            )


def test_write_cost_record_writes_under_ordinary_lane_directory(tmp_path):
    receipts = tmp_path / "receipts"
    lane_dir = receipts / f"LANE-{SLUG}"
    lane_dir.mkdir(parents=True)

    target = rr.write_cost_record(SLUG, receipts, root=tmp_path)

    assert target == lane_dir / rr.COST_NAME
    assert target.is_file()
    assert not target.with_name(f"{rr.COST_NAME}.tmp").exists()


@pytest.mark.parametrize(
    "usage_data",
    [
        {"totalPremiumRequestCost": 1},
        {"totalPremiumRequestCost": 1, "totalNanoAiu": None},
        {"totalPremiumRequestCost": 1, "totalNanoAiu": "not-numeric"},
    ],
    ids=("absent", "null", "non-numeric"),
)
def test_copilot_usage_without_numeric_aiu_is_unmeasured(tmp_path, usage_data):
    repo = tmp_path / "repo"
    repo.mkdir()
    receipts = tmp_path / "receipts"
    round_dir = receipts / f"LANE-{SLUG}" / "r1"
    round_dir.mkdir(parents=True)
    usage = round_dir / "P2-usage.json"
    usage.write_text(json.dumps(usage_data) + "\n", encoding="utf-8", newline="\n")
    _write_receipt(
        round_dir, "P2",
        command=["copilot", "--usage-output-file", str(usage)],
        head_sha="d" * 40,
    )

    record = rr.cost_record(SLUG, receipts, root=repo)
    row = record["rows"][0]
    totals = record["totals_by_provider"]["copilot-enterprise"]

    assert row["measured"] is False
    assert row["measurements"] == []
    assert "totalNanoAiu" in row["reason"]
    assert record["complete"] is False
    assert totals["unmeasured_attempts"] == 1
    assert not set(totals).intersection({"premium_requests", "aiu"})


def test_copilot_usage_with_both_numeric_fields_is_measured(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    receipts = tmp_path / "receipts"
    round_dir = receipts / f"LANE-{SLUG}" / "r1"
    round_dir.mkdir(parents=True)
    usage = round_dir / "P2-usage.json"
    usage.write_text(
        '{"totalPremiumRequestCost":1,"totalNanoAiu":813256000}\n',
        encoding="utf-8", newline="\n",
    )
    _write_receipt(
        round_dir, "P2",
        command=["copilot", "--usage-output-file", str(usage)],
        head_sha="d" * 40,
    )

    row = rr.cost_record(SLUG, receipts, root=repo)["rows"][0]

    assert row["measured"] is True
    assert row["measurements"] == [
        {"unit": "premium_requests", "amount": 1},
        {"unit": "aiu", "amount": 0.813256},
    ]


@pytest.mark.parametrize(
    ("complete_name", "incomplete_name"),
    [("r2", "r02"), ("r02", "r2")],
)
def test_equal_maximum_round_numbers_are_refused_with_both_paths(
    tmp_path, complete_name, incomplete_name,
):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    complete = _build_round(home, world, round_no=2)
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

    problems = _problems(world, home)

    assert any(
        str(complete_path) in problem and str(incomplete_path) in problem
        for problem in problems
    )


def test_single_complete_r2_is_accepted(tmp_path):
    world = _git_world(tmp_path)
    home = tmp_path / "receipts"
    _build_round(home, world, round_no=2)

    assert _problems(world, home) == []


def test_write_cost_record_refuses_preexisting_tmp_link_to_outside_file(tmp_path):
    receipts = tmp_path / "receipts"
    lane_dir = receipts / f"LANE-{SLUG}"
    lane_dir.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    sentinel = outside / "sentinel.txt"
    sentinel.write_text("unchanged\n", encoding="utf-8", newline="\n")
    scratch = lane_dir / f"{rr.COST_NAME}.tmp"
    if sys.platform == "win32":
        os.link(sentinel, scratch)
    else:
        os.symlink(sentinel, scratch)

    with pytest.raises(OSError):
        rr.write_cost_record(SLUG, receipts, root=tmp_path)

    assert sentinel.read_text(encoding="utf-8") == "unchanged\n"
    assert not (lane_dir / rr.COST_NAME).exists()
