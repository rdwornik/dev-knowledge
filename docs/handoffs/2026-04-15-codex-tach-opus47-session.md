# HANDOFF — Codex Integration + Tach Adoption + Opus 4.7 Updates
Date: 2026-04-15

## OBJECTIVE
Multi-topic session: Codex CLI as code reviewer, Tach import boundary enforcement via AI Council #26, Opus 4.7 tooling updates, Dev Practice OS universalization.

## STATUS: All items complete except magistrala verification.

## COMPLETED — Codex Review Integration
- Codex CLI installed (ChatGPT Plus $20/mo, GPT-5.4 default)
- AGENTS.md created in corp-monorepo (115 lines, severity calibrated: diff review = Critical+High only, full audit = all levels)
- `/review` slash command in ~/.claude/commands/review.md
- PLAYBOOK.md S15 [L+M] Cross-Tool Review added
- PLAYBOOK.md S16 [L only] Code Quality Audit Process added (audit-fix-verify cycle, severity definitions)
- ESSENTIALS.md updated with monthly audit + Codex review step in "Ending a Session"
- First full Codex audit ran: 4 CRITICAL + 4 HIGH findings, ~30% false positive rate
- Saved to corp-monorepo/docs/audits/2026-03-30-codex-full-audit.md
- templates/AGENTS.md.template.md created in .dev-knowledge (L + M scale variants)
- /ultrareview (Claude Code built-in, cloud multi-agent) added as alternative to Codex in S15. A/B test pending.

## COMPLETED — Tach Adoption (Council #26)
- AI Council #26 debated and decided: adopt Tach, pre-commit + CI, distributed ownership with lightweight review
- ADR-26 created in corp-monorepo/docs/decisions/
- Phase 1: tach.toml created (34 modules, 4 layers: foundation/core/orchestration/interface)
- corp.ingest reclassified core → orchestration (Codex audit found 3 upward deps in router.py)
- .pre-commit-config.yaml updated (tach hook after ruff, fires on src/corp/*.py)
- .github/workflows/tach.yml created (CI gate, parallel to pytest)
- CONTRIBUTING.md created (tach sync = cultural rule, NOT automation)
- AGENTS.md import-direction check replaced with Tach reference
- Phase 2: baseline violations resolved (corp.project_resolver → core, corp.query_engine → orchestration)
- Step 12: AGENTS.md + ARCHITECTURE.md + 5 module READMEs updated to 4-layer taxonomy
- tach check passes clean, CI unblocked, 2495 tests passing

## COMPLETED — Project Scale Tiers
- L/M/S definitions added to PLAYBOOK.md
- Tier tags added to scale-dependent sections ([L only], [L+M])
- Post-structural-change documentation rule with tier scaling
- ESSENTIALS.md reference added

## COMPLETED — Opus 4.7 + Tooling Updates
- ~/.claude/settings.json updated: showThinkingSummaries: true, includeCoAuthoredBy: false, cleanupPeriodDays: 90, recap: true
- CLAUDE_CODE_SUBPROCESS_ENV_SCRUB removed (conflicted with --dangerously-skip-permissions)
- VS Code extensions cleaned: removed spell-checker, debugpy, indent-rainbow (kept 12 core extensions)
- User preferences updated in claude.ai (added search-first rule, shortest-answer rule, Scale Tiers, Codex review rule, JOURNAL→CHANGELOG fix)
- Opus 4.7 xhigh effort level documented in ESSENTIALS.md and PLAYBOOK.md

## COMPLETED — Lessons (9 new entries in LESSONS.md dated 2026-03-30 and 2026-04-15)
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
- **Magistrala verification** — pipeline unverified end-to-end since Council #24 MyWork restructure. PROMPT_magistrala_verification.md is ready to execute. JOURNAL marks this as next priority.
- **Codex vs /ultrareview A/B test** — next feature branch in corp-monorepo, run both, compare findings, standardize on winner
- **claude-usage dashboard** (phuryn/claude-usage) — install for baseline cost numbers per project
- **Markitdown benchmark** — benchmark against CKE tier-1 extraction on Lenzing/PepsiCo test set
- **Tach lesson for Council process** — "always run data-gathering audit before Council debate"

## KEY DECISIONS FROM THIS SESSION
- Codex is reviewer only, Claude Code builds. Never reverse roles.
- tach sync is cultural rule — manual deliberate step, inspect diff, commit alongside code change. NEVER wire into CI/pre-commit.
- Review decision is post-build, not pre-prompt. Check git diff --stat after build, decide then.
- AGENTS.md is project-specific (describes architecture). Template is universal (in .dev-knowledge/templates/).
- Four-layer taxonomy (foundation/core/orchestration/interface) replaces 7-layer model in all docs.

## CONTEXT FOR NEW CHAT
- Claude Code v2.1.112, Opus 4.7 available
- corp-monorepo: 2495 tests, tach check clean, CI clean
- .dev-knowledge: S-scale, 14+ commits, all process docs current
- Codex CLI: installed, ChatGPT Plus, 88% → ~45% weekly budget after full audit
- settings.json: 6 new settings added today
