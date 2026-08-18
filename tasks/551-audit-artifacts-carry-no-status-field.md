---
id: "[#551]"
title: "Audit artifacts carry no `status:`, so a consumed audit is indistinguishable from a live one"
status: open
priority: P2
size: S
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#551] [P2][S] **Audit artifacts carry no `status:`, so a consumed audit is indistinguishable from a live one** — the smallest audit-corpus change consistent with **ADR-100**: a `status:` frontmatter field on `docs/audits/*.md` with the closed enum **LIVE | CONSUMED | SUPERSEDED**, written by the batch-7a disposition ledger as it dispositions each artifact, so the generated index can fold consumed evidence instead of listing every file forever. **It moves NO file** — ADR-100 forecloses that, which is why ADR-100 names the INDEX as its own remedy. · Done when: `docs/audits/*.md` carry a `status:` field with its closed enum stated at a canonical home, the index generator reads it, a CONSUMED artifact is visibly folded rather than flat-listed, the writer of the field is named, and the implementing commit restates the ADR-100 no-move invariant · refs ADR-100, docs/audits/2026-08-17-technical-audit-disposition-ledger.md, scripts/gen_audit_index.py, #269, #420 · kill-candidates: none — [#269] owns the index shape, not the per-file status field it would read, and no open row proposes any audit-corpus frontmatter change · source: ADR-100 (no-move invariant, ~78% un-re-pointable citations) + docs/audits/2026-08-16-census-nb6-archive-sweep.md §5.2 (the `docs/audits/**` exclusion)
