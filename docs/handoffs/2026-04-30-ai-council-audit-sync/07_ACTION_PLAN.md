# Action Plan — ai-council (Future State)

Per ADR-37 two-phase: this file = Future State.
Current State is in `06_STATE_OF_PLAY.md`.

---

## Goals

Complete Phase 1 governance application to ai-council:

1. Create `ai-council/VISION.md` — fulfills ADR-33 mandate (F-01)
2. Update `ai-council/CLAUDE.md` — documents DEV_KNOWLEDGE_PATH per ADR-35 (F-02)

Both actions are P1, tier-independent, actionable now.

---

## Directives (execute in order)

### Directive 1 — F-01: Create ai-council/VISION.md

**ADR reference:** ADR-33 (see `05_GOVERNANCE_ESSENCES.md` for operational essence)

Action: Create `ai-council/VISION.md` with ADR-33 Standard tier structure.

Required frontmatter:
```yaml
version: 1.0
tier: M
owner: rob
last_reviewed: 2026-04-30
scale: M
```

Required sections:
1. **Mission** — ai-council is an AI debate framework that orchestrates
   multi-provider LLM debates (Anthropic, OpenAI, Gemini, Grok, DeepSeek)
   with blind voting and research integration for software engineering decisions.
2. **Scope** — in scope: debate orchestration, provider management, research
   integration, dual output (ai-council/output + .dev-knowledge/transcripts).
   Out of scope: infrastructure automation, pre-sales work, general AI tooling.
3. **Methodology** — Python 3.11+ CLI, pytest, ADR-based decisions, Council
   debates for architecture choices. Working in Claude Code (Sonnet/Opus tier).
4. **Lifecycle** — VISION review triggered by: scope expansion, new provider
   integration, methodology change. Owner: rob. Review cadence: quarterly or
   on trigger.
5. **Relationships** — .dev-knowledge (governance authority, methodology source,
   handoff destination), corp-monorepo (consumer of debates), corp-ops (S tier,
   not dependent).

Scope tag: `<!-- scope: meta -->` at file level (single tag under H1, ADR-29 pattern).

**Verification:** `ai-council/VISION.md` exists, frontmatter has all 5 required
fields, all 5 required sections present.

---

### Directive 2 — F-02: Update ai-council/CLAUDE.md

**ADR reference:** ADR-35 (see `05_GOVERNANCE_ESSENCES.md` for operational essence)

Action: Add a `## Cross-repo lessons` section to `ai-council/CLAUDE.md` documenting
the DEV_KNOWLEDGE_PATH env var.

Content to add (place in existing CLAUDE.md, appropriate section):
```
## Cross-repo lessons

Set `DEV_KNOWLEDGE_PATH=C:/Users/1028120/Documents/Dev/.dev-knowledge`
to enable cross-repo lessons retrieval (ADR-35). Full implementation
(lessons-index.json + SessionStart hook) pending in .dev-knowledge (BACKLOG P2).
```

Read `ai-council/CLAUDE.md` first to find the best insertion point (after
the main setup instructions, before or after testing section).

**Verification:** CLAUDE.md contains "DEV_KNOWLEDGE_PATH" and "ADR-35".

---

### Directive 3 — Update ai-council CHANGELOG and JOURNAL

After completing Directives 1 and 2:

1. Append a new entry to `ai-council/CHANGELOG.md` (newest-first format):
   - Date: 2026-04-30 (audit application date) or session date
   - What: VISION.md created (ADR-33 F-01), CLAUDE.md updated with
     DEV_KNOWLEDGE_PATH (ADR-35 F-02)

2. Prepend a new entry to `ai-council/JOURNAL.md` (Did/Failed/Next format):
   - Did: F-01 (VISION.md), F-02 (CLAUDE.md)
   - Failed: anything that didn't go as planned
   - Next: Phase 2 items (deferred F-03/F-04, pending calibration)

**Verification:** CHANGELOG entry present, JOURNAL entry prepended.

---

### Directive 4 — Run tests

```
cd ai-council && pytest -x --tb=short
```

Expected: all tests pass (no regressions from documentation changes).

**Verification:** pytest exits 0.

---

### Directive 5 — Fill 09_EXECUTION_EVIDENCE.md

After completing Directives 1-4, fill out
`.dev-knowledge/docs/handoffs/2026-04-30-ai-council-audit-sync/09_EXECUTION_EVIDENCE.md`
with raw stdout, test output, final HEAD SHA.

---

## Boundaries (do NOT do these)

- **DO NOT create `ai-council/BACKLOG.md`** — F-03 deferred pending tier calibration
- **DO NOT create `ai-council/ARCHITECTURE.md`** — F-04 deferred pending tier calibration
- **DO NOT rename existing ai-council ADRs** — F-05 grandfathered; 7 existing ADRs
  keep kebab-case naming
- **DO NOT touch `config/settings.yaml`** — has uncommitted changes unrelated to
  this handoff; leave as-is
- **DO NOT re-litigate ADR-38 migration** — locked, completed
- **DO NOT duplicate BACKLOG content** — reference BACKLOG entry IDs, never copy queue

## Out of scope (deferred)

- PLAYBOOK.md content additions for ADRs 36-41 (BACKLOG Stream C P1)
- Audit tool P1 implementation (BACKLOG Stream C P1)
- ADR-35 full retrieval implementation (BACKLOG Stream C P2)
- Phase 2 universalization (BACKLOG Cross-stream P2)
- ADR-39 registry amendment for new template files (BACKLOG Stream C P3)

## Fallbacks

- If VISION.md creation fails validation: check scope tag format per ADR-27
  (`<!-- scope: meta -->` immediately under H1)
- If CLAUDE.md update causes test failures: the update is documentation-only;
  no test should fail — investigate import or parsing issues
- If pytest fails on unrelated tests: do not revert Directives 1-2; report
  specific test failures to Rob for separate investigation

---

## Success criteria

- [ ] `ai-council/VISION.md` exists with all required ADR-33 frontmatter + sections
- [ ] `ai-council/CLAUDE.md` contains DEV_KNOWLEDGE_PATH reference
- [ ] `ai-council/CHANGELOG.md` updated
- [ ] `ai-council/JOURNAL.md` updated
- [ ] `pytest -x` passes in ai-council
- [ ] `09_EXECUTION_EVIDENCE.md` filled with evidence
