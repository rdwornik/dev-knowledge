"""[#926] -- two ship-tier gates that could not recognise the only correction their own invariants
permit. RED-FIRST: written and run against a tree where neither check has the narrowing.

Operator order 2026-09-19. Each narrowing is TEMPORARY BY CONSTRUCTION: it carries an expiry the
CHECK READS (a module constant, overridable in tests through the module's `_today`), and past that
date the narrowing switches itself off and the finding names `[#926]` for re-ruling. Each check
also has a test proving the UNCORRECTED case still fails -- a narrowing that also silenced the
defect it scopes would be a widening wearing a narrower name.

  * journal_day_letters -- a duplicate day-letter counts as resolved only when a LATER entry
    (above both blocks, JOURNAL being newest-first) whose heading says CORRECTION names the
    collision and points at BOTH colliding blocks by their heading text. JOURNAL is append-only,
    so correction-by-addition is the only correction the file permits.
  * substrate_declaration -- leg 8 (`substrate-heartbeat-dead`) is scoped to PRE-LAUNCH
    contracts. A contract is post-launch when its batch's `closed_by:` packet is committed; a
    contract with no matching batch manifest stays pre-launch (fail toward refusal). No other leg
    is scoped, and the in-contract deviation-line escape is not used.

git is invoked directly, without a skipif guard: a proof that can be skipped on the machine that
breaks the property is not a proof (`check_proof_layer`).
"""
from __future__ import annotations

import datetime as _dt
import subprocess
from pathlib import Path

import audit as aud
import validate_substrate as vs
from audit_checks import check_substrate_declaration as adapter


# --- journal_day_letters ------------------------------------------------------------------

M6 = "### 2026-09-18 (f) - CC (Opus 5, integrator seat, batch AC): M6 merges the batch AC freeze"
P1 = "### 2026-09-18 (f) - CC (Opus 5): P1 of DECLARE-BATCH-AC-CLOSE-AMENDED -- the handback"


def _correction(*pointers: str, heading: str = "### 2026-09-19 (aq) - CC: CORRECTION -- "
                                               "2026-09-18 carries two entries lettered (f)") -> str:
    body = "\n".join(f"- `{p}...` -- pointer" for p in pointers)
    return f"{heading}\n\nThe collision 2026-09-18 (f):\n{body}\n\n"


def _journal(tmp_path: Path, monkeypatch, text: str, today: _dt.date = _dt.date(2026, 9, 20)):
    (tmp_path / "JOURNAL.md").write_text(text, encoding="utf-8")
    monkeypatch.setattr(aud, "_REPO_ROOT", str(tmp_path))
    monkeypatch.setattr(aud, "_today", lambda: today)
    return aud.check_journal_day_letters(tmp_path)[0]


def test_an_uncorrected_duplicate_day_letter_still_refuses(tmp_path, monkeypatch):
    """THE uncorrected case: no correction entry at all -> FAIL, exactly as before."""
    f = _journal(tmp_path, monkeypatch, f"{M6}\nbody\n\n{P1}\nbody\n")
    assert f.status == "fail"
    assert "2026-09-18 (f)" in f.evidence


def test_a_later_correction_naming_both_blocks_resolves_the_duplicate(tmp_path, monkeypatch):
    f = _journal(tmp_path, monkeypatch,
                 _correction(M6, P1) + f"{M6}\nbody\n\n{P1}\nbody\n")
    assert f.status == "pass", f.evidence
    assert "2026-09-18 (f)" in f.evidence       # the resolved collision stays VISIBLE
    assert "[#926]" in f.evidence


def test_a_correction_pointing_at_only_one_block_does_not_resolve(tmp_path, monkeypatch):
    f = _journal(tmp_path, monkeypatch, _correction(M6) + f"{M6}\nbody\n\n{P1}\nbody\n")
    assert f.status == "fail"


def test_a_correction_without_the_CORRECTION_heading_does_not_resolve(tmp_path, monkeypatch):
    text = (_correction(M6, P1, heading="### 2026-09-19 (aq) - CC: a note about (f)")
            + f"{M6}\nbody\n\n{P1}\nbody\n")
    assert _journal(tmp_path, monkeypatch, text).status == "fail"


def test_a_correction_OLDER_than_the_collision_does_not_resolve(tmp_path, monkeypatch):
    """Newest-first: a block below the collision predates it and cannot correct it."""
    text = f"{M6}\nbody\n\n{P1}\nbody\n\n" + _correction(
        M6, P1, heading="### 2026-09-17 (z) - CC: CORRECTION -- 2026-09-18 (f)")
    assert _journal(tmp_path, monkeypatch, text).status == "fail"


def test_a_correction_for_one_collision_does_not_resolve_another(tmp_path, monkeypatch):
    other_a = "### 2026-09-10 (b) - CC: first b entry on the tenth"
    other_b = "### 2026-09-10 (b) - CC: second b entry on the tenth"
    text = (_correction(M6, P1) + f"{M6}\nbody\n\n{P1}\nbody\n\n"
            f"{other_a}\nbody\n\n{other_b}\nbody\n")
    f = _journal(tmp_path, monkeypatch, text)
    assert f.status == "fail"
    assert "2026-09-10 (b)" in f.evidence and "2026-09-18 (f)" not in f.evidence


def test_the_journal_narrowing_expires_by_itself_and_names_926(tmp_path, monkeypatch):
    """TEMPORARY BY CONSTRUCTION: past the expiry the corrected duplicate FAILs again."""
    day_after = aud._JOURNAL_CORRECTION_EXPIRES + _dt.timedelta(days=1)
    f = _journal(tmp_path, monkeypatch, _correction(M6, P1) + f"{M6}\nbody\n\n{P1}\nbody\n",
                 today=day_after)
    assert f.status == "fail"
    assert "[#926]" in f.evidence and "expired" in f.evidence


def test_the_journal_expiry_is_a_real_date_the_check_reads():
    assert isinstance(aud._JOURNAL_CORRECTION_EXPIRES, _dt.date)


# --- substrate_declaration: leg 8 scoped to pre-launch ------------------------------------

LAUNCH_DIR = "docs/audits/2026-09-17-technical-batchq-launch-contracts"
CONTRACT = f"{LAUNCH_DIR}/LANE-q-1-census.md"
MANIFEST = "docs/audits/2026-09-17-technical-batch-q-manifest.md"
CLOSER = "docs/audits/2026-09-17-technical-batch-q-close-packet.md"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def _substrate_repo(tmp_path: Path, *, manifest: bool, closed: bool) -> Path:
    repo = tmp_path / "r"
    (repo / LAUNCH_DIR).mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")
    (repo / CONTRACT).write_text("# LANE q-1\n\n**Shape:** `cloud`\n", encoding="utf-8")
    if manifest:
        (repo / MANIFEST).write_text(
            f"---\nbatch: Q\nstatus: open\nclosed_by: {CLOSER}\n---\n\n# Batch Q\n",
            encoding="utf-8")
    if closed:
        (repo / CLOSER).write_text("# packet\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture")
    return repo


def _run_adapter(monkeypatch, repo: Path, rules=(vs.RULE_HEARTBEAT_DEAD,),
                 today: _dt.date = _dt.date(2026, 9, 20)):
    """Leg 8 reads a machine-local heartbeat receipt; the refusal is injected so the test asks
    the ADAPTER's question (is this refusal in scope?) and not the receipt's."""
    monkeypatch.setattr(adapter._vsub, "load_registry", lambda _repo: {})
    monkeypatch.setattr(adapter._vsub, "validate_batch", lambda gated, registry: [
        vs.Refusal(rule=r, source=src, substrate="cloud", detail=f"{r} on {src}")
        for src in gated for r in rules])
    monkeypatch.setattr(adapter, "_today", lambda: today)
    return adapter.check_substrate_declaration(repo)


def test_a_PRE_LAUNCH_contract_declaring_an_unproven_substrate_still_refuses(tmp_path, monkeypatch):
    """THE uncorrected case: the batch is open (closer absent) -> leg 8 still FAILs."""
    repo = _substrate_repo(tmp_path, manifest=True, closed=False)
    fails = [f for f in _run_adapter(monkeypatch, repo) if f.status == "fail"]
    assert len(fails) == 1 and "LANE-q-1-census.md" in fails[0].evidence


def test_a_contract_with_no_batch_manifest_is_treated_as_pre_launch(tmp_path, monkeypatch):
    repo = _substrate_repo(tmp_path, manifest=False, closed=False)
    assert any(f.status == "fail" for f in _run_adapter(monkeypatch, repo))


def test_a_POST_LAUNCH_contract_is_out_of_leg_8_scope_and_stays_visible(tmp_path, monkeypatch):
    repo = _substrate_repo(tmp_path, manifest=True, closed=True)
    out = _run_adapter(monkeypatch, repo)
    assert all(f.status == "pass" for f in out), [f.evidence for f in out]
    assert any("post-launch" in f.evidence and "[#926]" in f.evidence for f in out)


def test_the_post_launch_scope_out_stays_visible_beside_an_unrelated_warn(tmp_path, monkeypatch):
    """The scope-out must not vanish just because another leg WARNs on the same run."""
    repo = _substrate_repo(tmp_path, manifest=True, closed=True)
    monkeypatch.setattr(adapter._vsub, "load_registry", lambda _repo: {})
    monkeypatch.setattr(adapter._vsub, "validate_batch", lambda gated, registry: [
        vs.Refusal(rule=vs.RULE_HEARTBEAT_DEAD, source=src, substrate="cloud", detail="dead")
        for src in gated] + [vs.Refusal(rule=vs.RULE_SECOND_LOCAL_WRITER, source="x",
                                        severity=vs.SEVERITY_WARN, detail="two writers")])
    monkeypatch.setattr(adapter, "_today", lambda: _dt.date(2026, 9, 20))
    out = adapter.check_substrate_declaration(repo)
    assert any(f.status == "warn" for f in out)
    assert any(f.status == "pass" and "[#926]" in f.evidence for f in out)


def test_the_post_launch_scope_covers_leg_8_only(tmp_path, monkeypatch):
    """Every other leg still refuses a closed batch's contract: the narrowing is one leg wide."""
    repo = _substrate_repo(tmp_path, manifest=True, closed=True)
    out = _run_adapter(monkeypatch, repo, rules=(vs.RULE_HEARTBEAT_DEAD, vs.RULE_NO_LIVE_VERB))
    fails = [f for f in out if f.status == "fail"]
    assert len(fails) == 1 and vs.RULE_NO_LIVE_VERB in fails[0].evidence


def test_the_substrate_narrowing_expires_by_itself_and_names_926(tmp_path, monkeypatch):
    repo = _substrate_repo(tmp_path, manifest=True, closed=True)
    day_after = adapter.POST_LAUNCH_NARROWING_EXPIRES + _dt.timedelta(days=1)
    fails = [f for f in _run_adapter(monkeypatch, repo, today=day_after) if f.status == "fail"]
    assert len(fails) == 1
    assert "[#926]" in fails[0].evidence and "expired" in fails[0].evidence


def test_the_batch_key_joins_a_launch_dir_to_its_manifest_across_dash_spelling():
    """The live witness: `batchac-launch-contracts` belongs to `batch-ac-manifest.md`."""
    assert adapter._batch_key_of_launch_dir("2026-09-17-technical-batchac-launch-contracts") \
        == adapter._batch_key_of_manifest("docs/audits/2026-09-17-technical-batch-ac-manifest.md")
    assert adapter._batch_key_of_launch_dir("2026-09-13-technical-batch-x3-launch-contracts") \
        != adapter._batch_key_of_manifest("docs/audits/2026-09-13-technical-batch-x4-manifest.md")
