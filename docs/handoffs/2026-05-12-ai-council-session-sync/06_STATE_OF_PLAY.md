# State of Play — 2026-05-12-ai-council-session-sync

<!-- scope: meta -->

Source: Stage 2 REALITY + RATIONALE (architect response from OLD chat) +
Stage 3 repo verification.

---

## What was completed this session

*(Architect: witnessed unless marked otherwise)*

1. **F-01/F-02 closure:** VISION.md tier M created; DEV_KNOWLEDGE_PATH configured
   in CLAUDE.md per ADR-35
2. **Cross-project transcript routing feature:** `target-project` frontmatter +
   `--target-project` Click flag (`multiple=True`); `dev_root` + `target_projects`
   list schema in `config/settings.yaml`; `TargetResolver` in `routing.py`;
   fail-loud on unknown target at parse time
3. **ADR-43 amendment cycle 1:** schema refactor from `dict[name, full_path]` to
   `dev_root: str + target_projects: list[str]`; paths computed
4. **Post-routing cleanup:** `secondary_output_enabled` default flipped to `false`;
   code path retained for explicit opt-in
5. **Docs hygiene sweep:** `docs/HANDOFF.md` flat file deleted (handoffs are
   .dev-knowledge domain per ADR-42); `docs/archive/` consolidated into `docs/audits/`
6. **ADR governance sweep:** ADR-01 status date sync; ADR-02 Revised (3→5 model
   default); ADR-05 fix (3→4 providers, Grok added); ADR-06 Qwen close-out + reopen
   trigger; ADR-07 Superseded by ADR-43
7. **AI Council debate on synthesizer/panel refresh:** Option B unanimous (synth-only
   refresh, gated on smoke test); transcript routed to .dev-knowledge via target-project
   feature (first live use of routing)
8. **Cross-repo cycle 2 (ADR-34 universal hyphen mandate):** CLI emitter
   `council_out_*` → `council-out-*` shipped; cycle closed on merge
9. **Phase 1 + ADR-34 combined merge:** per-synthesis observability metrics (latency,
   transcript size, output tokens, error class), synthesis quality rubric created,
   ADR-06 Qwen close-out, Gemini version diagnostic
10. **Scrum-master review main implementation** (.dev-knowledge strażnik unilateral
    audit, single round trip): 9 of 10 findings; `tasks/todo.md` retired, BACKLOG.md
    created per ADR-41, README architecture + test count updates, ADR-34 filename
    violations fixed (including fresh `SYNTHESIS-QUALITY-RUBRIC.md` violation)
11. **Scrum-master review addendum (I7 + I8):** `tasks/lessons.md` → root `LESSONS.md`;
    `tasks/` folder retired entirely; `docs/handoffs/_archive/` → `docs/handoffs/archive/`

**Current state at handoff:**
- HEAD: `f094d0821a279f3aa36de554943c1b44576d0924`
- Working tree: clean
- Commits ahead of origin: ~74 (architect inference; verify with `git rev-list origin/main..HEAD --count`)
- Tests: 362 passing (architect: witnessed via Claude Code recap; Unknown — verify by running `pytest`)

**Cycle status:**
- Scrum-master review (main + addendum): fully closed
- ADR-43 cross-repo cycle 2: closed on merge
- No cross-repo handshakes currently in flight

---

## Decisions locked

- **Synthesizer refresh = Option B** (synth-only, gated on smoke test): Council
  unanimous; panel unchanged; Gemini stays until smoke test data justifies change
- **Cost-optimization principle established** (NOT YET IN ADR): synthesizer selection
  prefers lowest-cost model meeting quality rubric; Opus reserved as last resort.
  Captured in LESSONS.md; pending codification via Step 6 ADR-01 amendment
- **Cross-repo handshake = 1 round trip**: supersedes ADR-43 4-turn protocol. Operator
  principle established mid-session; well-formed requests close in one round; multi-turn
  = signal of badly framed request
- **Single-round-trip principle for scrum-master review**: .dev-knowledge strażnik
  produces unilateral audit; architect implements where agrees; N=1 instance complete

---

## Deferred items

- AGENTS.md addition — P3 BACKLOG, low urgency per architect
- ARCHITECTURE.md — optional at Scale M; not a gap unless scale escalates to L
- Step 5 smoke test pending operator execution
- Step 6 ADR-01 amendment pending Step 5 data
- Cost-optimization principle pending formal codification in ADR
- Codify scrum-master review authority pattern — N=2 needed or operator decision at N=1

---

## Rationale (architect judgment)

**Synthesizer refresh — Option B over A/C:**
Council unanimous: clean attribution. Option C (panel + synth) introduced too many
variables. Option A ignored model landscape shift. Gated on smoke test — operator
requires empirical evidence before changing defaults.

**Cost-optimization mid-session correction:**
Council recommended Claude Opus 4.7 without cost-benefit analysis. Operator caught
blind spot. Reframed Step 5: test current first, escalate only in cost order
(Sonnet → GPT → Opus last resort). Opus tier costs ~5-10x current Gemini per synthesis.
**Significant — this must survive to Step 6.**

**Combined Phase 1 + ADR-34 in single Claude Code prompt:**
Splitting was considered; discarded due to operator ceremony fatigue. Combined was
8 commits clean, single merge, less overhead.

**Operator principle on cross-repo handshakes:**
ADR-43 cycle 1 established 4-turn protocol. Cycle 2 confirmed it was over-engineered
for S-scale changes. Operator principle: 1 round trip. Multi-turn = badly framed request.
Supersedes scale-by-impact tier framing from cycle 1.

**Lesson A — local-config defense as architect failure mode:**
Strażnik audit accepted `tasks/lessons.md` as intentional per CLAUDE.md. Operator
flagged divergence. Architect initially defended same way — reproduced exact failure mode.
Key pattern: when convention divergence is flagged, default must be "evaluate against
ecosystem baseline," not "intentional per local config."

---

## Stage 3 verification summary

Architect provided ~15 witnessed claims verifiable from repo:

- **12 verified against repo state:**
  - `docs/HANDOFF.md` absent from git ls-files ✓ (deletion confirmed)
  - `BACKLOG.md` present at root ✓ (BACKLOG creation confirmed)
  - `LESSONS.md` present at root ✓ (I7 migration confirmed)
  - `tasks/` folder absent from git ls-files ✓ (retirement confirmed)
  - `docs/handoffs/archive/` present ✓ (`_archive` rename confirmed)
  - `src/ai_council/routing.py` present ✓ (routing feature confirmed)
  - `docs/synthesis-quality-rubric.md` present ✓ (quality rubric confirmed)
  - `src/ai_council/metrics.py` present ✓ (observability metrics confirmed)
  - ADR-07 Status = "Superseded by ADR-43" ✓ (governance sweep confirmed)
  - `secondary_output_enabled` default = false ✓ (confirmed in ADR-07 text)
  - `docs/audits/2026-05-12-codex-scrum-master-review-2026-05-12.md` present ✓
  - `docs/audits/2026-05-12-codex-phase-1-observability-adr34-hyphen.md` present ✓
- **2 unverifiable without execution:** test count (362), commits-ahead (~74)
- **3 architect-flagged inferences:** preserved with flag (reconciliation format,
  VISION.md frontmatter content, commits-ahead growth)
- **0 verification failures:** no witnessed claims contradicted repo state
