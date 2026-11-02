"""Provider/model registry contract — pydantic models for `ecosystem/provider-registry.yaml`.

Models ONLY: no file I/O, no network, no execution (Layer-2, ADR-28/36). The loader is
`scripts/provider_registry.py`, which parses the YAML and hands the mapping here for
validation; the seam checker (`scripts/check_provider_registry.py`) and the SessionStart
sentinel (`scripts/changelog_sentinel.py`) both reach the registry through that loader, so
every consumer validates through this module without any of them importing it.

WHY PYDANTIC AND NOT A HAND-ROLLED SHAPE CHECK — the contract's library-first clause, and it
was the right call on measurement rather than on preference. Before this module the whole of
the registry's shape enforcement was `check_registry_shape()`: eleven lines asserting exactly
one rule (*"every model names a registered provider"*). Nothing checked that a `cli:` and its
`version_command:` named the same binary, that a `changelog_tool_key` had a matching
`changelog_source_url`, or that an unknown key was a typo rather than a feature. `pydantic>=2`
is already in the curated baseline (`pyproject.toml`, ADR-109/[#382] W2) and the sibling
`ecosystem/schema/desired_state.py` already establishes this directory as the contract home,
so the divergence a hand-rolled checker would need to justify itself does not exist here.

THE SEPARATION THIS SCHEMA ENCODES — configuration is decoupled from role admission.

* `role_admission` is **optional and defaults to empty**. A model row is fully valid with no
  admission record whatsoever. Nothing in this schema can make a row's EXISTENCE conditional
  on a verdict, which is the structural statement of the rule: a provider that failed an
  admission floor is still configurable, still addressable, still in the vocabulary.
* What the schema DOES enforce is the other direction, and only the other direction: a role
  recorded as `refused` may not simultaneously appear in `roles:`. Admission governs role
  ELIGIBILITY. It governs nothing else.

The governing record for that rule, with the fork named and the ADR-98 section 3 test applied,
is `docs/audits/2026-08-23-technical-lane-provider-config.md` section 6.
"""

from __future__ import annotations

import datetime
import re
from pathlib import PurePosixPath
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, StrictStr, model_validator

#: 1.8.0 — `e32-provider-billing` ([#1833], [#1844]) adds, all optional with inert defaults:
#: `Provider.billing` / `.accounts` / `.account_failover`, `RoleEntry.billing_pool` / `.per_case_only` /
#: `.isolated_session`, `Role.batch_fallback`, `Model.also_served_by`, `ModelRates.cache_write_5m` /
#: `.long_context`, `FallbackTrigger`'s draft section-4 shape and the top-level `ProviderRegistry.evaluation`.
#: MINOR in kind.
#: 1.6.0 — `e2-subst-gate` (R138, R140, R153; P1) adds `RoleEntry.substrate` (where the entry runs:
#: `local` or `codespace`) and `RoleEntry.paired` (the entry runs TOGETHER with the other paired
#: entries of its role rather than as a fallback). MINOR: both are optional with inert defaults, so
#: every earlier registry validates unchanged.
#: 1.5.0 — `lane-bu-1536-routing` ([#1536], R104) adds `RoleEntry.max_turns_floor` (a reviewer entry
#: declares the minimum `--max-turns` its CLI needs) and the `red`/`qa`/`judge` role names. MINOR:
#: the field is optional, so every earlier registry validates unchanged.
#: 1.4.0 — `foundation-10-model-currency` (R61) adds `Model.last_verified` and `Model.evidence`:
#: the date a model id was last read as SERVED, and the records that show it. Both optional, so
#: every pre-R61 registry validates unchanged (MINOR); an unset date is read as unverified by
#: `scripts/check_model_currency.py`. Not a member of `validate_reconciliation._SPEC_REGISTRY`,
#: so no reconciliation obligation follows from this bump.
#: 1.7.0 — `e2-model-routing` (R177/R178, operator) adds `RoleEntry.vendor_fail_only` and the `seat-orchestrator` /
#: `seat-integrator` roles: `implement` is Copilot-first, and an anthropic `implement` entry must carry
#: `vendor_fail_only: true` (it runs only after a recorded `VENDOR-FAIL: implement ...`). MINOR: the
#: field defaults to false and the roles are optional, so every pre-1.7.0 registry still validates
#: unless it names an anthropic implementer.
#: 1.3.0 — `lane-ratified-unbuilt` (WAVE5B-N5-R, R22) adds `ProviderRegistry.dispatcher`
#: (`DispatcherPin`): the model the dispatcher session itself runs on. NOT a `roles:` entry —
#: the dispatcher is a session type whose logic is code, not one of AX21-1's six
#: producer/reviewer roles, and R22 is an explicit override against `roles.orchestrate`
#: (Opus-only, not rerankable), not a repoint of it. MINOR: the field is optional, so every
#: pre-R22 registry still validates unchanged. 1.2.0 was LANE-5B-2's `Provider.model_currency`
#: and `RoleEntry.currency_exception` (Done item 4: a role's pinned id is the newest its
#: provider's CLI lists, or carries a dated exception). 1.1.0 was `[#691]`'s THIRD collection
#: (`roles:`: ordered fallback lists, per-entry admission, the reviewer-not-producer flag) and
#: the per-provider `licence:` block. Not a member of `validate_reconciliation._SPEC_REGISTRY`
#: (which registers `handoff-process` and `prompt-template` only), so this bump carries no
#: reconciliation obligation — checked rather than assumed.
SCHEMA_VERSION = "1.8.0"

#: The prefix that marks an evidence reference as living on the operator's transport rather than
#: in this repository. CI cannot read the transport, so such a reference may ride beside an
#: in-repo one and is never checked for existence by the repository's own gates.
EVIDENCE_TRANSPORT_PREFIX = "transport:"

#: A verdict's closed vocabulary. `unevaluated` is a first-class member on purpose: a provider
#: nobody has run through the admission pipeline is a KNOWN state, not a missing one, and
#: saying so is what stops the absence being read as a refusal.
Verdict = Literal["admitted", "refused", "unevaluated"]


class _Contract(BaseModel):
    """Contract-native type: we own this grammar, so an unknown key is a spec error.

    `extra="forbid"` is the load-bearing half. The registry's fields were previously implied
    by whichever accessor happened to read them, so a misspelled key was silently inert data
    — the present-but-unread failure mode in miniature. Forbidding extras converts a typo
    into a blocked commit and makes "add a field deliberately" a real act with a real diff.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    @model_validator(mode="after")
    def _no_blank_or_untrimmed_strings(self) -> "_Contract":
        """No field is a blank, whitespace-only, or untrimmed string. Applies to EVERY model
        here, which is why it lives on the base rather than being repeated per field.

        terra CRITICAL + HIGH, round 6 (2026-08-23), and the failure was silent in both
        directions. `changelog_tool_key: ""` paired with `changelog_source_url: ""` satisfied
        the both-or-neither rule, then `version_commands()` and `changelog_source_urls()` —
        which guard with `if key and url` — dropped that provider from the SessionStart probe
        and from the S8 comparison, with nothing saying so. And ` codex ` is neither blank nor
        equal to `codex`, so it defeated the uniqueness rule while naming the same tool.

        A registry value is an identifier or a path. Neither has a legitimate blank form, and
        neither has a legitimate leading or trailing space.
        """
        for name, value in self:
            if isinstance(value, str):
                items = ((name, value),)
            elif isinstance(value, tuple) and all(isinstance(v, str) for v in value):
                items = tuple((f"{name}[{i}]", v) for i, v in enumerate(value))
            elif isinstance(value, dict):
                # Mapping KEYS are identifiers too — provider ids, model ids, role names —
                # and they were the hole this validator left after round 6 (terra HIGH,
                # round 7). A padded `role_admission` key does not intersect the matching
                # `roles` entry, so `" fan-out "` recorded as refused left `fan-out` held.
                items = tuple((f"{name}[{k!r}]", k) for k in value if isinstance(k, str))
            else:
                continue
            for label, v in items:
                if not v.strip():
                    raise ValueError(
                        f"`{label}` is blank — an absent value is expressed by omitting the "
                        f"key or setting it null, never by an empty string, which reads as "
                        f"present to a shape check and as absent to every consumer")
                if v != v.strip():
                    raise ValueError(
                        f"`{label}` has leading or trailing whitespace ({v!r}) — an "
                        f"identifier that differs from its neighbour only by padding is a "
                        f"duplicate that every equality check misses")
        return self


class Pin(_Contract):
    """One site where a model id is hardcoded, and the format the checker must parse."""

    path: StrictStr
    seam: StrictStr
    format: StrictStr


class RoleAdmission(_Contract):
    """One role's admission verdict for one model — provenance-bearing, never bare.

    A verdict with no decider, no date and no evidence is an assertion; this repo's whole
    posture is that an assertion is not a record. So anything other than `unevaluated` must
    carry all three, and the validator below refuses the row rather than trusting it.
    """

    verdict: Verdict
    decided_by: Optional[StrictStr] = None
    decided_on: Optional[datetime.date] = None
    #: The named floors the verdict turned on (e.g. `["G1", "G2"]`, standing ruling Q9's
    #: `G1 AND G2 AND G3` arithmetic). Empty is legitimate for `unevaluated`.
    floors: tuple[StrictStr, ...] = ()
    #: Repo-relative path to the artifact carrying the measurement. Existence is asserted by
    #: `check_provider_registry.check_role_admission_evidence`, not here — a schema that
    #: touched the filesystem would stop being a models-only module.
    evidence: Optional[StrictStr] = None
    #: The open row carrying any owed re-run, as a bracketed id (`[#578]`).
    rerun_carrier: Optional[StrictStr] = None

    @model_validator(mode="after")
    def _a_decided_verdict_carries_its_provenance(self) -> "RoleAdmission":
        if self.verdict == "unevaluated":
            return self
        # BLANK counts as missing, not as present (terra HIGH, 2026-08-23). Testing `is None`
        # alone let `evidence: ""` satisfy this rule and then skip the checker's existence
        # test, which is a verdict with provenance-shaped nothing behind it.
        missing = [
            name
            for name, value in (
                ("decided_by", self.decided_by),
                ("decided_on", self.decided_on),
                ("evidence", self.evidence),
            )
            if value is None or (isinstance(value, str) and not value.strip())
        ]
        if missing:
            raise ValueError(
                f"verdict `{self.verdict}` is missing its provenance: {', '.join(missing)} "
                f"— a verdict without a decider, a date and an evidence artifact is an "
                f"assertion, not a record"
            )
        return self

    @model_validator(mode="after")
    def _evidence_is_a_repo_relative_path(self) -> "RoleAdmission":
        """Shape only — existence is `check_role_admission_evidence`'s job, not a schema's.

        An absolute path, or one climbing out of the tree with `..`, can EXIST while proving
        nothing about this repository, which defeats the existence test downstream.
        """
        if self.evidence is None:
            return self
        p = PurePosixPath(self.evidence.replace("\\", "/"))
        if p.is_absolute() or ".." in p.parts or re.match(r"^[A-Za-z]:", self.evidence):
            raise ValueError(
                f"evidence `{self.evidence}` is not a repo-relative path — an absolute or "
                f"climbing path can resolve outside the tree the checker verifies"
            )
        return self


#: Whether this repo's use of a provider is permitted by the terms it is held under —
#: `[#691]` leg (c), which the row records as absent entirely ("grepped: zero hits for
#: licence/license/terms"). A CLOSED vocabulary with `unknown` as a first-class member, for the
#: same reason `Verdict` carries `unevaluated`: a licence nobody has ruled on is a KNOWN state,
#: and saying so is what stops the absence being read as permission.
#:
#: `restricted` is NOT "forbidden" — it is *permitted for some uses and not others*, which is
#: the honest shape for a seat licensed to an employer. The router treats anything other than
#: `permitted` as ineligible for a PRODUCING role; it is deliberately not this schema's job to
#: decide which, because that is a functional question and belongs to the operator (ADR-108 §A).
Licence = Literal["permitted", "restricted", "unknown", "not-applicable"]


class ProviderLicence(_Contract):
    """What terms a provider is used under here, and who says so.

    Provenance-bearing on the same principle as `RoleAdmission`: a bare `permitted` is an
    assertion. `unknown` is the one verdict that needs no decider — nobody decided it, which is
    precisely what it records — but it still carries a `reason` so the next reader learns what
    the open question actually is rather than re-deriving it.
    """

    status: Licence
    #: MANDATORY on every licence row. For `unknown` it states the open question; for the other
    #: three it states the basis. There is no shape of this field that is legitimately absent:
    #: a licence status with no stated ground is the drift this field exists to end.
    reason: StrictStr
    decided_by: Optional[StrictStr] = None
    decided_on: Optional[datetime.date] = None

    @model_validator(mode="after")
    def _a_decided_licence_carries_its_decider(self) -> "ProviderLicence":
        """`unknown` is exempt; every other status names who ruled it and when.

        The asymmetry is the point. `unknown` means no one has decided, so demanding a decider
        would make the honest state unexpressible and push every unruled provider into a
        fabricated `permitted` — the exact failure this vocabulary exists to prevent.
        """
        if self.status == "unknown":
            return self
        missing = [
            name
            for name, value in (("decided_by", self.decided_by), ("decided_on", self.decided_on))
            if value is None or (isinstance(value, str) and not value.strip())
        ]
        if missing:
            raise ValueError(
                f"licence status `{self.status}` is missing {', '.join(missing)} — a licence "
                f"ruling without a decider and a date is an assertion, not a record; use "
                f"`unknown` when nobody has actually decided"
            )
        return self


class CurrencyException(_Contract):
    """Why a model id's currency cannot be, or was not, verified against a live CLI listing —
    LANE-5B-2 Done item 4. Dated and provenance-bearing on the same principle as
    `RoleAdmission` and `ProviderLicence`: "we didn't check" is a fact that decays exactly
    like an admission does, so it is recorded rather than left implicit in an absence.
    """

    reason: StrictStr
    decided_by: StrictStr
    decided_on: datetime.date
    #: Where a reader can independently corroborate currency when no live listing exists for
    #: it (e.g. a changelog-review audit). Optional: an exception may simply record that no
    #: such source exists yet.
    source: Optional[StrictStr] = None


class ModelCurrency(_Contract):
    """How this provider's served-model currency is checked, or why it is not — LANE-5B-2
    Done item 4: *"a test asserts ... that each role's pinned id is the newest id that CLI
    lists for its tier, or that the registry row carries a dated `exception:` line."*

    DATA, not code: the probe command a currency test runs is read from `command` here rather
    than hard-coded per provider in test source, so a CLI's listing syntax changing needs one
    YAML edit, not a test-source edit.
    """

    #: argv that lists this provider's currently-served model ids, when the CLI offers one.
    #: `None` when it does not (`claude`, `copilot-enterprise` measured 2026-09-24: neither
    #: CLI has a listing subcommand) — `exception` is then mandatory, see the validator below.
    command: Optional[tuple[StrictStr, ...]] = None
    #: Free text: how to read `command`'s output into a set of currently-served ids (a JSON
    #: path, a visibility filter, a delimiter). Only meaningful alongside `command`.
    parse: Optional[StrictStr] = None
    exception: Optional[CurrencyException] = None

    @model_validator(mode="after")
    def _no_listing_command_needs_a_dated_exception(self) -> "ModelCurrency":
        if self.command is None and self.exception is None:
            raise ValueError(
                "`model_currency` names no `command` and no `exception` — a provider that is "
                "neither checkable nor excused is silence wearing this field's name"
            )
        return self


#: [#1833] D1 (PROPOSAL-ADR-ROUTING-COST v3): the closed set of billing classes. `subscription+credit` is a flat
#: plan that ALSO carries a pool of API credit (A-2); nothing routes to that pool without a separate ruling.
BILLING_CLASSES: tuple[str, ...] = (
    "subscription", "subscription-employer", "subscription+credit", "metered")
BillingClass = Literal["subscription", "subscription-employer", "subscription+credit", "metered"]

#: The `RoleEntry.billing_pool` value that names an API-credit pool (A-2): refused on a role entry of a
#: `subscription+credit` provider.
API_CREDIT_POOL = "api-credit"

#: The pseudo-role name under which `ProviderRegistry.evaluation` is routed (contract R12 / /decide evaluation).
#: NOT a member of `ROLE_NAMES`: other tests and `cost_usage_telemetry.ROLES` pin that vocabulary.
EVALUATION_ROLE = "evaluate"


class QuotaReaderSpec(_Contract):
    """How a provider's remaining quota is read (R-4); the reader itself is code in `scripts/quota_watch.py`."""

    kind: StrictStr
    refuse_launch_above_pct: Optional[float] = None

    @model_validator(mode="after")
    def _a_threshold_is_a_percentage(self) -> "QuotaReaderSpec":
        t = self.refuse_launch_above_pct
        if t is not None and not 0 < t <= 100:
            raise ValueError(f"`refuse_launch_above_pct` {t} is outside (0, 100] -- a launch threshold is a percentage")
        return self


class DailyBudget(_Contract):
    """R-5: the daily / month-to-date allowance of one provider. Every number is non-negative; zero is legal."""

    default_usd: Optional[float] = None
    per_case_cap_usd: Optional[float] = None
    warn_when_mtd_ahead_of_pace_x: Optional[float] = None
    refuse_noncritical_when_mtd_above: Optional[float] = None
    overage: Optional[StrictStr] = None
    record: Optional[Union[StrictStr, bool]] = None

    @model_validator(mode="after")
    def _no_negative_budget(self) -> "DailyBudget":
        for name in ("default_usd", "per_case_cap_usd", "warn_when_mtd_ahead_of_pace_x",
                     "refuse_noncritical_when_mtd_above"):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(
                    f"`daily_budget.{name}` is {value} -- a negative budget is not an allowance, "
                    f"and a total compared against it would pass or fail for no reason")
        return self


class ApiCredit(_Contract):
    """A-2: the API-credit pool a subscription may carry, as READ (balance + when + from where)."""

    monthly_usd: Optional[float] = None
    balance_usd: Optional[float] = None
    read_on: Optional[datetime.date] = None
    source: Optional[StrictStr] = None

    @model_validator(mode="after")
    def _no_negative_credit(self) -> "ApiCredit":
        for name in ("monthly_usd", "balance_usd"):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(f"`api_credit.{name}` is {value} -- a credit balance is not negative")
        return self


class Billing(_Contract):
    """What a provider costs the operator and how its quota is read -- [#1833] D1/R-5.

    Optional on `Provider` for the reason `licence` is: no fabricated values on rows that hold no role.
    `billing_class` is the YAML key `class` (a Python keyword), so the model dumps `by_alias`.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", populate_by_name=True)

    billing_class: BillingClass = Field(alias="class")
    plan: Optional[StrictStr] = None
    unit: Optional[StrictStr] = None
    included_per_month: Optional[float] = None
    quota_reader: Optional[QuotaReaderSpec] = None
    daily_budget: Optional[DailyBudget] = None
    overflow: Optional[dict[StrictStr, Union[StrictStr, int, float, bool]]] = None
    api_credit: Optional[ApiCredit] = None

    @model_validator(mode="after")
    def _the_class_carries_what_it_implies(self) -> "Billing":
        if self.billing_class == "subscription+credit" and self.api_credit is None:
            raise ValueError(
                "billing class `subscription+credit` declares no `api_credit` block -- the class "
                "exists to record a credit pool, and a pool with no balance read is `subscription`")
        if self.billing_class == "metered" and (
                self.daily_budget is None or self.daily_budget.default_usd is None):
            raise ValueError(
                "billing class `metered` declares no `daily_budget.default_usd` -- a metered "
                "provider's allowance is explicit (0 is legal), never implied by an absence")
        return self


class Account(_Contract):
    """D4: one login of a provider. `active: false` accounts are drafted and are never selected."""

    id: StrictStr
    config_dir: StrictStr
    surfaces: tuple[StrictStr, ...] = ()
    seats: tuple[StrictStr, ...] = ()
    active: bool


class AccountFailover(_Contract):
    on: tuple[StrictStr, ...] = ()
    rule: StrictStr
    resume: Optional[StrictStr] = None


class Provider(_Contract):
    """A vendor, the CLI that reaches it, and the host-side config that pins it."""

    display_name: StrictStr
    #: `[#691]` leg (c). OPTIONAL, and its absence means exactly `unknown` — see
    #: `ProviderRegistry.licence_of`. Optionality is deliberate rather than lax: making it
    #: required would have forced a licence verdict onto all seven existing rows in the same
    #: commit that introduced the field, which is how a registry acquires six fabricated
    #: values and one real one.
    licence: Optional[ProviderLicence] = None
    #: LANE-5B-2 Done item 4. OPTIONAL because most of this file's providers (deepseek, cursor,
    #: google) hold no role and are out of the named scope (`claude, codex, agy, copilot,
    #: grok`); the five named providers each carry one.
    model_currency: Optional[ModelCurrency] = None
    #: The token `protocols/AI_COUNCIL_PROCESS.md` names this provider by. It is a SEPARATE
    #: string from the registry key for two of five providers (`anthropic`/`claude`,
    #: `xai`/`grok`), which is exactly why it is data: without it the checker holding the
    #: council roster in agreement would have to hardcode the mapping, re-creating the drift
    #: the registry exists to end. `None` for a provider the council does not panel.
    council_alias: Optional[StrictStr] = None
    #: `None` when the provider has no CLI on this repo's surface. Not an omission — the
    #: absence is a fact about the surface and is asserted against `version_command` below.
    cli: Optional[StrictStr] = None
    version_command: Optional[tuple[StrictStr, ...]] = None
    changelog_tool_key: Optional[StrictStr] = None
    changelog_source_url: Optional[StrictStr] = None
    marketplace_id: Optional[StrictStr] = None
    marketplace_source_path: Optional[StrictStr] = None
    #: [#1833] D1/R-5. OPTIONAL: a provider that holds no role carries no fabricated billing class.
    billing: Optional[Billing] = None
    #: [#1833] D4: drafted accounts, INACTIVE until a ruling activates them.
    accounts: Optional[tuple[Account, ...]] = None
    account_failover: Optional[AccountFailover] = None

    @model_validator(mode="after")
    def _account_ids_are_unique(self) -> "Provider":
        ids = [a.id for a in self.accounts or ()]
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:
            raise ValueError(f"account id(s) {dup} appear twice under one provider -- an account id names one login")
        return self

    @model_validator(mode="after")
    def _cli_and_its_probe_agree(self) -> "Provider":
        if (self.cli is None) != (self.version_command is None):
            raise ValueError(
                "`cli` and `version_command` must be present or absent together — a probe "
                "with no CLI is unrunnable, and a CLI with no probe is invisible to the "
                "SessionStart sentinel"
            )
        if self.version_command is not None:
            if not self.version_command:
                raise ValueError("`version_command` is empty; it must name the binary to run")
            if self.version_command[0] != self.cli:
                raise ValueError(
                    f"`version_command` runs {self.version_command[0]!r} but `cli` is "
                    f"{self.cli!r} — the probe must exercise the CLI this provider declares"
                )
        return self

    @model_validator(mode="after")
    def _lookup_keys_are_lowercase(self) -> "Provider":
        for label, value in (("council_alias", self.council_alias),
                             ("changelog_tool_key", self.changelog_tool_key)):
            if value is not None:
                _require_lowercase(label, value)
        return self

    @model_validator(mode="after")
    def _changelog_identity_is_a_pair(self) -> "Provider":
        if (self.changelog_tool_key is None) != (self.changelog_source_url is None):
            raise ValueError(
                "`changelog_tool_key` and `changelog_source_url` must be present or absent "
                "together — the S8 agreement check keys on the first and compares the "
                "second, so half a pair is a seam that silently checks nothing"
            )
        return self


def _require_lowercase(label: str, value: str) -> None:
    """Refuse a non-lowercase LOOKUP KEY.

    terra MEDIUM, round 8 (2026-08-23), and it was a coherence defect this schema introduced:
    rounds 6-7 compared `council_alias` / `changelog_tool_key` / role names CASEFOLDED for
    collision detection, while every consumer looks them up RAW — `council_aliases()` keyed by
    the literal, `_sole_role_model("subagent-default")`, the sentinel's `tool-versions.yaml`
    lookup. So `council_alias: Claude` would validate, collide correctly, and resolve nowhere.

    This rule replaced that casefolding rather than joining it. Because it runs on each
    `Provider` / `Model` before `ProviderRegistry`'s cross-collection validators, a case
    variant never reaches a comparison, so all three uniqueness checks are now EXACT — the
    casefolded branches were removed rather than left as unreachable decoration.

    Canonicalizing by REFUSAL rather than by silent normalization is the deliberate half: a
    registry that quietly rewrote `Claude` to `claude` would make the file disagree with
    itself on disk, and this repo's posture is that the committed value is the value. Scope is
    lookup keys only — `display_name` (`OpenAI`, `xAI`), `attribution_token` (`grok L5`),
    model ids and paths keep their real casing.
    """
    if value != value.lower():
        raise ValueError(
            f"`{label}` is `{value}` — this is a lookup key, matched raw by every consumer "
            f"and compared exactly for collisions, so it is required lowercase rather than "
            f"silently rewritten"
        )


class LongContextRates(_Contract):
    """The price tier above a prompt-size threshold: every rate is stated, none is derived."""

    threshold_tokens: int
    input: float
    output: float
    cache_write: float
    cache_write_5m: float
    cache_read: float

    @model_validator(mode="after")
    def _every_tier_value_is_positive(self) -> "LongContextRates":
        if self.threshold_tokens < 1:
            raise ValueError(f"`long_context.threshold_tokens` is {self.threshold_tokens} -- a threshold is at least 1")
        for field in ("input", "output", "cache_write", "cache_write_5m", "cache_read"):
            value = getattr(self, field)
            if value <= 0:
                raise ValueError(
                    f"`long_context.{field}` is {value} -- a non-positive rate prices real tokens at "
                    f"nothing or less")
        return self


class ModelRates(_Contract):
    """What one model costs, in the rate card's currency and unit — `[#751]`.

    TWO NUMBERS ARE REQUIRED AND TWO ARE DERIVED. `input` and `output` are the declared
    per-unit prices. `cache_write` and `cache_read` are OPTIONAL overrides: absent, they are
    computed from `input` by the rate card's multipliers, which is the shape the published
    rates actually have (a cache write is a stated multiple of the input rate, not an
    independently quoted price). An override exists for the model whose cache read is quoted
    outright rather than as a multiple — writing that one as a multiplier would be arithmetic
    dressed as a fact.

    ZERO IS REFUSED, not clamped. A rate of 0.0 prices a real model's real tokens at nothing,
    and a total built from it meets any budget spectacularly while meaning nothing — the same
    failure class `merge_receipt` records for a 0.0-minute receipt. A model whose price is
    genuinely unknown carries NO `rates:` block, and the reader then refuses it BY NAME
    (`provider_registry.RateUnavailable`). Absent and free are different facts and the schema
    keeps them different.
    """

    input: float
    output: float
    #: Absent → `input × rate_card.cache_write_multiplier`.
    cache_write: Optional[float] = None
    #: Absent → `input × rate_card.cache_read_multiplier`.
    cache_read: Optional[float] = None
    #: [#1833] C-1/GP5: the 5-minute cache write, quoted outright (the card's multiplier prices the 1-hour write).
    cache_write_5m: Optional[float] = None
    #: [#1833] C-1/GP5: the rates that apply when the prompt exceeds `threshold_tokens` (Haiku 5.5: 100k).
    long_context: Optional[LongContextRates] = None
    #: Per-model provenance, for a price that did not come from the rate card's own source.
    source: Optional[StrictStr] = None

    @model_validator(mode="after")
    def _a_rate_is_positive(self) -> "ModelRates":
        for field in ("input", "output", "cache_write", "cache_read", "cache_write_5m"):
            value = getattr(self, field)
            if value is None:
                continue
            if value <= 0:
                raise ValueError(
                    f"`rates.{field}` is {value} — a non-positive rate prices real tokens at "
                    f"nothing or less, and a total built from it is not a measurement. A model "
                    f"whose price is unknown carries no `rates:` block at all, which the reader "
                    f"refuses by name rather than silently costing at zero"
                )
        return self


class RateCard(_Contract):
    """The units, the provenance and the cache multipliers — declared ONCE for the file.

    WHY THIS IS SEPARATE FROM `ModelRates` AND NOT A DUPLICATE HOME. They are two different
    facts. "What does this model cost" is a property of the model and lives on the model row,
    so adding a model cannot leave its price in a second place to be forgotten. "In what
    currency, per what unit, as of when, from what source, and what do cache tokens multiply
    by" is one fact about the whole card; repeating it on every model row would be the
    restated-constant defect this file exists to end.

    `as_of` IS REQUIRED AND IS THE HONEST LIMIT. A published price is true on a date. A
    consumer comparing a dollar figure across two dates needs to know whether the card moved
    underneath it, and a card with no date invites reading a stale number as a current one.
    """

    currency: StrictStr
    unit: Literal["per_million_tokens"]
    as_of: datetime.date
    #: How the numbers were arrived at — `list-price`, `measured`, `derived`. Free text on
    #: purpose: a closed vocabulary here would need a ruling, and this field informs a reader
    #: rather than gating anything.
    basis: StrictStr
    source: StrictStr
    cache_write_multiplier: float
    cache_read_multiplier: float

    @model_validator(mode="after")
    def _a_multiplier_is_positive(self) -> "RateCard":
        for field in ("cache_write_multiplier", "cache_read_multiplier"):
            if getattr(self, field) <= 0:
                raise ValueError(
                    f"`rate_card.{field}` is {getattr(self, field)} — a non-positive multiplier "
                    f"prices every cache token at nothing or less across the whole card"
                )
        return self


def _names_no_file(ref: str, path: PurePosixPath) -> bool:
    """`.` and a trailing-slash path name a directory, so no evidence file can resolve from them
    (Codex terra P2 on the lane that added `Model.evidence`)."""
    return str(path) == "." or ref.endswith(("/", "\\"))


class Model(_Contract):
    """One model string the repo names, with the roles it holds and the sites that pin it."""

    provider: StrictStr
    tier: Optional[StrictStr] = None
    #: Roles this model HOLDS. Never a role it was refused — see the validator below.
    roles: tuple[StrictStr, ...] = ()
    attribution_token: Optional[StrictStr] = None
    #: `{role: verdict record}`. OPTIONAL BY DESIGN: its absence is what makes configuration
    #: unconditional. See this module's docstring.
    role_admission: dict[StrictStr, RoleAdmission] = {}
    #: What this model costs (`[#751]`). OPTIONAL, and for the same reason `role_admission` is:
    #: a model row's EXISTENCE must not be conditional on a price being known. The repo names
    #: models it does not buy directly and models whose vendor publishes no per-token rate; a
    #: schema that required a price would force one to be invented. Absence is read as
    #: "unpriced" and refused by name at the reader, never costed at zero.
    rates: Optional[ModelRates] = None
    pinned_at: tuple[Pin, ...] = ()
    #: R61. The day this id was last read as SERVED -- by a run's own record (a transcript's
    #: `message.model`, a CLI's `usage.json` `primaryModelId`, a run header), never by a release
    #: note. Optional; absent reads as unverified, and `scripts/check_model_currency.py` flags an
    #: entry whose date is more than 14 days old or absent.
    last_verified: Optional[datetime.date] = None
    #: The records that show it: repo-relative paths, or `transport:<name>` for a file that lives
    #: only on the operator's transport. A date with no evidence is refused below.
    evidence: tuple[StrictStr, ...] = ()
    #: Model family (e.g. `anthropic`, `openai`); lets a role demand a distinct family.
    family: Optional[StrictStr] = None
    #: [#1833]: OTHER providers that serve this same model id (Copilot serves `gpt-5.6-terra`, Codex serves
    #: `gpt-6-luna`). A role entry may pin the model under one of these providers; any other cross-provider
    #: pin stays refused. `provider` remains the OWNER (the allowlist and admission key).
    also_served_by: tuple[StrictStr, ...] = ()

    @model_validator(mode="after")
    def _a_verification_date_names_its_evidence(self) -> "Model":
        if self.last_verified is not None and not self.evidence:
            raise ValueError(
                "`last_verified` is set but `evidence` names nothing to check it against -- a "
                "date nobody can verify is an assertion, not a record"
            )
        for ref in self.evidence:
            if ref.startswith(EVIDENCE_TRANSPORT_PREFIX):
                name = ref[len(EVIDENCE_TRANSPORT_PREFIX):]
                p = PurePosixPath(name.replace("\\", "/"))
                bad = (not name or p.is_absolute() or ".." in p.parts
                       or re.match(r"^[A-Za-z]:", name) or _names_no_file(name, p))
            else:
                p = PurePosixPath(ref.replace("\\", "/"))
                bad = (p.is_absolute() or ".." in p.parts or re.match(r"^[A-Za-z]:", ref)
                       or _names_no_file(ref, p))
            if bad:
                raise ValueError(
                    f"evidence `{ref}` is not a resolvable evidence reference -- a repo-relative "
                    f"path, or `{EVIDENCE_TRANSPORT_PREFIX}<name>` for a transport file; an "
                    f"absolute or climbing path can exist while proving nothing about this "
                    f"repository"
                )
        return self

    @model_validator(mode="after")
    def _a_refused_role_is_not_also_held(self) -> "Model":
        # Lowercase FIRST, then compare exactly. Round 6/7 casefolded the intersection so a
        # refused `Fan-Out` could not sit beside a held `fan-out`; round 8's lowercase
        # requirement makes that case unreachable, so the comparison is exact and the rule
        # that does the work is the one that raises.
        for i, r in enumerate(self.roles):
            _require_lowercase(f"roles[{i}]", r)
        for r in self.role_admission:
            _require_lowercase(f"role_admission[{r!r}]", r)
        refused = {r for r, a in self.role_admission.items() if a.verdict == "refused"}
        held = refused & set(self.roles)
        if held:
            raise ValueError(
                f"role(s) {sorted(held)} appear in `roles:` while `role_admission` records "
                f"them as refused — admission governs role eligibility, so a refused role "
                f"cannot be a held one"
            )
        return self


#: The six roles AX21-1's role->model table names, closed and in its order, plus `red`, `qa` and
#: `judge` (R104, 2026-10-14: Sonnet 5.5 writes the RED tests, a separate Copilot session runs QA,
#: Opus 5.5 judges). Held here AND in
#: `scripts/cost_usage_telemetry.ROLES` — two copies, which needs justifying rather than
#: hand-waving: the emitter must not import a pydantic schema to validate one string (it is a
#: leaf module with a deliberately thin import surface), and this module must not import a
#: script (Layer-2 models-only). `tests/test_provider_roles.py` asserts the two are equal, which
#: is this repo's standing answer to a value with two unavoidable homes — one checker, not one
#: import. NOT shared with `ecosystem/routing-table.yaml`'s coarse
#: producer/reviewer/adversarial/fan_out vocabulary: that table routes a role to a CLI, this one
#: keys a measured pass rate, and collapsing them would make one of the two lie.
ROLE_NAMES: frozenset[str] = frozenset(
    {"orchestrate", "plan", "implement", "review", "read", "verify", "red", "qa", "judge",
     "seat-orchestrator", "seat-integrator", "seat-dispatcher", "execute", "rulings"}
)


class ReservedShare(_Contract):
    """A declared share of a weekly budget pool reserved for a role. `value` stays null when the
    operator named none -- a number is never invented, and the reason says why it is unset."""

    pool: StrictStr
    value: Optional[float] = None
    reason: Optional[StrictStr] = None
    decided_by: StrictStr
    decided_on: datetime.date
    evidence: StrictStr

    @model_validator(mode="after")
    def _an_unset_value_carries_a_reason(self) -> "ReservedShare":
        if self.value is None:
            if self.reason is None or not self.reason.strip():
                raise ValueError(
                    "`reserved_share.value` is null with no `reason` -- an unset share must say "
                    "why it is unset"
                )
        elif not 0 < self.value <= 1:
            raise ValueError(
                f"`reserved_share.value` {self.value} is outside (0, 1] -- a share is a fraction"
            )
        return self

    @model_validator(mode="after")
    def _evidence_is_a_repo_relative_path(self) -> "ReservedShare":
        p = PurePosixPath(self.evidence.replace("\\", "/"))
        if p.is_absolute() or ".." in p.parts or re.match(r"^[A-Za-z]:", self.evidence):
            raise ValueError(
                f"reserved_share.evidence `{self.evidence}` is not a repo-relative path"
            )
        return self


def fallback_due(
    usage_pct: Optional[float],
    elapsed_week_pct: Optional[float],
    override: bool = False,
) -> bool:
    """Trigger B': True when the override is set, else when weekly usage is STRICTLY ahead of the
    elapsed share of the week (on pace to exhaust before reset). A missing input is not a trigger."""
    if override:
        return True
    if usage_pct is None or elapsed_week_pct is None:
        return False
    return usage_pct > elapsed_week_pct


def elapsed_week_pct(
    now_epoch: float, resets_at_epoch: float, window_minutes: int = 10080
) -> float:
    """Percent (0..100) of the rate-limit window already elapsed, clamped."""
    window_seconds = window_minutes * 60
    pct = (1 - (resets_at_epoch - now_epoch) / window_seconds) * 100
    return min(100.0, max(0.0, pct))


class FallbackTrigger(_Contract):
    """A declared fallback rule: which roles switch to which provider/model, on what signals."""

    rule: StrictStr
    roles: tuple[StrictStr, ...]
    #: [#1833] draft section 4: a trigger may be a pure wait rule (`bulk_no_max_pool`) with no target provider,
    #: a model MAP (`codex_quota`) instead of one model, and may be disabled (`bprime`). All optional.
    to_provider: Optional[StrictStr] = None
    to_model: Optional[StrictStr] = None
    to_model_map: dict[StrictStr, StrictStr] = {}
    override_flag: Optional[StrictStr] = None
    signals: dict[StrictStr, dict[str, str]] = {}
    enabled: bool = True
    unless: Optional[StrictStr] = None
    on_quota_out: Optional[StrictStr] = None
    note: Optional[StrictStr] = None
    decided_by: StrictStr
    decided_on: datetime.date
    evidence: StrictStr

    @model_validator(mode="after")
    def _signals_have_a_known_status(self) -> "FallbackTrigger":
        for name, signal in self.signals.items():
            if signal.get("status") not in ("AVAILABLE", "GAP"):
                raise ValueError(
                    f"signal `{name}` status {signal.get('status')!r} is not AVAILABLE or GAP"
                )
            if not str(signal.get("detail", "")).strip():
                raise ValueError(f"signal `{name}` carries no `detail`")
        return self

    @model_validator(mode="after")
    def _evidence_is_a_repo_relative_path(self) -> "FallbackTrigger":
        p = PurePosixPath(self.evidence.replace("\\", "/"))
        if p.is_absolute() or ".." in p.parts or re.match(r"^[A-Za-z]:", self.evidence):
            raise ValueError(
                f"fallback trigger evidence `{self.evidence}` is not a repo-relative path"
            )
        return self


class RoleEntry(_Contract):
    """One position in a role's ORDERED fallback list — `[#691]` leg (a).

    Names a PROVIDER, optionally pinning a MODEL. That direction is forced by the clauses
    rather than chosen: AX22-5 says *"the router refuses a PROVIDER not on the repo's list"*
    and AX22-1 measures *"the first ten tasks per PROVIDER"*, so admission and the allowlist are
    both provider-keyed. AX21-1's table mixes the two levels (`Copilot Enterprise` is a
    provider, `Grok 4.6` and `Sonnet` are models), and `model:` is how that is expressed without
    a second vocabulary.
    """

    provider: StrictStr
    #: Pin the exact model, when the role's entry means a specific one rather than "whatever
    #: this provider serves". Must be a registered model id belonging to `provider` — asserted
    #: at the registry level, where both collections are visible.
    model: Optional[StrictStr] = None
    #: This provider's admission verdict FOR THIS ROLE. Reuses `RoleAdmission` verbatim rather
    #: than inventing a parallel grammar: same provenance rules, same `unevaluated` default,
    #: same refusal of a bare verdict.
    #:
    #: ABSENT MEANS `unevaluated`, which means NOT ADMITTED. That equation is the whole of the
    #: Half A / Half B boundary (AX23-2): a provider is listed, addressable and trip-testable
    #: while holding no admission, and only a positive `admitted` verdict with provenance makes
    #: it routable. Silence never reads as permission.
    admission: Optional[RoleAdmission] = None
    #: THIS ENTRY's position is conditional on admission, even where its ROLE is not
    #: admission-gated. AX22-2 is the clause that forces a per-entry flag rather than a
    #: per-role one, and it is worth spelling out because the two look interchangeable until
    #: they are not: *"Codex terra reviews unless Codex produced; then the reviewer is Grok
    #: (AFTER ADMISSION) or Sonnet."* That conditions ONE ENTRY on admission — Grok's — while
    #: leaving the `review` role itself ungated, which is what lets Codex terra remain the
    #: routable reviewer while recorded NOT ADMITTED.
    #:
    #: A role-level gate cannot express that. Gating `review` would refuse Codex too (a
    #: behaviour change no clause asked for); leaving it ungated entirely would route to Grok
    #: before its admission, which AX22-2 forbids in as many words. So the condition lives
    #: where the clause puts it: on the entry.
    requires_admission: bool = False
    #: Why this entry sits where it sits — the DECLARED rationale, which the re-rank may later
    #: override. Optional; an entry with none is exactly as valid.
    note: Optional[StrictStr] = None
    #: LANE-5B-2 Done item 4, entry-level. Set when a currency test has found THIS pinned
    #: `model` is not the newest its provider's CLI currently lists for its tier — recorded
    #: rather than silently re-pinned, because moving an unadmitted position to an
    #: unverified id would manufacture the same kind of drift this field exists to end.
    currency_exception: Optional[CurrencyException] = None
    #: R104 / common rules section 7.6b: `grok -p` returns nothing at `--max-turns 1`, so a
    #: reviewer entry declares the minimum its CLI needs. `None` means no floor is declared.
    max_turns_floor: Optional[int] = None
    #: Where this entry runs: the operator's laptop (`local`) or a Codespace box (`codespace`).
    #: R140: agy is laptop-only, so a role entry for it must say `local`; R151: Codex reviews on the
    #: laptop. `None` means the entry declares no substrate (every pre-1.6.0 entry).
    substrate: Optional[Literal["local", "codespace"]] = None
    #: R138: the entry runs TOGETHER with the other `paired` entries of its role (review is a pair,
    #: Codex terra AND Copilot on every code lane) instead of being a fallback for the one before it.
    paired: bool = False
    #: R177: the entry runs only after a recorded `VENDOR-FAIL: implement ...` of the entry before it.
    vendor_fail_only: bool = False
    #: [#1833] D1: which billing pool this entry spends (`subscription-employer` for Copilot). Free text, except
    #: that `api-credit` is refused on a `subscription+credit` provider (A-2).
    billing_pool: Optional[StrictStr] = None
    #: [#1833] R-5: the entry is routable only for a case the operator approved (Grok). Required on every entry of a
    #: `metered` provider.
    per_case_only: bool = False
    #: [#1844] operator S-1: a SAME-VENDOR entry the router may take as the last review/judge rung, because it runs in a
    #: NEW session with no producer transcript or prose. The router refuses a same-vendor entry WITHOUT this flag.
    isolated_session: bool = False

    @model_validator(mode="after")
    def _max_turns_floor_is_at_least_one(self) -> "RoleEntry":
        if self.max_turns_floor is not None and self.max_turns_floor < 1:
            raise ValueError(
                f"max_turns_floor {self.max_turns_floor} is below 1 — a turn floor under one "
                f"is not a floor"
            )
        return self


class DispatcherPin(_Contract):
    """The model the dispatcher session itself runs on — R22, and NOT a `roles:` entry.

    `roles:` answers "who produces / reviews / reads / etc." for AX21-1's six-role vocabulary;
    the dispatcher session runs `dispatch.py`'s own logic, which is code, not judgment, and R22
    is an explicit override against `roles.orchestrate` (Opus-only, `rerankable: false`), not a
    repoint of it — the two stay independent so aligning this row can never silently move
    orchestrate's own pin. A single pin, not an ordered fallback list: R22 names no fallback.

    Provenance-bearing on the same principle as `RoleAdmission` and `ProviderLicence`: a bare
    `model: claude-sonnet-5` is an assertion, not a record of the ruling that put it there.
    """

    provider: StrictStr
    model: StrictStr
    #: Why this pin exists, or the override it records — free text, same role as `RoleEntry.note`.
    note: Optional[StrictStr] = None
    decided_by: StrictStr
    decided_on: datetime.date
    #: Repo-relative path to the ruling's record. Same shape rule as `RoleAdmission.evidence`.
    evidence: StrictStr

    @model_validator(mode="after")
    def _evidence_is_a_repo_relative_path(self) -> "DispatcherPin":
        p = PurePosixPath(self.evidence.replace("\\", "/"))
        if p.is_absolute() or ".." in p.parts or re.match(r"^[A-Za-z]:", self.evidence):
            raise ValueError(
                f"dispatcher.evidence `{self.evidence}` is not a repo-relative path — an "
                f"absolute or climbing path can exist while proving nothing about this "
                f"repository"
            )
        return self


class Role(_Contract):
    """A role's ordered fallback list plus the two rules that are not re-rankable.

    `[#691]`'s three legs land here: ORDER is `order`'s list position, ADMISSION is each
    entry's `admission`, and LICENCE is the provider's (checked across collections below).
    """

    #: MANDATORY. A role entry whose purpose is not stated is a list of names.
    description: StrictStr
    order: tuple[RoleEntry, ...]
    #: AX21-2's re-rank applies — `provider-registry.yaml` holds the DECLARED order and the
    #: router re-ranks by measured pass rate per cost. `False` pins the declared order against
    #: measurement, and it is used exactly once, for the reason this lane's contract states:
    #: *"orchestration never routes to a cheaper tier, which is the one line of the role table
    #: that is not subject to re-ranking."* A cheap model that happens to score well must not be
    #: promoted into the seat that decides what the expensive ones do.
    rerankable: bool = True
    #: AX22-2 — *"Reviewer != producer, always."* `True` makes the router refuse a candidate
    #: that produced the artifact under review. Set on `review`; the registry encodes the
    #: exclusion, the router enforces it before dispatch, and the tally records both roles.
    excludes_producer: bool = False
    #: The `ecosystem/routing-table.yaml` role this one corresponds to, when one does. NOT a
    #: second routing authority: register ruling Z-G3 A2 places the authoritative role -> CLI
    #: table there, and `ProviderRegistry` asserts agreement rather than competing. `None` where
    #: the correspondence is genuinely absent — writing a lossy mapping to fill the field would
    #: manufacture the drift the link exists to detect.
    routing_table_role: Optional[StrictStr] = None
    #: When set, `order[0].model` must equal it -- the pin is DATA on the row, not schema code.
    pinned_model: Optional[StrictStr] = None
    #: `order` must hold exactly one entry: no fallback exists for this role.
    no_fallback: bool = False
    #: A declared share of a weekly budget pool reserved for this role.
    reserved_share: Optional[ReservedShare] = None
    #: Names another role whose first model must be of a different model family.
    distinct_family_from: Optional[StrictStr] = None
    #: [#1833] R-3: what bulk work does when this role's provider is out of quota. Only `wait` exists: bulk work
    #: never falls back into another provider's subscription pool.
    batch_fallback: Optional[Literal["wait"]] = None

    @model_validator(mode="after")
    def _a_pin_and_a_no_fallback_hold_against_the_order(self) -> "Role":
        if self.pinned_model is not None and (
            not self.order or self.order[0].model != self.pinned_model
        ):
            raise ValueError(
                f"`pinned_model` is `{self.pinned_model}` but order[0] pins "
                f"`{self.order[0].model if self.order else None}`"
            )
        if self.no_fallback and len(self.order) != 1:
            raise ValueError(
                f"`no_fallback` is true but `order` holds {len(self.order)} entries -- exactly "
                f"one is allowed"
            )
        return self

    @model_validator(mode="after")
    def _the_order_is_non_empty_and_names_each_provider_once(self) -> "Role":
        if not self.order:
            raise ValueError(
                "`order` is empty — a role with no candidates is not a fallback list, and an "
                "empty list makes the router's refusal indistinguishable from its success"
            )
        seen: set[str] = set()
        for i, entry in enumerate(self.order):
            _require_lowercase(f"order[{i}].provider", entry.provider)
            if entry.provider in seen:
                raise ValueError(
                    f"provider `{entry.provider}` appears twice in this role's order — a "
                    f"fallback list is a ranking, and a provider holding two positions has no "
                    f"defined rank once the re-rank reorders it"
                )
            seen.add(entry.provider)
        return self


class ProviderRegistry(_Contract):
    """The whole file: `providers:`, `models:`, `roles:`, plus the cross-collection invariants."""

    providers: dict[StrictStr, Provider]
    models: dict[StrictStr, Model]
    #: `[#691]` — the THIRD collection. The row is explicit that this is not a rename of the
    #: per-model `roles:` list: *"today's `roles:` is a set, and a set cannot express a fallback
    #: chain ... a role entry is a third thing, not a field rename."* Both survive and answer
    #: different questions — `Model.roles` is "which roles does this model hold", this is "who
    #: answers for this role, in what order, and who answers when the first is ineligible".
    #:
    #: OPTIONAL, so the registry stays loadable by every pre-`[#691]` consumer.
    roles: dict[StrictStr, Role] = {}
    #: `[#751]` — the units, provenance and cache multipliers the per-model `rates:` blocks are
    #: quoted in. OPTIONAL on the same terms as `roles:` above: a registry carrying no prices at
    #: all stays loadable, which is what every consumer that predates this field needs.
    rate_card: Optional[RateCard] = None
    #: R22 — the model the dispatcher session runs on. OPTIONAL so every pre-R22 registry stays
    #: loadable; NOT part of `roles:` (see `DispatcherPin`'s docstring for why the two vocabularies
    #: stay separate).
    dispatcher: Optional[DispatcherPin] = None
    #: ids the Copilot gateway serves under requested=default, BATCH-E2-0 section 3.
    copilot_gateway_served: list[StrictStr] = []
    #: Declared fallback rules (e.g. B'), keyed by name.
    fallback_triggers: dict[StrictStr, FallbackTrigger] = {}
    #: [#1833] contract R12 / /decide evaluation order. A top-level collection, NOT a `roles:` entry: `ROLE_NAMES`
    #: is pinned by other tests and by `cost_usage_telemetry.ROLES`. Routed under the pseudo-role `evaluate`.
    evaluation: Optional[Role] = None

    def routed_roles(self) -> dict[str, Role]:
        """Every ordered fallback list, `evaluation` included under `evaluate`."""
        out = dict(self.roles)
        if self.evaluation is not None:
            out[EVALUATION_ROLE] = self.evaluation
        return out

    @model_validator(mode="after")
    def _also_served_by_names_declared_providers(self) -> "ProviderRegistry":
        for mid, m in self.models.items():
            for pid in m.also_served_by:
                if pid not in self.providers:
                    raise ValueError(
                        f"model `{mid}` `also_served_by` names undeclared provider `{pid}`")
        return self

    @model_validator(mode="after")
    def _a_fallback_trigger_names_declared_roles_and_provider(self) -> "ProviderRegistry":
        for name, trig in self.fallback_triggers.items():
            declared = set(self.roles) | ({EVALUATION_ROLE} if self.evaluation is not None else set())
            unknown = [r for r in trig.roles if r not in declared]
            if unknown:
                raise ValueError(
                    f"fallback trigger `{name}` names role(s) {unknown} not declared in `roles:`"
                )
            if trig.to_provider is not None and trig.to_provider not in self.providers:
                raise ValueError(
                    f"fallback trigger `{name}` names undeclared provider `{trig.to_provider}`"
                )
        return self

    @model_validator(mode="after")
    def _a_distinct_family_constraint_holds(self) -> "ProviderRegistry":
        for role, spec in self.roles.items():
            other = spec.distinct_family_from
            if other is None:
                continue
            if other not in self.roles:
                raise ValueError(f"role `{role}` distinct_family_from undeclared role `{other}`")
            families = []
            for r in (role, other):
                model_id = self.roles[r].order[0].model
                model = self.models.get(model_id) if model_id else None
                if model is None or not model.family:
                    raise ValueError(
                        f"role `{role}` demands a distinct family from `{other}`, but the first "
                        f"model of `{r}` (`{model_id}`) declares no `family`"
                    )
                families.append(model.family)
            if families[0] == families[1]:
                raise ValueError(
                    f"role `{role}` and role `{other}` both resolve to model family "
                    f"`{families[0]}` -- `distinct_family_from` requires them to differ"
                )
        return self

    @model_validator(mode="after")
    def _the_dispatcher_pin_names_a_declared_provider_and_model(self) -> "ProviderRegistry":
        if self.dispatcher is None:
            return self
        if self.dispatcher.provider not in self.providers:
            raise ValueError(
                f"dispatcher names undeclared provider `{self.dispatcher.provider}`"
            )
        model = self.models.get(self.dispatcher.model)
        if model is None:
            raise ValueError(f"dispatcher pins undeclared model `{self.dispatcher.model}`")
        if model.provider != self.dispatcher.provider:
            raise ValueError(
                f"dispatcher pins model `{self.dispatcher.model}`, which belongs to provider "
                f"`{model.provider}`, not `{self.dispatcher.provider}` — a pin that crosses "
                f"providers makes the allowlist check and the admission check disagree about "
                f"which vendor is being routed to"
            )
        return self

    @model_validator(mode="after")
    def _a_price_without_its_units_is_refused(self) -> "ProviderRegistry":
        """A model may not carry `rates:` while the file carries no `rate_card:`.

        A bare `input: 5.0` is not a price. It is a number whose currency, unit and date live
        nowhere, and a reader that guessed any of the three would produce a dollar figure it
        could not defend — the exact shape of the confident-figure-with-a-hidden-disagreement
        this repo files as a defect class. The two halves are optional SEPARATELY and bound
        TOGETHER: no prices at all is valid, prices without their card is not.

        The converse is deliberately NOT an error. A card with no priced model yet is a
        declaration made ahead of its first use, which is how a rate card is normally filled.
        """
        priced = sorted(m for m, spec in self.models.items() if spec.rates is not None)
        if priced and self.rate_card is None:
            raise ValueError(
                f"model(s) {priced} declare `rates:` while the file declares no `rate_card:` — "
                f"a bare number is not a price: its currency, its unit and the date it was true "
                f"on live on the card, and a consumer that guessed them would report a dollar "
                f"figure it cannot defend"
            )
        return self

    @model_validator(mode="after")
    def _every_role_is_a_known_name(self) -> "ProviderRegistry":
        unknown = sorted(set(self.roles) - ROLE_NAMES)
        if unknown:
            raise ValueError(
                f"role(s) {unknown} are not in the AX21-1 vocabulary {sorted(ROLE_NAMES)} — a "
                f"role is a lookup key the router and the re-rank both match raw, so an "
                f"invented name resolves nowhere while looking like configuration"
            )
        return self

    @model_validator(mode="after")
    def _implement_first_entry_is_admitted_and_later_claude_is_vendor_fail_only(self) -> "ProviderRegistry":
        spec = self.roles.get("implement")
        if spec is None:
            return self
        first = spec.order[0]
        if first.admission is None or first.admission.verdict != "admitted":
            raise ValueError(
                f"role `implement` order[0] is provider `{first.provider}` without an `admitted` "
                f"verdict — R11: the first implement entry must be admitted; the others run only "
                f"after a recorded VENDOR-FAIL"
            )
        for i, entry in enumerate(spec.order):
            if i > 0 and entry.provider == "anthropic" and not entry.vendor_fail_only:
                raise ValueError(
                    f"role `implement` order[{i}] is anthropic without `vendor_fail_only: true` — "
                    f"R11: a later Claude implementer runs only after a recorded VENDOR-FAIL"
                )
        return self

    @model_validator(mode="after")
    def _vendor_fail_only_is_never_on_the_first_entry(self) -> "ProviderRegistry":
        for role, spec in self.roles.items():
            if spec.order and spec.order[0].vendor_fail_only:
                raise ValueError(
                    f"role `{role}` order[0] carries `vendor_fail_only: true` — a vendor-fail fallback "
                    f"needs an entry before it to fail"
                )
        return self

    @model_validator(mode="after")
    def _every_role_entry_names_a_declared_provider_and_model(self) -> "ProviderRegistry":
        for role, spec in self.routed_roles().items():
            for i, entry in enumerate(spec.order):
                if entry.provider not in self.providers:
                    raise ValueError(
                        f"role `{role}` order[{i}] names undeclared provider "
                        f"`{entry.provider}`"
                    )
                if entry.model is None:
                    continue
                model = self.models.get(entry.model)
                if model is None:
                    raise ValueError(
                        f"role `{role}` order[{i}] pins undeclared model `{entry.model}`"
                    )
                if model.provider != entry.provider and entry.provider not in model.also_served_by:
                    raise ValueError(
                        f"role `{role}` order[{i}] pins model `{entry.model}`, which belongs "
                        f"to provider `{model.provider}`, not `{entry.provider}` — a pin that "
                        f"crosses providers makes the allowlist check and the admission check "
                        f"disagree about which vendor is being routed to"
                    )
        return self

    @model_validator(mode="after")
    def _an_admitted_entry_is_not_refused_at_its_model(self) -> "ProviderRegistry":
        """The two admission records cannot contradict each other.

        `Model.role_admission` already carries per-model verdicts (grok-4.6's refused `fan-out`
        is the live instance). A role entry pinning that model must not claim `admitted` for a
        role the model row records as `refused` — otherwise the same fact reads two ways
        depending on which collection a consumer happened to open, which is the drift the whole
        registry exists to end.
        """
        for role, spec in self.routed_roles().items():
            for i, entry in enumerate(spec.order):
                if entry.admission is None or entry.admission.verdict != "admitted":
                    continue
                if entry.model is None:
                    continue
                model_verdict = self.models[entry.model].role_admission.get(role)
                if model_verdict is not None and model_verdict.verdict == "refused":
                    raise ValueError(
                        f"role `{role}` order[{i}] records `{entry.model}` as admitted while "
                        f"its model row records role `{role}` as refused — one fact, two "
                        f"answers, depending on which collection the reader opened"
                    )
        return self

    @model_validator(mode="after")
    def _an_admitted_entry_has_a_permitting_licence(self) -> "ProviderRegistry":
        """`[#691]` leg (c), in its Done-when's own words: *"only providers that passed intake
        #75's seeded-defect admission bar, AND WHOSE LICENCE PERMITS THE USE, may appear on
        it."*

        Enforced on ADMISSION rather than on LISTING, and the distinction is load-bearing. A
        provider must be LISTABLE while unlicensed, because this lane's contract requires the
        four non-Claude entries to be present and recorded NOT ADMITTED precisely so the
        router's refusals can be trip-tested against them. What the Done-when is protecting is
        that nothing becomes ROUTABLE without a licence — and `admitted` is the only state that
        makes an entry routable. Listed is not eligible.
        """
        for role, spec in self.routed_roles().items():
            for i, entry in enumerate(spec.order):
                if entry.admission is None or entry.admission.verdict != "admitted":
                    continue
                licence = self.providers[entry.provider].licence
                status = licence.status if licence is not None else "unknown"
                if status != "permitted":
                    raise ValueError(
                        f"role `{role}` order[{i}] admits provider `{entry.provider}` whose "
                        f"licence is `{status}` — a provider may be LISTED under any licence "
                        f"(that is what makes the router's refusal trip-testable), but only a "
                        f"`permitted` one may be admitted, which is the state that makes it "
                        f"routable"
                    )
        return self

    def licence_of(self, provider_id: str) -> Licence:
        """This provider's licence status, with an ABSENT row reading as `unknown`.

        The default is the conservative one on purpose: absence must never resolve to
        `permitted`, because the whole point of the field is that an unruled licence is not a
        permission.
        """
        provider = self.providers[provider_id]
        return provider.licence.status if provider.licence is not None else "unknown"

    @model_validator(mode="after")
    def _billing_constrains_what_a_role_entry_may_do(self) -> "ProviderRegistry":
        """[#1833] R-5 and A-2, enforced where both collections are visible.

        * every role entry of a `metered` provider is `per_case_only` -- Grok is never a standing route;
        * no role entry of a `subscription+credit` provider spends the `api-credit` pool -- A-2: nothing routes
          to the credit pool without a separate ruling.
        """
        for role, spec in self.routed_roles().items():
            for i, entry in enumerate(spec.order):
                billing = self.providers[entry.provider].billing if entry.provider in self.providers else None
                if billing is None:
                    continue
                if billing.billing_class == "metered" and not entry.per_case_only:
                    raise ValueError(
                        f"role `{role}` order[{i}] is metered provider `{entry.provider}` without "
                        f"`per_case_only: true` -- a metered provider is routable for an approved case only")
                if billing.billing_class == "subscription+credit" and entry.billing_pool == API_CREDIT_POOL:
                    raise ValueError(
                        f"role `{role}` order[{i}] spends billing_pool `{API_CREDIT_POOL}` of provider "
                        f"`{entry.provider}` -- A-2: no role routes to the API-credit pool without a separate ruling")
        return self

    @model_validator(mode="after")
    def _evaluation_never_routes_to_claude(self) -> "ProviderRegistry":
        """Operator S-1 item 7: S-1's isolated-Claude rung is written for review and judge; evaluation keeps
        "never Claude"."""
        if self.evaluation is None:
            return self
        for i, entry in enumerate(self.evaluation.order):
            if entry.provider == "anthropic":
                raise ValueError(
                    f"evaluation order[{i}] is provider `anthropic` -- contract evaluation and /decide never "
                    f"route to Claude (RATIFICATION-2026-11-01-ROUTING-COST-S1.md item 7)")
        return self

    @model_validator(mode="after")
    def _every_model_names_a_declared_provider(self) -> "ProviderRegistry":
        unknown = {
            mid: m.provider for mid, m in self.models.items() if m.provider not in self.providers
        }
        if unknown:
            rows = ", ".join(f"`{mid}` -> `{pid}`" for mid, pid in sorted(unknown.items()))
            raise ValueError(f"model(s) name an undeclared provider: {rows}")
        return self

    @model_validator(mode="after")
    def _a_changelog_tool_key_resolves_to_one_provider(self) -> "ProviderRegistry":
        """terra HIGH round 5, 2026-08-23 — a SILENT overwrite, which is why it needs a rule.

        `provider_registry.version_commands()` and `changelog_source_urls()` both build a
        dict keyed by `changelog_tool_key`, so two providers sharing a key means the second
        silently replaces the first: the SessionStart sentinel would probe the wrong CLI for
        that tool while `check_s8_tool_versions` passed clean, because the key it looks up
        still exists.
        """
        # Compared EXACTLY, and that is sufficient rather than lax: `_lookup_keys_are_lowercase`
        # runs on each Provider before this cross-provider validator, so `CODEX` never reaches
        # here. Round 6 casefolded this comparison to catch `codex`/`CODEX`; round 8 replaced
        # that with the stronger lowercase requirement, which makes a casefold provably a
        # no-op. A no-op branch that looks like a rule is the vacuous-gate class this repo
        # refuses, so it is removed rather than kept as decoration.
        seen: dict[str, str] = {}
        for pid, p in self.providers.items():
            key = p.changelog_tool_key
            if key is None:
                continue
            if key in seen:
                raise ValueError(
                    f"changelog tool key `{key}` is claimed by both `{seen[key]}` and "
                    f"`{pid}` — the key indexes a dict, so a repeat silently drops one "
                    f"provider's version probe and changelog source"
                )
            seen[key] = pid
        return self

    @model_validator(mode="after")
    def _a_council_alias_resolves_to_one_provider(self) -> "ProviderRegistry":
        # Exact, for the same reason as the changelog key above: the lowercase requirement
        # runs first, so case variants cannot reach this comparison.
        seen: dict[str, str] = {}
        for pid, p in self.providers.items():
            if p.council_alias is None:
                continue
            if p.council_alias in seen:
                raise ValueError(
                    f"council alias `{p.council_alias}` is claimed by both "
                    f"`{seen[p.council_alias]}` and `{pid}` — an alias resolves to one "
                    f"provider or the roster check cannot say which"
                )
            seen[p.council_alias] = pid
        return self


__all__ = [
    "EVIDENCE_TRANSPORT_PREFIX",
    "ROLE_NAMES",
    "SCHEMA_VERSION",
    "CurrencyException",
    "DispatcherPin",
    "FallbackTrigger",
    "Licence",
    "Model",
    "ModelCurrency",
    "Pin",
    "Provider",
    "ProviderLicence",
    "ProviderRegistry",
    "ReservedShare",
    "Role",
    "RoleAdmission",
    "RoleEntry",
    "Verdict",
    "elapsed_week_pct",
    "fallback_due",
]
