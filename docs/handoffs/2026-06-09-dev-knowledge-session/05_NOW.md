===== FILE: 05_NOW — start =====

# 05 · What to do now

## Immediate objective

The operator's frame is **maximize the methodology before fleet rollout**. The
natural next step is the cheap, highest-leverage **codification cluster** — bringing
PLAYBOOK doctrine up to what we already practice — but **re-sync the stale backlog
against git first** (#134/#90 is the organ): the current snapshot predates this
session's #137 close and #138 add, so its counts/statuses are not trustworthy blind.
The floor stays **shelved** absent a real trigger. Scope: docs/methodology
codification + a backlog reconciliation pass — not net-new construction.

## Top priorities (from BACKLOG)

**No open P1 items** (the #134 groom moved #1/#2 → P2; the last P1, #107, closed). The
live top of the queue is P2, in the operator's stated pre-rollout order:

- **#135** [P2/S] — promote the diagram-form 5-rule algorithm to PLAYBOOK doctrine.
- **#136** [P2/S] — pruning-symmetry doctrine (every adding flow gets a review-gated
  pruning counterpart) → PLAYBOOK rule + a prompt-template "obsolescence pass" line.
- **#34** [P3/S] — the 4 posture codifications + the pre-emit prompt checklist
  (header-verbatim, Codex-applicability, context-budget, JOURNAL-read).
- **#112** [P2/M] — the governance wound: `adr_amend.py` helper + ADR immutable-zone
  extension that **resolves the CLAUDE.md §5 self-contradiction** + restamps.
- **#131 / #138** [P2] — floor rollout runbook (shelved) / the gitignore-negation
  install-note fix.
- Also live: **#124** (single-file BUNDLE.md + 05_NOW acknowledgment clause),
  **#132** (organ-index generator), **#1** (fresh-eyes on every handoff).

Reference `BACKLOG.md` for the full queue — do not act on its counts before the re-sync.

## In-progress branches & repo state

- **Branch:** `main`  ·  **HEAD:** `e6154d3` (baseline being handed off).
- This handoff was generated on `docs/handoff-2026-06-09`, which **merges back to
  main** (`--no-ff`) at Phase-2 close — no other feature branch is alive.
- **Working tree at generation:** clean (only the handoff bundle + JOURNAL marker).

## Boundaries

- **NOT hub work** (ADR-41 — do not execute here): the AI Council items
  (#96/#110/#128) live in the **ai-council chat**; the corp items (corp-sca
  `canonical_freshness` restamp, #100/#109/#126) live in the **corp chat**.
- **Do not treat the whole backlog as a pre-rollout gate** — that is the floor mistake
  at backlog scale. Close only what would *propagate* a gap or contradiction.
- **Plugin-guard propagation** (0.1.7–0.1.10 → siblings) waits for the next rollout
  dance — not now.

## How to choose

If `05_NOW` presents multiple candidate first-moves, **propose your choice with
rationale to Rob** — don't ask him to forced-rank. Operator energy is finite; your
job is reasoned pre-selection. Rob confirms or redirects.

## Top landmines (do-not list)

### Session landmines

- **Do NOT** build ahead of need — the build-ahead-of-need pull is this arc's
  recurring trap (the floor was the instance). Spend only where a real gap/contradiction
  would otherwise propagate.
- **Do NOT** declare closure on the easy metric — verify against the original goal,
  not "tests green." The operator had to force this three times this session.
- **Do NOT** act on the backlog's counts/statuses before re-syncing against git.
- **Do NOT** delete `.worktreeinclude` — it is load-bearing, not an orphan.
- **Do NOT** un-shelve the floor absent a real trigger (a collaborator, or genuine
  child-repo pain). Looks-wrong-but-intentional: corp-sca's `.claude/` is gitignored
  so the floor was force-added (#138 fixes with negations; until then edits need
  `git add -f`); corp-sca's `canonical_freshness` FAIL is a separate restamp owed in
  the corp chat.

### Standing invariants (repeat)

- **Append-only** `LESSONS.md` / `logs/TOKEN-LOG.md`; **immutable** ADRs / handoffs /
  transcripts / audits (supersede, never edit in place).
- **Layer 2 never executes** — read-only validators only.
- **No leftovers** — clean up and verify removal of anything you create.
- **OneDrive - Blue Yonder** — never write to or delete inside it.

===== FILE: 05_NOW — end =====
