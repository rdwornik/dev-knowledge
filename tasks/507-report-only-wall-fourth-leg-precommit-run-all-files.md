---
id: "[#507]"
title: "Report-only wall — decide the fourth recorded leg (`pre-commit run --all-files`)"
status: open
priority: P3
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
serialize-group: architecture
generates: BACKLOG.md
---

- [#507] [P3][S] **Report-only wall — decide the fourth recorded leg (`pre-commit run --all-files`)** — the [#501] wall re-runs **three of the seventeen** client-side gates (`pytest` — not a hook at all —, `audit.py health`, the anchor backstop). `ruff` and 13 others are not, so a `--no-verify` push carrying a ruff violation leaves **no server record** — and that record is the wall's whole point, being the one surface a local bypass cannot reach. Ch6's over-claim was corrected editorially; this row is the coverage half. A DECISION, not a chore: the leg changes what the record MEANS, adds runtime to every push, and overlaps two legs already recorded. · Done when: a ruling records either the leg landed (with a run showing a bypassed violation recorded server-side) or an explicit accepted-with-reason hold naming what stays unrecorded · footprint: `.github/workflows/report-only-wall.yml`, `ARCHITECTURE.md` Ch6, `tests/test_report_only_wall.py` · refs #501, #153, night-audit LA-3 · kill-candidates: none — #501 is closed and owned the recorder's existence, not its coverage · serialize-group: architecture
