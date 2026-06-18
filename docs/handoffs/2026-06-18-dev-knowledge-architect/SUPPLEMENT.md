# Architect strategic supplement — 2026-06-18-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-06-18

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
A. **"File-oriented dependency management" as an ADR — author it now, or defer?** The prior
   filled supplement (`…-architect/SUPPLEMENT.md`) directed: *name the paradigm as an ADR, not a
   VISION*. This window made the v2 roadmap **durable** (#179–#183, the new `coherence` group) but
   left the **capstone ADR unbuilt**, so #179–#183 currently read as a loose feature list rather
   than "extending the paradigm." Should authoring that ADR be the next session's first build, and
   what is the **priority order** of the coherence-by-memory failure classes it should enumerate?
B. **Sequencing the two unproven way-of-working items — #184 (demonstrate ADR-87) vs the §7
   reconcile.** ADR-87 (the architect/CC equilibrium contract) is **codified but never exercised
   on a real build** (#184), and the §7 review-command **graduated rule** the prior supplement
   specified (interim → `/code-review high`; final pre-merge 3+ files → `/codex-review`) was
   **not encoded** in PLAYBOOK §7. Is there off-repo intent on which to settle first — and on the
   Codex auth mode (ChatGPT-authed = no extra cost; API-key = bills per token)?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
