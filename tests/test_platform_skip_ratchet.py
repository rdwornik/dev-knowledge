"""Row L4 — the platform-skip ratchet. RED-first.

`to-browser/PROPOSAL-ADR-CI-VERIFICATION-2026-09-26-seat-71020de7.md` D7: "a
**platform-skip ratchet** (a new check: count of `skipif(sys.platform|os.name)` and body
`pytest.skip` on platform, may only shrink — `proof_layer.py:58-60` deliberately exempts
these, so it cannot be reused)." Row L4's Done-when: "the 9 ids green on ubuntu; ratchet
RED-first: an added platform skip fails."

This module proves, on FIXTURE trees (never the live one, for the growth/shrink legs — the
live tree must never be made to carry a seeded regression): scan_sites finds both shapes
(skipif, body-skip) and ignores the counter-rule's own class (tool-presence, e.g. `git`) and a
platform branch that does something other than skip; the ratchet FAILS (not WARN, unlike
`proof_layer`) on an added site and is silent on a removed one; `render_baseline` refuses to
grow an already-committed set. Two `@pytest.mark.live_repo` tests close the loop against the
real `tests/` tree and its committed `ecosystem/platform-skip-baseline.json`.
"""
from __future__ import annotations

import textwrap

import pytest

import platform_skip_ratchet as psr


# --- fixtures --------------------------------------------------------------------------------

_MODULE_SKIPIF_PLATFORM = textwrap.dedent('''\
    """The shim is PowerShell; the stub is a .cmd file."""
    import os
    import pytest

    pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows-only shim")

    def test_the_shim_runs():
        assert True

    def test_the_shim_help():
        assert True
    ''')

_FUNCTION_SKIPIF_PLATFORM_DIRECT = textwrap.dedent('''\
    """POSIX exec bit only."""
    import sys
    import pytest

    @pytest.mark.skipif(sys.platform == "win32", reason="POSIX exec bit only")
    def test_present_but_not_executable():
        assert True
    ''')

_FUNCTION_SKIPIF_PLATFORM_ALIAS = textwrap.dedent('''\
    """A drive root exists only on Windows paths."""
    import os
    import pytest

    shim_only = pytest.mark.skipif(os.name != "nt", reason="drive root is Windows-only")

    @shim_only
    def test_an_unmounted_prompts_authority():
        assert True

    def test_unrelated():
        assert True
    ''')

_BODY_SKIP_ON_PLATFORM = textwrap.dedent('''\
    """A body skip reached only through a platform-conditioned branch."""
    import sys
    import pytest

    def test_windows_only_behaviour():
        if sys.platform != "win32":
            pytest.skip("Windows-only behaviour")
        assert True
    ''')

_NOT_A_SKIP_JUST_A_BRANCH = textwrap.dedent('''\
    """The honest cross-platform arm: two working code paths, no skip."""
    import os

    def test_picks_a_shell():
        if os.name == "nt":
            shell = "cmd"
        else:
            shell = "sh"
        assert shell

    def test_unconditional_skip_elsewhere():
        import pytest
        if os.name == "nt":
            pass
        pytest.skip("unconditional, not reached only through the platform branch")
    ''')

_TOOL_PRESENCE_NOT_PLATFORM = textwrap.dedent('''\
    """The counter-rule's OTHER side: a tool-presence skipif is proof_layer's class, not this
    one — the two ratchets must never double-count the same guard."""
    import shutil
    import pytest

    requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not available")

    @requires_git
    def test_needs_git():
        assert True
    ''')

_VERSION_INFO_NOT_PLATFORM = textwrap.dedent('''\
    """sys.version_info is neither proof_layer's class nor this one."""
    import sys
    import pytest

    @pytest.mark.skipif(sys.version_info < (3, 12), reason="needs 3.12 syntax")
    def test_new_syntax():
        assert True
    ''')


def _tests_dir(tmp_path, **modules):
    d = tmp_path / "tests"
    d.mkdir(exist_ok=True)
    for name, text in modules.items():
        (d / f"{name}.py").write_text(text, encoding="utf-8")
    return d


# --- the predicate: detecting a platform-conditioned skip site ------------------------------

def test_a_module_level_platform_skipif_gates_every_test_in_the_module(tmp_path):
    d = _tests_dir(tmp_path, test_dispatch_shim=_MODULE_SKIPIF_PLATFORM)
    sites = psr.scan_sites(d)
    assert len(sites) == 1
    assert sites[0].scope == psr.SCOPE_MODULE
    assert sites[0].kind == psr.KIND_SKIPIF
    assert sites[0].gated_tests == 2
    assert sites[0].target == "<module>"


def test_a_direct_function_level_platform_skipif_is_found(tmp_path):
    d = _tests_dir(tmp_path, test_codespace_admission=_FUNCTION_SKIPIF_PLATFORM_DIRECT)
    sites = psr.scan_sites(d)
    assert len(sites) == 1
    assert sites[0].scope == psr.SCOPE_FUNCTION
    assert sites[0].kind == psr.KIND_SKIPIF
    assert sites[0].target == "test_present_but_not_executable"


def test_an_aliased_function_level_platform_skipif_is_found(tmp_path):
    """The alias form is dominant in this repo (`shim_only`, `requires_git`, ...) — the same
    resolution `proof_layer` already had to get right, reused rather than re-derived."""
    d = _tests_dir(tmp_path, test_dispatch_py=_FUNCTION_SKIPIF_PLATFORM_ALIAS)
    sites = psr.scan_sites(d)
    assert len(sites) == 1
    assert sites[0].target == "test_an_unmounted_prompts_authority"


def test_a_body_pytest_skip_reached_only_through_a_platform_if_is_found(tmp_path):
    """The shape `proof_layer` explicitly does not attempt (its own honest limit: 'a bare
    pytest.skip() inside a test body ... is NOT detected')."""
    d = _tests_dir(tmp_path, test_x=_BODY_SKIP_ON_PLATFORM)
    sites = psr.scan_sites(d)
    assert len(sites) == 1
    assert sites[0].kind == psr.KIND_BODY_SKIP
    assert sites[0].target == "test_windows_only_behaviour"


def test_a_platform_branch_that_does_not_skip_is_not_a_site(tmp_path):
    """The honest cross-platform arm (two working code paths) is not this class; an
    UNCONDITIONAL skip merely sitting beside an unrelated platform branch is not this class
    either — only a skip reached ONLY through the platform branch counts."""
    d = _tests_dir(tmp_path, test_x=_NOT_A_SKIP_JUST_A_BRANCH)
    assert psr.scan_sites(d) == []


def test_a_tool_presence_skipif_is_not_this_class(tmp_path):
    """The two ratchets partition the counter-rule: a guard is proof_layer's OR this one's,
    never both — so no guard is silently double-counted."""
    d = _tests_dir(tmp_path, test_review_artifact_coverage=_TOOL_PRESENCE_NOT_PLATFORM)
    assert psr.scan_sites(d) == []


def test_a_version_info_skipif_is_not_this_class(tmp_path):
    d = _tests_dir(tmp_path, test_x=_VERSION_INFO_NOT_PLATFORM)
    assert psr.scan_sites(d) == []


def test_an_ungated_module_produces_no_site(tmp_path):
    d = _tests_dir(tmp_path, test_plain=textwrap.dedent('''\
        def test_a():
            assert True
        '''))
    assert psr.scan_sites(d) == []


def test_an_unparseable_module_is_reported_not_skipped(tmp_path):
    d = _tests_dir(tmp_path, test_broken="def test(:\n    pass\n")
    sites, unreadable = psr.scan_sites(d, report_unreadable=True)
    assert sites == []
    assert unreadable == ["test_broken.py"]


def test_the_key_distinguishes_skipif_from_body_skip_on_the_same_target():
    """A function could carry both shapes; the key must not collapse them into one identity."""
    a = psr.PlatformSkip(module="m.py", scope=psr.SCOPE_FUNCTION, kind=psr.KIND_SKIPIF,
                         gated_tests=1, target="test_x")
    b = psr.PlatformSkip(module="m.py", scope=psr.SCOPE_FUNCTION, kind=psr.KIND_BODY_SKIP,
                         gated_tests=1, target="test_x")
    assert a.key != b.key


# --- THE RATCHET: RED-first, unlike proof_layer's WARN posture -----------------------------

def test_an_added_platform_skip_FAILS(tmp_path):
    """The row's own words: 'ratchet RED-first: an added platform skip fails.'"""
    d = _tests_dir(tmp_path, test_codespace_admission=_FUNCTION_SKIPIF_PLATFORM_DIRECT)
    findings = psr.ratchet_findings(psr.scan_sites(d), baseline=psr.Baseline(sites=()))
    assert [s for s, _ in findings] == ["fail"]
    assert "test_codespace_admission.py" in findings[0][1]
    assert "NEW" in findings[0][1]


def test_a_site_already_in_the_baseline_does_not_refire(tmp_path):
    d = _tests_dir(tmp_path, test_codespace_admission=_FUNCTION_SKIPIF_PLATFORM_DIRECT)
    sites = psr.scan_sites(d)
    baseline = psr.Baseline(sites=tuple(s.key for s in sites))
    assert psr.ratchet_findings(sites, baseline=baseline) == []


def test_a_removed_platform_skip_PASSES_quietly(tmp_path):
    """The row's other half: 'a removed one passes.' A site present in the baseline but absent
    from the current scan is not reported at all — the ratchet only watches for GROWTH."""
    d = _tests_dir(tmp_path, test_plain=textwrap.dedent('''\
        def test_a():
            assert True
        '''))
    baseline = psr.Baseline(sites=("test_codespace_admission.py::"
                                   "test_present_but_not_executable:skipif",))
    assert psr.ratchet_findings(psr.scan_sites(d), baseline=baseline) == []


def test_one_new_site_surfaces_even_while_another_is_removed(tmp_path):
    """Identity-keyed, not count-keyed — the swap a bare counter is blind to."""
    d = _tests_dir(tmp_path, test_dispatch_py=_FUNCTION_SKIPIF_PLATFORM_ALIAS)
    baseline = psr.Baseline(sites=("test_codespace_admission.py::"
                                   "test_present_but_not_executable:skipif",))
    findings = psr.ratchet_findings(psr.scan_sites(d), baseline=baseline)
    assert [s for s, _ in findings] == ["fail"]
    assert "test_dispatch_py.py" in findings[0][1]


def test_a_missing_baseline_fails_rather_than_reads_as_clean(tmp_path):
    d = _tests_dir(tmp_path, test_plain=textwrap.dedent('''\
        def test_a():
            assert True
        '''))
    findings = psr.ratchet_findings(psr.scan_sites(d), baseline=None)
    assert [s for s, _ in findings] == ["fail"]
    assert "no readable" in findings[0][1]


def test_a_detector_mismatch_fails_rather_than_compares(tmp_path):
    d = _tests_dir(tmp_path, test_plain=textwrap.dedent('''\
        def test_a():
            assert True
        '''))
    baseline = psr.Baseline(sites=(), detector_id="some-other-detector/v0")
    findings = psr.ratchet_findings(psr.scan_sites(d), baseline=baseline)
    assert [s for s, _ in findings] == ["fail"]
    assert "detector mismatch" in findings[0][1]


def test_each_finding_carries_the_site_key(tmp_path):
    d = _tests_dir(tmp_path, test_codespace_admission=_FUNCTION_SKIPIF_PLATFORM_DIRECT)
    [site] = psr.scan_sites(d)
    [(_, evidence)] = psr.ratchet_findings([site], baseline=psr.Baseline(sites=()))
    assert site.key in evidence


# --- render_baseline / load_baseline ---------------------------------------------------------

def test_render_baseline_refuses_to_grow_an_already_committed_set(tmp_path):
    """The only door row L4's 'may only fall' leaves open: growing the SAME detector's baseline
    raises rather than silently widening a shrink-only contract."""
    d = _tests_dir(tmp_path, test_codespace_admission=_FUNCTION_SKIPIF_PLATFORM_DIRECT)
    sites = psr.scan_sites(d)
    previous = psr.Baseline(sites=())  # the new site is not yet in the committed set
    with pytest.raises(ValueError, match="GROW"):
        psr.render_baseline(sites, "2026-09-27", "deadbeef", "test", previous=previous)


def test_render_baseline_allows_a_shrink(tmp_path):
    d = _tests_dir(tmp_path, test_plain=textwrap.dedent('''\
        def test_a():
            assert True
        '''))
    previous = psr.Baseline(sites=("test_codespace_admission.py::"
                                   "test_present_but_not_executable:skipif",))
    rendered = psr.render_baseline(psr.scan_sites(d), "2026-09-27", "deadbeef", "test",
                                   previous=previous)
    assert '"sites": []' in rendered or '"sites": [\n  ]' in rendered.replace(" ", "")


def test_render_baseline_ignores_a_previous_baseline_from_a_different_detector(tmp_path):
    """A stale/foreign-detector baseline is not a growth ceiling — it is not comparable."""
    d = _tests_dir(tmp_path, test_codespace_admission=_FUNCTION_SKIPIF_PLATFORM_DIRECT)
    previous = psr.Baseline(sites=(), detector_id="some-other-detector/v0")
    rendered = psr.render_baseline(psr.scan_sites(d), "2026-09-27", "deadbeef", "test",
                                   previous=previous)
    assert "test_present_but_not_executable" in rendered


def test_load_baseline_rejects_a_count_mismatch(tmp_path):
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / "ecosystem" / "platform-skip-baseline.json").write_text(
        '{"detector_id": "platform-skip-ratchet/v1", "site_count": 2, "sites": ["a"]}',
        encoding="utf-8")
    assert psr.load_baseline(tmp_path) is None


def test_load_baseline_rejects_duplicate_sites(tmp_path):
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / "ecosystem" / "platform-skip-baseline.json").write_text(
        '{"detector_id": "platform-skip-ratchet/v1", "site_count": 2, "sites": ["a", "a"]}',
        encoding="utf-8")
    assert psr.load_baseline(tmp_path) is None


def test_load_baseline_absent_file_is_none(tmp_path):
    assert psr.load_baseline(tmp_path) is None


def test_load_baseline_roundtrips_render_baseline(tmp_path):
    d = _tests_dir(tmp_path, test_codespace_admission=_FUNCTION_SKIPIF_PLATFORM_DIRECT)
    sites = psr.scan_sites(d)
    rendered = psr.render_baseline(sites, "2026-09-27", "deadbeef", "test")
    (tmp_path / "ecosystem").mkdir()
    (tmp_path / "ecosystem" / "platform-skip-baseline.json").write_text(
        rendered, encoding="utf-8")
    baseline = psr.load_baseline(tmp_path)
    assert baseline is not None
    assert set(baseline.sites) == {s.key for s in sites}


# --- the live tree ---------------------------------------------------------------------------

@pytest.mark.live_repo
def test_the_live_platform_skip_population_is_at_or_below_its_baseline():
    """The class cannot silently re-form: a NEW platform-conditioned skip surfaces by name; a
    removed one drains without complaint (mirrors proof_layer's own live-tree witness)."""
    sites = psr.scan_sites(psr.repo_root() / "tests")
    baseline = psr.load_baseline(psr.repo_root())
    assert baseline is not None, f"{psr.BASELINE_RELPATH} is absent or malformed"
    assert set(s.key for s in sites) - set(baseline.sites) == set()


@pytest.mark.live_repo
def test_the_live_tree_has_at_least_one_of_each_known_shape():
    """The four real modules this ratchet was built to catch (T2, 2026-09-26) are still found,
    so the predicate is measured against the live tree and not only fixtures."""
    sites = psr.scan_sites(psr.repo_root() / "tests")
    modules = {s.module for s in sites}
    # test_codespace_admission.py left this list when its Windows skip was fixed at its cause
    # (b2-codespace-green, item 2) -- a site removed because it was repaired is the ratchet working.
    for expected in ("test_dispatch_launch.py", "test_dispatch_py.py", "test_dispatch_shim.py"):
        assert expected in modules, f"{expected} no longer carries a platform skip site"
