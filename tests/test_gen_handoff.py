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
import subprocess
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
    "scripts/gen_task_tree.py": "x\n",     # P0a's currency assertion target (R2, [#446])
    "BACKLOG.md": "x\n",
    "protocols/HANDOFF_PROCESS.md": "# H\n\nno per-bundle README\n",
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
    assert len(rows) == 14  # 11 -> 14: P0a/P0b/P0c standing-topic legs added (R2 / [#446], 2026-07-31); P1a/P1b + P2..P10 (P10 = BACKLOG grooming, operator ruling 2026-07-17)
    hits = [(r["id"], c) for r in rows for c in ("question", "source", "why", "command")
            if re.search(r"expected[ :]", r[c], re.IGNORECASE)]
    assert hits == [], f"generated probe rows carry answer hints: {hits}"


def test_dogfood_generated_bundle_has_no_failing_probe(tmp_path):
    # The generated bundle PASSES verify_handoff_probes (done-contract bullet 5): resolved against
    # a self-contained stub repo, no probe is FAIL-class. (grep/sed/git absent -> `skipped`, not
    # `fail`; a fail would mean a toothless/malformed/missing-source generated row.)
    res = _gen(tmp_path)
    results = vhp.verify(res.bundle_dir, repo_root=res.bundle_dir.parents[2])
    assert len(results) == 14  # 11 -> 14: P0a/P0b/P0c standing-topic legs added (R2 / [#446], 2026-07-31); P1a/P1b + P2..P10 (P10 = BACKLOG grooming, operator ruling 2026-07-17)
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
