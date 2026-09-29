# Codex Review — lane-ratified-unbuilt

**Date:** 2026-09-29
**Branch:** `worktree-lane-ratified-unbuilt`
**HEAD:** `c4a095c3`
**Diff range:** `main..worktree-lane-ratified-unbuilt`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: LANE-5B5R-7-ratified-unbuilt.md (WAVE5B-N5-R, row L7).
Diff: adds ecosystem/schema/provider_registry.py::DispatcherPin + ProviderRegistry.dispatcher
(R22, the model the dispatcher session runs on -- deliberately NOT a roles: entry), the
matching dispatcher: row in ecosystem/provider-registry.yaml, and RED-first
tests/test_provider_registry_dispatcher.py. Please check: schema validator correctness
(cross-provider/model checks, evidence-path validation), whether the new field could be
confused with or silently interact with roles.orchestrate, and whether the new tests
actually exercise the validators added (not just extra=forbid).

---

## Findings
## CRITICAL

(none)

## HIGH

### ecosystem/schema/provider_registry.py:584 — Dispatcher evidence is never verified as an in-repo artifact

**What:** The new validator only rejects absolute/climbing paths; no dispatcher-specific check resolves `evidence` and requires an existing regular file.  
**Why:** A relative dead path or directory (for example `docs/missing.md` or `.`) validates, leaving the R22 pin with unverifiable provenance.  
**Fix direction:** Extend the evidence-resolution gate to inspect dispatcher evidence too, and add RED tests for missing and directory evidence.

### tests/test_provider_registry_dispatcher.py:45 — No negative test exercises the undeclared-model validator branch

**What:** The tests cover an unknown provider and a provider/model mismatch, but never mutate `dispatcher.model` to an undeclared ID under a valid provider.  
**Why:** Removing or breaking `ProviderRegistry._the_dispatcher_pin_names_a_declared_provider_and_model`’s undeclared-model check would still leave this test module green.  
**Fix direction:** Add a fixture with `provider: anthropic` and a nonexistent model ID, asserting schema validation fails.

## MEDIUM

(none)

## LOW

(none)