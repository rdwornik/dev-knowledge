# SEAT — Act 0 delta-groom + Act 1 rulings landing

| Model | Mode | Effort |
|---|---|---|
| opus | execute (interactive, primary checkout, branch main) | high |

**Repo:** `.dev-knowledge`, PRIMARY checkout only (Q2: primary is seat-arc-only — you are the
seat arc). **Purpose:** land the architect's ruled batch in governance surfaces, discharge the
delta-groom, and return exactly TWO evidence tables for the architect's one batched ruling
reply. Governance pointer: `protocols/PLAYBOOK.md`, `protocols/STANDING_RULINGS.md` §Q
(applies at read time — never edit §Q; ratchet holds), `BACKLOG.md`, `tasks/` via
`gen_task_tree.py --emit-source` ONLY.

**Git workflow:** feature branch `seat/2026-08-20-act0-act1` off main; one commit per phase
step; pytest + `python scripts/audit.py` before any merge request; merge to main is
OPERATOR-gated, one at a time. Push-before-delete (Q3) on anything harvested.

**UNDERSTAND before acting:** the window's bar is [#555] net closure; births are charged
against banked closures (release-halt: if a step would put births > banked, STOP and report).
Failure mode to avoid: silent WARN disposition, fake-green, touching `tasks/` outside the
generator.

## Phase 1 — land the architect's rulings (verbatim, in each governing row body)
Land each text below into the named row's body via `--emit-source`; one commit per ruling
(**COMMIT** each). Do NOT touch STANDING_RULINGS.

- **R2 → [#555] body:** "DENOMINATOR (ruled 2026-08-20, architect-2): the ledger count is the
  open-row count returned by validate_backlog on main — the live instrument, not census views
  (doc-counts/census are derived views; scope mismatches are documentation defects, not
  ledger inputs). Births = new [#id] rows filed in the window; closures = rows closed in the
  window. Decomposition accounting: pointer-izing an annotation-bloated row = 0 births,
  closure-neutral. Decomposing a content-bloated parent into k children = k−1 net births,
  charged against banked closures at proposal time; insufficient headroom ⇒ the decomposition
  waits. Release-halt rule stands."
- **R1 → [#559] body (doc_rot ceiling):** "RULED 2026-08-20: ceiling stays 1320. The 19
  over-length rows resolve by Q2 triage — annotation-driven overage: pointer-ize (verdict
  detail moves to the referenced audit doc; a one-line pointer stays in the row);
  content-bloat: decomposition, proposed to the architect with R2 headroom stated, never
  executed unilaterally. Aging or disposition is not an exit."
- **R3 → [#562] body:** "RULED 2026-08-20 (per outgoing-architect Q3, amended): N1/N2 remain
  scored items. G1 = COMPARATIVE-WITH-FLOOR — candidate ≥ incumbent on refusals AND ≥1 clean
  refusal. READING (binding): at incumbent 0/2 the comparative clause is vacuous; the floor +
  control item carry the gate. Add ONE role-reminder control item; promptable failure ⇒
  routing mitigation, measured. Grok rerun requires the no-pack sandbox guard."
- **R4 → [#539] status/body:** "RULED 2026-08-20: DISPATCHED batch 1 (lane
  lane-539-ch8-codification). The 2026-09-19 Q2/Q10 deferral rider discharges with this
  dispatch."
- **R5 → the ratification carrier row:** "RULED 2026-08-20: dedicated ratification lane,
  batch 2, split per review Q4 — preps all 7 DRAFTs, transitions the 4 non-fork; #35–#37 hold
  on the architect's R7 ADR-fork ruling (never the lane's). BOTH intake generators on every
  transition."
- **R6 → [#565] body (unblocks the telemetry lane):** "PRE-RULED 2026-08-20, principle level;
  lane derives details within these: (a) library-first — stdlib logging unless a MEASURED gap
  on this repo demands structlog, recorded either way; (b) the WAL store path is .gitignore'd
  (entry ships as a fenced diff, integrator applies); (c) repo root resolved at call time via
  `git rev-parse --show-toplevel` — safe under linked worktrees, never a hardcoded
  `_REPO_ROOT`; (d) the [#530] races close test-first: release compares-and-swaps on run_id,
  never on branch tip, and resolve-once is separated from rev-parse."
- **JOURNAL:** one dated entry anchoring the Phase-1 commits (two-commit anchor pattern OK).
  **COMMIT**

## Phase 2 — mechanical executions inside the seat's budget
1. **Pointer-ize** every annotation-driven over-length row per R1 (generator only), verify
   doc_rot WARN count drops accordingly. **COMMIT** per batch of rows, not per row.
2. **#348:** verify DEAD-candidate against live evidence; if confirmed, close it. **COMMIT**
3. Triage the two undispositioned suite REDs (stale routine-rows pin; constant-refusal test):
   fix if the fix is mechanical and test-covered, otherwise carry them into Table B. **COMMIT**
   if fixed.

## Phase 3 — return exactly TWO tables (chat output, no files), then PAUSE for the architect
- **Table A — AWAITING adjudication:** rows #549 #507 #420 #331 #541 #491 + N4's 14 AWAITING:
  id · title · one-line live evidence · your live/dead/awaiting-ruling recommendation + basis.
- **Table B — forks needing the architect:** (1) R7 evidence — the #35–#37 server-side-
  enforcement ADR fork: each option in ≤3 lines with its consequence; (2) every content-bloat
  decomposition proposal from Phase 2 with R2 headroom math; (3) anything Phase 2 could not
  execute mechanically. Batched — never dripped.

**Decision budget:** ask ONLY for curated-baseline touches, rule-vs-ruling conflicts, or
unruled fork classes — everything else per contract defaults, reported in Phase 3.
**What NOT to do:** no STANDING_RULINGS edits · no tasks/ edits outside the generator · no
new folders/paths · no deletions without the architect · no WARN dispositions · no merge to
main (operator gate) · no batch-2 work.
