---
id: "[#242]"
title: "ADR status-flip coherence check"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#242] [P2][M] ADR status-flip coherence check — the ratified go-forward status-flip pattern (ADR-94, Accepted 2026-07-03: an ADR's *status line* is editable in place on ratification while decision content stays frozen) standardizes on Pattern B (ADR-92's direct header edit). But ADR-88/89 still carry FROZEN `Proposed` headers reconciled only by an in-file amendment marker (Pattern A), and NO machine check reconciles a frozen `Proposed` header against the README-index / CLAUDE effective "Accepted" status (the gap the 2026-06-21 JOURNAL ratify entry records). Build a read-only audit leg that flags an ADR whose header status diverges from its README-index effective status (and, once ADR-88/89 are retro-normalized, that go-forward flips follow Pattern B). Sibling of #112 (the ADR immutable-zone amend helper); absorbs #7's ADR-frontmatter validation leg (transcript/ADR frontmatter + supersession + template checks). · Done when: a seeded ADR with a header↔README status divergence is flagged by an audit check, with tests · refs ADR-94, ADR-88, ADR-89, ADR-92, docs/decisions/README.md, #112 · serialize-group: audit-py
