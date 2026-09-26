"""Tests for scripts/gen_handoff.py — the v5 handoff bundle generator (#164 RF-2 / RF-1 b).

The load-bearing test is the RECURRING BLUFF-DOGFOOD (`test_dogfood_*`): it re-runs on every
collection, so the anti-bluff property is enforced BY CONSTRUCTION on every generation — not by
a one-time promotion check (the RF-1 remedy: "make the bluff-dogfood recurring"). The other
tests pin the scaffold/framing/fill-state mechanics and the answer-free-bundle invariant.
"""
from __future__ import annotations

import dataclasses
import inspect
import os
import re
import shutil
import subprocess
import sys

import pytest


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
    "scripts/gen_task_tree.py": "x\n",     # P0a's currency assertion target (R2, [#446])
    "BACKLOG.md": "x\n",
    "protocols/HANDOFF_PROCESS.md": "# H\n\nVersion: 7.1.0\n\nno per-bundle README\n",
    # The boot's DATA block points at these, and `verify_handoff_probes` resolves every pointer,
    # so the stub carries each target (lane-boot-contract, 2026-09-25).
    "protocols/HANDOFF_BOOT.md": "# Browser role\n",
    "protocols/STANDING_RULINGS.md": "# Standing rulings\n",
    "scripts/dispatch.py": "@cli.command(\"launch\")\ndef launch(): ...\n",
    "templates/dispatcher-order-template.md": "x\n",
    "templates/integrator-order-template.md": "x\n",
    "templates/batch-common-rules-template.md": "x\n",
    "templates/lane-contract-template.md": "x\n",
    "ecosystem/provider-registry.yaml": "x: 1\n",
    "ecosystem/harness.yaml": "x: 1\n",
    "docs/handoffs/README.md": "# Runbook\n",
    # P1a binds `README.md` `## Vision` since ADR-114 and P8b the grammar table; without these
    # two a generated bundle cannot pass its own probes in the stub (the dry-cut test needs it).
    "README.md": "# R\n\n## Vision\nWhat .dev-knowledge is.\n",
    "protocols/OPERATOR-INTERFACE.md": (
        "# O\n\n## 1. File exchange goes through the Downloads directory\n"),
    "ecosystem/doc-counts.md": "- tests: **1 collected**\n",
    "ecosystem/disposition-register.yaml": "dispositions: []\n",
    "docs/intake/README.md": "# INTAKE AREA DEFINITION\n",
    "docs/intake/2026-01-01-first.md": (
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
    assert len(rows) == 15  # 13 -> 15: P8a/P8b split + P11 (v7.1); an inherited red, fixed
    # 11 -> 14: P0a/P0b/P0c standing-topic legs added (R2 / [#446], 2026-07-31);
    # 14 -> 13: P10 (BACKLOG grooming) REMOVED 2026-08-26 — it asked for unbounded judgment
    # over an open set, which HANDOFF_PROCESS §5 cond. 4 rejects and names P10 as its origin.
    # Now P0a/P0b/P0c + P1a/P1b + P2..P9.
    hits = [(r["id"], c) for r in rows for c in ("question", "source", "why", "command")
            if re.search(r"expected[ :]", r[c], re.IGNORECASE)]
    assert hits == [], f"generated probe rows carry answer hints: {hits}"


def test_dogfood_generated_bundle_has_no_failing_probe(tmp_path):
    # The generated bundle PASSES verify_handoff_probes (done-contract bullet 5): resolved against
    # a self-contained stub repo, no probe is FAIL-class. (grep/sed/git absent -> `skipped`, not
    # `fail`; a fail would mean a toothless/malformed/missing-source generated row.)
    res = _gen(tmp_path)
    results = vhp.verify(res.bundle_dir, repo_root=res.bundle_dir.parents[2])
    # lane-boot-contract (2026-09-25): the boot's DATA rows are probe-checked too, and ride in
    # the same result list under a `BD-` id; the count below is the PROBES.md table only.
    results = [r for r in results if not r.probe_id.startswith(("BD-", "BP-"))]
    assert len(results) == 15  # 13 -> 15: P8a/P8b split + P11 added (v7.1); see the test above.
    # 11 -> 14: P0a/P0b/P0c standing-topic legs added (R2 / [#446], 2026-07-31);
    # 14 -> 13: P10 (BACKLOG grooming) REMOVED 2026-08-26 — it asked for unbounded judgment
    # over an open set, which HANDOFF_PROCESS §5 cond. 4 rejects and names P10 as its origin.
    # Now P0a/P0b/P0c + P1a/P1b + P2..P9.
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


def test_reflow_framing_flips_cold_sources_after_late_fill(tmp_path):
    # The fill-step bug the A5-5 fix closes: a bundle generated COLD, then the SUPPLEMENT filled
    # AFTER generation (the real workflow — assemble_paste is re-run, gen_handoff is not). The
    # source files still announce "generated EMPTY" until reflow_framing (now called by
    # assemble_paste) flips them, without clobbering hand-authored FILL-IN narrative.
    b = _gen(tmp_path).bundle_dir  # cold
    assert "generated EMPTY" in (b / "PROBES.md").read_text(encoding="utf-8")
    # operator hand-authors a frontier sentence that merely MENTIONS "generated EMPTY" (must be
    # preserved) and fills the supplement answers
    resid = (b / "RESIDUAL.md").read_text(encoding="utf-8")
    resid = resid.replace("<!-- FILL-IN:frontier END -->",
                          "The why: SUPPLEMENT ANSWERS is generated EMPTY per the author.\n"
                          "<!-- FILL-IN:frontier END -->")
    (b / "RESIDUAL.md").write_text(resid, encoding="utf-8")
    sup = (b / "SUPPLEMENT.md").read_text(encoding="utf-8")
    (b / "SUPPLEMENT.md").write_text(sup + "\n1. Intent: ship it.\n", encoding="utf-8")

    flipped = gh.reflow_framing(b)
    assert "PROBES.md" in flipped and "HANDOFF_BOOT.md" in flipped
    probes = (b / "PROBES.md").read_text(encoding="utf-8")
    assert "generated EMPTY" not in probes
    assert "NARROWS" in probes
    # the differently-worded hand-authored sentence is NOT matched by the surgical block replace
    assert "generated EMPTY per the author." in (b / "RESIDUAL.md").read_text(encoding="utf-8")
    # idempotent: a second reflow finds no cold framing block left to flip
    assert gh.reflow_framing(b) == []


def test_reflow_framing_noop_on_cold_bundle(tmp_path):
    # A cold (unfilled) supplement must leave the cold framing untouched — reflow is fill-gated.
    b = _gen(tmp_path).bundle_dir
    assert gh.reflow_framing(b) == []
    assert "generated EMPTY" in (b / "PROBES.md").read_text(encoding="utf-8")


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
    the stub docs/intake/ fixtures first, to exercise the absent-dir degrade path."""
    repo = _stub_repo(tmp_path)
    if strip_intake:
        shutil.rmtree(repo / "docs" / "intake")
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
    # No docs/intake/ at all (feed not yet run, or a repo that hasn't adopted the scene): the
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


# --- chat-title in every bundle header (#287 / #164 leg e) ------------------------

def test_chat_title_unit_grammar_per_mode():
    # The frozen grammar: `[REPO] <role> <ident> · SEQ 1`; role per mode; epic derives EPIC <n>.
    assert gh._chat_title("architect", ".dev-knowledge", "s") == "[dev-knowledge] Technical Architect — s · SEQ 1"
    assert gh._chat_title("execution", ".dev-knowledge", "s") == "[dev-knowledge] Developer — s · SEQ 1"
    assert gh._chat_title("functional", ".dev-knowledge", "s") == "[dev-knowledge] Functional Architect — s · SEQ 1"
    # epic: ident is the epic slug (name + number); EPIC <n> derived from the leading number.
    assert gh._chat_title("epic", ".dev-knowledge", "164-handoff-generator") == \
        "[dev-knowledge] Developer 164-handoff-generator EPIC 164 · SEQ 1"
    # epic slug with NO leading number: no EPIC <n> fabricated (degrade, never guess).
    assert gh._chat_title("epic", ".dev-knowledge", "hygiene-sweep") == \
        "[dev-knowledge] Developer hygiene-sweep · SEQ 1"


def test_chat_title_row_in_architect_and_execution_headers(tmp_path):
    for mode, role in (("architect", "Technical Architect"), ("execution", "Developer")):
        boot = (_gen(tmp_path / mode, mode=mode).bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
        assert re.search(r"(?im)^\|\s*\*{0,2}chat title\*{0,2}\s*\|", boot), f"{mode}: no Chat title row"
        assert f"[dev-knowledge] {role}" in boot
        assert "· SEQ 1" in boot
        assert "{{" not in boot          # token fully substituted


def test_chat_title_row_in_functional_header(tmp_path):
    boot = (_gen_functional(tmp_path).bundle_dir / "FUNCTIONAL_BOOT.md").read_text(encoding="utf-8")
    assert "[dev-knowledge] Functional Architect" in boot
    assert "· SEQ 1" in boot
    assert "{{" not in boot


def test_chat_title_row_in_epic_header_uses_epic_slug(tmp_path):
    repo = _stub_repo(tmp_path)
    b = gh.generate(repo, mode="epic", slug="0000-00-00-e", repo=".dev-knowledge", date="2026-07-08",
                    bundle_root=repo / "docs" / "handoffs", epic_slug="164-handoff-generator",
                    assemble=False).bundle_dir
    boot = (b / "EPIC_BOOT.md").read_text(encoding="utf-8")
    assert "[dev-knowledge] Developer 164-handoff-generator EPIC 164 · SEQ 1" in boot
    assert "{{" not in boot


# --- RM-8 overwrite refusal (R5 / [#446]) ----------------------------------------
# The REFUSAL itself is pinned by the frozen contract (tests/test_v6_frozen_contract.py
# ::test_fr5_*). These cover the halves the freeze does not: the fail-OPEN degrade
# contract, the sanctioned in-place re-render, and the suffix-naming rule.

def _git_init_commit(repo, msg="seed"):
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-qm", msg]):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)


def test_untracked_bundle_dir_is_still_rendered_in_place(tmp_path):
    """The sanctioned re-render path: a bundle dir that exists but holds NO tracked file is
    the bundle being generated right now (or a `--filled` reflow), so RM-8 must NOT refuse it.
    This is why `exist_ok=True` survives behind the guard rather than being deleted."""
    repo = _stub_repo(tmp_path)
    _git_init_commit(repo)                      # commits the stub files only...
    slug = "0000-00-00-inflight"
    bundle = repo / "docs" / "handoffs" / slug
    bundle.mkdir(parents=True)                  # ...the bundle appears AFTER, so it is untracked
    (bundle / "RESIDUAL.md").write_text("in-flight, uncommitted\n", encoding="utf-8")
    assert gh._tracked_under(repo, bundle) == []
    res = gh.generate(repo, mode="architect", slug=slug, repo=".dev-knowledge",
                      date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    assert res.bundle_dir == bundle             # in place: no refusal, no suffix


def test_refusal_survives_an_inherited_git_dir(tmp_path, monkeypatch):
    """REGRESSION (codex HIGH, 2026-07-31): `_git` returned "" for BOTH "no tracked files" and
    "git failed", so any git error authorized the target — an inherited bogus GIT_DIR silently
    DISARMED the RM-8 refusal against a genuinely tracked bundle ([#355]'s class, reproduced).

    Two fixes are asserted together: the git-location env is SCRUBBED (so an inherited GIT_DIR
    cannot redirect the query at all), and tracking-status-unknown is no longer conflated with
    nothing-tracked. Either alone leaves a hole."""
    repo = _stub_repo(tmp_path)
    slug = "0000-00-00-inherited"
    bundle = repo / "docs" / "handoffs" / slug
    bundle.mkdir(parents=True)
    (bundle / "RESIDUAL.md").write_text("committed\n", encoding="utf-8")
    _git_init_commit(repo)                         # the bundle IS tracked
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "nonexistent.git"))

    assert gh._tracked_under(repo, bundle), "scrubbed env must still see the tracked file"
    with pytest.raises(gh.BundleCollisionError):
        gh.generate(repo, mode="architect", slug=slug, repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=repo / "docs" / "handoffs")


def test_refusal_when_tracking_status_is_unknown(tmp_path, monkeypatch):
    """A git that is PRESENT but ERRORS leaves tracking status UNKNOWN — distinct from "not a
    git repo". Unknown refuses (conservative: an existing target may be a committed bundle);
    not-a-repo proceeds (nothing can be tracked). Conflating the two is what F3 was."""
    repo = _stub_repo(tmp_path)
    slug = "0000-00-00-unknown"
    bundle = repo / "docs" / "handoffs" / slug
    bundle.mkdir(parents=True)
    (bundle / "RESIDUAL.md").write_text("prior\n", encoding="utf-8")
    _git_init_commit(repo)
    monkeypatch.setattr(gh, "_git_status", lambda *a, **k: (None, "boom"))
    with pytest.raises(gh.BundleCollisionError) as exc:
        gh.generate(repo, mode="architect", slug=slug, repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=repo / "docs" / "handoffs")
    assert "could not be determined" in str(exc.value)


def test_refusal_degrades_open_without_git(tmp_path):
    """Fail-OPEN degrade contract (stated at `_tracked_under`): no git repo -> nothing is
    tracked -> generation proceeds. A generator that cannot reach git must not refuse to
    generate; `_stub_repo` is never `git init`ed, which is exactly that environment."""
    repo = _stub_repo(tmp_path)
    slug = "0000-00-00-nogit"
    bundle = repo / "docs" / "handoffs" / slug
    bundle.mkdir(parents=True)
    (bundle / "RESIDUAL.md").write_text("prior\n", encoding="utf-8")
    assert gh._tracked_under(repo, bundle) == []
    res = gh.generate(repo, mode="architect", slug=slug, repo=".dev-knowledge",
                      date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    assert res.bundle_dir == bundle


def test_allow_suffix_never_selects_an_existing_dir(tmp_path):
    """REGRESSION (codex HIGH, 2026-07-31): suffix selection accepted the first sibling with no
    TRACKED files — so an EXISTING dir holding untracked in-progress work was selected and then
    written into, destroying it. Reproduced with real data loss before this test existed.

    The contract the CLI already promised ("write a NEW `-<n>` sibling") is now the contract the
    code keeps: only a NONEXISTENT directory is selectable. Tracked-ness is not the test —
    existence is; an untracked in-progress bundle is exactly the thing worth not clobbering."""
    repo = _stub_repo(tmp_path)
    slug = "0000-00-00-collide"
    root = repo / "docs" / "handoffs"
    (root / slug).mkdir(parents=True)
    (root / slug / "RESIDUAL.md").write_text(f"committed {slug}\n", encoding="utf-8")
    _git_init_commit(repo)                       # slug is TRACKED -> collision
    # -2 exists and is UNTRACKED: in-progress work, invisible to `git ls-files`
    (root / f"{slug}-2").mkdir()
    sentinel = "IN-PROGRESS UNTRACKED WORK — MUST SURVIVE\n"
    (root / f"{slug}-2" / "RESIDUAL.md").write_text(sentinel, encoding="utf-8")

    res = gh.generate(repo, mode="architect", slug=slug, repo=".dev-knowledge",
                      date="2026-07-04", bundle_root=root, allow_suffix=True, assemble=False)

    assert res.bundle_dir == root / f"{slug}-3", \
        f"selected {res.bundle_dir.name}; an EXISTING dir is never selectable"
    assert (root / f"{slug}-2" / "RESIDUAL.md").read_text(encoding="utf-8") == sentinel, \
        "the untracked in-progress bundle was clobbered"
    assert (root / slug / "RESIDUAL.md").read_text(encoding="utf-8") == f"committed {slug}\n"


def test_allow_suffix_picks_the_next_free_sibling(tmp_path):
    """`--allow-suffix` writes `-2`, then `-3` when `-2` already exists — the repo's own
    witnessed convention (`2026-07-02-dev-knowledge-architect-2`). Here both colliders are
    TRACKED; the sibling case where `-2` exists but is UNTRACKED is the regression above."""
    repo = _stub_repo(tmp_path)
    slug = "0000-00-00-collide"
    root = repo / "docs" / "handoffs"
    for name in (slug, f"{slug}-2"):
        (root / name).mkdir(parents=True)
        (root / name / "RESIDUAL.md").write_text(f"committed {name}\n", encoding="utf-8")
    _git_init_commit(repo)                      # both are now TRACKED
    res = gh.generate(repo, mode="architect", slug=slug, repo=".dev-knowledge",
                      date="2026-07-04", bundle_root=root, allow_suffix=True, assemble=False)
    assert res.bundle_dir == root / f"{slug}-3"
    # neither collider was touched
    assert (root / slug / "RESIDUAL.md").read_text(encoding="utf-8") == f"committed {slug}\n"
    assert (root / f"{slug}-2" / "RESIDUAL.md").read_text(encoding="utf-8") == f"committed {slug}-2\n"


# --- Destination.branch is the BOOT DESTINATION, never the generation branch ------
# Field defect witnessed 2026-07-31: the 2026-08-01 bundle shipped
# `Destination · branch docs/2026-08-01-handoff-skeleton` — its own GENERATION branch, which
# MERGE IS ATOMIC then deleted at finalize, so P3 compared live `main` against a branch that no
# longer existed and blocked onboarding on a bundle that was otherwise clean. HANDOFF_PROCESS
# §13(c″) (v6.0.1) defines the field as the BOOT DESTINATION — "where the seat lands when it
# boots, not where its work is eventually committed" — and makes `main` legal for a primary-tree
# seat. Root cause is the LESSONS 2026-07-31 shape: ONE token ({{BRANCH}}) answering TWO different
# questions — "which branch was I generated on?" (Generated-at: correct) and "where does the seat
# boot?" (Destination: wrong). Both halves are pinned below so a future merge back to one token
# fails loudly.

def _destination_branch(boot_text: str) -> str:
    """The Destination row's branch field — P3's second operand."""
    row = next((ln for ln in boot_text.splitlines() if ln.startswith("| **Destination**")), "")
    assert row, "boot header carries no Destination row"
    m = re.search(r"branch `([^`]+)`", row)
    assert m, f"Destination row carries no branch field: {row[:160]}"
    return m.group(1)


def test_destination_branch_is_the_boot_destination_not_the_generation_branch(tmp_path):
    """A bundle generated ON a feature branch must still send the seat to its BOOT DESTINATION.

    Reproduces the field defect directly: generate while checked out on a `docs/…` lane branch —
    the branch a finalize merge deletes — and assert the Destination row does NOT name it.
    """
    repo = _stub_repo(tmp_path)
    _git_init_commit(repo)
    gen_branch = "docs/2026-08-01-handoff-skeleton"      # dies at finalize (MERGE IS ATOMIC)
    subprocess.run(["git", "checkout", "-q", "-b", gen_branch],
                   cwd=repo, check=True, capture_output=True)

    res = gh.generate(repo, mode="architect", slug="0000-00-00-dest", repo=".dev-knowledge",
                      date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    boot = (res.bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")

    dest = _destination_branch(boot)
    assert dest != gen_branch, (
        "Destination.branch names the GENERATION branch — the branch finalize deletes; "
        "P3 then compares live `main` against a dead ref and blocks a clean bundle")
    assert dest == "main", f"primary-tree seat must boot on `main` (§13(c″)); got `{dest}`"


def test_generated_at_line_still_names_the_generation_branch(tmp_path):
    """The OTHER question keeps its own answer: the `Generated at` pointer is explicitly the
    branch that was checked out at cut time, and must NOT be collapsed into the boot destination.
    """
    repo = _stub_repo(tmp_path)
    _git_init_commit(repo)
    gen_branch = "docs/2026-08-01-handoff-skeleton"
    subprocess.run(["git", "checkout", "-q", "-b", gen_branch],
                   cwd=repo, check=True, capture_output=True)

    res = gh.generate(repo, mode="architect", slug="0000-00-00-genat", repo=".dev-knowledge",
                      date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    boot = (res.bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")

    genat = next((ln for ln in boot.splitlines() if ln.startswith("| **Generated at**")), "")
    assert genat, "boot header lost its `Generated at` row"
    assert gen_branch in genat, (
        "`Generated at` no longer names the generation branch — the two questions were "
        "collapsed onto the boot destination instead of separated")


# --- seal identity: internal slug == final directory name ([#473] half B) ----
#
# `--allow-suffix` diverts the write to `<slug>-<n>`, but the render tokens were built from
# the REQUESTED slug, so every internal self-reference — the HANDOFF_BOOT Slug field, the
# PROBES P0c/P3/P8 locators, PASTE_THIS's embedded command — named the SIBLING. The bundle
# sealed pointing at a different directory, and `verify_handoff_probes` could not see it:
# the un-suffixed path EXISTS (it is the sibling), so every row resolved pass.
# Binding is not identity.


def _tracked_repo(tmp_path):
    """A stub repo whose first bundle is git-TRACKED, so a second generate() at the same slug
    trips the RM-8 refusal and `allow_suffix` diverts to `-2` (the real-world path)."""
    repo = _stub_repo(tmp_path)
    root = repo / "docs" / "handoffs"
    gh.generate(repo, mode="architect", slug="2026-08-01-t", repo=".dev-knowledge",
                date="2026-08-01", bundle_root=root, assemble=False)
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e.com",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e.com"}
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "seed"]):
        p = subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True, env=env)
        assert p.returncode == 0, f"git {args}: {p.stderr}"
    return repo, root


@pytest.mark.skipif(shutil.which("git") is None, reason="git not in PATH")
def test_suffixed_bundle_derives_every_internal_reference_from_its_final_directory(tmp_path):
    """THE DEFECT. Generate into a tracked slug with --allow-suffix; the bundle lands in `-2`
    and NOTHING inside it may still name the un-suffixed sibling."""
    repo, root = _tracked_repo(tmp_path)

    res = gh.generate(repo, mode="architect", slug="2026-08-01-t", repo=".dev-knowledge",
                      date="2026-08-01", bundle_root=root, assemble=False, allow_suffix=True)

    assert res.bundle_dir.name == "2026-08-01-t-2", "fixture premise: the write diverted"
    boot = (res.bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    assert "`2026-08-01-t-2`" in boot, "the Slug field must name the FINAL directory"
    probes = (res.bundle_dir / "PROBES.md").read_text(encoding="utf-8")
    assert "docs/handoffs/2026-08-01-t-2/" in probes, "P0c/P3/P8 locators must be suffixed"
    for f in res.bundle_dir.iterdir():
        body = f.read_text(encoding="utf-8")
        assert "docs/handoffs/2026-08-01-t/" not in body, f"{f.name} still names the sibling"


@pytest.mark.skipif(shutil.which("git") is None, reason="git not in PATH")
def test_suffixed_bundle_probes_resolve_against_their_own_directory(tmp_path):
    """The end the tokens serve: the generated bundle's own probe manifest binds — verified by
    the real validator, not by string-matching alone."""
    repo, root = _tracked_repo(tmp_path)
    res = gh.generate(repo, mode="architect", slug="2026-08-01-t", repo=".dev-knowledge",
                      date="2026-08-01", bundle_root=root, assemble=False, allow_suffix=True)

    results = vhp.verify(res.bundle_dir, repo_root=repo)
    assert results, "the generated bundle must carry probes"
    assert not [r for r in results if r.status == "fail"], [r.detail for r in results]
    assert not [r for r in results if r.locator_rebased], \
        "a freshly-generated bundle must need NO rebase — its locators are already its own"


def test_seal_refuses_a_bundle_whose_internal_slug_mismatches_its_directory(tmp_path):
    """The gate that makes the class unsealable (residual_completeness precedent): the system
    already refuses plausible-but-wrong artifacts, and a self-mislabelled bundle is one."""
    repo = _stub_repo(tmp_path)
    root = repo / "docs" / "handoffs"
    res = gh.generate(repo, mode="architect", slug="2026-08-01-t", repo=".dev-knowledge",
                      date="2026-08-01", bundle_root=root, assemble=False)
    boot = res.bundle_dir / "HANDOFF_BOOT.md"
    boot.write_text(boot.read_text(encoding="utf-8")
                    .replace("`2026-08-01-t`", "`2026-08-01-t-9`"), encoding="utf-8")

    with pytest.raises(gh.BundleIdentityError) as exc:
        gh.verify_seal_identity(res.bundle_dir)
    assert "2026-08-01-t-9" in str(exc.value) and "2026-08-01-t" in str(exc.value)


def test_seal_identity_accepts_a_correctly_labelled_bundle(tmp_path):
    """Negative control — a normal generation seals without complaint."""
    repo = _stub_repo(tmp_path)
    res = gh.generate(repo, mode="architect", slug="2026-08-01-t", repo=".dev-knowledge",
                      date="2026-08-01", bundle_root=repo / "docs" / "handoffs", assemble=False)
    gh.verify_seal_identity(res.bundle_dir)      # must not raise


@pytest.mark.skipif(shutil.which("git") is None, reason="git not in PATH")
def test_generation_itself_runs_the_seal_gate(tmp_path):
    """The gate is wired INTO generate(), not merely available to call — otherwise the defect
    class can seal again through the exact door it used the first time."""
    repo, root = _tracked_repo(tmp_path)
    calls = []
    real = gh.verify_seal_identity

    def spy(bundle_dir):
        calls.append(bundle_dir)
        return real(bundle_dir)

    gh.verify_seal_identity = spy
    try:
        res = gh.generate(repo, mode="architect", slug="2026-08-01-t", repo=".dev-knowledge",
                          date="2026-08-01", bundle_root=root, assemble=False, allow_suffix=True)
    finally:
        gh.verify_seal_identity = real
    assert res.bundle_dir in calls, "generate() must seal-gate the bundle it just wrote"


# --- the two boot/cut invariants (ARC-HANDOFF-ENGINE step 2) ----------------------
# WINDOW = BATCH (PLAYBOOK Ch8; ADR-110 §Rhythm) and the no-leftovers round-trip
# (CLAUDE.md §5 rule 9) were doctrine with no organ behind them at the generation site.
# A bundle cut mid-batch describes a tree nobody has integrated yet, so the successor boots
# against a manifest the rest of the batch is about to invalidate — the failure is silent,
# and the artifact is immutable once committed. Both refusals fire BEFORE anything is written.


class _FakeBatch:
    """The two OpenBatch fields the refusal names. Structural stand-in so these tests do not
    need a committed manifest — batch_manifest's own suite owns the resolution semantics."""

    def __init__(self, batch="9", path="docs/audits/2026-01-01-technical-batch-9-manifest.md",
                 closed_by="docs/audits/2026-01-01-technical-batch-9-packet.md"):
        self.batch, self.path, self.closed_by = batch, path, closed_by


def test_generation_refuses_while_a_batch_manifest_declares_an_open_batch(tmp_path, monkeypatch):
    """WINDOW = BATCH, enforced. A cut taken while a batch is open seals a bundle whose state
    the batch is still moving; handoffs happen at boundaries only."""
    repo = _stub_repo(tmp_path)
    monkeypatch.setattr(gh, "_open_batches", lambda _root: [_FakeBatch()])
    with pytest.raises(gh.OpenBatchError) as exc:
        gh.generate(repo, mode="architect", slug="0000-00-00-midbatch", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    msg = str(exc.value)
    # Naming the manifest AND its closer is the actionable half: "a batch is open" without
    # the two paths is a message the operator cannot act on.
    assert "batch 9" in msg
    assert "2026-01-01-technical-batch-9-manifest.md" in msg
    assert "2026-01-01-technical-batch-9-packet.md" in msg


def test_open_batch_refusal_writes_nothing(tmp_path, monkeypatch):
    """The refusal precedes creation. A half-written bundle directory left behind by a refused
    cut is itself a leftover, and would then be the untracked in-flight target RM-8 sanctions."""
    repo = _stub_repo(tmp_path)
    monkeypatch.setattr(gh, "_open_batches", lambda _root: [_FakeBatch()])
    with pytest.raises(gh.OpenBatchError):
        gh.generate(repo, mode="architect", slug="0000-00-00-midbatch", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    assert not (repo / "docs" / "handoffs" / "0000-00-00-midbatch").exists()


def test_generation_proceeds_when_no_batch_is_open(tmp_path):
    """Negative control — the overwhelmingly common state costs one read and refuses nothing."""
    repo = _stub_repo(tmp_path)
    assert gh._open_batches(repo) == []
    res = gh.generate(repo, mode="architect", slug="0000-00-00-clear", repo=".dev-knowledge",
                      date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    assert (res.bundle_dir / "HANDOFF_BOOT.md").exists()


def test_open_batch_reader_is_the_shared_batch_manifest_organ():
    """One definition of "a batch is open". A second, generator-local notion would drift from
    the one the audit gate reads, and the two would disagree exactly when it mattered."""
    src = (_REPO / "scripts" / "gen_handoff.py").read_text(encoding="utf-8")
    assert "batch_manifest" in src and "open_batches" in src


@pytest.mark.skipif(shutil.which("git") is None, reason="git not in PATH")
def test_generation_refuses_a_linked_worktree_and_names_it(tmp_path, monkeypatch):
    """Boundary hygiene, leg 1. `git worktree list` == primary only is the batch protocol's own
    refuse-to-finish item; a bundle cut over an un-torn-down lane inherits that lane's state.

    A REAL repo, with only the reader stubbed: a bare `.git` directory is not a repo, and
    `_tracked_under` refuses status-unknown before this leg is ever reached."""
    repo = _stub_repo(tmp_path)
    _git_init_commit(repo)
    monkeypatch.setattr(gh, "_linked_worktrees",
                        lambda _root: [r"C:\repo\.claude\worktrees\lane-a"])
    monkeypatch.setattr(gh, "_stash_entries", lambda _root: [])
    with pytest.raises(gh.BoundaryHygieneError) as exc:
        gh.generate(repo, mode="architect", slug="0000-00-00-wt", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    assert "lane-a" in str(exc.value)


@pytest.mark.skipif(shutil.which("git") is None, reason="git not in PATH")
def test_generation_refuses_a_nonempty_stash_and_names_it(tmp_path, monkeypatch):
    """Boundary hygiene, leg 2, and the one the other checks structurally cannot cover:
    `refs/stash` lives in the COMMON git dir, so a lane's stash survives every worktree- and
    branch-shaped teardown (batch-1 F4)."""
    repo = _stub_repo(tmp_path)
    _git_init_commit(repo)
    monkeypatch.setattr(gh, "_linked_worktrees", lambda _root: [])
    monkeypatch.setattr(gh, "_stash_entries",
                        lambda _root: ["stash@{0}: WIP on main: 1234567 lane-b half-edit"])
    with pytest.raises(gh.BoundaryHygieneError) as exc:
        gh.generate(repo, mode="architect", slug="0000-00-00-stash", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    assert "stash@{0}" in str(exc.value)


@pytest.mark.skipif(shutil.which("git") is None, reason="git not in PATH")
def test_boundary_hygiene_names_every_leftover_not_just_the_first(tmp_path, monkeypatch):
    """Reporting one leftover invites a fix-and-retry loop that reveals the next one; the
    operator gets the whole list in one refusal."""
    repo = _stub_repo(tmp_path)
    _git_init_commit(repo)
    monkeypatch.setattr(gh, "_linked_worktrees", lambda _root: ["/w/lane-a", "/w/lane-b"])
    monkeypatch.setattr(gh, "_stash_entries", lambda _root: ["stash@{0}: WIP"])
    with pytest.raises(gh.BoundaryHygieneError) as exc:
        gh.generate(repo, mode="architect", slug="0000-00-00-many", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    msg = str(exc.value)
    assert "lane-a" in msg and "lane-b" in msg and "stash@{0}" in msg


def test_boundary_hygiene_is_skipped_outside_a_git_repo(tmp_path):
    """Degrade contract, matching `_tracked_under`: not a git repo -> nothing can be provisioned
    or stashed -> generation proceeds. `_stub_repo` is never `git init`ed."""
    repo = _stub_repo(tmp_path)
    assert not (repo / ".git").exists()
    res = gh.generate(repo, mode="architect", slug="0000-00-00-nogit-h", repo=".dev-knowledge",
                      date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    assert (res.bundle_dir / "HANDOFF_BOOT.md").exists()


def test_boundary_hygiene_refuses_when_git_cannot_answer(tmp_path, monkeypatch):
    """The other half of that degrade, and the direction RM-8 already ruled: a git that is
    PRESENT but errors leaves hygiene UNKNOWN, and an unknown boundary is not a clean one."""
    repo = _stub_repo(tmp_path)
    (repo / ".git").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(gh, "_git_status", lambda *a, **k: (False, ""))
    with pytest.raises(gh.BoundaryHygieneError) as exc:
        gh.assert_boundary_hygiene(repo)
    assert "could not be determined" in str(exc.value)


@pytest.mark.skipif(shutil.which("git") is None, reason="git not in PATH")
def test_boundary_hygiene_reads_the_real_probes_in_a_real_repo(tmp_path):
    """Wiring, not stubs: against a real single-worktree, stash-free repo both readers answer
    empty and generation proceeds — so the GREEN above is not an artefact of monkeypatching."""
    repo = _stub_repo(tmp_path)
    _git_init_commit(repo)
    assert gh._linked_worktrees(repo) == []
    assert gh._stash_entries(repo) == []
    res = gh.generate(repo, mode="architect", slug="0000-00-00-realgit", repo=".dev-knowledge",
                      date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False)
    assert (res.bundle_dir / "HANDOFF_BOOT.md").exists()


@pytest.mark.skipif(shutil.which("git") is None, reason="git not in PATH")
def test_linked_worktrees_excludes_the_primary(tmp_path):
    """`git worktree list` always lists the primary first; counting it as a leftover would
    refuse every cut ever taken. The primary is the baseline, not a finding."""
    repo = _stub_repo(tmp_path)
    _git_init_commit(repo)
    ok, out = gh._git_status(repo, "worktree", "list", "--porcelain")
    assert ok and out.count("worktree ") == 1      # the primary, and only the primary
    assert gh._linked_worktrees(repo) == []


# --- R2: the generated Standing-vs-NEW attribution frame --------------------
#
# 47/86 bundles hand-authored this paragraph, averaging 1,847 B, saying the same thing in
# different words every window (2026-08-26 handoff census, item R2/b1). What is generated here
# is the ATTRIBUTION, never a value — the anti-bluff dogfood above still governs, and these
# tests exist so the block cannot quietly acquire one.

# The banned shapes: a ship-gate verdict, a WARN/disposition count, a `[stale]` line, a sha, or
# a backlog id. A frame that starts carrying one of these has become an answer.
_ANSWER_SHAPES = (
    re.compile(r"\bGREEN\b|\bRED\b"),
    re.compile(r"\[stale\]"),
    re.compile(r"\b[0-9a-f]{7,}\b"),
    re.compile(r"#\d+"),
    re.compile(r"\b\d+\s+(?:WARN|warn|dispositioned|organs?|entries)\b"),
)


def test_standing_vs_new_bindings_name_live_all_checks_members():
    """The manifest is CURATED, so this is the guard that keeps it from rotting into naming a
    retired organ — the failure mode the block's own scope note would otherwise hide.

    Reads `audit_checks.registry.CHECK_ORDER` rather than `audit.ALL_CHECKS` deliberately:
    `gen_handoff.collect_hints` inserts the STUB repo's `scripts/` at `sys.path[0]` and imports
    `audit` from there, so by the time this test runs `sys.modules["audit"]` is a one-line stub
    whose ALL_CHECKS is empty — and a test that read it would pass vacuously against nothing.
    CHECK_ORDER is the same registry as a list of names, and test_audit_parallel.py pins the
    two in agreement."""
    from audit_checks.registry import CHECK_ORDER
    live = {name.removeprefix("check_") for name in CHECK_ORDER}
    named = {organ for organ, _b, _w in gh._DRIFT_ORGAN_BINDINGS}
    assert named <= live, f"binding manifest names non-ALL_CHECKS organ(s): {named - live}"


def test_standing_vs_new_carries_no_answer_value():
    """THE contract for R2, run against the LIVE repo so it is evidence about the real block
    and not about a fixture: three lists of names, and not one value among them."""
    block = gh.standing_vs_new(_REPO)
    hits = [rx.pattern for rx in _ANSWER_SHAPES if rx.search(block)]
    assert hits == [], f"the generated frame carries answer-shaped text: {hits}"


def test_standing_vs_new_partitions_every_manifest_organ_exactly_once():
    block = gh.standing_vs_new(_REPO)
    for organ, _b, _w in gh._DRIFT_ORGAN_BINDINGS:
        assert block.count(f"`{organ}`") == 1, f"{organ} listed {block.count(organ)} times"
    for heading in ("Dispositioned by the register", "Dispositioned by absence",
                    "NEW-and-undispositioned", "Window"):
        assert heading in block


def test_standing_vs_new_degrades_loudly_when_the_window_is_unresolvable(tmp_path):
    """A generator that cannot compute the window says so. It never guesses a range, and it
    never falls through to a frame computed against nothing — which would file every organ as
    NEW and read as an alarm."""
    block = gh.standing_vs_new(_stub_repo(tmp_path))     # no git history at all
    assert "Window unresolved" in block
    assert "NEW-and-undispositioned" not in block


def test_standing_vs_new_degrades_when_the_register_is_unreadable(tmp_path, monkeypatch):
    """An empty register would silently reclassify every dispositioned organ as NEW — worse
    than no frame, so the frame is withheld instead."""
    monkeypatch.setattr(gh, "_window", lambda root: ("2026-01-01-prev", ["scripts/audit.py"]))
    block = gh.standing_vs_new(_stub_repo(tmp_path) / "nonexistent")
    assert "register unreadable" in block


def test_touched_treats_git_history_bindings_as_always_in_a_non_empty_window():
    """no_ff_merges and journal_spine_anchor fire against the spine, not a file. Fail toward
    NEW: put the organ in front of the seat rather than quietly filing it as standing."""
    assert gh._touched((gh._HISTORY_BINDING,), ["any/file.md"]) is True
    assert gh._touched((gh._HISTORY_BINDING,), []) is False


def test_touched_matches_dir_prefixes_and_exact_paths():
    assert gh._touched(("scripts/",), ["scripts/audit.py"]) is True
    assert gh._touched(("scripts/",), ["scriptsfoo/audit.py"]) is False
    assert gh._touched(("BACKLOG.md",), ["BACKLOG.md"]) is True
    assert gh._touched(("BACKLOG.md",), ["docs/BACKLOG.md"]) is False


def test_generated_residual_carries_the_frame_and_the_narrowed_fill_in(tmp_path):
    """End-to-end: the block reaches RESIDUAL.md §1, and the hand region below it now asks for
    ONE judgment — which NEW flag is a decision rather than a defect."""
    residual = (_gen(tmp_path).bundle_dir / "RESIDUAL.md").read_text(encoding="utf-8")
    assert "{{STANDING_VS_NEW}}" not in residual        # the token was substituted
    assert "Standing vs NEW" in residual
    assert "DECISION rather than a defect" in residual


def test_generated_residual_fill_in_regions_stay_recognised_as_unfilled(tmp_path):
    """residual_completeness stays green: the narrowed placeholder keeps the `_(fill: …)_`
    shape its scanner recognises, so a cold bundle still reports its regions as unfilled
    instead of a reworded placeholder passing as authored prose."""
    import validate_residual_completeness as vrc
    residual = _gen(tmp_path).bundle_dir / "RESIDUAL.md"
    regions = {u.region for u in vrc.scan_file(residual, "RESIDUAL.md")}
    assert "driftflags" in regions


# --- R5: the forms card renders the ruled verb, it does not copy it ---------

def test_dispatch_form_renders_the_line_ch8_rules():
    """The forms card carries a literal a seat TYPES, which a pointer cannot serve — but a
    COPIED command is what STANDING_RULINGS §V ruled on. Rendering resolves both."""
    import dispatch_surface as ds
    block = gh.dispatch_form(_REPO)
    assert block.startswith("```") and block.rstrip().endswith("```")
    for line in ds.ruled_form(_REPO):
        assert line in block


def test_dispatch_form_degrades_to_a_pointer_not_a_remembered_command(tmp_path):
    """A stale copy that renders confidently is the failure mode, so the degrade path names the
    table instead of naming a command."""
    block = gh.dispatch_form(tmp_path)
    assert "could not be rendered" in block
    assert "SOLE literal-command site" in block
    assert "dispatch <" not in block


def test_generated_boot_points_the_launch_form_at_the_launcher(tmp_path):
    """LANE-5A-9 (ruling O-5, 2026-09-23): the forms card no longer renders PLAYBOOK Ch8's
    dispatch table, which stopped describing how lanes launch; it points at the launcher's own
    --help. End-to-end through the stub repo, so no raw token is left behind either."""
    boot = (_gen(tmp_path).bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    assert "{{DISPATCH_FORM}}" not in boot
    assert "scripts/dispatch.py launch --help" in boot
    assert "SOLE literal-command site" not in boot


def test_template_holds_no_second_copy_of_the_dispatch_command():
    """The R5 contract, re-pointed by LANE-5A-9: the forms card carries no copied launch verb —
    it names the launcher and its --help. A fenced `dispatch …` line reappearing in the
    template is the regression."""
    import dispatch_surface as ds
    tmpl = (_REPO / "templates" / "handoff" / "v5" / "HANDOFF_BOOT.md.tmpl").read_text(
        encoding="utf-8")
    verb = ds.ruled_verb(_REPO)
    assert "{{DISPATCH_FORM}}" not in tmpl
    assert "scripts/dispatch.py launch --help" in tmpl
    assert not any(ln.split()[:1] == [verb] for ln in ds.fenced_lines(tmpl))


# --- FM-4: the FUNNEL HEALTH block (golden shape) ---------------------------
#
# The block is DERIVED, never recomputed: `gen_handoff` imports FM-2's derivation module and
# reads the eleven numbers off it. These tests pin the block's SHAPE — field names, their order,
# the numbers-only format, the delimiters — and deliberately NOT tonight's numbers, which move
# every day the funnel does. The FM-2 coupling is exercised through a fake module injected into
# `sys.modules`, so the shape is provable without a live corpus.
#
# THE SHAPE TESTS ARE NOT THE COUPLING TESTS, and `[#619]` is why the distinction is spelled out
# here. Every case below passed for the whole life of the dead coupling: the block rendered six
# labels in the pinned order with the pinned delimiters, and each one carried `unavailable`
# because not one of the six attributes existed on FM-2's measurement. A fake measurement cannot
# catch that — it answers to whatever names the fake was given. The coupling is measured against
# the LIVE module, by the three cases under "ANTI-DRIFT" at the end of this section.

# GOLDEN LITERALS. Written out rather than imported from `gen_handoff` on purpose: a test that
# spells its expectation as `gh._FUNNEL_BEGIN` re-derives the shape from the code it is meant to
# constrain and passes through any rename of it (terra HIGH, 2026-08-29). These strings ARE the
# contract; changing one is meant to cost a deliberate test edit.
_GOLDEN_BEGIN = "<!-- FUNNEL-HEALTH:BEGIN (generated by gen_handoff — do not edit) -->"
_GOLDEN_END = "<!-- FUNNEL-HEALTH:END -->"
_GOLDEN_HEADING = "## FUNNEL HEALTH (generated — numbers only)"
_GOLDEN_SOURCE_PREFIX = "source: scripts/funnel_lifecycle.py::measure (FM-2)"

_FUNNEL_LABELS = (
    "intakes live",
    "intakes archived",
    "intakes READY",
    "ADRs live",
    "rows",
    "rows post-cutoff",
    "leg a1 intakes terminal-unarchived",
    "leg a2 intakes ACCEPTED, every named row terminal",
    "leg b ADRs terminal-unarchived",
    "leg c rows post-cutoff, provenance unresolved",
    "leg d READY intakes past threshold",
)

# FM-2's leg names, as LITERALS — same doctrine as the golden strings above. The fake must not
# import the real constants: a fake that re-derives its names from the module under test would
# follow a rename and keep passing, which is exactly how the dead coupling stayed green.
# `test_funnel_fields_cover_fm2s_whole_int_and_leg_surface` is what binds these to the real ones.
_LEG_LITERALS = ("terminal-not-archived", "accepted-rows-terminal", "adr-terminal-not-archived",
                 "row-provenance-unresolved", "ready-past-threshold")


class _FakeMeasurement:
    """Stands in for FM-2's `measure()` result — the int fields plus `by_leg`."""
    live_intakes = 55
    archived_intakes = 10
    ready_intakes = 19
    live_adrs = 88
    rows = 349
    post_cutoff_rows = 13

    #: leg name -> how many violations to answer with. `by_leg` returns a LIST because the
    #: adapter takes its `len()`, exactly as FM-2's does.
    _counts = dict(zip(_LEG_LITERALS, (7, 0, 3, 2, 1), strict=True))

    def by_leg(self, leg):
        return ["violation"] * self._counts.get(leg, 0)


def _fake_fm2_module():
    """A module-shaped fake carrying FM-2's `measure` AND its `LEG_*` constants.

    The constants are not decoration: the adapter validates every leg key against them at render
    time, so a fake without them renders every leg field `unavailable` and the shape tests would
    measure half a block.
    """
    import types
    mod = types.ModuleType(gh._FUNNEL_MODULE)
    mod.measure = lambda repo_root: _FakeMeasurement()          # noqa: ARG005
    for name, leg in zip(("LEG_A1", "LEG_A2", "LEG_B", "LEG_C", "LEG_D"),
                         _LEG_LITERALS, strict=True):
        setattr(mod, name, leg)
    return mod


@pytest.fixture
def fm2(monkeypatch):
    """Install a fake FM-2 derivation module under the name gen_handoff imports."""
    import sys
    mod = _fake_fm2_module()
    monkeypatch.setitem(sys.modules, gh._FUNNEL_MODULE, mod)
    monkeypatch.setitem(sys.modules, f"scripts.{gh._FUNNEL_MODULE}", mod)
    return mod


def _block_body(block):
    """The non-blank lines between the golden delimiters, delimiters excluded."""
    lines = block.splitlines()
    assert lines[0] == _GOLDEN_BEGIN, lines[0]
    assert lines[-1] == _GOLDEN_END, lines[-1]
    return [ln for ln in lines[1:-1] if ln.strip()]


def test_funnel_health_block_shape_is_pinned(fm2):
    """GOLDEN. Delimiters, heading, source line, field names, their ORDER and the numbers-only
    format — every one of them as a LITERAL. Not tonight's values, which move every day."""
    body = _block_body(gh.funnel_health_block(_REPO))
    assert body[0] == _GOLDEN_HEADING
    assert body[1] == _GOLDEN_SOURCE_PREFIX or body[1].startswith(_GOLDEN_SOURCE_PREFIX + " — ")
    fields = body[2:]
    assert len(fields) == len(_FUNNEL_LABELS), fields
    for line, label in zip(fields, _FUNNEL_LABELS, strict=True):
        assert re.fullmatch(rf"{re.escape(label)}: (?:\d+|unavailable)", line), line


def test_golden_literals_and_the_production_constants_agree():
    """The other half of the golden: the literals above are the shipped strings. Without this
    the literals could drift into describing a block nothing emits."""
    assert gh._FUNNEL_BEGIN == _GOLDEN_BEGIN
    assert gh._FUNNEL_END == _GOLDEN_END
    assert [label for label, _kind, _key in gh._FUNNEL_FIELDS] == list(_FUNNEL_LABELS)


def test_funnel_health_block_carries_no_verdict_and_no_sha(fm2):
    """ANTI-BLUFF. Numbers only: no verdict word, no sha, no backlog id anywhere in the block."""
    block = gh.funnel_health_block(_REPO)
    for rx in (re.compile(r"\b(?:GREEN|RED|PASS|FAIL|WARN|healthy|degraded)\b"),
               re.compile(r"\b[0-9a-f]{7,}\b"),
               re.compile(r"#\d+")):
        assert not rx.search(block), f"{rx.pattern} matched: {block}"


def test_funnel_source_prefers_the_package_qualified_module(monkeypatch):
    """H3. The bare name resolves against the whole of `sys.path`; `scripts.` names this repo or
    nothing. A same-named module installed elsewhere must NOT have its numbers published under
    FM-2's name, so the package-qualified spelling is tried first."""
    import sys
    import types

    class _Ours:
        """Answers 1 to everything, so `theirs`' numbers are recognisable if they leak in."""

        def by_leg(self, leg):                                  # noqa: ARG002
            return ["violation"]

    for _label, kind, key in gh._FUNNEL_FIELDS:
        if kind == gh._FUNNEL_ATTR:
            setattr(_Ours, key, 1)
    theirs = _fake_fm2_module()
    ours = types.ModuleType(f"scripts.{gh._FUNNEL_MODULE}")
    ours.measure = lambda repo_root: _Ours()                    # noqa: ARG005
    for name, leg in zip(("LEG_A1", "LEG_A2", "LEG_B", "LEG_C", "LEG_D"),
                         _LEG_LITERALS, strict=True):
        setattr(ours, name, leg)
    monkeypatch.setitem(sys.modules, gh._FUNNEL_MODULE, theirs)
    monkeypatch.setitem(sys.modules, f"scripts.{gh._FUNNEL_MODULE}", ours)
    values, note = gh._funnel_health_numbers(_REPO)
    assert note == ""
    # ours (all 1s), never theirs (55/10/19/88/349/13 and 7/0/3/2/1)
    assert set(values.values()) == {"1"}, values


def test_exactly_one_public_funnel_health_emitter():
    """A1 (architect, 2026-08-29): FM-4 exposes EXACTLY ONE public funnel-health emitter.

    This is the assertion that actually holds the A1 ruling. FM-5 resolves FM-4's emitter by
    CAPABILITY over `dir(gen_handoff)`, and `dir()` does not consult `__all__` — so the thing
    that keeps the resolution unambiguous is that the other two callables are `_`-private, and
    nothing but a test stops a later hand from making one public again.

    FM-5's regex is IMPORTED, never re-typed here: a copy would let the two drift and this test
    would keep passing while the resolution it guards started refusing.
    """
    import governance_health as gh5

    public = [n for n in dir(gh) if not n.startswith("_") and callable(getattr(gh, n, None))]
    emitters = sorted(n for n in public if gh5.FM4_CALLABLE_RE.match(n))
    assert emitters == ["funnel_health_block"], (
        f"FM-5 resolves FM-4's emitter by capability and refuses on ambiguity; "
        f"expected exactly one public match, got {emitters}"
    )


def test_fm5_resolves_the_ruled_emitter():
    """The ruling discharged end-to-end: FM-5 resolves, and names the callable A1 ruled.

    The companion to the test above — that one pins the module's shape, this one pins the
    CONSUMER's verdict, which is what the ambiguity was actually costing.
    """
    import governance_health as gh5

    src = gh5.resolve_fm4_emitter()
    assert src.available, src.reason
    assert src.dotted == "gen_handoff:funnel_health_block", src.dotted


def test_the_privatised_delegates_are_still_reachable_and_wired():
    """Privatising is a rename, NOT a deletion — the block still delegates to both.

    Guards the failure this change could plausibly have caused: a rename that left
    `funnel_health_block` computing its own numbers, which would re-create the second
    implementation the whole FM-2 coupling exists to remove.
    """
    assert callable(gh._funnel_health_numbers)
    assert callable(gh._write_funnel_health)
    assert "_funnel_health_numbers(repo_root)" in inspect.getsource(gh.funnel_health_block)


def test_funnel_health_names_fm2_as_its_source(fm2):
    """ONE TRUTH: the block says where its numbers came from, by module path."""
    assert gh._FUNNEL_MODULE in gh.funnel_health_block(_REPO)


def test_funnel_health_degrades_honestly_when_fm2_is_absent(monkeypatch):
    """FM-2 is unreachable. The block must render `unavailable`, never a fabricated number —
    a second implementation of "is this intake consumed?" is the failure this batch removes."""
    monkeypatch.setattr(gh, "_load_funnel_measure", lambda: (None, None, "not importable"))
    fields = _block_body(gh.funnel_health_block(_REPO))[2:]
    assert len(fields) == len(_FUNNEL_LABELS)
    assert all(ln.endswith(": unavailable") for ln in fields), fields


def test_a_renamed_leg_renders_unavailable_and_never_a_false_zero(monkeypatch):
    """`[#619]`, the render-time half. `by_leg` FILTERS a list, so it answers `[]` for a leg it
    has never heard of — indistinguishable from `[]` for a leg with no violations. Rendering
    that as `0` would publish a confident false clean, which is strictly worse than
    `unavailable`. So the adapter validates every leg key against FM-2's own `LEG_*` constants
    and degrades the ones that do not resolve.
    """
    import sys

    mod = _fake_fm2_module()
    mod.LEG_C = "row-provenance-unresolved-RENAMED"     # FM-2 renames one leg
    monkeypatch.setitem(sys.modules, gh._FUNNEL_MODULE, mod)
    monkeypatch.setitem(sys.modules, f"scripts.{gh._FUNNEL_MODULE}", mod)

    values, note = gh._funnel_health_numbers(_REPO)
    assert values["leg c rows post-cutoff, provenance unresolved"] == "unavailable"
    assert "row-provenance-unresolved" in note
    # and ONLY that one degrades — the other ten still carry their numbers
    assert sum(v == "unavailable" for v in values.values()) == 1, values


# --- FM-4: ANTI-DRIFT — measured against the LIVE FM-2 module, never a fake ---
#
# `[#619]`: FM-4 read six attribute names off a measurement that exposed none of them. The
# intersection was EMPTY for the whole life of the block, every field rendered `unavailable` in
# every bundle ever cut, and every shape test above stayed green throughout — because a fake
# measurement answers to whatever names the fake was given. These three cases are the ones that
# could have caught it, and the only ones in this section that import the real module.

def _live_fm2():
    import funnel_lifecycle
    return funnel_lifecycle


def test_funnel_fields_cover_fm2s_whole_int_and_leg_surface():
    """THE COUPLING, asserted as set equality BOTH WAYS against the live module.

    The ruled rule (`docs/audits/2026-08-29-technical-batchd-a-619-fm-coupling-packet.md` §2.7):
    *FM-4 renders every `int`-typed field of `Measurement`, plus one count per `LEG_*` constant
    — nothing else, nothing less.* Both directions matter and for different reasons: a field
    FM-4 reads that FM-2 does not have renders `unavailable` (the `[#619]` defect), and a field
    FM-2 grows that FM-4 does not read is a number that silently stops being published.

    `int` is read from the ANNOTATIONS, not from a runtime `isinstance` of one sample: a field
    annotated `int | None` (`threshold_days`) can hold an `int` on a lucky tree and `None` on the
    next, and a field that renders `unavailable` on some trees is barred by the repair.
    """
    import typing

    fm2mod = _live_fm2()
    hints = typing.get_type_hints(fm2mod.Measurement)
    want_attrs = {name for name, ann in hints.items() if ann is int}
    want_legs = {v for k, v in vars(fm2mod).items()
                 if k.startswith("LEG_") and isinstance(v, str)}
    assert want_attrs and want_legs, "the live module exposes neither ints nor legs — read it"

    got_attrs = {key for _l, kind, key in gh._FUNNEL_FIELDS if kind == gh._FUNNEL_ATTR}
    got_legs = {key for _l, kind, key in gh._FUNNEL_FIELDS if kind == gh._FUNNEL_LEG}

    assert got_attrs == want_attrs, (
        f"FM-4 reads {sorted(got_attrs)} but FM-2's int surface is {sorted(want_attrs)}")
    assert got_legs == want_legs, (
        f"FM-4 counts {sorted(got_legs)} but FM-2's legs are {sorted(want_legs)}")


def test_funnel_fields_intersect_fm2():
    """The witnessed `[#619]` starting state, pinned as UNREACHABLE.

    The row's own witness command read six attributes off `_FUNNEL_FIELDS`, listed what
    `Measurement` exposed, and measured the intersection EMPTY. This asserts the negation
    directly, so the zero-overlap state cannot be re-reached in silence even if the set-equality
    rule above is later relaxed by a ruling.
    """
    fm2mod = _live_fm2()
    exposed = {n for n in dir(fm2mod.Measurement) if not n.startswith("_")}
    exposed |= {f.name for f in dataclasses.fields(fm2mod.Measurement)}
    read = {key for _l, kind, key in gh._FUNNEL_FIELDS if kind == gh._FUNNEL_ATTR}
    assert read, "FM-4 reads no attribute at all"
    assert read & exposed == read, f"FM-4 reads names FM-2 does not expose: {sorted(read - exposed)}"


@pytest.mark.live_repo
def test_funnel_health_renders_no_unavailable_against_the_live_repo():
    """The done-contract's own words: *no field is left rendering `unavailable` by default*.

    Asserted against the real tree with no fake installed, because that is the only place the
    `[#619]` defect was ever visible — under the `fm2` fixture the block has always rendered
    numbers, including on the day every one of them was `unavailable` in production.
    """
    body = _block_body(gh.funnel_health_block(_REPO))[2:]
    assert len(body) == len(_FUNNEL_LABELS)
    bad = [ln for ln in body if ln.endswith(": unavailable")]
    assert not bad, f"fields the live FM-2 could not derive: {bad}"
    for line in body:
        assert re.fullmatch(r".+: \d+", line), line


@pytest.mark.parametrize("mode", ["architect", "execution"])
def test_assembled_bundle_carries_the_funnel_health_block(tmp_path, fm2, mode):
    """EX-ANTE: the next assembled bundle carries the block."""
    res = _gen(tmp_path, mode=mode, assemble=True)
    text = (res.bundle_dir / "FUNNEL_HEALTH.md").read_text(encoding="utf-8")
    assert _GOLDEN_BEGIN in text and _GOLDEN_END in text
    for label in _FUNNEL_LABELS:
        assert f"{label}: " in text


def test_epic_bundle_carries_the_funnel_health_block(tmp_path, fm2):
    assert (_gen_epic(tmp_path).bundle_dir / "FUNNEL_HEALTH.md").exists()


def test_functional_bundle_stays_one_file(tmp_path, fm2):
    """SCOPED, and the reason is recorded: HANDOFF_PROCESS §16 pins functional mode at ONE
    file, and `protocols/` delta is 0 for this lane — so the block is not emitted there."""
    assert not (_gen_functional(tmp_path).bundle_dir / "FUNNEL_HEALTH.md").exists()


def test_funnel_health_is_regenerated_not_carried(tmp_path, fm2):
    """A STALE BLOCK IS WORSE THAN NONE. A re-generation overwrites the file whole — it is
    never spliced, never appended to, never left in place."""
    res = _gen(tmp_path)
    (res.bundle_dir / "FUNNEL_HEALTH.md").write_text("STALE — a previous window\n",
                                                     encoding="utf-8")
    res2 = _gen(tmp_path)
    text = (res2.bundle_dir / "FUNNEL_HEALTH.md").read_text(encoding="utf-8")
    assert "STALE" not in text
    assert _GOLDEN_BEGIN in text


def test_funnel_health_is_not_folded_into_the_browser_paste(tmp_path, fm2):
    """The answer-free invariant is preserved where it is stated: the browser-visible files
    (BOOT / RESIDUAL / PROBES) and the assembled PASTE_THIS carry no count."""
    res = _gen(tmp_path, assemble=True)
    for name in ("HANDOFF_BOOT.md", "RESIDUAL.md", "PROBES.md", "PASTE_THIS.md"):
        p = res.bundle_dir / name
        if p.exists():
            assert _GOLDEN_BEGIN not in p.read_text(encoding="utf-8"), name


# --- [#643] the ASSEMBLE seam: a refusing child must refuse the cut -----------------
# TERRA HIGH, 2026-09-09 (`REVIEW-lane-v-643-enforcement-debt.md` §2). Leg 2 refuses inside
# `assemble_paste.py`, but `generate()` spawned that child with `check=False`, so on the path
# an operator actually runs -- `gen_handoff --assemble`, which is the DEFAULT -- the refusal
# was swallowed: the command printed `Generated bundle` and exited 0. A gate that announces
# success when it meant to refuse manufactures a FALSE WITNESS, which is worse than no gate --
# the operator walks away holding a receipt that says the cut is clean.
#
# THE DIVISION OF LABOUR, stated so neither half is mistaken for the other. That the CHILD
# refuses -- exit 1, no PASTE_THIS.md, the OPEN carrier named on stderr -- is proven
# end-to-end against a real spawned process in tests/test_assemble_paste.py. What is proven
# HERE is the only thing those tests structurally cannot see: what the PARENT does with the
# code. So these stand in for the child at `_run_assembler` and assert on the parent alone.


def _refusing_assembler(_bundle_dir, **_kwargs):
    """A child assembler that REFUSED: exit 1, nothing assembled. Exit 1 is what
    `assemble_paste.assert_open_carriers_named` actually exits with."""
    return 1


def test_generate_refuses_when_the_assembler_refuses(tmp_path, monkeypatch):
    """RED-first witness for the swallowed exit code: against the seam-only tree this fails
    with DID NOT RAISE, because `generate()` returned a GenResult on a refused assembly.

    `RuntimeError` is the base deliberately, not a weakening -- every refusal this module
    already raises (`BundleCollisionError`, `OpenBatchError`, `BoundaryHygieneError`,
    `PreflightError`) subclasses it, so the `raises` clause names the refusal FAMILY and the
    message assertions below are what pin this particular member.
    """
    monkeypatch.setattr(gh, "_run_assembler", _refusing_assembler)
    repo = _stub_repo(tmp_path)
    with pytest.raises(RuntimeError) as exc:
        gh.generate(repo, mode="architect", slug="0000-00-00-asm", repo=".dev-knowledge",
                    date="2026-09-09", bundle_root=repo / "docs" / "handoffs", assemble=True)
    # The refusal names the bundle it stopped on and the code it read. The operator's next act
    # is to repair THAT bundle and re-run the assembler; a refusal naming neither sends them
    # looking for both.
    assert "0000-00-00-asm" in str(exc.value)
    assert "exit 1" in str(exc.value)


def test_a_clean_assembly_still_returns_normally(tmp_path, monkeypatch):
    """The negative control, and it is not optional: without it the test above proves only
    that the seam CAN refuse, never that a clean cut still completes -- which is the deadlock
    a propagated exit code is the obvious way to introduce."""
    monkeypatch.setattr(gh, "_run_assembler", lambda _bundle_dir, **_kw: 0)
    repo = _stub_repo(tmp_path)
    res = gh.generate(repo, mode="architect", slug="0000-00-00-ok", repo=".dev-knowledge",
                      date="2026-09-09", bundle_root=repo / "docs" / "handoffs", assemble=True)
    assert res.bundle_dir.name == "0000-00-00-ok"


def test_the_cut_command_reports_the_refusal_and_never_prints_generated_bundle(tmp_path,
                                                                               monkeypatch):
    """The operator-facing half, and the one the review named: the standard cut command must
    exit non-zero and must NOT print `Generated bundle`.

    Not a restatement of the first test. This pins that the new refusal reaches `main`'s
    REFUSAL handler -- one `[error]` line, non-zero exit -- rather than escaping as an
    unhandled traceback, which also exits non-zero and would leave the first test green while
    the operator reads a stack trace.

    THE THREE EARLIER REFUSALS ARE STUBBED OUT, and that is load-bearing rather than
    convenient: a stub repo fails `assert_preflight` on its own, so an unstubbed run exits 1
    with an `[error]` line from the WRONG gate and this test passes without the assemble step
    ever running -- the exact `passes for the wrong reason` defect the same review filed as its
    second finding. Each of the three has its own tests elsewhere; none of them is the subject
    here.
    """
    from click.testing import CliRunner

    repo = _stub_repo(tmp_path)
    monkeypatch.setattr(gh, "_run_assembler", _refusing_assembler)
    monkeypatch.setattr(gh, "_REPO_ROOT", repo)
    monkeypatch.setattr(gh, "assert_batch_boundary", lambda *a, **k: None)
    monkeypatch.setattr(gh, "assert_boundary_hygiene", lambda *a, **k: None)
    monkeypatch.setattr(gh, "assert_preflight", lambda *a, **k: [])

    result = CliRunner().invoke(gh.main, ["--slug", "0000-00-00-cli", "--date", "2026-09-09",
                                          "--assemble", "--no-emit-journal"])
    assert result.exit_code != 0, result.output
    assert "Generated bundle" not in result.output
    assert "[error]" in result.output
    # A traceback is not a refusal. `main` converts every refusal in this family to SystemExit
    # carrying the diagnostic; anything else here means the new error missed the handler tuple.
    assert isinstance(result.exception, SystemExit), repr(result.exception)


def test_the_child_argv_carries_no_cold_pass_flag(tmp_path):
    """THE BYPASS THAT IS NOT THERE, pinned so it cannot come back.

    An earlier cut told the assembler it was the cold pass via `--in-generation`. Terra,
    2026-09-09: a flag on a public CLI is a bypass anyone can type, so the post-fill gate could
    be defeated with `assemble_paste.py <filled-bundle> --in-generation`. The assembler now
    DERIVES that state from the residual, which cannot be asserted from outside.

    A negative assertion earns its place only when the thing it forbids was actually shipped
    and removed. This one was.
    """
    argv = gh._assembler_argv(tmp_path / "b")
    assert not [a for a in argv if a.startswith("--")], argv
    assert argv[-1].endswith("b")


def test_the_declared_unattended_invocation_still_cites_the_one_ceiling():
    """[#643] leg e. The unattended suite path is a DECLARED invocation in `pyproject.toml`,
    deliberately not `addopts` -- the interactive path is not changed, because an operator
    watching a run wants every core, and the contract pins that ("Do not change `addopts` for
    the interactive path").

    A declaration nobody checks is the class this whole lane exists to close, so the two claims
    that declaration makes are pinned here rather than trusted: that it clears `addopts`
    structurally rather than by argument ordering, and that its timeout IS
    `gen_handoff.SHIP_GATE_TIMEOUT_S` rather than a second number free to drift from it.

    HONEST LIMIT, stated so this test is not read as more than it is: it pins the DECLARATION,
    not the enforcement. A bare `pytest` still inherits no timeout, and closing that would mean
    changing `addopts`, which this lane is explicitly forbidden to do. Terra raised exactly that
    gap on 2026-09-09 and it is recorded in the lane artifact as an operator call, not silently
    absorbed here.
    """
    text = (_REPO / "pyproject.toml").read_text(encoding="utf-8")
    line = next((ln for ln in text.splitlines()
                 if "pytest" in ln and "--timeout=" in ln and "-o addopts=" in ln), None)
    assert line is not None, "the declared unattended invocation is gone from pyproject.toml"
    assert f"--timeout={gh.SHIP_GATE_TIMEOUT_S}" in line, line
    assert "--group analytics" in line, line     # the measured 44-vs-28 difference


# ------------------------------------------------- the stub repo does not escape this file
#
# `_stub_repo` writes one-line placeholders at the paths the probe-core resolves, INCLUDING
# `scripts/audit.py` (`ALL_CHECKS = []`). `collect_hints` used to put that directory on
# `sys.path` at position 0 and `import audit` from it -- neither undone -- so the stub became
# `sys.modules["audit"]` and the stub's `scripts/` stayed first on the path for the REST OF
# THE PROCESS. Every module collected after this one then got the placeholder.


def test_collect_hints_does_not_leave_the_stub_on_sys_path(tmp_path):
    """The path leak, which is the wider half: five one-line stubs, not just `audit`.

    `_STUB_FILES` also plants `validate_backlog.py`, `validate_doc_claims.py`,
    `validate_git_backlog.py` and `gen_task_tree.py` as the literal text `x\\n`. With the stub
    directory left at `sys.path[0]`, a later `import validate_backlog` anywhere in the session
    resolves to a module with no functions in it -- and a test asserting over an empty surface
    does not fail, it passes vacuously. That is the failure mode this repo names
    `silent_rule_ratchet`, arriving through the import system.
    """
    repo = _stub_repo(tmp_path)
    before = list(sys.path)
    gh.collect_hints(repo)
    added = [p for p in sys.path if p not in before]
    assert added == [], f"collect_hints left the stub repo's scripts/ on sys.path: {added}"


def test_collect_hints_does_not_cache_the_stub_as_the_real_audit_module(tmp_path):
    """The module leak. WITNESSED, not hypothesised (this worktree, 2026-09-13):

        uv run --locked pytest tests/test_gen_handoff.py tests/test_residual_completeness.py -n 0

    reddened three tests in the SECOND file --
    `AttributeError: module 'audit' has no attribute '_vrc'` -- while the same file alone was
    29/29 green. The failure is attributed to the file that suffers it, never to the file that
    caused it, which is why it survived: re-running the victim in isolation "proves" it is fine.

    The assertion is deliberately about IDENTITY rather than about `_vrc`. Naming one missing
    attribute would pin today's symptom; what must hold is that a temp fixture cannot become
    the process's idea of a real module.
    """
    repo = _stub_repo(tmp_path)
    real = sys.modules.get("audit")
    gh.collect_hints(repo)
    after = sys.modules.get("audit")
    assert after is real, (
        "collect_hints replaced sys.modules['audit'] with the stub repo's placeholder; "
        "every module collected after this one now sees ALL_CHECKS = []")
    if after is not None:
        assert getattr(after, "ALL_CHECKS", None), "the cached `audit` has an empty ALL_CHECKS"


def test_collect_hints_still_reads_the_check_count_from_the_repo_it_is_given(tmp_path):
    """The other direction -- isolation must not be bought by making the hint a constant.

    A fix that stopped importing the target repo's `audit` altogether would pass both tests
    above and silently start reporting the HUB's check count for every repo handed to the
    generator. The stub declares `ALL_CHECKS = []`, so the honest answer for the stub repo is
    the degrade string this function already promises, never the live hub's number.
    """
    hints = gh.collect_hints(_stub_repo(tmp_path))
    assert hints["all_checks"].startswith("unknown ("), (
        f"the stub repo declares `ALL_CHECKS = []`, so the only honest hint is the degrade "
        f"pointer this function promises -- got {hints['all_checks']!r}")


# --- lane-boot-contract (WAVE5B-N2 row 12, 2026-09-25): the boot as DATA + PROSE -------------
#
# The boot a seat pastes used to MIX facts a probe could verify (slug, mode, destination
# branch, the role pin's version, the launcher, the pointers) with prose it could only trust
# (purpose, write-scope, mode basis), and the pointers rode in `>` blocks no probe read. The
# generator now emits the header as two delimited parts: a DATA block every row of which a
# `verify_handoff_probes` rule checks, and a short PROSE block holding only the hand-authored
# regions. These tests are the contract: the split, the coupling (no data row without a rule),
# the prose budget, the receipt's boot-cost field, and the dry cut.

import json  # noqa: E402


def _header(boot_text: str) -> str:
    """The pasted part of HANDOFF_BOOT.md: everything above the first `## ` heading."""
    return re.split(r"(?m)^## ", boot_text, maxsplit=1)[0]


def test_boot_header_is_a_data_block_then_a_prose_block(tmp_path):
    boot = (_gen(tmp_path).bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    head = _header(boot)
    d0, d1 = head.find(gh.BOOT_DATA_BEGIN), head.find(gh.BOOT_DATA_END)
    p0, p1 = head.find(gh.BOOT_PROSE_BEGIN), head.find(gh.BOOT_PROSE_END)
    assert -1 not in (d0, d1, p0, p1), "the pasted header must carry both delimited blocks"
    assert d0 < d1 < p0 < p1, "DATA first, then PROSE, each closed before the next opens"
    # No doctrine pointer rides in an unverified `>` block any more: the pointers are DATA rows.
    assert not [ln for ln in head.splitlines() if ln.startswith(">")], \
        "a `>` pointer block in the pasted header is prose no probe reads"


def test_every_boot_data_row_has_a_probe_rule(tmp_path):
    boot = (_gen(tmp_path).bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    rows, _prose = vhp.parse_boot_blocks(boot)
    assert rows, "the generated DATA block parsed to no rows"
    keys = [k for k, _v in rows]
    unruled = [k for k in keys if k not in vhp.BOOT_DATA_RULES]
    assert unruled == [], f"data rows no probe checks (move them to PROSE): {unruled}"
    # The generator's declared row set and the verifier's rule set are the SAME set, both ways:
    # a rule with no row is a probe that can never fire, a row with no rule is an unverified fact.
    assert set(keys) == set(vhp.BOOT_DATA_RULES), (set(keys) ^ set(vhp.BOOT_DATA_RULES))


def test_generated_boot_data_rows_all_pass_their_probes(tmp_path):
    res = _gen(tmp_path, assemble=True)
    results = [r for r in vhp.verify(res.bundle_dir, repo_root=res.bundle_dir.parents[2])
               if r.probe_id.startswith(("BD-", "BP-"))]
    ids = {r.probe_id for r in results}
    assert {f"BD-{vhp.boot_data_id(k)}" for k in vhp.BOOT_DATA_RULES} <= ids
    assert "BP-budget" in ids
    fails = [(r.probe_id, r.detail) for r in results if r.status == "fail"]
    assert fails == [], f"generated boot data fails its own probes: {fails}"


def test_prose_block_holds_the_hand_authored_regions_and_nothing_else(tmp_path):
    boot = (_gen(tmp_path).bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    head = _header(boot)
    data = head[head.find(gh.BOOT_DATA_BEGIN):head.find(gh.BOOT_DATA_END)]
    prose = head[head.find(gh.BOOT_PROSE_BEGIN):head.find(gh.BOOT_PROSE_END)]
    names = {m.group("name") for m in gh.FILL_IN_RE.finditer(prose)}
    assert {"purpose", "dest-worktree", "dest-scope", "dest-mode-basis"} <= names
    assert not list(gh.FILL_IN_RE.finditer(data)), "a hand-authored region inside the DATA block"


def test_prose_budget_is_stated_in_code_and_the_render_fits_it(tmp_path):
    assert isinstance(gh.BOOT_PROSE_BYTE_BUDGET, int) and gh.BOOT_PROSE_BYTE_BUDGET > 0
    boot = (_gen(tmp_path).bundle_dir / "HANDOFF_BOOT.md").read_text(encoding="utf-8")
    _rows, prose = vhp.parse_boot_blocks(boot)
    assert prose is not None
    assert vhp.prose_bytes(prose) <= gh.BOOT_PROSE_BYTE_BUDGET


def test_assembled_paste_is_under_the_ceiling_the_code_states(tmp_path):
    import assemble_paste as ap
    b = _gen(tmp_path, assemble=True).bundle_dir
    size = (b / "PASTE_THIS.md").stat().st_size
    assert size <= ap.PASTE_BYTE_CEILING
    receipt = json.loads((b / gh.RECEIPT_FILE).read_text(encoding="utf-8"))
    assert receipt["paste"]["bytes"] == size
    assert receipt["paste"]["ceiling_bytes"] == ap.PASTE_BYTE_CEILING


# --- the handoff receipt and its boot-cost field ------------------------------------------

def test_generation_writes_a_receipt_with_a_boot_cost_field(tmp_path):
    b = _gen(tmp_path).bundle_dir
    receipt = json.loads((b / gh.RECEIPT_FILE).read_text(encoding="utf-8"))
    cost = receipt["boot_cost"]
    assert cost["metric"] == gh.BOOT_COST_METRIC == "turns to first correct dispatch"
    # No tally was passed, so the only honest value is none, with the reason stated.
    assert cost["value"] is None
    assert cost["status"].startswith("unmeasured — ") and len(cost["status"]) > len("unmeasured — ")
    assert receipt["slug"] == b.name and receipt["cut"] == "real"


def test_boot_cost_is_measured_when_the_tally_names_a_dispatch_that_exists(tmp_path):
    transport = tmp_path / "transport"
    (transport / "to-cc").mkdir(parents=True)
    (transport / "to-cc" / "BATCH-X-2026-09-25.md").write_text("order\n", encoding="utf-8")
    cost = gh.boot_cost(turns=4, dispatch="to-cc/BATCH-X-2026-09-25.md", transport=transport)
    assert cost["value"] == 4 and cost["status"] == "measured"
    assert cost["dispatch"] == "to-cc/BATCH-X-2026-09-25.md"


@pytest.mark.parametrize("turns,dispatch,why", [
    (4, "to-cc/GONE.md", "does not exist"),        # the dispatch cannot be witnessed
    (4, "to-browser/X.md", "to-cc/"),               # not a dispatch order at all
    (4, None, "names no dispatch"),                 # a count with no dispatch proves nothing
    (0, "to-cc/BATCH-X-2026-09-25.md", "turn count"),  # not a count of turns
])
def test_boot_cost_degrades_to_unmeasured_with_its_reason(tmp_path, turns, dispatch, why):
    transport = tmp_path / "transport"
    (transport / "to-cc").mkdir(parents=True)
    (transport / "to-cc" / "BATCH-X-2026-09-25.md").write_text("order\n", encoding="utf-8")
    cost = gh.boot_cost(turns=turns, dispatch=dispatch, transport=transport)
    assert cost["value"] is None
    assert cost["status"].startswith("unmeasured — ") and why in cost["status"], cost["status"]


def test_receipt_carries_a_measured_tally_through_generate(tmp_path, monkeypatch):
    transport = tmp_path / "transport"
    (transport / "to-cc").mkdir(parents=True)
    (transport / "to-cc" / "BATCH-X-2026-09-25.md").write_text("order\n", encoding="utf-8")
    monkeypatch.setenv("CLAUDE_PROMPTS_DIR", str(transport))
    repo = _stub_repo(tmp_path)
    b = gh.generate(repo, mode="architect", slug="0000-00-00-t", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=repo / "docs" / "handoffs", assemble=False,
                    boot_turns=3, boot_dispatch="to-cc/BATCH-X-2026-09-25.md").bundle_dir
    cost = json.loads((b / gh.RECEIPT_FILE).read_text(encoding="utf-8"))["boot_cost"]
    assert (cost["value"], cost["status"]) == (3, "measured")


# --- the dry cut: a real render + assembly, outside the repo, never a handoff -------------

def test_dry_cut_refuses_a_target_inside_the_repo(tmp_path):
    repo = _stub_repo(tmp_path)
    with pytest.raises(ValueError, match="outside"):
        gh.generate(repo, mode="architect", slug="0000-00-00-t", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=repo / "docs" / "handoffs", dry_cut=True)


def test_dry_cut_skips_the_cut_boundaries_and_says_so_in_its_receipt(tmp_path, monkeypatch):
    def _refuse(*_a, **_k):
        raise AssertionError("a dry cut must not run a real cut's boundary gates")
    for name in ("assert_batch_boundary", "assert_boundary_hygiene", "assert_preflight"):
        monkeypatch.setattr(gh, name, _refuse)
    repo = _stub_repo(tmp_path)
    out = tmp_path / "dry"
    b = gh.generate(repo, mode="architect", slug="0000-00-00-t", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=out, assemble=True, dry_cut=True).bundle_dir
    assert b.parent == out
    receipt = json.loads((b / gh.RECEIPT_FILE).read_text(encoding="utf-8"))
    assert receipt["cut"] == "dry"
    assert (b / "PASTE_THIS.md").exists()


def test_a_dry_cut_bundle_passes_its_probes_outside_the_repo(tmp_path):
    """A bundle's self-locators (`docs/handoffs/<slug>/…`) name ITS OWN directory, so a bundle
    outside the repo still binds them — resolved against the bundle, never against a sibling."""
    repo = _stub_repo(tmp_path)
    b = gh.generate(repo, mode="architect", slug="0000-00-00-t", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=tmp_path / "dry", assemble=True,
                    dry_cut=True).bundle_dir
    fails = [(r.probe_id, r.detail) for r in vhp.verify(b, repo_root=repo) if r.status == "fail"]
    assert fails == [], fails


# --- terra review 2026-09-25: the dry cut may not land where it could be committed ---------
# NOT skipif-on-git: the dry-cut refusal is a proof, and a proof that can be skipped on the box
# that lacks git is not a mechanism (audit.py proof_layer). Without git these FAIL, loudly.

def test_dry_cut_refuses_a_target_inside_another_git_work_tree(tmp_path):
    """A sibling worktree's `docs/handoffs/` is OUTSIDE this repo and is still committable."""
    repo = _stub_repo(tmp_path)
    other = tmp_path / "other"
    (other / "docs" / "handoffs").mkdir(parents=True)
    (other / "README.md").write_text("x\n", encoding="utf-8")
    _git_init_commit(other)
    with pytest.raises(gh.DryCutTargetError, match="could be committed"):
        gh.generate(repo, mode="architect", slug="0000-00-00-t", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=other / "docs" / "handoffs", dry_cut=True)


def test_dry_cut_accepts_a_path_the_containing_work_tree_ignores(tmp_path):
    """The job-tmp shape: `~/.claude` is a git repo whose `.gitignore` ignores `jobs/`."""
    repo = _stub_repo(tmp_path)
    home = tmp_path / "home"
    home.mkdir()
    (home / ".gitignore").write_text("/jobs/\n", encoding="utf-8")
    _git_init_commit(home)
    out = home / "jobs" / "x" / "tmp" / "dry"
    b = gh.generate(repo, mode="architect", slug="0000-00-00-t", repo=".dev-knowledge",
                    date="2026-07-04", bundle_root=out, assemble=False, dry_cut=True).bundle_dir
    assert b.parent == out


def test_a_measured_boot_cost_names_its_instrument_and_binds_its_dispatch(tmp_path):
    import hashlib
    transport = tmp_path / "transport"
    (transport / "to-cc").mkdir(parents=True)
    order = transport / "to-cc" / "BATCH-X-2026-09-25.md"
    order.write_text("order\n", encoding="utf-8")
    cost = gh.boot_cost(turns=2, dispatch="to-cc/BATCH-X-2026-09-25.md", transport=transport)
    assert cost["dispatch_sha256"] == hashlib.sha256(order.read_bytes()).hexdigest()
    assert cost["source"].startswith("operator tally")
    assert "not machine-witnessed" in cost["source"]
