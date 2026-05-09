# Action Plan — ai-council (audit-sync, 2026-05-09)

## Goal (OBJECTIVE)

Complete F-01 (VISION.md creation) and F-02 (lessons discovery configuration
in CLAUDE.md). Docs-only session — zero code changes, zero test changes.

**Definition of done:**
- `ai-council/VISION.md` exists with correct frontmatter + 5 required sections
- `ai-council/CLAUDE.md` contains DEV_KNOWLEDGE_PATH env var reference
- `config/settings.yaml` committed clean (working tree clean after)
- `ai-council/CHANGELOG.md` updated
- `ai-council/JOURNAL.md` updated
- `pytest -x` exits 0, test count matches baseline
- `09_EXECUTION_EVIDENCE.md` filled with command outputs

Estimated: ≤45 minutes Claude Code time. Session is docs-only.

## Directives (sequential — follow exactly)

1. **Review config/settings.yaml diff before committing.**
   Run `git diff config/settings.yaml` in ai-council. Stage 3 verified that
   the actual change is `grok model: "grok-4.20" → "grok-4.3"` (model string
   update) plus whitespace normalization — NOT a timeout change as architect
   believed. Write accurate commit message reflecting actual change.
   Commit: `config: update grok model string to grok-4.3`.
   Verify: `git status --porcelain` shows clean working tree.

2. **Create `ai-council/VISION.md`** per ADR-33 Lite schema (tier M).
   Frontmatter:
   ```yaml
   ---
   version: "1.0"
   tier: M
   owner: rob
   last_reviewed: "2026-05-09"
   scale: M
   ---
   ```
   Required sections (Lite tier):
   - **Mission**: Multi-model AI debate and research tool for architectural
     decision-making across the dev ecosystem.
   - **Scope**: 5 debate providers (Claude Opus, Gemini, GPT, Grok, DeepSeek),
     5 research providers (Perplexity, Gemini Deep Research, OpenAI o4-mini,
     Grok x_search, o3-deep), 4 modes (pick/ideas/judge/research), CLI entry
     `council`. Standalone tool; called by other repos. Outputs to dual paths
     (ai-council/output/ + .dev-knowledge/docs/decisions/transcripts/).
   - **Relationships**: No inbound code dependencies. Called by other repos via
     `council` CLI. Produces binding ADRs that govern all ecosystem repos.
   - **Lifecycle**: Active development with continuous improvement focus.
     Roadmap reviewed at session boundaries — improvements emerge from real
     usage and lessons. Recent additions: Grok as 5th research provider,
     downloads auto-scan, --models flag. Review triggers: provider API
     changes, new model availability, governance requirement changes,
     real-usage friction surfacing improvement opportunities.
     Static-maintenance posture is exception requiring explicit declaration.
   Commit: `docs: create VISION.md per ADR-33 (tier M)`
   Verify: file exists, frontmatter complete, sections present, `pytest -x` passes.

3. **Update `ai-council/CLAUDE.md`** — add DEV_KNOWLEDGE_PATH reference per
   ADR-35. Add a new section (e.g., "Lessons Discovery") with:
   ```
   Set DEV_KNOWLEDGE_PATH to the .dev-knowledge repo path:
   $env:DEV_KNOWLEDGE_PATH = "C:/Users/1028120/Documents/Dev/.dev-knowledge"

   - ai-council-local lessons: stay in tasks/lessons.md
   - Cross-ecosystem lessons: go to $DEV_KNOWLEDGE_PATH/LESSONS.md

   Future ADRs: use underscore naming (ADR-NN_topic.md) per ADR-34.
   Existing 7 ADRs (kebab-case) are grandfathered.
   ```
   Commit: `docs: configure lessons discovery per ADR-35, note ADR naming`
   Verify: CLAUDE.md contains DEV_KNOWLEDGE_PATH reference, `pytest -x` passes.

4. **Run `pytest -x`** — confirm 310/310 baseline holds.
   Verify: exit code 0. If count differs from 310, note actual count in
   09_EXECUTION_EVIDENCE.md but do not treat as failure unless tests fail.

5. **Update `ai-council/CHANGELOG.md`** — append entry dated 2026-05-09:
   - config/settings.yaml: update grok model string to grok-4.3
   - VISION.md created (tier M, per ADR-33)
   - CLAUDE.md: lessons discovery configuration (DEV_KNOWLEDGE_PATH, per ADR-35)

6. **Update `ai-council/JOURNAL.md`** — prepend new session entry:
   - Did: created VISION.md (tier M), configured lessons discovery in CLAUDE.md,
     committed config/settings.yaml (grok model string update)
   - Result: F-01 and F-02 closed; baseline 310/310 holds
   - Next: return 09_EXECUTION_EVIDENCE.md to .dev-knowledge for review;
     await ADR-40 recalibration for F-03/F-04 tier decisions
   Commit: `docs: CHANGELOG + JOURNAL for governance session`

7. **Fill `09_EXECUTION_EVIDENCE.md`** with command outputs from all steps above.
   See template in that file for required sections. Include: commands run,
   test results (pytest output), git diffs or log, final HEAD SHA, any failures.

## Boundaries (DO NOTs)

- **DO NOT** create BACKLOG.md (F-03 deferred — tier not confirmed by recalibration)
- **DO NOT** create ARCHITECTURE.md (F-04 deferred — tier not confirmed)
- **DO NOT** rename existing 7 ADR files (kebab-case grandfathered per ADR-29)
- **DO NOT** push without Rob's explicit confirmation
- **DO NOT** address pre-existing ruff (17) or mypy (4) errors — out of scope
- **DO NOT** make structural changes to src/ai_council/ — migration complete
- **DO NOT** migrate existing tasks/lessons.md entries to .dev-knowledge —
  they are ai-council-specific operational lessons; keep local
- **DO NOT** change provider code, model strings, settings, or debate/research logic
- **DO NOT** create or modify test files — baseline must hold
- **DO NOT** change the default synthesizer (Gemini) or default panel configuration
- **If `pytest -x` fails:** STOP immediately, report failure details, do not continue
- **If config/settings.yaml diff shows unexpected changes** beyond grok model string
  + whitespace: STOP, show diff to Rob, do not blindly commit

## Success criteria (verify all before declaring done)

```bash
cd C:/Users/1028120/Documents/Dev/ai-council
pytest -x                           # exit 0, test count ≥ 300
git status --porcelain              # empty (clean working tree)
ls VISION.md                        # file exists
grep -c "DEV_KNOWLEDGE_PATH" CLAUDE.md  # ≥ 1 match
git log --oneline -5                # 3 new commits visible
git rev-parse HEAD                  # capture final SHA for 09_EXECUTION_EVIDENCE
```
