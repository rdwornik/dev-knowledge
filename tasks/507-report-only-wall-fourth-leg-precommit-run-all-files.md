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

- [#507] [P3][S] **Report-only wall — decide the fourth recorded leg (`pre-commit run --all-files`)** — the [#501] wall re-runs **three of the seventeen** client-side gates off-host (`pytest` — not a hook at all —, `audit.py health`, the anchor backstop). `ruff` and 13 others are not re-run, so a `git push --no-verify` carrying a ruff violation still leaves **no server record** — and the server record is the wall's entire reason to exist, being the one surface a local bypass cannot reach. The ARCHITECTURE Ch6 over-claim ("the client-side gate set re-run off-host") was corrected editorially 2026-08-07, which closes the honesty gap and leaves the coverage gap open. **This row is the coverage half, and it is a DECISION not a chore:** adding the leg changes what the record MEANS (today "these three legs on the landed tree", after "the gate set"), it adds runtime to every push, and `pre-commit run --all-files` overlaps the two legs already recorded. Weigh against the alternative of leaving it at three and treating the narrowed Ch6 wording as the final answer. Architect-called per the batch-1 night audit LA-3. · Done when: a ruling records either the fourth leg landed (with a run showing a `--no-verify`-style ruff violation recorded server-side) or an explicit accepted-with-reason hold naming what stays unrecorded · footprint: `.github/workflows/report-only-wall.yml`, `ARCHITECTURE.md` Ch6, `tests/test_report_only_wall.py` · refs #501, #153, docs/audits/2026-08-06-technical-batch1-verification.md §5 LA-3 · kill-candidates: none — #501 is closed and owned the recorder's existence, not its coverage; no open row owns what the wall re-runs · serialize-group: architecture
