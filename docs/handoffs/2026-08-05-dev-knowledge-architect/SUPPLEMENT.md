# Architect strategic supplement — 2026-08-05-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-08-05

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

SUPPLEMENT ANSWERS — 2026-08-04/05 window, sealing architect — seal anchor 186efb5a

Q1 STRATEGIC INTENT. Shift the way of working from BUILDING verification to
CONSUMING it at scale: the next window's architect should adjudicate against
machine-built evidence (the 132-row ranked sheet, the one-graph-two-orderings
priority axis, measured model acceptances) instead of assembling evidence by
hand. Second, at fleet level: make "fleet-green" a TRUE claim — L0 is the
ladder's bottleneck two windows running (1/6 [#383] surfaces, parity 5/9) and
its two unlocks are NC2 and [#490]. Mechanisms exist now; the goal is
throughput through them.

Q2 TENSIONS WEIGHED. (i) Refuse-vs-surface on [#480]: landed LAYERED
(advisory now, hard leg [#499] behind 0FP/2-windows) because hard-wiring
before production mileage repeats [#483]'s measured 11/11-FP error; ADR-85's
asymmetry is the precedent. (ii) Trim-vs-disposition on doc_rot: self-induced
bloat is trimmed (dedup), a disposition is reserved for genuine rule-vs-ruling
conflict ([#492] — the ruled peg legitimately carries dates). (iii) Honest
filing vs §F optics: the batch was admitted with its close engine named
([#487]); [#498] and the cp1252 row prove filing-early beats hiding.
(iv) Protection-vs-ritual on the [#482] pin: tuple-identity over cardinality,
because a pin that REDs on benign growth trains number-bumping. (v) Library-
first floor: stdlib composition beat an installed dep on SEMANTICS (pathspec's
gitwildmatch ≠ pure glob) — library-first is measured divergence, not
dependency-first.

Q3 CONSIDERED + REJECTED (do not relitigate). pathspec engine (semantics) ·
glob.glob engine (reads worktree not index; kills the host-independence test)
· cardinality pin · hard-wiring any advisory leg before its evidence bar
(twice-ruled: [#483] R3, [#499]) · ADR creation NOW for the [#483]/[#480]
rulings (the ADR moment is the hard flip, arriving with data) · REMOVE for
.claude/** (REPAIR executed) · retro-editing the 9/16 legacy artifacts into
the canonical shape · a separate U-4 row (collapsed into [#499] rider R2) ·
fixing [#310] or the hook defect mid-arc (plan-governs held) · scanning
tasks/*.md alongside generated BACKLOG (duplicate findings).

Q4 OPEN QUESTIONS (deliberate). [#499]'s first false-positive count — owed at
the SUCCESSOR's seal, every seal thereafter · age threshold N for retirement
rank R3 (operator ruling) · GitHub private-repo required-checks plan limits
(intake #24 P1 verification item, verify before any Actions arc) · the
Antigravity identity question (Gemini lane exclusion stands until answered) ·
[#494] ladder promotion, pegged to §6-spine close · [#495] cadence, rules
with [#385] · the ecosystem/*.yaml prose vs silent_rule_ratchet tension
(candidate row, twice-measured) · U-1..U-3 ARCHITECTURE contents ([#408] owns
the mechanism).

Q5 DECOMPOSITION RATIONALE. Phase 1→2→3 is ordered by force-multiplication:
Gemini's acceptance IS Phase 2's first deliverable (the ranked-sheet verdict
inputs), so activation precedes the shrink it accelerates; Grok is calendar-
gated (4.6, ≥08-07), not preference-gated; [#490] parity 9/9 precedes any
[#383] wave because fleet verdicts on 5/9 are theater. Do NOT redo: the flip
adjudication (8 open / 3 re-pegged / [#489]→[#218]) · the [#218] re-scope
posture · the [#480]/[#483] rulings and the canonical tally grammar · the
plan-of-record's R-A..R-D amendments · the retirement ranking R1–R4 with
never-auto-retire (binding on [#488]'s research contract; [#218] consumes
R1–R4 as its target list).

Q6 OFF-REPO CONTEXT. NC2: the operator's confirming word ("przeczytałem") on
the caches wave record §5.3 was designated two windows ago and NEVER landed on
record — the substance was presented in full both windows; re-present at boot
and collect it, do not treat presentation as discharge. The session
plan-of-record and this window's working files live in the operator's
Downloads (off-repo by design; handoff-dir immutable). Intake #24 was landed
verbatim from an off-repo package. The night batch ran in a cloud container
with recorded deviations (4× --no-verify with hooks run manually; shallow-
clone artifacts; uv version mismatch) — all described in the morning report,
none reproducible locally. No LLM-budget ceiling stands.

Q7 RATIFIED-IN-CHAT REGISTER (verbatim term · definition · durable home):
· "regen-hygiene rule" — a failure that is a mechanical consequence of the
  arc's own diff, where the gate prints its own named fix and that fix clears
  it with no disposition and no baseline touch, is not a third failure;
  anything outside that exact shape is a hard STOP → PLAYBOOK (verification
  §), candidate LESSONS.
· "retire-on-close / retire-on-flip disposition shape" — every disposition or
  exemption names its own expiry so it cannot outlive its reason → PLAYBOOK
  (disposition-register §).
· "canonical tally header" — the [#480] grammar (Tally C/H/M/L + Branch +
  HEAD + Model, forward-only) → PLAYBOOK via [#499] rider R2 (row-bound, do
  not file separately).
· "retirement ranking R1–R4 + never-auto-retire" — one graph, two orderings;
  high-centrality rows always get a human read → [#488] row body (research
  contract input).
· "fails-toward-silence" — the review-tool defect class where an over-broad
  suppression rule fails toward reporting nothing → LESSONS.
· "dirty-tree-as-honest-signal" — a pending curated-baseline decision leaves
  the tree visibly dirty rather than stashed, bypassed, or unilaterally
  baselined → LESSONS.

Assemble the v6 bundle with these answers; the SUCCESSOR-SUPPLEMENT file in
the operator's Downloads is companion context, not a bundle section. Trigger
the handoff.
