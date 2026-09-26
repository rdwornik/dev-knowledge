# Codex Review — lane-adr-drafts

**Date:** 2026-09-25
**Branch:** `worktree-lane-adr-drafts`
**Reviewed commit:** `6731556c` (base `da11291b`)
**Codex version:** codex-cli 0.155.0 · session `01a0d96b-6c99-7ef2-8daf-91d62949acac`
**Mode:** documentation review (`codex exec`, prompt on stdin)
**Tally:** 0/2/1/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; reported by the codex header)
**Review profile:** docs — decision-matrix arithmetic, source fidelity, ADR-108 §A governance, contract completeness

**Consumer:** the lane contract `LANE-5B2-11-adr-drafts.md` (batch WAVE5B-N2 row 11), Done-contract item 4, which
requires this review record; the ADRs it reviews are `docs/decisions/ADR-123` … `ADR-126`.

---

## Focus

Four Proposed ADRs (distribution, code standard, prose → data, substrate and parallelism), their index rows in
`docs/decisions/README.md`, and the re-measured baselines in `tests/test_validate_adr_status.py`. Codex was asked
to recompute every matrix total and sensitivity claim, check numbers against the cited in-repo sources, check that
no functional question is decided in place of the operator, and check contract completeness.

## Findings and disposition

1. **[HIGH] ADR-123 Context 1 — carrier count omitted `carrier_docs`.** `deploy/tool.py::make_carriers()`
   (`:428-449`) registers six carriers; the ADR (following C1) described five. **FIXED** in the follow-up commit:
   six carriers named, the Ch4 *channel* count distinguished from the carrier count, C1's omission recorded.
2. **[HIGH] ADR-125 — the generic removal path would reach LESSONS.md, contradicting ADR-29.** ADR-29 (amend.
   2026-07-17) lets entries leave the active file only by byte-identical relocation to dated
   `LESSONS-legacy-<span>.md` files with a boundary pointer. **FIXED:** D2 now excludes LESSONS (relocation only,
   never removal) and, by the same reasoning, JOURNAL (append-only per `CLAUDE.md` §5 rule 2 and the carrier of
   ADR-85's anchor — freezing is in scope, removal needs its own decision amending ADR-85); the inventory row,
   migration steps 3-4 and Consequences follow.
3. **[MEDIUM] ADR-123 — the O9-versus-O6 sensitivity sentence omitted K4 (+15 to O9) and K6 (+10 to O6).** The
   total (+30) was right; the attribution was not. **FIXED:** all six differing cells named.

No Critical or Low findings. Codex raised no finding on any matrix total, on the governance checks (status,
required sections, functional questions routed to `## Operator decision options`) or on contract completeness;
that is an absence of findings, not a positive attestation.
