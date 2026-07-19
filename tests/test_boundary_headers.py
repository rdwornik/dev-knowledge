"""Tests for scripts/boundary_headers.py (reader-visible boundary headers).

The point of this module is that the boundary has ONE vocabulary. The machine markers
(`<!-- methodology:start ... owner=hub|repo -->`) are the single source of truth; the
reader-visible headers and the .vscode background decoration are both DERIVED from them.
These tests hold that invariant from three directions:

  * generator units      -- headers are a pure function of the marker attributes
  * placement contract   -- headers never enter a region body (byte-match with
                            templates/claude-regions/ survives)
  * decoration coupling  -- the .vscode regexes select exactly the parsed marker regions,
                            so the editor cannot paint a boundary the parser disagrees with
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_P = _ROOT / "scripts" / "boundary_headers.py"


def _load():
    spec = importlib.util.spec_from_file_location("boundary_headers", _P)
    module = importlib.util.module_from_spec(spec)
    sys.modules["boundary_headers"] = module
    spec.loader.exec_module(module)
    return module


bh = _load()


# ---------------------------------------------------------------- generator units

def test_header_is_a_pure_function_of_the_marker_attributes():
    assert bh.header_for("first-read", "hub").startswith("> **[HUB - methodology]**")
    assert "`first-read`" in bh.header_for("first-read", "hub")
    assert bh.header_for("repo-identity", "repo").startswith("> **[REPO - local]**")
    assert "`repo-identity`" in bh.header_for("repo-identity", "repo")


def test_hub_and_repo_headers_are_visually_distinct():
    assert bh.header_for("x", "hub") != bh.header_for("x", "repo")


_SAMPLE = (
    "# T\n\n"
    "<!-- methodology:start id=alpha owner=hub -->\n"
    "hub body\n"
    "<!-- methodology:end id=alpha -->\n\n"
    "<!-- methodology:start id=beta owner=repo -->\n"
    "repo body\n"
    "<!-- methodology:end id=beta -->\n"
)


def test_apply_headers_inserts_one_header_per_start_marker():
    out = bh.apply_headers(_SAMPLE)
    assert out.count("> **[HUB - methodology]** region `alpha`") == 1
    assert out.count("> **[REPO - local]** region `beta`") == 1


def test_apply_headers_is_idempotent():
    once = bh.apply_headers(_SAMPLE)
    assert bh.apply_headers(once) == once


def test_regeneration_repairs_a_hand_edited_header():
    """A hand-edited header is REPLACED -- markers win, prose does not."""
    tampered = bh.apply_headers(_SAMPLE).replace(
        "> **[HUB - methodology]** region `alpha`",
        "> **[HUB - methodology]** region `WRONG-ID`")
    assert bh.apply_headers(tampered) == bh.apply_headers(_SAMPLE)


def test_flipping_a_marker_owner_flips_the_header():
    """The anti-drift property: the header cannot disagree with its marker."""
    flipped = _SAMPLE.replace("id=alpha owner=hub", "id=alpha owner=repo")
    out = bh.apply_headers(flipped)
    assert "> **[REPO - local]** region `alpha`" in out
    assert "> **[HUB - methodology]** region `alpha`" not in out


def test_unmarked_file_is_untouched():
    plain = "# Nothing\n\njust prose\n"
    assert bh.apply_headers(plain) == plain
    assert not bh.has_markers(plain)


def test_is_fully_headed_detects_a_missing_header():
    assert not bh.is_fully_headed(_SAMPLE)
    assert bh.is_fully_headed(bh.apply_headers(_SAMPLE))


# ---------------------------------------------------------------- live-tree state

def test_live_tree_governed_files_are_discovered():
    govs = [p.name for p in bh.discover_governed(_ROOT)]
    assert "CLAUDE.md" in govs, "CLAUDE.md carries markers and must be governed"


def test_live_tree_coverage_is_complete():
    reports = bh.inspect(_ROOT)
    unheaded = [r.rel for r in reports if not r.headed]
    assert not unheaded, f"governed files missing reader-visible headers: {unheaded}"


def test_live_tree_headers_match_markers():
    """Regen-and-diff: the gate form. Fails if headers drift from markers."""
    drifted = [r.rel for r in bh.inspect(_ROOT) if r.drifted]
    assert not drifted, f"headers stale vs markers: {drifted}"


def test_live_tree_markers_parse_without_warnings():
    for rep in bh.inspect(_ROOT):
        assert not rep.warnings, f"{rep.rel}: {rep.warnings}"


# ------------------------------------------------------- placement contract

def test_headers_stay_outside_region_bodies():
    """A header must never land inside a region -- that is what preserves the
    byte-match between CLAUDE.md owner=hub regions and templates/claude-regions/."""
    from boundary_report import parse_regions
    regions, _ = parse_regions((_ROOT / "CLAUDE.md").read_text(encoding="utf-8"))
    assert regions, "CLAUDE.md must carry regions"
    for r in regions:
        assert not any(bh.is_generated_header(ln) for ln in r.body.splitlines()), \
            f"generated header leaked into region body {r.id}"


def test_hub_region_bodies_still_byte_match_the_templates():
    """The v2.39/v2.42 discipline: owner=hub bodies are byte-identical to their extracts."""
    from boundary_report import parse_regions
    regions, _ = parse_regions((_ROOT / "CLAUDE.md").read_text(encoding="utf-8"))
    tpl = _ROOT / "templates" / "claude-regions"
    checked = 0
    for r in regions:
        if r.owner != "hub":
            continue
        extract = tpl / f"{r.id}.md"
        if not extract.exists():
            pytest.fail(f"owner=hub region {r.id} has no template extract")
        assert extract.read_text(encoding="utf-8").strip() == r.body, \
            f"owner=hub region {r.id} drifted from its template extract"
        checked += 1
    assert checked == 8, f"expected 8 hub region extracts, checked {checked}"


# --------------------------------------------------- decoration coupling

def _vscode_regexes():
    cfg = json.loads((_ROOT / ".vscode" / "settings.json").read_text(encoding="utf-8"))
    return cfg["highlight.regexes"], cfg.get("highlight.regexFlags", "gm")


def test_vscode_declares_a_pattern_for_each_owner():
    regexes, flags = _vscode_regexes()
    assert "m" in flags, "line anchors require the multiline flag"
    owners = sorted("hub" if "owner=hub" in p else "repo" for p in regexes)
    assert owners == ["hub", "repo"], f"expected one pattern per owner, got {owners}"


def test_vscode_decoration_selects_exactly_the_parsed_marker_regions():
    """The two-vocabularies guard.

    The editor decoration and the marker parser must agree on WHICH lines are hub and
    which are repo. If someone re-words a .vscode regex so it stops tracking the marker
    vocabulary, this fails.
    """
    from boundary_report import parse_regions
    text = (_ROOT / "CLAUDE.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    regions, _ = parse_regions(text)
    expected = {"hub": sum(1 for r in regions if r.owner == "hub"),
                "repo": sum(1 for r in regions if r.owner == "repo")}

    regexes, _flags = _vscode_regexes()
    painted: list[tuple[int, int, str]] = []
    for pattern in regexes:
        owner = "hub" if "owner=hub" in pattern else "repo"
        for m in re.finditer(pattern, text, re.M):
            start = text.count("\n", 0, m.start())
            painted.append((start, start + m.group(0).count("\n"), owner))

    got = {"hub": sum(1 for p in painted if p[2] == "hub"),
           "repo": sum(1 for p in painted if p[2] == "repo")}
    assert got == expected, f"decoration painted {got}, markers say {expected}"

    painted.sort()
    for (s1, e1, _o1), (s2, _e2, _o2) in zip(painted, painted[1:]):
        assert e1 < s2, f"decoration bands overlap at lines {s1}-{e1} / {s2}-"


def test_vscode_bands_start_at_the_generated_header():
    """Each painted band opens on the generated header, so the reader sees the label
    and the shaded body as one block."""
    text = (_ROOT / "CLAUDE.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    regexes, _flags = _vscode_regexes()
    n = 0
    for pattern in regexes:
        for m in re.finditer(pattern, text, re.M):
            assert bh.is_generated_header(m.group(0).splitlines()[0]), \
                f"band does not open on a generated header: {m.group(0)[:60]!r}"
            n += 1
    assert n == 15, f"expected 15 painted regions, found {n}"


def test_vscode_is_scoped_to_governed_surfaces():
    regexes, _ = _vscode_regexes()
    for pattern, spec in regexes.items():
        assert "CLAUDE" in spec.get("filterFileRegex", ""), \
            "decoration must be scoped, not applied to every file"


def test_vscode_uses_navy_for_hub_and_grey_for_repo():
    regexes, _ = _vscode_regexes()
    for pattern, spec in regexes.items():
        bg = spec["decorations"][0]["backgroundColor"]
        r, g, b = (int(x) for x in re.findall(r"\d+", bg)[:3])
        if "owner=hub" in pattern:
            assert b > r and b > g, f"hub band should read navy, got {bg}"
        else:
            assert abs(r - g) <= 20 and abs(g - b) <= 20, f"repo band should read grey, got {bg}"


# ---------------------------------------------------------------- coverage gate

def test_coverage_fails_on_a_seeded_unheadered_governed_file(tmp_path, monkeypatch):
    """The acceptance demonstration, as a permanent regression test."""
    import subprocess
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".claude").mkdir()
    good = tmp_path / "CLAUDE.md"
    good.write_text(bh.apply_headers(_SAMPLE), encoding="utf-8")
    seeded = tmp_path / ".claude" / "seed.md"
    seeded.write_text(_SAMPLE, encoding="utf-8")  # markers, NO headers
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)

    assert bh.cmd_coverage(tmp_path) == 1, "unheadered governed file must fail coverage"

    bh.cmd_write(tmp_path)
    assert bh.cmd_coverage(tmp_path) == 0, "coverage must pass once headers are generated"
    assert bh.cmd_check(tmp_path) == 0
