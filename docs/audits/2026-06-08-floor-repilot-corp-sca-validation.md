# Floor Re-Pilot Validation — corp-sca-time-automation (.claude/ placement)

<!-- scope: meta -->

**Date:** 2026-06-08
**Pilot repo:** `corp-sca-time-automation` (child)
**Hub:** `.dev-knowledge`
**Decision:** ADR-78 (Child methodology floor — O2 Bounded Hybrid)
**Tests the corrective:** `.claude/` placement + baked install note (hub merges
`5c104e9` / `4f0bd12` / `3f2cc97`, 2026-06-08)
**Backlog:** rollout owned by [#131]; new finding filed [#138]
**Status:** PASS — smooth (zero correction rounds); three witnesses re-confirmed; one
onboarding-friction finding surfaced

---

## Purpose

The first pilot (`docs/audits/2026-06-08-floor-pilot-corp-sca-validation.md`) validated the
floor mechanism but surfaced install-note gaps AND a placement miss: the generator dropped
the floor into the child **repo root**. The hub corrective moved the floor under the
child's `.claude/` and baked every round-1 lesson into the generated install note. This
record is the **re-pilot** — re-running the full onboarding against the corrected mechanism
to prove the re-pilot is friction-free (the smoothness proof the corrective was for).

---

## Procedure (reverse → regen → reinstall)

1. **Reverse the round-1 (root) install** — removed the root-placed `CLAUDE-FLOOR.md`,
   `CLAUDE-FLOOR.md.sha256`, and the round-1 `INSTALL.md` from the child; root left clean.
2. **Regenerate to `.claude/`** — ran the corrected hub generator
   (`generate --out-dir <corp-sca>`); floor + sidecar landed under `.claude/`, and the
   complete install note printed with the child run.
3. **Reinstall from the baked note** — applied the printed runbook verbatim: the
   `@.claude/CLAUDE-FLOOR.md` include, `.claude/check_floor_hash.py`, the
   `.pre-commit-config.yaml` hook entry, and `pre-commit install`.

---

## Smoothness verdict: PASS — zero correction rounds

The re-pilot completed with **no correction rounds** — every round-1 friction was
pre-absorbed into the baked artifacts:

- **`check_floor_hash.py` was ruff-clean on the first try** — the split imports (no E401)
  and `'''`-docstring (no escaped-quote leak) emitted by the generator paste as valid,
  lint-clean Python with no edits.
- **The hook armed correctly** — `pre-commit install` was an explicit step in the note, so
  the round-1 *wired-but-inert* failure did not recur; the floor hash-verify hook fired.
- **The root stayed clean** — the floor + sidecar + hook script all landed under
  `.claude/`; no root clutter to clean up afterward.

---

## Witnesses

### (a)/(c) Floor loaded + re-anchor rule available — PASS

The generated `.claude/CLAUDE-FLOOR.md` auto-loaded in the child CC session via the
`@.claude/CLAUDE-FLOOR.md` include; the re-anchor rule was loaded and available before
structural work (the "re-read the floor before a structural change" mechanic).

### (b) Tamper caught on BOTH sides — PASS

A deliberate edit to the child floor (tamper) was caught by both enforcement surfaces:

- **Child side (pre-commit):** the child's `.claude/check_floor_hash.py` hook exited **1**,
  blocking the commit of the tampered floor.
- **Hub side (`audit.py floor_integrity`):** **FAIL** on hash drift
  (`fe7b0223…`) → restore → **PASS** with the hash back to the sidecar value
  (`4d268f32…`).

Restoring the floor to the committed version (`git checkout HEAD -- .claude/CLAUDE-FLOOR.md`)
returned both detectors to green.

---

## Finding (onboarding friction — fix before fleet rollout)

### (i) `.claude/` is commonly gitignored → the floor needs `.gitignore` negations

Many child repos `.gitignore` the `.claude/` directory (local CC config is typically not
tracked). With the floor now living **under** `.claude/`, the generated floor + sidecar +
hook script are swept up by that ignore rule and will not be tracked without `git add -f` —
force-add friction, and **variable behavior across the fleet** depending on each child's
existing `.claude/` ignore posture. The install note must instruct the child to add
**`.gitignore` negations** so the three floor files are tracked normally:

```
!.claude/CLAUDE-FLOOR.md
!.claude/CLAUDE-FLOOR.md.sha256
!.claude/check_floor_hash.py
```

Routed to **[#138]** (generator install-note enhancement) + annotated onto **[#131]**.

---

## Disposition

- **Re-pilot PASS** — smooth, zero correction rounds; the `.claude/` corrective is validated.
- **[#138]** filed — generator install-note adds the child `.gitignore` negations.
- **[#131]** annotated — per-child `.gitignore` negations + delete any orphaned ROOT floor
  copy on migration to `.claude/` (the hub audit now reads `.claude/` only, so a stray root
  floor is an invisible vacuous-skip).
