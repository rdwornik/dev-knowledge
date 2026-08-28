---
id: "[#612]"
title: "Doc-rot row-body archival mechanism"
status: open
priority: P2
size: M
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#612] [P2][M] **Doc-rot row-body archival mechanism** (packet-born 2026-08-28 under register ruling Z-G1 -- a ruled packet row is past triage; funded by the window's banked ledger) -- row annotation is unbounded debt trimming cannot clear: a row accretes decision history because that history has nowhere else to go, so the ceiling is hit again a few sessions after each condense pass. Measured surface, live 2026-08-28: `validate_doc_rot.py` reports **77 findings** -- 68 `backlog-row-length` over the 1320-char ceiling, **8 `backlog-accretion` loci**, 1 grooming-cadence lapse. Ruling G5 records the class as **ownerless**; this row is its carrier. The mechanism is archival, not trimming: a durable per-row record takes the narrative load and the row keeps a pointer, on the existing "row carries a pointer, the record carries the record" doctrine (PLAYBOOK Ch6) -- so condensing stops being the only remedy. No row is deleted and no history lost. · Done when: an archival destination and its write path are ruled and built; a re-run of `validate_doc_rot.py` shows `backlog-row-length` strictly reduced with **no content destroyed** (byte-identical relocation, ADR-29 precedent); the mechanism is documented at the doc-rot doctrine home · refs JOURNAL.md 2026-08-28 (c), #532, #577
