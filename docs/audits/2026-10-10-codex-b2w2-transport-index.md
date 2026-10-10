# Codex Review — b2w2-transport-index

**Date:** 2026-10-10
**Branch:** `worktree-b2w2-transport-index`
**HEAD:** `ff2bf578` (round 2; round 1 reviewed `b47c4f0d`)
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/3/0/0 <!-- Critical/High/Medium/Low of round 2, counted by hand: the wrapper's heuristic reads the bands `## Critical` / `### file:line` as zero. Round 1 was 2/3/0/0; both are kept below. -->

**Model used:** `gpt-6-astra` (pinned; both lanes — [#469])
**Review profile:** code
**Consumer:** [#1439] LANE-1439-b2w2-transport-index

---

## Rounds, served model, proof of reading, verdict (contract `LANE-1439-b2w2-transport-index`, J5 / Done 7)

- **Contract:** `LANE-1439-b2w2-transport-index` (row [#1439], batch B2-W3, plan revision 7); this record is its close-out diff review (Done 7).
- **Served model, from the tool's own log header (`model:` line):** `gpt-6-astra`, provider openai, codex-cli 0.155.0, sandbox read-only, reasoning effort high. `CODEX_API_KEY` unset (subscription login).
- **Round 1:** head `b47c4f0d`, codex session `01a1266c-8715-71b1-9c8c-e715f8cb5446`, nonce `4b19de7a84bbb3f8` returned as the first line with `HEAD b47c4f0d`. Findings **2 Critical, 3 High** -> **FAIL** (J5 calibration: PASS unless a CRITICAL or HIGH remains). Kept whole in the last section. Revision 1: tests `bfc141e6`, fixes `34283ea2`.
- **Round 2 (the one re-review):** a first attempt at 2026-10-10T16:10:09Z was refused for a usage limit (`WAITING codex`, printed reset `9:40 PM`, local clock UTC+02:00 = 19:40Z, not retried inside that window); run at 2026-10-10T19:42:51Z after the reset, head `ff2bf578`, codex session `01a12757-286e-75b1-89a1-fdfb5dea9d1c`, nonce `a3b61057f18cdbf1` returned as the first line with `HEAD ff2bf578`. Findings **1 Critical, 3 High** -> **FAIL**. Revision 2: tests `e348210a`, fixes `c22f899f`.
- **Verdict:** **FAIL on round 2, carried (S-33).** This lane ran no third review. The round 2 fixes below are **unreviewed**: they are verified by tests (321 passed in `tests/test_transport.py` + `tests/test_transport_lint.py`, 476 passed in 12 writer-side consumer test files) and by `ruff check`, not by the reviewer. Whether a further review is spent is the dispatcher's call under S-38.

### Dispositions of round 2

| Finding | Disposition |
|---|---|
| Critical `scripts/transport.py:1072` POSIX overwrite remains possible | **FIXED, unreviewed.** A move calls `_rename_no_replace`: Windows `os.rename` (raises for an existing name); Linux `renameat2(RENAME_NOREPLACE)`; macOS `renamex_np(RENAME_EXCL)`; a platform with none refuses the apply before any directory is made. **Honest limit:** the Linux and macOS branches could not be exercised on the Windows host this lane ran on; the same janitor tests would run through them on a Linux CI runner (ADR-127), which is the first place they are exercised. Tests `test_a_move_never_replaces_an_existing_destination`, `test_a_platform_with_no_atomic_no_replace_rename_refuses_the_apply_and_moves_nothing`, `test_a_destination_that_appears_at_the_rename_is_a_refusal_and_both_files_stay` |
| High `scripts/transport.py:1065` whole-file writers bypass the move lock | **FIXED, unreviewed.** `write()` replaces under the destination's lock (the one `append()` and the move take); the janitor's own INDEX write no longer wraps `write()` in a second lock. A writer that bypasses `transport.py` is not coordinated with (stated in `_move_one`). Test `test_a_whole_file_write_takes_the_destinations_lock_the_move_and_the_append_share` |
| High `scripts/transport.py:588` a failed head read becomes a persistent cached row | **FIXED, unreviewed.** `_read_window_checked` keeps the failure; the row is a placeholder; the INDEX header says `unreadable: N` when N > 0 and a refresh of such an INDEX trusts no cached row (so it equals a full rebuild). Test `test_a_failed_head_read_is_never_a_row_a_later_refresh_reuses` |
| High `scripts/transport_lint.py:141` a BOM before `by:` unsigns the file | **FIXED, unreviewed.** `by_value` ignores a leading UTF-8 BOM. Test `test_a_byte_order_mark_before_the_by_line_does_not_unsign_the_file` |

Round 2's own recheck line: C2, H2 and the H3 advisory correction are closed; H1 handles missed edits with newer mtimes (its failed-read case is the third High above).

---

## Focus (round 2)


Contract: LANE-1439-b2w2-transport-index (row [#1439], batch B2-W3, plan revision 7). Begin your answer with the single line 'NONCE a3b61057f18cdbf1' and, on the next line, 'HEAD ' followed by the output of git rev-parse --short HEAD in this repository.
This is the RECHECK of a first review of b47c4f0d that found 2 Critical and 3 High; the fixes are the commit 34283ea2 (tests first in bfc141e6). Verify each fix actually closes its finding, then hunt for what the fixes introduced or left:
(C1) scripts/transport.py _move_one: each janitor move runs under the source's append lock, re-checks the source bytes and the destination's absence, and reads FileExistsError/OSError from os.rename as a refusal; the POSIX overwrite window is stated, not closed. (C2) _manifest_out_problem and the exclusive-create write in _cmd_janitor: --manifest-out refuses an existing path and any path under the transport root. (H1) refresh_index/_older_than/_stamp_epoch/build_index: a cached INDEX row is reused only for a file whose mtime is older than the INDEX's regenerated: stamp less 5 s; the mtime is a cache validity test and never a date. (H2) scripts/transport_lint.py file_class: inventory lookup by normcase. (H3) the write gate stays keyed on the WRITER while the sweep is keyed on the KIND; the advisory for a script writer on a role-written kind now says the sweep refuses it (handback.py and gen_lane_contract.py are not this lane's files and cannot be made to stamp by:).
Also review the whole diff origin/main...HEAD once more for: data-loss paths in the janitor, a by: rule that refuses a legitimate write or fails open when it should fail closed, an incremental INDEX refresh that diverges from a full rebuild, attribution errors, Windows faults (cp1252, case-insensitive paths, os.rename onto an existing name, locks, lock sentinels left behind), and tests that cannot fail. Do not report style.

---

## Findings
NONCE a3b61057f18cdbf1
HEAD ff2bf578

## Critical

### scripts/transport.py:1072 — C1: POSIX overwrite remains possible

**What:** A destination created between `lexists()` and `os.rename()` is overwritten on POSIX.
**Why:** The competing archive file is lost before verification; documenting the window does not close the data-loss finding.
**Fix direction:** Use an atomic no-replace operation, or refuse apply on platforms without that guarantee.

## High

### scripts/transport.py:1065 — C1: Whole-file writers bypass the move lock

**What:** `_move_one()` takes the append lock, but `write()` replaces the source without acquiring it.
**Why:** A write between the hash check and rename causes unreviewed replacement bytes to be archived; the subsequent refusal leaves the newly written file missing from its live location.
**Fix direction:** Make whole-file writes and janitor moves share source synchronization.

### scripts/transport.py:588 — Failed head reads become persistent cached rows

**What:** `_read_window()` converts an `OSError` into an empty head, which becomes a normal cacheable INDEX row.
**Why:** After a transient read failure clears, an old file’s unchanged mtime passes `_older_than()`, so refreshes retain incorrect `UNATTRIBUTED`/`UNKNOWN` metadata while a full rebuild recovers it.
**Fix direction:** Preserve read-failure status and prohibit caching failed scans, or abort the refresh without advancing its stamp.

### scripts/transport_lint.py:141 — UTF-8 BOM causes legitimate signatures to be refused

**What:** A BOM-prefixed first-line `by:` fails the anchored regex because lint readers use `utf-8` without removing the BOM.
**Why:** A valid signed file produced by Windows tooling is rejected by check/sweep and role-writer appends, although the INDEX reader accepts the same head using `utf-8-sig`.
**Fix direction:** Normalize a leading BOM consistently before evaluating head keys.

## Medium

(none)

## Low

(none)

Recheck: C1 remains open. C2, H2, and the specified H3 advisory correction are closed. H1 handles missed edits with newer mtimes, but the failed-read cache case remains.

Static review only; tests were not run. The read-only session denied `uv` cache access.

---

# Round 1 (superseded by round 2) — head `b47c4f0d`, nonce `4b19de7a84bbb3f8`, codex session `01a1266c-8715-71b1-9c8c-e715f8cb5446`

**Tally of round 1:** 2/3/0/0 (the wrapper's heuristic printed `0/0/0/0`; counted by hand from the bands `## Critical` / `## High`).
**Dispositions of round 1** (fixed in `34283ea2`, tests first in `bfc141e6`): Critical 1 janitor move: a lock shared with `append()`, the bytes and the destination re-checked, `FileExistsError`/`OSError` read as a refusal (round 2 found its POSIX window and the `write()` bypass, above); Critical 2 `--manifest-out`: refuses an existing path and any path under the transport root, created exclusively; High 1 refresh reuse: a cached row is trusted only for a file older than the INDEX's `regenerated:` stamp less 5 s; High 2 inventory case: `os.path.normcase` lookup; High 3 gate vs sweep: kept writer-keyed, the advisory now says a lint sweep refuses the file (row owed: `handback.py` and `gen_lane_contract.py` are not this lane's files).

## Findings (round 1, verbatim)
NONCE 4b19de7a84bbb3f8
HEAD b47c4f0d

## Critical

### scripts/transport.py:1044 — Janitor checks do not protect the move

**What:** Source hashing and destination-existence checks occur separately from the unlocked `os.rename`.
**Why:** A concurrent source replacement can move unreviewed bytes; on POSIX, a destination created after `lexists` can be overwritten, with verification detecting damage only afterward.
**Fix direction:** Use an atomic no-overwrite move and coordinate source verification and movement with transport writers.

### scripts/transport.py:1450 — Dry-run manifest output can destroy existing files

**What:** `--manifest-out` uses truncating `write_text` without checking whether the target already exists or is a transport artifact.
**Why:** Pointing it at a live or archived file overwrites that file during a dry run, without `--apply` or a reviewed hash.
**Fix direction:** Refuse existing output targets and prevent manifest output from replacing transport artifacts.

## High

### scripts/transport.py:859 — Successful refreshes preserve previously missed edits

**What:** Refresh reuses every existing row except the destination’s without checking whether its source changed.
**Why:** If file A’s edit survives a failed refresh, subsequently writing B preserves A’s stale subject, attribution and supersedes information, diverging from a full rebuild.
**Fix direction:** Validate cached rows against their source windows or rebuild before reusing potentially stale rows.

### scripts/transport_lint.py:154 — Inventory lookup mishandles Windows filename casing

**What:** Inventory membership uses case-sensitive string keys.
**Why:** An inventoried `DIGEST-alpha.md` accessed as `DIGEST-ALPHA.md` is the same Windows file but becomes “new,” incorrectly refusing a legitimate unsigned write.
**Fix direction:** Normalize inventory keys and lookup paths consistently with the filesystem’s case semantics.

### scripts/transport.py:211 — Generated-kind exemption also admits mixed-writer kinds

**What:** The gate decides the unsigned exemption from the caller’s writer name instead of whether the kind is script-only.
**Why:** An unsigned new `SESSION-*.md` written by `handback` passes, although SESSION also permits `lane`; the subsequent lint sweep refuses the same file.
**Fix direction:** Apply the same kind-based classification in both the write gate and lint, reserving the exemption for script-only kinds.

## Medium

(none)

## Low

(none)

Validation was limited to source and test inspection: the runtime probe was blocked because `uv` required writable cache access.
