# Architect strategic supplement — 2026-07-21-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-21

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

1. STRATEGIC INTENT

The next session must break the plan→execution deadlock. This fleet has spent 3-5 sessions
planning what it cannot ship: assets/ still sits in ai-council, granted-and-planned since
2026-07-19, never executed. That is the way-of-working defect to fix — not another audit, not
another intake, not another ADR. The methodology-management goal (structure, naming, config,
dependencies — not only LLM working-methodology) is sound and the theory is complete. What is
missing is DELIVERY. So the intent is: pick ONE narrow, fully-specified, operator-witnessed
equalization and DRIVE IT TO A DEPLOYED END-STATE the operator sees with his own eyes — assets/
dissolution in ai-council is the obvious first, because it is the smallest granted-but-unexecuted
item and it is the operator's own symbol of the execution failure. Merged is not done; deployed-
and-witnessed is done. If the next session ends with assets/ gone from ai-council and the operator
confirms it, the deadlock is broken and the pattern is proven repeatable. If it ends with another
plan, the way-of-working has failed again and THAT becomes the finding.

The deeper way-of-working question the vision audit forced open: WHY can this fleet plan but not
ship? The likely answer is that the meta-work (audits, intakes, ADRs, census) has been crowding
out the object-work (actually changing consumer repos). The next session should treat "did a
consumer repo visibly change" as its only success metric, and treat any new audit/intake/ADR as
a distraction from that unless it is the direct enabler of the one shipped change.

2. TENSIONS WEIGHED

- PLAN vs SHIP. Weighed hard, landed on SHIP. Every prior session produced excellent artifacts
  and zero consumer-visible change. The bias must invert: no new planning artifact unless it is
  the direct enabler of a shipped change this session.
- BUY vs BUILD (the template engine). Weighed via the vision audit and REVERSED the earlier
  buy-vs-build draft: Copier/cruft are merge-replay engines that fail at heavy declared
  divergence; the field moved to projen's REGENERATE-DON'T-MERGE model, and the hub IS ALREADY
  THAT (generated rosters, floor-hash replica, regen-and-diff gates). Landing: do NOT adopt a
  template engine. Take only Copier's one good idea — a per-consumer template-version scalar as
  the desired-state hash — and keep the existing regenerate machinery. This DELETES a large
  planned workstream rather than building it, which serves intent #1.
- SIEM FRAME vs STATE-DIFF. Landed on state-diff. The fleet is nightly cooperative state-diff,
  not real-time adversarial event-stream. Keep the requirements (they're state-shaped already),
  drop the SIEM frame and its ingestion-machinery pull.
- SCOPE of the first ship: whole-fleet equalization vs one consumer, one surface. Landed on ONE
  (ai-council, assets/). Proving the delivery loop once beats planning the whole matrix again.
- NARROW vs BROAD id-allocation / session-coordination fix. The night proved (n=3) the repo holds
  serialization by discipline not machinery. Weighed building the organ now vs parking it. Landed:
  PARK it as a named ticket, do not let it become the next session's object-work — it is
  infrastructure, and infrastructure is how this fleet has avoided shipping. Fix it AFTER the
  delivery loop is proven once.

3. CONSIDERED + REJECTED (do not relitigate)

- Template engine adoption (Copier/cruft as the fleet engine) — REJECTED by the vision audit on
  evidence: merge-replay fails at this divergence profile; the hub is already regenerate-shaped.
  Keep only the version-pin scalar. Do not re-open "should we adopt Copier".
- Renovate for dependency parity — REJECTED: it needs a hosted platform; on local-disk repos it's
  detect-only. #332's central-constraints-file + per-repo-sync is already the proven pattern.
- SIEM as the architecture frame — REJECTED as the wrong mental model. Do not build event-pipeline
  ingestion.
- Narrowing the ARC-5 rule-fix goal to a bounded slice — REJECTED earlier by the operator (goal is
  ALL rules, prioritised, never lowered). Still stands.
- Auto-deleting from the backlog in a night batch — REJECTED; operator is the strike gate via
  /review-closures. Still stands.
- Another round of audits as the next session's work — REJECTED implicitly by intent #1. AUDITS ARE
  OVER (ARC-5's own banner, twice-violated). The three night audits are the last input; the next
  session consumes them, it does not commission more.
- Hand-close / hand-edit tickets outside the gate to force closures — REJECTED; the cleanup session
  held the line (closure set = 5 not 6 because #215 is gate-unreachable; declined rather than
  hand-forced).

4. OPEN QUESTIONS (unresolved / deliberately deferred)

- FIVE OWED RULINGS (one sentence each, needed before their tickets can close): #339 demotion
  (A2 byte-identical helper leg unbuilt, no owner); #327 demotion (clauses appear met but corp's
  own markers contradict — wording done + markers stale, or genuinely live?); #304+#305 (doc pass
  closes #304; #305 needs a code clause blocked by PreflightError — re-scope?); #262+#295 (policy
  ruling: abandon generator-management for flat layouts?); #215 (permanent gate-invisibility —
  text edit to make it gate-visible, or accept a manual disposition path?).
- THE POLYREPO BET, never decided (vision audit's sharpest hole): zero ADRs weigh monorepo vs
  polyrepo; the 10-20-repo target is asserted, never argued. The only coherent n=1 justification
  is that the workforce is AGENT SESSIONS. This is an afternoon's ADR that re-prices every other
  bet — deferred to its OWN awake session, NOT mixed into the delivery work. Do not build more
  fleet machinery until this is ruled, or you risk building an elegant solution to a problem a
  monorepo would dissolve.
- LITERAL hub-push into consumers (vs the ADR-28 read-only + hub-reports-PRs model) — an open
  ADR-28-amendment question, deferred.
- The session-coordination organ (live-session detection + fleet-scoped id-allocation) — the
  night's proven infrastructure gap; parked as a ticket, deferred until the delivery loop ships
  once.

5. DECOMPOSITION RATIONALE (what NOT to redo)

The task-graph shape is deliberately INVERTED from prior sessions: object-work first, meta-work
only as its enabler. The next session is ONE delivery lane (assets/ dissolution in ai-council to a
witnessed end-state), not a matrix of planning artifacts.

Do NOT redo / re-decide:
- The three night audits are DONE and merged — consume them, do not commission more.
- The cleanup is DONE — backlog is 5 tickets lighter and TRUE; the registry is annotated; four
  audit refutations are recorded (do not resurrect: #361 line-drift is false, #320 was wrong on
  three counts, #244 #130 is a delete-not-swap, #314 companion edit is premature). The audit's
  watch-out #1 orphan list is WRONG both ways (flags #210/#146/#277 which orphan nothing; misses
  #262/#278/#332/#344 which do; #241 is ×6) — use the registry lane's JOURNAL correction, NOT the
  audit, on the next /review-closures.
- The buy-vs-build and SIEM decisions are made (reject the engine, drop the frame) — do not
  re-derive them.
- assets/ dissolution is already GRANTED (operator GO 2026-07-19: relocate to config/ first,
  verify, then delete) — do not re-seek permission, EXECUTE it.
- The equalization scope enumeration exists (living-docs, folder layout, naming, .vscode, .claude
  surface, Python parity) — do not re-enumerate; pull ONE row and ship it.

6. OFF-REPO CONTEXT

- OPERATOR'S CORE FRUSTRATION, stated explicitly: this is the 3rd-5th session where everything is
  planned, theorised, prepared — and NOTHING ships. assets/ still sits in ai-council as the symbol
  of it. He expects the theory, the audits, the intakes, the ADRs to FINALLY be implemented
  intelligently. The next session is judged on delivery, not planning.
- The methodology-management scope is broad by operator ruling: not only LLM working-methodology
  but naming, file/folder structure, Python engineering standards, dependency parity — the
  architect owns all of it.
- The vision audit (Fable, cold-boot) is the operator's requested fresh-eyes critique of the whole
  direction — he takes it seriously and wants its theses acted on in their own session, not buried.
- Push is standing-permission; the operator is the merge/strike gate; he judges when a session ends.
- The two intake drafts (buy-vs-build, nightly-audit-standard) exist as downloadable files, NOT yet
  ingested into docs/intake/. Given the reject-the-engine ruling, the buy-vs-build intake needs
  REWRITING before ingest (it argued FOR a pivot the vision audit reversed) — flag, do not ingest
  as-is.
