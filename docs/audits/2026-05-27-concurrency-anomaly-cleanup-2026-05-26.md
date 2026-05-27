---
type: cleanup-record
date: 2026-05-27
basis: 2026-05-26 cross-repo universalization mega-session (multi-prompt, single workdir)
status: resolved
contract: branch-ref hygiene only; no content rewrite; no destructive deletion
---

# Concurrency Anomaly Resolution — 2026-05-26 Mega-Session

## Anomaly summary

The 2026-05-26 cross-repo universalization work ran as several mini-prompts in a
single `.dev-knowledge` working directory. Because branches were created and
switched within one shared workdir, the verification-report content landed on
`main` (commit `ab303c8`, "docs(audits): cross-repo universalization verification
report 2026-05-26") via the normal merge flow, while the **branch named for that
report** — `docs/cross-repo-universalization-verification-2026-05-26` — was left
pointing at an **unrelated** commit, `f532283` ("chore(workspace): remove
redundant Audits/Handoffs/ADRs aliases").

The branch label and its content had drifted apart. The report itself was never
at risk — it is on `main`.

## State at discovery (2026-05-27)

- Verification report content: on `main` at `ab303c8` — **SAFE** (verified
  `git log --oneline main | grep ab303c8`).
- Branch `docs/cross-repo-universalization-verification-2026-05-26`: pointed at
  `f532283` — the **wrong** commit (a workspace-alias cleanup, not the report).
- `f532283` itself: reachable from `main` (merged via `53dd379`), so it was never
  orphaned.
- Stale merged mini-prompt branches still present (already merged to `main`,
  retained as history): `chore/cleanup-stale-scope-tags-reference-2026-05-26`,
  `chore/migrate-ai-council-artifacts-to-docs-audits-2026-05-26`,
  `chore/workspace-aliases-cleanup-2026-05-26`.

## Resolution

**Chosen action: repoint, not delete** (operator decision 2026-05-27 — "skip
branch deletion").

```
git branch -f docs/cross-repo-universalization-verification-2026-05-26 ab303c8
```

The verification branch now points at the commit whose content matches its name
(`ab303c8`). Repointing is non-destructive: `f532283` remains reachable from
`main`, so no commit was orphaned. No branch was deleted; the stale merged
mini-prompt branches were left in place (deletion deferred — they are harmless
merged history and removing them is a separate housekeeping decision).

## Root cause

Two/more prompt cycles sharing a single working directory across one mega-session.
Branch refs were repointed implicitly by the switching cadence, decoupling a
branch's name from its intended content. This is the empirical failure mode that
BACKLOG #5 (git worktree pattern) is meant to prevent: per-task isolated workdirs
remove the shared-ref hazard entirely.

## Forward action

- **BACKLOG #5 (git worktree pattern):** this anomaly is concrete empirical
  evidence supporting it. Recommend the operator elevate its priority — a worktree
  per concurrent task would have made this anomaly structurally impossible.
- **Stale merged branches:** optional future housekeeping (delete the three merged
  `chore/*-2026-05-26` branches) — out of scope here per the "skip branch deletion"
  decision.

## Contract

This cleanup touched only a branch ref (`git branch -f`) and added this record.
No file content was rewritten, no commit was rebased, no branch was deleted, and
`main` was not modified.
