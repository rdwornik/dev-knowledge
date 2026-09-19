# Wave-2 L3 — `scripts/dispatch.py`: the launcher moves into the hub, and the token cap gets a home

- lane: `wave2-dispatch` (Sonnet producer) · payload: `BATCH-night-wave2-FINAL-2026-09-19.md` §3 L3
- ruling: operator, MOVE plus language REWRITE — not a new design
- why: four sessions were ordered 180k tokens and used ~845k. A budget in a prompt caps nothing.

## 1. Prior art — a command and its output

```
$ git -C win-tooling ls-files | grep -i -E "dispatch|shim"      (launch surface only)
scripts/dev-terminals/bin/dispatch.ps1        77 lines   PATH entry; forwards to Invoke-Dispatch.ps1
scripts/dispatch/Invoke-Dispatch.ps1         565 lines   contract flow; Assert-ClaudeCommand at :281
config/dispatch-helpers/DispatchHelpers.psm1 3964 lines  Start-DispatchLane :170, Start-DispatchCodespace :2157,
                                                         Get-CloudModelProvider :3222, Start-CloudModelSession :3639
```

Read in full: `dispatch.ps1`, `Invoke-Dispatch.ps1` (head + contract flow), `Start-DispatchLane`,
`Get-DispatchPromptsDir` / `Resolve-DispatchPromptFile`, `Get-CloudModelProvider`,
`Start-CloudModelSession`, and the `Start-DispatchCodespace` synopsis. Read only by outline:
the cloud v2 / harvest / `Start-DispatchAfter` bodies (not on the cap's path, not moved).

Hub-side dependencies verified live: `click` is already a declared dependency (`pyproject.toml`);
`lane_cost.py` already reads per-turn usage from session transcripts and is reused, not rewritten.
`claude --help` has `--max-budget-usd` **print-mode only** and no token flag — so no CLI flag can
carry the cap; that is why a supervisor is the mechanism.

## 2. What moved, and what was chosen

| PowerShell | `scripts/dispatch.py` |
|---|---|
| `Start-DispatchLane` (ruled lane line, effort map, bypass, branch guard) | `build_plan`, `EFFORTS`, `branch_guard` |
| `Resolve-DispatchPromptFile` / `Get-DispatchPromptsDir` | `resolve_contract`, `prompts_dir` (whitespace = unset; unmounted authority drive = its own refusal; resolved lazily) |
| `Get-CloudModelProvider` / `Start-CloudModelSession` | `PROVIDERS`, `child_env` (scrub Anthropic creds, route base URL; env built for the child, so no restore `finally`) |
| `Start-DispatchCodespace` steps 2–5 | `codespace_plan` (create → read NAME back → ship files in → `bash <one token>` → receipt out) |
| `Assert-ClaudeCommand` (head must be `claude`) | structural: the head comes from `--provider`; `codex` is admitted; a contract's `## Dispatch` block is never executed |

**Not moved:** Anthropic-hosted cloud substrate, harvest, `Start-DispatchAfter`, the deep-code wrapper,
the Windows User-scope registry read of `CLAUDE_PROMPTS_DIR`, and Invoke-Dispatch's derived-line
fallback (Model/Effort table + filename). Also not moved: `Stop-DispatchCodespace` and the codespace
machine-type / identity-file options.

## 3. The cap — what it is and what it is not

- Required argument, no default; non-positive refuses. Counts input + output + cache-write; cache
  reads excluded unless `--count-cache-reads` (this session alone read 2.3M cache tokens).
- `claude --bg` lane: governor polls the lane transcript via `lane_cost.lane_usage` (minus a
  pre-launch baseline) and runs `claude stop <id>` past the cap.
- codex / codespace: stdout is stream-metered; the process is terminated past the cap.
- **Live evidence (this box, 2026-09-19):**

```
LIVE stream cap=5  -> Verdict(exceeded=True,  used=22471, cap=5,       polls=18) exit 3
LIVE stream cap=1M -> Verdict(exceeded=False, used=18482, cap=1000000, polls=53) exit 0
LIVE transcript read wave2-dispatch: capped=169346 (input 64 + output 31106 + cache_write 138176)
```

  The first line is the honest limit in one number: the cap was 5 and the run stopped at 22,471,
  because the first message alone carried ~20k cache-write tokens. **The cap is enforced at message
  granularity, never mid-message; thinking tokens land only in the final `result` event.**
- **Not verified live:** a `claude --bg` launch (it would create a worktree, forbidden to this lane),
  `claude stop`, the `claude agents --json` liveness probe (matches on the lane id as a substring —
  field names were not inspected), the codespace execution path (`--dry-run` only; live execution
  refuses with a message), and the `codex` stream path (event shape confirmed live with a one-word
  run; the terminate path is the same code as the claude stream path, run live above).
- Governing a `--bg` lane means this process stays up. Ctrl-C leaves the lane uncapped and says so.

## 4. Layer-2 tension, recorded not resolved

CLAUDE.md §5 rule 4: "Layer 2 never executes — no script drives state in a child repo (ADR-28,
ADR-36)." A launcher that starts sessions is closer to that line than any validator. The operator
ruled the MOVE, so it landed; the boundary is kept by construction (it starts a lane and stops it;
it never writes into a child repo), but the operator/architect should confirm the reading of rule 4
when this merges. [#582]/[#602] (the ruled dispatch verb) and [#669]/[#689] (phase movement) were
neither read nor closed by this lane.

## 5. The win-tooling shim — CONTENT ONLY (that repo was not edited)

Replace the body of `scripts/dev-terminals/bin/dispatch.ps1` so the PATH command keeps working and
delegates to the hub. `-TokenCap` becomes mandatory — the old surface had none.

```powershell
#requires -Version 7
[CmdletBinding()]
param(
    [Parameter(Mandatory, Position = 0)][string]$ContractFile,
    [Parameter(Mandatory)][string]$Slug,
    [Parameter(Mandatory)][int]$TokenCap,
    [string]$Provider = 'anthropic',
    [string]$Model = 'opus',
    [string]$Effort = 'medium',
    [ValidateSet('local', 'codespace')][string]$Substrate = 'local',
    [string]$Repo,
    [switch]$DryRun
)
$Hub = Join-Path $HOME 'Documents\Dev\.dev-knowledge'
if (-not (Test-Path (Join-Path $Hub 'scripts\dispatch.py'))) {
    Write-Error "dispatch.py not found under $Hub -- is the hub checked out there?"; exit 2
}
$argv = @('run', '--locked', 'python', 'scripts/dispatch.py', 'launch', $ContractFile,
          '--slug', $Slug, '--token-cap', $TokenCap, '--provider', $Provider, '--model', $Model,
          '--effort', $Effort, '--substrate', $Substrate)
if ($Repo) { $argv += @('--repo', $Repo) }
if ($DryRun) { $argv += '--dry-run' }
Push-Location $Hub
try { & uv @argv; exit $LASTEXITCODE } finally { Pop-Location }
```

Caveats for whoever applies it: `Push-Location $Hub` runs `uv` in the hub, but `claude --worktree`
creates the worktree in the **current** repo — a lane meant for a child repo must run from that repo,
so use `uv run --locked --project $Hub python "$Hub\scripts\dispatch.py" …` instead of `Push-Location`
when dispatching outside the hub (untested here). `dispatch.cmd` needs no change. Keep
`DispatchHelpers.psm1` until the cloud substrate is either moved or retired; the shim above does not
replace `Start-DispatchCloudV2`.

## 6. rejected-alternatives

- **A `--max-budget-usd` flag:** print-mode only; cannot cap a `--bg` lane, and dollars are not the order.
- **A hard ceiling on the cap (e.g. refuse > 2M):** would be an invented policy number; the ordered
  figure is the operator's, so the launcher only refuses absent / non-positive.
- **Reading the contract's `## Dispatch` block:** Invoke-Dispatch's central feature. Dropped: it is
  the arbitrary-execution surface `Assert-ClaudeCommand` existed to fence, and the cap needs the
  launcher to own the argv.
- **Porting the whole 3,964-line module:** most of it (cloud v2, harvest, After) is off the cap's path.
- **Counting cache reads in the cap by default:** makes any realistic cap void; kept behind a flag.
- **Mutating `os.environ` and restoring it (the PS approach):** the child gets its own dict.

## 7. anti-claims

- This does **not** make the cap airtight: overshoot up to one message (stream) or one poll interval
  (transcript) is expected and was measured (22,471 against a cap of 5).
- A green test run does **not** show a live `--bg`, `claude stop` or codespace launch works.
- `codex` lanes are branch-named by codex's own `--worktree`, not `worktree-<slug>`; `branch_guard`
  does not cover them.
- Nothing here closes or advances any BACKLOG row; the win-tooling repo was not touched.

## 8. Codex terra review of the first cut (4 CRITICAL / 2 HIGH) — all six fixed, RED-first

`docs/audits/2026-09-19-codex-wave2-dispatch.md`. Each finding got a failing test before its fix
(5 tests red, then 28/28 green):

- other providers' API keys leaked into a third-party child -> every other provider's key is scrubbed;
- a missing transcript read as zero spend -> `None` = unobservable; 8 blind polls = UNGOVERNED (exit 4);
- a failed `claude stop` reported as a stop -> `stop_failed`, exit 4, message says the lane may still run;
- an unreadable `claude agents --json` read as "lane finished" -> `GovernorBlind` = UNGOVERNED;
- a failed streamed child exited 0 -> its own exit code is propagated;
- codex counts usage only at `turn.completed` -> not fixable by code (no incremental source); now
  LABELLED "post-hoc per completed turn" in the plan output and the module docstring.

Not done: an unobservable lane is reported, not killed (killing destroys work to report a gap).
The re-review of the fixed commit is recorded in the handback, not here.

no-consumer: lane output awaiting integrator merge (night wave 2, L3); it files and closes no BACKLOG row, so no [#id] cites it yet.

## 9. Codex RE-review of the fixed commit (2 CRITICAL / 2 HIGH) — fixed RED-first, NOT re-reviewed

`docs/audits/2026-09-19-codex-wave2-dispatch-rereview.md`. Four tests red, then 33/33 green:

- a stream with no parseable usage exited "under cap" -> UNGOVERNED (exit 4);
- `proc.terminate()` was never verified -> terminate, then kill, then check `poll()`; a survivor is `stop_failed`;
- `claude stop` / `claude agents --json` had no timeout or OSError handling -> `_control()` bounds both at 30 s and maps a hang to failed-stop / `GovernorBlind`;
- a `--bg` lane's transcript may not be filed under the slug -> `--slug-dir` (repeatable) is passed to the baseline and the poll. **This is the one finding only partly closed:** whether a real `--bg --worktree` lane files under the slug directory was NOT verified (it needs a live launch and a worktree). Unbound, the governor reports UNGOVERNED after 8 blind polls rather than "under cap" — it fails loud, it does not enforce.

No third review pass was run: that round's fixes carry tests, not a reviewer's word.
