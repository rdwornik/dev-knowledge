# Codex Review — foundation-13-codespace-toolset

**Date:** 2026-10-04
**Branch:** `worktree-foundation-13-codespace-toolset`
**Diff range:** `origin/main...a550f05b` (the lane's change before the review fixes; `diff.patch` in the review folder)
**Mode:** diff-review, isolated read-only folder under the job tmp holding the patch, post-change copies of the changed files, the contract and `nonce.txt`
**Tally:** P1=1 P2=2 P3=3 (all three P1/P2 code findings fixed or recorded; see dispositions)
**Consumer:** `LANE-FOUNDATION-foundation-13-codespace-toolset.md` (Done-contract item 4, "a review record, Codex terra first")

**Route:** Codex terra, first choice (Codex answered, no limit message). No `SUBSTITUTION`.

## Proof of read (R59 §0a item 1)

- **Served model id, from the tool's own run header and the rollout file:** `gpt-5.6-terra`, sandbox `read-only`, reasoning effort `low`, session id `01a1048f-51c5-7921-acfc-dbada20c3429`.
- **Nonce:** `nonce.txt` held `NONCE-1d492ac5ef07`; the reviewer's first line was `NONCE: NONCE-1d492ac5ef07` — matches.
- **DIFF-FIRST-LINE returned:** `diff --git a/.devcontainer/provision.sh b/.devcontainer/provision.sh` — matches the first line of the patch.

## Findings and dispositions

```
P1  provision_legs.py:849   a probe that timed out or could not start was read as "absent" -> exit 1 (drift)
    DISPOSITION: FIXED  probe rc 124/126 now state "unavailable"; `tools check` exits 2 (could not look), 1 stays for looked-and-found-drift.
                        RED-first: test_a_probe_that_could_not_run_is_unavailable_not_absent[124/126],
                        test_tools_check_exits_2_when_it_could_not_look_and_1_when_it_looked_and_found_drift.
P2  codespace_parity.py:279 any failed auth-status command recorded as "unauthenticated" -> could mask an unrunnable probe as a named auth exception
    DISPOSITION: FIXED  rc 124/127 -> state "probe-error"; C1 FAILS with "the auth probe for <tool> could not run".
                        RED-first: test_an_auth_probe_that_could_not_run_is_not_an_unauthenticated_tool,
                        test_an_auth_probe_error_on_the_codespace_fails_c1_instead_of_naming_an_exception.
P2  provision.sh:743/848    claude and agy install via vendor scripts fetched at run time, not hash-pinned
    DISPOSITION: RECORDED, NOT FIXED  neither vendor offers a version-pinned, integrity-verified installer for the Linux Codespace
                        (claude's installer takes a version but the script itself is mutable; agy's takes none). The final
                        `tools check` verifies the installed CLI version, not the installer code. Written into
                        provisioning.yaml as an HONEST LIMIT comment (a named supply-chain exception) rather than claimed as pinned.
P3  codespace_parity.py:454 `match()` with a `$`-anchored regex accepts a trailing newline
    DISPOSITION: FIXED  `.fullmatch` at both uses.
P3  test_codespace_parity.py:717 invalid-name test lacked the trailing-newline case
    DISPOSITION: FIXED  test_a_probe_name_with_a_trailing_newline_is_refused[probe.txt\n | probe.txt\r\n | x\n].
P3  run record:65           "all four legs assert clean" while five F5 legs exist
    DISPOSITION: MISREAD, CLARIFIED  that line is `provision.sh`'s pre-existing, unchanged DONE wording (it counts the original
                        four assertion legs, not F5). A note was added beside it in the run record.
```

## Reviewer output (verbatim)

```
NONCE: NONCE-1d492ac5ef07
DIFF-FIRST-LINE: diff --git a/.devcontainer/provision.sh b/.devcontainer/provision.sh

## P1

P1, scripts__provision_legs.py:849, what: Tool probe execution failures are converted to exit 127 and then classified as "absent," making `tools check` return 1 rather than unavailable (2). why: A timeout, shell failure, or execution error can trigger installation/container failure as if a verified tool violation occurred. fix direction: Preserve probe-unavailable state separately and return exit 2 for probe execution failures.

## P2

P2, scripts__codespace_parity.py:279, what: Any failed auth-status command is recorded as `unauthenticated`. why: A timeout, broken status subcommand, or runtime error can produce `PASS except named auth items`, masking inability to perform the auth check. fix direction: Record an explicit auth-probe-error state and make C1 NOT-RUN/FAIL rather than treating it as an auth exception.

P2, .devcontainer__provision.sh:743, what: Claude is installed by executing the mutable, unversioned `https://claude.ai/install.sh`; agy similarly executes an unpinned installer at line 848. why: The final version check verifies the resulting CLI version but not the installer code executed during container creation. fix direction: Use a versioned, integrity-verified artifact/installer where available; otherwise explicitly treat the unpinnable installer as a supply-chain exception rather than a pinned installation.

## P3

P3, codespace_parity.py:454, what: Probe-name validation uses `match()` with a `$`-anchored expression, which accepts a trailing newline. why: This does not fully enforce the claimed "single plain file name" invariant. fix direction: Use `fullmatch()` and add a newline-containing rejection test.

P3, tests__test_codespace_parity.py:717, what: The invalid probe-name test omits the trailing-newline case accepted by the implementation. why: The path-safety test is incomplete and would not catch the validation gap. fix direction: Add invalid names such as `"probe.txt\n"`.

P3, docs__audits__2026-10-04-technical-codespace-toolset-run.md:65, what: The pasted provisioning evidence says "all four legs assert clean," while the record lists five F5 tool legs. why: The claim is internally inconsistent and does not accurately describe the asserted toolset. fix direction: Correct the pasted evidence/interpretation to identify all five legs.

TALLY P1=1 P2=2 P3=3
```

## Verdict

The P1 is fixed and proven RED-first then GREEN (targeted run: 356 passed, 1 skipped, 1 failed — the one failure is `test_history_check_exits_0_on_this_repo`, red in every lane worktree because local `main` is behind `origin/main`, lane 5's known ROWS-OWED, not this lane's). The reviewer was not re-run on the fix diff; the fixes are each covered by a RED-first test.

## Amendment 2026-10-04 -- repair 1 (edge-class census row)

The integrator's check (b) refused `scripts/provision_legs.py`: the Actions-only hook `graph-edge-class-census` read its two version regexes (`_PIN_RE`, `_VERSION_RE`) as the five-kind edge-computation shape. A one-row data change, `"scripts/provision_legs.py": _not_an_edge(...)` in `scripts/graph_queries.py` `EDGE_COMPUTATIONS`, verdicts it out of the class: the regexes parse a tool version string off a `--version` probe and compare it with a hand-declared pin in `provisioning.yaml`; no corpus relation is computed. `provision_legs.py` itself is unchanged (not reshaped to slip under the predicate).

Reviewed by this lane's own read, not by a fresh Codex terra pass (the refusal says a fresh read is welcome, not required for a register row). RED/GREEN by the conductor's sequence (soft-reset to the merge-base with `origin/main`, then `pre-commit run graph-edge-class-census --hook-stage manual`): RED exit 1 naming `scripts/provision_legs.py` at `66a18389`; GREEN exit 0 at `207c0214`. Contract: `LANE-FOUNDATION-foundation-13-codespace-toolset.md` (repair claim `...-repair-1`).
