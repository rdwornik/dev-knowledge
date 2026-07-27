# Codex Review — 436-ratchet-gate5

**Date:** 2026-07-27
**Branch:** `feat/436-silent-rule-ratchet`
**HEAD:** `620f36cc`
**Diff range:** `527958fb..feat/436-silent-rule-ratchet`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

FIFTH pass, final gate. Rounds so far: 5, 3, 2, 3 HIGH -- 13 fixed, none dispositioned. The last three are claimed fixed in 620f36cc:
1. Absence now proven with 'git ls-tree' (rc=0 + empty output) instead of 'git cat-file -e'; failed lookup => invalid (blocking).
2. All resolved refs reconciled: any invalid blocks; comparison uses min() of valid baselines.
3. Content read from the object store via 'git cat-file --batch' on index blob ids; path collisions folded with NFC normalization + casefold.
Verify each is RESOLVED or STILL HIGH. Report any NEW blocking defect. If nothing blocking remains, say so explicitly and plainly.
Scope note: MEDIUM/LOW observations are welcome but are NOT blocking for this gate.

---

## Findings
Three new HIGH defects remain, so this is not clear to merge.

Claimed fixes:

1. **RESOLVED** — `ls-tree` proves absence; lookup failure becomes `invalid`.
2. **RESOLVED** — every resolved ref is considered; invalid blocks and valid baselines use `min()`.
3. **RESOLVED** — scoped content comes from index blob IDs through `cat-file --batch`; collisions use NFC normalization plus casefolding.

## Critical

(none)

## High

### HIGH [scripts/audit.py:2575](C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2575) — Baseline is read from a different snapshot than the measured corpus

**What:** The detector measures staged index blobs, but `_load_silent_rule_baseline` reads the working-tree file directly.

**Why:** With a partially staged baseline, the gate can validate the unstaged value while Git commits a different—potentially raised—value, defeating the commit-time ratchet.

**Fix direction:** Read the current baseline from its index blob using the same object-store snapshot as the detector, and add a staged/working-tree divergence regression test.

### HIGH [scripts/gen_task_tree.py:364](C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/gen_task_tree.py:364) — Task-tree gate validates working-tree bytes instead of committed bytes

**What:** `find_incoherences` reads `BACKLOG.md`, task files, and `manifest.json` from disk.

**Why:** A staged BACKLOG change can be hidden by restoring the working-tree copy before committing; the pre-commit check sees a coherent old tree while the commit records an incoherent source/tree combination.

**Fix direction:** Validate staged index blobs and staged path inventory during the commit gate, with a regression test covering staged-new/source-working-old state.

### HIGH [scripts/audit.py:2645](C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2645) — Integration ref is not held stable across the baseline probe

**What:** `_ref_baseline_state` resolves the ref to an OID, but then ignores that OID and runs `ls-tree` and `show` against the mutable ref name.

**Why:** A concurrent fetch/ref update can make the absence check and content read observe different commits, potentially classifying a target baseline as absent and bootstrapping past a raise.

**Fix direction:** Capture the resolved commit OID once and use that OID for both `ls-tree` and `show`; add a mocked ref-movement regression test.

## Medium

(none)

## Low

### LOW [scripts/audit.py:2740](C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2740) — Ratchet documentation still describes line counting

**What:** The check docstring says “LINE COUNT” and “counts lines,” while detector v4 counts keyword occurrences.

**Why:** It misstates the evidence operators and future maintainers are expected to interpret.

**Fix direction:** Update the wording to “normative-keyword occurrence count.”

Validation: 1,835 tests collected successfully, both live checks passed at `428 / 56 files`, and `git diff --check` was clean. The full suite could not run in the read-only environment because pytest requires writable temporary storage.
