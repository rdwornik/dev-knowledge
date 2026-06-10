===== FILE: 03_PROJECT — start =====

# 03 · The project — .dev-knowledge

## Vision

`.dev-knowledge` is the ecosystem's **methodology brain**: a universal, portable,
machine-agnostic LLM-driven development guide. It is **Knowledge Guardian,
Methodology Author, Auditor, and Disseminator** — it absorbs lessons from individual
projects, universalizes them into patterns, disseminates them back as enforceable
conventions, and audits child repos against the universal baseline. It is the
LLM-development "Scrum Master" for the ecosystem: **it does not write code** — it
ensures the framework is applied consistently and evolves with experience. This is
**Layer 2** of the ADR-28 three-layer model (Layer 1 = browser architect, Layer 3 =
Claude Code executors).

**Continuous improvement is the baseline posture, not an option.** Static methodology
is itself a failure mode. The methodology now **self-enforces** — it applies its own
conventions to its own process (the ADR-70 Tier-1 lifecycle holds session-boundary
closure, lint, and review to the same enforced-not-remembered bar it imposes on the
artifacts it governs).

**Strategic emphasis (current):** velocity in LLM-tech adoption; cross-repo
methodology consistency (drift detected proactively, corrected via universal updates
not per-repo patches); methodology evolution as obsession; lessons-capture as default.

## Scope

**In scope:** universal methodology + conventions for LLM-driven development;
cross-repo governance patterns (CLAUDE.md, ADRs, handoffs); knowledge consolidation;
audit/verification mechanisms ensuring child compliance.

**Out of scope (this is the most common source of new-chat drift — keep it):**
- Code-level implementation in child repos → child repos own it.
- Project-specific business logic, schemas, domain knowledge → Obsidian vault.
- Operational data / runtime telemetry.
- Replacement for a repo-specific CLAUDE.md or README.
- **Hierarchy or authority** over child repos beyond methodology compliance —
  there is no authority hierarchy, only functional roles.

## Purpose & critical paths

- **Status:** active. **Complexity:** medium (informal; repo-tier system deprecated
  2026-05-23).
- **Critical paths:** `protocols/`, `docs/decisions/` (ADRs + transcripts),
  `templates/`, `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`.
- **Related locations:** `~/.claude/` (CC runtime config — out of scope here);
  `.claude/` (project config: commands, rules, settings, the tier1-lifecycle plugin);
  `ObsidianVault/` (pre-sales — do not mix); `Dev/` (child repos, each owns its CLAUDE.md).
- **NOT a code project** — markdown governance files + read-only validators only.

## Sacred files (do not break these)

- **`LESSONS.md`** — append-only (ADR-29/39); oldest-top; never edit old entries.
- **`logs/TOKEN-LOG.md`** — append-only; never edit.
- **`JOURNAL.md`** — append-only, **newest-first prepend**; one entry per session/workday.
- **ADRs / transcripts / handoffs / audits** — **immutable**; supersede with a new
  file or an in-file amendment marker; never edit in place. The transcripts zone is
  enforced fail-closed by a PreToolUse guard (ADR-77).
- **Living docs** — `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`,
  `BACKLOG.md`: update in place; the canonical four carry a `last_reviewed` frontmatter
  stamp meaning *re-read end-to-end and confirmed accurate* — bump only after a genuine
  review (`audit.py` check #10 fails a stamp that predates the file's last edit).
- **`scripts/`** — read-only validators only; **Layer 2 never executes** (no
  orchestration that drives state in child repos).

## Cross-repo ownership (ADR-41)

This bundle covers **.dev-knowledge only**. Never direct work on another repo from
here, never edit another repo's BACKLOG or files. Cross-repo work routes through
dedicated artifacts (the corp chat, the ai-council chat), not this handoff.
`.dev-knowledge` is the methodology meta-layer; child repos consume it and feed
lessons back — no authority hierarchy, only functional roles.

===== FILE: 03_PROJECT — end =====
