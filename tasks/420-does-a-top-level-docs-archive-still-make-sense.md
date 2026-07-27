---
id: "[#420]"
title: "Does a TOP-LEVEL `docs/archive/` still make sense?"
status: open
priority: P3
size: S
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
serialize-group: architecture
source: BACKLOG.md
derived: true
---

- [#420] [P3][S] **Does a TOP-LEVEL `docs/archive/` still make sense?** — operator-raised structural question, filing only. Each docs area now carries its own archive (`docs/decisions/archive/`, `docs/handoffs/archive/`, `docs/intake/archive/`; `docs/audits/` deliberately has none — ADR-100 keep-all-accepted + a count-tiered index), while the top-level `docs/archive/` still holds 9 external-research / scoping / evidence files under its ADR-60 "pending-classification triage queue" charter. Two readings to rule between: it is a genre the per-area archives do not cover (unclassified inbound research), or it is a residue whose contents belong in a live area. **Do NOT touch `docs/archive/` while this is open** — no move, no promotion, no deletion. · Done when: the top-level archive is ruled kept-with-a-restated-charter or dissolved into per-area homes, with each of the 9 files given a destination · refs docs/archive/README.md, ADR-60 amendment 2026-05-27, ADR-100, ADR-101, protocols/PLAYBOOK.md "docs/ folder taxonomy" · kill-candidates: none — no open task owns the docs/ archive taxonomy · serialize-group: architecture
