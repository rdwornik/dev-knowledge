# Handoff Stage 2: ai-council (session-sync)

**Slug:** 2026-05-18-ai-council-session-sync
**Repo:** ai-council
**Type:** session-sync
**Generated:** 2026-05-18

<!-- ROB: Instructions for Stage 2
1. Open the EXISTING (OLD) browser chat for ai-council — the chat being wrapped up.
2. Copy the paste block from stage1-question.md (everything after PASTE_BOUNDARY).
3. Paste as a message in the existing chat and wait for the response.
4. Replace everything below the ═══ marker with the old chat's response verbatim.
5. Save this file.
6. In Claude Code at .dev-knowledge, say: "complete handoff for ai-council"
-->

═══ REPLACE EVERYTHING BELOW THIS LINE ═══

### **1. OBJECTIVE**

This section assumes zero prior session knowledge.

The immediate goal of the next session is to create `AGENTS.md` at the ai-council repository root — the repository instruction file that OpenAI's Codex CLI reads — as the lead step in pivoting the project from provider-reliability work to closing its remaining documentation and hygiene gaps.

Recent work was dominated by a cascade of provider-reliability fixes: migrating off deprecated OpenAI research models, adding a research-panel degradation alarm, classifying API-credit exhaustion as a distinct error category, scoping the provider health gate to the active mode, and hardening the Perplexity research timeout. That reliability arc is complete and merged; no provider follow-up is required, and the repository is in a stable state. The priority therefore shifts from reactive provider hardening to the standing documentation and hygiene backlog. `AGENTS.md` is the highest-value item there. It is the Codex counterpart to `CLAUDE.md`: Claude Code reads `CLAUDE.md`, and OpenAI's Codex CLI reads `AGENTS.md` as its repository instructions. ai-council has a `CLAUDE.md` but no `AGENTS.md`, so Codex — which operates on this repository as a code reviewer — currently runs without its instruction file, on incomplete repository context. The purpose is concrete — Codex's instruction file — not abstract cross-tool governance.

Neither this nor the other remaining items are urgent — the next session has latitude to sequence them — but `AGENTS.md` should lead because it closes a known drift risk and is a clean, self-contained, completable task.

### **2. REALITY**

This section assumes zero prior session knowledge.

**Completed and merged to `main` during recent work (provider-reliability hardening):**

- OpenAI research providers were migrated off deprecated deep-research model identifiers onto current-generation models (exact identifiers live in repo config — Stage 3 verifies).
- A research-panel degradation alarm was added: when fewer than a configured minimum of research providers succeed, the run still completes but emits a loud aggregate banner and exits with code 3. Recorded as ADR-08.
- The health classifier gained a distinct billing error category, so an exhausted-API-credit failure surfaces clearly rather than as a generic error.
- The provider health gate was scoped to the active mode, so a mode that does not use a given provider family no longer blocks startup on that family's health.
- The Perplexity research provider timeout was raised from 60s to 240s, with an SDK-level single transient retry added.
- A brief-file naming-convention section was added to `council-question-guide.md` (the document explaining how to formulate council research briefs).

Working tree is clean; all of the above is merged.

**Unclosed thread (awareness only):** A `datetime.utcnow()` deprecation sweep was identified during a code review of the Perplexity work but not executed — no commit exists for it. It is carried as DIRECTIVE #2 below.

**Dependencies, stability, and constraints:**

- External providers in play: Perplexity, OpenAI, xAI/Grok, Google Gemini, DeepSeek, and Anthropic. Research-mode runs use the non-Anthropic providers plus a DeepSeek summarizer (architect inference on exact panel composition — Stage 3 verifies config).
- Anthropic credit constraint: during recent work the Anthropic API credit balance was exhausted, causing Anthropic-backed (debate-mode) providers to fail their startup health check. Research mode was unaffected because it uses no Anthropic providers. Current credit state is Unknown — verify; debate mode will not run until credits are available.
- The test suite was kept green through each fix via red-then-green discipline; current test count is Unknown — Stage 3 verifies against the repo.
- (architect inference) `main` may be ahead of `origin/main` with unpushed commits — push state Unknown, verify against the repo.
- No other unstable areas were observed; the provider reliability issues addressed during recent work are believed resolved.

### **3. RATIONALE**

This section assumes zero prior session knowledge.

Three pieces of reasoning from recent work shape the current state and should be understood before related code is touched.

**Why API-credit exhaustion is a distinct error category.** A debate-mode provider failure was traced to an exhausted Anthropic API credit balance, not a code defect. A generic error classification would have buried this and sent future debugging toward phantom code bugs. Classifying credit/billing exhaustion as its own category makes the real cause legible at a glance, so the operator knows to top up credits rather than chase code.

**Why the provider health gate is scoped to the active mode.** The startup health gate originally checked all provider families globally. Because research mode uses no Anthropic-backed providers, a global gate would block research-mode runs whenever the Anthropic providers failed their health check (e.g. on exhausted credits) — even though research mode does not need them. Scoping the gate to the active mode means each mode only health-checks the providers it actually uses; for research mode the only relevant check is the summarizer, and that is treated as a warning rather than a hard block, because a summarizer outage is non-fatal (the run degrades gracefully).

**Why the Perplexity research timeout is 240s.** A live reproduction measured a real research query completing in roughly 68 seconds — over the prior 60s ceiling, which was the actual cause of intermittent timeouts. 240s was chosen over a tighter value because: the measurement was a single data point with unknown variance in query times; a higher ceiling is nearly free, since research providers run in parallel and the timeout only has any effect when a provider genuinely stalls — costing at most about one extra minute on a rare hang, with the run still completing via the degradation handling; and Perplexity is a priority provider, so the bias is against false timeouts. An SDK-level single transient retry was added alongside, mirroring the pattern already used by the OpenAI research provider. Relatedly, the accompanying test asserts a `>= 120` invariant rather than the literal `240`: the regression worth guarding against is a revert to the too-tight 60s ceiling, not a future deliberate retune, and a literal-value assertion would conflate the two.

### **4. DIRECTIVES**

This section assumes zero prior session knowledge.

1. **Create `AGENTS.md` at the ai-council repository root.** `AGENTS.md` is the repository instruction file that OpenAI's Codex CLI reads — the Codex counterpart to `CLAUDE.md` (which Claude Code reads). Populate it with the conventions, build and test commands, and constraints Codex needs when operating on ai-council. Its content will overlap with `CLAUDE.md`, but the two must not become blind-copied, independently-drifting duplicates — decide deliberately which content is shared and keep a single source of truth for it. Verify: the repo file tree confirms `AGENTS.md` does not currently exist; after creation, `pre-commit run --all-files` passes.

2. **Replace deprecated `datetime.utcnow()` calls across the provider modules.** This emerged as a follow-up from recent provider work — a code review flagged a `datetime.utcnow()` deprecation warning in the Perplexity research provider and recommended a sweep across all debate and research provider modules (architect inference on the full file set — confirm by grep). Replace with the timezone-aware equivalent. Verify: the test suite passes and the deprecation warning no longer appears.

3. **Backfill `[scope: X]` tags in `LESSONS.md`.** `LESSONS.md` is the repo's append-only lessons log; some entries lack the `[scope: X]` tag required by the ADR-46 entry schema, producing an advisory audit warning. Verify: the ADR-46 dated-entry audit check resolves from WARN to clean.

4. **Verify hyphen filename compliance and `ARCHITECTURE.md` placement.** Run the repo's hyphen-convention check; migrate any non-compliant filenames; confirm placement of `ARCHITECTURE.md` (an architecture-overview document) against ADR-38. A prior audit indicated this is likely low-impact — fast-path if the check comes back clean. Verify: hyphen check passes; `ARCHITECTURE.md` placement matches ADR-38.

5. **Record the session's work in `JOURNAL.md`.** `JOURNAL.md` is the repo's session-by-session work journal; add an entry per its standard schema covering the directives completed.

### **5. BOUNDARIES**

This section assumes zero prior session knowledge.

- **Do NOT change provider timeout values or retry logic without re-establishing the empirical basis.** The Perplexity research timeout (240s) and its single transient retry were set from a live reproduction that measured a real research query at roughly 68 seconds. The accompanying test deliberately asserts a `>= 120` invariant rather than the literal `240` — this guards against a regression to the previously-too-tight 60s ceiling while permitting legitimate retuning. Do not "correct" that test to assert a literal value.

- **Do NOT refactor the billing error classifier or the mode-scoped health gate without reviewing their test coverage.** Red tests were written for both during recent work; changes that ignore them risk silently reintroducing the failures they fixed.

- **Do NOT treat `AGENTS.md` as abstract cross-tool governance, and do NOT make it a verbatim copy of `CLAUDE.md`.** `AGENTS.md` is specifically the instruction file OpenAI's Codex CLI reads; `CLAUDE.md` is the one Claude Code reads. Their content will overlap, but they must not become two independently-maintained copies that drift apart — keep shared content single-sourced.

- **Do NOT treat debate mode as code-broken if Anthropic-backed providers fail their health check.** The root cause observed during recent work was an exhausted Anthropic API credit balance, which the health classifier now surfaces as a distinct billing error. The remedy is an operator credit top-up, not code changes. Research mode is unaffected — it uses no Anthropic providers.

- **Do NOT re-tune the research-panel degradation alarm without consulting ADR-08.** The behaviour — a non-zero exit code (3) and an aggregate banner when fewer than the configured minimum number of providers succeed — is an intentional design decision recorded in ADR-08, not a bug.
