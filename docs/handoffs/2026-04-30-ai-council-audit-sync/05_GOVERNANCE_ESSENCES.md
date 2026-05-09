# Governance Essences — ai-council audit-sync

ADR operational rules relevant to directives F-01 and F-02.
NOT full ADR copies — see full ADRs at paths cited below.

---

## ADR-33 — VISION.md Universalization

**Drives:** F-01 (Create ai-council/VISION.md)

VISION.md is mandatory at M+ tier (Lite for M, Standard for L). ai-council
is P1 audit finding F-01: VISION.md absent. Required regardless of whether
tier is M or L post-recalibration — both require VISION.md.

**Required frontmatter fields:**
```
version: 1.0
tier: M
owner: rob
last_reviewed: 2026-04-30
scale: M
```

**Required sections (Standard tier — 6 sections):**
1. Mission — what this project does, in 2-3 sentences
2. Scope — what's in, what's out
3. Methodology — how work is done (toolchain, process, conventions)
4. Lifecycle — how the project evolves (triggers for updates, review cadence)
5. Relationships — dependencies on other repos, integrations
6. (Optional: References — ADRs, docs, Council decisions)

**Tier field:** Use `tier: M` for ai-council given calibration concern with
current ADR-40 coefficients (F-08). Rob accepts M designation pending
recalibration.

Full ADR: `.dev-knowledge/docs/decisions/ADR-33_vision_universalization.md`

---

## ADR-35 — Lessons Base Activation

**Drives:** F-02 (Update ai-council/CLAUDE.md with DEV_KNOWLEDGE_PATH)

Cross-repo lessons retrieval requires `DEV_KNOWLEDGE_PATH` env var pointing
to `.dev-knowledge` root. Each repo's CLAUDE.md must document this variable
so Claude Code sessions can discover and query the lessons base. Full
implementation (lessons-index.json + retrieval hook) is pending in
`.dev-knowledge` (BACKLOG P2) — the action here is configuration documentation
only: add a note to `ai-council/CLAUDE.md` stating the env var and its purpose.

**What to add to CLAUDE.md:**
In a "## Cross-repo lessons" or similar section:
```
DEV_KNOWLEDGE_PATH=C:/Users/1028120/Documents/Dev/.dev-knowledge

Set this env var to enable cross-repo lessons retrieval (ADR-35).
Full implementation pending in .dev-knowledge (BACKLOG P2 item).
```

**What NOT to do:** Do not attempt to implement the retrieval mechanism itself
(that belongs to .dev-knowledge, not ai-council). Documentation only.

Full ADR: `.dev-knowledge/docs/decisions/ADR-35_lessons_base_activation.md`
