---
id: "[#646]"
title: "The ceremony ratio was measured once, by hand, and nothing computes it"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
generates: BACKLOG.md
---

- [#646] [P3][S] **The ceremony ratio was measured once, by hand, and nothing computes it** — DECLARE-REVIEWS finding R-4 measured 87 journal anchors and 145 merge commits inside 407 commits, putting the substantive share at roughly 10 %. That number decided the batch-size ceiling and the spine-anchor demotion, and it exists in one sentence of one transport file: nobody can tell today whether the ratio moved, and every later claim that 'the ceremony is down' is folklore until something prints it. The scorecard already prints per-window lines, so the gap is a line, not an organ · Done when: the scorecard prints a `substantive commit share` line computed from the commit range rather than typed, the classifier's anchor/merge/substantive predicate is stated where it is implemented, and the R-4 figures are reproduced by it as its first data point · refs DECLARE-REVIEWS §B R-4, `scripts/trace_scorecard.py`, `[#642]` · source: DECLARE-REVIEWS R-4, filed by batch V lane V-4
