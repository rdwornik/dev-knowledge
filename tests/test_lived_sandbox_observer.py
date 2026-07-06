"""Layer-1 (hermetic, offline) tests for the lived-workflow OBSERVER + engages ORACLE
(Slice B; [#252]). The oracle loads the essence-spec's engages: triples; the observer
derives its verdict from three EXTERNAL channels only (transcript-events / hook-stdout /
git-state) and NEVER from inner-session narration (C1). The live arc + the real frozen
fixtures (arc-green / arc-silent, the C4 discrimination proof) are in the skip-gated
acceptance section at the bottom, produced by the operator's live freeze (Step 7)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "deploy"))
import os  # noqa: E402
import shutil  # noqa: E402

from lived_sandbox import arc as arcmod  # noqa: E402
from lived_sandbox import oracle as orc  # noqa: E402
from lived_sandbox import observe as obs  # noqa: E402
from lived_sandbox import spawn as sp  # noqa: E402

_MANIFEST_V120 = _REPO / "deploy" / "manifest-v1.2.0.yaml"

# The gated firing-hook signatures as authored in manifest-v1.2.0.yaml (seven w/ #250).
_GATED_SIGNATURES = [
    "pre-commit installed at", "sha256 sidecar", "canonical_freshness",
    "TOC freshness", "Session-end", "propose_closures:", "Codemap freshness",
]


_TOOL_ID = iter(range(10_000))


def _tool_result(text: str, tool: str = "Bash") -> list[dict]:
    """A tool_use/tool_result PAIR (as real transcripts carry them). Bash results are the
    hook-stdout channel; any other tool's result is a content echo the channel excludes."""
    tid = f"toolu_{next(_TOOL_ID):05d}"
    return [
        {"type": "assistant", "message": {"role": "assistant",
         "content": [{"type": "tool_use", "id": tid, "name": tool, "input": {}}]}},
        {"type": "user", "message": {"role": "user",
         "content": [{"type": "tool_result", "tool_use_id": tid, "content": text}]}},
    ]


def _assistant_text(text: str) -> dict:
    """Assistant narration — the FORBIDDEN channel (must never enter hook-stdout)."""
    return {"type": "assistant", "message": {"role": "assistant",
            "content": [{"type": "text", "text": text}]}}


def _tool_use(name: str, command: str) -> dict:
    return {"type": "assistant", "message": {"role": "assistant",
            "content": [{"type": "tool_use", "name": name, "input": {"command": command}}]}}


def _green_events():
    """All seven hook signatures in REAL Bash tool-result stdout + a command act; ruff absent."""
    evs = []
    for s in _GATED_SIGNATURES:
        evs.extend(_tool_result(f"pre-commit hook fired: {s}....Passed"))
    evs.append(_tool_use("SlashCommand", "/review-closures"))
    return evs

_GATED_SET = {
    "floor-sessionstart-guard",
    "floor-hash-verify-hook",
    "canonical-freshness",
    "hub-toc-hooks",
    "hub-codemap-hooks",
    "session-end-backpressure",
    "propose-closures-stop-hook",
}


# --- the engages oracle (C2 data, loaded — not hand-coded) ---


def test_oracle_loads_the_real_v120_manifest():
    o = orc.load_oracle(_MANIFEST_V120)
    assert o.version == "1.2.0"
    assert len(o.expectations) == 14  # every component carries a triple (13 -> 14: #250 hub-codemap-hooks)


def test_oracle_gated_active_is_exactly_the_gated_set():
    o = orc.load_oracle(_MANIFEST_V120)
    assert {e.component_id for e in o.gated_active} == _GATED_SET


def test_oracle_ruff_tombstone_is_gated_absent():
    o = orc.load_oracle(_MANIFEST_V120)
    assert {e.component_id for e in o.gated_absent} == {"ruff-gate"}
    ruff = o.by_id("ruff-gate")
    assert ruff.absent is True and ruff.signature == "Ruff linter"


def test_oracle_observed_not_gated_excludes_the_gated_set():
    o = orc.load_oracle(_MANIFEST_V120)
    ids = {e.component_id for e in o.observed_not_gated}
    assert _GATED_SET.isdisjoint(ids)
    assert "methodology-floor" in ids          # git-state channel -> observed, not gated
    assert "review-closures-command" in ids    # operator-invoke -> OUT-OF-ARC


def test_oracle_string_expect_is_present_signature():
    o = orc.load_oracle(_MANIFEST_V120)
    canon = o.by_id("canonical-freshness")
    assert canon.signature == "canonical_freshness" and canon.absent is False


def test_oracle_load_for_version_resolves_the_manifest():
    o = orc.load_for_version("1.2.0")
    assert {e.component_id for e in o.gated_active} == _GATED_SET


def test_oracle_empty_expect_raises():
    with pytest.raises(orc.OracleError):
        orc._parse_expect("x", "   ")


def test_oracle_absent_mapping_without_signature_raises():
    with pytest.raises(orc.OracleError):
        orc._parse_expect("x", {"absent": True})


# --- signature-breadth discipline ([#253c]) ---


def test_signature_breadth_guard_flags_the_closure_case_253c():
    """[#253c] regression: the bare word `closure` is every failure mode at once — short,
    separator-free, a partial-word match on review_closures.py, and a substring of the
    arc prompt's /review-closures. The guard must flag it."""
    exp = orc.Expectation(component_id="x", kind="hook", status="active", trigger="stop",
                          observable="hook-stdout", signature="closure", absent=False)
    o = orc.Oracle(version="t", expectations=(exp,))
    probs = orc.signature_breadth_problems(o, repo_root=_REPO, arc_prompt=arcmod.ARC_PROMPT)
    assert any("shorter" in p for p in probs)
    assert any("bare word" in p for p in probs)
    assert any("partial-word-matches" in p for p in probs)
    assert any("arc prompt" in p for p in probs)


def test_signature_breadth_real_manifest_is_disciplined_253c():
    """THE lint gate: every gated signature in the live manifest passes the discipline
    (longest-stable-substring calibration; re-run after every step-7 recalibration)."""
    o = orc.load_oracle(_MANIFEST_V120)
    assert orc.signature_breadth_problems(
        o, repo_root=_REPO, arc_prompt=arcmod.ARC_PROMPT) == []


def test_partial_word_match_semantics_253c():
    assert orc._is_partial_word_match("closure", "review_closures.py")
    assert not orc._is_partial_word_match("canonical_freshness", "canonical_freshness_gate.py")
    assert not orc._is_partial_word_match("closure", "unrelated.py")


# --- the observer: gated verdict over the external channels ---


def test_observer_green_when_all_gated_fired():
    o = orc.load_oracle(_MANIFEST_V120)
    r = obs.observe(_green_events(), o)
    assert r.passed, r.summary()
    assert {f.component_id for f in r.gated_findings if f.verdict == obs.FIRED} == _GATED_SET
    assert not r.flags


def test_observer_flags_one_silent_hook():
    """A single gated firing hook whose stdout is absent -> EXPECTED-BUT-SILENT -> not passed."""
    o = orc.load_oracle(_MANIFEST_V120)
    # Drop the canonical_freshness signal (one of the gated set).
    events = [e for e in _green_events() if "canonical_freshness" not in json.dumps(e)]
    r = obs.observe(events, o)
    assert not r.passed
    assert any(f.component_id == "canonical-freshness" and f.verdict == obs.SILENT
               for f in r.silences)


def test_observer_ruff_tombstone_absent_ok():
    o = orc.load_oracle(_MANIFEST_V120)
    r = obs.observe(_green_events(), o)  # ruff signature "Ruff lint gate" is NOT present
    ruff = next(f for f in r.gated_findings if f.component_id == "ruff-gate")
    assert ruff.verdict == obs.ABSENT_OK


def test_observer_flags_ruff_tombstone_if_it_fires():
    """Prune regression: if ruff fired, the tombstone is UNEXPECTED -> not passed."""
    o = orc.load_oracle(_MANIFEST_V120)
    events = _green_events() + _tool_result(
        "Ruff linter (version-pinned >=0.15.5; system binary; blocks on violations)....Passed")
    r = obs.observe(events, o)
    assert not r.passed
    assert any(f.component_id == "ruff-gate" and f.verdict == obs.UNEXPECTED for f in r.flags)


def test_observer_ignores_inner_narration_C1():
    """C1 (THE proof): the gated signatures appearing ONLY in assistant *narration* must NOT
    count as firing — the observer flags them SILENT. Verify-by-state, never by narration."""
    o = orc.load_oracle(_MANIFEST_V120)
    narrated = [_assistant_text(
        "I ran all the hooks: " + " ".join(f"{s}....Passed" for s in _GATED_SIGNATURES)
        + " and /review-closures — everything is green.")]
    r = obs.observe(narrated, o)
    assert not r.passed, "narration must never produce a green verdict"
    assert {f.component_id for f in r.silences} == _GATED_SET


def test_observer_narration_excluded_from_hook_surface():
    """The hook-stdout channel is event-type keyed ([NB-2]): a signature in an assistant
    text item is absent from the surface; the same signature in a tool_result is present."""
    assert "canonical_freshness" not in obs.hook_stdout_surface(
        [_assistant_text("canonical_freshness passed")])
    assert "canonical_freshness" in obs.hook_stdout_surface(
        _tool_result("canonical_freshness passed"))


def test_observer_read_echo_never_counts_as_hook_stdout():
    """Step-7 leg-e witnessed: the child Read JOURNAL.md and the tool_result echoed a
    signature string from repo CONTENT, false-FIRING a disabled hook. Only BASH results
    can carry hook stdout; a Read/Grep result is a content echo -> excluded."""
    text = "canonical_freshness last_reviewed gate (A2 FAIL blocks the commit)"
    assert "canonical_freshness" not in obs.hook_stdout_surface(_tool_result(text, tool="Read"))
    assert "canonical_freshness" in obs.hook_stdout_surface(_tool_result(text))


def _result_event(text: str) -> dict:
    """A stream-json final `result` event — its `result` field is the child's closing
    narration (the [#253b] leak channel), never hook stdout."""
    return {"type": "result", "subtype": "success", "is_error": False, "result": text}


def test_observer_result_event_narration_excluded_253b():
    """[#253b] regression: a transcript whose ONLY signature matches live in the result
    event's narration field yields SILENT for all gated — never FIRED. (This leak made
    Block B's lone FIRED a narration artifact.)"""
    o = orc.load_oracle(_MANIFEST_V120)
    narrated = [_result_event(
        "ARC DONE — hooks all fired: " + " ".join(f"{s}....Passed" for s in _GATED_SIGNATURES))]
    r = obs.observe(narrated, o)
    assert not r.passed, "a result-event narration must never produce a green verdict"
    assert {f.component_id for f in r.silences} == _GATED_SET


def test_observer_result_event_excluded_from_hook_surface_253b():
    """The result field never enters the hook-stdout surface; a real tool_result still does."""
    assert "canonical_freshness" not in obs.hook_stdout_surface(
        [_result_event("canonical_freshness....Passed")])
    assert "canonical_freshness" in obs.hook_stdout_surface(
        _tool_result("canonical_freshness....Passed"))


def test_observer_counts_command_act():
    o = orc.load_oracle(_MANIFEST_V120)
    r = obs.observe(_green_events(), o)
    assert len(r.commands_observed) >= 1
    assert any("review-closures" in f.evidence or f.component_id == "review-closures-command"
               for f in r.commands_observed)


# --- the git-state channel: real git probes against a real temp repo (no narration) ---


def _init_repo(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for args in (["init", "-q"], ["config", "user.email", "t@e.st"],
                 ["config", "user.name", "T"], ["config", "commit.gpgsign", "false"],
                 ["checkout", "-q", "-b", "feat/arc"]):
        obs._git(root, *args)
    (root / "note.txt").write_text("edit\n", encoding="utf-8")
    obs._git(root, "add", "note.txt")
    obs._git(root, "commit", "-q", "-m", "arc: edit note")
    return root


def test_git_state_channel_probes_real_repo(tmp_path):
    repo = _init_repo(tmp_path / "clone")
    assert obs.branch_exists(repo, "feat/arc")
    assert not obs.branch_exists(repo, "nope")
    assert obs.head_commit(repo) is not None
    assert obs.file_in_head(repo, "note.txt")
    assert not obs.file_in_head(repo, "absent.txt")


def test_git_state_observed_component_present(tmp_path):
    """methodology-floor is git-state observed (not gated): present in the clone -> OBSERVED."""
    o = orc.load_oracle(_MANIFEST_V120)
    clone = tmp_path / "clone"
    (clone / ".claude").mkdir(parents=True)
    (clone / ".claude" / "CLAUDE-FLOOR.md").write_text("floor\n", encoding="utf-8")
    r = obs.observe(_green_events(), o, clone=clone)
    floor = next(f for f in r.observed_not_gated if f.component_id == "methodology-floor")
    assert floor.verdict == obs.OBSERVED and floor.gated is False


def test_observe_spawn_extracts_structured_events(tmp_path):
    """observe_spawn reads a SpawnResult's on-disk transcript jsonl structurally."""
    cfg = tmp_path / "cfg"
    proj = cfg / "projects" / "slug"
    proj.mkdir(parents=True)
    lines = [json.dumps(e) for e in _green_events()]
    (proj / "t.jsonl").write_text("\n".join(lines), encoding="utf-8")
    result = sp.SpawnResult(exit_code=0, stdout="", events=[], transcript_path=None,
                            config_dir=cfg, work_dir=tmp_path)
    o = orc.load_oracle(_MANIFEST_V120)
    r = obs.observe_spawn(result, o)
    assert r.passed, r.summary()


# --- arc.py: GATE-0 (isolation-only) + consumer-shaping + leg-e silencer ---


def _spawn_result(stdout: str, exit_code: int = 0):
    return sp.SpawnResult(exit_code=exit_code, stdout=stdout, events=[], transcript_path=None,
                          config_dir=Path("does-not-exist"), work_dir=Path("."))


def test_gate_zero_proven_when_isolated_and_exit0():
    r = _spawn_result(f"...{arcmod.PROVENANCE_MARKER}... ARC DONE", exit_code=0)
    g = arcmod.evaluate_gate_zero(r)
    assert g.passed, g.summary()


def test_gate_zero_fails_when_provenance_absent():
    """No sentinel -> the child did not read OUR config -> isolation unproven."""
    g = arcmod.evaluate_gate_zero(_spawn_result("ARC DONE", exit_code=0))
    assert not g.passed and not g.provenance_present


def test_gate_zero_fails_when_outer_markers_leak():
    """An outer ~/.claude L0 marker in the child transcript -> isolation leaked."""
    r = _spawn_result(f"{arcmod.PROVENANCE_MARKER}\n[fleet] 3 issues", exit_code=0)
    g = arcmod.evaluate_gate_zero(r)
    assert not g.passed and not g.outer_markers_absent


def _wire_clone(tmp_path, scripts: dict[str, str]) -> Path:
    """A minimal clone whose .claude/settings.json WIRES the given scripts as hooks —
    the wiring-derived self-emission surface (Codex HIGH 2026-07-05 tightening)."""
    clone = tmp_path / "clone"
    (clone / "scripts").mkdir(parents=True)
    (clone / ".claude").mkdir()
    hooks = []
    for name, body in scripts.items():
        (clone / "scripts" / name).write_text(body, encoding="utf-8")
        hooks.append({"type": "command", "command": f'python "$CLAUDE_PROJECT_DIR/scripts/{name}"'})
    (clone / ".claude" / "settings.json").write_text(json.dumps(
        {"hooks": {"SessionStart": [{"matcher": "", "hooks": hooks}]}}), encoding="utf-8")
    return clone


def test_gate_zero_hub_self_clone_passes_253d(tmp_path):
    """[#253d] regression (the Step-7 failure): markers the clone's WIRED hooks legitimately
    emit ([fleet]/[changelog]) are invalid controls — filtered, so the self-clone passes;
    a merely-QUOTED marker ([closures] in an unwired script) stays a LIVE control."""
    clone = _wire_clone(tmp_path, {
        "fleet_health.py": 'print("[fleet] ok")',
        "changelog_sentinel.py": 'print("[changelog] x")'})
    (clone / "scripts" / "review_closures.py").write_text(
        'msg = "[closures] proposed"', encoding="utf-8")  # NOT wired -> not self-emittable
    r = _spawn_result(
        f"{arcmod.PROVENANCE_MARKER}\n[fleet] 2 issue(s) in 5 repos\n[changelog] claude-code",
        exit_code=0)
    g = arcmod.evaluate_gate_zero(r, clone=clone)
    assert g.passed, g.summary()
    assert g.control_markers == ("[closures]",)  # quoted-but-unwired stays live


def test_gate_zero_outer_only_marker_still_fails_253d(tmp_path):
    """A marker the clone can NOT self-emit remains a live control: its leak fails the gate."""
    clone = _wire_clone(tmp_path, {"fleet_health.py": 'print("[fleet] ok")'})
    leaked = _spawn_result(f"{arcmod.PROVENANCE_MARKER}\n[closures] 3 proposed", exit_code=0)
    g = arcmod.evaluate_gate_zero(leaked, clone=clone)
    assert not g.passed and not g.outer_markers_absent
    assert g.control_markers == ("[changelog]", "[closures]")  # [fleet] filtered, rest live
    clean = _spawn_result(arcmod.PROVENANCE_MARKER, exit_code=0)
    assert arcmod.evaluate_gate_zero(clean, clone=clone).passed


def test_outer_only_markers_real_hub_wiring_derived_253d():
    """On the REAL hub: [fleet]/[changelog] are wired-hook-emittable (filtered); [closures]
    is only QUOTED (surfaced by the global ~/.claude path, not the arc) -> stays a LIVE
    control (Codex HIGH 2026-07-05; both real frozen arcs emitted no [closures])."""
    assert arcmod.outer_only_markers(_REPO) == ("[closures]",)


def test_commit_shape_baseline_verifies_clean(tmp_path):
    """Baseline commit is CHECKED: success leaves porcelain-clean; a non-repo raises."""
    repo = _init_repo(tmp_path / "r")
    (repo / "shaped.txt").write_text("x\n", encoding="utf-8")
    arcmod.commit_shape_baseline(repo)  # commits the dirt, ends clean
    assert obs._git(repo, "status", "--porcelain").stdout.strip() == ""
    arcmod.commit_shape_baseline(repo)  # idempotent: nothing-to-commit tolerated
    not_repo = tmp_path / "not-a-repo"
    not_repo.mkdir()
    with pytest.raises(sp.SandboxError):
        arcmod.commit_shape_baseline(not_repo)


def test_outer_only_markers_none_clone_is_strict():
    """No clone -> no filtering: the full candidate set applies (the strict default)."""
    assert arcmod.outer_only_markers(None) == arcmod.OUTER_MARKER_CANDIDATES


def test_gate_zero_fails_on_nonzero_exit():
    """Codex false-green guard, extended to the arc: a crashed child never proves isolation."""
    r = _spawn_result(arcmod.PROVENANCE_MARKER, exit_code=1)
    assert not arcmod.evaluate_gate_zero(r).passed


def test_gate_zero_independent_of_hook_completeness():
    """[MF-1]: GATE-0 asserts ONLY isolation, never that the gated set fired -> it holds on the
    arc-silent freeze (a silenced hook does not fail the gate)."""
    r = _spawn_result(arcmod.PROVENANCE_MARKER, exit_code=0)  # zero hook signatures present
    assert arcmod.evaluate_gate_zero(r).passed


# --- G4 fidelity: skip-echo guard, vacuous tombstone, git-state probes ---


def test_skipped_hook_name_echo_is_not_fired_g4a():
    """G4a (measurement-#2 root ruling): pre-commit prints a hook's NAME even when it Skipped
    it — a skip line must yield ARMED-BUT-SKIPPED (ok-class, reported distinctly), never
    FIRED. Live risk: ai-council's toc-freshness is file-scoped to COUNCIL_QUESTION_GUIDE.md."""
    o = orc.load_oracle(_MANIFEST_V120)
    events = _tool_result(
        "ARCHITECTURE.md TOC freshness check..................(no files to check)Skipped")
    r = obs.observe(events, o)
    toc = next(f for f in r.gated_findings if f.component_id == "hub-toc-hooks")
    assert toc.verdict == obs.SKIPPED_ARMED
    assert "Skipped" in toc.evidence
    assert "armed-but-skipped" in r.summary()


def test_skip_echo_never_outranks_real_execution_g4a():
    """A hook that both Skipped once and RAN once (two commits) is FIRED — execution wins."""
    o = orc.load_oracle(_MANIFEST_V120)
    events = _tool_result(
        "ARCHITECTURE.md TOC freshness check..................(no files to check)Skipped\n"
        "ARCHITECTURE.md TOC freshness check..............................................Passed")
    r = obs.observe(events, o)
    toc = next(f for f in r.gated_findings if f.component_id == "hub-toc-hooks")
    assert toc.verdict == obs.FIRED


def test_tombstone_vacuous_when_no_commit_attempted_g4b():
    """G4b: with NO pre-commit stage output at all (the measurement-#2 shape — the child
    never reached `git commit`), the ruff tombstone's absence proves nothing -> VACUOUS,
    not CORRECTLY-ABSENT."""
    o = orc.load_oracle(_MANIFEST_V120)
    events = _tool_result("pre-commit installed at .git\\hooks\\pre-commit")
    r = obs.observe(events, o)
    ruff = next(f for f in r.gated_findings if f.component_id == "ruff-gate")
    assert ruff.verdict == obs.VACUOUS
    assert "no commit attempted" in ruff.evidence


def test_tombstone_absent_ok_when_stage_ran_g4b():
    """Any per-hook report line (Passed/Failed/Skipped trailer) proves the stage ran —
    absence is then genuine prune-conformance."""
    o = orc.load_oracle(_MANIFEST_V120)
    events = _tool_result("canonical_freshness last_reviewed gate..........Passed")
    r = obs.observe(events, o)
    ruff = next(f for f in r.gated_findings if f.component_id == "ruff-gate")
    assert ruff.verdict == obs.ABSENT_OK


def test_tombstone_skip_echo_is_still_a_regression_g4b():
    """A Skipped ruff line still means ruff is WIRED in the consumer's config — the prune
    failed. Skip-echo softens a positive verdict, never a tombstone."""
    o = orc.load_oracle(_MANIFEST_V120)
    events = _tool_result("Ruff linter..........................(no files to check)Skipped")
    r = obs.observe(events, o)
    ruff = next(f for f in r.gated_findings if f.component_id == "ruff-gate")
    assert ruff.verdict == obs.UNEXPECTED


def test_skip_echo_scoped_to_precommit_stage_codex_high():
    """Codex HIGH 2026-07-06: skip-echo semantics are pre-commit REPORT semantics — a
    session-start/stop hook whose real output happens to look skip-shaped is still FIRED
    (its line IS execution evidence; file-scope skipping does not exist at those stages)."""
    o = orc.load_oracle(_MANIFEST_V120)
    events = _tool_result(
        "Session-end backpressure..............(no files to check)Skipped")  # contrived shape
    r = obs.observe(events, o)
    seb = next(f for f in r.gated_findings if f.component_id == "session-end-backpressure")
    assert seb.verdict == obs.FIRED


def test_stage_ran_needs_precommit_report_shape_codex_high():
    """Codex HIGH 2026-07-06: a bare '...Passed' trailer in unrelated Bash output must not
    fake the pre-commit stage into having run — the tombstone stays VACUOUS."""
    o = orc.load_oracle(_MANIFEST_V120)
    events = _tool_result("pre-commit installed at .git/hooks/pre-commit")
    events += _tool_result("All 5 integration checks Passed")   # no dot-leader report shape
    r = obs.observe(events, o)
    ruff = next(f for f in r.gated_findings if f.component_id == "ruff-gate")
    assert ruff.verdict == obs.VACUOUS


def test_vacuous_tombstone_is_surfaced_as_a_flag_codex_med():
    """Codex MED 2026-07-06: VACUOUS is a gated failure — it must appear in `flags`, never
    yield 'FLAGGED ... flags: none'."""
    o = orc.load_oracle(_MANIFEST_V120)
    r = obs.observe(_tool_result("pre-commit installed at .git/hooks/pre-commit"), o)
    assert any(f.component_id == "ruff-gate" and f.verdict == obs.VACUOUS for f in r.flags)
    assert "ruff-gate:VACUOUS" in r.summary()


def test_git_state_plugin_probe_requires_exact_enablement_codex_med(tmp_path):
    """Codex MED 2026-07-06: `enabledPlugins` with a DIFFERENT plugin must not read as the
    tier1 declaration — exact JSON key check, never a substring."""
    o = orc.load_oracle(_MANIFEST_V120)
    clone = tmp_path / "clone"
    (clone / ".claude").mkdir(parents=True)
    (clone / ".claude" / "settings.json").write_text(json.dumps(
        {"enabledPlugins": {"some-other-plugin@elsewhere": True}}), encoding="utf-8")
    r = obs.observe([], o, clone=clone)
    plug = next(f for f in r.findings if f.component_id == "tier1-lifecycle-plugin")
    assert plug.verdict == obs.NOT_OBSERVED


def test_git_state_machine_level_path_not_probed_g4c():
    """G4c: a ~-rooted signature is machine-level state a clone cannot witness — the probe
    says so honestly instead of path-testing the signature's first token."""
    o = orc.load_oracle(_MANIFEST_V120)
    r = obs.observe([], o, clone=Path("."))
    codex = next(f for f in r.findings if f.component_id == "codex-agents-config")
    assert codex.verdict == obs.NOT_OBSERVED
    assert "unobservable from a clone" in codex.evidence


def test_git_state_settings_declared_enablement_g4c(tmp_path):
    """G4c: the tier1 plugin's git-state expectation is a settings DECLARATION, not a path —
    probe the clone's .claude/settings.json content (measurement #2 showed the old
    first-token path test could never observe it)."""
    o = orc.load_oracle(_MANIFEST_V120)
    clone = tmp_path / "clone"
    (clone / ".claude").mkdir(parents=True)
    (clone / ".claude" / "settings.json").write_text(json.dumps(
        {"enabledPlugins": {"tier1-lifecycle@dev-knowledge-methodology": True}}),
        encoding="utf-8")
    r = obs.observe([], o, clone=clone)
    plug = next(f for f in r.findings if f.component_id == "tier1-lifecycle-plugin")
    assert plug.verdict == obs.OBSERVED
    assert "declared in .claude/settings.json" in plug.evidence


# --- attachment-wrapped hook events (the on-disk transcript shape, Step-7 witnessed) ---


def _attachment_hook(stdout: str, command: str = "python x.py") -> dict:
    return {"type": "user", "attachment": {"type": "hook_success", "hookName": "Stop",
            "stdout": stdout, "command": command}}


def test_observer_reads_attachment_hook_stdout():
    """Hook firings land as {"attachment": {"type": "hook_success", stdout}} in the on-disk
    transcript — that stdout IS external evidence and must enter the hook-stdout channel."""
    assert "Session-end" in obs.hook_stdout_surface(
        [_attachment_hook("Session-end hygiene (deterministic backpressure)")])


def test_observer_attachment_command_field_never_counts():
    """The command field is config echo, not execution evidence (Step-7 witnessed: a hook
    succeeding SILENTLY leaves no transcript record at all, so a command string can never
    stand in for output). Matching it would fire on wiring alone."""
    ev = _attachment_hook("", command="python scripts/session_end_backpressure.py")
    assert "session_end_backpressure" not in obs.hook_stdout_surface([ev])


def test_observer_non_hook_attachment_excluded():
    ev = {"type": "user", "attachment": {"type": "task_reminder",
                                         "stdout": "canonical_freshness noise"}}
    assert "canonical_freshness" not in obs.hook_stdout_surface([ev])


# --- Step-7 seeding: ecosystem state + the tier1 plugin into the isolated config ---


def test_seed_ecosystem_state_copies_state_files(tmp_path):
    src = tmp_path / "src"
    (src / "ecosystem" / "repoA").mkdir(parents=True)
    (src / "ecosystem" / "repoA" / "state.yaml").write_text("ok: 1\n", encoding="utf-8")
    clone = tmp_path / "clone"
    clone.mkdir()
    seeded = arcmod.seed_ecosystem_state(src, clone)
    assert seeded == ["seeded ecosystem/repoA/state.yaml"]
    assert (clone / "ecosystem" / "repoA" / "state.yaml").read_text(encoding="utf-8") == "ok: 1\n"


def test_seed_tier1_plugin_installs_into_isolated_config(tmp_path):
    """The plugin is seeded clone-rooted (its own plugins/ tree) into the isolated config's
    cache + registration files, deterministically — the Stop hook / command act seam."""
    clone = tmp_path / "clone"
    meta = clone / "plugins" / "tier1-lifecycle" / ".claude-plugin"
    meta.mkdir(parents=True)
    (meta / "plugin.json").write_text('{"version": "9.9.9"}', encoding="utf-8")
    (clone / "plugins" / "tier1-lifecycle" / "hooks.json").write_text("{}", encoding="utf-8")
    cfg = tmp_path / "cfg"
    assert arcmod.seed_tier1_plugin(cfg, clone) == "9.9.9"
    install = cfg / "plugins" / "cache" / "dev-knowledge-methodology" / "tier1-lifecycle" / "9.9.9"
    assert (install / "hooks.json").exists()
    reg = json.loads((cfg / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))
    entry = reg["plugins"]["tier1-lifecycle@dev-knowledge-methodology"][0]
    assert entry["projectPath"] == str(clone) and entry["version"] == "9.9.9"
    market = json.loads((cfg / "plugins" / "known_marketplaces.json").read_text(encoding="utf-8"))
    assert market["dev-knowledge-methodology"]["source"] == {
        "source": "directory", "path": str(clone)}
    assert arcmod.seed_tier1_plugin(cfg, clone) == "9.9.9"  # idempotent re-seed


def test_seed_tier1_plugin_none_without_source(tmp_path):
    clone = tmp_path / "clone"
    clone.mkdir()
    assert arcmod.seed_tier1_plugin(tmp_path / "cfg", clone) is None


def test_seed_tier1_plugin_from_hub_source_root_g2(tmp_path):
    """G2 (measurement-#2 root ruling): a REAL consumer clone carries NO plugins/ tree (only
    the settings enablement) — seeding sources the HUB checkout, registers the marketplace
    at the hub path, and keeps projectPath on the CLONE (the project the child runs in)."""
    hub = tmp_path / "hub"
    meta = hub / "plugins" / "tier1-lifecycle" / ".claude-plugin"
    meta.mkdir(parents=True)
    (meta / "plugin.json").write_text('{"version": "1.2.0"}', encoding="utf-8")
    (hub / "plugins" / "tier1-lifecycle" / "hooks.json").write_text("{}", encoding="utf-8")
    clone = tmp_path / "consumer-clone"
    clone.mkdir()  # deliberately NO plugins/ tree — the real-consumer shape
    cfg = tmp_path / "cfg"
    assert arcmod.seed_tier1_plugin(cfg, clone, source_root=hub) == "1.2.0"
    install = cfg / "plugins" / "cache" / "dev-knowledge-methodology" / "tier1-lifecycle" / "1.2.0"
    assert (install / "hooks.json").exists()
    reg = json.loads((cfg / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))
    entry = reg["plugins"]["tier1-lifecycle@dev-knowledge-methodology"][0]
    assert entry["projectPath"] == str(clone)      # the child's project stays the clone
    market = json.loads((cfg / "plugins" / "known_marketplaces.json").read_text(encoding="utf-8"))
    assert market["dev-knowledge-methodology"]["source"] == {
        "source": "directory", "path": str(hub)}   # the marketplace is the hub, as on a real machine


# --- [#253a] the arc permission seam: scoped allowlist, never bypass ---


def test_isolated_config_seeds_scoped_allowlist_253a(tmp_path):
    """The harness owns the child's config: it seeds EXACTLY the arc-op allowlist,
    deterministically, and never any bypass escape."""
    cfg = sp.write_isolated_config(tmp_path / "cfg", session_start_marker="M",
                                   allow_rules=arcmod.ARC_ALLOW_RULES)
    raw = (cfg / "settings.json").read_text(encoding="utf-8")
    settings = json.loads(raw)
    assert settings["permissions"]["allow"] == list(arcmod.ARC_ALLOW_RULES)
    assert "bypassPermissions" not in raw and "defaultMode" not in raw
    # Deterministic: a second write yields byte-identical settings.
    sp.write_isolated_config(tmp_path / "cfg2", session_start_marker="M",
                             allow_rules=arcmod.ARC_ALLOW_RULES)
    assert raw == (tmp_path / "cfg2" / "settings.json").read_text(encoding="utf-8")


def test_isolated_config_without_rules_stays_minimal_253a(tmp_path):
    """Slice-A callers (prove-isolation) are unchanged: no allow_rules -> no permissions key."""
    cfg = sp.write_isolated_config(tmp_path / "cfg")
    assert "permissions" not in json.loads((cfg / "settings.json").read_text(encoding="utf-8"))


def test_arc_allow_rules_are_scoped_to_the_arc_253a():
    """Every rule names a specific arc operation — no blanket Bash, no wildcard tool grant."""
    for rule in arcmod.ARC_ALLOW_RULES:
        assert rule != "*" and not rule.startswith(("Bash(*", "Bash(:")), rule
    bash_rules = [r for r in arcmod.ARC_ALLOW_RULES if r.startswith("Bash(")]
    assert all(r.startswith("Bash(git ") for r in bash_rules)  # only the git arc ops
    assert "SlashCommand(/review-closures)" in arcmod.ARC_ALLOW_RULES  # the one command act


def test_arc_allow_rules_narrowed_to_exact_arc_ops_codex_high():
    """Codex HIGH 2026-07-06: checkout/add are EXACT commands, commit is pinned to its `-m`
    form — `git checkout <other>`, `git add <path>`, and above all `git commit --no-verify`
    (a silent bypass of the very gates being measured) all still hit the permission wall."""
    assert "Bash(git checkout -b feat/sandbox-arc)" in arcmod.ARC_ALLOW_RULES
    assert "Bash(git add -A)" in arcmod.ARC_ALLOW_RULES
    assert "Bash(git commit -m:*)" in arcmod.ARC_ALLOW_RULES
    for broad in ("Bash(git checkout:*)", "Bash(git add:*)", "Bash(git commit:*)"):
        assert broad not in arcmod.ARC_ALLOW_RULES, broad


def test_arc_prompt_references_config_sanction_g3():
    """G3 (supersedes the [#253a] self-legitimizing preamble): the prompt only REFERENCES the
    owned-config sanction — it no longer asserts its own authority (measurement #2 witnessed
    a floor-carrying child rightly refusing a prompt-embedded authority claim as injection)."""
    p = arcmod.ARC_PROMPT
    assert "CLAUDE.md" in p and "consent" in p.lower()
    assert "SANCTIONED test-harness" not in p        # the superseded self-legitimizing claim
    assert "This work is authorized" not in p        # authority claims live in the config now
    # The mechanics are unchanged: same four steps, same refusals, same terse reply contract.
    for step in ("git checkout -b feat/sandbox-arc", "SANDBOX_ARC.md",
                 "git add -A && git commit", "/review-closures", "Do NOT push", "ARC DONE"):
        assert step in p


def test_sanction_lands_as_user_level_claude_md_g3(tmp_path):
    """G3: the sanction is written as the isolated profile's own CLAUDE.md — the principal's
    channel — by the ONE shared builder both arc paths use (the measurement-#2 failure was
    exactly this seam existing on one path only)."""
    cfg = arcmod.arc_isolated_config(tmp_path / "cfg")
    text = (cfg / "CLAUDE.md").read_text(encoding="utf-8")
    assert text == arcmod.ARC_SANCTION
    # Scoped consent: the four arc operations, the floor otherwise intact, no blanket grant.
    for needle in ("feat/sandbox-arc", "SANDBOX_ARC.md", "/review-closures",
                   "remains fully in force", "do not push"):
        assert needle in text
    # And the settings side carries the [#253a] allowlist (full parity through the builder).
    raw = (cfg / "settings.json").read_text(encoding="utf-8")
    assert json.loads(raw)["permissions"]["allow"] == list(arcmod.ARC_ALLOW_RULES)
    assert "bypassPermissions" not in raw


def test_sanction_never_carries_the_provenance_marker_g3():
    """GATE-0 soundness guard: the sanction text can echo into the child transcript, so the
    LITERAL provenance token inside it would hand the positive control a false-positive
    channel (marker present without the SessionStart hook firing). Prefix mention only."""
    assert arcmod.PROVENANCE_MARKER not in arcmod.ARC_SANCTION
    assert "LSANDBOX" in arcmod.ARC_SANCTION  # the explanation stays (prefix, not the token)


def test_write_isolated_config_without_sanction_writes_no_claude_md_g3(tmp_path):
    """Slice-A callers (prove-isolation) are unchanged: no sanction -> no CLAUDE.md."""
    cfg = sp.write_isolated_config(tmp_path / "cfg", session_start_marker="M")
    assert not (cfg / "CLAUDE.md").exists()


_RUFF_EXPECTED_BLOCK = {
    "repos": [{
        "repo": "https://github.com/astral-sh/ruff-pre-commit",
        "rev": "v0.15.5",
        "hooks": [{"id": "ruff",
                   "name": "Ruff lint gate (Tier-1, pinned rev; blocks on violations)",
                   "args": []}],
    }],
}


def test_consumer_shape_prunes_ruff(tmp_path):
    """The precommit remove-leg actually removes the seeded ruff block -> prune-conformance."""
    clone = tmp_path / "clone"
    clone.mkdir()
    import yaml
    (clone / ".pre-commit-config.yaml").write_text(
        yaml.safe_dump(_RUFF_EXPECTED_BLOCK, sort_keys=False), encoding="utf-8")
    changes = arcmod.consumer_shape(clone, repo_root=_REPO)
    after = (clone / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "ruff-pre-commit" not in after
    assert any("removed repo entry" in c for c in changes)


def test_consumer_shape_drops_hub_local_ruff(tmp_path):
    """Step-7 finding: the hub carries ruff INSIDE `repo: local` — the repo-entry prune
    classifies it 'already absent' and leaves it RUNNING. Consumer shape must drop it."""
    clone = tmp_path / "clone"
    clone.mkdir()
    import yaml
    (clone / ".pre-commit-config.yaml").write_text(yaml.safe_dump({"repos": [
        {"repo": "local", "hooks": [
            {"id": "ruff", "name": "Ruff linter (version-pinned)", "entry": "ruff check"},
            {"id": "canonical_freshness"}]}]}, sort_keys=False), encoding="utf-8")
    changes = arcmod.consumer_shape(clone, repo_root=_REPO)
    after = (clone / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "Ruff linter" not in after and "id: ruff" not in after
    assert "canonical_freshness" in after  # the rest of the local block survives
    assert any("removed hub-local ruff hook" in c for c in changes)


def test_disable_precommit_hook_silences_one(tmp_path):
    """leg-e: dropping a gated hook by id removes exactly it, preserving the rest."""
    clone = tmp_path / "clone"
    clone.mkdir()
    import yaml
    (clone / ".pre-commit-config.yaml").write_text(yaml.safe_dump({"repos": [
        {"repo": "local", "hooks": [{"id": "canonical_freshness"}, {"id": "floor-hash-verify"}]}]},
        sort_keys=False), encoding="utf-8")
    assert arcmod.disable_precommit_hook(clone, "canonical_freshness")
    after = (clone / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "canonical_freshness" not in after
    assert "floor-hash-verify" in after  # the others survive
    assert not arcmod.disable_precommit_hook(clone, "canonical_freshness")  # idempotent


@pytest.mark.skipif(shutil.which("claude") is None or not os.environ.get("LIVED_SANDBOX_LIVE"),
                    reason="live arc: set LIVED_SANDBOX_LIVE=1, have `claude` on PATH + a key")
def test_live_arc_gate_zero_holds():
    """Live GATE-0 under real work — never runs in offline CI (Step 7 operator freeze)."""
    run = arcmod.run_arc(model="haiku")
    assert run.gate.passed, run.gate.summary()


# --- cli.py: observe-arc dispatch + the [MC-2] scrub guard ---


def test_cli_usage_on_unknown_subcommand():
    from lived_sandbox import cli
    assert cli.main(["nonsense"]) == 2
    assert cli.main([]) == 2


def test_cli_observe_arc_is_a_known_subcommand():
    """observe-arc dispatches (does not hit the usage path). Monkeypatch run_arc to stay offline."""
    from lived_sandbox import arc as _arc
    from lived_sandbox import cli

    def fake_run(**_kw):
        gate = _arc.GateZero(True, True, True)
        return _arc.ArcRun(exit_code=0, gate=gate,
                           observation=obs.observe(_green_events(), orc.load_oracle(_MANIFEST_V120)),
                           transcript_jsonl="", changes=())
    orig = _arc.run_arc
    _arc.run_arc = fake_run
    try:
        assert cli.main(["observe-arc"]) == 0  # gate passed, nothing to freeze
    finally:
        _arc.run_arc = orig


def test_cli_leg_e_target_parsing():
    from lived_sandbox import cli
    assert cli._leg_e_target(["observe-arc"]) is None
    assert cli._leg_e_target(["observe-arc", "--leg-e", "toc-freshness"]) == "toc-freshness"
    assert cli._leg_e_target(["observe-arc", "--leg-e", "--freeze"]) == cli._LEG_E_DEFAULT


def test_cli_freeze_arc_scrub_rejects_key(tmp_path, monkeypatch):
    """[MC-2]: a transcript carrying an sk-ant- key is REFUSED, never frozen."""
    from lived_sandbox import arc as _arc
    from lived_sandbox import cli
    monkeypatch.setattr(cli, "_FIXTURES", tmp_path / "fx")
    run = _arc.ArcRun(exit_code=0, gate=_arc.GateZero(True, True, True),
                      observation=obs.observe([], orc.load_oracle(_MANIFEST_V120)),
                      transcript_jsonl='{"k":"sk-ant-DEADBEEFdeadbeef"}', changes=())
    with pytest.raises(sp.SandboxError):
        cli._freeze_arc(run, "arc-green.jsonl")
    assert not (tmp_path / "fx" / "arc-green.jsonl").exists()  # refused before writing


def test_cli_freeze_arc_writes_clean_fixture(tmp_path, monkeypatch):
    from lived_sandbox import arc as _arc
    from lived_sandbox import cli
    monkeypatch.setattr(cli, "_FIXTURES", tmp_path / "fx")
    run = _arc.ArcRun(exit_code=0, gate=_arc.GateZero(True, True, True),
                      observation=obs.observe([], orc.load_oracle(_MANIFEST_V120)),
                      transcript_jsonl='{"type":"user","content":"floor-hash-verify Passed"}',
                      changes=())
    assert cli._freeze_arc(run, "arc-green.jsonl") == "arc-green.jsonl"
    assert (tmp_path / "fx" / "arc-green.jsonl").exists()


# ===========================================================================
# ACCEPTANCE — C3 + C4 discrimination against the REAL frozen fixtures.
# These are the CLOSURE proof ([#252]). Skip-gated until the operator's live freeze
# (Step 7) produces arc-green.jsonl + arc-silent.jsonl; both green offline == closure.
# The two directions TOGETHER pin discrimination (Q2 ruling): arc-green -> no
# false-positive, arc-silent -> no false-negative. A silent-only assertion could pass
# with an observer that flags everything, so both are required.
# ===========================================================================

_FIXTURES = _REPO / "tests" / "fixtures" / "lived-workflow"
_ARC_GREEN = _FIXTURES / "arc-green.jsonl"
_ARC_SILENT = _FIXTURES / "arc-silent.jsonl"
_SECRET_RE = re.compile(r"sk-ant-[A-Za-z0-9_-]{8}")
_needs_fixtures = pytest.mark.skipif(
    not (_ARC_GREEN.exists() and _ARC_SILENT.exists()),
    reason="arc fixtures not captured — run cli observe-arc --freeze [+ --leg-e] (Step 7)")


def _events_from_fixture(path: Path) -> list[dict]:
    events: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


@_needs_fixtures
def test_acceptance_arc_green_all_gated_engaged_no_false_positive():
    """C3: the arc engages all gated + >=1 command act, observed GREEN — no false-positive.
    G4a recalibration (measurement-#2 root ruling): the two file-scoped pre-commit hooks
    (hub-toc-hooks, floor-hash-verify) are reported by pre-commit as Skipped for the arc's
    single-file commit — the frozen fixture proves they were name-echoes, so they are now
    honestly ARMED-BUT-SKIPPED (wired + consulted, ok-class), never conflated with FIRED.
    The four hooks that genuinely produced output stay FIRED. Same fixture, uninflated read."""
    o = orc.load_oracle(_MANIFEST_V120)
    r = obs.observe(_events_from_fixture(_ARC_GREEN), o, clone=None)
    assert r.passed, r.summary()
    fired = {f.component_id for f in r.gated_findings if f.verdict == obs.FIRED}
    armed = {f.component_id for f in r.gated_findings if f.verdict == obs.SKIPPED_ARMED}
    assert fired == {"floor-sessionstart-guard", "canonical-freshness",
                     "session-end-backpressure", "propose-closures-stop-hook"}
    assert armed == {"hub-toc-hooks", "floor-hash-verify-hook", "hub-codemap-hooks"}
    assert fired | armed == _GATED_SET          # every gated hook engaged — nothing silent
    assert len(r.commands_observed) >= 1        # >=1 command acts and is observed
    assert not r.flags


@_needs_fixtures
def test_acceptance_arc_silent_catches_seeded_silence():
    """C4: with one gated hook disabled, the observer FLAGS the silence — no false-negative."""
    o = orc.load_oracle(_MANIFEST_V120)
    r = obs.observe(_events_from_fixture(_ARC_SILENT), o, clone=None)
    assert not r.passed
    assert r.silences, "the seeded EXPECTED-BUT-SILENT hook must be flagged"


@_needs_fixtures
def test_acceptance_discrimination_is_closure_C4():
    """THE closure proof: the SAME observer greens arc-green AND flags arc-silent. Both
    directions together pin discrimination (the real C4 necessary condition)."""
    o = orc.load_oracle(_MANIFEST_V120)
    green = obs.observe(_events_from_fixture(_ARC_GREEN), o)
    silent = obs.observe(_events_from_fixture(_ARC_SILENT), o)
    assert green.passed and not silent.passed, (
        f"green={green.summary()} | silent={silent.summary()}")


@_needs_fixtures
def test_acceptance_fixtures_carry_no_secret():
    """[MC-2] belt-and-braces: no sk-ant- key survived into a committed fixture."""
    for p in (_ARC_GREEN, _ARC_SILENT):
        assert not _SECRET_RE.search(p.read_text(encoding="utf-8")), p.name
