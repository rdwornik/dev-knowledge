# Close-out review record -- b2w2-boot-teaching ([#1443], [#1438] folded in)

**Date:** 2026-10-10
**Contract:** `LANE-1443-b2w2-boot-teaching` (frozen Done-contract items 1-8; render notes N1-N9), batch B2-W3
**Branch:** `worktree-b2w2-boot-teaching`
**HEAD reviewed:** `01609f37` (the diff `origin/main...HEAD`, 14 files, `origin/main` = `b78c08b6`)
**Tip after the fixes:** `a79ad372`
**Route:** Copilot CLI second route of the reviewer order (common rules B2-W3 section 2 (e), S-38); J7 names this record file.
**Consumers:** [#1443] -- the lane's close-out evidence; `tests/test_onboarding_items.py::test_the_review_record_names_the_contract_and_the_served_model` reads it.

## Codex first: refused

Codex `gpt-6-astra` through `deploy/codex-review.ps1` was tried first (2026-10-10T15:40Z, the wrapper's own run) and refused before reading anything: `ERROR: You've hit your usage limit. ... or try again at 9:40 PM.` The printed reset is the local clock (UTC+2), that is 2026-10-10T19:40Z. Codex was not retried inside that window (S-38). Grok was not used ("grok billing: no"). The command to take the Codex route after the reset is in the lane's session file; a `-codex-` record would not need the S-55 hold.

## Reviewer and proof of reading

- Reviewer: GitHub Copilot CLI 1.0.95, `--model gpt-6.1-sol`, `-s --no-ask-user --allow-all-tools`, one premium request.
- Served model, from the tool's own usage file (`--usage-output-file`): `currentModel` = `gpt-6.1-sol`, the single `modelMetrics` key; `sessionStartTime` 2026-10-10T15:44:04.569Z; session id `63ebebc1-8968-4169-9d75-95bb399ca2b5` (the folder created under `~/.copilot/session-state` at that start time).
- Nonce issued by the lane and echoed first by the reviewer: NONCE-a71427acbe1b
- Content hashes the reviewer computed itself with a shell command and returned; the lane's own values are identical:
  - `lane.diff` (`git diff -U25 origin/main...HEAD` without `BACKLOG.md` and `tasks/manifest.json`, 125,127 B): 5536cb647b525f079e3f249d01d81e95a273a67701257c0da2b360dde807404f
  - `protocols/HANDOFF_BOOT.md` (17,986 B): 12bd6752348195c68aff75d9021c156a8c0f7e95b3e64d18e77792e649c7be92
- The reviewer was given the diff, full copies of `handoff_state.py`, `assemble_paste.py`, `HANDOFF_BOOT.md` and `test_onboarding_items.py`, the contract excerpt (N1-N9, Done 1-8) and a prompt naming five attack lines. `gen_handoff.py` (216 KB) was reviewed through its diff only.
- Output repair: the captured text had console mojibake (`ΓÇö` for a dash); it is repaired below and otherwise verbatim.

## Findings (verbatim, repaired)

Tally: Critical 0 / High 3 / Medium 2 / Low 0.

## Critical

(none)

## High

1. **High — `scripts\handoff_state.py:863,917–926,958` — Markdown answer keys pass both exam slots.** `_KEY_LINE_RE` recognises plain or bold line-start labels, but not headings or list items. A correctly named seat exam containing the required kind/title followed by `## Answer key` and `1. launch` resolves **OK**. A dispatch-exam section containing `### Answer key` also resolves **OK**. Both cases were reproduced through the resolver in memory. This violates Done 1's questions-only requirement; ordinary Markdown formatting is sufficient to expose answers. **Fix direction:** recognise heading/list forms of answer-bearing labels and add negative tests for both exam slots.

2. **High — `scripts\gen_handoff.py:3581–3603` — PROVEN evidence need not belong to the tracked tree.** `evidence_resolves()` checks filesystem containment, file existence and AST function names, but never Git tracking. An untracked Python file with the cited function returns `True` and produces `state: PROVEN`; this was reproduced using the supplied, untracked `test_onboarding_items.py`. In production, removing a cited test from Git while retaining its local file likewise preserves false proof. The new `_evidence_repo()` fixture has no Git repository, so the tests reinforce this incorrect acceptance. **Fix direction:** require the cited repository-relative file to be Git-tracked before AST resolution, and test tracked versus untracked evidence explicitly.

3. **High — `scripts\handoff_state.py:938–944` — An exam-named symlink bypasses the RESULT filename exclusion.** Acceptance examines `p.name`, while `is_file()` and `read_text()` follow symlinks. Thus `SEAT-EXAM-2099-01-01.md` pointing to `SEAT-EXAM-RESULT-2099-01-01.md` can win when the result contains a crafted `kind: SEAT-EXAM` and questions-only heading. An in-memory filesystem witness returned **OK** with a RESULT target. The direct RESULT basename exclusion therefore does not satisfy the "never resolves" requirement under N4. **Fix direction:** validate resolved targets as well as directory-entry names, reject RESULT targets and escapes from the permitted transport directory, and add an alias witness test.

## Medium

1. **Medium — `scripts\gen_handoff.py:3679–3681` — Concurrent map writers share one temporary file.** Every invocation stages into `MAP-DISPATCH.md.tmp`. With two overlapping invocations, A can stage its text, B overwrite that staging file, and A then successfully publish **B's** text; B subsequently fails because the temporary file is gone. That interleaving was reproduced in memory. Atomic replacement alone does not make this shared staging scheme a reliable atomic write. **Fix direction:** create a unique temporary file per invocation in the destination directory, replace from that file, and clean it up on failure.

2. **Medium — `scripts\assemble_paste.py:178–190` — The pasted header can still carry `HANDOFF_BOOT.md`.** `_drop_boot_name_rows()` removes only table rows. A supported header beginning `# HANDOFF_BOOT.md -- session` survives extraction and shedding unchanged, so the renamed section still exposes the ambiguous filename in its body. This was reproduced directly. The new fixture uses `# HANDOFF_BOOT` without `.md`, leaving this contract violation untested. **Fix direction:** ensure the entire emitted session-header section is filename-free, including titles and non-table text, while preserving its session information; add those input forms to the regression tests.

## Low

(none)

## Disposition (the lane's, after the review)

Every High and Medium was reproduced against the reviewed code by its own failing test first (10 failed, 2 passed on the new tests before the fixes -- the 2 are guards), then fixed in `a79ad372` (14 passed after).

- High 1 -- FIXED. `handoff_state._KEY_LINE_RE` now sees a key label after heading hashes, list markers, blockquote and bold marks. `test_a_markdown_key_in_any_line_form_never_passes_either_exam_slot` (six forms, both slots) and the guard `test_the_live_shaped_exam_text_is_not_flagged_as_a_key`. The live SEAT-EXAM files and the Dispatch exam section: 0 matches.
- High 2 -- FIXED. `gen_handoff.evidence_resolves` requires the cited file in the git index (`git ls-files --error-unmatch`, fail closed). `test_evidence_in_a_file_git_does_not_track_is_declared` (untracked, removed from the index, no repository); `_evidence_repo` now `git add`s its file.
- High 3 -- FIXED. `handoff_state._is_alias` skips a symlink and an entry that resolves to a file whose own name is not a dated name of the same item. `test_an_exam_named_alias_of_another_file_never_wins_the_exam_slot` (both legs, simulated so it runs without symlink privilege; the premise assertion shows the crafted entry wins without the check).
- Medium 1 -- FIXED. `gen_handoff.write_dispatch_map` stages in a `mkstemp` file per write and unlinks it if the replace fails. `test_the_map_write_stages_in_a_unique_temp_file_and_cleans_up_when_it_fails`.
- Medium 2 -- FIXED. `assemble_paste._drop_boot_name_rows` also replaces the file name inside any non-table header line. `test_the_pasted_header_carries_no_boot_name_outside_a_table_row_either`. The bundle file stays byte-identical.

No P1 is open. The review did not re-run after the fixes; the fixes are proven by the tests above, not by a second read.

## Limits of this record

- One reviewer, one pass, on a diff whose code files it saw in part (`gen_handoff.py` by diff). It found nothing in the boot text itself (no Critical/High/Medium/Low on `HANDOFF_BOOT.md`); that is a statement about this review, not a proof.
- Copilot route: the record name is `-verification-...-review.md`. Under S-55 a lane whose close-out record is a Copilot-route record merges only after S-54's predicate repair is MERGED; the lane waits `WAITING s54-predicate` for that and keeps its build and this record.
