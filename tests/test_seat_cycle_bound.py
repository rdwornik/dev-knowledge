"""The successor writes its own BOUND line: First-act section + the `bound` command (fakes only)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

import seat_cycle as sc


def _handover(tmp_path: Path, **kw) -> Path:
    return sc.write_handover(tmp_path / "HANDOVER-seat-a-cycle-3.md", seat="seat-a", role="orchestrator",
                             cycle=3, state="s", next_steps=["do it"], open_decisions=["none"],
                             live_children=["none"], bookkeeping="b", by="seat-a", **kw)


def _transcript(tmp_path: Path, model: str = "claude-opus-4-7") -> Path:
    path = tmp_path / "sess-1.jsonl"
    rows = [{"type": "assistant", "message": {"model": "old-model"}},
            {"type": "user", "message": {}},
            {"type": "assistant", "message": {"model": model}},
            {"type": "user", "message": {}}]
    path.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    return path


def _agents(*names: str) -> list[dict]:
    return [{"name": n, "id": f"job-{i}", "sessionId": "sess-1"} for i, n in enumerate(names)]


def test_handover_carries_exact_first_act_command(tmp_path):
    path = _handover(tmp_path, successor_slug="custom-slug")
    text = path.read_text(encoding="utf-8")
    cmd = (f"uv run --locked python scripts/seat_cycle.py bound --handover {path.resolve()} "
           f"--name custom-slug --seat seat-a --cycle 3")
    assert cmd in text
    assert text.index("## First act (successor)") > text.index("## Seat bookkeeping")
    assert sc.lint_handover(text) == []


def test_default_successor_slug(tmp_path):
    assert "--name seat-a-c4 " in _handover(tmp_path).read_text(encoding="utf-8")


def test_lint_flags_missing_first_act(tmp_path):
    text = _handover(tmp_path).read_text(encoding="utf-8")
    stripped = text.split("## First act (successor)")[0]
    assert any("First act" in d for d in sc.lint_handover(stripped))


def test_bound_writes_one_line_await_accepts(tmp_path, monkeypatch):
    path = _handover(tmp_path)
    transcript = _transcript(tmp_path)
    monkeypatch.setattr(sc, "_list_agents", lambda: _agents("other", "seat-a-c4"))
    monkeypatch.setattr(sc, "_find_transcript", lambda sid: transcript if sid == "sess-1" else None)
    res = CliRunner().invoke(sc.cli, ["bound", "--handover", str(path), "--name", "seat-a-c4",
                                      "--seat", "seat-a", "--cycle", "3"])
    assert res.exit_code == 0, res.output
    text = path.read_text(encoding="utf-8")
    assert text.count("BOUND seat=") == 1
    line = "BOUND seat=seat-a cycle=3 job=job-1 model=claude-opus-4-7"
    assert res.output.strip() == line
    assert sc.await_bound(path, job_id="job-1", timeout=0) == line


def test_unreadable_transcript_is_unknown(tmp_path):
    path = _handover(tmp_path)
    line = sc.bind_successor(path, name="x", seat="seat-a", cycle_no=3,
                             list_agents=lambda: _agents("x"), find_transcript=lambda sid: None)
    assert line.endswith("model=unknown")


@pytest.mark.parametrize("agents", [_agents("a", "a"), _agents("b")])
def test_ambiguous_or_missing_name_writes_nothing(tmp_path, monkeypatch, agents):
    path = _handover(tmp_path)
    before = path.read_text(encoding="utf-8")
    monkeypatch.setattr(sc, "_list_agents", lambda: agents)
    res = CliRunner().invoke(sc.cli, ["bound", "--handover", str(path), "--name", "a",
                                      "--seat", "seat-a", "--cycle", "3"])
    assert res.exit_code == 1
    assert "expected exactly 1" in res.output
    assert path.read_text(encoding="utf-8") == before
