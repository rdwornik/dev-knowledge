# Codex Review — 437-closure-diff

**Date:** 2026-07-28
**Branch:** `fix/437-closure-token-shared-core`
**HEAD:** `4ff31ff7`
**Diff range:** `main..fix/437-closure-token-shared-core`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

PRE-MERGE DIFF REVIEW of the [#437] arc (gate code - [#438] posture). The design + its two amendments live in docs/audits/2026-07-28-technical-437-closure-token-design.md; the design review (2H/2M, all dispositioned) in 2026-07-28-codex-437-closure-design.md.
Verify the BUILD against the amended design:
- Correctness of the strip set in propose_closures (_STRIP_RES order, same-line principle, CRLF, curly quotes): any way a REAL plain-text directive gets stripped (fail toward hiding drift) or a quoted token still matches?
- Single-implementation claim: any remaining duplicate closure-token logic anywhere (validate_git_backlog deleted its _strip_code; plugin twin hand-mirrored)? Any consumer of find_strong/find_weak whose behavior changes unexpectedly (WEAK now treats quoted-only commits as plain - is that wired correctly)?
- Twin parity test: does it actually pin the core (pattern+flags for regexes, getsource for functions), and would it catch a one-character divergence in either copy?
- The H1 reversal: plugin.json back at 0.1.10, release act filed as [#444] - is anything else version-coupled that the revert missed?
- Ride-alongs: tasks/ regen (444 add, 440 rename-remnant removal), doc-counts pytest_collected 1903->1948 - each justified?
Verdict: CLEAR or findings with severity.

---

## Findings
```text
Verdict: FINDINGS — not CLEAR

## Critical

(none)

## High

### HIGH scripts/propose_closures.py:73 (plugin twin: plugins/tier1-lifecycle/scripts/propose_closures.py:102) — Stripping can synthesize closure directives

What: Replacing each quoted context with whitespace can join surrounding fragments into a new match; for example, `closes "quoted" [#5]`, a block-quote line, or a fenced span between `closes` and `[#N]` all become detected directives.

Why: Both STRONG scanners can manufacture false closures that were absent from the original text, violating the plain-text-only contract and repeatedly surfacing incorrect drift/proposals.

Fix direction: Mask stripped spans with a non-whitespace barrier or perform span-aware matching so matches cannot cross removed contexts; add regression tests for quote, block-quote, inline-code, and fence bridges.

### HIGH scripts/propose_closures.py:63 (plugin twin: plugins/tier1-lifecycle/scripts/propose_closures.py:92) — Multi-backtick inline code remains matchable

What: The single-backtick regex does not recognize equal-length multi-backtick spans; `docs: explain ``closes [#99]`` convention` currently returns `["99"]`.

Why: A standard quoted inline-code token still becomes STRONG evidence, leaving the original false-positive class partially open.

Fix direction: Recognize same-line equal-length backtick runs while preserving the unpaired/cross-line fail-safe behavior; add single-, double-, and longer-run fixtures.

## Medium

(none)

## Low

(none)

Verification notes:
- No remaining duplicate closure-token implementation was found beyond the required standalone plugin twin; `validate_git_backlog` now consumes `find_strong`.
- Quoted-only commits correctly become WEAK-eligible.
- Twin parity pins regex pattern/flags/order and function source; a one-character divergence within the declared core is caught.
- Plugin version remains consistently `0.1.10`; the release coupling is captured by [#444].
- `gen_task_tree --check` passes; manifest changes correctly add #444 and follow the #440 R100 rename.
- 1,948 tests collect; the 45 new scoped tests pass.
```
