---
id: "[#480]"
title: "A code-impact merge with no codex-review artifact is mechanically invisible — make the absence surface"
status: open
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#480] [P3][M] **A code-impact merge with no codex-review artifact is mechanically invisible — make the absence surface** — the 2026-08-02 W2 report recorded “terra review: zero findings on both arcs” while NO artifact existed anywhere. The claim was never refuted; it was UNFALSIFIABLE, and nothing in the repo could tell the two apart. All 88 prior codex reviews left a `docs/audits/<date>-codex-<slug>.md`, so the convention is strong enough to check against. Cured retroactively for W2, but the MECHANISM gap remains: a review claim is trusted prose. Needs a ruling FIRST on whether an artifact is REQUIRED for a code-impact merge and what counts as code-impact — the check is cheap, the policy is not. · Done when: the ruling is recorded AND, if required, a code-impact merge lacking its review artifact is surfaced by a named organ with a test · refs docs/audits/2026-08-03-technical-night-la-w2-verification.md, ADR-70, #431, #469 · kill-candidates: none — no row owns review-artifact presence; [#431]/[#469] own the wrapper's routing and model pin, not whether a review happened · serialize-group: audit-py
