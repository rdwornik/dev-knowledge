---
id: "[#654]"
title: "The 037 render-pass ruling has no intake file, so `reconciled_with` stays hand-typed"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
generates: BACKLOG.md
---

- [#654] [P2][M] **The 037 render-pass ruling has no intake file, so `reconciled_with` stays hand-typed** — INBOX-037 and its amendment rule a commit-time render pass: governed markdown is template plus data, marked regions are rendered in place, the rendered file is what is committed, and a committed file that differs from a fresh render is a FAIL. Prose references stay the graph's job, not the renderer's. No `docs/intake/` file carries any of it — 034 and 035 were filed as intakes `#86` and `#87`; 037 arrived after the last filings session and nothing has run since. The first sitting's ruling 11 depends on it: `reconciled_with` becomes DERIVED by the version ratchet, and adding a hand-stamped schema field now creates the copy the ratchet would overwrite · Done when: the 037 ruling is filed as a `docs/intake/` doc under ADR-98 with the render pass's scope and its first dry-run count as the acceptance number, and `AMEND-037-001`'s `carried-by:` names that path · refs DECLARE-SITTING ruling 11, `AMEND-037-001` and INBOX-037 on the transport, `[#642]` · source: DECLARE-SITTING ruling 11, filed by batch V lane V-4
