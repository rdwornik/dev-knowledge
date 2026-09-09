---
id: "[#668]"
title: "Step E — the paste test becomes a scored eval, or the whole recovery plan is graded by vibe"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
depends-on: "#667"
generates: BACKLOG.md
---

- [#668] [P2][M] **Step E — the paste test becomes a scored eval, or the whole recovery plan is graded by vibe** — step E of the recovery plan (intake `#89` § 0, § 4). The plan states its own acceptance as a test: a fresh seat reads `ARCHITECTURE.md` ONLY and answers ten questions — what fires at commit · what fires at push · what fires at session start and stop · what the operator triggers · which module owns stage N of the loop · what reads and writes file X · which repos are consumers · where the dispatch verb lives · which organs are orphans · what changed since the last cut. **Any question answered by "grep the repo" means the file failed.** The same shape, ten process questions, for `protocols/PLAYBOOK.md`. This is SDA-1's eval shape finally run: **scored per cut and kept by a freshness hook**, so a later edit that quietly re-breaks the file shows up as a falling score rather than as nobody noticing. Substrate is Codespaces — read-only compute. **The bar is not stated in the source and stating it is part of this row**: a score recorded per cut with no threshold is telemetry, which is the exact shape three of the operator's four standing asks are already stuck in · Done when: both ten-question sets run as a scored eval against a seat given only the file under test; the score is recorded per cut at a stated home; a freshness hook keeps it; and a PASSING BAR is declared, so the eval can fail rather than only report · depends-on: #667 · refs `docs/intake/2026-09-09-tech-recovery-plan.md` (intake `#89`) § 0 and § 4 step E, `[#667]`, `ARCHITECTURE.md`, `protocols/PLAYBOOK.md` · kill-candidates: none — no open row owns a doc-legibility eval; `[#639]` retires organs that fire and report, which is the class this row must not join · source: DECLARE-RECOVERY-2026-09-09 § 0 and § 4 step E, filed by batch V lane `lane-v-000-window-rulings`
