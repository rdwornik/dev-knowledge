# Codex Review — b2-merge-gate

**Date:** 2026-10-04
**Branch:** `worktree-b2-merge-gate`
**HEAD at review time:** `3a83b5d3` (read 1); repaired through `54d890a5`
**Diff range:** `2dd2067d..HEAD` limited to the 14 files this lane changed (+1428/−132 at read 1); lane 4's carried commits are not re-reviewed here (its own record: `docs/audits/2026-10-04-codex-foundation-4-merge-gate.md`, carried as it stands, ruling (i))
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review, isolated read-only session (`--sandbox read-only`, a folder holding only `DIFF.patch`, the changed files at tip, `CONTRACT.md`, `nonce.txt`, `PROMPT.md`)
**Tally:** read 1 P1=3 P2=0 P3=0 · read 2 P1=2 · read 3 P1=1 P2=1 · read 4 P1=1 — every P1 fixed (below)
**Consumer:** `LANE-B2-W1-b2-merge-gate.md` item 6 ("the review record"); `docs/decisions/ADR-127-ci-os-verification.md`; `[#966]`

**Model used:** `gpt-5.6-terra` — the served id, read from each run's own header (`model: gpt-5.6-terra`, provider openai, `reasoning effort: low`). No substitution was needed.
**Review profile:** code

---

## How it was run

`codex exec -c model=gpt-5.6-terra --sandbox read-only --skip-git-repo-check -C <isolated folder> --output-last-message <file> -`, the prompt piped on stdin (a bare `codex exec` can hang reading it). Four reads: the lane diff, then each repair's own diff.

The first attempt of read 1 failed at once with `You've hit your usage limit … try again at 5:21 PM` (17:18 local). Diagnosed as a time-bound limit, not retried in a loop: one retry after the stated reset, which ran. No Grok substitution.

| Read | Diff reviewed | Nonce returned (line 1, verbatim) | Line 2 quoted | sha256 of the raw answer (first 16 hex) | Tally |
|---|---|---|---|---|---|
| 1 | the 14-file lane diff at `3a83b5d3` | `NONCE-825297143-755943962` | first diff line | `9648e20beb98bd8f` | P1=3 |
| 2 | repair 1, `3a83b5d3..8174ee4d` | `NONCE-257089379-952556172` | first diff line | `b546c6283ad7ef01` | P1=2 |
| 3 | repair 2, `8174ee4d..de8bb6e6` | `NONCE-1274734666-428367027` | first diff line | `a96f01b22bcfe4d6` | P1=1 P2=1 |
| 4 | repair 3, `de8bb6e6..37a9061e` | `NONCE-119544395-536524572` | first diff line | `3450d46de454885b` | P1=1 |

## Findings and dispositions

**Read 1 · P1 `scripts/merge_path.py:575` — `land --no-push` still writes a run event, "despite promising to record nothing".**
NOT A DEFECT in behaviour; the CLAIM was inexact, and is FIXED. A run event goes to the R17 private state home (never the repository, never the receipt) and every verb emits one — the contract itself says run events go there. What `--no-push` must not do is push or write a receipt step, and it does neither (`test_b2_land_in_NO_PUSH_mode_reads_the_verdict_and_pushes_nothing_anywhere`: no push of any kind, no receipt step, no push record; `test_b2_no_push_mode_*` for the rest). The help text and `lane-integrate.md` said "records nothing"; both now say it writes no receipt step and that the run event, carrying `no_push=true`, is still written. Wording only, so no RED test.

**Read 1 · P1 `scripts/merge_path.py:425` — a rehearsal record with no run identity or completion evidence is accepted.**
CONFIRMED, FIXED RED-first. A record holding only the schema, the sha, `event: push` and six `success` strings armed the ruleset. `rehearsal_problems` now requires an integer `run_id` (a `bool` is refused) and `run_status == "completed"`. Witnesses (RED at `3a83b5d3`, 7 of 7 failing): `test_b2_apply_refuses_a_record_with_no_run_identity_or_completion_evidence`, `test_b2_apply_refuses_a_record_whose_run_is_unnamed_or_not_completed`.

**Read 1 · P1 `scripts/known_reds.py:846` — the normalization masks every quoted set, so it can erase a genuinely changed assertion.**
CONFIRMED, FIXED RED-first; see the chain below (it took four reads to land the discriminator). Witness at read 1 (RED): `test_b2_a_set_of_quoted_values_that_are_not_file_names_is_not_masked`.

**Read 2 · P1 `scripts/known_reds.py:839` — the file-name heuristic masks arbitrary dotted values (`{'expected.v1'}`).**
CONFIRMED, FIXED, then superseded by the rule that landed (below). Witness: `test_b2_a_dotted_value_that_is_not_a_known_file_type_is_not_masked`.

**Read 2 · P1 `scripts/merge_path.py:435` — apply verifies only the record's self-reported sha, so a record copied from sha A's completed run with its `sha` edited to B arms the ruleset.**
CONFIRMED, FIXED RED-first. The record is self-reported evidence. `apply_preconditions(live_check=True)` — which the `apply` verb always sets — now re-reads the ONE run the record names (`verify_rehearsal_live`): it must be that sha's own completed `push` run, and every required context must be `success` in ITS live job list whatever the file says; an unreadable run or job list is a problem, never a pass. Witnesses (RED at `8174ee4d`, 7 failing): `test_b2_a_record_copied_from_another_shas_run_with_the_sha_edited_is_refused`, `…_claiming_success_the_live_run_does_not_show_is_refused`, `test_b2_the_live_run_must_be_a_completed_push_run`, `test_b2_an_unreadable_run_or_job_list_refuses_rather_than_trusting_the_file`, `test_b2_the_apply_verb_always_turns_the_live_check_on`, with `…_whose_run_really_ran_for_the_sha_passes_the_live_check` as the positive control. **Run live as well, against real GitHub, no seams:** a forged all-`success` record for run 37202610639 (pytest legs really red) is refused naming both legs; the reviewer's edited-sha copy is refused on the sha and on the contexts; run id `1` refuses on the 404.

**Read 3 · P1 `scripts/known_reds.py:845` — an extension whitelist masks `{'feature_on.py'}`; P2 `:844` — it misses `.rst` and others.**
CONFIRMED both; they pull in opposite directions, which is itself the finding that no extension list is the discriminator. FIXED: the per-merge value is the repo's own DATED artifact name (`YYYY-MM-DD-slug.ext`, which every audit carries). Witnesses (RED, 3): `test_b2_a_dated_artifact_name_normalises_whatever_its_extension[rst|lock]`, `test_b2_an_undated_file_name_is_an_assertions_own_content_and_is_not_masked`.

**Read 4 · P1 `scripts/known_reds.py:842` — a date prefix alone masks `{'2026-10-04-expected'}`.**
CONFIRMED, FIXED at `54d890a5`: the member must open with a date AND end in an extension. Witness (RED, 1): `test_b2_a_dated_value_that_is_not_a_file_name_is_not_masked`. This repair was NOT re-read by the reviewer; the line below is where the reads stopped.

**Residual, in the reviewer's own words (read 4):** "even a correctly constrained content-only matcher cannot distinguish a genuinely changed assertion involving two valid dated artifact names from the per-merge audit-file value." That is the honest ceiling of item 3's "normalize the per-merge value": a set of dated FILE names that genuinely changed is masked. Nothing narrower is possible from content alone; it would need non-content context (which merge added which audit file).

## Honest limits

- One reviewer, `reasoning effort: low`, four passes over diffs; the final repair (`54d890a5`) was not re-read.
- The reviewer's findings 2→4 on `normalize_signature` converge on an inherent ambiguity rather than a closing defect list; treat the date-and-extension rule as the best content-only rule, not a proof.
- The live re-read in `apply` is exercised by seam tests and by the three live probes above; the full `--execute` path (which sends to GitHub) was NOT run, by order.
- `ruleset rehearse` was run live once on the replay sha and mapped all six required contexts from real job names.
