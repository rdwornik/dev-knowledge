---
type: research-preflight
scope: multi-branch consolidation pre-flight state snapshot
date: 2026-05-26
status: snapshot (input to consolidation session)
contract: read-only verification; no destructive op performed before this snapshot
---

# Consolidation Pre-flight Snapshot — 2026-05-26

Captured before any consolidation/merge action, per the session's Phase A. Three
parallel Claude Code sessions (2026-05-25 → 2026-05-26) scattered commits across
branches due to a shared-working-tree race (single `.git/`, single HEAD switched
mid-session). This snapshot records the verified state the consolidation acts on.

## Concurrent-session check
- No active Council debate / python process running (only a passive `ruff server`
  for ai-council). Working tree **clean and stable** across all discovery commands —
  the race has ended. Safe to proceed.

## Branch HEADs (at snapshot)

| Branch | HEAD | Commits above `main` | Notes |
|---|---|---|---|
| `main` | `fe6232d` | — | base |
| `chore/council-debate-force-completion-2026-05-25` | `e10ce30` | 9 | catch-all; holds everyone's scattered commits |
| `docs/council-pipeline-and-docs-taxonomy-audit-2026-05-25` | `a01ff56` | 1 | only the discovery commit; audit/proposal/index missing |
| `docs/ai-council-universalization-audit-and-plan-2026-05-25` (v1) | `ba117d2` | (pipeline chain) | **mislabeled** — points at the pipeline index commit, NOT universalization work; to be deleted |
| `chore/council-debate-execution-2026-05-25-handoff-methodology` | `2006395` | 1 | holds a duplicate of the mechanism-discovery doc |
| `docs/handoff-methodology-council-preparation-2026-05-25` | `233208c` | (merged) | content already in `main` (fe6232d merge); stale |

## chore/force-completion linear history (the pile), `main..e10ce30`
```
e10ce30  README=delete decision recorded in plan       (universalization)
f909768  bring forward mechanism-discovery doc          (UNPLANNED in prompt inventory)
7c1b208  land 5 Council transcripts Q1-Q5               (force-completion)
3efbcd1  ai-council universalization execution plan      (universalization)
f96fed5  ai-council universalization audit refresh       (universalization)
e8ebdcb  Council debate forensics                        (force-completion)
ba117d2  pipeline+taxonomy index                         (pipeline)
b060574  pipeline+taxonomy proposal                      (pipeline)
8ef5f1f  pipeline+taxonomy audit                          (pipeline)
```

## SHA verification (`git cat-file -e`)
All present: `a01ff56 8ef5f1f b060574 ba117d2 e8ebdcb 7c1b208 f96fed5 3efbcd1 e10ce30`
(prompt's 9) **plus two not in the prompt inventory:** `f909768`, `2006395`.

## Untracked-artifact disposition
- Working tree is **clean** — the 2 council-out transcripts seen in the prior session
  were committed by the concurrent process in `7c1b208`.
- `7c1b208` contains exactly the **5** Q1–Q5 transcripts
  (`docs/decisions/transcripts/council-out-20260526_*-handoff-council-Q[1-5]-*.md`).
  No strays to delete, no missing pieces to add.

## Divergences from the prompt's model + dispositions (non-lossy)

1. **`f909768` (mechanism-discovery doc) is unplanned and lives only on the chore
   branch.** The literal plan (`reset --hard main` + cherry-pick only `e8ebdcb 7c1b208`)
   would orphan it. Its content is **byte-identical** to `2006395` (on the execution
   branch), so no unique content is at risk — but if dropped, the doc reaches `main`
   from *neither* branch (the execution branch is not merged).
   **Disposition:** include `f909768` in the chore rebuild (`cherry-pick e8ebdcb 7c1b208
   f909768`). Its commit message says "onto force-completion branch," so that is its
   natural home, and it reaches `main` via the force-completion merge. This **satisfies
   pipeline-audit finding E3** ("mechanism doc branch-local, absent from main — Medium"),
   so it is intent-aligned, not a deviation.
   `2006395` / the execution branch is left untouched (an unmerged duplicate; branch
   deletion not authorized by the prompt).

2. **ADR-43 routing premise verified true.** Phase D rests on "routing is implemented."
   Confirmed: `ai-council/src/ai_council/routing.py` (`TargetResolver`) routes
   transcripts to `<dev_root>/<name>/docs/decisions/transcripts/` from a
   `target-project:` frontmatter field / `--target-project` flag; `settings.yaml`
   `target_projects` includes `.dev-knowledge`; the 5 Q-files carry
   `target-project: .dev-knowledge`. **Nuance:** routing is **opt-in per-invocation**
   (requires a target-project) and mirror writes are best-effort (failure logs a warning,
   per pipeline-audit D2) — the Phase D truth-up text reflects this, not a blanket
   "every debate auto-mirrors" claim.

3. **Phase E target file (`…execution-plan.md`) is not on the consolidation branch**
   (it arrives on `main` only via the Phase C universalization merge). Disposition: after
   Phase C, merge `main` into the consolidation branch so Phases D–G edit the merged
   files; the final operator merge then adds D–G cleanly.

## Reflog tail (abridged)
Shows the race: branch creations interleaved with commits landing on whichever branch
HEAD happened to be on (`checkout main → docs/ai-council-universalization…`, then commits
`8ef5f1f/b060574/ba117d2`, then `checkout → chore/force-completion`, then the
universalization + transcript + mechanism commits). Root cause for BACKLOG entry #5
(git worktree pattern for parallel sessions).

---

**No destructive operation performed before this snapshot.** ai-council inspected
read-only.
