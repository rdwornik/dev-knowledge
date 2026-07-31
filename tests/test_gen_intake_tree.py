"""Tests for scripts/gen_intake_tree.py ([#383] wave 1 — the ADR-109 §4 generality proof).

Firing tests: the line model is lossless (including the Unicode-line-boundary class that
str.splitlines would silently eat), item rows inside the marker block become per-item nodes
while look-alike doctrine lines outside it stay residue, the residue manifest carries the
ADR-107 §5 finding-6 shape (ordering + non-member residue + hash + direction), the round-trip
reassembles byte-for-byte, and the regen-and-diff check REDs on each distinct failure mode
before it greens. Plus the two contracts a proof must not quietly lose: the projection is
SHARED with gen_intake_index (not a second copy), and the audit leg is hub-only so it cannot
manufacture a consumer gap.
"""

import importlib.util
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gt = _load("gen_intake_tree")
gi = _load("gen_intake_index")


def _doc(status: str, intake_id: str, title: str) -> str:
    return (f"---\nintake-id: {intake_id}\nstatus: {status}\norigin: test\n---\n\n"
            f"# {title}\n\nbody prose\n")


def _readme(rows: str, doctrine: str = "## 1. Doctrine\n\nprose -> with an arrow\n") -> str:
    return (f"# intake\n\n## Contents\n\n{gi._START_MARKER}\n{rows}{gi._END_MARKER}\n\n"
            f"{doctrine}")


def _make_surface(tmp_path: Path, docs: dict[str, str], readme: str) -> Path:
    d = tmp_path / "intake"
    d.mkdir()
    for name, content in docs.items():
        (d / name).write_text(content, encoding="utf-8", newline="")
    (d / "README.md").write_text(readme, encoding="utf-8", newline="")
    return d


def _seeded(tmp_path: Path) -> Path:
    """A minimal surface whose README already matches what the generator would render."""
    docs = {"a.md": _doc("SEED", "1", "Alpha"), "b.md": _doc("ACCEPTED", "2", "Beta")}
    d = _make_surface(tmp_path, docs, _readme(""))
    (d / "README.md").write_text(
        _readme(gi.render_contents(d)), encoding="utf-8", newline="")
    return d


def _write_manifest(d: Path) -> None:
    text = (d / "README.md").read_bytes().decode("utf-8")
    manifest = gt.build_manifest(text, gt.parse_readme(text), d)
    (d / "manifest.json").write_text(gt._dump(manifest), encoding="utf-8", newline="\n")


# --- the line model ----------------------------------------------------------

def test_line_model_is_lossless_on_the_live_readme():
    text = gt._SOURCE.read_bytes().decode("utf-8")
    model = gt.parse_readme(text)
    assert model.reassemble() == text


def test_parse_splits_only_on_newline_not_unicode_line_boundaries():
    """str.splitlines() would eat U+2028/U+0085/\\x0b and break byte-exactness."""
    text = "# t\n weird\x0bmoretail\n"
    assert gt.parse_readme(text).reassemble() == text
    assert len(text.split("\n")) != len(text.splitlines())


def test_item_rows_inside_the_block_become_nodes(tmp_path):
    d = _seeded(tmp_path)
    model = gt.parse_readme((d / "README.md").read_bytes().decode("utf-8"))
    items = [n.value for n in model.nodes if n.kind == "item"]
    assert sorted(items) == ["a.md", "b.md"]


def test_lookalike_row_outside_the_block_stays_residue(tmp_path):
    """A doctrine line sharing the row shape must NOT be captured as an item node."""
    d = _seeded(tmp_path)
    readme = (d / "README.md").read_bytes().decode("utf-8")
    readme += "\n- [#99](ghost.md) — a doctrine example, not an index row\n"
    (d / "README.md").write_text(readme, encoding="utf-8", newline="")
    model = gt.parse_readme(readme)
    assert [n.value for n in model.nodes if n.kind == "item"] == ["a.md", "b.md"]
    assert any(n.kind == "line" and "ghost.md" in n.value for n in model.nodes)


# --- the residue manifest (AC-4) ---------------------------------------------

def test_manifest_carries_the_finding_6_shape(tmp_path):
    d = _seeded(tmp_path)
    text = (d / "README.md").read_bytes().decode("utf-8")
    m = gt.build_manifest(text, gt.parse_readme(text), d)
    assert m["schema"] == gt.SCHEMA_ID
    assert m["direction"] == "derived-from"          # DIRECTION
    assert m["nodes"]                                 # ORDERING + NON-MEMBER RESIDUE
    assert len(m["source_sha256"]) == 64              # HASH
    assert any(n["t"] == "line" for n in m["nodes"])


def test_manifest_enumerates_what_the_split_does_not_capture(tmp_path):
    d = _seeded(tmp_path)
    text = (d / "README.md").read_bytes().decode("utf-8")
    nc = gt.build_manifest(text, gt.parse_readme(text), d)["not_captured"]
    assert "intake_document_bodies" in nc
    assert nc["projected_frontmatter_keys"] == list(gt._PROJECTED_FM_KEYS)
    # `origin` is present on every fixture doc and is NOT projected -> must be enumerated.
    assert nc["off_projection_frontmatter_keys"]["a.md"] == ["origin"]


def test_manifest_is_pure_ascii_and_lf(tmp_path):
    d = _seeded(tmp_path)
    _write_manifest(d)
    raw = (d / "manifest.json").read_bytes()
    assert b"\r\n" not in raw
    assert all(b < 128 for b in raw)


def test_honest_limit_records_the_inverted_ratio(tmp_path):
    """The architect ruling: the generality claim must state what was shown."""
    d = _seeded(tmp_path)
    text = (d / "README.md").read_bytes().decode("utf-8")
    hl = gt.build_manifest(text, gt.parse_readme(text), d)["honest_limit"]
    assert hl["item_derived_lines"] + hl["residue_lines"] == hl["total_lines"]
    assert "inverted" in hl["surface_1_comparison"].lower()


# --- the round-trip + regen-and-diff (AC-3 / AC-5) ---------------------------

def test_roundtrip_from_manifest_is_byte_exact(tmp_path):
    d = _seeded(tmp_path)
    _write_manifest(d)
    manifest = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
    rebuilt = gt.manifest_to_model(manifest).reassemble(d)
    assert rebuilt == (d / "README.md").read_bytes().decode("utf-8")


def test_evaluate_green_on_a_coherent_surface(tmp_path):
    d = _seeded(tmp_path)
    _write_manifest(d)
    assert gt.evaluate(d)[0] == gt.OK


def test_evaluate_reds_on_residue_drift(tmp_path):
    """The RED-first witness, as a regression: a doctrine edit without a regen must fire."""
    d = _seeded(tmp_path)
    _write_manifest(d)
    readme = (d / "README.md").read_bytes().decode("utf-8")
    (d / "README.md").write_text(readme.replace("## 1. Doctrine", "## 1. Doctrine EDITED"),
                                 encoding="utf-8", newline="")
    verdict, reasons = gt.evaluate(d)
    assert verdict == gt.DRIFT
    assert any("stale" in r for r in reasons)
    assert any("source_sha256" in r for r in reasons)


def test_evaluate_reds_when_an_intake_title_changes(tmp_path):
    """An item-side change: the row re-derives, so the carried residue no longer matches."""
    d = _seeded(tmp_path)
    _write_manifest(d)
    (d / "a.md").write_text(_doc("SEED", "1", "Alpha RENAMED"), encoding="utf-8", newline="")
    assert gt.evaluate(d)[0] == gt.DRIFT


def test_evaluate_malformed_on_missing_carrier(tmp_path):
    d = _seeded(tmp_path)
    verdict, reasons = gt.evaluate(d)
    assert verdict == gt.MALFORMED
    assert "manifest.json is missing" in reasons[0]


def test_evaluate_malformed_on_wrong_schema(tmp_path):
    d = _seeded(tmp_path)
    _write_manifest(d)
    (d / "manifest.json").write_text(json.dumps({"schema": "bogus/v9", "nodes": []}),
                                     encoding="utf-8", newline="\n")
    assert gt.evaluate(d)[0] == gt.MALFORMED


def test_evaluate_malformed_on_unknown_node_type(tmp_path):
    d = _seeded(tmp_path)
    _write_manifest(d)
    m = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
    m["nodes"].append({"t": "bogus"})
    (d / "manifest.json").write_text(json.dumps(m), encoding="utf-8", newline="\n")
    assert gt.evaluate(d)[0] == gt.MALFORMED


def test_evaluate_reasons_are_ascii_only(tmp_path):
    """README.md carries U+2192 and Windows stdout is cp1252 — a drift report that echoed
    source content would crash on exactly the path that most needs to be readable."""
    d = _seeded(tmp_path)
    _write_manifest(d)
    readme = (d / "README.md").read_bytes().decode("utf-8")
    (d / "README.md").write_text(readme.replace("prose -> with an arrow", "prose → arrow"),
                                 encoding="utf-8", newline="")
    verdict, reasons = gt.evaluate(d)
    assert verdict == gt.DRIFT
    for reason in reasons:
        reason.encode("cp1252")  # raises UnicodeEncodeError if a non-cp1252 glyph leaked
        assert "→" not in reason


# --- codex-review 2026-07-31 HIGH findings, each reproduced then pinned -------

def test_status_only_change_reds_the_gate(tmp_path):
    """F4: status drives GROUPING, not row text — so reassembly alone cannot see a flip.
    Reproduced green before the fix; the item-set leg is what closes it."""
    d = _seeded(tmp_path)
    _write_manifest(d)
    (d / "a.md").write_text(_doc("ACCEPTED", "1", "Alpha"), encoding="utf-8", newline="")
    verdict, reasons = gt.evaluate(d)
    assert verdict == gt.DRIFT
    assert any("projected status drift" in r for r in reasons)


def test_carrier_with_zero_item_nodes_reds(tmp_path):
    """F1: the gate must not be satisfiable by deleting exactly what it proves.
    Stripping every row and regenerating produced an all-residue carrier that passed."""
    d = _seeded(tmp_path)
    readme = (d / "README.md").read_bytes().decode("utf-8")
    stripped = "\n".join(ln for ln in readme.split("\n")
                         if not ln.startswith("- [#"))
    (d / "README.md").write_text(stripped, encoding="utf-8", newline="")
    (d / "manifest.json").write_text(
        gt._dump(gt.build_manifest(stripped, gt.parse_readme(stripped), d)),
        encoding="utf-8", newline="\n")
    verdict, reasons = gt.evaluate(d)
    assert verdict == gt.DRIFT
    assert any("ZERO item nodes" in r for r in reasons)


def test_item_node_without_an_intake_doc_reds(tmp_path):
    d = _seeded(tmp_path)
    _write_manifest(d)
    (d / "a.md").unlink()
    verdict, reasons = gt.evaluate(d)
    assert verdict == gt.DRIFT
    assert any("no intake doc on disk" in r for r in reasons)


def test_duplicate_item_nodes_red(tmp_path):
    d = _seeded(tmp_path)
    _write_manifest(d)
    m = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
    m["nodes"].append(next(n for n in m["nodes"] if n["t"] == "item"))
    (d / "manifest.json").write_text(json.dumps(m), encoding="utf-8", newline="\n")
    assert any("duplicate item node" in r for r in gt.evaluate(d)[1])


def test_audit_leg_fails_when_index_and_worktree_disagree(tmp_path, monkeypatch):
    """F2: the working-tree read is only trustworthy while the index agrees — otherwise a
    staged deletion under docs/intake/ is hidden by restoring the working copy."""
    import audit as aud

    monkeypatch.setattr(aud, "_index_worktree_divergence",
                        lambda *_a, **_k: ("dirty", ["docs/intake/manifest.json"]))
    finding = aud.check_intake_tree_coherence(Path(gt._REPO_ROOT))[0]
    assert finding.status == "fail"
    assert "index and working tree disagree" in finding.evidence


# --- the contracts a proof must not quietly lose ------------------------------

def test_projection_is_shared_with_gen_intake_index_not_copied():
    """One definition of the row format: gen_intake_tree must not re-declare it.

    Asserted by PROVENANCE, not object identity — the loader above re-execs each module, so
    the two module objects legitimately hold distinct function objects for the same source.
    """
    assert gt.render_row.__module__ == "gen_intake_index"
    assert gt.render_row.__code__.co_filename == gi.render_row.__code__.co_filename
    src = (_SCRIPTS / "gen_intake_tree.py").read_text(encoding="utf-8")
    assert "- [{label}](" not in src


def test_live_manifest_on_disk_is_current():
    """The committed carrier must be coherent with the committed README (the gate's subject)."""
    assert gt.evaluate()[0] == gt.OK


def test_audit_leg_is_hub_only_and_na_off_hub(tmp_path):
    """Guarding on docs/intake/ EXISTING would FAIL consumer repos that carry one without a
    carrier (corp-monorepo, ai-council both do) — a manufactured fleet gap."""
    import audit as aud

    (tmp_path / "docs" / "intake").mkdir(parents=True)
    finding = aud.check_intake_tree_coherence(tmp_path)[0]
    assert finding.status == "n/a"


def test_audit_leg_passes_on_the_live_hub(monkeypatch):
    """Index/worktree agreement is stubbed to 'ok' deliberately: without it this asserts
    transient git state (it REDs mid-arc while docs/intake/ edits are unstaged, which is the
    guard working as designed) rather than the wrapper's own verdict."""
    import audit as aud

    monkeypatch.setattr(aud, "_index_worktree_divergence", lambda *_a, **_k: ("ok", []))
    finding = aud.check_intake_tree_coherence(Path(gt._REPO_ROOT))[0]
    assert finding.status == "pass"


def test_check_is_registered_as_a_ship_gate_leg():
    import audit as aud

    assert aud.check_intake_tree_coherence in aud.ALL_CHECKS
