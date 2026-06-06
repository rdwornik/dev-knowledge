<!-- scope: meta -->

# ADR-74 — Automation doctrine consolidation; layer→job matrix canonical; ADR-70 amended

- **Status:** Accepted — 2026-06-06
- **Amends:** ADR-70
- **Related:** ADR-36, ADR-66, ADR-68, ADR-69, ADR-71, ADR-72, ADR-73; BACKLOG #84, #85, #95
- **Decommission:** none
- **Source:** Operator ratification, browser session 2026-06-06 (sender audit + ratification; doctrine-pass synthesis).

## Context

ADR-70's three-tier process layer shipped, but its text predates three realities:

1. `/boot` was archived 2026-06-05 with no stated replacement.
2. The ADR-68 local-scheduler Tier-2 host was refuted (night-run shipped as cloud Routine, ADR-72/73); ADR-70's "the natural host is the ADR-68 night agent" clause is now stale.
3. Two enforcing hooks (`normalize-dated-headers`, `backlog-id-on-close`) and one global guard (`block-onedrive.ps1`) operate with no governing decision.

The doctrine pass (2026-06-06) consolidated the system into one layer→job matrix and surfaced the gaps (G1–G5).

## Decision

### 1. Layer→job doctrine matrix is canonical

The following matrix is the authoritative record of every automation organ and its placement. Rows in **bold** are OPEN (not yet shipped) or explicitly REJECTED.

| Job class | Organ / layer | Failure mode | Path | Tier | ADR |
|---|---|---|---|---|---|
| P0 safety (exclusion zone) | PreToolUse global hook (`block-onedrive.ps1`) | fail-closed | every tool call | — | ADR-75 |
| Format / schema / lint / freshness | pre-commit hooks | fail-closed | local commit | 1 | 66, 70, 71, ADR-74 (adoption) |
| Lifecycle capture (`closes [#id]`) | commit-msg hook | fail-closed | local commit | 1 | 65, 66, 70, ADR-74 (adoption) |
| Self-conformance (13 checks) | audit-health / `audit.py` | fail-closed on commit | local commit + manual | 1–2 | 36, 70 |
| Cross-repo baseline | `fleet_health.py` | fail-soft | SessionStart (throttled) | 2 | 69, 70, ADR-74 |
| Awareness / surfacing | SessionStart scripts | fail-soft | session start | 1–2 | 68, 70 |
| Done-detection | Stop → `propose_closures.py` | propose-only | session end | 1 | 70 |
| Heavy verification | Dynamic Workflow (#81) | read-only + skeptic + evidence-required | explicit / cloud | 3 | 70 |
| Autonomous night review | cloud Routine | read-only, self-contained | schedule | 3 | 68 (amended), 72, 73 |
| Cloud→main contract | GH Action triage | fail-closed (counts marker, diff guard) | PR path | 2 (consumption) | 68, 70 |
| **OPEN: LOCAL scheduled night (Tier-2 cross-repo host)** | Desktop scheduler → fleet baseline (#85) | fail-soft + catch-up (R2) | local schedule | 2 | ADR-74; gate n=1 pending |
| **REJECTED: `/loop` tier** | — | — | — | — | session-scoped, 7-day auto-expire, 50-task cap → disqualified for persistence-needing jobs |

Footnote A: the matrix instantiates **per repo** (corp already runs its own self-conformance, night-Routine, and cloud→main contract rows); the hub holds the canonical template (ADR-72/73).

Footnote B (governance doctrine, not an organ): patterns are codified only after n=2 real runs — the evidence-gate meta-rule. BACKLOG #84 is the live instance.

### 2. Doctrine sentence

Deterministic gates on executing paths fail closed; awareness surfaces fail soft; LLM judgment is always read-only + adversarial-skeptic-filtered + operator-ratified; every contract lives on the path production actually takes.

### 3. ADR-70 amendments

**(a) Session-start primitive updated.** `/boot` is archived (2026-06-05). SessionStart hooks (`fleet_health.py`, `surface_triage.ps1`, global `surface-closures.ps1`) are the session-start primitive.

**(b) Tier-2 hosting split.** ADR-70 named the ADR-68 night agent as the structural cross-repo Tier-2 host; that host was refuted (ADR-72/73: cloud sessions see a single clone, not siblings). Tier-2 is now split: SessionStart-throttled `fleet_health.py` serves today's cross-repo baseline; the ratified #85 LOCAL scheduled track is the structural cross-repo host going forward (structural advantage: only local sessions see sibling repos — `siblings_available()` in `fleet_health.py` encodes this). Cloud = per-repo self-contained Tier-3; local = cross-repo Tier-2.

**(c) Lesson-promotion skill.** The lesson-promotion skill (BACKLOG #4) remains unbuilt. ADR-70 listed it as a Tier-1 primitive; this ADR does not re-decide it — tracked in #4, not resolved here.

### 4. Orphan-organ adoption by reference

`normalize-dated-headers` (pre-commit) and `backlog-id-on-close` (commit-msg) are adopted as Tier-1 primitives under ADR-74. No per-hook ADRs are needed.

### 5. Non-doctrinal classification

`claude-notify.ps1` (global Stop, desktop notification) is operational convenience, deliberately outside doctrine.

## Consequences

- The coherent automation whole is now written in one place; doc-debt gaps A3/A4 closed.
- The matrix instantiates per repo with the hub as the canonical template (ADR-72/73).
- New debt made explicit: **G5 — nothing watches template↔copy orchestration drift** between rollout moments; tracked as BACKLOG #95.
- #84 (PLAYBOOK two-tier workflow doctrine) remains gated at n=2 and will reference ADR-74.

## Alternatives considered

Five per-gap ADRs — rejected. Fragmentation; one consolidation amending ADR-70 keeps the doctrine citable as a unit.
