---
id: "[#146]"
title: "De-hardcode-first doctrine + sweep"
status: deferred
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: playbook
generates: BACKLOG.md
---

- [#146] [P3][S] De-hardcode-first doctrine + sweep — the `amendment_coherence` gate (#11, shipped) is a BACKSTOP; the superior fix for a coupled version surface is to de-hardcode it so it interpolates the anchor. #11's honest limit names de-hardcoding as the actual v3.4 fix, so per ADR-81 (d) that deferral must be tracked, not left as a disclaimer: (a) record de-hardcode-first as doctrine in PLAYBOOK "Multi-surface amendment coherence"; (b) sweep remaining hand-maintained version surfaces for de-hardcoding candidates. **Clause (a) is landed at `PLAYBOOK:1016-1024`** — the `amendment_coherence` honest-limits paragraph carries de-hardcode-first verbatim. Authorship unverified: the text is there, but nothing ties it to this row rather than to #11's own write-up. Row stays OPEN on clause (b), the sweep, which has not run. · Done when: `protocols/PLAYBOOK.md`'s `amendment_coherence` honest-limits section carries de-hardcode-first as doctrine, and a `docs/audits/<date>-technical-*` sweep names every hand-maintained version surface with a per-surface verdict of de-hardcoded or kept-as-manifest — each kept-as-manifest surface carrying its reason · refs #11, ADR-81 (d), LESSONS 2026-05-29 (v3.4 abort) · serialize-group: playbook · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
