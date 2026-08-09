# Technical decision sheet — everything awaiting an architect ruling

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-09 · **Slug:** decision-sheet
- **Seat:** CC (Opus 5), hub PRIMARY checkout, ARC-3 hygiene close-out, step 5
- **Purpose:** one line per pending decision so the architect rules from this sheet instead of
  re-reading `2026-08-09-technical-consolidation-report.md` (546 lines) and its sources.
- **Posture:** **no recommendations, no rulings.** Each row carries its evidence in one clause and
  its options. Where a row's own source already recommended something, that recommendation is
  reported as the source's, attributed, and not adopted here.

---

## 1. The fifteen OPERATOR-owed items (consolidation report §7)

| # | Decision | Evidence, one clause | Options |
|---|---|---|---|
| 1 | `[#492]` — has Grok 4.6 released? | external fact, unverifiable from inside the repo (N1 R-5) | confirm released · confirm not · park the row behind a dated re-check |
| 2 | The four kill proposals | §4.5, each with a Done-when clause that can no longer be met — **expanded in §2 below** | per-item: kill · re-peg · fold · close-via-escape |
| 3 | The OneDrive rule conflict | three surfaces, two rules: ai-council forbids reads of those paths, corp-ops permits enumerated non-destructive reads, global core-invariants matches corp-ops | unify on the permissive-with-enumeration form · unify on the strict form · declare the divergence intentional and per-repo |
| 4 | ADR-111 ratification | Proposed at `da274889`; its §4 departure is its own item — **§3 below** | ratify as written · ratify with the §4 amendment · reject |
| 5 | `[#511]` — which handoff load is cut | no engineering closes criterion (5); the mechanized cost measured at ~4.5 s of a ~30-minute wall clock | name the load to cut · re-scope the row to the non-mechanized cost · close as measured-and-not-worth-it |
| 6 | Intake #30 / #31 unfiled | **DISCHARGED this arc** — both filed verbatim at `036385a6`, DRAFT, zero births | no decision owed; triage at the batch-4 GO with #28/#29 |
| 7 | N2 R6 — the n=5 unattributed HEAD swaps | UNVERIFIED; the reflog needed to check is gitignored | accept unverifiable and close · un-gitignore the reflog · leave open with a stated evidence gap |
| 8 | N3 item 4 — the `2h43m` / `~9 minutes` figures | unlocated anywhere in the tracked record | re-measure and record · strike the figures as unsourced · accept as untracked seat memory |
| 9 | N5 R1 — rewriting pre-commit hooks | `trailing-whitespace` / `end-of-file-fixer` collide with the append-only and immutability invariants | read-only set only · admit rewriters with path exclusions for the immutable corpora · admit wholesale |
| 10 | N1 R-14 — the pending closure proposals | could not be examined from a cloud clone; the store is gitignored (153 pending at that reading; the SessionStart digest reports 143 today) | track the store · export a tracked digest per session · accept cloud-blindness as a stated limit |
| 11 | The two engine amendments | operator-endorsed but **UNRATIFIED**; attached to `[#511]` as evidence and scope, not treated as ruled | ratify both · ratify one · leave attached-as-evidence |
| 12 | ARCHITECTURE.md not re-read, not re-stamped | stated by ARC-2 rather than papered over; **still true after this arc** — ARC-3 did not re-read it either | commission a re-read arc · re-stamp on a scoped read · leave the stamp honest and stale |
| 13 | `[#322]` — its peg referent | the referent exists and was ruled *against* ("visualization deferred wholesale"), so the row waits on answered research | re-peg to a live trigger · close · convert to a dated review |
| 14 | `[#502]`'s Done-when | **the premise is defective — see §4 item A.** `[#502]` is the mutmut row, not the import-convention row | decide where the Shape-B residual is owned |
| 15 | Intake #28 §B is DRAFT | the whole North Star scoreboard is scored against an unratified finish line | ratify §B · re-score against a ratified baseline · accept the scoreboard as indicative |

---

## 2. The four kill candidates (report §4.5 — reported with evidence, none executed)

Deletion candidates are never acted on without operator approval (standing ruling). Each row's
**source recommendation** is the consolidation report's, reproduced for convenience only.

| # | Row | The clause that can no longer be met | Evidence | Source recommendation |
|---|---|---|---|---|
| K-1 | `[#102]` P2/M machine-readable repo index | *"a pilot index on one repo demonstrably replaces exploratory reads"* | the row's own peg says the precondition will never occur — flat/single-package layouts stay hand-authored **by policy**, so no fleet codemap migration is coming; `#262`/`#295` verified closed at `19b5d598`; the `verify-first` clause was never discharged | KILL |
| K-2 | `[#308]` P3/S the `verify` skill's canonical home | *"decided … at/along the P6 carrier step"* — that step is gone | its own `kill-candidates:` line: the P6 corpus roll it pegged to (`#221`) closed at `8aab4356` **with no successor**; the underlying distribute-vs-hub-local decision is still real | RE-PEG (to the intake #25 W-wave carrier decision), not kill |
| K-3 | `[#325]` P3/S carry `/save` to consumers | same dead P6 referent | same `#221`-with-no-successor peg; `[#294]` is the nearest live carrier row and now holds the W-wave peg | FOLD into `[#294]` |
| K-4 | `[#310]` P3/S cold-bundle annotation surface | *"a sanctioned cold-annotation surface is defined AND the 07-05 bundle is recorded as-cold"* | `#292` — the precondition named in the row's OWN escape clause — is verified closed; the live `preflight_backlog_ids` WARN points at this row every run | KILL via its own escape clause (a close, not a deletion) |

**Coupling the architect should see before ruling K-4:** `[#310]` is the disclaimed neighbour in
`[#520]`'s `kill-candidates:` line (born this arc). `[#310]` owns annotating a bundle
**COLD/incomplete**; `[#520]` owns retiring one whose **seal is structurally wrong**. Closing
`[#310]` does not orphan `[#520]`, but the two read as adjacent and the distinction is the reason
both exist.

---

## 3. ADR-111 §4 — the departure, stated as its own decision

ADR-111 (Proposed) **declines** the ARC-2 contract's literal clause *"an intake may not become rows
without an ADR"*, because that clause contradicts ratified **ADR-98 §3** — an ADR is authored *only*
at a genuine fork, **0..n per intake**, while epics are **1..n per accepted intake**. Live practice
matches ADR-98: intakes #16, #26 and #25 were each accepted by recorded operator ruling in
`decided-by`, not by ADR. ADR-111 therefore ratifies the weaker coherent rule — **birth requires a
ratified intake**, with an ADR required only where the fork test is met.

- **Option A** — ratify ADR-111 as written; the contract's literal clause is superseded and the
  departure stands recorded.
- **Option B** — rule that an ADR really is mandatory per birth; this is an **amendment to ADR-98
  §3** and lands as one, not as an ADR-111 clause.
- **Option C** — reject ADR-111 and leave the pipeline unruled.

---

## 4. Surfaced by ARC-3, not on the §7 list

| # | Decision | Evidence | Options |
|---|---|---|---|
| A | **Who owns the `sys.path` substrate?** | consolidation report §6.2(a) attributes the Shape-B ruling to *"`[#502]` P3/M import convention"*, but `[#502]` is `tasks/502-mutmut-mutation-testing-evaluation-ci-hosted.md`, title *"mutmut 3.7.0 mutation-testing evaluation — CI-hosted"*; the architect's own challenge answer says the import convention is **not** `[#502]`'s Done-when and needs its own row at batch 4. **No open row owns it.** The ruling itself is now landed at `STANDING_RULINGS` H4 | birth the rollout row at batch 4 · fold into `[#502]` and amend that row's Done-when · leave the ruling recorded and unowned |
| B | **Was `[#520]` a permitted birth?** | ARC-3 step 2 caps the arc at ONE birth; step 3(c) separately names "A7(d) row and its direction" as owed. Read as: the cap governs births from this arc's triage, while `[#520]` is a carried debt the 2026-08-08 JOURNAL already scheduled. Both rows landed | keep both · kill `[#520]` and re-birth it at batch 4 · confirm the reading for future arcs |
| C | **Does the deferred set belong in `open-total`?** | now ruled as reporting law (`STANDING_RULINGS` H2 — the denominator is the live count), but the underlying question is live: N1 R-12 asks whether a row may be simultaneously P1 and deferred; **8 rows are P1/P2 *and* deferred, two of them P1** (`[#218]`, `[#300]`) | legal, with the priority meaning "when un-parked" · illegal, forcing a re-priority at defer time · legal but capped |

---

## 5. What this sheet does NOT cover

- **Priority ordering** for the next window — report §8 already ranks it (`[#270]` P1 idle 32 days
  is the standout and unblocks three rows; `[#514]` P1 wedges the merge queue). Sequencing, not a
  fork.
- **Retained branches** — report §9; nothing was deleted and nothing is proposed for deletion.
- **The 229 triaged findings** — report §6.2 dispositions every one; only the residue reaches this
  sheet.
