# ADR-27: Scope Tagging Architecture (Council #27, Option A)

**Status:** Accepted
**Date:** 2026-04-21
**Type:** Binding — Council #27 decision (4/5 models, consensus)
**Council output:** `output/20260421_145718_2026-04-21-council-27-brief.md`

## Context

`.dev-knowledge/` has drifted from a single-domain dev methodology repo. Phase 2 audit (63 sections across 8 primary files) found scope distribution: 14% `[dev]`, 22% `[llm]`, 21% `[hybrid]`, 8% `[runtime]`, 35% `[meta]`. The repo is no longer majority-dev by section count. Council #27 was convened to decide between four options: defer (Option 0), section-level tagging (A), two repos with shared core (B), base+extension overlay (C).

## Decision

Adopt **Option A — single repo with section-level scope tagging**, with two additions: pre-commit hook enforcement, and evidence-triggered reopening conditions (not calendar-based).

### Tag vocabulary

Five values, exhaustive and mutually exclusive per section:

- `dev` — dev methodology: code, git, testing, programming workflow
- `llm` — LLM work generally: prompting, model choice, tokens, chat workflow
- `hybrid` — inseparably both dev and llm; cannot be split without rewriting
- `runtime` — Claude Code runtime config: skills, shortcuts, hooks, slash commands
- `meta` — about the repo/knowledge system itself: index, triage, governance, decisions

### Tag mechanism

HTML comment directly under each section header:

```
## Section Title
<!-- scope: hybrid -->

Section body...
```

Rationale: invisible in rendered markdown (GitHub, VS Code preview), grep-friendly for hook validation, no YAML frontmatter layout disruption, zero tooling changes.

### Consumer read sets

Defined in CLAUDE.md (not in this ADR). Tag vocabulary is canonical here; consumer-to-tag mapping is operational and may evolve without reopening this ADR.

### Governance rules

- **Hybrid ≤25% ceiling.** Phase 2 baseline is 21%. If hybrid grows beyond 25%, quarterly hygiene pass decomposes hybrid sections into dev + llm pairs.
- **Pre-commit hook enforcement.** All sections MUST have a `<!-- scope: X -->` comment with X from the vocabulary. Commits that introduce untagged sections or invalid values are blocked.
- **Evidence-triggered reopening.** This decision is revisited if ANY of:
  1. A staffed non-dev project starts (e.g. presales prompt library work begins)
  2. 5+ new `[llm]`-only sections written within 60 days (demand signal real)
  3. A second contributor begins writing to `.dev-knowledge/`

  Calendar-based reopening is explicitly rejected — revisit is triggered by evidence, not by date.

### LESSONS.md disposition

See ADR-29 (grandfathering rule).

## Council vote

Binding per AI Council protocol. Consensus 4/5 models on Round 2. Vote distribution:

- Claude Opus 4.7: R1 → Option 0, R2 → Option A
- Gemini 3.1 Pro Preview: R1 → A, R2 → A
- GPT-5.4: R1 → A, R2 → A
- DeepSeek Reasoner: R1 → A, R2 → A
- Grok 4.20: R1 → B, R2 → C (rejected)

Decisive argument (GPT-5.4 R2): Option A is dominant strategy — correct if non-dev demand stays weak (terminal architecture), correct if demand strengthens (pre-classifies for later split).

## Consequences

**Accepted costs:**
- Tag hygiene requires discipline; stale/missing tag poisons filter. Pre-commit hook mitigates.
- Scope confusion partially remains in single-folder structure — `.dev-knowledge/` name still reads dev-first to non-dev consumers.
- Consumers carry filter overhead at read time (browser upload preprocessing or manual section selection).

**Rejected alternatives:**
- **Option 0 (defer):** rejected because Phase 2 audit IS the evidence; additional 6-8 weeks of observation adds marginal value.
- **Option B (two repos):** rejected because non-dev demand is currently hypothetical; 35% meta overhead duplication premature.
- **Option C (overlay):** rejected because custom markdown loader is liability; fails "2am test"; pattern generalization unproven.

## References

- Council brief: `docs/audits/2026-04-21-council-27-brief.md`
- Phase 1 inventory: `docs/audits/2026-04-21-dev-knowledge-inventory.md`
- Phase 2 tagging: `docs/audits/2026-04-21-dev-knowledge-scope-tagging.md`
- Council debate output: `output/20260421_145718_2026-04-21-council-27-brief.md`
- ADR-28: three-layer architecture (complementary frame)
- ADR-29: LESSONS.md grandfathering (LESSONS-specific rule under this decision)
