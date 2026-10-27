### 2026-10-25 (s) - CC (Sonnet 5.5, INTEGRATOR-E2.1 cycle 1, batch E2.1): `[#1697]` closes as SUPERSEDED by the operator's CL-1 ruling, and the cloud-remove-tail-3 chain is on main (`5a369f6d4`, receipt `9d00fdf99`)

**Anchors:** `076e27729` (the closure commit: `gen_task_tree.py --close-row 1697`), `5a369f6d4` (the merge whose content satisfies the row: the cloud entry leaves `ecosystem/substrate-registry.yaml`, `RETIRED_SUBSTRATES` refuses a cloud declaration dated 2026-10-24 or later), `9c43c6d9a` (the lane tip), `10146ad20` (remove the cloud build substrate)

**Did:** the orchestrator ruled the closure (DECIDED-BY-ORCHESTRATOR: close `[#1697]` as superseded by `RATIFICATION-2026-10-24.md` AMENDMENT (b), row CL-1, which names `[#1697]` and replaces the row's "correct the entry to read-only" with removal; not recorded as Done-when-met). Closed it with `gen_task_tree.py --close-row 1697 --evidence 5a369f6d4b14b0975a1a81863634d6a0c7c84c41` naming `tests/test_validate_substrate.py::test_cl1_registry_removes_cloud_and_keeps_other_substrates` and `::test_cloud_date_on_or_after_retirement_is_still_refused`, appended "superseded by RATIFICATION-2026-10-24 (b) CL-1 (cloud substrate removed, not corrected); landed 5a369f6d4" to the row, regenerated `BACKLOG.md`. Landed with `land_lane.py --operator-act CL-1 --ratification RATIFICATION-2026-10-24.md` (a bookkeeping change; no model call).

**Result:** `[#1595]` and `[#1634]`, also named in CL-1, stay open: `[#1595]` asks for a test over `ecosystem/provisioning.yaml` that every listed substrate has a launcher or is absent, which the chain did not add, and `[#1634]` needs the operator's shim install and per-entry deletion GO.

**Changes:** `tasks/1697-*.md`, `tasks/manifest.json`, `BACKLOG.md`, `ecosystem/doc-counts.md`, `logs/MERGE-RECEIPTS.jsonl`, `JOURNAL.md`.

**Next:** the S4 ruling lanes and `routine-uv-pin-tail` once their rulings are recorded; the PLAYBOOK cloud-verb follow-up.

