#requires -Version 7
<#
.SYNOPSIS
  Caller-side dispatch shim -- the ONE place a lane is started. Shipped FROM the hub.

.DESCRIPTION
  THE HUB SHIPS THE CODE, THE CALLER RUNS IT (operator ruling 2026-09-19, BUILD-LIST
  "Dispatch / Layer 2"). CLAUDE.md section 5 rule 4: Layer 2 never executes. So the hub's
  scripts/dispatch.py never starts a lane; it PLANS one and GOVERNS one. This shim sits between
  the two and does the starting, from the CALLER's repo root -- the lane's worktree is created
  in the repo the operator is standing in, not in the hub:

    1. dispatch.py plan    contract -> JSON plan (argv, env delta, model + effort from the
                           CONTRACT). Every pre-launch refusal fires here.
    2. this shim           runs the plan's argv. Nothing about the argv is decided here.
    3. dispatch.py govern  lane id -> binds the lane's own usage by session id, stops the lane
                           past the cap, and refuses a launch whose usage cannot be bound.

  NO MODEL OR EFFORT DEFAULT ([#717]). Both come from the contract's `| Model | Mode | Effort |`
  table, or from -Model / -Effort when given. A contract with neither is REFUSED by `plan`.
  A default here would silently re-decide the most expensive constant on the line.

  The contract's `## Dispatch` block is never read or run.

  INSTALL. Copy this file over win-tooling's scripts\dev-terminals\bin\dispatch.ps1 (the PATH
  command); dispatch.cmd beside it needs no change. -TokenCap is mandatory: the old surface had
  none, and a budget written into a prompt caps nothing.

  NOT SUPPORTED, and refused rather than run ungoverned: the codespace substrate, and any plan
  whose metering is not `transcript` (codex, `claude -p`). A stream-metered lane needs a
  caller-side owner that can terminate the child; that is not built.

.PARAMETER ContractFile
  Path to a contract .md, or a bare file name resolved against the prompts directory.

.PARAMETER TokenCap
  REQUIRED. Tokens (input + output + cache-write) after which the lane is STOPPED.

.PARAMETER Model
  Overrides the contract's Model cell. No default.

.PARAMETER Effort
  Overrides the contract's Effort cell. No default.

.PARAMETER DryRun
  Print the plan and stop. Starts nothing.

.EXAMPLE
  dispatch LANE-wave3-dispatch-split.md -TokenCap 400000
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory, Position = 0)][string]$ContractFile,
    [Parameter(Mandatory)][int]$TokenCap,
    [string]$Slug,
    [string]$Provider = 'anthropic',
    [string]$Model,
    [string]$Effort,
    [switch]$CountCacheReads,
    [double]$Interval = 15,
    [switch]$DryRun,
    [string]$Hub = (Join-Path $HOME 'Documents\Dev\.dev-knowledge')
)

$ErrorActionPreference = 'Stop'
$DispatchPy = Join-Path $Hub 'scripts\dispatch.py'
if (-not (Test-Path -LiteralPath $DispatchPy)) {
    Write-Error "dispatch.py not found at $DispatchPy -- is the hub checked out there? (-Hub to override)"
    exit 2
}

# `--project $Hub` runs the hub's locked environment WITHOUT changing directory: the plan, the
# spawn and the governor all run from the caller's repo root.
function Invoke-Hub {
    param([string[]]$Verb)
    & uv run --locked --project $Hub python $DispatchPy @Verb
}

# --- 1. PLAN -------------------------------------------------------------------------------
$planArgs = @('plan', $ContractFile, '--token-cap', $TokenCap, '--provider', $Provider)
if ($Slug)   { $planArgs += @('--slug', $Slug) }
if ($Model)  { $planArgs += @('--model', $Model) }
if ($Effort) { $planArgs += @('--effort', $Effort) }
if (-not $DryRun) { $planArgs += '--emit-env' }   # the env values reach this process only

$planJson = Invoke-Hub $planArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$plan = ($planJson -join "`n") | ConvertFrom-Json

if ($DryRun) {
    Write-Host "[dispatch] slug=$($plan.slug) provider=$($plan.provider) model=$($plan.model) effort=$($plan.effort) token-cap=$($plan.token_cap)"
    Write-Host "[dispatch] $(($plan.argv | Select-Object -SkipLast 1) -join ' ')"
    Write-Host "[dispatch] prompt: $($plan.prompt)"
    exit 0
}
if ($plan.substrate -ne 'local' -or $plan.metering -ne 'transcript') {
    Write-Error ("Refusing: this shim starts only a local lane governed by its transcript " +
                 "(substrate=$($plan.substrate), metering=$($plan.metering)). Running it would " +
                 "leave the cap unenforced.")
    exit 2
}

# --- 2. SPAWN (the only spawn) -------------------------------------------------------------
# The env delta is applied to THIS process for the one call and put back afterwards: the
# operator's shell is never left changed.
$saved = @{}
foreach ($p in $plan.env_set.PSObject.Properties) {
    $saved[$p.Name] = [Environment]::GetEnvironmentVariable($p.Name)
    [Environment]::SetEnvironmentVariable($p.Name, [string]$p.Value)
}
foreach ($name in $plan.env_unset) {
    $saved[$name] = [Environment]::GetEnvironmentVariable($name)
    [Environment]::SetEnvironmentVariable($name, $null)
}
try {
    $exe, $rest = $plan.argv
    $started = (& $exe @rest | Out-String)
    $startCode = $LASTEXITCODE
}
finally {
    foreach ($name in $saved.Keys) { [Environment]::SetEnvironmentVariable($name, $saved[$name]) }
}
Write-Host $started.Trim()
if ($startCode -ne 0) {
    Write-Error "$exe exited $startCode -- no lane was started"
    exit $startCode
}

# The id is read from the start output; when it cannot be, `govern` FINDS the lane by its worktree
# (`.../worktrees/<slug>`) in `claude agents --json` rather than leaving a running lane ungoverned.
# PROVISIONAL either way: `govern` checks the bound lane's worktree against the slug and drops an
# id that belongs to another lane.
$found = [regex]::Match($started, '(?im)^\s*backgrounded\b[^0-9a-f\r\n]*([0-9a-f]{8})\b')
$laneArgs = if ($found.Success) { @($found.Groups[1].Value) } else { @() }

# --- 3. GOVERN -----------------------------------------------------------------------------
$governArgs = @('govern') + $laneArgs + @('--slug', $plan.slug, '--token-cap', $TokenCap, '--interval', $Interval)
if ($CountCacheReads) { $governArgs += '--count-cache-reads' }
Invoke-Hub $governArgs
exit $LASTEXITCODE
