# Codex Review — b2-transport-lint

**Date:** 2026-10-04
**Branch:** `worktree-b2-transport-lint`
**HEAD:** `40d4f813`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low, counted by hand from the Findings section: three HIGH headings (the script's heuristic printed 0/0/0/0 because terra's `###` finding shape is not the one it parses). -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Consumer:** [#978] LANE-B2-W1-b2-transport-lint

## R59 proof of read (lane b2-transport-lint, 2026-10-04)

- **Contract:** `LANE-B2-W1-b2-transport-lint` (batch B2-W1, lane W1-6), Done-contract item 6.
- **Served model id, from the tool's own log:** `model: gpt-5.6-terra` (the `codex exec` run
  header, session `01a106f0-1536-7b01-b210-573df2ce596a`, provider openai, sandbox read-only,
  effort high). The reviewer's own one-line self-report said `gpt-5`; the run header is the
  record.
- **Content hash returned by the reviewer:** `scripts/transport_lint.py`
  `sha256=feb177ab856d547947bca5f46455baf4e18bff7be6acc4c5c751f50f6300287b`. Recomputed by the
  lane with `Get-FileHash` before the run (`feb177ab856d547947bca5f46455baf4e18bff7be6acc4c5c751f50f6300287b`):
  equal, so the read was real.
- **Reviewed HEAD:** `40d4f813`.

## Disposition (added by the lane after the review, same day)

All three HIGH findings are P1 and are fixed in the commit that follows this record; each has a
test in `tests/test_transport_lint.py`.

1. `scripts/transport.py` case variants (`TO-BROWSER`) -- fixed: `_folder_of` and
   `is_transport_dest` compare case-insensitively; test
   `test_a_differently_cased_folder_name_is_still_the_transport`.
2. `emit()` treating any same-named directory as the transport -- fixed: with a configured (or
   passed) transport root, `is_transport_dest` requires the resolved parent to be that root or its
   immediate `to-cc/` / `to-browser/` child; test
   `test_a_scratch_directory_sharing_the_basename_is_not_the_transport`.
3. `scripts/transport_lint.py` R59 words accepted anywhere in a lane contract -- fixed: the words
   count only in the close-out item (first `Close-out` mention to the next heading); tests
   `test_r59_words_in_unrelated_prose_do_not_satisfy_the_close_out_gate` and
   `test_a_lane_contract_with_no_close_out_item_is_refused`.

---

## Focus

Contract: LANE-B2-W1-b2-transport-lint (a transport file that breaks the grammar is caught when written). Attack: scripts/transport_lint.py (lint_entry, sweep, carriage check), scripts/transport.py (_lint in write/append, emit, is_transport_dest), the call sites gen_ledger/propose_row_closures/transport_report, ecosystem/transport-registry.yaml class field and new kinds. Look for false negatives (a bad decision file passing), false positives that would block a legitimate writer, Windows path issues, and cycles in imports. R59 PROOF OF READ: begin your reply with exactly one line 'CONTENT-HASH scripts/transport_lint.py sha256=<hex>' where <hex> is the SHA-256 of that file as YOU read it from the working tree, then a line naming the model id that is serving you.

---

## Findings
CONTENT-HASH scripts/transport_lint.py sha256=feb177ab856d547947bca5f46455baf4e18bff7be6acc4c5c751f50f6300287b
MODEL-ID gpt-5

## CRITICAL

(none)

## HIGH

### scripts/transport.py:199 — Windows case variants can bypass the transport gate

**What:** `is_transport_dest()` and `_folder_of()` compare folder names case-sensitively; a Windows path ending in `TO-BROWSER` is treated as non-transport by `emit()`.
**Why:** Windows resolves that to the real `to-browser` directory, so a `--out` path with different casing bypasses registry, writer, and lint checks; direct `write()` instead falsely rejects it as `root`.
**Fix direction:** Determine the destination from normalized/resolved paths relative to the configured transport root, with case-insensitive folder classification.

### scripts/transport.py:199 — `emit()` treats arbitrary same-named directories as transport

**What:** Any output path whose immediate parent is named `to-browser` or `to-cc` is lint-gated, even when it is outside `CLAUDE_PROMPTS_DIR`.
**Why:** The documented arbitrary `--out` paths in `gen_ledger` and `propose_row_closures` can be wrongly refused merely because a scratch directory shares that basename.
**Fix direction:** Require the resolved destination parent to be an immediate child of the resolved configured transport root before routing through `write()`.

### scripts/transport_lint.py:126 — R59 validation accepts proof wording anywhere in a lane contract

**What:** The validator searches the entire file for “served model” and “nonce”/“content hash,” rather than the close-out requirement or an actual review record.
**Why:** A contract can mention those terms in unrelated prose while omitting the required close-out proof, silently passing the new gate.
**Fix direction:** Parse and validate the designated close-out/R59 section or a structured review-record field.

## MEDIUM

(none)

## LOW

(none)
## Amendment 2026-10-05 -- repair 2 of 2 (refusal `REFUSED-b2-transport-lint.md`)

Consumer: [#978] LANE-B2-W1-b2-transport-lint-repair-2. The integrator refused the lane at step 3(b):
`tests/test_transport_lint.py::test_the_lane_contract_template_still_names_the_proof_at_the_line_the_contract_cites`
sliced `lines[84:92]` of `templates/lane-contract-template.md` (the contract's `:88`, frozen at
`e67f27ac`); lane W1-1 then inserted 6 lines above, so the slice missed a property that still held
(night rule N5: a comparison against a frozen copy of a volatile fact).

**Change (tests only, this function and two negatives):** the test now finds the numbered
`## Done-contract` item that carries `R59 proof of read` and asserts `nonce or content hash` in the same
item; both phrases are still asserted. Negative tests: the item moved under `## Do not` fails; unrelated
flush-left prose adjacent to a numbered item fails. Synced from `origin/main` (merge `fcc7ccb0`), RED
reproduced there before the edit, GREEN after.

**One Codex terra read of the changed test** (commit `5b28f52c`):
- **Served model id, from the run header:** `model: gpt-5.6-terra` (codex-cli 0.155.0, provider openai,
  sandbox read-only, session `01a10ad2-dbe7-71e2-be7a-21fde30efb72`).
- **Nonce returned:** `REV-128E3BFF` (the reviewer's final line, matching the one set in the Focus).
- **Tally:** 0/1/0/0 (one P1).
- **P1 -- unrelated Done-contract prose could be treated as the R59 item** (the backward/forward scan
  accepted any nonblank line as a continuation). **Fixed, not declined:** a continuation line must be
  indented, flush-left prose ends the item, and a hit with no numbered-item start returns empty; test
  `test_the_template_proof_check_refuses_unrelated_prose_adjacent_to_a_numbered_item` (RED on the first
  helper, GREEN on the fix).
