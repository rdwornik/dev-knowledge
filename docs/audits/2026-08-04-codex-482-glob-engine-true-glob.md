# Codex Review — 482-glob-engine-true-glob

**Date:** 2026-08-04
**Branch:** `fix/482-boundary-glob-engine-true-glob`
**HEAD:** `3e969a63`
**Diff range:** `main..fix/482-boundary-glob-engine-true-glob`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Severity tally

Written into the artifact body per NC4 — a tally that lives only in terminal output is not
auditable after the fact.

| Critical | High | Medium | Low | Total |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 1 |

Counting method: one row per severity heading in the Findings section below. The HIGH was
**resolved before merge** — see **Disposition**.

## AC2 measured reference values (evidence, not assertions)

Derived live at execution time over the tracked corpus; recorded here per the operator
amendment, deliberately **not** pinned as a test assertion.

- **Live corpus: 1854 tracked files** (the row's reference value was 1830)
- **Governed union: 14 under BOTH engines** — the AC2 invariant holds

| glob | fnmatch (before) | true-glob (after) |
|---|---|---|
| `CLAUDE.md` | 1 | 1 |
| `.claude/*.md` | 13 | 1 |
| `.claude/**/*.md` | 12 | 13 |
| **UNION** | **14** | **14** |

**The 13 → 14 delta is accounted for, not waved through.** The row's reference figures
(`1/12/11`, union 13, corpus 1830) were measured 2026-08-03. Every live per-glob figure is
exactly **+1**, and the cause is witnessed: **`.claude/commands/preflight.md`**, added at
**`4f11a792`** on **2026-08-04 — this window**, after that measurement. The AC2 fork-stop fired
as designed; the invariant it protects (union equality across engines) holds live, so the
resolution was to proceed and record the delta here as evidence.

Per-glob attribution moved by design; **no file entered or left the governed set**. This is
intent, not coverage.

## Focus

- The glob engine in scripts/boundary_headers.py was switched from fnmatchcase to a hand-composed true-glob segment matcher `_glob_matches`. Verify the matcher is CORRECT: `*` must never cross `/`, `**` must mean zero or more whole segments, and the recursion must terminate. Look hard for pathological patterns (leading/trailing `**`, consecutive `**/**`, empty segments from a leading or doubled `/`, a pattern with more segments than the path) and for exponential backtracking on many `**` segments.
- Was hand-composing justified? glob.translate() and PurePath.full_match() are Python 3.13+; this repo floor is >=3.12 and 3.12 PurePath.match() is right-anchored with non-recursive `**`. glob.glob(recursive=True) was rejected as the ENGINE because it reads the working tree not the git index, and retained as the ORACLE. pathspec was rejected because gitwildmatch is not pure glob. Challenge any of these if wrong.
- test_governed_union_is_identical_before_and_after_the_engine_switch recomputes the OLD fnmatch engine live rather than quoting a constant. Is that a genuine before/after invariant, or does re-running the old engine in-process make it circular or vacuous?
- test_glob_matches_agrees_with_stdlib_glob_per_glob asserts PER GLOB against glob.glob. Assess whether the include_hidden=True choice and the intersection with tracked files hide a real disagreement, and whether a union-only check would have been weaker (the claim is yes, because the union is equal under the old engine too).
- AC3 pin: test_governed_globs_tuple_is_pinned plus test_each_governed_glob_still_means_what_it_is_pinned_to_mean. Assess whether the pin genuinely fires on add/remove/reword and on an engine regression, and whether it can be defeated. The synthetic probes are deliberately not drawn from the live corpus so ordinary repo growth does not fire the pin. Is there a change that SHOULD fire it but does not?
- Confirm no file entered or left the governed set: per-glob attribution moved 13/12 to 1/13 but the union is 14 on both engines over 1854 tracked files.

---

## Findings
## Critical

(none)

## High

**Severity:** High  
**File:** [scripts/boundary_headers.py](/C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/boundary_headers.py:266)  
**What:** Consecutive `**` segments cause exponential recomputation of identical `(path-index, pattern-index)` states on a non-match.  
**Why:** Recursion terminates because `j` always advances, but a future legitimate glob such as repeated `**/**/.../missing` can make coverage/check impractically slow across tracked files.  
**Fix direction:** Memoize `walk(i, j)` (or use iterative DP), and add a non-match test with many consecutive `**` segments.

## Medium

(none)

## Low

(none)

Notes: the current three governed globs have correct segment semantics; `*` cannot cross `/`, `**` handles zero-or-more segments, and the current governed union remains 14 files. The old-engine union test is a genuine independent relational invariant, not circular. The per-glob stdlib oracle is stronger than a union-only assertion; `include_hidden=True` and intersecting with tracked paths are appropriate for this index-backed engine. The tuple/meaning pin catches unaccompanied glob edits and engine regressions, though—as with any test pin—it can be consciously re-baselined alongside its probes. The stated Python-version rationale is accurate: 3.12 `PurePath.match()` is right-anchored and non-recursive for `**`; `full_match()` is later. [Python 3.12 docs](https://docs.python.org/3.12/library/pathlib.html#pathlib.PurePath.match)
---

## Disposition

The single HIGH was ACCEPTED and fixed pre-merge. No finding deferred or dispositioned away.

**HIGH — exponential recomputation on consecutive `**`.** Correct, and the concern was **cost,
not termination**: `walk` always advances `j`, so it terminates, but without memoization
repeated `**` re-explores identical `(path-index, pattern-index)` states on a non-match.

*Reproduced before fixing, rather than accepted on the reviewer's word:*

| consecutive `**` (non-match) | before | after |
|---|---|---|
| 6 | 0.026 s | — |
| 8 | 0.201 s | — |
| 10 | 1.249 s | — |
| 12 | **6.204 s** | **0.00069 s** |
| 20 | (not run) | 0.00084 s |
| 40 | (not run) | 0.00205 s |

Roughly 6× per added segment before; flat after. Fixed by memoizing **failed** states, which
bounds the search at `O(len(parts) × len(pats))`. The current three globs cannot trigger this,
but the predicate runs over every tracked file, so a future glob carrying repeated `**` would
have made the gate impractical rather than merely slow.

Terra's suggested regression test was added — `test_repeated_double_star_does_not_blow_up_on_a_non_match`
— asserting both the wall-clock ceiling **and** the answers, since a fast wrong answer is not a
fix. It also pins the zero-segment cases (`**/x.md` matching `x.md`, `a/**/**/x.md` matching
`a/x.md`) so the memo cannot change semantics while making them cheap.

**Confirmations recorded** (terra's Notes, kept because they discharge specific contract
clauses): the old-engine union test is a genuine independent relational invariant, not circular;
the per-glob stdlib oracle is stronger than a union-only assertion; `include_hidden=True` plus
the tracked-set intersection are appropriate for an index-backed engine; the tuple/meaning pin
catches unaccompanied glob edits and engine regressions; and the Python-version rationale is
accurate — 3.12's `PurePath.match()` is right-anchored with non-recursive `**`, `full_match()`
is later.

**Honest limit, terra's wording retained:** as with any test pin, the AC3 pin *can* be
consciously re-baselined alongside its probes. That is the design — it forces a conscious
re-pin, it does not make one impossible.
