# Codex Review — l5-no-leftovers

**Date:** 2026-09-20
**Branch:** `worktree-lane-l5-no-leftovers`
**HEAD:** `cfcfc8a6`
**Diff range:** `main..worktree-lane-l5-no-leftovers`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/no_leftovers.py: is it truly read-only (git wrapper allowlist, no mutating call, claude agents listing)? Any way a leftover reads as PASS (unreadable evidence, prefix-sibling matching, case/slash normalisation, admin-entry matching)?
- The eleven checks vs the spec: worktree list, dir absent, find -mindepth 1 enumeration, .git/worktrees, branch -a, refs naming lane, ls-remote heads, job record, claude agents, clean tree, main == origin/main.
- tests/test_no_leftovers.py: does each check have a real failing and passing fixture; any vacuous assertion; any test touching the live hub.
- Exit codes: non-zero on every leftover; slugged run does not fail on OTHER lanes' husks (deliberate, NOTE only) - is that a hole?

---

## Findings
## CRITICAL

(none)

## HIGH

### scripts/no_leftovers.py:305 — Admin-entry collision heuristic flags legitimate sibling lanes

**What:** Any `.git/worktrees/<lane><digits>` entry is treated as this lane’s leftover without checking its `gitdir` target.  
**Why:** A valid concurrently registered lane whose slug is the target slug plus digits causes a clean teardown to fail; the tests cover only a `-2` sibling, not this allowed form.  
**Fix direction:** Treat a suffixed admin directory as relevant only when its resolved `gitdir` points to this lane, and add a passing sibling fixture with a digit-appended slug.

### scripts/no_leftovers.py:302 — Unreadable administrative evidence can be accepted as clean

**What:** Failure to read an admin entry’s `gitdir` is silently ignored.  
**Why:** An arbitrarily named or collision-suffixed administrative entry that points at the lane can be missed when its target cannot be read, producing PASS despite unknown evidence.  
**Fix direction:** Make unreadable relevant/ambiguous admin entries fail closed and add an unreadable-entry fixture.

### scripts/no_leftovers.py:351 — Corrupt or unreadable job records are skipped while check 8 can pass

**What:** Per-job JSON read/parse failures are recorded only as a note and do not fail `job-record-absent`.  
**Why:** A surviving job record that cannot be inspected may still point at the lane, contradicting the verifier’s fail-closed claim; the test explicitly codifies this PASS behavior.  
**Fix direction:** Fail check 8 when any job record cannot be read or parsed, or establish independently verifiable metadata before allowing it to be ignored.

## MEDIUM

(none)

## LOW

(none)

## Dispositions (lane-l5-no-leftovers, same session)

- **HIGH 1 (digit-suffixed admin entry flagged by name) -- ACCEPTED, fixed.** A `.git/worktrees/<slug>N` entry now
  counts as the lane's only when its `gitdir` target resolves to the lane path; the name alone decides only for an
  exact `<slug>` entry. `test_4_passes_for_a_digit_suffixed_admin_entry_that_belongs_to_a_live_sibling`
  (RED witnessed on the old code: failed, evidence named the sibling as a leftover).
- **HIGH 2 (unreadable admin `gitdir` accepted as clean) -- ACCEPTED, fixed.** An admin entry with an unreadable or
  empty `gitdir` now FAILS check 4 and is named in the evidence. `test_4_fails_closed_on_an_admin_entry_whose_gitdir_cannot_be_read`
  (RED witnessed: passed on the old code) and `test_4_fails_closed_on_an_ambiguous_suffixed_entry_with_no_readable_target`
  (already green on the old code by name match; kept as the guard that the fix did not reopen that case).
- **HIGH 3 (unparseable job record skipped) -- ACCEPTED, fixed.** A job record that cannot be read or parsed now FAILS
  check 8. `test_8_fails_closed_on_a_job_record_it_cannot_parse` replaces the earlier test that codified the PASS
  (RED witnessed: passed on the old code). Stated cost: a `state.json` caught mid-write reads as FAIL until a re-run.
- The review's fourth focus (slugged run does not fail on OTHER lanes' husks) raised no finding; it stays a deliberate
  NOTE-only design, stated in the module's HONEST LIMITS.
