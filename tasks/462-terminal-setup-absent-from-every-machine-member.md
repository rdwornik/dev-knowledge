---
id: "[#462]"
title: "terminal-setup is declared fleet (ADR-104, VISION) but absent from EVERY machine membership surface — wave-1 input"
status: open
priority: P2
size: S
theme: "[E9] Fleet Desired-State System (North Star)"
story: "[S25] Converge surfaces in waves, with a mechanical done-signal"
serialize-group: architecture
generates: BACKLOG.md
---

- [#462] [P2][S] **terminal-setup is declared fleet (ADR-104, VISION) but absent from EVERY machine membership surface — wave-1 input** — surfaced by the 2026-07-30/31 nightly conformance digests (findings N4/S3), grep-verified live 2026-07-31: `ecosystem/registry.md` has no row, `ecosystem/index.yaml` no entry, no `ecosystem/terminal-setup/` state dir — yet ADR-104 declares it one of the 9 fleet repos and VISION.md:111 lists it. Structural lesson to carry, not just a missing row: the [#382] census could not SEE this gap because it censused `registry.md` itself — a membership census read off one registry cannot detect a member missing from that registry; membership needs a wider source (the ADR-104 declaration vs each machine surface, diffed). And per ADR-109 §2 `registry.md` loses authority anyway, so the fix is NOT a hand-added registry row — it is making the [#383] wave-1 desired-state contract carry the full ADR-104 member set, terminal-setup included, with the declaration-vs-surface diff as the census method. · Done when: the wave-1 desired-state fleet member set includes terminal-setup (or an operator ruling removes it from the fleet), and the wave-1 census method diffs the ADR-104 declaration against machine surfaces rather than reading one registry · refs ADR-104, ADR-109, VISION.md, ecosystem/registry.md, docs/audits/2026-07-30-conformance-nightly-digest.md, docs/audits/2026-07-31-conformance-nightly-digest.md, #383 · kill-candidates: none — [#383] owns wave execution, this is a wave-1 input it must not lose; no open row names the terminal-setup gap · serialize-group: architecture
