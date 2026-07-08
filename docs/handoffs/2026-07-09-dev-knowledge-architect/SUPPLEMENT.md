# Architect strategic supplement — 2026-07-09-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-09

> **Operator — 3 steps:**
> 1. Copy the QUESTIONS below into the outgoing architect chat (the chat that did this
>    session's work).
> 2. Paste that chat's answers into the ANSWERS section at the bottom — combine multiple
>    chats if needed.
> 3. Tell CC `supplement filled` → CC commits this file on the handoff branch and folds
>    the answers into the next session's PASTE_THIS.
>
> **No outgoing chat to ask (cold / cleared handoff)?** Leave ANSWERS empty. The next
> session captures off-repo context live via the §13(d) operator-context beat. The empty
> file is still committed — a record that this session had no transmissible live "why"
> (this is the defined cold-handoff disposition, not a defect).

## QUESTIONS — paste these to the outgoing architect chat

1. **Strategic intent** — what should the next session achieve at the way-of-working
   level? (A design / methodology goal, not a task.)
2. **Tensions weighed** — which design trade-offs were weighed, where did you land, and
   why?
3. **Considered + rejected** — which options were rejected and why (so the next session
   does not relitigate them)?
4. **Open questions** — which design questions are unresolved or deliberately deferred?
5. **Decomposition rationale** — why this task-graph shape? What must the next session
   NOT redo or re-decide?
6. **Off-repo context** — intent, priorities, changed decisions, or findings not in the
   repo.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

A. **CC-observed residual (session-close 2026-07-09, #255 retirement):** the conformance-digest
   mechanism was retired (workflow removed, remote branch deleted, `surface_triage.ps1` Surfacing 2
   removed, #255 closed) — but the LIVING-doc narrative still describes it as current in
   `ARCHITECTURE.md` (Ch ~440/442/600, incl. an outcome-table row) and `CONTRIBUTING.md` (~L134–147).
   Left un-edited deliberately (out of the operator's #255 contract scope + touching them triggers a
   `canonical_freshness` re-stamp); ship-gate is GREEN (the prose is ungated). Reconcile this
   narrative as part of absorbing the retirement. The ADR-84 record itself is immutable (correct as
   history).

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

A1 (strategic intent): SEED 6–9 triage (accept→elaborate / defer / reject) → selective brainstorm Wave-1 admission (F1: backlog stays short, post-shrink budget ~74) → Wave-1 per-repo sequencing, ai-council first. #264 rides SEED-9.

A2 (tensions weighed): build-pull of 4 fresh SEEDs vs admission discipline; night layer (SEED-8) stays behind #270 gate absolutely.

A3 (considered + rejected — do NOT relitigate): all 2026-07-08 leg-c rulings; the 39 WEAK rejections; #255 retirement; guard-v3 three-tier design.

A4 (open questions): first LIVE exercise of the filing-backpressure hook (proven in tests, not yet in a real filing); #122 shim references (billing_leak_sentinel) need untangling before delete; V1/V2 changelog spot-checks optional.

A5 (decomposition rationale): triage order 6→7→8→9 (bootstrap = biggest absorber first; dashboards last — needs the operator's one-sentence Arc-5 P6 usability verdict as its ex-ante gate).

A6 (off-repo context): Fable reset ~21:00; three-repo backups now exist (F1 closed via #291); operator usability sentence for #264/SEED-9 still outstanding.
