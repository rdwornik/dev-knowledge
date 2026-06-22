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

import pytest

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
    assert vdce.iter_doc_rule_ids(tmp_path, include=("a.md", "b.md")) == {"ALPHA-1", "BETA.2"}


def test_iter_empty_when_no_annotations(tmp_path):
    (tmp_path / "plain.md").write_text("no rule tokens here\n", encoding="utf-8")
    assert vdce.iter_doc_rule_ids(tmp_path, include=("plain.md",)) == set()


def test_iter_include_scopes_to_listed_docs(tmp_path):
    """Registry-scoped (ADR-89 OQ1): only docs in the include-list are scanned, so a token in a
    NON-listed doc (a `docs/`-style record, a root log) is NOT discovered as a live edge."""
    (tmp_path / "PLAYBOOK.md").write_text("governed <!-- rule: LIVE-1 -->\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "adr.md").write_text(
        "example <!-- rule: ILLUS-1 -->\n", encoding="utf-8"
    )
    (tmp_path / "JOURNAL.md").write_text(
        "wrap quoted <!-- rule: ILLUS-2 -->\n", encoding="utf-8"
    )
    assert vdce.iter_doc_rule_ids(tmp_path, include=("PLAYBOOK.md",)) == {"LIVE-1"}


def test_iter_placeholder_not_matched(tmp_path):
    """Angle-bracket placeholder tokens are outside the ID charset, so a teaching example never
    registers as a live edge -- even inside a scanned declaration doc (the self-trip guard)."""
    (tmp_path / "PLAYBOOK.md").write_text(
        "teach the form: <!-- rule: <domain>-<slug> -->\n", encoding="utf-8")
    assert vdce.iter_doc_rule_ids(tmp_path, include=("PLAYBOOK.md",)) == set()


# --- deployed audit check: check_doc_code_edge (#194 sub-arc-1 advisory) ----------------

def _as_hub(tmp_path, monkeypatch):
    """Point audit._REPO_ROOT at a tmp dir so the hub-only guard passes for that dir."""
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))


def _write_registry(tmp_path, docs=("PLAYBOOK.md",)):
    """Seed the tmp hub's ecosystem/doc-code-edge.yaml include-list (declaration_docs)."""
    eco = tmp_path / "ecosystem"
    eco.mkdir(exist_ok=True)
    body = "declaration_docs:\n" + "".join(f"  - {d}\n" for d in docs)
    (eco / "doc-code-edge.yaml").write_text(body, encoding="utf-8")


def test_load_declaration_docs_failsoft(tmp_path):
    """Loader fail-soft contract: missing / malformed / non-list registry -> () (the advisory
    check renders inert, never raises); a valid list -> the declared repo-relative paths."""
    assert aud._load_declaration_docs(tmp_path) == ()                      # absent file
    eco = tmp_path / "ecosystem"
    eco.mkdir()
    (eco / "doc-code-edge.yaml").write_text("declaration_docs: [unclosed", encoding="utf-8")
    assert aud._load_declaration_docs(tmp_path) == ()                      # malformed YAML
    (eco / "doc-code-edge.yaml").write_text("declaration_docs: notalist\n", encoding="utf-8")
    assert aud._load_declaration_docs(tmp_path) == ()                      # non-list value
    (eco / "doc-code-edge.yaml").write_text(
        "declaration_docs:\n  - protocols/PLAYBOOK.md\n", encoding="utf-8")
    assert aud._load_declaration_docs(tmp_path) == ("protocols/PLAYBOOK.md",)  # happy path


def test_edge_check_skips_non_hub_repo(tmp_path):
    findings = aud.check_doc_code_edge(tmp_path / "some-child")
    assert len(findings) == 1
    assert findings[0].check_name == "doc_code_edge"
    assert findings[0].status == "pass"
    assert "hub-only" in findings[0].evidence


def test_edge_check_warns_on_broken_edge(tmp_path, monkeypatch):
    _as_hub(tmp_path, monkeypatch)
    _write_registry(tmp_path)
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
    _write_registry(tmp_path)
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
    _write_registry(tmp_path)
    (tmp_path / "PLAYBOOK.md").write_text("no rule tokens here\n", encoding="utf-8")
    findings = aud.check_doc_code_edge(tmp_path)
    assert findings[0].status == "pass"
    assert "advisory inactive" in findings[0].evidence


def test_edge_check_only_scans_listed_docs(tmp_path, monkeypatch):
    """Registry-scoped (ADR-89 OQ1): a `<!-- rule: -->` token in a doc NOT listed in
    declaration_docs is not a live edge -- so an illustrative token in a record tree / unlisted
    doc keeps the advisory honestly inactive (replaces the old hardcoded record-tree exclude)."""
    _as_hub(tmp_path, monkeypatch)
    _write_registry(tmp_path, ("PLAYBOOK.md",))
    (tmp_path / "PLAYBOOK.md").write_text("no governed tokens here\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "adr.md").write_text(
        "example token <!-- rule: ILLUS-9 -->\n", encoding="utf-8")
    findings = aud.check_doc_code_edge(tmp_path)
    assert findings[0].status == "pass"
    assert "advisory inactive" in findings[0].evidence


def test_edge_check_registered_and_resolves_starter_set():
    """Registered in ALL_CHECKS (count 23) AND the LIVE hub scan resolves the #194 cohort-1 set
    over the declaration-doc registry: 5 enforced rules (the 3 starters seal-journal-anchor /
    canonical-freshness / coherence-spec-reconciled + Phase-B coherence-amendment /
    governance-backlog-schema) each resolve doc<->code -- the edge is REAL + advisory (never FAILs)."""
    assert aud.check_doc_code_edge in aud.ALL_CHECKS
    assert len(aud.ALL_CHECKS) == 23
    findings = aud.check_doc_code_edge(Path(aud._REPO_ROOT))
    assert all(f.status != "fail" for f in findings)        # advisory: never FAIL
    assert len(findings) == 1
    assert findings[0].status == "pass"
    assert "5 doc" in findings[0].evidence                  # the 5 cohort-1 rules (Phase B)
    assert "resolved" in findings[0].evidence


# --- cp1252-safe output regression (#194 sub-arc-2; fix 633e44a had only a gotcha note) -

def test_doc_code_edge_output_is_cp1252_safe(tmp_path, monkeypatch):
    """Every Finding `check_doc_code_edge` can emit must render on a Windows cp1252 console.

    `cmd_health` prints evidence via `click.echo`, which crashes on a char outside cp1252
    (e.g. U+2192 ``->``); the resolved-state evidence once carried such a char (fixed 633e44a,
    swapped to ASCII ``->``). Guard the class at the source: drive EVERY Finding-producing
    state and assert each field encodes to cp1252. (Em-dash U+2014 in the hub-only / inactive
    evidence IS cp1252 0x97, so it must NOT trip this -- only a genuinely non-cp1252 char does,
    which is exactly the regression being fenced.)
    """
    findings = []

    # hub-only: repo_path != the real _REPO_ROOT (called before _as_hub) -> pass finding.
    findings += aud.check_doc_code_edge(tmp_path / "child-repo")

    # the remaining states run as the tmp hub.
    _as_hub(tmp_path, monkeypatch)
    _write_registry(tmp_path)
    (tmp_path / "scripts").mkdir()

    # advisory-inactive: a listed doc carries no rule annotations.
    (tmp_path / "PLAYBOOK.md").write_text("no rule tokens here\n", encoding="utf-8")
    findings += aud.check_doc_code_edge(tmp_path)

    # resolved: doc rule + matching code annotation (the state the bugged string lived in).
    (tmp_path / "PLAYBOOK.md").write_text("a rule <!-- rule: GOV-OK -->\n", encoding="utf-8")
    (tmp_path / "scripts" / "ok.py").write_text(
        "def f():\n    # rule: GOV-OK\n    return 1\n", encoding="utf-8")
    findings += aud.check_doc_code_edge(tmp_path)

    # broken_edge: doc rule, no matching code annotation.
    (tmp_path / "PLAYBOOK.md").write_text(
        "a rule <!-- rule: GOV-BROKEN -->\n", encoding="utf-8")
    findings += aud.check_doc_code_edge(tmp_path)

    # ambiguous: doc rule + two code annotations.
    (tmp_path / "PLAYBOOK.md").write_text("a rule <!-- rule: GOV-DUP -->\n", encoding="utf-8")
    (tmp_path / "scripts" / "a.py").write_text(
        "def a():\n    # rule: GOV-DUP\n    return 1\n", encoding="utf-8")
    (tmp_path / "scripts" / "b.py").write_text(
        "def b():\n    # rule: GOV-DUP\n    return 2\n", encoding="utf-8")
    findings += aud.check_doc_code_edge(tmp_path)

    assert len(findings) == 5  # one Finding per state -> all five exercised (not vacuous)
    for f in findings:
        for field in (f.check_name, f.status, f.evidence):
            field.encode("cp1252")  # non-cp1252 char -> UnicodeEncodeError -> test fails


# --- real-starter resolve/break regression (#194 sub-arc-2 annotations, under mutation) -

_STARTERS = [
    ("seal-journal-anchor", "protocols/DEFINITION_OF_DONE.md",
     "scripts/session_end_backpressure.py"),
    ("canonical-freshness", "protocols/PLAYBOOK.md", "scripts/audit.py"),
    ("coherence-spec-reconciled", "protocols/PLAYBOOK.md",
     "scripts/validate_reconciliation.py"),
]


@pytest.mark.parametrize("rule_id, doc_rel, code_rel", _STARTERS)
def test_real_starter_edges_resolve_and_break(tmp_path, rule_id, doc_rel, code_rel):
    """On REAL content + real wiring: each starter resolves as it ships AND breaking it is caught.

    Copies the live doc + code into a tmp tree (NEVER mutates the real repo), resolves the edge,
    then deletes the `# rule: <id>` code annotation and re-resolves. The automated form of a
    manual mutation -- and a regression guard if a real annotation is silently lost or changed
    (the aggregate `3 resolved` assertion catches the count, never WHICH edge broke)."""
    doc_dst = tmp_path / doc_rel
    code_dst = tmp_path / code_rel
    doc_dst.parent.mkdir(parents=True, exist_ok=True)
    code_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(_REPO_ROOT / doc_rel, doc_dst)
    shutil.copy2(_REPO_ROOT / code_rel, code_dst)

    code_root = tmp_path / "scripts"
    assert vdce.resolve_edge(rule_id, tmp_path, code_root).status == "resolved"

    # Delete ONLY this rule's code annotation (faithful to the resolver's own CODE_RE matcher;
    # robust to indentation), leaving every other line intact.
    kept = [
        line for line in code_dst.read_text(encoding="utf-8").splitlines(keepends=True)
        if not ((m := vdce.CODE_RE.search(line)) and m.group(1) == rule_id)
    ]
    code_dst.write_text("".join(kept), encoding="utf-8")

    assert vdce.resolve_edge(rule_id, tmp_path, code_root).status == "broken_edge"


# --- doc->code coverage gate (#194 Arc-1, the permanent guard) -------------------------
# Every in-scope enforced rule (ecosystem/doc-code-edge.yaml `coverage_scope:`) must resolve
# doc<->code. Committed xfail-strict in Phase A as the executable success criterion; at cohort-1
# completion (Phase B) all coverage_scope rules resolve, the xfail was removed, and this now
# stands as the PERMANENT coverage guard -- it FAILs if a future edit breaks any in-scope edge,
# or if a rule is added to coverage_scope without its doc+code annotation.


def test_coverage_all_in_scope_rules_resolve():
    """Every rule-ID in coverage_scope (the #194 in-scope enforced rules) must resolve doc<->code.

    Resolves each against the LIVE hub (declaration docs at repo root, code under scripts/) --
    the same repo-wide resolution check_doc_code_edge performs. The assertion message names any
    rule that regresses to broken_edge/ambiguous (or is scoped without its annotation).
    """
    scope = aud._load_coverage_scope(_REPO_ROOT)
    assert scope, "coverage_scope is empty/absent -- the guard would vacuously pass"
    code_root = _REPO_ROOT / "scripts"
    unresolved = [
        rid for rid in scope
        if vdce.resolve_edge(rid, _REPO_ROOT, code_root).status != "resolved"
    ]
    assert not unresolved, (
        f"{len(unresolved)}/{len(scope)} in-scope rules not yet resolved: "
        + ", ".join(sorted(unresolved))
    )
