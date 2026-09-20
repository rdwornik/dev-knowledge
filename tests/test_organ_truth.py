"""lane-l3-organ-truth -- the organ index tells the truth, and an organ with no moment is a FAIL.

Five witnesses the frozen contract names, each RED before the code that turns it GREEN:

  1. a hook set to the manual stage is reported MANUAL, not ARMED (`generate_organ_index`);
  2. an organ absent from L1's declaration makes `check_organ_truth` FAIL;
  3. an organ declared `optional` and unbuilt FAILs and NAMES the lane that owes it;
  4. a declared, armed, existing organ passes;
  5. the adversarial role resolves to a pinned model (`ecosystem/routing-table.yaml`).

Every case but the last two lives on a SYNTHETIC tree under `tmp_path`, so it asserts the logic
rather than today's contents of this repo. The declaration is read from `ecosystem/harness.yaml`
(`moments:` and `stages:`) -- L1's file, never amended here.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest
import yaml

_SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, _SCRIPTS)

import audit as aud  # noqa: E402
import generate_organ_index as goi  # noqa: E402
import graph_queries as gq  # noqa: E402

_REPO = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------------------------- fixtures

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


_PRECOMMIT = (
    "default_stages: [pre-commit]\n"
    "repos:\n"
    "  - repo: local\n"
    "    hooks:\n"
    "      - id: armed-hook\n"
    "        entry: python scripts/a.py\n"
    "      - id: manual-hook\n"
    "        stages: [manual]   # MOVED to the conductor\n"
    "        entry: python scripts/b.py\n"
    "      - id: dated-manual-hook\n"
    "        # manual_until: 2026-10-04\n"
    "        stages: [manual]\n"
    "        entry: python scripts/c.py\n"
    "      - id: mixed-hook\n"
    "        stages: [manual, pre-push]\n"
    "        entry: python scripts/d.py\n"
)


def _index_tree(root: Path, *, disable_all_hooks: bool = False) -> Path:
    _write(root / ".pre-commit-config.yaml", _PRECOMMIT)
    _write(root / ".claude" / "settings.json", json.dumps({
        "disableAllHooks": disable_all_hooks,
        "hooks": {"Stop": [{"hooks": [
            {"type": "command", "command": 'python "$CLAUDE_PROJECT_DIR/scripts/stop.py"'}]}]},
    }))
    return root


def _harness(root: Path, moments=None, stages=None) -> None:
    _write(root / "ecosystem" / "harness.yaml", yaml.safe_dump(
        {"stages": stages or [], "moments": moments or []}, sort_keys=False))


def _organ(oid: str, script: str, *, optional: bool = False, **extra) -> dict:
    row = {"id": oid, "receipt": f"MOMENT-X-{oid.upper()}.json", "manual_until": "2026-10-04",
           "command": ["uv", "run", "--locked", "python", script, "--lane", "{lane}"]}
    if optional:
        row["optional"] = True
    row.update(extra)
    return row


def _moment(name: str, *organs: dict) -> dict:
    return {"name": name, "trigger": "a test trigger", "organs": list(organs)}


def _roster(*paths: str) -> list:
    return [gq.ProcessRow(path=p, process_class="script", triggered=False, trigger="")
            for p in paths]


def _statuses(rows) -> dict[str, str]:
    return {r.path: r.status for r in rows}


# ------------------------------------------------- 1. the index reports REAL arming

def test_a_hook_set_to_the_manual_stage_is_reported_manual_not_armed(tmp_path):
    hooks = {o.name: o for o in goi.collect_git_hooks(_index_tree(tmp_path))}
    assert hooks["manual-hook"].status == "MANUAL"
    assert hooks["armed-hook"].status == "ARMED"
    # the stage it is set to stays visible as the trigger -- MANUAL is the verdict, not a rename
    assert hooks["manual-hook"].trigger == "manual"


def test_a_hook_with_any_automatic_stage_is_armed_even_if_it_also_lists_manual(tmp_path):
    hooks = {o.name: o for o in goi.collect_git_hooks(_index_tree(tmp_path))}
    assert hooks["mixed-hook"].status == "ARMED"


def test_a_manual_hook_carries_its_manual_until_date_where_one_is_declared(tmp_path):
    hooks = {o.name: o for o in goi.collect_git_hooks(_index_tree(tmp_path))}
    assert hooks["dated-manual-hook"].status == "MANUAL until 2026-10-04"
    # no date declared -> no date invented
    assert hooks["manual-hook"].status == "MANUAL"


def test_the_rendered_index_never_calls_a_manual_hook_armed(tmp_path):
    text = goi.render_index(_index_tree(tmp_path))
    rows = {line.split("|")[1].strip(" `"): line for line in text.splitlines()
            if line.startswith("| `") and "pre-commit" in line}
    assert "MANUAL" in rows["manual-hook"] and "ARMED" not in rows["manual-hook"]
    assert "ARMED" in rows["armed-hook"]


def test_session_hooks_are_absent_when_settings_disable_every_hook(tmp_path):
    on = [o for o in goi.collect_session_hooks(_index_tree(tmp_path / "on"))]
    off = [o for o in goi.collect_session_hooks(
        _index_tree(tmp_path / "off", disable_all_hooks=True))]
    assert [o.status for o in on] == ["ARMED"]
    assert [o.status for o in off] == ["ABSENT"]


def test_every_live_hook_stage_the_repo_declares_is_what_the_index_reports():
    """Live tree, computed from the YAML independently of the generator: a hook whose only
    stage is `manual` must never come back ARMED."""
    data = yaml.safe_load((_REPO / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    default = data.get("default_stages") or ["pre-commit"]
    expected = {}
    for repo in data["repos"]:
        for hook in repo.get("hooks") or []:
            stages = hook.get("stages") or default
            expected[hook["id"]] = "MANUAL" if set(stages) == {"manual"} else "ARMED"
    live = {o.name: o.status.split()[0] for o in goi.collect_git_hooks(_REPO)}
    assert live == expected
    assert "MANUAL" in live.values() and "ARMED" in live.values()


# ---------------------------------------------- 2/3/4. the moments mode + the audit check

def test_a_declared_armed_existing_organ_is_declared_at_a_moment(tmp_path):
    _write(tmp_path / "scripts" / "built.py", "print(1)\n")
    _harness(tmp_path, [_moment("lane-start", _organ("built", "scripts/built.py"))])
    rows = gq.organ_moments(tmp_path, roster=_roster("scripts/built.py"))
    assert _statuses(rows) == {"scripts/built.py": gq.MOMENT_DECLARED}
    assert rows[0].moment == "lane-start"


def test_an_organ_absent_from_the_declaration_is_declared_nowhere(tmp_path):
    _write(tmp_path / "scripts" / "built.py", "print(1)\n")
    _write(tmp_path / "scripts" / "stray.py", "print(2)\n")
    _harness(tmp_path, [_moment("lane-start", _organ("built", "scripts/built.py"))])
    rows = gq.organ_moments(tmp_path, roster=_roster("scripts/built.py", "scripts/stray.py"))
    assert _statuses(rows)["scripts/stray.py"] == gq.MOMENT_NOWHERE
    assert _statuses(rows)["scripts/built.py"] == gq.MOMENT_DECLARED


def test_a_spine_stage_command_counts_as_declared(tmp_path):
    _write(tmp_path / "scripts" / "stagey.py", "print(1)\n")
    _harness(tmp_path, stages=[{"stage": 5, "name": "deps", "field": "dependencies",
                                "kind": "deterministic",
                                "command": ["uv", "run", "python", "scripts/stagey.py"]}])
    rows = gq.organ_moments(tmp_path, roster=_roster("scripts/stagey.py"))
    assert _statuses(rows) == {"scripts/stagey.py": gq.MOMENT_DECLARED}


def test_an_optional_organ_whose_command_does_not_exist_is_declared_optional_unbuilt(tmp_path):
    _harness(tmp_path, [_moment(
        "teardown", _organ("no_leftovers", "scripts/no_leftovers.py", optional=True))])
    rows = gq.organ_moments(tmp_path, roster=_roster())
    assert _statuses(rows) == {"scripts/no_leftovers.py": gq.MOMENT_OPTIONAL_UNBUILT}
    assert rows[0].owing_lane == "lane-l5-no-leftovers"


def test_an_optional_organ_that_now_exists_is_declared_not_unbuilt(tmp_path):
    _write(tmp_path / "scripts" / "no_leftovers.py", "print(1)\n")
    _harness(tmp_path, [_moment(
        "teardown", _organ("no_leftovers", "scripts/no_leftovers.py", optional=True))])
    rows = gq.organ_moments(tmp_path, roster=_roster("scripts/no_leftovers.py"))
    assert _statuses(rows) == {"scripts/no_leftovers.py": gq.MOMENT_DECLARED}


def test_a_declared_dotted_organ_id_resolves_to_its_module(tmp_path):
    _write(tmp_path / "scripts" / "merge_receipt.py", "print(1)\n")
    _harness(tmp_path, [_moment("merge", {
        "id": "merge_receipt.models", "receipt": "MOMENT-MERGE-MODELS.json",
        "command": ["uv", "run", "python", "-c", "import merge_receipt as m; m.models()"]})])
    rows = gq.organ_moments(tmp_path, roster=_roster("scripts/merge_receipt.py"))
    assert _statuses(rows) == {"scripts/merge_receipt.py": gq.MOMENT_DECLARED}


def test_moments_mode_is_a_cli_verb_that_refuses_on_a_gap(tmp_path, monkeypatch, capsys):
    _harness(tmp_path, [_moment("lane-start", _organ("built", "scripts/built.py"))])
    _write(tmp_path / "scripts" / "built.py", "print(1)\n")

    class _Store:
        def processes(self):
            return [type("N", (), {"path": p, "process_class": "script", "key": p})()
                    for p in ("scripts/built.py", "scripts/stray.py")]

        def roots(self):
            return set()

        def reachable(self, *_a, **_k):
            return set()

        def trigger_of(self, _k):
            return ""

    monkeypatch.setattr(gq, "_open", lambda _args: _Store())
    code = gq.main(["moments", "--repo-root", str(tmp_path)])
    out = capsys.readouterr().out
    assert code == 1
    assert "scripts/stray.py" in out and gq.MOMENT_NOWHERE in out


def _clean_repo(root: Path) -> Path:
    """A tree the check must PASS: one built organ, declared, index generated from it."""
    _write(root / "scripts" / "built.py", "print(1)\n")
    _harness(root, [_moment("lane-start", _organ("built", "scripts/built.py"))])
    _index_tree(root)
    goi._cmd_write(root)
    return root


def _patch_roster(monkeypatch, *paths: str) -> None:
    monkeypatch.setattr(gq, "roster_rows", lambda _root: _roster(*paths))


def test_the_check_passes_a_declared_armed_existing_organ(tmp_path, monkeypatch):
    _clean_repo(tmp_path)
    _patch_roster(monkeypatch, "scripts/built.py")
    findings = aud.check_organ_truth(tmp_path)
    assert [f.status for f in findings] == ["pass"], [f.evidence for f in findings]


def test_the_check_fails_an_organ_declared_nowhere(tmp_path, monkeypatch):
    _clean_repo(tmp_path)
    _write(tmp_path / "scripts" / "stray.py", "print(2)\n")
    _patch_roster(monkeypatch, "scripts/built.py", "scripts/stray.py")
    findings = aud.check_organ_truth(tmp_path)
    fails = [f for f in findings if f.status == "fail"]
    assert fails and any("scripts/stray.py" in f.evidence for f in fails)
    assert all(f.check_name == "organ_truth" for f in findings)


def test_the_check_fails_an_optional_unbuilt_organ_and_names_the_owing_lane(
        tmp_path, monkeypatch):
    _clean_repo(tmp_path)
    _harness(tmp_path, [_moment(
        "lane-start", _organ("built", "scripts/built.py"),
        _organ("test_pairing", "scripts/test_pairing.py", optional=True))])
    _patch_roster(monkeypatch, "scripts/built.py")
    fails = [f for f in aud.check_organ_truth(tmp_path) if f.status == "fail"]
    assert len(fails) == 1
    assert "scripts/test_pairing.py" in fails[0].evidence
    assert "lane-l6-test-pairing" in fails[0].evidence


def test_the_check_fails_an_index_claim_that_contradicts_the_live_config(tmp_path, monkeypatch):
    _clean_repo(tmp_path)
    index = tmp_path / "ecosystem" / "organ-index.md"
    index.write_text(index.read_text(encoding="utf-8").replace(
        "| `manual-hook` | git-hook | manual | `.pre-commit-config.yaml` | pre-commit | MANUAL |",
        "| `manual-hook` | git-hook | manual | `.pre-commit-config.yaml` | pre-commit | ARMED |"),
        encoding="utf-8")
    _patch_roster(monkeypatch, "scripts/built.py")
    fails = [f for f in aud.check_organ_truth(tmp_path) if f.status == "fail"]
    assert fails and any("manual-hook" in f.evidence and "ARMED" in f.evidence for f in fails)


def test_the_check_fails_when_the_index_it_must_check_is_absent(tmp_path, monkeypatch):
    _clean_repo(tmp_path)
    (tmp_path / "ecosystem" / "organ-index.md").unlink()
    _patch_roster(monkeypatch, "scripts/built.py")
    assert any(f.status == "fail" for f in aud.check_organ_truth(tmp_path))


def test_the_check_is_not_applicable_to_a_repo_with_no_harness(tmp_path):
    findings = aud.check_organ_truth(tmp_path)
    assert [f.status for f in findings] == ["n/a"]


def test_the_check_is_registered_and_its_tier_is_declared_ship():
    assert aud.check_organ_truth in aud.ALL_CHECKS
    assert aud.tier_of(aud.check_organ_truth) == aud.TIER_SHIP


# ---------------------------------------------------- 5. the adversarial role is pinned

def test_the_adversarial_role_resolves_to_a_pinned_model():
    table = yaml.safe_load((_REPO / "ecosystem" / "routing-table.yaml").read_text("utf-8"))
    row = table["roles"]["adversarial"]
    assert row["cli"] == "codex"
    assert row.get("model"), "the adversarial role carries no model pin"
    registry = yaml.safe_load((_REPO / "ecosystem" / "provider-registry.yaml").read_text("utf-8"))
    assert row["model"] in registry["models"], (
        "the pin must be a model the repo's own registry already knows -- no invented provider")


# ---------- codex terra review (docs/audits/2026-09-20-codex-l3-organ-truth.md), three HIGHs

def test_a_from_import_in_a_dash_c_command_names_its_script(tmp_path):
    _write(tmp_path / "scripts" / "fleet_health.py", "print(1)\n")
    _harness(tmp_path, [_moment("lane-end", {
        "id": "seat_line", "receipt": "MOMENT-X-SEAT.json",
        "command": ["uv", "run", "python", "-c",
                    "import sys; sys.path.insert(0, 'scripts'); from fleet_health import f; f()"]})])
    rows = gq.organ_moments(tmp_path, roster=_roster("scripts/fleet_health.py"))
    assert _statuses(rows) == {"scripts/fleet_health.py": gq.MOMENT_DECLARED}


def test_an_absent_optional_organ_imported_via_dash_c_is_still_unbuilt(tmp_path):
    _harness(tmp_path, [_moment("lane-end", {
        "id": "future", "receipt": "MOMENT-X-FUTURE.json", "optional": True,
        "command": ["uv", "run", "python", "-c",
                    "import sys; sys.path.insert(0, 'scripts'); import future_organ as f; f.run()"]})])
    rows = gq.organ_moments(tmp_path, roster=_roster())
    assert _statuses(rows) == {"scripts/future_organ.py": gq.MOMENT_OPTIONAL_UNBUILT}


def test_a_malformed_organ_command_is_refused_not_read_as_empty(tmp_path):
    _harness(tmp_path, [_moment("teardown", {
        "id": "bad", "receipt": "MOMENT-X-BAD.json", "optional": True,
        "command": "python scripts/no_leftovers.py"})])
    with pytest.raises(gq.MomentsUnreadable):
        gq.load_declaration(tmp_path)


def test_a_malformed_moment_shape_is_refused(tmp_path):
    _write(tmp_path / "ecosystem" / "harness.yaml",
           yaml.safe_dump({"stages": [], "moments": [{"name": "m", "organs": "nope"}]}))
    with pytest.raises(gq.MomentsUnreadable):
        gq.load_declaration(tmp_path)


def test_an_index_row_for_a_hook_the_config_no_longer_carries_contradicts_whatever_it_claims(
        tmp_path):
    _clean_repo(tmp_path)
    index = tmp_path / "ecosystem" / "organ-index.md"
    ghost = ("| `ghost-hook` | git-hook | manual | `.pre-commit-config.yaml` | pre-commit "
             "| MANUAL until 2026-10-04 |\n")
    marker = "| `manual-hook` |"
    index.write_text(index.read_text(encoding="utf-8").replace(marker, ghost + marker, 1),
                     encoding="utf-8")
    contradictions = goi.arming_contradictions(tmp_path)
    assert any("ghost-hook" in c for c in contradictions), contradictions
