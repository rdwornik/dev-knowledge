# Codex Review — lane-connection-hygiene

**Date:** 2026-09-22
**Branch:** `worktree-lane-connection-hygiene`
**HEAD:** `718ceb09`
**Diff range:** `main..worktree-lane-connection-hygiene`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0
**Consumer:** W4-4, DECLARE-WAVE4A goal G2/G6 (`to-cc/DECLARE-WAVE4A-2026-09-22.md`).

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

## Diff-range caveat (recorded before commit, not a Codex finding)

The wrapper's default diff range is `main..<branch>` against the **local** `main` ref, not
`origin/main`. At review time, local `main` (`8746b741`) was a clean fast-forward ahead of
`origin/main` (`df0c1ac8`, this lane's actual fork point and merge-base) by sibling lane
W4-1's `worktree-lane-known-reds` merge (`af701a47` feat: test_pairing batch registry,
`d3efa367` fix: preflight all-digit-sha) — merged into the shared local `main` ref by that
lane's own session, not yet pushed to origin. `git diff HEAD origin/main -- <the 3 flagged
files>` is empty: this lane is byte-identical to the actually-pushed truth on all three.

All three High findings below (`preflight_contract.py` sha.isdigit, `test_pairing.py`
record-base/compare, `tasks/manifest.json` #937-#941) are therefore this lane's fork point
predating W4-1's local-only merge, surfaced by tip-to-tip diff as if this lane "removed"
work it never had — not a regression this lane's own commits introduced. Per the frozen
contract this lane does not touch `test_pairing.py`, does not rebase mid-arc, and does not
read another lane's state; reconciling the two local-`main` states is the integrator's job
at the merge moment, not this lane's.

---

## Findings
## Critical

(none)

## High

### scripts/preflight_contract.py:371 — All-digit commit SHAs are silently ignored

**What:** The new `sha.isdigit()` early return skips valid all-digit short commit IDs.  
**Why:** A stale or valid locator can be reported clean without verification.  
**Fix direction:** Validate all SHA-shaped tokens and retain disambiguating failure text for numeric-looking ones.

### scripts/test_pairing.py:390 — Batch pairing commands were removed

**What:** `record-base`/`compare`, their registry, and skip/unregistered fail-closed guards are absent.  
**Why:** Batch integrations lose the one-base comparison and can no longer refuse unattributable results.  
**Fix direction:** Rebase onto `main` so the batch registry implementation and its tests are retained.

### tasks/manifest.json:680 — Generated task manifest drops #937–#941

**What:** The source-of-truth manifest ends after task #936, omitting the five Wave 4 task rows present on `main`.  
**Why:** Regenerating `BACKLOG.md` from this branch would silently remove active task records.  
**Fix direction:** Rebase and regenerate the manifest from the current task sources.

## Medium

(none)

## Low

(none)