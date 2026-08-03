# Codex Review — 472-declaration-anchor

**Date:** 2026-08-03
**Branch:** `feat/472-declaration-anchor`
**HEAD:** `8d57c9b8`
**Diff range:** `main..feat/472-declaration-anchor`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- audit.read_adr104_declaration: is the anchor parsing sound? Consider a start marker inside a code fence, nested/overlapping markers, an end-before-start pair, an id that is a PREFIX of another (adr104-fleet-members vs adr104-fleet-members-v2), CRLF input, blank/indented lines in the block. Can it ever return a WRONG id list rather than raising?
- _declaration_agreement: must catch drift in BOTH directions AND a duplicated id. Is the Counter-difference logic correct for the duplicate case? Any silent pass-when-it-should-fail path?
- Attach point: evaluated after the _is_hub guard and BEFORE the surfaces loop, but EMITTED LAST on all 5 return paths. Verify the declaration verdict survives every early return, and that nothing feeds the ADR block into classify_membership (ADR-109 section 2 must hold; resolve_fleet_members untouched).
- The ADR-104 amendment is append-only (72 insertions, 0 deletions). Does the appended block content match ADR104_FLEET_DECLARATION exactly, and does the anchor appear exactly once in the file?
- Tests: any vacuous, tautological or self-constructing assertions? The fixtures build their own ADR text - circular? Two existing tests changed from "exactly one finding" to "all pass" - weakening or strengthening?

---

## Findings
## Critical

(none)

## High

### scripts/audit.py:3226 — Anchor parser can accept a fenced/example marker as the declaration source

**What:** The regex scans all text, including Markdown code fences, and the start pattern also accepts IDs prefixed with `adr104-fleet-members` (for example `...-v2`).  
**Why:** An incidental fenced example can supply the only matched start/end pair and return a wrong ID list—or even pass if its content matches the constant—instead of detecting that the real anchor is absent.  
**Fix direction:** Parse Markdown fence state, require full-line exact start/end markers with an exact ID boundary, and add fixtures for fenced markers and prefix IDs.

## Medium

(none)

## Low

(none)

I also verified the requested non-finding checks: `Counter` differences catch duplicates and both drift directions; the declaration verdict is evaluated after the hub guard, retained on surface-read early returns, and emitted last; `classify_membership` still receives only `ADR104_FLEET_DECLARATION`. The ADR amendment is 72 additions/0 deletions, its anchored IDs match the constant, and the start/end pair appears once.