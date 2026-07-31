# Architect strategic supplement — 2026-08-01-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-01

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
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo: the verbatim term · a one-line definition ·
   its intended durable home (BACKLOG id / ADR / LESSONS / PLAYBOOK §). "None" is a valid
   answer.
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

1. STRATEGIC INTENT. Execution-first holds: one arc, and it is [#383] wave 1 — discharge ADR-109 §4 (a SECOND governed surface, same engine pattern, committed round-trip proof; cheapest candidate docs/intake/*.md). Way-of-working lesson to institutionalize: value that does not land on main does not exist — a FAIL sat unread on a branch for 46 days and a durable-record leg died for 15 days unnoticed. Prefer land-and-triage over write-and-forget in every lane you touch.
2. TENSIONS WEIGHED. Doc-level status vs partial ratification → promotion pattern (ADR-108/109), never flip-and-over-claim. Declare-now vs wait-for-generality → declared-NOT-general with a checkable pending clause (§4). Preserve vs delete on immutable records → preserve-then-delete, never delete unread. Speed vs verification → the push-before-verdict miss; the LESSONS line is binding.
3. CONSIDERED + REJECTED (do not relitigate). Second-viewer K1-K5 re-run as #433's residual (dormant replacement procedure, no candidate). CONSUMED flips for intake #16/#22 (partial consumption must not over-claim). networkx in schema v1 ([#383]'s consumer). An ADR-108 §A exception class for the ruling cohort (Done-when re-routed instead). Hand-adding terminal-setup to registry.md ([#462] fixes the census method, not the symptom).
4. OPEN QUESTIONS. [#460] night-lane ruling {OPERATOR-RULED THIS SESSION: recommendation recorded, ruling open}; divergence-report consumer + schedule (ADR-105, sequenced behind [#460]); [#459] codemap source-root ruling; §H builder probe; [#450] per-section ratification; [#449] paste budget.
5. DECOMPOSITION RATIONALE. Four serial waves with frozen ex-ante contracts + operator GO per merge worked end-to-end; keep the shape for [#383]. Do NOT redo: THE-FOUR enumeration + dissolution map, obligation-3 DISCHARGED, the sol adjudication table, boot-destination ruling, [#382] closure evidence.
6. OFF-REPO CONTEXT. Operator priorities: business-value language over process vocabulary; the six window metrics are a standing commitment (report every window; mechanization = [#461]); net backlog delta ran clearly positive this window — verified boot-vs-final count lives in the generation JOURNAL entry, and intake #22 §F ("backlog must shrink") enters at 08-26: the next window should expect that pressure and close more than it files. §C evidence landed (grok caught two load-breaking defects terra missed); §H derivation+review portability witnessed, builder lane untested.
7. RATIFIED-IN-CHAT REGISTER. (a) "push is part of the act it verifies" — LANDED (LESSONS). (b) "value must land on main or it does not exist" — one-line LESSONS candidate, home: LESSONS.md, rides [#460]'s resolution. (c) the six-metric window report — home: [#461] + HANDOFF_PROCESS report convention when mechanized. (d) preserve-then-delete for protected immutable branches — home: git-discipline.md one-liner, next docs arc. None others.
