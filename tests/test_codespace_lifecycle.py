"""RED-FIRST witnesses for the delivery gate and the handback lifecycle in `scripts/dispatch.py`.

Doctrine: the box is deleted only after what the browser will read has landed in the transport
directory, byte-identical to the box source. Every test drives the `invoker` seam; no real `gh`.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

import codespace_regime as regime
import dispatch as d

LANE = "lane-x"
REPO = "rdwornik/.dev-knowledge"
CHECKOUT = "/workspaces/.dev-knowledge"
WORKDIR = "/workspaces/dispatch"
SESSION_SRC = f"{CHECKOUT}/to-browser/SESSION-{LANE}.md"
LOG_SRC = f"{WORKDIR}/run.log"
SESSION_NAME = f"SESSION-{LANE}.md"
LOG_NAME = f"{LANE}-run.log"
SESSION_BYTES = ("# Session\n\nÉtat é — ✓\n" * 3).encode("utf-8")
LOG_BYTES = b"line one\nline two\n" * 20


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


class FakeBox:
    """A fake `gh` for one box: `files` maps box path -> true bytes; `cp_mode` mutates what `cp`
    delivers (truncate / empty / flip) so the box's own hash disagrees with the staged copy."""

    def __init__(self, name="box-1", files=None, cp_mode=None, list_keeps_name=False, delete_ok=True):
        self.name = name
        self.files = dict(files if files is not None else {SESSION_SRC: SESSION_BYTES, LOG_SRC: LOG_BYTES})
        self.cp_mode = cp_mode or {}
        self.list_keeps_name = list_keeps_name
        self.delete_ok = delete_ok
        self.deleted = False
        self.calls: list[list[str]] = []
        self.kwargs: list[dict] = []

    def __call__(self, argv, **kw):
        argv = list(argv)
        self.calls.append(argv)
        self.kwargs.append(kw)
        verb = argv[:2]
        if verb == ["codespace", "cp"]:
            src = argv[-2].removeprefix("remote:")
            if src not in self.files:
                return d.GhResult(ok=False, exit_code=1, stdout="no such file")
            data = self.files[src]
            mode = self.cp_mode.get(src)
            if mode == "truncate":
                data = data[:40]
            elif mode == "empty":
                data = b""
            elif mode == "flip":
                data = bytes([data[0] ^ 0xFF]) + data[1:]
            Path(argv[-1]).write_bytes(data)
            return d.GhResult(ok=True, exit_code=0, stdout="")
        if verb == ["codespace", "ssh"]:
            command = argv[-1]
            for src, data in self.files.items():
                if src in command and ("sha256sum" in command or "wc" in command):
                    return d.GhResult(ok=True, exit_code=0,
                                      stdout=f"{len(data)}\n{hashlib.sha256(data).hexdigest()}  {src}\n")
            return d.GhResult(ok=True, exit_code=0, stdout="")
        if verb == ["codespace", "delete"]:
            if self.delete_ok:
                self.deleted = True
            return d.GhResult(ok=self.delete_ok, exit_code=0 if self.delete_ok else 1, stdout="")
        if verb == ["codespace", "list"]:
            alive = (not self.deleted) or self.list_keeps_name
            return d.GhResult(ok=True, exit_code=0, stdout=json.dumps([{"name": self.name}] if alive else []))
        raise AssertionError(f"unexpected gh call: {argv}")

    def delete_calls(self):
        return [c for c in self.calls if c[:2] == ["codespace", "delete"]]


def _deliver(box, tmp_path, transport=None):
    transport_dir = tmp_path / "to-browser" if transport is None else transport
    if transport is None:
        transport_dir.mkdir(exist_ok=True)
    stage = tmp_path / "stage"
    stage.mkdir(exist_ok=True)
    return d.deliver_to_transport(box.name, lane=LANE, workdir=WORKDIR, checkout_dir=CHECKOUT,
                                  transport_dir=transport_dir, stage_dir=stage, invoker=box)


# ------------------------------------------------------------------ deliver_to_transport

def test_a_clean_delivery_lands_both_files_byte_identical(tmp_path):
    box = FakeBox()
    result = _deliver(box, tmp_path)
    assert result.ok, result.reason
    assert (tmp_path / "to-browser" / SESSION_NAME).read_bytes() == SESSION_BYTES
    assert (tmp_path / "to-browser" / LOG_NAME).read_bytes() == LOG_BYTES
    assert set(result.delivered) == {SESSION_NAME, LOG_NAME}


def test_the_cp_argv_is_exactly_the_specified_shape(tmp_path):
    box = FakeBox()
    _deliver(box, tmp_path)
    stage = tmp_path / "stage"
    cps = [c for c in box.calls if c[:2] == ["codespace", "cp"]]
    assert ["codespace", "cp", "-c", "box-1", "-e", f"remote:{SESSION_SRC}", str(stage / SESSION_NAME)] in cps
    assert ["codespace", "cp", "-c", "box-1", "-e", f"remote:{LOG_SRC}", str(stage / LOG_NAME)] in cps


def test_the_box_is_asked_for_bytes_and_hash_over_ssh_sh_c(tmp_path):
    box = FakeBox()
    _deliver(box, tmp_path)
    ssh = [c for c in box.calls if c[:2] == ["codespace", "ssh"]]
    assert ssh
    for call in ssh:
        assert call[2:5] == ["-c", "box-1", "--"] and call[5:7] == ["sh", "-c"]
        assert "sha256sum" in call[-1] and "wc -c" in call[-1]


def test_the_recorded_hashes_match_the_source_bytes(tmp_path):
    result = _deliver(FakeBox(), tmp_path)
    assert result.delivered[SESSION_NAME] == hashlib.sha256(SESSION_BYTES).hexdigest()
    assert result.delivered[LOG_NAME] == hashlib.sha256(LOG_BYTES).hexdigest()
    assert result.commands


def test_the_delivery_carries_no_credential_and_no_stdin(tmp_path):
    box = FakeBox()
    _deliver(box, tmp_path)
    for argv in box.calls:
        joined = " ".join(argv)
        for needle in ("token", "GH_TOKEN", "ghp_", "gho_"):
            assert needle not in joined, (needle, argv)
    assert all("input_bytes" not in kw for kw in box.kwargs)


def test_a_missing_box_source_is_refused_naming_the_file(tmp_path):
    box = FakeBox(files={LOG_SRC: LOG_BYTES})
    result = _deliver(box, tmp_path)
    assert not result.ok
    assert SESSION_NAME in result.reason


def test_a_missing_transport_dir_is_refused_naming_transport(tmp_path):
    result = _deliver(FakeBox(), tmp_path, transport=tmp_path / "no" / "such" / "dir")
    assert not result.ok
    assert "transport" in result.reason


def test_an_unwritable_transport_is_refused_naming_transport(tmp_path):
    blocker = tmp_path / "a-file"
    blocker.write_text("x", encoding="utf-8")
    result = _deliver(FakeBox(), tmp_path, transport=blocker)
    assert not result.ok
    assert "transport" in result.reason


def test_non_ascii_session_text_round_trips_byte_identically(tmp_path):
    text = "é — ✓ session\n".encode("utf-8")
    box = FakeBox(files={SESSION_SRC: text, LOG_SRC: LOG_BYTES})
    result = _deliver(box, tmp_path)
    assert result.ok, result.reason
    assert (tmp_path / "to-browser" / SESSION_NAME).read_bytes() == text
    assert result.delivered[SESSION_NAME] == hashlib.sha256(text).hexdigest()


# ------------------------------------------------------------------ mutation witnesses

def test_a_truncated_delivery_is_refused_with_a_size_reason(tmp_path):
    big = b"x" * 100
    box = FakeBox(files={SESSION_SRC: big, LOG_SRC: LOG_BYTES}, cp_mode={SESSION_SRC: "truncate"})
    result = _deliver(box, tmp_path)
    assert not result.ok
    assert SESSION_NAME in result.reason and "size" in result.reason


def test_an_empty_delivery_is_refused_with_an_empty_reason(tmp_path):
    box = FakeBox(cp_mode={SESSION_SRC: "empty"})
    result = _deliver(box, tmp_path)
    assert not result.ok
    assert SESSION_NAME in result.reason and "empty" in result.reason


def test_a_bit_flipped_delivery_is_refused_with_a_sha256_reason(tmp_path):
    box = FakeBox(cp_mode={LOG_SRC: "flip"})
    result = _deliver(box, tmp_path)
    assert not result.ok
    assert LOG_NAME in result.reason and "sha256" in result.reason


# ------------------------------------------------------------------ codespace_handback

@pytest.fixture
def handback_env(tmp_path, monkeypatch):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    ledger = tmp_path / "ledger.jsonl"
    monkeypatch.setattr(
        d, "codespace_harvest",
        lambda name, **k: d.HarvestResult(True, name=name, out_dir=out_dir, manifest_path=out_dir / "m.json"))
    monkeypatch.setattr(d, "verify_harvest_manifest", lambda *a, **k: d.HarvestVerdict(True, "ok"))
    transport = tmp_path / "to-browser"
    transport.mkdir()
    return {"transport_dir": transport, "out_root": tmp_path / "out-root", "receipts_root": tmp_path / "rr",
            "ledger_path": ledger}


def _handback(box, env, **over):
    kw = dict(batch="B1", lane=LANE, repo=REPO, workdir=WORKDIR, invoker=box, **env)
    kw.update(over)
    return d.codespace_handback(box.name, **kw)


def test_a_good_handback_runs_the_four_steps_in_order_and_deletes(handback_env):
    box = FakeBox()
    result = _handback(box, handback_env)
    assert result.ok, result.reason
    assert result.deleted is True
    assert result.steps == ("harvest", "deliver", "delete", "verify-teardown")
    assert len(box.delete_calls()) == 1


def test_the_teardown_check_lists_json_names(handback_env):
    box = FakeBox()
    _handback(box, handback_env)
    assert ["codespace", "list", "--json", "name"] in box.calls


def test_the_delivery_uses_the_checkout_named_by_the_repo_basename(handback_env):
    box = FakeBox()
    _handback(box, handback_env)
    assert any(f"remote:{SESSION_SRC}" in c for c in box.calls)


@pytest.mark.parametrize("mode,src", [("truncate", SESSION_SRC), ("empty", SESSION_SRC), ("flip", LOG_SRC)])
def test_a_bad_delivery_never_issues_a_delete(handback_env, mode, src):
    box = FakeBox(files={SESSION_SRC: b"x" * 100, LOG_SRC: LOG_BYTES}, cp_mode={src: mode})
    result = _handback(box, handback_env)
    assert not result.ok and result.deleted is False
    assert result.reason
    assert box.delete_calls() == []
    assert "delete" not in result.steps


def test_an_unreachable_transport_never_issues_a_delete(handback_env):
    box = FakeBox()
    result = _handback(box, dict(handback_env, transport_dir=handback_env["transport_dir"] / "gone"))
    assert not result.ok and result.deleted is False
    assert result.reason
    assert box.delete_calls() == []


def test_a_box_still_listed_after_delete_is_a_failure_naming_still_listed(handback_env):
    box = FakeBox(list_keeps_name=True)
    result = _handback(box, handback_env)
    assert not result.ok
    assert "still listed" in result.reason


# ------------------------------------------------------------------ codespace_lifecycle

def test_lifecycle_runs_exec_then_handback_when_exec_names_a_box(tmp_path, monkeypatch):
    order = []
    monkeypatch.setattr(d, "codespace_exec",
                        lambda *a, **k: (order.append("exec"), d.ExecResult(True, name="box-1"))[1])

    def handback(name, **k):
        order.append(("handback", name))
        return d.LifecycleResult(True, True, "", ("harvest", "deliver", "delete", "verify-teardown"))

    monkeypatch.setattr(d, "codespace_handback", handback)
    result = d.codespace_lifecycle(REPO, "main", LANE, tmp_path / "c.md", ["claude"], batch="B1",
                                   transport_dir=tmp_path, out_root=tmp_path, receipts_root=tmp_path,
                                   ledger_path=tmp_path / "l.jsonl", invoker=lambda a, **k: None)
    assert order == ["exec", ("handback", "box-1")]
    assert result.ok
    assert result.steps[0] == "exec"


def test_lifecycle_still_hands_back_a_box_whose_exec_failed(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(d, "codespace_exec",
                        lambda *a, **k: d.ExecResult(False, name="box-1", failure="runner failed"))
    monkeypatch.setattr(d, "codespace_handback",
                        lambda name, **k: (calls.append(name),
                                           d.LifecycleResult(True, True, "", ("harvest",)))[1])
    result = d.codespace_lifecycle(REPO, "main", LANE, tmp_path / "c.md", ["claude"], batch="B1",
                                   transport_dir=tmp_path, out_root=tmp_path, receipts_root=tmp_path,
                                   ledger_path=tmp_path / "l.jsonl", invoker=lambda a, **k: None)
    assert calls == ["box-1"]
    assert not result.ok


def test_lifecycle_without_a_box_name_runs_no_handback(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(d, "codespace_exec", lambda *a, **k: d.ExecResult(False, failure="create failed"))
    monkeypatch.setattr(d, "codespace_handback", lambda name, **k: calls.append(name))
    result = d.codespace_lifecycle(REPO, "main", LANE, tmp_path / "c.md", ["claude"], batch="B1",
                                   transport_dir=tmp_path, out_root=tmp_path, receipts_root=tmp_path,
                                   ledger_path=tmp_path / "l.jsonl", invoker=lambda a, **k: None)
    assert calls == []
    assert not result.ok


# ------------------------------------------------------------------ CLI

def test_codespace_harvest_help_mentions_transport_dir():
    result = CliRunner().invoke(d.cli, ["codespace-harvest", "--help"])
    assert result.exit_code == 0
    assert "--transport-dir" in result.output
