"""RED-first tests for the six handoff preflight truth rows.

Each failing fixture records a specific miss from the 2026-10-22 cut; the repaired
fixtures pin the corresponding evidence that lets the row pass.

Implements [#1640] (R6 stage L12b, lane handoff-truth): the cut-time preflight rows.
"""
from __future__ import annotations

import hashlib
import re

import pytest

import gen_handoff as gh

_TODAY = "2026-10-23"
_NEW_ROWS = (
    "fill_ins_filled",
    "seat_ids_both",
    "supplement_matches_transport",
    "landed_vs_ratified",
    "operator_decisions_list",
    "digest_owed_present",
)


def _transport(tmp_path, *, ledger_date=None, ratification_date=None,
               status_bytes=0, questions=(), answers=(), repo_name=".dev-knowledge"):
    """A transport directory with `to-cc/` and `to-browser/`."""
    root = tmp_path / "transport"
    to_browser = root / "to-browser"
    to_cc = root / "to-cc"
    to_browser.mkdir(parents=True, exist_ok=True)
    to_cc.mkdir(parents=True, exist_ok=True)
    if ledger_date:
        (to_browser / f"LEDGER-{repo_name.lstrip('.')}.md").write_text(
            f"# LEDGER\n<!-- owner: browser seat - v4 refreshed {ledger_date} 00:05 -->\n",
            encoding="utf-8")
    if ratification_date:
        (to_browser / f"RATIFICATION-{ratification_date}.md").write_text(
            "# RATIFICATION\n", encoding="utf-8")
    if status_bytes:
        head = b"## now\n"
        (to_browser / "STATUS-integrator.md").write_bytes(
            head + b"x" * (status_bytes - len(head)))
    for name, body in questions:
        (to_browser / name).write_text(body, encoding="utf-8")
    for name in answers:
        (to_cc / name).write_text("# ANSWER\n", encoding="utf-8")
    return root


def _hub_stub(tmp_path):
    """A repo with valid stamps on the docs read by the existing preflight rows."""
    repo = tmp_path / "repo"
    for rel in gh._stamped_docs():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"---\nlast_reviewed: {_TODAY}\nstatus: active\n---\n\n# doc\n",
            encoding="utf-8")
    return repo


@pytest.fixture
def _quiet_hub(monkeypatch):
    """Keep unrelated hub readers quiet so each test isolates its row's evidence."""
    monkeypatch.setattr(gh, "_is_hub", lambda _root: True)
    monkeypatch.setattr(gh, "_handoff_organ_findings", lambda _root: [])
    monkeypatch.setattr(gh, "_journal_spine_gaps", lambda _root: [])
    monkeypatch.setattr(gh, "_linked_worktrees", lambda _root: [])
    monkeypatch.setattr(gh, "_git_hygiene_branches", lambda _root: (["main"], ["main"]))


def _row(repo, transport, name, *, bundle_dir=None, trial_cut=False):
    rows = gh.preflight_rows(
        repo,
        transport=transport,
        today=_TODAY,
        bundle_dir=bundle_dir,
        trial_cut=trial_cut,
    )
    assert name in gh.PREFLIGHT_ROW_NAMES, (
        f"row not found: {name} not in PREFLIGHT_ROW_NAMES"
    )
    matching = [row for row in rows if row.name == name]
    assert matching, f"row not found: {name} not returned by preflight_rows"
    return matching[0]


def _fill_in_bundle(tmp_path, *, filled):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    markers = (
        ("purpose", "Purpose"),
        ("dest-worktree", "Destination worktree"),
        ("dest-scope", "Destination scope"),
        ("dest-mode-basis", "Destination mode basis"),
        ("driftflags", "Drift flags"),
        ("shipped", "Shipped"),
        ("frontier", "Frontier"),
    )
    contents = []
    for marker_id, label in markers:
        body = f"Recorded {label.lower()}." if filled else ""
        contents.append(
            f"<!-- FILL-IN:{marker_id} START ({label}) -->"
            f"{body}"
            f"<!-- FILL-IN:{marker_id} END -->"
        )
    (bundle / "HANDOFF_BOOT.md").write_text("\n".join(contents[:4]), encoding="utf-8")
    (bundle / "RESIDUAL.md").write_text("\n".join(contents[4:]), encoding="utf-8")
    return bundle


def _write_seat_evidence(repo, transport, *, registered):
    (transport / "to-cc" /
     "SUPPLEMENT-ANSWERS-Tech-Architect-46-2026-10-22.md").write_text(
        "# Answers\n", encoding="utf-8")
    (transport / "to-cc" /
     "SUPPLEMENT-ANSWERS-Tech-Architect-48-2026-10-24-superseded.md").write_text(
        "# Superseded answers\n", encoding="utf-8")
    seats = "\n".join(
        f"  - seat: Tech-Architect-{seat}\n    session: session-{seat}"
        for seat in registered
    )
    registry = repo / "ecosystem" / "seat-ids.yaml"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(f"seats:\n{seats}\n", encoding="utf-8")


def _supplement_evidence(tmp_path, *, folded_addendum):
    transport = _transport(tmp_path)
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    older = "Outgoing architect answers, version one."
    addendum = "A newer answer clarifies the destination."
    (transport / "to-cc" /
     "SUPPLEMENT-ANSWERS-Tech-Architect-46-2026-10-22.md").write_text(
        older, encoding="utf-8")
    (transport / "to-cc" /
     "SUPPLEMENT-ANSWERS-Tech-Architect-46-2026-10-23-addendum.md").write_text(
        addendum, encoding="utf-8")
    (transport / "to-cc" /
     "SUPPLEMENT-ANSWERS-Tech-Architect-46-2026-10-24-superseded.md").write_text(
        "Superseded answer that must not be selected.", encoding="utf-8")
    body = older + ("\n\n" + addendum if folded_addendum else "")
    (bundle / "SUPPLEMENT.md").write_text(body, encoding="utf-8")
    return transport, bundle, addendum, body


def _ruling_evidence(tmp_path, *, ratified, landed):
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    lines = "\n".join(f"- **R{number}** ratified ruling" for number in ratified)
    (transport / "to-browser" / "RATIFICATION-2026-10-22.md").write_text(
        f"# RATIFICATION\n{lines}\n", encoding="utf-8")
    (transport / "to-browser" / "RATIFICATION-2026-10-23-superseded.md").write_text(
        "# RATIFICATION\n- **R98**\n", encoding="utf-8")
    (transport / "to-browser" / "RATIFICATION-2026-10-24-withdrawn.md").write_text(
        "# RATIFICATION\n- **R99**\n", encoding="utf-8")
    standing = repo / "protocols" / "STANDING_RULINGS.md"
    standing.parent.mkdir(parents=True, exist_ok=True)
    standing.write_text(
        "\n".join(f"- **R{number}** landed ruling" for number in landed) + "\n",
        encoding="utf-8")
    return repo, transport


def _cut_fixture(tmp_path):
    """Reproduce the empty fields, missing seat, and disagreement from the 2026-10-22 cut."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    bundle = _fill_in_bundle(tmp_path, filled=False)
    _write_seat_evidence(repo, transport, registered=("43", "44", "45"))

    addendum = "A newer answer clarifies the destination."
    (transport / "to-cc" /
     "SUPPLEMENT-ANSWERS-Tech-Architect-46-2026-10-22.md").write_text(
        "Outgoing architect answers, version one.", encoding="utf-8")
    (transport / "to-cc" /
     "SUPPLEMENT-ANSWERS-Tech-Architect-46-2026-10-23-addendum.md").write_text(
        addendum, encoding="utf-8")
    (bundle / "SUPPLEMENT.md").write_text(
        "Outgoing architect answers, version one.", encoding="utf-8")

    (transport / "to-browser" / "RATIFICATION-2026-10-22.md").write_text(
        "# RATIFICATION\n- **R1**\n- **R2**\n- **R6**\n", encoding="utf-8")
    standing = repo / "protocols" / "STANDING_RULINGS.md"
    standing.parent.mkdir(parents=True, exist_ok=True)
    standing.write_text("- **R1**\n- **R2**\n", encoding="utf-8")

    (transport / "to-browser" / "DIGEST-2026-10-22.md").write_text(
        "# Batch digest\nNo owed list.\n", encoding="utf-8")
    return repo, transport, bundle


@pytest.mark.parametrize("name", _NEW_ROWS)
def test_absent_subject_is_not_applicable(tmp_path, _quiet_hub, name):
    """The 2026-10-22 cut's absent evidence must not be reported as a clean pass."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    row = _row(repo, transport, name)
    assert row.status == gh.PREFLIGHT_NA, row.render()


def test_bundle_without_fill_in_markers_is_not_applicable(tmp_path, _quiet_hub):
    """An untemplated bundle is absent FILL-IN evidence, not a repaired 2026-10-22 cut."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "HANDOFF_BOOT.md").write_text("# No fill-in markers\n", encoding="utf-8")
    row = _row(repo, transport, "fill_ins_filled", bundle_dir=bundle)
    assert row.status == gh.PREFLIGHT_NA, row.render()


def test_bundle_without_markdown_is_not_applicable_for_operator_decisions(
    tmp_path, _quiet_hub
):
    """An empty bundle directory has no operator-decision evidence from the 2026-10-22 cut."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    row = _row(repo, transport, "operator_decisions_list", bundle_dir=bundle)
    assert row.status == gh.PREFLIGHT_NA, row.render()


@pytest.mark.parametrize("missing", ("bundle", "transport"))
def test_missing_supplement_subject_is_not_applicable(tmp_path, _quiet_hub, missing):
    """Either missing supplement operand from the 2026-10-22 cut is n/a, not a mismatch."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (transport / "to-cc" / "SUPPLEMENT-ANSWERS-Tech-Architect-46.md").write_text(
        "Answers\n", encoding="utf-8")
    if missing == "transport":
        (transport / "to-cc" / "SUPPLEMENT-ANSWERS-Tech-Architect-46.md").unlink()
        (bundle / "SUPPLEMENT.md").write_text("Answers\n", encoding="utf-8")
    row = _row(
        repo,
        transport,
        "supplement_matches_transport",
        bundle_dir=None if missing == "bundle" else bundle,
    )
    assert row.status == gh.PREFLIGHT_NA, row.render()


@pytest.mark.parametrize("missing", ("ratification", "standing"))
def test_missing_ruling_source_is_not_applicable(tmp_path, _quiet_hub, missing):
    """A missing ruling source from the 2026-10-22 cut is n/a, not an empty-set match."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    if missing == "ratification":
        standing = repo / "protocols" / "STANDING_RULINGS.md"
        standing.parent.mkdir(parents=True, exist_ok=True)
        standing.write_text("- **R1** landed ruling\n", encoding="utf-8")
    else:
        (transport / "to-browser" / "RATIFICATION-2026-10-22.md").write_text(
            "# RATIFICATION\n- **R1**\n", encoding="utf-8")
    row = _row(repo, transport, "landed_vs_ratified")
    assert row.status == gh.PREFLIGHT_NA, row.render()


def test_fill_ins_refuse_the_seven_empty_fields_from_the_2026_10_22_cut(
    tmp_path, _quiet_hub
):
    """Reproduces seven empty FILL-INs that the 2026-10-22 cut left unresolved."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    bundle = _fill_in_bundle(tmp_path, filled=False)
    row = _row(repo, transport, "fill_ins_filled", bundle_dir=bundle)
    assert row.status == gh.PREFLIGHT_FAIL, row.render()
    for marker_id in ("purpose", "dest-worktree", "dest-scope", "dest-mode-basis",
                      "driftflags", "shipped", "frontier"):
        assert marker_id in row.detail
    assert "HANDOFF_BOOT.md" in row.detail
    assert "RESIDUAL.md" in row.detail


def test_filled_in_bundle_repairs_the_empty_fields_from_the_2026_10_22_cut(
    tmp_path, _quiet_hub
):
    """Reproduces the repaired bundle after all seven 2026-10-22 FILL-INs are filled."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    bundle = _fill_in_bundle(tmp_path, filled=True)
    row = _row(repo, transport, "fill_ins_filled", bundle_dir=bundle)
    assert row.status == gh.PREFLIGHT_PASS, row.render()


def test_fill_in_placeholder_text_is_still_empty_in_the_2026_10_22_cut(
    tmp_path, _quiet_hub
):
    """Reproduces a 2026-10-22 FILL-IN left at its generated `_(fill:...)` placeholder."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "HANDOFF_BOOT.md").write_text(
        "<!-- FILL-IN:purpose START (Purpose) -->_(fill: describe purpose)"
        "<!-- FILL-IN:purpose END -->\n",
        encoding="utf-8")
    row = _row(repo, transport, "fill_ins_filled", bundle_dir=bundle)
    assert row.status == gh.PREFLIGHT_FAIL, row.render()
    assert "purpose" in row.detail


def test_seat_registry_names_the_missing_tech_architect_47_from_the_2026_10_22_cut(
    tmp_path, _quiet_hub
):
    """Reproduces the 2026-10-22 cut's unregistered incoming Tech-Architect-47."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    _write_seat_evidence(repo, transport, registered=("43", "44", "45"))
    row = _row(repo, transport, "seat_ids_both")
    assert row.status == gh.PREFLIGHT_FAIL, row.render()
    assert "Tech-Architect-46" in row.detail
    assert "Tech-Architect-47" in row.detail


def test_both_seats_registered_repairs_the_2026_10_22_seat_gap(tmp_path, _quiet_hub):
    """Reproduces the repaired 2026-10-22 seat registry with both adjacent seats present."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    _write_seat_evidence(repo, transport, registered=("46", "47"))
    row = _row(repo, transport, "seat_ids_both")
    assert row.status == gh.PREFLIGHT_PASS, row.render()


def test_supplement_mismatch_names_the_newer_addendum_from_the_2026_10_22_cut(
    tmp_path, _quiet_hub
):
    """Reproduces the 2026-10-22 cut folding an older supplement but missing its addendum."""
    repo = _hub_stub(tmp_path)
    transport, bundle, addendum, body = _supplement_evidence(
        tmp_path, folded_addendum=False)
    row = _row(repo, transport, "supplement_matches_transport", bundle_dir=bundle)
    assert row.status == gh.PREFLIGHT_FAIL, row.render()
    transport_path = (transport / "to-cc" /
                      "SUPPLEMENT-ANSWERS-Tech-Architect-46-2026-10-23-addendum.md")
    transport_sha = hashlib.sha256(transport_path.read_bytes()).hexdigest()
    bundle_sha = hashlib.sha256((bundle / "SUPPLEMENT.md").read_bytes()).hexdigest()
    assert addendum not in body
    assert transport_sha in row.detail
    assert bundle_sha in row.detail
    assert transport_path.name in row.detail
    assert re.search(r"\b[0-9a-f]{64}\b", row.detail)


def test_supplement_folding_the_newest_addendum_repairs_the_2026_10_22_cut(
    tmp_path, _quiet_hub
):
    """Reproduces the repaired 2026-10-22 bundle after folding the newest answer verbatim."""
    repo = _hub_stub(tmp_path)
    transport, bundle, _addendum, _body = _supplement_evidence(
        tmp_path, folded_addendum=True)
    row = _row(repo, transport, "supplement_matches_transport", bundle_dir=bundle)
    assert row.status == gh.PREFLIGHT_PASS, row.render()


@pytest.mark.parametrize(
    ("ratified", "landed", "missing_label", "missing_ids"),
    [
        ((1, 2, 3), (1, 2, 3, 4, 5), "landed-not-ratified:", ("R4", "R5")),
        ((1, 2, 6), (1, 2), "ratified-not-landed:", ("R6",)),
    ],
)
def test_ruling_sets_disagreeing_on_the_2026_10_22_cut_are_named(
    tmp_path, _quiet_hub, ratified, landed, missing_label, missing_ids
):
    """Reproduces either direction of the 2026-10-22 Rulings/Landed disagreement."""
    repo, transport = _ruling_evidence(tmp_path, ratified=ratified, landed=landed)
    row = _row(repo, transport, "landed_vs_ratified")
    assert row.status == gh.PREFLIGHT_FAIL, row.render()
    assert missing_label in row.detail
    for missing_id in missing_ids:
        assert missing_id in row.detail
    assert "ratified-not-landed:" in row.detail
    assert "landed-not-ratified:" in row.detail


def test_equal_ruling_sets_repair_the_2026_10_22_boot_disagreement(tmp_path, _quiet_hub):
    """Reproduces the repaired 2026-10-22 ruling ledger with matching ratified and landed ids."""
    repo, transport = _ruling_evidence(tmp_path, ratified=(1, 2, 3), landed=(1, 2, 3))
    row = _row(repo, transport, "landed_vs_ratified")
    assert row.status == gh.PREFLIGHT_PASS, row.render()


def test_missing_operator_decisions_heading_reproduces_the_2026_10_22_cut(
    tmp_path, _quiet_hub
):
    """Reproduces the 2026-10-22 bundle omitting its operator-decisions section."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "HANDOFF_BOOT.md").write_text("# Handoff\n", encoding="utf-8")
    row = _row(repo, transport, "operator_decisions_list", bundle_dir=bundle)
    assert row.status == gh.PREFLIGHT_FAIL, row.render()


def test_operator_decisions_heading_repairs_the_2026_10_22_bundle(tmp_path, _quiet_hub):
    """Reproduces the repaired bundle with its case-insensitive operator-decisions heading."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "HANDOFF_BOOT.md").write_text(
        "# Handoff\n\n## operator decisions\n\n- Continue.\n", encoding="utf-8")
    row = _row(repo, transport, "operator_decisions_list", bundle_dir=bundle)
    assert row.status == gh.PREFLIGHT_PASS, row.render()


def test_digest_without_owed_list_reproduces_the_2026_10_22_cut(tmp_path, _quiet_hub):
    """Reproduces the 2026-10-22 batch digest that omitted its owed list."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    (transport / "to-browser" / "DIGEST-2026-10-21.md").write_text(
        "# Older digest\nowed:\n- old item\n", encoding="utf-8")
    digest = transport / "to-browser" / "DIGEST-2026-10-22.md"
    digest.write_text("# Batch digest\n", encoding="utf-8")
    row = _row(repo, transport, "digest_owed_present")
    assert row.status == gh.PREFLIGHT_FAIL, row.render()
    assert digest.name in row.detail


def test_digest_with_owed_list_repairs_the_2026_10_22_cut(tmp_path, _quiet_hub):
    """Reproduces the repaired 2026-10-22 digest with a flush-left owed list."""
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    (transport / "to-browser" / "DIGEST-2026-10-22.md").write_text(
        "# Batch digest\nowed:\n- R6 follow-up\n", encoding="utf-8")
    row = _row(repo, transport, "digest_owed_present")
    assert row.status == gh.PREFLIGHT_PASS, row.render()


def test_new_truth_rows_are_appended_after_git_hygiene_in_contract_order():
    """Pins the six rows added to expose the 2026-10-22 cut's omitted truth checks."""
    assert gh.PREFLIGHT_ROW_NAMES[-7:] == ("git_hygiene", *_NEW_ROWS)


def test_truth_rows_do_not_change_between_trial_and_real_cut(tmp_path, _quiet_hub):
    """The 2026-10-22 cut's six failures remain visible in both cut evaluation modes."""
    repo, transport, bundle = _cut_fixture(tmp_path)
    normal_rows = gh.preflight_rows(
        repo, transport=transport, today=_TODAY, bundle_dir=bundle, trial_cut=False)
    trial_rows = gh.preflight_rows(
        repo, transport=transport, today=_TODAY, bundle_dir=bundle, trial_cut=True)
    normal = {row.name: row.status for row in normal_rows if row.name in _NEW_ROWS}
    trial = {row.name: row.status for row in trial_rows if row.name in _NEW_ROWS}
    assert tuple(name for name in _NEW_ROWS if name in normal) == _NEW_ROWS
    assert trial == normal
    assert set(normal.values()) == {gh.PREFLIGHT_FAIL}


def _role_pin_fixture(tmp_path, *, seat_model="claude-opus-5.5", registry_model="claude-opus-5.5",
                      pasted_sha=None, project_boot=None):
    import hashlib

    repo = tmp_path / "role-repo"
    transport = tmp_path / "role-transport"
    bundle = tmp_path / "role-bundle"
    (repo / "protocols").mkdir(parents=True)
    (repo / "ecosystem").mkdir()
    (transport / "to-browser").mkdir(parents=True)
    bundle.mkdir()
    boot = b"---\nboot_version: 3\n---\n\n# Operating protocol\n"
    boot_path = repo / "protocols" / "HANDOFF_BOOT.md"
    boot_path.write_bytes(boot)
    (repo / "ecosystem" / "provider-registry.yaml").write_text(
        "roles:\n  architect:\n    order:\n      - model: " + registry_model + "\n",
        encoding="utf-8",
    )
    (bundle / "SEAT-BOOT-Tech-Architect-47.md").write_text(
        f"<!-- ROLE PIN | model: {seat_model} | -->\n", encoding="utf-8")
    live_sha = hashlib.sha256(boot).hexdigest()
    (bundle / "PASTE_THIS.md").write_text(
        f"ROLE PIN — HANDOFF_BOOT.md @ handoff-process v3\nsha256: "
        f"{pasted_sha or live_sha}\n",
        encoding="utf-8",
    )
    if project_boot is not None:
        (transport / "HANDOFF_BOOT.md").write_bytes(project_boot)
    return repo, transport, bundle, live_sha


def _role_pin_row(repo, transport, bundle):
    row_fn = getattr(gh, "_row_role_pin_current", None)
    assert callable(row_fn), "gen_handoff._row_role_pin_current is required"
    return row_fn(repo, transport, bundle)


def test_role_pin_current_is_the_final_preflight_row():
    assert gh.PREFLIGHT_ROW_NAMES[-1] == "role_pin_current"


def test_role_pin_current_is_not_applicable_without_a_bundle(tmp_path):
    repo, transport, _bundle, _sha = _role_pin_fixture(tmp_path)
    row = _role_pin_row(repo, transport, None)
    assert row.status == gh.PREFLIGHT_NA
    assert row.detail.startswith("SUBJECT-ABSENT")


def test_role_pin_current_rejects_a_seat_model_missing_from_the_provider_registry(tmp_path):
    repo, transport, bundle, _sha = _role_pin_fixture(
        tmp_path, seat_model="unregistered-model")
    row = _role_pin_row(repo, transport, bundle)
    assert row.status == gh.PREFLIGHT_FAIL
    assert "SEAT-BOOT-Tech-Architect-47.md" in row.detail
    assert "unregistered-model" in row.detail


def test_role_pin_current_names_both_hashes_for_a_stale_boot_pin(tmp_path):
    repo, transport, bundle, live_sha = _role_pin_fixture(tmp_path, pasted_sha="0" * 64)
    row = _role_pin_row(repo, transport, bundle)
    assert row.status == gh.PREFLIGHT_FAIL
    assert "0" * 64 in row.detail and live_sha in row.detail


def test_role_pin_current_names_versions_and_hashes_for_a_stale_project_copy(tmp_path):
    import hashlib

    stale_copy = b"---\nboot_version: 2\n---\n\n# Old project copy\n"
    repo, transport, bundle, live_sha = _role_pin_fixture(
        tmp_path, project_boot=stale_copy)
    row = _role_pin_row(repo, transport, bundle)
    stale_sha = hashlib.sha256(stale_copy).hexdigest()
    assert row.status == gh.PREFLIGHT_FAIL
    assert "stale Project copy" in row.detail
    assert "2" in row.detail and "3" in row.detail
    assert stale_sha in row.detail and live_sha in row.detail


@pytest.mark.parametrize("seat_model", ("opus", "claude-opus-5.5"))
def test_role_pin_current_passes_registered_model_and_fresh_boot_copies(tmp_path, seat_model):
    repo, transport, bundle, live_sha = _role_pin_fixture(tmp_path, seat_model=seat_model)
    (transport / "HANDOFF_BOOT.md").write_bytes(
        (repo / "protocols" / "HANDOFF_BOOT.md").read_bytes())
    row = _role_pin_row(repo, transport, bundle)
    assert row.status == gh.PREFLIGHT_PASS
    assert "SEAT-BOOT-Tech-Architect-47.md" in row.detail
    assert live_sha[:8] in row.detail


def test_role_pin_current_skips_an_absent_project_copy(tmp_path):
    repo, transport, bundle, _live_sha = _role_pin_fixture(tmp_path, seat_model="opus")
    row = _role_pin_row(repo, transport, bundle)
    assert not (transport / "HANDOFF_BOOT.md").exists()
    assert row.status == gh.PREFLIGHT_PASS


def test_preflight_rows_include_role_pin_current(tmp_path, _quiet_hub):
    repo = _hub_stub(tmp_path)
    transport = _transport(tmp_path)
    (repo / "ecosystem").mkdir(exist_ok=True)
    (repo / "ecosystem" / "provider-registry.yaml").write_text(
        "roles:\n  architect:\n    order:\n      - model: claude-opus-5.5\n",
        encoding="utf-8",
    )
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    boot = b"---\nboot_version: 3\n---\n"
    (repo / "protocols" / "HANDOFF_BOOT.md").write_bytes(boot)
    sha = hashlib.sha256(boot).hexdigest()
    (bundle / "SEAT-BOOT-Tech-Architect-47.md").write_text(
        "<!-- ROLE PIN | model: claude-opus-5.5 | -->\n", encoding="utf-8")
    (bundle / "PASTE_THIS.md").write_text(
        f"ROLE PIN — HANDOFF_BOOT.md @ handoff-process v3\nsha256: {sha}\n",
        encoding="utf-8",
    )
    row = _row(repo, transport, "role_pin_current", bundle_dir=bundle)
    assert row.name == "role_pin_current"
