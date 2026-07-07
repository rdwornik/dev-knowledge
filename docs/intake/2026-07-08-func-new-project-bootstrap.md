---
intake-id: 6
status: SEED
origin: "operator pre-handoff themes, 2026-07-08 (this session)"
consumed-by:
---

# New-project bootstrap — "register project X with purpose Y" as one elaborated flow

> **Backlog lineage (grooming leg-c, 2026-07-08):** absorbs #16 #17 #109 #129 — template/scaffold scope (maximal workspace template, ADR-guidance in CLAUDE-md-template, subdirectory-CLAUDE.md convention, skill-authoring scaffold) folds into this bootstrap epic. #43 remains the decomposition target.

## Problem / motivation

Starting a new repo under `Dev/` has no single entry point. PLAYBOOK §1 ("Starting a
New Project") documents a generic bash scaffold plus a minimum-viable CLAUDE.md, but the
fleet's two most recent cold-starts each **re-derived the governance taxonomy by hand and
diverged** (census `2026-07-08-fleet-consistency-census.md` Part 5): demo-prep grew its own
`docs/intake/` + full hub docs taxonomy + own 3-digit ADRs + armed pre-commit/pre-push;
life-architect grew a root `intake/` + `docs/decisions/` + a baseline pre-commit. Neither
got a `ecosystem/REGISTRY.md` row automatically — the census had to draft both registration
entries. #43 ("decide + author a one-step new-repo scaffold") has sat `[P3][L]` open for the
same reason. The itch: the operator wants to say *"register project X, its purpose is Y"* and
have the whole first-day sequence — registry row, repo scaffold, governance baseline, and the
right role-chat sequence — happen as **one elaborated flow** rather than N hand-re-derivations
that drift.

## Scenarios (+1 view)

- As the operator I come to dev-knowledge and say *"register project X with purpose Y"*, and a
  `ecosystem/REGISTRY.md` row is added (name · path · purpose · status) plus the machine-registry
  seed (`ecosystem/<repo>/`, `index.yaml` regenerated).
- As the operator, immediately after registration, a **repo scaffold** is produced: `git init`;
  the mandatory governance baseline (VISION / CLAUDE / ARCHITECTURE / BACKLOG per ADR-38 A5),
  README/JOURNAL where warranted, the `docs/` taxonomy (decisions / audits / handoffs / **intake**),
  and a baseline pre-commit config armed.
- As the operator the flow then runs a **role-chat sequence scaled to the project's size** — a
  functional pass (intake doc), a technical pass (decomposition), a developer pass (build); a small
  project collapses the sequence, a large one runs all three.
- As the operator I want the new repo to be registry-consistent from minute one, so the next fleet
  census finds no "drafted-not-landed" registration and no hand-divergent taxonomy for it.

## Functional requirements

- **Must:** a single operator entry ("register X, purpose Y") produces the `REGISTRY.md` row + the
  scaffold with the mandatory governance baseline + the `docs/` taxonomy including `docs/intake/` +
  a baseline pre-commit.
- **Must:** the flow is **size-scaled** — it selects which role-chats (func / tech / developer) run
  based on the project's size.
- **Should:** fold #43's scaffold scope (an ADR + `templates/new-repo-skeleton/`, **no scripts**)
  into this flow — the scaffold is the artifact this initiative produces.
- **Should:** the produced repo passes a fleet-consistency census cleanly (intake at `docs/intake/`,
  `.gitattributes` present, EOL normalized).
- **Could:** the purpose statement is distilled into the new repo's `VISION.md` seed, not only the
  registry row.

## Acceptance criteria (ex-ante)

1. Given the operator states "register `<name>` with purpose `<purpose>`", a `REGISTRY.md` row appears
   (name · path · purpose · status) **and** the machine-registry seed exists (`ecosystem/<name>/`
   present, `index.yaml` regenerated) — verified by reading both surfaces.
2. The scaffolded repo contains the mandatory governance baseline (VISION.md, CLAUDE.md,
   ARCHITECTURE.md, BACKLOG.md), a `docs/` taxonomy including `docs/intake/`, and an armed baseline
   pre-commit — verified by a directory listing + a pre-commit dry-run.
3. The role-chat sequence actually run is recorded and matches the size band (e.g. an S project runs
   functional→developer only; an L project runs functional→technical→developer) — verified against a
   stated size→sequence table.
4. Re-running the next fleet-consistency census against the new repo surfaces **zero** registration-drift
   and **zero** hand-divergent-taxonomy findings for it.

## Non-goals

- **Not a code generator** — no product/domain code is scaffolded, only the governance + docs baseline.
- **No orchestration scripts land in this repo** (Layer-2 invariant, ADR-28/36) — the scaffold is
  templates + an ADR, not a driver (matches #43's "no scripts").
- Does **not** decide methodology-deploy propagation (that is #280 / the deploy manifest) — this flow
  is the bootstrap, not the full onboarding mesh (#131 / #215).
- Does **not** retire PLAYBOOK §1's generic scaffold doctrine; it supersedes the hand-re-derivation,
  not the documented convention.

## Impact sketch (4+1 lite)

- **Logical:** a new "bootstrap" seam between operator intent and a registered, scaffolded repo.
- **Process:** collapses N hand-re-derivations into one elaborated flow; the functional role-chat is
  the first real use of the intake pipeline on a greenfield repo.
- **Development:** `templates/new-repo-skeleton/` (from #43) + REGISTRY / machine-registry writes; no
  new runtime scripts here.
- **Physical:** touches `ecosystem/REGISTRY.md`, `ecosystem/index.yaml`, and the new repo's tree.

## Open questions

- Where does the flow physically run — a hub command, a functional-boot mode variant, or an
  operator-driven checklist? (technical-architect question — recorded, not answered.)
- How is "project size" determined for the role-chat scaling — operator-declared band vs inferred?
- Does the machine-registry seed (`ecosystem/<repo>/state.yaml` gitignored + `index.yaml` regen) happen
  at bootstrap or at methodology-onboarding (a separate, later step)?
- Interaction with #131 / #215 (the 6-layer onboarding runbook + conformance-verify): is bootstrap a
  prefix of onboarding, or a distinct lighter path for the methodology-unonboarded class
  (demo-prep / life-architect)?

## Status

SEED — captured 2026-07-08 from operator themes (this session). Folds #43's scaffold scope
(#43 annotated superseded-by this intake). Awaiting functional-architect elaboration, then
technical triage.
