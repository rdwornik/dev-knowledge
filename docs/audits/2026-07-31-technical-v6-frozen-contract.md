# [#446] §B(b) — frozen contract for R1..R7 (RED-first freeze record)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-31 · **Slug:** v6-frozen-contract
- **Serves:** the G-TDD freeze that precedes any [#446] build code — the pytest set, the
  rerunnable prose witnesses, and the observed RED table proving every item fails before
  the build starts.
- **Inputs:** rulings `docs/audits/2026-07-31-technical-v6-open-rulings.md` (R1..R7, the
  authority) · spec `docs/audits/2026-07-30-technical-v6-spec-sol-draft.md` ("OPEN
  questions" items 1-7, the questions closed) · intake
  `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md` (R2's pinned definitions).
- **Status:** FROZEN, awaiting architect review. No build code exists.

## FR numbering

**FR<n> == R<n>** of the rulings artifact. There is no pre-existing FR1..FR7 register for
this work — the fleet's other `FR-<n>` series belongs to intake #14 / #328 and is unrelated.
The frozen module `tests/test_v6_frozen_contract.py` IS the register.

## Frozen pytest set — observed RED table

Run verbatim:

```
python -m pytest tests/test_v6_frozen_contract.py -p no:cacheprovider --tb=line -q
```

Observed at freeze: **9 failed, 0 passed** (3.57s). Every item fails for the mechanism's
absence, not a fixture defect — the failing assertion is quoted per row.

| FR | ruling | test | observed failure at freeze |
|---|---|---|---|
| FR1 | R1 | `test_fr1_handoff_verify_is_a_separate_command` | `R1 unbuilt: .claude/commands/handoff-verify.md absent` |
| FR2 | R2 | `test_fr2_p0_standing_topic_legs_are_emitted` | `R2 unbuilt: standing-topic legs absent from generated PROBES.md: ['P0a', 'P0b', 'P0c']` |
| FR3 | R3 | `test_fr3_p3_compares_live_branch_to_the_destination_row` | `R3/A4 unbuilt: boot header carries no Destination row (P3's second operand)` |
| FR4a | R4 | `test_fr4a_boot_byte_budget_is_mechanically_enforced` | `R4 unbuilt: assemble_paste exposes no HANDOFF_BOOT_BYTE_BUDGET` |
| FR4b | R4 | `test_fr4b_ruled_budget_is_pinned` | `R4 numeric budget UNRULED (ruling text says <number>) - architect-blocked; A10 cannot close` |
| FR5 | R5 | `test_fr5_generation_refuses_a_bundle_dir_holding_tracked_files` | `DID NOT RAISE <class 'Exception'>` — generation silently reused a bundle dir holding a git-tracked file |
| FR6 | R6 | `test_fr6_repo_root_and_cross_repo_are_codified_and_cli_mapped` | ``R6 unbuilt: `--cross-repo` without `--repo-root` returned 0; must be a HARD ERROR`` |
| FR7 v1 | R7 | `test_fr7_v1_file_re_binds_repo_root_dotfiles` | `assert ['pre-commit-config.yaml'] == ['.pre-commit-config.yaml']` — leading dot lost |
| FR7 v2 | R7 | `test_fr7_v2_header_tokens_ignores_a_bare_id` | `assert ['#421'] == []` — a backticked ticket id mis-tokenizes as a header anchor |

**Two halves are pre-satisfied INSIDE otherwise-RED tests** (R6 codifies existing semantics,
so they must not be rewritten to fail): `verify(bundle_path, repo_root=None,
cross_repo=False)` and the `:444` default call `results = verify(bundle)`. Both are asserted
in FR6, which is RED on its CLI half. No test is green at freeze.

**Suite colour:** the freeze deliberately reds the repo suite. Collection is unaffected, and
`validate_doc_claims` claim 3 uses `pytest --collect-only` (skipped in gate mode), so no
commit gate is blocked. A green-suite freeze is available on request as a one-line-per-test
`@pytest.mark.xfail(strict=True)` conversion, which flips to XPASS-fails the moment the build
lands; not applied, because the freeze instruction is an explicit RED table.

## Prose witnesses (R1..R6) — rerunnable verbatim

Run from the repo root under git-bash. Each block's observed output at freeze follows it.

### W1 — R1 (`/handoff-verify` separate; `/handoff` unflagged; `/boot` archived)

```
ls .claude/commands/handoff-verify.md            # RED: No such file or directory (rc=2)
grep -n -- "--verify" .claude/commands/handoff.md # pre-satisfied: no match (rc=1)
ls .claude/commands/boot.md                      # pre-satisfied: absent (rc=2)
```

Live inventory at freeze: `changelog-review.md`, `handoff.md`, `override.md`, `save.md`.

### W2 — R2 (P0a/P0b/P0c legs + P0a's currency assertion)

```
grep -cE '\| P0[abc] \|' templates/handoff/v5/PROBES.md.tmpl   # RED: 0 (rc=1)
grep -n "gen_task_tree" templates/handoff/v5/PROBES.md.tmpl    # RED: no match (rc=1)
```

### W3 — R3 (Destination row is P3's second operand)

```
grep -n "Destination" templates/handoff/v5/HANDOFF_BOOT.md.tmpl        # RED: no match (rc=1)
grep -E '^\| P3 \|' templates/handoff/v5/PROBES.md.tmpl | grep -c "Destination"  # RED: 0 (rc=1)
```

The existing P3 already runs `git branch --show-current` (as one of four git-state legs);
what is absent is the comparison target. R3 is a narrowing plus a second operand, not a new
command.

### W4 — R4 (byte budget in the assembler's existing size machinery)

```
grep -n "HANDOFF_BOOT_BYTE_BUDGET" scripts/assemble_paste.py   # RED: no match (rc=1)
wc -c protocols/HANDOFF_BOOT.md                                # 16156 bytes at freeze
```

Precedent for the home: `scripts/assemble_paste.py:32 _SIZE_WARN_BYTES = 65_000` with the
warn at `:189`. Sol draft §5 keeps the action a WARNING, not a blocking gate.

### W5 — R5 (RM-8 refusal at the creation site)

```
grep -n "exist_ok=True" scripts/gen_handoff.py       # RED: :436 still present (rc=0)
grep -n -- "allow_suffix" scripts/gen_handoff.py     # RED: no escape hatch (rc=1)
```

### W6 — R6 (CLI mapping; signature codification pre-satisfied)

```
grep -n -- "--repo-root\|--cross-repo" scripts/verify_handoff_probes.py           # RED: no match (rc=1)
grep -n "^def verify(bundle_path, repo_root=None, cross_repo=False)" scripts/verify_handoff_probes.py  # :409 (rc=0)
grep -n "results = verify(bundle)" scripts/verify_handoff_probes.py               # :444 (rc=0)
```

R7 has no prose witness by design: both variants are tokenizer behaviour, and behaviour is
witnessed by the two pytest cases above, not by a grep.

## Architect-blocked before build

1. **R4's number is a placeholder.** The ruling text reads `<number> bytes`, and the sol
   draft's OPEN question 4 states A10 cannot close on a placeholder. `_R4_RULED_BUDGET` in the
   frozen module is the single pin site and is `None`; FR4b is the mechanical record of the
   gap. Live boot is 16156 bytes — the number is not invented here.
2. **R7 fallback C is not exercised.** Option B (both variants inside [#446]) is frozen. If
   terra review rules v1 outside [#446]'s file scope, the new owning row must exist BEFORE
   [#421] closes — the [#447] closure-polarity lesson, applied forward.

## Anchor re-verification at freeze

Every locator cited by the rulings was re-read live on this branch; none drifted.

| ruling | locator | live at freeze |
|---|---|---|
| R2 | `docs/intake/2026-07-27-tech-handoff-process-v6-proposal.md:110-112` | the P0a/P0b/P0c mechanism rows (terra-H3 narrowing at `:113`) |
| R5 | `scripts/gen_handoff.py:436` | `bundle_dir.mkdir(parents=True, exist_ok=True)` |
| R5 | `_select_active_bundle` | present, `scripts/audit.py:1575` |
| R6 | `scripts/verify_handoff_probes.py:409` | `def verify(bundle_path, repo_root=None, cross_repo=False)` |
| R6 | `scripts/verify_handoff_probes.py:444` | `results = verify(bundle)` |
| R7 v1 | `scripts/verify_handoff_probes.py:54` | `_FILE_RE` |
| R7 v2 | `scripts/verify_handoff_probes.py:131-133` | `header_tokens` |
| R4 | `protocols/HANDOFF_BOOT.md` | present, 16156 bytes |
| R1 | `.claude/commands/` | 4 commands, no `boot.md`, no `handoff-verify.md` |
