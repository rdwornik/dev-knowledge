# W4b — Done-when conversions, group B (18 rows)

## Dispatch
```
claude --bg --model sonnet --effort medium --worktree lane-i-conversions-w4b --permission-mode bypassPermissions "[dk · w4b · conversions] Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\W4B-conversions.md — step 0 commits the contract of record; run the /lane-boot sequence from step 3 onward, commit-and-STOP."
```
**Dispatch only after W3 (lane-c) is merged to `main` and the operator gives the wave GO.**

## Assigned ids (18 — group B of the 2026-08-13 partition print, unchanged)
324, 338, 341, 344, 346, 347, 349, 350, 351, 353, 356, 357, 358, 361, 362, 364, 366, 371

## Repo + Purpose
`.dev-knowledge`. Purpose: convert each assigned row's Done-when from prose to its mechanically-testable form, applying the ready census P1/P2 conversion DRAFTS verbatim-with-adaptation. This is `[W4]` wave-1 work — the biggest under-100/zero-untestable lever. The census drafts are the spec; this lane designs nothing.

## Hard laws pinned in-contract
- **G-6:** any recorded-reason surface is `STANDING_RULINGS` — not relitigated in-lane.
- **L14** (LESSONS.md) applies to this lane — read it at boot and obey.
- **Regenerate, never hand-merge:** `BACKLOG.md` + `tasks/manifest.json` are regenerated via the generator at close; never hand-edited.
- File footprint: `tasks/<id>-*.md` for assigned ids ONLY, + regeneration outputs + own contract/JOURNAL. Nothing else.

## Steps
1. **Step 0 self-serve:** commit this contract (I-D3) + manifest amendment marker; confirm worktree letter free; **verify each assigned id is `status: open` live — a closed/in-flight id is SKIPPED with a one-line note, never converted, never failed on.** → COMMIT
2. Per id: apply its census conversion draft to the row's Done-when; where the draft is missing or stale against the live row, SKIP with note (batched, never dripped). Commit in batches of ~5 rows. → COMMIT ×N
3. Regenerate BACKLOG + manifest; verify `validate_backlog` OK. → COMMIT
4. JOURNAL on the lane branch. → COMMIT

## Lane discipline
V-2 decision budget stated back in one line · commit-and-STOP, never self-merge · questions batched in the packet · no births, no closes, no `CLAUDE.md`/`ARCHITECTURE.md`/`scripts/` edits · ratchet ≤ 441 (Done-when wording is declarative by construction) · expected-REDs: none — any suite change is a defect, report it.

## Review
**Terra: waived — docs/data-only lane, no code impact** (one-line waiver).

## Done-when (frozen)
(1) Every assigned OPEN id's Done-when is mechanically testable per its draft — grep over the assigned set shows zero remaining prose-only Done-when except SKIPPED ids; (2) every SKIP carries its one-line reason; (3) regeneration clean, `validate_backlog` OK; (4) lane packet: shas · converted/skipped counts · decision-budget report.

## Step 0 execution note (this lane's judgment call, recorded per lane discipline)

**"Manifest amendment marker"** in step 1 above is inherited boilerplate from the master W4
contract skeleton (`docs/audits/2026-08-12-technical-night-2-lessons-governance-strategy.md`
§(b)), which describes a single unified W4 lane flipping the batch-4 manifest's `PENDING-CONTRACT`
row. This dispatch instead split W4 wave-1 into four parallel sibling lanes (`h`/`i`/`j`/`k` ·
groups A–D), and this contract's own **File footprint** clause restricts this lane to
`tasks/<id>-*.md` for the 18 assigned ids + regeneration outputs + this lane's own
contract/JOURNAL — **"nothing else"**, which excludes hand-editing the shared
`docs/audits/2026-08-11-technical-batch-4-manifest.md` (a file three concurrent sibling lanes
would otherwise collide on). Resolved as: this contract-of-record commit (I-D3) **is** this
lane's manifest-amendment marker — recorded here rather than as an edit to the shared manifest
file. Flagged for the integrator to reconcile the shared batch-4 manifest's `W4` row against the
four sibling contracts at merge time, once, rather than four times.

## Step 0 verification (live, this session)

Worktree letter `i` confirmed free/unique (`git worktree list`: h/i/j/k each a distinct
`conversions-w4[a-d]` lane). All 18 assigned ids verified `status: open` live in
`tasks/<id>-*.md` frontmatter at boot — none closed or in-flight, none SKIPPED at this step.
