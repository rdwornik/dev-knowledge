---
id: "[#492]"
title: "Grok review-lane acceptance — gated ≥ 2026-08-07, measured against terra on the same diffs"
status: deferred
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
generates: BACKLOG.md
---

- [#492] [P3][S] **Grok review-lane acceptance — gated ≥ 2026-08-07, measured against terra on the same diffs** — a 4.5 run is a burned test, so the row does not open before the 4.6 release. Method: seed a defect list drawn from THIS fleet's own history (vacuous test, fail-open except, stale locator, fence corruption) into real diffs, then compare catch rate against the terra baseline on the SAME diffs. Entry by measured acceptance, never vibes. Every new lane obeys artifact-or-RED and **writes its severity tally into the artifact body** from day one — the [#480] durability property applied to a new lane at birth rather than retrofitted. · Done when: the comparison has run on ≥1 real diff set post-4.6 and the lane is admitted or refused on the measured result · refs #480, #469 (codex lane runs an unpinned model), docs/audits/2026-08-04-codex-483-preflight-discrimination.md · kill-candidates: none — [#469] owns the codex lane's model pin, not a second reviewer's admission · DEFER — peg: NIGHT-BATCH DRAFT, awaiting architect flip at morning review
