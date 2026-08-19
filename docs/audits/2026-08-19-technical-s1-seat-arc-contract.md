# SEAT ARC S-1 (2026-08-19) — NIGHT ADJUDICATION EXECUTION

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**Primary checkout, `main`, sole writer alongside worktree lanes (they never touch your
surfaces; you never touch theirs — no scripts/, no tests/).** Write-scope: docs/audits/,
protocols/STANDING_RULINGS.md, .methodology.yaml, tasks/ via gen_task_tree --emit-source,
JOURNAL, LESSONS. Serialize your commits normally; hooks run.
**ADR-110:** commit this contract first as
`docs/audits/2026-08-19-technical-s1-seat-arc-contract.md`.
Source of truth for every act: `MORNING-REPORT-2026-08-19.md`'s pointers into the merged packs
— re-read the pointed section before each act; the report is a digest, the artifact governs.

## ACTS (in order; COMMIT per act or logical pair)
1. **N4 landing (architect ruling b′):** from `origin/claude/n4-grooming-wave1-audit-ahltfa`
   tip, land ONLY the `docs/audits/2026-08-19-technical-n4-grooming-wave1.md` final file state
   (`git checkout <tip> -- <path>`), commit under YOUR authorship with a JOURNAL anchor; the
   lane's own journal entries are discarded (single-night-entry doctrine). Verify the landed
   file byte-equals the branch tip's version. Keep the branch. Regen audits index.
2. **Two rules into `protocols/STANDING_RULINGS.md`** (operator-ratified at GO):
   (a) *A lane never writes JOURNAL.md; the integrator's single entry anchors a batch/night.*
   (b) *Anti-orphan ratification rule:* every intake flipped to ACCEPTED carries ≥1 carrier row
   or `disposition: deferred` with a live, DATED trigger — never ACCEPTED-with-zero-carrier.
   Quote each rule's provenance (this window's rulings + reviewer approval).
3. **D8 = Route 2 (operator GO):** declare `.devcontainer` in this repo's `.methodology.yaml`
   with a short `review_date` (pick +30d, record why). Verify `fleet_parity` WARN clears; run
   `audit.py health`.
4. **Ledger re-derivation + births:** re-derive the arithmetic from N3 pack §1.3 against the
   LIVE open-row count. Release births strictly while banked-closures(window) > births(window):
   order = kernel row (intake #38 → dev-knowledge-kernel; if arithmetic forbids even it, land
   §6.5's dated deferral instead — never silence) → N5 §4.5 review-linkage row → then N3's own
   order, hard cap 5+1 total. Each birth via the generator from the pack's draft source; each
   consumes its draft (mark consumed in your artifact). Intake status flips for intakes whose
   carrier/deferral landed: DRAFT → ACCEPTED, per the anti-orphan rule you just recorded.
5. **LESSONS promotion:** per architect ruling — split candidate 7 into its two incidents;
   candidates 8+9 relocate to the channel-runbook draft home ([#539]/[#540] refs), NOT
   LESSONS; reconcile candidates 1–2 against the Phase-0 artifact as N5 flagged; promote the
   remainder (append-only).
6. **[#534] corroboration pointer:** append N4's 6.9% locator-rot measurement as an evidence
   ref on [#534]'s row (generator edit).
7. **Architect L-5 rulings transcription:** the 8 rulings (#122 #323 #407 #450 #449 #406 #281
   #494) arrive from the architect as a paste block AFTER the probe returns — HOLD this act
   until that block is in your session; then transcribe each verdict to its row (generator),
   closing any row whose ask the ruling fully discharges (each such closure re-runs act 4's
   arithmetic and may release a held birth).
8. **JOURNAL** one entry for the arc, anchors on ONE line. Push; both gates must pass.

## END PACKET
Per act: sha + verification line · ledger table (closures/births window totals, releases held) ·
WARN delta (expect fleet_parity −1) · intake status map #35–#39 · what act 7 still awaits.

## WHAT NOT TO DO
No scripts/tests edits · no #529/#530/#554/seam work (lanes own those) · no rulings of your own
— every verdict traces to the report, the packs, or the architect's block · no `--no-verify` ·
no `git add -A` · no branch deletions.
