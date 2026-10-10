# Close-out diff review -- b2w3-red-burn-down repair 1 (Copilot route, Codex limit-refused)

**Date:** 2026-10-10
**Branch:** `worktree-b2w3-red-burn-down`
**Reviewed tip:** `a7327ebe` (one commit on top of `a03c3020`: the predicate fix, its tests, the v4 re-stamp, doc-counts)
**Diff range:** `a03c3020..a7327ebe` over `scripts/ tests/ ecosystem/audit-consumer-baseline.json ecosystem/doc-counts.md` (`diff.patch` sha256 prefix `13f17e3ef624`)
**Mode:** close-out diff review of a repair (common rules 2 (e), S-38 (b), S-54 item 5)
**Tally:** 0/0/1/0 <!-- Critical/High/Medium/Low -->

Consumer: lane contract `LANE-1341-b2w3-red-burn-down.md` (batch B2-W3, lane 2) as repaired by `to-cc/AMEND-BATCH-B2-W3-REPAIR-2026-10-10.md` S-54 (`[#1341]`; contract Done-contract item 6 requires this record; amend sha256 prefix `03dc5c8eee46`).

## Route and proof of reading

- **First route, Codex `gpt-6-astra`, refused on a usage limit.** `codex exec -m gpt-6-astra -c model_reasoning_effort=high -s read-only` (codex-cli 0.155.0, session `01a126a0-d465-7c63-86bd-f5871695a8a3`, header `model: gpt-6-astra`) exited 1 at 2026-10-10T16:24Z with `You've hit your usage limit ... try again at 9:40 PM.` Not retried inside that window. No review output exists from it.
- **Second route (S-38 order 2), the Copilot CLI**, a different vendor from the producer (Anthropic): `copilot -p ... --model gpt-6.1-sol --add-dir <isolated folder> --allow-all-tools --no-ask-user -s --no-color --usage-output-file`.
  - **Served model id, from the tool's own usage file** (sha256 prefix `7c6894ed36f0`): `currentModel` `gpt-6.1-sol`, 1 request, `totalPremiumRequestCost` 1.
  - **Nonce returned:** `53ba316b0db8` (the value in the folder's `nonce.txt`).
  - **Input hashes returned and matching the files read:** `diff.patch` `13f17e3ef624`, `amend-s54.md` `03dc5c8eee46`.
- The folder held only `amend-s54.md`, `diff.patch`, `prompt.txt`, the two changed source files at the tip and `nonce.txt`.

## Findings

CRITICAL: (none)

HIGH: (none)

MEDIUM -- `scripts/consumer_at_landing.py:383` (`receipt_linked_identifiers`): the new verification grammar inherits the `-codex-` route's suffix-tolerant prefix match, so with only a merge receipt for `b2w3-red-burn-down`, `2026-10-10-verification-b2w3-red-burn-down-repair-1-review.md` binds to that lane although its extracted slug is `b2w3-red-burn-down-repair-1`. The reviewer's fix direction: exact equality for this grammar, prefix matching kept for `-codex-`. The added negative test uses a non-prefix unrelated slug and does not see this case.

LOW: (none)

TALLY CRITICAL:0 HIGH:0 MEDIUM:1 LOW:0

## Disposition

- No CRITICAL or HIGH finding, so nothing gates the handback (common rules 2 (e)).
- The MEDIUM is **not taken, by decision, and pinned by a test**:
  - S-54 item 2 says the audit "reaches the same merge-receipt route as a `-codex-` one", and that route's rule is the prefix rule (`2026-09-29-codex-lane-handoff-probes-5b5r-6b-repair-1.md` binds to the receipt slug `lane-handoff-probes`). The integrator writes one receipt per lane, never a per-repair slug.
  - Exact equality for this grammar alone would leave every repair's review record, including this one, undeclared on merge and would red the same three tests again.
  - The false-positive guard the finding worries about is kept: `rest` must equal the slug or continue with `-`, so a slug that merely appears inside a longer unrelated `rest` does not bind.
  - A test added after the review (test-only, no change to the reviewed production code) fixes both halves of that behaviour: `test_a_copilot_route_repair_record_binds_to_its_lanes_receipt_like_a_codex_one`.
