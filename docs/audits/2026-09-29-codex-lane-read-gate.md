# Codex Review — lane-read-gate

**Date:** 2026-09-29
**Branch:** `worktree-lane-read-gate`
**HEAD:** `9294c3d2`
**Diff range:** `origin/main..worktree-lane-read-gate`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 2/3/0/0 <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: this review is for LANE-5B5-11-lane-read-gate.md (H:\My Drive\CLAUDE PROMPT DIR\LANE-5B5-11-lane-read-gate.md), batch WAVE5B-N5.
Diff: scripts/read_gate.py, tests/test_read_gate.py, tests/fixtures/read_gate/synth.py, pyproject.toml (pdfplumber dep), uv.lock, logs/READ-OUTCOMES.jsonl (one real appended line).
Change: a verifier (verify_read) that accepts a route's read only if its output file exists and is non-empty, its log carries no "print timeout" line, and every quotation in its output (straight or curly double-quoted spans, whitespace-normalized) is a literal substring of the locally-extracted source text (PDF via pdfplumber, EPUB via stdlib zipfile+html.parser, plain text as-is). A route runner (run_read_gate) walks roles.read from ecosystem/provider-registry.yaml at run time, verifies each attempt via an injectable invoker, falls through on a failed check, appends one JSONL line per attempt to logs/READ-OUTCOMES.jsonl, and returns the first verified result or a failure naming every route and its failed check. Real invokers for antigravity/copilot-enterprise shell out (mirroring scripts/provider_bench.py's argv shapes); the anthropic/claude-sonnet-5 route is a "live terminal fallback" invoker with no subprocess.
Please check specifically: (1) whether the quotation-literal-substring check (extract_quotations + normalize_whitespace) can be bypassed by a paraphrase engineered to dodge the straight/curly-quote regex or the whitespace normalization, (2) whether the fall-through in run_read_gate could silently accept a bad read under any invoker behavior (e.g. an invoker that raises after partially writing the output file), (3) whether the real _cli_invoker's subprocess handling (timeout, missing binary, non-JSON output) could hang or crash the caller instead of falling through, (4) general code quality and docstring accuracy.
NOTE: local main ref is stale (b30f96ba); this review's DiffRange is explicitly origin/main..worktree-lane-read-gate to scope to only this lane's own commit.

---

## Findings
## CRITICAL

## [CRITICAL] scripts/read_gate.py:135 — Unquoted paraphrases are accepted

**What:** `extract_quotations()` can return no spans, after which `verify_read()` accepts any non-empty output.  
**Why:** A reader can evade literal verification by emitting a paraphrase without double quotes (or using unsupported delimiters such as single quotes); the included test explicitly locks in this bypass.  
**Fix direction:** Require at least one valid literal quotation and reject unsupported quote-like delimiters, or use a structured output format with required quote fields.

## [CRITICAL] scripts/read_gate.py:325 — “Live terminal fallback” fabricates a verified read

**What:** `anthropic_fallback_invoker()` locally extracts the source and writes its first 400 normalized characters as a quote; it never invokes or waits for the live Claude session.  
**Why:** The route is marked accepted without any reader performing the requested locating/answering work, and its docstring inaccurately describes that local copy as a live terminal read.  
**Fix direction:** Make this route obtain output from the actual live-session handoff, or represent it as unavailable rather than automatically manufacturing an accepted result.

## HIGH

## [HIGH] scripts/read_gate.py:279 — CLI child inherits stdin and can block the fallback chain

**What:** `_cli_invoker()` omits `stdin=subprocess.DEVNULL`, unlike the mirrored `provider_bench.run_one()` implementation.  
**Why:** A CLI that waits for EOF or an interactive prompt can stall the caller for the full 600-second timeout before the next route is tried.  
**Fix direction:** Close child stdin explicitly and add mocked subprocess coverage for timeout, missing executable, and non-JSON output.

## [HIGH] scripts/read_gate.py:225 — Verification failures can abort instead of falling through

**What:** Only `invoke()` is inside the route-level exception boundary; `verify_read()` can raise on a deleted/replaced path, directory, unreadable file, or invalid UTF-8 output.  
**Why:** A malformed or partially written route output can terminate `run_read_gate()` before later routes are attempted, contrary to its stated fall-through behavior.  
**Fix direction:** Treat verification I/O and decode errors as rejected route outcomes, append their ledger entries, and continue.

## [HIGH] scripts/read_gate.py:225 — Runner trusts an invoker-supplied output path without freshness or containment checks

**What:** An injectable invoker may return any existing path, including a stale output, the source file, or a file outside `workdir`.  
**Why:** A faulty invoker can produce an accepted result from pre-existing content rather than from its current route attempt.  
**Fix direction:** Have the runner own per-attempt output paths, remove them before invocation, and require the returned path to be the newly created expected path under `workdir`.

## MEDIUM

(none)

## LOW

(none)

Missing binaries and `subprocess.TimeoutExpired` are caught and fall through; non-JSON CLI output is not parsed, so it does not independently crash this path.

---

## Amendment (in-file, ADR-94-style status-only exception does not apply here -- this is
## content, appended not edited) -- all 5 findings fixed, same-session

- **CRITICAL scripts/read_gate.py:135** -- FIXED. `verify_read` now rejects
  `no-quotation-in-output` when `extract_quotations()` returns an empty list (a 4th check,
  strengthening rather than weakening the AMEND's three -- ADR-108 SS B). Test:
  `test_verify_read_rejects_output_with_no_quotations_at_all`.
- **CRITICAL scripts/read_gate.py:325** -- FIXED. `anthropic_fallback_invoker` (the
  auto-fabricating function) is removed entirely. `real_invoker` now raises `ReadGateError`
  for the `anthropic` route rather than manufacturing an accepted result; a caller driving a
  live session supplies its own invoker for that one entry. Test:
  `test_real_invoker_refuses_the_anthropic_route_rather_than_fabricating_a_read`.
- **HIGH scripts/read_gate.py:279** -- FIXED. `_cli_invoker` now passes
  `stdin=subprocess.DEVNULL`. Test:
  `test_cli_invoker_passes_devnull_stdin_so_it_cannot_hang_on_a_waiting_cli`. (Also given an
  injectable `runner` parameter, mirroring `aj_scan.delegate_describe`, so this and the
  timeout/missing-binary/non-JSON paths are now unit-testable without a real CLI.)
- **HIGH scripts/read_gate.py:225 (verification abort)** -- FIXED. `run_read_gate` now wraps
  `verify_read` in its own `try/except (OSError, UnicodeDecodeError)`, rejecting that one
  route (`verify-error:...`) instead of aborting the run. Test:
  `test_run_read_gate_rejects_rather_than_raises_on_an_unreadable_output`.
- **HIGH scripts/read_gate.py:225 (path containment)** -- FIXED. `run_read_gate` now computes
  each attempt's canonical output path itself (`workdir / f"{route.provider}.output.txt"`),
  clears it before invoking, and verifies THAT path rather than whatever path an
  `InvokeAttempt` claims. Tests:
  `test_run_read_gate_ignores_a_stale_or_foreign_path_an_invoker_claims`,
  `test_run_read_gate_clears_a_route_leftover_before_invoking_it`.

32/32 tests pass on the fixed tip (`uv run --locked pytest tests/test_read_gate.py -q`); the
live DONE-ITEM 7 demonstration was re-run after these fixes -- see
`to-browser/SESSION-lane-read-gate.md`.