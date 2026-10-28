# Architect strategic supplement — 2026-10-28-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-10-28

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
6. **Off-repo context — changed INTENT only.** Intent, priorities and decisions that moved
   this window and are not in the repo. **Not** the operator's interface mechanics — file
   exchange through Downloads, `.md` uploads because a large inline paste arrives empty,
   shipping the exact start command, reports travelling as files. Those are constants, they
   live at `protocols/OPERATOR-INTERFACE.md`, and the incoming bundle's forms card already
   carries them; one of them being wrong is a defect report about that file, not an answer
   here.
7. **Ratified-in-chat register** — terms, rulings, or contracts ratified in this window's
   chats that are NOT yet recorded in the repo, **and interface BEHAVIORS you relied on that
   are not yet named in `protocols/OPERATOR-INTERFACE.md`** — e.g. a copy-ready block
   substituting for a described action, a paste arriving as a `.md` upload rather than inline
   text, reliance on the `PASTE_THIS.md` END sentinel to detect a truncated paste, or a
   Downloads-directory fallback for file exchange. For either kind: the verbatim term/behavior ·
   a one-line definition (or what relying on it looked like) · its intended durable home
   (BACKLOG id / ADR / LESSONS / PLAYBOOK §, or `OPERATOR-INTERFACE.md` for an interface
   behavior). "None" is a valid answer.
8. **Fixed slots (Part A minimum — REFUSED if the pasted answer omits one).** Restate the
   above as five short LABELED LINES, each non-empty (`"none"` is a valid non-empty value; a
   blank line after the label is not). This is the outgoing seat's judgement in a shape the
   next session can scan in five lines without reading the freeform answer above it; Part B
   (WAVE5B-N5 B1, the `seat-release` moment) is what eventually moves them into the boot card
   itself and makes the refusal a harness transaction rather than a re-render check
   (`gen_handoff.assert_supplement_fixed_slots`). The five labels, exactly:

   ```
   Headline: <one line>
   Open threads (with carriers): <thread — who/what carries it, or "none">
   Next authorized action: <the next act this window authorized, or "none">
   Contingencies: <what changes the plan if it happens, or "none">
   Do-not-repeat: <a mistake or dead end this window found, or "none">
   ```
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
<!-- the five Fixed-slot labeled lines (Q8) go anywhere in this region, each on its own line -->
