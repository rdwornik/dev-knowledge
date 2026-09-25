# Codex Review — transport-registry

**Date:** 2026-09-25
**Branch:** `worktree-lane-transport-registry`
**HEAD:** `cf724ac9`
**Diff range:** `2b5a4ef8..HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- lane-transport-registry (BATCH-WAVE5B-N1 #9), contract: LANE-5B-9-transport-registry.md
- new files: ecosystem/transport-registry.yaml, scripts/transport.py, tests/test_transport.py
- changed: scripts/handback.py (writer switch only -- its two direct transport writes now
  route through transport.write/transport.append), ecosystem/harness.yaml (one additive
  fates: line for scripts/transport.py)
- review scripts/transport.py's derive_kinds_from_code() heuristic (regex-based, not an AST
  parse) for soundness: false positives/negatives on the real scripts/ tree, and whether the
  write()/append() gate correctly refuses an unregistered kind or an unregistered writer
  before touching the filesystem
- confirm handback.py's behavior is unchanged for existing callers (its own test suite,
  tests/test_handback.py, passed unmodified)

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/transport.py:132 — Gate does not enforce the registered destination folder

**What:** `_check()` validates only `dest.name` and `writer`, ignoring `Kind.folder`.
**Why:** A registered writer can write `SESSION-*.md` into `to-cc/` or outside the transport entirely; this defeats the registry’s folder ownership and can recreate the wrong-folder failure the registry is meant to prevent.
**Fix direction:** Validate the resolved destination against the kind’s registered folder and transport root before any `mkdir`, `open`, or delivery call; add wrong-folder/outside-root refusal tests.

## [HIGH] scripts/transport.py:162 — Concurrent appends can race

**What:** `append()` performs the separator check and writes without a lock or single atomic append operation.
**Why:** Concurrent session writers can interleave or make separator decisions against stale file size, corrupting the structured handback/session content.
**Fix direction:** Serialize per-destination appends or use an atomic append strategy that writes each complete normalized block as one protected operation.

## Medium

(none)

## Low

(none)

`derive` currently reports 17 prefixes with none missing from the registry. The handback switch preserves its existing paths and normal output behavior for current callers.

## Disposition ledger

Self-dispositioning (architect ruling 2026-08-17; a new ledger discharges itself by carrying
its own row rather than landing as one more undispositioned artifact).

| File | Disposition | Evidence locator |
|---|---|---|
| 2026-09-25-codex-transport-registry.md | ACTIONED | 46d37a7c -- both HIGH findings above fixed in code (folder-check in `_check()`, `_DestinationLock` around `append()`'s critical section) with regression tests, before this lane's handback |