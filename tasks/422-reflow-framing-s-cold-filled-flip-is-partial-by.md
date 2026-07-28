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

- [#422] [P2][S] **`reflow_framing`'s cold→FILLED flip is partial by design, and nothing detects the self-contradiction it leaves** (surfaced 2026-07-25 folding the same bundle's supplement; mechanism VERIFIED): `reflow_framing` (`scripts/gen_handoff.py:270-293`) replaces only the exact `_FRAMING` cold/warm block pairs across `HANDOFF_BOOT.md`/`RESIDUAL.md`/`PROBES.md`. That precision is **deliberate and correct** — its docstring states differently-worded prose merely mentioning "generated EMPTY" is not matched, so hand-authored FILL-IN narrative is never clobbered (the RF-6 contract). **The defect is the missing detector, not the narrow replace:** on the 2026-07-25 fold the assembler reported flipping `HANDOFF_BOOT.md, RESIDUAL.md` and left `PROBES.md` untouched, where **five** hand-authored "supplement is generated EMPTY / the §13(d) beat fires FULL" claims survived. The bundle then asserted both NARROWS (boot) and FULL (probes) — a §8 self-contradiction inside one bundle that **no drift-check catches, because each claim is checked against state and never against the others**. Caught only by a manual post-fold grep sweep; a fold that nobody sweeps ships contradictory. Do **not** fix by widening the replace (that reintroduces the clobber RF-6 exists to prevent) — the fix is detection · Done when: a post-fold check FAILs on a bundle carrying cold-state framing prose after a FILLED flip (a `--check`-shaped leg over the bundle, wired where the fold runs), pinned by a test that seeds a hand-authored cold claim in `PROBES.md` and shows it caught · refs `scripts/gen_handoff.py:270-293` `reflow_framing` + `_FRAMING`, `scripts/assemble_paste.py:97-105` (the fold call site), protocols/HANDOFF_PROCESS.md §13 (the mechanized cold→FILLED flip), `docs/handoffs/2026-07-25-ai-council-architect/` (the witnessed instance) · kill-candidates: none — #298 is DEFERred generator polish (WARNs on `--epic-slug`), #404 is execution-mode framing; neither owns the post-fold coherence gap · serialize-group: handoff
