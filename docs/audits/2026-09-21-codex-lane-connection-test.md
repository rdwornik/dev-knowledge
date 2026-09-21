# Codex Review — lane-connection-test

**Date:** 2026-09-21
**Branch:** `worktree-lane-connection-test`
**HEAD:** `f8012b9d`
**Diff range:** `main..worktree-lane-connection-test`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/4/0/0
**Consumer:** W3-F, DECLARE-WAVE3-CONNECT goal G1 (`to-cc/DECLARE-WAVE3-CONNECT-2026-09-21.md`); no-consumer: a lane review record, not a governance surface.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- This is a TESTS-ONLY lane (tests/test_connection_loop.py + tests/fixtures/connection_loop/). Check the test can actually fail: vacuous assertions, a stop that can be swallowed, the strict-xfail and EXPECTED_STOPS pin, the shared-walk lock across xdist workers.
- Boundaries: nothing may write to the operator's live transport or real ~/.claude (HOME is redirected; the registry read is shimmed by fixtures/connection_loop/sitecustomize.py). Look for any path that escapes the tmp world.
- Only the provider spawn and the git remote may be faked; no moment, organ or harness.yaml row may be mocked. Flag any place the test substitutes an organ.
- The integrator chain is reproduced from .claude/commands/lane-integrate.md (race and actions deliberately not run). Flag anything in that reproduction that would make a later moment pass or fail for a reason other than the loop.

---

## Findings
## CRITICAL

(none)

## HIGH

### tests/test_connection_loop.py:408 — HANDBACK refusal is ignored before merging

**What:** The test records `audit.py handback`’s exit code but unconditionally performs `git merge`.  
**Why:** A broken HANDBACK guard can refuse while the test still reaches merge, teardown, and batch-close, producing misleading later-stop results.  
**Fix direction:** Require a successful verdict before merging, or record it as a terminal stop and do not simulate later integration steps.

### tests/test_connection_loop.py:499 — Replaces a declared organ with a synthetic one

**What:** A successful declared `digest` receipt is overwritten in the walk model as `digest-names-the-task`.  
**Why:** This substitutes a non-harness organ and makes the strict-xfail/`EXPECTED_STOPS` queue red for a synthetic failure rather than the declared moment’s actual result.  
**Fix direction:** Preserve the declared digest receipt and track the digest-content requirement separately.

### tests/test_connection_loop.py:511 — xdist readers can consume a partially-written shared walk

**What:** One worker checks for the result file while another writes it directly with `write_text`.  
**Why:** A waiting worker can see the file before JSON publication completes and fail decoding it, making the shared-walk lock flaky under xdist.  
**Fix direction:** Write to a temporary file in the shared directory and atomically replace the result file.

### tests/test_connection_loop.py:577 — Live-transport safety check permits unobservable writes

**What:** The test passes when live transport observation is `None`, and its fingerprint compares only matching filenames.  
**Why:** A failed redirect or overwrite of an existing toy-named live file can escape detection, despite the test’s isolation boundary.  
**Fix direction:** Probe the child-process registry shim directly and require a verified temporary transport destination; compare stronger metadata if retaining the live check.

## MEDIUM

(none)

## LOW

(none)

---

## Dispositions (W3-F, 2026-09-21)

All four HIGH findings were real and are fixed in `tests/test_connection_loop.py`; the fixes were not re-reviewed by Codex.

- **HANDBACK refusal ignored (line 408) -- FIXED.** `integrate_merge` returns `(None, info)` on a non-zero `audit.py handback`
  and merges nothing; the walk records a `Stop("integrate", "handback-verdict", ...)` and simulates no later step.
  The missing-GO negative test now asserts the verdict passed, so the refusal under test is the missing GO.
- **Declared digest receipt overwritten (line 499) -- FIXED.** The declared `digest` receipt is left exactly as the
  organ wrote it; "the digest names the task" is a separate `Stop` (`batch-close`/`digest-names-the-task`) appended to the
  queue. `EXPECTED_STOPS` is unchanged.
- **Partially-written shared walk (line 511) -- FIXED.** The result is written to a per-process temp file in the run's
  folder and published with `os.replace`.
- **Live-transport check permits unobservable writes (line 577) -- FIXED, with a stated limit.** The walk now asks a
  CHILD process where the User-scope transport is (`registry_redirect`, must be `verified` on Windows); the live
  fingerprint carries (size, mtime_ns) for toy-named files. Limit: an unresolvable live transport (CI, no drive) is
  still `None` and passes -- there is then nothing of the operator's to touch.
