# Codex Review — lane-handoff-unblock

**Date:** 2026-10-01
**Branch:** `worktree-lane-handoff-unblock`
**HEAD:** `1e767963`
**Diff range:** `main..worktree-lane-handoff-unblock`
**Codex version:** n/a — SUBSTITUTED (see below)
**Mode:** diff-review
**Tally:** 0/3/1/2 <!-- Critical/High/Medium/Low -->

**Model used:** `gemini-3.1-pro-high` (SUBSTITUTE for the pinned `gpt-5.6-terra` — see Substitution note)
**Review profile:** code
**Consumer:** [#1328] [#1329] [#1330] (`LANE-HANDOFF-UNBLOCK-lane-handoff-unblock.md`)

---

## Substitution note

`SUBSTITUTION: codex terra -> agy gemini-3.1-pro-high`. Attempted via the hub carrier
`deploy/codex-review.ps1` first (run from the hub path, not `~/.claude/`, per [#1329] item
2), topic `lane-handoff-unblock`, `-Consumer "[#1328] [#1329] [#1330] ..."` — the organ's own
`Get-ConsumerLine` (`deploy/codex-review-lib.ps1`) accepted the declaration and the wrapper
invoked `codex exec` (session `01a0f4fd-630d-7270-b26b-3fe1f60f1eb1`, workdir this worktree,
model `gpt-5.6-terra`, reasoning effort high), which failed:

```
ERROR: You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit
https://chatgpt.com/codex/settings/usage to purchase more credits or try again at Oct 3rd,
2026 9:07 PM.
```

Per ruling (e) (common rules §2) and `JOURNAL.md:49` ("`agy` as the recorded SUBSTITUTION for
Codex terra (usage limit)"), the equivalent review was run via `agy` (`gemini-3.1-pro-high`,
effort high, `--dangerously-skip-permissions`), reusing the SAME prompt the hub wrapper built
(file restriction list, severity-band instructions, AGENTS.md definitions) — captured verbatim
from the failed `codex exec` invocation's own echoed prompt before it errored. This record is
therefore hand-composed in the organ's frontmatter shape rather than emitted by the script
itself, because the script's own file-write path only fires after a successful `codex exec`
exit; `Get-ConsumerLine`'s declaration-acceptance behavior was still exercised and is not
substituted.

## Focus

(none specified)

## Files reviewed

- deploy/carrier_codexreview.py
- deploy/codex-review-lib.ps1
- deploy/codex-review.ps1
- deploy/manifest-v1.5.0.yaml
- deploy/tool.py
- ecosystem/audit-consumer-baseline.json
- pyproject.toml
- scripts/consumer_at_landing.py
- scripts/gen_handoff.py
- scripts/handoff_state.py
- scripts/verify_handoff_probes.py
- tasks/manifest.json
- tests/test_codex_review_consumer.py
- tests/test_consumer_at_landing.py
- tests/test_deploy_codex_review_carrier.py
- tests/test_gen_handoff.py
- tests/test_handoff_state.py
- tests/test_verify_handoff_probes.py

---

## Findings

## Critical
(none)

## High

## HIGH deploy/carrier_codexreview.py:110 — Missing error handling for file I/O
**What:** File I/O operations (`read_bytes()`, `write_bytes()`) are executed without
`try/except` blocks (also lines 129, 152, 192, 195).
**Why:** Unreadable, missing files, or locked directories will raise an unhandled `OSError`
and crash the carrier tool unexpectedly.
**Fix direction:** Wrap the file operations in a `try/except OSError:` block and return an
appropriate failure state.
**Disposition:** NOT FIXED. `_read_source`/`_classify_organ` (lines 102-129) are pre-existing
`[#1328]` logic this lane did not author or restructure — this lane's only edit to this file
was appending a third tuple to `_DEFAULT_PAIRS`. `[#1328]` is already closed
(evidence f643e4e3/059d49a6) and its Done-when proved this carrier's source
byte-identical to the live-installed organ at that commit; editing the file's control flow
now would be unauthorized scope expansion into an already-closed row (R38), not a fix this
lane's rows call for. Recorded for the operator/next lane touching this carrier.

## HIGH deploy/codex-review.ps1:348 — Missing error handling for subprocesses
**What:** Subprocess calls (`git rev-parse`, `codex --version`, `git diff`) lack
`try/catch`/`$LASTEXITCODE` checks (also lines 349, 351, 402).
**Why:** A silent failure lets the script continue with invalid variables, risking cascading
logical failures or invalid input reaching Codex.
**Fix direction:** Validate `$LASTEXITCODE` immediately after each call, or wrap in
try/catch.
**Disposition:** NOT FIXED. `codex-review.ps1` is the `[#1328]` hub-tracked REPRODUCTION of
the pre-existing, untracked `~/.claude/bin/codex-review.ps1` organ (render note N3: "its
source moves under the hub... byte-identical, so the [#1328] reproduction holds"). This
lane's only edits to this file (for `[#1329]` item 2) were adding the `-Consumer`/
`-NoConsumerReason` params and the `Get-ConsumerLine` call/dot-source near the top — lines
348/402 are untouched, pre-existing control flow from the original organ. Editing them now
would break the `[#1328]` byte-identity precedent this lane's own `[#1329]` tests
(`tests/test_codex_review_consumer.py`) build on. Recorded for the operator.

## HIGH deploy/codex-review.ps1:581 — Missing error handling for .NET file I/O
**What:** `[System.IO.File]::WriteAllText` (also line 642) has no `try/catch`.
**Why:** A write failure throws a raw .NET exception bypassing the script's graceful exit
handling.
**Fix direction:** Wrap in a PowerShell `try { ... } catch { ... }` block.
**Disposition:** NOT FIXED, same reason as above — pre-existing `[#1328]` code, untouched by
this lane's edits, byte-identity-locked. Recorded for the operator.

## Medium

## MEDIUM deploy/codex-review.ps1:330 — Magic numbers used for exit codes
**What:** Unnamed magic numbers for exit codes (`exit 2`, `exit 3`, `exit 4` at lines 330,
535, 627).
**Why:** Hardcoded exit codes obscure the failure condition for a consuming script.
**Fix direction:** Define named variables for these constants at the script header.
**Disposition:** NOT FIXED — pre-existing `[#1328]` code, same reasoning as the HIGH findings
above.

## Low

## LOW deploy/codex-review-lib.ps1:241 — Missing docstring
**What:** `Get-ConsumerLine` lacks PowerShell comment-based help (`.SYNOPSIS` block).
**Why:** Reduces discoverability of the function's parameters and intent.
**Fix direction:** Add a `<# ... #>` comment-based help block above the function.
**Disposition:** NOT FIXED (LOW, not P1). This is the one finding in code this lane actually
newly authored (`deploy/codex-review-lib.ps1`, new for `[#1329]`); carried as a cosmetic
follow-up rather than blocking this lane's close-out.

## LOW deploy/codex-review.ps1:348 — Inconsistent naming patterns
**What:** Variable names mix `PascalCase` (`$OutDir`, `$Topic`) and `camelCase` (`$branch`,
`$headShort`).
**Why:** Inconsistent casing reduces readability.
**Fix direction:** Standardize on one convention for local variables.
**Disposition:** NOT FIXED — pre-existing `[#1328]` code (LOW, not P1 either way).

---

## Disposition summary (ruling (e): fix P1, record the rest)

Zero Critical findings. All three High findings, and the one Medium finding, are in
pre-existing `[#1328]` organ code this lane did not author and is barred from altering
without breaking the already-proven byte-identity invariant (R38: not this lane's fix to
make). The one finding in code this lane DID newly write (`codex-review-lib.ps1`) is LOW.
Nothing in this review is fixed in this commit; every finding is recorded above with its
specific disposition reasoning.
