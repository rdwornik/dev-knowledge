"""Coverage for scripts/system_map.py -- the generated drill-down system map ([#781], lane C6).

The lane's Done-contract names three test clauses and this file carries each:

  * determinism -- the same tree yields a byte-identical map JSON
      -> test_the_same_tree_gives_byte_identical_json
  * a file the file-purpose graph cannot explain is rendered AS SUCH, not dropped
      -> test_a_file_nothing_explains_is_rendered_unexplained
  * a trigger-less organ is rendered DEAD, visibly, and is also listed separately
      -> test_a_trigger_less_organ_is_rendered_dead

plus the record clause (previous sha + added/removed nodes in a committed file) and the
grimp import edge. Every case runs against a SYNTHETIC git repo under tmp_path, so the
assertions test the generator's logic rather than today's contents of this repo.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import system_map as sm  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True, text=True)


_PRECOMMIT = """\
repos:
  - repo: local
    hooks:
      - id: live-gate
        name: live gate
        entry: uv run --locked python scripts/alpha.py
        language: system
        stages: [pre-commit]
      - id: sleeping-gate
        name: sleeping gate
        entry: uv run --locked python scripts/beta.py
        language: system
        stages: [manual]
"""


def _tree(tmp_path: Path) -> Path:
    """A minimal committed repo: two scripts (beta imports alpha), one command, one hook
    config with a live and a manual-only hook, and one ecosystem file nothing names."""
    root = tmp_path / "repo"
    _write(root / "scripts" / "alpha.py", '"""Alpha: the imported module."""\nVALUE = 1\n')
    _write(root / "scripts" / "beta.py",
           '"""Beta: imports alpha."""\nfrom scripts import alpha\n\nX = alpha.VALUE\n')
    _write(root / ".claude" / "commands" / "hello.md",
           "---\nname: hello\ndescription: say hello\n---\n\n# /hello\n")
    _write(root / ".pre-commit-config.yaml", _PRECOMMIT)
    _write(root / "ecosystem" / "stray.yaml", "nobody: names-me\n")
    _write(root / "tests" / "test_alpha.py", "def test_x():\n    assert True\n")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@t")
    _git(root, "config", "user.name", "t")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "init")
    return root


def test_the_same_tree_gives_byte_identical_json(tmp_path):
    root = _tree(tmp_path)
    first = sm.render_json(sm.build_map(root))
    second = sm.render_json(sm.build_map(root))
    assert first == second
    assert sm.map_sha(first) == sm.map_sha(second)
    assert len(sm.map_sha(first)) == 64


def test_a_file_nothing_explains_is_rendered_unexplained(tmp_path):
    root = _tree(tmp_path)
    data = sm.build_map(root)
    assert "ecosystem/stray.yaml" in data["unexplained"]
    leaf = data["files"]["ecosystem/stray.yaml"]
    assert leaf["explained"] is False
    assert leaf["purpose"] == sm.UNEXPLAINED
    # a process file is always a graph node, so it is NOT reported unexplained
    assert data["files"]["scripts/alpha.py"]["explained"] is True
    html = sm.render_html(data, sm.map_sha(sm.render_json(data)))
    assert "ecosystem/stray.yaml" in html
    assert sm.UNEXPLAINED in html


def test_a_trigger_less_organ_is_rendered_dead(tmp_path):
    root = _tree(tmp_path)
    data = sm.build_map(root)
    organs = {o["name"]: o for o in data["organs"]}
    assert organs["sleeping-gate"]["state"] == sm.DEAD
    assert organs["live-gate"]["state"] == sm.LIVE
    assert "organ:git-hook:sleeping-gate" in data["dead_organs"]
    assert "organ:git-hook:live-gate" not in data["dead_organs"]
    html = sm.render_html(data, sm.map_sha(sm.render_json(data)))
    # DEAD is rendered in the organ table AND in the separate DEAD list
    assert html.count('data-organ="organ:git-hook:sleeping-gate"') == 2
    assert 'class="dead"' in html


def test_grimp_import_edges_reach_the_leaf(tmp_path):
    root = _tree(tmp_path)
    data = sm.build_map(root)
    assert "scripts/alpha.py" in data["files"]["scripts/beta.py"]["imports"]
    assert "scripts/beta.py" in data["files"]["scripts/alpha.py"]["imported_by"]
    assert data["files"]["scripts/alpha.py"]["used"] is True
    assert data["files"]["scripts/alpha.py"]["tests"] == ["tests/test_alpha.py"]
    assert data["meta"]["grimp"]["modules"] >= 2


def test_the_html_is_static_and_self_contained(tmp_path):
    root = _tree(tmp_path)
    data = sm.build_map(root)
    html = sm.render_html(data, "0" * 64)
    assert "<script>" in html                      # inline expand/collapse
    assert "src=\"http" not in html and "href=\"http" not in html   # no CDN
    assert "0" * 64 in html


def test_the_record_keeps_the_previous_sha_and_a_node_diff(tmp_path):
    root = _tree(tmp_path)
    out = tmp_path / "out"
    record = tmp_path / "record.json"
    first = sm.write_outputs(root, out, record)
    assert first["previous_sha"] is None
    _write(root / "scripts" / "gamma.py", '"""Gamma."""\n')
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "gamma")
    second = sm.write_outputs(root, out, record)
    assert second["previous_sha"] == first["map_sha"]
    assert second["map_sha"] != first["map_sha"]
    assert "file:scripts/gamma.py" in second["diff"]["added"]
    assert second["diff"]["removed"] == []
    on_disk = json.loads(record.read_text(encoding="utf-8"))
    assert on_disk["map_sha"] == second["map_sha"]
    assert (out / sm.JSON_NAME).is_file() and (out / sm.HTML_NAME).is_file()


def test_an_unchanged_map_leaves_the_record_untouched(tmp_path):
    root = _tree(tmp_path)
    out = tmp_path / "out"
    record = tmp_path / "record.json"
    sm.write_outputs(root, out, record)
    before = record.read_bytes()
    again = sm.write_outputs(root, out, record)
    assert record.read_bytes() == before
    assert again["changed"] is False


def test_the_cli_prints_the_path_and_the_map_sha(tmp_path):
    root = _tree(tmp_path)
    out = tmp_path / "out"
    record = tmp_path / "record.json"
    result = CliRunner().invoke(sm.cli, ["build", "--repo-root", str(root),
                                         "--out-dir", str(out), "--record", str(record)])
    assert result.exit_code == 0, result.output
    sha = json.loads(record.read_text(encoding="utf-8"))["map_sha"]
    assert f"map_sha: {sha}" in result.output
    assert sm.HTML_NAME in result.output


def test_the_map_command_runs_the_generator():
    text = (_REPO_ROOT / ".claude" / "commands" / "map.md").read_text(encoding="utf-8")
    assert "scripts/system_map.py build" in text


def test_identical_trees_with_different_histories_give_identical_json(tmp_path):
    """Codex r1 HIGH: the map is a function of the TREE, not of the commit history. A per-file
    last-commit sha is history, so it is shown in the HTML and kept out of the hashed JSON."""
    one = _tree(tmp_path / "one")
    two = _tree(tmp_path / "two")
    _write(two / "scripts" / "alpha.py", '"""Alpha: an interim edit."""\nVALUE = 2\n')
    _git(two, "commit", "-q", "-am", "interim")
    _write(two / "scripts" / "alpha.py", '"""Alpha: the imported module."""\nVALUE = 1\n')
    _git(two, "commit", "-q", "-am", "revert interim")
    assert sm.render_json(sm.build_map(one)) == sm.render_json(sm.build_map(two))
    # the history is still shown on the page
    html = sm.render_html(sm.build_map(two), "0" * 64, sm.last_commits(two))
    head = subprocess.run(["git", "-C", str(two), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()
    assert head[:12] in html
