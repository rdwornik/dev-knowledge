"""Acceptance tests for the computed handoff KPI and the bounded intake surface."""
from __future__ import annotations

import importlib
import importlib.util
import re
import sys
from pathlib import Path

import pytest

import gen_handoff as gh

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


def _intake_module():
    spec = importlib.util.find_spec("handoff_intake")
    assert spec is not None, "scripts/handoff_intake.py is required"
    return importlib.import_module("handoff_intake")


def test_kpi_computes_escaped_irreducible_rounds_and_measured_hypercare():
    intake = _intake_module()
    result = intake.kpi(
        escaped=["Which branch is active?"],
        irreducible=["Operator must choose the destination."],
        rounds=1,
        hypercare_minutes=12,
        timebox_minutes=15,
    )
    assert result["escaped_questions"] == {
        "count": 1,
        "items": ["Which branch is active?"],
        "target": 0,
        "met": False,
    }
    assert result["irreducible"] == {
        "items": ["Operator must choose the destination."],
        "owner": "operator",
        "route": "RATIFICATION",
    }
    assert result["rounds"] == {"value": 1, "target": 1, "met": True}
    assert result["hypercare"] == {
        "duration_minutes": 12,
        "timebox_minutes": 15,
        "target": "<= timebox",
        "met": True,
    }
    empty = intake.kpi(
        escaped=[], irreducible=[], rounds=1,
        hypercare_minutes=None, timebox_minutes=None,
    )
    assert empty["escaped_questions"] == {
        "count": 0, "items": [], "target": 0, "met": True,
    }


def test_kpi_marks_hypercare_over_the_declared_timebox_unmet():
    hypercare = _intake_module().kpi(
        escaped=[], irreducible=[], rounds=1,
        hypercare_minutes=16, timebox_minutes=15,
    )["hypercare"]
    assert hypercare["met"] is False
    assert hypercare["target"] == "<= timebox"


@pytest.mark.parametrize("rounds", (0, -1))
def test_kpi_rejects_round_counts_below_one(rounds):
    with pytest.raises(ValueError):
        _intake_module().kpi(
            escaped=[], irreducible=[], rounds=rounds,
            hypercare_minutes=None, timebox_minutes=None,
        )


def test_kpi_leaves_unmeasured_hypercare_unknown_instead_of_zero():
    hypercare = _intake_module().kpi(
        escaped=[], irreducible=[], rounds=1,
        hypercare_minutes=None, timebox_minutes=20,
    )["hypercare"]
    assert hypercare["duration_minutes"] is None
    assert hypercare["status"].startswith("unmeasured — ")
    assert hypercare["met"] is None
    assert hypercare["duration_minutes"] != 0


def test_kpi_with_duration_but_no_timebox_reports_unmeasured_timebox():
    hypercare = _intake_module().kpi(
        escaped=[], irreducible=[], rounds=1,
        hypercare_minutes=4, timebox_minutes=None,
    )["hypercare"]
    assert hypercare["duration_minutes"] == 4
    assert hypercare["status"] == "unmeasured — no declared timebox"
    assert hypercare["met"] is None


def test_kpi_lines_are_flat_key_value_lines():
    intake = _intake_module()
    result = intake.kpi(
        escaped=[], irreducible=["Need operator ruling."], rounds=2,
        hypercare_minutes=9, timebox_minutes=5,
    )
    lines = intake.kpi_lines(result)
    assert lines.strip()
    assert "|" not in lines and not re.search(r"(?m)^\s*\|", lines)
    assert all(":" in line for line in lines.splitlines())
    assert result["rounds"] == {"value": 2, "target": 1, "met": False}


def test_kpi_cli_reads_question_files_and_prints_the_computed_fields(tmp_path, capsys):
    intake = _intake_module()
    escaped = tmp_path / "escaped.txt"
    irreducible = tmp_path / "irreducible.txt"
    escaped.write_text("Question one?\nQuestion two?\n", encoding="utf-8")
    irreducible.write_text("Operator decision.\n", encoding="utf-8")
    rc = intake.main([
        "kpi", "--escaped-file", str(escaped), "--irreducible-file", str(irreducible),
        "--rounds", "1", "--hypercare-minutes", "7", "--timebox-minutes", "10",
    ])
    assert rc == 0
    output = capsys.readouterr().out
    expected = intake.kpi(
        escaped=["Question one?", "Question two?"],
        irreducible=["Operator decision."],
        rounds=1,
        hypercare_minutes=7,
        timebox_minutes=10,
    )
    assert output == intake.kpi_lines(expected)


# --- Best effort (h): bounded FINDING intake, deliberately tested after the KPI contract ---

def test_build_intake_emits_one_disposition_ledger_and_owed_ids():
    intake = _intake_module()
    body = intake.build_intake(
        "- Should we proceed?\n"
        "- Record R166 landing\n"
        "- Use prior context\n"
        "- Keep the intro concise\n",
        owed_sources=["Use prior context", "H-Q1"],
        seat="Tech-Architect-47",
        today="2026-10-24",
    )
    lines = body.splitlines()
    assert lines[:3] == [
        "kind: FINDING",
        "date: 2026-10-24",
        "by: Tech-Architect-47",
    ]
    assert "# FINDING-Tech-Architect-47-INTAKE-2026-10-24" in lines
    assert "## Disposition ledger" in body
    assert "| 1 | Should we proceed? | ASK |" in body
    assert "| 2 | Record R166 landing | OWED |" in body
    assert "| 3 | Use prior context | OWED |" in body
    assert "| 4 | Keep the intro concise | ASSUME |" in body
    owed_line = re.search(r"(?m)^owed: (.*)$", body)
    assert owed_line is not None
    assert {"R166", "H-Q1"} <= set(re.findall(
        r"\b(?:R\d+|K\d+|D\d+|H-Q\d+|H-L\d+|H-P\d+|H\d+)\b", owed_line.group(1)))
    assert not re.search(r"(?m)^## owed:", body)


def test_build_intake_caps_questions_at_seven_and_defers_the_rest():
    intake = _intake_module()
    plan = "\n".join(f"- Question number {n}?" for n in range(1, 10))
    body = intake.build_intake(
        plan, owed_sources=[], seat="Seat-1", today="2026-10-24")
    question_section = re.search(
        r"(?ms)^## Questions\s*\n(.*?)(?=^## |\Z)", body)
    deferred_section = re.search(
        r"(?ms)^## Deferred \(round 2 not allowed\)\s*\n(.*?)(?=^## |\Z)", body)
    assert question_section is not None and deferred_section is not None
    assert sum(
        f"Question number {n}?" in question_section.group(1) for n in range(1, 10)
    ) == 7
    assert "Question number 8?" in deferred_section.group(1)
    assert "Question number 9?" in deferred_section.group(1)
    assert body.count("## Questions") == 1


def test_intake_cli_writes_through_transport_and_requires_a_plan(tmp_path, monkeypatch):
    from click.testing import CliRunner
    import transport

    transport_root = tmp_path / "transport"
    (transport_root / "to-browser").mkdir(parents=True)
    (transport_root / "to-cc").mkdir()
    plan = tmp_path / "plan.md"
    plan.write_text("- Should we proceed?\n- Record R166 landing\n", encoding="utf-8")
    monkeypatch.setattr(gh, "transport_root", lambda *args, **kwargs: transport_root)
    real_write = transport.write
    writers = []

    def tracked_write(writer, *args, **kwargs):
        writers.append(writer)
        return real_write(writer, *args, **kwargs)

    monkeypatch.setattr(transport, "write", tracked_write)
    runner = CliRunner()

    missing = runner.invoke(gh.main, ["--intake"], env={"CLAUDE_PROMPTS_DIR": str(transport_root)})
    assert missing.exit_code != 0
    assert "--plan" in missing.output

    result = runner.invoke(
        gh.main, ["--intake", "--plan", str(plan)],
        env={"CLAUDE_PROMPTS_DIR": str(transport_root)},
    )
    assert result.exit_code == 0, result.output
    assert "FINDING-" in result.output
    assert "lane" in writers
    written = list((transport_root / "to-browser").glob("FINDING-*-INTAKE-*.md"))
    assert len(written) == 1
    text = written[0].read_text(encoding="utf-8")
    assert text.startswith("kind: FINDING\n")
    assert "owed: R166" in text


def test_carry_ledger_owed_returns_owed_lines_and_decision_table_rows(tmp_path):
    intake = _intake_module()
    ledger = tmp_path / "CARRY-LEDGER.md"
    owed_line = "owed: H-Q1 R166"
    decision_row = "| H-Q6 | owed lists use decision ids | transport lint |"
    ledger.write_text(
        "## Carried\n"
        + owed_line + "\n"
        + "| Item | Description | Carrier |\n"
        + decision_row + "\n"
        + "| ordinary | not a decision token | none |\n",
        encoding="utf-8",
    )
    assert intake.carry_ledger_owed(ledger) == [owed_line, decision_row]
