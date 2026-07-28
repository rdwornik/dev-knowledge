---
id: "[#347]"
title: "Formalize the engineering loop/harness end-to-end + sanctioned safe-deletion pattern"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
serialize-group: playbook
generates: BACKLOG.md
---

- [#347] [P2][M] Formalize the engineering loop/harness end-to-end + sanctioned safe-deletion pattern (operator priority-program item 2, 2026-07-18) — decompose the full dev loop into a governed harness: intake → functional-requirements (a functional-architect session that SEEDS the backlog) → ADR → implementation → sandbox/console dynamic testing → review → backlog-close + REAL deletion. Standing pain (operator): files get frozen/tombstoned instead of deleted — the junkyard effect; design a sanctioned safe-deletion path extending the proof-then-delete ruling on #122 (design question, not yet ruled). This entry is the decomposition/design anchor, not the build. · Done when: the loop-harness is decomposed into filed sub-arcs AND the safe-deletion pattern is ruled (sanctioned path defined or recorded permanent-defer-with-reason) · refs #122, #126, #278, ADR-70, ADR-98 · kill-candidates: none — operator-dictated priority-program item 2; no existing task subsumes the end-to-end harness or the safe-deletion ruling · serialize-group: playbook
