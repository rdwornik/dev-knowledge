"""RED-first tests for process-binding source anchors and diagram checks."""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_process_diagrams as gpd  # noqa: E402


def _repo(tmp_path: Path, source: str = "first_call()\nunique_marker()\n") -> Path:
    root = tmp_path / "repo"
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "target.py").write_text(source, encoding="utf-8")
    (scripts / "dispatch.py").write_text("def dispatch():\n    pass\n", encoding="utf-8")
    return root


def _state_binding(
    name: str = "drafted",
    file_line: str = "scripts/target.py:2",
    anchor: str = "unique_marker(",
) -> dict:
    return {
        "schema": "process-binding/1",
        "processes": {
            "P1": {
                "states": [
                    {
                        "id": "S01",
                        "name": name,
                        "binding": {
                            "code": {"file_line": file_line, "anchor": anchor}
                        },
                    }
                ],
                "transitions": [],
                "retired": [],
            }
        },
    }


def test_find_anchor_returns_all_one_based_matching_lines_and_empty_for_missing(
    tmp_path: Path,
):
    root = _repo(tmp_path, "same_marker()\nother()\nsame_marker()\n")
    binding = _state_binding(
        file_line="scripts/target.py:1", anchor="same_marker("
    )

    assert gpd.find_anchor("scripts/target.py", "same_marker(", root) == [1, 3]
    assert gpd.find_anchor("scripts/target.py", "absent(", root) == []
    assert gpd.find_anchor("scripts/missing.py", "same_marker(", root) == []
    assert gpd.anchor_problems(binding, root) == []


def test_anchor_problems_accepts_exact_and_unique_drifted_anchors(tmp_path: Path):
    root = _repo(tmp_path)

    assert gpd.anchor_problems(_state_binding(), root) == []
    assert gpd.anchor_problems(
        _state_binding(file_line="scripts/target.py:1"), root
    ) == []


def test_anchor_problems_reports_absent_anchor_and_names_state_and_file(tmp_path: Path):
    root = _repo(tmp_path)

    problems = gpd.anchor_problems(_state_binding(anchor="not_present("), root)

    assert len(problems) == 1
    assert "drafted" in problems[0]
    assert "scripts/target.py" in problems[0]


def test_anchor_problems_reports_missing_file(tmp_path: Path):
    root = _repo(tmp_path)
    binding = _state_binding(file_line="scripts/missing.py:1")

    problems = gpd.anchor_problems(binding, root)

    assert len(problems) == 1
    assert "drafted" in problems[0]
    assert "scripts/missing.py" in problems[0]


def test_anchor_problems_reports_ambiguous_anchor_when_hint_matches_neither(
    tmp_path: Path,
):
    root = _repo(tmp_path, "repeat_marker()\nother()\nrepeat_marker()\n")
    binding = _state_binding(
        file_line="scripts/target.py:2", anchor="repeat_marker("
    )

    problems = gpd.anchor_problems(binding, root)

    assert len(problems) == 1
    assert "drafted" in problems[0]
    assert "scripts/target.py" in problems[0]


def test_anchor_problems_accepts_ambiguous_anchor_when_hint_is_a_match(tmp_path: Path):
    root = _repo(tmp_path, "repeat_marker()\nother()\nrepeat_marker()\n")
    binding = _state_binding(
        file_line="scripts/target.py:3", anchor="repeat_marker("
    )

    assert gpd.anchor_problems(binding, root) == []


def test_hole_only_state_has_no_anchor_problem(tmp_path: Path):
    root = _repo(tmp_path)
    binding = {
        "schema": "process-binding/1",
        "processes": {
            "P1": {
                "states": [{"id": "S01", "name": "drafted", "hole": "operator step"}],
                "transitions": [],
                "retired": [],
            }
        },
    }

    assert gpd.anchor_problems(binding, root) == []


def test_anchor_problems_checks_transition_bindings(tmp_path: Path):
    root = _repo(tmp_path)
    binding = {
        "schema": "process-binding/1",
        "processes": {
            "P1": {
                "states": [],
                "transitions": [
                    {
                        "event": "emit",
                        "source": "drafted",
                        "target": "emitted",
                        "guard": None,
                        "file_line": "scripts/target.py:1",
                        "anchor": "missing_transition_anchor(",
                    }
                ],
                "retired": [],
            }
        },
    }

    problems = gpd.anchor_problems(binding, root)

    assert len(problems) == 1
    assert "emit drafted->emitted" in problems[0]
    assert "scripts/target.py" in problems[0]


def test_rebind_fixes_drift_is_idempotent_and_changes_only_file_line(tmp_path: Path):
    root = _repo(tmp_path)
    binding_path = tmp_path / "binding.yaml"
    before = (
        b"schema: process-binding/1\n"
        b"processes:\n"
        b"  P1:\n"
        b"    states:\n"
        b"    - id: S01\n"
        b"      name: drafted\n"
        b"      binding:\n"
        b"        code:\n"
        b"          file_line: scripts/target.py:1\n"
        b'          anchor: "unique_marker("\n'
        b"    transitions: []\n"
        b"    retired: []\n"
        b"diagram_mermaid: |-\n"
        b"  stateDiagram-v2\n"
    )
    binding_path.write_bytes(before)

    assert gpd.rebind(binding_path, root) is True

    expected = before.replace(
        b"file_line: scripts/target.py:1", b"file_line: scripts/target.py:2"
    )
    assert binding_path.read_bytes() == expected
    assert gpd.rebind(binding_path, root) is False


def test_rebind_uses_nearest_match_when_anchor_is_ambiguous(tmp_path: Path):
    root = _repo(tmp_path, "repeat_marker()\nother()\nrepeat_marker()\n")
    binding_path = tmp_path / "binding.yaml"
    binding_path.write_text(
        "schema: process-binding/1\n"
        "processes:\n"
        "  P1:\n"
        "    states:\n"
        "    - id: S01\n"
        "      name: drafted\n"
        "      binding:\n"
        "        code:\n"
        "          file_line: scripts/target.py:4\n"
        '          anchor: "repeat_marker("\n'
        "    transitions: []\n"
        "    retired: []\n",
        encoding="utf-8",
    )

    assert gpd.rebind(binding_path, root) is True
    assert "file_line: scripts/target.py:3" in binding_path.read_text(encoding="utf-8")


def test_rebind_preserves_crlf_line_endings(tmp_path: Path):
    root = _repo(tmp_path)
    binding_path = tmp_path / "binding-crlf.yaml"
    before = (
        b"schema: process-binding/1\r\n"
        b"processes:\r\n"
        b"  P1:\r\n"
        b"    states:\r\n"
        b"    - id: S01\r\n"
        b"      name: drafted\r\n"
        b"      binding:\r\n"
        b"        code:\r\n"
        b"          file_line: scripts/target.py:1\r\n"
        b'          anchor: "unique_marker("\r\n'
        b"    transitions: []\r\n"
        b"    retired: []\r\n"
        b"diagram_mermaid: |-\r\n"
        b"  stateDiagram-v2\r\n"
    )
    binding_path.write_bytes(before)

    assert gpd.rebind(binding_path, root) is True

    after = binding_path.read_bytes()
    assert after == before.replace(
        b"file_line: scripts/target.py:1", b"file_line: scripts/target.py:2"
    )
    assert b"\r\n" in after
    assert b"\n" not in after.replace(b"\r\n", b"")


def test_rebind_raises_value_error_for_stale_anchor_and_names_node(tmp_path: Path):
    root = _repo(tmp_path)
    binding_path = tmp_path / "binding.yaml"
    binding_path.write_text(
        "schema: process-binding/1\n"
        "processes:\n"
        "  P1:\n"
        "    states:\n"
        "    - id: S01\n"
        "      name: drafted\n"
        "      binding:\n"
        "        code:\n"
        "          file_line: scripts/target.py:1\n"
        '          anchor: "missing_marker("\n'
        "    transitions: []\n"
        "    retired: []\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="drafted"):
        gpd.rebind(binding_path, root)


def _copy_real_binding(tmp_path: Path) -> Path:
    _repo(tmp_path)
    binding_path = tmp_path / "process-binding.yaml"
    shutil.copyfile(
        Path(gpd.REPO) / "ecosystem" / "process-binding.yaml", binding_path
    )
    return binding_path


def test_check_diagram_accepts_rebound_copy_of_current_binding(tmp_path: Path):
    binding_path = _copy_real_binding(tmp_path)

    gpd.rebind(binding_path, gpd.REPO)

    assert gpd.check_diagram(binding_path, gpd.REPO) == 0


def test_check_diagram_rejects_changed_mermaid_character(tmp_path: Path):
    binding_path = _copy_real_binding(tmp_path)
    gpd.rebind(binding_path, gpd.REPO)
    lines = binding_path.read_bytes().splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.startswith(b"diagram_mermaid:"))
    for i in range(start + 1, len(lines)):
        stripped = lines[i].lstrip()
        if stripped.strip():
            offset = len(lines[i]) - len(stripped)
            replacement = b"x" if lines[i][offset:offset + 1] != b"x" else b"y"
            lines[i] = lines[i][:offset] + replacement + lines[i][offset + 1:]
            break
    binding_path.write_bytes(b"".join(lines))

    assert gpd.check_diagram(binding_path, gpd.REPO) == 1


def test_check_diagram_rejects_stale_anchor(tmp_path: Path):
    binding_path = _copy_real_binding(tmp_path)
    gpd.rebind(binding_path, gpd.REPO)
    lines = binding_path.read_bytes().splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.lstrip().startswith(b"anchor:"):
            ending = b"\r\n" if line.endswith(b"\r\n") else b"\n"
            indent = line[: len(line) - len(line.lstrip())]
            lines[i] = indent + b"anchor: 'def anchor_that_does_not_exist('" + ending
            break
    binding_path.write_bytes(b"".join(lines))

    assert gpd.check_diagram(binding_path, gpd.REPO) == 1
