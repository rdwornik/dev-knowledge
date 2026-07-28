---
id: "[#320]"
title: "Fleet backup posture"
status: open
priority: P2
size: S
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
generates: BACKLOG.md
---

- [#320] [P2][S] Fleet backup posture — three repos hold unpushed work on one disk: corp-ops `main` 4 ahead of `origin/main`, corp-sca-time-automation `main` 4 ahead, demo-prep `main` 53 ahead. Premise corrected at HEAD 7c592062: all three DO have an `origin` remote (`github.com/rdwornik/*`) with pushed history — the gap is unpushed commits, NOT a missing remote — and corp-sca's `feature/tenrox-loader` is fully pushed (its unpushed work sits on `main`). corp-ops+corp-sca are the #284 concern (its closure premise is false on live state, night-audit F1); demo-prep newly surfaced. Operator: per repo, push the outstanding commits or record accept-local. · Done when: each of the three has every local branch pushed to its tracking remote, or a recorded accept-local decision · refs #284, docs/audits/2026-07-09-deletion-candidates-report.md, docs/audits/2026-07-12-technical-night-delete-candidates.md · kill-candidates: none — data-safety gap; prior-sweep item never filed
