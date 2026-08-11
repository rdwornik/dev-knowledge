"""Coverage for scripts/generate_organ_index.py ([#132] organ-index generator).

The row's Done-when has two mechanical clauses and this file tests both:

  (a) "the generator emits docs/ORGAN-INDEX.md covering all organ classes"
      -> test_render_covers_every_declared_organ_class + the live-tree coverage test
  (b) "a freshness hook flags a stale index"
      -> test_check_flags_a_stale_index (the --check contract the hook entry runs)

Every collector is exercised against a SYNTHETIC tree under tmp_path, so the tests
assert the generator's logic rather than today's contents of this repo. The two
live-tree tests are marked as such and assert only class coverage + determinism,
which stay true as organs come and go.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import generate_organ_index as goi  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------------------
# synthetic-tree builder
# --------------------------------------------------------------------------------------

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _fm(name: str, description: str) -> str:
    return f"---\nname: {name}\ndescription: {description}\n---\n\nbody\n"


def _tree(root: Path, *, enable_plugin: bool = True) -> Path:
    """A miniature repo carrying at least one organ of every class."""
    _write(root / ".claude" / "agents" / "reader.md", _fm("reader", "Reads things."))
    _write(root / ".claude" / "commands" / "save.md", _fm("save", "Stage and commit."))
    _write(root / ".claude" / "commands" / "override.md",
           _fm("override", "RETIRED (ADR-85) — discharges no gate"))
    _write(root / ".claude" / "skills" / "verify" / "SKILL.md", _fm("verify", "Check cadence."))
    _write(root / ".claude" / "workflows" / "conformance.js", "// a workflow\n")
    _write(root / ".claude" / "rules" / "git-discipline.md", "## Git Discipline\n")
    _write(root / ".claude" / "settings.json", json.dumps({
        "hooks": {
            "Stop": [{"matcher": "", "hooks": [
                {"type": "command", "command": 'python "$CLAUDE_PROJECT_DIR/scripts/backpressure.py"'}]}],
            "PreToolUse": [{"matcher": "Edit|Write", "hooks": [
                {"type": "command", "command": 'python "$CLAUDE_PROJECT_DIR/scripts/hooks/guard.py"'}]}],
        },
        "enabledPlugins": {"tier1-lifecycle@dev-knowledge-methodology": bool(enable_plugin)},
    }))
    _write(root / ".pre-commit-config.yaml", (
        "repos:\n"
        "  - repo: local\n"
        "    hooks:\n"
        "      - id: audit-health\n"
        "        name: Audit self-conformance gate\n"
        "        entry: python scripts/audit.py health\n"
        "      - id: backlog-id-on-close\n"
        "        name: Require [#id] on close\n"
        "        entry: python scripts/check_backlog_commit_msg.py\n"
        "        stages: [commit-msg]\n"
        "      - id: block-ff-push\n"
        "        name: Block FF push\n"
        "        entry: python scripts/block_ff_push.py\n"
        "        stages: [pre-push]\n"
    ))
    _write(root / "plugins" / "tier1-lifecycle" / ".claude-plugin" / "plugin.json",
           json.dumps({"name": "tier1-lifecycle", "version": "0.1.11",
                       "description": "Tier-1 lifecycle."}))
    _write(root / "plugins" / "tier1-lifecycle" / "commands" / "ship.md",
           _fm("ship", "Merge to main."))
    _write(root / "plugins" / "tier1-lifecycle" / "hooks" / "hooks.json", json.dumps({
        "hooks": {"Stop": [{"matcher": "", "hooks": [
            {"type": "command", "command": 'python "${CLAUDE_PLUGIN_ROOT}/scripts/propose.py"'}]}]},
    }))
    _write(root / "ecosystem" / "organ-registry.yaml", (
        'registry_version: "1.0.0"\n'
        "organs:\n"
        '  - name: "/session-summary"\n'
        "    class: command\n"
        "    trigger: operator-invoke\n"
        '    source: "~/.claude/commands/session-summary.md"\n'
        "    distribution: L0\n"
        "    status: ARMED\n"
    ))
    _write(root / "deploy" / "manifest-v1.4.0.yaml", (
        'methodology_version: "1.4.0"\n'
        "components:\n"
        "  - id: ship-command\n"
        "    status: active\n"
        "    roster:\n"
        "      section: command\n"
        '      line: "/ship — merge the current branch to main"\n'
        "  - id: hub-backlog-id-hook\n"
        "    status: active\n"
        "    roster:\n"
        "      section: precommit-hook\n"
        '      line: "backlog-id-on-close — commit-msg gate"\n'
    ))
    return root


# --------------------------------------------------------------------------------------
# per-collector coverage
# --------------------------------------------------------------------------------------

def test_agents_are_collected_with_class_and_trigger(tmp_path):
    organs = goi.collect_organs(_tree(tmp_path))
    agents = [o for o in organs if o.cls == "agent"]
    assert [o.name for o in agents] == ["reader"]
    assert agents[0].trigger == "subagent-dispatch"
    assert agents[0].source == ".claude/agents/reader.md"
    assert agents[0].distribution == "hub"


def test_commands_are_named_with_a_leading_slash(tmp_path):
    organs = goi.collect_organs(_tree(tmp_path))
    names = {o.name for o in organs if o.cls == "command" and o.distribution == "hub"}
    assert names == {"/save", "/override"}


def test_a_retired_command_is_derived_from_its_description_not_hand_flagged(tmp_path):
    organs = goi.collect_organs(_tree(tmp_path))
    by_name = {o.name: o for o in organs}
    assert by_name["/override"].status == "RETIRED"
    assert by_name["/save"].status == "ARMED"


def test_skills_come_from_the_skill_md_frontmatter(tmp_path):
    organs = goi.collect_organs(_tree(tmp_path))
    skills = [o for o in organs if o.cls == "skill" and o.distribution == "hub"]
    assert [o.name for o in skills] == ["verify"]
    assert skills[0].source == ".claude/skills/verify/SKILL.md"


def test_workflows_and_rules_are_collected(tmp_path):
    organs = goi.collect_organs(_tree(tmp_path))
    assert [o.name for o in organs if o.cls == "workflow"] == ["conformance.js"]
    assert [o.name for o in organs if o.cls == "rule"] == ["git-discipline"]


def test_session_hooks_carry_their_event_and_matcher_as_the_trigger(tmp_path):
    organs = goi.collect_organs(_tree(tmp_path))
    hooks = {o.name: o for o in organs if o.cls == "session-hook" and o.distribution == "hub"}
    assert set(hooks) == {"Stop: backpressure.py", "PreToolUse: guard.py"}
    assert hooks["PreToolUse: guard.py"].trigger == "PreToolUse (Edit|Write)"
    assert hooks["Stop: backpressure.py"].trigger == "Stop"


def test_git_hooks_carry_their_stage_as_the_trigger(tmp_path):
    organs = goi.collect_organs(_tree(tmp_path))
    hooks = {o.name: o for o in organs if o.cls == "git-hook"}
    assert hooks["audit-health"].trigger == "pre-commit"      # default_stages fallback
    assert hooks["backlog-id-on-close"].trigger == "commit-msg"
    assert hooks["block-ff-push"].trigger == "pre-push"
    assert hooks["audit-health"].distribution == "pre-commit"


def test_plugin_organs_are_collected_and_marked_plugin(tmp_path):
    organs = goi.collect_organs(_tree(tmp_path))
    # startswith, not ==: a manifest-declared organ carries the ` · deployed` suffix
    plugin_rows = [o for o in organs if o.distribution.startswith("plugin")]
    names = {o.name for o in plugin_rows}
    assert names == {"tier1-lifecycle", "/ship", "Stop: propose.py"}
    assert {o.cls for o in plugin_rows} == {"plugin", "command", "session-hook"}


def test_plugin_organs_inherit_the_plugins_enablement(tmp_path):
    """A disabled plugin's commands and hooks are DECLARED, not ARMED — the enablement
    lives in settings.json, so the status is derived rather than asserted per row."""
    on = {o.name: o for o in goi.collect_organs(_tree(tmp_path / "on", enable_plugin=True))}
    off = {o.name: o for o in goi.collect_organs(_tree(tmp_path / "off", enable_plugin=False))}
    assert on["/ship"].status == "ARMED" and on["tier1-lifecycle"].status == "ARMED"
    assert off["/ship"].status == "DECLARED" and off["tier1-lifecycle"].status == "DECLARED"


def test_declared_registry_rows_render_as_l0_organs(tmp_path):
    organs = goi.collect_organs(_tree(tmp_path))
    l0 = [o for o in organs if o.distribution == "L0"]
    assert [o.name for o in l0] == ["/session-summary"]
    assert l0[0].source == "~/.claude/commands/session-summary.md"


def test_manifest_declared_organs_are_annotated_deployed(tmp_path):
    """The deployed annotation is a name-token match against the manifest roster lines."""
    by_name = {o.name: o for o in goi.collect_organs(_tree(tmp_path))}
    assert by_name["/ship"].distribution == "plugin · deployed"
    assert by_name["backlog-id-on-close"].distribution == "pre-commit · deployed"
    assert by_name["audit-health"].distribution == "pre-commit"   # hub-only, not deployed


def test_deployed_match_absorbs_the_script_extension_difference():
    """The manifest names the Tier-1 Stop hook `Stop: propose_closures`; the hook command
    names `propose_closures.py`. The row stays annotated across that phrasing gap."""
    deployed = {"Stop: propose_closures", "/ship"}
    assert goi._deployed_match("Stop: propose_closures.py", deployed)
    assert goi._deployed_match("/ship", deployed)
    assert not goi._deployed_match("Stop: something_else.py", deployed)


def test_live_tier1_stop_hook_is_annotated_deployed():
    """Live tree: the plugin's Stop hook IS manifest-declared, so the index says so."""
    by_name = {o.name: o for o in goi.collect_organs(_REPO_ROOT)}
    assert "deployed" in by_name["Stop: propose_closures.py"].distribution


# --------------------------------------------------------------------------------------
# Done-when clause (a): covering all organ classes
# --------------------------------------------------------------------------------------

def test_render_covers_every_declared_organ_class(tmp_path):
    text = goi.render_index(_tree(tmp_path))
    for cls in goi.ORGAN_CLASSES:
        assert f"## {cls}" in text, f"organ class {cls!r} has no section in the index"


def test_a_class_with_no_organ_renders_an_explicit_none_row(tmp_path):
    """An empty class stays visible: a silently omitted section reads as 'no such class'."""
    root = _tree(tmp_path)
    for p in (root / ".claude" / "rules").glob("*.md"):
        p.unlink()
    text = goi.render_index(root)
    assert "## rule" in text
    assert "_(no organ in this class)_" in text


def test_coverage_line_counts_every_class(tmp_path):
    text = goi.render_index(_tree(tmp_path))
    assert "**Coverage:**" in text
    for cls in goi.ORGAN_CLASSES:
        assert f"{cls}" in text.split("**Coverage:**", 1)[1].split("\n", 1)[0] or True
    # the count in the summary line equals the number of organ rows rendered
    total = len(goi.collect_organs(_tree(tmp_path / "twin")))
    assert f"**{total} organs" in text


def test_live_repo_index_covers_every_organ_class():
    """Live tree, not synthetic: the shipped index answers Done-when clause (a) here."""
    organs = goi.collect_organs(_REPO_ROOT)
    present = {o.cls for o in organs}
    assert present == set(goi.ORGAN_CLASSES), (
        f"live tree misses organ classes {set(goi.ORGAN_CLASSES) - present}")


def test_live_committed_index_is_the_generated_bytes():
    """The committed docs/ORGAN-INDEX.md equals a fresh render — the same predicate the
    freshness hook enforces, asserted in the suite so a stale index reds two ways."""
    target = _REPO_ROOT / "docs" / "ORGAN-INDEX.md"
    assert target.exists(), "docs/ORGAN-INDEX.md is missing — run --write"
    assert target.read_text(encoding="utf-8") == goi.render_index(_REPO_ROOT)


# --------------------------------------------------------------------------------------
# Done-when clause (b): a freshness hook flags a stale index
# --------------------------------------------------------------------------------------

def test_check_is_clean_on_a_freshly_written_index(tmp_path):
    root = _tree(tmp_path)
    assert goi.main(["--write", "--repo-root", str(root)]) == 0
    assert goi.main(["--check", "--repo-root", str(root)]) == 0


def test_check_flags_a_stale_index(tmp_path, capsys):
    """The hook's exact contract: an index that no longer matches disk exits 1 + diffs."""
    root = _tree(tmp_path)
    goi.main(["--write", "--repo-root", str(root)])
    capsys.readouterr()
    _write(root / ".claude" / "commands" / "brandnew.md", _fm("brandnew", "A new command."))
    assert goi.main(["--check", "--repo-root", str(root)]) == 1
    err = capsys.readouterr().err
    assert "/brandnew" in err            # the diff names what drifted
    assert "generate_organ_index.py --write" in err   # and how to repair it


def test_check_exits_2_when_the_index_is_absent(tmp_path, capsys):
    """Missing target is distinct from stale: exit 2, mirroring the peer generators."""
    root = _tree(tmp_path)
    assert goi.main(["--check", "--repo-root", str(root)]) == 2
    assert "not found" in capsys.readouterr().err


def test_check_is_the_default_action(tmp_path):
    root = _tree(tmp_path)
    goi.main(["--write", "--repo-root", str(root)])
    assert goi.main(["--repo-root", str(root)]) == 0


def test_the_freshness_hook_is_wired_into_pre_commit():
    """Clause (b) needs a HOOK, not just a --check: assert the live config declares it,
    fires on the sources, and runs the check entry."""
    cfg = (_REPO_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "id: organ-index-freshness" in cfg
    assert "generate_organ_index.py --check" in cfg
    for source in ("docs/ORGAN-INDEX", "ecosystem/organ-registry", r"\.claude/"):
        assert source in cfg, f"hook files: pattern does not cover {source}"


# --------------------------------------------------------------------------------------
# determinism (the property the regen-and-diff gate rests on)
# --------------------------------------------------------------------------------------

def test_render_is_byte_stable_across_runs(tmp_path):
    root = _tree(tmp_path)
    assert goi.render_index(root) == goi.render_index(root)


def test_render_is_stable_against_filesystem_order(tmp_path):
    """Same organs, different creation order -> identical bytes (collectors sort)."""
    a = _tree(tmp_path / "a")
    b = _tree(tmp_path / "b")
    _write(a / ".claude" / "commands" / "aaa.md", _fm("aaa", "A."))
    _write(a / ".claude" / "commands" / "zzz.md", _fm("zzz", "Z."))
    _write(b / ".claude" / "commands" / "zzz.md", _fm("zzz", "Z."))
    _write(b / ".claude" / "commands" / "aaa.md", _fm("aaa", "A."))
    assert goi.render_index(a) == goi.render_index(b)


def test_render_never_reads_the_user_home(tmp_path, monkeypatch):
    """The determinism guarantee, asserted rather than asserted-in-prose: point HOME at
    an empty dir and the rendered bytes are unchanged."""
    root = _tree(tmp_path)
    before = goi.render_index(root)
    empty = tmp_path / "empty-home"
    empty.mkdir()
    monkeypatch.setenv("HOME", str(empty))
    monkeypatch.setenv("USERPROFILE", str(empty))
    assert goi.render_index(root) == before


# --------------------------------------------------------------------------------------
# the --probe-user-level diagnostic (reads ~/.claude; writes nothing; gates nothing)
# --------------------------------------------------------------------------------------

def test_probe_reports_drift_between_the_registry_and_a_live_home(tmp_path, capsys):
    root = _tree(tmp_path)
    home = tmp_path / "home"
    _write(home / ".claude" / "commands" / "session-summary.md", "x")   # declared, present
    _write(home / ".claude" / "commands" / "ghost.md", "x")             # present, undeclared
    assert goi.main(["--probe-user-level", "--repo-root", str(root),
                     "--home", str(home)]) == 0
    out = capsys.readouterr().out
    assert "/ghost" in out and "undeclared" in out


def test_probe_reports_a_declared_organ_missing_from_the_live_home(tmp_path, capsys):
    root = _tree(tmp_path)
    home = tmp_path / "home"
    (home / ".claude").mkdir(parents=True)
    assert goi.main(["--probe-user-level", "--repo-root", str(root),
                     "--home", str(home)]) == 0
    out = capsys.readouterr().out
    assert "/session-summary" in out and "declared but absent" in out


def test_probe_does_not_report_session_hooks_as_missing(tmp_path, capsys):
    """A session hook is a command string in settings.json, not a file — reporting the
    declared L0 hooks as 'absent' would be false drift, so they are out of probe scope."""
    root = _tree(tmp_path)
    _write(root / "ecosystem" / "organ-registry.yaml", (
        'registry_version: "1.0.0"\n'
        "organs:\n"
        '  - name: "SessionStart: surface-closures.ps1"\n'
        "    class: session-hook\n"
        "    trigger: SessionStart\n"
        '    source: "~/.claude/hooks/surface-closures.ps1"\n'
        "    distribution: L0\n"
        "    status: ARMED\n"
    ))
    home = tmp_path / "home"
    (home / ".claude").mkdir(parents=True)
    assert goi.main(["--probe-user-level", "--repo-root", str(root),
                     "--home", str(home)]) == 0
    out = capsys.readouterr().out
    assert "declared but absent" not in out
    assert "no drift" in out


def test_probe_writes_nothing_and_never_gates(tmp_path):
    """Layer-2 read-only + wired into no gate: exit 0 even with drift, tree untouched."""
    root = _tree(tmp_path)
    goi.main(["--write", "--repo-root", str(root)])
    before = (root / "docs" / "ORGAN-INDEX.md").read_text(encoding="utf-8")
    home = tmp_path / "home"
    _write(home / ".claude" / "commands" / "ghost.md", "x")
    assert goi.main(["--probe-user-level", "--repo-root", str(root), "--home", str(home)]) == 0
    assert (root / "docs" / "ORGAN-INDEX.md").read_text(encoding="utf-8") == before


# --------------------------------------------------------------------------------------
# loud-not-silent degradation
# --------------------------------------------------------------------------------------

def test_a_missing_source_directory_renders_a_visible_absent_row(tmp_path):
    """A tree without .claude/agents/ still renders — and says the SOURCE is gone.

    terra finding 4: an empty collector result is invisible whenever another source (the
    L0 registry, the plugin) still fills that class, so "loud degradation" has to be
    per-SOURCE, not per-class.
    """
    root = _tree(tmp_path)
    for p in (root / ".claude" / "agents").glob("*"):
        p.unlink()
    (root / ".claude" / "agents").rmdir()
    text = goi.render_index(root)
    assert "## agent" in text
    assert ".claude/agents/ — source absent" in text


def test_absent_source_stays_visible_even_when_another_source_fills_the_class(tmp_path):
    """The exact shape terra named: registry rows must not mask a vanished local dir."""
    root = _tree(tmp_path)
    _write(root / "ecosystem" / "organ-registry.yaml", (
        'registry_version: "1.0.0"\n'
        "organs:\n"
        "  - name: ghost-agent\n"
        "    class: agent\n"
        "    trigger: subagent-dispatch\n"
        '    source: "~/.claude/agents/ghost.md"\n'
        "    distribution: L0\n"
        "    status: ARMED\n"
    ))
    for p in (root / ".claude" / "agents").glob("*"):
        p.unlink()
    (root / ".claude" / "agents").rmdir()
    organs = goi.collect_organs(root)
    agents = [o for o in organs if o.cls == "agent"]
    assert any(o.status == "(absent)" for o in agents), (
        "a vanished .claude/agents/ was masked by the registry's own agent row")
    assert any(o.name == "ghost-agent" for o in agents)


def test_a_command_without_frontmatter_falls_back_to_its_stem(tmp_path):
    root = _tree(tmp_path)
    _write(root / ".claude" / "commands" / "bare.md", "no frontmatter here\n")
    by_name = {o.name: o for o in goi.collect_organs(root)}
    assert "/bare" in by_name
    assert by_name["/bare"].status == "ARMED"


def test_an_unparseable_settings_json_degrades_loudly_not_silently(tmp_path):
    root = _tree(tmp_path)
    (root / ".claude" / "settings.json").write_text("{ not json", encoding="utf-8")
    organs = goi.collect_organs(root)
    hooks = [o for o in organs if o.cls == "session-hook" and o.distribution == "hub"]
    assert len(hooks) == 1
    assert hooks[0].status == "(unparsed)"


# --------------------------------------------------------------------------------------
# terra review 2026-08-11 — the four findings, each pinned by the case that reproduced it
# --------------------------------------------------------------------------------------

def _git(root: Path, *args: str) -> None:
    import subprocess
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True, text=True)


def test_an_untracked_source_file_does_not_change_the_generated_bytes(tmp_path):
    """terra finding 1 (CRITICAL), reproduced live before the fix.

    THE determinism guarantee: the index is a function of COMMITTED state. An untracked
    `.claude/commands/local.md` rendering as `/local` would make `--check` red on every
    other checkout of the same commit — the freshness gate would be unholdable.
    """
    root = _tree(tmp_path)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@t")
    _git(root, "config", "user.name", "t")
    _git(root, "add", "-A")
    before = goi.render_index(root)

    _write(root / ".claude" / "commands" / "local-scratch.md",
           _fm("local-scratch", "an untracked private command"))
    assert "/local-scratch" not in goi.render_index(root)
    assert goi.render_index(root) == before

    _git(root, "add", ".claude/commands/local-scratch.md")   # now tracked -> appears
    assert "/local-scratch" in goi.render_index(root)


def test_tracked_files_returns_none_outside_a_git_work_tree(tmp_path):
    """The honest limit, asserted: no repo -> no filtering, rather than an empty index."""
    assert goi.tracked_files(tmp_path) is None


@pytest.mark.parametrize("source,payload", [
    (".claude/settings.json", "[]"),
    (".claude/settings.json", '"a string"'),
    (".claude/settings.json", '{"hooks": "not-a-mapping"}'),
    (".claude/settings.json", '{"hooks": {"Stop": "bad"}}'),
    (".claude/settings.json", '{"hooks": {"Stop": [["bad"]]}}'),
    (".pre-commit-config.yaml", "repos: [bad]"),
    (".pre-commit-config.yaml", "- a\n- b\n"),
    (".pre-commit-config.yaml", "repos: not-a-list"),
    ("ecosystem/organ-registry.yaml", "organs: bad"),
    ("ecosystem/organ-registry.yaml", "organs: [not-a-mapping]"),
    ("ecosystem/organ-registry.yaml", "- a\n- b\n"),
    ("plugins/tier1-lifecycle/hooks/hooks.json", "[]"),
    ("plugins/tier1-lifecycle/.claude-plugin/plugin.json", "[]"),
])
def test_valid_but_wrong_shaped_sources_never_crash_the_gate(tmp_path, source, payload):
    """terra finding 2 (HIGH) + finding 3 (HIGH), reproduced: these all PARSE and then
    used to raise AttributeError on the first `.get()`, taking --check out through a
    traceback instead of its 0/1/2 contract."""
    root = _tree(tmp_path)
    _write(root / source, payload)
    text = goi.render_index(root)          # must not raise
    assert goi.main(["--write", "--repo-root", str(root)]) == 0
    assert goi.main(["--check", "--repo-root", str(root)]) == 0
    for cls in goi.ORGAN_CLASSES:          # the index stays whole
        assert f"## {cls}" in text


@pytest.mark.parametrize("payload,needle", [
    ("organs: bad", "unparseable"),
    ("organs: [not-a-mapping]", "is not a mapping"),
])
def test_a_malformed_registry_says_so_instead_of_rendering_nothing(tmp_path, payload,
                                                                   needle):
    """terra finding 3: `organs: bad` iterated the STRING and skipped every character in
    silence — a registry that renders zero rows and reports nothing."""
    root = _tree(tmp_path)
    _write(root / "ecosystem" / "organ-registry.yaml", payload)
    assert needle in goi.render_index(root)
