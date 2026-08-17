---
id: "[#542]"
title: "`ARCHITECTURE.md` still claims four `doc_rot` sub-detectors; there are five"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S13] Keep canonical files accurate"
generates: BACKLOG.md
---

- [#542] [P3][S] **`ARCHITECTURE.md` still claims four `doc_rot` sub-detectors; there are five** — `:427` reads *"Four read-only sub-detectors — BACKLOG inline-history accretion, per-section Section-history accretion, file-bloat vs a self-declared budget, grooming-cadence lapse"*, which is the pre-`[#532]` enumeration. The live detector declares five categories — `backlog-accretion`, `backlog-row-length`, `section-history`, `file-budget`, `grooming-cadence` — because `[#532]` split the BACKLOG scanner into two independently-named arms. The batch-6 packet named `ARCHITECTURE.md:427` in its **Owed** list and it was never paid. `validate_doc_claims` checks 4 claims and this is not one of them, so nothing catches it. · Done when: `ARCHITECTURE.md` names the five live `doc_rot` categories, and `ecosystem/doc-code-edge.yaml` carries the claim so `doc_claims` fails when the count and the detector disagree · refs ARCHITECTURE.md:427, scripts/validate_doc_rot.py, scripts/validate_doc_claims.py, ecosystem/doc-code-edge.yaml, #532 · kill-candidates: none — `[#532]` is closed on the split; its documentation debt was booked to the batch-6 packet's Owed list, which owns nothing · source: docs/audits/2026-08-16-technical-batch-6-packet.md (Owed list)
