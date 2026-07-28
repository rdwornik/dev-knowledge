# Codex Review — 437-closure-recheck (terra-pinned passes 2 + 3)

**Date:** 2026-07-28
**Branch:** `fix/437-closure-token-shared-core`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review re-verification, `codex exec` direct with `model=gpt-5.6-terra`
pinned (the lane's code profile defaults to sol; the [#437] arc contract names terra,
so the verification passes were re-run terra-pinned). Pass 1 (sol, wrapper lane):
`2026-07-28-codex-437-closure-diff.md`.

---

## Pass 2 — recheck after the H-A/H-B fixes (@ `583ec527`)

Verbatim final message:

```text
## HIGH scripts/propose_closures.py:63 — tilde-fenced quoted directive still matches

What: ~~~\ncloses [#8]\n~~~ returns ["8"]; the same core exists in the plugin copy
(plugins/tier1-lifecycle/scripts/propose_closures.py:93).
Why: ~~~ is a valid Markdown fenced-code delimiter, so quoted convention prose can
still create a false STRONG proposal and false git_backlog_drift result.
Fix direction: Strip paired tilde fences too, with regression coverage in both
scanner paths.

- H-A is dead: closes "x" [#5] becomes closes \0 [#5] and does not match. H-B is
  dead: ``closes [#6]`` does not match. Real directives adjacent to stripped content
  still match (for example, `q` closes [#1] and closes [#2] "q").
- The hub/plugin detection block from CLOSES_RE through find_weak is exactly
  byte-identical (5,426 characters). validate_git_backlog now reuses that core.
- Pre-existing fail-open paths remain outside this diff: both git_log_commits copies
  return [] on git log failure; the Stop hook also exits 0 after exceptions, with
  error-artifact write failure silently swallowed.
```

**Disposition:** the tilde-fence HIGH was FIXED in-arc (TDD-witnessed; `_STRIP_RES`
gains `~~~.*?~~~`, both copies, parity green, sweep re-derived unchanged). The
out-of-diff fail-open notes are deliberate postures (Stop hook must never wedge
session-end; validate_git_backlog is an awareness layer) — recorded, not changed.

## Pass 3 — final verification (@ tilde fix HEAD)

Verbatim final message:

```text
## HIGH scripts/propose_closures.py:63 — indented Markdown code blocks still produce
closure matches

What: A realistic commit body containing an indented code example, e.g.
"\n\n    closes [#451]\n", returns ["451"]; neither shared scanner strips CommonMark
indented code blocks (plugin twin: plugins/tier1-lifecycle/scripts/propose_closures.py:92).
Why: This is quoted code/context, not a closure directive, yet it can create a false
STRONG proposal or backlog-drift finding.
Fix direction: Extend the shared stripping core to barrier-out contiguous indented
code blocks and add this exact counterexample to the quoting tests.
```

**Disposition: REJECTED-BY-DESIGN (one line + provenance).** Indented lines are the
one context the design note (§2) explicitly excludes — commit bodies indent freely
(`d993922e` indents its own filing text 2 spaces; list continuations routinely indent
4+), so an indent-as-code rule would HIDE real directives, the worse failure direction
for a drift detector — and the terra DESIGN review endorsed exactly this: "Single
quotes and indented commit-body lines are also sound non-strip choices." The observed
10-occurrence false-positive corpus contains zero indent-only cases. Made loud with a
new residual test (`test_residual_indented_line_stays_detected`).

**Net after three passes:** every in-diff finding fixed (H-A barrier, H-B equal-run
backticks, tilde fences) or dispositioned by prior reviewed design (indented blocks);
H-A/H-B confirmed dead by terra with counterexamples; twin byte-identity confirmed
(5,426-char core block).
