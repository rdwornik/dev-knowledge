# Codex Review — b2-rulings-landing

**Date:** 2026-10-04
**Branch:** `worktree-b2-rulings-landing`
**Diff range:** `origin/main...HEAD`; pass 1 at `dc9bfb21`, later passes on the fix deltas named per pass
**Mode:** diff-review, isolated read-only session (the diff and the changed files in an empty job-tmp folder, not the lane)
**Consumer:** `LANE-B2-W1-b2-rulings-landing.md` (Done-contract item 5, "the review record citing this contract inside it", per common rules §2 (e)); `to-cc/AMEND-B2-W1-2-2026-10-04.md` (the ruling this lane lands and gates)

**Model used:** `gpt-5.6-terra` (served — read from each run's own header: `OpenAI Codex v0.155.0`, `model: gpt-5.6-terra`, `provider: openai`, `reasoning effort: low`)
**Review profile:** code
**Command (every pass):** from an empty job-tmp folder holding `diff.patch`, the changed source and test files, `contract.md`, `nonce.txt` and `prompt.md` —
`codex exec -c model=gpt-5.6-terra --sandbox read-only --skip-git-repo-check --output-last-message codex-out.txt -` with the prompt on stdin, run detached.
**Output contract:** the answer had to open with the nonce from `nonce.txt` and quote the first line of `diff.patch`; every pass did.

| pass | nonce returned | first line quoted | scope | reviewer verdict | tally |
|---|---|---|---|---|---|
| 1 | `NONCE-18a43d8e1d69` | `diff --git a/BACKLOG.md b/BACKLOG.md` | the lane's whole diff at `dc9bfb21` | reject | P1=4 P2=1 |
| 2 | `NONCE-a308d7a42ebe` | `diff --git a/scripts/decision_coverage.py b/scripts/decision_coverage.py` | fix commit `c499dddb` | reject | 2 fixed, 4 open (P1) |
| 3 | `NONCE-724858df6f9f` | same | fix commit `8d74b255` | reject | 3 fixed, 4 open (P1) |
| 4 | `NONCE-64909d886697` | same | fix commit `eed7071d` | reject | 5 confirmed fixed, 3 new (P1=2 P2=1) |

The reviewer's own verdict line read `reject` on all four passes and is reported as given. The tip of this record is `393bc9a3`
(the fix for pass 4); **no fifth pass was run**, so pass 4's three new items are fixed or declined below on this lane's own evidence,
not on a reviewer's confirmation.

## Pass 1 — the lane's diff

| finding | disposition |
|---|---|
| **P1** `decision_coverage.py:1112` — a carrying row was accepted with no owner (the contract asks for "an owner (wave or lane)") | **Fixed**, RED-first: `test_a_row_with_no_owner_does_not_carry`. All 19 rows this lane filed already named an owner. |
| **P1** `:1198` — `file_rulings` caught every `OSError` and returned `[]`, so an unreadable RATIFICATION file read as a file with no rulings | **Fixed**: it raises `TransportUnreadable`; `test_an_unreadable_ratification_file_is_not_an_empty_one`. |
| **P1** `:1205/1228` — `date.fromisoformat` on `2026-99-01` crashed the ship gate | **Fixed**: `_parse_day` returns None; `test_a_malformed_header_date_reads_as_undated_and_does_not_crash` and `test_a_malformed_CLOSED_date_makes_the_batch_clock_unreadable_not_a_crash`. |
| **P1** `:1251` — an unlanded ruling with no computable date was skipped ("never refused on a guess"), so it was exempt forever | **Fixed**: refused, naming the missing date; `test_an_undated_unlanded_ruling_is_REFUSED_not_forgotten`. This reverses a design decision of this lane, recorded in the SESSION file. |
| **P2** `tests/test_decision_coverage.py:1154` — the test pinned the fail-open | **Fixed**: replaced by the refusal test above. |

A consequence found while fixing: row `[#1334]` (R57's carrier, filed by FOUNDATION) names no owner and is not this lane's to edit, so the
stricter rule refused R57. Row `[#1379]` was filed in this lane's block to give it one, and R57 names both.

## Pass 2 — fix commit `c499dddb`

Confirmed fixed: the undated ruling (P1) and its test (P2). Open and fixed in `8d74b255`, each RED-first:

- an unmeasured report rendered `OK` and the CLI exited 0 → the headline reads `leg (b) OK; leg (a) NOT MEASURED` and the CLI exits 2 unless `--no-transport` was passed;
- a present-but-invalid `date:` header fell back to the file-name date, which can sit inside the grace period → it reads as undated;
- an unreadable `STATE-BATCH` file was dropped by `_head` → it makes the clock unreadable;
- `owner:` accepted any text → placeholders (`none`, `tbd`, `n/a`, `nobody`, `unknown`, `unassigned`, `-`) name nobody.

## Pass 3 — fix commit `8d74b255`

Confirmed fixed: the undated ruling and the invalid-header fallback for `2026-99-01`. Open and fixed in `eed7071d`, each RED-first:

- `date: 2026-09-01garbage` and `CLOSED 2026-09-01garbage` matched on a valid-looking prefix → the whole first token is read and judged;
- `Path.glob` can hide an enumeration error → `to-browser/` is listed with `os.listdir`, which raises;
- `RulingsReport.refused` is False for an unmeasured report → `passed` added (True only when both legs were measured clean);
- `non-owner:` and `co-owner:` matched `owner:` → tightened (and again in pass 4).

## Pass 4 — fix commit `eed7071d`

Confirmed fixed by the reviewer: whole-token dates, the undated refusal, the invalid-header fallback, the enumeration error. Dispositions of what was left, in `393bc9a3`:

| finding | disposition |
|---|---|
| **P1** `:1094` — `not  owner:` (two spaces) and `non owner:` still read as owner clauses | **Fixed**, RED-first: `owner:` must open a clause (line start, `·`, `(` or `;`); `has no owner:` is prose too. A negation list would never end, so the clause position replaced it. |
| **P2** `:1193` — a `CLOSED 2026-09-05Tgarbage` stamp was accepted | **Fixed**, RED-first: the time part is shaped by a regex and judged by `datetime.fromisoformat`. |
| **P1** `refused` is still False for an unmeasured report, "so a consumer could pass fail-open" | **Declined, with the reason.** No module reads `.refused` except `decision_coverage.main`, which maps an unmeasured leg to exit 2, and the audit adapter reads the report's fields and emits an `n/a` finding with the SUBJECT-ABSENT reason, never a pass. `passed` exists for any future consumer and the property's docstring now says to ask it. Changing `refused` to be True when unmeasured would make `--no-transport` and CI refuse. |

## What the review did not examine

- The register's prose. Pass prompts scoped the review to the gate and its tests; `STANDING_RULINGS.md` section AR was supplied only as context, so its fidelity to the transport is proven by `tests/test_standing_rulings_sources.py` (a verbatim diff against the live transport, skipped as unverified where the transport is unreachable), not by this review.
- Whether an `owner:` value names a live lane or wave. The gate checks that someone is named; naming the right one is a reading.
- Windows-only behaviour beyond what the fixtures exercise (CRLF header handling is covered by `_top`; permission errors are simulated by monkeypatching `Path.read_text` and `os.listdir`).
