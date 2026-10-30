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

by: Tech-Architect-47 (2026-10-22-dev-knowledge-architect)
date: 2026-10-30
kind: SUPPLEMENT-ANSWERS v2 (final; supersedes the DRAFT v1 of 2026-10-25)
answers: to-browser/QUESTIONS-FOR-OUTGOING-2026-10-28.md Ask 1 (O11)
scope: prose only for what code cannot know (intent, lessons, tensions, open decisions). Every state fact cites its file; CC re-derives it before acting.

# SUPPLEMENT ANSWERS - Tech-Architect-47 (v2)

## 1. Strategic intent
The harness runs its own processes; people only rule. A process is a transition A -> B that an ADR defines and code enforces (PR-1, to-browser/RATIFICATION-2026-10-27-adr4-consolidation.md); order and understanding come before any build (PR-2). E2.2 put the handoff through that loop first (ADR-132, merge b8d7b06b3). The next session takes the next process through the same loop: dispatch, meaning the step between processes. The E2.2 evidence is that work stopped whenever no code fired the next step (L10). Success is measured as hand steps per process and tokens to understand a task (PR-4, to-browser/RATIFICATION-2026-10-27-principles.md), not as features added.

## 2. Tensions weighed
- Cut-time refresh vs landing-time regeneration: landed on cut-time refresh (ADR-132 option H2); landing-time (H4) is the flip-condition fallback if median active cut time exceeds 32 min.
- Parallel tracks vs serial landings: tracks H and G ran in parallel in named worktrees, and landings stayed serial through one integrator. That worked: 4 landings, 0 conflicts (to-browser/SESSION-integrator-E2.2-close-2026-10-27.md).
- Review cost vs defect catch: two reviewers on the final tip forced repairs (docs-boot 2, bind-handoff 1), but caught real bugs, e.g. an inverted `_branch_is_merged` and the LEDGER line the cut dirties (to-browser/SESSION-bind-handoff.md item 10). Kept.
- Plan prose vs code: GO carriers are still prose plan files (PLAN, AMEND). Accepted only as pure-intent prose (PR-3). A ruling issued after a contract froze reached a lane only by message, and the lane rightly refused it (L12).
- Token cost is not a goal: lanes reported totals with and without cache reads; the cap is record-only (to-cc/PLAN-E2-2-PHASE3-2026-10-27.md, other forks).

## 3. Considered and rejected (do not relitigate)
- Handoff options H0, H1 (prose runbook), H3, H5: rejected in ADR-132 (docs/decisions/ADR-132-*.md).
- Closing backlog rows by age plus no holder alone: rejected; P0/P1, live dependency and NEXT-frontier rows are protected (GO-1 amended, to-cc/PLAN-E2-2-PHASE3-2026-10-27.md).
- Closing INDEX requests because a later digest cites them: rejected; all 26 closed as OBSOLETE by one class rule (to-browser/SESSION-transport-g3.md).
- Pruning tests without coverage edges: rejected; 0 removed this batch (GO-2).
- Setting CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP: rejected; run tests one file per invocation and leave the full file to CI.
- Models picking backlog ids (S-ID): withdrawn; ids come only from an operator grant through scripts/id_allocator.py.
- Hand-written LEDGER: rejected; scripts/gen_ledger.py is its only writer (ecosystem/transport-registry.yaml).

## 4. Open questions (owner: operator unless named)
- C1: may the browser seat write HANDOFF_BOOT.md into the Project from the cut's sha-matched copy and verify by read-back? Not yet permitted, so D4 step 12 stays the operator's (to-browser/RATIFICATION-2026-10-28.md, paste 1 last line).
- The ADR-132 LEDGER mask (bind-handoff TODAY-GLUE 3): keep the one-line mask as an ADR amendment (TA-47 recommends), or make gen_ledger ignore cut-owned paths.
- Step 1 (ratify) can never appear in `stops:` (bind-handoff TODAY-GLUE 4): TA-47 recommends counting the ratification_present refusal record as the step-1 stop and keeping the row blocking.
- Should `--cut` refuse every primary-checkout cut, not only a cut on main (TODAY-GLUE 10)? TA-47 recommends yes: a cut runs only in its own worktree.
- Queue-only scope (PLAYBOOK:2219, :2900, HANDOFF_BOOT:207): TA-47 recommends option A, i.e. queue-only covers batch lanes, `dispatch.py launch` stays documented as the primitive the queue calls, and the PLAYBOOK says so.
- The Claude Code advisor tool (claude-opus-5-5) is declared to every lane by the user-level config, but no lane called it (to-browser/DIGEST-E2-2-SESSION-CLOSE-2026-10-27.md TODAY-GLUE). TA-47 recommends lanes launch with it disallowed, so R178 holds by mechanism.
- 461 KEEP rows map to none of the four ADRs (to-browser/DIGEST-BACKLOG-TRIAGE-2026-10-27.md section 8).

## 5. Decomposition rationale
E2.2 ran two tracks. H (handoff) was the critical path: docs-boot, census, /decide, ratification, bind-handoff, cut. G (hygiene: backlog, transport, archive, STEP 0) ran beside it in its own worktrees, because none of it depends on the handoff. Every item is O1-O16 in to-browser/DIGEST-E2-2-SESSION-CLOSE-2026-10-27.md.
Do NOT redo or re-decide: ADR-132; GO-1..GO-4 and their amendments; QC-D3 (nine browser-writable kinds, now in protocols/OPERATOR-INTERFACE.md section 1); K1-STANDING; the census baseline (16 hand steps); STEP 0 = NO (a green conductor run is a verdict, conductor.yml:286-301).

## 6. Off-repo context - changed intent only
- The operator wants the harness to do its own handoff out of its own process, measured AS-IS -> TO-BE. This is not hand work by the architect (to-cc/AMEND-1-PLAN-E2-2-SESSION-CLOSE-2026-10-27.md).
- A HANDOFF_BOOT change must be one ordinary landing. The handoff process historically took far too long to update; that was the problem fixed this window.
- Principles PR-1..PR-5, PO-B..PO-E, PO-T, PO-H and DC-1 live only on the transport (to-browser/RATIFICATION-2026-10-27-principles.md, to-browser/RATIFICATION-2026-10-27-adr4-consolidation.md). They are not yet in protocols/STANDING_RULINGS.md (K10 assigns R-numbers at landing).

## 7. Ratified-in-chat register
- "the paste is the ratification": an operator paste that names a PROPOSED plan/AMEND file ratifies that file as written · relied on for to-browser/RATIFICATION-2026-10-28.md · home: protocols/OPERATOR-INTERFACE.md.
- The browser seat writes its own decision files straight to to-cc/ through the Drive connector. The operator does not place them, despite what QUESTIONS-FOR-OUTGOING-2026-10-28 "How to answer" says · home: OPERATOR-INTERFACE.md.
- The operator relays CC status as an attached .txt of terminal output plus the background-agent list, and the browser treats it as relay, not witness: transport files decide · home: OPERATOR-INTERFACE.md.
- The operator's chat arrives dictated and garbled; the browser states its reading in one line before acting on it · home: OPERATOR-INTERFACE.md.
- STALE-60d with protections (a) P0/P1, (b) live depends-on target, (c) NEXT frontier: the backlog closure class rule · home: BACKLOG process row (PLAN-NEXT item 4).

## 8. Fixed slots

Headline: The handoff is now a declared, coded process (ADR-132 --cut: 16 hand steps -> 3 sanctioned stops plus 5 seat glue steps); the next bottleneck is that nothing fires the next step between processes.
Open threads (with carriers): C1 Project write - operator; LEDGER mask, ratify stop, primary-checkout cut, queue-only scope, advisor disallow - operator, recommendations in this file section 4; the 5 cut glue steps - to-cc/PLAN-NEXT-2026-10-28.md item 2; dispatch process loop - PLAN-NEXT item 1.
Next authorized action: none beyond finishing this cut (fold, assemble, --land); the next batch starts from to-cc/PLAN-NEXT-2026-10-28.md after the operator's GO.
Contingencies: if median active cut time over the next 3 cuts exceeds 32 min, reconsider landing-time regeneration (ADR-132 flip-condition); if the laptop reaps again, move test-heavy lanes to Codespace before tuning the laptop.
Do-not-repeat: an orchestrator that ends its turn between steps leaves REFUSED lanes and next lanes unfired for hours; architect numbers stated from memory ("11 of 12").

## Lessons (L1-L9 from v1, updated; L10-L15 new in E2.2; each must become code)
L1 Built-but-never-run is the root failure. -> usage census per batch-close digest. E2.2: `--cut` was used for real on its first day.
L2 Prose disabled working code. -> dependencies only in the queue; templates checked against code.
L3 A mechanism works only when code triggers it. E2.2 proved it three times (L10).
L4 Host RAM is the laptop's hard limit. E2.2: test runs were reaped mid-run (docs-boot-repair-2), and E2.2 used no Codespace at all. -> Codespace for test-heavy lanes.
L5 Gates are right but noisy (lane-added files are red by construction). Unchanged.
L6 Removal needs the consumer graph first. Held: the bind-handoff removal inventory found readers for all 5 candidates.
L7 Naming and model rows confused. -> fixed (seat-cycle-fix); seat-orchestrator -> lane-head rename still owed.
L8 Browser seat errors (E2.1): hand-written LEDGER, invented numbers, reactive patching, recommending before reading, overstating "harness on".
L9 The TA-46 -> TA-47 hand-over cost >= 203 questions; KPI for the intake: escaped questions 0, rounds 1.
L10 The orchestrator is a session, not a process. docs-boot sat REFUSED about 6 h (20:02 -> 01:50); H-4 was not queued after docs-boot merged; a repair handback file was missed by watchers keyed on SESSION-<slug>.md. -> REFUSED -> repair re-fire and MERGED -> next lane in code (PLAN-NEXT item 1).
L11 TA-47's closure rules were too weak: age-based STALE would have closed 3 of the 5 NEXT P1 rows, and protections (a)-(c) still missed a body saying STAYS OPEN ([#419]). -> `gen_task_tree --close-row` refuses such a row.
L12 A ruling issued after a contract freezes has no carrier the lane can verify (AMEND-2 R3). -> rulings enter only through the lane's contract file.
L13 Two reviewers on the final tip catch real defects. Keep, and make "any commit after review restarts review" a gate (it already is in subst_gate on handback).
L14 Copilot gpt-6-luna as RED author was never used in E2.2 lanes (bind-handoff MODELS: red-author NOT run). The isolation ruling is prose until a contract check refuses a lane whose RED author equals its implementer.
L15 Browser seat errors (E2.2): the "11 of 12" figure from memory (withdrawn, AMEND-2 C5); a decision matrix too abstract for the operator to use; a too-weak STALE rule; an AMEND written without its carried-by line (p11_carriage FAIL).

=== END OF SUPPLEMENT-ANSWERS v2 ===
