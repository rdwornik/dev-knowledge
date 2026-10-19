"""RED-first witnesses for the substrate / paired fields of the live provider registry (schema 1.6.0)."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ecosystem.schema.provider_registry import (  # noqa: E402
    SCHEMA_VERSION,
    ProviderRegistry,
    RoleEntry,
)

_REGISTRY_PATH = _ROOT / "ecosystem" / "provider-registry.yaml"


@pytest.fixture(scope="module")
def live() -> dict:
    return yaml.safe_load(_REGISTRY_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def registry(live) -> ProviderRegistry:
    return ProviderRegistry.model_validate(live)


def _entry(registry, role, provider):
    return next(e for e in registry.roles[role].order if e.provider == provider)


def test_the_schema_version_is_1_6_0():
    assert SCHEMA_VERSION == "1.6.0"


def test_a_role_entry_has_substrate_and_paired_with_safe_defaults():
    assert RoleEntry.model_fields["substrate"].default is None
    assert RoleEntry.model_fields["paired"].default is False


def test_an_invalid_substrate_is_rejected(live):
    data = copy.deepcopy(live)
    data["roles"]["verify"]["order"][0]["substrate"] = "moon"
    with pytest.raises(Exception) as exc:
        ProviderRegistry.model_validate(data)
    assert "substrate" in str(exc.value)


def test_a_valid_substrate_is_accepted(live):
    data = copy.deepcopy(live)
    data["roles"]["verify"]["order"][0]["substrate"] = "local"
    assert ProviderRegistry.model_validate(data).roles["verify"].order[0].substrate == "local"


def test_implement_is_led_by_sonnet_on_a_codespace_not_grok(registry):
    first = registry.roles["implement"].order[0]
    assert (first.provider, first.model, first.substrate) == ("anthropic", "claude-sonnet-5-5", "codespace")
    assert not (first.provider == "xai" and first.model == "grok-4.7")


def test_red_is_led_by_copilot_default_on_a_codespace(registry):
    first = registry.roles["red"].order[0]
    assert first.provider == "copilot-enterprise"
    assert first.model is None
    assert first.substrate == "codespace"


def test_review_is_a_pair_of_codex_local_and_copilot_codespace(registry):
    role = registry.roles["review"]
    codex = _entry(registry, "review", "openai")
    copilot = _entry(registry, "review", "copilot-enterprise")
    assert (codex.model, codex.substrate, codex.paired) == ("gpt-5.6-terra", "local", True)
    assert (copilot.model, copilot.substrate, copilot.paired) == (None, "codespace", True)
    assert role.excludes_producer is True


def test_verify_is_sonnet_local(registry):
    first = registry.roles["verify"].order[0]
    assert (first.provider, first.model, first.substrate) == ("anthropic", "claude-sonnet-5-5", "local")


def test_read_keeps_antigravity_local_and_anthropic_on_haiku_5_5(registry):
    assert _entry(registry, "read", "antigravity").substrate == "local"
    assert _entry(registry, "read", "anthropic").model == "claude-haiku-5-5"
    assert "claude-haiku-5-5" in registry.models


@pytest.mark.parametrize("role", ["judge", "orchestrate"])
def test_judge_and_orchestrate_stay_opus_only(registry, role):
    first = registry.roles[role].order[0]
    assert (first.provider, first.model) == ("anthropic", "claude-opus-5-5")
