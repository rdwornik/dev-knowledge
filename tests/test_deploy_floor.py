"""Tests for the per-repo methodology-floor carrier (ADR-92 C4).

Covers the (three-state) reconcile model on the floor carrier
(deploy/carrier_floor.py) against the ADR-92 contract:

- absent floor: ABSENT -> apply -> verify passes (floor + sidecar written under the
  consumer's .claude/);
- drifted (floor edited / sidecar missing / sidecar stale): PRESENT_DRIFTED -> apply
  -> verify;
- idempotency: apply then apply again writes nothing (byte-identical);
- arm-leg STAGE CARDINALITY (#290): verify FAILs a 1-stage-armed consumer (naming the
  dormant stages) and one re-deploy self-heals it in place, touching only the arm;
- verify reports failures rather than silently passing;
- detect/verify INDEPENDENCE (D9): each survives the other's judgment helper being
  sabotaged;
- the carrier writes ONLY the consumer tree — apply() does NOT refresh the HUB's
  templates/child-methodology-floor.sha256 anchor (the differentiator from shelling
  out to generate_floor.py generate --out-dir).

The consumer is a temp dir; the floor is rendered from the real hub template. No
network, no real consumer repos, and the hub tree is left untouched.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_floor as cf  # noqa: E402
import contract  # noqa: E402

_FLOOR_TARGET = {
    "floor_path": ".claude/CLAUDE-FLOOR.md",
    "sidecar_path": ".claude/CLAUDE-FLOOR.md.sha256",
}

# Oracle: the corpus-state floor body + digest, computed independently of the
# carrier's own helper (straight from the hub generator's public functions).
_FLOOR_BODY = cf.gf.render_floor()
_FLOOR_DIGEST = cf.gf.floor_sha256(_FLOOR_BODY)


def _carrier(repo: Path) -> cf.FloorCarrier:
    return cf.FloorCarrier(repo)


def _floor_file(repo: Path) -> Path:
    return repo / ".claude" / "CLAUDE-FLOOR.md"


def _sidecar_file(repo: Path) -> Path:
    return repo / ".claude" / "CLAUDE-FLOOR.md.sha256"


def _hook_script(repo: Path) -> Path:
    return repo / ".claude" / "check_floor_hash.py"


def _claude_md(repo: Path) -> Path:
    return repo / "CLAUDE.md"


def _gitignore(repo: Path) -> Path:
    return repo / ".gitignore"


def _settings(repo: Path) -> Path:
    return repo / ".claude" / "settings.json"


# ---------------------------------------------------------------------------
# absent -> apply -> verify
# ---------------------------------------------------------------------------


def test_absent_detects_then_applies_and_verifies(tmp_path):
    car = _carrier(tmp_path)
    assert not _floor_file(tmp_path).exists()
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.ABSENT

    result = car.apply(_FLOOR_TARGET)
    assert result.changed is True
    # armed set on a bare consumer: floor + sidecar + hook script + @-include +
    # .gitignore negation block + settings.json SessionStart hook (structured output).
    assert len(result.changes) == 6

    assert _floor_file(tmp_path).exists()
    assert _sidecar_file(tmp_path).exists()
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_FLOOR_TARGET).ok is True


def test_apply_writes_floor_and_sidecar_matching_hub_render(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    # floor body is byte-for-byte the hub render (LF-normalized read to be autocrlf-proof)
    assert cf.gf.normalize(_floor_file(tmp_path).read_text(encoding="utf-8")) == _FLOOR_BODY
    # sidecar records the matching content-integrity digest
    assert cf._read_sidecar_hash(_sidecar_file(tmp_path)) == _FLOOR_DIGEST


def test_floor_written_under_consumer_claude_dir(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    assert (tmp_path / ".claude").is_dir()  # the consumer's own CC config dir, created


# ---------------------------------------------------------------------------
# drifted -> reconcile (three drift shapes)
# ---------------------------------------------------------------------------


def test_drifted_floor_edited_detects_then_reconciles(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    # tamper the floor body — content hash no longer matches the corpus digest.
    _floor_file(tmp_path).write_text(_FLOOR_BODY + "\nTAMPER\n", encoding="utf-8", newline="\n")
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    result = car.apply(_FLOOR_TARGET)
    assert result.changed is True
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_FLOOR_TARGET).ok is True


def test_drifted_sidecar_missing_detects_drifted(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _sidecar_file(tmp_path).unlink()  # floor intact, sidecar gone
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    car.apply(_FLOOR_TARGET)
    assert car.verify(_FLOOR_TARGET).ok is True


def test_drifted_sidecar_stale_detects_drifted(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _sidecar_file(tmp_path).write_text("0" * 64 + "\n", encoding="utf-8", newline="\n")
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    car.apply(_FLOOR_TARGET)
    assert cf._read_sidecar_hash(_sidecar_file(tmp_path)) == _FLOOR_DIGEST  # re-pinned
    assert car.verify(_FLOOR_TARGET).ok is True


# ---------------------------------------------------------------------------
# idempotency — apply twice writes nothing the second time
# ---------------------------------------------------------------------------


def test_apply_is_idempotent(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    floor_before = _floor_file(tmp_path).read_bytes()
    sidecar_before = _sidecar_file(tmp_path).read_bytes()

    second = car.apply(_FLOOR_TARGET)
    assert second.changed is False
    assert second.changes == ()
    assert _floor_file(tmp_path).read_bytes() == floor_before
    assert _sidecar_file(tmp_path).read_bytes() == sidecar_before


# ---------------------------------------------------------------------------
# verify reports failures (not a silent pass)
# ---------------------------------------------------------------------------


def test_verify_on_absent_floor_is_not_ok(tmp_path):
    result = _carrier(tmp_path).verify(_FLOOR_TARGET)
    assert result.ok is False
    assert any("floor absent" in f for f in result.failures)


def test_verify_reports_floor_and_sidecar_failures(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _floor_file(tmp_path).write_text(_FLOOR_BODY + "\nTAMPER\n", encoding="utf-8", newline="\n")
    _sidecar_file(tmp_path).unlink()
    failures = car.verify(_FLOOR_TARGET).failures
    assert any("floor content hash" in f for f in failures)
    assert any("sidecar absent" in f for f in failures)


# ---------------------------------------------------------------------------
# D9 — verify is independent of detect (no shared correctness-judgment path)
# ---------------------------------------------------------------------------


def test_verify_does_not_route_through_detect_classifier(tmp_path, monkeypatch):
    """Sabotage detect's judgment (_classify_floor); verify must still pass."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("verify must not call detect's _classify_floor (D9)")

    monkeypatch.setattr(cf, "_classify_floor", _boom)
    assert car.verify(_FLOOR_TARGET).ok is True  # independent path — unaffected


def test_detect_does_not_route_through_verify_judge(tmp_path, monkeypatch):
    """Sabotage verify's judgment (_verify_floor); detect must still classify."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)

    def _boom(*_a, **_k):
        raise AssertionError("detect must not call verify's _verify_floor (D9)")

    monkeypatch.setattr(cf, "_verify_floor", _boom)
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT


# ---------------------------------------------------------------------------
# consumer-scoped — apply() never mutates the HUB canonical SHA anchor
# ---------------------------------------------------------------------------


def test_apply_does_not_refresh_hub_canonical_sha(tmp_path):
    # The differentiator from `generate_floor.py generate --out-dir` (which refreshes
    # the hub anchor as a side-effect): this carrier writes ONLY the consumer tree.
    hub_anchor = cf.gf.HUB_CANONICAL_SHA
    assert hub_anchor.exists()
    before = hub_anchor.read_bytes()

    _carrier(tmp_path).apply(_FLOOR_TARGET)

    assert hub_anchor.read_bytes() == before  # hub anchor untouched


# ---------------------------------------------------------------------------
# ARMING (ADR-93) — apply does not merely drop content; it arms the floor so a
# fresh clone self-arms. Six artifacts; PRESENT_CORRECT requires ALL.
# ---------------------------------------------------------------------------


def test_apply_writes_canonical_guard_script(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    # The one canonical guard both legs run, single-sourced from the hub generator.
    assert _hook_script(tmp_path).exists()
    assert (
        _hook_script(tmp_path).read_text(encoding="utf-8")
        == cf.gf.CHECK_FLOOR_HASH_SCRIPT
    )


def test_apply_adds_at_include_to_claude_md(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    assert cf.INCLUDE_LINE in _claude_md(tmp_path).read_text(encoding="utf-8")


def test_apply_inserts_include_after_frontmatter_preserving_content(tmp_path):
    existing = "---\nlast_reviewed: 2026-06-02\n---\n\n# CLAUDE.md — Consumer\nBody.\n"
    _claude_md(tmp_path).write_text(existing, encoding="utf-8", newline="\n")
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    text = _claude_md(tmp_path).read_text(encoding="utf-8")
    assert cf.INCLUDE_LINE in text
    assert "# CLAUDE.md — Consumer" in text and "Body." in text  # content preserved
    # include sits after the frontmatter close, before the H1
    assert text.index(cf.INCLUDE_LINE) > text.index("last_reviewed")
    assert text.index(cf.INCLUDE_LINE) < text.index("# CLAUDE.md — Consumer")


def test_apply_rewrites_bare_claude_gitignore_to_contents_form(tmp_path):
    _gitignore(tmp_path).write_text("# Claude\n.claude/\n", encoding="utf-8", newline="\n")
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    lines = [ln.strip() for ln in _gitignore(tmp_path).read_text(encoding="utf-8").splitlines()]
    assert ".claude/" not in lines  # bare dir form replaced (defeats negations, #138)
    assert ".claude/*" in lines
    for neg in ("!.claude/CLAUDE-FLOOR.md", "!.claude/CLAUDE-FLOOR.md.sha256",
                "!.claude/check_floor_hash.py"):
        assert neg in lines


def test_apply_adds_sessionstart_guard_with_both_legs(tmp_path):
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    data = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    cmds = [
        h["command"]
        for g in data["hooks"]["SessionStart"]
        for h in g["hooks"]
    ]
    # verify leg runs --require-present so a deleted-but-tracked floor fails loud (ADR-93)
    assert any("check_floor_hash.py --require-present" in c for c in cmds)
    assert any("pre_commit install" in c for c in cmds)           # bootstrap arm leg


def test_apply_arms_all_three_hook_stages(tmp_path):
    """#275b: the SessionStart arm command the carrier writes arms ALL THREE hook stages
    (pre-commit / commit-msg / pre-push), not just pre-commit — else commit-msg / pre-push
    stage hooks land wired-but-dormant on a fresh consumer."""
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    data = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    cmds = [h["command"] for g in data["hooks"]["SessionStart"] for h in g["hooks"]]
    arm = next(c for c in cmds if "pre_commit install" in c)
    for tok in ("-t pre-commit", "-t commit-msg", "-t pre-push"):
        assert tok in arm, f"arm cmd missing {tok!r} (#275b): {arm!r}"


def test_apply_merges_sessionstart_preserving_existing_settings(tmp_path):
    existing = {"enabledPlugins": {"tier1-lifecycle@dev-knowledge-methodology": True}}
    _settings(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    _settings(tmp_path).write_text(json.dumps(existing), encoding="utf-8", newline="\n")
    _carrier(tmp_path).apply(_FLOOR_TARGET)
    data = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    assert data["enabledPlugins"] == existing["enabledPlugins"]  # preserved
    assert data["hooks"]["SessionStart"]                          # guard added


# ---------------------------------------------------------------------------
# ARM-LEG STAGE CARDINALITY (#290) — the teeth + the self-heal. A consumer armed by a
# pre-#275b deploy carries a bare 1-stage `pre_commit install`; verify must FAIL it, and one
# re-deploy must heal it without disturbing anything else.
# ---------------------------------------------------------------------------

_ONE_STAGE_ARM = "python -m pre_commit install"  # the pre-#275b arm leg, verbatim


def _rewrite_arm_leg(repo: Path, command: str) -> None:
    """Put `command` in place of the armed settings.json's arm leg (nothing else moves)."""
    data = json.loads(_settings(repo).read_text(encoding="utf-8"))
    for group in data["hooks"]["SessionStart"]:
        for hook in group["hooks"]:
            if "pre_commit install" in hook["command"]:
                hook["command"] = command
    _settings(repo).write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def _arm_commands(repo: Path) -> list[str]:
    """Every SessionStart command mentioning `install` — deliberately a BROADER filter than
    the carrier's own `_is_arm_command`, so a test can see a leg the carrier does not
    recognise (and catch a leg the carrier wrongly rewrote or duplicated)."""
    data = json.loads(_settings(repo).read_text(encoding="utf-8"))
    return [
        h["command"]
        for g in data["hooks"]["SessionStart"]
        for h in g["hooks"]
        if "install" in h["command"]
    ]


def test_stage_cardinality_is_single_sourced_from_the_hub_self_arm():
    """No second source of truth for stage cardinality (#290): the carrier's expectation IS
    the hub's own self-arm list, and the command it writes is derived from it."""
    import arm_hooks

    assert cf.ARM_HOOK_TYPES is arm_hooks.HOOK_TYPES
    for stage in arm_hooks.HOOK_TYPES:
        assert f"-t {stage}" in cf._SESSIONSTART_ARM_CMD


def test_verify_fails_a_one_stage_armed_consumer(tmp_path):
    """FROZEN: `carrier_floor.verify` FAILs a 1-stage-armed consumer, naming the stages that
    would land wired-but-dormant. Before #290 this passed — verify checked only the verify
    leg — so a pre-#275b consumer verified green with commit-msg / pre-push dormant."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    assert car.verify(_FLOOR_TARGET).ok is True  # baseline: fully armed
    _rewrite_arm_leg(tmp_path, _ONE_STAGE_ARM)

    result = car.verify(_FLOOR_TARGET)
    assert result.ok is False
    dormant = next(f for f in result.failures if "arm leg arms" in f)
    # names the ACTUALLY dormant stages — a bare `install` does arm pre-commit by default
    assert "commit-msg" in dormant and "pre-push" in dormant
    assert "1/3" in dormant


def test_detect_classifies_a_one_stage_armed_consumer_drifted(tmp_path):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _rewrite_arm_leg(tmp_path, _ONE_STAGE_ARM)
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED


def test_redeploy_self_heals_a_one_stage_arm_to_full_cardinality(tmp_path):
    """FROZEN: a re-deploy against that same fixture leaves it 3-stage-armed and verify-green
    (#290 (b)) — the half that makes the (a) DRIFTED verdict repairable."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _rewrite_arm_leg(tmp_path, _ONE_STAGE_ARM)

    healed = car.apply(_FLOOR_TARGET)
    assert healed.changed is True
    assert any("self-healed" in c for c in healed.changes)

    arm = _arm_commands(tmp_path)
    assert len(arm) == 1  # repaired IN PLACE — not a second arm leg appended
    for stage in cf.ARM_HOOK_TYPES:
        assert f"-t {stage}" in arm[0]
    assert car.verify(_FLOOR_TARGET).ok is True
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT


def test_redeploy_on_an_already_armed_consumer_changes_nothing(tmp_path):
    """FROZEN: an already-3-stage fixture is UNCHANGED by re-deploy (idempotence) — the
    self-heal must not rewrite a consumer that was already correct."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    before = _settings(tmp_path).read_bytes()

    second = car.apply(_FLOOR_TARGET)
    assert second.changed is False
    assert _settings(tmp_path).read_bytes() == before  # byte-identical


def test_self_heal_touches_only_the_arm_leg(tmp_path):
    """The repair is scoped: unrelated settings.json keys, the verify leg, sibling
    SessionStart hooks and the arm hook's own non-command keys all survive verbatim."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    data = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    data["enabledPlugins"] = {"tier1-lifecycle@dev-knowledge-methodology": True}
    data["permissions"] = {"allow": ["Bash(git status)"]}
    group = data["hooks"]["SessionStart"][0]
    group["hooks"].append({"type": "command", "command": "python custom_surfacing.py",
                           "timeout": 5})
    for hook in group["hooks"]:
        if "pre_commit install" in hook["command"]:
            hook["command"] = _ONE_STAGE_ARM
            hook["timeout"] = 45  # a consumer-tuned timeout the repair must preserve
    _settings(tmp_path).write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    car.apply(_FLOOR_TARGET)
    healed = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))

    assert healed["enabledPlugins"] == data["enabledPlugins"]
    assert healed["permissions"] == data["permissions"]
    cmds = [h["command"] for g in healed["hooks"]["SessionStart"] for h in g["hooks"]]
    assert "python custom_surfacing.py" in cmds          # sibling hook untouched
    assert any("check_floor_hash.py --require-present" in c for c in cmds)  # verify leg kept
    assert len(healed["hooks"]["SessionStart"]) == 1      # no duplicate guard block
    arm = next(
        h for g in healed["hooks"]["SessionStart"] for h in g["hooks"]
        if "pre_commit install" in h["command"]
    )
    assert arm["timeout"] == 45  # only `command` was rewritten
    assert car.verify(_FLOOR_TARGET).ok is True


@pytest.mark.parametrize("long_form", [
    "python -m pre_commit install --hook-type pre-commit --hook-type commit-msg "
    "--hook-type pre-push",
    "python -m pre_commit install --hook-type=pre-commit --hook-type=commit-msg "
    "--hook-type=pre-push",
])
def test_long_form_stage_flags_count_as_fully_armed(tmp_path, long_form):
    """A consumer armed with `pre-commit install`'s long-form flag is NOT stale — a false
    DRIFTED here would have the self-heal rewrite a config that was already correct."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _rewrite_arm_leg(tmp_path, long_form)

    assert car.verify(_FLOOR_TARGET).ok is True
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.apply(_FLOOR_TARGET).changed is False       # no gratuitous rewrite
    assert _arm_commands(tmp_path) == [long_form]          # left verbatim


@pytest.mark.parametrize("cmd,expected", [
    # stage flags belonging to a DIFFERENT pre-commit subcommand must not be credited to
    # `install` — `install-hooks` is a distinct subcommand that arms no git hook stage
    ("python -m pre_commit install-hooks -t pre-commit -t commit-msg -t pre-push", set()),
    # ...nor may flags from a neighbouring shell segment
    ("python -m pre_commit run -t pre-commit -t commit-msg -t pre-push; "
     "python -m pre_commit install", {"pre-commit"}),
    ("python -m pre_commit run -t commit-msg && python -m pre_commit install -t pre-push",
     {"pre-push"}),
    # a mere MENTION of the arm command is not an arm command
    ('echo "pre_commit install -t pre-commit -t commit-msg -t pre-push"', set()),
    # a flag with NO VALUE is an argparse error, so the install arms nothing — it does NOT
    # fall back to the default stage (my own wrong assumption, caught by terra pass 4)
    ("python -m pre_commit install -t", set()),
    ("python -m pre_commit install --hook-type", set()),
    # a command performing no install contributes NOTHING — the default-stage fallback is a
    # property of an invocation, not of an unrelated SessionStart hook
    ("python scripts/surface_triage.py", set()),
    ("python .claude/check_floor_hash.py --require-present", set()),
    # real invocations, in each spelling pre-commit accepts
    ("python -m pre_commit install -t pre-commit -t commit-msg -t pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    ("pre-commit install --hook-type=pre-commit --hook-type=commit-msg "
     "--hook-type=pre-push", {"pre-commit", "commit-msg", "pre-push"}),
    ("/usr/local/bin/pre-commit install -tpre-commit -tcommit-msg -tpre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    (r"C:\venv\Scripts\pre-commit.exe install -t pre-commit -t commit-msg -t pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    # a bare install arms pre-commit only — the #275 defect, stated honestly
    ("python -m pre_commit install", {"pre-commit"}),
    # --- terra pass 2: pre-commit must be the command INVOKED, not a token that appears ---
    # unquoted mention in argument position (the quoted `echo` case above missed this)
    ("echo pre-commit install -t pre-commit -t commit-msg -t pre-push", set()),
    ("git commit -m 'run pre-commit install -t pre-push'", set()),
    # a NEWLINE is a command boundary — a flag on a later line is not this install's
    ("python -m pre_commit install\necho -t commit-msg -t pre-push", {"pre-commit"}),
    ("echo arming\npython -m pre_commit install -t pre-commit -t commit-msg -t pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    # quoting is RESOLVED — a quoted stage name is the stage it names. Reading these as
    # under-armed is the damaging direction: apply would rewrite a CORRECT consumer.
    ("PRE_COMMIT_HOME=/tmp pre-commit install -t 'pre-commit' -t 'commit-msg' "
     "-t 'pre-push'", {"pre-commit", "commit-msg", "pre-push"}),
    ('pre-commit install -t "pre-commit" -t "commit-msg" -t "pre-push"',
     {"pre-commit", "commit-msg", "pre-push"}),
    # a bounded runner prefix is tolerated — this repo's own hooks invoke via `uv run`
    ("uv run pre-commit install -t pre-commit -t commit-msg -t pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    ("py -3 -m pre_commit install -t pre-commit -t commit-msg -t pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    # past `--` a `-t` is a positional, not a stage flag
    ("python -m pre_commit install -- -t pre-commit -t commit-msg -t pre-push",
     {"pre-commit"}),
    # an opaque wrapper is not statically readable -> reads as no invocation (stated limit)
    ("sh -c 'pre-commit install -t pre-commit -t commit-msg -t pre-push'", set()),
    # unbalanced quotes must not raise — the whitespace-split fallback still reads the flags
    ("pre-commit install -t 'pre-commit -t commit-msg", {"pre-commit", "commit-msg"}),
    # --- terra pass 3: the runner prefix is a SEQUENCE, not a bag of allowed words ---
    # an INCOMPLETE runner prefix never reaches the pre-commit CLI, so it arms nothing
    ("python pre-commit install -t pre-commit -t commit-msg -t pre-push", set()),
    ("uv pre-commit install -t pre-commit -t commit-msg -t pre-push", set()),
    ("poetry pre-commit install -t pre-commit -t commit-msg -t pre-push", set()),
    ("run pre-commit install -t pre-commit -t commit-msg -t pre-push", set()),
    ("exec pre-commit install -t pre-commit -t commit-msg -t pre-push", set()),
    # ...while each COMPLETE prefix does
    ("uvx pre-commit install -t pre-commit -t commit-msg -t pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    ("poetry run pre-commit install -t pre-commit -t commit-msg -t pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    ("py -3.12 -m pre_commit install -t pre-commit -t commit-msg -t pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    # `-t=X` — argparse splits an `=`-bearing short option and takes the remainder as the
    # value, so this IS a valid full arm; reading it as under-armed would rewrite a correct
    # consumer (the damaging direction)
    ("pre-commit install -t=pre-commit -t=commit-msg -t=pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    # a POSIX line continuation is ONE command, not two under-armed segments
    ("pre-commit install -t pre-commit \\\n  -t commit-msg -t pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    # Windows executable names are case-insensitive
    (r"C:\venv\Scripts\PRE-COMMIT.EXE install -t pre-commit -t commit-msg -t pre-push",
     {"pre-commit", "commit-msg", "pre-push"}),
    # degenerate inputs must not raise
    ("", set()),
    ("   ", set()),
    ("\n\n", set()),
    # --- terra pass 4: an invocation that FAILS argument parsing arms nothing ---
    # `-t` is choices-constrained, so one invalid value aborts the whole install BEFORE
    # anything is written. Discarding it and crediting the three valid ones is FALSE-ARMED.
    ("pre-commit install -t pre-commit -t commit-msg -t pre-push -t bogus", set()),
    ("pre-commit install -t=bogus", set()),
    ("pre-commit install --hook-type=not-a-hook -t pre-commit", set()),
    # argparse splits a short option on the FIRST `=` only, so `-t==X` passes it `=X` and the
    # invocation is rejected — exactly one optional `=` is valid, not any number of them
    ("pre-commit install -t=pre-commit -t==commit-msg -t=pre-push", set()),
    ("pre-commit install -t===pre-commit", set()),
    # ...but a VALID stage this carrier does not manage is not an error: the install succeeds
    # and all three managed stages really are armed
    ("pre-commit install -t pre-commit -t commit-msg -t pre-push -t post-commit",
     {"pre-commit", "commit-msg", "pre-push"}),
    ("pre-commit install -t post-checkout", set()),  # valid, but manages none of ours
])


def test_armed_stages_binds_flags_to_the_install_invocation(cmd, expected):
    """The stage parser must credit a flag only to the `pre-commit install` that consumes it.

    A whole-token scan (the pre-terra-review draft) read `install-hooks -t ...` and
    `run -t ...; install` as fully armed — a false PRESENT_CORRECT, i.e. the very
    dormant-stage defect #290 exists to catch, reintroduced by the teeth themselves."""
    assert cf._armed_stages(cmd) == frozenset(expected)


def test_valid_hook_types_come_from_pre_commit_itself():
    """The valid-stage enum is pre-commit's own (library-first), and the fallback literal is
    only a mirror — so `post-commit` cannot drift into looking invalid."""
    from pre_commit.clientlib import HOOK_TYPES as upstream

    assert cf._VALID_HOOK_TYPES == frozenset(upstream)
    # every stage this carrier requires must be one pre-commit can actually install
    assert set(cf.ARM_HOOK_TYPES) <= cf._VALID_HOOK_TYPES


@pytest.mark.parametrize("cmd", [
    "python -m pre_commit install-hooks -t pre-commit",
    'echo "pre_commit install"',
    "echo pre-commit install",
    "sh -c 'pre-commit install'",
    "python scripts/surface_triage.py",
])
def test_non_arming_commands_are_not_arm_legs(cmd):
    assert cf._is_arm_command(cmd) is False


@pytest.mark.parametrize("armed_cmd", [
    "PRE_COMMIT_HOME=/tmp pre-commit install -t 'pre-commit' -t 'commit-msg' -t 'pre-push'",
    "uv run pre-commit install -t pre-commit -t commit-msg -t pre-push",
    "pre-commit install --hook-type=pre-commit --hook-type=commit-msg --hook-type=pre-push",
    "pre-commit install -t=pre-commit -t=commit-msg -t=pre-push",
    r"C:\venv\Scripts\PRE-COMMIT.EXE install -t pre-commit -t commit-msg -t pre-push",
    "pre-commit install -t pre-commit \\\n  -t commit-msg -t pre-push",
])
def test_apply_never_rewrites_an_already_armed_variant(tmp_path, armed_cmd):
    """The damaging direction: a FALSE under-armed read would have apply rewrite a correct
    consumer's command, discarding its env prefix / runner / quoting. These must be no-ops."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _rewrite_arm_leg(tmp_path, armed_cmd)

    assert car.verify(_FLOOR_TARGET).ok is True
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.apply(_FLOOR_TARGET).changed is False
    assert _arm_commands(tmp_path) == [armed_cmd]  # byte-identical, untouched


def test_an_opaque_wrapper_gains_a_leg_and_is_never_rewritten(tmp_path):
    """A `sh -c '...'` arm leg cannot be read statically, so it reads as absent. apply must
    ADD a canonical leg beside it and leave the wrapper verbatim — repairing without
    destroying behaviour it cannot understand (the stated parser limit)."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    opaque = "sh -c 'pre-commit install -t pre-commit -t commit-msg -t pre-push'"
    _rewrite_arm_leg(tmp_path, opaque)

    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED
    car.apply(_FLOOR_TARGET)
    cmds = [
        h["command"]
        for g in json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
                      ["hooks"]["SessionStart"]
        for h in g["hooks"]
    ]
    assert opaque in cmds                                  # wrapper preserved verbatim
    assert cf._SESSIONSTART_ARM_CMD in cmds                # canonical leg added beside it
    assert car.verify(_FLOOR_TARGET).ok is True
    assert car.apply(_FLOOR_TARGET).changed is False        # and settles (no oscillation)


def test_a_fooled_parser_would_false_green_a_dormant_consumer(tmp_path):
    """End-to-end teeth on the terra HIGH: a consumer whose arm leg is `install-hooks` with
    all three stage flags arms NO git hook stage, so it must be DRIFTED and repaired — not
    read as correct because the flags happen to be present in the string."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _rewrite_arm_leg(
        tmp_path, "python -m pre_commit install-hooks -t pre-commit -t commit-msg -t pre-push"
    )

    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED
    failures = car.verify(_FLOOR_TARGET).failures
    assert any("missing SessionStart arm hook" in f for f in failures)

    car.apply(_FLOOR_TARGET)
    assert car.verify(_FLOOR_TARGET).ok is True
    assert car.apply(_FLOOR_TARGET).changed is False


def test_arm_leg_split_across_two_commands_is_fully_armed(tmp_path):
    """Coverage is a union: arming split across two commands satisfies the requirement, so
    the self-heal does not 'repair' a complete-but-split arm into a redundant third."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    data = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    group = data["hooks"]["SessionStart"][0]
    for hook in group["hooks"]:
        if "pre_commit install" in hook["command"]:
            hook["command"] = "python -m pre_commit install -t pre-commit"
    group["hooks"].append({"type": "command", "timeout": 30,
                           "command": "python -m pre_commit install -t commit-msg -t pre-push"})
    _settings(tmp_path).write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    assert car.verify(_FLOOR_TARGET).ok is True
    assert car.apply(_FLOOR_TARGET).changed is False
    assert len(_arm_commands(tmp_path)) == 2  # neither leg rewritten


def test_missing_arm_leg_entirely_is_drifted_then_repaired_without_duplicating(tmp_path):
    """The teeth now FAIL a settings.json carrying the verify leg but NO arm leg, so apply
    must repair that too — a verdict apply could not fix is the shape #290 exists to avoid.
    The missing leg joins the existing group rather than appending a second guard block."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    data = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    group = data["hooks"]["SessionStart"][0]
    group["hooks"] = [h for h in group["hooks"] if "pre_commit install" not in h["command"]]
    _settings(tmp_path).write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED
    failures = car.verify(_FLOOR_TARGET).failures
    assert any("missing SessionStart arm hook" in f for f in failures)

    car.apply(_FLOOR_TARGET)
    healed = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    assert len(healed["hooks"]["SessionStart"]) == 1  # joined the existing group
    assert car.verify(_FLOOR_TARGET).ok is True
    assert car.apply(_FLOOR_TARGET).changed is False  # and settles


def test_missing_verify_leg_is_repaired_without_duplicating_the_arm(tmp_path):
    """The mirror gap: arm leg present, verify leg gone. Previously the sentinel miss made
    apply append a whole second guard block (a redundant arm leg); now only the verify leg
    is added back."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    data = json.loads(_settings(tmp_path).read_text(encoding="utf-8"))
    group = data["hooks"]["SessionStart"][0]
    group["hooks"] = [h for h in group["hooks"] if "check_floor_hash.py" not in h["command"]]
    _settings(tmp_path).write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED
    car.apply(_FLOOR_TARGET)
    assert len(_arm_commands(tmp_path)) == 1  # arm leg NOT duplicated
    assert car.verify(_FLOOR_TARGET).ok is True


def test_verify_teeth_do_not_route_through_detect_classifier(tmp_path, monkeypatch):
    """D9 holds across the new arm-leg judgment: verify's FAIL on a 1-stage arm is its own,
    not a call into detect's classifier."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _rewrite_arm_leg(tmp_path, _ONE_STAGE_ARM)

    def _boom(*_a, **_k):
        raise AssertionError("verify must not call detect's _classify_floor (D9)")

    monkeypatch.setattr(cf, "_classify_floor", _boom)
    assert car.verify(_FLOOR_TARGET).ok is False


def test_detect_teeth_do_not_route_through_verify_judge(tmp_path, monkeypatch):
    """D9's mirror on the same new judgment."""
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    _rewrite_arm_leg(tmp_path, _ONE_STAGE_ARM)

    def _boom(*_a, **_k):
        raise AssertionError("detect must not call verify's _verify_floor (D9)")

    monkeypatch.setattr(cf, "_verify_floor", _boom)
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED


@pytest.mark.parametrize("break_it", [
    lambda repo: _claude_md(repo).write_text("# no include\n", encoding="utf-8", newline="\n"),
    lambda repo: _hook_script(repo).write_text("print('tampered')\n", encoding="utf-8", newline="\n"),
    lambda repo: _gitignore(repo).write_text(".claude/\n", encoding="utf-8", newline="\n"),
    lambda repo: _settings(repo).write_text("{}", encoding="utf-8", newline="\n"),
    lambda repo: _rewrite_arm_leg(repo, _ONE_STAGE_ARM),  # #290: a stale 1-stage arm leg
])
def test_missing_arming_artifact_detects_drifted_then_reconciles(tmp_path, break_it):
    car = _carrier(tmp_path)
    car.apply(_FLOOR_TARGET)
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    break_it(tmp_path)  # floor+sidecar intact, but one arming artifact broken
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_DRIFTED
    assert car.verify(_FLOOR_TARGET).ok is False

    car.apply(_FLOOR_TARGET)
    assert car.detect(_FLOOR_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_FLOOR_TARGET).ok is True
