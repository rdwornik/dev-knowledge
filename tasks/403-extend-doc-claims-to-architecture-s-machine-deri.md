---
id: "[#403]"
title: "Extend `doc_claims` to ARCHITECTURE's machine-derivable claims"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#403] [P3][S] **Extend `doc_claims` to ARCHITECTURE's machine-derivable claims** — the currency lane fixed a 5-site carrier-count drift, a stale child roster, and a Governing-ADRs list stopping at ADR-93 — machine-derivable, unchecked; [#321]'s re-read (f865abfa) missed them. **RULED 2026-07-25 — carrier-set derivation:** count/list ⇐ `make_carriers()` keys. **SCOPE EXTENDED (intake #17 §1 D6) — child-roster derivation is IN, reversing its same-day deferral:** evidence is D6's three-fleet-counts drift, re-confirmed here — the map mis-modeled its denominators (`onboarded` as innermost ring though `index.yaml` carries unonboarded repos); `registry.md` holds 8 rows vs ADR-104's 9. **Obstacle:** `discover_repos()` reads gitignored per-tree `state.yaml`, so it disagrees between clones ([#418] shape) — the build needs a clone-stable ground truth. Governing-ADR completeness stays DEFERRED (a citation is not a governing relation). · Done when: carrier-set AND child-roster gated (doc_claims or a regen-and-diff sibling) with tests · refs 2026-07-21 digest F1, #222, ADR-92 amendment, #418, intake #17 §1 D6 · kill-candidates: none — no task checks these claims · serialize-group: audit-py
