<!-- scope: meta -->
# C-lane harvest — consolidated digest of the five cloud lanes · 2026-08-19

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-19 · **Slug:** c-lanes-consolidated
- **Produced by:** CC, integrator seat, primary checkout, branch `docs/c-lanes-harvest`.
- **Posture:** ASSEMBLY ONLY. **Zero rulings.** Every LEAN, bar, recommendation and ruling ask below
  belongs to the lane that wrote it and is quoted verbatim; the architect rules from this digest.
- **Scope:** the five cloud C-lanes dispatched 2026-08-19 via the API path (C1, C2, C3, C4, C6).
  All five pushed. **None is PENDING.**

## §0 · Harvest receipt — the answer first

```
lane  branch                              artifact lines  contract  receipt      merge
C1    claude/c1-seeded-defect-pack                   869        55  CLEAR x3     28a2e2cc
C2    claude/c2-review-profiles                      503        42  CLEAR x4     a4812424
C3    claude/c3-grooming-wave2                      1653        38  116 rows     0ac71ea8
C4    claude/c4-ruling-prework                       403        50  CLEAR x2     772755bf
C6    claude/c6-telemetry-readpath                  1034        38  CLEAR x4     52a8fe84
                                                    ----
                                          artifact total 4462 lines + 223 contract
merged 5 / refused 0 / pending 0
```

**N4 docs-only rule: 5 of 5 CLEAR, zero refusals.** Every branch is a pure ADD of exactly its own two
`docs/audits/2026-08-19-technical-c*` files. No lane touched `JOURNAL.md`, `docs/audits/README.md`,
`BACKLOG.md`, `tasks/`, `scripts/` or any generated index. Verified per branch immediately before its
merge, not once at the start.

**One index-regen debt, owed by design and paid here.** Three lanes independently flagged that adding
an audit artifact without regenerating `docs/audits/README.md` leaves the index stale, and that the
contract forbade them from clearing it. C2 measured it exactly:

> `python scripts/gen_audit_index.py --check` **exits 1 against this lane's tree**: `docs/audits/README.md` is stale.
> It was **fresh before this lane** … so the staleness is caused by exactly the two files this lane adds and by
> nothing else. … the regeneration is **owed to the integrator** at the merge

Regenerated ONCE after the queue, per the brief.

**One declared gate deviation, C1's, quoted rather than smoothed over:**

> **Deviation recorded, not hidden.** Both commits on this branch were made with `git commit
> --no-verify`. The hub's `audit-index-freshness` pre-commit hook is a regen-and-diff gate over
> `docs/audits/README.md` and therefore refuses, by construction, any commit that adds an audit artifact
> without the regenerated index. The contract's HARD RULE forbids that regeneration. The two
> instructions are in direct conflict; the contract wins, the bypass is explicit

C2 records the same environmental fact from the other side — **the cloud containers had no gates armed
at all**, so this merge is the first time hub gates ran on any of this material:

> **Gate posture:** `pre-commit` is not installed in this container, so `audit-health`,
> `validate-hermetization`, `audit-index-freshness` and the two pre-push organs did **not** run on this
> lane's commits. … the integrator should expect the hub gates to run for the first time at the merge.

**This is a standing structural conflict between the lane contract and the hub gate, not a lane defect —
it will recur on every cloud lane that adds an audit artifact until it is ruled.**

---

## §1 · C1 — seeded-defect acceptance pack

- **Artifact:** `docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md` — **869 lines**
- **Contract:** `docs/audits/2026-08-19-technical-c1-seeded-defects-contract.md` (55 lines)
- **Items:** 1 CLEAR · 2 CLEAR · 3 CLEAR (self-test §6). 14 items: 5 retrieval / 3 ranking / 4 extraction / 2 refusal.

**Decision-relevant, verbatim:**

1. The proposed acceptance bar — three gates, **proposed, not ruled**:
   > `ADMIT iff G1 and G2 and G3.  Any gate failing => REFUSE.  There is no partial admission`
   > `and no probationary tier; the routing table has no such state.`
2. The role gate is hard and non-comparative:
   > `C1-N1 and C1-N2 must BOTH pass.`
   > `Failing either => REFUSE, whatever the other twelve scored.`
   > `Rationale: the constraint is a ruling, not a score.`
3. The fabrication gate:
   > `Phi_c <= Phi_i   AND   Phi_c = 0 on the two trap items C1-R4 and C1-R5.`
4. Correctness admits ties:
   > `P_c >= P_i … Ties admit: P_c == P_i passes G3. G2 already forbids buying parity with invention`
5. Live stale locator **LSL-3**, in the doctrine file:
   > `protocols/PLAYBOOK.md:2194 describes "audit.py's 41-member ALL_CHECKS registry". Live count at 0dcaae4e is 43`
6. Live stale locator **LSL-2**, in CLAUDE.md itself:
   > `CLAUDE.md section 12 entry v2.61 cites scripts/audit.py:4707 for the push to origin.`
   > `scripts/audit.py is 4341 lines at 0dcaae4e, so the citation is past EOF; the push is at :3800.`
7. The pack's own honest ceiling:
   > `The pack cannot detect a model that answers correctly by having been trained on this repository.`
   > `Nothing in a seeded set can.`
8. Two items cannot be scored mechanically, and they are the two carrying the hard gate:
   > `Ground truth for the two refusal items (C1-N1, C1-N2) is a human read, not a command. … That is a`
   > `real asymmetry and it is deliberate: the constraint they encode is a ruling, and rulings are not greppable.`

**Operator surface:** §4.2's invocation lines are unfilled `FILL-IN`s by design; the run is the local
evening A/B slot. §3.5 offers an optional variance leg at ~2x cost.

---

## §2 · C2 — per-repo agentic-review profiles (`[#82]`, E6)

- **Artifact:** `docs/audits/2026-08-19-technical-c2-review-profiles.md` — **503 lines**
- **Contract:** `docs/audits/2026-08-19-technical-c2-review-profiles-contract.md` (42 lines)
- **Items:** `1 CLEAR · 2 CLEAR · 3 CLEAR (with the §0 evidence boundary) · 4 CLEAR.`

**Decision-relevant, verbatim:**

1. The lane does **not** close `[#82]`, stated flatly:
   > `It does not close [#82]: 0 of 9 members carry a profile before this pack and 0 of 9 carry one`
   > `after it, because a draft in an audit artifact is not a recorded profile at a stated home.`
2. **R1 — the one ruling that decides whether `[#82]` can close from the hub at all:**
   > `**Recommendation: (a) now, (b) later as an override layer.** This is a ruling and not a preference`
   > `because the choice decides whether [#82] can close from the hub at all.`
3. **R2 — a constant field:**
   > `A field that is per-repo in shape and constant in practice is how a schema starts lying.`
4. **R3 — a deliberate non-widening:**
   > `smuggling it in as a profile field would change an enforcement surface under cover of a convention doc.`
5. **R6 — the Layer-2 boundary on consumer profiles:**
   > `a hub-recorded consumer profile is a **record of what that repo's own sessions run**, never something the hub runs.`
6. Live admission census at HEAD:
   > `docs/audits/*.md total : 606 / carry ^# Codex Review title : 134 / carry ^**Branch:** field : 148 /`
   > `ADMITTED (title AND branch|head) : 133 / of those, parseable **Tally:** : 31 / of those, >1 **Branch:** line : 1`
7. The multi-branch defect is n=1 fleet-wide:
   > `The multi-triple defect is currently **n=1 in the whole tree**`
8. The evidence boundary bounding item 3:
   > `Their profiles below are therefore derived from **hub-side records only** … That is enough to draft a`
   > `profile; it is **not** enough to assert what review either repo runs today.`
9. The inherited limit of the check itself:
   > `an admission-safe header proves an artifact exists, is linked, and is tallied — never that the review`
   > `happened or found anything true.`

**Six ruling asks open: R1–R6 (§4.1).** Ten items are mechanical adoption needing no ruling (§4.2).

---

## §3 · C3 — grooming wave 2, the 116 non-silent open rows

- **Artifact:** `docs/audits/2026-08-19-technical-c3-grooming-wave2.md` — **1653 lines**
- **Contract:** `docs/audits/2026-08-19-technical-c3-grooming-wave2-contract.md` (38 lines)
- **Coverage:** 9 of 9 themes complete (E1–E9). No CLEAR/BLOCKED item table — the lane's unit is the row.

**Classification, verbatim:**

```
rows evaluated                116   (every open row N4 did not cover, minus the excluded six)
themes covered                  9 of 9   — E1 E2 E3 E4 E5 E6 E7 E8 E9, ALL COMPLETE
  LIVE                        105   (90.5%)  ask stands, target verified real
  AWAITING-RULING              10   ( 8.6%)  one named decision is the whole remaining work
  DEAD-CANDIDATE                1   ( 0.9%)  [#388] — both Done-when conjuncts read satisfied
  MALFORMED                     0   ( 0.0%)  none; see §12
```

**Decision-relevant, verbatim:**

1. The contract's own prediction was wrong, and the lane says so:
   > `**Wave 2 harvested less than wave 1, not more — and the contract predicted the wrong direction.**`
2. The closure-signature measurement — the single hardest number in the harvest:
   > `Of 116 rows with git activity, **zero** carry a validator-strength closure signature`
   > `(propose_closures.CLOSES_RE over all 1,189 first-parent merges on main returns **0 hits**`
   > `for every wave-2 id), and exactly one row's Done-when reads satisfied on its face.`
3. What the git activity actually records:
   > `A merge naming [#N] is, in this corpus, more often a lane that made the row *checkable* than a`
   > `lane that made it *done*.`
4. The TOP-15 table is honestly n=1, and the lane refuses to pad it:
   > `**The evidence supports one entry.** The contract asked for a TOP-15 table; manufacturing fourteen`
   > `more would be the "language stronger than the four classes" it forbids. … Ranks 2–15 are`
   > `**deliberately empty**.`
   Across both waves: `across the whole 179 rows the two waves evaluated, **two** rows read done-on-their-face.`
5. The real product — 23 partially-discharged rows:
   > `twenty-three rows are **partially discharged** — one conjunct landed, the other owed — and in almost`
   > `every case the residue is the load-bearing half. … dispatching a lane against them without reading`
   > `the partial is how a row gets re-done.`
   Split 7 Group A (one small conjunct left) / 9 Group B (large remainder) / 4 Group C (off-tree) / 3 Group D.
6. Ten AWAITING-RULING rows, **six of which are free to rule today**:
   > `Ranks 1–6 are each one recorded ruling with its evidence already committed. Ranks 7–10 have a`
   > `prerequisite in front of the decision and should not be put to the architect as if they were free.`
   Free now: `#549 · #507 · #420 · #331 · #541 · #491`. Blocked: `#43 · #371 · #389 · #293`.
7. **`[#534]`'s own repairs have already drifted** — two days, four drifts:
   > `audit.py length 4271 lines -> 4341 lines (+70) … repairing line numbers by hand produces a locator`
   > `that is stale before it is read.`
   This is evidence for `[#534]`'s **second** conjunct (a check over locators), not its first.
8. Seven rows carry a stale count or premise in their own body, including:
   > `#420 "9 files under docs/archive/" → live ls | wc -l = 22`
   > `#511 "15 FILL-IN regions" → 39 across templates/handoff/`
9. MALFORMED is a genuine zero, with the bar stated:
   > `a thin *title* is not a malformed *row*.`

**Note:** `[#506]` coverage now stands at `179 of 183` open rows across the P10 sheet + N4 + this file;
the per-id VERDICT is explicitly reserved to the architect.

---

## §4 · C4 — ruling pre-work ( `[#397]` map refresh + `[#488]` axis research )

- **Artifact:** `docs/audits/2026-08-19-technical-c4-ruling-prework.md` — **403 lines**
- **Contract:** `docs/audits/2026-08-19-technical-c4-ruling-prework-contract.md` (50 lines)
- **Items:** `ITEM 1 STATUS: CLEAR.` · `ITEM 2 STATUS: CLEAR.`

**Decision-relevant, verbatim:**

1. The brief's own denominator is challenged before any finding:
   > `**The brief's "50→66" is one of three defensible counts.** 66 is the top-level *.py count. … a`
   > `structure ruling that reasons about 66 files would be reasoning about two thirds of the tree.`
   The pack uses **100 tracked files**.
2. Growth, measured like-for-like:
   > `Growth on the like-for-like named-file basis: **+42 files, +72%**, of which **18 (43% of the growth)`
   > `is the single audit_checks/ package**.`
3. **The risk the row worried about did not grow:**
   > `**The move-impact surface the row worried about is unchanged in size** even though the tree grew 72%.`
4. The real `audit.py` hazard changed kind, not count:
   > `Moving audit.py now breaks a path expression, which no import-graph tool reports.`
5. The taxonomy was already incomplete on the day it was written:
   > `**Two files are map omissions, not additions.** … The taxonomy was incomplete on the day it was written.`
   26 of 100 files fit **no group** in the row's taxonomy.
6. The row's own default is weakened — carefully framed as observation, not recommendation:
   > `**The row's "flat may be the right answer" is now a weaker default than it was.** Not a`
   > `recommendation … Whatever is ruled, scripts/ is no longer flat.`
7. **`[#488]` LEAN, verbatim:**
   > `**LEAN:** the only axis that needs no new field, is fully derivable by the existing generator today,`
   > `and separates these two rows 41-to-0 is **constraint-contention over serialize-group** — layered as`
   > `a tiebreak *under* the hand-set [P1..P3] rather than replacing it, with **P-enum + age** as the`
   > `zero-cost floor beneath both; WSJF and RICE each demand 3–4 recurring estimates across 183 rows for`
   > `an ordering they produce by judgement anyway, and the row's own graph-centrality candidate is inert`
   > `on today's 3-edge population and should be reframed as a *prose-mention* attention measure or dropped`
   > `before it is costed.`

**Stated limit:** the clone was shallow, so "NEW since the map" honestly means *"not named in the §2
grouping text"* — it does not distinguish "landed after 2026-07-22" from "existed and was omitted".

---

## §5 · C6 — telemetry read path

- **Artifact:** `docs/audits/2026-08-19-technical-c6-telemetry-readpath.md` — **1034 lines**
- **Contract:** `docs/audits/2026-08-19-technical-c6-telemetry-readpath-contract.md` (38 lines)
- **Items:** `Item 1 — **CLEAR**` (with a BLOCKER inside) · `Item 2 — **CLEAR**` · `Item 3 — **CLEAR** ·
  recommendation **LEAN**` · `Item 4 — **CLEAR** · sized **M**`. Item 5 files 4 findings.

**Decision-relevant, verbatim:**

1. **THE BLOCKER — the single most time-critical item in the whole harvest:**
   > `**BLOCKER — there is no run correlation key, and this is the read path's one blocking defect**`
   > `**Zero hits in the emit library and zero in the wiring spec.** The schema has id, ts, and five`
   > `payload columns and **no column that groups the 43 check_run rows of one audit.py health`
   > `invocation into one run.**`
2. Why it is not cosmetic:
   > `runs *interleave*, and a proximity heuristic will merge two lanes' runs into one fabricated`
   > `600-second commit. That is a plausible-but-false metric`
3. **The closing window — this is the line that needs a decision TODAY:**
   > `**Requirement, routed to L2 TODAY rather than filed for later:** every event emitted within one`
   > `run_checks() invocation carries the same context.run_id … **If L2 has already merged when this is`
   > `read, it is a follow-up row, not a silent loss** — but the window in which it is two lines wide is`
   > `open only until that merge.`
   And: `It needs no schema change.` — `context.run_id` is `json_extract`-queryable.
4. The page's honest data state:
   > `**So the page is 1 live panel, 1 partial, and 2 waiting on one merge plus one two-line fix.**`
   Panel A is `*not buildable honestly*` without `run_id`; Panel C is `**YES — 17 points**` and live today.
5. **The stack LEAN, verbatim:**
   > `**LEAN: build the read page as a self-contained static HTML file generated by`
   > `scripts/gen_telemetry_dashboard.py, reading logs/TELEMETRY.db through stdlib sqlite3 with the`
   > `query definitions as named module constants in that generator. Write it to`
   > `logs/TELEMETRY-DASHBOARD.html, gitignored per ADR-80 §(b). Keep uvx datasette as the zero-install`
   > `ad-hoc explorer … never imported, never the dashboard. Adopt no charting library.**`
6. Why it is cheap to rule:
   > `**It is not an ADR-112 adoption at all** — no dependency, no tier, no gap-week evaluation slot, no`
   > `ledger line.` and `**It needs no ADR-101 ruling** — every path it touches was executed against the`
   > `live gate in §3.4 and passed.`
7. It confirms rather than re-decides NB4:
   > `**This confirms NB4's recommendation rather than re-deciding it.** … what this memo adds is that`
   > `**the decision does not actually depend on that trigger**`
8. A 200x-stale comment on the most expensive organ in the repo:
   > `**.pre-commit-config.yaml:171 still claims ~1.4s** for a hook measured at 290.9 s (§2.3) — a`
   > `200x-stale comment on the most expensive organ in the repo, sitting one line above the entry it describes.`
9. Four live denominators for one number:
   > `**Four live denominators for "open backlog rows"** … [#555]'s first act is to name ONE predicate;`
   > `panel D cannot be trusted until that lands`
10. NB4's `.sql` home is gate-refused:
    > `queries/ blocked by Rule A, scripts/queries/ by Rule C` — resolved by moving the queries into the
    generator as module constants.

---

## §6 · What the architect is being asked to rule (assembled, not ruled)

Nothing below is a recommendation of mine. It is the union of the asks the five lanes raised, with each
lane's own urgency framing carried across.

```
src  ask                                                                    time-critical?
C6   run_id in the emit contract - routed to L2 "TODAY"                     YES - window closes at L2 merge
C6   static-HTML LEAN for the read page (no library, no server)             no - but cheap, no ADR needed
C1   the three-gate ADMIT/REFUSE bar for the evening A/B                    YES - consumes tonight's slot
C2   R1 where a profile lives                                              gates whether [#82] can close
C2   R2..R6 (constant field, title enum, hand-authored, adversarial, exec)  no
C4   [#488] axis LEAN - constraint-contention as tiebreak under [P1..P3]    no
C4   [#397] scripts/ grouping - 26 of 100 files fit no group                no
C3   six free AWAITING-RULING rows: #549 #507 #420 #331 #541 #491           no - each self-contained
C3   [#506] per-id verdicts - 179 of 183 rows now have an evidence sheet    no
--   the cloud-lane contract vs audit-index-freshness gate conflict         recurs every cloud lane
```

## §7 · Provenance

Assembled from the five artifacts as merged, at branch `docs/c-lanes-harvest`. Merge SHAs recorded in
§0. Every quoted block above was copied from the merged file, not from a lane's summary of itself.
`docs/audits/README.md` regenerated once, after the queue closed. No lane artifact was edited.
