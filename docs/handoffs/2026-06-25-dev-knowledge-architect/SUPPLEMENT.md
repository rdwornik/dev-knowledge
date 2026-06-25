# Architect strategic supplement — 2026-06-25-dev-knowledge-architect

Repo: dev-knowledge · Mode: architect · Date: 2026-06-25

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

A. **Computed-edge keystone (CC-observed).** This window finished the *declared*-edge half
   (#194 built, ADR-88/89 Accepted). The next keystone is the *computed* code↔code edge —
   wiring the proven-but-ungated Pyright reverse-dep oracle into a gate (GAP-1 / #195 /
   ADR-89 OQ3). Is that the priority for the next planning session, or does something
   off-repo outrank it?
B. **Two fresh audits to dispose (CC-observed).** Audit-A (dependency-architecture +
   coverage) and Audit-B (process/trigger/usage) landed report-only. Which of their
   findings do you want built first, and which are decline/defer?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
