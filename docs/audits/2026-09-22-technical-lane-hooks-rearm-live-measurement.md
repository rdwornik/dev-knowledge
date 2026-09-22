# Lane hooks-rearm — the eight emergency-disabled SessionStart hooks, tested live and re-armed on evidence

**Lane:** `lane-hooks-rearm` · **Branch:** `worktree-lane-hooks-rearm` · **Date:** 2026-09-22

Consumers: [#956] (this lane's row); no-consumer clauses elsewhere in this record refer to
findings this audit does not carry forward as a governance surface.

## 0 · Inventory — the eight entries, and why each was disabled

Source: `.claude/settings.json`'s `//hooks-RESTORED-AND-DISABLED-INDIVIDUALLY-2026-09-17` comment
block (`disabled_individually`), cross-checked against `docs/audits/2026-09-16-technical-lane-ab-808-guard-timeout.md`
(the measurement that produced the bypass-rate table) and `//hooks-EMERGENCY-DISABLED-2026-09-17`
(the separate orphaned-interpreter incident). All eight carry `expiry: 2026-09-24`.

| # | Hook | Event | Disable reason | Bypass rate | Owner |
|---|---|---|---|---|---|
| 1 | `surface_triage.ps1` | SessionStart | over the 10% bypass bar (168h window, ≥20 runs, operator ruling 2026-09-17 item 2) | 252/262 = 96% | `[#808]` |
| 2 | `surface-closures.ps1` | SessionStart | over the bar; **not a repo-owned hook** — its home is user-level `~/.claude/settings.json`, which has no `SessionStart` array at all (confirmed live, §1.1) | 145/252 = 58% | `[#808]`, advisory/out-of-repo |
| 3 | `fleet_health.py` | SessionStart | over the bar; also the host `bounded_hook.py`'s own bypass surface rides inside | 107/263 = 41% | `[#808]` |
| 4 | `codespace_regime.py session-start` | SessionStart | over the bar | 15/45 = 33% | `[#808]` |
| 5 | `resource_lifecycle.py session-start` | SessionStart | over the bar | 16/63 = 25% | `[#808]` |
| 6 | `billing_leak_sentinel.ps1` | SessionStart | over the bar **and** separately named in the 2026-09-17 emergency order (orphaned interpreters, suspended-at-creation, alongside the two PreToolUse guards) — a double disable, only the first leg is this lane's to test | 45/205 = 22% | `[#863]` |
| 7 | `conductor.py session-start` | SessionStart | over the bar | 34/199 = 17% | `[#808]` |
| 8 | `changelog_sentinel.py` | SessionStart | over the bar (barely) | 27/263 = 10.3% | `[#808]` |

`propose_closures.py` (Stop, 15%) is a ninth entry in the same comment block but is explicitly
`state: RUNNING (not disabled)` — KNOWN-UNGOVERNABLE, left running by deliberate operator ruling
because every lever is machine-wide. It is not one of the eight and this lane does not touch it.

### 0.1 · `surface-closures.ps1` is out of this lane's file ownership

`Read` of `C:\Users\1028120\.claude\settings.json` (live, this session) confirms `"hooks"` there
carries only a `Notification` entry — no `SessionStart` array exists at user level, and no
`surface-closures.ps1` file exists anywhere in this repo (`Glob **/surface-closures.ps1` — no
matches). The frozen contract scopes this lane to `.claude/settings.json` (the repo file) only.
Re-arming a hook whose home is `~/.claude/` would be a global-infra edit requiring its own
operator ruling (global CLAUDE.md rule 6), which this lane does not have and does not seek.
**Verdict for this entry is therefore scope, not measurement**: it cannot be tested or armed from
here (§3).

## 1 · Methodology — what "live test" means here, and why

The contract asks to "start one minimal real session in this worktree with only that hook armed;
record duration, exit code, and interpreter processes before and after." A full nested `claude`
session was **not** spawned to do this, for three stated reasons:

1. **WAVE4B common rule 6** bars scheduled wakeups, loops and cron, and states "nothing of yours
   may outlive your last message (three sessions hung yesterday)." A nested session that hangs —
   which is exactly the failure mode under test — would itself outlive this session's messages if
   anything went wrong, reproducing inside this lane the very risk the eight hooks were disabled
   over.
2. The original 2026-09-17 incident's own root cause (processes "created suspended and never
   resumed") was never identified (`docs/audits/2026-09-16-technical-lane-ab-808-guard-timeout.md`
   §0.1, §7). Deliberately spawning more nested sessions to probe an unidentified suspension defect
   is the wrong instrument for a lane whose job is to re-arm, not to re-open that investigation.
3. `docs/audits/2026-09-16-technical-lane-ab-808-guard-timeout.md` §1.1 itself used throwaway
   **child** `claude -p` sessions for its step-1 probe — a different, heavier instrument than what
   this lane uses, but establishing that testing the exact hook *command*, not the full harness
   around it, is an accepted measurement class in this repo's own precedent.

**What was actually run:** for each of the seven repo-owned hooks, the **exact command string**
`.claude/settings.json` carried immediately before the 2026-09-17 disables (recovered from git
history: `9af353f7^` for six of them, `426b9cac^` for `billing_leak_sentinel.ps1`), invoked through
`bash -c` (Git Bash — the same POSIX shell Claude Code's hook launcher uses) with
`CLAUDE_PROJECT_DIR` set to this worktree's root, exactly as SessionStart would set it. Each run
was bounded by its declared `timeout` **plus 20s headroom** (`bounded_hook.py`'s own
`HARNESS_HEADROOM_S` convention, reused rather than invented), so a run that does not self-bound is
killed rather than left to hang the lane. Duration, exit code and a before/after process snapshot
(`Get-CimInstance Win32_Process`, filtered to `python`/`uv`/`powershell`/`pwsh`/`conhost`) were
recorded per hook. Pass = finished inside its **declared budget** (not the +20s kill bound), exit
0, zero new processes still alive a few seconds after return.

**One methodology defect found and fixed in-session, disclosed rather than hidden:** the first
pass routed hook commands through `Start-Process -FilePath 'bash'`, which on this box resolves to
the Windows App Execution Alias stub (`WindowsApps\bash.exe`, the WSL launcher), not Git Bash — it
failed every hook instantly with "Windows Subsystem for Linux has no installed distributions." That
was a harness bug, not a hook defect, and is why the raw first-pass numbers (all `exit=1`,
sub-second) are not reported below; only the corrected run (explicit
`C:\Program Files\Git\bin\bash.exe`, and for the `uv run` hooks a second correction routing them
through the Bash tool directly rather than through nested `Start-Process` argument quoting, which
was mis-escaping the `uv run --locked python "<path>"` argument and making `uv` print its own
top-level `--help`) is recorded.

## 2 · Live-test results

| Hook | Budget | Kill bound | Exit | Duration | Within budget | Orphans | Verdict |
|---|---|---|---|---|---|---|---|
| `surface_triage.ps1` | 10s | 30s | 0 | 3.99s | yes | 0 | **PASS** |
| `fleet_health.py` | 60s | 80s | killed (never returned) | >5 min (manually terminated) | **no** | 0 (clean after manual kill) | **FAIL** |
| `codespace_regime.py session-start` | 15s | 35s | 0 | ~1.3s | yes | 0 | **PASS** |
| `resource_lifecycle.py session-start` | 30s | 50s | 0 | ~1.1s | yes | 0 | **PASS** |
| `billing_leak_sentinel.ps1` | 10s | 30s | 0 | 3.98s | yes | 0 | **PASS**, with caveat (§2.1) |
| `conductor.py session-start` | 25s | 45s | 0 | ~1.1s | yes | 0 | **PASS** |
| `changelog_sentinel.py` | 20s | 40s | 0 | ~1.1s | yes | 0 | **PASS** |

Six of seven testable hooks finished well inside their declared budget with clean exits and no
surviving descendants. One did not.

### 2.1 · `fleet_health.py` — FAIL, and a second, more severe defect found underneath it

Run through the same command SessionStart uses, `fleet_health.py` printed one line —
`fleet_health: running cross-repo audit (stale or first run)...` — and then did not return. It was
still running, unchanged at that line, past its 80s kill bound and past a further ~4 minutes of
this lane's own wall-clock while other hooks were tested; it was then terminated by hand
(`Stop-Process -Force` on its **visible** process tree: two `bash.exe` layers, `uv.exe`, and two
`python.exe` layers). A follow-up sweep of that same process tree found zero survivors, and this
lane first recorded the kill as clean. **It was not.**

**What was actually still running, unkilled: `audit.py run`, a grandchild `fleet_health.py` spawns
by `subprocess.run` (`scripts/fleet_health.py::run_audit`, line 1240) whose own command line names
only `audit.py`, not `fleet_health.py`** — so this lane's kill, filtered on `CommandLine -like
'*fleet_health.py*'`, never matched it and never touched it. It kept running, undetected, for
roughly nine more minutes after the hook first printed its stall message (19:28 to ~19:37), across
five more of this lane's own tool calls, and completed on its own: six dated files appeared under
`ecosystem/*/history/2026-09-22.md` (one per registered sibling repo plus the hub itself) — the
exact g2 "detached descendant holds the pipe, no attachment, tool proceeds" pattern
`docs/audits/2026-09-16-technical-lane-ab-808-guard-timeout.md` §1.2 measured and named, now
reproduced directly rather than inferred from a silent gap in a transcript.

**Then it did something worse than run long: it deleted this lane's own in-progress work.**
`audit.py run`'s `_commit_routine_outputs` (`scripts/audit.py` line 6211) commits that run's
`docs/audits/` and `ecosystem/*/history/` output onto an orphan `automation/fleet-audit` branch via
a separate git index, then **restores the main working tree** on the stated assumption that "the
durable scope is clean going in (the automation invariant)" (its own docstring, line 6228). That
assumption does not hold during live operation: **this very audit document**, mid-draft and
untracked, was sitting under `docs/audits/` — the same pathspec the routine scans — when the
detached process finished. It was swept into the `git status --porcelain --untracked-files=all`
snapshot alongside `audit.py`'s own genuine output, committed onto `automation/fleet-audit` (commit
`1253eb35`, confirmed: `git show --stat automation/fleet-audit -- docs/audits/` lists this file,
167 lines added), and then **deleted from this working tree** by the same restore step, with no
warning and no confirmation — simply gone, discovered only because this lane happened to check
`git status` for an unrelated reason minutes later. It was recovered by hand from
`automation/fleet-audit` (`git show automation/fleet-audit:docs/audits/2026-09-22-technical-lane-hooks-rearm-live-measurement.md`)
and is the file being read now. Had this lane not separately re-checked the tree, the loss would
have gone unnoticed until commit time.

**Why this is a live defect, not a one-off accident of timing.** `docs/audits/` is where every
lane and every operator session in this repo writes its own in-progress audit records — it is not
a directory `audit.py` owns exclusively, and nothing marks a file inside it as "mine, do not
touch." Any session with an untracked, not-yet-committed file under `docs/audits/` — which is the
normal, expected state of a lane mid-draft on this very kind of document — is exposed to the same
loss if `fleet_health.py`'s cross-repo audit fires (SessionStart, on any stale cache) while that
file exists. This lane's own methodology (§1) explicitly chose not to spawn nested sessions to
avoid reproducing the orphaning risk; the risk showed up anyway, from the one hook this lane WAS
directed to test, and it turned out to carry a second, unrelated hazard the bypass-rate measurement
never named: **not just "silently permits the tool call", but "silently destroys untracked work
under `docs/audits/` that happens to be present when it completes."**

**Verdict: FAIL**, and more severely than the original framing. The timeout defect is in
`fleet_health.py`'s cross-repo audit path; the destructive-restore defect is in
`audit.py::_commit_routine_outputs`'s working-tree restore, reachable from `fleet_health.py`'s
SessionStart hook via `run_audit`. Both are out of this lane's footprint (`Files you own` names
only `.claude/settings.json`, its tests, and this wave's rows) and are not fixed here. **This
finding is escalated in the handback rather than resolved into a new task row by this lane** — see
§4 for why, and §5 for the escalation itself.

### 2.2 · `billing_leak_sentinel.ps1` — passes clean, one disclosed residual risk

This hook carries a double disable: the bypass-rate measurement (22%, over the bar) **and** a
separate naming in the 2026-09-17 emergency order alongside the two PreToolUse guards, whose
re-enable bar as originally stated was "a bounded, fail-open, loudly recorded execution time **and**
only once the suspended-at-creation cause is identified" (`.claude/settings.json`
`//hooks-EMERGENCY-DISABLED-2026-09-17`). That root cause was never identified
(`docs/audits/2026-09-16-technical-lane-ab-808-guard-timeout.md` §0.1, §7 — an open item, not
closed by any later record found in this repo).

**Why this lane arms it anyway, stated rather than silently overridden:**
`to-cc/RATIFICATION-2026-09-22-secrets-and-build-mode.md`, the same ruling that authorizes this
lane, states explicitly: "Guards switched off for reasons other than BUILD MODE (the 2026-09-17
emergency hook disable...) are not covered by O-2: they are re-armed **on their own evidence as the
first item of the next window**" — naming this lane's act, not a resolved root cause, as the
re-enable condition. The live test above is that evidence: real invocation of the exact hook
command through the same shell the harness uses, exit 0, 3.98s against a 10s budget, zero
surviving processes on an explicit before/after snapshot. **This does not mean the suspended-at-
creation defect is explained** — only that this specific script, run this way, today, did not
exhibit it. The residual risk is carried forward openly in the settings.json comment (§3) rather
than dropped.

## 3 · Verdicts

| Hook | Verdict | Action |
|---|---|---|
| `surface_triage.ps1` | PASS | armed; expiry marker removed |
| `surface-closures.ps1` | out of scope (§0.1) | stays disabled; expiry reset to 2026-12-21 (90 days) with a scope reason, not a retest date — nothing in this repo can retest it |
| `fleet_health.py` | FAIL, severe (§2.1) | stays disabled; new expiry 2026-09-29 (one week); reason: measured hang past 60s budget on the cross-repo-audit cold-cache path **plus** a detached `audit.py run` descendant that survives a process-tree kill and, on completion, silently deletes untracked work under `docs/audits/` via `_commit_routine_outputs`'s working-tree restore — a destructive-data-loss hazard, not just a timeout, escalated in the handback (§4) rather than resolved here |
| `codespace_regime.py session-start` | PASS | armed; expiry marker removed |
| `resource_lifecycle.py session-start` | PASS | armed; expiry marker removed |
| `billing_leak_sentinel.ps1` | PASS with disclosed residual (§2.2) | armed per the 2026-09-22 ratification; residual risk kept in the settings.json comment |
| `conductor.py session-start` | PASS | armed; expiry marker removed |
| `changelog_sentinel.py` | PASS | armed; expiry marker removed |

Six of eight come back. Two stay off, each with its own reason and its own dated marker — neither
is deleted, per the contract's "What NOT to do."

## 4 · What this lane does not do

- Does not touch BUILD MODE's guards (the two PreToolUse guards, the ADR-77 transcript guard) —
  those are O-2's set and stay off until BUILD MODE's own three conditions hold
  (`to-cc/RATIFICATION-2026-09-22-secrets-and-build-mode.md` O-2).
- Does not touch the Stop entries (`session_end_backpressure.py`, `lane_end_guard.py`,
  `propose_closures.py`) or `arm_hooks.py` — already active, not among the eight.
- Does not fix `fleet_health.py`'s cross-repo-audit slowness, nor `audit.py::_commit_routine_outputs`'s
  destructive working-tree restore (§2.1) — both are script-level defects inside files this lane
  does not own; kill-candidates below name why no new row is filed for either from inside this lane.

**kill-candidates: none, for two different reasons.** For the slowness leg: `[#808]` is the open
row that owns the nine measured-broken hooks as a class and already covers a defect found in one
of them; a second row would duplicate its scope. For the destructive-restore leg found in §2.1 —
materially different from slowness, and not one `[#808]`'s own scope names — **this lane does not
unilaterally file a new task row for it either.** ADR-111's decision funnel routes every audit
finding through exactly one of OWNED / DISCHARGED / CANDIDATE / REJECTED, and a CANDIDATE becomes
a task row only via intake (ADR-98) and ratification, not by an audit document declaring one for
itself. This finding is triaged **CANDIDATE** and surfaced in the handback for the operator to
route to intake — self-filing a row here would be exactly the unilateral act ADR-111 exists to
prevent, and would also reach outside `Files you own` (`.claude/settings.json`, its tests, and this
wave's rows only).
