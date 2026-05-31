# BACKLOG Reconciliation — Classification Table (Marathon Arc 2026-05-26 → 2026-05-31)

<!-- scope: meta -->

> **Step 1 deliverable** of the marathon-arc BACKLOG reconciliation
> (`chore/backlog-reconciliation-arc-2026-05-31`). Read-only classification of every
> currently-open/partial BACKLOG entry against arc evidence. **No BACKLOG writes have
> been made.** Operator reviews + may reclassify before Steps 2–6 apply any updates.
>
> Authority/discipline: BACKLOG is Living/update-in-place (CLAUDE.md §4; ADR-39 mutable).
> Method per operator decision 2026-05-31: for closures, flip `[open]`→`[closed]` in the
> header AND add a dated `Status update` bullet; preserve all prior text as evidence.
> Priorities are NOT changed unilaterally — wrong-priority suspicions go to NEEDS-DECISION.

## Arc evidence base (verified this session)

- ADRs **59** (visual pattern), **60** (docs taxonomy + same-day amendment), **61** (worktree),
  **62** (v4 handoff ratification), **63** (scrum-master authority) — all present in `docs/decisions/`.
- **11 LESSONS entries dated 2026-05-30** at top of `LESSONS.md`.
- HANDOFF_PROCESS **v4 → v4.3.1 stable**; session-2 handoff bundle present.
- `protocols/AI_COUNCIL_PROCESS.md` v1.0 present (confirms line 729 closure).
- `scripts/audit.py` has **9 checks** (vision, adr38, claude, dot_prefix, canonical_md,
  workspace, mermaid_theme #7, handoff_bundle #8, handoff_tag #9) → health 9/9.
- **No `lessons-index.json`** anywhere (confirms line 41 = NO-CHANGE; Lessons activation unbuilt).

## Summary counts

| Classification | Count | Entries (line) |
|----------------|-------|----------------|
| CLOSE | 0 | — (arc closed its own items in-place; no missed full closures) |
| PARTIAL | 4 | 257, 286, 392, 504 |
| SCOPE-UPDATE | 2 | 47, 801 |
| NEEDS-DECISION | 2 | 418, 576 |
| NO-CHANGE | ~57 | all others open/partial |
| NEW (Step 5 candidates) | 3 BACKLOG + 1 LESSONS | see below |

**Why zero CLOSE:** the arc sessions diligently closed their own items in-place (ADR-62→line 200,
ADR-63→line 373, ADR-60→line 672, ADR-61→line 680, AI_COUNCIL_PROCESS→line 729, etc. are already
`[closed]`). The reconciliation finds no open entry the arc *fully* closed but left marked open.

## Actionable entries (PARTIAL / SCOPE-UPDATE)

| Line | Pri | Entry | Class | Evidence | Proposed note |
|------|-----|-------|-------|----------|---------------|
| 257 | P3 | v4.3.1 deferred refinements (7 sub-items) | PARTIAL ⚠ | Session-2 bundle addressed sub-items **(3)** AI Council CLI/convene example in 02_METHODOLOGY and **(7)** passive-storage reframe in 03_PROJECT — **at the generated-bundle instance level**; AI_COUNCIL_PROCESS.md v1.0 (2026-05-28) informs **(6)** auto-routing claim | "Partial — sub-items (3)+(7) addressed at bundle-instance level in session-2 bundle; (6) informed by AI_COUNCIL_PROCESS.md v1.0. **Open:** confirm whether the `.tmpl` templates themselves were edited (vs one bundle); sub-items (1) check #10, (2) fresh-eyes cadence, (4) ML namespace, (5) operating-mode wording remain." **⚠ verify .tmpl files before writing** |
| 286 | P3 | Cross-repo audit (Phase 3) | PARTIAL | 2026-05-29 ecosystem coherence audit + 2026-05-27 cross-repo retrofit verification are manual cross-repo audits | "Partial — manual cross-repo audits done (2026-05-29 ecosystem coherence audit; 2026-05-27 retrofit verification). **Open:** the audit-**tool**-driven cross-repo compliance run (overlaps line 817 option b)." |
| 392 | P3 | Apply scrum-master pattern to other child repos | PARTIAL | Codification dependency (old P1 line 373) **closed by ADR-63** 2026-05-30 | "Partial — the codification dependency this entry sequenced after is now **closed (ADR-63, 2026-05-30)**; rollout to child repos remains open. Update the stale 'codification is now P1 above' reference to point at ADR-63." |
| 504 | P2 | Ecosystem feedback-loop enforcement (ML-2/ML-3) | PARTIAL | ML-3 (promote abort to LESSONS) → LESSONS 2026-05-30 batch; ML-2 (un-enforced guard) → ADR-63 codifies the review-authority backstop | "Partial — **ML-3 done** (v3.4-abort meta-lessons appended in the 2026-05-30 LESSONS batch); **ML-2 partly done** (ADR-63 codifies the scrum-master review as the backstop for un-enforced guards). **Open:** the literal guard→amendment-checklist/gate conversion." |
| 47 | P2 | ESSENTIALS additions ADRs 35-54 | SCOPE-UPDATE | Arc added ADRs 55-63; ADR-61 parallel-sessions cheat already added to ESSENTIALS (line 686) | "Scope update — extend candidate range to **ADRs 35-63** (arc added 55-63). Note ADR-61 parallel-sessions cheat already landed in ESSENTIALS; ADR-59/60/62/63 are new candidates." |
| 801 | P2 | CLAUDE-md-template refresh ADRs 54-61 | SCOPE-UPDATE | Arc added ADR-62 (v4 ratification) + ADR-63 (scrum-master) | "Scope update — extend encode-range to **ADRs 54-63** (add ADR-62/63); §11 'last 5 ADRs' rotation target is now 59-63, not 57-61." |

## NEEDS-DECISION (operator input before any write)

| Line | Pri | Entry | Question |
|------|-----|-------|----------|
| 418 | P3 | ADR-42 amendment — single vs multi-artifact handoff format | The 2026-05-11 empirical finding ("single-artifact handoffs work better as flat `.md`") is **contradicted by v4/ADR-62**, which standardizes on the 8-file folder bundle (README+01–07) for *all* handoffs. **Does v4/ADR-62 supersede/moot this ADR-42 amendment?** If yes → mark superseded; if the distinction still matters for non-v4 child-repo handoffs → keep open with a v4 cross-ref. |
| 576 | P2 | Content-scoped archival principle codification | The principle ("each content type gets its own scoped archive subfolder") is **directionally contradicted by ADR-60**, which chose a **flat `archive/` pending-zone** and flattened `docs/archive/` (removed `tech-radar/` subfolder). **Does ADR-60's flat-archive decision supersede this entry**, or is content-scoped archival still wanted for a different artifact class? |

## NO-CHANGE (arc did not substantively touch; status already current)

Grouped for readability — each remains correctly open/partial:

- **ai-council / corp-monorepo / child-repo work** (arc was `.dev-knowledge` self-work + plan authoring; child execution pending): 26, 162, 406, 412, 425, 528, 544, 554, 561, 569, 590, 607, 614, 621, 627, 633, 665, 695, 717, 833.
- **`.dev-knowledge` governance not touched by arc:** 41 (Lessons activation — no lessons-index.json), 68 (taxonomy grooming — quarterly), 88, 94, 101, 107, 134, 141 (stale-test note still present in CLAUDE.md §4), 184, 314, 380.
- **Arc-created entries, correctly still open:** 250 (adversarial fresh-eyes — agent framework stub), 264 (relax-vs-gate principle), 271 (extend audit checks to ADRs/transcripts), 278 (metaphor methodology), 293 (council-decisions consolidation — 2 sub-items open), 300 (sacred-files enforcement), 307 (hooks — audit done 2026-05-29, impl open; status current), 496 (doc-truth sweep — note: arc made some drifts worse but same open work), 512, 520, 536.
- **Tooling/wishlist not touched:** 329, 343, 351, 358, 688, 737, 744, 751, 758, 765, 772, 779, 809, 817, 825.

## NEW entry candidates (Step 5 — pending operator approval)

**BACKLOG** (cross-session + actionable per ADR-41):
1. **Ecosystem-folder operating-model design** (P2, Cross-stream/Ecosystem) — operator stated 2026-05-31 the `ecosystem/` folder exists but its operating model (static snapshot vs continuous cross-repo audit process) is undefined. Council-scope.
2. **AI Council convene-vs-Path-A decision criterion** (P2 or P3) — ADR-62/63 introduced "Path A direct ADR vs convene Council" as a *new* decision not covered by AI_COUNCIL_PROCESS.md v1.0. Pairs with line 264 (relax-vs-gate). Narrower than the closed line 729 (which delivered the lifecycle runbook).
3. **Phase-1 handoff operator-invariants section** (P3) — capture the defaults an inheritor should assume (clean-git-after-handoff, immediate-merge habit, three-domain separation) so a fresh chat doesn't over-ask. Surfaced 2026-05-31.

**LESSONS** (prepend, ADR-46 6-field format):
4. **Inheritor pushback discipline** — state-and-act when the prior is strong and the correction is cheap (surfaced 2026-05-31 from new-chat over-asking on merge state + role). Cross-session-worthy.

**Deliberately NOT added** (per ADR-41 same-session-closed criterion):
- audit.py check #8 patch-version regex fix (closed same session, `a7576dd`).
- handoff comprehensive 5-case matrix (closed same session).
- Level-8 patch-stamp curse-of-knowledge meta-lesson — caught+closed same session (`a7576dd`); **flagged for operator** whether the meta-pattern (each fix-iteration introduces a blind spot one meta-level up) is cross-session-worthy on its own, but default is skip (LESSONS 2026-05-30 entry #11 already captures the meta-recursion pattern).

---

**STOP GATE:** Operator reviews this table. On approval (with any reclassifications),
Steps 2–6 apply the PARTIAL/SCOPE-UPDATE notes, resolve the 2 NEEDS-DECISION items,
add approved NEW entries, and stamp the BACKLOG header.
