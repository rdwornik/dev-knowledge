"""scripts/known_reds.py -- ADR-121 step 1: baseline identity, attribution, no anonymous red.

RED-FIRST (ADR-108 SS B). Every test here was authored and witnessed FAILING before
scripts/known_reds.py existed.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def kr():
    if str(_REPO) not in sys.path:
        sys.path.insert(0, str(_REPO))
    return _load("known_reds_under_test", _REPO / "scripts" / "known_reds.py")


WITNESS_1 = (
    "tests/test_graph_spine_commit_tier.py::"
    "test_the_live_spine_is_ordered_rebuild_first_and_always_runs"
)


# --- baseline id -----------------------------------------------------------------------

def test_compute_baseline_id_is_deterministic_regardless_of_dict_order(kr):
    a = {"x": {"attribution": "pre-freeze"}, "y": {"attribution": "witness"}}
    b = {"y": {"attribution": "witness"}, "x": {"attribution": "pre-freeze"}}
    assert kr.compute_baseline_id(a, date="2026-09-24") == kr.compute_baseline_id(b, date="2026-09-24")


def test_compute_baseline_id_changes_with_content(kr):
    a = {"x": {"attribution": "pre-freeze"}}
    b = {"x": {"attribution": "unattributed", "reason": "why"}}
    assert kr.compute_baseline_id(a, date="2026-09-24") != kr.compute_baseline_id(b, date="2026-09-24")


def test_compute_baseline_id_carries_the_date(kr):
    members = {"x": {"attribution": "pre-freeze"}}
    assert kr.compute_baseline_id(members, date="2026-09-24").startswith("2026-09-24-")


def test_compute_baseline_id_is_unaffected_by_an_absent_or_empty_members_by_os(kr):
    """D2 backward compatibility: a registry that never used `members_by_os` computes the
    IDENTICAL baseline id whether the new kwarg is omitted, None, or `{}` -- every registry
    written before D2 keeps its existing baseline id verbatim on the next refresh."""
    members = {"x": {"attribution": "pre-freeze"}}
    plain = kr.compute_baseline_id(members, date="2026-09-24")
    assert kr.compute_baseline_id(members, date="2026-09-24", members_by_os=None) == plain
    assert kr.compute_baseline_id(members, date="2026-09-24", members_by_os={}) == plain


def test_compute_baseline_id_changes_when_members_by_os_content_changes(kr):
    members = {"x": {"attribution": "pre-freeze"}}
    a = kr.compute_baseline_id(members, date="2026-09-24",
                               members_by_os={"windows-latest": {"y": {"attribution": "x"}}})
    b = kr.compute_baseline_id(members, date="2026-09-24",
                               members_by_os={"windows-latest": {"y": {"attribution": "z"}}})
    assert a != b
    assert a != kr.compute_baseline_id(members, date="2026-09-24")


# --- refresh -----------------------------------------------------------------------------

def test_refresh_carries_forward_previous_attribution_and_marks_witnesses(kr):
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-17-abc", measured_at_sha="old",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": _owned()})
    failed = frozenset({"tests/a.py::t1", WITNESS_1})
    registry, dropped = kr.refresh(failed=failed, workers=4, commit="new", measured_via="local",
                                   date="2026-09-24", attribution={WITNESS_1: dict(_OWNED)},
                                   previous=previous)
    assert registry.members["tests/a.py::t1"] == _owned()
    assert registry.members[WITNESS_1]["attribution"] == kr.WITNESS
    assert registry.members[WITNESS_1]["task"] == _OWNED["task"]
    assert dropped == []


def test_refresh_refuses_a_witness_that_is_not_owned_either(kr):
    with pytest.raises(kr.KnownRedsError, match="task"):
        kr.refresh(failed=frozenset({WITNESS_1}), workers=4, commit="new", measured_via="local",
                   date="2026-09-24", attribution={}, previous=None)


def test_refresh_refuses_a_new_unattributed_red(kr):
    failed = frozenset({"tests/a.py::t1", "tests/b.py::t2"})
    with pytest.raises(kr.KnownRedsError, match="tests/b.py::t2"):
        kr.refresh(failed=failed, workers=4, commit="new", measured_via="local",
                  date="2026-09-24", attribution={"tests/a.py::t1": _owned()},
                  previous=None)


def test_refresh_accepts_a_new_red_with_real_attribution(kr):
    failed = frozenset({"tests/b.py::t2"})
    attribution = {"tests/b.py::t2": _owned(
        {"attribution": {"first_bad_sha": "deadbeef", "lane": "x"}})}
    registry, _ = kr.refresh(failed=failed, workers=4, commit="new", measured_via="local",
                             date="2026-09-24", attribution=attribution, previous=None)
    assert registry.members["tests/b.py::t2"]["attribution"] == {"first_bad_sha": "deadbeef",
                                                                   "lane": "x"}


def test_refresh_drops_members_no_longer_failing(kr):
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="old",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": _owned(),
                                    "tests/fixed.py::t9": _owned()})
    registry, dropped = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new",
                                   measured_via="local", date="2026-09-24", attribution={},
                                   previous=previous)
    assert dropped == ["tests/fixed.py::t9"]
    assert "tests/fixed.py::t9" not in registry.members


def test_refresh_carries_forward_the_previous_registrys_hooks_section(kr):
    """lane-ci-signal, [#802] evidence run gh-run:36220172268: `refresh` built its next
    Registry without passing `hooks=`, so a live refresh silently dropped the committed
    `audit-health` hook registration -- caught only because the compare-hook step's own
    verdict flipped from PASS to a bare exit-1 refusal on the very next run. `hooks` carries
    no pytest node id and is never touched by the failed-set walk above it, so it must be
    carried forward unconditionally, the same way `notes` already is."""
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="old",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": _owned()},
                           hooks={"audit-health": _owned({"attribution": "environment-mismatch",
                                                          "reason": "pre-existing"})})
    registry, _ = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new",
                             measured_via="local", date="2026-09-24", attribution={},
                             previous=previous)
    assert registry.hooks == previous.hooks


def test_refresh_is_idempotent_on_the_same_failed_set(kr):
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="old",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": _owned()})
    r1, _ = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new",
                       measured_via="local", date="2026-09-24", attribution={}, previous=previous)
    r2, _ = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new",
                       measured_via="local", date="2026-09-24", attribution={}, previous=r1)
    assert r1.baseline_id == r2.baseline_id


# --- refresh: OS-keyed capture (D2, WAVE5B-N4 L2) ------------------------------------------

def test_refresh_with_os_key_writes_members_by_os_and_leaves_shared_members_untouched(kr):
    """`--os windows-latest` writes `members_by_os['windows-latest']`; the shared `members` set
    (what a plain `refresh`, e.g. ecosystem/harness.yaml's merge-moment caller, reads and
    writes) is byte-identical to before -- backward compatible for that caller."""
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="old",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": _owned()})
    registry, dropped = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new",
                                   measured_via="local", date="2026-09-24", attribution={},
                                   previous=previous, os_key="windows-latest")
    assert registry.members == previous.members
    assert registry.members_by_os == {"windows-latest": {"tests/a.py::t1": _owned()}}
    assert dropped == []


def test_refresh_os_key_stamps_a_signature_only_on_the_first_capture(kr):
    """A member's first OS-scoped capture stamps the run's observed signature (there is none
    yet); a later refresh of that same OS bucket carries the recorded signature forward
    UNCHANGED even if the run's current text differs -- the signature is the fingerprint
    `compare` diffs against, so it must not silently re-stamp on every run."""
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="old",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": _owned()})
    r1, _ = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new",
                       measured_via="local", date="2026-09-24", attribution={}, previous=previous,
                       os_key="windows-latest",
                       signatures={"tests/a.py::t1": "AssertionError: first shape"})
    assert r1.members_by_os["windows-latest"]["tests/a.py::t1"]["signature"] == \
        "AssertionError: first shape"

    r2, _ = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="newer",
                       measured_via="local", date="2026-09-25", attribution={}, previous=r1,
                       os_key="windows-latest",
                       signatures={"tests/a.py::t1": "AssertionError: DIFFERENT shape"})
    assert r2.members_by_os["windows-latest"]["tests/a.py::t1"]["signature"] == \
        "AssertionError: first shape"


def test_refresh_os_key_first_capture_never_inherits_the_shared_entrys_own_signature(kr):
    """Codex terra HIGH, 2026-09-27: a shared entry can already carry a signature (stamped by a
    plain `os_key=None` refresh, captured on WHATEVER OS ran it). The first OS-scoped capture of
    that same member must never adopt it as if it were this OS's own fingerprint -- it
    establishes a fresh one from the current run's `signatures` instead."""
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="old",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": _owned(
                               {"attribution": "pre-freeze",
                                "signature": "AssertionError: shared-os"})})
    registry, _ = kr.refresh(failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new",
                             measured_via="local", date="2026-09-27", attribution={},
                             previous=previous, os_key="windows-latest",
                             signatures={"tests/a.py::t1": "AssertionError: windows-specific"})
    assert registry.members_by_os["windows-latest"]["tests/a.py::t1"]["signature"] == \
        "AssertionError: windows-specific"
    # the shared set is untouched, still carrying its own original signature
    assert registry.members["tests/a.py::t1"]["signature"] == "AssertionError: shared-os"


def test_refresh_without_os_key_ignores_an_existing_members_by_os_section(kr):
    """A plain (`os_key=None`) refresh -- ecosystem/harness.yaml's own call shape -- carries
    `members_by_os` forward unchanged and never reads it to seed `members`."""
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="old",
                           measured_via="local", workers=4, members={},
                           members_by_os={"windows-latest": {"tests/win.py::t": _owned()}})
    registry, _ = kr.refresh(failed=frozenset({"tests/lin.py::t"}), workers=4, commit="new",
                             measured_via="local", date="2026-09-24",
                             attribution={"tests/lin.py::t": _owned()},
                             previous=previous)
    assert registry.members == {"tests/lin.py::t": _owned()}
    assert registry.members_by_os == previous.members_by_os


# --- registry round-trip ------------------------------------------------------------------

def test_registry_round_trips_through_json(kr, tmp_path):
    registry = kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-24-abc123", measured_at_sha="s",
                           measured_via="local", workers=4,
                           members={"tests/a.py::t1": _owned()})
    path = tmp_path / "registry.json"
    kr.write_registry(path, registry)
    loaded = kr.load_registry(path)
    assert loaded == registry


def test_load_registry_missing_file_fails_closed(kr, tmp_path):
    with pytest.raises(kr.KnownRedsError, match="no registry"):
        kr.load_registry(tmp_path / "absent.json")


def test_load_registry_wrong_schema_refuses(kr, tmp_path):
    path = tmp_path / "registry.json"
    path.write_text('{"schema": "something-else/1"}', encoding="utf-8")
    with pytest.raises(kr.KnownRedsError, match="schema"):
        kr.load_registry(path)


def test_registry_hooks_field_defaults_empty_and_round_trips(kr, tmp_path):
    """A registry written with no `hooks` key (every registry before lane-ci-signal) loads
    with `hooks == {}` rather than erroring -- the extension is additive, never a breaking
    schema bump (contract done-contract item 1: "the existing readers ... stay unchanged")."""
    path = tmp_path / "registry.json"
    path.write_text(
        f'{{"schema": "{kr.SCHEMA}", "baseline_id": "b", "measured_at_sha": "s", '
        '"measured_via": "local", "workers": 4, "members": {}}', encoding="utf-8")
    loaded = kr.load_registry(path)
    assert loaded.hooks == {}

    registry = kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-26-abc", measured_at_sha="s",
                           measured_via="local", workers=4, members={},
                           hooks={"audit-health": _owned({"attribution": kr.ENVIRONMENT_MISMATCH,
                                                          "reason": "why"})})
    kr.write_registry(path, registry)
    round_tripped = kr.load_registry(path)
    assert round_tripped == registry


def test_registry_members_by_os_field_defaults_empty_and_round_trips(kr, tmp_path):
    """Same additive shape as `hooks` (D2, WAVE5B-N4 L2): a registry with no `members_by_os`
    key loads with `{}`, and a registry that has one round-trips it exactly."""
    path = tmp_path / "registry.json"
    path.write_text(
        f'{{"schema": "{kr.SCHEMA}", "baseline_id": "b", "measured_at_sha": "s", '
        '"measured_via": "local", "workers": 4, "members": {}}', encoding="utf-8")
    assert kr.load_registry(path).members_by_os == {}

    registry = kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-27-abc", measured_at_sha="s",
                           measured_via="local", workers=4, members={},
                           members_by_os={"windows-latest": {"tests/a.py::t1": _owned()}})
    kr.write_registry(path, registry)
    assert kr.load_registry(path) == registry


# --- compare -------------------------------------------------------------------------------

def _registry(kr, members, workers=4):
    return kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-24-xyz", measured_at_sha="s",
                       measured_via="local", workers=workers, members=members)


def test_compare_prints_baseline_id_on_a_clean_run(kr):
    registry = _registry(kr, {})
    result = kr.compare(frozenset(), registry, workers=4)
    assert result["verdict"] == "pass"
    assert result["baseline_id"] == registry.baseline_id


def test_compare_prints_baseline_id_on_a_failing_run(kr):
    registry = _registry(kr, {})
    result = kr.compare(frozenset({"tests/new.py::t"}), registry, workers=4)
    assert result["verdict"] == "fail"
    assert result["baseline_id"] == registry.baseline_id


def test_compare_a_known_member_is_pre_existing_not_a_regression(kr):
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": "pre-freeze"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4)
    assert result["verdict"] == "pass"
    assert result["pre_existing"] == ["tests/a.py::t1"]
    assert result["regressions"] == []


def test_compare_an_unknown_failure_is_a_regression(kr):
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": "pre-freeze"}})
    result = kr.compare(frozenset({"tests/a.py::t1", "tests/new.py::t"}), registry, workers=4)
    assert result["verdict"] == "fail"
    assert result["regressions"] == ["tests/new.py::t"]
    assert result["pre_existing"] == ["tests/a.py::t1"]


def test_compare_a_witness_is_reported_separately_never_as_a_regression(kr):
    registry = _registry(kr, {WITNESS_1: {"attribution": kr.WITNESS}})
    result = kr.compare(frozenset({WITNESS_1}), registry, workers=4)
    assert result["verdict"] == "pass"
    assert result["witnesses"] == [WITNESS_1]
    assert result["regressions"] == []
    assert result["pre_existing"] == []


def test_compare_worker_mismatch_is_not_comparable(kr):
    registry = _registry(kr, {}, workers=4)
    result = kr.compare(frozenset(), registry, workers=2)
    assert result["verdict"] == "fail"
    assert "NOT COMPARABLE" in result["reason"]


def test_compare_a_broken_pytest_exit_is_not_comparable(kr):
    registry = _registry(kr, {})
    result = kr.compare(frozenset(), registry, workers=4, pytest_exit=2)
    assert result["verdict"] == "fail"
    assert "NOT COMPARABLE" in result["reason"]


def test_compare_an_unattributed_known_member_is_a_regression(kr):
    """D2 (WAVE5B-N4 L2) RED-first witness: a known member the registry cannot explain never
    reads as known-safe -- `compare` reports it in BOTH `unattributed` (informational: which
    known member) and `regressions` (the verdict), unlike the pre-D2 behaviour of a bare pass."""
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": kr.UNATTRIBUTED, "reason": "x"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4)
    assert result["verdict"] == "fail"
    assert result["unattributed"] == ["tests/a.py::t1"]
    assert result["regressions"] == ["tests/a.py::t1"]


def test_render_compare_uses_no_pipe_tables(kr):
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": "pre-freeze"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4)
    report = kr.render_compare(result)
    assert "|" not in report
    assert registry.baseline_id in report


# --- compare: OS-keyed overlay + failure signatures (D2, WAVE5B-N4 L2) ---------------------

def test_compare_uses_the_os_specific_overlay_when_given_an_os_key(kr):
    """A member known ONLY on `members_by_os[os_key]` (not in the shared set) is `pre_existing`
    when compared with that `os_key` -- this is the windows-only capture from L1's run."""
    registry = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="s",
                           measured_via="local", workers=4, members={},
                           members_by_os={"windows-latest": {"tests/win.py::t":
                                                             {"attribution": "pre-freeze"}}})
    result = kr.compare(frozenset({"tests/win.py::t"}), registry, workers=4,
                        os_key="windows-latest")
    assert result["verdict"] == "pass"
    assert result["pre_existing"] == ["tests/win.py::t"]


def test_compare_ignores_another_os_s_overlay(kr):
    """The SAME failing id, compared with a DIFFERENT `os_key` (or none), is not covered by an
    overlay registered under a different OS -- it reports as a regression, not a known member."""
    registry = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="s",
                           measured_via="local", workers=4, members={},
                           members_by_os={"windows-latest": {"tests/win.py::t":
                                                             {"attribution": "pre-freeze"}}})
    result = kr.compare(frozenset({"tests/win.py::t"}), registry, workers=4,
                        os_key="ubuntu-latest")
    assert result["verdict"] == "fail"
    assert result["regressions"] == ["tests/win.py::t"]

    result_no_os = kr.compare(frozenset({"tests/win.py::t"}), registry, workers=4)
    assert result_no_os["verdict"] == "fail"
    assert result_no_os["regressions"] == ["tests/win.py::t"]


def test_compare_a_changed_signature_on_a_known_member_is_a_regression(kr):
    """D2 RED-first witness: the SAME node id, still a registered member, but its current
    signature no longer matches the registered one -- 'a registered test that fails worse
    still passes' (C1), closed at the signature level."""
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": "pre-freeze",
                                                  "signature": "AssertionError: original"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4,
                        signatures={"tests/a.py::t1": "TypeError: a completely different cause"})
    assert result["verdict"] == "fail"
    assert result["regressions"] == ["tests/a.py::t1"]
    assert result["signature_changed"] == ["tests/a.py::t1"]


def test_compare_an_unchanged_signature_stays_pre_existing(kr):
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": "pre-freeze",
                                                  "signature": "AssertionError: original"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4,
                        signatures={"tests/a.py::t1": "AssertionError: original"})
    assert result["verdict"] == "pass"
    assert result["pre_existing"] == ["tests/a.py::t1"]
    assert result["signature_changed"] == []


def test_compare_without_signatures_never_flags_a_change(kr):
    """Backward compatible: a caller that never supplies `signatures` (every caller before D2)
    is unaffected even though the member carries a recorded signature."""
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": "pre-freeze",
                                                  "signature": "AssertionError: original"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4)
    assert result["verdict"] == "pass"
    assert result["signature_changed"] == []


def test_compare_a_member_with_no_recorded_signature_is_never_flagged_as_changed(kr):
    """Every member registered before D2 carries no `signature` -- `compare` must not invent a
    'change' against nothing recorded, or the whole pre-existing 90-member registry would
    spuriously regress the moment `signatures` starts being supplied."""
    registry = _registry(kr, {"tests/a.py::t1": {"attribution": "pre-freeze"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4,
                        signatures={"tests/a.py::t1": "AssertionError: whatever it is today"})
    assert result["verdict"] == "pass"
    assert result["signature_changed"] == []


# --- normalize_signature (repair 1, REFUSED-lane-known-reds-signatures.md, 2026-09-27) -----
#
# The new Windows overlay's first live run turned three UNCHANGED failures into regressions
# because their captured signature embedded a run-volatile token (a random generated-name
# suffix, a pair of commit shas plus an absolute runner path, and a list literal that grows as
# audits land). RED-first witness (verbatim from the refusal): two reasons differing only in a
# sha / random suffix / path compare EQUAL, and a genuinely different assertion still compares
# CHANGED.

def test_normalize_signature_masks_a_random_generated_name_suffix(kr):
    """The real regression: `lane-zz-occupancy-witness-<n>`'s random suffix differs on every
    run (registry: 3684; the refused CI run: 6332) although the failure itself is identical."""
    a = ("AssertionError: assert ('lane-zz-occupancy-witness-3684' in "
        "'ERROR `claude` is not on PATH -- the live-session leg cannot be read')")
    b = ("AssertionError: assert ('lane-zz-occupancy-witness-6332' in "
        "'ERROR `claude` is not on PATH -- the live-session leg cannot be read')")
    assert kr.normalize_signature(a) == kr.normalize_signature(b)


def test_normalize_signature_masks_shas_and_an_absolute_path(kr):
    """The second real regression: two different commit shas and an absolute Windows runner
    path, same otherwise-identical wording."""
    a = ("AssertionError: worktree.baseRef='head' resolves the base to dev-knowledge:HEAD "
        "(the dispatching checkout) at 4ad29e44, but main HEAD is 1a0dc573 -- the dispatching "
        "checkout D:\\a\\dev-knowledge\\dev-knowledge is not on main HEAD, so `head` seeds "
        "lanes from wherever it is sitting")
    b = ("AssertionError: worktree.baseRef='head' resolves the base to dev-knowledge:HEAD "
        "(the dispatching checkout) at 0dcef85d, but main HEAD is 316d3205 -- the dispatching "
        "checkout D:\\a\\dev-knowledge\\dev-knowledge is not on main HEAD, so `head` seeds "
        "lanes from wherever it is sitting")
    assert kr.normalize_signature(a) == kr.normalize_signature(b)


def test_normalize_signature_masks_a_growing_list_body(kr):
    """The third real regression: a list of file names that grows as audits land -- the intro
    sentence is stable, only the bracketed census differs in length and content."""
    a = ("AssertionError: the committed baseline must produce a clean verdict on the tree it "
        "was measured from: [('warn', 'a.md carries no disposition'), "
        "('warn', 'b.md carries no disposition')]")
    b = ("AssertionError: the committed baseline must produce a clean verdict on the tree it "
        "was measured from: [('warn', 'a.md carries no disposition'), "
        "('warn', 'b.md carries no disposition'), "
        "('warn', 'c.md carries no disposition')]")
    assert kr.normalize_signature(a) == kr.normalize_signature(b)


def test_normalize_signature_never_masks_a_bare_list_equality_assertion(kr):
    """Codex terra HIGH, 2026-09-27: list-body masking is scoped to a list trailing an
    explanatory ': ' (the census/citation shape both real regressions had) -- an ordinary
    pytest comparison repr with no such prefix, e.g. `assert ['old'] == ['expected']`, must
    still normalize to a DIFFERENT string when its contents genuinely change, or a real
    list-equality regression would silently read as pre-existing."""
    assert kr.normalize_signature("AssertionError: assert ['old'] == ['expected']") != \
        kr.normalize_signature("AssertionError: assert ['new'] == ['expected']")


def test_normalize_signature_still_distinguishes_a_genuinely_different_assertion(kr):
    """The other half of the RED-first witness: masking is narrow -- an ordinary number in an
    assertion (not part of a hyphenated generated name) is never touched, so a real behavior
    change (22 == 21 becoming 23 == 21) still normalizes to a DIFFERENT string."""
    assert kr.normalize_signature("AssertionError: assert 22 == 21") != \
        kr.normalize_signature("AssertionError: assert 23 == 21")
    assert kr.normalize_signature("AssertionError: original shape") != \
        kr.normalize_signature("TypeError: a completely different cause")


def test_compare_two_reasons_differing_only_by_a_random_suffix_compare_equal(kr):
    """`compare` itself, not just the helper: a registered signature with the OLD random
    suffix and a current run with a NEW one is pre-existing, not a regression."""
    registry = _registry(kr, {"tests/a.py::t1": {
        "attribution": "pre-freeze",
        "signature": "AssertionError: assert ('witness-3684' in 'X')"}})
    result = kr.compare(frozenset({"tests/a.py::t1"}), registry, workers=4,
                        signatures={"tests/a.py::t1":
                                   "AssertionError: assert ('witness-9999' in 'X')"})
    assert result["verdict"] == "pass"
    assert result["signature_changed"] == []
    assert result["pre_existing"] == ["tests/a.py::t1"]


def test_refresh_stores_a_normalized_signature(kr):
    """`refresh` normalizes BEFORE storing, so a freshly-captured registry never re-embeds the
    volatile token in the first place."""
    registry, _ = kr.refresh(
        failed=frozenset({"tests/a.py::t1"}), workers=4, commit="new", measured_via="local",
        date="2026-09-27",
        attribution={"tests/a.py::t1": _owned({"attribution": "pre-freeze"})}, previous=None,
        signatures={"tests/a.py::t1": "AssertionError: assert ('witness-3684' in 'X')"})
    assert registry.members["tests/a.py::t1"]["signature"] == \
        "AssertionError: assert ('witness-<N>' in 'X')"


# --- compare-hook (lane-ci-signal, [#802]: the non-pytest sibling of `compare`) -------------

def _registry_with_hooks(kr, hooks):
    return kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-26-hooks", measured_at_sha="s",
                       measured_via="local", workers=4, members={}, hooks=hooks)


def test_compare_hook_a_clean_exit_passes_even_if_unregistered(kr):
    registry = _registry_with_hooks(kr, {})
    result = kr.compare_hook("audit-health", 0, registry)
    assert result["verdict"] == "pass"
    assert result["baseline_id"] == registry.baseline_id


def test_compare_hook_a_registered_red_passes_and_names_the_entry(kr):
    entry = {"attribution": kr.ENVIRONMENT_MISMATCH, "reason": "CI checkout mismatch"}
    registry = _registry_with_hooks(kr, {"audit-health": entry})
    result = kr.compare_hook("audit-health", 1, registry)
    assert result["verdict"] == "pass"
    assert result["registered"] == entry


def test_compare_hook_an_unregistered_red_is_a_regression(kr):
    registry = _registry_with_hooks(kr, {})
    result = kr.compare_hook("derived-copies-rebind", 1, registry)
    assert result["verdict"] == "fail"
    assert result["regressions"] == ["derived-copies-rebind"]
    assert "REGRESSION" in result["reason"]


def test_compare_hook_does_not_launder_a_different_hooks_registration(kr):
    """A registration for one hook id never covers another -- the register names WHICH check,
    not "some check failed", the same specificity `compare`'s node-id keying already has."""
    registry = _registry_with_hooks(kr, {"audit-health": {"attribution": kr.ENVIRONMENT_MISMATCH,
                                                          "reason": "x"}})
    result = kr.compare_hook("graph-orphan-census", 1, registry)
    assert result["verdict"] == "fail"


def test_render_compare_hook_uses_no_pipe_tables(kr):
    registry = _registry_with_hooks(kr, {"audit-health": {"attribution": kr.ENVIRONMENT_MISMATCH,
                                                          "reason": "x"}})
    result = kr.compare_hook("audit-health", 1, registry)
    report = kr.render_compare_hook(result)
    assert "|" not in report
    assert registry.baseline_id in report
    assert "audit-health" in report


# --- compare-hook `checks` scoping (Codex terra HIGH, 2026-09-26: a whole-hook registration
# silently launders a NEW, different failing check under the same registration) -------------

def test_extract_failing_check_names_reads_both_audit_py_health_sections(kr):
    output = (
        "operational:\n"
        "  [OK] click importable\n"
        "  [!!] repos registered  (none)\n"
        "self-audit (.dev-knowledge) - 5/6 pass:\n"
        "  [OK] git_backlog_drift: clean\n"
        "  [!!] hooks_armed: no .git/hooks/pre-commit\n"
        "  [!!] dispatch_drift: 12 unresolved\n"
        "health: DEGRADED\n"
    )
    assert kr.extract_failing_check_names(output) == {
        "repos registered", "hooks_armed", "dispatch_drift"}


def test_compare_hook_with_checks_allowlist_passes_on_exactly_the_registered_set(kr):
    entry = {"attribution": kr.ENVIRONMENT_MISMATCH, "reason": "x",
             "checks": ["hooks_armed", "repos registered", "dispatch_drift"]}
    registry = _registry_with_hooks(kr, {"audit-health": entry})
    output = ("operational:\n  [!!] repos registered  (none)\n"
             "self-audit (.dev-knowledge) - 4/6 pass:\n"
             "  [!!] hooks_armed: x\n  [!!] dispatch_drift: y\nhealth: DEGRADED\n")
    result = kr.compare_hook("audit-health", 1, registry, hook_output=output)
    assert result["verdict"] == "pass"


def test_compare_hook_with_checks_allowlist_is_a_regression_on_a_new_unregistered_check(kr):
    """RED-FIRST witness for the Codex terra HIGH finding: before `checks` scoping existed, a
    registered `audit-health` hook laundered ANY new failing check under the same registration.
    This is the failure that scoping refuses."""
    entry = {"attribution": kr.ENVIRONMENT_MISMATCH, "reason": "x",
             "checks": ["hooks_armed", "repos registered", "dispatch_drift"]}
    registry = _registry_with_hooks(kr, {"audit-health": entry})
    output = ("operational:\n  [!!] repos registered  (none)\n"
             "self-audit (.dev-knowledge) - 3/6 pass:\n"
             "  [!!] hooks_armed: x\n  [!!] dispatch_drift: y\n"
             "  [!!] a_brand_new_check_name: this is a real regression\nhealth: DEGRADED\n")
    result = kr.compare_hook("audit-health", 1, registry, hook_output=output)
    assert result["verdict"] == "fail"
    assert result["regressions"] == ["a_brand_new_check_name"]
    assert "a_brand_new_check_name" in result["reason"]


def test_compare_hook_without_hook_output_keeps_the_prior_whole_hook_behavior(kr):
    """Backward-compatible: an existing caller that never passes `--hook-output` (or a
    registration with no `checks` list at all) is unaffected by the scoping."""
    entry = {"attribution": kr.ENVIRONMENT_MISMATCH, "reason": "x",
             "checks": ["hooks_armed", "repos registered", "dispatch_drift"]}
    registry = _registry_with_hooks(kr, {"audit-health": entry})
    result = kr.compare_hook("audit-health", 1, registry)
    assert result["verdict"] == "pass"

    entry_no_checks = {"attribution": kr.ENVIRONMENT_MISMATCH, "reason": "x"}
    registry2 = _registry_with_hooks(kr, {"audit-health": entry_no_checks})
    result2 = kr.compare_hook("audit-health", 1, registry2,
                              hook_output="self-audit - 0/1 pass:\n  [!!] anything: z\n")
    assert result2["verdict"] == "pass"


# --- extract_failure_signatures / default_os_key (D2, WAVE5B-N4 L2) ------------------------

def test_extract_failure_signatures_reads_the_reason_after_the_dash(kr):
    output = ("FAILED tests/a.py::t1 - AssertionError: assert 1 == 2\n"
             "ERROR tests/b.py::t2 - RuntimeError: boom\n")
    assert kr.extract_failure_signatures(output) == {
        "tests/a.py::t1": "AssertionError: assert 1 == 2",
        "tests/b.py::t2": "RuntimeError: boom"}


def test_extract_failure_signatures_skips_a_bare_failed_line_with_no_reason(kr):
    assert kr.extract_failure_signatures("FAILED tests/a.py::t1\n") == {}


def test_default_os_key_reads_runner_os_first(kr, monkeypatch):
    monkeypatch.setenv("RUNNER_OS", "Windows")
    assert kr.default_os_key() == "windows-latest"
    monkeypatch.setenv("RUNNER_OS", "Linux")
    assert kr.default_os_key() == "ubuntu-latest"


def test_default_os_key_falls_back_to_sys_platform_off_a_runner(kr, monkeypatch):
    monkeypatch.delenv("RUNNER_OS", raising=False)
    monkeypatch.setattr(kr.sys, "platform", "win32")
    assert kr.default_os_key() == "windows-latest"
    monkeypatch.setattr(kr.sys, "platform", "linux")
    assert kr.default_os_key() == "ubuntu-latest"


# --- the live registry (D2 done-when: "unattributed = 0 per OS") ---------------------------

def test_the_live_registry_carries_zero_unattributed_members_per_os(kr):
    registry = kr.load_registry(_REPO / kr.REGISTRY_PATH)
    shared_unattributed = [n for n, e in registry.members.items()
                           if e.get("attribution") == kr.UNATTRIBUTED]
    assert shared_unattributed == []
    for os_key, members in registry.members_by_os.items():
        os_unattributed = [n for n, e in members.items()
                          if e.get("attribution") == kr.UNATTRIBUTED]
        assert os_unattributed == [], f"{os_key}: {os_unattributed}"


# --- find_lane -------------------------------------------------------------------------------

def _git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout.strip()


def _init_repo(repo: Path) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")


@pytest.fixture
def toy_repo(tmp_path):
    repo = tmp_path / "toy"
    _init_repo(repo)
    (repo / "README.md").write_text("hi\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-q", "-m", "init")
    return repo


def test_find_lane_reads_the_merge_subject_when_the_first_bad_sha_is_itself_the_merge(kr, toy_repo):
    _git(toy_repo, "checkout", "-q", "-b", "worktree-my-lane")
    (toy_repo / "f.txt").write_text("x\n", encoding="utf-8")
    _git(toy_repo, "add", "f.txt")
    _git(toy_repo, "commit", "-q", "-m", "work")
    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "merge", "--no-ff", "-q", "-m", "Merge branch 'worktree-my-lane' @ deadbeef",
        "worktree-my-lane")
    merge_sha = _git(toy_repo, "rev-parse", "HEAD")
    assert kr.find_lane(toy_repo, merge_sha, merge_sha) == "my-lane"


def test_find_lane_reads_the_first_merge_on_the_ancestry_path(kr, toy_repo):
    _git(toy_repo, "checkout", "-q", "-b", "worktree-my-lane")
    (toy_repo / "f.txt").write_text("x\n", encoding="utf-8")
    _git(toy_repo, "add", "f.txt")
    _git(toy_repo, "commit", "-q", "-m", "work")
    first_bad = _git(toy_repo, "rev-parse", "HEAD")
    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "merge", "--no-ff", "-q", "-m", "Merge branch 'worktree-my-lane' @ deadbeef",
        "worktree-my-lane")
    _git(toy_repo, "commit", "-q", "--allow-empty", "-m", "later, unrelated")
    tip = _git(toy_repo, "rev-parse", "HEAD")
    assert kr.find_lane(toy_repo, first_bad, tip) == "my-lane"


# --- attribute: the real git-bisect-run wrapper, end to end ---------------------------------

def test_attribute_bisects_a_tiny_repo_and_names_the_first_bad_commit_and_lane(kr, toy_repo):
    tests_dir = toy_repo / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_toy.py").write_text("def test_toy():\n    assert True\n", encoding="utf-8")
    _git(toy_repo, "add", "tests/test_toy.py")
    _git(toy_repo, "commit", "-q", "-m", "add a passing toy test")
    good_sha = _git(toy_repo, "rev-parse", "HEAD")

    _git(toy_repo, "checkout", "-q", "-b", "worktree-break-it")
    (tests_dir / "test_toy.py").write_text("def test_toy():\n    assert False\n", encoding="utf-8")
    _git(toy_repo, "add", "tests/test_toy.py")
    _git(toy_repo, "commit", "-q", "-m", "break the toy test")
    break_sha = _git(toy_repo, "rev-parse", "HEAD")

    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "merge", "--no-ff", "-q", "-m",
        "Merge branch 'worktree-break-it' @ deadbeef", "worktree-break-it")
    bad_sha = _git(toy_repo, "rev-parse", "HEAD")

    result = kr.attribute(toy_repo, "tests/test_toy.py::test_toy", good=good_sha, bad=bad_sha,
                          venv_python=Path(sys.executable), timeout=60.0)
    assert result["first_bad_sha"] == break_sha
    assert result["lane"] == "break-it"


def test_attribute_skips_commits_where_the_test_file_does_not_yet_exist(kr, toy_repo):
    """The test file is added AFTER `good`; bisect must skip through the commits where it does
    not exist rather than mis-report the range as untestable."""
    tests_dir = toy_repo / "tests"
    tests_dir.mkdir()
    good_sha = _git(toy_repo, "rev-parse", "HEAD")  # the toy_repo's own init commit: no tests/

    _git(toy_repo, "checkout", "-q", "-b", "worktree-add-it")
    (tests_dir / "test_new.py").write_text("def test_new():\n    assert True\n", encoding="utf-8")
    _git(toy_repo, "add", "tests/test_new.py")
    _git(toy_repo, "commit", "-q", "-m", "add the test, passing")
    (tests_dir / "test_new.py").write_text("def test_new():\n    assert False\n", encoding="utf-8")
    _git(toy_repo, "add", "tests/test_new.py")
    _git(toy_repo, "commit", "-q", "-m", "break it later")
    break_sha = _git(toy_repo, "rev-parse", "HEAD")

    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "merge", "--no-ff", "-q", "-m",
        "Merge branch 'worktree-add-it' @ deadbeef", "worktree-add-it")
    bad_sha = _git(toy_repo, "rev-parse", "HEAD")

    result = kr.attribute(toy_repo, "tests/test_new.py::test_new", good=good_sha, bad=bad_sha,
                          venv_python=Path(sys.executable), timeout=60.0)
    assert result["first_bad_sha"] == break_sha


def test_find_lane_walks_past_an_origin_main_sync_merge_to_the_real_lane_merge(kr, toy_repo):
    """Codex terra HIGH #2: an intervening `Merge remote-tracking branch 'origin/main' into
    worktree-...` sync merge must be walked PAST, not stopped at -- it never carries a lane's
    work into main itself."""
    _git(toy_repo, "checkout", "-q", "-b", "worktree-my-lane")
    (toy_repo / "f.txt").write_text("x\n", encoding="utf-8")
    _git(toy_repo, "add", "f.txt")
    _git(toy_repo, "commit", "-q", "-m", "work")
    first_bad = _git(toy_repo, "rev-parse", "HEAD")

    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "commit", "-q", "--allow-empty", "-m", "unrelated main progress")
    _git(toy_repo, "checkout", "-q", "worktree-my-lane")
    _git(toy_repo, "merge", "--no-ff", "-q", "-m",
        "Merge remote-tracking branch 'origin/main' into worktree-my-lane", "main")

    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "merge", "--no-ff", "-q", "-m", "Merge branch 'worktree-my-lane' @ deadbeef",
        "worktree-my-lane")
    tip = _git(toy_repo, "rev-parse", "HEAD")
    assert kr.find_lane(toy_repo, first_bad, tip) == "my-lane"


def test_bisect_step_prefers_a_definitive_returncode_over_skip_looking_output(kr, monkeypatch):
    """Codex terra HIGH #1: a genuinely failing test (returncode 1) whose output happens to
    contain a skip-ish phrase (e.g. inside a traceback/assertion message) must still be
    classified `1` (bad), never `125` (skip)."""
    class _FakeDone:
        returncode = 1
        stdout = "AssertionError: no tests ran the way I expected\n1 failed in 0.01s\n"
        stderr = ""

    monkeypatch.setattr(kr.subprocess, "run", lambda *a, **k: _FakeDone())
    monkeypatch.setenv("_KNOWN_REDS_BISECT_TEST_ID", "tests/x.py::t")
    monkeypatch.setenv("_KNOWN_REDS_BISECT_VENV_PY", sys.executable)
    monkeypatch.setenv("_KNOWN_REDS_BISECT_CLONE", ".")
    monkeypatch.setenv("_KNOWN_REDS_BISECT_TIMEOUT", "60")
    assert kr._bisect_step() == 1


def test_bisect_step_still_skips_a_genuine_zero_collection(kr, monkeypatch):
    class _FakeDone:
        returncode = 5
        stdout = "no tests ran\n"
        stderr = ""

    monkeypatch.setattr(kr.subprocess, "run", lambda *a, **k: _FakeDone())
    monkeypatch.setenv("_KNOWN_REDS_BISECT_TEST_ID", "tests/x.py::t")
    monkeypatch.setenv("_KNOWN_REDS_BISECT_VENV_PY", sys.executable)
    monkeypatch.setenv("_KNOWN_REDS_BISECT_CLONE", ".")
    monkeypatch.setenv("_KNOWN_REDS_BISECT_TIMEOUT", "60")
    assert kr._bisect_step() == 125


# --- refresh CLI: ancestor validation of --previous -------------------------------------------

def test_main_refresh_refuses_a_previous_registry_not_an_ancestor_of_commit(kr, toy_repo, tmp_path):
    """Codex terra HIGH #3: a --previous registry measured on unrelated history must not be
    trusted to carry members forward."""
    _git(toy_repo, "checkout", "-q", "-b", "side")
    _git(toy_repo, "commit", "-q", "--allow-empty", "-m", "unrelated side history")
    side_sha = _git(toy_repo, "rev-parse", "HEAD")
    _git(toy_repo, "checkout", "-q", "main")
    _git(toy_repo, "commit", "-q", "--allow-empty", "-m", "main progress")
    main_sha = _git(toy_repo, "rev-parse", "HEAD")

    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-01-deadbeefcafe",
                           measured_at_sha=side_sha, measured_via="local", workers=4,
                           members={"tests/a.py::t1": _owned({"attribution": kr.PRE_FREEZE})})
    prev_path = tmp_path / "previous.json"
    kr.write_registry(prev_path, previous)

    pytest_out = tmp_path / "pytest.out"
    pytest_out.write_text("FAILED tests/a.py::t1 - x\n", encoding="utf-8")
    registry_out = tmp_path / "registry.json"

    rc = kr.main(["--repo-root", str(toy_repo), "refresh", "--pytest-output", str(pytest_out),
                 "--workers", "4", "--commit", main_sha, "--date", "2026-09-24",
                 "--previous", str(prev_path), "--registry", str(registry_out)])
    assert rc == 1
    assert not registry_out.exists()


def test_main_refresh_accepts_a_previous_registry_that_is_an_ancestor(kr, toy_repo, tmp_path):
    ancestor_sha = _git(toy_repo, "rev-parse", "HEAD")
    _git(toy_repo, "commit", "-q", "--allow-empty", "-m", "main progress")
    tip_sha = _git(toy_repo, "rev-parse", "HEAD")

    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-01-deadbeefcafe",
                           measured_at_sha=ancestor_sha, measured_via="local", workers=4,
                           members={"tests/a.py::t1": _owned({"attribution": kr.PRE_FREEZE})})
    prev_path = tmp_path / "previous.json"
    kr.write_registry(prev_path, previous)

    pytest_out = tmp_path / "pytest.out"
    pytest_out.write_text("FAILED tests/a.py::t1 - x\n", encoding="utf-8")
    registry_out = tmp_path / "registry.json"

    rc = kr.main(["--repo-root", str(toy_repo), "refresh", "--pytest-output", str(pytest_out),
                 "--workers", "4", "--commit", tip_sha, "--date", "2026-09-24",
                 "--previous", str(prev_path), "--registry", str(registry_out)])
    assert rc == 0
    assert registry_out.exists()


# --- refresh/compare CLI: --os (D2, WAVE5B-N4 L2 -- backward-compatible CLI, new flag) -------

def test_main_refresh_with_os_flag_writes_members_by_os(kr, toy_repo, tmp_path):
    previous = kr.Registry(schema=kr.SCHEMA, baseline_id="2026-09-01-deadbeefcafe",
                           measured_at_sha=_git(toy_repo, "rev-parse", "HEAD"), measured_via="local",
                           workers=4, members={"tests/a.py::t1": _owned({"attribution": kr.PRE_FREEZE})})
    prev_path = tmp_path / "previous.json"
    kr.write_registry(prev_path, previous)
    _git(toy_repo, "commit", "-q", "--allow-empty", "-m", "progress")
    tip_sha = _git(toy_repo, "rev-parse", "HEAD")

    pytest_out = tmp_path / "pytest.out"
    pytest_out.write_text("FAILED tests/a.py::t1 - AssertionError: on windows\n", encoding="utf-8")
    registry_out = tmp_path / "registry.json"

    rc = kr.main(["--repo-root", str(toy_repo), "refresh", "--pytest-output", str(pytest_out),
                 "--workers", "4", "--commit", tip_sha, "--date", "2026-09-27",
                 "--previous", str(prev_path), "--registry", str(registry_out),
                 "--os", "windows-latest"])
    assert rc == 0
    written = kr.load_registry(registry_out)
    assert written.members == previous.members  # shared set untouched
    assert written.members_by_os["windows-latest"]["tests/a.py::t1"]["signature"] == \
        "AssertionError: on windows"


def test_main_compare_with_os_flag_uses_the_overlay(kr, tmp_path):
    registry = kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="s",
                           measured_via="local", workers=4, members={},
                           members_by_os={"windows-latest": {"tests/win.py::t": _owned()}})
    registry_path = tmp_path / "registry.json"
    kr.write_registry(registry_path, registry)
    pytest_out = tmp_path / "pytest.out"
    pytest_out.write_text("FAILED tests/win.py::t - x\n", encoding="utf-8")

    rc = kr.main(["compare", "--pytest-output", str(pytest_out), "--workers", "4",
                 "--registry", str(registry_path), "--os", "windows-latest"])
    assert rc == 0

    rc_wrong_os = kr.main(["compare", "--pytest-output", str(pytest_out), "--workers", "4",
                           "--registry", str(registry_path), "--os", "ubuntu-latest"])
    assert rc_wrong_os == 1


# --- foundation-1-honest-green item 1: the parser reads node ids, never captured-log lines --
#
# DCT D3 (`to-browser/DIGEST-CI-TRIAGE-2026-10-03.md`): pytest prints captured `logging` output
# as `ERROR    <logger>:<file>.py:<line> <message>` inside a failing test's report, and the
# `ERROR`-prefixed extractor took every such line for a failed test id. The pseudo-id then
# either reads as a REGRESSION or -- once registered -- is a "known red" that no test can ever
# turn green (`logs/KNOWN-REDS-REGISTRY.json` carried one for months).

_CAPTURED_LOG_OUTPUT = (
    "=================================== FAILURES ===================================\n"
    "------------------------------ Captured log call -------------------------------\n"
    "ERROR    codespace-admission:codespace_admission.py:332 admission: REFUSED -- "
    "claude_on_path, uv_on_path, pre_commit_on_path, gh_not_broken\n"
    "ERROR    provision_legs:provision_legs.py:775 history: ref 'main' does not resolve "
    "in this clone - retry with fetch-depth 0\n"
    "=========================== short test summary info ============================\n"
    "ERROR    codespace-admission:codespace_admission.py:332 admission: REFUSED -- gh_not_broken\n"
    "FAILED tests/test_demo.py::test_a_real_failure - AssertionError: boom\n"
    "ERROR tests/test_demo_collect.py - ImportError: no module named x\n"
)
_REAL_NODE_ID = "tests/test_demo.py::test_a_real_failure"
_REAL_COLLECT_ERROR = "tests/test_demo_collect.py"

#: The three R52-Q2 fields every entry carries; the far-future date keeps a fixture from ever
#: expiring under the suite.
_OWNED = {"task": "[#912]", "owner": "rob", "expiry": "2999-12-31"}


def _owned(entry: dict | None = None) -> dict:
    return {**(entry or {"attribution": "pre-freeze"}), **_OWNED}


def test_compare_ignores_captured_log_lines(kr, tmp_path, capsys):
    registry = kr.Registry(
        schema=kr.SCHEMA, baseline_id="b", measured_at_sha="s", measured_via="local", workers=4,
        members={_REAL_NODE_ID: _owned(), _REAL_COLLECT_ERROR: _owned()})
    registry_path = tmp_path / "registry.json"
    kr.write_registry(registry_path, registry)
    pytest_out = tmp_path / "pytest.out"
    pytest_out.write_text(_CAPTURED_LOG_OUTPUT, encoding="utf-8", newline="\n")

    rc = kr.main(["compare", "--pytest-output", str(pytest_out), "--workers", "4",
                  "--registry", str(registry_path), "--os", "ubuntu-latest"])
    shown = capsys.readouterr().out

    assert "codespace-admission" not in shown and "provision_legs" not in shown, shown
    assert f"  known         {_REAL_NODE_ID}" in shown
    assert f"  known         {_REAL_COLLECT_ERROR}" in shown
    assert "pre-existing   : 2" in shown and "regressions    : 0" in shown, shown
    assert rc == 0


def test_the_extractors_agree_a_captured_log_line_is_not_a_failure(kr):
    ids = kr.conductor.parse_failed_node_ids(_CAPTURED_LOG_OUTPUT)
    assert ids == frozenset({_REAL_NODE_ID, _REAL_COLLECT_ERROR})
    sigs = kr.extract_failure_signatures(_CAPTURED_LOG_OUTPUT)
    assert set(sigs) == {_REAL_NODE_ID, _REAL_COLLECT_ERROR}
    assert sigs[_REAL_NODE_ID] == "AssertionError: boom"


# --- foundation-1-honest-green items 2-4: every entry is owned, dated, and tied to a row -----
#
# R52 Q2 (`to-browser/RATIFICATION-2026-10-02.md`): "every current known-red gets its own row
# with a task id. The known-reds registry refuses an entry without one." Without an owner and
# an expiry "known red" means "forgotten red". AM2-3: a growing known failure is registered at
# its base-measured value only with a ceiling the compare enforces.

import datetime as dt  # noqa: E402 -- section-local, next to the tests that use it
import json  # noqa: E402


def _write_raw(tmp_path, kr, *, members=None, by_os=None, hooks=None, schema=None):
    data = {"schema": schema or kr.SCHEMA, "baseline_id": "b", "measured_at_sha": "s",
            "measured_via": "local", "workers": 4, "members": members or {},
            "members_by_os": by_os or {}, "hooks": hooks or {}}
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


@pytest.mark.parametrize("missing", ["task", "owner", "expiry"])
def test_load_registry_refuses_an_entry_missing_task_owner_or_expiry(kr, tmp_path, missing):
    entry = _owned()
    del entry[missing]
    path = _write_raw(tmp_path, kr, members={"tests/a.py::t1": entry})
    with pytest.raises(kr.KnownRedsError, match=missing):
        kr.load_registry(path)


@pytest.mark.parametrize("where", ["members", "members_by_os", "hooks"])
def test_the_refusal_covers_the_overlay_and_the_hooks_section_too(kr, tmp_path, where):
    bare = {"attribution": "pre-freeze"}
    kwargs = {"members": {"members": {"tests/a.py::t": bare}},
              "members_by_os": {"by_os": {"windows-latest": {"tests/a.py::t": bare}}},
              "hooks": {"hooks": {"audit-health": bare}}}[where]
    with pytest.raises(kr.KnownRedsError, match="task"):
        kr.load_registry(_write_raw(tmp_path, kr, **kwargs))


def test_load_registry_refuses_an_expired_entry(kr, tmp_path):
    entry = {**_owned(), "expiry": "2026-10-01"}
    path = _write_raw(tmp_path, kr, members={"tests/a.py::t1": entry})
    with pytest.raises(kr.KnownRedsError, match="EXPIRED"):
        kr.load_registry(path, today=dt.date(2026, 10, 2))
    # the last day is still inside the window: expired means strictly after the expiry
    assert kr.load_registry(path, today=dt.date(2026, 10, 1)).members


def test_load_registry_refuses_a_malformed_task_or_date(kr, tmp_path):
    for field, value in (("task", "912"), ("task", "#912"), ("expiry", "soon"), ("owner", " ")):
        entry = {**_owned(), field: value}
        path = _write_raw(tmp_path, kr, members={"tests/a.py::t1": entry})
        with pytest.raises(kr.KnownRedsError, match=field):
            kr.load_registry(path)


def test_load_registry_refuses_the_legacy_schema_and_says_why(kr, tmp_path):
    path = _write_raw(tmp_path, kr, schema="known-reds-registry/1",
                      members={"tests/a.py::t1": {"attribution": "pre-freeze"}})
    with pytest.raises(kr.KnownRedsError, match="R52"):
        kr.load_registry(path)


def test_compare_exits_uncomparable_on_a_registry_with_an_unowned_entry(kr, tmp_path):
    path = _write_raw(tmp_path, kr, members={"tests/a.py::t1": {"attribution": "pre-freeze"}})
    out = tmp_path / "pytest.out"
    out.write_text("FAILED tests/a.py::t1 - x\n", encoding="utf-8")
    rc = kr.main(["compare", "--pytest-output", str(out), "--workers", "4",
                  "--registry", str(path), "--os", "ubuntu-latest"])
    assert rc == kr.EXIT_UNCOMPARABLE


def test_compare_hook_exits_uncomparable_on_a_registry_with_an_unowned_hook(kr, tmp_path):
    path = _write_raw(tmp_path, kr, hooks={"audit-health": {"attribution": "environment-mismatch"}})
    rc = kr.main(["compare-hook", "--hook-id", "audit-health", "--exit-code", "1",
                  "--registry", str(path)])
    assert rc == kr.EXIT_UNCOMPARABLE


def test_refresh_refuses_a_new_red_whose_attribution_carries_no_task_owner_expiry(kr):
    with pytest.raises(kr.KnownRedsError, match="expiry"):
        kr.refresh(failed=frozenset({"tests/new.py::t"}), workers=4, commit="c",
                   measured_via="local", date="2026-10-03", previous=None,
                   attribution={"tests/new.py::t": {"attribution": "pre-freeze",
                                                    "task": "[#912]", "owner": "rob"}})


def test_refresh_accepts_a_new_red_that_is_owned(kr):
    registry, _ = kr.refresh(failed=frozenset({"tests/new.py::t"}), workers=4, commit="c",
                             measured_via="local", date="2026-10-03", previous=None,
                             attribution={"tests/new.py::t": _owned()})
    assert registry.members["tests/new.py::t"]["task"] == "[#912]"


# --- the live file ----------------------------------------------------------------------------

def test_the_live_registry_every_entry_has_a_task_an_owner_and_an_expiry(kr):
    """Item 3: no entry of the committed file lacks the three fields. `load_registry` already
    refuses one; this reads the raw JSON so the assertion does not rest on the loader."""
    raw = json.loads((_REPO / kr.REGISTRY_PATH).read_text(encoding="utf-8"))
    buckets = [("members", raw["members"]), ("hooks", raw.get("hooks", {}))]
    buckets += [(f"members_by_os[{osk}]", m) for osk, m in raw.get("members_by_os", {}).items()]
    bare = [f"{label}: {key}" for label, bucket in buckets for key, entry in bucket.items()
            if any(not str(entry.get(f, "")).strip() for f in kr.OWNED_FIELDS)]
    assert bare == []
    assert raw["schema"] == kr.SCHEMA


def test_every_live_entry_names_a_row_that_is_still_open(kr):
    """The tie is to a row that exists and is open -- a task id nobody can read is the same
    forgotten red with a number on it."""
    import re
    registry = kr.load_registry(_REPO / kr.REGISTRY_PATH)
    entries = [*registry.members.values(), *registry.hooks.values(),
               *(e for m in registry.members_by_os.values() for e in m.values())]
    tasks = sorted({e["task"] for e in entries})
    not_open = []
    for task in tasks:
        number = task.strip("[]#")
        files = list((_REPO / "tasks").glob(f"{number}-*.md"))
        status = re.search(r"^status:\s*(\S+)", files[0].read_text(encoding="utf-8"), re.M) \
            if files else None
        if not files or status is None or status.group(1) != "open":
            not_open.append(task)
    assert not_open == []


# --- AM2-3: a growing known failure is registered at its measured value, under a ceiling -------

_BOOT_SIG = "AssertionError: 41,174 B tracked boot base exceeds 40,000"


def _growing(**over):
    entry = {"attribution": "pre-freeze", "signature": _BOOT_SIG,
             "ceiling": {"pattern": r"(?P<n>[\d,]+) B tracked boot base", "max": 41174},
             "growth": {"from": 40544, "to": 41174, "commits": "4ad29e44..2e7fa5f2"},
             **_OWNED}
    entry.update(over)
    return entry


def _registry_of(kr, entry=None):
    return kr.Registry(schema=kr.SCHEMA, baseline_id="b", measured_at_sha="s",
                       measured_via="local", workers=4,
                       members={"tests/boot.py::t": entry or _growing()})


def _compare_growing(kr, current_value: str):
    sig = f"AssertionError: {current_value} B tracked boot base exceeds 40,000"
    return kr.compare(frozenset({"tests/boot.py::t"}), _registry_of(kr), workers=4,
                      signatures={"tests/boot.py::t": sig})


def test_a_growing_item_at_its_ceiling_is_pre_existing(kr):
    result = _compare_growing(kr, "41,174")
    assert result["verdict"] == "pass" and result["pre_existing"] == ["tests/boot.py::t"]
    assert result["ceiling_exceeded"] == []


def test_a_further_step_of_growth_reads_as_a_regression(kr):
    """Item 4's RED-first witness: one byte past the ceiling is not 'the same known red'."""
    result = _compare_growing(kr, "41,175")
    assert result["verdict"] == "fail"
    assert result["regressions"] == ["tests/boot.py::t"]
    assert result["ceiling_exceeded"] == ["tests/boot.py::t"]


def test_a_lower_measured_value_is_reported_so_the_ceiling_can_come_down(kr):
    result = _compare_growing(kr, "40,900")
    assert result["verdict"] == "pass"
    assert result["ceiling_slack"] == ["tests/boot.py::t"]


def test_a_growing_item_that_fails_a_different_way_is_a_regression(kr):
    result = kr.compare(frozenset({"tests/boot.py::t"}), _registry_of(kr), workers=4,
                        signatures={"tests/boot.py::t": "KeyError: 'boot'"})
    assert result["verdict"] == "fail" and result["signature_changed"] == ["tests/boot.py::t"]


def test_a_ceiling_entry_with_no_current_signature_fails_closed(kr):
    result = kr.compare(frozenset({"tests/boot.py::t"}), _registry_of(kr), workers=4)
    assert result["verdict"] == "fail"


def test_the_ceiling_is_enforced_through_the_cli(kr, tmp_path):
    path = tmp_path / "registry.json"
    kr.write_registry(path, _registry_of(kr))
    out = tmp_path / "pytest.out"
    argv = ["compare", "--workers", "4", "--registry", str(path), "--os", "ubuntu-latest",
            "--pytest-output", str(out)]
    out.write_text(f"FAILED tests/boot.py::t - {_BOOT_SIG}\n", encoding="utf-8")
    assert kr.main(argv) == 0
    out.write_text(f"FAILED tests/boot.py::t - {_BOOT_SIG.replace('41,174', '41,175')}\n",
                   encoding="utf-8")
    assert kr.main(argv) == 1


@pytest.mark.parametrize("breakage", ["no-growth", "no-from", "bad-max", "no-group", "bad-regex"])
def test_load_registry_refuses_a_ceiling_that_is_not_fully_stated(kr, tmp_path, breakage):
    entry = _growing()
    if breakage == "no-growth":
        del entry["growth"]
    elif breakage == "no-from":
        del entry["growth"]["from"]
    elif breakage == "bad-max":
        entry["ceiling"]["max"] = "lots"
    elif breakage == "no-group":
        entry["ceiling"]["pattern"] = r"[\d,]+ B tracked"
    else:
        entry["ceiling"]["pattern"] = r"(?P<n>[\d,]+"
    path = _write_raw(tmp_path, kr, members={"tests/boot.py::t": entry})
    with pytest.raises(kr.KnownRedsError, match="ceiling|growth"):
        kr.load_registry(path)


def test_refresh_lowers_a_ceiling_to_a_lower_measured_value(kr):
    previous = _registry_of(kr)
    registry, _ = kr.refresh(
        failed=frozenset({"tests/boot.py::t"}), workers=4, commit="c", measured_via="local",
        date="2026-10-03", attribution={}, previous=previous,
        signatures={"tests/boot.py::t": "AssertionError: 40,900 B tracked boot base exceeds 40,000"})
    assert registry.members["tests/boot.py::t"]["ceiling"]["max"] == 40900
    assert previous.members["tests/boot.py::t"]["ceiling"]["max"] == 41174  # input untouched


def test_refresh_refuses_to_carry_a_ceiling_entry_that_grew(kr):
    with pytest.raises(kr.KnownRedsError, match="ceiling"):
        kr.refresh(
            failed=frozenset({"tests/boot.py::t"}), workers=4, commit="c", measured_via="local",
            date="2026-10-03", attribution={}, previous=_registry_of(kr),
            signatures={"tests/boot.py::t": "AssertionError: 41,175 B tracked boot base exceeds 40,000"})
