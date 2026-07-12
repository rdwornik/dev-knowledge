---
intake-id: 12
status: settled
origin: architect draft, 2026-07-11 — derived from the three 2026-07-11 structural reports (hub fleet-structure comparison · corp #326 leg · ai-council #326+parity leg)
consumed-by:
note: "architect-drafted ownership manifest + nightly decision tree, derived from the three 2026-07-11 structural reports; SETTLED at A0 promotion 2026-07-12 with the §9a hub-`.methodology.yaml` contract reconciliation (see the Tier-1 inverse-rule note); #328's build consumes this as its FIXED charter target"
---

# Fleet Ownership Manifest (SETTLED) + Nightly Hygiene Decision Tree
> #328 charter input. Derived from the three 2026-07-11 structural reports (hub fleet-structure comparison · corp #326 leg · ai-council #326+parity leg). Operator's model: TWO TREES — the hub template tree (per-role) and each repo's implementation tree; the manifest is their join; the nightly check walks it.

## Severity model (operator-defined)
- **MUST** (warunek konieczny) → absent/unfaithful = **ERROR**
- **SHOULD** (good practice / warunek dostateczny) → absent = **WARN**
- **LOCAL-declared** → OK by definition (lives in that repo's .methodology.yaml)
- **UNDECLARED deviation** → WARN in v1, ERROR after hardening (ADR-85 pattern)

## TIER 1 — Methodology spine (hub-owned, MUST for every fleet repo)
| Entry | Note |
|---|---|
| VISION / ARCHITECTURE / CLAUDE / JOURNAL / LESSONS / BACKLOG / CONTRIBUTING (.md) | the 7 canonical docs; ARCHITECTURE = CC-facing (no ToC/Mermaid, #326) |
| docs/ {audits, decisions, intake, archive} | governance shape; audit filenames per ONE convention (open ruling: hub lowercase vs corp _AUDIT_) |
| .claude/ (+ CLAUDE-FLOOR.md hash-guarded replica in consumers; hub = origin, no replica) | |
| .pre-commit-config.yaml with the hub block pinned to a GitHub TAG | consumers; content fidelity = rev + hook ids per manifest |
| .gitignore, .gitattributes, pyproject.toml, .<repo>.code-workspace | |
| tests/, scripts/, logs/, config/ | shape only; contents role-dependent |
| CLAUDE.md: Form-A owner markers + human-visible boundary note | machine map = markers; waivers = .methodology.yaml |

**Consumers additionally MUST:** INSTALL.md (hub-canonical; durable carrier = #315) · .methodology.yaml (the divergence register — a repo without one is unauditable).
**Hub additionally MUST (source role):** .methodology.yaml (its OWN — §9a: the hub is a fleet member, not an implicit exception) · .pre-commit-hooks.yaml (hook exporter) · deploy/ · ecosystem/ · plugins/ · templates/. The hub is a ROLE in the manifest, not an exception (§9a ruling).
**Inverse rule (presence = violation):** docs/handoffs/ in a consumer (ADR-42 centralizes handoffs at the hub) · src/ in the hub (Layer-2 never executes) · INSTALL.md in the hub.
> **A0-promotion reconciliation (2026-07-12):** the DRAFT's inverse rule listed `.methodology.yaml in the hub` as a violation (consumer-only / forbidden-in-hub). That is SUPERSEDED by the operator's §9a ruling — the hub carries its OWN `.methodology.yaml` as a fleet member (no implicit exception) — so `.methodology.yaml` is REMOVED from the hub inverse rule and ADDED to the hub MUST list above. This is the blocking contract-reconciliation named by the Codex derivation (`docs/intake/2026-07-13-siem-fleet-management-requirements-codex.md:34`); with it settled, #328 has a fixed target (`FPR-M` / `HBL:172`).

## TIER 2 — Role/size-conditional (SHOULD → WARN)
| Entry | Condition |
|---|---|
| protocols/ | every repo SHOULD carry one as its inter-repo interface (#327 ruling pending; corp gap = #314) |
| tach.toml | monorepo-size repos (corp yes; small consumers exempt) |
| .github/ CI | today corp-only — OPEN ruling: fleet-generic or local? |
| BACKLOG E-prefix/S-n story-map schema | consumers pending #331 ruling |

## TIER 3 — LOCAL (legitimate, must be DECLARED)
src/<app>/ layout · data/ eval/ models/ output/ (corp) · council_inbox/ output/ transcripts (ai-council) · assets/ruff-pre-commit.yaml (ai-council; INSTALL §2 reference origin) · .env (ai-council; gitignored CWD-fallback, verified) · docs/diagrams/ (corp; NOTE: interacts with the deferred-visualization ruling — review at reopen) · ruff config (three forms exist today: hub .ruff.toml, corp .ruff.toml, ai-council assets/ — CONVERGENCE CANDIDATE: one form, rest declared).

## TIER 4 — IGNORE (gitignored ephemera; check = gitignore parity, never presence)
.venv/ .env(where local) __pycache__/ .pytest_cache/ .ruff_cache/ .mypy_cache/ .hypothesis/ egg-info/ node_modules/ logs-output ephemera.

## Deviations the three reports surface TODAY (feed straight into the register)
1. hub temp/ (junk) — register item, delete-candidate (operator rules). runbox/ did NOT appear in the hub structural report — verify whether it still exists before ruling.
2. ruff-config placement: three different forms across three repos (Tier-3 note) — pick one, declare the rest.
3. corp missing protocols/ (#314) — becomes a Tier-2 WARN the day the check ships.
4. docs/diagrams/ only in corp — reconcile with the ARCHITECTURE-is-CC-facing + deferred-visualization rulings.
5. .vscode/: hub-only today — OPEN ruling (workspace settings: carried template or local?).
6. Audit filename convention clash — open register item; hub form is the interim default.

## The nightly decision tree (per repo R, per root entry E)
```
E in manifest[role(R)]?
├─ YES, tier MUST  → present?
│                     ├─ NO → ERROR (missing necessary)
│                     └─ YES → carried artifact? → fidelity check (tag/rev/hash/ids)
│                                ├─ faithful → OK
│                                └─ drifted  → ERROR (present ≠ carried)
├─ YES, tier SHOULD → present? → OK / WARN
├─ YES, INVERSE     → present? → ERROR (must be absent for this role)
└─ NO (not in template tree)
     ├─ declared in R/.methodology.yaml → OK (LOCAL)
     ├─ matches IGNORE set → gitignored? → OK / WARN (tracked ephemera)
     └─ else → UNDECLARED DEVIATION → WARN v1 (harden to ERROR later)
```
Outputs: per-repo nightly report (ERROR/WARN/OK counts + rows) → verdict-sheet → morning prompt (the #324 standing routine consumes it). The VS Code color layer (#329) renders THE SAME manifest — one truth, three consumers: gate, night report, editor.

## What this replaces
Twenty sessions of the operator manually diffing roots by eye. The tree makes hygiene a routine walk; change management becomes: edit the manifest (one PR at the hub), and every repo's next nightly run enforces it.
