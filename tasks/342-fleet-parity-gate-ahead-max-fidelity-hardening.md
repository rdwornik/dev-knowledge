---
id: "[#342]"
title: "fleet_parity gate-ahead max-fidelity hardening"
status: open
priority: P3
size: S
theme: "[E6] Cross-repo universalization"
story: "[S15] Converge every child repo on the universal baseline"
serialize-group: audit-py
source: BACKLOG.md
derived: true
---

- [#342] [P3][S] fleet_parity gate-ahead max-fidelity hardening (deferred from #336/ADR-102, operator-ruled) — three net-new fidelity items beyond the shipped `gate_rev_ahead` axis: (1) verify the pinned gate tag actually EXPORTS the required hook ids (read `G:.pre-commit-hooks.yaml`, not just that the consumer stanza LISTS them — the current `precommit_remote` probe lacks this even for the normal case); (2) refuse an AMBIGUOUS `precommit_remote` match (`fleet_parity.py` first-wins `next((r for r in remotes if token in r["repo"]))`) instead of silently taking the first hit; (3) peeled-SHA pin in the `gate_rev_ahead` provenance (assert the tag peels to the recorded immutable commit). · Done when: each of the three lands with a test (an exported-id mismatch WARNs; an ambiguous remote match REFUSES; a provenance SHA mismatch WARNs) · refs docs/decisions/ADR-102-parity-gate-rev-axis.md, scripts/fleet_parity.py, #336 · kill-candidates: none — operator-ruled follow-up (the deferred #336 max-fidelity items; no existing task subsumed) · serialize-group: audit-py
