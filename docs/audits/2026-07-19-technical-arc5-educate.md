# ARC-5 educate artifact — what landed, why it matters, what happens next

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-19 · **Slug:** arc5-educate
- **Source-session:** ARC-5 integration + silent-rule census (Opus 4.8, 1M), primary checkout, branches `docs/canon-inoculation` → `docs/arc5-plan-of-record` → `docs/arc5-census-filing`, all merged `--no-ff` to `main`
- **Contract basis:** the `il → close` gate floor — *a so-what artifact (change · why · what-next) is produced*. Per `[E8]` closure clause (c), every shipped wave carries an educate artifact with file-level before→after. This discharges that obligation for what has landed **so far**; ARC-5 is **not** closed.
- **Surface note:** placed in `docs/audits/` under class `technical` following the live convention for arc/cycle-close reports (precedent: `2026-07-19-technical-night-consolidated-cycle-close.md`, itself `[E8]`'s cited Source). There is **no `educate` genre or class** — the ADR-101 genre set is `archive · audits · decisions · handoffs · intake · runbooks` and the audit-class enum is closed at 11. No new surface was created.

---

## 1. What landed — file-level before → after

| Change | File | Before | After | Commits |
|---|---|---|---|---|
| Canon inoculation | `protocols/PLAYBOOK.md` | 3746 lines | 3808 lines (+64/−2) | `ee5b1302`, `5833610f`, merge `8c913a6a` |
| Canon inoculation | `protocols/ESSENTIALS.md` | 175 lines | 180 lines (+7/−1) | same |
| Canon inoculation | seed-1 ruling coverage | **0/8 sites** | **8/8 sites** (4 rulings × 2 surfaces) | same |
| Audit-index regen | `docs/audits/*.md` | 260 files | 261 files | `dd7f3615`, merge `9aadaee9` |
| Audit-index regen | `docs/audits/README.md` | stale | regenerated | same |
| `[E8]` plan of record | `BACKLOG.md` | 7 themes / 20 stories / 116 tasks | 8 themes / 22 stories / 125 tasks | `cc1a680e`, `496ac6ac`, merge `e6395a1a` |
| Census filing | `BACKLOG.md` | no metric definition, no baseline | `[E8]` carries the declaration test verbatim, the baseline, and open decision **R12**; new story `[S22]` with `[#357]`–`[#362]` | `45edaf07`, `00f86494`, merge `9a3fb86b` |
| Census filing | `JOURNAL.md` | — | +24 lines, session anchored | `049aad7e` |
| This artifact | `docs/audits/` | 261 files | 262 files | this commit |

---

## 2. Change · why · what-next

**Canon inoculation — change:** four rulings that existed only in chat and JOURNAL narrative were written into `PLAYBOOK` and `ESSENTIALS` (RULING-W · two-tier new-path · worktree side-effect · consumer merge-delegation). **Why:** a ruling nobody can read is a ruling nobody follows; the night audit found "decision recorded ≠ decision enforced ≠ decision legible" as the single recurring failure across all nine streams, and this closes the *legibility* third of it. **What-next:** legibility is not enforcement — `[#356]` tracks that two of the four still have neither a mechanism nor a declaration, and `[#354]` tracks the recurrence half (a co-change checker so a doctrine amendment cannot land without its companion text).

**Audit-index regen — change:** the canon-inoculation Codex doc-review was archived and the generated index rebuilt, 260 → 261. **Why:** the index is regen-and-diff gated; a stale index silently misrepresents what evidence exists. **What-next:** nothing — this is routine hygiene, gated by `audit-index-freshness`.

**`[E8]` plan of record — change:** ARC-5's wave map (W1–W7), frozen closure contract, and nine unruled decisions (R1–R8 + R1b) were filed as a BACKLOG theme rather than an ADR. **Why:** an ADR is immutable and a wave map must evolve as waves land; `BACKLOG.md` is the living spec surface. **What-next:** the operator collects the R1–R8 rulings in one bounded pass, then opens W1 (shelf-life 2026-08-13).

**Census filing — change:** the first measurement of the four-state ledger, plus the operative definition that makes it meaningful, plus six tickets. **Why:** clause (b) of the closure contract turns on a silent/declared boundary that until now existed only in a session transcript — an unwritten definition governing the arc's headline metric. **What-next:** `[#357]` sweeps `docs/decisions/` to complete the denominator; R12 decides whether the arc target is narrowed or re-aimed.

---

## 3. The baseline, stated plainly

**320 MUST-shaped rules were measured. 176 of them — 55% — are silent.**

"Silent" means the rule reads as binding, nothing enforces it, and nothing anywhere says it is unenforced. Not 176 broken rules; 176 rules operating on the reader's good faith alone.

Alongside: **130 enforced** (conservative — ~55 rules where only one leg is gated are counted as enforced; a stricter split would push the silent count *up*) and **14 declared-unenforced** (honest, ticketed, on-surface).

**What it means for the arc.** Closure clause (b) as written requires that "everything still unenforced has moved to declared-unenforced with an owner and a review date." At 176 that is **not reachable in one arc** — it would mean authoring 176 declarations. This is not a reason to weaken the clause; it is the reason **R12** exists, and R12 is deliberately **UNRULED**: either narrow the arc's target to a bounded load-bearing slice, or stop trying to drain the pool and instead gate its growth. That is the operator's call, not the lane's.

**Two findings the four-state model cannot express.** `[#359]` — `HANDOFF_PROCESS.md:502-503` claims a mechanism that does not exist, so it scores as neither silent nor declared; *phantom enforcement* is worse than silence because a reader is actively told a guard exists. `[#362]` — the `#242` handoff cluster's supersession vector is **v4, not v5**, and **49 rules were dropped with no successor**, so retiring it on status alone would silently discard live guards.

---

## 4. NOT DONE — stated as such

**Zero backlog tasks were closed this arc.** Accretion ran **116 → 125 tasks (+9)**, and *all nine are arc-minted* (`#354`–`#362`). Measured against closure clause (d) — "backlog accretion is net ≤ 0 excluding tickets minted by ARC-5's own waves" — the exclusion technically holds, but the honest reading is that this arc has so far only **added** to the queue. Nothing has been discharged.

**Nothing was deleted.** There is still no sanctioned deletion path: the `safe_remove.py` M2/M3 extension is W3 work and **unbuilt** (`#347`, and R3 authorising it is UNRULED). `#300` d.ii remains **on disk awaiting an operator GO**. The night audit's finding — the backlog accretes against a groom scheduled 82 days out — is unchanged by anything in this arc.

**The seed-1 canon-inoculation merge never got a full test-suite run.** It was gated only by the doc-gate subset (**104 tests**), `toc.cli`, and `audit-health`. A doc-only diff is a weak justification for skipping the suite when the diff lands in the two files every session reads. That gap is closed in this session — see the run recorded in the JOURNAL entry for this arc — but it was closed **after** the merge, not before it, which is the wrong order.

**Escalations are filed, not fixed.** `[#358]`–`[#361]` are recorded and routed; none is repaired. That was the explicit instruction for the filing lane, and it is stated here so the artifact is not mistaken for a remediation record.

**ARC-5 is not closed.** Of the six closure conditions, (a) is partially met (the ledger exists as a measurement, not yet as a mechanism), (b) is blocked pending R12, (c) is discharged only for the waves above, and (d), (e), (f) are untouched. No wave has had operator confirmation in his own words that the named pain is gone.
