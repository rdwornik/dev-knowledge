---
id: "[#227]"
title: "Relocate AGENT_FRAMEWORK.md out of protocols/"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#227] [P3][S] Relocate AGENT_FRAMEWORK.md out of protocols/ — `protocols/AGENT_FRAMEWORK.md` is a self-labelled v0.1 unimplemented stub with no readers (no living doc references it) and no gate; it is not an authoritative loaded protocol, so it does not belong in the authoritative `protocols/` dir. Move it to `docs/` (idea / design-note home) and fix the one inbound ref (#1's `refs protocols/AGENT_FRAMEWORK.md`). · Done when: AGENT_FRAMEWORK.md lives under docs/ and every inbound ref resolves to the new path · refs protocols/AGENT_FRAMEWORK.md, #1, ADR-60
