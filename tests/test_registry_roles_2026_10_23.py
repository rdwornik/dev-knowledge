from copy import deepcopy
from datetime import date
from pathlib import Path
import sys

import pytest
import yaml
from pydantic import ValidationError


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ecosystem.schema.provider_registry import (  # noqa: E402
    ProviderRegistry,
    Role,
    ReservedShare,
    FallbackTrigger,
    fallback_due,
    elapsed_week_pct,
    ROLE_NAMES,
)


REGISTRY_PATH = ROOT / "ecosystem" / "provider-registry.yaml"
DECISION_DATE = date(2026, 10, 23)


@pytest.fixture
def registry_data():
    with REGISTRY_PATH.open(encoding="utf-8") as registry_file:
        return yaml.safe_load(registry_file)


def validate(data):
    return ProviderRegistry.model_validate(data)


def assert_operator_decision(admission):
    assert admission.decided_by == "operator"
    assert admission.decided_on == DECISION_DATE
    assert admission.evidence.strip()


def test_registry_schema_accepts_new_fields(registry_data):
    registry = validate(registry_data)

    assert isinstance(registry.roles["seat-integrator"], Role)
    assert isinstance(registry.roles["orchestrate"].reserved_share, ReservedShare)
    assert isinstance(next(iter(registry.fallback_triggers.values())), FallbackTrigger)
    assert {"seat-dispatcher", "execute", "rulings"} <= set(ROLE_NAMES)


def test_integrator_pin_is_enforced_by_registry_data(registry_data):
    registry = validate(registry_data)
    integrator = registry.roles["seat-integrator"]

    assert integrator.order[0].model == "claude-sonnet-5-5"
    assert integrator.pinned_model == "claude-sonnet-5-5"
    assert len(integrator.order) == 1
    assert_operator_decision(integrator.order[0].admission)
    assert "claude-opus-5-5" in integrator.order[0].note

    changed_model = deepcopy(registry_data)
    changed_model["roles"]["seat-integrator"]["order"][0]["model"] = "claude-opus-5-5"
    assert "claude-opus-5-5" in changed_model["models"]
    with pytest.raises(ValidationError):
        validate(changed_model)

    without_pin = deepcopy(changed_model)
    without_pin["roles"]["seat-integrator"].pop("pinned_model")
    validate(without_pin)


def test_dispatcher_and_lane_head_are_distinct_registry_rows(registry_data):
    registry = validate(registry_data)
    dispatcher = registry.roles["seat-dispatcher"]

    assert len(dispatcher.order) == 1
    assert dispatcher.order[0].provider == "anthropic"
    assert dispatcher.order[0].model == "claude-opus-5-5"
    assert dispatcher.no_fallback is True
    assert_operator_decision(dispatcher.order[0].admission)
    assert registry.roles["seat-orchestrator"].order[0].model == "claude-sonnet-5-5"


@pytest.mark.parametrize("role_name", ["orchestrate", "plan"])
def test_orchestration_roles_pin_opus_without_fallback(registry_data, role_name):
    registry = validate(registry_data)
    role = registry.roles[role_name]

    assert role.no_fallback is True
    assert role.order[0].model == "claude-opus-5-5"
    assert role.reserved_share is not None
    assert "opus" in role.reserved_share.pool.lower()
    assert role.reserved_share.value is None
    assert role.reserved_share.reason.strip()


def test_rulings_execute_and_review_routes(registry_data):
    registry = validate(registry_data)

    assert registry.roles["rulings"].order[0].model == "claude-fable-5-1"
    assert [
        (entry.provider, entry.model)
        for entry in registry.roles["execute"].order
    ] == [("anthropic", "claude-sonnet-5-5"), ("xai", "grok-4.7")]

    review_order = registry.roles["review"].order
    assert review_order[0].provider == "openai"
    assert any(entry.provider == "xai" for entry in review_order[1:])


def test_test_writer_uses_a_different_model_family_than_coder(registry_data):
    registry = validate(registry_data)
    test_writer = registry.roles["red"]
    coder = registry.roles["implement"]

    assert test_writer.distinct_family_from == "implement"
    test_family = registry.models[test_writer.order[0].model].family
    coder_family = registry.models[coder.order[0].model].family
    assert test_family
    assert coder_family
    assert test_family != coder_family


def test_fallback_trigger_routes_execute_and_review_to_xai(registry_data):
    registry = validate(registry_data)
    matching = [
        trigger
        for trigger in registry.fallback_triggers.values()
        if {"execute", "review"} <= set(trigger.roles)
    ]

    assert len(matching) == 1
    trigger = matching[0]
    assert trigger.to_provider == "xai"
    assert trigger.to_model == "grok-4.7"
    assert trigger.override_flag
    assert trigger.signals
    assert all(signal["status"] in {"AVAILABLE", "GAP"} for signal in trigger.signals.values())


def test_no_fallback_rejects_multiple_order_entries(registry_data):
    data = deepcopy(registry_data)
    execute = data["roles"]["execute"]
    execute["no_fallback"] = True
    execute["order"].append(deepcopy(execute["order"][0]))

    with pytest.raises(ValidationError):
        validate(data)


def test_reserved_share_requires_a_reason_when_value_is_unset(registry_data):
    data = deepcopy(registry_data)
    data["roles"]["orchestrate"]["reserved_share"]["value"] = None
    data["roles"]["orchestrate"]["reserved_share"]["reason"] = "   "

    with pytest.raises(ValidationError):
        validate(data)


def test_distinct_family_constraint_rejects_matching_families(registry_data):
    data = deepcopy(registry_data)
    red_model = data["roles"]["red"]["order"][0]["model"]
    coder_model = data["roles"]["implement"]["order"][0]["model"]
    data["models"][red_model]["family"] = data["models"][coder_model]["family"]

    with pytest.raises(ValidationError):
        validate(data)


def test_fallback_trigger_rejects_unknown_role(registry_data):
    data = deepcopy(registry_data)
    trigger = next(iter(data["fallback_triggers"].values()))
    trigger["roles"].append("unknown-role")

    with pytest.raises(ValidationError):
        validate(data)


def test_fallback_due_uses_a_strict_usage_boundary():
    assert fallback_due(60.01, 60.0) is True
    assert fallback_due(60.0, 60.0) is False
    assert fallback_due(59.99, 60.0) is False


def test_fallback_due_override_and_missing_percentages():
    assert fallback_due(20.0, 50.0, override=True) is True
    assert fallback_due(None, 50.0) is False
    assert fallback_due(50.0, None) is False
    assert fallback_due(None, None) is False
    assert fallback_due(None, None, override=True) is True


def test_elapsed_week_percentage_and_clamping():
    seconds_per_week = 7 * 24 * 60 * 60
    start = 1_000_000.0
    reset = start + seconds_per_week

    assert elapsed_week_pct(start, reset) == pytest.approx(0.0)
    assert elapsed_week_pct(start + seconds_per_week / 2, reset) == pytest.approx(50.0)
    assert elapsed_week_pct(reset, reset) == pytest.approx(100.0)
    assert elapsed_week_pct(start - 1, reset) == pytest.approx(0.0)
    assert elapsed_week_pct(reset + 1, reset) == pytest.approx(100.0)
