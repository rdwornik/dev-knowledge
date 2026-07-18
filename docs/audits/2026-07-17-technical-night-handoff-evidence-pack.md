# HANDOFF EVIDENCE PACK — 2026-07-17 night (INPUT ONLY — NOT a bundle)

- **Class:** technical (ADR-101 enum) · **Date:** 2026-07-17
- **Source:** 2026-07-17 night-run scratchpad (`HANDOFF-EVIDENCE-PACK.md`), content unchanged below this block.
- **Night rule:** the run was READ-ONLY / zero-commit — no writes to any real repo tree; all
  outputs went to scratchpad. This docs-only arc (branch `docs/2026-07-17-night-audit`, filed
  2026-07-18) is its first commit.
- **Companion night-run audits (same arc):** `2026-07-17-technical-night-verdict-sheet.md`, `2026-07-17-technical-night-divergence-ledger.md`, `2026-07-17-technical-night-live-fire-sheet.md`, `2026-07-17-technical-night-handoff-evidence-pack.md`.

> Per operator instruction: this is **evidence for the morning session + the eventual bundle**.
> The handoff bundle itself was **NOT generated** tonight (explicitly forbidden). Bundle happens
> on the operator's explicit go at true session end.

## Today's shipped map (first-parent merges to main, 2026-07-17)

| SHA | arc | closes/refs |
|---|---|---|
| `ca8d3903` + `4de214ea` + `9fe3cc17` | **ARC 1 — ADR-102** parity enforcement-gate-rev axis; corp split → GATE_AHEAD_DECLARED; cleared the sole fleet_parity WARN | closes **#336** |
| `6a74fc7c` | **ARC 3 — ADR-103** parity-surfaces ownership + reason axis (73 rows classified 52/9/12; shared no-fork grammar; terra CLEAN r2) | closes **#316** |
| `a37a4056` | **ADR-29** chronological legacy-split **amendment (Proposed)** + JOURNAL/audit anchors | **#339** |
| `e0cbffdb` (HEAD) | **ADR-29 RATIFIED** — chronological legacy-archival split; atomic cross-doc canon reconciliation | **#339 sanction** |

Also merged today: ADR-102 ratification JOURNAL anchor, corp-monorepo executor v5 bundle + filled
supplement, ai-council P4/P6 handoff bundles, Codex role-governance arc (#341 producer mechanism),
grooming-close #312/#313, token-log snapshot.

## Verification verdicts (full detail: NIGHT-VERDICT-SHEET.md)

- **P1.1 ship-gate:** GREEN — 14 WARN dispositioned, 0 new, no `[stale]`.
- **P1.2 fleet_parity:** 161 at-parity · **0 warn-undeclared · 0 must-absent** · 1 gate-ahead-declared · 0 refused · ownership 52/9/12.
- **P1.3 pytest:** 1589 passed, 3 skipped (exit 0) + targeted fleet_parity tests green.
- **P1.4 ADR-29 coherence:** all 6 touchpoints consistent + **ratified** (region extracts byte-match; by-scope split correctly still-rejected).
- **P1.5 roster/index:** recent-adrs 99..103; doc-counts 1592=1589+3 / 29 checks / 15 gates; audits index coherent (lists **4** codex artifacts today, prompt said 2 — undercount, not rot).

## Live-fire (full detail: LIVE-FIRE-SHEET.md)

**S1–S7 all FIRED** (0 SILENT). fleet_parity loader refusals (S3/S4), gate-ahead undeclared/drift
WARN (S1/S2), corpus-catch-up stale (S5), block-ff-push refusal (S6), ship-gate RED on an
undispositioned WARN (S7) — each with a verbatim trigger line. Honest nuances recorded (row-level
refused = exit 0 WARN-posture, not exit-2; S7 sandbox baseline RED = the known clone-dir-name
artifact). Sandbox torn down; **hub tree byte-identical to P0**.

## Divergence ledger (full detail: DIVERGENCE-LEDGER.md, incl. P3 sol pass)

Cross-consumer toolchain/infra witnessed at file level (L1–L9). Headline: the feared silent
divergence is mostly (a) already fleet-aligned (ruff **gate**, root sanctioning) or (b) divergent
-with-a-real-reason. sol corrected 6 of my findings (notably the `.mypy_cache` "gap" = a witness
false-negative, RETRACTED). Post-sol actionable set: 2 trivial hub edits, 1 consumer cleanup, 1
defect to close, 1 real measurement gap (ruff **rule-set** — aligned gate, unaligned lint rules,
unmeasured).

## ⚠ FLEET-NOT-QUIESCENT (material for the bundle)

A **parallel night session ran against the fleet tonight**:
- corp-monorepo on branch `docs/2026-07-17-night-process-audit`; HEAD advanced **560a38d → 2454a6f**
  (3 external commits) during this run.
- ai-council gained `docs/audits/2026-07-17-night-batch-empirical-e2e-audit.md` (untracked) + a live
  `config/settings.yaml` edit (toggled during the run).
- **NONE of this is my activity** (I made zero real-tree writes; read-only + local clones only).
- **Implication:** the ledger's corp/ai rows were witnessed ~22:40–23:00 and may have shifted.
  **Re-witness corp/ai before executing any consumer alignment arc.**

## Open items (state as of tonight)

| id | P/size | title | status tonight |
|---|---|---|---|
| **#337** | P2/S | promote fleet_parity → blocking `ALL_CHECKS` member | **NOW READY** — peg #336 LANDED today; tonight's fleet run = 0 warn-undeclared (zero-WARN steady state holds). The prompt's **ARC 2**. |
| **#339** | P3/S | LESSONS legacy-split **build leg** | UNBLOCKED — ADR-29 now ratified. LESSONS at 241 < 300 → likely "record not-yet-needed" + build the A2 byte-identity helper + ADR-39 registry entry already landed. |
| **#342** | P3/S | fleet_parity gate-ahead max-fidelity hardening (3 items) | deferred from #336; open. |
| **#300** | P1/M | hermetization rulings **d.i/d.ii/d.iii** (the residual rulings) | DEFER — peg BEFORE Wave-2. |
| **#341** | P2/S | Codex producer-lane activation mechanism | open (EPIC-H producer axis). |
| **#338** | P2/S | codex-review drift consolidation (a–e) | open (successor to #333). |
| D-queue | — | nightly-triage findings (#47,#45,…,#19 — 15 await per SessionStart) | Issues tab; unreviewed. |

## Session hygiene note

- `logs/FLEET-PARITY.md` in the REAL hub was rewritten by the P1.2 `fleet_parity.py` run (it is a
  **gitignored** digest — `--write` default). This is NOT a tracked-tree change (git status hub = CLEAN).
  All P4 sandbox runs used `--no-write`. No real-tree tracked file was touched by this session.
