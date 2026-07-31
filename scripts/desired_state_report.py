"""ADR-109 divergence report ([#382] W4) — surface × repo × {conform | diverge | declared}.

The `terraform plan` analog (intake #16 §2): renders the DECLARATION layer of the
loaded FleetModel as a flat, fenced, two-minute read. READ-ONLY (Layer-2); writes
nothing. Verdict semantics are pandas-free (`build_matrix`, terra H5); the pandas
DataFrame integration (`build_report`) rides the `analytics` dependency group:

    uv sync --locked --group analytics
    uv run --locked python scripts/desired_state_report.py

Verdict semantics (also stated in the report's own HONEST LIMITS block; terra W4
review applied — docs/audits/2026-07-31-codex-382-w4-report.md):
- declared — a declared divergence attaches to the cell: an ACTIVE gate-rev-ahead
  declaration (self-invalidates once deployed source_tag reaches gate_tag_raw —
  terra H3), a repo-keyed tier override that DIFFERS from the resolved role posture
  (terra H4 — an equal or baseline-less repo rule is just the posture), a matched
  waiver (surface.waiver_component ↔ loaded parity-waiver; hub column only — the
  only register this repo can read), a declared_divergence pair, or an
  audit-disposition joined by the <surface>/<repo> concern grammar.
- diverge — an UNDECLARED gap visible in hub-side records: today the derived
  corpus-version row — deployed behind the declared target (G11), or nothing
  deployed under a desired-FULL ruling (C3; a floor-only or unruled repo is NOT
  the C3 gap — terra H2).
- conform — NO divergence is DECLARED for the cell. This is the declaration layer:
  no observational join is claimed (a reliable surface⇄finding join needs the G9
  crosswalk populated — #383-era; terra H1), and probe execution stays
  scripts/fleet_parity.py's.
- · — not applicable (no applicability rule reaches the repo; the hub on the
  corpus row — the hub IS the source; or no corpus expectation is recorded).
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ecosystem.schema.desired_state import (  # noqa: E402
    DivergenceKind,
    FleetModel,
    LifecycleStage,
    Posture,
    Repo,
    Semantics,
    Surface,
)
from scripts.desired_state_loader import (  # noqa: E402
    load_fleet_model,
    resolve_fleet_members,
)

CONFORM, DIVERGE, DECLARED, NA = "conform", "diverge", "declared", "·"


def _posture_for(surface: Surface, repo: Repo) -> tuple[Posture | None, Posture | None]:
    """Resolve applicability for one repo: (effective posture, role-baseline posture).
    A repository-selector rule overrides a role-selector rule (the parity grammar);
    the baseline is returned so a repo override is judged a DEPARTURE only when it
    differs (terra H4)."""
    role_rule = repo_override = None
    for rule in surface.applicability:
        if rule.selector_kind == "repository" and rule.selector == repo.id:
            repo_override = rule.posture
        elif rule.selector_kind == "role" and repo.role is not None \
                and rule.selector == repo.role.value:
            role_rule = rule.posture
    if repo_override is not None:
        return repo_override, role_rule
    return role_rule, role_rule


def _cell(surface: Surface, repo: Repo, waived_components: set[str],
          disposition_concerns: set[str]) -> str:
    posture, baseline = _posture_for(surface, repo)
    if posture is None:
        return NA
    if dict(surface.gate_rev_ahead).get(repo.id):
        # the surface→divergence reference is validated at the model root (W2 M6),
        # so an attached ref is never dangling here
        return DECLARED
    if f"{surface.id}/{repo.id}" in disposition_concerns:
        return DECLARED
    if repo.id in dict(surface.declared_divergence):
        return DECLARED
    if repo.role is not None and repo.role.value == "hub" \
            and surface.waiver_component in waived_components:
        return DECLARED
    if baseline is not None and posture != baseline:
        return DECLARED  # a repo-keyed DEPARTURE from the role baseline is a declaration
    return CONFORM


def _desired_full(repo: Repo) -> bool:
    """terra H2: the C3 gap exists only under a desired-FULL assertion (the ruled
    target); floor-only or unruled repos carry no recorded corpus expectation."""
    return any(a.semantics == Semantics.desired and a.mapped_stage == LifecycleStage.full
               for a in repo.assertions)


def _corpus_cell(repo: Repo, target_version: str, gate_tags: dict[str, str]) -> str:
    """The derived G11 row: declared corpus target vs recorded deployment."""
    if repo.role is not None and repo.role.value == "hub":
        return NA  # the hub IS the source; its null row is by design (G10 recorded)
    deployed = repo.deployed
    gate_tag = gate_tags.get(repo.id)
    if gate_tag is not None and (deployed is None or deployed.source_tag != gate_tag):
        return DECLARED  # active gate-ahead declaration
    # gate reached (or none): the declaration is self-invalidated (terra H3) — judge
    # the recorded deployment against the declared target.
    if deployed is None or deployed.version is None:
        return DIVERGE if _desired_full(repo) else NA
    if deployed.version == target_version:
        return CONFORM
    return DIVERGE  # deployed behind the declared target, undeclared (G11)


def build_matrix(model: FleetModel) -> dict[str, dict[str, str]]:
    """Pure verdict semantics (no pandas — terra H5): {surface id: {repo id: verdict}},
    columns = the resolved fleet members (deployed-versions.yaml anchor), plus the
    derived corpus-version row."""
    members = resolve_fleet_members(model.desired)
    repos = {r.id: r for r in model.desired.repos if r.id in members}
    waived = {d.concern_id for d in model.desired.divergences
              if d.kind == DivergenceKind.parity_waiver}
    dispositions = {d.concern_id for d in model.desired.divergences
                    if d.kind == DivergenceKind.audit_disposition}
    gate_tags: dict[str, str] = {}
    for d in model.desired.divergences:
        if d.kind == DivergenceKind.gate_rev_ahead and "/" in d.concern_id \
                and d.gate_tag_raw is not None:
            gate_tags[d.concern_id.split("/", 1)[1]] = d.gate_tag_raw
    matrix = {s.id: {rid: _cell(s, repos[rid], waived, dispositions) for rid in members}
              for s in model.desired.surfaces}
    target = model.desired.manifest.methodology_version if model.desired.manifest else ""
    matrix["corpus-version"] = {rid: _corpus_cell(repos[rid], target, gate_tags)
                                for rid in members}
    return matrix


def build_report(model: FleetModel):
    """The pandas frame over build_matrix (the analytics-group integration surface)."""
    import pandas as pd

    matrix = build_matrix(model)
    members = list(next(iter(matrix.values())).keys()) if matrix else []
    return pd.DataFrame.from_dict(matrix, orient="index", columns=members)


def render_report(model: FleetModel) -> str:
    """Flat + fenced (CLAUDE.md §4 render-layer rule): pipe table with no column
    padding, wrapped in a code fence so the TUI never paints borders."""
    matrix = build_matrix(model)
    members = list(next(iter(matrix.values())).keys())
    tally = {CONFORM: 0, DIVERGE: 0, DECLARED: 0, NA: 0}
    for row in matrix.values():
        for v in row.values():
            tally[v] += 1
    lines = ["```", "DESIRED-STATE DIVERGENCE REPORT (ADR-109 W4 — the declaration layer)",
             f"fleet members (deployed-versions anchor): {', '.join(members)}",
             f"summary — conform: {tally[CONFORM]} · diverge: {tally[DIVERGE]} · "
             f"declared: {tally[DECLARED]} · n/a: {tally[NA]}", ""]
    lines.append("| surface | " + " | ".join(members) + " |")
    lines.append("|" + "---|" * (len(members) + 1))
    for sid, row in matrix.items():
        lines.append("| " + sid + " | " + " | ".join(row[m] for m in members) + " |")
    stamp = model.observed.generated_raw or "unknown"
    lines += [
        "",
        "HONEST LIMITS",
        "- hub-side declarations only: consumer actuals are limited to what hub-side",
        "  records hold; consumer .methodology.yaml registers are unreadable from here.",
        "- 'conform' = no divergence DECLARED for the cell — the declaration layer.",
        "  No observational join is claimed (surface⇄finding joins await the G9",
        "  crosswalk population), and probe execution stays fleet_parity's.",
        f"- the observed rollup (index.yaml) is dated {stamp} and is rendered as-is,",
        "  never regenerated here (C8).",
        "- disposition-register is not among the seven loaded sources; audit-disposition",
        "  rows render DECLARED when a later wave loads them.",
        "- the corpus-version row is DERIVED (manifest target vs recorded deployment;",
        "  gate-rev-ahead declarations self-invalidate once the gate tag is reached);",
        "  every other row renders the parity surface set.",
        "```",
    ]
    return "\n".join(lines)


def main() -> int:
    print(render_report(load_fleet_model(_ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
