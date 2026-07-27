# Codex Review — 436-ratchet-clear

**Date:** 2026-07-27
**Branch:** `feat/436-silent-rule-ratchet`
**HEAD:** `1ea5d5e3`
**Diff range:** `527958fb..feat/436-silent-rule-ratchet`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

FOURTH pass. Prior rounds: R1 5 HIGH, R2 3 remaining, R3 2 remaining. Those 2 are claimed fixed in 1ea5d5e3. Verify ONLY whether any BLOCKING/HIGH defect remains:
1. _target_baseline_state() now models valid/absent/invalid/unresolved and proves absence with 'git cat-file -e'. Is the raise-guard fail-open genuinely closed? Any path where a raise passes uncompared?
2. iter_scoped_files() now derives the corpus from 'git ls-files -s -z', excludes symlinks/gitlinks, refuses casefold-colliding tracked paths, and raises DetectorError rather than degrading. Any remaining platform-dependence or non-determinism in the measured set?
State RESOLVED or STILL HIGH for each. Report any NEW blocking defect introduced by these two changes. If nothing blocking remains, say so explicitly.

---

## Findings
Verdict:

1. `_target_baseline_state()`: **STILL HIGH**
2. `iter_scoped_files()`: **STILL HIGH**

Blocking findings remain.

## Critical

(none)

## High

### HIGH [scripts/audit.py:2623](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2623>) — Git probe failures are treated as proven absence

**What:** Every nonzero `git cat-file -e` result follows the `absent` path, although nonzero also covers inaccessible/corrupt objects, promisor-fetch failures, and other Git errors.  
**Why:** A resolved target with an existing but inaccessible baseline returns `("absent", None)`, allowing a raised branch baseline to pass as bootstrap without comparison.  
**Fix direction:** Use a tree-entry query that distinguishes rc=0/empty absence from command failure, and classify every error or inconsistent probe as `invalid`.

### HIGH [scripts/audit.py:2637](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/audit.py:2637>) — First valid integration ref can conceal a raise over the other

**What:** The function returns the first valid baseline—`origin/main` before `main`—without reconciling both resolved refs.  
**Why:** If `origin/main` has 500 and an ahead local `main` has 400, a branch baseline of 450 passes against 500 despite raising the actual local integration target from 400.  
**Fix direction:** Require resolved refs to agree, explicitly establish the integration target, or compare against the minimum valid baseline; block ambiguous/divergent states.

### HIGH [scripts/silent_rule_detector.py:240](</C:/Users/1028120/Documents/Dev/.dev-knowledge/scripts/silent_rule_detector.py:240>) — Git defines the path list, but the host filesystem still defines measured content

**What:** `ls-files -s` supplies index paths and blob IDs, but the IDs are discarded and each path is reopened from the working tree. The casefold guard also misses normalization-equivalent names such as NFC/NFD variants.  
**Why:** Smudge filters, filesystem aliases, junction/symlink ancestors, or normalization-insensitive filesystems can make the same index measure different bytes—or count one physical file twice—across hosts.  
**Fix direction:** Retain the index blob IDs and read content through Git, then reject normalized-and-casefolded path collisions before measurement.

Validation: 1,830 tests collected; six focused ratchet tests passed, but none covers these three states.
