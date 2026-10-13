# Lane bw-1001-sessionstart-one — the SessionStart injections, measured, and the one bounded entry that replaces them

**Lane:** `lane-bw-1001-sessionstart-one` · **Branch:** `worktree-lane-bw-1001-sessionstart-one` · **Batch:** BW (wave C) · **Date:** 2026-10-13

Consumers: [#1001] (this lane's row; the contract is
`docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1001-sessionstart-one.md`).

## 0 · The true count is NINE

`.claude/settings.json` at `26bd4d93` (the lane's base) registered **nine** SessionStart
commands in one group: `arm_hooks.py`, `surface_triage.py`, `changelog_sentinel.py`,
`conductor.py session-start`, `resource_lifecycle.py session-start`,
`codespace_regime.py session-start`, `billing_leak_sentinel.py`, `fleet_health.py`,
`hooks/quota_daily.py`. `CLAUDE.md` §9 says "8 SessionStart" and lists eight: it omits
`quota_daily.py`, which `LANE-5B3-2-wire-quota-distiller` added as the ninth. The order's "9"
is the true number.

Outside this repo, measured the same day: the user-level `~/.claude/settings.json` carries
**no** `SessionStart` array (its only hook is a `Notification` entry), the `tier1-lifecycle`
plugin's `hooks/hooks.json` declares only `Stop`, and there is no machine-wide managed settings
file (`C:\ProgramData\ClaudeCode\` does not exist). So no SessionStart reader on this box runs
from outside the repo. The `[hook-ADVISORY] ... registered outside this repo` lines that
`fleet_health.py` prints (`cmd:billing_leak_sentinel.py`, `cmd:quota_daily.py`,
`cmd:surface_triage.py`, ...) are history in the transcript store, keyed `cmd:<script>` because
no posture matched them when they were recorded. They do not mark a live outside registration.
`surface-closures.ps1` is wired nowhere today. No operator edit to `~/.claude/` is needed.

## 1 · Method

- **Box:** the operator's Windows 11 machine (16 logical CPUs), Git Bash, uv 0.11.19, CPython 3.12.10.
- **How a reader was run:** the exact `command` string from `.claude/settings.json`, through
  `C:\Program Files\Git\bin\bash.exe -c`, with `CLAUDE_PROJECT_DIR` set to the worktree root,
  cwd at the worktree root, and the stdin payload
  `{"hook_event_name": "SessionStart", "source": "startup"}`. The payload carries no `session_id`,
  so `seat_registry` writes nothing. This is how Claude Code runs a hook. No Claude Code session
  was started in a loop.
- **Bytes injected** = the command's stdout, the stream Claude Code folds into context. stderr is
  recorded separately.
- **p90** = nearest rank over the runs: the maximum at 5 runs, the 6th of 7 at 7 runs.
- The harness was a throwaway script in the orchestrator's scratch directory, not committed
  (no new home was named for it). Its logic is described above in full.

## 2 · Before, per entry (5 runs each, one at a time)

| entry | stdout bytes (median) | p50 s | p90 s |
|---|---|---|---|
| `arm_hooks.py` | 0 (69 on the first run: it armed `merge.ours.driver`) | 2.11 | 6.29 |
| `surface_triage.py` | 0 | 5.45 | 6.25 |
| `changelog_sentinel.py` | 81 | 4.41 | 4.82 |
| `conductor.py session-start` | 434 | 5.96 | 6.00 |
| `resource_lifecycle.py session-start` | 240 | 5.02 | 6.01 |
| `codespace_regime.py session-start` | 53 | 1.55 | 1.75 |
| `billing_leak_sentinel.py` | 0 | 1.45 | 1.50 |
| `fleet_health.py` | 9,222 | 9.21 | 10.38 |
| `hooks/quota_daily.py` | 96 | 2.38 | 2.45 |
| **total** | **10,126** | (sum of p50s 37.54) | |

`billing_leak_sentinel.py` does almost nothing (one environment read), so its 1.45 s p50 is
about the cost of `uv run --locked python` starting up on this box. Nine entries paid that cost
nine times.

**Before, as Claude Code runs them** (all nine started at once, wall time until the last one
exits, 7 runs, measured in a detached checkout of `26bd4d93`): **p50 15.00 s, p90 15.35 s**,
9,954 to 10,023 bytes of stdout in total.

## 3 · After — one entry, one interpreter

`.claude/settings.json` registers ONE SessionStart command:
`scripts/hooks/session_start.py`, run through the shared launcher
`scripts/hooks/hook_launcher.py` with timeout 60. It imports the nine readers and runs each one's
own entry point on a separate thread. Each reader's stdout and stderr are captured on its own
thread. The output is composed in a fixed reader order, and the result is bounded:
`OUTPUT_CAP_BYTES = 8192` for the whole stdout and `LINE_CAP_BYTES = 240` for each line.
Overflow is cut from the end, but never a line tagged as a refusal or a warning.

**7 runs, same method:** **p50 12.36 s, p90 14.16 s** (max 17.05 s). Stdout is **6,557 bytes**
on every run, so the bound holds: the 9,222-byte `fleet_health.py` block shrinks because each
long `[hook-BROKEN]` / `[hook-ADVISORY]` line is shortened to 240 bytes. No line was dropped,
and every tag of the nine readers is present.

**Dropped readers:** none. `session_start.DROPPED` is empty. All nine run.

## 4 · The 2-second p90 — NOT MET, and why

Measured p90: **14.16 s**, against a target under 2 s. The cause has two parts, and this lane
can remove neither:

1. **Startup floor, about 2 s.** Starting `uv run --locked python` costs 1.45 s p50 (see
   `billing_leak_sentinel.py` above). The shared launcher then adds two `git rev-parse`
   subshells; its own docstring measured 1.70 s against 2.30 s for that shape. Together that
   is already about 2 s before any reader runs a line.
2. **CPU inside one GIL.** Each reader was run alone, in-process (wall / CPU seconds):
   `fleet_health` 6.41 / 5.28, `conductor` 4.02 / 2.00, `surface_triage` 3.35 / 0.20,
   `resource_lifecycle` 2.85 / 0.05, `changelog_sentinel` 2.37 / 0.67, all others ≤ 0.42 / 0.12.
   Threads overlap the waiting: gh, the version probes and the process table. They cannot
   overlap the roughly 8.4 s of Python CPU, which one interpreter runs serially. Inside
   `fleet_health`, `funnel_health_line` takes 3.71 s and `seat_health_line` 1.22 s (profiled
   section by section).

The one-interpreter shape is still faster than the nine concurrent processes it replaces
(p90 15.35 s → 14.16 s). It also injects 35% fewer bytes (10,126 → 6,557). To get under 2 s,
the CPU-heavy digest lines would have to be computed off the boot path: the `[#962]`
reader/producer split, applied to `funnel` / `seats` / the conductor phase gate, so that
SessionStart only reads a cached digest. Those modules are outside this lane's footprint. This
is recorded as the follow-up, not attempted here.

## 5 · R8 usage test — Copilot CLI, at the worktree root

`copilot -p "<report any SessionStart-injected text>" --allow-all-tools --log-level debug`
(GitHub Copilot CLI 1.0.96, served model `claude-sonnet-5.5`, session
`ab8df310-25dd-49b1-a09b-7583f314055f`):

- Copilot loaded the repo hooks ("loaded repo hooks (hookCount=6)"). It ran the ONE SessionStart
  entry through the launcher, under its own shell and with no `CLAUDE_PROJECT_DIR`.
  `hook.start` to `[hook stdout]` took about 11.6 s.
- **Injected SessionStart text size: 6,579 bytes, 50 lines.** That is the hook's stdout as
  Copilot's debug log records it. All nine readers' tags are present, from `[prompts]` through
  `[quota]`.
- Copilot **did not fold that stdout into the model's context**: the model answered "NONE", and
  the session transcript carries no hook text. Under Copilot the entry runs and is bounded, but
  its text reaches the debug log, not the model.
