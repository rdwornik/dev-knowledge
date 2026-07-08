# SessionStart surfacing for the nightly conformance loop (Phase C4 / ADR-68).
#
# Mirrors the L0 surface-closures.ps1 pattern: READ-ONLY, fail-soft, ALWAYS exit 0,
# silent on the happy path (gh absent / offline, or nothing to report). Surfaces
# two things, each only when there is something to say:
#   [gh]      — gh auth is invalid/expired (operator-recoverable ONLY; surfaces the
#               refresh command, then skips the gh-dependent checks below)
#   [triage]  — open `nightly-triage` Issues await review
# This is a surfacing nudge only — it never blocks or noises the session.
#
# RETIRED 2026-07-09 (#255): the two [nightly] conformance-run-health surfacings (the
# "Nightly Conformance Triage" Action-run check + the automation/conformance-digest
# branch digest-presence check) were removed with the conformance-digest mechanism — a
# PR-triggered organ under a local-merge workflow was vacuous (it never fired). The
# successor surface for fleet health is the local scripts/fleet_health.py SessionStart digest.
#
# verify: under Windows PowerShell 5.1 (`powershell -File scripts/surface_triage.ps1`,
#   the hook's actual runtime) with zero open `nightly-triage` Issues it prints NO
#   "[triage]" line (not "[triage] 1 ... await: #"); with N open it prints
#   "[triage] N nightly finding(s) await: #a, #b ...". On the all-green happy path it
#   prints nothing, exit 0.
#   With an invalid/expired gh token (`gh auth status` exits non-zero) it prints
#   exactly "[gh] auth invalid -- run: gh auth refresh -h github.com" and skips the
#   gh-dependent checks (exit 0) -- it does NOT fall through to a false all-clear.

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

    # --- Leading gate: gh auth must be valid ---------------------------------
    # gh auth failures are operator-recoverable ONLY -- the device/OAuth flow
    # needs a human, so a session can never fix an expired/invalid token by
    # retrying. Surface the exact recovery command and skip every gh-dependent
    # check below (fail-soft, exit 0). `gh auth status` exits non-zero when no
    # host is authenticated or the token is invalid/expired. Do NOT swallow it
    # as a silent no-op -- that masks a skipped nightly behind a false all-clear.
    # (LESSONS 2026-06-06, gh-auth failure class; durable fix = long-expiry PAT.)
    $null = & $gh auth status 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Output "[gh] auth invalid -- run: gh auth refresh -h github.com"
        exit 0
    }

    # Resolve the repo from the project dir (gh reads the cwd's git remote).
    $dir = $env:CLAUDE_PROJECT_DIR
    if ($dir -and (Test-Path -LiteralPath $dir)) { Set-Location -LiteralPath $dir }

    # --- Surfacing 1: open nightly-triage Issues -----------------------------
    # NOTE: do NOT early-exit when there are zero open issues -- the nightly
    # run-health checks below must run on every session, and zero open triage
    # issues is the common case.
    $json = & $gh issue list --label nightly-triage --state open --json number,title 2>$null
    if ($json) {
        # Two Windows PowerShell 5.1 traps (the SessionStart hook runs under 5.1,
        # NOT pwsh 7 -- both are real and were masking each other):
        #  (1) Empty result: `'[]' | ConvertFrom-Json` piped on yields a 1-element
        #      $null array, so an EMPTY gh result printed the bogus banner
        #      "[triage] 1 nightly finding await: #" (Count=1, .number empty).
        #  (2) Non-empty result: ConvertFrom-Json does NOT unroll a root JSON array
        #      into the pipeline, so `... | ConvertFrom-Json | Where-Object` sees
        #      the whole array as ONE item and miscounts N issues as 1.
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
    }

    # Surfacing 2 (nightly conformance-run health) RETIRED 2026-07-09 (#255): the
    # conformance-digest mechanism (PR-triggered workflow + automation/conformance-digest
    # branch) was vacuous under the fleet's local-merge workflow and has been removed.
    # Local fleet health now surfaces via scripts/fleet_health.py. No branch/Action probe here.
} catch {
    # never block or noise the session on a surfacing failure
}
exit 0
