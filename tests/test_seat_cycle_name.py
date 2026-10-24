import json
import re

import pytest

import dispatch
import seat_cycle as sc


CONFIG = {
    "threshold": {
        "orchestrator": {"context_tokens": 1000, "max_age_hours": 6.0, "effort": "medium"},
        "integrator": {"context_tokens": 1000, "max_age_hours": 6.0, "effort": "high"},
    },
    "stop_poll": {"window_seconds": 10.0, "interval_seconds": 1.0},
}
JOB = "abcd1234"
BATCH = "E2.1"


def _transcript(path):
    path.write_text(
        json.dumps({"message": {"usage": {"input_tokens": 5000}}}) + "\n",
        encoding="utf-8",
    )
    return path


def _lane(calls):
    def successor_lane(request, *, repo_root):
        calls.append(request)
        return dispatch.Spawned(returncode=0, stdout=f"backgrounded {JOB}\n", pid=1)

    return successor_lane


def _cycle(tmp_path, role, calls):
    return sc.cycle(
        "seat-predecessor-7",
        role=role,
        transcript=_transcript(tmp_path / "transcript.jsonl"),
        bound_age_hours=0.0,
        config=CONFIG,
        handover_dir=tmp_path,
        cycle_no=1,
        batch=BATCH,
        base="main",
        repo_root=tmp_path,
        state="mid-batch",
        next_steps=["continue work"],
        open_decisions=["none"],
        live_children=[],
        bookkeeping="cycle 1 of 3",
        successor_lane=_lane(calls),
        wait_bound=lambda handover, job_id: sc.write_bound(
            handover,
            job_id=job_id,
            served_model=sc.successor_model(role),
            seat="seat-predecessor-7",
            cycle=2,
        ),
        stop=lambda seat: None,
        verify=lambda seat: sc.StopVerdict(verified=True, reasons=[]),
    )


@pytest.mark.parametrize("role", ["orchestrator", "integrator"])
def test_cycle_uses_batch_role_and_next_cycle_for_successor_name(tmp_path, role):
    calls = []
    result = _cycle(tmp_path, role, calls)

    batch_slug = "-".join(re.findall(r"[a-z0-9]+", BATCH.lower()))
    expected = f"{role}-{batch_slug}-cycle-2"
    assert calls[0].slug == expected
    assert re.search(rf"--name {re.escape(expected)}(?:\s|$)", result.handover.read_text(encoding="utf-8"))
    assert dispatch._SLUG.fullmatch(calls[0].slug)


@pytest.mark.parametrize("role", ["orchestrator", "integrator"])
def test_cycle_handover_successor_name_round_trips_through_bind(tmp_path, role):
    calls = []
    result = _cycle(tmp_path, role, calls)
    name = calls[0].slug

    line = sc.bind_successor(
        result.handover,
        name=name,
        seat="seat-predecessor-7",
        cycle_no=2,
        list_agents=lambda: [{"name": name, "id": JOB, "sessionId": "session-1"}],
        find_transcript=lambda session_id: None,
    )

    assert line == f"BOUND seat=seat-predecessor-7 cycle=2 job={JOB} model=unknown"
    assert line in result.handover.read_text(encoding="utf-8")
