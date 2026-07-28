---
id: "[#348]"
title: "Backlog grooming as a standing routine, not ad-hoc"
status: open
priority: P3
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: settings-json
depends-on: "#270"
generates: BACKLOG.md
---

- [#348] [P3][S] **Backlog grooming as a standing routine, not ad-hoc** (operator priority-program item 3, half (b)) — turn the improvised-per-session grooming pass into CONFIGURATION: a defined cadence, scope and trigger, rather than "whoever notices". **DECOMPOSED 2026-07-25** (a)->[#412], (c)->[#411]; holds (b) only — see 89ae1d1d. Builds on the load-gauge-first sequencing (#270) — that gates this. · Done when: the grooming cadence is captured as a routine definition (trigger, scope, consumption path) rather than per-session improvisation, gated behind #270's load-gauge · refs #270, #271, #324, #123, #411, #412, #419 · kill-candidates: none — operator-dictated priority-program item; #270 is a prerequisite, not a subsumer · depends-on: #270 · routine: trigger=on-demand (operator/session boot) · scope=BACKLOG.md rows · consumer=any session reading BACKLOG.md · consumption_path=BACKLOG.md in place · verified_by=validate_backlog · review_date=2026-08-26 · serialize-group: settings-json
