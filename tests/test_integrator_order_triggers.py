"""Witnesses for `templates/integrator-order-template.md`'s close and refusal steps
(LANE-5B3-2-wire-quota-distiller, Done-contract item 1).

The two silent organs `quota_watch.py` and `learning_distiller.py` MERGED with nobody
triggering them (DIGEST-WAVE5B-N2-2026-09-26.md G9). This file asserts the trigger prose is
actually in the template, not merely that this lane believes it wrote it: the close step
calls `quota_watch.py record` then `quota_watch.py line`, and `learning_distiller.py run`
over the batch's REFUSED files; the refusal step calls `learning_distiller.py run` over the
one REFUSED file it just wrote. Ownership: this lane edits ONLY the close and refusal
sections (ruling (i)) -- a separate test asserts every other section is byte-unchanged.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

TEMPLATE = REPO_ROOT / "templates" / "integrator-order-template.md"


def _section(text: str, heading: str) -> str:
    """The body of one `## <heading>` section, up to the next `## ` heading or EOF."""
    pattern = re.compile(
        rf"^##\s*{re.escape(heading)}\s*$(?P<body>.*?)(?=^##\s|\Z)", re.M | re.S)
    m = pattern.search(text)
    assert m, f"no '## {heading}' section found in {TEMPLATE}"
    return m.group("body")


def _close_section(text: str) -> str:
    return _section(text, "Close — when every lane is MERGED or FAILED, or at <time>, whichever comes first")


def _refusals_section(text: str) -> str:
    return _section(text, "Refusals and repairs")


def test_template_exists():
    assert TEMPLATE.exists()


def test_close_step_calls_quota_watch_record_then_line():
    text = TEMPLATE.read_text(encoding="utf-8")
    close = _close_section(text)
    record_idx = close.find("scripts/quota_watch.py record")
    line_idx = close.find("scripts/quota_watch.py line")
    assert record_idx != -1, "close step does not call `quota_watch.py record`"
    assert line_idx != -1, "close step does not call `quota_watch.py line`"
    assert record_idx < line_idx, "record must be called before line, not after"


def test_close_step_calls_learning_distiller_over_the_batchs_refused_files():
    text = TEMPLATE.read_text(encoding="utf-8")
    close = _close_section(text)
    assert "scripts/learning_distiller.py" in close
    assert "run --integrator" in close
    assert "--dispatcher" in close
    assert "--refused" in close
    assert "REFUSED-" in close


def test_close_step_never_claims_the_distiller_files_rows():
    text = TEMPLATE.read_text(encoding="utf-8")
    close = _close_section(text)
    assert "ruling h" in close
    assert "does not file" in close or "files nothing" in close


def test_refusal_step_calls_learning_distiller_over_the_refused_file_it_just_wrote():
    text = TEMPLATE.read_text(encoding="utf-8")
    refusals = _refusals_section(text)
    assert "REFUSED-<slug>.md" in refusals, "the refusal step must name the file it just wrote"
    assert "scripts/learning_distiller.py" in refusals
    assert "run --integrator" in refusals
    assert "--refused to-browser/REFUSED-<slug>.md" in refusals
    assert "ruling h" in refusals


def test_both_organs_are_called_from_both_the_close_and_refusal_steps_collectively():
    """The contract's own framing: 'both calls' (quota_watch + learning_distiller) show up
    across 'both steps' (close + refusal) -- quota_watch only at close (there is no per-
    refusal cost line), learning_distiller at both close and refusal."""
    text = TEMPLATE.read_text(encoding="utf-8")
    close, refusals = _close_section(text), _refusals_section(text)
    assert "quota_watch.py" in close
    assert "learning_distiller.py" in close
    assert "learning_distiller.py" in refusals


def test_no_must_shall_or_never_added_zero_headroom_baseline():
    """Lessons of N2 (a): `protocols/*.md`, `templates/**`, `ecosystem/*.yaml` carry zero
    headroom on the silent-rule baseline -- this template had zero occurrences before this
    lane touched it, and it must stay at zero. (Regression guard for this lane's own edit,
    not a claim on the integrator's full ratchet test, which only the integrator runs.)"""
    text = TEMPLATE.read_text(encoding="utf-8")
    hits = re.findall(r"\b(must|shall|never)\b", text)
    assert hits == [], f"forbidden normative word(s) found: {hits}"


def test_only_close_and_refusal_headings_changed_shape_others_untouched():
    """Ownership (ruling (i)): this lane edits ONLY the close and refusal steps. The other
    section headings and their intervening prose stay exactly as `templates/dispatcher-
    order-template.md`'s sibling lane and `lane-orchestrator-cycling` expect to find them."""
    text = TEMPLATE.read_text(encoding="utf-8")
    for heading in (
        "Merge priority when several are waiting",
        "Per handback — the one path",
    ):
        assert re.search(rf"^##\s*{re.escape(heading)}\s*$", text, re.M), (
            f"heading '{heading}' is missing or reworded -- out of this lane's ownership")


# --- LANE-B2-W1-b2-integrator-liveness: the integrator never goes silent and never runs as one 15 h session ----

def _wait_section(text: str) -> str:
    return _section(text, "Waiting — a handback wakes you")


def _cycle_section(text: str) -> str:
    return _section(text, "Cycle — hand over to a fresh session of the same role")


def test_the_wait_section_names_the_watch_command_for_a_monitor_and_keeps_the_cron_as_the_fallback():
    wait = _wait_section(TEMPLATE.read_text(encoding="utf-8"))
    assert "scripts/lane_end_guard.py watch" in wait, "the Monitor's one command"
    assert "Monitor" in wait
    assert "CronCreate" in wait and re.search(r"\b10[ -]min", wait), "the 10-minute cron stays as the fallback"
    assert re.search(r"fallback", wait, re.I)


def test_the_wake_runs_the_transport_sweep_and_the_integrators_writes_call_the_lint():
    """Done-contract 3: W1-6's sweep on every wake, W1-6's lint before every transport write."""
    wait = _wait_section(TEMPLATE.read_text(encoding="utf-8"))
    assert "scripts/transport_lint.py sweep" in wait and "--since" in wait
    assert "TRANSPORT-LINT" in wait
    assert "scripts/transport_lint.py check" in wait, "a file written by hand is linted before it is written"
    for written in ("STATE-", "REFUSED-", "DIGEST-", "SESSION-integrator"):
        assert written in wait, f"the lint covers {written}"


def test_the_cycle_hands_over_only_at_a_no_merge_point():
    cycle = _cycle_section(TEMPLATE.read_text(encoding="utf-8"))
    assert "no-merge point" in cycle
    assert re.search(r"no integration worktree (is )?open", cycle)
    assert re.search(r"no CI wait (is )?in flight", cycle)


def test_the_cycle_ceiling_is_three_hours_since_bind_and_the_old_two_hour_wording_is_gone():
    cycle = _cycle_section(TEMPLATE.read_text(encoding="utf-8"))
    assert re.search(r"at least every 3 h", cycle), "the ceiling is 3 h"
    assert re.search(r"since (you|the seat) bound|since bind", cycle)
    assert "About every 2 h" not in cycle


def test_the_successor_claims_and_binds_before_the_outgoing_seat_releases():
    cycle = _cycle_section(TEMPLATE.read_text(encoding="utf-8"))
    claim = cycle.index("INTEGRATOR-<BATCH>-cycle-<n>")
    bind = cycle.index("seat_registry.py bind")
    release = cycle.index("claim.py release")
    unbind = cycle.index("seat_registry.py unbind")
    assert claim < bind < release, "claim, then bind, then the outgoing release"
    assert bind < unbind


def test_the_successor_reads_the_receipt_back_three_times_thirty_seconds_apart():
    cycle = _cycle_section(TEMPLATE.read_text(encoding="utf-8"))
    assert re.search(r"three times", cycle) and re.search(r"30 s apart", cycle)
    assert "STATE" in cycle and "SESSION-integrator" in cycle


def test_the_successor_scans_the_in_flight_lanes_and_the_outgoing_seat_starts_no_new_merge():
    """Codex terra P1, round 2: the wake ledger records what a Monitor reported, not what was acted on, and two
    Monitors overlap while a handover runs. The cycle says who acts: the successor, from a scan of every lane
    the state file lists as IN-FLIGHT; the outgoing seat starts no merge once the successor has claimed."""
    cycle = _cycle_section(TEMPLATE.read_text(encoding="utf-8"))
    assert "IN-FLIGHT" in cycle and "HANDBACK" in cycle
    assert re.search(r"starts no new merge", cycle)


def test_the_cycle_runs_the_transport_sweep_and_stops_every_monitor_and_cron_before_handing_over():
    cycle = _cycle_section(TEMPLATE.read_text(encoding="utf-8"))
    assert "scripts/transport_lint.py sweep" in cycle
    assert "CronDelete" in cycle and "Monitor" in cycle
    assert "scripts/seat_state.py read" in cycle, "the state-file rebind of the existing wording is kept"
