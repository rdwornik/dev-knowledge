# Changelog review — claude-code 2.1.168 + codex 0.137.0

**Date:** 2026-06-07 · **Type:** operator-invoked `/changelog-review` (#113 PUSH) · **Trigger:** SessionStart sentinel fired `[changelog] claude-code 2.1.168 > last reviewed 2.1.167`. First real run of the command — also the live witness for #113.

## Scope reviewed

- **claude-code:** `2.1.168` only (the sole version header > last_reviewed `2.1.167`; 2.1.168 is the newest published). Source: raw CHANGELOG.md.
- **codex:** `0.137.0` only (the sole **stable** > `0.136.0`; 0.138.0-alpha.* skipped — pre-releases). Source: `gh release view rust-v0.137.0 -R openai/codex`.

## Sentinel witness (both branches, one boot)

- **Fired:** claude-code (installed 2.1.168 > reviewed 2.1.167).
- **Silent:** codex (installed 0.136.0 == reviewed 0.136.0 — current).

That single live boot exercised both sentinel branches, as designed.

## Bucket counts

- ADOPT: **1** (codex update → already owned by #119)
- OBSOLETES-WORKAROUND: **0**
- STALE-NAMES: **0 actionable** (1 checked-and-clean)
- VERIFY: **0 new**
- NOISE-count: claude-code 2.1.168 (1 opaque entry) + codex 0.137.0 (~123 of ~125 PRs)

Low-yield by nature: 2.1.168 is a bugfix-only CC release, and codex 0.137.0's only stack-relevant content was already captured. The review's value is that it **clears the sentinel** and confirms no *new* adoption is owed.

## ADOPT

- **codex 0.136.0 → 0.137.0** — carries the Windows-x64 SQLite startup stability fix (#25490) + "preserve auto-review approval policy in `codex exec`" (#23763), plus Windows reliability companions (thread-resume path normalization #25509, setup-helper UAC manifest #25949, startup stack-pressure #25844/#25847). Directly relevant to our `codex exec --sandbox read-only` wrapper on Windows.
  - **Already owned by [#119]** (codex currency: 0.136.0 → 0.137.0 via `codex update`). No new BACKLOG item. → operator/architect decision: when to run the update.

## OBSOLETES-WORKAROUND

None. Nothing in 2.1.168 / 0.137.0 retires an artifact we hand-built.

## STALE-NAMES

- **CLEAN.** codex 0.137.0 removed the experimental `persist_extended_history` flag (#25712). We reference it **nowhere** — the codex/pre-commit gotcha watch-list already records it as removed-0.137 and confirms our config/wrapper use none of the deprecated keys (verified 2026-06-07). No `file:line` drift.

## VERIFY

No new live-checks. (The codex-max audit's standing VERIFY — raise review `model_reasoning_effort` to high/xhigh — remains queued under #82, not re-opened here.)

## NOISE-count (counted, not itemized)

- **claude-code 2.1.168:** 1 entry — *"Bug fixes and reliability improvements"* (opaque; no doc-able feature, no rubric hit).
- **codex 0.137.0:** ~123 of ~125 PRs — all 6 New-Feature groups (multi-agent v2, remote-control app-server RPCs, plugin catalog/`plugin list --json`, enterprise/EDU credit limits + cloud config bundles, TUI F13–F24 / paste-in-menus, hosted web/image code-mode tools), the 5 chore groups (Bazel/CI, Python SDK wheels, Justfile/formatting, crate-splitting), and the doc groups (app-server schema, codex's own AGENTS.md conventions). Irrelevant to a solo `codex exec --sandbox read-only` reviewer on gpt-5.5.

## Operator routing

- **One decision flagged:** the codex 0.137.0 update (#119) — already on the backlog; this review confirms it's the only adoption-worthy item in the window and worth doing for the Windows SQLite fix. Route to operator + browser architect per ADR-28. The command implements nothing.

State bumped: `ecosystem/tool-versions.yaml` → claude-code `2.1.168`, codex `0.137.0`, reviewed_date `2026-06-07`. Sentinel now silent for both.
