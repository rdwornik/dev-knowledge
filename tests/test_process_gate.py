"""RED-first tests for the process binding's two-way coverage gate."""
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

def helper():
    helper_anchor()
"""


def _repo(tmp_path: Path, dispatch: str = DISPATCH) -> Path:
    root = tmp_path / "repo"
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "dispatch.py").write_text(dispatch, encoding="utf-8")
    (scripts / "target.py").write_text("target_anchor()\n", encoding="utf-8")
    return root


def _binding(
    states: list[dict] | None = None,
    transitions: list[dict] | None = None,
) -> dict:
    return {
        "schema": "process-binding/1",
        "processes": {
            "P1": {
                "states": states or [],
                "transitions": transitions or [],
                "retired": [],
            }
        },
    }


def _state(name: str, line: int | None = None, anchor: str = "target_anchor(") -> dict:
    state = {"id": f"S-{name}", "name": name}
    if line is not None:
        state["binding"] = {
            "code": {
                "file_line": f"scripts/dispatch.py:{line}",
                "anchor": anchor,
            }
        }
    return state


def _line(source: str, text: str) -> int:
    return next(i for i, line in enumerate(source.splitlines(), start=1) if text in line)


def _write_binding(tmp_path: Path, binding: dict) -> Path:
    path = tmp_path / "binding.yaml"
    path.write_text(yaml.safe_dump(binding, sort_keys=False), encoding="utf-8")
    return path


def test_gate_reports_unbound_state_and_transition_nodes(tmp_path: Path):
    root = _repo(tmp_path)
    binding = _binding(
        states=[{"id": "S02", "name": "unbound-state"}],
        transitions=[
            {
                "event": "emit",
                "source": "drafted",
                "target": "emitted",
                "guard": None,
            }
        ],
    )

    problems = gpd.gate_problems(binding, root)

    assert problems["unbound_nodes"] == [
        "state:unbound-state",
        "transition:emit:drafted->emitted",
    ]
    assert problems["unbound_entry_points"] == ["cli:launch", "def:launch_lane"]


def test_gate_reports_no_unbound_nodes_when_every_node_is_bound(tmp_path: Path):
    root = _repo(tmp_path)
    binding = _binding(
        states=[
            {
                "id": "S01",
                "name": "bound",
                "binding": {
                    "code": {
                        "file_line": "scripts/target.py:1",
                        "anchor": "target_anchor(",
                    }
                },
            },
            {
                "id": "S02",
                "name": "also-bound",
                "binding": {
                    "code": {
                        "file_line": "scripts/target.py:1",
                        "anchor": "target_anchor(",
                    }
                },
            },
        ],
        transitions=[
            {
                "event": "emit",
                "source": "drafted",
                "target": "emitted",
                "guard": None,
                "file_line": "scripts/target.py:1",
                "anchor": "target_anchor(",
            }
        ],
    )

    problems = gpd.gate_problems(binding, root)

    assert problems["unbound_nodes"] == []
    assert list(problems) == ["unbound_nodes", "unbound_entry_points"]


def test_gate_reports_dispatch_entry_point_without_resolved_anchor(tmp_path: Path):
    root = _repo(tmp_path)

    problems = gpd.gate_problems(_binding(), root)

    assert problems["unbound_entry_points"] == ["cli:launch", "def:launch_lane"]


def test_binding_inside_command_function_covers_cli_entry_point(tmp_path: Path):
    root = _repo(tmp_path)
    line = _line(DISPATCH, "launch_anchor()")
    binding = _binding(states=[_state("launch", line, "launch_anchor(")])

    problems = gpd.gate_problems(binding, root)

    assert problems["unbound_entry_points"] == ["def:launch_lane"]


def test_hole_does_not_bind_entry_point(tmp_path: Path):
    root = _repo(tmp_path)
    binding = _binding(states=[{"id": "S01", "name": "launch", "hole": "manual"}])

    problems = gpd.gate_problems(binding, root)

    assert problems["unbound_entry_points"] == ["cli:launch", "def:launch_lane"]


def test_binding_inside_launch_lane_covers_function_entry_point(tmp_path: Path):
    root = _repo(tmp_path)
    line = _line(DISPATCH, "lane_anchor()")
    binding = _binding(states=[_state("lane", line, "lane_anchor(")])

    problems = gpd.gate_problems(binding, root)

    assert problems["unbound_entry_points"] == ["cli:launch"]


def test_entry_points_include_decorated_command_and_top_level_launch_lane_only(
    tmp_path: Path,
):
    root = _repo(tmp_path)
    binding = _binding()

    assert gpd.entry_points(root) == ["cli:launch", "def:launch_lane"]
    assert gpd.gate_problems(binding, root)["unbound_entry_points"] == [
        "cli:launch",
        "def:launch_lane",
    ]


def test_entry_points_missing_dispatch_file_is_empty(tmp_path: Path):
    root = _repo(tmp_path)
    (root / "scripts" / "dispatch.py").unlink()
    binding = _binding()

    assert gpd.entry_points(root) == []
    assert gpd.gate_problems(binding, root)["unbound_entry_points"] == []


def test_gate_problem_lists_are_sorted(tmp_path: Path):
    root = _repo(tmp_path)
    binding = _binding(
        states=[
            {"id": "S02", "name": "zulu"},
            {"id": "S01", "name": "alpha"},
        ],
        transitions=[
            {
                "event": "z-event",
                "source": "z",
                "target": "zz",
                "guard": None,
            },
            {
                "event": "a-event",
                "source": "a",
                "target": "aa",
                "guard": None,
            },
        ],
    )

    problems = gpd.gate_problems(binding, root)

    assert problems["unbound_nodes"] == [
        "state:alpha",
        "state:zulu",
        "transition:a-event:a->aa",
        "transition:z-event:z->zz",
    ]
    assert problems["unbound_entry_points"] == ["cli:launch", "def:launch_lane"]


def test_gate_main_prints_unbound_lists_and_returns_one(tmp_path: Path, capsys):
    root = _repo(tmp_path)
    binding_path = _write_binding(
        tmp_path, _binding(states=[{"id": "S01", "name": "drafted"}])
    )

    result = gpd.gate_main(binding_path, root, report_only=False)

    assert result == 1
    assert capsys.readouterr().out.splitlines() == [
        "UNBOUND NODE state:drafted",
        "UNBOUND ENTRY cli:launch",
        "UNBOUND ENTRY def:launch_lane",
    ]


def test_gate_main_returns_zero_when_clean(tmp_path: Path, capsys):
    root = _repo(tmp_path)
    line = _line(DISPATCH, "launch_anchor()")
    lane_line = _line(DISPATCH, "lane_anchor()")
    binding = _binding(
        states=[
            _state("launch", line, "launch_anchor("),
            _state("lane", lane_line, "lane_anchor("),
        ]
    )
    binding_path = _write_binding(tmp_path, binding)

    result = gpd.gate_main(binding_path, root, report_only=False)

    assert result == 0
    assert capsys.readouterr().out == ""


def test_gate_main_report_only_returns_zero_but_prints_all_problems(
    tmp_path: Path, capsys
):
    root = _repo(tmp_path)
    binding_path = _write_binding(
        tmp_path, _binding(states=[{"id": "S01", "name": "drafted"}])
    )

    result = gpd.gate_main(binding_path, root, report_only=True)

    assert result == 0
    assert capsys.readouterr().out.splitlines() == [
        "UNBOUND NODE state:drafted",
        "UNBOUND ENTRY cli:launch",
        "UNBOUND ENTRY def:launch_lane",
    ]
