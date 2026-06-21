"""Tests for scripts/validate_doc_code_edge.py -- #194 Phase-A move-safety spike (ADR-89).

The load-bearing proof is (b): a moved annotated code file must NOT fire `broken_edge` --
the resolver re-finds `# rule: TEST-01` at its NEW path, proving identity = annotation
content, never a stored path. If the resolver had secretly cached a path, (b) would fail and
the spike STOPS (the mechanism needs redesign; we are not build-ready).

The four proofs:
  (a) resolves              -- doc <-> code resolve at all
  (b) MOVE-SAFETY           -- move the code file -> still resolved, at the new path
  (c) real breakage fires   -- delete the annotation -> broken_edge (teeth on real breakage)
  (d) duplicate guard       -- two annotations -> ambiguous
"""

import importlib.util
import shutil
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_MOD = _REPO_ROOT / "scripts" / "validate_doc_code_edge.py"
_FIXTURE = _REPO_ROOT / "tests" / "fixtures" / "doc-code-edge"


def _load():
    spec = importlib.util.spec_from_file_location("validate_doc_code_edge", _MOD)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # future-annotations + dataclasses need it registered
    spec.loader.exec_module(module)
    return module


vdce = _load()

sys.path.insert(0, str(_REPO_ROOT / "scripts"))
import audit as aud  # noqa: E402  (audit imports the same module as its _vdce)


def _copy_fixture(tmp_path):
    """Copy the fixture into a tmp tree; doc + code share one dir, so both roots = it."""
    dst = tmp_path / "edge"
    shutil.copytree(_FIXTURE, dst)
    return dst, dst  # (doc_root, code_root)


# --- (a) resolves ----------------------------------------------------------------------

def test_a_resolves(tmp_path):
    doc_root, code_root = _copy_fixture(tmp_path)
    result = vdce.resolve_edge("TEST-01", doc_root, code_root)
    assert result.status == "resolved"
    assert result.doc_sites[0].file == "doc.md"
    assert result.code_sites[0].file == "sample_module.py"


# --- (b) MOVE-SAFETY (the load-bearing proof) ------------------------------------------

def test_b_move_safety(tmp_path):
    doc_root, code_root = _copy_fixture(tmp_path)
    assert vdce.resolve_edge("TEST-01", doc_root, code_root).status == "resolved"

    # Move/rename the annotated code file to a brand-new path within the code tree.
    moved_to = code_root / "renamed_pkg" / "moved_module.py"
    moved_to.parent.mkdir()
    shutil.move(str(code_root / "sample_module.py"), str(moved_to))

    result = vdce.resolve_edge("TEST-01", doc_root, code_root)
    assert result.status == "resolved"  # NOT broken_edge -- the move did not break the edge
    # Re-found at the NEW path -> identity is the annotation, never a stored path.
    assert result.code_sites[0].file == "renamed_pkg/moved_module.py"


# --- (c) real breakage fires -----------------------------------------------------------

def test_c_breakage_fires(tmp_path):
    doc_root, code_root = _copy_fixture(tmp_path)
    code = code_root / "sample_module.py"
    code.write_text(
        code.read_text(encoding="utf-8").replace("    # rule: TEST-01\n", ""),
        encoding="utf-8",
    )
    result = vdce.resolve_edge("TEST-01", doc_root, code_root)
    assert result.status == "broken_edge"
    assert result.code_sites == ()


# --- (d) duplicate guard ---------------------------------------------------------------

def test_d_duplicate_guard(tmp_path):
    doc_root, code_root = _copy_fixture(tmp_path)
    (code_root / "dup_module.py").write_text(
        "def other():\n    # rule: TEST-01\n    return 0\n", encoding="utf-8"
    )
    result = vdce.resolve_edge("TEST-01", doc_root, code_root)
    assert result.status == "ambiguous"
    assert len(result.code_sites) == 2


# --- string-literal isolation (tokenize, not raw grep) ---------------------------------

def test_string_literal_is_not_a_false_hit(tmp_path):
    """A `# rule: ID` inside a string literal must NOT count as an annotation."""
    doc_root, code_root = _copy_fixture(tmp_path)
    (code_root / "sample_module.py").write_text(
        'NOTE = "see # rule: TEST-01 in the docs"\n', encoding="utf-8"
    )
    result = vdce.resolve_edge("TEST-01", doc_root, code_root)
    assert result.status == "broken_edge"  # the string mention is not a real comment token


# --- iter_doc_rule_ids: doc-side enumeration (Phase-2 advisory-check seed, #194) --------

def test_iter_collects_all_ids(tmp_path):
    (tmp_path / "a.md").write_text("rule one <!-- rule: ALPHA-1 -->\n", encoding="utf-8")
    (tmp_path / "b.md").write_text("rule two <!-- rule: BETA.2 -->\n", encoding="utf-8")
    assert vdce.iter_doc_rule_ids(tmp_path) == {"ALPHA-1", "BETA.2"}


def test_iter_empty_when_no_annotations(tmp_path):
    (tmp_path / "plain.md").write_text("no rule tokens here\n", encoding="utf-8")
    assert vdce.iter_doc_rule_ids(tmp_path) == set()


def test_iter_exclude_top_skips_named_trees(tmp_path):
    """Illustrative tokens in excluded trees (a `docs/`-style record, a root log) must NOT
    register as live edges -- only the governed-doc token survives the exclusion."""
    (tmp_path / "PLAYBOOK.md").write_text("governed <!-- rule: LIVE-1 -->\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "adr.md").write_text(
        "example <!-- rule: ILLUS-1 -->\n", encoding="utf-8"
    )
    (tmp_path / "JOURNAL.md").write_text(
        "wrap quoted <!-- rule: ILLUS-2 -->\n", encoding="utf-8"
    )
    assert vdce.iter_doc_rule_ids(
        tmp_path, exclude_top=("docs", "JOURNAL.md")
    ) == {"LIVE-1"}


# --- deployed audit check: check_doc_code_edge (#194 sub-arc-1 advisory) ----------------

def _as_hub(tmp_path, monkeypatch):
    """Point audit._REPO_ROOT at a tmp dir so the hub-only guard passes for that dir."""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))


def test_edge_check_skips_non_hub_repo(tmp_path):
    findings = aud.check_doc_code_edge(tmp_path / "some-child")
    assert len(findings) == 1
    assert findings[0].check_name == "doc_code_edge"
    assert findings[0].status == "pass"
    assert "hub-only" in findings[0].evidence


def test_edge_check_warns_on_broken_edge(tmp_path, monkeypatch):
    _as_hub(tmp_path, monkeypatch)
    (tmp_path / "PLAYBOOK.md").write_text("a rule <!-- rule: GOV-1 -->\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "thing.py").write_text(
        "def f():\n    return 1\n", encoding="utf-8")  # no `# rule: GOV-1` annotation
    findings = aud.check_doc_code_edge(tmp_path)
    assert all(f.status != "fail" for f in findings)        # WARN-only contract, never FAIL
    assert len(findings) == 1
    assert findings[0].status == "warn"
    assert "GOV-1" in findings[0].evidence
    assert "broken_edge" in findings[0].evidence
    assert "|" not in findings[0].evidence                  # markdown-table-safe evidence


def test_edge_check_passes_on_resolved_edge(tmp_path, monkeypatch):
    _as_hub(tmp_path, monkeypatch)
    (tmp_path / "PLAYBOOK.md").write_text("a rule <!-- rule: GOV-2 -->\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "thing.py").write_text(
        "def f():\n    # rule: GOV-2\n    return 1\n", encoding="utf-8")
    findings = aud.check_doc_code_edge(tmp_path)
    assert len(findings) == 1
    assert findings[0].status == "pass"
    assert "resolved" in findings[0].evidence


def test_edge_check_advisory_inactive_when_no_annotations(tmp_path, monkeypatch):
    _as_hub(tmp_path, monkeypatch)
    (tmp_path / "PLAYBOOK.md").write_text("no rule tokens here\n", encoding="utf-8")
    findings = aud.check_doc_code_edge(tmp_path)
    assert findings[0].status == "pass"
    assert "advisory inactive" in findings[0].evidence


def test_edge_check_excludes_record_trees(tmp_path, monkeypatch):
    """Operator concern-1 fix: illustrative tokens in docs/ + JOURNAL.md + tests/ must NOT
    register as live edges -- else the check WARNs on prose in immutable design records."""
    _as_hub(tmp_path, monkeypatch)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "adr.md").write_text(
        "example token `<!-- rule: PB-07 -->`\n", encoding="utf-8")
    (tmp_path / "JOURNAL.md").write_text("wrap quoting <!-- rule: ID -->\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "fix.md").write_text("<!-- rule: TEST-01 -->\n", encoding="utf-8")
    findings = aud.check_doc_code_edge(tmp_path)
    assert findings[0].status == "pass"
    assert "advisory inactive" in findings[0].evidence


def test_edge_check_registered_and_inactive_on_live_repo():
    """Registered in ALL_CHECKS (count 23) AND the LIVE hub scan is genuinely empty: every
    live `<!-- rule: -->` token sits in an excluded record/fixture tree, so the advisory is
    honestly inactive (never FAILs). This is the run the operator required before asserting 0."""
    assert aud.check_doc_code_edge in aud.ALL_CHECKS
    assert len(aud.ALL_CHECKS) == 23
    findings = aud.check_doc_code_edge(Path(aud._REPO_ROOT))
    assert len(findings) == 1
    assert findings[0].status == "pass"
    assert "advisory inactive" in findings[0].evidence
