---
id: "[#826]"
title: "Id blocks in a batch manifest must be machine-read -- a prose block stopped nothing"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#826] [P1][S] **Id blocks in a batch manifest must be machine-read -- a prose block stopped nothing** - Batch AB's manifest (`8a24f469`) reserved ids 811-826 per holder in a markdown table. `[#827]` was then filed on `main` (`d89b836a`) outside every block, and nothing noticed: no gate, no allocator and no lane reads the table. The push-reservation allocator from lane ab-804 holds an id once reserved, but the block a lane may draw from is still prose, so an out-of-block id is legal to every surface. · Done when: (1) a manifest declares id blocks in a machine-read form (frontmatter or a fenced block) that `batch_manifest.py` parses; (2) RED-first, `id_allocator.py allocate` for a holder refuses an id outside that holder's declared block, naming the block; (3) a commit on `main` that files a task id inside an open batch's reserved range under a non-holder is refused at commit time; witnessed against a fixture reproducing the `[#827]` case · refs `scripts/batch_manifest.py`, `scripts/id_allocator.py`, `docs/audits/2026-09-16-technical-batch-ab-manifest.md` section 3 · kill-candidates: none -- this is `[#804]` Done-when (2) (reading the per-lane block by machine), split out as its own witness because the AB manifest proved the prose form inert · source: operator order 2026-09-16, integrator-AB
