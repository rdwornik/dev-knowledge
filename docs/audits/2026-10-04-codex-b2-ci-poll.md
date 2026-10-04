# Codex Review — b2-ci-poll

**Date:** 2026-10-04
**Branch:** `worktree-b2-ci-poll`
**HEAD at review time:** `2166b06a` (read 1, the code); `122a8a37` (read 2, the fix)
**Diff range:** `origin/main...HEAD` (merge-base `1546090c`), limited to `tests/test_connection_loop.py`; `ecosystem/doc-counts.md` is a regenerated count and was told to be ignored
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review, `--sandbox read-only` from the lane's own worktree (not a copied folder: the reviewer could read the whole tree, never write it)
**Tally:** read 1 Critical=0 High=1 Medium=0 Low=0 · read 2 Critical=0 High=0 Medium=0 Low=0 — the one High fixed (below)
**Consumer:** `LANE-B2-W1-b2-ci-poll.md` Done-contract item 5 ("the review record"); `docs/decisions/ADR-127-ci-os-verification.md`; `[#889]`

**Model used:** `gpt-5.6-terra` — the served id, read from each run's own header (`model: gpt-5.6-terra`, provider openai, `reasoning effort: high`, sessions `01a108b2-b577-7201-bcbe-a4e37d48b1ab` and `01a108bd-c9cc-7123-93a4-334204550c6b`). No substitution was needed.
**Review profile:** code

---

## How it was run

`codex exec --sandbox read-only -c model=gpt-5.6-terra -c model_reasoning_effort=high --output-last-message <file> -`, the prompt on stdin from a file (a bare `codex exec` can hang reading it), launched detached. Each prompt told the reviewer to run `git diff origin/main...HEAD` itself, stated the contract's intent, named the claim to attack, and required its first reply line to be a nonce.

| Read | Diff reviewed | Nonce returned (line 1, verbatim) | sha256 of the raw answer (first 16 hex) | Tally |
|---|---|---|---|---|
| 1 | the lane diff at `2166b06a` (wait fix, comment fix, four tests) | `NONCE-HTKLP5F4QS` | `42fcf5a792b3dd03` | High=1 |
| 2 | the fix, `122a8a37` | `NONCE-ELD4HA80MY` | `59048228837830c8` | none |

## The claim read 1 was asked to attack

After `World.run(...)` (a synchronous subprocess of the declared Stop command, not backgrounded) returns, `not receipt.exists()` means the guard took no claim and spawned no worker: `lane_end_guard.main` writes the `running` claim (`_write_atomic(receipt_path, claim_receipt)`, `scripts/lane_end_guard.py:302`) before it calls `spawn_worker` (`:311`), and returns 0 on every path. Read 1 found no path by which the receipt is absent at that instant and a worker writes one later, and no change in what the positive-path caller (`walk_the_loop`, `world.stop_hook(worktree)` then the lane-end receipts) sees.

## Findings and dispositions

| Read | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | High | `tests/test_connection_loop.py` (the bound test): it asserted `300 <= waited <= 301`, so a `LANE_END_WAIT_S` raised to 301 would still pass and the frozen 300 s bound would not be pinned | **Fixed** in `122a8a37`: `assert waited == 300` and `assert LANE_END_WAIT_S == 300`. Witnessed: with the constant mutated to 301 the test fails (`the wait ended at 301s, not at the 300 s bound`, 1 failed, 3 passed); restored, 4 passed. |
| 2 | — | "Fix verified … No assertions were removed or weakened relative to `origin/main`. No new findings." | none needed |

Read 1's other bands were `(none)`: it raised nothing on xdist leakage of the monkeypatched module `time` / `World.run` (both are `monkeypatch.setattr`, undone at test end) and nothing vacuous in the four tests.
