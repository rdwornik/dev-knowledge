===== FILE: 05_NOW — start =====

# 05 · What to do now

## Immediate objective

Run a **comparative audit** of our handoff / skills / way-of-working against **Matt
Pocock's** material, then drive the **v5 redesign of HANDOFF_PROCESS (#148)** through
AI Council. Scope: analysis + synthesis + a Council debate — **not** code, **not**
editing the live process this session. Fetch Matt's material as **primary sources —
do NOT reproduce them into the repo** (URLs are pointers only):
- YouTube workshop: https://www.youtube.com/watch?v=-QFHIoCo-Ko
- github.com/mattpocock/dictionary-of-ai-coding · github.com/mattpocock/skills ·
  github.com/mattpocock

**Reconcile the two tracks (do not conflate them):**
- **Migration** rides on **v4.4 §G validation** (promote beta→stable via one fresh-eyes
  review: <2 critical findings AND reviewer verdict PROMOTE/PROMOTE-WITH-CAVEATS). It is
  pointer-first and does **not** wait on v5.
- **#148/v5** is a **parallel hub-side enhancement** that propagates to children via the
  existing pointers — it is **NOT "the architecture behind the migration"** and **NOT a
  blocker**. Stating both as one dependent thing is an internal contradiction.

§G promotion is **now in reach**; surfaced (not decided) pilot candidates: the hub
(lowest-risk — a fresh-eyes review of an existing v4.4 bundle could satisfy §G), or
corp-monorepo (richest stress test). **This bundle can itself be the production-pilot**
— but promotion is **downstream** of completing + reviewing it, and is **Rob's call**.

## Top priorities (from BACKLOG)

**No open P1.** Relevant open work (full queue in `BACKLOG.md` — this is a pointer, not
a re-narration):
- **`[#148] [P2][L]` — HANDOFF_PROCESS v5 redesign** (Tier-1, AI-Council). *Today's thread.*
- `[#131] [P2][M]` — repo-onboarding runbook (6-layer install sequence).
- `[#139] [P2][L]` — merged-arc→record verifier (low-urgency; not a blocker).

## In-progress branches & repo state

- **Branch:** `docs/handoff-2026-06-10-v5-pivot` (this bundle)  ·  **HEAD:** `fda1306`
- **`main` tip:** `2c2a1b5` (fleet-audit merge)  ·  no other in-progress feature branches.
- **Working tree at generation:** clean once this bundle is committed.

## Boundaries

- **Do NOT modify HANDOFF_PROCESS v4.4** until this handoff is reviewed — generate
  *with* it; the process is frozen.
- **Do NOT close #77** (CLOSURE-VOIDED 2026-06-09 — stays open).
- **Do NOT rebuild §C's static forced-read** in v5 — the active-alignment skill replaces it.
- **Do NOT reproduce Matt's transcript/dictionary into the repo** — URLs only.
- ADR-41 (no cross-repo edits); Layer-2 read-only (validators only).

## How to choose

If you see multiple candidate first-moves, **propose your choice with rationale to
Rob** — don't ask him to forced-rank. Operator energy is finite; your job is reasoned
pre-selection. Rob confirms or redirects.

## Top landmines (do-not list)
<!-- positional-redundancy: deliberate duplicate, do not deduplicate (v4.4 §A/§B) —
     RECENCY-PEAK tail: the last thing read before acknowledgment. -->

### Session landmines

- **Do NOT** conflate the migration (v4.4 §G validation) with #148/v5 — they are
  parallel tracks, not a dependency chain.
- **Do NOT** re-narrate done-work IDs/SHAs — task-state is a pointer to BACKLOG/JOURNAL/git.
- **Do NOT** hand-copy the bundle/spec structure from any extract — read the live
  `HANDOFF_PROCESS.md` + `PLAYBOOK.md` and build to them.
- **Do NOT** treat v4.4 as already `stable` — promotion needs Rob's fresh-eyes verdict.
- **Do NOT** reproduce Matt's material into the repo — primary-source pointers only.

### Standing invariants (repeat)

The load-bearing invariants from `01_ROLE`, repeated here at the recency peak:

- **Append-only** `LESSONS.md` / `logs/TOKEN-LOG.md`; **immutable** ADRs / handoffs /
  transcripts / audits (supersede, never edit in place).
- **Layer 2 never executes** — read-only validators only.
- **No leftovers** — clean up and verify removal of anything you create.
- **OneDrive - Blue Yonder** — never write to or delete inside it.

===== FILE: 05_NOW — end =====
