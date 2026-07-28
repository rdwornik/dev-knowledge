---
id: "[#439]"
title: "ADR-107 strangler STEP 3 — the source-of-truth flip"
status: closed
priority: P1
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: architecture
generates: BACKLOG.md
---

- [#439] [P1][M] **ADR-107 strangler STEP 3 — the source-of-truth flip** — the separately-contracted execution ADR-107 §7.2 conditions on (i) the ADR Accepted AND (ii) the `tasks/` coherence gate ARMED, and §7.5 assigns to its OWN ticket, not [#433]. Both held at filing (ratified 2026-07-28; gate armed `fa3f10a3`, witnessed firing twice). Inverts the derivation: `tasks/` (per-task `.md` bodies + `manifest.json`) becomes the SOURCE OF TRUTH, `BACKLOG.md` becomes GENERATED, and the coherence gate's expectation side flips to the tree. `BACKLOG.md` is NOT decommissioned (§Decommission: none) — it stays byte-identical on disk, so every BACKLOG-reading gate keeps working unchanged. **Step 4 stays DEFERRED** per §7.3, not pulled in. · Done when: `--emit-source` rebuilds `BACKLOG.md` byte-identically from the tree AND the flipped `--check` REDs a divergence AND ship-gate + `task_tree_coherence` are GREEN on main, with tests · refs ADR-107 §7.2/§7.3/§7.5, scripts/gen_task_tree.py, scripts/audit.py, #433 · kill-candidates: none — §7.5 assigns step 3 its own ticket, disjoint from [#433] (open on §6.2) · serialize-group: architecture
