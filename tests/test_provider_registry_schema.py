"""`ecosystem/schema/provider_registry.py` — the declared contract for the provider registry.

Every rule below is asserted by MUTATION: a legal registry is built, one field is broken, and
the schema is required to refuse it. A schema test that only proves the live file passes is
vacuous — it would still pass if every validator were deleted.

Sibling of `tests/test_desired_state_schema.py`, and it opens the same way: the import is
inside the test so a collection error cannot take the whole suite with it.
"""

from __future__ import annotations

import copy

import pytest

pydantic = pytest.importorskip("pydantic")
ValidationError = pydantic.ValidationError


def _schema():
    from ecosystem.schema import provider_registry as s

    return s


#: A minimal registry that is legal under every rule. Each test deep-copies it and breaks
#: exactly one thing, so a failure names the rule that fired rather than a fixture drift.
_LEGAL = {
    "providers": {
        "acme": {
            "display_name": "Acme",
            "council_alias": "acme",
            "cli": "acmecli",
            "version_command": ["acmecli", "--version"],
            "changelog_tool_key": "acme-cli",
            "changelog_source_url": "https://example.invalid/acme",
        },
        "nocli": {"display_name": "NoCLI", "council_alias": "nocli"},
    },
    "models": {
        "acme-1": {
            "provider": "acme",
            "tier": "M",
            "roles": ["reviewer"],
            "pinned_at": [{"path": "pyproject.toml", "seam": "S30", "format": "comment"}],
        },
    },
}


def _mutate():
    """A fresh deep copy of `_LEGAL`, for a test to break in exactly one place."""
    return copy.deepcopy(_LEGAL)


def _validate(data):
    return _schema().ProviderRegistry.model_validate(data)


# --- the baseline: the fixture and the live file both pass ---------------------------------

def test_the_legal_fixture_validates():
    assert _validate(_mutate()) is not None


@pytest.mark.live_repo
def test_the_live_registry_validates_against_its_declared_schema():
    from scripts import provider_registry as preg

    # load_registry() validates internally; reaching this line without RegistryError is the
    # assertion. Re-validating explicitly documents which contract was applied.
    _validate(preg.load_registry())


# --- extra="forbid": a typo is a spec error, not inert data --------------------------------

def test_an_unknown_provider_key_is_refused():
    d = _mutate()
    d["providers"]["acme"]["clii"] = "acmecli"
    with pytest.raises(ValidationError, match="clii"):
        _validate(d)


def test_an_unknown_model_key_is_refused():
    d = _mutate()
    d["models"]["acme-1"]["role"] = "reviewer"          # singular typo for `roles`
    with pytest.raises(ValidationError, match="role"):
        _validate(d)


# --- cli <-> version_command coherence -----------------------------------------------------

def test_a_cli_with_no_version_command_is_refused():
    d = _mutate()
    d["providers"]["acme"]["version_command"] = None
    with pytest.raises(ValidationError, match="present or absent together"):
        _validate(d)


def test_a_version_command_with_no_cli_is_refused():
    """The exact shape the pre-schema test fixture carried — a probe with nothing to probe."""
    d = _mutate()
    d["providers"]["acme"]["cli"] = None
    with pytest.raises(ValidationError, match="present or absent together"):
        _validate(d)


def test_a_version_command_that_runs_a_different_binary_is_refused():
    d = _mutate()
    d["providers"]["acme"]["version_command"] = ["someothercli", "--version"]
    with pytest.raises(ValidationError, match="must exercise the CLI this provider declares"):
        _validate(d)


def test_an_empty_version_command_is_refused():
    d = _mutate()
    d["providers"]["acme"]["version_command"] = []
    with pytest.raises(ValidationError, match="must name the binary"):
        _validate(d)


# --- the S8 identity pair ------------------------------------------------------------------

def test_a_changelog_tool_key_without_its_source_url_is_refused():
    d = _mutate()
    d["providers"]["acme"]["changelog_source_url"] = None
    with pytest.raises(ValidationError, match="present or absent together"):
        _validate(d)


def test_a_changelog_source_url_without_its_tool_key_is_refused():
    d = _mutate()
    d["providers"]["acme"]["changelog_tool_key"] = None
    with pytest.raises(ValidationError, match="present or absent together"):
        _validate(d)


# --- cross-collection invariants -----------------------------------------------------------

def test_a_model_naming_an_undeclared_provider_is_refused():
    d = _mutate()
    d["models"]["acme-1"]["provider"] = "ghost"
    with pytest.raises(ValidationError, match="undeclared provider"):
        _validate(d)


def test_two_providers_claiming_one_council_alias_is_refused():
    d = _mutate()
    d["providers"]["nocli"]["council_alias"] = "acme"
    with pytest.raises(ValidationError, match="claimed by both"):
        _validate(d)


def test_a_provider_the_council_does_not_panel_may_omit_its_alias():
    d = _mutate()
    d["providers"]["nocli"].pop("council_alias")
    assert _validate(d) is not None


# --- THE SEPARATION: configuration is not gated on admission -------------------------------

def test_a_model_with_no_admission_record_at_all_is_fully_valid():
    """The positive half of the rule, and the one worth pinning.

    Nothing in this schema can make a row's EXISTENCE conditional on a verdict. If a future
    edit made `role_admission` required, this test is what fails.
    """
    d = _mutate()
    assert "role_admission" not in d["models"]["acme-1"]
    assert _validate(d) is not None


def test_a_refused_model_is_still_a_valid_configured_row():
    d = _mutate()
    d["models"]["acme-1"]["roles"] = []
    d["models"]["acme-1"]["role_admission"] = {
        "fan-out": {
            "verdict": "refused",
            "decided_by": "architect",
            "decided_on": "2026-08-23",
            "floors": ["G1"],
            "evidence": "docs/audits/x.md",
        }
    }
    assert _validate(d) is not None


def test_a_refused_role_may_not_also_be_a_held_role():
    """The negative half: admission governs role eligibility, so the two cannot disagree."""
    d = _mutate()
    d["models"]["acme-1"]["role_admission"] = {
        "reviewer": {
            "verdict": "refused",
            "decided_by": "architect",
            "decided_on": "2026-08-23",
            "evidence": "docs/audits/x.md",
        }
    }
    with pytest.raises(ValidationError, match="cannot be a held one"):
        _validate(d)


def test_an_admitted_role_may_be_a_held_role():
    d = _mutate()
    d["models"]["acme-1"]["role_admission"] = {
        "reviewer": {
            "verdict": "admitted",
            "decided_by": "architect",
            "decided_on": "2026-08-23",
            "evidence": "docs/audits/x.md",
        }
    }
    assert _validate(d) is not None


# --- a verdict carries its provenance ------------------------------------------------------

@pytest.mark.parametrize("dropped", ["decided_by", "decided_on", "evidence"])
def test_a_decided_verdict_missing_any_provenance_field_is_refused(dropped):
    d = _mutate()
    record = {
        "verdict": "refused",
        "decided_by": "architect",
        "decided_on": "2026-08-23",
        "evidence": "docs/audits/x.md",
    }
    record.pop(dropped)
    d["models"]["acme-1"]["roles"] = []
    d["models"]["acme-1"]["role_admission"] = {"fan-out": record}
    with pytest.raises(ValidationError, match=dropped):
        _validate(d)


def test_unevaluated_needs_no_provenance_because_nobody_decided_anything():
    d = _mutate()
    d["models"]["acme-1"]["roles"] = []
    d["models"]["acme-1"]["role_admission"] = {"fan-out": {"verdict": "unevaluated"}}
    assert _validate(d) is not None


def test_a_verdict_outside_the_closed_vocabulary_is_refused():
    d = _mutate()
    d["models"]["acme-1"]["roles"] = []
    d["models"]["acme-1"]["role_admission"] = {"fan-out": {"verdict": "probably-fine"}}
    with pytest.raises(ValidationError, match="verdict"):
        _validate(d)
