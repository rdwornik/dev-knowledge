"""[#1535] the outer-loop phase adapter (`scripts/run_phase.py`) + receipt schema (`ecosystem/schema/phase_receipt.py`).

Done-when (1): a phase is a spawned process the harness OWNS -- stdin is DEVNULL, a fresh,
nonce-bound, schema-valid payload (or the root's exit, or the timeout) ends it, and on every
kill the whole process tree is verified dead (`survivors == ()`), never assumed. A payload
older than the spawn, with the wrong nonce, or failing its schema is never harvested.

Done-when (3): the PhaseReceipt is built ONLY by the harness. `vendor` is derived from argv and
`served_model` from the CLI's own record, so a receipt that forges either, or whose served model
does not fit the vendor family, is refused; its keys are a superset of the dodo `_RECEIPT_KEYS`.

RED-FIRST (ADR-108 §B): the modules under test do not exist when this file lands. They are
imported INSIDE tests/helpers so each test fails individually (ModuleNotFoundError at call
time) instead of erroring at collection.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

import psutil
import pytest
import yaml

_REPO = Path(__file__).resolve().parents[1]
_SCHEMA_FILE = _REPO / "ecosystem" / "schema" / "phase-receipt.schema.json"
_REGISTRY = _REPO / "ecosystem" / "provider-registry.yaml"
_HASH = hashlib.sha256(b"x").hexdigest()
_CLI_VENDORS = {"claude": "anthropic", "codex": "openai", "grok": "xai",
                "copilot": "copilot-enterprise"}


@pytest.fixture(autouse=True)
def _repo_cwd(monkeypatch):
    """The validator's default registry path is repo-relative; pin cwd to the repo root."""
    monkeypatch.chdir(_REPO)


def _rp():
    from scripts import run_phase
    return run_phase


def _pr():
    from ecosystem.schema import phase_receipt
    return phase_receipt


# --------------------------------------------------------------------------- fake vendors

_VENDOR = r'''
import json, os, subprocess, sys, time
pid_file, mode = sys.argv[1], sys.argv[2]
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
with open(pid_file, "w") as fh:
    fh.write(str(child.pid))
payload = {"nonce": os.environ["PHASE_NONCE"], "input_hash": os.environ["PHASE_INPUT_HASH"],
           "outcome": "PASS", "detail": "fake vendor"}
if mode == "wrong_nonce":
    payload["nonce"] = "wrongnonce0000000"
elif mode == "extra_key":
    payload["bogus"] = 1
if mode in ("payload", "wrong_nonce", "extra_key"):
    target = os.environ["PHASE_PAYLOAD"]
    with open(target + ".tmp", "w") as fh:
        json.dump(payload, fh)
    os.replace(target + ".tmp", target)
time.sleep(600)
'''


def _vendor_argv(tmp_path: Path, mode: str) -> tuple[list[str], Path]:
    script = tmp_path / "fake_vendor.py"
    script.write_text(_VENDOR, encoding="utf-8")
    pid_file = tmp_path / "grandchild.pid"
    return [sys.executable, str(script), str(pid_file), mode], pid_file


def _pid_alive(pid: int) -> bool:
    try:
        return psutil.pid_exists(pid) and psutil.Process(pid).status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


def _gone(pid: int, wait_s: float = 10.0) -> bool:
    deadline = time.monotonic() + wait_s
    while _pid_alive(pid):
        if time.monotonic() > deadline:
            return False
        time.sleep(0.1)
    return True


def _reap(pid_file: Path) -> None:
    """No leftovers: kill the 600 s grandchild even if the assertion under test failed."""
    try:
        pid = int(pid_file.read_text())
        psutil.Process(pid).kill()
    except (OSError, ValueError, psutil.Error):
        pass


def _run_vendor(tmp_path: Path, mode: str, *, timeout_s: float = 3, contract: bool = True,
                nonce: str | None = None, input_hash: str = _HASH):
    """Run the never-exiting fake vendor; return (PhaseRun, grandchild pid, payload path)."""
    rp = _rp()
    argv, pid_file = _vendor_argv(tmp_path, mode)
    payload_path = tmp_path / "payload.json"
    kwargs = {}
    if contract:
        kwargs = {"payload_path": payload_path, "nonce": nonce or rp.new_nonce(),
                  "input_hash": input_hash}
    try:
        run = rp.run_phase(argv, timeout_s, poll_s=0.1, stdout_path=tmp_path / "out.txt", **kwargs)
        assert pid_file.exists(), "the fake vendor never reported its grandchild pid"
        return run, int(pid_file.read_text()), payload_path
    finally:
        _reap(pid_file)


# --------------------------------------------------------------------------- run_phase

def test_timeout_kills_tree_status_killed_no_survivor(tmp_path):
    """No payload contract: a never-exiting vendor is KILLED at timeout and its grandchild dies."""
    run, pid, _ = _run_vendor(tmp_path, "none", contract=False)
    assert run.status == "KILLED"
    assert run.killed is True and run.exit_code is None
    assert run.survivors == ()
    assert pid in run.targeted, "the kill must have targeted the grandchild"
    assert _gone(pid), "grandchild survived the tree kill"


def test_fresh_valid_payload_completes_and_kills_never_exiting_vendor(tmp_path):
    """A fresh nonce-bound payload from a vendor that never exits -> COMPLETE, killed, exit None."""
    run, pid, _ = _run_vendor(tmp_path, "payload", timeout_s=8)
    assert run.status == "COMPLETE", run.reason
    assert run.killed is True and run.exit_code is None
    assert run.payload is not None and run.payload["outcome"] == "PASS"
    assert run.payload_sha256 and len(run.payload_sha256) == 64
    assert run.survivors == ()
    assert _gone(pid), "grandchild survived the tree kill"


def test_no_payload_times_out_failed_and_tree_dead(tmp_path):
    """Payload contract, vendor writes nothing -> FAILED at timeout, tree dead."""
    run, pid, _ = _run_vendor(tmp_path, "none")
    assert run.status == "FAILED"
    assert "timeout" in run.reason
    assert run.killed is True and run.survivors == ()
    assert _gone(pid)


def test_stale_payload_written_before_spawn_is_not_harvested(tmp_path):
    """A payload with the right nonce but an mtime before the spawn never counts."""
    rp = _rp()
    nonce = rp.new_nonce()
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps({"nonce": nonce, "input_hash": _HASH, "outcome": "PASS"}),
                            encoding="utf-8")
    past = time.time() - 60
    os.utime(payload_path, (past, past))
    run, pid, _ = _run_vendor(tmp_path, "none", nonce=nonce)
    assert run.status == "FAILED", "a stale payload must not be harvested"
    assert run.payload is None
    assert _gone(pid)


def test_wrong_nonce_payload_is_not_harvested(tmp_path):
    """A fresh, schema-valid payload carrying the wrong nonce -> FAILED."""
    run, pid, _ = _run_vendor(tmp_path, "wrong_nonce")
    assert run.status == "FAILED"
    assert run.payload is None
    assert _gone(pid)


def test_schema_invalid_payload_extra_key_is_not_harvested(tmp_path):
    """A payload with an extra key fails the extra=forbid schema -> FAILED."""
    run, pid, _ = _run_vendor(tmp_path, "extra_key")
    assert run.status == "FAILED"
    assert run.payload is None
    assert _gone(pid)


def test_normal_exit_zero_is_ok(tmp_path):
    """No payload contract: exit 0 -> ok, nothing killed."""
    rp = _rp()
    run = rp.run_phase([sys.executable, "-c", "pass"], 30, poll_s=0.1)
    assert run.status == "ok" and run.exit_code == 0
    assert run.killed is False and run.targeted == () and run.survivors == ()
    assert run.started_at <= run.finished_at and run.duration_ms >= 0


def test_exit_three_is_failed_with_exit_code(tmp_path):
    """No payload contract: exit 3 -> FAILED and the code is recorded."""
    rp = _rp()
    run = rp.run_phase([sys.executable, "-c", "raise SystemExit(3)"], 30, poll_s=0.1)
    assert run.status == "FAILED" and run.exit_code == 3


def test_exit_with_no_payload_under_contract_is_failed(tmp_path):
    """Payload contract: a clean exit 0 with no fresh payload is still FAILED."""
    rp = _rp()
    run = rp.run_phase([sys.executable, "-c", "pass"], 30, poll_s=0.1,
                       payload_path=tmp_path / "payload.json", nonce=rp.new_nonce(),
                       input_hash=_HASH)
    assert run.status == "FAILED"
    assert "no fresh valid payload" in run.reason


def test_payload_contract_requires_nonce_and_input_hash(tmp_path):
    """payload_path without nonce/input_hash is a ValueError, nothing is spawned."""
    rp = _rp()
    with pytest.raises(ValueError):
        rp.run_phase([sys.executable, "-c", "pass"], 5, payload_path=tmp_path / "p.json")


def test_heartbeat_file_written(tmp_path):
    """heartbeat_path receives {pid, elapsed_s, payload_present, at} at spawn."""
    rp = _rp()
    beat = tmp_path / "beat.json"
    rp.run_phase([sys.executable, "-c", "import time; time.sleep(1)"], 30, poll_s=0.1,
                 heartbeat_path=beat, heartbeat_s=0.5)
    data = json.loads(beat.read_text(encoding="utf-8"))
    assert {"pid", "elapsed_s", "payload_present", "at"} <= set(data)


def test_new_nonce_is_32_hex_and_unique():
    """new_nonce is secrets.token_hex(16): 32 hex chars, never repeated."""
    rp = _rp()
    first, second = rp.new_nonce(), rp.new_nonce()
    assert first != second
    assert len(first) == 32 and int(first, 16) >= 0


def test_fresh_payload_accepts_only_fresh_matching_valid(tmp_path):
    """fresh_payload: valid -> model; stale / wrong nonce / wrong hash / garbage / missing -> None."""
    rp = _rp()
    path = tmp_path / "p.json"
    nonce = "abcdef0123456789"
    body = {"nonce": nonce, "input_hash": _HASH, "outcome": "PASS"}

    assert rp.fresh_payload(path, spawned_at=0.0, nonce=nonce, input_hash=_HASH) is None  # missing
    path.write_text("{not json", encoding="utf-8")
    assert rp.fresh_payload(path, spawned_at=0.0, nonce=nonce, input_hash=_HASH) is None  # garbage
    path.write_text(json.dumps(body), encoding="utf-8")
    got = rp.fresh_payload(path, spawned_at=time.time() - 30, nonce=nonce, input_hash=_HASH)
    assert got is not None and got.outcome == "PASS"
    assert rp.fresh_payload(path, spawned_at=time.time() + 30, nonce=nonce,
                            input_hash=_HASH) is None  # stale
    assert rp.fresh_payload(path, spawned_at=0.0, nonce="otherotherother1",
                            input_hash=_HASH) is None  # wrong nonce
    assert rp.fresh_payload(path, spawned_at=0.0, nonce=nonce,
                            input_hash=hashlib.sha256(b"y").hexdigest()) is None  # wrong hash


# --------------------------------------------------------------------------- phase_receipt

def _payload_dict(**over):
    return {"nonce": "abcdef0123456789", "input_hash": _HASH, "outcome": "PASS", **over}


def _receipt_dict(**over):
    base = {
        "schema": "phase-receipt/1", "organ": "P1", "status": "ok", "exit_code": 0,
        "duration_ms": 5, "input_hash": _HASH, "model_requested": "claude-opus",
        "model_reported": "claude-opus-4", "command": ["claude", "-p", "go"],
        "finished_at": "2026-10-15T00:00:05Z", "row": "1535", "lane": "L", "phase": "P1",
        "round": 1, "vendor": "anthropic", "cli_version": None, "served_model": "claude-opus-4",
        "started_at": "2026-10-15T00:00:00Z", "inputs": [], "nonce": "abcdef0123456789",
        "usage": None, "payload_sha256": None, "payload": None, "substituted_from": None,
    }
    base.update(over)
    return base


def test_phase_payload_extra_key_refused():
    """PhasePayload is extra=forbid: an agent cannot smuggle a field in."""
    pr = _pr()
    pr.PhasePayload.model_validate(_payload_dict())
    with pytest.raises(Exception) as err:
        pr.PhasePayload.model_validate(_payload_dict(bogus=1))
    assert "bogus" in str(err.value)


def test_valid_receipt_accepted_and_dumps_by_alias():
    """A well-formed receipt validates and dumps its `schema` key by alias."""
    pr = _pr()
    receipt = pr.PhaseReceipt.model_validate(_receipt_dict())
    assert receipt.model_dump(by_alias=True)["schema"] == "phase-receipt/1"


def test_receipt_keys_superset_of_dodo_receipt_keys():
    """RECEIPT_KEYS == dodo._RECEIPT_KEYS (all ten) and a dumped receipt carries every one."""
    pr = _pr()
    from scripts import dodo
    assert set(pr.RECEIPT_KEYS) == set(dodo._RECEIPT_KEYS)
    assert len(set(pr.RECEIPT_KEYS)) == 10
    dumped = pr.PhaseReceipt.model_validate(_receipt_dict()).model_dump(by_alias=True)
    assert set(pr.RECEIPT_KEYS) <= set(dumped)


def test_forged_vendor_refused():
    """vendor must equal vendor_for_argv(command): a claude command cannot claim xai."""
    pr = _pr()
    with pytest.raises(Exception) as err:
        pr.PhaseReceipt.model_validate(
            _receipt_dict(vendor="xai", served_model=None, model_reported=None))
    assert "vendor" in str(err.value)


def test_served_model_not_equal_model_reported_refused():
    """served_model and model_reported are one fact: a mismatch is refused."""
    pr = _pr()
    with pytest.raises(Exception):
        pr.PhaseReceipt.model_validate(
            _receipt_dict(served_model="claude-opus-4", model_reported="claude-sonnet-4"))


def test_served_model_family_mismatch_refused():
    """An anthropic vendor cannot have served a gpt-* model."""
    pr = _pr()
    with pytest.raises(Exception):
        pr.PhaseReceipt.model_validate(
            _receipt_dict(served_model="gpt-5", model_reported="gpt-5"))


def test_local_vendor_must_have_no_served_model():
    """An unknown head maps to vendor local, whose served_model must be None."""
    pr = _pr()
    pr.PhaseReceipt.model_validate(_receipt_dict(
        command=["mytool"], vendor="local", served_model=None, model_reported=None))
    with pytest.raises(Exception):
        pr.PhaseReceipt.model_validate(_receipt_dict(
            command=["mytool"], vendor="local", served_model="claude-x", model_reported="claude-x"))


def test_complete_status_requires_payload():
    """status COMPLETE with no payload is refused."""
    pr = _pr()
    with pytest.raises(Exception):
        pr.PhaseReceipt.model_validate(_receipt_dict(status="COMPLETE"))


def test_payload_sha256_must_match_payload():
    """payload_sha256 must be the digest of the carried payload, and None without one."""
    pr = _pr()
    payload = pr.PhasePayload.model_validate(_payload_dict())
    good = pr.payload_sha256(payload)
    pr.PhaseReceipt.model_validate(_receipt_dict(
        status="COMPLETE", payload=payload.model_dump(), payload_sha256=good))
    with pytest.raises(Exception):
        pr.PhaseReceipt.model_validate(_receipt_dict(
            status="COMPLETE", payload=payload.model_dump(), payload_sha256=_HASH))
    with pytest.raises(Exception):
        pr.PhaseReceipt.model_validate(_receipt_dict(payload_sha256=good))


def test_vendor_for_argv_maps_head_and_defaults_to_local():
    """Head basename, lower-cased, extension stripped, mapped; unknown -> local."""
    pr = _pr()
    assert pr.vendor_for_argv(["claude", "-p"], _CLI_VENDORS) == "anthropic"
    assert pr.vendor_for_argv(["/opt/bin/Codex.EXE", "exec"], _CLI_VENDORS) == "openai"
    assert pr.vendor_for_argv(["grok"], _CLI_VENDORS) == "xai"
    assert pr.vendor_for_argv(["copilot.cmd"], _CLI_VENDORS) == "copilot-enterprise"
    assert pr.vendor_for_argv(["mytool"], _CLI_VENDORS) == "local"


def test_load_cli_vendors_reads_real_registry():
    """The real registry maps cli -> provider key, skipping null cli."""
    pr = _pr()
    got = pr.load_cli_vendors(_REGISTRY)
    assert got["claude"] == "anthropic" and got["codex"] == "openai"
    assert got["copilot"] == "copilot-enterprise" and got["grok"] == "xai"
    assert "gemini" not in got and got["agy"] == "antigravity"
    assert None not in got


def test_served_model_from_record_per_cli():
    """claude -> biggest-output modelUsage key; codex/grok -> model; copilot -> currentModel."""
    pr = _pr()
    usage = {"modelUsage": {"claude-small": {"outputTokens": 5},
                            "claude-big": {"outputTokens": 500}}}
    assert pr.served_model_from_record("claude", usage) == "claude-big"
    assert pr.served_model_from_record("claude", {"modelUsage": {"claude-only": {}}}) == "claude-only"
    assert pr.served_model_from_record("codex", {"model": "gpt-5"}) == "gpt-5"
    assert pr.served_model_from_record("grok", {"model": "grok-4"}) == "grok-4"
    assert pr.served_model_from_record("copilot", {"currentModel": "gpt-5"}) == "gpt-5"
    assert pr.served_model_from_record("gemini", {"model": "gemini-3"}) is None
    assert pr.served_model_from_record("claude", None) is None
    assert pr.served_model_from_record("codex", {}) is None


def _phase_run(status="ok", payload=None, sha=None):
    rp = _rp()
    return rp.PhaseRun(status=status, exit_code=0, killed=False, targeted=(), survivors=(),
                       started_at="2026-10-15T00:00:00Z", finished_at="2026-10-15T00:00:05Z",
                       duration_ms=5, payload=payload, payload_sha256=sha, reason="done")


def _build(argv, run, record, **over):
    return _rp().build_receipt(
        run, organ="P1", row="1535", lane="L", phase="P1", round_no=1, argv=argv,
        input_hash=_HASH, nonce="abcdef0123456789", inputs=[], model_requested="m",
        cli_record=record, cli_vendors=_CLI_VENDORS, **over)


def test_build_receipt_derives_vendor_and_served_model_from_argv_and_record():
    """claude argv -> anthropic + served model from the record; unknown head -> local, None."""
    record = {"modelUsage": {"claude-small": {"outputTokens": 1},
                             "claude-big": {"outputTokens": 9}}}
    receipt = _build(["claude", "-p", "go"], _phase_run(), record)
    assert receipt.vendor == "anthropic"
    assert receipt.served_model == "claude-big" and receipt.model_reported == "claude-big"
    local = _build(["mytool.exe", "--x"], _phase_run(), None)
    assert local.vendor == "local" and local.served_model is None


def test_build_receipt_revalidates_payload_and_computes_sha():
    """The payload is re-validated into PhasePayload and its sha256 computed by the schema module."""
    pr = _pr()
    payload = _payload_dict()
    receipt = _build(["codex", "exec"], _phase_run("COMPLETE", payload, "0" * 64),
                     {"model": "gpt-5"})
    assert receipt.payload is not None and receipt.payload.outcome == "PASS"
    assert receipt.payload_sha256 == pr.payload_sha256(pr.PhasePayload.model_validate(payload))
    assert receipt.vendor == "openai" and receipt.served_model == "gpt-5"


def test_generated_schema_file_matches_render_and_check_passes():
    """phase-receipt.schema.json is the generated PhaseReceipt schema; --check exits 0."""
    pr = _pr()
    assert _SCHEMA_FILE.exists(), "ecosystem/schema/phase-receipt.schema.json is not generated"
    on_disk = _SCHEMA_FILE.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert on_disk == pr.render_json_schema().replace("\r\n", "\n")
    assert pr.main(["--check"]) == 0


# --------------------------------------------------------------------------- round-2 RED (reviewer terra)

def test_fresh_payload_refuses_mtime_equal_to_spawned_at(tmp_path):
    """The contract is mtime strictly AFTER the spawn: mtime == spawned_at is not fresh."""
    rp = _rp()
    path = tmp_path / "p.json"
    nonce = "abcdef0123456789"
    path.write_text(json.dumps({"nonce": nonce, "input_hash": _HASH, "outcome": "PASS"}),
                    encoding="utf-8")
    mtime = path.stat().st_mtime
    assert rp.fresh_payload(path, spawned_at=mtime, nonce=nonce, input_hash=_HASH) is None
    got = rp.fresh_payload(path, spawned_at=mtime - 1, nonce=nonce, input_hash=_HASH)
    assert got is not None and got.outcome == "PASS"


def test_receipt_refuses_a_payload_whose_nonce_differs_from_the_receipt_nonce():
    """The carried payload is bound to the receipt: a swapped-in payload nonce is refused even
    when payload_sha256 is recomputed for the swapped payload."""
    from pydantic import ValidationError
    pr = _pr()
    swapped = pr.PhasePayload.model_validate(_payload_dict(nonce="zzzzzzzzzzzzzzzz"))
    with pytest.raises(ValidationError):
        pr.PhaseReceipt.model_validate(_receipt_dict(
            status="COMPLETE", nonce="abcdef0123456789", payload=swapped.model_dump(),
            payload_sha256=pr.payload_sha256(swapped)))


def test_receipt_refuses_a_payload_whose_input_hash_differs_from_the_receipt_input_hash():
    """Same binding for input_hash: a payload carrying another input's hash is refused even
    when payload_sha256 is recomputed for the swapped payload."""
    from pydantic import ValidationError
    pr = _pr()
    other = hashlib.sha256(b"other-input").hexdigest()
    swapped = pr.PhasePayload.model_validate(_payload_dict(input_hash=other))
    with pytest.raises(ValidationError):
        pr.PhaseReceipt.model_validate(_receipt_dict(
            status="COMPLETE", input_hash=_HASH, payload=swapped.model_dump(),
            payload_sha256=pr.payload_sha256(swapped)))


# --- applied premise from lane L4 (codespace-finish), witnessed live 2026-10-15 -----------------
# The Claude API answers HTTP 400 to a `claude -p --json-schema` whose TOP LEVEL carries
# allOf / anyOf / oneOf (the lane-report schema failed that way). Such rules stay in pydantic
# validation; no schema this lane can hand a CLI may carry one at its top level.

_COMBINATORS = ("allOf", "anyOf", "oneOf")


def test_no_schema_the_adapter_can_emit_has_a_top_level_combinator(capsys):
    """Every model schema, every committed *.schema.json of the lane, and the `--payload-schema`
    output (what `claude -p --json-schema` would receive) is combinator-free at its top level."""
    from ecosystem.schema import challenge_receipt, distill_receipt
    pr = _pr()
    schemas = {name: model.model_json_schema(by_alias=True) for name, model in (
        ("PhasePayload", pr.PhasePayload), ("PhaseReceipt", pr.PhaseReceipt),
        ("DistillReceipt", distill_receipt.DistillReceipt),
        ("ChallengeReceipt", challenge_receipt.ChallengeReceipt),
        ("ChallengePayload", challenge_receipt.ChallengePayload))}
    for stem in ("phase-receipt", "distill-receipt", "challenge-receipt"):
        path = _REPO / "ecosystem" / "schema" / f"{stem}.schema.json"
        schemas[path.name] = json.loads(path.read_text(encoding="utf-8"))
    assert pr.main(["--payload-schema"]) == 0
    schemas["--payload-schema"] = json.loads(capsys.readouterr().out)
    offenders = {name: [k for k in _COMBINATORS if k in s] for name, s in schemas.items()}
    assert not {n: ks for n, ks in offenders.items() if ks}, offenders


# --- served-model capture ----------------------------------------------------------------------

def _fake_cli_bin(tmp_path: Path, monkeypatch) -> Path:
    """Put fake claude/copilot launchers on PATH, including Windows .cmd shims."""
    bindir = tmp_path / "fake-bin"
    bindir.mkdir()
    helper = tmp_path / "fake_cli.py"
    helper.write_text(
        """\
import json
import sys
from pathlib import Path

vendor, *args = sys.argv[1:]
if vendor == "claude":
    print(json.dumps({"result": "ok", "modelUsage": {"claude-haiku-5-5": {"outputTokens": 3}}}))
    print("claude stderr noise", file=sys.stderr)
else:
    if "--usage-output-file" in args:
        usage_path = Path(args[args.index("--usage-output-file") + 1])
        usage_path.parent.mkdir(parents=True, exist_ok=True)
        usage_path.write_text(json.dumps({"currentModel": "gpt-6-luna"}), encoding="utf-8")
    print("ok")
""",
        encoding="utf-8",
    )
    for vendor in ("claude", "copilot"):
        if os.name == "nt":
            shim = bindir / f"{vendor}.cmd"
            shim.write_text(
                f'@"{sys.executable}" "{helper}" {vendor} %*\r\n',
                encoding="utf-8",
            )
        else:
            shim = bindir / vendor
            shim.write_text(
                f'#!/bin/sh\nexec "{sys.executable}" "{helper}" {vendor} "$@"\n',
                encoding="utf-8",
            )
            shim.chmod(0o755)
    monkeypatch.setenv("PATH", str(bindir) + os.pathsep + os.environ.get("PATH", ""))
    return bindir


def test_run_phase_sends_stderr_to_default_sidecar(tmp_path):
    """With a stdout file and no stderr path, stderr is kept in the .stderr sidecar."""
    rp = _rp()
    stdout = tmp_path / "phase.json"
    stderr = Path(str(stdout) + ".stderr")
    script = "import sys; print('out'); print('noise', file=sys.stderr)"

    run = rp.run_phase([sys.executable, "-c", script], 10, stdout_path=stdout)

    assert run.status == "ok"
    assert stdout.read_text(encoding="utf-8").strip() == "out"
    assert stderr.read_text(encoding="utf-8").strip() == "noise"


def test_cli_run_writes_claude_json_and_requested_and_served_models(tmp_path, monkeypatch):
    """claude stdout is pure JSON, stderr is separate, and the receipt records both models."""
    _fake_cli_bin(tmp_path, monkeypatch)
    rp = _rp()
    requested = "claude-sonnet-5-5"
    stdout = tmp_path / "claude.stdout.json"
    stderr = tmp_path / "claude.stderr"
    receipt = tmp_path / "claude.receipt.json"

    result = rp.main([
        "run", "--receipt", str(receipt), "--organ", "test", "--timeout", "10",
        "--stdout", str(stdout), "--stderr", str(stderr), "--",
        "claude", "--model", requested,
    ])

    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert result == 0
    assert json.loads(stdout.read_text(encoding="utf-8"))["result"] == "ok"
    assert "claude stderr noise" in stderr.read_text(encoding="utf-8")
    assert data["model_requested"] == requested
    assert data["served_model"] == data["model_reported"] == "claude-haiku-5-5"


def test_cli_run_reads_copilot_usage_record_and_defaults_stderr_path(tmp_path, monkeypatch):
    """copilot currentModel comes from its usage file and model_requested comes from --model."""
    _fake_cli_bin(tmp_path, monkeypatch)
    rp = _rp()
    requested = "claude-sonnet-5.5"
    stdout = tmp_path / "copilot.stdout.txt"
    usage = tmp_path / "copilot.usage.json"
    receipt = tmp_path / "copilot.receipt.json"

    result = rp.main([
        "run", "--receipt", str(receipt), "--organ", "test", "--timeout", "10",
        "--stdout", str(stdout), "--",
        "copilot", "-p", "--model", requested, "--usage-output-file", str(usage),
    ])

    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert result == 0
    assert stdout.read_text(encoding="utf-8").strip() == "ok"
    assert json.loads(usage.read_text(encoding="utf-8")) == {"currentModel": "gpt-6-luna"}
    assert data["model_requested"] == requested
    assert data["served_model"] == data["model_reported"] == "gpt-6-luna"
    assert Path(str(stdout) + ".stderr").is_file()


def test_harness_copilot_phases_declare_round_usage_files():
    """P3 and P5 capture Copilot usage at a round-local .usage.json path."""
    harness = yaml.safe_load((_REPO / "ecosystem" / "harness.yaml").read_text(encoding="utf-8"))
    phases = {phase["id"]: phase for phase in harness["phases"]}

    for phase_id in ("P3", "P5"):
        command = phases[phase_id]["command"]
        usage_arg = command.index("--usage-output-file")
        usage_path = command[usage_arg + 1]
        assert usage_path.endswith(".usage.json")
        assert "{round_dir}" in usage_path


def test_phase_task_records_copilot_served_model(tmp_path, monkeypatch):
    """A P3-style phase task records currentModel from the Copilot usage output file."""
    _fake_cli_bin(tmp_path, monkeypatch)
    rp = _rp()
    requested = "claude-sonnet-5.5"
    phase = {
        "id": "P3", "name": "implement", "timeout_s": 10, "gate": "exit",
        "model": requested,
        "command": ["copilot", "-p", "--model", requested, "--usage-output-file",
                    "{round_dir}/P3.usage.json"],
    }
    task = next(rp.phase_tasks(
        [phase], {"{receipts}": str(tmp_path / "receipts"), "{lane}": "toy"},
        lambda tokens: tokens, lambda paths: {}, tmp_path,
    ))

    assert task["actions"][0]() is True
    data = json.loads(Path(task["targets"][0]).read_text(encoding="utf-8"))
    assert data["model_requested"] == requested
    assert data["served_model"] == data["model_reported"] == "gpt-6-luna"
