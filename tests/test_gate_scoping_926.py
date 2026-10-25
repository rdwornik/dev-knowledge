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
    failing, _, disclosed = f.evidence.partition("; ")
    assert "2026-09-10 (b)" in failing and "2026-09-18 (f)" not in failing
    # Codex terra MED 2026-09-19 (pass 3): the scoped-out collision stays VISIBLE on a FAIL run.
    assert "2026-09-18 (f) resolved" in disclosed and "[#926]" in disclosed


def test_the_journal_narrowing_expires_by_itself_and_names_926(tmp_path, monkeypatch):
    """TEMPORARY BY CONSTRUCTION: past the expiry the corrected duplicate FAILs again."""
    day_after = aud._JOURNAL_CORRECTION_EXPIRES + _dt.timedelta(days=1)
    f = _journal(tmp_path, monkeypatch, _correction(M6, P1) + f"{M6}\nbody\n\n{P1}\nbody\n",
                 today=day_after)
    assert f.status == "fail"
    assert "[#926]" in f.evidence and "expired" in f.evidence


def test_the_journal_expiry_is_a_real_date_the_check_reads():
    assert isinstance(aud._JOURNAL_CORRECTION_EXPIRES, _dt.date)


# batch BW lane bw-926-main-red: the 2026-10-11 (d) collision -- FIVE entries lettered (d) whose
# heading lines share 69 leading characters, more than the fixed 60-character pointer, so no
# correction could tell them apart and the collision was unresolvable by construction. The
# pointer is now the SHORTEST prefix (at least 60 characters) that distinguishes every colliding
# heading; the headings below are the five live ones, verbatim.
D5 = [
    "### 2026-10-11 (d) - Copilot CLI (claude-opus-5.5, batch B2-W4 lane B6 preflight-dead-id): "
    "a dead [#id] names its live value; provider_router refuses an unknown role in one line",
    "### 2026-10-11 (d) - Copilot CLI (claude-opus-5.5, batch B2-W4 lane B4 read-gate-fix): "
    "the read gate refuses a non-UTF-8 source; quotes inside code spans pair correctly",
    "### 2026-10-11 (d) - Copilot CLI (claude-opus-5.5, batch B2-W4 lane B3 dispatch-plan-fix): "
    "plan refuses a --slug the Dispatch block disagrees with; the --token-cap doc matches --help",
    "### 2026-10-11 (d) - Copilot CLI (claude-opus-5.5, batch B2-W4 lane B2 handoff-verify-fix): "
    "a cp1252-redirected handoff verify exits 0 and its warn count is true",
    "### 2026-10-11 (d) - Copilot CLI (claude-opus-5.5, batch B2-W4 lane B1 stop-fail-closed): "
    "Stop hooks fail closed; the launchers are shell-neutral",
]
D5_BODY = "".join(f"{h}\nbody\n\n" for h in D5)
D5_HEADING = "### 2026-10-13 (b) - CC: CORRECTION -- 2026-10-11 carries five entries lettered (d)"


def _d5_correction(*pointers: str) -> str:
    body = "\n".join(f"- `{p}` -- pointer" for p in pointers)
    return f"{D5_HEADING}\n\nThe collision 2026-10-11 (d):\n{body}\n\n"


def test_five_headings_sharing_more_than_60_chars_are_resolvable_by_a_full_quote(
        tmp_path, monkeypatch):
    """(i) THE correction clears it: a later CORRECTION quoting each colliding heading in full."""
    assert len(set(h[:aud._JOURNAL_POINTER_CHARS] for h in D5)) == 1   # the premise, measured
    f = _journal(tmp_path, monkeypatch, _d5_correction(*D5) + D5_BODY,
                 today=_dt.date(2026, 10, 13))
    assert f.status == "pass", f.evidence
    assert "2026-10-11 (d) resolved" in f.evidence and "[#926]" in f.evidence


def test_a_quote_only_as_long_as_the_shared_prefix_does_not_resolve(tmp_path, monkeypatch):
    """Ambiguous is not corrected: a pointer that cannot tell the five blocks apart names none."""
    shared = D5[0][:69]
    assert all(h.startswith(shared) for h in D5)
    f = _journal(tmp_path, monkeypatch, _d5_correction(*[shared] * 5) + D5_BODY,
                 today=_dt.date(2026, 10, 13))
    assert f.status == "fail"


def test_a_correction_quoting_four_of_the_five_does_not_resolve(tmp_path, monkeypatch):
    f = _journal(tmp_path, monkeypatch, _d5_correction(*D5[:4]) + D5_BODY,
                 today=_dt.date(2026, 10, 13))
    assert f.status == "fail"
    assert "2026-10-11 (d)" in f.evidence.partition("; ")[0]


def test_a_new_uncorrected_duplicate_still_fails_beside_the_corrected_five(tmp_path, monkeypatch):
    """(ii) a NEW, uncorrected duplicate still FAILs -- the corrected one stays only disclosed."""
    new_a = "### 2026-10-13 (a) - CC: the wave entry"
    new_b = "### 2026-10-13 (a) - CC: a second wave entry re-using the letter"
    text = f"{new_a}\nbody\n\n{new_b}\nbody\n\n" + _d5_correction(*D5) + D5_BODY
    f = _journal(tmp_path, monkeypatch, text, today=_dt.date(2026, 10, 13))
    assert f.status == "fail"
    failing, _, disclosed = f.evidence.partition("; ")
    assert "2026-10-13 (a)" in failing and "2026-10-11 (d)" not in failing
    assert "2026-10-11 (d) resolved" in disclosed


def test_identical_colliding_headings_are_never_resolvable(tmp_path, monkeypatch):
    """No prefix of two IDENTICAL heading lines tells them apart, so no quote can resolve them."""
    same = "### 2026-10-11 (d) - CC: the very same heading line, twice"
    text = _d5_correction(same) + f"{same}\nbody one\n\n{same}\nbody two\n"
    f = _journal(tmp_path, monkeypatch, text, today=_dt.date(2026, 10, 13))
    assert f.status == "fail"


def test_a_heading_that_is_a_prefix_of_another_is_never_resolvable(tmp_path, monkeypatch):
    """Quoting the longer heading would also 'quote' the shorter one, so pointing is ambiguous."""
    short = "### 2026-10-11 (d) - CC: a heading line that is long enough to pass sixty characters"
    long_ = short + " and then carries on"
    text = _d5_correction(long_) + f"{short}\nbody\n\n{long_}\nbody\n"
    f = _journal(tmp_path, monkeypatch, text, today=_dt.date(2026, 10, 13))
    assert f.status == "fail"


def test_the_five_way_correction_still_expires_by_itself(tmp_path, monkeypatch):
    day_after = aud._JOURNAL_CORRECTION_EXPIRES + _dt.timedelta(days=1)
    f = _journal(tmp_path, monkeypatch, _d5_correction(*D5) + D5_BODY, today=day_after)
    assert f.status == "fail"
    assert "[#926]" in f.evidence and "expired" in f.evidence


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
        vs.Refusal(rule=r, source=src, substrate="codespace", detail=f"{r} on {src}")
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


def test_a_launch_dir_nested_inside_a_closed_batchs_dir_is_judged_by_its_own_batch(
        tmp_path, monkeypatch):
    """Codex terra HIGH 2026-09-19 (pass 2): the NEAREST launch-contracts dir owns the contract.
    Batch R has no manifest (pre-launch) even though it sits inside closed batch Q's dir."""
    repo = _substrate_repo(tmp_path, manifest=True, closed=True)
    inner = repo / LAUNCH_DIR / "2026-09-18-technical-batch-r-launch-contracts"
    inner.mkdir()
    (inner / "LANE-r-1.md").write_text("# LANE\n\n**Shape:** `cloud`\n", encoding="utf-8")
    (repo / CONTRACT).unlink()
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "nested")
    fails = [f for f in _run_adapter(monkeypatch, repo) if f.status == "fail"]
    assert len(fails) == 1 and "LANE-r-1.md" in fails[0].evidence


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
    # Codex terra HIGH 2026-09-19 (pass 3): case is identity, not a folded spelling variation.
    assert adapter._batch_key_of_launch_dir("2026-09-13-technical-batch-X-launch-contracts") \
        != adapter._batch_key_of_manifest("docs/audits/2026-09-13-technical-batch-x-manifest.md")


def test_a_closed_batch_does_not_scope_out_a_same_day_batch_spelled_one_dash_apart(
        tmp_path, monkeypatch):
    """Codex terra HIGH 2026-09-19: stripping EVERY dash made `batch-x3` and `batch-x-3` one
    key, so closing x3 silenced leg 8 on x-3's still-open contract. Only the dash directly after
    `batch` is the sanctioned spelling variation; anything else stays a different batch."""
    repo = tmp_path / "r"
    x3_dir = "docs/audits/2026-09-17-technical-batch-x-3-launch-contracts"
    (repo / x3_dir).mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@t.t")
    _git(repo, "config", "user.name", "t")
    (repo / x3_dir / "LANE-x-3-1.md").write_text("# LANE\n\n**Shape:** `cloud`\n", encoding="utf-8")
    closer = "docs/audits/2026-09-17-technical-batch-x3-close-packet.md"
    (repo / "docs/audits/2026-09-17-technical-batch-x3-manifest.md").write_text(
        f"---\nbatch: X3\nstatus: open\nclosed_by: {closer}\n---\n\n# Batch X3\n", encoding="utf-8")
    (repo / closer).write_text("# packet\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture")
    fails = [f for f in _run_adapter(monkeypatch, repo) if f.status == "fail"]
    assert len(fails) == 1 and "LANE-x-3-1.md" in fails[0].evidence
