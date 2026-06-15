# SessionStart surfacing for the nightly conformance loop (Phase C4 / ADR-68).
#
# Mirrors the L0 surface-closures.ps1 pattern: READ-ONLY, fail-soft, ALWAYS exit 0,
# silent on the happy path (gh absent / offline, or nothing to report). Surfaces
# four things, each only when there is something to say:
#   [gh]      — gh auth is invalid/expired (operator-recoverable ONLY; surfaces the
#               refresh command, then skips the gh-dependent checks below)
#   [triage]  — open `nightly-triage` Issues await review
#   [nightly] — the last Nightly Conformance Triage Action run did NOT succeed
#   [nightly] — the automation/conformance-digest branch EXISTS but the expected
#               dated digest is missing from it (the no-retry silent-skip class —
#               side-effect check per ADR-68). A branch that does not yet exist is
#               "not-yet-initialized" and is SILENT, not an alarm (transition-window).
# This is a surfacing nudge only — it never blocks or noises the session.
#
# verify: under Windows PowerShell 5.1 (`powershell -File scripts/surface_triage.ps1`,
#   the hook's actual runtime) with zero open `nightly-triage` Issues it prints NO
#   "[triage]" line (not "[triage] 1 ... await: #"); with N open it prints
#   "[triage] N nightly finding(s) await: #a, #b ...". It emits a "[nightly]" line
#   ONLY when the last Action run failed, or the automation/conformance-digest
#   branch EXISTS but the expected dated digest is missing from it; a branch that
#   does NOT yet exist is silent (not-yet-initialized, not a skip). On the all-green
#   happy path it prints nothing, exit 0.
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

    # --- Surfacing 2: nightly run health (ADR-68 outcome loop) ----------------
    # The platform emails on a failed Routine run but has NO retry and NO
    # in-session surfacing -- so a failed run, or a silently-skipped one (machine
    # asleep at 03:00), goes unseen until someone notices a missing digest.
    # Side-effect checks are the documented best practice for the no-retry class.

    # (a) Last "Nightly Conformance Triage" Action run -- not success -> loud.
    $runJson = & $gh run list --workflow "Nightly Conformance Triage" --limit 1 --json conclusion,status,url 2>$null
    if ($runJson) {
        $runParsed = $runJson | ConvertFrom-Json
        $runs = @($runParsed | Where-Object { $_ -and $_.url })
        if ($runs.Count -gt 0 -and $runs[0].status -eq 'completed' -and $runs[0].conclusion -ne 'success') {
            Write-Output "[nightly] last Nightly Conformance Triage run did NOT succeed (conclusion=$($runs[0].conclusion)): $($runs[0].url)"
        }
    }

    # (b) Side-effect check: the expected digest for the most recent run date
    #     should exist on the automation/conformance-digest branch (ADR-84/Q9 —
    #     the digest is isolated from main; the nightly Action diverts it there).
    #     Missing -> last night's nightly likely silently skipped (no-retry class).
    #     Query GitHub directly (gh fills {owner}/{repo} from cwd) so a stale local
    #     clone cannot false-alarm. Get-Date is the real local clock (correct at runtime).
    $now = Get-Date
    $expected = if ($now.Hour -ge 4) { $now } else { $now.AddDays(-1) }
    $stamp = $expected.ToString('yyyy-MM-dd')
    $digestPath = "docs/audits/$stamp-conformance-nightly-digest.md"

    # ATOMIZE the two concerns this probe used to conflate into one alarm:
    #   (1) the automation branch does NOT YET EXIST -> "not-yet-initialized",
    #       NOT a skipped nightly -> STAY SILENT. This is the transition-window
    #       false positive: when ADR-84 (or any future repoint) points this probe
    #       at the branch BEFORE the branch's first digest has ever been written,
    #       a `contents` query 404s and the old code cried "silently skipped" on a
    #       perfectly healthy pipeline. Branch-absence is the tell that there is
    #       simply nothing to expect yet.
    #   (2) the branch EXISTS but the dated digest is MISSING -> the real no-retry
    #       silent-skip signal -> alarm, exactly as before.
    # Both probes query GitHub LIVE so a stale local clone cannot decide either
    # one. `gh api` exits 0 ONLY on HTTP 200 and prints the error BODY to STDOUT on
    # a 404 -- so gate on the EXIT CODE, never on stdout truthiness (a 404 body is
    # non-empty and would read as a false "present"). Branch names carry a slash;
    # `branches/automation/conformance-digest` is accepted as-is (same as the
    # `?ref=automation/conformance-digest` form already used below).
    $null = & $gh api "repos/{owner}/{repo}/branches/automation/conformance-digest" 2>$null
    $branchExists = ($LASTEXITCODE -eq 0)
    if ($branchExists) {
        $found = & $gh api "repos/{owner}/{repo}/contents/$digestPath?ref=automation/conformance-digest" --jq '.name' 2>$null
        $present = ($LASTEXITCODE -eq 0) -and ($found -match '\.md\s*$')
        if (-not $present) {
            Write-Output "[nightly] expected digest '$digestPath' is NOT on the automation/conformance-digest branch -- last night's nightly may have silently skipped (no retry)."
        }
    }
} catch {
    # never block or noise the session on a surfacing failure
}
exit 0
