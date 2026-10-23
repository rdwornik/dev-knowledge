"""Input-completeness tests for the process binding gate."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_process_diagrams as gpd  # noqa: E402


DISPATCH = """\
class Cli:
    def command(self, name):
        return lambda function: function


cli = Cli()

@cli.command("launch")
def launch():
    launch_anchor()

def launch_lane():
    lane_anchor()
"""


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "dispatch.py").write_text(DISPATCH, encoding="utf-8")
    (scripts / "target.py").write_text("target_anchor()\n", encoding="utf-8")
    return root


def _binding(states: list[dict]) -> dict:
    return {
        "schema": "process-binding/1",
        "processes": {
            "P1": {
                "states": states,
                "transitions": [],
                "retired": [],
            }
        },
    }


def _state(name: str, line: int, anchor: str, file: str = "scripts/dispatch.py") -> dict:
    return {
        "id": f"S-{name}",
        "name": name,
        "binding": {
            "code": {
                "file_line": f"{file}:{line}",
                "anchor": anchor,
            }
        },
    }


def _line(source: str, text: str) -> int:
    return next(i for i, line in enumerate(source.splitlines(), start=1) if text in line)


def _write_binding(tmp_path: Path, binding: dict) -> Path:
    path = tmp_path / "binding.yaml"
    path.write_text(yaml.safe_dump(binding, sort_keys=False), encoding="utf-8")
    return path


def _clean_binding() -> dict:
    return _binding(
        states=[
            _state("launch", _line(DISPATCH, "launch_anchor()"), "launch_anchor("),
            _state("lane", _line(DISPATCH, "lane_anchor()"), "lane_anchor("),
        ]
    )


MISSING_DISPATCH_LINES = [
    "GATE INPUT launch: file scripts/dispatch.py is missing",
    "GATE INPUT lane: file scripts/dispatch.py is missing",
    "GATE INPUT scripts/dispatch.py is missing: the entry-point set is empty, not complete",
]


def test_gate_fails_when_dispatch_input_is_missing(tmp_path: Path, capsys):
    root = _repo(tmp_path)
    binding = _clean_binding()
    assert not any(gpd.gate_problems(binding, root).values())
    binding_path = _write_binding(tmp_path, binding)
    (root / "scripts" / "dispatch.py").unlink()

    result = gpd.gate_main(binding_path, root)

    assert result == 1
    assert capsys.readouterr().out.splitlines() == MISSING_DISPATCH_LINES


def test_gate_fails_when_a_bound_anchor_is_stale(tmp_path: Path, capsys):
    root = _repo(tmp_path)
    binding = _clean_binding()
    binding["processes"]["P1"]["states"].append(
        _state("stale", 1, "absent_anchor(", file="scripts/target.py")
    )
    binding_path = _write_binding(tmp_path, binding)

    result = gpd.gate_main(binding_path, root)

    assert result == 1
    assert capsys.readouterr().out.splitlines() == [
        "GATE INPUT stale: anchor 'absent_anchor(' is stale, absent from scripts/target.py"
    ]


def test_report_only_returns_zero_for_missing_dispatch_with_same_output(
    tmp_path: Path, capsys
):
    root = _repo(tmp_path)
    binding_path = _write_binding(tmp_path, _clean_binding())
    (root / "scripts" / "dispatch.py").unlink()

    result = gpd.gate_main(binding_path, root, report_only=True)

    assert result == 0
    assert capsys.readouterr().out.splitlines() == MISSING_DISPATCH_LINES


def test_report_only_returns_zero_for_stale_anchor_with_same_output(
    tmp_path: Path, capsys
):
    root = _repo(tmp_path)
    binding = _clean_binding()
    binding["processes"]["P1"]["states"].append(
        _state("stale", 1, "absent_anchor(", file="scripts/target.py")
    )
    binding_path = _write_binding(tmp_path, binding)

    result = gpd.gate_main(binding_path, root, report_only=True)

    assert result == 0
    assert capsys.readouterr().out.splitlines() == [
        "GATE INPUT stale: anchor 'absent_anchor(' is stale, absent from scripts/target.py"
    ]


def test_gate_returns_zero_and_prints_nothing_when_inputs_are_clean(
    tmp_path: Path, capsys
):
    root = _repo(tmp_path)
    binding_path = _write_binding(tmp_path, _clean_binding())

    result = gpd.gate_main(binding_path, root)

    assert result == 0
    assert capsys.readouterr().out == ""
