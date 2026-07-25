# Architect strategic supplement — 2026-07-25-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-25

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


1. STRATEGIC INTENT (way-of-working, not task)

Make SELECTION and CLOSURE mechanical instead of remembered.

Today both run on operator recall: what matters next lives in the architect's head (five ruling
clusters leaked across three handoffs), and whether a ticket is done is a prose judgement (#215
was permanently gate-invisible; #339 sat open across two handoffs because its Done-when was a
disjunction nobody parsed). The methodology goal is that a fresh session knows what matters
without being told, and a ticket cannot be filed without naming what proves it done.

Falsifiable at the way-of-working level: a fresh session's FIRST message quotes the top-5
ready-set with rationales plus every ruling overdue > 8 days, with zero operator memory involved.

2. TENSIONS WEIGHED — and where they landed

(a) Rebuild-first vs deploy-first. Resolved NOT by old-vs-new but by ARTIFACT LOCATION: what
    deploys becomes N copies to migrate; what is hub-only costs nothing to change. Almost every
    rebuild candidate is hub-only. Landed: rebuild first, bounded to one arc with an exit test.
    Caveat that survived self-review: validate_backlog ships in the tier1-lifecycle PLUGIN, so
    the migration carries an explicit plugin leg — the one row where "hub-only" was false.
(b) Big-bang vs strangler migration. Landed strangler: verbatim split -> byte-stable round-trip
    -> source-of-truth flip -> prose relocation AFTER. Reason: 158 files plus four gates changing
    at once, on the fleet's most-referenced file, is the wrong risk profile when a reversible
    path costs one extra generator.
(c) Graph vs LLM scoring. Landed graph-only this arc. The graph signals are computed, exact, and
    have no hallucination surface; they alone would have caught the leaked clusters. LLM
    estimation is the speculative half and waits for evidence that selection still feels
    vibes-driven. This is ADR-104's own incremental doctrine applied to our own tooling.
(d) Adopt Backlog.md vs build-thin. Landed build-thin with Backlog.md as PATTERN DONOR (one task
    = one file, frontmatter, folder-by-status). Reasons: taxonomy collision with docs/intake +
    docs/decisions + ADR-101 grammar; [#N] ids are cited across all git history; no scoring
    engine either way. What would flip it: valuing a ready-made board UI above schema control —
    name that trade explicitly in the ADR, never split the difference silently.
(e) Fibonacci as doctrine vs decoration. Landed: BINDING for estimated fields and free constants
    (the log-spaced scale is why sums are sound and why "7 vs 8" false precision dies); NOT
    retrofitted onto functionally measured values (token budgets, calendar cadences). A
    golden-ratio file-size rule has no enforcing mechanism and no failure mode it prevents.
(f) Model lanes: capability vs consumer. Landed one binding guard — NO MODEL LANE WITHOUT A NAMED
    CONSUMER. Derived from the operator's own #419 reframe: the defect is output nobody reads, so
    a lane must state which morning-loop slot or gate consumes it before it activates.
(g) PLAN.md ceremony vs traceability. Landed FOUR states (DRAFT -> REVIEWED -> APPROVED ->
    CLOSED-with-outcomes). Three erased the review beat, which was the arc's highest-hit-rate
    mechanism (six defects caught pre-execution); six was ceremony for a solo operator.

3. CONSIDERED + REJECTED — do not relitigate

- Backlog.md AS ENGINE (adopted as pattern donor only) — reasons in 2(d).
- L5b predictive ML — not "gated on volume", NOT APPLICABLE: defect prediction needs labelled
  defect data; this fleet records decisions, not defects.
- Product-form scoring (priority x alignment x unblock_count) — compounds estimation error, zeroes
  items on one weak term, and folds an exactly-computed number into soft ones. Sum over a single
  Fibonacci scale, unblock_count as its own column.
- Weekly full re-scoring of every ticket — waste; event-driven instead.
- Six-state PLAN.md lifecycle — 2(g).
- Big-bang migration — 2(b).
- A managed id-counter FILE — the directory is the counter (max+1); a counter file is one more
  thing to desync.
- Gemini for EXACT-TOKEN RETRIEVAL — deterministic git grep / git log is cheaper AND more correct
  there. (This rejection is scoped to that job class ONLY; see 4 and 6 — Gemini IS accepted for
  semantic work.)
- Copilot activation NOW — filed with a TRIGGER, not rejected: every current job is assigned, and
  a fourth producer before the morning-loop consumer exists worsens #419.
- Relitigating ADR-104 — four days old, rules the fold shape. Appetite change = an explicit
  one-sentence amendment, never drift.
- Hand-closing tickets outside the gate (rejected 2026-07-21, still rejected).

4. OPEN QUESTIONS — unresolved or deliberately deferred

- R-G: WHICH Gemini CLI is the scanning lane? Blocks everything Gemini — the recorded lane
  (Antigravity) is ADR-12-excluded until the AG-2 identity-roulette question clears.
- R-N: confirm 8 days as the overdue-ruling WARN threshold (Fibonacci family).
- R-S: confirm the seeded-defect list for grok's acceptance test (assertion-beyond-verified-scope,
  the GIT_* scrub-set derivation, the duplicate stale header, the wrapper scoping gap).
- CODEMAP SCOPE — asked in v1 and NEVER ANSWERED: the codemap reports two modules, both orphan,
  zero dependencies, because --source-root scripts admits only packages; audit.py, deploy/ and the
  hooks are invisible. Widen the source root, or stop calling it the canonical code-structure
  artifact? Unresolved.
- [#420]: does a TOP-LEVEL docs/archive/ still make sense given per-area archives? Structural,
  filed, unruled. Resolve INSIDE the backlog restructure — same folder-taxonomy question.
- Prose relocation target: does <= 233 chars apply to all 158 tickets or only the >= 900 group?
- Deliberately deferred: LLM scoring layer · #401(b) build · #405 build · #402 deploy window ·
  corp #327 merge · #383 fold stages · satellite wave (frozen).

5. DECOMPOSITION RATIONALE — and what NOT to redo

Three pieces, not one arc, because they differ in KIND:
- MICRO-WINDOW is orientation-surface repair. ARCHITECTURE is what the next session reads to
  orient; fixing it first makes every later judgement in the arc better-grounded. It also carries
  the two unfiled gaps, which cost nothing and rot if carried.
- MAIN ARC is one wave = one merged arc (the standing rule v1 violated by packing six lanes).
- AGENTS.md is a RULING, not a build — a decision sitting does not belong inside a build arc, and
  its input (the redundancy map) comes from a Gemini pilot that is gated on R-G.

Sequencing rule INSIDE the main arc, and this is the safety design, not a preference:
REVERSIBLE BEFORE IRREVERSIBLE · READER BEFORE WRITER · VERIFIER BEFORE GENERATOR.
Concretely: build the validator over the new format FIRST, then generate the tree, then diff the
generated tree against BACKLOG.md. Until the source-of-truth FLIP, BACKLOG.md remains
authoritative and every commit is trivially revertible. There are exactly TWO one-way doors — the
flip, and the prose relocation — and each takes its own operator GO, never mid-lane.

MUST NOT be redone or re-decided: the six self-review corrections D1-D6 · the model-fleet
dispositions (grok in now, Codex retires only on the seeded-defect test, Gemini propose-only with
deterministic-first routing, Copilot filed-with-trigger) · the scoring form (sum over one
Fibonacci scale, unblock_count separate, event-driven re-scoring, sticky override) · verified_by
as a required field · the strangler sequence · ADR-104 · the four PLAN.md states.

6. OFF-REPO CONTEXT

- TRANSPORT: the consolidation decision v2 was authored in chat and is being ingested as an
  intake. No architect-emitted artifact stays in Downloads — that is the loop the PLAN.md brief
  exists to close.
- OPERATOR PHILOSOPHY (dictated, treat as design input): Fibonacci / golden ratio woven through
  the system — scales, free constants, proportions of thought. Honored where a scale or an
  arbitrary constant is needed; explicitly NOT retrofitted onto measured values. He asked for this
  to be a standing element, not a one-off.
- MODEL FLEET is the operator's call and he made it: he WANTS grok (enters now, shadow), KEEPS
  Copilot available (free), and WANTS Gemini used (free, long context, "fantastic at scanning").
  The architect reversed its Gemini rejection on the merits — semantic dependency work (doc2doc,
  doc2file, code2file) is exactly what grep structurally cannot do, and ADR-88's own
  "declare-what-you-cannot-compute" is the opening.
- STANDING EDUCATE OBLIGATION: when the operator follows a recommendation he has not inspected, he
  gets a plain-language report-back per milestone — what changed and what it means in practice.
- METHOD WARNING for the incoming architect: the outgoing one issued THREE defective instructions
  in one session (asserted recommendations existed in a handoff when they were open questions;
  demanded a single-file check when the repo's own rules required three; told CC not to treat a
  dirty index as a merge blocker when git refuses outright). Each was caught by CC or by terra.
  Verify instructions against tool and repo behaviour before issuing them — the class is asserting
  beyond verified scope, and it is the same class terra caught in the code.
- INCIDENT FAMILIES still open: [#414] self-acting-on-main (two instances); the ADR-85 any-SHA gap
  (a JOURNAL anchor is satisfied by ANY in-session SHA); live-session detection must enumerate ALL
  ~/.claude/projects dirs, never a subset (a subset scan produced a false LIVE today).
- NO CI EXISTS (.github/workflows absent) and no pre-commit hook runs pytest — the suite runs only
  when a human or the verify skill invokes it. This is why a Lane C regression sat on origin for a
  whole arc. Any contract touching BACKLOG, JOURNAL, or a file a test reads MUST require full
  pytest with exit codes read directly, never through a pipe.
