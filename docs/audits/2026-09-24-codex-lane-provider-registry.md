# Codex Review — lane-provider-registry

**Date:** 2026-09-24
**Branch:** `worktree-lane-provider-registry`
**HEAD:** `6685bec9`
**Diff range:** `main..worktree-lane-provider-registry`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

no-consumer: this lane files no BACKLOG row of its own for this finding -- it was fixed
directly in the same session's commit `1e71d88f`, so the disposition below and the
self-disposition row at the foot of this file are the record, the same direct-disposition
route `2026-09-24-codex-lane-ci-verdict.md`'s own no-consumer line takes for its findings.

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

### ecosystem/provider-registry.yaml:216 — Permitted licence opens an unadmitted `read` route

**What:** Marking Copilot Enterprise as `permitted` makes it eligible for `.dev-knowledge`’s `read` role: it is allowlisted and `read` does not enforce admission.  
**Why:** This contradicts the stated implement-only admission scope; the router can now return Copilot for read work despite its `read` entry remaining unevaluated, and the updated tests do not assert this effective route.  
**Fix direction:** Make the effective routing policy match the intended role scope, and add an exact `read`-route assertion covering Copilot’s eligibility or refusal.

## Medium

(none)

## Low

(none)

---

## Dispositions (lane-provider-registry, same session)

- **HIGH 1 (permitted licence opens an unadmitted `read` route) — ACCEPTED, fixed by adding the
  missing assertion, not by narrowing the route.** The effective routing IS the intended shape:
  `providers.copilot-enterprise.licence` is a provider-level fact (operator ruling O-3 is not
  scoped to one role), and `read`'s own registry description already states the design this
  exposes — "a not-yet-admitted reader is still a coherent idea … CC verifies." `read` was never
  admission-gated (`ADMISSION_GATED_ROLES = {"implement"}`) and this entry sets no
  `requires_admission`, so licence was the last gate standing and clearing it makes Copilot an
  eligible reader, same as `antigravity` already is on that role. What the finding correctly
  named is that this consequence was untested. Fixed: `test_provider_router.py::
  test_the_licence_fix_also_opens_copilot_on_read_though_its_admission_there_is_untouched`
  asserts the eligibility and the exact `read` survivor order
  (`["antigravity", "copilot-enterprise", "anthropic"]`) as a checked property.

| File | Disposition | Evidence locator |
|---|---|---|
| 2026-09-24-codex-lane-provider-registry.md | ACTIONED | 1e71d88f |