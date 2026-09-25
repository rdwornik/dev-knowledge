"""Tests for scripts/learning_distiller.py (LANE-5B2-13, [#1015]-adjacent v0 build).

THE FIXTURE-PINNED CASE is Done-contract item 2: running the module on the N1 receipts
(`tests/fixtures/learning_distiller/`) must yield exactly three candidate rows -- the two
repaired REFUSED lanes (hooks-port, plan-lint-grammar) and the dispatcher's one
`**DISPATCHER FAULT**` marker (the malformed-argv repair-launch fault at 03:38:52, fired from
inside the repair watcher loop -- the contract's "the dispatcher's watcher-loop fault"). No
other N1 event qualifies: no lane in the fixture ends `STATE ... FAILED`.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import learning_distiller as ld

_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "learning_distiller"
_INTEGRATOR = _FIXTURES / "SESSION-integrator-wave5b-n1-2026-09-24.md"
_DISPATCHER = _FIXTURES / "SESSION-dispatcher-wave5b-n1-2026-09-24.md"
_REFUSED_HOOKS = _FIXTURES / "REFUSED-lane-hooks-port.md"
_REFUSED_PLAN_LINT = _FIXTURES / "REFUSED-lane-plan-lint-grammar.md"


@pytest.fixture(scope="module")
def n1_rows() -> list[ld.CandidateRow]:
    return ld.distill(_INTEGRATOR, _DISPATCHER, [_REFUSED_HOOKS, _REFUSED_PLAN_LINT])


# --- Done-contract item 2: exactly these three, on the real N1 fixture -----------------

def test_n1_fixture_yields_exactly_three_rows(n1_rows):
    assert len(n1_rows) == 3


def test_n1_fixture_yields_the_two_repairs_and_one_dispatcher_fault(n1_rows):
    kinds = sorted(r.kind for r in n1_rows)
    assert kinds == ["dispatcher_fault", "repair", "repair"]


def test_n1_fixture_repair_slugs_are_hooks_port_and_plan_lint_grammar(n1_rows):
    repair_slugs = sorted(r.slug for r in n1_rows if r.kind == "repair")
    assert repair_slugs == ["lane-hooks-port", "lane-plan-lint-grammar"]


def test_n1_dispatcher_fault_row_names_the_repair_launch_incident(n1_rows):
    fault = next(r for r in n1_rows if r.kind == "dispatcher_fault")
    assert "03:38:52" in fault.provenance
    assert "argv" in fault.title.lower() or "argv" in fault.detail.lower()


def test_every_n1_row_has_a_check_command_never_a_bare_comment(n1_rows):
    for row in n1_rows:
        assert row.check.strip()
        assert not row.check.strip().startswith("#"), row.check


def test_n1_repair_rows_are_not_proposed_dispatcher_fault_row_is(n1_rows):
    for row in n1_rows:
        if row.kind == "repair":
            assert row.proposed is False, row
        elif row.kind == "dispatcher_fault":
            assert row.proposed is True, row


# --- repair rows: the regression check is DERIVED from the REFUSED file's own evidence --

def test_hooks_port_repair_check_targets_the_named_test_file(n1_rows):
    row = next(r for r in n1_rows if r.slug == "lane-hooks-port")
    assert row.check == "uv run --locked pytest tests/test_surface_triage.py -q"


def test_plan_lint_grammar_repair_check_targets_the_named_test_file(n1_rows):
    row = next(r for r in n1_rows if r.slug == "lane-plan-lint-grammar")
    assert row.check == "uv run --locked pytest tests/test_silent_rule_ratchet.py -q"


def test_hooks_port_repair_provenance_cites_the_refused_file_and_repair_number(n1_rows):
    row = next(r for r in n1_rows if r.slug == "lane-hooks-port")
    assert "REFUSED-lane-hooks-port.md" in row.provenance
    assert "repair 1 of 2" in row.provenance
    assert "the INTEGRATOR" in row.provenance


# --- unit-level: parse_refused, in isolation ---------------------------------------------

def test_parse_refused_returns_none_without_the_refused_heading():
    assert ld.parse_refused("no heading here", Path("x.md")) is None


def test_parse_refused_title_carries_the_bold_summary_phrase():
    row = ld.parse_refused(_REFUSED_HOOKS.read_text(encoding="utf-8"), _REFUSED_HOOKS)
    assert row is not None
    assert "lane-hooks-port" in row.title
    assert "four reds in a test file this lane rewrote" in row.title


def test_test_files_ignores_a_bare_prose_mention_without_a_node_id():
    body = ("See `tests/test_billing_leak_sentinel.py` for the same shape, but only "
            "`tests/test_surface_triage.py::test_real_one` actually failed.")
    assert ld._test_files(body) == ["tests/test_surface_triage.py"]


# --- unit-level: find_failed_lanes, exercised on a synthetic string (no N1 fixture has one) -

def test_find_failed_lanes_on_a_synthetic_state_line():
    text = (
        "some earlier receipt text\n\n"
        "STATE lane-synthetic-failure FAILED deadbeef1 2026-09-25T09:00+02:00 -\n"
    )
    rows = ld.find_failed_lanes(text, Path("SESSION-integrator-synthetic.md"))
    assert len(rows) == 1
    assert rows[0].kind == "failed"
    assert rows[0].slug == "lane-synthetic-failure"
    assert "deadbeef1" in rows[0].provenance


def test_find_failed_lanes_is_empty_on_the_n1_integrator_fixture():
    text = _INTEGRATOR.read_text(encoding="utf-8")
    assert ld.find_failed_lanes(text, _INTEGRATOR) == []


# --- unit-level: find_dispatcher_faults, exercised on a synthetic second marker ----------

def test_find_dispatcher_faults_finds_two_markers_in_one_file():
    text = (
        "## Repairs\n\n"
        "- **01:00:00 DISPATCHER FAULT** — `lane-a` fired with a bad flag: exit 2, no work.\n"
        "- next bullet, unrelated\n\n"
        "## Later\n\n"
        "- **02:00:00 DISPATCHER FAULT** — `lane-b` fired twice: duplicate job, killed.\n"
    )
    rows = ld.find_dispatcher_faults(text, Path("SESSION-dispatcher-synthetic.md"))
    assert [r.slug for r in rows] == ["lane-a", "lane-b"]
    assert all(r.kind == "dispatcher_fault" for r in rows)


# --- rendering: text and JSON ------------------------------------------------------------

def test_render_rows_text_is_flat_and_counts_kinds(n1_rows):
    text = ld.render_rows(n1_rows)
    assert "3 candidate row(s)" in text
    assert "1 dispatcher_fault" in text
    assert "2 repair" in text
    for row in n1_rows:
        assert row.title in text


def test_render_rows_empty_says_so_rather_than_nothing():
    assert "no REFUSED" in ld.render_rows([])


def test_to_dict_round_trips_every_field(n1_rows):
    for row in n1_rows:
        d = row.to_dict()
        assert d["kind"] == row.kind
        assert d["slug"] == row.slug
        assert d["check"] == row.check
        assert d["proposed"] == row.proposed


# --- unit-level: lane_terminal_state / _verify_refused_row -------------------------------

def test_lane_terminal_state_reads_the_last_matching_state_line():
    text = (
        "STATE lane-x REFUSED abc123 2026-09-25T00:00+02:00 - repair 1 of 2\n"
        "STATE lane-x MERGED def4567 2026-09-25T01:00+02:00\n"
    )
    assert ld.lane_terminal_state(text, "lane-x") == ("MERGED", "def4567")


def test_lane_terminal_state_none_when_slug_never_appears():
    assert ld.lane_terminal_state("STATE lane-y MERGED abc1234", "lane-x") is None


def test_verify_refused_row_reclassifies_an_unmerged_refusal():
    row = ld.CandidateRow(kind="repair", slug="lane-never-merged", title="t",
                          provenance="p", check="uv run --locked pytest tests/x.py -q")
    verified = ld._verify_refused_row(row, "STATE lane-never-merged REFUSED abc FAILED foo")
    # no MERGED line for this exact slug -> reclassified
    assert verified.kind == "unverified_refusal"
    assert "UNVERIFIED" in verified.title


def test_verify_refused_row_keeps_repair_kind_when_merged():
    row = ld.CandidateRow(kind="repair", slug="lane-ok", title="t", provenance="p", check="c")
    verified = ld._verify_refused_row(row, "STATE lane-ok MERGED abc1234")
    assert verified.kind == "repair"
    assert verified.title == "t"


def test_n1_fixture_refused_rows_are_verified_merged_via_the_real_integrator_text(n1_rows):
    # both N1 REFUSED lanes really did land (STATE ... MERGED ...) later in the same
    # integrator receipt, so the real fixture must NOT trip the unverified path.
    assert all(r.kind != "unverified_refusal" for r in n1_rows)


# --- CLI: the real entry point, end to end -----------------------------------------------

def test_cli_run_text_format_end_to_end():
    result = subprocess.run(
        [sys.executable, str(Path(ld.__file__).resolve()), "run",
         "--integrator", str(_INTEGRATOR), "--dispatcher", str(_DISPATCHER),
         "--refused", str(_REFUSED_HOOKS), "--refused", str(_REFUSED_PLAN_LINT)],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    assert "3 candidate row(s)" in result.stdout


def test_cli_run_json_format_end_to_end():
    result = subprocess.run(
        [sys.executable, str(Path(ld.__file__).resolve()), "run",
         "--integrator", str(_INTEGRATOR), "--dispatcher", str(_DISPATCHER),
         "--refused", str(_REFUSED_HOOKS), "--refused", str(_REFUSED_PLAN_LINT),
         "--format", "json"],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    rows = json.loads(result.stdout)
    assert len(rows) == 3
    assert {r["kind"] for r in rows} == {"repair", "dispatcher_fault"}


def test_cli_run_without_refused_files_still_finds_the_dispatcher_fault():
    result = subprocess.run(
        [sys.executable, str(Path(ld.__file__).resolve()), "run",
         "--integrator", str(_INTEGRATOR), "--dispatcher", str(_DISPATCHER),
         "--format", "json"],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    rows = json.loads(result.stdout)
    assert len(rows) == 1
    assert rows[0]["kind"] == "dispatcher_fault"
