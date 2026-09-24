---
id: "[#1015]"
title: "`scripts/plan_lint.py` silently reads zero ownership from a contract using only an `Owns:` label"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#1015] [P2][S] **`scripts/plan_lint.py` silently reads zero ownership from a contract using only an `Owns:` label** - MEASURED 2026-09-23 (`docs/audits/2026-09-24-technical-digest-measurements.md` §3, the Opus A/B): `parse_lane_contract` reads ownership only from the `**Files you own:**` paragraph (`_FILES_YOU_OWN_RE`); all 10 live WAVE5A contracts carried `**Owns:**` instead, so their owned-paths set parsed as empty -- corroborated independently by the WAVE5A dispatcher's own receipt (`SESSION-dispatcher-wave5a-2026-09-23.md` lines 10-36), which hand-translated contracts to work around it -- and it blocked the WIRE of `plan_lint` at `pre-launch` (`docs/audits/2026-09-24-technical-digest-organ-triage.md`). RE-VERIFIED on this branch (`scripts/plan_lint.py:192-207`, base `2ae86d07`): the slug leg is no longer the live gap -- `_SLUG_RE` now matches `` slug `<slug>` `` anywhere in the text rather than requiring an anchored line -- but the ownership leg is unchanged and the defect is silent, not a refusal: a `**Owns:**`-only contract still parses with `owned_paths=()`, so file-collision (class 1) and stale-ownership (class 2) checks see no paths to compare and pass vacuously rather than erroring. · Done when: `parse_lane_contract` reads ownership from `**Owns:**` when `**Files you own:**` is absent, or `_FILES_YOU_OWN_RE`/its caller is taught the live label as a synonym (library-first: the paragraph shape is identical, only the label differs); a RED-first test stages a fixture using only `**Owns:**` with real path tokens and asserts `owned_paths` is non-empty; `scripts/plan_lint.py` wired at the `pre-launch` moment per the organ-triage GO · refs `scripts/plan_lint.py`, `docs/audits/2026-09-24-technical-digest-measurements.md` (§3, primary provenance), `docs/audits/2026-09-24-technical-digest-organ-triage.md` (corroboration), `to-browser/SESSION-lane-precut-landing.md` (ROWS-OWED item 1, transport, cited in addition) · kill-candidates: none -- `[#985]` covers a different plan_lint gap (no Codex-verification check on audit orders), no open row covers this one
