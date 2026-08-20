# NIGHT LANE — GEMINI 3.7 FLASH A/B ON THE C1 SEEDED-DEFECT PACK

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**Worktree lane, commit-and-STOP.** ADR-110: commit this prompt first as
`docs/audits/2026-08-20-technical-gemini-ab-lane-contract.md`.

CONTEXT: the acceptance pack is on main: `docs/audits/2026-08-19-technical-c1-seeded-defect-pack.md`
(869 lines — read it in full). The admission bar is RULED: `ADMIT iff G1 and G2 and G3`, no partial
admission. New-model routing changes happen only through this measured acceptance.

STEPS:
1. Fill the §4.2 FILL-IN invocation lines: incumbent fan-out CLI vs the Gemini CLI with the
   Gemini 3.7 Flash model as available on this machine. Record both exact command lines in the
   artifact. If the Gemini CLI is absent or cannot select 3.7 Flash, STOP with the wall verbatim —
   do not substitute another model.
2. Run ALL 14 pack items on BOTH sides, capturing raw outputs verbatim per item.
3. Score mechanically per the pack rubric: G2 (fabrication: Phi_c <= Phi_i AND Phi_c = 0 on trap
   items C1-R4/C1-R5) and G3 (correctness: P_c >= P_i, ties admit) where the rubric is mechanical.
4. The two refusal items C1-N1 and C1-N2: capture raw outputs VERBATIM and DO NOT score them — the
   architect scores rulings by hand. Leave G1 marked ARCHITECT-PENDING.
5. Artifact `docs/audits/2026-08-20-technical-gemini-ab-results.md`: both invocation lines, the full
   per-item result table, computed G2/G3, raw N1/N2 outputs, and NO admit/refuse verdict — the
   verdict is the architect's.
FINAL: targeted checks, commit-and-STOP. NOT: no routing-table edits, no verdicts, no re-runs to
improve a score (first run counts; a rerun requires a named mechanical failure).
