<!-- scope: meta -->

# Validation record — #85 local fleet-baseline scheduler (ADR-76)

- **Opened:** 2026-06-06
- **Status:** OPEN — partial (n=1 evidence captured; full validation spans real nights)
- **Refs:** ADR-76 (mechanism), ADR-74 (rider R2), BACKLOG #85
- **Subject:** Windows Task Scheduler `\DevKnowledge\fleet-baseline` → `python scripts/fleet_health.py` (read-only collector; no LLM on the scheduled path)

> **Immutable dated artifact.** Future validation results land as **dated addenda**
> appended below — never edit the cases above. Tick a box only in an addendum that
> records the witnessing run.

## Closure gate

**#85 closes only when cases 1, 2, 3, and 5 are witnessed.** Case 4 is best-effort
(non-blocking). Each tick must cite a dated addendum with concrete evidence.

## Council validation cases

- [ ] **(1) Normal scheduled fire** — the task fires unattended at its daily 09:00
  trigger (no manual `schtasks /run`) and writes a fresh digest with a
  `completed_at` stamp and `Baseline completed (N/T green)`. *Pre-case witnessed
  2026-06-06 via manual fire — see addendum; the unattended 09:00 fire is still owed.*
- [ ] **(2) Sleep-miss + lid-open catch-up** — machine asleep/off across the 09:00
  trigger; on next wake/logon Task Scheduler's "run as soon as possible after a
  missed start" (StartWhenAvailable) fires the run, and no wake-from-sleep occurred
  (WakeToRun OFF). Witness: `Get-ScheduledTaskInfo` LastRunTime lands after a known
  sleep window, with no wake event.
- [ ] **(3) Stale warning fires** — when the last successful `completed_at` is older
  than 48h, `fleet_health.py` prints `[fleet] digest stale (>48h) -- scheduled run
  may be failing` on both the skip/surface and run paths, and still exits 0.
- [ ] **(4) Concurrent SessionStart read during run** *(best-effort)* — a SessionStart
  `fleet_health.py` read that overlaps an in-flight scheduled write never observes a
  half-written digest. Guarded by the atomic write (`os.replace`); hard to force
  deterministically, hence best-effort.
- [ ] **(5) Hung-repo timeout** — a wedged repo check does not hang the run: the audit
  subprocess is killed at the `120s × repo-count` budget and the digest records an
  **INCOMPLETE** baseline (no `completed_at`), exit 0. *Attribution limit: the timeout
  is fleet-level — the single `audit.py run` subprocess audits all repos in-process,
  so the digest records the run as INCOMPLETE but does not name which repo wedged. The
  safety property (bounded, never an unbounded hang; failure recorded not silent) is
  delivered; per-repo naming is not.*

## Witnessed evidence — 2026-06-06 (pre-case for case 1)

**Manual scheduler-context fire** (`schtasks /run`, not the 09:00 trigger) — the
env-divergence test: does the collector succeed under the Task Scheduler environment
(PATH, working dir, interpreter), not just the interactive shell?

- Registration: `setup-fleet-scheduler.ps1` registered `\DevKnowledge\fleet-baseline`
  — Daily @ 09:00, Logon Mode `Interactive only`, Run As `1028120`, Start In =
  repo root, Stop after `00:15:00`, Power Management empty (no wake), Next Run
  `2026-06-07 09:00`.
- Forced the refresh path by moving the gitignored `logs/FLEET-HEALTH.md` aside
  (today's cached digest would otherwise throttle the run), then `schtasks /run`.
- **Result: `LastTaskResult: 0` (success).** The collector ran the cross-repo audit
  under the scheduler env and rewrote the digest:
  - `completed_at: 2026-06-06T18:23:18` present.
  - `Baseline completed (4/5 green).`
  - The audit genuinely executed git/python under the scheduled environment — it
    surfaced a real `corp-monorepo` finding (4/5, not a no-op), proving PATH/git/
    interpreter resolve correctly under the Task Scheduler token, not only in the
    interactive shell.
- The audit's tracked-file side effects (`ecosystem/*/state.yaml`, history,
  `docs/audits/*-ecosystem-audit.md`) were restored on the feature branch — pre-existing
  audit-state churn, out of #85 scope. **Operational note:** every scheduled run leaves
  these tracked-file modifications in the working tree (the collector calls `audit.py
  run`, which refreshes them); an unattended run does not commit, so an interactive
  session will see them dirty afterward. This is inherited behavior, not introduced by
  the scheduler, but it is the thing to watch during nightly validation.

**Not yet witnessed:** the unattended 09:00 fire (case 1 proper), the sleep-miss
catch-up (2), the stale warning in situ (3), and the hung-repo timeout (5) — these
require real elapsed nights / fault injection and land as dated addenda.

---

## Addenda

*(none yet — append dated entries here as cases are witnessed)*
