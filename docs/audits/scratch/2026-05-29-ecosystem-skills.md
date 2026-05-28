# Ecosystem Skills Audit — scratch (2026-05-29)

<!-- scope: meta -->

Overnight ecosystem-coherence audit, Phase 1. Read-only sweep of CC skills +
commands accessible from `.dev-knowledge`. Findings → BACKLOG; no edits to
`~/.claude/` runtime config (out of scope per CLAUDE.md §4).

## Inventory (Dimension A)

| Location | Items | Type |
|---|---|---|
| `~/.claude/skills/` | `gotchas/` (SKILL.md + gotchas.md), `verify/` (SKILL.md + cross-repo-boundaries.ps1) | user skills |
| `~/.claude/commands/` | `boot.md`, `codex-review.md`, `evolve.md`, `session-summary.md` | user commands |
| `.dev-knowledge/.claude/commands/` | `handoff.md`, `save.md` | repo commands |
| `.dev-knowledge/.claude/rules/` | `git-discipline.md` | repo rule |

Freshness: gotchas last-triggered dates span 2026-03-25 … 2026-05-23 (live).
`verify/cross-repo-boundaries.ps1` header "Last validated: 2026-03-28".

## Findings

| ID | Sev | Dim | Evidence (file:line) | Description | Fix scope | Owner |
|---|---|---|---|---|---|---|
| SK-1 | medium | B | `CLAUDE.md:§7` vs `~/.claude/commands/` | §7 lists user-level commands as `/session-summary`, `/boot`, `/save`. Reality: `~/.claude/commands/` has boot, codex-review, evolve, session-summary — **no `save`** at user level (save is repo-level only). `/codex-review` and `/evolve` exist but are undocumented in §7. | Update CLAUDE.md §7 to match disk (add codex-review, evolve; move /save to repo-level list). | self |
| SK-2 | medium | B | `CLAUDE.md:§8` vs `~/.claude/skills/` | §8 lists user-level **skills** as gotchas, boot, session-summary, handoff, save. Only `gotchas` + `verify` are actual SKILL.md skills; boot/session-summary/handoff/save are **commands**, not skills. The `verify` skill is omitted entirely. §8 conflates skills with commands. | Rewrite CLAUDE.md §8: skills = gotchas + verify; move boot/session-summary/handoff/save to the commands inventory (§7). | self |
| SK-3 | medium | C | `~/.claude/commands/boot.md:7-19`; global `~/.claude/CLAUDE.md` Self-Evolution Protocol §2/§5 | boot.md tails `sessions.jsonl`, `violations.jsonl`, `corrections.jsonl`; the Self-Evolution Protocol also references `observations.jsonl`. **None exist** — `~/.claude/memory/` holds only `learned-rules.md`, `evolution-log.md`, `README.md`. Graceful-degrades via `||`, so not breaking, but session-trend + correction-promotion machinery is **vacuous** (SessionStart hook reports "Corrections: 0"). | Either create the .jsonl logs (runtime) or update boot.md + protocol to use `evolution-log.md`. | ~/.claude (runtime) |
| SK-4 | low | C | `~/.claude/skills/verify/cross-repo-boundaries.ps1:1-30` | Validator hard-codes `corp-monorepo/packages/{corp-knowledge-extractor, corp-os-meta, corp-by-os}` import-boundary layout; "Last validated 2026-03-28". Whether that package layout still holds is a corp-monorepo question (Phase 5). If the layout drifted, the validator silently passes (Get-ChildItem on missing path → no errors). Low confidence pending Phase 5. | Re-validate script against current corp-monorepo layout; add a "packages root missing" guard. | ~/.claude + corp-monorepo |
| SK-5 | low | D | (inferential — no file) | Gap: no `SessionStop`/`SessionEnd` lifecycle hook for session-close automation (clean-tree check, JOURNAL nudge, audit.py health). Overlaps the existing BACKLOG P2 "Hooks audit" item; detailed in Phase 2. Low confidence (may be intentional). | Evaluate a SessionStop hook (Phase 2). | self |

## Notes

- Dimension C spot-checks: `boot.md` (traced — coherent except SK-3 dangling logs);
  `gotchas.md` (entries match their `verify:` lines, dates live); `handoff.md` (just
  rewritten to v3.4 this session — coherent by construction).
- SK-1/SK-2 are the same root cause as the cross-doc drift audited in Phase 6:
  CLAUDE.md's self-description of its own tooling has drifted from disk.
- All findings are documentation/runtime-config drift; **zero are breaking**. No skill
  fails to do what its description claims; the description *inventory* in CLAUDE.md is
  what's stale.
