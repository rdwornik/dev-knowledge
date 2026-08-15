# CONTRACT W2-0 — land the wave-2 draft artifact · worktree `lane-s-w20-draft-landing`
**Purpose:** bring the reviewed NB2-G draft artifact onto a main-mergeable branch, byte-faithful except the four ruled fork edits. This lane merges FIRST in the phase-1 batch (N-9): every conversion lane consumes this file from main.
**OWNED-FILES manifest:** `docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md` (+ audit-index regen).

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
Problem: 30 conversion drafts exist only on branch `claude/night2-wave2-drafts-fmbwa4`. Risk: silent divergence from the reviewed content. Failure mode: re-deriving instead of landing (violates do-not-rederive), or applying stale census drafts.

## Steps
1. COMMIT — fetch the artifact via `git show origin/claude/night2-wave2-drafts-fmbwa4:docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md` and commit it BYTE-FAITHFUL into the same path on this branch.
2. COMMIT — apply EXACTLY four ruled edits, nothing else: (a) [#364]'s draft REMOVED entirely, replaced by one line "[#364] withdrawn — obsoleted 2026-08-15, premise discharged by the 1320 threshold (Y-2)"; (b) [#391]'s draft: delete the second half (the re-expressed dead-[#384] disjunct) per ruling D6.3(a) — nightly wiring required outright; (c) [#417]'s draft: append one line noting the converted clause carries the unlanded remainder (extract shared scope list from scripts/audit.py:2625-2633) per D6.4(b); (d) confirm the [#419] draft carries its "supersedes the census draft" note (present per NB2-G §5 — verify, do not rewrite).
3. Quote the FULL diff of step 2 in your packet (the reviewer's byte-faithfulness guard).
4. Targeted checks: audit-index freshness hook green; no other file changed (git status proof in packet). STOPPED.

## Step 0 verification (live, this session)

Worktree letter `s` confirmed unique via `git worktree list` (7 sibling lanes `m/n/o/p/q/r/s`, each a
distinct topic, none named `w20-draft-landing` but this one) — branch
`worktree-lane-s-w20-draft-landing`, tree clean at boot on top of main tip `d62796ad`.

Source branch `origin/claude/night2-wave2-drafts-fmbwa4` verified live at
`104e8b12245956a5cefdd8796e33b841f318a1d8` (`git ls-remote origin`); the target path
`docs/audits/2026-08-14-technical-w4-wave2-conversion-drafts.md` verified **absent** on this branch
pre-landing — no collision.

Env seeded per the common-law line: `.claude/settings.local.json` already present in this worktree;
`ecosystem/{ai-council,corp-monorepo,corp-ops,corp-sca-time-automation,win-tooling}/state.yaml` (5
files, untracked) copied from the primary checkout; `uv sync --locked --group analytics` run clean
(5 packages installed: numpy/pandas/python-dateutil/six/tzdata); `worktree_import_proof.py` →
`NOT-APPLICABLE` (expected — the hub declares no importable package; same answer the hub always
gives, per `lane-boot` §6).

Rulings D6.1–D6.6 cross-checked live against `~/Downloads/MORNING-ADJUDICATION-2026-08-15.md` §A:
D6.3 (`#391`) RULED (a) and D6.4 (`#417`) RULED (b) both verbatim-match this contract's step 2(b)/(c)
wording — no drift between the ruling register and the dispatched contract.
