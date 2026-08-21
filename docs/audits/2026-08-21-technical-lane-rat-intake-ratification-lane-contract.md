# LANE-RAT — DRAFT-intake ratification (batch 1, lane D)

| Model | Mode | Effort |
|---|---|---|
| opus (default) | execute — no plan mode | medium |

**Worktree ⇄ file:** slug `lane-rat-intakes` → branch `worktree-lane-rat-intakes` →
`LANE-RAT-intakes.md`. **Repo:** `.dev-knowledge`. **Purpose:** ruled split (R5, per
outgoing-architect Q4): PREP all 7 DRAFT intakes, TRANSITION the 4 non-fork ones. #35–#37
HOLD on the architect's R7 ADR-fork ruling — never this lane's call. You are the SOLE owner
of docs/intake/** this batch.

**Done-contract (immutable):**
1. Enumerate the 7 DRAFT intakes live. Classify: the three touching the server-side-
   enforcement ADR fork (#35–#37) vs the 4 non-fork.
2. PREP all 7: completeness pass per the intake template/protocol (quote which protocol file
   governs intakes — read it first); fixes committed per intake. **COMMIT** per intake.
3. TRANSITION the 4 non-fork to their next status, running **BOTH intake generators** on
   every transition (only one is hook-gated — running one is the known trap; show both
   command lines + exit codes in the artifact). **COMMIT** per transition.
4. #35–#37: prep only, status untouched; in the artifact write the R7 evidence block — each
   fork option in ≤3 lines with its consequence — for the architect's ruling.
5. **Carrier rows:** tasks/ is SEAT-owned — do NOT touch tasks/ or BACKLOG.md. For every
   transition that needs a carrier row (ratification without a carrier row = orphan
   violation), emit a generator-ready row spec block in `ARTIFACT-lane-rat.md` (worktree
   root); the SEAT lands them. Note in the artifact that transitions are
   PENDING-CARRIER until the seat lands the rows — the integrator sequences your merge
   AFTER the seat's so no orphan window exists on main.
6. Artifact: 7-row status table · both-generators evidence · R7 evidence block · carrier-row
   specs. `python scripts/audit.py` green of your making. **COMMIT, then STOP.**

**What NOT to do:** no #35–#37 status change · no tasks//BACKLOG edits · no archival of
intakes (lane C's deferred leg, later) · no §Q/PLAYBOOK edits · no new folders · no merges ·
docs-only: no terra. **Decision budget:** zero questions; ambiguity → prep-only + report.
