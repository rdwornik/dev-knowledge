# DIGEST: hook architecture, derived by the repo from itself

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: OPEN` with no repo citation. Source:
> `to-browser/DIGEST-HOOK-ARCHITECTURE-2026-09-23.md`. Read-only proposal record — nothing here
> was filed or edited by the session that produced it. Full evidence, lists, stale-statement
> catalogue and the draft ADR text live in the companion appendix,
> `2026-09-23-technical-hook-architecture-appendix.md`.
> Carrier rows: the S2 eight-row set filed by `lane-landing-window` per this digest's §5, and
> D26/D27 (`to-cc/DECLARE-WINDOW-DEFECTS-2026-09-23.md`).

carried-by: OPEN
lands-via: read by S3 (DIGEST-HANDOFF-READINESS) and the architect; proposals only, nothing filed or edited
date: 2026-09-23
from: postwave-hooks (POSTWAVE CHAIN S2), read-only, main @ 4667f731
model-served: claude-opus-5-5 (Opus 5.5); requested `opus`
appendix: DIGEST-HOOK-ARCHITECTURE-2026-09-23-APPENDIX.md

## 0 · Headline

- **The boot is slow and partly timing out.** In real sessions since the W4B-0 re-arm (2026-09-22 18:00 → now, about 31 boots):
  - SessionStart hooks take 7 to 16 s each at p50, against 1 to 4 s measured in isolation. Hooks for one event run in parallel, so the boot waits for the slowest one: `fleet_health.py` at p50 15.6 s and p90 26.6 s.
  - `surface_triage.ps1` timed out on **23 of about 31 boots** (bound 10 s).
  - The re-arm evidence method (one isolated run per hook) did not predict in-session cost.
- **Stop costs about 11 s per turn end,** and `propose_closures` timed out on 33 of 208 recorded runs. Its reader, `surface-closures.ps1`, is not wired anywhere, so it is a producer with no consumer.
- **Against the operator rule** (a start hook reads, an event hook triggers background work, heavy work runs isolated): 6 of 11 session hooks violate it. Only `lane_end_guard.py` fully embodies it.
- **Path protection is off.**
  - The only in-loop class BUILD-MODE rule 8 allows (path protection) is disarmed: `block-onedrive.ps1` (P0 exclusion zone) and the ADR-77 transcript guard have been off since 2026-09-17 with no expiry.
  - Only a `permissions.deny Read(...)` rule on the OneDrive path still binds, and it does not cover Write, Edit or Bash.
- **The commit-hook counter cannot support the 2026-09-25 "0 catches → REMOVE" verdict.**
  - The store is per-checkout (`<toplevel>/logs/TELEMETRY.db`, gitignored), so every lane's rows die at teardown.
  - Four armed hooks have **zero runs** in the primary store.
  - In the whole window, one hook (`backlog-filing-backpressure`) blocked anything, 4 times in 49 runs.
- **No harness moment covers a hook event.** `graph_queries.py moments` puts all 15 hook scripts in "declared nowhere". `lane-start` and `SessionEnd` have no trigger at all.
- **The boot banner states falsehoods every session.** Seven re-armed hooks are printed as "DECLARED BROKEN": the declarations file was never reconciled with the 2026-09-22/23 re-arm. Six more stale statements are listed in appendix A6.

## 1 · Inventory, every event

Cost: in-session p50, 72 h, from transcript `hookEvent` attachments (caveat in A1).

| event | hook | runs | cost | moment / process it serves |
|---|---|---|---|---|
| SessionStart | arm_hooks.py (uv) | `pre-commit install` ×3 types, idempotent | 12.2 s | arms the commit gate |
| SessionStart | surface_triage.ps1 | `gh auth status` + `gh issue list` (network) | 11.9 s, **23 timeouts** | nightly-triage surfacing (ADR-68) |
| SessionStart | changelog_sentinel.py (uv) | spawns `claude/codex --version` | 7.5 s | the /changelog-review nudge (#113) |
| SessionStart | conductor.py session-start (uv) | `gh run list` (network) + phase gate over `tasks/` | 10.4 s | conductor surfacing ([#689]) |
| SessionStart | resource_lifecycle.py session-start (uv) | process table; **writes** a seat event + a sample | 10.8 s | seat registry ([#833]), allocation |
| SessionStart | codespace_regime.py session-start (uv) | reads the local receipt ledger | 7.1 s | codespace leak surfacing |
| SessionStart | billing_leak_sentinel.ps1 | one env-var check | ~4 s isolated (powershell start-up) | billing trap (#101) |
| SessionStart | fleet_health.py (uv) | reads digest + **168 h transcript scan** + **writes** the scan cache and declarations; triggers the producer when stale | 15.6 s (p90 26.6) | fleet health, hook-rate [#808], asks, funnel, cost, seats |
| Stop | session_end_backpressure.py (uv) | git probes; advisory `additionalContext`, fires once; seat Stop event | 7.1 s, 13 timeouts | ADR-85 hygiene nudge |
| Stop | lane_end_guard.py (stdlib) | claim → detached `moment:lane-end` → receipt → reaper | ~0.3 s | **moment `lane-end`** |
| Stop (plugin) | propose_closures.py (system python) | `git log` + BACKLOG parse + **writes** `logs/PROPOSALS-<date>.md` on every turn | 10.7 s, **33 timeouts** | ADR-70 Tier-1 done-detection; reader unwired |
| PreToolUse | none wired in the repo; L0 block-onedrive off | n/a | n/a | path protection is **absent** |
| PostToolUse / UserPromptSubmit / SubagentStop / PreCompact / SessionEnd | none | n/a | n/a | n/a |
| Notification (L0) | claude-notify.ps1 | user `disableAllHooks: true`; firing is unwitnessed | n/a | operator alert |
| git pre-commit | 12 ids (10 with counter + expiry 2026-09-25) | uv per hook | 0.3 to 5.8 s check time, plus about 2.5 s uv each | freshness, hermetization, impacted tests |
| git commit-msg | 3 ids (counter + expiry) | uv | 0.3 to 1.0 s | backlog id / kill-candidates / type prefix |
| git pre-push | block-ff-push, block-unanchored-push (no counter) | uv | n/a | core-invariant #5; ADR-85 JOURNAL anchor |
| CI | conductor.yml `commit-gate`, 19 manual ids, REPORT-ONLY | Actions | n/a | the last 3 pushes show `failure`, with no owner in the banner |

## 2 · Classification against the operator rule

The rule (architect ruling delegated by the operator, LANE-W4B-6 2026-09-22): **R1** a start hook reads · **R2** an event hook triggers background work · **R3** heavy work runs in an isolated checkout.

| hook | verdict | why |
|---|---|---|
| fleet_health.py | **VIOLATES R1** | The audit moved out (W4B-6), but the `[#808]` hook-rate block still scans 168 h of transcripts and writes `HOOK-BYPASSES-SCAN-CACHE.json` and `HOOK-BYPASSES-BROKEN.json` in-session. |
| surface_triage.ps1 | **VIOLATES R1** (network) | Two `gh` round-trips on every boot; times out on most boots. |
| conductor.py session-start | **VIOLATES R1** (network + compute) | A `gh run list` plus a 441-row phase gate on every boot. Both are producer work whose result the Actions run already has. |
| arm_hooks.py | **VIOLATES R1** (write + spawn) | Runs `pre-commit install` on every boot to assert an idempotent state. A read would detect the rare case that needs the install. |
| propose_closures.py (plugin Stop) | **VIOLATES R2** | Does the work inline on every turn end for a job whose unit is "new commits since last run". Writes a file nobody reads. |
| session_end_backpressure.py | **VIOLATES R2** (soft) | Inline and advisory; the cost is almost all `uv` start-up (the checks are git probes). |
| resource_lifecycle.py | complies, with an exception | Its writes are the seat **event record** (only a hook knows the session id) plus one sample; the ADR draft allows exactly that one append. |
| changelog_sentinel.py · codespace_regime.py · billing_leak_sentinel.ps1 | comply | Local reads. Their cost is interpreter start-up under load (uv or powershell), not work. |
| lane_end_guard.py | **the model** | Claim, detached worker, receipt, reaper; stdlib; never exits 2. |

**Root cause: one interpreter per concern per event.** Eight SessionStart entries (seven via `uv run`, about 2.5 s each) start together on a loaded box. That count is also the [#863] exposure.

## 3 · Gaps

**Moments no hook reaches**
- `lane-start` (harness.yaml: "the lane's own first turn"): no trigger, so a lane that skips it is invisible.
- `SessionEnd`: `seat_registry` maps it to `absent`, but no hook sends it.
- `merge`, `teardown` and `batch-close` are integrator commands. That is correct: no git hook should run them.

**Hooks reaching no moment**
- `propose_closures.py`: output unread, because `surface-closures.ps1` is not wired.
- All 15 hook scripts are "declared nowhere" (A1): `harness.yaml` has no SessionStart, commit or push moment, so the graph cannot see the processes they serve.

**Off without a dated expiry** (appendix A5)
- prompts guard, ADR-77 guard, logs_retention: owner [#863], no expiry.
- block-onedrive: owner [#865], no expiry.
- L0 claude-notify Stop: no owner.
- `.git/hooks/pre-commit.legacy.disabled-2026-09-13`: no reason found anywhere.
- The 19 manual ids have a return condition (a counter) but no date.

**Mislabel that leaves guards in no track**
- O-2 says the 2026-09-17 emergency disable is NOT BUILD MODE's, and re-arms it on its own evidence. W4B-0 re-armed only the eight SessionStart hooks and called the PreToolUse and ADR-77 guards "O-2's set" (§4).
- So the prompts guard, the ADR-77 guard, logs_retention and block-onedrive sit in neither track. Two of them are path protection, which rule 8 keeps in-loop.

**BUILD MODE set: listed and left alone (O-2)**
- `deny_and_point.py` (PreToolUse, unwired 2026-09-18 by rule 8, script kept).
- The commit-layer return path: B2 lane 4's counter-and-expiry arming of 13 hooks. Nothing here proposes arming or disarming any of them.
- The 19 `manual` ids return only under BUILD-LIST 2026-09-18 (a counter that shows catches). They are listed, not touched.

## 4 · Design: target hook set per event

Reuse first. The primitives already exist:
- `lane_end_guard.spawn_worker` (breakaway detach), already imported by `fleet_health`.
- `_take_marker` (O_EXCL claim), `_write_atomic` receipt, and `_reap_abandoned`.
- `fleet_health.provision_isolated_checkout`.

Delta verbs are BUILD-MODE's: MOVE / WIRE / REWRITE. No BUILD.

| event | target | serves | delta |
|---|---|---|---|
| SessionStart | **ONE stdlib reader entry:** prints the published boot digest; checks the billing env var and the git-hook shims by reading them; appends the seat event. If the digest is stale → the existing claim + detached producer. In a lane → claim + detached `moment:lane-start`. | boot surfacing; seat registry; lane-start | MOVE the six surfacing computations into the producer; WIRE lane-start |
| Stop | **ONE stdlib trigger entry:** seat Stop event + `lane_end_guard` + a closure-proposal trigger claimed per new HEAD SHA (runs once per new commit, not once per turn). The backpressure advisory becomes stdlib and stays fire-once, or folds into the same entry. | lane-end; ADR-70 done-detection; ADR-85 nudge | REWRITE propose_closures' trigger (same script, run by the worker) |
| SessionEnd | stdlib seat `absent` record | seat registry | WIRE |
| PreToolUse | **path protection as `permissions.deny`** (no process per call): Edit, Write and NotebookEdit on the OneDrive exclusion path ([#865] option c) and on `docs/decisions/transcripts/**` (ADR-77). No process-spawning PreToolUse hook before the [#863] watchdog. The Bash hole is stated. | core-invariant #1; ADR-77 | REWRITE (hook → deny rule) |
| pre-commit / commit-msg | unchanged set until the 2026-09-25 verdict; the counter store moves to the git **common dir**, so lane rows survive teardown | data loss, freshness | MOVE (the counter path) |
| pre-push | unchanged; wrap both in the same counter | core-invariant #5; ADR-85 | WIRE |
| CI | conductor `commit-gate` stays REPORT-ONLY; its verdict is what the SessionStart reader prints, instead of polling `gh` | the manual 19 | MOVE |

**Caveat on reusing `_reap_abandoned`:** it can mark a live worker FAILED after 300 s (appendix A8). Add a pid-liveness check before reaping.

**Expected effect:**
- Boot: from 8 interpreters to 1, with no `uv` on the path, so the target is at most 2 s p90 in-session.
- Stop: from 3 interpreters to 1.
- [#863] exposure divided by the same factor.
- The per-turn `propose_closures` cost falls to near zero between commits.

## 5 · Proposed rows (proposals only; no ids, nothing filed)

1. **SessionStart becomes one reader.** Provenance: LANE-W4B-6 rule; A2 cost table; `docs/audits/2026-09-22-technical-lane-hooks-rearm-live-measurement.md` §2.1. Done when:
   - over 20 real boots the SessionStart p90 is at most 2 s, and there are zero timeouts, measured from transcript attachments;
   - no SessionStart entry makes a network call or writes anything except the seat event;
   - the hook-rate scan, the conductor and triage `gh` polls and the changelog probe run only in the detached producer.
2. **Re-arm evidence must be in-session.** Provenance: A2 against W4B-0 §2. Done when a hook is admitted or re-armed only on 20 or more real events under the concurrent hook set, from transcript attachments; `surface_triage.ps1` is folded into row 1 or re-measured that way.
3. **Closure proposals run once per new commit, with a reader.** Provenance: A2 (`propose_closures` 33 timeouts); `.claude/settings.json` KNOWN-UNGOVERNABLE entry; plugin `hooks.json`. Done when:
   - the plugin Stop hook claims per HEAD SHA and hands the work to a detached worker, so the parity MUST `settings-plugin-tier1` stays green;
   - its in-session cost is under 1 s;
   - `PROPOSALS-*.md` has a wired reader, or the operator rules the producer retired.
4. **The commit-gate counter survives lanes, and "no runs" is not "no catches".** Provenance: A3; `telemetry_emit.default_db_path`. Done when:
   - a lane's `hook_run` rows are readable from the primary after its worktree is removed;
   - the 2026-09-25 expiry report lists runs and blocks per hook, and marks a hook with zero runs UNMEASURED rather than REMOVE.
   **Time-critical:** expiry is 2026-09-25.
5. **Path protection comes back without a process.** Provenance: [#865] option (c); ADR-77; BUILD-MODE rule 8 ("nothing but path protection"). Done when:
   - the operator has ruled on [#865];
   - `permissions.deny` rules for Edit, Write and NotebookEdit cover the exclusion path and the transcript zone, each witnessed by a refused call in a throwaway session;
   - `~/.claude/rules/core-invariants.md` is changed in the same act;
   - the Bash gap is stated in the rule.
6. **The boot banner tells the truth about hook state.** Provenance: A6 item 6; [#888]. Done when:
   - no hook is printed DECLARED BROKEN while settings arm it with a PASS record newer than the declaration;
   - the declarations file and the settings `//` register come from one record (the [#888] DEGRADED record, or reconciled by a check);
   - the seven stale declarations are reinstated.
7. **SessionEnd and lane-start get their triggers.** Provenance: `seat_registry.py` (SessionEnd → absent); `harness.yaml` moment `lane-start`. Done when:
   - a SessionEnd stdlib hook writes the seat's `absent` record;
   - the first SessionStart in a lane worktree claims and detaches `moment:lane-start` exactly once per lane, witnessed by its receipt.
8. **Stale-statement sweep** (A6 items 1 to 5). Provenance: this digest. Done when `CLAUDE.md` §4, the manifest behind `methodology-roster.md`, the two `harness.yaml` fates, the L0 rows of `ecosystem/organ-registry.yaml` and the ADR-74 matrix match live state. The ADR-74 item goes through the ADR below, not an in-place edit.

## 6 · ADR draft: hook taxonomy (full text in appendix A7)

**ADR-NNN (Proposed): a start hook reads, an event hook triggers, heavy work runs isolated.** It amends ADR-74 §1 and is consistent with ADR-85 and BUILD-MODE rule 8. It sets four closed classes (READER, TRIGGER, PATH GUARD, GATE), one stdlib entry per event, in-session admission over 20 or more events, and the off/degraded register as [#888] data. It rejects longer timeouts, wrapping every hook in `bounded_hook.py`, and scheduled tasks.

DONE 2026-09-23T20:04Z
