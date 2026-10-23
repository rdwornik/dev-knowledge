---
id: "[#1716]"
title: "Codespace delivery quoting (FR9: one quoted remote command)"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1716] [P1][S] **Codespace delivery quoting (FR9: one quoted remote command)** - Every gh codespace ssh -c <box> -- ... passed its remote command as several argv elements, so the remote shell re-split it (a path with a space, or sh -c with ;/<, broke) · Done when: every ssh call carries ONE quoted remote command; a test fails on the unquoted argv · owner: E2 lane. target batch: E2.1 · touches: scripts/dispatch.py, 	ests/test_codespace_delivery_fix.py · kill-candidates: none -- no open row covers this · refs 	o-browser/RATIFICATION-2026-10-23.md D1, 	o-browser/RATIFICATION-2026-10-22.md K4 · source: lane codespace-delivery-fix (LANE-codespace-delivery-fix.md, batch E2.1)
