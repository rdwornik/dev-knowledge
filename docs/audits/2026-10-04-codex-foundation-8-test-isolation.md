# Codex Review — foundation-8-test-isolation

**Date:** 2026-10-04
**Branch:** `worktree-foundation-8-test-isolation`
**Diff range:** `origin/main...HEAD` at tip `7dc45a8f` (base `ae54e7da`, the sha this lane merged at step 0)
**Mode:** diff-review, isolated read-only session (the diff, the five changed files, three unchanged scripts and the probe, in an empty folder — not the lane)
**Consumer:** `LANE-FOUNDATION-foundation-8-test-isolation.md` (Done-contract item 3, "the review record citing this contract inside it")

**Model used:** `gpt-5.6-terra` (served — read from the run's own header: `OpenAI Codex v0.155.0`, `model: gpt-5.6-terra`, `provider: openai`, reasoning effort low)
**Review profile:** code
**Tally:** P1=1 P2=1 P3=0. The reviewer's verdict line read `reject`, reported as given. P1 fixed; P2 disputed (below).

No substitution: Codex was past its usage limit (21:07 on 2026-10-03), so the registry's first route ran.

**Command:** from an empty job-tmp folder holding `diff.patch` (`git diff origin/main...HEAD`), `changed/` (the three test files, the registry, the `tasks/1350` row), `context/` (unchanged `graph_store.py`, `transport.py`, `deny_and_point.py` and the in-process probe the registry reasons cite), `contract.md` (this lane's frozen contract), `nonce.txt` and `prompt.md` —
`codex exec -c model=gpt-5.6-terra --sandbox read-only --skip-git-repo-check --output-last-message codex-out.txt -` with the prompt on stdin; started 2026-10-04 02:42 local; exit 0.
**Output contract (R59 item 1):** the answer had to open with the nonce from `nonce.txt` and quote the first line of `diff.patch`; it did
(`NONCE-3e259351007d`; `diff --git a/BACKLOG.md b/BACKLOG.md`).

| finding | disposition |
|---|---|
| **P1** `tests/test_deny_and_point.py:221` — the new child-pytest call adds `timeout=300`, contrary to the contract's "never raise a timeout" | **Fixed.** The call had no timeout before and none is needed for a ~1 s child run; the argument is removed. (A note, not a finding: the reviewer read an added bound as a raised one; the bound is removed either way.) |
| **P2** `tasks/1350-…md:12` — `kill-candidates: none` is inside the list item, not flush-left | **Disputed, no change.** N4 requires the flush-left line in the COMMIT message, and `7dc45a8f` carries it. The row's own `· kill-candidates:` clause follows the shape of the neighbouring filed rows `[#1344]` and `[#1349]`, and `gen_task_tree.py --check` passes on the tree with it. I did not test whether a flush-left line inside a task file would parse. |

The review confirmed, with no finding: the `owned_store` fixture patches `graph_store.store_path` to a populated SQLite store the test owns; the subprocess test's separate bare `GIT_DIR`, `-n 0`, direct node ids and the `"2 passed"` check are not vacuous or materially OS-fragile; the two causes follow from the unchanged code (the graph-store token is only PID plus `time.time_ns()`; transport retries only `FileExistsError`), so quarantine rather than a script edit is what N5 asks; the registry rows carry task, owner and expiry and no re-signed signature; no skip, deselection, `xfail` or weakened assertion was added.
