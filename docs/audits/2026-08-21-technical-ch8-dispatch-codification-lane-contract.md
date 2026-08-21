# LANE-539 — Ch8 dispatch-system codification (batch 1, lane A)

| Model | Mode | Effort |
|---|---|---|
| opus (default) | execute — no plan mode (bounded, well-specified) | high |

**Worktree ⇄ file pairing:** slug `lane-539-ch8-codification` → branch
`worktree-lane-539-ch8-codification` → this contract `LANE-539-ch8-codification.md`.
**Repo:** `.dev-knowledge` · **Purpose:** [#539] — the dispatch system lives IN THE REPO
(operator mandate P1: a lane, not a theme). Governance pointer: `protocols/PLAYBOOK.md` Ch8
("Handoff prep for the next architect — an index, not a restatement"), `STANDING_RULINGS.md`
§Q read-only.

**Done-contract (immutable):**
1. PLAYBOOK Ch8 carries the dispatch methodology: the five §Q rulings whose declared home is
   Ch8 (census reads all five ABSENT today — enumerate them from §Q, quote ids), the batch
   shape (ADR-110: one plan → N file-disjoint lanes → one integrator), lane lifecycle
   (dispatch → commit-and-STOP → serial integration → teardown with Q3 push-before-delete).
2. **Generator as the guarantee:** a `gen_lane_contract` script exists and emits a contract
   file containing, baked in: the dispatch-block template
   (`Dispatch-Lane <slug> <file> [-Effort {low|medium|high|xhigh|max}]`, model default opus,
   `--permission-mode bypassPermissions` stated), decision-budget section, worktree⇄file
   pairing line, receipt-gate fields for cloud lanes. Tests cover: emitted file parses, all
   mandatory fields present, invalid effort names rejected.
   LOCATION: derive the taxonomy-correct home from Folder Governance / dev-root schema —
   QUOTE the governing line in your artifact; if no governance line covers it, propose the
   home in your end report and mark the commit `PROPOSED-PATH`. Never invent silently.
3. Docs and code in English; hyphen-only names; logging not print; Click CLI if a CLI is
   warranted; pytest green.

**Pre-commit:** you do NOT edit `.pre-commit-config.yaml`. If Ch8/generator needs a hook
entry, ship it as a fenced proposed-diff in your final artifact — the integrator applies it.
Do not regenerate the audits index — integrator does, once.

**Git workflow:** all work on `worktree-lane-539-ch8-codification`; commit per step
(**COMMIT** markers below); `pytest` before final commit; **commit-and-STOP — never merge,
never push to main, never touch other branches.**

**Steps**
1. Read `CLAUDE.md`, PLAYBOOK Ch8 as-is, §Q. UNDERSTAND: enumerate the five Ch8-bound rulings
   and the current Ch8 gap in `ARTIFACT-lane-539.md` at the worktree root. **COMMIT**
   Do NOT write anywhere under docs/audits/ — the archival lane owns that tree this batch;
   the integrator relocates your artifact per governance.
2. Write Ch8 content (index-style, not restatement). **COMMIT**
3. Build `gen_lane_contract` + tests (location rule above). **COMMIT**
4. Library-first line in the artifact: what existing pattern/template was checked before
   hand-rolling the generator, one line.
5. Terra review: run `/codex-review` on the diff; write the severity tally INTO the final
   artifact; fix P1/P2 findings. **COMMIT**
6. Final: pytest green, one end-of-lane artifact (what changed · proposed diffs · tally ·
   open items), **COMMIT, then STOP.**

**Decision budget:** zero interactive questions — decide per defaults, report everything in
the end artifact. **What NOT to do:** no merges · no tasks/BACKLOG edits · no §Q edits · no
new folders without the quoted-basis/PROPOSED-PATH rule · no deletions · no pre-commit edits
· no audits-index regeneration.
