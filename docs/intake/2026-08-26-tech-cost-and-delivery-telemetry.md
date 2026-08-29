---
intake-id: 50
status: READY
origin: endgame governance session, 2026-08-26; WINDOW-RECORD-AND-DIAGNOSTIC.md Part VIII I2
consumers: the first consumer-repo arc after the performance window (O4 parity); the D1 substrate decision
---

# Cost-and-delivery telemetry — one weekly automated report, and why it is the first consumer arc

## Problem / motivation

**The fleet cannot see what it spends or what it delivers.** On 2026-08-26 a credential
misconfiguration silently billed the operator's work off his subscription and onto a metered API
path. It ran for hours and was **caught by eye, on a banner** — no mechanism noticed. A weekly
report that joins provider billing to local token usage catches that on **run one**.

The same absence blocks a decision already in flight: **D1, the substrate fork**, needs
cost-and-latency evidence to price a Codespaces rung against local execution. The batch-1 close
packet records that this batch produced **no successful devcontainer execution at all**
(`docs/audits/2026-08-26-verification-batch-1-close-packet.md` §7 and §11), so D1 currently has
opinion where it needs numbers.

The research is done and landed: `docs/audits/2026-08-26-technical-research-cost-usage-telemetry.md`
(L5) plus `docs/audits/2026-08-25-technical-research-delivery-telemetry-attribution.md` (R-J).
Between them they establish that **~90% of this is existing components** and the only custom code
is a join-and-render script of roughly 150–250 lines.

## Scenarios (+1 view)

- **As the operator on a Monday**, I open one Markdown report committed to a repo and see, per
  project: tokens and cost by tool, provider invoice totals, Codespaces core-hours, and delivery
  (commits, merges, rows closed) — and I notice a line that should not be there.
- **As the architect pricing D1**, I read measured cost-per-lane on each substrate instead of
  arguing from wall-times taken on a contended workstation.
- **As the fleet, three months from now**, a billing anomaly is caught by a scheduled job rather
  than by the operator happening to look at a banner.

## Functional requirements

- **Must:** a **weekly automated report**, rendered as Markdown and **committed to a repo** (so it
  is diffable, greppable and git-native like everything else); it joins (a) local per-tool
  tokens/cost including subscription usage, (b) provider billing APIs, (c) compute billing for
  Codespaces core-hours and Actions, and (d) git delivery data per project.
- **Must — library-first, per ADR-112 Tier L/S:** `ccusage` for local JSONL usage, each provider's
  admin/cost API, a price catalog to value subscription usage, DuckDB/SQLite as the join store, and
  a scheduled cron as the runner. **Only the join-and-render script is custom**, because no
  existing tool joins subscription-imputed value + API billing + compute + git delivery per project.
- **Must — declare, do not engineer around:** Anthropic-hosted cloud sessions expose **no usage
  export**. The report states that gap rather than silently under-counting.
- **Should:** the `Assisted-by:` / `Model:` commit-trailer convention (R-J) as the attribution
  half, enforced by a `commit-msg` hook — it is the published cross-ecosystem standard, so adopt
  rather than invent.
- **Could:** anomaly thresholds that raise a signal mid-week rather than waiting for the report.

## Acceptance criteria (ex-ante)

1. A scheduled run produces a committed Markdown report with **6–8 numbers** per project, and the
   run is reproducible from a clean checkout.
2. **The leak test:** replaying the 2026-08-26 credential-misconfiguration window through the
   pipeline **surfaces it in the report** — this is the acceptance test, not a nice-to-have.
3. Every number carries its source (which API, which local file, which git range); no number is
   computed two ways in two places.
4. The Anthropic-hosted-cloud gap appears **as a declared gap in the report output**, not as a
   missing row.
5. The report costs less to produce than it reports — measured, not assumed.

## Non-goals

- A dashboard, a service, or a platform. This is a pull-join-render pipeline on a cron.
- Per-request tracing or a cost-attribution model finer than per-project-per-week.
- Choosing providers or models. **Roles and provider admission are R3's**; this measures whatever
  is in use.

## Impact sketch (4+1 lite)

- **Logical:** a new observability seam that is read-only over billing and git.
- **Process:** a weekly artifact the operator actually reads; D1 gains an evidence base.
- **Development:** one custom script; everything else is configuration of existing tools.
- **Physical:** **this is the first CONSUMER arc (O4 parity), not a hub arc** — the beneficiary is
  the operator, and the hub's role is to carry the methodology, not the pipeline.

## Open questions

1. Which repo owns the pipeline and the committed report? The consumer-arc framing says not the
   hub, but the hub owns the methodology that would propagate it.
2. Does valuing subscription usage against a price catalog produce a number the operator trusts,
   or does an imputed figure sitting beside a real invoice mislead?
3. Is GitHub's enhanced-billing endpoint sufficient for Codespaces core-hours at this account tier,
   or does it need the account-level export? (Technical-factual; not guessed.)

## Status

READY — filed 2026-08-26 by the endgame governance session. **Recommended as the FIRST consumer
arc.** Evidence: `docs/audits/2026-08-26-technical-research-cost-usage-telemetry.md` (L5),
`docs/audits/2026-08-25-technical-research-delivery-telemetry-attribution.md` (R-J), and the
billing-leak measurement summarised in
`docs/audits/2026-08-26-technical-provider-surface-repair-summary.md` §1.


---

## AMENDMENT — 2026-08-29: the telemetry scope extension, and what it made visible

> Appended, not edited. Amends an existing READY intake rather than birthing a rival
> (reconcile-before-birth, Z-G1 / ADR-111).

**THE OPERATOR'S EXTENSION, verbatim (2026-08-29):** *"locate the operator's telemetry artifact
(intake #50 + the L5 cost-research) and extend DB-1's inputs: backlog-consumption velocity +
per-model change quality trends."*

**Carried into the running lane, then measured.** The extension reached DB-1 (wave-2 lane N) as a
dispatch-time addendum, so the lane built against it rather than being told afterwards. Its
enumeration of the live history stores is the first honest answer this intake has had:

```
backlog velocity (net banked - births)   IMPROVING  +16 rows/week   4 samples, LIVE
commit-gate wall-time                    ABSENT     logs/TELEMETRY.db is gitignored and does
                                                    not exist -- there is no store at all
suite wall-time                          ABSENT     no store
per-model change quality                 ABSENT     nothing records the authoring model
```

**Two findings this intake should carry forward.**

1. **`logs/TELEMETRY.db` does not exist and is gitignored.** The series most obviously wanted —
   what the commit gate costs per invocation — has **no store**, not merely no report. That is a
   collection gap, and it is this intake's own subject.
2. **Per-model change quality is not derivable today**, and DB-1 renders it **absent, in the
   legend, with the reason** rather than proxying it. The enabling act is filed separately as
   **MODEL ATTRIBUTION** (birth 2 of 2): every model-authored commit carries a model+version
   signature trailer, hook-enforced, and the telemetry store consumes it. Until that lands, the
   series stays absent by construction.

**The fence held.** DB-1's contract said *"telemetry intake #50 stays its own arc — do NOT absorb
it"*, and the lane read this intake to **find the store**, not to implement it. Nothing in DB-1
collects; it renders what already exists and names what does not.

**Provider posture, re-recorded rather than re-litigated:** grok stays **point-use** through the
same measured gate when a point case exists — **no default role**.
