"""Integration tests for [#276] D2 waiver-honoring through the REAL orchestrator
(deploy/tool.py `assess()` / `execute()`) driving the REAL `PrecommitCarrier`
(deploy/carrier_precommit.py) -- not a scripted fake, unlike
tests/test_deploy_tool_execute.py / tests/test_deploy_prune.py's execute-sweep
suite. Proves lane step 3 ("prove both legs on a previously-deployed consumer
shape") end-to-end: a consumer's own `.methodology.yaml` makes `--execute` stand
down on BOTH the prune leg (no REFUSE-abort) and the add/converge leg (no
re-append), with a full record write on success -- and a CONTRAST run without the
allowlist still aborts, proving the fix discriminates rather than disabling the
hash-guard.

Hermetic: hub + consumer are throwaway git repos in tmp_path (mirrors
tests/test_deploy_prune.py's `world` fixture); the manifest is a minimal fixture
carrying exactly one carrier (precommit) so only carrier_precommit.py is exercised.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml


import tool  # noqa: E402
from carrier_precommit import PrecommitCarrier  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent
_V120 = yaml.safe_load(
    (_REPO_ROOT / "deploy" / "manifest-v1.2.0.yaml").read_text(encoding="utf-8")
)
_RUFF_COMPONENT = next(c for c in _V120["components"] if c["id"] == "ruff-gate")
_RUFF_REPO = _RUFF_COMPONENT["prune"]["match"]["repo"]
_RUFF_EXPECTED = _RUFF_COMPONENT["prune"]["expected"]

_HUB_REPO = "https://github.com/rdwornik/dev-knowledge"
_HUB_REV = "v1.2.0"
_WAIVED_HOOK = "codemap-freshness"
_KEPT_HOOK = "toc-freshness"

REGISTRY_TEXT = (
    "repos:\n"
    "  ai-council:\n"
    "    deployed_methodology_version: null\n"
    "    deployed_date: null\n"
    "    source_tag: null\n"
)


def _manifest() -> dict:
    return {
        "methodology_version": "1.2.0",
        "source_tag": "v1.2.0",
        "carriers": [{
            "id": "precommit", "order": 1, "implemented": True,
            "target": {
                "config_path": ".pre-commit-config.yaml",
                "required_repos": [],
                "hub_hooks": {
                    "rev": _HUB_REV,
                    "marker_hook_ids": [_WAIVED_HOOK, _KEPT_HOOK],
                    "repo": _HUB_REPO,
                    "hooks": [{"id": _WAIVED_HOOK}, {"id": _KEPT_HOOK}],
                },
                "required_local_hooks": [],
            },
        }],
        "components": [_RUFF_COMPONENT],
    }


def _consumer_config() -> dict:
    """A previously-deployed consumer carrying BOTH live-corpus shapes at once:
    the ai-council-shape consumer-owned ruff gate (prune leg) AND a hub-hooks
    entry missing the waived hook (add leg, the #276 FOLD shape)."""
    return {
        "repos": [
            {"repo": _RUFF_REPO, "rev": _RUFF_EXPECTED["rev"], "hooks": [{"id": "ruff"}]},
            {"repo": _HUB_REPO, "rev": _HUB_REV, "hooks": [{"id": _KEPT_HOOK}]},
        ]
    }


def _write_methodology_yaml(repo: Path, components: list[str]) -> None:
    lines = ["sanctioned_divergences:"]
    for cid in components:
        lines += [
            f"  - component: {cid}",
            "    reason: >-",
            "      declared for this test's LANE-d-4 fixture",
            "    review_date: 2099-01-01",
        ]
    (repo / ".methodology.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


@pytest.fixture
def world(tmp_path):
    hub = tmp_path / "hub"
    consumer = tmp_path / "consumer"

    def g(repo, *args):
        r = subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True)
        assert r.returncode == 0, (args, r.stderr)
        return r.stdout.strip()

    hub.mkdir()
    g(hub, "init", "-b", "main")
    g(hub, "config", "user.email", "t@t")
    g(hub, "config", "user.name", "T")
    (hub / "ecosystem").mkdir()
    (hub / "ecosystem" / "deployed-versions.yaml").write_text(REGISTRY_TEXT, encoding="utf-8")
    g(hub, "add", "-A")
    g(hub, "commit", "-m", "init")

    consumer.mkdir()
    (consumer / ".pre-commit-config.yaml").write_text(
        yaml.safe_dump(_consumer_config(), sort_keys=False), encoding="utf-8", newline="\n",
    )
    g(consumer, "init", "-b", "main")
    g(consumer, "config", "user.email", "t@t")
    g(consumer, "config", "user.name", "T")
    g(consumer, "add", "-A")
    g(consumer, "commit", "-m", "seed")
    return {"hub": hub, "consumer": consumer, "git": g}


def _ctx(world, *, deployed_version="1.1.0"):
    # non-null: models a PREVIOUSLY-DEPLOYED consumer (ai-council/corp-monorepo),
    # where full ADR-96 prune semantics apply (Done-when's "previously-deployed").
    return tool.PreflightContext(
        repo="ai-council", version="v1.2.0", bare_version="1.2.0",
        repo_root=world["consumer"], source_tag="v1.2.0",
        manifest=_manifest(), manifest_path=Path("manifest-v1.2.0.yaml"),
        deployed_version=deployed_version,
    )


def _exec(world, **kw):
    return tool.execute(
        _ctx(world),
        carrier_factory=lambda root: {"precommit": PrecommitCarrier(root)},
        git=tool._default_git, hub_root=world["hub"], today="2026-09-01",
        auto_approve=True, **kw,
    )


# ---------------------------------------------------------------------------
# Contrast baseline -- no .methodology.yaml -> the pre-#276-fix behavior holds:
# --execute REFUSE-aborts on the prune leg. Proves the fix DISCRIMINATES rather
# than disabling the hash-guard wholesale.
# ---------------------------------------------------------------------------


def test_execute_aborts_without_a_waiver(world):
    res = _exec(world)
    assert res.aborted is True
    po = next(p for p in res.prune_outcomes if p.component_id == "ruff-gate")
    assert po.refused
    assert res.record_branch is None  # no record on abort


# ---------------------------------------------------------------------------
# [#276] Done-when, end-to-end: BOTH legs stand down together on a consumer that
# declared BOTH divergences.
# ---------------------------------------------------------------------------


def test_execute_succeeds_when_both_divergences_are_declared(world):
    _write_methodology_yaml(world["consumer"], ["ruff-gate", _WAIVED_HOOK])
    res = _exec(world)

    assert res.aborted is False
    assert res.record_branch is not None  # full success -> the record IS written

    po = next(p for p in res.prune_outcomes if p.component_id == "ruff-gate")
    assert po.pruned is False and po.refused == ()  # skipped, not refused

    # The add leg never touched the file: still missing the waived hook, the
    # consumer-owned ruff entry untouched, the kept hook still present.
    data = yaml.safe_load(
        (world["consumer"] / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    )
    hub_entry = next(e for e in data["repos"] if e["repo"] == _HUB_REPO)
    hub_ids = {h["id"] for h in hub_entry["hooks"]}
    assert _WAIVED_HOOK not in hub_ids
    assert _KEPT_HOOK in hub_ids
    ruff_entry = next(e for e in data["repos"] if e["repo"] == _RUFF_REPO)
    assert ruff_entry["hooks"] == [{"id": "ruff"}]  # byte-untouched


def test_assess_plan_reflects_both_standing_down(world):
    """Read-only assess() (no writes): the prune item is excluded from
    `prune_pending` (no destroy-confirm would fire) and the precommit carrier
    reads PRESENT_CORRECT (no drift to apply)."""
    _write_methodology_yaml(world["consumer"], ["ruff-gate", _WAIVED_HOOK])
    ctx = _ctx(world)
    plan = tool.assess(ctx, carrier_factory=lambda root: {"precommit": PrecommitCarrier(root)})

    assert plan.prune_pending == ()
    precommit_item = next(i for i in plan.items if i.carrier_id == "precommit")
    from contract import CarrierState
    assert precommit_item.state is CarrierState.PRESENT_CORRECT
