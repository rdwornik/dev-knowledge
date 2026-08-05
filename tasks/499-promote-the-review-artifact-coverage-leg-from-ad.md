---
id: "[#499]"
title: "Promote the review-artifact coverage leg to a hard pre-push gate"
status: deferred
priority: P3
size: M
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#499] [P3][M] **Promote the review-artifact coverage leg to a hard pre-push gate** — [#480]'s ruling is LAYERED: the advisory WARN-tier leg (`audit.check_review_artifact_coverage`) shipped with it; this row is the HARD leg, and it does not open on a date. **Evidence bar: 0 false positives over two consecutive windows, reported at each seal** — the advisory leg produces that data. The hard leg is a pre-push refusal shaped like `block_unanchored_push`. · Done when: two consecutive windows are sealed with the leg's false-positive count reported and equal to 0, the hard leg lands with its own tests, **AND the coverage debt is discharged — the PLAYBOOK rule written, a `coverage_scope` entry replacing the TEMPORARY `ecosystem/doc-code-edge.yaml` exemption, and the `# rule: review-artifact-coverage` marker reinstated in `scripts/audit.py`** (rider R2 — this row owns the exemption's expiry so it cannot outlive its reason) · refs scripts/audit.py, tests/test_review_artifact_coverage.py, scripts/block_unanchored_push.py, ecosystem/doc-code-edge.yaml, #480, #483 · kill-candidates: none — no open row owns the hard flip · DEFER — peg: 0 false positives reported at two consecutive seals
