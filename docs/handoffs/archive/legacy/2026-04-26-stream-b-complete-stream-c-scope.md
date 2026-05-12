# Handoff — Stream B complete + Stream C scope

**Date:** 2026-04-26  
**Repo:** `.dev-knowledge` (Scale M)  
**Branch state:** master, working tree clean  
**Hybrid ratio:** 17% (under 25% ceiling)  
**Stream B status:** ✅ COMPLETE 19/19 + 1 amendment  
**Handoff format:** Scale L (full template per HANDOFF_PROCESS.md v1.1)

---

## TL;DR

Stream B done. `.dev-knowledge` is universal source; per-repo CLAUDE.md is thin pointer; AGENTS.md template + 14 other gap implementations live in PLAYBOOK.md.

Stream C is **new work** (not amendment) addressing 14 foundational standards gaps surfaced post-Stream-B. Recommended Stream C session 1: Cluster 1 items 1+2 (git branch convention + file naming convention).

---

## Objective (this session)

Close Stream B (19-gap cycle for Rob's `.dev-knowledge` operating system). Identify Stream C scope. Establish 3-artifact handoff process per v1.1 amendment discovered during this very handoff generation.

---

## Status

**Stream B: 19/19 gaps complete + 1 amendment.** All artifacts on master.

| Gap | Topic | Artifact location |
|-----|-------|-------------------|
| #1 | Roles (browser/Claude Code) | ESSENTIALS.md "Roles" v1.0 |
| #2 | Prompt format template | templates/prompt-template.md + PLAYBOOK section |
| #3 | Prompt quality checklist | PLAYBOOK subsection of #2 |
| #4 | Doc files taxonomy | PLAYBOOK "Documentation file types and session continuity" |
| #5 | CLAUDE.md template | templates/CLAUDE-md-template.md + PLAYBOOK section |
| #6 | AGENTS.md template | templates/AGENTS-md-template.md + PLAYBOOK section |
| #7a-d | Claude Code internals | PLAYBOOK "Claude Code internals" + amendment 2026-04-25 |
| #8 | VS Code workspace per Scale | templates/workspace-{S,M,L}.code-workspace + PLAYBOOK subsection |
| #9 | Claude Code features audit | docs/audits/2026-04-25-claude-code-features-inventory.md |
| #10 | Adoption protocol | PLAYBOOK subsection in Claude Code internals |
| #11 | Handoff process | HANDOFF_PROCESS.md v1.1 (amended 2026-04-26 to 3-artifact model) |
| #12 | Council gating | PLAYBOOK Section 5 subsection |
| #13 | Session boundaries | PLAYBOOK section v1.0 |
| #14 | Token management | TOKEN-LOG + ENVIRONMENT + PLAYBOOK Token cadence |
| #15 | Pytest per Scale | PLAYBOOK Project Scale Tiers extension |
| #16 | Codex archival | PLAYBOOK Section 5 subsection |
| #17 | Continuous Improvement | PLAYBOOK Section 6 + docs/tech-radar/ folder |
| #18 | Session continuity per Scale | Combined with Gap #4 — Scale matrix |
| #19 | Amendment vs Reopen | PLAYBOOK Section 5 subsection |

**Plus ad-hoc fixes during Stream B:**
- Validator/hook H3 divergence (invocation semantics bug, ADR-27 amendment 2026-04-25)
- Two AGENTS templates reconciled
- Repo hygiene cleanup 2026-04-24
- TOKEN-LOG order convention flipped to newest-first
- HANDOFF_PROCESS.md v1.1 amendment 2026-04-26 (3-artifact model — discovered during this handoff generation)

---

## Decisions made (architectural commitments)

- `.dev-knowledge` as universal source; per-repo CLAUDE.md = thin pointer (≤200 lines)
- AGENTS.md = canonical cross-tool governance per Council #28 community standard
- Hybrid pattern: AGENTS.md per-repo specifics, points to .dev-knowledge for universal rules
- PLAYBOOK structural: single-file growth (Opcja Y), TOC + numbered sections, ~30 sections target
- TOKEN-LOG threshold-based (7 days) cadence via /session-summary
- Amendment vs Reopen: when validator/tooling diverges from ADR but intent unchanged → amend in place
- **Handoff = 3 artifacts** (persistent doc + Claude Code commit prompt + first-message template), per v1.1

**Process commitments:**
- Browser chat = architect (downloadable .md prompts only); Claude Code = executor
- Handoffs explicit-trigger only ("wygeneruj handoff" or `/session-summary`)
- Per-step test cadence Scale M+: pytest -x --tb=short + ruff + git status
- Council debate gated to ADR-worthy decisions (~70% use single-model + critic)
- Codex review archival: critical/high findings → docs/audits/YYYY-MM-DD-codex-{slug}.md

**Tools adopted:**
- ccusage (npm 18.0.11) for token tracking, replaces /stats
- Subagents (ecosystem-snapshot, report-generator) confirmed active at user-level
- Perplexity research provider added to ai-council
- Spec Kit deferred (no immediate trigger); Kiro rejected (IDE lock-in)

---

## Pending — Stream B per-repo action items (NOT this session)

These require per-repo work beyond `.dev-knowledge`:

1. corp-monorepo CLAUDE.md trim per Gap #5 template (≤200 lines, currently 4KB stale)
2. corp-monorepo AGENTS.md expand per Gap #6 template (currently Codex-only)
3. `.dev-knowledge` create AGENTS.md — **but verify per Stream C Cluster 2 amendment** (M-scale may not need)
4. ai-council create AGENTS.md — same caveat
5. ADR-27 collision fix corp-monorepo
6. Read corp-monorepo `.claude/settings.local.json` (Gap #9 audit blind spot #4)
7. Ultrareview pilot — 3 free runs expire May 5, 2026 (time-sensitive)
8. Promote LESSONS.md entry: "Documentation prompts prescribing absence claims must include filesystem verification" (currently only in CHANGELOG)

---

## Stream C scope identified

Post-Stream B, Rob raised 14 concerns revealing foundational standards gaps Stream B did not address. **NOT Stream B amendments** — Stream B was "what we knew was missing." Stream C is "what we didn't know was missing." Per Gap #19: new stream of work, not amendment to Stream B.

### Cluster 1: Foundational standards (most urgent — Stream C session 1+2)

Ground every other decision.

1. **git default branch convention** — `.dev-knowledge` uses `master`, world uses `main`. Standardize, document rationale or rename.
2. **File naming convention** — currently mixed: kebab (`AGENTS-md-template.md`), snake (`validate_scope_tags.py`), dated kebab (`2026-04-24-stream-b-gaps-mapping.md`). Standardize per file type.
3. **Folder structure standard** — what `docs/` subfolders exist per Scale tier.
4. **`.secrets/` location standard** — `C:\Users\1028120\Documents\.secrets\.env` mentioned in userMemories, not in PLAYBOOK as standard.
5. **Capital vs lowercase convention** — file/folder casing rules.

### Cluster 2: Scale assessment + Stream B amendments (Stream C session 3+4)

Likely Council debate territory.

6. **Scale assessment process** — who decides Scale, when re-assess, what triggers re-evaluation.
7. **Gap #6 amendment candidate:** AGENTS.md only required for Scale L (currently M+L).
8. **Gap #18 amendment candidate:** Scale matrix recalibration based on actual project sizes.
9. **Council CLI mention in PLAYBOOK** — referenced but doesn't exist. Build, remove reference, or move to parking lot.

### Cluster 3: Future-state infrastructure (Stream C session 5+)

10. **Parking lot file** — single intake for "good ideas, not now." Currently scattered.
11. **Cross-repo review mechanics** — how Claude Code in corp-monorepo reviews using `.dev-knowledge` rules.
12. **Browser ↔ Claude Code in different repo handoff** — protocol when scope shifts repos.
13. **Global skills review process** — 2 user-level skills need periodic review.
14. **Claude Code self-review cadence** — periodic config optimality check tied to Continuous Improvement Stage 6.

**Estimated total Stream C:** 12-20h across 5-8 sessions, 2-4 weeks.

### Suggested Stream C session 1 scope

- **In scope:** Cluster 1 items 1+2 (git branch convention + file naming convention)
- **Out of scope:** items 3-5 of Cluster 1, all of Cluster 2/3, per-repo action items
- **Success criterion:** ADR for git branch convention merged + naming convention documented in PLAYBOOK

---

## Files to upload to next browser chat (in order)

Required for any Stream C session:
1. `ESSENTIALS.md` — Rob's daily working style + Roles section
2. **This handoff file** — `docs/handoffs/2026-04-26-stream-b-complete-stream-c-scope.md`
3. `PLAYBOOK.md` — universal protocols (~2000 lines, contains all Stream B sections)

Conditional for Stream C session 1 (Cluster 1):
4. `README.md` — current `.dev-knowledge` user-first navigation
5. `docs/audits/2026-04-24-stream-b-gaps-mapping.md` — Stream B reference (context for "what was scoped vs what surfaced post-stream")

DON'T upload (avoid context bloat):
- Individual ADR files (referenced in PLAYBOOK)
- Templates (referenced in PLAYBOOK, content not needed for standards work)
- Research/audit history beyond #5

---

## Self-critical observations

For Stream C to learn from:

1. **Session boundaries violated by the very session implementing them.** ~13h active across 2026-04-24/25/26. Quality held but risk was real. Stream C must respect own protocol (≤3h, ≤3 architectural decisions).

2. **Recursive planning anti-pattern caught only by Rob's pushback.** System detection insufficient — protocol is human-judgment-dependent.

3. **Documentation drift (Gap #7d v1.0)** caught next day. Lesson candidate not yet promoted to LESSONS.md (currently CHANGELOG only).

4. **Stream B = "what we knew was missing"; missed "what we didn't know was missing"** (Cluster 1 standards). Healthy that Stream C now exists.

5. **Per-repo action items deferred indefinitely.** Should clarify if these come before or after Cluster 1 standards (likely after — standards ground them).

6. **Handoff process v1.0 was incomplete.** Discovered during this very handoff generation: 3 artifacts needed (not 1). Amended to v1.1 mid-handoff. Lesson: process specification benefits from going through full cycle before ratification — v1.0 was specified without dogfooding the full handoff cycle.

---

## Lessons worth promoting to LESSONS.md (after Stream C session 1)

- **`[scope:meta]`** Documentation prompts prescribing "X does not exist" or "X is deferred" must include filesystem verification step (Gap #7d v1.0 drift is proof case)
- **`[scope:process]`** Stream completion ≠ scope completion. Build "what didn't we look for?" check into stream closure ritual.
- **`[scope:dev]`** `/review` gate applies to 3+ CODE files only — markdown + single-line config doesn't warrant.
- **`[scope:dev]`** Delta-based enforcement > threshold-based for repo metric gates.
- **`[scope:meta]`** Process specifications need full-cycle dogfooding before ratification (HANDOFF_PROCESS.md v1.0 → v1.1 example).

---

## Closing

`.dev-knowledge` post-Stream-B is a working operating system for LLM-augmented dev practice. Templates exist, protocols are explicit, decision-making has lifecycle, observability is automated. Stream B + v1.1 handoff amendment provide the foundation; Stream C addresses the foundational standards layer (naming, structure, Scale assessment).

After Stream C, per-repo action items become natural execution applying combined Stream B + Stream C standards.

Next session: upload 5 files (in order above), paste first message template, execute Cluster 1 item 1 (git branch convention).
