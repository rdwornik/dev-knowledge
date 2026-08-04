# Architect strategic supplement — 2026-08-04-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-04

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

**Q1 Strategic intent.** Make *verification of mechanisms* the standing way of working, not
this window's discovery: every organ gets its own test (the T8 pattern), every emitted
contract gets pre-flight ([#483]), every review gets artifact-or-RED ([#480] is the open
mechanism gap, now evidenced 12-for-12). Second intent: pay the flow debt — this window
closed 3 / filed 5; open the next window by closing the small residue ([#481] [#482] [#483]
enforcement question) before filing anything new.

**Q2 Tensions weighed.** Mechanism vs vigilance → mechanism, every time it was tested (1200
ceiling, ratchet baseline, gotcha-vs-write-helper). ADR-first vs code-first for governance
fixes → ADR-first, with the caution that judgment ceremony must not multiply: one
adjudication, then build — the operator correctly called out a stall when dual derivation +
ratification gates stacked. Honest filing vs §F optics → honest filing; the flow rule
reported RED and the verdict stands. Row-vs-record → the row carries a pointer.

**Q3 Considered + rejected — do not relitigate.** Desired-state as a new persisted file
(barred, ADR-109 §2/§9, twice); anchored-regex over ADR prose and its D/E variants (killed in
the [#472] matrix); raising `_BACKLOG_GROSS_CHARS` for one row; raising the silent-rule
ratchet baseline for one word; REMOVE for the `.claude/**` glob (REPAIR ruled, [#482]);
renaming `organ_id` inside a repoint arc (own row, [#481]); honoring `stop_hook_active` on a
hard Stop leg (the whole hard-Stop model was retired instead, ADR-85 amendment); re-invoking
sol for build review (derivations are spent on judgment, terra reviews builds).

**Q4 Open questions.** [#480] wrapper-tally mechanism — highest-value open item, 12/12
evidence; [#481] rename scope; [#482] glob-engine switch + governed-set pin; [#483] gate
wiring (adoption-first was deliberate); [#485] LF write helper; [#484]/ADR-106 (~1 window,
deferred by name); [#383] five surfaces remain and **clause (c) of the caches wave awaits the
operator's read of the wave record §5.3**; B-2 investigation (why the scheduled task is
silent 10 days); flow debt −2; 139 closure proposals + 2 fleet issues parked from
/review-closures.

**Q5 Decomposition rationale — do not redo.** [#383] proceeds per SURFACE, named, never
numbered ("wave 3" was an alias; retired). The ADR-85 model is SETTLED: obligation domain =
integration onto main, hard organ at pre-push, Stop advisory, backstop in ALL_CHECKS,
floor 24882f8cc in the ADR — none of it re-opens without new evidence. §F is a flow rule
with seal-SHA boundaries — not a count target. Retire-not-delete everywhere. One contract =
one deliverable.

**Q6 Off-repo context.** Operator's standing methodology: everything flows through CC
prompts (no manual pastes into other tools); Codex utilization is mandatory (terra default
for review, sol for independent derivations of foundational artifacts — spent once per
judgment); library-first (now codified, ARC 1d). Eleven premise errors this window — nine
architect, two CC — every one caught by a mechanism or downstream review, none by the author;
that measurement is [#483]'s reason to exist. Mid-window machine crash recovered with zero
loss — commit-and-STOP validated in production. Operator delegated the §F / B-2 / B-3 / B-4 /
ADR-ratification rulings to the architect this window and ratified the outcomes.

**Q7 Ratified-in-chat register.** After ARC 1 lands (c) and (d): **"last-run-wins"** —
[#465] closure semantics, recorded in JOURNAL:951 ruling + closure, home already reached;
**"clause (c) operator-read"** — the caches-wave Done-when's third clause is deliberately
non-delegable, home = the wave record (present, awaiting the read). Everything else ruled
this window is already in its durable home. Otherwise: none.
