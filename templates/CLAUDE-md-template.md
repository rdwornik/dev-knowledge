---
last_reviewed: <YYYY-MM-DD>
status: active
owner: <Rob | other>
---

# CLAUDE.md — <Repo>
<!-- scope: meta -->
<!-- version: 2.3 — 2026-07-12 -->

<!-- CONDITIONAL (consumers only): child repos import the methodology floor here and carry
     a human-facing boundary note; the HUB does NOT (@import absent — hub asymmetry, per
     the fleet-boundary marker design). For a consumer, uncomment the import line:
@.claude/CLAUDE-FLOOR.md
     (methodology floor — hash-guarded replica, ADR-78/93) -->

> **Session contract for Claude Code in this repo.** Read on every session start (auto). Single canonical agent-instruction file (≤200 lines). Per ADR-53.
>
> **For universal rules:** read the hub methodology protocols `ESSENTIALS.md` and `PLAYBOOK.md` (at the hub `.dev-knowledge/protocols/` set; hub-pointer, never copied into a consumer).

## 1. First read (session start)
<!-- scope: meta -->
<!-- methodology:start id=first-read owner=hub -->
<!-- SYNC verbatim from templates/claude-regions/first-read.md — do not hand-edit; owner=hub -->
<!-- methodology:end id=first-read -->

## 2. Repo identity
<!-- scope: meta -->
<!-- methodology:start id=repo-identity owner=repo -->

- **Name:** `<repo-name>`
- **Status:** `<active | maintenance | archived>`
- **Purpose:** `<one-sentence purpose>`
- **Owner:** `<Rob | other>`
- **Critical paths:** `<key dirs/files>`
<!-- methodology:end id=repo-identity -->

## 3. Architecture
<!-- scope: meta -->
<!-- methodology:start id=repo-architecture owner=repo -->

See `ARCHITECTURE.md` for the structural model; read it before structural changes (required for every repo, per ADR-51 as amended 2026-05-23).
<!-- methodology:end id=repo-architecture -->

## 4. Conventions
<!-- scope: meta -->

- **Naming:** `<repo naming conventions>`
<!-- methodology:start id=conventions-commit-branch owner=hub -->
<!-- SYNC verbatim from templates/claude-regions/conventions-commit-branch.md — do not hand-edit; owner=hub -->
<!-- methodology:end id=conventions-commit-branch -->
- **Testing:** `<e.g. pytest -x --tb=short>`
- **Linting:** `<e.g. ruff check --fix>`

**Out of scope for this repo:**
- `<what belongs elsewhere — e.g. client/pre-sales data → Obsidian vault>`
<!-- methodology:start id=conventions-output-formatting owner=hub -->
<!-- SYNC verbatim from templates/claude-regions/conventions-output-formatting.md — do not hand-edit; owner=hub -->
<!-- methodology:end id=conventions-output-formatting -->

## 5. Critical rules
<!-- scope: meta -->

<!-- methodology:start id=critical-rules-records owner=hub -->
<!-- SYNC verbatim from templates/claude-regions/critical-rules-records.md (rules 1-3) — do not hand-edit; owner=hub -->
<!-- methodology:end id=critical-rules-records -->
4. `<repo-specific rule>`
5. `<repo-specific rule>`
<!-- methodology:start id=critical-rules-consistency owner=hub -->
<!-- SYNC verbatim from templates/claude-regions/critical-rules-consistency.md (rule 6) — do not hand-edit; owner=hub -->
<!-- methodology:end id=critical-rules-consistency -->
7. `<repo-specific rule>`
8. `<repo-specific rule>`
<!-- methodology:start id=critical-rules-no-leftovers owner=hub -->
<!-- SYNC verbatim from templates/claude-regions/critical-rules-no-leftovers.md (rule 9) — do not hand-edit; owner=hub -->
<!-- methodology:end id=critical-rules-no-leftovers -->

The owner=hub rules (records 1-3, consistency 6, no-leftovers 9) are fixed and synced by id; number your repo-specific rules around them. Total ≤10 bullets.

## 6. Session start protocol
<!-- scope: runtime -->
<!-- methodology:start id=session-start-protocol owner=hub -->
<!-- SYNC verbatim from templates/claude-regions/session-start-protocol.md — do not hand-edit; owner=hub -->
<!-- methodology:end id=session-start-protocol -->

## 7. Slash commands available
<!-- scope: runtime -->
<!-- methodology:start id=commands-repo-roster owner=repo -->

User-level (`~/.claude/commands/`):
- `<command + one-line purpose>`

Repo-level (`./.claude/commands/`):
- `<command + one-line purpose>`
<!-- methodology:end id=commands-repo-roster -->

## 8. Skills active
<!-- scope: runtime -->
<!-- methodology:start id=skills-repo-roster owner=repo -->

User-level (`~/.claude/skills/`):
- `<skill + trigger>`

Repo-level (`./.claude/`):
- `<skill + purpose>`
<!-- methodology:end id=skills-repo-roster -->

## 9. Hooks active
<!-- scope: runtime -->
<!-- methodology:start id=hooks-repo-roster owner=repo -->

Pre-commit (`.pre-commit-config.yaml` — set-match this list to the live config):
- `<hook + purpose>`

Session hooks (`.claude/settings.json`):
- `<hook + purpose>`
<!-- methodology:end id=hooks-repo-roster -->

## 10. Anti-patterns specific to Claude Code in this repo
<!-- scope: meta -->
<!-- methodology:start id=antipatterns-universal owner=hub -->
<!-- SYNC verbatim from templates/claude-regions/antipatterns-universal.md — do not hand-edit; owner=hub -->
<!-- methodology:end id=antipatterns-universal -->

## 11. Recent ADRs binding here (last 5)
<!-- scope: meta -->
<!-- methodology:start id=recent-adrs-roster owner=repo -->

Brief one-liners (or a generated fragment). Full list in `docs/decisions/README.md`. (Conditional — present only where the repo has `docs/decisions/`.)

- ADR-NN: `<topic — one sentence>`
<!-- methodology:end id=recent-adrs-roster -->

## 12. Section history
<!-- scope: meta -->
<!-- methodology:start id=section-history owner=repo -->

- v1.0 (2026-04-24) — initial template per Gap #5. Hybrid pattern, thin pointer, ≤200 lines target.
- v2.0 (2026-05-19) — ADR-53: retire thin-pointer/AGENTS.md framing; CLAUDE.md is now the substantive single canonical per-repo agent-instruction file.
- v2.1 (2026-05-19) — add §3 Architecture and §4 Conventions; renumber old §3–§10 to §5–§12.
- v2.2 (2026-06-02) — ADR-38 A6: add mandatory `last_reviewed`/`status`/`owner` frontmatter; H1 → `# CLAUDE.md — <Repo>`; §11 → "(last 5)". The 12-section spine is the locked CLAUDE.md canonical template.
- v2.3 (2026-07-12) — content-parity inventory B1: add the 15-region methodology-marker topology (8 owner=hub + 7 owner=repo) matching the live hub CLAUDE.md, preserving the §4/§5 interleaving; owner=hub regions now SYNC by id from `templates/claude-regions/<id>.md` (not embedded — DRY); child-floor `@import` + boundary note marked CONDITIONAL (consumers only; hub asymmetry). Content refresh of the placeholder bodies remains BACKLOG #17.
<!-- methodology:end id=section-history -->

---

**Last updated:** `<YYYY-MM-DD>`
**Maintained by:** `<Rob | other>`
