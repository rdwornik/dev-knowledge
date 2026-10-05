# Codex Review — b2-dispatch-local-sole

**Date:** 2026-10-05
**Branch:** `worktree-b2-dispatch-local-sole`
**HEAD:** `5be9e596`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/1/0 <!-- reviewer's own scale P1/P2/P3 = 2/1/0; counted here as High/Medium/Low with P1 as High -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Consumer:** [#920] LANE-B2-W1-b2-dispatch-local-sole

## R59 proof of read (lane b2-dispatch-local-sole, 2026-10-05)

- **Contract:** `LANE-B2-W1-b2-dispatch-local-sole` (batch B2-W1, lane W1-4), Done-contract item 6.
- **Served model id, from the tool's own log:** `model: gpt-5.6-terra` (the `codex exec` run header,
  session `01a10b38-c81c-7272-a569-c141cfc15304`, provider openai, sandbox read-only, reasoning
  effort low). The reviewer's own last line said `GPT-5`; the run header is the record.
- **Content hash returned by the reviewer:** `scripts/gen_lane_contract.py`
  `sha256=10FF8659E9174E300246B54337B46B4778725B0D526F74FFED461A32BE802228`. The lane computed
  `Get-FileHash` on the same file at `5be9e596` before the run
  (`10ff8659e9174e300246b54337b46b4778725b0d526f74ffed461a32be802228`): equal, so the read was real.
- **Reviewed HEAD:** `5be9e596`.

## Disposition (added by the lane after the review, same day)

Both P1 findings are fixed in the commit that follows this record, each with a test; the P2 is fixed.

1. P1 `scripts/gen_lane_contract.py` -- the typed-in-full `launch_command` resolves only from the hub
   checkout, yet the contract told the operator to type it from the target repo root. Fixed: the
   contract now tells the operator to type `dispatch <file>` from the target repo root (the shim runs
   the hub's launcher without changing directory) and says the full line is the same act typed from
   the hub checkout; PLAYBOOK Ch8's ruling says the same. The emitted launch line is unchanged
   (`dispatch.py launch`, the Done-contract's own wording). Test
   `test_the_contract_tells_the_operator_to_type_the_shim_from_the_target_repo_root`.
2. P1 `scripts/gen_lane_contract.py` -- `transport.emit` writes a destination outside the transport
   plainly, so `--out-dir <scratch>` persisted a lint-invalid contract. Fixed: `_write_contract`
   lints whatever the destination, then calls `transport.emit`. Test
   `test_a_scratch_out_dir_does_not_bypass_the_lint`.
3. P2 `protocols/BUILD-LIST.md:68` -- still named the retired hook as code and as its WIRE target.
   Fixed: the row names `tests/test_dispatch_conformance.py` and records the hook's retirement.

---

## Focus

Contract: LANE-B2-W1-b2-dispatch-local-sole (local dispatch runs only through the hub's
`dispatch.py`). Attack, in order: transport.emit / `_write_contract` letting a refused contract reach
disk; behaviour change in `gen_lane_contract` for existing callers and frozen contracts; dangling
references to the retired hook and module; vacuous tests; must/shall/never added to protocols or
templates, or a PLAYBOOK contradiction.

---

## Findings
CONTENT-HASH scripts/gen_lane_contract.py sha256=10FF8659E9174E300246B54337B46B4778725B0D526F74FFED461A32BE802228
MODEL-ID GPT-5

## P1 scripts/gen_lane_contract.py:829 — emitted fallback cannot launch from the stated target repo root

**What:** `launch_command()` emits `uv run --locked python scripts/dispatch.py launch <contract>`, while the shim deliberately uses `--project $Hub` and the hub's absolute `scripts/dispatch.py`.
**Why:** From a consumer/target repo root, `scripts/dispatch.py` is absent (or is not the hub launcher), so the generated "manual fallback" fails before dispatching.
**Fix direction:** Emit a hub-addressed invocation equivalent to the shim, or stop presenting the relative command as runnable from the target repo root.

## P1 scripts/gen_lane_contract.py:1755 — `--out-dir` bypasses the transport lint

**What:** `_write_contract()` calls `transport.emit()`, but `emit()` writes plainly when the destination is outside `CLAUDE_PROMPTS_DIR`; `--out-dir C:\scratch` therefore persists a lint-invalid contract.
**Why:** A caller can write a contract missing the required R59 close-out proof to disk even though the transport lint would refuse that same content at the transport root.
**Fix direction:** Apply the lint unconditionally for lane-contract writes, before delegating destination-specific transport handling.

## P2 protocols/BUILD-LIST.md:68 — active registry still names retired hook/module

**What:** The dispatch row still lists `dispatch-conformance` as code at `stages: [manual]` and makes arming that hook its WIRE target.
**Why:** The hook and `scripts/dispatch_conformance.py` were deleted, so this is a dangling operational reference and an impossible gate target.
**Fix direction:** Repoint the row to the replacement seam witness or retire/update its WIRE target.

P3: none

TALLY P1:2 P2:1 P3:0
