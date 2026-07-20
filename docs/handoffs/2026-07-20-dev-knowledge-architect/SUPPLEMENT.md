# Architect strategic supplement — 2026-07-20-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-20

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
The thesis grew from "recorded ≠ enforced" to "recorded ≠ enforced ≠ EFFECTIVE". Four
green-that-means-nothing instances in one day: phantom enforcement (#359, a rule naming an absent
mechanism); a Codex review that filtered its own subject out of the diff and returned a verdict
(#363); a colour test whose grey predicate also satisfied navy so it passed either way; and a
one-directional doc↔code check reporting agreement it never established. Next session's
way-of-working goal: treat GREEN as a claim to falsify, not a result to trust — prove by violation.
The residual-completeness gate built this session is the template: it shipped only because it was
demonstrated RED on a real unfilled bundle, not because it was registered.

PAIN → BUILD MAP (why the operator cares, one line per wave; the build detail lives in [E8], not here)
- W1 visible boundary — the colours, his single most-repeated ask across ~20 sessions (MERGED, render witness pending).
- W2 structure — "why do the folders differ": assets/→config/, Pyrefly universal, root-vs-config rule.
- W3 lifecycle — intake→ADR→close→DELETE: the process problem, real deletion, accretion brake.
- W4 archive — he must SEE live vs archived; archiving coupled to status, precedes W3.
- W5 guards — the worktree pain; hub goes read-only, handoff the sole writable surface.
- W6 canon+prompt — inoculation legibility (shipped) + the co-change enforcement half ([#354]).
- W7 testing+fleet — evidence gate + the fleet-state collector.

2. TENSIONS WEIGHED
- Measure-the-whole-corpus vs ship-mechanisms → ship, with a measured baseline behind it (320
  MUST-shaped rules, 176 silent = 55%, a FLOOR — docs/decisions/ unswept, #357).
- Ledger as report vs as mechanism → mechanism; a one-off table decays.
- Generate the .vscode config vs eliminate the state → elimination (two regexes keyed on markers
  carry no per-region state, cannot rot). Recorded as a [#352] Done-when amendment. #329 still
  genuinely needs generation from parity-surfaces.yaml.
- Markers vs headers as boundary source of truth → markers win; headers generated from them.

3. CONSIDERED + REJECTED — do not relitigate
- Narrowing the arc to a ~55-rule slice → REJECTED by the operator. Fix ALL rules, prioritised,
  goal never lowered. ARC 5 is the first tranche of a tracked burn-down.
- A fifth ledger state for advisory rules → REJECTED; a MUST-shaped-only denominator drops them out.
- Ratifying the six off-canon intake statuses → REJECTED. One enforced pattern instead:
  SEED→DRAFT→READY→{ACCEPTED|CONSUMED|SUPERSEDED|REJECTED}, the "to what" in required companion
  fields; naming YYYY-MM-DD-<class>-<slug>. Dissolves the id:14 triple.
- mypy as a sanctioned divergence → REJECTED by the operator. Python stack, tooling universal →
  Pyrefly (stable 1.0 May 2026, ships AI-agent workflow docs incl. Stop-event hooks matching this
  fleet; `pyrefly init` migrates from mypy config cheaply).
- Mid-arc re-planning → REJECTED. The plan governs; new scope goes to BACKLOG, execution does not swerve.

4. OPEN QUESTIONS — unresolved / deferred
- [#352] W1 is MERGED, NOT CLOSED — closes only on the operator's render witness, which has not
  happened. Closure clause (f) open.
- W1 clause (c): no archived Codex review artifact — the reviews ran, the evidence was never
  written to docs/audits/. Clause (c) is itself a MUST-rule with no mechanism: the closure contract
  is silently unenforced from wave 1. Rule it now, at n=1.
- Two failure classes the four-state ledger cannot express: phantom enforcement (#359) and orphan
  enforcement (a mechanism no rule declares).
- codex-review scoping (#363): filters mixed diffs to their code subset; can review a fraction while
  reporting a whole-diff verdict. Until fixed, invoke `codex exec` with files named explicitly.
- R8 (corp #38) is OUT — the architect handles hub + methodology only, nothing corp-side.

5. DECOMPOSITION RATIONALE — what NOT to redo
The ARC-5 plan of record is BACKLOG theme [E8] (NOT an ADR — a wave map must evolve). Read [E8];
do not re-file it, re-derive the baseline, or re-adjudicate the nine seeds (terra killed none; W1
and W4 are the seedless waves; seeds 5 and 6 map to W2/W5 by content). Recommended first move: the
STRUCTURE wave (W2) — assets/ dissolution (operator GO recorded; relocate to config/ first, then
delete), the Pyrefly rollout, and the root-vs-config placement rule (root only for tool-mandated
files like pyproject.toml — a named closed exception list; everything else to config/). It is where
the operator's granted rulings sit and what he sees in every repo. The ARCHIVE wave now PRECEDES the
lifecycle wave: archiving is coupled to status (terminal statuses move the file to <folder>/archive/,
so it is a file move needing a reference-integrity check — reversing the inbound "stay-in-place"
convention on the operator's explicit reasoning that he must SEE live vs archived).

6. OFF-REPO CONTEXT
- Operator rulings this session, binding: .vscode is SHARED FLEET CONFIG (hub-owned). Consumers get
  READ-ONLY hub access — read and query, never write; the sole writable surface is docs/handoffs/,
  which another repo may trigger. Simplifies the #344 Ask-2 guard from a HEAD-bound token to a
  path-scoped write deny; aligns with ADR-28 (Layer 2 is passive, not an execution engine).
- ROLE EXPANDED: the architect owns Python engineering standards and cross-repo dependency
  management (real incident: one repo lacked pytest requirements another had), tooling choice, and
  folder/file naming — not only LLM working-methodology.
- The sort-order incident surfaced the .vscode shared-vs-personal boundary: personal view
  preferences (sort order) must NOT live in fleet-canonical config. This is a W2 boundary question.
- NOTHING was deleted this arc and NO backlog task was closed (116→132+). The visible pain the
  operator still sees — the assets/ folder — is W2 work, granted but not executed.

BINDING — do not relitigate
- The baseline is established: 320 MUST-shaped rules, 176 silent (a FLOOR — docs/decisions/ unswept).
- The four-state ledger schema stands.
- The declaration test stands: on-surface AND bound to an open ticket. Neither condition suffices alone.
- .vscode is SHARED FLEET CONFIG, hub-owned.
- The hub is READ-ONLY to consumers; docs/handoffs/ is the sole writable surface.
- Pyrefly is universal across the fleet — NOT a sanctioned mypy divergence.
- Archiving is coupled to status, and the ARCHIVE wave PRECEDES the lifecycle wave.
- The goal is ALL rules, prioritised — not a bounded slice. The goal is never lowered.

DO-NOT-REDO
- [E8] is filed as a BACKLOG theme — do not re-file it or convert it to an ADR.
- The baseline is measured — do not re-derive it.
- The nine seeds are adjudicated — terra killed none; W1 and W4 are the seedless waves; seeds 5 and 6
  map to W2 and W5 by CONTENT, not by label.
- The residual-completeness gate is built AND demonstrated RED on a real bundle — do not rebuild it.
