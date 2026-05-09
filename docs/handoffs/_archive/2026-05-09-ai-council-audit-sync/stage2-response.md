# Stage 2 Response: ai-council (audit-sync)

Slug: 2026-05-09-ai-council-audit-sync
Generated: 2026-05-09 (afternoon)
Architect source: existing ai-council architect chat (Browser-2, OLD)

<!-- Architect response begins below this line -->

### 1. OBJECTIVE

The next ai-council session should complete F-01 (VISION.md) and F-02 (lessons discovery configuration in CLAUDE.md). These are the only two P1 governance items. Session is docs-only — zero code changes, zero test changes. Done = VISION.md exists with correct schema, CLAUDE.md has DEV_KNOWLEDGE_PATH reference, config/settings.yaml committed clean, CHANGELOG and JOURNAL updated, 310/310 tests still passing. One session, under 45 minutes of Claude Code time.

I confirm the audit's suggested P1 actions are correct and sufficient. No revision needed.

### 2. REALITY

**Witnessed in this conversation:**

- ADR-38 structural migration was planned, prompted, executed, and merged in this chat. src/ → src/ai_council/ completed successfully with 310/310 tests passing. Key surprise: 56 mock.patch() string literals needed a second pass beyond import rewrites.
- Gemini was switched to default synthesizer (replacing Claude Sonnet 4.6 which timed out on 5-model transcripts). Witnessed the timeout error and the decision.
- Grok was added as 5th research provider (x_search + web_search tools via Responses API). Witnessed the implementation, the 400 error debugging (model string wrong), and the successful smoke test ($0.23, 1m06s).
- Citation parsing was fixed for both Grok (url_citation annotations in content blocks) and Gemini (markdown link regex from report text). Witnessed the 0-sources bug and the fix.
- Research display improved: Sources column moved to avoid truncation, error reasons shown in progress table.
- config/settings.yaml modification is intentional — Grok research timeout increased from 120s to 300s. Witnessed the timeout error that prompted this change. Safe to commit. Recommended message: `config: increase Grok research timeout to 300s`.
- Downloads auto-scan deployed with frontmatter detection (case-insensitive council keys). Witnessed the bug where files without frontmatter were silently skipped, and the fix to also detect files with "council" in the filename.
- council_inbox/ was incorrectly created in .dev-knowledge/ — witnessed the bug report. Fix was to resolve inbox path to repo root, not cwd. (architect inference) I believe the fix was committed but should be verified.
- council CLI entry point, --full as default, --lite flag — all implemented and verified in this conversation.
- OpenAI o4-mini-deep-research intermittently fails on complex queries but works on simple ones ("test question" succeeded at $0.02, 1m03s). This is an OpenAI-side issue, not our code. Witnessed multiple failures.

**Unknown — verify against repo:**

- Exact commit count ahead of origin/main. We never pushed in this conversation.
- Whether council_inbox/ creation fix was committed or only discussed.
- Exact content of config/settings.yaml diff beyond the Grok timeout change — there may be accumulated uncommitted changes from prior sessions.
- Whether --models flag filtering for research providers was implemented (we discussed it, prompt was given, but I did not witness confirmation of completion).

### 3. RATIONALE

**VISION.md tier — M, not L.** My reasoning:

- ai-council is a personal productivity tool for one developer. No team, no production users, no SLA, no uptime requirements. L implies infrastructure criticality that does not apply. (witnessed: every usage of ai-council in this chat was Rob running it locally from PowerShell.)
- 310 tests and 102K tokens look heavy on paper, but the core debate engine is relatively simple: parallel API calls, prompt assembly, blind voting shuffle, synthesis call. Most test volume is provider mocking and config validation. (architect inference based on writing prompts that touched these files.)
- Limited blast radius — if ai-council breaks, Rob loses a convenience tool. No data corruption risk, no dependent services, no customer impact. (witnessed: when providers timed out or errored, the only consequence was a degraded debate output, not a system failure.)
- However, ai-council IS the decision-making infrastructure for the ecosystem — Council debates produce binding ADRs that govern all other repos. This argues for M (not S) because the tool's output has downstream governance consequences even if the tool itself is low-criticality.

Recommend tier M with a note that tier may be revised upward if ai-council gains inbound API dependencies or automated pipeline integration.

**Lessons discovery (F-02):** ai-council has tasks/lessons.md with operational lessons. Witnessed entries being added during this conversation (mock.patch string literals, inbox path mirroring, interactive path). These are ai-council-specific — they describe provider API quirks, SDK gotchas, and code patterns unique to this repo. They should NOT migrate to .dev-knowledge LESSONS.md. The correct action: reference DEV_KNOWLEDGE_PATH in CLAUDE.md so future cross-cutting lessons CAN flow there, but keep existing entries local. Criteria: if a lesson applies only to ai-council code → stays local. If it applies to any repo doing package renames, provider integrations, etc. → copy to .dev-knowledge.

**config/settings.yaml:** witnessed change is Grok research timeout 120s → 300s. Grok with x_search + web_search tools timed out at 120s on a complex research query (witnessed the error output). First successful run took 1m28s. Safe to commit.

### 4. DIRECTIVES

1. Commit config/settings.yaml — message: `config: increase Grok research timeout to 300s`. Verify: `git status --porcelain` shows clean working tree. (architect inference: if the diff contains more than the timeout change, review before committing — there may be accumulated changes from prior sessions.)

2. Create VISION.md per ADR-33 schema. Content guidance based on witnessed project state:
   - Tier: M
   - Mission: Multi-model AI debate and research tool for architectural decision-making across the dev ecosystem.
   - Scope: 5 debate providers (Claude Opus 4.6, Gemini 3.1 Pro, GPT-5.4, Grok 4.20-beta, DeepSeek R1), 5 research providers (Perplexity sonar-pro, Gemini Deep Research, OpenAI o4-mini, Grok x_search+web, o3-deep), 4 modes (pick/ideas/judge/research with auto-detection), CLI entry point `council`.
   - Lifecycle: Feature-complete v1. Active maintenance. No planned major features. Incremental provider/model updates as landscape changes.
   - Relationships: Standalone. Called by other repos via `council` CLI or `scripts/council-ask.ps1`. No inbound code dependencies. Outputs transcripts to dual paths (ai-council/output/ + .dev-knowledge/docs/decisions/transcripts/).
   - Verify: file exists, frontmatter includes version/tier/owner/last_reviewed/scale, all required sections present, pytest -x passes.
   - COMMIT: `docs: create VISION.md per ADR-33 (tier M)`

3. Update CLAUDE.md for lessons discovery — add section referencing DEV_KNOWLEDGE_PATH env var per ADR-35. Include note: "ai-council-local lessons stay in tasks/lessons.md. Cross-ecosystem lessons go to $DEV_KNOWLEDGE_PATH/LESSONS.md." Also add one line noting future ADRs use underscore naming per ADR-34 (trivial, bundle with this step). Verify: CLAUDE.md contains DEV_KNOWLEDGE_PATH reference, pytest -x passes.
   - COMMIT: `docs: configure lessons discovery per ADR-35, note ADR naming convention`

4. Run `pytest -x` — confirm baseline holds. Verify: exit code 0, test count matches expected. (architect inference: count should be 310 but verify against actual output.)

5. Update CHANGELOG.md — entry dated today: VISION.md created (tier M), lessons discovery configured, Grok timeout committed. Update JOURNAL.md — 3-line entry (Did/Result/Next).
   - COMMIT: `docs: CHANGELOG + JOURNAL for governance session`

6. Fill 09_EXECUTION_EVIDENCE.md with command outputs from steps above. (Unknown — exact format defer to .dev-knowledge handoff bundle's 09_EXECUTION_EVIDENCE.md template.)

### 5. BOUNDARIES

- DO NOT create BACKLOG.md (F-03) — deferred until tier confirmed by .dev-knowledge recalibration
- DO NOT create ARCHITECTURE.md (F-04) — deferred until tier confirmed
- DO NOT rename existing 7 ADR files from kebab-case — grandfathered per ADR-29
- DO NOT push without Rob's explicit confirmation
- DO NOT address pre-existing ruff errors (17) or mypy errors (4) — out of scope, verified as identical to pre-migration main
- DO NOT make structural changes to src/ai_council/ — ADR-38 migration is complete and verified
- DO NOT migrate existing tasks/lessons.md entries to .dev-knowledge — they are ai-council-local operational lessons
- DO NOT change any provider code, model strings, settings, or debate/research logic — governance docs only
- DO NOT create or modify test files — baseline must hold at current count
- DO NOT change the default synthesizer (currently Gemini) or default panel (currently full 5-model) — these were deliberate decisions made in this conversation
- If `pytest -x` fails at any step: STOP, report failure details, do not continue — governance changes are docs-only and should never break tests
- If config/settings.yaml diff contains unexpected changes beyond Grok timeout: STOP, show diff to Rob, do not blindly commit accumulated changes
