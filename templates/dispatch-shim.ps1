#requires -Version 7
<#
.SYNOPSIS
  Thin PowerShell wrapper over `scripts/dispatch.py launch` -- one command launches a lane.
  Shipped FROM the hub; NOT deployed by the lane that wrote it (an operator act).

.DESCRIPTION
  All of the logic lives in scripts/dispatch.py. This file only turns PowerShell parameters into
  one `dispatch.py launch ...` call and hands back its exit code. It hard-codes no lane line, no
  model and no effort, and it has no path that can end a run.

  dispatch.py has five subcommands (`dispatch.py --help` describes each; `-Help` here runs it):

    launch  <contract>   what this shim runs. Reads the contract's Dispatch block, runs
                         `doit moment:pre-launch` for the lane (occupancy, live integrator,
                         routing agreement), and only on a pass spawns a background `claude` job
                         named `-n <slug>` (or `codex exec` when the contract names it), then writes a launch
                         receipt and a job-to-lane record under logs/receipts/. A refusal spawns
                         nothing and exits 5 with the reason.
    govern  <slug>       a MONITOR, run by hand: `dispatch.py govern --slug <slug>`. Records the
                         lane's spend against the cap field. It never stops, pauses or kills a lane.
    plan    <contract>   prints the launch plan as JSON and starts nothing (harness stage 11).
    queue   <contracts>  the launch order (priority, Starts after, serialize-group, substrate),
                         and, unless --dry-run, one pass or a bounded --watch loop firing whatever
                         clears the dependency/cap/RAM gates. Not wrapped by this shim -- run
                         `dispatch.py queue` directly.
    repair  <slug> <contract>   relaunch a repair into slug's EXISTING worktree, never a fresh
                         `--worktree`. Not wrapped by this shim -- run `dispatch.py repair` directly.

  Model and effort come from the contract (its Dispatch block or its `| Model | Mode | Effort |`
  table) or from -Model / -Effort. There is no default and no cap argument: -TokenCap is optional
  and only WRITES the cap field into the launch receipt.

.PARAMETER ContractFile
  Path to a contract .md, or a bare file name resolved against the prompts directory.

.PARAMETER Slug
  Overrides the lane slug. Default: the Dispatch block's -n / --worktree.

.PARAMETER Provider
  Overrides the Dispatch block's head (claude -> anthropic, codex -> codex).

.PARAMETER Model
  Overrides the contract's model. No default.

.PARAMETER Effort
  Overrides the contract's effort. No default.

.PARAMETER Batch
  The batch the lane joins; pre-launch checks that batch's integrator is live.

.PARAMETER TokenCap
  Optional. Recorded in the launch receipt as the cap field. It stops nothing.

.PARAMETER DryRun
  Print the resolved request as JSON and start nothing (pre-launch is not run).

.PARAMETER Run
  Launch. This is the default; the switch is kept so `dispatch <file> -Run` keeps working.

.PARAMETER Help
  Print `dispatch.py --help` (every subcommand) and exit.

.EXAMPLE
  dispatch LANE-W3-B-launch-adapter.md -Batch wave3 -DryRun

.EXAMPLE
  dispatch LANE-W3-B-launch-adapter.md -Batch wave3 -Run
#>
[CmdletBinding(DefaultParameterSetName = 'Launch')]
param(
    [Parameter(ParameterSetName = 'Launch', Mandatory, Position = 0)][string]$ContractFile,
    [Parameter(ParameterSetName = 'Help', Mandatory)][switch]$Help,
    [Parameter(ParameterSetName = 'Launch')][string]$Slug,
    [Parameter(ParameterSetName = 'Launch')][string]$Provider,
    [Parameter(ParameterSetName = 'Launch')][string]$Model,
    [Parameter(ParameterSetName = 'Launch')][string]$Effort,
    [Parameter(ParameterSetName = 'Launch')][string]$Batch,
    [Parameter(ParameterSetName = 'Launch')][int]$TokenCap,
    [Parameter(ParameterSetName = 'Launch')][switch]$DryRun,
    [Parameter(ParameterSetName = 'Launch')][switch]$Run,
    [string]$Hub = (Join-Path $HOME 'Documents\Dev\.dev-knowledge')
)

$ErrorActionPreference = 'Stop'
$DispatchPy = Join-Path $Hub 'scripts\dispatch.py'
if (-not (Test-Path -LiteralPath $DispatchPy)) {
    Write-Error "dispatch.py not found at $DispatchPy -- is the hub checked out there? (-Hub to override)"
    exit 2
}

# `--project $Hub` runs the hub's locked environment WITHOUT changing directory, so the lane is
# spawned from the caller's repo root.
[string[]]$verb = if ($Help) { '--help' } else { 'launch', $ContractFile }
if (-not $Help) {
    if ($Slug)     { $verb += @('--slug', $Slug) }
    if ($Provider) { $verb += @('--provider', $Provider) }
    if ($Model)    { $verb += @('--model', $Model) }
    if ($Effort)   { $verb += @('--effort', $Effort) }
    if ($Batch)    { $verb += @('--batch', $Batch) }
    if ($PSBoundParameters.ContainsKey('TokenCap')) { $verb += @('--token-cap', $TokenCap) }
    if ($DryRun)   { $verb += '--dry-run' }
}
& uv run --locked --project $Hub python $DispatchPy @verb
exit $LASTEXITCODE
