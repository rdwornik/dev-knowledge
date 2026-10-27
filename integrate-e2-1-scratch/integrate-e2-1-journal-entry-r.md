### 2026-10-25 (p) - CC (Sonnet 5.5, INTEGRATOR-E2.1 cycle 1, batch E2.1): l12-acceptance is on main (`8b744ede4`, receipt `633452dae`), and lane template-wake-fix (P6, `[#1727]`) lands: the dispatcher template now says a queue FIRE leaves `LAUNCH-<SLUG>.json` and carries the `queue --watch` / Monitor / 10-minute cron / re-arm-on-BIND wake section

**Anchors:** `d686c8636` (the lane tip: the receipt sentence kept at its original two lines so the S15 process-binding anchor holds), `f67d1333d` (the template says a queue FIRE leaves the launch receipt and adds the wake section), `a497e24fb` (RED tests), `dd359b7f4` (the claiming row `[#1727]`)

**Did:** (1) l12-acceptance landed on the second `land_lane.py` attempt: attempt 1 (merge `3a2031a8c`, run 40146547036) judged one new red, `test_cli_flags_and_refusal_exit_code_are_unchanged`, caused by the lane (it added `--intake` and `--plan` to `gen_handoff.py` and left the full-flag-set pin at the old set); the one-line integrator repair `848226a68` (test only) cleared it, and attempt 2 landed in 1070 s. The spine stayed anchored with no hand-written anchor entry (the `[#1721]` property, second real use). (2) Merged `origin/worktree-template-wake-fix` @ `d686c8636` onto main `633452dae` (6 lane commits; `templates/dispatcher-order-template.md`, `tests/test_dispatcher_order_adopts_queue.py`, row `[#1727]`). `BACKLOG.md` and `tasks/manifest.json` conflicted as generated files: took main's, registered the `[#1727]` node after `[#1721]`, regenerated with `gen_task_tree.py --emit-source`; regenerated `ecosystem/doc-counts.md` (the lane's own handback names that regeneration as the integrator's).

**Result:** `[#1727]` stays OPEN: its Done-when 3 (branch CI explained) is judged by the landing CI, and the launcher bullet at `templates/dispatcher-order-template.md:61` still names per-lane HOLD lines under `--watch` (the lane's owed line, decision id H1-X follow-up).

**Changes:** `templates/dispatcher-order-template.md`, `tests/test_dispatcher_order_adopts_queue.py`, `tasks/1727-*.md`, `tasks/manifest.json`, `BACKLOG.md`, `ecosystem/doc-counts.md`, `logs/MERGE-RECEIPTS.jsonl`, `JOURNAL.md`.

**Next:** cloud-remove-tail-2 (supersedes cloud-remove-tail), routine-uv-pin-tail, then the held P2 / ci-one-verdict-2 on the operator's S4 ruling.

