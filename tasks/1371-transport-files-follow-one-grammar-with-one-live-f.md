---
id: "[#1371]"
title: "Transport files follow one grammar with one live file per subject, and a generated index and a non-deleting janitor keep it so"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1371] [P1][M] **Transport files follow one grammar with one live file per subject, and a generated index and a non-deleting janitor keep it so** - R71 (operator, 2026-10-04): every transport file follows the registry's grammar KIND-subject-date, superseded files leave the reading path for an archive, and the transport lint enforces both, including on the seat's own writes. R79 item 1 ratifies the mechanism: the registry and each file's `supersedes:` decide current versus archived, the generated `to-browser/INDEX.md` is the seat's first read, and the `transport_lint` janitor may create `<folder>/archive/YYYY-MM/` and move superseded files into it, never deleting. · Done when: `transport_lint` refuses a transport file whose name breaks KIND-subject-date, including one written by the seat, and refuses a second live file for one subject (tests); the generated `to-browser/INDEX.md` lists only current files; the janitor creates `archive/YYYY-MM/` and moves superseded files into it, and a test asserts the file count before equals the count after (it deletes nothing) · owner: lane `b2-transport-lint` (W1-6) builds the lint; the W2 lane `b2-transport-index` builds the index and the janitor after W1-6 · touches: `scripts/transport.py` and `ecosystem/transport-registry.yaml` (W1-6), the index generator (W2), tests · kill-candidates: none -- `[#978]` registers the file kinds; it does not enforce one live file per subject or archive · refs `[#978]`, `ecosystem/transport-registry.yaml`, `protocols/STANDING_RULINGS.md` section AR (R71, R79) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R71, R79 in `to-browser/RATIFICATION-2026-10-04.md R71, R79`
