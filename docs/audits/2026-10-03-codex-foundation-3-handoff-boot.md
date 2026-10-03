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

---

## Amendment 2026-10-03 (repair 1 of 2) — the review re-run with the output contract met

*Dated in-file amendment marker (audit immutability, CLAUDE.md §5 rule 3): the text above is unchanged. The
integrator's refusal (`REFUSED-foundation-3-handoff-boot.md`) found that the first review named no served
model and no nonce (BATCH-COMMON §0a item 1, R59), so that read counted as failed. This section is the
re-run and supersedes the "Served model" and "Proof of read" lines above; the single record name per lane
is kept because the audit grammar admits one `docs/audits/<date>-codex-<slug>.md`.*

`SUBSTITUTION: codex terra -> grok-4.7 (Codex is at its usage limit until 2026-10-03 21:07; this re-run ran at 18:10Z, 20:10 local)`.
Route per `to-cc/AMEND-BATCH-FOUNDATION-3-2026-10-03.md` (grok-4.7 before 21:07). Not the producer's vendor and not the implementing session.

- **Reviewed tip:** `938ff0a5` (origin/main `ce6ecb08` already merged; `git fetch` + `git merge origin/main` at repair start: already up to date).
- **Command:** from an empty job-tmp folder holding `changes.diff` (`git diff origin/main...HEAD`, excluding `protocols/STANDING_RULINGS.md`, `JOURNAL.md`, `BACKLOG.md`, `tasks/`, `ecosystem/doc-counts.md`, `docs/audits/README.md`), the 12 changed source/test files under `files/`, `CONTRACT.md` (this lane's frozen contract) and `nonce.txt` —
  `grok -m grok-4.7 --tools read_file,list_dir,grep -p "<prompt.md>"`.
- **Exit code:** 0; stderr empty; 19 model calls.
- **Served model:** `grok-4.7`, read from the session's `usage.json` `primaryModelId` (`modelUsage` holds only `grok-4.7`).
- **Nonce:** `NONCE-1d8ae831cbf4` — written to `nonce.txt`, returned verbatim as the answer's first line; the reviewer also returned the first line of `changes.diff` verbatim (`diff --git a/docs/audits/2026-10-03-codex-foundation-3-handoff-boot.md …`). The read is proven under R59.

| # | Sev | Finding | Disposition |
|---|---|---|---|
| 1 | P1 (claimed) | Item 6 unmet: `protocols/STANDING_RULINGS.md` R35–R54 not in the diff or tip snapshot | **Disputed, measured — an input omission, not a defect.** The review folder excluded that file on purpose (its 44,736 B diff is verbatim-quoted text, diffed by `tests/test_standing_rulings_sources.py`, as the first review note says). At the tip `protocols/STANDING_RULINGS.md:5150` is `## AQ. RATIFICATION 2026-09-29 → 2026-10-02 R35–R54, and the newest-models ruling …`; `tests/test_standing_rulings_sources.py` + `tests/test_onboarding_items.py`: 25 passed at `938ff0a5`. |

No other finding was returned. **Tally:** P1=0 real (1 disputed with a measurement) P2=0 P3=0.
