---
last_reviewed: 2026-06-01
status: active
owner: Rob
---

# CLAUDE.md — Dev Knowledge
<!-- scope: meta -->
<!-- version: 2.1 — 2026-05-19 -->

> **Session contract for Claude Code in this repo.** Read on every session start (auto). Single canonical agent-instruction file (≤200 lines). Per ADR-53.
>
> **For universal rules:** read `protocols/ESSENTIALS.md` and `protocols/PLAYBOOK.md`.

## 1. First read (session start)
<!-- scope: meta -->

In order, read:
1. This file (you're here)
2. `protocols/ESSENTIALS.md` — Rob's universal working style
3. `protocols/PLAYBOOK.md` — universal protocols (only sections relevant to current task)
4. Most recent `docs/handoffs/*/HANDOFF.md` if continuing prior session
5. Last 5 entries of `JOURNAL.md`

If ESSENTIALS or PLAYBOOK are unavailable, proceed with this file alone but flag it.

## 2. Repo identity
<!-- scope: meta -->

- **Name:** `.dev-knowledge`
- **Complexity:** medium (informal; repo-tier system deprecated 2026-05-23 — no declared tier)
- **Status:** active
- **Purpose:** Universal LLM-driven development guide and methodology framework; governs all projects under `Dev/`; Layer 2 of the ADR-28 three-layer ecosystem model
- **Owner:** Rob
- **Critical paths:** `protocols/`, `docs/decisions/`, `templates/`, `VISION.md`, `ARCHITECTURE.md`
- **Related locations:** `~/.claude/` (Claude Code runtime config); `.claude/` (project-level config); `ObsidianVault/` (pre-sales, do not mix); `Dev/` (child repos, each has own `CLAUDE.md`)

## 3. Architecture
<!-- scope: meta -->

See `ARCHITECTURE.md` for the structural model; read it before structural changes (required for every repo, per ADR-51 as amended 2026-05-23). NOT a code project — markdown governance files + read-only validators only.

## 4. Conventions
<!-- scope: meta -->

- **Naming:** UPPERCASE for top-level living docs (`VISION.md`, `CLAUDE.md`, etc.); `ADR-NN-topic.md` for decisions; `YYYY-MM-DD-slug.md` for dated artifacts; `council-out-YYYYMMDD_HHMMSS-topic.md` for Council CLI output; kebab-case otherwise
- **Commits:** Conventional Commits — `feat/fix/docs/chore/refactor`
- **Branches:** `feat/<topic>`, `fix/<issue>`, `docs/<scope>`, `chore/<scope>` off `main`
- **Testing:** `pytest -x --tb=short`
- **Linting:** `ruff check --fix` (pre-commit)
- **Scope tags:** `<!-- scope: X -->` (`dev|llm|hybrid|runtime|meta`) — informal only; not enforced (ADR-27; enforcement withdrawn per ADR-48)
- **File lifecycle:** Append-only: `LESSONS.md`, `TOKEN-LOG.md` (never edit), `JOURNAL.md` (newest-first prepend). Immutable: ADRs, transcripts, handoffs, audits (supersede with new file). Living: `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `BACKLOG.md` (update in place).
- **Freshness cadence:** the living docs `VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING` carry a `last_reviewed` frontmatter stamp meaning *re-read end-to-end and confirmed accurate (or drift filed)* — **not** merely "touched". `audit.py` check #10 fails when a stamp predates the file's last edit (edited-but-not-re-reviewed) and warns past a 30-day backstop. Bump `last_reviewed` only after a genuine review. See PLAYBOOK "Canonical-file freshness cadence".

**Out of scope for this repo:**
- Code-level implementation → child repos (corp-monorepo, ai-council, etc.)
- Client/product/domain knowledge → Obsidian vault
- Project-specific CLAUDE.md content → each repo owns its own
- Claude Code runtime config → `~/.claude/`
- Council debate transcripts originate in `ai-council/`; they archive here in `docs/decisions/transcripts/`

- **Output formatting:** Session summaries and step reports use plain markdown tables (`| col | col |`) or bullet lists. No Unicode box-drawing characters (`┌─┐ │ ├─┤ └─┘`). No column-padding spaces. Markdown is human-readable and token-cheap; box-drawing is terminal-only and costs ~3x the tokens for equivalent info.

## 5. Critical rules
<!-- scope: meta -->

1. **`LESSONS.md` and `TOKEN-LOG.md` are append-only** — never edit old entries; only append (ADR-29, ADR-39)
2. **`JOURNAL.md` is append-only newest-first** — prepend at session wrap or workday close
3. **ADRs, transcripts, handoffs, audits are immutable** — supersede with a new file or in-file marker; never edit in place
4. **Layer 2 never executes** — no orchestration scripts; `scripts/` contains read-only validators only (ADR-28, ADR-36)
5. **No new markdown files without checking navigation/growth triggers** — when navigation overhead emerges, evaluate DevVault migration. Root `README.md` deleted 2026-05-23 (deprecated per ADR-38 amendment A5; redundant with VISION + CLAUDE.md + ARCHITECTURE for this internal-only repo) — do not recreate it.
6. **Keep files consistent** — ESSENTIALS summarizes PLAYBOOK, not copies it; divergence causes drift
7. **No executable rules in this repo** — those go in `~/.claude/` with `verify:` lines
8. **Do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`** — deleted 2026-05-16; git history + JOURNAL `Changes:` line replace CHANGELOG

## 6. Session start protocol
<!-- scope: runtime -->

1. `/boot` (loads skills, memory, recent commits)
2. `git status` — clean working tree?
3. `git log --oneline -5` — recent context
4. Read most recent handoff if continuing prior session
5. Check `BACKLOG.md` for in-progress items
6. `pytest --collect-only` — test discovery sanity check
7. Wait for Rob's prompt — never improvise

If any check fails → stop and ask Rob before proceeding.

Verify after updates: ESSENTIALS ↔ PLAYBOOK alignment; ENVIRONMENT ↔ `~/.claude/` state; SESSION_SETUP ↔ PLAYBOOK process changes; JOURNAL reflects last session.

## 7. Slash commands available
<!-- scope: runtime -->

User-level (`~/.claude/commands/`):
- `/session-summary` — generate token-efficient session summary + handoff
- `/boot` — load context (skills, memory, recent commits)
- `/save` — stage + commit with Conventional Commits message

Repo-level (`./.claude/commands/`):
- `/save` — commit workflow with full body per git-discipline rule
- `/handoff` — generate/complete handoff per ADR-42 v3.3.3 three-stage flow

## 8. Skills active
<!-- scope: runtime -->

User-level (`~/.claude/skills/`):
- `gotchas` — universal dev gotchas (encoding, shell safety, test pitfalls)
- `boot`, `session-summary`, `handoff`, `save` — session lifecycle skills

Repo-level (`./.claude/`):
- No repo-level skills directory exists yet (`.claude/` holds `commands/` and `rules/` only). Repo-specific empirical patterns live in `LESSONS.md` (append-only) — read it before structural changes; universal gotchas are the user-level `gotchas` skill above. If a repo-specific gotchas skill is later added it goes under `.claude/skills/gotchas/`.

## 9. Hooks active
<!-- scope: runtime -->

Pre-commit (`.pre-commit-config.yaml`):
- `ruff check --fix` — Python linting
- `normalize_headers.py` — dated-log header normalization

Rules (`.claude/rules/`):
- `git-discipline.md` — mandatory commit after every file edit; clean working tree at session end

## 10. Anti-patterns specific to Claude Code in this repo
<!-- scope: meta -->

- **Editing old LESSONS.md or TOKEN-LOG.md entries** — append-only; editing corrupts the institutional record
- **Adding orchestration scripts** — Layer 2 invariant: validators only, no scripts that drive state in child repos
- **Narrating or managing AGENTS.md** — AGENTS.md is retired (ADR-53); CLAUDE.md is the single instruction file
- **Duplicating content between files** — ESSENTIALS summarizes PLAYBOOK, not copies; drift is the failure mode
- **Putting executable rules in this repo** — those belong in `~/.claude/` with `verify:` lines
- **Running validators with no args** — vacuous pass; always pass `--all` or specific paths

## 11. Recent ADRs binding here (last 5)
<!-- scope: meta -->

Brief one-liners. Full list in `docs/decisions/README.md`; full governance list in `ARCHITECTURE.md`.

- ADR-57: Two-layer bundle contract — handoff bundle = browser-readable layer + Claude-runnable layer
- ADR-58: Structured claims verification — handoff applied-task gate + structured ratification protocol
- ADR-59: Universal visual repository pattern — dot-prefix configs + ALL-CAPS canonical roots + workspace sort settings (audit-enforced via checks #4–#6)
- ADR-60: docs/ folder taxonomy — two-variant semantic role per subfolder + 2026-05-28 baseline-folder-uniformity addendum
- ADR-61: Git worktree for parallel CC sessions — same-repo parallel requires `git worktree add`; different-repo parallel is safe without

## 12. Section history
<!-- scope: meta -->

- v1.0 (2026-04-24) — initial thin-pointer CLAUDE.md per Gap #5
- v2.0 (2026-05-19) — ADR-53: retire thin-pointer/AGENTS.md framing; CLAUDE.md becomes substantive single canonical per-repo agent-instruction file
- v2.1 (2026-05-19) — add §3 Architecture, §4 Conventions; renumber; migrate content from AGENTS.md per ADR-53 Decision 2
- v2.2 (2026-05-24) — self-audit fix (E1): §8 repo-level skills bullet corrected — no `.claude/skills/` dir exists; repo gotchas live in LESSONS.md
- v2.3 (2026-05-28) — §11 ADR list rotated to most-recent 5 (57–61) per the file's own "last 5" header; durability-audit clear-gap C3

---

**Last updated:** 2026-06-01
**Maintained by:** Rob
