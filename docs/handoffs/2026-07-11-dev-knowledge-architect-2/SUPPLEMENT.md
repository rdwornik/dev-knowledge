# Architect strategic supplement — 2026-07-11-dev-knowledge-architect-2

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-11

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

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

STRATEGIC INTENT — CONSUMER ROLLOUT WAVE: universalize + hermetize ai-council and
corp-monorepo as goal ONE. Every mechanism built in the prior arc must be SEEN
working in a consumer: Form-A boundary markers in each consumer CLAUDE.md, carried
gates ARMED AND FIRING, global-vs-local split visible per repo (methodology =
hub-owned, project = local, machine-readable). Way-of-working shift: hub-building
posture -> fleet-rollout posture. Second axis: the methodology must be TESTABLE
continuously — the night-batch pattern (proven 2026-07-11->12) becomes a standing
routine: night runs verify hygiene/audit-naming/boundary-drift + stage work; a
standard MORNING PROMPT consumes the verdict-sheet (review -> consolidate ->
decide). Third axis: token economy — Codex as PRODUCER for long bounded tasks
(CC verifies state-fidelity, architect reviews), Claude Opus reserved for
judgment; Codex substrate confirmed at 5.6 (sol/terra/luna live in CLI).

TENSIONS WEIGHED — (a) rollout speed vs carrier quality: #318/#319 (Codex parity
findings) triage FIRST, then ai-council GO — arming known-holed gates in a
consumer is rejected. (b) Codex producer substrate: CONFIRMED live by operator
(gpt-5.6-sol/terra/luna in the CLI /model selector; the config.toml pin was
stale at gpt-5.5 -> corrected to gpt-5.6-sol). Producer/CC-verifies contract AND
the variant-routing pilot both proceed NOW: working hypothesis = SOL for
long/complex bounded builds, TERRA for everyday bounded tasks, LUNA for cheap
fan-out/mechanical passes — mirroring the Opus/Sonnet/Haiku doctrine one-to-one;
the pilot assigns real task classes with ex-ante criteria. (c) audit-corpus
growth vs navigability: the corpus earned its cost (matrix -> rulings ->
mechanisms) but needs a sequential review pass — every audit gets a verb
(keep/archive/delete-candidate), lists + paths produced by a night leg, operator
rules deletions. (d) plan-continuity placement: the plan-of-record is authored
at session END by the outgoing architect and consumed at the NEXT session's boot
as the comparison baseline (#301 clause iv prior_plan carrier) — both ends, one
artifact.

CONSIDERED + REJECTED (do not relitigate) — (a) consumer rollout before
#318/#319 triage: rejected. (b) ad-hoc Codex adoption without doctrine: rejected
— EPIC H axis, pilot with ex-ante criteria. (c) deleting audits without a
reviewed verb list: rejected (never-delete-without-asking). (d) waiting or
gating on Codex 5.6 availability: OBSOLETE — availability operator-confirmed
live; the earlier "ABSENT from CLI" claim was a config-vs-selector conflation
(config pin states the DEFAULT, the CLI selector states AVAILABILITY). (e)
treating the night-batch as one-off: rejected — it graduates to a standing
routine with a morning-prompt consumer.

OPEN QUESTIONS — (a) Mermaid/ToC successor: C4 architect-owed, 4x overdue,
blocks DEFER(c) + the #322 dashboard visualization leg. (b) D1 ruling (global
core-invariant #2 -> parallel verify) at #317 build. (c) BACKLOG notation
grooming (restore S-n/epic markers, E-prefix decision, 57 WEAK). (d) Codex
SOL/TERRA/LUNA task-class assignment — pilot design, first consumer = which
task? (e) automation/fleet-audit integrate-or-abandon. (f) which night-batch
legs become the standing routine vs stay on-demand.

DECOMPOSITION RATIONALE — P1: #318/#319 triage -> ai-council rollout (staged
draft docs/audits/2026-07-12-technical-night-rollout-ai-council.md) -> corp
rollout (ADR-41 chat, staged draft + D4 STALENESS dimension). P2: audit-corpus
sequential review (night leg produces the list, operator rules verbs) +
nightly-routine codification (workflow: night batch -> verdict-sheet -> morning
prompt). P3: C4 -> Mermaid/ToC ruling -> #322 dashboards. P4: EPIC H incl. the
Codex variant-routing pilot (now unblocked) -> #317 (post-D1) -> #270 ->
grooming. Do NOT redo: the boundary matrix, the marker design, v1.3.0, the
night findings — all are canon inputs now.

OFF-REPO CONTEXT — Codex: config pin was stale (gpt-5.5) while 5.6
sol/terra/luna are live in the CLI — operator verified in the /model selector,
pin corrected to gpt-5.6-sol; the arc's night reviews ran on 5.5 (findings
stand, re-review on 5.6 optional). LESSONS entry owed/extended: premise
verification must target the AUTHORITATIVE surface (config = default, selector
= availability); this failed twice in one chain (architect stale memory, then
CC's config-only read accepted without the selector check). Token-budget
pressure is real and drives the Codex-producer strategy. win-tooling is
registered (operator's own arc, c198cf1) — onboarding DEFERRED until after
ai-council + corp. The plan-vs-execution review doc (2026-07-11) is committed
alongside the -2 bundle as the incoming session's comparison baseline.
