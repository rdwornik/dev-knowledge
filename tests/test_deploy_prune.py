"""Tests for the deploy remove leg (P2 / [#244] / ADR-96).

The add-only engine gains the ability to PRUNE a status:removed component from a
consumer, safely and verifiably. Coverage maps to the frozen acceptance contract:

- criterion 1 (prune-removes): PRESENT_CLEAN -> prune -> artifact ABSENT +
  verify_pruned ok;
- idempotency: ALREADY_ABSENT -> prune no-ops;
- criterion 3 (hash-guard BOTH paths): clean target prunes; a locally-modified
  target reads PRESENT_MODIFIED and prune REFUSES (no delete, entry still present);
- criterion 4 (golden-diff): pruning ruff-gate leaves every OTHER repo/hook/key
  byte-identical (prune-isolated collateral check);
- criterion 5 / D9 (reconcile integrity): verify_pruned is independent of
  detect_prune -- a sabotaged detect cannot make verify falsely pass; the execute
  sweep aborts before stage/record on a refuse or a failed verify_pruned;
- confirm-on-execute (D-b amendment): a present prune REQUIRES confirmation by
  default; --auto-approve skips it; an add-only plan never prompts;
- PruneUnsupported: a carrier with no remove leg fails loud.

The n=1 subject is ruff-gate; its component (incl. the prune: block) is sourced
from the real manifest-v1.2.0.yaml so the tests track the shipped spec.
"""
from __future__ import annotations

import copy
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_precommit as cp  # noqa: E402
import contract  # noqa: E402
import tool  # noqa: E402
from contract import (  # noqa: E402
    ApplyResult,
    CarrierState,
    PruneResult,
    PruneState,
    PruneUnsupported,
    VerifyResult,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_V120 = yaml.safe_load((_REPO_ROOT / "deploy" / "manifest-v1.2.0.yaml").read_text(encoding="utf-8"))
_RUFF_COMPONENT = next(c for c in _V120["components"] if c["id"] == "ruff-gate")
_RUFF_REPO = _RUFF_COMPONENT["prune"]["match"]["repo"]
_RUFF_EXPECTED = _RUFF_COMPONENT["prune"]["expected"]


def _write_config(repo: Path, data: dict) -> Path:
    path = repo / ".pre-commit-config.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8", newline="\n")
    return path


def _ruff_entry() -> dict:
    """The consumer's ruff entry, byte-matching the deployed shape (PRESENT_CLEAN)."""
    return {
        "repo": _RUFF_REPO,
        "rev": _RUFF_EXPECTED["rev"],
        "hooks": copy.deepcopy(_RUFF_EXPECTED["hooks"]),
    }


def _other_entries() -> list[dict]:
    """Non-ruff entries that must survive a prune byte-identical (golden-diff)."""
    return [
        {"repo": "local", "hooks": [
            {"id": "floor-hash-verify", "entry": "python .claude/check_floor_hash.py",
             "language": "system"}]},
        {"repo": "../.dev-knowledge", "rev": "v1.2.0", "hooks": [
            {"id": "toc-freshness", "files": "^protocols/GUIDE.md$"}]},
    ]


def _carrier(repo: Path) -> cp.PrecommitCarrier:
    return cp.PrecommitCarrier(repo)


# ---------------------------------------------------------------------------
# Contract: PruneUnsupported — the opt-in-per-carrier boundary.
# ---------------------------------------------------------------------------


class _BareCarrier(contract.Carrier):
    """A carrier with only the add-path implemented (no remove leg)."""

    carrier_id = "bare"

    def detect(self, target):
        return CarrierState.PRESENT_CORRECT

    def apply(self, target):
        return ApplyResult(changed=False)

    def verify(self, target):
        return VerifyResult(ok=True)


@pytest.mark.parametrize("method", ["detect_prune", "prune", "verify_pruned"])
def test_base_carrier_prune_raises_unsupported(method):
    car = _BareCarrier()
    with pytest.raises(PruneUnsupported, match="bare"):
        getattr(car, method)({"id": "whatever"})


# ---------------------------------------------------------------------------
# detect_prune — the three states (the hash-guard classification).
# ---------------------------------------------------------------------------


def test_detect_prune_present_clean(tmp_path):
    _write_config(tmp_path, {"repos": [*_other_entries(), _ruff_entry()]})
    assert _carrier(tmp_path).detect_prune(_RUFF_COMPONENT) is PruneState.PRESENT_CLEAN


def test_detect_prune_already_absent(tmp_path):
    _write_config(tmp_path, {"repos": _other_entries()})  # no ruff
    assert _carrier(tmp_path).detect_prune(_RUFF_COMPONENT) is PruneState.ALREADY_ABSENT


def test_detect_prune_absent_when_no_config(tmp_path):
    assert _carrier(tmp_path).detect_prune(_RUFF_COMPONENT) is PruneState.ALREADY_ABSENT


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda e: e.update(rev="v0.99.0"), id="edited-rev"),
    pytest.param(lambda e: e["hooks"][0].update(args=["--fix"]), id="edited-args"),
    pytest.param(lambda e: e["hooks"].append({"id": "ruff-format"}), id="extra-hook"),
    pytest.param(lambda e: e["hooks"][0].pop("name"), id="dropped-field"),
])
def test_detect_prune_modified_on_any_local_edit(tmp_path, mutate):
    entry = _ruff_entry()
    mutate(entry)
    _write_config(tmp_path, {"repos": [*_other_entries(), entry]})
    assert _carrier(tmp_path).detect_prune(_RUFF_COMPONENT) is PruneState.PRESENT_MODIFIED


# ---------------------------------------------------------------------------
# prune — removes clean (criterion 1), idempotent, REFUSES modified (criterion 3).
# ---------------------------------------------------------------------------


def _repos_without_ruff(repo: Path) -> list[dict]:
    data = yaml.safe_load((repo / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    return [e for e in data["repos"] if e.get("repo") != _RUFF_REPO]


def test_prune_removes_clean_and_verifies_absent(tmp_path):
    _write_config(tmp_path, {"repos": [*_other_entries(), _ruff_entry()]})
    car = _carrier(tmp_path)

    result = car.prune(_RUFF_COMPONENT)
    assert result.pruned is True
    assert any(_RUFF_REPO in c for c in result.removed)
    # artifact ABSENT + independent verify confirms it
    assert car.detect_prune(_RUFF_COMPONENT) is PruneState.ALREADY_ABSENT
    assert car.verify_pruned(_RUFF_COMPONENT).ok is True
    data = yaml.safe_load((tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    assert all(e.get("repo") != _RUFF_REPO for e in data["repos"])


def test_prune_idempotent_when_already_absent(tmp_path):
    _write_config(tmp_path, {"repos": _other_entries()})
    result = _carrier(tmp_path).prune(_RUFF_COMPONENT)
    assert result.pruned is False
    assert "already absent" in result.detail


def test_prune_refuses_locally_modified_target(tmp_path):
    entry = _ruff_entry()
    entry["rev"] = "v0.99.0"  # local edit
    _write_config(tmp_path, {"repos": [*_other_entries(), entry]})
    car = _carrier(tmp_path)

    result = car.prune(_RUFF_COMPONENT)
    assert result.pruned is False
    assert result.refused  # surfaced the conflict
    assert "REFUSING" in result.refused[0]
    # the entry is STILL PRESENT — nothing clobbered
    data = yaml.safe_load((tmp_path / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    assert any(e.get("repo") == _RUFF_REPO for e in data["repos"])


# ---------------------------------------------------------------------------
# criterion 4 — golden-diff: the non-pruned surface is byte-identical.
# ---------------------------------------------------------------------------


def test_golden_diff_non_pruned_surface_unchanged(tmp_path):
    car = _carrier(tmp_path)
    # write the initial config through the carrier's own dumper so both snapshots
    # are in canonical form (the only intended change is the ruff entry leaving).
    cp._dump_config(tmp_path / ".pre-commit-config.yaml",
                    {"repos": [*_other_entries(), _ruff_entry()]})
    before_others = _repos_without_ruff(tmp_path)

    car.prune(_RUFF_COMPONENT)

    after_others = _repos_without_ruff(tmp_path)
    assert after_others == before_others  # zero collateral: every other entry intact


# ---------------------------------------------------------------------------
# criterion 5 / D9 — verify_pruned is independent of detect_prune.
# ---------------------------------------------------------------------------


def test_verify_pruned_does_not_route_through_detect(tmp_path, monkeypatch):
    """Sabotage detect's prune judgment; verify_pruned must still catch a present entry."""
    _write_config(tmp_path, {"repos": [*_other_entries(), _ruff_entry()]})  # ruff PRESENT
    car = _carrier(tmp_path)

    def _boom(*_a, **_k):
        raise AssertionError("verify_pruned must not call detect's _classify_prune/_find_repo (D9)")

    monkeypatch.setattr(cp, "_classify_prune", _boom)
    monkeypatch.setattr(cp, "_find_repo", _boom)
    # independent path still (correctly) reports the entry is present -> not absent
    result = car.verify_pruned(_RUFF_COMPONENT)
    assert result.ok is False
    assert any(_RUFF_REPO in f for f in result.failures)


def test_detect_prune_does_not_route_through_verify(tmp_path, monkeypatch):
    """Sabotage verify's absence scan; detect_prune must still classify."""
    _write_config(tmp_path, {"repos": [*_other_entries(), _ruff_entry()]})
    car = _carrier(tmp_path)

    def _boom(*_a, **_k):
        raise AssertionError("detect_prune must not call verify's _verify_absent (D9)")

    monkeypatch.setattr(cp, "_verify_absent", _boom)
    assert car.detect_prune(_RUFF_COMPONENT) is PruneState.PRESENT_CLEAN


# ---------------------------------------------------------------------------
# tool.build_prune_plan + assess — the read-only prune plan.
# ---------------------------------------------------------------------------


def test_build_prune_plan_reports_removed_components(tmp_path):
    _write_config(tmp_path, {"repos": [*_other_entries(), _ruff_entry()]})
    carriers = {"precommit": _carrier(tmp_path)}
    plan = tool.build_prune_plan(_V120, carriers)
    assert len(plan) == 1
    item = plan[0]
    assert item.component_id == "ruff-gate"
    assert item.carrier_id == "precommit"
    assert item.removed_in == "1.2.0"
    assert item.state is PruneState.PRESENT_CLEAN


def test_build_prune_plan_skips_active_components(tmp_path):
    # a manifest with no removed components -> empty prune plan
    manifest = {"components": [c for c in _V120["components"] if c["status"] == "active"]}
    plan = tool.build_prune_plan(manifest, {"precommit": _carrier(tmp_path)})
    assert plan == ()


# ---------------------------------------------------------------------------
# tool.execute — the prune sweep + confirm gate (fake carrier + git world).
# ---------------------------------------------------------------------------


REGISTRY_TEXT = (
    "repos:\n"
    "  ai-council:\n"
    "    deployed_methodology_version: null\n"
    "    deployed_date: null\n"
    "    source_tag: null\n"
)


class FakePruneCarrier(contract.Carrier):
    """Scripted add-path + remove-leg carrier for the execute sweep tests."""

    def __init__(self, cid, *, prune_state=PruneState.PRESENT_CLEAN, verify_absent_ok=True):
        self.carrier_id = cid
        self._prune_state = prune_state
        self._verify_absent_ok = verify_absent_ok
        self.repo_root = None
        self.calls: list[str] = []

    def detect(self, target):
        return CarrierState.PRESENT_CORRECT

    def apply(self, target):
        return ApplyResult(changed=False)

    def verify(self, target):
        return VerifyResult(ok=True)

    def detect_prune(self, component):
        self.calls.append("detect_prune")
        return self._prune_state

    def prune(self, component):
        self.calls.append("prune")
        if self._prune_state is PruneState.PRESENT_MODIFIED:
            return PruneResult(pruned=False, refused=("locally modified -- REFUSING",))
        if self._prune_state is PruneState.ALREADY_ABSENT:
            return PruneResult(pruned=False, detail="already absent")
        return PruneResult(pruned=True, removed=("removed x",))

    def verify_pruned(self, component):
        self.calls.append("verify_pruned")
        return VerifyResult(
            ok=self._verify_absent_ok,
            failures=() if self._verify_absent_ok else ("still present",),
        )


def _manifest(*, removed=True):
    comps = [{"id": "keep", "kind": "hook", "carrier": "precommit",
              "status": "active", "verify": "wired"}]
    if removed:
        comps.append({"id": "ruff-gate", "kind": "hook", "carrier": "precommit",
                      "status": "removed", "removed_in": "1.2.0",
                      "reason": "test tombstone", "verify": "wired",
                      "prune": {"match": {"repo": "x"}, "expected": {}}})
    return {
        "methodology_version": "1.2.0",
        "source_tag": "v1.2.0",
        "carriers": [{"id": "precommit", "order": 1, "implemented": True, "target": {}}],
        "components": comps,
    }


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
    g(consumer, "init", "-b", "main")
    g(consumer, "config", "user.email", "t@t")
    g(consumer, "config", "user.name", "T")
    (consumer / "seed.txt").write_text("seed\n", encoding="utf-8")
    g(consumer, "add", "-A")
    g(consumer, "commit", "-m", "seed")
    return {"hub": hub, "consumer": consumer, "git": g}


def _ctx(world, manifest):
    return tool.PreflightContext(
        repo="ai-council", version="v1.2.0", bare_version="1.2.0",
        repo_root=world["consumer"], source_tag="v1.2.0",
        manifest=manifest, manifest_path=Path("manifest-v1.2.0.yaml"),
    )


def _exec(world, carrier, manifest, **kw):
    return tool.execute(
        _ctx(world, manifest),
        carrier_factory=lambda _root: {carrier.carrier_id: carrier},
        git=tool._default_git, hub_root=world["hub"], today="2026-07-04", **kw,
    )


def test_prune_success_records_and_reports_tombstone(world):
    car = FakePruneCarrier("precommit")
    res = _exec(world, car, _manifest(), auto_approve=True)
    assert res.aborted is False
    assert len(res.prune_outcomes) == 1
    po = res.prune_outcomes[0]
    assert po.component_id == "ruff-gate" and po.pruned and po.verify_ok
    assert po.removed_in == "1.2.0"
    assert res.record_branch is not None  # record written only on full success


def test_confirm_required_by_default_declined_aborts(world):
    car = FakePruneCarrier("precommit")
    calls = {"n": 0}

    def decline(pending):
        calls["n"] += 1
        assert len(pending) == 1  # the one present removed component
        return False

    res = _exec(world, car, _manifest(), prune_confirm=decline)
    assert calls["n"] == 1  # confirm WAS required
    assert res.aborted is True
    assert res.prune_declined is True
    assert res.record_branch is None  # nothing written
    assert "prune" not in car.calls  # the sweep never ran


def test_auto_approve_skips_confirm(world):
    car = FakePruneCarrier("precommit")

    def boom(pending):
        raise AssertionError("--auto-approve must NOT call the confirm prompt")

    res = _exec(world, car, _manifest(), auto_approve=True, prune_confirm=boom)
    assert res.aborted is False
    assert "prune" in car.calls  # pruned without prompting


def test_add_only_plan_never_prompts(world):
    car = FakePruneCarrier("precommit")

    def boom(pending):
        raise AssertionError("an add-only plan (no removed components) must NOT prompt")

    res = _exec(world, car, _manifest(removed=False), prune_confirm=boom)
    assert res.aborted is False
    assert res.prune_outcomes == ()


def test_prune_refuse_aborts_before_record(world):
    car = FakePruneCarrier("precommit", prune_state=PruneState.PRESENT_MODIFIED)
    res = _exec(world, car, _manifest(), auto_approve=True)
    assert res.aborted is True
    assert res.failed_carrier == "ruff-gate"
    assert res.prune_outcomes[0].refused
    assert res.record_branch is None  # criterion 3: refuse -> no record, no stage


def test_failed_verify_pruned_aborts_before_record(world):
    # criterion 5: no state where the record says success while the removed
    # component is still present -> a failed verify_pruned aborts.
    car = FakePruneCarrier("precommit", verify_absent_ok=False)
    res = _exec(world, car, _manifest(), auto_approve=True)
    assert res.aborted is True
    assert res.prune_outcomes[0].verify_ok is False
    assert res.record_branch is None
