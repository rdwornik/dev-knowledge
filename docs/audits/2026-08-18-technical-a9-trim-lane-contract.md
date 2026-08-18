# LANE G — A9 EXECUTION, TRIM ROUTE: ROW-LENGTH WARNS UNDER THE CEILING

| Model | Mode | Effort |
|---|---|---|
| default (Opus-class) | execute — frozen contract, NO plan-mode | high |

**Governing ruling (architect, plan v1.1 §3 A9, reviewer-approved):** the 1320-char ceiling
STANDS; every `backlog-row-length` WARN gets exactly one of two routes — (i) TRIM with a
grep-verified carrier, or (ii) "accepted, ruled" disposition. **This lane executes route (i)
ONLY.** Route (ii) is the seat's register act — you REPORT candidates for it, never write it.
**ADR-110:** save this prompt as
`docs/audits/2026-08-18-technical-a9-trim-lane-contract.md`, COMMIT first.

## SCOPE — eligible rows (23; every other row is EXCLUDED)
`#552 #293 #514 #528 #417 #546 #548 #551 #547 #531 #428 #277 #549 #550 #492 #523 #412 #484
#443 #271 #361 #146 #553`
**EXCLUDED — owned by live lanes or scheduled session acts, do not touch even if over-ceiling:**
`#533 #529 #530 #554 #555 #502 #556 #557 #558`.

## HARD TERMS
- **No trim without a verified carrier (operator-reviewed term):** before deleting any prose,
  grep-PROVE the named carrier (intake / audit doc / ADR) actually holds that content. Proof =
  carrier path + matched phrase, recorded per row in the lane artifact. No carrier proven → NO
  trim → row goes on the REPORT list for the seat's route-(ii) disposition.
- **Write path = the generator only.** Edit `tasks/<id>-*.md` bodies; regenerate `BACKLOG.md` +
  manifest via `gen_task_tree --emit-source`; `--check` must exit 0. Never hand-edit BACKLOG.md.
- **Structure is untouchable:** `Done when` · `refs` · `kill-candidates` · `serialize-group` ·
  `source` · `footprint` clauses survive every trim intact (condensable, never deleted). Trim
  relocatable DETAIL prose only — the #554/#555 precedent pattern.
- **Length is measured on the RENDERED BACKLOG.md line** (whole line incl. prefix and all ·
  clauses — `validate_doc_rot.py:199`). Verify each trimmed row ≤1320 on the rendered line, not
  the tasks/ file.
- **Accretion arm (`#293 #428 #550 #553`):** trim LENGTH only; do not chase the accretion
  finding — report each row's accretion status before/after. The pre-existing accretion suite
  RED is OWNED by the seat; your work must not silently change its firing set without saying so.
- **Trivial set (`#412 #484 #443 #271 #361 #146`, ≤5% over):** trim <100 chars of genuine
  redundancy; if nothing is redundant, REPORT rather than force it.

## STEPS
**STEP 0** — contract commit. `COMMIT`
**STEP 1** — per-row worksheet in the lane artifact: current rendered length · candidate cut ·
named carrier · grep proof (or "no carrier → REPORT"). Complete the worksheet for ALL 23 before
the first trim. `COMMIT`
**STEP 2** — execute trims in batches (~8 rows per commit), regen + `--check` each batch,
re-measure rendered lengths. `COMMIT` per batch
**STEP 3** — delta measurement: `validate_doc_rot` row-length WARN count before vs after (this
lane's scope only). `COMMIT` (artifact update)

## FINAL
Targeted checks `-n 0`: `gen_task_tree --check`, `validate_backlog`, `validate_doc_rot`.
Commit-and-STOP. STOP packet: per-row table (id | before→after | carrier+proof | or REPORT) ·
WARN delta · REPORT list for the seat's route-(ii) · shas. **No merge, no closures, no status
flips, no disposition-register writes.**

## WHAT NOT TO DO
No touching excluded rows · no BACKLOG.md hand-edits · no deletion of governance clauses · no
disposition writes · no accretion-arm chasing · no new files outside the lane artifact · no merge.
