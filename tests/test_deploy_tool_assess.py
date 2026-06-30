"""Tests for the deploy orchestrator's ASSESS half (ADR-92 C2a — deploy/tool.py).

Strictly read-only engine: preflight -> detect every carrier -> structured plan,
with NO apply / record write / staging. The suite proves:

- preflight aborts (each gate) with a clear message: bad version (no manifest),
  unregistered consumer, missing consumer tree, unresolvable release tag, dirty
  consumer tree; and passes when all gates are met;
- the assess loop walks carriers in manifest `order`, calls ONLY `detect`, and
  maps each detected state to the right plan row + planned action;
- a carrier whose `detect` RAISES becomes an error row (run continues) — assess
  stays usable against a degraded fleet;
- a not-implemented manifest carrier is skipped (not a failure);
- l0_scope deferred / enforced-elsewhere payloads surface as out-of-scope, not
  failures;
- read-only: a carrier's `apply`/`verify` are NEVER invoked by assess;
- the plugin carrier is driven through the REAL carrier with its CLI **mocked**
  via the injectable runner — no real `claude`, no network, no real consumer.

Git and the carrier factory are injected, so no real git / real fleet / real
`~/.codex` / real `claude` is ever touched.
"""
from __future__ import annotations

import io
import os
import sys
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner
from rich.console import Console

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_plugin as cp  # noqa: E402
import contract  # noqa: E402
import tool  # noqa: E402
from contract import CarrierState  # noqa: E402


# ---------------------------------------------------------------------------
# Test doubles.
# ---------------------------------------------------------------------------


class StubCarrier(contract.Carrier):
    """A carrier with a crafted detect result; apply/verify must never be called."""

    def __init__(self, carrier_id, state=None, raise_on_detect=None):
        self.carrier_id = carrier_id
        self._state = state
        self._raise = raise_on_detect
        self.calls: list[str] = []

    def detect(self, target):
        self.calls.append("detect")
        if self._raise is not None:
            raise self._raise
        return self._state

    def apply(self, target):  # pragma: no cover - asserts it is never reached
        self.calls.append("apply")
        raise AssertionError("assess must never call apply()")

    def verify(self, target):  # pragma: no cover - asserts it is never reached
        self.calls.append("verify")
        raise AssertionError("assess must never call verify()")


def make_git(*, clean=True, tag=True):
    """A fake git runner: control working-tree cleanliness + tag resolvability."""

    def git(args, cwd):
        if args and args[0] == "rev-parse":
            return tool.GitResult(0 if tag else 1, "deadbeef" if tag else "", "")
        if args and args[0] == "status":
            return tool.GitResult(0, "" if clean else " M changed.py\n", "")
        return tool.GitResult(0, "", "")

    return git


ASSESS_MANIFEST = {
    "methodology_version": "1.0.0",
    "source_tag": "v1.0.0",
    "carriers": [
        {
            "id": "global-config",
            "order": 1,
            "implemented": True,
            "target": {},
            "l0_scope": {
                "deferred_deployables": [
                    {"payload": "surface-closures", "target": "~/.claude hook", "status": "live"}
                ],
                "enforced_elsewhere": [
                    {
                        "payload": "no-ff-rule",
                        "rule": "branch then --no-ff merge",
                        "enforced_by": "pre-commit + /ship",
                    }
                ],
            },
        },
        {"id": "tier1-plugin", "order": 2, "implemented": True, "target": {}},
        {"id": "precommit", "order": 3, "implemented": True, "target": {}},
        {"id": "floor", "order": 4, "implemented": True, "target": {}},
        {"id": "future-carrier", "order": 5, "implemented": False, "target": {}},
    ],
}


def make_ctx(repo_root, manifest=None):
    """Build a preflight-passed context directly (preflight tested separately)."""
    return tool.PreflightContext(
        repo="fakerepo",
        version="v1.0.0",
        bare_version="1.0.0",
        repo_root=Path(repo_root),
        source_tag="v1.0.0",
        manifest=manifest or ASSESS_MANIFEST,
        manifest_path=Path("manifest-v1.0.0.yaml"),
    )


# ---------------------------------------------------------------------------
# Preflight.
# ---------------------------------------------------------------------------


@pytest.fixture
def preflight_world(tmp_path):
    """A hermetic hub/consumer/registry layout for preflight tests."""
    dev = tmp_path / "dev"
    hub = dev / ".dev-knowledge"
    deploy_dir = hub / "deploy"
    consumer = dev / "myrepo"
    for d in (deploy_dir, consumer):
        d.mkdir(parents=True)
    (deploy_dir / "manifest-v1.0.0.yaml").write_text(
        yaml.safe_dump(
            {
                "methodology_version": "1.0.0",
                "source_tag": "v1.0.0",
                "carriers": [{"id": "precommit", "order": 1, "implemented": True, "target": {}}],
            }
        ),
        encoding="utf-8",
    )
    registry = dev / "deployed-versions.yaml"
    registry.write_text(
        yaml.safe_dump({"repos": {"myrepo": {"deployed_methodology_version": None}}}),
        encoding="utf-8",
    )
    return {"hub": hub, "deploy_dir": deploy_dir, "registry": registry}


def _preflight(world, repo="myrepo", version="v1.0.0", git=None):
    return tool.preflight(
        repo,
        version,
        hub_root=world["hub"],
        deploy_dir=world["deploy_dir"],
        registry_path=world["registry"],
        git=git or make_git(),
    )


def test_preflight_passes_when_all_gates_met(preflight_world):
    ctx = _preflight(preflight_world)
    assert ctx.repo == "myrepo"
    assert ctx.bare_version == "1.0.0"
    assert ctx.source_tag == "v1.0.0"
    assert ctx.repo_root.name == "myrepo"


def test_preflight_accepts_bare_and_v_prefixed_version(preflight_world):
    assert _preflight(preflight_world, version="1.0.0").bare_version == "1.0.0"
    assert _preflight(preflight_world, version="v1.0.0").bare_version == "1.0.0"


def test_preflight_aborts_on_missing_manifest(preflight_world):
    with pytest.raises(tool.PreflightError, match="no manifest"):
        _preflight(preflight_world, version="v9.9.9")


def test_preflight_aborts_on_unregistered_consumer(preflight_world):
    with pytest.raises(tool.PreflightError, match="not a registered consumer"):
        _preflight(preflight_world, repo="strangerepo")


def test_preflight_aborts_on_missing_consumer_tree(preflight_world, tmp_path):
    # Registered but the directory does not exist on disk.
    reg = tmp_path / "dev" / "deployed-versions.yaml"
    reg.write_text(
        yaml.safe_dump({"repos": {"ghostrepo": {"deployed_methodology_version": None}}}),
        encoding="utf-8",
    )
    preflight_world["registry"] = reg
    with pytest.raises(tool.PreflightError, match="working tree not found"):
        _preflight(preflight_world, repo="ghostrepo")


def test_preflight_aborts_on_unresolvable_tag(preflight_world):
    with pytest.raises(tool.PreflightError, match="does not resolve"):
        _preflight(preflight_world, git=make_git(tag=False))


def test_preflight_aborts_on_dirty_tree(preflight_world):
    with pytest.raises(tool.PreflightError, match="not clean"):
        _preflight(preflight_world, git=make_git(clean=False))


# ---------------------------------------------------------------------------
# Assess loop + plan.
# ---------------------------------------------------------------------------


def _stub_factory(states):
    """A carrier factory yielding StubCarriers for the given {id: state-or-exc}."""
    stubs = {}
    for cid, val in states.items():
        if isinstance(val, Exception):
            stubs[cid] = StubCarrier(cid, raise_on_detect=val)
        else:
            stubs[cid] = StubCarrier(cid, state=val)

    def factory(repo_root):
        return stubs

    factory.stubs = stubs  # exposed for assertions
    return factory


def test_assess_maps_each_state_to_a_plan_row(tmp_path):
    factory = _stub_factory(
        {
            "global-config": CarrierState.PRESENT_CORRECT,
            "tier1-plugin": CarrierState.ABSENT,
            "precommit": CarrierState.PRESENT_DRIFTED,
            "floor": CarrierState.PRESENT_WRONG_VERSION,
        }
    )
    plan = tool.assess(make_ctx(tmp_path), carrier_factory=factory)

    by_id = {i.carrier_id: i for i in plan.items}
    assert by_id["global-config"].state is CarrierState.PRESENT_CORRECT
    assert by_id["global-config"].action == "already correct -- skip"
    assert by_id["tier1-plugin"].state is CarrierState.ABSENT
    assert "would apply from scratch" in by_id["tier1-plugin"].action
    assert by_id["precommit"].state is CarrierState.PRESENT_DRIFTED
    assert "would reconcile drift" in by_id["precommit"].action
    assert by_id["floor"].state is CarrierState.PRESENT_WRONG_VERSION
    assert "would update to target version" in by_id["floor"].action


def test_assess_walks_carriers_in_manifest_order(tmp_path):
    factory = _stub_factory(
        {
            "global-config": CarrierState.ABSENT,
            "tier1-plugin": CarrierState.ABSENT,
            "precommit": CarrierState.ABSENT,
            "floor": CarrierState.ABSENT,
        }
    )
    plan = tool.assess(make_ctx(tmp_path), carrier_factory=factory)
    orders = [i.order for i in plan.items]
    assert orders == sorted(orders)
    assert [i.carrier_id for i in plan.items][:4] == [
        "global-config",
        "tier1-plugin",
        "precommit",
        "floor",
    ]


def test_assess_summary_buckets(tmp_path):
    factory = _stub_factory(
        {
            "global-config": CarrierState.PRESENT_CORRECT,
            "tier1-plugin": CarrierState.ABSENT,
            "precommit": CarrierState.PRESENT_DRIFTED,
            "floor": CarrierState.PRESENT_WRONG_VERSION,
        }
    )
    plan = tool.assess(make_ctx(tmp_path), carrier_factory=factory)
    assert len(plan.needs_apply) == 3
    assert len(plan.correct) == 1
    assert len(plan.errored) == 0
    assert len(plan.skipped) == 1  # future-carrier (implemented: false)


def test_assess_skips_not_implemented_carrier(tmp_path):
    factory = _stub_factory({"global-config": CarrierState.ABSENT, "tier1-plugin": CarrierState.ABSENT,
                             "precommit": CarrierState.ABSENT, "floor": CarrierState.ABSENT})
    plan = tool.assess(make_ctx(tmp_path), carrier_factory=factory)
    future = next(i for i in plan.items if i.carrier_id == "future-carrier")
    assert future.implemented is False
    assert future.state is None
    assert "not implemented" in future.action


def test_assess_captures_detect_error_and_continues(tmp_path):
    factory = _stub_factory(
        {
            "global-config": CarrierState.ABSENT,
            "tier1-plugin": RuntimeError("claude CLI not found"),
            "precommit": CarrierState.PRESENT_CORRECT,
            "floor": CarrierState.ABSENT,
        }
    )
    plan = tool.assess(make_ctx(tmp_path), carrier_factory=factory)
    by_id = {i.carrier_id: i for i in plan.items}
    # the raising carrier is an error row...
    assert by_id["tier1-plugin"].state is None
    assert by_id["tier1-plugin"].error == "claude CLI not found"
    assert len(plan.errored) == 1
    # ...and the run continued: later carriers were still detected.
    assert by_id["precommit"].state is CarrierState.PRESENT_CORRECT
    assert by_id["floor"].state is CarrierState.ABSENT


def test_assess_surfaces_l0_scope_out_of_scope_not_failures(tmp_path):
    factory = _stub_factory({"global-config": CarrierState.ABSENT, "tier1-plugin": CarrierState.ABSENT,
                             "precommit": CarrierState.ABSENT, "floor": CarrierState.ABSENT})
    plan = tool.assess(make_ctx(tmp_path), carrier_factory=factory)
    payloads = {o.payload for o in plan.out_of_scope}
    reasons = {o.reason for o in plan.out_of_scope}
    assert payloads == {"surface-closures", "no-ff-rule"}
    assert reasons == {"deferred deployable", "enforced elsewhere"}


def test_assess_is_read_only_apply_and_verify_never_called(tmp_path):
    factory = _stub_factory({"global-config": CarrierState.ABSENT, "tier1-plugin": CarrierState.ABSENT,
                             "precommit": CarrierState.PRESENT_DRIFTED, "floor": CarrierState.PRESENT_CORRECT})
    tool.assess(make_ctx(tmp_path), carrier_factory=factory)
    for stub in factory.stubs.values():
        assert stub.calls == ["detect"]  # detect only — never apply/verify


# ---------------------------------------------------------------------------
# Integration: REAL carriers against a crafted consumer, plugin CLI mocked.
# ---------------------------------------------------------------------------


def test_assess_real_carriers_against_crafted_consumer(tmp_path, monkeypatch):
    """All four REAL carriers detect ABSENT on an empty consumer; no real CLI/fleet.

    The plugin carrier runs through the genuine PluginCarrier with its runner
    mocked (returns an empty `plugin list --json`), so no real `claude` is
    invoked; global-config points at a temp user base; precommit/floor see no
    consumer files. This exercises the orchestrator over the real detect() paths.
    """
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    user_base = tmp_path / "userhome" / ".codex"  # no AGENTS.md -> global-config ABSENT

    def fake_plugin_runner(args, cwd):
        # Only `plugin list --json` is reached by detect; return an empty list.
        return cp.CmdResult(0, "[]", "")

    def real_factory(repo_root):
        return tool.make_carriers(
            repo_root, plugin_runner=fake_plugin_runner, user_config_base=user_base
        )

    # Load the REAL v1.0.0 manifest so each carrier gets its real target shape.
    manifest = tool.load_manifest(tool.manifest_path_for("1.0.0"))
    ctx = make_ctx(consumer, manifest=manifest)

    plan = tool.assess(ctx, carrier_factory=real_factory)
    by_id = {i.carrier_id: i for i in plan.items}
    assert by_id["global-config"].state is CarrierState.ABSENT
    assert by_id["tier1-plugin"].state is CarrierState.ABSENT
    assert by_id["precommit"].state is CarrierState.ABSENT
    assert by_id["floor"].state is CarrierState.ABSENT
    assert len(plan.errored) == 0  # every real detect ran cleanly, no crash


# ---------------------------------------------------------------------------
# Rendering + CLI wiring.
# ---------------------------------------------------------------------------


def test_render_plan_emits_assess_banner_and_no_record_footer(tmp_path):
    factory = _stub_factory({"global-config": CarrierState.ABSENT, "tier1-plugin": CarrierState.ABSENT,
                             "precommit": CarrierState.PRESENT_CORRECT, "floor": CarrierState.ABSENT})
    plan = tool.assess(make_ctx(tmp_path), carrier_factory=factory)
    buf = io.StringIO()
    render_console = Console(file=buf, width=200, force_terminal=False)
    tool.render_plan(plan, console=render_console)
    out = buf.getvalue()
    assert "ASSESS" in out
    assert "Out of scope" in out
    assert "No record will be written in assess mode" in out


def test_cli_execute_flag_is_wired_not_guarded():
    # C2b implemented --execute: the C2a "implemented in C2b" guard is GONE; the
    # flag now reaches the real execute path (which here aborts at preflight,
    # since 'myrepo' is not a registered consumer -- so nothing is mutated).
    res = CliRunner().invoke(tool.deploy, ["myrepo", "--target", "v1.0.0", "--execute"])
    assert res.exit_code != 0
    assert "C2b" not in res.output          # the assess-era guard is gone
    assert "preflight failed" in res.output  # wired to the real execute path


def test_cli_surfaces_preflight_failure(monkeypatch):
    def boom(*a, **k):
        raise tool.PreflightError("registry absent")

    monkeypatch.setattr(tool, "preflight", boom)
    res = CliRunner().invoke(tool.deploy, ["myrepo", "--target", "v1.0.0"])
    assert res.exit_code != 0
    assert "preflight failed" in res.output
    assert "registry absent" in res.output
