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

## Review 2 — the repair of item 1 (REFUSED-b2-handoff-hardening.md, repair 1 of 2)

**Consumer:** `LANE-B2-W1-b2-handoff-hardening.md` (Done-contract item 1) and the integrator's refusal `to-browser/REFUSED-b2-handoff-hardening.md`, which asks for a reviewed repair diff, "served id plus nonce, P1s fixed".
**Diff range:** `af99d08c...HEAD` over `scripts/` and `tests/` (the repair only; `af99d08c` is the merge of origin/main `1ae12a29` into the lane). Final reviewed tip `1c8e97d5`.
**Model used:** `gpt-5.6-terra`, served — each run's own header read `model: gpt-5.6-terra` (OpenAI Codex, `codex exec -c model=gpt-5.6-terra --sandbox read-only`, isolated folder under the job tmp holding the diff, the two changed scripts, the contract, the refusal, the real plan heads and a `nonce.txt`).
**Nonce returned (final pass):** `NONCE-491e5d72ec4506d9`, the first line of the answer, equal to its `nonce.txt` (session `01a1088c-9c53-7592-9bfb-8777cdf0b70f`). Earlier passes each returned their own nonce (`NONCE-14df7829a316d322`, `…c6e0828e902c26e0`, `…5ff2d828ee5e5993`, `…e11e60a8409dc46b`, `…3a909bebad9f5532`, `…0d7296057e04c2a0`, `…4d99757e4f8adfa2`).
**Tally (final):** `VERDICT: PASS (P1=0 P2=0 P3=0)`.

Eight passes ran; the first seven each returned a FAIL with P1s that were real defects of the repaired row, each fixed RED-first before the next pass:

| pass | P1/P2 | disposition |
|---|---|---|
| 1 | `supersedes:` could name `../` or an absolute path; `as_of` did not bind lineage ancestors; refusal test did not cover a committed bundle (P2) | fixed `8a43a1de`; the committed-bundle test added as a regression guard |
| 2 | an undated lineage predecessor bypassed `as_of` | fixed `6b8e6911` |
| 3 | a symlinked predecessor escaped the plan directory | fixed `6a26c984` (the first draft of that test was vacuous: a bare companion refused on its own; rewritten so the symlink is the only variable) |
| 4 | an undated newer plan hid behind a dated master (the shared reader ranks a name with no date token first) | fixed `a4327fa6`: the row ranks by name date, else mtime date |
| 5 | a versioned `kind: PLAN v2 — … complements …` matched the master shape first | fixed `b15b2f67`: the companion declaration is tested first |
| 6 | a top-level `PLAN-*.md` symlink resolving out of `to-cc`; `supersedes: X.md/ignored` accepted | fixed `70228c11` |
| 7 | an undated plan bypassed `as_of` | fixed `1c8e97d5`: an undated plan is bound by its mtime date |
| 8 (final) | none | PASS |

The first reviewed tip after the refusal repair itself (`d7444f89`) had no unreviewed code beyond what the table lists; `HANDOFF_BOOT.md` is unchanged by the repair (17,924 B, sha8 `3b097159`).
