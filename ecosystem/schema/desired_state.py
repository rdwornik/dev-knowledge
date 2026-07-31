"""ADR-109 fleet desired-state contract v1 — pydantic models ([#382] W2).

Models ONLY: no file I/O, no fleet reads, no execution (Layer-2, ADR-28/36). The
loader (scripts/, W3) parses live registry sources into these types; the report
(W4) renders divergence from a loaded model. Spec: ADR-109 §3 (the seven ADR-107
§5 findings as constraints) + §7 (the sol-vs-CC adjudicated shape).

Constraint map, in-code:
- finding 1: every identity is StrictStr, opaque, byte-exact — never coerced.
- finding 2: write-path policy is a closed enum carried as data (SourceRecord).
- finding 4: raw values ride beside parsed ones (LifecycleAssertion.raw_value,
  Edge.raw, TaskRow.depends_on carried verbatim, Probe extra params preserved).
- finding 5: lineage direction is validated (ResidueManifest: a source-of-truth
  surface declares `generates`, never `source` — the post-flip ADR-107 amendment).
- finding 7: AllocationRule.concurrent_prevention structurally cannot claim
  prevention ([#429] owns it).

Directory authorization (F2): `ecosystem/schema/` is a NEW directory approved by
the operator via the architect at the 2026-07-31 plan review (ADR-109 §8).
"""

from __future__ import annotations

import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, model_validator

SCHEMA_VERSION = "1.0.0"


class _Contract(BaseModel):
    """Contract-native type: we own the grammar — unknown keys are a spec error."""

    model_config = ConfigDict(frozen=True, extra="forbid")


def _deep_freeze(value: object) -> object:
    """Lists become tuples recursively so frozen extras cannot be mutated in place
    (terra H6). Dicts are left as dicts — a recorded v1 limit: dict extras are
    read-only by convention until the loader normalizes them (W3)."""
    if isinstance(value, list):
        return tuple(_deep_freeze(v) for v in value)
    if isinstance(value, dict):
        return {k: _deep_freeze(v) for k, v in value.items()}
    return value


class _SourceMirror(BaseModel):
    """Source-mirroring type: unknown keys survive our read path (finding 2 applied
    to ourselves — forward-compatible with source growth). Values are preserved as
    PARSED data, not source bytes: byte-exact round-trip is the loader's obligation
    at the per-source envelope level (ADR-109 §7 D4), never per-row."""

    model_config = ConfigDict(frozen=True, extra="allow")

    @model_validator(mode="before")
    @classmethod
    def _freeze_extra_containers(cls, data: object) -> object:
        if isinstance(data, dict):
            return {k: _deep_freeze(v) for k, v in data.items()}
        return data


# --- enums (closed vocabularies; every value witnessed on disk or ruled in ADR-109) -----

class LifecycleStage(StrEnum):
    source = "source"
    unonboarded = "unonboarded"
    floor_only = "floor_only"
    full = "full"


class Semantics(StrEnum):
    """D2: a lifecycle statement is DESIRED (a ruling), OBSERVED (state), or a
    ROLE classification — conflating them is the C3/G4 defect."""

    desired = "desired"
    observed = "observed"
    role_classification = "role-classification"


class SourceSurface(StrEnum):
    registry = "registry"
    parity = "parity"
    onboarding_ruling = "onboarding-ruling"
    deployed_version = "deployed-version"


class Role(StrEnum):
    hub = "hub"
    consumer = "consumer"
    pre_deploy = "pre-deploy"


class SurfaceKind(StrEnum):
    path = "path"
    gitignore_effect = "gitignore-effect"
    command = "command"
    settings_hook_block = "settings-hook-block"
    precommit_hook = "precommit-hook"
    doc_marker = "doc-marker"
    tombstone_join = "tombstone-join"
    claude_subtree = "claude-subtree"
    roster = "roster"


class Posture(StrEnum):
    MUST = "MUST"
    SHOULD = "SHOULD"
    LOCAL = "LOCAL"
    IGNORE = "IGNORE"
    INVERSE = "INVERSE"
    TOMBSTONE = "TOMBSTONE"


class SelectorKind(StrEnum):
    role = "role"
    repository = "repository"


class ProbeType(StrEnum):
    dir_tracked = "dir_tracked"
    path_tracked = "path_tracked"
    check_ignore = "check_ignore"
    file_contains = "file_contains"
    command_present = "command_present"
    dir_exists = "dir_exists"
    precommit_hook = "precommit_hook"
    settings_hook = "settings_hook"
    file_exists = "file_exists"
    precommit_remote = "precommit_remote"
    glob_tracked = "glob_tracked"
    plugin_enabled = "plugin_enabled"
    settings_local_blocks = "settings_local_blocks"
    ruff_config_form = "ruff_config_form"
    claude_subtrees = "claude_subtrees"
    commands_roster = "commands_roster"


class OwnershipValue(StrEnum):
    methodology_generic = "methodology-generic"
    conditional = "conditional"
    project = "project"


class DivergenceKind(StrEnum):
    parity_waiver = "parity-waiver"
    audit_disposition = "audit-disposition"
    gate_rev_ahead = "gate-rev-ahead"


class DivergenceEffect(StrEnum):
    waive = "waive"
    suppress_warning = "suppress-warning"
    declare_only = "declare-only"


class EdgeKind(StrEnum):
    doc2doc = "doc2doc"
    doc2file = "doc2file"
    doc2code = "doc2code"
    hook = "hook"
    skill = "skill"
    task_dep = "task-dep"
    carrier = "carrier"
    region = "region"


class IdSpace(StrEnum):
    """The nine witnessed identity spaces (dossier G9) + path."""

    spec_id = "spec-id"
    rule_id = "rule-id"
    check_name = "check-name"
    surface_id = "surface-id"
    hook_id = "hook-id"
    region_id = "region-id"
    task_id = "task-id"
    component_id = "component-id"
    python_symbol = "python-symbol"
    path = "path"


class Enforcement(StrEnum):
    """ADR-109 §6 normative tokens (terra H7/grok H4 — code had drifted to
    fail-gating/warn-only; the ADR vocabulary wins)."""

    fail = "fail"
    warn = "warn"
    never_gates = "never-gates"
    inert = "inert"


class CrosswalkRelation(StrEnum):
    same_organ = "same-organ"
    overlaps = "overlaps"
    implements = "implements"
    probes = "probes"
    carries = "carries"


class RefKind(StrEnum):
    git_tag = "git-tag"
    git_commit = "git-commit"
    backlog = "backlog"
    adr = "adr"
    audit = "audit"  # live on disk (parity-surfaces ownership provenance) — grok C1
    census = "census"
    file = "file"
    ruling = "ruling"
    document = "document"
    operator_ruling = "operator-ruling"


class WritePolicy(StrEnum):
    round_trip = "round-trip-unknown-byte-stable"
    barred = "third-party-writers-barred"


class SourceRole(StrEnum):
    declarative = "declarative"
    derived = "derived"
    state = "state"
    ruling = "ruling"
    consumer_owned = "consumer-owned"


class ManifestRole(StrEnum):
    source_of_truth = "source-of-truth"
    derived = "derived"


# --- provenance (one grammar for the five observed "why" shapes, dossier §i.3) ----------

class ProvenanceRef(_Contract):
    kind: RefKind
    ref: StrictStr
    repo: StrictStr | None = None
    actor: StrictStr | None = None
    # dates are PARSED scalars by design (ISO-string coercion accepted) — identity
    # fields are the opaque-verbatim class, dates are not (grok L2 disposition)
    date: datetime.date | None = None


class Provenance(_Contract):
    reason: StrictStr
    refs: tuple[ProvenanceRef, ...] = ()
    ruled_by: StrictStr | None = None
    ruled_date: datetime.date | None = None
    review_date: datetime.date | None = None
    raw: StrictStr | None = None  # byte-exact legacy free-text block, when importing one


# --- observed state (the R3 trio; null semantics per deployed-versions.yaml:18-20) ------

class DeployedState(_Contract):
    version: StrictStr | None = None
    deployed_date: StrictStr | None = None  # raw scalar, not parsed — preserve-verbatim
    source_tag: StrictStr | None = None
    consumer_pin_raw: StrictStr | None = None  # hub-side knowledge only (ADR-109 §8)
    pin_observation_status: Literal["observed", "unavailable", "not-applicable"] = "unavailable"

    @model_validator(mode="after")
    def _consistent_nullness(self) -> DeployedState:
        if (self.version is None) != (self.source_tag is None):
            raise ValueError("DeployedState: version and source_tag are both set or both null "
                             "(a value cannot precede its release — deployed-versions.yaml contract)")
        return self


# --- lifecycle (D2: lossless assertions; role is NOT lifecycle-bearing) -----------------

class LifecycleAssertion(_Contract):
    source_surface: SourceSurface
    semantics: Semantics
    raw_value: StrictStr  # verbatim, incl. free prose like "registered · unonboarded (floor-carrying)"
    mapped_stage: LifecycleStage
    provenance: Provenance | None = None


def lifecycle_from_parity_role(role: str) -> LifecycleStage | None:
    """D2 amendment: parity `role` does not map into lifecycle — `consumer`/`pre-deploy`
    carry no deployment evidence (the over-claim class). Sole exception: hub → source.
    An unknown token is an error, never a silent None (grok L3)."""
    if role not in {r.value for r in Role}:
        raise ValueError(f"unknown parity role: {role!r}")
    return LifecycleStage.source if role == Role.hub else None


class Repo(_Contract):
    id: StrictStr  # opaque byte-exact directory name — THE join key (dossier C6)
    path: StrictStr | None = None
    purpose: StrictStr | None = None
    role: Role | None = None
    registered: StrictBool = False
    floor_carrying: StrictBool = False
    assertions: tuple[LifecycleAssertion, ...] = ()
    deployed: DeployedState | None = None
    membership: frozenset[StrictStr] = frozenset()  # which registries list this repo — C1 as data
    status_raw: tuple[tuple[StrictStr, StrictStr], ...] = ()  # (source, verbatim status) pairs


# --- surfaces (the parity-surfaces row grammar, absorbed; ADR-109 §2 item 3) ------------

class Ownership(_Contract):
    value: OwnershipValue
    reason: StrictStr = Field(min_length=1)
    provenance: tuple[ProvenanceRef, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _reason_not_blank(self) -> Ownership:
        if not self.reason.strip():
            raise ValueError("ownership reason must be non-blank (parity grammar — grok H3)")
        return self


class ApplicabilityRule(_Contract):
    """D5: the model form of the role-or-repo-keyed `tier` map — the loader maps the
    file grammar here mechanically (repo-id overrides role); the file is unchanged in v1."""

    selector_kind: SelectorKind
    selector: StrictStr
    posture: Posture
    provenance: Provenance | None = None


class Probe(_SourceMirror):
    """Typed discriminator + per-type params preserved raw (16 grammars; discriminated
    nested models deferred until a consumer needs them — ADR-109 §7, sol OP5)."""

    type: ProbeType


class Join(_SourceMirror):
    """Disk shape: `join: {manifest_component: <id>}` (grok C2)."""

    manifest_component: StrictStr


class PendingMigration(_SourceMirror):
    """Disk shape: `pending_migration: {to, ticket}` (grok C2)."""

    to: StrictStr | None = None
    ticket: StrictStr | None = None


class Surface(_Contract):
    id: StrictStr
    kind: SurfaceKind
    applicability: tuple[ApplicabilityRule, ...]
    probe: Probe
    ownership: Ownership  # mandatory — loader refuses absence (parity contract :63-64)
    tier_raw: StrictStr | None = None  # the verbatim role/repo-keyed tier block (D5)
    waivable: StrictBool | None = None
    waiver_component: StrictStr | None = None
    local_names: tuple[tuple[StrictStr, StrictStr], ...] = ()  # (repo id, local name) pairs
    declared_by: StrictStr | None = None
    declared_divergence: tuple[tuple[StrictStr, StrictStr], ...] = ()  # (repo id, expected-text)
    pending_migration: PendingMigration | None = None
    join: Join | None = None
    gate_rev_ahead: tuple[tuple[StrictStr, StrictStr], ...] = ()  # (repo id, concern_id) refs (D6)


# --- divergences (C7/G14: two suppression vocabularies + gate_rev_ahead, ONE type) ------

class DeclaredDivergence(_Contract):
    kind: DivergenceKind
    concern_id: StrictStr  # the one-per-concern join key
    effect: DivergenceEffect
    provenance: Provenance
    component: StrictStr | None = None  # .methodology.yaml vocabulary
    organ: StrictStr | None = None  # disposition-register vocabulary
    match: StrictStr | None = None  # evidence-substring (disposition-register)
    gate_tag_raw: StrictStr | None = None
    auto_clearable_by: StrictStr | None = None
    review_date: datetime.date | None = None

    @property
    def waives_must(self) -> bool:
        """No mechanism in this type waives a parity MUST (ADR-102; MUST rows are
        non-waivable by contract) — structurally False, not policy-False."""
        return False

    @model_validator(mode="after")
    def _kind_effect_mapping(self) -> DeclaredDivergence:
        """The full kind→effect map (terra H5): each mechanism has exactly one effect —
        parity-waiver waives, audit-disposition suppresses, gate-rev-ahead declares."""
        expected = {DivergenceKind.parity_waiver: DivergenceEffect.waive,
                    DivergenceKind.audit_disposition: DivergenceEffect.suppress_warning,
                    DivergenceKind.gate_rev_ahead: DivergenceEffect.declare_only}
        if self.effect != expected[self.kind]:
            raise ValueError(f"{self.kind.value} requires effect {expected[self.kind].value!r}, "
                             f"got {self.effect.value!r}")
        if self.kind == DivergenceKind.gate_rev_ahead and self.gate_tag_raw is None:
            raise ValueError("gate-rev-ahead requires gate_tag_raw")
        return self


# --- edges + crosswalk (G9: the id-space crosswalk is data, never inference) ------------

class EntityRef(_Contract):
    id_space: IdSpace
    id: StrictStr
    repo: StrictStr | None = None
    path: StrictStr | None = None
    source_location: StrictStr | None = None


class Edge(_Contract):
    id: StrictStr | None = None  # optional opaque edge identity (terra H1)
    kind: EdgeKind
    src: EntityRef
    dst: EntityRef
    enforcement: Enforcement
    raw: StrictStr | None = None  # the verbatim declaration (finding 4)
    declared_at: StrictStr | None = None  # file[:line]
    provenance: Provenance | None = None


class Crosswalk(_Contract):
    organ: StrictStr
    members: tuple[EntityRef, ...] = Field(min_length=2)
    relation: CrosswalkRelation
    provenance: Provenance | None = None


# --- allocation (finding 7: honesty is structural) --------------------------------------

class AllocationRule(_Contract):
    namespace: StrictStr
    ledger_surface: StrictStr
    next_free_rule: StrictStr
    closed_ids_remain_allocated: Literal[True]
    retirement_policy: Literal["retain-allocation-record"]
    duplicate_id_policy: Literal["refuse"]
    collision_detection_stage: Literal["validation", "merge-gate"]
    # v1 permits ONLY not-provided (terra H4): "externally-coordinated" is a
    # prevention-shaped claim with no organ behind it — widening this Literal is
    # a schema-version change gated on [#429] delivering the organ.
    concurrent_prevention: Literal["not-provided"]


# --- document rows + residue (findings 3/5/6; S3d composability) ------------------------

class TaskRow(_SourceMirror):
    id: StrictStr  # opaque "[#N]", byte-exact — never a normalized integer
    body: StrictStr  # verbatim
    status: StrictStr | None = None
    priority: StrictStr | None = None
    size: StrictStr | None = None
    theme: StrictStr | None = None
    story: StrictStr | None = None
    serialize_group: StrictStr | None = None
    generates: StrictStr | None = None
    depends_on: StrictStr | None = None  # RAW: "382" and "#382" are different signals ([#424])


class ResidueManifest(_Contract):
    role: ManifestRole
    generates: StrictStr | None = None
    generated_sha256: StrictStr | None = None
    source: StrictStr | None = None
    source_sha256: StrictStr | None = None
    schema_raw: StrictStr | None = None
    row_order: tuple[StrictStr, ...] = ()
    non_member_residue: tuple[StrictStr, ...] = ()

    @model_validator(mode="after")
    def _direction_honesty(self) -> ResidueManifest:
        if self.role == ManifestRole.source_of_truth:
            if self.generates is None or self.generated_sha256 is None:
                raise ValueError("source-of-truth manifest declares generates + generated_sha256 "
                                 "(ADR-107 amendment: the tree IS source)")
            if self.source is not None or self.source_sha256 is not None:
                raise ValueError("source-of-truth manifest must not claim source/source_sha256 "
                                 "(false in the same breath — ADR-107 amendment)")
        else:
            if self.source is None or self.source_sha256 is None:
                raise ValueError("derived manifest requires the source + source_sha256 pair "
                                 "(finding 6 — terra H3: half a provenance pair is none)")
            if self.generates is not None:
                raise ValueError("derived manifest must not claim generates")
        return self


# --- components + lineage (terra CRITICAL: ADR-109 §7 D1/D3 + finding 5) ----------------

class ComponentKind(StrEnum):
    organ = "organ"
    hook = "hook"
    command = "command"
    skill = "skill"
    doc_shape = "doc-shape"
    config = "config"
    library = "library"
    template = "template"
    carrier = "carrier"


class ComponentOwnership(StrEnum):
    hub = "hub"
    repo = "repo"
    conditional = "conditional"


class DesiredPresence(StrEnum):
    present = "present"
    absent = "absent"
    local = "local"
    ignored = "ignored"


class ComponentSpec(_Contract):
    """The §E query spine ("which repos have component X"). Population bound (D3):
    components derive from existing declarations (manifest, parity) — never a new
    hand-authored registry."""

    id: StrictStr
    kind: ComponentKind
    ownership: ComponentOwnership
    description: StrictStr | None = None
    version_raw: StrictStr | None = None
    provenance: Provenance | None = None


class ComponentAssignment(_Contract):
    repo_id: StrictStr
    component_id: StrictStr
    desired_presence: DesiredPresence
    desired_version_raw: StrictStr | None = None
    provenance: Provenance | None = None


class LineageMode(StrEnum):
    derived_from = "derived-from"
    generates = "generates"


class Lineage(_Contract):
    """Finding 5 generalized: every derived/generated surface relation is a typed,
    directed row — `derived-from` (with source semantics) or `generates` (post-flip)."""

    mode: LineageMode
    from_surface: StrictStr
    to_surface: StrictStr
    residue_manifest_id: StrictStr | None = None
    provenance: Provenance | None = None


# --- source registry metadata (finding 2 as data) ---------------------------------------

class SourceRecord(_Contract):
    path: StrictStr
    role: SourceRole
    write_policy: WritePolicy
    parsed_note: StrictStr | None = None


class ManifestCut(_Contract):
    """Minimal manifest anchors (D8) — makes G11's declared-vs-deployed gap computable."""

    methodology_version: StrictStr
    source_tag: StrictStr

    @model_validator(mode="after")
    def _anchors_agree(self) -> ManifestCut:
        if self.source_tag != f"v{self.methodology_version}":
            raise ValueError("manifest anchors disagree: source_tag must be 'v' + methodology_version")
        return self


# --- observed root (W3 loader target; reclassified index.yaml — ADR-109 §2 item 2) ------

class AuditFinding(_SourceMirror):
    check_name: StrictStr
    evidence: StrictStr
    status: StrictStr


class RepoObservation(_Contract):
    repo_id: StrictStr
    last_audit: StrictStr | None = None  # raw scalar
    findings: tuple[AuditFinding, ...] = ()


class ObservedFleetState(_Contract):
    generated_raw: StrictStr | None = None  # index.yaml stamp, surfaced never hidden (C8)
    repos: tuple[RepoObservation, ...] = ()


# --- desired root -----------------------------------------------------------------------

class FleetDesiredState(_Contract):
    schema_version: Literal["1.0.0"]
    repos: tuple[Repo, ...] = ()
    surfaces: tuple[Surface, ...] = ()
    edges: tuple[Edge, ...] = ()
    crosswalks: tuple[Crosswalk, ...] = ()
    divergences: tuple[DeclaredDivergence, ...] = ()
    allocation_rules: tuple[AllocationRule, ...] = ()
    components: tuple[ComponentSpec, ...] = ()
    assignments: tuple[ComponentAssignment, ...] = ()
    lineage: tuple[Lineage, ...] = ()
    task_rows: tuple[TaskRow, ...] = ()
    residue_manifests: tuple[ResidueManifest, ...] = ()
    manifest: ManifestCut | None = None
    # Default-empty by design (terra H2 disposition): per-source write-policy
    # COVERAGE is the loader's obligation — it alone knows which sources it read (W3).
    sources: tuple[SourceRecord, ...] = ()

    @model_validator(mode="after")
    def _one_per_concern(self) -> FleetDesiredState:
        seen: set[tuple[str, str]] = set()
        for d in self.divergences:
            key = (d.kind.value, d.concern_id)
            if key in seen:
                raise ValueError(f"one-per-concern violated: duplicate {key[0]} declaration "
                                 f"for concern '{key[1]}' (disposition-register grammar)")
            seen.add(key)
        return self

    @model_validator(mode="after")
    def _repo_ids_unique(self) -> FleetDesiredState:
        ids = [r.id for r in self.repos]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate repo id in fleet")
        return self

    @model_validator(mode="after")
    def _gate_rev_refs_resolve(self) -> FleetDesiredState:
        """grok M6: a Surface gate_rev_ahead reference is a pointer into divergences —
        dangling means the only live payload (tag + reason + provenance) is lost."""
        declared = {d.concern_id for d in self.divergences
                    if d.kind == DivergenceKind.gate_rev_ahead}
        for s in self.surfaces:
            for _repo, concern in s.gate_rev_ahead:
                if concern not in declared:
                    raise ValueError(f"surface {s.id!r} references gate-rev-ahead concern "
                                     f"{concern!r} with no matching DeclaredDivergence")
        return self


class FleetModel(_Contract):
    """D1: the composition view — desired and observed stay typed apart and meet
    only here; the divergence report (W4) consumes this, never a blended type."""

    desired: FleetDesiredState
    observed: ObservedFleetState
