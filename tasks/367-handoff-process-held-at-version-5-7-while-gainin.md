---
id: "[#367]"
title: "HANDOFF_PROCESS held at `Version: 5.7` while gaining an additive normative rule"
status: open
priority: P2
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: handoff
generates: BACKLOG.md
---

- [#367] [P2][S] **HANDOFF_PROCESS held at `Version: 5.7` while gaining an additive normative rule** — codex HIGH 2026-07-19. The residual-completeness rule landed as new binding contract text with no version bump, so every dependent declaring `reconciled_with: handoff-process@5.7` stays green **without ever reviewing the new rule** — the declared-coherence spine reports agreement that was never checked. Deliberate at authoring time (the reconciliation touches protocol files outside that lane's boundary) but not a resolution. · Done when: the spec bumps 5.7 → 5.8 with a Section-history entry, every `handoff-process@5.7` dependent is reconciled via the check-against-spec flow, and `reconciled_versions` is green at the new version — OR holding 5.7 is recorded as accepted-with-reason · refs protocols/HANDOFF_PROCESS.md, ADR-88, docs/audits/2026-07-19-codex-residual-rule-declaration.md · kill-candidates: none — a coherence-spine gap opened by this arc; no open task covers the v5.7 bump · serialize-group: handoff
