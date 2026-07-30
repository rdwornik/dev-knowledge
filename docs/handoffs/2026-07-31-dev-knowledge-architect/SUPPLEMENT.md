# Architect strategic supplement — 2026-07-31-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-29

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

=== ANSWERS === (outgoing browser seat, 2026-07-30, window closed at 470b24fa)

1. STRATEGIC INTENT — Finish the prose→mechanism migration this window started: the next
session converts the ADOPTED §B(b) direction into a working mechanism (one-round-trip boot)
via the [#446] build consuming the sol draft. Way-of-working goal: RULE FIRST, BUILD SECOND —
the draft's 7 OPEN questions are rulings, not implementation details; settle them before any
code, then build TDD-style (ex-ante witnesses, the pattern that held 3/3 arcs this window).
The v6 bump lands WITH the build, never before (the 5.7 precedent, kept honest twice now).

2. TENSIONS WEIGHED — (a) U3 pure-A5 vs default+exception: landed the scoped exception —
pure A5 is also collision-free, but the exception preserves the one witnessed remedy
(adr∥ratchet) at zero cost and keeps condition-2 truthful. (b) v5.8 vs v6: landed v6 CUT with
the bump riding [#446] — the label follows the receiver-must-do test, and stamping before the
mechanism exists would be a lie. (c) frontier artifact vs prose: landed prose (RESIDUAL §4) —
a standing frontier file is the v4 hand-maintained-surface disease §13 names. (d) self-induced
doc_rot: trim, not disposition — dispositions are for states we won't fix, not fresh debt.

3. CONSIDERED + REJECTED — do not relitigate: draining must/never tokens elsewhere to dodge
the ratchet raise (out-of-plan edits, meaning-change risk — the raise IS the designed path);
reconciled_with on the orientation snapshot (a stale edge is worse than none — dated snapshot
is definitionally uncoupled); U6(b) standing closure delegation (per-batch operator words keep
closures trustworthy at the cost of one sentence per session); frontier as intake-section or
new audit (folder-line violation / new-audit ban); in-place edits to the immutable
ratification record (amendment marker is the sanctioned path); [#382] pull-forward (declined —
#446 has a spec in hand and completes W-D).

4. OPEN QUESTIONS — (a) the sol draft's 7 OPEN items, in the draft's order — the build's
FIRST rulings (command name · P0 locators/assertions · P3 comparison+PASS · the HANDOFF_BOOT
byte budget number · RM-8 targets · main() types/CLI · the [#421] tokenizer absorption test).
(b) The 08-26 cluster split — FIRST architect call when 08-26 planning opens; the
§3.2-vs-[#364]-4(a) cap conflict is that planning's ENTRY GATE (1597 ruled-but-never-landed vs
4(a) leave-unchanged; live code 1200). (c) duplicate intake-id 14 (schema-integrity, deferred).
(d) does an ARCHIVED snapshot keep a live disposition — the intake-21 edge does not self-clear;
08-26 decides. (e) BACKLOG-advisory closure polarity (see Q7c — await a second instance).
(f) [#441]'s ADR-61 one-launch-test reconciliation leg, still unrecorded.

5. DECOMPOSITION RATIONALE — [#446] first because the spec exists, W-D completion unlocks the
entire #382→#383→#385 chain, and the 7 rulings are cheap while context is warm. Do NOT redo or
re-decide: any intake-#18 verdict (ledger is complete, A1–A11 + U1 + U5 + riders); the U3
canonical statement wording; baseline 441; the RULING-W execution (all three repos at 08-26,
corp has both .vscode files + the gitignore negation); the closure batch ([#421] stays open BY
#446's own scope; [#433] standing §6.2; [#445] global-infra); ARCHITECTURE.md (delta-checked
07-28, deliberately untouched since — do not re-open without a forcing delta).

6. OFF-REPO CONTEXT — Operator words this window, all executed: #435 close · U6(b) declined ·
core-invariants #5 EXECUTED in C:\Users\1028120\.claude\rules\core-invariants.md (file is
untracked — the amendment marker + JOURNAL 2026-07-30 (c) ARE the evidence trail) · #382
pull-forward declined. Operating precedent proven twice and endorsed: the AUTHORIZED
INTEGRATION ACT — operator GO embedded verbatim in the prompt licenses CC to run the merge+push
as the operator's act (used for the ratchet-raise merge and the final wrap). Browser-side
session plans (v1–v3) live outside the repo and are superseded by the repo artifacts — no
action owed. Cloud night lane unchanged: UNVERIFIED-UNTIL-LOCAL, rider U6(a) trigger intact.

7. RATIFIED-IN-CHAT REGISTER (capture-only, transcription debt): (a) "GREEN-on-branch vs
GREEN-on-main" — mandatory honesty split in close-out reporting when witnesses need unmerged
branches; home: PLAYBOOK Ch8 (close-out reporting) or LESSONS. (b) "authorized integration
act" — operator GO embedded in a prompt authorizes CC to execute merge+push as the operator's
serial-gate act, conditions quoted verbatim in the prompt; home: PLAYBOOK Ch4 + HANDOFF_PROCESS
§13 boundary note. (c) "BACKLOG-advisory closure-polarity false negative" — the session-end
advisory keys on added/modified markers, but a flipped-host closure is a DELETION from the
generated file; one instance witnessed 2026-07-30, second instance promotes it onto the [#447]
family row; home: [#447] (on promotion) or LESSONS.
