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

SCHEMA_VERSION = "1.0.0"

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


class Provider(_Contract):
    """A vendor, the CLI that reaches it, and the host-side config that pins it."""

    display_name: StrictStr
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


class ProviderRegistry(_Contract):
    """The whole file: `providers:` and `models:`, plus the cross-collection invariants."""

    providers: dict[StrictStr, Provider]
    models: dict[StrictStr, Model]

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
    "SCHEMA_VERSION",
    "Model",
    "Pin",
    "Provider",
    "ProviderRegistry",
    "RoleAdmission",
    "Verdict",
]
