"""RED tests: distill() must read the integrator's real refusal shapes (E2.0 fixtures)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

import learning_distiller as ld

_FIX = Path(__file__).parent / "fixtures" / "distiller"
_REFUSED = _FIX / "REFUSED-e2-rulings.md"
_INTEGRATOR = _FIX / "SESSION-integrator-e2-0.md"
_DISPATCHER = _FIX / "SESSION-e2-orchestrator.md"
_NO_EVENT = "no REFUSED, repair, FAILED or dispatcher-fault event found"
_VERBATIM = "test_the_live_tree_carries_no_IN_ERA_uncovered_decision"


@pytest.fixture(scope="module")
def rows() -> list[ld.CandidateRow]:
    return ld.distill(_INTEGRATOR, _DISPATCHER, [_REFUSED])


def _cli_args(*extra: str) -> list[str]:
    return ["run", "--refused", str(_REFUSED), "--dispatcher", str(_DISPATCHER),
            "--integrator", str(_INTEGRATOR), *extra]


def test_rulings_and_fates_events_each_yield_rows(rows):
    rulings = [r for r in rows if r.slug == "e2-rulings"]
    fates = [r for r in rows if r.slug == "e2-fates"]
    assert len(rulings) >= 2
    assert any("repair 1 of 2" in r.provenance for r in rulings)
    assert any("repair 2 of 2" in r.provenance for r in rulings)
    assert len(fates) >= 2


def test_state_line_does_not_duplicate_a_refused_file_row(rows):
    rulings = [r for r in rows if r.slug == "e2-rulings"]
    assert len(rulings) == 2
    assert sum("repair 1 of 2" in r.provenance for r in rulings) == 1
    assert sum("repair 2 of 2" in r.provenance for r in rulings) == 1


def test_rows_carry_check_title_and_unverified_kind(rows):
    assert rows
    assert all(r.check.strip() and r.title.strip() for r in rows)
    rulings = [r for r in rows if r.slug == "e2-rulings"]
    assert rulings
    assert all(r.kind == "unverified_refusal" for r in rulings)


def test_repair_2_detail_quotes_refusal_verbatim(rows):
    repair2 = [r for r in rows if r.slug == "e2-rulings" and "repair 2 of 2" in r.provenance]
    assert repair2
    assert _VERBATIM in repair2[0].detail


def test_cli_text_reports_events():
    result = CliRunner().invoke(ld.cli, _cli_args())
    assert result.exit_code == 0
    assert _NO_EVENT not in result.output


def test_cli_json_lists_at_least_four_objects():
    result = CliRunner().invoke(ld.cli, _cli_args("--format", "json"))
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, list) and len(data) >= 4
    assert all(isinstance(d, dict) for d in data)


def test_legacy_heading_still_yields_unverified_refusal(tmp_path):
    refused = tmp_path / "REFUSED-lane-x.md"
    refused.write_text(
        "# REFUSED \u2014 lane-x, repair 1 of 2\n\n## What failed\n\n"
        "`tests/test_x.py::test_it` failed.\n", encoding="utf-8")
    integrator = tmp_path / "integrator.md"
    integrator.write_text("nothing here\n", encoding="utf-8")
    dispatcher = tmp_path / "dispatcher.md"
    dispatcher.write_text("nothing here\n", encoding="utf-8")
    out = ld.distill(integrator, dispatcher, [refused])
    assert [(r.kind, r.slug) for r in out if r.slug == "lane-x"] == [("unverified_refusal", "lane-x")]


def test_legacy_state_merged_line_still_read():
    assert ld.lane_terminal_state("STATE lane-x MERGED abc1234\n", "lane-x") == ("MERGED", "abc1234")
