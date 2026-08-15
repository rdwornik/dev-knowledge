# CONTRACT N — [#528] legs 1+2, lane-latency · worktree `lane-n-528-legs12-latency`
**Purpose:** leg (1) gate-run call sites take `-n auto --dist worksteal` (with `--max-worker-restart=0` in gate contexts); leg (2) tiered-suite doctrine written into PLAYBOOK/ESSENTIALS: "targeted in-lane, ONE full suite at integration" + the D5.2 settings ladder (maxprocesses; `-n 0` under forking parents — `-p no:xdist` is NOT serial; `--dist loadfile/loadgroup` for oracle+corpus tiers; `-p no:cacheprovider` in hooks; stray-worker detection note) + the oracle-tier correctness rule (a lane touching safe_remove/reverse_dep_oracle MUST run the oracle tier). Leg (3) is NOT yours (owed after [#529] lands).
**OWNED-FILES manifest (CANDIDATES + derivation, review 2b):** candidates: the Python call sites that invoke pytest for gate purposes + `protocols/PLAYBOOK.md` + `protocols/ESSENTIALS.md`. STEP 0 DERIVES the exact list from the repo (grep the pytest invocations, quote each locator). **HARD EXCLUSION: `.pre-commit-config.yaml` and any hook script are lane O's property — if a gate-run call site lives there, EXCLUDE it, list it in the packet as "owed at integration", and do not touch it.**

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
Problem: full suite ~15:18 taxes every merge; settings that make xdist safe on Windows are evidence-backed (NB2-D) but unadopted. Risk: colliding with lane O; codifying before deriving. Failure mode: a doctrine paragraph that contradicts the measured exclusion set.

## Steps
0b. COMMIT — print the DERIVED manifest (exact files + locators) as a packet artifact before editing.
1. COMMIT — leg 1: flags at the derived call sites (excluding O's files).
2. COMMIT — leg 2: the doctrine paragraph(s), declarative phrasing (ratchet!), citing the measured basis (serial 701.6s vs -n auto 473.0s INDICATIVE-cloud; host full suite 918.9s).
3. Targeted tests: any test files covering the touched call sites. Packet lists exclusions owed at integration. STOPPED.
