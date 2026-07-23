"""Tests for scripts/gen_intake_index.py (#307 status-grouped intake index).

Firing tests: frontmatter parse, status grouping in canonical lifecycle order, the loud
OTHER bucket for unknown states, marker-splice (never overwrites the doctrine sections),
the regen-and-diff drift check, and the "moves no file" contract.
"""

import importlib.util
import sys
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "scripts" / "gen_intake_index.py"


def _load():
    spec = importlib.util.spec_from_file_location("gen_intake_index", _P)
    module = importlib.util.module_from_spec(spec)
    sys.modules["gen_intake_index"] = module
    spec.loader.exec_module(module)
    return module


gi = _load()


def _doc(status: str, intake_id: str, title: str) -> str:
    return (f"---\nintake-id: {intake_id}\nstatus: {status}\norigin: test\n---\n\n"
            f"# {title}\n\nbody\n")


def _make_intake_dir(tmp_path: Path, docs: dict[str, str]) -> Path:
    d = tmp_path / "intake"
    d.mkdir()
    for name, content in docs.items():
        (d / name).write_text(content, encoding="utf-8")
    return d


# --- frontmatter + collect ---------------------------------------------------

def test_parse_frontmatter_extracts_status_and_id():
    fm = gi._parse_frontmatter(_doc("SEED", "7", "A thing"))
    assert fm["status"] == "SEED"
    assert fm["intake-id"] == "7"


def test_parse_frontmatter_absent_is_empty():
    assert gi._parse_frontmatter("# no frontmatter\n") == {}


def test_collect_excludes_readme_and_reads_status(tmp_path):
    d = _make_intake_dir(tmp_path, {
        "2026-07-06-a.md": _doc("CONSUMED", "1", "Alpha"),
        "2026-07-07-b.md": _doc("SEED", "2", "Beta"),
        "README.md": "# readme\n",
    })
    rows = gi.collect_intakes(d)
    names = {r[2] for r in rows}
    assert names == {"2026-07-06-a.md", "2026-07-07-b.md"}
    statuses = {r[2]: r[0] for r in rows}
    assert statuses["2026-07-06-a.md"] == "CONSUMED"


# --- render: grouping, order, counts, OTHER bucket ---------------------------

def test_render_groups_in_canonical_lifecycle_order(tmp_path):
    d = _make_intake_dir(tmp_path, {
        "c.md": _doc("CONSUMED", "3", "Cee"),
        "s.md": _doc("SEED", "1", "Ess"),
        "r.md": _doc("REJECTED", "2", "Arr"),
    })
    out = gi.render_contents(d)
    # SEED must render before CONSUMED before REJECTED regardless of file order.
    assert out.index("### SEED") < out.index("### CONSUMED") < out.index("### REJECTED")
    assert "**3 intake documents.**" in out
    assert "### SEED (1)" in out
    assert "[#1](s.md) — Ess" in out


def test_status_order_is_the_ruled_enum():
    # The [#398]-deployed enum (2026-07-19 ruling, SUPPLEMENT.md:68-70) — the
    # gate-readable canon a status-coupled validator will consume.
    assert gi._STATUS_ORDER == (
        "SEED", "DRAFT", "READY", "ACCEPTED", "CONSUMED", "SUPERSEDED", "REJECTED")


def test_render_groups_new_states_in_lifecycle_order(tmp_path):
    d = _make_intake_dir(tmp_path, {
        "u.md": _doc("SUPERSEDED", "2", "Sup"),
        "a.md": _doc("ACCEPTED", "1", "Acc"),
        "y.md": _doc("READY", "3", "Red"),
    })
    out = gi.render_contents(d)
    # READY < ACCEPTED < SUPERSEDED, and none of the ruled states leaks into OTHER.
    assert out.index("### READY") < out.index("### ACCEPTED") < out.index("### SUPERSEDED")
    assert "### OTHER" not in out


def test_render_unknown_status_lands_in_loud_other_bucket(tmp_path):
    d = _make_intake_dir(tmp_path, {"x.md": _doc("BOGUS", "9", "Weird")})
    out = gi.render_contents(d)
    assert "### OTHER (1)" in out
    assert "[#9](x.md) — Weird" in out  # NOT dropped


def test_render_is_deterministic(tmp_path):
    d = _make_intake_dir(tmp_path, {
        "a.md": _doc("SEED", "2", "A"), "b.md": _doc("SEED", "1", "B")})
    assert gi.render_contents(d) == gi.render_contents(d)
    out = gi.render_contents(d)
    # within a group, sorted by numeric intake-id: #1 before #2
    assert out.index("[#1](b.md)") < out.index("[#2](a.md)")


# --- splice: preserves doctrine, drift check, moves no file ------------------

_README = ("# docs/intake/\n\nintro\n\n"
           "## Contents\n\n"
           f"{gi._START_MARKER}\n(stale)\n{gi._END_MARKER}\n\n"
           "## 1. What this folder is\n\ndoctrine stays\n")


def test_splice_replaces_only_between_markers():
    spliced = gi._splice(_README, "FRESH BLOCK\n")
    assert "FRESH BLOCK" in spliced
    assert "(stale)" not in spliced
    assert "## 1. What this folder is" in spliced  # doctrine preserved
    assert "doctrine stays" in spliced


def test_splice_raises_without_markers():
    import pytest
    with pytest.raises(RuntimeError):
        gi._splice("# no markers here\n", "x\n")


def test_cmd_check_and_write_roundtrip(tmp_path, monkeypatch):
    d = _make_intake_dir(tmp_path, {"s.md": _doc("SEED", "1", "Ess")})
    readme = d / "README.md"
    readme.write_text(_README, encoding="utf-8")
    monkeypatch.setattr(gi, "_INTAKE_DIR", d)
    monkeypatch.setattr(gi, "_TARGET", readme)
    monkeypatch.setattr(gi, "_REPO_ROOT", tmp_path)

    assert gi._cmd_check() == 1          # (stale) block drifts from disk
    assert gi._cmd_write() == 0          # regenerate
    assert gi._cmd_check() == 0          # now clean
    # moved no file: the intake doc is untouched, doctrine section survives
    body = readme.read_text(encoding="utf-8")
    assert "## 1. What this folder is" in body
    assert (d / "s.md").exists()
    assert "[#1](s.md) — Ess" in body


def test_cmd_check_missing_markers_is_2(tmp_path, monkeypatch):
    d = _make_intake_dir(tmp_path, {"s.md": _doc("SEED", "1", "Ess")})
    readme = d / "README.md"
    readme.write_text("# no markers\n", encoding="utf-8")
    monkeypatch.setattr(gi, "_INTAKE_DIR", d)
    monkeypatch.setattr(gi, "_TARGET", readme)
    monkeypatch.setattr(gi, "_REPO_ROOT", tmp_path)
    assert gi._cmd_check() == 2


# --- codex-review 2026-07-11 hardening ---------------------------------------

def test_parse_frontmatter_unterminated_is_empty():
    # `---` with no closing `---` is INVALID -> empty (not silently parsed from the body).
    assert gi._parse_frontmatter("---\nstatus: SEED\nintake-id: 3\n\n# body, no close\n") == {}


def test_missing_intake_id_renders_loud_label(tmp_path):
    # A doc lacking intake-id must render a LOUD MISSING-ID label, never a `[2026]` fragment.
    d = _make_intake_dir(tmp_path, {"2026-07-07-x.md": "---\nstatus: SEED\n---\n\n# X\n"})
    out = gi.render_contents(d)
    assert "MISSING-ID" in out
    assert "[2026]" not in out


def test_splice_rejects_duplicate_markers():
    import pytest
    dup = f"# t\n{gi._START_MARKER}\na\n{gi._END_MARKER}\n{gi._START_MARKER}\nb\n{gi._END_MARKER}\n"
    with pytest.raises(RuntimeError):
        gi._splice(dup, "x\n")


def test_splice_rejects_reversed_markers():
    import pytest
    rev = f"# t\n{gi._END_MARKER}\nmid\n{gi._START_MARKER}\n"
    with pytest.raises(RuntimeError):
        gi._splice(rev, "x\n")
