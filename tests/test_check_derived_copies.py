"""Tests for the derived-copy registry and its commit-time organ.

THE SHAPE OF THIS FILE. Three populations, and the split is deliberate:

  * the MATCHER, tested directly as a pure function — including the two over-match cases a
    bare `fnmatch` over the whole path would get wrong, because an over-matching gate is the
    failure mode that gets a gate bypassed rather than fixed;
  * the LIVE REGISTRY, asserted against the live tree — every declared gate really exists,
    every self-gated row really verifies today. A registry that validated but described a
    tree that no longer exists would be exactly the rot it was built to catch;
  * TRIP TESTS, which are the ones that matter. A gate that has never been seen to REFUSE is
    a gate nobody has evidence about. Each leg is driven onto a constructed violation and
    the refusal is asserted, on a temporary registry rather than by editing the live one.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts import check_derived_copies as cdc  # noqa: E402


# --- the matcher ------------------------------------------------------------------------


@pytest.mark.parametrize("path,pattern,expected", [
    ("ecosystem/routing-table.yaml", "ecosystem/routing-table.yaml", True),
    ("tasks/manifest.json", "tasks/**/*.json", True),
    ("tasks/sub/deep/a.md", "tasks/**/*.md", True),
    ("docs/decisions/ADR-115-agents-md.md", "docs/decisions/ADR-*.md", True),
    (".claude/agents/artifact-reader.md", ".claude/agents/**", True),
    ("deploy/manifest-v1.5.0.yaml", "deploy/manifest-v*.yaml", True),
    ("scripts/toc/generator.py", "scripts/**/*.py", True),
    # misses
    ("ecosystem/provider-registry.yaml", "ecosystem/routing-table.yaml", False),
    ("tasks/manifest.json", "tasks/**/*.md", False),
    ("docs/decisions/README.md", "docs/decisions/ADR-*.md", False),
])
def test_glob_matches_segment_wise(path, pattern, expected):
    assert cdc.glob_matches(path, pattern) is expected


@pytest.mark.parametrize("path", [
    "docs/intake/sub/deep.md",
    "docs/intake/a/b/c.md",
])
def test_star_does_not_cross_a_separator(path):
    """`*` stays inside one segment — the whole reason this is not `fnmatch.fnmatch`.

    `fnmatch.fnmatch("docs/intake/sub/deep.md", "docs/intake/*.md")` returns True, because
    plain fnmatch lets `*` swallow `/`. Under that behaviour the `intake-index` row would be
    rebound by a commit touching a nested file the generator does not read, and the gate
    would refuse commits it has no business refusing.
    """
    assert cdc.glob_matches(path, "docs/intake/*.md") is False


def test_matching_is_case_sensitive():
    """git tracks paths case-sensitively everywhere; folding would make the row set
    platform-dependent, which is the defect `silent_rule_detector` records for its corpus."""
    assert cdc.glob_matches("ecosystem/ROUTING-TABLE.yaml",
                            "ecosystem/routing-table.yaml") is False


# --- the live registry ------------------------------------------------------------------


@pytest.fixture(scope="module")
def registry():
    return cdc.load_registry(_REPO_ROOT)


def test_live_registry_validates(registry):
    assert registry.schema_version == "1.0.0"
    assert len(registry.copies) >= 1


def test_every_delegated_gate_exists_in_precommit_config(registry):
    """LEG 2 against the live tree: no row delegates to a hook that is not configured."""
    assert cdc.check_disarm(registry, _REPO_ROOT) == []


def test_every_delegated_gate_id_is_really_declared(registry):
    """The same property from the other end, so a bug in `check_disarm` cannot hide it."""
    present = cdc.configured_hook_ids(_REPO_ROOT)
    assert set(registry.gate_ids) <= present


def test_every_row_names_a_renderer_that_exists(registry):
    """A registry entry that cannot be rendered is worse than an absent one.

    Structural rather than executed: it asserts the renderer this row points at is a real
    file in this tree. The two self-gated rows are actually RUN below; running all eleven
    would pay eleven subprocesses for a property this settles statically.
    """
    for cid, copy in registry.copies.items():
        assert copy.render.startswith("uv run --locked "), (
            f"{cid}: a bare `python` resolves nothing on a clean checkout (ADR-106)")
        argv = list(copy.verify or ())
        assert argv, f"{cid}: no verify argv"
        if argv[0] == "-m":
            module = argv[1].replace(".", "/")
            assert (_REPO_ROOT / f"{module}.py").is_file() or (
                _REPO_ROOT / module).is_dir(), f"{cid}: no module {argv[1]}"
        else:
            assert (_REPO_ROOT / argv[0]).is_file(), f"{cid}: no script {argv[0]}"


def test_every_row_can_actually_fire_on_this_tree(registry):
    """A row none of whose sources match anything is a row that can never fire.

    ASSERTED PER ROW, NOT PER GLOB, and that weakening is deliberate rather than a
    convenience. Some source globs are legitimately PROSPECTIVE: `conftest.py` and
    `tach.toml` are both absent from this repo — a root `conftest.py` is refused by the
    [#430](a) ruling, and this repo does not use tach — yet both appear in the live
    `files:` selectors of `doc-counts-pytest-freshness` and `codemap-freshness`. The rows
    mirror those selectors on purpose, so requiring every glob to match today would force
    the registry to disagree with the hooks it documents. What is a real defect is a row
    that matches NOTHING, because that row is inert and reads as covered.
    """
    tracked = [p for p in _tracked_paths() if p]
    assert tracked, "git listed no tracked files; the assertion below would be vacuous"
    for cid, copy in registry.copies.items():
        assert any(cdc.glob_matches(t, g) for g in copy.sources for t in tracked), (
            f"{cid}: none of {copy.sources} matches any tracked path")


def _tracked_paths() -> list[str]:
    import subprocess
    out = subprocess.run(["git", "ls-files"], cwd=_REPO_ROOT,
                         capture_output=True, text=True, check=True)
    return [line.replace("\\", "/") for line in out.stdout.splitlines()]


def test_the_l0_routing_row_is_registered_and_self_gated(registry):
    """The witnessed instance is the row the deliverable exists for."""
    row = registry.copies["l0-routing-region"]
    assert row.commit_gate == "self"
    assert "ecosystem/routing-table.yaml" in row.sources
    # the RENDERER is a source too (terra HIGH): editing render_table changes what the copy
    # is supposed to contain exactly as editing the table does
    assert "scripts/routing_agreement.py" in row.sources
    assert row.kind == "region"
    assert row.region_begin and row.region_end
    assert row.on_target_absent == "warn"


def test_self_gated_rows_pass_on_the_current_tree(registry):
    """Every self-gated row is CURRENT right now — so arming the gate refuses nothing
    that is already committed, which is what makes it landable rather than a wedge."""
    assert registry.self_gated, "no self-gated row: this test would pass vacuously"
    for cid, copy in registry.self_gated.items():
        findings = cdc.check_rebinds(
            cdc.DerivedCopiesRegistry(schema_version=registry.schema_version,
                                      copies={cid: copy}),
            _REPO_ROOT,
            # a path guaranteed to rebind THIS row: its first literal source, or a
            # constructed one for a glob source
            [_a_path_matching(copy.sources[0])])
        assert findings == [], f"{cid} is already stale on the current tree: {findings}"


def _a_path_matching(pattern: str) -> str:
    """A concrete repo-relative path that the pattern matches."""
    return (pattern.replace("**/", "sub/").replace("*.md", "a.md")
            .replace("*.json", "a.json").replace("*.py", "a.py").replace("*", "x"))


def test_the_helper_really_produces_matching_paths():
    """Guards the test above from passing vacuously on a path that matches nothing."""
    for pat in ("tasks/**/*.md", "tasks/**/*.json", "ecosystem/routing-table.yaml"):
        assert cdc.glob_matches(_a_path_matching(pat), pat), pat


# --- trip tests: each leg is driven onto a violation ------------------------------------


def _write_registry(tmp_path: Path, copies: dict) -> Path:
    """A temporary repo root carrying a registry and a pre-commit config."""
    (tmp_path / "ecosystem").mkdir(parents=True, exist_ok=True)
    (tmp_path / "ecosystem" / "derived-copies.yaml").write_text(
        yaml.safe_dump({"schema_version": "1.0.0", "copies": copies}), encoding="utf-8")
    (tmp_path / ".pre-commit-config.yaml").write_text(
        yaml.safe_dump({"repos": [{"repo": "local", "hooks": [
            {"id": "a-real-hook", "entry": "true", "files": "^a/"},
            {"id": "a-narrowed-hook", "entry": "true", "files": "^$"},
            {"id": "a-pre-push-hook", "entry": "true", "always_run": True,
             "stages": ["pre-push"]},
        ]}]}), encoding="utf-8")
    return tmp_path


_GATED_ROW = {
    "what": "x", "sources": ["a/b.yaml"], "target": "a/c.md", "target_scope": "repo",
    "render": "uv run --locked python scripts/x.py --write", "kind": "command",
    "verify": ["scripts/x.py", "--check"], "commit_gate": "gate",
}


def test_leg2_trips_on_a_gate_that_is_not_configured(tmp_path):
    """A row delegating to a deleted hook is REFUSED — the disarm this registry exists for."""
    repo = _write_registry(tmp_path, {"row": {**_GATED_ROW, "gate": "a-deleted-hook"}})
    findings = cdc.check_disarm(cdc.load_registry(repo), repo)
    assert len(findings) == 1
    assert findings[0].copy_id == "row"
    assert "a-deleted-hook" in findings[0].detail


def test_leg2_passes_when_the_gate_is_configured(tmp_path):
    repo = _write_registry(tmp_path, {"row": {**_GATED_ROW, "gate": "a-real-hook"}})
    assert cdc.check_disarm(cdc.load_registry(repo), repo) == []


def test_leg1_trips_when_a_staged_source_leaves_its_copy_stale(tmp_path):
    """THE DELIVERABLE, driven: a staged source + a failing verify == a refused commit."""
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "stale.py").write_text("import sys; sys.exit(1)\n",
                                                   encoding="utf-8")
    repo = _write_registry(tmp_path, {"row": {
        **_GATED_ROW, "commit_gate": "self", "verify": ["scripts/stale.py"]}})
    findings = cdc.check_rebinds(cdc.load_registry(repo), repo, ["a/b.yaml"])
    assert len(findings) == 1
    assert "a/b.yaml" in findings[0].detail
    assert "--write" in findings[0].remedy


def test_leg1_is_silent_when_the_commit_does_not_stage_the_source(tmp_path):
    """The narrowing that makes this landable: an unrelated commit is not looked at, so the
    failing verify above is never even run."""
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "stale.py").write_text("import sys; sys.exit(1)\n",
                                                   encoding="utf-8")
    repo = _write_registry(tmp_path, {"row": {
        **_GATED_ROW, "commit_gate": "self", "verify": ["scripts/stale.py"]}})
    assert cdc.check_rebinds(cdc.load_registry(repo), repo, ["unrelated/file.md"]) == []


def test_leg1_region_absent_target_warns_rather_than_failing(tmp_path, capsys):
    """Z-G4 posture: L0 is absent on CI, in a container and on a cloud lane. An absent
    target is a NAMED gap, and naming it is not the same as failing the commit."""
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "render.py").write_text("print('REGION')\n", encoding="utf-8")
    repo = _write_registry(tmp_path, {"row": {
        **_GATED_ROW, "commit_gate": "self", "kind": "region",
        "target": str(tmp_path / "nope.md"), "target_scope": "l0",
        "region_begin": "<!--b-->", "region_end": "<!--e-->",
        "on_target_absent": "warn", "verify": ["scripts/render.py"]}})
    assert cdc.check_rebinds(cdc.load_registry(repo), repo, ["a/b.yaml"]) == []
    assert "not a pass" in capsys.readouterr().err


_RENDER_NEW = "print('<!--b-->\\nNEW\\n<!--e-->')\n"


def _region_row(target, **over):
    return {**_GATED_ROW, "commit_gate": "self", "kind": "region",
            "target": str(target), "target_scope": "l0",
            "region_begin": "<!--b-->", "region_end": "<!--e-->",
            "verify": ["scripts/render.py"], **over}


def test_leg1_region_trips_when_the_region_is_stale(tmp_path):
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "render.py").write_text(_RENDER_NEW, encoding="utf-8")
    target = tmp_path / "l0.md"
    target.write_text("prose\n<!--b-->\nOLD\n<!--e-->\nmore\n", encoding="utf-8")
    repo = _write_registry(tmp_path, {"row": _region_row(target)})
    findings = cdc.check_rebinds(cdc.load_registry(repo), repo, ["a/b.yaml"])
    assert len(findings) == 1
    assert "is not what the source renders to" in findings[0].detail


def test_leg1_region_is_not_launderable_by_a_duplicate_elsewhere(tmp_path):
    """THE terra HIGH, driven. The authoritative region is STALE and the freshly-rendered
    text also appears further down the document — in a fenced example, a changelog, a
    comment quoting the new table. A substring test passes this; a bounded compare refuses
    it, which is the whole difference between checking the copy and checking the file."""
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "render.py").write_text(_RENDER_NEW, encoding="utf-8")
    target = tmp_path / "l0.md"
    target.write_text(
        "prose\n<!--b-->\nOLD\n<!--e-->\n\nexample:\n```\n<!--b-->\nNEW\n<!--e-->\n```\n",
        encoding="utf-8")
    repo = _write_registry(tmp_path, {"row": _region_row(target)})
    findings = cdc.check_rebinds(cdc.load_registry(repo), repo, ["a/b.yaml"])
    assert len(findings) == 1, "a duplicate occurrence laundered a stale region"
    # duplicate markers are refused outright rather than resolved by picking the first
    assert "markers" in findings[0].detail


def test_leg1_region_tolerates_crlf_in_the_target(tmp_path):
    """A Windows-written L0 copy diverging only in line endings is NOT a divergence —
    a false refusal there would teach authors to bypass the gate."""
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "render.py").write_text(
        "print('<!--b-->\\nA\\n<!--e-->')\n", encoding="utf-8")
    target = tmp_path / "l0.md"
    target.write_bytes(b"prose\r\n<!--b-->\r\nA\r\n<!--e-->\r\nmore\r\n")
    repo = _write_registry(tmp_path, {"row": _region_row(target)})
    assert cdc.check_rebinds(cdc.load_registry(repo), repo, ["a/b.yaml"]) == []


# --- terra review fixes, each driven onto its own violation -----------------------------


def test_extract_region_refuses_duplicate_markers():
    _, why = cdc.extract_region("<!--b-->x<!--e--><!--b-->y<!--e-->",
                                "<!--b-->", "<!--e-->")
    assert why and "exactly one pair" in why


def test_extract_region_refuses_reversed_markers():
    _, why = cdc.extract_region("<!--e-->body<!--b-->", "<!--b-->", "<!--e-->")
    assert why and "before" in why


def test_a_deletion_still_rebinds_its_copy():
    """terra HIGH: `--diff-filter=ACMR` dropped deletions, so DELETING a registered source
    exited 0 while leaving the copy it fed orphaned."""
    stream = "D\0ecosystem/routing-table.yaml\0"
    assert cdc.parse_name_status(stream) == ("ecosystem/routing-table.yaml",)


def test_a_rename_exposes_both_halves():
    """terra HIGH: `--name-only` reports only a rename's DESTINATION, so moving a source
    OUT of a registered glob showed a path matching no row and the gate went quiet."""
    stream = ("R100\0ecosystem/routing-table.yaml\0docs/archive/routing-table.yaml\0"
              "M\0BACKLOG.md\0")
    assert cdc.parse_name_status(stream) == (
        "ecosystem/routing-table.yaml", "docs/archive/routing-table.yaml", "BACKLOG.md")


def test_leg2_trips_when_a_gate_is_narrowed_to_match_nothing(tmp_path):
    """terra HIGH: id-presence alone was defeatable. `files: '^$'` keeps the id and guards
    nothing — the silent-disarm class the registry exists to expose, one level up."""
    repo = _write_registry(tmp_path, {"row": {**_GATED_ROW, "gate": "a-narrowed-hook"}})
    findings = cdc.check_disarm(cdc.load_registry(repo), repo)
    assert len(findings) == 1
    assert "does not reach" in findings[0].detail


def test_leg2_trips_when_a_gate_is_moved_off_the_commit_stage(tmp_path):
    """A hook that runs at pre-push is not a commit-time guarantee, whatever its id says."""
    repo = _write_registry(tmp_path, {"row": {**_GATED_ROW, "gate": "a-pre-push-hook"}})
    findings = cdc.check_disarm(cdc.load_registry(repo), repo)
    assert len(findings) == 1
    assert "not pre-commit" in findings[0].detail


def test_ship_gated_rows_owe_a_reason(tmp_path):
    """`commit_gate: ship` records a DECISION. Without the reason it is indistinguishable
    from an oversight, which is the thing the registry exists to tell apart."""
    repo = _write_registry(tmp_path, {"row": {**_GATED_ROW, "commit_gate": "ship"}})
    with pytest.raises(cdc.DerivedCopiesError):
        cdc.load_registry(repo)


def test_the_audits_index_row_is_ship_gated_with_its_reason(registry):
    """It was registered as `gate` while the hook [#590] narrowed covers neither the
    artifacts that derive it nor their addition. Recording where the guarantee actually
    lives is the honest shape."""
    row = registry.copies["audits-index"]
    assert row.commit_gate == "ship"
    assert row.ship_reason and "[#590]" in row.ship_reason
    assert "docs/audits/*.md" in row.sources


def test_doc_counts_declares_the_inputs_its_gate_does_not_cover(registry):
    """The document carries three values and the named hook guards one of them."""
    row = registry.copies["doc-counts"]
    assert "scripts/audit.py" in row.uncovered_inputs
    assert ".pre-commit-config.yaml" in row.uncovered_inputs


@pytest.mark.parametrize("bad", ["", "/a/b", "a//b", "a/b/", "a\\b"])
def test_schema_refuses_a_malformed_source_glob(tmp_path, bad):
    """terra MEDIUM: the matcher drops empty segments, so a malformed glob would silently
    mean something else instead of being refused."""
    repo = _write_registry(tmp_path, {"row": {**_GATED_ROW, "gate": "a-real-hook",
                                              "sources": [bad]}})
    with pytest.raises(cdc.DerivedCopiesError):
        cdc.load_registry(repo)


def test_schema_refuses_an_unimplemented_version(tmp_path):
    """terra MEDIUM: `schema_version` was declared and compared to nothing."""
    repo = _write_registry(tmp_path, {"row": {**_GATED_ROW, "gate": "a-real-hook"}})
    cfg = repo / "ecosystem" / "derived-copies.yaml"
    cfg.write_text(cfg.read_text(encoding="utf-8").replace("1.0.0", "9.9.9"),
                   encoding="utf-8")
    with pytest.raises(cdc.DerivedCopiesError):
        cdc.load_registry(repo)


def test_schema_forbids_an_unknown_key(tmp_path):
    """`extra="forbid"`: a misspelled key is a blocked commit, not inert data."""
    repo = _write_registry(tmp_path, {"row": {**_GATED_ROW, "gate": "a-real-hook",
                                              "comit_gate": "self"}})
    with pytest.raises(cdc.DerivedCopiesError):
        cdc.load_registry(repo)


def test_schema_refuses_self_without_a_verify(tmp_path):
    """A `self` row with no way to check itself reads as covered and is not."""
    row = {k: v for k, v in _GATED_ROW.items() if k != "verify"}
    repo = _write_registry(tmp_path, {"row": {**row, "commit_gate": "self"}})
    with pytest.raises(cdc.DerivedCopiesError):
        cdc.load_registry(repo)


def test_schema_refuses_gate_without_a_hook_id(tmp_path):
    repo = _write_registry(tmp_path, {"row": dict(_GATED_ROW)})
    with pytest.raises(cdc.DerivedCopiesError):
        cdc.load_registry(repo)


def test_schema_refuses_a_region_row_without_markers(tmp_path):
    """terra HIGH, at the schema: without markers the checker falls back to a substring
    test over the whole target, which any duplicate of the rendered text launders."""
    repo = _write_registry(tmp_path, {"row": {
        **_GATED_ROW, "commit_gate": "self", "kind": "region",
        "verify": ["scripts/render.py"]}})
    with pytest.raises(cdc.DerivedCopiesError):
        cdc.load_registry(repo)


def test_schema_refuses_an_empty_registry(tmp_path):
    repo = _write_registry(tmp_path, {})
    with pytest.raises(cdc.DerivedCopiesError):
        cdc.load_registry(repo)


