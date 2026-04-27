# Handoff — Stream C session 1: git default branch convention + PLAYBOOK Repo conventions skeleton

**Date:** 2026-04-26
**Repo:** `.dev-knowledge` (Scale M)
**Branch state at session start:** master (renamed to `main` in Phase 2 of this session)
**Stream C status:** session 1 of 11 — Cluster 1 item 1 only (item 2 → session 2)
**Handoff format:** Scale L (full template per HANDOFF_PROCESS.md v1.1)
**Successor of:** `2026-04-26-stream-b-complete-stream-c-scope.md`

---

## TL;DR

Stream C planned: 11 sessions total. Architectural plan (Cluster 1+2+3 reordered, execution sprints inserted, AGENTS.md Section 11 work added) approved before session 1 ADR-30 work began.

This session: ADR-30 universal `main` rule + PLAYBOOK "Repo conventions" section with 5-subsection skeleton (1 filled, 4 TBD with forward-references to ADR-31/32/33/34). `.dev-knowledge` renamed master→main. Per-repo execution deferred to Stream C execution sprint 1 (session 4).

Lessons promotion (8 candidates from Stream B leftovers) extracted to standalone Claude Code task running BEFORE this session — not browser session time.

---

## Architectural plan — Stream C (revised, 11 sessions)

Approved before session 1 ADR-30 work began. Plan groups items by effort and respects Cluster sequencing.

### Decisions A-E (approved)

- **A.** 5 narrow ADRs for Cluster 1+2 (ADR-30 through ADR-34) — one ADR per topic, no umbrella
- **B.** PLAYBOOK "Repo conventions" section with full 5-subsection skeleton in session 1 (1 filled, 4 TBD with forward-references)
- **C.** Folder structure (originally Cluster 1 item 3) moved to Cluster 2 — depends on Scale assessment
- **D.** Execution sprint between Cluster 1 and Cluster 2 (1-2 sessions, mechanical) WITH:
  - Ultrareview pilot as STANDALONE parallel task (May 5 expiry, time-sensitive, runs independent of sprint sequence)
  - corp-monorepo `.claude/settings.local.json` audit as mini-task in sprint 1
- **E.** 11 sessions total (10 with combine 10+11; session 7 non-combinable due to dependency on session 6)

### Session breakdown

| # | Session | Items | Output | Effort |
|---|---------|-------|--------|--------|
| 1 | Branch convention (this session) | C1.1 | ADR-30 + PLAYBOOK Repo conventions section skeleton + `.dev-knowledge` rename | M |
| 2 | File naming | C1.2 | ADR-31 + fill subsection 2 + migrate-vs-grandfather decision | M-L |
| 3 | Secrets path + Capitalization | C1.4 + C1.5 | ADR-33 + ADR-34 + fill subsections 4 and 5 | S |
| 4 | Execution sprint 1 | per-repo Cluster 1 standards | corp-monorepo + ai-council branch renames; corp-monorepo settings.local.json audit | M |
| 5 | Execution sprint 2 | per-repo Stream B leftovers | CLAUDE.md trims + AGENTS.md creates/expands (per current Gap #6 scope, M+L) | L |
| 6 | Scale assessment + AGENTS.md scope amendment | C2.6 + C2.7 | ADR-35 (Scale assessment) + Gap #6 amendment (M+L → L only? — Council debate) | L (Council territory) |
| 7 | AGENTS.md Section 11 work (NEW) | Section 11 — Session continuity & handoff intelligence | Gap #6 template amendment (10→11 sections) + Section 11 spec + HANDOFF_PROCESS v1.2 + per-repo Section 11 fill-in | M |
| 8 | Folder structure + Scale matrix | C2.3 + C2.8 | ADR-32 + fill subsection 3 + Gap #18 amendment | M |
| 9 | Council CLI decision | C2.9 | Build, remove reference, or parking lot | S |
| 10 | Parking lot + cross-repo review | C3.10 + C3.11 | parking-lot.md + PLAYBOOK section | M |
| 11 | Cross-repo handoff + global skills + self-review | C3.12 + C3.13 + C3.14 | PLAYBOOK additions | M |

**Combine 10+11 → 10 sessions.** Session 7 (AGENTS.md Section 11) non-combinable due to dependency on session 6 amendment.

**Total elapsed time estimate:** 4-6 weeks at sustainable pace.

### Sequencing risk to revisit between sprint 1 and sprint 2

Sprint 2 (session 5) creates AGENTS.md per current Gap #6 scope (M+L). If session 6 amendment changes scope to L only, AGENTS.md created for ai-council (M scale) becomes unnecessary work.

**Mitigation option:** swap session 5 and 6 — do scope amendment FIRST, then sprint 2 with updated scope. Trade-off: amendment work lands before sprint 2 needs unblocking, may delay sprint 2 if Council debate goes long.

**Decision:** revisit at end of sprint 1 (session 4). Don't pre-decide now.

### Ultrareview pilot — parallel standalone task (NOT in session sequence)

- Time-sensitive: 3 free runs expire May 5, 2026
- What it is: Anthropic research preview, multi-agent parallel cloud code review
- Use case: TBD by Rob when fresh context. Likely candidates: comparison vs Codex on corp-monorepo PR/changeset
- Decision protocol per Continuous Improvement Stage 4 (adopt/reject/defer)
- NOT blocking Stream C planning — runs in parallel, Rob triggers when ready
- After May 5: free runs gone, decision on paid adoption or skip

---

## AGENTS.md scope clarification — historical note

Documenting state to prevent future rediscovery confusion:

**Q1 2026:** Pierwotny `templates/AGENTS.md.template.md` był Codex-specific (severity tiers, modes, output format). Nazwa "AGENTS.md template" była mylna od początku — to był Codex review configuration template, nie cross-tool governance template.

**2026-04-24 (Stream B Gap #6):** Created NEW `templates/AGENTS-md-template.md` — cross-tool governance per Council #28 (10 sections, read by Claude Code, Codex, Cursor, Aider, Jules, Factory).

**2026-04-24 reconciliation:** Renamed stary plik do `templates/codex-review-config-template.md` to disambiguate.

**Aktualnie:**
- `templates/AGENTS-md-template.md` = cross-tool governance contract (10 sections)
- `templates/codex-review-config-template.md` = Codex review config, embeddable w AGENTS.md Section 5

**Definitively documented:** PLAYBOOK lines 58, 72.

**Why this note exists:** mental model has reverted to pre-reconciliation state at least twice in browser sessions. This note grounds the truth so future sessions don't re-litigate. If in doubt about AGENTS.md scope: grep PLAYBOOK before responding.

---

## Objective (this session)

Close Stream C session 1: standardize git default branch as `main` across Rob's stack, document via ADR-30, create PLAYBOOK "Repo conventions" section with full 5-subsection skeleton, execute rename for `.dev-knowledge`.

Pre-work (separate Claude Code task, runs BEFORE this session): promote 8 lesson candidates from CHANGELOG to LESSONS.md.

---

## Status

**Pre-session work (Artifact 4 — standalone Claude Code prompt):**

| Lesson | Scope | Source |
|--------|-------|--------|
| 1 | meta | Gap #7d v1.0 drift (filesystem verification for absence claims) |
| 2 | meta | HANDOFF v1.0 → v1.1 (full-cycle dogfooding before ratification) |
| 3 | meta | AGENTS.md sycophancy 2026-04-26 (decision fatigue → false concession) |
| 4 | meta | Stream C scope (handoff INSTANCES vs INTELLIGENCE conflation) |
| 5 | meta | Stream B → C discovery (stream completion ≠ scope completion) |
| 6 | meta | Stream B → C handoff (3-artifact checkpoint) |
| 7 | meta | Selective error reporting (selection bias + sycophancy) |
| 8 | meta | Post-reconciliation mental model drift (grep PLAYBOOK before responding) |

**Browser session decisions (this conversation):**

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Universal `main` rule | Industry alignment, removes LLM-tooling friction, removes intra-stack inconsistency |
| 2 | PLAYBOOK section "Repo conventions" with 5-subsection skeleton | Documents full plan visibly; 4 TBD subsections with forward-references prevent organic drift |
| 3 | ADR scope narrow — ADR-30 = default branch only | Each topic gets own ADR; ADRs 31, 33, 34 reserved for Cluster 1; ADR-32 reserved for Cluster 2 (folder structure) |
| 4 | ADR-30 numbering | README states 30 ADRs active (01–29 + CLAUDE.md governing). Confirmed nothing merged between Stream B close and now |
| 5 | Execution scope `.dev-knowledge` only this session | Per-repo execution → Stream C execution sprint 1 (session 4) |
| 6 | Hardcoded `master` grep before rename | Mandatory — `.github/workflows/`, `.pre-commit-config.yaml`, `scripts/`, hooks, docs referencing branch by name |

**Verification of Stream B sections raised pre-session (A/B/C check):**
- A ("main file opisujący wszystko") — deferred. Intent unclear; revisit when concrete need surfaces. README Navigation may already be the answer
- B ("proces zarządzania nowymi technologiami") — confirmed pokryte przez PLAYBOOK Section 6 Continuous Improvement (Gap #17 done in Stream B). Not amended
- C ("proces Council archiwizacji") — confirmed pokryte przez PLAYBOOK Section 5 Council Debate Archival Protocol (Gap #12 done in Stream B). Not amended

**Execution status (post-merge):** Execution complete 2026-04-26. Lessons promotion (Artifact 4): commit `aa6b34f` on `chore/lessons-promotion-stream-b-leftovers`, merged to main. ADR-30 work (Artifact 2): 8 commits (`2b337bf`, `274221b`, `341548c`, `415f275`, `7289cdd`, `bc85704`, `3a2bf18`, `fabb6eb`) on `feat/adr-30-default-branch-main`, merged via `9df901e`. Codex audit: 0 Critical, 0 High, 1 Medium fixed, 2 Low (Finding 1 accepted as deliberate extended ADR schema, Finding 2 fixed in commit `fabb6eb`). Branch state: `main`. Working tree clean. Hybrid ratio 16% (under 25% ceiling). Phase 2 reduced scope: Steps 11-14 (push/delete/GitHub UI) N/A — `.dev-knowledge` is local-only repo, no remote configured. First full-flow validation of Phase 2 lands in sprint 1 (corp-monorepo, ai-council).

---

## Decisions made (architectural commitments)

**ADR-30 (to be created by Artifact 2):** All Rob's repos use `main` as default branch. Universal rule. Implementation deferred per repo (only `.dev-knowledge` this session).

**PLAYBOOK new section "Repo conventions":** Inserted between "CLAUDE.md as session contract" (~line 169) and "Writing prompts for Claude Code" (~line 170). Initial subsection: "Default branch — `main`" filled. Subsections 2-5 are TBD placeholders with explicit forward-references (ADR-31, ADR-32, ADR-33, ADR-34).

**Stream C execution sequencing (approved Decision D + modifications):**
- Sprint 1 (session 4): per-repo branch renames + corp-monorepo `.claude/settings.local.json` audit
- Sprint 2 (session 5): per-repo CLAUDE.md trims + AGENTS.md creates/expands (per current Gap #6 scope)
- Cluster 2 sessions follow with Gap #6 amendment, Section 11 work, folder structure, etc.

**Process commitments:**
- Branch rename destructive on remote — Phase 2 of Artifact 2 requires explicit Rob confirm
- Codex `/review` triggered (4+ files: ADR-30, PLAYBOOK, README, CHANGELOG)
- Feature branch `feat/adr-30-default-branch-main`, merged to current default before rename

---

## Pending — Stream C per-repo action items

Combined with Stream B per-repo pending items (from previous handoff):

**From Stream B (carried forward):**
1. corp-monorepo CLAUDE.md trim per Gap #5 template (≤200 lines, currently 4KB stale)
2. corp-monorepo AGENTS.md expand per Gap #6 template (currently Codex-only)
3. `.dev-knowledge` create AGENTS.md — verify per Stream C session 6 amendment (M scale may not need)
4. ai-council create AGENTS.md — same caveat
5. ADR-27 collision fix corp-monorepo
6. Read corp-monorepo `.claude/settings.local.json` (Gap #9 audit blind spot #4) — **assigned to sprint 1**
7. Promote LESSONS.md entry: "Documentation prompts prescribing absence claims must include filesystem verification" — **done via Artifact 4 (this session pre-work)**

**From Stream C session 1 (added):**
8. corp-monorepo rename `master` → `main` (Stream C sprint 1)
9. ai-council rename `master` → `main` (Stream C sprint 1)
10. Any other Rob's repo on `master` — sweep + rename
11. GitHub default branch UI step per repo

**Parallel time-sensitive:**
12. Ultrareview pilot before May 5, 2026 (use case TBD, decision per Continuous Improvement Stage 4)

**From Stream C session 1 execution feedback (added post-merge):**
13. LESSONS.md format reconciliation — block entries lines 136-160 diverge from ADR-29 H3 pipe prescription. Mechanical conversion task, 15-30 min Claude Code, candidate slot between session 2 and 3
14. Vocabulary verification check in prompt template — add "verify scope tags against ADR-27 / ESSENTIALS vocabulary" to Read first standardowego prompt template (PLAYBOOK Section "Writing prompts for Claude Code"). Session 7 work or earlier opportunistic
15. ADR template formalization — `templates/ADR-NN-template.md` documenting `Stream` / `Supersedes` / `Superseded by` as optional extended schema; retroactive migration of ADR-27/28/29 if applicable. Session 7 work
16. ADR-30 Steps 11-14 (push main, set remote HEAD, delete origin/master, GitHub UI) untested locally — `.dev-knowledge` has no remote. First full-flow validation lands in sprint 1 (corp-monorepo, ai-council). Standard git ops, low risk, but flag any edge cases
17. Council #27 filter-by-tag rule for chat startup — UNRESOLVED.
    Source: docs/audits/2026-04-21-council-27-brief.md:305 (proposal).
    Status: explicitly flagged as unresolved gap in
    docs/decisions/transcripts/DECISION_27_llm_practice_ecosystem.md:1188
    ("actual workflow was never spelled out"). Decision scope:
    (a) chat type taxonomy, (b) tag-to-context mapping, (c) filter
    mechanism (file-level upload vs section-level read), (d) doc placement.
    Stream C session candidate: session 9 or 11 (Council CLI / cross-repo
    handoff cluster). New ESSENTIALS structure (post-Commit 1) is
    design-neutral, accommodates any future filter mechanism.

---

## Files to upload to next browser chat (Stream C session 2 — file naming)

Required:
1. `ESSENTIALS.md` — daily working style
2. **This handoff** — `docs/handoffs/2026-04-26-stream-c-session-1-branch-convention.md`
3. `PLAYBOOK.md` — current state (with new "Repo conventions" section after Artifact 2 execution)
4. `2026-04-26-stream-b-complete-stream-c-scope.md` — Stream C scope context

Conditional:
5. `README.md` — already documents some naming patterns
6. `naming-sample.txt` — output of `find . -type f -name "*.md" -not -path "./.git/*" | sort` for grounding

DON'T upload:
- Individual ADR-30 (referenced via path mention)
- Templates folder contents

---

## Self-critical observations

1. **Pre-work extraction was Rob's intervention, not browser-side proactivity.** I bundled lessons promotion into session 1 originally; Rob caught it and forced standalone task. Pattern: browser session time should be reserved for analytical work, mechanical promotion belongs in Claude Code prompts. Lesson candidate already in promotion list (#7 selective error reporting).

2. **Session 1 originally proposed without architectural Stream C plan.** I jumped to "rozpisz plan dla item 1" instead of "rozpisz plan dla całego Stream C, potem zoom on session 1." Rob caught it. Result: this handoff has the full 11-session plan, but only because Rob redirected. Lesson candidate to promote next round: "Architectural-first thinking should default to highest scope, then zoom — not bottom-up from current item."

3. **A/B/C reverification check was useful.** Rob raised 14 points at Stream B close; sanity-checked 3 against actual PLAYBOOK content before session 1. Would have been quiet drift if skipped. Already a process pattern; should formalize in HANDOFF_PROCESS v1.2 amendment (session 7 work).

4. **Sequencing risk between sprint 2 and Gap #6 amendment** — flagged in plan, mitigation deferred to end of sprint 1. Documenting because deferring decisions is fine; forgetting deferred decisions is not. Sprint 1 wrap should re-check this.

5. **AGENTS.md historical note added defensively.** Mental model has reverted to pre-reconciliation state ≥2 times in 48h. Note exists to ground truth for future browser sessions. If 3rd revert happens despite this note → process problem, not memory problem. Worth tracking.

6. **TBD subsections in PLAYBOOK have rot risk.** Forward-references show "ADR-31, Stream C session 2" — if Stream C slips, TBD entries age. Mitigation: each TBD shows source-of-truth (ADR number + session); reader can check completion status. Acceptable risk for now; revisit if any TBD entry is >30 days old.

7. **Plan estimates 11 sessions / 4-6 weeks elapsed.** That's longer than original Stream B handoff suggested (5-8 sessions, 2-4 weeks). Variance comes from: rejecting bundling, adding execution sprints, adding Section 11 work. If plan slips beyond 6 weeks elapsed, re-prioritize Cluster 3 items or merge them into a single closing session.

---

## Lessons worth promoting after Artifact 2 execution succeeds (next round)

- **`[scope:meta]`** Architectural-first thinking should default to highest scope, then zoom — not bottom-up from current item. Source: Stream C session 1 plan-then-execute pattern (Rob's redirect).
- **`[scope:meta]`** Pre-session reverification check (verify previous-session deliverables match memory before adding new work) — formalize in HANDOFF_PROCESS v1.2 (session 7 work).
- **`[scope:meta]`** Mechanical promotion tasks (CHANGELOG → LESSONS, etc.) belong in Claude Code prompts, not browser sessions. Browser session time = analytical only.
- **`[scope:meta]`** When deferring a decision, document deferral with concrete revisit trigger (e.g., "end of sprint 1") — deferring is fine, forgetting deferred decisions is not.
- **`[scope:meta]`** Vocabulary tags must be verified against current taxonomy (ADR-27 / ESSENTIALS) before use in prompts. Counter-pattern: prompts using scope tags include 1-line vocabulary check in Read first step. Source: Stream C session 1 Artifact 4 — `[scope: process]` tag invented in prompt (not in ADR-27 vocabulary `dev | llm | hybrid | runtime | meta`), mapped to `[scope: meta]` by Claude Code during execution. Ironic data point for Lesson #8 (post-reconciliation mental model drift).
- **`[scope:meta]`** Browser session execution sequences with multiple Krok N steps where one Krok is "commit document to repo" — that step is easily skipped if flow naturally continues to next executable Krok. Counter-pattern: handoff document commit must be its own confirmed milestone before next prompt runs, not implicit step. Add explicit "Did you commit the handoff?" checkpoint in execution sequence templates. Source: Stream C session 1 — Artifact 1 commit was Krok 2 in execution sequence, skipped en route to Krok 3 (ADR-30 prompt), discovered only at session wrap when Claude Code couldn't find handoff file.

---

## Closing

Session 1 closure delivers ADR-30 (universal `main` rule) + PLAYBOOK "Repo conventions" section foundation with 5-subsection skeleton + `.dev-knowledge` rename + 8 lessons promoted (via standalone pre-work).

Stream C plan is now fully scaffolded: 11 sessions across 4 clusters (Cluster 1 standards, execution sprints, Cluster 2 amendments + new Section 11 work, Cluster 3 future-state). Per-repo execution becomes mechanical follow-up. Plan re-evaluatable at any sprint boundary.

Next session: upload 4 files (in order above), paste first message template (Artifact 3), execute Cluster 1 item 2 (file naming convention).

Order of execution for closing session 1:
1. Rob runs Artifact 4 (standalone lessons promotion via Claude Code) — separate from session sequence
2. Rob commits Artifact 1 update (this handoff document with full plan + clarifications)
3. Stream C session 1 starts: Rob runs Artifact 2 (ADR-30 + PLAYBOOK skeleton + rename)
4. Phase 2 confirm gate before remote rename
5. Codex `/review` before merge
