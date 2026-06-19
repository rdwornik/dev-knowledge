# Architect strategic supplement — 2026-06-19-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-06-19

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
A. **ADR-88 ratification path — Council or operator-ratify, and what does it gate?** ADR-88
   (*file-oriented dependency management*) was **authored this window (Proposed)** — the capstone the
   2026-06-18 supplement directed. Its FC4 deterministic trigger (#140 `doc_rot`) already shipped.
   Does ratification go through AI Council, or operator-ratify (the ADR-82/#149 precedent)? And does
   anything (e.g. treating #179–#183 as "doctrine" vs "proposal") wait on it? (RESIDUAL §4 Q1.)
B. **The `ship-gate` RED disposition — A/B/C.** Two 2026-06-19 wrap commits (`3a894ee`, `d0f9ead`)
   landed direct-on-`main` (already pushed; un-FF off the table), so ship-gate is RED. Resolution is a
   *methodology* call: (A) disposition the journal/chore-wrap-direct pattern, (B) operator-accept the
   one-off, or (C) tighten the wrap workflow so even the journal-wrap branches. Which — and does it
   change how strictly core-invariant #5 binds a wrap? (RESIDUAL §1 / §4 Q4.)

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
