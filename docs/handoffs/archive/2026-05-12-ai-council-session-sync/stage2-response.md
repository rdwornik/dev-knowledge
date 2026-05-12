# Handoff Stage 2 Response: ai-council (session-sync)

<!-- scope: meta -->

**Repo:** ai-council
**Type:** session-sync
**Slug:** `2026-05-12-ai-council-session-sync`
**Timestamp:** 2026-05-12
**Status:** AWAITING ARCHITECT RESPONSE

<!-- INSTRUCTIONS FOR ROB:
  1. Go to the EXISTING (OLD) browser chat for ai-council.
  2. Paste the content from PASTE_BOUNDARY to end of stage1-question.md.
  3. The old chat will answer the 5 questions (OBJECTIVE / REALITY /
     RATIONALE / DIRECTIVES / BOUNDARIES).
  4. Come back here and replace EVERYTHING below the thick line with the
     architect's response. Save.
  5. Then say "complete handoff for ai-council" in Claude Code (.dev-knowledge).
-->

### 1. OBJECTIVE

The next ai-council session's highest-priority action is **NOT what the .dev-knowledge BACKLOG shown in the handoff bundle suggests** — most of its P1/P2 items are stale relative to what was actually shipped this session.

The real immediate goal: **Step 5 smoke test execution** (operator-driven) — score current Gemini synthesizer on ~15 recent debate transcripts per `docs/synthesis-quality-rubric.md` to determine whether synthesizer refresh is justified or current configuration meets the bar at lower cost. This unblocks Step 6 (Phase 3 conditional ADR-01 amendment codifying the cost-optimization principle that emerged mid-session).

If next session is architect-focused rather than operator-focused: there is **no actively-blocked architect work**. AGENTS.md addition (P3, deferred per strażnik own "low urgency" framing) is the only carryover backlog item directly attributable to this session. The .dev-knowledge BACKLOG items shown require reconciliation against actual ai-council state before any of them should be executed.

What should be finished vs deferred:
- **Finish:** Step 5 smoke test (small, mechanical scoring exercise; unlocks Step 6)
- **Defer:** AGENTS.md (low urgency; bundle with future maintenance pass)
- **Defer:** ARCHITECTURE.md addition (optional at Scale M per ADR-38; CLAUDE.md Architecture section serves equivalent purpose unless scale escalates to L)

### 2. REALITY

**Witnessed work shipped this session (chronological by workstream):**

1. F-01/F-02 closure: VISION.md tier M created; DEV_KNOWLEDGE_PATH configured in CLAUDE.md per ADR-35
2. Cross-project transcript routing feature: `target-project` frontmatter + `--target-project` Click flag (`multiple=True`); `dev_root` + `target_projects` list schema in `config/settings.yaml`; `TargetResolver` in `routing.py`; fail-loud on unknown target at parse time
3. ADR-43 amendment cycle 1: schema refactor from `dict[name, full_path]` to `dev_root: str + target_projects: list[str]`; paths computed
4. Post-routing cleanup: `secondary_output_enabled` default flipped to `false`; code path retained for explicit opt-in
5. Docs hygiene sweep: `docs/HANDOFF.md` flat file deleted (handoffs are .dev-knowledge domain per ADR-42); `docs/archive/` consolidated into `docs/audits/`
6. ADR governance sweep: ADR-01 status date sync; ADR-02 Revised (3→5 model default); ADR-05 fix (3→4 providers, Grok added); ADR-06 Qwen close-out + reopen trigger; ADR-07 Superseded by ADR-43
7. AI Council debate on synthesizer/panel refresh: Option B unanimous (synth-only refresh, gated on smoke test); transcript routed to .dev-knowledge via target-project feature (first live use of routing on real meta-debate)
8. Cross-repo cycle 2 (ADR-34 universal hyphen mandate): CLI emitter `council_out_*` → `council-out-*` shipped; cycle closed on merge per .dev-knowledge final closure note (NO Turn 4 artifact, per operator principle established mid-session)
9. Phase 1 + ADR-34 combined merge: per-synthesis observability metrics (latency, transcript size, output tokens, error class), synthesis quality rubric created, ADR-06 Qwen close-out, Gemini version diagnostic (Case A vs B handled by Claude Code)
10. Scrum-master review main implementation (.dev-knowledge strażnik unilateral audit, single round trip): 9 of 10 findings; tasks/todo.md retired, BACKLOG.md created per ADR-41, README architecture + test count updates, ADR-34 filename violations fixed (including architect's own fresh violation `SYNTHESIS-QUALITY-RUBRIC.md` UPPERCASE), legacy `_CODE_REVIEW_REPORT.md` audits archived
11. Scrum-master review addendum (I7 + I8): `tasks/lessons.md` → root `LESSONS.md`; `tasks/` folder retired entirely; `docs/handoffs/_archive/` → `docs/handoffs/archive/`; M2 (LESSONS.md absent) superseded by I7

**Current state at handoff:**
- HEAD: `f094d08` (witnessed via operator paste; Stage 1 also verified)
- Working tree: clean
- Commits ahead of origin: ~74 (witnessed via operator running count; verify against repo)
- Tests: 362 passing (witnessed via Claude Code recap)

**Cycle status:**
- Scrum-master review (main + addendum): fully closed; no Turn 4 artifacts expected per single-round-trip principle
- ADR-43 cross-repo cycle 2: closed on merge per .dev-knowledge final closure (2026-05-11)
- No cross-repo handshakes currently in flight

**Critical staleness flag for handoff bundle BACKLOG** — the items shown in the handoff bundle from .dev-knowledge are significantly out of date:
- "Cross-repo handshake: ADR-34 amendment propagation to ai-council" → **ALREADY IMPLEMENTED** this session
- "ai-council hyphen migration" → **DONE** (CLI emitter changed, two doc files renamed, legacy archived)
- "ADR-38 Scale M gaps: LESSONS.md, BACKLOG.md" → **DONE** (I7 + I1 this session)
- "Handoff folder format adoption" → partially done (`_archive` → `archive` via I8; full ADR-42 folder pattern adoption Unknown — verify against repo)
- "docs/HANDOFF.md flat file deprecation" → **DONE** (deleted in docs hygiene sweep)
- "AGENTS.md" → still open (intentionally deferred per strażnik "low urgency")
- "VISION.md tier declarations" → tier M declared this session (architect inference: present in VISION.md frontmatter — verify)
- "Codify scrum-master review authority pattern" → N=1 instance just completed; codification still .dev-knowledge work

The .dev-knowledge BACKLOG needs reconciliation against actual ai-council git log + file state before any P1/P2 item is acted upon.

**Gaps witnessed/inferred:**
- Cost-optimization principle for synthesizer selection (correction made mid-session after Council debate) is **NOT YET CODIFIED in any ADR** — currently captured only in chat history + LESSONS.md entry (architect inference: visible in LESSONS.md given prompt design). Step 6 ADR-01 amendment is intended codification path.
- ARCHITECTURE.md absent at root — optional per ADR-38 at Scale M; not a gap unless scale escalates
- Step 5 smoke test pending operator execution

**External dependencies:**
- .dev-knowledge has its own pending Prompt K (their ~31 file rename migration) — independent, doesn't block ai-council
- .dev-knowledge A2 underscore-prefix-drop decision codification (their BACKLOG entry) — informs future ai-council audits but not blocking

**Constraints next session must respect:**
- Cross-repo handshake = 1 round trip; multi-turn = signal of badly framed request (operator principle established this session, supersedes 4-turn protocol from ADR-43)
- No timeline qualifiers in advice ("this week," "next session")
- Defer requires explicit justification
- No push to origin without explicit operator authorization
- Fast-forward merges only
- Cost-optimization principle: synthesizer selection prefers lowest-cost model meeting quality rubric

### 3. RATIONALE

**Synthesizer refresh — Option B over A/C (Council debate outcome):**
Council reached unanimous Option B (synthesizer-only refresh, panel unchanged) over Option A (no change) or C (panel + synthesizer). Reasoning: clean attribution. Option C introduced too many variables for evaluating quality changes. Option A ignored model landscape shift since defaults were established. Gated on smoke test rather than direct flip — operator has empirical evidence requirement before changing defaults.

**Cost-optimization mid-session correction:**
Council debate recommended Claude Opus 4.7 as synthesizer candidate without serious cost-benefit analysis. Operator caught the blind spot. Reframed Step 5 from "test Opus" to "score current first, escalate only if needed in cost order (Sonnet → GPT → Opus as last resort)." This is significant — Opus tier costs ~5-10x current Gemini per synthesis run. Council's recommendation inherited a quality-first frame without questioning cost. Worth preserving for Step 6: synthesizer selection prefers lowest-cost model meeting quality rubric; Opus reserved as last resort.

**Combined Phase 1 + ADR-34 in single Claude Code prompt:**
Considered splitting into two prompts (different concerns, cleaner audit trail). Discarded because operator was explicit about ceremony fatigue. Combined was 8 commits clean, single merge, less paste-back overhead. Worked.

**Operator principle on cross-repo handshakes — supersedes 4-turn protocol:**
ADR-43 amendment process I helped establish in cycle 1 specified 4-turn protocol (proposal → approval → closure → delivery report). Cycle 2 retroactively confirmed this was over-engineered for S-scale changes. Operator stated sharper principle mid-session: "A cross-repo handshake = one round trip. Multi-turn = signal of badly framed request, not protocol depth signal." This supersedes scale-by-impact tier framing from cycle 1. .dev-knowledge will codify in BACKLOG Cross-stream P2. Cycle 2 closed on merge with no Turn 4 artifact.

**Single-round-trip principle applied to scrum-master review:**
.dev-knowledge strażnik produced unilateral audit (no bilateral handshake). Single round trip. Architect implements where agrees; pushes back as separate new conversation if disagrees. Worked. N=1 empirical instance for the pattern.

**Lesson A — local-config defense as architect failure mode:**
Strażnik's original audit accepted `tasks/lessons.md` as "by-design per CLAUDE.md Lessons Discovery" without checking ecosystem convention. Operator caught it post-implementation. When operator pointed it out, I (architect) defended same way — reproduced exact same failure mode. Strażnik addendum codified Lesson A. Architect-side symmetric lesson appended to LESSONS.md. Significant pattern: when convention divergence is flagged, default response must be "evaluate against ecosystem baseline," not "intentional per local config."

**Almost did but discarded:**
- Almost generated handoff at premature point — operator overrode ("I have my own method")
- Almost framed smoke test as Opus-first — operator corrected toward cost-tier escalation
- Almost defended tasks/lessons.md location as intentional — strażnik addendum corrected via I7

### 4. DIRECTIVES

The default proposal in the handoff prompt (implement ADR-34 CLI migration, add LESSONS.md/BACKLOG.md, etc.) is **stale** — these are already done. Revised directive sequence:

1. **Reconcile .dev-knowledge BACKLOG against ai-council actual state.** Cross-check each P1/P2 BACKLOG item (shown in handoff bundle) against ai-council git log + current file state; produce reconciliation report flagging which items are already complete (most), which remain open (AGENTS.md, ARCHITECTURE.md optional, codify scrum-master review authority N=2 trigger). Verify: reconciliation artifact produced and routed back to .dev-knowledge browser chat for their BACKLOG cleanup.

2. **Step 5 smoke test execution (operator-driven).** Score CURRENT Gemini synthesizer output on ~15 recent debate transcripts in `output/` per `docs/synthesis-quality-rubric.md` 5-point checklist. Aggregate pass rate per criterion. Verify: scoring artifact captures per-transcript pass/fail per criterion; aggregate decision (≥80% pass → no flip recommended; <80% → cost-tier escalation triggered).

3. **Step 6 Phase 3 conditional implementation** (gated on Step 5 data). If Step 5 passes: formal Claude Code prompt for ADR-01 amendment recording Council debate + smoke test data + **cost-optimization principle codified** ("synthesizer selection prefers lowest-cost model meeting quality rubric; Opus tier reserved for last resort"). If Step 5 fails: separate escalation test session in cost order (Sonnet → GPT → Opus). Verify: ADR-01 amendment merged; cost-optimization principle present in governance docs; BACKLOG P1 entry closed.

4. **AGENTS.md addition** (P3, BACKLOG-tracked). Reference ADR-28 + PLAYBOOK AGENTS.md template (.dev-knowledge has the template). Low urgency; bundle with future maintenance cycle or do standalone in light session. Verify: file present at root; canonical cross-tool governance points to it (Codex, Cursor, Aider operating contexts referenced).

5. **Push to origin** (operator timing decision). ~74 commits ahead at handoff (architect inference: number grows each session; backup risk grows with it). Verify: `git push` to remote; commits-ahead count drops to 0.

(Architect inference) on directive specifics: action 1 reconciliation report format is undefined — likely a simple markdown artifact routed via paste-back to .dev-knowledge. Stage 3 should verify whether .dev-knowledge expects a specific format.

### 5. BOUNDARIES

**Do NOT:**

- Execute .dev-knowledge BACKLOG items as written without first reconciling against ai-council actual state — most P1/P2 items are stale (ADR-34 CLI migration, BACKLOG.md creation, LESSONS.md addition, HANDOFF.md flat file deletion, `_archive` rename) ALREADY DONE this session
- Force synthesizer flip to Claude Opus 4.7 based on Council debate alone — Council recommendation had cost-optimization blind spot caught mid-session by operator; smoke test (Step 5) must be cost-tier-aware (test current first; escalate only if needed in cost order: Sonnet → GPT → Opus as last resort)
- Codify any cross-repo handshake protocol requiring >1 round trip — operator principle established this session: well-formed requests close in one round
- Defend "local config" or "by-design per CLAUDE.md" as justification when convention divergence is flagged — Lesson A applies symmetrically to architect; default response must be "evaluate against ecosystem baseline"
- Create artifacts following 4-turn cross-repo protocol — superseded by single-round-trip principle
- Generate Turn 4 delivery reports for routine cross-repo cycle completion — git log + CHANGELOG = sufficient audit trail
- Push to origin without explicit operator authorization
- Touch files in `.dev-knowledge` repo from ai-council architect role (boundary discipline: ai-council work in ai-council; .dev-knowledge work routes via artifacts to .dev-knowledge browser chat)
- Add timeline qualifiers to recommendations ("this week," "next session," "end of day," "heavy-work window")
- Pre-emptively flag context degradation based on message count rather than measurable quality issues (per operator preference)
- Skip Codex `/review` on formal-prompt-scale PRs (3+ files per Playbook §15)
- Use UPPERCASE letters in any new filenames — ADR-34 = lowercase + hyphens; ADR prefix grandfathered. Architect's own fresh violation this session (`SYNTHESIS-QUALITY-RUBRIC.md`) is empirical evidence the convention is easy to slip on; double-check during prompt drafting
- Combine ADR amendment work with feature shipping in same prompt without clear section separation — governance changes deserve their own commits for audit-trail clarity (even when combined-prompt approach is taken to reduce ceremony)
- Treat any .dev-knowledge methodology proposal (e.g., ADR audit step in formal-prompt template) as ai-council work — those route to .dev-knowledge browser chat

**Fallback contingencies:**

- If Step 5 smoke test scores are inconclusive (e.g., ambiguous quality, pass rate near threshold): expand sample size (30 transcripts instead of 15) before escalating to higher-cost tier
- If Codex `/review` surfaces a blocker requiring `.dev-knowledge` input mid-implementation: opens new cross-repo conversation (different handshake from routine completion; not part of single-round-trip cycle)
- If new feature work surfaces ADR drift mid-PR: invoke ADR audit step inline (methodology proposal pending .dev-knowledge decision); architect judgment call until proposal accepted
- If .dev-knowledge BACKLOG reconciliation surfaces disagreement (e.g., they show item complete that ai-council shows still open, or vice versa): produces a new cross-repo conversation; do not auto-resolve unilaterally
- If operator declares scope creep mid-session: stop, summarize completed work, propose handoff or scope contraction per single-round-trip principle (not multi-turn deepening)
