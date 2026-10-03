# Codex Review — foundation-3-handoff-boot

**Date:** 2026-10-03
**Branch:** `worktree-foundation-3-handoff-boot`
**HEAD at review time:** `cc1a8a42`
**Diff range:** `origin/main...cc1a8a42` (the STANDING_RULINGS.md body excluded: it is verbatim-quoted text, diffed by `tests/test_standing_rulings_sources.py`)
**Codex version:** n/a — SUBSTITUTED under BATCH-COMMON §0 ruling (e) (see below)
**Mode:** diff-review, isolated read-only session (one file, `changes.diff`, in an empty folder — not the lane)
**Tally:** P1=3 P2=4 P3=0 — all dispositioned below (5 fixed, 1 fixed by adding the missing half, 1 disputed with a measurement)
**Consumer:** `LANE-FOUNDATION-foundation-3-handoff-boot.md` (Done-contract item 9, "the review record citing this contract inside it");
`docs/decisions/ADR-129-handoff-cut-gated-by-handoff-relevant-checks.md` (the handoff cut is gated by handoff-relevant checks, which the new rows join)

**Model used:** `grok-4.6` (SUBSTITUTE for the pinned `gpt-5.6-terra` — see Substitution note)
**Review profile:** code

---

## Substitution note

`SUBSTITUTION: codex terra -> grok-4.6 (Codex is at its usage limit until 2026-10-03 21:07; this review ran at about 18:30 local time)`.
This is the batch order's own route (BATCH-COMMON §0 ruling (e)), not a silent one. Grok is not the
producer's vendor and is not the implementing session.

**Command:** from an empty job-temp folder holding only `changes.diff` and `prompt.md` —
`grok -m grok-4.6 --permission-mode plan --disable-web-search --no-subagents --prompt-file prompt.md`; exit 0.
**Served model:** requested `grok-4.6`; this invocation wrote no `usage.json`, so the served id is **not**
independently confirmed (unlike the foundation-2 record). **Proof of read:** the findings cite
`tests/test_onboarding_items.py:78/85/90/101/190`, `tests/test_handoff_state.py:802`,
`scripts/handoff_state.py:530/562` and `scripts/verify_handoff_probes.py:1771`, each matching the diff.

## Findings and dispositions

| # | Sev | Finding | Disposition |
|---|---|---|---|
| 1 | P1 | Item 5 passed on any four `- ` bullets under the heading | **Fixed.** Item 5 now also requires `registry`, `manual_until`, `daemon`, `usage limit` in the section; a non-vacuity case deletes the `manual_until` bullet and must fail |
| 2 | P1 | Item 2 passed with no plan pointer; no non-vacuity case for it | **Fixed.** Item 2 requires `master plan`; a case strips it and must fail |
| 3 | P1 | Item 7's `evidence:` may be absent from the real row value | **Disputed, measured.** `test_a_fresh_seat_finds_all_13_onboarding_items` cuts a real bundle and parses its DATA block with `parse_boot_blocks`; item 7 is PRESENT there, so the real cell carries `evidence:`. The fixture string is a synthetic stand-in |
| 4 | P2 | Item 4 was one pointer plus one phrase | **Fixed.** Also requires `seat order`, `render`, `queue` |
| 5 | P2 | Item 12 passed on the disclaimer alone | **Fixed.** Also requires the `implement` role in the Models cell |
| 6 | P2 | Items 3, 8, 10 had no non-vacuity case | **Fixed.** One case each |
| 7 | P2 | The era test never showed a post-era bundle FAILs for the omission | **Fixed.** A new test copies the 2026-10-02 boot into a `2026-10-03-…` bundle and asserts the four `BD-*` omissions FAIL |

## Consumer

This record is the review the contract names (`LANE-FOUNDATION-foundation-3-handoff-boot.md`, Done-contract
item 9), written to the name the audit grammar admits (`docs/audits/<date>-codex-<slug>.md`).
`docs/audits/README.md` is left stale for the integrator (`[#590]`).
