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

## Amendment 2026-04-24: Commit-time enforcement prescription

The original text specified a hybrid ≤25% ceiling with quarterly hygiene pass for remediation but did not prescribe commit-time enforcement behavior. This amendment adds that prescription.

### Ratio-aware enforcement rule

The pre-commit hook enforces the hybrid ceiling using a delta-based predicate across ALL IN_SCOPE_FILES (repo-wide ratio, not per-file):

- **Block** if: `working_ratio > HEAD_ratio` AND `working_ratio > 25%`
- **Pass** if: `working_ratio ≤ HEAD_ratio` (hygiene in progress or neutral change)
- **Pass** if: `working_ratio ≤ 25%` (within ceiling regardless of direction)
- **Genesis case** (no HEAD baseline exists for any IN_SCOPE_FILE): flat 25% ceiling applies

Rationale: flat 25% blocking causes a "stuck above ceiling" failure mode where commits are blocked indefinitely until a full hygiene pass is completed. Delta-based enforcement blocks regressions only, permitting incremental hygiene commits to proceed.

### Genesis case handling

When no IN_SCOPE_FILE exists at HEAD (first commit of the repo), the working-tree ratio must not exceed 25%. This prevents seeding the repo with high-hybrid baseline content.

### Ratio reporting

On every hook run (pass or block), the hook prints:
`Hybrid ratio: X% (HEAD: Y%, Δ: +/-Z%)`

### Relationship to original text

Decision intent unchanged. This amendment adds prescription for commit-time enforcement behavior that was under-specified in the original text (which addressed quarterly hygiene, not commit-time delta behavior). The 25% threshold, vocabulary, and governance rules are unmodified.

## Amendment 2026-04-25: Heading level scope and validator no-args behavior

Two under-specified behaviors clarified based on a divergence discovered during Gap #1 implementation (2026-04-24).

### Heading levels covered

Scope tags are required under **H2 (`##`) and H3 (`###`) headings**. H4+ headings are exempt (they are sub-items of a section, not sections in their own right). The validator already implements this via `H2_RE = re.compile(r"^#{2,3}\s+")`. ADR-27 original text said "section headers" without specifying level; this amendment makes the prescription explicit.

### Validator standalone invocation

When `validate_scope_tags.py` is invoked without filename arguments (manual check), it must scan all in-scope files on disk — not produce a vacuous pass. The pre-commit hook passes staged filenames via `pass_filenames: true`; standalone runs without args must be equivalent to a full-repo check, not a no-op.

**Fix applied:** `main()` now falls back to all `IN_SCOPE_FILES` present on disk when `paths` is empty.

### Discovery context

Validator reported "all files pass" (no-args invocation). Pre-commit hook failed citing missing H3 scope tags. Apparent divergence; actual cause was empty-path vacuous pass. Tools agree on H3 requirement — invocation semantics were the gap.
