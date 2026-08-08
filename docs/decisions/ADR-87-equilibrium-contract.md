# ADR-87: Architect↔CC equilibrium contract — conditional intent-only prompting

**Status:** Accepted
**Date:** 2026-06-18
**Decision tier:** Architecture (Path A — direct operator ruling, grounded in the STEP 1 empirical self-load finding; no Council transcript, like ADR-65/66/80/81)
**Related:** ADR-82 (handoff v5 — the sibling architect↔CC channel), PLAYBOOK §2 (prompt conventions — the maintenance authority), #159 (operator-context beat), #184 (this arc's tracking item), #185 (the GAP-2 backstop, filed-not-built)

## Context

A "next-build" prompt has historically front-loaded a full skeleton (PLAYBOOK §2): summary
table, read-first pointers, git workflow, UNDERSTAND, numbered steps, anti-patterns. The open
question this arc set out to answer empirically: **how much of that must the architect author,
versus how much does CC self-load reliably from the repo it holds?**

STEP 1 of this arc verified the answer **by class**. CC self-loads context **reliably only for
code-impact tasks** (the #167 class — a task that edits code/specs gives CC a concrete file
target, and it pulls CLAUDE.md, the touched module, and adjacent tests on its own). It is
**unreliable** for three gaps:

- **GAP-1 — read-only tasks.** With no code-impact target, the self-load isn't triggered; CC
  does not reliably pull the governing docs for an audit/review/analysis ask.
- **GAP-2 — execution-time micro-decision gotchas.** Empirically recurred **n=2/n=3 even with**
  the standing "check gotchas" line in the prompt. Prose cannot fix this class — the failure is
  a per-action micro-decision (a commit-message shape, an Edit that deletes), not a session-start
  read. Only a **deterministic backstop** (a hook) closes it.
- **GAP-3 — governance context.** Which specific ADR / LESSONS entry / sibling-spec a task
  touches is **not self-inferred** — CC does not reliably discover the one decision record or
  prior-art file that governs the change unless it is named.

Therefore **"intent-only" prompting is conditional**, not universal. It works for the
code-impact class; it under-loads the other three. The fix is a recorded **division of labor**
plus a thin, always-present pointer for the gap CC structurally cannot close from inside the
repo (GAP-3). The GAP-2 gap is orthogonal to the prompt and gets a deterministic backstop,
filed separately (#185).

## Decision

1. **Record the self-load finding (reliable by class).** Code-impact self-load is reliable;
   read-only (GAP-1), governance-context (GAP-3), and execution-time gotcha (GAP-2) self-load
   are not. This is the empirical basis for everything below.

2. **The equilibrium contract — who emits what.**
   - **The architect emits:** *intent* · *closure* (what "done" looks like) · *anti-patterns* ·
     the **plan/auto mode** · a **thin per-task governance-context pointer** (the specific
     ADR / LESSONS entry / sibling-spec the task touches — GAP-3 won't self-infer it).
   - **CC owns:** *code-impact context* (the files/tests it self-loads) · *generic gotchas* ·
     the prompt **skeleton** (PLAYBOOK §2 — now CC's consumption-spec, not the architect's
     authoring burden) · *model/effort*.

3. **Intent-only is conditional.** For a code-impact task, the architect may emit intent + mode
   (+ pointer if any governance applies) and CC self-loads the rest reliably. For a read-only,
   governance-touching, or gotcha-sensitive task, the architect **must** supply the thin
   governance-pointer — omitting it regresses GAP-3.

4. **The thin governance-pointer is always available, required when governance applies.** It is
   *thin* (a pointer, not a restatement — CC pulls the named source) and *per-task* (only the
   ADR/LESSONS/sibling-spec this task actually touches). It is the architect's contribution to
   the one gap CC cannot close from inside the repo.

5. **The mode is the architect's judgment, with a recorded basis.** Choose **plan** when
   uncertain / multi-file / unfamiliar; **auto** when the diff is a trivial one-sentence change.
   The selection criterion is already documented — PLAYBOOK §2 "How to choose Mode"
   (auto-accept / plan-then-auto / plan); this ADR points to it rather than restating it. The
   rule is "state the mode **and** the basis," not merely "state a mode."

6. **The GAP-2 backstop is filed, not built here.** A deterministic PreToolUse guard that
   injects the matching gotcha on a commit-message / Edit-deletion pattern is the GAP-2 fix —
   orthogonal to this prompt contract. Tracked as #185; **not** part of this codification.

7. **The contract lives in the durable surfaces, not operator memory.** Canonical home: this
   ADR. Maintenance authority + consumption-spec framing: PLAYBOOK §2. Standing rule (one line):
   ESSENTIALS "Writing a Prompt". Per-session carrier (pointer): HANDOFF_BOOT "Architect mode".
   The **format/skeleton stays in PLAYBOOK**; the handoff carries the **contract**, not the format.

## Consequences

**Positive:** the architect's authoring burden drops to what CC genuinely cannot self-load
(intent + mode + the GAP-3 pointer); the skeleton is reframed as CC's consumption-spec, so a
complete prompt is still defined without the architect hand-writing all of it; GAP-3 has an
always-present channel; the finding and the division of labor are recorded once, referenced
everywhere, so neither rides in operator memory.

**Negative / accepted:** the contract is **conditional**, which is a judgment surface — the
architect must classify the task (code-impact vs read-only/governance/gotcha-sensitive) to know
whether the pointer is mandatory; misclassifying a governance task as code-impact silently
re-opens GAP-3. GAP-2 stays open until #185 ships — prose in this contract does **not** close it
(that is the whole point of filing the deterministic backstop). The closure of the arc is an
*empirical* demonstration on the next real build (#184), not the landing of this codification.

## Alternatives rejected

- **Universal intent-only ("just say what you want; CC figures out the rest").** Rejected: STEP 1
  showed it under-loads GAP-1/2/3. Intent-only is reliable only for the code-impact class.
- **Keep the full architect-authored skeleton (status quo).** Rejected: most of the skeleton is
  context CC self-loads reliably; hand-authoring it is redundant work and invites stale copies.
  The skeleton is retained — but as CC's consumption-spec, not the architect's authoring task.
- **Fix GAP-2 with a stronger prose instruction in the contract.** Rejected: it already recurred
  n=2/n=3 *with* the standing "check gotchas" line. A per-action micro-decision needs a
  deterministic guard (#185), not more prose.
- **Carry the skeleton/format in the handoff bundle.** Rejected: the format belongs in PLAYBOOK
  (the maintenance authority); the handoff carries only a pointer to the contract. Duplicating
  the format into the handoff is the drift failure mode this repo guards against.

## Links

- ADR-82 — HANDOFF_PROCESS v5 (the architect↔CC handoff channel this contract rides)
- PLAYBOOK §2 "Creating a Claude Code Prompt" — prompt-convention maintenance authority + the skeleton (CC's consumption-spec) + "How to choose Mode"
- `protocols/ESSENTIALS.md` "Writing a Prompt" — the one-line standing rule
- `protocols/HANDOFF_BOOT.md` "Architect mode — generative posture" — the per-session contract pointer
- BACKLOG #159 (operator-context beat — adjacent, distinct), #184 (arc tracking item — closes on empirical demonstration), #185 (GAP-2 deterministic backstop — filed, not built)

## Amendment — 2026-08-08: the population boundary on model/effort

> **The architect states the session's boot tier; CC routes sub-steps inside it.**

Ratified 2026-08-06 (architect supplement, A7(c)); landed in-repo 2026-08-08.

**What it resolves.** The equilibrium contract in the Decision section above assigns *model/effort*
to CC without naming the level that assignment applies at, and the word carries two readings: the
tier a **session boots at**, and the tier each **sub-step inside that session** runs at. Read as
the first, it contradicts the architect's dispatch responsibility; read as the second, it is
exactly right. The boundary is drawn by **population, not by authority** — the architect owns the
one-per-session choice, CC owns the many-per-session ones.

**This is an amendment section, not an edit.** Decision item 2 ("the equilibrium contract — who
emits what") stands exactly as written; where the two are read together, this section governs.
Nothing else in the division of labor moves: the architect still emits intent, closure,
anti-patterns, the mode, and the thin per-task governance pointer; CC still owns code-impact
context, generic gotchas, and the prompt skeleton.

**Out of scope.** Which tier any given repo or arc actually boots at is not decided here — the
routing matrix is `protocols/PLAYBOOK.md` Ch8, "Model + effort are stated at dispatch — the
routing matrix". This amendment fixes *who states the boot tier*, not *what it is*.
