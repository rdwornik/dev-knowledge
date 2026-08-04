# Codex Review — 481-organ-id-rename

**Date:** 2026-08-04
**Branch:** `fix/481-organ-id-names-measured-organ`
**HEAD:** `e564733e`
**Diff range:** `main..fix/481-organ-id-names-measured-organ`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Severity tally

Written into the artifact body per NC4 (the `[#480]` durability property applied immediately):
the 2026-08-02→04 window's failure was a `0/0/0/0` tally read from transient terminal output
with no committed trace while the artifact bodies carried ≥1 CRITICAL + 21 HIGH. A tally that
lives only in a terminal is not auditable after the fact.

| Critical | High | Medium | Low | Total |
|---|---|---|---|---|
| 0 | 0 | 1 | 2 | 3 |

Counting method: one row per `## [SEVERITY]` heading in the Findings section below.
All three were resolved before merge — see **Disposition** at the end of this artifact.

---

## Focus

- The organ id session_end_backpressure was renamed to lock_unanchored_push in scripts/enforcement_coverage.py. The token is OVERLOADED: scripts/session_end_backpressure.py is still a live script, still deployed by deploy/carrier_mesh.py, still wired as an advisory Stop hook. Verify that no occurrence which legitimately names that SCRIPT was renamed, and that no organ-id-role occurrence was missed.
- tests/test_enforcement_coverage.py gained two invariants. Assess whether test_anchor_organ_id_names_the_organ_it_measures is circular or vacuous: it resolves the probe from TIER1_ORGANS by GROUP rather than by id literal, precisely to avoid selecting on the string under test. Does it actually fail if the id and the measured script diverge again?
- Assess test_organ_id_census_carries_no_retired_id: does its live-registry introspection plus four syntactic organ-id-position regexes genuinely cover the organ-id role, or does it have a hole that would let a retired-id reference survive? Its stated honest limit is that prose mentions are out of scope.
- _ORGAN_TO_COMPONENT was REKEYED only, with behavior deliberately held identical, and a recorded honest limit that the mapped component's carrier deploys the advisory Stop script and never deploys block_unanchored_push. Is holding behavior identical here correct, and is the comment accurate?
- Check the renamed probe helpers (_seb_* -> _anchor_*, _seb_candidate_command -> _stop_backpressure_command) for any missed call site or stale docstring/comment claim about what the probe now measures.

---

## Findings
## Critical

(none)

## High

(none)

## Medium

## [MEDIUM] tests/test_enforcement_coverage.py:840 — Retired-id census is not a complete organ-id-role scan

**What:** The regexes only match narrow double-quoted literal forms; they miss valid role positions such as `ec.Cell(_RETIRED_ORGAN_ID, ...)`, single quotes, `cells.get(...)`, and `Tier3Cell` rows whose component is not `session-end-backpressure`.  
**Why:** A retired organ id can survive in a test-side identity position while this invariant still passes, despite its claim to census that role.  
**Fix direction:** Use a structural AST-based check or broaden coverage to all relevant constructor/access forms, including constants and both quote styles.

## Low

## [LOW] tests/test_enforcement_coverage.py:207 — Historical helper claim is stale

**What:** The docstring says `_anchor_fire` probed the Stop hook before the repoint; that helper was renamed from `_seb_fire` in this diff.  
**Why:** It misstates the probe history and obscures which helper actually changed behavior.  
**Fix direction:** Refer to `_seb_fire` for the pre-repoint implementation.

## [LOW] tests/test_enforcement_coverage.py:615 — Tier-3 test descriptions still call the measured organ “seb”

**What:** The tests now construct `block_unanchored_push` cells, but their docstrings/comments describe a “seb divergence” or inert Stop-hook candidate.  
**Why:** The Stop hook is now advisory evidence only; the measured absent organ is the pre-push anchor gate.  
**Fix direction:** Distinguish the `session-end-backpressure` component attribution from the `block_unanchored_push` organ being measured.

---

## Disposition

All three findings ACCEPTED and fixed pre-merge. No finding was deferred or dispositioned away.

**MEDIUM — census not a complete organ-id-role scan.** Correct, and the honest limit as
originally written understated the gap. The four positional regexes were replaced with an
**AST scan**: every string-literal node equal to the retired id, in any construct or quoting
style, bar the single sanctioned `_RETIRED_ORGAN_ID` definition — identified by its
*assignment*, never by line number (a line pin drifts and silently stops protecting anything).
Comments fall out by construction (not AST nodes); docstrings are dropped explicitly, matching
the stated prose limit. The remaining limit is narrowed and restated in the docstring: prose,
and dynamically composed ids (concatenation / f-string / external data).

*Teeth verified by mutation, not by inspection:* injecting `_ALIAS_CHECK =
['session_end_backpressure']` — a single-quoted literal in a list, a form **none** of the four
retired regexes covered — makes the census FAIL with the offending line number. Source restored
byte-identically after the probe.

**LOW — stale historical helper claim (`:207`).** Correct, and it is the same defect class this
arc exists to close, committed by this arc's own rename. The sentence describes the
*pre-repoint* implementation, which was named `_seb_fire` at that time; renaming it there
falsified a historical claim. Reverted to `_seb_fire`, with the pre-`[#481]` name marked as
historical in place.

**LOW — Tier-3 docstrings still say “seb”.** Correct. Rewritten to state the distinction
explicitly: the measured ORGAN is `block_unanchored_push`, the COMPONENT it is attributed to is
`session-end-backpressure`, and that attribution is known-misfiled per the `_ORGAN_TO_COMPONENT`
honest limit. The stale `"Stop hook did NOT block"` evidence strings — describing the organ the
probe no longer reads — were corrected to `"no pre-push anchor hook"` in the same pass.

**Note on the Focus block above:** the hint text reached Codex with several backticked
identifiers mangled (`block_unanchored_push` → `lock_unanchored_push`) because a PowerShell
**double-quoted** here-string treats the backtick as an escape character. The review itself ran
against the real diff and is unaffected; only the echoed hint text is corrupted. Recorded as a
gotcha so the next invocation uses a single-quoted here-string.

The `session_end_backpressure.py` script references were preserved where they name the live Stop-hook script. The anchor-id invariant is non-circular and will fail for the intended regression—changing `_ANCHOR_ORGAN_SCRIPT` without changing the Group-C id. The `_ORGAN_TO_COMPONENT` rekey deliberately preserves existing behavior; its honest-limit comment is accurate: the mapped carrier deploys the advisory Stop script, not `block_unanchored_push`.