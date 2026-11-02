---
id: "[#1125]"
title: "N5: absorb or retire the claude/conformance-* digest branches"
status: closed
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1125] [P2][S] **N5: absorb or retire the claude/conformance-* digest branches** - R26 (to-browser/RATIFICATION-2026-09-28.md v5) item 4: ten `claude/conformance-2026-09-18..27` branches stay on origin under their standing rule (git-discipline I-F3: protected until absorbed); R24 does not override it. N5 absorbs each (then it deletes at its own merge) or the operator retires it, and until then they are listed in R25's allowed set with the rule that protects them and an expiry · Done when: no `claude/conformance-*` branch on origin is both unabsorbed and unlisted, and R25's allowed-set data names the rule and an expiry for any that remain · refs .claude/rules/git-discipline.md, to-cc/BATCH-LEFTOVERS-GATE-2026-09-28.md · kill-candidates: none -- no open row tracks conformance absorption · **CLOSED 2026-11-02** — evidence a062d59d28fe553cd7941717f9da2cc7e45330b0
sweep-close: legacy-sweep · witnesses checked=K1,K2,K3 absent=K1,K2,K3 · filed 2026-09-28 before 2026-10-01; no KEEP witness (K1 protected, K2 alive in code, K3 agreed LINE P1/P2) holds
