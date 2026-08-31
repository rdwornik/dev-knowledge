# LANE batch-e-b-2-essentials-and-claude-md — ONE lane, two acts in order: dissolve ESSENTIALS, then purify CLAUDE.md's genre. DC-2 and DC-3 merged by architect ruling CUT-3(a).

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — an on-machine committing lane in its own worktree.

```
Dispatch-Lane lane-b-2-essentials-and-claude-md LANE-b-2-essentials-and-claude-md.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT.** Batch E's codespace admission probe came back RED on
2026-08-31 (`RemoteExitCode=1`, agent unauthenticated —
`docs/audits/2026-08-31-verification-codespace-admission-probe.md`).

## Worktree pairing

slug `lane-b-2-essentials-and-claude-md` -> branch `worktree-lane-b-2-essentials-and-claude-md` -> contract `LANE-b-2-essentials-and-claude-md.md`

## WHY THIS IS ONE LANE AND NOT TWO — architect ruling CUT-3(a)

DC-2 and DC-3 both write `CLAUDE.md`. Split across two lanes they buy no parallelism and cost a
merge-order constraint plus a near-certain conflict. **A dependency chain is a LANE, not a
schedule.** They run SEQUENTIALLY INSIDE this one worktree, in the order below. Predicate 6 of
the `[#591]` validator now REFUSES a batch whose declared write-scopes intersect, so this
merge is what makes the freeze pass rather than a preference.

## Write-scope (frozen)

- `protocols/ESSENTIALS.md`
- `protocols/PLAYBOOK.md`
- `CLAUDE.md`
- `templates/claude-regions/first-read.md`
- `templates/claude-regions/critical-rules-consistency.md`
- `templates/claude-regions/antipatterns-universal.md`
- `templates/claude-regions/conventions-commit-branch.md`
- `templates/claude-regions/conventions-output-formatting.md`
- `templates/child-methodology-floor.md.tmpl`
- `tests/test_claude_md_byte_cap.py`

## Done-contract (immutable)

1. **ESSENTIALS is dissolved** — always-on imperatives relocated to the thin `CLAUDE.md` / floor
   carrier, reference material to `protocols/PLAYBOOK.md`, the file archived, and every
   "ESSENTIALS summarizes PLAYBOOK" clause removed from `CLAUDE.md`.
2. **A consumer the census shows would BREAK stops this lane.** Name it and STOP — do not route
   around it, do not repair it in passing.
3. **CLAUDE.md's genre is purified** — the branch-prefix enum and the TUI output-formatting
   rationale RELOCATED to PLAYBOOK with pointers, each to a NAMED destination.
4. **The two `ObsidianVault/` lines are DELETED outright** (`:40`, `:77`), unconditionally, per
   ruling CUT-2. Both are repo-owned, so this is hub-local with zero fleet consequence.
5. **The byte budget is re-gated** — `tests/test_claude_md_byte_cap.py`, ceiling 24,576 B.
6. **The VISION lines (`:39`, `:68`) are removed LAST and ONLY IF DC-1 has merged.** If it has
   not, the lane stops and reports itself partially complete rather than landing them early.
7. **Every hub-region edit lands in BOTH places** — `CLAUDE.md` and its
   `templates/claude-regions/*.md` source — or the byte-match discipline breaks.

## ACT ONE — DC-2, ESSENTIALS dissolution

On the batch-D census (`docs/audits/2026-08-29-census-essentials-consumers.md`), sharpened by
tier (A)'s A3 stale-doctrine census when it harvests.

1. **Always-on imperatives** -> the thin `CLAUDE.md` / floor carrier.
2. **Reference material** -> `protocols/PLAYBOOK.md`.
3. **`ESSENTIALS.md` archived.**
4. **Every "ESSENTIALS summarizes PLAYBOOK" clause removed** — `CLAUDE.md` `:16` `:25` `:29`
   `:97` `:201`. All five locators were resolved at freeze and all five hit exactly.

**REFUSE-TO-PROCEED CLAUSE, from the brief and NOT softened: a consumer the census shows would
break ⇒ NAME IT AND STOP.** Do not route around it, do not "fix it while here". Stop and report.

## ACT TWO — DC-3, CLAUDE.md genre purification

Batch-D lane c cut BYTES; this cuts GENRE. Every removal is a relocation to a NAMED destination,
except the two ruled deletions.

1. **Relocate to PLAYBOOK with a pointer:** the branch-prefix enum (`:63`) and the TUI
   output-formatting rationale (`:81`).
2. **DELETE OUTRIGHT — ruled, unconditional (CUT-2):** the `ObsidianVault/ (pre-sales — do not
   mix)` lines at `:40` and `:77`. **Both are REPO-owned** (verified against the
   `methodology:start/end` markers at freeze), so this is hub-local with zero fleet
   consequence. The operator defines his own mixing rules.
3. **Re-gate the byte budget** — `tests/test_claude_md_byte_cap.py`, ceiling 24,576 B.

## ACT THREE — LAST, and CONDITIONAL

**Remove VISION from `CLAUDE.md` `:39` (critical paths) and `:68` (living docs) — ONLY after
DC-1 has MERGED.** These are VISION-retirement edits that must ride the CLAUDE.md lane
(CUT-3(c)). If DC-1 is not yet merged when you reach this act, **STOP and report the lane as
partially complete**; do not land it early and do not wait idle inside the lane.

## THE HUB-REGION FACT YOU MUST NOT DISCOVER LATE

Six of the eleven cited lines sit inside `<!-- methodology:start … owner=hub -->` regions whose
bodies are **byte-identical** to `templates/claude-regions/*.md` and are deploy-carried to every
ADR-104 member: `:25` `:29` (first-read), `:63` (conventions-commit-branch), `:81`
(conventions-output-formatting), `:97` (critical-rules-consistency), `:201`
(antipatterns-universal). **Editing them means editing the region template too**, which is why
those templates are in the write-scope.

**This is RULED NOT A BLOCKER (CUT-2).** The hub regions are the SOURCE OF TRUTH; consolidating
them IS the DOCTRINE CONSOLIDATION arc. The DEPLOYMENT WAVE's `blocked_by` says do not SHIP a
churning corpus — not do not CHANGE it. A parity window between this merge and the first
consumer deploy is EXPECTED and DECLARED, and closes on `hub -> monorepo`.

## Decision budget

**V-2 — escalate on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. A refuted premise PAUSEs
with the fact (Q10).

## Steps

1. `/preflight` every locator this contract cites — all eleven were live at freeze; re-verify,
   because line numbers rot in-branch.
2. ACT ONE, then its targeted tests. 3. ACT TWO, then the byte-cap re-gate.
4. ACT THREE only if DC-1 is merged. 5. Run the TARGETED tests for this diff. Commit and STOP.

## What NOT to do

- No merges, no pushes to `main` — commit-and-STOP.
- No JOURNAL entry (P-1), no index regeneration (Q1), no row births.
- Do not weaken the REFUSE-TO-PROCEED clause into a warning.
- No edits outside the declared footprint. Prose in English; hyphen-only names.
