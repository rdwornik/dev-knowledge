# Architect strategic supplement — 2026-07-21-ai-council-architect

Repo: ai-council · Mode: architect · Date: 2026-07-21

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

A. **The spike teardown — deliberate discard, or an unnoticed gap?** The teardown entry *named
   the risk in writing* ("cherry-pick … to main if it should survive worktree teardown"), and the
   cherry-picks that followed carried the JOURNAL prose but **not** `spike/FINDINGS.md` or
   `spike/evidence.py`. Was letting the evidence go a **considered call** (conclusions are enough,
   the spike was throwaway by design) — or did the prose-only cherry-pick simply not register as a
   partial mitigation? This decides whether `RESIDUAL.md` §1's flag is a *recovery task* or a
   *closed decision the next session should stop re-opening*. Answer even if the answer is "I
   didn't notice."

B. **`[#81]`'s done-when vs the F8 "under-match toward the loud failure" doctrine.** As written the
   two cannot both hold: the doctrine prefers an honestly-empty result over a plausibly-wrong one,
   while `[#81]`'s done-when requires that a fenced options list is *not* silently emptied. Was the
   done-when authored **before** the F8 doctrine was ruled (so it is simply stale and should be
   amended), or did you intend a reconciliation the ticket text does not capture — e.g. fence-aware
   extraction that *detects* and *reports* the fenced case rather than silently returning either
   result? This is `RESIDUAL.md` §4's item (1) and the next session's first ruling.

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
