---
id: "[#437]"
title: "`CLOSES_RE` quoting defect — backtick-strip before the closure regex"
status: closed
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#437] [P2][S] **`CLOSES_RE` quoting defect — backtick-strip before the closure regex** — `propose_closures.py:80` (`CLOSES_RE`, :51) scans raw commit text, so a quoted tag inside an inline-code or fenced span (convention-quoting PROSE) reads as a closure. **n=1:** `12e6b45b`'s body denies such a tag exists for `[#370]`, making it the STRONG proposal in every window sampled. **n=2, self-inflicted 2026-07-28:** ratification commit `096364ac` quoted the offending phrase verbatim; the quotation matched `CLOSES_RE`, manufacturing a false signal against `[#433]` — the one row that arc had to leave open — and `git_backlog_drift` reported it closed-but-present; amended pre-merge. Fires on WRITING ABOUT the convention. Lever one file over: `validate_git_backlog._strip_code_spans:87` (shared-core divergence, not missing capability). **gate-code class ([#438]).** · Done when: both closure scanners strip inline-code/fenced spans via one shared helper AND a seeded quoted tag yields no proposal, with tests · refs propose_closures.py:51,80, validate_git_backlog.py:87, `12e6b45b`, `096364ac` · kill-candidates: none — a live false positive in a Tier-1 organ · serialize-group: audit-py
