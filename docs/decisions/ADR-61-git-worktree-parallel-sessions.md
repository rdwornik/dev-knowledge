---
adr: 61
title: Git Worktree Pattern for Parallel Claude Code Sessions
status: Accepted 2026-05-28
date: 2026-05-28
---

# ADR-61: Git Worktree Pattern for Parallel Claude Code Sessions

## Context

Concurrent Claude Code sessions sharing a single working tree caused repeated race
conditions (2026-05-26/27, ≥3 incidents). One working tree has one HEAD; two sessions
committing and branching collide, scattering commits and requiring 1-2h cleanup each.

Evidence:
- `docs/audits/2026-05-27-concurrency-anomaly-cleanup-2026-05-26.md` — branch ref
  decoupled from its named content; repoint required.
- `docs/archive/2026/2026-05-26-consolidation-preflight.md` — reflog showing HEAD
  switching mid-session across three concurrent prompts.
- BACKLOG #5 escalated P2 → P1 after second incident on 2026-05-27.

## Decision

### When parallelism is already safe (no worktree needed)

Sessions in **different repos** are isolated by separate `.git/` directories. Run them
in parallel freely — no worktree needed.

Cross-repo orchestration from one session (sequentially `cd`-ing into multiple repos)
is also safe; it is sequential, not parallel, and each write targets a distinct `.git/`.

### When a worktree is required

**Two or more sessions on the SAME repo** require separate working trees via
`git worktree`. Each gets its own working directory, its own HEAD, and a distinct branch.
Git enforces the per-branch invariant: the same branch cannot be checked out in two
worktrees simultaneously.

> ⚠️ **SUPERSEDED (mechanics only) — do NOT use the `<repo>-parallel` sibling-dir recipe below.**
> The decision (same-repo parallelism requires a worktree) still stands, but the *mechanism* was
> replaced by the **native in-repo worktree convention** (#107, 2026-06-07): `claude --worktree
> <name>` → `.claude/worktrees/<name>/` on branch `worktree-<name>`. **Live procedure → PLAYBOOK
> §"Parallel sessions & worktree discipline"** (cold-start runbook). The adjacent `<repo>-parallel`
> sibling dirs this section describes spawned the `.dev-knowledge-cadence` / `.dev-knowledge-night-adr`
> rule-9 orphans; do not recreate them. The blocks below are preserved as point-in-time history.

### Setup (operator, before opening a 2nd same-repo session) — ❌ SUPERSEDED, use native (see PLAYBOOK)

```
git -C <repo> worktree add <repo>-parallel main   # ❌ SUPERSEDED — use native: claude --worktree <name> (see PLAYBOOK)
```

Example for `.dev-knowledge`:

```
git -C C:\Users\1028120\Documents\Dev\.dev-knowledge worktree add ..\..dev-knowledge-parallel main   # ❌ SUPERSEDED — use native (see PLAYBOOK)
```

Open the 2nd Claude Code session from inside the worktree directory. Each session
immediately creates its own feature branch (git prevents two worktrees on the same
branch, so each must diverge before meaningful work begins).

### Cleanup (after merging the parallel branch into main) — ❌ SUPERSEDED, use native (see PLAYBOOK)

```
git -C <repo> worktree remove <repo>-parallel   # ❌ SUPERSEDED — native teardown in PLAYBOOK §"Parallel sessions & worktree discipline"
git -C <repo> worktree prune
```

### Naming convention — ❌ SUPERSEDED by `<issue#>-<kebab-slug>` (see PLAYBOOK)

- ~~`<repo>-parallel` — ad-hoc single concurrent session~~ ❌ SUPERSEDED
- ~~`<repo>-wt-<purpose>` — when multiple concurrent worktrees are needed simultaneously~~ ❌ SUPERSEDED

### Rules

1. **Primary tree stays on main; worktrees hold feature branches.**
2. **One branch per worktree** — git-enforced; cannot be bypassed.
3. **Pre-flight `git worktree list`** before starting any parallel same-repo work.
4. **Merge in primary tree**, then `git worktree remove`.
5. **Prompt hard-stops** — CC prompts for same-repo parallel work must verify they are
   in the expected worktree (check `pwd` vs expected path) before proceeding.

## Consequences

**Positive:**
- Safe same-repo parallelism; no more commit-scatter or HEAD-drift cleanup.
- Each session operates on its own branch from the start; merges are explicit.
- Faster throughput when work is genuinely parallelizable across a single large repo.

**Risks:**
- Operator must remember setup/cleanup; stale worktrees accumulate if not pruned.
  Mitigated by `git worktree list` pre-flight and `worktree prune` habit.
- Two worktrees cannot share a branch — a deliberate constraint, not a bug.

**Trade-off:** ~60s setup overhead vs 1-2h of race-condition cleanup per incident.
