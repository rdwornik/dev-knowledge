===== FILE: 05_NOW — start =====

# 05 · What to do now

## Immediate objective

The capture work is shipped and `main` is pushed; this handoff completes the loop. The
**next big thrust the operator named is the migration of the other chats/repos onto this
handoff system** — bring every browser-chat-per-repo under HANDOFF_PROCESS v4.4 so
methodology-continuity is structural, not memory-dependent. Scope: methodology + process
(not code). Treat this handoff as the live proof-of-concept the migration generalizes
from. Propose a migration plan with rationale; don't ask Rob to forced-rank — pre-select.

## Top priorities (from BACKLOG)

There are **no open `[P1]` items**. The relevant open work, newest-relevant first:

- **#148 [P2][L] — HANDOFF_PROCESS v5 redesign → AI Council** (Tier-1 candidate). The
  architecture decision behind the migration. **Rescoped:** the "forced-read with teeth"
  is largely ALREADY built in v4.4 §C — the real v5 gaps are **lean task-state**
  (BACKLOG = spec, stop re-narrating IDs) + a **self-updating `/handoff`** that always
  pulls current process + methodology pointers (no hand-copies). Seed: the LESSON at the
  top of `LESSONS.md` + the v4.4-as-production-test observation in `04_RECENT`.
- **#139 [P2] — arc-content verifier** (#90b): flips the #77 register row manual→computed.
  **Low urgency, NOT a blocker** — the manual register works with its one entry.
- **#131 [P2][M] — repo-onboarding runbook** (the 6-layer install sequence) — adjacent to
  the migration thrust.
- **Methodology-improvement frontier** the operator flagged: model-selection refinement,
  CC-prompt-creation optimization, re-evaluation cadence, and **token-efficiency** (the
  lean-handoff work + context maximization — this session hit a compaction, itself the
  signal). These are framing inputs to #148, not separate tickets yet.

## In-progress branches & repo state

- `docs/handoff-2026-06-10` — **this handoff's branch**, mid-Phase-2; will be merged
  `--no-ff` to `main` at the Phase-2 commit (and the `in-progress/` interview removed).
- No other unmerged feature branches.
- **Branch:** `main` (after this handoff merges)  ·  **HEAD at generation:** `c8716c2`
- **Working tree at generation:** clean; `main` == `origin/main`.

## Boundaries

- **Do NOT modify HANDOFF_PROCESS v4.4 until this production handoff completes and is
  reviewed** — it is beta (§G); mid-test changes destroy attributability.
- **Do NOT close #77** — it is intentionally open (CLOSURE-VOIDED; the ship-gate
  dispositions it). The `/review-closures` propose-hook will keep suggesting it; closing
  re-makes a corrected error.
- **Do NOT rebuild the forced-read-with-teeth in the v5 council** — it already exists in
  v4.4 §C; only lean-state + self-updating are genuine gaps.
- Layer 2 only: no orchestration scripts; validators are read-only.

## How to choose

If `05_NOW` presents multiple candidate first-moves, **propose your choice with
rationale to Rob** — don't ask him to forced-rank. Operator energy is finite; your
job is reasoned pre-selection. Rob confirms or redirects.

## Top landmines (do-not list)

### Session landmines

- **Do NOT act on a load-bearing claim from memory or a compaction summary** — they are
  stale secondary sources; verify against the file/git first (the v4.4-from-stale-memory
  near-miss this session is the worked example).
- **Do NOT modify v4.4 mid-test**, and **do NOT close #77**.
- **Do NOT rebuild v4.4 §C's forced-read in the v5 council** — rescope to lean-state +
  self-updating `/handoff`.
- **Re-derive `pytest_collected` whenever tests change** — it has drifted 3× (#141/#11/#147).
- **As v4.4's production test, watch ONE thing:** does §C + §3.1 produce real
  methodology *internalization*, or can the apprentice game it by citing the
  `02_METHODOLOGY` extract without reading the live PLAYBOOK? Capture it for the v5 council.

### Standing invariants (repeat)

The load-bearing invariants from `01_ROLE`, repeated here at the recency peak:

- **Append-only** `LESSONS.md` / `logs/TOKEN-LOG.md`; **immutable** ADRs / handoffs /
  transcripts / audits (supersede, never edit in place).
- **Layer 2 never executes** — read-only validators only.
- **No leftovers** — clean up and verify removal of anything you create.
- **OneDrive - Blue Yonder** — never write to or delete inside it.

===== FILE: 05_NOW — end =====
