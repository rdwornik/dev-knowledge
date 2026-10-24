from datetime import date
from pathlib import Path
import importlib.util
import sys

import pytest
import yaml


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ecosystem.schema.provider_registry import ProviderRegistry  # noqa: E402


REGISTRY_PATH = ROOT / "ecosystem" / "provider-registry.yaml"
DECISION_DATE = date(2026, 10, 24)


@pytest.fixture
def registry_data():
    with REGISTRY_PATH.open(encoding="utf-8") as registry_file:
        return yaml.safe_load(registry_file)


@pytest.fixture
def registry(registry_data):
    return ProviderRegistry.model_validate(registry_data)


def _load_router():
    spec = importlib.util.spec_from_file_location(
        "provider_router", ROOT / "scripts" / "provider_router.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["provider_router"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def router():
    return _load_router()


def assert_repo_evidence(evidence):
    evidence_path = Path(evidence)
    assert not evidence_path.is_absolute()
    assert ".." not in evidence_path.parts
    assert (ROOT / evidence_path).is_file()


@pytest.mark.parametrize("role_name", ["orchestrate", "plan"])
def test_reserved_share_is_operator_ruled_and_note_updated(registry, role_name):
    role = registry.roles[role_name]
    share = role.reserved_share

    assert share.pool == "anthropic-weekly-opus"
    assert share.value == 0.30
    assert 0 < share.value <= 1
    assert share.decided_by == "operator"
    assert share.decided_on == DECISION_DATE
    reason = share.reason
    assert "30%" in reason
    assert "weekly Anthropic budget" in reason
    assert "batch close" in reason
    assert "quota_watch" in reason
    assert "a number is not invented" not in reason.lower()
    assert_repo_evidence(share.evidence)

    assert len(role.order) == 1
    note = " ".join(role.order[0].note.split())
    assert "(value unset)" not in note


def test_execute_grok_admission_is_operator_ruled(registry):
    execute = registry.roles["execute"]
    grok = next(
        entry for entry in execute.order
        if entry.provider == "xai" and entry.model == "grok-4.7"
    )

    assert grok.admission.verdict == "admitted"
    assert grok.admission.decided_by == "operator"
    assert grok.admission.decided_on == DECISION_DATE
    assert_repo_evidence(grok.admission.evidence)
    assert "NOT ADMITTED" not in grok.note.upper()


def test_execute_routes_grok_after_admission(router):
    got = router.route("execute", repo=".dev-knowledge")
    assert [candidate.provider for candidate in got] == ["anthropic", "xai"]

    verdicts = {verdict.provider: verdict
                for verdict in router.explain("execute", repo=".dev-knowledge")}
    assert verdicts["xai"].refusal is None


def test_grok_admission_remains_role_scoped(registry):
    xai_admitted_roles = {
        role_name
        for role_name, role in registry.roles.items()
        for entry in role.order
        if entry.provider == "xai" and entry.admission.verdict == "admitted"
    }
    assert xai_admitted_roles == {"review", "execute"}

    admitted_providers = {
        entry.provider
        for role in registry.roles.values()
        for entry in role.order
        if entry.admission.verdict == "admitted"
    }
    assert admitted_providers == {"anthropic", "copilot-enterprise", "xai"}
    assert registry.providers["xai"].licence.decided_on == date(2026, 8, 26)


def test_bprime_trigger_still_covers_execute_and_review(registry):
    trigger = registry.fallback_triggers["bprime"]
    assert {"execute", "review"} <= set(trigger.roles)
    assert trigger.to_model == "grok-4.7"
