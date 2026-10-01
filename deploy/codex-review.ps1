[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$Topic,

    [Parameter(Mandatory=$false)]
    [string]$DiffRange,

    [Parameter(Mandatory=$false)]
    [string]$Focus = "",

    [Parameter(Mandatory=$false)]
    [string]$OutDir,

    [Parameter(Mandatory=$false)]
    [string]$Consumer = "",

    [Parameter(Mandatory=$false)]
    [string]$NoConsumerReason = "",

    [switch]$AutoCommit,
    [switch]$FullAudit,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

# --- Consumer declaration ([#1329]) -------------------------------------------
# Every new review record declares its own consumer at landing -- a governance citation
# (-Consumer) or an explicit -NoConsumerReason -- so it clears consumer_at_landing.undeclared()
# on its own text rather than relying on a human edit after the fact. Resolved BEFORE the
# (expensive, codex-invoking) review runs: a bad or missing declaration fails fast.
. (Join-Path $PSScriptRoot 'codex-review-lib.ps1')
$consumerLine = Get-ConsumerLine -Consumer $Consumer -NoConsumerReason $NoConsumerReason

# --- Preconditions -----------------------------------------------------------

if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    Write-Error "codex CLI not found on PATH. Install: npm i -g @openai/codex"
    exit 2
}

$insideRepo = (& git rev-parse --is-inside-work-tree 2>$null)
if ($LASTEXITCODE -ne 0 -or $insideRepo -ne 'true') {
    Write-Error "Not inside a git repository. cd to a repo before running codex-review."
    exit 2
}

# --- Normalize inputs --------------------------------------------------------

$Topic = ($Topic.ToLower() -replace '\s+', '-') -replace '[^a-z0-9\-_]', ''
if ([string]::IsNullOrWhiteSpace($Topic)) {
    Write-Error "Topic is empty after normalization. Provide alphanumeric/hyphen chars."
    exit 2
}

$repoRoot = (& git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0) {
    Write-Error "git rev-parse --show-toplevel failed (exit $LASTEXITCODE)."
    exit 2
}
$branch   = (& git rev-parse --abbrev-ref HEAD).Trim()
if ($LASTEXITCODE -ne 0) {
    Write-Error "git rev-parse --abbrev-ref HEAD failed (exit $LASTEXITCODE)."
    exit 2
}
$headShort = (& git rev-parse --short HEAD).Trim()
if ($LASTEXITCODE -ne 0) {
    Write-Error "git rev-parse --short HEAD failed (exit $LASTEXITCODE)."
    exit 2
}
$date = Get-Date -Format 'yyyy-MM-dd'
$codexVersion = ((& codex --version 2>&1) | Select-Object -First 1).ToString().Trim()
if ($LASTEXITCODE -ne 0) {
    Write-Error "codex --version failed (exit $LASTEXITCODE). Is the codex CLI healthy?"
    exit 2
}

if (-not $DiffRange -and -not $FullAudit) {
    $DiffRange = "main..$branch"
}

# --- Code-only path-guard ----------------------------------------------------
# codex-review is for code, not markdown/prose. Filter diff (or src/ tree for
# FullAudit) by extension allowlist. Empty/markdown-only diff exits cleanly.
$codeExtensions = @(
    '.py','.ps1','.psm1','.sh','.bash','.ts','.tsx','.js','.jsx',
    '.go','.rs','.rb','.java','.cs','.cpp','.cc','.c','.h','.hpp','.sql',
    '.toml','.yaml','.yml','.json','.ini'
)

function Get-CodeFiles([string[]]$paths) {
    return $paths | Where-Object {
        $ext = [System.IO.Path]::GetExtension($_).ToLower()
        $codeExtensions -contains $ext
    }
}

# Doc-lane ([#333]): a pure-prose diff (no code files) is not skipped -- it routes
# to a prose/structural review profile instead. Diff mode only; -FullAudit stays code-only.
$docExtensions = @('.md','.rst','.txt')

function Get-DocFiles([string[]]$paths) {
    return $paths | Where-Object {
        $ext = [System.IO.Path]::GetExtension($_).ToLower()
        $docExtensions -contains $ext
    }
}

$reviewProfile = 'code'
$codeFileList = ""
$docFileList = ""
if ($FullAudit) {
    $srcDir = Join-Path $repoRoot 'src'
    if (-not (Test-Path $srcDir)) {
        Write-Host "[codex-review] -FullAudit requires src/ at repo root; not found at $srcDir" -ForegroundColor Yellow
        exit 0
    }
    $allFiles = @(Get-ChildItem -Path $srcDir -Recurse -File | ForEach-Object { $_.FullName })
    $codeFiles = @(Get-CodeFiles $allFiles)
    if ($codeFiles.Count -eq 0) {
        Write-Host "[codex-review] no code files under src/ -- codex-review is for code, not markdown" -ForegroundColor Yellow
        exit 0
    }
    $relCodeFiles = $codeFiles | ForEach-Object { $_.Substring($repoRoot.Length).TrimStart('\','/') }
    $codeFileList = ($relCodeFiles | ForEach-Object { "- $_" }) -join "`n"
} else {
    $changedFiles = @((& git diff --name-only $DiffRange 2>$null) | Where-Object { $_ })
    if ($LASTEXITCODE -ne 0) {
        Write-Error "git diff --name-only '$DiffRange' failed (exit $LASTEXITCODE). Check the diff range."
        exit 2
    }
    if ($changedFiles.Count -eq 0) {
        Write-Host "[codex-review] no diff to review for range '$DiffRange' -- check out a feature branch or pass -DiffRange/-FullAudit" -ForegroundColor Yellow
        exit 0
    }
    $codeFiles = @(Get-CodeFiles $changedFiles)
    if ($codeFiles.Count -eq 0) {
        # Doc-lane ([#333]): no code files -- if the diff has prose files, review them via
        # the doc profile instead of skipping. Only a diff with neither code nor doc exits.
        $docFiles = @(Get-DocFiles $changedFiles)
        if ($docFiles.Count -eq 0) {
            Write-Host "[codex-review] no code or doc changes to review -- nothing to send to codex" -ForegroundColor Yellow
            exit 0
        }
        $reviewProfile = 'doc'
        $docFileList = ($docFiles | ForEach-Object { "- $_" }) -join "`n"
    } else {
        $codeFileList = ($codeFiles | ForEach-Object { "- $_" }) -join "`n"
    }
}

if (-not $OutDir) {
    $docsDir = Join-Path $repoRoot 'docs'
    if (-not (Test-Path $docsDir)) {
        Write-Error "No docs/ directory at repo root ($repoRoot). Pass -OutDir explicitly."
        exit 2
    }
    $OutDir = Join-Path $docsDir 'audits'
}
if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
}

$outFile = Join-Path $OutDir "$date-codex-$Topic.md"
$tempFile = Join-Path $env:TEMP "codex-$date-$Topic-$(Get-Random).md"

if ((Test-Path $outFile) -and -not $Force) {
    Write-Host "Output file already exists: $outFile" -ForegroundColor Yellow
    $resp = Read-Host "Overwrite? (y/N)"
    if ($resp -notmatch '^[Yy]') {
        Write-Host "Aborted." -ForegroundColor Yellow
        exit 1
    }
}

# --- Build prompt ------------------------------------------------------------

$focusBlock = if ([string]::IsNullOrWhiteSpace($Focus)) { "(none specified)" } else { $Focus }

if ($reviewProfile -eq 'doc') {
    $prompt = @"
Review the DOCUMENTATION diff: $DiffRange

This is a PROSE / STRUCTURAL review, not a code review. Restrict review to these
prose/markdown files only (ignore any other paths in the diff):
$docFileList

Focus hints:
$focusBlock

Assess the changed prose along these axes:
- Disposition-faithfulness: does the text accurately reflect the decision, state, or
  behavior it claims? Flag over-claims and statements not supported by the change.
- Cross-doc consistency: contradictions with sibling docs, stale claims, dangling or
  broken cross-references, superseded facts left standing.
- Structural integrity: broken links, wrong section/anchor numbers, TOC or heading drift,
  mis-ordered or duplicated sections.
- Template / usability: is the guidance actionable and unambiguous for its reader?

Use these severity definitions (Critical / High / Medium / Low).
For each finding output: severity, file:line, what, why, fix direction.
If there are no findings in a severity band, write "(none)".
Group findings by severity band, highest first.
"@
} elseif ($FullAudit) {
    $prompt = @"
Full audit of src/ in this repository.

Restrict review to these code files only (ignore any other paths under src/):
$codeFileList

Focus hints:
$focusBlock

Use the repo's AGENTS.md severity definitions (Critical / High / Medium / Low).
For each finding output: severity, file:line, what, why, fix direction.
If there are no findings in a severity band, write "(none)".
Group findings by severity band, highest first.
"@
} else {
    $prompt = @"
Review the diff: $DiffRange

Restrict review to these code files only (ignore any other paths in the diff):
$codeFileList

Focus hints:
$focusBlock

Use the repo's AGENTS.md severity definitions (Critical / High / Medium / Low).
For each finding output: severity, file:line, what, why, fix direction.
If there are no findings in a severity band, write "(none)".
Group findings by severity band, highest first.
"@
}

# --- Invoke Codex ------------------------------------------------------------

$mode = if ($reviewProfile -eq 'doc') { 'doc-review' } elseif ($FullAudit) { 'full-audit' } else { 'diff-review' }
Write-Host "[codex-review] mode=$mode topic=$Topic branch=$branch head=$headShort" -ForegroundColor Cyan
Write-Host "[codex-review] output: $outFile" -ForegroundColor Cyan
Write-Host "[codex-review] invoking codex exec (this may take a few minutes)..." -ForegroundColor Cyan

# BOTH lanes pin the model explicitly ([#469], 2026-08-01; doc-lane pin was [#333]).
# Previously only the doc lane pinned, and the code lane passed no model flag -- so it
# inherited ~/.codex/config.toml. Combined with the [#431] mixed-diff demotion, a review the
# operator asked for as terra silently EXECUTED as sol (witnessed 2026-08-01), and nothing in
# the artifact recorded which model had run. An unpinned reviewer also makes the cross-provider
# comparisons the portability work depends on unreproducible. terra is the verified-working
# string -- never a bare gpt-5.6.
$reviewModel = 'gpt-5.6-terra'
$modelArgs = @('-c', "model=$reviewModel")
$prompt | & codex exec --sandbox read-only @modelArgs -c model_reasoning_effort=high --output-last-message $tempFile -
$codexExit = $LASTEXITCODE

if ($codexExit -ne 0) {
    Write-Error "codex exec failed with exit code $codexExit"
    if (Test-Path $tempFile) { Remove-Item $tempFile -Force }
    exit $codexExit
}

if (-not (Test-Path $tempFile)) {
    Write-Error "codex exec produced no output file at $tempFile"
    exit 3
}

$codexOutput = Get-Content $tempFile -Raw
if ([string]::IsNullOrWhiteSpace($codexOutput)) {
    Write-Error "codex exec output was empty. No review produced."
    Remove-Item $tempFile -Force
    exit 3
}

# --- Compose final file with frontmatter ------------------------------------

$diffRangeLabel = if ($FullAudit) { "(full audit)" } else { $DiffRange }

$header = @"
# Codex Review — $Topic

**Date:** $date
**Branch:** ``$branch``
**HEAD:** ``$headShort``
**Diff range:** ``$diffRangeLabel``
**Codex version:** $codexVersion
**Mode:** $mode
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** ``$reviewModel`` (pinned; both lanes — [#469])
**Review profile:** $reviewProfile
$consumerLine

---

## Focus

$focusBlock

---

## Findings

"@

# LF-safe write ([#471]'s sibling defect, 2026-08-01). The here-strings above inherit THIS
# file's CRLF line endings, so Set-Content emitted a CRLF artifact into an LF-canonical repo --
# a whole-file phantom diff, and the same class the repo-side generators were just fixed for.
# WriteAllText with an explicit BOM-less UTF8 encoding writes exactly the bytes given.
$finalContent = ($header + $codexOutput) -replace "`r`n", "`n"
try {
    [System.IO.File]::WriteAllText($outFile, $finalContent, (New-Object System.Text.UTF8Encoding($false)))
} catch {
    Write-Error "Could not write review artifact to $outFile`: $($_.Exception.Message)"
    exit 4
}
Remove-Item $tempFile -Force

# --- Parse severity counts for summary --------------------------------------

$finalContent = Get-Content $outFile -Raw
# Widened 2026-08-07 (hub LC-1). The old pattern required a `:` or `-` immediately after the
# label, so it MISSED terra's actual finding shape -- `## HIGH scripts/x.py:62 - what` -- and
# reported 0/0/0/0 for a review carrying a real HIGH (measured on the lane-a-501-retro run).
# A band HEADING (`## High` with nothing after it) still must NOT count, so the alternation is
# "label then a separator" OR "label then whitespace then something".
function Count-Severity([string]$content, [string]$label) {
    # NOTE [ \t] not \s throughout: \s matches newlines, so `## High` followed by a blank
    # line and `(none)` would satisfy "label then whitespace then something" and every band
    # heading would count as a finding. Everything here stays on ONE line by construction.
    $pattern = "(?im)^[ \t]*[#*\-]*[ \t]*(?:\*\*)?$label(?:\*\*)?[ \t]*(?:[:\-]|[ \t]+\S)"
    return [regex]::Matches($content, $pattern).Count
}
$sevCounts = [ordered]@{
    Critical = Count-Severity $codexOutput 'Critical'
    High     = Count-Severity $codexOutput 'High'
    Medium   = Count-Severity $codexOutput 'Medium'
    Low      = Count-Severity $codexOutput 'Low'
}

Write-Host ""
Write-Host "[codex-review] Saved: $outFile" -ForegroundColor Green
Write-Host "[codex-review] Severity mentions (heuristic):" -ForegroundColor Green
foreach ($k in $sevCounts.Keys) {
    Write-Host ("  {0,-8} {1}" -f $k, $sevCounts[$k])
}
# The artifact ships `**Tally:** TBD/TBD/TBD/TBD` deliberately: this count is a HEURISTIC over
# free-form model prose and has been wrong in production, so writing it into the artifact
# unread would convert an honest "unrecorded" into a confident falsehood -- the exact failure
# [#480] exists to prevent. Suggest it; make a human/agent confirm it against the findings.
Write-Host ""
Write-Host ("[codex-review] SUGGESTED tally (verify against Findings, then replace the TBD line):") -ForegroundColor Yellow
Write-Host ("  **Tally:** {0}/{1}/{2}/{3}" -f $sevCounts.Critical, $sevCounts.High, $sevCounts.Medium, $sevCounts.Low) -ForegroundColor Yellow

# --- Auto-commit -------------------------------------------------------------

if ($AutoCommit) {
    $relOut = (Resolve-Path $outFile).Path.Substring($repoRoot.Length).TrimStart('\','/')
    & git add -- $outFile
    if ($LASTEXITCODE -ne 0) {
        Write-Error "git add failed"
        exit 4
    }

    $modeLabel = if ($FullAudit) { "full audit" } else { "review" }
    $msgFile = Join-Path $env:TEMP "codex-review-msg-$(Get-Random).txt"
    $msg = @"
docs(audit): codex $modeLabel for $Topic

Branch: $branch
HEAD: $headShort
Diff: $diffRangeLabel
Findings (heuristic): Critical=$($sevCounts.Critical) High=$($sevCounts.High) Medium=$($sevCounts.Medium) Low=$($sevCounts.Low)
"@
    # LF-safe, same reason as the artifact write above: a CRLF commit message file is passed
    # verbatim to `git commit -F`.
    try {
        [System.IO.File]::WriteAllText($msgFile, ($msg -replace "`r`n", "`n"),
                                       (New-Object System.Text.UTF8Encoding($false)))
    } catch {
        Write-Error "Could not write commit-message temp file $msgFile`: $($_.Exception.Message)"
        exit 4
    }
    & git commit -F $msgFile
    $commitExit = $LASTEXITCODE
    Remove-Item $msgFile -Force -ErrorAction SilentlyContinue

    if ($commitExit -ne 0) {
        Write-Error "git commit failed (exit $commitExit). File is staged."
        exit $commitExit
    }
    Write-Host "[codex-review] Committed." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "To commit:" -ForegroundColor Yellow
    Write-Host "  git add `"$outFile`"" -ForegroundColor Yellow
    Write-Host "  git commit -m `"docs(audit): codex review for $Topic`"" -ForegroundColor Yellow
}
