"""Tests for the tier1-plugin carrier (ADR-92 — the external-CLI carrier).

Covers the (four-state) reconcile model on the plugin carrier
(deploy/carrier_plugin.py) against the ADR-92 contract, with the `claude` CLI
**fully mocked** — NO real `claude` invocation happens in this suite (every
carrier is built with an injected ``runner``; the one real install lives in the
isolated throwaway smoke-test, not here):

- absent -> install -> verify (marketplace add PRECEDES install — finding (a) gotcha);
- drifted (installed-but-disabled) -> re-install -> enabled;
- wrong version -> `plugin update` (NOT install) -> at target;
- correct -> idempotent no-op (no marketplace/install/update issued);
- install failure -> apply raises PluginCliError (no silent partial record);
- verify reports failures (settings-not-enabled / version-mismatch) not a silent pass;
- detect/verify INDEPENDENCE (D9): each survives the other's judgment helper being
  sabotaged, proving they share no correctness-judgment code path;
- projectPath isolation: a plugin installed in OTHER repos is not mistaken for this one.

The target version is monkeypatched to a fixed value so the suite does not couple
to the live plugin.json version.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "deploy"))

import carrier_plugin as cp  # noqa: E402
import contract  # noqa: E402

TARGET_VERSION = "9.9.9"  # fixed test spec — decoupled from the live plugin.json
PLUGIN = cp.DEFAULT_PLUGIN
_TARGET = {"plugin": PLUGIN, "marketplace": cp.DEFAULT_MARKETPLACE, "scope": "project"}


@pytest.fixture(autouse=True)
def _fixed_target_version(monkeypatch):
    """Pin the spec version so tests don't track the live plugin.json bumps."""
    monkeypatch.setattr(cp, "_read_target_version", lambda *_a, **_k: TARGET_VERSION)


# ---------------------------------------------------------------------------
# A mock `claude` CLI that models the installed state (NO real subprocess).
# ---------------------------------------------------------------------------


class FakeCli:
    """Injectable runner standing in for the real `claude` binary.

    Models just enough state to drive the carrier: a `plugin list --json` view, a
    set of known marketplaces, and the side effects of install/update (mutating the
    list + writing the consumer .claude/settings.json, exactly as --scope project
    does). ``calls`` records the command sequence so order assertions are possible.
    """

    def __init__(
        self,
        entries=None,
        marketplaces=None,
        install_version=TARGET_VERSION,
        fail_install=False,
        require_marketplace=True,
    ):
        self.entries = [dict(e) for e in (entries or [])]
        self.marketplaces = set(marketplaces or [])
        self.install_version = install_version
        self.fail_install = fail_install
        self.require_marketplace = require_marketplace
        self.calls: list[tuple[str, ...]] = []

    def __call__(self, args, cwd) -> cp.CmdResult:
        args = list(args)
        self.calls.append(tuple(args))
        cwd = Path(cwd)
        if args[:3] == ["claude", "plugin", "list"]:
            return cp.CmdResult(0, json.dumps(self.entries), "")
        if args[:4] == ["claude", "plugin", "marketplace", "add"]:
            source = args[4]
            if source in self.marketplaces:
                return cp.CmdResult(1, "", "marketplace already exists")
            self.marketplaces.add(source)
            return cp.CmdResult(0, "added", "")
        if args[:3] == ["claude", "plugin", "install"]:
            if self.fail_install:
                return cp.CmdResult(1, "", "install boom")
            if self.require_marketplace and not self.marketplaces:
                return cp.CmdResult(1, "", "Plugin not found in marketplace")
            self._install(args[3], cwd)
            self._write_settings(args[3], cwd)
            return cp.CmdResult(0, "installed", "")
        if args[:3] == ["claude", "plugin", "update"]:
            self._set_version(args[3], cwd, self.install_version)
            self._write_settings(args[3], cwd)
            return cp.CmdResult(0, "updated", "")
        return cp.CmdResult(1, "", f"unknown command {args}")

    # -- modelled side effects ---------------------------------------------

    def _entry(self, plugin, cwd):
        norm = cp._norm(cwd)
        for e in self.entries:
            if (
                e.get("id") == plugin
                and e.get("projectPath")
                and cp._norm(e["projectPath"]) == norm
            ):
                return e
        return None

    def _install(self, plugin, cwd):
        e = self._entry(plugin, cwd)
        if e is None:  # fresh install at the install_version, enabled
            self.entries.append(
                {
                    "id": plugin,
                    "version": self.install_version,
                    "scope": "project",
                    "enabled": True,
                    "projectPath": str(cwd),
                }
            )
        else:  # already installed: re-records enablement (install no-ops on version)
            e["enabled"] = True

    def _set_version(self, plugin, cwd, version):
        e = self._entry(plugin, cwd)
        if e is None:
            self.entries.append(
                {
                    "id": plugin,
                    "version": version,
                    "scope": "project",
                    "enabled": True,
                    "projectPath": str(cwd),
                }
            )
        else:
            e["version"] = version
            e["enabled"] = True

    def _write_settings(self, plugin, cwd):
        sp = Path(cwd) / ".claude" / "settings.json"
        sp.parent.mkdir(parents=True, exist_ok=True)
        data = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else {}
        data.setdefault("enabledPlugins", {})[plugin] = True
        sp.write_text(json.dumps(data), encoding="utf-8")


def _enabled_entry(repo_root, version=TARGET_VERSION, enabled=True):
    return {
        "id": PLUGIN,
        "version": version,
        "scope": "project",
        "enabled": enabled,
        "projectPath": str(repo_root),
    }


def _write_settings_enabled(repo_root):
    sp = Path(repo_root) / ".claude" / "settings.json"
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps({"enabledPlugins": {PLUGIN: True}}), encoding="utf-8")


# ---------------------------------------------------------------------------
# absent -> install -> verify (and marketplace add precedes install)
# ---------------------------------------------------------------------------


def test_absent_detects_then_installs_and_verifies(tmp_path):
    fake = FakeCli(entries=[], marketplaces=[])
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)
    assert car.detect(_TARGET) is contract.CarrierState.ABSENT

    result = car.apply(_TARGET)
    assert result.changed is True
    assert result.changes  # structured output

    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_TARGET).ok is True
    # the consumer .claude/settings.json now records the enablement
    settings = json.loads((tmp_path / ".claude" / "settings.json").read_text())
    assert settings["enabledPlugins"][PLUGIN] is True


def test_marketplace_add_precedes_install(tmp_path):
    """finding (a) gotcha: install fails on a fresh cache without marketplace add."""
    fake = FakeCli(entries=[], marketplaces=[], require_marketplace=True)
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)
    car.apply(_TARGET)
    add_idx = next(i for i, c in enumerate(fake.calls) if c[:4] == ("claude", "plugin", "marketplace", "add"))
    install_idx = next(i for i, c in enumerate(fake.calls) if c[:3] == ("claude", "plugin", "install"))
    assert add_idx < install_idx  # add must come first or the fake install would 404


# ---------------------------------------------------------------------------
# drifted (installed but NOT enabled) -> reconcile to enabled
# ---------------------------------------------------------------------------


def test_drifted_installed_but_disabled_reconciles(tmp_path):
    fake = FakeCli(entries=[_enabled_entry(tmp_path, enabled=False)], marketplaces=[tmp_path])
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)
    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_DRIFTED

    car.apply(_TARGET)
    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_TARGET).ok is True


# ---------------------------------------------------------------------------
# wrong version -> `plugin update` (NOT install)
# ---------------------------------------------------------------------------


def test_wrong_version_uses_update_not_install(tmp_path):
    fake = FakeCli(entries=[_enabled_entry(tmp_path, version="0.0.1")], marketplaces=[tmp_path])
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)
    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_WRONG_VERSION

    result = car.apply(_TARGET)
    assert result.changed is True
    assert any(c[:3] == ("claude", "plugin", "update") for c in fake.calls)
    assert not any(c[:3] == ("claude", "plugin", "install") for c in fake.calls)
    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_CORRECT
    assert car.verify(_TARGET).ok is True


# ---------------------------------------------------------------------------
# correct -> idempotent no-op (no mutating CLI issued)
# ---------------------------------------------------------------------------


def test_correct_is_idempotent_noop(tmp_path):
    fake = FakeCli(entries=[_enabled_entry(tmp_path)], marketplaces=[tmp_path])
    _write_settings_enabled(tmp_path)
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)
    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_CORRECT

    result = car.apply(_TARGET)
    assert result.changed is False
    assert result.changes == ()
    # only read-only `plugin list` ran — no marketplace add / install / update
    assert all(c[:3] == ("claude", "plugin", "list") for c in fake.calls)


# ---------------------------------------------------------------------------
# install failure -> apply raises (no silent partial record)
# ---------------------------------------------------------------------------


def test_install_failure_raises(tmp_path):
    fake = FakeCli(entries=[], marketplaces=[], fail_install=True)
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)
    with pytest.raises(cp.PluginCliError):
        car.apply(_TARGET)


# ---------------------------------------------------------------------------
# verify reports failures (not a silent pass)
# ---------------------------------------------------------------------------


def test_verify_on_absent_is_not_ok(tmp_path):
    fake = FakeCli(entries=[], marketplaces=[])
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)
    result = car.verify(_TARGET)
    assert result.ok is False
    assert result.failures


def test_verify_fails_when_settings_disabled_despite_list(tmp_path):
    """List shows enabled, but settings.json does NOT — verify (settings-anchored) fails."""
    fake = FakeCli(entries=[_enabled_entry(tmp_path)], marketplaces=[tmp_path])
    # no settings.json written -> enabledPlugins missing
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)
    result = car.verify(_TARGET)
    assert result.ok is False
    assert any("settings.json" in f for f in result.failures)


def test_verify_fails_on_version_mismatch(tmp_path):
    fake = FakeCli(entries=[_enabled_entry(tmp_path, version="0.0.1")], marketplaces=[tmp_path])
    _write_settings_enabled(tmp_path)
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)
    result = car.verify(_TARGET)
    assert result.ok is False
    assert any("version" in f for f in result.failures)


# ---------------------------------------------------------------------------
# projectPath isolation — plugin installed in OTHER repos is not mistaken for this
# ---------------------------------------------------------------------------


def test_other_repo_install_is_not_counted(tmp_path):
    other = tmp_path / "other-repo"
    fake = FakeCli(entries=[_enabled_entry(other)], marketplaces=[tmp_path])
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)
    # the plugin is installed for `other`, not for tmp_path -> ABSENT here
    assert car.detect(_TARGET) is contract.CarrierState.ABSENT


# ---------------------------------------------------------------------------
# D9 — verify is independent of detect (no shared correctness-judgment path)
# ---------------------------------------------------------------------------


def test_verify_does_not_route_through_detect_classifier(tmp_path, monkeypatch):
    """Sabotage detect's judgment (_classify_plugin); verify must still pass."""
    fake = FakeCli(entries=[_enabled_entry(tmp_path)], marketplaces=[tmp_path])
    _write_settings_enabled(tmp_path)
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)

    def _boom(*_a, **_k):
        raise AssertionError("verify must not call detect's _classify_plugin (D9)")

    monkeypatch.setattr(cp, "_classify_plugin", _boom)
    assert car.verify(_TARGET).ok is True


def test_detect_does_not_route_through_verify_judge(tmp_path, monkeypatch):
    """Sabotage verify's judgment (_verify_plugin); detect must still classify."""
    fake = FakeCli(entries=[_enabled_entry(tmp_path)], marketplaces=[tmp_path])
    car = cp.PluginCarrier(tmp_path, runner=fake, marketplace_source=tmp_path)

    def _boom(*_a, **_k):
        raise AssertionError("detect must not call verify's _verify_plugin (D9)")

    monkeypatch.setattr(cp, "_verify_plugin", _boom)
    assert car.detect(_TARGET) is contract.CarrierState.PRESENT_CORRECT
