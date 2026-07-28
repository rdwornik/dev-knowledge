---
id: "[#126]"
title: "Backpressure-loop pattern evaluation"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S19] Decide the undecided artifact/tool models"
generates: BACKLOG.md
---

- [#126] [P2][M] Backpressure-loop pattern evaluation — a sanctioned in-session *iterate-until-green* primitive for unknown-iteration tasks (lint/type-debt burndown; red→green after a rebase or dependency bump). **VERIFY FIRST:** current `/loop` command semantics in CC docs/help — the ADR-74 REJECTED row covers `/loop` as a *persistence host* ONLY, not in-session repair (ADR-74 Amendment 2026-06-07). Doctrine bounds: operator-invoked only, never on automated paths, **deterministic checks as the feedback source** (pytest/ruff/type-check, not model judgment), a **mandatory iteration budget**, and "do-not-change-tests"-class constraints (fix code to satisfy fixed acceptance criteria, never edit the criteria). Pilot target: corp-monorepo (**execute in the corp dedicated chat**, ADR-41 — queue-only here) · absorbs #106 (Auto Mode go/no-go) + #155 (loops-architecture scope) · Done when: a go/no-go is recorded with the doctrine bounds + a corp pilot result (or an explicit operator drop) · refs ADR-74 (REJECTED row, now persistence-scoped), ADR-76, #8 (Stop `additionalContext` = native backpressure surface), #127, generativeprogrammer backpressure article 2026-06
