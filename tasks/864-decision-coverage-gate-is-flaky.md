---
id: "[#864]"
title: "The decision-coverage gate is FLAKY -- it failed and then passed on retry with nothing changed"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#864] [P1][S] **The decision-coverage gate is FLAKY -- it failed and then passed on retry with nothing changed** - Operator report 2026-09-17: the `decision-coverage` pre-commit gate (`[#692]`, A9-1) refused a commit and then passed on retry with nothing changed. **A gate that is non-deterministic is worse than one that is strict**: a strict gate teaches the rule, while a flaky one teaches that retrying is the fix, and that habit then covers a real refusal too. Not yet reproduced by the filing seat. Its own three commit attempts that day reached the gate three times: two passed it, and the third was killed mid-run by Claude Code for low system memory, so load-dependence is a live hypothesis, not a finding. · Done when: (1) the non-determinism is reproduced by running the gate repeatedly on one frozen tree and index, the verdict distribution is recorded, and the input that varies is named (wall clock, git state read outside the index, a concurrent writer in the primary checkout, subprocess timeout under memory pressure, or iteration order); (2) RED-first: a witness pins that input and fails on the flaky behaviour; (3) the gate returns the same verdict for the same tree and index on every run, or, where it depends on something outside them, says so in its output rather than refusing silently · refs `.pre-commit-config.yaml` (`decision-coverage`), `[#692]` (closed; built the gate), `[#783]`, `[#768]` · kill-candidates: none -- `[#783]` is an unexercised leg, `[#768]` the refusal-channel shape; neither covers non-determinism · source: operator order 2026-09-17
