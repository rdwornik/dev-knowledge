---
id: "[#621]"
title: "ADR-114 option (C): the nine-repo VISION.md to README.md filename migration"
status: open
priority: P2
size: L
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#621] [P2][L] **ADR-114 option (C): the nine-repo VISION.md to README.md filename migration** — ADR-114 `Decommission` item **(b)**, the `ARCHITECTURE.md:366` echo. **That locator does not exist** — `grep -n "recreate" ARCHITECTURE.md` returns no match — so item (b) was discharged by attrition before the ADR was ruled; `[#614]` lane-b corrected the stale deletion fact at `:478` and the stale PARKED verdict in the Governing-ADRs list in its place. **Residual — the migration itself, which lane-b deliberately did not attempt:** the ten `canonical_docs.py` machine constants, five `deploy/manifest-v*.yaml` `doc_shapes` spines, `gen_handoff._vision_extract`, `conformance-hub.js:133`, the two deploy-carried SOFT-import literals, the `canonical-doc-vision` parity probe path (`{hub: MUST, consumer: MUST}` — and only **2 of 8** children carry a root README, so a flip REDs six), 91 `tests/` occurrences, and `VISION.md`'s archival. · Done when: a sequencing plan across the ADR-104 members exists before the first commit, and ADR-114's second (spine) decision is made in the same ruling · refs docs/audits/2026-08-29-technical-614-consumer-enumeration.md, #614 · source: ADR-114 Decommission (b)
