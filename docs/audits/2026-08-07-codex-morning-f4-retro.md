# Codex Review — morning-f4-retro

**Date:** 2026-08-07
**Branch:** `docs/morning-consolidation`
**HEAD:** `2f2edd2b`
**Diff range:** `319f885d..2f2edd2b`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review (RETROACTIVE)
**Tally:** 0/2/0/0
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- RETROACTIVE review of the already-merged morning consolidation arc (F4 stash hardening).
- scripts/audit.py: new _git_stash_entries reader + _stash_findings leg + wiring into check_stale_worktrees. Check the None-vs-empty-list distinction (None = not-a-repo, [] = looked and found nothing), the WARN-only posture, subprocess timeout/encoding handling, and whether the leg can ever mask or be masked by the worktree leg.
- tests/test_stale_worktrees.py: are the new tests actually constraining, or would a reader that always returned [] still pass them?
- scripts/validate_branch_naming.py: the automation/ prefix addition.
- Ignore prose/markdown paths in this range entirely.

---

## Findings
## Critical

(none)

## High

## HIGH tests/test_stale_worktrees.py:341 — The integration test never creates a stash

**What:** It overwrites the already tracked `f.txt`? Wait correction: `_init_repo` tracks `f.txt`, and the test overwrites it, so it does create a tracked modification.  
**Why:** No issue here; the real-Git test does constrain an always-`[]` reader.  
**Fix direction:** No change needed.

## HIGH scripts/audit.py:1160 — A stash-reader failure is silently reported as a clean worktree result

**What:** `_git_stash_entries()` uses `None` for any command failure, and `_stash_findings()` drops that result even when `_git_linked_worktrees()` already succeeded.  
**Why:** A timeout or `git stash list` failure can yield only the worktree `pass`, masking that the stash leg did not run; `None` therefore no longer exclusively means “not a repository.”  
**Fix direction:** Preserve a distinct unavailable/indeterminate WARN finding when the stash read fails after the worktree reader succeeded.

## HIGH scripts/audit.py:1137 — UTF-8 decoding errors can break the WARN-only audit check

**What:** The new subprocess forces UTF-8 decoding without `errors="replace"` and does not catch `UnicodeDecodeError`.  
**Why:** A repository configured to emit a non-UTF-8 stash subject can raise out of the check, turning this advisory WARN leg into an audit failure/crash.  
**Fix direction:** Make decoding tolerant while retaining the timeout/error distinction.

## Medium

(none)

## Low

(none)
---

## Disposition — 2026-08-07 (PRE-2 arc)

**Tally 0/2/0/0 — and BOTH were ACCEPTED AND FIXED in this arc.** The reviewed code is the F4
stash hardening this same seat wrote and merged hours earlier at `2f2edd2b`. The `[#480]` leg
flagged it for the same reason it flagged lanes A and B, and it was right to: two real defects
came back, one of them a hole in reasoning I had written into the docstring myself.

### H1 · "The integration test never creates a stash" — NOT A FINDING (self-retracted in-line)

terra opened this one and reversed itself inside its own What paragraph
(*"Wait correction: `_init_repo` tracks `f.txt`, and the test overwrites it, so it does create
a tracked modification"*), closing with *"No issue here… Fix direction: No change needed."*
**Excluded from the tally on substance, not on convenience**: it names no defect and prescribes
no change. Left in the artifact verbatim rather than edited out — an artifact that quietly drops
what a reviewer said is worth less than one that shows the reversal.

### H2 · A stash-reader failure was silently reported as a clean result — ACCEPTED, FIXED

**The sharpest finding of the three reviews, because it caught the code contradicting its own
docstring.** `_git_stash_entries` returns `None` for BOTH "not a git repo" and "git works but
the read failed" (timeout, non-zero exit). `_stash_findings` dropped every `None` silently,
justified in the docstring as *"the caller has already emitted the n/a that covers a repo git
cannot read"* — a justification that only holds when the **worktree reader also failed**. When
`_git_linked_worktrees` had just succeeded, git was demonstrably working, so the `None` was a
genuine read failure and the organ reported a clean worktree verdict while the stash leg had
not run at all. I had written *"a detector that cannot see does not report clean"* into that
very docstring and then not implemented it in this branch.

**Fixed:** `_stash_findings(repo_path, git_known_good=...)`. The caller passes `True` (it only
reaches the leg after a successful worktree read), and a `None` under that condition now emits
an explicit indeterminate WARN naming what it does not know. The `git_known_good=False` path
keeps the old silence, which is correct there — the n/a is already emitted.

**Test change, recorded because it inverts an assertion:**
`test_stash_leg_stays_silent_when_the_stash_cannot_be_read` asserted the OLD behaviour and is
replaced by `test_an_unreadable_stash_warns_when_git_itself_is_working` plus
`test_an_unreadable_stash_stays_silent_when_git_is_absent`, which pin the two halves of the
distinction separately. Six pre-existing tests that stubbed only the worktree reader now stub
both, since a half-stubbed fixture no longer models a real repo.

### H3 · `UnicodeDecodeError` could crash a WARN-tier leg — ACCEPTED, FIXED

`subprocess.run(..., encoding="utf-8")` without `errors="replace"`, and `UnicodeDecodeError` is
a `ValueError` — **not** caught by the `except (OSError, subprocess.SubprocessError)` handler.
A stash subject is an arbitrary commit message, so a repo emitting non-UTF-8 bytes would raise
straight out of an advisory leg and take the whole audit check down. **Fixed** by adding
`errors="replace"`, pinned by `test_the_stash_reader_survives_undecodable_bytes` (asserted at
the source: manufacturing a non-UTF-8 stash portably is awkward, and the decode posture is the
actual property).

**Sibling note, not fixed:** `_git_linked_worktrees` has the same `encoding="utf-8"` without
`errors=`. It is pre-existing rather than introduced here, and out of this arc's scope —
recorded so it is a known thing rather than a lucky survival.

### Verified clean

`scripts/validate_branch_naming.py`'s `automation/` addition drew nothing, and terra confirmed
the real-git integration test genuinely constrains an always-`[]` reader — which was the
specific worry the focus hints asked it to check.

**Suite after the fixes:** `tests/test_stale_worktrees.py` 23 passed.
