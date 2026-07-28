# [#364] option matrix — the `doc_rot` cap vs the record it degrades (evidence through 2026-07-28)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-28 · **Slug:** 364-cap-option-matrix
- **What this is:** the priced option surface for the still-unruled [#364] cap-vs-record tension, folding the
  fresh evidence from the 2026-07-28 window. **[#364] carries "no ruling attached" by design; this artifact
  attaches prices, not a ruling.**
- **Arc:** PROMPT P6 prep arc, branch `docs/p6-dated-pressure-prep`.

> **PREP, NOT EXECUTION.** No cap is changed, no hook is added, no exemption is declared, no row is edited.
> This arc measured before writing and wrote nothing the cap governs: zero BACKLOG/`tasks/` row edits.

---

## 1. The mechanism, precisely (so options price against the real thing)

`scripts/validate_doc_rot.py` WARNs a BACKLOG task line on **either** leg:
- **Gross leg:** > **1200** chars regardless of dates (`:58` `_BACKLOG_GROSS_CHARS`).
- **Compound leg:** ≥ **3** ISO dates **AND** > **700** chars (`:57` `_BACKLOG_LONG_CHARS`, `:98-105`) —
  inline-history accretion. **This leg trips independently of the 1200 gross cap**: a 750-char row with three
  dates WARNs while a 1150-char row with two dates passes.

Post-flip note: `BACKLOG.md` is generated verbatim from `tasks/` bodies ([#439]), so the cap now effectively
governs **task-file body lines**; the enforcement point (ship-gate, not pre-commit) is unchanged and owned by
the separate row [#406].

## 2. Fresh evidence from this window (the fold this artifact exists for)

1. **The recording-batch 6-WARN incident** (JOURNAL 2026-07-28 (i), correction commit `9ce96be8` over batch
   `93f92ab8`): the four rows the batch annotated were already at **1190 / 1167 / 1090 / 1028** chars —
   **10–172 chars of headroom** — so *no size of honest disposition would have fit*, and the two new rows
   overshot on their own. Six new WARNs = ship-gate RED, forcing a second merge the arc contract didn't allow.
   The entry's own verdict: the cap is deterministic and was knowable up front; not measuring first was the
   avoidable half — the un-fittable disposition was not.
2. **The compound leg is a separate, nearer wall** (JOURNAL 2026-07-28 (j)): [#388] sat at **1102 chars /
   2 ISO dates — 98 free** under the gross cap, yet the ruling's own suggested note text carried a **third
   ISO date**, which would have tripped the ≥3-dates & >700 leg with ~100 gross chars still "free". Headroom
   under one leg is not headroom.
3. **The `9ce96be8` compress-precedent is now used twice** (entries (i) and (j)): compress
   ruling-superseded prose, never disposition self-induced bloat — [#388] folded to **1182/2 dates**, [#443]
   drafted at 1303 → landed **1163/2 dates** (a 1197 first fit was rejected as a 3-char trap). The precedent
   works, but it spends session time per row and it only buys chars that superseded prose happens to hold.
4. **The victim's live state (measured 2026-07-28, this arc):** [#353] = **1189 chars / 2 ISO dates**
   (11 under gross; ONE date under the compound trigger at its length) — the next "n=N+1" incident entry
   cannot land honestly. [#364] itself = 1159/1. The cap-vs-record tension is not hypothetical; it is one
   incident away on its founding row.

## 3. Options, priced with blast radius

| Option | Mechanism | Blast radius | What it buys / fails to buy |
|---|---|---|---|
| **(1) Raise the cap** (e.g. 1200→1600; leave the compound leg) | one constant + test pins in `validate_doc_rot.py` | every row fleet-wide (carrier twin: consumers run the same validator — a hub cap change is a fleet behavior change); erodes the accretion backpressure the cap exists for ([#433] root cause: one file, five workloads) | Buys ~400 chars once; the accumulating-evidence class hits the new wall in a few more incidents; does nothing about the compound leg (evidence entries carry dates by nature — the leg [#388] nearly tripped) |
| **(2) Pre-commit doc_rot leg** | a staged-diff hook ([#406] option (b)) | every commit touching `tasks/` — filing backpressure tightens; [#406] itself records the over-tight risk | Moves *detection* earlier (kills the (i)-class second-merge cost) but changes **capacity not at all** — [#353] still cannot accrue. Solves [#406]'s problem, not [#364]'s |
| **(3) Pre-write measure step as mechanism** | codify the (j) discipline — measure gross + dates before any row write (PLAYBOOK §10 step, or a `coherence-nudge`-style advisory) | zero gate change; a process step per row edit | Prevents self-inflicted WARNs and the (i) incident class; **also no capacity** — prevention, not room. Cheap, composable with any other option |
| **(4) Structured-disposition exemption** — [#364]'s own recorded pair: **(a)** linked evidence file (an `incident-evidence`-class audit artifact — the class already exists in the ADR-101 enum, `validate_hermetization.py AUDIT_CLASS_ENUM`) with the row carrying only a pointer; **(b)** per-ticket declared cap exemption in the validator | (a): zero validator change — a convention + one pointer edit per adopting row. (b): a validator change + a declaration surface; per-ticket so it cannot become a blanket escape | (a) buys **unbounded honest capacity** for the evidence-accumulating class and keeps the cap's accretion job intact for everyone else; cost is one indirection (the row no longer self-contains its evidence). (b) buys in-row capacity but weakens the gate by exactly one declared hole per grant and needs its own review-date hygiene |

Interaction note: options 3 and 4(a) are independent of each other and of [#406]'s enforcement-point ruling —
adopting both changes no gate and leaves [#406] free to be ruled on its own merits later. Option 1 and
option 4(b) both touch the validator and its fleet twin; neither should ride a prep or recording arc.

## 4. Recommendation (one line, as commissioned)

**Adopt 4(a) — the `incident-evidence` linked-file pattern — for evidence-accumulating rows, plus codify (3)
pre-write measurement as the standing step; leave both cap legs unchanged.** (Architect's recommendation;
[#364] remains the operator's ruling — nothing here moves it.)

## 5. What the ruling session re-verifies

`validate_doc_rot.py:57-58` constants unchanged · [#353]/[#364] live char/date counts (§2.4 rots with every
edit) · [#406] still open/unruled (if its enforcement-point ruling landed, option 2 is settled there) ·
whether any row adopted an evidence-file pointer in the interim.
