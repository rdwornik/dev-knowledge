# Audit — Codex-maximization: releases + docs vs our review workflow

**Date:** 2026-06-07 · **Type:** read-only analysis (report persisted post-hoc) · **Session:** terminal B (Opus/high) · **Status:** actionables captured to BACKLOG via `docs/audit-trio-capture`; effort raise + currency item queued.

---

**Bottom line:** We use Codex correctly and within doctrine — `codex exec --sandbox read-only` + global `~/.codex/AGENTS.md` are all current canonical spellings. Two real gaps: we run reviews at **medium** reasoning effort when high/xhigh is available on our tier and is OpenAI's documented deep-review setting, and we're one stable release behind (0.136.0 vs 0.137.0, which carries a Windows SQLite stability fix). Everything else is either already-correct, doctrine-forbidden, or cost > gain for a solo operator.

## COVERAGE

- Releases: 100 GitHub releases mined, span rust-v0.122.0 (2026-04-20) → rust-v0.138.0-alpha.6 (2026-06-06); 14 stable, ~68 empty-body alphas.
- Docs pages: 20 authoritative SPA pages fetched + cleaned (config-reference, config-basic, config-advanced, cli, cli/reference, cli/features, models, sandboxing, auto-review, guides/agents-md, memories, subagents, workflows, permissions, sdk, hooks, feature-maturity, noninteractive, slash-commands, changelog?type=cli).
- Reader passes: 4 artifact-reader subagents (config/cli/models; review/automation; GitHub releases; curated CLI changelog).
- Compression: 31 MB raw fetched → 730 KB chunked to readers → 4 structured summaries surfaced in main thread (raw never entered it).
- Sources unreachable: none. (Repo docs/*.md are stubs; real docs are the SPA site — used the site.)

## CORRECTION TO THE PROMPT'S STATED BASELINE

The prompt listed "exec/non-interactive mode" and "sandbox modes" as "NOT used today." They ARE used: the wrapper (`~/.claude/bin/codex-review.ps1:165`) runs `codex exec --sandbox read-only --output-last-message <file> -`. So our single pattern already = non-interactive exec + read-only sandbox + stdin-piped prompt. Model/effort is set GLOBALLY in `~/.codex/config.toml` (gpt-5.5 / medium), not per-invocation — "defaulted at call time," not "unconfigured."

## CURRENCY VERDICT

**(1) INSTALLED vs LATEST** — Installed: codex-cli 0.136.0 (2026-06-01). Latest stable: 0.137.0 (2026-06-04) → ONE stable behind. version.json self-reported 0.136.0 as latest on 2026-06-03; 0.137.0 shipped the next day. Worth updating: 0.137.0 carries a Windows-x64 SQLite stability fix (#25490, prevents silent crashes on our platform) and "preserve auto-review approval policy in codex exec" (#23763). Sanctioned update path: `codex update` (self-update, added 0.128.0) OR installer/npm. REPORT-ONLY — not updated this session.

**(2) REVIEW MODEL / EFFORT ← the one real underuse** — Model: gpt-5.5 = current & correct (catalog: gpt-5.5 / gpt-5.4 / gpt-5.4-mini / gpt-5.3-codex-spark [Pro-preview]); no deeper codex-branded variant exists. Stay on gpt-5.5. Effort: we run "medium". Tiers are minimal|low|medium|high|xhigh. CONFIRMED our auth tier offers high AND xhigh (models_cache.json). OpenAI's own docs demonstrate a "deep-review" profile at xhigh on gpt-5.5 (config-advanced). For a post-implementation bug-finding reviewer, medium is under-powered. → RAISE review effort to high (or xhigh). Highest-leverage change in this audit.

**(3) AGENTS.md SEMANTICS — assumption HOLDS** — Global ~/.codex/AGENTS.md is still discovered FIRST (before project files); `project_doc_fallback_filenames=["CLAUDE.md"]` still honored. Repo↔global AGENTS.md are byte-identical except line endings (repo CRLF, global LF) — content match confirmed. New since last look: AGENTS.override.md outranks AGENTS.md at each level (we have none — fine); 32 KiB project_doc_max_bytes cap (our ~4 KB global + CLAUDE.md well under — no truncation risk).

## FIVE BUCKETS (post-skeptic)

**UNDERUSED-NATIVE**
- Reasoning effort high/xhigh — `model_reasoning_effort` ∈ {…,high,xhigh}; stable on gpt-5.5/Responses API. We pin medium. COMPLEMENT (deepens existing organ, read-only-safe). Mechanisms: (a) per-call `-c model_reasoning_effort=high` on the wrapper's exec line (simplest; global stays medium for interactive); (b) profile: ~/.codex/deep-review.config.toml + `--profile deep-review`.
- `--ephemeral` — suppresses session-rollout persistence; clean slate per review run. Doctrine-safe, near-zero cost. COMPLEMENT to wrapper.
- Output-hygiene keys for a review profile — hide_agent_reasoning=true, model_reasoning_summary="none|concise", web_search="disabled" (smaller attack surface, cleaner --output-last-message). COMPLEMENT, bundle only if a profile is created.

**ADOPT**
- Update 0.136.0 → 0.137.0 (Windows SQLite fix #25490 + exec approval-policy preservation). Home: small currency item + ENVIRONMENT version row.
- Raise review reasoning effort (above). Best home: BACKLOG #82 (per-repo review profiles).

**STALE-NAMES — CLEAN**
- Live/maintained surfaces (PLAYBOOK, ESSENTIALS, codex/AGENTS.md, .claude/commands, codex-review.ps1, codex-review.md, config template) carry NO dead names; wrapper uses all-current spellings.
- Only hits, all benign/non-actionable: ~/.codex/config.toml:14 "gpt-5.2-codex"="gpt-5.4" ← Codex's OWN auto-written [notice.model_migrations] block; LESSONS.md:109 / JOURNAL.md:1782 — append-only history of the ALREADY-FIXED stale gpt-5.2-codex pin; docs/archive/* and transcripts — immutable history. No edits warranted (append-only/immutable forbid them anyway).

**VERIFY**
- xhigh actually engages on a real review: `codex exec --sandbox read-only -c model_reasoning_effort=xhigh -o out.md - <<< "Review this diff: main..HEAD"` (throwaway repo; confirm no auth-tier error).
- Memories stay OFF on any automated path: confirm no `[features] memories=true` and no `memories.use_memories=true` in ~/.codex/config.toml. Today: absent = safe.
- auto-review model-override key name (#23767, 0.137.0) — name not in docs yet; moot for us (approval_policy implicitly "never" via non-interactive exec → auto-review structurally bypassed).

**NOISE** — ~68 empty-body alpha pre-releases; dozens of UI/perf/bugfix commits; TUI-only ergonomics (Alt+,/Alt+. effort toggles, /skills picker). Counted, not carried.

## SELF-SKEPTIC KILL LIST — 8 kills

1. Auto-review / guardian (approvals_reviewer="auto_review") — KILL: LLM approval gate, non-deterministic by OpenAI's own admission; violates ADR-74/ADR-76; AND moot — non-interactive exec has no approval prompts.
2. Native /review command — KILL: TUI-only, cannot be invoked via codex exec; interactive convenience, not a wrapper replacement.
3. @codex review (GitHub PR) — KILL: cloud surface, repo feature-enable required; duplicates the local pre-merge organ; adds cloud dependency to a local-first solo workflow.
4. Read-only reviewer SUBAGENT (.codex/agents/reviewer.toml) — KILL: needs orchestrating parent; complexity > gain for a single pass.
5. spawn_agents_on_csv per-file bulk review — KILL: EXPERIMENTAL (maturity risk); premature.
6. Codex SDK (Python/TS, Sandbox.read_only) — KILL: requires local app-server; heavier than codex exec; no solo-operator gain.
7. Hooks as a write-prevention gate — KILL: docs say PreToolUse is "not a complete enforcement boundary"; --sandbox read-only is the real boundary; a hook gate adds false assurance.
8. --ignore-rules / --ignore-user-config — KILL: premature; no conflicting .rules/user-config exist.

## DEPRECATED-KEY WATCH (for whenever config IS touched — none present today)

experimental_instructions_file→model_instructions_file (removed 0.131); [profiles.NAME] inline → separate $CODEX_HOME/NAME.config.toml (0.134); --profile-v2→--profile (0.134); --full-auto→explicit --sandbox (dep. 0.128); approval "on-failure"→"never"/"on-request"; persist_extended_history (removed 0.137). Our config/wrapper use NONE of these. ✓

## CONFIRMATION

ZERO repo changes; git status --porcelain → 0 lines · branch main · temp dir (31 MB) deleted + removal verified. ~/.codex/ untouched; no Codex update performed (report-only).

**One-action takeaway:** add `-c model_reasoning_effort=high` to the wrapper's codex exec line (or create a deep-review profile) — the single change that materially improves the heterogeneous reader, fully read-only-safe. Version bump to 0.137.0 = nice-to-have (Windows stability).
