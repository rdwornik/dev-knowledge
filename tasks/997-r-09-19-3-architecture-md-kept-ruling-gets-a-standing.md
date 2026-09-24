---
id: "[#997]"
title: "R-09-19-3: ARCHITECTURE.md KEPT ruling gets a STANDING_RULINGS entry, not just a BUILD-LIST line"
status: open
priority: P2
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#997] [P2][S] **R-09-19-3: ARCHITECTURE.md KEPT ruling gets a STANDING_RULINGS entry, not just a BUILD-LIST line** - R-09-19-3 (`docs/audits/2026-09-23-technical-handoff-readiness.md` §6): the ruling that `ARCHITECTURE.md` is KEPT, with a stated exit condition, lives only in `protocols/BUILD-LIST.md` (expiry 2026-11-18) and has never been landed in `protocols/STANDING_RULINGS.md`, so it does not survive past BUILD MODE's own end · Done when: `protocols/STANDING_RULINGS.md` carries an entry for the ARCHITECTURE.md-KEPT ruling, citing its exit condition and the 2026-11-18 backstop, so the ruling outlives the BUILD-LIST file it currently depends on · implements: ADR-120 · refs `protocols/BUILD-LIST.md`, `protocols/STANDING_RULINGS.md`, `docs/audits/2026-09-23-technical-handoff-readiness.md` · kill-candidates: none -- no open row lands this ruling in STANDING_RULINGS
