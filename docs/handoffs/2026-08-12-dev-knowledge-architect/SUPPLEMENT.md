# Architect strategic supplement — 2026-08-12-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-12

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

### CC-observed addenda — this window's carried items

> These are **CC observations from the closing arc, not chat answers.** They are placed here so the
> outgoing architect chat can confirm, correct, or add the "why" behind each; they do **not**
> pre-empt the ANSWERS region below, which stays EMPTY until the operator fills it. CC never
> fabricates an outgoing chat's answers.

**A. The two night artifacts ride UNADJUDICATED — the incoming seat's first order of business.**
`night-1` (truth audit + handoff numbers) and `night-2` (lessons, governance, strategy) are merged
to `main` and ratify nothing. Landing them made their content reviewable in the tree; it accepted
none of it. Ask the outgoing chat what it *intended* each to bind, because the artifacts themselves
state findings rather than decisions.

**B. OPEN RULING carried — the I-D6 working-set reading.** I-D6 defines the working set as
SEED/DRAFT/READY; the BRIEF one day later applies DRAFT-only. Measured at the cut the two readings
differ by **11** (definition-reading 14 against a ceiling of 6; applied 3). Not reconcilable by
evidence — two different rules, and the choice is the operator's. **It gates the consolidation-intake
filing**, so it is upstream of item C.

**C. The consolidation intake is mis-scoped as drafted.** Night-1 verified the three GAPs
negatively: GAP-1 is real; GAP-2's archive leg is owned by `[#420]` under a live do-not-touch order;
GAP-3 is W-9(a) inside an ACCEPTED intake with a recorded `AGENTS.md` collision hazard. Filing
GAP-1+2+3 as one intake would re-derive two owned scopes — the failure its own brief names.

**D. The VS Code incident closed during the arc.** Root cause was a `terminal.integrated.env.windows`
`"Path"` member that REPLACES the terminal PATH — **not ours**, present in every settings backup
back to 2026-07-12, now removed. 26 dead `pytest-of-*` PATH entries cleaned (1286 → 4168 → 1322
chars). The test-isolation defect that **was** ours is fixed (the suite wrote the real
`HKCU:\Environment` key; an autouse conftest tripwire now fails the offending test and restores the
value). Merged `win-tooling@1f8b300`, pushed.

**E. The night lanes ran LOCALLY — a deviation with a near-miss.** Both ran against the primary
checkout rather than one worktree per lane. A commit was silently re-targeted onto the other lane's
branch between `git add` and `git commit`, sweeping in that lane's untracked artifact; repaired
non-destructively and nothing was lost. **`git add` then `git commit` is not atomic against a
concurrent branch switch in a shared tree.** The shared index also made `audit-index-freshness`
unsatisfiable from inside a lane — that generator defect is now fixed (tracked-files-only).

**F. The organ index relocated and the gate-shape hole closed.** `docs/ORGAN-INDEX.md` →
`ecosystem/organ-index.md` (operator ruling A; register `STANDING_RULINGS` **K-1**), plus **Rule C**
in `validate_hermetization.py`. The finding worth carrying is *why* it landed loose: ADR-101's gate
read the top level and the `docs/<genre>/` level and stopped, so Rule A was silent **by its own
literal spec** — and a test asserted that silence. Rule C reads the rest of the path; Rule A is
untouched.

**G. Architect-model note — how to boot this seat.** Per PLAYBOOK **Ch8**, the architect seat
**boots Opus**. **Fable is reserved for adversarial passes** (the plan-review / red-team role), not
for the primary architect seat — booting it here would spend the adversarial reserve on ordinary
adjudication and leave nothing independent to check the result.


===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->
