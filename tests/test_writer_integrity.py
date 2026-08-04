"""[#465] leg 4 — the writer-integrity class: a check whose subject no longer exists.

THE DEFECT IS THE WRITER, NOT THE ROW. `handoff_tag_canonicity` emitted a verdict token every
day for two spec generations after its subject stopped existing, and nothing in the writer, the
dailies, `ALL_CHECKS` or the ship gate noticed. Census over every `ecosystem/*/history/*.md` on
`origin/automation/fleet-audit`: 285 `n/a` vs 5 `pass`, and the five passes are all 2026-06-15
carrying the SAME evidence string as the n/a's — that era was the leg-1 skip-as-pass defect,
fixed at `80e743aa`. The check was therefore either lying or inert for its entire recorded life.

Deleting it would have repaired the instance and left the class: the next check to lose its
subject goes inert identically and is equally invisible. So leg 4 built the DETECTOR and let it
decide the disposition (FR-5). It found `handoff_tag_canonicity`, and the disposition was
RETIRE — `ALL_CHECKS` 39 -> 38.

AC-1 EX-ANTE RED WITNESS, recorded on unmodified HEAD `0cf327e5` BEFORE any fix existed
(a witness authored after the change is a description, not a witness — LESSONS.md 2026-07-30):

    R1  AssertionError: no inert-check detector exists (the [#465] leg-4 defect)
    R2  the fail branch is unreachable from the live spec: got 'n/a' /
        '§3.1 section not found (consolidated?) — nothing to lint'
    R3  AssertionError: 'clean pass' is contained in check_handoff_tag_canonicity.__doc__
    -> 3 failed in 0.52s

R2 and R3 are discharged BY THE RETIREMENT (the unreachable branch and the stale docstring left
with the function); they are replaced below by assertions that the retirement actually happened,
so their subject cannot quietly come back. R1 survives as the generic detector proof.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest

import audit as aud


# ---------------------------------------------------------------------------
# FR-1 — an n/a says WHY, in machine-readable form, without touching Finding.
# ---------------------------------------------------------------------------

def test_na_reason_round_trips_and_keeps_the_locked_finding_shape():
    f = aud._na("x", "SUBJECT-ABSENT", "the subject is gone")
    assert (f.check_name, f.status) == ("x", "n/a")
    assert aud._na_reason(f) == "SUBJECT-ABSENT"
    assert aud._na_reason(aud._na("y", "NOT-APPLICABLE", "not here")) == "NOT-APPLICABLE"
    # The LOCKED spine contract is untouched: three fields, five-value status enum.
    assert [x for x in (f.check_name, f.status, f.evidence)] == list(f.__dict__.values())


def test_na_reason_is_none_for_an_unclassified_na():
    """None is meaningful, not an error value — the detector turns it into a loud WARN rather
    than guessing a reason."""
    assert aud._na_reason(aud.Finding("y", "n/a", "bare, no prefix")) is None
    assert aud._na_reason(aud.Finding("y", "pass", "[n/a-reason:SUBJECT-ABSENT] x")) is None


def test_na_rejects_an_unknown_reason():
    """A mis-typed reason must raise, never silently become an unclassifiable n/a."""
    with pytest.raises(ValueError):
        aud._na("x", "MAYBE", "…")


def test_na_evidence_stays_markdown_table_safe():
    assert "|" not in aud._na("x", "SUBJECT-ABSENT", "a | b").evidence


# ---------------------------------------------------------------------------
# FR-2 / R1 — the detector. Self-enumerating over ALL_CHECKS, never a roster.
# ---------------------------------------------------------------------------

def test_R1_detector_flags_an_unconditionally_inert_member(tmp_path):
    """The RED that proved the class, now green against a synthetic member.

    Synthetic ON PURPOSE, per the contract's F5: had this pinned `handoff_tag_canonicity`, the
    test would have evaporated the moment FR-5 retired it — the detector would then be covered
    by nothing, which is the same invisibility the leg exists to remove.
    """
    def check_synthetic_inert(_repo):
        return [aud._na("synthetic_inert", "SUBJECT-ABSENT", "no subject anywhere")]

    out = aud.detect_unconditionally_inert_checks(
        {"hub": tmp_path, "consumer": tmp_path}, [check_synthetic_inert])
    assert [(f.check_name, f.status) for f in out] == [("writer_integrity", "warn")]
    assert "synthetic_inert" in out[0].evidence
    assert "INERT" in out[0].evidence


def test_AC3_detector_self_enumerates_with_no_edit_to_any_list(tmp_path, monkeypatch):
    """AC-3: adding a member to ALL_CHECKS is enough — the detector late-binds the registry.

    Called with `checks=None` deliberately: that is the production path, and it is what proves
    there is no hand-maintained roster to forget to update (FR-4)."""
    def check_added_tomorrow(_repo):
        return [aud._na("added_tomorrow", "SUBJECT-ABSENT", "subject never existed")]

    monkeypatch.setattr(aud, "ALL_CHECKS", [check_added_tomorrow])
    out = aud.detect_unconditionally_inert_checks({"hub": tmp_path})
    assert len(out) == 1 and "added_tomorrow" in out[0].evidence


def test_AC4_a_consumer_lacking_a_hub_surface_is_NOT_a_defect(tmp_path):
    """FR-7 / AC-4 — the D1 regression from the wave-1 producer lane, witnessed not argued.

    NOT-APPLICABLE everywhere is a correct skip. Flagging it would manufacture a fleet gap on
    every consumer that legitimately lacks a hub-only surface, which is precisely what the
    wave-1 Codex output would have done to corp-monorepo and ai-council.
    """
    def check_hub_only(_repo):
        return [aud._na("hub_only_thing", "NOT-APPLICABLE", "hub-only — skipped")]

    assert aud.detect_unconditionally_inert_checks(
        {"hub": tmp_path, "consumer": tmp_path}, [check_hub_only]) == []


def test_detector_ignores_a_member_that_can_report_something_somewhere(tmp_path):
    """One real verdict anywhere means the check is alive — not inert."""
    seen = {"n": 0}

    def check_mixed(_repo):
        seen["n"] += 1
        if seen["n"] == 1:
            return [aud._na("mixed", "SUBJECT-ABSENT", "absent here")]
        return [aud.Finding("mixed", "pass", "fired for real")]

    assert aud.detect_unconditionally_inert_checks(
        {"a": tmp_path, "b": tmp_path}, [check_mixed]) == []


# ---------------------------------------------------------------------------
# FR-3 — the detector must be loud when it cannot see, never quietly clean.
# ---------------------------------------------------------------------------

def test_detector_warns_on_an_unclassified_na(tmp_path):
    def check_bare_na(_repo):
        return [aud.Finding("bare_na", "n/a", "no reason prefix")]

    out = aud.detect_unconditionally_inert_checks({"hub": tmp_path}, [check_bare_na])
    assert [f.status for f in out] == ["warn"]
    assert "machine-readable reason" in out[0].evidence


def test_detector_warns_when_a_check_raises(tmp_path):
    def check_explodes(_repo):
        raise RuntimeError("boom")

    out = aud.detect_unconditionally_inert_checks({"hub": tmp_path}, [check_explodes])
    assert [f.status for f in out] == ["warn"]
    assert "could not be evaluated" in out[0].evidence


def test_detector_warns_when_a_check_returns_nothing(tmp_path):
    out = aud.detect_unconditionally_inert_checks({"hub": tmp_path}, [lambda _r: []])
    assert [f.status for f in out] == ["warn"]
    assert "cannot be read as clean" in out[0].evidence
    assert "NOT judged" in out[0].evidence, "inertness must not be concluded without coverage"


# ---------------------------------------------------------------------------
# FR-5 / FR-6 — the retirement actually happened, and cannot quietly come back.
# (These replace R2 and R3, whose subject the retirement removed.)
# ---------------------------------------------------------------------------

def test_R2_R3_discharged_handoff_tag_canonicity_is_retired():
    assert not hasattr(aud, "check_handoff_tag_canonicity"), \
        "the retired check is back — R2's unreachable branch and R3's stale docstring with it"
    assert not any(c.__name__ == "check_handoff_tag_canonicity" for c in aud.ALL_CHECKS)


def test_all_checks_count_is_pinned():
    """AC-2: a silent count change is a contract breach.

    History: 39 -> 38 when check_handoff_tag_canonicity was retired ([#465] leg 4); 38 -> 39
    when check_preflight_backlog_ids was added ([#483] R3 — the ADVISORY leg, WARN-tier, with
    hard-gating deferred pending zero false positives over two windows, 2026-08-04).

    Renamed from `..._post_retirement_38`: the count moved by an ADDITION, so a name asserting
    a post-retirement 38 would have described neither the number nor the reason.
    """
    assert len(aud.ALL_CHECKS) == 39


def test_no_surviving_docstring_describes_the_removed_skip_as_pass_behaviour():
    """FR-6, generalized past the one docstring: leg 1 (`80e743aa`) removed skip-as-pass, so no
    check may still claim it "degrades to a clean pass"."""
    offenders = [c.__name__ for c in aud.ALL_CHECKS if "clean pass" in (c.__doc__ or "")]
    assert offenders == [], offenders


@pytest.mark.live_repo
def test_live_registry_has_no_unconditionally_inert_check_left(tmp_path):
    """The detector's own verdict on the live registry after the retirement it prompted.

    Honest limit, stated rather than implied: this runs the real checks against the live hub and
    a bare consumer-shaped tree, so it proves no member is inert ACROSS THOSE TWO — not across
    every fleet repo, which `audit.py run` covers at fleet scope.
    """
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    out = aud.detect_unconditionally_inert_checks(
        {"hub": Path(aud._REPO_ROOT), "consumer": consumer})
    # EMPTY, not merely "no INERT line" (terra HIGH, 2026-08-04). Filtering for "INERT" would
    # pass while the live registry emitted writer_integrity WARNs for an unclassified n/a, a
    # check that raised, or a check that returned nothing — and this is the ONLY test that runs
    # the real ALL_CHECKS through the detector, so it is where the 32 mechanically converted
    # call sites are proven classifiable and evaluable in production shape.
    assert [f.evidence for f in out] == [], [f.evidence for f in out]


# ---------------------------------------------------------------------------
# FR-5 — the retirement is visible to a reader of the DAILIES, not only a commit.
# ---------------------------------------------------------------------------

def test_history_names_a_check_that_disappeared_since_the_previous_reading(tmp_path, monkeypatch):
    """Without this, a retired check simply stops appearing, and its absence is
    indistinguishable from a run that never reached it — the same invisibility the leg exists
    to remove. Derived from the history files themselves; there is no retired-check registry."""
    from datetime import date

    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path)
    hist = tmp_path / "demo" / "history"
    hist.mkdir(parents=True)
    (hist / "2026-08-03.md").write_text(
        "## 2026-08-03\n\n| Check | Status | Evidence |\n|---|---|---|\n"
        "| kept_check | pass | fine |\n| doomed_check | n/a | nothing |\n\n",
        encoding="utf-8", newline="\n")

    state = aud.RepoState(name="demo", path=str(tmp_path / "demo"),
                          last_audit="2026-08-04",
                          findings=[aud.Finding("kept_check", "pass", "fine")])
    aud.append_history(state, date(2026, 8, 4))

    written = (hist / "2026-08-04.md").read_text(encoding="utf-8")
    assert "Checks retired since the previous reading:** doomed_check" in written
    assert "kept_check" not in written.split("|---|---|---|")[0]  # not named as retired


def test_history_says_nothing_when_no_check_disappeared(tmp_path, monkeypatch):
    """The notice must not fire on an ordinary day, or it becomes noise and stops being read."""
    from datetime import date

    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path)
    hist = tmp_path / "demo" / "history"
    hist.mkdir(parents=True)
    (hist / "2026-08-03.md").write_text(
        "## 2026-08-03\n\n| Check | Status | Evidence |\n|---|---|---|\n"
        "| kept_check | pass | fine |\n\n", encoding="utf-8", newline="\n")

    state = aud.RepoState(name="demo", path=str(tmp_path / "demo"), last_audit="2026-08-04",
                          findings=[aud.Finding("kept_check", "pass", "fine")])
    aud.append_history(state, date(2026, 8, 4))
    assert "retired since" not in (hist / "2026-08-04.md").read_text(encoding="utf-8")


def test_history_first_ever_run_reports_no_retirement(tmp_path, monkeypatch):
    """No prior reading means nothing was retired — not 'everything was'."""
    from datetime import date

    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path)
    state = aud.RepoState(name="fresh", path=str(tmp_path / "fresh"), last_audit="2026-08-04",
                          findings=[aud.Finding("a_check", "pass", "fine")])
    aud.append_history(state, date(2026, 8, 4))
    assert "retired since" not in (tmp_path / "fresh" / "history" / "2026-08-04.md").read_text(
        encoding="utf-8")


# ---------------------------------------------------------------------------
# The detector must actually RUN in production — terra HIGH, 2026-08-04.
# A detector nothing calls is a mechanism that reports nothing, which is the
# exact class this leg exists to remove.
# ---------------------------------------------------------------------------

def test_the_rule_is_defined_once_and_shared_by_both_callers():
    """`detect_unconditionally_inert_checks` (test seam, runs the checks) and `cmd_run`
    (production, reuses findings already computed) must not carry two copies of the rule."""
    import inspect

    src = inspect.getsource(aud.detect_unconditionally_inert_checks)
    assert "classify_inert_checks(" in src, "the detector re-implements the rule"
    # `cmd_run` is a click Command; the function body hangs off `.callback`.
    run_src = inspect.getsource(getattr(aud.cmd_run, "callback", aud.cmd_run))
    assert "classify_inert_checks(" in run_src, \
        "cmd_run does not use the shared rule — the detector is not wired into production"


def test_classify_inert_checks_matches_the_running_detector(tmp_path):
    """Equivalence of the two paths, on the same input."""
    def check_dead(_repo):
        return [aud._na("dead", "SUBJECT-ABSENT", "gone")]

    via_running = aud.detect_unconditionally_inert_checks({"hub": tmp_path}, [check_dead])
    via_findings = aud.classify_inert_checks({"dead": {"hub": check_dead(tmp_path)}}, ["hub"])
    assert [f.evidence for f in via_running] == [f.evidence for f in via_findings]


def test_same_day_rerun_does_not_repeat_a_retirement_notice(tmp_path, monkeypatch):
    """terra HIGH 2026-08-04: comparing strictly against an EARLIER DATE meant a second run on
    the same day compared against yesterday and re-emitted a notice the first run had already
    written — a false "retired since the previous reading" in the durable history, every rerun."""
    from datetime import date

    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path)
    hist = tmp_path / "demo" / "history"
    hist.mkdir(parents=True)
    (hist / "2026-08-03.md").write_text(
        "## 2026-08-03\n\n| Check | Status | Evidence |\n|---|---|---|\n"
        "| kept | pass | fine |\n| doomed | n/a | nothing |\n\n", encoding="utf-8", newline="\n")

    state = aud.RepoState(name="demo", path=str(tmp_path / "demo"), last_audit="2026-08-04",
                          findings=[aud.Finding("kept", "pass", "fine")])
    aud.append_history(state, date(2026, 8, 4))
    aud.append_history(state, date(2026, 8, 4))          # the rerun
    written = (hist / "2026-08-04.md").read_text(encoding="utf-8")
    assert written.count("retired since the previous reading") == 1, written


def test_only_the_last_reading_in_a_file_is_compared(tmp_path, monkeypatch):
    """Unioning every appended table would resurrect names retired several readings ago and
    suppress the notice for a check that vanished today."""
    from datetime import date

    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path)
    hist = tmp_path / "demo" / "history"
    hist.mkdir(parents=True)
    (hist / "2026-08-03.md").write_text(
        "## 2026-08-03 — a\n\n| Check | Status | Evidence |\n|---|---|---|\n"
        "| long_gone | n/a | x |\n\n"
        "## 2026-08-03 — b\n\n| Check | Status | Evidence |\n|---|---|---|\n"
        "| kept | pass | fine |\n| doomed | n/a | x |\n\n", encoding="utf-8", newline="\n")

    state = aud.RepoState(name="demo", path=str(tmp_path / "demo"), last_audit="2026-08-04",
                          findings=[aud.Finding("kept", "pass", "fine")])
    aud.append_history(state, date(2026, 8, 4))
    written = (hist / "2026-08-04.md").read_text(encoding="utf-8")
    assert "doomed" in written and "long_gone" not in written, written


def test_cmd_run_actually_attaches_the_warn_to_the_hub_state(monkeypatch, tmp_path):
    """BEHAVIOURAL proof that the detector runs in production, not a source-string match.

    The sibling test greps `cmd_run` for the call; a grep passes against a call that is dead,
    guarded off, or in an unreachable branch. This one drives `cmd_run` end to end with the
    persistence seams captured and asserts the writer_integrity WARN actually lands on the HUB's
    state — and, per FR-7, on no consumer's.
    """
    from datetime import date

    saved: dict[str, aud.RepoState] = {}
    hub, consumer = aud.HUB_REPO_NAME, "some-consumer"

    def fake_audit_repo(name, _path, _run_date):
        # Both repos see the same inert check: n/a everywhere, SUBJECT-ABSENT on the hub.
        reason = "SUBJECT-ABSENT" if name == hub else "NOT-APPLICABLE"
        return aud.RepoState(name=name, path=str(tmp_path / name), last_audit="2026-08-04",
                             findings=[aud._na("zombie_check", reason, "subject is gone")])

    monkeypatch.setattr(aud, "discover_repos", lambda: [hub, consumer])
    monkeypatch.setattr(aud, "load_state", lambda _n: None)
    monkeypatch.setattr(aud, "resolve_repo_path", lambda n, _p: tmp_path / n)
    monkeypatch.setattr(aud, "audit_repo", fake_audit_repo)
    monkeypatch.setattr(aud, "save_state", lambda s: saved.__setitem__(s.name, s))
    monkeypatch.setattr(aud, "append_history", lambda *_a, **_k: None)
    monkeypatch.setattr(aud, "generate_report", lambda *_a, **_k: "report")
    monkeypatch.setattr(aud, "write_report", lambda *_a, **_k: tmp_path / "r.md")
    monkeypatch.setattr(aud, "_commit_routine_outputs", lambda *_a, **_k: None)
    monkeypatch.setattr(aud, "_today", lambda: date(2026, 8, 4), raising=False)

    callback = getattr(aud.cmd_run, "callback", aud.cmd_run)
    try:
        callback(None)
    except SystemExit:
        pass  # cmd_run exits non-zero only on FAILs; WARNs must not cause one

    hub_warns = [f for f in saved[hub].findings if f.check_name == "writer_integrity"]
    assert hub_warns, "the detector's WARN never reached the hub state — it is not wired in"
    assert "zombie_check" in hub_warns[0].evidence
    assert [f for f in saved[consumer].findings if f.check_name == "writer_integrity"] == [], \
        "a writer_integrity WARN was written onto a CONSUMER — that is the FR-7 fleet gap"


def test_inertness_is_not_concluded_from_a_partial_fleet(tmp_path):
    """terra HIGH r2 — coverage is part of the rule. A check n/a on the one repo that WAS
    evaluated must not be called inert while another repo went unaudited: that would let a
    single unavailable tree retire a check that is alive elsewhere."""
    findings = [aud._na("maybe_dead", "SUBJECT-ABSENT", "absent here")]
    out = aud.classify_inert_checks({"maybe_dead": {"hub": findings}}, ["hub", "consumer"])
    assert [f.status for f in out] == ["warn"]
    assert "coverage is incomplete" in out[0].evidence
    assert "INERT" not in out[0].evidence, "inertness was concluded from a partial fleet"


def test_an_unavailable_previous_reading_blocks_the_retirement_comparison(tmp_path, monkeypatch):
    """terra HIGH r2 — an unavailable repo's reading is a single `availability` row. Treating it
    as complete would announce EVERY check the repo normally runs as retired in the next daily,
    writing a false entry into the durable history."""
    from datetime import date

    monkeypatch.setattr(aud, "ECOSYSTEM_DIR", tmp_path)
    hist = tmp_path / "demo" / "history"
    hist.mkdir(parents=True)
    (hist / "2026-08-03.md").write_text(
        "## 2026-08-03\n\n| Check | Status | Evidence |\n|---|---|---|\n"
        "| availability | unavailable | Path not found: /gone |\n\n",
        encoding="utf-8", newline="\n")

    state = aud.RepoState(name="demo", path=str(tmp_path / "demo"), last_audit="2026-08-04",
                          findings=[aud.Finding("kept", "pass", "fine")])
    aud.append_history(state, date(2026, 8, 4))
    written = (hist / "2026-08-04.md").read_text(encoding="utf-8")
    assert "Retirement comparison unavailable" in written
    assert "retired since the previous reading" not in written


def test_cmd_run_persists_consumers_even_when_a_later_repo_raises(monkeypatch, tmp_path):
    """terra HIGH r2 — deferring ALL persistence until after the loop silently changed failure
    semantics: a later repo raising discarded earlier repos' durable progress. Consumers save as
    they complete; the hub is persisted in a `finally` so it survives too."""
    saved: dict[str, aud.RepoState] = {}
    hub = aud.HUB_REPO_NAME

    def fake_audit_repo(name, _p, _d):
        if name == "explodes":
            raise RuntimeError("boom")
        return aud.RepoState(name=name, path=str(tmp_path / name), last_audit="2026-08-04",
                             findings=[aud.Finding("a_check", "pass", "fine")])

    monkeypatch.setattr(aud, "discover_repos", lambda: [hub, "good-consumer", "explodes"])
    monkeypatch.setattr(aud, "load_state", lambda _n: None)
    monkeypatch.setattr(aud, "resolve_repo_path", lambda n, _p: tmp_path / n)
    monkeypatch.setattr(aud, "audit_repo", fake_audit_repo)
    monkeypatch.setattr(aud, "save_state", lambda s: saved.__setitem__(s.name, s))
    monkeypatch.setattr(aud, "append_history", lambda *_a, **_k: None)
    monkeypatch.setattr(aud, "generate_report", lambda *_a, **_k: "report")
    monkeypatch.setattr(aud, "write_report", lambda *_a, **_k: tmp_path / "r.md")
    monkeypatch.setattr(aud, "_commit_routine_outputs", lambda *_a, **_k: None)

    callback = getattr(aud.cmd_run, "callback", aud.cmd_run)
    with pytest.raises(RuntimeError):
        callback(None)
    assert "good-consumer" in saved, "an earlier consumer's durable progress was lost"
    assert hub in saved, "the hub was not persisted despite the finally"
