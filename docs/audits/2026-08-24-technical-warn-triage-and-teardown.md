# WARN triage and teardown record — 2026-08-24 batch close

Completes contract Step 7's triage leg and Step 10's leftovers verification. Written after the
close-out packet because both are measurements taken at the very end of the window.

---

## 1. The four non-row-length WARN classes, triaged

Measured on merged `main` `c5d6bca4`. **The contract's figures for three of the four did not
reproduce**, which is itself part of the intake-`#46` pattern.

### 1.1 `grooming-cadence` — REAL, owed, not actionable by this seat

```
last groom 2026-07-30, 25d ago (> 21d cadence, ADR-41)
```

Contract said 24d; measured **25d**. **Triage: genuine and overdue.** BACKLOG grooming is an
operator/architect act (the 2026-07-17 operator ruling makes the whole open set the unit, and
probe P10 makes it a boot obligation). This seat cannot discharge it, and `banked = 0` forbids
filing a row for it. **Carried to the operator as an owed act, not suppressed.**

### 1.2 `undeclared_edges` — 20 undispositioned, not two

Contract said *"two `undeclared_edges`"*. Measured: **20 undispositioned**, alongside 18 already
dispositioned under `ref #241`. All 20 are ADR-88 FC2 prose edges into exactly two spec ids:

| Target spec | Undispositioned sources |
|---|---|
| `prompt-template` | `BACKLOG.md`, `VISION.md`, `protocols/{HANDOFF_BOOT,HANDOFF_PROCESS,PLAYBOOK,STANDING_RULINGS}.md`, 4 × `docs/intake/*` |
| `handoff-process` | `BACKLOG.md`, `VISION.md`, `protocols/{AI_COUNCIL_PROCESS,ESSENTIALS}.md`, 4 × `docs/intake/*`, `docs/intake/README.md`, `ecosystem/conformance.md` |

**Triage: ONE defect class, not 20 findings.** Every row is the same shape — a doc mentions a spec
without declaring `reconciled_with`. **Not suppressed and not declared**, for a recorded reason:
the memory of this repo is explicit that `reconciled_with` should be declared **only for a coupled
and current edge**, because a stale declared edge is worse than none. Declaring 20 edges to clear a
WARN would manufacture exactly that. **Owner: `[#241]`, open**, which is the same row the 18
existing dispositions cite.

### 1.3 `review_artifact_coverage` — 27, and THIS BATCH made it worse

```
27 code-impact merge(s) since 2026-08-05 carry no linked review artifact
 1 linked artifact carries no parseable **Tally:** line (5af0b33c)
```

Contract said 22. Measured **27** — and the increase is **this batch's own eleven merges**. The
contract calls this *"a live indictment of the reviewer discipline this batch depends on"*, and the
honest reading is sharper: **the batch that was asked to triage the metric is the largest single
contributor to its current value.**

**Triage: real, advisory by ruling, and NOT dispositionable here.** `[#480]`'s P3 ruling keeps the
hard pre-push leg deferred *pending zero false positives over two consecutive windows* — so the
WARN is doing exactly its job, and suppressing it would destroy the evidence the deferral is
waiting on. **Left standing deliberately.**

### 1.4 `reconciled_versions` — one malformed stamp

```
templates/CONTRIBUTING-md-template.md: malformed (reconciled_with not '<spec-id>@<version>')
```

**Triage: a real, small, mechanical defect** in a *template*, already carrying a live disposition
elsewhere in the register under `ref #335`. Not fixed here: `banked = 0`, and this window did not
author that template. **Named so it is not lost.**

### 1.5 `[S24]` — reported, not fixed (contract Step 7)

`validate_backlog` WARNs *"user story with no tasks — `[S24]`"* (`BACKLOG.md:459`). **Cause
identified:** `[S24]` is marked **COMPLETED 2026-08-01**; its rows correctly left `BACKLOG.md` per
ADR-65. The WARN is real; the story is not defective. The latent question — should the validator
warn on a *completed* story that has properly shed its rows? — is left for the architect.

---

## 2. Teardown record and leftovers verification (Step 10)

**Torn down — four lanes, each proven superseded before removal:**

| Lane | Branch | `git cherry main` | Worktree dirt | Mirrored to origin |
|---|---|---|---|---|
| L6 | `worktree-rulings-landing` | EMPTY | 0 | `a85179bd` = `a85179bd` |
| L1 | `worktree-provider-config` | EMPTY | 0 | `3cdf1126` = `3cdf1126` |
| L3 | `worktree-status-grammar` | EMPTY | 0 | `3f663996` = `3f663996` |
| L7 | `worktree-dispatch-codification` | EMPTY | 0 | `1e224c5a` = `1e224c5a` |

Order: `git worktree remove` → `git worktree prune` → `git branch -d`. **`-d` only; `-D` never
used.** Supersession was proven by an **empty** `git cherry`, not by "looks merged".

**Excluded and untouched, with the hold independently confirmed by measurement:**

| Lane | Branch | Uncommitted entries |
|---|---|---|
| L2 | `worktree-funnel-coverage` (`2c6587d5`, locked) | **2** |
| L4 | `worktree-dashboard-commit-path` (`278c26c6`) | **8** |

Both are dirty, which corroborates the contract's hold on independent evidence rather than on its
say-so.

### 2.1 Leftovers verification — two findings, NEITHER deleted

`stale_worktrees` is **OK** (3 registered, down from 7) and `git stash list` is empty. Two things
survive that this seat did **not** remove, because deleting without asking is forbidden:

1. **`.claude/worktrees/lane-docs-governance/` exists on disk but is NOT a registered worktree.**
   It does not appear in `git worktree list` and survived `git worktree prune`. It is a **leftover
   from a previous window** (the `lane-docs-governance` lane recorded at `CLAUDE.md` §12 v2.65),
   and it is a standing breach of `CLAUDE.md` §5 rule 9 — *"any automated or scratch-creating
   process removes and verifies removal of everything it created"*. **Operator call: delete it or
   adopt it.**
2. **A seventh worktree, `probe-substrate` (`c559392a`, locked), is registered and predates this
   batch.** Not a batch lane, not in the queue, not torn down. Named so the next seat does not
   mistake it for batch residue.

**Neither is this batch's residue. This batch's own residue is zero.**
