"""ADR-109 desired-state loader ([#382] W3) — the seven live registry sources → ONE
validated FleetModel.

READ-ONLY against the fleet (Layer-2, ADR-28/36): this module opens files for
reading only and writes nothing. Membership is the UNION of what the sources list;
disagreements RESOLVE toward ecosystem/deployed-versions.yaml (the durable record,
per registry.md's own derivation rule) and are carried as model FACTS — a
contradiction between sources is data, never a load error. The sanctioned
corp-monorepo corpus-vs-gate divergence loads as a gate-rev-ahead DECLARATION.
index.yaml is observed state: its `generated` stamp is surfaced on the model (C8)
and the file is never regenerated here.

Sources (frozen W3 contract):
  ecosystem/registry.md · ecosystem/index.yaml · ecosystem/deployed-versions.yaml ·
  ecosystem/parity-surfaces.yaml · ecosystem/satellite-onboarding-rulings.yaml ·
  .methodology.yaml · deploy/manifest-v1.4.0.yaml
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ecosystem.schema.desired_state import (  # noqa: E402
    ApplicabilityRule,
    AuditFinding,
    DeclaredDivergence,
    DeployedState,
    FleetDesiredState,
    FleetModel,
    Join,
    LifecycleAssertion,
    LifecycleStage,
    ManifestCut,
    ObservedFleetState,
    Ownership,
    PendingMigration,
    Probe,
    Provenance,
    ProvenanceRef,
    Repo,
    RepoObservation,
    Role,
    SourceRecord,
    Surface,
)

MANIFEST_NAME = "manifest-v1.4.0.yaml"

# Membership-source tokens (the C1 facts vocabulary).
SRC_REGISTRY = "registry-md"
SRC_INDEX = "index-yaml"
SRC_DEPLOYED = "deployed-versions"
SRC_PARITY = "parity-surfaces"
SRC_RULINGS = "onboarding-rulings"

# finding 2 as data: the ADR-109 §3 write-policy table for the seven sources.
_SOURCE_RECORDS = (
    SourceRecord(path="ecosystem/registry.md", role="declarative",
                 write_policy="third-party-writers-barred",
                 parsed_note="RETIRED as authoritative (ADR-109 §2 item 1)"),
    SourceRecord(path="ecosystem/index.yaml", role="derived",
                 write_policy="third-party-writers-barred",
                 parsed_note="observed-state input; writer = audit.py regenerate only"),
    SourceRecord(path="ecosystem/deployed-versions.yaml", role="state",
                 write_policy="third-party-writers-barred",
                 parsed_note="the membership tie-break anchor; writer = deploy tool"),
    SourceRecord(path="ecosystem/parity-surfaces.yaml", role="declarative",
                 write_policy="third-party-writers-barred",
                 parsed_note="the v1 schema-validated instance (ADR-109 §2 item 3)"),
    SourceRecord(path="ecosystem/satellite-onboarding-rulings.yaml", role="ruling",
                 write_policy="third-party-writers-barred"),
    SourceRecord(path=".methodology.yaml", role="consumer-owned",
                 write_policy="round-trip-unknown-byte-stable",
                 parsed_note="repo-owned divergence register; hub read-only"),
    SourceRecord(path=f"deploy/{MANIFEST_NAME}", role="declarative",
                 write_policy="third-party-writers-barred"),
)

# sol §3 mapping (adjudicated D2): registry free prose → one LifecycleStage, raw kept.
_REGISTRY_STAGE_RULES = (
    ("floor-carrying", LifecycleStage.floor_only),
    ("methodology-unonboarded", LifecycleStage.unonboarded),
    ("unonboarded", LifecycleStage.unonboarded),
    ("onboarded", LifecycleStage.full),
    ("source", LifecycleStage.source),
)

_ROLE_TOKENS = {r.value for r in Role}


def _read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def _registry_stage(status: str) -> LifecycleStage:
    for token, stage in _REGISTRY_STAGE_RULES:
        if token in status:
            return stage
    return LifecycleStage.unonboarded


def parse_registry_md(text: str) -> dict[str, dict[str, str]]:
    """The hand-maintained markdown table → {repo id: {path, purpose, status}}."""
    rows: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*`([^`]+)`\s*\|([^|]*)\|([^|]*)\|([^|]*)\|\s*$", line)
        if m:
            rows[m.group(1)] = {"path": m.group(2).strip(), "purpose": m.group(3).strip(),
                                "status": m.group(4).strip()}
    return rows


def _prov_refs(items: list[dict]) -> tuple[ProvenanceRef, ...]:
    return tuple(ProvenanceRef(kind=i["kind"], ref=str(i["ref"]), repo=i.get("repo"))
                 for i in items or ())


def _applicability(tier: dict) -> tuple[ApplicabilityRule, ...]:
    """The role-or-repo-keyed tier map → typed rules (D5); repo-id keys type as
    `repository` (they override role rows by the parity contract's own grammar)."""
    rules = []
    for key, posture in (tier or {}).items():
        kind = "role" if key in _ROLE_TOKENS else "repository"
        rules.append(ApplicabilityRule(selector_kind=kind, selector=key, posture=posture))
    return tuple(rules)


def _load_surfaces(parity: dict) -> tuple[tuple[Surface, ...], tuple[DeclaredDivergence, ...]]:
    surfaces, divergences = [], []
    for row in parity.get("surfaces", ()):
        gra_refs = []
        for repo_id, decl in (row.get("gate_rev_ahead") or {}).items():
            concern = f"{row['id']}/{repo_id}"
            divergences.append(DeclaredDivergence(
                kind="gate-rev-ahead", concern_id=concern, effect="declare-only",
                gate_tag_raw=str(decl["gate_tag"]),
                provenance=Provenance(reason=str(decl.get("reason", "")).strip() or "declared",
                                      refs=_prov_refs(decl.get("provenance"))),
            ))
            gra_refs.append((repo_id, concern))
        own = row["ownership"]
        pm = row.get("pending_migration")
        jn = row.get("join")
        surfaces.append(Surface(
            id=row["id"], kind=row["kind"],
            applicability=_applicability(row.get("tier", {})),
            tier_raw=yaml.safe_dump(row.get("tier", {}), default_flow_style=True).strip(),
            probe=Probe(**row["probe"]),
            ownership=Ownership(value=own["value"], reason=str(own["reason"]).strip(),
                                provenance=_prov_refs(own.get("provenance"))),
            waivable=row.get("waivable"),
            waiver_component=row.get("waiver_component"),
            local_names=tuple((k, v) for k, v in (row.get("local_names") or {}).items()),
            declared_by=row.get("declared_by"),
            declared_divergence=tuple((k, str(v).strip())
                                      for k, v in (row.get("declared_divergence") or {}).items()),
            pending_migration=PendingMigration(**pm) if isinstance(pm, dict) else None,
            join=Join(**jn) if isinstance(jn, dict) else None,
            gate_rev_ahead=tuple(gra_refs),
        ))
    return tuple(surfaces), tuple(divergences)


def _load_waivers(methodology: dict) -> tuple[DeclaredDivergence, ...]:
    out = []
    for entry in methodology.get("sanctioned_divergences", ()):
        out.append(DeclaredDivergence(
            kind="parity-waiver", concern_id=entry["component"], effect="waive",
            component=entry["component"],
            provenance=Provenance(reason=str(entry["reason"]).strip()),
            review_date=entry.get("review_date"),
        ))
    return tuple(out)


def _assemble_repos(registry: dict, deployed: dict, fleet_roles: dict,
                    rulings: dict, index_repos: list[dict]) -> tuple[Repo, ...]:
    index_by_name = {r["name"]: r for r in index_repos}
    union = (set(registry) | set(deployed) | set(fleet_roles) | set(rulings)
             | set(index_by_name))
    repos = []
    for rid in sorted(union):
        membership = set()
        assertions: list[LifecycleAssertion] = []
        status_raw: list[tuple[str, str]] = []
        path = purpose = None
        floor_carrying = False

        if rid in registry:
            membership.add(SRC_REGISTRY)
            row = registry[rid]
            path, purpose = row["path"] or None, row["purpose"] or None
            status = row["status"]
            status_raw.append((SRC_REGISTRY, status))
            floor_carrying = "floor-carrying" in status
            assertions.append(LifecycleAssertion(
                source_surface="registry", semantics="observed",
                raw_value=status, mapped_stage=_registry_stage(status)))
        if rid in index_by_name:
            membership.add(SRC_INDEX)
            path = path or index_by_name[rid].get("path")
        role = None
        if rid in fleet_roles:
            membership.add(SRC_PARITY)
            role = fleet_roles[rid]["role"]
            assertions.append(LifecycleAssertion(
                source_surface="parity", semantics="role-classification",
                raw_value=role,
                mapped_stage=(LifecycleStage.source if role == "hub"
                              else LifecycleStage.unonboarded)))
        if rid in rulings:
            membership.add(SRC_RULINGS)
            ruling = rulings[rid]
            profile = ruling["profile"]
            status_raw.append((SRC_RULINGS, profile))
            assertions.append(LifecycleAssertion(
                source_surface="onboarding-ruling", semantics="desired",
                raw_value=profile,
                mapped_stage=(LifecycleStage.full if profile == "full"
                              else LifecycleStage.floor_only),
                provenance=Provenance(reason=f"operator onboarding-profile ruling for {rid}",
                                      ruled_by=ruling.get("ruled_by"),
                                      ruled_date=ruling.get("ruled_date"),
                                      refs=(ProvenanceRef(kind="census",
                                                          ref=str(ruling["census_ref"])),)
                                      if ruling.get("census_ref") else ())))
        ds = DeployedState()
        if rid in deployed:
            membership.add(SRC_DEPLOYED)
            rec = deployed[rid] or {}
            ds = DeployedState(version=rec.get("deployed_methodology_version"),
                               deployed_date=rec.get("deployed_date"),
                               source_tag=rec.get("source_tag"))
            if ds.version is not None:
                assertions.append(LifecycleAssertion(
                    source_surface="deployed-version", semantics="observed",
                    raw_value=ds.version, mapped_stage=LifecycleStage.full))
        repos.append(Repo(id=rid, path=path, purpose=purpose, role=role,
                          registered=rid in registry, floor_carrying=floor_carrying,
                          assertions=tuple(assertions), deployed=ds,
                          membership=frozenset(membership),
                          status_raw=tuple(status_raw)))
    return tuple(repos)


def _load_observed(index: dict) -> ObservedFleetState:
    obs = []
    for row in index.get("repos", ()):
        obs.append(RepoObservation(
            repo_id=row["name"], last_audit=str(row.get("last_audit") or "") or None,
            findings=tuple(AuditFinding(check_name=f["check_name"], evidence=f["evidence"],
                                        status=str(f["status"]))
                           for f in row.get("findings", ()))))
    generated = index.get("generated")
    return ObservedFleetState(generated_raw=str(generated) if generated is not None else None,
                              repos=tuple(obs))


def load_fleet_model(repo_root: str | Path) -> FleetModel:
    """Parse all seven live sources under `repo_root` into one validated FleetModel."""
    root = Path(repo_root)
    registry = parse_registry_md(_read(root, "ecosystem/registry.md"))
    deployed = (yaml.safe_load(_read(root, "ecosystem/deployed-versions.yaml")) or {}
                ).get("repos", {})
    parity = yaml.safe_load(_read(root, "ecosystem/parity-surfaces.yaml")) or {}
    rulings = (yaml.safe_load(_read(root, "ecosystem/satellite-onboarding-rulings.yaml")) or {}
               ).get("rulings", {})
    methodology = yaml.safe_load(_read(root, ".methodology.yaml")) or {}
    index = yaml.safe_load(_read(root, "ecosystem/index.yaml")) or {}
    manifest = yaml.safe_load(_read(root, f"deploy/{MANIFEST_NAME}")) or {}

    surfaces, gate_divergences = _load_surfaces(parity)
    desired = FleetDesiredState(
        schema_version="1.0.0",
        repos=_assemble_repos(registry, deployed, parity.get("fleet", {}), rulings,
                              index.get("repos", [])),
        surfaces=surfaces,
        divergences=gate_divergences + _load_waivers(methodology),
        manifest=ManifestCut(methodology_version=str(manifest["methodology_version"]),
                             source_tag=str(manifest["source_tag"])),
        sources=_SOURCE_RECORDS,
    )
    return FleetModel(desired=desired, observed=_load_observed(index))


def resolve_fleet_members(desired: FleetDesiredState) -> tuple[str, ...]:
    """C1 resolution: fleet membership resolves toward deployed-versions.yaml — the
    durable record. Repos listed elsewhere still load (facts), but are not members."""
    return tuple(r.id for r in desired.repos if SRC_DEPLOYED in r.membership)
