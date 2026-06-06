# Codex Review — immutability-guard

**Date:** 2026-06-06
**Branch:** `feat/immutability-guard`
**HEAD:** `20d67ab`
**Diff range:** `main..feat/immutability-guard`
**Codex version:** codex-cli 0.136.0
**Mode:** diff-review

---

## Focus

- block_immutable_edits.py is a SECURITY guard. Scrutinize the fail-open vs fail-closed asymmetry: outside-zone/parse-error must ALLOW (no lockout); once a zone path is identified, any error must DENY.
- Can any in-place edit of an existing transcript bypass the guard? Consider path normalization (case, backslashes, ./, trailing slash, symlinks), the file_path vs notebook_path fields, and the mutating-tool set (Edit/MultiEdit/Write/NotebookEdit) — is any mutating tool missed?
- Could the guard FALSELY block legitimate work outside docs/decisions/transcripts/ (e.g. an ADR edit, a path merely containing the substring)?
- Wire protocol: decision=block + exit 2 matches the block-onedrive precedent?
- billing_leak_sentinel.ps1: any way it leaks the key value, or fails non-soft (blocks session-start)?

---

## Findings
## CRITICAL

## CRITICAL scripts/hooks/block_immutable_edits.py:67 — symlink/junction path bypass

**What:** Zone detection is lexical only, so an outside-zone symlink/junction path to an existing transcript is treated as outside the immutable zone.  
**Why:** Editing through that alternate path can mutate an existing transcript while the guard allows it.  
**Fix direction:** Resolve the target path canonically before zone comparison, and compare against the canonical transcript-zone root.

## CRITICAL .claude/settings.json:5 — shell writes bypass the guard

**What:** The hook only matches `Edit|MultiEdit|Write|NotebookEdit`, so a `Bash`/shell command can still modify transcript files directly.  
**Why:** This leaves an obvious in-place mutation path around a security guard.  
**Fix direction:** Add shell-command coverage or a separate shell guard that blocks mutating commands targeting `docs/decisions/transcripts/**`.

## CRITICAL scripts/hooks/block_immutable_edits.py:86 — `file_path` can mask `notebook_path`

**What:** The guard chooses `file_path` before `notebook_path`, so a payload containing both could allow a benign `file_path` while the actual notebook target is in the immutable zone.  
**Why:** Once any recognized target path is in-zone, the hook must deny or fail closed.  
**Fix direction:** Evaluate tool-specific path fields, and treat any in-zone recognized path as controlling.

## HIGH

## HIGH scripts/hooks/block_immutable_edits.py:70 — lexical substring can falsely block outside-zone paths

**What:** A normalized path like `docs/decisions/transcripts/../ADR-77-...md` resolves outside the transcript zone but still matches the substring.  
**Why:** This can block legitimate ADR or non-transcript work, violating the intended fail-open outside-zone behavior.  
**Fix direction:** Normalize and resolve paths before comparing them to the transcript-zone root.

## MEDIUM

(none)

## LOW

(none)

I did not run tests; this was a read-only review. Wire protocol and billing sentinel looked fine: `decision=block` plus exit `2` is present, and the sentinel only prints key presence and exits `0`.
