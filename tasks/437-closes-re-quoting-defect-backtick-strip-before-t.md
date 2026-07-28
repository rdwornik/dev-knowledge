---
id: "[#437]"
title: "`CLOSES_RE` quoting defect — backtick-strip before the closure regex"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#437] [P2][S] **`CLOSES_RE` quoting defect — backtick-strip before the closure regex** — `scripts/propose_closures.py:80` (`CLOSES_RE`, :51) scans raw commit text, so a `closes [#N]` inside an inline-code or fenced span — convention-quoting PROSE — reads as a real closure. **Witnessed, still live:** `12e6b45b`'s body states "no commit carries a `closes [#370]` tag", and that sentence alone makes `[#370]` the STRONG proposal in every window sampled, today's included. The lever exists one file over (`validate_git_backlog._strip_code_spans:87`) — shared-core divergence, not missing capability; the same blind spot weakens direction-(a) dead-detection wherever the cores drift. **Class: gate-code — design review BEFORE build applies ([#438]).** · Done when: both closure scanners strip inline-code/fenced spans via one shared helper AND a seeded backtick-quoted `closes [#N]` yields no proposal, with tests · refs scripts/propose_closures.py:51,80, scripts/validate_git_backlog.py:87, `12e6b45b`, logs/PROPOSALS-2026-07-28.md, ADR-65 · kill-candidates: none — a live false positive in a Tier-1 lifecycle organ; no open row covers the closure-detector core · serialize-group: audit-py
