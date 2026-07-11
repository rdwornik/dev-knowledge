# Plan-continuity mechanism — proposal for operator ruling (H4)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-12
- **Source-session:** night-batch Phase 2.75 (H4) · **Model:** claude-opus-4-8
- **Status:** PROPOSAL-ONLY — no HANDOFF_PROCESS/gen_handoff edit tonight (governance canon = operator-gated)

## The operator's idea

Each handoff should carry the PREVIOUS session's plan-of-record so the incoming browser can
compare **plan-vs-implementation across browser generations** — did the session do what it planned?

## (a) What the machinery mandates today — VERIFIED live

- **HANDOFF_PROCESS.md (v5.7):** grep for `plan-of-record | PLAN.md | gap-check | retrospective |
  plan-vs` = **0 hits.** No plan-of-record, no plan-comparison artifact, no gap-check is mandated
  per bundle.
- **gen_handoff.py:** one incidental `"planning scope"` string (a mode label); **no plan artifact
  emitted.**
- **Historical precedent:** the retired v4 numbered bundles carried `07_ACTION_PLAN.md` (e.g.
  `docs/handoffs/2026-05-09-*/07_ACTION_PLAN.md`) — a per-bundle plan artifact existed in v4 and
  was DROPPED at the v5 flip. So the capability regressed; it is not novel.

**Conclusion: no live mechanism mandates a plan-of-record or plan-vs-execution comparison.**

## (b) The manual instance / template

- The exact `…-architect-plan-vs-execution-review.md` the H4 brief cited was **NOT located in the
  hub tree** (searched `docs/handoffs/**`, `docs/audits/2026-07-1*`); it may live in the architect
  session's own (uncommitted) workspace. Flagged honestly, not fabricated.
- The intended template already exists as a ticket: **#301's PLAN.md skeleton** (objective ·
  epics/stories bound to live ids · traceability · decisions · risks) **+ its RETROSPECTIVE**
  (done/not-done/incidents/carry-forward). The v4 `07_ACTION_PLAN.md` is the historical shape.

## (c) Proposal — FOLD into #301 (do not mint a new ticket)

#301 already owns the plan-artifact class and its clause **(iv) "optional cross-chat gap-check
beat for T4+ plans"** is 80% of this idea. The operator's cross-GENERATION comparison is the
hardening of (iv) from "optional beat" to a **named carrier**. Per doctrine (mechanism, not prose),
the carrier is a **three-part seam**:

1. **Bundle field (the carrier):** the architect bundle's `HANDOFF_BOOT.md` frontmatter gains a
   `prior_plan:` pointer (relative path to the PREVIOUS bundle's `PLAN.md`, or `none` for a cold
   start). This is the render-invisible data the incoming browser reads — the same shape as the
   existing probe-manifest field.
2. **Generator step (gen_handoff.py):** `--mode architect` resolves the most-recent prior
   architect bundle's `PLAN.md` and writes its path into `prior_plan:` automatically (a discover-
   from-disk step, mirroring how the runbook pointer is seeded). No hand-copy.
3. **Session-close gate/beat (the comparison):** the RETROSPECTIVE fill (§301-iii) gains a
   mandatory **"plan-vs-execution" subsection** — for each prior-plan objective: delivered /
   partial / dropped + why. Advisory Stop-gate beat first (ADR-85 path), hardenable to a gate that
   REFUSES a wrap while the plan-vs-execution subsection is unfilled (the #292 fill-omission
   pattern applies).

**Touchpoints:** `protocols/HANDOFF_PROCESS.md` §13/§16 (mode-artifact map), `scripts/gen_handoff.py`
(the mode-architect path), `templates/handoff/` (the PLAN.md + RETROSPECTIVE skeletons), ADR-85
(the Stop-gate hardening path), #292 (the fill-omission gate precedent).

**Recommended ruling:** extend #301 with the three-part carrier above (bundle field + generator
step + close-beat) rather than a new ticket; keep it bundle-resident (no new top-level docs class,
#300/ADR-101). This proposal edits no governance canon — it is the ticket text for the operator's
morning ruling.
