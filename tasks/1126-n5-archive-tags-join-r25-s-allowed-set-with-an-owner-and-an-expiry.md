---
id: "[#1126]"
title: "N5: archive/* tags join R25's allowed set with an owner and an expiry"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1126] [P2][S] **N5: archive/* tags join R25's allowed set with an owner and an expiry** - Operator order 2026-09-28 (handoff cut): origin carries `archive/*` tags — the seven R24 tags `archive/worktree-lane-{codespace-proof,moments-fire,python-standard-1,runtime-data-home,scope-guard,teardown-visible,transport-rclone}` (preserved FAILED/kept lane tips) and the older `archive/drafts-2026-07-07`. Each joins R25's allowed set with an owner and an expiry; each is deleted when its lane's redo merges or the operator drops it. Nothing deleted at filing · Done when: R25's allowed-set data lists every `archive/*` tag with owner + expiry + close condition, and the leftovers gate refuses an unlisted or expired one · refs to-cc/BATCH-LEFTOVERS-GATE-2026-09-28.md, to-browser/SESSION-handoff-cut-2026-09-28.md · kill-candidates: none -- no open row tracks archive tags
