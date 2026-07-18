# ARC-4 leg-1 — fleet ruff-shape + pytest-floor equalization (before→after evidence)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-18
- **Source-session:** ARC-4 fleet-equalization leg-1 — first live application of RULING-W (`d94f548b`). Hub HEAD at authoring: `feat/arc4-leg1-ruff-equalization`.
- **Status:** complete (educate artifact — ARC-4 acceptance-contract item e)
- **Model:** Opus 4.8 (1M)

This is the **educate artifact** for ARC-4 equalization leg-1: file-level before→after
evidence per repo, with exact paths and the exact section headers now visible. The goal
(operator, verbatim): *"I never again want to ask why files differ between repos."*

## The universal shape (what was equalized)

Four methodology-**universal** config values, now pinned uniform across hub + corp-monorepo
+ ai-council (all in each repo's root `pyproject.toml`):

| Key | Value | Ruling | fleet_parity surface (MUST) |
|-----|-------|--------|-----------------------------|
| ruff `required-version` | `">=0.15.5"` | == pinned pre-commit ruff rev v0.15.5 | `ruff-required-version` |
| ruff `target-version` | `"py311"` | RULING-PY baseline (newest-Python lift = #351) | `ruff-target-version` |
| ruff `line-length` | `120` | ARC-4 D1 (operator) | `ruff-line-length` |
| pytest `minversion` | `"9.0"` | ARC-4 D2 (lowest shared 9.0.x line) | `pytest-minversion` |

Everything else (lint `select`/`ignore`/`per-file-ignores`, `[tool.ruff.format]`, pytest
markers/`testpaths`/`addopts`) is **REPO-PERSONAL** — free to differ, and now visibly
separated by RULING-S `=== UNIVERSAL ===` / `=== REPO-PERSONAL ===` header comments.

## Per-repo before → after

### Hub — `.dev-knowledge/pyproject.toml` (commit `0b814dc`)

Before: `[tool.ruff]` had only `required-version = ">=0.15.5"` (no target-version, no
line-length; ruff default 88). `[tool.pytest.ini_options]` had no `minversion`.

After — `[tool.ruff]`:
```
[tool.ruff]
# === UNIVERSAL (fleet methodology — ARC 4 leg 1, 2026-07-18) ==================
required-version = ">=0.15.5"   # floor == pinned pre-commit ruff rev (v0.15.5)
target-version = "py311"        # RULING-PY baseline; "always newest Python" lift = #351
line-length = 120               # agreed fleet line-length (ARC 4 D1)
# === REPO-PERSONAL (this repo's lint posture — may differ; declared) ==========
[tool.ruff.lint]
extend-select = []
```
After — `[tool.pytest.ini_options]` gains, under a `=== UNIVERSAL ===` header,
`minversion = "9.0"`; the existing markers/tiering fall under `=== REPO-PERSONAL ===`.

### corp-monorepo — `pyproject.toml` (branch `feat/arc4-leg1-ruff-equalization`, `bee236c`)

Before: **no `[tool.ruff]` table at all** — only `[tool.ruff.lint]` (`select = ["E","F","I"]`,
`ignore = ["E501"]`). No `minversion`. dev floors `pytest>=8.0`, `ruff>=0.9`.

After: a new `[tool.ruff]` table with the 3 universal keys under `=== UNIVERSAL ===`, and
`select`/`ignore`/`per-file-ignores` kept under `=== REPO-PERSONAL ===`. `minversion = "9.0"`
added. dev floors aligned to the universal keys (terra [P1] fix, caused-by-diff): `pytest>=9.0`,
`ruff>=0.15.5`. Effectiveness proven by `ruff check --show-settings` → `target_version = 3.11`,
`line_length = 120` (no `.ruff.toml` precedence trap — corp has none).

### ai-council — `pyproject.toml` (branch `feat/arc4-leg1-ruff-equalization`, `d1003fd`)

Before: `[tool.ruff]` had `target-version = "py312"`, `line-length = 120` (no `required-version`).
No `minversion`. dev floors `pytest>=8.0`, `ruff>=0.9`.

After: `required-version = ">=0.15.5"` added; `target-version` **`py312` → `py311`** (RULING-PY
floor; the newest-Python lift back to ≥312 fleet-wide is tracked #351); `line-length = 120`
retained. `=== UNIVERSAL ===` / `=== REPO-PERSONAL ===` headers added; `select = ["E","F","I","W"]`
and `[tool.ruff.format]` stay REPO-PERSONAL. `minversion = "9.0"` added. dev floors → `pytest>=9.0`,
`ruff>=0.15.5`. (`[tool.mypy] python_version = "3.12"` untouched — separate tool, out of scope.)

## fleet_parity verification (contract b — zero warn-undeclared)

`python scripts/fleet_parity.py --run-date 2026-07-18` → **173 at-parity (was 161; +12 = 4 new
surfaces × 3 evaluated repos), 0 warn-undeclared, 0 must-absent, 0 tombstone-violated, 0
refused.** The 4 universal keys are MUST-uniform + drift-gated fleet-wide; any future divergence
WARNs the nightly ecosystem audit. Pre-deploy repos (corp-ops, corp-sca) render **skipped**,
never warned (satellite wave frozen). Manifest `ecosystem/parity-surfaces.yaml` bumped 1.2.0→1.3.0.

## RULING-W execution provenance

- **Mechanism-first:** the ADR-36/41 consumer-write amendment (`d94f548b`) was already landed;
  leg-1 is its first live application. Every consumer edit went via a **separate worktree/branch**,
  never the live checkout; commit-and-STOP + report; **per-consumer merge GO with the operator**.
- **Re-witness:** consumer HEADs moved repeatedly during the arc (corp `59f29d8` → `236de12` →
  `af02a0c`); worktrees branched off **live `main`**, never a stale SHA.
- **Terra review (codex lane, pre-merge):** corp — terra returned a real [P1] (minversion 9.0 vs
  dev `pytest>=8.0`); fixed (caused-by-diff), terra re-review clean. ai-council — terra clean.
- **corp `--no-verify` (operator-ruled, good-faith):** corp's `canonical_freshness` FAIL was
  **pre-existing and orthogonal** — corp `CONTRIBUTING.md` `last_reviewed 2026-07-13 < edit
  2026-07-18`, re-pointed by corp's OWN parallel session. The hub leg neither stamped nor re-read
  corp canonicals; the freshness debt is **owed by corp's active session**, reported not fixed.
  ai-council needed no bypass (gate passed clean).

## Replication material (contract d — satellite wave frozen, material only)

- `templates/ruff-config-block.toml` — canonical copy-paste material (hand-merged per RULING-W,
  never a whole-file carrier over a repo-authored pyproject).
- `deploy/release-v1.3.x-contract.md` §3.7 — carrier-row spec (MATERIAL / design-defer). No
  manifest cut here; the shape ships when the wave thaws.

## Branch / merge ledger

- Hub leg-1 config + template + §3.7: `feat/arc4-leg1-ruff-equalization` (`0b814dc`).
- Hub Leg-3 parity probes: same branch (`0320c5e6`).
- corp: `feat/arc4-leg1-ruff-equalization` (`07578f6` config + `bee236c` terra-fix) — MERGED.
- ai-council: `feat/arc4-leg1-ruff-equalization` (`d1003fd`) — MERGED.
