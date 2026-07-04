<!--
  SUPPLEMENT.md — architect strategic supplement (HANDOFF_PROCESS.md §13
  "Architect strategic supplement"). Generated from templates/handoff/v5/SUPPLEMENT.md.tmpl
  for this bundle. Self-documenting fillable form.

  Lifecycle: CC writes this UNCONDITIONALLY (empty), commits it on the handoff branch;
  the operator pastes the QUESTIONS to the OUTGOING architect chat, pastes answers below
  the divider, says `supplement filled`; CC commits verbatim + re-runs assemble_paste.py,
  which folds the ANSWERS region into the next PASTE_THIS — only if non-empty.

  SCOPE (load-bearing): answer ONLY the non-re-derivable strategic *why*. NEVER repo
  state / methodology / task-state / counts / SHAs (those are source-authoritative +
  forced-read, §3/§5). Advisory, never teeth, never fabricated — unanswered = committed EMPTY.
-->

# Architect strategic supplement — 2026-07-04-dev-knowledge-architect-2

Repo: dev-knowledge · Mode: architect · Date: 2026-07-04

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

<!-- CC-observed addenda (session-specific; §13 permits 1–2) -->
A. **Slice A acceptance bar** — what is your accept/iterate criterion for the sandbox
   spawn+isolation foundation before Slice B builds on it? (The Codex 2 CRIT + 2 HIGH are
   fixed; is the isolation contract — `CLAUDE_CONFIG_DIR`-hooks, system-temp teardown,
   protected env keys, exit-gating — the seam you want, or does the boundary move?)
B. **Sequencing the deferred handoff-spec arc vs the sandbox** — do you want the
   HANDOFF_PROCESS §5/§13 → option-b reconciliation + `5.3→5.4` bump folded into the
   ARCHITECTURE-currency pass BEFORE Slice B (so the corpus is settled), or after (so
   Slice B momentum isn't interrupted)? It collides with sandbox-owned `ARCHITECTURE.md`.

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
