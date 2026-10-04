---
id: "[#1370]"
title: "Volatile facts have one source and every copy is generated, and the handoff boot's version follows its content"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1370] [P1][L] **Volatile facts have one source and every copy is generated, and the handoff boot's version follows its content** - R70 (operator, 2026-10-04): model ids, tool versions, document versions, dates and counts each have one source of truth; every other copy is generated from it at render time; a hand copy that disagrees with its source is a false positive under R59; and the handoff boot's version changes whenever its content changes. The operator's words: the problem is that prose manages a variable that changes. · Done when: a census lists each volatile-fact class with its single source and every place a copy is typed by hand; a RED-first lint refuses a hand copy that disagrees with its source (a fixture types a model id in prose that differs from `ecosystem/provider-registry.yaml`); a test shows that changing the handoff boot's content without changing its version stamp is refused; each class is either generated like `ecosystem/doc-counts.md` or listed in the census as an exception with its reason · owner: wave B2 W2: a generated-facts lane · touches: the generators and lints per class, `ecosystem/doc-counts.md`, `protocols/HANDOFF_BOOT.md` (stamp), tests · kill-candidates: none -- `[#1008]` sweeps six stale claims once; this row is the standing rule that stops their return · refs `[#1008]`, `ecosystem/provider-registry.yaml`, `ecosystem/doc-counts.md`, `protocols/STANDING_RULINGS.md` section AR (R70) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R70 in `to-browser/RATIFICATION-2026-10-04.md R70`
