---
id: "[#1329]"
title: "consumer_at_landing accepts the integrator merge receipt; the Codex-review organ writes the consumer line"
status: closed
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
depends-on: "#1328"
generates: BACKLOG.md
---

- [#1329] [P1][M] **consumer_at_landing accepts the integrator merge receipt; the Codex-review organ writes the consumer line** - R42.2 + R42.4 (`to-browser/RATIFICATION-2026-09-30.md` v2): three audits (`2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md` merged `ae1a4170`, `2026-09-29-codex-lane-scope-guard-2-repair-1.md` merged `13fce088`, `2026-09-30-codex-lane-handoff-boot-dispatch-repair-1.md` merged `a2443799`) hard-FAIL `consumer_at_landing` and block the handoff cut. No route clears them: `undeclared()` (`scripts/consumer_at_landing.py:375`) reads only the audit's own text, audits are immutable, and the disposition register clears WARNs only (`scripts/audit.py:6813`). Half of the one handoff-unblock lane R42.4 orders, with `[#1330]`. · depends-on: #1328 · Done when: RED-first, (1) an audit whose lane's integrator merge receipt names it counts as declaring a consumer, and the three audits above clear the FAIL with no edit to them and no exclusion entry (R38); (2) the Codex-review organ, from its `[#1328]` hub source, writes a governance citation or `no-consumer:` line into every new review record, pinned by a test · touches: `scripts/consumer_at_landing.py` (`undeclared`, `read_artifact`, the manifest-link route at :352 as precedent, `DETECTOR_ID` v2->v3), `scripts/audit_checks/check_consumer_at_landing.py`, `scripts/batch_manifest.py` if reused, the merge-receipt writer (`logs/MERGE-RECEIPTS.jsonl` and its writer), `ecosystem/audit-consumer-baseline.json` (re-measure + re-stamp), `tests/test_consumer_at_landing.py`, the `[#1328]` organ source and its test · refs scripts/consumer_at_landing.py, tests/test_consumer_at_landing.py, deploy/codex-review.ps1, deploy/codex-review-lib.ps1, deploy/codex-review.md, tests/test_codex_review_consumer.py, deploy/carrier_codexreview.py, tests/test_deploy_codex_review_carrier.py, deploy/manifest-v1.5.0.yaml, ecosystem/audit-consumer-baseline.json · kill-candidates: none -- no open row tracked this route before this entry · **CLOSED 2026-10-01** — evidence e085c17f
