---
intake-id: 83
status: DRAFT
origin: browser architect seat, deliberate read of the AJ catalogue, 2026-09-07 — `to-cc/DECLARE-F-2-2026-09-07.md` §B row C-F; catalogue row A-05 in `docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md:252` and its empty-search ES-07
consumed-by:
---

# Cost is a weekly aggregate, so "what did this lane cost" has no answer

## Problem / motivation

A-05 treats cost per command as an **architecture signal** — its worked example is $0.76 for an
unmodularised call against $0.56 modularised, the same work at a different structure. The
catalogue's cross-column is precise about our side: *"`logs/TOKEN-LOG.md` is a weekly aggregate;
no per-command cost figure exists."*

That matches the tree at filing time (2026-09-07). `logs/TOKEN-LOG.md` is a weekly append of
`/stats` deltas — dollars, token totals, model share, peak day — with no attribution below the
week. There is no per-lane figure anywhere. `scripts/cost_usage_telemetry.py` exists and is the
right-shaped seam: it emits one span per model call in the OpenTelemetry GenAI shape with a
`devknowledge.*` extension namespace explicitly covering cost and **lane/batch/run correlation**.
Its own docstring records that it is *library only, no call sites*, and that no OTel SDK or
exporter is declared in `pyproject.toml` / `uv.lock` — so nothing is wired, by design and by a
recorded ADR-106 boundary.

The consequence is a claim we make and cannot check. "Tokens saved by offload" is the headline
number the offload arc exists to produce; W1-6's frozen contract states it will print as a
**placeholder = 0 until D15 lands**, which is honest and is also the point — the number is not
computable today, and it will not become computable by printing it. A structural question like
*did splitting this work across lanes cost more or less than doing it in one* is currently
unanswerable, because the unit we spend in (a lane) is not a unit we measure in (a week).

## Scenarios (+1 view)

- As the operator after a night batch, I read a per-lane cost column and see that one lane cost
  four times its siblings. That is an architecture signal about that lane's shape, exactly A-05's
  use of the number.
- As the operator, "tokens saved by offload" stops being a placeholder and becomes a subtraction
  between two measured quantities I can name.
- As a reviewer of the batch protocol, I compare the cost of running seven lanes in parallel
  against the cost of the same work serially, because both were measured at the same grain.
- As the weekly reader, `logs/TOKEN-LOG.md` is unchanged — the aggregate keeps working and keeps
  being append-only, and the per-lane figure sits beside it rather than replacing it.
- As a lane that produced no receipt, I appear in the scorecard as *unmeasured*, not as zero.

## Functional requirements

- **Must:** a per-lane cost figure is derived from the receipts a lane already produces, and lands
  in the scorecard alongside the other numbers rather than in a new report.
- **Must:** the derivation is by correlation id, not by wall-clock windowing. The correlation
  concept already exists (`telemetry_emit.current_run_id()`, reused rather than re-minted by
  `cost_usage_telemetry.py`); parallel lanes overlap in time, so any time-slicing attribution
  would be wrong by construction.
- **Must:** `logs/TOKEN-LOG.md` stays exactly as it is — weekly, append-only, unedited. This
  intake adds a grain; it does not migrate one.
- **Must:** an unmeasured lane renders as unmeasured. A missing receipt must never be rendered as
  a $0 lane, which would make the aggregate quietly wrong.
- **Should:** "tokens saved by offload" becomes computable — defined as a subtraction between two
  measured quantities, with both named, rather than a line printed at 0.
- **Could:** the per-lane figure feeds the batch board (intake C-D), so cost sits next to phase and
  status on the operator's single live surface.

## Acceptance criteria (ex-ante)

- **AC-1:** For a completed batch, every lane with a receipt has a cost figure, and the sum of
  per-lane figures is reconcilable against the same window's aggregate — the reconciliation is
  printed, and a discrepancy beyond a stated tolerance is a failure.
- **AC-2:** A lane with no receipt renders as `unmeasured` in the scorecard, asserted as that
  string by a test, never as `0`.
- **AC-3:** Two lanes running concurrently are attributed by correlation id: a test with
  overlapping spans from two run ids produces two distinct figures, and swapping their wall-clock
  order does not change either.
- **AC-4:** `logs/TOKEN-LOG.md` is byte-unchanged by the build; the append-only surface is proven
  untouched.
- **AC-5:** "Tokens saved by offload" is either computed from two named measured quantities, or it
  is still absent — it is **not** printed as a placeholder once this lands. A placeholder that
  survives the arc that was supposed to fill it is the failure mode this criterion exists to catch.

## Non-goals

- **Not** wiring an OpenTelemetry SDK or exporter. `cost_usage_telemetry.py` records that adding
  one is a separately gated ADR-106 act; this intake does not smuggle it in as a side effect.
- **Not** a cost-based control loop. Nothing refuses, throttles or routes on a dollar figure. The
  number is a signal for the operator and the architect, not an input to an organ.
- **Not** a migration of the weekly log. Two grains, two surfaces.
- **Not** a per-*command* figure in the first step. A-05's unit is the command; the lane is the
  unit we dispatch, budget and compare at, and it is the cheapest honest grain to start from.
- **Not** the SlopCodeBench / long-term-modifiability benchmark that shares A-05's row. That is a
  designed-never-run artifact with its own guard, and it is a different question.

## Impact sketch (4+1 lite)

- **Logical:** cost gains a second grain, and the offload thesis gains a computable metric.
- **Process:** the scorecard gains a column; a lane's receipt becomes load-bearing rather than
  incidental, which means a missing receipt becomes visible.
- **Development:** `scripts/fleet_health.py` (the scorecard's home, and W1-6's file — this is a
  serialization constraint, not just a coupling), `scripts/cost_usage_telemetry.py`, and whatever
  writes the receipts today.
- **Physical:** receipts must be durable long enough to be read after the lane's worktree is gone.
  Whether they are today is an open question below.

## Open questions

- **Do lane receipts actually carry cost?** §B says "per-lane cost from receipts"; this filing
  verified the *seam* (`cost_usage_telemetry.py`'s `devknowledge.*` cost and lane-correlation
  attributes) but not that any receipt in the tree carries a dollar or token figure today. If none
  does, the first step is emitting it, not aggregating it. Technical-architect question.
- Where does the per-lane figure persist? A worktree-local receipt dies with the worktree, and the
  no-leftovers rule guarantees it.
- What is the reconciliation tolerance in AC-1, and against which source — `ccusage`, the
  harness's own accounting, or the spans?
- What are the two named quantities in "tokens saved by offload"? Until they are named, the metric
  is a slogan, and that is the state W1-6's placeholder honestly records.

## Status

DRAFT — filed 2026-09-07. The operator deferred ratification: DECLARE-F-2 §B files this row as
DRAFT, "ratified at the next sitting". No backlog row and no ADR are owed until then.

Filing note (measured, not inherited): §B's *"W1-6 has the placeholder"* is accurate as a
statement about W1-6's **frozen contract**, which declares the placeholder line at
`docs/audits/2026-09-06-technical-batch-u-launch-contracts/LANE-u-000-trace-scorecard-consumer.md:38`.
It is not yet a statement about the tree — no `scorecard` identifier exists in
`scripts/fleet_health.py` on `main` or on `origin/worktree-lane-u-000-trace-scorecard-consumer` at
filing time. W1-6 is serialized behind W1-3 per the batch manifest.
