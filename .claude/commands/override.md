---
name: override
description: RETIRED (ADR-85 amendment 2026-08-03 §A2) — discharges no gate; arms a local telemetry token only
---

> **RETIRED — this command overrides nothing.** The ADR-85 amendment 2026-08-03 §A2 retired the
> §4 local-token path: local state cannot make an integration event compliant, so
> `_override_active()` is kept **inert** and `scripts/session_end_backpressure.py` no longer
> consults the token. §A5 made that Stop-hook **advisory in full** — it cannot block turn-end, so
> there is no block left to exit.
>
> **The live hard leg is elsewhere:** `scripts/block_unanchored_push.py` refuses a push to `main`
> whose range carries unanchored first-parent spine entries. **Its sole escape is
> `git push --no-verify`** — transport-level, explicit, human-typed — made non-silent by the
> `journal_spine_anchor` audit backstop, which keeps **FAIL**ing until an anchor lands. Canon:
> `protocols/DEFINITION_OF_DONE.md` "JOURNAL spine anchor"; ADR-85 §A2/§A5.
>
> Running this command still appends to `logs/OVERRIDES.md` and writes the token, but **no gate
> reads either**. It survives only as the local override-rate telemetry record below. Do not
> reach for it expecting a bypass, and do not cite it as one.

`$ARGUMENTS` is the reason.

## Procedure

1. **Require a reason.** If `$ARGUMENTS` is empty or whitespace → **reject**: do nothing,
   write nothing, and tell the operator a reason is mandatory. Never arm an unexplained
   override.
2. **Log + arm**, in this order (the token must record the HEAD the Stop-hook will see, so
   do **not** commit anything in between — both files are gitignored, so the tree stays
   clean and HEAD does not move):
   - Append a newest-first entry to `logs/OVERRIDES.md` (gitignored ephemeral local audit):
     timestamp, reason, branch, HEAD.
   - Write the HEAD-bound one-shot token `logs/.session-override-token` (gitignored) =
     `{ "head": <current HEAD>, "reason": <reason>, "ts": <timestamp> }`.

   Run this (PowerShell):

   ```powershell
   $reason = "$ARGUMENTS".Trim()
   if (-not $reason) { Write-Output "REJECTED — /override requires a reason. Nothing armed."; return }
   $head   = (git rev-parse HEAD).Trim()
   $branch = (git branch --show-current).Trim()
   $ts     = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
   if (-not (Test-Path logs)) { New-Item -ItemType Directory logs | Out-Null }  # logs/ is not tracked (gitignored-ephemeral); create on demand
   if (-not (Test-Path logs/OVERRIDES.md)) { Set-Content logs/OVERRIDES.md "# Session-gate overrides (ADR-85)`n`nAppend-only, newest-first. Gitignored ephemeral local audit (override-rate telemetry).`n" -Encoding utf8 }
   $existing = Get-Content logs/OVERRIDES.md -Raw
   $entry = "## $ts — $branch @ $($head.Substring(0,7))`n$reason`n`n"
   # prepend the new entry directly under the H1 header block (newest-first)
   $parts = $existing -split "(?<=telemetry\)\.`r?`n)", 2
   Set-Content logs/OVERRIDES.md ($parts[0] + "`n" + $entry + $parts[1]) -Encoding utf8 -NoNewline
   @{ head = $head; reason = $reason; ts = $ts } | ConvertTo-Json -Compress | Set-Content logs/.session-override-token -Encoding utf8 -NoNewline
   Write-Output "OVERRIDE LOGGED (telemetry only) — HEAD $($head.Substring(0,7)) on $branch. This discharges NO gate: the Stop hook is advisory in full and no longer reads the token (ADR-85 §A2/§A5). The pre-push hard leg's only escape is 'git push --no-verify'."
   ```

3. **Report** what was logged — and say plainly that **no gate was discharged**. Never report
   this as a bypass; if the operator wanted the pre-push leg bypassed, the answer is
   `git push --no-verify`, typed by them.

## Notes
- **The token is inert.** It is still HEAD-bound and one-shot by construction, but nothing
  consults it: `session_end_backpressure.py::_override_active()` is kept only for the record
  (ADR-85 §A2). Writing it changes no gate's verdict.
- **Never committed.** `logs/.session-override-token` and `logs/OVERRIDES.md` are gitignored
  (ADR-85). Arming an override does not dirty the tracked tree and creates no leftover.
- **Telemetry.** `logs/OVERRIDES.md` is the local override-rate record — if overrides exceed
  ~10% of sessions, the gate rules need tuning, not the human reinstated as trigger (ADR-85
  consequences).
