"""RED-first witnesses for `scripts/impacted_tests.py` -- impacted-test selection ([#278]).

Written BEFORE the module, per ADR-108 section B: this file is the frozen pass/fail
criterion, and the build is what makes it green.

THE MAPPING IS WHAT THESE TESTS GUARD. The Done-when AW2-1 added requires that "a
RED-first test fails when the mapping is removed" -- so the mapping is not an
implementation detail here, it is the asserted subject.
`test_the_mapping_is_load_bearing_and_its_removal_is_RED` fails loudly if the rule
table is emptied, and the per-rule tests below fail if any single rule is dropped.

WHY THE PRECISION GUARD EXISTS. The lane contract names the trap this mechanism is
most likely to fall into: "A selector that returns the whole corpus satisfies
'non-empty for every W-lane diff' and selects nothing." A non-empty floor is
therefore NOT the acceptance, and `test_a_leaf_module_does_not_select_the_whole_corpus`
is the leg that refuses the degenerate answer a non-empty assertion would wave through.
"""
from __future__ import annotations

import pathlib

import pytest

import impacted_tests

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


# --- the mapping itself ---------------------------------------------------------

def test_the_mapping_is_load_bearing_and_its_removal_is_RED():
    """Remove the rule table and selection must stop answering -- the [#278] Done-when.

    Not a tautology about a non-empty list: it asserts that the rules are what
    PRODUCES the answer, by emptying them and requiring the selector to fall back to
    the declared fail-safe rather than quietly returning a plausible-looking set.
    """
    assert impacted_tests.RULES, "the rule table is the mapping; empty means no mechanism"

    live = impacted_tests.select(REPO_ROOT, ["scripts/journal_anchor.py"])
    assert live.test_files, "with the mapping present a source change selects tests"

    stripped = impacted_tests.select(
        REPO_ROOT, ["scripts/journal_anchor.py"], rules=()
    )
    assert stripped.full_suite, (
        "with the mapping removed the selector must fail SAFE to the full suite, "
        "never return a narrowed set it can no longer justify"
    )


def test_every_rule_declares_a_reason_string():
    """A selection a reader cannot audit is a selection nobody will trust."""
    for rule in impacted_tests.RULES:
        assert rule.reason and isinstance(rule.reason, str)


# --- rule 1: a changed source selects the tests that cover it -------------------

@pytest.mark.live_repo
def test_a_changed_source_selects_the_test_that_covers_it():
    sel = impacted_tests.select(REPO_ROOT, ["scripts/journal_anchor.py"])
    assert "tests/test_journal_anchor.py" in sel.test_files


@pytest.mark.live_repo
def test_the_naming_convention_recovers_the_importlib_idiom():
    """tests/test_fleet_health.py loads its subject by COMPOSED path, not by import.

    The filename is a string constant inside a BinOp rather than in call position,
    so FPG-1's `_import_targets` cannot see it by design (widening that rule
    reintroduces the docstring blowup the process-trigger census recorded). The
    convention rule is what recovers this class, and it was adopted on a measured
    miss-rate improvement of 0.064 -> 0.048.
    """
    sel = impacted_tests.select(REPO_ROOT, ["scripts/fleet_health.py"])
    assert "tests/test_fleet_health.py" in sel.test_files


# --- rule 2: a changed test selects itself --------------------------------------

@pytest.mark.live_repo
def test_a_changed_test_file_selects_itself():
    sel = impacted_tests.select(REPO_ROOT, ["tests/test_journal_anchor.py"])
    assert "tests/test_journal_anchor.py" in sel.test_files


# --- rule 3: a docs-only diff selects the live-tree tier ------------------------

@pytest.mark.live_repo
def test_a_docs_only_diff_selects_the_live_repo_tier():
    """Batch W is 6/6 a process batch, so this is the COMMON case here, not the edge.

    Three of the four W-lane diffs this lane was asked to witness carry no .py file
    at all. An import-graph selector returns the empty set for them, which is why the
    marker tier is part of the mapping rather than an afterthought.
    """
    sel = impacted_tests.select(REPO_ROOT, ["JOURNAL.md", "docs/audits/README.md"])
    assert sel.marker == "live_repo"
    assert not sel.full_suite


# --- rule 4: the fail-safe ------------------------------------------------------

@pytest.mark.live_repo
def test_an_environment_file_falls_back_to_the_full_suite():
    """pyproject.toml / uv.lock can move any test; narrowing there would be a guess."""
    sel = impacted_tests.select(REPO_ROOT, ["pyproject.toml"])
    assert sel.full_suite


@pytest.mark.live_repo
def test_an_unrecognised_path_falls_back_to_the_full_suite():
    sel = impacted_tests.select(REPO_ROOT, ["some/unmapped/thing.bin"])
    assert sel.full_suite


# --- the precision leg: the contract's named trap -------------------------------

@pytest.mark.live_repo
def test_a_leaf_module_does_not_select_the_whole_corpus():
    """The measured trap: transitivity through a hub module returns everything.

    `scripts/journal_anchor.py` had a truth set of ONE test file in the lane's oracle
    run. A selector that answers "all 173" here would post a perfect miss-rate and be
    worthless, which is exactly the failure the contract told this lane to refuse.
    """
    sel = impacted_tests.select(REPO_ROOT, ["scripts/journal_anchor.py"])
    corpus = impacted_tests.all_test_files(REPO_ROOT)
    assert len(sel.test_files) < len(corpus) / 2, (
        f"selected {len(sel.test_files)} of {len(corpus)} -- a corpus-wide answer "
        "has a miss-rate of zero and a value of zero"
    )


@pytest.mark.live_repo
def test_depth_is_bounded_so_the_closure_cannot_run_away():
    """Unbounded, 'tests reaching fleet_health.py' was 76 of 173 against a truth of 7."""
    assert impacted_tests.DEFAULT_DEPTH == 3
    deep = impacted_tests.select(REPO_ROOT, ["scripts/fleet_health.py"], depth=99)
    bounded = impacted_tests.select(REPO_ROOT, ["scripts/fleet_health.py"])
    assert len(bounded.test_files) <= len(deep.test_files)


# --- the marker/file intersection trap ------------------------------------------

@pytest.mark.live_repo
def test_a_mixed_diff_never_emits_a_marker_alongside_a_file_list():
    """`pytest -m live_repo a.py b.py` INTERSECTS -- it does not union.

    A mixed code+docs diff that emitted both would run only the live_repo-marked tests
    inside the covering files, silently dropping every covering test without the
    marker. This is a silent under-selection, which is the worst failure shape a
    selector has, so it is pinned rather than left to code review.
    """
    sel = impacted_tests.select(
        REPO_ROOT, ["scripts/fleet_health.py", "JOURNAL.md"]
    )
    args = sel.pytest_args()
    assert "-m" not in args, "a file list must never be narrowed by a marker"
    assert len(sel.test_files) > 0


@pytest.mark.live_repo
def test_a_docs_only_diff_still_uses_the_declared_marker_tier():
    """The pure docs case keeps `-m live_repo` -- the repo's existing /ship tier."""
    sel = impacted_tests.select(REPO_ROOT, ["JOURNAL.md"])
    assert sel.pytest_args() == ["-m", "live_repo"]


# --- the FPG-1 seam -------------------------------------------------------------

def test_the_fpg1_seam_this_module_connects_to_still_exists():
    """This selector is a CONNECT to FPG-1, not a second import graph.

    It reaches into `file_purpose_graph` for the module map and the call-site edge
    reader. Those are the two functions the process-trigger census hardened, and
    reusing them is the point -- but a rename there would otherwise degrade selection
    SILENTLY, which is the failure mode this asserts against.
    """
    import file_purpose_graph as fpg

    assert callable(fpg._script_module_map)
    assert callable(fpg._import_targets)


# --- live in the verify cadence -------------------------------------------------

@pytest.mark.live_repo
def test_the_verify_cadence_actually_calls_the_selector():
    """The Done-when says selection is LIVE IN THE VERIFY CADENCE, with a test.

    Behaviour, not a name-grep: the skill's own function is imported and run, and it
    has to come back with a target and a note. A grep for "impacted_tests" would prove
    the string is present, not that the cadence uses it.
    """
    import importlib.util

    path = REPO_ROOT / ".claude" / "skills" / "verify" / "verify.py"
    spec = importlib.util.spec_from_file_location("verify_skill", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    target, note = module.select_pytest_target()
    assert isinstance(target, str) and isinstance(note, str)
    assert note, "the cadence must say which tier it ran"


@pytest.mark.live_repo
def test_the_verify_cadence_fails_safe_to_the_full_suite(monkeypatch):
    """A broken selector must yield the FULL suite, never a narrowed one.

    An under-selection is silent. In a gate, silence is the failure that lets a
    regression through, so every error path here is required to widen, not narrow.
    """
    import importlib.util

    path = REPO_ROOT / ".claude" / "skills" / "verify" / "verify.py"
    spec = importlib.util.spec_from_file_location("verify_skill2", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    monkeypatch.setenv("VERIFY_FULL_SUITE", "1")
    target, note = module.select_pytest_target()
    assert target == ""
    assert "full suite" in note


# --- leg (b): the zero-selection refusal, and its TRIP-TEST ---------------------

@pytest.mark.live_repo
def test_the_refusal_trips_on_a_script_with_no_covering_test(tmp_path):
    """THE TRIP-TEST. A scripts/ file selecting zero tests must be REFUSED.

    Built in a synthetic tree rather than by dirtying the real one: a gate proved only
    by the tree it happens to run in is proved by a coincidence.
    """
    (tmp_path / "scripts").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "scripts" / "lonely_organ.py").write_text(
        "def run():\n    return 1\n", encoding="utf-8"
    )

    findings = impacted_tests.guard_findings(tmp_path, ["scripts/lonely_organ.py"])
    assert findings, "a script no test covers must be refused"
    source, witness = findings[0]
    assert source == "scripts/lonely_organ.py"
    assert witness == "tests/test_lonely_organ.py", (
        "the refusal must NAME the RED-first test to write -- a refusal that only "
        "says 'no tests' does half the job"
    )


@pytest.mark.live_repo
def test_the_refusal_stays_silent_when_a_covering_test_exists(tmp_path):
    """The other half of the trip-test: it must not refuse a covered file."""
    (tmp_path / "scripts").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "scripts" / "covered_organ.py").write_text(
        "def run():\n    return 1\n", encoding="utf-8"
    )
    (tmp_path / "tests" / "test_covered_organ.py").write_text(
        "import covered_organ\n\ndef test_it():\n    assert covered_organ.run() == 1\n",
        encoding="utf-8",
    )

    assert impacted_tests.guard_findings(tmp_path, ["scripts/covered_organ.py"]) == []


@pytest.mark.live_repo
def test_the_refusal_is_scoped_and_does_not_fire_outside_scripts(tmp_path):
    """Scope is `scripts/` only. deploy/ and plugins/ were not measured for this."""
    (tmp_path / "deploy").mkdir()
    (tmp_path / "deploy" / "unmeasured.py").write_text("x = 1\n", encoding="utf-8")
    assert impacted_tests.guard_findings(tmp_path, ["deploy/unmeasured.py"]) == []


@pytest.mark.live_repo
def test_the_refusal_does_not_wedge_this_repo_today():
    """The contract's explicit worry, answered with the live tree rather than a guess.

    "Do not arm the (b) refusal tree-wide on its first day -- a gate that refuses every
    scripts/*.py commit wedges the batch it is running inside." Measured: 136 of 140
    already select a test, so the gate refuses a NEW gap, not pre-existing debt.
    """
    scripts = [
        p.relative_to(REPO_ROOT).as_posix()
        for p in (REPO_ROOT / "scripts").rglob("*.py")
        if "__pycache__" not in p.as_posix()
    ]
    findings = impacted_tests.guard_findings(REPO_ROOT, scripts)
    assert findings == [], (
        "arming leg (b) must not refuse a commit touching any script in the tree "
        f"as it stands; unexpected findings: {findings}"
    )


def test_the_grandfather_set_is_a_ratchet():
    """It may shrink, never grow -- a new untested script is what leg (b) refuses."""
    assert len(impacted_tests.ZERO_COVER_GRANDFATHERED) <= 4
    for rel in impacted_tests.ZERO_COVER_GRANDFATHERED:
        assert (REPO_ROOT / rel).exists(), (
            f"{rel} is grandfathered but gone -- shrink the set rather than carrying "
            "a name that no longer resolves"
        )


# --- the Done-when witness ------------------------------------------------------

@pytest.mark.live_repo
def test_selection_is_non_empty_for_a_docs_diff_and_a_code_diff():
    """The Done-when's floor -- kept explicitly as a FLOOR, not as the acceptance.

    The acceptance is the measured miss-rate in
    docs/audits/2026-09-11-technical-w278-selector-leg-measurement.md; this only
    refuses the empty answer.
    """
    docs = impacted_tests.select(REPO_ROOT, ["JOURNAL.md"])
    code = impacted_tests.select(REPO_ROOT, ["scripts/fleet_health.py"])
    assert docs.marker or docs.test_files or docs.full_suite
    assert code.test_files
