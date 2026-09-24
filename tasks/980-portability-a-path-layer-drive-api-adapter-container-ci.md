---
id: "[#980]"
title: "Portability: a path layer + Drive API adapter + container CI job removes the Codespace blocker"
status: open
priority: P2
size: L
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#980] [P2][L] **Portability: a path layer + Drive API adapter + container CI job removes the Codespace blocker** - D21: Codespace dispatch has been blocked by Windows paths and shell tokens all window, on a repeatedly-stated "no Linux Drive client" premise that later review found false (`to-cc/DECLARE-OFFBOX-PORTABILITY-2026-09-23.md`) · Done when: the path layer (D20) plus a Drive API or rclone adapter let a Codespace or container session read/write the transport with no Windows-path assumption; a container CI job exercises one full lane dispatch/handback round-trip and passes · implements: ADR-120 · refs `to-cc/DECLARE-OFFBOX-PORTABILITY-2026-09-23.md`, `docs/audits/2026-09-23-technical-window-defects.md` · kill-candidates: none -- no open row builds the Drive API/rclone adapter or the container CI job
