# Night batch 2026-08-09/10 (cloud lanes N-A · N-B · N-C) — end-of-batch packet

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-10 · **Slug:** batch-night-cloud-packet
- **Closes:** `docs/audits/2026-08-10-technical-batch-night-cloud-manifest.md` (`batch: 0`,
  committed `737dd479`) — this file is the path that manifest named in `closed_by:`, so committing
  it is the single act that discharges the batch. No edit anywhere expires it; only this landing.
- **Integrator:** CC (Opus 5), hub **primary checkout**, no worktree, `main` from `e67fb8db`,
  integration branch `docs/arc5-night-batch-archive`.
- **Content record:** the three lane reports themselves. This packet is the *process* record.

---

## 1. Per-lane delivery — 3 of 3 delivered, 3 of 3 merged, nothing abandoned

All three lanes ran in **one cloud session against one branch**, so there is one tip and one merge
rather than three.

| Lane | Subject | Report | Lines |
|---|---|---|---|
| N-A | Satisfied-row census | `docs/audits/2026-08-10-technical-satisfied-row-census.md` | 228 |
| N-B | Decision-sheet verification | `docs/audits/2026-08-10-technical-decision-sheet-verification.md` | 215 |
| N-C | Origin branch census | `docs/audits/2026-08-10-technical-origin-branch-census.md` | 173 |

- **Branch:** `claude/night-batch-cloud-lanes-a4mpkp`, tip **`fe81e896`**.
- **Merge:** **`19aca464`**, `--no-ff`, into the integration branch.
- **Declared-path conformance: 3 of 3 EXACT.** Every report landed at the path the manifest's lane
  table names — checked against the table rather than assumed, because that table is load-bearing
  twice (the file-disjointness guarantee and closure condition 1).
- **No branch was found that the manifest omitted, and none was planned-but-absent.** The remaining
  unmerged remote set is `automation/fleet-audit` and the six `claude/conformance-*` dailies; both
  classes are explicitly out of this batch's scope and **neither was touched**.

### 1a. The one merge conflict, and how it was resolved

`docs/audits/README.md` conflicted — both sides rewrote its count line and its `2026-08` group (the
branch to 455, the manifest commit to 453). **Resolved by regeneration, never by hand**:
`gen_audit_index.py --write` over the merged tree, then `--check` exit 0, then a grep confirming
zero conflict markers reached the staged blob. Final count **456** = 452 on `main` + 1 manifest + 3
lane reports. Hand-picking a side would have produced a number matching no tree.

## 2. Velocity — the filter travels with the number (STANDING_RULINGS H2)

| Metric | Value |
|---|---|
| **Opened** | **0** |
| **Closed** | **0** |
| **Net** | **0** |
| **Open-total (live: `status: open` + `status: deferred`)** | **196** |
| Open-total (narrow: `status: open` only) | 170 |

**Measured after this arc's final generator run, reconciled across two independent reads that
agree:** `tasks/` frontmatter → 170 `open` + 26 `deferred` = 196 (254 files total: 170 open, 55
closed, 26 deferred, 1 superseded, 1 retired, plus `tasks/README.md` which carries no frontmatter
and is not a row); `validate_backlog` → **196 tasks** (9 themes, 26 stories, 1 warning — a
pre-existing `[S24]` story-with-no-tasks WARN, not introduced here).

**The denominator is the live count** per H2, because a deferred row is not a closed row and a close
would have to retire it too. The narrow reading is printed beside it so the two cannot be confused
by the next seat — one earlier window carried both 169 and 202 as "the open total" and both were
correct.

**Zero rows were born, closed, edited, deferred or un-deferred** by this batch or by the arc that
archives it. The net-0 is a fact about the batch, not a rounding.

## 3. Width delta — dispatched 3, closed 3, delta 0

The **count** matched. The **shape** did not, and the divergence is recorded because it changes what
a lane's evidence is worth:

- **Dispatched as:** 3 lanes, read-only, file-disjoint by report path.
- **Ran as:** 3 lane sections delivered to **one** cloud session, which may push only its assigned
  branch. So the lanes are file-disjoint but **not process-isolated** — they share one context, one
  clone, and one gate posture. Three reports from one session are not three independent reads.
- **Consequence for the reader:** the reports' agreement with each other is weaker evidence than
  three separate lanes' agreement would have been. Their agreement with the *tree* is unaffected,
  and that is what this arc re-derived independently for the claims it acted on (§4).

## 4. Closure contract — all three conditions met

1. **All three reports merged to `main`** — via `19aca464`, which reaches `main` through this arc's
   integrating merge.
2. **The JOURNAL anchor `fe81e896` created and could not discharge is attached by this arc** — it
   lands as the last commit before push, naming this merge's contents. The lane never journals; the
   integrator does.
3. **This packet reports opened / closed / net / open-total with its filter named, and the
   dispatched-vs-close width delta** — §2 and §3.

**Not a closure condition, and deliberately not manufactured into one:** each report's
`## Needs a ruling` section. Those are architect input for the batch-4 planning GO. The dispatch did
not carry an adjudication obligation and this packet does not invent one.

## 5. Gate posture — the integrating arc's, not the cloud clone's

The lanes declared their own posture honestly (hand-run, not gate-passed; `uv 0.8.17` against the
`==0.11.19` pin makes every `uv run --locked` hook entry refuse, and the clone's `.git/hooks/` held
only samples). **That posture is superseded by this arc's**: every commit of the integration ran the
full local gate set — `normalize-dated-headers`, `audit-index-freshness`, `validate-hermetization`,
`audit-health`, `backlog-id-on-close`, `backlog-filing-backpressure` — with **zero `SKIP=`, zero
`--no-verify`, zero force-pushes, zero deletions**. Full-suite, `audit.py health` and ship-gate
results are reported in this arc's JOURNAL entry.

The uv-pin recurrence is the **fourth** fleet-wide and the second consecutive night. Already carried
as intake #27 §A row 36 with a PROPOSED (not ruled) class change. Recorded, not ruled.

## 6. What this batch produced, in one line each

- **N-A** — **zero** fully-satisfied rows in the ~22 deep-tested of 53 that intersect recent work;
  **132 of 170** open rows carry prose-only Done-when clauses and cannot be tested mechanically at
  all. Five partially satisfied with a named smallest act, best `[#390]`.
- **N-B** — 24 claims on the decision surface: **15 verified, 2 refuted, 1 partial, 6 unverifiable**.
  Both errors were *inherited* claims; every *measured* claim was correct.
- **N-C** — `origin` carries **8 heads**, zero deletion candidates, no branch an ancestor of `main`;
  `automation/fleet-audit` is an orphan with its own root protected by no written clause; six
  conformance digests absent from `main`.

Two of these were re-derived independently by this arc rather than inherited:
`docs/audits/2026-08-10-verification-ruled-dispositions-and-digest-gap.md` verifies four ruled
dispositions (4 of 4 landed) and establishes the digest gap as a **broken step**, naming it. That
file is the discharge of N-C's open question, not a restatement of it.

## 7. What this packet deliberately does NOT do

- **It merges no conformance digest.** Establishing the gap was this arc's task; consuming six
  nights of findings is an operator act (§2.6 of the verification artifact).
- **It closes no BACKLOG row**, including `[#419]` and `[#426]`, which the digest gap is evidence
  against rather than evidence for.
- **It reaps no branch.** `claude/night-batch-cloud-lanes-a4mpkp` is left standing for the operator,
  consistent with this arc touching no branch lifecycle.
- **It adjudicates nothing.** Every `## Needs a ruling` item stays open for the architect.
