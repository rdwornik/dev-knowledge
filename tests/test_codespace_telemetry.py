"""RED-FIRST witnesses for the substrate / readiness / end telemetry on the receipts.

Covers `codespace_regime.write_receipt` + `mark_ready`, the `LAUNCH-<SLUG>.json` receipt, and the
`codespace_exec` / `codespace_delete` legs that stamp `ready` and `end`.
"""
from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import codespace_regime as regime
import dispatch as d

T0 = datetime(2026, 10, 19, 22, 9, 51, tzinfo=timezone.utc)
UNMEASURED_READY = "UNMEASURED: the box was not probed for readiness"
LOCAL_END_REASON = "UNMEASURED: the launcher exits when the lane starts; it cannot observe the lane's end"


@pytest.fixture(autouse=True)
def _private_receipt_homes(tmp_path_factory, monkeypatch):
    root = tmp_path_factory.mktemp("receipt-homes")
    monkeypatch.setattr(d, "DEFAULT_HARVEST_ROOT", root / "remote-runs")
    for mod in {id(m): m for m in (regime, d.regime, sys.modules.get("scripts.codespace_regime"),
                                   sys.modules.get("codespace_regime")) if m is not None}.values():
        monkeypatch.setattr(mod, "_REPO_ROOT", root / "repo")


@pytest.fixture(autouse=True)
def _pre_launch_cleared(monkeypatch):
    monkeypatch.setattr(d, "run_prelaunch", lambda *a, **k: d.PreLaunch(True))


def _rows(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


def _write(path, **kw):
    args = dict(slug="s", batch="B", codespace="c1", created=T0, deleted=None,
                machine="standardLinux32gb", prebuild=False, tokens={}, ledger_path=path,
                now=T0 + timedelta(minutes=5))
    args.update(kw)
    return regime.write_receipt(**args)


# ---------------------------------------------------------------- A. regime rows

def test_every_receipt_row_is_stamped_codespace_substrate(tmp_path):
    assert _write(tmp_path / "l.jsonl")["substrate"] == "codespace"


def test_an_unprobed_open_row_says_ready_is_unmeasured(tmp_path):
    row = _write(tmp_path / "l.jsonl")
    assert row["ready"] is None
    assert row["ready_reason"] == UNMEASURED_READY


def test_a_given_ready_stamp_is_carried_and_reason_defaults_empty(tmp_path):
    row = _write(tmp_path / "l.jsonl", ready=T0.isoformat(), )
    assert row["ready"] == T0.isoformat()
    assert row["ready_reason"] == ""


def test_an_explicit_ready_reason_is_kept_when_ready_is_none(tmp_path):
    row = _write(tmp_path / "l.jsonl", ready_reason="probe timed out")
    assert row["ready"] is None and row["ready_reason"] == "probe timed out"


def test_an_open_row_has_no_end_and_says_why(tmp_path):
    row = _write(tmp_path / "l.jsonl")
    assert row["end"] is None
    assert row["end_reason"] == "open: the box has not been deleted"


def test_a_closed_row_end_is_the_deleted_stamp_with_empty_reason(tmp_path):
    deleted = T0 + timedelta(minutes=35)
    row = _write(tmp_path / "l.jsonl", deleted=deleted)
    assert row["end"] == deleted.isoformat()
    assert row["end_reason"] == ""


def test_mark_ready_appends_an_open_copy_with_ready_set(tmp_path):
    path = tmp_path / "l.jsonl"
    _write(path)
    later = T0 + timedelta(minutes=2)
    row = regime.mark_ready("c1", ledger_path=path, now=later)
    assert row["ready"] == later.isoformat()
    assert row["open"] is True and row["codespace"] == "c1" and row["slug"] == "s"
    assert len(_rows(path)) == 2


def test_mark_ready_keeps_exactly_one_open_row_last_wins(tmp_path):
    path = tmp_path / "l.jsonl"
    _write(path)
    regime.mark_ready("c1", ledger_path=path, now=T0 + timedelta(minutes=2))
    opened = regime.open_receipts(path)
    assert [r["codespace"] for r in opened] == ["c1"]
    assert opened[0]["ready"] == (T0 + timedelta(minutes=2)).isoformat()


def test_mark_ready_for_an_unknown_codespace_returns_none_and_appends_nothing(tmp_path):
    path = tmp_path / "l.jsonl"
    _write(path)
    assert regime.mark_ready("ghost", ledger_path=path, now=T0) is None
    assert len(_rows(path)) == 1


def test_mark_ready_for_a_closed_codespace_returns_none(tmp_path):
    path = tmp_path / "l.jsonl"
    _write(path, deleted=T0 + timedelta(minutes=9))
    assert regime.mark_ready("c1", ledger_path=path, now=T0) is None
    assert len(_rows(path)) == 1


def test_old_shape_rows_are_still_read_by_open_receipts(tmp_path):
    path = tmp_path / "l.jsonl"
    old = {"kind": "codespace", "slug": "s", "batch": "B", "codespace": "c1",
           "machine": "basicLinux32gb", "created": T0.isoformat(), "deleted": None, "open": True,
           "uptime_minutes": 1.0}
    path.write_text(json.dumps(old) + "\n", encoding="utf-8")
    assert [r["codespace"] for r in regime.open_receipts(path)] == ["c1"]
    # and the new surface is exercised against it, so this is RED today
    assert regime.mark_ready("c1", ledger_path=path, now=T0)["ready"] == T0.isoformat()


# ---------------------------------------------------------------- B. launch receipt

class _FakeClaude:
    def __init__(self, interrupt=False):
        self.interrupt = interrupt

    def __call__(self, argv, env, cwd, log_path=None):
        if self.interrupt:
            raise KeyboardInterrupt
        return d.Spawned(returncode=0, stdout="backgrounded abcd1234\n", pid=4321)


_CONTRACT = """# LANE lane-launch-adapter -- a test contract

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Dispatch

```
claude --bg -n lane-launch-adapter --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-launch-adapter "Read and execute the frozen contract"
```

slug `lane-launch-adapter` -> branch `worktree-lane-launch-adapter`
"""


@pytest.fixture
def launch_receipts(tmp_path, monkeypatch):
    target = tmp_path / "launch-receipts"
    monkeypatch.setenv("HARNESS_RECEIPTS_DIR", str(target))
    return target


@pytest.fixture
def contract(tmp_path):
    path = tmp_path / "LANE-W3-B-launch-adapter.md"
    path.write_text(_CONTRACT, encoding="utf-8")
    return path


def _launch(contract, tmp_path, spawn):
    request = d.request_from_contract(contract)
    return d.launch_lane(request, prelaunch=lambda r: d.PreLaunch(passed=True, reason=""), spawn=spawn,
                         agents=lambda: [], cwd=tmp_path, sleep=lambda s: None)


def test_the_launch_receipt_is_substrate_local_with_an_unmeasured_end(contract, tmp_path, launch_receipts):
    try:
        _launch(contract, tmp_path, _FakeClaude())
    except d.LaunchIncomplete:
        pass
    receipt = json.loads((launch_receipts / "LAUNCH-LANE-LAUNCH-ADAPTER.json").read_text(encoding="utf-8"))
    assert receipt["substrate"] == "local"
    assert receipt["end"] is None
    assert receipt["end_reason"] == LOCAL_END_REASON


def test_the_intent_receipt_written_before_the_provider_starts_carries_the_same_fields(
        contract, tmp_path, launch_receipts):
    with pytest.raises(KeyboardInterrupt):
        _launch(contract, tmp_path, _FakeClaude(interrupt=True))
    receipt = json.loads((launch_receipts / "LAUNCH-LANE-LAUNCH-ADAPTER.json").read_text(encoding="utf-8"))
    assert receipt["job_id"] == "pending"
    assert receipt["substrate"] == "local"
    assert receipt["end"] is None
    assert receipt["end_reason"] == LOCAL_END_REASON


# ---------------------------------------------------------------- B. exec / delete

_REPORT = {"exit_code": 0, "is_error": False, "status": "success", "turns": 3,
           "result": "ok", "session_id": "s-1"}


class _Gh:
    def __init__(self, fail_mkdir=False, receipt=None):
        self.calls, self.fail_mkdir, self.receipt = [], fail_mkdir, receipt

    def __call__(self, argv, **kw):
        argv = list(argv)
        self.calls.append(argv)
        verb = " ".join(argv[:2])
        if verb == "codespace create":
            return d.GhResult(ok=True, exit_code=0, stdout="fluffy-space-1\n")
        if verb == "codespace cp":
            if argv[-2].startswith("remote:") and self.receipt is not None:
                Path(argv[-1]).write_text(json.dumps(self.receipt), encoding="utf-8")
            return d.GhResult(ok=True, exit_code=0, stdout="")
        if verb == "codespace ssh":
            if "mkdir" in argv and self.fail_mkdir:
                return d.GhResult(ok=False, exit_code=255, stdout="boom")
            if "creation.log" in " ".join(argv):
                return d.GhResult(ok=True, exit_code=0,
                                  stdout="[2026-10-05 08:04:02.884Z] Finished configuring codespace.\n")
            return d.GhResult(ok=True, exit_code=0, stdout="")
        return d.GhResult(ok=True, exit_code=0, stdout="")


def test_exec_marks_the_box_ready_after_the_first_ssh_succeeds(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# c\n", encoding="utf-8")
    ledger = tmp_path / "ledger.jsonl"
    d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", "hi"],
                     invoker=_Gh(receipt=copy.deepcopy(_REPORT)), batch="B1", ledger_path=ledger)
    opened = [r for r in regime.open_receipts(ledger) if r["codespace"] == "fluffy-space-1"]
    assert len(opened) == 1
    assert opened[0]["ready"], opened[0]
    assert opened[0]["ready_reason"] == ""


def test_exec_whose_ssh_fails_before_ready_leaves_it_unmeasured(tmp_path):
    contract = tmp_path / "LANE-x.md"
    contract.write_text("# c\n", encoding="utf-8")
    ledger = tmp_path / "ledger.jsonl"
    d.codespace_exec("me/repo", "main", "lane-x", contract, ["claude", "-p", "hi"],
                     invoker=_Gh(fail_mkdir=True), batch="B1", ledger_path=ledger)
    rows = [r for r in _rows(ledger) if r.get("codespace") == "fluffy-space-1"]
    assert rows, "the create row must exist"
    assert all(r["ready"] is None for r in rows)
    assert rows[-1]["ready_reason"] == UNMEASURED_READY


def test_delete_close_row_carries_ready_and_end(tmp_path, monkeypatch):
    ledger = tmp_path / "ledger.jsonl"
    _write(ledger, codespace="box-1", slug="lane-x", batch="B1", created=datetime.now(timezone.utc))
    ready = regime.mark_ready("box-1", ledger_path=ledger, now=datetime.now(timezone.utc))
    assert ready is not None
    monkeypatch.setattr(d, "verify_harvest_manifest", lambda *a, **k: d.HarvestVerdict(True, "ok"))
    res = d.codespace_delete("box-1", out_dir=tmp_path / "out", invoker=lambda argv, **k: d.GhResult(True, 0, ""),
                             batch="B1", lane="lane-x", receipts_root=tmp_path / "rr", ledger_path=ledger)
    assert res.ok
    closed = _rows(ledger)[-1]
    assert closed["open"] is False
    assert closed["ready"] == ready["ready"]
    assert closed["end"] == closed["deleted"]
    assert closed["end_reason"] == ""
