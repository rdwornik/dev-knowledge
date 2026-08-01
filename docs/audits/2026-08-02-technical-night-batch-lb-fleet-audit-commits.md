# Night batch 2026-08-02 · lane L-B — the 51 fleet-audit commits, triaged

- **Class:** technical (ADR-101 enum) · **Date:** 2026-08-02 · **Slug:** night-batch-lb-fleet-audit-commits
- **Status:** PROPOSAL — read-only. No row was reworded, closed, or filed.
- **Base:** `main` = `a02dd111`; evidence branch `origin/automation/fleet-audit` = `63b772fc`.
- **Method:** read-only. Clone **unshallowed** to 2026-03-30 and the evidence branch fetched
  (refs only), so **nothing here is marked UNVERIFIED** — the cloud shallow-clone caveat was
  lifted before triage, not worked around. Working tree verified clean throughout.

---

## 1. Premise verdict — TRUE, exactly 51

`git log --oneline --since=2026-07-16 --until=2026-08-02 origin/automation/fleet-audit` = **51**.

**Why they were invisible.** The 51 are not on `main` and never were: `automation/fleet-audit` is
an **ADR-84 orphan branch**, by design never merged. [#463]/[#464] describe them as existing
"LOCALLY ONLY — unpushed, unread"; the accurate statement is that they were **pushed but
un-merged and unread**. `main` carries only 3 hand-committed dailies (`0ed63e4f`, `d16f7120`),
which is why a `main`-only search finds almost nothing.

**One structural gap inside the 51:** no standalone 2026-07-24 commit exists on any branch. Five
of six repos got 07-24 backfilled inside the 07-25 commit; **win-tooling never got a 07-24 file
at all**, on any branch, at any time.

## 2. Headline — do the 51 change any row's evidence?

**Yes for one row, decisively; the other two are confirmed rather than changed.**

| Row | Verdict | One-line |
|---|---|---|
| [#463] win-tooling | **CONFIRM** (4/4 items) | every item byte-identical 07-17 → 08-01; the evidence gap closes *in the row's favour* |
| [#464] consumer drift | **CONFIRM** (5/5 items) | every item byte-identical 07-16 → 08-01; only day-counts advance (44d → 60d) |
| [#465] writer integrity | **EXTEND, substantially** | legs (2)+(3) go from "2 known instances, 2 separate opens" to one systemic ~daily pattern with a demonstrated single root cause |

**No candidate row is refuted.** One genuinely new candidate is added (§5).

## 3. [#463] and [#464] — CONFIRM, and what that means

Both rows named an EVIDENCE GAP and both are vindicated by it closing. Representative evidence,
byte-identical between the window's first and last day:

- win-tooling `dot_prefix_discipline | fail | Root config files not dot-prefixed (not on ADR-59
  exception list): ['config.yaml']` — `2026-07-17.md:6` and `2026-08-01.md:6`.
- win-tooling `canonical_freshness | fail | 2 stale (edited since review): VISION.md:
  last_reviewed 2026-07-11 predates last edit 2026-07-12 … ARCHITECTURE.md: …` — identical down
  to the stale dates. **Zero action for at least 15 further days beyond what was known.**
- corp-sca-time-automation `canonical_freshness | fail | 1 stale (edited since review):
  CLAUDE.md: last_reviewed 2026-06-02 predates last edit 2026-06-08` — FAIL line identical; the
  three cadence WARNs identical, only `44d` → `60d` advancing.
- ai-council `reconciled_versions | warn | CONTRIBUTING.md: unknown-spec
  (protocols/HANDOFF_PROCESS.md absent or version unparseable)` — byte-identical both dates.

**The finding is the flatness.** Nine named items, fifteen days of newly-visible daily evidence,
and **not one moved**. That is not new drift — it is proof that the existing drift is inert, and
it is the strongest available evidence for [#460]'s triage-gap thesis: the lane was producing
correct findings daily into a surface nobody read.

**Consequence for the rows:** both carry an EVIDENCE GAP clause that is now **stale as written**
("51 further baseline commits … exist LOCALLY ONLY — unpushed and unread"). The gap is closed.
**Proposal: reword the clause, do not close the rows** — their findings are untouched and all are
consumer-repo work.

## 4. [#465] — EXTEND: the single biggest finding of the 51

The row treats leg (2) *(a same-day digest overwrites an earlier one, "two digests each dropped
14 WARNs")* and leg (3) *(the hub intermittently resolves as not-the-hub, "9 hub-only checks
skipped-as-PASS, 6 of the last 8 runs")* as **two separate remaining bugs**. The 51 commits show
they are **one mechanism**.

**Direct reproduction, verified independently by this orchestrator, not taken on the probe's word:**

| Commit (2026-07-21) | Hub daily WARN lines | Composition |
|---|---|---|
| `a5efca9e` 00:51 | **16** | no_ff_merges 4 · doc_rot 4 · undeclared_edges 6 · canonical_freshness 1 · reconciled_versions 1 |
| `2f6f3c71` 10:51 | **2** | canonical_freshness 1 · reconciled_versions 1 — plus **10 lines reading "not the hub repo"** |

The delta is **exactly 14**, and the 14 are **precisely the three hub-only checks**
(4+4+6). The chain is therefore: **hub self-misresolution → hub-only checks skip → their WARNs
vanish from the day's record**. Leg (3) *causes* leg (2). The 14-WARN figure the row cites is
reproduced exactly.

The high-fidelity run is **unrecoverable from the branch tip** — the day settles at 2 WARNs by
the final commit `231a35b7` (23:51) and the 16-WARN run is visible only via
`git show <sha>:<path>` on the superseded commit.

**Recurrence — 8 of 10 multi-commit days**, high count collapsing to low the same day:

```
07-17  18 -> 1   (-17)     07-23  21 -> 2   (-19)
07-18  17 -> 1   (-16)     07-25  18 -> 2   (-16)
07-19  17 -> 1   (-16)     07-26  21 -> 1   (-20)
07-20  18 -> 2   (-16)     07-27  24 -> 1   (-23)
07-21  16 -> 2   (-14)     07-28  22 -> 20 -> 20  (stable — the exception)
```

**Correlates with the un-retired parallel trigger.** The high/correct count matches the 09:00
scheduled run; the collapse follows same-day from the parallel SessionStart trigger that ADR-76
said would be "removed once the scheduled task is confirmed reliable" — it never was.

**Confirmed hub-specific.** On 07-23, same-day multiplicity shows *stable* WARN counts for
ai-council, win-tooling, corp-ops, corp-monorepo and corp-sca-time-automation. Only the hub's own
file flaps — because only the hub has hub-only checks that can misresolve.

**A second, distinct symptom the row does not name.** On 2026-07-24, 2026-07-30 (all 6 repos) and
2026-08-01 (ai-council), a day's file contains **multiple fully-accumulated `## <date>` tables
concatenated in one blob** — accumulation instead of overwrite. The 08-01 ai-council pair was
checked byte-for-byte: the two tables are **identical in content**, so this manifestation
*duplicates* rather than drops. Same writer, same root instability, opposite failure direction.

**Leg (4) — CONFIRM unchanged.** `handoff_tag_canonicity` reads `n/a` every sampled day 07-17 →
08-01: `§3.1 section not found (consolidated?) — nothing to lint`, byte-identical.

**Proposal:** fold the causal unification into [#465] — legs (2) and (3) are one root cause with
one fix, which materially changes the row's size estimate. Add the duplication symptom as texture.

## 5. New candidate — one

**`silent_rule_ratchet` FAIL on the hub, first seen 2026-08-01.**

```
silent_rule_ratchet | fail | raise-guard INDETERMINATE: the baseline on the integration ref
exists but is unreadable or malformed, so a raise cannot be ruled out (live 439, committed 441)
```

Verified directly in `63b772fc:ecosystem/.dev-knowledge/history/2026-08-01.md`. `pass` on 07-28,
07-29, 07-30, 07-31 ("live N <= baseline N"); **`fail` for the first time on 08-01**, the
window's last day, so persistence is n=1 and cannot be extended further from this evidence.

**No open row names this check** (`grep silent_rule_ratchet BACKLOG.md` → nothing). **Hub work.**
Too fresh to distinguish a real infrastructure problem from a one-off blip, but the FAIL text
("unreadable or malformed") describes a plumbing fault, not a policy breach.

**Notable second-order observation:** that same 2026-08-01 hub daily contains **both**
`silent_rule_ratchet | pass` **and** `silent_rule_ratchet | fail`. The duplication symptom from
§4 is therefore not always benign — here it concatenates two runs with **contradictory verdicts**
for the same check into one committed record. A reader taking the first match gets `pass`; the
truth is `fail`.

**Not filed as separate candidates** (would be kill-candidate duplicates): the win-tooling 07-24
total-skip → texture on [#463]; the duplication symptom → texture on [#465].

## 6. External landings (ADR-41 — queue-only here)

- **[#463]'s four items — EXTERNAL** (win-tooling repo): dot-prefix a config file, re-review two
  docs, add workspace settings, register in `deployed-versions.yaml`.
- **[#464]'s five items — EXTERNAL** across three consumer repos (corp-sca-time-automation,
  corp-ops, corp-monorepo, ai-council).
- **[#465] — NOT external.** `scripts/audit.py` is hub-local; this is hub work.

One reconciliation item, out of this probe's scope: a smaller HEAD-only lineage
(`d16f7120`/`0ed63e4f`) independently recorded some of the same 07-31 dailies on `main` and is
**not** an ancestor of `automation/fleet-audit`. Two lineages record overlapping days.

## 7. Blocking questions for the architect

| # | Question | Decision shape |
|---|---|---|
| B-1 | [#465] legs (2)+(3) are one root cause. Re-scope to a single fix, or keep two legs? | re-scope / keep-split |
| B-2 | Retire the parallel SessionStart audit trigger now that it is named as the collapse source? | retire / keep / investigate-first |
| B-3 | File the `silent_rule_ratchet` FAIL at n=1, or wait for a second daily? | file-now / watch / fold-into-465 |
| B-4 | Two lineages record the same dailies (`main` vs `automation/fleet-audit`). Which is authoritative? | branch-authoritative / main / reconcile |

---

*Read-only night batch. No commits were created, amended, or cherry-picked; the evidence branch
was fetched read-only and never checked out.*
