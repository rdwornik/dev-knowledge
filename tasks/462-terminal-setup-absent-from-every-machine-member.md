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

- [#462] [P2][S] **terminal-setup is declared fleet (ADR-104, VISION) but absent from EVERY machine membership surface — wave-1 input** — conformance-digest findings N4/S3, grep-verified live at filing: no `registry.md` row, no `index.yaml` entry, no `ecosystem/` state dir — yet ADR-104 and VISION.md:111 declare it one of the 9 fleet repos. Structural lesson to carry: the [#382] census censused `registry.md` itself, so a member missing FROM that registry was invisible — membership needs the ADR-104 declaration diffed against each machine surface. And per ADR-109 §2 `registry.md` loses authority anyway, so the fix is the [#383] wave-1 desired-state member set carrying the full ADR-104 declaration, not a hand-added registry row. · Done when: the wave-1 member set includes terminal-setup (or an operator ruling removes it from the fleet) and the wave-1 census diffs the declaration against machine surfaces · refs ADR-104, ADR-109, VISION.md, docs/audits/2026-07-30-conformance-nightly-digest.md, #383 · kill-candidates: none — [#383] owns wave execution; no open row names the gap · serialize-group: architecture
