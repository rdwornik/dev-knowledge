# Codex Review — lane-runtime-data-home-followup

**Date:** 2026-09-27
**Branch:** `worktree-lane-runtime-data-home`
**HEAD:** `26371a04`
**Diff range:** `main..worktree-lane-runtime-data-home`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- This is a follow-up review of LANE-5B4-15-runtime-data-home after the first codex-review
  (docs/audits/2026-09-27-codex-lane-runtime-data-home.md) found 3 Critical + 1 High in the
  first-pass redaction design in scripts/cost_usage_telemetry.py.
- Confirm whether each of the four findings from that prior review is actually resolved by
  this diff: (1) deny-by-default _PERMITTED_EVENT_NAMES replacing the refused-3-names list,
  (2) devknowledge.run_id no longer unconditionally exempted from redaction -- caller-supplied
  run_id values are now scrubbed with scan_generic_hex=False, (3) POSIX path matching broadened
  from an enumerated top-level-dir allowlist to a general absolute-path shape, plus a new UNC
  path matcher, (4) gen_ai.conversation.id no longer scrubbed by the generic hex-blob catch-all
  (so a legitimate UUID/hash-shaped id survives) while still catching named-token/path shapes.
- Also review tests/test_telemetry_redaction.py, tests/test_routing_telemetry.py, and
  tests/test_fleet_shape_spec_readers.py for correctness and coverage gaps.

---

## Findings
## Critical

## [CRITICAL] scripts/cost_usage_telemetry.py:651 — Arbitrary prompt text can still enter identifier and other string fields

**What:** `run_id` only receives pattern redaction, while fields such as `request_model`, `finish_reasons`, `lane_id`, and `reviewed_by` are serialized without any validation or redaction.  
**Why:** A caller can supply ordinary prompt text in these fields; it matches none of the regexes and is stored verbatim, defeating the store’s no-prompt-text guarantee. This means prior finding (2) is only partially resolved.  
**Fix direction:** Validate semantic identifier fields against constrained formats/vocabularies and reject unsupported free text; add regression cases using ordinary prose in every accepted string field.

## [CRITICAL] scripts/cost_usage_telemetry.py:476 — POSIX/UNC paths containing spaces are only partially redacted

**What:** The POSIX and UNC matchers stop at whitespace, leaving path components after a space unredacted (for example, `/Users/Rob Smith/private/key` or `\\server\Team Share\secret`).  
**Why:** Such paths are common and can still disclose usernames, share names, and sensitive path suffixes, so prior finding (3) is not fully resolved.  
**Fix direction:** Match complete path-shaped values including valid spaces, with tests that assert no path components survive.

## [CRITICAL] scripts/cost_usage_telemetry.py:481 — Lowercase bearer credentials bypass token redaction

**What:** `_NAMED_TOKEN_RE` matches only capitalized `Bearer`, although authentication scheme names are case-insensitive.  
**Why:** `bearer <token>` in `error_type`, `conversation_id`, or caller-supplied `run_id` is persisted unredacted.  
**Fix direction:** Make the bearer-token recognition case-insensitive and add lowercase/mixed-case regression cases.

## High

(none)

## Medium

(none)

## Low

(none)

Follow-up status: (1) deny-by-default events is resolved; (2) is only partially resolved; (3) is only partially resolved; (4) UUID/hash-shaped conversation IDs now correctly survive the generic-hex pass while named-token/path scans remain active.