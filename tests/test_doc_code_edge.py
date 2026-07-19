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


@pytest.mark.live_repo
def test_edge_check_registered_and_resolves_starter_set():
    """Registered in ALL_CHECKS (count 28) AND the LIVE hub scan resolves the post-#202 set over
    the declaration-doc registry: 12 enforced rules -- the 5 cohort-1 (seal-journal-anchor /
    canonical-freshness / coherence-spec-reconciled / coherence-amendment / governance-backlog-
    schema) + the #201 governance trio (governance-no-ff / -child-floor / -backlog-leave) + the
    #202 Tier-3 quartet (coherence-doc-claims / -rot / -structure, handoff-probes-bind), the
    multi-organ ones via ADR-90 -- each resolve doc<->code; the edge is REAL + advisory (never
    FAILs)."""
    assert aud.check_doc_code_edge in aud.ALL_CHECKS
    assert len(aud.ALL_CHECKS) == 31  # 30 -> 31: check_residual_completeness added (ARC-5 residual gate, 2026-07-19); 29 -> 30: check_fleet_parity added ([#337], 2026-07-18); 28 -> 29: check_import_edges (#249, 2026-07-06); 29 -> 28: check #7 retired (ADR-51 amend. 2026-07-05)
    findings = aud.check_doc_code_edge(Path(aud._REPO_ROOT))
    assert all(f.status != "fail" for f in findings)        # advisory: never FAIL
    assert len(findings) == 1
    assert findings[0].status == "pass"
    assert "13 doc" in findings[0].evidence                 # 5 cohort-1 + trio + Tier-3 quartet + governance-backlog-story-id (#286)
    assert "resolved" in findings[0].evidence


def test_edge_check_warns_on_code_orphan(tmp_path, monkeypatch):
    """Step-3 live wiring (#194 L1): the advisory ALSO surfaces a code-side ORPHAN -- a
    `# rule:` whose ID is declared in NO declaration doc (code->nonexistent-rule) -- as a WARN,
    never FAIL. This is the direction the doc-side resolution alone structurally cannot see."""
    _as_hub(tmp_path, monkeypatch)
    _write_registry(tmp_path)
    (tmp_path / "PLAYBOOK.md").write_text("no governed tokens here\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "thing.py").write_text(            # `# rule:` with NO declaration
        "def f():\n    # rule: gov-orphan\n    return 1\n", encoding="utf-8")
    findings = aud.check_doc_code_edge(tmp_path)
    assert all(f.status != "fail" for f in findings)          # WARN-only contract, never FAIL
    assert any("gov-orphan" in f.evidence and "code_orphan" in f.evidence for f in findings)


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

    # broken_edge: doc rule, no matching code annotation. Drop the resolved-state ok.py first --
    # else its GOV-OK now surfaces as a code_orphan (Step-3 L1 wiring) and splits this state's
    # finding count; each state must stay exactly one Finding for the (not-vacuous) guard.
    (tmp_path / "scripts" / "ok.py").unlink()
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

    # code_orphan (Step-3 L1 wiring): a `# rule:` declared in no doc = code->nonexistent-rule.
    for _p in (tmp_path / "scripts").glob("*.py"):
        _p.unlink()
    (tmp_path / "PLAYBOOK.md").write_text("no governed tokens here\n", encoding="utf-8")
    (tmp_path / "scripts" / "orphan.py").write_text(
        "def f():\n    # rule: GOV-ORPHAN\n    return 1\n", encoding="utf-8")
    findings += aud.check_doc_code_edge(tmp_path)

    assert len(findings) == 6  # one Finding per state -> all six exercised (not vacuous)
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
@pytest.mark.live_repo
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


@pytest.mark.live_repo
def test_coverage_all_in_scope_rules_resolve():
    """Every rule-ID in coverage_scope (the #194 in-scope enforced rules) must resolve doc<->code.

    SCOPE: this guards the CURATED `coverage_scope` list -- cohort-1's 5 in-scope rules -- NOT
    every enforced rule. The deferred tail is OUTSIDE this guard: the two-organ governance trio
    (#201) and the Tier-3 quartet (#202), with #203 owed to mechanize the drift-guard over
    ALL_CHECKS. So a GREEN result means "cohort-1's 5 edges resolve," NOT "rollout complete."

    Resolves each against the LIVE hub (declaration docs at repo root, code under scripts/) --
    the same repo-wide resolution check_doc_code_edge performs. The assertion message names any
    rule that regresses to broken_edge/ambiguous (or is scoped without its annotation).
    """
    scope = aud._load_coverage_scope(_REPO_ROOT)
    assert scope, "coverage_scope is empty/absent -- the guard would vacuously pass"
    code_root = _REPO_ROOT / "scripts"
    decl = aud._load_declaration_docs(_REPO_ROOT)  # registry-scoped resolution (matches the live check)
    multi = aud._load_multi_site(_REPO_ROOT)       # ADR-90 multi-site counts (matches the live check)
    unresolved = [
        rid for rid in scope
        if vdce.resolve_edge(rid, _REPO_ROOT, code_root,
                             include=decl, multi_site=multi).status != "resolved"
    ]
    assert not unresolved, (
        f"{len(unresolved)}/{len(scope)} in-scope rules not yet resolved: "
        + ", ".join(sorted(unresolved))
    )


# --- registry-scoped resolution regression guard (#194 doc-site-scoping fix) -----------
# Permanent guard for the scan/resolve ASYMMETRY: enumeration (iter_doc_rule_ids) was
# registry-scoped while resolution (find_doc_sites) scanned every *.md, so a real rule-ID
# quoted in PROSE in a non-declaration doc (an immutable audit file discussing the token)
# was counted as a second doc-site -> the real edge went `ambiguous`. This is a STRUCTURAL
# guard, not a symptom guard: it constructs the colliding doc itself, so it keeps teeth even
# if the audit file that first triggered it ever changes.

def test_resolution_is_registry_scoped_not_fooled_by_prose_mention(tmp_path):
    """A real rule-ID quoted in prose in a NON-declaration doc must NOT count as a doc-site:
    registry-scoped resolution (the `include` declaration-doc list) stays `resolved`, never
    `ambiguous`. The UNSCOPED form is asserted to STILL be fooled, proving the scoping -- not the
    absence of a colliding doc -- is what fixes it."""
    (tmp_path / "PLAYBOOK.md").write_text("governed <!-- rule: GOV-9 -->\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "impl.py").write_text(
        "def f():\n    # rule: GOV-9\n    return 1\n", encoding="utf-8")
    # a NON-declaration doc quotes the same real token in prose (the audit-file collision class)
    (tmp_path / "docs" / "audits").mkdir(parents=True)
    (tmp_path / "docs" / "audits" / "report.md").write_text(
        "the audit notes <!-- rule: GOV-9 --> resolves to impl.py\n", encoding="utf-8")

    code_root = tmp_path / "scripts"
    # registry-scoped: only PLAYBOOK.md is a declaration doc -> 1 doc-site -> resolved
    scoped = vdce.resolve_edge("GOV-9", tmp_path, code_root, include=("PLAYBOOK.md",))
    assert scoped.status == "resolved", \
        f"scoped resolution must ignore the prose mention, got {scoped.status}"
    assert len(scoped.doc_sites) == 1 and scoped.doc_sites[0].file == "PLAYBOOK.md"
    # teeth: the UNSCOPED form IS fooled (2 doc-sites -> ambiguous) -- scoping is the fix
    unscoped = vdce.resolve_edge("GOV-9", tmp_path, code_root)
    assert unscoped.status == "ambiguous"


# --- L1 structural-integrity scan + rebuildable index (#194 "Done when", the seal) -----
# The binding #194 closure clause: "the scheme + structural check flag a fixture's
# dangling/duplicate rule-IDs, tested." These prove the seal on an ISOLATED fixture copy:
#   * ENFORCEMENT  -- scan_structural_integrity flags dangling (BOTH directions: declared-
#     unimplemented + code->nonexistent-rule) and duplicate (BOTH sides), and is SILENT on a
#     clean resolved edge (negative control -- no false positives).
#   * REBUILDABLE INDEX -- build_edge_index is (a) deterministic (two rebuilds equal) and
#     (b) derived-from-source: mutating the fixture (implement the dangling rule in code) and
#     rebuilding flips that edge to resolved (round-trip), proving the index is rebuilt every
#     scan, NEVER hand-maintained (ADR-88 P3; the fit-check's "no central manifest").
# DETECT-first / advisory -- the scan returns findings, never raises, never gates.

_STRUCT_FIXTURE = _REPO_ROOT / "tests" / "fixtures" / "doc-code-structural"


def _copy_struct_fixture(tmp_path):
    """Copy the structural fixture into a tmp tree (ISOLATED copy); doc + code share one dir,
    so both roots = it. Negative-control + mutation work on this copy, NEVER the committed
    fixture (the same isolation pattern as _copy_fixture for the move-safety proofs)."""
    dst = tmp_path / "struct"
    shutil.copytree(_STRUCT_FIXTURE, dst)
    return dst


def test_structural_scan_flags_dangling_and_duplicate(tmp_path):
    """THE SEAL: scan_structural_integrity flags every structural defect on the fixture --
    dangling (both directions) + duplicate (both sides) -- and is silent on the clean edge."""
    root = _copy_struct_fixture(tmp_path)
    findings = vdce.scan_structural_integrity(root, root, include=("doc.md",))
    got = {(f.rule_id, f.kind) for f in findings}
    assert got == {
        ("dangling-doc-1", "dangling_doc"),    # declared, no code impl
        ("code-orphan-1", "code_orphan"),      # `# rule:` with no declaration (code->nonexistent-rule)
        ("dup-doc-1", "duplicate_doc"),        # two doc sites
        ("dup-code-1", "duplicate_code"),      # two code sites
    }, f"unexpected structural findings: {sorted(got)}"
    # negative control: the clean resolved edge is NEVER flagged (no false positive)
    assert all(f.rule_id != "clean-ok" for f in findings)


def test_structural_scan_silent_when_no_defects(tmp_path):
    """A tree with only a resolved edge -> no findings (the scan does not cry wolf)."""
    (tmp_path / "doc.md").write_text("ok <!-- rule: only-ok -->\n", encoding="utf-8")
    (tmp_path / "impl.py").write_text(
        "def f():\n    # rule: only-ok\n    return 1\n", encoding="utf-8")
    assert vdce.scan_structural_integrity(tmp_path, tmp_path, include=("doc.md",)) == []


def test_edge_index_rebuilds_deterministically(tmp_path):
    """The derived index is a pure function of source: two rebuilds are byte-for-byte equal,
    and it really resolved (statuses present, not a vacuous empty dict)."""
    root = _copy_struct_fixture(tmp_path)
    idx1 = vdce.build_edge_index(root, root, include=("doc.md",))
    idx2 = vdce.build_edge_index(root, root, include=("doc.md",))
    assert idx1 == idx2
    assert idx1["clean-ok"].status == "resolved"
    assert idx1["dangling-doc-1"].status == "broken_edge"   # doc present, code absent
    assert idx1["code-orphan-1"].status == "broken_edge"    # code present, doc absent


def test_edge_index_round_trip_reflects_source_mutation(tmp_path):
    """The index is REBUILT from source, never hand-held: implement the dangling rule in the
    isolated copy, rebuild, and the edge flips broken_edge -> resolved (the round-trip proof)."""
    root = _copy_struct_fixture(tmp_path)
    before = vdce.build_edge_index(root, root, include=("doc.md",))
    assert before["dangling-doc-1"].status == "broken_edge"
    impl = root / "impl.py"
    impl.write_text(
        impl.read_text(encoding="utf-8")
        + "\n\ndef now_implemented():\n    # rule: dangling-doc-1\n    return 0\n",
        encoding="utf-8")
    after = vdce.build_edge_index(root, root, include=("doc.md",))
    assert after["dangling-doc-1"].status == "resolved"     # the rebuild reflected the mutation


def test_iter_code_rule_ids_collects_comment_tokens_only(tmp_path):
    """The code-side enumerator (the missing half of the index) reads real COMMENT tokens
    only -- a `# rule:` inside a string literal is never collected."""
    (tmp_path / "a.py").write_text(
        "def f():\n    # rule: CODE-1\n    return 1\n", encoding="utf-8")
    (tmp_path / "b.py").write_text(
        'NOTE = "see # rule: STRING-ONLY here"\n', encoding="utf-8")
    assert vdce.iter_code_rule_ids(tmp_path) == {"CODE-1"}


# --- ADR-90 resolver-allows-N: declared multi-site rules (#201) -------------------------
# A rule legitimately enforced in N `# rule:`-able code organs declares its expected count in
# `multi_site`; resolve_edge resolves it at EXACTLY that count + ONE doc site. Any other code
# count (incl. +/-1) stays `ambiguous` -- the duplicate-guard keeps its teeth for declared organs.

def _write_two_organ(tmp_path, n_code=2, n_doc=1, rid="GOV-2ORG"):
    """A tmp tree: `n_doc` doc declaration(s) of `rid` + `n_code` `# rule: rid` code sites."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "PLAYBOOK.md").write_text(
        "".join(f"decl {i} <!-- rule: {rid} -->\n" for i in range(n_doc)), encoding="utf-8")
    scripts = tmp_path / "scripts"
    scripts.mkdir(exist_ok=True)
    for i in range(n_code):
        (scripts / f"organ{i}.py").write_text(
            f"def f{i}():\n    # rule: {rid}\n    return {i}\n", encoding="utf-8")
    return tmp_path, scripts


def test_multi_site_resolves_at_declared_count(tmp_path):
    """A 2-code-site rule is `ambiguous` under the strict 1:1 guard but `resolved` once multi_site
    declares count 2 (the core #201 capability)."""
    root, code_root = _write_two_organ(tmp_path, n_code=2)
    strict = vdce.resolve_edge("GOV-2ORG", root, code_root, include=("PLAYBOOK.md",))
    assert strict.status == "ambiguous"                       # 2 code sites, no declaration
    declared = vdce.resolve_edge("GOV-2ORG", root, code_root,
                                 include=("PLAYBOOK.md",), multi_site={"GOV-2ORG": 2})
    assert declared.status == "resolved"
    assert len(declared.code_sites) == 2


def test_multi_site_count_mismatch_still_ambiguous(tmp_path):
    """The duplicate-guard keeps its teeth: count+1 (an undeclared extra organ) AND count-1 (a
    lost organ) both stay `ambiguous` -- declaring N does NOT relax to '>=1'."""
    over, over_code = _write_two_organ(tmp_path / "over", n_code=3)
    r_over = vdce.resolve_edge("GOV-2ORG", over, over_code,
                               include=("PLAYBOOK.md",), multi_site={"GOV-2ORG": 2})
    assert r_over.status == "ambiguous" and len(r_over.code_sites) == 3      # 3 != declared 2
    under, under_code = _write_two_organ(tmp_path / "under", n_code=1)
    r_under = vdce.resolve_edge("GOV-2ORG", under, under_code,
                                include=("PLAYBOOK.md",), multi_site={"GOV-2ORG": 2})
    assert r_under.status == "ambiguous" and len(r_under.code_sites) == 1    # 1 != declared 2


def test_multi_site_relaxes_code_side_only_doc_stays_1to1(tmp_path):
    """multi_site governs the CODE side; >1 doc site is still `ambiguous` (declare at one source)."""
    root, code_root = _write_two_organ(tmp_path, n_code=2, n_doc=2)
    r = vdce.resolve_edge("GOV-2ORG", root, code_root,
                          include=("PLAYBOOK.md",), multi_site={"GOV-2ORG": 2})
    assert r.status == "ambiguous"                            # 2 doc sites -> ambiguous regardless


def test_multi_site_unlisted_rule_keeps_strict_guard(tmp_path):
    """A rule ABSENT from multi_site keeps the strict 1:1 duplicate-guard even when other rules
    are declared multi-site (per-rule opt-in, conservative default)."""
    root, code_root = _write_two_organ(tmp_path, n_code=2, rid="UNLISTED-1")
    r = vdce.resolve_edge("UNLISTED-1", root, code_root,
                          include=("PLAYBOOK.md",), multi_site={"OTHER-2ORG": 2})
    assert r.status == "ambiguous"                            # not in the map -> strict >1 guard


def test_multi_site_no_duplicate_code_structural_finding_at_count(tmp_path):
    """scan_structural_integrity does NOT raise `duplicate_code` for a declared multi-site rule at
    its expected count (the index threads multi_site), but DOES above it."""
    at_root, _ = _write_two_organ(tmp_path / "at", n_code=2)
    at = vdce.scan_structural_integrity(at_root, at_root / "scripts",
                                        include=("PLAYBOOK.md",), multi_site={"GOV-2ORG": 2})
    assert not [f for f in at if f.kind == "duplicate_code"]               # 2 == declared 2
    over_root, _ = _write_two_organ(tmp_path / "over", n_code=3)
    over = vdce.scan_structural_integrity(over_root, over_root / "scripts",
                                          include=("PLAYBOOK.md",), multi_site={"GOV-2ORG": 2})
    assert [f for f in over if f.kind == "duplicate_code"]                 # 3 > declared 2


def test_load_multi_site_failsoft(tmp_path):
    """audit._load_multi_site fail-soft contract: missing / malformed / non-mapping -> {}; only
    str->int(>=2) entries kept (a bool / count<1 / non-int is dropped)."""
    assert aud._load_multi_site(tmp_path) == {}                            # absent file
    eco = tmp_path / "ecosystem"
    eco.mkdir()
    (eco / "doc-code-edge.yaml").write_text("multi_site: [unclosed", encoding="utf-8")
    assert aud._load_multi_site(tmp_path) == {}                            # malformed YAML
    (eco / "doc-code-edge.yaml").write_text("multi_site: notamap\n", encoding="utf-8")
    assert aud._load_multi_site(tmp_path) == {}                            # non-mapping value
    (eco / "doc-code-edge.yaml").write_text(
        "multi_site:\n  good-2: 2\n  good-3: 3\n  bad-one: 1\n  bad-bool: true\n  bad-str: x\n",
        encoding="utf-8")
    assert aud._load_multi_site(tmp_path) == {"good-2": 2, "good-3": 3}    # only str->int>=2


_MULTI_RULES = [
    # #201 governance trio + retro coherence-spec-reconciled
    ("governance-no-ff", 3),
    ("governance-child-floor", 2),
    ("governance-backlog-leave", 3),
    ("coherence-spec-reconciled", 2),
    # #202 Tier-3 quartet (adapter + logic module, count 2 each)
    ("coherence-doc-claims", 2),
    ("coherence-doc-rot", 2),
    ("coherence-doc-structure", 2),
    ("handoff-probes-bind", 2),
]


@pytest.mark.parametrize("rule_id, count", _MULTI_RULES)
@pytest.mark.live_repo
def test_governance_multi_site_rules_resolve_live(rule_id, count):
    """The real multi-organ rules resolve doc<->code on the LIVE hub at their declared count: the
    #201 governance trio + retro coherence-spec-reconciled + the #202 Tier-3 quartet (each an
    audit.py adapter + its validate_*/verify_* logic module), via the live multi_site map. #201
    demonstrated on real 2-/3-site rules (e.g. governance-no-ff: validate_no_ff detect +
    block_ff_push prevent + check_no_ff_merges adapter)."""
    decl = aud._load_declaration_docs(_REPO_ROOT)
    multi = aud._load_multi_site(_REPO_ROOT)
    assert multi.get(rule_id) == count, f"multi_site must declare {rule_id}={count}, got {multi.get(rule_id)}"
    code_root = _REPO_ROOT / "scripts"
    r = vdce.resolve_edge(rule_id, _REPO_ROOT, code_root, include=decl, multi_site=multi)
    assert r.status == "resolved", f"{rule_id}: {r.status} (code sites={len(r.code_sites)})"
    assert len(r.code_sites) == count                          # all N organs annotated + found


# --- #203 coverage drift-guard (the demonstrated catch) --------------------------------
# check_doc_code_coverage_drift FAILs when an ALL_CHECKS member is neither annotated with a
# coverage_scope `# rule:` marker NOR exempt -- so a NEW enforced rule can't silently escape the
# curated scope. The TEETH are proven by SEEDING such a member and asserting the flag NAMES it
# (a test that never exercises the flag proves nothing -- #195/#207).

# Module-level fakes (inspect.getsource needs them at module scope). check_fake_mapped carries a
# real above-def marker; the other two carry none.
def check_fake_undeclared(repo_path):   # no marker, not exempt -> must be FLAGGED
    return []


# rule: canonical-freshness
def check_fake_mapped(repo_path):       # marker in coverage_scope -> mapped, passes
    return []


def check_fake_exempt(repo_path):       # no marker, but listed exempt -> passes
    return []


def test_markers_in_source_reads_comment_tokens_only():
    """markers_in_source collects a real `# rule:` COMMENT but NEVER one inside a string or a
    docstring -- the docstring-false-positive the tokenize approach (not a regex) exists to avoid."""
    src = (
        "def f():\n"
        "    # rule: real-one\n"
        '    note = "see # rule: string-only here"\n'
        '    """also # rule: docstring-only"""\n'
        "    return 1\n"
    )
    assert vdce.markers_in_source(src) == {"real-one"}


def test_coverage_drift_guard_flags_undeclared_check_naming_it():
    """THE TEETH (#203), helper level: the per-member core FLAGS a seeded check that is neither
    coverage_scope-annotated nor exempt, NAMING it; (B) a coverage-marked check and (C) an exempt
    check both pass (absent from the drift list)."""
    scope = {"canonical-freshness"}
    exempt = {"fake_exempt"}
    drift = aud._coverage_drift_findings(
        [check_fake_undeclared, check_fake_mapped, check_fake_exempt], scope, exempt)
    flagged = {name for name, _ in drift}
    assert flagged == {"fake_undeclared"}, f"expected only fake_undeclared flagged, got {flagged}"


@pytest.mark.live_repo
def test_coverage_drift_guard_full_check_fails_on_injected_escape(monkeypatch):
    """End-to-end teeth (the CAPTURED FLAG = #203 closure evidence): inject an unannotated,
    non-exempt member into ALL_CHECKS -> check_doc_code_coverage_drift returns a FAIL Finding that
    NAMES the escapee. Not a toothless wiring test -- it exercises the flag."""
    monkeypatch.setattr(aud, "ALL_CHECKS", list(aud.ALL_CHECKS) + [check_fake_undeclared])
    findings = aud.check_doc_code_coverage_drift(Path(aud._REPO_ROOT))
    assert len(findings) == 1
    assert findings[0].status == "fail"
    assert "fake_undeclared" in findings[0].evidence


@pytest.mark.live_repo
def test_coverage_drift_guard_registered_and_clean_on_live_repo():
    """The drift-guard is in ALL_CHECKS (count 28) and PASSES on the live repo: every member is
    either coverage_scope-annotated or exempt (the post-#203 end-state)."""
    assert aud.check_doc_code_coverage_drift in aud.ALL_CHECKS
    assert len(aud.ALL_CHECKS) == 31  # 30 -> 31: check_residual_completeness added (ARC-5 residual gate, 2026-07-19); 29 -> 30: check_fleet_parity added ([#337], 2026-07-18); 28 -> 29: check_import_edges (#249, 2026-07-06); 29 -> 28: check #7 retired (ADR-51 amend. 2026-07-05)
    findings = aud.check_doc_code_coverage_drift(Path(aud._REPO_ROOT))
    assert len(findings) == 1
    assert findings[0].status == "pass", findings[0].evidence


def test_load_coverage_exempt_failsoft(tmp_path):
    """audit._load_coverage_exempt fail-soft: missing / malformed / non-list -> set(); a valid
    list of str check-names is kept."""
    assert aud._load_coverage_exempt(tmp_path) == set()                    # absent file
    eco = tmp_path / "ecosystem"
    eco.mkdir()
    (eco / "doc-code-edge.yaml").write_text("exempt: [unclosed", encoding="utf-8")
    assert aud._load_coverage_exempt(tmp_path) == set()                    # malformed YAML
    (eco / "doc-code-edge.yaml").write_text("exempt: notalist\n", encoding="utf-8")
    assert aud._load_coverage_exempt(tmp_path) == set()                    # non-list value
    (eco / "doc-code-edge.yaml").write_text(
        "exempt:\n  - vision_md\n  - doc_code_edge\n", encoding="utf-8")
    assert aud._load_coverage_exempt(tmp_path) == {"vision_md", "doc_code_edge"}


def test_coverage_drift_guard_inert_on_empty_config(tmp_path, monkeypatch):
    """An empty coverage_scope OR exempt makes the guard report INERT (WARN), never a vacuous pass
    -- an absent config cannot silently certify every member as covered."""
    _as_hub(tmp_path, monkeypatch)
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / "ecosystem" / "doc-code-edge.yaml").write_text(
        "coverage_scope: []\nexempt: []\n", encoding="utf-8")
    findings = aud.check_doc_code_coverage_drift(tmp_path)
    assert findings[0].status == "warn"
    assert "inert" in findings[0].evidence
