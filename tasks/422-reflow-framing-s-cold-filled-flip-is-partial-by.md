---
id: "[#422]"
title: "`reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the self-contradiction it leaves"
status: open
priority: P2
size: S
theme: "[E1] Handoff continuity"
story: "[S2] Finish the v5 handoff machinery deferred at the #149 flip"
serialize-group: handoff
generates: BACKLOG.md
---

- [#422] [P2][S] **`reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the self-contradiction it leaves** (mechanism VERIFIED): `reflow_framing` replaces only the exact `_FRAMING` block pairs. The precision is **deliberate** — differently-worded cold prose is not matched, so hand-authored narrative is never clobbered (RF-6). **The defect is the missing detector, not the narrow replace:** on the witnessed fold, boot/residual flipped while five cold-state claims survived in `PROBES.md`, so the bundle asserted both NARROWS and FULL — **no drift-check catches this, because each claim is checked against state, never against the others**. Do **not** widen the replace (reintroduces the clobber RF-6 prevents) — the fix is detection · Done when: a post-fold check FAILs on a bundle carrying cold-state framing prose after a FILLED flip (a `--check`-shaped leg wired where the fold runs), pinned by a test seeding a hand-authored cold claim in `PROBES.md` · refs `scripts/gen_handoff.py:270-293`, `scripts/assemble_paste.py:97-105`, protocols/HANDOFF_PROCESS.md §13 · kill-candidates: none — #298/#404 are disjoint; neither owns the post-fold gap · serialize-group: handoff
