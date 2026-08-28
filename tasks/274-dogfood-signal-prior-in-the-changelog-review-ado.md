---
id: "[#274]"
title: "Dogfood-signal prior in the /changelog-review ADOPT rubric"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#274] [P3][S] Dogfood-signal prior in the /changelog-review ADOPT rubric (intake doc #2 R4) — features Anthropic ships as CC defaults for its own use (auto mode, agents view, /usage, /recap) carry a prior of adoption-worthiness; the rubric should triage them first · Done when: `.claude/commands/changelog-review.md`'s ADOPT rubric names the dogfood-signal prior, and one subsequent `docs/audits/<date>-changelog-review-*` digest cites that prior by name against at least one classified item · refs .claude/commands/changelog-review.md, docs/intake/archive/2026-07-06-platform-feature-scan.md §6 R4 · **RE-CUT 2026-08-28** — the K4 verdict was DO-IT, and the first of two Done-when legs is LANDED: `.claude/commands/changelog-review.md`'s ADOPT bucket now carries the **dogfood-signal prior** by name, with the four cited defaults, the triage-first instruction, and the honest bound that it is a prior and not a verdict (a dogfooded feature that does not fit the stack still classifies NOISE-count). **Not closed, and the reason is structural rather than effort:** leg 2 requires *"one **subsequent** `docs/audits/<date>-changelog-review-*` digest"* to cite the prior against a classified item, and the command is PUSH-trigger / operator-invoked by its own frontmatter — no act that writes the rubric can also produce the subsequent run that consumes it. Faking that would put a false closure in the record. **Row narrowed to leg 2 alone**, which is now its whole scope · Peg: the next `/changelog-review` run — one is already due (SessionStart surfaced claude-code 2.1.250 against last-reviewed 2.1.204), so this is a live peg, not a parked one · un-deferred from the 2026-08-27 icebox sweep by this lane
