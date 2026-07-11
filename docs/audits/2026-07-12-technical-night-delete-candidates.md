# Delete-candidates sweep — night 2026-07-11→12 (H3)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-12
- **Source-session:** night-batch Phase 2.75 (H3) · **Model:** claude-opus-4-8
- **Status:** LIST ONLY — zero deletions performed (never-delete-without-asking is absolute)

## Executive so-what

**The corpus is lean; tonight proposes ZERO new deletions.** This sweep's real value is the
**disposition of the PRIOR 2026-07-09 deletion-candidates report against live state** (the
operator explicitly asked whether those were taken into account) + a **still-unfiled backup-gap
task**. The gitignored on-disk clutter (temp/, node_modules, .claude/worktrees) is unchanged and
low-risk. My 3 build branches are night work (operator merges), not candidates.

## Prior 2026-07-09 candidates — disposition against LIVE state (the operator's question)

```
prior item                                          live status now
1 delete 3 merged branches (hub 2, demo-prep 1)     hub 2 ACTIONED (docs/2026-07-08-architect-
                                                    handoff + worktree-cadence-teeth both GONE);
                                                    demo-prep 1 = consumer scope (unverified,
                                                    read-only)
2 backup gap (corp-ops/corp-sca/demo-prep unbacked) STILL PENDING + UNFILED — the proposed
                                                    "[P2][S] Fleet backup posture" task is NOT in
                                                    the hub BACKLOG (grep=0). The one prior item
                                                    that fell through. (consumer scope, ADR-41)
3 origin/automation/conformance-digest (#255)       GONE/pruned (not in current branch list) —
                                                    #255 verify-then-delete appears ACTIONED
4 automation/fleet-audit push-for-durability (#254) ACTIONED — origin/automation/fleet-audit now
                                                    exists + tracks (78 commits, latest 07-09)
5 three 0-code-referrer modules (keep-by-design)    KEEP unchanged (probe_child_backlogs /
                                                    review_closures / release_lint — by design)
6 v4 handoff templates (gated #164)                 STILL GATED by #164 (unchanged)
7 docs/archive/ triage-queue (periodic review)      STILL pending an operator archive-review call
```

**Answer to the operator:** yes — the prior candidates were reconciled. 4/7 are actioned or
tracked-closed (items 1-hub, 3, 4), 3 remain by-design/gated (5, 6, 7), and **item 2 (fleet
backup posture) is the one still-open, still-UNFILED gap** — recommend filing it (task text is
verbatim in the 2026-07-09 report §"Proposed ready-to-file task").

## Tonight's candidates (LIST only)

```
candidate                          why / evidence                          risk    recommend
gitignored temp/                   0 files, 4K (empty — #229 relocation     none    KEEP (empty; the
                                   held; not regrown)                               dir itself is harmless)
gitignored .claude/worktrees/      0 files, 4K (empty — no leftover                 none    KEEP (empty
                                   worktrees; no .dev-knowledge-* orphans)          scaffold dir)
gitignored node_modules/           5296 files, 29M — npm deps (tooling).    LOW     KEEP unless the npm
                                   Not in git; on-disk only                         toolchain is retired;
                                                                                    not this session's call
feat/306-hermetization-gate        night build (2 commits), UNMERGED        n/a     KEEP — operator merges
feat/307-intake-index              night build (2 commits), UNMERGED        n/a     KEEP — operator merges
feat/e2e-lifecycle                 night build (1 commit), UNMERGED         n/a     KEEP — operator merges
automation/fleet-audit             data-branch organ, #254 ruled KEEP,      n/a     KEEP (ruled) — the H3
                                   origin tracks                                    "integrate-or-abandon"
                                                                                    ask is already RULED KEEP
superseded-era handoff bundles     ADR-101 §5 + 2026-07-09 §S4-3: STAY as   n/a     KEEP (by doctrine)
                                   historical (no archiving rule)
```

## Recommendations / routing

- **File the backup-posture task** (prior item 2) — the single prior candidate that fell through;
  it is a HIGH-risk data-safety gap (3 repos unbacked on one disk), not a deletion.
- **No deletions tonight.** The `automation/fleet-audit` "integrate-or-abandon" question the H3
  brief posed is already RULED (KEEP, #254 — a data-branch organ, origin-durable); its 78 daily
  baselines are the organ's designed output, not overlap-with-landed-work.
- gitignored clutter is empty (temp/, worktrees) or tooling (node_modules) — nothing to reclaim.

## Scope / method

Read-only: `git branch -a`, per-branch merge/ahead status, `find`/`du` on gitignored dirs, the
prior 2026-07-09 report cross-referenced item-by-item against live branch/BACKLOG state. corp
UPPERCASE quarantine class = corp read-only, LISTED not touched (it is the R4 motivating fixture,
already captured in #306). Nothing deleted, renamed, or modified.
