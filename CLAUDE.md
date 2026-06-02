---
last_reviewed: 2026-06-02
status: active
owner: Rob
---

# CLAUDE.md — Dev Knowledge
<!-- scope: meta -->
<!-- version: 2.9 — 2026-06-02 -->

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
- **Linting:** `ruff check --fix` (manual / via `/save`); `ruff check` is also enforced as a pre-commit gate (see §9) — violations block commits
- **Scope tags:** `<!-- scope: X -->` (`dev|llm|hybrid|runtime|meta`) — informal only; not enforced (ADR-27; enforcement withdrawn per ADR-48)
- **File lifecycle:** Append-only: `LESSONS.md`, `logs/TOKEN-LOG.md` (never edit), `JOURNAL.md` (newest-first prepend). Immutable: ADRs, transcripts, handoffs, audits (supersede with new file). Living: `VISION.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `protocols/*.md`, `BACKLOG.md` (update in place).
- **Freshness cadence:** the living docs `VISION/ARCHITECTURE/CLAUDE/CONTRIBUTING` carry a `last_reviewed` frontmatter stamp meaning *re-read end-to-end and confirmed accurate (or drift filed)* — **not** merely "touched". `audit.py` check #10 fails when a stamp predates the file's last edit (edited-but-not-re-reviewed) and warns past a 30-day backstop. Bump `last_reviewed` only after a genuine review. See PLAYBOOK "Canonical-file freshness cadence".

**Out of scope for this repo:**
- Code-level implementation → child repos (corp-monorepo, ai-council, etc.)
- Client/product/domain knowledge → Obsidian vault
- Project-specific CLAUDE.md content → each repo owns its own
- Claude Code runtime config → `~/.claude/`
- Council debate transcripts originate in `ai-council/`; they archive here in `docs/decisions/transcripts/`

- **Output formatting (render-layer):** Claude does **not** emit box-drawing glyphs — the Claude Code TUI *paints* plain markdown pipe-tables (`| col | col |`) as Unicode borders (`┌─┬─┐ │ └─┴─┘`) **client-side at render time**. So a bare table looks clean in the terminal but copies into browser chat as costly border glyphs (~3× the tokens), and a rule that merely bans Claude from *writing* box-drawing is a no-op (Claude already doesn't). The working fix is at the render layer: any report the operator copies out must be (1) **flat** — plain markdown or `key: value` / bullet lists, no column-padding spaces — **and** (2) **wrapped in a triple-backtick code fence**, which makes the TUI render it raw/un-painted so the copied text carries no borders. Same fenced-block discipline already used for Scale-S snippets (ESSENTIALS) and downloadable prompts (§2). Persistent diagrams in `ARCHITECTURE.md` are mermaid (ADR-51/ADR-59), out of scope. Full rationale + `/session-summary` reconciliation: PLAYBOOK §8 "Output the operator copies into browser chat".

## 5. Critical rules
<!-- scope: meta -->

1. **`LESSONS.md` and `logs/TOKEN-LOG.md` are append-only** — never edit old entries; only append (ADR-29, ADR-39)
2. **`JOURNAL.md` is append-only newest-first** — prepend at session wrap or workday close
3. **ADRs, transcripts, handoffs, audits are immutable** — supersede with a new file or in-file marker; never edit in place
4. **Layer 2 never executes** — no orchestration scripts; `scripts/` contains read-only validators only (ADR-28, ADR-36)
5. **No new markdown files without checking navigation/growth triggers** — when navigation overhead emerges, evaluate DevVault migration. Root `README.md` deleted 2026-05-23 (deprecated per ADR-38 amendment A5; redundant with VISION + CLAUDE.md + ARCHITECTURE for this internal-only repo) — do not recreate it.
6. **Keep files consistent** — ESSENTIALS summarizes PLAYBOOK, not copies it; divergence causes drift
7. **No executable rules in this repo** — those go in `~/.claude/` with `verify:` lines
8. **Do not recreate `CHANGELOG.md` or `BACKLOG_ARCHIVE.md`** — deleted 2026-05-16; git history + JOURNAL `Changes:` line replace CHANGELOG
9. **No leftovers** — any automated or scratch-creating process (parallel-session worktree, night-agent run per ADR-68, temp file) removes **and verifies removal of** everything it created before it counts as done; cleanup fires even on abort. The provision→cleanup round-trip must leave the tree identical. See PLAYBOOK §Session-boundaries "No leftovers" (the `.dev-knowledge-*` orphans are the failure it prevents)

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
- `/evolve` — evolution audit: promote/prune/graduate learned rules (weekly / ~10 sessions)
- `/codex-review` — invoke Codex review on a staged **code** diff (code only)

Repo-level (`./.claude/commands/`):
- `/save` — commit workflow with full body per git-discipline rule
- `/handoff` — generate/complete handoff per `HANDOFF_PROCESS.md` v4 two-phase flow (ADR-62)
- `/review-closures` — review the session-end closure proposals + execute ONLY operator-approved closures (ADR-70 Tier-1; human-gated, done-items-leave). Added by [#8]

(When to invoke each + auto-vs-manual for hooks: PLAYBOOK §"Usage protocol: which command / hook, when".)

## 8. Skills active
<!-- scope: runtime -->

User-level (`~/.claude/skills/`):
- `gotchas` — universal dev gotchas (encoding, shell safety, test pitfalls)
- `verify` — domain-specific verification scripts for the ecosystem (run after `pytest`)

(`boot`/`session-summary`/`handoff`/`save` are **commands**, not skills — see §7; current Claude Code also surfaces commands in its skill picker, but their files live under `commands/`, not `skills/`.)

Repo-level (`./.claude/`):
- No repo-level skills directory exists yet (`.claude/` holds `commands/` and `rules/` only). Repo-specific empirical patterns live in `LESSONS.md` (append-only) — read it before structural changes; universal gotchas are the user-level `gotchas` skill above. If a repo-specific gotchas skill is later added it goes under `.claude/skills/gotchas/`.

## 9. Hooks active
<!-- scope: runtime -->

Pre-commit (`.pre-commit-config.yaml`):
- `normalize-dated-headers` — dated-log header normalization
- `codemap-freshness` — ARCHITECTURE codemap vs `scripts/` staleness check
- `validate-backlog` — BACKLOG.md story-map schema (ADR-66)
- `audit-health` — self-conformance gate: `audit.py health` (FAIL blocks the commit, WARN informs); added by [#69]
- `ruff` — lint gate: `ruff check` (gate mode; blocks on violations); version-pinned >=0.15.5 via `pyproject.toml`; `language: system` (no mismatch); added by [#13]
- `backlog-id-on-close` (commit-msg) — require `[#id]` when a commit removes a backlog task

Session hooks (`.claude/settings.json`, project-level — merges with, does not replace, the `~/.claude` hooks):
- `Stop` → `scripts/propose_closures.py` — ADR-70 Tier-1 session-end closure detector. Deterministic (no LLM), read-only: writes `logs/PROPOSALS-<date>.md` (gitignored) proposing backlog items whose closing-commit landed but never left the file; **detect-and-propose only — never mutates BACKLOG**; reviewed at next `/boot`. Non-blocking (exits 0). Added by [#8].
- `SessionStart` → `scripts/review_closures.py surface` — ADR-70 Tier-1. Read-only: prints a one-line "N closures proposed — run `/review-closures`" when the latest proposals file has candidates; silent otherwise. Non-blocking (exits 0). The review/approve/close half is the `/review-closures` command (§7). Added by [#8].

Rules (`.claude/rules/`):
- `git-discipline.md` — mandatory commit after every file edit; clean working tree at session end

## 10. Anti-patterns specific to Claude Code in this repo
<!-- scope: meta -->

- **Editing old LESSONS.md or logs/TOKEN-LOG.md entries** — append-only; editing corrupts the institutional record
- **Adding orchestration scripts** — Layer 2 invariant: validators only, no scripts that drive state in child repos
- **Narrating or managing AGENTS.md** — AGENTS.md is retired (ADR-53); CLAUDE.md is the single instruction file
- **Duplicating content between files** — ESSENTIALS summarizes PLAYBOOK, not copies; drift is the failure mode
- **Putting executable rules in this repo** — those belong in `~/.claude/` with `verify:` lines
- **Running validators with no args** — vacuous pass; always pass `--all` or specific paths

## 11. Recent ADRs binding here (last 5)
<!-- scope: meta -->

Brief one-liners. Full list in `docs/decisions/README.md`; full governance list in `ARCHITECTURE.md`.

- ADR-65: BACKLOG done-item disposition — git is the technical record, JOURNAL the per-session business record; refines ADR-64 Decision 1
- ADR-66: BACKLOG story-map hierarchy — Big Picture → Theme → User Story → Task; supersedes ADR-64 Decision 2 (flat layout)
- ADR-67: AI-Council process operationalization — six-step gated loop (Frame→Generate→Gate→Run→Verdict→Return); `/council-question` trigger; amends `AI_COUNCIL_PROCESS.md` v1.0
- ADR-68: Autonomous overnight review agent — local Task Scheduler → headless read-only review → morning briefing; ephemeral read-only worktrees (ADR-61)
- ADR-69: Cross-repo audit reach model — `audit.py` reaches child repos via a Layer-2 read-only cross-repo runner (`run` over the `ecosystem/` registry); commit-time enforcement stays self-only (the #72 residual)

## 12. Section history
<!-- scope: meta -->

- v1.0 (2026-04-24) — initial thin-pointer CLAUDE.md per Gap #5
- v2.0 (2026-05-19) — ADR-53: retire thin-pointer/AGENTS.md framing; CLAUDE.md becomes substantive single canonical per-repo agent-instruction file
- v2.1 (2026-05-19) — add §3 Architecture, §4 Conventions; renumber; migrate content from AGENTS.md per ADR-53 Decision 2
- v2.2 (2026-05-24) — self-audit fix (E1): §8 repo-level skills bullet corrected — no `.claude/skills/` dir exists; repo gotchas live in LESSONS.md
- v2.3 (2026-05-28) — §11 ADR list rotated to most-recent 5 (57–61) per the file's own "last 5" header; durability-audit clear-gap C3
- v2.4 (2026-06-01) — doc-coherence audit: §11 rotated to 64–68; §7 `/handoff` corrected to v4 two-phase; §9 pre-commit list corrected to actual hooks (drop unwired `ruff`, add `audit-health`/`validate-backlog`/`codemap-freshness`); §4 ruff marked manual; version comment synced
- v2.5 (2026-06-01) — process-hardening sweep: §4 output-formatting rewritten to the render-layer fix (G3); §5 critical rule #9 no-leftovers invariant (G5); §7 user-level command list corrected (+`/evolve`, +`/codex-review`, −`/save` which is repo-level) + usage-protocol cross-ref; §8 skills list corrected (+`verify`; clarify `boot`/`session-summary`/`handoff`/`save` are commands, not skills) (G6)
- v2.6 (2026-06-02) — backlog-groom currency fix: §11 "last 5" rotated 64–68 → 65–69 (add ADR-69 cross-repo audit reach model; drop ADR-64). Full end-to-end re-read confirmed the rest current as of the groom (the §4/§9 `#13` refs stay valid — #13 was re-scoped, not closed); `last_reviewed` re-stamped.
- v2.7 (2026-06-02) — ruff gate wired (#13 closes): §4 ruff description updated (now an enforced pre-commit gate); §9 pre-commit list updated (ruff hook added, [#13] removed parenthetical). Re-read end-to-end confirmed rest current; `last_reviewed` re-stamped.
- v2.8 (2026-06-02) — propose-closures Stop hook landed (ADR-70 Tier-1, advances #8): §9 gains a "Session hooks" subsection documenting the project-level `.claude/settings.json` Stop → `propose_closures.py` (detect-and-propose, never mutates BACKLOG). No other section changed; `last_reviewed` unchanged (re-read this session).
- v2.9 (2026-06-02) — closure loop made whole (ADR-70 Tier-1, advances #8): §7 adds the `/review-closures` repo command; §9 adds the `SessionStart → review_closures.py surface` hook. The review/approve/close half (human-gated, done-items-leave) complements Unit-2's Stop→propose. `last_reviewed` unchanged (re-read this session).

---

**Last updated:** 2026-06-02
**Maintained by:** Rob
