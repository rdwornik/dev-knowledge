"""Tests for scripts/validate_doc_claims.py — #89 prose-vs-state checker.

A read-only Layer-2 validator (mirrors #90 validate_git_backlog): assert a living
doc's own self-contained, deterministically-checkable CLAIMS match repo ground truth
at three loci — (1) audit check-count (`len(ALL_CHECKS)`), (2a/2b) pre-commit hook
count + roster (`.pre-commit-config.yaml` ids), (3) pytest collected-count (off-gate).
WARN-only / fail-soft; never a gate; never mutates.

Scope boundary (do NOT duplicate): check #10 owns last_reviewed staleness; check #13
owns HANDOFF version stamps; #140 owns cross-file fidelity / duplication / bloat.
"""
from __future__ import annotations

import dataclasses
import re
import types
from pathlib import Path

import pytest


import validate_doc_claims as vdc  # noqa: E402
import audit as aud  # noqa: E402

# --- mini-doc fixtures (a self-consistent temp repo) ------------------------

_HOOK_IDS = [
    "normalize-dated-headers", "codemap-freshness", "toc-freshness",
    "toc-freshness-playbook", "validate-backlog", "audit-health", "ruff",
    "backlog-id-on-close",
]


def _precommit_yaml(ids):
    lines = ["repos:", "  - repo: local", "    hooks:"]
    for i in ids:
        stage = "\n        stages: [commit-msg]" if i == "backlog-id-on-close" else ""
        lines.append(f"      - id: {i}\n        name: {i}\n        entry: echo{stage}")
    return "\n".join(lines) + "\n"


def _claude_md(roster_ids):
    # roster bullets carry a TRAILING backtick token too (e.g. `via audit.py health`) —
    # the extractor must capture only the LEADING token. A §12-style changelog below
    # names hooks in prose and must NOT leak into the claimed set (window-bounding).
    bullets = "\n".join(f"- `{i}` — the {i} hook, run `via {i} thing`" for i in roster_ids)
    return (
        "# CLAUDE\n\n## 8. Skills\nstuff\n\n"
        "## 9. Hooks active\n"
        "Pre-commit (`.pre-commit-config.yaml`):\n"
        f"{bullets}\n\n"
        "Rules (`.claude/rules/`):\n- `git-discipline.md` — commit discipline\n\n"
        "## 10. Anti-patterns\nnothing\n\n"
        "## 12. Section history\n"
        "- v2.7 — `ruff` gate wired; `audit-health` added; `validate-backlog` noted\n"
    )


def _doc_counts_md(checks=15, gates=8, collected=372):
    # The three count claims live in ecosystem/doc-counts.md (moved off ARCHITECTURE.md by
    # #222 so a count bump does not trip the freshness gate). Anchors match the _CLAIMS regexes.
    return (
        "# doc-counts\n\n"
        "<!-- COUNTS:START -->\n"
        f"- pre-commit gates ({gates}) (`.pre-commit-config.yaml`)\n"
        f"- audit: **{checks} registered checks**\n"
        f"- tests: **{collected} collected**\n"
        "<!-- COUNTS:END -->\n"
    )


def _architecture_md():
    return "# ARCH\n\n## Validators\n- `scripts/audit.py` — cross-repo conformance.\n"


def _init_doc_repo(tmp_path, *, checks=15, gates=8, collected=372, ids=None, roster_ids=None):
    ids = list(_HOOK_IDS if ids is None else ids)
    roster_ids = list(ids if roster_ids is None else roster_ids)
    repo = tmp_path / "r"
    repo.mkdir()
    (repo / "ARCHITECTURE.md").write_text(_architecture_md(), encoding="utf-8")
    (repo / "ecosystem").mkdir()
    (repo / "ecosystem" / "doc-counts.md").write_text(
        _doc_counts_md(checks, gates, collected), encoding="utf-8")
    (repo / ".pre-commit-config.yaml").write_text(_precommit_yaml(ids), encoding="utf-8")
    (repo / "CLAUDE.md").write_text(_claude_md(roster_ids), encoding="utf-8")
    return repo


def _by_name(results):
    return {r.name: r for r in results}


# --- pure core: extractors --------------------------------------------------

def test_extract_hook_ids_counts_all_including_commit_msg():
    # CRITICAL zero-FP: ARCHITECTURE "(8)" includes the commit-msg backlog-id-on-close.
    # The deriver counts ALL ids (8), NOT pre-commit-stage-only (7).
    ids = vdc.extract_hook_ids(_precommit_yaml(_HOOK_IDS))
    assert ids == _HOOK_IDS
    assert len(ids) == 8
    assert "backlog-id-on-close" in ids


def test_extract_hook_ids_resilient_to_added_hook():
    ids = vdc.extract_hook_ids(_precommit_yaml(_HOOK_IDS + ["new-hook"]))
    assert len(ids) == 9
    assert "new-hook" in ids


def test_extract_claimed_hooks_ignores_description_backticks():
    # bullets carry trailing `via ... thing` backtick tokens — only the leading id counts.
    claimed = vdc.extract_claimed_hooks(_claude_md(_HOOK_IDS))
    assert claimed == set(_HOOK_IDS)


def test_extract_claimed_hooks_ignores_changelog_prose_outside_window():
    # §12 Section-history names ruff/audit-health/validate-backlog in prose; window-bounding
    # to §9 must exclude them so the roster set is exactly the §9 bullets.
    claimed = vdc.extract_claimed_hooks(_claude_md(_HOOK_IDS))
    assert "git-discipline.md" not in claimed  # the Rules sub-block bullet, after pre-commit
    assert claimed == set(_HOOK_IDS)


def test_extract_claimed_hooks_anchor_missing_when_no_section9():
    # no '## 9. Hooks active' heading -> None (anchor-missing), never a spurious set.
    assert vdc.extract_claimed_hooks("# CLAUDE\n\n## 1. Intro\ntext\n") is None


# --- pure core: reconcile (count/set/skip) ----------------------------------

def test_reconcile_all_match_on_consistent_repo(tmp_path):
    repo = _init_doc_repo(tmp_path, checks=15, gates=8)
    results = vdc.reconcile(repo, audit_check_count=15, run_expensive=False)
    by = _by_name(results)
    assert by["audit_check_count"].status == "match"
    assert by["precommit_hook_count"].status == "match"
    assert by["precommit_hook_roster"].status == "match"


def test_reconcile_flags_count_mismatch_only(tmp_path):
    # ARCHITECTURE claims 15 checks; ground truth (injected) is 16 -> only that row mismatches.
    repo = _init_doc_repo(tmp_path, checks=15, gates=8)
    by = _by_name(vdc.reconcile(repo, audit_check_count=16, run_expensive=False))
    assert by["audit_check_count"].status == "mismatch"
    assert by["audit_check_count"].claimed == "15"
    assert by["audit_check_count"].actual == "16"
    assert by["precommit_hook_count"].status == "match"
    assert by["precommit_hook_roster"].status == "match"


def test_reconcile_gate_count_uses_all_ids_not_stage_scoped(tmp_path):
    # zero-FP guard: doc says (8), yaml has 8 ids incl. commit-msg -> match (NOT 7-vs-8 FP).
    repo = _init_doc_repo(tmp_path, gates=8)
    by = _by_name(vdc.reconcile(repo, audit_check_count=15, run_expensive=False))
    assert by["precommit_hook_count"].status == "match"
    assert by["precommit_hook_count"].actual == "8"


def test_reconcile_roster_mismatch_on_added_hook(tmp_path):
    # config has 9 hooks; CLAUDE §9 still lists 8 -> roster + count both drift.
    repo = _init_doc_repo(tmp_path, ids=_HOOK_IDS + ["new-hook"], roster_ids=_HOOK_IDS, gates=8)
    by = _by_name(vdc.reconcile(repo, audit_check_count=15, run_expensive=False))
    assert by["precommit_hook_roster"].status == "mismatch"
    assert "new-hook" in by["precommit_hook_roster"].actual


def test_reconcile_roster_match_is_order_independent(tmp_path):
    shuffled = list(reversed(_HOOK_IDS))
    repo = _init_doc_repo(tmp_path, roster_ids=shuffled)
    by = _by_name(vdc.reconcile(repo, audit_check_count=15, run_expensive=False))
    assert by["precommit_hook_roster"].status == "match"


def test_reconcile_anchor_missing_is_not_a_mismatch(tmp_path):
    # doc-counts.md with the 'registered checks' phrase reworded away -> anchor-missing.
    repo = _init_doc_repo(tmp_path)
    counts = repo / "ecosystem" / "doc-counts.md"
    counts.write_text(counts.read_text(encoding="utf-8").replace(
        "**15 registered checks**", "fifteen checks (reworded)"), encoding="utf-8")
    by = _by_name(vdc.reconcile(repo, audit_check_count=15, run_expensive=False))
    assert by["audit_check_count"].status == "anchor-missing"
    assert by["audit_check_count"].status != "mismatch"


def test_reconcile_skips_test_count_when_not_expensive(tmp_path):
    # claim 3 (pytest collect) is OFF the commit gate: run_expensive=False -> skipped.
    repo = _init_doc_repo(tmp_path, collected=372)
    by = _by_name(vdc.reconcile(repo, audit_check_count=15, run_expensive=False))
    assert "pytest_collected" in by
    assert by["pytest_collected"].status == "skipped"


def test_reconcile_evaluates_test_count_when_expensive(tmp_path, monkeypatch):
    # run_expensive=True actually EVALUATES claim 3 (not skip). Mock the pytest subprocess for
    # a deterministic collected count (42); doc claims 42 -> match, proving the deriver RAN and
    # compared. The `!= "skipped"` assertion is the teeth: a vacuous skip-pass (the #141 bug —
    # claim-3 silently stops evaluating yet the test still goes green) is rejected here.
    repo = _init_doc_repo(tmp_path, collected=42)
    monkeypatch.setattr(vdc.subprocess, "run", lambda *a, **k: types.SimpleNamespace(
        stdout="42 tests collected in 0.10s", stderr=""))
    by = _by_name(vdc.reconcile(repo, audit_check_count=15, run_expensive=True))
    assert by["pytest_collected"].status == "match"
    assert by["pytest_collected"].status != "skipped"   # teeth: not a vacuous skip-pass
    assert by["pytest_collected"].actual == "42"


def test_reconcile_skips_when_deriver_unavailable(tmp_path, monkeypatch):
    # The separate None->skipped path: subprocess launch fails -> deriver returns None ->
    # 'skipped' (fail-soft; an infra hiccup must not flap a WARN). Kept distinct from the
    # evaluated path above so neither masks the other.
    def _boom(*a, **k):
        raise OSError("pytest launcher gone")

    monkeypatch.setattr(vdc.subprocess, "run", _boom)
    repo = _init_doc_repo(tmp_path, collected=42)
    by = _by_name(vdc.reconcile(repo, audit_check_count=15, run_expensive=True))
    assert by["pytest_collected"].status == "skipped"


def test_derive_pytest_collected_disables_cache_and_bytecode(tmp_path, monkeypatch):
    # Layer-2 "writes NOTHING" (#141 Fix 1, red-first): the collection subprocess must disable
    # the pytest cache (-p no:cacheprovider -> no .pytest_cache/) and bytecode writes
    # (PYTHONDONTWRITEBYTECODE=1 -> no __pycache__/). Captures the subprocess call and asserts
    # both — fails until Fix 1 lands.
    seen = {}

    def _capture(argv, *a, **k):
        seen["argv"] = argv
        seen["env"] = k.get("env")
        return types.SimpleNamespace(stdout="5 tests collected", stderr="")

    monkeypatch.setattr(vdc.subprocess, "run", _capture)
    vdc._derive_pytest_collected(tmp_path, 0)
    assert "-p" in seen["argv"] and "no:cacheprovider" in seen["argv"]
    assert seen["env"] is not None and seen["env"].get("PYTHONDONTWRITEBYTECODE") == "1"


def test_format_findings_lists_only_mismatches_no_pipe(tmp_path):
    repo = _init_doc_repo(tmp_path, checks=15)
    results = vdc.reconcile(repo, audit_check_count=16, run_expensive=False)
    out = vdc.format_findings(results)
    assert "audit_check_count" in out
    assert "precommit_hook_roster" not in out  # a matching row is not listed
    assert "|" not in out


# --- deployed audit check: check_doc_claims ---------------------------------

def test_check_skips_non_hub_repo(tmp_path):
    findings = aud.check_doc_claims(tmp_path / "some-child")
    assert len(findings) == 1
    assert findings[0].check_name == "doc_claims"
    assert findings[0].status == "n/a"  # [#465] leg 1
    assert "hub-only" in findings[0].evidence


def test_check_warns_not_fails_on_mismatch(monkeypatch):
    hub = Path(aud._REPO_ROOT)
    monkeypatch.setattr(aud._vdc, "reconcile", lambda root, n, run_expensive: [
        vdc.ClaimResult("audit_check_count", "mismatch", "15", "16", "ARCHITECTURE.md")])
    findings = aud.check_doc_claims(hub)
    assert findings[0].status == "warn"          # never "fail"
    assert "audit_check_count" in findings[0].evidence
    assert "|" not in findings[0].evidence


def test_check_warns_on_anchor_missing(monkeypatch):
    hub = Path(aud._REPO_ROOT)
    monkeypatch.setattr(aud._vdc, "reconcile", lambda root, n, run_expensive: [
        vdc.ClaimResult("audit_check_count", "anchor-missing", "", "16", "ARCHITECTURE.md")])
    findings = aud.check_doc_claims(hub)
    assert findings[0].status == "warn"
    assert "anchor" in findings[0].evidence.lower()


def test_check_passes_when_all_match(monkeypatch):
    hub = Path(aud._REPO_ROOT)
    monkeypatch.setattr(aud._vdc, "reconcile", lambda root, n, run_expensive: [
        vdc.ClaimResult("audit_check_count", "match", "16", "16", "ARCHITECTURE.md")])
    assert aud.check_doc_claims(hub)[0].status == "pass"


def test_check_failsoft_on_error(monkeypatch):
    hub = Path(aud._REPO_ROOT)

    def _boom(root, n, run_expensive):
        raise RuntimeError("yaml exploded")

    monkeypatch.setattr(aud._vdc, "reconcile", _boom)
    findings = aud.check_doc_claims(hub)
    assert findings[0].status == "warn"
    assert "yaml exploded" in findings[0].evidence or "degraded" in findings[0].evidence


# --- #208 / GAP-6: the claim REGISTRY is data-driven (every row guarded; new rows auto-tested) ---
# These three guards iterate vdc._CLAIMS, so a NEWLY-APPENDED claim row is automatically
# exercised — the GAP-6 "registry extension is auto-tested" contract — with no per-claim test.


@pytest.mark.parametrize("claim", vdc._CLAIMS, ids=lambda c: c.name)
def test_every_claim_row_is_structurally_valid(claim):
    # Each registry row must carry a callable deriver and a kind-appropriate anchor.
    assert callable(claim.deriver)
    assert claim.kind in {"count", "set"}
    if claim.kind == "count":
        assert claim.anchor is not None        # count claims resolve a numeric anchor
    else:
        assert claim.anchor is None            # the set claim uses extract_claimed_hooks instead


@pytest.mark.parametrize("claim", vdc._CLAIMS, ids=lambda c: c.name)
@pytest.mark.live_repo
def test_every_claim_anchor_still_resolves_in_live_doc(claim):
    # "anchor still present" guard: if a living doc is reworded so a claim's anchor no longer
    # matches, the claim silently degrades to anchor-missing (un-checkable). Assert every
    # registered anchor currently resolves in its LIVE doc, so such a reword fails loudly here.
    text = (Path(vdc._REPO_ROOT) / claim.doc).read_text(encoding="utf-8")
    if claim.kind == "count":
        assert claim.anchor.search(text) is not None, \
            f"{claim.name}: anchor no longer resolves in live {claim.doc} (reworded?)"
    else:
        assert vdc.extract_claimed_hooks(text) is not None, \
            f"{claim.name}: §9 roster anchor no longer resolves in live {claim.doc}"


@pytest.mark.parametrize("claim", [c for c in vdc._CLAIMS if not c.expensive], ids=lambda c: c.name)
@pytest.mark.live_repo
def test_every_nonexpensive_deriver_returns_value_on_live_repo(claim):
    # "working deriver": each cheap deriver must return a non-None ground truth against the
    # live repo (the expensive pytest deriver is exercised separately, to keep this fast).
    assert claim.deriver(Path(vdc._REPO_ROOT), 0) is not None


def test_registry_extension_is_auto_evaluated_and_mismatch_flagged(tmp_path):
    # NEGATIVE CONTROL (GAP-6 (2)): extend the registry data-drivenly with a NEW claim row
    # whose deriver returns a known value (5), pointed at a tmp doc that claims the WRONG
    # number (99). reconcile must auto-evaluate the appended row and FLAG the mismatch ->
    # proves the registry is extensible AND a wrong doc number is caught.
    (tmp_path / "EXTRA.md").write_text(
        "# extra\n\nThis subsystem declares 99 widgets.\n", encoding="utf-8")
    extra = vdc.Claim("extra_demo", "EXTRA.md",
                      re.compile(r"declares (\d+) widgets"), "count",
                      lambda root, n: 5)
    by = _by_name(vdc.reconcile(tmp_path, audit_check_count=None, claims=[extra]))
    assert by["extra_demo"].status == "mismatch"
    assert by["extra_demo"].claimed == "99"
    assert by["extra_demo"].actual == "5"


def test_registry_extension_matches_when_doc_number_correct(tmp_path):
    # Positive companion: the SAME extended row matches when the doc states the right number,
    # so the negative control above is genuinely discriminating, not constant-fail.
    (tmp_path / "EXTRA.md").write_text(
        "# extra\n\nThis subsystem declares 5 widgets.\n", encoding="utf-8")
    extra = vdc.Claim("extra_demo", "EXTRA.md",
                      re.compile(r"declares (\d+) widgets"), "count",
                      lambda root, n: 5)
    by = _by_name(vdc.reconcile(tmp_path, audit_check_count=None, claims=[extra]))
    assert by["extra_demo"].status == "match"


def test_check_runs_every_claim_and_is_deferred_off_the_commit_gate(monkeypatch):
    # [#597] replaced `test_check_passes_run_expensive_false_in_gate_mode`. The old contract
    # was "at the commit gate the adapter passes run_expensive=False", carried by the
    # `_GATE_MODE` global. The tier says the same thing one level up: the whole check is
    # ship-tier, so wherever it runs it runs COMPLETE (claim 3 included) -- and the commit gate
    # does not run it at all. Both halves are asserted, because either alone would pass while
    # the expensive claim silently stopped running anywhere.
    hub = Path(aud._REPO_ROOT)
    seen = {}

    def _rec(root, n, run_expensive):
        seen["run_expensive"] = run_expensive
        return [vdc.ClaimResult("audit_check_count", "match", "16", "16", "ARCHITECTURE.md")]

    monkeypatch.setattr(aud._vdc, "reconcile", _rec)
    aud.check_doc_claims(hub)
    assert seen["run_expensive"] is True

    seen.clear()
    findings = aud.run_checks(hub, checks=[aud.check_doc_claims], tier=aud.TIER_COMMIT)
    assert seen == {}                      # never called at the commit tier
    assert findings[0].status == "n/a" and "ship-tier" in findings[0].evidence
    assert aud.tier_of(aud.check_doc_claims) == aud.TIER_SHIP


# --- end-to-end: seeded mismatch fires through the REGISTERED check ----------

def test_e2e_seeded_mismatch_fires_through_registered_check(tmp_path, monkeypatch):
    # The ADR-81 'deployed' proof: a seeded count mismatch in real-shaped docs fires WARN
    # through the check registered in ALL_CHECKS — deployed, not merely written.
    repo = _init_doc_repo(tmp_path, checks=99, gates=8)   # ARCHITECTURE claims 99 checks
    monkeypatch.setattr(aud, "_REPO_ROOT", str(repo))     # make the temp repo look like the hub
    # Claim 3 stubbed to its fail-soft answer. It used to be suppressed by `_GATE_MODE`, which
    # [#597] retired; the check is ship-tier now and always asks. What is under test here is the
    # count mismatch, not the collector, and a real `pytest --collect-only` in a tmp dir would
    # add seconds to every run of this test for nothing.
    #
    # Patched on the REGISTRY, never `monkeypatch.setattr(vdc, "_derive_pytest_collected", ...)`:
    # `_CLAIMS` captured the function object at import, so rebinding the module attribute leaves
    # the row pointing at the real deriver and the stub is INERT. That is exactly what the first
    # version of this line did (terra HIGH, 2026-08-27) — it shelled out to a real pytest and the
    # test passed anyway, which is the seam-detaches-silently class this file's own
    # `_claims_with_stub_pytest` docstring already warned about.
    monkeypatch.setattr(vdc, "_CLAIMS", _claims_with_stub_pytest(lambda root, n: None))
    findings = aud.check_doc_claims(repo)
    assert findings[0].status == "warn"
    assert "audit_check_count" in findings[0].evidence
    assert aud.check_doc_claims in aud.ALL_CHECKS          # actually registered


@pytest.mark.live_repo
def test_registered_check_never_fails_on_live_repo():
    # WARN-only contract holds in production: the live hub run must never return FAIL.
    findings = aud.check_doc_claims(Path(aud._REPO_ROOT))
    assert findings[0].status in {"pass", "warn"}


# --- green-by-skip: a claim that cannot compute its ground truth must FAIL ----
# STANDING_RULINGS section U (2026-08-25). The defect: `audit_check_count` reported
# `skipped — <ground truth unavailable>` while the CLI printed `OK — no prose drift`,
# so the surface that exists to catch count drift read GREEN exactly when it was blind.
# Third paid instance of the shape (pre-push degraded-allow, ADR-85 §A6;
# block_commit_on_main silent-allow). The two legs below are its regression.
#
# Both legs SIMULATE drift rather than observe it: ecosystem/doc-counts.md and live
# len(ALL_CHECKS) both read 46, so the defect is LATENT on the live repo and a test that
# merely ran the real thing would pass with the bug present.


def _claims_with_stub_pytest(deriver):
    """`_CLAIMS` with claim 3's deriver swapped, via the supported `claims=` hook.

    NOT monkeypatch.setattr(vdc, "_derive_pytest_collected", ...): the registry captured
    the function object at import time, so rebinding the module attribute leaves the row
    pointing at the real one, which then shells out to pytest against a tmp repo (slow,
    and it returns 0 -> a mismatch that looks like a genuine failure).
    """
    return [dataclasses.replace(c, deriver=deriver) if c.name == "pytest_collected" else c
            for c in vdc._CLAIMS]

def test_unavailable_ground_truth_fails_and_is_not_a_skip(tmp_path):
    # Leg 1 (the fix): injected count is None -> the claim cannot be computed at all.
    # It must NOT come back 'skipped' (which callers render as green) and must carry a
    # reason naming the paths that DO compute it.
    repo = _init_doc_repo(tmp_path, checks=15, gates=8)
    by = _by_name(vdc.reconcile(repo, audit_check_count=None, run_expensive=False))
    assert by["audit_check_count"].status == "not-computed"
    assert by["audit_check_count"].status != "skipped"     # the teeth: not a vacuous skip
    assert by["audit_check_count"].status != "match"
    reason = by["audit_check_count"].actual
    assert "audit health" in reason and "audit run" in reason
    # the OTHER claims still evaluate — one un-computable claim must not blind the rest
    assert by["precommit_hook_count"].status == "match"
    assert by["precommit_hook_roster"].status == "match"


def test_cli_reports_fail_and_exits_nonzero_when_a_claim_is_unavailable(tmp_path, monkeypatch, capsys):
    # Leg 2 (the reported defect verbatim): the CLI must not print `OK` over a claim it
    # never checked, and must not exit 0. This is the exact string pairing section U
    # measured — `skipped — <ground truth unavailable>` under `OK — no prose drift`.
    repo = _init_doc_repo(tmp_path, checks=15, gates=8)
    monkeypatch.setattr(vdc, "_REPO_ROOT", repo)
    # keep it fast + hermetic: claim 3 would otherwise shell out to pytest against the
    # tmp repo. Patched on the REGISTRY (see _claims_with_stub_pytest) because main()
    # reads _CLAIMS, which holds the original function object.
    monkeypatch.setattr(vdc, "_CLAIMS", _claims_with_stub_pytest(lambda root, n: 0))
    rc = vdc.main()
    out = capsys.readouterr().out
    assert rc == 1                                        # was 0 unconditionally
    assert "FAIL" in out
    assert "OK" not in out                                # the green headline is gone
    assert "audit_check_count" in out


def test_simulated_drift_still_mismatches_when_the_count_is_available(tmp_path):
    # Discriminator: the fail-closed leg must not swallow ordinary drift. With a count
    # actually injected, a doc/live disagreement is still a MISMATCH, not 'unavailable'.
    repo = _init_doc_repo(tmp_path, checks=46, gates=8)   # doc claims 46
    by = _by_name(vdc.reconcile(repo, audit_check_count=47, run_expensive=False))
    assert by["audit_check_count"].status == "mismatch"
    assert (by["audit_check_count"].claimed, by["audit_check_count"].actual) == ("46", "47")


def test_pytest_collected_keeps_its_documented_fail_soft_skip(tmp_path):
    # The scope boundary, asserted so a later edit cannot widen fail-closed semantics by
    # accident: claim 3's deriver SHELLS OUT, so None there means an infra hiccup, and
    # flapping a WARN on a failed subprocess launch is the documented wrong answer.
    # It stays 'skipped' while audit_check_count goes 'not-computed' in the SAME run.
    #
    # The deriver is swapped through the `claims=` extension point, not monkeypatched on
    # the module: `_CLAIMS` captured the function OBJECT at import, so rebinding the
    # module attribute does not reach the registry row (it silently ran the real pytest
    # subprocess against the tmp repo and returned 0 -> mismatch).
    repo = _init_doc_repo(tmp_path, checks=15, gates=8)
    by = _by_name(vdc.reconcile(repo, audit_check_count=None, run_expensive=True,
                                claims=_claims_with_stub_pytest(lambda root, n: None)))
    assert by["pytest_collected"].status == "skipped"
    assert by["audit_check_count"].status == "not-computed"


def test_adapter_surfaces_unavailable_rather_than_passing(tmp_path, monkeypatch):
    # The audit-adapter leg: an 'unavailable' claim must reach the operator as a named
    # WARN, never be counted as a pass. WARN (not FAIL) is deliberate — check_doc_claims'
    # never-block-the-commit-gate posture is a separate ruling, not widened here.
    repo = _init_doc_repo(tmp_path, checks=15, gates=8)
    monkeypatch.setattr(aud, "_REPO_ROOT", str(repo))
    # (the `_GATE_MODE` patch this test used to carry was already inert -- `reconcile` itself is
    # replaced below, so nothing read the flag. [#597] retired it.)
    monkeypatch.setattr(aud._vdc, "reconcile",
                        lambda *a, **k: [vdc.ClaimResult("audit_check_count", "not-computed",
                                                         "", "<NOT COMPUTED>", "d.md")])
    findings = aud.check_doc_claims(repo)
    assert findings[0].status == "warn"
    assert "NOT CHECKED" in findings[0].evidence
    assert "audit_check_count" in findings[0].evidence
