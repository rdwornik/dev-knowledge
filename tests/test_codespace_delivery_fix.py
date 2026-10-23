from __future__ import annotations

import hashlib
import json
import shlex
from datetime import datetime, timedelta, timezone
from pathlib import Path

import codespace_regime as regime
import dispatch as d


import pytest
import sys


@pytest.fixture(autouse=True)
def _private_receipt_homes(tmp_path_factory, monkeypatch):
    """Same isolation as tests/test_dispatch_codespace.py: no test here reaches the tracked ledger."""
    root = tmp_path_factory.mktemp("receipt-homes")
    monkeypatch.setattr(d, "DEFAULT_HARVEST_ROOT", root / "remote-runs")
    for mod in {id(m): m for m in (regime, d.regime, sys.modules.get("scripts.codespace_regime"),
                                   sys.modules.get("codespace_regime")) if m is not None}.values():
        monkeypatch.setattr(mod, "_REPO_ROOT", root / "repo")
    monkeypatch.setattr(d, "run_prelaunch", lambda *a, **k: d.PreLaunch(True))

_REPORT = {
    "lane": "lane-x",
    "batch": "B1",
    "task": "sample task",
    "kind": "doc",
    "state": "COMPLETED",
    "done": {"met": 1, "total": 1},
    "checks": [],
    "intent_met": None,
    "unresolved": [],
    "operator_action": None,
    "merged_sha": None,
    "producer": {"vendor": "anthropic", "model": "claude-sonnet-5", "session": "session-x"},
    "cost_usd": None,
    "evidence": {"branch": "worktree-x", "check_run": None, "audit": None},
}


def _result(ok: bool = True, stdout: str = "", exit_code: int = 0):
    return d.GhResult(ok=ok, exit_code=exit_code, stdout=stdout)


def _remote_command(argv: list[str]) -> str:
    return argv[argv.index("--") + 1]


def test_runner_and_lane_handbacks_have_distinct_paths(tmp_path):
    runner_file = getattr(d, "RUNNER_HANDBACK_FILE", None)
    assert runner_file == "runner-handback.json"

    script = d._codespace_runner_script("/workspaces/dispatch", "/workspaces/repo", ["true"])
    assert "runner-handback.json" in script
    assert "/workspaces/dispatch/handback.json" not in script
    assert "/workspaces/dispatch/runner-handback.json" in script
    assert all("runner-handback.json" in line for line in script.splitlines()
               if "handback" in line.lower())
    assert {"handback.json", "runner-handback.json"} <= set(d.HARVEST_FILES)

    payloads = {
        "handback.json": b'{"source":"lane"}\n',
        "runner-handback.json": b'{"source":"runner"}\n',
    }

    def fake(argv, timeout=None, **_kw):
        joined = " ".join(argv)
        for name, payload in sorted(payloads.items(), key=lambda kv: -len(kv[0])):
            if name in joined:
                return _result(stdout=payload.decode("utf-8"))
        return _result(ok=False, exit_code=1)

    harvested = d.codespace_harvest("box-1", batch="B1", lane="lane-x",
                                    out_root=tmp_path, invoker=fake)
    assert harvested.ok, harvested.failure
    manifest = json.loads(harvested.manifest_path.read_text(encoding="utf-8"))
    for name, payload in payloads.items():
        assert (harvested.out_dir / name).read_bytes() == payload
        assert name in manifest["files"]


def test_codespace_exec_reads_the_runner_handback_path(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    calls: list[list[str]] = []
    receipt = {"exit_code": 0, "is_error": False, "status": "success"}

    def fake(argv, timeout=None, **_kw):
        argv = list(argv)
        calls.append(argv)
        if argv[:2] == ["codespace", "create"]:
            return _result(stdout="box-1\n")
        if argv[:2] == ["codespace", "cp"]:
            if argv[-2].startswith("remote:") and argv[-2].endswith("receipt.json"):
                Path(argv[-1]).write_text(json.dumps(receipt), encoding="utf-8")
            return _result()
        if argv[:2] == ["codespace", "ssh"]:
            joined = " ".join(argv)
            if "creation.log" in joined:
                return _result(stdout="Finished configuring codespace.\n")
            if "runner-handback.json" in joined:
                return _result(stdout=json.dumps(_REPORT))
            return _result()
        raise AssertionError(f"unexpected fake gh call: {argv}")

    d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", "hi"],
                     invoker=fake, batch="B1")

    handback_reads = [
        call for call in calls
        if call[:2] == ["codespace", "ssh"] and "handback" in " ".join(call).lower()
    ]
    assert handback_reads, "exec did not read the runner handback"
    assert all("runner-handback.json" in " ".join(call) for call in handback_reads)
    assert all("handback.json" not in _remote_command(call).replace(
        "runner-handback.json", "") for call in handback_reads)


def test_harvest_copies_and_verifies_the_session_file(tmp_path):
    checkout = "/workspaces/repo"
    session_path = f"{checkout}/to-browser/SESSION-lane-x.md"
    payload = b"session evidence\n"
    digest = hashlib.sha256(payload).hexdigest()
    transport = tmp_path / "transport"
    transport.mkdir()

    def fake(argv, timeout=None, **_kw):
        joined = " ".join(argv)
        if session_path in joined and "sha256sum" in joined:
            return _result(stdout=f"{len(payload)}\n{digest}  {session_path}\n")
        if session_path in joined:
            return _result(stdout=payload.decode("utf-8"))
        return _result(ok=False, exit_code=1)

    result = d.codespace_harvest(
        "box-1", batch="B1", lane="lane-x", workdir="/workspaces/dispatch",
        out_root=tmp_path / "out", checkout_dir=checkout, transport_dir=transport,
        invoker=fake,
    )

    assert result.ok, result.failure
    out_file = result.out_dir / "SESSION-lane-x.md"
    transport_file = transport / "SESSION-lane-x.md"
    assert out_file.read_bytes() == payload
    assert transport_file.read_bytes() == payload
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["files"]["SESSION-lane-x.md"] == hashlib.sha256(
        transport_file.read_bytes()
    ).hexdigest()


def test_harvest_removes_session_file_if_remote_hash_is_wrong(tmp_path):
    checkout = "/workspaces/repo"
    session_path = f"{checkout}/to-browser/SESSION-lane-x.md"
    payload = b"session evidence\n"
    transport = tmp_path / "transport"
    transport.mkdir()

    def fake(argv, timeout=None, **_kw):
        joined = " ".join(argv)
        if session_path in joined and "sha256sum" in joined:
            return _result(stdout=f"{len(payload)}\n{'0' * 64}  {session_path}\n")
        if session_path in joined:
            return _result(stdout=payload.decode("utf-8"))
        return _result(ok=False, exit_code=1)

    result = d.codespace_harvest(
        "box-1", batch="B1", lane="lane-x", workdir="/workspaces/dispatch",
        out_root=tmp_path / "out", checkout_dir=checkout, transport_dir=transport,
        invoker=fake,
    )

    assert not result.ok
    assert "sha256" in result.failure.lower()
    assert not list(transport.iterdir())


def test_harvest_refuses_an_empty_manifest(tmp_path):
    result = d.codespace_harvest(
        "box-1", batch="B1", lane="lane-x", out_root=tmp_path,
        invoker=lambda _argv, timeout=None, **_kw: _result(ok=False, exit_code=1),
    )
    assert not result.ok
    assert result.failure


def _harvest_run_log(tmp_path):
    def fake(argv, timeout=None, **_kw):
        if "run.log" in " ".join(argv):
            return _result(stdout="clean\n")
        return _result(ok=False, exit_code=1)

    return d.codespace_harvest("box-1", batch="B1", lane="lane-x",
                               out_root=tmp_path / "out", invoker=fake)


def _open_regime_row(ledger: Path):
    now = datetime.now(timezone.utc)
    regime.write_receipt(
        "lane-x", "B1", "box-1", created=now - timedelta(minutes=5), deleted=None,
        machine="standardLinux32gb", prebuild=False, tokens={}, ledger_path=ledger,
    )


def test_successful_delete_closes_the_codespace_ledger_row(tmp_path):
    ledger = tmp_path / "CODESPACE-RECEIPTS.jsonl"
    _open_regime_row(ledger)
    harvested = _harvest_run_log(tmp_path)
    assert harvested.ok, harvested.failure

    result = d.codespace_delete(
        "box-1", out_dir=harvested.out_dir, batch="B1", lane="lane-x",
        receipts_root=tmp_path / "out", ledger_path=ledger,
        invoker=lambda _argv, timeout=None, **_kw: _result(),
    )

    assert result.ok, result
    rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    closed = [row for row in rows if row["codespace"] == "box-1"][-1]
    assert closed["deleted"] is not None
    assert closed["open"] is False
    assert closed["end_reason"]


def test_failed_delete_does_not_close_the_codespace_ledger_row(tmp_path):
    ledger = tmp_path / "CODESPACE-RECEIPTS.jsonl"
    _open_regime_row(ledger)
    harvested = _harvest_run_log(tmp_path)
    assert harvested.ok, harvested.failure

    result = d.codespace_delete(
        "box-1", out_dir=harvested.out_dir, batch="B1", lane="lane-x",
        receipts_root=tmp_path / "out", ledger_path=ledger,
        invoker=lambda _argv, timeout=None, **_kw: _result(ok=False, exit_code=1),
    )

    assert not result.ok
    rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    assert not any(row["codespace"] == "box-1" and not row["open"] for row in rows)


def test_remote_ssh_commands_are_single_quoted_argv_elements(tmp_path):
    workdir = "/workspaces/dis patch"
    checkout = "/workspaces/repo"
    session_path = f"{checkout}/to-browser/SESSION-lane-x.md"
    session_bytes = b"session file\n"
    session_hash = hashlib.sha256(session_bytes).hexdigest()
    run_log_path = f"{workdir}/run.log"
    run_log_bytes = b"run log\n"
    run_log_hash = hashlib.sha256(run_log_bytes).hexdigest()
    calls: list[list[str]] = []
    transport = tmp_path / "transport"
    transport.mkdir()
    stage = tmp_path / "stage"
    stage.mkdir()

    def fake(argv, timeout=None, **_kw):
        argv = list(argv)
        calls.append(argv)
        joined = " ".join(argv)
        if argv[:2] == ["codespace", "cp"]:
            source = argv[-2]
            if source.startswith("remote:") and source.endswith("SESSION-lane-x.md"):
                Path(argv[-1]).write_bytes(session_bytes)
            elif source.startswith("remote:") and source.endswith("/run.log"):
                Path(argv[-1]).write_bytes(run_log_bytes)
            elif source.startswith("remote:") and source.endswith("receipt.json"):
                Path(argv[-1]).write_text(
                    json.dumps({"exit_code": 0, "is_error": False, "status": "success"}),
                    encoding="utf-8",
                )
            return _result()
        if session_path in joined and "sha256sum" in joined:
            return _result(stdout=f"{len(session_bytes)}\n{session_hash}  {session_path}\n")
        if run_log_path in joined and "sha256sum" in joined:
            return _result(stdout=f"{len(run_log_bytes)}\n{run_log_hash}  {run_log_path}\n")
        if session_path in joined:
            return _result(stdout=session_bytes.decode("utf-8"))
        if run_log_path in joined:
            return _result(stdout=run_log_bytes.decode("utf-8"))
        if "creation.log" in joined:
            return _result(stdout="Finished configuring codespace.\n")
        if argv[:2] == ["codespace", "create"]:
            return _result(stdout="box-1\n")
        return _result()

    d.codespace_harvest(
        "box-1", batch="B1", lane="lane-x", workdir=workdir,
        out_root=tmp_path / "out", checkout_dir=checkout, transport_dir=transport,
        invoker=fake,
    )
    delivered = d.deliver_to_transport(
        "box-1", lane="lane-x", workdir=workdir, checkout_dir=checkout,
        transport_dir=transport, stage_dir=stage, invoker=fake,
    )
    assert delivered.ok, delivered

    contract = tmp_path / "LANE-x.md"
    contract.write_text("# contract\n", encoding="utf-8")
    d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", "hi"],
                     invoker=fake, batch="B1")

    ssh_calls = [call for call in calls if call[:2] == ["codespace", "ssh"]]
    assert ssh_calls
    for call in ssh_calls:
        assert len(call[call.index("--") + 1:]) == 1
        words = shlex.split(_remote_command(call))
        assert words
    parsed = [shlex.split(_remote_command(call)) for call in ssh_calls]
    assert any(words[:2] == ["sh", "-c"] and "sha256sum" in " ".join(words)
               for words in parsed), "delivery did not issue its remote size/hash probe"
    assert any(words[0] == "mkdir" for words in parsed), "exec did not issue its remote mkdir"
    assert any(words[0] == "bash" for words in parsed), "exec did not launch the runner"
    cat_calls = [
        call for call in ssh_calls
        if shlex.split(_remote_command(call))[:1] == ["cat"]
        and "run.log" in _remote_command(call)
    ]
    assert cat_calls
    assert shlex.split(_remote_command(cat_calls[0])) == [
        "cat", f"{workdir}/run.log",
    ]


def test_creation_log_waits_through_long_builds_and_is_bounded():
    sleeps: list[float] = []
    reads = 0

    def delayed_call(_argv, timeout=None, **_kw):
        nonlocal reads
        reads += 1
        if reads <= 12:
            return _result(stdout="Building container...\n")
        return _result(stdout="Finished configuring codespace.\n")

    refusal = d._creation_log_refusal("box-1", delayed_call, sleeps.append)
    assert refusal == ""
    assert reads > 12

    bound = getattr(d, "CREATION_LOG_WAIT_BOUND_S", None)
    assert isinstance(bound, int) and 600 <= bound <= 1800

    elapsed = 0.0
    never_finishes_reads = 0

    def unfinished_call(_argv, timeout=None, **_kw):
        nonlocal never_finishes_reads
        never_finishes_reads += 1
        return _result(stdout="Building container...\n")

    def virtual_sleep(seconds):
        nonlocal elapsed
        elapsed += seconds

    reason = d._creation_log_refusal("box-1", unfinished_call, virtual_sleep)
    assert reason
    assert elapsed <= 1800


def test_claude_background_plan_passes_disallowed_tools_as_one_token():
    prompt = "Keep this prompt as the final argument"
    argv = d.build_plan("anthropic", "opus", "lane-x", "high", prompt).argv

    assert "--disallowedTools=AskUserQuestion" in argv
    assert argv.index("--disallowedTools=AskUserQuestion") < len(argv) - 1
    assert argv[-1] == prompt
