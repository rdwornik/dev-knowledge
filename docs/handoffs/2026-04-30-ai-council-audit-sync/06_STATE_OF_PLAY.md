# State of Play — ai-council (Current State)

Per ADR-37 two-phase: this file = Current State.
Future State is in `07_ACTION_PLAN.md`.

---

## Migration completed (locked)

ai-council achieved full ADR-38 architectural compliance via 5-commit migration:

| SHA | Message |
|---|---|
| `8d16c3c` | refactor: move src/ files into src/ai_council/ package namespace |
| `88681ce` | refactor: update imports in src/ai_council/ to new package path |
| `c410eaa` | build: update pyproject.toml for ai_council package structure |
| `1608fab` | refactor: update imports in tests/ to new package path |
| `0eef938` | docs: CHANGELOG, CLAUDE.md, JOURNAL for ADR-38 migration |

Plus merge commit `c821157` (HEAD). All 5 checks PASS (see `06_STATE_OF_PLAY.md`):
`src/ai_council/` namespace, `__init__.py` present, `[build-system]` in
pyproject.toml, `pytest.ini` removed, imports updated.

**Locked decision:** Migration approach was import-path refactoring only —
no logic changes, no test modifications.

---

## Audit findings (Faza A2 — 2026-04-30)

Source: `docs/audits/2026-04-30-ai-council-audit-report.md`

### P1 — Governance-blocking, tier-independent (ACTIONABLE NOW)

| ID | Finding | Status |
|---|---|---|
| F-01 | VISION.md absent (ADR-33 mandate, required at M+) | **OPEN — action required** |
| F-02 | Lessons discovery not configured (DEV_KNOWLEDGE_PATH, ADR-35) | **OPEN — action required** |

### P2 — Important, tier-dependent (DEFERRED)

| ID | Finding | Status |
|---|---|---|
| F-03 | BACKLOG.md absent (ADR-41, mandatory at M+) | DEFERRED — awaits tier calibration |
| F-04 | ARCHITECTURE.md absent (ADR-38, mandatory at L) | DEFERRED — awaits tier calibration |

### P3 — Minor / amendment candidates (DEFERRED or no action)

| ID | Finding | Status |
|---|---|---|
| F-05 | ADR file naming divergence (kebab-case vs ADR-34 underscores) | DEFERRED — grandfather existing 7 ADRs; future ADRs use underscores |
| F-06 | Test count discrepancy (grep 219 vs CLAUDE.md 266) | NO ACTION — class-based tests not caught by grep; use pytest --collect-only |
| F-07 | Module count underrepresents complexity (2 strict vs 8 estimated) | NO ACTION — ADR-38 amendment candidate (BACKLOG) |

### Calibration concern (ecosystem-wide)

| ID | Finding | Status |
|---|---|---|
| F-08 | ADR-40 coefficients produce L for all repos — algorithm not differentiating | DEFERRED — Path 3 strategy: await audit tool P1 multi-repo data |

---

## Tier classification

| Method | Result |
|---|---|
| ADR-40 algorithm (b=12, c=8, d=15) | **L** (score -9.0, clamped 0.0) |
| Intuitive judgment (calibration concern) | **M** (calibration concern registered) |
| Rob's decision | Use **M** for VISION.md `tier:` field pending recalibration |

Locked decision: F-03 (BACKLOG.md) and F-04 (ARCHITECTURE.md) DEFERRED pending
calibration. F-01 and F-02 proceed regardless of tier.

---

## Repo metrics (post-migration, 2026-04-30)

| Signal | Value |
|---|---|
| Modules | 2 (`providers/`, `research/`) |
| Tests (grep) | 219 (likely 266+ per pytest --collect-only) |
| TCR | ~102k tokens (407,119 chars) |
| Files tracked | 79 (src/, tests/, docs, config, scripts) |

---

## Deferred items (BACKLOG references — do NOT duplicate)

- BACKLOG.md Stream B: no items currently (Phase 2 universalization pending)
- BACKLOG.md Cross-stream [P1]: "Phase 1 validation — audit + handoff dry-run on ai-council"
- BACKLOG.md Cross-stream [P2]: "Phase 2 universalization rollout"
- F-03 (BACKLOG.md for ai-council) and F-04 (ARCHITECTURE.md) await ADR-40 recalibration
- ADR-35 full implementation (lessons retrieval) awaits `.dev-knowledge` BACKLOG P2 item

---

## What's locked (do not re-litigate)

1. ADR-38 migration approach: import path refactoring, no logic changes
2. Tier calibration deferral: Path 3 strategy, await audit tool P1 data
3. F-05 grandfathering: existing 7 ADRs keep kebab-case, no renames
4. F-03/F-04 deferral: BACKLOG.md and ARCHITECTURE.md await calibration
