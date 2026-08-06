---
id: "[#503]"
title: "Doc-currency sweep — eight sites the world moved past"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#503] [P3][S] **Doc-currency sweep — eight sites the world moved past** — the mechanism is the point, and it is why no gate caught these: each doc is stale not from a bad edit but because **the thing it describes was retired underneath it**. Nothing edited the file, so every edit-keyed signal (`canonical_freshness` A2, `last_reviewed`) stays green while the prose is wrong — the prose↔state seam, arriving from the state side. Eight sites with live locators: **`CONTRIBUTING.md` ×6** stale claims (including the deleted Action described in present tense); **`protocols/DEFINITION_OF_DONE.md:141-149`**; and **`.claude/commands/override.md`**, documenting a path the ADR-85 amendment §A2 RETIRED — the Stop hook is advisory in full, so `/override` has nothing to override. Also: `DEFINITION_OF_DONE.md` is absent from the freshness-gated set, so its `last_reviewed` is read by nothing. · Done when: each site is corrected or recorded as intentional, and the DoD gating gap is closed or filed · footprint: `CONTRIBUTING.md`, `protocols/DEFINITION_OF_DONE.md`, `.claude/commands/override.md` · refs ADR-85, #497 · kill-candidates: none — [#497] owns retired-posture claims at *different* sites
