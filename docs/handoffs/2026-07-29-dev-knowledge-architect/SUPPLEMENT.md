# Architect strategic supplement — 2026-07-29-dev-knowledge-architect

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
<!-- generator may append session-specific CC-observed addenda here as "A./B. ..." -->

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

=== ANSWERS === (outgoing browser seat, 2026-07-29)

Q1 STRATEGIC INTENT: Move from the structure era to the consumption era. This window made
tasks/ the live source, the closure loop real (4 full loops), and the fat-prompt default
doctrine (PLAYBOOK Ch8). The next session's way-of-working goal: pay the ratification debt
— intake #18 per-amendment rulings + the v6 cut decision — so the remaining prose-held
coordination properties (boot round-trip, JOURNAL letters, spec currency) move into
mechanism. After that, the 2026-08-26 cluster executes dispositions at scale, and the
[#382]→[#383]→[#385] chain is the system-implementation era (charter on main; the operator
may pull [#382] build forward of the 08-26 sizing as a priority call).

Q2 TENSIONS WEIGHED: (a) speed vs verification — operator-directed early merge (14bcb1c4)
landed as a NAMED precedent: sanctioned only with the mandatory post-hoc verification leg;
unshortened default stands. (b) delegation vs ADR-70 — closure sweep ran on a BATCH-SCOPED
delegation with dual independent Done-when verdicts; a standing delegation was deliberately
NOT created (would need an ADR-70 amendment — raise at #18 only if the operator wants it).
(c) producer≠reviewer economics on S-size — CC-builds/terra-reviews chosen over
Codex-producer (which would force sol). (d) cloud night lane vs absent user-level gates —
UNVERIFIED-UNTIL-LOCAL contract, branch-only, no merges. (e) cap integrity vs record
richness — compress-precedent used 3×, option 4(a) adopted, build at 08-26.

Q3 CONSIDERED + REJECTED (do not relitigate): PLAYBOOK codification of lesson 7 as-written
(self-blocked by prove-then-codify → LESSONS.md + [#443] chosen) · intake #16 → CONSUMED
(archives a live spec → ACCEPTED+deferred, trigger "[#382] build starts") · in-arc plugin
bump (half-release worse than documented lag → [#444] release act) · indented-code-block
stripping (excluded by design, loud residual test) · [#433] closure (twice, two concordant
NOT-MET on ADR-107 §6.2; sol E5 holds) · night work as a ROUTINE (ADR-105 + unratified
#19 §B → one-off cloud batch under branch-only).

Q4 OPEN QUESTIONS: [#441] condition-2 (pre-allocated JOURNAL letters) vs intake #18 A5
(assign-at-integration) — named fork, decide AT #18 · A7 + A4-item-3 sequence AFTER the
§B(b) one-round-trip-boot ruling · audit row 13 (HANDOFF_PROCESS §14a clarifier) rides the
v6 cut · .vscode mechanism DATE + vehicle ADR ([#387]) — 08-26 · #364 4(a) build shape —
08-26 · governs-vs-contains sub-question inside the #370 disposition · standing closure
delegation (ADR-70 amendment): raised, undecided, operator's call.

Q5 DECOMPOSITION RATIONALE / DO-NOT-REDO: the window ran serial-primary + Codex background
with per-arc frozen A–H contracts — keep that shape (it produced 100% plan execution, zero
process violations). Do NOT redo or re-decide: flip mechanics (live-witnessed) · shared
closure-token core design · #20/#16 rulings · .vscode option (b) · the Ch8 four-condition
launch test · the 12 stale-procedure fixes · everything in Q3. Next task-graph: W-D #18
FIRST (dossier docs/audits/2026-07-29-technical-intake18-ratification-dossier.md is the
decision surface; sol derives the v6 spec ONLY if a cut is ruled) → cross-repo RULING-W arc
(corp .vscode copy + both e1 re-dates; corp GO already given) → 2026-08-26 cluster.

Q6 OFF-REPO CONTEXT: operator escalation calibration (2026-07-28): D3/D4-class decisions
are the ARCHITECT's lane — decide + one-line note; escalate only real forks
(irreversibility, operator drivers, no objectively best option). Operator endorses the
fat-prompt default live ("better quality than singles", running the browser seat on Fable)
— recorded as [#441] evidence. Merge 14bcb1c4 authorship CONFIRMED by the operator in chat.
Night lane environment class: Anthropic cloud VM = no ~/.claude, no Codex — every future
night batch inherits UNVERIFIED-UNTIL-LOCAL. Operator wants night batches to continue —
route the standing version through #19 §B at the #18 session, not ad-hoc.
