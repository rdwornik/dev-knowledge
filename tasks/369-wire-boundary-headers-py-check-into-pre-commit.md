---
id: "[#369]"
title: "Wire `boundary_headers.py --check` into pre-commit"
status: open
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: pre-commit-config
generates: BACKLOG.md
---

- [#369] [P3][S] **Wire `boundary_headers.py --check` into pre-commit** — the reader-visible ownership headers' generated-not-hand-maintained property rests on the **test suite alone**: a hand-edited header is caught at ship-gate but is **unenforced at commit time**, unlike every sibling generated surface (six regen-and-diff hooks, `CLAUDE.md` §9). Route to **W6**. · Done when: the hook is registered and blocks a hand-edited header, `CLAUDE.md` §9 lists it, and `ecosystem/doc-counts.md` agrees with the live hook roster · **RE-SCOPED 2026-08-12 — off the absolute gate count** (register M-7 `N2-R1-05`): the struck clause read "doc-counts reflects 16 gates" against a file reading **17**, and the roster has grown again since. An absolute number is the wrong predicate *regardless of repair* — it re-breaks every time a hook lands — so the clause above is agreement-with-the-regen, true at any roster size · refs scripts/boundary_headers.py, #352 · kill-candidates: none — no open task covers this commit-time gap · serialize-group: pre-commit-config
