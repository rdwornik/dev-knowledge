# Architect strategic supplement — 2026-10-02-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-10-02

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
carried-by: OPEN
lands-via: CC transcribes these verbatim into the 2026-10-02 bundle's SUPPLEMENT.md ANSWERS region ("supplement filled")
date: 2026-10-02
from: 2026-09-28-dev-knowledge-architect (outgoing browser seat, SEQ 1) — authored by the seat, per the SUPPLEMENT authorship rule
kind: ANSWER — handoff cut supplement, 2026-10-02

# SUPPLEMENT ANSWERS — 2026-10-02 architect cut

## 1. Strategic intent

**Build the deterministic outer harness, before any feature.** Every way-of-working rule becomes code that refuses, proven by an outcome test (R45). This includes:
- the outcome test first;
- stop-the-line;
- WIP limit 1;
- failures surfaced by code;
- task IDs everywhere;
- isolated stage agents and an evaluator;
- a constraint registry;
- a gate registry with cost and catches;
- automatic hygiene;
- one command that lists the whole harness.

Each window states ONE SMART goal at boot and reports outcomes, never activity. Feature lanes stay frozen until the process engine's first build is GREEN (R46.4). The order is in `to-browser/MECHANISMS-NO-RECURRENCE-2026-10-02.md`.

## 2. Tensions weighed

- **Speed vs verification.** Independent verification stays: the integrator runs the outcome test itself, and an isolated reviewer looks at every change. It caught a stub, a false "done", a regression and 2 P1s. Speed comes from cutting the gate tax — gates with zero catches, measured under R49 — not from cutting checks.
- **Whole-repository gating vs handoff-relevant gating.** Landed in ADR-129: the cut gates on a named 12-organ set (end-to-end test 96.64 s), and the whole-repo verdict is reported, not blocking.
- **Stopgap vs systemic.** Systemic only (R38). Stopgaps were withdrawn (R37.2).
- **The browser as process bus vs CC-led.** CC leads and challenges every order (R41). The browser rules, and accepts outcomes on test evidence (R47.6).

## 3. Considered and rejected

- Cutting with the old 57-organ preflight, or with a detached-process workaround — R44 built first.
- Dispositioning hard-fails to unblock a cut. No mechanism exists for it; the R42 v1 assumption was wrong.
- The merge-path stopgap (R37.2, withdrawn).
- Building N5-9 (the scheduler) before the process-engine decision (held).
- From the tools review: LiteLLM (a PyPI credential-stealer incident), RTK (+7.6 % cost), Caveman's 65 % claim (8.5 % measured).
- Treating a lane's own report, or the seat's reading, as evidence.

## 4. Open questions

- **The ratification packet** (`DIGEST-RATIFY-PACKET-2026-09-29.md`): process engine, self-maintaining repo, merge path, Copilot.
- **The R50 retro and debate** (running): `RETRO-HANDOFF-2026-10-02.md` and `PROPOSAL-ADR-NO-RECURRENCE-2026-10-02.md`.
- **M07**, the A/B instrument.
- **ADR-121** (SQLite).
- **#863:** the 14-day hook extension, by 10-07.
- **rclone OAuth** re-mint, by 10-03.
- **58 owed items** not yet filed as rows.
- **Redo bundles** in `to-browser/archive/2026-10-01/`: L1, L4, L8, L10, L5, N5-8.

## 5. Decomposition rationale

The order is visibility (the one-command table, R48.5/R49) → cheap high-leverage gates (R45, R46.6, R47.3) → dispatcher control (R46.1–3) → the process engine (R47, R48) → features.

The reason: features built on prose-driven, self-reviewing lanes failed. The lane review found 1 delivered, 9 partial, 7 theatre and 5 not built.

**Do not redo:**
- the handoff redesign (ADR-129, merged f971562e);
- the evidence digests — value audit, lane review, operator questions, AJ all-modules;
- rulings R44–R51.

## 6. Off-repo context — changed intent only

- The operator measures outcomes, not activity: SMART goals, measured.
- No temporary fixes.
- CC-led, with isolated evaluation.
- The browser verifies; it does not read-and-ratify.
- Zero trust in seat claims without mechanically extracted evidence.
- Feature freeze until the foundation works.

## 7. Ratified-in-chat register

**Rulings.**
- R29–R51 live only in transport files: `RATIFICATION-2026-09-29.md` v12, `-09-30.md` v2, `-10-01.md` v6, `-10-02.md`. `STANDING_RULINGS.md` holds only up to R34. Durable home: `protocols/STANDING_RULINGS.md`, via the next rulings lane.
- `ARCHITECT-OPERATING-GUIDE-2026-10-01.md`. Durable home: `protocols/HANDOFF_BOOT.md`.
- `MECHANISMS-NO-RECURRENCE-2026-10-02.md`. Durable home: the ADR from the R50 proposal.

**Interface behaviours relied on.**
- **Exact session addressing.** The seat names the exact session title shown in the operator's agents list for every paste, one block per session.
- **The browser reads and writes the Drive transport directly.**

Durable home for both: `protocols/OPERATOR-INTERFACE.md`.

## 8. Fixed slots

```
Headline: Handoff redesign (ADR-129) merged and proven; the window's lesson is that rules must become refusing code with outcome tests before any feature work.
Open threads (with carriers): ratification packet + R50 no-recurrence proposal — next seat; retro+debate — running CC session; 58 owed items — G1 filing lane; redo bundles — to-browser/archive/2026-10-01/
Next authorized action: ratify the no-recurrence proposal and the process engine, then build MECHANISMS-NO-RECURRENCE step 1 (one-command harness table with gate cost and catches)
Contingencies: if the R50 proposal disagrees with the mechanism map, the proposal wins after ratification; if any preflight row fails at the next cut, the trial cut at batch close (ADR-129) is the first thing to check
Do-not-repeat: declaring work done from a lane's report or a seat's reading without an independently run outcome test
```
