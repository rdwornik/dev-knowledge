"""Unit tests for scripts/trace_writer.py (Lane h0 — the dispatch trace stream)."""

import importlib.util
from datetime import date
from pathlib import Path

from click.testing import CliRunner


_P = Path(__file__).resolve().parent.parent / "scripts" / "trace_writer.py"


def _load():
    spec = importlib.util.spec_from_file_location("trace_writer", _P)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tw = _load()

_CONTRACT = "# LANE-h0-trace — a contract AS SENT\n\nsome body text\n"
_SKELETON = "#!/usr/bin/env bash\nclaude -p \"...\" --permission-mode bypassPermissions\n"
_RECEIPT = '{\n  "is_error": false,\n  "status": "DONE",\n  "exit_code": 0\n}\n'


def _seed(tmp_path: Path):
    contract = tmp_path / "LANE-h0-trace.md"
    contract.write_text(_CONTRACT, encoding="utf-8")
    skeleton = tmp_path / "dispatch-run.sh"
    skeleton.write_text(_SKELETON, encoding="utf-8")
    receipt = tmp_path / "receipt.json"
    receipt.write_text(_RECEIPT, encoding="utf-8")
    return contract, skeleton, receipt


# --- render_trace ------------------------------------------------------------

def test_render_trace_carries_all_five_parts():
    body = tw.render_trace(
        lane="lane-h0-trace", contract_text=_CONTRACT, skeleton_text=_SKELETON,
        receipt_text=_RECEIPT, outcome="branch: worktree-lane-h0-trace; commits: 1",
        model="opus", effort="high",
    )
    assert "## 1. Contract AS SENT" in body and _CONTRACT.strip() in body
    assert "## 2. Skeleton run" in body and _SKELETON.strip() in body
    assert "## 3. receipt.json" in body and '"is_error": false' in body
    assert "## 4. Outcome" in body and "worktree-lane-h0-trace" in body
    assert "## 5. Model / effort" in body and "opus" in body and "high" in body


# --- write_trace ---------------------------------------------------------------

def test_write_trace_names_file_by_date_and_lane(tmp_path):
    contract, skeleton, receipt = _seed(tmp_path)
    out_dir = tmp_path / "prompts"
    path = tw.write_trace(
        lane="lane-h0-trace", contract_path=contract, skeleton_path=skeleton,
        receipt_path=receipt, outcome="branch: x; commits: 1; tests: pytest -k trace",
        model="opus", effort="high", out_dir=out_dir, on=date(2026, 9, 5),
    )
    assert path == out_dir / "2026-09-05-lane-h0-trace.md"
    assert path.exists()


def test_write_trace_seeds_exactly_one_file(tmp_path):
    contract, skeleton, receipt = _seed(tmp_path)
    out_dir = tmp_path / "prompts"
    tw.write_trace(
        lane="lane-h0-trace", contract_path=contract, skeleton_path=skeleton,
        receipt_path=receipt, outcome="branch: x; commits: 1; tests: pytest -k trace",
        model="opus", effort="high", out_dir=out_dir, on=date(2026, 9, 5),
    )
    assert sorted(p.name for p in out_dir.iterdir()) == ["2026-09-05-lane-h0-trace.md"]


def test_write_trace_second_dispatch_same_day_overwrites_not_accumulates(tmp_path):
    contract, skeleton, receipt = _seed(tmp_path)
    out_dir = tmp_path / "prompts"
    for outcome in ("first outcome", "second outcome"):
        tw.write_trace(
            lane="lane-h0-trace", contract_path=contract, skeleton_path=skeleton,
            receipt_path=receipt, outcome=outcome, model="opus", effort="high",
            out_dir=out_dir, on=date(2026, 9, 5),
        )
    files = list(out_dir.iterdir())
    assert len(files) == 1
    assert "second outcome" in files[0].read_text(encoding="utf-8")


def test_write_trace_creates_out_dir(tmp_path):
    contract, skeleton, receipt = _seed(tmp_path)
    out_dir = tmp_path / "nested" / "prompts"
    assert not out_dir.exists()
    tw.write_trace(
        lane="lane-h0-trace", contract_path=contract, skeleton_path=skeleton,
        receipt_path=receipt, outcome="outcome", model="opus", effort="high",
        out_dir=out_dir, on=date(2026, 9, 5),
    )
    assert out_dir.is_dir()


# --- CLI -----------------------------------------------------------------------

def test_cli_writes_trace_and_echoes_path(tmp_path):
    contract, skeleton, receipt = _seed(tmp_path)
    out_dir = tmp_path / "prompts"
    runner = CliRunner()
    result = runner.invoke(tw.main, [
        "--lane", "lane-h0-trace",
        "--contract", str(contract),
        "--skeleton", str(skeleton),
        "--receipt", str(receipt),
        "--outcome", "branch: worktree-lane-h0-trace; commits: 1",
        "--model", "opus",
        "--effort", "high",
        "--out-dir", str(out_dir),
    ])
    assert result.exit_code == 0, result.output
    assert "trace written:" in result.output
    written = list(out_dir.iterdir())
    assert len(written) == 1
    assert "opus" in written[0].read_text(encoding="utf-8")
