# Codex Review — consumer-instrument-hardening

**Date:** 2026-07-06
**Branch:** `feat/consumer-instrument-hardening`
**HEAD:** `211eea6`
**Diff range:** `main..feat/consumer-instrument-hardening`
**Codex version:** codex-cli 0.141.0
**Mode:** diff-review

---

## Focus

- TRUST SEAM (heterogeneity mandate from root): G3 moves arc authorization from prompt prose to the harness-owned isolated config (ARC_SANCTION written as the profile's user-level CLAUDE.md; ARC_PROMPT only references it). Attack it: can a measured child or the clone's own content forge/alter the sanction? Does the sanction leak the GATE-0 provenance token (false-positive channel)? Is any bypass/defaultMode escape possible via the seeded settings?
- G1: run_consumer_arc now seeds ARC_ALLOW_RULES user-level (untrusted workspace ignores clone-level allows). Verify scope: no rule broader than the four arc ops, no wildcard.
- G2: seed_tier1_plugin(source_root=hub) for consumer measurement — marketplace registers at hub path, projectPath stays the clone. Check path handling + facade risk (are we measuring seeded firing honestly vs manufacturing presence?).
- G4: observe.py skip-echo guard (ARMED-BUT-SKIPPED), VACUOUS tombstone (stage-ran detector _STAGE_RAN_RE), git-state probes (machine-level ~ paths honest, settings-declared enablement). Check the regexes for false classification (a hook whose REAL output line ends with 'Skipped'? a Passed-trailer in non-pre-commit Bash output faking stage-ran?), and the coverage arithmetic in consumer.build_report (armed counted once, never double).

---

## Findings
## CRITICAL

(none)

## HIGH

## HIGH deploy/lived_sandbox/arc.py:211 — allowlist is broader than the arc

**What:** `Bash(git checkout:*)`, `Bash(git add:*)`, and `Bash(git commit:*)` allow any checkout/add/commit variant, not just the three exact arc commands.  
**Why:** A measured child can perform other git state changes inside the clone while still staying inside the harness-owned allowlist, weakening the trust seam.  
**Fix direction:** Narrow the Bash permissions to the exact sanctioned commands from `ARC_PROMPT`.

## HIGH deploy/lived_sandbox/consumer.py:159 — consumer plugin firing can be manufactured

**What:** `run_consumer_arc` seeds the hub plugin into the isolated config unconditionally, before proving the consumer clone declares `tier1-lifecycle@dev-knowledge-methodology` enabled.  
**Why:** A consumer without the deployed plugin setting can still receive harness-created plugin state, so Stop hook or command firing may reflect the harness seed instead of consumer enforcement.  
**Fix direction:** Gate seeding on an exact consumer `.claude/settings.json` enablement check, and report plugin expectations as absent/untrusted when that declaration is missing.

## HIGH deploy/lived_sandbox/observe.py:49 — skip detection is not limited to pre-commit report lines

**What:** Any hook-stdout line containing a signature and ending in `Skipped` is classified as `ARMED-BUT-SKIPPED`.  
**Why:** Non-pre-commit hooks such as Stop or SessionStart can be counted as OK-class skipped even though file-scope skip semantics do not apply to them.  
**Fix direction:** Apply skip classification only to pre-commit expectations and only for lines matching the pre-commit hook report shape.

## HIGH deploy/lived_sandbox/observe.py:52 — stage-ran detection accepts unrelated output

**What:** `_STAGE_RAN_RE` scans the entire hook stdout surface for any line ending `Passed`, `Failed`, or `Skipped`.  
**Why:** A non-pre-commit Bash or hook output line can fake that the pre-commit stage ran, causing the ruff tombstone to become `CORRECTLY-ABSENT` instead of `VACUOUS`.  
**Fix direction:** Derive `precommit_ran` only from the `git commit` Bash result or from known pre-commit hook report lines.

## MEDIUM

## MEDIUM deploy/lived_sandbox/observe.py:287 — plugin enablement probe matches partial settings tokens

**What:** The git-state check marks the tier1 plugin observed when any token from `enabledPlugins tier1-lifecycle@dev-knowledge-methodology` appears in settings.  
**Why:** A settings file with `enabledPlugins` but without the tier1 plugin still reports the plugin declaration as observed.  
**Fix direction:** Parse `.claude/settings.json` as JSON and require `enabledPlugins["tier1-lifecycle@dev-knowledge-methodology"] is true`.

## MEDIUM deploy/lived_sandbox/observe.py:45 — VACUOUS is not surfaced as a gated flag

**What:** `_GATED_FLAG` excludes `VACUOUS`, even though `passed` correctly fails on it.  
**Why:** CLI summaries can say `observer FLAGGED ... flags: none` for the exact tombstone failure G4 added.  
**Fix direction:** Include `VACUOUS` in the gated failure set used by `flags`.

## LOW

(none)
