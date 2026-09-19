# Wave-3 L3 -- the hub plans and governs, a caller-side shim spawns; a launch that cannot be bound is stopped

- lane: `wave3-dispatch-split` (Sonnet producer, `--bg`, own worktree) · branch `worktree-wave3-dispatch-split`
- base: `c00f9c10` (L3 of night wave 2, `worktree-wave2-dispatch`) -- the branch was BRANCHED FROM it, not merged onto main (amendment 1)
- rulings implemented, not re-decided: `protocols/BUILD-LIST.md` Decisions 2026-09-19 "Dispatch / Layer 2" -- (a) LAYER-2: the hub ships the code, the caller runs it; (b) TOKEN CAP: a default `--bg --worktree` launch binds its own usage with no `--slug-dir`, and an unbindable or over-cap launch is REFUSED / STOPPED, never left running and reported as ungoverned
- tip when the witnesses ran and the last review came back clean: `b9a98421`; **no code has changed since `1f742353`**

## 0. Amendments received, verbatim

**Base contract step 0** said to merge `c00f9c10` onto main and named the merge clean. It conflicted in `JOURNAL.md` (L3 prepends two entries there, main had prepended five since). The lane STOPPED and reported, per its own refute rule.

**Amendment 1 -- integrator, 2026-09-19 (peer session "worktree wave2 cleanup"):**

> CONTRACT AMENDMENT (integrator, 2026-09-19): step 0 was mis-specified. Your pause was correct: the premise was mine and it was false. Take neither option 1 nor 2. Do this instead:
>
> STEP 0 (amended): the operator's order is that this lane is BRANCHED FROM c00f9c10, not that c00f9c10 is merged onto main. Your branch has no commits and a clean tree, so run:
>   git reset --hard c00f9c10
> Verify `git log -1` shows c00f9c10 and `git status` is clean. Seed ecosystem/*/state.yaml from the primary checkout if absent. There is no step-0 commit.
>
> JOURNAL.md stays out of your footprint entirely. L3's (ae)/(x) entries ride along untouched, and I resolve the JOURNAL conflict and re-letter at the step-3 merge, which is the integrator's surface. Do not edit JOURNAL.md.
>
> Everything else in the contract stands unchanged: steps 1-6, the done-contract, the footprint, commit-and-STOP, no push. Record this amendment verbatim in your end-of-lane artifact. Continue now.

Done: the branch had 0 commits and a clean tree before `git reset --hard c00f9c10` (no commits, clean tree); afterwards `git log -1` showed `c00f9c10` and the tree was clean. `ecosystem/*/state.yaml` are present in the worktree. `JOURNAL.md` is untouched by this lane (`git diff c00f9c10..HEAD -- JOURNAL.md` is empty).

**Operator ruling (user message, 2026-09-19, relayed into the session):**

> Ruling on the JOURNAL.md conflict: do NOT resolve it. Leave JOURNAL.md exactly as the base has it and continue with the rest of the contract. Under STANDING_RULINGS P-1 a lane does not write JOURNAL; the integrator anchors at merge and resolves this collision — it already did so losslessly for L2 today (19 insertions, 0 deletions). The contract's refute rule fired correctly on a premise I got wrong: I assumed L3 did not touch JOURNAL. It does, in its seven inherited commits. Everything else in the contract stands, including the mandatory live `--bg` witness: the handback must carry the verbatim output of a real launch over the cap being REFUSED, and one under it running. A green tally is not a witness.

**Amendment 2 -- integrator relaying an operator order, 2026-09-19:**

> CONTRACT AMENDMENT 2 (integrator relaying an operator order, 2026-09-19): done-when 3 is strengthened. This is a MERGE BLOCKER.
>
> The handback artifact must carry the VERBATIM terminal output, pasted in full rather than summarised, of TWO real launches made through the shim, each `--bg --worktree`, NO --slug-dir, explicit --model haiku:
>   (A) OVER the cap: a small cap the lane will exceed. Show it REFUSED or STOPPED with the refusal exit code, and never reported UNGOVERNED after blind polls.
>   (B) UNDER the cap: a cap it stays under. Show that it runs, that its usage is read, and that it ends normally.
> For each: the exact command, its full output, the exit code, the ORDERED cap vs RAN tokens, and the witness worktree + branch removed with the `git worktree list` / `git branch -a` output after removal pasted.
>
> A test tally is NOT a substitute. If either witness cannot be produced, do NOT claim done. Write the blocker (the exact error output) into the handback, commit, and STOP.
>
> Also in the handback: state whether the codex terra RE-REVIEW of your fixes (12977bdb) came back clean, with its tally. Re-reviewing the fixes is required, not only the original findings.
>
> Everything else stands. Record this amendment verbatim in the end-of-lane artifact.

Both witnesses were produced (section 3). **The codex terra RE-REVIEW of the fixes came back CLEAN on the fifth pass, tally 0/0/0/0** -- but the first four passes were not clean; see section 4 for all five.

## 1. What changed

| Surface | Before (`c00f9c10`) | After |
|---|---|---|
| `scripts/dispatch.py` | `launch` verb: contract -> `subprocess.run(plan.argv)` -> govern; `run_streamed` `Popen`ed codex / `claude -p` lanes | two verbs, **neither starts a lane**: `plan` (contract -> JSON plan) and `govern` (lane id -> bind, poll, stop, commit-witness); plus `stop --slug` (recovery). `launch`, `run_streamed`, `--slug-dir`, `_lane_reader`, `--dry-run` are gone. AST test `test_the_hub_dispatch_module_spawns_no_lane`: no `Popen`, `os.system` or `run(plan.argv)` |
| shim | audit section 5 sketch, `[string]$Model = 'opus'` (defect `[#717]`) | `templates/dispatch-shim.ps1`: runs `plan`, runs the plan's argv (the ONLY spawn), hands the lane to `govern`. **No model or effort default** |
| usage binding | slug matching over `~/.claude/projects`; blind after 8 polls = UNGOVERNED, lane left running | `bind_lane` reads the lane's session id + cwd from `claude agents --json`; reader is `lane_cost.seat_usage(session_id)` (by id, store-wide). No slug, no `--slug-dir` |
| unbindable / blind / probe-failed / interrupted / governor-crashed lane | reported ungoverned, **left running** | **stopped**, exit 5. Exit 4 only when a stop could not be confirmed, or nothing verified could be stopped ("may be running") |
| over cap | stopped, exit 3 | unchanged |
| `lane_alive` | `lane_id in listing.stdout` -- a finished lane stays listed with `state: done`, so it read alive forever | reads the record's `state` |
| model/effort | `--model` default `opus`, `--effort` default `medium` | from the contract's `\| Model \| Mode \| Effort \|` table, or `--model`/`--effort`; a contract with neither is REFUSED |
| `CLAUDE_PROMPTS_DIR` | process env only | User-scope registry value first (`windows_user_env`), then process copy, then `~/Downloads` |
| done means a commit | absent from the port (it lived in win-tooling's off-machine receipts) | `commit_witness`: DONE / FAILED / UNWITNESSED from the branch's reflog start point vs its tip; a finished-under-cap lane with no commit exits 6, an unwitnessable one 7 |

**Exit codes:** 0 ok and DONE · 3 cap exceeded, lane stopped · 4 UNGOVERNED -- the lane may still be running · 5 REFUSED -- usage could not be bound; the lane was stopped (or had already ended) · 6 finished under cap but committed nothing · 7 finished under cap, commit unwitnessed.

**Corrections to the contract's premises** (both surfaced, neither decided around): (1) the contract listed "done-means-a-commit" and the User-scope prompts dir as things the port "already has"; neither is in `scripts/dispatch.py` at `c00f9c10` (`grep -c commit` = 0; the move audit section 2 lists the registry read as NOT moved) -- both are built here and tested. (2) The contract's library-first lead (`gen_handoff._session_slug`, a mangled worktree path -> transcript directory) was checked and is the weaker fit: the listing states the session id outright and `lane_cost.seat_usage` already reads by it, so no directory has to be derived. `_session_slug` was not used.

**Superseded L3 tests** (a contract change, not a weakening -- listed so none is lost silently): an unobservable lane was asserted ungoverned / not stopped (exit 4) and is now asserted stopped / exit 5; a lane that ends with its spend unread was exit 4, now exit 5; `run_streamed`'s spawn tests became `meter_lines` callback tests; the `--slug-dir` reader test is gone with the flag; the `launch --dry-run` tests became `plan` tests.

**Tests:** 85 across `tests/test_dispatch_py.py`, `test_dispatch_split.py`, `test_dispatch_review_fixes.py`, `test_dispatch_review_fixes_2.py`, `test_dispatch_shim.py` (the last runs the shim under pwsh against stub `uv` / `claude`; nothing starts a lane). `uv run --locked ruff check` clean. RED commits (each committed failing, before its fix): `018b1437` (the split), `1a64ce57`, `5bc9c3f9`, `84008b9d`, `7aa37b0a` (one per review pass); the build is `f09c7ac8`.

## 2. What was NOT built, and the honest limits

- **Stream-metered lanes** (codex, `claude -p`, the codespace substrate): the metering primitive `meter_lines` stays, tested, but there is **no caller-side spawner** -- a spawner has to own the child to terminate it, and a PowerShell pipe to a downstream meter was not shown to kill the upstream. The shim REFUSES them (exit 2) rather than run them ungoverned. This is a scope call that falls out of "no hub script spawns a lane"; it removes a capability the unmerged L3 had.
- **The cap is a poll.** Witness A: cap 5,000, ran 27,670 (2 model calls, 27,178 of it cache-write, before the first poll could act). It is enforced at poll granularity, never mid-message.
- **Cache reads are not counted** (Witness B: 636,122 cache-read tokens were excluded from the 39,999 counted; `--count-cache-reads` includes them).
- **Not exercised live:** the `stop --slug` verb, `find_lane_by_slug` and the shim's governor-failure recovery (tests and the pwsh stub test only); the exit-4 "may be running" paths; a lane finishing under cap with NO commit (exit 6). What the live runs DID prove about them: the real `claude agents --json` `cwd` is `...\worktrees\<slug>`, so `_cwd_is_lane` holds on real data (both witnesses passed it), and `id` / `sessionId` / `state` are the real field names.
- **An unexplained line** appears in every real launch, between the `plan` call and `claude`'s own output: `'m' is not recognized as an internal or external command, operable program or batch file.` Its source is not identified (it appears identically in witnesses A and B and in the earlier pre-fix witness); it did not affect either run. Not investigated -- outside the lane's footprint.
- `git branch -d` refuses witness B's branch (two unmerged commits), so it was removed with `-D` after `git log b9a98421..worktree-wave3-witness-b` showed only `witness` and a `JOURNAL` entry the lane wrote because the repo's own CLAUDE.md told it to. The contract ordered the removal.

## 3. The live witnesses -- real `--bg --worktree` launches through the shim, no `--slug-dir`, `-Model haiku`

Both ran from this lane's own worktree (`-Hub $PWD`), on `b9a98421`, with `-Interval 5`. Contracts were disposable files in `%TEMP%` (deleted after). The order is A then B.

### 3A. OVER the cap -- STOPPED, exit 3, never UNGOVERNED

Contract `LANE-wave3-witness-a.md`: model table `haiku / execute / low`; "Read scripts/dispatch.py in full, then scripts/lane_cost.py in full, then write a ten-line summary of each in chat. Do not edit, create or commit any file."

**Command and full output, verbatim:**

```
HEAD: b9a98421
PS> & 'C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\wave3-dispatch-split\templates\dispatch-shim.ps1' 'C:\Users\1028120\AppData\Local\Temp\LANE-wave3-witness-a.md' -TokenCap 5000 -Model haiku -Interval 5 -Hub 'C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\wave3-dispatch-split'
start: 2026-09-19T17:31:51.4064626+02:00
warning: `VIRTUAL_ENV=C:\Users\1028120\Documents\Dev\.dev-knowledge\.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
'm' is not recognized as an internal or external command,
operable program or batch file.
backgrounded · 13493aa1
  claude agents             list sessions
  claude attach 13493aa1    open in this terminal
  claude logs 13493aa1      show recent output
  claude stop 13493aa1      stop this session
warning: `VIRTUAL_ENV=C:\Users\1028120\Documents\Dev\.dev-knowledge\.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
[dispatch] governing lane 13493aa1 (session 13493aa1-b4a7-43e7-8890-ba92b98e126f) -- cap 5000
[dispatch] CAP EXCEEDED -- lane stopped: used 27670 of 5000 tokens
shim exit=3
end: 2026-09-19T17:32:35.4576759+02:00
```

- **Exit code: 3** (`EXIT_CAP_EXCEEDED`).
- **ORDERED cap 5,000 vs RAN 27,670 tokens** (the governor's own figure).
- Independent check, read straight from the lane's session transcript with `lane_cost.seat_usage("13493aa1-b4a7-43e7-8890-ba92b98e126f")` after the run: `claude-haiku-4-5-20251001` input 18 + output 474 + cache-write 27,178 = **27,670**, 2 calls, plus 85,810 cache-read tokens not counted against the cap. Model confirmed `haiku`.
- Bound by session id from `claude agents --json` (no slug, no `--slug-dir`); never reported UNGOVERNED.
- Removal: `git worktree unlock`, `git worktree remove`, `git worktree prune`, then `Deleted branch worktree-wave3-witness-a (was b9a98421).` (`-d`, contained).

### 3B. UNDER the cap -- runs, usage read, ends normally, exit 0

Contract `LANE-wave3-witness-b.md`: model table `haiku / execute / low`; "Create a file named witness-b.txt in the current directory containing the single line OK. Commit it with `git add witness-b.txt` and `git commit -m "witness"`. Then reply with the single word DONE and stop. Do not read or edit any other file."

**Command and full output, verbatim:**

```
HEAD: b9a98421
PS> & 'C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\wave3-dispatch-split\templates\dispatch-shim.ps1' 'C:\Users\1028120\AppData\Local\Temp\LANE-wave3-witness-b.md' -TokenCap 1000000 -Model haiku -Interval 5 -Hub 'C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\wave3-dispatch-split'
start: 2026-09-19T17:33:10.6007690+02:00
warning: `VIRTUAL_ENV=C:\Users\1028120\Documents\Dev\.dev-knowledge\.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
'm' is not recognized as an internal or external command,
operable program or batch file.
backgrounded · d20da113
  claude agents             list sessions
  claude attach d20da113    open in this terminal
  claude logs d20da113      show recent output
  claude stop d20da113      stop this session
warning: `VIRTUAL_ENV=C:\Users\1028120\Documents\Dev\.dev-knowledge\.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
[dispatch] governing lane d20da113 (session d20da113-2783-4697-a900-4e0090571f98) -- cap 1000000
[dispatch] finished under cap: used 39999 of 1000000 tokens
[dispatch] DONE: 2 commit(s) on worktree-wave3-witness-b
shim exit=0
end: 2026-09-19T17:35:42.1053601+02:00
```

- **Exit code: 0.** Ran 2 min 32 s.
- **ORDERED cap 1,000,000 vs RAN 39,999 tokens** (under). Independent check from the transcript, `seat_usage("d20da113-2783-4697-a900-4e0090571f98")`: haiku input 92 + output 2,773 + cache-write 37,134 = **39,999**, 11 calls, plus 636,122 cache-read tokens not counted.
- Usage was read (the governor's figure equals the transcript's), the lane ended `state: done`, and `commit_witness` returned DONE -- **done-means-a-commit exercised live**. The count says 2 because the lane, following this repo's own CLAUDE.md, also wrote a JOURNAL entry: `git log b9a98421..worktree-wave3-witness-b` showed `29cb5c66 docs: add witness-b session entry to JOURNAL` and `068e37ae witness`. That branch was discarded, not merged.
- Removal: `git worktree unlock`; the first `git worktree remove` failed -- `error: failed to delete '.../worktrees/wave3-witness-b': Permission denied` -- because the finished lane's idle process still held the directory. `claude stop d20da113` stopped it, leaving an empty directory that `rmdir` removed; `git worktree prune`; `git branch -D worktree-wave3-witness-b` -> `Deleted branch worktree-wave3-witness-b (was 29cb5c66).`

### 3C. After BOTH removals -- CLAUDE.md section 5 rule 9, pasted verbatim

`git worktree list`:

```
C:/Users/1028120/Documents/Dev/.dev-knowledge                                        56ec7dc3 [main]
C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/worktrees/wave3-answerable     15aa18f0 [worktree-wave3-answerable] locked
C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/worktrees/wave3-dispatch-split b9a98421 [worktree-wave3-dispatch-split] locked
C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/worktrees/wave3-hookmap        37858811 [worktree-wave3-hookmap] locked
C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/worktrees/wave3-spine-fixups   2dd1d955 [worktree-wave3-spine-fixups] locked
```

`git branch -a`:

```
  automation/fleet-audit
+ main
  worktree-wave2-dispatch
+ worktree-wave3-answerable
* worktree-wave3-dispatch-split
+ worktree-wave3-hookmap
+ worktree-wave3-spine-fixups
  remotes/origin/HEAD -> origin/main
  remotes/origin/automation/fleet-audit
  remotes/origin/claude/conformance-2026-09-18
  remotes/origin/claude/conformance-2026-09-19
  remotes/origin/main
  remotes/origin/worktree-wave2-dispatch
```

No `wave3-witness-a` / `-b` in either; `git ls-remote --heads origin "worktree-wave3-witness*"` empty (nothing was ever pushed); `.claude/worktrees/` lists no witness directory. The other lanes shown (`wave3-answerable`, `wave3-hookmap`, `wave3-spine-fixups`, and `worktree-wave2-dispatch`) are not this lane's and were not touched.

### 3D. An earlier witness, on the pre-fix tree (superseded, kept for the record)

Before the review passes, one witness ran at `f09c7ac8` (contract `LANE-wave3-witness.md`, cap 5,000, `-Model haiku`): `[dispatch] governing lane 4c128d01 (session 4c128d01-2525-46d5-aedc-3fa8b6bba228) -- cap 5000` then `[dispatch] CAP EXCEEDED -- lane stopped: used 57081 of 5000 tokens`, exit 3; the transcript read back 18 + 459 + 56,604 = 57,081. It is superseded by 3A and B, which ran on the final tree.

## 4. Codex terra review -- five passes, five artifacts, the last CLEAN

Model `gpt-5.6-terra`, pinned, via `~/.claude/bin/codex-review.ps1`. Every CRITICAL/HIGH was fixed RED-first and re-reviewed; the re-review kept finding new defects in the recovery code each fix added, until the fifth pass.

| Pass | Artifact | Reviewed | Tally C/H/M/L | Fix (RED -> green) |
|---|---|---|---|---|
| 1 | `2026-09-19-codex-wave3-dispatch-split.md` | `f09c7ac8` | 1/1/0/0 | `1a64ce57` -> `12977bdb` |
| 2 | `...-rereview.md` | `10868a8e` | 2/0/0/0 | `5bc9c3f9` -> `e60712d2` |
| 3 | `...-rereview-2.md` | `236295b6` | 2/0/0/0 | `84008b9d` -> `c5808275` |
| 4 | `...-rereview-3.md` | `242b7061` | 2/0/0/0 | `7aa37b0a` -> `1f742353` |
| 5 | `...-rereview-4.md` | `ea2724bb` | **0/0/0/0** | -- |

**Range caveat, recorded in artifact 1:** pass 1 was given `main..HEAD` (two-dot), which also carried the wave-2 lanes main has and this branch (based on `c00f9c10`) does not, so its file list included unrelated files. Its two findings were in this lane's own files. Passes 2-5 used `main...HEAD`. Every artifact carries the author's disposition; pass 1's HIGH was accepted only in part (the lane had already ended, so there was nothing to stop -- the defect was the exit code, reclassified 4 -> 5).

The findings, in one line each: the shim left a launch with an unreadable id uncapped (found by worktree now); exit 4 must mean only "may still be running"; a mis-parsed 8-hex id could stop ANOTHER lane (worktree must match the slug); a transcript-read exception escaped the governor (any governor failure now stops the lane); recovery could stop an unverified id and could itself escape (only a `verified` id, `_safe_stop`, `_recover`); a stale `done` record could be bound (must be live); a governor that failed to even run left the shim exiting arbitrarily (`stop --slug` verb, shim exits 5 or 4).

## 5. For the operator -- the exact win-tooling replacement (that repo was NOT edited)

1. **Copy** `.dev-knowledge/templates/dispatch-shim.ps1` **over** `win-tooling/scripts/dev-terminals/bin/dispatch.ps1` (the PATH command). Leave `dispatch.cmd` beside it unchanged. If win-tooling deploys its `bin\` to another location, re-run that deploy step so the deployed copy matches (not verified by this lane).
2. **Needs** `uv` on PATH and the hub checked out at `$HOME\Documents\Dev\.dev-knowledge` (or pass `-Hub <path>`); `pwsh` 7+.
3. **The command changes:** `dispatch LANE-x.md -TokenCap 400000` -- **`-TokenCap` is mandatory**. Model and effort come from the contract's `| Model | Mode | Effort |` table (`-Model` / `-Effort` override); there is no default. Run it from the TARGET repo root: the lane's worktree is created in the repo you stand in.
4. **What the operator loses versus the old `dispatch.ps1` -> `Invoke-Dispatch.ps1`:** the `[y/N]` confirm and `-Run` (the shim runs immediately; `-DryRun` prints the plan and starts nothing); the contract's `## Dispatch` block is no longer read or run (argv is built by the hub's `plan`); codex / `claude -p` / codespace lanes are refused by the shim (section 2). The cloud (Anthropic-hosted) substrate was never in dispatch.py and stays in win-tooling's `DispatchHelpers.psm1`.
5. Win-tooling's `dispatch.ps1` docstring and its `Invoke-Dispatch.ps1` are then stale; `DispatchHelpers.psm1` still serves the cloud substrate.

## 6. Open items (not done here -- outside the footprint)

- **PLAYBOOK Ch8 now describes the old surface.** `protocols/PLAYBOOK.md` lines ~98 (TOC), 2217-2220, 2818-2832, 2851, 2896, 3267 and the section "The dispatch surface is `dispatch <file>` -- the contract file is the source ([#509] v2)" (~3326-3408) say `Invoke-Dispatch.ps1` reads the contract's `## Dispatch` block, resolves `$env:CLAUDE_PROMPTS_DIR`, asks `[y/N]`, and that `-Run` is reachable via `Invoke-Dispatch.ps1`. After the shim lands: the surface takes `-TokenCap`, reads model/effort from the table, never reads `## Dispatch`, and the confirm is gone. Lane contracts that carry a `## Dispatch` block have its `claude ...` line ignored by the new verb; whether the generator should keep emitting it is the integrator's decision.
- **BUILD-LIST carrier table:** the `worktree-wave2-dispatch` carrier row is to close "when the caller-side shim lands"; this lane is that shim's source.
- **JOURNAL:** this lane wrote none (P-1, and the operator's ruling above). L3's inherited entries `(ae)` and `(x)` ride along untouched; the integrator resolves and re-letters at merge. This branch is based on `c00f9c10`, which predates main's wave-2 merges, so the merge conflicts in `JOURNAL.md` only.
- **A stream-metered spawner** (section 2) if codex / DeepSeek / Moonshot lanes are wanted through `dispatch` again; the `meter_lines` primitive is ready.
- **The `'m' is not recognized` line** in every real launch (section 2).
- `MEMORY` candidates for the integrator (not written by this lane): a finished `--bg` lane stays in `claude agents --json` with `state: done` and its process keeps its worktree directory locked until `claude stop`; `git worktree remove` then fails `Permission denied`.

no-consumer: lane output awaiting integrator merge (wave 3, L3 split); it files and closes no BACKLOG row, so no [#id] cites it yet.
