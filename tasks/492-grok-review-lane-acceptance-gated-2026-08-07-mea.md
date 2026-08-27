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

- [#492] [P3][S] **Grok review-lane acceptance — gated ≥ 2026-08-07, measured against terra on the same diffs** — a 4.5 run is a burned test, so the row does not open before the 4.6 release. Method: seed a defect list drawn from THIS fleet's own history (vacuous test, fail-open except, stale locator, fence corruption) into real diffs, then compare catch rate against the terra baseline on the SAME diffs. Entry by measured acceptance, never vibes. · Done when: the comparison has run on ≥1 real diff set post-4.6 and the lane is admitted or refused on the measured result · refs #480, #469 (codex lane runs an unpinned model), docs/audits/2026-08-04-codex-483-preflight-discrimination.md · kill-candidates: none — [#469] owns the codex lane's model pin, not a second reviewer's admission · DEFER — peg: the Grok 4.6 release ALONE — the calendar leg is SPENT and dropped; release is an external fact, OPERATOR (N1 R-5) · **PEG UNMET at the dated 2026-08-17 re-check; the corpus-currency leg is separately closed and the re-check date is UNMOVED** · source: protocols/STANDING_RULINGS.md I-D item 1 (browser-verified non-release, dated re-check) + docs/audits/2026-08-13-verification-492-corpus-reconciliation.md (12 seed verdicts, 0 flips) · **RE-PEGGED 2026-08-27** (X1 step 3, night-harvest governance session) — peg unchanged and CONFIRMED — the calendar leg was already spent and dropped, leaving the Grok 4.6 release alone, an external fact and OPERATOR-owned (N1 R-5). **New measured context landed the same day, and it bears on the acceptance criterion rather than the peg:** `docs/audits/2026-08-26-technical-provider-surface-v2.md` prices grok as **pay-per-call, ~$0.037/test, point-use only, never fan-out**. A review LANE is a fan-out shape, so if the release lands, the comparison must be run point-use or the lane refused on cost before it is measured on quality.
