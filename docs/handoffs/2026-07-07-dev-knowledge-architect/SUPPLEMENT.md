# Architect strategic supplement — 2026-07-07-dev-knowledge-architect

Repo: .dev-knowledge · Mode: architect · Date: 2026-07-07

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

SUPPLEMENT ANSWERS — outgoing architect (Fable 5 browser chat), 2026-07-06/07

Q1 — Strategic intent
A RATIFICATION session (plan-first/design): turn drafted proposals into
ratified methodology, then clear the decision queue. (a) INTAKE PROCESS —
ratify the functional->technical-architect->epic-chat pipeline; the
drafts-branch proposal is SUPERSEDED-IN-PART by two operator intake briefs
(uploaded at boot): brief #1 (functional-architect scene + nightly proposal
loop) is the matured intent and is itself intake-doc-#1 by its own AC-5
(dogfood the triage on it). (b) EPIC-NAMING: draft rec Track-X now /
story-map migration at P6. (c) AUDIT-RETENTION: rec keep-all + age-tiered
index, one ADR folding #212. THEN the queue: P6 fleet-roll WAIT-lift
(all four gates closed + independently verified; decision = lift + pick
first n=2 consumer, corp-monorepo is the natural candidate, vs record a
reasoned hold) · #267 attended-run mechanism (LEAN recorded: iii
instruct-the-child for n=1; ii discover-from-config at fleet scale) ·
changelog flags A1/A2/V1 · Fable-5 tier in the routing doctrine (pending
since 06-15, zero build cost; weeks of empirical Fable use incl. this
architect arc). Sequencing is deliberate: intake BEFORE P6 — P6 is the
first big consumer of the new pipeline; ai-council deployment/conformance
work (References coupling, relative paths, A2 contradiction,
settings.local.json) is ADR-41-routed to its dedicated chat AFTER
ratification, so fixes land on a ratified convention, not a draft.

Q2 — Tensions weighed
(1) One-chat role-progression (drafts branch) vs separate --mode functional
+ minimal boot (brief #1): architect lean = brief supersedes (operator's
matured intent; solves "where do requirements come from" structurally);
adjudicate with both artifacts on the table. (2) Nightly loop: revived ONLY
under brief #1 §6 constraints — every routine names its CONSUMER + survival
metric ex-ante (fleet-audit lesson: 61 baselines, zero readers), cap ~5
proposals/night, 7-day auto-expiry, load-gauge first, night executes
pre-authorized contracts / judgment sleeps. (3) Buy-vs-build (brief #2):
adopt native platform features where they DELETE our scaffolding; the
governance layer (boundaries, frozen contracts, §14, closure discipline)
is the value-add and stays ours. (4) Enforcement-proven vs
fully-conformant: ai-council is the former, not the latter — the explicit
distinction now governs consumer claims.

Q3 — Considered + rejected (do not relitigate)
Separate proposals/ folder (SEEDs live in intake/) · raw transcript storage
(converted intake doc only) · a separate nightly audit routine (rot-report
IS the nightly audit once built) · Task-Scheduler auto-resume (failed in
practice; any re-automation is a fresh design) · armed-as-enforcing as
doctrine (REJECTED; #267 witnesses FIRED) · hand-copied mesh transfer ·
pre-ratifying the intake briefs into BACKLOG from chat (would split truth
and kill the AC-5 dogfood).

Q4 — Open questions
Brief #1 §8 set (transcript storage confirmed rejected; MoSCoW vs
must/should/could at build; nightly-pass model cost check; functional-boot
probes — lean none) + brief #2 §7 set (Routines trust boundary;
Outcomes rubric home; /batch-under-governance make-or-break; auto-mode
vs deny-first floor — reconcile or reject, never both silently; which
G-batch workarounds the Week-26 subagent-permission change obsoletes) +
R2: whether #119 (codex Windows SQLite fix, only ADOPT of the 06-07
window) was ever executed — status unknown, a month old.

Q5 — Decomposition rationale (do not redo)
Ratify intake -> then P6 (pipeline before its first consumer). Brief #1's
acceptance criteria ARE the build epic's UAT verbatim (blueprint=intake,
implementation=epic lanes, UAT=EPIC RETURN, go-live=root merge). Stage-3
adjudication, fold FLAG (#168/#170 co-seq #239/#240, #139 separate), E1
deviation, mission closure on hard metric — all ADJUDICATED and archived
in JOURNAL 2026-07-07; do not reopen. The four P6 gates are closed AND
independently verified (read-only pass @ 07a0d40) — the WAIT decision
needs no further evidence gathering.

Q6 — Off-repo context + honest ledger
Two intake briefs arrive as .md uploads at the incoming session's boot
(operator holds them at Downloads\intake-brief-functional-architect-
nightly-loop.md + intake-brief-platform-feature-scan.md); NOT committed —
intake/ folder creation is itself a ratification outcome (new-folder
approval rides it). A parallel operator /changelog-review arc ran during
the wrap (digest committed 2026-07-06-changelog-review.md; cc
2.1.177->2.1.201, codex ->0.142.5; flags A1/A2/V1 queued). Branch hygiene
done (wrap + changelog branches deleted; drafts + fleet-audit intact).
PROCESS NOTE: the supplement-fill step was skipped before /handoff ran —
the bundle was cut cold and this fill happened via the QUESTIONS flow
afterward; incoming §13(d) beat should NARROW to "anything changed since
this fill?". Overnight mission + verification + wrap all ran with zero
envelope violations; three self-report defects caught by mechanism
(CLOSED-count inflation, drafts commit-count, stale branch-deletion claim)
— trust the probes, not the summaries. System-date skew (clock 07-06,
artifacts 07-07) is benign and precedented. This arc ran on Fable 5 —
empirical input to the Fable-tier decision. No LLM-budget ceiling.

ADDENDUM (outgoing architect self-review, same fill):
- Q1/P6 precision: the P6 call is TWO decisions — (1) WAIT-lift + first n=2
  consumer pick, AND (2) carrier-vs-current-manifest: the #262 deploy
  carrier was REJECTED overnight per the [NB-1] INERT-on-tagged-manifest
  precedent and explicitly deferred TO this decision (a carrier requires a
  v1.3.0 release arc + child re-verification; rolling with the current
  manifest avoids it). Decide both together.
- Q1/naming routing: ratification picks the convention; the Track-X rename
  itself EXECUTES in ai-council's dedicated chat (ADR-41), never from hub.
- Q4/gating: A1 (pinned-model refresh) is GATED on V1 (deprecation check
  on claude-sonnet-4-6); V1 execution status UNKNOWN at fill time — if no
  V1 verdict is on record, run it read-only at session start before
  deciding A1. R2 (#119 codex fix status) likewise unverified.
