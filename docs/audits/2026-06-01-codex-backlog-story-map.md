# Codex Review — backlog-story-map

**Date:** 2026-06-01
**Branch:** `docs/backlog-readability-2026-06-01`
**HEAD:** `86a5a8d`
**Diff range:** `main..docs/backlog-readability-2026-06-01`
**Codex version:** codex-cli 0.131.0
**Mode:** diff-review

---

## Focus

scripts/validate_backlog.py (ADR-66 hierarchy parser): correctness, false pos/neg in So-that detection, orphan/theme detection, the _DONE_MARKER_RE vs legit text (does 'Done when:' or normal task prose trip it?), regex robustness, Layer-2 read-only. scripts/check_backlog_commit_msg.py: removed-minus-added id logic, -U0 diff-parsing robustness, edge cases (reword, multi-id, no BACKLOG change). .pre-commit-config.yaml: commit-msg stage wiring (stages, always_run).

---

## Findings
**Critical**

(none)

**High**

## [HIGH] scripts/validate_backlog.py:43 — done-marker regex hard-fails legitimate task prose

**What:** `_DONE_MARKER_RE` treats any `status: done`, `[x]`, or `~~` anywhere in the task line as a completed-task marker.
**Why:** This creates false positives for valid backlog text like documenting `status: done` syntax, mentioning `[x]` literally, or referencing markdown `~~strikethrough~~`, so the validator can block legitimate `BACKLOG.md` edits.
**Fix direction:** Restrict done detection to actual task-state syntax at the start of the bullet or to tightly-scoped structured tokens, instead of substring-matching anywhere in the prose.

## [HIGH] scripts/check_backlog_commit_msg.py:42 — hook silently disables itself on runtime failures

**What:** The commit-msg hook catches `Exception` around the `git diff` call and returns success.
**Why:** If `git` invocation fails or the hook is misconfigured, the enforcement quietly turns off and commits that remove backlog IDs can slip through without any reference check.
**Fix direction:** Catch only the specific read/process errors you expect, and fail closed with a clear stderr message when the diff cannot be obtained.

## [HIGH] scripts/validate_backlog.py:46 — required `## Big picture` section is never actually enforced

**What:** The parser records themes, but validation never checks that `## Big picture` exists or is unique.
**Why:** A malformed backlog can drop or rename the required top-level ADR-66 section and still pass pre-commit, which weakens the story-map gate the hook is supposed to enforce.
**Fix direction:** Add an explicit structural check for exactly one `## Big picture` section before accepting the rest of the hierarchy.

## [HIGH] scripts/validate_backlog.py:46 / scripts/check_backlog_commit_msg.py:26 — load-bearing parser changes landed without targeted tests

**What:** The ADR-66 hierarchy parser and the new commit-msg diff parser were added without any accompanying test coverage in the diff.
**Why:** These are correctness-sensitive gates, and the edge cases called out here (`So that` detection, done-marker false positives, removed-vs-added ID logic, no-BACKLOG-change commits) are easy to regress silently.
**Fix direction:** Add focused unit tests for valid/invalid story hierarchies, literal `Done when:`/`status: done` prose, reword vs close, multi-ID removals, and empty-BACKLOG diffs.

**Medium**

(none)

**Low**

(none)
