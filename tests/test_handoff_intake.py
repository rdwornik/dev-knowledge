"""Acceptance tests for the H-Q5 KPI and bounded H-Q1 intake interface."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


def _intake():
    try:
        return importlib.import_module("handoff_intake")
    except ModuleNotFoundError as exc:
        if exc.name == "handoff_intake":
            pytest.fail("missing scripts/handoff_intake.py acceptance interface")
        raise


def test_kpi_computes_escaped_irreducible_rounds_and_measured_hypercare():
    intake = _intake()
    result = intake.kpi(
        escaped=["Where is the generated map?"],
        irreducible=["Approve destructive action"],
        rounds=2,
        hypercare_minutes=17,
        timebox_minutes=15,
    )
    assert result["escaped_questions"] == {
        "count": 1,
        "items": ["Where is the generated map?"],
        "target": 0,
        "met": False,
    }
    assert result["irreducible"] == {
        "items": ["Approve destructive action"],
        "owner": "operator",
        "route": "RATIFICATION",
    }
    assert result["rounds"] == {"value": 2, "target": 1, "met": False}
    assert result["hypercare"] == {
        "duration_minutes": 17,
        "timebox_minutes": 15,
        "target": "<= timebox",
        "met": False,
    }


def test_kpi_does_not_invent_hypercare_and_rejects_invalid_rounds():
    intake = _intake()
    unmeasured = intake.kpi(
        escaped=[], irreducible=[], rounds=1,
        hypercare_minutes=None, timebox_minutes=15,
    )
    assert unmeasured["hypercare"]["duration_minutes"] is None
    assert unmeasured["hypercare"]["status"].startswith("unmeasured — ")
    assert unmeasured["hypercare"]["met"] is None

    no_timebox = intake.kpi(
        escaped=[], irreducible=[], rounds=1,
        hypercare_minutes=3, timebox_minutes=None,
    )
    assert no_timebox["hypercare"] == {
        "duration_minutes": 3,
        "status": "unmeasured — no declared timebox",
        "met": None,
    }
    with pytest.raises(ValueError):
        intake.kpi(
            escaped=[], irreducible=[], rounds=0,
            hypercare_minutes=None, timebox_minutes=None,
        )


def test_kpi_lines_are_flat_key_value_lines():
    intake = _intake()
    lines = intake.kpi_lines(intake.kpi(
        escaped=[], irreducible=["Operator decision"], rounds=1,
        hypercare_minutes=4, timebox_minutes=5,
    ))
    assert lines.strip()
    assert "|" not in lines
    assert all(":" in line for line in lines.splitlines() if line.strip())
    assert "escaped_questions" in lines
    assert "RATIFICATION" in lines


def test_kpi_cli_reads_the_two_input_files_and_prints_fields(tmp_path, capsys):
    intake = _intake()
    escaped = tmp_path / "escaped.txt"
    irreducible = tmp_path / "irreducible.txt"
    escaped.write_text("", encoding="utf-8")
    irreducible.write_text("Operator approval\n", encoding="utf-8")
    rc = intake.main([
        "kpi", "--escaped-file", str(escaped), "--irreducible-file", str(irreducible),
        "--rounds", "1", "--hypercare-minutes", "4", "--timebox-minutes", "5",
    ])
    captured = capsys.readouterr()
    assert rc == 0
    assert "escaped_questions" in captured.out
    assert "RATIFICATION" in captured.out
    assert "duration_minutes" in captured.out


# --- best-effort intake, deliberately tested after the required KPI surface ----------------------------

def test_build_intake_writes_a_disposition_for_every_plan_item():
    intake = _intake()
    body = intake.build_intake(
        "- Where is the generated index?\n"
        "- Apply R166 before the cut.\n"
        "- Choose the output folder.\n",
        owed_sources=["K12 is also owed by the current handoff."],
        seat="Tech-Architect-46",
        today="2026-10-24",
    )
    assert body.startswith(
        "kind: FINDING\ndate: 2026-10-24\nby: Tech-Architect-46\n"
    )
    assert "# FINDING-Tech-Architect-46-INTAKE-2026-10-24" in body
    assert "## Disposition ledger" in body
    assert "| 1 | Where is the generated index? | ASK |" in body
    assert "| 2 | Apply R166 before the cut. | OWED |" in body
    assert "| 3 | Choose the output folder. | ASSUME |" in body
    assert "owed: K12 R166" in body
    assert "## owed:" not in body


def test_build_intake_caps_questions_at_seven_and_defers_the_rest():
    intake = _intake()
    plan = "\n".join(f"- Question {number}?" for number in range(1, 10))
    body = intake.build_intake(
        plan, owed_sources=[], seat="Tech-Architect-46", today="2026-10-24"
    )
    assert body.count("## Questions") == 1
    questions = body.split("## Questions", 1)[1].split("## ", 1)[0]
    assert sum(line.startswith("- ") for line in questions.splitlines()) == 7
    deferred = body.split("## Deferred (round 2 not allowed)", 1)[1]
    assert "Question 8?" in deferred and "Question 9?" in deferred


def test_carry_ledger_owed_extracts_owed_lines_and_decision_table_rows(tmp_path):
    intake = _intake()
    ledger = tmp_path / "CARRY-LEDGER.md"
    ledger.write_text(
        "owed: R166\n"
        "| ID | Owed |\n"
        "|---|---|\n"
        "| H-Q6 | enforce decision ids |\n"
        "| plain | ignore this row |\n",
        encoding="utf-8",
    )
    assert intake.carry_ledger_owed(ledger) == [
        "owed: R166",
        "| H-Q6 | enforce decision ids |",
    ]


def test_gen_handoff_intake_cli_routes_a_finding_through_transport(
    tmp_path, monkeypatch, capsys
):
    from click.testing import CliRunner

    import gen_handoff as gh
    import transport

    transport_root = tmp_path / "transport"
    (transport_root / "to-browser").mkdir(parents=True)
    (transport_root / "to-cc").mkdir()
    monkeypatch.setattr(transport, "known_root", lambda: transport_root)
    plan = tmp_path / "plan.md"
    plan.write_text("- Where is the map?\n", encoding="utf-8")
    result = CliRunner().invoke(gh.main, ["--intake", "--plan", str(plan)])
    assert result.exit_code == 0, result.output
    captured = capsys.readouterr()
    emitted_path = Path(result.output.strip().splitlines()[-1])
    assert emitted_path.is_file()
    assert emitted_path.parent == transport_root / "to-browser"
    assert emitted_path.read_text(encoding="utf-8").startswith("kind: FINDING")
    assert str(emitted_path) in result.output or str(emitted_path) in captured.out


def test_gen_handoff_intake_requires_a_plan_and_names_the_missing_flag():
    from click.testing import CliRunner

    import gen_handoff as gh

    result = CliRunner().invoke(gh.main, ["--intake"])
    assert result.exit_code != 0
    assert "--plan" in result.output
