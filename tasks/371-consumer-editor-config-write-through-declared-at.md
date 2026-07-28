---
id: "[#371]"
title: "Consumer editor-config write-through — declared at v1.4.0, never built, never ticketed"
status: open
priority: P2
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#371] [P2][S] **Consumer editor-config write-through — declared at v1.4.0, never built, never ticketed** — `deploy/manifest-v1.4.0.yaml:325` carrier `editor-config` is `implemented: false` ("the consumer write-through is the next ticket"); never filed, so the gap sat untracked. Live: both consumers carry a 77/72-byte `.vscode/settings.json` with **zero** highlight keys, so the user-global extension finds nothing to read there — the boundary renders nowhere it matters. Consumers otherwise READY (both `CLAUDE.md` carry both owner values; regexes yield 8 grey/13 navy corp, 8/15 ai-council). **Vehicle decided by the buy-vs-build fleet-template ADR (intake pending) — do NOT implement bespoke** (R7 pattern). ADR-93: a write MERGEs into the existing `files.watcherExclude`, never clobbers. · Done when: the ADR rules the vehicle, the config reaches both consumers under it, and `implemented:` reflects reality · refs deploy/manifest-v1.4.0.yaml, ADR-93, docs/audits/2026-07-20-technical-352-boundary-render-diagnostic.md, #352 · kill-candidates: none — a declared-but-unbuilt carrier half no open task covers; [#352] is its parent, not its owner · serialize-group: settings-json
