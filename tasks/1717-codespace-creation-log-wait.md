---
id: "[#1717]"
title: "Codespace creation-log wait is shorter than the devcontainer build"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1717] [P1][S] **Codespace creation-log wait is shorter than the devcontainer build** - _creation_log_refusal gave up after 3 reads x 20 s while a devcontainer build runs longer, refusing a healthy box · Done when: the wait reads the creation log until its end marker, bounded (900 s); a test with a fake slow build passes · owner: E2 lane. target batch: E2.1 · touches: scripts/dispatch.py, 	ests/test_codespace_delivery_fix.py · kill-candidates: none -- no open row covers this · refs 	o-browser/RATIFICATION-2026-10-23.md D1, 	o-browser/RATIFICATION-2026-10-22.md K4 · source: lane codespace-delivery-fix (LANE-codespace-delivery-fix.md, batch E2.1)
