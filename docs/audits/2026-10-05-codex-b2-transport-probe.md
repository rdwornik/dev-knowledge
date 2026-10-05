# Codex Review — b2-transport-probe

**Date:** 2026-10-05
**Branch:** `worktree-b2-transport-probe`
**HEAD:** `1f0ca673`
**Diff range:** `origin/main..HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low, counted from the Findings section below: two HIGH. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
no-consumer: LANE-B2-W1-b2-transport-probe: the handoff_probes audit check reads BD-transport via this rule

---

## Focus

Contract LANE-B2-W1-b2-transport-probe (batch B2-W1, lane W1-11). Defect: BD-transport equality-matched a count so registry growth red the handoff probe. Check: (1) growth passes and a removed recorded kind fails, incl. removal-with-replacement when a cut sha is resolvable; (2) legacy count-only rows judged on count floor; (3) no other BOOT-DATA key verdict changes; (4) the git-show snapshot is only trusted when it re-hashes to the recorded digest; (5) any false PASS path. First line of your findings must echo this nonce verbatim: NONCE=d68b27729aad4610

---

## Findings
NONCE=d68b27729aad4610

## Critical

(none)

## High

## HIGH scripts/verify_handoff_probes.py:1497 — unavailable registry can pass

**What:** The exact-rendered-value fast path passes a Transport row even when `row_transport()` degraded because the registry is unreadable or absent.  
**Why:** A cut that recorded the same `unavailable ...` text will receive `BD-transport: pass`, contradicting the intended fail-closed unreadable-registry behavior.  
**Fix direction:** Reject degraded/unavailable live Transport rows before applying the exact-match shortcut.

## HIGH scripts/verify_handoff_probes.py:1499 — malformed Transport rows can pass the count fallback

**What:** `_TRANSPORT_VALUE_RE.match()` plus only an `endswith()` check accepts inserted content between the first delimiter and the evidence tail.  
**Why:** A value such as `106 kind(s) registered — forged text — evidence: ... [SLOW]` reaches the legacy count-floor path and can pass, despite being malformed/tampered.  
**Fix direction:** Parse the complete value with an anchored/full-match grammar that permits no intervening content.

## Medium

(none)

## Low

(none)

---

## Proof of read and disposition (appended by the producing lane, 2026-10-05)

- **Contract:** `to-cc/LANE-B2-W1-b2-transport-probe.md` (`LANE-B2-W1-b2-transport-probe`, batch B2-W1 lane W1-11); this record is its Done item 2's review. It cites the contract as its consumer (the `no-consumer:` line above names the contract).
- **Served model id, from the tool's own log:** the codex exec run header reads `model: gpt-5.6-terra` (codex-cli 0.155.0, session id `01a10a06-7502-74c1-8d1b-0f3f6e53bfae`, reasoning effort high); not the producer's vendor.
- **Nonce the reviewer returned:** `d68b27729aad4610` (first line of its findings, `NONCE=d68b27729aad4610`), equal to the nonce placed in the Focus above.
- **Reviewed range:** `origin/main..HEAD` at `1f0ca673` (after merging `origin/main` `0db61b7b`). An earlier attempt at a stale base failed with exit 1 and no output; its diff range had pulled in unrelated files (diagnosed: the lane had not yet synced after the W1-7 and W1-10 merges), so it is not a review.

### Dispositions (both HIGH fixed in `31231c8c`, each with a RED-first test)

1. **HIGH `scripts/verify_handoff_probes.py` — an unavailable registry can pass (exact-match shortcut).** FIXED: the shortcut is removed; a recorded `unavailable — …` reading no longer matches the value grammar and FAILs, even over an unreadable live registry. The one existing test that leaned on it (`test_a_well_formed_boot_data_block_passes_every_row`, whose stub repo had no registry) now writes a registry into its stub, a fixture addition, no assertion weakened. Test: `test_a_forged_or_degraded_transport_value_cannot_reach_the_count_floor`.
2. **HIGH `scripts/verify_handoff_probes.py` — a malformed row reaches the count floor (`match` plus `endswith`).** FIXED: the cell is parsed with `fullmatch` over the whole grammar; text between the count/digest and the evidence tail, or a non-hex digest, FAILs. Same test, plus `test_the_transport_value_grammar_names_the_registry_the_row_reads` pinning the grammar's literal to `handoff_state.TRANSPORT_REGISTRY_REL` and the live row to the grammar.

### Amendment, 2026-10-05 (later the same day): disposition 1 is reversed to DECLINED

Disposition 1 above said HIGH 1 was FIXED in `31231c8c`. Running the W1-6 refusal ids on that tip showed the fix refuses real cuts: the stub repos that `tests/test_onboarding_items.py`, `tests/test_seat_release_moment.py` and `tests/test_gen_handoff.py` cut bundles from carry no `ecosystem/transport-registry.yaml`, so the Transport row records the degraded `unavailable — …` reading, and failing that closed made `handoff_probes` a hard fail in the cut preflight (14 setup errors, plus `test_filled_waiver_refuses_a_malformed_seats_row` reporting BD-transport instead of BD-seats). Those tests belong to other lanes, and every state row has always recorded and re-derived a degrade the same way.

- **HIGH 1 — DECLINED, reason above.** The shortcut returns, narrowed: it passes only when the cut recorded the degraded reading AND the re-derivation is that same degraded reading now, and its detail says `degraded`, never a clean reading. A degraded value over a registry that is readable now FAILs. Pinned by `test_a_forged_or_degraded_transport_value_cannot_reach_the_count_floor`.
- **HIGH 2 — FIXED, unchanged:** the cell is parsed with `fullmatch`.
- The fixture addition to `test_a_well_formed_boot_data_block_passes_every_row` made under disposition 1 is reverted; that test is as on `origin/main`.
