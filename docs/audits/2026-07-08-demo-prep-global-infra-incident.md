# Demo-prep Pass-D global-infra incident + hub ratify-or-revert — 2026-07-08

<!-- scope: meta -->

> **What this is.** The motivating incident record for the hub's global-infra ratify-or-revert
> ruling of 2026-07-08. Demo-prep's Pass D (2026-07-07/08) made operator-ruled but
> **hub-unratified** changes to global infrastructure (`~/.claude/…`), which per core-invariant
> **#6** (global-infra edits = exception-with-ruling, never unilateral) sat live-on-disk pending
> `.dev-knowledge` ratification. The source audit trail is demo-prep
> `docs/audits/2026-07-08-global-infra-changes-dossier.md`, imported verbatim below (no operator
> paste was provided; the dossier is the available source). This file is the hub's immutable
> record (docs/audits are immutable, CLAUDE.md §5).

## Hub resolution (operator-ratified ruling, 2026-07-08)

Per-item disposition of the live-on-disk `~/.claude` changes:

- **invariant #1 sanctioned-SharePoint-source amendment → REVERTED (partial).** Enumerated
  source **(2)** (the SharePoint "Blue Yonder Platform - Documents" library bullet) removed from
  `~/.claude/rules/core-invariants.md` #1, leaving `sync-mywork.ps1` as the sole enumerated
  sanctioned read source. The "write/delete class" reword and rule **#6** are KEPT (a hand edit
  per the dossier's Partial-revert step 1, not a blanket `git checkout`).
- **`block-onedrive.ps1` guard v2 (fail-closed read-only allow-list, Read-tool gating) → KEPT**
  as ratified live state.
- **`settings.json` PreToolUse matcher `…|Edit|Write|NotebookEdit|Read` → KEPT** as ratified
  live state.
- **rule #6 (global-infra edits are exception-with-ruling) → KEPT.** Its canonical home is
  **pending the #153 methodology-reach decision** (whether ecosystem enforcement owns `~/.claude`).

**Flag (recorded, safe-direction):** keeping the hook's allow-list while removing the SharePoint
source from the rule leaves the **hook more permissive than the rule** — the hook still ALLOWS a
read of the sanctioned library, while rule #1 no longer enumerates it (so a rule-following agent
would "stop and ask"). This diverges from the dossier's Partial-revert step 2 (which neuters the
hook's `$SANCTIONED` to a sentinel so nothing is sanctioned). No write/delete hole; the divergence
is read-only and rule-stricter-than-hook. One-line convergence if later desired:
`$SANCTIONED = 'OneDrive - Blue Yonder\__none__'` in the hook.

**Follow-on:** the fleet-level ownership of this guard + the global-edit-governance standard is
tracked by hub `[#289]` (hub-own the OneDrive guard; versioned canonical source + policy + deploy
carrier + Informant coverage) — to be filed on the grooming-apply batch. **No fleet-roll / deploy
until this ratify-or-revert lands.**

---

## Source dossier (demo-prep `docs/audits/2026-07-08-global-infra-changes-dossier.md`, verbatim)

# Global-infra changes dossier — Pass D — 2026-07-08

**Why this exists:** Pass D required changes to **global/hub infrastructure** outside this repo (`~/.claude/…` and `.dev-knowledge/`). Per core-invariant **#6** (global-infra edits = exception-with-ruling, never unilateral), those changes are **operator-ruled but NOT committed** — they sit live-on-disk pending **`.dev-knowledge` ratification** (operator directive, 2026-07-08). This dossier is the audit trail: per file — what changed, the ruling that gated it, current state, and the **exact revert command** — plus a **partial-revert recipe** and the **ready-to-paste hub `[#289]`** entry.

**Scope note:** none of this touched the demo-prep tracked set (the Pass-D repo work is separate + merged). `~/.claude/skills/gotchas/gotchas.md` is dirty from **another session** — NOT a Pass-D change; excluded from everything here.

---

## Changes live on this machine (uncommitted)

### 1. `~/.claude/rules/core-invariants.md` — enumerated sanctioned source (#1) + new rule #6
- **What changed:** (a) **#1** gains a 2nd enumerated **sanctioned READ-ONLY source** — the SharePoint "Blue Yonder Platform - Documents" library (site `https://jda365.sharepoint.com/sites/BlueYonderPlatform`); "exclusion zone" reworded to *write/delete class*. (b) New **#6** — "global-infra edits are exception-with-ruling, never unilateral."
- **Ruling that gated it:** operator ruling 2026-07-07 — "record as a PERMANENT invariant amendment, NOT a one-time exception" (source-access decision); + the META ruling "global-infra edits = exception-with-ruling."
- **Current state:** `M rules/core-invariants.md` (modified, uncommitted).
- **Revert (full):** `git -C ~/.claude checkout -- rules/core-invariants.md`

### 2. `~/.claude/hooks/block-onedrive.ps1` — rebuilt guard (v2)
- **What changed:** the blunt substring-block was rebuilt into a **fail-closed read-only ALLOW-LIST** that (a) blocks all Edit/Write/NotebookEdit into the zone, (b) gates the **Read tool** (sanctioned library + non-video only), (c) allows only provably-read-only Bash/PowerShell commands referencing solely the sanctioned library. Matrix-proven (9/9). The temporary **copy-FROM exception (v3)** used for the 4-PDF copy was **reverted byte-identical to v2** (proven: `git diff --no-index` → identical, 0 copy-FROM markers).
- **Ruling:** operator rulings 2026-07-07 — "Option 1 (durable patch) with allow-list amendment"; "harden to gate the Read tool"; "copy-FROM exception dies this session."
- **Current state:** `M hooks/block-onedrive.ps1` (= v2). Two backups (untracked): `block-onedrive.SUPERSEDED.ps1` (the **original** pre-Pass-D guard), `block-onedrive.SUPERSEDED-2026-07-07-allowlist-v1.ps1` (v1, pre-Read-gate).
- **Revert (to original):** `git -C ~/.claude checkout -- hooks/block-onedrive.ps1` (restores the committed original) **or** `cp ~/.claude/hooks/block-onedrive.SUPERSEDED.ps1 ~/.claude/hooks/block-onedrive.ps1`.

### 3. `~/.claude/settings.json` — PreToolUse matcher gains `Read`
- **What changed:** the `block-onedrive` PreToolUse matcher `Bash|PowerShell|Edit|Write|NotebookEdit` → `…|Read` (so the hook can gate the Read tool). Hot-reloaded live this session (verified: a non-sanctioned Read was blocked).
- **Ruling:** operator ruling 2026-07-07 — "harden: add Read to the hook."
- **Current state:** `M settings.json` (modified).
- **Revert:** `git -C ~/.claude checkout -- settings.json`

### 4. Untracked backups (2)
- `~/.claude/hooks/block-onedrive.SUPERSEDED.ps1`, `…SUPERSEDED-2026-07-07-allowlist-v1.ps1` — rollback copies.
- **Revert (remove):** `rm ~/.claude/hooks/block-onedrive.SUPERSEDED*.ps1`

### 5. `.dev-knowledge/BACKLOG.md` — `[#289]` (REVERTED)
- **What changed / state:** `[#289]` (hub-own the OneDrive guard) was added, then **reverted/lost** by the concurrently-active hub session (its own `M JOURNAL.md` work). **Not currently filed.** Ready-to-paste text in §Appendix; operator will file when the hub is quiescent.

---

## Full revert (undo ALL Pass-D global changes)

```sh
git -C ~/.claude checkout -- rules/core-invariants.md hooks/block-onedrive.ps1 settings.json
rm ~/.claude/hooks/block-onedrive.SUPERSEDED.ps1 ~/.claude/hooks/block-onedrive.SUPERSEDED-2026-07-07-allowlist-v1.ps1
# .dev-knowledge/[#289] was already reverted — nothing to undo there.
```

## Partial revert — drop the sanctioned SOURCE, KEEP the guard hardening + rule #6

Use this if the operator ratifies the *guard improvement + governance rule* but NOT the BY-Platform read carve-out:

1. **`core-invariants.md`** — manual edit: in **#1**, delete enumerated source **(2)** (the entire "The SharePoint **Blue Yonder Platform - Documents** library …" bullet), leaving `sync-mywork.ps1` as the sole enumerated source. **Keep #6 and the "write/delete class" reword.** (A blanket `git checkout` would also drop #6 — so this leg is a hand edit, not a checkout.)
2. **`block-onedrive.ps1`** — to stop the guard *allowing* that library while keeping the Read/Edit/Write gating + fail-closed structure: set `$SANCTIONED` to an unmatchable sentinel (e.g. `$SANCTIONED = 'OneDrive - Blue Yonder\__none__'`). The hook then blocks **all** zone reads (nothing sanctioned) but retains the improved Read-tool gating + allow-list. *(Alternative: `cp …SUPERSEDED.ps1` to fully restore the original blunt block — but that loses the Read-tool gating.)*
3. **`settings.json`** matcher `+Read` — **keep** (harmless; the hook then simply blocks every zone Read).

Net: the OneDrive exclusion zone is fully closed again (no sanctioned reads), but the guard is materially better than pre-Pass-D (Read-tool now gated; Edit/Write file_path now covered; fail-closed allow-list) and rule #6 stands.

---

## Appendix — ready-to-paste hub `.dev-knowledge/BACKLOG.md` entry (operator files when quiescent)

> Number `[#289]` is the placeholder used across Pass D; assign the actual next id at file time.

```
- [#289] [P2][L] Ratify (or revert) the Pass-D global-infra change-governance standard + the OneDrive read-only guard — Pass D (demo-prep, 2026-07-07/08) made operator-ruled but hub-unratified changes to `~/.claude` (see demo-prep `docs/audits/2026-07-08-global-infra-changes-dossier.md`): (a) a **sanctioned READ-ONLY source model** for a specific OneDrive/SharePoint library (core-invariants #1); (b) the **`block-onedrive.ps1` guard redesign** — blunt substring-block → **fail-closed read-only allow-list** covering Edit/Write file_path + a **Read-tool guard** (sanctioned + non-video only); (c) **core-invariant #6** — "global-infra edits are exception-with-ruling, never in-session/unilateral." These are per-machine + ad-hoc; the OneDrive-guard + the global-edit-governance standard are **fleet-level** and should be hub-owned (versioned canonical hook + policy, carried by the deploy subsystem ADR-91/92, measured by the Informant Organ), NOT per-machine. · Done when: the hub RATIFIES the standard (canonical versioned guard + policy doc + deploy carrier) or RULES a revert (dossier's full/partial recipe), AND the ratify-or-revert decision for the changes currently live on this machine is recorded · refs demo-prep docs/audits/2026-07-08-global-infra-changes-dossier.md, ~/.claude/hooks/block-onedrive.ps1, ~/.claude/rules/core-invariants.md (#1, #6), #191, #188, #189, #236, ADR-91, ADR-92, ADR-75 · serialize-group: settings-json
```
