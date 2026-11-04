# Design: the seat lifecycle -- a seat is a role with one workspace, state lives at the primary (/decide, run seat-lifecycle)

- **Run date:** 2026-11-04
- **Producer:** claude-opus-5-5 (dispatcher seat orchestrator-e3-0-cycle-5, job b0649864). Research subagents were claude-sonnet-5-5: three of them, read-only, run in parallel.
- **Row:** `[#1869]` (`tasks/1869-seat-lifecycle-role-workspace-state-home-ref-registry.md`), parent `[#1868]` C0 part (a)
- **Input:** three transport files, read in full:
  - PROPOSAL-ADR-SEAT-LIFECYCLE-2026-11-04.md (sections 1-7)
  - DIGEST-RESEARCH-SEAT-WORKTREES-2026-11-04.md (sections 1-4)
  - AUDIT-SEAT-WORKTREE-CONSEQUENCES-2026-11-04.md (A1-A7 and its 19:3x CORRECTION)
  
  The operator order is DIGEST-PLAN-SEAT-LIFECYCLE-FIX-AND-CLOSE-2026-11-04.md, steps P0 and P1, under the operator GO of 2026-11-04 evening.
- **Output:** `docs/decisions/ADR-140-a-seat-is-a-role-with-one-workspace-and-its-state-lives-at-the-primary.md` at status Proposed. Nothing is built, removed or migrated by this run.

## Brief

Question: how should the harness (a) give an orchestrator or integrator seat its checkout so that a seat rotation (cycle N -> N+1) leaves nothing behind, (b) keep per-session state (launch receipts, `logs/<month>`) so that no checkout holds state that exists nowhere else, (c) make every git ref the harness creates carry a declared owner and exit, and (d) check A1-A7 of the consequence audit permanently?

Known constraints (no answer pre-committed):
- Scope is fixed by the plan's P2: I1-I4, the audit as a script, and a move-only migration. New scope becomes a row, not this lane.
- No hand cleanup. Today's state is cleaned by the mechanism's own first run (P4).
- The 2026-10-17 rule stands: no handoff on stray refs; automation/fleet-audit is protected.
- Library-first. The candidates are `git worktree add --detach`, `git rev-parse --git-common-dir`, `git worktree lock/prune`, and the existing `land_on_handback._primary`.

Sub-questions fanned out:
- Q1: worktree creation and launch paths.
- Q2: the state home.
- Q3: the ref registry, git_hygiene and batch close.

## Subagent briefs

Each brief is copied verbatim from the file the subagent was sent (C:/Users/1028120/.claude/jobs/b0649864/tmp/briefs-seat/brief-N.md). `decide_checks subagent-exclusions` over the three files found 0 defects.

### Brief 1

```text
CONTEXT: a design decision on the .dev-knowledge harness SEAT lifecycle (orchestrator/integrator seats rotate cycle N -> N+1 via scripts/seat_cycle.py). Nothing is being built.
SUB-QUESTION 1 (worktree creation and launch paths): (a) every code path that creates a git worktree or a branch for a seat or a lane: scripts/seat_cycle.py (cycle, launch_successor, the repo_root default near :624), scripts/dispatch.py (successor_lane near :2491, the lane/queue launch paths, any 'worktree add'), scripts/merge_path.py (integration worktree 'integrate-<batch>' creation and removal), and any other 'worktree", "add' / 'git worktree' call under scripts/ (grep). For each: file:line, how the location is computed (cwd? HUB_ROOT? git rev-parse?), branch name form, detached or not. (b) every code path that REMOVES a worktree or branch (teardown, K1, batch close, prune): file:line and what triggers it. (c) does any code use 'git rev-parse --git-common-dir' or '--show-toplevel' to find the primary? (d) how is a queued lane's session cwd chosen (the claude --bg launch cwd) - quote the line. (e) which existing tests cover seat_cycle successor launch and dispatch successor_lane (tests/ file::function).
EXCLUSION (R15): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository; do not run git add/commit/push, pytest, or any writer; no git worktree add/remove/prune. Work in C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/worktrees/orchestrator-e3-0-cycle-5 (HEAD = origin/main 33005b8c2). Every claim you return MUST carry a file:line you opened, or the exact command + output excerpt; mark anything you could not verify UNVERIFIED. Return a compact bullet list (<= 60 bullets), no prose essay.
```

### Brief 2

```text
CONTEXT: a design decision on where the .dev-knowledge harness keeps per-session STATE (receipts, logs/<month>) so any worktree is disposable. Nothing is being built.
SUB-QUESTION 2 (state home): (a) scripts/dispatch.py receipts_dir() (near :870) and HUB_ROOT (near :142): quote them; list every other module that computes a receipts dir or a logs dir (grep 'logs/receipts', 'receipts_dir', 'HARNESS_RECEIPTS_DIR', '"logs"', 'logs_dir', LOGS_DIR) with file:line and how it anchors (module __file__, cwd, env var). (b) scripts/subst_gate.py launch_receipt_problems (refusal near :497): what path it reads and whether HARNESS_RECEIPTS_DIR redirects reads and writes alike. (c) which hooks in .claude/settings.json write under logs/ (SessionStart, Stop: propose_closures PROPOSALS-*, fleet_health, SESSION-START-FULL.txt) and how they anchor the path. (d) .gitignore lines for logs/ and logs/receipts. (e) existing tests that pin receipts_dir or HARNESS_RECEIPTS_DIR (tests/ file::function). (f) is there any existing notion of a shared state dir anchored at the primary (git-common-dir, a ~/.claude path, CLAUDE_PROMPTS_DIR)?
EXCLUSION (R15): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository; do not run git add/commit/push, pytest, or any writer; no git worktree add/remove/prune. Work in C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/worktrees/orchestrator-e3-0-cycle-5 (HEAD = origin/main 33005b8c2). Every claim you return MUST carry a file:line you opened, or the exact command + output excerpt; mark anything you could not verify UNVERIFIED. Return a compact bullet list (<= 60 bullets), no prose essay.
```

### Brief 3

```text
CONTEXT: a design decision making every git ref the .dev-knowledge harness may create carry a declared owner and exit (a registry as data), and a permanent audit of worktrees. Nothing is being built.
SUB-QUESTION 3 (ref registry, git_hygiene, batch close): (a) the handoff preflight row git_hygiene: find it (grep -rn git_hygiene scripts/), quote how it decides 'stray' and whether it reads any allowlist / protected list (automation/fleet-audit); file:line. (b) scripts/validate_branch_naming.py: the prefix enum and where it is enforced (hook? test?). (c) any existing registry/yaml of ref owners, protected branches or seat roles (grep ecosystem/ for 'fleet-audit', 'protected', 'seat', 'role'); ecosystem/seat-cycle.yaml content summary. (d) what 'batch close' means in code: any script/verb that closes a batch (grep 'batch close', 'close_batch', 'tag', 'annotated tag' in scripts/ incl. ADR-135's batch tag), file:line. (e) gen_handoff.py preflight rows list (names + file:line) and how a new row is registered. (f) existing tests for git_hygiene (tests/ file::function).
EXCLUSION (R15): never read, list, write or delete any path containing the folder name "OneDrive - Blue Yonder". If a search would touch it, skip it and say so. You are read-only: change no file in this repository; do not run git add/commit/push, pytest, or any writer; no git worktree add/remove/prune. Work in C:/Users/1028120/Documents/Dev/.dev-knowledge/.claude/worktrees/orchestrator-e3-0-cycle-5 (HEAD = origin/main 33005b8c2). Every claim you return MUST carry a file:line you opened, or the exact command + output excerpt; mark anything you could not verify UNVERIFIED. Return a compact bullet list (<= 60 bullets), no prose essay.
```

## Subagent claims

Every claim the matrix, the pre-mortem or the ADR relies on is listed here. The producer opened each `path:line` probe on HEAD 33005b8c2, and `decide_checks subagent-claims` re-runs every probe.

- the seat-cycle repo root defaults to the process cwd {probe: scripts/seat_cycle.py:624}
- dispatch's default root is the checkout holding the running script, not the primary {probe: scripts/dispatch.py:142}
- the successor worktree is cut under repo_root/.claude/worktrees/<slug> {probe: scripts/dispatch.py:2513}
- the successor gets a branch named worktree-<slug> {probe: scripts/dispatch.py:2514}
- the plain launch path takes cwd from the caller or Path.cwd() {probe: scripts/dispatch.py:1453}
- receipts_dir is HARNESS_RECEIPTS_DIR or HUB_ROOT/logs/receipts, per checkout {probe: scripts/dispatch.py:870}
- the launch-receipt gate reads root/logs/receipts unless a dir is passed {probe: scripts/subst_gate.py:469}
- land_on_handback already resolves the primary from git-common-dir {probe: scripts/land_on_handback.py:148}
- handback.py resolves the primary root the same way {probe: scripts/handback.py:423}
- worktree_seed already returns (root, primary) from git-common-dir {probe: scripts/worktree_seed.py:213}
- propose_closures anchors its logs dir on its own file, not the primary {probe: scripts/propose_closures.py:47}
- the integration worktree is created by a runbook step, not by code {probe: .claude/commands/lane-integrate.md:167}
- the git_hygiene row is a hand-written function in gen_handoff {probe: scripts/gen_handoff.py:2087}
- git_hygiene reads an allow-list file that is data {probe: grep -c 'automation/fleet-audit' ecosystem/git-hygiene-allowlist.yaml}
- the preflight roster is data, and git_hygiene is a blocking cut row {probe: grep -c 'git_hygiene' ecosystem/handoff-preflight-rows.yaml}
- batch close is a harness moment with organs, not a verb {probe: grep -c 'batch-close' ecosystem/harness.yaml}
- the lane-boot command already forbids raw sibling worktree names {probe: .claude/commands/lane-boot.md:126}
- the claude-made worktree location for a --worktree lane is decided by Claude Code, not hub code {unverified}
- no code removes a seat's worktree after a cycle (a reading of seat_cycle.cycle, which ends at stop and verify) {probe: scripts/seat_cycle.py:424}

## Evidence and matrix

What exists, from the probes above and the audit:
- **Location is relative to where the caller stands.**
  - Seat launch uses the cwd (seat_cycle :624).
  - Lane and queue launch use HUB_ROOT or the cwd (dispatch :142, :1453).
  - Three modules already anchor on the primary through git-common-dir: land_on_handback, handback and worktree_seed. That is the library answer, already in production in this repo.
- **State is per checkout.**
  - About 15 modules recompute `<file root>/logs/receipts`.
  - Month-bucket writers such as propose_closures have no override at all.
  - The audit measured the result:
    - 549 unique `logs/2026-11` files, 7 unique receipts and 22 differing copies across 6 worktrees (A3);
    - 4 hand copies of LAUNCH receipts in one batch (A7);
    - a lane whose session cwd was a stopped seat's checkout, writing 13 files there after the seat stopped (A5).
- **Exits.**
  - A lane branch exits at landing (K1).
  - The integration worktree exits by a runbook step.
  - A seat worktree and branch have no exit in code.
  - The one ref registry that exists is `ecosystem/git-hygiene-allowlist.yaml`. It holds branches only, with no exit or kind, and git_hygiene reads it.

Options:
- **O0, status quo.**
- **A, a teardown step in cycle().** After the stop: harvest, then remove the predecessor's worktree and branch, and guard repo_root.
- **B, a role-bound workspace.**
  - Each role gets one workspace per batch, detached with no branch, reused by every cycle.
  - The state home is anchored at the primary.
  - Refs go in a registry with exits.
  - Retirement happens only at batch close.
- **C, seats with no worktree.** Seats run in the primary checkout.
- **A2, A plus the state home.** Teardown per cycle, with no harvest needed.

Criteria:
- **lose_nothing:** no state exists only in a disposable checkout, and no removal can lose work.
- **root_cause:** the option removes RC1-RC4 at the source rather than repairing their effects.
- **hand_steps:** the landings, rotations and closes in a batch need no hand step.
- **footprint:** new organs, files and gates.
- **modifiability:** how much a later change (sibling location, more roles) costs.

Scores run from 1 to 5. A score of 4 or 5 needs a footnote measured on this repo this session; otherwise the cap is 3.

Weights: lose_nothing=25 root_cause=25 hand_steps=20 footprint=15 modifiability=15

| Option | lose_nothing | root_cause | hand_steps | footprint | modifiability | Σ |
|---|---|---|---|---|---|---|
| O0 status quo | 1 | 1 | 1 | 4[^1] | 3 | 1.75 |
| A teardown in cycle() | 2 | 2 | 2 | 3 | 2 | 2.15 |
| A2 teardown plus state home | 3 | 2 | 3 | 2 | 2 | 2.45 |
| B role workspace, state home, ref registry | 3 | 4[^2] | 3 | 3 | 3 | 3.25 |
| C seats in the primary | 3 | 3 | 3 | 3 | 2 | 2.85 |

[^1]: measured -- O0 adds nothing by construction: `git status` of this worktree was clean at the start of the run, and the run changes no script, so O0's footprint is zero new organs or gates.
[^2]: measured -- the anchor B needs already runs in production in this repo: `scripts/land_on_handback.py:148` and `scripts/handback.py:423` resolve the primary from `git rev-parse --git-common-dir`. Every RC1-RC4 instance the audit found traces to a cwd or file-relative anchor: A4 nesting to `scripts/seat_cycle.py:624`, A5/A7 to `scripts/dispatch.py:142` and `:870`. The anchor removes that class.

Reading the matrix:
- **B leads C by 0.40.**
  - C's only edge is that it creates nothing. It binds every seat to the operator's checkout, which sat behind origin/main all day: the audit's A6 ledger names ac13bf33d as main.
  - It also leaves two seats sharing one checkout. That is what the one-checkout-one-committing-session rule (AGENTS.md, "Landing a change") forbids.
- **A and A2 keep a create/destroy pair on every cycle.**
  - A also keeps the harvest as a recurring hand-shaped step. A2 removes the harvest but keeps per-cycle refs, so every rotation is a git write that can fail mid-handover.
  - In the research digest's terms (section 2), the binding of a branch to a session is the mistake, not the cycle.
- **O0's footprint advantage is real and does not survive lose_nothing.**
- **Library-first check:**
  - `git worktree add --detach` gives a branchless workspace.
  - `git rev-parse --path-format=absolute --git-common-dir` gives the anchor, already wrapped by `land_on_handback._primary`, and the build reuses that wrapper.
  - `git worktree lock --reason` and `git worktree prune` give the startup prune.
  - The PID liveness test is `psutil.pid_exists` if psutil is already locked, otherwise `os.kill(pid, 0)` on POSIX and `OpenProcess` via ctypes on Windows; the lane checks uv.lock first.
  - Nothing is hand-rolled that git already does. No new dependency is admitted by this ADR.

## Pre-mortem

Assume ADR-140 was built as B and failed six months later. The likely causes, and what the design carries against each:
1. **Two seats of one role run in one workspace at the same time** (the handover overlap: the successor binds before the predecessor stops).
   - Against: neither seat mutates git in the role workspace (detached, no branch, read-only by contract and by a check). Concurrent reads of one tree are safe.
   - The only shared writes are ignored files, and those move to the home (I2).
2. **The state home becomes a new single point of loss** (the primary checkout is deleted or re-cloned).
   - Against: the home holds exactly what the primary-run sessions hold today, so the loss surface does not grow.
   - Retention stays logs_retention's job. A re-clone loses ignored state today too.
3. **A seat must commit**, as this /decide run does.
   - Against: a seat commit goes in a lane worktree, or in integrate-<batch> for the integrator. The role workspace refuses a commit through a pre-commit check on a detached HEAD in a registered role path. This run's own commit, on a docs/ branch in a seat worktree, is the last of the old form.
4. **The registry drifts from git.**
   - Against: git_hygiene and the audit read the registry and git together, and any ref git has that the registry does not admit is stray. The registry is never a list of what exists, only of what may exist and when it must go.
5. **The migration overwrites or loses a file.**
   - Against: it compares sha256 and never overwrites. A same-name file with a different hash is kept side by side under `logs/migrated/<worktree>/`.
   - The source is removed only by the retire step, after the audit shows A3 CLEAN for that worktree.
   - Running it twice moves nothing the second time (tested).
6. **Retirement removes a live seat's checkout** (today's A4 nesting).
   - Against: retire refuses any worktree that another registered worktree is nested inside, or whose owner session is live. Liveness is checked by `session_live` (job record plus process); `worktree_owners` is not used for this (SOL7). Retire runs only from the primary, and the live seat moves to its role workspace first.
7. **Claude Code's own `--worktree` lanes keep landing where Claude Code puts them** (unverified in hub code).
   - Against: the lane launch passes the primary as cwd (I1), so Claude Code's `.claude/worktrees/<slug>` resolves under the primary. The audit's A4 leg catches any other location on the next run.
8. **The lane grows** (about 25 modules recompute a logs path).
   - Against: scope is receipts and `logs/<month>`, through one resolver. The top-level `logs/*` caches (FLEET-HEALTH.md, SESSION-START-FULL.txt, OPERATOR-LOAD.csv) are rebuildable and stay per checkout, with that reason recorded. Any other module becomes a row.

## Evaluator findings and responses

Evaluator records (header lines copied verbatim from each file). The files are kept in the dispatcher job dir, `C:/Users/1028120/.claude/jobs/b0649864/tmp/eval/`.

EVAL-sol.md: served-model: gpt-6.1-sol / attestation-source: copilot usage file currentModel (eval/sol-usage.json, which reads "currentModel": "gpt-6.1-sol") / nonce 2d40ae30 (matches the brief) / VERDICT: DISAGREE -- Same-cwd launch is supported, but safe overlap, retirement, shared-state concurrency, registry enforcement and acceptance remain underspecified or contradictory.

EVAL-argon.md: served-model: gemini-4-argon / attestation-source: copilot usage file currentModel (eval/argon-usage.json, which reads "currentModel": "gemini-4-argon") / nonce 2847ddc2 (matches the brief) / VERDICT: DISAGREE -- D1 breaks seat_cycle stop-verification and occupancy checks, I2 omits dodo.py/handback.py receipt writers/readers, and D3/D4/D5 deadlock on unmigrated caches and out-of-scope audit findings. Format note: argon wrote `- ARGON1 [HIGH] ...`. For the parser, the producer normalized those lines to `- id: ARGON1 -- [HIGH] ...` in EVAL-argon-norm.md and changed no other byte.

Before answering, the producer checked each finding against the cited file and line. The decisive checks held:
- `scripts/seat_cycle.py:298` matches `[job_id, worktree]`;
- `scripts/dispatch.py:2525-2532` refuses a detached tree;
- `scripts/worktree_occupancy.py:55` admits no dot in `_SLUG_RE`;
- `scripts/dodo.py:85-86` anchors on `_ROOT`;
- `scripts/propose_closures.py:461-473` checks for the file, then writes.

Every finding is Accepted. The ADR is revised as r2.

| id | objection (short) | response |
|---|---|---|
| SOL1 | refreshing the shared workspace during the overlap can drop a detached commit or race a landing | **Accepted** -- D1: the integrator's role workspace is separate from `integrate-<batch>`. No seat commits, checks out or resets in a role workspace. HEAD moves only in `rotate`, after the verified stop, and only on a clean tree whose HEAD is an ancestor of origin/main |
| SOL2 | the shared home makes the PROPOSALS name allocation racy | **Accepted** -- D2 I2: every name allocated in the home uses exclusive create (`open(..., "x")`) with a retry. T5 runs two writers concurrently |
| SOL3 | batch-close retire would remove the integrator's own running checkout | **Accepted** -- D0: batch close only tags. `retire` runs from the PRIMARY, at the cut or at the next `open_batch`, after both role seats are stopped and verified. T11 refuses retire's own cwd |
| SOL4 | dodo.py receipts are missing from I2 | **Accepted** -- D2 I2: the census test T15 now enforces the caller set. dodo, gates, test_pairing and handback are named in the known set |
| SOL5 | Claude/Codex `--worktree` launches bypass the two guarded add sites | **Accepted** -- D2 I3: registry admission of the intended slug runs before ANY provider spawn, including `scripts/dispatch.py:636` and `:678-679`. T7 covers the launch refusal |
| SOL6 | kinds without an exit-event source, plus the current-branch exemption, cannot implement the post-exit stray rule | **Accepted** -- D2 I3: each kind binds an instance key and an exit that git can observe. A lane's exit is a tip that is an ancestor of origin/main. An integration or role workspace's exit is `refs/tags/batch/<batch>` (ADR-135 D4). The running-checkout exemption is kept for the primary only. T8 tests the same instance before and after its exit |
| SOL7 | worktree_owners is not a liveness check | **Accepted** -- D2: `session_live(job_id)` reads the job record and the process list, and fails closed. worktree_owners is not used for retire or occupancy |
| SOL8 | a conflicting LAUNCH receipt moved aside can make landing refuse or choose the wrong gate | **Accepted** -- D4: a LAUNCH conflict resolves to the latest launch for that slug and batch, and the losing copy is kept in `logs/migrated/`. T16 lands from the migrated home and checks the gate selection |
| SOL9 | an all-CLEAN acceptance is impossible while history legs and out-of-scope items exist | **Accepted** -- D3: only the current-state legs block (A1, A2 in linked worktrees, A3, A4). History legs and out-of-scope items are reported against a baseline file. Acceptance is "no blocking item" |
| SOL10 | in-place rotation breaks stop verification through the shared-path needle | **Accepted** -- D1: in a role workspace, `verify_stop` matches only the predecessor's job id and session id. T6b runs it with a live successor |
| SOL11 | some tests cannot be RED, and a fake spawn cannot witness a real overlap | **Accepted** -- D5: T7's protected clause is labelled a regression guard. T8 is re-cut as before/after on one instance, which is RED today. P4's first real rotation is named as the live overlap witness that decides the flip-condition |
| ARGON1 | verify_stop always fails with a live successor in the same workspace | **Accepted** -- same answer as SOL10 (D1, T6b) |
| ARGON2 | successor_lane needs a branch and refuses detached trees; occupancy rejects dotted names and live sessions | **Accepted** -- D1: rotation gets its own launch path, `seat_cycle.rotate`, instead of `successor_lane`. The batch token replaces `.` with `-` (`e3-0`), which passes `_SLUG_RE`. Role-workspace occupancy admits the named predecessor |
| ARGON3 | integrate-<batch> cannot be both branchless and the branch-carrying landing workspace | **Accepted** -- D1: the integrator's role workspace is `integrator-<batch-token>`, detached. `integrate-<batch>` stays the landing workspace (kind integration) |
| ARGON4 | the dodo, gates, test_pairing and handback receipt paths are omitted | **Accepted** -- same answer as SOL4 (census test T15) |
| ARGON5 | the blocking audit cannot pass because of history and out-of-scope items | **Accepted** -- same answer as SOL9 (D3 blocking predicate plus baseline) |
| ARGON6 | rebuildable caches flagged LOST-RISK deadlock retire | **Accepted** -- D2 I2 and D3: a named rebuildable list in the registry makes these caches CLEAN for A3, and they are not copied |
| ARGON7 | git_hygiene at batch close fails while seats still occupy their role workspaces, and there is no exit predicate | **Accepted** -- D0 and I3: the exit is the batch tag, which git can observe. Retire and the stray judgement run after the seats stop, from the primary |
| ARGON8 | migration unlinks from live worktrees, and LAUNCH conflicts and jsonl collisions are unresolved | **Accepted** -- D4: migrate copies and never unlinks; retire unlinks after a verified stop. A LAUNCH conflict resolves to the latest launch, with the losing copy kept. A jsonl is merged as a line union |
| ARGON9 | T8 and T7's protected clause already pass on origin/main | **Accepted** -- same answer as SOL11 (T8 re-cut, T7's clause labelled a regression guard) |
| ARGON10 | the pre-commit role-workspace refusal is untested and the role token is open | **Accepted** -- D1: the role enum is closed (orchestrator, integrator) in the registry. T14 tests the pre-commit refusal |
