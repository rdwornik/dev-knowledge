---
intake-id: 71
status: DRAFT
origin: architect verdict on the Python quality & speed research arc, ARCHITECT-INBOX-2026-09-05-004 item A.2; source audit docs/audits/2026-09-05-technical-research-python-quality-speed.md (1060 lines) on worktree-research-python-quality @ e95a4f15
consumed-by:
---

# Batch P — audit-gate speed from measured spawn and re-read cost

> **Proposed row shape when this is ratified:** theme `[E7] Tooling & evaluation`, size **M**,
> as directed by the architect verdict. Recorded here rather than in frontmatter because the
> intake schema (`docs/intake/README.md` §3) carries no theme/size keys — those are backlog
> fields, and inventing frontmatter keys REDs the tree manifest.

> **RECONCILE-BEFORE-BIRTH — READ THIS FIRST. This intake OVERLAPS `intake-id: 54`
> (`docs/intake/2026-08-26-tech-loop-tax-and-gate-performance.md`, status READY), and the
> overlap is not incidental.** Both describe the same program from different evidence, and
> **both use a "P-n" vocabulary that does not agree**:
>
> | this intake | #54's name | same work? |
> |---|---|---|
> | P1 — one `git log` per handoff-bundle dir | **P-1** journal-anchor single-pass inversion | same *shape* (collapse a per-dir walk to one pass), different call site |
> | P2 — git-spawn consolidation into one in-memory index | **P-2** spine parent-map in one git process | yes, P2 is the general case of #54's P-2 |
> | P3 — read-through file cache per run | **P-5** shared corpus loader | yes |
> | P4 — arm ruff `N` naming rules | *(absent from #54)* | no — this is the quality-doctrine half |
> | *(absent here)* | **P-3** `[#529]` telemetry window | no — and #54 makes P-3 a *precondition* |
> | *(absent here)* | **P-4** commit/ship tiering | **already landed as `[#597]`** |
>
> **Two live "P-n" vocabularies for one performance program is a defect, not a coincidence**, and
> whichever is kept, the other must be retired by name — this is Open question 1 and it is the
> first thing to decide, before any lane is scheduled. Note also that #54 rules **P-3 telemetry
> lands BEFORE any retiering**; nothing in this intake is a retiering, so that gate is not
> tripped, but the ordering claim belongs to #54 and is not re-litigated here.

## Problem / motivation

**The audit gates cost more than the work they gate, and the cost is architecture rather than
language.** Measured on real runs with paired A/B, not estimated:

| measurement | value |
|---|---|
| `audit.py ship-gate` wall-clock | **664 s** |
| `audit.py health` wall-clock | **75 s** |
| git process spawns, `health` | **159** |
| git process spawns, `ship-gate` | **1,307** |
| git's share of both gates | **75–79 %** |
| file re-reads, `health` | **5,191 of 5,985 (87 %)** |
| file re-reads, `ship-gate` | **15,356 of 15,578 (99 %)** |
| the single worst site (`audit.py:2345`, one `git log` per handoff-bundle dir) | **118 spawns / 46.374 s → 1 spawn / 0.347 s**, all 118 add-dates identical |

**What the arc REFUTED matters as much as what it found**, and both are recorded so neither is
re-litigated: the cost is **not** the interpreter and **not** `audit.py`'s length (mean cyclomatic
complexity ~7; four F-rank functions in 1,620), and a **Rust rewrite is REJECTED on measurement**
— the compiled ceiling is **1.33×**, which cannot pay for a rewrite when 75–79 % of the time is
spent in `git` subprocesses that a rewrite does not remove.

**Why this is a governance intake.** These gates run at every commit (`audit-health`) and at every
ship. A 664-second ship-gate is not slowness in a tool; it is a tax on every arc the batch protocol
runs, and it is the reason sessions reach for `--no-verify`. A gate people route around enforces
nothing.

## Scenarios (+1 view)

- As the **integrator**, I run the merge queue serially and pay `audit-health` per commit; at 75 s
  a ten-commit queue spends over twelve minutes inside the gate alone, so I batch commits to avoid
  it — which is exactly the behaviour the per-commit gate exists to prevent.
- As a **lane seat**, I finish work and want the ship-gate verdict; at 664 s I start it and context-
  switch away, so the verdict arrives after I have moved on and is read as a formality rather than
  a decision point.
- As the **operator**, I ask whether a governance change is safe; the honest answer today is
  "the gate says so, eleven minutes from now".

## Functional requirements

- **Must — P1: collapse the handoff-bundle add-date walk to one git call.** `audit.py:2345` spawns
  one `git log` per bundle directory. Measured A/B: **118 spawns / 46.374 s → 1 / 0.347 s**, with
  **all 118 add-dates identical** between methods. This is separable from the rest and the
  architect has already routed it as a **serial hotfix ahead of the batch** (004-B), not a lane.
- **Must — P2: one git pass per run, consumed by every check that currently spawns per file or per
  directory.** Today: 159 spawns in `health`, 1,307 in `ship-gate`. Required outcome: **≥ 5× fewer
  spawns**, with **verdicts byte-identical** on the live tree (a diff of both gate outputs must be
  empty).
- **Must — P3: a read-through file cache per run, keyed on path + mtime.** Today: 5,191/5,985 and
  15,356/15,578 reads are re-reads. Required outcome: opens counted before/after, outputs
  byte-identical, and **no cache persists across runs** — a stale cache would make a gate lie,
  which is worse than a slow gate.
- **Must — P4: arm the RULED half of the quality doctrine.** PEP 8 naming (ruff `N` rules) costs
  **13 fixes, 12 of them one `N818` rename**. ADR-108 §B-4 is a DECIDED question with **no carrier**
  — it arms no gate today — and `[#502]` closed as a report-only ratchet. Arming `N` gives B-4 its
  carrier line. **The complexity families (134 fixes) are explicitly NOT armed**: `[#609]`'s
  exclusion stands and this intake does not reopen it.

## Acceptance criteria (ex-ante)

1. `audit.py ship-gate` wall-clock **664 s → ≤ 200 s**.
2. `audit.py health` wall-clock **75 s → ≤ 25 s**.
3. **Verdicts byte-identical** across the change for both gates on the live tree — this is the
   criterion that makes the speedup admissible at all; a faster gate that decides differently is a
   different gate.
4. Spawn counts and open counts printed **before and after**, per lane, from the same tree.
5. P4 only: ruff `N` enabled in `pyproject.toml` + pre-commit, the 13 fixes landed, and ADR-108 §B-4
   carries a line naming the sha that armed it.
6. **Library-first: no new dependency.** git plus stdlib caching. (This is an acceptance
   constraint the architect set, recorded here because it bounds the solution space rather than
   describing a solution.)

## Non-goals

- **A Rust or compiled rewrite — REJECTED, MEASURED (1.33× ceiling).** Recorded so it is not
  re-proposed.
- **`audit.py` decomposition.** Blocked on test-monkeypatch coupling; the blocker is recorded, and
  scheduling it is not this intake's business.
- **Re-tiering which checks run at which stage.** That is #54's P-4, already landed as `[#597]`,
  and #54 gates any further retiering behind its P-3 telemetry window.
- **Complexity/refactor lint families.** `[#609]`'s exclusion stands.

## Impact sketch (4+1 lite)

- **Logical:** one new per-run index/cache layer consumed by existing checks; no check changes its
  question, only where its facts come from.
- **Development:** three hot-path changes (P1, P2, P3) plus one lint arming (P4). P1 is separable
  and is already routed as a serial hotfix.
- **Process:** lanes in worktrees, integrator serial, after the H0-prep merges — the ordinary batch
  shape.
- **Risk:** the byte-identical-verdict criterion is the whole safety argument. A per-run cache that
  outlives its run, or an index built from a different git query than the check assumed, changes a
  verdict silently — which is why criteria 3 and 4 are stated ex-ante rather than checked at the end.
- **+1 scenario:** the integrator runs the queue and the per-commit gate is no longer the reason to
  batch commits.

## Open questions

1. **Which "P-n" vocabulary survives — this one or `intake-id: 54`'s?** They disagree on the same
   work (see the table above). Whichever is kept, the other must be retired *by name*, and the
   rows already born against #54's names (`P-1`, `P-2`, `P-4`, `P-6`) must be re-pointed or left
   alone deliberately. **This is a functional question and therefore the operator's to rule**
   (ADR-108 §A).
2. **Does this intake supersede #54, narrow it, or sit beside it?** #54 is broader (suite time,
   generated-file merge conflicts, corpus accumulation) and is status READY; this one is narrower
   and carries the measured spawn/re-read evidence #54 lacked. Superseding a READY intake is a
   decision, not a tidy-up.
3. **Is `[#529]`'s telemetry window (#54's P-3) a precondition here?** #54 rules it a precondition
   for *retiering*. Nothing here retiers, so the letter of that gate is not tripped — but P2 and P3
   would be easier to argue with per-check cost data in hand, and cheaper to verify.
4. **Where does the ADR-108 §B-4 carrier line live** once ruff `N` is armed — in the ADR, in
   `pyproject.toml`'s rationale, or both? The gap is that B-4 is decided and carried nowhere.

## Status

**DRAFT** — filed 2026-09-05 by the FILINGS-3 seat from the architect's verdict in
ARCHITECT-INBOX-2026-09-05-004 §A.2. Not yet ratified; the reconciliation with `intake-id: 54`
(open questions 1 and 2) is the gating decision and belongs to the operator, not to this seat.
