# Batch AB — manifest amendment 1 · 2026-09-16

**Seat:** integrator-AB (Opus 5, background) · **Amends:** `docs/audits/2026-09-16-technical-batch-ab-manifest.md`
(`d0fe3865`, merged `8a24f469`), which is immutable; this file is the in-batch supersession · **Base:** `main` `83b0c32f`.

The batch stays OPEN under the original manifest's frontmatter (`status: open`, `closed_by:` the close packet). This file
deliberately does not match `batch_manifest.MANIFEST_GLOB`, so it declares no second batch.

## 1 · The rulings, recorded

Operator, 2026-09-16, to integrator-AB and (directly) to the dispatcher seat:

> "Full parallel execution of the plan, not four lanes. Dispatch everything whose dependencies are on main, all at once, in
> worktrees ... the constraint is lifted and the serialisation goes with it."

> "Sequence ONLY genuine file conflicts and name them; everything else goes in parallel."

> "Log-review and charts stay held on the telemetry lane alone, and fire the moment it merges."

> "the prompt distiller is RE-SCOPED, not retired ... the replacement Done-when is 'an intent resolves to the command, skill
> and hook for a named model without the browser composing it', with the logs/prompts/ trace home as clause 1. Amend the row,
> do not close it."

**Supersedes in the original manifest:** section 4's hold of the conductor lane behind lane R's heartbeat; the three-lane
roster; sequential backfill (JOURNAL 2026-09-16 (k)). **No slot ceiling** -- the operator told the dispatcher directly to fire
everything in parallel. **Roles:** the dispatcher seat freezes and fires; integrator-AB lands this amendment as the single
writer on `main` and merges. CI enforcement stays OFF (a separate operator ruling).

## 2 · Lanes — contracts pinned by sha256 (prompts dir), every hash verified by this seat

| Lane | Rows | Ordered model / effort | Contract sha256 | State |
|---|---|---|---|---|
| `lane-ab-810-substrate-repair` | `[#810]` | sonnet / high (re-frozen) | `322250264a30056c0868048be1f89885b54a818a108bd5c790abadad32499c33` | FIRED `490d7b1f`, ran claude-sonnet-5 |
| `lane-ab-808-guard-timeout` | `[#808]` | opus / high | `2e7d91a63f11deb52a4582916da2b1ed790c5149c8d8e6826d776a9fc610afa1` | FIRED `810dac9e`, ran claude-opus-5 |
| `lane-ab-828-closure-census` | 25 Table-1 closures of `DIGEST-2026-09-16-closure-candidates.md` | producer Copilot Enterprise (unpinnable) + reviewer Codex `gpt-5.6-terra` | `95874ff3e927821c2b1dbe53590ef73a8f25caf089dce45c35e755a91b12cd3d` | fire now |
| `lane-ab-802-conductor-freeze` | `[#802]` | sonnet / high | `7ecc8b30ee367f25a3cd2dc0b6a148af0cf3847e595208f9f6bc849f6764b944` | fire now |
| `lane-ab-664-spine-witnessed` | `[#664]` | opus / high | `e68d99b0a9ebb7aa05389e78821916465dbc3e80bad5554f5ad2968280415c1c` | fire now |
| `lane-ab-694-cost-telemetry` | `[#694]` | sonnet / high | `08ffb7150c969a390ef8d6c02b31b9b097e22f78f6d32a33272307db3ed1e294` | fire now |
| `lane-ab-832-copilot-collections-comparison` | `[#832]` (lane files it) | producer Copilot Enterprise + reviewer Codex, via runner | `baa07f2d22bd6a599c3860c0bf91896eb9276c302cb7825ff6d356f80b04261f` | fire now |
| `lane-ab-833-seat-registry` | `[#833]` (lane files it) | opus / high | `978954e42252847ab3f4cd20244f55e8d2a4aefa5c387d1e196b333d2df03481` | fire now |
| `lane-ab-834-protocols-heading-gate` | `[#834]` (lane files it) | sonnet / medium | `f5e953230969d2652d80ed1f0f2d0827f0fb371677eabdbed39ceb5bed28a4fb` | fire now |
| `lane-ab-589-backlog-row-format` | `[#589]` | set at freeze | not frozen | AFTER ab-828 (section 4) |
| `lane-ab-781-management-map` | `[#781]` | set at freeze | not frozen | AFTER ab-664 (section 4) |
| `lane-ab-760-architecture-target` | `[#760]` | set at freeze | not frozen | AFTER ab-664 (section 4) |
| `lane-ab-715-path-registry` | `[#715]` | set at freeze | not frozen | AFTER ab-664, ab-760 and ab-810 (section 4) |
| `lane-ab-617-prompt-distiller` | `[#617]` (re-scoped in this commit) | sonnet / high | `1b42868c873d2bda7308a89bfbd50e635539a65fd9c5ae801e10cfa4892aeaa1` -- **STALE** | HELD: the contract predates the re-scope; the dispatcher re-freezes only on the operator's word in its own session |
| log-review `[#723]`, charts `[#705]` | `[#723]` `[#705]` | set at freeze | not frozen | HELD on ab-694 alone; fire the moment it merges |

Every lane carries, per the operator: its model explicit with ordered-vs-ran reported; library-first (FPG-1 implements
edges, `decision_coverage`, `graph_queries`, the orphan census) with new code only for what no organ answers, the gap named
as a row; a Done-when that is a witnessed refusal or a measured number; and a first commit filing or amending its own row.
The ab-828 and ab-832 lanes launch through a hand-written runner because no verb exists for a non-Claude producer
(`[#824]`).

## 3 · Ids — reserved by PUSH, not only by this table

Reserved on `origin` with `scripts/id_allocator.py reserve task-id` (refs `refs/reservations/task-id/<n>`) before this file
was committed -- the first live use of lane ab-804's allocator:

| Ids | Holder |
|---|---|
| 823-826 | integrator-AB -- filed in this commit: `[#823]` dispatch verb boots a lane with no manifest, `[#824]` no launch verb for a non-Claude lane, `[#825]` `single_flight` exits 2 not 3 on a real race, `[#826]` id blocks must be machine-read |
| 828-831 | `lane-ab-828-closure-census` |
| 832 | `lane-ab-832-copilot-collections-comparison` (its row) |
| 833 | `lane-ab-833-seat-registry` (its row) |
| 834 | `lane-ab-834-protocols-heading-gate` (its row) |

**New ids beyond those:** a lane runs `uv run --locked python scripts/id_allocator.py allocate` with `--holder` set to its
slug, inside its block below. The block is still prose (`[#826]` owns making it machine-read); the push reservation is what
holds.

| Block | Holder |
|---|---|
| 835-838 | ab-802 |
| 839-842 | ab-664 |
| 843-846 | ab-694 |
| 847-850 | ab-832 |
| 851-854 | ab-833 |
| 855-858 | ab-834 |
| 859-862 | ab-589 |
| 863-866 | ab-781 |
| 867-870 | ab-760 |
| 871-874 | ab-715 |
| 875-878 | ab-617 |
| 879-882 | log-review / charts |
| 883-890 | integrator-AB |

Lanes ab-808 (811-814) and ab-810 (819-822) keep the original section 3 blocks. **`[#827]` fell outside every block** --
that is `[#826]`'s witness.

## 4 · Sequencing — genuine file conflicts only, each named

Checked against each row's `serialize-group`, the lanes' likely footprints and the prior contracts.

| Order | Shared non-generated file(s) | Why it is a real conflict |
|---|---|---|
| ab-828 -> ab-589 | `scripts/gen_task_tree.py`, `scripts/validate_backlog.py`, `scripts/propose_row_closures.py`, the task schema | 828 closes 25 rows and files the closure-predicate / `witness:` row through the schema 589 reshapes. `[#589]` also declares `depends-on` `[#523]` (OPEN, same `serialize-group: architecture`, not in flight); 589's first commit absorbs or releases that dependency on its own row. |
| ab-664 -> ab-760 | `scripts/file_purpose_graph.py` | 760 needs a render subcommand behind `[#664]` step D, in the file 664's witnesses may repair. |
| ab-664 -> ab-781 | `scripts/file_purpose_graph.py` / the organ-index render path | Sequenced as the contract author declared it. This seat's check found the pair avoidable if 781's generator is a new script reading `ecosystem/organ-index.md`; the declared order stands. |
| ab-664, ab-760, ab-810 -> ab-715 | `scripts/file_purpose_graph.py` (root loaders); `win-tooling` `DispatchHelpers.psm1` | 715's own row is blocked on `[#664]`; 810 back-ports the deployed module into the tracked copy first. |
| ab-808 <-> ab-833 | `.claude/settings.json` | Both register hooks. 833 runs now; its `settings.json` wiring commit bases on `main` after ab-808 merges. |
| ab-834 <-> ab-617 | `protocols/HANDOFF_BOOT.md` | Moot this wave (617 HELD); when 617 fires, its `protocols/` edits base on `main` after 834 merges. |

**Checked and NOT sequenced:** ab-802 vs ab-694 (`actions_verdict.py` is 802's; 694 wires cost through `scripts/lane_boot.py`
and `scripts/merge_receipt.py` and must not edit `actions_verdict.py`); ab-810 vs ab-694 (694 wires through the hub entry
point, not `DispatchHelpers.psm1`); ab-664 vs ab-833 and ab-664 vs ab-694 (organ index only, regenerated at integration).
`.pre-commit-config.yaml` hook additions (664, 781, 834, 715) are textual and absorbed serially at merge. **Generated files
the integrator regenerates at each merge:** `BACKLOG.md`, `tasks/manifest.json`, `ecosystem/doc-counts.md`,
`ecosystem/organ-index.md`, `docs/audits/README.md`.

## 5 · Integration

One integrator (integrator-AB), serial, from the primary: each lane synced onto `main` before its merge, two-step merge with
its JOURNAL entry inside the merge commit, push per merge, Actions read as the receipt's `suite` step, teardown, receipt
closed. No tests on this workstation beyond collection. **A second integrator** is booted if handbacks queue faster than one
seat merges (a merge measured 17.6-19.2 min wall today); a handback with no receiving seat is an abandoned lane.

## 6 · Kill-candidates

none -- `[#823]` and `[#826]` are `[#804]`'s open legs (1) and (2), split out as separate witnesses in other footprints;
`[#824]` is the launch path, distinct from `[#752]`'s declared-model enforcement; `[#825]` is `single_flight`'s exit
contract, not `[#530]`'s guard (closed).
