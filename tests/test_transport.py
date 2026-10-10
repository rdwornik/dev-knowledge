"""lane-transport-registry (BATCH-WAVE5B-N1 #9): the transport's kinds, registered, and the
one write gate every future writer composes.

Done-when 1: `ecosystem/transport-registry.yaml` lists every kind the code uses, and a test
derives the kind set from the code and asserts none is missing -- `test_derivation_finds_
nothing_missing_from_the_real_registry` below, against the real `scripts/` tree, not a fixture.

Done-when 2: `transport.write` refuses an unregistered writer -- `test_handback_cannot_write_
the_integrators_refused_kind` is the literal case the contract names.

Done-when 3: the stray-file report is exercised in `test_scan_*` (report-only: `scan()` never
writes, moves or deletes).

Every test but the derivation one drives a synthetic transport in `tmp_path`; nothing here
touches the real drive.
"""
from __future__ import annotations

import hashlib
import importlib
import os
import re
import shutil
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

REGISTRY_PATH = _REPO / "ecosystem" / "transport-registry.yaml"


def _mod(name: str):
    return importlib.import_module(name)


@pytest.fixture()
def t():
    return _mod("transport")


@pytest.fixture()
def registry(t):
    return t.load_registry(REGISTRY_PATH)


@pytest.fixture()
def world(tmp_path: Path) -> dict:
    root = tmp_path / "drive"
    (root / "to-cc").mkdir(parents=True)
    (root / "to-browser").mkdir()
    return {"root": root, "cc": root / "to-cc", "browser": root / "to-browser"}


# --- the registry itself, as data ----------------------------------------------------------------

def test_the_real_registry_loads_and_every_row_is_well_formed(t, registry):
    assert len(registry) >= 15
    names = [k.name for k in registry]
    assert len(names) == len(set(names)), "duplicate kind names"
    for k in registry:
        assert k.folder in t.FOLDERS
        assert k.writers, f"{k.name} has no writer"
        # Three sanctioned prefix shapes (lane-transport-strays widened this beyond the
        # original code-derived-only set, which was always a hyphen-terminated template lead-in):
        #   (a) a live template prefix, ending in "-", with variable content after it
        #       (the ORIGINAL and still the common shape: `GO-`, `SESSION-`, ...), or a bare
        #       word lead-in the pattern extends with more required content (`WAVE`, `LEG`,
        #       `PASTE_THIS`) -- proven by a PLAIN (non-regex) substring check: the prefix is
        #       literal text with no regex metacharacters, so it must appear verbatim right
        #       after the pattern's `^` anchor. (`re.escape` is deliberately NOT used here --
        #       it escapes `-` too, which would make this assert the wrong thing for every
        #       hyphen-bearing prefix, hiding the one real drift this exists to catch.)
        #   (b) empty -- no fixed lead-in exists at all (a pure dated-slug/regex-driven kind,
        #       e.g. DATED_SLUG); every such kind's own pattern is exercised by a dedicated
        #       test below instead of this generic round-trip;
        #   (c) a one-off EXACT filename with no placeholder at all (`STATUS.md`,
        #       `R5-DECLARED.md`) -- its own pattern must therefore match the prefix text
        #       verbatim as a complete filename.
        pattern_text = k.regex.pattern
        assert pattern_text.startswith("^"), f"{k.name}'s pattern must be left-anchored"
        if k.prefix:
            assert pattern_text[1:].startswith(k.prefix) or k.regex.match(k.prefix), (
                f"{k.name}: prefix {k.prefix!r} is neither a literal lead-in of its own "
                f"pattern {k.regex.pattern!r} nor a complete match against it")


#: The kinds `lane-transport-registry` (BATCH-WAVE5B-N1 #9) originally built the registry with --
#: every one of these follows exactly one shape (prefix + arbitrary content + `.md`), so a
#: synthetic "prefix+example+date+.md" sample is a faithful round-trip for them. Everything else
#: in the registry is a `lane-transport-strays` addition; several require specific literal
#: content right after the prefix (`DISPATCH-(CARD|CONTRACT)-`, `BROWSER-SEAT-FLOOR-(DRAFT|PIN)-`,
#: ...) or a non-`.md` extension (`.zip`, `.js`, `.log`, `.json`/`.stderr.txt`) that a generic
#: sample cannot satisfy -- those are proven instead, against their REAL observed filenames, by
#: `test_lane_transport_strays_additions_classify_their_real_observed_filenames` below.
_ORIGINAL_KIND_NAMES = {
    "GO", "LEDGER", "PLAN", "BATCH", "DECLARE", "AMEND", "LANE_END", "HANDBACK_REFUSED",
    "SESSION", "REFUSED", "SEAT_BOOT", "MERGE_PLAN", "ESCALATE", "LANE_CONTRACT",
    "RATIFICATION", "STATUS", "QUESTION", "ANSWER", "CLOSURE_LIST", "STATE_BATCH", "DIGEST",
}


def test_every_hyphen_terminated_kind_classifies_a_filename_shaped_from_its_own_prefix(t, registry):
    """Round-trip for shape (a) above: a synthetic filename built from a kind's own `prefix`
    (which ends in "-") must classify back to THAT kind (not a shorter sibling prefix) --
    catches a `pattern` that drifted from `prefix`. Shapes (b)/(c) (no trailing hyphen, or
    empty) cannot build a generic sample this way -- see the dedicated tests below."""
    for k in registry:
        if k.name not in _ORIGINAL_KIND_NAMES or not k.prefix.endswith("-"):
            continue
        sample = f"{k.prefix}example-2026-09-25.md"
        got = t.classify(sample, registry)
        assert got is not None, f"{k.name}'s own prefix {k.prefix!r} does not self-classify"
        assert got.name == k.name, (
            f"{sample!r} classified as {got.name!r}, not {k.name!r} -- a shorter sibling "
            f"prefix (e.g. LANE- vs LANE-END-) is shadowing it")


# --- lane-transport-strays: the widened shapes (literal filenames, bare word lead-ins, and
# no-fixed-lead-in kinds a 300-file historical-debris classification pass actually needed) ------

#: Real filenames the live transport's stray-file report actually held (300+ files, lane-
#: transport-strays), one per new kind this lane's registry additions classify -- proof against
#: ground truth rather than a synthetically-generated sample, since many of these kinds require
#: specific literal content after their prefix or a non-`.md` extension a generic sample cannot
#: exercise (see the scoping note on the round-trip test above).
_LANE_TRANSPORT_STRAYS_SAMPLES = {
    "ADDENDUM-lane-t-000-nc1-clear-A2.md": "ADDENDUM",
    "AMEND2-PLAN-WAVE5-2026-09-24.md": "AMEND_PLAN",
    "ARCHITECT-INBOX-2026-09-05.md": "ARCHITECT_INBOX",
    "ARCHITECT-INBOX-2026-09-05-002.md": "ARCHITECT_INBOX",
    "CONTRACT-cv-rewrite-v4-2026-09-10.md": "CONTRACT",
    "CONTRACT-github-profile-copy-2026-09-10-v1-superseded.md": "CONTRACT",
    "dispatch-measure.ps1": "DISPATCH_MEASURE_SCRIPT",
    "DISPATCHER-WAVE5B-N1-2026-09-24-v1-superseded.md": "DISPATCHER",
    "DRAFT-cv-copy-v8-2026-09-10.md": "DRAFT",
    "FINAL-batch-u-close-packet.md": "FINAL",
    "FINDING-filings-N2-P11-form.md": "FINDING",
    "FINISH-5A-2026-09-24.md": "FINISH",
    "FIX-BATCH-W-002-guard-root.md": "FIX",
    "FLEET-READINESS-CONTRACT-2026-09-05.md": "FLEET_READINESS_CONTRACT",
    "INBOX-dev-knowledge-2026-09-06-028.md": "INBOX_DEV_KNOWLEDGE",
    "INTEGRATOR-FINISH-WAVE4A-2026-09-22-v2-superseded.md": "INTEGRATOR_FINISH",
    "INTEGRATOR-PREHANDOFF-2026-09-24.md": "INTEGRATOR_PREHANDOFF",
    "INTEGRATOR-STANDING-ORDER-WAVE4B-2026-09-22.md": "INTEGRATOR_STANDING_ORDER",
    "INTEGRATOR-STANDING-ORDER-2026-09-20.md": "INTEGRATOR_STANDING_ORDER",
    "INTEGRATOR-WAVE5A-2026-09-23-v1-superseded.md": "INTEGRATOR_WAVE",
    "INTEGRATOR-WAVE5B-N1-2026-09-24.md": "INTEGRATOR_WAVE",
    "lane-3-9-window-metrics.patch": "LANE_WINDOW_METRICS_PATCH",
    "POSTWAVE-CHAIN-2026-09-22-v1-superseded.md": "POSTWAVE_CHAIN",
    "PRECUT-2026-09-24.md": "PRECUT",
    "R5-DECLARED.md": "R5_DECLARED",
    "RECOVERED-lane-u-000-branch-enum-parity.patch": "RECOVERED",
    "RULING-RELAY-DECLARE-SITTING-2026-09-06.md": "RULING_RELAY",
    "run-lane-copilot.ps1": "RUN_LANE_COPILOT_SCRIPT",
    "SUITE-ANALYTICS-CODESPACES-2026-09-08.log": "SUITE_LOG",
    "SUITE-BASELINE-CODESPACES-2026-09-08.log": "SUITE_LOG",
    "SUPPLEMENT-ANSWERS-2026-09-07.md": "SUPPLEMENT_ANSWERS",
    "SUPPLEMENT-ANSWERS-CITATIONS-2026-09-08.md": "SUPPLEMENT_ANSWERS",
    "SUPPLEMENT-QUESTIONS-2026-09-24.md": "SUPPLEMENT_QUESTIONS",
    "WAVE2-ORDER-2026-09-20.md": "WAVE_ORDER",
    "WAVE2-SUBWAVE-PLAN.md": "WAVE_SUBWAVE_PLAN",
    "WAVE3-COMMON-2026-09-21.md": "WAVE_COMMON",
    "WAVE4B-COMMON-2026-09-22.md": "WAVE_COMMON",
    "WAVE3-CLOSE-2026-09-19.md": "WAVE_CLOSE",
    "AJ-SECOND-PASS-2026-09-05.md": "AJ_SECOND_PASS",
    "FUNNEL-GROOM-2026-09-05.md": "FUNNEL_GROOM",
    "ADR-120-the-spine-is-the-whole-loop.md": "ADR_COPY",
    "BOOT-SESSION-8-SECTION-2026-09-08.md": "BOOT_SESSION",
    "BRIEFING-2026-09-17-retrospective-priorities-and-how-to-operate.md": "BRIEFING",
    "BROWSER-SEAT-FLOOR-DRAFT-2026-09-06.md": "BROWSER_SEAT_FLOOR",
    "BROWSER-SEAT-FLOOR-DRAFT-2026-09-06.md.sha256": "BROWSER_SEAT_FLOOR",
    "BROWSER-SEAT-FLOOR-PIN-2026-09-06.txt": "BROWSER_SEAT_FLOOR",
    "browser-seat-skills-2026-09-06.zip": "BROWSER_SEAT_SKILLS",
    "CARRIED-QUESTIONS-ELEVEN-2026-09-08.md": "CARRIED_QUESTIONS",
    "CLOSE-2026-09-17-window-close-and-successor-start.md": "CLOSE",
    "CLOSURE-VERDICTS-2026-09-13.md": "CLOSURE_VERDICTS",
    "COPY-MEMORY.md": "COPY",
    "COPY-2026-09-06-technical-batch-t-close-packet.md": "COPY",
    "DECISION-SHEET-cv-f2-2026-09-10.md": "DECISION_SHEET",
    "DEFECT-transport-grammar-seat-name-collision.md": "DEFECT",
    "DELETE-LIST-2026-09-13.md": "DELETE_LIST",
    "DISPATCH-CARD-2026-09-20.md": "DISPATCH_ARTIFACT",
    "DISPATCH-CONTRACT-2026-09-19.md": "DISPATCH_ARTIFACT",
    "DOCS-CUT-LIST-2026-09-13.md": "DOCS_CUT_LIST",
    "HANDBACK-batch-AC-consolidated.md": "HANDBACK",
    "HANDBACK-wave2-boot-base-2026-09-19.md": "HANDBACK",
    "HANDOFF-SUPPLEMENT-2026-09-06.md": "HANDOFF_SUPPLEMENT",
    "HANDOFF-VERIFY-2026-09-08-architect-2.md": "HANDOFF_VERIFY",
    "HANDOFF_BOOT-2026-09-06-architect.md": "HANDOFF_BOOT_TRANSPORT",
    "HANDOVER-ARCHITECTURE-2026-09-08.md": "HANDOVER",
    "HOW-TO-DISPATCH-AND-INTEGRATE-2026-09-20-v1-superseded.md": "HOW_TO_DISPATCH_AND_INTEGRATE",
    "INTEGRATOR-STOP-wave2-2026-09-19.md": "INTEGRATOR_WAVE2",
    "INTEGRATOR-wave2-2026-09-19.md": "INTEGRATOR_WAVE2",
    "INTEGRATOR-wave2-pass2-2026-09-19.md": "INTEGRATOR_WAVE2",
    "LAUNCH-REPORT-night-wave2-2026-09-19.md": "LAUNCH_REPORT",
    "LEG1-BOOT-BASE-ITEMISED-2026-09-19.md": "LEG_REPORT",
    "LEG2-SPINE-PRIOR-ART-2026-09-19.md": "LEG_REPORT",
    "NIGHT-LEG1-ARMED-CENSUS-2026-09-19.md": "NIGHT_LEG",
    "MAP-2026-09-16-harness-state-and-defects.md": "MAP",
    "MAP-DATA-CORRECTED-2026-09-20.js": "MAP_DATA",
    "MAP-VERIFICATION-2026-09-20.md": "MAP_VERIFICATION",
    "NEW-ARCHITECT-03-PLAN-2026-09-20-SUPERSEDED-v1.md": "NEW_ARCHITECT",
    "NEW-ARCHITECT-03-PLAN-2026-09-20.md": "NEW_ARCHITECT",
    "PASTE_THIS.md": "PASTE_THIS",
    "PASTE_THIS-2026-09-19-dev-knowledge-architect.md": "PASTE_THIS",
    "PERMISSION-DIAGNOSIS-night-wave2-2026-09-19.md": "PERMISSION_DIAGNOSIS",
    "PIN-2026-09-07.md": "PIN",
    "POSTURE-v3-split-2026-09-06-r2.md": "POSTURE",
    "POSTURE-v3-split-2026-09-06.md": "POSTURE",
    "PREPARED-filing-transport-delivery-refuses-loudly-2026-09-19.md": "PREPARED",
    "PROPOSED-CLOSURES-2026-09-24.md": "PROPOSED_CLOSURES_LEGACY",
    "RECEIPT-wave2-integrator-pass1-2026-09-19.json": "RECEIPT_WAVE2",
    "RECEIPT-wave2-integrator-pass1-2026-09-19.stderr.txt": "RECEIPT_WAVE2",
    "RECON-NIGHT-2026-09-20.md": "RECON_NIGHT",
    "REGISTER-2026-09-17-unfinished-work-intakes-models-codespace.md": "REGISTER",
    "REPOMAP-EVALUATION-2026-09-19.md": "REPOMAP_EVALUATION",
    "RESUME-zed-config-2026-09-15.md": "RESUME",
    "REVIEW-lane-v-643-enforcement-debt.md": "REVIEW",
    "SCAN-fpg1-coverage-roster-2026-09-19.md": "SCAN",
    "SPINE-FIRST-STOP-2026-09-19.md": "SPINE_FIRST_STOP",
    "STATE-2026-09-14-waves-x1-x3-and-y.md": "STATE",
    "STATE-OF-THE-HARNESS-2026-09-20.md": "STATE_OF_THE_HARNESS",
    "STATUS.md": "STATUS_BARE",
    "UNOWNED-2026-09-06.md": "UNOWNED",
    "WATCHER-LOG-night-wave2-2026-09-19.md": "WATCHER",
    "WATCHER-night-wave2-2026-09-19.md": "WATCHER",
    "WINDOW-GOALS-2026-09-25-superseded-moved-into-LEDGER.md": "WINDOW_GOALS",
}


@pytest.mark.parametrize("filename,expected_kind", sorted(_LANE_TRANSPORT_STRAYS_SAMPLES.items()))
def test_lane_transport_strays_additions_classify_their_real_observed_filenames(
        t, registry, filename, expected_kind):
    got = t.classify(filename, registry)
    assert got is not None and got.name == expected_kind, f"{filename!r} -> {got}"


def test_no_fixed_lead_in_kinds_classify_their_dated_shape_and_stay_mutually_exclusive(t, registry):
    assert t.classify("2026-09-19-technical-wave3-answerable-lane-contract.md", registry).name \
        == "DATED_SLUG_LANE_CONTRACT"
    assert t.classify("2026-09-05-technical-fleet-readiness.md", registry).name == "DATED_SLUG"
    # the mutual exclusion is textual (negative lookahead), never registry row order (see the
    # registry's own notes on both kinds)
    assert t.classify("2026-09-05-technical-fleet-readiness.md", list(reversed(registry))).name \
        == "DATED_SLUG"


def test_the_widened_digest_pattern_covers_non_markdown_attachments(t, registry):
    for filename in ("DIGEST-cv-build-2026-09-10-after-p1.png",
                     "DIGEST-github-review-2026-09-10-acts.yaml",
                     "DIGEST-WAVE5B-N1-2026-09-25.md"):
        got = t.classify(filename, registry)
        assert got is not None and got.name == "DIGEST", f"{filename!r} -> {got}"


def test_longest_prefix_wins_lane_end_over_the_bare_lane_contract_kind(t, registry):
    assert t.classify("LANE-END-lane-x.md", registry).name == "LANE_END"
    assert t.classify("LANE-a-539-ch8.md", registry).name == "LANE_CONTRACT"


# --- Done-when 1: derived from the code, not hand-copied ------------------------------------------

def test_derivation_finds_nothing_missing_from_the_real_registry(t, registry):
    derived = t.derive_kinds_from_code(_SCRIPTS)
    registered_prefixes = {k.prefix for k in registry}
    missing = derived - registered_prefixes
    assert not missing, (
        f"the code builds {sorted(missing)} on the transport and "
        f"{REGISTRY_PATH.name} has no row for it")


def test_derivation_finds_the_known_kinds_this_lane_read_off_the_code(t):
    """A floor, not a ceiling: these specific prefixes are the ones this lane's own research
    (handback.py, transport_report.py, gen_ledger.py, gen_seat_boot.py, gen_lane_contract.py,
    gen_handoff.py, propose_row_closures.py) found built on the transport. A future refactor
    that stops literally building one of these is fine; a run that finds NONE of them means the
    scan itself broke."""
    derived = t.derive_kinds_from_code(_SCRIPTS)
    expected = {"GO-", "LEDGER-", "LANE-END-", "HANDBACK-REFUSED-", "SESSION-", "SEAT-BOOT-",
               "MERGE-PLAN-", "ESCALATE-", "DECLARE-", "AMEND-", "BATCH-", "LANE-",
               "RATIFICATION-", "STATUS-", "QUESTION-", "ANSWER-", "CLOSURE-LIST-"}
    assert expected <= derived, f"missing from the scan: {sorted(expected - derived)}"


def test_derivation_does_not_pick_up_a_concrete_historical_filename(t, tmp_path):
    """A docstring citing an already-resolved past artifact (no placeholder after the prefix)
    is not a template -- the false positive this lane's own build hit first."""
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "example.py").write_text(
        'to_browser = resolve_transport()\n'
        '# see `to-browser/DIGEST-AUDIT-CROSSCHECK-2026-09-23.md` for the full account\n',
        encoding="utf-8")
    assert t.derive_kinds_from_code(scripts_dir) == set()


def test_derivation_ignores_a_same_shaped_local_receipt_path_with_no_transport_anchor(t, tmp_path):
    """`X() / f"LAUNCH-{slug}.json"` is exactly the (join) shape a real transport write has --
    the thing that tells them apart is a nearby transport-resolving call, not the syntax."""
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "unrelated.py").write_text(
        'def receipts_dir():\n'
        '    return Path("logs/receipts")\n'
        '\n'
        'def launch_path(slug):\n'
        '    return receipts_dir() / f"LAUNCH-{slug.upper()}.json"\n',
        encoding="utf-8")
    assert t.derive_kinds_from_code(scripts_dir) == set()


# --- the write gate --------------------------------------------------------------------------

def test_write_succeeds_for_the_kinds_registered_writer(t, world, registry):
    dest = world["browser"] / "HANDBACK-REFUSED-lane-x.md"
    got = t.write("handback", dest, "line one\n", registry=registry)
    assert got == dest
    assert dest.read_text(encoding="utf-8") == "line one\n"


def test_handback_cannot_write_the_integrators_refused_kind(t, world, registry):
    """Done-when 2's literal case: `REFUSED-<lane>.md` is the INTEGRATOR's own repair-order
    path (D10); `handback` writing it would be exactly the collision D10 exists to prevent."""
    dest = world["browser"] / "REFUSED-lane-x.md"
    with pytest.raises(t.TransportWriteRefused, match="REFUSED"):
        t.write("handback", dest, "x", registry=registry)
    assert not dest.exists()


def test_write_refuses_an_entirely_unregistered_kind(t, world, registry):
    dest = world["browser"] / "ODD-NAME-lane-x.md"
    with pytest.raises(t.TransportWriteRefused, match="no registered kind"):
        t.write("handback", dest, "x", registry=registry)
    assert not dest.exists()


def test_write_is_atomic_and_replaces_rather_than_appends(t, world, registry):
    dest = world["browser"] / "LANE-END-lane-x.md"
    t.write("transport_report", dest, "first\n", registry=registry)
    t.write("transport_report", dest, "second\n", registry=registry)
    assert dest.read_text(encoding="utf-8") == "second\n"


def test_write_refuses_a_registered_kind_sitting_in_the_wrong_folder(t, world, registry):
    """Codex terra HIGH (this lane's own review): `_check` matched `dest.name` alone, so a
    registered writer could recreate the exact wrong-folder failure the registry exists to
    end -- a correctly-NAMED SESSION file written into `to-cc/` instead of `to-browser/`."""
    dest = world["cc"] / "SESSION-lane-x.md"
    with pytest.raises(t.TransportWriteRefused, match="to-browser"):
        t.write("handback", dest, "x", registry=registry)
    assert not dest.exists()


def test_write_refuses_a_lane_contract_kind_sitting_inside_a_subfolder(t, world, registry):
    """LANE_CONTRACT's folder is `root` (the transport root itself, not to-cc/to-browser) --
    a lane contract written into either subfolder is also a wrong-folder refusal."""
    dest = world["cc"] / "LANE-a-539-ch8.md"
    with pytest.raises(t.TransportWriteRefused, match="root"):
        t.write("gen_lane_contract", dest, "x", registry=registry)
    assert not dest.exists()


def test_write_accepts_a_lane_contract_kind_at_the_transport_root(t, world, registry):
    dest = world["root"] / "LANE-a-539-ch8.md"
    # a lane contract now lints at write time (b2-transport-lint): its close-out names the R59
    # proof of read, so the fixture body does too
    body = "close-out: the served model id and a nonce or content hash the reviewer returned\n"
    got = t.write("gen_lane_contract", dest, body, registry=registry)
    assert got.read_text(encoding="utf-8") == body


def test_concurrent_appends_to_the_same_destination_serialize_without_interleaving(t, world, registry):
    """Codex terra HIGH (this lane's own review): the separator-size-check-then-write was not
    one protected step; two threads appending to the same SESSION file must not interleave or
    disagree about whether a separating newline is needed."""
    import threading

    dest = world["browser"] / "SESSION-lane-x.md"
    blocks = [f"block-{i}" for i in range(20)]
    errors: list[BaseException] = []

    def worker(block: str) -> None:
        try:
            t.append("handback", dest, block, registry=registry)
        except BaseException as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(b,)) for b in blocks]
    for th in threads:
        th.start()
    for th in threads:
        th.join(timeout=30)

    assert not errors, errors
    text = dest.read_text(encoding="utf-8")
    # every block landed on its own line, exactly once, never merged with a neighbour mid-word
    # ("block-1" is a substring of "block-10".."block-19", so this compares whole LINES, not
    # substring counts)
    lines = [ln for ln in text.splitlines() if ln.startswith("block-")]
    assert sorted(lines) == sorted(blocks)


def test_append_is_gated_the_same_way_as_write(t, world, registry):
    dest = world["browser"] / "REFUSED-lane-x.md"
    with pytest.raises(t.TransportWriteRefused):
        t.append("handback", dest, "x", registry=registry)
    assert not dest.exists()


def test_append_keeps_prior_content_and_adds_a_separating_newline(t, world, registry):
    dest = world["browser"] / "SESSION-lane-x.md"
    dest.write_text("some narrative the lane wrote by hand\n", encoding="utf-8")
    t.append("handback", dest, "HANDBACK worktree-lane-x @ deadbeef code", registry=registry)
    text = dest.read_text(encoding="utf-8")
    assert "some narrative the lane wrote by hand" in text
    assert "HANDBACK worktree-lane-x @ deadbeef code" in text
    assert text.count("HANDBACK ") == 1


# --- the stray-file report (Done-when 3, report-only) ----------------------------------------

def test_scan_is_clean_over_a_transport_holding_only_registered_kinds_in_their_own_folder(
        t, world, registry):
    (world["cc"] / "GO-batch1.md").write_text("x", encoding="utf-8")
    (world["browser"] / "SESSION-lane-x.md").write_text("x", encoding="utf-8")
    assert t.scan(world["root"], registry) == []


def test_scan_reports_an_unregistered_kind(t, world, registry):
    (world["browser"] / "ODD-NAME.md").write_text("x", encoding="utf-8")
    findings = t.scan(world["root"], registry)
    assert len(findings) == 1
    assert findings[0].path == "to-browser/ODD-NAME.md"
    assert "unregistered" in findings[0].reason


def test_scan_reports_a_registered_kind_sitting_in_the_wrong_folder(t, world, registry):
    """The lane's own Value line: 'a report once landed in the wrong folder.'"""
    (world["cc"] / "HANDBACK-REFUSED-lane-x.md").write_text("x", encoding="utf-8")
    findings = t.scan(world["root"], registry)
    assert len(findings) == 1
    assert findings[0].path == "to-cc/HANDBACK-REFUSED-lane-x.md"
    assert "HANDBACK_REFUSED" in findings[0].reason and "to-browser" in findings[0].reason


def test_scan_never_writes_moves_or_deletes_anything(t, world, registry):
    (world["browser"] / "ODD-NAME.md").write_text("x", encoding="utf-8")
    before = sorted(p.name for p in world["browser"].iterdir())
    t.scan(world["root"], registry)
    after = sorted(p.name for p in world["browser"].iterdir())
    assert before == after


# --- lane-transport-strays Done-when 1: an exit-code-gated check, pinned by a fixture ----------

def test_cmd_strays_exits_zero_on_a_clean_transport(t, world):
    (world["cc"] / "GO-batch1.md").write_text("x", encoding="utf-8")
    rc = t.main(["strays", "--transport-root", str(world["root"])])
    assert rc == 0


def test_cmd_strays_exits_nonzero_on_a_fixture_with_exactly_one_unclassified_stray(t, world):
    (world["browser"] / "ODD-NAME-not-in-the-registry.md").write_text("x", encoding="utf-8")
    rc = t.main(["strays", "--transport-root", str(world["root"])])
    assert rc == 1


def test_cmd_strays_unclassified_count_excludes_a_misfoldered_but_known_kind(t, world):
    """Done-when 1's literal wording is '0 UNCLASSIFIED' -- a registered kind sitting in the
    wrong folder is a real, reported finding (still nonzero exit, still worth fixing), but it
    is not what this exit code is keyed to; the JSON breaks the two counts out so a caller can
    tell "unknown kind" apart from "known kind, wrong home"."""
    (world["cc"] / "HANDBACK-REFUSED-lane-x.md").write_text("x", encoding="utf-8")
    rc = t.main(["strays", "--transport-root", str(world["root"])])
    assert rc == 1  # still a nonzero exit: SOME stray exists
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        t.main(["strays", "--transport-root", str(world["root"])])
    import json
    payload = json.loads(buf.getvalue())
    assert payload["unclassified_count"] == 0
    assert payload["misfoldered_count"] == 1


def test_the_windows_append_flake_is_quarantined_with_its_cause_and_rates_not_skipped():
    """foundation-8 item 2. The cause lives in `scripts/transport.py`
    (`_DestinationLock.__enter__` catches only FileExistsError; Windows answers a lock file that
    is mid-delete with PermissionError) -- not a test defect and not this lane's to edit -- so the
    test is QUARANTINED in the registry with its task, owner, expiry and measured rates, and keeps
    RUNNING: no skip, skipif or xfail."""
    import datetime
    import json
    import re

    node_id = ("tests/test_transport.py::"
               "test_concurrent_appends_to_the_same_destination_serialize_without_interleaving")
    registry = json.loads((_REPO / "logs" / "KNOWN-REDS-REGISTRY.json").read_text(encoding="utf-8"))
    entry = registry["members_by_os"].get("windows-latest", {}).get(node_id)
    assert entry is not None, f"{node_id} is not quarantined on windows-latest"
    assert entry.get("attribution") == "flaky"
    row = re.fullmatch(r"\[#(\d+)\]", entry.get("task", ""))
    row_files = list(_REPO.glob(f"tasks/{row.group(1)}-*.md")) if row else []
    assert row_files, f"task {entry.get('task')!r} resolves to no tasks/ row"
    assert "status: open" in row_files[0].read_text(encoding="utf-8")
    assert entry.get("owner")
    assert datetime.date.fromisoformat(entry["expiry"]) <= datetime.date(2026, 10, 19)
    reason = entry.get("reason", "")
    assert "PermissionError" in reason and "scripts/transport.py" in reason
    assert len(re.findall(r"\b\d+/\d+\b", reason)) >= 2, "no measured control-run rates"
    marks = {m.name for m in getattr(
        test_concurrent_appends_to_the_same_destination_serialize_without_interleaving,
        "pytestmark", [])}
    assert not marks & {"skip", "skipif", "xfail"}


# =====================================================================================================
# lane b2w2-transport-index ([#1439], batch B2-W3): the generated INDEX, the attribution rule, the
# seat-ID map, the landing inventory, the janitor and the INDEX trigger.
#
# Every test drives a synthetic transport in `tmp_path`; nothing here touches the real drive. The
# oracles below are written from the contract, the seat's AMENDs and the lane's plan (revision 7),
# in this file, and are NOT imported from `transport`: a test that borrowed the module's own
# predicate could not show the module agrees with the AMEND's words.
# =====================================================================================================

STAMP = "2026-10-10T12:00:00Z"
TA44 = "Tech-Architect-44 (R91)"
TA43 = "Tech-Architect-43 (R91)"
SEAT_43 = {"seat": "Tech-Architect-43", "session": "2026-10-02-dev-knowledge-architect",
           "provenance": "to-cc/AMEND-seed-43.md", "stated_in": 1}
SEAT_44 = {"seat": "Tech-Architect-44", "session": "2026-10-08-dev-knowledge-architect",
           "provenance": "to-cc/AMEND-seed-44.md", "stated_in": 1}
SEATS = [SEAT_43, SEAT_44]


def _put(root: Path, rel: str, text: str = "x\n") -> Path:
    """Write `text` (LF bytes) at `rel` under `root`; `rel` is `to-cc/NAME`, `to-browser/NAME` or a bare
    NAME for the transport root, the convention `scan()` reports paths in."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def _head(*, by=None, date=None, summary=None, supersedes=None, heading=None, body=("dev-knowledge",)) -> str:
    lines = []
    for key, value in (("by", by), ("date", date), ("summary", summary), ("supersedes", supersedes)):
        if value is not None:
            lines.append(f"{key}: {value}")
    lines.append("")
    if heading:
        lines.append(f"# {heading}")
    lines.extend(body)
    return "\n".join(lines) + "\n"


def _seatmap_digest(seats) -> str:
    text = "\n".join(sorted(f"{s['seat']}={s['session']}" for s in seats))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _seat_file(tmp_path: Path, seats=SEATS, inventory=None) -> Path:
    import transport
    path = tmp_path / "seat-ids.yaml"
    transport.write_seat_ids(path, seats=list(seats), inventory=dict(inventory or {}))
    return path


def _index(t, root: Path, seats=SEATS, stamp: str = STAMP, trigger: str = "index") -> str:
    return t.build_index(root, seats=list(seats), generated_at=stamp, trigger=trigger)


def _entries(t, text: str) -> list[dict]:
    return t.parse_index(text)["entries"]


# --- the registry row ---------------------------------------------------------------------------------

def test_the_index_kind_is_registered_and_the_row_avoids_the_three_silent_rule_words(t, registry):
    kind = t.classify("INDEX.md", registry)
    assert kind is not None and kind.name == "INDEX"
    assert kind.folder == "to-browser" and kind.writers == ("transport",)
    assert kind.repo_scope == "hub" and kind.decision is False
    raw = REGISTRY_PATH.read_text(encoding="utf-8")
    row = raw.split("kind: INDEX", 1)[1].split("\n  - kind:", 1)[0].lower()
    for word in ("must", "shall", "never"):
        assert not re.search(rf"\b{word}\b", row), f"the INDEX row carries the word {word!r}"
    assert t.classify("INDEX.md.bak", registry) is None


# --- Done 1: the generated INDEX ------------------------------------------------------------------------

def _snapshot_world(world) -> None:
    root = world["root"]
    _put(root, "to-browser/DIGEST-alpha-2026-10-08.md",
         _head(by=TA44, date="2026-10-08", summary="Alpha digest"))
    _put(root, "to-browser/DIGEST-beta-2026-10-09.md",
         _head(by=TA44, date="2026-10-09", summary="Beta digest"))
    _put(root, "to-browser/DIGEST-delta-2026-10-09.md",
         _head(by=TA44, date="2026-10-09", summary="Delta digest"))
    _put(root, "to-browser/DIGEST-gamma-2026-10-09.md",
         _head(by=TA43, date="2026-10-09", summary="Gamma digest"))
    _put(root, "to-browser/DIGEST-nosigner-2026-10-07.md", _head(heading="Unsigned digest"))
    _put(root, "to-browser/DIGEST-undated.md", _head(by=TA44))
    _put(root, "to-browser/DIGEST-old-2026-10-01-superseded.md",
         _head(by=TA44, date="2026-10-01", summary="Old digest"))
    _put(root, "to-browser/DIGEST-nosignal-2026-10-03.md", _head(body=()))
    _put(root, "to-cc/PLAN-x-v1.md", _head(by=TA44, date="2026-10-05", summary="Plan one"))
    _put(root, "to-cc/PLAN-x-v2.md",
         _head(by=TA44, date="2026-10-06", summary="Plan two", supersedes="PLAN-x-v1.md"))
    _put(root, "to-cc/notes.txt", "a stray\n")
    _put(root, "to-browser/.hidden.tmp", "dotfile\n")
    _put(root, "to-browser/desktop.ini", "[.ShellClassInfo]\n")


def _golden_snapshot() -> str:
    row = "- {path} | {kind} | {subject} | {date} | by: {by}".format
    return "\n".join([
        "by: transport.py index (generated)",
        "date: 2026-10-10",
        "summary: Generated index of the current transport files, by kind and writer, newest first.",
        "regenerated: 2026-10-10T12:00:00Z",
        "trigger: index",
        f"inputs: veto=- seatmap={_seatmap_digest(SEATS)}",
        "",
        "# INDEX — current files on the transport",
        "",
        "Generated by `transport.py index --write`. Regenerate it; do not edit it by hand.",
        "",
        "repository: dev-knowledge",
        "live: 12",
        "classified: 11",
        "listed: 10",
        "current: 8",
        "superseded: 2",
        "UNATTRIBUTED: 1",
        "unclassified: 1",
        "UNATTRIBUTED by kind: DIGEST=1",
        "",
        "## Current",
        "",
        "### DIGEST (6)",
        "",
        "#### Tech-Architect-43 (1)",
        "",
        row(path="to-browser/DIGEST-gamma-2026-10-09.md", kind="DIGEST", subject="Gamma digest",
            date="2026-10-09", by=TA43),
        "",
        "#### Tech-Architect-44 (4)",
        "",
        row(path="to-browser/DIGEST-beta-2026-10-09.md", kind="DIGEST", subject="Beta digest",
            date="2026-10-09", by=TA44),
        row(path="to-browser/DIGEST-delta-2026-10-09.md", kind="DIGEST", subject="Delta digest",
            date="2026-10-09", by=TA44),
        row(path="to-browser/DIGEST-alpha-2026-10-08.md", kind="DIGEST", subject="Alpha digest",
            date="2026-10-08", by=TA44),
        row(path="to-browser/DIGEST-undated.md", kind="DIGEST", subject="(no subject)",
            date="undated", by=TA44),
        "",
        "#### UNKNOWN (1)",
        "",
        row(path="to-browser/DIGEST-nosigner-2026-10-07.md", kind="DIGEST", subject="Unsigned digest",
            date="2026-10-07", by="UNKNOWN"),
        "",
        "### INDEX (1)",
        "",
        "#### transport.py index (1)",
        "",
        row(path="to-browser/INDEX.md", kind="INDEX",
            subject="Generated index of the current transport files, by kind and writer, newest first.",
            date="2026-10-10", by="transport.py index (generated)"),
        "",
        "### PLAN (1)",
        "",
        "#### Tech-Architect-44 (1)",
        "",
        row(path="to-cc/PLAN-x-v2.md", kind="PLAN", subject="Plan two", date="2026-10-06", by=TA44),
        "",
        "## Superseded",
        "",
        "### DIGEST (1)",
        "",
        row(path="to-browser/DIGEST-old-2026-10-01-superseded.md", kind="DIGEST", subject="Old digest",
            date="2026-10-01", by=TA44),
        "",
        "### PLAN (1)",
        "",
        row(path="to-cc/PLAN-x-v1.md", kind="PLAN", subject="Plan one", date="2026-10-05", by=TA44),
        "",
        "## UNATTRIBUTED",
        "",
        "### DIGEST (1)",
        "",
        row(path="to-browser/DIGEST-nosignal-2026-10-03.md", kind="DIGEST", subject="(no subject)",
            date="2026-10-03", by="UNKNOWN"),
        "",
        "## Supersedes edges",
        "",
        "- to-cc/PLAN-x-v2.md supersedes PLAN-x-v1.md",
        "",
    ])


def test_index_snapshot_matches_the_stored_text(t, world):
    """Done 1: grouped by kind then writer, newest first, ties by path, `by: UNKNOWN`, `undated`,
    a superseded section, the UNATTRIBUTED section and its count by kind, the INDEX's own row."""
    _snapshot_world(world)
    assert _index(t, world["root"]) == _golden_snapshot()


def test_index_is_deterministic_and_independent_of_listing_order(t, world, monkeypatch):
    _snapshot_world(world)
    first = _index(t, world["root"])
    orig = t.live_files
    monkeypatch.setattr(t, "live_files", lambda root: list(reversed(orig(root))))
    assert _index(t, world["root"]) == first


def test_index_says_the_rule_for_current_and_the_sort_key(t, world):
    """No mtime anywhere: a file whose mtime is changed lands in the same place."""
    _snapshot_world(world)
    before = _index(t, world["root"])
    path = world["root"] / "to-browser" / "DIGEST-undated.md"
    os.utime(path, (978307200, 978307200))   # 2001-01-01
    assert _index(t, world["root"]) == before


def _oracle_names(root: Path, registry, t) -> dict:
    """The classified live files, split into listed / UNATTRIBUTED by an independent walk."""
    live = []
    for folder, sub in (("to-cc", root / "to-cc"), ("to-browser", root / "to-browser"), ("root", root)):
        for p in sorted(sub.iterdir()):
            if p.is_file() and not p.name.startswith(".") and p.name != "desktop.ini" and p.name != "INDEX.md":
                live.append((folder, p))
    ledger_names = set()
    for folder, p in live:
        m = re.match(r"LEDGER-(.+)\.md$", p.name)
        if m:
            tok = m.group(1).lower().replace("_", "-")
            while True:
                new = re.sub(r"(-\d{4}-\d{2}-\d{2}|-superseded|-v\d+)$", "", tok)
                if new == tok:
                    break
                tok = new
            if tok != "dev-knowledge":
                ledger_names.add(tok)
    listed, unattributed, strays = [], [], 0
    for folder, p in live:
        kind = t.classify(p.name, registry)
        if kind is None:
            strays += 1
            continue
        rel = p.name if folder == "root" else f"{folder}/{p.name}"
        text = p.read_text(encoding="utf-8", errors="replace") if p.suffix == ".md" else ""
        window = "\n".join(text.splitlines()[:30]).lower().replace("_", "-")
        lname = p.name.lower().replace("_", "-")
        vetoed = any(re.search(rf"(?<![a-z0-9]){re.escape(tok)}(?![a-z0-9])", lname + "\n" + window)
                     for tok in ledger_names)
        stem = re.sub(r"\.[A-Za-z0-9]{1,6}$", "", p.name).lower()
        vetoed = vetoed or "cv" in stem.split("-")
        cited = [c for c in re.findall(r"[A-Za-z0-9._-]+\.md", "\n".join(text.splitlines()[:30]))
                 if c != p.name and (t.classify(c, registry) is not None)
                 and t.classify(c, registry).repo_scope == "hub"]
        signal = bool(re.search(r"\bdev-knowledge\b", "\n".join(text.splitlines()[:30]))
                      or re.search(r"Tech-Architect-\d+", "\n".join(text.splitlines()[:30]))
                      or cited)
        (listed if (signal and not vetoed) else unattributed).append(rel)
    return {"listed": sorted(listed), "unattributed": sorted(unattributed), "strays": strays}


def test_index_entries_equal_the_classified_live_files_attributable_to_this_repo(t, world, registry):
    """P-L3-1: entries equal, in number and identity, an oracle that walks the fixture on its own; the
    INDEX's own row is one of them; a file not attributable is UNATTRIBUTED, not dropped."""
    root = world["root"]
    _snapshot_world(world)
    _put(root, "to-browser/LEDGER-dev-knowledge.md", _head(by="gen_ledger.py", date="2026-10-09"))
    _put(root, "to-browser/LEDGER-acme-ops.md", _head(by="gen_ledger.py", date="2026-10-09"))
    _put(root, "to-browser/DIGEST-mentions-acme-ops-2026-10-09.md", _head(by=TA44, body=("acme-ops notes",)))
    _put(root, "to-cc/CONTRACT-cv-build-2026-09-10.md", _head(by=TA44))
    _put(root, "to-cc/GO-demo-2026-10-09.md", _head(by=TA44, date="2026-10-09"))
    _put(root, "to-cc/GO-bare-2026-10-09.md", "just text\n")
    _put(root, "LANE-demo.md", _head(by=TA44, date="2026-10-09"))
    _put(root, "to-cc/LANE-demo.CLAIMED-ab12cd", "claim\n")
    text = _index(t, root)
    entries = _entries(t, text)
    oracle = _oracle_names(root, registry, t)
    got_listed = sorted(e["path"] for e in entries if e["status"] in ("current", "superseded")
                        and e["path"] != "to-browser/INDEX.md")
    got_unattr = sorted(e["path"] for e in entries if e["status"] == "unattributed")
    assert got_listed == oracle["listed"]
    assert got_unattr == oracle["unattributed"]
    assert any(e["path"] == "to-browser/INDEX.md" and e["kind"] == "INDEX" for e in entries)
    assert "to-cc/CONTRACT-cv-build-2026-09-10.md" in got_unattr
    assert "to-browser/LEDGER-acme-ops.md" in got_unattr            # the derived veto: its own name
    assert "to-browser/DIGEST-mentions-acme-ops-2026-10-09.md" in got_unattr
    assert "to-cc/GO-bare-2026-10-09.md" in got_unattr               # a hub kind earns nothing by scope
    assert "LANE-demo.md" in got_listed
    assert "to-cc/LANE-demo.CLAIMED-ab12cd" in got_unattr            # a claim marker has no head signal
    assert t.parse_index(text)["header"]["unclassified"] == str(oracle["strays"])


def test_every_entry_carries_kind_subject_date_and_by(t, world, registry):
    """P-L3-1 (grok review of revision 4): the four fields on every listed and UNATTRIBUTED entry,
    each equal to the oracle's value, never empty."""
    _snapshot_world(world)
    entries = _entries(t, _index(t, world["root"]))
    assert len(entries) == 11                              # ten listed (the INDEX's own row among them) + one
    by_path = {e["path"]: e for e in entries}
    for e in entries:
        assert e["kind"] and e["subject"] and e["date"] and e["by"], e
        assert t.classify(Path(e["path"]).name, registry).name == e["kind"]
    assert by_path["to-browser/DIGEST-alpha-2026-10-08.md"]["subject"] == "Alpha digest"
    assert by_path["to-browser/DIGEST-alpha-2026-10-08.md"]["date"] == "2026-10-08"
    assert by_path["to-browser/DIGEST-alpha-2026-10-08.md"]["by"] == TA44
    assert by_path["to-browser/DIGEST-nosigner-2026-10-07.md"]["subject"] == "Unsigned digest"   # heading
    assert by_path["to-browser/DIGEST-nosigner-2026-10-07.md"]["date"] == "2026-10-07"            # name date
    assert by_path["to-browser/DIGEST-nosigner-2026-10-07.md"]["by"] == "UNKNOWN"
    assert by_path["to-browser/DIGEST-undated.md"]["subject"] == "(no subject)"
    assert by_path["to-browser/DIGEST-undated.md"]["date"] == "undated"
    assert by_path["to-browser/DIGEST-nosignal-2026-10-03.md"]["by"] == "UNKNOWN"
    assert by_path["to-browser/DIGEST-nosignal-2026-10-03.md"]["status"] == "unattributed"


def test_a_long_or_pipe_bearing_subject_stays_one_row(t, world):
    _put(world["root"], "to-browser/DIGEST-pipes-2026-10-09.md",
         _head(by=TA44, date="2026-10-09", summary="a | b | " + "x" * 200))
    entries = {e["path"]: e for e in _entries(t, _index(t, world["root"]))}
    e = entries["to-browser/DIGEST-pipes-2026-10-09.md"]
    assert len(e["subject"]) <= 100 and "|" not in e["subject"]


def test_index_check_cli_exits_1_with_no_index_and_0_after_the_index_is_written(t, world, tmp_path, capsys):
    _snapshot_world(world)
    seat_file = _seat_file(tmp_path)
    args = ["--transport-root", str(world["root"]), "--seat-ids", str(seat_file)]
    assert t.main(["index", "--check", *args]) == 1                      # no INDEX
    assert not (world["browser"] / "INDEX.md").exists()                  # --check writes nothing
    assert t.main(["index", "--write", "--generated-at", STAMP, *args]) == 0
    written = (world["browser"] / "INDEX.md").read_text(encoding="utf-8")
    assert written == _golden_snapshot()
    assert t.main(["index", "--check", *args]) == 0
    _put(world["root"], "to-browser/DIGEST-late-2026-10-10.md", _head(by=TA44, date="2026-10-10"))
    assert t.main(["index", "--check", *args]) == 1                      # a new file makes it stale
    capsys.readouterr()
    assert t.main(["index", *args]) == 0                                  # no flag: prints, writes nothing
    out = capsys.readouterr().out
    assert "UNATTRIBUTED" in out and (world["browser"] / "INDEX.md").read_text(encoding="utf-8") == written


def test_an_empty_seat_map_fails_the_index_run(t, world, tmp_path):
    """Done 4: an empty map cannot pass; the INDEX run refuses and writes nothing."""
    _snapshot_world(world)
    with pytest.raises(t.EmptySeatMap):
        t.build_index(world["root"], seats=[], generated_at=STAMP, trigger="index")
    empty = _seat_file(tmp_path, seats=[])
    rc = t.main(["index", "--write", "--transport-root", str(world["root"]), "--seat-ids", str(empty)])
    assert rc == 2 and not (world["browser"] / "INDEX.md").exists()


# --- Done 1 / S-10: the attribution rule, oracle written from the AMEND's own words -----------------------

SEATS_OTHER = [{"seat": "Tech-Architect-12", "session": "2026-09-01-other-architect",
                "provenance": "to-cc/AMEND-seed-12.md", "stated_in": 1}]


def _attr_case(world, name, text, extra=()):
    """The attribution status of every file on a fixture transport holding `to-browser/<name>`."""
    root = world["root"]
    for rel, body in extra:
        _put(root, rel, body)
    _put(root, f"to-browser/{name}", text)
    mod = _mod("transport")
    return {e["path"]: e["status"] for e in _entries(mod, _index(mod, root, seats=SEATS_OTHER))}


def _lines(n_before: int, line: str) -> str:
    """A head with `line` on line n_before + 1 and filler everywhere else."""
    return "\n".join(["filler"] * n_before + [line]) + "\n"


@pytest.mark.parametrize("name,text,expected", [
    # accepted signals (S-10 C3): the repository token, word-bounded, in the first 30 lines
    ("DIGEST-tok-line-1.md", "dev-knowledge notes\n", "listed"),
    ("DIGEST-tok-line-30.md", _lines(29, "see dev-knowledge"), "listed"),
    ("DIGEST-tok-line-31.md", _lines(30, "see dev-knowledge"), "unattributed"),
    ("DIGEST-tok-substring.md", "mydev-knowledgebase\n", "unattributed"),
    # a Tech-Architect-NN id, any, or a session slug present in the seat map
    ("DIGEST-ta-id.md", "by: Tech-Architect-77 (R91)\n", "listed"),
    ("DIGEST-seat-slug.md", "from: 2026-09-01-other-architect\n", "listed"),
    ("DIGEST-unmapped-slug.md", "from: 2026-09-02-unmapped-architect\n", "unattributed"),
    # a cited transport file name that classifies as a hub-scope kind
    ("DIGEST-cites-hub.md", "see GO-demo-2026-10-09.md for the order\n", "listed"),
    ("DIGEST-cites-any.md", "see DIGEST-other-2026-10-09.md\n", "unattributed"),
    # rejected by the AMEND: a name-only signal, and a path that exists under the repository root
    ("DIGEST-dev-knowledge-name-only.md", "plain text\n", "unattributed"),
    ("DIGEST-cites-a-repo-path.md", "see scripts/transport.py and ecosystem/transport-registry.yaml\n", "unattributed"),
    # a hub-scope kind with no head signal earns nothing by its scope
    ("SIGNAL-hub-bare.md", "plain text\n", "unattributed"),
])
def test_attribution_follows_the_amend_table(t, world, name, text, expected):
    status = _attr_case(world, name, text)
    got = status[f"to-browser/{name}"]
    assert (got != "unattributed") == (expected == "listed"), (name, got)


def test_the_derived_veto_removes_a_file_that_carries_an_accepted_signal(t, world):
    status = _attr_case(
        world, "DIGEST-about-acme-ops-2026-10-09.md", "dev-knowledge and Tech-Architect-44\n",
        extra=[("to-browser/LEDGER-acme-ops.md", _head(by="gen_ledger.py")),
               ("to-browser/LEDGER-acme-ops-v1-superseded-2026-09-10.md", _head(by="gen_ledger.py")),
               ("to-browser/LEDGER-Acme_Ops2.md", _head(by="gen_ledger.py"))])
    assert status["to-browser/DIGEST-about-acme-ops-2026-10-09.md"] == "unattributed"
    assert status["to-browser/LEDGER-acme-ops.md"] == "unattributed"


def test_a_ledger_of_this_repo_does_not_veto(t, world):
    status = _attr_case(world, "DIGEST-fine-2026-10-09.md", "dev-knowledge\n",
                        extra=[("to-browser/LEDGER-dev-knowledge.md", _head(by="gen_ledger.py"))])
    assert status["to-browser/DIGEST-fine-2026-10-09.md"] != "unattributed"


def test_known_limit_witness_a_foreign_contract_naming_this_repo_is_attributed(t, world):
    """Pinned as documented behaviour (D5's stated limit, S-17): no head signal tells a foreign file that
    names this repository from a dev-knowledge file; the janitor's exposure is removed by the no-live-apply
    ruling and the seat's review of the dry-run list, not by this heuristic."""
    root = world["root"]
    _put(root, "to-cc/CONTRACT-foreign-2026-09-10.md", "committed in dev-knowledge\nsome other workstream\n")
    status = {e["path"]: e["status"] for e in _entries(t, _index(t, root))}
    assert status["to-cc/CONTRACT-foreign-2026-09-10.md"] != "unattributed"


# --- Done 1 / S-40: the `cv` name segment ---------------------------------------------------------------

#: The 14 files `SESSION-b2w2-transport-index.md` :486 lists as naming the CV repo, by their real names.
CV_FILES = (
    "to-browser/LEDGER-robert-dwornik-cv.md",
    "to-browser/LEDGER-robert-dwornik-cv-v1-superseded-2026-09-10.md",
    "to-browser/LEDGER-robert-dwornik-cv-v2-superseded-2026-09-10.md",
    "to-browser/LEDGER-robert-dwornik-cv-v3-superseded-2026-09-10.md",
    "to-browser/DECISION-SHEET-cv-f2-2026-09-10.md",
    "to-cc/CONTRACT-cv-build-2026-09-10.md",
    "to-cc/CONTRACT-cv-review-2026-09-10.md",
    "to-cc/CONTRACT-cv-copy-apply-2026-09-10.md",
    "to-cc/CONTRACT-cv-copy-fix-2026-09-10.md",
    "to-cc/CONTRACT-cv-rewrite-v4-2026-09-10.md",
    "to-cc/CONTRACT-cv-v5-2026-09-10.md",
    "to-cc/CONTRACT-cv-v8-build-2026-09-10.md",
    "to-cc/CONTRACT-cv-v9-layout-2026-09-10.md",
    "to-cc/CONTRACT-cv-v10-2026-09-10.md",
)
_CV_HEAD = _head(by=TA44, date="2026-09-10", body=("dev-knowledge", "see GO-demo-2026-10-09.md"))


def test_the_cv_witness_is_14_files(t):
    assert len(CV_FILES) == 14 and len(set(CV_FILES)) == 14


@pytest.mark.parametrize("rel", CV_FILES)
def test_cv_segment_veto_each_of_the_14_files_reads_unattributed(t, world, rel):
    """S-40 (the lane's fourth named fix): every one of the 14 files carries accepted signals in its head
    (the repository token, a Tech-Architect id, a cited hub-kind file name) and still reads UNATTRIBUTED."""
    for other in CV_FILES:
        _put(world["root"], other, _CV_HEAD)
    status = {e["path"]: e["status"] for e in _entries(t, _index(t, world["root"]))}
    assert status[rel] == "unattributed"


@pytest.mark.parametrize("rel", [r for r in CV_FILES if not r.startswith("to-browser/LEDGER")])
def test_cv_segment_alone_vetoes_with_no_ledger_on_the_transport(t, world, rel):
    """The segment is its own veto: with no LEDGER of another workstream (the derived part empty) the
    DECISION-SHEET and the nine CONTRACT-cv-* are still UNATTRIBUTED."""
    for other in CV_FILES:
        if not other.startswith("to-browser/LEDGER"):
            _put(world["root"], other, _CV_HEAD)
    status = {e["path"]: e["status"] for e in _entries(t, _index(t, world["root"]))}
    assert status[rel] == "unattributed"


def test_a_cv_vetoed_file_is_never_a_janitor_candidate(t, world):
    root = world["root"]
    for rel in CV_FILES:
        _put(root, rel, _CV_HEAD)
    _put(root, "to-cc/CONTRACT-cv-old-v1-superseded.md", _CV_HEAD)
    _put(root, "to-browser/DIGEST-cv-old-2026-09-10-superseded.md", _CV_HEAD)
    plan = t.janitor_plan(root, seats=SEATS)
    assert plan["moves"] == []
    reasons = {s["path"]: s["reason"] for s in plan["skipped"]}
    assert reasons["to-cc/CONTRACT-cv-old-v1-superseded.md"] == "UNATTRIBUTED"
    assert reasons["to-browser/DIGEST-cv-old-2026-09-10-superseded.md"] == "UNATTRIBUTED"


@pytest.mark.parametrize("name,expected", [
    ("CONTRACT-cv-build-2026-09-10.md", True), ("DRAFT-cv.md", True), ("cv-first.md", True),
    ("LEDGER-robert-dwornik-cv.md", True), ("DIGEST-CV-notes.md", True),
    ("DIGEST-recv-2026-09-10.md", False), ("DIGEST-cvs-notes-2026-09-10.md", False),
    ("DIGEST-devcv-2026-09-10.md", False), ("DIGEST-cv_notes.md", False), ("DIGEST-x.cv", False),
])
def test_the_cv_segment_matches_a_whole_hyphen_delimited_segment_only(t, name, expected):
    assert t.name_has_cv_segment(name) is expected


def test_whole_segment_negatives_stay_attributed_and_a_head_mention_does_not_veto(t, world):
    root = world["root"]
    for name in ("DIGEST-recv-2026-09-10.md", "DIGEST-cvs-notes-2026-09-10.md", "DIGEST-devcv-2026-09-10.md"):
        _put(root, f"to-browser/{name}", _head(by=TA44))
    _put(root, "to-browser/DIGEST-headcv-2026-09-10.md", _head(by=TA44, body=("my cv notes", "dev-knowledge")))
    status = {e["path"]: e["status"] for e in _entries(t, _index(t, root))}
    for name in ("DIGEST-recv-2026-09-10.md", "DIGEST-cvs-notes-2026-09-10.md",
                 "DIGEST-devcv-2026-09-10.md", "DIGEST-headcv-2026-09-10.md"):
        assert status[f"to-browser/{name}"] != "unattributed", name


# --- Done 4: the seat-ID map -------------------------------------------------------------------------------

def _seat_world(world) -> None:
    root = world["root"]
    _put(root, "to-cc/AMEND-seat-a.md",       # form 1: two keys, the seat on `by:`, the session on `from:`
         "carried-by: OPEN\nfrom: 2026-10-08-dev-knowledge-architect (Layer-1 browser seat, SEQ 1)\n"
         "by: Tech-Architect-44 (R91)\n\n# A\n")
    _put(root, "to-cc/AMEND-seat-b.md",       # form 2: one line, the session inside the seat's parentheses
         "carried-by: OPEN\nfrom: Tech-Architect-43 (2026-10-02-dev-knowledge-architect, SEQ 1)\n\n# B\n")
    _put(root, "to-browser/DIGEST-seat-c.md",  # a distinct third pair, form 1
         "from: 2026-09-20-ops-architect\nby: Tech-Architect-41 (R91)\n\n# C\n")
    _put(root, "to-browser/DIGEST-seat-a2.md",  # the first pair stated again by another file
         "from: 2026-10-08-dev-knowledge-architect\nby: Tech-Architect-44 (R91)\n\n# A2\n")
    _put(root, "to-browser/DIGEST-only-seat.md", "by: Tech-Architect-45 (R91)\n\n# only the seat side\n")
    _put(root, "to-browser/DIGEST-only-slug.md", "from: 2026-10-05-lonely-architect\n\n# only the session side\n")


def test_seat_ids_hold_exactly_the_three_stated_pairs_with_provenance(t, world):
    _seat_world(world)
    got = t.build_seat_map(world["root"])
    pairs = {(s["seat"], s["session"]): s for s in got["seats"]}
    assert set(pairs) == {("Tech-Architect-44", "2026-10-08-dev-knowledge-architect"),
                          ("Tech-Architect-43", "2026-10-02-dev-knowledge-architect"),
                          ("Tech-Architect-41", "2026-09-20-ops-architect")}
    assert len(got["seats"]) == 3                                   # neither one-sided file is a pair
    assert pairs[("Tech-Architect-44", "2026-10-08-dev-knowledge-architect")]["provenance"] == "to-cc/AMEND-seat-a.md"
    assert pairs[("Tech-Architect-44", "2026-10-08-dev-knowledge-architect")]["stated_in"] == 2
    assert pairs[("Tech-Architect-43", "2026-10-02-dev-knowledge-architect")]["provenance"] == "to-cc/AMEND-seat-b.md"
    assert pairs[("Tech-Architect-41", "2026-09-20-ops-architect")]["provenance"] == "to-browser/DIGEST-seat-c.md"
    assert got["conflicts"] == []


def test_seat_ids_are_byte_identical_on_regeneration_and_under_a_reversed_listing(t, world, monkeypatch):
    _seat_world(world)
    one = t.render_seat_ids(t.build_seat_map(world["root"])["seats"], {})
    assert t.render_seat_ids(t.build_seat_map(world["root"])["seats"], {}) == one
    orig = t.live_files
    monkeypatch.setattr(t, "live_files", lambda root: list(reversed(orig(root))))
    assert t.render_seat_ids(t.build_seat_map(world["root"])["seats"], {}) == one
    assert "generated" in one.lower()


def test_a_conflicting_pair_is_reported_and_excluded_and_an_ambiguous_head_is_skipped(t, world):
    root = world["root"]
    _put(root, "to-cc/AMEND-c1.md", "from: 2026-10-01-one-architect\nby: Tech-Architect-50 (R91)\n\n# 1\n")
    _put(root, "to-cc/AMEND-c2.md", "from: 2026-10-02-two-architect\nby: Tech-Architect-50 (R91)\n\n# 2\n")
    _put(root, "to-cc/AMEND-two-seats.md",
         "from: Tech-Architect-60 (2026-10-03-three-architect)\nby: Tech-Architect-61 (R91)\n\n# two ids\n")
    got = t.build_seat_map(root)
    assert got["seats"] == []
    assert [c["seat"] for c in got["conflicts"]] == ["Tech-Architect-50"]


def test_an_empty_transport_gives_a_map_the_check_refuses(t, world, tmp_path):
    seat_file = tmp_path / "seat-ids.yaml"
    assert t.build_seat_map(world["root"])["seats"] == []
    rc = t.main(["seat-ids", "--check", "--transport-root", str(world["root"]), "--seat-ids", str(seat_file)])
    assert rc == 1


def test_seat_ids_write_then_check_round_trip_and_keep_the_inventory_section(t, world, tmp_path):
    _seat_world(world)
    seat_file = tmp_path / "seat-ids.yaml"
    t.write_seat_ids(seat_file, inventory={"to-cc/A.md": "ab" * 32})
    args = ["--transport-root", str(world["root"]), "--seat-ids", str(seat_file)]
    assert t.main(["seat-ids", "--write", *args]) == 0
    seats, inventory = t.load_seat_ids(seat_file)
    assert len(seats) == 3 and inventory == {"to-cc/A.md": "ab" * 32}      # only its own key was rewritten
    assert t.main(["seat-ids", "--check", *args]) == 0
    _put(world["root"], "to-cc/AMEND-seat-new.md", "from: 2026-10-09-new-architect\nby: Tech-Architect-46 (R91)\n")
    assert t.main(["seat-ids", "--check", *args]) == 1


def test_a_file_whose_by_names_only_the_session_slug_is_grouped_under_its_seat(t, world):
    root = world["root"]
    _put(root, "to-browser/DIGEST-slug-writer-2026-10-09.md",
         _head(by="2026-10-08-dev-knowledge-architect (Layer-1 browser seat)", date="2026-10-09"))
    text = _index(t, root)
    block = text.split("#### Tech-Architect-44", 1)[1].split("\n####", 1)[0]
    assert "DIGEST-slug-writer-2026-10-09.md" in block
    assert "by: 2026-10-08-dev-knowledge-architect (Layer-1 browser seat)" in block   # shown as written


def test_the_shipped_seat_ids_file_holds_stated_pairs_with_provenance_and_says_it_is_generated():
    path = _REPO / "ecosystem" / "seat-ids.yaml"
    assert path.is_file(), "ecosystem/seat-ids.yaml is generated and committed by the lane (S6)"
    import yaml
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert len(data["seats"]) >= 2
    for s in data["seats"]:
        assert re.fullmatch(r"Tech-Architect-\d+", s["seat"]) and s["session"] and s["provenance"]
    head = "\n".join(path.read_text(encoding="utf-8").splitlines()[:6]).lower()
    assert "generated" in head
    assert isinstance(data["landing_inventory"], dict) and data["landing_inventory"]


# --- Done 2: the landing inventory (the generator; the classes are tested in test_transport_lint) -----------

def test_the_inventory_is_generated_byte_identical_and_lists_the_reading_path_files(t, world, tmp_path):
    root = world["root"]
    _snapshot_world(world)
    _put(root, "LANE-demo.md", _head(by=TA44))
    inv = t.build_inventory(root)
    assert inv["to-cc/PLAN-x-v1.md"] == hashlib.sha256((root / "to-cc" / "PLAN-x-v1.md").read_bytes()).hexdigest()
    assert "LANE-demo.md" in inv and "to-cc/notes.txt" in inv              # unclassified files are inventoried
    assert not [k for k in inv if k.split("/")[-1].startswith(".") or k.endswith("desktop.ini")]
    assert t.build_inventory(root) == inv
    one, two = tmp_path / "one.yaml", tmp_path / "two.yaml"
    for path in (one, two):
        t.write_seat_ids(path, seats=list(SEATS), inventory=inv)
    assert one.read_bytes() == two.read_bytes()
    assert t.load_inventory(one) == inv
    assert t.load_inventory(tmp_path / "missing.yaml") is None
    (tmp_path / "bad.yaml").write_text("seats: [\n", encoding="utf-8")
    assert t.load_inventory(tmp_path / "bad.yaml") is None


def test_the_inventory_command_rewrites_only_its_own_section(t, world, tmp_path):
    _snapshot_world(world)
    seat_file = _seat_file(tmp_path)
    args = ["--transport-root", str(world["root"]), "--seat-ids", str(seat_file)]
    before_seats, _ = t.load_seat_ids(seat_file)
    assert t.main(["inventory", "--write", *args]) == 0
    seats, inv = t.load_seat_ids(seat_file)
    assert seats == before_seats and inv == t.build_inventory(world["root"])
    first = seat_file.read_bytes()
    assert t.main(["inventory", "--write", *args]) == 0
    assert seat_file.read_bytes() == first


# --- Done 3: the janitor ---------------------------------------------------------------------------------

def _janitor_world(world) -> dict:
    root = world["root"]
    sig = _head(by=TA44, date="2026-09-01")
    files = {
        "to-browser/DIGEST-s1-2026-09-01-superseded.md": sig,                          # head date -> 2026-09
        "to-cc/PLAN-p1-v1-superseded.md": _head(by=TA44),                              # no date -> undated
        "to-browser/QUESTION-seat9-superseded.md": _head(by="lane-x (job 1)", date="2026-09-20"),
        "to-cc/ANSWER-seat9-superseded.md": _head(by=TA44, date="2026-09-20"),
        "to-browser/DIGEST-name-date-2026-07-15-superseded.md": _head(by=TA44),         # name date -> 2026-07
        "to-browser/LEDGER-acme-ops.md": _head(by="gen_ledger.py"),
        "to-browser/LEDGER-acme-ops-v1-superseded-2026-09-10.md": _head(by=TA44, date="2026-09-10"),
        "to-browser/DIGEST-cv-old-2026-09-10-superseded.md": sig,
        "to-cc/CONTRACT-nosignal-v1-superseded.md": "plain\n",
        "to-browser/ODD-thing-superseded.md": sig,
        "to-browser/DIGEST-live-2026-10-01.md": sig,
        "to-cc/LANE-x.CLAIMED-ab12cd": "claim\n",
        "to-cc/DIGEST-wrongfolder-superseded.md": sig,
        "to-browser/DIGEST-coll-2026-08-01-superseded.md": _head(by=TA44, date="2026-08-01", summary="new"),
        "to-browser/archive/2026-09-05/old-day-file.md": "kept\n",
        "to-browser/archive/flat-old.md": "kept\n",
        "to-browser/archive/2026-08/DIGEST-coll-2026-08-01-superseded.md": "different bytes\n",
    }
    for rel, text in files.items():
        _put(root, rel, text)
    return files


def _tree_census(root: Path) -> dict:
    """live (direct children of the three homes) + archive (everything under an archive/ folder), and the
    multiset of every file's sha256 on the whole tree."""
    live = archive = 0
    shas = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        shas.append(hashlib.sha256(p.read_bytes()).hexdigest())
        if "archive" in p.relative_to(root).parts:
            archive += 1
        elif p.parent in (root, root / "to-cc", root / "to-browser") and not p.name.startswith("."):
            live += 1
    return {"live": live, "archive": archive, "shas": sorted(shas)}


def test_janitor_dry_run_lists_exactly_the_movable_set_and_moves_nothing(t, world):
    root = world["root"]
    _janitor_world(world)
    before = _tree_census(root)
    plan = t.janitor_plan(root, seats=SEATS)
    moved = {m["source"]: m for m in plan["moves"]}
    assert set(moved) == {
        "to-browser/DIGEST-s1-2026-09-01-superseded.md", "to-cc/PLAN-p1-v1-superseded.md",
        "to-browser/QUESTION-seat9-superseded.md", "to-cc/ANSWER-seat9-superseded.md",
        "to-browser/DIGEST-name-date-2026-07-15-superseded.md",
    }
    m = moved["to-browser/DIGEST-s1-2026-09-01-superseded.md"]
    assert m["destination"] == "to-browser/archive/2026-09/DIGEST-s1-2026-09-01-superseded.md"
    assert m["month"] == "2026-09" and m["month_source"] == "head"
    assert m["sha256"] == hashlib.sha256((root / m["source"]).read_bytes()).hexdigest() and m["bytes"] > 0
    assert moved["to-cc/PLAN-p1-v1-superseded.md"]["destination"] == "to-cc/archive/undated/PLAN-p1-v1-superseded.md"
    assert moved["to-cc/PLAN-p1-v1-superseded.md"]["month_source"] == "undated"
    nd = moved["to-browser/DIGEST-name-date-2026-07-15-superseded.md"]
    assert nd["month"] == "2026-07" and nd["month_source"] == "name"
    reasons = {s["path"]: s["reason"] for s in plan["skipped"]}
    assert reasons["to-browser/LEDGER-acme-ops-v1-superseded-2026-09-10.md"] == "UNATTRIBUTED"   # the veto
    assert reasons["to-browser/DIGEST-cv-old-2026-09-10-superseded.md"] == "UNATTRIBUTED"         # the cv segment
    assert reasons["to-cc/CONTRACT-nosignal-v1-superseded.md"] == "UNATTRIBUTED"
    assert reasons["to-browser/ODD-thing-superseded.md"] == "unregistered"
    assert reasons["to-cc/DIGEST-wrongfolder-superseded.md"] == "misfoldered"
    assert reasons["to-browser/DIGEST-coll-2026-08-01-superseded.md"] == "COLLISION"
    assert _tree_census(root) == before                                        # a dry run moves nothing
    expect = hashlib.sha256("\n".join(sorted(
        f"{m['source']}|{m['destination']}|{m['sha256']}" for m in plan["moves"])).encode("utf-8")).hexdigest()
    assert plan["manifest_sha256"] == expect
    live = before["live"]
    assert len(plan["moves"]) + len(plan["skipped"]) + plan["untouched"] == live


def test_janitor_apply_moves_exactly_the_plan_with_bytes_unchanged_and_counts_equal(t, world, monkeypatch):
    root = world["root"]
    _janitor_world(world)
    before = _tree_census(root)
    plan = t.janitor_plan(root, seats=SEATS)
    collision_src = root / "to-browser" / "DIGEST-coll-2026-08-01-superseded.md"
    collision_dst = root / "to-browser" / "archive" / "2026-08" / "DIGEST-coll-2026-08-01-superseded.md"
    src_bytes, dst_bytes = collision_src.read_bytes(), collision_dst.read_bytes()

    def boom(*a, **k):
        raise AssertionError("a delete or an overwrite was attempted")

    with monkeypatch.context() as mp:
        for target in ("remove", "unlink", "replace"):
            mp.setattr(os, target, boom)
        mp.setattr(shutil, "rmtree", boom)
        mp.setattr(shutil, "move", boom)
        report = t.janitor_apply(root, plan["manifest_sha256"], seats=SEATS)
    after = _tree_census(root)
    assert after["shas"] == before["shas"]                                     # no byte lost, none gained
    assert after["live"] + after["archive"] == before["live"] + before["archive"]
    assert after["live"] == before["live"] - len(plan["moves"])
    assert after["archive"] == before["archive"] + len(plan["moves"])
    assert report["moved"] == len(plan["moves"]) and report["census_after"]["live"] == after["live"]
    for m in plan["moves"]:
        assert not (root / m["source"]).exists()
        assert hashlib.sha256((root / m["destination"]).read_bytes()).hexdigest() == m["sha256"]
    assert collision_src.read_bytes() == src_bytes and collision_dst.read_bytes() == dst_bytes
    for kept in ("to-browser/archive/2026-09-05/old-day-file.md", "to-browser/archive/flat-old.md",
                 "to-browser/LEDGER-acme-ops-v1-superseded-2026-09-10.md", "to-browser/DIGEST-live-2026-10-01.md",
                 "to-cc/LANE-x.CLAIMED-ab12cd"):
        assert (root / kept).exists(), kept


def test_janitor_month_is_never_read_from_mtime(t, world):
    root = world["root"]
    _put(root, "to-browser/DIGEST-m-2026-06-01-superseded.md", _head(by=TA44))
    before = t.janitor_plan(root, seats=SEATS)
    os.utime(root / "to-browser" / "DIGEST-m-2026-06-01-superseded.md", (978307200, 978307200))
    after = t.janitor_plan(root, seats=SEATS)
    assert before["moves"] == after["moves"] and after["moves"][0]["month"] == "2026-06"


def test_janitor_apply_is_bound_to_the_reviewed_manifest(t, world, capsys):
    root = world["root"]
    _janitor_world(world)
    before = _tree_census(root)
    seat_file = _seat_file(world["root"].parent)
    args = ["--transport-root", str(root), "--seat-ids", str(seat_file)]
    assert t.main(["janitor", *args]) == 0                                     # the dry run
    out = capsys.readouterr().out
    manifest = re.search(r"manifest-sha256: ([0-9a-f]{64})", out).group(1)
    assert sum(1 for ln in out.splitlines() if " | " in ln and "archive/" in ln) == 5
    assert _tree_census(root) == before
    assert t.main(["janitor", "--apply", *args]) == 2                           # no hash: refused
    assert t.main(["janitor", "--apply", "--expect-manifest", "0" * 12, *args]) == 2
    assert t.main(["janitor", "--apply", "--expect-manifest", manifest[:8], *args]) == 2   # under 12 hex
    assert _tree_census(root) == before                                         # nothing moved by a refusal
    assert t.main(["janitor", "--apply", "--expect-manifest", manifest[:12], *args]) == 0
    assert _tree_census(root)["live"] == before["live"] - 5


def test_janitor_apply_refuses_when_the_list_changed_since_it_was_read(t, world):
    root = world["root"]
    _janitor_world(world)
    plan = t.janitor_plan(root, seats=SEATS)
    _put(root, "to-browser/DIGEST-extra-2026-09-02-superseded.md", _head(by=TA44, date="2026-09-02"))
    with pytest.raises(t.JanitorRefused):
        t.janitor_apply(root, plan["manifest_sha256"], seats=SEATS)
    assert (root / "to-browser" / "DIGEST-extra-2026-09-02-superseded.md").exists()


def test_gen_handoff_still_reads_the_moved_question_and_answer(t, world):
    """P-L3-3: `archive/<YYYY-MM>/` is one level down, where gen_handoff's globs look."""
    root = world["root"]
    _janitor_world(world)
    plan = t.janitor_plan(root, seats=SEATS)
    t.janitor_apply(root, plan["manifest_sha256"], seats=SEATS)
    gh = _mod("gen_handoff")
    questions = gh._question_files(root)
    moved_q = root / "to-browser" / "archive" / "2026-09" / "QUESTION-seat9-superseded.md"
    assert moved_q in questions
    verdict = gh._question_disposition_verdict(moved_q, root, None)
    assert verdict[0] is True and "ANSWERED by ANSWER-seat9-superseded.md" in verdict[1]


def test_janitor_apply_ends_with_a_full_index_run_when_an_index_exists(t, world, tmp_path):
    root = world["root"]
    _janitor_world(world)
    seat_file = _seat_file(tmp_path)
    args = ["--transport-root", str(root), "--seat-ids", str(seat_file)]
    assert t.main(["index", "--write", "--generated-at", STAMP, *args]) == 0
    plan = t.janitor_plan(root, seats=SEATS)
    t.janitor_apply(root, plan["manifest_sha256"], seats=SEATS, trigger_stamp=STAMP)
    assert t.main(["index", "--check", *args]) == 0                             # fresh after the moves


# --- Done 5: the INDEX trigger -----------------------------------------------------------------------------

@pytest.fixture()
def live(t, world, tmp_path, monkeypatch):
    """A fixture transport with an INDEX, the module told this root is the known transport and this
    seat-ids file its landing data."""
    seat_file = _seat_file(tmp_path)
    monkeypatch.setattr(t, "known_root", lambda: world["root"])
    monkeypatch.setattr(t, "DEFAULT_SEAT_IDS", seat_file)
    monkeypatch.setattr(t, "INDEX_LOCK_TIMEOUT_S", 0.2)
    _snapshot_world(world)
    index = world["browser"] / "INDEX.md"
    index.write_text(_index(t, world["root"]), encoding="utf-8", newline="\n")
    return {"index": index, "seat_file": seat_file, "root": world["root"]}


def _full_rebuild_like(t, live_ctx) -> str:
    """The full rebuild at the stamp and trigger the INDEX itself recorded."""
    header = t.parse_index(live_ctx["index"].read_text(encoding="utf-8"))["header"]
    return t.build_index(live_ctx["root"], seats=list(SEATS), generated_at=header["regenerated"],
                         trigger=header["trigger"])


def test_index_trigger_write_of_a_new_file_adds_its_row_and_records_the_trigger(t, world, live):
    dest = world["browser"] / "DIGEST-new-2026-10-10.md"
    t.write("operator", dest, _head(by=TA44, date="2026-10-10", summary="New digest"))
    text = live["index"].read_text(encoding="utf-8")
    parsed = t.parse_index(text)
    assert parsed["header"]["trigger"] == "write:to-browser/DIGEST-new-2026-10-10.md"
    assert parsed["header"]["regenerated"] != STAMP
    row = {e["path"]: e for e in parsed["entries"]}["to-browser/DIGEST-new-2026-10-10.md"]
    assert row["status"] == "current" and row["subject"] == "New digest" and row["by"] == TA44
    assert text == _full_rebuild_like(t, live)                     # the incremental result is the full rebuild


def test_index_trigger_with_no_index_creates_nothing(t, world, tmp_path, monkeypatch):
    seat_file = _seat_file(tmp_path)
    monkeypatch.setattr(t, "known_root", lambda: world["root"])
    monkeypatch.setattr(t, "DEFAULT_SEAT_IDS", seat_file)
    t.write("operator", world["browser"] / "DIGEST-new-2026-10-10.md", _head(by=TA44, date="2026-10-10"))
    assert not (world["browser"] / "INDEX.md").exists()


def test_index_trigger_does_nothing_for_a_root_that_is_not_the_known_transport(t, world, live, tmp_path, monkeypatch):
    other = tmp_path / "scratch" / "to-browser"
    other.mkdir(parents=True)
    before = live["index"].read_bytes()
    t.write("operator", other / "DIGEST-x-2026-10-10.md", _head(by=TA44))
    assert live["index"].read_bytes() == before


def test_writing_the_index_itself_does_not_recurse(t, world, live):
    body = _index(t, world["root"], stamp="2026-10-11T00:00:00Z")
    t.write("transport", live["index"], body)
    assert live["index"].read_text(encoding="utf-8") == body


def test_index_trigger_supersedes_changes_the_status_and_equals_a_full_rebuild(t, world, live):
    t.write("operator", world["cc"] / "PLAN-x-v3.md",
            _head(by=TA44, date="2026-10-09", summary="Plan three", supersedes="PLAN-x-v2.md"))
    text = live["index"].read_text(encoding="utf-8")
    status = {e["path"]: e["status"] for e in t.parse_index(text)["entries"]}
    assert status["to-cc/PLAN-x-v2.md"] == "superseded" and status["to-cc/PLAN-x-v3.md"] == "current"
    assert text == _full_rebuild_like(t, live)
    t.write("operator", world["cc"] / "PLAN-x-v3.md", _head(by=TA44, date="2026-10-09", summary="Plan three"))
    text = live["index"].read_text(encoding="utf-8")                # the supersedes line is gone: v2 is current
    assert {e["path"]: e["status"] for e in t.parse_index(text)["entries"]}["to-cc/PLAN-x-v2.md"] == "current"
    assert text == _full_rebuild_like(t, live)


def test_index_trigger_append_that_changes_the_head_equals_a_full_rebuild(t, world, live):
    dest = world["browser"] / "SESSION-lane-one.md"
    t.append("lane", dest, "by: lane-one (job abc12345)\ndate: 2026-10-09\nsummary: first block\n\n# S\n")
    text = live["index"].read_text(encoding="utf-8")
    assert text == _full_rebuild_like(t, live)
    t.append("lane", dest, "later block\n" * 3)
    assert live["index"].read_text(encoding="utf-8") == text         # head unchanged -> no refresh


def test_an_attribution_signal_appended_at_line_15_moves_an_unattributed_row(t, world, live):
    """Fix 1 (the Codex HIGH on revision 5): the row depends on the whole 30-line attribution window, not on
    the 12-line head. The signal lands beyond line 12 and inside line 30 of a file with 13 filler lines."""
    dest = world["browser"] / "SESSION-late-signal.md"
    # lines 1-13: a `by:` line (it carries no attribution signal) and 12 filler lines
    t.append("lane", dest, "by: lane-late (job abc12345)\n" + "\n".join(f"filler {i}" for i in range(2, 14)) + "\n")
    status = {e["path"]: e["status"] for e in t.parse_index(live["index"].read_text(encoding="utf-8"))["entries"]}
    assert status["to-browser/SESSION-late-signal.md"] == "unattributed"
    t.append("lane", dest, "dev-knowledge cited here\n")                              # line 15 (after the separator)
    lines = dest.read_text(encoding="utf-8").splitlines()
    assert lines.index("dev-knowledge cited here") + 1 == 15
    text = live["index"].read_text(encoding="utf-8")
    status = {e["path"]: e["status"] for e in t.parse_index(text)["entries"]}
    assert status["to-browser/SESSION-late-signal.md"] == "current"
    assert text == _full_rebuild_like(t, live)


def test_an_append_past_line_30_leaves_the_index_untouched(t, world, live):
    dest = world["browser"] / "SESSION-far-signal.md"
    # 30 lines: a `by:` line (it carries no attribution signal) and 29 filler lines
    t.append("lane", dest, "by: lane-far (job abc12345)\n" + "\n".join(f"filler {i}" for i in range(2, 31)) + "\n")
    before = live["index"].read_bytes()
    t.append("lane", dest, "dev-knowledge cited far away\n")
    assert live["index"].read_bytes() == before


def test_a_new_ledger_changes_the_veto_set_so_the_refresh_rebuilds_in_full(t, world, live):
    mention = world["browser"] / "DIGEST-mentions-acme-ops-2026-10-09.md"
    t.write("operator", mention, _head(by=TA44, date="2026-10-09", summary="mentions", body=("acme-ops notes",)))
    status = {e["path"]: e["status"] for e in t.parse_index(live["index"].read_text(encoding="utf-8"))["entries"]}
    assert status["to-browser/DIGEST-mentions-acme-ops-2026-10-09.md"] == "current"
    assert "acme-ops" not in t.parse_index(live["index"].read_text(encoding="utf-8"))["header"]["inputs"]
    t.write("gen_ledger", world["browser"] / "LEDGER-acme-ops.md", _head(by="gen_ledger.py", date="2026-10-10"))
    text = live["index"].read_text(encoding="utf-8")
    parsed = t.parse_index(text)
    assert {e["path"]: e["status"] for e in parsed["entries"]}[
        "to-browser/DIGEST-mentions-acme-ops-2026-10-09.md"] == "unattributed"
    assert "acme-ops" in parsed["header"]["inputs"]
    assert text == _full_rebuild_like(t, live)


def test_a_held_lock_or_a_permission_error_skips_the_refresh_and_the_write_succeeds(
        t, world, live, capsys, monkeypatch):
    before = live["index"].read_bytes()
    (world["browser"] / ".INDEX.md.append.lock").write_text("held", encoding="utf-8")
    dest = world["browser"] / "DIGEST-locked-2026-10-10.md"
    t.write("operator", dest, _head(by=TA44, date="2026-10-10"))
    assert dest.exists() and live["index"].read_bytes() == before
    assert "INDEX refresh skipped" in capsys.readouterr().err
    (world["browser"] / ".INDEX.md.append.lock").unlink()

    def deny(self):
        raise PermissionError("denied")

    monkeypatch.setattr(t._DestinationLock, "__enter__", deny)
    dest2 = world["browser"] / "DIGEST-denied-2026-10-10.md"
    t.write("operator", dest2, _head(by=TA44, date="2026-10-10"))
    assert dest2.exists() and live["index"].read_bytes() == before
    assert "INDEX refresh skipped" in capsys.readouterr().err


def test_a_refresh_failure_never_fails_the_callers_write(t, world, live, monkeypatch, capsys):
    monkeypatch.setattr(t, "refresh_index", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    dest = world["browser"] / "DIGEST-boom-2026-10-10.md"
    t.write("operator", dest, _head(by=TA44, date="2026-10-10"))
    assert dest.exists() and "INDEX refresh skipped" in capsys.readouterr().err


# --- Done 2: the write gate's by: rule ----------------------------------------------------------------------

def test_the_gate_refuses_a_role_writers_new_unsigned_md_and_advises_a_script_writer(
        t, world, live, capsys):
    unsigned = "plain text, no by line\n"
    with pytest.raises(t.TransportWriteRefused, match="by:"):
        t.write("operator", world["browser"] / "DIGEST-unsigned-2026-10-10.md", unsigned)
    assert not (world["browser"] / "DIGEST-unsigned-2026-10-10.md").exists()
    with pytest.raises(t.TransportWriteRefused, match="by:"):
        t.append("lane", world["browser"] / "SESSION-unsigned.md", unsigned)
    ok = t.write("gen_ledger", world["browser"] / "LEDGER-unsigned-repo.md", unsigned)   # a script writer
    assert ok.exists() and "no `by:`" in capsys.readouterr().err
    t.write("operator", world["browser"] / "DIGEST-signed-2026-10-10.md", _head(by=TA44))


def test_the_gate_lets_an_inventoried_path_through_and_fails_closed_without_an_inventory(
        t, world, live, tmp_path, monkeypatch):
    dest = world["browser"] / "DIGEST-old-unsigned-2026-10-02.md"
    dest.write_text("plain text\n", encoding="utf-8")
    inv = t.build_inventory(world["root"])
    seat_file = tmp_path / "with-inventory.yaml"
    t.write_seat_ids(seat_file, seats=list(SEATS), inventory=inv)
    monkeypatch.setattr(t, "DEFAULT_SEAT_IDS", seat_file)
    t.write("operator", dest, "plain text, edited\n")                  # in the inventory: not new, not refused
    monkeypatch.setattr(t, "DEFAULT_SEAT_IDS", tmp_path / "no-such-file.yaml")
    with pytest.raises(t.TransportWriteRefused, match="inventory"):
        t.write("operator", dest, "plain text, edited again\n")        # no readable inventory: fail closed


def test_the_gate_leaves_a_destination_outside_the_known_transport_alone(t, world, tmp_path):
    # no `known_root` patch: the fixture is not the real transport, so the by: rule does not engage
    t.write("operator", world["browser"] / "DIGEST-plain-2026-10-10.md", "plain\n")
