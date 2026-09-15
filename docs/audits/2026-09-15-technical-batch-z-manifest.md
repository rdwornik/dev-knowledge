# Batch Z manifest — the night of 2026-09-15

> **Dispatcher seat.** Carrier for `DECLARE-NIGHT-PLAN-2026-09-15-FINAL.md`,
> `AMEND-NIGHT-PLAN-001.md` and `AMEND-NIGHT-PLAN-002.md` (all three name this file in their
> `carried-by:` line, and `seat_refusals carried-by` passes 3 of 3).
>
> **What this file is.** The batch record: what was frozen, what fired, what was DEFERRED and
> why, and the substrate evidence that forced the re-cut. It is immutable once landed —
> supersede with a new file or an in-file amendment marker.

## 1 · The headline: the batch was re-cut from sixteen lanes to six, and the reason is evidence, not preference

Two independent facts forced it, both established before the first worktree existed.

**(a) The ceiling organ refused sixteen.** `seat_refusals lane-ceiling --check-worktrees` is a
STEP-0 REFUSAL, not a warning printed afterwards:

```
REFUSED [lane-ceiling]: the plan names 16 lanes against a ceiling of 6; the excess is
lane-z-6-charts, lane-z-7-backlog-bar, lane-z-8-protocols-heading, lane-z-9-architecture,
lane-z-10-aj-m04, lane-z-11-three-repo, lane-z-12-distiller, lane-z-13-path-registry,
lane-z-14-management-map, lane-z-15-actions-lane -- hand the excess back to the plan
```

**(b) The CODESPACE substrate is DEAD, and was dead before tonight.** The plan routes eight
lanes there. A Codespace cannot run any of them. This is measured, not inferred — §3.

The re-cut is six lanes, which the ceiling passes. The excess is handed **back to the plan** as
the next batch's opening rows (§5), never forward to a queue.

## 2 · The six that fired

| # | Lane | Substrate | Ordered model | Ran model | Receipt |
|---|---|---|---|---|---|
| 0 | `lane-z-0-quality-requirements` | LOCAL | opus | opus | bg `54637863`, branch `worktree-lane-z-0-quality-requirements` |
| — | `lane-z-746-devcontainer-substrate` | LOCAL | opus | opus | bg `b6e34a84`, branch `worktree-lane-z-746-devcontainer-substrate` |
| 4 | `lane-z-4-non-claude-execution` | LOCAL | opus | opus | bg `a07a1f47`, branch `worktree-lane-z-4-non-claude-execution` |
| 10 | `lane-z-10-aj-m04-first-pass` | LOCAL | opus | opus | bg `b69df795`, branch `worktree-lane-z-10-aj-m04-first-pass` |
| 11 | `lane-z-11-three-repo-comparison` | CC CLOUD | opus | claude-opus-5 | `session_01B9HcopUNegngr37k9QDQ6U`, G1/G2/G3 OK, receipt at 51s |
| 14 | `lane-z-14-management-map` | CC CLOUD | opus | claude-opus-5 | `session_011HDnnyPdvSh7HvqytYrRUR`, G1/G2/G3 OK, receipt at 41s |

`lane-z-746-devcontainer-substrate` is **not** in the fifteen. It was promoted into the batch
because it is the unlock for the eight deferred Codespace lanes — see §3. It carries row
`[#746]`, already filed at P2.

Every lane's contract instructs its **first commit to file or amend its own row**. Both cloud
lanes echoed the brief back intact (80 lines, correct final line, not truncated) before working.

## 3 · Why CODESPACE is dead — the measurement, in order

A fresh `gh codespace create -R rdwornik/dev-knowledge -b main` was run tonight. It came up
`Available` and carried **no `claude`, no `node`, no `npm`, no `uv`, no `gh`** — only
`/usr/bin/python3`. The reason is in its own creation log:

```
[provision] L2 OK — full history (6206 commits reachable from HEAD)
[provision] L1 OK — uv 0.11.19 == pin 0.11.19
[provision] environment OK — Python 3.12.10 (.python-version), deps from uv.lock via --locked
/workspaces/dev-knowledge/.venv/bin/python3: can't open file
    '/workspaces/dev-knowledge/scripts/cloud_provisioning.py': [Errno 2] No such file or directory
/workspaces/dev-knowledge/.venv/bin/python3: can't open file
    '/workspaces/dev-knowledge/scripts/cloud_provisioning.py': [Errno 2] No such file or directory
[provision] REFUSED: B1 the history guard could not look (exit 2) — an unknown history state is not a clean one
postCreateCommand from devcontainer.json failed with exit code 1.
Error: Command failed: /bin/sh -c bash .devcontainer/provision.sh
Container creation failed.
Creating recovery container.
```

Three things this establishes, each worth stating separately:

1. **Everything else provisions correctly.** Full history, `uv` at an EXACT pin match, the right
   interpreter, locked deps. The substrate is one file away from working.
2. **`scripts/cloud_provisioning.py` was retired** by commit `3c9418cc`
   (*feat(x-734): retire six census orphans*). `provision.sh`'s own comments at lines 368 and
   580 claim both call sites were REMOVED at `[#664]` on 2026-09-13. **Two call sites survive**
   and still invoke the deleted file. The removal was incomplete and nothing caught it.
3. **The failure is SILENT by design of the platform.** Codespaces does not surface a failed
   build — it substitutes a bare `mcr.microsoft.com/devcontainers/base:alpine` **recovery
   container** and reports `Available`. A lane dispatched there does not fail loudly; it runs
   in a box where every gate is *vacuous rather than absent*. That is the dangerous shape.

`provision.sh` is behaving **correctly**: it refuses fail-closed on an unknown history state.
The fix is to restore the leg, never to weaken the guard.

The older codespace (`suite-baseline-2026-09-08`) is a different state again: properly
provisioned with `uv 0.11.19`, but still **no `claude`** — the 2026-08-25 failure the
`Dispatch-Codespace` module already encodes as exit code 91,
`{"error":"claude is not installed in this devcontainer"}`.

**Conclusion:** `[#746]` is not a P2. It is the blocker for eight of tonight's sixteen lanes,
and it was promoted into this batch as a lane of its own.

## 4 · The evidence answers the two questions that were asked with evidence

**Q (AN1-7): can the provider CLIs authenticate inside a Codespace? If Copilot Enterprise can,
lane 4 moves there and LOCAL drops to one lane.**

**A: No — not tonight, and the blocker is not authentication.** `GITHUB_TOKEN` *is* present in
the container, so a GitHub-native CLI would have something to authenticate with. But `copilot`,
`codex` and `gemini` are all **npm packages**, and the container has **no `node` and no `npm`** —
there is nothing to install them with, before any question of entitlement arises. Lane 4 stays
LOCAL. LOCAL therefore carries **two** of the fifteen (lanes 4 and 10), exactly as AN1-1 ruled,
plus the two lanes added by this batch's own re-cut.

The question becomes answerable the moment `[#746]` lands, because the devcontainer's Claude
Code feature installs `node` as a side effect. It is re-asked then, not guessed now.

**Q: can Actions run a lane end to end (lane 15)?**

**A: No, and here is exactly what blocks it** — reported rather than substituted with something
easier, per the operator's instruction. Three blockers, all verified tonight:

1. **No credential.** `gh secret list -R rdwornik/dev-knowledge` returns **empty**, for both
   `actions` and `codespaces` scopes. There is no `ANTHROPIC_API_KEY` and no Claude Code OAuth
   token in the repository. A workflow cannot start an agent it cannot authenticate.
2. **No write permission.** `conductor.yml` declares `permissions: contents: read`, and its own
   header states the boundary in terms: *"This workflow EVALUATES and REPORTS; it moves no
   row."* A lane commits and hands back a branch; this workflow is constitutionally unable to.
3. **No lane runner exists.** The two workflows present (`conductor.yml`, `report-only-wall.yml`)
   run the **suite** — `pytest`, `ruff`, `seal`. Neither dispatches an agent. Lane 15's premise,
   *"today Actions are proven for the SUITE only; nobody has run a lane there"*, is confirmed
   exactly as written.

Blocker 1 is the real one, and it is **not a technical decision** — putting an Anthropic
credential into GitHub Actions secrets is an outward-facing act with a blast radius, and it is
the operator's call, not the dispatcher's. It is carried to him as the batch's single ask
(§6), unmade.

## 5 · DEFERRED — every X1/X2/X3 item not in this batch, with its reason

| # | Lane | Planned substrate | Deferred because |
|---|---|---|---|
| 1 | Cost telemetry WIRED | CODESPACE (AN1-1) | substrate dead (§3). No local dependency, so it must NOT be re-routed LOCAL by habit — that is the exact error AN1-1 corrected. Next batch, on a repaired Codespace. |
| 2 | Decision engine WITNESSED | CODESPACE (AN1-1) | substrate dead (§3); same reasoning as lane 1. |
| 3 | Spine `[#664]` WITNESSED | CODESPACE (AN1-1) | substrate dead (§3); same reasoning as lane 1. |
| 5 | Log-review routine | CODESPACE | substrate dead (§3). Also gated on lane 1. **This is the lane that closes AN2-3's self-healing loop** — until it lands, the dispatcher reports register breaches in its receipt, which is what §7 does. |
| 6 | Charts | CODESPACE | substrate dead (§3); gated on lane 1. |
| 7 | BACKLOG to bar + one row format | CODESPACE | substrate dead (§3). |
| 8 | One `protocols/` heading | CODESPACE | substrate dead (§3). |
| 9 | ARCHITECTURE to target | CODESPACE | substrate dead (§3); also gated on `[#755]`'s 11-chapter measurement. |
| 12 | Prompt distiller `[#617]` | CODESPACE | substrate dead (§3). |
| 13 | Path registry `[#715]` | CODESPACE | substrate dead (§3). |
| 15 | **Actions runs a LANE** | ACTIONS | blocked on three things, not deferred by preference — §4. Needs an operator decision on a credential before it is even a lane. |

Eleven deferred, six fired, one promoted. The eight `substrate dead` rows have **one shared
unblock**, `[#746]`, which is in this batch.

## 6 · The single ask carried to the operator

**Does an Anthropic credential go into this repository's GitHub Actions secrets?**

It is the only thing standing between lane 15 and a dispatch, and it unblocks every future
night from being bounded by this workstation's memory. It is an ask-class **(c)** item — a fork
class with no standing ruling — and it is outward-facing, so the dispatcher does not make it.
Nothing else in this batch waits on an answer.

## 7 · Register breaches reported in this batch (AN2-3, until lane 5 lands)

- **Performance / AN1-3 is half wrong, and the correction matters.** AN1-3 names graph-rebuild
  and audit-health together as "the heaviest local operation". Measured on a quiet box tonight,
  paired runs: `graph-rebuild` 14.5 s / 13.6 s wall at **50 MB** peak; `audit-health` 16.0 s /
  16.5 s wall at **768 MB** peak. Only audit-health is memory-heavy — 15× graph-rebuild — and
  it runs on every commit. The wall-time half of AN1-3 was right; the memory half named the
  wrong organ.
- **Resource control: the memory floor was exercised, and it never refused.** Floor 3000 MB.
  Free RAM before each of the four local dispatches: 8357, 8178, 7872, 7638 MB. All passed with
  wide margin; no lane was refused. The mechanism ran, which is the point — it was not a
  judgement call.
- **Availability: no Codespace was left detached.** Two probe codespaces were created tonight
  and both were driven attached over `gh codespace ssh`. They are named in §8 for teardown.
- **Availability: 23 background sessions were holding ~9.2 GB having never started.** §8.

## 8 · What the dispatcher did to the box before dispatching

- **Reclaimed 23 idle background sessions, ~9.9 GB.** They were cwd'd in primary checkouts and
  are not this batch's lanes. Established finished — in fact *never started*: each had
  `user=0, assistant=0` turns and a 3 KB transcript, idle 19–28 minutes. claude processes
  53 → 5; claude working set 11,028 MB → 1,132 MB; daemon roster 25 workers → 2. Free RAM
  5,570 → 11,140 MB.
- **The reclaim needed the supported verb, and this is the finding.** `Stop-Process` on the
  whole tree (72 processes, verified 0 survivors, 0 orphans) reclaimed **nothing**: within 30
  seconds the daemon rehydrated all 23 from `~/.claude/daemon/roster.json` under the *same
  session-ids*, at `"attempt": 2`. It did so again with the FleetView TUI already killed — the
  resurrector is the daemon, which also hosts this dispatcher and the integrator, so killing it
  was not available. `claude stop <id>` deregisters, and it held. **A SIGKILL on a background
  session is a no-op for reclaim.**
- **Deleted the nine empty worktree husks** (operator's word). Eight matched the stated
  predicate exactly (0 entries, no `.git`, unregistered, no branch). The ninth,
  `lane-x-000-docs-cut-manifest`, held one file —
  `logs/2026-09/DETECTOR-ERROR-2026-09-13.md`, preserved verbatim in §9 — written by a Stop
  hook that resolved its repo root **to the husk** and wrote there. It self-describes as
  *"the absence of a result, not a result."* `git worktree list` and `git status` clean after.
- **Two probe codespaces are alive and must be torn down:**
  `suite-baseline-2026-09-08-pgw54jq9r4xh76q5` and `lane-z-substrate-probe-q945j7g6v992pvj`.
  A stopped codespace still consumes storage quota; stopping is not deleting. Lane
  `lane-z-746-devcontainer-substrate` deletes its own probe; these two are the dispatcher's.

## 9 · Preserved verbatim — the husk artifact

```
# Closure proposals - DETECTOR ERROR (2026-09-13)

The session-end detector did not run: BACKLOG.md not found at
C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\lane-x-000-docs-cut-manifest\BACKLOG.md
(repo root resolved to
C:\Users\1028120\Documents\Dev\.dev-knowledge\.claude\worktrees\lane-x-000-docs-cut-manifest)
- the detector was pointed at a tree that is not the host repo

BACKLOG was not touched, and NO closure proposals were produced -- this
file is the absence of a result, not a result. Investigate
propose_closures.py.
```

This is a register candidate in its own right, and lane 0 is instructed to seed it: *a session
whose worktree was torn down must REFUSE to write, not silently resolve to another tree.*

## 10 · A generator defect this batch paid for, filed not fixed

**`gen_lane_contract.py emit --shape cloud` emits a contract that `audit.py health`
always REFUSES.** The generator's fixed Done-contract item 3 ends `` `pytest` green. ``
for every shape. `validate_substrate.py`'s `substrate-cloud-gate-dependent` rule scans the
**Done-when section only** and refuses `cloud` + a gate token there. So every cloud contract
this generator produces is born failing a blocking gate.

The detector's own docstring makes the trap sharper, and it is deliberate: *"a Done-when that
names `pytest` in a sentence saying the lane does NOT run it is refused."* An exculpating
clause does not clear it — the token must be absent. That is the right call for a detector
(a substring that can be talked around is not a gate), and it means the fix belongs in the
generator, exactly as the batch-V defect
(`DEFECT-dispatch-verb-rejects-generated-contract.md`) concluded for the dispatch line.

Cost here: the two cloud lanes were dispatched, archived and re-dispatched **twice** before
the record was clean. The first patch edited the **Steps** section and did not clear the gate,
because the detector does not read Steps — a fault in the fix, not in the detector.

This is the same shape as batch V's finding and deserves the same disposition: **fix the
generator, add the missing test — the shape gate checks that a Done-contract is PRESENT, never
that the substrate validator can accept it.** Presence is not acceptability. Natural owner: the
row that owns `gen_lane_contract.py`; it is filed here, not assigned.

Four cloud sessions were created and two archived in the course of this. The archived pair are
`cse_01SdDmaX4wEtCm6as4eSBBfr` / `cse_019vvMNRrX24JJD87RRozgjY` (first dispatch) and
`cse_01J1Guc3Vpm7w6RDNRyDKmgt` / `cse_01FPSYHVxynvnFngaSqUc6vz` (second). The live pair is in
§2. Every superseded session was archived rather than left running — a correction re-enters as
a NEW contract (per-lane requirement 1), and the superseded session is stopped, not raced.

## 11 · The concurrent-id collision, witnessed rather than theorised

While this manifest was being landed, the integrator seat landed `4328496e` on `main` carrying
`[#763]` and `[#764]` — **the same two ids this seat had allocated for different work**, from a
branch that could not see them. ADR-107 §6.3 records concurrent-branch id collision as a
residual it does **not** prevent; this is a live instance, and it cost a renumber.

The dispatcher's rows are therefore `[#780]`–`[#783]`, deliberately allocated well clear of the
range live lanes are drawing from (lane 4 had already taken `[#772]` from a tree whose maximum
was `762`). That is a mitigation, not a fix: any lane may still land in the 78x range.

**The integrator's `[#764]` also corrected this seat on a point of fact, and the correction is
recorded rather than quietly absorbed.** This seat concluded from the derived frontmatter that
one row can implement exactly one decision, and filed two rows partly to satisfy that. It is
wrong: `gen_task_tree._IMPLEMENTS_RE` reads a **comma-separated list** from one clause, so a
single row resolves all four decisions — which is what `[#764]` does. The two rows this seat
filed on the mistaken reading were withdrawn before landing; `[#783]` keeps only the finding
that survives scrutiny, that the `resolves:` leg has never been exercised by any document.

One more thing `[#764]` establishes that belongs in this record: **writing a DECLARE into the
transport arms a commit-tier gate against every concurrent session, and nothing warns the
author.** `decision_coverage` computes from repo state, not from staged files, so from the moment
tonight's four plan files appeared in the prompts dir, every commit in this repo was blocked —
this seat's, the integrator's, and all live lanes' alike — and a lane hitting it would have read
it as its own defect. That is the decision engine's **first witnessed refusal**, and it was not a
deliberate trip.

## 12 · Measurements this batch is standing on

```
per LOCAL bg lane      ~400 MB   session 256 + pty host 132 + conhost 10
                                 cross-check: 24 sessions -> 72 procs / 9604 MB = 400 MB/lane
                                 (tonight's diagnostic measured 392 MB counting session+pty only)
total RAM              28330 MB
non-claude floor       15631 MB
OOM watermark           1400 MB  five full-suite attempts killed at this level
audit-health peak        768 MB  every commit
graph-rebuild peak        50 MB  every commit
MEMORY FLOOR            3000 MB  = OOM watermark 1400 + two concurrent commit-gate peaks (2x768)
```

The floor is **derived, not chosen** (AN1-5): it is the level below which one more local lane
reaching its commit gate could put the box back in the range where the OOM reaper has already
been observed killing work.
