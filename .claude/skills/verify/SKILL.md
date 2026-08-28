---
name: verify
description: Run the standard check cadence (pytest + ruff + git-status) and report compact pass/fail. Invoke after each numbered step. Any FAIL blocks the current step.
---

When invoked, run the bundled check script and report its output verbatim:

```powershell
uv run --locked python .claude/skills/verify/verify.py
```

**On success the output is exactly three lines** — report them as-is.

**On failure** ([#127] contract) the script adds an `--- Actionable ---` section carrying,
for each failing check, a four-field block:

```
[pytest]
  file      : tests/test_widget.py::test_widget_count
  expected  : exit 0 - every test passes
  received  : assert 2 == 3
  directive : fix the failing test or the code under it, then re-run this skill
```

Report the three lines **and** the Actionable section; the `--- Full output ---` tail is
there when the block is not enough. If any line shows `FAIL`, **stop and fix before
proceeding** — do not continue to the next step.

**Semantic exit codes** — the machine-readable half of the same signal, for an
iterate-until-green loop:

| code | meaning |
|---|---|
| 0 | everything passed |
| 2 | pytest failed |
| 4 | ruff failed |
| 8 | git working tree dirty |

The codes are a **bitmask**, so they compose: `6` means pytest *and* ruff are red. This is
deliberate — the same code twice in a row means the last iteration made no progress, which
is the anti-retry-loop signal a first-failure-only code cannot express.

Note: canonical-home question deliberately open — refs #9; this is the hub-local pilot.
