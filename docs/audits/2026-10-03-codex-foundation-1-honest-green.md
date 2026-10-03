# Codex Review — foundation-1-honest-green

**Date:** 2026-10-03
**Branch:** `worktree-foundation-1-honest-green`
**HEAD at review time:** `6bfa5885`
**Diff range:** `origin/main...6bfa5885` (115,393 B, BACKLOG.md, `tasks/manifest.json` and the registry JSON diff excluded for size; the live registry was supplied whole)
**Codex version:** n/a — SUBSTITUTED under the batch order's review route (see below)
**Mode:** diff-review, fresh isolated session (contract + diff + live registry only — not the lane)
**Tally:** P1=0 P2=4 P3=2
**Consumer:** `LANE-FOUNDATION-foundation-1-honest-green.md` (item 8, "the review record")

**Model used:** `grok-4.6` (SUBSTITUTE for the pinned Codex terra — see Substitution note)
**Review profile:** code

---

## Substitution note

Codex terra is at its usage limit until 2026-10-03 21:07. The batch order's own route for this
window is `grok-4.6`, run read-only from a job-tmp folder (the step 0.5 shape of
`to-browser/EVAL-merge-path-grok-2026-10-03.md`). This is a recorded `SUBSTITUTION`, not a
silent one; isolation is by SESSION and by tool set — the session saw only `contract.md`,
`diff.patch`, `registry-live.json` and a `PROMPT.md`, with `read_file`, `list_dir` and `grep`
and no shell.

**Command:** `grok -m grok-4.6 --tools read_file,list_dir,grep --max-turns 40 -p <prompt>`
(grok 1.0.5), cwd a folder under the job's `tmp\` holding only the four files above.
**Served:** `grok-4.6` — `~/.grok/sessions/.../01a10226-3647-7a11-b325-4b7d5c0d0726/usage.json`
`"primaryModelId": "grok-4.6"`, 12 model calls, 709,902 tokens (the model's own last line says
only `SERVED: grok`). A first launch failed before any model call (argument quoting split the
prompt; `error: unrecognized subcommand 'in'`) and produced no session.

## Findings, verbatim from the reviewer, with the lane's disposition

**No P1.**

1. **P2** `tests/test_quota_daily.py:32` / `:133` — the primary-SessionStart cleanliness test is
   satisfied by the autouse `DEV_KNOWLEDGE_QUOTA_READS_LEDGER` override, so it never exercises
   the default ledger home. *Scenario:* restore `reads_ledger_path` to `repo_root /
   "logs/QUOTA-READS.jsonl"` with the override in place; the test still passes.
   **FIXED** (`7353fa6e`): the test now drops the override and redirects only
   `platformdirs.user_state_dir`, so the default resolution is what runs, and asserts the row
   landed in that home and outside the checkout.

2. **P2** `ecosystem/transport-registry.yaml:1155` — named by the contract as a reader to
   re-point, and not in the diff. **NO CHANGE NEEDED — PREMISE-FAILED, recorded.** The entry at
   `:1151-1162` is the `QUOTA_WARN` transport kind (`prefix: "QUOTA-WARN-"`, writer
   `quota_watch`, reader `gen_handoff`). It names no ledger path; a repo-wide grep for
   `QUOTA-READS` finds the readers this lane did re-point and no other. The reviewer inferred
   the reader from the contract's listing, not from the file.

3. **P2** `scripts/known_reds.py:115` / `registry-live.json:1161` — the windows overlay entry for
   `test_an_overrun_builder_does_not_release_its_SUCCESSORS_lock` carries `attribution: "flaky"`
   with no `signature`, so a different failure of that test is accepted as the known one.
   **NOT FIXED — a disclosed limit.** That test's failure text takes three distinct normalized
   forms over the six runs read (timing), so any single signature would read the flake itself as
   a changed failure. The registry's own `notes` say so; the entry is dated 2026-10-17 and owned
   by `[#664]`; row `[#1344]` removes it on 10 consecutive green windows runs.

4. **P2** `scripts/known_reds.py:194` — `_ceiling_problems` never requires `ceiling.max` to be
   tied to `growth.to`; a `/2` registry with `growth.to: 23` and `ceiling.max: 23000` loads, and a
   further bump reads as slack. **FIXED** (`7353fa6e`, RED first): `max` above `growth.to` is
   refused at load. `max` may sit below `growth.to`, which is what a lowered ceiling looks like.

5. **P3** `registry-live.json:200` / `:1168` — D8 states aj-scan → `decide.md` and carries no
   `ceiling`. **NO CHANGE — by design, stated.** D8 is a changed FIRST orphan, not a count that
   grows, so there is no number to cap; it is held by exact signature, so a later first orphan
   reads as a changed failure. The registry's AM2-3 note and the handback say so. The growing
   items are D5, D6 and D7 and each carries a ceiling.

6. **P3** `scripts/known_reds.py:434` — `refresh` carried a ceiling entry whose measured
   signature no longer carried the number. **FIXED** (`7353fa6e`, RED first): refresh refuses it
   ("no longer reads as the registered failure").

## Result

P1=0. Fixed: 3 (1, 4, 6). Disclosed limits, no change: 3 (2 — premise failed; 3 — flake text;
5 — not a count). The post-fix targeted run: `tests/test_known_reds.py`, `tests/test_quota_daily.py`,
`tests/test_quota_watch.py` — 161 passed.
