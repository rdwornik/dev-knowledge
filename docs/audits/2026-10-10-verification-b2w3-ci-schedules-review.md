# Close-out diff review -- b2w3-ci-schedules resume 1 (Copilot route, Codex limit-refused)

**Date:** 2026-10-10
**Branch:** `worktree-b2w3-ci-schedules`
**Reviewed range:** `c399a1f7..028b1f58` over `pyproject.toml` (`[tool.mutmut]` only), `.github/workflows/report-only-wall.yml`, `tests/test_report_only_wall.py`, `logs/MUTATION-BASELINE.json` (`diff.patch` sha256 prefix `da798317014e`)
**Mode:** close-out diff review of a resume (common rules 2 (e), S-38 (b), `to-cc/AMEND-BATCH-B2-W3-CI-CLOCK-2026-10-10.md` S-56)
**Tally:** 0/1/2/0 <!-- Critical/High/Medium/Low -->

Consumer: lane contract `LANE-1103-b2w3-ci-schedules.md` (batch B2-W3, lane 3) as resumed by `to-cc/AMEND-BATCH-B2-W3-CI-CLOCK-2026-10-10.md` S-56 (`[#1103]`; contract Done-contract item 6 requires this record; amend sha256 prefix `58f6693698e9`, contract prefix `c3b52fc4687f`).

## Route and proof of reading

- **First route, Codex `gpt-6-astra`, refused on a usage limit.** `deploy/codex-review.ps1 -Topic b2w3-ci-schedules-resume-1 -DiffRange c399a1f7..HEAD` (codex-cli 0.155.0, session `01a12705-653f-7db3-a2e0-e19f8ef6abed`, header `model: gpt-6-astra`) ran at 2026-10-10T18:13Z and ended with `You've hit your usage limit ... try again at 9:40 PM.` (9:40 PM local is 19:40Z.) Not retried inside that window. No review output exists from it, and the wrapper wrote no record.
- **Second route (S-38 order 2), the Copilot CLI**, a different vendor from the producer (Anthropic): `copilot -p ... --model gpt-6.1-sol --add-dir <isolated folder> --allow-all-tools --no-ask-user -s --no-color --usage-output-file`, started 2026-10-10T18:32:58Z.
  - **Served model id, from the tool's own usage file** (sha256 prefix `0782996444ba`): `modelMetrics` key `gpt-6.1-sol`, 1 user request, `totalPremiumRequestCost` 1.
  - **Nonce returned:** `4500d7b2582d` (the value in the folder's `nonce.txt`), as the first line of the reply (reply sha256 prefix `a1826c831d52`).
  - **Input hashes returned and matching the files read:** `diff.patch` `da798317014e`, `amend-s56.md` `58f6693698e9`, `contract.md` `c3b52fc4687f`.
- The folder held only the contract, the amend, `diff.patch`, the four changed files at the reviewed tip, the artifact `mutmut.out` of the seeding run 38073707389, `prompt.txt` and `nonce.txt`.

## Findings

CRITICAL: (none)

HIGH -- `.github/workflows/report-only-wall.yml:343-349`: the new step treats processed mutants as executed ones. The N of mutmut's `N/M` also counts `no tests` mutants (the seeding artifact opens with `1/2291 ... 1`), so a run with `2291/2291  killed 0, no tests 2291` and every other status 0 passes the step while no mutant was executed. The same predicate sat in the seed test (it summed every status). Fix direction: require at least one genuinely executed outcome, add a no-tests-only regression case.

MEDIUM -- `tests/test_report_only_wall.py:340-341`: the seed's provenance was only shape-checked; a well-formed wrong run id and a wrong 40-hex sha passed. Fix direction: assert the expected run id and sha, and the run url and artifact name against them; add wrong-but-well-formed cases.

MEDIUM -- `tests/test_report_only_wall.py:215-225`: the `also_copy` ordering test was vacuous when the table is absent (the loop ran zero times), so reverting the configuration left it green. Fix direction: require the file entry first and keep lone-file and reversed-order negative cases.

LOW: (none)

The reviewer also stated: the diff changes only `also_copy` inside `[tool.mutmut]`, the directory-first order creates `ecosystem` before the bare `copy2`; UTF-8 decoding and carriage-return handling accept the supplied healthy artifact, and missing output, a zero progress line, generation-only output and a failed collection are rejected; no existing assertion is weakened, no `contents: write` is added, and survival stays report-only.

TALLY CRITICAL:0 HIGH:1 MEDIUM:2 LOW:0

## Disposition

- **HIGH fixed**, RED first: `0d3178d7` adds the `only-no-tests` case (it failed: the vacuous run exited 0 with `2291 of 2291 mutants executed`), `f43f95b2` makes the step count killed + survived + timeout + suspicious. The real artifact of run 38073707389 through the real step now prints `2077 of 2291 mutants executed (2291 checked)`.
- **Both MEDIUMs fixed** in `0d3178d7`: the seed test pins run id `38073707389` and sha `3c923880...` and checks the run url and artifact name against them (`wrong-run-id`, `wrong-sha` cases); the ordering test requires the spec entry, goes through a helper, and fails with `also_copy` removed (shown: 2 failed with the key deleted).
- The reviewer ran no tests; its stated limit is a read of the supplied files.
