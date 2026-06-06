# billing_leak_sentinel.ps1 — BACKLOG #101 SessionStart billing-leak sentinel.
#
# Fail-soft tripwire. If ANTHROPIC_API_KEY is visible inside this Claude Code
# session, print ONE WARN line; a clean session stays silent. A non-empty key
# silently switches CC from Max-subscription billing to API billing with no TUI
# indicator (billing-trap gotcha, 2026-06-06). The PATH shim
# (AppData\Roaming\npm\claude.cmd) strips the key, but an npm update can clobber
# the shim and re-leak it — this sentinel catches that regression at session start.
#
# Presence-only: never echoes any part of the key value into the transcript.
# Read-only; never wedges session-start (always exits 0). Mirrors the
# surface-closures.ps1 SessionStart pattern.

try {
    if (-not [string]::IsNullOrWhiteSpace($env:ANTHROPIC_API_KEY)) {
        Write-Output "[billing] WARN: ANTHROPIC_API_KEY is visible in this Claude Code session - billing is going to the API key, NOT the Max subscription (no TUI indicator). The PATH shim may be clobbered (npm can overwrite AppData\Roaming\npm\claude.cmd). See gotchas: billing-trap 2026-06-06."
    }
} catch {
    # fail-soft: a sentinel must never block session-start
}
exit 0
