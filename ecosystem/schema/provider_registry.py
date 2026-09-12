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
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, StrictStr, model_validator

#: 1.1.0 — `[#691]` adds the THIRD collection (`roles:`: ordered fallback lists, per-entry
#: admission, the reviewer-not-producer flag) and the per-provider `licence:` block. MINOR, not
#: major: both additions are optional, so every pre-`[#691]` registry still validates unchanged.
#: Not a member of `validate_reconciliation._SPEC_REGISTRY` (which registers `handoff-process`
#: and `prompt-template` only), so this bump carries no reconciliation obligation — checked
#: rather than assumed.
SCHEMA_VERSION = "1.1.0"

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


class Provider(_Contract):
    """A vendor, the CLI that reaches it, and the host-side config that pins it."""

    display_name: StrictStr
    #: `[#691]` leg (c). OPTIONAL, and its absence means exactly `unknown` — see
    #: `ProviderRegistry.licence_of`. Optionality is deliberate rather than lax: making it
    #: required would have forced a licence verdict onto all seven existing rows in the same
    #: commit that introduced the field, which is how a registry acquires six fabricated
    #: values and one real one.
    licence: Optional[ProviderLicence] = None
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
    pinned_at: tuple[Pin, ...] = ()

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


#: The six roles AX21-1's role->model table names, closed and in its order. Held here AND in
#: `scripts/cost_usage_telemetry.ROLES` — two copies, which needs justifying rather than
#: hand-waving: the emitter must not import a pydantic schema to validate one string (it is a
#: leaf module with a deliberately thin import surface), and this module must not import a
#: script (Layer-2 models-only). `tests/test_provider_roles.py` asserts the two are equal, which
#: is this repo's standing answer to a value with two unavoidable homes — one checker, not one
#: import. NOT shared with `ecosystem/routing-table.yaml`'s coarse
#: producer/reviewer/adversarial/fan_out vocabulary: that table routes a role to a CLI, this one
#: keys a measured pass rate, and collapsing them would make one of the two lie.
ROLE_NAMES: frozenset[str] = frozenset(
    {"orchestrate", "plan", "implement", "review", "read", "verify"}
)


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
    #: Why this entry sits where it sits — the DECLARED rationale, which the re-rank may later
    #: override. Optional; an entry with none is exactly as valid.
    note: Optional[StrictStr] = None


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
    def _every_role_entry_names_a_declared_provider_and_model(self) -> "ProviderRegistry":
        for role, spec in self.roles.items():
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
                if model.provider != entry.provider:
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
        for role, spec in self.roles.items():
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
        for role, spec in self.roles.items():
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
    "ROLE_NAMES",
    "SCHEMA_VERSION",
    "Licence",
    "Model",
    "Pin",
    "Provider",
    "ProviderLicence",
    "ProviderRegistry",
    "Role",
    "RoleAdmission",
    "RoleEntry",
    "Verdict",
]
