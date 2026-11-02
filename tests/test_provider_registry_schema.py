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
        "review": {  # not `implement`: R177 pins that role's first entry to copilot-enterprise
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


def _e32_role(data, *, provider="acme", model="acme-1", **entry_fields):
    data["roles"] = {
        "review": {
            "description": "Review a change.",
            "order": [{"provider": provider, "model": model, **entry_fields}],
        }
    }
    return data


@pytest.mark.parametrize(
    "billing_class", ["subscription", "subscription-employer", "subscription+credit", "metered"]
)
def test_e32_provider_billing_class_accepts_each_declared_value(billing_class):
    """Done-contract A1: each declared billing class has a valid schema representation."""
    assert _validate(_mutate()).providers["acme"].billing is None
    d = _mutate()
    d["providers"]["acme"]["billing"] = {"class": billing_class}
    validated = _validate(d)
    assert validated.providers["acme"].billing is not None
    assert validated.model_dump(by_alias=True)["providers"]["acme"]["billing"]["class"] == (
        billing_class
    )


def test_e32_provider_billing_class_refuses_an_undeclared_value():
    """Done-contract A1: `free` is not a billing class."""
    supported = _mutate()
    supported["providers"]["acme"]["billing"] = {"class": "subscription"}
    assert _validate(supported).providers["acme"].billing is not None
    d = _mutate()
    d["providers"]["acme"]["billing"] = {"class": "free"}
    with pytest.raises(ValidationError, match="class"):
        _validate(d)


def test_e32_billing_accepts_optional_quota_budget_overflow_and_credit_fields():
    """Done-contract A1: the optional nested billing surface stays explicit and extensible."""
    d = _mutate()
    d["providers"]["acme"]["billing"] = {
        "class": "subscription",
        "plan": "Ultra",
        "unit": "credits/month",
        "included_per_month": 25000,
        "quota_reader": {
            "kind": "internal_user",
            "refuse_launch_above_pct": 95.0,
        },
        "daily_budget": {
            "default_usd": 20,
            "per_case_cap_usd": 5,
            "warn_when_mtd_ahead_of_pace_x": 1.5,
            "refuse_noncritical_when_mtd_above": 25000,
            "overage": "refuse",
            "record": True,
        },
        "overflow": {"provider": "openai", "model": "gpt-6-sol"},
        "api_credit": {
            "monthly_usd": 20,
            "balance_usd": 12.5,
            "read_on": "2026-11-01",
            "source": "provider dashboard",
        },
    }
    billing = _validate(d).providers["acme"].billing
    assert billing.quota_reader.refuse_launch_above_pct == 95.0
    assert billing.daily_budget.overage == "refuse"
    assert billing.overflow["provider"] == "openai"
    assert billing.api_credit.balance_usd == 12.5


def test_e32_subscription_credit_requires_an_api_credit_block():
    """Done-contract A2: a subscription-plus-credit provider must declare its credit block."""
    d = _mutate()
    d["providers"]["acme"]["billing"] = {"class": "subscription+credit"}
    with pytest.raises(ValidationError, match="api_credit"):
        _validate(d)


def test_e32_subscription_credit_accepts_its_api_credit_block():
    """Done-contract A2: an API-credit balance and its provenance are valid billing data."""
    d = _mutate()
    d["providers"]["acme"]["billing"] = {
        "class": "subscription+credit",
        "api_credit": {
            "monthly_usd": 20,
            "balance_usd": 12.5,
            "read_on": "2026-11-01",
            "source": "provider dashboard",
        },
    }
    assert _validate(d).providers["acme"].billing.api_credit.balance_usd == 12.5


def test_e32_metered_billing_requires_a_daily_default_and_allows_zero():
    """Done-contract A3: metered billing requires `default_usd`; zero remains representable."""
    d = _mutate()
    d["providers"]["acme"]["billing"] = {"class": "metered", "daily_budget": {}}
    with pytest.raises(ValidationError, match="default_usd"):
        _validate(d)
    d["providers"]["acme"]["billing"]["daily_budget"]["default_usd"] = 0
    assert _validate(d).providers["acme"].billing.daily_budget.default_usd == 0


@pytest.mark.parametrize(
    "budget",
    [
        {"default_usd": -0.01},
        {"default_usd": 1, "per_case_cap_usd": -1},
        {"default_usd": 1, "warn_when_mtd_ahead_of_pace_x": -1},
        {"default_usd": 1, "refuse_noncritical_when_mtd_above": -1},
    ],
)
def test_e32_daily_budget_refuses_negative_numbers(budget):
    """Done-contract A3: negative budget values cannot become a plausible allowance."""
    valid = _mutate()
    valid["providers"]["acme"]["billing"] = {
        "class": "metered",
        "daily_budget": {"default_usd": 1},
    }
    assert _validate(valid).providers["acme"].billing.daily_budget.default_usd == 1
    d = _mutate()
    d["providers"]["acme"]["billing"] = {
        "class": "metered",
        "daily_budget": {"default_usd": 1, **budget},
    }
    with pytest.raises(ValidationError, match="budget|positive|negative|greater"):
        _validate(d)


def test_e32_role_entry_accepts_billing_flags_and_read_batch_fallback():
    """Done-contract A4: role routing carries pool/session metadata and the `wait` policy."""
    d = _e32_role(
        _mutate(),
        billing_pool="subscription-employer",
        per_case_only=True,
        isolated_session=True,
    )
    d["roles"]["review"]["batch_fallback"] = "wait"
    validated = _validate(d)
    assert validated.roles["review"].order[0].billing_pool == "subscription-employer"
    assert validated.roles["review"].order[0].per_case_only is True
    assert validated.roles["review"].order[0].isolated_session is True
    assert validated.roles["review"].batch_fallback == "wait"
    d["roles"]["review"]["batch_fallback"] = "route"
    with pytest.raises(ValidationError, match="batch_fallback"):
        _validate(d)
    defaults = _e32_role(_mutate())
    entry = _validate(defaults).roles["review"].order[0]
    assert entry.billing_pool is None
    assert entry.per_case_only is False
    assert entry.isolated_session is False


def test_e32_metered_role_entries_must_be_per_case_only():
    """Done-contract A5: no ordinary role route may spend a metered provider."""
    d = _e32_role(_mutate())
    d["providers"]["acme"]["billing"] = {
        "class": "metered",
        "daily_budget": {"default_usd": 1},
    }
    with pytest.raises(ValidationError, match="per_case_only"):
        _validate(d)
    d["roles"]["review"]["order"][0]["per_case_only"] = True
    assert _validate(d).roles["review"].order[0].per_case_only is True


def test_e32_api_credit_pool_cannot_be_a_subscription_credit_role_route():
    """Done-contract A6: API credits are tracked but never selected by a role."""
    d = _e32_role(_mutate(), billing_pool="api-credit")
    d["providers"]["acme"]["billing"] = {
        "class": "subscription+credit",
        "api_credit": {"balance_usd": 2},
    }
    with pytest.raises(ValidationError, match="api-credit"):
        _validate(d)
    d["providers"]["acme"]["billing"] = {"class": "subscription"}
    assert _validate(d).roles["review"].order[0].billing_pool == "api-credit"


def test_e32_provider_accounts_and_failover_are_valid_and_account_ids_are_unique():
    """Done-contract A7: account identity is per-provider and inactive seats remain explicit."""
    account = {
        "id": "acct-1",
        "config_dir": "~/.config/acme",
        "surfaces": ["cli"],
        "seats": ["*"],
        "active": True,
    }
    d = _mutate()
    d["providers"]["acme"]["accounts"] = [account]
    d["providers"]["acme"]["account_failover"] = {
        "on": ["quota"],
        "rule": "select the next active account",
        "resume": "retry when reset",
    }
    assert _validate(d).providers["acme"].accounts[0].active is True
    d["providers"]["acme"]["accounts"] = [account, {**account}]
    with pytest.raises(ValidationError, match="account"):
        _validate(d)
    missing_active = {key: value for key, value in account.items() if key != "active"}
    d["providers"]["acme"]["accounts"] = [missing_active]
    with pytest.raises(ValidationError, match="active"):
        _validate(d)


def test_e32_cross_provider_model_pin_requires_also_served_by():
    """Done-contract A8: cross-provider pins require an explicit serving declaration."""
    d = _mutate()
    d["providers"]["p2"] = {"display_name": "Provider Two"}
    d["roles"] = {
        "review": {
            "description": "Review.",
            "order": [{"provider": "p2", "model": "acme-1"}],
        }
    }
    with pytest.raises(ValidationError, match="belongs to provider"):
        _validate(d)
    d["models"]["acme-1"]["also_served_by"] = ["p2"]
    assert _validate(d).roles["review"].order[0].provider == "p2"
    d["models"]["acme-1"]["also_served_by"] = ["ghost"]
    with pytest.raises(ValidationError, match="undeclared provider"):
        _validate(d)


def test_e32_evaluation_is_a_separate_optional_role_collection():
    """Done-contract A9: evaluation uses Role shape without changing ROLE_NAMES."""
    s = _schema()
    assert "evaluate" not in s.ROLE_NAMES
    assert _validate(_mutate()).evaluation is None
    d = _mutate()
    d["evaluation"] = {
        "description": "Independent evaluation.",
        "excludes_producer": True,
        "order": [
            {
                "provider": "acme",
                "model": "acme-1",
                "requires_admission": True,
            }
        ],
    }
    validated = _validate(d)
    assert validated.evaluation.excludes_producer is True
    assert validated.evaluation.order[0].requires_admission is True
    d["providers"]["p2"] = {"display_name": "Provider Two"}
    d["evaluation"]["order"] = [
        {"provider": "p2", "model": "acme-1", "requires_admission": True}
    ]
    with pytest.raises(ValidationError, match="belongs to provider"):
        _validate(d)
    d["models"]["acme-1"]["also_served_by"] = ["p2"]
    assert _validate(d).evaluation.order[0].requires_admission is True


def test_e32_evaluation_refuses_unknown_targets_and_anthropic():
    """Done-contract A9: evaluation entries use normal reference checks and exclude Claude."""
    d = _mutate()
    d["evaluation"] = {
        "description": "Independent evaluation.",
        "order": [{"provider": "ghost", "model": "acme-1"}],
    }
    with pytest.raises(ValidationError, match="undeclared provider"):
        _validate(d)
    d["evaluation"]["order"] = [{"provider": "acme", "model": "missing"}]
    with pytest.raises(ValidationError, match="undeclared model"):
        _validate(d)
    d["providers"]["anthropic"] = {"display_name": "Anthropic"}
    d["models"]["anthropic-1"] = {"provider": "anthropic"}
    d["evaluation"]["order"] = [{"provider": "anthropic", "model": "anthropic-1"}]
    with pytest.raises(ValidationError, match="anthropic"):
        _validate(d)


def test_e32_model_rates_accept_short_cache_and_long_context_rates():
    """Done-contract A10: optional short-cache and large-context tiers are positive rates."""
    d = _mutate()
    d["rate_card"] = {
        "currency": "USD",
        "unit": "per_million_tokens",
        "as_of": "2026-11-01",
        "basis": "list-price",
        "source": "official pricing",
        "cache_write_multiplier": 2,
        "cache_read_multiplier": 0.1,
    }
    d["models"]["acme-1"]["rates"] = {
        "input": 1,
        "output": 2,
        "cache_write_5m": 0.5,
        "long_context": {
            "threshold_tokens": 100000,
            "input": 2,
            "output": 4,
            "cache_write": 4,
            "cache_write_5m": 1,
            "cache_read": 0.2,
        },
    }
    rates = _validate(d).models["acme-1"].rates
    assert rates.cache_write_5m == 0.5
    assert rates.long_context.threshold_tokens == 100000


@pytest.mark.parametrize(
    "rates",
    [
        {"cache_write_5m": 0},
        {"cache_write_5m": -0.1},
        {"long_context": {"threshold_tokens": 0, "input": 1, "output": 1,
                          "cache_write": 1, "cache_write_5m": 1, "cache_read": 1}},
        {"long_context": {"threshold_tokens": 100, "input": 0, "output": 1,
                          "cache_write": 1, "cache_write_5m": 1, "cache_read": 1}},
        {"long_context": {"threshold_tokens": 100, "input": 1, "output": 1,
                          "cache_write": 1, "cache_write_5m": 1, "cache_read": -1}},
        {"long_context": {"threshold_tokens": 100, "input": 1, "output": 0,
                          "cache_write": 1, "cache_write_5m": 1, "cache_read": 1}},
        {"long_context": {"threshold_tokens": 100, "input": 1, "output": 1,
                          "cache_write": 0, "cache_write_5m": 1, "cache_read": 1}},
        {"long_context": {"threshold_tokens": 100, "input": 1, "output": 1,
                          "cache_write": 1, "cache_write_5m": 0, "cache_read": 1}},
    ],
)
def test_e32_model_rates_refuse_nonpositive_cache_and_long_context_values(rates):
    """Done-contract A10: every optional rate and its threshold must be positive."""
    valid = _mutate()
    valid["rate_card"] = {
        "currency": "USD",
        "unit": "per_million_tokens",
        "as_of": "2026-11-01",
        "basis": "list-price",
        "source": "official pricing",
        "cache_write_multiplier": 2,
        "cache_read_multiplier": 0.1,
    }
    valid["models"]["acme-1"]["rates"] = {
        "input": 1,
        "output": 2,
        "cache_write_5m": 0.5,
        "long_context": {
            "threshold_tokens": 100,
            "input": 2,
            "output": 4,
            "cache_write": 4,
            "cache_write_5m": 1,
            "cache_read": 0.2,
        },
    }
    assert _validate(valid).models["acme-1"].rates.cache_write_5m == 0.5
    d = _mutate()
    d["rate_card"] = {
        "currency": "USD",
        "unit": "per_million_tokens",
        "as_of": "2026-11-01",
        "basis": "list-price",
        "source": "official pricing",
        "cache_write_multiplier": 2,
        "cache_read_multiplier": 0.1,
    }
    d["models"]["acme-1"]["rates"] = {"input": 1, "output": 2, **rates}
    with pytest.raises(ValidationError):
        _validate(d)


def test_e32_fallback_trigger_accepts_model_map_and_optional_draft_fields():
    """Done-contract A11: the draft trigger shape needs no single target model or signal."""
    d = _mutate()
    d["roles"] = {
        "review": {
            "description": "Review.",
            "order": [{"provider": "acme", "model": "acme-1"}],
        }
    }
    d["fallback_triggers"] = {
        "codex_quota": {
            "rule": "route after quota",
            "roles": ["review"],
            "to_provider": "acme",
            "to_model_map": {"model-a": "model-b"},
            "decided_by": "operator",
            "decided_on": "2026-11-01",
            "evidence": "docs/audit.md",
        }
    }
    trigger = _validate(d).fallback_triggers["codex_quota"]
    assert trigger.to_model_map == {"model-a": "model-b"}
    assert trigger.enabled is True
    assert trigger.signals == {}
    d["fallback_triggers"]["codex_quota"].update(
        enabled=False,
        unless="operator override",
        on_quota_out="wait",
        note="retain the current rung",
    )
    optional_fields = _validate(d).fallback_triggers["codex_quota"]
    assert optional_fields.enabled is False
    assert optional_fields.unless == "operator override"
    assert optional_fields.on_quota_out == "wait"
    assert optional_fields.note == "retain the current rung"


def test_e32_fallback_trigger_still_refuses_an_undeclared_role():
    """Done-contract A11: making trigger fields optional does not loosen role references."""
    d = _mutate()
    d["roles"] = {
        "review": {
            "description": "Review.",
            "order": [{"provider": "acme", "model": "acme-1"}],
        }
    }
    d["fallback_triggers"] = {
        "bad": {
            "rule": "route after quota",
            "roles": ["ghost"],
            "to_provider": "acme",
            "to_model_map": {},
            "decided_by": "operator",
            "decided_on": "2026-11-01",
            "evidence": "docs/audit.md",
        }
    }
    valid = copy.deepcopy(d)
    valid["fallback_triggers"]["bad"]["roles"] = ["review"]
    assert _validate(valid).fallback_triggers["bad"].roles == ("review",)
    with pytest.raises(ValidationError, match="ghost"):
        _validate(d)
