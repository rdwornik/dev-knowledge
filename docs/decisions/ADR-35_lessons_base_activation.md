# ADR-35 — Lessons base activation: storage, retrieval, querying

<!-- scope: meta -->

Status: Accepted
Date: 2026-04-29
Related: ADR-29 (lessons format), ADR-33 (universalization pattern),
         ADR-34 (file naming convention),
         transcript council_out_20260429_210057_*

## Context

LESSONS.md has accumulated 70+ append-only entries per ADR-29 format.
Three concrete gaps surfaced: no retrieval (session start doesn't
selectively surface relevant lessons), no promotion mechanism (lessons
to executable rules is ad-hoc), no querying (no way to ask "what
lessons about X?").

ADR-35 addresses storage, retrieval, querying, and the connection
model between LESSONS.md and ~/.claude/ runtime infrastructure.
Promotion automation is deferred to ADR-36 (separate session) per
Council Q8 split.

Council debate (council_out_20260429_210057_*) covered Q1-Q9.

## Decision

### Storage (Q2)

LESSONS.md remains canonical narrative source of truth (human-readable,
append-only per ADR-29). Derived `lessons-index.json` provides machine
queryable index. Index regenerated on LESSONS.md change via pre-commit
hook + manual `lessons reindex` command.

Index schema (minimum fields): id, date, source, lesson, category,
scope, action, repo (optional).

### Retrieval (Q3) — Push mode

SessionStart hook reads `lessons-index.json` filtered by:
- **Scope tags** matching current session context (dev / llm / hybrid /
  runtime / meta)
- **Recency**: last 60 days (configurable)

Filter logic: agent's session context (cwd, repo, task type) →
applicable scope tags → matching lessons surface at session start.

Evergreen flag (lessons that should always surface regardless of
recency) deferred to v2 post-baseline (covered in P3 refinements).

### Querying (Q5) — Pull mode

CLI command in .dev-knowledge: `lessons query "topic"` reads
`lessons-index.json`, returns matches by topic substring + scope tag.

Retrieval (Push) and querying (Pull) use SAME `lessons-index.json`.
Built together as single tooling unit.

### Connection model (Q6)

Bidirectional pipeline, formalized:

```
~/.claude/memory/corrections.jsonl
        │
        │ (manual review now; automation per ADR-36 future)
        ▼
.dev-knowledge/LESSONS.md  ◄── canonical narrative source of truth
        │
        ├──(reindex)──> lessons-index.json (machine search index)
        │
        └──(promotion per ADR-36)──> ~/.claude/rules/ (runtime executable)
```

LESSONS.md is source of truth. `lessons-index.json` is derived index.
`~/.claude/rules/` is derived runtime. Promotion mechanism specified
in ADR-36.

### Cross-repo discovery (Q7)

Hybrid:
- **Primary**: environment variable `DEV_KNOWLEDGE_PATH` set in shell
  profile, points to .dev-knowledge repo root
- **Fallback**: walk up from cwd until `.dev-knowledge` directory found
- **Documentation**: child repo CLAUDE.md / AGENTS.md explicit note
  pointing to .dev-knowledge LESSONS.md as authoritative reference

Per ADR-33 universalization pattern.

### Universalization (per ADR-33/34 pattern)

- **Mandate**: .dev-knowledge owns LESSONS.md and lessons-index.json
- **Recommendation**: child repos (corp-monorepo, ai-council, corp-ops,
  corp-sca-time-automation, future repos) configure discovery via
  env var + CLAUDE.md note
- **Migration cohort**:
  - Immediate (Stream C Phase 2): ai-council, corp-monorepo
    CLAUDE.md updated to reference .dev-knowledge LESSONS.md
  - Trigger-based: corp-ops, corp-sca-time-automation, future repos
    — next session touching repo for >1 commit, OR by 2026-06-30
- **Cross-repo audit (Phase 3)**: auditor tool verifies discovery
  configured (env var documented + CLAUDE.md reference present)

## Implementation plan

### P1 (separate session — Phase 2): lessons-index.json + retrieval + querying

Build as single tooling unit. Concrete deliverables:
- `lessons-index.json` schema definition + initial population
- `scripts/reindex_lessons.py` — parses LESSONS.md → lessons-index.json
- Pre-commit hook entry: regenerates index when LESSONS.md changes
- `~/.claude/hooks/SessionStart` integration — reads index, filters by
  scope + recency, surfaces top N relevant lessons
- `scripts/lessons_query.py` — CLI for `lessons query "<topic>"`
- Tests: index roundtrip, retrieval filter logic, query matching

### P2 (future ADR-36): promotion automation

Out of scope ADR-35. Triggered when P1 produces baseline data on
correction frequency.

### P3 (post-implementation review): refinements

- Evergreen flag if usage shows certain lessons are timeless
- Severity flagging if certain lessons need immediate runtime promotion
- Schema additions if usage surfaces missing fields

## Consequences

### Positive
- Lessons base becomes active, not passive archive
- Session start surfaces relevant context automatically (Push mode)
- Rob can query lessons by topic on demand (Pull mode)
- Bidirectional pipeline formalized (no more implicit/ad-hoc)
- LESSONS.md remains human-readable canonical source of truth
- Single index serves both retrieval and querying — no duplication

### Negative
- Index regeneration cost on LESSONS.md edit (pre-commit ~1-2s; small)
- SessionStart hook adds latency (mitigated — 70 entries is tiny)
- Cross-repo discovery requires env var setup OR walk-up (one-time per
  machine)
- Schema migration risk if LESSONS.md format changes (mitigated by
  append-only per ADR-29)

### Follow-ups
- ADR-36 (separate session): promotion automation
- P1 implementation (separate session): tooling build
- ai-council CLAUDE.md update: reference .dev-knowledge LESSONS.md
  (Stream C Phase 2)
- corp-monorepo CLAUDE.md update: same (Stream C Phase 2)
- Cross-repo audit tool spec includes lessons discovery validation
  (Phase 3)
- Re-audit at 2026-06-30 for trigger-based cohort compliance

## References

- transcript council_out_20260429_210057_pick_council_adr35_lessons_base_activation.md
- ADR-29 (lessons format and grandfathering)
- ADR-33 (VISION.md universalization pattern)
- ADR-34 (file naming convention)
- ESSENTIALS "Three Homes for Knowledge"
- ESSENTIALS "Feedback Loop"
