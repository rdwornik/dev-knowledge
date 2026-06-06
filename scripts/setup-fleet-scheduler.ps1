<#
.SYNOPSIS
    Register (or update in place) the local fleet-baseline scheduled task.

.DESCRIPTION
    ADR-76 host for the recurring Tier-2 fleet-baseline run: Windows Task
    Scheduler -> `python scripts/fleet_health.py` directly. No `claude -p` / no
    LLM on the scheduled path (ADR-76 decision 1/2). LLM interpretation, if
    wanted, is attached at the next interactive SessionStart via the existing
    SessionStart-throttled trigger -- which stays live during validation
    (ADR-76 decision 5; do not remove it here).

    The task is read-only with respect to the repo's tracked content: it only
    runs the Python collector, which writes the gitignored logs/FLEET-HEALTH.md
    digest (and refreshes ecosystem/<name>/state.yaml, as the audit already does
    at SessionStart). No wake-from-sleep, no alerting -- missed runs are tolerated
    by design (ADR-76 decision 3 / ADR-74 rider R2): Task Scheduler's built-in
    "run as soon as possible after a missed start" catches up, and stale data is
    surfaced at the next interactive SessionStart.

    Idempotent: re-running overwrites the existing registration in place
    (-Force). PS 5.1-compatible (no PS7-only syntax).

.PARAMETER At
    Daily trigger time (local). Default 09:00.

.PARAMETER PythonExe
    Python interpreter for the action. Default: the interpreter resolved from
    `python -c "import sys;print(sys.executable)"` on PATH.

.PARAMETER DryRun
    Print the planned registration and exit without registering or exporting.

.PARAMETER XmlOut
    Path to export the registered task XML. Default scripts/fleet-baseline.task.xml.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts/setup-fleet-scheduler.ps1
.EXAMPLE
    powershell -File scripts/setup-fleet-scheduler.ps1 -At 06:30 -DryRun
#>
[CmdletBinding()]
param(
    [string]$At = "09:00",
    [string]$PythonExe = "",
    [switch]$DryRun,
    [string]$XmlOut = ""
)

$ErrorActionPreference = "Stop"

$TaskPath = "\DevKnowledge\"
$TaskName = "fleet-baseline"

function Fail($msg) {
    Write-Error "setup-fleet-scheduler: $msg"
    exit 1
}

# --- Resolve paths ----------------------------------------------------------
$ScriptsDir = $PSScriptRoot
$RepoRoot   = Split-Path -Parent $ScriptsDir
$Collector  = Join-Path $ScriptsDir "fleet_health.py"

if (-not (Test-Path $Collector)) { Fail "collector not found: $Collector" }

if (-not $XmlOut) { $XmlOut = Join-Path $ScriptsDir "fleet-baseline.task.xml" }

# Resolve the Python interpreter (absolute path) the action will hardcode.
if (-not $PythonExe) {
    try {
        $PythonExe = (& python -c "import sys;print(sys.executable)" 2>$null).Trim()
    } catch {
        $PythonExe = ""
    }
}
if (-not $PythonExe -or -not (Test-Path $PythonExe)) {
    Fail "could not resolve a Python interpreter; pass -PythonExe <abs path>"
}

# Parse the -At time (HH:mm) into a concrete trigger time-of-day.
try {
    $trigTime = [datetime]::ParseExact($At, "HH:mm", $null)
} catch {
    Fail "invalid -At '$At'; expected 24h HH:mm (e.g. 09:00)"
}

$UserId = "$env:USERDOMAIN\$env:USERNAME"

Write-Host "Planned fleet-baseline task:"
Write-Host "  TaskPath/Name : $TaskPath$TaskName"
Write-Host "  Trigger       : Daily @ $At (local)"
Write-Host "  Action        : $PythonExe $Collector"
Write-Host "  WorkingDir    : $RepoRoot"
Write-Host "  Principal     : $UserId (Interactive, RunLevel Limited; no stored credentials)"
Write-Host "  Settings      : StartWhenAvailable=ON, WakeToRun=OFF, OnBatteries=allowed,"
Write-Host "                  MultipleInstances=IgnoreNew, ExecutionTimeLimit=15min"
Write-Host "  XML export    : $XmlOut"

if ($DryRun) {
    Write-Host ""
    Write-Host "[dry-run] not registering and not exporting XML."
    exit 0
}

# --- Build task components --------------------------------------------------
$action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$Collector`"" -WorkingDirectory $RepoRoot

$trigger = New-ScheduledTaskTrigger -Daily -At $trigTime

# StartWhenAvailable = catch up a missed start (ADR-76 #3). WakeToRun is left
# OFF (switch absent). Battery starts allowed; do not stop on battery.
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 15)

# Run only when the user is logged on: interactive token, no stored password.
$principal = New-ScheduledTaskPrincipal -UserId $UserId -LogonType Interactive -RunLevel Limited

# --- Register (idempotent: -Force overwrites in place) ----------------------
try {
    $null = Register-ScheduledTask `
        -TaskName $TaskName -TaskPath $TaskPath `
        -Action $action -Trigger $trigger -Settings $settings -Principal $principal `
        -Description "ADR-76 Tier-2 fleet-baseline: python scripts/fleet_health.py (read-only collector; no LLM). Missed runs catch up; no wake." `
        -Force
} catch {
    Fail "Register-ScheduledTask failed: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "Registered $TaskPath$TaskName."

# --- Export XML snapshot ----------------------------------------------------
try {
    $xml = Export-ScheduledTask -TaskName $TaskName -TaskPath $TaskPath
    # Export-ScheduledTask stamps the declaration encoding as UTF-16; we persist
    # UTF-8 (no BOM) for a clean git diff, so rewrite the declaration to match the
    # actual bytes (otherwise a parser trusts the wrong declared encoding).
    $xml = $xml -replace 'encoding="UTF-16"', 'encoding="UTF-8"'
    [System.IO.File]::WriteAllText($XmlOut, $xml, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "Exported task XML -> $XmlOut"
} catch {
    Fail "Export-ScheduledTask failed: $($_.Exception.Message)"
}

exit 0
