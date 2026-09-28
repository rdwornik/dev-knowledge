---
id: "[#1123]"
title: "Handoff part B: stamp the cut manifest after the required fills"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1123] [P2][S] **Handoff part B: stamp the cut manifest after the required fills** - R26 (to-browser/RATIFICATION-2026-09-28.md v5) item 2: `gen_handoff.generate()` stamps HANDOFF_RECEIPT.json's manifest over the COLD render, so the required post-cut fills (SUPPLEMENT, RESIDUAL, HANDOFF_BOOT, the second assemble) always break `BD-manifest`; the `--filled` re-render that would re-stamp it is refused by its own preflight ship_gate row, because `handoff_probes` hard-fails on that same uncommitted bundle. The 2026-09-28 cut needed a one-off authorized re-stamp. Part B B3/B5 · Done when: a cut, filled and re-assembled per HANDOFF_PROCESS, passes `BD-manifest` with no hand re-stamp (stamp after the fills, or `--filled` accepts the cut's own known hard-fails), with a test · refs scripts/gen_handoff.py, scripts/verify_handoff_probes.py, docs/handoffs/2026-09-28-dev-knowledge-architect/ · kill-candidates: none -- no open row tracks the manifest circularity
