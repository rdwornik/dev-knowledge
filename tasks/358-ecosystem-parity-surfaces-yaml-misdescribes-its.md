---
id: "[#358]"
title: "`ecosystem/parity-surfaces.yaml` misdescribes its own enforcement posture at HEAD"
status: open
priority: P2
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: architecture
source: BACKLOG.md
derived: true
---

- [#358] [P2][S] **`ecosystem/parity-surfaces.yaml` misdescribes its own enforcement posture at HEAD** — header `:6` and `:93-94` still declare "WARN-only v1, zero blocking gates" / "the checker never blocks", and `scripts/fleet_parity.py:131` carries "never blocks in v1", while `scripts/audit.py:2425` makes it a **BLOCKING `ALL_CHECKS` member** and `ARCHITECTURE.md:192` agrees ("fail-closed"). The #337 promotion updated `audit.py` and `ARCHITECTURE.md` and missed these three sites. A reader trusting the manifest header draws the wrong conclusion about what a MUST row costs. Live doc-vs-code contradiction, not a classification artifact. Routes to W2. · Done when: the three stale sites state the post-#337 blocking posture, or the divergence is recorded with a reason · refs ecosystem/parity-surfaces.yaml, scripts/fleet_parity.py, scripts/audit.py, ARCHITECTURE.md, #337 · kill-candidates: none — census-surfaced; no open task covers parity-surfaces self-description · serialize-group: architecture
