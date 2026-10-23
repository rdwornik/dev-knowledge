# Codex pre-merge reviews — lane connector-land (`worktree-connector-land`, batch E2.1)

- **Consumer:** [#1625] [#1626] [#1639] (the rows this lane advances) and the frozen contract `LANE-connector-land.md`; read by the E2.1 integrator at merge.
- **Date:** 2026-10-23
- **Diff reviewed:** `git diff origin/main...HEAD` at `fb473c290` (diff sha256 prefix `721d63d9eca5`); the fixes the reviews caused are `652fbb691` and `83c883453`.

## Review 1 — Codex `gpt-5.6-terra` (R138)

- Served model, from the banner: `model: gpt-5.6-terra` (read-only). Nonce returned: `721d63d9eca5`, equal to the sha256 prefix of the diff file.
- P2 `scripts/gen_process_diagrams.py:480`: `rebind()` takes the nearest duplicate when the recorded line matches no occurrence of an ambiguous anchor. Disposition: RECORDED, not fixed — the nearest-match rule is what the frozen RED test `test_rebind_uses_nearest_match_when_anchor_is_ambiguous` pins; an ambiguous anchor is also reported by `--check`.
- P2 `scripts/gen_process_diagrams.py:463`: the text rewrite recognises only unquoted, comment-free `file_line` scalars. Disposition: RECORDED — `rebind` aborts loudly on a count mismatch rather than writing a wrong line; the file is generated-shape.
- P3 `scripts/gen_process_diagrams.py:501`: a bare `@cli.command()` is not an entry point. Disposition: RECORDED (deferred) — every `dispatch.py` command names itself today; the isolated verify raised the same gap.

## Review 2 — Codex `gpt-6-sol`, adversarial (R172)

- Served model, from the banner: `model: gpt-6-sol`. Nonce returned: `721D63D9ECA5` (same prefix, upper case).
- P1 `scripts/gen_process_diagrams.py:545`: the gate passed with a stale or missing anchor. Disposition: FIXED in `652fbb691` (`gate_main` also prints and fails on `anchor_problems`).
- P1 `scripts/gen_process_diagrams.py:490`: a missing `scripts/dispatch.py` emptied the entry-point set and the gate passed. Disposition: FIXED in `652fbb691`. Witness: `tests/test_process_gate_inputs.py` (5 tests, 4 fail on the pre-fix generator).
- P2 `:445`: a unique anchor that moved is accepted by `--check` until `--rebind` runs. Disposition: RECORDED — line numbers are derived output (contract item 2); the anchor is the binding.
- P2 `:537`: any anchor inside a command's span counts as coverage of that entry point. Disposition: RECORDED — the gate checks that a binding exists, not that it is meaningful; W9 reads the list.
