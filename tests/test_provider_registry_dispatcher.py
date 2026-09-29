"""tests/test_provider_registry_dispatcher.py — R22: the dispatcher's model is registered.

R22 (`to-browser/RATIFICATION-2026-09-25-v14-superseded.md`): "The order is binding: the
dispatcher runs on the Sonnet 5 id ... the registry row for the dispatcher role is changed to
the Sonnet 5 id in the next batch so the two sources agree again." Until this module the
registry named no dispatcher at all — `ecosystem/provider-registry.yaml`'s own comment recorded
"today no role names the dispatcher" — so a session reading the registry alone could not tell
R22 had ever been ratified. RED-first: this module fails against a registry that carries no
`dispatcher:` row, or one shaped wrong, and only a correctly-provenanced row makes it pass.

NOT a `roles:` entry. AX21-1's six-role vocabulary (`ecosystem.schema.provider_registry.
ROLE_NAMES`) answers "who produces/reviews/reads/etc", a different question from "what model
does the dispatcher session itself run on" — the dispatcher's own logic is code, and R22 is an
explicit `OVERRIDE` against `roles.orchestrate` (Opus-only, not rerankable), not a repoint of it.
"""
from __future__ import annotations

import copy

import pytest

pydantic = pytest.importorskip("pydantic")


def _schema():
    from ecosystem.schema import provider_registry as s

    return s


def test_the_live_registry_names_the_dispatchers_model():
    """`ecosystem/provider-registry.yaml` carries a `dispatcher:` row naming a versioned id."""
    from scripts import provider_registry as preg

    data = preg.load_registry()
    dispatcher = data.get("dispatcher")
    assert dispatcher is not None, (
        "the registry names no dispatcher — R22 (\"the order is binding: the dispatcher runs "
        "on the Sonnet 5 id\") is ratified but not reflected in ecosystem/provider-registry.yaml"
    )
    assert dispatcher["provider"] == "anthropic"
    assert dispatcher["model"] == "claude-sonnet-5"


def test_the_dispatcher_model_is_a_versioned_id_not_a_bare_alias():
    """A bare CLI alias (`sonnet`, `opus`) silently repoints when the CLI's own default moves —
    the exact drift `roles.orchestrate`'s comment names as the reason every `order[].model` in
    this file is a versioned id. The dispatcher row is held to the same discipline.
    """
    from scripts import provider_registry as preg

    dispatcher = preg.load_registry().get("dispatcher") or {}
    model = dispatcher.get("model", "")
    assert model in preg.model_ids(), (
        f"dispatcher.model {model!r} is not a registered model id in `models:` — a bare alias "
        f"is not addressable, resolvable or checkable the way a versioned id is"
    )


def test_the_schema_accepts_the_live_dispatcher_shape():
    """The live file's `dispatcher:` row validates, and round-trips onto a typed attribute —
    proof the schema's `dispatcher` field is wired, not merely tolerated by `extra` handling.
    """
    from scripts import provider_registry as preg

    data = copy.deepcopy(preg.load_registry())
    registry = _schema().ProviderRegistry.model_validate(data)
    assert registry.dispatcher is not None
    assert registry.dispatcher.model == "claude-sonnet-5"
    assert registry.dispatcher.provider == "anthropic"


def test_a_dispatcher_pin_naming_an_undeclared_provider_is_refused():
    from scripts import provider_registry as preg

    data = copy.deepcopy(preg.load_registry())
    data["dispatcher"] = {
        "provider": "not-a-real-provider",
        "model": "claude-sonnet-5",
        "decided_by": "operator",
        "decided_on": "2026-09-25",
        "evidence": "protocols/STANDING_RULINGS.md",
    }
    with pytest.raises(pydantic.ValidationError):
        _schema().ProviderRegistry.model_validate(data)


def test_a_dispatcher_pin_naming_a_model_of_a_different_provider_is_refused():
    from scripts import provider_registry as preg

    data = copy.deepcopy(preg.load_registry())
    data["dispatcher"] = {
        "provider": "openai",
        "model": "claude-sonnet-5",
        "decided_by": "operator",
        "decided_on": "2026-09-25",
        "evidence": "protocols/STANDING_RULINGS.md",
    }
    with pytest.raises(pydantic.ValidationError):
        _schema().ProviderRegistry.model_validate(data)


def test_a_dispatcher_pin_without_provenance_is_refused():
    """Same principle as `RoleAdmission`: a pin with no decider, date and evidence is an
    assertion, not a record.
    """
    from scripts import provider_registry as preg

    data = copy.deepcopy(preg.load_registry())
    data["dispatcher"] = {"provider": "anthropic", "model": "claude-sonnet-5"}
    with pytest.raises(pydantic.ValidationError):
        _schema().ProviderRegistry.model_validate(data)


def test_a_dispatcher_pin_with_an_absolute_evidence_path_is_refused():
    from scripts import provider_registry as preg

    data = copy.deepcopy(preg.load_registry())
    data["dispatcher"] = {
        "provider": "anthropic",
        "model": "claude-sonnet-5",
        "decided_by": "operator",
        "decided_on": "2026-09-25",
        "evidence": "/etc/passwd",
    }
    with pytest.raises(pydantic.ValidationError):
        _schema().ProviderRegistry.model_validate(data)
