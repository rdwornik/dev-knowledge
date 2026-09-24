# APPENDIX: hook architecture evidence, full lists, ADR draft text

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: OPEN` with no repo citation. Source:
> `to-browser/DIGEST-HOOK-ARCHITECTURE-2026-09-23-APPENDIX.md`.
> Front door: `2026-09-23-technical-hook-architecture.md`.
> Carrier rows: the S2 eight-row set filed by `lane-landing-window` (front door §5), and
> D26/D27 (`to-cc/DECLARE-WINDOW-DEFECTS-2026-09-23.md`).

carried-by: OPEN
lands-via: read by S3 and the architect; proposals only, nothing filed
date: 2026-09-23
from: postwave-hooks (POSTWAVE CHAIN S2), read-only, main @ 4667f731
front-door: DIGEST-HOOK-ARCHITECTURE-2026-09-23.md

## A1 · Evidence commands (all read-only; `git status --porcelain` was empty before and after, 0 lines)

- **Wiring:** `.claude/settings.json` (hooks + the `//` register blocks) · `~/.claude/settings.json` (`disableAllHooks: true`, hooks = Notification only) · `~/.claude/settings.hooks-DISABLED-2026-09-17.json` (the removed L0 block) · `plugins/tier1-lifecycle/hooks/hooks.json` · `.pre-commit-config.yaml` · `ls .git/hooks` (commit-msg, pre-commit, pre-push, all dated 2026-09-23 16:19, plus an empty `pre-commit.legacy.disabled-2026-09-13`, 0 bytes, no reference to it in the repo).
- **Per-hook stage:** `uv run --locked python -c "import yaml; ..."` over `.pre-commit-config.yaml`, which prints each id with its effective `stages` (default_stages = pre-commit).
- **In-session hook cost:** a stdlib scan of `~/.claude/projects/*/*.jsonl` (and one level deeper) for `attachment.hookEvent` records, reading `durationMs`, `timedOut` and `command`. Window: records with `timestamp >= 2026-09-22T18:00` (after the W4B-0 re-arm), plus a separate 72 h view for p50/p90. Scripts: `$CLAUDE_JOB_DIR/tmp/hookcost.py`, `hookcost2.py`. They were deleted with the job; the logic is described here in full.
  **Caveat, per memory `hook-timeout-bounds-only-a-live-top-process`:** an attachment is written only when a hook produces output or times out. Attachments are therefore NOT runs. Durations come from output-producing runs only. Timeouts are exact counts, because a timed-out run always writes an attachment. The boot denominator used is `resource_lifecycle.py` attachments (it prints on every boot): 31.
- **Commit-hook counters:** `sqlite3 file:logs/TELEMETRY.db?mode=ro`, `select name,count(*),sum(outcome='block'),avg(duration_ms) from events where event_type='hook_run' group by name`.
- **Counter locality:** `scripts/telemetry_emit.py::default_db_path` resolves `<git rev-parse --show-toplevel>/logs/TELEMETRY.db`, which is gitignored at `.gitignore:124`. In a worktree that is the worktree's own file. The two live worktrees (`lane-adr-state-store`, `postwave-changelog`) carry no `logs/TELEMETRY.db` at all.
- **Moments:** `uv run --locked python scripts/graph_queries.py moments --db $CLAUDE_JOB_DIR/tmp/graph.db` (a scratch store, so the repo's stale store was not rebuilt in place). Result: 189 organs; 23 declared at a moment; 166 declared nowhere (130 wired by another surface, 36 by none). All 15 hook scripts are declared nowhere.
- **L0 probe:** `generate_organ_index.py --probe-user-level` reports "no drift", but it states that session hooks are NOT probed.
- **Model that served this session:** `claude-opus-5-5` (Opus 5.5); requested `opus`.

## A2 · In-session cost table (since 2026-09-22T18:00; 72 h p50/p90 in brackets)

| event | hook | attachments | timedOut | p50 / p90 / max (72 h) |
|---|---|---|---|---|
| SessionStart | arm_hooks.py | 16 | 0 | 12.2 / 15.8 / 30.0 s |
| SessionStart | surface_triage.ps1 | 23 | **23** (bound 10 s) | 11.9 / 14.5 / 15.8 s |
| SessionStart | changelog_sentinel.py | 30 | 0 | 7.5 / 11.0 / 11.5 s |
| SessionStart | conductor.py session-start | 30 | 0 | 10.4 / 14.4 / 20.5 s |
| SessionStart | resource_lifecycle.py session-start | 31 | 0 | 10.8 / 13.4 / 15.1 s |
| SessionStart | codespace_regime.py session-start | 27 | 0 | 7.1 / 9.4 / 10.5 s |
| SessionStart | fleet_health.py | 16 | 0 | 15.6 / 26.6 / 28.0 s |
| SessionStart | billing_leak_sentinel.ps1 | 0 (silent when clean) | 0 | not observable in-session; 3.98 s isolated |
| Stop | propose_closures.py (plugin) | 208 | **33** (bound 15 s) | 10.7 / 15.5 / 23.3 s |
| Stop | session_end_backpressure.py | 103 | **13** (bound 15 s) | 7.1 / 13.8 / 23.1 s |
| Stop | lane_end_guard.py | 0 (silent skip path) | 0 | ~0.3 s by its own receipt `guard_ms` |

The W4B-0 isolated measurement (`docs/audits/2026-09-22-technical-lane-hooks-rearm-live-measurement.md` §2) gave 1.1 to 4.0 s per hook. In real boots, with eight interpreters starting in parallel on a box running 11 seats, the same hooks take 7 to 16 s at p50. The isolated run did not predict in-session cost. This session's own boot recorded 10.5, 10.5, 13.8 (timed out), 13.8, 14.9 and 26.6 s.

## A3 · Commit-layer counters (`logs/TELEMETRY.db`, primary checkout only)

| hook | runs | blocks | avg ms |
|---|---|---|---|
| commit-message-type-prefix | 49 | 0 | 349 |
| backlog-id-on-close | 49 | 0 | 660 |
| backlog-filing-backpressure | 49 | **4** | 966 |
| validate-hermetization | 43 | 0 | 892 |
| provider-registry-agreement | 43 | 0 | 1824 |
| impacted-tests-guard | 43 | 0 | 5777 (max 13889) |
| dispatch-conformance | 43 | 0 | 973 |
| row-archive-proof | 3 | 0 | 786 |
| claude-rosters-freshness | 1 | 0 | 328 |
| codemap-freshness · roster-freshness · quality-requirements-freshness · intake-index-freshness | **0 rows** | n/a | n/a |
| audit-index-freshness · organ-index-freshness · block-ff-push · block-unanchored-push | not wrapped | n/a | n/a |

Four armed hooks have **no runs at all** in the store their expiry is judged from. "0 catches" and "0 runs" are different findings, and the 2026-09-25 rule ("0 catches in-window -> REMOVE") cannot tell them apart. See memory `failure-only-records-are-not-a-rate`.

## A4 · Full pre-commit register (36 ids)

- **pre-commit (12):** codemap-freshness, roster-freshness, claude-rosters-freshness, audit-index-freshness, organ-index-freshness, quality-requirements-freshness, validate-hermetization, intake-index-freshness, row-archive-proof, provider-registry-agreement, impacted-tests-guard, dispatch-conformance.
- **commit-msg (3):** backlog-id-on-close, backlog-filing-backpressure, commit-message-type-prefix.
- **pre-push (2):** block-ff-push, block-unanchored-push.
- **manual (19), run REPORT-ONLY by `.github/workflows/conductor.yml` job `commit-gate`:**
  - block-commit-on-main, normalize-dated-headers, toc-freshness-playbook, audit-title-gate, doc-counts-pytest-freshness, check-seal-identity, validate-backlog, prepend-order, lane-contract-check, derived-copies-rebind, graph-rebuild, graph-orphan-census, graph-task-coverage, graph-process-list, graph-edge-class-census, decision-coverage, audit-health, coherence-nudge, ruff.
  - Of these, B2 lane 4 measured seven as broken on the tree and nine as clean but over 15 s; `ruff` and `coherence-nudge` are manual by design (`docs/audits/2026-09-18-technical-b2-lane4-hook-role-review.md` Part B).
- **Conductor:** the SessionStart line showed `failure` for the last three pushes (2026-09-23 14:13, 17:23, 19:12). No row or owner is named in the banner.

## A5 · Off-register: every hook that is off, and whether it has a dated reason

| hook | off since | reason recorded | owner | expiry |
|---|---|---|---|---|
| deny_and_point.py (PreToolUse) | 2026-09-18 | BUILD-MODE rule 8, affordance mis-built as refusal | BUILD MODE | none; BUILD MODE exit or 2026-11-18 |
| prompts guard (`fleet_health.py --prompts-guard`, PreToolUse) | 2026-09-17 | emergency (suspended orphans) | [#863] | **none** |
| block_immutable_edits.py (ADR-77, PreToolUse) | 2026-09-17 | emergency collateral, "real safety loss" | [#863] | **none** |
| logs_retention.py (SessionStart) | 2026-09-17 | still_off list | [#863] | **none** |
| block-onedrive.ps1 (L0 PreToolUse) | 2026-09-17 | sidecar `~/.claude/settings.hooks-DISABLED-2026-09-17.json` | [#865] | **none** |
| surface-closures.ps1 (L0 SessionStart) | 2026-09-17 | out of repo scope | [#808] | 2026-12-21 (scope re-check) |
| claude-notify.ps1 (L0 Stop) | 2026-09-17 | sidecar | none named | **none** |
| claude-notify.ps1 (L0 Notification) | still wired; user `disableAllHooks: true` | sidecar | none named | no attachment witnessed in the 30 newest transcripts, so whether it fires under the project's `false` is UNWITNESSED |
| 19 manual pre-commit ids | 2026-09-17 (AB close) | header of `.pre-commit-config.yaml` | [#863] / BUILD-LIST 2026-09-18 | the return condition is a counter, not a date |
| `pre-commit.legacy.disabled-2026-09-13` | 2026-09-13 (filename) | **none found** | none | none |

## A6 · Stale statements found on the way (location, then the live evidence)

1. `CLAUDE.md` §4 "Out of scope": "the ADR-77 guard stays armed". Evidence: it has been off since 2026-09-17 (`.claude/settings.json` `still_off_not_restored_by_this_act`).
2. `.claude/methodology-roster.md` (generated from the manifest): "session_end_backpressure.py ... (JOURNAL SHA-anchor hard block)". Evidence: advisory in full since the ADR-85 amendment of 2026-08-03 (the script's own docstring). Fix at the manifest, then regenerate.
3. `ecosystem/harness.yaml` fates for `scripts/codespace_regime.py` and `scripts/surface_triage.ps1`: "its hook is off since 2026-09-17 and returns when [#863] lands". Evidence: both re-armed 2026-09-22 (`//hooks-REARMED-ON-EVIDENCE-2026-09-22`).
4. `ecosystem/organ-index.md` rows 99, 100, 108, 110 mark L0 `Notification`, `PreToolUse: block-onedrive`, `SessionStart: surface-closures` and `Stop: claude-notify` as **ARMED**. Evidence: live `~/.claude/settings.json` has `disableAllHooks: true` and wires Notification only. The source is `ecosystem/organ-registry.yaml` (declared, not probed).
5. `docs/decisions/ADR-74` §1 matrix places "Cross-repo baseline | fleet_health.py | SessionStart (throttled)". Evidence: the architect ruling in LANE-W4B-6 (2026-09-22) moved the work to a detached producer; SessionStart only reads.
6. The fleet_health `[hook-BROKEN]` banner, printed at every boot from `logs/HOOK-BYPASSES-BROKEN.json`: it declares surface-triage, codespace-regime, resource-lifecycle, billing-leak-sentinel, conductor-session-start, changelog-sentinel and fleet-health-session-start BROKEN, "Disabled: NO". Evidence: all seven are armed with a PASS record dated 2026-09-22 or 2026-09-23. `bounded_hook.py reinstate` was never run for any of them.
7. `docs/audits/2026-09-22-technical-lane-hooks-rearm-live-measurement.md` §4 calls the two PreToolUse guards and the ADR-77 guard "O-2's set". Evidence: O-2 (`to-cc/RATIFICATION-2026-09-22-secrets-and-build-mode.md`) says the 2026-09-17 emergency disable is **not** covered by O-2. The audit is immutable, so this is recorded here and not corrected there.

## A7 · ADR draft (full text; proposal only, number not reserved, nothing filed)

**ADR-NNN: Hook taxonomy: a start hook reads, an event hook triggers, heavy work runs isolated**
Status: Proposed (draft by postwave-hooks, 2026-09-23). Amends ADR-74 §1 (the rows "Cross-repo baseline", "Awareness / surfacing" and "Done-detection"). Consistent with ADR-85 (a Stop hook carries no teeth) and BUILD-MODE rule 8 (refusals only at git boundaries; in-loop only path protection).

Context: the operator rule of 2026-09-22 (LANE-W4B-6 Value) was written for one hook, fleet_health. The in-session measurement in A2 shows the same shape in six other hooks: in-session network calls, whole-tree computation, and writes. The result is a boot blocked for about 16 s at p50 and 27 s at p90, 23 timeouts in about 31 boots, and 46 Stop timeouts. The 2026-09-16/17 wedges ([#863]) came from the same place: interpreter count per event.

Decision:
1. **Four hook classes, closed.**
   - READER (SessionStart): prints published state; no network; no writes except ONE append-only event record (the seat registry); target at most 2 s p90 in-session.
   - TRIGGER (any event that starts work: SessionStart when state is stale, Stop, SessionEnd): exclusive claim, then a detached worker, then a receipt, then a reaper. This is the `lane_end_guard.py` pattern. It returns in under 1 s and never exits 2.
   - PATH GUARD (PreToolUse): only path protection, expressed as `permissions.deny` rules wherever expressible, with no process per call. A process-spawning PreToolUse hook is admitted only after the [#863] watchdog exists.
   - GATE (git pre-commit, commit-msg, pre-push; CI): the only refusing class. Each gate carries a counter and an expiry (BUILD-MODE rule 7), and its counter survives worktree teardown.
2. **Heavy work** (a cross-repo audit, a transcript scan, a graph rebuild, a moment) runs only in a TRIGGER's worker, in an isolated checkout when it reads or writes the tree (`fleet_health.provision_isolated_checkout`).
3. **One entry per event per repo where possible.** Each hook entry is one more interpreter at the event. Hook entries are stdlib `python`, not `uv run`, on the READER and TRIGGER paths. The `uv` start-up cost is paid by the worker, not by the event.
4. **Admission test for a new or re-armed hook:** it is measured in-session, under the real concurrent set for its event, over at least 20 events, from transcript attachments. An isolated single run is not admission evidence.
5. **The register is data.** Off, degraded and re-armed state lives in the [#888] DEGRADED record, not in `//` comment keys. The `[hook-BROKEN]` banner reads the same record as the settings file.

Consequences: SessionStart shrinks from 8 entries to 1 or 2, and Stop from 3 to 1 or 2. `propose_closures` becomes a trigger that runs once per new HEAD, which keeps the plugin wired (the parity MUST holds) and removes the per-turn cost. `surface_triage` and conductor's `gh` poll move into the producer. The ADR-74 matrix rows are re-pointed. Nothing in the BUILD MODE set is changed by this ADR.
Alternatives rejected: (a) longer timeouts, which do not bound the suspended mode ([#863]); (b) `bounded_hook.py run` as a wrapper for every hook, which is one more interpreter per event, whose wiring is held by the operator ruling of 2026-09-17, and which closes only the descendant case; (c) moving everything to a scheduled task, which cannot see the session id or the lane's HANDBACK line.

## A8 · Caveat on reusing `lane_end_guard._reap_abandoned`

`_reap_abandoned` treats a claim as abandoned when the receipt is still `running` and its mtime is more than `STALE_RUNNING_S` = 300 s old. The worker has no deadline (DECLARE-NIGHT N3) and writes no heartbeat. So a producer that legitimately runs past 5 minutes gets a FAILED receipt from the next Stop or boot while it is still running. For comparison, the cold cross-repo audit ran for about 9 minutes on 2026-09-22 (W4B-0 §2.1). `_finish` later overwrites the FAILED receipt, because the handback matches, so the final state is right. In between, readers see a false FAILED. When this pattern is reused for longer producers: record the worker pid in the claim, and reap only when that pid is gone. Do not lengthen the window.
