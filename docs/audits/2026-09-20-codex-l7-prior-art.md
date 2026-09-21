# Codex Review — l7-prior-art

**Date:** 2026-09-20
**Branch:** `worktree-lane-l7-prior-art`
**HEAD:** `1641006e`
**Diff range:** `main..worktree-lane-l7-prior-art`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/5/1/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/stage_prior_art.py: can a real prior-art hit be MISSED (case, unicode, CRLF, binary skip, file-name-only match, per-source limit truncation, newest-first order)? Is 'NONE FOUND' ever printed when a root was unreadable or the search did not really run?
- Exit semantics: nothing found must exit 0; an unrunnable search (git missing/failing, unreadable file) must exit 1 -- check both, and the empty-subject refusal.
- ecosystem/harness.yaml stage 2: exactly one line changed; does the spine's placeholder substitution ({subject}, unset subject) still behave, and does the resume/receipt hash cover what stage 2 now reads?
- tests/test_stage_prior_art.py + the tests/test_dodo.py regex change: any vacuous assertion, fixture that cannot fail, or test coupled to the live archive that will rot?

---

## Findings
## CRITICAL

(none)

## HIGH

### HIGH — scripts/stage_prior_art.py:82 — Unreadable archive directories can yield `NONE FOUND`

**What:** `Path.rglob()` suppresses directory enumeration errors, so an unreadable root or nested directory is treated as zero files scanned.  
**Why:** The command can exit 0 and print `NONE FOUND` despite not searching all declared archive content.  
**Fix direction:** Walk roots with explicit error reporting and fail with `SearchError` on any inaccessible directory.

### HIGH — scripts/stage_prior_art.py:132 — A present but non-directory root is reported as absent

**What:** Any `docs/audits` or `docs/archive` path that exists but is not a directory falls into the “absent, not searched” path.  
**Why:** A malformed/unsearchable root can produce a successful negative result rather than exit 1.  
**Fix direction:** Distinguish a missing root from an existing non-directory or inaccessible root; refuse the latter.

### HIGH — scripts/stage_prior_art.py:87 — Binary files with matching names are skipped entirely

**What:** The binary-NUL check precedes the filename match at line 99.  
**Why:** A real prior-art hit represented by a binary file whose filename contains the subject is missed, contradicting the advertised filename search.  
**Fix direction:** Check the relative filename before skipping binary content.

### HIGH — scripts/stage_prior_art.py:79 — Unicode case-insensitive matches are incomplete

**What:** Matching uses `lower()` and the ASCII byte fast path rather than Unicode `casefold()`.  
**Why:** Legitimate case variants such as `Straße`/`STRASSE` or Greek sigma variants can be reported as absent.  
**Fix direction:** Use Unicode-aware case folding consistently for decoded content and paths, with an optimization that preserves those semantics.

### HIGH — tests/test_dodo.py:126 — Spine regression test passes when the spine stops before stage 6

**What:** The assertion only checks that a specific stage-6 STOP line is absent; it does not require a successful run or stage-6 receipt.  
**Why:** A new stage-2 failure can stop the spine before stage 6 and leave this test green.  
**Fix direction:** Assert that stage 6 executed successfully (for example, via its receipt/output), or that the run progressed beyond it.

## MEDIUM

### MEDIUM — tests/test_stage_prior_art.py:217 — “Other eleven stages untouched” assertion does not establish that claim

**What:** The test samples fragments of stages 1, 6, and 7 and the stage-number set, while leaving most commands and fields unchecked.  
**Why:** Changes to any of the other stage rows can pass despite the test claiming only stage 2 may differ.  
**Fix direction:** Compare all non-stage-2 rows to the intended baseline or assert their complete structured values.

## LOW

(none)
---

## Disposition (lane-l7-prior-art, after the review)

All six findings were accepted and fixed; none disputed. RED for the four behavioural ones was
committed first (`c054493d`, 4 failed / 18 deselected), the fixes second.

| Finding | Disposition |
|---|---|
| HIGH `stage_prior_art.py:82` unreadable directory yields NONE FOUND | FIXED -- `os.walk(onerror=)` raises `SearchError` (exit 1); test `test_an_unreadable_root_is_refused_never_a_silent_none_found` |
| HIGH `:132` non-directory root reported absent | FIXED -- absent means `not exists()`; an existing non-directory raises; test `test_a_present_root_that_is_not_a_directory_is_refused_not_reported_absent` |
| HIGH `:87` binary file with a matching NAME skipped | FIXED -- the name is matched before the binary skip; test `test_a_binary_file_whose_name_holds_the_subject_is_still_a_candidate` |
| HIGH `:79` `lower()` not Unicode-aware | FIXED -- `casefold()` on term, content, lines and names; the ASCII byte fast path was dropped (it cannot see `Straße` vs `STRASSE`), costing ~0.1 s over 25 MB; test `test_matching_is_unicode_case_folded_not_just_lowercased` |
| HIGH `test_dodo.py:126` regression test vacuous if the spine stops early | FIXED -- it now also requires `SPINE-06-*.json` with `exit_code == 0` |
| MEDIUM `test_stage_prior_art.py:217` "eleven stages untouched" overclaims | FIXED by narrowing the claim -- retitled `test_the_neighbouring_stage_rows_still_resolve_to_their_scripts`; "only one line changed" is proven by `git diff main -- ecosystem/harness.yaml`, quoted in the handback, not by a test that would rot at the next legitimate edit |

One residual the review did not raise: a phrase that spans a line break is reported as a file-level
hit (line 0), not located. A whole-phrase, single-string match is the documented limit (see the
module's ANTI-CLAIMS).
