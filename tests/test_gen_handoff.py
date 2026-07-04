"""Tests for scripts/gen_handoff.py — the v5 handoff bundle generator (#164 RF-2 / RF-1 b).

The load-bearing test is the RECURRING BLUFF-DOGFOOD (`test_dogfood_*`): it re-runs on every
collection, so the anti-bluff property is enforced BY CONSTRUCTION on every generation — not by
a one-time promotion check (the RF-1 remedy: "make the bluff-dogfood recurring"). The other
tests pin the scaffold/framing/fill-state mechanics and the answer-free-bundle invariant.
"""
from __future__ import annotations

import os
import re
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
