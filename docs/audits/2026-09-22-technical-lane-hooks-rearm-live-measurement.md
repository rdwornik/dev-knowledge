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

### 2.1 · `fleet_health.py` — the one measured failure, and its cause

Run through the same command SessionStart uses, `fleet_health.py` printed one line —
`fleet_health: running cross-repo audit (stale or first run)...` — and then did not return. It was
still running, unchanged at that line, past its 80s kill bound and past a further ~4 minutes of
this lane's own wall-clock while other hooks were tested; it was then terminated by hand
(`Stop-Process -Force` on its full process tree: two `bash.exe` layers, `uv.exe`, and two
`python.exe` layers). A follow-up sweep of the same process tree found zero survivors — the kill
was clean — but the hook itself did not self-bound, which is the fail criterion regardless of
cleanup. This independently reproduces and explains the 41% bypass rate the 2026-09-16 measurement
found: on a "stale or first run" cache state, the cross-repo audit path this hook runs can take
minutes, far past its declared 60s, and the harness's own `timeout` then fails it open silently —
exactly the mechanism `docs/audits/2026-09-16-technical-lane-ab-808-guard-timeout.md` §1.2 describes.
**Verdict: FAIL.** The fix is in `fleet_health.py`'s cross-repo audit path (a cache/timeout defect
inside the script), which is out of this lane's footprint (`Files you own` names only
`.claude/settings.json`, its tests, and this wave's rows) — filed as a fresh dated disable, not a
new task row (the row would duplicate `[#808]`'s open scope; see kill-candidates below).

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
| `fleet_health.py` | FAIL (§2.1) | stays disabled; new expiry 2026-09-29 (one week); reason: measured hang past 60s budget on the cross-repo-audit cold-cache path, cause identified, fix out of this lane's footprint |
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
- Does not fix `fleet_health.py`'s cross-repo-audit slowness — that is a script-level defect inside
  a file this lane does not own; kill-candidates below name why no new row is filed for it.

**kill-candidates for a `fleet_health.py` cross-repo-audit fix: none — `[#808]` is the open row
that owns the nine measured-broken hooks as a class and already covers a defect found in one of
them; a second row would duplicate its scope.**
