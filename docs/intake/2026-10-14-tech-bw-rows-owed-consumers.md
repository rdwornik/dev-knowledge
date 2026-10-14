---
intake-id: 107
status: SEED
origin: "operator decision 2026-10-14 (R106, 'ROWS-OWED means rows, not silence'); batch BW close packet section 3 ROWS-OWED, 2026-10-12"
consumed-by:
---

# SEED -- the 23 BW-batch audits that no row, ADR or intake consumes

`scripts/consumer_at_landing.py` lists 23 audits as unconsumed and new against `ecosystem/audit-consumer-baseline.json` (`logs/receipts/green-main-2026-10-14/stage-1-spec.json`, defect bw912). The BW close packet (`docs/audits/2026-10-12-technical-batch-bw-close-packet.md` section 3) records the reds as ROWS-OWED. Each artifact has one carrier row, [#1510]-[#1532]. A row decides nothing: it asks for the artifact's finding to be owned or dispositioned (ADR-111).

Carrier rows: [#1510]-[#1532].

- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1001-hook-launcher.md` -- row [#1510]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1001-sessionstart-one.md` -- row [#1511]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1103-registry-repoint.md` -- row [#1512]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1368-lane-report-rollup.md` -- row [#1513]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1374-lane-controller.md` -- row [#1514]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1378-rulings-landing.md` -- row [#1515]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1439-transport-index.md` -- row [#1516]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1447-distill-kind-fix.md` -- row [#1517]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-1450-boot-teaching.md` -- row [#1518]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-242-adr-lifecycle.md` -- row [#1519]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-670-harness-probes.md` -- row [#1520]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-680-handoff-gen.md` -- row [#1521]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-735-reuse-gate.md` -- row [#1522]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-781-system-map.md` -- row [#1523]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-893-b2w3-carry.md` -- row [#1524]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-912-known-reds-expiry.md` -- row [#1525]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-926-main-red.md` -- row [#1526]
- `docs/audits/2026-10-12-technical-batch-bw-launch-contracts/LANE-bw-958-required-tools.md` -- row [#1527]
- `docs/audits/2026-10-10-codex-b2w2-transport-index.md` -- row [#1528]
- `docs/audits/2026-10-13-codex-bw-1439-transport-index.md` -- row [#1529]
- `docs/audits/2026-10-13-codex-lane-bw-670-harness-probes.md` -- row [#1530]
- `docs/audits/2026-10-13-technical-lane-bw-1001-sessionstart-measurement.md` -- row [#1531]
- `docs/audits/2026-10-13-verification-harness-probes-receipts.md` -- row [#1532]

Note: the 18 undated `LANE-bw-*.md` contracts cannot be consumed by a citation (the pool tokenizer extracts dated names only); their route is a batch-manifest link or a baseline entry.
