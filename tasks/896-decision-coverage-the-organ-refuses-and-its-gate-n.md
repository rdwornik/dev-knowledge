---
id: "[#896]"
title: "decision_coverage -- the organ refuses correctly and its gate never fires locally (stages:[manual] behind a disabled ruleset)"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "DECLARE-BATCH-AC-CLOSE-2026-09-18"
generates: BACKLOG.md
---

- [#896] [P1][S] **decision_coverage -- the organ refuses correctly and its gate never fires locally (stages:[manual] behind a disabled ruleset)** - B0 ran `decision_coverage.py` directly and it exited 1 on 6 uncovered decisions, including the batch AC night order itself: **the organ is alive.** Its gate, the `decision-coverage` pre-commit id, is `stages: [manual]` since 2026-09-17. It is therefore reachable only through conductor job `commit-gate`, whose required-check ruleset (`deploy/conductor-required-checks.ruleset.json`) arrives `enforcement: disabled`, so **it never fires on a local commit.** It is one instance of a class: of 36 pre-commit ids, only 4 fire locally (the audits-index and organ-index freshness hooks, `block-ff-push`, `block-unanchored-push`), and the other 32 sit behind the same disabled ruleset (`to-browser/HANDBACK-batch-AC-consolidated.md` L-freeze item 9). The AX9-5 re-run (`docs/audits/2026-09-18-census-ax9-5-organ-use-rerun.md` §6) finds seven hook entry points uninvoked in 30 days for the same reason · Done when: `decision_coverage` refuses on a surface that actually runs, either a local stage restored with a measured wall-time that clears the hook bar, or the conductor ruleset armed for it. A commit that adds an uncovered decision is refused in a witnessed run. The same Done-when is stated, or explicitly waived by ruling, for each of the other 31 manual-stage ids, so "organ alive, gate unreachable" stops being the default posture · implements: DECLARE-BATCH-AC-CLOSE-2026-09-18 · refs `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md` §6 W5 + §7, `scripts/decision_coverage.py`, `.pre-commit-config.yaml`, `deploy/conductor-required-checks.ruleset.json`, `scripts/conductor.py`, `[#692]` (closed: built the organ), `[#689]` (conductor E), `[#889]` (acceptance test's armed-guard field) · kill-candidates: `[#689]` -- if arming conductor E's ruleset is ruled the path, this row is that act's acceptance witness and folds into it
