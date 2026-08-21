# LANE-539 — Ch8 dispatch-system codification (batch 1, lane A)

**Contract:** `LANE-539-ch8-codification.md` (prompts dir) · **Worktree:** `lane-539-ch8-codification`
· **Branch:** `worktree-lane-539-ch8-codification` · **Repo:** `.dev-knowledge` · **Row:** `[#539]`

> **Artifact home — read this first, it is owed to the integrator.** This file sits at the worktree
> root because the contract puts it there and forbids `docs/audits/` for this batch ("the archival
> lane owns that tree this batch; the integrator relocates your artifact per governance"). A
> top-level `ARTIFACT-lane-539.md` is **refused by `validate-hermetization` Rule A** — Tier-1 files
> are a closed class (ADR-101 §1) and this name is in none of it. The refusal is real, was verified
> rather than assumed, and is handled per the "Deviations" section at the end of this file.
> **PROPOSED-PATH for the integrator's relocation:**
> `docs/audits/2026-08-21-technical-ch8-dispatch-codification.md` — Rule-B conformant
> (`<date>-<class>-<slug>`, class token `technical`, lowercase kebab throughout).

---

## Step 1 — UNDERSTAND

### 1.1 The five §Q rulings whose declared home is Ch8

`protocols/STANDING_RULINGS.md` §Q states the binding explicitly, in its own preamble:

> **This register is the application surface; Ch8 is the declared durable home for Q1 and Q3–Q6,
> and `[#539]`'s codification lane carries them there.**

So the five are **Q1, Q3, Q4, Q5, Q6** — enumerated by id, not by inference. Q2 and Q10 are
excluded by the same preamble (their durable home *is* the register; what they are owed is a
one-line Ch8 pointer, dated `2026-09-19` and explicitly declared as owed by neither lane).
Q7/Q8/Q9 are model-admission rulings carried by `[#491]`/`[#562]`/`[#568]`, not by Ch8.

| id | Ruling, as §Q states it | Gap-table id |
|---|---|---|
| **Q1** | *index freshness on lane material* — the integrator is gate-of-record, and a declared single-hook bypass on a lane branch is sanctioned, with the declaration carried in the commit body | G10 |
| **Q3** | *harvest order* — push-before-delete, on every harvest: a merged branch is deleted on `origin` only after the merge is pushed, so no window exists in which integrated work lives solely in a local clone | G9 |
| **Q4** | *cloud lane hygiene* — a cloud lane branches fresh off `origin/main` and leaves foreign dirty files untouched | G14 |
| **Q5** | *receipt gate* — every cloud dispatch carries one: the git source resolves non-empty AND the first assistant text is echoed back. A dispatch without both is not a dispatch that ran | G3 |
| **Q6** | *contract-as-file without exception* — the frozen contract is a committed repo artifact at dispatch time; inline-with-a-dummy-filename is a forbidden dispatch form. This is the unconditional reading of I-D3, and it retires the "repair path, for batch 3" scoping that `protocols/PLAYBOOK.md` :2045–2086 still carries | G13 |

The gap-table column maps each to `docs/audits/2026-08-20-technical-playbook-status.md`, which §Q
itself names as the independent mapping and which "reads each of them as ABSENT from
`protocols/PLAYBOOK.md` today."

### 1.2 The gap, measured rather than inherited

The census claim was **re-measured live on this worktree's tree**, not carried over. A single
`ripgrep` pass over `protocols/PLAYBOOK.md` for the identifying tokens of all five rulings:

```
pattern: push-before-delete|audit-index-freshness|receipt|Receipt|foreign dirty|gate-of-record|CloudV2|origin/main
file:    protocols/PLAYBOOK.md
result:  No matches found
```

**All five read ABSENT — 0 matches, confirming the census at n=1 independently.** Q6 is the one
partial case: its *subject matter* is present (the section "Dispatch prompts and the contract of
record", :2045–2086) but present in exactly the scoped form Q6 retires — "**The repair path, for
batch 3**" — so the ruling itself, the unconditional reading, is absent. That is the shape §Q
describes, verified rather than trusted.

### 1.3 What Ch8 already carries — the reason this is an index, not a restatement

Ch8 (`protocols/PLAYBOOK.md` :1233–2283, 14 subsections) already holds most of the dispatch
system. The contract's Done-item 1 names three things Ch8 "carries"; two of the three are already
there in full, and re-stating them would create the second-copy-free-to-disagree defect Ch8's own
closing subsection was written to prevent:

| Done-item 1 clause | Live status in Ch8 today | This lane's act |
|---|---|---|
| the batch shape (ADR-110: one plan → N file-disjoint lanes → one integrator) | **Present, canonical** — "The batch protocol — ONE plan → N lanes → ONE integrator (ADR-110)", :1792 | **Point at it.** No restatement. |
| lane lifecycle: dispatch → commit-and-STOP → serial integration → teardown | **Present, distributed across five subsections** — dispatch (:2087, :2172), commit-and-STOP (per-lane requirement 4, :1834), serial integration (:1655 "Integrate from the primary"), teardown (:1679 three-command round-trip) | **Index the sequence**; the one genuinely missing step is the harvest leg. |
| …teardown **with Q3 push-before-delete** | **ABSENT.** The three-command round-trip at :1679 is `worktree remove` → `prune` → `branch -d`, and the merge/push ordering that precedes it is stated at :1655 without the *origin*-delete ordering Q3 rules | **Write it.** This is the real gap in the lifecycle. |

The governance pointer the contract names — Ch8 "Handoff prep for the next architect — an index,
not a restatement" (:2240) — is the doctrinal warrant for that column: *"This subsection is the
index and carries no doctrine of its own — every line below is a pointer, deliberately, because a
second copy of a rule is a second thing to keep true."* Applying that rule to this lane's own
output is the whole design.

**What is genuinely new content, therefore, is exactly the five rulings** plus one index that makes
the lane lifecycle readable end-to-end as one sequence, which it currently is not: a seat has to
assemble it from five subsections that never name each other in order.

### 1.4 Constraints discovered before writing (each verified, not assumed)

1. **`silent_rule_ratchet` headroom is 1 token.** `protocols/PLAYBOOK.md` is inside the detector's
   scope root (`protocols/*.md`). Live count **440** against committed baseline **441**
   (`python scripts/silent_rule_detector.py`, detector `silent-rule-v4`, 58 files). The check FAILs
   on an increase and blocks the commit through `audit-health`. **Consequence: the new Ch8 text is
   authored with zero new `must`/`shall`/`never` occurrences** — declarative phrasing, the same
   discipline `STANDING_RULINGS.md`'s own editing note imposes on itself. This is a real
   constraint on wording, and it is why the new text says "a lane deletes on `origin` only after
   the push lands" rather than the imperative form.
2. **`toc-freshness-playbook` is a regen-and-diff gate** on `^protocols/PLAYBOOK\.md$`. Every new
   `###` heading has to land in the `<!-- TOC:START -->` block. Regen:
   `python -m scripts.toc.cli generate protocols/PLAYBOOK.md --write`.
3. **`validate-hermetization` Rule A refuses a new top-level file.** See the banner at the top of
   this artifact; `scripts/validate_hermetization.py:213` is the classifier, and Tier-1 files are a
   closed class per ADR-101 §1:35.
4. **`scripts/` and `tests/` are both sanctioned Tier-1 directories and allowlisted Rule-C homes**
   (`_HOME_PATTERNS`, `scripts/validate_hermetization.py:172,176`), so the generator needs no
   PROPOSED-PATH of its own. Basis quoted in §3 below.

### 1.5 What could break

- **The ratchet.** One stray `never` in 200 lines of new doctrine REDs `audit-health` and blocks
  every commit including the one that would explain it. Mitigated by measuring before and after
  each PLAYBOOK commit rather than at the end.
- **Restatement drift.** Writing the batch shape out again where Ch8 already carries it creates two
  sources for one rule — the exact defect the ADR-110 section and the index subsection both warn
  about. Mitigated by the §1.3 table: pointer, not copy.
- **Q6 vs the live text.** Q6 does not add a rule beside :2045–2086; it *retires that section's
  scoping*. Landing Q6 as a new paragraph while the old "repair path, for batch 3" wording stands
  would leave the corpus stating both readings. Mitigated by amending the live text in place and
  saying so.
- **A generator that encodes rules no document owns.** The audit's own note: "Doctrine first,
  generator second — the reverse order produces a generator that encodes rules no document owns."
  Mitigated by contract step order (Ch8 at step 2, generator at step 3) and honoured literally.
