---
intake-id: 25
status: DRAFT
origin: sealing 2026-08-04/05 architect, operator-directed retrospective + web research 2026-08-05; landed post-seal by operator instruction
---
# INTAKE DRAFT — simplification & distribution wave: adopt the commoditized layers, keep the edge
*(functional mode — WHAT/WHY; receiving architect triages, routes ADR-vs-rows, sequences under plan-governs. Provenance: sealing 2026-08-04/05 architect, operator-directed retrospective + web research 2026-08-05. Companion to intake #24 — extends its "buy commoditized walls" strategy from CI to the WHOLE distribution and object layer.)*

## WHY — the self-critique this intake encodes
Retrospective finding, stated without cushioning: the fleet hand-rolled THREE layers that are industry-solved, while correctly hand-building the one layer that is not. (1) **Structure propagation**: the [#383] per-surface waves and the parity manifest hand-walk what template-update tooling (copier) does with a merge-and-flag update command per consumer repo. (2) **Hook distribution**: carrier_mesh hand-copies scripts that pre-commit natively distributes by hub-repo reference + pinned rev — the [#498] exec-bit defect lived exactly in that hand-rolled path. (3) **Row-object machinery**: IDs, single-status enums, links with incoming auto-calculation, ID-regex build-stops, schema validation of fields and relationships — the exact feature list of sphinx-needs — were rebuilt as gen_task_tree + validators. Honest scope: ~30–40% of hand-rolled code sits in these three layers. The enforcement organs (JOURNAL anchoring, review-artifact coverage, git discipline, ship-gate) are NOT commoditized anywhere — they are the fleet's edge and stay build. Strategy unchanged from intake #24, list corrected: **buy the walls AND the plumbing; build only the organs.**

## WHAT — candidates, priority-ordered by value

**W-1 — copier: the methodology as a LIVING TEMPLATE (answers "how do we deploy and manage the methodology on other repos").**
Kernel of the idea: the deployable shape of .dev-knowledge becomes a copier template (folder/file structure, naming, pyproject skeleton, .pre-commit-config, tasks/ schema, CLAUDE.md skeleton). New repo = `copier copy`; methodology change = edit template once, each consumer runs `copier update` — changes merge, conflicts flag, drift is VISIBLE instead of hand-audited. Directly mechanizes L0 (names + structure as managed state) and re-frames [#383]: remaining five surfaces become template content, waves become `copier update` runs. Answers-file per repo records template version = parity is a version comparison, not a walk. Evaluation bar: pilot on ONE absent-from-manifest repo (e.g. win-tooling) — template the kernel surfaces, measure the update flow against one deliberate template change.

**W-2 — kernel/lab split + kernel as installable package (answers "base for libraries, paths, what to pull").**
Tier every ALL_CHECKS member: `kernel` (portable, consumer-grade: git discipline, JOURNAL anchor, backlog schema, review-artifact coverage — target 8–12) vs `hub` (methodology-lab: doc_rot, silent_rule_ratchet, parity internals). The kernel ships as an installable package from the hub (git-tag-pinned dependency: `uv add dev-knowledge-kernel @ git+<hub>@vX.Y`), so consumers pull versioned CODE by reference; the hub repo is the base. Python unification rides the same vehicle: kernel package pins `requires-python`, uv `required-version`, and exposes a shared ruff config consumers `extend`. One version bump = fleet-wide toolchain move.

**W-3 — pre-commit native distribution replaces carrier_mesh's copy path for hooks.**
Consumers' `.pre-commit-config.yaml` references the hub repo + rev; `pre-commit autoupdate` is the propagation cadence. The [#498] class (a bit lost in hand-copying) becomes structurally impossible — pre-commit installs from the source repo. carrier_mesh retains only what pre-commit cannot carry (non-hook assets), which W-1's template then absorbs. Evaluation: one consumer repo, hooks via reference, diff behavior vs carried copies.

**W-4 — GitHub reusable workflow as the ONE CI definition (extends intake #24 P1 across the fleet).**
`kernel.yml` lives in the hub; every consumer's workflow is three lines of `uses: <hub>/.github/workflows/kernel.yml@v1`. The second wall is written once, versioned, and referenced — not copied nine times. Rides intake #24 P1's plan-limit verification.

**W-5 — pytest-testmon for the dev loop (operator-endorsed).**
Test-impact analysis: dependency DB via Coverage.py, re-runs only tests affected by the change. Directly attacks the 410s-per-run pain; industry reports ~2× median CI reduction. Placement: dev-loop and pre-commit tier ONLY — the full suite remains the pre-merge and CI gate (testmon narrows the loop, the wall stays full). Eval: one week side-by-side, count missed-selection incidents (expect 0) and minutes saved.

**W-6 — schema-as-code for governed YAML + tasks frontmatter (check-jsonschema / pydantic).**
Schemas replace hand validators for ecosystem/*.yaml and tasks/*.md frontmatter; field `description` lives IN the schema — which also structurally resolves the recorded ecosystem-prose vs silent_rule_ratchet tension (prose moves to the schema, data files go quiet). Eval on one file family first.

**W-7 — sphinx-needs: adopt-as-pattern now, migration STUDY as a research row (not adoption).**
Its feature set (ID regex enforced at build, one-status-from-enum, links with auto incoming, conditional links validated at build, JSON-schema over fields/relationships, needs.json import/export incl. EXTERNAL cross-project needs) is the industry twin of our object layer. Two extractable wins without migration: (a) needs.json as the fleet interchange/aggregation format candidate (one dashboard over nine repos' objects); (b) its conditional-link validation pattern for our kill-candidates/depends-on edges. Full migration is a study row with a measured pilot, not a commitment — our markdown+scripts stack is load-bearing.

**W-8 — local-copy vs hub-reference ruling matrix (the operator's explicit ask — proposed as the standing rule):**

| Fleet asset | Mode | Vehicle |
|---|---|---|
| Enforcement code (kernel checks, hooks) | REFERENCE, version-pinned | W-2 package + W-3 pre-commit rev |
| Structure, naming, config skeletons | REFERENCE with merge | W-1 copier template + answers file |
| CI definition | REFERENCE | W-4 reusable workflow @tag |
| Toolchain pins (python, uv, ruff base) | REFERENCE | W-2 package metadata |
| Repo's own tasks/, JOURNAL, ADRs, state | LOCAL, always | the repo's identity — never templated |
| Methodology docs (PLAYBOOK etc.) | LOCAL pointer to hub version | template stamps the version, hub hosts the text |
Principle: **code and structure by reference (versioned, updatable), state and identity local.** Every "carry" the fleet does today gets re-homed into one of these vehicles or explicitly ruled an exception.

## North Star delta (what this changes on the ladder)
L0 and L2 stop being hand-advanced: structure conformance becomes `copier update` + a version check (L0), deployment becomes package/rev bumps (L2). [#490] parity-9/9 gains a cheaper path: joining the fleet = adopting the template, and the manifest reads answers-file versions. The [#383] row's remaining surfaces are re-triaged as template content — the receiving architect rules whether the row re-scopes onto W-1 (recommended for evaluation) or continues hand-waves. L4 gets its first proof that the research→rule→distribute lane pays: this intake IS an L4 artifact.

## Sequencing note (not binding)
W-5 and W-6 are independent quick evals (any gap-week). W-2 tiering is the design keystone and precedes W-1/W-3/W-4 (you template and package what the tiering names). W-1 pilot on one absent repo doubles as [#490] progress. §F honesty: ~6–8 births; the close engine remains [#487] — and W-1/W-3, if adopted, RETIRE standing work (surface waves, carrier copy-legs), so this intake is net-negative on fleet effort at steady state. Risk posture per operator: run evals immediately and in parallel; adopt fast on pass — the bar stays "measured divergence", the tempo is not cautious.

## Do-not-relitigate carried
Renovate (L4 owns revisit) · PyDriller · Backlog.md-as-engine · public repos for CI · towncrier/git-cliff (JOURNAL is narrative) · cookiecutter/cruft where copier is evaluated (copier's built-in update + migrations is the differentiator; do not split the eval across three tools).
