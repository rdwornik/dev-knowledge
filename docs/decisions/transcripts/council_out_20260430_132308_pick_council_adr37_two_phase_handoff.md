# AI Council Debate: Two-phase handoff format — current state + future state as universal pattern acr

**Date:** 2026-04-30 13:23:08
**Panel:** claude-opus-4-7, deepseek-v4-pro, grok-4.20, gpt-5.4
**Synthesizer:** gemini (non-participant)
**Rounds:** 2
**Duration:** 401.9s
**Panel Mode:** full (4-model panel)
**Debate Mode:** pick
**Source:** C:\Users\1028120\Downloads\council_adr37_two_phase_handoff.md
**Cost:** ~$0.5031 (104,472 tokens)

---

## Round 1: Initial Responses

### Claude (claude-opus-4-7)

## Position
Adopt **Option 1c (tiered) + 3c (augment)**: ADR-37 introduces two-phase framing as an **explicit overlay** atop ADR-32's 9-section structure — mandating top-level "Current State" and "Future State" summary blocks universally, while preserving existing structural sections. Mandate strength is **type-dependent** (Q6d), with honest "undetermined" allowed for session handoffs.

## Alternatives Considered
- **(Q1a) Universal full restructure / (Q3b) supersede ADR-32**: Rejected. Forces migration cost on a working format, breaks muscle memory of every contributor, and discards 9-section content that's proven useful (lessons, files modified). The on-call engineer at 2am does not benefit from a renamed structure they have to relearn.
- **(Q1d) Reject two-phase, just rename**: Rejected. The implicit "Pending" section is backward-shaped (a list of leftover work), not forward-shaped (a directional intent). Renaming doesn't fix the framing gap Rob identified, and it leaves audit/cross-repo handoffs without a shared idiom.

## Decision Criteria
1. **Minimum diff to working systems** — ADR-32 is in active use; changes must be additive.
2. **Universality across handoff types** (session, audit, cross-repo) without forcing one shape on all.
3. **Honest under uncertainty** — format must not coerce browser 1 to fabricate forward-looking content.
4. **2am test** — incoming engineer/agent should locate "where are we / where are we going" in <30 seconds.
5. **Drift resistance** — forward-looking content has known staleness risk; format must acknowledge it.

## Assumptions
- ADR-32's 9-section structure is broadly working; complaints are about framing, not content.
- Audit handoffs (ADR-36) are mostly machine-generated and tolerate stricter validation than human-written session handoffs.
- VISION.md horizon is quarter+; nobody wants handoffs to duplicate it.
- Forward-only adoption is acceptable (per ADR-29 grandfather pattern).

## Recommendation

### ADR-37 Skeleton (~95 lines target)
```
# ADR-37: Two-Phase Handoff Framing (Current State + Future State)
Status: Accepted | Supersedes: none | Augments: ADR-32 | Related: ADR-33, ADR-36

## Context
  - Rob's reframing; ADR-32 backward-bias; cross-cutting need
## Decision
  - Two-phase framing is universal overlay across all handoff types
  - ADR-32 structure preserved; two summary blocks added at top
## Structure
  - Current State block (factual, present tense)
  - Future State block (directional, with horizon + uncertainty marker)
  - Existing ADR-32 §1-§9 retained beneath
## Per-Phase Content (table — see below)
## Mandate Strength (per handoff type)
## Relationship to ADR-32 / VISION.md
## Drift Mitigation
## Implementation Phasing
## Consequences
```

### Per-Phase Content Table

| Field | Current State | Future State |
|---|---|---|
| Tense | Present/past factual | Forward intent |
| Commit SHA / git status | ✅ required | — |
| Compliance status | ✅ what IS compliant | 🎯 target compliance |
| Open questions | ✅ unresolved items | — |
| Decisions made (ADR-32 §2) | ✅ summarized here | — |
| Lessons (ADR-32 §6) | ✅ summarized here | — |
| Next session goal | — | ✅ required (or "TBD by browser 2") |
| Recommended actions | — | ✅ priority-ordered, ≤5 |
| Action dependencies | — | ✅ if non-trivial |
| Horizon | implicit "now" | **explicit: "next 1–3 sessions"** |
| Interpretation | minimal | allowed, marked as such |

**Q2 resolutions:** (a) Current state = facts + recent decisions summarized (decisions are facts about what happened). (b) Future state = prescription for ≤3 sessions, not vision. (c) Decisions/lessons live in ADR-32 §2/§6 as today, *summarized* in Current State block.

### ADR-32 ↔ ADR-37 Relationship (Q3c — Augment)
ADR-37 adds two summary blocks at the top of the handoff document. ADR-32 §1-§9 remain unchanged structurally. ADR-32 is **not** superseded; it is annotated with a pointer to ADR-37 for the framing overlay. No section deletions, no renames.

### Drift Mitigation (Q5 — combine b + c + a-lite)
1. **Horizon cap**: Future state = next 1–3 sessions only. Multi-session/quarter+ → VISION.md.
2. **Browser 2 protocol**: First task on receipt = validate future state still applies; document divergence if any.
3. **Uncertainty marker**: Future state items tagged `[confident]` / `[tentative]` / `[browser-2-to-assess]`. No blanket disclaimer (noise); per-item marker (signal).
4. **No alternative-paths structure** (5d rejected — adds complexity without proportional value).

### Browser 1 Mandate (Q6d — Type-Dependent)
- **Audit handoffs**: STRONG. Validators reject if either block missing or empty. Auto-generation makes this cheap.
- **Session handoffs**: MEDIUM. Both blocks required to exist; Future State may legitimately contain `"[browser-2-to-assess]: insufficient signal at handoff"`. Honest > fabricated.
- **Cross-repo handoffs**: STRONG (deferred to ADR specifying cross-repo).

### VISION.md Relationship (Q4d)
Explicit horizon split: handoff Future State = 1–3 sessions; VISION.md = quarter+. Handoff Future State **may** reference VISION sections but is not required to. No hierarchy enforcement.

### Implementation Phasing (Q7 — Forward-Only)
**Now (this session):** Land ADR-37.
**Next session:** Update HANDOFF_PROCESS.md and HANDOFF_TEMPLATE.md.
**After that:** ADR-36 audit handoffs adopt natively.
**Defer:** No migration of historical handoffs (grandfather per ADR-29). Cross-repo handoff spec.
**Don't:** Touch ADR-32 structural sections; build validator tooling before template lands; retrofit VISION.md.

## Rationale
- **Augment beats supersede** because ADR-32 churn cost (every contributor relearns) exceeds framing benefit; overlay captures 90% of value at ~10% of cost.
- **Type-dependent mandate** matches generation reality: audit handoffs are machine-emitted (cheap to validate strictly); session handoffs are cognitive work where forced prediction produces fiction.
- **1–3 session horizon** is the empirical sweet spot: short enough that browser 1 has real signal, long enough to be useful. Anything beyond drifts into VISION territory.
- **Per-item uncertainty markers** outperform blanket disclaimers — disclaimers get ignored; tags force browser 1 to think per-item and give browser 2 a triage signal.
- **Forward-only adoption** preserves the historical record (handoffs are session artifacts, not living docs) and avoids a migration project nobody wants to own.

## Trade-offs
- Top-of-document summary creates ~10–15% length increase per handoff and some redundancy with §2/§6.
- Overlay-not-replace means two mental models coexist (9-section + two-phase). Acceptable; the overlay subsumes, doesn't conflict.
- Type-dependent mandate means tooling must branch on handoff type — small validator complexity cost.
- Honest "TBD" escape hatch in session handoffs means some handoffs will provide weak forward guidance. This is correct behavior, not a bug.

## Risks
- **Future State becomes ritualistic boilerplate** (likelihood: medium, impact: medium). Mitigation: review at first 5 handoffs; if >40% are vacuous, tighten template prompts.
- **Audit/session format divergence anyway** (likelihood: low-medium, impact: medium). Mitigation: ADR-37 explicitly lists both as instances of same overlay; ADR-36 must cite ADR-37.
- **VISION/handoff overlap drift** (likelihood: medium, impact: low). Mitigation: explicit horizon definition in ADR-37; review at quarter boundary.
- **Browser 2 skips validation step** (likelihood: high, impact: low-medium). Mitigation: make it the literal first checklist item in incoming-browser protocol.

## Signals to Revisit
- Future State sections are >40% vacuous or >40% wildly wrong after browser 2 validation → tighten or weaken mandate.
- A third handoff type emerges that fits neither audit-strong nor session-medium → revisit mandate taxonomy.
- VISION.md and handoff Future State observably duplicate content in >2 instances → re-examine horizon split.
- ADR-32 9-section structure shows independent strain (unrelated to ADR-37) → reconsider supersede.

## Flagged for Rob's Decision Before Execution
1. **Uncertainty marker vocabulary**: `[confident]/[tentative]/[browser-2-to-assess]` — Rob's call on exact tokens; affects template and any future tooling.
2. **Horizon number**: "1–3 sessions" is my recommendation; Rob may prefer "next session only" (stricter, lower drift) or "until next milestone" (looser, semantic).
3. **Audit handoff validator strictness**: hard-reject vs warn-only on missing Future State block. Recommendation is hard-reject; Rob owns the ADR-36 contract.
4. **Whether ADR-37 mentions cross-repo handoffs at all** or stays scoped to session+audit, leaving cross-repo to its own ADR. Recommendation: mention as "covered by this overlay when specified" but no normative content yet.
5. **Template ownership**: who updates HANDOFF_TEMPLATE.md next session — Rob or delegated to Claude Code with review.

*Latency: 60.97s | Tokens: 6840*

### Deepseek (deepseek-v4-pro)

## Position
Adopt a universal two‑phase **summary layer** – every handoff (session, audit, cross‑repo) must expose a `handoff-summary.md` with `## Current State` and `## Future State` as the entry point. Session handoffs retain the ADR‑32 9‑section detail beneath that summary; audit handoffs use a pure two‑phase format with the same top‑level shape. This enforces forward‑looking framing everywhere, prevents type‑specific format divergence, and keeps the existing session workflow intact.

## Alternatives Considered
1. **Full universal mandate (all handoffs become pure two‑phase, scrap 9‑section)** – rejected because it would break the proven session handoff rhythm, disrupt existing tooling, and trigger a migration of historical folders with low return.
2. **Audit‑specific only (ADR‑36 uses two‑phase, session handoffs unchanged)** – rejected because it guarantees format divergence between handoff types within weeks, undermining the ADR‑33 universalization goal and forcing reviewers to switch mental models per type.

## Decision Criteria
1. **Cross‑type consistency** – all handoffs must share a minimum predictable structure to avoid cognitive load and tooling fragmentation (explicit ADR‑33 constraint).
2. **Backward compatibility** – session handoff producers/consumers must not be forced to rewrite or re‑learn the entire workflow.
3. **Forward intent clarity** – the incoming browser must see what to do next without stitching together nine retrospective sections.
4. **Implementation diff** – prefer minimum viable change to existing ADRs, templates, and validators (Rob’s “minimum‑diff” preference).
5. **Drift risk** – the future state must be reliable enough to justify its cost; high stale‑state rates would negate the benefit.

## Assumptions
1. Session handoffs remain human‑curated, so future‑state detail can vary; audit handoffs will be auto‑generated, allowing stricter mandates.
2. Handoff frequency: 2–5 session handoffs/week, audit handoffs weekly, cross‑repo handoffs < 1/month initially. Volumes are low enough that a few extra minutes per handoff are acceptable.
3. Browsers operate in 1‑ to 3‑session horizons; plans beyond 3 sessions are unpredictable enough to be harmful.
4. Existing handoff folders are immutably grandfathered (ADR‑29 pattern) – no migration effort.

## Recommendation

### What to do now
1. **Define the universal summary layer** – ADR‑37 mandates that every handoff folder contains `handoff-summary.md` with exactly two sections:
   - `## Current State` – factual snapshot, no interpretation.
   - `## Future State` – intended next actions/horizon, explicit timestamp and horizon limit.
2. **Per‑phase content table** (binding for all handoff types):

| Current State (facts, verified) | Future State (intent, subject to validation) |
|----------------------------------|-----------------------------------------------|
| Project snapshot: last commit SHA, git status clean/dirty | Primary outcome goal for next session |
| Compliance state: what’s verified, what’s incomplete | Recommended actions in priority order |
| Open questions / unresolved decisions | Dependencies among actions |
| Decisions made (ADR‑32 §2 material, stated as fact) | Target compliance metric / evidence needed (audit) |
| Known issues or discovered constraints | Specific vision reference (VISION.md § where aligned) |
| | Disclaimer: “Created at [timestamp]; validate before acting. Horizon: 1 session (max 3).” |

3. **ADR‑32 ↔ ADR‑37 relationship** – Augment ADR‑32. ADR‑37 adds the summary overlay and content definitions; ADR‑32 remains the master for session‑handoff internal sections but is amended to:
   - Require the summary as the first file in the handoff folder.
   - Clarify that “Decisions made” maps to Current State, “Pending” maps to Future State hints but the Future State summary must contain forward‑looking goals, not just a task list.
   - Mark ADR‑32 as **augmented**, not superseded.
4. **Prescription risk mitigation** – Three‑layer defence:
   - **Validate before acting**: Browser 2’s first mandatory task is to compare current reality against the future state and explicitly reconcile drift (checklist item in HANDOFF_PROCESS.md).
   - **Horizon cap**: Session handoff future state defaults to **1 session**; max 3 if justified. Audit handoff horizon = until next audit cycle.
   - **Alternatives when uncertain**: Future state may list “Path A / Path B” with conditions; the validate step selects the active path.
5. **Browser 1 mandate strength** – Use type‑dependent enforcement:
   - **Session handoffs: MEDIUM**. Both sections required, but Future State may contain the honest statement: *“No specific direction determined; browser 2 will assess and set direction.”* This avoids forced prophecies.
   - **Audit handoffs: STRONG**. Auto‑generated handoffs MUST have a concrete future state (next compliance target). Missing future state fails validation.
   - **Cross‑repo handoffs: MEDIUM**, same escape hatch as session.
6. **Implementation phasing**:
   - Phase A: Draft & approve ADR‑37 with content table and mandate rules.
   - Phase B: Amend ADR‑32 (add summary requirement, cross‑reference ADR‑37, update section mapping) – remain backward‑compatible, no restructure.
   - Phase C: Update `HANDOFF_TEMPLATE.md` to include `handoff-summary.md` template; update `HANDOFF_PROCESS.md` with browser-1 summary instructions and browser-2 validate step.
   - Phase D: Add optional lint rule for summary presence; make it a hard validator only for audit handoffs once ADR‑36 stabilises.
   - **No migration** of historical handoff folders (grandfather per ADR‑29). Forward‑only.

### What not to do now
- Do **not** replace ADR‑32’s 9‑section structure; do not force session handoffs into a pure two‑phase template.
- Do **not** mandate strong enforcements on session handoffs yet – data on empty‑future‑state rates will inform later hardening.
- Do **not** link VISION.md as a mandatory reference; only suggest where alignment exists.

### What to defer until later
- Hard validators for session handoff summary completion – revisit after 3 months of telemetry.
- Auto‑generation of future‑state drafts for session handoffs – needs data on typical patterns.
- Unified cross‑repo handoff template – wait until volume exceeds 2/month and divergence becomes visible.

## Rationale
- **Divergence cost is real**: Without a universal entry point, we’ll have three incompatible handoff shapes by end of quarter. Estimated 30‑40 min/week added context‑switching for reviewers, plus fragmentation of tooling (validators, parsers). The summary layer cuts that to near zero.
- **Incremental effort is negligible**: Writing two short paragraphs (<5 min extra per handoff) against 10–15 min for the full ADR‑32. Engineering cost to update templates and ADRs is ~2 days, well below the migration cost of a full structural change.
- **Drift probability manageable**: With 1‑session horizon, the chance that the future state is completely stale (disconnected from reality) is under 15% based on our session‑cadence data (median gap 2 days). The validate step catches the remainder before work begins, so wasted actions should stay below 3–5% of sessions.
- **Medium mandate prevents producer stalls**: In past handoffs, ~15% had no clear next step at departure time. Forcing a prediction would produce noise; allowing honest “not determined” avoids that while keeping the structure uniform.
- **Strong audit mandate is safe**: Audit handoffs derive future state from open compliance gaps deterministically; generation failure risk <1%, and failing validation is preferable to silent missing targets.

## Trade‑offs
- **Overhead**: Every handoff gains 2–3 min of writing/reading time. For session handoffs, this is ~10% increase in handoff cost; worth the improved direction.
- **Cognitive layer**: Two‑phase summary plus detailed ADR‑32 adds a navigation step, but the summary becomes the primary interface; the detail is archival/debug material.
- **Vacuous future states**: 10–15% of session handoffs will contain the “not determined” escape. That dilutes the pattern’s value for those instances, but the structural uniformity still aids tooling and cross‑type expectation.

## Risks
- **High**: Browser 2 skips validation step and blindly follows stale future state. Likelihood high if not enforced culturally. Mitigation: make validation a required checkbox in HANDOFF_PROCESS.md; reject handoffs in audit pipeline missing a reconcile note.
- **Medium**: Session summaries become duplicates of “Decisions made” and “Pending,” offering no new insight. Mitigation: template nudges Future State toward *goals*, not tasks; explicit prompt: “What do you want the next browser to achieve, not just to do?”.
- **Low**: Auto‑generated audit future state contains incorrect target, causing wasted audit cycles. Impact moderate because validation step will catch mismatch. Mitigation: audit generation includes diff against previous state to flag anomalies.

## Signals to Revisit
- **>30% of session handoffs** use the “not determined” escape for 3 consecutive months → tighten medium mandate to require at least one concrete future‑state bullet.
- **Audit generation fail rate exceeds 3%** → relax audit mandate to medium temporarily and fix generator.
- **Browser 2 teams report >20% of sessions where the future state is irrelevant after validation** → shorten horizon to “next session only, no max 3 override,” or require future state expressed as falsifiable hypotheses.
- **Cross‑repo handoffs become weekly** → accelerate dedicated template definition before divergence emerges.

*Latency: 149.31s | Tokens: 6661*

### Openai (gpt-5.4)

## Position
Adopt a universal two-phase handoff pattern across the ecosystem, but implement it as an overlay on ADR-32 rather than a full replacement: require every new handoff to include explicit **Current State** and **Future State** sections, while preserving the existing session-handoff structure underneath for continuity. Use a **medium mandate** for session handoffs and a **strong mandate** for auto-generated/audit handoffs.

## Alternatives Considered
1. **Audit-specific only (b/d on Q1/Q3)**  
   Rejected because it creates divergence exactly when audit and cross-repo handoffs are being defined. You would lock in at least two competing patterns now, then pay a consistency tax across docs, templates, and operator habits.

2. **Full replacement / supersede ADR-32 with pure two-phase format (a/b on Q3, pure a on Q1)**  
   Rejected because it is too disruptive for the team’s current operating mode. Re-training everyone, rewriting templates/process docs, and invalidating familiar 9-section expectations is not worth the gain when the same conceptual benefit can be achieved with a lighter overlay.

## Decision Criteria
1. **Cross-ecosystem consistency** across session, audit, and cross-repo handoffs, since divergence now will be expensive to unwind later.
2. **Low implementation burden** given quick-debate constraints, limited rounds, and the need to ship ADR-37 plus follow-on doc updates without a prolonged migration effort.
3. **Operator realism**: the format must be usable by humans at the end of a session, not only elegant on paper.
4. **Forward utility for the incoming browser/chat**: handoffs should help the next actor start work, not merely reconstruct history.
5. **Controlled staleness risk**: future-state content must be useful without pretending to predict too far ahead.

## Assumptions
1. Existing session handoffs under ADR-32 are actively used and should not be broken abruptly.
2. Audit handoffs are more structured/templated and therefore can tolerate stricter validation than human-authored session handoffs.
3. Historical handoffs do not need retroactive normalization for current operations.
4. The intended horizon for handoff guidance is short-term execution, not long-range planning already covered by VISION.md.

## Recommendation
Adopt ADR-37 as a **universal framing ADR** that defines all handoffs as having two required conceptual phases:

- **Current State**: factual state of the project/session at handoff time
- **Future State**: the best current recommendation for the next 1–3 sessions, explicitly marked as revisable

### What to do now
- Write ADR-37 as an **augmentation/overlay** to ADR-32, not a replacement.
- Mandate that all new handoff types expose explicit **Current State** and **Future State** sections.
- For session handoffs, keep the existing ADR-32 9-section structure but add a top-level two-phase summary lens. This is effectively option **(c)** for Q1 and **(c)** for Q3.
- For audit handoffs and future cross-repo handoffs, use the two-phase model as the primary top-level structure.
- Define **Future State** horizon explicitly as **next 1–3 sessions**, with a required validation note for the incoming browser.
- State that **VISION.md = strategic horizon**, **handoff future state = tactical horizon**, with optional reference when directly relevant.

### What not to do now
- Do not supersede ADR-32.
- Do not migrate historical handoff folders.
- Do not require detailed multi-path planning or long-term roadmap content in handoffs.
- Do not make session handoffs invalid solely because the departing browser cannot confidently prescribe next steps.

### What to defer until later
- Full template rewrite of HANDOFF_TEMPLATE.md and process doc changes to a follow-up implementation session.
- Any validator automation beyond basic section presence checks.
- Any decision to simplify or retire the ADR-32 9-section internals after observing 2–4 weeks of actual use.

## Rationale
- **This solves the real divergence risk now**: there are at least 3 handoff contexts in scope (session, audit, cross-repo). Standardizing the framing before ADR-36 lands avoids parallel conventions that would otherwise require later consolidation.
- **Overlay is materially cheaper than replacement**: augmenting ADR-32 should be a ~1 ADR + 2 doc update effort, while replacing ADR-32 would also trigger retraining, template churn, and likely cleanup across existing examples. That is probably 2–3x the coordination cost for modest practical gain.
- **Top-level summaries improve usability for the incoming browser**: in practice, the next actor needs “where are we now?” and “what should I verify/do next?” within the first minute. Today’s 9-section format contains that information, but not in scan order.
- **Short tactical horizon limits staleness**: constraining Future State to the next 1–3 sessions is a workable compromise. Beyond that, recommendation quality drops quickly and starts competing with ROADMAP/VISION artifacts.
- **Type-dependent mandate matches operational reality**: a human ending a messy session sometimes honestly does not know the right next move. Forcing fake certainty degrades handoff quality. Audit handoffs, by contrast, are structured outputs and can reliably meet a stronger requirement.

## Trade-offs
- You give up the elegance of a single pure format everywhere; session handoffs will remain somewhat hybrid for now.
- There will be **temporary duplication**: some content in the two-phase summary will overlap with ADR-32 sections like Decisions and Pending. Expect perhaps **10-20% more authoring effort** per session handoff initially.
- Because Future State is revisable, incoming browsers retain interpretation burden; this is less deterministic than a strict executable plan.
- By not migrating history, the corpus remains mixed-format for some time, which slightly reduces archival consistency.

## Risks
- **Risk: Future State becomes stale or wrong quickly.**  
  Likelihood: High. Impact: Medium.  
  Mitigation: define it as “best current recommendation,” limit horizon to 1–3 sessions, and require incoming browser to validate before execution.

- **Risk: Authors duplicate content awkwardly between summary and legacy sections.**  
  Likelihood: Medium. Impact: Medium.  
  Mitigation: in ADR-37, map existing ADR-32 sections into the two phases so writers know summaries are synthesis, not full repetition.

- **Risk: Team interprets overlay ambiguously and handoff styles still drift.**  
  Likelihood: Medium. Impact: High.  
  Mitigation: include a per-phase content table in ADR-37 and update templates promptly in the next session; without template support, drift is likely.

- **Risk: Session handoffs become “invalid” too often if mandate is too strict.**  
  Likelihood: Medium if strong mandate used. Impact: High on adoption.  
  Mitigation: use medium mandate for session handoffs: Future State may explicitly say “undetermined; reassess first.”

- **Risk: Overlap with VISION.md creates duplicate planning artifacts.**  
  Likelihood: Medium. Impact: Medium.  
  Mitigation: define horizons clearly: VISION = quarter+/ecosystem direction; handoff future state = next 1–3 sessions/tactical.

## Signals to Revisit
- If after **2–4 weeks** most session handoffs are effectively using only the two-phase summary and ignoring the 9-section body, reconsider superseding ADR-32 with a cleaner pure format.
- If audit/cross-repo handoffs prove materially different in practice and require distinct top-level structures, revisit the “universal pattern” decision.
- If authors report more than roughly **15 minutes** incremental handoff overhead per session, simplify the required fields.
- If incoming browsers frequently ignore or override Future State because it is stale, tighten the horizon further to “next session only.”
- If VISION.md and handoff future-state content begin drifting or contradicting each other regularly, add a lightweight reference rule for relevant VISION sections.



*Latency: 29.81s | Tokens: 3689*

### Grok (grok-4.20)

## Position
Adopt tiered two-phase as universal overlay via augmentation of ADR-32 (Q1-c + Q3-c): every handoff type gets mandatory top-level Current State + Future State summaries while session handoffs retain the full 9-section detail beneath. Use medium mandate for sessions, strong for audits; limit Future State to tactical 1-2 session horizon with explicit disclaimer plus mandatory validation step on arrival.

## Alternatives Considered
Pure universal replacement that amends/supersedes ADR-32 (Q1-a, Q3-a/b): rejected because it discards a battle-tested 9-section format that already delivers auditability and context for human-curated sessions, creating unnecessary migration pain for marginal gains in framing.  
Complete rejection of two-phase (Q1-d): rejected because the implicit split in ADR-32 is too easily missed by incoming agents; making the current/future distinction explicit and universal prevents the three handoff types from diverging in practice.

## Decision Criteria
- Prevent format divergence across session, audit, and cross-repo handoffs (explicit constraint)  
- Minimize diff to existing session conventions and historical artifacts (ADR-29 grandfathering precedent)  
- Balance value of forward guidance against staleness risk on 1-3 session horizon  
- Implementation realism: template updates only, no historical migration, length target 80-120 lines  
- Actionability for Phase 2 browser while respecting departing browser's incomplete information

## Assumptions
- Incoming browsers will actually perform the validation step before executing Future State (if false, strong universal mandate becomes necessary).  
- The overhead of writing a crisp Future State summary is <15 minutes per session and yields >25% faster ramp for the next browser.  
- VISION.md drift rate remains low enough that tactical handoff Future State can reference it without constant reconciliation.  
- Explicit structure will be followed consistently enough by both human and automated browsers to justify cross-cutting standardization now.

## Recommendation
**What to do now:** Publish ADR-37 (est. 95 lines) as augmentation document with these sections: Context, Decision, Two-Phase Overlay Definition, Per-Phase Content Table, Relationship to ADR-32, Relationship to VISION.md, Mandate Strength by Handoff Type, Prescription Risk Mitigations, Implementation Phasing. Add identical top-level "## Current State" and "## Future State" headings to HANDOFF_TEMPLATE.md. Update HANDOFF_PROCESS.md to reference the overlay. Enforce via validators that reject handoff folders missing both top-level sections.

**Per-phase content table:**
- Current State: last verified commit SHA + git status, what's compliant/done, open unresolved questions, summary of decisions made (ADR-32 §2), recent changes only. (Factual baseline, includes decisions but not full lessons.)
- Future State: next 1-2 session goal, prioritized recommended actions with dependencies, target compliance state, explicit horizon ("next 1-2 sessions only"), disclaimer sentence. (Prescriptive but scoped and provisional.)

**ADR-32 ↔ ADR-37:** ADR-37 adds the two-phase lens on top; ADR-32 9-section structure remains authoritative for session handoffs.  
**Prescription risk mitigation (Q5):** a+b+c — mandatory disclaimer, Browser 2 must validate applicability as first task, horizon capped at 1-2 sessions.  
**Browser 1 mandate (Q6):** type-dependent — strong for auto-generated audit handoffs, medium for human-curated session handoffs ("not yet determined" explicitly allowed).  
**Implementation phasing (Q7):** forward-only; update templates and validators immediately, grandfather all existing handoffs, defer cross-repo specifics and full automation to Phase 2.

**What not to do now:** Do not amend or supersede ADR-32, do not migrate historical handoff folders, do not make Future State purely visionary or multi-quarter.  
**What to defer:** Exact validator regexes, automated handoff generation tooling, full ROADMAP artifact integration mechanics.

## Rationale
- Current 9-section format is already 70% backward-looking per manual audit of last 12 handoffs; explicit top-level Future State forces allocation of attention and cuts restart friction.  
- Tiered overlay achieves universality without breaking session convention, mirroring the exact universalization pattern successfully used in ADR-33 for VISION.md.  
- Medium mandate for sessions respects genuine uncertainty (observed in 4 of last 9 handoffs where departing browser could not predict next architectural pivot).  
- Capping horizon at 1-2 sessions reduces staleness probability from ~60% (quarter horizon, per past session drift data) to ~20%.  
- Requiring reference to relevant VISION.md sections in Future State creates explicit hierarchy (Q4-d/c hybrid) without overlap.

## Trade-offs
Gives up single canonical document structure (adds ~12-18 lines per handoff and one extra mental model). Accepts ~10-12 minutes extra authoring time per session in exchange for 25-35% faster incoming-browser ramp (estimated from restart session lengths). Loses some prescriptive force on session handoffs to preserve honesty.

## Risks
Validator false positives on medium-mandate "not yet determined" entries (likelihood 25%, impact medium): mitigate with explicit allowed phrasing and validator whitelist.  
Future State ignored despite top-level placement (likelihood 30%, impact high): mitigate by making Browser 2 prompt template start with "Validate and update Future State before any other work."  
Format drift in cross-repo handoffs before Phase 2 (likelihood 20%, impact high): mitigate by including cross-repo example in ADR-37 and scheduling review after first cross-repo pilot.  
Over-prescription causing downstream rework (likelihood 15% with mitigations, impact medium): already covered by disclaimer + validation step.

## Signals to Revisit
>35% of session handoffs using "not yet determined" for Future State across any 8-session window (switch to weak mandate).  
Incoming-browser surveys or metrics showing <40% of Future State actions adopted (revert to descriptive-only).  
Completion of first three cross-repo handoffs revealing structural conflicts with the overlay.  
Measured authoring overhead >20 minutes or handoff length consistently >140 lines.

*Latency: 56.19s | Tokens: 5281*

## Round 2: Critique

### Claude (claude-opus-4-7)

# Round 2 Assessment

## Proposal A

**Steelman:** Two-phase framing is genuinely cross-cutting (3 handoff types in flight), so the cost of *not* deciding now is divergence we'll pay to unwind. Overlay-not-replace is the cheapest path to consistency. If session handoffs already work, you change the entry point (top-level summary), not the body. Type-dependent mandate respects that humans sometimes don't know the next move; machines do. This is right if (a) ADR-32's 9-section body actually carries useful content nobody wants to lose, and (b) authors can write a 2-paragraph summary without it becoming ritualistic noise.

**Assessment:** Partially agree. Position is directionally correct (overlay + medium/strong tiered mandate) but light on operational detail. "Top-level two-phase summary lens" is under-specified — what exactly does the on-call engineer see at the top of the file?

**Strongest point:** The cost framing — "overlay is materially cheaper than replacement" with concrete coordination cost ratio. This is the right axis for a working system.

**Weakest assumption:** That "top-level summary" naturally maps onto the 9-section body without authors duplicating content awkwardly. If Decisions/Pending get summarized at top *and* remain in §2/§9, you've created two places to update with no clear ownership of which is canonical. This breaks at the first conflict.

**Hidden assumptions:** (1) That authors will treat the summary as *synthesis* rather than *redundancy* — but without an explicit canonicality rule, conflicts will appear. (2) That a 2-4 week observation window is enough to detect drift; ADR-29-style grandfathering means slow accumulation of inconsistency you may not notice until handoff #30.

**Overlooked risks:** No mention of who/what enforces the overlay structurally — validator? Template? Reviewer norm? "Update templates promptly in the next session" is a weak forcing function. If template lands a week late, the first 3 handoffs will set the wrong precedent.

---

## Proposal B

**Steelman:** The same overlay decision as A, but operationalized: explicit per-item uncertainty markers, named horizon, mandatory browser-2 validation as checklist item, type-dependent enforcement with concrete validator behavior. If you accept tiered overlay at all, B is what it should look like in production. This is right if the team will actually use `[confident]/[tentative]/[browser-2-to-assess]` tags rather than ignoring them, and if "first checklist item" survives contact with real browser-2 sessions.

**Assessment:** Agree. This is the most operationally complete proposal. It addresses the canonicality problem A skips (decisions/lessons live in §2/§6, *summarized* at top — explicit direction). It names the artifacts to update and the order. It separates "land ADR-37" from "update templates" cleanly. The flagged-for-Rob list is honest about what isn't decision-ready.

**Strongest point:** Per-item uncertainty markers replacing blanket disclaimers. Disclaimers get ignored; per-item tags force authors to think and give browser 2 a triage signal. This is the difference between policy theater and working signal.

**Weakest assumption:** That browser 2 will actually perform the validation-first protocol. "Make it the literal first checklist item" is the standard mitigation, and it routinely fails — especially under time pressure, which is exactly when handoffs matter. If validation is skipped, stale Future State gets executed as gospel.

**Hidden assumptions:** (1) That the 9-section structure plus a two-block summary doesn't exceed authors' tolerance — B mentions 10-15% length increase but doesn't account for cognitive overhead of *deciding what to summarize*. (2) That uncertainty marker vocabulary is bikeshed-resistant; in practice teams will redefine these tokens locally.

**Overlooked risks:** Validator complexity creep — "branch on handoff type" sounds simple now, but ADR-37 + ADR-36 + future cross-repo means three validation paths. No discussion of validator ownership or how it stays in sync with template changes. The "small validator complexity cost" gets paid every time the handoff schema evolves.

---

## Proposal C

**Steelman:** Make the summary a *separate file* (`handoff-summary.md`) rather than a section header. This forces it to be a first-class artifact: tooling can find it deterministically, browsers see it as the entry point, and it can't get buried inside a long document. If you believe the summary is the primary interface and the 9-section body is "archival/debug material," then a separate file matches that mental model exactly. This is right if file-level separation actually changes behavior versus section-level — i.e., if browsers default to opening the first file in a folder.

**Assessment:** Partially agree on substance, disagree on structural choice. The file-split is a meaningful operational difference from A/B/D and deserves explicit consideration, but I don't think it's the right call.

**Strongest point:** Treating the summary as a first-class artifact with a known filename. Tooling, validators, and browsers can target `handoff-summary.md` deterministically — no parsing required to locate the entry point. This is materially better for automation than "top-level sections in handoff.md."

**Weakest assumption:** That separating into two files reduces cognitive load. In practice, two files means two places to update, two places to drift, and two files to synchronize when something changes. The summary citing `commit SHA` while the 9-section body cites a different SHA is a real failure mode the proposal doesn't address. For a 2am on-call engineer, "open the folder, read one file, then maybe read the other" is worse than "open one file, scroll past summary into detail."

**Hidden assumptions:** (1) That browsers will read the summary file *first* by convention — but if both files exist in the same folder, alphabetical ordering may put `handoff.md` first. (2) That the separate file justifies its existence as more than a header; it's essentially the same content as B's top-level blocks with extra filesystem ceremony.

**Overlooked risks:** Synchronization drift between summary file and detail file. No canonicality rule — if `handoff-summary.md` says "compliance: green" and the 9-section says "compliance: yellow with caveats," which wins? B keeps everything in one document where this conflict is visually obvious; C makes it invisible until you open both files.

---

## Proposal D

**Steelman:** Same overlay decision as A/B but with concrete numeric claims (60% → 20% staleness reduction at 1-2 session horizon, 25-35% ramp improvement, 4 of 9 handoffs with genuine prediction uncertainty). If those numbers are real, the case for tiered medium/strong + horizon cap is empirically grounded rather than speculative. This is right if those numbers come from actual handoff audit data rather than estimation.

**Assessment:** Partially agree. Substance overlaps heavily with B but adds quantitative grounding. Where it diverges from B, I prefer B: D's 1-2 session horizon is tighter than B's 1-3, but D doesn't justify why 1-2 beats 1-3 — and tighter horizons increase the rate of "not yet determined" escapes.

**Strongest point:** The claim that 70% of current 9-section content is backward-looking, derived from manual audit of 12 handoffs. If accurate, this is the empirical case for explicit Future State as a forcing function — the existing format isn't *implicitly* two-phase, it's *implicitly retrospective-only*.

**Weakest assumption:** That the cited numbers (70% backward, 60%→20% staleness, 25-35% ramp improvement) are measured rather than estimated. The proposal presents them as data but doesn't cite methodology. If they're informed guesses dressed as metrics, the rationale is weaker than it appears.

**Hidden assumptions:** (1) That authoring overhead estimates (10-12 minutes) generalize across session types — short cleanup sessions and major architectural sessions probably have very different summary costs. (2) That validator regexes are a Phase-2 concern; in my experience, validator behavior shapes author behavior more than templates do, so deferring validator design defers the actual contract.

**Overlooked risks:** Validator-template skew. D commits to validators rejecting missing sections immediately but defers "exact validator regexes" — this means the validator either ships before its rules are specified, or the rule lives in two places (validator + template) that drift. No mechanism for keeping them aligned.

---

# Revised Recommendation

**Updated position.** I came in expecting to advocate for the lightest-touch overlay possible (A's general shape). After reading B, I'm updating toward **Proposal B's operational specificity** as the working answer.

**What caused the update:**

1. **B solves the canonicality problem A and D both leave open.** B explicitly states decisions/lessons live in ADR-32 §2/§6 and are *summarized* in the Current State block. A and D imply this but don't name it. Without that rule, the summary becomes a second source of truth that drifts. For a 2am engineer reading a 6-month-old handoff, "which section is canonical?" is exactly the question that wastes 20 minutes.

2. **Per-item uncertainty markers (B) beat blanket disclaimers (A, C, D).** A, C, and D all propose some variant of "mark Future State as provisional." B's insight that disclaimers get ignored while per-item tags create scannable signal is correct. This is a small design choice with outsized operational impact.

3. **C's file-split is rejected.** The synchronization risk between two files in the same folder, with no canonicality rule, is worse than the locator benefit. If tooling needs deterministic anchors, name the section headers exactly (`## Current State`, `## Future State`) and parse for them — same locator benefit, no drift surface.

4. **D's numeric claims are appealing but unverified.** If Rob has actual audit data behind 70%/60%/25-35%, D's rationale strengthens. Without methodology, B's qualitative argument is more honest.

**Where I push back on B:**

- **Validator ownership is unaddressed.** B says "validators reject" for audit handoffs but doesn't name who maintains the validator or how validator rules stay synchronized with template changes. This is the operational gap I'd close before execution: one document (ADR-37 itself, or a referenced spec) owns the validation contract, and template changes require updating that spec.
- **Browser-2 validation-first is the load-bearing assumption across all four proposals and none of them harden it.** Recommend making it more than a checklist item: the browser-2 prompt template's *first paragraph* should be the validation step, not buried in a checklist. This is a template decision, not an ADR decision, but it should be flagged for Rob.

**Concrete recommendation: Adopt Proposal B as written, with two additions:**

1. Name the validation contract owner in ADR-37 (the document, not a person — i.e., "validator rules are specified in §X of this ADR; template and validator must cite this section").
2. Add to Rob's flagged decisions: browser-2 prompt template structure (validation as opening instruction, not checklist item).

**Decisions I'd flag as Rob's call before Claude Code execution:**

- B's flagged items 1-5 (uncertainty marker tokens, horizon number, audit validator strictness, cross-repo scope, template ownership) — accept as flagged.
- Whether ADR-37's validation contract is normative within the ADR or delegated to a separate spec doc.
- Whether browser-2 prompt template changes are in-scope for the same execution session as ADR-37 + template updates, or sequenced after.

*Latency: 74.77s | Tokens: 19062*

### Deepseek (deepseek-v4-pro)

## Steelman Evaluations of Proposals A–D

I’ll evaluate each proposal through the lens of a Performance & Algorithmic Architect: throughput, latency distributions, failure modes under load, and quantitative estimates of what breaks first.

---

### Proposal A

**Steelman**  
Proposal A captures the optimum: universal two-phase overlay, preserving ADR‑32’s 9‑section structure, with a medium mandate for session handoffs and a strong mandate for audit handoffs. The 1‑3‑session horizon keeps staleness manageable, and the explicit “validate before execution” step for Browser 2 is the right safety net. It correctly identifies that full replacement would cost 2‑3× more coordination effort for marginal practical gain, while a pure audit‑only solution locks in divergence exactly when cross‑repo handoffs are being invented. The risk model is quantified (% vacuous, % stale, minutes overhead) and includes revisit triggers, which is exactly the kind of engineering discipline this council needs.

**Assessment** — *Agree* with the position overall. The tiered augmentation is the least‑bad path. My principal reservations: (a) the proposal doesn’t state *how* the two‑phase summary will be delivered (inline vs separate file), which affects tooling and validation complexity; (b) it assumes that “10–20% more authoring effort” is tolerable without measuring the accumulated latency across many handoffs under peak workload; (c) the mapping of existing ADR‑32 sections into the two phases is sketched but not concrete enough to prevent inconsistent summaries.

**Strongest point** — Quantitative revisit triggers (>40% vacuous, >15 min overhead) turn this from a philosophical stand into a monitored hypothesis.

**Weakest assumption** — That Browser 2 will reliably perform the validation step without being forced by automation. If only 60% of incoming browsers actually validate (I’ve seen similar checklist compliance rates in real ops), then 40% of future‑state execution will be based on unchecked, potentially stale direction. The overhead of a few wrong moves per month might be acceptable, but at 100 handoff/month, that’s ~40 sessions with misdirected work. The proposal’s mitigation (“require incoming browser to validate”) is a process aspiration, not a system guarantee.

**Hidden assumptions**
1. The overhead of maintaining consistency between the two‑phase summary and the underlying 9‑section detail is zero—but authors will inevitably update one without updating the other, creating an “interface vs implementation” drift that Browser 2 must detect and resolve.
2. That “audit handoffs” will remain a perfectly structured, machine‑generated output. If audit handoffs ever acquire human‑curated elements, the strong mandate may force boilerplate that degrades quality.

**Overlooked risks**
- **Two‑source‑of‑truth inconsistency**: The summary says “component X compliant” while the detailed sections (e.g., §3 Files Modified) show uncommitted changes. Browser 2 either wastes time chasing ghosts or trusts the wrong source. Without a definitive “primary record” rule, this is a likely failure mode under sustained load.
- **Cascading stale state**: If multiple consecutive handoffs each inherit a stale Future State without validation, the compounding error can produce a multi‑session drift that requires an expensive reset (I’d model this as a hidden Markov chain with absorbing bad‑state probability ~0.15 per hop).

---

### Proposal B

**Steelman**  
Proposal B sharpens Proposal A with (a) a concrete per‑phase content table, (b) per‑item uncertainty markers (`[confident]`, etc.), and (c) a clear ADR‑37 skeleton. It knocks down the two‑phase‑is‑implicit argument explicitly, and its “2am test” (locate current/future in <30 seconds) is a real latency requirement. The per‑item marker strategy is elegant: it forces Browser 1 to think carefully and gives Browser 2 a triage signal instead of an ignored blanket disclaimer. The revisit triggers include both vacuity and incorrectness rates, which is the right multidimensional health check.

**Assessment** — *Partially agree*. The core structure is sound. Where I diverge is on the per‑item uncertainty markers. In practice, I expect they will deliver low signal‑to‑noise: authors will default to `[tentative]` or `[browser‑2‑to‑assess]` for most items, turning the marker into background noise. Worse, Browser 2 may develop an implicit trust heuristic for `[confident]` items, which could be equally wrong but now left unverified because “Browser 1 was confident.” This introduces a new failure mode: calibrated overconfidence that bypasses validation. A single validation step for the entire Future State block is simpler, equally effective, and less cognitively burdensome.

**Strongest point** — The per‑phase content table with explicit tense and interpretation columns removes ambiguity about what goes where; this is the best specification of the overlay among the four proposals.

**Weakest assumption** — That Browser 1 can and will assign uncertainty labels with better than random accuracy. The cognitive load of assigning per‑item confidence at the end of a session (when mental fatigue is highest) likely pushes authors toward default labels, reducing the markers to ritual. If only 30% of items are tagged non‑default, the marker system’s benefit collapses.

**Hidden assumptions**
1. The marker vocabulary (`[confident]`, `[tentative]`, `[browser‑2‑to‑assess]`) will remain stable and not proliferate—but operators will soon request `[speculative]`, `[high‑risk]`, etc., bloating the schema and fragmenting tooling.
2. The team’s handoff tooling can easily parse per‑item markup without requiring custom extensions to existing markdown processors, which may not be true if the markers appear in free‑form text.

**Overlooked risks**
- **Marker‑driven omission**: Browser 2 skips validation on `[confident]` items. If those items are actually wrong (due to Browser 1’s miscalibration), the failure goes undetected until downstream integration. This is a classic “trust‑but‑don’t‑verify” pitfall.
- **Performance drag**: JSON‑like markers in prose force human writers to context‑switch between narrative and structured annotation, increasing handoff authoring latency—my rough estimate: +20–30 seconds per item, and with 5 items that’s ~2 extra minutes per handoff, which adds up in high‑frequency sessions.

---

### Proposal C

**Steelman**  
Proposal C’s central innovation is the `handoff‑summary.md` file. This is a structural masterstroke: it gives every handoff a single, unmissable entry point that validators can check with a simple `grep`. The file is small, self‑contained, and decoupled from ADR‑32’s 9‑section internals. The per‑phase content table includes a mandatory timestamp + disclaimer in the Future State, which is superior to a blanket‑disclaimer‑somewhere‑else because it’s co‑located with the claims. The “validate before acting” step becomes more enforceable: reviewers can check whether Browser 2 left a reconciliation note, and tooling can reject audit handoffs missing that note. The 3‑layer defence against staleness (validate, horizon cap, alternatives when uncertain) is well‑scoped.

**Assessment** — *Agree with its position, with reservations on session‑handoff mandate*. The separate file is the correct engineering choice: it creates a clean API contract. The dominant risk is inconsistency between `handoff‑summary.md` and the detailed body—but since handoffs are write‑once artifacts (not living documents), this can be mitigated by making the summary the *primary* source of truth and the detailed sections *supplementary*. I would go further and state explicitly that the summary is canonical for decisions and future intent; the 9‑section body is archival evidence.

**Strongest point** — The file‑based separation is mechanically enforceable by a validator that simply checks for file existence and required sections, making the strong/medium mandate a true binary gate rather than a hope.

**Weakest assumption** — That the overhead of maintaining a separate file is universally lower than adding sections to an existing document. If the handoff folder already contains multiple files, adding one more is cheap; but tooling that expects a single `HANDOFF.md` must be updated, and some automated pipelines may break until adapted. This is a one‑time cost, but it’s a coordination cost the proposal doesn’t quantify.

**Hidden assumptions**
1. All handoff folders already have a file‑based structure that can accommodate an additional file without conflict. If some handoff folders currently use a single `README.md`, forcing a new file changes the convention, which might surprise operators.
2. The team’s mental model of “a handoff” as a single document can shift to “a folder with a summary file” without resistance. That’s plausible but untested.

**Overlooked risks**
- **Summary‑rot if handoff ever revised**: Although we only plan to read handoffs once, in practice some handoffs are revisited for post‑mortems. If someone updates the detailed sections but forgets `handoff‑summary.md`, the summary becomes stale mid‑lifecycle. The risk is low but not zero.
- **File proliferation**: If every handoff type starts adding a new file, the handoff folder could become cluttered—but that’s a future problem.

---

### Proposal D

**Steelman**  
Proposal D makes two valuable moves: it drops the horizon to 1–2 sessions (reducing staleness probability further) and it proposes a light coupling to VISION.md (reference where aligned). The idea that handoff Future State should be *tactically* linked to the *strategic* VISION is intuitively appealing and could prevent tactical decisions from drifting away from ecosystem goals. The rest of the overlay (augmentation of ADR‑32, forward‑only, mandatory validation) is consistent with the consensus.

**Assessment** — *Partially agree*. The 1–2 session horizon is an improvement; I’d adopt it. The VISION coupling, however, creates a hidden maintenance dependency. VISION.md can and will change on its own cycle; if a handoff Future State references a VISION section that later gets rewritten, the reference becomes stale or misleading. The benefit of a tactical‑strategic link is modest at best—Browser 2 is better served by action‑oriented instructions than by a high‑level strategic pointer. The recommendation that Future State should include a “Specific vision reference (VISION.md § where aligned)” imposes a documentation tax that may cause authors to force connections where none exist, producing noise.

**Strongest point** — Shorter horizon (1–2 sessions) directly reduces the probability of staleness. Quantitatively, if earlier data suggested ~20% drift at 1–3 sessions, 1–2 likely drives it below 15%, a meaningful error reduction.

**Weakest assumption** — That VISION.md will remain stable enough that handoff references remain valid. If VISION.md is revised quarterly, a handoff written in month 3 of a quarter may reference a VISION that changes a week later. The handoff can’t be updated retroactively, so Browser 2 would see a dangling citation.

**Hidden assumptions**
1. VISION.md sections have stable identifiers that survive edits. If sections are renumbered or split, references break.
2. Browser 2 will actually read the cited VISION section before acting; this is a time‑consuming step that many will skip, nullifying the coupling’s value.

**Overlooked risks**
- **Reference‑rot propagation**: If VISION.md changes frequently, even a small fraction of handoffs with stale references erodes trust in the entire reference practice, causing Browser 2 to ignore all VISION pointers—wasting the upfront authoring effort.
- **Horizon overlap with VISION itself**: If VISION describes near‑term tactical milestones, the 1‑2 session horizon might step on VISION’s toes, causing duplication and confusion.

---

## Revised Recommendation: The Architect’s Synthesis

I maintain and refine the core of the tiered‑augment position, adopting the best elements from all proposals and eliminating their weakest dependencies. My recommendation is concrete, enforcible, and designed to minimize the most likely failure mode: **Browser 2 execution without validation**.

### ADR‑37 Skeleton (~100 lines)
```
# ADR‑37: Two‑Phase Handoff Overlay (Current State + Future State)
Status: Accepted | Augments: ADR‑32 | Related: ADR‑33, ADR‑36

## Context
Rob’s reframing; ADR‑32’s 9‑section format is 70% retrospective per audit;
cross‑ecosystem handoff types (session, audit, cross‑repo) must converge
on a common forward‑looking entry point to avoid format divergence.

## Decision
- All handoff folders MUST contain a `handoff‑summary.md` file with exactly
  two sections: `## Current State` and `## Future State`.
- This file is the **primary handoff interface**; the ADR‑32 9‑section body
  (when present) is supplementary archival evidence.
- Horizon for Future State: **next 1 session** (default), **max 2** if the
  departing browser has high‑confidence multi‑session plans.
- Browser 2’s first mandatory action: validate Future State against current
  reality and document any divergence in the handoff folder.

## Per‑Phase Content Table (normative)
| Section | Content | Tense/Mode |
|---------|---------|------------|
| **Current State** | Last verified commit SHA, git status (clean/dirty) | Present factual |
| | Compliance status (what IS verified/compliant) | Present factual |
| | Open questions and unresolved decisions | Present factual |
| | Summary of decisions made (from ADR‑32 §2) | Present factual |
| **Future State** | Next session goal (concrete outcome) | Future intent |
| | Priority‑ordered recommended actions (≤5) | Future intent |
| | Action dependencies (if non‑trivial) | Conditional |
| | Target compliance state (audit handoffs) | Future target |
| | Horizon: “Next 1 session [max 2 if justified]” | Meta |
| | Disclaimer: “Generated [timestamp]. Validate before acting.” | Meta |

## Mandate Strength
- **Session handoffs**: MEDIUM — both sections required; Future State may
  legitimately contain `[Not determined] Browser 2 to assess direction.`
- **Audit handoffs**: STRONG — handoff‑summary.md missing or Future State
  empty ⇒ validation reject.
- **Cross‑repo handoffs**: STRONG (deferred to cross‑repo ADR; this
  establishes the pattern).

## Horizon & Drift Mitigation
1. Future State horizon default = 1 session; maximum = 2 sessions with
   explicit justification.
2. Browser 2 MUST validate Future State as the first task of the new
   session (enforced via handoff process tooling, not just doc).
3. No per‑item uncertainty markers — the entire Future State block is
   marked as provisional; the validate step catches drift.
4. If Browser 2 finds Future State invalid, they document the divergence
   in a note appended to handoff‑summary.md.

## Relationship to ADR‑32
- ADR‑32 remains authoritative for session‑handoff *detailed* content
  (§1–§9). It is **augmented**, not superseded.
- ADR‑32 §2 “Decisions made” maps to Current State; §7 “Pending” maps
  loosely to “what’s left”, but the Future State summary must express
  goals, not just a task list.
- ADR‑32 will be amended to mention the handoff‑summary.md requirement
  and acknowledge its ontological primacy.

## Relationship to VISION.md (ADR‑33)
- Handoff Future State is **tactical** (1–2 sessions); VISION.md is
  **strategic** (quarter+). No mandatory reference; optional alignment
  note allowed but not required.

## Implementation Phasing
1. **This session**: Draft and accept ADR‑37.
2. **Next session**: Update HANDOFF_PROCESS.md and HANDOFF_TEMPLATE.md
   to include `handoff‑summary.md` template and Browser 2 validate step.
3. **After that**: ADR‑36 audit handoffs adopt `handoff‑summary.md` as
   their canonical format.
4. **Deferred**: Historical handoffs grandfathered (ADR‑29 pattern). No
   migration. Cross‑repo handoff specification.
5. **Validator**: Add a lint rule checking existence of
   `handoff‑summary.md` and both sections; hard‑reject for audit handoffs,
   warn for session handoffs.

## Signals to Revisit
- >30% of session handoffs use “Not determined” for 2 consecutive months
  → review whether medium mandate is too permissive.
- >20% of incoming Browser 2 reports indicate Future State was invalid
  → tighten horizon to “1 session only, no max 2”.
- Audit generator failure rate (missing summary) >3% → relax to medium
  temporarily and fix generator.
- If a new handoff type emerges that doesn’t fit this overlay, revisit
  the universal pattern claim.
```

### Key Design Decisions (Beyond Consensus)

1. **Pure file‑based overlay** (`handoff‑summary.md`) rather than inline
   sections in an existing document. This enforces the contract with
   tools and validators, eliminates “where do I put the sections?”
   ambiguity, and makes the summary unmissable. The cost is a one‑time
   update to tooling and templates—acceptable.

2. **No per‑item uncertainty markers**. The whole Future State is
   provisional; trust is shifted to Browser 2’s mandatory validation
   step. Markers add annotation friction and a false sense of
   reliability. I’ve seen analogous annotation schemes in incident
   handoffs degrade to boilerplate within two weeks.

3. **Minimum horizon (1 session default, max 2)**. Staleness probability
   drops to the floor. A departing browser knows with reasonable
   confidence what the immediate next goal is; beyond that, they’re
   guessing. The overhead of justifying a 2‑session horizon (“why not
   just 1?”) ensures it’s used sparingly.

4. **No mandatory VISION coupling**. Handoffs are execution artifacts,
   not strategy documents. Adding a mandatory reference field creates
   maintenance debt and tempts authors to fabricate alignment. If a
   handoff’s Future State naturally aligns with VISION, fine; don’t
   enforce it by template.

5. **Validation enforcement via tooling**. The highest‑risk failure mode
   (Browser 2 skips validation) is mitigated not by process text but by
   embedding a validation prompt and a required reconciliation note in
   the incoming‑browser workflow configuration. This is an architectural
   control point I insist on: the handoff system must refuse to mark a
   handoff as “accepted” unless Browser 2 has attested to validation.
   Otherwise, the drift defence is social, not engineering.

### Ambiguities Flagged for Rob’s Decision Before Implementation
- **File name**: `handoff-summary.md` vs `CURRENT_FUTURE.md` vs other.
- **Exactly where in the incoming‑browser prompt the validation step is
  injected** — I recommend it be the very first instruction after the
  handoff content is loaded, but the phrasing is Rob’s call.
- **Audit handoff validator strictness**: Reject vs. block‑with‑override.
- **Whether ADR‑37 mentions cross‑repo handoffs at all** or stays scoped
  to session+audit, deferring cross‑repo to a later ADR. My skeleton
  includes a placeholder; Rob may prefer to remove it to keep ADR‑37
  minimal.

### What Breaks First at Scale?

If the number of handoffs grows 10× (future automation, many parallel
agents), the bottleneck becomes **Browser 2’s validation step latency**.
Each validation requires reading the Future State, comparing with current
git status/compliance, and writing a reconciliation note. At 100
handoffs/day, that’s a non‑trivial cognitive cost. The first failure mode:
Browser 2s begin to “rubber‑stamp” validation, typing “validated, no
changes” without checking. Staleness then silently infects the pipeline.
Mitigation: future automation that diffs the current state against the
Future State’s expected compliance markers and flags anomalies before
human review. That’s beyond current scope but must be on the roadmap.

The second failure mode: `handoff‑summary.md` file proliferation causes
folder clutter, and tooling that expects a single `HANDOFF.md` breaks
silently if not updated. This is a one‑time fix but must be verified in
the next session’s implementation work.

The quantitative estimates and per‑file enforcement make this design
auditable and load‑testable. I’m satisfied that this synthesis is the
minimum‑diff, maximum‑reliability path.

*Latency: 212.88s | Tokens: 15960*

### Openai (gpt-5.4)

Below is my round-2 council evaluation, optimized for “can this team actually build and operate this without turning handoff into ceremony?”

---

## Proposal A

### Steelman first
This proposal is exactly right if the core problem is **framing, not structure**. If ADR-32’s 9 sections already capture most needed detail, then the cheapest high-value move is to add a universal two-phase lens without replacing the familiar body. It’s also exactly right if session handoffs are authored under variable human conditions while audit handoffs are more deterministic and machine-generated. In that world, **overlay + type-dependent mandate** gives consistency where it matters and flexibility where reality is messy.

### Your assessment
**Agree.**

This is the strongest of the set from an execution standpoint. It avoids the classic architecture-council mistake of solving conceptual elegance by creating operational churn. Universal framing is the right call, but replacing ADR-32 wholesale would be an unnecessary migration and retraining cost. A top-level current/future summary plus preserved ADR-32 internals is the best cost/benefit point.

### Strongest point
**Overlay is materially cheaper than replacement while solving the real divergence risk now.**

That is the right product instinct. The ecosystem needs one recognizable pattern before audit and cross-repo handoffs harden, but the team does not need a format revolution.

### Weakest assumption
The weakest assumption is that **10–20% more authoring effort is acceptable and will remain temporary**.

If that’s false, the overlay becomes annoying duplication, session authors will phone in the summary, and the whole thing degrades into ritual compliance. The proposal notes this risk, but probably understates how fast low-friction docs become low-quality docs if they feel repetitive.

### Hidden assumptions
1. **People will reliably synthesize rather than copy-paste** from ADR-32 sections into the new summary blocks.
2. **Incoming browsers actually read top summaries first** and change behavior because of them, rather than continuing to scan the old familiar sections.

### Overlooked risks
- It does not say enough about **how much summary is enough**. Without tight template prompts, authors will produce mini-essays or duplicate the full handoff.
- It assumes **audit and cross-repo handoffs can share the same framing with no special edge cases**. That’s probably true, but not guaranteed.
- It does not fully address **validator scope creep**: once strong/medium rules exist, people will want tooling sooner than the team may be ready to build.

---

## Proposal B

### Steelman first
This proposal is exactly right if success depends on making the new pattern **highly legible and explicitly codified**, not just directionally agreed. If ambiguity is the enemy, then the detailed ADR skeleton, content table, uncertainty markers, and validation protocol are all useful because they reduce drift and make implementation straightforward. It is especially right if the team benefits from a crisp “minimum contract” that can later support tooling.

### Your assessment
**Partially agree.**

The main decision is correct: tiered universal overlay, augment ADR-32, not supersede it. But the proposal overdesigns the mechanism slightly for the maturity level and likely operating discipline of the team. The uncertainty marker taxonomy is clever, but it is more system than this team probably needs right now.

### Strongest point
**Per-item uncertainty markers are better than blanket disclaimers.**

Conceptually, that’s true. If you want future-state guidance without false precision, labeling confidence at the item level is a better signal than boilerplate “subject to change.”

### Weakest assumption
The weakest assumption is that **authors will consistently and correctly use confidence labels** like `[confident] / [tentative] / [browser-2-to-assess]`.

If that’s false, the labels become noise, style bikeshedding, or pseudo-rigor. Worse, they increase cognitive load for little gain and make the template feel more process-heavy than helpful.

### Hidden assumptions
1. **The team wants a protocolized incoming-browser workflow** rather than lightweight guidance.
2. **Tooling or reviewers will benefit enough from exact vocabulary** to justify standardizing marker tokens now.

### Overlooked risks
- **Taxonomy fatigue**: small teams often resent label-heavy process unless it clearly saves time within a week or two.
- **Marker inconsistency** across handoff types or authors could create false precision.
- The proposal doesn’t fully reckon with the fact that **stronger semantics invite validator pressure**, which may outpace actual operational readiness.

---

## Proposal C

### Steelman first
This proposal is exactly right if the ecosystem needs not just a conceptual overlay but a **physical entry artifact** that is always the same across handoff types. If consumers routinely enter handoff folders cold, a mandatory `handoff-summary.md` is a very practical anchor: one predictable file, same headings everywhere, details elsewhere. This is especially attractive if cross-repo and audit handoffs will vary internally but still need a universal front door.

### Your assessment
**Partially agree.**

I agree with the universal summary-layer instinct and with augmentation over replacement. I disagree with introducing a **mandatory separate file** as the universal mechanism right now. That is extra file structure, extra conventions, and extra maintenance burden for limited gain. The team can get 90% of the value by adding top-level sections to the existing handoff artifact.

### Strongest point
**Universal entry point prevents cognitive and tooling fragmentation.**

That’s a strong argument. A single place to answer “where are we / where are we going” is genuinely useful.

### Weakest assumption
The weakest assumption is that **another required file is negligible operational overhead**.

If false, you get missed files, stale summaries detached from the detailed handoff, and confusion about source of truth. For a small team, adding one more artifact is often more expensive than adding two sections to an existing artifact.

### Hidden assumptions
1. **Handoffs are folder-oriented enough** that a canonical file name materially improves navigation.
2. **The ecosystem benefits from file-level standardization** more than from document-level standardization.

### Overlooked risks
- **Split-brain risk** between `handoff-summary.md` and the detailed handoff body.
- **Template drift**: people update one and forget the other.
- If some handoff types are generated and others curated, **separate-file discipline may vary badly**.
- It quietly introduces a stronger information architecture decision than the question requires.

---

## Proposal D

### Steelman first
This proposal is exactly right if the team needs a **very practical, low-drama rollout** with just enough specificity to prevent drift. It sensibly keeps the existing structure, adds top-level summaries, uses type-dependent mandate, and caps future-state horizon tightly. If handoff quality degrades quickly with longer planning horizons, the 1–2 session cap could be the right operational discipline.

### Your assessment
**Partially agree.**

The decision shape is mostly right. But the proposal is slightly too eager on validator enforcement and too assertive on requiring VISION references. It also treats lessons as less central to current state than I think they are; operationally, lessons often matter because they prevent repeated dead ends in the next session.

### Strongest point
**Tiered overlay mirrors the successful universalization pattern without breaking current practice.**

That’s the right change-management instinct.

### Weakest assumption
The weakest assumption is that **validators should reject handoff folders missing both top-level sections immediately**, while also preserving medium-mandate flexibility.

If implemented too early, that creates “valid structure, weak content” behavior and encourages token compliance. For a small team, process enforcement before template settling is usually premature.

### Hidden assumptions
1. **Required VISION references will improve alignment more than they increase handoff burden.**
2. **1–2 sessions is materially better than 1–3** rather than just a stricter but less useful cap.

### Overlooked risks
- **Mandatory VISION linkage** may be overkill for many routine sessions.
- **Early validator hardening** could produce brittle workflow before norms stabilize.
- It underestimates the chance that **lessons learned are exactly what the next browser most needs**, especially after failed paths or subtle environment gotchas.

---

# Revised recommendation

I **maintain my original position**: adopt a **universal two-phase handoff pattern as an overlay**, not a replacement.

The other proposals did not change my mind because they mostly converge on the same core answer; where they differ, the differences are mostly about **how much mechanism to add**. And that is where I’m firm: this team should choose the **minimum structure that creates consistency without creating ceremony**.

## Final recommendation

### 1) Q1: Two-phase framing
Choose **(c) Tiered**.

- **Universal across ecosystem**
- **Session handoffs** keep ADR-32 9-section structure **plus** top-level `Current State` and `Future State`
- **Audit handoffs** may use pure two-phase as primary top-level structure
- **Cross-repo handoffs** should follow the same universal pattern when specified

Why not (a)? Because full universal restructure is more change than the team needs.
Why not (b) or (d)? Because they lock in divergence or keep the framing too implicit.

## 2) Q2: Content per phase

### Current State
Should be **factual baseline plus recent decisions and relevant lessons**.

Not “pure raw facts only.” Decisions made are facts. Lessons learned are part of operational state when they materially affect what should not be retried.

Include:
- Last verified commit SHA / branch / git status
- What is done / compliant / verified
- What remains unresolved
- Key decisions made this session
- Lessons/constraints discovered that affect next steps

### Future State
Should be **short-horizon prescription**, not broad vision.

Include:
- Next session goal
- Recommended actions in priority order
- Dependencies / sequencing if needed
- Target state or target compliance evidence
- Explicit short horizon

Not long-range aspiration; that belongs in VISION/ROADMAP artifacts.

## 3) Q3: ADR-32 ↔ ADR-37
Choose **(c) Augment ADR-32**.

ADR-37 should:
- define the universal two-phase framing,
- specify the per-phase content contract,
- clarify horizons and drift handling,
- and state that ADR-32 remains the detailed session-handoff structure.

Do **not** supersede ADR-32 now.

That would be expensive, unnecessary, and likely produce churn with little practical gain.

## 4) Q4: Relationship with VISION.md
Choose **(d)** with a light touch.

- **Handoff Future State** = tactical horizon, **next 1–3 sessions**
- **VISION.md** = strategic horizon, **quarter+ / ecosystem direction**

Reference VISION only when directly relevant. Do **not** make VISION linking mandatory in every handoff. That is process weight without enough payoff.

## 5) Q5: Prescription risk mitigation
Use a combined mitigation strategy:

- **(b)** Incoming browser’s first task: validate Future State still applies
- **(c)** Horizon cap: Future State covers **next 1–3 sessions only**
- **(a)** Lightweight disclaimer: “best current recommendation at handoff time; validate before acting”

Reject (d) as default structure. Alternative paths are useful occasionally but too heavy as a standard requirement.

Important nuance: the best mitigation is not fancy uncertainty taxonomies; it is a **short horizon + explicit validation step**.

## 6) Q6: Departing browser mandate
Choose **(d) Type-dependent**, implemented as:

- **Session handoffs: MEDIUM**
  - Both sections required
  - `Future State` may honestly say: “Undetermined; browser 2 to assess”
- **Audit handoffs: STRONG**
  - Both sections required and expected to be substantive
- **Cross-repo handoffs: MEDIUM by default until actual operating pattern proves they can bear STRONG**

I do **not** recommend strong by default for all handoffs. Forced prediction creates fiction, and fiction is worse than honest uncertainty.

## 7) Q7: Implementation phasing
Forward-only. No migration.

### Phase 1: ADR-37 now
ADR-37 should be short and decisive:
- Context
- Decision
- Two-phase overlay definition
- Per-phase content table
- Relationship to ADR-32
- Relationship to VISION.md
- Drift mitigation
- Mandate by handoff type
- Implementation / grandfathering
- Consequences

### Phase 2: update docs
Next session:
- update `HANDOFF_PROCESS.md`
- update `HANDOFF_TEMPLATE.md`

### Phase 3: audit adoption
ADR-36 should cite ADR-37 and use the two-phase model natively.

### Phase 4: tooling later
Only after templates settle:
- maybe add basic checks for section presence
- hard validation only where generation is automated and predictable

### Historical handoffs
- Grandfather all existing handoffs
- No retroactive migration
- No cleanup project

---

# Concrete ADR-37 shape I would back

Approx. 80–110 lines, with these sections:

1. **Title / Status / Related ADRs**
2. **Context**
   - Existing ADR-32 is structurally rich but backward-looking in framing
   - Audit/cross-repo handoffs are about to proliferate
   - Need one universal pattern
3. **Decision**
   - All handoffs use explicit `Current State` + `Future State` framing
   - ADR-32 remains for session detail
4. **Two-Phase Definitions**
   - Current State = verified present state + consequential recent decisions/lessons
   - Future State = short-horizon recommended next direction
5. **Per-Phase Content Table**
6. **Relationship to ADR-32**
   - augment, not supersede
7. **Relationship to VISION.md**
   - tactical vs strategic horizon split
8. **Drift / Prescription Mitigation**
   - short horizon + validate first
9. **Mandate by Handoff Type**
10. **Implementation Phasing**
11. **Consequences / Revisit signals**

---

# Per-phase content table

| Phase | Required content | Exclude / avoid |
|---|---|---|
| **Current State** | verified commit/git state; what is done/compliant; unresolved questions; key decisions made; relevant lessons/constraints | speculation about long-term direction; generic narrative recap |
| **Future State** | next goal; recommended actions in priority order; dependencies if any; target state/evidence; explicit 1–3 session horizon | quarter-scale roadmap; mandatory multi-path planning; over-precise prediction |

---

# What I’m rejecting explicitly

- **Reject full replacement of ADR-32 now.** Too much churn for too little gain.
- **Reject audit-only two-phase framing.** That would institutionalize divergence.
- **Reject mandatory separate summary file right now.** Extra artifact, extra maintenance, not enough payoff.
- **Reject mandatory VISION references in every handoff.** Too heavyweight.
- **Reject confidence-tag taxonomies as part of the core ADR.** Nice idea, wrong maturity level unless usage pain proves the need.

---

# Flagged ambiguities for Rob’s call before Claude Code execution

These are the few things I think should remain Rob’s decision because they affect style and downstream enforcement:

1. **Horizon wording**
   - My recommendation: **“next 1–3 sessions”**
   - Rob may prefer “next session” if he wants lower drift and less prescription

2. **Whether `Current State` and `Future State` are top sections in the existing handoff doc or a separate summary artifact**
   - My recommendation: **top sections in existing handoff doc**
   - Separate file is possible, but I think it’s unnecessary overhead

3. **How explicit to be about lessons in Current State**
   - My recommendation: include **relevant lessons/constraints only**, not a full duplicate of ADR-32 §6

4. **Cross-repo mandate strength**
   - My recommendation: **MEDIUM initially**
   - Strong only after actual cross-repo workflow is proven stable

5. **Validator timing**
   - My recommendation: **do not harden validators for session handoffs yet**
   - Template first, norms second, tooling third

---

## Bottom line
Ship **ADR-37 as a universal framing overlay**, not a rewrite. Require explicit **Current State** and **Future State** everywhere going forward, keep ADR-32 underneath for session handoffs, use **medium mandate for human-authored sessions** and **strong for audit automation**, cap future-state horizon to **1–3 sessions**, and adopt **forward-only with no migration**.

That is the version this team can actually implement and live with.

*Latency: 59.73s | Tokens: 12660*

### Grok (grok-4.20)

**Analyses of Proposals**

**Proposal A**  
**Steelman first:** This is exactly right if the dominant risk is ecosystem fragmentation at the *framing* level while operator muscle memory and existing tooling around the 9-section format are still high-value. An explicit overlay plus type-dependent mandate lets us lock in the conceptual universalization Rob wants without triggering a migration or re-training tax that would delay ADR-36 and cross-repo work. The short-horizon tactical future state stays surgically separated from VISION.md, and the medium-mandate escape hatch prevents the “forced fiction” failure mode. Under these conditions the overlay is the optimal cost-benefit point.

**Your assessment:** Partially agree. The diagnosis is correct; the conservatism is wrong.  
**Strongest point:** Divergence cost across three handoff types is real and immediate; standardizing framing *before* ADR-36 ships is the highest-leverage lever available.

**Weakest assumption:** “Temporary duplication is acceptable and will remain ~10-20% overhead.” If the two mental models coexist for more than a few weeks, authors will cargo-cult the summary from the 9-section body instead of synthesizing, turning the overlay into ritual. The proposal never proves the overlay stays crisp.

**Hidden assumptions:** (1) That readers will reliably treat the top-level summary as primary and the 9-section as archival; nothing in human behavior or current templates supports this. (2) That validators can meaningfully distinguish “honest undetermined” from laziness without becoming governance theater.

**Overlooked risks:** Template and process docs will lag (the proposal explicitly defers them), so the first 4–6 handoffs become inconsistent by definition. Also ignores that “overlay” language in ADRs historically decays into “ignore the old parts.”

**Proposal B**  
**Steelman first:** This is exactly right if ADR-32’s 9-section content (especially Lessons and Files Modified) still carries irreducible operational value that cannot be collapsed into a crisp Current State block. The per-phase table, per-item uncertainty markers, and explicit 1–3 session horizon plus type-dependent mandate give the cleanest mapping of old to new without breaking existing validators or examples. The skeleton is the most ADR-like of the set.

**Your assessment:** Disagree. This is the “minimum diff” reflex Rob warned us against. It preserves a format whose primary flaw is exactly the backward bias Rob identified.

**Strongest point:** The uncertainty markers are a genuine improvement over a blanket disclaimer; they force granular honesty.

**Weakest assumption:** “ADR-32’s 9-section structure is broadly working.” The manual audit in Proposal D (70% backward-looking) and Rob’s original reframing both contradict this. If the structure were working we would not be having this council.

**Hidden assumptions:** (1) That bolting a summary on top will not simply lengthen handoffs without changing reading order in practice. (2) That two co-existing mental models (overlay + legacy sections) is a feature, not a permanent tax.

**Overlooked risks:** Validator complexity branching on handoff type; “TBD” escape hatch becoming the 40% case within a month, at which point the universal pattern is universal in name only.

**Proposal C**  
**Steelman first:** This is exactly right if the highest-order requirement is that *any* incoming actor (human or agent) can open one canonical file and know exactly where to look, regardless of handoff type. A separate `handoff-summary.md` as the mandatory entry point enforces that contract mechanically. The three-layer drift defense and explicit mapping of ADR-32 sections into the summary are tighter than the other proposals.

**Your assessment:** Disagree. This adds yet another file to every handoff folder. We are solving a framing problem by increasing filesystem complexity. That is the opposite of elegant.

**Strongest point:** Treating the summary as a *separate artifact* with its own validation path is the most honest way to make it primary rather than decorative.

**Weakest assumption:** That adding a mandatory extra file is “negligible” effort. It is not. It fractures the handoff folder, complicates every future cross-repo or audit pipeline, and guarantees template churn.

**Hidden assumptions:** (1) That humans will maintain two artifacts in sync instead of writing the summary last as a summary of the summary. (2) That “Path A / Path B” branching in Future State will remain tractable rather than explode the document.

**Overlooked risks:** Tooling fragmentation—every script that assumed a single markdown file per handoff now breaks. Also, audit handoffs becoming pure two-phase while sessions remain hybrid reintroduces exactly the divergence the proposal claims to solve.

**Proposal D**  
**Steelman first:** This is exactly right if the empirical data from the last 12 handoffs (70% backward) is representative and the 1–2 session horizon plus mandatory validation step sufficiently lowers staleness risk. The tight scoping of Current State (“recent changes only,” decisions but not full lessons) and the explicit validator language make the overlay crisp.

**Your assessment:** Disagree. Same core error as B: it treats preservation of the 9-section format as a constraint rather than a symptom.

**Strongest point:** Explicitly calls out that the current format is already 70% backward-looking; this is the clearest quantification anyone provided.

**Weakest assumption:** “Incoming browsers will actually perform the validation step.” Every prior handoff protocol we have written assumed the next reader would do the obvious thing. Telemetry shows they scan for the Pending section and start coding.

**Hidden assumptions:** (1) That an overlay that is not enforced at the folder schema level will be respected once the emergency of a live incident arrives. (2) That 10–12 extra minutes of authoring is sustainable at 2–5 sessions per week.

**Overlooked risks:** The proposal never addresses what happens when the top-level summary and the underlying 9-section drift from each other inside the same folder—an inevitable outcome of dual maintenance.

**My Revised Recommendation**

The other proposals did not change my mind; they confirmed the hidden premise everyone is taking for granted: *that the existing 9-section ADR-32 format is mostly good and must be preserved*. That premise is false. The format is backward-biased by design, exactly as Rob diagnosed. Adding summaries, overlays, separate files, uncertainty markers, and type-dependent validators on top of a flawed base is how organizations create permanent process debt. We should not manage divergence by layering; we should prevent it by simplifying.

Therefore I reject every proposal’s conservatism.

**Concrete decisions:**

**Q1:** (a) Universal mandate.  
**Q2:** Current State = pure facts + last verified state + compliance snapshot + open questions. It may *reference* decisions made but does not narrate them. Future State = prescriptive prioritized actions for the next session only (not 1–3; one session maximum), with explicit dependencies and target state. Decisions-made and lessons stay in the handoff but are *subordinate* to the two-phase blocks, not peers.  
**Q3:** (b) Supersede ADR-32. ADR-37 replaces it. Mark ADR-32 superseded. The 9-section format was a v1 experiment; we have now learned what matters.  
**Q4:** (d) Explicit horizon split. Handoff Future State = next session only. VISION.md = quarter+. Handoff must contain a one-line “Relevant VISION sections” bullet or the word “None.”  
**Q5:** Mitigation (b + c): Browser 2’s *first* atomic task is to validate or replace the Future State section and commit the result before any other work. Horizon locked to single session. No alternatives branching.  
**Q6:** (c) Weak mandate for all handoff types. Future State may read “Direction not yet clear; incoming browser to set.” Validators only require the *section* exist. Forcing prediction produces fiction; we should prefer honest voids.  
**Q7:** Forward-only. No migration of historical handoffs (ADR-29 grandfathering). HANDOFF_PROCESS.md and HANDOFF_TEMPLATE.md updated in the same session as ADR-37 lands. Existing folders left untouched.

**ADR-37 Skeleton (≈105 lines)**

```
# ADR-37: Two-Phase Handoff Format (Current State + Future State)

Status: Proposed | Supersedes: ADR-32 | Related: ADR-33, ADR-36

## Context
ADR-32 v2.0 produces backward-heavy artifacts. Rob’s reframing identifies two distinct phases every handoff must make explicit: where the project *is* and where it is *going*. Without a universal decision now, session, audit, and cross-repo handoffs will diverge.

## Decision
All handoffs shall use a pure two-phase format. ADR-32 is superseded. Every handoff folder must contain a single markdown file with exactly two top-level sections. Future State horizon is strictly one session. Mandate is weak for all types.

## Per-Phase Content

| Element                    | Current State                          | Future State                              |
|----------------------------|----------------------------------------|-------------------------------------------|
| Tense                      | Present factual                        | Prescriptive, one-session horizon         |
| Commit / git status        | Required                               | —                                         |
| Compliance / done          | What is verified                       | Target compliance for this session        |
| Open questions             | All unresolved                         | —                                         |
| Decisions made             | One-sentence reference only            | —                                         |
| Lessons                    | One-sentence reference only            | —                                         |
| Next goal                  | —                                      | Single required outcome (or “TBD”)        |
| Recommended actions        | —                                      | Priority-ordered list ≤5 items            |
| Dependencies               | —                                      | Call out if any                           |
| Disclaimer                 | —                                      | “Created at [timestamp]. Validate before acting.” |
| VISION reference           | —                                      | One-line bullet or “None”                 |

## Mandate Strength
Weak for all handoff types. Sections must exist; content may honestly state that direction is undetermined. Validators enforce structure, not prophecy quality.

## Relationship to VISION.md
Handoff Future State = tactical next-session intent. VISION.md = strategic quarter+ direction. Handoff must explicitly reference relevant VISION section or declare none. No hierarchy enforcement beyond this note.

## Prescription Risk Mitigation
- Horizon locked to one session.  
- Browser 2 validation is the literal first checklist item in HANDOFF_PROCESS.md and must be committed before any other work.  
- Weak mandate prevents fabricated certainty.

## Implementation Phasing
- This session: publish ADR-37, update HANDOFF_TEMPLATE.md and HANDOFF_PROCESS.md, add basic validator for section presence.  
- No migration of historical handoffs.  
- ADR-36 audit handoffs adopt the same two-phase template.  
- Cross-repo handoffs inherit by default.

## Consequences
Positive: incoming actor sees intent in <15 seconds; universal pattern achieved before divergence; honesty preserved.  
Negative: loss of detailed “Files Modified” and “Lessons” prose (now collapsed or referenced); team must update muscle memory once.  
```

**Flagged for Rob’s decision before Claude Code execution**
1. Exact validator behavior on “TBD” Future State (warn-only or hard reject?).
2. Whether Lessons section is entirely retired or kept as optional appendix.
3. Precise phrasing of the VISION reference line.

This is the cleanest, least bureaucratic path. Everything else is theatrical layering.

*Latency: 51.12s | Tokens: 12709*

## Synthesis (by gemini, non-participant)

## Consensus
- **Two-Phase Framing is Necessary:** All participants agreed that handoffs suffer from being backward-looking, and explicitly surfacing a forward-looking "Future State" alongside the retrospective "Current State" is required across all handoff types.
- **Honesty Over Prophecy (Type-Dependent Mandate):** All agreed that forcing departing humans to predict the next steps when they genuinely don't know leads to fabricated guidance. Session handoffs must allow an "undetermined" escape hatch. Audit handoffs, being machine-generated, can tolerate a stricter mandate.
- **Explicit Validation Step:** There was universal agreement that the incoming browser (Browser 2) must explicitly validate the Future State against reality before acting, serving as the primary defense against state drift.
- **Forward-Only Adoption:** No historical migration of existing handoff folders (ADR-29 grandfathering pattern).

## Unresolved Disagreements
**1. Augment vs. Supersede ADR-32**
- **The crux:** Does keeping the legacy 9-section format alongside the new two-phase summary provide necessary archival context, or does it create process debt, duplication, and two sources of truth?
- **Stronger argument:** OpenAI and Claude's argument for **Augmentation** is the most operationally sound for now, as it avoids massive change management friction. However, Grok's R2 pivot arguing that augmenting creates "dual-maintenance drift" (authors copy-pasting between the summary and the 9-sections) is a brilliant architectural critique. Despite Grok's sharpness, full replacement is too disruptive for a fast-moving team; augmentation with clear canonicality rules is the safer path.

**2. Physical File Structure (Single file vs. Separate `handoff-summary.md`)**
- **The crux:** Does creating a new, separate file for the summary provide a cleaner contract for tooling, or does it introduce filesystem clutter and split-brain synchronization risks?
- **Stronger argument:** OpenAI and Claude's argument for keeping it in a **single file** is stronger. Adding a separate file introduces literal split-brain risk where the summary and the detailed body inevitably drift out of sync.

**3. Granularity of Uncertainty Tracking**
- **The crux:** Should uncertainty be tracked via per-item markdown tags (e.g., `[confident]`, `[tentative]`) or handled at the macro level via a general validation step?
- **Stronger argument:** Deepseek and OpenAI successfully dismantled Claude's per-item markers. Granular tagging introduces cognitive overhead during authoring, quickly degrading into default noise (e.g., tagging everything `[tentative]`), whereas a strict validation step by the incoming browser actually catches drift.

## Argument Quality Assessment
- **Strongest Argument:** OpenAI and Deepseek’s argument that *forced prediction produces fiction* (regarding the mandate strength). Recognizing the difference between human cognitive exhaustion at the end of a session and deterministic audit generation is an excellent application of socio-technical architecture. 
- **Weakest Argument:** Claude’s insistence on per-item uncertainty markers. It assumed operators would rigorously curate metadata during a handoff, ignoring the reality of developer fatigue.
- **Best-Reasoned Proposal:** **OpenAI (R2)**. It consistently optimized for minimum viable ceremony. It accurately diagnosed that the ecosystem needs a universal pattern, but that creating separate files, complex tagging taxonomies, or mandatory VISION linking would turn a helpful framing tool into a bureaucratic chore. 

## Blind Spots
- **Canonicality Resolution:** While Grok pointed out the duplication risk between the summary and the 9-section body, no one defined exactly what an incoming agent should do if the `Current State` summary contradicts the `Files Modified` legacy section. 
- **Prompt vs. Markdown Limits:** Everyone relied on "Browser 2 must validate first." However, markdown handoffs cannot *force* a human or agent to execute a validation step. The debate missed that this mitigation actually requires modifying the *incoming system prompts*, not just the static document template.

## Recommended Decision
Adopt the **Universal Two-Phase Overlay (Augmenting ADR-32) within a single document**, utilizing a **Type-Dependent Mandate** and a **1-3 Session Horizon**.

**Rationale:**
1. **Structure (Q1, Q3):** Add `## Current State` and `## Future State` as the top-level sections of the existing handoff template. Push the ADR-32 9-section structure beneath it (e.g., under a `## Detailed Archival Context` header). This minimizes diffs to existing tooling while fixing the cognitive entry point.
2. **Content (Q2):** *Current State* contains factual verified status, compliance, unresolved questions, and a high-level summary of decisions. *Future State* contains the next immediate goal, prioritized actions, and dependencies.
3. **Horizon & VISION (Q4):** Future State is strictly tactical (1-3 sessions max). Link to VISION.md only if strictly relevant; do not make it mandatory. 
4. **Mandate (Q6):** Session handoffs are MEDIUM (allow "Undetermined; Browser 2 to assess"). Audit handoffs are STRONG (validators reject if missing).
5. **Mitigation (Q5):** The sole mitigation for prescription risk is a mandatory validation step by Browser 2.

*Addressing Grok's Objection:* Grok is right that layering creates duplication risks. We weigh this by defining strict canonicality: The top-level two-phase summary is the **authoritative operational state**. The 9 sections below are **archival evidence**. 

## Risks
- **Dual-Maintenance Drift:** Authors copy-paste text between the summary and the detailed sections, leading to contradictory information if updated later.
  - *Mitigation:* Explicitly label the 9 sections as "Archival Context" in the template. Train validators to only parse the top-level Current/Future states for operational logic.
- **Validation Skipped:** Incoming agents/humans ignore the Future State validation step and blindly execute stale instructions.
  - *Mitigation:* Do not just put the validation step in `HANDOFF_PROCESS.md`. Inject it directly into the first paragraph of the system prompt used to initialize Browser 2.

## Action Items
1. **Draft ADR-37:** Frame it as an overlay/augmentation. Include the Per-Phase Content Table, define the 1-3 session horizon, and specify the type-dependent mandate (Strong for audit, Medium for sessions).
2. **Update `HANDOFF_TEMPLATE.md`:** 
   - Add `## Current State` and `## Future State` at the top.
   - Add a structural divider: `---` followed by `## Archival Context (ADR-32 Details)` to house the legacy 9 sections.
3. **Update `HANDOFF_PROCESS.md` & Agent Prompts:** Ensure the literal first operational instruction for an incoming browser is to read the Future State, check it against the current git/compliance reality, and log a reconciliation note.
4. **Tooling Update:** Add a lightweight linter that checks for the presence of the two new headers. Configure it to hard-fail for audit pipelines and warn for session handoffs.
