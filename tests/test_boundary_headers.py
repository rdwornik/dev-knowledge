"""Tests for scripts/boundary_headers.py (reader-visible boundary headers).

The point of this module is that the boundary has ONE vocabulary. The machine markers
(`<!-- methodology:start ... owner=hub|repo -->`) are the single source of truth; the
reader-visible headers and the .vscode background decoration are both DERIVED from them.
These tests hold that invariant from four directions:

  * generator units      -- headers are a pure function of the marker attributes
  * placement contract   -- headers never enter a region body (byte-match with
                            templates/claude-regions/ survives)
  * decoration coupling  -- the .vscode regexes select exactly the parsed marker regions,
                            so the editor cannot paint a boundary the parser disagrees with
  * adversarial safety   -- the classes a codex review found on the first cut: prose
                            deletion, fenced examples, CRLF rewriting, vacuous coverage,
                            and a decoration regex that accepts a looser marker language
"""

import importlib.util
import json
import re
import subprocess
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

_SAMPLE = (
    "# T\n\n"
    "<!-- methodology:start id=alpha owner=hub -->\n"
    "hub body\n"
    "<!-- methodology:end id=alpha -->\n\n"
    "<!-- methodology:start id=beta owner=repo -->\n"
    "repo body\n"
    "<!-- methodology:end id=beta -->\n"
)


def _seed_repo(tmp_path: Path, claude_text: str, **extra: str) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "CLAUDE.md").write_text(claude_text, encoding="utf-8", newline="")
    for rel, body in extra.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8", newline="")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    return tmp_path


# ---------------------------------------------------------------- generator units

def test_header_is_a_pure_function_of_the_marker_attributes():
    assert bh.header_for("first-read", "hub").startswith("> **[HUB - methodology]**")
    assert "`first-read`" in bh.header_for("first-read", "hub")
    assert bh.header_for("repo-identity", "repo").startswith("> **[REPO - local]**")


def test_hub_and_repo_headers_are_visually_distinct():
    assert bh.header_for("x", "hub") != bh.header_for("x", "repo")


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
        "> **[HUB - methodology]** region `wrong-id`")
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


# ------------------------------------------------- adversarial safety (codex findings)

def test_prose_quoting_the_header_format_is_never_deleted():
    """CRITICAL regression: stripping must be MARKER-ADJACENT.

    A history entry or doc that quotes the header grammar is authored content. An earlier
    cut used startswith() and would silently delete it on --write.
    """
    doc = (
        "# Doc\n\n"
        "The generator emits lines like this one:\n"
        "> **[HUB - methodology]** region `example` - single-sourced from the hub.\n"
        "...and that is the whole convention.\n\n"
        + _SAMPLE
    )
    out = bh.apply_headers(doc)
    assert "region `example` - single-sourced from the hub." in out, \
        "authored prose that merely quotes the header format was deleted"
    assert out.count("> **[HUB - methodology]** region `alpha`") == 1


def test_markers_inside_a_fenced_code_block_are_examples_not_markers():
    fenced = (
        "# Doc\n\n"
        "```\n"
        "<!-- methodology:start id=example owner=hub -->\n"
        "body\n"
        "<!-- methodology:end id=example -->\n"
        "```\n\n"
        + _SAMPLE
    )
    out = bh.apply_headers(fenced)
    assert "region `example`" not in out, "a fenced example was treated as a real marker"
    assert out.count("region `alpha`") == 1


def test_a_duplicated_stale_header_does_not_survive_regeneration():
    """A contiguous RUN of generated headers is stripped whole.

    Stripping only the marker-adjacent line left a stale duplicate that then survived every
    later regeneration -- a header disagreeing with its marker while --check reported clean.
    """
    doubled = _SAMPLE.replace(
        "<!-- methodology:start id=alpha owner=hub -->",
        "> **[HUB - methodology]** region `stale-wrong-id` - single-sourced from the hub.\n"
        "> **[HUB - methodology]** region `alpha` - single-sourced from the hub.\n"
        "<!-- methodology:start id=alpha owner=hub -->")
    out = bh.apply_headers(doubled)
    assert "stale-wrong-id" not in out, "a stale duplicate header survived regeneration"
    assert out.count("region `alpha`") == 1
    assert out == bh.apply_headers(_SAMPLE)


def test_a_tilde_fence_containing_backticks_does_not_desync_the_scanner():
    """Fence tracking must match the OPENING delimiter, not toggle on any fence line."""
    doc = (
        "# Doc\n\n"
        "~~~\n"
        "```\n"                       # content inside the ~~~ block, NOT a delimiter
        "<!-- methodology:start id=example owner=hub -->\n"
        "~~~\n\n"
        + _SAMPLE
    )
    out = bh.apply_headers(doc)
    assert "region `example`" not in out, "a fenced example was treated as a real marker"
    assert out.count("region `alpha`") == 1


def test_a_marker_hidden_by_a_fence_is_reported_not_silently_skipped(tmp_path):
    """The generator is fence-aware, boundary_report is not. A disagreement must be loud."""
    doc = ("# T\n\n```\n"
           "<!-- methodology:start id=alpha owner=hub -->\nb\n"
           "<!-- methodology:end id=alpha -->\n```\n")
    repo = _seed_repo(tmp_path, doc)
    reports, errors = bh.inspect(repo)
    assert any("disagreement" in e for r in reports for e in r.errors) or errors, \
        "a fenced/unfenced marker disagreement was not surfaced"
    assert bh.cmd_check(repo) == 1


def test_an_undeclared_governed_file_is_an_error(tmp_path):
    """Discovery is a tripwire: a marked file must be DECLARED, not silently counted."""
    repo = _seed_repo(tmp_path, bh.apply_headers(_SAMPLE),
                      **{".claude/extra.md": bh.apply_headers(_SAMPLE)})
    _reports, errors = bh.discover_governed(repo)[1], bh.inspect(repo)[1]
    assert any("_REQUIRED_GOVERNED" in e for e in errors), \
        "an undeclared governed file was accepted silently"
    assert bh.cmd_coverage(repo) == 1


def test_crlf_line_endings_are_preserved_exactly():
    """Region bodies must not be silently rewritten LF<->CRLF by regeneration."""
    crlf = _SAMPLE.replace("\n", "\r\n")
    out = bh.apply_headers(crlf)
    assert "\r\n" in out
    assert re.search(r"[^\r]\n", out) is None, "a CRLF file gained bare-LF lines"
    assert out.count("\r\n") == crlf.count("\r\n") + 2  # two headers inserted


def test_write_refuses_on_an_unbalanced_marker(tmp_path):
    broken = "# T\n\n<!-- methodology:start id=alpha owner=hub -->\nbody, never closed\n"
    repo = _seed_repo(tmp_path, broken)
    assert bh.cmd_write(repo) == 1, "must refuse to write into an unparseable file"
    assert bh.cmd_check(repo) == 1
    assert (repo / "CLAUDE.md").read_text(encoding="utf-8") == broken, "file was mutated"


def test_coverage_is_not_vacuous_when_every_marker_is_deleted(tmp_path):
    """The metric must FAIL when the boundary disappears, not report an empty 100%."""
    repo = _seed_repo(tmp_path, "# T\n\nno markers at all\n")
    assert bh.cmd_coverage(repo) == 1, "marker-less required file reported as covered"


def test_mismatched_close_id_is_a_parse_warning_and_fails_check(tmp_path):
    bad = ("# T\n\n<!-- methodology:start id=alpha owner=hub -->\nb\n"
           "<!-- methodology:end id=beta -->\n")
    repo = _seed_repo(tmp_path, bad)
    assert bh.cmd_check(repo) == 1


# ---------------------------------------------------------------- live-tree state

def test_live_tree_governed_files_are_discovered():
    paths, errors = bh.discover_governed(_ROOT)
    assert not errors, errors
    assert "CLAUDE.md" in [p.name for p in paths]


def test_live_tree_coverage_is_complete():
    reports, errors = bh.inspect(_ROOT)
    assert not errors, errors
    unheaded = [r.rel for r in reports if not r.headed]
    assert not unheaded, f"governed files missing reader-visible headers: {unheaded}"


def test_live_tree_headers_match_markers():
    """Regen-and-diff: the gate form. Fails if headers drift from markers."""
    reports, _ = bh.inspect(_ROOT)
    drifted = [r.rel for r in reports if r.drifted]
    assert not drifted, f"headers stale vs markers: {drifted}"


def test_live_tree_markers_parse_without_warnings():
    reports, _ = bh.inspect(_ROOT)
    for rep in reports:
        assert not rep.warnings, f"{rep.rel}: {rep.warnings}"
        assert not rep.errors, f"{rep.rel}: {rep.errors}"


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


def test_regeneration_does_not_change_any_region_body(tmp_path):
    """End-to-end form of the placement contract, on exact bytes."""
    from boundary_report import parse_regions
    text = (_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    before, _ = parse_regions(text)
    after, _ = parse_regions(bh.apply_headers(text))
    assert {r.id: r.body for r in before} == {r.id: r.body for r in after}


# --------------------------------------------------- decoration coupling

def _vscode_regexes():
    cfg = json.loads((_ROOT / ".vscode" / "settings.json").read_text(encoding="utf-8"))
    return cfg["highlight.regexes"], cfg.get("highlight.regexFlags", "gm")


def test_vscode_declares_a_pattern_for_each_owner():
    regexes, flags = _vscode_regexes()
    assert "m" in flags, "line anchors require the multiline flag"
    owners = sorted("hub" if "owner=hub" in p else "repo" for p in regexes)
    assert owners == ["hub", "repo"]


def _paint(text: str):
    regexes, _ = _vscode_regexes()
    out = []
    for pattern in regexes:
        owner = "hub" if "owner=hub" in pattern else "repo"
        for m in re.finditer(pattern, text, re.M):
            start = text.count("\n", 0, m.start())
            out.append((start, start + m.group(0).count("\n"), owner))
    return sorted(out)


def test_vscode_decoration_selects_exactly_the_parsed_marker_regions():
    """The two-vocabularies guard: the editor and the parser must agree."""
    from boundary_report import parse_regions
    text = (_ROOT / "CLAUDE.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    regions, _ = parse_regions(text)
    expected = {"hub": sum(1 for r in regions if r.owner == "hub"),
                "repo": sum(1 for r in regions if r.owner == "repo")}
    painted = _paint(text)
    got = {"hub": sum(1 for p in painted if p[2] == "hub"),
           "repo": sum(1 for p in painted if p[2] == "repo")}
    assert got == expected, f"decoration painted {got}, markers say {expected}"
    for (s1, e1, _o1), (s2, _e2, _o2) in zip(painted, painted[1:]):
        assert e1 < s2, f"decoration bands overlap at lines {s1}-{e1} / {s2}-"


def test_vscode_bands_start_at_the_generated_header():
    text = (_ROOT / "CLAUDE.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    regexes, _ = _vscode_regexes()
    n = 0
    for pattern in regexes:
        for m in re.finditer(pattern, text, re.M):
            assert bh.is_generated_header(m.group(0).splitlines()[0])
            n += 1
    assert n == 15, f"expected 15 painted regions, found {n}"


def test_vscode_regex_rejects_a_looser_marker_language():
    """The decoration must not paint what the parser would reject."""
    from boundary_report import parse_regions
    bogus = (
        "<!-- methodology:start id=alpha owner=hubbish -->\n"
        "not a real owner\n"
        "<!-- methodology:end id=alpha -->\n"
    )
    assert parse_regions(bogus)[0] == [], "precondition: parser rejects owner=hubbish"
    assert _paint(bogus) == [], "decoration painted a marker the parser rejects"


def test_vscode_regex_requires_the_close_id_to_match_the_open_id():
    mismatched = (
        "<!-- methodology:start id=alpha owner=hub -->\n"
        "body\n"
        "<!-- methodology:end id=beta -->\n"
    )
    assert _paint(mismatched) == [], "decoration paints across a mismatched close id"


def test_vscode_is_scoped_to_governed_surfaces():
    regexes, _ = _vscode_regexes()
    for _pattern, spec in regexes.items():
        assert "CLAUDE" in spec.get("filterFileRegex", "")


def test_vscode_uses_grey_for_hub_and_navy_for_repo():
    regexes, _ = _vscode_regexes()
    for pattern, spec in regexes.items():
        bg = spec["decorations"][0]["backgroundColor"]
        r, g, b = (int(x) for x in re.findall(r"\d+", bg)[:3])
        grey = abs(r - g) <= 20 and abs(g - b) <= 20
        navy = b > r and b > g
        # Mutually exclusive on purpose: a blue-tinted "grey" would satisfy BOTH and the
        # hub/repo distinction would not actually be legible.
        if "owner=hub" in pattern:
            assert grey and not navy, f"hub band must read unambiguously grey, got {bg}"
        else:
            assert navy and not grey, f"repo band must read unambiguously navy, got {bg}"


# ---------------------------------------------------------------- coverage gate

def test_coverage_fails_on_a_seeded_unheadered_governed_file(tmp_path, monkeypatch):
    """The acceptance demonstration, as a permanent regression test.

    The seeded file is DECLARED (the tripwire in
    `test_an_undeclared_governed_file_is_an_error` covers the undeclared path), so this
    exercises the headed/unheaded axis on its own: FAIL at 1/2, GREEN at 2/2 after --write.
    """
    monkeypatch.setattr(bh, "_REQUIRED_GOVERNED", ("CLAUDE.md", ".claude/seed.md"))
    repo = _seed_repo(tmp_path, bh.apply_headers(_SAMPLE),
                      **{".claude/seed.md": _SAMPLE})  # markers, NO headers
    assert bh.cmd_coverage(repo) == 1, "unheadered governed file must fail coverage"
    assert bh.cmd_write(repo) == 0
    assert bh.cmd_coverage(repo) == 0, "coverage must pass once headers are generated"
    assert bh.cmd_check(repo) == 0


# ---------------------------------------------------------------------------
# Governed-glob matching must mean the SAME THING on every host.
# ---------------------------------------------------------------------------

def test_governed_glob_match_is_case_sensitive_on_every_host(monkeypatch):
    """`fnmatch` delegates to the HOST's case rules — case-insensitive on Windows,
    case-sensitive on Linux — so the same repo yielded a different governed set per box and
    the coverage gate measured a different thing depending on where it ran. A gate whose
    denominator is OS-dependent cannot be compared across the fleet or across CI.

    HOST-INDEPENDENT BY CONSTRUCTION (terra HIGH, 2026-08-03). The first version of this test
    just asserted that an uppercased path does not match. That is a real RED on Windows and a
    VACUOUS PASS on Linux/macOS, where `fnmatch` is already case-sensitive — so CI could have
    gone green with the bug fully restored. It was the arc's own defect class, one level up.

    The fix is to stop depending on which host runs it: `fnmatch` case-folds by calling
    `os.path.normcase`, so forcing `normcase` to lowercase makes EVERY platform behave like
    Windows. Under `fnmatch` the uppercased path then matches and this test FAILS anywhere;
    under `fnmatchcase`, `normcase` is never consulted and it passes anywhere. Behavioural,
    not an assertion about which symbol was imported.

    DERIVED, not enumerated: both the positive control and the case-variant are constructed
    FROM `_GOVERNED_GLOBS` itself, so adding or changing a glob re-derives the assertion
    instead of leaving a stale hand-written literal behind.
    """
    import os.path as _osp

    monkeypatch.setattr(_osp, "normcase", str.lower)
    # Guard the guard: if normcase is no longer the folding seam fnmatch uses, this test has
    # stopped simulating Windows and would silently go vacuous again.
    from fnmatch import fnmatch as _raw_fnmatch
    assert _raw_fnmatch("CLAUDE.MD", "CLAUDE.md"), (
        "patching os.path.normcase no longer makes fnmatch case-insensitive — the Windows "
        "simulation is broken, so this test would prove nothing")

    assert bh._GOVERNED_GLOBS, "no governed globs — this test would be vacuous"
    for glob in bh._GOVERNED_GLOBS:
        literal = glob.replace("**/", "").replace("*", "x")
        assert bh._matches_governed_glob(literal), (
            f"positive control failed: {literal!r} should match {glob!r}")
        assert not bh._matches_governed_glob(literal.upper()), (
            f"{glob!r} matched the uppercased path {literal.upper()!r} — glob matching is "
            "following host case rules, so the governed set differs per OS")


# ---------------------------------------------------------------------------
# [#482] — the glob engine must mean what the pattern reads.
#
# `fnmatch` has no `**`, and its `*` CROSSES `/`. So `.claude/*.md` is already recursive
# while `.claude/**/*.md` is a strict subset of it that adds nothing — a glob that reads
# narrower than it behaves. Operator ruling 2026-08-03: REPAIR (true-glob), not REMOVE.
# ---------------------------------------------------------------------------


def test_star_does_not_cross_a_path_separator(monkeypatch):
    """[#482] `*` must not cross `/` — `.claude/*.md` names DIRECT children only.

    Per-glob attribution is demonstrated by narrowing `_GOVERNED_GLOBS` to the single glob
    under test, so the defect is shown through the module's OWN predicate without adding a
    seam first — the RED commit touches no source at all.

    The fixture is a REAL tracked path, asserted live before it is used: a hand-invented
    path would let this test keep passing against a corpus that no longer contains it.
    """
    nested = ".claude/commands/save.md"
    assert nested in bh._tracked_files(_ROOT), (
        f"{nested!r} is no longer tracked — this fixture must be live corpus, not a fiction; "
        "re-point it at a real nested .claude/**/*.md file")

    monkeypatch.setattr(bh, "_GOVERNED_GLOBS", (".claude/*.md",))
    assert not bh._matches_governed_glob(nested), (
        "`.claude/*.md` matched the NESTED path {!r} — `*` crossed `/`, so the glob behaves "
        "recursively while reading as direct-children-only ([#482])".format(nested))


def test_governed_union_is_identical_before_and_after_the_engine_switch():
    """[#482] AC2 — the governed UNION is unchanged by the repair; only ATTRIBUTION moves.

    Per-glob meanings change BY DESIGN under true-glob (`.claude/*.md` stops being recursive;
    `.claude/**/*.md` starts being). What must NOT change is which files are governed. So the
    invariant is the UNION, and "behaviour unchanged" would have been unfalsifiable.

    BOTH SIDES COMPUTED LIVE over the real tracked corpus — the old engine is re-run here
    rather than quoted, so this can never degrade into asserting a remembered constant, and
    ordinary corpus growth cannot break it (it is an equality between two engines, whatever
    the corpus happens to be).
    """
    from fnmatch import fnmatchcase

    tracked = bh._tracked_files(_ROOT)
    assert tracked, "empty tracked corpus — this test would be vacuous"
    assert bh._GOVERNED_GLOBS, "no governed globs — this test would be vacuous"

    before = {p for p in tracked if any(fnmatchcase(p, g) for g in bh._GOVERNED_GLOBS)}
    after = {p for p in tracked if any(bh._glob_matches(p, g) for g in bh._GOVERNED_GLOBS)}

    assert before, "the pre-repair engine governed nothing — fixture is not exercising the rule"
    assert after == before, (
        "the repair changed WHICH files are governed, not merely how they are attributed: "
        f"only-before={sorted(before - after)} only-after={sorted(after - before)}")


def test_glob_matches_agrees_with_stdlib_glob_per_glob():
    """[#482] AC5 — the hand-composed matcher carries its own proof against the stdlib.

    `glob.glob(recursive=True)` is the stdlib true-glob ORACLE. It was rejected as the engine
    (it reads the working tree, not the git index, so a tracked-but-deleted file would leave
    the governed set silently), but it is exactly the right thing to be measured against.

    PER-GLOB, not merely on the union: the union is equal under the OLD engine too, so a
    union-only check would pass against the very semantics this repair replaces. Agreement is
    asserted glob-by-glob, which is where the meanings actually moved.
    """
    import glob as _glob
    import os

    tracked = set(bh._tracked_files(_ROOT))
    assert tracked, "empty tracked corpus — this test would be vacuous"

    for pattern in bh._GOVERNED_GLOBS:
        ours = {p for p in tracked if bh._glob_matches(p, pattern)}
        hits = _glob.glob(pattern, root_dir=_ROOT, recursive=True, include_hidden=True)
        stdlib = {h.replace(os.sep, "/") for h in hits} & tracked
        assert ours == stdlib, (
            f"{pattern!r}: hand-composed matcher disagrees with stdlib glob — "
            f"only-ours={sorted(ours - stdlib)} only-stdlib={sorted(stdlib - ours)}")
