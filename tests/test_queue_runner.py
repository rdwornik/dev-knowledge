"""RED-first acceptance tests for the one-shot queue runner."""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

import gen_process_diagrams as gpd
import pytest

REPO = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures" / "queue_runner"
EXPECTED_QUEUE_LINES = [
    "[queue-runner] would-fire queue a (handback)",
    "[queue-runner] would-fire queue a (merged)",
    "[queue-runner] would-fire repair b (attempt 1)",
]


def _runner():
    return importlib.import_module("queue_runner")


def _contracts():
    return [FIXTURES / "LANE-a.md", FIXTURES / "LANE-b.md"]


def _event_tree(tmp_path, *, state="", files=None):
    transport = tmp_path / "transport"
    to_browser = transport / "to-browser"
    to_browser.mkdir(parents=True)
    for name, text in (files or {}).items():
        (to_browser / name).write_text(text, encoding="utf-8")
    state_file = tmp_path / "SESSION-integrator.md"
    state_file.write_text(state, encoding="utf-8")
    return transport, state_file


def _run_arguments(tmp_path, transport, state_file, *, ledger_path=None):
    return {
        "batch": "E3.0",
        "state_file": state_file,
        "transport": transport,
        "contracts": _contracts(),
        "ledger_path": ledger_path or tmp_path / "QUEUE-RUNNER-E3.0.jsonl",
    }


def _successful_fire(qr, calls):
    def fire(argv, env):
        calls.append((list(argv), dict(env)))
        return qr.FireResult(returncode=0, output="")

    return fire


def test_collect_events_reads_sources_in_contract_order_and_keeps_keys_unique():
    qr = _runner()
    events = qr.collect_events(
        transport=FIXTURES / "transport",
        state_file=FIXTURES / "SESSION-integrator.md",
        slugs=("a", "b"),
    )

    assert [(event.kind, event.lane) for event in events] == [
        ("handback", "a"),
        ("merged", "a"),
        ("refused", "b"),
    ]
    assert len({event.key for event in events}) == len(events)
    assert [event.source for event in events] == [
        "SESSION-a.md",
        "SESSION-integrator.md",
        "REFUSED-b.md",
    ]


def test_collect_events_ignores_non_events_and_lanes_outside_the_contracts(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path,
        state=(
            "STATE a REFUSED - 2026-11-01T10:00 0\n"
            "STATE a WAITING - 2026-11-01T10:01 0\n"
            "STATE a REPORTED - 2026-11-01T10:02 0\n"
            "STATE other MERGED abc1234 2026-11-01T10:03 1\n"
        ),
        files={
            "SESSION-a.md": (
                "    HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"
                "`HANDBACK worktree-a @ 2222222222222222222222222222222222222222 code`\n"
            ),
            "SESSION-other.md": "HANDBACK worktree-other @ abc code\n",
            "HANDBACK-REFUSED-a.md": "from: the INTEGRATOR\nrepair 1 of 2\n",
            "REFUSED-a.md": "repair 1 of 2\n",
            "REFUSED-b.md": "from: the DISPATCHER\nrepair 1 of 2\n",
            "REFUSED-a-repair.md": "from: the INTEGRATOR\n",
        },
    )

    assert qr.collect_events(
        transport=transport,
        state_file=state_file,
        slugs=("a", "b"),
    ) == []


def test_event_keys_change_when_the_event_text_changes(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path,
        files={
            "SESSION-a.md": (
                "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"
                "HANDBACK worktree-a @ 2222222222222222222222222222222222222222 code\n"
            )
        },
    )
    events = qr.collect_events(transport=transport, state_file=state_file, slugs=("a",))

    assert len(events) == 2
    assert events[0].key != events[1].key


def test_collect_events_accepts_handbacks_from_repair_sessions(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path,
        files={
            "SESSION-a.md": "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n",
            "SESSION-a-repair-2.md": (
                "HANDBACK worktree-a-repair-2 @ 2222222222222222222222222222222222222222 code\n"
            ),
        },
    )

    events = qr.collect_events(transport=transport, state_file=state_file, slugs=("a",))

    assert [event.source for event in events] == [
        "SESSION-a-repair-2.md",
        "SESSION-a.md",
    ]


def test_run_once_fires_exact_queue_and_repair_arguments_only_once(tmp_path):
    qr = _runner()
    transport = FIXTURES / "transport"
    state_file = FIXTURES / "SESSION-integrator.md"
    ledger_path = tmp_path / "ledger.jsonl"
    calls = []

    fired = qr.run_once(
        **_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
        fire=_successful_fire(qr, calls),
    )

    queue_argv = [
        "queue",
        "--batch",
        "E3.0",
        "--state-file",
        str(state_file),
        str(_contracts()[0]),
        str(_contracts()[1]),
    ]
    repair_argv = [
        "repair",
        "b",
        str(_contracts()[1]),
        "--model",
        "claude-sonnet-5-5",
        "--effort",
        "high",
        "--attempt",
        "1",
        "--batch",
        "E3.0",
    ]
    assert [item.argv for item in fired] == [queue_argv, queue_argv, repair_argv]
    assert [(item.verb, item.lane, item.kind) for item in fired] == [
        ("queue", "a", "handback"),
        ("queue", "a", "merged"),
        ("repair", "b", "refused"),
    ]
    assert [call[0] for call in calls] == [queue_argv, queue_argv, repair_argv]


def test_restart_does_not_refire_events_already_recorded(tmp_path):
    qr = _runner()
    transport = FIXTURES / "transport"
    state_file = FIXTURES / "SESSION-integrator.md"
    ledger_path = tmp_path / "ledger.jsonl"
    calls = []
    arguments = _run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path)

    qr.run_once(**arguments, fire=_successful_fire(qr, calls))
    after_first_run = len(calls)
    restarted = qr.Ledger(path=ledger_path)
    keys = [
        event.key
        for event in qr.collect_events(
            transport=transport,
            state_file=state_file,
            slugs=("a", "b"),
        )
    ]
    assert all(restarted.seen(key) for key in keys)

    qr.run_once(**arguments, fire=_successful_fire(qr, calls))

    assert after_first_run == 3
    assert len(calls) == after_first_run


def test_failed_fires_are_retried_at_most_three_times(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path,
        files={"SESSION-a.md": "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"},
    )
    ledger_path = tmp_path / "ledger.jsonl"
    calls = []

    def failing_fire(argv, env):
        calls.append(list(argv))
        return qr.FireResult(returncode=1, output="dispatch failed")

    for _ in range(4):
        qr.run_once(
            **_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
            fire=failing_fire,
        )

    assert len(calls) == 3


def test_dry_run_is_read_only_exact_and_does_not_suppress_live_fires(tmp_path):
    qr = _runner()
    transport = FIXTURES / "transport"
    state_file = FIXTURES / "SESSION-integrator.md"
    ledger_path = tmp_path / "ledger.jsonl"
    arguments = _run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path)
    lines = []

    qr.run_once(
        **arguments,
        fire=lambda *_args: pytest.fail("dry-run must not call fire"),
        dry_run=True,
        echo=lines.append,
    )
    assert lines == EXPECTED_QUEUE_LINES
    assert not ledger_path.exists()

    calls = []
    qr.run_once(**arguments, fire=_successful_fire(qr, calls))
    assert len(calls) == 3
    before_second_dry_run = ledger_path.read_bytes()

    lines.clear()
    qr.run_once(
        **arguments,
        fire=lambda *_args: pytest.fail("dry-run must not call fire"),
        dry_run=True,
        echo=lines.append,
    )
    assert lines == []
    assert ledger_path.read_bytes() == before_second_dry_run


@pytest.mark.parametrize(
    ("state", "files", "slug", "expected_state"),
    [
        (
            "",
            {"SESSION-a.md": "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"},
            "a",
            "integrating",
        ),
        ("STATE a MERGED abc1234 2026-11-01T10:00 5\n", {}, "a", "merged"),
        ("STATE a FAILED - 2026-11-01T10:00 5\n", {}, "a", "failed"),
        (
            "",
            {"REFUSED-b.md": "from: the INTEGRATOR\nrepair 1 of 2\n"},
            "b",
            "running",
        ),
    ],
)
def test_machine_resting_states_are_recorded(tmp_path, state, files, slug, expected_state):
    qr = _runner()
    transport, state_file = _event_tree(tmp_path, state=state, files=files)
    ledger_path = tmp_path / "ledger.jsonl"

    qr.run_once(
        **_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
        fire=_successful_fire(qr, []),
    )

    assert qr.Ledger(path=ledger_path).lane_state(slug) == expected_state


@pytest.mark.parametrize(
    ("initial", "second_event", "expected_state"),
    [("MERGED", "handback", "merged"), ("FAILED", "merged", "failed")],
)
def test_machine_refused_event_is_seen_and_not_fired(
    tmp_path, initial, second_event, expected_state
):
    qr = _runner()
    initial_line = f"STATE a {initial} abc1234 2026-11-01T10:00 5\n"
    transport, state_file = _event_tree(tmp_path, state=initial_line)
    ledger_path = tmp_path / "ledger.jsonl"
    qr.run_once(
        **_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
        fire=_successful_fire(qr, []),
    )
    if second_event == "handback":
        (transport / "to-browser" / "SESSION-a.md").write_text(
            "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n",
            encoding="utf-8",
        )
    else:
        with state_file.open("a", encoding="utf-8") as receipt:
            receipt.write("STATE a MERGED def5678 2026-11-01T10:05 1\n")
    calls = []
    qr.run_once(
        **_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
        fire=_successful_fire(qr, calls),
    )
    rows = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines()]

    assert qr.Ledger(path=ledger_path).lane_state("a") == expected_state
    assert calls == []
    assert any(row.get("status") == "machine-refused" for row in rows)


def test_repair_three_of_two_fails_without_firing(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path,
        files={"REFUSED-b.md": "from: the INTEGRATOR\nrepair 3 of 2\n"},
    )
    ledger_path = tmp_path / "ledger.jsonl"
    calls = []

    fired = qr.run_once(
        **_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
        fire=_successful_fire(qr, calls),
    )

    assert fired == []
    assert calls == []
    assert qr.Ledger(path=ledger_path).lane_state("b") == "failed"


def test_fire_environment_identifies_queue_runner(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path,
        files={"SESSION-a.md": "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"},
    )
    calls = []

    qr.run_once(
        **_run_arguments(tmp_path, transport, state_file),
        fire=_successful_fire(qr, calls),
    )

    assert qr.CALLER_ENV == "DISPATCH_CALLER"
    assert calls[0][1][qr.CALLER_ENV] == qr.CALLER_VALUE == "queue_runner"


def test_event_is_a_frozen_dataclass():
    qr = _runner()
    event = qr.Event(
        kind="handback",
        lane="a",
        key="event-key",
        attempt=None,
        source="SESSION-a.md",
        text="HANDBACK worktree-a @ sha code",
    )

    assert is_dataclass(event)
    with pytest.raises(FrozenInstanceError):
        event.kind = "merged"


def test_machine_is_the_process_diagrams_dispatch_machine():
    qr = _runner()

    assert qr.MACHINE is gpd.P1DispatchLane


def test_dispatcher_order_template_is_retired_at_its_carried_by_header():
    lines = (REPO / "templates" / "dispatcher-order-template.md").read_text(
        encoding="utf-8"
    ).splitlines()
    header_line = next(i for i, line in enumerate(lines) if line.startswith("carried-by:"))

    assert lines[header_line].startswith("carried-by: RETIRED")
    assert "RETIRED (R130, [#1633])" in "\n".join(lines[:header_line])


def test_integrator_order_template_does_not_name_a_queue_call():
    text = (REPO / "templates" / "integrator-order-template.md").read_text(encoding="utf-8")

    assert "dispatch.py queue" not in text
    assert "queue --watch" not in text


def test_cli_witness_prints_the_three_expected_dry_run_events():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/queue_runner.py",
            "watch",
            "--once",
            "--dry-run",
            "--batch",
            "E3.0",
            "--state-file",
            str(FIXTURES / "SESSION-integrator.md"),
            "--transport",
            str(FIXTURES / "transport"),
            "--contracts",
            str(FIXTURES / "LANE-a.md"),
            str(FIXTURES / "LANE-b.md"),
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert [
        line
        for line in result.stdout.splitlines()
        if line.startswith("[queue-runner] would-fire")
    ] == EXPECTED_QUEUE_LINES


def test_a_lane_the_queue_pass_fired_is_running_so_its_handback_is_legal(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path,
        files={"SESSION-a.md": "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"},
    )
    ledger_path = tmp_path / "ledger.jsonl"

    def fire(argv, env):
        return qr.FireResult(returncode=0, output="[queue] FIRE b: job abcd1234\n")

    qr.run_once(**_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path), fire=fire)

    assert qr.Ledger(path=ledger_path).lane_state("b") == "running"


def test_a_merge_for_a_lane_still_held_running_catches_the_lane_up_and_fires(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(tmp_path)
    ledger_path = tmp_path / "ledger.jsonl"
    qr_ledger_row = {"key": "fire|x|a", "kind": "fire", "lane": "a", "status": "observed",
                     "state_after": "running"}
    ledger_path.write_text(json.dumps(qr_ledger_row) + "\n", encoding="utf-8")
    state_file.write_text("STATE a MERGED abc1234 2026-11-01T10:00 5\n", encoding="utf-8")
    calls = []

    qr.run_once(**_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
                fire=_successful_fire(qr, calls))

    assert len(calls) == 1
    assert qr.Ledger(path=ledger_path).lane_state("a") == "merged"


def test_a_failed_line_after_repair_three_of_two_still_fires_the_queue_pass(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path, files={"REFUSED-b.md": "from: the INTEGRATOR\nrepair 3 of 2\n"})
    ledger_path = tmp_path / "ledger.jsonl"
    qr.run_once(**_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
                fire=_successful_fire(qr, []))
    state_file.write_text("STATE b FAILED - 2026-11-01T10:00 5\n", encoding="utf-8")
    calls = []

    qr.run_once(**_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
                fire=_successful_fire(qr, calls))

    assert [call[0][0] for call in calls] == ["queue"]
    assert qr.Ledger(path=ledger_path).lane_state("b") == "failed"


def test_an_unwritable_ledger_does_not_end_the_pass(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path,
        files={"SESSION-a.md": "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"},
    )
    blocker = tmp_path / "a-file"
    blocker.write_text("x", encoding="utf-8")
    calls = []

    fired = qr.run_once(**_run_arguments(tmp_path, transport, state_file, ledger_path=blocker / "l.jsonl"),
                        fire=_successful_fire(qr, calls))

    assert len(fired) == len(calls) == 1


def test_main_rejects_an_interval_below_one_second(tmp_path):
    qr = _runner()
    with pytest.raises(SystemExit) as exit_info:
        qr.main(["watch", "--batch", "E3.0", "--state-file", str(tmp_path / "s.md"), "--transport",
                 str(tmp_path), "--contracts", str(_contracts()[0]), "--interval", "0", "--once"])
    assert exit_info.value.code == 2


def test_a_fire_that_raises_counts_as_a_failed_fire_and_the_cap_still_holds(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path,
        files={"SESSION-a.md": "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"},
    )
    ledger_path = tmp_path / "ledger.jsonl"
    calls = []

    def raising_fire(argv, env):
        calls.append(argv)
        raise OSError("the child never started")

    for _ in range(4):
        qr.run_once(**_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
                    fire=raising_fire)

    assert len(calls) == 3


def test_a_dry_run_of_a_machine_refused_event_prints_nothing_and_writes_nothing(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path, state="STATE a MERGED abc1234 2026-11-01T10:00 5\n",
        files={"SESSION-a.md": "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"})
    ledger_path = tmp_path / "ledger.jsonl"
    qr.run_once(**_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
                fire=_successful_fire(qr, []))
    before = ledger_path.read_bytes()
    (transport / "to-browser" / "SESSION-a.md").write_text(
        "HANDBACK worktree-a @ 2222222222222222222222222222222222222222 code\n", encoding="utf-8")
    lines = []

    fired = qr.run_once(**_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
                        fire=lambda *_a: pytest.fail("a dry run must not fire"), dry_run=True,
                        echo=lines.append)

    assert fired == [] and lines == []
    assert ledger_path.read_bytes() == before


def test_an_unwritable_ledger_does_not_refire_across_the_passes_of_one_watch(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path,
        files={"SESSION-a.md": "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"},
    )
    blocker = tmp_path / "a-file"
    blocker.write_text("x", encoding="utf-8")
    ledger = qr.Ledger(path=blocker / "l.jsonl")
    calls = []

    for _ in range(3):
        qr.run_once(**_run_arguments(tmp_path, transport, state_file, ledger_path=blocker / "l.jsonl"),
                    fire=_successful_fire(qr, calls), ledger=ledger)

    assert len(calls) == 1


def test_every_event_of_a_pass_is_seen_after_it_and_nothing_is_fired_twice(tmp_path):
    qr = _runner()
    transport, state_file = _event_tree(
        tmp_path, state="STATE a MERGED abc1234 2026-11-01T10:00 5\n",
        files={"SESSION-a.md": "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n",
               "REFUSED-b.md": "from: the INTEGRATOR\nrepair 3 of 2\n"})
    ledger_path = tmp_path / "ledger.jsonl"
    calls = []
    for _ in range(3):
        qr.run_once(**_run_arguments(tmp_path, transport, state_file, ledger_path=ledger_path),
                    fire=_successful_fire(qr, calls))

    events = qr.collect_events(transport=transport, state_file=state_file, slugs=("a", "b"))
    assert {event.kind for event in events} == {"handback", "merged", "refused"}
    ledger = qr.Ledger(path=ledger_path)
    assert all(ledger.seen(event.key) for event in events)
    assert [call[0][0] for call in calls] == ["queue", "queue"]    # handback + merge, once each; repair 3 of 2 fires nothing


def test_repair_sessions_sort_by_number_not_by_text(tmp_path):
    qr = _runner()
    line = "HANDBACK worktree-a @ 1111111111111111111111111111111111111111 code\n"
    transport, state_file = _event_tree(
        tmp_path, files={f"SESSION-a-repair-{n}.md": line for n in (10, 2, 1)})

    events = qr.collect_events(transport=transport, state_file=state_file, slugs=("a",))

    assert [event.source for event in events] == [
        "SESSION-a-repair-1.md", "SESSION-a-repair-2.md", "SESSION-a-repair-10.md"]
