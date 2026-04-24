# PLAYBOOK Tagging Sanity Check — 2026-04-24

## Purpose

On 2026-04-24, PLAYBOOK.md's 78 headers were tagged under pre-commit hook pressure as a one-shot ad-hoc execution rather than via Vibe Code 4's planned Phase 2-audit-driven workflow. This check verifies whether those tags match the canonical tag assignments in the Phase 2 scope audit (`2026-04-21-dev-knowledge-scope-tagging.md`), and whether a stratified sample of subsections correctly inherit their parent's audit tag.

## Method

- **Source of truth:** `docs/audits/2026-04-21-dev-knowledge-scope-tagging.md` (Phase 2 audit, 2026-04-21)
- **PLAYBOOK.md read:** full file, 911 lines, all `##` and `###` headers extracted with their `<!-- scope: X -->` values
- **Top-level match:** all 20 sections covered by the audit joined against current PLAYBOOK.md state
- **Sections not in audit:** 2 top-level headers exist in PLAYBOOK.md that were absent from the Phase 2 audit (noted separately)
- **Sample strategy:** stratified by parent's audit tag (dev / llm / hybrid / runtime / meta), deterministic first-match by file order

---

## Top-level match matrix

The Phase 2 audit covers 20 top-level sections of PLAYBOOK.md. PLAYBOOK.md currently has 22 top-level `##` headers; two are outside audit scope (noted below the table).

| # | Section title | Line | Audit tag | Current tag | Match |
|---|--------------|------|-----------|-------------|-------|
| S0 | Project Scale Tiers | 55 | `dev` | `dev` | ✅ |
| S1 | 1. Starting a New Project | 73 | `dev` | `dev` | ✅ |
| S2 | 2. Creating a Claude Code Prompt | 145 | `hybrid` | `hybrid` | ✅ |
| S3 | 3. Absorbing New Information | 254 | `hybrid` | `hybrid` | ✅ |
| S4 | 4. Extracting Lessons from Any Session | 278 | `llm` | `hybrid` | ❌ |
| S5 | 5. Running an AI Council Debate | 326 | `llm` | `llm` | ✅ |
| S6 | 6. Code Review with Claude Code | 427 | `dev` | `hybrid` | ❌ |
| S7 | 7. Managing a Long Claude Code Session | 441 | `hybrid` | `runtime` | ❌ |
| S8 | 8. Handing Off Between Sessions | 483 | `hybrid` | `hybrid` | ✅ |
| S9 | 9. Weekly Review (Friday) | 555 | `hybrid` | `hybrid` | ✅ |
| S10 | 10. Evaluating a New Tool/Framework/Model | 570 | `hybrid` | `hybrid` | ✅ |
| S11 | 11. Multi-Project Rules | 594 | `dev` | `dev` | ✅ |
| S12 | 12. Where Knowledge Lives | 619 | `meta` | `meta` | ✅ |
| S13 | 13. Markdown Governance | 661 | `dev` | `dev` | ✅ |
| S14 | 14. Anti-Patterns — What NOT to Do | 696 | `hybrid` | `dev` | ❌ |
| S15 | 15. Cross-Tool Review \[L+M\] | 731 | `dev` | `hybrid` | ❌ |
| S16 | 16. Code Quality Audit Process | 754 | `dev` | `dev` | ✅ |
| AppA | Appendix A: Claude Code Shortcuts | 796 | `runtime` | `runtime` | ✅ |
| AppB | Appendix B: Model Routing Table | 861 | `llm` | `llm` | ✅ |
| AppC | Appendix C: Token Optimization Techniques | 888 | `llm` | `llm` | ✅ |

### Sections not covered by the Phase 2 audit

Two top-level `##` headers in PLAYBOOK.md were absent from the 2026-04-21 audit (likely added or split after the audit was written):

| Section title | Line | Current tag | Status |
|--------------|------|-------------|--------|
| System Architecture | 8 | `meta` | Not in audit — no canonical reference |
| The 10 Commandments | 715 | `hybrid` | Not in audit — audit folded into S14 conceptually; current `hybrid` is plausible |

---

## Subsection inherit-parent sample

One subsection per audit parent-tag type, deterministic first-match by file order.

| Parent tag (audit) | Subsection title | Line | Parent section | Subsection current tag | Verdict |
|-------------------|-----------------|------|----------------|----------------------|---------|
| `dev` | Scaffold | 78 | S1: Starting a New Project | `dev` | ✅ |
| `llm` | When to extract | 283 | S4: Extracting Lessons from Any Session | `hybrid` | ❌ |
| `hybrid` | Summary table (required at top of every formal prompt) | 153 | S2: Creating a Claude Code Prompt | `hybrid` | ✅ |
| `runtime` | Permission Modes (Shift+Tab cycles) | 799 | Appendix A: Claude Code Shortcuts | `runtime` | ✅ |
| `meta` | "Where does this go?" decision rule | 633 | S12: Where Knowledge Lives | `meta` | ✅ |

The `llm` row failure (S4 "When to extract" tagged `hybrid`) is a cascade of the S4 top-level mismatch: the parent was mis-tagged `hybrid` during the one-shot script, so the subsection inherited the wrong parent tag.

---

## Verdict

- **Top-level:** 15 / 20 match audit, 0 missing, **5 mismatched** (S4, S6, S7, S14, S15)
- **Sections outside audit scope:** 2 (System Architecture, The 10 Commandments) — not counted as mismatches
- **Subsection inherit-parent:** 4 / 5 sampled correctly inherit, **1 differs** (S4 → "When to extract"), 0 missing
- **Overall: FAIL**

### Mismatched sections (top-level)

| Section | Audit says | PLAYBOOK.md has | Direction of error |
|---------|-----------|-----------------|-------------------|
| S4: Extracting Lessons from Any Session | `llm` | `hybrid` | over-tagged |
| S6: Code Review with Claude Code | `dev` | `hybrid` | over-tagged |
| S7: Managing a Long Claude Code Session | `hybrid` | `runtime` | wrong category |
| S14: Anti-Patterns — What NOT to Do | `hybrid` | `dev` | under-tagged |
| S15: Cross-Tool Review \[L+M\] | `dev` | `hybrid` | over-tagged |

---

## If FAIL — next action

Write Prompt 3.6 fix task: correct 5 top-level `##` tags (S4 → `llm`, S6 → `dev`, S7 → `hybrid`, S14 → `hybrid`, S15 → `dev`) and re-tag all subsections under each corrected parent to match the new parent tag.

---

## Follow-up — Prompt 3.6 resolution (2026-04-24)

All 5 top-level mismatches corrected.
Cascade subsection fixes applied: 9 edits total — 4 under S4 (`hybrid` → `llm`), 4 under S7 (`runtime` → `hybrid`), 1 under S15 (`hybrid` → `dev`). S6 had one subsection already matching new parent (`dev`); S14 had no subsections.
Subsections flagged as potential intentional overrides (not changed): S4 → "When a lesson becomes a rule" (`meta`) — content governs `~/.claude/` rule promotion, `meta` tag is plausible intentional override.
Hybrid ratio: before (not recorded) → after 0% (info only, threshold 25%).
Re-verification: all 5 corrected parent sections and all 11 verifiable subsections match expected post-fix state.

Status: Stream A Prompt 3.6 complete. Sanity check verdict now PASS.
