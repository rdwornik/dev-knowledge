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
import subprocess

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


# --- rule 5: non-Python source families FPG-1's AST pass cannot see -------------
# W4-4 Done-contract 3: `templates/*.ps1` and `tests/fixtures/**` used to fall through
# every rule above to the "unmapped" fail-safe -- correct but total, and the queue
# item this closes is that it made a pairing over them partial rather than precise.

@pytest.mark.live_repo
def test_a_changed_template_selects_the_tests_that_reference_it():
    """A `.ps1` template has no import edge; the connection is the literal filename
    a test uses to find it (`templates/dispatch-shim.ps1` -> `"dispatch-shim.ps1"`)."""
    sel = impacted_tests.select(REPO_ROOT, ["templates/dispatch-shim.ps1"])
    assert "tests/test_dispatch_shim.py" in sel.test_files
    assert not sel.full_suite


@pytest.mark.live_repo
def test_a_changed_fixture_selects_the_tests_that_reference_its_directory():
    """A fixture file is data, not an import; the connection is the literal fixture
    directory name a test uses to find it (`fixtures/connection_loop` -> `"connection_loop"`)."""
    sel = impacted_tests.select(REPO_ROOT, ["tests/fixtures/connection_loop/sitecustomize.py"])
    assert "tests/test_connection_loop.py" in sel.test_files
    assert not sel.full_suite


@pytest.mark.live_repo
def test_a_fixture_change_does_not_fall_back_to_the_doc_marker_tier():
    """Before this rule, a `.md` fixture (like `negative-contract.md`) fell through to
    the doc rule and selected only `live_repo`-marked files -- not `test_connection_loop.py`,
    which carries no such marker, so the actual covering test was silently dropped."""
    sel = impacted_tests.select(REPO_ROOT, ["tests/fixtures/connection_loop/negative-contract.md"])
    assert "tests/test_connection_loop.py" in sel.test_files
    assert sel.marker is None


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


# The EXACT approved grandfather set. A size bound is not a ratchet: swapping one
# entry out for a new uncovered script keeps the count at four and slips straight
# through, which is how the earlier `len(...) <= 4` form of this pin was defeated
# (reviewer finding, 2026-09-11). Membership is the checkable surface, so an
# addition has to edit THIS line, where it is seen.
APPROVED_GRANDFATHER = frozenset({
    "scripts/codemap/cli.py",
    "scripts/codemap_hook.py",
    "scripts/toc/cli.py",
    "scripts/toc_hook.py",
})


def test_the_grandfather_set_is_a_ratchet():
    """It may shrink, never grow -- a new untested script is what leg (b) refuses."""
    live = impacted_tests.ZERO_COVER_GRANDFATHERED
    added = set(live) - APPROVED_GRANDFATHER
    assert added == set(), (
        f"{sorted(added)} joined the grandfather set. It may only SHRINK -- an "
        "uncovered script entering it is precisely what leg (b) exists to refuse. "
        "Write the RED-first witness instead; widening the exemption needs an "
        "operator ruling recorded here, not a set literal edit."
    )
    assert len(live) <= len(APPROVED_GRANDFATHER)
    for rel in live:
        assert (REPO_ROOT / rel).exists(), (
            f"{rel} is grandfathered but gone -- shrink the set rather than carrying "
            "a name that no longer resolves"
        )


def test_machine_read_config_under_a_source_root_is_not_treated_as_prose():
    """`hooks.json` IS behaviour, so it must not select only the live-tree marker.

    Reviewer HIGH, 2026-09-11: DOC_SUFFIXES matched `.json` anywhere, so changing
    `plugins/tier1-lifecycle/hooks/hooks.json` selected just `-m live_repo` and missed the
    unmarked witness covering malformed-`hooks.json` handling. The fail-safe direction for
    a class the import graph cannot map is the FULL SUITE.
    """
    sel = impacted_tests.select(
        REPO_ROOT, ["plugins/tier1-lifecycle/hooks/hooks.json"])
    assert sel.full_suite, (
        "a machine-read config file under a source root must fail safe to the full "
        f"suite, not select a marker tier; got marker={sel.marker!r} "
        f"files={len(sel.test_files)}"
    )
    assert sel.pytest_args() == [], "the full suite takes no narrowing arguments"


def test_prose_under_a_source_root_still_gets_the_cheap_tier():
    """The fix above must not swallow plugin documentation -- that costs the saving.

    A README under `plugins/` genuinely can only break a live-tree assertion, so it stays
    on the marker tier. This pins the boundary so a later widening of CONFIG_SUFFIXES
    cannot quietly route all prose to the full suite.
    """
    sel = impacted_tests.select(REPO_ROOT, ["plugins/tier1-lifecycle/README.md"])
    assert not sel.full_suite, (
        "prose under a source root must not trigger the full suite -- that is the "
        "wall-clock saving this mechanism exists to produce"
    )
    assert sel.marker == impacted_tests.LIVE_REPO_MARKER


def test_a_staged_RENAME_is_inside_the_guards_scope():
    """A rename to an uncovered name must be refused, not invisible.

    Reviewer HIGH, 2026-09-11, and a regression the self-scoping fix introduced:
    `--diff-filter=ACM` reports NOTHING for a staged rename, so renaming a covered script
    to an uncovered name skipped the guard. Measured in a throwaway repo: `git mv a.py
    b.py` yields `[]` under ACM and `['b.py']` under ACMR. pre-commit's own staged list
    includes renamed destinations, so ACM was narrower than the wiring it replaced.

    This pins the FILTER, because the alternative -- staging a real rename inside the lane
    to observe it -- mutates the tree under test.
    """
    import inspect

    src = inspect.getsource(impacted_tests.staged_from_git)
    assert "--diff-filter=ACMRT" in src, (
        "staged_from_git must include R (rename) and T (typechange). Dropping R makes a "
        "rename to an uncovered script invisible to the guard; dropping D stays correct "
        "because a deletion is not a missing witness."
    )
    assert "--diff-filter=ACM\"" not in src and "--diff-filter=ACM'" not in src, (
        "the bare ACM filter is the rename gap; do not restore it"
    )


def test_the_guard_cannot_be_disarmed_by_its_own_wiring():
    """The hook's scope must NOT come from a `files:` regex the commit can narrow.

    Reviewer HIGH, 2026-09-11: with `files: '^scripts/.*\\.py$'`, a commit that added an
    uncovered `scripts/new_tool.py` AND narrowed that regex in the same act skipped the
    hook -- pre-commit evaluates the staged config, so the gate was removable by the
    change it exists to inspect. The guard now reads the staged set itself, and this pin
    is what makes re-introducing a filter RED instead of a quiet narrowing.
    """
    import yaml

    config = yaml.safe_load((REPO_ROOT / ".pre-commit-config.yaml").read_text(
        encoding="utf-8"))
    rows = [
        hook
        for repo in config["repos"]
        for hook in repo.get("hooks", [])
        if hook.get("id") == "impacted-tests-guard"
    ]
    assert len(rows) == 1, f"expected exactly one impacted-tests-guard row, got {len(rows)}"
    row = rows[0]

    assert row.get("always_run") is True, (
        "the guard must always_run; a scope that comes from pre-commit's file list is a "
        "scope the inspected commit can edit"
    )
    assert row.get("pass_filenames") is False, (
        "pass_filenames must be false -- the guard determines the staged set itself"
    )
    for narrowing in ("files", "exclude", "types", "types_or"):
        assert narrowing not in row, (
            f"`{narrowing}:` reintroduces a mutable selector on the guard row. That is "
            "the self-disarm this pin exists to refuse: narrow it and the commit adding "
            "an uncovered script stops being inspected. Widen scope in "
            "`impacted_tests.GUARD_ROOT` instead, where a test can see it."
        )


def test_deleting_a_script_is_not_refused_as_uncovered():
    """A removed script has no inbound edges -- that is not a missing witness.

    `changed_from_git` reports deletions (bare `git diff --name-only`), so without an
    existence filter the guard would block a commit that removes a script and its
    tests, naming a RED-first test for a file that is gone.
    """
    findings = impacted_tests.guard_findings(
        REPO_ROOT, ["scripts/a_script_that_was_deleted_by_this_commit.py"]
    )
    assert findings == [], (
        "a deleted script must not be refused as zero-selection; the guard names a "
        f"test to write for a file that no longer exists: {findings}"
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


# =============================================================================================
# lane-verify-in-lane (W4B-4), Done-contract 1: selection from the LANE'S OWN diff.
#
# `origin/main...<lane>` (merge-base triple-dot) rather than `changed_from_git`'s two-dot
# working-tree-vs-ref, because the two-dot form also carries whatever main did AFTER the lane
# branched -- exactly the thing a lane-side verification must not be charged for. Every test
# below builds a synthetic git repo (never the live hub or its worktrees, per the contract's
# "what NOT to do") with real branches, so the merge-base arithmetic is exercised for real.
# =============================================================================================

def _git(repo: pathlib.Path, *args: str) -> str:
    cmd = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
           "-c", "core.hooksPath=", *args]
    done = subprocess.run(cmd, cwd=repo, check=True, capture_output=True, text=True)
    return done.stdout.strip()


def _write(repo: pathlib.Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")


def _commit(repo: pathlib.Path, files: dict[str, str], message: str) -> str:
    _write(repo, files)
    _git(repo, "add", "-A")
    _git(repo, "commit", "--no-verify", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def lane_repo(tmp_path: pathlib.Path) -> pathlib.Path:
    """main with one module+test, and a `lane` branch checked out at its tip."""
    root = tmp_path / "lane-src"
    root.mkdir()
    _git(root, "init", "-b", "main")
    _commit(root, {
        "pyproject.toml": '[tool.pytest.ini_options]\npythonpath = ["scripts"]\n',
        "scripts/mod.py": "def value():\n    return 1\n",
        "tests/test_mod.py": "import mod\n\n\ndef test_value():\n    assert mod.value() == 1\n",
    }, "base")
    _git(root, "checkout", "-b", "lane")
    return root


def test_the_lane_diff_mode_ignores_what_main_did_after_the_lane_branched(lane_repo):
    """The two-dot form would blame the lane for main's own later commit; triple-dot must not."""
    _commit(lane_repo, {"scripts/mod.py": "def value():\n    return 2\n"}, "lane touches mod")
    _git(lane_repo, "checkout", "main")
    _commit(lane_repo, {"scripts/other.py": "Y = 1\n",
                        "tests/test_other.py": "def test_other():\n    assert False\n"},
           "main moves on after the lane branched")
    _git(lane_repo, "checkout", "lane")

    sel = impacted_tests.select_lane_diff(lane_repo, main_ref="main", lane_ref="lane")

    assert sel.test_files == ("tests/test_mod.py",), (
        "main's own post-branch commit must not appear in the lane's own diff"
    )


def test_integrator_regenerated_files_are_excluded_from_lane_diff_selection(lane_repo):
    """A lane's copy of an index the integrator regenerates at merge must not tax it.

    Citation for the exclusion set: protocols/PLAYBOOK.md "Index freshness on lane
    material" ("the audits index, the intake index, the organ index ... regenerated
    once, by the integrator, at the merge") and `.claude/commands/lane-integrate.md`
    item 4b / [#590] for the audits index concretely.
    """
    for rel in impacted_tests.INTEGRATOR_REGENERATED_FILES:
        _write(lane_repo, {rel: "stale copy\n"})
    _git(lane_repo, "add", "-A")
    _git(lane_repo, "commit", "--no-verify", "-m", "lane's stale copies of the regenerated indices")

    sel = impacted_tests.select_lane_diff(lane_repo, main_ref="main", lane_ref="lane")

    assert sel.test_files == () and not sel.full_suite, (
        "a diff containing ONLY integrator-regenerated files must select nothing and must "
        "never fall back to the full suite -- there is nothing here for the lane to answer for"
    )
    for rel in impacted_tests.INTEGRATOR_REGENERATED_FILES:
        assert sel.reasons[rel][0] == "integrator-regenerated"


def test_a_regenerated_file_is_excluded_even_inside_a_mixed_diff(lane_repo):
    _commit(lane_repo, {
        "scripts/mod.py": "def value():\n    return 2\n",
        "docs/audits/README.md": "stale copy\n",
    }, "real change plus a stale regenerated index")

    sel = impacted_tests.select_lane_diff(lane_repo, main_ref="main", lane_ref="lane")

    assert sel.test_files == ("tests/test_mod.py",)
    assert sel.reasons["docs/audits/README.md"][0] == "integrator-regenerated"


def test_the_old_two_dot_mode_is_unchanged_by_the_new_lane_diff_entry_point(lane_repo):
    """Common rule 8: a new mode, never a changed flag on the old one."""
    sel = impacted_tests.select(lane_repo, ["scripts/mod.py"])
    assert sel.test_files == ("tests/test_mod.py",)


def test_changed_from_lane_diff_raises_on_a_bad_ref_instead_of_selecting_nothing(lane_repo):
    """Codex terra HIGH: `check=False` with no returncode check meant an invalid/unfetched
    ref (e.g. `select-lane` called before `git fetch origin`) silently returned `[]`, and
    an empty selection reads as "nothing to verify", not "the ref lookup failed"."""
    with pytest.raises(RuntimeError, match="git diff"):
        impacted_tests.changed_from_lane_diff(lane_repo, "origin/main", "lane")


@pytest.mark.live_repo
def test_a_rows_only_change_maps_to_the_funnel_test():
    """Finding 3 (DIGEST-WAVE4-FINAL): a tasks/*.md row must map to the funnel detector.

    Before this rule a `tasks/*.md` change fell through to the generic doc-marker tier,
    which only selects files carrying the `live_repo` marker -- and
    `tests/test_funnel_lifecycle.py` carries no such marker, so it was silently dropped.
    """
    sel = impacted_tests.select(REPO_ROOT, ["tasks/960-some-row.md"])
    assert "tests/test_funnel_lifecycle.py" in sel.test_files
    assert not sel.full_suite


@pytest.mark.live_repo
def test_a_rows_only_change_does_not_fall_back_to_the_full_suite():
    sel = impacted_tests.select(REPO_ROOT, ["tasks/960-some-row.md"])
    assert not sel.full_suite, "a tasks/*.md row is mapped, not unmapped"


# --- LANE-5A-2 Done-contract item 2: the merge-receipts ledger never forces FULL SUITE ---
# The ledger (`logs/MERGE-RECEIPTS.jsonl`) sits in nearly every merge diff -- every merge
# folds one appended line into it. Before this rule it matched no rule in the table, so it
# fell to the "unmapped" fail-safe: replaying this selector on the five wave-4b merge diffs
# (docs/audits/2026-09-23-technical-lane-test-selection-measured-proof.md) returned
# `full_suite=True` on all five for that reason alone, and `gates.py`'s per-merge gate
# REFUSES rather than runs a selector's FULL SUITE answer -- so the ledger's own presence,
# not anything it broke, was enough to red the gate.

@pytest.mark.live_repo
def test_the_merge_receipts_ledger_never_forces_the_full_suite():
    sel = impacted_tests.select(REPO_ROOT, [impacted_tests.MERGE_RECEIPTS_LEDGER])
    assert not sel.full_suite
    assert "tests/test_merge_receipt.py" in sel.test_files


@pytest.mark.live_repo
def test_the_ledger_alongside_a_normal_diff_still_does_not_force_the_full_suite():
    """The ledger is present in EVERY wave-4b merge diff replayed for this lane's proof
    table; a real diff always carries it beside other, unrelated changes."""
    sel = impacted_tests.select(
        REPO_ROOT, [impacted_tests.MERGE_RECEIPTS_LEDGER, "JOURNAL.md"]
    )
    assert not sel.full_suite


# --- LANE-5A-2 Done-contract item 1: a prose/generated edit no longer unions in the ------
# --- corpus-wide 58-file `live_repo` tier on top of a mixed diff's own selection ---------
# Measured (docs/audits/2026-09-23-technical-lane-test-selection-measured-proof.md): on the
# same five merge diffs with the ledger set aside, the OLD selector added 58-60 files to
# every mixed diff (the whole `live_repo`-marked corpus); the fix below removes that.

@pytest.mark.live_repo
def test_a_mixed_diff_does_not_union_in_the_corpus_wide_live_repo_tier():
    """`scripts/journal_anchor.py` alone has a truth set of ONE covering test (pinned by
    `test_a_changed_source_selects_the_test_that_covers_it` above); a `JOURNAL.md` change
    in the SAME diff must not add anything beyond that one file."""
    code_only = impacted_tests.select(REPO_ROOT, ["scripts/journal_anchor.py"])
    mixed = impacted_tests.select(REPO_ROOT, ["scripts/journal_anchor.py", "JOURNAL.md"])
    assert mixed.marker == "live_repo", "the doc tier still matched -- it must stay reachable"
    assert set(mixed.test_files) == set(code_only.test_files), (
        f"a prose file in the same diff added {set(mixed.test_files) - set(code_only.test_files)} "
        "-- the marker was resolved into the lane's own file list again"
    )


@pytest.mark.live_repo
def test_the_prose_tier_stays_reachable_on_its_own_in_a_mixed_diff():
    """The doc tier is not dropped -- it is *decoupled*, so whoever runs it (the
    integrator, once per batch) can still get it, separately from the lane's own run."""
    sel = impacted_tests.select(REPO_ROOT, ["scripts/journal_anchor.py", "JOURNAL.md"])
    assert sel.docs_tier_args() == ["-m", "live_repo"]
    assert "-m" not in sel.pytest_args(), "the lane's own run must not be narrowed by it"


@pytest.mark.live_repo
def test_docs_tier_args_is_none_when_nothing_prose_matched():
    sel = impacted_tests.select(REPO_ROOT, ["scripts/journal_anchor.py"])
    assert sel.docs_tier_args() is None


@pytest.mark.live_repo
def test_docs_tier_args_matches_pytest_args_in_the_pure_docs_case():
    """The already-declared `/ship` docs-only tier is unchanged by this fix."""
    sel = impacted_tests.select(REPO_ROOT, ["JOURNAL.md"])
    assert sel.docs_tier_args() == sel.pytest_args() == ["-m", "live_repo"]
