"""RED witnesses for the e2-model-routing registry role table.

`implement` becomes Copilot-first, Claude Sonnet 5.5 is usable only after a recorded
`VENDOR-FAIL: implement ...` (`vendor_fail_only: true`), and two seat roles are added.
The registry is the one source: the schema and the checker both refuse a Claude implementer
that is not a vendor-fail fallback.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import yaml

_ROOT = Path(__file__).resolve().parent.parent
for _p in (_ROOT, _ROOT / "scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from ecosystem.schema.provider_registry import ProviderRegistry  # noqa: E402

import check_provider_registry as cpr  # noqa: E402

_REGISTRY_PATH = _ROOT / "ecosystem" / "provider-registry.yaml"
SONNET = "claude-sonnet-5-5"
OPUS = "claude-opus-5-5"


@pytest.fixture(scope="module")
def live() -> dict:
    return yaml.safe_load(_REGISTRY_PATH.read_text(encoding="utf-8"))


def _mutated(live: dict, mutate) -> dict:
    data = copy.deepcopy(live)
    mutate(data)
    return data


def _refuses(data: dict) -> None:
    with pytest.raises(Exception) as exc:
        ProviderRegistry.model_validate(data)
    assert type(exc.value).__name__ == "ValidationError", repr(exc.value)


def test_the_live_registry_validates(live):
    ProviderRegistry.model_validate(live)


def test_implement_is_sonnet_first_and_copilot_is_second(live):
    order = ProviderRegistry.model_validate(live).roles["implement"].order
    # GO-E3.0 R11: admitted Sonnet 5.5 is the first implement entry.
    assert (order[0].provider, order[0].model) == ("anthropic", SONNET)
    sonnet = [e for e in order if e.model == SONNET]
    assert len(sonnet) == 1
    # GO-E3.0 R11: first-entry Sonnet no longer carries vendor_fail_only.
    assert getattr(sonnet[0], "vendor_fail_only", False) is False
    # GO-E3.0 R11: Copilot is second and Grok remains third.
    assert order[1].provider == "copilot-enterprise" and order[2].model == "grok-4.7"


def test_seat_roles_and_opus_only_roles(live):
    roles = ProviderRegistry.model_validate(live).roles
    assert {"seat-orchestrator", "seat-integrator"} <= set(roles), "seat roles missing from the registry"
    assert [(e.provider, e.model) for e in roles["seat-orchestrator"].order] == [("anthropic", SONNET)]
    assert [(e.provider, e.model) for e in roles["seat-integrator"].order] == [("anthropic", SONNET)]  # D2 amended 2026-10-23
    assert [(e.provider, e.model) for e in roles["seat-dispatcher"].order] == [("anthropic", OPUS)]  # D9
    for name in ("orchestrate", "plan"):
        assert roles[name].rerankable is False
        assert [e.model for e in roles[name].order] == [OPUS]


def test_schema_accepts_admitted_claude_as_the_first_implement_entry(live):
    def mutate(d):
        order = d["roles"]["implement"]["order"]
        claude = next(e for e in order if e.get("model") == SONNET)
        rest = [e for e in order if e is not claude]
        d["roles"]["implement"]["order"] = [claude, *rest]

    # GO-E3.0 R11: admission, not provider identity, governs the first implement entry.
    assert ProviderRegistry.model_validate(_mutated(live, mutate)).roles["implement"].order[0].provider == "anthropic"


def test_schema_refuses_an_anthropic_implement_entry_without_vendor_fail_only(live):
    def mutate(d):
        order = d["roles"]["implement"]["order"]
        sonnet = next(e for e in order if e["provider"] == "anthropic")
        copilot = next(e for e in order if e["provider"] == "copilot-enterprise")
        # GO-E3.0 R11: only a later Anthropic implement entry requires vendor_fail_only.
        sonnet.pop("vendor_fail_only", None)
        d["roles"]["implement"]["order"] = [copilot, sonnet, *[
            e for e in order if e not in (copilot, sonnet)
        ]]

    _refuses(_mutated(live, mutate))


def _put_first(d: dict, provider: str) -> None:
    order = d["roles"]["implement"]["order"]
    if provider == "openai":
        entry = {"provider": "openai", "model": "gpt-5.6-terra"}
    else:
        entry = next(e for e in order if e["provider"] == provider)
    d["roles"]["implement"]["order"] = [entry, *[e for e in order if e is not entry]]


@pytest.mark.parametrize("provider", ["xai", "openai"])
def test_schema_refuses_a_non_copilot_first_implement_entry(live, provider):
    data = _mutated(live, lambda d: _put_first(d, provider))
    _refuses(data)


@pytest.mark.parametrize("provider", ["xai", "openai"])
def test_the_checker_reports_a_non_admitted_first_implement_entry(live, monkeypatch, provider):
    bad = _mutated(live, lambda d: _put_first(d, provider))
    monkeypatch.setattr(cpr._preg, "load_registry", lambda path=None: bad)
    findings = cpr.check_implement_vendor_fail(_ROOT)
    # GO-E3.0 R11: the checker requires an admitted first entry, not Copilot specifically.
    assert any("implement" in f and "admitted" in f for f in findings), findings


def test_the_checker_is_clean_on_the_live_registry():
    assert cpr.check_implement_vendor_fail(_ROOT) == []


def test_schema_refuses_vendor_fail_only_on_the_first_entry_of_a_role(live):
    def mutate(d):
        d["roles"]["read"]["order"][0]["vendor_fail_only"] = True

    _refuses(_mutated(live, mutate))


def test_the_checker_reports_vendor_fail_only_on_a_first_entry(live, monkeypatch):
    def mutate(d):
        d["roles"]["implement"]["order"][0]["vendor_fail_only"] = True

    bad = _mutated(live, mutate)
    monkeypatch.setattr(cpr._preg, "load_registry", lambda path=None: bad)
    assert any("vendor_fail_only" in f for f in cpr.check_implement_vendor_fail(_ROOT))


def test_the_checker_reports_a_claude_implement_without_the_vendor_fail_clause(live, monkeypatch):
    def mutate(d):
        order = d["roles"]["implement"]["order"]
        claude = next(e for e in order if e["provider"] == "anthropic")
        copilot = next(e for e in order if e["provider"] == "copilot-enterprise")
        # GO-E3.0 R11: test missing vendor_fail_only only for Anthropic after the first entry.
        claude["vendor_fail_only"] = False
        d["roles"]["implement"]["order"] = [copilot, claude, *[
            e for e in order if e not in (copilot, claude)
        ]]

    bad = _mutated(live, mutate)
    # the schema would refuse this file at load time; hand the checker the raw mapping so the
    # checker's own seam-level report (a returned string) is what is under test
    monkeypatch.setattr(cpr._preg, "load_registry", lambda path=None: bad)
    findings = cpr.run(_ROOT)
    assert any("implement" in f and ("VENDOR-FAIL" in f or "vendor" in f.lower()) for f in findings), (
        f"run() must return a problem string for a Claude implement without the vendor-fail clause; "
        f"got {findings}")
