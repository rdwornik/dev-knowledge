---
name: verify
description: Run the standard check cadence (pytest + ruff + git-status) and report compact pass/fail. Invoke after each numbered step. Any FAIL blocks the current step.
---

When invoked, run the bundled check script and report its 3-line output verbatim:

```powershell
uv run --locked python .claude/skills/verify/verify.py
```

Report the 3 lines as-is. If any line shows `FAIL`, **stop and fix before proceeding** — do not continue to the next step. On failure the script also prints full output; include that in your report.

Note: canonical-home question deliberately open — refs #9; this is the hub-local pilot.
