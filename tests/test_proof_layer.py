"""`[#596]` — family 3 at the PROOF layer. RED-first.

The class, as the sweep's §9.1 addendum states it: §0–§8 swept the `ALL_CHECKS` members for a
check that **cannot compute its ground truth at run time and reports a non-failing status
anyway**. Family 3 is that defect displaced one layer — *"the PROOF that an enforcement organ
fires is itself gated on the presence of the very environment it polices. Nothing reports
`unavailable` — the test simply never runs, and the suite prints green."*

And why it is WORSE than the `unavailable` it resembles: *"`unavailable` at least renders as
N/A in the audit table, so a reader can see that a cell was not measured. A skipped test
renders as a dot in a pytest summary nobody reads line by line, and the enforcement claim it
was written to support survives in prose entirely unqualified."*

The row's done-when, leg by leg:

  1. the class is stated once in a durable home **with its predicate** — `scripts/proof_layer.py`
     is that home, and the predicate is executable rather than prose;
  2. `[#583]`'s sweep rows are shown to be **instances** of it rather than a separate list;
  3. **a fire-test demonstrates the proof layer catching a check that reports OK without
     evaluating**;
  4. the relationship between the two rows is recorded so neither absorbs the other.

Plus the contract's rider: the sweep artifact's **two named exemplars** are covered —
`tests/test_enforcement_coverage.py` (§9.3) and `tests/test_floor_conformance.py` (§9.4).
"""
from __future__ import annotations

import textwrap

import pytest

import proof_layer as pl


# --- fixtures ---------------------------------------------------------------

_MODULE_GATED = textwrap.dedent('''\
    """Proves the armed loop FUNCTIONS — the pre-commit hook fires on a poisoned floor."""
    import importlib.util
    import pytest

    pytestmark = pytest.mark.skipif(
        importlib.util.find_spec("pre_commit") is None,
        reason="pre-commit not installed — the commit-time leg cannot be exercised offline",
    )

    def test_hook_fires_on_a_poisoned_floor():
        assert True

    def test_hook_auto_arms():
        assert True
    ''')

_FUNCTION_GATED = textwrap.dedent('''\
    """The reporter measures whether enforcement FIRES, not whether files are present."""
    import importlib.util
    import pytest

    _HAS_PRECOMMIT = importlib.util.find_spec("pre_commit") is not None

    @pytest.mark.skipif(not _HAS_PRECOMMIT, reason="pre-commit not installed")
    def test_commit_time_leg_fires():
        assert True

    def test_something_unguarded():
        assert True
    ''')

_UNGATED = textwrap.dedent('''\
    """A root-layout guard that inherits no tool dependency."""
    def test_root_is_clean():
        assert True
    ''')

_WHICH_GATED = textwrap.dedent('''\
    """The hygiene scripts are pwsh-only."""
    import shutil
    from pathlib import Path
    import pytest

    PWSH = shutil.which("pwsh") or r"C:\\Program Files\\PowerShell\\7\\pwsh.exe"

    pytestmark = pytest.mark.skipif(
        not Path(PWSH).exists(), reason="pwsh 7 not present; the hygiene scripts are pwsh-only"
    )

    def test_worktree_hygiene():
        assert True
    ''')


def _tests_dir(tmp_path, **modules):
    d = tmp_path / "tests"
    d.mkdir(exist_ok=True)
    for name, text in modules.items():
        (d / f"{name}.py").write_text(text, encoding="utf-8")
    return d


# --- the predicate: detecting an environment-conditional guard --------------

def test_a_module_level_skipif_gates_every_test_in_the_module(tmp_path):
    d = _tests_dir(tmp_path, test_floor_conformance=_MODULE_GATED)
    guards = pl.scan_guards(d)
    assert len(guards) == 1
    assert guards[0].scope == pl.SCOPE_MODULE
    assert guards[0].gated_tests == 2
    assert guards[0].tool == "pre_commit"


def test_a_function_level_skipif_gates_one_test(tmp_path):
    d = _tests_dir(tmp_path, test_enforcement_coverage=_FUNCTION_GATED)
    guards = pl.scan_guards(d)
    assert len(guards) == 1
    assert guards[0].scope == pl.SCOPE_FUNCTION
    assert guards[0].gated_tests == 1


def test_a_shutil_which_probe_is_an_environment_condition(tmp_path):
    """The win-tooling exemplar's own shape (sweep §9.2)."""
    d = _tests_dir(tmp_path, test_worktree_hygiene=_WHICH_GATED)
    guards = pl.scan_guards(d)
    assert len(guards) == 1
    assert guards[0].tool == "pwsh"


def test_an_ungated_module_produces_no_guard(tmp_path):
    d = _tests_dir(tmp_path, test_repo_root_hygiene=_UNGATED)
    assert pl.scan_guards(d) == []


def test_a_skipif_on_a_non_environment_condition_is_not_family_three(tmp_path):
    """The counter-rule. Over-applying the predicate turns every conditional test into a
    defect, which is how a real class gets buried in noise."""
    d = _tests_dir(tmp_path, test_x=textwrap.dedent('''\
        import sys
        import pytest

        @pytest.mark.skipif(sys.version_info < (3, 12), reason="needs 3.12 syntax")
        def test_new_syntax():
            assert True
        '''))
    assert pl.scan_guards(d) == []


def test_an_unparseable_module_is_reported_not_skipped(tmp_path):
    """A module the scanner cannot parse is UNKNOWN, never assumed clean — assuming clean is
    the very move this whole class is about."""
    d = _tests_dir(tmp_path, test_broken="def test(:\n    pass\n")
    guards, unreadable = pl.scan_guards(d, report_unreadable=True)
    assert guards == []
    assert unreadable == ["test_broken.py"]


# --- self-policing: gated on the environment it polices ---------------------

def test_a_guard_gated_on_the_tool_its_module_polices_is_self_policing(tmp_path):
    d = _tests_dir(tmp_path, test_floor_conformance=_MODULE_GATED)
    assert pl.scan_guards(d)[0].self_policing is True


def test_a_guard_on_an_unrelated_tool_is_not_self_policing(tmp_path):
    d = _tests_dir(tmp_path, test_worktree_hygiene=_WHICH_GATED)
    guard = pl.scan_guards(d)[0]
    assert guard.self_policing is False


# --- THE FIRE-TEST: a proof that reports OK without evaluating --------------

def test_a_skipped_proof_renders_as_not_proven_never_as_proven():
    """The row's leg 3, in its sharpest form.

    `proof_status` is the §9.6 conforming pattern made general: the reporting surface derives
    its cell from THE SAME predicate the skipif uses, so a proof that did not run renders as
    `not-proven` rather than being absorbed into a green run. There is no argument for which
    this returns `proven` without the predicate being true.
    """
    guard = pl.Guard(module="test_floor_conformance.py", scope=pl.SCOPE_MODULE,
                     tool="pre_commit", gated_tests=21, self_policing=True,
                     reason="pre-commit not installed")
    assert pl.proof_status(guard, environment_present=False) == pl.NOT_PROVEN
    assert pl.proof_status(guard, environment_present=True) == pl.PROVEN
    assert pl.proof_status(guard, environment_present=None) == pl.NOT_PROVEN


def test_the_fire_test_a_planted_self_policing_guard_is_caught(tmp_path):
    """A seeded enforcement proof, gated on the very tool it polices, is CAUGHT — reported as
    a family-3 instance with its blast radius, rather than passing as a green module."""
    d = _tests_dir(tmp_path, test_enforcement_coverage=_MODULE_GATED)
    findings = pl.ratchet_findings(pl.scan_guards(d), baseline=pl.Baseline(guards=()))
    assert findings, "the planted guard was not caught"
    assert [s for s, _ in findings] == ["warn"]
    assert "test_enforcement_coverage.py" in findings[0][1]
    assert "2 test(s)" in findings[0][1]


def test_a_guard_in_the_baseline_does_not_refire(tmp_path):
    d = _tests_dir(tmp_path, test_floor_conformance=_MODULE_GATED)
    guards = pl.scan_guards(d)
    baseline = pl.Baseline(guards=tuple(g.key for g in guards))
    assert pl.ratchet_findings(guards, baseline=baseline) == []


def test_a_new_guard_surfaces_even_while_another_is_removed(tmp_path):
    """Identity-keyed, not count-keyed: the swap that a counter is blind to."""
    d = _tests_dir(tmp_path, test_enforcement_coverage=_MODULE_GATED)
    baseline = pl.Baseline(guards=("test_floor_conformance.py::<module>",))
    findings = pl.ratchet_findings(pl.scan_guards(d), baseline=baseline)
    assert [s for s, _ in findings] == ["warn"]
    assert "test_enforcement_coverage.py" in findings[0][1]


# --- leg 2: [#583]'s rows are INSTANCES, and the two exemplars are covered --

def test_the_class_declares_its_relationship_to_583():
    """Leg 4: recorded so neither row is read as absorbing the other."""
    assert pl.SITE_LAYER_ROW == "[#583]"
    assert pl.PROOF_LAYER_ROW == "[#596]"
    assert "SITE" in pl.LAYER_RELATIONSHIP
    assert "PROOF" in pl.LAYER_RELATIONSHIP


def test_the_two_named_exemplars_are_declared():
    """The contract's rider: the sweep artifact's two named exemplars are covered."""
    assert set(pl.SWEEP_EXEMPLARS) == {
        "tests/test_enforcement_coverage.py", "tests/test_floor_conformance.py"}


@pytest.mark.live_repo
def test_both_named_exemplars_are_detected_on_the_live_tree():
    """The acceptance criterion that cannot be satisfied by a fixture: the predicate finds the
    two instances the sweep found by hand, in the live `tests/` tree."""
    guards = pl.scan_guards(pl.repo_root() / "tests")
    modules = {g.module for g in guards}
    for exemplar in pl.SWEEP_EXEMPLARS:
        assert exemplar.rsplit("/", 1)[-1] in modules, (
            f"{exemplar} is a named sweep exemplar the predicate did not find; "
            f"found: {sorted(modules)}")


@pytest.mark.live_repo
def test_the_live_guard_population_is_at_or_below_its_baseline():
    """The class cannot silently re-form. A NEW environment-conditional guard surfaces by
    name; a removed one drains without complaint."""
    guards = pl.scan_guards(pl.repo_root() / "tests")
    baseline = pl.load_baseline(pl.repo_root())
    assert baseline is not None, f"{pl.BASELINE_RELPATH} is absent or malformed"
    assert set(g.key for g in guards) - set(baseline.guards) == set()
