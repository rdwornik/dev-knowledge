---
id: "[#645]"
title: "`INSTALL.md`'s repo-root path is retired to `docs/`, not allow-listed into the seal"
status: open
priority: P2
size: S
theme: "[E6] Cross-repo universalization"
story: "[S17] Make new-repo scaffolding correct-by-default"
generates: BACKLOG.md
---

- [#645] [P2][S] **`INSTALL.md`'s repo-root path is retired to `docs/`, not allow-listed into the seal** — the carrier places `INSTALL.md` at the repo root and the tree seal refuses a stray root markdown file, so the component is circular by construction: the mechanism that ships it is the reason it fails. DECLARE-REVIEWS finding R-3 proposed a seal-allowlist entry sourced from the manifest; the first sitting **overruled that** and ruled the root path RETIRED instead — allow-listing is a waiver, and lane V-3 had just withdrawn 132 of those, so adding one back to keep a mis-homed file is the shape the seal exists to end. Under homes-by-kind an install doc's home is `docs/`. `[#315]`, which put the file at the root, is CLOSED and its body is not its ruling · Done when: the component's declared path is under `docs/`, the v1.5.0 carrier manifest names the new path, `root_allowlist.files` gains no entry, and win-tooling's `test_repo_root_carries_no_stray_markdown` goes from RED to GREEN · refs DECLARE-SITTING ruling 6, DECLARE-REVIEWS §B R-3, `deploy/manifest-v1.5.0.yaml`, `plugins/tier1-lifecycle/INSTALL.md`, `[#315]` · source: DECLARE-SITTING ruling 6, filed by batch V lane V-4
