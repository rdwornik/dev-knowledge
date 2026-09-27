# Codex Review — lane-handoff-min

**Date:** 2026-09-27
**Branch:** `worktree-lane-handoff-min`
**HEAD:** `b8d12772`
**Diff range:** `main..worktree-lane-handoff-min`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/4/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: LANE-5B4-17-handoff-min.md (H:\My Drive\CLAUDE PROMPT DIR\LANE-5B4-17-handoff-min.md) -- Part A of PROPOSAL-ADR-HANDOFF-SYSTEM-2026-09-26.md. Review scripts/handoff_state.py (new), the gen_handoff.py/verify_handoff_probes.py wiring (BOOT_DATA_RULES, verify_boot's BD-manifest check, bundle_manifest/publish_bundle/verify_published), the SUPPLEMENT fixed-slots gate (SUPPLEMENT_FIXED_SLOTS, fixed_slots, assert_supplement_fixed_slots, and its _FIXED_SLOT_LINE_RE regex), and the template/command-doc edits.

---

## Findings
## CRITICAL

## [CRITICAL] scripts/gen_handoff.py:2304 — Manifest paths can escape the publish destination

**What:** `publish_bundle()` joins unvalidated manifest keys to both source and destination paths.  
**Why:** A `../` or absolute key in a modified receipt can read outside the bundle and overwrite files outside `dest_dir`.  
**Fix direction:** Reject absolute/traversal paths and verify resolved paths remain under their respective roots before copying.

## HIGH

## [HIGH] scripts/gen_handoff.py:2974 — Normal post-fill assembly invalidates the manifest

**What:** The manifest is written during the cold generation, before the documented fill-and-rerun-assembler flow changes `SUPPLEMENT.md`, framing files, and `PASTE_THIS.md`.  
**Why:** A legitimate filled bundle subsequently fails `BD-manifest`, making the integrity check unusable at handoff time.  
**Fix direction:** Refresh/seal the manifest after the final post-fill assembly, or explicitly scope it to immutable artifacts.

## [HIGH] scripts/verify_handoff_probes.py:1377 — BD-manifest does not validate the manifest’s file set

**What:** Verification hashes only paths listed in `manifest.files`; it never compares that list with the actual bundle contents.  
**Why:** Removing an altered file’s entry from the receipt, or adding an unlisted file, produces a passing integrity result despite the “every bundle file” claim.  
**Fix direction:** Enumerate non-receipt bundle files and require an exact path-set match before comparing hashes.

## [HIGH] scripts/gen_handoff.py:2316 — `verify_published()` treats a missing manifest as verified

**What:** A readable receipt with no `manifest.files` yields an empty loop and returns `[]`.  
**Why:** Callers interpret `[]` as a successful publish verification, so legacy or malformed receipts silently pass.  
**Fix direction:** Fail closed when the receipt lacks a non-empty, valid manifest, matching `publish_bundle()`’s behavior.

## [HIGH] .github/workflows/conductor.yml:97 — Matrix job names break CI verdict regression attribution

**What:** The pytest matrix creates job names such as `pytest (ubuntu-latest)`, while `ci_verdict` selects only a job named exactly `pytest`.  
**Why:** CI verdicts can no longer read the suite-gate logs or identify actual regression node IDs, degrading handoff CI-state data to job-level failures.  
**Fix direction:** Update the CI verdict consumer to handle both matrix legs (or retain a stable non-matrix aggregation job).

## MEDIUM

(none)

## LOW

(none)