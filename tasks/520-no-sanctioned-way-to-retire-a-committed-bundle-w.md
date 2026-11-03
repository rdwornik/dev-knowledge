---
id: "[#520]"
title: "No sanctioned way to retire a committed bundle whose seal is wrong"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S7] Wire up the lifecycle hooks the workflow relies on"
serialize-group: handoff
generates: BACKLOG.md
---

- [#520] [P2][S] **No sanctioned way to retire a committed bundle whose seal is wrong** — `docs/handoffs/2026-08-01-dev-knowledge-architect-2` declares its SIBLING's slug (same stem, no `-2`), so `check_seal_identity` FAILs it on every `pre-commit run --all-files` sweep. Because that sibling directory EXISTS, the bundle's own self-references (Slug row, PROBES P0c/P3/P8, the embedded `/handoff-verify`) verify green about the WRONG bundle. Pre-existing at `80dd54d6`, untouched by batch 2. `docs/handoffs/` is immutable, so this is a rule gap in an artifact that cannot be edited; direction ruled — retire via an external dated marker, bundle left byte-unchanged. · Done when: the marker surface is defined, that bundle carries one, and `check_seal_identity` skips a marked-retired bundle, with a test pinning both halves · refs scripts/check_seal_identity.py, protocols/STANDING_RULINGS.md H1, [#475] · kill-candidates: none — [#310] owns annotating a bundle COLD/incomplete, a different state from a structurally wrong seal · serialize-group: handoff
