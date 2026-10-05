# B2-W1 W1-8 -- the journal pin and lane-shape witness added here are claimed under [#1101].
"""Step 1 (the Done-when, R44/R45): the real cut path, dry-cut / no-commit mode, against the
live hub tree, gated on the ADR-129 handoff organ set.

LANE-HANDOFF-REDESIGN-BUILD-lane-handoff-redesign.md Step 1 names five criteria a single dry
cut must satisfy: (a) one attempt; (b) only the named handoff organ set is evaluated; (c) a
fixture hard-fail OUTSIDE the set does not block, and its converse (L4) -- a fixture hard-fail
INSIDE the set DOES block; (d) wall time <= 120s; (e) the bundle files are produced.

Runs against `gen_handoff._REPO_ROOT` (the live hub tree this test's own `scripts/` resolves
to -- this worktree, never the primary checkout) with a FIXTURE transport (item 7/L2: a tmp
dir with a valid ledger + ratification; QUESTION/STATUS left absent, both a legitimate
SUBJECT-ABSENT pass, not a hole). The two LIVE-STATE rows (`worktree_owners`,
`memory_within_cap`, N2) are pinned to a fixture too, so the test is deterministic
(AMEND-HANDOFF-REDESIGN-BUILD-2026-10-01 item 2 / R47) -- their live behaviour gets its own
separate tests in `tests/test_gen_handoff_preflight.py`.
"""
from __future__ import annotations

import time
from pathlib import Path

import pytest

import audit as aud
import gen_handoff as gh
from branch_context import pin_journal_spine, witness

# repair U1 follow-up (integrator d9fa78c0, CI run 36945030700): `scripts/audit_checks/
# check_dispatch_drift.py` resolves its module as `from scripts import dispatch_drift`
# first, which succeeds (an implicit namespace package) and lands on `sys.modules
# ["scripts.dispatch_drift"]` -- a DIFFERENT object than the bare `sys.modules
# ["dispatch_drift"]` a plain `import dispatch_drift as dd` here would bind. Patching the
# bare module's attributes then never reaches the one the real organ actually calls, so the
# fixture silently no-ops and the live `find_powershell`/`resolve_via_get_command` run for
# real -- harmless on a dev box with pwsh on PATH, a genuine hard-fail on a bare CI runner.
# Mirror the adapter's own resolution order so this binds the identical object it uses.
try:
    from scripts import dispatch_drift as dd
except ImportError:
    import dispatch_drift as dd

#: The 120s bound (item 9/L9 Performance scenario; AMEND item 3): measured on the parallel
#: path, never raised to paper over a slow run -- a run over it is a refusal.
WALL_TIME_BOUND_S = 120


def _fixture_transport(tmp_path: Path, today: str) -> Path:
    """A tmp transport carrying a valid ledger + ratification (item 7/L2). QUESTION/STATUS
    files are left absent -- both rows read that as SUBJECT-ABSENT (a real PASS-equivalent via
    `_na_row`, not a hole left in the fixture)."""
    transport = tmp_path / "transport"
    (transport / "to-browser").mkdir(parents=True)
    (transport / "to-cc").mkdir(parents=True)
    (transport / "to-browser" / "LEDGER-dev-knowledge.md").write_text(
        f"refreshed {today}\n", encoding="utf-8")
    (transport / "to-browser" / f"RATIFICATION-{today}.md").write_text(
        "# Ratification -- test fixture\n", encoding="utf-8")
    return transport


def _run_dry_cut(tmp_path: Path, monkeypatch, *, today: str = "2026-10-01",
                 inject_fail_organ: "str | None" = None):
    """One invocation of the real cut path (`gen_handoff.generate(..., dry_cut=True)`).

    `inject_fail_organ`, when given, monkeypatches that `audit` check function (by name) to
    return a single hard-fail `Finding` -- item 9/L4's (c) and its converse share this one
    injection path so the two directions cannot silently diverge in setup.
    """
    transport = _fixture_transport(tmp_path, today)
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(transport))
    # Row 9 (worktree_owners) is a LIVE-STATE row (N2): this worktree's own `git worktree list`
    # carries every sibling lane's worktree too, which is exactly the flakiness class
    # DIGEST-HANDOFF-UNBLOCK-2026-09-30 §3 measured. Pinned to "none" for determinism
    # (AMEND item 2); its live behaviour has its own test in test_gen_handoff_preflight.py.
    monkeypatch.setattr(gh, "_linked_worktrees", lambda repo_root: [])
    # Rows 6 (`journal_anchored`) and the ship_gate row's `journal_spine_anchor` organ read the live
    # JOURNAL against `main`'s spine, so they are red on any lane whose tree lags `main` and on
    # `main` between a merge and its JOURNAL entry -- a fact about the branch, not about the cut
    # (B2-W1 W1-8; tests/branch_context.py::pin_journal_spine). Their own behaviour has its own
    # tests; this one pins them clean.
    pin_journal_spine(monkeypatch)
    # dispatch_drift (also in the handoff organ set) resolves every literal command in
    # PLAYBOOK Ch8's dispatch table via Get-Command on THIS machine's PATH -- clean on a dev
    # box with codex/agy/etc. installed, a genuine hard-fail on a bare CI runner that carries
    # none of them (found by CI, not by this test's own author; same AMEND R47 flakiness
    # class as worktree_owners/memory_within_cap above, a third instance the AMEND's two named
    # rows did not anticipate). Repair U1 (REFUSED-lane-handoff-redesign.md): fixture ONLY the
    # machine probe -- `dd.find_powershell` / `dd.resolve_via_get_command` -- never the organ
    # itself, so `check_dispatch_drift` really calls `_dd.scan`, really parses PLAYBOOK Ch8's
    # dispatch table and really checks `/lane-boot`'s ruled verb; only the host-dependent
    # Get-Command leg is pinned to a clean answer. The real resolution logic (a planted dead
    # command, a shell-less tier, the live command set) has its own tests in
    # tests/test_dispatch_drift.py (AMEND §2's pattern for worktree_owners/memory_within_cap).
    monkeypatch.setattr(dd, "find_powershell", lambda: "pwsh-fixture")
    monkeypatch.setattr(
        dd, "resolve_via_get_command",
        lambda names, **kw: [dd.Resolution(n, True, "fixture: resolved") for n in names])
    memory_fixture = tmp_path / "MEMORY.md"
    memory_fixture.write_text("# memory fixture\n", encoding="utf-8")

    if inject_fail_organ is not None:
        def _fail(repo_path):
            return [aud.Finding(inject_fail_organ.removeprefix("check_"), "fail",
                                "INJECTED by test_handoff_cut_acceptance")]
        monkeypatch.setattr(aud, inject_fail_organ, _fail)

    bundle_root = tmp_path / "dry-cut-out"
    start = time.perf_counter()
    result = gh.generate(
        gh._REPO_ROOT, mode="architect", slug="step1-acceptance", repo=".dev-knowledge",
        date=today, bundle_root=bundle_root, assemble=True, dry_cut=True,
        memory_path=memory_fixture, sessions_root=tmp_path / "no-sessions-store",
    )
    elapsed = time.perf_counter() - start
    return result, elapsed


def test_dry_cut_one_attempt_under_bound_with_bundle_files(tmp_path, monkeypatch):
    """(a) one attempt: a single `generate(dry_cut=True, ...)` call succeeds, no retry.
    (d) wall time <= 120s on the laptop.
    (e) the bundle files are produced.
    """
    result, elapsed = _run_dry_cut(tmp_path, monkeypatch)
    assert elapsed <= WALL_TIME_BOUND_S, (
        f"dry cut took {elapsed:.1f}s, over the {WALL_TIME_BOUND_S}s bound")
    for name in ("HANDOFF_BOOT.md", "RESIDUAL.md", "PROBES.md", "PASTE_THIS.md",
                "HANDOFF_RECEIPT.json"):
        assert (result.bundle_dir / name).exists(), f"{name} was not produced"


def test_dry_cut_evaluates_only_the_named_handoff_organ_set(tmp_path, monkeypatch):
    """(b) only the named handoff organ set from the proposal is evaluated: row 1 (ship_gate)
    runs EXACTLY `audit.HANDOFF_ORGAN_NAMES` through `run_checks(..., parallel=True)`, never
    the whole 57-organ registry (`audit.ALL_CHECKS`)."""
    seen: dict = {}
    real_run_checks = aud.run_checks
    handoff_names = set(aud.HANDOFF_ORGAN_NAMES)

    def _spy(repo_path, checks=None, **kw):
        if checks is not None:
            names = {getattr(c, "__name__", "") for c in checks}
            if names == handoff_names:
                seen["checks"] = checks
                seen["parallel"] = kw.get("parallel")
        return real_run_checks(repo_path, checks=checks, **kw)

    monkeypatch.setattr(aud, "run_checks", _spy)
    _run_dry_cut(tmp_path, monkeypatch)
    assert "checks" in seen, "row 1 never ran the handoff organ set through run_checks"
    assert {f.__name__ for f in seen["checks"]} == handoff_names
    assert len(handoff_names) == 12, "the ratified set is eleven organs plus rulings_carried"
    assert seen["parallel"] is True, "the set must run in parallel (L6)"


def test_dry_cut_not_blocked_by_a_hard_fail_outside_the_set(tmp_path, monkeypatch):
    """(c): a fixture hard-fail in an organ OUTSIDE the handoff set does not block the cut."""
    assert "check_fleet_parity" not in aud.HANDOFF_ORGAN_NAMES
    result, _ = _run_dry_cut(tmp_path, monkeypatch, inject_fail_organ="check_fleet_parity")
    assert result.bundle_dir.exists()
    assert (result.bundle_dir / "HANDOFF_RECEIPT.json").exists()


def test_dry_cut_blocked_by_a_hard_fail_inside_the_set(tmp_path, monkeypatch):
    """(c)'s converse (L4): a fixture hard-fail in an organ INSIDE the handoff set DOES block
    the cut -- the set still has teeth."""
    assert "check_dispatch_drift" in aud.HANDOFF_ORGAN_NAMES
    with pytest.raises(gh.PreflightError):
        _run_dry_cut(tmp_path, monkeypatch, inject_fail_organ="check_dispatch_drift")


def test_check_doc_claims_is_the_one_named_warn_only_exception(tmp_path, monkeypatch):
    """L5 / AMEND item 1: `check_doc_claims` is WARN-tier BY RULING and can never hard-fail the
    cut -- a fixture WARN from it must not block, and it is named by this test, not silently
    excluded by a tier-based predicate (S7's fix: a tier-only test missed exactly this class)."""
    assert aud.HANDOFF_ORGAN_WARN_ONLY == ("check_doc_claims",)

    def _warn_only(repo_path):
        return [aud.Finding("doc_claims", "warn", "INJECTED WARN by the test fixture")]

    monkeypatch.setattr(aud, "check_doc_claims", _warn_only)
    result, _ = _run_dry_cut(tmp_path, monkeypatch)
    assert result.bundle_dir.exists()


def test_the_journal_pin_replaces_the_spine_list_and_leaves_both_organs_real(monkeypatch):
    """The pin is an INPUT, not an organ (terra review of b2-branch-context-tests, H3): the preflight
    row and the `ship_gate` organ stay the real functions, and only the list of unanchored spine
    entries they ask `journal_anchor` for is empty."""
    import journal_anchor as ja

    organ, row, predicate = aud.check_journal_spine_anchor, gh._journal_spine_gaps, ja.unanchored_on_spine
    pin_journal_spine(monkeypatch)
    assert aud.check_journal_spine_anchor is organ
    assert gh._journal_spine_gaps is row
    assert ja.unanchored_on_spine is not predicate
    assert ja.unanchored_on_spine(Path("."), "main", "floor", "journal text") == []


@pytest.mark.xdist_group(name="branch_context")
def test_the_dry_cut_tests_give_the_same_verdict_on_a_lane_whose_tree_lags_main(
        tmp_path_factory):
    """The witness for the four dry-cut tests that read the live JOURNAL spine (B2-W1 W1-8): the
    same four, run from a clone whose `main` is one merge AHEAD of the lane's tree (the shape a
    lane has once a sibling merged), must pass as they do on `main`."""
    names = ("test_dry_cut_one_attempt_under_bound_with_bundle_files",
             "test_dry_cut_evaluates_only_the_named_handoff_organ_set",
             "test_dry_cut_not_blocked_by_a_hard_fail_outside_the_set",
             "test_check_doc_claims_is_the_one_named_warn_only_exception")
    witness(tmp_path_factory, *(f"tests/test_handoff_cut_acceptance.py::{n}" for n in names),
            peer_files={"PEER-PROBE.txt": "a sibling lane merged to main\n"})
