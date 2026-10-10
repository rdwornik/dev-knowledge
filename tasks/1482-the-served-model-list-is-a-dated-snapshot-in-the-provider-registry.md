---
id: "[#1482]"
title: "The served model list is a dated snapshot in the provider registry, admitted by a schema version bump"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1482] [P2][S] **The served model list is a dated snapshot in the provider registry, admitted by a schema version bump** - Seat ruling S-34 (`to-cc/AMEND-BATCH-B2-W3-2026-10-10.md` §4, lane 4, P-L4-3): for batch B2-W3, lane `b2w3-registry-repoint` ([#1452]) records the provider's served model list inside its test module, with its source and date, and "the dated snapshot with a schema bump is a follow-on row". The reason is the code: `ModelCurrency` forbids extra keys (`ecosystem/schema/provider_registry.py`, `extra="forbid"`), and the Anthropic block has `model_currency.command: null` (`ecosystem/provider-registry.yaml:180-194`), so no in-repo surface holds a served list a check can read. "Newest" is decidable only from the provider's own creation dates, never from version strings (`to-browser/DIGEST-READONLY-SWEEP-2026-10-09.md` RO-3.4). · Done when: the Anthropic `model_currency` block carries a dated served-list snapshot (each id with the provider's creation date, the source and the probe date); the schema version is bumped to admit it, RED-first; and the test that every role pin is the newest served id reads that snapshot instead of a module-local list · starts after: `b2w3-registry-repoint` merged · refs `ecosystem/provider-registry.yaml`, `ecosystem/schema/provider_registry.py`, `scripts/check_model_currency.py`, `LANE-1452-b2w3-registry-repoint.md` N6, [#1452] · kill-candidates: none -- [#1452] moves the pins and keeps the list in a test module only (S-34); no open row owns the snapshot or the schema bump · source: seat ruling S-34 P-L4-3, filed by the B2-W3 render on its rows branch
