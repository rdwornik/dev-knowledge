---
id: "[#455]"
title: "`registry.md` derived-field drift checker — no organ reads the file at all"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#455] [P3][S] **`registry.md` derived-field drift checker — no organ reads the file at all** — `ecosystem/registry.md` declares itself the DERIVED side of the onboarding record (“Do not hand-fabricate a version here; read it from `deployed-versions.yaml`”), but nothing verifies that derivation: the only reference to `registry.md` anywhere in `scripts/` is an EXCLUSION in `fleet_analytics.py`. The gap was not theoretical — the ai-council row asserted v1.2.0 against a recorded 1.3.1 and no gate could surface it. Must NOT flag the corp-monorepo 1.2.0-vs-v1.3.1 pair, which is sanctioned by design and modelled as ADR-102 `gate_rev_ahead`. · Done when: a read-only check compares each `registry.md` Status version against `deployed-versions.yaml` and reports drift, with a test covering both the drift case and the sanctioned-exception case · refs ecosystem/registry.md, ecosystem/deployed-versions.yaml, ecosystem/parity-surfaces.yaml, ADR-102, #382 · kill-candidates: none — [#382] dissolves the registry sprawl into one contract but is gated behind the pilot, so this drift stays unguarded until then · serialize-group: audit-py
