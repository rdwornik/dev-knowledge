# HANDOFF — Tech Radar + Dev Practice OS Session
Date: 2026-04-15
Project Scale: S (.dev-knowledge)

## OBJECTIVE
Evaluacja nowych narzędzi (Codex CLI, Tach, Opus 4.7), wdrożenie ich w projekty (corp-monorepo L, corp-sca-time-automation M), universalizacja Dev Practice OS.

## STATUS: All items complete except magistrala verification and one A/B test.

## COMPLETED — Codex Review Integration
- Research: community consensus Claude builds + Codex reviews, tweet analysis, 10+ sources
- Codex CLI installed (ChatGPT Plus $20/mo, GPT-5.4)
- AGENTS.md created in corp-monorepo (115 lines, severity calibrated, two review modes: diff/full audit)
- AGENTS.md fix: read-only commands clarified, type hints moved HIGH→MEDIUM
- /review slash command in ~/.claude/commands/review.md
- PLAYBOOK.md S15 [L+M] Cross-Tool Review (Codex + /ultrareview as options)
- PLAYBOOK.md S16 [L only] Code Quality Audit Process (audit-fix-verify cycle, severity definitions)
- ESSENTIALS.md: monthly audit + Codex review in "Ending a Session"
- First Codex full audit: 4 CRITICAL + 4 HIGH, ~30% false positive rate
- Saved to corp-monorepo/docs/audits/2026-03-30-codex-full-audit.md
- templates/AGENTS.md.template.md in .dev-knowledge (L + M scale variants)

## COMPLETED — Tach Adoption (Council #26)
- Council brief prepared with real data (0 violations, pytest 166s, .pre-commit-config.yaml contents)
- Council #26 debated: 4 models, 2 rounds, synthesis by OpenAI
- Decision: adopt Tach, pre-commit + CI, distributed ownership with lightweight review
- ADR-26 created in corp-monorepo
- Phase 1: tach.toml (34 modules, 4 layers: foundation/core/orchestration/interface)
- corp.ingest reclassified core→orchestration (Codex audit: 3 upward deps in router.py)
- Phase 2: baseline violations resolved (project_resolver→core, query_engine→orchestration)
- Step 12: AGENTS.md + ARCHITECTURE.md + 5 module READMEs updated to 4-layer taxonomy
- tach check clean, CI unblocked, 2495 tests passing

## COMPLETED — Project Scale Tiers
- L/M/S definitions in PLAYBOOK.md
- Tier tags on scale-dependent sections ([L only], [L+M])
- Post-structural-change documentation rule with tier scaling
- ESSENTIALS.md reference

## COMPLETED — Opus 4.7 + Tooling Updates
- settings.json: showThinkingSummaries, includeCoAuthoredBy, cleanupPeriodDays, recap added
- CLAUDE_CODE_SUBPROCESS_ENV_SCRUB removed (conflicted with --dangerously-skip-permissions)
- Source: PowerShell profile, not settings.json — discovered through 3-step debugging
- VS Code extensions: removed spell-checker, debugpy, indent-rainbow (12 core remain)
- User preferences updated in claude.ai (search-first, shortest-answer, Scale Tiers, CHANGELOG not JOURNAL)
- Opus 4.7 xhigh effort level documented in ESSENTIALS.md and PLAYBOOK.md
- /ultrareview added to S15 as alternative to Codex — A/B test pending

## COMPLETED — Process Improvements
- Verified handoff workflow: browser generates → Claude Code verifies against repo → saves to docs/handoffs/
- ESSENTIALS.md updated with verified handoff process
- State audit of .dev-knowledge: 14/16 changes verified, 2 gaps closed

## COMPLETED — Lessons (10 entries in LESSONS.md)
1. Audit-first, fix-second pattern
2. Two-AI-reviewer setup catches different blind spots
3. Structural refactors need shims, not big-bang
4. ARCHITECTURE.md is highest-value deliverable
5. False positives in automated audit need severity calibration
6. Universal rules that don't apply universally erode compliance
7. TODO markers: code OK, docs never
8. Intent-based module classification fails; use actual import graph
9. Baseline violations are documentation, not blockers
10. Council debate quality scales with real data

## PENDING
- Magistrala verification — pipeline unverified end-to-end since Council #24 MyWork restructure
- Codex vs /ultrareview A/B test — next feature branch, run both, compare findings
- claude-usage dashboard (phuryn/claude-usage) — install for baseline cost numbers
- Markitdown benchmark — against CKE tier-1 extraction on Lenzing/PepsiCo test set
- Tach for M-scale repos (ai-council, corp-ops) — Council #26 deferred, evaluate after 1 month

## KEY DECISIONS
- Codex = reviewer only, Claude Code builds. Never reverse.
- tach sync = cultural rule, NEVER automation — manual deliberate step, inspect diff, commit alongside code change. Never wire into CI/pre-commit.
- Review decision is post-build (check git diff --stat), not pre-prompt
- AGENTS.md is project-specific, template is universal
- 4-layer taxonomy replaces 7-layer model
- Project Scale Tiers (L/M/S) gate which processes apply
- /ultrareview vs Codex — A/B test before standardizing
- Handoff workflow: browser generates → Claude Code verifies → saves to docs/handoffs/

## CONTEXT
- Claude Code v2.1.112, Opus 4.7 available
- corp-monorepo: 2495 tests, tach check clean, CI clean, 4-layer taxonomy aligned
- .dev-knowledge: S-scale, all process docs current
- Codex CLI: installed, ChatGPT Plus, weekly budget used ~55% on full audit
- settings.json: 6 new settings added
- Three active project chats: corp-monorepo (L), corp-sca-time-automation (M), this one (tech radar)
