---
id: "[#548]"
title: "Intake #12's SETTLED ownership manifest is parked on a departed id, and three live rows depend on it by name"
status: open
priority: P2
size: S
theme: "[E4] Decision management"
story: "[S11] Keep the decision corpus navigable and contradiction-aware"
depends-on: "#329, #331, #332"
generates: BACKLOG.md
---

- [#548] [P2][S] **Intake #12's SETTLED ownership manifest is parked on a departed id, and three live rows depend on it by name** — `docs/intake/2026-07-11-tech-ownership-manifest.md` is ACCEPTED-but-deferred behind `trigger: "#328 build"`, and **[#328] does not exist** (verified 2026-08-17), so the un-park condition can never fire; **[#329], [#331] and [#332] each name that manifest as their input**. **Not an archival candidate**: `docs/intake/README.md` §5 rules ACCEPTED explicitly non-terminal, so the answer is a carrier, not a move. · Done when: intake #12's TIER-1/TIER-2 manifest content has a live carrier — a row that owns building it or retiring it — OR the document's `trigger:` is re-anchored onto a live id or a date on the [#322] precedent (*"a peg whose referent will not occur tests nothing, so the trigger is a date"*), with [#329]/[#331]/[#332]'s dangling `#328` references repointed in the same act · refs docs/intake/2026-07-11-tech-ownership-manifest.md, docs/intake/README.md, #329, #331, #332, #322, ADR-98 · kill-candidates: none — [#329]/[#331]/[#332] CONSUME the manifest and none owns producing it; [#549] and [#550] carry the plan and requirements halves of the same departed build · source: docs/audits/2026-08-16-census-nb6-archive-sweep.md §1.3 + the intake's frontmatter · depends-on: #329, #331, #332
