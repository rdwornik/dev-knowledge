"""ADR-109 divergence report ([#382] W4) — surface × repo × {conform | diverge | declared}.

The `terraform plan` analog (intake #16 §2): renders the DECLARATION layer of the
loaded FleetModel as a flat, fenced, two-minute read. READ-ONLY (Layer-2); writes
nothing; pandas rides the `analytics` dependency group:

    uv sync --locked --group analytics
    uv run --locked python scripts/desired_state_report.py

Verdict semantics (also stated in the report's own HONEST LIMITS block):
- declared — a declared divergence attaches to the cell: a gate-rev-ahead
  declaration, a repo-keyed tier override (LOCAL/IGNORE/INVERSE/TOMBSTONE where the
  role row says otherwise), a matched waiver (surface.waiver_component ↔ loaded
  parity-waiver — the terra-H5 join), a declared_divergence pair, or an
  audit-disposition joined by the <surface>/<repo> concern grammar.
- diverge — an UNDECLARED gap visible in hub-side records (today: the derived
  corpus-version row — declared target vs recorded deployment, G11/C3).
- conform — NO divergence is declared or observable in hub-side records for the
  cell. NOT a live probe result: probe execution stays scripts/fleet_parity.py's.
- · — not applicable (no applicability rule reaches the repo; or the hub on the
  corpus row — the hub IS the source).
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
    Posture,
    Repo,
    Surface,
)
from scripts.desired_state_loader import (  # noqa: E402
    load_fleet_model,
    resolve_fleet_members,
)

CONFORM, DIVERGE, DECLARED, NA = "conform", "diverge", "declared", "·"
_OVERRIDE_POSTURES = {Posture.LOCAL, Posture.IGNORE, Posture.INVERSE, Posture.TOMBSTONE}


def _posture_for(surface: Surface, repo: Repo) -> tuple[Posture | None, bool]:
    """Resolve the applicability posture for one repo: a repository-selector rule
    overrides a role-selector rule (the parity grammar). Returns (posture,
    is_repo_override)."""
    role_rule = repo_override = None
    for rule in surface.applicability:
        if rule.selector_kind == "repository" and rule.selector == repo.id:
            repo_override = rule.posture
        elif rule.selector_kind == "role" and repo.role is not None \
                and rule.selector == repo.role.value:
            role_rule = rule.posture
    if repo_override is not None:
        return repo_override, True
    return role_rule, False


def _cell(surface: Surface, repo: Repo, model: FleetModel,
          waived_components: set[str], disposition_concerns: set[str]) -> str:
    posture, is_override = _posture_for(surface, repo)
    if posture is None:
        return NA
    if dict(surface.gate_rev_ahead).get(repo.id):
        return DECLARED
    if f"{surface.id}/{repo.id}" in disposition_concerns:
        return DECLARED
    if repo.id in dict(surface.declared_divergence):
        return DECLARED
    # terra H5 join: the hub's .methodology.yaml is the only register this repo can
    # read, so a MATCHED waiver declares on the hub column (consumer registers are
    # a recorded hub-side gap).
    if repo.role is not None and repo.role.value == "hub" \
            and surface.waiver_component in waived_components:
        return DECLARED
    if is_override and posture in _OVERRIDE_POSTURES:
        return DECLARED  # a repo-keyed departure from the generic posture IS a declaration
    return CONFORM


def _corpus_cell(repo: Repo, target_version: str, gate_ahead_repos: set[str]) -> str:
    """The derived G11 row: declared corpus target vs recorded deployment."""
    if repo.role is not None and repo.role.value == "hub":
        return NA  # the hub IS the source; its null row is by design (G10 recorded)
    if repo.id in gate_ahead_repos:
        return DECLARED
    if repo.deployed is None or repo.deployed.version is None:
        return DIVERGE  # ruled-or-listed but nothing recorded deployed (the C3 gap)
    if repo.deployed.version == target_version:
        return CONFORM
    return DIVERGE  # deployed behind the declared target, undeclared (G11)


def build_report(model: FleetModel):
    """The frame: index = surface ids + the derived corpus-version row; columns =
    the resolved fleet members (deployed-versions.yaml anchor)."""
    import pandas as pd

    members = resolve_fleet_members(model.desired)
    repos = {r.id: r for r in model.desired.repos if r.id in members}
    waived = {d.concern_id for d in model.desired.divergences
              if d.kind == DivergenceKind.parity_waiver}
    dispositions = {d.concern_id for d in model.desired.divergences
                    if d.kind == DivergenceKind.audit_disposition}
    gate_ahead = {c.split("/", 1)[1] for d in model.desired.divergences
                  if d.kind == DivergenceKind.gate_rev_ahead
                  for c in (d.concern_id,) if "/" in c}
    rows = {s.id: {rid: _cell(s, repos[rid], model, waived, dispositions)
                   for rid in members}
            for s in model.desired.surfaces}
    target = model.desired.manifest.methodology_version if model.desired.manifest else ""
    rows["corpus-version"] = {rid: _corpus_cell(repos[rid], target, gate_ahead)
                              for rid in members}
    return pd.DataFrame.from_dict(rows, orient="index", columns=list(members))


def render_report(model: FleetModel) -> str:
    """Flat + fenced (CLAUDE.md §4 render-layer rule): pipe table with no column
    padding, wrapped in a code fence so the TUI never paints borders."""
    df = build_report(model)
    tally = {CONFORM: 0, DIVERGE: 0, DECLARED: 0, NA: 0}
    for v in df.values.ravel():
        tally[v] += 1
    lines = ["```", "DESIRED-STATE DIVERGENCE REPORT (ADR-109 W4 — the declaration layer)",
             f"fleet members (deployed-versions anchor): {', '.join(df.columns)}",
             f"summary — conform: {tally[CONFORM]} · diverge: {tally[DIVERGE]} · "
             f"declared: {tally[DECLARED]} · n/a: {tally[NA]}", ""]
    lines.append("| surface | " + " | ".join(df.columns) + " |")
    lines.append("|" + "---|" * (len(df.columns) + 1))
    for sid, row in df.iterrows():
        lines.append("| " + sid + " | " + " | ".join(row[c] for c in df.columns) + " |")
    stamp = model.observed.generated_raw or "unknown"
    lines += [
        "",
        "HONEST LIMITS",
        "- hub-side declarations only: consumer actuals are limited to what hub-side",
        "  records hold; consumer .methodology.yaml registers are unreadable from here.",
        "- 'conform' = no divergence declared or observable in hub-side records — it is",
        "  NOT a live probe result; probe execution stays fleet_parity's.",
        f"- the observed rollup (index.yaml) is dated {stamp} and is rendered as-is,",
        "  never regenerated here (C8).",
        "- disposition-register is not among the seven loaded sources; audit-disposition",
        "  rows render DECLARED when a later wave loads them.",
        "- the corpus-version row is DERIVED (manifest target vs recorded deployment);",
        "  every other row renders the parity surface set.",
        "```",
    ]
    return "\n".join(lines)


def main() -> int:
    print(render_report(load_fleet_model(_ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
