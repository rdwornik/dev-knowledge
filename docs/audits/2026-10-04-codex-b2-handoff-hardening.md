# Codex Review — b2-handoff-hardening

**Date:** 2026-10-04
**Branch:** `worktree-b2-handoff-hardening`
**Diff range:** `origin/main...HEAD` (doc-counts excluded as generated). Reviewed at `10565b84`; base `e67f27ac`, the sha this lane started from.
**Mode:** diff-review, isolated read-only session — a folder under the job tmp holding the diff, the changed files, the contract and a `nonce.txt` (not the lane)
**Consumer:** `LANE-B2-W1-b2-handoff-hardening.md` (Done-contract item 9, "the Codex review record … citing the contract, P1s fixed"); the integrator's merge verdict for batch B2-W1 reads it.
no-consumer: a lane's frozen contract is the only consumer this record has, and it is a transport file, not a governance surface (`[#id]` row, ADR, `STANDING_RULINGS`, intake) that `consumer_at_landing` recognises

**Model used:** `gpt-5.6-terra`, served — read from the run's own header: `OpenAI Codex v0.155.0`, `model: gpt-5.6-terra`, `provider: openai`, reasoning effort high (session `01a1076d-089e-7600-81d2-ed3d52988d91`). Codex route, so no substitution.
**Nonce returned:** `NONCE-e8b49cb3da21454b` — the first line of the reviewer's answer, equal to the `nonce.txt` it was given.
**Review profile:** code
**Tally:** P1=0 P2=1 P3=0, verdict `PASS (P1=0 P2=1 P3=0)`, reported as given. The P2 is fixed (below). The tip after the fix, `a23eaaf3`, was **not** reviewed a second time.

## Review 1 (tip `10565b84`)

The reviewer was asked to check Done-contract items 1–8 and callers of the old `row_rulings(transport, as_of=...)` signature, the old ROLE PIN refusal text and the PASTE_THIS section count, and whether any test is vacuous.

| P | Finding | Disposition |
|---|---|---|
| P1 | (none) | — |
| P2 | `scripts/assemble_paste.py:10` — the module docstring (and the comment near line 265) still says the role is resident in the Project instructions, contradicting the one install mode in OPERATOR-INTERFACE §5/§6 (the Project's knowledge file plus a one-line pointer) | **Fixed, `a23eaaf3`.** The docstring, the comment and the install echo now say the Project's knowledge file |
| P3 | (none) | — |

## What shipped, in one line

The boot test's defects, each RED-first: a generated `Plan` row (newest master plan by its own head, with a `BOOT_DATA_RULES` rule); a `boot_version` plus a body-hash pair that fails on a content change with the version kept; the whole first move once in core item 3; a `Rulings` row printing the ids in force and a computed `not landed:` set; one install mode in OPERATOR-INTERFACE §5/§6 and the ROLE PIN refusal; no probe table folded into an architect paste (the bundle still holds `PROBES.md` for CC's gate); the author of each fill-in stated with its home quoted; and a warm boot-test fixture.
