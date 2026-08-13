"""Tests for scripts/validate_landing_predicate.py — [#513] landing-predicate scanner.

A read-only Layer-2 validator: reads every `landed:` predicate declared in a STANDING_RULINGS-
shaped register (a fenced ```landed``` block per entry, one `site:` line per location) and
reports, per entry, whether its declared sites agree. MIXED = a propagation gap, the class this
row exists to surface — fixing one found site repairs the instance, not the class.
"""
from __future__ import annotations

from pathlib import Path

import validate_landing_predicate as vlp  # noqa: E402


# --- parse_landed_entries ----------------------------------------------------

def test_parse_landed_entries_associates_block_with_nearest_preceding_heading():
    text = """
### F2 · names, paths and identifiers derive from validators and enums

Some unrelated prose with no block of its own.

- **Expiry:** blah

### X-1 · a seeded ruling

prose describing the ruling

```landed
site: scripts/a.py | pattern: FOO
site: scripts/b.py | pattern: BAR
```

- **Expiry:** none
"""
    entries = vlp.parse_landed_entries(text)
    assert entries == [("X-1", "a seeded ruling", [("scripts/a.py", "FOO"), ("scripts/b.py", "BAR")])]


def test_parse_landed_entries_ignores_non_landed_fences():
    text = """
### X-2 · not a real declaration

```landed-shape
site: scripts/a.py | pattern: FOO
```

```python
site: scripts/a.py | pattern: FOO
```
"""
    assert vlp.parse_landed_entries(text) == []


def test_parse_landed_entries_multiple_entries_in_one_register():
    text = """
### A-1 · first

```landed
site: scripts/a.py | pattern: FOO
site: scripts/b.py | pattern: FOO
```

### A-2 · second

```landed
site: scripts/c.py | pattern: BAR
site: scripts/d.py | pattern: BAR
```
"""
    entries = vlp.parse_landed_entries(text)
    assert [e[0] for e in entries] == ["A-1", "A-2"]


# --- scan() — the seed test, both directions (row clause (c)) ---------------

def _write(root: Path, rel: str, content: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _register(sites: list[tuple[str, str]]) -> str:
    lines = "\n".join(f"site: {p} | pattern: {pat}" for p, pat in sites)
    return f"""
### SEED-1 · a half-landed adoption, seeded for the test

```landed
{lines}
```

- **Expiry:** test-only
"""


def test_scan_fires_red_on_a_half_landed_seed(tmp_path: Path):
    """RED: one site has adopted the ruling, the other has not — MIXED."""
    _write(tmp_path, "scripts/adopted.py", "from markdown_it import MarkdownIt\n")
    _write(tmp_path, "scripts/not_adopted.py", "import re\n")
    reg = tmp_path / "STANDING_RULINGS.md"
    reg.write_text(
        _register([("scripts/adopted.py", "from markdown_it import MarkdownIt"),
                    ("scripts/not_adopted.py", "from markdown_it import MarkdownIt")]),
        encoding="utf-8",
    )
    entries = vlp.scan(tmp_path, register=reg)
    assert len(entries) == 1
    assert entries[0].ruling_id == "SEED-1"
    assert entries[0].mixed is True


def test_scan_goes_green_once_the_seed_is_conformed(tmp_path: Path):
    """GREEN direction 1: the un-adopted site is fixed so both sites now agree."""
    _write(tmp_path, "scripts/adopted.py", "from markdown_it import MarkdownIt\n")
    _write(tmp_path, "scripts/not_adopted.py", "from markdown_it import MarkdownIt\n")  # conformed
    reg = tmp_path / "STANDING_RULINGS.md"
    reg.write_text(
        _register([("scripts/adopted.py", "from markdown_it import MarkdownIt"),
                    ("scripts/not_adopted.py", "from markdown_it import MarkdownIt")]),
        encoding="utf-8",
    )
    entries = vlp.scan(tmp_path, register=reg)
    assert len(entries) == 1
    assert entries[0].mixed is False


def test_scan_reports_a_missing_site_file_as_error_not_a_silent_boolean(tmp_path: Path):
    _write(tmp_path, "scripts/adopted.py", "from markdown_it import MarkdownIt\n")
    reg = tmp_path / "STANDING_RULINGS.md"
    reg.write_text(
        _register([("scripts/adopted.py", "from markdown_it import MarkdownIt"),
                    ("scripts/does_not_exist.py", "whatever")]),
        encoding="utf-8",
    )
    entries = vlp.scan(tmp_path, register=reg)
    assert len(entries) == 1
    assert len(entries[0].errors) == 1
    assert entries[0].errors[0].path == "scripts/does_not_exist.py"
    # a missing site is not folded into the mixed boolean as either True or False
    assert entries[0].mixed is False


def test_scan_is_a_hub_only_no_op_when_the_register_is_absent(tmp_path: Path):
    assert vlp.scan(tmp_path) == []


def test_scan_single_site_entry_is_never_mixed(tmp_path: Path):
    """An entry naming exactly one site cannot disagree with itself — not a propagation gap
    by this row's own definition (a gap needs >=2 sites in disagreement)."""
    _write(tmp_path, "scripts/only.py", "anything\n")
    reg = tmp_path / "STANDING_RULINGS.md"
    reg.write_text(_register([("scripts/only.py", "NOT_PRESENT")]), encoding="utf-8")
    entries = vlp.scan(tmp_path, register=reg)
    assert entries[0].mixed is False


def test_main_cli_exits_nonzero_on_a_mixed_register(tmp_path: Path, capsys, monkeypatch):
    _write(tmp_path, "scripts/adopted.py", "from markdown_it import MarkdownIt\n")
    _write(tmp_path, "scripts/not_adopted.py", "import re\n")
    reg = tmp_path / "protocols" / "STANDING_RULINGS.md"
    reg.parent.mkdir(parents=True)
    reg.write_text(
        _register([("scripts/adopted.py", "from markdown_it import MarkdownIt"),
                    ("scripts/not_adopted.py", "from markdown_it import MarkdownIt")]),
        encoding="utf-8",
    )
    monkeypatch.setattr(vlp, "_REPO_ROOT", tmp_path)
    assert vlp.main([]) == 1
    out = capsys.readouterr().out
    assert "MIXED" in out


# --- N-3 / L19: the organ's own first natural test case (live repo) ---------

def test_l19_dispatch_doctrine_site_reports_landed_on_the_live_repo():
    """[#513] scope addition 2: PLAYBOOK.md Ch8's dispatch-alias paragraph (night-2 lesson
    L19) is the organ's first natural test case, run over the REAL repo -- not a synthetic
    fixture. The repair landed at `10822b09` (2026-08-12, already on `main`, before this
    lane started); this asserts the organ reads the real STANDING_RULINGS.md N-3 entry and
    reports the real PLAYBOOK.md site as landed."""
    repo_root = Path(__file__).resolve().parents[1]
    entries = vlp.scan(repo_root)
    n3 = next((e for e in entries if e.ruling_id == "N-3"), None)
    assert n3 is not None, "N-3 (the L19 dispatch-doctrine ruling) is not declared"
    assert n3.mixed is False
    assert not n3.errors
    assert all(s.landed is True for s in n3.sites)
