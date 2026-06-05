# SessionStart surfacing for nightly-triage Issues (Phase C4 / ADR-68 outcome loop).
#
# Mirrors the L0 surface-closures.ps1 pattern: READ-ONLY, fail-soft, ALWAYS exit 0,
# silent when gh is absent / unauthenticated / offline or when no triage Issues are
# open. Prints a single "[triage] ..." line when open `nightly-triage` Issues exist.
# This is a surfacing nudge only — it never blocks or noises the session.
#
# verify: with zero open `nightly-triage` Issues, running this under Windows
#   PowerShell 5.1 (`powershell -File scripts/surface_triage.ps1`, the hook's
#   actual runtime) prints NOTHING and exits 0 — not "[triage] 1 ... await: #".
#   With N open, it prints "[triage] N nightly finding(s) await: #a, #b ...".

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

    # Two Windows PowerShell 5.1 traps (the SessionStart hook runs under 5.1,
    # NOT pwsh 7 -- both are real and were masking each other):
    #  (1) Empty result: `'[]' | ConvertFrom-Json` piped on yields a 1-element
    #      $null array, so an EMPTY gh result printed the bogus banner
    #      "[triage] 1 nightly finding await: #" (Count=1, .number empty).
    #  (2) Non-empty result: ConvertFrom-Json does NOT unroll a root JSON array
    #      into the pipeline, so `... | ConvertFrom-Json | Where-Object` sees the
    #      whole array as ONE item and miscounts N issues as 1.
    # Fix for both: ASSIGN the parse to a variable first (it becomes Object[]),
    # THEN filter that array element-wise, keeping only real entries (.number
    # set). Now 0 open -> no banner; N open -> correct N + issue numbers.
    # (pwsh 7 is unaffected by either trap; this is correct on both.)
    $parsed = $json | ConvertFrom-Json
    $issues = @($parsed | Where-Object { $_ -and $null -ne $_.number })
    if ($issues.Count -gt 0) {
        $nums = ($issues | ForEach-Object { "#$($_.number)" }) -join ', '
        $word = if ($issues.Count -eq 1) { 'finding' } else { 'findings' }
        Write-Output "[triage] $($issues.Count) nightly $word await: $nums -- see the Issues tab."
    }
} catch {
    # never block or noise the session on a surfacing failure
}
exit 0
