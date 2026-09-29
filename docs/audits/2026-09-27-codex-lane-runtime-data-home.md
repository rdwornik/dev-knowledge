# Codex Review — lane-runtime-data-home

**Date:** 2026-09-27
**Branch:** `worktree-lane-runtime-data-home`
**HEAD:** `95674262`
**Diff range:** `main..worktree-lane-runtime-data-home`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/cost_usage_telemetry.py: default_db_path() moved off-tree via platformdirs.user_state_dir; content-capture event refusal (_check_no_content_capture_events); path/token redaction (_redact_string / _redact_json_value) applied to error.type, gen_ai.conversation.id and events payloads, deliberately excluding devknowledge.run_id from the token scan
- tests/test_telemetry_redaction.py (new): RED-first proof of both refusal and redaction, plus a regression lock that a real 32-hex run_id survives the scan unmarked
- tests/test_routing_telemetry.py: three new tests proving default_db_path() resolves outside the repo tree, is stable across worktrees/cwd, and still honors the env override
- tests/test_fleet_shape_spec_readers.py: DECIDED-BY-LANE edit widening an existing ratchet test to admit one new legitimately-unasserted clause
- Look specifically for: redaction regex false positives/negatives, any path where content-capture refusal could be bypassed, correctness of the off-tree path resolution, and whether excluding run_id from the token scan is safe

---

## Findings
## Critical

### scripts/cost_usage_telemetry.py:503 — Content-capture refusal is trivially bypassed

**What:** Only three exact event names are refused; a caller can put prompt/response text in any other event’s `body` (or a non-mapping event) and it is serialized.  
**Why:** Ordinary prompt text matches neither redaction regex; the new test explicitly establishes that non-content event bodies are accepted. This breaks the “holds no prompt text” guarantee.  
**Fix direction:** Validate an allowlisted event schema and reject message/body-bearing or unrecognized payloads before serialization; do not use `default=str` for unsupported event values.

### scripts/cost_usage_telemetry.py:612 — The `run_id` exclusion permits unredacted secrets

**What:** Explicit `run_id` values need only be nonblank, then are copied unredacted into both the JSON attributes and database column.  
**Why:** A caller or inherited `DEV_KNOWLEDGE_TELEMETRY_RUN_ID` can supply a token, path, or prompt-derived value; excluding all run IDs is only safe for a validated canonical UUID-hex value.  
**Fix direction:** Exempt only validated generated-format run IDs, and redact or refuse other values before storing them.

### scripts/cost_usage_telemetry.py:456 — Path redaction misses common absolute paths

**What:** The POSIX matcher excludes paths such as `/workspaces/...`, `/srv/...`, `/data/...`, and `/usr/...`; the Windows matcher excludes UNC paths such as `\\server\share\...`.  
**Why:** Those values remain in `error.type`, conversation IDs, and accepted event payloads despite the stated foreign-path protection.  
**Fix direction:** Cover generic absolute POSIX and UNC path forms, with regression cases for Codespaces-style and network paths.

## High

### scripts/cost_usage_telemetry.py:466 — Generic hex-token rule corrupts legitimate conversation identifiers

**What:** Any 32+ hex-character substring in `gen_ai.conversation.id` is replaced as a token.  
**Why:** UUID-hex conversation IDs and hashes are legitimate correlation identifiers, so this silently destroys telemetry joinability; only `run_id` has a regression exemption.  
**Fix direction:** Make token detection context-aware or preserve validated identifier formats, with a UUID-hex conversation-ID regression test.

## Medium

(none)

## Low

(none)