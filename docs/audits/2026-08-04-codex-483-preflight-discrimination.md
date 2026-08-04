# Codex Review — 483-preflight-discrimination

**Date:** 2026-08-04
**Branch:** `fix/483-preflight-discrimination`
**HEAD:** `efd54cf1`
**Diff range:** `main..fix/483-preflight-discrimination`
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
| 0 | 2 | 0 | 0 | 2 |

Counting method: one row per severity heading in the Findings section. **Both HIGHs were
reproduced, then fixed before merge** — see **Disposition**. Both were in the silent-suppression
direction, which is the one this tool must never fail in.

## AC3 evidence — the two re-runs

| run | before | after |
|---|---|---|
| the 2026-08-04 handoff bundle (5 files) | **19** backlog-id flags | **0** |
| the advisory leg on the live BACKLOG | n/a (leg did not exist) | **1** — `[#310] -> #292` |

**The "11" in ruling R1 had already moved to 19** by the time this arc ran, because `[#481]` and
`[#482]` closed earlier the same day (FR-1, FR-2). Removing their 8 occurrences reproduces 11
exactly, confirming R1's figure at its own moment and establishing that it is point-in-time, not
a constant. Per-file arithmetic is tabled in the ruling record.

The single leg finding is a **true positive**, predicted at plan time and left deliberately
unfixed: row `[#310]`'s kill-candidate names `#292`, which is closed. Plan-governs — it is the
advisory leg's first production finding and routes to FR-8a grooming, not a mid-arc swerve.

### The 24 → 2 → 1 progression (why ordering is load-bearing)

Measured on the live `BACKLOG.md` while deriving the rule:

| rule | flags | why |
|---|---|---|
| naive whole-fragment scan | **24** | conflates `kill-candidates: none — <reason citing a closed id>` with a real kill-candidate |
| field value only (split on em-dash) | **2** | reason prose correctly excluded |
| strip backticks FIRST, then match | **1** | catches the row whose own prose quotes `` `kill-candidates: #370` `` |

## Focus

- New role classifier in scripts/preflight_contract.py: surface_role() (Layer 1, path class) and line_role() (Layer 2, per-occurrence in-line context). It decides whether an [#id] is an ASSERTION (claims the row is OPEN) or a CITATION (historical narration). Scoped to the backlog-id claim kind ONLY. Attack the classifier: can a genuinely stale assertion be misclassified as a citation and silently suppressed? That direction is the dangerous one - it fails toward saying nothing, which is the posture this tool claims not to have.
- surface_role defaults to ASSERTION for anything outside the repo and anything in-repo it does not recognise. Verify that default is actually reached and cannot invert. Check the relative_to/resolve logic on Windows paths, symlinks, and a repo_root that is itself a subdirectory.
- line_role masks backtick spans to EQUAL LENGTH so offsets stay aligned, then locates the kill-candidates field on the masked line. Verify the offset arithmetic is correct, including nested or unbalanced backticks, an odd number of backticks on a line, and a line where a quoted field precedes a real field.
- _BACKLOG_ROW was tightened from ^- [#id] to require the [P#][size] tags after an existing test caught the loose form suppressing a real assertion in an ordinary markdown bullet. Verify the tightened form matches every real BACKLOG row shape and cannot be evaded - what about a row with different size tags, or extra whitespace?
- The closed-table state machine in verify() sets in_closed_table on a header row and clears it on any non-table line. Check it cannot leak across sections, cannot be set by a table whose header merely mentions the word closed in a later cell, and behaves on nested or malformed tables.
- New ALL_CHECKS leg check_preflight_backlog_ids in scripts/audit.py: WARN-tier, never FAIL, hub-only, scanning BACKLOG kill-candidates field values for bare #id. It imports the role predicates from preflight_contract rather than restating them. Assess whether the broad except Exception is right for an advisory leg, whether the leg can wedge the ship-gate, and whether reusing private underscore-prefixed helpers across modules is the right coupling or a fragility.
- Assess the tests: are the citation fixtures genuinely non-vacuous, and does the control test (a stale assertion must still FAIL) actually prevent the classifier from degrading into blanket suppression?

---

## Findings
## Critical

(none)

## High

### High — scripts/preflight_contract.py:113

**What:** `_KILL_FIELD.search()` accepts the first `kill-candidates:` anywhere in a row, not a delimiter-anchored field. Prose such as `… kill-candidates: none … · kill-candidates: #479` makes the real stale assertion invisible. The same issue reaches the audit leg through `scripts/audit.py:3643`.  
**Why:** A genuinely stale `#479` is classified as non-assertion and silently suppressed. Double-delimited or unbalanced backticks create the same bypass because `_TICK_SPAN` only handles single paired ticks.  
**Fix direction:** Parse only a properly delimited `· kill-candidates:` field; handle Markdown backtick delimiter runs, and treat ambiguous/malformed field context conservatively as an assertion/WARN. Add stale-value controls after prose, double-backtick, and unbalanced-backtick prefixes.

### High — scripts/preflight_contract.py:351

**What:** Any line beginning `| closed` immediately enables `in_closed_table`, without verifying a Markdown separator row or table semantics; all following pipe-prefixed lines are then citations.  
**Why:** A malformed table, or a regular table whose first heading is `closed` but whose later rows contain forward actions, can suppress a stale assertion until a non-table line appears.  
**Fix direction:** Require a validated header-plus-separator before entering closed-table mode, and narrow suppression to rows unambiguously belonging to a closed-items table. Add malformed-table and mixed-status-table controls.

## Medium

(none)

## Low

(none)
---

## Disposition

Both HIGHs ACCEPTED, reproduced, and fixed pre-merge. Nothing deferred or dispositioned away.
A third defect — **not found by the review** — was caught by the regression test written for
HIGH 2, and is recorded below because it was the most dangerous of the three.

**HIGH 1 — `_KILL_FIELD.search()` took the first field, not every field.** Reproduced: a row
reading `· kill-candidates: none — spent · kill-candidates: [#479] — real` classified the second,
genuinely stale id as a CITATION. Fixed two ways: the field is now **delimiter-anchored** (it
must begin a row field — line start or `·`, so prose merely containing the words cannot open an
assertion span), and **every** field is scanned via a shared `kill_candidate_value_spans()`
helper. The audit leg was switched to the same helper, so tool and leg cannot disagree.

*The double-backtick sub-case terra flagged did **not** reproduce* — `_mask_ticks` already
handled `` ``q`` `` correctly. The tick regex was still made run-aware (`` (`+)…\1 ``) since
markdown permits multi-tick spans. An unbalanced tick matches nothing and therefore masks
nothing, which is the safe direction: unmasked text stays assertion-role.

**HIGH 2 — closed-table mode opened on a lookalike header.** Reproduced: `| closed-loop notes |`
matched, because `\b` ends the token at the hyphen, so every following pipe-prefixed row was
suppressed until a non-table line. A header with no separator row underneath also opened
suppression. Fixed: the first cell must be **exactly** a closed-state word (`\s*\|` after it),
**and** a markdown separator row must follow. Controls added for the lookalike header, the
missing separator, and leakage past the end of the table.

**Found by the fix, not by the review — a blanket backtick rule that suppressed silently.**
Writing HIGH 2's control surfaced that `| `[#479]` | close this row next arc |` was *already*
being waved through, whatever the table logic did. The cause was my own earlier rule: *any*
`[#id]` inside backticks counted as a citation. In this repo backticks around an `[#id]` are
**ordinary formatting** — the closed-table shape is literally `` | `[#479]` | `` — so every
properly formatted stale assertion would have been suppressed. The blanket rule is removed.
Backticks still matter, but only where they quote a **field name**, and that is handled by
masking inside `kill_candidate_value_spans()` — one narrow, testable place instead of a rule
spanning every occurrence. This was the worst of the three defects and the review did not find
it; the regression test did.

**On the leg's broad `except Exception`** (terra asked): retained deliberately. The leg is
advisory by ruling and must never wedge a gate on its own input — an error becomes a WARN
carrying the exception, never a FAIL and never a silent pass. That is the opposite posture from
the tool's `exit 2` fail-closed, and the asymmetry is intended: the tool is invoked to answer a
question, the leg rides every audit run.

**On reusing underscore-prefixed helpers across modules** (terra asked): the leg now imports one
PUBLIC helper, `kill_candidate_value_spans()`, plus `_BACKLOG_ROW`. A test asserts both the reuse
and the absence of any restated grammar in the leg's code, so the coupling is enforced rather
than hoped for.

---

## Close-out: the no-fix rider and the GREEN bar were never in tension

At close the ship-gate went RED — not on a defect in this arc, but because the new leg did its
job: `[~~] preflight_backlog_ids: [#310] -> #292`, a new undispositioned WARN. That set the
ruling's no-fix rider (the finding routes to FR-8a, it is not swept up mid-arc) against AC6's
"ship-gate GREEN at close".

**The conflict resolved structurally, not by choosing a side.** WARN-tier plus the disposition
register is precisely the designed channel for *found, deliberately deferred, tracked*. The two
requirements were only ever in tension if the finding were **ignored**; dispositioning it
satisfies both — the gate is green because the finding is recorded, not because it is hidden.

Disposition `warn-preflight-backlog-ids-310-292` is keyed to the specific row-and-id pair, so it
suppresses **one known finding, never the leg**: any other stale `kill-candidates:` assertion
still REDs the gate. It carries a `review_date` shelf-life (ADR-75) so it cannot rot into paper
suppression, and it is marked **retire-on-close** — the FR-8a grooming row cites this disposition
id, so when `[#310]`'s stale kill-candidate is groomed the entry leaves with it and cannot
outlive its reason.

Final: **ship-gate GREEN, 16 WARN dispositioned.** The leg reports `[~~]`, never `[FAIL]` —
R3's advisory posture holds mechanically, and a test fails if anyone promotes it without R3's
evidence bar.
