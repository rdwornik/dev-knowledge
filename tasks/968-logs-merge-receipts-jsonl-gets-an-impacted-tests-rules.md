---
id: "[#968]"
title: "`logs/MERGE-RECEIPTS.jsonl` gets an `impacted_tests.RULES` mapping before it reds every gate"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
implements: "ADR-120"
generates: BACKLOG.md
---

- [#968] [P1][S] **`logs/MERGE-RECEIPTS.jsonl` gets an `impacted_tests.RULES` mapping before it reds every gate** - D5: each merge commit folds a row into `logs/MERGE-RECEIPTS.jsonl`, and no `impacted_tests.RULES` entry claims that path; replaying `select --ref <merge>^1` on a wave-4b merge returns `# FULL SUITE`, which `gates.py::impacted_tests_gate` turns into a RED refusal on the very next commit that touches only that file (`docs/audits/2026-09-23-technical-verify-time.md` §Latent hazard, confirmed `docs/audits/2026-09-23-technical-audit-crosscheck.md` C10) · Done when: `logs/MERGE-RECEIPTS.jsonl` has a `RULES` entry in `scripts/impacted_tests.py` that maps it to a narrow, correct test set (not FULL SUITE); a RED-first test stages only that file and asserts `impacted_tests_gate` does not refuse · implements: ADR-120 · refs `scripts/impacted_tests.py`, `scripts/gates.py`, `logs/MERGE-RECEIPTS.jsonl`, `docs/audits/2026-09-23-technical-verify-time.md` · kill-candidates: none -- no open row maps this path
