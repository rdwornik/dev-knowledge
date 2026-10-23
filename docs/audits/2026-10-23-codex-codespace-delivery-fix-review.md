# Codex pre-merge reviews — lane codespace-delivery-fix (`worktree-codespace-delivery-fix`, batch E2.1)

- **Consumer:** [#1662] [#1657] [#1658] (the rows this lane closes) and the frozen contract `LANE-codespace-delivery-fix.md`; read by the E2.1 integrator at merge.
- **Date:** 2026-10-23
- **Diff reviewed:** `git diff origin/main...HEAD` at `99a19959c` (review 2 ran at `62c677593`+`cc281131c`+`53b8dac16`; the one fix it caused is `e43b5ad39`).

## Review 1 — Codex `gpt-5.6-terra` (R138)

- Served model, from the banner: `model: gpt-5.6-terra` (codex-cli 0.155.0, read-only). Nonce returned: `50620b5ba1`.
- P1 `scripts/codespace_state.py:277,366` and P1 `scripts/codespace_parity.py:2254`: other ssh helpers still pass several argv elements. Disposition: RECORDED, not fixed — outside the contract's file set, fixed paths without spaces.
- P2 `scripts/dispatch.py` (delete): the close row is written only when both `batch` and `lane` are given. Disposition: pre-existing behaviour; the CLI always passes both. Recorded.

## Review 2 — Codex `gpt-6-sol`, adversarial (R172)

- Served model, from the banner: `model: gpt-6-sol`. The reviewer's own `MODEL:` line read `gpt-6-astra`; the banner is the served field. Nonce returned: `393bc2a15d`.
- P1 failed SESSION read silently skipped (`dispatch.py` harvest). Disposition: FIXED in `e43b5ad39`, with `test_harvest_refuses_when_the_requested_session_file_cannot_be_read`.
- P1 SESSION delivery optional when `checkout_dir`/`transport_dir` are absent. Disposition: by design — `codespace_handback` gates the delete on `deliver_to_transport`; recorded.
- P1 the transport registry gains a `root` folder for the SESSION kind. Disposition: DECIDED — the operator names the directory; the writer and content lint still apply.
- P2 `codespace_state.py:366` progress probe: as review 1, recorded.
