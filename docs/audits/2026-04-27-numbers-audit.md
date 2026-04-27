# Numbers Audit — Path B principle — 2026-04-27

<!-- scope: meta -->

> READ-ONLY audit per Stream C session 1 bonus scope (Krok 3, Tier 2).
> Findings only — fixes in Tier 3 prompt per Rob's per-finding triage.
> Every finding has grep-verified file:line:content. No numbers invented.
>
> Categories per Path B 5-category model:
> 1 = state caching · 2 = arbitrary threshold · 3 = immutable identifier
> 4 = configuration value · 5 = time-bounded snapshot

---

## Summary

**42 numeric references audited across 9 files.**
- **Tier A (REMOVE):** 13 — pure state caching
- **Tier B (REPLACE_WITH_SUBJECTIVE):** 3 — arbitrary thresholds
- **Tier C (KEEP):** 19 — identifiers, dates, config, empirical values
- **Tier D (KEEP + ADD RATIONALE):** 4 — valid but rationale missing
- **Tier E (NEEDS REVIEW):** 3 — ambiguous

---

## Tier A — REMOVE (pure state caching, Cat. 1)

Numbers that describe filesystem/corpus state. Drift on every change. Replace with source reference.

| File:line | Number | Context (exact) | Recommendation |
|-----------|--------|-----------------|----------------|
| `README.md:62` | "31 ADRs active" | "31 ADRs active (ADR-01 through ADR-30, plus CLAUDE.md governing this repo)" | Replace: "ADRs in `docs/decisions/` + corp-monorepo" |
| `README.md:63` | "69 lessons" | "69 lessons in LESSONS.md, scope-tagged inline per ADR-29" | Replace: "see LESSONS.md" |
| `README.md:64` | "#1-#29 archived" | "Council #1-#29 archived (transcripts in corp-monorepo...)" | Replace: "see docs/decisions/transcripts/" |
| `README.md:65` | "19 gaps" | "19 gaps identified for future streams (see latest audit file)" | Replace: "see latest audit file" (pointer already there; drop the count) |
| `ENVIRONMENT.md:51` | "3 universal entries" | "gotchas/gotchas.md ← 3 universal entries (cp1252, az shell, pytest-asyncio)" | Replace: "gotchas/gotchas.md" (drop count) |
| `ENVIRONMENT.md:62` | "4 compression-proof rules" | "core-invariants.md ← 4 compression-proof rules (paths: **/* = every file touch)" | Replace: "core-invariants.md" (drop count) |
| `ENVIRONMENT.md:89` | "10 installed" | "### Extensions (10 installed)" | Replace: "### Extensions" (table is self-documenting) |
| `ENVIRONMENT.md:163` | "14 sections + appendices" | "PLAYBOOK.md ← Full process reference (14 sections + appendices)" | Replace: "PLAYBOOK.md ← Full process reference" |
| `ENVIRONMENT.md:181` | "488+ notes" | "01_Knowledge/ ← Flat (488+ notes)" | Replace: "01_Knowledge/ ← Flat notes" |
| `ENVIRONMENT.md:182` | "9 MOC folders" | "02_Navigate/ ← 9 MOC folders (auto-generated)" | Replace: "02_Navigate/ ← MOC folders (auto-generated)" |
| `ENVIRONMENT.md:183` | "11 tag dimensions" | "99_System/ ← taxonomy.yaml, 11 tag dimensions" | Replace: "99_System/ ← taxonomy.yaml" |
| `PLAYBOOK.md:393` | "2515 tests ... ~200" | "corp-monorepo 2515 tests at L; ai-council ~200 at M" | Remove example counts; Scale tier definitions are sufficient |
| `PLAYBOOK.md:871` | "~30 entries" | "corp-monorepo/.claude/skills/gotchas/SKILL.md ... (~30 entries, Trigger/Symptom/Fix/verify pattern)" | Drop count; file is self-documenting |

---

## Tier B — REPLACE_WITH_SUBJECTIVE (arbitrary thresholds, Cat. 2)

Magnitude was chosen without documented empirical basis. Governance rules that drift relative to reality.

| File:line | Number | Context (exact) | Recommendation |
|-----------|--------|-----------------|----------------|
| `CLAUDE.md:35` + `CLAUDE.md:107` + `ENVIRONMENT.md:170` | "20 files" | "20 files → evaluate Obsidian DevVault migration" | Replace: "when navigation overhead emerges, evaluate DevVault migration" — threshold is arbitrary; current file count already exceeds it periodically |
| `CLAUDE.md:108` | "50 entries" | "Trigger: 50 entries in LESSONS.md → split into topic files" | Replace: "when LESSONS.md becomes hard to navigate by topic, split" — 50 is arbitrary; currently 70+ entries, no split yet, so trigger is already stale |
| `CLAUDE.md:15` (partial) | "~44 H2 headers" | "Full process reference. Numbered sections (currently ~44 H2 headers, numbered 1–16 + unnumbered + appendices)" | "~44" is state caching (Tier A) but "numbered 1–16" is identifier (Tier C); sentence mixes categories. Recommend: drop the count, keep "numbered 1–16 + unnumbered + appendices" |

---

## Tier C — KEEP (identifiers, dates, config, empirical values)

No action needed. Listed by file for completeness; sample only for large groups.

**Identifiers (Cat. 3):** ADR-27, ADR-28, ADR-29, ADR-30, Council #23/#24/#27/#28, Stream A/B/C, v1.0/v1.1, Section 5/12/16, Gap #13/#19, Phase 1/Phase 2 — all names, not counts.

**Timestamps (Cat. 5):** `PLAYBOOK.md:4` (2026-04-21), `ENVIRONMENT.md:4` (2026-04-27), `ESSENTIALS.md:28` (version: 1.0 — 2026-04-24), `HANDOFF_PROCESS.md:2` (v1.1 — 2026-04-26), all TOKEN-LOG entries.

**Configuration values (Cat. 4) — selected:**

| File:line | Value | Context |
|-----------|-------|---------|
| `ENVIRONMENT.md:31` | 10000 | `MAX_THINKING_TOKENS: 10000` |
| `ENVIRONMENT.md:32` | 40 | `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: 40` |
| `ENVIRONMENT.md:26` | 7 days | "threshold-based (7 days) via /session-summary" |
| `CLAUDE.md:18` | 7-day | "Threshold-triggered (7-day) via /session-summary" |
| `CLAUDE.md:87` | ≤25% | "Hybrid ≤25% ceiling (ADR-27)" |
| `PLAYBOOK.md:599` | >3h + >3 decisions | "Decision fatigue: >3 hours active session AND >3 architectural decisions" |
| `PLAYBOOK.md:842` | <500 lines | "SKILL.md < 500 lines, trigger description + instructions" |
| `PLAYBOOK.md:932` | <5 seconds | "Cost: hooks run on every commit; keep fast (<5 seconds typical)" |
| `ESSENTIALS.md:173` | 2x | "same mistake 2x → auto-promoted to permanent rule" |
| `ESSENTIALS.md:177` | ~30% | "expect ~30% false positives" (Codex audit) |
| `HANDOFF_PROCESS.md:102-104` | ~30 / ~60-80 / ~120-200 lines | Scale S/M/L handoff lengths |
| `PLAYBOOK.md:352-354` | 60% / 80% | Coverage targets per Scale tier |

---

## Tier D — KEEP + ADD RATIONALE (Cat. 2/4 with unstated basis)

Numbers that should stay but currently read as arbitrary. Future readers will strip them without a rationale comment.

| File:line | Number | Context | What to add |
|-----------|--------|---------|-------------|
| `ESSENTIALS.md:179` + `SESSION_SETUP.md:100` | >100 stars, >v1.0 | "mature (>100 stars, >v1.0)?" | Add: "heuristics for community validation + production stability signal" |
| `PLAYBOOK.md:352-354` | 60% / 80% | Coverage targets for Scale M / Scale L | Line 393 note says "Baseline numbers from observed practice" — move rationale next to the rule, not in version note at bottom |
| `ESSENTIALS.md:158` | "3+ files, 2+ packages" | "If 3+ files changed or 2+ packages touched → codex-review" | Add: "threshold for cross-module risk — single-file changes don't need review" |
| `PLAYBOOK.md:726` | "4+ criteria" | "If 4+ criteria met → proceed to Evaluation" | Add: "majority-of-6 threshold; ≤3 = not worth evaluation cost" |

---

## Tier E — NEEDS REVIEW (ambiguous)

| File:line | Number | Context | Ambiguity |
|-----------|--------|---------|-----------|
| `ESSENTIALS.md:165` + `SESSION_SETUP.md:122` | ~2 hours | "~2 hours of conversation" (handoff trigger) | Cat. 2 (arbitrary) or Cat. 4 (empirical from PLAYBOOK:599/618 decision fatigue research)? If same basis as >3h threshold, keep with rationale. If different threshold, reconcile. |
| `ESSENTIALS.md:3` | "1 page" | "Keep under 1 page" | Cat. 2 or UX constraint? If UX constraint (reader cognitive load), legitimate Cat. 4. |
| `PLAYBOOK.md:133` | "24 Council Decisions" | "stale numbers like '24 Council Decisions' when there are 29" — this is in prose describing failure mode | Illustrative example of the problem, not a live claim. Contextually fine but could confuse reader. |

---

## Cross-file consistency

Numbers appearing in 2+ files must be treated identically:

| Number | Files | Treatment |
|--------|-------|-----------|
| "20 files → DevVault" | `CLAUDE.md:35`, `CLAUDE.md:107`, `ENVIRONMENT.md:170` | All Tier B — replace all 3 with subjective trigger |
| ">100 stars, >v1.0" | `ESSENTIALS.md:179`, `SESSION_SETUP.md:100` | Both Tier D — add rationale to both |
| "~2 hours" handoff trigger | `ESSENTIALS.md:165`, `SESSION_SETUP.md:122` | Both Tier E — decide in triage, then apply consistently |
| "50 entries → split" | `CLAUDE.md:108` (trigger), `README.md:108` (trigger context) | Both Tier B — remove/replace both |

---

## Notes on append-only files

**TOKEN-LOG.md:** All numbers are usage snapshots (Cat. 5). No action needed — frozen historical data by design.

**CHANGELOG.md:** All numbers are historical record (commit counts, line deltas, gap numbers). Cat. 5 + Cat. 3. No action needed.

---

## Recommendations summary for Tier 3 prompt

**Files requiring edits (Tier A + B fixes):**
1. `README.md` — 4 Tier A removals (lines 62-65)
2. `ENVIRONMENT.md` — 7 Tier A removals + 1 Tier B (lines 51, 62, 89, 163, 170, 181, 182, 183)
3. `CLAUDE.md` — 1 Tier A + 2 Tier B (lines 15, 35, 107, 108)
4. `PLAYBOOK.md` — 2 Tier A removals (lines 393, 871)

**Files requiring rationale additions only (Tier D):**
5. `ESSENTIALS.md` — add rationale at lines 158, 179
6. `SESSION_SETUP.md` — add rationale at line 100
7. `PLAYBOOK.md` — move rationale to be adjacent to lines 352-354; add rationale at line 726

**Rob decides before any edit (Tier E):**
- `~2 hours` trigger: Cat. 4 (keep + rationale) or Cat. 2 (replace with subjective)?
- `1 page` in ESSENTIALS:3: UX constraint (keep) or arbitrary (replace)?

---

## What was NOT audited (out of scope)

- `LESSONS.md` content (append-only, do not edit)
- `docs/decisions/ADR-*.md` (separate audit if needed)
- `templates/`, `scripts/`, `.claude/` config files
- `docs/handoffs/`, `docs/audits/` historical files (frozen)
- Cross-repo files
