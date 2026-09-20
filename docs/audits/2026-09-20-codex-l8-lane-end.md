# Codex Review — l8-lane-end

**Date:** 2026-09-20
**Branch:** `worktree-lane-l8-lane-end`
**HEAD:** `c101f0f4`
**Diff range:** `main..worktree-lane-l8-lane-end`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/5/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/transport_report.py: idempotence (one artifact replaced at every turn end), read-back verification is real, unmounted/unset drive NEVER falls back to a downloads folder and never claims delivery, exit codes never 2 (Stop hook blocking code), nothing can raise out of main.
- Runtime budget: stdlib only, one shared git deadline, inside a 15 s hook budget shared with another hook.
- Path safety: lane name -> file name, tmp file cleanup, never writes the agent-bound folder.
- scripts/lane_digest.py: plain-language digest names every lane and every open item; no identifiers leak; verdict logic.
- tests: any vacuous assertions in tests/test_transport_report.py and tests/test_lane_digest.py.

---

## Findings
## Critical

(none)

## High

### scripts/transport_report.py:116

**What:** `to-browser` is accepted without checking its resolved target remains under the transport root or outside `Downloads`/`to-cc`.  
**Why:** A junction or symlink can redirect the artifact into the agent-bound folder or a Downloads folder while reporting successful delivery.  
**Fix direction:** Resolve and validate the final destination before writing; add symlink/junction coverage.

### scripts/transport_report.py:170

**What:** `read_bytes()[:MAX_RECEIPT_BYTES + 1]` reads each entire receipt before applying the size limit.  
**Why:** A large receipt can consume memory or exceed the shared 15-second Stop-hook budget, despite the advertised bound.  
**Fix direction:** Read at most the limit-plus-one bytes from an opened file, and test with an oversized receipt.

### scripts/lane_digest.py:136

**What:** Valid JSON receipts without an `organ` field are silently dropped.  
**Why:** With other successful receipts present, the digest can declare the lane “finished clean” while omitting a malformed receipt and its open item.  
**Fix direction:** Treat every unrecognizable receipt shape as unreadable/open, using a safe human-readable label.

### tests/test_transport_report.py:148

**What:** The runtime assertion accepts the initial/default value of `0`.  
**Why:** Removing runtime measurement entirely would still pass, leaving the required hook-budget evidence unprotected.  
**Fix direction:** Control the clock or compare against elapsed execution so the test proves `runtime_ms` is measured.

### tests/test_transport_report.py:171

**What:** Checking only `GIT_TIMEOUT_S <= 3` does not test that all Git calls share one deadline.  
**Why:** A regression that gives each Git subprocess a new three-second deadline still passes while exceeding the hook budget.  
**Fix direction:** Stub Git/time and assert subsequent calls receive the same diminishing deadline.

## Medium

(none)

## Low

(none)
---

## Disposition (lane-l8-lane-end, after review)

All five HIGH findings were valid and are fixed in the commit that follows the review, each with a test:

1. `transport_report.py:116` (junction or symlink named `to-browser`) -- FIXED. `resolve_transport` now judges where the folder RESOLVES: the resolved name must be `to-browser`, inside the transport root, and not inside a downloads folder. Tests: `test_a_to_browser_link_into_the_agent_bound_folder_is_refused`, `test_a_to_browser_link_into_downloads_is_refused` (a real junction on Windows, a symlink elsewhere).
2. `transport_report.py:170` (unbounded receipt read) -- FIXED. The file is opened and at most `MAX_RECEIPT_BYTES + 1` bytes are read. Test: `test_an_oversized_receipt_is_bounded_and_marked`.
3. `lane_digest.py:136` (valid JSON without `organ` dropped) -- FIXED. Any unrecognised shape becomes an `unreadable` receipt: an open item and a `needs attention` verdict. Test: `test_a_receipt_of_an_unrecognised_shape_is_an_open_item_never_dropped`.
4. `test_transport_report.py:148` (runtime assertion accepts the default 0) -- FIXED. `test_the_runtime_is_measured_not_defaulted` drives a fake clock and requires `runtime_ms == 250`.
5. `test_transport_report.py:171` (constant-only budget test) -- FIXED. `test_the_two_git_calls_of_one_summary_get_the_same_deadline` records the deadline each call receives. Residual, stated plainly: `commit_subjects` (used by the digest) takes its own deadline per call, so a batch digest over N lanes can spend up to N x 3 s; the per-turn organ `transport_report` is bounded to one shared 3 s.

The fixes were committed together with their tests; their red state was not witnessed in a separate commit.
