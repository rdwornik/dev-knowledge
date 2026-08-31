"""Tests for `gen_north_star` -- the NORTH STAR arc view.

What these pin is the DECLARED/DERIVED split, because that split is the whole design. An arc's
name and order are architect judgments and may change freely; its counts and member rows are facts
and must never be typed. A test that only checked "the file renders" would pass against a
hand-written roadmap, which is the artifact this generator exists to replace.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import gen_north_star as gns  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parents[1]


def _repo(tmp_path, rows):
    """A minimal tasks/ tree: `rows` is (id, status, theme, priority), manifest-referenced."""
    tasks = tmp_path / "tasks"
    tasks.mkdir(parents=True)
    nodes = []
    for i, (rid, status, theme, pri) in enumerate(rows):
        name = f"{rid}-row.md"
        (tasks / name).write_text(
            "---\n"
            f'id: "[#{rid}]"\n'
            f"title: row {rid}\n"
            f"status: {status}\n"
            f"priority: {pri}\n"
            f'theme: "{theme}"\n'
            "---\n\n"
            f"- [#{rid}] body\n",
            encoding="utf-8", newline="\n")
        nodes.append({"task": int(rid), "file": name})
    (tasks / "manifest.json").write_text(json.dumps({"nodes": nodes}), encoding="utf-8")
    return tmp_path


def test_counts_are_derived_from_tasks_not_typed(tmp_path):
    """The core property: change the tree, the numbers move with no edit to the generator."""
    theme = gns.ARCS[0]["themes"][0]
    repo = _repo(tmp_path, [("1", "open", theme, "P1"), ("2", "open", theme, "P2"),
                            ("3", "closed", theme, "P2")])
    body = gns.render(repo)
    assert "Open rows: **2** of 3 manifest-referenced" in body


def test_retired_allocation_records_are_NOT_counted(tmp_path):
    """The denominator bug this generator shipped with, pinned so it cannot return.

    `tasks/` keeps retired allocation records so a closed id is never re-issued (ADR-107 6.3).
    A bare glob counted them and produced 354 against `validate_backlog`'s 217 -- a generated
    view whose total disagrees with the repo's own validator is worse than no view.
    """
    theme = gns.ARCS[0]["themes"][0]
    repo = _repo(tmp_path, [("1", "open", theme, "P1")])
    (repo / "tasks" / "999-retired.md").write_text(
        '---\nid: "[#999]"\nstatus: closed\n---\n\n- [#999] retired\n',
        encoding="utf-8", newline="\n")
    body = gns.render(repo)
    assert "of 1 manifest-referenced" in body, "the unreferenced record was counted"


def test_deferred_rows_are_surfaced_separately(tmp_path):
    """Deferred is shown because a deferred BLOCKER is what [#624] exists about.

    A plan resting on a deferred row is a plan resting on nothing, and the failure mode is that
    `deferred` reads like `closed` at a glance and like `open` in a total.
    """
    theme = gns.ARCS[0]["themes"][0]
    repo = _repo(tmp_path, [("1", "open", theme, "P1"), ("2", "deferred", theme, "P2")])
    body = gns.render(repo)
    assert "**1 deferred**" in body
    assert "Deferred in scope:** 1" in body


def test_membership_is_by_theme_PREDICATE_so_a_new_row_appears_unedited(tmp_path):
    """A row filed into an arc's theme tomorrow shows up without touching this generator.

    The same reason [#383] was re-scoped onto a `kind:` selector rather than line ranges: a
    hand-listed id set is stale the moment someone files.
    """
    theme = gns.ARCS[0]["themes"][0]
    before = gns.render(_repo(tmp_path / "a", [("1", "open", theme, "P1")]))
    after = gns.render(_repo(tmp_path / "b", [("1", "open", theme, "P1"),
                                              ("2", "open", theme, "P1")]))
    assert "Open rows in scope:** 1" in before
    assert "Open rows in scope:** 2" in after


def test_every_declared_arc_carries_its_four_architect_fields():
    """The DECLARED half. An arc with no done-when or no starting contract is a heading."""
    assert gns.ARCS, "no arcs declared"
    for arc in gns.ARCS:
        for field in ("name", "themes", "blocked_by", "done_when", "contract"):
            assert arc.get(field), f"{arc.get('key')} is missing {field}"
        assert arc["themes"], f"{arc['key']} selects on nothing"


def test_the_committed_view_is_current():
    """`--check` is the freshness gate; a stale generated file is worse than none."""
    assert gns.main(["--check", "--repo-root", str(_REPO_ROOT)]) == 0
