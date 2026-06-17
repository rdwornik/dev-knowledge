# Architect strategic supplement — 2026-06-17-dev-knowledge-architect

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
>
> **This bundle is the cold case.** This is a fresh CC session — the v5.2 arc it hands off
> was done in a *prior* session (see `RESIDUAL.md` provenance + §2), so there is no outgoing
> browser holding the deliberation. ANSWERS is left empty by design — the structural close,
> not a missing deliverable. (To capture this session's strategic *why* anyway, route the
> QUESTIONS to a chat that still holds the v5.2 deliberation and say `supplement filled`.)

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
A. **The hybrid handoff is shipped + hardened (v5.2) but the *value* is STILL un-dogfooded.**
   v5.1 answered the design question; v5.2 closed the cold-handoff gap (always-generated
   fillable file + defined cold disposition + ANSWERS-only fold). But no supplement has ever
   been filled with *real answers* and folded into a live `PASTE_THIS`. Is the value considered
   proven now that the mechanism is shipped + hardened, or is the first real fill-and-fold run
   still owed? (#159 — the only-remaining clause; this handoff is again cold.)
B. **PLAYBOOK Move 2 — maintainability, not parallelism (Council-bound).** The structural
   split → thin `§N`-index + per-section modules is justified on maintainability (~84k
   tokens, ~3.5× the read-cap, frequently edited), not parallelism. The `§N`-index design
   is a genuine fork: the §1–§19 spine is the consumer API (ESSENTIALS / CLAUDE.md reference
   by §N), so the split must preserve §N addressability. Still the priority, and does the
   `§N`-index approach hold? (#39 / the playbook serialize-group.)

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
