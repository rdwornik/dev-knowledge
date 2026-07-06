"""Tests for scripts/gen_handoff.py — the v5 handoff bundle generator (#164 RF-2 / RF-1 b).

The load-bearing test is the RECURRING BLUFF-DOGFOOD (`test_dogfood_*`): it re-runs on every
collection, so the anti-bluff property is enforced BY CONSTRUCTION on every generation — not by
a one-time promotion check (the RF-1 remedy: "make the bluff-dogfood recurring"). The other
tests pin the scaffold/framing/fill-state mechanics and the answer-free-bundle invariant.
"""
from __future__ import annotations

import os
import re
import shutil
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import gen_handoff as gh  # noqa: E402
import verify_handoff_probes as vhp  # noqa: E402

_REPO = gh._REPO_ROOT

# Minimal source stubs the hub probe-core binds to, so a generated bundle can be RESOLVED by
# verify_handoff_probes against a self-contained temp repo (no pollution of the live tree).
_STUB_FILES = {
    "VISION.md": "# V\n\n## Vision\nWhat .dev-knowledge is.\n",
    "ARCHITECTURE.md": "# A\n\n## Purpose [CORE]\nLayer 2 of the ADR-28 model.\n",
    "scripts/audit.py": "ALL_CHECKS = []\n",
    "scripts/validate_git_backlog.py": "x\n",
    "scripts/validate_doc_claims.py": "x\n",
    "scripts/validate_backlog.py": "x\n",
    "BACKLOG.md": "x\n",
    "protocols/HANDOFF_PROCESS.md": "# H\n\nno per-bundle README\n",
    "ecosystem/doc-counts.md": "- tests: **1 collected**\n",
    "ecosystem/disposition-register.yaml": "dispositions: []\n",
    "intake/README.md": "# INTAKE AREA DEFINITION\n",
    "intake/2026-01-01-first.md": (
        "---\nintake-id: 1\nstatus: SEED\norigin: test\nconsumed-by:\n---\n\n"
        "# First Stub Intake\n"
    ),
}


def _stub_repo(tmp_path):
    """A self-contained temp repo carrying every file the hub probe-core resolves against."""
    repo = tmp_path / "repo"
    for rel, content in _STUB_FILES.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return repo


def _gen(tmp_path, *, mode="architect", slug="0000-00-00-t", assemble=False, force_filled=None):
    repo = _stub_repo(tmp_path)
    return gh.generate(repo, mode=mode, slug=slug, repo=".dev-knowledge", date="2026-07-04",
                       bundle_root=repo / "docs" / "handoffs", force_filled=force_filled,
                       assemble=assemble)


def _rows(bundle_dir):
    return vhp.parse_probes((bundle_dir / "PROBES.md").read_text(encoding="utf-8"))


# --- the recurring bluff-dogfood (closure-critical, re-runs every collection) ------

def test_dogfood_no_probe_row_carries_an_answer_value(tmp_path):
    # ANTI-BLUFF BY CONSTRUCTION: no generated probe ROW may print an `expected:` answer hint
    # (the exact RF-1 regression). Re-runs every generation, so the property cannot silently rot.
    rows = _rows(_gen(tmp_path).bundle_dir)
    assert len(rows) == 10
    hits = [(r["id"], c) for r in rows for c in ("question", "source", "why", "command")
            if re.search(r"expected[ :]", r[c], re.IGNORECASE)]
    assert hits == [], f"generated probe rows carry answer hints: {hits}"


def test_dogfood_generated_bundle_has_no_failing_probe(tmp_path):
    # The generated bundle PASSES verify_handoff_probes (done-contract bullet 5): resolved against
    # a self-contained stub repo, no probe is FAIL-class. (grep/sed/git absent -> `skipped`, not
    # `fail`; a fail would mean a toothless/malformed/missing-source generated row.)
    res = _gen(tmp_path)
    results = vhp.verify(res.bundle_dir, repo_root=res.bundle_dir.parents[2])
    assert len(results) == 10
    fails = [(r.probe_id, r.detail) for r in results if r.status == "fail"]
    assert fails == [], f"generated bundle has failing probes: {fails}"


def test_dogfood_generated_rows_are_not_toothless(tmp_path):
    # Repo-independent structural guard: every generated row binds to a resolvable target
    # (file/anchor token) OR ships a value-bearing command — never toothless (mirrors the
    # #207 rung-3 condition without needing file resolution).
    for r in _rows(_gen(tmp_path).bundle_dir):
        assert all(r[c].strip() for c in ("question", "source", "why", "command")), r
        has_token = bool(vhp.file_tokens(r["source"]) or vhp._command_file_tokens(r["command"])
                         or vhp.header_tokens(r["source"]))
        value_bearing = not vhp._is_trivial_command(vhp.first_span(r["command"]))
        assert has_token or value_bearing, f"toothless generated row: {r['id']}"


# --- answer-free bundle invariant (bundle-wide, not just PROBES) -------------

def test_generation_hints_go_to_journal_draft_not_the_bundle(tmp_path):
    # The generator computes drift-reference VALUES for the JOURNAL draft, but they must never
    # enter a browser-visible file. Assert the draft is non-empty and the browser files carry
    # no `expected:` answer hint anywhere (rows or prose-as-values).
    res = _gen(tmp_path, assemble=True)
    assert "drift-reference hints" in res.journal_draft
    assert "NOT in the bundle" in res.journal_draft
    for name in ("PROBES.md", "HANDOFF_BOOT.md", "RESIDUAL.md", "PASTE_THIS.md"):
        text = (res.bundle_dir / name).read_text(encoding="utf-8")
        # no probe row prints an answer; RESIDUAL/BOOT state no verdict/count value
        for row in vhp.parse_probes(text):
            for c in ("question", "source", "why", "command"):
                assert not re.search(r"expected[ :]", row[c], re.IGNORECASE)


# --- cold <-> FILLED framing flip (deterministic, RF-2 item 3) ---------------

def test_cold_framing_when_supplement_empty(tmp_path):
    res = _gen(tmp_path)  # fresh SUPPLEMENT written empty -> cold
    assert res.filled is False
    probes = (res.bundle_dir / "PROBES.md").read_text(encoding="utf-8")
    boot = (res.bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    assert "beat fires **FULL**" in probes
    assert "generated EMPTY" in boot


def test_filled_framing_and_fillin_narrative_preserved(tmp_path):
    res = _gen(tmp_path)
    b = res.bundle_dir
    # operator fills the RESIDUAL frontier narrative + the SUPPLEMENT answers
    resid = (b / "RESIDUAL.md").read_text(encoding="utf-8")
    marker = "<!-- FILL-IN:frontier END -->"
    resid = resid.replace(marker, "OPERATOR-NARRATIVE-SENTINEL\n" + marker)
    (b / "RESIDUAL.md").write_text(resid, encoding="utf-8")
    sup = (b / "SUPPLEMENT.md").read_text(encoding="utf-8")
    (b / "SUPPLEMENT.md").write_text(sup + "\n1. Intent: ship it.\n", encoding="utf-8")
    # regenerate -> flips to FILLED, preserves the narrative
    res2 = gh.generate(b.parents[2], mode="architect", slug=b.name, repo=".dev-knowledge",
                       date="2026-07-04", bundle_root=b.parent, assemble=False)
    assert res2.filled is True
    probes = (b / "PROBES.md").read_text(encoding="utf-8")
    resid2 = (b / "RESIDUAL.md").read_text(encoding="utf-8")
    assert "NARROWS" in probes
    assert "OPERATOR-NARRATIVE-SENTINEL" in resid2   # RF-6: narrative not clobbered
    assert "ship it." in (b / "SUPPLEMENT.md").read_text(encoding="utf-8")  # supplement not clobbered


def test_force_filled_overrides_detection(tmp_path):
    res = _gen(tmp_path, force_filled=True)  # empty supplement, but forced filled framing
    assert res.filled is True
    assert "NARROWS" in (res.bundle_dir / "PROBES.md").read_text(encoding="utf-8")


# --- bundle shape / structure -----------------------------------------------

def test_architect_bundle_writes_all_files_and_mode_row(tmp_path):
    b = _gen(tmp_path, assemble=True).bundle_dir
    for name in ("HANDOFF_BOOT.md", "RESIDUAL.md", "PROBES.md", "SUPPLEMENT.md", "PASTE_THIS.md"):
        assert (b / name).exists(), name
    boot = (b / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    # assemble_paste must be able to read the Mode row
    assert re.search(r"(?im)^\|\s*\*{0,2}mode\*{0,2}\s*\|\s*\*{0,2}architect", boot)
    # the template-authoring comment must NOT ship
    assert "HANDOFF_BOOT.md.tmpl" not in boot
    assert boot.lstrip().startswith("# Handoff boot")


def test_execution_mode_writes_no_supplement(tmp_path):
    b = _gen(tmp_path, mode="execution").bundle_dir
    assert not (b / "SUPPLEMENT.md").exists()
    assert (b / "PROBES.md").exists()
    assert "execution mode" in (b / "HANDOFF_BOOT.md").read_text(encoding="utf-8")


def test_supplement_not_clobbered_on_regeneration(tmp_path):
    res = _gen(tmp_path)
    sup_path = res.bundle_dir / "SUPPLEMENT.md"
    sup_path.write_text(sup_path.read_text(encoding="utf-8") + "\nOPERATOR-FILLED\n", encoding="utf-8")
    gh.generate(res.bundle_dir.parents[2], mode="architect", slug=res.bundle_dir.name,
                repo=".dev-knowledge", date="2026-07-04", bundle_root=res.bundle_dir.parent,
                assemble=False)
    assert "OPERATOR-FILLED" in sup_path.read_text(encoding="utf-8")


def test_invalid_mode_rejected(tmp_path):
    with pytest.raises(ValueError):
        gh.generate(_stub_repo(tmp_path), mode="bogus", slug="0000-00-00-t")


# --- epic mode (§14a/§14b, ADR-97) — the dummy-epic done-contract demonstration ---

def _gen_epic(tmp_path, *, slug="0000-00-00-epic-t", epic_slug="dummy-epic"):
    """A dummy-epic bundle generated from a committed-state stub repo (the Epic 2
    done-contract demonstration: `--mode epic` produces a valid EPIC_BOOT bundle)."""
    repo = _stub_repo(tmp_path)
    return gh.generate(repo, mode="epic", slug=slug, repo=".dev-knowledge", date="2026-07-05",
                       bundle_root=repo / "docs" / "handoffs", epic_slug=epic_slug,
                       assemble=True)  # assemble is a no-op in epic mode (no PASTE_THIS)


def test_epic_bundle_writes_contract_files_and_no_v5_files(tmp_path):
    # EPIC_BOOT + PROBES + EPIC_RETURN; no v5 architect/execution artifacts (no SUPPLEMENT /
    # RESIDUAL / PASTE_THIS — assemble_paste's manifest is v5-shaped, deliberately skipped).
    b = _gen_epic(tmp_path).bundle_dir
    for name in ("EPIC_BOOT.md", "PROBES.md", "EPIC_RETURN.md"):
        assert (b / name).exists(), name
    for name in ("SUPPLEMENT.md", "RESIDUAL.md", "PASTE_THIS.md", "HANDOFF_BOOT.md"):
        assert not (b / name).exists(), name
    boot = (b / "EPIC_BOOT.md").read_text(encoding="utf-8")
    assert "EPIC_BOOT.md.tmpl" not in boot          # template-authoring comment stripped
    assert boot.lstrip().startswith("# EPIC HANDOFF — dummy-epic")
    assert "`epic/dummy-epic`" in boot              # {{EPIC_BRANCH}} substituted
    assert "epic-dummy-epic" in boot                # worktree naming convention
    assert re.search(r"(?im)^\|\s*\*{0,2}mode\*{0,2}\s*\|\s*\*{0,2}epic", boot)


def test_epic_probe_rows_are_answer_free_and_not_toothless(tmp_path):
    # The recurring bluff-dogfood, epic flavor: no generated row carries an answer hint, and
    # every row binds (file/anchor token or value-bearing command) — §5 held by construction.
    rows = _rows(_gen_epic(tmp_path).bundle_dir)
    assert len(rows) == 5
    hits = [(r["id"], c) for r in rows for c in ("question", "source", "why", "command")
            if re.search(r"expected[ :]", r[c], re.IGNORECASE)]
    assert hits == [], f"generated epic probe rows carry answer hints: {hits}"
    for r in rows:
        assert all(r[c].strip() for c in ("question", "source", "why", "command")), r
        has_token = bool(vhp.file_tokens(r["source"]) or vhp._command_file_tokens(r["command"])
                         or vhp.header_tokens(r["source"]))
        value_bearing = not vhp._is_trivial_command(vhp.first_span(r["command"]))
        assert has_token or value_bearing, f"toothless generated epic row: {r['id']}"


def test_epic_bundle_has_no_failing_probe(tmp_path):
    # The done-contract bullet: the generated dummy-epic bundle VALIDATES — resolved by
    # verify_handoff_probes against the self-contained stub repo, no probe is FAIL-class.
    res = _gen_epic(tmp_path)
    results = vhp.verify(res.bundle_dir, repo_root=res.bundle_dir.parents[2])
    assert len(results) == 5
    fails = [(r.probe_id, r.detail) for r in results if r.status == "fail"]
    assert fails == [], f"generated epic bundle has failing probes: {fails}"


def test_epic_fillins_and_return_survive_regeneration(tmp_path):
    # RF-6 carried into epic mode: the root's FILL-IN contract content and a lane-filled
    # EPIC_RETURN are preserved byte-for-byte across a re-render (never clobbered).
    res = _gen_epic(tmp_path)
    b = res.bundle_dir
    boot = (b / "EPIC_BOOT.md").read_text(encoding="utf-8")
    marker = "<!-- FILL-IN:boundary END -->"
    boot = boot.replace(marker, "ROOT-BOUNDARY-SENTINEL\n" + marker)
    (b / "EPIC_BOOT.md").write_text(boot, encoding="utf-8")
    ret_path = b / "EPIC_RETURN.md"
    ret_path.write_text(ret_path.read_text(encoding="utf-8") + "\nLANE-FILLED-RETURN\n",
                        encoding="utf-8")
    gh.generate(b.parents[2], mode="epic", slug=b.name, repo=".dev-knowledge",
                date="2026-07-05", bundle_root=b.parent, epic_slug="dummy-epic", assemble=False)
    assert "ROOT-BOUNDARY-SENTINEL" in (b / "EPIC_BOOT.md").read_text(encoding="utf-8")
    assert "LANE-FILLED-RETURN" in ret_path.read_text(encoding="utf-8")


def test_epic_slug_defaults_to_bundle_slug_and_hints_stay_out(tmp_path):
    # epic_slug omitted -> falls back to the bundle slug; the JOURNAL draft carries the
    # drift-reference hints and the bundle files carry none (answer-free invariant).
    repo = _stub_repo(tmp_path)
    res = gh.generate(repo, mode="epic", slug="0000-00-00-e2", repo=".dev-knowledge",
                      date="2026-07-05", bundle_root=repo / "docs" / "handoffs", assemble=False)
    boot = (res.bundle_dir / "EPIC_BOOT.md").read_text(encoding="utf-8")
    assert "`epic/0000-00-00-e2`" in boot
    assert "drift-reference hints" in res.journal_draft
    for name in ("EPIC_BOOT.md", "PROBES.md", "EPIC_RETURN.md"):
        text = (res.bundle_dir / name).read_text(encoding="utf-8")
        for row in vhp.parse_probes(text):
            for c in ("question", "source", "why", "command"):
                assert not re.search(r"expected[ :]", row[c], re.IGNORECASE)


# --- functional mode (§16, ADR-98) — the minimal one-file intake-capture boot -----

def _gen_functional(tmp_path, *, slug="0000-00-00-func-t", strip_intake=False):
    """A functional-mode bundle from a committed-state stub repo. `strip_intake` removes
    the stub intake/ fixtures first, to exercise the absent-dir degrade path."""
    repo = _stub_repo(tmp_path)
    if strip_intake:
        shutil.rmtree(repo / "intake")
    return gh.generate(repo, mode="functional", slug=slug, repo=".dev-knowledge", date="2026-07-07",
                       bundle_root=repo / "docs" / "handoffs", assemble=True)  # assemble is a no-op


def test_functional_bundle_is_one_file(tmp_path):
    b = _gen_functional(tmp_path).bundle_dir
    assert (b / "FUNCTIONAL_BOOT.md").exists()
    for name in ("PROBES.md", "RESIDUAL.md", "SUPPLEMENT.md", "EPIC_BOOT.md", "PASTE_THIS.md"):
        assert not (b / name).exists(), name


def test_functional_boot_carries_vision_extract_and_intake_index(tmp_path):
    boot = (_gen_functional(tmp_path).bundle_dir / "FUNCTIONAL_BOOT.md").read_text(encoding="utf-8")
    assert "What .dev-knowledge is." in boot                 # the stub VISION.md `## Vision` body
    assert "2026-01-01-first.md" in boot                     # intake index: filename
    assert "SEED" in boot                                    # intake index: status
    assert "First Stub Intake" in boot                        # intake index: title
    assert "INTAKE AREA DEFINITION" not in boot               # README.md excluded from the index


def test_functional_boot_is_probe_free_and_hint_free(tmp_path):
    res = _gen_functional(tmp_path)
    boot = (res.bundle_dir / "FUNCTIONAL_BOOT.md").read_text(encoding="utf-8")
    assert vhp.parse_probes(boot) == []
    assert not re.search(r"expected[ :]", boot, re.IGNORECASE)
    assert "drift-reference hints" in res.journal_draft       # hints still computed...
    assert "NOT in the bundle" in res.journal_draft            # ...but stay out of the bundle


def test_functional_absent_intake_dir_degrades(tmp_path):
    # No intake/ at all (feed not yet run, or a repo that hasn't adopted the scene): the
    # generator must degrade to the literal marker, never guess, and never raise.
    res = _gen_functional(tmp_path, strip_intake=True)
    boot = (res.bundle_dir / "FUNCTIONAL_BOOT.md").read_text(encoding="utf-8")
    assert "(no intake docs yet)" in boot


def test_functional_state_summary_fillin_survives_regeneration(tmp_path):
    # RF-6 in the functional shape: CC's authored state-summary paragraph is preserved
    # byte-for-byte across a re-render (mirrors test_epic_fillins_and_return_survive_regeneration).
    res = _gen_functional(tmp_path)
    b = res.bundle_dir
    boot = (b / "FUNCTIONAL_BOOT.md").read_text(encoding="utf-8")
    marker = "<!-- FILL-IN:state-summary END -->"
    boot = boot.replace(marker, "STATE-SUMMARY-SENTINEL\n" + marker)
    (b / "FUNCTIONAL_BOOT.md").write_text(boot, encoding="utf-8")
    gh.generate(b.parents[2], mode="functional", slug=b.name, repo=".dev-knowledge",
                date="2026-07-07", bundle_root=b.parent, assemble=False)
    assert "STATE-SUMMARY-SENTINEL" in (b / "FUNCTIONAL_BOOT.md").read_text(encoding="utf-8")


# --- developer mode (ADR-98) — a pure additive alias of epic ---------------------

def test_developer_alias_is_byte_identical_to_epic(tmp_path):
    repo = _stub_repo(tmp_path)
    res_epic = gh.generate(repo, mode="epic", slug="0000-00-00-alias-t", repo=".dev-knowledge",
                           date="2026-07-05", bundle_root=repo / "docs" / "handoffs-epic",
                           epic_slug="dummy-epic", assemble=False)
    res_dev = gh.generate(repo, mode="developer", slug="0000-00-00-alias-t", repo=".dev-knowledge",
                          date="2026-07-05", bundle_root=repo / "docs" / "handoffs-dev",
                          epic_slug="dummy-epic", assemble=False)
    for name in ("EPIC_BOOT.md", "PROBES.md", "EPIC_RETURN.md"):
        epic_bytes = (res_epic.bundle_dir / name).read_bytes()
        dev_bytes = (res_dev.bundle_dir / name).read_bytes()
        assert epic_bytes == dev_bytes, name
    assert not (res_dev.bundle_dir / "FUNCTIONAL_BOOT.md").exists()
