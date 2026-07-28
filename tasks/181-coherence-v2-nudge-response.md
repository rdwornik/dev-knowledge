---
id: "[#181]"
title: "Coherence v2 nudge-response"
status: deferred
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: coherence
generates: BACKLOG.md
---

- [#181] [P2][S] Coherence v2 nudge-response — decide escape-hatch vs deferred-hash vs promote-nudge-to-gate for the forgotten-version-bump nudge; data-gated on logs/coherence-nudge.log (noisy → escape-hatch/deferred-hash; accurate+rare → promote to gate) · Done when: the nudge log shows real firing signal AND the response is decided + implemented, with tests · refs #172, coherence_nudge.py, docs/handoffs/2026-06-17-dev-knowledge-architect-2/SUPPLEMENT.md §B · serialize-group: coherence · DEFER — peg: coherence-nudge.log has enough entries to adjudicate
