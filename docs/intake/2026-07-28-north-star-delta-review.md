---
intake-id: 20
status: DRAFT
origin: "operator-ordered delta review, 2026-07-28 — recording batch R3; compares the operator's local copy C:/Users/1028120/Downloads/FLEET_NORTH_STAR_2026-07-21.md (read-only, never entered the repo) against in-repo intake #16"
consumers: "operator ratification; then the [E9] sequencing session ([#382] → [#383] → [#385]) and the [#388] figure-correction lane"
note: "NON-CITABLE UNTIL RATIFIED. Status DRAFT — no ADR, backlog row, or handoff may cite this document as authority until the operator ratifies it. It records STATUS, it does not rule anything. Operator's driver, recorded verbatim at his instruction: nothing agreed gets lost."
---

# North Star delta review — local 2026-07-21 doc vs in-repo intake #16

**Reading contract.** Status **DRAFT** → **non-citable until ratified** (`docs/intake/README.md`
§5). Nothing here is a decision. Every status below is backed by a commit sha, an ADR id, or a
BACKLOG row read live on 2026-07-28 at `main` `6195d932` — **never from memory**. Where a claim
could not be evidenced, it is marked so rather than softened.

**Driver (operator, 2026-07-28), recorded because it is the reason this document exists:**
*nothing agreed gets lost.*

**Sources compared:**

| Side | Path | Note |
|---|---|---|
| Local | `C:/Users/1028120/Downloads/FLEET_NORTH_STAR_2026-07-21.md` | 113 lines / 13,474 bytes. Read-only; **never enters the repo verbatim** |
| In-repo | `docs/intake/2026-07-21-func-fleet-north-star.md` | 121 lines / 13,910 bytes. Intake **#16**, status DRAFT |

---

## 1. (i) Items in the local doc ABSENT from the in-repo version

**ZERO. Nothing was lost in the consumption.**

This is a measured result, not an eyeball pass. Stripping the 7-line intake frontmatter from the
in-repo file and diffing the remainder against the local doc yields exactly one hunk, and it is
not content:

```
--- Downloads/FLEET_NORTH_STAR_2026-07-21.md
+++ docs/intake/2026-07-21-func-fleet-north-star.md (frontmatter stripped)
@@ -1,3 +1,4 @@
+
 # FLEET NORTH STAR — Consolidated Vision & Plan
```

A single added blank line after the frontmatter fence. **No prose, table row, list item, figure,
recommendation, or constraint differs** — §0 through §6 and the closing seed note are
byte-identical across both copies.

**Consequence for this review.** Because (i) is empty, the whole of the local doc is already the
in-repo doc, so §2 below statuses the *in-repo* text and covers the local text by identity. The
one thing the in-repo copy adds is the frontmatter — `intake-id: 16`, `status: DRAFT`,
`consumers:` naming the two consuming sessions, and an **empty `consumed-by:`**, which is itself
a live signal: intake #16 is still DRAFT and has never been formally marked consumed, even though
two of its consumers have since produced ADRs (§2 steps 1–2).

---

## 2. (ii) Per-item status — 15 tracked items

Scope: the 7 sequenced plan steps (§6), the 7 codified lessons (§5), and the 1 hygiene item
carried in §0. The §1 layer table is state-of-the-world rather than a work item, so it is
statused separately in §4. §4's polyrepo inputs are superseded wholesale — §3.

**Tally: 6 DONE · 1 IN-PROGRESS · 8 NOT-STARTED.**

### 2a. §6 plan steps (7)

| # | Item | Status | Evidence (live, 2026-07-28) |
|---|---|---|---|
| 1 | **Close `assets/`** — push from ai-council main | **DONE** | Merge `88b0876` (`chore/dissolve-assets`) is on ai-council **`origin/main`** — verified via `git -C ../ai-council branch -r --contains 88b0876`. Cited back in `protocols/PLAYBOOK.md:3630` as the proving run |
| 2 | **Polyrepo ruling session** → first shape ADR | **DONE** | **ADR-104** *Fleet repository shape — partial fold on engineering grounds; polyrepo mostly retained*, Status **Accepted**, Date **2026-07-24**; merged `92fabb51`, which closes **[#381]**. ADR-104 cites `Intake: #16 §4`, so the seam held. **Supersedes §4 — see §3** |
| 2b | ↳ correct **10–20 → 5–8+** in the 3 handoff files | **NOT-STARTED** | **[#388]** still OPEN (`BACKLOG.md:159`). The only commit touching the figure is `2da5da22`, the ingestion merge that *filed* the correction as a ticket. The fabricated figure is still in the downstream handoff files |
| 3 | **Desired-state intake → ADR** (pydantic + networkx + pandas) | **NOT-STARTED** | **[#382]** OPEN, **[P1][M]** (`BACKLOG.md:421`). No schema is committed; no ADR cites it. Adjacent but **not** this item: ADR-107 (Proposed) declares a fleet-owned schema for BACKLOG only |
| 4 | **Execution waves per surface** | **NOT-STARTED** | **[#383]** OPEN, gated `depends-on: 382`. No wave has opened; no divergence report exists |
| 5 | **L5a analytics lane** — PyDriller mining | **DONE**, with a named carve-out | Built at `5631660c` (`feat(analytics): L5a descriptive fleet mining — hotspots, coupling, rot [#384]`); **[#384] closed** at merge `ffba8dd8` / `37844c2a`, Done-when verified against `09c50cc0`/`a6b326f1`/`09e4d707`. **Carve-out: the "nightly lane" half is NOT true** — nothing invokes `scripts/fleet_analytics.py`; it is manual CLI only, filed as **[#391]** (open). [#392]/[#393]/[#394] are open follow-ups from the first real run |
| 6 | **L4 tech-currency lane** | **NOT-STARTED** | **[#385]** OPEN, gated `depends-on: 383`. Doubly blocked (382 → 383 → 385) |
| 7 | **L5b predictive** — risk scoring | **NOT-STARTED** | No BACKLOG row exists. Correctly so — the doc itself gates it on "L5a shows signal volume", and step 5's frames have run once, not enough to trip that gate |

### 2b. §5 lessons codified (7)

| # | Lesson | Status | Evidence (live, 2026-07-28) |
|---|---|---|---|
| 1 | **One data model, not N registries** | **NOT-STARTED** | Its only vehicle is **[#382]** (open, above). The 4-registry sprawl the doc names is undissolved; `ecosystem/` still carries separate registries |
| 2 | **Decide the bet before building its machinery** | **DONE** | The standing brake ("no new fleet machinery before [#381] rules") was **discharged** by ADR-104 at merge `92fabb51`; the discharge is recorded in-place at `BACKLOG.md:417` ("**The brake is DISCHARGED**"), so the rule was applied and then released rather than quietly dropped |
| 3 | **Prove, then codify** | **DONE** | `protocols/PLAYBOOK.md:2590` states it as a rule (with its threshold — *one shipped run*, explicitly lower than Ch11's n=2) and §21 landed at merge `db878f4c` ([#386]). **NOTE: [#386] is closure-eligible but still OPEN** — see §5 |
| 4 | **Witnessed, not merged** | **DONE** | Same landing `db878f4c`: PLAYBOOK §21 makes **gate 7 OPERATOR WITNESS** an ordered gate *after* the merge, and states "**Merged ≠ done**" — "A lane that stops at the merge has completed six of eight" |
| 5 | **Adopt the model, not the tool** | **IN-PROGRESS** | Applied in the ruling layer — ADR-104 took a *partial fold* rather than a tool-shaped binary, and the doc's own Copier precedent is settled. But **[#387]** is OPEN: intake **#2** still argues FOR the rejected template engine, and **[#371]** names that stale intake as its deciding vehicle — so the un-rewritten argument is load-bearing on open work |
| 6 | **Verify numbers before they propagate** | **NOT-STARTED** | The lesson's own worked example is still unrepaired: **[#388]** open (2b above). A lesson about propagating figures whose triggering figure is still propagating is not yet codified in any enforcing sense |
| 7 | **Meta serves object** | **NOT-STARTED** | No codification and no ticket. `grep -in "meta serves object" protocols/PLAYBOOK.md protocols/ESSENTIALS.md` → **zero hits**. This is the only §5 lesson with neither a rule nor a row — it is the one at genuine risk of being lost, which is exactly the class the operator's driver names |

### 2c. §0 hygiene item (1)

Counted at 2b of the plan table above (**[#388]**, NOT-STARTED) — §0's "one hygiene item rides
along" and §6 step 2's correction clause are the same obligation, not two.

---

## 3. Superseded items (marked as such, per the operator's instruction)

| Local-doc content | Superseded by | Effect |
|---|---|---|
| **§4 in full** — the polyrepo ruling inputs (facts 1–7 + the architect's partial-fold recommendation) | **ADR-104** (Accepted 2026-07-24, merge `92fabb51`) | §4 was explicitly *inputs, not a decision* ("decision is the operator's, in its own session"). That session happened and ruled. §4 is now **historical input to a settled ADR** — read it for provenance, never as a live recommendation. Its fact 2 (the fabricated 10–20) survives as the still-open **[#388]** |
| **§2 + §3 architecture** — the desired-state contract, mapping table, and L5 sequencing | **[#382]** (open, P1) | Not superseded in the sense of overruled — *routed*. These sections remain the live specification for a build that has not started. Cited correctly by ADR-104's Decommission line: "Execution is the downstream chain #382 → #383 → #385" |

Both supersessions were named in the operator's brief (polyrepo → ADR-104; desired-state →
[#382]) and are confirmed here against live state rather than accepted on assertion.

---

## 4. §1 layer table — drift since 2026-07-21 (context, not work items)

The doc's "Today" column is a 2026-07-21 snapshot. One week on:

| Layer | Doc said | Still true? |
|---|---|---|
| **L0** ~25% | "fragments, 4 registries, no single contract" | **Unchanged** — [#382] unstarted |
| **L1** ~45% | ADR-88/89, doc-code-edge.yaml, freshness live | **Unchanged** |
| **L2** ~40% | "manifest/carriers half-built (editor-config `implemented:false`)" | **Unchanged and verified** — `deploy/manifest-v1.4.0.yaml:327` still reads `implemented: false`; the consumer write-through is still the next ticket |
| **L3** harness ~80% | "archive/safe_remove decided, unbuilt" | **Advanced** — `scripts/safe_remove.py` exists with a demonstrated-catch suite (`b2d3d9c6`). The doc's "unbuilt" is stale |
| **L4** ~5% | one-offs only | **Unchanged** — [#385] doubly blocked |
| **L5** 0% | "designed below" | **Advanced** — L5a built and closed ([#384] @ `ffba8dd8`); L5b still 0% and correctly gated |

---

## 5. What this sweep found that was not already visible

1. **Nothing was lost between the local doc and the repo.** The (i) question — the reason the
   review was ordered — resolves to zero. The consumption was faithful.
2. **§5 lesson 7 ("meta serves object") is the single un-anchored item** — no PLAYBOOK rule, no
   ESSENTIALS line, no BACKLOG row. Every other lesson has at least a vehicle. If anything in this
   doc is going to expire by being forgotten, it is this one.
3. **[#386] appears closure-eligible** — its Done-when names the live-session check, the frozen
   contract, and witnessed-not-merged "each stated as rules", and PLAYBOOK §21 (`db878f4c`) states
   all three. **Not closed here** — closure is the operator's `/review-closures` act (ADR-70).
   Recorded as an observation for that review, not as a verdict.
4. **Step 5's "nightly lane" claim was closed while half-true.** [#384] closed on frames-reviewed
   evidence; the scheduling half was split out to [#391] and remains open. The doc's step-5 text
   still reads "Runs as a nightly lane", which is not yet the case — hence the §6 status marker
   on that row rather than a bare DONE.
5. **Intake #16 is still `status: DRAFT` with an empty `consumed-by:`** despite two consumers
   having produced ADR-104 and the [E9] theme. Whether it advances to CONSUMED or stays DRAFT as a
   living seed (its own closing line says "it evolves") is an operator call — flagged, not taken.

---

## 6. Open questions for the operator

1. **Lesson 7** — file a row, codify it into PLAYBOOK, or record it as deliberately not-a-rule?
   It is currently neither.
2. **Intake #16 lifecycle** — DRAFT (living seed, per its own closing line) or CONSUMED
   (`consumed-by: ADR-104, [E9]`)? The frontmatter and the doc's self-description currently point
   different ways.
3. **[#388]** — the figure-correction ticket has been open since ingestion while the lesson it
   proves ("verify numbers before they propagate") is counted as codified doctrine elsewhere. Is
   it a P-bump, or accepted as low-harm?

---

*Delta review only. It statuses; it does not rule, close, drain, or rewrite. Statuses are pinned
to `main` `6195d932`, 2026-07-28.*
