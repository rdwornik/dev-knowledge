---
intake-id: 54
status: READY
origin: endgame governance session, 2026-08-26; WINDOW-RECORD-AND-DIAGNOSTIC.md Part VIII (I-PERF), operator mandate "performance is priority #1"
consumers: wave-2 rows P-1, P-2, P-4, P-6; the consumer-at-landing gate; the archive-rule enforcement
---

# The loop tax — the working loop costs more than the work

## Problem / motivation

**The fleet's bottleneck is its own verification loop.** Measured this window, on real runs, not
estimated:

| measurement | value | source |
|---|---|---|
| full suite, bare `main` | **1526.5 s** (25 m 26 s), 3949 collected | close packet §8 |
| full suite on the merged batch result | **1870.1 s** (31 m 10 s), 3977 collected | close packet §11 |
| an isolated 5-test attribution probe (`-n 0`) | **870.7 s** (14 m 30 s) for **five tests** | close packet §8 |
| one targeted lane run (2 modules) | 910.0 s (15 m 09 s) | close packet §8 |
| generated files' share of conflicted merges | **7 of 7 — 100%** | diagnostic §5.3 |

**`pytest-xdist` is already the baseline, not an available speedup.** `pyproject.toml` sets
`addopts = "-n auto"` across 16 logical CPUs, so **every number above is already a parallel
number** — the obvious first lever is spent. That is the finding that reframes the problem: what
remains is not "parallelise it" but **stop recomputing, and stop running everything every time**.

**Why this is a governance intake and not just an engineering one.** The batch protocol multiplies
the loop: an integration that takes hours is not slowness, it is the loop tax compounded across
lanes (WINDOW-RECORD Part VI.b). And the corpus keeps growing the surfaces the loop walks —
**728 audit files / 12.3 MB**, of which **290 (40%) have no human or governance consumer**
(diagnostic §1 and §3.1). **Accumulation is a performance problem, so subtraction is a performance
mechanism.**

> **Provenance gap, stated rather than papered over.** The cloud lane's `PERF-RECON-2026-08-25`
> report **did not reach the operator's Downloads** and is therefore **not landed in this repo**;
> `LANE-P-perf-recon.md` is the lane *contract*, not the result. The row names `P-1`, `P-2`, `P-4`
> and `P-6` used below and in the wave-2 rows come from the **endgame brief's own enumeration**
> plus the close-packet and diagnostic measurements cited above — **not** from a PERF-RECON
> artifact this repo holds. If that report is later recovered, this intake and those rows should
> be reconciled against it.

## Scenarios (+1 view)

- **As a lane finishing its work**, I run the checks that cover my diff and finish in a minute,
  instead of a full-suite run that re-verifies 3,900 tests untouched by my change.
- **As the integrator**, I run the full suite **once**, at integration, and it is the only
  full-suite run in the batch.
- **As the operator committing one doc**, the commit gate does not cost minutes of tree-walking
  that the previous commit already did identically.
- **As the corpus**, a landed artifact that acquires no consumer is subtracted by a rule instead of
  accumulating until nobody can read anything.

## Functional requirements

- **Must — P-1: journal-anchor single-pass inversion.** The anchoring predicate currently
  re-derives per candidate; invert it to one pass over the range.
- **Must — P-2: spine parent-map in one git process.** Replace repeated per-commit git invocations
  with a single parent-map query. Subprocess spawns inside loops are the measured shape.
- **Must — P-4: commit/ship tiering per check.** Every check does not deserve every stage. Each
  check declares the tier it runs at (commit / push / integration). **Measure-first: this depends
  on a telemetry window (P-3) that records per-check cost before anything is retiered** — no check
  is demoted on intuition.
- **Must — P-6: a slow-marker selector**, so tiered gating has a mechanical way to select.
- **Must — the subtraction mechanism:** a **consumer-at-landing gate** for `docs/audits/` — a
  landed artifact declares its consumer, so the 40%-unconsumed class cannot re-form silently — and
  **enforcement of the archive rule that already exists** and is simply not being honoured
  (diagnostic §6.3).
- **Should:** the concurrency fix that removes the hottest conflict source — `docs/audits/README.md`
  is touched **41 times per 300 commits**, more than twice `BACKLOG.md`, because every lane that
  writes an artifact must regenerate the index. Regenerating **on read** rather than merge-resolving
  removes the whole class. *(Filed jointly with intake #49.)*
- **Could:** content-hash caching for checks that recompute identical results across runs.

## Acceptance criteria (ex-ante)

1. **P-3 telemetry lands BEFORE any retiering**, and every subsequent tier decision cites a
   measured per-check cost. A check demoted without a number is a defect.
2. A lane's targeted run over its own diff completes in **< 120 s**, versus the 910 s measured this
   window.
3. The full suite runs **exactly once per batch**, at integration — asserted by the close packet's
   own checklist, not by convention.
4. Zero generated-file merge conflicts across the next 20 merges, versus 7 of 7 today.
5. `docs/audits/` unconsumed-artifact count **does not grow** window-over-window, measured the same
   way the diagnostic measured it (identifier-keyed, not filename-keyed — a filename-keyed reaper
   would have proposed deleting 14 live documents and 420 live handoff files).
6. **No check is made faster by making it weaker.** Any speedup that reduces what a gate detects is
   refused; a check that cannot compute ground truth reports `info`, never green-by-skip.

## Non-goals

- Rewriting anything in another language. Profile → parallelise → cache → *only then* consider
  language-level work, and the parallelise rung is already spent.
- Switching off `-n auto` or unloading xdist mid-flight; `pyproject.toml` documents why it cannot
  simply be unloaded, and nothing was switched mid-batch.
- Weakening the gate set to buy time. See criterion 6.

## Impact sketch (4+1 lite)

- **Logical:** checks gain a declared tier; artifacts gain a declared consumer.
- **Process:** targeted-per-merge plus one full suite per batch becomes the enforced cadence rather
  than a convention lanes may forget.
- **Development:** two hot-path inversions (P-1, P-2), a selector (P-6), a tiering mechanism (P-4)
  behind a telemetry window (P-3).
- **Physical:** the loop stops being the dominant cost of the work.

## Open questions

1. What is the per-check cost distribution? **Unknown — that is P-3, and it gates P-4.**
2. Is the audits-index concurrency fix (regenerate-on-read) compatible with the regen-and-diff
   pre-commit gate that currently makes regeneration mandatory, or does one replace the other?
3. Does a consumer-at-landing gate create a perverse incentive to declare a nominal consumer? What
   makes a declared consumer *real*, mechanically?
4. Can the PERF-RECON report be recovered from the cloud session, and does it name P-3 and P-5 as
   this intake infers from the gaps in the P-numbering?

## Status

READY — filed 2026-08-26 by the endgame governance session. Evidence:
`docs/audits/2026-08-26-verification-batch-1-close-packet.md` §8 and §11,
`docs/audits/2026-08-26-technical-hub-diagnostic.md` §1, §3.1, §5, §6.3, §7, and
WINDOW-RECORD-AND-DIAGNOSTIC.md Part VI.b. **PERF-RECON itself is a recorded GAP** — see the
provenance note above.
