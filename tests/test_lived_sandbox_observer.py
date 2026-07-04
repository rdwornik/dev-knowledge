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

# The six gated firing-hook signatures as authored in manifest-v1.2.0.yaml.
_SIX_SIGNATURES = [
    "check_floor_hash", "floor-hash-verify", "canonical_freshness",
    "toc-freshness", "session_end_backpressure", "closure",
]


def _tool_result(text: str) -> dict:
    """A user message carrying a tool_result (Bash stdout / hook output) — external evidence."""
    return {"type": "user", "message": {"role": "user",
            "content": [{"type": "tool_result", "content": text}]}}


def _assistant_text(text: str) -> dict:
    """Assistant narration — the FORBIDDEN channel (must never enter hook-stdout)."""
    return {"type": "assistant", "message": {"role": "assistant",
            "content": [{"type": "text", "text": text}]}}


def _tool_use(name: str, command: str) -> dict:
    return {"type": "assistant", "message": {"role": "assistant",
            "content": [{"type": "tool_use", "name": name, "input": {"command": command}}]}}


def _green_events():
    """All six hook signatures in REAL tool-result stdout + a command act; ruff absent."""
    evs = [_tool_result(f"pre-commit hook fired: {s}....Passed") for s in _SIX_SIGNATURES]
    evs.append(_tool_use("SlashCommand", "/review-closures"))
    return evs

_GATED_SIX = {
    "floor-sessionstart-guard",
    "floor-hash-verify-hook",
    "canonical-freshness",
    "hub-toc-hooks",
    "session-end-backpressure",
    "propose-closures-stop-hook",
}


# --- the engages oracle (C2 data, loaded — not hand-coded) ---


def test_oracle_loads_the_real_v120_manifest():
    o = orc.load_oracle(_MANIFEST_V120)
    assert o.version == "1.2.0"
    assert len(o.expectations) == 13  # every component carries a triple


def test_oracle_gated_active_is_exactly_the_six():
    o = orc.load_oracle(_MANIFEST_V120)
    assert {e.component_id for e in o.gated_active} == _GATED_SIX


def test_oracle_ruff_tombstone_is_gated_absent():
    o = orc.load_oracle(_MANIFEST_V120)
    assert {e.component_id for e in o.gated_absent} == {"ruff-gate"}
    ruff = o.by_id("ruff-gate")
    assert ruff.absent is True and ruff.signature == "Ruff lint gate"


def test_oracle_observed_not_gated_excludes_the_six():
    o = orc.load_oracle(_MANIFEST_V120)
    ids = {e.component_id for e in o.observed_not_gated}
    assert _GATED_SIX.isdisjoint(ids)
    assert "methodology-floor" in ids          # git-state channel -> observed, not gated
    assert "review-closures-command" in ids    # operator-invoke -> OUT-OF-ARC


def test_oracle_string_expect_is_present_signature():
    o = orc.load_oracle(_MANIFEST_V120)
    canon = o.by_id("canonical-freshness")
    assert canon.signature == "canonical_freshness" and canon.absent is False


def test_oracle_load_for_version_resolves_the_manifest():
    o = orc.load_for_version("1.2.0")
    assert {e.component_id for e in o.gated_active} == _GATED_SIX


def test_oracle_empty_expect_raises():
    with pytest.raises(orc.OracleError):
        orc._parse_expect("x", "   ")


def test_oracle_absent_mapping_without_signature_raises():
    with pytest.raises(orc.OracleError):
        orc._parse_expect("x", {"absent": True})


# --- the observer: gated verdict over the external channels ---


def test_observer_green_when_all_six_fired():
    o = orc.load_oracle(_MANIFEST_V120)
    r = obs.observe(_green_events(), o)
    assert r.passed, r.summary()
    assert {f.component_id for f in r.gated_findings if f.verdict == obs.FIRED} == _GATED_SIX
    assert not r.flags


def test_observer_flags_one_silent_hook():
    """A single gated firing hook whose stdout is absent -> EXPECTED-BUT-SILENT -> not passed."""
    o = orc.load_oracle(_MANIFEST_V120)
    # Drop the canonical_freshness signal (one of the six).
    events = [e for e in _green_events()
              if "canonical_freshness" not in obs.hook_stdout_surface([e])]
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
    events = _green_events() + [_tool_result("Ruff lint gate....Passed")]
    r = obs.observe(events, o)
    assert not r.passed
    assert any(f.component_id == "ruff-gate" and f.verdict == obs.UNEXPECTED for f in r.flags)


def test_observer_ignores_inner_narration_C1():
    """C1 (THE proof): the six signatures appearing ONLY in assistant *narration* must NOT
    count as firing — the observer flags them SILENT. Verify-by-state, never by narration."""
    o = orc.load_oracle(_MANIFEST_V120)
    narrated = [_assistant_text(
        "I ran all the hooks: " + " ".join(f"{s}....Passed" for s in _SIX_SIGNATURES)
        + " and /review-closures — everything is green.")]
    r = obs.observe(narrated, o)
    assert not r.passed, "narration must never produce a green verdict"
    assert {f.component_id for f in r.silences} == _GATED_SIX


def test_observer_narration_excluded_from_hook_surface():
    """The hook-stdout channel is event-type keyed ([NB-2]): a signature in an assistant
    text item is absent from the surface; the same signature in a tool_result is present."""
    assert "canonical_freshness" not in obs.hook_stdout_surface(
        [_assistant_text("canonical_freshness passed")])
    assert "canonical_freshness" in obs.hook_stdout_surface(
        [_tool_result("canonical_freshness passed")])


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


def test_gate_zero_fails_on_nonzero_exit():
    """Codex false-green guard, extended to the arc: a crashed child never proves isolation."""
    r = _spawn_result(arcmod.PROVENANCE_MARKER, exit_code=1)
    assert not arcmod.evaluate_gate_zero(r).passed


def test_gate_zero_independent_of_hook_completeness():
    """[MF-1]: GATE-0 asserts ONLY isolation, never that the six fired -> it holds on the
    arc-silent freeze (a silenced hook does not fail the gate)."""
    r = _spawn_result(arcmod.PROVENANCE_MARKER, exit_code=0)  # zero hook signatures present
    assert arcmod.evaluate_gate_zero(r).passed


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
def test_acceptance_arc_green_all_six_fired_no_false_positive():
    """C3: the arc fires all six + >=1 command act, observed GREEN — no false-positive."""
    o = orc.load_oracle(_MANIFEST_V120)
    r = obs.observe(_events_from_fixture(_ARC_GREEN), o, clone=None)
    assert r.passed, r.summary()
    assert {f.component_id for f in r.gated_findings if f.verdict == obs.FIRED} == _GATED_SIX
    assert len(r.commands_observed) >= 1  # >=1 command acts and is observed
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
