# Architect strategic supplement — 2026-10-17-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-10-17

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

# Supplement answers — window Tech-Architect-45 (2026-10-14 … 2026-10-17)

## 1. Your one goal

**ADOPTION, not construction.** Read `to-cc/PLAN-HARNESS-2026-10-17.md` (status: MASTER PLAN).

**Step 0 is the decision-to-implementation audit:** `to-cc/DECLARE-DECISION-ADOPTION-AUDIT-2026-10-16.md`, R125. Start it in your first turn after the boot. Do not design anything new before its counts are in.

## 2. What is TRUE on main (witnessed; read the commits, not this prose)

| Commit | What |
|---|---|
| 9fa73898 | BU 6/6 closed |
| e1fd5543 | **the first lane run end to end in a Codespace** (`[#1015]`, 3.6 core-h) |
| f8ca281c | 38 digests archived + 50 defect rows `[#1569]`–`[#1618]` |
| eda714a4 | rows N1–N5 |
| 2767501b | **start-up context −7,860 tokens/turn** |
| 8e8ef452 | **merges judged on Linux** (ADR-127 am. 2) |
| 0bea1ff6 | **Copilot staged-input adapter, Grok pinned with `-m`, VENDOR-FAIL** |
| night-retire, if its land report says DONE | `/handoff-verify` retired; the templates self-launch Cycle successors + foreground waits |

**The process matrix (night PART 9):** 90 processes = 57 WORK / 12 BROKEN / 8 DEAD / 6 DECLARED-ONLY / 6 unrun / 1 duplicate.

## 3. The rules you inherit (RATIFICATION-2026-10-17, R121–R128)

**Built but unused = a failure.**
- A lane is done only with a real-use witness.
- No silent vendor substitution.
- A night run waits on its dependencies and alarms on END-EARLY.
- Lands are judged on Linux.
- No new decision before the adoption audit.

## 4. Do NOT repeat this seat's failures (each cost the operator hours or budget)

1. **It answered from memory instead of re-reading the plan of record**: it re-proposed the decided Conductor E (v209, withdrawn).
2. **It said "I don't know" about capabilities already witnessed on the transport**: the seat self-launch, 09-29.
3. **It wrote a night order whose dependencies became SKIP and END**: 8 idle hours (fixed by R122). **It never read the night report that sat on the transport while it was in session.**
4. **It reported "built" as progress.**
5. **It left the RAM diagnosis of 2026-10-03 uncarried** while the reaper killed six steps.
6. **It minted 19 LEDGER files.**
7. **It ordered a queue with a false dependency:** the integrator sat idle.
8. **It accepted R116's withdrawal of Linux-first on a cost-only premise.**

**Use the transport INDEX and the generated status, not Drive search.** Read every report a session produced before speaking about it.

## 5. Known open items (all carried as rows or files)

- `[#1350]` known-reds expiry 2026-10-19; the night-retire land verifies it.
- `[#1015]` stays open (`plan_lint` at pre-launch, A5).
- `[#1536]` close after the `[#1452]` remainder.
- The Linux-only CI witness is not yet observed (A1b).
- The token-cuts r1 receipt line was lost (recorded).
- The census was never run (laptop RAM); run it in a Codespace.
- The operator's pending decisions: RATIFICATION-2026-10-17 "Pending".

## 6. Budget

The operator was at about 80 % of the weekly limit on 2026-10-17; the reset is Mon 15:00.
- Sonnet for execution, Opus only to judge.
- Sessions ≤ 2 h.
- Cost per landed lane: baseline USD 13–16.
