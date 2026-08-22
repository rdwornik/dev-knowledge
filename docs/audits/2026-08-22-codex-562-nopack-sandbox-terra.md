# Codex Review — 562-nopack-sandbox-terra

**Date:** 2026-08-22
**Branch:** `HEAD`
**HEAD:** `7c646699`
**Diff range:** `main...HEAD`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 2/2/0/0

**Disposition (integrator, 2026-08-22): the lane is HELD — NOT merged.** Per the wave-close D1 rule, unfixed Critical/High holds a lane, and both Criticals are CONFIRMED against source at `7c646699`. **This review is exactly what the lane asked for.** Its own artifact declares that `gpt-5.6-terra` was unreachable in its container, that the substitute was an in-lane adversarial pass which *"shares the author's blind spots"*, and that its 0-Critical tally should be **treated as a floor**. It was a floor: real terra found two Criticals the in-lane pass did not.

**C1 — `teardown()` recursively deletes any path handed to `--sandbox`.** Confirmed: `nopack_sandbox.py:574` is `shutil.rmtree(path)` guarded only by `path.exists()`, reached straight from the CLI at `:908`. No marker, no manifest check, no sandbox-root containment. A typo, or a path pointing at a real checkout or a synced directory, destroys it. **This is the hazard class the operator's own P0 exclusion rules exist for** — the recorded history is cleanup scripts that deleted personal files alongside their intended targets — which is why it is held rather than filed forward.

**C2 — provisioning overwrites `<dest parent>/sandbox-manifest.json` unconditionally**, destroying an unrelated file that happens to sit at that path. The manifest belongs inside the sandbox, or needs exclusive creation.

**H1 — a failed provision leaves the full, unstripped clone at `dest`.** Two costs, not one: it violates the no-leftovers rule (Critical Rule #9) **and** it leaves the answer-key content the whole guard exists to strip sitting readable on disk. **H2 — the allowlist screens top-level shell segments while execution is `shell=True` (`:726`), so `cat $(touch file)` runs an unapproved command inside the sandbox** — the advertised read-only command surface is bypassable by substitution.

**None of this bears on leg 3's blocked status**, which is a credentials/network fact and is correctly evidenced in the lane's §2. The guard is a genuine deliverable with a real defect set; the finding is that it is not yet safe to run, not that the lane was idle.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## Critical

- **scripts/nopack_sandbox.py:909**  
  **What:** `teardown` recursively deletes any path supplied to `--sandbox` without verifying it is a provisioned sandbox.  
  **Why:** A typo or malicious argument can delete a real repository or synced directory.  
  **Fix direction:** Require and validate a sandbox-owned manifest/marker and reject paths outside a dedicated sandbox root.

- **scripts/nopack_sandbox.py:873**  
  **What:** Provisioning unconditionally overwrites `<dest parent>/sandbox-manifest.json`.  
  **Why:** An existing unrelated file at that path is silently destroyed.  
  **Fix direction:** Store the manifest inside the sandbox or create it exclusively with collision handling.

## High

- **scripts/nopack_sandbox.py:452**  
  **What:** Failures after `git clone`—for example an invalid `--head` at line 460—leave the full, unstripped clone at `dest`.  
  **Why:** This violates the no-leftovers guarantee and leaves the answer-key content accessible after a failed provision.  
  **Fix direction:** Wrap all post-clone work in cleanup-on-error logic that removes and verifies removal of the created sandbox.

- **scripts/nopack_sandbox.py:640**  
  **What:** The command allowlist inspects only top-level shell segments while execution uses `shell=True` at line 726. Shell substitutions can run unapproved commands, e.g. `cat $(touch file)`.  
  **Why:** The advertised read-only command surface can be bypassed, allowing sandbox mutation or other unintended subprocesses.  
  **Fix direction:** Avoid shell execution and use structured argv validation, or reject shell expansions and compound constructs comprehensively.

## Medium

(none)

## Low

(none)