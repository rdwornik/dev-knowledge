# Codex Review — lane-1-490-430-parity-manifest

**Date:** 2026-08-07
**Branch:** `worktree-joyful-scribbling-hummingbird`
**HEAD:** `3cf3a5b0`
**Diff range:** `main..worktree-joyful-scribbling-hummingbird`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low -->

**Disposition: both HIGHs FIXED in-lane, not deferred.** Each was the same
wrong-type class — a YAML value of an unexpected shape reaching a predicate written for a
string:

1. `fleet_parity.py` non-string `reason` — `str(x or "").strip()` coerced a list, mapping,
   number or bare `true` into a truthy "reason", so structured junk bought a `pre-deploy`
   member out of the registry cross-check while telling a reader nothing. Fixed by a shared
   `_declared_reason()` helper that requires `isinstance(str)`; both call sites use it, so
   the two cannot drift. 5 parametrized RED-first tests.
2. `fleet_parity.py` malformed `declared_by` — `x not in frozenset` raises `TypeError` on an
   unhashable value, so a `declared_by:` written as a YAML list/mapping aborted
   `load_manifest` outright (exit-2 class) instead of refusing the one bad row. Fixed by an
   `isinstance` guard ordered BEFORE the membership test. 3 parametrized RED-first tests
   that also assert validation continues and the following good row survives.

The reviewer's non-blocking note on the `--` split is also closed rather than accepted: the
declared reason is now a `RepoTarget.declared_reason` field instead of being parsed back out
of the formatted `note`, so the delimiter is no longer load-bearing and no parse-back exists
to get wrong. Regression test covers a reason containing `--`.

Review ran against `3cf3a5b0`; the fixes landed at `c4f505ef`. `tests/test_fleet_parity.py`
83 passed, ruff clean.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- [#490]: resolve_fleet now lets a pre-deploy fleet member absent from deployed-versions.yaml stand IF it carries a non-empty eason:. Is this escape actually narrow? Can a walked role (hub/consumer) slip through? Can an empty/whitespace/non-string reason satisfy it?
- [#490]: the pre-deploy eason: is parsed back out of RepoTarget.note by splitting on the first '--'. A reason containing '--' or a note without one: does the render degrade safely or silently drop/garble the reason?
- [#430](a): declared_by became a validated enum (TEMPLATE_DECLARATION_MARKERS). Does the new loader refusal sit at the right place in load_manifest's control flow, and does it skip the row correctly without swallowing later validations?
- [#430](a): the new root-conftest row makes conftest.py a covered top-level segment. Does that suppress anything it should NOT (e.g. a Tier-4 ephemera or an INVERSE rule elsewhere)?
- Does removing the disposition-register entry leave any dangling reference (ref, RETIRE-ON-CLOSE citation, review_date sweep) elsewhere in the repo?

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/fleet_parity.py:476 — Non-string `reason` values satisfy declared absence

**What:** `str(...).strip()` accepts values such as YAML lists, mappings, booleans, or numbers as non-empty reasons.  
**Why:** A `pre-deploy` member can bypass the deployed-registry refusal with meaningless structured/scalar data.  
**Fix direction:** Require `reason` to be a string and non-blank; refuse other types.

## [HIGH] scripts/fleet_parity.py:302 — Malformed `declared_by` can crash the loader

**What:** Membership against the marker `frozenset` raises `TypeError` for YAML list/mapping values.  
**Why:** A malformed row crashes loading rather than yielding the intended row-level refusal and continuing validation.  
**Fix direction:** Type-check `declared_by` as a string before enum membership, refusing invalid types.

## Medium

(none)

## Low

(none)

`--` inside a reason is preserved by the one-time split. A `RepoTarget.note` without `--` silently renders the generic fallback and loses any reason, though `resolve_fleet()` currently always emits the delimiter. No direct dangling disposition ID, RETIRE-ON-CLOSE citation, or old review-date reference was found; `ecosystem/index.yaml` merely contains an older generated warning snapshot.