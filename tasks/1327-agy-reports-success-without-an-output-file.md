---
id: "[#1327]"
title: "`agy` reports SUCCESS without an output file"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1327] [P2][S] **`agy` reports SUCCESS without an output file** - R34.4 (`to-browser/RATIFICATION-2026-09-29.md`, v4-superseded snapshot: "A backlog row: `agy` reports SUCCESS without an output file — a defect; its fix checks the output file's existence and size"). Evidence: `to-browser/PROPOSAL-ADR-AJ-M06-2026-09-29.md`, v1-superseded snapshot, ROWS-OWED — "the registry's reader (agy) is not a verbatim reader. It reported `"status":"SUCCESS"` on a 20-minute print timeout with no output file (L04), and its one-pass ebook summary put paraphrase in quotation marks on 4 of 6 pages checked". · Done when: RED-first, a fixture reproducing a SUCCESS status with a missing or empty output file is rejected; a read-role result is accepted only if its output file exists with size > 0 and the log has no "print timeout" line · **Likely already discharged, not yet verified or closed by this lane (Owns restricts this lane to filing, not closing, `[#1327]`):** `scripts/read_gate.py` (merged into this tree at `9fadaf12`, lane-read-gate/N5-11, before this lane's render) states its own closed defect verbatim as "`agy` reported SUCCESS on a 20-minute print timeout with no output file" and `tests/test_read_gate.py::test_a_success_with_no_output_file_is_rejected_and_falls_through` plus `::test_verify_read_rejects_a_missing_output_file` / `::test_verify_read_rejects_an_empty_output_file` / `::test_verify_read_rejects_a_log_carrying_a_print_timeout` appear to be exactly this row's RED-first witnesses. The next seat should confirm the match and close with that evidence rather than re-building · refs `scripts/read_gate.py`, `tests/test_read_gate.py`, `ecosystem/provider-registry.yaml` (`roles.read`), `logs/READ-OUTCOMES.jsonl` · kill-candidates: none -- no open row tracked this defect before this entry
