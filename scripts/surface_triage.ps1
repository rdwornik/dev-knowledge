# SessionStart surfacing for nightly-triage Issues (Phase C4 / ADR-68 outcome loop).
#
# Mirrors the L0 surface-closures.ps1 pattern: READ-ONLY, fail-soft, ALWAYS exit 0,
# silent when gh is absent / unauthenticated / offline or when no triage Issues are
# open. Prints a single "[triage] ..." line when open `nightly-triage` Issues exist.
# This is a surfacing nudge only — it never blocks or noises the session.

$ErrorActionPreference = 'SilentlyContinue'
try {
    # Resolve gh: PATH first, then the default Windows install location as a fallback
    # (the SessionStart shell does not always inherit an updated PATH).
    $gh = (Get-Command gh -ErrorAction SilentlyContinue).Source
    if (-not $gh) {
        $fallback = Join-Path $env:ProgramFiles 'GitHub CLI\gh.exe'
        if (Test-Path -LiteralPath $fallback) { $gh = $fallback }
    }
    if (-not $gh) { exit 0 }

    # Resolve the repo from the project dir (gh reads the cwd's git remote).
    $dir = $env:CLAUDE_PROJECT_DIR
    if ($dir -and (Test-Path -LiteralPath $dir)) { Set-Location -LiteralPath $dir }

    $json = & $gh issue list --label nightly-triage --state open --json number,title 2>$null
    if (-not $json) { exit 0 }

    $issues = @($json | ConvertFrom-Json)
    if ($issues.Count -gt 0) {
        $nums = ($issues | ForEach-Object { "#$($_.number)" }) -join ', '
        $word = if ($issues.Count -eq 1) { 'finding' } else { 'findings' }
        Write-Output "[triage] $($issues.Count) nightly $word await: $nums -- see the Issues tab."
    }
} catch {
    # never block or noise the session on a surfacing failure
}
exit 0
