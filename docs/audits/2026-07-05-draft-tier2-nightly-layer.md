# 2026-07-05 — DRAFT (plan-only): Tier-2 nightly layer, load-gauge-first

> **PLAN-ONLY. Nothing here is built.** Produced by the 2026-07-05 overnight run (Block E)
> for architect review. Binding inputs: the 2026-07-04 Fable architecture review §5
> (operator saturation = "the one entropy source with NO counter-tactic"), §7 item 9 /
> §8 roadmap 9 (operator-load gauge), the ADR-74/76/80 Tier-2 doctrine, and the standing
> operator rule this draft encodes: **the load-gauge is the FIRST element of any Tier-2
> nightly layer — nothing else lands in that layer before it.**

## Why load-gauge first (the standing rule, made concrete)

Every deterministic gate in the system ultimately discharges into one place: the operator's
ratification funnel (closure proposals, nightly-triage Issues, dispositioned WARNs,
ARCHITECT-REVIEW-PENDING items, grooming digests). The 07-04 review's sharpest systemic
finding: when that funnel saturates, ratification degrades to rubber-stamping, **which
silently re-opens every gate that assumes a genuine human check.** A nightly layer that adds
MORE findings before the funnel is measured makes the one unmeasured leak worse. Hence the
rule: measure the funnel before feeding it.

## Element 1 (FIRST): the operator-load gauge

- **What it counts (all deterministic, read-only, local):**
  1. open `nightly-triage` Issues (`gh issue list --label nightly-triage` or the REST call
     `surface_triage.ps1` already makes);
  2. pending closure proposals (`logs/PROPOSALS-*.md` STRONG+WEAK rows not yet reviewed —
     the `[closures] N proposed` number already surfaced at SessionStart);
  3. disposition-register entries standing (count of `ecosystem/disposition-register.yaml`
     rows — each is a ratified-but-live exception the operator carries);
  4. `ARCHITECT-REVIEW-PENDING` markers in the latest run/audit artifacts (grep over
     `docs/audits/` newest N files);
  5. open BACKLOG items by priority band (P2/P3 counts — trend, not alarm).
- **Where it lives:** one section in the existing `fleet_health.py` digest (the Tier-2 host
  that already runs SessionStart-throttled >24h; ADR-76 — Task Scheduler → Python, no LLM).
  No new organ, no new schedule: the gauge rides the organ the operator already reads.
- **Output shape:** one flat line + a small trend block, e.g.
  `[load] funnel: 3 triage / 45 closures / 10 dispositions / 6 review-pending; 7d delta +4`.
  ASCII-only (the cp1252 lesson), fail-soft, exit 0 always.
- **Persistence for the trend:** append one dated row per day to a gitignored
  `logs/OPERATOR-LOAD.csv` (date, five counts). Gitignored = no commit noise; the trend is
  local like the other Tier-2 state. (Committed promotion is a later, separate decision.)

## Ex-ante funnel-shrink metric (the ADR-81 acceptance contract, frozen before build)

The nightly layer as a whole (gauge + any later elements) is **succeeding** iff, over a
4-week window after the gauge lands:
- **M1 (primary):** the open-funnel total (sum of counts 1–4) trends DOWN or holds while
  merge volume holds — i.e., findings are being retired at least as fast as generated.
- **M2 (guard):** ratification latency does not degrade into batch rubber-stamping —
  proxy: `/review-closures` sessions still reject/skip a nonzero fraction (a 100% accept
  rate across 3+ consecutive reviews is the rubber-stamp signature and FAILS the metric).
- **Kill criterion (pre-registered, ADR-74 Footnote B):** if two consecutive weekly reads
  show the gauge itself unread/unactioned (no funnel item cites it), demote the gauge line
  to the weekly review only — do not let the meter become more noise.

## What is deliberately NOT in this layer (refusals inherited)

- No LLM on the Tier-2 path (ADR-76/80 — deterministic only).
- No new per-session hard gates (ADR-85 scope-freeze; the 07-04 review's NA-6).
- No auto-prioritization/auto-closure of funnel items — the gauge measures, the human
  ratifies (#179 rule).
- No second conformance organ; later nightly elements (e.g. the rot report, deferred by the
  Phase-2 rule) queue BEHIND the gauge and inherit M1/M2.

## Sequencing + effort

One session, S/M: `fleet_health.py` section + counters (reusing existing surfacing code
paths) + CSV appender + ~6 tests. Files: `scripts/fleet_health.py`, `tests/test_fleet_health.py`,
`.gitignore` (one line). Riders: none — the gauge deliberately precedes every other
nightly-layer candidate. BACKLOG: file as its own item with this metric as the ex-ante
contract (do not fold into #123/#130).
