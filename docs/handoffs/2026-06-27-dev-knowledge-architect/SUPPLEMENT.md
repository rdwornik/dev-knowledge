<!--
  SUPPLEMENT.md — architect strategic supplement (HANDOFF_PROCESS.md §13
  "Architect strategic supplement"). Self-documenting fillable form, interpolated from
  templates/handoff/v5/SUPPLEMENT.md.tmpl for this bundle.

  Lifecycle (see HANDOFF_PROCESS.md §13 "Architect strategic supplement"):
    1. CC writes this file UNCONDITIONALLY for every architect handoff (questions + an
       empty answers section), committed on the handoff branch for durable tracking.
    2. The operator copies the QUESTIONS into the OUTGOING architect chat (the chat that
       did this session's work), pastes that chat's answers below the divider, and tells
       CC `supplement filled`.
    3. CC commits the filled (or deliberately-empty) file; the assembler folds the ANSWERS
       region into the next session's PASTE_THIS — only if non-empty.

  SCOPE (load-bearing): answer ONLY the non-re-derivable strategic *why*. NEVER put repo
  state, methodology, task-state, counts, or SHAs here — those are source-authoritative +
  forced-read (§3/§5). This supplement is ADVISORY; never trusted over the repo. CC NEVER
  fabricates answers — an unanswered supplement is committed EMPTY, never synthesized.
-->

# Architect strategic supplement — 2026-06-27-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-06-27

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
> (this is the defined cold-handoff disposition, not a defect). **This bundle was generated
> COLD (a `/clear`ed session, no outgoing architect) — empty is the expected state here.**

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
<!-- CC-observed, session-specific addenda (off-repo *why* the residual cannot carry): -->
A. **#131↔#215 split rationale** — these two onboarding items were filed separately
   (#131 = the 6-layer install runbook; #215 = onboard *+ verify-it-conformed*). What was
   the original intent behind splitting them, so the start-of-next-session merge-or-split
   decision (RESIDUAL §4.1) is informed rather than relitigated from scratch?
B. **New-keystone steer** — the dependency-management spine is now built (RESIDUAL §3-A).
   Was there an off-repo priority signal pointing the next frontier toward cross-repo
   dissemination (the ai-council onboarding pilot + two-lifelines generalization probe)
   vs the conformance dashboard (#171→#169) vs finishing #218 — or is that genuinely the
   incoming architect's open call?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
