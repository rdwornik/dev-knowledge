# NIGHT-VERDICT SHEET — P0 + P1 E2E regression (2026-07-17 night)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-17
- **Source:** 2026-07-17 night-run scratchpad (`NIGHT-VERDICT-SHEET.md`), content unchanged below this block.
- **Night rule:** the run was READ-ONLY / zero-commit — no writes to any real repo tree; all
  outputs went to scratchpad. This docs-only arc (branch `docs/2026-07-17-night-audit`, filed
  2026-07-18) is its first commit.
- **Companion night-run audits (same arc):** `2026-07-17-technical-night-verdict-sheet.md`, `2026-07-17-technical-night-divergence-ledger.md`, `2026-07-17-technical-night-live-fire-sheet.md`, `2026-07-17-technical-night-handoff-evidence-pack.md`.

Session: hub `.dev-knowledge`, CC Opus 4.8 (1M), effort xhigh. ZERO commits, ZERO writes to any
real repo tree. All outputs in scratchpad.

## P0 — Preflight (roots resolved live via `git rev-parse --show-toplevel`)

| repo | root | HEAD (at P0) | branch | tree |
|---|---|---|---|---|
| hub | `C:/Users/1028120/Documents/Dev/.dev-knowledge` | `e0cbffdb` | main (synced origin/main) | CLEAN |
| corp | `C:/Users/1028120/Documents/Dev/corp-monorepo` | `560a38d` | `docs/2026-07-17-night-process-audit` (0/0 vs main) | CLEAN |
| ai-council | `C:/Users/1028120/Documents/Dev/ai-council` | `3862749` | main (synced) | CLEAN |

**P0 gate: PASS** — no dirty trees, no genuine in-progress ops. Two notes:
- hub carried a stale `REBASE_HEAD` **ref** (leftover from a completed rebase — no
  `rebase-merge/`/`rebase-apply/` dir; `git status -sb` showed a normal branch line). Benign.
- corp was checked out on a night-audit **feature branch** at exactly main's tip (0/0),
  clean — the first sign of a **concurrent night session** (see LIVE-FIRE-SHEET "fleet-not-quiescent").

## P1 — E2E regression of everything shipped today

| # | Check | Grade | Verbatim evidence |
|---|---|---|---|
| P1.1 | `audit.py ship-gate` | **PASS** | `ship-gate: GREEN — verification organs green against this arc (14 WARN dispositioned)` — 0 new, no `[stale]`. Exactly the expected 14 dispositioned (3 no_ff + 1 reconciled_versions + 4 doc_rot + 6 undeclared_edges). |
| P1.2 | `fleet_parity.py --run-date 2026-07-17` | **PASS** | `3 repo(s) walked: 161 at-parity, 20 pass-declared, 1 gate-ahead-declared, 0 warn-undeclared, 0 must-absent, 0 tombstone-violated, 0 advisory-rewarn, 0 stale, 0 refused` · `ownership (ADR-103): 52 methodology-generic, 9 project, 12 conditional`. Matches the target tally exactly. |
| P1.3 | full `pytest` + targeted | **PASS** | `1589 passed, 3 skipped in 1058.46s`, exit 0. Targeted `tests/test_fleet_parity.py` completed exit 0 (ownership + no-fork + live-manifest-zero-refusal pins green). |
| P1.4 | ADR-29 canon coherence (6 touchpoints) | **PASS** | All 6 consistent + **ratified**. See breakdown below. |
| P1.5 | roster/index coherence | **PASS (1 honest note)** | recent-adrs `99..103` ✓; doc-counts `1592 collected` = `1589 passed + 3 skipped` ✓, `29 checks`, `15 gates`; audits index coherent. NOTE below. |

### P1.4 — ADR-29 chronological legacy-archival split, 6 touchpoints (all CONSISTENT + RATIFIED)

1. **ADR-29** (`docs/decisions/ADR-29-lessons-grandfathering.md`): amendment marker L58; SANCTIONED = chronological legacy split, STILL REJECTED = by-scope/by-topic (L70–71). **L126 `**Ratified 2026-07-17** — operator ruling (core-invariant #6)`** appended (not in-place edit; ADR-88/89 pattern) — enumerates the full atomic set. ✓
2. **CLAUDE.md** §4/§5/§10 — byte-identical to the lockstep region extracts:
   - `templates/claude-regions/critical-rules-records.md` line 1 == CLAUDE.md §5 record 1 (exact string match). ✓
   - `templates/claude-regions/antipatterns-universal.md` line 2 == CLAUDE.md §10 anti-pattern (exact string match). ✓
3. **ARCHITECTURE.md** L108–111 (append-only rule w/ LESSONS-legacy exception) + Ch5 table L530. ✓
4. **PLAYBOOK.md** L922 (LESSONS row) + L3258 (growth trigger: "NOT a by-topic / by-scope split — that stays rejected"). ✓
5. **ADR-39** L403–416 — six-element `LESSONS-legacy-<span>.md` file-class registry entry. ✓
6. **README** (`docs/decisions/README.md`) L16 ADR-29 row: "amended 2026-07-17 — chronological legacy-archival split sanctioned (`LESSONS-legacy-<span>.md`; distinct from the still-rejected by-scope split)". ✓

No spot describes the current sanction as by-topic; every by-topic mention correctly labels it the *rejected* alternative. **LESSONS.md content unmoved (241 entries < 300 threshold — the move is [#339]'s build leg).**

### P1.5 — honest note

The prompt anticipated "today's **two** codex artifacts" in `docs/audits/README.md`; the index in
fact lists **four** dated 2026-07-17 — `codex-role-governance`, `codex-gate-rev-axis`,
`codex-arc3-ownership-axis`, `codex-adr29-legacy-split-amendment`. The index is **coherent with
disk** (regen-and-diff gated by `audit-index-freshness`), so this is a prompt **undercount**, not
index rot. gate-rev-axis ↔ ADR-102, arc3-ownership-axis ↔ ADR-103, adr29-legacy-split ↔ the ADR-29
amendment; role-governance is the fourth.

## Overall P1 verdict: **GREEN across the board.** Everything shipped today regresses clean.
