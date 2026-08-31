---
id: "[#624]"
title: "Nothing watches a BLOCKER's status — a fold target went deferred and no organ noticed"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#624] [P2][M] **Nothing watches a BLOCKER's status — a fold target went deferred and no organ noticed** — `[#424]` made `depends-on` edges PARSE, and reference-existence plus cycle detection now fire; **watching what an edge POINTS AT is a different property and no organ has it.** Live instance, measured 2026-08-30: intake #35's PROPOSED ROW R3 carries a `kill-candidates` line reading *fold, do not birth* — fold into the `[#491]`/`[#492]` corpus. `docs/audits/2026-08-19-technical-n3-ratification-pack.md:311` records that target as *"`[#491]` (open) and `[#492]` (deferred)"*; **both are `status: deferred` today.** `[#491]` moved from open to deferred and nothing surfaced it, so an instruction authored against a live target silently became an instruction to fold into a dormant one — *a birth wearing a fold's clothes*. **The cost is not hypothetical:** three independent AUT lanes converged on R3 as the arc's rank-1 item (the missing reward function four other items sit behind), and its execution is blocked on a ruling that only exists because the blocker moved unwatched. **This is a DETECTION gap, not a data gap** — the edges are parseable and the statuses are in frontmatter; nothing reads the pair together. Scope note: the general form is broader than `depends-on` — a `kill-candidates` target, a `refs` id, an intake's `consumed-by` and an ADR's `Decommission` list all name objects whose status can move underneath the citing text. · Done when: an organ reports, for every row or intake naming another object as a precondition, any case where that object's status changed after the citing text was written — the `[#491]`/`[#492]` instance is the regression case, and the report distinguishes *the target moved* from *the target never existed* (which reference-existence already covers) · refs docs/audits/2026-08-29-technical-autonomy-synthesis.md, docs/audits/2026-08-19-technical-n3-ratification-pack.md, docs/intake/2026-08-17-tech-agent-instruction-layers-and-distillation.md, #424, #491, #492 · kill-candidates: none — `[#424]` is CLOSED and owned the parser, not the watcher; no open row owns status-drift detection · serialize-group: audit-py
