<!-- scope: meta -->
# Codex-review wrapper — model pin + LF-safe writes (global-infra change record)

**Date:** 2026-08-01
**Author:** Claude Code (Opus 5), operator-authorized
**Nature:** **Change record for an edit OUTSIDE this repository.** `~/.claude/bin/codex-review.ps1`
is global infrastructure; core-invariant #6 forbids modifying it unilaterally. The operator
recorded an explicit GO for this specific edit, which is what authorizes it. This file exists
because the change produces **no repo diff** — without it the edit would be invisible to every
future reader of this tree, which is the same silent-record defect [#460] was filed about.

---

## Why this file exists

`~/.claude/bin/` is not version-controlled by this repo. A change there is real, load-bearing,
and undiscoverable from `git log`. The two changes below are therefore transcribed with their
before/after state, so a later session can tell what the wrapper does and when it started
doing it — and can detect a silent revert.

---

## Change 1 — pin the review model on BOTH lanes ([#469])

**Before** (`codex-review.ps1`, the `$modelArgs` block):

```powershell
# Doc-lane pins the terra model string explicitly ([#333]; terra = the verified-working
# default, never a bare gpt-5.6). The code lane passes no model flag -- it inherits the
# config default unchanged, so code-review behavior is untouched.
$modelArgs = @()
if ($reviewProfile -eq 'doc') { $modelArgs = @('-c', 'model=gpt-5.6-terra') }
```

**After:**

```powershell
$reviewModel = 'gpt-5.6-terra'
$modelArgs = @('-c', "model=$reviewModel")
```

**The defect this closes.** Only the doc lane pinned. The code lane passed no model flag and so
inherited `~/.codex/config.toml` (`model = "gpt-5.6-sol"`). Combined with the [#431] mixed-diff
demotion — any `.py` in the diff routes the whole review to the CODE profile — a review the
operator asked for as terra silently **executed as sol**. Witnessed twice on 2026-08-01, in the
very arc that filed [#469]. Nothing in the output recorded which model had run, so the
substitution was undetectable after the fact.

## Change 2 — record the model in the artifact frontmatter ([#469]'s second clause)

Added to the generated header:

```
**Model used:** `$reviewModel` (pinned; both lanes — [#469])
**Review profile:** $reviewProfile
```

Without this, "which model reviewed this?" is unanswerable for every past artifact — and the
cross-provider comparisons the §C/§H portability work depends on are unreproducible.

## Change 3 — LF-safe writes (the [#471] sibling defect)

Both `Set-Content` calls replaced with explicit BOM-less `WriteAllText` after CRLF→LF
normalisation:

```powershell
$finalContent = ($header + $codexOutput) -replace "`r`n", "`n"
[System.IO.File]::WriteAllText($outFile, $finalContent, (New-Object System.Text.UTF8Encoding($false)))
```

**Root cause, which is not obvious:** the here-strings that build the header inherit **the
`.ps1` file's own line endings**, and that file is CRLF (322 CRLF / 322 LF). So the wrapper
emitted a CRLF artifact into an LF-canonical repo — a whole-file phantom diff, and the same
defect class as [#471], which was fixed on the repo side the same day. The commit-message file
passed to `git commit -F` got the same treatment.

---

## Verification (live, not asserted)

Syntax: `[System.Management.Automation.Language.Parser]::ParseFile` → **no syntax errors**.

Then the wrapper was run for real, on a diff containing `.py` files — i.e. the exact case that
previously fell through to sol:

```
[codex-review] mode=diff-review topic=460-replication-and-close
model: gpt-5.6-terra          <- the pin, on the CODE profile
```

Resulting artifact `docs/audits/2026-08-01-codex-460-replication-and-close.md`:

```
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
CRLF count: 0 | BOM: False
```

All three changes verified by their first real output rather than by inspection.

## Known limitation, stated rather than left implicit

The severity heuristic still miscounts: it printed `High 0` while the body carried one HIGH
(same miscount recorded in the [#383] wave-1 JOURNAL entry). **Read the body, never the
summary.** Not fixed here — it is a distinct defect in a different part of the wrapper, and
the operator's GO covered the model pin and the newline fix. It belongs to the [#431]/[#445]
wrapper family.

## Rollback

A backup of the pre-change file was taken to the session scratchpad before editing. To revert,
restore `codex-review.ps1` from it, or re-apply the three "Before" blocks above.
