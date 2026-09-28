# Codex Review — lane-known-reds-signatures

**Date:** 2026-09-27
**Branch:** `worktree-lane-known-reds-signatures`
**HEAD:** `2457eb69`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low. Verified against the Findings section below: one High, zero elsewhere. Fixed in a follow-up commit -- see the note after Findings. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/known_reds.py:251 — OS overlay can inherit another OS’s signature

**What:** A first `--os` capture copies the shared entry, including its `signature`, and only records the current OS signature when that copied entry lacks one.  
**Why:** Once a normal shared refresh has recorded a signature, a subsequent Windows/Linux overlay compares against that other environment’s fingerprint, causing false regressions and preventing a valid OS-local baseline.  
**Fix direction:** On an overlay’s first capture, derive attribution from the shared entry but establish the signature from that OS’s current output.

## Medium

(none)

## Low

(none)

---

## Disposition

**Fixed**, same lane, next commit: `refresh` now distinguishes a member's first OS-scoped
capture (seeded from the shared entry, whose `signature` may reflect a different OS) from a
member already OS-scoped (whose recorded signature is preserved). The first case drops any
inherited signature and establishes a fresh one from the current run instead. RED-first witness:
`tests/test_known_reds.py::test_refresh_os_key_first_capture_never_inherits_the_shared_entrys_own_signature`.
Confirmed harmless to the windows-latest capture already committed here: at capture time no
shared member carried a `signature` field yet (D2 introduces the field), so the bug could not
have fired against this lane's own committed registry data.