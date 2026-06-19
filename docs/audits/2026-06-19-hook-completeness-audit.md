# Deny-rule + Hook-Completeness Audit — 2026-06-19

<!-- scope: meta -->

> **Read-only, adversarial coverage audit (BACKLOG #188).** Immutable per repo convention
> (supersede with a new dated file; never edit in place). No fixes are applied *by* this
> audit — it emits the coverage matrix. Findings were verified against live repo + `~/.claude`
> state during the session that produced this file; line numbers are as of 2026-06-19.
>
> **Distinct from #132** (the organ *inventory* / `ARCHITECTURE.md` Ch2 Organ map): that
> enumerates every organ. **This is the coverage *gap* view** — it maps the organs **against
> the ADR-75 exclusion-zone register** and asks the two questions #188 poses: *is any zone
> uncovered?* and *is any guard's match bypassable?*

---

## Orientation — what is being checked

ADR-75 makes the register's governance rule explicit: *"A register entry with no enforcing
organ on the executing path is decoration — every zone must be backed by a fail-closed organ
before the entry is considered active."* This audit tests that invariant from both directions:

1. **Zone → organ** (no uncovered zone): every ADR-75 register zone (as amended by ADR-77,
   ADR-78) has a fail-closed organ on the executing path.
2. **Organ → bypass** (no bypassable glob): each guard's path/string match actually catches
   the writes it claims to, with its evasion vectors enumerated honestly.

The register is small (three zones); the enforcement mesh is large (~31 mechanical points).
Most of the mesh is **structural/freshness gating** (pre-commit + session hooks), which is
*not* zone enforcement and is out of #188's scope except where noted.

---

## Enforcement-organ inventory (the executing-path guards)

**PreToolUse guards (the only fail-closed *zone* organs):**
- **`~/.claude/hooks/block-onedrive.ps1`** (global) — matcher `Bash|PowerShell`. Reads
  `tool_input.command`; `if ($command -match "OneDrive - Blue Yonder")` → `decision:block`,
  `exit 2`; else `exit 0`. **10 lines** (`block-onedrive.ps1:1-10`).
- **`scripts/hooks/block_immutable_edits.py`** (hub) — matcher `Edit|MultiEdit|Write|NotebookEdit`.
  Zone `_ZONE_SEGMENT = "/docs/decisions/transcripts/"` (`:83`), matched case-insensitively
  (`if _ZONE_SEGMENT in norm.lower()`, `:113`) on a canonicalized path (`normpath` +
  `realpath`). `MUTATING_TOOLS` blocked in-zone; `CREATE_CAPABLE = {Write, NotebookEdit}`
  allowed to *create* new files (lifecycle). Fail-closed in-zone, fail-open out-of-zone
  (ADR-77).

**`permissions.deny` globs:** **none exist** — neither project `.claude/settings.json`
(only `permissions.allow: ["Workflow"]`, `:63-67`) nor global `~/.claude/settings.json`
(no `deny` key). See Finding 3.

**Pre-commit gates (`.pre-commit-config.yaml`, 9 hooks — structural, not zone):**
8 blocking — `normalize-dated-headers`, `codemap-freshness`, `toc-freshness`,
`toc-freshness-playbook`, `validate-backlog`, `audit-health` (`audit.py health`), `ruff`,
`backlog-id-on-close` (commit-msg) — + 1 non-blocking nudge (`coherence-nudge`, exits 0
always).

**Stop hooks:** hub-local `session_end_backpressure.py` (ADR-85 hard JOURNAL gate + advisory
legs) + plugin `propose_closures.py` (detect-and-propose; never mutates). Session-discipline,
not zone enforcement — but see Finding 4 (C1), where the JOURNAL gate had a coverage hole of
its own.

**SessionStart hooks:** all fail-soft surfacing (`fleet_health`, `surface_triage`,
`billing_leak_sentinel`, `changelog_sentinel`, global `surface-closures`). No zone role.

---

## Coverage matrix — ADR-75 register zones × organs

| Zone (register) | Path pattern | Enforcing organ | Tools covered | Posture | Uncovered? | Bypass verdict |
|---|---|---|---|---|---|---|
| **P0 exclusion** (ADR-75 founding) | any path containing `OneDrive - Blue Yonder` | `block-onedrive.ps1` | `Bash`, `PowerShell` only | fail-closed | **No** | **Partial** — string-match on `tool_input.command`; does not see `Edit`/`Write` `file_path` (Finding 1) |
| **Immutable-paths** (ADR-77) | `docs/decisions/transcripts/**` (incl. `archive/`) | `block_immutable_edits.py` | `Edit`, `MultiEdit`, `Write`, `NotebookEdit` | fail-closed in-zone | **No** | **Low** — canonical (`normpath`+`realpath`), case-insensitive; residual = shell-tool writes (Finding 2) |
| **methodology_surface** (ADR-78) | child-floor whitelist/blacklist (`CLAUDE-FLOOR.md`) | `audit.py floor_integrity` + child `.sha256` pre-commit + `/ship` gate | (commit-path, not PreToolUse) | conditional-FAIL + gate warn | **No** | **Low** — hash-verified; not a runtime PreToolUse class (Finding 5) |

**Verdict on #188's primary question: no zone in the ADR-75 register is uncovered.** All
three have an organ on their executing path. The findings below are *bypass-surface* and
*deny-layer* observations, not uncovered zones.

---

## Findings

### Finding 1 — P0 OneDrive guard is tool-scoped to the command string (not a glob bypass, a *channel* gap)
`block-onedrive.ps1` reads only `tool_input.command` and only fires on the `Bash|PowerShell`
matcher. Two clarifications, stated honestly:
- **Case variation does NOT bypass.** PowerShell `-match` is case-*insensitive* by default
  (`-cmatch` is the case-sensitive operator). `"onedrive - blue yonder" -match "OneDrive - Blue
  Yonder"` is `$true`. An earlier first-pass read called this a case bypass; that was wrong.
- **Real residual:** the guard inspects the *command string*, so an `Edit`/`Write`/`MultiEdit`
  with a `file_path` inside an excluded OneDrive path is **not** seen by this hook (those tools
  aren't on its matcher, and it doesn't read `file_path`). In practice excluded paths sit
  outside the repo and the global CLAUDE.md §P0 + `core-invariants.md` #1 forbid them by
  convention, but there is **no PreToolUse `file_path` guard** for the P0 zone — only a
  command-string guard. A path built indirectly (variable, piped) can also evade a substring
  match. *Severity: MEDIUM — the most exploitable channel in the mesh, though the realistic
  blast radius is small (excluded paths are off-repo).*

### Finding 2 — Transcript immutability guard is robust; one documented residual
`block_immutable_edits.py` resists the obvious evasions: `..` escapes collapse under
`normpath` (an in-zone-looking path that resolves out is correctly *allowed*); symlink/junction
aliases resolve under `realpath`; the match is case-insensitive; all four mutating tools are
enumerated; `Write`/`NotebookEdit` may still *create* (lifecycle) but not *overwrite*.
**Residual (already documented in the hook's own honesty section):** shell-tool mutations —
`Set-Content`, `>>`, `git checkout -- <transcript>` via `Bash`/`PowerShell` — are **not**
caught, by design (a shell-write guard would over-block legitimate reads). Tracked as future
work under BACKLOG #112. *Severity: LOW (known, bounded, documented).*

### Finding 3 — There is no `permissions.deny` layer at all — and that is deliberate
The "deny-rule" half of #188's title resolves to: **zero deny globs exist**, by design. The
project `settings.json` `//permissions` note states it explicitly — *"NO Write/Edit deny is
committed by design: deny beats allow with no path carve-outs, so a blanket deny would break
BOTH local daily work and the routine's own digest write. Cloud subagent containment is
instead provided by platform guards."* So defense rests entirely on (a) the two PreToolUse
guards above and (b) platform guards for the cloud path (Routines push only to `claude/*`,
every run lands in a no-auto-merge PR, conformance agents are read-only). *This is a recorded
design choice, not a coverage gap — but it means the register's enforcement has **no
defence-in-depth at the permissions layer**; a PreToolUse hook that fails open is the whole
backstop for its zone.* *Severity: INFORMATIONAL.*

### Finding 4 — C1 (folded in): the ADR-85 Stop gate had a cross-session coverage hole + a vacuous-empty-range pass — **fixed this session**
A #188-shaped finding in a non-register organ. `check_journal_sha_anchor()` in
`scripts/session_end_backpressure.py` computed its commit arc as `_base_ref()..HEAD` where
`_base_ref()` resolved to `@{upstream}` (= `origin/main`, the **push** boundary). Under
deferred-serial-push that arc spans **multiple sessions**, and `any(sha[:7] in added ...)` let
**one** citation from a *prior* session vaccinate the whole arc → a later session that shipped
commits without journaling **passed silently** (witnessed on the 2026-06-18 arc: prior SHAs
`8e6a4ab/8d7b250/496016a` cited → this session's `7e6f996/e97ac47` rode free). Secondary: a
bad/missing base made `git rev-list base..HEAD` error → empty list → **vacuous PASS**.
**Fix (this session):** the arc is narrowed to the **session boundary** (commits since the
last JOURNAL-citing commit; `--first-parent` so a `--no-ff` merge that carries the branch's
journal still anchors), and a rev-list error now anchors on HEAD instead of vacuous-passing.
Recorded in the **ADR-85 2026-06-19 amendment**; witnessed by the regression tests
`test_e2e_cross_session_miss_blocks` + `test_session_shas_bad_base_anchors_head`.
*Severity: HIGH (a hard gate that silently let its target slip) — now closed.*

### Finding 5 — methodology_surface is hash-gated at commit/ship time, not a runtime class
ADR-78's `methodology_surface` zone is enforced by `audit.py floor_integrity` + a child
`.sha256` pre-commit + a `/ship` gate warning, not by a PreToolUse guard. That is appropriate
(the surface is a generated artifact, not a live-edit target), and it is hash-verified, so
silent drift is caught. Noted only so the matrix is complete: this zone's organ is on the
*commit* path, not the *tool-call* path. *Severity: NONE.*

---

## Self-check / reconciliation

- **"No uncovered zones" vs Findings 1–2 (bypass surfaces).** Not contradictory: every zone
  *has* an organ (coverage), and separately some organs have *bypass surfaces* (depth). #188
  asks both questions; the answers are "none uncovered" + "two bounded bypass surfaces + a
  deliberate no-deny posture."
- **Finding 1 "case bypass" retraction.** The PowerShell `-match` case-insensitivity was
  verified; the retraction is recorded so a future audit does not re-flag a non-issue.
- **Finding 4 vs scope.** C1 is in a Stop hook, not an ADR-75 register zone — folded in per
  the #188 ruling (C1 is a #188-shaped coverage hole), not a claim that the register itself
  was breached.

---

## Summary — what this audit emits (the #188 deliverable)

**Uncovered zones:** **none.** All three ADR-75 register zones (P0 OneDrive, transcripts,
methodology_surface) have a fail-closed organ on their executing path.

**Bypassable / residual surfaces (honest list):**
1. P0 OneDrive guard sees only the Bash/PowerShell *command string*, not `Edit`/`Write`
   `file_path` — MEDIUM (small realistic blast radius; off-repo paths). No `file_path` guard
   exists for the P0 zone.
2. Transcript guard does not catch shell-tool mutations (`Set-Content`/`>>`/`git checkout`) —
   LOW, documented, BACKLOG #112.
3. **No `permissions.deny` layer** anywhere — deliberate (deny-beats-allow has no carve-outs);
   defense is PreToolUse hooks + platform guards only. INFORMATIONAL.
4. **C1** — the ADR-85 JOURNAL Stop gate's cross-session vaccination + vacuous-empty-range
   pass — HIGH, **fixed this session** (ADR-85 2026-06-19 amendment + regression tests).

**Possible follow-ups (not filed by this read-only audit; for the operator / closure loop):**
a `file_path` PreToolUse guard for the P0 zone (closes Finding 1); the shell-write transcript
guard already tracked as #112.

---

*Audit produced read-only on 2026-06-19 (BACKLOG #188; refs #112, #132, ADR-75, ADR-77,
ADR-78, ADR-85). No source files were modified by this audit; the C1 fix it folds in is a
separate commit in the same session.*
