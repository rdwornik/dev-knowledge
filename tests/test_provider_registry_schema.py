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


@pytest.mark.parametrize("field", ["display_name", "cli", "council_alias",
                                   "changelog_tool_key", "changelog_source_url"])
@pytest.mark.parametrize("bad", ["", "   "])
def test_a_blank_string_field_is_refused(field, bad):
    """terra CRITICAL round 6: `changelog_tool_key: ""` paired with `changelog_source_url: ""`
    satisfied the both-or-neither rule, then every consumer's `if key and url` guard dropped
    that provider from the sentinel probe and the S8 comparison — silently, both ways."""
    d = _mutate()
    d["providers"]["acme"][field] = bad
    with pytest.raises(ValidationError, match="blank"):
        _validate(d)


@pytest.mark.parametrize("bad", [" codex", "codex ", "\tcodex"])
def test_an_untrimmed_string_field_is_refused(bad):
    d = _mutate()
    d["providers"]["acme"]["changelog_tool_key"] = bad
    with pytest.raises(ValidationError, match="whitespace"):
        _validate(d)


@pytest.mark.parametrize("variant", ["ACME-CLI", "Acme-Cli"])
def test_a_case_variant_changelog_key_never_reaches_the_uniqueness_check(variant):
    """terra HIGH round 6 asked for casefolded uniqueness so `codex`/`CODEX` could not both
    validate. Round 8's lowercase requirement is STRONGER and fires first, so the case variant
    is refused before uniqueness is consulted — asserted on the message that actually raises,
    because a test claiming the wrong rule fired is a test that would survive that rule's
    removal."""
    d = _mutate()
    d["providers"]["nocli"].update({
        "changelog_tool_key": variant,
        "changelog_source_url": "https://example.invalid/other",
    })
    with pytest.raises(ValidationError, match="lookup key"):
        _validate(d)


def test_a_case_variant_council_alias_never_reaches_the_uniqueness_check():
    d = _mutate()
    d["providers"]["nocli"]["council_alias"] = "ACME"
    with pytest.raises(ValidationError, match="lookup key"):
        _validate(d)


def test_two_providers_claiming_one_council_alias_is_refused_exactly():
    """The uniqueness rule itself, exercised with two LOWERCASE aliases so it is the rule
    under test rather than the casing rule."""
    d = _mutate()
    d["providers"]["nocli"]["council_alias"] = "acme"
    with pytest.raises(ValidationError, match="claimed by both"):
        _validate(d)


def test_two_providers_claiming_one_changelog_tool_key_is_refused():
    """terra HIGH round 5: a repeat silently drops one provider's probe, because both
    `version_commands()` and `changelog_source_urls()` key a dict on it."""
    d = _mutate()
    d["providers"]["nocli"].update({
        "changelog_tool_key": "acme-cli",
        "changelog_source_url": "https://example.invalid/other",
    })
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


@pytest.mark.parametrize("collection,key", [
    ("providers", " acme "), ("providers", "  "), ("models", " acme-1 "), ("models", ""),
])
def test_a_blank_or_padded_mapping_key_is_refused(collection, key):
    """terra HIGH round 7: mapping KEYS are identifiers too, and the round-6 validator saw
    only field values."""
    d = _mutate()
    original = next(iter(d[collection]))
    d[collection][key] = d[collection].pop(original)
    if collection == "providers":
        d["models"]["acme-1"]["provider"] = key
    with pytest.raises(ValidationError, match="blank|whitespace"):
        _validate(d)


def test_a_padded_admission_key_cannot_hide_a_refused_role():
    """The invariant the padded key defeated: `" fan-out "` refused, `fan-out` still held."""
    d = _mutate()
    d["models"]["acme-1"]["roles"] = ["fan-out"]
    d["models"]["acme-1"]["role_admission"] = {
        " fan-out ": {"verdict": "refused", "decided_by": "architect",
                      "decided_on": "2026-08-23", "evidence": "docs/audits/x.md"},
    }
    with pytest.raises(ValidationError, match="whitespace"):
        _validate(d)


@pytest.mark.parametrize("field,value", [
    ("council_alias", "Acme"), ("changelog_tool_key", "ACME-CLI"),
])
def test_a_non_lowercase_provider_lookup_key_is_refused(field, value):
    """terra MEDIUM round 8: rounds 6-7 compared these casefolded for collisions while every
    consumer looks them up RAW (`council_aliases()` keyed by the literal, the sentinel's
    `tool-versions.yaml` lookup), so `Claude` would validate, collide correctly, and resolve
    nowhere. Requiring lowercase replaced that casefolding; the comparisons are now exact."""
    d = _mutate()
    d["providers"]["acme"][field] = value
    with pytest.raises(ValidationError, match="lookup key"):
        _validate(d)


def test_a_non_lowercase_role_name_is_refused():
    """`_sole_role_model("subagent-default")` is an exact-match lookup."""
    d = _mutate()
    d["models"]["acme-1"]["roles"] = ["Reviewer"]
    with pytest.raises(ValidationError, match="lookup key"):
        _validate(d)


def test_a_non_lowercase_admission_role_key_is_refused():
    d = _mutate()
    d["models"]["acme-1"]["roles"] = []
    d["models"]["acme-1"]["role_admission"] = {
        "Fan-Out": {"verdict": "unevaluated"},
    }
    with pytest.raises(ValidationError, match="lookup key"):
        _validate(d)


def test_display_name_and_attribution_token_keep_their_real_casing():
    """The scope boundary: `OpenAI`, `xAI` and `grok L5` are values, not lookup keys."""
    d = _mutate()
    d["providers"]["acme"]["display_name"] = "AcmeAI"
    d["models"]["acme-1"]["attribution_token"] = "Acme L5"
    assert _validate(d) is not None


def test_a_case_variant_admission_key_cannot_hide_a_refused_role():
    """Same supersession as the two above: round 6/7 casefolded the intersection, round 8's
    lowercase rule refuses the variant outright and is what raises."""
    d = _mutate()
    d["models"]["acme-1"]["roles"] = ["fan-out"]
    d["models"]["acme-1"]["role_admission"] = {
        "Fan-Out": {"verdict": "refused", "decided_by": "architect",
                    "decided_on": "2026-08-23", "evidence": "docs/audits/x.md"},
    }
    with pytest.raises(ValidationError, match="lookup key"):
        _validate(d)


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


@pytest.mark.parametrize("blank", ["", "   ", "\t"])
def test_a_blank_provenance_string_counts_as_missing_not_as_present(blank):
    """terra HIGH, 2026-08-23: `is None` alone let `evidence: ""` satisfy the rule and then
    skip the checker's existence test — a verdict with provenance-shaped nothing behind it."""
    d = _mutate()
    d["models"]["acme-1"]["roles"] = []
    d["models"]["acme-1"]["role_admission"] = {
        "fan-out": {
            "verdict": "refused",
            "decided_by": "architect",
            "decided_on": "2026-08-23",
            "evidence": blank,
        }
    }
    with pytest.raises(ValidationError, match="evidence"):
        _validate(d)


@pytest.mark.parametrize("bad", ["/etc/passwd", "../outside/artifact.md",
                                 "docs/../../outside.md", r"C:\outside\artifact.md"])
def test_evidence_that_escapes_the_tree_is_refused_on_shape(bad):
    """terra HIGH, 2026-08-23: such a path can EXIST while proving nothing about this repo,
    which is exactly what the downstream existence test relies on."""
    d = _mutate()
    d["models"]["acme-1"]["roles"] = []
    d["models"]["acme-1"]["role_admission"] = {
        "fan-out": {
            "verdict": "refused",
            "decided_by": "architect",
            "decided_on": "2026-08-23",
            "evidence": bad,
        }
    }
    with pytest.raises(ValidationError, match="repo-relative"):
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


# --- LANE-5B-2 Done item 4: `Provider.model_currency` / `RoleEntry.currency_exception` -----

def test_model_currency_with_neither_command_nor_exception_is_refused():
    """A provider that is neither checkable (`command`) nor excused (`exception`) is silence
    wearing this field's name — the same shape as a `RoleAdmission` with no provenance."""
    d = _mutate()
    d["providers"]["acme"]["model_currency"] = {}
    with pytest.raises(ValidationError, match="model_currency"):
        _validate(d)


def test_model_currency_with_only_an_exception_is_legal():
    d = _mutate()
    d["providers"]["acme"]["model_currency"] = {
        "exception": {
            "reason": "no listing subcommand",
            "decided_by": "architect",
            "decided_on": "2026-09-24",
        }
    }
    assert _validate(d) is not None


def test_model_currency_with_only_a_command_is_legal():
    d = _mutate()
    d["providers"]["acme"]["model_currency"] = {"command": ["acmecli", "models"]}
    assert _validate(d) is not None


def test_a_role_entrys_currency_exception_needs_full_provenance():
    """Reuses `CurrencyException`'s own required fields — this is not a second provenance rule,
    it is the same one `RoleAdmission`/`ProviderLicence` already enforce, applied here too."""
    d = _mutate()
    d["roles"] = {
        "implement": {
            "description": "produce",
            "order": [
                {
                    "provider": "acme",
                    "model": "acme-1",
                    "currency_exception": {"reason": "stale", "decided_by": "architect"},
                }
            ],
        }
    }
    with pytest.raises(ValidationError, match="decided_on"):
        _validate(d)


def test_a_role_entrys_currency_exception_with_full_provenance_is_legal():
    d = _mutate()
    d["roles"] = {
        "implement": {
            "description": "produce",
            "order": [
                {
                    "provider": "acme",
                    "model": "acme-1",
                    "currency_exception": {
                        "reason": "stale",
                        "decided_by": "architect",
                        "decided_on": "2026-09-25",
                    },
                }
            ],
        }
    }
    assert _validate(d) is not None
