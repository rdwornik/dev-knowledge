---
id: "[#364]"
title: "`doc_rot`'s length cap blocks [#353] from doing its job"
status: open
priority: P3
size: S
theme: "[E8] ARC-5 execution"
story: "[S22] Discharge the silent-rule census findings"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#364] [P3][S] **`doc_rot`'s length cap blocks [#353] from doing its job** — [#353] exists to accumulate "n=N recovered-not-prevented" incident evidence, and at 1189 chars it has ~11 left under the 1200 cap. The 2026-07-19 entry (n=7) already had to be compressed to a pointer. **At the current rate it hits the cap within about two more incidents**, after which the mechanism forces either an uninformative evidence line or a disposition on a ticket that is working correctly — a gate degrading the record it is meant to protect. Options to record, **no ruling attached**: (a) a linked evidence file (e.g. an `incident-evidence`-class audit artifact, already in the ADR-101 enum) with the ticket carrying only a pointer; or (b) a cap exemption for evidence-accumulating tickets, declared per-ticket so it cannot become a blanket escape. · Done when: [#353] can accrue further incidents without tripping `doc_rot`, or the constraint is recorded as accepted-with-reason · refs #353, scripts/validate_doc_rot.py, ADR-101 audit-class enum · kill-candidates: none — a mechanism-blocks-ticket defect; #353 is the victim, not the owner · serialize-group: audit-py
