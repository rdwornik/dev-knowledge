---
id: "[#983]"
title: "Decisions and audits land in the repo every wave -- a recurring step, not a one-off catch-up"
status: open
priority: P1
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#983] [P1][M] **Decisions and audits land in the repo every wave -- a recurring step, not a one-off catch-up** - D24: decisions and audits lived only on the operator's Drive transport and were invisible to prior art until a lane like this one (LANE-5A-5) does a catch-up landing; this window's own S3 finding (10 of 17 standing requests with no home, 32 of 45 DECLARE/AMEND/BATCH files OPEN and unnamed in RESIDUAL) shows the catch-up cadence is one window behind · Done when: every wave's close includes a landing step (this lane's own docs/audits/ commits are the first instance) that commits that wave's read-only digests under `docs/audits/` and rows or STANDING_RULINGS-lands that wave's rulings, so P11's OPEN-and-unhomed count does not grow between wave closes; the landing step is named in the batch-close checklist, not left to a dedicated future lane · implements: ADR-120 · refs `docs/audits/2026-09-23-technical-handoff-readiness.md` §5/§6, `docs/audits/2026-09-23-technical-window-defects.md`, this lane's own commits landing 11 audits · kill-candidates: none -- no open row makes the landing step a recurring per-wave close item rather than a catch-up lane
