---
template: scrum-master-cover-letter
version: 1.0
last_reviewed: 2026-05-12
---

# Scrum-Master Review — Cover Letter

> Operator copies this template, fills placeholders below, then routes filled cover letter + full audit-report contents to the target-repo architect. See `protocols/PLAYBOOK.md` § 17 Scrum-Master Review Propagation for the full three-stage flow.

**From:** `.dev-knowledge` (ecosystem strażnik)
**To:** `<target-repo>` architect
**Date:** YYYY-MM-DD
**Review type:** `<scrum-master-review | governance-audit | convention-compliance>`
**Audit report:** `docs/audits/YYYY-MM-DD-<target-repo>-scrum-master-review.md` (full report content pasted alongside this cover letter)

## Summary

`<one-paragraph summary of what was reviewed and the highest-impact finding>`

## Severity counts

- CRITICAL: `<N>`
- HIGH: `<N>`
- MEDIUM: `<N>`
- LOW: `<N>`

## Top 3 findings

1. **`<finding-1 short title>`** (`<severity>`) — `<one-line description + suggested action>`
2. **`<finding-2 short title>`** (`<severity>`) — `<one-line description + suggested action>`
3. **`<finding-3 short title>`** (`<severity>`) — `<one-line description + suggested action>`

(Full findings list in the attached audit report.)

## Expected response

**Single round trip.** Architect at `<target-repo>` reviews findings and implements in their own repo. No browser-to-browser delivery turn back to `.dev-knowledge` is expected — completion evidence is the implementation commits + CHANGELOG entry in `<target-repo>`, verifiable read-only by strażnik at next session start.

**If architect pushes back** on a finding (disagrees, scope mismatch, by-design justification): open a new conversation framed as a separate handshake. Do NOT continue this routing thread.

## Addendum mechanism

If `.dev-knowledge` strażnik catches additional gaps after this routing (findings missed during initial audit), an addendum artifact is produced and routed alongside this letter. The addendum supplements; it does not supersede.

---

**Empirical reference:** First instance of this propagation pattern — `docs/audits/2026-05-11-ai-council-scrum-master-review.md` (ai-council review, 10 findings + addendum covering audit gaps I7 and I8).
