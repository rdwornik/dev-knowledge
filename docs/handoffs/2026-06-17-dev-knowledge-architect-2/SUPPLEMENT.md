# Architect strategic supplement — 2026-06-17-dev-knowledge-architect-2

Repo: .dev-knowledge · Mode: architect · Date: 2026-06-17

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
A. **"File-oriented dependency management" as doctrine** — the coherence spine v1 (#172)
   is the *first* mechanism of the reframe you named in the prior bundle's filled supplement.
   Should the paradigm be elaborated as **named doctrine** (an ADR / a VISION or ARCHITECTURE
   thread), or stay an implicit organizing idea? And beyond the v1 single `reconciled_with` edge,
   which **coherence-by-memory failure classes** should it cover next (the priority order)?
B. **Coherence v2 trigger + the `/codex-review` vs `/code-review` reconcile** — v2's
   escape-hatch / deferred-hash / promote-nudge-to-gate decision is firing-rate-gated on
   `logs/coherence-nudge.log`; is there off-repo intent on which way to lean before the data
   accumulates? And the surfaced doc-vs-practice drift — PLAYBOOK §7 names `/codex-review` as the
   canonical pre-merge gate while the coherence feature's practice used `/code-review high` — which
   is canonical going forward?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
