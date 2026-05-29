# Ecosystem Hooks Audit — scratch (2026-05-29)

<!-- scope: meta -->

Overnight ecosystem-coherence audit, Phase 2. Satisfies the audit portion of the
BACKLOG P2 "Hooks audit + lifecycle-hook workflow-automation patterns" item.
Read-only sweep; findings → BACKLOG; no edits to `~/.claude/` or sibling repos.

## Inventory (Dimension A)

**Pre-commit per repo:**

| Repo | Pre-commit hooks | ruff enforced? |
|---|---|---|
| `.dev-knowledge` | `normalize-dated-headers`, `codemap-freshness` (both local) | **no** |
| `corp-monorepo` | `ruff` (astral-sh ruff-pre-commit `v0.15.8`), `tach-check`, `normalize-headers` (local) | yes |
| `ai-council` | `normalize-headers` (local) only | no |
| `corp-ops` | **none** (no `.pre-commit-config.yaml`) | no |
| `corp-sca-time-automation` | **none** (no `.pre-commit-config.yaml`) | no |

**Claude Code lifecycle hooks (`~/.claude/settings.json`):**

| Event | Hook | Purpose |
|---|---|---|
| PreToolUse (Bash) | `block-onedrive.ps1` | enforces OneDrive exclusion zone (P0) — coherent ✓ |
| SessionStart | echo `[EVOLUTION] …` | counts learned-rules + corrections, nudges `/boot` |
| Stop | `claude-notify.ps1` + echo `[EVOLUTION] …` | desktop notify + "log corrections/observations + write scorecard" reminder |

`~/.claude/hooks/` holds only `block-onedrive.ps1`.

## Findings

| ID | Sev | Dim | Evidence | Description | Fix scope | Owner |
|---|---|---|---|---|---|---|
| HK-1 | medium | B/D | `CLAUDE.md:§9` + `§4` vs `.pre-commit-config.yaml` | CLAUDE.md §9 ("Pre-commit: `ruff check --fix`") and §4 ("Linting: `ruff check --fix` (pre-commit)") claim ruff is a pre-commit hook. It is **not** in `.pre-commit-config.yaml` (only normalize-dated-headers + codemap-freshness). ruff runs by manual convention, not enforced. corp-monorepo *does* enforce ruff via pre-commit — so the doc claims an enforcement the repo lacks and that diverges from the sibling that has it. | Either add the ruff pre-commit hook to `.dev-knowledge` OR correct CLAUDE.md §9/§4 to say ruff is manual/convention. Decide in a focused session. | self |
| HK-2 | medium | C | `~/.claude/settings.json` SessionStart + Stop; `~/.claude/memory/` | The evolution hooks count/echo from `corrections.jsonl` / `sessions.jsonl`, which **do not exist** (only `learned-rules.md` + `evolution-log.md`). SessionStart always reports "Corrections: 0"; the Stop reminder to "write scorecard to sessions.jsonl" has no existing sink. Same root cause as skills SK-3. The evolution loop is wired but its data store is absent. | Create the .jsonl logs OR repoint hooks + Self-Evolution Protocol to `evolution-log.md`. | ~/.claude (runtime) |
| HK-3 | medium | C | `~/.claude/settings.json` Stop hook; BACKLOG "no SessionStop hook today" | A Stop hook exists (notify + echo) but performs **no functional session-close automation**. BACKLOG's "no SessionStop hook today" is imprecise (one exists) but its intent holds. Concrete automation use cases (Dim C): (1) Stop → `git status`, warn on dirty tree (enforces git-discipline rule); (2) Stop → `audit.py health`, surface non-7/7; (3) handoff-trigger PreToolUse → flag dirty tree before Stage 1 capture; (4) SessionStart → auto-surface latest JOURNAL entry (today only via manual /boot). | Design 1-2 of these as a focused hooks session. Layer-2 caveat: read-only checks/notify only, no state-driving orchestration. | self / ~/.claude |
| HK-4 | low | A/D | per-repo configs above | Hook coverage + naming inconsistent across the ecosystem: corp-ops + corp-sca-time-automation have **no** pre-commit at all; ai-council has only normalize-headers; only corp-monorepo enforces ruff/tach. The shared header-normalizer is `normalize-dated-headers` in `.dev-knowledge` but `normalize-headers` elsewhere (naming drift for the same intent). | Decide a baseline pre-commit floor for all active repos (at minimum the header normalizer); align the hook id name. Per-repo owners. | corp-ops, corp-sca-time-automation, ai-council |

## What works (no finding)

- `block-onedrive.ps1` PreToolUse hook correctly guards the P0 OneDrive exclusion.
- `.dev-knowledge` pre-commit (`normalize-dated-headers` + `codemap-freshness`) runs
  green on every commit this session.

## Notes

- HK-1 is the highest-value hooks finding: a load-bearing convention (ruff lint) is
  *documented as enforced* but is actually manual — a session could commit ruff
  violations and the doc would imply they were blocked.
- HK-2 overlaps skills SK-3 and Phase 7 (memory/feedback) — same missing-.jsonl root.
