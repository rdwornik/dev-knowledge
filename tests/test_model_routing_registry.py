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


def test_implement_is_copilot_first_and_sonnet_is_vendor_fail_only(live):
    order = ProviderRegistry.model_validate(live).roles["implement"].order
    assert order[0].provider == "copilot-enterprise", (
        "implement.order[0] must be Copilot (served model read from the CLI usage file); "
        f"got {order[0].provider}")
    sonnet = [e for e in order if e.model == SONNET]
    assert len(sonnet) == 1
    assert getattr(sonnet[0], "vendor_fail_only", False) is True, (
        "the Claude implement entry must carry `vendor_fail_only: true`")
    assert order[1].model == SONNET and order[2].model == "grok-4.7"


def test_seat_roles_and_opus_only_roles(live):
    roles = ProviderRegistry.model_validate(live).roles
    assert {"seat-orchestrator", "seat-integrator"} <= set(roles), "seat roles missing from the registry"
    assert [(e.provider, e.model) for e in roles["seat-orchestrator"].order] == [("anthropic", SONNET)]
    assert [(e.provider, e.model) for e in roles["seat-integrator"].order] == [("anthropic", OPUS)]
    for name in ("orchestrate", "plan"):
        assert roles[name].rerankable is False
        assert [e.model for e in roles[name].order] == [OPUS]


def test_schema_refuses_a_claude_model_as_the_first_implement_entry(live):
    def mutate(d):
        order = d["roles"]["implement"]["order"]
        claude = next(e for e in order if e.get("model") == SONNET)
        rest = [e for e in order if e is not claude]
        d["roles"]["implement"]["order"] = [claude, *rest]

    _refuses(_mutated(live, mutate))


def test_schema_refuses_an_anthropic_implement_entry_without_vendor_fail_only(live):
    def mutate(d):
        for e in d["roles"]["implement"]["order"]:
            if e["provider"] == "anthropic":
                e.pop("vendor_fail_only", None)

    _refuses(_mutated(live, mutate))


def test_the_checker_reports_a_claude_implement_without_the_vendor_fail_clause(live, monkeypatch):
    def mutate(d):
        for e in d["roles"]["implement"]["order"]:
            if e["provider"] == "anthropic":
                e["vendor_fail_only"] = False
        order = d["roles"]["implement"]["order"]
        claude = next(e for e in order if e["provider"] == "anthropic")
        d["roles"]["implement"]["order"] = [claude, *[e for e in order if e is not claude]]

    bad = _mutated(live, mutate)
    # the schema would refuse this file at load time; hand the checker the raw mapping so the
    # checker's own seam-level report (a returned string) is what is under test
    monkeypatch.setattr(cpr._preg, "load_registry", lambda path=None: bad)
    findings = cpr.run(_ROOT)
    assert any("implement" in f and ("VENDOR-FAIL" in f or "vendor" in f.lower()) for f in findings), (
        f"run() must return a problem string for a Claude implement without the vendor-fail clause; "
        f"got {findings}")
