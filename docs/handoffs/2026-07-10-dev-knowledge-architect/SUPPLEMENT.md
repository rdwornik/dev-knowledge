# Architect strategic supplement — 2026-07-10-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-10

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

A1 (strategic intent): EXECUTE plan-v3 §D — theme: "teeth for the edges".
Convert 07-09's incident set (I1–I6) into mechanism: G8 runbook fix first
(gates B-S2), corp-monorepo onboarded as runbook n=2 + seeder first consumer,
#300 hermetization ADR drafted (P1, before Wave-2), EPIC G decomposition the
moment the operator's QA-functional intake lands. Visible-results bar stands.

A2 (tensions weighed): night autonomy vs proposals-only → proposals-only,
validated n=1 (zero unwanted mutations, full queue honored). d.iii retroactive
vs prospective → prospective + grandfather + canonical CLASS enum (S3
quantified: retro = ~65% corpus rename for near-zero gain). PLAN.md generator
vs manual → manual n=1 done (this bundle), generator build = #301. Subagent
parallelism → read-only fan-out only; git mutations serial (index-race,
ratified from lived-QA + night run).

A3 (considered + rejected — do NOT relitigate): retroactive audit renames;
parallel subagent commits on one tree; fabricating SUPPLEMENT/retrospectives
for past sessions (07-05 cold bundle → accept-and-annotate, not backfill);
mandatory-TDD (council-rejected, stands); night merges beyond the 4 committed
classes; docs/plans/ top-level (plans are bundle-resident, #301).

A4 (open questions): #300 d.ii mode-boot bundle home + fate of the 07-07
committed functional bundle + 27 superseded-era bundles (S4-3, one migration
pass); d.iii CLASS enum contents (ruling shape decided, list to draft in the
ADR); age-based backstop design — the night audit's single structural theme
(intake-age → #270/#271, cold-bundle → #292 gate, Pattern-C
amendment-summary drift has NO organ yet, unfiled); EPIC H doctrine (run
changelog V1 worktree-contamination verify as its first input); #254(b)
fleet-audit auto-push vs manual cadence; P7 (operator, one line, closes
EPIC C); QA-functional session output pending.

A5 (decomposition rationale): §D order is dependency-true: G8 fix gates
B-S2 (n=2 must run the corrected layer-6 verify); B-S2 gates v4-template
archival (corp must be off v4) and provides #262 tool-managed n≥1; #300
before Wave-2 (artifact classes multiply per repo onboarded); QA
decomposition ∥ B-S2 is collision-free (hub/browser vs corp-monorepo chat).
Session-start batch (small, serial): ADR-51 README one-liner (verify-then-
fix) · 2 stale intake Status: lines · #181 citation convention ·
docs/handoffs README documents PLAN.md as bundle member · demo-prep backup
verdict if terminal check showed unpushed work. Do NOT redo: the grooming,
#300 scope text (filed verbatim), the d.iii ruling, the night autonomy
contract, C-S3v2 results, lived-QA findings (F1 already filed as #302).

A6 (off-repo context): operator verdicts on record this cycle: QA must be
a PROCESS-level role (playbook + onboarding legs, fleet carrier); test
depth proportional to T1–T5 scope tags; subagent routing doctrine wanted
(EPIC H); night runs wanted — gated by #270, which RE-ENTERS admission;
plans are part of every session (#301, operator-ratified pattern); folder/
naming discipline is a hard trigger for the operator — treat R13 and #300
as P1 posture, not paperwork. WMI machine incident root-caused and fixed
(elevated winmgmt restart; G9 latent, dormant). Operator still owes: P7
one-liner + the QA-functional session (boot is printed and ready). Budget:
sky-is-the-limit stands; Opus+high effort default for judgment work.
