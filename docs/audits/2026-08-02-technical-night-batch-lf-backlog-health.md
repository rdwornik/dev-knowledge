# Night batch 2026-08-02 · lane L-F — backlog & tasks health

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-02 · **Slug:** night-batch-lf-backlog-health
- **Status:** PROPOSAL — read-only night batch, unattended. Nothing filed, closed, reworded or
  deleted. Every verdict below is a proposal for the morning architect.
- **Base:** `main` = `a02dd111` (the post-handoff window-close tip). Clone unshallowed to
  `2026-03-30`, so history claims here are verified, not shallow-limited.
- **Method:** read-only. `tasks/manifest.json` + per-task frontmatter parsed directly;
  `scripts/window_metrics.py` run over the window range; git history queried, never mutated.

---

## 1. Headline

**The backlog did not shrink this window; it grew by 3 (183 → 186), peaking at 194 mid-window.**
Against intake #22 §F — *"The backlog must SHRINK — that is a functional requirement, not a
review item"* — the window is a **miss**, and the shape of the miss is that filing outran
closing 5-to-2.

Two structural facts materially change how §F should be read, and neither is visible in the
"186" headline:

1. **186 is not 186 open rows.** It is **157 `open` + 29 `deferred`**. The deferred pool is
   16% of the count and is a different disposition problem from the open pool.
2. **§F names no number.** It states a direction ("must SHRINK") and a mechanism (the 08-26
   cluster). There is no target figure anywhere in the repo. Any "reduce to N by 08-26"
   arithmetic is therefore an *invented* target — see §5, where one such invention is refuted.

---

## 2. The disk↔manifest delta, explained (23 files)

| Quantity | Count | Meaning |
|---|---|---|
| `tasks/*.md` on disk | 209 | every task file ever written, retained |
| manifest task nodes (`file`+`task` keys) | 186 | the counted rows |
| delta | 23 | 22 files with `status: closed` + 1 `README.md` (no frontmatter) |

**No orphans.** Every manifest node resolves to an existing file (0 missing), and every
disk-only file is either explicitly `closed` or the directory README. This is the ADR-107
§6.3 retire-not-delete convention working as designed — a closed task keeps its allocation
record on disk and leaves the count. **No defect here; verified, not assumed.**

## 3. Distribution (parsed from frontmatter, all 186)

Status: `open` 157 · `deferred` 29

| Priority | Count |
|---|---|
| P1 | 5 |
| P2 | 86 |
| P3 | 95 |

| Size | Count |
|---|---|
| S | 113 |
| M | 67 |
| L | 6 |

| Theme | Count |
|---|---|
| [E2] Enforced governance | 60 |
| [E7] Tooling & evaluation | 40 |
| [E6] Cross-repo universalization | 27 |
| [E8] ARC-5 execution | 20 |
| [E1] Handoff continuity | 11 |
| [E5] Canonical-file integrity | 9 |
| [E3] Lessons feedback loop | 8 |
| [E9] Fleet Desired-State System (North Star) | 7 |
| [E4] Decision management | 4 |

**Read on this shape.** 113 of 186 are size-S and 95 are P3 — the pool is dominated by small,
low-priority rows. That is the profile of a backlog that shrinks by *disposition* (batch-rule a
class out) far faster than by *execution* (work rows off one at a time). [E2] alone is 60 rows,
a third of everything.

## 4. Staleness scan — the method failed, and that is the finding

A staleness scan keyed on "no commit touched this task file in >21 days" returns **0 rows**.
That result is **vacuous, not clean**: commit `9bd0d719` (2026-07-27, `[#433] module 3 —
generated tasks/ tree`) created 174 task files in a single migration commit, resetting every
file's git mtime to that date. Nothing in `tasks/` can be older than 2026-07-27 by that measure.

**Consequence:** file-mtime staleness is unusable as a grooming signal in `tasks/` until enough
post-migration history accrues. A grooming organ built on it would report a clean bill for
reasons unrelated to the backlog's actual age. Recommend any future staleness check key on the
row's own cited evidence dates, not the file's git date.

## 5. §F projection — the arithmetic, and one refuted figure

**Verified window figures** (`scripts/window_metrics.py f7abe228..HEAD`, computed not carried):

```
183 -> 186 rows
filed 5   (#463, #464, #465, #470, #472)
closed 2  (#458, #459)
net +3
```

Row-count trace across the window's first-parent merges: 183 → 185 → 189 → 190 → **194** →
191 → 189 → 188 → **186**. The pool peaked at 194 and was drawn back to 186 by the close.

**Days to the 2026-08-26 cluster:** 25 (from 2026-08-01).

**Windows remaining — a JUDGMENT INPUT, not a measurement.** `window_metrics.py` deliberately
refuses to compute this ("a judgment INPUT, not an observation ([#461]); supply it from the
ladder analysis, do not derive it"). Recent windows have run 2–11 days. At that spread, 25 days
is **≈3–8 windows**. Stated as a range with its basis, per the metric's own contract.

**The required rate, honestly framed.** §F sets no target number, so the only defensible
statement is directional:

- To merely **HOLD** at 186, the close rate must equal the file rate — currently **5 filed per
  window vs 2 closed**. Closing must roughly **2.5×**.
- To **SHRINK** at all, closes must exceed files every window.
- At the observed **+3/window** over ≈3–8 remaining windows, the 08-26 projection is
  **≈195–210 rows** — i.e. the functional requirement is currently being **violated**, and
  passively continuing produces a *larger* backlog at the cutoff, not a smaller one.

**REFUTED — a figure that must not propagate.** A rate of "+52.8 adds/week, backlog growing at
+52.2/week" was derived in-lane from `git log --diff-filter=A -- tasks/` over the last four
weeks. It is an **artifact of the ADR-107 migration**: of ~211 file-adds in that span, **174
came from the single commit `9bd0d719`**, which generated the tasks/ tree rather than filing
work. The true filing rate is 5 per window. Recording the refutation here because intake #16 §5
lesson 6 ("Verify numbers before they propagate") names exactly this failure class, and the
10–20-repo incident is its precedent.

Likewise **refuted**: a "target 150 rows (25% reduction)" figure. No such target exists in §F or
anywhere else in the repo. It was invented in-lane. **Do not adopt it.**

**2026-08-26 references found in-repo:** `BACKLOG.md:329` (silent-rule drain `review_date`),
plus rows [#348] (backlog grooming routine) and [#426] (routine consumer declaration). These are
gates *at* the date, not a count target.

## 6. Groom candidates — the auto-generated list did not survive review

A 12-row groom list was produced in-lane. **Four were spot-checked against their own Done-when
clauses and all four failed**, so the list is reported as **UNRELIABLE** rather than forwarded:

| Row | In-lane verdict | Adjudication | Evidence |
|---|---|---|---|
| [#465] | close-candidate | **REJECT** — row states legs 2–4 explicitly remain (same-day digest overwrite, hub-identity flap, tag-canonicity self-disabled). Only leg 1 landed (`80e743a`). | `tasks/465-*.md` |
| [#452] | close-candidate | **REJECT** — Done-when unmet: the `depends-on` clause is still absent on both `tasks/433-*` and `tasks/382-*`; nothing was written or recorded. | `tasks/452-*.md` |
| [#457] | defer | **REJECT** — both live-repo test failures are unfixed; the row's own instruction is to census before repinning. | `tasks/457-*.md` |
| [#455] | reword | **REJECT** — no check exists; `registry.md` is still read by nothing but an exclusion in `fleet_analytics.py`. | `tasks/455-*.md` |

This matches a known pattern in this repo: the 2026-07-09 architect triage rejected **39/39**
auto-generated WEAK closure proposals (JOURNAL). A groom list generated without reading each
row's Done-when reproduces that defect.

**The two groom observations that DO survive scrutiny** — both narrow, both evidence-backed:

1. **[#463] and [#464] carry an EVIDENCE GAP clause that is now stale.** Both state verbatim
   that "51 further baseline commits … exist **LOCALLY ONLY** — unpushed and unread". [#460]
   closed this window with the title "REPLICATION MECHANIZED: push leg + divergence alarm live,
   **origin current**". If origin is current, the clause is false as written.
   **Verdict: REWORD candidates** (not close — the underlying findings are untouched).
   The evidence question is lane L-B's; see the L-B report for whether the 51 actually landed
   and whether they change either row's findings.
2. **The 29 `deferred` rows are an unexamined disposition class.** They are 16% of the count and
   no row owns their review. If §F wants the count down, a single ruling over 29 rows is the
   cheapest available lever — cheaper than any execution plan. **Proposal:** the architect
   decides whether `deferred` rows count against the §F number at all.

## 7. Rows whose text contradicts landed state

Beyond the [#463]/[#464] evidence clause above, one further contradiction is confirmed:

- **[#472]** ("Census must diff the ADR-104 declaration against machine surfaces — no loadable
  declaration source exists yet") — the ADR-109 2026-08-01 amendment records that
  `terminal-setup` now "reports declared-but-not-deployed **as data at PASS**" via
  `check_membership_agreement` ([#462], landed `d48ebd6`). The row's premise that no declaration
  source is loadable needs re-checking against that check. **Verdict: verify-then-reword**, not
  close — `resolve_fleet_members` was deliberately *not* widened (a named §2 ruling), which is
  the part of [#472] that plainly survives.

## 8. Blocking questions for the architect

| # | Question | Decision shape |
|---|---|---|
| F-1 | What is the §F target number at 2026-08-26? Direction alone cannot be gated. | A number, or an explicit "directional only, no gate" |
| F-2 | Do `deferred` rows (29) count against the §F number? | Yes / No / re-disposition them as a batch |
| F-3 | Is a filing-rate cap wanted, given filing outran closing 5:2? | Cap / no cap / cap only on P3-size-S |

---

*Read-only night batch. No file under `tasks/` or `BACKLOG.md` was read-modified; nothing was
filed, closed, or reworded.*
