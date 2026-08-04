# Codex Review — 483-preflight-contract

**Date:** 2026-08-04
**Branch:** `feat/preflight-contract`
**HEAD:** `4f11a792`
**Diff range:** `main..feat/preflight-contract`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- preflight_contract.py extraction: are the four regexes right? Can _FILE_LINE_RE / _SHA_RE / _BACKLOG_RE / _HEADING_RE produce FALSE POSITIVES on ordinary prose (a verifier that cries wolf gets ignored), or FALSE NEGATIVES that make the tool vacuous (it PASSES a contract whose locators it never extracted)? Consider markdown code fences, tables, nested backticks, Windows paths, and the dedupe.
- _resolve source-root fallback: can it make a WRONG path pass by resolving a bare name to an unrelated file in another root? Is the order safe?
- exit codes: is 2 genuinely fail-closed for every internal error path, and is 1 vs 2 never conflated? Does verify() ever return a clean report when it could not actually read something?
- _open_backlog_ids reads BACKLOG.md ^- \[#id\] rows - correct source for liveness given retire-not-delete keeps closed task files?
- Tests: any vacuous, tautological or self-constructing assertions? The tests assert on report.render() - is that sound? Is the CLAIM_KINDS structural assertion real coverage or decoration?
- The parity/methodology/roster declarations added for the new command - are they consistent with how the other commands are declared, and did I miss a coupled surface?

---

## Findings
## Critical

(none)

## High

### High — [scripts/preflight_contract.py:162](C:\Users\1028120\Documents\Dev\.dev-knowledge\scripts\preflight_contract.py:162) — “heading” validation accepts ordinary text

**What:** A claimed heading passes whenever its text occurs anywhere in the file, not on a Markdown heading line.  
**Why:** `` `CLAUDE.md` heading "No executable rules" `` passes because that prose exists at `CLAUDE.md:95`, though no such heading exists.  
**Fix direction:** Match normalized Markdown heading syntax (and exclude fenced code) rather than substring-searching the whole file; add a false-positive test.

### High — [scripts/preflight_contract.py:157](C:\Users\1028120\Documents\Dev\.dev-knowledge\scripts\preflight_contract.py:157) — Markdown examples are treated as live claims

**What:** All four extractors scan fenced code blocks and multi-backtick literal examples.  
**Why:** A contract explaining syntax with `` `deadbee` `` or `[#999999]` inside a fenced block produces a real SHA/backlog failure, making normal documentation fail preflight and encouraging users to ignore it.  
**Fix direction:** Tokenize/strip fenced code blocks before extraction and cover fenced blocks, tables, and nested-backtick literals in tests.

### High — [scripts/preflight_contract.py:66](C:\Users\1028120\Documents\Dev\.dev-knowledge\scripts\preflight_contract.py:66) — Windows absolute file locators are silently skipped

**What:** `_FILE_LINE_RE` permits backslashes but not the drive colon (or spaces), so `` `C:\repo\scripts\audit.py:12` `` is not extracted.  
**Why:** A contract containing only that stale locator returns a clean `0/0` report, despite the verifier being run on Windows and accepting `--repo-root` for other checkouts.  
**Fix direction:** Support Windows absolute paths or explicitly report/reject unsupported locator shapes; add a regression test that cannot pass with zero extracted claims.

### High — [scripts/preflight_contract.py:110](C:\Users\1028120\Documents\Dev\.dev-knowledge\scripts\preflight_contract.py:110) — Bare-name fallback can verify the wrong file

**What:** `_resolve()` accepts the first matching basename across broad roots, including `protocols/` and `docs/`.  
**Why:** For example, bare `README.md:1` resolves to `protocols/README.md`, even if the contract meant one of many `docs/**/README.md` files; the wrong locator can therefore pass.  
**Fix direction:** Restrict fallback to unambiguous source roots or fail on multiple matches and require a qualified path.

### High — [scripts/preflight_contract.py:184](C:\Users\1028120\Documents\Dev\.dev-knowledge\scripts\preflight_contract.py:184) — Git operational failures are conflated with stale SHAs

**What:** Any non-zero `git cat-file` result becomes an ordinary “not reachable” claim failure.  
**Why:** A broken/non-worktree Git invocation can return exit `1`, not the documented fail-closed `2`, so “could not check” is indistinguishable from “checked and stale.”  
**Fix direction:** Establish Git/repository health separately and use a SHA probe with distinguishable absent-vs-operational-error outcomes; test the internal-error path.

## Medium

(none)

## Low

(none)

The parity, methodology, generated roster, and task-manifest declarations are consistent; I found no missing coupled declaration.