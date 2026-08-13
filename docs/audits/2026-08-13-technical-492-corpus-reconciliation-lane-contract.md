# CORPUS-492 — Seeded-defect corpus reconciliation (gates the 2026-08-17 Grok re-check)

## Dispatch
```
model: sonnet
worktree: lane-e-492-corpus-reconciliation
label: corpus-492-reconciliation
effort: medium
mode: auto
```
Note to the executor: the fields above are canonical; if the helper's exercised syntax (the corrected W3 line) differs in form, mirror that form verbatim with these values. Letter `e` = confirm next free letter against the manifest at step 0.

## Repo + Purpose
`.dev-knowledge`. Purpose: reconcile seeded-defect corpus v0.1 to the **landed** lint spec — the 11/12 verdicts currently pinned to `extend-select = []` are re-derived against the spec as merged, each verdict re-pinned with its locator — so the `[#492]` Grok re-check (due **2026-08-17**) runs against a corpus that measures the repo we actually have. Row-is-the-spec: `[#492]`'s own text + the corpus artifact govern; this contract adds no scope.

## Why this lane is legal beside W3 (stated, not assumed)
File-disjoint by construction: this lane touches ONLY the corpus artifact + its reconciliation note (docs) — no `scripts/`, no `tests/`, no `tasks/` bodies, no PLAYBOOK. Shared append-surfaces (JOURNAL on own branch; BACKLOG `[#492]` row note) follow regenerate/append convention. If reconciliation turns out to require ANY file W3's contract names, STOP and batch the question — do not proceed into overlap.

## Steps
1. **Step 0 self-serve:** commit this contract per I-D3; manifest amendment marker; confirm worktree letter. → COMMIT
2. Re-derive each of the 12 verdicts against the landed spec; re-pin with locator; where a verdict flips, record old→new with the one-line reason. → COMMIT
3. Reconciliation note appended to the corpus artifact (declarative wording; ratchet ≤ 441 if any PLAYBOOK-adjacent prose is touched — none is expected). → COMMIT
4. `[#492]` row: reconciliation leg recorded done; re-check remains scheduled 2026-08-17 (no date move). → COMMIT

## Lane discipline
V-2 decision budget stated back in one line · JOURNAL on the lane branch · commit-and-STOP, never self-merge · questions batched · no births · expected-REDs: none for a docs lane — any suite change is a defect, report it.

## Review
**Terra: waived — docs/data-only lane, no code impact** (one-line waiver; conditional: if any `scripts/` file is touched, the overlap STOP above already fired first).

## Done-when (frozen)
(1) 12/12 verdicts pinned to the landed spec with locators, flips recorded old→new; (2) reconciliation note in the artifact; (3) `[#492]` leg recorded, date unmoved; (4) lane packet: shas · flip count · decision-budget report · confirmation that no W3-named file was touched.
