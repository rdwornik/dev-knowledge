# Architect strategic supplement — 2026-07-18-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-18

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

ANSWERS — outgoing architect (2026-07-18 serial-integration close-out session)

These are OPERATOR RULINGS made in the outgoing chat and transcribed VERBATIM —
they exist only in chat and must travel. Read them as the binding off-repo "why"
for ARC 4; the schema mapping below is secondary to the verbatim text.

RULINGS (verbatim):

- RULING-W: hub MAY/SHOULD write into consumer repos for methodology/cleanup —
  separate worktree/branch, then report; FIRST step of any consumer leg = codify
  this as the ADR-36/41 amendment (mechanism before act).

- RULING-S: every governed file gets READER-VISIBLE sections separating
  methodology-universal vs repo-personal (CLAUDE.md + configs; machine markers
  alone insufficient).

- RULING-PY: ruff baseline targets py311 now (corp floor); standing direction
  "always newest Python" -> file the fleet-upgrade ticket.

- RULING-CF: ai-council adopts the conformance workflow.

- #329 design input: editor-side background decoration of owner=hub/repo regions
  via versioned .vscode (grey/navy on dark theme).

- #341 R2 ruling: producer-activation = sanctioned repo-local AGENTS.md override
  (per-run flag rejected, witnessed evidence).

- Satellite wave: still FROZEN until corp + ai-council lessons extracted.

--- schema mapping (CC framing of the verbatim rulings above; the rulings are authoritative) ---

1. STRATEGIC INTENT: run ARC 4 — fleet equalization. Bring the Wave-1 consumers
   (corp-monorepo, ai-council) into methodology parity with the hub, harvesting
   their lessons first. RULING-W is the enabling doctrine: the read-only hub
   becomes one that can WRITE into consumers under a mechanism-first discipline
   (worktree/branch → report). The way-of-working goal is the ADR-36/41 amendment
   that sanctions this — it is the FIRST step of any consumer leg, before any
   equalization edit.

2. TENSIONS WEIGHED: breadth-first onboarding vs depth-first hub hardening —
   resolved toward equalizing the two Wave-1 consumers before firing the satellite
   wave (which stays FROZEN until their lessons are extracted). Mechanism-before-act
   (RULING-W) over expedient direct writes: the amendment lands before the edits.
   Machine markers vs human legibility (RULING-S) — resolved that reader-visible
   sections are REQUIRED; the owner=hub/repo comment markers are necessary but not
   sufficient, and #329's editor decoration is the complementary human-facing half.

3. CONSIDERED + REJECTED (do not relitigate): a per-run codex profile/flag for
   producer activation — REJECTED in favor of a sanctioned repo-local AGENTS.md
   override, on witnessed precedence evidence (#341 R2). Firing the satellite
   onboarding wave now — REJECTED (frozen until corp + ai-council lessons land).
   Unmediated hub→consumer or consumer→hub tree writes — REJECTED; the sanctioned
   path is worktree/branch + report (RULING-W). Chasing "always newest Python" as an
   immediate baseline bump — deferred to a filed fleet-upgrade ticket; the ruff
   baseline stays py311 (corp floor) for now (RULING-PY).

4. OPEN / DEFERRED: #344 session-close gate + consumer hub-write guard
   (NEEDS-RULING — Ask 1 pre-handoff gate, Ask 2 consumer-side PreToolUse guard;
   RULING-W defines the sanctioned write path Ask 2 must allow). The fleet-upgrade
   ("always newest Python") ticket is not yet filed. #300 hermetization residual
   (d.i/d.ii/d.iii) pegged BEFORE Wave-2. #339 ADR-29 chronological-split build leg.
   The #162/S1 architect actor-vs-mode vocab collision, standing.

5. DECOMPOSITION RATIONALE: ARC 4 opens with the ADR-36/41 amendment (RULING-W,
   mechanism-first) — NOT an equalization edit — then re-witnesses each consumer
   live before touching it. The reviewer-path (#338) and producer-path (#341) are
   disjoint codex threads; #341's activation decision is already made (R2), so it is
   build, not design. Do NOT re-derive the producer-activation mechanism (repo-local
   AGENTS.md, ruled) or re-open the satellite freeze.

6. OFF-REPO CONTEXT: the ARC 4 prompt file is operator-held (approved, off-repo).
   Re-witness the consumers first — their state may have moved since the last window.
   All seven rulings above are this session's binding operator input and exist only
   in chat; they are the reason the equalization arc can proceed at all.
