---
id: "[#315]"
title: "`INSTALL.md` uniform fleet-wide, hub-owned, deploy-carried"
status: open
priority: P3
size: S
theme: "[E6] Cross-repo universalization"
story: "[S17] Make new-repo scaffolding correct-by-default"
generates: BACKLOG.md
---

- [#315] [P3][S] `INSTALL.md` uniform fleet-wide, hub-owned, deploy-carried (operator ruling; fleet-boundary-matrix Surface 8) — the tier1-plugin-install `INSTALL.md` becomes a hub-canonical, deploy-manifest-carried file present in every onboarded repo (sibling of #280). Rationale: content is methodology-generic (tier1 plugin install) but placement was accidental — only the co-authoring repo (ai-council) carried a root copy; the operator ruled uniform-everywhere over accept-local. Reversible. STRUCTURAL SPEC: carry as a manifest doc-artifact — **path** `INSTALL.md` (repo root), **source** `plugins/tier1-lifecycle/INSTALL.md`; needs the #280-class doc carrier (global-config is L0 user-machine single-file, not a repo-root doc carrier — §3.2). · Done when: `INSTALL.md` has a hub-canonical source (`plugins/tier1-lifecycle/INSTALL.md`) AND ships via a deploy manifest doc-artifact (path `INSTALL.md`) so each onboarded consumer carries it (n≥1) · refs docs/audits/2026-07-11-technical-fleet-boundary-matrix.md (Surface 8), plugins/tier1-lifecycle/INSTALL.md, deploy/manifest-v1.3.1.yaml, #280 · kill-candidates: none — operator-ruled disposition (2026-07-11)
