# Architect strategic supplement — 2026-06-17-dev-knowledge-architect-2

Repo: .dev-knowledge · Mode: architect · Date: 2026-06-17

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
A. **"File-oriented dependency management" as doctrine** — the coherence spine v1 (#172)
   is the *first* mechanism of the reframe you named in the prior bundle's filled supplement.
   Should the paradigm be elaborated as **named doctrine** (an ADR / a VISION or ARCHITECTURE
   thread), or stay an implicit organizing idea? And beyond the v1 single `reconciled_with` edge,
   which **coherence-by-memory failure classes** should it cover next (the priority order)?
B. **Coherence v2 trigger + the `/codex-review` vs `/code-review` reconcile** — v2's
   escape-hatch / deferred-hash / promote-nudge-to-gate decision is firing-rate-gated on
   `logs/coherence-nudge.log`; is there off-repo intent on which way to lean before the data
   accumulates? And the surfaced doc-vs-practice drift — PLAYBOOK §7 names `/codex-review` as the
   canonical pre-merge gate while the coherence feature's practice used `/code-review high` — which
   is canonical going forward?

===================== PASTE CHAT ANSWERS BELOW THIS LINE =====================
<!-- operator: paste answers here; combine multiple chats if needed; leave empty if there is no outgoing chat -->

Orientation for the incoming architect. This session took a 107-candidate brainstorm on dependency coherence and shipped one proven thing: coherence spine v1 (#172) — a narrow, complete, end-to-end slice on a single edge (dependent README ← spec HANDOFF_PROCESS, version-coupling). It is a proof-of-concept for a doctrine, not just a feature. Read these answers as a map of what was decided and why, so you extend a proven primitive deliberately rather than rebuild or relitigate it.
1. Strategic intent (way-of-working level).

Two goals, both methodology, neither a task. First: decide whether coherence-by-mechanism instead of coherence-by-memory becomes named doctrine (see A), and establish a cadence for adding mechanisms without sliding into maximalism. Second, harder: make the backlog genuinely load-bearing. This session shipped v1 to main three times before the backlog story even existed — the advisory gate nudged but never stopped us. You are the architect who drives from the backlog and delegates; freewheeling ("wolna amerykanka") is the anti-pattern to kill. Operate that for real, not nominally.
2. Tensions weighed + where we landed.

Maximalism vs narrow slice — 107 candidates, four visions. Landed narrow (one edge, the minimal Spine), deferred the rest. Reason: solo-dev constraint — the methodology must not outgrow the work; prove the mechanism before scaling.
The crux flip — I first believed the trigger (version-vs-hash) was the crux. The Council plus first-principles flipped it: the enumerator is load-bearing. The partial-update miss (walkthrough + diagram left stale) happens after the trigger fires — it is a completeness problem caught only by enumerating every reference site, not a detection problem. Do not re-elevate the trigger.
Version-coupling vs content-hash (DEC-01) — landed version-coupling (fires only on deliberate change, no over-firing on prose) plus a pre-commit nudge as a cheap forgotten-bump floor. Deferred the full content-hash floor until nudge data justifies it.
Deterministic vs AI — deterministic trigger + deterministic site-extraction + AI per-site verdict + human signature. The AI advises inside the gate; it never waives it.
Closure — the e2e mutation test (real injected drift → real checker fails → enumerator names the missed sites) is closure. Not green tests.
Review independence vs usage limits — leaned toward an independent lens at the pre-merge gate (codex caught 2 HIGH this session). See B.

3. Considered + rejected (do not relitigate).

The §16 do-not-build list stands: graph-DB for the methodology (killed empirically — grep was cheaper), a second task tool (two sources of truth), enterprise cross-tool ingestion (a solo dev is the curator), transclusion-everywhere (literate spaghetti), self-healing without human approval (ungrounded LLM drifts further), predictive-drift ML (no data advantage at solo scale), adopting any substrate platform / the Reactive Kernel (VISION-1) as a build target — study and borrow, do not migrate.
Dumping the raw brainstorm inventory into the repo — rejected. The architect distills it into an ADR; the brainstorm doc is off-repo input, not a repo artifact.
"The trigger is the crux" — rejected; the enumerator is load-bearing.
Forcing one regex for the deduped version parser — rejected; pin both behaviours, unify at the consumer layer, layer A's numeric validation, never bend a test.
Hand-closing #172 / freewheeling the backlog — rejected; the operator-gated closure loop owns it.

4. Open questions (unresolved / deferred).

The doctrine question (A) — name it or keep it implicit. Your first decision.
DEC-04 — lead with removal (transclusion/generation) or detection (gate)? We built detection first as the backstop; the split is unresolved.
DEC-03 — file-level vs element-level granularity; the stakes threshold for element-level is undecided.
DEC-07 — folder-level dependency contracts (_index.md); lean was rollup-over-files, folder-as-unit for high-stakes only.
Coherence v2 escape-hatch / deferred-hash / promote-nudge-to-gate — firing-rate-gated on logs/coherence-nudge.log; deliberately deferred until data (B).
§7 review-command canon + Codex auth mode — unresolved; lean given (B).
Which coherence-by-memory failure classes the spine covers next, and in what order (A).
#168 (backlog advisory → hard) — justified, depends on #170; sequencing open.

5. Decomposition rationale + what NOT to redo.

Shape: one organizing story (#172 = the spine), v1 as three sub-arcs (A checker / B enumerator / Integration), v2 as a deferred list. Reason: the spine is a general mechanism that several existing point-checks are instances of — #169 (canonical-doc staleness) reparents under it, #166 (task→ADR) reparents, #171 (dashboard) is its shared output surface, #170 (traceability) is a sibling. A and B were split for parallel build behind a clean Edge contract; Integration wired them. v1 narrow proves the mechanism; v2 scales, each item trigger-gated.

Do not redo or re-decide: the spine core (shipped and proven — build on it), DEC-01 for v1, the enumerator-is-load-bearing call, the deterministic/AI/human boundary, the §16 list. Do not reparent #169/#166 yet — deferred until ≥2 real drifts plus a #169-fit decision (a deliberate evidence-gate, not an oversight). Do not hand-close #172.

Critical hygiene, your first backlog action: the v2-deferred list currently lives inside #172's body. Extract those items into their own backlog IDs before closing #172, or the roadmap orphans on closure. (And reconcile this whole map against the live backlog — I can't see it from the browser.)
6. Off-repo context.

The brainstorm inventory (the 107 candidates, the full design-pattern catalogue, the do-not-build reasoning, the open decisions) is off-repo. The architect carries it by re-upload. Your first build task: distil it into an ADR and extract the active v2 items. It is also the record of what we chose not to build.
Codex pricing (researched here): Codex CLI is included in a paid ChatGPT plan if authed via ChatGPT sign-in (no extra money, draws plan limits); API-key mode bills per token (extra money). /code-review runs on Claude / your Max plan (no extra money). Confirm the auth mode before settling the review rule.
The methodology's own backlog discipline failed three times this session (shipped untracked → recovered via retroactive #172). That is the live case for #168 and the reason the architect wants the backlog genuinely load-bearing. The recurring spec↔practice drift in our own docs (§7, the pytest_collected count) is the same shape — the problem we are solving keeps appearing in our own process. Validating, not embarrassing.
Operating intent throughout: narrow-first, deliberate extension, the architect selects and decides — not dump, not maximise.

A. "File-oriented dependency management" as doctrine + next failure classes.

Name it — as an ADR, not a VISION. It is proven in miniature, and a proven mechanism earns a decision-record; a name gives the next mechanisms a coherent frame so v2 reads as "extending the paradigm" rather than ad-hoc feature-adding. Keep it an ADR (decision + principles + the v1 proof + the distilled roadmap), not a sprawling VISION — a VISION invites exactly the maximalism we just resisted. Bound it in the ADR: the doctrine is coherence-by-mechanism; deterministic trigger + AI judgment + human signature; graph-in-repo-not-model; narrow-first — and the do-not-build list is part of the doctrine, not separate from it.

Next failure classes, priority order (beyond the single reconciled_with edge):

More spec→dependent edges of the same type (other docs describing other specs) — just more declarations, proven mechanism, immediate value; includes scaling — generate the graph from frontmatter (SPINE-08), cross-repo (SPINE-09 / confirm #164 covers this).
Resolve DEC-04 and, for the highest-duplication content, remove the drift surface (transclusion) rather than detect it — the field's strongest claim; a bigger commitment, so gate it on the DEC-04 decision.
The forgotten / mis-classified bump (the false-negative the version edge can't see) — currently the nudge; promote to a content-hash floor if nudge data shows real misses.
Undeclared edges — dependencies that live in prose but aren't declared; AGENT-11 infers candidates for human confirmation.
Intra-file frontmatter↔prose drift (DET-16) and a whole-graph contradiction sweep (DET-11) — periodic, non-blocking.

You set the exact order; this is the shape.

B. Coherence v2 trigger lean + §7 reconcile.

v2 escape-hatch / deferred-hash / promote-nudge-to-gate: no off-repo intent should pre-empt the data — instrumenting the nudge is the decision mechanism. Hold it; do not let the next session build it speculatively. If forced to lean: promote-nudge-to-gate is the natural escalation if the nudge fires accurately and rarely; the escape-hatch and deferred-hash are the answer only if it proves noisy. Decide from logs/coherence-nudge.log.

§7 reconcile: this is not a cost decision — both are included if Codex is ChatGPT-authed. Lean: interim / small reviews → /code-review high (you're already in Claude); final pre-merge gate (3+ files) → /codex-review (independent GPT lens — it earned its place this session). Encode that graduated rule in §7, not a single command. Confirm Codex auth mode first; if it's API-key, codex costs extra → flip toward /code-review or switch the auth. And note the meta-point worth carrying: §7-vs-practice drift is itself a coherence instance — reconciling it is the doctrine in action.
