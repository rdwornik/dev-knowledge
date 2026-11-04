from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
for _path in (str(_REPO), str(_SCRIPTS)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

LANE = "lane-models-e2"
BRANCH = f"worktree-{LANE}"
_PHASES = ("P1", "P2", "P3", "P4", "P5", "P6a", "P6b", "P6c", "P7")
_LABELS = {
    "P1": "spec", "P2": "red", "P3": "implement", "P4": "constraints",
    "P5": "qa", "P6a": "review-1", "P6b": "review-2", "P6c": "ci-verdict",
    "P7": "judge",
}
_MODELS = {
    "P1": ("claude", "claude-sonnet-5-5"),
    "P2": ("codex", "gpt-5.6-terra"),
    "P3": ("claude", "claude-sonnet-5-5"),
    "P4": ("python", None),
    "P5": ("python", None),
    "P6a": ("codex", "gpt-5.6-terra"),
    "P6b": ("claude", "claude-sonnet-5-5"),
    "P6c": ("python", None),
    "P7": ("codex", "gpt-6-sol"),
}
_CHECKS = (
    "branch-purity", "ship-gate", "ratchet", "review-consumer", "branch-naming",
    "transport-write",
)


def _mod(name: str):
    return importlib.import_module(name)


def _git(cwd: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _repo_and_transport(tmp_path: Path) -> tuple[Path, Path, Path]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.name", "test")
    _git(repo, "config", "user.email", "test@example.com")
    (repo / "tracked.txt").write_text("base\n", encoding="utf-8", newline="\n")
    _git(repo, "add", "tracked.txt")
    _git(repo, "commit", "-m", "base")
    bare = tmp_path / "origin.git"
    subprocess.run(["git", "init", "--bare", str(bare)], capture_output=True, text=True, check=True)
    _git(repo, "remote", "add", "origin", str(bare))
    _git(repo, "push", "-u", "origin", "main")
    _git(repo, "checkout", "-b", BRANCH)

    transport = tmp_path / "transport"
    (transport / "to-browser").mkdir(parents=True)
    (transport / "to-cc").mkdir()
    return repo, bare, transport


def _receipt_data(phase: str, *, head: str | None = None, requested: str | None = None,
                  served: str | None = None, substituted_from: str | None = None) -> dict:
    default_head, default_model = _MODELS[phase]
    head = head or default_head
    requested = default_model if requested is None else requested
    served = requested if served is None else served
    vendor = {"claude": "anthropic", "codex": "openai", "copilot": "copilot-enterprise",
              "python": "local"}[head]
    return {
        "schema": "phase-receipt/1", "organ": f"phase:{phase}", "status": "ok", "exit_code": 0,
        "duration_ms": 1, "input_hash": "a" * 64, "model_requested": requested,
        "model_reported": served, "command": [head, "-p", "fixture"],
        "finished_at": "2026-11-03T12:00:00Z", "row": "1857", "lane": LANE,
        "phase": phase, "round": 1, "vendor": vendor, "cli_version": None,
        "served_model": served, "started_at": "2026-11-03T11:59:59Z", "inputs": [],
        "nonce": "n" * 16, "usage": None, "payload_sha256": None, "payload": None,
        "substituted_from": substituted_from, "head_sha": head,
    }


def _write_receipts(round_dir: Path, *, overrides: dict[str, dict] | None = None) -> None:
    from ecosystem.schema.phase_receipt import PhaseReceipt

    overrides = overrides or {}
    round_dir.mkdir(parents=True, exist_ok=True)
    for phase in _PHASES:
        data = {**_receipt_data(phase), **overrides.get(phase, {})}
        PhaseReceipt.model_validate(data)
        (round_dir / f"{phase}.json").write_text(
            json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n"
        )


def _review_payload_override(phase: str, findings: list[dict]) -> dict:
    from ecosystem.schema.phase_receipt import PhasePayload, payload_sha256

    receipt = _receipt_data(phase)
    payload = {
        "nonce": receipt["nonce"],
        "input_hash": receipt["input_hash"],
        "outcome": "PASS",
        "findings": findings,
    }
    return {
        "payload": payload,
        "payload_sha256": payload_sha256(PhasePayload.model_validate(payload)),
    }


def _write_launch(root: Path, lane: str = LANE, batch: str = "E3.0") -> Path:
    path = root / "logs" / "receipts" / f"LAUNCH-{lane.upper()}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"organ": "launch", "batch": batch}) + "\n",
                    encoding="utf-8", newline="\n")
    return path


def _stub_six_checks(monkeypatch, hb) -> None:
    checks = [hb.CheckResult(name, True, "ok") for name in _CHECKS]
    purity = hb.CheckResult("branch-purity", True, "ok")
    monkeypatch.setattr(hb, "run_self_check", lambda *args, **kwargs: (purity, checks))


def _run_with_receipts(monkeypatch, tmp_path, *, overrides=None, launch=True, session=None,
                       env_receipts=None, repo=None, transport=None):
    hb = _mod("handback")
    root, _bare, tr = _repo_and_transport(tmp_path) if repo is None else (repo, None, transport)
    round_dir = tmp_path / "round"
    _write_receipts(round_dir, overrides=overrides)
    if launch:
        _write_launch(root)
    if session is not None:
        (tr / "to-browser" / f"SESSION-{LANE}.md").write_text(
            session, encoding="utf-8", newline="\n"
        )
    if env_receipts is not None:
        monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(env_receipts))
    elif launch:
        monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(root / "logs" / "receipts"))
    else:
        monkeypatch.delenv("HARNESS_RECEIPTS_DIR", raising=False)
    _stub_six_checks(monkeypatch, hb)
    code, receipt = hb.run(
        LANE, BRANCH, "docs-only", root, resolve_transport=lambda: tr / "to-browser",
        receipts_dir=round_dir, batch="E3.0",
    )
    session_path = tr / "to-browser" / f"SESSION-{LANE}.md"
    return hb, code, receipt, root, tr, round_dir, session_path


def test_item3a_all_phases_render_the_exact_checked_block_and_hand_back_cleanly(
    monkeypatch, tmp_path
):
    hb = _mod("handback")
    round_dir = tmp_path / "receipts"
    _write_receipts(round_dir)
    block = hb.models_block_from_receipts(round_dir)
    expected = "\n".join([
        "MODELS:",
        "  spec: requested=claude-sonnet-5-5 served=claude-sonnet-5-5",
        "  red: requested=gpt-5.6-terra served=gpt-5.6-terra",
        "  implement: requested=claude-sonnet-5-5 served=claude-sonnet-5-5",
        "  constraints: not applicable (deterministic phase P4)",
        "  qa: not applicable (deterministic phase P5)",
        "  review-1: requested=gpt-5.6-terra served=gpt-5.6-terra",
        "  review-2: requested=claude-sonnet-5-5 served=claude-sonnet-5-5",
        "  ci-verdict: not applicable (deterministic phase P6c)",
        "  judge: requested=gpt-6-sol served=gpt-6-sol",
    ])
    subst_gate = _mod("subst_gate")
    assert block == expected
    assert subst_gate.check_models_block(block) == ([], [])
    _, code, receipt, root, _tr, _round_dir, session = _run_with_receipts(monkeypatch, tmp_path)
    assert code == hb.EXIT_OK
    text = session.read_text(encoding="utf-8")
    assert text.index("MODELS:") < text.index("## Handback organ self-check")
    lines = [x for x in text.rstrip().splitlines() if x.strip()]
    assert lines[-2].startswith("HANDBACK ")
    assert lines[-1].startswith("STATE ")
    assert receipt["checks"]["models-block"] is True
    problems, _subs = _mod("subst_gate").handback_problems(
        root, LANE, "E3.0", session,
        receipts_dir=Path(os.environ["HARNESS_RECEIPTS_DIR"]),
    )
    assert problems == []


def test_item3b_copilot_receipt_uses_copilot_model_prefix(tmp_path):
    hb = _mod("handback")
    round_dir = tmp_path / "round"
    _write_receipts(round_dir, overrides={
        "P3": {"command": ["copilot", "-p", "fixture"],
               "vendor": "copilot-enterprise", "model_requested": "claude-sonnet-5.5",
               "served_model": "claude-sonnet-5.5", "model_reported": "claude-sonnet-5.5"}
    })

    block = hb.models_block_from_receipts(round_dir)

    assert "  implement: requested=copilot/claude-sonnet-5.5 served=claude-sonnet-5.5" in block
    assert _mod("subst_gate").check_models_block(block) == ([], [])


def test_item3c_null_served_model_is_marked_unverified_without_fabrication(tmp_path):
    hb = _mod("handback")
    round_dir = tmp_path / "round"
    _write_receipts(round_dir, overrides={
        "P6a": {"served_model": None, "model_reported": None}
    })

    block = hb.models_block_from_receipts(round_dir)

    assert ("  review-1: requested=gpt-5.6-terra served=gpt-5.6-terra UNVERIFIED "
            "(receipt P6a.json served_model is null)") in block
    assert json.loads((round_dir / "P6a.json").read_text(encoding="utf-8"))["served_model"] is None
    assert _mod("subst_gate").check_models_block(block) == ([], [])


def test_item3d_substitution_is_reported_only_when_receipt_records_fallback(tmp_path):
    hb = _mod("handback")
    round_dir = tmp_path / "round"
    _write_receipts(round_dir, overrides={
        "P3": {"substituted_from": "openai"}
    })

    block = hb.models_block_from_receipts(round_dir)

    assert ("  implement: requested=claude-sonnet-5-5 served=claude-sonnet-5-5 "
            "VENDOR-FAIL: implement fallback ran after openai failed "
            "(receipt P3.json substituted_from)") in block
    problems, subs = _mod("subst_gate").check_models_block(block)
    assert problems == []
    assert len(subs) == 1


def test_item3e_silent_codex_substitution_refuses_without_writing_session(
    monkeypatch, tmp_path
):
    hb, code, receipt, _root, tr, _rd, session = _run_with_receipts(
        monkeypatch, tmp_path,
        overrides={"P6a": {"served_model": "gpt-6-sol", "model_reported": "gpt-6-sol"}},
    )

    assert code == hb.EXIT_REFUSED
    assert code == 3
    assert receipt["checks"]["models-block"]["ok"] is False
    assert "models-block" in (tr / "to-browser" / f"HANDBACK-REFUSED-{LANE}.md").read_text(
        encoding="utf-8"
    )
    assert not session.exists() or "HANDBACK " not in session.read_text(encoding="utf-8")


def test_item3f_launch_leg_and_landing_gate_use_the_same_receipt_lookup(
    monkeypatch, tmp_path
):
    hb = _mod("handback")
    root, _bare, tr = _repo_and_transport(tmp_path)
    round_dir = tmp_path / "round"
    _write_receipts(round_dir)
    launch_dir = tmp_path / "dispatch-receipts"
    launch_path = _write_launch(launch_dir, lane=LANE)
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(launch_path.parent))
    _stub_six_checks(monkeypatch, hb)

    code, receipt = hb.run(
        LANE, BRANCH, "docs-only", root, resolve_transport=lambda: tr / "to-browser",
        receipts_dir=round_dir, batch="E3.0",
    )
    session = tr / "to-browser" / f"SESSION-{LANE}.md"
    problems, _subs = _mod("subst_gate").handback_problems(
        root, LANE, "E3.0", session, receipts_dir=launch_path.parent
    )
    assert code == hb.EXIT_OK
    assert receipt["checks"]["launch-receipt"] is True
    assert launch_path.parent != round_dir
    assert problems == []

    worktree = root / ".claude" / "worktrees" / LANE
    worktree.parent.mkdir(parents=True, exist_ok=True)
    _git(root, "worktree", "add", "--detach", str(worktree), "main")
    _write_launch(root)
    monkeypatch.delenv("HARNESS_RECEIPTS_DIR", raising=False)
    _stub_six_checks(monkeypatch, hb)
    tr2 = tmp_path / "transport-worktree"
    (tr2 / "to-browser").mkdir(parents=True)
    (tr2 / "to-cc").mkdir()
    code, receipt = hb.run(
        LANE, BRANCH, "docs-only", worktree, resolve_transport=lambda: tr2 / "to-browser",
        receipts_dir=round_dir, batch="E3.0",
    )
    worktree_session = tr2 / "to-browser" / f"SESSION-{LANE}.md"
    problems, _subs = _mod("subst_gate").handback_problems(root, LANE, "E3.0", worktree_session)
    assert code == hb.EXIT_OK
    assert receipt["checks"]["launch-receipt"] is True
    assert problems == []


def test_item3f_missing_launch_receipt_refuses(monkeypatch, tmp_path):
    hb, code, receipt, root, tr, _rd, session = _run_with_receipts(
        monkeypatch, tmp_path, launch=False
    )

    assert code == hb.EXIT_REFUSED
    assert code == 3
    assert receipt["checks"]["launch-receipt"]["ok"] is False
    assert "launch-receipt" in (tr / "to-browser" / f"HANDBACK-REFUSED-{LANE}.md").read_text(
        encoding="utf-8"
    )
    assert not session.exists() or "HANDBACK " not in session.read_text(encoding="utf-8")

    # Done 3(f): with the receipt absent BOTH the organ leg and the landing gate fail
    problems, _subs = _mod("subst_gate").handback_problems(
        root, LANE, "E3.0", session, receipts_dir=None
    )
    assert any(p.startswith("REFUSED [launch-receipt]") for p in problems), problems


def test_item3g_receipt_selection_ignores_neighboring_round_artifacts(tmp_path):
    hb = _mod("handback")
    round_dir = tmp_path / "round"
    _write_receipts(round_dir, overrides={"P3": {
        "command": ["copilot", "-p", "fixture"], "vendor": "copilot-enterprise",
        "model_requested": "claude-sonnet-5.5", "served_model": "claude-sonnet-5.5",
        "model_reported": "claude-sonnet-5.5",
    }})
    for path in round_dir.glob("*.json"):
        if path.name != "P3.json":
            path.unlink()
    for name in ("P3.payload.json", "P3.usage.json", "P3.heartbeat.json", "P3-OUTPUT.txt"):
        (round_dir / name).write_text("{}\n", encoding="utf-8", newline="\n")

    block = hb.models_block_from_receipts(round_dir)

    assert block.splitlines() == [
        "MODELS:",
        "  implement: requested=copilot/claude-sonnet-5.5 served=claude-sonnet-5.5",
    ]


@pytest.mark.parametrize("bad_receipts", ["invalid", "absent"])
def test_item3g_invalid_or_absent_receipts_are_named_in_refusal(
    monkeypatch, tmp_path, bad_receipts
):
    hb = _mod("handback")
    round_dir = tmp_path / "round"
    round_dir.mkdir()
    if bad_receipts == "invalid":
        (round_dir / "P3.json").write_text('{"phase":"P3"}\n', encoding="utf-8", newline="\n")
    (tmp_path / "second").mkdir()
    root, _bare, tr = _repo_and_transport(tmp_path / "second")
    _write_launch(root)
    _stub_six_checks(monkeypatch, hb)
    code, receipt = hb.run(
        LANE, BRANCH, "docs-only", root, resolve_transport=lambda: tr / "to-browser",
        receipts_dir=round_dir, batch="E3.0",
    )

    assert code == hb.EXIT_REFUSED
    assert receipt["checks"]["models-block"]["ok"] is False
    refusal = (tr / "to-browser" / f"HANDBACK-REFUSED-{LANE}.md").read_text(encoding="utf-8")
    if bad_receipts == "absent":
        assert "P3.json" in refusal or "P<id>.json" in refusal
    else:
        assert "P3.json" in refusal


def test_item3g_existing_models_header_refuses_without_appending(monkeypatch, tmp_path):
    hb, code, receipt, _root, tr, _round_dir, session = _run_with_receipts(
        monkeypatch, tmp_path, session="# SESSION\n\nMODELS:\n  old: requested=x served=x\n"
    )

    assert code == hb.EXIT_REFUSED
    assert receipt["checks"]["models-block"]["ok"] is False
    before = "# SESSION\n\nMODELS:\n  old: requested=x served=x\n"
    assert session.read_text(encoding="utf-8") == before
    assert "MODELS:" in (tr / "to-browser" / f"HANDBACK-REFUSED-{LANE}.md").read_text(
        encoding="utf-8"
    )


def test_item3h_cli_batch_requires_receipts_dir_and_receipts_dir_reads_launch_batch(
    monkeypatch, tmp_path, capsys
):
    hb = _mod("handback")
    with pytest.raises(SystemExit) as err:
        hb._parser().parse_args(["run", "--lane", LANE, "--branch", BRANCH,
                                 "--class", "docs-only", "--batch", "E3.0"])
    assert err.value.code == 2
    parser_args = hb._parser().parse_args([
        "run", "--lane", LANE, "--branch", BRANCH, "--class", "docs-only",
        "--receipts-dir", str(tmp_path / "round"),
    ])
    assert parser_args.receipts_dir == str(tmp_path / "round")
    with pytest.raises(SystemExit) as base_err:
        hb._parser().parse_args(["run", "--lane", LANE, "--branch", BRANCH,
                                 "--class", "docs-only", "--base", "HEAD"])
    assert base_err.value.code == 2

    (tmp_path / "cli").mkdir()
    root, _bare, tr = _repo_and_transport(tmp_path / "cli")
    round_dir = tmp_path / "cli-round"
    _write_receipts(round_dir)
    launch_path = _write_launch(root)
    run_kwargs = []
    _stub_six_checks(monkeypatch, hb)
    monkeypatch.setattr(hb, "_ROOT", root)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(tr))
    real_run = hb.run
    # The CLI resolves the Windows User-scope transport before the patched environment.
    monkeypatch.setattr(
        hb, "run",
        lambda *a, **k: (
            run_kwargs.append(k.copy()),
            real_run(*a, resolve_transport=lambda: tr / "to-browser", **k),
        )[1],
    )
    exit_code = hb.main([
        "run", "--lane", LANE, "--branch", BRANCH, "--class", "docs-only",
        "--repo", str(root), "--receipts-dir", str(round_dir),
    ])
    out = capsys.readouterr().out
    receipt = json.loads(out[out.rindex("\n{") + 1:] if "\n{" in out else out)
    assert exit_code == hb.EXIT_OK
    assert run_kwargs[0]["batch"] is None
    assert receipt["checks"]["launch-receipt"] is True
    assert json.loads(launch_path.read_text(encoding="utf-8"))["batch"] == "E3.0"
    assert (tr / "to-browser" / f"SESSION-{LANE}.md").is_file()


# Done 3(h): --receipts-dir alone fails the launch-receipt leg when the LAUNCH receipt (and so the batch) is absent
def test_item3h_receipts_dir_alone_fails_launch_receipt_leg_without_a_launch_receipt(
    monkeypatch, tmp_path, capsys
):
    hb = _mod("handback")
    root, _bare, tr = _repo_and_transport(tmp_path)
    round_dir = tmp_path / "round"
    _write_receipts(round_dir)
    monkeypatch.delenv("HARNESS_RECEIPTS_DIR", raising=False)
    _stub_six_checks(monkeypatch, hb)

    code, receipt = hb.run(
        LANE, BRANCH, "docs-only", root, resolve_transport=lambda: tr / "to-browser",
        receipts_dir=round_dir, batch=None,
    )
    refusal = tr / "to-browser" / f"HANDBACK-REFUSED-{LANE}.md"
    session = tr / "to-browser" / f"SESSION-{LANE}.md"

    assert code == hb.EXIT_REFUSED
    assert receipt["checks"]["launch-receipt"]["ok"] is False
    assert refusal.is_file()
    assert "launch-receipt" in refusal.read_text(encoding="utf-8")

    cli_tmp = tmp_path / "cli-no-launch"
    cli_tmp.mkdir()
    cli_root, _cli_bare, cli_tr = _repo_and_transport(cli_tmp)
    cli_round = cli_tmp / "round"
    _write_receipts(cli_round)
    monkeypatch.setattr(hb, "_ROOT", cli_root)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(cli_tr))
    monkeypatch.delenv("HARNESS_RECEIPTS_DIR", raising=False)
    _stub_six_checks(monkeypatch, hb)
    real_run = hb.run
    monkeypatch.setattr(
        hb, "run",
        lambda *a, **k: real_run(
            *a, resolve_transport=lambda: cli_tr / "to-browser", **k
        ),
    )
    exit_code = hb.main([
        "run", "--lane", LANE, "--branch", BRANCH, "--class", "docs-only",
        "--repo", str(cli_root), "--receipts-dir", str(cli_round),
    ])
    out = capsys.readouterr().out
    receipt = json.loads(out[out.rindex("\n{") + 1:] if "\n{" in out else out)
    assert exit_code == 3
    assert receipt["checks"]["launch-receipt"]["ok"] is False
    assert not session.exists() or "HANDBACK " not in session.read_text(encoding="utf-8")


def test_item3i_without_receipts_dir_retains_exactly_the_original_six_legs(
    monkeypatch, tmp_path
):
    hb = _mod("handback")
    assert callable(getattr(hb, "models_block_from_receipts", None))
    root, _bare, tr = _repo_and_transport(tmp_path)
    _stub_six_checks(monkeypatch, hb)

    code, receipt = hb.run(
        LANE, BRANCH, "docs-only", root, resolve_transport=lambda: tr / "to-browser"
    )

    assert code == hb.EXIT_OK
    assert set(receipt["checks"]) == set(_CHECKS)


def test_code_handback_derives_review_evidence_or_refuses_without_review_payloads(
    monkeypatch, tmp_path
):
    hb = _mod("handback")
    root, _bare, tr = _repo_and_transport(tmp_path)
    round_dir = tmp_path / "round"
    _write_receipts(round_dir)
    _write_launch(root)
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(root / "logs" / "receipts"))
    _stub_six_checks(monkeypatch, hb)

    def resolve_transport():
        return tr / "to-browser"

    code, receipt = hb.run(
        LANE, BRANCH, "code", root, resolve_transport=resolve_transport,
        receipts_dir=round_dir, batch="E3.0",
    )
    refusal = tr / "to-browser" / f"HANDBACK-REFUSED-{LANE}.md"
    session = tr / "to-browser" / f"SESSION-{LANE}.md"

    assert code == hb.EXIT_REFUSED == 3
    assert refusal.is_file()
    review_check = receipt["checks"]["review-receipts"]
    assert review_check["ok"] is False
    assert "no review receipt" in review_check["detail"]
    assert not session.exists() or not any(
        line.startswith("HANDBACK ") for line in session.read_text(encoding="utf-8").splitlines()
    )

    _write_receipts(round_dir, overrides={
        "P6a": _review_payload_override("P6a", [
            {"id": "critical", "severity": "CRITICAL",
             "claim": "A critical review finding", "evidence": "P6a evidence"},
            {"id": "info", "severity": "INFO",
             "claim": "An informational review note", "evidence": "P6a note"},
        ]),
        "P6b": _review_payload_override("P6b", []),
    })
    code, receipt = hb.run(
        LANE, BRANCH, "code", root, resolve_transport=resolve_transport,
        receipts_dir=round_dir, batch="E3.0",
    )
    expected = (
        f"HANDBACK {BRANCH} @ {_git(root, 'rev-parse', 'HEAD')} code "
        "review=gpt-5.6-terra/claude-sonnet-5-5 HIGH:1 MED:0 LOW:0"
    )

    assert code == hb.EXIT_OK
    assert receipt["handback"] == expected
    assert expected in session.read_text(encoding="utf-8").splitlines()
