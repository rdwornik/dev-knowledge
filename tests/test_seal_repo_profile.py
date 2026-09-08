"""The repo-profile seam -- the fix for the two hub-local seal rules (batch V, V-3).

`docs/audits/2026-09-09-technical-seal-rule-attribution.md` measured the defect: Rule B and
Rule C are pure functions of a path string, carry no repo identity, and therefore apply the
hub's own audit-class enum and the hub's own home tuple to every repository they are pointed
at. Measured over the nine ratified members that manufactures 308 of the fleet's 336 WAIVEs.

Each rule splits into a FLEET leg that travels and a REPO-LOCAL leg that does not, and the
spec already writes both halves down:

    Rule B   fleet: the YYYY-MM-DD- date shape and the R4 casing rule
             repo-local: the audit class enum (`audit_class_enum_scope: repo-local`)
    Rule C   fleet: the docs/ genre-tree rule (`docs` is not a home, by design)
             repo-local: the home tuple ("never with the hub's tuple")

These tests pin both halves in both directions, and they pin the property that makes the
change safe to land: the HUB's behaviour is unchanged, so every gate that already calls
these functions keeps its verdicts.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
_P = _REPO / "scripts" / "validate_hermetization.py"


def _load():
    spec = importlib.util.spec_from_file_location("validate_hermetization", _P)
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_hermetization"] = module
    spec.loader.exec_module(module)
    return module


vh = _load()


# --- the seam exists at all ----------------------------------------------------------

def test_the_two_rules_take_a_repo_profile():
    """The defect in one assertion: before the fix these functions had no repo identity."""
    assert hasattr(vh, "RepoProfile")
    assert hasattr(vh, "HUB_PROFILE")
    assert hasattr(vh, "FLEET_PROFILE")
    assert vh.rule_b_violation("docs/audits/x.md", vh.FLEET_PROFILE) is not None
    assert vh.rule_c_violation("tests/deep/nest/x.py", vh.FLEET_PROFILE) is None


def test_the_fleet_profile_declares_neither_repo_local_leg():
    assert vh.FLEET_PROFILE.audit_class_enum is None
    assert vh.FLEET_PROFILE.home_patterns is None


def test_the_hub_profile_declares_both_from_the_spec():
    assert vh.HUB_PROFILE.audit_class_enum == vh.AUDIT_CLASS_ENUM
    assert vh.HUB_PROFILE.home_patterns == vh._HOME_PATTERNS


# --- the hub's own behaviour does not move -------------------------------------------

def test_the_default_profile_is_the_hub_profile():
    """Every existing caller passes no profile, so the default decides whether the fix is
    a change of behaviour at the hub. It is not."""
    samples = [
        "notes.txt", "newpkg/mod.py", "docs/newgenre/x.md",
        "docs/audits/2026-01-01-technical-a-slug.md",
        "docs/audits/2026-01-01-Estate_Recon.md",
        "docs/audits/2026-01-01-estate-recon.md",
        "docs/loose.md", "tests/extractor/fixtures/x.json",
        "scripts/audit_checks/x.py", "src/pkg/deep/mod.py",
    ]
    for p in samples:
        assert vh.classify(p) == vh.classify(p, vh.HUB_PROFILE), p


def test_rule_c_still_admits_every_tracked_path_in_the_live_repo():
    """The spec cannot silently stop describing the tree it governs -- the same direction
    `tests/test_fleet_shape_spec.py` asserts, re-asserted through the profile seam."""
    out = subprocess.run(["git", "-C", str(_REPO), "ls-files"],
                         capture_output=True, text=True, encoding="utf-8")
    assert out.returncode == 0
    refused = [p for p in out.stdout.splitlines()
               if p.strip() and vh.rule_a_violation(p) is None
               and vh.rule_c_violation(p) is not None]
    assert refused == []


# --- Rule B: the class enum is repo-local, the casing and date legs are fleet ---------

def test_an_undeclared_repo_does_not_inherit_the_hub_audit_class_enum():
    """corp-monorepo's 28 lowercase, well-formed, heavily-cited audit files -- class B2,
    194 items fleet-wide -- refused for one reason: a vocabulary that is not theirs."""
    path = "docs/audits/2026-07-05-estate-recon.md"
    assert vh.rule_b_violation(path, vh.HUB_PROFILE) is not None
    assert vh.rule_b_violation(path, vh.HUB_PROFILE).startswith("class:")
    assert vh.rule_b_violation(path, vh.FLEET_PROFILE) is None


def test_the_r4_casing_leg_travels_to_an_undeclared_repo():
    """The casing leg is a fleet clause and a consumer already runs it locally, so the fix
    must not switch it off along with the enum."""
    path = "docs/audits/2026-07-05-ESTATE_RECON.md"
    for profile in (vh.HUB_PROFILE, vh.FLEET_PROFILE):
        reason = vh.rule_b_violation(path, profile)
        assert reason is not None and reason.startswith("casing:"), profile.name


def test_the_date_shape_leg_travels_to_an_undeclared_repo():
    path = "docs/audits/estate-recon.md"
    for profile in (vh.HUB_PROFILE, vh.FLEET_PROFILE):
        reason = vh.rule_b_violation(path, profile)
        assert reason is not None and reason.startswith("grammar:"), profile.name


def test_a_repo_that_declares_its_own_enum_is_policed_by_that_enum():
    profile = vh.RepoProfile(name="demo", audit_class_enum=frozenset({"brief", "deck"}))
    assert vh.rule_b_violation("docs/audits/2026-01-01-brief-q3.md", profile) is None
    assert vh.rule_b_violation("docs/audits/2026-01-01-deck.md", profile) is None
    reason = vh.rule_b_violation("docs/audits/2026-01-01-technical-x.md", profile)
    assert reason is not None and reason.startswith("class:")


def test_a_declared_enum_still_requires_a_well_formed_slug():
    profile = vh.RepoProfile(name="demo", audit_class_enum=frozenset({"brief"}))
    reason = vh.rule_b_violation("docs/audits/2026-01-01-brief--q3.md", profile)
    assert reason is not None and reason.startswith("slug:")


# --- Rule C: the home tuple is repo-local, the docs/ genre rule is fleet --------------

@pytest.mark.parametrize("path", [
    "tests/extractor/fixtures/sample.json",   # corp -- 20 tests/* homes
    "config/rfp/prompts/system.md",           # corp -- 10 config/* homes
    "scripts/typewhisper/main.py",            # win-tooling -- scripts/<tool>/
    "templates/_PPTX_TEMPLATE_KIT/a.pptx",    # demo-prep -- templates/*
])
def test_an_undeclared_repo_does_not_inherit_the_hub_home_tuple(path):
    """Class H1, 72 items: a sanctioned directory organized one level deeper than the hub
    organizes it. The hub refuses each of these; an undeclared consumer must not be."""
    assert vh.rule_c_violation(path, vh.HUB_PROFILE) is not None
    assert vh.rule_c_violation(path, vh.FLEET_PROFILE) is None


def test_the_docs_root_leg_is_fleet_and_survives_an_undeclared_repo():
    """`docs` itself is not a home -- the spec states that absence as the rule this clause
    exists to state, and it is what caught both of Rule C's genuine fleet findings."""
    for profile in (vh.HUB_PROFILE, vh.FLEET_PROFILE):
        assert vh.rule_c_violation("docs/2026-08-28-nb2-lane-b-packet.md",
                                   profile) is not None, profile.name


def test_a_genre_tree_is_the_repos_own_business_in_an_undeclared_repo():
    """Below a sanctioned genre, depth is the repo's structure, not the hub's."""
    assert vh.rule_c_violation("docs/decisions/transcripts/2026-01-01-x.md",
                               vh.FLEET_PROFILE) is None
    assert vh.rule_c_violation("docs/audits/2026-01-01-bundle/blinded/x.md",
                               vh.FLEET_PROFILE) is None


def test_a_repo_that_declares_its_own_homes_is_policed_by_them():
    profile = vh.RepoProfile(name="demo", home_patterns=("tests", "tests/*"))
    assert vh.rule_c_violation("tests/unit/x.py", profile) is None
    assert vh.rule_c_violation("tests/unit/deep/x.py", profile) is not None


# --- the archive shape: one grammar rule, not six literals ---------------------------

@pytest.mark.parametrize("home", [
    "protocols/archive", "templates/archive", "tasks/archive",
    "docs/decisions/archive", "docs/intake/archive",
    "scripts/archive",              # corp -- class H3, the item the six literals miss
])
def test_sanctioned_parent_archive_is_one_grammar_rule(home):
    assert vh.is_allowed_home(home)


def test_archive_under_an_unsanctioned_parent_is_still_refused():
    """The generalization is `<allowed-home>/archive`, not `<anything>/archive`."""
    assert not vh.is_allowed_home("warehouse/archive")
    assert not vh.is_allowed_home("docs/archive/deep/archive")


# --- the declaration surface ---------------------------------------------------------

def _write(root: Path, body: str) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / ".methodology.yaml").write_text(body, encoding="utf-8")
    return root


def test_profile_for_repo_reads_the_repos_own_methodology_yaml(tmp_path):
    root = _write(tmp_path / "demo", """
sanctioned_divergences: []
shape_profile:
  audit_class_enum:
    - brief
    - deck
  home_patterns:
    - tests
    - tests/*
""")
    profile = vh.profile_for_repo(root)
    assert profile.name == "demo"
    assert profile.audit_class_enum == frozenset({"brief", "deck"})
    assert profile.home_patterns == ("tests", "tests/*")


def test_profile_for_repo_without_a_declaration_is_the_fleet_profile(tmp_path):
    root = _write(tmp_path / "plain", "sanctioned_divergences: []\n")
    profile = vh.profile_for_repo(root)
    assert profile.audit_class_enum is None
    assert profile.home_patterns is None


def test_profile_for_repo_without_a_methodology_file_is_the_fleet_profile(tmp_path):
    root = tmp_path / "bare"
    root.mkdir()
    profile = vh.profile_for_repo(root)
    assert profile.audit_class_enum is None
    assert profile.home_patterns is None


def test_a_half_declaration_arms_only_the_half_it_declares(tmp_path):
    root = _write(tmp_path / "half", """
shape_profile:
  audit_class_enum:
    - brief
""")
    profile = vh.profile_for_repo(root)
    assert profile.audit_class_enum == frozenset({"brief"})
    assert profile.home_patterns is None


def test_a_malformed_declaration_is_refused_rather_than_silently_ignored(tmp_path):
    """Fail-closed, matching `ShapeSpecError`: a declaration the reader cannot parse means
    the rule has no vocabulary, and a seal that silently admits everything is worse than
    one that says why it cannot start."""
    root = _write(tmp_path / "bad", "shape_profile:\n  audit_class_enum: technical\n")
    with pytest.raises(vh.ShapeSpecError):
        vh.profile_for_repo(root)


# --- the seal, run over a whole repository -------------------------------------------

def test_seal_repo_reports_items_at_the_declared_grain():
    """Rule A per item, Rule B per file, Rule C per distinct home -- the grain both
    predecessor seal reports declare, so their numbers and this one are commensurable."""
    report = vh.seal_repo(_REPO)
    assert report.profile.name == ".dev-knowledge"
    assert report.rule_a_items == []
    assert report.rule_c_homes == []
    assert len(report.rule_b_files) == report.item_count - len(report.rule_a_items)
    assert all(p.startswith("docs/audits/") for p in report.rule_b_files)


def test_seal_repo_is_read_only_against_the_repo_it_reads(tmp_path):
    """The seal reads a consumer with `git ls-files` and writes nothing -- the property
    every consumer run of this organ has been asserted on by hand until now."""
    root = tmp_path / "clean"
    root.mkdir()
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    (root / "notes.txt").write_text("x", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "notes.txt"], check=True)
    before = sorted(p.name for p in root.iterdir())
    report = vh.seal_repo(root)
    assert report.item_count == 1
    assert sorted(p.name for p in root.iterdir()) == before
    status = subprocess.run(["git", "-C", str(root), "status", "--porcelain"],
                            capture_output=True, text=True)
    assert status.stdout.strip() == "A  notes.txt"
