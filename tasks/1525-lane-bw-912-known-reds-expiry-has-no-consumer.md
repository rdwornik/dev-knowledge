---
id: "[#1525]"
title: "LANE-bw-912-known-reds-expiry.md has no consumer -- its finding is owned or dispositioned"
status: closed
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1525] [P3][S] **LANE-bw-912-known-reds-expiry.md has no consumer -- its finding is owned or dispositioned** - `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-912-known-reds-expiry.md` is unconsumed per `scripts/consumer_at_landing.py` (one of 23 audits new against `ecosystem/audit-consumer-baseline.json`, measured in `logs/receipts/green-main-2026-10-14/stage-1-spec.json` defect bw912). It is an undated launch contract, so the consumer_at_landing pool tokenizer (dated names only) cannot count a tasks/ or ADR citation as consumption; the route is a batch-manifest link or a baseline entry, not a citation. Filed as ROWS-OWED of `docs/audits/2026-10-12-technical-batch-bw-close-packet.md` section 3 ("rows for the three test_consumer_at_landing reds (ROWS-OWED at every BW land)"), operator decision 2026-10-14 R106 ("ROWS-OWED means rows, not silence"); listed with its 22 siblings in `docs/intake/2026-10-14-tech-bw-rows-owed-consumers.md` · Done when: the artifact is consumed by an OPEN or closed row, ADR or intake that owns or dispositions its finding, and `uv run --locked python scripts/consumer_at_landing.py` no longer lists it · refs `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-912-known-reds-expiry.md`, `scripts/consumer_at_landing.py`, `ecosystem/audit-consumer-baseline.json`, `docs/intake/2026-10-14-tech-bw-rows-owed-consumers.md` · kill-candidates: none -- no open row consumes this artifact (grep over tasks/ and docs/intake on 2026-10-14) · source: `docs/audits/2026-10-12-technical-batch-bw-close-packet.md` section 3; `logs/receipts/green-main-2026-10-14/stage-1-spec.json`

**Closed 2026-10-24 (lane ci-one-verdict-2):** linked by path from an Amendment 1 section of `docs/audits/2026-10-12-technical-batch-bw-manifest.md` (batch-manifest route, `explicit`); `consumer_at_landing.py` prints 801 unconsumed (was 802) and the baseline entry was removed (shrink only). Test: `tests/test_bw912_contract_consumed.py`.
