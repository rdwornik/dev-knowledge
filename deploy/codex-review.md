# /codex-review — Invoke Codex review

Runs `codex-review.ps1` which wraps `codex exec --output-last-message`. Produces a dated, frontmatter-wrapped audit file in `docs/audits/`.

## Diff review (default)

Reviews the diff between current branch and main. Invoke the script by explicit path
(no PowerShell-profile function required):

```powershell
& "$env:USERPROFILE\.claude\bin\codex-review.ps1" -Topic <topic>
```

With focus hints and auto-commit:

```powershell
& "$env:USERPROFILE\.claude\bin\codex-review.ps1" -Topic hotfix-review -AutoCommit -Focus @"
- Bullet 1
- Bullet 2
"@
```

Custom diff range:

```powershell
& "$env:USERPROFILE\.claude\bin\codex-review.ps1" -Topic compare -DiffRange feature/branch-a..feature/branch-b
```

## Full audit / whole-repo (Scale L, monthly cadence per Playbook S16)

The whole-repo audit is the `-FullAudit` switch (this is the "`--full`" capability — no
separate flag needed; `-FullAudit` audits the code files under `src/` rather than a diff):

```powershell
& "$env:USERPROFILE\.claude\bin\codex-review.ps1" -Topic quarterly-audit -FullAudit
```

## Output

- File: `docs/audits/YYYY-MM-DD-codex-{topic}.md`
- Frontmatter: date, branch, HEAD, diff range, Codex version, mode, consumer declaration
- Severity bands: Critical / High / Medium / Low (per AGENTS.md)

## Consumer declaration ([#1329])

Every review record declares its own consumer before the review runs (fails fast, before
invoking `codex`, on a missing or invalid declaration). Pass exactly one:

```powershell
# a governance citation -- a [#id] row, ADR-<n>, STANDING_RULINGS, or intake #<n>
& "$env:USERPROFILE\.claude\bin\codex-review.ps1" -Topic hotfix-review -Consumer "[#1329]"

# or an explicit reason it has none (24+ characters)
& "$env:USERPROFILE\.claude\bin\codex-review.ps1" -Topic hotfix-review -NoConsumerReason "ad-hoc spot-check, no tracked follow-up"
```

## Rules

- Always runs against the current working branch — check out the right branch first
- Never merges or pushes — review-only artifact
- Auto-commit is opt-in via `-AutoCommit`
- OneDrive-safe commit messages via file-based `git commit -F`
- Re-running with same Topic+Date prompts to overwrite (use `-Force` to skip prompt)
- **Code-vs-doc path-guard:** a diff containing **any** code file (extension allowlist below) is reviewed with the **code profile**; a diff with **no code files but ≥1 prose file** (`.md`/`.rst`/`.txt`) routes to the **doc-lane** prose/structural profile ([#333]) instead of being skipped (non-prose paths like images are ignored, not a blocker). **Mixed** code+prose diffs are filtered down to the code subset and reviewed with the code profile (prose in a mixed diff is not separately doc-reviewed).
- **Empty-diff guard:** if the resolved diff range contains zero changed files (e.g. running on `main` where `main..main` is empty), or contains neither code nor doc files, exits cleanly with a message and does NOT invoke codex.
- **`-FullAudit` is code-only:** the doc-lane applies to diff mode only. `-FullAudit` reviews the code files under `src/`; if `src/` contains no code files, it exits cleanly.

### Code-extension allowlist

`.py` `.ps1` `.psm1` `.sh` `.bash` `.ts` `.tsx` `.js` `.jsx` `.go` `.rs` `.rb` `.java` `.cs` `.cpp` `.cc` `.c` `.h` `.hpp` `.sql` `.toml` `.yaml` `.yml` `.json` `.ini`

Prose files — `.md` `.rst` `.txt` — are **not** code, but a diff with no code files and at least one of these routes to the doc-lane (below). Everything else (images, binaries) is neither code nor prose and is ignored.

### Doc-lane review ([#333])

When a diff has **no** code files but **does** have prose files (`.md`/`.rst`/`.txt`), the
wrapper runs a **prose/structural** review instead of skipping — `mode=doc-review`. It
assesses disposition-faithfulness, cross-doc consistency (stale claims, dangling
references), structural integrity (broken links, section/anchor/TOC drift), and
template/usability, under the same Critical/High/Medium/Low bands. **Both lanes** pin the
model explicitly to **`gpt-5.6-terra`** (the verified default; never a bare `gpt-5.6`) — the
doc-lane pin was [#333], the code lane joined it at [#469] (2026-08-01) after a run the
operator asked for as terra silently EXECUTED as sol, with nothing in the artifact recording
which model had run. Neither lane inherits the config default. Diff mode only — see PLAYBOOK §16.

## Setup

The script lives at `~/.claude/bin/codex-review.ps1` and is invoked by explicit path (see
examples above) — **no PowerShell-profile function or PATH entry is required**. A profile
alias is optional convenience only; the command no longer depends on it:

```powershell
# optional convenience alias — NOT required:
function codex-review { & "$env:USERPROFILE\.claude\bin\codex-review.ps1" @args }
```
