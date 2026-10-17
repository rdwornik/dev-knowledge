---
id: "[#1374]"
title: "All dispatch lives in the hub for local, Codespace and cloud, win-tooling keeps at most a shim, and an ADR amends R11(3)"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1374] [P1][L] **All dispatch lives in the hub for local, Codespace and cloud, win-tooling keeps at most a shim, and an ADR amends R11(3)** - R75 (operator, 2026-10-04): local, Codespace and Anthropic-cloud dispatch all live in the hub; win-tooling keeps at most a thin shim. The cloud leg needs an amendment to ARCHITECTURE R11(3): the operator's direction is yes, the ADR is written in B2 W2 for him to ratify. This repeats his 2026-09-27 stance, which was never carried. · Done when: a test shows win-tooling's dispatch entry is a shim (it holds no routing logic, only a call into the hub); `scripts/dispatch.py` routes each of the three substrates through one verb; an ADR amending ARCHITECTURE R11(3) for the cloud leg exists with Status Proposed, citing R75 and the 2026-09-27 stance; ratifying it is the operator's act and is recorded as such · owner: lane `b2-dispatch-local-sole` (W1-4) makes local sole; B2 W2 writes the ADR and adds the cloud leg; the operator ratifies · touches: `scripts/dispatch.py`, the win-tooling shim (a child repo, so recorded not edited from here), `docs/decisions/` (the new ADR), tests · kill-candidates: none -- `[#931]` builds the launch adapter; no open row moves the cloud leg into the hub · refs `ARCHITECTURE.md`, `[#931]`, `scripts/dispatch.py`, `protocols/STANDING_RULINGS.md` section AR (R75) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R75 in `to-browser/RATIFICATION-2026-10-04.md R75`

**Resume pointer** (2026-10-17, AMEND-1-BATCH-CUT-2026-10-17): the unfinished BW lane `lane-bw-1374-lane-controller` (3/7 done) is preserved as the tag `archive/worktree-lane-bw-1374-lane-controller` @ b1db35ff (its branch deleted); resume with `git switch -c worktree-<name> archive/worktree-lane-bw-1374-lane-controller`. Three open findings, from `LANE-END-lane-bw-1374-lane-controller.md` (Codex gpt-5.6-terra r1, REQUEST-CHANGES HIGH x3): (1) `scripts/dispatch.py:848` slug-only ledger; (2) `scripts/merge_path.py:257` squash/FF bypass; (3) the R8 end-to-end usage test (Copilot + Codex lane) is absent. Also open: `land` refuses the integrator own no-change merges (LANE-UNATTRIBUTED, defect against Done 3).
