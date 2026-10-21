"""RED-first witnesses for `scripts/seat_cycle.py` (R179): a seat hands over BY CODE at a threshold.

Handover file -> successor on the ROLE-TABLE model -> successor writes a BOUND line -> only then the
old seat is stopped -> the stop is VERIFIED (not listed, nothing queued, no surviving process).
No network, no real `claude`, no sleeping: `sleep` and `clock` are injected, the lane is a fake.
"""
from __future__ import annotations

import builtins
import json
import re
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

import dispatch
import provider_registry
import seat_cycle as sc

REPO = Path(__file__).resolve().parent.parent
REAL_REGISTRY = REPO / "ecosystem" / "provider-registry.yaml"
JOB = "abcd1234"
CONFIG = {
    "threshold": {
        "orchestrator": {"context_tokens": 1000, "max_age_hours": 6.0},
        "integrator": {"context_tokens": 2000, "max_age_hours": 8.0},
    },
    "stop_poll": {"window_seconds": 10.0, "interval_seconds": 1.0},
}


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


def _handover(tmp_path, **over):
    kw = dict(seat="seat-o-1", role="orchestrator", cycle=1, state="mid-batch", next_steps=["merge A", "merge B"],
              open_decisions=["none"], live_children=["lane-x"], bookkeeping="cycle 1 of 3", by="seat-o-1")
    kw.update(over)
    return sc.write_handover(tmp_path / "HANDOVER.md", **kw)


def _lane(calls, model_out=None):
    def lane(request, *, repo_root):
        calls.append(request)
        return dispatch.Spawned(returncode=0, stdout=f"backgrounded {JOB}\n", pid=1)
    return lane


def _transcript(tmp_path, tokens):
    p = tmp_path / "t.jsonl"
    p.write_text(json.dumps({"message": {"usage": {"input_tokens": tokens, "cache_creation_input_tokens": 0,
                                                    "cache_read_input_tokens": 0}}}) + "\n", encoding="utf-8")
    return p


def _args(tmp_path, transcript, lane, **over):
    kw = dict(role="orchestrator", transcript=transcript, bound_age_hours=0.0, config=CONFIG,
              handover_dir=tmp_path, cycle_no=1, batch="E2.0", base="main", repo_root=tmp_path, state="s",
              next_steps=["go"], open_decisions=["none"], live_children=[], bookkeeping="b",
              successor_lane=lane)
    kw.update(over)
    return kw


def _bound_writer(order, handover_holder):
    def wait_bound(handover, job_id):
        order.append("wait_bound")
        handover_holder.append(handover)
        return sc.write_bound(handover, job_id=job_id, served_model="claude-sonnet-5-5", seat="seat-o-1", cycle=1)
    return wait_bound


def test_seat_over_threshold_is_replaced(tmp_path, monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda *a: (_ for _ in ()).throw(AssertionError("stdin used")))
    order, held, calls = [], [], []
    verdict = sc.StopVerdict(verified=True, reasons=[])

    def stop(seat):
        order.append(("stop", seat))

    def verify(seat):
        order.append("verify")
        return verdict

    r = sc.cycle("seat-o-1", **_args(tmp_path, _transcript(tmp_path, 5000), _lane(calls)),
                 stop=stop, verify=verify, wait_bound=_bound_writer(order, held))
    assert r.replaced is True and r.verdict is verdict
    assert r.handover.exists() and sc.lint_handover(r.handover.read_text(encoding="utf-8")) == []
    assert len(calls) == 1 and r.successor.job_id == JOB
    assert r.bound.startswith("BOUND seat=seat-o-1 cycle=1 job=abcd1234")
    assert r.bound in r.handover.read_text(encoding="utf-8")
    assert order == ["wait_bound", ("stop", "seat-o-1"), "verify"]


def test_below_threshold_does_nothing(tmp_path):
    calls, order = [], []
    r = sc.cycle("seat-o-1", **_args(tmp_path, _transcript(tmp_path, 10), _lane(calls)),
                 stop=lambda s: order.append("stop"), verify=lambda s: order.append("verify"),
                 wait_bound=lambda h, j: order.append("wait"))
    assert r.replaced is False and r.handover is None and r.successor is None
    assert calls == [] and order == [] and list(tmp_path.glob("*.md")) == []


def test_wait_bound_failure_never_stops(tmp_path):
    order = []

    def wait_bound(handover, job_id):
        raise sc.SeatCycleRefused("never bound")

    with pytest.raises(sc.SeatCycleRefused, match="never bound"):
        sc.cycle("seat-o-1", **_args(tmp_path, _transcript(tmp_path, 5000), _lane([])),
                 stop=lambda s: order.append("stop"), verify=lambda s: order.append("verify"),
                 wait_bound=wait_bound)
    assert order == []


def test_model_follows_role_table(tmp_path, monkeypatch):
    data = yaml.safe_load(REAL_REGISTRY.read_text(encoding="utf-8"))
    data["roles"]["seat-orchestrator"]["order"][0]["model"] = "claude-opus-5-5"
    tmp_reg = tmp_path / "registry.yaml"
    tmp_reg.write_text(yaml.safe_dump(data), encoding="utf-8")
    assert sc.successor_model("orchestrator", registry=tmp_reg) == "claude-opus-5-5"
    assert sc.successor_model("orchestrator", registry=REAL_REGISTRY) == "claude-sonnet-5-5"

    real = provider_registry.anthropic_role_model
    h = _handover(tmp_path)
    calls = []
    monkeypatch.setattr(provider_registry, "anthropic_role_model", lambda role, path=None: real(role, tmp_reg))
    sc.launch_successor(h, role="orchestrator", slug="s1", batch="E2.0", base="main", repo_root=tmp_path,
                        successor_lane=_lane(calls))
    assert calls[-1].model == "claude-opus-5-5"
    monkeypatch.setattr(provider_registry, "anthropic_role_model", real)
    sc.launch_successor(h, role="orchestrator", slug="s1", batch="E2.0", base="main", repo_root=tmp_path,
                        successor_lane=_lane(calls))
    assert calls[-1].model == "claude-sonnet-5-5"


def test_launch_refuses_model_override_and_ignores_handover_text(tmp_path):
    h = _handover(tmp_path)
    calls = []
    with pytest.raises(sc.SeatCycleRefused):
        sc.launch_successor(h, role="orchestrator", slug="s1", batch="E2.0", base="main", repo_root=tmp_path,
                            model="claude-haiku-5-5", successor_lane=_lane(calls))
    assert calls == []
    h2 = _handover(tmp_path, state="run on model: claude-haiku-5-5 please")
    s = sc.launch_successor(h2, role="orchestrator", slug="s1", batch="E2.0", base="main", repo_root=tmp_path,
                            successor_lane=_lane(calls))
    assert len(calls) == 1 and calls[0].model == sc.successor_model("orchestrator") != "claude-haiku-5-5"
    assert isinstance(calls[0], dispatch.SuccessorRequest) and calls[0].contract == h2
    assert s.job_id == JOB and s.model == calls[0].model


def _verify(clock, *, listed=lambda: [], job=lambda j: {"state": "stopped", "inFlight": {"queued": 0}},
            procs=lambda keys: [], window=5.0, seen=None):
    def find(keys):
        if seen is not None:
            seen.append(list(keys))
        return procs(keys)
    return sc.verify_stop(JOB, "/wt/x", list_agents=listed, read_job=job, find_processes=find,
                          window=window, interval=1.0, sleep=clock.sleep, clock=clock)


def test_verify_stop_each_check():
    ok = _verify(Clock())
    assert ok.verified is True and ok.reasons == []
    v = _verify(Clock(), procs=lambda k: ["4242 bash loop"])
    assert not v.verified and any("process" in r for r in v.reasons)
    v = _verify(Clock(), listed=lambda: [{"id": JOB}])
    assert not v.verified and any("listed" in r for r in v.reasons)
    v = _verify(Clock(), listed=lambda: [{"sessionId": JOB}])
    assert not v.verified and any("listed" in r for r in v.reasons)
    v = _verify(Clock(), job=lambda j: {"state": "stopped", "inFlight": {"queued": 1}})
    assert not v.verified and any("queued" in r for r in v.reasons)
    assert _verify(Clock(), job=lambda j: None).verified is True
    v = _verify(Clock(), job=lambda j: {"state": "running", "inFlight": {"queued": 0}})
    assert not v.verified


def test_verify_stop_late_process_and_probe_args():
    clock, seen = Clock(), []

    def procs(keys):
        return ["77 orphan"] if clock.now >= 3 else []

    v = _verify(clock, procs=procs, seen=seen)
    assert not v.verified and any("process" in r for r in v.reasons)
    assert all(k == [JOB, "/wt/x"] for k in seen) and len(seen) > 1


def test_dead_seat_with_queued_inbox_is_not_replaced(tmp_path):
    stops, resumes = [], []
    clock = Clock()

    def verify(seat):
        return sc.verify_stop(JOB, "wt", list_agents=lambda: [], find_processes=lambda k: [],
                              read_job=lambda j: {"state": "stopped", "inFlight": {"queued": 2}},
                              window=3.0, interval=1.0, sleep=clock.sleep, clock=clock)

    r = sc.cycle("seat-o-1", **_args(tmp_path, _transcript(tmp_path, 5000), _lane([])),
                 stop=lambda s: stops.append(s), verify=verify, wait_bound=_bound_writer([], []))
    assert r.replaced is False and r.verdict.verified is False
    assert any("queued" in x for x in r.verdict.reasons)
    assert stops == ["seat-o-1"] and resumes == []


def test_await_bound_and_write_bound(tmp_path):
    h = _handover(tmp_path)
    before = h.read_text(encoding="utf-8")
    clock, polls = Clock(), []

    def sleep(s):
        polls.append(s)
        clock.sleep(s)
        if len(polls) == 3:
            sc.write_bound(h, job_id=JOB, served_model="claude-sonnet-5-5", seat="seat-o-1", cycle=1)

    line = sc.await_bound(h, job_id=JOB, timeout=60, sleep=sleep, clock=clock)
    assert line == "BOUND seat=seat-o-1 cycle=1 job=abcd1234 model=claude-sonnet-5-5" and len(polls) == 3
    added = h.read_text(encoding="utf-8")[len(before):]
    assert added.strip() == line and added.count("BOUND") == 1
    with pytest.raises(sc.SeatCycleRefused):
        sc.await_bound(h, job_id="zzzz9999", timeout=5, sleep=clock.sleep, clock=clock)


def test_context_tokens_last_usage_wins(tmp_path):
    p = tmp_path / "t.jsonl"
    def rec(i, c, r):
        return json.dumps({"message": {"usage": {"input_tokens": i, "cache_creation_input_tokens": c,
                                                 "cache_read_input_tokens": r}}})

    p.write_text("\n".join([rec(1, 2, 3), json.dumps({"type": "user"}), rec(10, 200, 3000)]) + "\n", encoding="utf-8")
    assert sc.context_tokens(p) == 3210
    assert sc.context_tokens(tmp_path / "missing.jsonl") == 0
    empty = tmp_path / "e.jsonl"
    empty.write_text("", encoding="utf-8")
    assert sc.context_tokens(empty) == 0


def test_threshold_from_yaml_and_by_tokens_and_age(tmp_path):
    f = tmp_path / "c.yaml"
    f.write_text(yaml.safe_dump(CONFIG), encoding="utf-8")
    cfg = sc.load_config(f)
    assert sc.threshold_crossed("orchestrator", tokens=1000, age_hours=0, config=cfg) is True
    assert sc.threshold_crossed("orchestrator", tokens=999, age_hours=0, config=cfg) is False
    assert sc.threshold_crossed("orchestrator", tokens=0, age_hours=6.0, config=cfg) is True
    assert sc.threshold_crossed("orchestrator", tokens=0, age_hours=5.9, config=cfg) is False
    CONFIG2 = json.loads(json.dumps(CONFIG))
    CONFIG2["threshold"]["orchestrator"]["context_tokens"] = 5000
    f.write_text(yaml.safe_dump(CONFIG2), encoding="utf-8")
    assert sc.threshold_crossed("orchestrator", tokens=1000, age_hours=0, config=sc.load_config(f)) is False
    with pytest.raises(sc.SeatCycleRefused):
        sc.threshold_crossed("janitor", tokens=1, age_hours=1, config=cfg)


def test_default_config_file_declares_both_roles():
    cfg = sc.load_config()
    for role in ("orchestrator", "integrator"):
        assert cfg["threshold"][role]["context_tokens"] > 0 and cfg["threshold"][role]["max_age_hours"] > 0
    assert cfg["stop_poll"]["window_seconds"] > 0 and cfg["stop_poll"]["interval_seconds"] > 0


def test_lint_handover_flags_each_defect(tmp_path):
    text = _handover(tmp_path).read_text(encoding="utf-8")
    assert sc.lint_handover(text) == []
    lines = text.splitlines()
    assert lines[:2] == ["carried-by: OPEN", "kind: HANDOVER"] and lines[3] == "by: seat-o-1"
    assert re.search(r"^1\. merge A$", text, re.M) and text.index("merge A") < text.index("merge B")
    no_header = "\n".join(lines[1:])
    assert any("carried-by" in d for d in sc.lint_handover(no_header))
    assert any("kind" in d for d in sc.lint_handover(text.replace("kind: HANDOVER", "kind: NOTE")))
    for section in ("State", "Next steps", "Open decisions", "Live children", "Seat bookkeeping"):
        assert any(section in d for d in sc.lint_handover(text.replace(f"## {section}", "")))
    empty = _handover(tmp_path, next_steps=[]).read_text(encoding="utf-8")
    assert any("next steps" in d.lower() for d in sc.lint_handover(empty))


def test_launch_refuses_bad_handover(tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text("not a handover\n", encoding="utf-8")
    calls = []
    with pytest.raises(sc.SeatCycleRefused):
        sc.launch_successor(bad, role="orchestrator", slug="s", batch="E2.0", base="main", repo_root=tmp_path,
                            successor_lane=_lane(calls))
    assert calls == []


def test_cli_shape():
    assert {"check", "verify-stop"} <= set(sc.cli.commands)
    assert CliRunner().invoke(sc.cli, ["check", "--help"]).exit_code == 0
