### 2026-10-25 (o) - CC (Sonnet 5.5, INTEGRATOR-E2.1 cycle 1, batch E2.1): lane l12-acceptance (`[#1640]`, H-Q1..H-Q6) -- the R6 handoff design lands: `handoff_intake.py` and `gen_handoff.py --intake --plan`, boot v3 (instructions only, facts in BOOT-DATA), `role_pin_current`, the labelled `Diagram` row, KPI by code, the `owed:` decision-id lint

**Anchors:** `5ae14a9f8` (the lane tip: silent-rule pool drained), `7c159b71d` (the R6 acceptance delta H-Q1..H-Q6 on L12), `6692b4d3c` (37 RED tests frozen first)

**Did:** merged `origin/worktree-l12-acceptance` @ `5ae14a9f8` onto main `188ac7070` (6 lane commits, base `c8fd7e08c`, clean; 13 files: `scripts/handoff_intake.py` new, `scripts/gen_handoff.py`, `scripts/transport_lint.py`, `scripts/verify_handoff_probes.py`, `protocols/HANDOFF_BOOT.md`, `templates/handoff/v5/HANDOFF_BOOT.md.tmpl`, `ecosystem/harness.yaml` and six test files). The lane's two items it could not do are done here: the neighbouring-file sweep over the handoff tests and the branch CI verdict (see the integrator receipt). Regenerated `ecosystem/doc-counts.md`.

**Result:** recorded in the integrator receipt (tests, sweep, ship-gate diff, the landing's CI). The R6 rulings it implements are `RATIFICATION-2026-10-24.md` H-Q1..H-Q7; the 2026-10-31 cut is the first under the ruled design. The lane's recorded-not-fixed items stay with the architect: wiring `narrative_findings` and `role_pin_current` into a post-render check, comparing `DIAGRAM.md` in the Diagram rule, tightening `owed:` to ids only.

**Changes:** `scripts/handoff_intake.py`, `scripts/gen_handoff.py`, `scripts/transport_lint.py`, `scripts/verify_handoff_probes.py`, `protocols/HANDOFF_BOOT.md`, `templates/handoff/v5/HANDOFF_BOOT.md.tmpl`, `ecosystem/harness.yaml`, `tests/`, `ecosystem/doc-counts.md`, `JOURNAL.md`.

**Next:** template-wake-fix, then cloud-remove-tail; P2 known-reds-extend and ci-one-verdict-2 stay held on the operator's S4 ruling.

