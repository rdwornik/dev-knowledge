# CONTRACT R — gate-close: drain the 8 top-decile rows · worktree `lane-r-gateclose-drain8`
**Purpose:** close the WARN ledger's decision class: drain history-accretion at tasks/ source for `#344 #514 #423 #430 #415 #487 #523 #428` (ruled in SESSION-PLAN §2), keep ruled-peg dated blocks (escape clause), regen via `gen_task_tree.py --emit-source`.
**OWNED-FILES manifest:** those 8 `tasks/<id>-*.md` files (+ regen surfaces).

## Common law (all phase-1 contracts)
| Model | Mode | Effort |
|---|---|---|
| per dispatch line | auto (zero design freedom beyond stated steps) | per dispatch line |
- Repo: .dev-knowledge (primary = operator's checkout; you are in your own worktree/branch).
- Read CLAUDE.md first. Gotchas: PYTHONUTF8=1 on console errors; manifest-first when closing rows; BACKLOG.md is GENERATED (edit tasks/ source + `python scripts/gen_task_tree.py --emit-source`); freshness-gated docs need a genuine full re-read before stamp moves; silent_rule_ratchet — phrase doc additions declaratively, no new must/shall/never tokens.
- Env: `uv sync --locked --group analytics` before anything (17/19 prior lane reds were this miss).
- Git: work ONLY on this lane's branch in this worktree; commit per step with the step name; NEVER merge, NEVER push main, NEVER --no-verify, NEVER SKIP=.
- T_start: first line of your packet records dispatch timestamp.
- Tiered suite law: targeted test files in-lane only; the full suite runs ONCE at batch integration, not here.
- Decision budget: decide per defaults and REPORT in one end-of-arc packet. STOP-and-report only for: (a) curated-baseline touches, (b) rule-vs-ruling conflicts, (c) a fork class with no standing ruling. Never drip questions.
- File discipline: step 0 prints your OWNED-FILES manifest; you modify NOTHING outside it (BACKLOG/manifest/audit-index regens excluded — regen-at-merge surfaces). Zero births of [#id]s. No register/STANDING_RULINGS edits unless your contract names them.
- Packet: ONE .md — T_start · manifest as executed · per-step commit shas · targeted-test evidence · deviations self-reported · final "STOPPED" line.
## What NOT to do (all lanes)
No merges · no pushes to main · no new ids · no new repo folders/paths (homes derive from quoted governance sources only) · no deleting content without an explicit contract step · no full-suite runs · no edits outside the manifest · no answering stop-hooks with new scope.

## UNDERSTAND
Problem: 8 genuine ≥p90 accretion rows keep the gate RED. Risk: draining a ruled peg; mis-draining a YOUNG row. Failure mode: paper-thin rows that lose load-bearing history.

## Steps
0b. COMMIT-if-changed — **[#523] verification (review item 3):** born 2026-08-12. Read its history: if the fat is its own BIRTH content → drain = trim the birth text, say so in the packet; if the accretion metric misfires on young rows → EXCLUDE #523 from the drain, and write the finding (metric misfire on <p-age rows) into the packet as a filed observation — no register edit, no birth.
1. COMMIT — drain the (7 or 8) rows: condense dated blocks info-preserving (git retains text), keep ruled pegs verbatim, regen.
2. Targeted check: `python scripts/audit.py ship-gate` — expect doc_rot backlog-accretion count to drop by the drained n; quote before/after lines. Packet states expected end-state math: 11 − n − (3 Y-3 landing with owners) → 0. STOPPED.
