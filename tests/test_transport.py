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

import importlib
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
    got = t.write("gen_lane_contract", dest, "x", registry=registry)
    assert got.read_text(encoding="utf-8") == "x"


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
